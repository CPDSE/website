---
layout: sectioned-page
title: Educational Programme
eyebrow: Education
permalink: /educational-programme/
description: How CPDSE thinks about data science education in pharmaceutical sciences — and why it matters.

sections:

  - color: soft-white
    title: "Why data science for pharmacists"
    image:
      src: /assets/images/Why-Data-Science.webp
      alt: R code in RStudio for pharmaceutical data analysis — tablet content, blood pressure, and drug release plots
      position: right
    content: |
      Pharmaceutical science generates more data than ever, from high-throughput screening to real-world patient records. The students and researchers who can work with that data directly and communicate with data specialists, are at a fundamental advantage. CPDSE exists to close that gap.

      Integrating data science into pharmaceutical workflows marks a pivotal shift from manual, siloed analysis to a unified, computational framework that accelerates discovery and guarantees reproducibility. By harnessing the power of free, industry-standard open-source ecosystems like Python and R, organizations can seamlessly execute complex tasks across the entire development spectrum ranging from lab data analysis and image processing to predictive simulations.

      This transition not only democratizes access to advanced analytics but also establishes a robust foundation for data-driven innovation in modern pharmacy.

      [Track the progress of data science integration into the pharmacy curricula at SDU and UCPH →](https://cpdse.ku.dk/edu_circle/pharma-ds-dashboard_server_static_mock.html){:.btn .btn-primary target="_blank"}

  - color: sage-green
    title: "What We Offer"
    intro: "From regular talks to open learning materials — everything CPDSE produces is freely accessible to students, researchers, and practitioners at every level."
    card_columns: 3
    card_color: soft-white
    cards:
      - title: Convergence Talks
        content: "Regular 30-minute talks on topics at the intersection of pharmaceutical science and data science. Free to attend — join us in person or follow along online."
        link_text: "View upcoming talks →"
        link_url: /news-events/

      - title: Pharma Code Club
        content: "A collaborative space for students at SDU or KU to practice and advance data science skills. All levels welcome — no prior experience required."
        link_text: "About the Code Club →"
        link_url: /codeclub/

      - title: Open Source Materials
        content: "All data science curriculum materials — datasets, notebooks, exercises, and more — are openly published so anyone can learn, reuse, and contribute."
        link_text: "Browse on GitHub →"
        link_url: https://github.com/CPDSE-EDUX
        link_external: true

      - title: Cheat Sheets
        content: "Concise, printable reference cards covering essential data science and pharmaceutical concepts — Python, R, statistics, and more. Made by CPDSE for students and practitioners."
        link_text: "View cheat sheets →"
        link_url: https://github.com/CPDSE-EDUX/CheatSheets
        link_external: true

      - title: R Documentation
        content: "Worked R examples across pharmacometrics, pharmacovigilance, and drug data science — documented and annotated for learners at all levels."
        link_text: "Open R docs →"
        link_url: https://cpdse-edux.github.io/R_documentation/
        link_external: true

  - color: soft-white
    title: "What data science actually is"
    intro: "Data science is often treated as synonymous with machine learning or coding. In reality it is a broad competency spanning ethics, mathematics, computing, data management, analysis, AI, and communication."
    include: competency-model.html
    pillars:
      - title: "Mathematics & Statistics"
        icon: "ti-math-function"
        color: "#E6F1FB"
        iconColor: "#0C447C"
        borderColor: "#378ADD"
        desc: "Foundational quantitative reasoning, statistical inference, and mathematical modeling."
      - title: "Computing & Programming"
        icon: "ti-terminal-2"
        color: "#EEEDFE"
        iconColor: "#3C3489"
        borderColor: "#7F77DD"
        desc: "Software development, scripting, and computational thinking for data workflows."
      - title: "Data Acquisition & Management"
        icon: "ti-database"
        color: "#E1F5EE"
        iconColor: "#085041"
        borderColor: "#1D9E75"
        desc: "Collecting, storing, cleaning, and governing data at scale."
      - title: "Exploration, Mining & Analysis"
        icon: "ti-telescope"
        color: "#FAEEDA"
        iconColor: "#633806"
        borderColor: "#BA7517"
        desc: "Uncovering patterns, anomalies, and insights from raw datasets."
      - title: "Visualization & Presentation"
        icon: "ti-chart-bar"
        color: "#FBEAF0"
        iconColor: "#72243E"
        borderColor: "#D4537E"
        desc: "Designing compelling charts, dashboards, and data stories for diverse audiences."
      - title: "Machine Learning & AI"
        icon: "ti-brain"
        color: "#EEEDFE"
        iconColor: "#26215C"
        borderColor: "#534AB7"
        desc: "Building, evaluating, and deploying predictive and generative models."
      - title: "Ethics, Legislation & Privacy"
        icon: "ti-scale"
        color: "#EAF3DE"
        iconColor: "#27500A"
        borderColor: "#639922"
        desc: "Ensuring responsible, lawful, and transparent use of data and AI systems."

  - color: sage-green
    title: "How to Include Data Science in Education"
    intro: "Data science is more than programming. It originates in algorithmic thinking and data literacy, extending to the application of advanced algorithms and ethical judgment. Some practical ways to include data science in the curricular are:"
    card_columns: 3
    card_color: soft-white
    cards:
      - title: Coding exercises
        content: |
          - Use R or Phthon
          - Students analyze their own lab data
          - Simulation of processes that are not covered in the lab
      - title: Lab reports in notebooks
        content: |
          - Use Quarto
          - Integrate code, results, and interpretation
          - Directly exportable (HTML, PDF, WOrd) and reproducible
      - title: Interactive apps
        content: |
          - Build interactive Shiny or Streamlit apps
          - Turn an analysis into a shareable tool
          - Allows data exploration without coding
---
