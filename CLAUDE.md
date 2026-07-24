# CPDSE Website — Claude Guidelines

This is a Jekyll static site deployed via GitHub Pages to the custom domain `https://cpdse.dk` (CNAME file; `baseurl: ""`). Content is edited through `.md` files; the layout and design system must not be changed without explicit instruction.

---

## How to handle requests that conflict with these guidelines

If a user asks for something that would break a rule in this file — wrong colour, new font, edits to a forbidden file, content changes outside the requested scope, an inline `style=` attribute, a non-approved layout, anything that contradicts the design system — **do not silently comply**. Instead:

1. **Stop before making the change.**
2. **Tell the user clearly which rule the request conflicts with** and quote the relevant line from this file.
3. **Explain what the rule exists to protect** (consistency, design system, content boundaries).
4. **Offer the closest compliant alternative**, if there is one.
5. **Ask for explicit confirmation** before proceeding. A reply like "yes do it anyway" or "override the rule for this case" is required — silence or ambiguity means do not proceed.

The user is the project owner and can override any rule, but they must do so knowingly. Never assume an override; never bury the warning in a long reply. The warning comes first.

---

## Content editing — always use the MD files

Every page has a `.md` source file. See `README.md` for the full table. **Never hardcode content into layout files, includes, or CSS.** The sections system in `_includes/page-section.html` reads YAML frontmatter and handles all rendering.

---

## Do not change content the user did not ask about

**Only modify the specific text, section, or element the user explicitly named.** Surrounding paragraphs, headings, links, images, lists, and YAML values must be left exactly as they are.

- Do **not** rewrite, paraphrase, or "improve" copy that the user did not call out — even if it has typos, awkward phrasing, or grammar issues
- Do **not** change wording, capitalisation, punctuation, or tone in unrelated sections
- Do **not** swap images, alt text, URLs, or link labels outside the requested change
- Do **not** reorder sections, cards, or list items unless asked
- Do **not** "tidy up" YAML — keep existing keys, quoting style, and spacing intact for fields you aren't touching
- If you notice a likely typo or factual issue while making a different change, **mention it in your reply** and let the user decide — do not fix it silently

When in doubt about scope, ask before editing rather than guessing. A minimal, surgical change is always preferred over a broad sweep.

---

## Colour system — four approved pairings only

| `color:` value | Background | Headlines & eyebrows | Body text |
|---|---|---|---|
| `soft-white` | `#F9F9F9` | Forest Green `#3C5E3E` | Charcoal `#333333` |
| `mint-gray` | `#A9BBAA` | Ivory Gold Tint `#F6F1DC` | Charcoal `#333333` |
| `sage-green` | `#5F7D61` | Warm Sand `#E4D7A1` | Soft White `#F9F9F9` |
| `forest-green` | `#3C5E3E` | Antique Gold `#D6C17C` | Soft White `#F9F9F9` |

**Never introduce a new background colour.** If a section needs a dark background, use `sage-green` or `forest-green`. If it needs a light background, use `soft-white` or `mint-gray`.

Use CSS custom property tokens — never raw hex values in new rules:

```
--color-forest-green   --color-soft-white   --color-sage-green
--color-mint-gray      --color-warm-sand    --color-antique-gold
--color-ivory-gold-tint  --color-charcoal   --color-ivory
--color-antique-gold   (also available as var(--accent))
```

---

## Hero (page banner)

- Background: dark green gradient (defined in `.page-hero` in `main.css`) — do not change
- `h1` title: **antique gold** (`var(--accent, #D6C17C)`) — do not override to white
- Eyebrow (`hero-label`): **antique gold** — already set globally, do not override
- Description `<p>`: soft-white at reduced opacity — do not change

Hero fields live in page frontmatter:

```yaml
title: Page Title       # antique gold h1
eyebrow: Education      # antique gold all-caps label
description: One line.  # soft-white paragraph
```

---

## Cards

- Card backgrounds: **always soft-white** (`#F9F9F9`) — use `card_color: soft-white`
- Card titles: **always forest-green** — enforced by CSS
- Card body text: charcoal
- This applies even when cards are inside a dark section (`sage-green` or `forest-green`) — the CSS handles it correctly when `card_color: soft-white` is set

