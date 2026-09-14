"""Explorer pages for the three models, the level rubric and the tool crosswalk."""
from __future__ import annotations

import re

from ..text import h, inline_md, strip_md
from . import components as C
from .core import Ctx, Page
from .copy import copy
from .svg import four_cs_cycle


def _entry(t, k, m, u, p="", x="", s="", b=""):
    return {"t": t, "k": k, "m": m, "u": u, "p": p, "x": x, "s": s, "b": b}


def _scale_label(lv) -> str:
    return f'<span class="scale-n">L{lv["n"]}</span><span class="scale-name">{h(lv["name"])}</span>'


def _tiers_label(site, sid):
    st = site.stage_by_id[sid]
    return f"{st['tier']} · substep {st['order']} of {len(site.stages)}"


# ==== WHERE ======================================================================

def where_overview(site) -> Page:
    path = "where/"
    ctx = Ctx(site, path)
    meta = (C.chip(f"{len(site.tiers)} steps · {len(site.stages)} substeps") + C.chip(site.vc["version"], "chip-mono")
            + C.draft_badge(site.vc["status"]))
    head = C.page_head(ctx, model="where", crumbs_items=[("Start", ""), ("Where", None)],
                       eyebrow_text="Where · the first question", title="Pharma Value Chain",
                       lede_html=copy(ctx, "where-intro.html"), meta_html=meta)
    tiers = []
    for t in site.tiers:
        cards = []
        for sid in t["stages"]:
            st = site.stage_by_id[sid]
            n_methods = sum(len(g["items"]) for g in st["method_groups"])
            n_tools = len({tool["slug"] for tool, _ in site.stage_tools[sid]})
            ex = site.stage_examples[sid]
            ex_note = f'<span class="card-ex">Used in {len(ex)} example{"s" if len(ex) != 1 else ""} (illustrative)</span>' if ex else ""
            tool_note = f" · {n_tools} in the crosswalk" if n_tools else ""
            cards.append(
                f'<li class="card card-where"><span class="card-n">{st["order"]}</span>'
                f'<h3 class="card-title">{ctx.a(site.u_stage(sid), h(st["display_name"]), cls="card-link")}</h3>'
                f'<p class="card-q">{h(st["primary_question"])}</p>'
                f'<p class="card-meta"><span>{len(st["key_questions"])} key questions · {n_methods} methods and tools{tool_note}</span>{ex_note}</p></li>'
            )
        tiers.append(f'<section class="tier-section" id="{t["id"]}" aria-labelledby="{t["id"]}-h">'
                     f'<h2 id="{t["id"]}-h" class="section-title"><span class="step-num">Step {t["step"]}</span> {h(t["name"])}</h2>'
                     f'<ol class="cards cards-where">{"".join(cards)}</ol></section>')
    body = f'{head}<div class="wrap">{copy(ctx, "where-read.html")}{"".join(tiers)}</div>'
    search = [_entry("Pharma Value Chain", "model", "where", path, "Where",
                     "The drug pipeline in 3 steps and 14 substeps", "value chain pipeline where")]
    for t in site.tiers:
        search.append(_entry(t["name"], "tier", "where", site.u_tier(t["id"]), "Where", f"Step {t['step']} of the value chain",
                             "tier step", " ".join(site.stage_by_id[s]["display_name"] for s in t["stages"])))
    return Page(path, "Pharma Value Chain", "where", body,
                description="The Pharma Value Chain Model: three steps and fourteen substeps of drug development.", search=search)


