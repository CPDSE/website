"""The onboarding flow (Start page), worked examples, search/index and About."""
from __future__ import annotations

import json
import math
import re

from .. import BuildError
from ..text import h, inline_md, strip_md, words
from . import components as C
from .core import MODELS, Ctx, Page
from .copy import copy, raw
from .svg import map_legend, value_competence_map


def _entry(t, k, m, u, p="", x="", s="", b=""):
    return {"t": t, "k": k, "m": m, "u": u, "p": p, "x": x, "s": s, "b": b}


def _stage_pill(site, sid) -> str:
    st = site.stage_by_id[sid]
    return f'<span class="cell-n">{st["order"]}</span> {h(st["display_name"])}'


WPM = 180  # a careful reading pace for readers with English as a second language


def _hero_title(title: str) -> str:
    """Colour each model's question word in the Start page title."""
    out = []
    for word in title.split(" "):
        key = next((m for m in ("where", "what", "how") if word.strip(",.").lower() == m), None)
        out.append(f'<span class="hw-{key}">{h(word)}</span>' if key else h(word))
    return " ".join(out)


def _ex_name(ex) -> str:
    return f'{ex["institution"]} {ex["code"]}'


# ==== landing components ==========================================================

def _model_cards(ctx: Ctx) -> str:
    s = ctx.site
    c = s.counts()
    rows = [
        ("where", "Where in drug development?", "Anchors a course or workshop to the substeps it prepares people for.",
         f'{c["tiers"]} steps, {c["substeps"]} substeps · {s.vc["version"]}, draft'),
        ("what", "What should people be able to do?", "Describes Pharmaceutical Data Science (PDS) capabilities, so we can assess today's level and set a target.",
         f'{c["domains"]} domains, {c["subareas"]} sub-areas, {c["competencies"]} competencies · levels L1–L5'),
        ("how", "How do we build it so it sticks?", "Shapes every session so participants do the work themselves, because the person doing the work does the learning.",
         f'Bowman\'s 4Cs (a four-part session plan) and Six Trumps (six rules of thumb) · {s.ped["version"]}, draft'),
    ]
    cards = "".join(
        f'<li class="model-card mc-{m}"><p class="mc-q">{ctx.icon(MODELS[m]["icon"])}<span>{h(MODELS[m]["q"])}</span></p>'
        f'<h3 class="mc-name">{ctx.a(MODELS[m]["home"], h(MODELS[m]["name"]), cls="card-link")}</h3>'
        f'<p class="mc-ask">{h(q)}</p><p class="mc-does">{h(does)}</p><p class="mc-facts">{h(facts)}</p></li>'
        for m, q, does, facts in rows
    )
    return f'<ul class="model-cards">{cards}</ul>'


def _take_one_away(ctx: Ctx) -> str:
    s = ctx.site
    panels = []
    for p in s.config["take_one_away"]:
        chips = []
        for m in ("where", "what", "how"):
            off = p["missing"] == m
            label = f'{h(MODELS[m]["q"])}<span class="sr-only">{" (missing)" if off else ""}</span>'
            chips.append(f'<li class="tchip tchip-{m}{" is-off" if off else ""}">{ctx.icon(MODELS[m]["icon"])}{label}</li>')
        cls = "panel is-whole" if p["missing"] is None else "panel"
        title = "All three models" if p["missing"] is None else f'Without {MODELS[p["missing"]]["q"]}'
        panels.append(f'<li class="{cls}"><p class="panel-title">{h(title)}</p><ul class="tchips">{"".join(chips)}</ul>'
                      f'<p class="panel-result">{h(p["result"])}</p><p class="panel-why">{h(p["why"])}</p></li>')
    return f'<ol class="panels">{"".join(panels)}</ol>'


