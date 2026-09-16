"""Page context, the page record, and shortcode resolution for hand-written copy."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from string import Template

from .. import BuildError
from ..text import h, rel

MODELS = {
    "where": {"q": "Where", "name": "Pharma Value Chain", "short": "Value chain", "icon": "i-where", "home": "where/"},
    "what": {"q": "What", "name": "PDS Competence Model", "short": "Competencies", "icon": "i-what", "home": "what/"},
    "how": {"q": "How", "name": "Pedagogic Practices", "short": "Teaching practice", "icon": "i-how", "home": "how/"},
    "ex": {"q": "Examples", "name": "Worked examples", "short": "Courses & workshops", "icon": "i-ex", "home": "examples/"},
}


@dataclass
class Page:
    path: str                      # site path of the page directory, e.g. "where/lead-identification/"
    title: str                     # <title> and usually <h1>
    model: str                     # "start" | "where" | "what" | "how" | "ex" | "neutral"
    body: str
    description: str = ""
    search: list = field(default_factory=list)   # search index entries contributed by this page
    data_json: str = ""            # optional JSON for site.js (<script type="application/json">)
    body_class: str = ""


class Ctx:
    def __init__(self, site, path: str):
        self.site = site
        self.path = path

    def href(self, to: str) -> str:
        return rel(self.path, to)

    def a(self, to: str, inner_html: str, cls: str = "", extra: str = "") -> str:
        """Link to a site path. Links take the colour of the model they point to (``to-*``)."""
        classes = " ".join(c for c in (cls, target_class(to)) if c)
        c = f' class="{classes}"' if classes else ""
        return f'<a href="{h(self.href(to))}"{c}{extra}>{inner_html}</a>'

    def icon(self, name: str, cls: str = "ico") -> str:
        return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#{name}"></use></svg>'


def target_class(to: str) -> str:
    if to.startswith("#"):
        return ""
    for prefix, key in (("where/", "where"), ("what/", "what"), ("how/", "how"), ("examples/", "ex")):
        if to.startswith(prefix):
            return f"to-{key}"
    return ""


_SHORT = re.compile(r"\[\[([a-z0-9]+):([^\]|]+)(?:\|([^\]]+))?\]\]")


def resolve_shortcodes(ctx: Ctx, html_text: str, components: dict | None = None, where: str = "") -> str:
    """Replace ``[[kind:ref|label]]`` with canonical links; unknown refs fail the build."""
    site = ctx.site
    components = components or {}

    def link(to: str, label: str, model: str) -> str:
        return ctx.a(to, h(label), cls=f"ref ref-{model}")

    def sub(m: re.Match) -> str:
        kind, ref, label = m.group(1), m.group(2).strip(), (m.group(3) or "").strip()
        if kind == "component":
            if ref not in components:
                raise BuildError(f"{where}: unknown component '{ref}'")
            return components[ref]()
        if kind == "stage":
            st = site.stage_by_id.get(ref)
            if st is None:
                raise BuildError(f"{where}: unknown stage '{ref}'")
            return link(site.u_stage(ref), label or st["display_name"], "where")
        if kind == "tier":
            tier = next((t for t in site.tiers if t["id"] == ref), None)
            if tier is None:
                raise BuildError(f"{where}: unknown tier '{ref}'")
            return link(site.u_tier(ref), label or tier["name"], "where")
        if kind == "domain":
            d = site.domain_by_id.get(ref)
            if d is None:
                raise BuildError(f"{where}: unknown domain '{ref}'")
            return link(site.u_domain(ref), label or d["name"], "what")
        if kind == "sub":
            sa = site.sub_by_id.get(ref)
            if sa is None:
                raise BuildError(f"{where}: unknown sub-area '{ref}'")
            return link(site.u_sub(ref), label or sa["name"], "what")
        if kind == "comp":
            said, _, slug = ref.partition("/")
            c = site.comp_by_key.get((said, slug))
            if c is None:
                raise BuildError(f"{where}: unknown competency '{ref}' (use sub-area-id/competency-slug)")
            return link(site.u_comp(said, slug), label or c["name"], "what")
        if kind == "level":
            if ref not in {"1", "2", "3", "4", "5"}:
                raise BuildError(f"{where}: unknown level '{ref}'")
            name = site.comp["levels"][int(ref) - 1]["name"]
            return link(site.u_level(int(ref)), label or f"L{ref} {name}", "what")
        if kind == "c4":
            c = site.c4_by_id.get(ref)
            if c is None:
                raise BuildError(f"{where}: unknown C '{ref}'")
            return link(site.u_c4(ref), label or c["name"], "how")
        if kind == "trump":
            t = site.trump_by_id.get(ref)
            if t is None:
                raise BuildError(f"{where}: unknown Trump '{ref}'")
            return link(site.u_trump(ref), label or t["name"], "how")
        if kind == "ex":
            e = site.example_by_id.get(ref)
            if e is None:
                raise BuildError(f"{where}: unknown example '{ref}'")
            return link(site.u_example(ref), label or f"{e['institution']} {e['code']}", "ex")
        if kind == "model":
            if ref not in MODELS:
                raise BuildError(f"{where}: unknown model '{ref}'")
            return link(MODELS[ref]["home"], label or MODELS[ref]["name"], ref)
        if kind == "page":
            if not label:
                raise BuildError(f"{where}: [[page:{ref}]] needs a label")
            return ctx.a(ref, h(label))
        raise BuildError(f"{where}: unknown shortcode kind '{kind}'")

    return _SHORT.sub(sub, html_text)


def fill(template_text: str, values: dict, where: str) -> str:
    try:
        return Template(template_text).substitute(values)
    except (KeyError, ValueError) as exc:
        raise BuildError(f"{where}: template placeholder problem: {exc}") from exc