def stage_page(site, sid: str) -> Page:
    path = site.u_stage(sid)
    ctx = Ctx(site, path)
    st = site.stage_by_id[sid]
    idx = [s["id"] for s in site.stages].index(sid)
    tools_here = [tool for tool, _ in site.stage_tools[sid]]

    aliases = (C.chip("Also called: " + ", ".join(st["aliases"]), "chip-soft")) if st["aliases"] else ""
    meta = C.chip(_tiers_label(site, sid)) + aliases + C.draft_badge(site.vc["status"])
    head = C.page_head(ctx, model="where",
                       crumbs_items=[("Start", ""), ("Where", "where/"), (st["tier"], site.u_tier(st["tier_id"])), (st["display_name"], None)],
                       eyebrow_text=f"Where · {st['tier']}", title=st["display_name"], meta_html=meta,
                       strip_html=C.stage_strip(ctx, sid))

    notes = "".join(f'<p class="scope-note">{inline_md(n)}</p>' for n in st["notes"])
    kq = "".join(f"<li>{inline_md(q)}</li>" for q in st["key_questions"])
    groups = []
    for g in st["method_groups"]:
        title = f'<h3 class="method-group">{h(g["title"])}</h3>' if g["title"] else ""
        gnotes = "".join(f'<p class="group-note">{inline_md(n)}</p>' for n in g["notes"])
        items = []
        for it in g["items"]:
            if it["rest"]:
                txt = f'<span class="m-lead">{C.linkify_tools(ctx, it["lead"], tools_here)}</span>: {C.linkify_tools(ctx, it["rest"], tools_here)}'
            else:
                txt = C.linkify_tools(ctx, it["lead"], tools_here)
            flag = f' <span class="badge badge-flag">Beyond reference: {h(it["flag"])}</span>' if it["flag"] else ""
            items.append(f"<li>{txt}{flag}</li>")
        groups.append(f'{title}{gnotes}<ul class="methods">{"".join(items)}</ul>')

    main = (f'<section class="primary-q" aria-labelledby="pq-h"><h2 id="pq-h" class="kicker">Primary data-science question</h2>'
            f'<p class="pull">{h(st["primary_question"])}</p></section>{notes}'
            f'<section aria-labelledby="kq-h"><h2 id="kq-h" class="section-title">Key questions</h2><ul class="kq">{kq}</ul></section>'
            f'<section aria-labelledby="mt-h"><h2 id="mt-h" class="section-title">Established methods and tools</h2>'
            f'<p class="hint">Linked names are in the tool crosswalk.</p>{"".join(groups)}</section>')

    # aside
    ex_rows = [(ex, h(role) + ": " + h(ex["short"]["anchor"])) for ex, role in site.stage_examples[sid]]
    aside = C.example_callout(ctx, ex_rows)
    subs = site.stage_subs[sid]
    if subs:
        blocks = []
        for did, by_sub in subs.items():
            d = site.domain_by_id[did]
            lis = []
            for said, tools in by_sub.items():
                n = len({t["slug"] for t in tools})
                label = ctx.a(site.u_sub(said), h(site.sub_by_id[said]["name"])) if said else f'<span class="muted">{h(d["name"])}, no sub-area given</span>'
                lis.append(f'<li>{label}<div class="via">via {C.count_tools(tools)}: {C.tool_names(ctx, tools, 4)}</div></li>')
            blocks.append(f'<li class="conn-domain"><span class="conn-domain-name">{ctx.a(site.u_domain(did), h(d["name"]))}</span><ul>{"".join(lis)}</ul></li>')
        conn = f'<ul class="conn-list">{"".join(blocks)}</ul>'
    else:
        conn = '<p class="empty">No tools in the crosswalk link this substep to a competence sub-area yet.</p>'
    aside += (f'<section class="aside-block">{C.aside_heading("Competence sub-areas that share tools", C.tool_based_pill())}'
              f'<p class="aside-note">These links come from tools used both here and in a sub-area. They are not a list of required competencies: CPDSE sets targets per course or workshop.</p>{conn}</section>')

    prev = (site.stages[idx - 1]["display_name"], site.u_stage(site.stages[idx - 1]["id"])) if idx > 0 else None
    nxt = (site.stages[idx + 1]["display_name"], site.u_stage(site.stages[idx + 1]["id"])) if idx < len(site.stages) - 1 else None
    body = C.entity(head, main, aside, C.pager(ctx, "Previous and next substep", prev, nxt))

    methods_text = " ".join(it["text"] for g in st["method_groups"] for it in g["items"])
    search = [_entry(st["display_name"], "stage", "where", path, f"Where › {st['tier']}", st["primary_question"],
                     " ".join(st["aliases"] + [f"substep {st['order']}"]),
                     " ".join(st["key_questions"]) + " " + methods_text)]
    return Page(path, st["display_name"], "where", body, description=st["primary_question"], search=search)


# ==== WHAT =======================================================================

