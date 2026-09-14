"""Strict validation of the hand-authored running examples (``_src/examples.json``).

Examples reference model entities by vocab id and by competency name, so a
renamed stage or competency breaks the build here with a suggestion, instead of
silently producing a dead link on the site.
"""
from __future__ import annotations

import difflib
import json
from pathlib import Path

from . import BuildError

KINDS = {
    "curriculum-course": "Curriculum course",
    "people-development": "People Development",
}
TOP_KEYS = {"id", "kind", "title", "code", "short_name", "institution", "facts", "source_url", "source_label", "summary",
            "short", "anchor", "targets", "design", "illustrative"}
TARGET_KEYS = {"subarea", "competency", "today", "target", "why"}
BLOCK_KEYS = {"c4", "minutes", "title", "activity", "trumps"}


def _suggest(value: str, options) -> str:
    close = difflib.get_close_matches(value, list(options), n=1, cutoff=0.5)
    return f" Did you mean '{close[0]}'?" if close else ""


def _keys(obj: dict, allowed: set, where: str, required: set | None = None) -> None:
    if not isinstance(obj, dict):
        raise BuildError(f"{where}: expected an object")
    extra = set(obj) - allowed
    if extra:
        raise BuildError(f"{where}: unknown key(s) {sorted(extra)}")
    missing = (required if required is not None else allowed) - set(obj)
    if missing:
        raise BuildError(f"{where}: missing key(s) {sorted(missing)}")


def load(path: Path, vocab, competence: dict, pedagogy: dict, warnings: list[str]) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BuildError(f"{path}: invalid JSON ({exc})") from exc
    _keys(data, {"examples"}, str(path))

    sub_by_id = {sa["id"]: sa for sa in competence["subareas"]}
    c4_ids = {c["id"] for c in pedagogy["cs"]}
    trump_ids = {t["id"] for t in pedagogy["trumps"]}
    seen: set[str] = set()
    out = []
    for i, ex in enumerate(data["examples"]):
        where = f"{path.name} examples[{i}]"
        _keys(ex, TOP_KEYS, where)
        if ex["id"] in seen:
            raise BuildError(f"{where}: duplicate id '{ex['id']}'")
        seen.add(ex["id"])
        where = f"{path.name} examples[{ex['id']}]"
        if ex["kind"] not in KINDS:
            raise BuildError(f"{where}.kind: '{ex['kind']}' is not one of {sorted(KINDS)}")
        _keys(ex["short"], {"anchor", "deliver"}, f"{where}.short")
        _keys(ex["anchor"], {"stages", "why"}, f"{where}.anchor")
        if not ex["anchor"]["stages"]:
            raise BuildError(f"{where}.anchor.stages: needs at least one stage id")
        for sid in ex["anchor"]["stages"]:
            if sid not in vocab.stage_by_id:
                raise BuildError(f"{where}.anchor.stages: unknown stage id '{sid}'.{_suggest(sid, vocab.stage_by_id)}")
        for label, value in ex["facts"]:
            if not (isinstance(label, str) and isinstance(value, str)):
                raise BuildError(f"{where}.facts: each fact is a [label, value] pair of strings")

        for j, t in enumerate(ex["targets"]):
            tw = f"{where}.targets[{j}]"
            _keys(t, TARGET_KEYS, tw)
            sa = sub_by_id.get(t["subarea"])
            if sa is None:
                raise BuildError(f"{tw}.subarea: unknown sub-area id '{t['subarea']}'.{_suggest(t['subarea'], sub_by_id)}")
            names = {c["name"]: c for c in sa["competencies"]}
            comp = names.get(t["competency"])
            if comp is None:
                raise BuildError(
                    f"{tw}.competency: '{t['competency']}' is not a competency in '{sa['name']}'."
                    f"{_suggest(t['competency'], names)}"
                )
            if not (isinstance(t["today"], int) and isinstance(t["target"], int) and 1 <= t["today"] < t["target"] <= 5):
                raise BuildError(f"{tw}: need 1 ≤ today < target ≤ 5 (got {t['today']} → {t['target']})")
            for key in ("today", "target"):
                lv = comp["levels"][t[key] - 1]
                if lv["state"] != "ok":
                    raise BuildError(f"{tw}.{key}: L{t[key]} of '{comp['name']}' does not apply ({lv['text'] or 'no sentence'})")
            t["slug"] = comp["slug"]
            t["id"] = comp["id"]

        _keys(ex["design"], {"format", "blocks"}, f"{where}.design")
        for k, b in enumerate(ex["design"]["blocks"]):
            bw = f"{where}.design.blocks[{k}]"
            _keys(b, BLOCK_KEYS, bw)
            if b["c4"] not in c4_ids:
                raise BuildError(f"{bw}.c4: unknown C '{b['c4']}'.{_suggest(b['c4'], c4_ids)}")
            if not (isinstance(b["minutes"], int) and b["minutes"] > 0 and b["minutes"] % 5 == 0):
                raise BuildError(f"{bw}.minutes: use a positive multiple of 5 (got {b['minutes']})")
            for tr in b["trumps"]:
                if tr not in trump_ids:
                    raise BuildError(f"{bw}.trumps: unknown Trump '{tr}'.{_suggest(tr, trump_ids)}")
        covered = {b["c4"] for b in ex["design"]["blocks"]}
        if covered != c4_ids:
            warnings.append(f"{where}: design does not cover {sorted(c4_ids - covered)}")

        for key in ("targets", "design"):
            if key not in ex["illustrative"]:
                raise BuildError(f"{where}.illustrative must include '{key}' (levels and designs are examples, not assessments)")
        ex["kind_label"] = KINDS[ex["kind"]]
        ex["minutes"] = sum(b["minutes"] for b in ex["design"]["blocks"])
        out.append(ex)
    return out
