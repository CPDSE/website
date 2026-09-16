"""Hand-written copy from ``_src/``: ``$count`` placeholders, then shortcodes."""
from __future__ import annotations

from .. import BuildError
from .core import Ctx, fill, resolve_shortcodes


def values(site) -> dict:
    c = site.counts()
    return {
        "n_tiers": c["tiers"], "n_substeps": c["substeps"], "n_domains": c["domains"],
        "n_subareas": c["subareas"], "n_competencies": c["competencies"], "n_cs": c["cs"],
        "n_trumps": c["trumps"], "n_tools": c["tools"], "n_crosswalk": c["crosswalk_rows"],
        "n_examples": c["examples"],
        "vc_version": site.vc["version"], "ped_version": site.ped["version"],
        "competence_date": site.prov.files["competence"]["date"],
        "source_sha": site.prov.short_sha, "source_date": site.prov.commit_date,
    }


def raw(site, name: str, folder: str = "pages") -> str:
    path = site.src / folder / name
    if not path.is_file():
        raise BuildError(f"Missing hand-written copy {path}")
    return path.read_text(encoding="utf-8")


def copy(ctx: Ctx, name: str, folder: str = "pages", components: dict | None = None) -> str:
    where = f"_src/{folder}/{name}"
    text = fill(raw(ctx.site, name, folder), values(ctx.site), where)
    return resolve_shortcodes(ctx, text, components, where)
