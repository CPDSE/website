"""Colour tokens → CSS custom properties, with WCAG contrast assertions."""
from __future__ import annotations

import json
from pathlib import Path

from . import BuildError


def _lum(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    if len(h) != 6:
        raise BuildError(f"Token colour '{hex_colour}' must be #RRGGBB")
    chans = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in chans]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    light, dark = data["light"], data["dark"]
    if set(light) != set(dark):
        raise BuildError(f"tokens.json: light and dark define different tokens: {sorted(set(light) ^ set(dark))}")
    failures = []
    for fg, bg, minimum in data["pairs"]:
        for theme_name, theme in (("light", light), ("dark", dark)):
            ratio = contrast(theme[fg], theme[bg])
            if ratio < minimum:
                failures.append(f"{theme_name}: {fg} {theme[fg]} on {bg} {theme[bg]} = {ratio:.2f} (needs {minimum})")
    if failures:
        raise BuildError("Colour contrast below WCAG minimum:\n  " + "\n  ".join(failures))
    return data


def css(data: dict) -> str:
    def block(theme: dict, indent: str = "  ") -> str:
        return "\n".join(f"{indent}--{k}: {v};" for k, v in theme.items())

    return (
        "/* Generated from _src/tokens.json by scripts/onboarding_lib/tokens.py */\n"
        f":root {{\n  color-scheme: light;\n{block(data['light'])}\n}}\n"
        "@media (prefers-color-scheme: dark) {\n"
        f"  :root:not([data-theme=\"light\"]) {{\n    color-scheme: dark;\n{block(data['dark'], '    ')}\n  }}\n}}\n"
        f":root[data-theme=\"dark\"] {{\n  color-scheme: dark;\n{block(data['dark'])}\n}}\n"
    )
