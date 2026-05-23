# CPDSE Website Guide

Website design & how to update content.

---

## Content files — quick reference

Files are listed in nav-bar order. Click the path to open the file.

| Nav item | File to edit | Notes |
|---|---|---|
| **Home** | [`markdown/home/index.md`](markdown/home/index.md) | Sections-based; hero text in frontmatter |
| **News & Events** | [`markdown/news/news-events.md`](markdown/news/news-events.md) | Page intro; individual posts in [`_posts/news/`](_posts/news/) |
| — *individual posts* | [`_posts/news/`](_posts/news/) | One `.md` file per post; date in filename |
| **About CPDSE** | [`markdown/about/about.md`](markdown/about/about.md) | Sections-based |
| **People** | [`markdown/about/people.md`](markdown/about/people.md) | `intro_left:` for the hero text; person data in `assets/data/people.json` |
| **Corporate Identity** | [`markdown/about/corporate-identity.md`](markdown/about/corporate-identity.md) | |
| **Educational Vision** | [`markdown/education/educational-vision.md`](markdown/education/educational-vision.md) | Competency model pillar text under `pillars:` |
| **Educational Offers** | [`markdown/education/educational-offers.md`](markdown/education/educational-offers.md) | |
| **Learning Resources** | [`markdown/education/learning-resources.md`](markdown/education/learning-resources.md) | |
| **Student Code Club** | [`markdown/education/codeclub.md`](markdown/education/codeclub.md) | Landing/hub page |
| — SDU Code Club | [`markdown/education/codeclub-sdu.md`](markdown/education/codeclub-sdu.md) | Sections-based |
| — KU Code Club | [`markdown/education/codeclub-ku.md`](markdown/education/codeclub-ku.md) | Raw HTML (`layout: bare`) — no sections system, no site chrome |
| **Researchers & Units** | [`markdown/research/research-units.md`](markdown/research/research-units.md) | Department grid, PhD students, and group leaders all in frontmatter |
| **Contact** | [`markdown/contact/contact.md`](markdown/contact/contact.md) | |
| Funding *(not in nav)* | [`markdown/other/funding.md`](markdown/other/funding.md) | |
| Privacy *(not in nav)* | [`markdown/other/privacy.md`](markdown/other/privacy.md) | |

---

## Hero

The hero is the full-width banner at the top of each interior page. It has a dark green gradient background with a subtle dot pattern.

![Example hero section](docs/example-hero.png)

**Colours:** the eyebrow and `h1` title are both **antique gold** (`#D6C17C`). The description paragraph is soft-white at reduced opacity.

To update the hero, edit the frontmatter at the top of the page's `.md` file:

```yaml
---
layout: sectioned-page        # always sectioned-page for standard pages
eyebrow: Research             # small all-caps label above the headline (optional)
title: Page Title             # the big headline (antique gold)
description: Descriptive text shown below the title.
permalink: /your-url/         # what comes after cpdse.dk/
---
```

**URL naming rule:** always use a flat, single-level permalink — `cpdse.dk/page-name/` — never a nested path like `cpdse.dk/section/page-name/`. Even if the `.md` file lives in a subfolder (e.g. `education/`), the permalink should still be `/page-name/`.

**Special layout — bare:** the KU Code Club page uses `layout: bare`, which strips the site nav, hero, and footer entirely so the page can render its own full-screen HTML.

---

## Content sections

The content below the hero is divided into sections. Each section has a separate background colour. Four approved colour pairings are available:

| Background | `color:` value | Headlines & eyebrows | Body text |
|---|---|---|---|
| Soft White | `soft-white` | Forest Green | Charcoal |
| Mint Gray | `mint-gray` | Ivory Gold Tint | Charcoal |
| Sage Green | `sage-green` | Warm Sand | Soft White |
| Forest Green | `forest-green` | Antique Gold | Soft White |

To add content, open the page's `.md` file and add a `sections:` list after the frontmatter `---`. Each item in the list becomes one full-width section band.

