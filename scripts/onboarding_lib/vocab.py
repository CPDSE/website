"""Load the controlled vocabulary CSVs (the system of record for ids and names)."""
from __future__ import annotations

import csv
from pathlib import Path

from . import BuildError
from .text import slugify


OVERFLOW_WARNINGS: list[str] = []


def _load(path: Path) -> list[dict]:
    """Read a CSV; an unquoted comma in the last column is rejoined, with a warning."""
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for lineno, cells in enumerate(reader, start=2):
            if not cells:
                continue
            if len(cells) > len(header):
                OVERFLOW_WARNINGS.append(
                    f"{path.parent.name}/{path.name}:{lineno}: unquoted comma in '{header[-1]}' "
                    f"(read as '{','.join(cells[len(header) - 1:])}')"
                )
                cells = cells[:len(header) - 1] + [",".join(cells[len(header) - 1:])]
            cells += [""] * (len(header) - len(cells))
            rows.append({k: v.strip() for k, v in zip(header, cells)})
        return rows


def tier_key(name: str) -> str:
    """Compare tier names case- and punctuation-insensitively."""
    return "".join(ch for ch in name.lower() if ch.isalnum())


class Vocab:
    def __init__(self, repo: Path):
        root = repo / "vocab"
        self.stages = sorted(_load(root / "stages.csv"), key=lambda r: int(r["order"]))
        self.domains = sorted(_load(root / "domains.csv"), key=lambda r: int(r["order"]))
        self.subareas = sorted(_load(root / "subareas.csv"), key=lambda r: int(r["order"]))
        self.crosswalk = _load(root / "crosswalk.csv")

        for s in self.stages:
            s["order"] = int(s["order"])
            s["aliases"] = [a.strip() for a in s["aliases"].split("|") if a.strip()]
        for d in self.domains:
            d["order"] = int(d["order"])
        for sa in self.subareas:
            sa["order"] = int(sa["order"])

        self.stage_by_id = {s["id"]: s for s in self.stages}
        self.domain_by_id = {d["id"]: d for d in self.domains}
        self.subarea_by_id = {sa["id"]: sa for sa in self.subareas}

        self._stage_lookup: dict[str, str] = {}
        for s in self.stages:
            self._stage_lookup[s["display_name"].lower()] = s["id"]
            for a in s["aliases"]:
                self._stage_lookup[a.lower()] = s["id"]

        # Tiers in first-appearance order.
        self.tiers: list[dict] = []
        for s in self.stages:
            if not self.tiers or self.tiers[-1]["name"] != s["tier"]:
                self.tiers.append({"name": s["tier"], "id": slugify(s["tier"]), "stages": []})
            self.tiers[-1]["stages"].append(s["id"])
            s["tier_id"] = self.tiers[-1]["id"]

    def stage_for_heading(self, heading: str) -> str:
        key = heading.strip().lower()
        if key not in self._stage_lookup:
            raise BuildError(f"Substep heading '{heading}' has no stages.csv row (display name or alias)")
        return self._stage_lookup[key]

    def tools(self) -> list[dict]:
        """Group crosswalk rows by tool; one entry per canonical tool."""
        by_slug: dict[str, dict] = {}
        for row in self.crosswalk:
            name = row["canonical_tool"]
            slug = slugify(name)
            tool = by_slug.setdefault(slug, {
                "slug": slug,
                "name": name,
                "type": row["type"],
                "aliases": [],
                "links": [],
            })
            if tool["name"] != name:
                raise BuildError(f"Tool names '{tool['name']}' and '{name}' collide on slug '{slug}'")
            for a in row["aliases"].split("|"):
                a = a.strip()
                if a and a not in tool["aliases"]:
                    tool["aliases"].append(a)
            tool["links"].append({
                "stage": row["stage_id"],
                "domain": row["pds_domain"],
                "subarea": row["pds_subarea"] or None,
                "flag": row["flag"] or None,
                "confidence": row["confidence"],
                "notes": row["notes"],
            })
        order = {s["id"]: s["order"] for s in self.stages}
        for tool in by_slug.values():
            tool["links"].sort(key=lambda l: order[l["stage"]])
        return sorted(by_slug.values(), key=lambda t: t["name"].lower())
