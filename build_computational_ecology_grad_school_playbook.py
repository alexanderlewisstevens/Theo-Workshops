#!/usr/bin/env python3
"""Generate a simple funded computational ecology PhD application playbook."""

from __future__ import annotations

import csv
from pathlib import Path

OPPS_CSV = Path("computational_ecology_opportunities.csv")
GUIDE_OUT = Path("computational_ecology_grad_school_playbook.md")
ACTION_CSV_OUT = Path("computational_ecology_grad_school_action_plan.csv")
TODAY = "2026-04-10"

NSF_GRFP_URL = "https://www.nsf.gov/funding/opportunities/grfp-nsf-graduate-research-fellowship-program/nsf25-547/solicitation"
DOE_CSGF_URL = "https://www.krellinst.org/csgf/about-doe-csgf/eligibility-program-requirements"
DOE_CSGF_BENEFITS_URL = "https://www.krellinst.org/csgf/about-doe-csgf/benefits-opportunities"
NDSEG_URL = "https://ndseg.org/eligibility"


def load_opportunities() -> list[dict[str, str]]:
    with OPPS_CSV.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def by_name(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {r["opportunity_name"]: r for r in rows}


def md_cell(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def link(label: str, url: str) -> str:
    return f"[{label}]({url})" if url else label


def compact_cost(row: dict[str, str]) -> str:
    cost = row.get("cost", "")
    access = row.get("free_or_online", "")
    if access and access not in cost:
        return f"{cost} {access}".strip()
    return cost


def cv_line(row: dict[str, str]) -> str:
    name = row["opportunity_name"]
    if name == "Ecological Forecasting Initiative 2026 Conference":
        return 'Poster presenter, Ecological Forecasting Initiative Conference, Toronto, Canada, 2026. Poster: "[Forecasting question] with [model/data source]."'
    if name == "Gordon Research Seminar: Unifying Ecology Across Scales":
        return 'Selected participant and poster presenter, Gordon Research Seminar: Unifying Ecology Across Scales, Stonehill College, 2026.'
    if name == "Gordon Research Conference: Unifying Ecology Across Scales":
        return 'Participant, Gordon Research Conference: Unifying Ecology Across Scales, Stonehill College, 2026.'
    if name == "European Conference on Mathematical and Theoretical Biology 2026 (ECMTB)":
        return 'Poster presenter, European Conference on Mathematical and Theoretical Biology, Graz, Austria, 2026. Poster: "[Modeling title]."'
    if name == "Evolution 2026":
        return 'Participant/presenter, Evolution 2026, Cleveland, Ohio, 2026. Focus: evolutionary ecology and quantitative methods.'
    if name == "NEON Data Skills Webinar: NEON Data in Google Earth Engine":
        return 'Completed NEON Data Skills Webinar: NEON Data in Google Earth Engine, 2026; built reproducible Python/GEE workflow for [ecological dataset].'
    if name == "Ecological Forecasting Initiative Statistical Methods Seminar Series":
        return 'Participant, Ecological Forecasting Initiative Statistical Methods Seminar Series, 2026; focused on [method] for ecological forecasting.'
    if name == "Data Carpentry Semester Biology Materials":
        return 'Completed self-guided Data Carpentry biology data-analysis modules; created reproducible ecology analysis repository, 2026.'
    if name == "NEON Learning Hub Tutorials":
        return 'Completed NEON open-data tutorials; built reproducible analysis of [NEON data product/ecosystem], 2026.'
    if name == "Esri User Conference 2026":
        return 'Participant, Esri User Conference, San Diego, 2026; completed training in GIS/spatial analysis for ecological data.'
    if name == "SciPy 2026":
        return 'Participant, SciPy 2026, Minneapolis, 2026; contributed to sprint/open-source workflow for scientific Python.'
    if name == "posit::conf(2026)":
        return 'Participant, posit::conf(2026), 2026; completed R/Python workflow training relevant to reproducible ecological analysis.'
    if name == "SPEC School":
        return 'Selected participant, SPEC School, [year]; completed remote-sensing and spectral ecology training.'
    if name == "BIOS2 Summer School: Biodiversity Modelling":
        return 'Participant, BIOS2 Summer School in Biodiversity Modelling, [year]; completed graduate training in quantitative biodiversity models.'
    if name == "CV4Ecology Workshop":
        return 'Selected participant, CV4Ecology Workshop, [year]; trained in computer vision methods for ecological image data.'
    return f'Participant, {name}, [year]; focus: [one specific computational ecology skill or research output].'


def application_sentence(row: dict[str, str]) -> str:
    name = row["opportunity_name"]
    if "Forecasting" in name:
        return "This matters because ecological forecasting labs want evidence that he understands prediction, uncertainty, data pipelines, and reproducible workflows."
    if "Gordon" in name:
        return "This matters because GRC/GRS participation signals serious research fit and gives him access to faculty who work on quantitative ecology at a high level."
    if "Mathematical" in name or "ECMTB" in name:
        return "This matters because it gives a direct mathematical biology signal, which is useful for theory-heavy computational ecology PhD programs."
    if name == "Evolution 2026":
        return "This matters if his computational ecology story touches eco-evolutionary dynamics, population genetics, phylogenetics, or quantitative evolutionary ecology."
    if "NEON" in name:
        return "This matters because NEON is a recognizable U.S. open ecological data source and makes a strong portfolio project possible without lab-specific data access."
    if name in {"SciPy 2026", "posit::conf(2026)", "Data Carpentry Semester Biology Materials"}:
        return "This matters only if he turns the training into a public project; attendance alone is not enough."
    if name == "Esri User Conference 2026":
        return "This matters if he wants spatial ecology, remote sensing, or GIS-heavy labs; it should be paired with a map/model portfolio project."
    return row.get("why_it_looks_good", "")


def write_action_csv(rows: list[dict[str, str]]) -> None:
    actions = [
        {
            "when": "2026-04-10 to 2026-04-15",
            "priority": "1",
            "action": "Decide whether he can submit EFI, ECMTB, Evolution support, or System Dynamics scholarship materials before the imminent deadlines.",
            "output": "One submitted abstract/support application, or an explicit decision to skip.",
            "why_it_matters": "These are the fastest ways to create a funded/presenting opportunity before PhD applications.",
        },
        {
            "when": "2026-04-10 to 2026-04-28",
            "priority": "1",
            "action": "Register for the NEON Google Earth Engine webinar and choose one NEON dataset for a small reproducible project.",
            "output": "One GitHub repo or notebook: question, data, code, figure, short interpretation.",
            "why_it_matters": "A portfolio artifact helps faculty see evidence of computational ability.",
        },
        {
            "when": "2026-04-15 to 2026-06-14",
            "priority": "1",
            "action": "Apply to GRS/GRC Unifying Ecology Across Scales if the budget and fit make sense.",
            "output": "Application plus poster title/abstract draft.",
            "why_it_matters": "Selective research settings have high advisor-networking value.",
        },
        {
            "when": "2026-05 to 2026-06",
            "priority": "1",
            "action": "Build a faculty shortlist: 12-18 potential PhD advisors, each with funding-fit notes and 2 recent papers read.",
            "output": "Faculty spreadsheet with lab, university, funding clues, papers, and fit sentence.",
            "why_it_matters": "Funded PhD admissions are advisor-fit driven in many ecology programs.",
        },
        {
            "when": "2026-06 to 2026-08",
            "priority": "1",
            "action": "Finish one polished computational ecology project and one poster-style figure.",
            "output": "GitHub repo, 1-page project summary, 1 figure, and 3-sentence pitch.",
            "why_it_matters": "This turns coursework/workshops into evidence.",
        },
        {
            "when": "2026-08 to 2026-09",
            "priority": "1",
            "action": "Email potential advisors with a short, specific message asking if they are reviewing PhD students and anticipate funding.",
            "output": "10-15 targeted emails and response tracker.",
            "why_it_matters": "This reduces wasted applications to labs without openings/funding.",
        },
        {
            "when": "2026-09 to 2026-11",
            "priority": "1",
            "action": "Draft and revise SOP/research statement around one coherent identity: ecological question + computational method + data type.",
            "output": "CV, SOP, research statement, personal/diversity statement if needed, recommender packet.",
            "why_it_matters": "Top programs need a clear research fit, not just broad interest in ecology. ",
        },
        {
            "when": "2026-10 to 2026-12",
            "priority": "1",
            "action": "Apply only where there is plausible funding: advisor has RA funding, department guarantees TA/RA, or fellowship path is realistic.",
            "output": "Final school list with funding model written next to every program.",
            "why_it_matters": "The goal is a funded PhD offer, not just an admission.",
        },
    ]
    with ACTION_CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["when", "priority", "action", "output", "why_it_matters"])
        writer.writeheader()
        writer.writerows(actions)


def profile_table(rows: list[dict[str, str]], names: list[str]) -> list[str]:
    idx = by_name(rows)
    lines = ["| Opportunity | Use it for | CV line template | Cost/access note | Source |", "|---|---|---|---|---|"]
    for name in names:
        r = idx[name]
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(name),
                    md_cell(application_sentence(r)),
                    md_cell(cv_line(r)),
                    md_cell(compact_cost(r)),
                    link("source", r["source_url"]),
                ]
            )
            + " |"
        )
    return lines


