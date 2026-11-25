# Design Kit Integration — Ready to Push

## Status: ✅ Complete

You have successfully integrated the design-kit files in a **minimal, removable, non-breaking** way.

---

## What you have

### Production files (commit these):
- `DESIGN_PRINCIPLES.md` — Universal design philosophy
- `AGENTS.md` — AI agent instructions (references CLAUDE.md)
- `.github/pull_request_template.md` — PR form with design checklist

### Reference documents (optional; can be deleted later):
- `DESIGN_KIT_INTEGRATION_ANALYSIS.md` — Detailed analysis
- `DESIGN_KIT_INTEGRATION_NOTES.md` — Integration overview
- `INTEGRATION_READY.md` — This file
- `QUICK_REFERENCE.md` — Quick reference card

---

## How to commit

```bash
cd "C:\Users\mittenentzwei\OneDrive - Syddansk Universitet\GitHub\PagesCMS"

# Check status
git status

# Stage the three production files
git add DESIGN_PRINCIPLES.md AGENTS.md .github/pull_request_template.md

# (Optional) Also add reference docs if you want to keep them in the repo
# git add DESIGN_KIT_INTEGRATION_ANALYSIS.md DESIGN_KIT_INTEGRATION_NOTES.md QUICK_REFERENCE.md

# Commit
git commit -m "Add design governance layer: DESIGN_PRINCIPLES, AGENTS, PR template

- DESIGN_PRINCIPLES.md: Universal design philosophy (simplicity, consistency, hierarchy, etc.)
- AGENTS.md: AI agent instructions referencing CLAUDE.md for site-specific rules
- .github/pull_request_template.md: PR form with design decisions checklist

These complement CLAUDE.md (not a replacement) and are fully removable.
They improve PR hygiene and make design decisions explicit.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# Push
git push
```

---

## What happens after you push

1. **On GitHub:** Next PR will show your new PR template
2. **In VS Code:** Copilot will read AGENTS.md alongside CLAUDE.md
3. **For reviewers:** DESIGN_PRINCIPLES.md becomes the shared standard

---

## If it's not working

Completely revert with:

```bash
git rm DESIGN_PRINCIPLES.md AGENTS.md .github/pull_request_template.md
git commit -m "Remove design governance files"
git push
```

**Everything goes back to 100% normal.** No side effects, no cleanup needed.

---

## If you want to add GitHub Actions CI later

The design-kit includes a workflow for automated Claude PR reviews. To enable:

1. Copy `design-kit/.github/workflows/design-review.yml` to `.github/workflows/`
2. Add `ANTHROPIC_API_KEY` secret to GitHub (Settings > Secrets and variables > Actions)
3. Optionally configure branch protection to require the check

This is **entirely optional** and can wait until you know the template approach is working.

---

## Files to keep vs delete

### Essential (commit):
- ✅ DESIGN_PRINCIPLES.md
- ✅ AGENTS.md
- ✅ .github/pull_request_template.md

### Documentation (optional; can delete later):
- 📄 DESIGN_KIT_INTEGRATION_ANALYSIS.md
- 📄 DESIGN_KIT_INTEGRATION_NOTES.md
- 📄 QUICK_REFERENCE.md
- 📄 INTEGRATION_READY.md (this file)

---

## Ready? 

```bash
git add DESIGN_PRINCIPLES.md AGENTS.md .github/pull_request_template.md
git commit -m "Add design governance layer"
git push
```

That's it. You're done! 🎉
