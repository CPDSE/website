# Quick Reference Card

## Three files ready to commit

### 1. DESIGN_PRINCIPLES.md
**Purpose:** Shared design philosophy  
**Readers:** AI agents + human reviewers  
**Key content:** Simplicity, consistency, hierarchy, complexity budget, red flags  
**When you need it:** Reviewing PRs, training new contributors  

### 2. AGENTS.md
**Purpose:** Tell AI agents (Claude, Copilot, Cursor) how to work  
**Readers:** AI agents (Copilot in VS Code, Claude Code, etc.)  
**Key content:** Pre-work checklist, hard rules, pre-finish checklist  
**When you need it:** Applies automatically when AI agents read the repo  

### 3. .github/pull_request_template.md
**Purpose:** Guide PR authors to fill in design decisions  
**Readers:** PR authors (humans)  
**Key content:** Design decisions form, screenshots, checklist  
**When you need it:** Appears in every new PR  

---

## How they work together

```
AI agent (Claude in VS Code)
  ├─ reads CLAUDE.md (site-specific rules: colors, buttons, sections)
  ├─ reads DESIGN_PRINCIPLES.md (philosophy: why simplicity matters)
  ├─ reads AGENTS.md (this is what I should do)
  └─ makes informed changes with design accountability

PR author (human)
  ├─ template appears (reminds them of requirements)
  ├─ reads CLAUDE.md (site-specific rules)
  ├─ reads DESIGN_PRINCIPLES.md (philosophy)
  ├─ fills in design decisions form
  ├─ attaches screenshots
  └─ checks the checklist boxes

Reviewer (human)
  ├─ looks at the form + screenshots + diff
  ├─ checks CLAUDE.md for site-specific violations
  ├─ checks DESIGN_PRINCIPLES.md for philosophical ones
  ├─ approves or requests changes
  └─ design decisions are now documented for future reference
```

---

## To commit

```bash
git add DESIGN_PRINCIPLES.md AGENTS.md .github/pull_request_template.md
git commit -m "Add design governance layer from design-kit template"
git push
```

## To remove (if it doesn't work)

```bash
git rm DESIGN_PRINCIPLES.md AGENTS.md .github/pull_request_template.md
git commit -m "Remove design governance files"
git push
```

---

## Key differences from design-kit

| Part of design-kit | Used? | Why |
|---|---|---|
| `.github/workflows/design-review.yml` | ❌ No | GitHub Actions CI is optional and can be added later |
| `.github/pull_request_template.md` | ✅ Yes | PR hygiene matters |
| `AGENTS.md` | ✅ Yes (edited) | Customized to reference your CLAUDE.md |
| `DESIGN_PRINCIPLES.md` | ✅ Yes | Generic philosophy is valuable |
| `CLAUDE.md` from design-kit | ❌ No | Your CLAUDE.md is better (CPDSE-specific) |
| `README.md` from design-kit | ℹ️ Reference only | Setup instructions you already have |

---

## Nothing changed

✅ CLAUDE.md — untouched  
✅ Existing markdown files — untouched  
✅ Layouts, CSS, assets — untouched  
✅ Workflows in .github/workflows/ — untouched  
✅ Configuration files — untouched  

Only **three new files** added. Fully removable. Zero side effects.

