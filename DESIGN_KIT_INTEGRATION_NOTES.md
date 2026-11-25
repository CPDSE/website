# Design Kit Integration — Summary

**Date integrated:** 2026-11-25  
**Version:** From `design-kit/` folder (GitHub template)  
**Integration scope:** Minimal, fully removable

---

## What was added

Three new files at the repo root and in `.github/`:

| File | Purpose | From design-kit |
|---|---|---|
| `DESIGN_PRINCIPLES.md` | Public design philosophy (simplicity, consistency, hierarchy, etc.) | `design-kit/DESIGN_PRINCIPLES.md` |
| `AGENTS.md` | AI agent instructions; references `CLAUDE.md` for site-specific rules | `design-kit/AGENTS.md` (edited) |
| `.github/pull_request_template.md` | PR form; guides authors to fill in design decisions and checklist | `design-kit/.github/pull_request_template.md` |

---

## Key design decisions

### Why `DESIGN_PRINCIPLES.md` is separate from `CLAUDE.md`

- **`CLAUDE.md`** = CPDSE-specific implementation rules (4 color pairings, capsule buttons, sections system, file structure)
- **`DESIGN_PRINCIPLES.md`** = Universal design philosophy (why simplicity matters, what consistency means, typical red flags)
- Both are read by AI agents; `CLAUDE.md` overrides when there's conflict
- Humans can read the philosophy without getting bogged down in CPDSE-specific mechanics

### Why no GitHub Actions workflow

The design-kit included a `.github/workflows/design-review.yml` file for automated Claude PR reviews. We skipped it because:
- It requires `ANTHROPIC_API_KEY` secret setup (additional GitHub config)
- It adds CI complexity that may not be needed right now
- If you want it later, it can be added easily (just copy the workflow file and add the secret)
- For now, the PR template + human review is sufficient

### How these files work together

```
PR author opens a PR
        ↓
.github/pull_request_template.md appears (reminds them to fill in design decisions & check the boxes)
        ↓
They read CLAUDE.md (site-specific rules: colors, buttons, sections system)
        ↓
They read DESIGN_PRINCIPLES.md (philosophy: simplicity, consistency, etc.)
        ↓
They fill in the form, attach screenshots, check the boxes
        ↓
Reviewer looks at the form + their screenshots + the diff
        ↓
Reviewer uses DESIGN_PRINCIPLES.md + CLAUDE.md to evaluate
        ↓
(If you add GitHub Actions later, Claude would review here automatically before human review)
```

---

## How to remove it (if it doesn't work out)

To completely revert the design-kit integration, delete these files:

```bash
rm DESIGN_PRINCIPLES.md
rm AGENTS.md
rm .github/pull_request_template.md
```

Then undo the git commit. Everything else stays the same:
- `CLAUDE.md` remains unchanged
- Existing workflows remain unchanged
- Repository structure unchanged

---

## How to use it

### For PR authors:

When you open a PR (or update one), the template will appear automatically with these sections:

1. **What and why** — brief description of the change
2. **Design decisions** (required):
   - Purpose of the change (one sentence)
   - The one primary action
   - Existing components/tokens reused
   - Anything new and why nothing existing fit
   - What you removed from the first draft
3. **Screenshots** — mobile + desktop
4. **Checklist** — did you read the rules? mobile/desktop checked? only tokens used? etc.

Fill these in honestly. The checklist is especially important; it catches issues before review.

### For reviewers:

Use this order when reviewing:

1. **Did they read and follow the checklist?** (quick win)
2. **Did they fill in design decisions honestly?** (shows they thought it through)
3. **Check against `CLAUDE.md`** — site-specific rules (colors, buttons, sections, files)
4. **Check against `DESIGN_PRINCIPLES.md`** — universal principles (simplicity, consistency, etc.)
5. **Look at their screenshots** — does it match existing pages?
6. **If it fails a hard rule, ask them to fix it.** If it exceeds the complexity budget, ask why.

---

## If you want to add GitHub Actions CI later

The design-kit includes a workflow template. To add it:

1. Copy `.github/workflows/design-review.yml` from the `design-kit/` folder to your repo
2. Go to Settings > Secrets and variables > Actions
3. Add a new secret: `ANTHROPIC_API_KEY` = (your Anthropic API key)
4. Optionally configure branch protection to require the "Design review" check to pass
5. Next PR will get an automated Claude review before human review

This is totally optional and can wait until you know the template approach is working.

---

## Files unchanged

Everything else in the repository stays exactly as it was:

- ✅ `CLAUDE.md` — untouched (this is your source of truth)
- ✅ All markdown files, layouts, CSS, assets — untouched
- ✅ Existing workflows in `.github/workflows/` — untouched
- ✅ Configuration (`_config.yml`, Gemfile, etc.) — untouched

The integration is purely additive and removable.

---

## Next steps

1. **Review and commit** these new files:
   ```bash
   git add DESIGN_PRINCIPLES.md AGENTS.md .github/pull_request_template.md
   git commit -m "Add design governance files from design-kit template"
   ```

2. **Try it out** — make a test PR or use it on the next one

3. **Adjust if needed** — if the template feels too verbose, simplify it. If the principles feel off, adjust them.

4. **If it's not working:** delete the three files and revert the commit. Zero side effects.