def write_guide(rows: list[dict[str, str]]) -> None:
    idx = by_name(rows)
    tier1 = [r for r in rows if r["priority_tier"].startswith("1")]
    easy_access_names = [
        "NEON Data Skills Webinar: NEON Data in Google Earth Engine",
        "Ecological Forecasting Initiative Statistical Methods Seminar Series",
        "Data Carpentry Semester Biology Materials",
        "NEON Learning Hub Tutorials",
        "iDigBio Digital Data 2026",
        "posit::conf(2026)",
        "SciPy 2026",
        "Esri User Conference 2026",
    ]
    watch_names = [
        "SPEC School",
        "BIOS2 Summer School: Biodiversity Modelling",
        "BIOS2 Summer School: Data-driven Ecological Synthesis",
        "CV4Ecology Workshop",
        "ESIIL Innovation Summit 2026: AI for Sustainability",
        "Santa Fe Institute Complex Systems Summer School 2026",
    ]

    lines: list[str] = []
    lines.append("# Very Easy Guide to a Funded Computational Ecology PhD")
    lines.append("")
    lines.append(f"Compiled on {TODAY}. Goal: help a current master's student become a credible, funded PhD applicant in computational ecology.")
    lines.append("")
    lines.append("## The Short Version")
    lines.append("")
    lines.append("He should not try to do everything. He should do three things well:")
    lines.append("")
    lines.append("1. Create one clear research identity: ecological question + computational method + data source.")
    lines.append("2. Produce one visible artifact: poster, preprint, GitHub notebook, software contribution, or polished project page.")
    lines.append("3. Apply only to labs/programs where funding is plausible: advisor RA, department TA/RA guarantee, or realistic fellowship route.")
    lines.append("")
    lines.append("A strong one-sentence identity could be:")
    lines.append("")
    lines.append('> I use Bayesian/statistical models and open ecological data to forecast how [species/ecosystem/process] changes across space and time.')
    lines.append("")
    lines.append("## What Fully Funded Usually Means")
    lines.append("")
    lines.append("For ecology PhD programs, a funded offer usually comes from one or more of these:")
    lines.append("")
    lines.append("- RA funding: a professor has grant money and pays him to work on a research project.")
    lines.append("- TA funding: the department funds him to teach while completing the PhD.")
    lines.append("- Fellowship funding: external money such as NSF GRFP, DOE CSGF, NDSEG, university fellowships, or program-specific fellowships.")
    lines.append("")
    lines.append("The rule: do not accept an unfunded research PhD unless there is an unusual reason. For every program, write down the funding model before applying.")
    lines.append("")
    lines.append("## Funding Reality Check")
    lines.append("")
    lines.append("| Funding path | Fit for him | What to check | Source |")
    lines.append("|---|---|---|---|")
    lines.append(f"| Advisor RA / department TA | Usually the most realistic path | Ask each potential advisor: Are you reviewing PhD students for Fall 2027, and do you anticipate RA/TA/fellowship funding? | Program/advisor websites |")
    lines.append(f"| NSF GRFP | Potentially excellent, but eligibility is strict for current graduate students | NSF's FY 2026 solicitation says eligible categories include current first-year graduate students in their first graduate degree program with less than one academic year completed. Because he is already a master's student, he must verify eligibility before spending time on it. | {link('NSF GRFP solicitation', NSF_GRFP_URL)} |")
    lines.append(f"| DOE CSGF | Very strong if he does serious high-performance computing, modeling, AI, statistics, or computational science | DOE CSGF lists current master's students as eligible only if they enroll at a different institution for PhD studies by the fellowship start; it also requires full-time PhD study at a U.S. university. | {link('DOE CSGF eligibility', DOE_CSGF_URL)}; {link('benefits', DOE_CSGF_BENEFITS_URL)} |")
    lines.append(f"| NDSEG | Fit-dependent; stronger if his work connects to supported STEM areas such as oceanography, remote sensing, computation, or defense-relevant environmental modeling | NDSEG is limited to U.S. citizens/nationals and doctoral study at a U.S. institution; check discipline fit carefully. | {link('NDSEG eligibility', NDSEG_URL)} |")
    lines.append("| University fellowships | Worth checking for every target program | Look for first-year PhD fellowships, graduate school fellowships, diversity fellowships, and internal nominations. | Each university graduate school page |")
    lines.append("")
    lines.append("## The Fastest High-Yield Plan")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart TD")
    lines.append("  A[Pick one computational ecology identity] --> B[Make one portfolio project]")
    lines.append("  B --> C[Submit or attend one high-signal opportunity]")
    lines.append("  C --> D[Build 12-18 advisor targets]")
    lines.append("  D --> E[Email faculty about fit and funding]")
    lines.append("  E --> F[Apply only where funding is plausible]")
    lines.append("  F --> G[Choose funded offer]")
    lines.append("```")
    lines.append("")
    lines.append("## Immediate Actions")
    lines.append("")
    lines.append("| When | Action | Output |")
    lines.append("|---|---|---|")
    lines.append("| 2026-04-10 to 2026-04-15 | Decide whether to submit EFI, ECMTB, Evolution support, or System Dynamics scholarship materials. | One submission, or a documented decision to skip because fit/timing is wrong. |")
    lines.append("| 2026-04-10 to 2026-04-28 | Register for the NEON Google Earth Engine webinar. | A NEON/GEE mini-project idea. |")
    lines.append("| 2026-04-15 to 2026-06-14 | Apply to GRS/GRC if fit and budget make sense. | Application plus poster title/abstract. |")
    lines.append("| May to June 2026 | Build a faculty list. | 12-18 advisors, each with 2 recent papers and funding notes. |")
    lines.append("| June to August 2026 | Finish one portfolio project. | GitHub repo, one figure, 1-page project summary, 3-sentence pitch. |")
    lines.append("| August to September 2026 | Email potential advisors. | 10-15 targeted emails asking about PhD openings and funding. |")
    lines.append("| September to November 2026 | Draft applications. | CV, SOP, research statement, recommender packet. |")
    lines.append("| October to December 2026 | Apply to funded-fit programs. | Final program list with funding model beside each program. |")
    lines.append("")
    lines.append("## Highest-Impact Opportunities")
    lines.append("")
    lines.extend(profile_table(rows, [r["opportunity_name"] for r in tier1]))
    lines.append("")
    lines.append("## Easy Wins and Low-Cost Signals")
    lines.append("")
    lines.extend(profile_table(rows, easy_access_names))
    lines.append("")
    lines.append("## Watch-List Opportunities for the Next Cycle")
    lines.append("")
    lines.extend(profile_table(rows, watch_names))
    lines.append("")
    lines.append("## How to Turn an Opportunity into an Application Advantage")
    lines.append("")
    lines.append("Bad CV line:")
    lines.append("")
    lines.append('> Attended ecology workshop.')
    lines.append("")
    lines.append("Good CV line:")
    lines.append("")
    lines.append('> Poster presenter, Ecological Forecasting Initiative Conference, 2026. Used Bayesian state-space models and NEON data to forecast [process] across [region].')
    lines.append("")
    lines.append("Best version:")
    lines.append("")
    lines.append('> Poster presenter, Ecological Forecasting Initiative Conference, 2026; built reproducible forecasting workflow in R/Python using NEON data; repository: [GitHub link].')
    lines.append("")
    lines.append("## Faculty-Finding Workflow")
    lines.append("")
    lines.append("For each faculty target, fill in this table before applying:")
    lines.append("")
    lines.append("| Field | What to write |")
    lines.append("|---|---|")
    lines.append("| Faculty name | Name and title |")
    lines.append("| University/program | Department and graduate program |")
    lines.append("| Why this lab | One sentence connecting his project to their work |")
    lines.append("| Methods match | Forecasting, Bayesian models, ML, GIS, remote sensing, population models, networks, HPC, etc. |")
    lines.append("| Data/system match | NEON, camera traps, remote sensing, freshwater, forests, species interactions, disease, etc. |")
    lines.append("| Funding clue | Lab hiring page, grant, RA posting, department guarantee, or direct email response |")
    lines.append("| Two recent papers | Full citation or DOI for two papers he actually read |")
    lines.append("| Email status | Not contacted / contacted / replied / meeting scheduled / not taking students |")
    lines.append("")
    lines.append("Good email template:")
    lines.append("")
    lines.append("```text")
    lines.append("Subject: Prospective PhD student interested in computational ecology and [specific topic]")
    lines.append("")
    lines.append("Dear Professor [Name],")
    lines.append("")
    lines.append("I am a master's student working on [one-line project]. I am interested in PhD programs for Fall [year] and was excited by your recent work on [specific paper/topic], especially [specific detail].")
    lines.append("")
    lines.append("My current direction is [ecological question] using [computational method/data]. I have experience with [R/Python/GIS/modeling skill] and am building [poster/GitHub/project].")
    lines.append("")
    lines.append("Are you reviewing PhD students for Fall [year], and do you anticipate funding for a student working in this area?")
    lines.append("")
    lines.append("Best,")
    lines.append("[Name]")
    lines.append("```")
    lines.append("")
    lines.append("## Journals He Should Scan")
    lines.append("")
    lines.append("This is not a claim about any one faculty member's publication record. It is a practical reading map for computational ecology.")
    lines.append("")
    lines.append("| Journal | Why it matters |")
    lines.append("|---|---|")
    lines.append("| Methods in Ecology and Evolution | Methods, software, workflows, statistics, reproducibility. |")
    lines.append("| Ecology Letters | High-impact ecology, often theory/data synthesis. |")
    lines.append("| Ecological Applications | Applied modeling and decision-relevant ecology. |")
    lines.append("| Theoretical Ecology | Mathematical and theoretical ecology. |")
    lines.append("| Journal of Theoretical Biology | Broader mathematical biology and modeling. |")
    lines.append("| Ecological Informatics | Computation, data, software, informatics. |")
    lines.append("| Global Change Biology | Climate/global-change ecology and large datasets. |")
    lines.append("| Remote Sensing of Environment | Remote sensing, spatial data, environmental monitoring. |")
    lines.append("| Ecosphere / Ecology / Ecological Monographs | Core ecology venues to understand the field. |")
    lines.append("| PNAS / Nature Ecology & Evolution | High-level examples of how strong ecology papers are framed. |")
    lines.append("")
    lines.append("## What He Should Have Before Applications")
    lines.append("")
    lines.append("- CV with one computational ecology project clearly visible.")
    lines.append("- One GitHub repo or reproducible notebook that a professor can skim in 2 minutes.")
    lines.append("- One figure showing he can turn ecological data into an interpretable result.")
    lines.append("- One paragraph explaining the research identity: question, data, method, why it matters.")
    lines.append("- 12-18 faculty targets, not just school names.")
    lines.append("- Funding notes for every application.")
    lines.append("- 2-3 letter writers who can speak to research ability, coding/quantitative skill, and independence.")
    lines.append("")
    lines.append("## Decision Rule")
    lines.append("")
    lines.append("If an opportunity does not create one of these outputs, skip it:")
    lines.append("")
    lines.append("- Poster/presentation.")
    lines.append("- Faculty conversation.")
    lines.append("- Funding/scholarship application.")
    lines.append("- Portfolio project.")
    lines.append("- Concrete method skill tied to a research question.")
    lines.append("")
    lines.append("The goal is not to collect activities. The goal is to make faculty believe: this student can join my lab, learn fast, analyze data, and finish a funded research project.")
    lines.append("")
    GUIDE_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = load_opportunities()
    write_guide(rows)
    write_action_csv(rows)
    print(f"Wrote {GUIDE_OUT}")
    print(f"Wrote {ACTION_CSV_OUT}")


if __name__ == "__main__":
    main()
