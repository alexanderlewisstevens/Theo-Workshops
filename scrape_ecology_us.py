#!/usr/bin/env python3
"""Scrape ecology institutes, grad programs, and workshops into CSV files."""

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
STUDENT_WORKSHOPS_CSV = BASE_DIR / "ecology_workshops_student_focused_global.csv"

SUBFIELD_TAGS_FIELD = "ecology_subfield_tags"
STUDENT_AUDIENCE_FIELD = "student_audience_tags"
STUDENT_AUDIENCE_NOTES_FIELD = "student_audience_notes"

INSTITUTE_FIELDNAMES = [
    "institute_name",
    SUBFIELD_TAGS_FIELD,
    "network",
    "site_status",
    "ecosystem_focus",
    "latitude",
    "longitude",
    "homepage_url",
    "profile_url",
    "source_url",
]

GRAD_PROGRAM_FIELDNAMES = [
    "institution_name",
    SUBFIELD_TAGS_FIELD,
    "institution_type",
    "city",
    "state",
    "tuition_and_fees",
    "program_page_url",
    "source_url",
]

WORKSHOP_FIELDNAMES = [
    "workshop_name",
    SUBFIELD_TAGS_FIELD,
    STUDENT_AUDIENCE_FIELD,
    STUDENT_AUDIENCE_NOTES_FIELD,
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
]

SPECIALIZED_INSTITUTES = [
    {
        "institute_name": "National Center for Ecological Analysis and Synthesis (NCEAS)",
        SUBFIELD_TAGS_FIELD: "computational;quantitative",
        "network": "Research center",
        "site_status": "n/a",
        "ecosystem_focus": "Ecological synthesis, data-intensive ecology, modeling, and analysis",
        "latitude": "",
        "longitude": "",
        "homepage_url": "https://www.nceas.ucsb.edu/",
        "profile_url": "https://www.nceas.ucsb.edu/",
        "source_url": "https://www.nceas.ucsb.edu/",
    },
    {
        "institute_name": "Quantitative Ecology Lab | University of Washington",
        SUBFIELD_TAGS_FIELD: "quantitative",
        "network": "University lab",
        "site_status": "n/a",
        "ecosystem_focus": "Quantitative ecology, population ecology, and ecological statistics",
        "latitude": "",
        "longitude": "",
        "homepage_url": "https://depts.washington.edu/sefsqel/",
        "profile_url": "https://depts.washington.edu/sefsqel/",
        "source_url": "https://depts.washington.edu/sefsqel/",
    },
    {
        "institute_name": "Mathematical and Computational Ecology and Evolution | University of Tennessee, Knoxville",
        SUBFIELD_TAGS_FIELD: "computational;quantitative;theoretical",
        "network": "University lab",
        "site_status": "n/a",
        "ecosystem_focus": "Mathematical ecology, computational ecology, and evolution",
        "latitude": "",
        "longitude": "",
        "homepage_url": "https://lgross.utk.edu/matheco",
        "profile_url": "https://lgross.utk.edu/matheco",
        "source_url": "https://lgross.utk.edu/matheco",
    },
    {
        "institute_name": "QuantitativeEcology.org | Northern Arizona University",
        SUBFIELD_TAGS_FIELD: "computational;quantitative;theoretical",
        "network": "University research group",
        "site_status": "n/a",
        "ecosystem_focus": "Mathematical, computational, technological, and statistical tools for ecology",
        "latitude": "",
        "longitude": "",
        "homepage_url": "https://quantitativeecology.org/",
        "profile_url": "https://quantitativeecology.org/",
        "source_url": "https://quantitativeecology.org/",
    },
    {
        "institute_name": "Quantitative Ecology Lab - North Carolina State University",
        SUBFIELD_TAGS_FIELD: "quantitative;theoretical",
        "network": "University lab",
        "site_status": "n/a",
        "ecosystem_focus": "Ecological models, field studies, and statistical tools",
        "latitude": "",
        "longitude": "",
        "homepage_url": "https://quantecolab.com/",
        "profile_url": "https://quantecolab.com/",
        "source_url": "https://quantecolab.com/",
    },
    {
        "institute_name": "Tourani Quantitative Ecology Lab | University of Montana",
        SUBFIELD_TAGS_FIELD: "quantitative",
        "network": "University lab",
        "site_status": "n/a",
        "ecosystem_focus": "Species monitoring, ecological statistics, and population modeling",
        "latitude": "",
        "longitude": "",
        "homepage_url": "https://www.umt.edu/quantitative-ecology-lab/default.php",
        "profile_url": "https://www.umt.edu/quantitative-ecology-lab/default.php",
        "source_url": "https://www.umt.edu/quantitative-ecology-lab/default.php",
    },
]

