"""Integrity checks over the generated site (in memory or on disk).

Errors fail the build; warnings are reported. Checks: internal links and
#fragments resolve, no external assets, external links only to allowed hosts,
per-page structure, banned words, Jekyll safety, and size budgets.
"""
from __future__ import annotations

import json
import posixpath
import re
from html.parser import HTMLParser

BUDGETS = {".html": 90_000, "site.css": 72_000, "site.js": 30_000, "search-index.json": 260_000}


class _Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[tuple[str, str, str]] = []  # (tag, attr, value)
        self.h1 = 0
        self.lang = None
        self.title = False
        self.robots = False
        self.skip = False
        self.style_attrs: list[str] = []
        self.dup_ids: set[str] = set()
        self.text: list[str] = []
        self._in = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                self.dup_ids.add(a["id"])
            self.ids.add(a["id"])
        if "style" in a:
            self.style_attrs.append(tag)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self.title = True
        elif tag == "meta" and a.get("name") == "robots" and "noindex" in (a.get("content") or ""):
            self.robots = True
        if tag == "a" and "skip-link" in (a.get("class") or ""):
            self.skip = True
        for attr in ("href", "src"):
            if attr in a and a[attr] is not None:
                self.links.append((tag, attr, a[attr]))
        if tag in ("script", "style"):
            self._in.append(tag)

    def handle_endtag(self, tag):
        if self._in and self._in[-1] == tag:
            self._in.pop()

    def handle_data(self, data):
        if not self._in:
            self.text.append(data)


def _resolve(page_path: str, url: str) -> tuple[str, str]:
    path, _, frag = url.partition("#")
    base = posixpath.dirname(page_path)
    if not path:
        return page_path, frag
    joined = posixpath.normpath(posixpath.join(base, path))
    if path.endswith("/") or joined == ".":
        joined = posixpath.join("" if joined == "." else joined, "index.html")
    return joined, frag


def run(files: dict, allow_external: list[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    pages: dict[str, _Page] = {}
    for path, data in files.items():
        if not path.endswith(".html"):
            continue
        text = data.decode("utf-8")
        if text.startswith("---"):
            errors.append(f"{path}: starts with '---' (Jekyll would process it)")
        if re.search(r"\{\{|\{%", re.sub(r"<code>.*?</code>", "", text, flags=re.S)):
            errors.append(f"{path}: contains Liquid-like '{{{{' or '{{%'")
        p = _Page()
        p.feed(text)
        pages[path] = p
        if p.h1 != 1:
            errors.append(f"{path}: has {p.h1} <h1> elements (expected 1)")
        if p.lang != "en":
            errors.append(f"{path}: <html lang> missing")
        if not p.title:
            errors.append(f"{path}: <title> missing")
        if not p.robots:
            errors.append(f"{path}: noindex meta missing")
        if not p.skip:
            errors.append(f"{path}: skip link missing")
        if p.style_attrs:
            errors.append(f"{path}: style attributes on {sorted(set(p.style_attrs))}")
        if p.dup_ids:
            errors.append(f"{path}: duplicate ids {sorted(p.dup_ids)[:5]}")
        body_text = " ".join(p.text)
        if re.search(r"\bconsultants?\b", body_text, re.I):
            errors.append(f"{path}: uses the word 'consultant' (say CPDSE-teacher)")
        for word in ("customer", "client"):
            if re.search(rf"\b{word}s?\b", body_text, re.I):
                warnings.append(f"{path}: uses the word '{word}'")

    for path, p in pages.items():
        for tag, attr, url in p.links:
            if url.startswith(("http://", "https://", "//")):
                if tag != "a":
                    errors.append(f"{path}: external {tag}[{attr}] {url}")
                elif not any(url.startswith(prefix) for prefix in allow_external):
                    errors.append(f"{path}: external link not on the allow-list: {url}")
                continue
            if url.startswith(("mailto:", "data:")):
                errors.append(f"{path}: unexpected {url[:20]}")
                continue
            if tag == "use":
                if url.startswith("#") and url[1:] not in p.ids:
                    errors.append(f"{path}: <use> points at missing symbol {url}")
                continue
            target, frag = _resolve(path, url)
            if target.startswith("../") or target == "..":
                errors.append(f"{path}: link leaves the site folder: {url}")
                continue
            if target not in files:
                errors.append(f"{path}: broken link {url} (→ {target})")
                continue
            if frag and target.endswith(".html"):
                tp = pages.get(target)
                if tp is not None and frag not in tp.ids:
                    errors.append(f"{path}: missing fragment {url} (#{frag} not in {target})")

    css = files.get("assets/site.css", b"").decode("utf-8")
    for url in re.findall(r"url\(([^)]+)\)", css):
        url = url.strip("'\" ")
        if url.startswith(("http", "//")):
            errors.append(f"assets/site.css: external url({url})")
        elif not url.startswith("#") and posixpath.normpath(posixpath.join("assets", url)) not in files:
            errors.append(f"assets/site.css: missing url({url})")

    index = files.get("assets/search-index.json")
    if index is not None:
        for e in json.loads(index.decode("utf-8")):
            target, frag = _resolve("index.html", e["u"] or "./")
            if target not in files:
                errors.append(f"search index: broken URL {e['u']}")
            elif frag and frag not in pages[target].ids:
                errors.append(f"search index: missing fragment {e['u']}")

    for path, data in files.items():
        for key, limit in BUDGETS.items():
            if (path.endswith(key) if key.startswith(".") else posixpath.basename(path) == key) and len(data) > limit:
                errors.append(f"{path}: {len(data):,} bytes is over the {limit:,} budget")
    return errors, warnings