def _journey(ctx: Ctx) -> str:
    s = ctx.site
    cols = []
    steps = [("where", "Anchor", "Place it in the value chain. This sets what is in scope."),
             ("what", "Assess and target", "Estimate today's level for two or three competencies and choose targets."),
             ("how", "Deliver", "Plan each session as a 4Cs sequence and check its blocks against the Six Trumps.")]
    for n, (m, name, what) in enumerate(steps, start=1):
        boxes = []
        for ex in s.examples:
            if m == "where":
                st = s.stage_by_id[ex["anchor"]["stages"][0]]
                content = f'{h(ex["short"]["anchor"])}: {ctx.a(s.u_stage(st["id"]), h(st["display_name"]))} <span class="muted">({h(st["tier"])})</span>'
            elif m == "what":
                content = '<ul class="jt">' + "".join(
                    f'<li>{ctx.a(s.u_comp(t["subarea"], t["slug"]), h(s.comp_by_key[(t["subarea"], t["slug"])]["name"]))} {C.level_move(s, t["today"], t["target"])}</li>'
                    for t in ex["targets"]) + "</ul>"
            else:
                seq = " → ".join(s.c4_by_id[b["c4"]]["name"] for b in ex["design"]["blocks"])
                content = f'{h(ex["short"]["deliver"])} <span class="jseq">{h(seq)}</span>'
            boxes.append(f'<div class="jbox exk-{ex["kind"]}"><p class="jbox-tag">{h(ex["kind_label"])} · '
                         f'{ctx.a(s.u_example(ex["id"]), h(ex["short_name"]))}</p><div class="jbox-body">{content}</div></div>')
        cols.append(f'<li class="jstep jstep-{m}"><div class="jhead"><span class="jn">{n}</span><div><h3 class="jname">{h(name)}</h3>'
                    f'<p class="juses">{ctx.icon(MODELS[m]["icon"])}Uses {ctx.a(MODELS[m]["home"], h(MODELS[m]["name"]))}</p></div></div>'
                    f'<p class="jwhat">{h(what)}</p>{"".join(boxes)}</li>')
    key = ('<p class="jkey"><span class="jkey-item exk-curriculum-course">Curriculum course</span>'
           '<span class="jkey-item exk-people-development">People Development</span></p>')
    return f'{key}<ol class="journey">{"".join(cols)}</ol>'


def _map(ctx: Ctx) -> str:
    return (f'<figure class="fig fig-map-wrap"><div class="map-scroll">{value_competence_map(ctx)}</div>'
            f'<figcaption><p class="map-key"><span class="jkey-item exk-curriculum-course">Curriculum course</span>'
            f'<span class="jkey-item exk-people-development">People Development</span><span class="map-key-n">1→3 = illustrative level today → target</span></p>'
            f'<details class="map-list"><summary>The map as a list</summary>{map_legend(ctx)}</details></figcaption></figure>')


def _explore(ctx: Ctx) -> str:
    s = ctx.site
    c = s.counts()
    rows = [
        ("where", f'{c["substeps"]} substeps with their questions, methods and tools', "Start with", s.u_stage("lead-identification"), "Lead Identification"),
        ("what", f'{c["competencies"]} competencies at five levels, plus the level rubric', "Start with", "what/levels/", "the level rubric"),
        ("how", f'The 4Cs and the Six Trumps, with example session designs', "Start with", s.u_c4("concrete-practice"), "Concrete Practice"),
        ("ex", f'{c["examples"]} worked examples and a worksheet for your own course', "Start with", "examples/#your-course", "the worksheet"),
    ]
    cards = "".join(
        f'<li class="explore-card ec-{m}"><p class="mc-q">{ctx.icon(MODELS[m]["icon"])}<span>{h(MODELS[m]["q"])}</span></p>'
        f'<h3 class="mc-name">{ctx.a(MODELS[m]["home"], h(MODELS[m]["name"]), cls="card-link")}</h3>'
        f'<p>{h(desc)}</p><p class="ec-first">{h(lead)} {ctx.a(to, h(label))}</p></li>'
        for m, desc, lead, to, label in rows
    )
    return (f'<ul class="explore-cards">{cards}</ul>'
            f'<p class="explore-more">Or {ctx.a("search/", "search everything")}, browse {ctx.a("tools/", "all tools and methods")}, '
            f'or read {ctx.a("about/", "about this site, its sources and the glossary")}.</p>')


# ==== pages =======================================================================

