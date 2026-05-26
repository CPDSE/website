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

### 📝 Create a new news post (one click)

[**→ Open GitHub's "create new file" editor pre-filled with the news post template**](https://github.com/CPDSE/website/new/main/_posts/news?filename=YYYY-MM-DD-slug.md&value=---%0Alayout%3A%20post%0Atitle%3A%20%22Your%20post%20title%20here%22%0Adate%3A%202026-05-26%0Acategory%3A%20Announcement%0Adescription%3A%20One-sentence%20summary%20shown%20in%20the%20news%20feed.%0A---%0A%0AOpening%20paragraph%20%E2%80%94%20keep%20it%20short%20and%20direct.%20This%20is%20what%20readers%20see%20in%20the%20news%20feed%20preview%2C%20so%20make%20it%20count.%0A%0A%23%23%20A%20subheading%0A%0AMarkdown%20formatting%20works%20here.%20You%20can%20use%20%2A%2Abold%20text%2A%2A%2C%20%2Aitalic%20text%2A%2C%20and%20%5Bexternal%20links%5D%28https%3A%2F%2Fexample.com%29.%0A%0A%23%23%23%20A%20smaller%20subheading%0A%0A-%20Bullet%20list%20item%20one%0A-%20Bullet%20list%20item%20two%0A-%20Bullet%20list%20item%20three%0A%0A1.%20Numbered%20list%0A2.%20Works%20the%20same%20way%0A3.%20Each%20item%20on%20its%20own%20line%0A%0A%3E%20A%20blockquote%20%E2%80%94%20useful%20for%20pull-quotes%20or%20short%20citations.%0A%0AYou%20can%20also%20use%20%60inline%20code%60%20and%20fenced%20code%20blocks%3A%0A%0A%60%60%60r%0A%23%20Example%20R%20snippet%0Alibrary%28tidyverse%29%0Adf%20%25%3E%25%20filter%28year%20%3D%3D%202026%29%0A%60%60%60%0A%0AFor%20images%2C%20place%20the%20file%20under%20%60%2Fassets%2Fimages%2F%60%20and%20reference%20it%20like%3A%0A%0A%21%5BAlt%20text%20describing%20the%20image%5D%28%2Fassets%2Fimages%2Fexample.jpg%29%0A%0AYou%20can%20also%20create%20tables%3A%0A%0A%7C%20Column%20A%20%7C%20Column%20B%20%7C%20Column%20C%20%7C%0A%7C---%7C---%7C---%7C%0A%7C%20Row%201%20%20%20%20%7C%20Value%20%20%20%20%7C%2042%20%20%20%20%20%20%20%7C%0A%7C%20Row%202%20%20%20%20%7C%20Value%20%20%20%20%7C%2088%20%20%20%20%20%20%20%7C%0A%0AClose%20with%20a%20short%20call-to-action%20paragraph%20or%20link%2C%20e.g.%20%22%5BRead%20more%20on%20our%20research%20page%5D%28%2Fresearchers-units%2F%29%22.%0A)

The editor opens with the frontmatter and a markdown-formatting demo already in place. You only need to:

1. Replace `YYYY-MM-DD-slug.md` in the filename field with the real date and a short slug
2. Edit the title, date, category, description, and body
3. Click **"Commit new file"** at the bottom of the page

### Fallback: copy from the reference template

If you'd rather copy-paste manually (or you're working locally), the same template lives at [`_posts/news/_template.md`](_posts/news/_template.md). It is excluded from the Jekyll build (declared in `_config.yml`), so it never shows up as a real post.

### Post frontmatter

```yaml
---
layout: post
title: "Post headline"
date: 2026-05-23
category: Announcement
description: One-sentence summary shown in the news feed.
---

Post body in markdown.
```

`future: true` is already enabled in `_config.yml`, so posts with future dates are built and visible on the site.

---

## Adding images

Site images live in [`assets/images/`](assets/images/). Reference them in markdown with `/assets/images/filename.ext` (the leading `/` is important — it resolves to the site root, baseurl-aware).

**Compress before committing.** Phone cameras and screenshots often produce 3–10 MB files that load slowly on mobile. Use [**squoosh.app**](https://squoosh.app) — a free, browser-based image compressor by Google. Drop the image in, pick **WebP** or **MozJPEG** on the right-hand panel, and aim for under 500 KB. WebP usually gives the best size-to-quality ratio for screenshots and photos and is supported by every modern browser.

Naming convention: `Capitalised-With-Hyphens.webp` (or `.jpg`/`.png`). Avoid spaces.

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