SPECIALIZED_GRAD_PROGRAMS = [
    {
        "institution_name": "University of Washington - Quantitative Ecology and Resource Management (QERM)",
        SUBFIELD_TAGS_FIELD: "quantitative",
        "institution_type": "Interdisciplinary graduate program",
        "city": "Seattle",
        "state": "WA",
        "tuition_and_fees": "",
        "program_page_url": "https://quantitative.uw.edu/graduate/qerm/",
        "source_url": "https://quantitative.uw.edu/graduate/qerm/",
    },
    {
        "institution_name": "Penn State - Quantitative Ecology Option",
        SUBFIELD_TAGS_FIELD: "quantitative",
        "institution_type": "MS/PhD ecology option",
        "city": "University Park",
        "state": "PA",
        "tuition_and_fees": "",
        "program_page_url": "https://www.huck.psu.edu/graduate-programs/ecology/degree-requirements/options-and-dual-titles/quantitative-ecology",
        "source_url": "https://www.huck.psu.edu/graduate-programs/ecology/degree-requirements/options-and-dual-titles/quantitative-ecology",
    },
]

SPECIALIZED_WORKSHOPS = [
    {
        "workshop_name": "CV4Ecology Workshop",
        SUBFIELD_TAGS_FIELD: "computational",
        STUDENT_AUDIENCE_FIELD: "unspecified",
        STUDENT_AUDIENCE_NOTES_FIELD: "",
        "start_date": "",
        "end_date": "",
        "venue_name": "Smithsonian Conservation Biology Institute / Smithsonian Mason School of Conservation",
        "city": "Front Royal",
        "state": "VA",
        "country": "US",
        "attendance_mode": "Offline",
        "description": "Workshop on computer vision methods for ecology.",
        "event_url": "https://cv4ecology.csail.mit.edu/",
        "source_query_url": "https://cv4ecology.csail.mit.edu/",
    },
    {
        "workshop_name": "Theory Tea",
        SUBFIELD_TAGS_FIELD: "theoretical",
        STUDENT_AUDIENCE_FIELD: "unspecified",
        STUDENT_AUDIENCE_NOTES_FIELD: "",
        "start_date": "",
        "end_date": "",
        "venue_name": "Princeton University Department of Ecology and Evolutionary Biology",
        "city": "Princeton",
        "state": "NJ",
        "country": "US",
        "attendance_mode": "Offline",
        "description": "Weekly seminar series on theoretical ecology and related fields.",
        "event_url": "https://eeb.princeton.edu/people/group/theoretical-ecology-tea",
        "source_query_url": "https://eeb.princeton.edu/people/group/theoretical-ecology-tea",
    },
    {
        "workshop_name": "Statistical Methods Seminar Series",
        SUBFIELD_TAGS_FIELD: "quantitative",
        STUDENT_AUDIENCE_FIELD: "unspecified",
        STUDENT_AUDIENCE_NOTES_FIELD: "",
        "start_date": "",
        "end_date": "",
        "venue_name": "EcoForecast Network",
        "city": "",
        "state": "",
        "country": "US",
        "attendance_mode": "Online",
        "description": "Seminar series on quantitative and statistical methods in ecology and environmental science using R.",
        "event_url": "https://ecoforecast.org/workshops/statistical-methods-seminar-series/",
        "source_query_url": "https://ecoforecast.org/workshops/statistical-methods-seminar-series/",
    },
    {
        "workshop_name": "Applied Spatial Ecology Workshop",
        SUBFIELD_TAGS_FIELD: "quantitative",
        STUDENT_AUDIENCE_FIELD: "unspecified",
        STUDENT_AUDIENCE_NOTES_FIELD: "",
        "start_date": "2022-09-27",
        "end_date": "2022-09-28",
        "venue_name": "Penn State",
        "city": "University Park",
        "state": "PA",
        "country": "US",
        "attendance_mode": "Offline",
        "description": "Two-day short course in applied spatial ecology using R.",
        "event_url": "https://ecosystems.psu.edu/research/labs/walter-lab/workshop",
        "source_query_url": "https://ecosystems.psu.edu/research/labs/walter-lab/workshop",
    },
    {
        "workshop_name": "Big Data Analytics in Forestry",
        SUBFIELD_TAGS_FIELD: "computational;quantitative",
        STUDENT_AUDIENCE_FIELD: "unspecified",
        STUDENT_AUDIENCE_NOTES_FIELD: "",
        "start_date": "",
        "end_date": "",
        "venue_name": "Northern Arizona University",
        "city": "Flagstaff",
        "state": "AZ",
        "country": "US",
        "attendance_mode": "Unknown",
        "description": "Workshop taught through QuantitativeEcology.org on big-data analytics relevant to ecology and forestry.",
        "event_url": "http://quantitativeecology.org/big-data/",
        "source_query_url": "https://quantitativeecology.org/",
    },
    {
        "workshop_name": "SEEDS Geographic Information Systems (GIS) Workshop",
        SUBFIELD_TAGS_FIELD: "quantitative",
        STUDENT_AUDIENCE_FIELD: "graduate",
        STUDENT_AUDIENCE_NOTES_FIELD: "Applicants must be enrolled in a graduate program within the United States.",
        "start_date": "2024-05-20",
        "end_date": "2024-05-25",
        "venue_name": "Florida A&M University Sustainability Institute",
        "city": "Tallahassee",
        "state": "FL",
        "country": "US",
        "attendance_mode": "Offline",
        "description": "Hands-on GIS and remote-sensing workshop for ecological research using NEON data.",
        "event_url": "https://esa.org/seeds/meetings/gis-graduate-workshop/",
        "source_query_url": "https://esa.org/seeds/meetings/gis-graduate-workshop/",
    },
    {
        "workshop_name": "SEEDS National Field Trip - Kellogg Biological Field Station",
        SUBFIELD_TAGS_FIELD: "general",
        STUDENT_AUDIENCE_FIELD: "undergraduate",
        STUDENT_AUDIENCE_NOTES_FIELD: "The field trip hosted 20 diverse undergraduate students from around the country.",
        "start_date": "2023-04-28",
        "end_date": "2023-04-30",
        "venue_name": "Kellogg Biological Field Station",
        "city": "Hickory Corners",
        "state": "MI",
        "country": "US",
        "attendance_mode": "Offline",
        "description": "SEEDS field trip focused on agroecology, field research, and career exploration.",
        "event_url": "https://esa.org/seeds/field-trip/past-field-trips/",
        "source_query_url": "https://esa.org/seeds/field-trip/past-field-trips/",
    },
    {
        "workshop_name": "SPEC School",
        SUBFIELD_TAGS_FIELD: "quantitative",
        STUDENT_AUDIENCE_FIELD: "graduate",
        STUDENT_AUDIENCE_NOTES_FIELD: "Aimed primarily at graduate students and early postdoctoral researchers working with spectral data.",
        "start_date": "",
        "end_date": "",
        "venue_name": "SPEC School",
        "city": "",
        "state": "",
        "country": "US",
        "attendance_mode": "Hybrid",
        "description": "Summer school on theory and application of spectroscopy and remote sensing in ecology.",
        "event_url": "https://www.specschool.org/",
        "source_query_url": "https://www.specschool.org/",
    },
]