def landing(site) -> Page:
    path = ""
    ctx = Ctx(site, path)
    comps = {"model-cards": lambda: _model_cards(ctx), "take-one-away": lambda: _take_one_away(ctx),
             "journey": lambda: _journey(ctx), "map": lambda: _map(ctx), "explore": lambda: _explore(ctx)}
    sections_cfg = site.config["landing"]["sections"]
    steps_total = sum(1 for sc in sections_cfg if sc["step"])
    rendered, total_words = [], 0
    for sc in sections_cfg:
        html = copy(ctx, sc["file"], "narrative", comps)
        w = words(re.sub(r"<[^>]+>", " ", html))
        total_words += w
        minutes = max(1, math.ceil(w / WPM))
        if sc["step"]:
            c4 = site.c4_by_id[sc["c4"]]["name"]
            label = f'Part {sc["step"]} of {steps_total} · {c4} · about {minutes} min'
        elif sc["c4"]:
            label = f'Before you start · {site.c4_by_id[sc["c4"]]["name"]}'
        else:
            label = "Your next stop"
        rendered.append((sc, label, html))

    rail = "".join(
        f'<li><a href="#{sc["id"]}" class="rail-link"><span class="rail-n" aria-hidden="true">{sc["step"] or "·"}</span>'
        f'<span>{h(sc["label"])}</span></a></li>' for sc, _, _ in rendered
    )
    sections = []
    for i, (sc, label, html) in enumerate(rendered):
        nxt = rendered[i + 1][0] if i + 1 < len(rendered) else None
        nxt_html = f'<p class="flow-next"><a href="#{nxt["id"]}">Next: {h(nxt["label"])}<span aria-hidden="true"> ↓</span></a></p>' if nxt else ""
        sections.append(f'<section class="flow-section flow-{sc["id"]}" id="{sc["id"]}" aria-labelledby="{sc["id"]}-h">'
                        f'<p class="flow-step">{h(label)}</p><h2 id="{sc["id"]}-h" class="flow-title">{h(sc["label"])}</h2>'
                        f'{html}{nxt_html}</section>')
    minutes_total = max(1, math.ceil(total_words / WPM))
    hero = (f'<div class="hero"><div class="wrap hero-inner"><p class="eyebrow eyebrow-start">{ctx.icon("i-start")}<span>Onboarding for CPDSE-teachers</span></p>'
            f'<h1 class="hero-title">{_hero_title(site.config["landing"]["title"])}</h1>'
            f'<p class="hero-lede">CPDSE uses three reference models to plan its course upgrades and its People Development workshops (training for staff already in post). '
            f'This page explains why there are three, how they fit together, and where to look things up.</p>'
            f'<p class="hero-meta"><span>About {minutes_total} minutes</span><span>{steps_total} parts</span>'
            f'<a href="#explore">Skip to the models</a></p></div></div>')
    body = (f'{hero}<div class="wrap flow"><nav class="step-rail" aria-label="On this page" data-step-rail><ol>{rail}</ol></nav>'
            f'<div class="flow-main">{"".join(sections)}</div></div>')
    search = [_entry("Start: Where, What, How", "page", "start", "", "Start", "Why CPDSE uses three reference models and how they fit together",
                     "onboarding start introduction why three models methodology sentence")]
    for sc, _, html in rendered:
        search.append(_entry(sc["label"], "section", "start", f'#{sc["id"]}', "Start", "", "", strip_md(re.sub(r"<[^>]+>", " ", html))[:400]))
    return Page(path, site.config["landing"]["title"], "start", body,
                description="Onboarding for CPDSE-teachers: the three reference models, why there are three and how they work together.",
                search=search)


