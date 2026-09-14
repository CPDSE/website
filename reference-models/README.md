# reference-models/ — generated site

An onboarding guide and explorer for CPDSE's three reference models (Pharma
Value Chain, PDS Competence Model, Pedagogic Practices), written for
CPDSE-teachers. It is served at `/reference-models/`. It is **intentionally not in
the site navigation** and every page asks search engines not to index it.

**Everything in this folder except `_src/` and this README is generated.** Do not
edit generated files by hand: the next build overwrites them.

## Build

The build reads a local checkout of the private
[`CPDSE/cpdse-reference-models`](https://github.com/CPDSE/cpdse-reference-models)
repo. By default it expects that checkout next to this repo
(`../cpdse-reference-models`).

```bash
python3 scripts/build_onboarding.py            # writes only files that changed
python3 scripts/build_onboarding.py --check    # fails if the output is stale or broken; writes nothing
python3 -m unittest discover -s scripts/onboarding_lib/tests -t scripts
```

Options: `--models PATH` (or `CPDSE_REFERENCE_MODELS=PATH`), `--allow-dirty` to
preview uncommitted model changes, `--examples FILE` to try another examples file.

GitHub Pages builds this repo straight from `main` with no CI, so **commit the
generated output** together with the change that caused it. Run `--check`
before committing.

Requirements: Python 3.9+ standard library only. Jekyll copies the pages
verbatim because they start with `<!doctype html>`, not front matter; folders
starting with `_` (like `_src/`) are not published.

## What you can edit

| File | What it controls |
|---|---|
| `_src/narrative/*.html` | The Start page sections, in the order listed in `site.json` |
| `_src/pages/*.html` | Intros for the overview pages, the worksheet and About |
| `_src/site.json` | Start page sections, the "take one away" panels, glossary, allowed external links |
| `_src/examples.json` | The worked examples (see below) |
| `_src/tokens.json` | Colour tokens for light and dark themes, with contrast pairs checked at build |
| `_src/css/site.css`, `_src/js/site.js` | Styles and the progressive-enhancement script |
| `_src/fonts/`, `_src/icons/` | Self-hosted Source Serif 4 / Source Sans 3 (OFL) and brand icons |

Hand-written HTML supports two kinds of placeholder:

- `$n_substeps`, `$n_competencies`, `$vc_version` and other counts
  (see `scripts/onboarding_lib/render/copy.py`). Write `$$` for a literal dollar sign.
- Shortcodes that become checked links:
  `[[stage:lead-identification]]`, `[[sub:statistics]]`,
  `[[comp:statistics/hypothesis-testing]]`, `[[level:3]]`,
  `[[c4:concrete-practice]]`, `[[trump:talking-trumps-listening]]`,
  `[[ex:fa516]]`, `[[model:where|label]]`, `[[page:tools/|label]]`.
  An unknown reference fails the build.

## Adding or changing an example

Examples reference the models by id, so the build catches renames. In
`_src/examples.json`:

- `anchor.stages` uses ids from `vocab/stages.csv` (the first is where the example
  sits on the map).
- Each target names a sub-area id from `vocab/subareas.csv` and the **exact**
  competency name within it. `today` and `target` are levels 1–5, and neither may be
  a level marked as not applicable.
- `design.blocks` use 4C ids (`connections`, `concepts`, `concrete-practice`,
  `conclusions`) and Trump ids (such as `talking-trumps-listening`).
- `illustrative` must include `targets` and `design`. Levels and designs are
  examples, never assessments of real people.

## Rules this site keeps

- Say **CPDSE-teacher**, never "consultant" (the build fails on the word).
- The value chain and the competence model are connected only through the tool
  crosswalk ("tool-based link") and the examples. There is no substep-to-competency
  map, and the site must not imply one.
- No fonts, scripts or other assets from CDNs (GDPR). External links are allowed
  only to hosts listed in `site.json`.
- Draft models (marked "AI-drafted, pending review" in their source) show a draft badge.

## Known issues

- `vocab/stages.csv` in the models repo has an unquoted comma in an alias
  (`Preclinical (DMPK, tox)`). The build reads it correctly and prints a warning;
  it should be fixed upstream.
- One pharma-example tag in the competence model is truncated
  ("Design of experiments (DOE)..."); the build matches it by prefix.
- `competency-model/Level_Rubric.md` (upstream) calls L3 "the reference line on
  the radar", a chart this site does not have, and uses the phrase "Detect
  bullshit" at L4. Both are shown as written; raise them with the model owner.
- The value-chain and pedagogy source headers say "pending MO review"; the site
  shows this as "pending CPDSE review".
