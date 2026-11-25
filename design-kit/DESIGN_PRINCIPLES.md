# Design Principles

Every page and component on this website must follow these principles.
They apply to humans and to AI agents. If a change breaks one, either fix the change
or explain in the PR why the principle doesn't apply. "The AI made it" is not a reason.

## The core rule: restraint

**Every page has ONE purpose and ONE primary action.**
If you can't state both in one sentence each, the page isn't ready.
When in doubt, remove something. A good change often deletes more than it adds.

---

## 1. Simplicity

A visitor should know within 5 seconds where they are and what to do next.

- The headline says what the page is for, in plain words.
- One primary button per view. Secondary actions look visibly less important.
- Every element has a job. If you can't name it, delete it.
- Prefer whitespace over boxes, dividers, badges and decoration.
- No card-inside-card, no more than one level of visual nesting.
- No animation unless it explains something. Never autoplay, never looping.
- Don't ask the visitor to make more than 2-3 choices at once.

## 2. Consistency

The site must look like one product, not a patchwork.

- **Reuse before you create.** Use existing components, layouts and tokens first.
  Only add a new one if nothing existing fits, and say why in the PR.
- Colors, fonts, spacing, radii and shadows come from the design tokens (see `AGENTS.md`).
  No hard-coded hex values, no ad-hoc pixel values, no new fonts.
- Same header, footer and navigation on every page, in the same place.
- Same button looks and behaves the same everywhere.
- Same tone in copy: same voice, same capitalization style, same terminology.

## 3. Navigation is a conversation

- Labels are literal and say what the visitor gets: "Pricing", "How it works",
  "Book a demo". Avoid vague words like "Solutions", "Discover", "Explore", "Resources".
- Every page is reachable from the navigation. No orphan pages.
- The visitor can always tell where they are (active state, page title, breadcrumbs when deep).
- The link text says where it goes. Never "click here" or "read more" alone.
- Keep top-level navigation short (max ~6 items).

## 4. Hierarchy

- One H1 per page. Headings go in order (H1, H2, H3), no skipping for looks.
- Size, weight and color show importance. If everything is bold, nothing is.
- Max 2 font weights and the existing type scale in use per page.
- Text blocks are short. Paragraphs of 2-4 lines. Use real lists for lists.

## 5. Content and copy

- Write like a person. No filler ("Unlock the power of...", "Seamlessly...", "Elevate your...").
- No emoji as decoration or as icons. Use the site's icon set.
- No invented numbers, testimonials, logos, or claims. Placeholder content never ships.
- No lorem ipsum, no "Feature 1 / Feature 2".

## 6. Works for everyone, everywhere

- **Mobile first.** Check it at ~375px wide and at desktop width. No horizontal scroll.
- Text contrast meets WCAG AA (4.5:1 body, 3:1 large text).
- Real HTML semantics: `button` for actions, `a` for links, landmarks (`header`, `nav`, `main`, `footer`).
- All images have meaningful `alt` (or empty `alt` if decorative).
- Everything works with keyboard only, with a visible focus state.
- Design the empty, loading and error states, not just the happy path.

## 7. Lightweight

- No new dependencies, frameworks, or CDN scripts without discussion.
- No huge inline `<style>` or `<script>` blobs. Styles go in the shared stylesheet, behavior in small modules.
- Optimize images (right size, modern format, lazy-load below the fold).
- A page that needs a lot of JavaScript to show text is a bug.

## 8. Iterated, not generated

A first AI draft is a draft. Before opening a PR:

- You have looked at the page yourself on mobile and desktop.
- You have removed at least one thing from the first draft.
- You have compared it side by side with an existing page and it matches.
- You attached screenshots (mobile + desktop) to the PR.

### Typical AI-slop tells (reviewers and agents: flag these)

- Purple/blue gradients, glassmorphism, glowing shadows, neon accents
- Emoji bullets and emoji headings
- Hero + 3 feature cards + stats row + testimonial + CTA banner, on every page
- Cards in cards, borders around everything, five different border radii
- Stats and claims that nobody can source
- Many different colors or font sizes on one page
- Hover/scroll animations on everything
- Single-file pages with hundreds of lines of inline CSS/JS
- Pages that duplicate existing ones with slightly different styling

---

## Complexity budget (per page)

| Thing | Limit |
|---|---|
| Primary buttons per view | 1 |
| Sections on a page | 5 (more needs a reason in the PR) |
| Accent colors | 1 (from tokens) |
| Font families | the site's existing ones only |
| New components | 0 by default |
| New dependencies | 0 by default |
| Inline `<style>`/`<script>` | none |

Going over a limit is allowed only with a written reason in the PR.