def examples_overview(site) -> Page:
    path = "examples/"
    ctx = Ctx(site, path)
    head = C.page_head(ctx, model="ex", crumbs_items=[("Start", ""), ("Examples", None)], eyebrow_text="Examples · the models in use",
                       title="Worked examples", lede_html=copy(ctx, "examples-intro.html"))
    cards = []
    for ex in site.examples:
        st = site.stage_by_id[ex["anchor"]["stages"][0]]
        targets = "; ".join(f'{site.comp_by_key[(t["subarea"], t["slug"])]["name"]} L{t["today"]}→L{t["target"]}' for t in ex["targets"])
        cards.append(
            f'<li class="ex-card exk-{ex["kind"]}"><p class="ex-kind">{h(ex["kind_label"])} · {h(ex["short_name"])}</p>'
            f'<h2 class="ex-title">{ctx.a(site.u_example(ex["id"]), h(ex["title"]), cls="card-link")}</h2><p>{h(ex["summary"])}</p>'
            f'<dl class="ex-steps"><div><dt>Anchor</dt><dd>{h(st["display_name"])}</dd></div><div><dt>Targets {C.illustrative_badge()}</dt><dd>{h(targets)}</dd></div>'
            f'<div><dt>Deliver {C.illustrative_badge()}</dt><dd>{h(ex["design"]["format"])}</dd></div></dl></li>'
        )
    body = f'{head}<div class="wrap"><ul class="ex-cards">{"".join(cards)}</ul>{copy(ctx, "worksheet.html")}</div>'
    search = [_entry("Worked examples", "page", "ex", path, "Examples", "A curriculum course and a People Development workshop, step by step",
                     "examples people development fraiday bar vibe cafe tailored workshop curriculum course",
                     strip_md(re.sub(r"<[^>]+>", " ", raw(site, "examples-intro.html")))),
              _entry("Worksheet: place your own course", "section", "ex", "examples/#your-course", "Examples", "Anchor, assess and target, deliver", "worksheet exercise"),
              _entry("People Development: FrAIday Bar, Vibe Café and tailored workshops", "section", "ex", "examples/", "Examples",
                     "CPDSE's learning offer for staff already in post", "fraiday bar vibe cafe tailored workshop staff upskilling")]
    return Page(path, "Worked examples", "ex", body, description="Worked examples: one curriculum course and one People Development workshop.", search=search)