def what_overview(site) -> Page:
    path = "what/"
    ctx = Ctx(site, path)
    c = site.counts()
    meta = (C.chip(f'{c["domains"]} domains · {c["subareas"]} sub-areas · {c["competencies"]} competencies')
            + C.chip(f'Last changed {site.prov.files["competence"]["date"]}', "chip-soft"))
    head = C.page_head(ctx, model="what", crumbs_items=[("Start", ""), ("What", None)],
                       eyebrow_text="What · the second question", title="PDS Competence Model",
                       lede_html=copy(ctx, "what-intro.html"), meta_html=meta)
    scale = "".join(
        f'<li class="scale-step{" is-target" if lv["n"] == 3 else ""}">{ctx.a(site.u_level(lv["n"]), _scale_label(lv), cls="scale-link")}'
        f'{C.level_meter(lv["n"])}<span class="scale-short">{h(lv["short"])}</span></li>'
        for lv in site.comp["levels"]
    )
    scale_html = (f'<section class="scale-section" aria-labelledby="scale-h"><h2 id="scale-h" class="section-title">One scale for every competency</h2>'
                  f'<ol class="scale">{scale}</ol><p class="hint">{ctx.a("what/levels/", "Read the full level rubric and compare levels")}. '
                  f'L3 is the target working level, but nobody is expected to reach L3 in every competency.</p></section>')
    names_count: dict = {}
    for cp in site.comp["competencies"]:
        names_count[cp["name"].lower()] = names_count.get(cp["name"].lower(), 0) + 1
    doms = []
    for d in site.comp["domains"]:
        cards = []
        for sa in d["subareas"]:
            comps = "".join(f'<li>{ctx.a(site.u_comp(sa["id"], cp["slug"]), h(cp["name"]) + (f"<span class=sr-only> ({h(sa[chr(110) + chr(97) + chr(109) + chr(101)])})</span>" if names_count[cp["name"].lower()] > 1 else ""))}</li>' for cp in sa["competencies"])
            n_st = len(site.sub_stages[sa["id"]])
            ex = site.sub_examples[sa["id"]]
            ex_note = f' · used in {len(ex)} example{"s" if len(ex) != 1 else ""} (illustrative)' if ex else ""
            st_note = f' · tools shared with {n_st} substep{"s" if n_st != 1 else ""}' if n_st else ""
            cards.append(f'<li class="card card-what"><span class="card-n">{d["order"]}.{d["subareas"].index(sa) + 1}</span><h3 class="card-title">{ctx.a(site.u_sub(sa["id"]), h(sa["name"]), cls="card-link")}</h3>'
                         f'<p class="card-meta">{len(sa["competencies"])} competencies{st_note}{ex_note}</p>'
                         f'<ul class="card-comps">{comps}</ul></li>')
        doms.append(f'<section class="domain-section" id="{d["id"]}" aria-labelledby="{d["id"]}-h">'
                    f'<h2 id="{d["id"]}-h" class="section-title"><span class="step-num">Domain {d["order"]}</span> {h(d["name"])}</h2>'
                    f'<ul class="cards cards-what">{"".join(cards)}</ul></section>')
    body = f'{head}<div class="wrap">{scale_html}{"".join(doms)}</div>'
    search = [_entry("PDS Competence Model", "model", "what", path, "What", "7 domains, 30 sub-areas, 123 competencies, rated L1–L5",
                     "competence competency model what pds")]
    for d in site.comp["domains"]:
        search.append(_entry(d["name"], "domain", "what", site.u_domain(d["id"]), "What", f"Domain {d['order']} of the competence model",
                             "domain", " ".join(sa["name"] for sa in d["subareas"])))
    return Page(path, "PDS Competence Model", "what", body,
                description="The PDS Competence Model: domains, sub-areas and competencies rated from L1 to L5.", search=search)


