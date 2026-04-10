#!/usr/bin/env python3
"""Generate a readable markdown directory for computational ecology faculty lists."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

LONGLIST_CSV = Path("computational_ecology_faculty_longlist.csv")
SHORTLIST_CSV = Path("computational_ecology_faculty_shortlist_theo.csv")
SHORTLIST_US_CSV = Path("computational_ecology_faculty_shortlist_theo_us.csv")
OUT_MD = Path("computational_ecology_faculty_directory.md")


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def md_escape(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ").strip()


def link(text: str, url: str) -> str:
    u = (url or "").strip()
    if not u:
        return text
    return f"[{md_escape(text)}]({u})"


def add_table(lines: list[str], headers: list[str], rows: list[list[str]]) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")


def make_rows_us(shortlist_us: list[dict[str, str]], limit: int = 70) -> list[list[str]]:
    rows: list[list[str]] = []
    for r in shortlist_us[:limit]:
        rows.append(
            [
                md_escape(r.get("rank", "")),
                link(r.get("faculty_name", ""), r.get("openalex_profile_url", "")),
                md_escape(r.get("institution", "")),
                md_escape(r.get("priority_bucket", "")),
                md_escape(r.get("focus_tags", "")),
            ]
        )
    return rows


def make_rows_global(shortlist: list[dict[str, str]], limit: int = 90) -> list[list[str]]:
    rows: list[list[str]] = []
    for r in shortlist[:limit]:
        rows.append(
            [
                md_escape(r.get("rank", "")),
                link(r.get("faculty_name", ""), r.get("openalex_profile_url", "")),
                md_escape(r.get("institution", "")),
                md_escape(r.get("country_code", "")),
                md_escape(r.get("priority_bucket", "")),
                md_escape(r.get("focus_tags", "")),
            ]
        )
    return rows


def make_rows_longlist(longlist: list[dict[str, str]], limit: int | None = None) -> list[list[str]]:
    rows: list[list[str]] = []
    subset = longlist if limit is None else longlist[:limit]
    for r in subset:
        rows.append(
            [
                md_escape(r.get("rank", "")),
                link(r.get("faculty_name", ""), r.get("openalex_profile_url", "")),
                md_escape(r.get("institution", "")),
                md_escape(r.get("country_code", "")),
                md_escape(r.get("priority_bucket", "")),
                md_escape(r.get("grad_advisor_fit", "")),
                md_escape(r.get("computational_ecology_fit_tags", "")),
            ]
        )
    return rows


def build_markdown() -> None:
    longlist = load_csv(LONGLIST_CSV)
    shortlist = load_csv(SHORTLIST_CSV)
    shortlist_us = load_csv(SHORTLIST_US_CSV)

    lines: list[str] = []
    lines.append("# Computational Ecology Faculty Directory")
    lines.append("")
    lines.append(f"Generated on {date.today().isoformat()} from the faculty CSV outputs.")
    lines.append("")
    lines.append("## How to Use")
    lines.append("")
    lines.append("- Start with the US shortlist if Theo is targeting funded US PhD programs first.")
    lines.append("- Use the global shortlist for international options.")
    lines.append("- Use the longlist section to expand beyond the shortlist.")
    lines.append("")
    lines.append("## Snapshot")
    lines.append("")
    lines.append(f"- Total longlist entries: {len(longlist)}")
    lines.append(f"- Theo global shortlist entries: {len(shortlist)}")
    lines.append(f"- Theo US shortlist entries: {len(shortlist_us)}")
    lines.append("")

    lines.append("## US Shortlist (Theo)")
    lines.append("")
    add_table(
        lines,
        ["Rank", "Faculty", "Institution", "Priority", "Focus Tags"],
        make_rows_us(shortlist_us, limit=70),
    )
    lines.append("")

    lines.append("## Global Shortlist (Theo)")
    lines.append("")
    add_table(
        lines,
        ["Rank", "Faculty", "Institution", "Country", "Priority", "Focus Tags"],
        make_rows_global(shortlist, limit=90),
    )
    lines.append("")

    lines.append("## Full Longlist (All 550)")
    lines.append("")
    add_table(
        lines,
        ["Rank", "Faculty", "Institution", "Country", "Priority", "Advisor Fit", "Fit Tags"],
        make_rows_longlist(longlist, limit=None),
    )
    lines.append("")
    lines.append("## Source Files")
    lines.append("")
    lines.append("- `computational_ecology_faculty_longlist.csv`")
    lines.append("- `computational_ecology_faculty_shortlist_theo.csv`")
    lines.append("- `computational_ecology_faculty_shortlist_theo_us.csv`")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    build_markdown()
    print(f"Wrote {OUT_MD}")