def example_page(site, ex: dict) -> Page:
    path = site.u_example(ex["id"])
    ctx = Ctx(site, path)
    exs = site.examples
    idx = exs.index(ex)
    meta = C.chip(ex["kind_label"]) + C.chip(_ex_name(ex), "chip-mono") + C.illustrative_badge("Illustrative levels and design")
    head = C.page_head(ctx, model="ex", crumbs_items=[("Start", ""), ("Examples", "examples/"), (_ex_name(ex), None)],
                       eyebrow_text=f"Example · {ex['kind_label']}", title=f'{ex["code"]} · {ex["title"]}', lede_html=f"<p>{h(ex['summary'])}</p>", meta_html=meta)
    facts = "".join(f"<div><dt>{h(k)}</dt><dd>{h(v)}</dd></div>" for k, v in ex["facts"])
    facts_html = (f'<dl class="facts">{facts}</dl><p class="source">{C.ext_link(ctx, ex["source_url"], ex["source_label"])}</p>')

    # 1 anchor
    stages = "".join(
        f'<li>{ctx.a(site.u_stage(sid), _stage_pill(site, sid), cls="stage-pill")}'
        f'<span class="muted"> {h(site.stage_by_id[sid]["tier"])}{" · anchored here" if i == 0 else " · also touches"}</span></li>'
        for i, sid in enumerate(ex["anchor"]["stages"])
    )
    anchor = (f'<section class="ex-step ex-step-where" aria-labelledby="s1-h"><p class="eyebrow eyebrow-where">{ctx.icon("i-where")}<span>Uses the Pharma Value Chain</span></p>'
              f'<h2 id="s1-h" class="section-title">Anchor</h2><ul class="stage-pills">{stages}</ul><p>{h(ex["anchor"]["why"])}</p>'
              f'{C.stage_strip(ctx, None, on=tuple(ex["anchor"]["stages"][:1]), also=tuple(ex["anchor"]["stages"][1:]))}</section>')

    # 2 assess & target
    tcards = []
    for t in ex["targets"]:
        comp = site.comp_by_key[(t["subarea"], t["slug"])]
        sa = site.sub_by_id[t["subarea"]]
        meter = C.level_meter(today=t["today"], target=t["target"], size="meter-lg",
                              label=f"Illustrative: from L{t['today']} to L{t['target']} of 5")
        lv_today, lv_target = comp["levels"][t["today"] - 1], comp["levels"][t["target"] - 1]
        tcards.append(
            f'<li class="target-card"><h3 class="tc-name">{ctx.a(site.u_comp(t["subarea"], t["slug"]), h(comp["name"]))}</h3>'
            f'<p class="tc-sub">{ctx.a(site.u_sub(sa["id"]), h(sa["name"]))} · competency {h(comp["id"])}</p>'
            f'<p class="tc-move">{meter}<span class="tc-move-t">Start L{t["today"]} · target L{t["target"]}</span></p>'
            f'<dl class="tc-levels"><div><dt>Today, L{t["today"]} {h(site.comp["levels"][t["today"] - 1]["name"])}</dt><dd>{inline_md(lv_today["text"])}</dd></div>'
            f'<div><dt>Target, L{t["target"]} {h(site.comp["levels"][t["target"] - 1]["name"])}</dt><dd>{inline_md(lv_target["text"])}</dd></div></dl>'
            f'<p class="tc-why"><strong>Why this target:</strong> {h(t["why"])}</p></li>'
        )
    assess = (f'<section class="ex-step ex-step-what" aria-labelledby="s2-h"><p class="eyebrow eyebrow-what">{ctx.icon("i-what")}<span>Uses the PDS Competence Model</span></p>'
              f'<h2 id="s2-h" class="section-title">Assess and target {C.illustrative_badge()}</h2>'
              f'<ul class="target-cards">{"".join(tcards)}</ul></section>')

    # 3 deliver
    total = ex["minutes"]
    bars = "".join(
        f'<li class="tb tb-{b["c4"]} tw-{b["minutes"] // 5}"><span class="tb-n">{i}</span>'
        f'<span class="tb-l"><span class="tb-c">{h(site.c4_by_id[b["c4"]]["name"])} · </span>{b["minutes"]} min</span></li>'
        for i, b in enumerate(ex["design"]["blocks"], start=1)
    )
    timebar = f'<ol class="timebar" aria-label="{total}-minute session in {len(ex["design"]["blocks"])} blocks">{bars}</ol>'
    blocks = []
    for i, b in enumerate(ex["design"]["blocks"], start=1):
        tr = "".join(f'<li>{ctx.a(site.u_trump(x_), h(site.trump_by_id[x_]["name"]))}</li>' for x_ in b["trumps"])
        blocks.append(f'<li class="block block-{b["c4"]}"><div class="block-head"><span class="block-n">{i}</span>'
                      f'{ctx.a(site.u_c4(b["c4"]), h(site.c4_by_id[b["c4"]]["name"]), cls="c4-chip c4-" + b["c4"])}<span class="block-min">{b["minutes"]} min</span></div>'
                      f'<h3 class="block-title">{h(b["title"])}</h3><p>{h(b["activity"])}</p><ul class="block-trumps" aria-label="Six Trumps used">{tr}</ul></li>')
    deliver = (f'<section class="ex-step ex-step-how" aria-labelledby="s3-h"><p class="eyebrow eyebrow-how">{ctx.icon("i-how")}<span>Uses the Pedagogic Practices</span></p>'
               f'<h2 id="s3-h" class="section-title">Deliver {C.illustrative_badge()}</h2><p class="ex-format">{h(ex["design"]["format"])}</p>'
               f'{timebar}<ol class="blocks">{"".join(blocks)}</ol></section>')

    main = facts_html + anchor + assess + deliver
    uses = []
    uses.append("<li><strong>Where:</strong> " + ", ".join(ctx.a(site.u_stage(sid), h(site.stage_by_id[sid]["display_name"])) for sid in ex["anchor"]["stages"]) + "</li>")
    uses.append("<li><strong>What:</strong> " + ", ".join(ctx.a(site.u_comp(t["subarea"], t["slug"]), h(site.comp_by_key[(t["subarea"], t["slug"])]["name"])) for t in ex["targets"]) + "</li>")
    c4s = list(dict.fromkeys(b["c4"] for b in ex["design"]["blocks"]))
    trs = list(dict.fromkeys(x_ for b in ex["design"]["blocks"] for x_ in b["trumps"]))
    uses.append("<li><strong>How:</strong> " + ", ".join(ctx.a(site.u_c4(c), h(site.c4_by_id[c]["name"])) for c in c4s) + "; "
                + ", ".join(ctx.a(site.u_trump(t), h(site.trump_by_id[t]["name"])) for t in trs) + "</li>")
    aside = f'<section class="aside-block"><h3 class="aside-h">Everything this example uses</h3><ul class="conn-flat uses">{"".join(uses)}</ul></section>'
    others = [e for e in exs if e is not ex]
    if others:
        aside += '<section class="aside-block"><h3 class="aside-h">The other example</h3><ul class="conn-flat">' + "".join(
            f'<li>{ctx.a(site.u_example(e["id"]), h(_ex_name(e) + ": " + e["title"]))}</li>' for e in others) + "</ul></section>"
    prev = (exs[idx - 1]["title"], site.u_example(exs[idx - 1]["id"])) if idx > 0 else None
    nxt = (exs[idx + 1]["title"], site.u_example(exs[idx + 1]["id"])) if idx < len(exs) - 1 else None
    body = C.entity(head, main, aside, C.pager(ctx, "Previous and next example", prev, nxt))
    search = [_entry(f'{ex["code"]} · {ex["title"]}', "example", "ex", path, f'Examples › {ex["kind_label"]}', ex["summary"], f'{_ex_name(ex)} {ex["short_name"]} {ex["kind_label"]}',
                     " ".join(b["title"] + " " + b["activity"] for b in ex["design"]["blocks"]))]
    return Page(path, f'{ex["code"]} · {ex["title"]}', "ex", body, description=ex["summary"], search=search)


