---
layout: home
title: Home
permalink: /

# ── Hero ──────────────────────────────────────────────────────────────────────
eyebrow: Center for Pharmaceutical Data Science Education
hero_headline: "Pharma is full of data,<br>but not <em>data science.</em>"
hero_sub: We are here to change that — educating the next generation of drug experts who speak both data and drugs.

# ── Stats strip (the forest-green band below the hero) ────────────────────────
stats:
  - number: 60
    suffix: "+"
    label: People
  - number: 7
    label: Departments
  - number: 7
    label: Courses Upgrading
  - number: 6
    label: PhD Scholarships

# ── Data story (about strip) ──────────────────────────────────────────────────
# Numbers live in _data/pharma_data_growth.json. Colours are data-viz series
# colours (deliberately outside the four-pairing palette — approved choice).
viz_label: Pharma is full of data
viz_finale_number: "1.6M+"
viz_finale_unit: data records since 2000
viz_curve_color: "#E3B043"
viz_hot_color: "#9A6B0A"
viz_series:
  - key: ct
    name: Clinical trials
    color: "#D85A30"
    dash: ""
  - key: pm
    name: Drug papers
    color: "#7F77DD"
    dash: "6 4"
  - key: pdb
    name: Protein structures
    color: "#1D9E75"
    dash: "2 4"
viz_annotation:
  year: 2005
  series: ct
  lines:
    - "2005 — trial registration"
    - "required to publish"
viz_sources_intro: "New records per year. Sources:"
viz_sources:
  - label: ClinicalTrials.gov
    url: "https://clinicaltrials.gov/"
  - label: PubMed
    url: "https://pubmed.ncbi.nlm.nih.gov/"
  - label: RCSB Protein Data Bank
    url: "https://www.rcsb.org/"
viz_steps:
  - intro: true
    caption: "In 2000, pharma produced <span class='ds-num' data-series='hot'>under 20,000</span> new data records a year. Today it's <span class='ds-num' data-series='hot'>over 100,000</span> — and still climbing."
  - show: [ct]
    anno: true
    caption: "Where does it all come from? Start with clinical trials — about <span class='ds-num' data-series='ct'>43,000</span> registered in 2025, roughly <span class='ds-num' data-series='ct'>40×</span> the number in 2000."
  - show: [ct, pm]
    caption: "Add the literature: PubMed absorbed over <span class='ds-num' data-series='pm'>45,000</span> new drug-research papers in 2025 alone."
  - show: [ct, pm, pdb]
    caption: "And the molecules themselves — <span class='ds-num' data-series='pdb'>17,000+</span> new protein structures released in 2025, up from <span class='ds-num' data-series='pdb'>a few thousand</span> a year in 2000."
  - show: [ct, pm, pdb]
    finale: true
    caption: "Three public sources. <span class='ds-num' data-series='hot'>1.6 million+</span> records since 2000. Pharma is full of data — what it needs is the <em>data science</em> to read it."

# ── About intro ───────────────────────────────────────────────────────────────
about_label: About CPDSE
about_headline: "Pharmaceutical sciences,<br><em>boosted by data science</em>"
about_body:
  - "The Center for Pharmaceutical Data Science Education (CPDSE) is dedicated to developing research-based education for the future workforce of drug experts, spanning bachelor, master, PhD and life-long learning levels. Pharmaceutical scientists will become bilinguals speaking both “data and drugs”. CPDSE works closely with students, university teachers and researchers, as well as professionals from the pharmaceutical industry to ensure education that is relevant, collaborative, and aligned with real-world needs."

# ── Community ─────────────────────────────────────────────────────────────────
community_label: Community
community_headline: "Who are we"
community_body:
  - CPDSE is a cross-institutional community of students, researchers, educators, data scientists, pharmacists and collaborators working together to strengthen pharmaceutical data science education.
  - "We grow through shared projects, workshops, retreats, teaching development and everyday collaboration across UCPH and SDU. What makes the center valuable is not only the formal structure, but the people in it: a community that exchanges ideas, builds capacity and helps each other move from plans to practice."

# ── Audience / Who we serve ───────────────────────────────────────────────────
audience_label: Who we serve
audience_headline: "Educate <em>data &amp; drug</em> bilinguals"
audience_intro: We aim to upskill and educate people that understand and can apply the right data science across the breadth of the pharmaceutical value chain.
audience_cards:
  - category: Students
    number: "01"
    title: A safe space to learn data science
    body: We provide consultations to help you enter data science, overcome project challenges, and build data literacy. We run workshops and coding events, creating a safe and collaborative space.
    offers:
      - Drop-in data science consultations
      - Coding workshops & hackathons
      - Project guidance & peer learning
      - Open teaching materials on GitHub
  - category: "Teachers & Researchers"
    number: "02"
    title: Hands-on tools to teach data science
    body: We develop hands-on educational materials to embed and expand data science in university curricula, while training educators and providing data-driven methodological expertise.
    offers:
      - Ready-to-use course modules
      - Educator training in data methods
      - Curriculum integration support
      - Methodological consulting
  - category: Life-long Learners
    number: "03"
    title: A network beyond the university
    body: We reach beyond university borders by creating opportunities for networking and continuous knowledge exchange through workshops, symposiums, and community events.
    offers:
      - Industry networking events
      - Symposiums & community meetups
      - Continuing education workshops
      - Online resources & tutorials
audience_ctas:
  - label: Teaching Materials on GitHub
    url: https://github.com/CPDSE-EDUX
    external: true
  - label: Research Materials on GitHub
    url: https://github.com/CPDSE
    external: true

# ── Spotlight (tabbed feature band below "Who we serve") ──────────────────────
spotlight_label: What we offer
spotlight_headline: "Engage with us"
spotlight_intro: Three ways to work with the center, whether you teach, study, or want to build your own data science skills.
spotlight:
  - title: Access Resources
    body: We develop and publish free educational resources for data science in pharma — two short steps in Python or R to get started, then a full library for when you want to go deeper.
    image: /assets/images/Why-Data-Science-spotlight.webp
    alt: Why data science matters for pharmaceutical sciences
    link_text: Read more
    link_url: /learning-resources/
  - title: Employ Services
    body: We help teachers adapt their courses to modern requirements and the growing need to include data science, upgrading and reforming pharma curricula across all levels.
    image: /assets/images/retreat-01-2026-spotlight.jpg
    alt: CPDSE members at the January 2026 retreat
    link_text: Read more
    link_url: /curriculum-development/
  - title: Join Us
    body: Visit us and join our talks, take on a project opportunity, or become a fellow — several ways to get involved with the community.
    image: /assets/images/new-years-celebration-spotlight.jpg
    alt: CPDSE community at a new year celebration
    link_text: Read more
    link_url: /join-us/

# ── Funders ───────────────────────────────────────────────────────────────────
funders_note: "This work was supported by the Novo Nordisk Foundation (NNF24SA0092613), the LEO Foundation (LF-ST-24-500013), and the Lundbeck Foundation (R469-2024-629) through funding to the Center for Pharmaceutical Data Science Education."
---
