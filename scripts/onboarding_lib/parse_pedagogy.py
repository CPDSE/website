"""Parse Pedagogic_Practices.md: sources, premise, the 4Cs, the Six Trumps and
the 4Cs → Workshop 1 block mapping."""
from __future__ import annotations

import re

from . import BuildError
from .text import join_lines, slugify

VERSION_RE = re.compile(r"^#\s*Version:\s*(v[\d.]+)\s*(?:\((.+)\))?\s*$")
UPDATED_RE = re.compile(r"^#\s*Last updated:\s*(\S+)")
ITEM_RE = re.compile(r"^(\d)\.\s+\*\*(.+?)\*\*\s*[—–-]\s*(.+)$")
PREMISE_RE = re.compile(r"^Core premise:\s*(.+)$")
ROW_RE = re.compile(r"^\|(.+)\|(.+)\|\s*$")


def _split_marker(text: str, marker: str) -> tuple[str, str]:
    body, sep, extra = text.partition(f"*{marker}:*")
    return body.strip(), extra.strip() if sep else ""


def parse(md: str) -> dict:
    version = status = updated = None
    section = None
    blocks: dict[str, list[list[str]]] = {"intro": [], "4cs": [], "trumps": [], "uses": []}
    cur: list[str] = []

    def flush():
        if cur and section in blocks:
            blocks[section].append(list(cur))
        cur.clear()

    for raw in md.splitlines():
        line = raw.rstrip()
        if version is None and (m := VERSION_RE.match(line)):
            version, status = m.group(1), (m.group(2) or "").strip() or None
            continue
        if updated is None and (m := UPDATED_RE.match(line)):
            updated = m.group(1)
            continue
        if line.startswith("## "):
            flush()
            title = line[3:].lower()
            section = ("intro" if title.startswith("what this is") else
                       "4cs" if title.startswith("the 4cs") else
                       "trumps" if title.startswith("the six trumps") else
                       "uses" if title.startswith("how cpdse uses") else None)
            continue
        if not line.strip() or line.strip() == "---":
            flush()
            continue
        # A new numbered item starts a new block even without a blank line.
        if ITEM_RE.match(line) and cur:
            flush()
        cur.append(line)
    flush()

    def items(key: str, marker: str) -> tuple[str, list[dict]]:
        intro, out = [], []
        for block in blocks[key]:
            m = ITEM_RE.match(block[0])
            if not m:
                if not out:
                    intro.append(join_lines(block))
                continue
            text = join_lines([m.group(3)] + block[1:])
            body, extra = _split_marker(text, marker)
            out.append({"n": int(m.group(1)), "name": m.group(2).strip(), "id": slugify(m.group(2)),
                        "body": body, marker.lower(): extra})
        return " ".join(intro), out

    cs_intro, cs = items("4cs", "Examples")
    trumps_intro, trumps = items("trumps", "Apply")
    if [c["name"] for c in cs] != ["Connections", "Concepts", "Concrete Practice", "Conclusions"]:
        raise BuildError(f"Expected the 4Cs in order, found {[c['name'] for c in cs]}")
    if len(trumps) != 6:
        raise BuildError(f"Expected six Trumps, found {len(trumps)}")

    premise, sources, intro_paras = "", [], []
    for block in blocks["intro"]:
        text = join_lines(block)
        if block[0].lstrip().startswith("- "):
            item: list[str] = []
            for ln in block:
                if ln.lstrip().startswith("- ") and item:
                    sources.append(join_lines(item))
                    item = []
                item.append(ln.strip()[2:] if ln.lstrip().startswith("- ") else ln)
            if item:
                sources.append(join_lines(item))
        elif m := PREMISE_RE.match(text):
            premise = m.group(1)
        else:
            intro_paras.append(text)

    by_name = {c["name"].lower(): c["id"] for c in cs}
    workshop, uses_notes = [], []
    for block in blocks["uses"]:
        if block[0].lstrip().startswith("|"):
            for ln in block:
                m = ROW_RE.match(ln.strip())
                if not m or set(m.group(1).strip()) <= set("-: "):
                    continue
                left, right = m.group(1).strip(), m.group(2).strip()
                if left.lower().startswith("workshop 1 block"):
                    continue
                named = re.findall(r"\*\*(.+?)\*\*", right)
                ids = []
                for chunk in named:
                    for part in re.split(r"\s*\+\s*", chunk):
                        key = re.sub(r"\s*\(.*\)$", "", part).strip().lower()
                        if key in by_name:
                            ids.append(by_name[key])
                if not ids:
                    raise BuildError(f"Workshop mapping row '{left}' names no known C: {right}")
                workshop.append({"block": left, "cs": ids, "text": right})
        else:
            uses_notes.append(join_lines(block))

    if not version:
        raise BuildError("Pedagogic practices doc has no '# Version:' header")
    return {
        "version": version, "status": status, "updated": updated,
        "premise": premise, "sources": sources, "intro": intro_paras,
        "cs_intro": cs_intro, "cs": cs, "trumps_intro": trumps_intro, "trumps": trumps,
        "workshop": workshop, "uses_notes": uses_notes,
    }