def search_page(site, all_entries: list) -> Page:
    path = "search/"
    ctx = Ctx(site, path)
    head = C.page_head(ctx, model="neutral", crumbs_items=[("Start", ""), ("Search", None)], eyebrow_text="Find anything",
                       title="Search and index",
                       lede_html="<p>Search substeps, competencies, levels, practices, tools and examples. Every page is also listed in the index below.</p>")
    form = ('<form class="search-page" data-search-page hidden role="search" action="./" method="get">'
            '<label for="sp-q" class="field-label">Search the reference models</label>'
            '<div class="search-row"><input id="sp-q" name="q" type="search" autocomplete="off" spellcheck="false" '
            'aria-describedby="sp-hint" aria-controls="sp-results"><button type="submit" class="btn">Search</button></div>'
            '<p id="sp-hint" class="hint">Try a tool (SHAP), a topic (survival analysis) or a level (L3).</p>'
            '<p class="search-status" aria-live="polite"></p><div id="sp-results" class="search-results"></div></form>')
    groups = []
    group_defs = [("where", "Where: Pharma Value Chain", None), ("what", "What: PDS Competence Model", None), ("how", "How: Pedagogic Practices", None),
                  ("ex", "Examples", None), ("start", "Start page", None), ("neutral", "Other pages", ("tool", "glossary")),
                  ("tool", "Tools and methods", "tool"), ("glossary", "Glossary", "glossary")]
    for m, title, kind in group_defs:
        if kind in ("tool", "glossary"):
            items = [e for e in all_entries if e["k"] == kind]
        else:
            items = [e for e in all_entries if e["m"] == m and e["k"] not in ("tool", "section", "glossary")]
        if not items:
            continue
        items.sort(key=lambda e: e["t"].lower())
        lis = "".join(f'<li>{ctx.a(e["u"], h(e["t"]))}<span class="idx-path">{h(e["p"])}</span></li>' for e in items)
        gid = f"idx-{m}"
        groups.append(f'<section class="idx-group" aria-labelledby="{gid}"><h2 id="{gid}" class="section-title">{h(title)} <span class="count">{len(items)}</span></h2><ul class="idx">{lis}</ul></section>')
    body = f'{head}<div class="wrap">{form}<div class="index">{"".join(groups)}</div></div>'
    return Page(path, "Search and index", "neutral", body, description="Search and A–Z index of the CPDSE reference models.")


