"""Reusable HTML components. Every function returns an HTML string."""
from __future__ import annotations

import re

from ..text import h, inline_md
from .core import MODELS, Ctx

_UID = [0]


def uid(prefix: str) -> str:
    _UID[0] += 1
    return f"{prefix}-{_UID[0]}"


def reset_uids() -> None:
    _UID[0] = 0


# ---- small pieces -------------------------------------------------------------

def crumbs(ctx: Ctx, items: list) -> str:
    """items: [(label, site_path or None)]; the last item is the current page."""
    lis = []
    for i, (label, to) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li><span aria-current="page">{h(label)}</span></li>')
        else:
            lis.append(f"<li>{ctx.a(to, h(label))}</li>")
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def eyebrow(ctx: Ctx, model: str, text: str) -> str:
    icon = MODELS[model]["icon"] if model in MODELS else "i-start"
    return f'<p class="eyebrow eyebrow-{model}">{ctx.icon(icon)}<span>{h(text)}</span></p>'


def chip(text: str, cls: str = "") -> str:
    return f'<span class="chip {cls}">{h(text)}</span>'


def draft_badge(status: str | None) -> str:
    if not status:
        return ""
    text = status.replace("MO review", "CPDSE review")
    return f'<span class="badge badge-draft">Draft: {h(text)}</span>'


def illustrative_badge(text: str = "Illustrative") -> str:
    return f'<span class="badge badge-illus">{h(text)}</span>'


def tool_based_pill() -> str:
    return '<span class="badge badge-tool">Tool-based link</span>'


def aside_heading(title_html: str, badge_html: str = "") -> str:
    badge = f'<p class="aside-badge">{badge_html}</p>' if badge_html else ""
    return f'<h3 class="aside-h">{title_html}</h3>{badge}'


def ext_link(ctx: Ctx, url: str, label: str) -> str:
    return (f'<a class="ext" href="{h(url)}" rel="noopener">{h(label)}'
            f'{ctx.icon("i-ext", "ico ico-ext")}<span class="sr-only"> (external site)</span></a>')


def page_head(ctx: Ctx, *, model: str, crumbs_items: list, eyebrow_text: str, title: str,
              lede_html: str = "", meta_html: str = "", strip_html: str = "") -> str:
    lede = f'<div class="lede">{lede_html}</div>' if lede_html else ""
    meta = f'<div class="meta-row">{meta_html}</div>' if meta_html else ""
    return (f'<div class="page-head page-head-{model}"><div class="wrap">'
            f'{crumbs(ctx, crumbs_items)}{eyebrow(ctx, model, eyebrow_text)}'
            f'<h1>{h(title)}</h1>{lede}{meta}{strip_html}</div></div>')


def pager(ctx: Ctx, label: str, prev: tuple | None, nxt: tuple | None) -> str:
    parts = []
    if prev:
        parts.append(f'<a class="pager-link pager-prev" rel="prev" href="{h(ctx.href(prev[1]))}">'
                     f'<span class="pager-dir">Previous<span class="sr-only">: </span></span><span class="pager-t">{h(prev[0])}</span></a>')
    else:
        parts.append('<span class="pager-link pager-empty"></span>')
    if nxt:
        parts.append(f'<a class="pager-link pager-next" rel="next" href="{h(ctx.href(nxt[1]))}">'
                     f'<span class="pager-dir">Next<span class="sr-only">: </span></span><span class="pager-t">{h(nxt[0])}</span></a>')
    return f'<nav class="pager" aria-label="{h(label)}">{"".join(parts)}</nav>'


def entity(head_html: str, main_html: str, aside_html: str, pager_html: str = "") -> str:
    aside = (f'<aside class="entity-aside" aria-labelledby="conn-h"><h2 id="conn-h" class="aside-title">Connections</h2>'
             f'{aside_html}</aside>') if aside_html else ""
    grid = "entity-grid" if aside_html else "entity-grid entity-grid-single"
    return (f'{head_html}<div class="wrap"><div class="{grid}"><div class="entity-main">{main_html}</div>{aside}</div>'
            f'{pager_html}</div>')