### Section header fields

All three header fields are optional. Omit any you don't need.

```yaml
sections:
  - color: soft-white          # soft-white | mint-gray | sage-green | forest-green
    eyebrow: Philosophy        # small all-caps label above the title
    title: Section Headline    # large headline
    intro: Lead paragraph shown beneath the title in a smaller, muted style.
```

Each section then contains exactly one layout type, described below.

---

### Layout 1 — Plain text

A single column of markdown content. Supports paragraphs, **bold**, *italic*, [links](https://example.com), bullet lists, and blockquotes.

```yaml
  - color: soft-white
    title: Our Approach
    content: |
      Regular paragraph text here.

      - Item one
      - Item two

      > A pull-quote styled as a blockquote.
```

---

### Layout 2 — Two columns

Two blocks of text placed side by side.

```yaml
  - color: soft-white
    columns:
      - content: |
          **At UCPH** we focus on drug design and formulation.
      - content: |
          **At SDU** we work on epidemiology and statistics.
```

---

### Layout 3 — Cards

Cards arranged in a grid.

```yaml
  - color: sage-green
    title: What we offer
    card_columns: 3            # 2 | 3  (default: 3)
    card_color: soft-white     # soft-white (default) — works on both light and dark sections
    card_style: alternating    # odd cards get a filled forest-green background
    cards:
      - icon: community        # SVG icon name from _includes/icons/ (no .svg)
        num: "01"              # small label shown above the title
        title: First Card
        content: Body text for this card. Markdown lists work here too.
        link_text: Learn more  # optional call-to-action link
        link_url: /some-page/
        link_external: true    # opens in new tab
      - title: Second Card     # icon, num, link_text are all optional
        content: Body text for the second card.
```

`card_color: soft-white` gives white cards with forest-green titles and charcoal body text regardless of the section background colour — including on dark `sage-green` and `forest-green` sections.

---

### Layout 4 — Image + text

An image placed alongside a block of text.

```yaml
  - color: soft-white
    image:
      src: /assets/images/team.jpg
      alt: CPDSE team photo
      position: right          # left | right  (default: left)
    content: |
      We are a cross-institutional group of researchers,
      educators, and data scientists.
```

---

### Layout 5 — Stats banner

A row of large animated numbers. Works best with `color: forest-green`.

```yaml
  - color: forest-green
    stats:
      - number: 60
        suffix: "+"            # optional: +, %, ×, etc.
        label: People
      - number: 7
        label: Departments
```

---

### Layout 6 — HTML include

Renders a custom HTML partial from `_includes/`. The full section data is passed as `include.section`, so custom keys added to the YAML become available inside the partial.

```yaml
  - color: soft-white
    title: Competency Model
    include: competency-model.html
    pillars:                   # custom key read by competency-model.html
      - title: "Mathematics & Statistics"
        icon: "ti-math-function"
        desc: "..."
```

---

## News posts

Individual news items live in [`_posts/news/`](_posts/news/). The filename must follow the format `YYYY-MM-DD-slug.md`.

```yaml
---
layout: post
title: "Post headline"
date: 2026-05-23
category: news
description: One-sentence summary shown in the news feed.
---

Post body in markdown.
```

Set `future: true` is already enabled in `_config.yml`, so posts with future dates are built and visible on the site.

---

## People data

The people visualisation and directory on the [People page](markdown/about/people.md) are driven by [`assets/data/people.json`](assets/data/people.json). Edit that file to add, remove, or update people.

The hero intro text (left column) is editable via the `intro_left:` frontmatter field in [`markdown/about/people.md`](markdown/about/people.md).

---

## Update Danish pharma snapshot

The About section visualization reads from `assets/data/pharma_snapshot.json`.

To regenerate that snapshot from Medstat download files, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/update-pharma-snapshot.ps1
```

Optional parameters:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/update-pharma-snapshot.ps1 -OutputPath "assets/data/pharma_snapshot.json" -MaxLookbackYears 8
```
