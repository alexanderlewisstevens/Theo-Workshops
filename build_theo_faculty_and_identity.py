#!/usr/bin/env python3
"""Build a computational ecology faculty longlist and Theo online-identity guide."""

from __future__ import annotations

import csv
import json
import math
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

TODAY = date.today().isoformat()
OPENALEX_BASE = "https://api.openalex.org"
ECOLOGY_CONCEPT = "https://openalex.org/C18903297"

INPUT_US_PROGRAMS = Path("ecology_grad_programs_us.csv")
OUT_LONGLIST = Path("computational_ecology_faculty_longlist.csv")
OUT_SHORTLIST = Path("computational_ecology_faculty_shortlist_theo.csv")
OUT_SHORTLIST_US = Path("computational_ecology_faculty_shortlist_theo_us.csv")
OUT_IDENTITY_GUIDE = Path("theo_online_identity_playbook.md")

# Weighted query terms tuned for computational/theoretical/quantitative ecology.
QUERY_TERMS: list[tuple[str, float, str]] = [
    ("ecological forecasting", 1.7, "forecasting"),
    ("species distribution model", 1.6, "species_distribution"),
    ("ecological niche model", 1.5, "species_distribution"),
    ("occupancy model ecology", 1.5, "occupancy_models"),
    ("joint species distribution model", 1.6, "joint_models"),
    ("bayesian ecological model", 1.7, "bayesian_models"),
    ("hierarchical model ecology", 1.4, "hierarchical_models"),
    ("theoretical ecology model", 1.8, "theoretical_ecology"),
    ("population dynamics model ecology", 1.5, "population_dynamics"),
    ("metapopulation model ecology", 1.4, "metapopulation"),
    ("food web model", 1.3, "food_webs"),
    ("ecological network model", 1.4, "ecological_networks"),
    ("agent-based model ecology", 1.4, "agent_based_models"),
    ("data assimilation ecology", 1.6, "data_assimilation"),
    ("remote sensing biodiversity", 1.4, "remote_sensing"),
    ("machine learning ecology", 1.3, "ecological_ml"),
    ("macroecology model", 1.3, "macroecology"),
    ("ecosystem model", 1.2, "ecosystem_modeling"),
]

MIN_PUBLICATION_DATE = "2019-01-01"
PAGES_PER_TERM = 2
PER_PAGE = 200
MIN_MATCHED_WORKS = 2
MAX_AUTHORS_TO_ENRICH = 550
SHORTLIST_SIZE = 90
SHORTLIST_US_SIZE = 70


@dataclass
class WorkHit:
    work_id: str
    title: str
    year: int
    cited_by_count: int
    source: str
    score: float = 0.0
    tags: set[str] = field(default_factory=set)


@dataclass
class AuthorAggregate:
    author_id: str
    name: str
    works: dict[str, WorkHit] = field(default_factory=dict)
    tag_counter: Counter[str] = field(default_factory=Counter)
    score: float = 0.0
    matched_works_count: int = 0
    most_recent_year: int = 0
    top_tags: list[str] = field(default_factory=list)
    top_journals: list[str] = field(default_factory=list)
    representative_titles: list[str] = field(default_factory=list)


def openalex_get(path: str, params: dict[str, str], retries: int = 4) -> dict[str, Any]:
    url = OPENALEX_BASE + path + "?" + urllib.parse.urlencode(params)
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "TheoWorkshopsBot/1.0 (computational ecology faculty discovery)"
                },
            )
            with urllib.request.urlopen(req, timeout=45) as resp:
                return json.load(resp)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            last_err = exc
            sleep_for = 1.5 * (attempt + 1)
            time.sleep(sleep_for)
    raise RuntimeError(f"OpenAlex request failed after retries: {url}; {last_err}")


