"""Small text helpers shared by the parsers and renderers."""
from __future__ import annotations

import html
import posixpath
import re
import unicodedata

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def slugify(text: str, maxlen: int = 60) -> str:
    """ASCII, lowercase, hyphen-separated; cut at a word boundary."""
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    norm = norm.lower().replace("&", " and ")
    slug = _SLUG_STRIP.sub("-", norm).strip("-")
    if len(slug) > maxlen:
        cut = slug[:maxlen]
        slug = cut.rsplit("-", 1)[0] if "-" in cut else cut
    return slug


def h(value: object) -> str:
    """Escape text for HTML element content and double-quoted attributes."""
    return html.escape(str(value), quote=True)


_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITAL = re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])")


def inline_md(text: str) -> str:
    """Escape, then render the tiny markdown subset used in the model docs.

    Supports `code`, **bold** and *italic*. Code spans are protected first so
    asterisks inside them are left alone.
    """
    codes: list[str] = []

    def keep(m: re.Match) -> str:
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    out = _CODE.sub(keep, text)
    out = h(out)
    out = _BOLD.sub(r"<strong>\1</strong>", out)
    out = _ITAL.sub(r"<em>\1</em>", out)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{h(codes[int(m.group(1))])}</code>", out)


def strip_md(text: str) -> str:
    """Plain text version of inline markdown (for search and meta tags)."""
    return _ITAL.sub(r"\1", _BOLD.sub(r"\1", _CODE.sub(r"\1", text)))


def rel(from_dir: str, to: str) -> str:
    """Relative URL from a page directory to a site path.

    Site paths are root-relative without a leading slash: ``""`` is the root,
    ``"where/lead-identification/"`` a page directory, ``"assets/site.css"`` a
    file. An optional ``#fragment`` is carried through.
    """
    if to.startswith("#"):
        return to
    path, _, frag = to.partition("#")
    frag = f"#{frag}" if frag else ""
    start = from_dir.rstrip("/") or "."
    if path == "" or path.endswith("/"):
        target = path.rstrip("/") or "."
        out = posixpath.relpath(target, start)
        out = "./" if out == "." else out + "/"
    else:
        out = posixpath.relpath(path, start)
    if out == "./" and frag:
        return frag
    return out + frag


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9’']+", text))


def join_lines(lines: list[str]) -> str:
    return " ".join(line.strip() for line in lines if line.strip())