---

## Buttons

- All buttons and button-style links use the **capsule shape**: `border-radius: 999px` (a fully rounded pill), as used by `.btn`, `.btn-primary`, and `.btn-ghost`.
- Any button-like control must match this — including section CTAs such as the spotlight "Read more" (`.spotlight__cta`). Do **not** introduce square or small-radius buttons, and do not use `var(--radius)` for a button corner.

---

## Sections system

All layout is controlled through `sections:` YAML. The seven layout types are:

1. **Plain text** — `content: |`
2. **Two columns** — `columns:` list with two `content:` blocks
3. **Cards** — `cards:` list; control columns with `card_columns: 2` or `3`
4. **Image + text** — `image:` with `src:`, `alt:`, `position: left|right` plus `content:`
5. **Stats banner** — `stats:` list; best on `forest-green`
6. **HTML include** — `include: filename.html`; pass data via custom YAML keys
7. **Spotlight** — `spotlight:` list of topics; tabbed feature band, best on `forest-green`. Note: `eyebrow`/`title`/`intro` render inside the left column, not across the top

Each section may also have `eyebrow:`, `title:`, and `intro:` header fields.

---

## CSS rules

- **Always use the existing token variables** — never add raw hex colours to CSS
- **Never use inline `style=` attributes** for colours — add a scoped CSS class instead
- **Never change** `.page-hero`, `.page-section--*` base colour rules, or `:root` token values without explicit instruction
- **Specificity pattern for overrides:** scope to the most specific context (e.g. `.page-section--sage-green .page-section__cards--soft-white .page-section__card-title`)

---

## Layouts

- `layout: sectioned-page` — standard interior pages (hero + sections)
- `layout: home` — home page (hero video, stats strip, milestone timeline)
- `layout: people` — People page (custom two-column hero with radial viz)
- `layout: news-events` — News & Events page (post feed + FullCalendar)
- `layout: post` — individual news posts in `_posts/news/`
- `layout: learning-resources` — Learning Resources page
- `layout: publications` — publications listing
- `layout: page` — simple generic page
- `layout: bare` — strips all site chrome (nav, hero, footer); only for KU Code Club
- `layout: default` — base layout; rarely used directly

---

## File structure

```
markdown/          # all editable page content
  about/           # About CPDSE, People, Fellow Program, Visual Identity
  education/       # Curriculum Development, Learning Resources, Code Clubs (hub, SDU, KU)
  news/            # News & Events page
  research/        # Researchers & Units
  contact/
  home/
  other/           # Funding, Privacy (not in nav)
_posts/news/       # individual news posts (YYYY-MM-DD-slug.md)
_data/             # milestones.yml, convergence_talks.yml, learning_resources.json
assets/
  css/
    main.css           # global styles — edit with care
    page-sections.css  # sections system styles
    people.css         # people page only
    research-units.css # research units page only
    (plus per-page styles: about, convtalks, educational-offerings,
     learning-resources, publications, visual-identity, fullcalendar.min)
  fonts/             # self-hosted webfonts (GDPR) — never load fonts from a CDN
  js/
    vendor/          # self-hosted JS libraries (GDPR) — never load scripts from a CDN
  data/
    people.json        # people page data
    publications.json  # publications data
    events-calendar.ics  # auto-updated by GitHub Action — do not edit by hand
  images/            # site images
scripts/             # data-refresh scripts (not published to the site)
_includes/           # HTML partials — edit only when the MD system cannot do the job
_layouts/            # page layout templates — rarely need editing
```

---

## What not to do

- Do not add new colour values, fonts, or spacing tokens
- Do not change permalink values without updating `_config.yml` nav URLs
- Do not edit `_layouts/default.html`, `_layouts/sectioned-page.html`, or `_includes/nav.html` for content changes — use the MD files
- Do not use `layout: bare` on any page except KU Code Club
- Do not load fonts, scripts, or other assets from external CDNs (Google Fonts, jsDelivr, …) — self-host them under `assets/fonts/` or `assets/js/vendor/` instead; third-party requests leak visitor IPs and break GDPR compliance
- Do not commit `.env` files, credentials, or large binaries
- Do not push directly to `main` without checking the build passes on GitHub Pages
