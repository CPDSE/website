"""Data-driven SVG figures. Colours come from CSS classes (site.css), never inline styles."""
from __future__ import annotations

from ..text import h
from .core import Ctx


def value_competence_map(ctx: Ctx, title_id: str = "map-title") -> str:
    """The map: value-chain substeps across, competence domains down, example targets as marks."""
    s = ctx.site
    left, right, top = 232, 948, 78
    gap, row_h = 8, 46
    n = len(s.stages)
    col_w = (right - left - gap * (len(s.tiers) - 1)) / n
    col_x: dict[str, float] = {}
    x = left
    tier_spans = []
    for t in s.tiers:
        start = x
        for sid in t["stages"]:
            col_x[sid] = x
            x += col_w
        tier_spans.append((t, start, x))
        x += gap
    doms = s.comp["domains"]
    height = top + row_h * len(doms) + 50

    out = [f'<svg class="fig-map" viewBox="0 0 960 {height}" role="group" aria-labelledby="{title_id}">'
           f'<title id="{title_id}">Grid of the {n} value-chain substeps against the {len(doms)} competence domains, '
           f'with the illustrative targets from our two examples</title>']
    for t, x0, x1 in tier_spans:
        out.append(f'<a href="{h(ctx.href(s.u_tier(t["id"])))}"><rect class="m-tier" x="{x0:.1f}" y="0" width="{x1 - x0:.1f}" height="26" rx="4"></rect>'
                   f'<text class="m-tier-t" x="{x0 + 8:.1f}" y="18">{h(t["name"])}</text></a>')
    for st in s.stages:
        cx = col_x[st["id"]] + col_w / 2
        out.append(f'<a href="{h(ctx.href(s.u_stage(st["id"])))}"><title>Substep {st["order"]}: {h(st["display_name"])}</title>'
                   f'<rect class="m-num-hit" x="{col_x[st["id"]]:.1f}" y="32" width="{col_w:.1f}" height="28"></rect>'
                   f'<text class="m-num" x="{cx:.1f}" y="51" text-anchor="middle">{st["order"]}</text></a>')
    for ri, d in enumerate(doms):
        y = top + ri * row_h
        out.append(f'<a href="{h(ctx.href(s.u_domain(d["id"])))}"><text class="m-row-t" x="{left - 12}" y="{y + row_h / 2 + 4:.1f}" text-anchor="end">{h(d["name"])}</text></a>')
        for st in s.stages:
            out.append(f'<rect class="m-cell" x="{col_x[st["id"]] + 1.5:.1f}" y="{y + 1.5:.1f}" width="{col_w - 3:.1f}" height="{row_h - 3}" rx="3"></rect>')
    row_of = {d["id"]: i for i, d in enumerate(doms)}
    for ex in s.examples:
        sid = ex["anchor"]["stages"][0]
        for t in ex["targets"]:
            dom = s.sub_by_id[t["subarea"]]["domain"]
            cx = col_x[sid] + col_w / 2
            cy = top + row_of[dom] * row_h + row_h / 2 + 7
            comp = s.comp_by_key[(t["subarea"], t["slug"])]
            label = f'{ex["short_name"]}: {comp["name"]}, illustrative L{t["today"]} to L{t["target"]}'
            out.append(f'<a href="{h(ctx.href(s.u_comp(t["subarea"], t["slug"])))}"><title>{h(label)}</title>'
                       f'<circle class="m-mark exk-{ex["kind"]}" cx="{cx:.1f}" cy="{cy:.1f}" r="8"></circle>'
                       f'<text class="m-mark-t" x="{cx:.1f}" y="{cy - 12:.1f}" text-anchor="middle">{t["today"]}→{t["target"]}</text></a>')
    y_axis = top + row_h * len(doms) + 32
    out.append(f'<text class="m-axis" x="{left}" y="{y_axis}">WHERE: value-chain substeps, numbered in pipeline order</text>')
    out.append(f'<text class="m-axis" x="0" y="{top - 22}">WHAT: competence domains</text>')
    out.append("</svg>")
    return "".join(out)


def map_legend(ctx: Ctx) -> str:
    s = ctx.site
    items = []
    for ex in s.examples:
        st = s.stage_by_id[ex["anchor"]["stages"][0]]
        for t in ex["targets"]:
            comp = s.comp_by_key[(t["subarea"], t["slug"])]
            dom = s.domain_by_id[s.sub_by_id[t["subarea"]]["domain"]]
            items.append(
                f'<li class="legend-item exk-{ex["kind"]}"><span class="legend-dot" aria-hidden="true"></span>'
                f'<span>{ctx.a(s.u_example(ex["id"]), h(ex["short_name"]))} ({h(ex["kind_label"])}): '
                f'{ctx.a(s.u_comp(t["subarea"], t["slug"]), h(comp["name"]))} in {h(dom["name"])}, '
                f'from L{t["today"]} to L{t["target"]} (illustrative), anchored at substep {st["order"]}, '
                f'{ctx.a(s.u_stage(st["id"]), h(st["display_name"]))}.</span></li>'
            )
    return f'<ul class="legend">{"".join(items)}</ul>'


def four_cs_cycle(ctx: Ctx, current: str | None = None, uid: str = "cyc") -> str:
    s = ctx.site
    pos = [(180, 32), (296, 150), (180, 268), (64, 150)]
    w, hgt = 120, 44
    out = [f'<svg class="fig-cycle" viewBox="-8 -8 376 316" role="img" aria-labelledby="{uid}-t">'
           f'<title id="{uid}-t">The 4Cs as a cycle: Connections, Concepts, Concrete Practice, Conclusions</title>'
           f'<defs><marker id="{uid}-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           f'<path class="cyc-head" d="M0,0 L10,5 L0,10 z"></path></marker></defs>']
    arcs = ["M244,34 Q294,42 296,124", "M296,176 Q294,258 244,266", "M116,266 Q66,258 64,176", "M64,124 Q66,42 116,34"]
    for d in arcs:
        out.append(f'<path class="cyc-arc" d="{d}" marker-end="url(#{uid}-arrow)"></path>')
    out.append('<text class="cyc-center" x="180" y="148" text-anchor="middle">4Cs</text>'
               '<text class="cyc-center-sub" x="180" y="172" text-anchor="middle">one session</text>')
    for (cx, cy), c in zip(pos, s.ped["cs"]):
        is_cur = c["id"] == current
        aria = ' aria-current="page"' if is_cur else ""
        label = c["name"]
        out.append(f'<a href="{h(ctx.href(s.u_c4(c["id"])))}"{aria}><rect class="cyc-node{" is-current" if is_cur else ""}" x="{cx - w / 2}" y="{cy - hgt / 2}" width="{w}" height="{hgt}" rx="22"></rect>'
                   f'<text class="cyc-label{" is-current" if is_cur else ""}" x="{cx}" y="{cy + 5}" text-anchor="middle">{h(label)}</text></a>')
    out.append("</svg>")
    return "".join(out)
