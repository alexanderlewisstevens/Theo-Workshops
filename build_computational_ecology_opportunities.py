#!/usr/bin/env python3
"""Build a practical opportunity packet for a master's student targeting computational ecology PhD programs."""

from __future__ import annotations

import csv
import re
from pathlib import Path

TODAY = "2026-04-10"
CSV_OUT = Path("computational_ecology_opportunities.csv")
MD_OUT = Path("computational_ecology_opportunities.md")

FIELDS = [
    "opportunity_name",
    "opportunity_type",
    "priority_tier",
    "status_as_of_2026_04_10",
    "target_student_level",
    "computational_theoretical_quantitative_flag",
    "subfield_tags",
    "date_start",
    "date_end",
    "deadline_or_next_action_date",
    "location",
    "delivery_mode",
    "cost",
    "free_or_online",
    "recommended_action",
    "why_it_looks_good",
    "notes",
    "source_url",
]


def opp(**kwargs):
    row = {field: "" for field in FIELDS}
    row.update(kwargs)
    return row


OPPORTUNITIES = [
    opp(
        opportunity_name="Ecological Forecasting Initiative 2026 Conference",
        opportunity_type="conference; student travel support; presentation opportunity",
        priority_tier="1 - apply/present now",
        status_as_of_2026_04_10="Open; abstract and travel scholarship deadlines imminent",
        target_student_level="graduate students; early-career researchers; ecological forecasting community",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="ecological forecasting; Bayesian/statistical modeling; reproducible workflows; synthesis; data assimilation",
        date_start="2026-08-04",
        date_end="2026-08-07",
        deadline_or_next_action_date="2026-04-15: abstracts and travel scholarship applications close",
        location="Toronto, Ontario, Canada",
        delivery_mode="in person",
        cost="Registration not posted on the source page checked; travel scholarships available by application.",
        free_or_online="Financial support available; not free by default",
        recommended_action="Submit an abstract and travel scholarship application by 2026-04-15 if he has any model, forecast, or data-analysis result that can become a poster.",
        why_it_looks_good="Directly signals computational ecology fit, puts him in the forecasting network, and can produce a poster line on the CV.",
        notes="Highest-priority near-term target because it is specific to ecological forecasting and has a student support mechanism.",
        source_url="https://ecoforecast.org/efi-2026-conference/",
    ),
    opp(
        opportunity_name="ESA Annual Meeting 2026",
        opportunity_type="major ecology conference; workshops; networking; presentation opportunity",
        priority_tier="1 - apply/present now",
        status_as_of_2026_04_10="Open; abstract deadlines mostly passed, registration/workshop planning remains relevant",
        target_student_level="undergraduate, master's, PhD, postdoc, faculty, practitioner",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="ecology; quantitative ecology; theoretical ecology; remote sensing; spatial ecology; data science",
        date_start="2026-07-26",
        date_end="2026-07-31",
        deadline_or_next_action_date="Check late-breaking poster, workshop, and student award deadlines on the ESA 2026 site",
        location="Salt Lake City, Utah, USA",
        delivery_mode="in person",
        cost="Registration rates were not found on the official pages checked; confirm on ESA registration page before committing.",
        free_or_online="Not free by default",
        recommended_action="Attend if he can present, volunteer, join a section event, or target computational sessions; otherwise prioritize EFI/GRC/ECMTB first.",
        why_it_looks_good="ESA is the flagship U.S. ecology meeting and makes ecology-grad-school networking much easier.",
        notes="Use this to meet potential PhD advisors, attend quantitative/theory section events, and ask about labs before applications.",
        source_url="https://esa.org/saltlake2026/important-dates/",
    ),
    opp(
        opportunity_name="Gordon Research Seminar: Unifying Ecology Across Scales",
        opportunity_type="graduate-student/postdoc seminar; presentation opportunity",
        priority_tier="1 - apply/present now",
        status_as_of_2026_04_10="Applications open until 2026-06-13, subject to available space",
        target_student_level="graduate students and postdocs",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="theoretical ecology; quantitative ecology; ecological models; mechanisms; data across scales",
        date_start="2026-07-11",
        date_end="2026-07-12",
        deadline_or_next_action_date="2026-06-13: application deadline",
        location="Stonehill College, Easton, Massachusetts, USA",
        delivery_mode="in person",
        cost="GRC page lists GRS conference fee USD 245, meals USD 250, lodging double occupancy USD 340 or private room USD 420.",
        free_or_online="Not free; selective early-career format",
        recommended_action="Apply to the GRS and request to present a poster/talk if his work fits models, data, or cross-scale mechanisms.",
        why_it_looks_good="A GRS is unusually strong for a master's student because it is designed around graduate-student presentation and peer networking.",
        notes="Best paired with the following Gordon Research Conference if budget allows.",
        source_url="https://www.grc.org/unifying-ecology-across-scales-grs-conference/2026/",
    ),
    opp(
        opportunity_name="Gordon Research Conference: Unifying Ecology Across Scales",
        opportunity_type="selective research conference; high-level networking",
        priority_tier="1 - apply/present now",
        status_as_of_2026_04_10="Applications open until 2026-06-14, subject to available space",
        target_student_level="graduate students, postdocs, faculty, researchers",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="theoretical ecology; models; data integration; scaling; mechanisms; ecosystem dynamics",
        date_start="2026-07-12",
        date_end="2026-07-17",
        deadline_or_next_action_date="2026-06-14: application deadline",
        location="Stonehill College, Easton, Massachusetts, USA",
        delivery_mode="in person",
        cost="GRC page lists conference fee USD 950, meals USD 690, lodging double occupancy USD 620 or private room USD 840.",
        free_or_online="Not free; application-based",
        recommended_action="Apply if he has a clear computational/theory interest and can write a focused statement of fit.",
        why_it_looks_good="Small selective conference with concentrated access to senior quantitative and theoretical ecologists.",
        notes="Expensive but high-signal if he can secure advisor/department support.",
        source_url="https://www.grc.org/unifying-ecology-across-scales-conference/2026/",
    ),
    opp(
        opportunity_name="Evolution 2026",
        opportunity_type="conference; student support; presentation opportunity",
        priority_tier="1 - apply/present now",
        status_as_of_2026_04_10="Open; participation support deadline is imminent",
        target_student_level="undergraduate, graduate students, postdocs, faculty, researchers",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="evolutionary ecology; population genetics; phylogenetics; quantitative methods; modeling",
        date_start="2026-06-20",
        date_end="2026-06-24",
        deadline_or_next_action_date="2026-04-13: participation support; 2026-04-15: early registration rate deadline",
        location="Cleveland, Ohio, USA",
        delivery_mode="in person plus virtual components",
        cost="Official registration page lists graduate student in-person+virtual rates of USD 400 by 2026-04-15, USD 500 from 2026-04-16 to 2026-06-01, USD 550 after 2026-06-01; online-only student rate listed as USD 10.",
        free_or_online="Low-cost virtual option; participation support available by application",
        recommended_action="Apply for participation support by 2026-04-13 if eligible; otherwise consider the low-cost online option or register before 2026-04-15.",
        why_it_looks_good="Strong if his computational ecology interests touch evolution, population modeling, phylogenetics, or eco-evolutionary dynamics.",
        notes="Online option is unusually cheap and still useful for CV/professional development if travel is not possible.",
        source_url="https://www.evolutionmeetings.org/registration.html",
    ),
    opp(
        opportunity_name="European Conference on Mathematical and Theoretical Biology 2026 (ECMTB)",
        opportunity_type="international conference; mathematical biology; presentation opportunity",
        priority_tier="1 - apply/present now",
        status_as_of_2026_04_10="Open; participation grant and early registration deadlines are near",
        target_student_level="students, PhD students, postdocs, faculty, mathematical biology researchers",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="mathematical biology; theoretical ecology; population dynamics; modeling; computation",
        date_start="2026-07-13",
        date_end="2026-07-17",
        deadline_or_next_action_date="2026-04-15: participation grant deadline; 2026-04-30: early-bird registration deadline",
        location="University of Graz, Graz, Austria",
        delivery_mode="in person",
        cost="Early-bird regular student EUR 420; regular student EUR 520; SMB/ESMTB member student EUR 320 early or EUR 420 regular. PhD-student rates are higher.",
        free_or_online="Participation grants available; not free by default",
        recommended_action="Apply for a participation grant by 2026-04-15 and register by 2026-04-30 if funded.",
        why_it_looks_good="Very strong signal for computational/theoretical ecology, especially for PhD programs that value mathematical modeling.",
        notes="International travel cost is the main barrier; grant application is the key first step.",
        source_url="https://ecmtb2026.org/how-to-register",
    ),
    opp(
        opportunity_name="SPEC School",
        opportunity_type="selective graduate workshop; remote sensing; field plus virtual training",
        priority_tier="4 - watch next cycle",
        status_as_of_2026_04_10="2026 cycle appears closed; watch the next application cycle",
        target_student_level="primarily graduate students and early postdocs",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="remote sensing; spectral ecology; imaging spectroscopy; field ecology; data analysis",
        date_start="annual cycle; virtual meetings start around March, with an in-person field week",
        date_end="",
        deadline_or_next_action_date="Next-cycle deadline TBD; join notification list or monitor site",
        location="Virtual meetings plus Mountain Lake Biological Station near Pembroke, Virginia, USA",
        delivery_mode="hybrid: virtual meetings plus in-person field week",
        cost="Program states it fully supports 15-20 U.S.-based participants per year; international participants need to fund travel into the U.S.",
        free_or_online="Funded for selected U.S.-based participants; partially online",
        recommended_action="Join the notification list and prepare a one-page fit statement around spectral data, remote sensing, and ecological questions.",
        why_it_looks_good="Selective, technical, ecology-specific training in remote-sensing data, which is highly relevant for computational ecology.",
        notes="Good target for the next cycle if he wants a remote sensing or spatial ecology angle.",
        source_url="https://www.specschool.org/",
    ),
    opp(
        opportunity_name="BIOS2 Summer School: Data-driven Ecological Synthesis",
        opportunity_type="graduate summer school; data synthesis",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Recurring summer school; monitor current-year dates and guest participant scholarship details",
        target_student_level="graduate students; also open to undergraduates, postdocs, and researchers",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="data-driven ecology; synthesis; biodiversity; reproducible analysis; ecological modeling",
        date_start="May annually",
        date_end="",
        deadline_or_next_action_date="Check BIOS2 site for current application deadline",
        location="Quebec, Canada; location varies by offering",
        delivery_mode="in person or hybrid depending on offering",
        cost="BIOS2 fellows have open access; guest scholarships may cover part of costs.",
        free_or_online="Scholarships may be available; not free by default",
        recommended_action="Watch for the next guest-participant application and apply if he can frame his master's work as a data-synthesis project.",
        why_it_looks_good="Purpose-built for data-driven ecological synthesis and graduate-level methods training.",
        notes="Especially good if he wants Canadian/international computational ecology contacts.",
        source_url="https://bios2.usherbrooke.ca/program/program-components/summer-schools/",
    ),
    opp(
        opportunity_name="BIOS2 Summer School: Biodiversity Modelling",
        opportunity_type="graduate summer school; modeling",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Recurring summer school; monitor current-year dates and guest participant scholarship details",
        target_student_level="graduate students; also open to undergraduates, postdocs, and researchers",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="biodiversity modeling; ecological modeling; quantitative ecology; conservation data science",
        date_start="August annually",
        date_end="",
        deadline_or_next_action_date="Check BIOS2 site for current application deadline",
        location="Quebec, Canada; location varies by offering",
        delivery_mode="in person or hybrid depending on offering",
        cost="BIOS2 fellows have open access; guest scholarships may cover part of costs.",
        free_or_online="Scholarships may be available; not free by default",
        recommended_action="Apply when the next call opens if he wants a modeling-focused summer credential.",
        why_it_looks_good="Directly names biodiversity modeling, which maps well to computational ecology graduate applications.",
        notes="Use this as a more domain-specific alternative to generic data-science conferences.",
        source_url="https://bios2.usherbrooke.ca/program/program-components/summer-schools/",
    ),
    opp(
        opportunity_name="CV4Ecology Workshop",
        opportunity_type="selective workshop; computer vision for ecology",
        priority_tier="4 - watch next cycle",
        status_as_of_2026_04_10="2026 applications closed; watch the next cycle",
        target_student_level="students and researchers working at the ecology/computer-vision interface",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="computer vision; machine learning; wildlife monitoring; image data; ecological AI",
        date_start="2026-01-04",
        date_end="2026-01-24",
        deadline_or_next_action_date="Next-cycle deadline TBD; sign up for future announcements",
        location="Front Royal, Virginia, USA; Smithsonian/National Zoo context plus travel to Washington, DC noted on source",
        delivery_mode="in person",
        cost="2026 source listed USD 3,250 tuition for international students and attendee responsibility for travel to Washington, DC; some sponsorship may be possible.",
        free_or_online="Not free by default; sponsorship may be possible",
        recommended_action="Watch the next call and prepare a small portfolio item using camera-trap, drone, or biodiversity image data.",
        why_it_looks_good="Very strong computational-ecology signal if he wants machine learning, computer vision, or automated biodiversity monitoring.",
        notes="2026 is closed, but this is worth tracking because the credential is distinctive.",
        source_url="https://cv4ecology.caltech.edu/call_for_applications.html",
    ),
    opp(
        opportunity_name="Santa Fe Institute Complex Systems Summer School 2026",
        opportunity_type="selective summer school; complex systems",
        priority_tier="4 - watch next cycle",
        status_as_of_2026_04_10="2026 application deadline passed; watch 2027",
        target_student_level="advanced undergraduates, graduate students, postdocs, and professionals depending on cohort rules",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="complex systems; nonlinear dynamics; network science; modeling; theory",
        date_start="2026-06-09",
        date_end="2026-07-01",
        deadline_or_next_action_date="2026-02-04 deadline passed for 2026; monitor 2027 cycle",
        location="Santa Fe, New Mexico, USA",
        delivery_mode="in person",
        cost="Source lists USD 4,500 academic rate for 2026.",
        free_or_online="Not free by default; check SFI for scholarships/fellowships",
        recommended_action="Watch 2027 and apply only if he can explain how complex-systems methods support his ecology questions.",
        why_it_looks_good="Prestigious quantitative training, especially for theory-heavy or dynamical-systems ecology applications.",
        notes="Not ecology-specific, so the application framing matters.",
        source_url="https://www.santafe.edu/engage/learn/programs/complex-systems-summer-school",
    ),
    opp(
        opportunity_name="ESIIL Innovation Summit 2026: AI for Sustainability",
        opportunity_type="selective summit; AI and environmental data synthesis",
        priority_tier="4 - watch next cycle",
        status_as_of_2026_04_10="2026 application deadline passed; watch next ESIIL cycle and pre-summit trainings",
        target_student_level="researchers, students, practitioners, interdisciplinary teams",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="AI for sustainability; environmental data science; synthesis; cyberinfrastructure; open science",
        date_start="2026-05-12",
        date_end="2026-05-14",
        deadline_or_next_action_date="2026-01-31 application deadline passed for 2026",
        location="University of Colorado Boulder, Boulder, Colorado, USA",
        delivery_mode="in person plus pre-summit virtual training opportunities",
        cost="No registration fee for accepted participants; travel awards up to USD 1,200 available according to source.",
        free_or_online="Free for accepted participants; travel awards available; some associated trainings virtual",
        recommended_action="Monitor ESIIL training/events and apply next cycle if he can connect AI methods to ecological decision-making.",
        why_it_looks_good="Strong AI/environmental-data signal and good regional opportunity if he is near Colorado.",
        notes="Even if the summit is closed, ESIIL training resources/events are worth monitoring.",
        source_url="https://cu-esiil.github.io/Innovation-Summit-2026/",
    ),
    opp(
        opportunity_name="NEON Data Skills Webinar: NEON Data in Google Earth Engine",
        opportunity_type="webinar; technical skill builder",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Upcoming online event",
        target_student_level="students and researchers using NEON, remote sensing, or spatial data",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="NEON; Google Earth Engine; Python API; remote sensing; spatial ecology",
        date_start="2026-04-28",
        date_end="2026-04-28",
        deadline_or_next_action_date="Register before 2026-04-28 event",
        location="Online",
        delivery_mode="online live webinar",
        cost="No fee found on the NEON event page checked.",
        free_or_online="Online; appears free/no fee listed",
        recommended_action="Register and attend; turn the workflow into a small GitHub notebook using a NEON dataset.",
        why_it_looks_good="A quick way to add a concrete remote-sensing/GEE skill relevant to computational ecology.",
        notes="Small credential by itself; much stronger if paired with a reproducible mini-project.",
        source_url="https://www.neonscience.org/get-involved/events/data-skills-webinar-neon-data-google-earth-engine",
    ),
    opp(
        opportunity_name="Ecological Forecasting Initiative Statistical Methods Seminar Series",
        opportunity_type="online seminar series; quantitative methods",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Recurring virtual series; 2026 sessions listed",
        target_student_level="graduate students and researchers interested in ecological forecasting",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="ecological forecasting; statistics; Bayesian methods; reproducible modeling",
        date_start="recurring",
        date_end="",
        deadline_or_next_action_date="Register for the next virtual seminar listed on the EFI page",
        location="Online",
        delivery_mode="online seminar series",
        cost="No fee found on the source page checked.",
        free_or_online="Online; appears free/no fee listed",
        recommended_action="Attend regularly and cite specific methods learned in statements or advisor conversations.",
        why_it_looks_good="Signals sustained engagement with ecological forecasting rather than one-off interest.",
        notes="Best paired with the EFI conference or a forecast-analysis portfolio project.",
        source_url="https://ecoforecast.org/workshops/statistical-methods-seminar-series/",
    ),
    opp(
        opportunity_name="iDigBio Digital Data 2026",
        opportunity_type="virtual conference; biodiversity data",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Upcoming virtual event; registration details coming soon on source page",
        target_student_level="students, biodiversity-data researchers, collections/informatics community",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="biodiversity data; informatics; integrated data; collections data; open science",
        date_start="2026-06-02",
        date_end="2026-06-04",
        deadline_or_next_action_date="Monitor registration details; program and speakers coming soon",
        location="Online via Zoom",
        delivery_mode="online virtual conference",
        cost="Registration details were listed as coming soon; no cost posted on source page checked.",
        free_or_online="Online; cost not yet posted",
        recommended_action="Register when it opens and attend biodiversity-data methods sessions; look for poster or networking opportunities if offered.",
        why_it_looks_good="Good fit for computational biodiversity, data integration, and informatics-oriented ecology applications.",
        notes="Online and likely lower-friction than travel conferences.",
        source_url="https://www.idigbio.org/content/digital-data-2026",
    ),
    opp(
        opportunity_name="ASLO-SIL 2026 Joint Meeting",
        opportunity_type="aquatic sciences conference; student/ECR programming",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Upcoming; major abstract deadlines passed, student/ECR events remain relevant",
        target_student_level="students, early-career researchers, aquatic scientists",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="aquatic ecology; limnology; oceanography; ecological modeling; data science",
        date_start="2026-05-12",
        date_end="2026-05-16",
        deadline_or_next_action_date="Check student/ECR events, mentor program, and late registration options",
        location="Montreal, Quebec, Canada",
        delivery_mode="in person",
        cost="Rates not captured from official page; confirm on ASLO registration materials.",
        free_or_online="Not free by default",
        recommended_action="Consider only if his work is aquatic/freshwater/marine or if he can use student/ECR networking strongly.",
        why_it_looks_good="Strong domain-specific conference if computational ecology is tied to aquatic systems.",
        notes="Student volunteer and mentor-program opportunities can improve value even if he is not presenting.",
        source_url="https://www.aslo.org/aslo-sil-2026/",
    ),
    opp(
        opportunity_name="USSEE 2026 Biennial Conference",
        opportunity_type="conference; ecological economics; socio-ecological systems",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Open registration",
        target_student_level="students, ecological economists, sustainability researchers",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="ecological economics; socio-ecological systems; sustainability modeling; policy",
        date_start="2026-06-18",
        date_end="2026-06-21",
        deadline_or_next_action_date="Register if socio-ecological modeling is a fit",
        location="Oberlin College, Oberlin, Ohio, USA",
        delivery_mode="in person",
        cost="Student regular registration after 2026-03-01 listed as USD 125 member or USD 150 non-member; full range USD 125-400.",
        free_or_online="Low-cost student rate; Degrowth Assembly listed as free for registered conference participants",
        recommended_action="Use if his computational ecology angle includes human-environment systems, sustainability, or policy modeling.",
        why_it_looks_good="Shows interdisciplinary quantitative ecology beyond a narrow biology department frame.",
        notes="Lower priority if his interests are purely ecological theory or biodiversity informatics.",
        source_url="https://ussee.org/event/2026-biennial-conference/",
    ),
    opp(
        opportunity_name="AGU26 Annual Meeting",
        opportunity_type="major Earth/environmental science conference; presentation opportunity",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Session/workshop proposal window open; abstract window opens later",
        target_student_level="students, postdocs, faculty, Earth and environmental scientists",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="ecosystem science; climate; remote sensing; Earth systems; environmental data science",
        date_start="2026-12-07",
        date_end="2026-12-11",
        deadline_or_next_action_date="2026-04-22: session/town hall/scientific workshop proposals close; 2026-08-05: abstract submissions close",
        location="Moscone Center, San Francisco, California, USA",
        delivery_mode="in person with possible online components depending on registration type",
        cost="Registration rates not posted on the source page checked for AGU26.",
        free_or_online="Not free by default",
        recommended_action="Plan an abstract by 2026-08-05 if his work involves remote sensing, climate, hydrology, carbon, or ecosystem modeling.",
        why_it_looks_good="Strong if he wants computational ecology connected to Earth systems, climate, or remote sensing labs.",
        notes="Not as ecology-specific as ESA/EFI, but broad and high-profile.",
        source_url="https://www.agu.org/annual-meeting",
    ),
    opp(
        opportunity_name="Esri User Conference 2026",
        opportunity_type="GIS/remote-sensing conference; technical training",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Open registration",
        target_student_level="students, GIS users, researchers, practitioners",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="GIS; spatial ecology; remote sensing; geospatial analysis; environmental mapping",
        date_start="2026-07-13",
        date_end="2026-07-17",
        deadline_or_next_action_date="2026-05-29: Young Professionals Network early/standard rate deadline; student rate listed without deadline",
        location="San Diego Convention Center, San Diego, California, USA",
        delivery_mode="in person plus digital access option",
        cost="Standard in-person USD 2,600; university student USD 150; digital access USD 99 or no cost for qualifying current Esri subscriptions/licenses; YPN USD 625 by 2026-05-29 then USD 1,275.",
        free_or_online="Digital access can be no cost for qualifying users; student in-person rate is low-cost",
        recommended_action="Use the student rate if he needs GIS/remote-sensing credibility; otherwise use digital access if available through school licensing.",
        why_it_looks_good="Useful if he wants to show serious spatial-ecology and geospatial-analysis skills.",
        notes="More applied/industry than ecology theory, so pair it with a research question or portfolio map/model.",
        source_url="https://www.esri.com/en-us/about/events/uc/registration",
    ),
    opp(
        opportunity_name="posit::conf(2026)",
        opportunity_type="R/Python data-science conference; workshops; virtual option",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Open registration; super early bird ends today",
        target_student_level="students, educators, analysts, data scientists, researchers",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="R; Python; reproducible workflows; Shiny; Quarto; data science; AI",
        date_start="2026-09-14",
        date_end="2026-09-16",
        deadline_or_next_action_date="2026-04-10: super early bird ends; 2026-06-22: early bird ends",
        location="Hilton Americas-Houston, Houston, Texas, USA; virtual passes available",
        delivery_mode="hybrid: in person and virtual",
        cost="Academic students/educators: USD 1,298 all access, USD 749 conference-only, USD 549 workshops-only. Virtual students/educators: USD 98 all access, USD 49 conference-only, USD 49 workshops-only. Needs-based USD 0 conference-only option listed.",
        free_or_online="Virtual student option; needs-based USD 0 conference-only option listed",
        recommended_action="Use the USD 49 virtual student conference or USD 0 needs-based option if he wants inexpensive R/Python professional development.",
        why_it_looks_good="Good for demonstrating modern reproducible R/Python workflows, but weaker than ecology-specific opportunities unless he builds a project from it.",
        notes="Prioritize the virtual or needs-based route unless travel funding is easy.",
        source_url="https://conf.posit.co/2026/pricing",
    ),
    opp(
        opportunity_name="SciPy 2026",
        opportunity_type="scientific Python conference; tutorials; sprints; virtual option coming later",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Open registration; financial-aid deadline passed; CFP closed",
        target_student_level="students, researchers, scientific Python developers",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="scientific Python; numerical computing; machine learning; data-driven discovery; open source",
        date_start="2026-07-13",
        date_end="2026-07-19",
        deadline_or_next_action_date="Financial aid deadline 2026-04-06 passed; room block closes 2026-06-22; online tickets to be released later",
        location="University of Minnesota / McNamara Alumni Center, Minneapolis, Minnesota, USA",
        delivery_mode="in person; online tickets to be released later; sprints free in person",
        cost="Student early-bird: USD 520 tutorials+conference, USD 275 tutorials-only, USD 275 conference-only. Student regular: USD 570 tutorials+conference, USD 335 tutorials-only, USD 335 conference-only. Sprints are free and open to everyone; 3.9% processing fee added at checkout.",
        free_or_online="Free sprints; online tickets planned; financial aid exists but 2026 deadline passed",
        recommended_action="Consider if he already codes in Python; if attending, join sprints and produce a visible open-source contribution.",
        why_it_looks_good="Good computational signal for Python-heavy ecology, especially if he can point to a GitHub contribution or scientific-computing workflow.",
        notes="Not ecology-specific; the value comes from applying the skills to an ecology project.",
        source_url="https://ti.to/scipy/scipy2026",
    ),
    opp(
        opportunity_name="System Dynamics Society Summer School 2026",
        opportunity_type="online summer school; simulation modeling",
        priority_tier="2 - strong if aligned",
        status_as_of_2026_04_10="Open; scholarship deadline imminent",
        target_student_level="students, recent graduates, researchers, practitioners",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="system dynamics; simulation modeling; feedbacks; coupled human-natural systems; ecological models",
        date_start="2026-06-08",
        date_end="2026-07-09",
        deadline_or_next_action_date="2026-04-15: scholarship applications; 2026-06-14: registration deadline",
        location="Online",
        delivery_mode="online asynchronous plus live sessions July 6-9",
        cost="Regular USD 600; student USD 400; Society members receive USD 100 discount; scholarships available by application.",
        free_or_online="Online; scholarships available; not free by default",
        recommended_action="Apply for scholarship by 2026-04-15 if his work involves feedback models, population dynamics, or socio-ecological systems.",
        why_it_looks_good="Concrete modeling training with a certificate, useful for theory/modeling statements.",
        notes="Frame it as ecological or socio-ecological modeling, not generic management training.",
        source_url="https://systemdynamics.org/summer-school/",
    ),
    opp(
        opportunity_name="International System Dynamics Conference 2026",
        opportunity_type="hybrid modeling conference; presentation opportunity",
        priority_tier="3 - useful skill/network",
        status_as_of_2026_04_10="Open registration; hybrid event",
        target_student_level="students, recent graduates, researchers, practitioners",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="system dynamics; simulation; policy modeling; coupled systems; uncertainty",
        date_start="2026-07-20",
        date_end="2026-07-24",
        deadline_or_next_action_date="Check conference registration and scholarship/volunteer options",
        location="TU Delft, Delft, Netherlands, plus online",
        delivery_mode="hybrid: in person and online",
        cost="Official event page lists price range USD 120-855; scholarships and volunteer registration-refund option mentioned.",
        free_or_online="Online option; scholarships/volunteering may reduce cost",
        recommended_action="Use only if his project genuinely uses system dynamics or feedback simulation; otherwise prioritize ecology-specific meetings.",
        why_it_looks_good="International modeling network and possible virtual participation, useful for socio-ecological dynamics.",
        notes="Adjacent rather than core ecology.",
        source_url="https://systemdynamics.org/event/2026-international-system-dynamics-conference/",
    ),
    opp(
        opportunity_name="Society for Freshwater Science 2026 Annual Meeting",
        opportunity_type="freshwater ecology conference; workshops; student networking",
        priority_tier="3 - useful skill/network",
        status_as_of_2026_04_10="Upcoming; early registration closed but workshops listed",
        target_student_level="students, early-career freshwater scientists, researchers",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="freshwater ecology; NEON aquatic data; R; bioassessment; watershed modeling",
        date_start="2026-05-17",
        date_end="2026-05-21",
        deadline_or_next_action_date="Register if freshwater/aquatic ecology is a fit; workshops occur 2026-05-17",
        location="Spokane, Washington, USA",
        delivery_mode="in person",
        cost="Registration rates not fully captured; workshop page lists some add-ons including a free early-career/student workshop for registered attendees and a NEON aquatic data coding workshop.",
        free_or_online="Free add-on workshop for registered attendees; not free overall",
        recommended_action="Consider if he works on streams, lakes, watersheds, or aquatic NEON data; target the NEON aquatic data coding workshop.",
        why_it_looks_good="Domain-specific if his computational ecology has freshwater/aquatic data content.",
        notes="The NEON R workshop is the most computationally relevant piece.",
        source_url="https://www.sfsannualmeeting.org/workshops",
    ),
    opp(
        opportunity_name="IALE-North America 2026 Annual Meeting",
        opportunity_type="landscape ecology conference; workshops; presentation opportunity",
        priority_tier="3 - useful skill/network",
        status_as_of_2026_04_10="Registration open; early rate and travel-award deadlines passed",
        target_student_level="students, landscape ecologists, spatial ecologists, remote-sensing researchers",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="landscape ecology; spatial ecology; remote sensing; GIS; spatial modeling",
        date_start="2026-04-19",
        date_end="2026-04-23",
        deadline_or_next_action_date="Register late only if the spatial-ecology fit is strong; otherwise monitor 2027",
        location="Athens, Georgia, USA",
        delivery_mode="in person",
        cost="Student member late rate USD 382.50 staying at host hotels/local commuter or USD 475 not staying at host hotels; student non-member late rate USD 450 or USD 550 depending on lodging category.",
        free_or_online="Not free by default; travel-award deadlines passed for 2026",
        recommended_action="Use if he has spatial/landscape ecology interests and can attend on short notice; otherwise monitor for 2027 travel awards.",
        why_it_looks_good="Strong fit for spatial ecology, GIS, landscape modeling, and remote sensing PhD interests.",
        notes="2026 is very close; likely a monitor-next-cycle item unless local/travel funding is easy.",
        source_url="https://www.ialena.org/registration.html",
    ),
    opp(
        opportunity_name="Data Carpentry Semester Biology Materials",
        opportunity_type="free self-paced training; reproducible data skills",
        priority_tier="3 - useful skill/network",
        status_as_of_2026_04_10="Available online",
        target_student_level="students and researchers building data-analysis foundations",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="data cleaning; R; reproducible analysis; biological datasets; versioned workflows",
        date_start="self-paced",
        date_end="",
        deadline_or_next_action_date="Start any time",
        location="Online",
        delivery_mode="self-paced online materials",
        cost="Free online materials.",
        free_or_online="Free and online",
        recommended_action="Complete selected modules and turn them into a clean ecology-analysis GitHub repository rather than just listing a course.",
        why_it_looks_good="Helps close practical data-skill gaps before PhD applications.",
        notes="This is a skill-builder, not a prestige item; the portfolio output matters.",
        source_url="https://datacarpentry.github.io/semester-biology/materials/",
    ),
    opp(
        opportunity_name="NEON Learning Hub Tutorials",
        opportunity_type="free self-paced training; open ecological data",
        priority_tier="3 - useful skill/network",
        status_as_of_2026_04_10="Available online",
        target_student_level="students, educators, researchers using NEON open data",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="NEON; open ecological data; R; Python; remote sensing; biodiversity observations",
        date_start="self-paced",
        date_end="",
        deadline_or_next_action_date="Start any time",
        location="Online",
        delivery_mode="self-paced online tutorials",
        cost="Free online tutorials.",
        free_or_online="Free and online",
        recommended_action="Build one polished notebook using NEON data and cite it in his CV/personal statement as an open-data project.",
        why_it_looks_good="NEON data is highly recognizable in U.S. ecology and gives him a defensible portfolio project.",
        notes="Best if paired with a question-driven mini-analysis, not just tutorial completion.",
        source_url="https://www.neonscience.org/resources/learning-hub/tutorials",
    ),
    opp(
        opportunity_name="NCEAS Learning Hub Training and Data Science Resources",
        opportunity_type="training hub; synthesis and reproducible environmental data science",
        priority_tier="3 - useful skill/network",
        status_as_of_2026_04_10="Monitor for current workshops and use resources",
        target_student_level="graduate students, researchers, environmental data scientists",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="environmental data science; synthesis; R; reproducible workflows; open science",
        date_start="varies",
        date_end="",
        deadline_or_next_action_date="Monitor NCEAS Learning Hub for current offerings",
        location="Online and Santa Barbara, California, USA depending on event",
        delivery_mode="online resources and periodic workshops",
        cost="Varies by offering; confirm on current event page.",
        free_or_online="Some resources online; event cost varies",
        recommended_action="Monitor for short courses and use their materials to strengthen reproducible analysis skills.",
        why_it_looks_good="NCEAS is well-known for ecological synthesis and open-science training.",
        notes="Included as a watch-list item because offerings change frequently.",
        source_url="https://learning.nceas.ucsb.edu/",
    ),
    opp(
        opportunity_name="Princeton EEB Theory Tea",
        opportunity_type="seminar series; theoretical ecology community",
        priority_tier="3 - useful skill/network",
        status_as_of_2026_04_10="Recurring seminar/community listing",
        target_student_level="graduate students, postdocs, researchers interested in theory",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="theoretical ecology; mathematical ecology; models; discussion group",
        date_start="recurring",
        date_end="",
        deadline_or_next_action_date="Check seminar schedule and online/public access, if any",
        location="Princeton, New Jersey, USA",
        delivery_mode="seminar; likely in person unless listed otherwise",
        cost="No fee found in local/source listing.",
        free_or_online="May be free; online access not confirmed",
        recommended_action="Use mainly as a model for identifying theory-heavy labs and papers; attend if accessible or local.",
        why_it_looks_good="Useful for learning the theoretical ecology literature and potential advisor landscape.",
        notes="Not a resume-builder unless he participates or connects it to research reading.",
        source_url="https://eeb.princeton.edu/people/group/theoretical-ecology-tea",
    ),
    opp(
        opportunity_name="SEEDS Geographic Information Systems (GIS) Graduate Workshop",
        opportunity_type="student-focused GIS workshop; watch-list item",
        priority_tier="4 - watch next cycle",
        status_as_of_2026_04_10="Most recent local listing found was 2024; monitor ESA SEEDS for recurrence/eligibility",
        target_student_level="graduate students, especially from groups targeted by SEEDS programming; confirm current eligibility",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="GIS; spatial ecology; geospatial analysis; conservation; ecology education",
        date_start="most recent local listing: 2024-05-20",
        date_end="most recent local listing: 2024-05-25",
        deadline_or_next_action_date="Monitor ESA SEEDS for next graduate GIS workshop call",
        location="Most recent local listing: Tallahassee, Florida, USA",
        delivery_mode="in person when offered",
        cost="Not captured in current local listing; confirm on next call.",
        free_or_online="Unknown; student-focused",
        recommended_action="Monitor for the next graduate GIS workshop if he wants a spatial ecology credential.",
        why_it_looks_good="Student-focused GIS training tied to ESA can be a good application signal if eligible.",
        notes="Do not list as a current 2026 opportunity unless a new call is posted.",
        source_url="https://esa.org/seeds/meetings/gis-graduate-workshop/",
    ),
    opp(
        opportunity_name="Ant Ecol Summer School 2026",
        opportunity_type="international ecology summer school; niche field/computational fit",
        priority_tier="4 - watch next cycle",
        status_as_of_2026_04_10="Upcoming 2026 offering listed in local source file; verify current application status on organizer page",
        target_student_level="students/early-career researchers interested in ant ecology; confirm eligibility",
        computational_theoretical_quantitative_flag="Potentially",
        subfield_tags="ant ecology; invasion ecology; community ecology; modeling potential; field ecology",
        date_start="2026-08-24",
        date_end="2026-08-28",
        deadline_or_next_action_date="Check application/registration deadline on organizer page",
        location="Arolla, Switzerland",
        delivery_mode="in person",
        cost="Not captured in current local listing; confirm on organizer page.",
        free_or_online="Unknown; international travel likely required",
        recommended_action="Use only if his research touches insects, invasion ecology, community ecology, or species interactions.",
        why_it_looks_good="Niche but international and student-focused; useful if the subfield fits his research story.",
        notes="Not primarily computational; value depends on matching it to a modeling/data question.",
        source_url="https://wp.unil.ch/bertelsmeiergroup/antecol/",
    ),
    opp(
        opportunity_name="ACCESS Aarhus Comprehensive Computational Entomology Summer School",
        opportunity_type="international computational summer school; watch-list item",
        priority_tier="4 - watch next cycle",
        status_as_of_2026_04_10="2025 offering found in local source file; monitor for future cycles",
        target_student_level="students/early-career researchers interested in computational entomology; confirm eligibility",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="computational entomology; ecology; bioinformatics; modeling; insects",
        date_start="most recent local listing: 2025-09-28",
        date_end="most recent local listing: 2025-10-03",
        deadline_or_next_action_date="Monitor organizer page for future calls",
        location="Aarhus, Denmark",
        delivery_mode="in person when offered",
        cost="Not captured in current local listing; confirm on future call.",
        free_or_online="Unknown; international travel likely required",
        recommended_action="Track for future cycles if insect ecology, bioinformatics, or computational biodiversity are part of his application story.",
        why_it_looks_good="The title directly signals computation plus organismal ecology if the subfield fits.",
        notes="Past event; included as a watch-list lead, not a current application target.",
        source_url="https://darsa.info/ACCESS-2025/",
    ),
    opp(
        opportunity_name="Advanced Field School in Computational Ecology",
        opportunity_type="computational ecology field school; watch-list item",
        priority_tier="4 - watch next cycle",
        status_as_of_2026_04_10="Past 2023 offering found in local source file; monitor organizer for recurrence",
        target_student_level="graduate students/early-career researchers; confirm eligibility if repeated",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="computational ecology; field ecology; modeling; data analysis",
        date_start="past local listing: 2023-05-19",
        date_end="past local listing: 2023-05-26",
        deadline_or_next_action_date="Monitor Sentinel North / Laval organizer pages for recurrence",
        location="Val-Morin, Quebec, Canada",
        delivery_mode="in person when offered",
        cost="Not captured in current local listing; confirm if repeated.",
        free_or_online="Unknown",
        recommended_action="Track only as a recurrence lead; do not treat as a current opportunity unless a new call is posted.",
        why_it_looks_good="The title is exactly aligned with computational ecology and would be high-value if repeated.",
        notes="Past event, so this is a lead for future searching rather than a live application.",
        source_url="https://sentinellenord.ulaval.ca/en/ecology2023",
    ),
    opp(
        opportunity_name="Big Data Analytics in Forestry",
        opportunity_type="quantitative ecology/forestry workshop; watch-list item",
        priority_tier="4 - watch next cycle",
        status_as_of_2026_04_10="Local listing found; current dates not captured",
        target_student_level="graduate students/researchers using forest/ecosystem data; confirm eligibility",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="forest ecology; big data; quantitative ecology; remote sensing; analytics",
        date_start="varies / current date not captured",
        date_end="",
        deadline_or_next_action_date="Check source for next offering",
        location="Flagstaff, Arizona, USA in local listing",
        delivery_mode="in person when offered",
        cost="Not captured in current local listing; confirm on source page.",
        free_or_online="Unknown",
        recommended_action="Use only if his work is forestry, ecosystem monitoring, or large environmental datasets.",
        why_it_looks_good="Relevant applied computational ecology if forest systems are part of his research target.",
        notes="Lower priority unless subfield match is strong.",
        source_url="http://quantitativeecology.org/big-data/",
    ),
    opp(
        opportunity_name="CoSMic x MICROnet Educator Training Workshop",
        opportunity_type="microbiome/data education workshop; niche fit",
        priority_tier="5 - niche/fit-dependent",
        status_as_of_2026_04_10="Upcoming/posted NEON event; eligibility appears educator/instructor oriented",
        target_student_level="educators/instructors; possibly useful for graduate TAs if eligible",
        computational_theoretical_quantitative_flag="Yes",
        subfield_tags="microbiome; ecological data; education; bioinformatics; open data",
        date_start="2026 event; exact dates not captured in output file",
        date_end="",
        deadline_or_next_action_date="Check NEON event page for eligibility and application details",
        location="Denver, Colorado, USA",
        delivery_mode="in person",
        cost="NEON source notes program support for travel and accommodation for selected participants.",
        free_or_online="Travel/accommodation support noted for selected participants; not general-audience free",
        recommended_action="Only pursue if he is teaching/TAing microbiome or data-science content and meets eligibility rules.",
        why_it_looks_good="Could help if his ecology story includes microbiome data and teaching leadership.",
        notes="Not a general grad-school resume booster for most computational ecology applicants.",
        source_url="https://www.neonscience.org/get-involved/events/cosmic-x-micronet-educator-training-workshop",
    ),
]


