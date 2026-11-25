# Design Kit Integration — Ready to Commit

✅ **Status:** Complete and ready. All new files are separate, removable, and non-breaking.

---

## What was integrated

Three governance files layered on top of your existing `CLAUDE.md`:

### 1. **DESIGN_PRINCIPLES.md** (5KB)
Universal design philosophy covering:
- Simplicity, consistency, navigation, hierarchy
- Content & copy standards
- Accessibility & mobile-first approach
- Complexity budget (1 button, 5 sections, 1 accent color, 0 new components, 0 new dependencies per page)
- Red flags ("AI-slop tells") to watch for

**Why separate:** This is the "why" — philosophy that applies to any website. Your CLAUDE.md is the "how" — CPDSE-specific rules. Both are read by AI agents; they complement each other.

### 2. **AGENTS.md** (3.5KB)
Instructions for AI coding agents (Claude, Cursor, Copilot, Codex). Contains:
- Pre-work checklist (look at existing pages, state purpose & primary action)
- Hard rules (use tokens, no new fonts/dependencies, no emoji, no inline styles)
- Pre-finish checklist (mobile checked? only tokens used? copy is plain?)
- **Explicitly references CLAUDE.md** for site-specific rules

**Why this version:** Edited from the design-kit template to reference your CLAUDE.md instead of generic TODOs. Points to your actual token file and sections system.

### 3. **.github/pull_request_template.md** (1KB)
PR form that appears when opening a PR. Includes:
- Design decisions section (purpose, primary action, components reused, what was removed)
- Required screenshots (mobile + desktop)
- Checklist (did you read the rules? mobile/desktop checked? only tokens used?)

**Why this version:** Edited to reference both CLAUDE.md and DESIGN_PRINCIPLES.md in the checklist.

---

## How it works

```
You open a PR
  ↓
PR template appears (reminds you of requirements)
  ↓
You read CLAUDE.md (site-specific: colors, buttons, sections) + DESIGN_PRINCIPLES.md (philosophy)
  ↓
You fill in the design decisions form + screenshots + checklist
  ↓
Reviewer uses CLAUDE.md + DESIGN_PRINCIPLES.md to evaluate your work
  ↓
Deploy or request changes
```

No GitHub Actions CI yet. Just better PR hygiene and visibility into design decisions.

---

## How to remove it (if needed)

To completely revert:

```bash
git rm DESIGN_PRINCIPLES.md AGENTS.md .github/pull_request_template.md
git rm DESIGN_KIT_INTEGRATION_ANALYSIS.md DESIGN_KIT_INTEGRATION_NOTES.md  # (optional cleanup)
git commit -m "Remove design kit integration files"
git push
```

That's it. Everything else stays the same:
- `CLAUDE.md` remains untouched
- Existing workflows remain untouched
- No configuration changes
- No breaking changes

---

## Next steps

### To commit the integration:

```bash
git add DESIGN_PRINCIPLES.md AGENTS.md .github/pull_request_template.md
git commit -m "Add design governance layer: DESIGN_PRINCIPLES, AGENTS, PR template

- DESIGN_PRINCIPLES.md: universal design philosophy (simplicity, consistency, etc.)
- AGENTS.md: AI agent instructions referencing CLAUDE.md for site-specific rules
- .github/pull_request_template.md: PR form with design decisions checklist

These files are complementary to CLAUDE.md (not a replacement) and fully removable.
They improve PR hygiene and make design decisions explicit without CI automation.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
git push
```

### To test it:

1. **Make a test PR** (or use an upcoming one) and see the template appear
2. **Have reviewers reference DESIGN_PRINCIPLES.md** when evaluating PRs
3. **Track whether the template helps** (better PR descriptions? fewer design revisions?)
4. **Adjust or remove if it feels heavy** — total removal takes 10 seconds

### If you want GitHub Actions later:

The design-kit includes a workflow for automated Claude PR reviews. To add it:
1. Copy `design-kit/.github/workflows/design-review.yml` to `.github/workflows/`
2. Add `ANTHROPIC_API_KEY` secret to GitHub (Settings > Secrets and variables > Actions)
3. Optionally configure branch protection to require the check

This is optional and can wait until you know the template is working.

---

## Files added (what git status will show)

```
?? .github/pull_request_template.md        ← PR template (design governance)
?? AGENTS.md                               ← AI agent instructions (design governance)
?? DESIGN_PRINCIPLES.md                    ← Universal principles (design governance)
?? DESIGN_KIT_INTEGRATION_ANALYSIS.md      ← Analysis document (for reference, can delete)
?? DESIGN_KIT_INTEGRATION_NOTES.md         ← Integration notes (for reference, can delete)
```

The first three are the actual integration. The last two are documentation you created for understanding.

---

## Key principles of this integration

✅ **Minimal:** Only 3 essential files (+ 2 reference docs)  
✅ **Non-breaking:** No changes to existing files  
✅ **Removable:** Delete 3 files and revert; zero side effects  
✅ **Complementary:** Layers on top of CLAUDE.md, doesn't replace it  
✅ **Clear:** Separates philosophy (DESIGN_PRINCIPLES) from mechanics (CLAUDE)  
✅ **Practical:** Better PR descriptions, clearer design decisions  
✅ **Scalable:** Can add GitHub Actions CI later if the template works  

---

## Ready? 

```bash
git add DESIGN_PRINCIPLES.md AGENTS.md .github/pull_request_template.md
git commit -m "Add design governance files from design-kit template"
git push
```

That's it. Try it on the next PR and see if it helps.