def subarea_page(site, said: str) -> Page:
    path = site.u_sub(said)
    ctx = Ctx(site, path)
    sa = site.sub_by_id[said]
    d = site.domain_by_id[sa["domain"]]
    subs = site.comp["subareas"]
    idx = [x["id"] for x in subs].index(said)
    head = C.page_head(ctx, model="what",
                       crumbs_items=[("Start", ""), ("What", "what/"), (d["name"], site.u_domain(d["id"])), (sa["name"], None)],
                       eyebrow_text=f"What · {d['name']}", title=sa["name"],
                       meta_html=C.chip(f'{len(sa["competencies"])} competencies') + C.chip(f'Sub-area {d["order"]}.{d["subareas"].index(sa) + 1}', "chip-soft"),
                       strip_html=C.subarea_strip(ctx, said))

    stack_text = re.sub(r"\(\s+`", "(`", re.sub(r"`\s+([,)])", r"`\1", sa["stack"]))
    stack = f'<section aria-labelledby="st-h"><h2 id="st-h" class="section-title">Typical stack</h2><p class="stack">{inline_md(stack_text)}</p></section>' if sa["stack"] else ""
    ex_items = []
    for ex in sa["examples"]:
        tags = []
        for t in ex["tags"]:
            label = f'{h(t["name"])} <span class="lvl">L{t["level"]}</span>'
            if t["slug"]:
                tags.append(ctx.a(site.u_comp(said, t["slug"]) + f'#l{t["level"]}', label, cls="tag"))
            else:
                tags.append(f'<span class="tag tag-unresolved">{label}</span>')
        ex_items.append(f'<li><span class="px-text">{inline_md(ex["text"])}</span><span class="tags">{"".join(tags)}</span></li>')
    pharma = (f'<section aria-labelledby="px-h"><h2 id="px-h" class="section-title">Pharma examples</h2>'
              f'<p class="hint">Each example is tagged with the competency and level it shows. Tags open that level.</p>'
              f'<ul class="pharma-ex">{"".join(ex_items)}</ul></section>') if ex_items else ""

    radio_id = C.uid("focus")
    radios = "".join(f'<label class="seg"><input type="radio" name="{radio_id}" id="{radio_id}-{n}" value="{n}"{" checked" if n == 3 else ""}>'
                     f'<span>L{n}</span></label>' for n in range(1, 6))
    comps = []
    for cp in sa["competencies"]:
        sentences = "".join(
            f'<div class="focus-level" data-l="{lv["n"]}"{"" if lv["n"] == 3 else " hidden"}>'
            f'<span class="focus-tag">L{lv["n"]} {h(site.comp["levels"][lv["n"] - 1]["name"])}</span>{C.level_sentence(site, lv)}</div>'
            for lv in cp["levels"]
        )
        comps.append(f'<li class="comp-item"><h3 class="comp-name">{ctx.a(site.u_comp(said, cp["slug"]), h(cp["name"]))}'
                     f'<span class="comp-id">{h(cp["id"])}</span></h3>{sentences}</li>')
    comp_html = (f'<section aria-labelledby="cp-h" data-level-focus><div class="section-bar"><h2 id="cp-h" class="section-title">Competencies</h2>'
                 f'<fieldset class="segmented focus-control" hidden><legend>Show indicators at</legend><div class="seg-row">{radios}</div></fieldset>'
                 f'<p class="hint" data-focus-note>Showing the L3 indicator for each competency. Open a competency to see all five levels.</p></div>'
                 f'<ul class="comp-list">{"".join(comps)}</ul></section>')
    main = comp_html + pharma + stack

    ex_rows = []
    for ex, t in site.sub_examples[said]:
        cp = site.comp_by_key[(said, t["slug"])]
        ex_rows.append((ex, f'{h(cp["name"])}: {C.level_move(site, t["today"], t["target"])}'))
    aside = C.example_callout(ctx, ex_rows)
    stages = site.sub_stages[said]
    if stages:
        lis = "".join(
            f'<li>{ctx.a(site.u_stage(sid), h(str(site.stage_by_id[sid]["order"]) + ". " + site.stage_by_id[sid]["display_name"]))}'
            f'<div class="via">via {C.count_tools(tools)}: {C.tool_names(ctx, tools, 4)}</div></li>'
            for sid, tools in stages.items()
        )
        conn = f'<ul class="conn-flat">{lis}</ul>'
    else:
        conn = '<p class="empty">No tools in the crosswalk link this sub-area to a value-chain substep yet.</p>'
    aside += (f'<section class="aside-block">{C.aside_heading("Value-chain substeps that share tools", C.tool_based_pill())}'
              f'<p class="aside-note">Tools used in this sub-area also appear in these substeps. That shows overlap, not a requirement.</p>{conn}</section>')

    prev = (subs[idx - 1]["name"], site.u_sub(subs[idx - 1]["id"])) if idx > 0 else None
    nxt = (subs[idx + 1]["name"], site.u_sub(subs[idx + 1]["id"])) if idx < len(subs) - 1 else None
    body = C.entity(head, main, aside, C.pager(ctx, "Previous and next sub-area", prev, nxt))
    search = [_entry(sa["name"], "subarea", "what", path, f"What › {d['name']}",
                     f'{len(sa["competencies"])} competencies. Typical stack: {strip_md(sa["stack"])}'[:180],
                     "sub-area", strip_md(sa["stack"]) + " " + " ".join(e["text"] for e in sa["examples"]))]
    return Page(path, sa["name"], "what", body, description=f"{sa['name']}: competencies, typical stack and pharma examples.", search=search)


