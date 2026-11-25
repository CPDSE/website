# Design Kit Integration Analysis

## Summary

The `design-kit/` folder contains **reusable governance and enforcement patterns** (a template) that can optionally be integrated into your CPDSE website repository. It is **NOT incompatible** with your existing `CLAUDE.md` — they are **complementary** and designed to work together.

---

## What's in design-kit/

### 1. **DESIGN_PRINCIPLES.md** (Generic template)
A philosophy-driven governance document covering:
- **Simplicity** — one purpose, one primary action per page
- **Consistency** — reuse existing components, use tokens only
- **Navigation** — literal labels, no "Discover" / "Explore" vagueness
- **Hierarchy** — one H1, ordered headings, one primary button per view
- **Content & copy** — write like a person, no filler ("Unlock the power of...")
- **Accessibility/mobile** — WCAG AA, keyboard-only, 375px layout
- **Lightweight** — no new dependencies or bloated JavaScript
- **Iterated, not generated** — AI output must be reviewed and edited, not shipped raw

**Complexity budget table** (per page):
| Thing | Limit |
|---|---|
| Primary buttons per view | 1 |
| Sections per page | 5 |
| Accent colors | 1 (from tokens) |
| Font families | site's existing only |
| New components | 0 by default |
| New dependencies | 0 by default |
| Inline `<style>`/`<script>` | none |