# ---- level meter: one drawing of L1–L5 used everywhere ---------------------------

def level_meter(level: int | None = None, today: int | None = None, target: int | None = None,
                label: str = "", size: str = "") -> str:
    """Five segments. ``level`` fills 1..level. ``today``/``target`` draw a move:
    filled up to today, hatched from today to target."""
    segs = []
    for n in range(1, 6):
        if today is not None and target is not None:
            state = "is-fill" if n <= today else ("is-gain" if n <= target else "")
        else:
            state = "is-fill" if level is not None and n <= level else ""
        segs.append(f'<span class="mseg {state}"></span>')
    if not label:
        label = (f"from L{today} to L{target} of 5" if today is not None else f"L{level} of 5")
    cls = f"meter {size}".strip()
    return f'<span class="{cls}" role="img" aria-label="{h(label)}">{"".join(segs)}</span>'


# ---- position strips ------------------------------------------------------------

def _strip(ctx: Ctx, model: str, label: str, groups: list, compact: bool, extra_cls: str = "") -> str:
    """groups: [(group_label, group_href, [(n_label, name, href, state)])]; state: "current" | "on" | "also" | ""."""
    gs = []
    for glabel, ghref, cells in groups:
        lis = []
        for n_label, name, href, state in cells:
            cur = ' aria-current="page"' if state == "current" else ""
            cls = "cell" + (f" is-{state}" if state in ("on", "also") else "")
            note = {"on": " (anchored here)", "also": " (also touches)"}.get(state, "")
            lis.append(f'<li><a class="{cls}" href="{h(ctx.href(href))}"{cur}>'
                       f'<span class="cell-n" aria-hidden="true">{h(n_label)}</span>'
                       f'<span class="cell-name">{h(name)}{h(note)}</span></a></li>')
        gname = ctx.a(ghref, h(glabel), cls="strip-group-name") if ghref else f'<span class="strip-group-name">{h(glabel)}</span>'
        gs.append(f'<li class="strip-group w-{min(len(cells), 9)}">{gname}<ol class="strip-cells">{"".join(lis)}</ol></li>')
    cls = f"strip strip-{model}" + (" strip-compact" if compact else "") + (f" {extra_cls}" if extra_cls else "")
    return f'<nav class="{cls}" aria-label="{h(label)}" data-strip><ol class="strip-groups">{"".join(gs)}</ol></nav>'


def stage_strip(ctx: Ctx, current: str | None = None, compact: bool = True, on: tuple = (), also: tuple = ()) -> str:
    s = ctx.site
    groups = []
    for t in s.tiers:
        cells = []
        for sid in t["stages"]:
            st = s.stage_by_id[sid]
            state = "current" if sid == current else "on" if sid in on else "also" if sid in also else ""
            cells.append((str(st["order"]), st["display_name"], s.u_stage(sid), state))
        groups.append((t["name"], s.u_tier(t["id"]), cells))
    return _strip(ctx, "where", "Substeps of the value chain", groups, compact)


def subarea_strip(ctx: Ctx, current: str | None = None) -> str:
    s = ctx.site
    groups = []
    for d in s.comp["domains"]:
        cells = [(f'{d["order"]}.{i}', sa["name"], s.u_sub(sa["id"]), "current" if sa["id"] == current else "")
                 for i, sa in enumerate(d["subareas"], start=1)]
        groups.append((d["name"], s.u_domain(d["id"]), cells))
    return _strip(ctx, "what", "Sub-areas of the competence model", groups, True)


def how_strip(ctx: Ctx, current: str | None = None) -> str:
    s = ctx.site
    cs = [(c["name"], c["name"], s.u_c4(c["id"]), "current" if c["id"] == current else "") for c in s.ped["cs"]]
    ts = [(t["name"].split(" ")[0], t["name"], s.u_trump(t["id"]), "current" if t["id"] == current else "") for t in s.ped["trumps"]]
    return _strip(ctx, "how", "Parts of the pedagogic practices",
                  [("4Cs", "how/#four-cs", cs), ("Six Trumps", "how/#six-trumps", ts)], True, "strip-words")