def competency_page(site, comp: dict) -> Page:
    said, slug = comp["subarea"], comp["slug"]
    path = site.u_comp(said, slug)
    ctx = Ctx(site, path)
    sa = site.sub_by_id[said]
    d = site.domain_by_id[sa["domain"]]
    sib = sa["competencies"]
    idx = [c["slug"] for c in sib].index(slug)
    head = C.page_head(ctx, model="what",
                       crumbs_items=[("Start", ""), ("What", "what/"), (d["name"], site.u_domain(d["id"])),
                                     (sa["name"], site.u_sub(said)), (comp["name"], None)],
                       eyebrow_text=f"What · {sa['name']}", title=comp["name"],
                       meta_html=C.chip(f"Competency {comp['id']}", "chip-mono") + C.chip(f"{d['name']} › {sa['name']}", "chip-soft"),
                       strip_html=C.subarea_strip(ctx, said))
    ladder = (f'<section aria-labelledby="lv-h"><h2 id="lv-h" class="section-title">What each level looks like</h2>'
              f'{C.ladder(ctx, comp)}</section>')
    compare = C.compare_panel(ctx, 2, "Pick two levels to see how the general rubric changes between them. The levels above stay in view.")
    pex = ""
    if comp["examples"]:
        lis = "".join(f'<li><span class="px-text">{inline_md(e["text"])}</span> {ctx.a("#l" + str(e["level"]), "L" + str(e["level"]), cls="tag")}</li>'
                      for e in comp["examples"])
        pex = (f'<section aria-labelledby="px-h"><h2 id="px-h" class="section-title">In pharma practice</h2>'
               f'<p class="hint">From the pharma examples of {ctx.a(site.u_sub(said), h(sa["name"]))}.</p><ul class="pharma-ex">{lis}</ul></section>')
    twins = [c for c in site.comp["competencies"] if c["name"].lower() == comp["name"].lower() and c is not comp]
    twin_note = ""
    if twins:
        links = ", ".join(ctx.a(site.u_comp(c["subarea"], c["slug"]), h(site.sub_by_id[c["subarea"]]["name"] + " › " + c["name"])) for c in twins)
        twin_note = f'<p class="twin-note">This is the competency in {h(sa["name"])}. A competency with the same name also exists in {links}.</p>'
    main = twin_note + ladder + compare + pex

    rows = [(ex, f'{C.level_move(site, t["today"], t["target"])} {h(t["why"])}') for ex, t in site.comp_examples.get((said, slug), [])]
    aside = C.example_callout(ctx, rows)
    sibs = "".join(f'<li>{ctx.a(site.u_comp(said, c["slug"]), h(c["name"]))}</li>' if c["slug"] != slug
                   else f'<li><span aria-current="page">{h(c["name"])}</span></li>' for c in sib)
    aside += f'<section class="aside-block"><h3 class="aside-h">In {ctx.a(site.u_sub(said), h(sa["name"]))}</h3><ul class="conn-flat sibs">{sibs}</ul></section>'
    stages = site.sub_stages[said]
    if stages:
        lis = "".join(f'<li>{ctx.a(site.u_stage(sid), h(str(site.stage_by_id[sid]["order"]) + ". " + site.stage_by_id[sid]["display_name"]))}</li>'
                      for sid in stages)
        conn = f'<ul class="conn-flat">{lis}</ul>'
    else:
        conn = '<p class="empty">No tools in the crosswalk link this sub-area to a substep yet.</p>'
    aside += (f'<section class="aside-block">{C.aside_heading("Substeps that share tools with this sub-area", C.tool_based_pill())}'
              f'<p class="aside-note">The crosswalk links tools to sub-areas, not to single competencies.</p>{conn}</section>')

    prev = (sib[idx - 1]["name"], site.u_comp(said, sib[idx - 1]["slug"])) if idx > 0 else None
    nxt = (sib[idx + 1]["name"], site.u_comp(said, sib[idx + 1]["slug"])) if idx < len(sib) - 1 else None
    body = C.entity(head, main, aside, C.pager(ctx, f"Previous and next competency in {sa['name']}", prev, nxt))
    l3 = comp["levels"][2]
    twins = [c for c in site.comp["competencies"] if c["name"].lower() == comp["name"].lower() and c is not comp]
    page_title = f"{comp['name']} ({sa['name']})" if twins else comp["name"]
    search = [_entry(page_title, "competency", "what", path, f"What › {d['name']} › {sa['name']}",
                     f"L3: {strip_md(l3['text'])}" if l3["state"] == "ok" else "",
                     comp["id"], " ".join(strip_md(l["text"]) for l in comp["levels"]))]
    return Page(path, page_title, "what", body,
                description=f"{comp['name']} ({sa['name']}): what L1 to L5 look like.", search=search)