INTERNATIONAL_STUDENT_WORKSHOPS = [
    {
        "workshop_name": "British Ecological Society Undergraduate Summer School",
        SUBFIELD_TAGS_FIELD: "general",
        STUDENT_AUDIENCE_FIELD: "undergraduate",
        STUDENT_AUDIENCE_NOTES_FIELD: "Applications are considered for undergraduate students studying degrees related to ecological sciences.",
        "start_date": "2024-07-16",
        "end_date": "2024-07-22",
        "venue_name": "Rhyd-y-creuau FSC Centre",
        "city": "",
        "state": "Wales",
        "country": "GB",
        "attendance_mode": "Hybrid",
        "description": "Undergraduate summer school with practical field skills, specialist ecological workshops, careers talks, and transferable-skills development.",
        "event_url": "https://www.britishecologicalsociety.org/wp-content/uploads/2024/02/Student-Guidance-BESUG24.pdf",
        "source_query_url": "https://www.britishecologicalsociety.org/wp-content/uploads/2024/02/Student-Guidance-BESUG24.pdf",
    },
    {
        "workshop_name": "BIOS2 Data-driven Ecological Synthesis",
        SUBFIELD_TAGS_FIELD: "computational;quantitative",
        STUDENT_AUDIENCE_FIELD: "undergraduate;graduate",
        STUDENT_AUDIENCE_NOTES_FIELD: "The course is intended for graduate students but is also open to undergraduate students.",
        "start_date": "",
        "end_date": "",
        "venue_name": "Universite de Montreal",
        "city": "Montreal",
        "state": "QC",
        "country": "CA",
        "attendance_mode": "Unknown",
        "description": "Week-long class teaching data management and analysis for ecological synthesis research.",
        "event_url": "https://bios2.usherbrooke.ca/program/program-components/summer-schools/",
        "source_query_url": "https://bios2.usherbrooke.ca/program/program-components/summer-schools/",
    },
    {
        "workshop_name": "BIOS2 Summer School in Biodiversity Modelling",
        SUBFIELD_TAGS_FIELD: "computational;quantitative",
        STUDENT_AUDIENCE_FIELD: "undergraduate;graduate",
        STUDENT_AUDIENCE_NOTES_FIELD: "The course is intended for graduate students but is also open to undergraduate students.",
        "start_date": "2020-08-23",
        "end_date": "2020-08-28",
        "venue_name": "Orford Musique",
        "city": "Orford",
        "state": "QC",
        "country": "CA",
        "attendance_mode": "Offline",
        "description": "Summer school covering biodiversity modelling, joint distribution models, simulations, and ecological network analysis.",
        "event_url": "https://bios2.usherbrooke.ca/program/program-components/summer-schools/",
        "source_query_url": "https://bios2.usherbrooke.ca/program/program-components/summer-schools/",
    },
    {
        "workshop_name": "Advanced Field School in Computational Ecology",
        SUBFIELD_TAGS_FIELD: "computational;quantitative",
        STUDENT_AUDIENCE_FIELD: "graduate",
        STUDENT_AUDIENCE_NOTES_FIELD: "Described by the organizers as an international PhD school in computational ecology.",
        "start_date": "2023-05-19",
        "end_date": "2023-05-26",
        "venue_name": "Couvent de Val-Morin",
        "city": "Val-Morin",
        "state": "QC",
        "country": "CA",
        "attendance_mode": "Offline",
        "description": "Advanced field school on computational ecology with modelling and data-analysis training.",
        "event_url": "https://sentinellenord.ulaval.ca/en/ecology2023",
        "source_query_url": "https://sentinellenord.ulaval.ca/en/ecology2023",
    },
    {
        "workshop_name": "ACCESS-2025 Aarhus Comprehensive Computational Entomology Summer School",
        SUBFIELD_TAGS_FIELD: "computational",
        STUDENT_AUDIENCE_FIELD: "graduate",
        STUDENT_AUDIENCE_NOTES_FIELD: "The course particularly supports early-career researchers including graduate students and PhD students.",
        "start_date": "2025-09-28",
        "end_date": "2025-10-03",
        "venue_name": "Mols Laboratory",
        "city": "Aarhus",
        "state": "",
        "country": "DK",
        "attendance_mode": "Offline",
        "description": "Residential summer school on computational methods for insect ecology and entomology.",
        "event_url": "https://darsa.info/ACCESS-2025/",
        "source_query_url": "https://darsa.info/ACCESS-2025/",
    },
    {
        "workshop_name": "Helsinki Summer School on Mathematical Ecology and Evolution 2018",
        SUBFIELD_TAGS_FIELD: "theoretical;quantitative",
        STUDENT_AUDIENCE_FIELD: "undergraduate;graduate",
        STUDENT_AUDIENCE_NOTES_FIELD: "The workshop is aimed at graduate students and also welcomes advanced undergraduate students.",
        "start_date": "2018-08-19",
        "end_date": "2018-08-26",
        "venue_name": "Turku",
        "city": "Turku",
        "state": "",
        "country": "FI",
        "attendance_mode": "Offline",
        "description": "Summer school on mathematical ecology and evolution emphasizing theoretical and quantitative approaches.",
        "event_url": "https://wiki.helsinki.fi/xwiki/bin/view/BioMath/The%20Research%20Group%20of%20Biomathematics/Summer%20Schools/The%20Helsinki%20Summer%20School%20on%20Mathematical%20Ecology%20and%20Evolution%202018/",
        "source_query_url": "https://wiki.helsinki.fi/xwiki/bin/view/BioMath/The%20Research%20Group%20of%20Biomathematics/Summer%20Schools/The%20Helsinki%20Summer%20School%20on%20Mathematical%20Ecology%20and%20Evolution%202018/",
    },
    {
        "workshop_name": "Ant Ecol Summer School",
        SUBFIELD_TAGS_FIELD: "quantitative",
        STUDENT_AUDIENCE_FIELD: "graduate",
        STUDENT_AUDIENCE_NOTES_FIELD: "The summer school is for PhD students, postdocs, and early-career scientists working on ants.",
        "start_date": "2026-08-24",
        "end_date": "2026-08-28",
        "venue_name": "Arolla",
        "city": "Arolla",
        "state": "",
        "country": "CH",
        "attendance_mode": "Offline",
        "description": "International summer school on ant ecology under global change with GIS, data-analysis, and field-work components.",
        "event_url": "https://wp.unil.ch/bertelsmeiergroup/antecol/",
        "source_query_url": "https://wp.unil.ch/bertelsmeiergroup/antecol/",
    },
]


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


