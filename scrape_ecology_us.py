#!/usr/bin/env python3
"""Scrape US ecology institutes, grad programs, and workshops into CSV files."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Dict, List
from urllib.request import Request, urlopen


BASE_DIR = Path(__file__).resolve().parent

INSTITUTES_CSV = BASE_DIR / "ecology_institutes_us.csv"
GRAD_PROGRAMS_CSV = BASE_DIR / "ecology_grad_programs_us.csv"
WORKSHOPS_CSV = BASE_DIR / "ecology_workshops_us.csv"


def fetch_text(url: str) -> str:
    req = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; TheoWorkshopsBot/1.0)"},
    )
    with urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8", "ignore")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u2013", "-").replace("\u2014", "-")).strip()


def write_csv(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def scrape_institutes() -> List[Dict[str, str]]:
    source_url = "https://lternet.edu/site/"
    html = fetch_text(source_url)

    map_match = re.search(r"var map_locations = (\[.*?\]);", html, flags=re.S)
    if not map_match:
        raise RuntimeError("Could not locate LTER map location data.")
    raw_locations = json.loads(map_match.group(1))

    current_block_match = re.search(
        r"<h2>Current LTER Sites</h2>(.*?)<h2>Legacy LTER Sites</h2>",
        html,
        flags=re.S,
    )
    current_titles = set()
    if current_block_match:
        current_titles = {
            normalize_text(name)
            for name in re.findall(r'<li><a href="[^"]+">([^<]+)</a></li>', current_block_match.group(1))
        }

    rows: List[Dict[str, str]] = []
    for site in raw_locations:
        lat_raw = str(site.get("lat", "")).strip()
        lon_raw = str(site.get("lon", "")).strip()
        if not lat_raw or not lon_raw:
            continue

        try:
            lat = float(lat_raw)
            lon = float(lon_raw)
        except ValueError:
            continue

        # Bounding boxes for US/US-territory ecology sites in this source.
        if not (15.0 < lat < 72.0 and -170.0 < lon < -60.0):
            continue

        name = normalize_text(str(site.get("title", "")))
        if not name:
            continue

        status = "current" if name in current_titles else "legacy"
        ecosystem = normalize_text(str(site.get("ecosystem", "")))
        if ecosystem.lower() == "administrative" or "network office" in name.lower():
            continue

        rows.append(
            {
                "institute_name": name,
                "network": "NSF LTER",
                "site_status": status,
                "ecosystem_focus": ecosystem,
                "latitude": f"{lat:.6f}",
                "longitude": f"{lon:.6f}",
                "homepage_url": str(site.get("homepage", "")).strip(),
                "profile_url": str(site.get("link", "")).strip(),
                "source_url": source_url,
            }
        )

    rows.sort(key=lambda r: (r["site_status"], r["institute_name"]))
    return rows


def scrape_grad_programs() -> List[Dict[str, str]]:
    base_url = "https://www.collegetuitioncompare.com/graduate/ecology/"
    card_marker = '<div class="card-body px-md-5 py-md-5 p-2 mb-5 d-flex flex-row align-items-center school-box">'

    rows_by_url: Dict[str, Dict[str, str]] = {}
    for page in range(0, 5):
        page_url = f"{base_url}?page={page}"
        html = fetch_text(page_url)
        parts = html.split(card_marker)[1:]
        for part in parts:
            name_match = re.search(r'<h4 class="h5 lh-xs mb-1"><a href="([^"]+)">([^<]+)</a></h4>', part)
            badges = re.findall(
                r'<span class="badge bg-pale-ash text-dark rounded py-1 mb-2">([^<]+)</span>',
                part,
            )
            tuition_match = re.search(r"<p class=\"mb-0 text-body\">Tuition & Fees :\s*([^<]+)</p>", part)
            if not name_match or len(badges) < 2:
                continue

            page_href, institution_name = name_match.groups()
            program_page_url = f"https:{page_href}" if page_href.startswith("//") else page_href

            institution_type = normalize_text(badges[0])
            city_state = normalize_text(badges[1])
            if "," in city_state:
                city, state = [x.strip() for x in city_state.rsplit(",", 1)]
            else:
                city, state = city_state, ""

            rows_by_url[program_page_url] = {
                "institution_name": normalize_text(institution_name),
                "institution_type": institution_type,
                "city": city,
                "state": state,
                "tuition_and_fees": normalize_text(tuition_match.group(1) if tuition_match else ""),
                "program_page_url": program_page_url,
                "source_url": base_url,
            }

    rows = list(rows_by_url.values())
    rows.sort(key=lambda r: r["institution_name"])
    return rows


def scrape_workshops() -> List[Dict[str, str]]:
    query_slugs = [
        "ecology-workshop",
        "conservation-workshop",
        "environmental-science-workshop",
    ]
    keyword_re = re.compile(
        r"\b(ecology|ecological|ecosystem|conservation|biodiversity|wildlife|habitat|"
        r"restoration|environmental|marine|botany|forestry|naturalist|sustainability|climate)\b",
        flags=re.I,
    )
    workshop_type_re = re.compile(
        r"\b(workshop|class|training|course|seminar|bootcamp|camp|institute|field school)\b",
        flags=re.I,
    )

    rows_by_url: Dict[str, Dict[str, str]] = {}
    for query in query_slugs:
        for page in range(1, 6):
            page_url = f"https://www.eventbrite.com/d/united-states/{query}/"
            if page > 1:
                page_url += f"?page={page}"

            html = fetch_text(page_url)
            json_blocks = re.findall(
                r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
                html,
                flags=re.S,
            )

            item_list = []
            for block in json_blocks:
                try:
                    parsed = json.loads(block)
                except json.JSONDecodeError:
                    continue
                if isinstance(parsed, dict) and parsed.get("@type") == "ItemList":
                    item_list = parsed.get("itemListElement", [])
                    break

            for item in item_list:
                event = item.get("item", {}) if isinstance(item, dict) else {}
                event_url = str(event.get("url", "")).strip()
                if not event_url:
                    continue

                name = normalize_text(str(event.get("name", "")))
                description = normalize_text(str(event.get("description", "")))
                combined_text = f"{name} {description}"
                if not keyword_re.search(combined_text):
                    continue
                if not workshop_type_re.search(name):
                    continue

                location = event.get("location", {}) if isinstance(event.get("location"), dict) else {}
                address = location.get("address", {}) if isinstance(location.get("address"), dict) else {}
                country = str(address.get("addressCountry", "")).strip().upper()
                if country and country != "US":
                    continue

                attendance_mode = str(event.get("eventAttendanceMode", "")).strip()
                attendance_mode = (
                    attendance_mode.rsplit("/", 1)[-1].replace("EventAttendanceMode", "") or "Unknown"
                )

                rows_by_url[event_url] = {
                    "workshop_name": name,
                    "start_date": str(event.get("startDate", "")).strip(),
                    "end_date": str(event.get("endDate", "")).strip(),
                    "venue_name": normalize_text(str(location.get("name", ""))),
                    "city": normalize_text(str(address.get("addressLocality", ""))),
                    "state": normalize_text(str(address.get("addressRegion", ""))),
                    "country": country or "US",
                    "attendance_mode": attendance_mode,
                    "description": description,
                    "event_url": event_url,
                    "source_query_url": page_url,
                }

    rows = list(rows_by_url.values())
    rows.sort(key=lambda r: (r["start_date"], r["workshop_name"]))
    return rows


def main() -> None:
    institutes = scrape_institutes()
    grad_programs = scrape_grad_programs()
    workshops = scrape_workshops()

    write_csv(
        INSTITUTES_CSV,
        institutes,
        [
            "institute_name",
            "network",
            "site_status",
            "ecosystem_focus",
            "latitude",
            "longitude",
            "homepage_url",
            "profile_url",
            "source_url",
        ],
    )
    write_csv(
        GRAD_PROGRAMS_CSV,
        grad_programs,
        [
            "institution_name",
            "institution_type",
            "city",
            "state",
            "tuition_and_fees",
            "program_page_url",
            "source_url",
        ],
    )
    write_csv(
        WORKSHOPS_CSV,
        workshops,
        [
            "workshop_name",
            "start_date",
            "end_date",
            "venue_name",
            "city",
            "state",
            "country",
            "attendance_mode",
            "description",
            "event_url",
            "source_query_url",
        ],
    )

    print(f"Wrote {INSTITUTES_CSV.name} ({len(institutes)} rows)")
    print(f"Wrote {GRAD_PROGRAMS_CSV.name} ({len(grad_programs)} rows)")
    print(f"Wrote {WORKSHOPS_CSV.name} ({len(workshops)} rows)")


if __name__ == "__main__":
    main()