def levels_page(site) -> Page:
    path = "what/levels/"
    ctx = Ctx(site, path)
    r = site.rubric
    head = C.page_head(ctx, model="what", crumbs_items=[("Start", ""), ("What", "what/"), ("Levels", None)],
                       eyebrow_text="What · the level rubric", title="Levels L1 to L5",
                       lede_html=copy(ctx, "levels-intro.html"))
    th = "".join(f'<th scope="col" class="{"is-target" if n == 3 else ""}">{ctx.a("#l" + str(n), "L" + str(n) + " " + h(site.comp["levels"][n - 1]["name"]))}</th>' for n in range(1, 6))
    rows = "".join(f'<tr><th scope="row">{h(dm["name"])}</th>' + "".join(
        f'<td class="{"is-target" if i == 3 else ""}">{h(c)}</td>' for i, c in enumerate(dm["cells"], start=1)) + "</tr>"
        for dm in r["dimensions"])
    table = (f'<section aria-labelledby="dims-h"><h2 id="dims-h" class="section-title">Four dimensions that rise together</h2>'
             f'<div class="table-wrap" role="region" aria-labelledby="dims-h" tabindex="0"><table class="dims">'
             f'<thead><tr><th scope="col">Dimension</th>{th}</tr></thead><tbody>{rows}</tbody></table></div></section>')
    compare = C.compare_panel(ctx, 2, "Choose any two levels. Each dimension shows the change, followed by what holds a person back and the signal for moving up.")
    fallback = []
    for lv in r["levels"][:-1]:
        nxt = r["levels"][lv["n"]]
        dims = "".join(f'<li><strong>{h(dm["name"])}:</strong> {h(dm["cells"][lv["n"] - 1])} → {h(dm["cells"][lv["n"]])}</li>' for dm in r["dimensions"])
        fallback.append(f'<details class="transition" id="from-{lv["n"]}-to-{nxt["n"]}" open><summary>From L{lv["n"]} {h(lv["name"])} to L{nxt["n"]} {h(nxt["name"])}</summary>'
                        f'<ul>{dims}</ul><p><strong>Signal for moving up:</strong> {inline_md(lv["promotion"])}</p></details>')
    noscript = (f'<section class="compare-fallback" data-compare-fallback aria-labelledby="tr-h"><h2 id="tr-h" class="section-title">Moving up one level</h2>'
                f'{"".join(fallback)}</section>')
    levels = []
    for lv in r["levels"]:
        can = "".join(f"<li>{inline_md(x)}</li>" for x in lv["can"])
        notes = "".join(f'<p class="level-note">{inline_md(n)}</p>' for n in lv["notes"])
        cannot = (f'<p><strong>Cannot yet{(" (" + h(lv["cannot_qualifier"]) + ")") if lv["cannot_qualifier"] else ""}:</strong> {inline_md(lv["cannot"])}</p>'
                  if lv["cannot"] else "")
        promo = f'<p><strong>Signal for moving up to L{lv["n"] + 1}:</strong> {inline_md(lv["promotion"])}</p>' if lv["promotion"] else ""
        examples = site.level_examples[lv["n"]]
        ex_html = ""
        if examples:
            items = "".join(f'<li>{ctx.a(site.u_comp(t["subarea"], t["slug"]) + "#l" + str(lv["n"]), h(site.comp_by_key[(t["subarea"], t["slug"])]["name"]))} '
                            f'in {ctx.a(site.u_example(ex["id"]), h(ex["short_name"]))}</li>' for ex, t in examples)
            ex_html = f'<div class="level-ex"><p class="kicker">Illustrative targets at this level</p><ul>{items}</ul></div>'
        levels.append(f'<section class="level-card{" is-target" if lv["n"] == 3 else ""}" id="l{lv["n"]}" aria-labelledby="l{lv["n"]}-h">'
                      f'<h2 id="l{lv["n"]}-h" class="level-title"><span class="rung-n">L{lv["n"]}</span> {h(lv["name"])} {C.level_meter(lv["n"], size="meter-lg")}</h2>'
                      f'<p class="level-quote">{inline_md(lv["quote"])}</p>{notes}<p class="kicker">A person at L{lv["n"]} can</p><ul class="can">{can}</ul>'
                      f'{cannot}{promo}{ex_html}</section>')
    body = f'{head}<div class="wrap">{table}{compare}{noscript}<div class="levels">{"".join(levels)}</div></div>'
    search = [_entry("Levels L1 to L5", "levels", "what", path, "What", "The behavioural rubric shared by every competency",
                     "rubric levels dimensions autonomy context judgment compare", " ".join(dm["name"] for dm in r["dimensions"]))]
    for lv in r["levels"]:
        search.append(_entry(f"L{lv['n']} {lv['name']}", "level", "what", f"what/levels/#l{lv['n']}", "What › Levels", strip_md(lv["quote"]),
                             f"level {lv['n']}", " ".join(strip_md(x) for x in lv["can"])))
    return Page(path, "Levels L1 to L5", "what", body, description="The L1–L5 rubric: autonomy, context, judgment and effect on others.", search=search)


# ==== HOW ========================================================================

def how_overview(site) -> Page:
    path = "how/"
    ctx = Ctx(site, path)
    p = site.ped
    meta = C.chip("4Cs · Six Trumps") + C.chip(p["version"], "chip-mono") + C.draft_badge(p["status"])
    head = C.page_head(ctx, model="how", crumbs_items=[("Start", ""), ("How", None)],
                       eyebrow_text="How · the third question", title="Pedagogic Practices",
                       lede_html=copy(ctx, "how-intro.html"), meta_html=meta)
    cs = "".join(f'<li class="card card-how"><span class="card-n">{c["n"]}</span><h3 class="card-title">{ctx.a(site.u_c4(c["id"]), h(c["name"]), cls="card-link")}</h3>'
                 f'<p class="card-q">{inline_md(c["body"].split(". ")[0].rstrip(".") + ".")}</p></li>' for c in p["cs"])
    trumps = "".join(f'<li class="card card-how card-trump"><h3 class="card-title">{ctx.a(site.u_trump(t["id"]), h(t["name"]), cls="card-link")}</h3>'
                     f'<p class="card-q">{inline_md(t["body"])}</p></li>' for t in p["trumps"])
    body = (f'{head}<div class="wrap">'
            f'<section id="four-cs" class="how-section" aria-labelledby="fc-h"><div class="how-split"><div>'
            f'<h2 id="fc-h" class="section-title">The 4Cs: a map for any learning block</h2><p class="prose">{inline_md(p["cs_intro"])}</p>'
            f'<ol class="cards cards-how">{cs}</ol></div><figure class="fig">{four_cs_cycle(ctx)}</figure></div></section>'
            f'<section id="six-trumps" class="how-section" aria-labelledby="st-h"><h2 id="st-h" class="section-title">The Six Trumps: a check inside each block</h2>'
            f'<p class="prose">{inline_md(p["trumps_intro"])}</p><ul class="cards cards-trumps">{trumps}</ul></section>'
            f'{copy(ctx, "how-this-site.html")}'

            f'<section class="sources" aria-labelledby="src-h"><h2 id="src-h" class="kicker">Source</h2>'
            f'<p>Both frameworks come from Sharon L. Bowman. The descriptions on this site paraphrase CPDSE\'s reference document; read her books for the originals.</p>'
            f'<ul>{"".join(f"<li>{inline_md(s)}</li>" for s in p["sources"])}</ul></section></div>')
    search = [_entry("Pedagogic Practices", "model", "how", path, "How", "Training from the Back of the Room: the 4Cs and the Six Trumps",
                     "pedagogy how bowman training from the back of the room tbr", strip_md(p["premise"]))]
    return Page(path, "Pedagogic Practices", "how", body,
                description="Pedagogic Practices: the 4Cs and the Six Trumps from Training from the Back of the Room.", search=search)