# ---- competence -------------------------------------------------------------------

def level_sentence(site, lv: dict) -> str:
    if lv["state"] == "na":
        note = f" {inline_md(lv['text'])}" if lv["text"] else ""
        return f'<p class="na"><span class="na-label">Does not apply at this level.</span>{note}</p>'
    if lv["state"] == "missing":
        return '<p class="na"><span class="na-label">No indicator written yet.</span></p>'
    return f"<p>{inline_md(lv['text'])}</p>"


def ladder(ctx: Ctx, comp: dict) -> str:
    s = ctx.site
    markers: dict[int, list] = {}
    for ex, t in s.comp_examples.get((comp["subarea"], comp["slug"]), []):
        markers.setdefault(t["today"], []).append(("today", ex))
        markers.setdefault(t["target"], []).append(("target", ex))
    rungs = []
    for lv in comp["levels"]:
        n = lv["n"]
        name = s.comp["levels"][n - 1]["name"]
        tag = '<span class="rung-target">Target working level</span>' if n == 3 else ""
        mk = ""
        if n in markers:
            items = []
            for kind, ex in markers[n]:
                word = "Illustrative start" if kind == "today" else "Illustrative target"
                items.append(f'<li class="marker marker-{kind} exk-{ex["kind"]}"><span class="marker-dot" aria-hidden="true"></span>'
                             f'{word}: {ctx.a(s.u_example(ex["id"]), h(ex["short_name"]))}</li>')
            mk = f'<ul class="markers">{"".join(items)}</ul>'
        cls = "rung" + (" rung-na" if lv["state"] != "ok" else "") + (" rung-target-level" if n == 3 else "")
        name_link = ctx.a(s.u_level(n), f'{h(name)}<span class="sr-only">: what L{n} means for any competency</span>', cls="rung-name")
        rungs.append(
            f'<li class="{cls}" id="l{n}" data-level="{n}">'
            f'<div class="rung-level"><span class="rung-n">L{n}</span>{name_link}{level_meter(n)}{tag}</div>'
            f'<div class="rung-body">{level_sentence(s, lv)}{mk}</div></li>'
        )
    return (f'<ol class="ladder" aria-label="Levels for {h(comp["name"])}">{"".join(rungs)}</ol>'
            f'<p class="hint">Level names link to what that level means for any competency.</p>')


def compare_panel(ctx: Ctx, heading_level: int = 2, intro: str = "") -> str:
    """Interactive L-from → L-to comparison built on the rubric's four dimensions.

    Rendered hidden; site.js reveals and drives it. Without JavaScript the
    static rubric on the levels page is the fallback.
    """
    s = ctx.site
    r = s.rubric
    cid = uid("cmp")
    hl = f"h{heading_level}"

    def radios(name: str, legend: str, checked: int) -> str:
        opts = "".join(
            f'<label class="seg"><input type="radio" name="{cid}-{name}" id="{cid}-{name}-{n}" value="{n}"'
            f'{" checked" if n == checked else ""}><span>L{n}</span></label>'
            for n in range(1, 6)
        )
        return f'<fieldset class="segmented"><legend>{legend}</legend><div class="seg-row">{opts}</div></fieldset>'

    dims = []
    for d in r["dimensions"]:
        cells = "".join(f'<span class="cmp-cell" data-l="{i}">{h(c)}</span>' for i, c in enumerate(d["cells"], start=1))
        dims.append(f'<div class="cmp-dim"><dt>{h(d["name"])}</dt><dd><span class="cmp-from">{cells}</span>'
                    f'<span class="cmp-arrow" aria-hidden="true">→</span><span class="cmp-to">{cells}</span></dd></div>')
    gates = "".join(
        f'<div class="cmp-gate" data-l="{lv["n"]}"><p><strong>At L{lv["n"]}, cannot yet{(" (" + h(lv["cannot_qualifier"]) + ")") if lv["cannot_qualifier"] else ""}:</strong> {inline_md(lv["cannot"])}</p>'
        + (f'<p><strong>Signal for moving up to L{lv["n"] + 1}:</strong> {inline_md(lv["promotion"])}</p>' if lv["promotion"] else "")
        + "</div>"
        for lv in r["levels"] if lv["cannot"] or lv["promotion"]
    )
    intro_html = f'<p class="cmp-intro">{intro}</p>' if intro else ""
    return (f'<section class="compare" data-compare hidden aria-labelledby="{cid}-h">'
            f'<{hl} id="{cid}-h" class="section-title">Compare two levels</{hl}>{intro_html}'
            f'<div class="cmp-controls">{radios("from", "From", 2)}{radios("to", "To", 3)}</div>'
            f'<p class="cmp-status" aria-live="polite"></p>'
            f'<dl class="cmp-dims">{"".join(dims)}</dl><div class="cmp-gates">{gates}</div></section>')