def merge_rows(
    rows: List[Dict[str, str]],
    extra_rows: List[Dict[str, str]],
    key_field: str,
) -> List[Dict[str, str]]:
    rows_by_key = {normalize_text(row.get(key_field, "")).lower(): row for row in rows}
    for row in extra_rows:
        key = normalize_text(row.get(key_field, "")).lower()
        if key:
            rows_by_key[key] = row
    return list(rows_by_key.values())


def student_focused_rows(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    focused = [row for row in rows if row.get(STUDENT_AUDIENCE_FIELD, "unspecified") != "unspecified"]
    focused = merge_rows(focused, INTERNATIONAL_STUDENT_WORKSHOPS, "workshop_name")
    focused.sort(key=lambda r: (r["start_date"], r["country"], r["workshop_name"]))
    return focused


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
                SUBFIELD_TAGS_FIELD: "general",
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

    rows = merge_rows(rows, SPECIALIZED_INSTITUTES, "homepage_url")
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
                SUBFIELD_TAGS_FIELD: "general",
                "institution_type": institution_type,
                "city": city,
                "state": state,
                "tuition_and_fees": normalize_text(tuition_match.group(1) if tuition_match else ""),
                "program_page_url": program_page_url,
                "source_url": base_url,
            }

    rows = merge_rows(list(rows_by_url.values()), SPECIALIZED_GRAD_PROGRAMS, "program_page_url")
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
                    SUBFIELD_TAGS_FIELD: "general",
                    STUDENT_AUDIENCE_FIELD: "unspecified",
                    STUDENT_AUDIENCE_NOTES_FIELD: "",
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

    rows = merge_rows(list(rows_by_url.values()), SPECIALIZED_WORKSHOPS, "event_url")
    rows.sort(key=lambda r: (r["start_date"], r["workshop_name"]))
    return rows


def main() -> None:
    institutes = scrape_institutes()
    grad_programs = scrape_grad_programs()
    workshops = scrape_workshops()
    student_workshops = student_focused_rows(workshops)

    write_csv(
        INSTITUTES_CSV,
        institutes,
        INSTITUTE_FIELDNAMES,
    )
    write_csv(
        GRAD_PROGRAMS_CSV,
        grad_programs,
        GRAD_PROGRAM_FIELDNAMES,
    )
    write_csv(
        WORKSHOPS_CSV,
        workshops,
        WORKSHOP_FIELDNAMES,
    )
    write_csv(
        STUDENT_WORKSHOPS_CSV,
        student_workshops,
        WORKSHOP_FIELDNAMES,
    )

    print(f"Wrote {INSTITUTES_CSV.name} ({len(institutes)} rows)")
    print(f"Wrote {GRAD_PROGRAMS_CSV.name} ({len(grad_programs)} rows)")
    print(f"Wrote {WORKSHOPS_CSV.name} ({len(workshops)} rows)")
    print(f"Wrote {STUDENT_WORKSHOPS_CSV.name} ({len(student_workshops)} rows)")


if __name__ == "__main__":
    main()