def _how_used(ctx, rows) -> str:
    s = ctx.site
    return C.example_callout(ctx, [(ex, f'Block {i}: {h(b["title"])} ({b["minutes"]} min)') for ex, b, i in rows])


def c4_page(site, cid: str) -> Page:
    path = site.u_c4(cid)
    ctx = Ctx(site, path)
    c = site.c4_by_id[cid]
    cs = site.ped["cs"]
    idx = [x["id"] for x in cs].index(cid)
    head = C.page_head(ctx, model="how", crumbs_items=[("Start", ""), ("How", "how/"), ("4Cs", "how/#four-cs"), (c["name"], None)],
                       eyebrow_text=f"How · the 4Cs · {c['n']} of 4", title=c["name"],
                       meta_html=C.draft_badge(site.ped["status"]), strip_html=C.how_strip(ctx, cid))
    trumps = "".join(f'<li>{ctx.a(site.u_trump(t["id"]), h(t["name"]))}</li>' for t in site.ped["trumps"])
    blocks = []
    for ex, b, i in site.c4_examples[cid]:
        tr = ", ".join(ctx.a(site.u_trump(x), h(site.trump_by_id[x]["name"])) for x in b["trumps"])
        blocks.append(f'<li class="design-block exk-{ex["kind"]}"><p class="db-meta">{ctx.a(site.u_example(ex["id"]), h(ex["short_name"]))} · block {i} · {b["minutes"]} min</p>'
                      f'<p class="db-title">{h(b["title"])}</p><p>{h(b["activity"])}</p><p class="db-trumps">Trumps used: {tr}</p></li>')
    ex_html = (f'<section aria-labelledby="ib-h"><h2 id="ib-h" class="section-title">In our example designs {C.illustrative_badge()}</h2>'
               f'<ul class="design-blocks">{"".join(blocks)}</ul></section>') if blocks else ""
    main = (f'<p class="pull">{inline_md(c["body"])}</p>'
            f'<section aria-labelledby="eg-h"><h2 id="eg-h" class="kicker">Typical activities</h2><p>{inline_md(c["examples"])}</p></section>'
            f'{ex_html}'
            f'<section aria-labelledby="tc-h"><h2 id="tc-h" class="section-title">Check the block with the Six Trumps</h2>'
            f'<p>The Six Trumps apply inside every block, whichever C it is.</p><ul class="inline-list">{trumps}</ul></section>')
    aside = _how_used(ctx, site.c4_examples[cid])
    aside += f'<section class="aside-block"><h3 class="aside-h">The cycle</h3><figure class="fig fig-small">{four_cs_cycle(ctx, cid, "cyc-a")}</figure></section>'
    prev = (cs[idx - 1]["name"], site.u_c4(cs[idx - 1]["id"])) if idx > 0 else None
    nxt = (cs[idx + 1]["name"], site.u_c4(cs[idx + 1]["id"])) if idx < len(cs) - 1 else None
    body = C.entity(head, main, aside, C.pager(ctx, "Previous and next C", prev, nxt))
    search = [_entry(c["name"], "c4", "how", path, "How › 4Cs", strip_md(c["body"])[:180], f"4cs {c['n']}", strip_md(c["examples"]))]
    return Page(path, c["name"], "how", body, description=f"{c['name']}: one of Bowman's 4Cs.", search=search)


