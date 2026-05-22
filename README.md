# CPDSE Website Guide

Website design & how to update content.

---

## Hero

The hero is the top area of each page. It has a gradient and subtle pattern in the background.

![Example hero section](docs/example-hero.png)

To update the hero, edit the frontmatter at the top of the page's `.md` file:

```yaml
---
layout: sectioned-page        # always sectioned-page for standard pages
eyebrow: Research             # small all-caps label above the headline (optional)
title: Page Title             # the big headline
description: Descriptive text shown below the title.
permalink: /your-url/         # what comes after cpdse.dk/
---
```

**URL naming rule:** always use a flat, single-level permalink — `cpdse.dk/page-name/` — never a nested path like `cpdse.dk/section/page-name/`. Even if the `.md` file lives in a subfolder (e.g. `education/`), the permalink should still be `/page-name/`.

---

## Content sections

The content below the hero is divided into sections. Each section has a separate background colour. Usually **Soft White** and **Mint Gray** are used in alternating order, beginning with Soft White. Highlight sections use **Forest Green**.

To add content, open the page's `.md` file and add a `sections:` list after the frontmatter `---`. Each item in the list becomes one full-width section band.

### Section header fields

All three header fields are optional. Omit any you don't need.

```yaml
sections:
  - color: soft-white          # soft-white | mint-gray | forest-green
    eyebrow: Philosophy        # small all-caps label above the title
    title: Section Headline    # large headline
    intro: Lead paragraph shown beneath the title in a smaller, muted style.
```

Each section then contains exactly one layout type, described below.

---

### Layout 1 — Plain text

A single column of markdown content. Supports paragraphs, **bold**, *italic*, [links](https://example.com), and bullet lists. Custom HTML is also accepted.

```yaml
  - color: soft-white
    title: Our Approach
    content: |
      Regular paragraph text here.

      - Item one
      - Item two
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

Cards arranged in a grid. The `cards:` key is required; everything else is optional.

```yaml
  - color: mint-gray
    title: What we offer
    card_columns: 3            # 2 | 3  (default: 3)
    card_color: soft-white     # soft-white | ivory  (default: soft-white)
    card_style: alternating    # odd cards get a filled forest-green background
    cards:
      - icon: community        # SVG icon name from _includes/icons/ (no .svg)
        num: "01"              # small label shown above the title
        title: First Card
        content: Body text for this card.
        link_text: Learn more  # optional call-to-action link
        link_url: /some-page/
        link_external: true    # opens in new tab
      - title: Second Card     # icon, num, link_text are all optional
        content: Body text for the second card.
```

All card fields except `title` and `content` are optional. Cards without an `icon:` simply render without one.

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