# ---- examples ---------------------------------------------------------------------

def example_callout(ctx: Ctx, rows: list) -> str:
    """rows: [(example, role_html)]"""
    if not rows:
        return ""
    s = ctx.site
    lis = "".join(
        f'<li class="exref exk-{ex["kind"]}"><span class="exref-kind">{h(ex["kind_label"])}</span>'
        f'{ctx.a(s.u_example(ex["id"]), h(ex["short_name"]), cls="exref-link")}'
        f'<span class="exref-role">{role}</span></li>'
        for ex, role in rows
    )
    return (f'<section class="aside-block callout-ex">{aside_heading("Used in our examples", illustrative_badge())}'
            f'<ul class="exrefs">{lis}</ul></section>')


def level_move(site, today: int, target: int) -> str:
    return (f'<span class="move"><span class="move-from">L{today}</span><span class="sr-only"> to </span>'
            f'<span class="move-arrow" aria-hidden="true">→</span><span class="move-to">L{target}</span></span>')


# ---- tools -------------------------------------------------------------------------

def tool_names(ctx: Ctx, tools: list, limit: int = 6) -> str:
    s = ctx.site
    seen, out = set(), []
    for t in tools:
        if t["slug"] in seen:
            continue
        seen.add(t["slug"])
        out.append(ctx.a(s.u_tool(t["slug"]), h(t["name"]), cls="tool-link"))
    if len(out) <= limit:
        return ", ".join(out)
    rest = ", ".join(out[limit:])
    return (", ".join(out[:limit])
            + f'<details class="more-tools"><summary>and {len(out) - limit} more</summary>{rest}</details>')


def count_tools(tools: list) -> str:
    n = len({t["slug"] for t in tools})
    return f'{n} tool{"s" if n != 1 else ""} or method{"s" if n != 1 else ""}'


def linkify_tools(ctx: Ctx, text: str, tools: list) -> str:
    """Escape ``text`` and link the first mention of each crosswalk tool (or alias)."""
    s = ctx.site
    names = []
    for t in tools:
        for n in [t["name"], *t["aliases"]]:
            if len(n) >= 2:
                names.append((n, t))
    names.sort(key=lambda p: -len(p[0]))
    spans: list[tuple[int, int, dict]] = []
    used: set[str] = set()
    for n, t in names:
        if t["slug"] in used:
            continue
        m = re.search(rf"(?<![\w-]){re.escape(n)}(?![\w-])", text)
        if not m or any(a < m.end() and m.start() < b for a, b, _ in spans):
            continue
        spans.append((m.start(), m.end(), t))
        used.add(t["slug"])
    spans.sort()
    out, pos = [], 0
    for a, b, t in spans:
        out.append(h(text[pos:a]))
        out.append(ctx.a(s.u_tool(t["slug"]), h(text[a:b]), cls="tool-link"))
        pos = b
    out.append(h(text[pos:]))
    return "".join(out)