def trump_page(site, tid: str) -> Page:
    path = site.u_trump(tid)
    ctx = Ctx(site, path)
    t = site.trump_by_id[tid]
    ts = site.ped["trumps"]
    idx = [x["id"] for x in ts].index(tid)
    head = C.page_head(ctx, model="how", crumbs_items=[("Start", ""), ("How", "how/"), ("Six Trumps", "how/#six-trumps"), (t["name"], None)],
                       eyebrow_text=f"How · the Six Trumps · {t['n']} of 6", title=t["name"],
                       meta_html=C.draft_badge(site.ped["status"]), strip_html=C.how_strip(ctx, tid))
    blocks = []
    for ex, b, i in site.trump_examples[tid]:
        blocks.append(f'<li class="design-block exk-{ex["kind"]}"><p class="db-meta">{ctx.a(site.u_example(ex["id"]), h(ex["short_name"]))} · '
                      f'{ctx.a(site.u_c4(b["c4"]), h(site.c4_by_id[b["c4"]]["name"]))} · {b["minutes"]} min</p>'
                      f'<p class="db-title">{h(b["title"])}</p><p>{h(b["activity"])}</p></li>')
    ex_html = (f'<section aria-labelledby="ib-h"><h2 id="ib-h" class="section-title">In our example designs {C.illustrative_badge()}</h2>'
               f'<ul class="design-blocks">{"".join(blocks)}</ul></section>') if blocks else ""
    main = (f'<p class="pull">{inline_md(t["body"])}</p>'
            f'<section aria-labelledby="ap-h"><h2 id="ap-h" class="kicker">How CPDSE applies it</h2><p>{inline_md(t["apply"])}</p></section>{ex_html}')
    aside = _how_used(ctx, site.trump_examples[tid])
    prev = (ts[idx - 1]["name"], site.u_trump(ts[idx - 1]["id"])) if idx > 0 else None
    nxt = (ts[idx + 1]["name"], site.u_trump(ts[idx + 1]["id"])) if idx < len(ts) - 1 else None
    body = C.entity(head, main, aside, C.pager(ctx, "Previous and next Trump", prev, nxt))
    search = [_entry(t["name"], "trump", "how", path, "How › Six Trumps", strip_md(t["body"])[:180], f"trump {t['n']}", strip_md(t["apply"]))]
    return Page(path, t["name"], "how", body, description=f"{t['name']}: one of Bowman's Six Trumps.", search=search)


# ==== TOOLS ======================================================================

def tools_page(site) -> Page:
    path = "tools/"
    ctx = Ctx(site, path)
    types = sorted({t["type"] for t in site.tools})
    head = C.page_head(ctx, model="neutral", crumbs_items=[("Start", ""), ("Tools", None)],
                       eyebrow_text="Crosswalk", title="Tools and methods",
                       lede_html=copy(ctx, "tools-intro.html"),
                       meta_html=C.chip(f"{len(site.tools)} tools and methods · {len(site.vocab.crosswalk)} links") + C.tool_based_pill())
    opts = "".join(f'<option value="{h(t)}">{h(t.capitalize())}</option>' for t in types)
    filters = (f'<form class="filters" data-tool-filter hidden role="search" aria-label="Filter tools">'
               f'<div class="field"><label for="tf-q">Filter by name</label><input id="tf-q" name="q" type="search" autocomplete="off"></div>'
               f'<div class="field"><label for="tf-type">Type</label><select id="tf-type" name="type"><option value="">All types</option>{opts}</select></div>'
               f'<p class="filter-count" aria-live="polite"></p></form>')
    rows = []
    for t in site.tools:
        links = []
        for l in t["links"]:
            st = site.stage_by_id[l["stage"]]
            target = (ctx.a(site.u_sub(l["subarea"]), h(site.sub_by_id[l["subarea"]]["name"])) if l["subarea"]
                      else ctx.a(site.u_domain(l["domain"]), h(site.domain_by_id[l["domain"]]["name"])))
            flag = ' <span class="badge badge-flag">Beyond reference</span>' if l["flag"] else ""
            links.append(f'<li>{ctx.a(site.u_stage(l["stage"]), h(str(st["order"]) + ". " + st["display_name"]))} <span class="arrow" aria-hidden="true">→</span><span class="sr-only"> links to </span> {target}{flag}</li>')
        aliases = f'<span class="tool-alias">Also: {h(", ".join(t["aliases"]))}</span>' if t["aliases"] else ""
        rows.append(f'<tr id="t-{t["slug"]}" data-name="{h((t["name"] + " " + " ".join(t["aliases"])).lower())}" data-type="{h(t["type"])}">'
                    f'<th scope="row"><span class="tool-name">{h(t["name"])}</span>{aliases}</th><td>{h(t["type"])}</td>'
                    f'<td><ul class="tool-links">{"".join(links)}</ul></td></tr>')
    table = (f'<div class="table-wrap" role="region" aria-label="Tools and methods" tabindex="0"><table class="tools">'
             f'<thead><tr><th scope="col">Tool or method</th><th scope="col">Type</th><th scope="col">Substep → competence sub-area</th></tr></thead>'
             f'<tbody>{"".join(rows)}</tbody></table></div>'
             f'<p class="empty" data-tool-empty hidden>No tools match. Clear the filter to see all {len(site.tools)}.</p>')
    body = f'{head}<div class="wrap">{filters}{table}</div>'
    search = [_entry("Tools and methods", "tools", "neutral", path, "Crosswalk", "Every tool linked to a substep and a competence sub-area", "crosswalk tools")]
    for t in site.tools:
        where = "; ".join(site.stage_by_id[l["stage"]]["display_name"] for l in t["links"])
        search.append(_entry(t["name"], "tool", "neutral", site.u_tool(t["slug"]), f"Tools › {t['type']}", f"Used in {where}", " ".join(t["aliases"])))
    return Page(path, "Tools and methods", "neutral", body, description="The tool crosswalk between value-chain substeps and competence sub-areas.", search=search)
