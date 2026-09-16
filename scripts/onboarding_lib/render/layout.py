"""Page shell: head, icon sprite, header with model switcher, footer."""
from __future__ import annotations

from ..text import h
from .core import MODELS, Ctx, Page

SITE_NAME = "CPDSE Reference Models"

SPRITE = """<svg class="sprite" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">
<symbol id="i-where" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="4" cy="12" r="2.6"/><circle cx="12" cy="12" r="2.6"/><circle cx="20" cy="12" r="2.6"/><path d="M7 12h2.4M14.6 12H17"/></g></symbol>
<symbol id="i-what" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 11h12M4 16h8M4 20h4"/></g></symbol>
<symbol id="i-how" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.6 12a7.4 7.4 0 0 1 12.6-5.2M17.4 4v3.4H14M19.4 12a7.4 7.4 0 0 1-12.6 5.2M6.6 20v-3.4H10"/></g></symbol>
<symbol id="i-ex" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 3h6v3H9zM8.5 11h7M8.5 15h4.5"/></g></symbol>
<symbol id="i-start" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h13M12 6l6 6-6 6"/></g></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></g></symbol>
<symbol id="i-theme" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 0 0 16z" fill="currentColor"/></g></symbol>
<symbol id="i-ext" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></g></symbol>
<symbol id="i-tool" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 6.5a4 4 0 0 0-5.3 5.3L4 17v3h3l5.2-5.2a4 4 0 0 0 5.3-5.3l-2.4 2.4-2.6-.4-.4-2.6z"/></g></symbol>
</svg>"""

THEME_BOOT = ("<script>(function(){try{var t=localStorage.getItem('cpdse-rm-theme');"
              "if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}})();</script>")


def header(ctx: Ctx, model: str) -> str:
    items = [("start", "", "Start", "Onboarding", "i-start")]
    items += [(k, MODELS[k]["home"], MODELS[k]["q"], MODELS[k]["short"], MODELS[k]["icon"]) for k in ("where", "what", "how", "ex")]
    links = []
    for key, to, q, short, icon in items:
        current = ' aria-current="true"' if key == model else ""
        links.append(
            f'<a class="sw sw-{key}" href="{h(ctx.href(to))}"{current}>{ctx.icon(icon)}'
            f'<span class="sw-q">{h(q)}</span><span class="sw-name">{h(short)}</span></a>'
        )
    return f"""<header class="site-header">
<div class="header-inner">
<a class="wordmark" href="{h(ctx.href(''))}"><img src="{h(ctx.href('assets/logo-snake.svg'))}" alt="" width="30" height="27"><span class="wm-text"><span class="wm-name">Reference Models</span><span class="wm-sub">for CPDSE-teachers</span></span></a>
<nav class="switcher" aria-label="Models">{''.join(links)}</nav>
<div class="header-tools">
<a class="search-trigger" href="{h(ctx.href('search/'))}" data-search-trigger>{ctx.icon('i-search')}<span class="st-label">Search</span><kbd class="st-kbd" hidden>Ctrl K</kbd></a>
<button type="button" class="theme-toggle" data-theme-toggle hidden>{ctx.icon('i-theme')}<span class="tt-label">Theme: auto</span></button>
</div>
</div>
</header>"""


def footer(ctx: Ctx) -> str:
    s = ctx.site
    p = s.prov
    dirty = " (with uncommitted changes)" if p.dirty else ""
    return f"""<footer class="site-footer">
<div class="footer-inner">
<p class="foot-lead">Built from <strong>{h(p.repo)}</strong> at commit <code>{h(p.short_sha)}</code>{h(dirty)}, {h(p.commit_date)}.
Pharma Value Chain {h(s.vc['version'])} · PDS Competence Model (last changed {h(p.files['competence']['date'])}) · Pedagogic Practices {h(s.ped['version'])}.</p>
<p>Levels and teaching designs in the examples are illustrative, not assessments of real people.</p>
<nav class="foot-nav" aria-label="Site">{ctx.a('', 'Start')}{ctx.a('tools/', 'Tools')}{ctx.a('search/', 'Search and index')}{ctx.a('about/', 'About this site')}</nav>
</div>
</footer>"""


def shell(site, page: Page) -> str:
    ctx = Ctx(site, page.path)
    root = ctx.href("")
    title = SITE_NAME if page.model == "start" and not page.path else f"{page.title} · {SITE_NAME}"
    desc = f'<meta name="description" content="{h(page.description)}">\n' if page.description else ""
    data = f'<script type="application/json" id="page-data">{page.data_json}</script>\n' if page.data_json else ""
    fonts = "".join(
        f'<link rel="preload" href="{h(ctx.href("assets/fonts/" + f))}" as="font" type="font/woff2" crossorigin>\n'
        for f in ("source-sans-3-normal-latin.woff2", "source-serif-4-normal-latin.woff2")
    )
    body_class = f"model-{page.model} {page.body_class}".strip()
    return f"""<!doctype html>
<!-- GENERATED by scripts/build_onboarding.py from {h(site.prov.repo)}@{h(site.prov.short_sha)}. Do not edit: change reference-models/_src/ and rebuild. -->
<html lang="en" data-root="{h(root)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="generator" content="scripts/build_onboarding.py">
<title>{h(title)}</title>
{desc}{THEME_BOOT}
{fonts}<link rel="stylesheet" href="{h(ctx.href('assets/site.css'))}">
<link rel="icon" href="{h(ctx.href('assets/favicon.svg'))}" type="image/svg+xml">
<script src="{h(ctx.href('assets/site.js'))}" defer></script>
</head>
<body class="{h(body_class)}">
<a class="skip-link" href="#main">Skip to content</a>
{SPRITE}
{header(ctx, page.model)}
<main id="main" tabindex="-1">
{page.body}
</main>
{footer(ctx)}
{data}</body>
</html>
"""