def normalize_institution(name: str) -> str:
    text = (name or "").lower()
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    text = re.sub(r"\b(the|of|at|and)\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_us_program_institutions() -> set[str]:
    if not INPUT_US_PROGRAMS.exists():
        return set()
    names: set[str] = set()
    with INPUT_US_PROGRAMS.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            norm = normalize_institution(row.get("institution_name", ""))
            if norm:
                names.add(norm)
    return names


def fetch_term_works(term: str) -> list[dict[str, Any]]:
    works: list[dict[str, Any]] = []
    cursor = "*"
    for _ in range(PAGES_PER_TERM):
        params = {
            "filter": f"concepts.id:{ECOLOGY_CONCEPT},title.search:{term},from_publication_date:{MIN_PUBLICATION_DATE}",
            "sort": "cited_by_count:desc",
            "per-page": str(PER_PAGE),
            "cursor": cursor,
        }
        payload = openalex_get("/works", params)
        batch = payload.get("results", [])
        if not batch:
            break
        works.extend(batch)
        cursor = payload.get("meta", {}).get("next_cursor")
        if not cursor:
            break
        # Stay polite with API throughput.
        time.sleep(0.12)
    return works


def add_work_hits(
    author_map: dict[str, AuthorAggregate],
    works: list[dict[str, Any]],
    term_weight: float,
    tag: str,
) -> None:
    for work in works:
        work_id = work.get("id", "")
        title = (work.get("display_name") or "").strip()
        year = int(work.get("publication_year") or 0)
        cites = int(work.get("cited_by_count") or 0)
        source_obj = ((work.get("primary_location") or {}).get("source") or {})
        source = (source_obj.get("display_name") or "").strip()
        if not work_id or not title or not year:
            continue

        citation_factor = 1.0 + min(math.log1p(cites), 6.0) / 6.0

        for authorship in work.get("authorships", []):
            author = authorship.get("author") or {}
            author_id = author.get("id", "")
            author_name = (author.get("display_name") or "").strip()
            if not author_id or not author_name:
                continue

            position = (authorship.get("author_position") or "").lower()
            position_factor = 1.15 if position in {"first", "last"} else 1.0
            base_score = term_weight * citation_factor * position_factor

            agg = author_map.get(author_id)
            if agg is None:
                agg = AuthorAggregate(author_id=author_id, name=author_name)
                author_map[author_id] = agg

            hit = agg.works.get(work_id)
            if hit is None:
                hit = WorkHit(
                    work_id=work_id,
                    title=title,
                    year=year,
                    cited_by_count=cites,
                    source=source,
                    score=base_score,
                    tags={tag},
                )
                agg.works[work_id] = hit
            else:
                hit.score = max(hit.score, base_score)
                hit.tags.add(tag)


def finalize_aggregates(author_map: dict[str, AuthorAggregate]) -> list[AuthorAggregate]:
    out: list[AuthorAggregate] = []
    for agg in author_map.values():
        hits = list(agg.works.values())
        agg.matched_works_count = len(hits)
        if agg.matched_works_count < MIN_MATCHED_WORKS:
            continue

        agg.most_recent_year = max(h.year for h in hits)

        for h in hits:
            for tag in h.tags:
                agg.tag_counter[tag] += 1

        agg.top_tags = [t for t, _ in agg.tag_counter.most_common(6)]

        journal_counter = Counter(h.source for h in hits if h.source)
        agg.top_journals = [j for j, _ in journal_counter.most_common(4)]

        # Representative works favor high score and recency.
        reps = sorted(hits, key=lambda x: (x.score, x.year, x.cited_by_count), reverse=True)
        agg.representative_titles = [r.title for r in reps[:3]]

        topic_diversity_bonus = 1.0 + (0.035 * max(0, len(agg.top_tags) - 1))
        recency_bonus = 1.0 + (0.02 * max(0, agg.most_recent_year - 2022))
        agg.score = sum(h.score for h in hits) * topic_diversity_bonus * recency_bonus

        out.append(agg)

    out.sort(key=lambda a: (a.score, a.matched_works_count, a.most_recent_year), reverse=True)
    return out


def fetch_author_metadata(author_id: str) -> dict[str, Any]:
    short_id = author_id.rsplit("/", 1)[-1]
    payload = openalex_get(f"/authors/{short_id}", {})
    inst = (payload.get("last_known_institutions") or [{}])[0]
    summary = payload.get("summary_stats") or {}
    return {
        "works_count": int(payload.get("works_count") or 0),
        "cited_by_count": int(payload.get("cited_by_count") or 0),
        "h_index": int(summary.get("h_index") or 0),
        "i10_index": int(summary.get("i10_index") or 0),
        "institution": (inst.get("display_name") or "").strip(),
        "country": (inst.get("country_code") or "").strip(),
        "orcid": (payload.get("orcid") or "").strip(),
        "profile": payload.get("id") or author_id,
    }


def likely_faculty_status(works_count: int, h_index: int, matched_works: int) -> str:
    if works_count >= 45 and h_index >= 14 and matched_works >= 3:
        return "Likely faculty/senior PI"
    if works_count >= 25 and h_index >= 9 and matched_works >= 2:
        return "Possible faculty/senior researcher"
    return "Career stage unclear (manual check needed)"


def priority_bucket(score: float, matched_works: int, h_index: int) -> str:
    if score >= 26 and matched_works >= 6 and h_index >= 16:
        return "A - strongest fit"
    if score >= 18 and matched_works >= 4 and h_index >= 11:
        return "B - high potential"
    return "C - keep on longlist"


def why_research(top_tags: list[str], matched_works: int) -> str:
    tag_phrase = ", ".join(top_tags[:3]) if top_tags else "computational ecology methods"
    return (
        f"Recurring publication signal ({matched_works} matched works) in {tag_phrase}; "
        "worth reading recent papers for advisor-fit and funding alignment."
    )


def outreach_angle(top_tags: list[str]) -> str:
    if not top_tags:
        return "Ask about open PhD slots and how your current project could map into the lab's modeling workflow."
    chosen = top_tags[0].replace("_", " ")
    return (
        f"Lead with your interest in {chosen} and reference one recent paper where their method could be applied to your data."
    )


def in_us_program_list(inst_name: str, us_programs: set[str]) -> str:
    if not inst_name:
        return "unknown"
    inst_norm = normalize_institution(inst_name)
    if not inst_norm:
        return "unknown"
    if inst_norm in us_programs:
        return "yes"
    # Lightweight fuzzy containment check.
    for item in us_programs:
        if inst_norm in item or item in inst_norm:
            return "yes"
    return "no"


def grad_advisor_fit(institution: str, country: str) -> str:
    text = (institution or "").lower()
    university_markers = (
        "university",
        "universit",
        "college",
        " tech",
        "polytechnic",
        "school of",
        "institute of technology",
    )
    non_advisor_markers = (
        "medical center",
        "hospital",
        "museum",
        "national laboratory",
        "national lab",
        "association",
        "academy of sciences",
        "agency",
        "noaa",
        "usgs",
        "forest service",
        "consulting",
        "llc",
    )
    if any(m in text for m in non_advisor_markers):
        return "Lower (not a typical PhD advisor home)"
    if any(m in text for m in university_markers):
        return "Strong (university advisor pipeline)"
    if country == "US" and "institute" in text:
        return "Possible (verify if supervising PhD students)"
    return "Possible (manual verification needed)"


def institution_rank_multiplier(grad_fit: str) -> float:
    if grad_fit.startswith("Strong"):
        return 1.15
    if grad_fit.startswith("Lower"):
        return 0.72
    return 0.95


def advisor_competitiveness(
    priority: str, h_index: int, matched_works: int, grad_fit: str
) -> str:
    score = 0
    if priority.startswith("A"):
        score += 3
    elif priority.startswith("B"):
        score += 2
    else:
        score += 1

    if h_index >= 60:
        score += 3
    elif h_index >= 35:
        score += 2
    elif h_index >= 20:
        score += 1

    if matched_works >= 15:
        score += 2
    elif matched_works >= 8:
        score += 1

    if grad_fit.startswith("Strong"):
        score += 1
    elif grad_fit.startswith("Lower"):
        score -= 1

    if score >= 8:
        return "Very high"
    if score >= 6:
        return "High"
    if score >= 4:
        return "Moderate"
    return "Selective but variable"


def write_longlist_csv(rows: list[dict[str, str]]) -> None:
    fields = [
        "rank",
        "priority_bucket",
        "faculty_name",
        "likely_faculty_status",
        "institution",
        "country_code",
        "us_or_non_us",
        "in_existing_us_grad_program_file",
        "grad_advisor_fit",
        "advisor_competitiveness",
        "matched_works_count",
        "most_recent_matched_year",
        "computational_ecology_fit_tags",
        "openalex_h_index",
        "openalex_works_count",
        "openalex_cited_by_count",
        "top_matched_journals",
        "representative_work_1",
        "representative_work_2",
        "representative_work_3",
        "why_theo_should_research",
        "suggested_first_email_angle",
        "orcid",
        "openalex_profile_url",
        "data_source_snapshot_date",
    ]
    with OUT_LONGLIST.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_shortlist_csv(long_rows: list[dict[str, str]]) -> None:
    top_rows = long_rows[:SHORTLIST_SIZE]
    fields = [
        "rank",
        "faculty_name",
        "institution",
        "country_code",
        "priority_bucket",
        "grad_advisor_fit",
        "advisor_competitiveness",
        "focus_tags",
        "why_research_now",
        "first_action_for_theo",
        "suggested_outreach_window",
        "openalex_profile_url",
    ]
    shortlist: list[dict[str, str]] = []
    for row in top_rows:
        shortlist.append(
            {
                "rank": row["rank"],
                "faculty_name": row["faculty_name"],
                "institution": row["institution"],
                "country_code": row["country_code"],
                "priority_bucket": row["priority_bucket"],
                "grad_advisor_fit": row["grad_advisor_fit"],
                "advisor_competitiveness": row["advisor_competitiveness"],
                "focus_tags": row["computational_ecology_fit_tags"],
                "why_research_now": row["why_theo_should_research"],
                "first_action_for_theo": "Read 2 papers + draft 3-sentence fit note + log funding clues.",
                "suggested_outreach_window": "2026-08-01 to 2026-09-30",
                "openalex_profile_url": row["openalex_profile_url"],
            }
        )
    with OUT_SHORTLIST.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(shortlist)


def write_shortlist_us_csv(long_rows: list[dict[str, str]]) -> None:
    us_rows = [
        r
        for r in long_rows
        if r["country_code"] == "US"
        and r["grad_advisor_fit"].startswith("Strong")
    ][:SHORTLIST_US_SIZE]
    fields = [
        "rank",
        "faculty_name",
        "institution",
        "priority_bucket",
        "grad_advisor_fit",
        "advisor_competitiveness",
        "focus_tags",
        "why_research_now",
        "first_action_for_theo",
        "suggested_outreach_window",
        "openalex_profile_url",
    ]
    rows: list[dict[str, str]] = []
    for row in us_rows:
        rows.append(
            {
                "rank": row["rank"],
                "faculty_name": row["faculty_name"],
                "institution": row["institution"],
                "priority_bucket": row["priority_bucket"],
                "grad_advisor_fit": row["grad_advisor_fit"],
                "advisor_competitiveness": row["advisor_competitiveness"],
                "focus_tags": row["computational_ecology_fit_tags"],
                "why_research_now": row["why_theo_should_research"],
                "first_action_for_theo": "Read 2 papers + verify current PhD openings/funding + draft tailored email.",
                "suggested_outreach_window": "2026-08-01 to 2026-09-30",
                "openalex_profile_url": row["openalex_profile_url"],
            }
        )
    with OUT_SHORTLIST_US.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_identity_playbook(longlist_rows: list[dict[str, str]]) -> None:
    lines: list[str] = []
    lines.append("# Theo Computational Ecology Online Identity Playbook")
    lines.append("")
    lines.append(f"Compiled on {TODAY}. This plan is for Theo's PhD-application positioning in computational ecology.")
    lines.append("")
    lines.append("LinkedIn reference provided by user: https://www.linkedin.com/in/theo-canji-3149aa266/")
    lines.append("")
    lines.append("## Core Positioning")
    lines.append("")
    lines.append("Use one stable identity sentence everywhere (LinkedIn headline, About, CV summary, email outreach, website hero text):")
    lines.append("")
    lines.append("> I build reproducible computational models with open ecological data to forecast biodiversity and ecosystem change.")
    lines.append("")
    lines.append("Backup variants if needed:")
    lines.append("")
    lines.append("- I combine Bayesian/statistical modeling, remote sensing, and ecological data synthesis to answer applied ecology questions.")
    lines.append("- I use computational and theoretical ecology methods to predict species and ecosystem dynamics under environmental change.")
    lines.append("")
    lines.append("## Pointed Goals for Theo (90-Day)")
    lines.append("")
    lines.append("1. By 2026-04-30: finalize one 1-page research narrative (question, data, methods, result, next step).")
    lines.append("2. By 2026-05-20: publish one clean GitHub project with README, environment file, and one figure.")
    lines.append("3. By 2026-06-10: post one public methods summary on LinkedIn plus repository link.")
    lines.append("4. By 2026-06-30: build a tracked faculty shortlist from the generated CSV and read 2 papers each for top 20.")
    lines.append("5. By 2026-07-31: produce one poster-style PDF and attach it on LinkedIn Featured plus personal site/GitHub release.")
    lines.append("6. By 2026-09-30: send 12-20 targeted faculty emails with explicit funding/openings question.")
    lines.append("")
    lines.append("## LinkedIn Upgrade Checklist")
    lines.append("")
    lines.append("- Headline template: `MS Student | Computational Ecology | Bayesian Modeling | Ecological Forecasting | R/Python/GIS`.")
    lines.append("- About section: 6-8 lines with one focal research question, methods stack, and current project output link.")
    lines.append("- Featured section: add GitHub repo, poster PDF, and one technical post.")
    lines.append("- Experience section: each role gets 2 bullets with measurable outputs (dataset size, model type, reproducibility artifact).")
    lines.append("- Skills section: prioritize `R`, `Python`, `Bayesian statistics`, `Ecological modeling`, `GIS`, `Remote sensing`, `Reproducible workflows`.")
    lines.append("- Custom URL and consistent name format across LinkedIn/GitHub/ORCID.")
    lines.append("")
    lines.append("## What to Post (High Signal, Low Noise)")
    lines.append("")
    lines.append("Post cadence: 2 posts/month. Each post must include a concrete artifact.")
    lines.append("")
    lines.append("- Post type 1: mini methods note (problem, data, model, one plot, one limitation).")
    lines.append("- Post type 2: conference/workshop takeaway with specific method learned and how it changed your workflow.")
    lines.append("- Post type 3: paper replication thread (what you reproduced, what matched, what did not).")
    lines.append("")
    lines.append("Template:")
    lines.append("")
    lines.append("```text")
    lines.append("Question: [ecological question]")
    lines.append("Data: [dataset/source]")
    lines.append("Method: [model/workflow]")
    lines.append("Result: [1 quantitative finding]")
    lines.append("Artifact: [GitHub/poster/notebook link]")
    lines.append("Next step: [what you are improving]")
    lines.append("```")
    lines.append("")
    lines.append("## Research Infrastructure Theo Should Set Up")
    lines.append("")
    lines.append("- GitHub profile README with research statement, methods stack, and pinned repositories.")
    lines.append("- ORCID profile synced with publications/posters.")
    lines.append("- Google Scholar profile (if publications exist) to improve discoverability.")
    lines.append("- Simple personal site (GitHub Pages is enough): About, Projects, CV, Contact.")
    lines.append("- A single folder template for every project: `data/`, `notebooks/`, `src/`, `figures/`, `README.md`, `environment.yml`.")
    lines.append("")
    lines.append("## Faculty Research Workflow Using New CSVs")
    lines.append("")
    lines.append("1. Start with `computational_ecology_faculty_shortlist_theo.csv` and pick top 20 names.")
    lines.append("2. For US applications first, use `computational_ecology_faculty_shortlist_theo_us.csv`.")
    lines.append("3. For each person, read 2 recent papers and write one 3-sentence fit note.")
    lines.append("4. Record funding clues (RA grant, project page, lab hiring notes, graduate guarantees).")
    lines.append("5. Keep only faculty where Theo can clearly map his current project/question to their methods.")
    lines.append("6. Use this reduced list as the core application and outreach target set.")
    lines.append("")
    lines.append("## Priority Snapshot from Longlist")
    lines.append("")

    for row in longlist_rows[:20]:
        lines.append(
            f"- Rank {row['rank']}: {row['faculty_name']} ({row['institution']}, {row['country_code']}) | "
            f"{row['priority_bucket']} | {row['grad_advisor_fit']} | tags: {row['computational_ecology_fit_tags']}"
        )

    lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    lines.append("- Do not send generic outreach emails; every email must reference one specific paper and one specific method fit.")
    lines.append("- Do not list workshops/conferences on CV without output; pair each with poster, notebook, or written methods note.")
    lines.append("- Do not apply to unfunded PhD offers unless there is a clearly justified exception.")

    OUT_IDENTITY_GUIDE.write_text("\n".join(lines), encoding="utf-8")


def build() -> None:
    us_programs = load_us_program_institutions()

    author_map: dict[str, AuthorAggregate] = {}
    for term, weight, tag in QUERY_TERMS:
        works = fetch_term_works(term)
        add_work_hits(author_map, works, weight, tag)

    aggregates = finalize_aggregates(author_map)
    selected = aggregates[:MAX_AUTHORS_TO_ENRICH]

    meta_map: dict[str, dict[str, Any]] = {}
    for idx, agg in enumerate(selected, start=1):
        meta_map[agg.author_id] = fetch_author_metadata(agg.author_id)
        # Light pacing to avoid API stress.
        if idx % 10 == 0:
            time.sleep(0.35)

    rows: list[dict[str, str]] = []
    for agg in selected:
        meta = meta_map.get(agg.author_id, {})
        institution = str(meta.get("institution", ""))
        country = str(meta.get("country", ""))
        h_index = int(meta.get("h_index", 0))
        works_count = int(meta.get("works_count", 0))
        cited_by = int(meta.get("cited_by_count", 0))
        status = likely_faculty_status(works_count, h_index, agg.matched_works_count)
        fit = grad_advisor_fit(institution, country)
        priority = priority_bucket(agg.score, agg.matched_works_count, h_index)
        competitiveness = advisor_competitiveness(
            priority, h_index, agg.matched_works_count, fit
        )
        rank_score = (
            agg.score
            * institution_rank_multiplier(fit)
            * (1.0 + min(h_index, 80) / 450.0)
            * (1.0 + min(agg.matched_works_count, 20) / 120.0)
        )

        row = {
            "rank": "0",
            "priority_bucket": priority,
            "faculty_name": agg.name,
            "likely_faculty_status": status,
            "institution": institution,
            "country_code": country,
            "us_or_non_us": "US" if country == "US" else "Non-US",
            "in_existing_us_grad_program_file": in_us_program_list(institution, us_programs),
            "grad_advisor_fit": fit,
            "advisor_competitiveness": competitiveness,
            "matched_works_count": str(agg.matched_works_count),
            "most_recent_matched_year": str(agg.most_recent_year),
            "computational_ecology_fit_tags": "; ".join(agg.top_tags),
            "openalex_h_index": str(h_index),
            "openalex_works_count": str(works_count),
            "openalex_cited_by_count": str(cited_by),
            "top_matched_journals": "; ".join(agg.top_journals),
            "representative_work_1": agg.representative_titles[0] if len(agg.representative_titles) > 0 else "",
            "representative_work_2": agg.representative_titles[1] if len(agg.representative_titles) > 1 else "",
            "representative_work_3": agg.representative_titles[2] if len(agg.representative_titles) > 2 else "",
            "why_theo_should_research": why_research(agg.top_tags, agg.matched_works_count),
            "suggested_first_email_angle": outreach_angle(agg.top_tags),
            "orcid": str(meta.get("orcid", "")),
            "openalex_profile_url": str(meta.get("profile", agg.author_id)),
            "data_source_snapshot_date": TODAY,
            "_rank_score": f"{rank_score:.6f}",
        }
        rows.append(row)

    rows.sort(key=lambda r: float(r["_rank_score"]), reverse=True)
    for rank, row in enumerate(rows, start=1):
        row["rank"] = str(rank)

    for row in rows:
        row.pop("_rank_score", None)

    write_longlist_csv(rows)
    write_shortlist_csv(rows)
    write_shortlist_us_csv(rows)
    write_identity_playbook(rows)

    print(f"Wrote {OUT_LONGLIST} ({len(rows)} rows)")
    print(f"Wrote {OUT_SHORTLIST} ({min(len(rows), SHORTLIST_SIZE)} rows)")
    print(f"Wrote {OUT_SHORTLIST_US} ({min(len([r for r in rows if r['country_code'] == 'US']), SHORTLIST_US_SIZE)} rows)")
    print(f"Wrote {OUT_IDENTITY_GUIDE}")


if __name__ == "__main__":
    build()
