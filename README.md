# Website
New version of the CPDSE website using Jekyll.

---

## Editing pages

Pages are edited as `.md` files. The top of each file contains **front matter** — a block of keywords between `---` lines that controls the page layout and content. No HTML is needed.

### Page hero

Every page has a hero section at the top. These keywords are the same for all pages:

```yaml
---
title: Page Title              # large headline in the hero
hero_label: Research           # small label above the headline (e.g. the section name)
description: One or two sentences shown beneath the headline.
permalink: /your-url/          # the URL of the page
---
```

---

### Content sections (`layout: sectioned-page`)

Pages that use `layout: sectioned-page` can define any number of sections in their front matter. Each section is one item in the `sections:` list.

**Every section can have:**

```yaml
sections:
  - color: soft-white          # section background: soft-white | ivory | forest-green
    title: Section Headline    # large heading at the top of the section
    intro: Lead paragraph shown beneath the title in a smaller, muted style.
```

---

#### Plain text

A single column of text, capped at a readable width.

```yaml
  - color: soft-white
    title: Our Approach
    intro: Optional lead sentence.
    content: |
      Regular paragraph text here. Supports **bold**, *italic*,
      [links](https://example.com), and bullet lists.

      - Item one
      - Item two
```

---

#### Cards

A grid of cards. Control the number of columns and the card background colour.

```yaml
  - color: ivory
    title: What we offer
    intro: Optional lead sentence.
    card_columns: 2            # 2 | 3
    card_color: soft-white     # soft-white | ivory
    cards:
      - title: First Card
        content: Body text for the first card.
      - title: Second Card
        content: Body text for the second card.
```

---

#### Two text columns

Splits the content area into two equal columns.

```yaml
  - color: soft-white
    title: Two perspectives
    columns:
      - content: |
          **At UCPH** we focus on drug design and formulation.
      - content: |
          **At SDU** we work on epidemiology and statistics.
```

---

#### Image + text

Places an image alongside a block of text. The image can go on the left or right.

```yaml
  - color: soft-white
    title: The team
    image:
      src: /assets/images/team.jpg
      alt: CPDSE team photo
      position: right          # left | right
    content: |
      We are a cross-institutional group of researchers,
      educators, and data scientists.
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