### 2. **AGENTS.md** (Generic template with TODOs)
Instructions for AI coding agents (Claude, Cursor, Copilot, Codex). Contains:
- Pre-checks before writing (look at 2-3 existing pages, state purpose & primary action)
- **Hard rules** (use tokens, no new fonts/dependencies, no emoji, no placeholder text, semantic HTML)
- **Default to less** (delete before adding, don't pad pages with feature grids)
- Pre-finish checklist (mobile/desktop checked, only tokens used, copy is plain)
- Requirement for a **"Design decisions" note** in PRs (purpose, action, what was reused, deviations & why)

### 3. **.github/workflows/design-review.yml** (CI automation)
A GitHub Actions workflow that:
- Runs on every PR (`opened`, `synchronize`, `reopened`)
- Uses `anthropics/claude-code-action@v1` to invoke Claude via API
- Reads `DESIGN_PRINCIPLES.md` and `AGENTS.md`
- Reviews the PR diff using `gh pr diff`, compares with existing pages
- Posts a one-comment review with verdict: **PASS | NEEDS CHANGES | SIMPLIFY FIRST**
- Checks for 9 specific things (simplicity, consistency, nav, hierarchy, content, a11y, complexity budget, AI-slop tells, honest PR description)

**Setup required:**
1. Add `ANTHROPIC_API_KEY` to repo secrets (Actions section)
2. Configure branch protection on `main` to require this check (optional but recommended)
3. Add `CODEOWNERS` file if you want specific reviewers on design-critical files (optional)

### 4. **.github/pull_request_template.md** (PR form)
Guides authors to fill in:
- **What and why** (one or two sentences)
- **Design decisions** (required):
  - Purpose of change (one sentence)
  - The one primary action
  - Existing components/tokens reused
  - Anything new and why nothing existing fit
  - What was removed from first draft
- **Screenshots** (mobile 375px + desktop)
- **Checklist** (did you read DESIGN_PRINCIPLES.md? Did you check mobile/desktop yourself? Only tokens used? Etc.)

---

## Comparison: Your CLAUDE.md vs. design-kit AGENTS.md + DESIGN_PRINCIPLES.md

| Aspect | Your CLAUDE.md | design-kit | Overlap / Difference |
|---|---|---|---|
| **Primary enforcement** | Custom rules for CPDSE site | Generic principles for any site | 🟡 High overlap — yours is a *specialization* of the generic |
| **Colour system** | 4 specific CPDSE pairings (soft-white, mint-gray, sage-green, forest-green) with hex codes | Generic rule: "use tokens only, no hard-coded colors" | 🟡 Yours is MORE specific; design-kit is a template |
| **Token variables** | Lists 9 CSS custom properties (--color-*, --accent, etc.) | Refers to "design tokens" but doesn't list yours | 🟡 design-kit assumes you have them; yours defines them |
| **Buttons** | Capsule shape (`border-radius: 999px`) enforced | Generic rule: "one primary button per view, same button looks same everywhere" | 🟡 Yours specifies the shape; design-kit just says consistency |
| **Sections system** | Defines 7 layout types (plain, columns, cards, image+text, stats, include, spotlight) | No mention of your sections system | ❌ No overlap — design-kit is framework-agnostic |
| **Content editing** | "Always use MD files, never hardcode into layouts" | "No placeholder text, write like a person" | 🟡 Yours has workflow rules; design-kit has content rules |
| **Hero (page banner)** | Specific rules: antique gold H1, specific opacity for description | Generic: "H1 should be clear, one purpose" | 🟡 Yours is CPDSE-specific |
| **GitHub Actions CI** | None — no automated design review | `design-review.yml` workflow + PR template | ✅ design-kit adds this; your repo doesn't have it |
| **Complexity budget** | No explicit table | Has a table (1 button, 5 sections, 1 accent color, 0 new components, 0 new dependencies) | ✅ design-kit adds structure; yours assumes common sense |
| **AI-slop tells** | No specific list | Lists 12 red flags (purple gradients, glassmorphism, emoji bullets, hero+3cards+stats pattern, etc.) | ✅ design-kit adds early-warning specifics |
| **Conflict handling** | Detailed: "Stop before changing, tell user the rule, offer alternative, ask for explicit override" | Assumes review happens in PR | 🟡 Yours is for the AI agent to follow; design-kit assumes human reviewers also read it |

---

## Three Options

### **Option 1: Keep CLAUDE.md as-is, ignore design-kit** ✅ Safe, working now
- Your `CLAUDE.md` is already specific, complete, and enforced by prompt injection
- design-kit's governance and CI workflow are **optional extras**
- No integration needed; they don't conflict

### **Option 2: Layer design-kit ON TOP** ✅ Recommended
1. **Keep your CLAUDE.md unchanged** — it's your CPDSE-specific rules
2. **Copy design-kit files into the repo root:**
   - `.github/workflows/design-review.yml`
   - `.github/pull_request_template.md`
   - `DESIGN_PRINCIPLES.md` (new file)
   - `AGENTS.md` (edit to point to your CLAUDE.md, tokens, components)
3. **Edit AGENTS.md** to replace its TODO comments with:
   - Point to your `CLAUDE.md` (already the source of truth)
   - Point to your token variables in `assets/css/main.css`
   - Point to your component/layout includes in `_includes/`
4. **Set up GitHub Actions secrets** and branch protection (5 minutes)
5. **Result:** Every PR gets an automated design review by Claude before human review; PR author checklist ensures they thought through decisions

**Why this works:**
- `CLAUDE.md` stays your internal north star (what the AI *must* do)
- `DESIGN_PRINCIPLES.md` is public philosophy (what the site values)
- `AGENTS.md` glues them together for future AI agents
- GitHub Actions makes design review automatic, consistent, and **documentable**

### **Option 3: Merge CLAUDE.md and DESIGN_PRINCIPLES.md** ⚠️ Works but loses clarity
- Combine your CPDSE-specific rules + generic principles into one file
- Easier for humans to read in one place
- Loses the distinction between "this site's rules" (CLAUDE.md) and "this site's principles" (DESIGN_PRINCIPLES.md)
- Not recommended — separating them is clearer for future contributors

---

## My Recommendation: **Option 2**

**Why:**
1. **No breaking changes** to your current setup
2. **Adds CI automation** that catches design drift automatically (huge win for a site run by multiple people or future contributors)
3. **Makes governance visible** — everyone can read DESIGN_PRINCIPLES.md and know the bar
4. **Lowers human reviewer load** — Claude flags obvious issues first; human reviewers focus on intent and edge cases
5. **Scales for contributor onboarding** — new people see the PR template + AI feedback before a human even looks

**Work required:**
- Copy 4 files from `design-kit/` into repo root (`.github/workflows/`, `.github/pull_request_template.md`, `DESIGN_PRINCIPLES.md`)
- Edit `AGENTS.md` (replace 2-3 TODO comments with real paths to your tokens/components)
- Add `ANTHROPIC_API_KEY` to repo secrets (1 GitHub setting)
- Optionally add `CODEOWNERS` for design-critical files

**Time:** ~15 minutes setup, then automatic forever.

---

## If You Choose Option 2: Step-by-Step

1. **Copy files:**
   ```bash
   cp design-kit/.github/workflows/design-review.yml .github/workflows/
   cp design-kit/.github/pull_request_template.md .github/
   cp design-kit/DESIGN_PRINCIPLES.md .
   cp design-kit/AGENTS.md .
   ```

2. **Edit AGENTS.md** — replace the TODO section (~line 10) with:
   ```markdown
   <!-- TODO: point to your real files, e.g. -->
   - Design tokens: `assets/css/main.css` (--color-*, --accent, etc.)
   - Layout system: `_includes/page-section.html` (sections: plain, columns, cards, image+text, stats, include, spotlight)
   - Components: `_includes/` (nav.html, footer.html, etc.)
   - Site rules: `CLAUDE.md` (read this first for CPDSE-specific overrides)
   ```

3. **Edit .github/workflows/design-review.yml** — replace the prompt's TODO section with:
   ```markdown
   Also read CLAUDE.md for site-specific rules (color pairings, button shapes, sections system, etc.)
   These override DESIGN_PRINCIPLES.md for this site.
   ```

4. **GitHub setup:**
   - Settings > Secrets and variables > Actions > New repository secret
   - Name: `ANTHROPIC_API_KEY`, Value: (your Anthropic API key)
   - Settings > Branches > Add branch protection rule for `main`
   - Require a pull request before merging
   - Optionally require the "Design review" check

5. **Commit and test:**
   ```bash
   git add DESIGN_PRINCIPLES.md AGENTS.md .github/
   git commit -m "Add design governance & CI review"
   git push
   ```
   Make a test PR to see the workflow run and Claude's first review.

---

## FAQ

**Q: Will this break my existing workflow?**
A: No. Your `CLAUDE.md` remains the source of truth for Copilot in VS Code. The GitHub Actions workflow just adds an *additional* review step in PRs.

**Q: Do I have to use the GitHub Actions workflow?**
A: No. Option 1 (do nothing) works fine. But it's a quick win for consistency.

**Q: What if Claude's review is wrong?**
A: PR author can reply "this is intentional" with a reason. The human reviewer (you) has final say. The workflow is advisory, not a gate (unless you configure branch protection to require it).

**Q: What if I disagree with DESIGN_PRINCIPLES.md?**
A: Keep it as written (generic principles) and use `CLAUDE.md` to override with CPDSE-specific rules. Authors will read both — Claude will check both.

**Q: Will adding DESIGN_PRINCIPLES.md conflict with CLAUDE.md?**
A: No, they complement each other. `CLAUDE.md` is your specialization (this site's rules). `DESIGN_PRINCIPLES.md` is the universal philosophy (why we care about simplicity, consistency, etc.).

---

## Files to integrate

```
design-kit/
├── .github/
│   ├── workflows/
│   │   └── design-review.yml          → copy to .github/workflows/
│   └── pull_request_template.md       → copy to .github/
├── AGENTS.md                           → copy to repo root, edit TODOs
├── DESIGN_PRINCIPLES.md                → copy to repo root (new file)
├── CLAUDE.md                           → DO NOT COPY (you have a better one)
└── README.md                           → reference only
```

**After integration, your repo root will have:**
- `CLAUDE.md` (existing, unchanged)
- `DESIGN_PRINCIPLES.md` (new, from design-kit)
- `AGENTS.md` (new, from design-kit, edited)
- `.github/workflows/design-review.yml` (new, from design-kit)
- `.github/pull_request_template.md` (new, from design-kit)
