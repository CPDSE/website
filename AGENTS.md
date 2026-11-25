# Instructions for AI coding agents

This file is read by Claude Code, Cursor, Copilot, Codex and similar tools.
It applies to every change in this repository.

**Read `CLAUDE.md` first** — it contains CPDSE-specific design rules that override generic principles.
**Then read `DESIGN_PRINCIPLES.md`** — it contains the universal design philosophy.

## Site-specific rules (from CLAUDE.md)

- **Design tokens:** `assets/css/main.css` defines CSS custom properties:
  - Colors: `--color-forest-green`, `--color-soft-white`, `--color-sage-green`, `--color-mint-gray`, `--color-warm-sand`, `--color-antique-gold`, `--color-ivory-gold-tint`, `--color-charcoal`
  - Use these only; never hard-code hex values
- **Colour pairings:** 4 approved background + text combinations (soft-white, mint-gray, sage-green, forest-green)
- **Buttons:** Always use capsule shape (`border-radius: 999px`), never square or small-radius
- **Hero:** H1 must be antique gold (`var(--accent)`), not white
- **Cards:** Always soft-white background, forest-green titles, never nested cards
- **Sections system:** Use YAML frontmatter; supports 7 layout types (plain, columns, cards, image+text, stats, include, spotlight)
- **Content:** Always edit `.md` files in `markdown/` — never hardcode into layouts
- **No new:** fonts, CDN scripts, inline styles, or CSS framework imports

## Before you write anything

1. Look at 2-3 existing pages and the shared components/styles. Match them.
2. State in one sentence each: the page's **purpose** and its **one primary action**.
   If the user's request doesn't make these clear, ask them before building.
3. Check whether an existing component, layout or page already does this. Extend it instead of making a new one.

## Hard rules

- Use the existing design tokens only (colors, spacing, type scale, radii). No hard-coded colors or magic pixel values.
  See `assets/css/main.css` and `CLAUDE.md` for the full token set and colour pairings.
- Do not add new fonts, icon sets, CSS frameworks, animation libraries, or other dependencies.
- No inline `<style>` blocks or large inline `<script>` blocks. Use the shared stylesheet and existing modules.
- No emoji as decoration or icons.
- No placeholder, lorem ipsum, or invented statistics, testimonials or logos.
- Every new page must be linked from the shared navigation and use the shared header and footer.
- Navigation labels are literal ("Pricing", "How it works"), never vague ("Solutions", "Discover").
- One H1 per page, one primary button per view.
- Must work at 375px width, with keyboard only, and meet WCAG AA contrast.

## Default to less

- Prefer deleting and simplifying over adding.
- Don't pad pages with extra sections (feature grids, stat rows, testimonial strips, CTA banners) unless requested.
- If a request would exceed the complexity budget in `DESIGN_PRINCIPLES.md`, say so and propose a simpler version first.

## Before you finish

Run through this and fix problems before reporting done:

- [ ] Does it look like it belongs next to the existing pages?
- [ ] Could anything be removed without losing meaning? Remove it.
- [ ] Mobile (375px) and desktop checked?
- [ ] Only tokens and existing components used?
- [ ] Copy is plain, specific, and free of filler?

In your final message, include a short **Design decisions** note:
purpose, primary action, what existing components you reused, and anything that deviates from the principles and why.