def about_page(site) -> Page:
    path = "about/"
    ctx = Ctx(site, path)
    head = C.page_head(ctx, model="neutral", crumbs_items=[("Start", ""), ("About", None)], eyebrow_text="About",
                       title="About this site")
    p = site.prov
    rows = [
        ("Pharma Value Chain", site.vc["version"], site.vc["status"] or "", p.files["value_chain"]),
        ("PDS Competence Model", "no version number", "", p.files["competence"]),
        ("Level rubric", "no version number", "", p.files["rubric"]),
        ("Pedagogic Practices", site.ped["version"], site.ped["status"] or "", p.files["pedagogy"]),
        ("Vocabulary and crosswalk", "", "", p.files["vocab"]),
    ]
    trs = "".join(f'<tr><th scope="row">{h(n)}</th><td>{h(v)}</td><td>{h(st)}</td><td><code>{h(f["path"])}</code></td>'
                  f'<td><code>{h(f["commit"])}</code> {h(f["date"])}</td></tr>' for n, v, st, f in rows)
    prov = (f'<section aria-labelledby="ab-prov"><h2 id="ab-prov" class="section-title">Sources</h2>'
            f'<p>Built from <code>{h(p.repo)}</code> at <code>{h(p.sha)}</code> ({h(p.commit_date)}){" with uncommitted changes" if p.dirty else ""}.</p>'
            f'<div class="table-wrap" role="region" aria-labelledby="ab-prov" tabindex="0"><table class="simple"><thead><tr><th scope="col">Model</th><th scope="col">Version</th>'
            f'<th scope="col">Status</th><th scope="col">Source file</th><th scope="col">Last change</th></tr></thead><tbody>{trs}</tbody></table></div></section>')
    gl = "".join(f'<div id="g-{re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")}"><dt>{h(term)}</dt><dd>{h(defn)}</dd></div>'
                 for term, defn in site.config["glossary"])
    glossary = f'<section aria-labelledby="ab-gl"><h2 id="ab-gl" class="section-title">Glossary</h2><dl class="glossary">{gl}</dl></section>'
    licence = ('<section aria-labelledby="ab-lic"><h2 id="ab-lic" class="section-title">Credits and licences</h2>'
               '<ul><li>The reference models are CPDSE work, released under the '
               f'{C.ext_link(ctx, "https://www.gnu.org/licenses/gpl-3.0.html", "GNU General Public License v3.0")}.</li>'
               '<li>The 4Cs and the Six Trumps are by Sharon L. Bowman (<em>Training from the Back of the Room!</em>, 2009; '
               '<em>Using Brain Science to Make Training Stick</em>, 2011). This site paraphrases CPDSE\'s summary of them.</li>'
               f'<li>Typefaces: Source Serif 4 and Source Sans 3 by Adobe, under the {C.ext_link(ctx, "https://openfontlicense.org/", "SIL Open Font License")}, served from this site.</li>'
               '<li>Course facts come from the official SDU and UCPH course descriptions linked on each example.</li></ul></section>')
    body = C.entity(head, copy(ctx, "about.html") + prov + glossary + licence, "")
    search = [_entry("About this site", "page", "neutral", path, "About", "Sources, versions, glossary and licences", "about provenance version licence")]
    for term, defn in site.config["glossary"]:
        search.append(_entry(term, "glossary", "neutral", f'about/#g-{re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")}', "Glossary", defn))
    return Page(path, "About this site", "neutral", body, description="Sources, versions, glossary and licences for the CPDSE reference-models site.", search=search)


def favicon() -> str:
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#3C5E3E"/>'
            '<g fill="none" stroke="#D6C17C" stroke-width="2.6" stroke-linecap="round"><circle cx="8" cy="16" r="3"/><circle cx="16" cy="16" r="3"/>'
            '<circle cx="24" cy="16" r="3"/></g></svg>\n')
