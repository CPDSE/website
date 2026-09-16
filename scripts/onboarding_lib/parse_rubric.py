"""Parse Level_Rubric.md: the four-dimension table and one section per level."""
from __future__ import annotations

import re

from . import BuildError
from .text import join_lines

ROW_RE = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|(.+)\|\s*$")
LEVEL_RE = re.compile(r"^## L([1-5]) — (\w+)\s*$")
QUOTE_RE = re.compile(r"^>\s*\*(.+)\*\s*$")
PROMO_RE = re.compile(r"^\*\*Promotion signal to L([1-5]):\*\*\s*(.+)$")
CANNOT_RE = re.compile(r"^Cannot yet(?:\s*\(([^)]*)\))?:\s*(.+)$")
STOP_RE = re.compile(r"^## How to write")


def parse(md: str) -> dict:
    dims: list[dict] = []
    levels: list[dict] = []
    cur: dict | None = None
    para: list[str] = []

    def close_para():
        if cur is not None and para:
            text = join_lines(para)
            if not re.match(r"^A person at L\d can:$", text):
                cur["notes"].append(text)
        para.clear()

    for raw in md.splitlines():
        line = raw.strip()
        if STOP_RE.match(line):
            break
        if cur is None and (m := ROW_RE.match(line)):
            cells = [c.strip() for c in m.group(2).split("|")]
            if len(cells) != 5:
                raise BuildError(f"Rubric row '{m.group(1)}' should have 5 level cells, has {len(cells)}")
            dims.append({"name": m.group(1), "cells": cells})
            continue
        if m := LEVEL_RE.match(line):
            close_para()
            cur = {"n": int(m.group(1)), "name": m.group(2), "quote": "", "can": [], "cannot": "",
                   "cannot_qualifier": "", "promotion": "", "notes": []}
            levels.append(cur)
            continue
        if cur is None:
            continue
        if not line or line == "---":
            close_para()
            continue
        if m := QUOTE_RE.match(line):
            cur["quote"] = m.group(1).strip()
            continue
        if line.startswith("- "):
            close_para()
            cur["can"].append(line[2:].strip())
            continue
        if m := CANNOT_RE.match(line):
            close_para()
            cur["cannot_qualifier"] = (m.group(1) or "").strip()
            cur["cannot"] = m.group(2).strip()
            continue
        if m := PROMO_RE.match(line):
            close_para()
            cur["promotion"] = m.group(2).strip()
            continue
        para.append(line)
    close_para()

    if [d["name"] for d in dims] != ["Autonomy", "Context", "Judgment", "Effect on others"]:
        raise BuildError(f"Rubric dimensions changed: {[d['name'] for d in dims]}")
    if [lv["n"] for lv in levels] != [1, 2, 3, 4, 5]:
        raise BuildError("Rubric must have sections L1–L5 in order")
    for lv in levels:
        if not (lv["quote"] and lv["can"]):
            raise BuildError(f"Rubric L{lv['n']} is missing its quote or can-list")
        if lv["n"] < 5 and not lv["promotion"]:
            raise BuildError(f"Rubric L{lv['n']} is missing its promotion signal")
    return {"dimensions": dims, "levels": levels}
