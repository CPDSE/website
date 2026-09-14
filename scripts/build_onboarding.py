#!/usr/bin/env python3
"""Build the CPDSE Reference Models onboarding site into reference-models/.

Reads a local checkout of the private CPDSE/cpdse-reference-models repo, plus the
hand-written inputs in reference-models/_src/, and writes a static site that
Jekyll copies verbatim. GitHub Pages has no build CI here, so commit the output.

    python3 scripts/build_onboarding.py                # build (writes only changed files)
    python3 scripts/build_onboarding.py --check        # fail if output is stale or broken; writes nothing
    python3 scripts/build_onboarding.py --allow-dirty  # preview with uncommitted model changes

Stdlib only; Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from onboarding_lib import BuildError  # noqa: E402
from onboarding_lib import check, competence, examples, parse_pedagogy, parse_rubric, parse_value_chain, tokens  # noqa: E402
from onboarding_lib.graph import Site  # noqa: E402
from onboarding_lib.render import components as C  # noqa: E402
from onboarding_lib.render import pages_flow as F  # noqa: E402
from onboarding_lib.render import pages_models as M  # noqa: E402
from onboarding_lib.render.layout import shell  # noqa: E402
from onboarding_lib.sources import SOURCE_FILES, provenance, resolve_models_path, run_vocab_validator  # noqa: E402
from onboarding_lib.vocab import OVERFLOW_WARNINGS, Vocab  # noqa: E402

WEBSITE = Path(__file__).resolve().parent.parent
MANIFEST = "build-info.json"
PROTECTED = ("_src/", "README.md")

FONT_FACES = [
    ("Source Sans 3", "normal", "200 900", "source-sans-3-normal"),
    ("Source Sans 3", "italic", "200 900", "source-sans-3-italic"),
    ("Source Serif 4", "normal", "200 900", "source-serif-4-normal"),
]
RANGES = {
    "latin": "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, "
             "U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD",
    "latin-ext": "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, "
                 "U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF",
}


def font_css() -> str:
    out = ["/* Self-hosted typefaces (SIL Open Font License); no third-party requests. */"]
    for family, style, weight, stem in FONT_FACES:
        for subset in ("latin-ext", "latin"):
            out.append(f"@font-face {{ font-family: '{family}'; font-style: {style}; font-weight: {weight}; font-display: swap; "
                       f"src: url(fonts/{stem}-{subset}.woff2) format('woff2'); unicode-range: {RANGES[subset]}; }}")
    return "\n".join(out) + "\n"


def build(models_arg: str | None, out_name: str, examples_arg: str | None, allow_dirty: bool) -> tuple[dict, Site, list]:
    out_dir = WEBSITE / out_name
    src = out_dir / "_src"
    warnings: list[str] = []

    repo = resolve_models_path(models_arg, WEBSITE)
    prov = provenance(repo, allow_dirty)
    run_vocab_validator(repo)
    vocab = Vocab(repo)
    warnings += OVERFLOW_WARNINGS
    comp = competence.load(repo, vocab, warnings)
    vc = parse_value_chain.parse((repo / SOURCE_FILES["value_chain"]).read_text(encoding="utf-8"), vocab)
    rubric = parse_rubric.parse((repo / SOURCE_FILES["rubric"]).read_text(encoding="utf-8"))
    ped = parse_pedagogy.parse((repo / SOURCE_FILES["pedagogy"]).read_text(encoding="utf-8"))
    config = json.loads((src / "site.json").read_text(encoding="utf-8"))
    exs = examples.load(Path(examples_arg) if examples_arg else src / "examples.json", vocab, comp, ped, warnings)

    site = Site(vocab=vocab, prov=prov, value_chain=vc, competence=comp, rubric=rubric, pedagogy=ped,
                examples=exs, warnings=warnings)
    site.src = src
    site.config = config
    tok = tokens.load(src / "tokens.json")

    makers = [lambda: F.landing(site), lambda: M.where_overview(site)]
    makers += [lambda sid=s["id"]: M.stage_page(site, sid) for s in site.stages]
    makers += [lambda: M.what_overview(site), lambda: M.levels_page(site)]
    makers += [lambda said=sa["id"]: M.subarea_page(site, said) for sa in comp["subareas"]]
    makers += [lambda c=c: M.competency_page(site, c) for c in comp["competencies"]]
    makers += [lambda: M.how_overview(site)]
    makers += [lambda cid=c["id"]: M.c4_page(site, cid) for c in ped["cs"]]
    makers += [lambda tid=t["id"]: M.trump_page(site, tid) for t in ped["trumps"]]
    makers += [lambda: F.examples_overview(site)]
    makers += [lambda e=e: F.example_page(site, e) for e in exs]
    makers += [lambda: M.tools_page(site), lambda: F.about_page(site)]

    pages = []
    for make in makers:
        C.reset_uids()
        pages.append(make())
    entries = [e for p in pages for e in p.search]
    C.reset_uids()
    search = F.search_page(site, entries)
    search.search = [{"t": "Search and index", "k": "page", "m": "neutral", "u": "search/", "p": "Search",
                      "x": "Every page in one list", "s": "index a-z", "b": ""}]
    pages.append(search)
    entries += search.search

    files: dict[str, bytes] = {}
    for p in pages:
        key = f"{p.path}index.html"
        if key in files:
            raise BuildError(f"Two pages render to {key}")
        files[key] = shell(site, p).encode("utf-8")

    files["assets/site.css"] = (tokens.css(tok) + font_css() + (src / "css" / "site.css").read_text(encoding="utf-8")).encode("utf-8")
    files["assets/site.js"] = (src / "js" / "site.js").read_bytes()
    files["assets/search-index.json"] = (json.dumps(entries, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
    files["assets/favicon.svg"] = F.favicon().encode("utf-8")
    files["assets/logo-snake.svg"] = (src / "icons" / "logo_snake_green.svg").read_bytes()
    for f in sorted((src / "fonts").iterdir()):
        if f.suffix in (".woff2", ".txt"):
            files[f"assets/fonts/{f.name}"] = f.read_bytes()

    errors, check_warnings = check.run(files, config["external_allow"])
    warnings += check_warnings
    if errors:
        raise BuildError("Generated site failed its checks:\n  " + "\n  ".join(errors[:60])
                         + (f"\n  … and {len(errors) - 60} more" if len(errors) > 60 else ""))

    info = {
        "generator": "scripts/build_onboarding.py",
        "source": {"repo": prov.repo, "sha": prov.sha, "commit_date": prov.commit_date, "dirty": prov.dirty, "files": prov.files},
        "versions": {"value_chain": vc["version"], "pedagogy": ped["version"], "competence": None},
        "counts": dict(site.counts(), pages=len(pages)),
        "warnings": sorted(set(warnings)),
        "files": sorted(files),
    }
    files[MANIFEST] = (json.dumps(info, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    return files, site, sorted(set(warnings))


def write(out_dir: Path, files: dict) -> tuple[int, int]:
    previous: list[str] = []
    manifest = out_dir / MANIFEST
    if manifest.is_file():
        previous = json.loads(manifest.read_text(encoding="utf-8")).get("files", [])
    changed = 0
    for rel_path, data in sorted(files.items()):
        path = out_dir / rel_path
        if path.is_file() and path.read_bytes() == data:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        changed += 1
    removed = 0
    for rel_path in previous:
        if rel_path in files or rel_path.startswith(PROTECTED):
            continue
        path = out_dir / rel_path
        if path.is_file():
            path.unlink()
            removed += 1
            parent = path.parent
            while parent != out_dir and parent.is_dir() and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
    return changed, removed


def stale(out_dir: Path, files: dict) -> list[str]:
    diffs = []
    for rel_path, data in sorted(files.items()):
        path = out_dir / rel_path
        if not path.is_file():
            diffs.append(f"missing {rel_path}")
        elif path.read_bytes() != data:
            diffs.append(f"differs {rel_path}")
    manifest = out_dir / MANIFEST
    if manifest.is_file():
        for rel_path in json.loads(manifest.read_text(encoding="utf-8")).get("files", []):
            if rel_path not in files and (out_dir / rel_path).is_file():
                diffs.append(f"leftover {rel_path}")
    return diffs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", help="Path to a cpdse-reference-models checkout (default: $CPDSE_REFERENCE_MODELS or ../cpdse-reference-models)")
    ap.add_argument("--out", default="reference-models", help="Output folder inside the website repo (default: reference-models)")
    ap.add_argument("--examples", help="Use a different examples.json (for testing)")
    ap.add_argument("--check", action="store_true", help="Build in memory and fail if the committed output is stale; write nothing")
    ap.add_argument("--allow-dirty", action="store_true", help="Allow uncommitted changes in the models repo")
    args = ap.parse_args(argv)
    out_dir = WEBSITE / args.out
    try:
        files, site, warnings = build(args.models, args.out, args.examples, args.allow_dirty)
    except BuildError as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        return 1
    c = site.counts()
    summary = (f"{c['substeps']} substeps · {c['domains']} domains · {c['subareas']} sub-areas · {c['competencies']} competencies · "
               f"{c['cs']} Cs · {c['trumps']} Trumps · {c['crosswalk_rows']} crosswalk rows · {c['examples']} examples")
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    pages = sum(1 for k in files if k.endswith(".html"))
    if args.check:
        diffs = stale(out_dir, files)
        if diffs:
            print(f"check failed: output in {args.out}/ is stale ({len(diffs)} files). Rebuild and commit.", file=sys.stderr)
            for d in diffs[:20]:
                print(f"  {d}", file=sys.stderr)
            return 1
        print(f"check ok: {pages} pages · {summary}")
        return 0
    changed, removed = write(out_dir, files)
    print(f"{pages} pages · {changed} changed · {removed} removed · {len(warnings)} warning{'s' if len(warnings) != 1 else ''}\n{summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
