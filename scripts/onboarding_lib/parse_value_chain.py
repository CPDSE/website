"""Parse Pharma_Value_Chain_Model.md into tiers and substeps.

Each substep has the same three-part form: Primary DS question, Key questions,
Established DS methods and tools. This is a line state machine; the format is
regular but has wrapped bullet lines, bold group headers, group notes and
inline ``[BEYOND REFERENCE — …]`` flags.
"""
from __future__ import annotations

import re

from . import BuildError
from .text import join_lines
from .vocab import Vocab, tier_key

VERSION_RE = re.compile(r"^#\s*Version:\s*(v[\d.]+)\s*(?:\((.+)\))?\s*$")
UPDATED_RE = re.compile(r"^#\s*Last updated:\s*(\S+)")
TIER_RE = re.compile(r"^# Tier 1 · Step (\d+) — (.+?)\s*$")
SUBSTEP_RE = re.compile(r"^## Substep:\s*(.+?)\s*$")
GROUP_RE = re.compile(r"^\*\*([^*].*?)\*\*\s*$")
FLAG_RE = re.compile(r"\s*\[BEYOND REFERENCE(?:\s*[—–-]\s*([^\]]*))?\]\s*")
STOP = "## Coverage status"


def _flush_para(buf: list[str]) -> str:
    text = join_lines(buf)
    buf.clear()
    return text


def _item(text: str) -> dict:
    flag = None
    m = FLAG_RE.search(text)
    if m:
        flag = (m.group(1) or "").strip() or "beyond reference"
        text = FLAG_RE.sub(" ", text).strip()
    lead, sep, rest = text.partition(": ")
    if not sep:
        lead, rest = text, ""
    return {"text": text, "lead": lead.strip(), "rest": rest.strip(), "flag": flag}


def parse(md: str, vocab: Vocab) -> dict:
    version = status = updated = None
    tiers: list[dict] = []
    stages: dict[str, dict] = {}
    stage: dict | None = None
    section = None  # "pre" | "primary" | "key" | "methods"
    para: list[str] = []
    italic: list[str] = []
    group: dict | None = None

    def close_italic():
        if italic and stage is not None:
            text = join_lines(italic).strip()
            if text.startswith("*") and text.endswith("*"):
                text = text[1:-1].strip()
            stage["notes"].append(text)
        italic.clear()

    def close_para():
        if stage is None:
            para.clear()
            return
        text = _flush_para(para)
        if not text:
            return
        if section == "primary":
            stage["primary_question"] = (stage["primary_question"] + " " + text).strip()
        elif section == "methods" and group is not None:
            group["notes"].append(text)

    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith(STOP):
            break
        if version is None and (m := VERSION_RE.match(line)):
            version, status = m.group(1), (m.group(2) or "").strip() or None
            continue
        if updated is None and (m := UPDATED_RE.match(line)):
            updated = m.group(1)
            continue

        if m := TIER_RE.match(line):
            close_para(); close_italic()
            tiers.append({"step": int(m.group(1)), "heading": m.group(2), "stages": []})
            stage, section, group = None, None, None
            continue

        if m := SUBSTEP_RE.match(line):
            close_para(); close_italic()
            if not tiers:
                raise BuildError(f"Substep '{m.group(1)}' appears before any tier heading")
            sid = vocab.stage_for_heading(m.group(1))
            if sid in stages:
                raise BuildError(f"Substep '{m.group(1)}' appears twice")
            csv_row = vocab.stage_by_id[sid]
            if tier_key(csv_row["tier"]) != tier_key(tiers[-1]["heading"]):
                raise BuildError(
                    f"Substep '{m.group(1)}' is under tier '{tiers[-1]['heading']}' but stages.csv says '{csv_row['tier']}'"
                )
            stage = {"id": sid, "heading": m.group(1), "primary_question": "", "key_questions": [],
                     "method_groups": [], "notes": []}
            stages[sid] = stage
            tiers[-1]["stages"].append(sid)
            section, group = "pre", None
            continue

        if stage is None:
            continue

        if line.startswith("### "):
            close_para(); close_italic()
            title = line[4:].strip().lower()
            if title.startswith("primary ds question"):
                section = "primary"
            elif title.startswith("key questions"):
                section = "key"
            elif title.startswith("established ds methods"):
                section = "methods"
                group = {"title": None, "notes": [], "items": []}
                stage["method_groups"].append(group)
            else:
                raise BuildError(f"Unexpected section '{line}' in substep '{stage['heading']}'")
            continue

        stripped = line.strip()
        if stripped == "---":
            close_para(); close_italic()
            continue
        if not stripped:
            close_para()
            if italic and italic[-1].rstrip().endswith("*"):
                close_italic()
            continue

        # Italic scope notes (anywhere in a substep, outside lists).
        if italic:
            italic.append(stripped)
            if stripped.endswith("*") and not stripped.endswith("**"):
                close_italic()
            continue
        if stripped.startswith("*") and not stripped.startswith("**"):
            close_para()
            italic.append(stripped)
            if len(stripped) > 1 and stripped.endswith("*") and not stripped.endswith("**"):
                close_italic()
            continue

        if section == "key":
            if stripped.startswith("- "):
                stage["key_questions"].append(stripped[2:].strip())
            elif raw.startswith(" ") and stage["key_questions"]:
                stage["key_questions"][-1] += " " + stripped
            else:
                raise BuildError(f"Unexpected line in key questions of '{stage['heading']}': {stripped}")
            continue

        if section == "methods":
            if m := GROUP_RE.match(stripped):
                close_para()
                if group is not None and not group["items"] and not group["notes"] and group["title"] is None:
                    group["title"] = m.group(1)
                else:
                    group = {"title": m.group(1), "notes": [], "items": []}
                    stage["method_groups"].append(group)
                continue
            if stripped.startswith("- "):
                close_para()
                group["items"].append(_item(stripped[2:].strip()))
                continue
            if raw.startswith(" ") and group["items"] and not para:
                last = group["items"][-1]
                glue = "" if re.search(r"\w-$", last["text"]) else " "
                group["items"][-1] = _item(last["text"] + glue + stripped + (
                    f" [BEYOND REFERENCE — {last['flag']}]" if last["flag"] else ""))
                continue
            para.append(stripped)
            continue

        if section == "primary":
            para.append(stripped)
            continue

    close_para(); close_italic()

    for sid, st in stages.items():
        missing = [k for k in ("primary_question", "key_questions") if not st[k]]
        if not any(g["items"] for g in st["method_groups"]):
            missing.append("method_groups")
        if missing:
            raise BuildError(f"Substep '{st['heading']}' is missing: {', '.join(missing)}")
        st["method_groups"] = [g for g in st["method_groups"] if g["items"] or g["notes"]]

    expected = [s["id"] for s in vocab.stages]
    found = [sid for t in tiers for sid in t["stages"]]
    if found != expected:
        raise BuildError(
            "Value chain substeps do not match vocab/stages.csv order:\n"
            f"  markdown: {found}\n  csv:      {expected}"
        )
    if not version:
        raise BuildError("Value chain model has no '# Version:' header")
    return {"version": version, "status": status, "updated": updated, "tiers": tiers, "stages": stages}
