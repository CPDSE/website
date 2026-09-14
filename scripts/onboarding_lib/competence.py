"""PDS Competence Model: reuse the models repo's own parser, then enrich it.

``build_model_json.parse`` stays the single parser for the competence markdown.
This module joins its output to the vocab CSVs (ids), adds URL slugs, detects
not-applicable levels and resolves the ``competency @ level`` example tags.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

from . import BuildError
from .sources import SOURCE_FILES
from .text import slugify
from .vocab import Vocab

PARSER = "competency-model/viz/build_model_json.py"


def load_parser(repo: Path):
    path = repo / PARSER
    if not path.is_file():
        raise BuildError(f"Missing competence parser {path}")
    # The models repo has no .gitignore: never leave __pycache__ behind in it.
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("cpdse_build_model_json", path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    if not hasattr(module, "parse"):
        raise BuildError(f"{path} no longer exposes parse(md_text)")
    return module


def level_state(desc: str) -> tuple[str, str]:
    """Classify one level sentence.

    A leading em dash means the level does not apply; any text after it is a
    note (``— *(merges with …)*``). The older explorer only matched a bare dash.
    """
    s = desc.strip()
    if not s:
        return ("missing", "")
    if s.startswith("—"):
        note = s[1:].strip().strip("*").strip()
        if note.startswith("(") and note.endswith(")"):
            note = note[1:-1].strip()
        return ("na", note)
    return ("ok", s)


_ELLIPSIS = re.compile(r"(\.\.\.|…)\s*$")


def _norm(name: str) -> str:
    return " ".join(name.lower().split())


def resolve_tag(name: str, comps: list[dict]) -> dict | None:
    """Exact (case-insensitive) match, else a prefix match for truncated tags."""
    key = _norm(name)
    for c in comps:
        if _norm(c["name"]) == key:
            return c
    if _ELLIPSIS.search(name):
        prefix = _norm(_ELLIPSIS.sub("", name))
        hits = [c for c in comps if _norm(c["name"]).startswith(prefix)]
        if len(hits) == 1:
            return hits[0]
    return None


def load(repo: Path, vocab: Vocab, warnings: list[str]) -> dict:
    parser = load_parser(repo)
    md = (repo / SOURCE_FILES["competence"]).read_text(encoding="utf-8")
    model = parser.parse(md)

    if [d["name"] for d in model["domains"]] != [d["display_name"] for d in vocab.domains]:
        raise BuildError(
            "Competence model domains do not match vocab/domains.csv (names or order):\n"
            f"  markdown: {[d['name'] for d in model['domains']]}\n"
            f"  csv:      {[d['display_name'] for d in vocab.domains]}"
        )

    level_defs = {ld["level"]: ld for ld in model.get("levelDefs", [])}
    if sorted(level_defs) != [1, 2, 3, 4, 5]:
        raise BuildError("Competence model intro must define L1–L5")

    domains: list[dict] = []
    subareas: list[dict] = []
    csv_subs = iter(vocab.subareas)
    for d_md, d_csv in zip(model["domains"], vocab.domains):
        domain = {"id": d_csv["id"], "name": d_csv["display_name"], "order": d_csv["order"], "subareas": []}
        for sa_md in d_md["subareas"]:
            sa_csv = next(csv_subs, None)
            if sa_csv is None or sa_csv["display_name"] != sa_md["name"] or sa_csv["domain_id"] != domain["id"]:
                raise BuildError(
                    f"Sub-area '{sa_md['name']}' in domain '{domain['name']}' does not match the next "
                    f"vocab/subareas.csv row ({sa_csv['display_name'] if sa_csv else 'none left'})"
                )
            comps: list[dict] = []
            seen: set[str] = set()
            for c in sa_md["competencies"]:
                slug = slugify(c["name"])
                base, n = slug, 2
                while slug in seen:
                    slug, n = f"{base}-{n}", n + 1
                seen.add(slug)
                levels = []
                for i, desc in enumerate(c["descriptions"], start=1):
                    state, text = level_state(desc)
                    if state == "missing":
                        warnings.append(f"Competency {c['id']} '{c['name']}' has no L{i} sentence")
                    levels.append({"n": i, "state": state, "text": text})
                comps.append({
                    "id": c["id"],
                    "slug": slug,
                    "name": c["name"],
                    "subarea": sa_csv["id"],
                    "domain": domain["id"],
                    "levels": levels,
                    "examples": [],
                })
            examples = []
            for ex in sa_md["examples"]:
                tags = []
                for t in ex["tags"]:
                    comp = resolve_tag(t["competency"], comps)
                    if comp is None:
                        warnings.append(
                            f"Pharma example tag '{t['competency']} @ L{t['level']}' in sub-area "
                            f"'{sa_csv['display_name']}' matches no competency (upstream data)"
                        )
                    tags.append({"name": t["competency"], "level": t["level"], "slug": comp["slug"] if comp else None})
                    if comp is not None:
                        comp["examples"].append({"text": ex["text"], "level": t["level"]})
                examples.append({"text": ex["text"], "tags": tags})
            subarea = {
                "id": sa_csv["id"],
                "name": sa_csv["display_name"],
                "order": sa_csv["order"],
                "domain": domain["id"],
                "stack": sa_md.get("stack", ""),
                "examples": examples,
                "competencies": comps,
            }
            domain["subareas"].append(subarea)
            subareas.append(subarea)
        domains.append(domain)

    if next(csv_subs, None) is not None:
        raise BuildError("vocab/subareas.csv has rows the competence markdown does not")

    return {
        "levels": [{"n": n, "name": level_defs[n]["name"], "short": level_defs[n]["short"]} for n in range(1, 6)],
        "domains": domains,
        "subareas": subareas,
        "competencies": [c for sa in subareas for c in sa["competencies"]],
    }