def tier_key(row: dict[str, str]) -> tuple[int, str, str]:
    tier = row["priority_tier"].split(" ", 1)[0]
    try:
        tier_int = int(tier)
    except ValueError:
        tier_int = 99
    start = row["date_start"]
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", start):
        start = "9999-99-99"
    if start < TODAY:
        start = f"9998-{start}"
    return tier_int, start, row["opportunity_name"].lower()


def deadline_sort_key(row: dict[str, str]) -> tuple[str, str]:
    match = re.search(r"20\d{2}-\d{2}-\d{2}", row["deadline_or_next_action_date"])
    return (match.group(0) if match else "9999-99-99", row["opportunity_name"].lower())


def md_cell(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def md_link(url: str) -> str:
    if not url:
        return ""
    return f"[source]({url})"


def write_csv(rows: list[dict[str, str]]) -> None:
    with CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    urgent = [
        r
        for r in rows
        if re.search(r"2026-04-(1[0-9]|2[0-9]|30)", r["deadline_or_next_action_date"])
        or "imminent" in r["status_as_of_2026_04_10"].lower()
    ]
    urgent = sorted(urgent, key=deadline_sort_key)
    best = [r for r in rows if r["priority_tier"].startswith("1")]
    def has_cost_access_angle(row: dict[str, str]) -> bool:
        note = row["free_or_online"].lower()
        cost = row["cost"].lower()
        mode = row["delivery_mode"].lower()
        aid_or_low_cost_markers = [
            "free and",
            "free for",
            "free sprints",
            "no fee",
            "no cost",
            "low-cost",
            "needs-based",
            "scholarship",
            "scholarships",
            "grant",
            "grants",
            "funded",
            "financial support",
            "travel awards",
            "sponsorship",
            "usd 0",
            "usd 10",
            "usd 49",
            "usd 98",
            "usd 99",
            "usd 150",
        ]
        text_without_mode = f"{note} {cost}"
        if any(marker in text_without_mode for marker in aid_or_low_cost_markers):
            return True
        if "online" in note or "virtual" in note:
            return True
        if mode.startswith("online") or mode.startswith("self-paced online") or "virtual conference" in mode:
            return True
        return False

    free_or_online = [r for r in rows if has_cost_access_angle(r)]

    lines = []
    lines.append("# Computational Ecology Opportunities for a Master's Student")
    lines.append("")
    lines.append(f"Verified and compiled on {TODAY}. This packet prioritizes opportunities that would strengthen a computational, theoretical, or quantitative ecology PhD application. Rows marked as past/closed are intentionally included only when they are high-signal watch-list items for the next cycle.")
    lines.append("")
    lines.append("## How to Use This")
    lines.append("")
    lines.append("- Best CV signal: submit a poster/abstract, win travel support, complete a selective workshop, or produce a public GitHub/notebook artifact from a training.")
    lines.append("- Highest near-term value: EFI 2026, Evolution 2026 support/virtual option, ECMTB grants, GRS/GRC Unifying Ecology Across Scales, and one online/free skill-builder tied to a small project.")
    lines.append("- High-signal watch-list items for later cycles: SPEC School, BIOS2 summer schools, CV4Ecology, ESIIL, and SFI Complex Systems Summer School.")
    lines.append("- For any generic data-science conference, make the ecology link explicit. A short reproducible ecology project is more persuasive than simply listing attendance.")
    lines.append("")
    lines.append("## Immediate Deadline Checklist")
    lines.append("")
    lines.append("| Deadline / action date | Opportunity | Recommended action | Source |")
    lines.append("|---|---|---|---|")
    for r in urgent:
        lines.append(
            f"| {md_cell(r['deadline_or_next_action_date'])} | {md_cell(r['opportunity_name'])} | {md_cell(r['recommended_action'])} | {md_link(r['source_url'])} |"
        )
    lines.append("")
    lines.append("## Best Application Signals")
    lines.append("")
    lines.append("| Opportunity | Dates | Location / mode | Cost notes | Why it helps |")
    lines.append("|---|---|---|---|---|")
    for r in best:
        dates = r["date_start"] if not r["date_end"] else f"{r['date_start']} to {r['date_end']}"
        loc = f"{r['location']} ({r['delivery_mode']})"
        lines.append(
            f"| {md_cell(r['opportunity_name'])} | {md_cell(dates)} | {md_cell(loc)} | {md_cell(r['cost'])} | {md_cell(r['why_it_looks_good'])} |"
        )
    lines.append("")
    lines.append("## Free, Online, Funded, or Lower-Cost Options")
    lines.append("")
    lines.append("| Opportunity | Cost/access note | Recommended use | Source |")
    lines.append("|---|---|---|---|")
    for r in free_or_online:
        lines.append(
            f"| {md_cell(r['opportunity_name'])} | {md_cell(r['free_or_online'])} | {md_cell(r['recommended_action'])} | {md_link(r['source_url'])} |"
        )
    lines.append("")
    lines.append("## Full Opportunity List")
    lines.append("")
    lines.append("| Tier | Opportunity | Type | Dates | Location / mode | Cost | Action | Source |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in rows:
        dates = r["date_start"] if not r["date_end"] else f"{r['date_start']} to {r['date_end']}"
        loc = f"{r['location']} ({r['delivery_mode']})"
        lines.append(
            f"| {md_cell(r['priority_tier'])} | {md_cell(r['opportunity_name'])} | {md_cell(r['opportunity_type'])} | {md_cell(dates)} | {md_cell(loc)} | {md_cell(r['cost'])} | {md_cell(r['recommended_action'])} | {md_link(r['source_url'])} |"
        )
    lines.append("")
    lines.append("## Notes on Scope")
    lines.append("")
    lines.append("- I excluded generic public naturalist workshops and local public events unless they had a clear computational, quantitative, theoretical, GIS, forecasting, remote-sensing, or graduate-student training angle.")
    lines.append("- Costs and dates can change. Confirm the source URL before applying or paying, especially for registration rates and deadlines.")
    lines.append("- The CSV version has more detail per row, including subfield tags, student fit, and status as of the verification date.")
    lines.append("")
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = sorted(OPPORTUNITIES, key=tier_key)
    write_csv(rows)
    write_markdown(rows)
    print(f"Wrote {CSV_OUT} with {len(rows)} opportunities")
    print(f"Wrote {MD_OUT}")


if __name__ == "__main__":
    main()
