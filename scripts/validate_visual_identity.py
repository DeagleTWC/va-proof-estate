#!/usr/bin/env python3
"""Bounded public-site visual identity check. No scientific or proof-status inference."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html",
    "foundation.html",
    "reviewer-route.html",
    "end-to-end.html",
    "source-reading.html",
)
INTERNAL = PAGES[1:]
LEGACY_THEME = ("#b6f2d4", "#b8f0d2", "#a4dfbe", "#b7edcd", "#1b302b")


def verify(root: Path = ROOT) -> list[str]:
    root = Path(root)
    errors: list[str] = []
    try:
        css = (root / "va-gold-design.css").read_text(encoding="utf-8")
        manifest = json.loads((root / "proof-estate-manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["unavailable visual design contract or publication manifest: " + type(exc).__name__]

    for required in (
        "--va-obsidian:#090807",
        "--va-gold:#f3cb80",
        "--va-ivory:#f5ebdb",
        "body.va-gold-site",
        ".va-sigil",
        "prefers-reduced-motion:reduce",
    ):
        if required not in css:
            errors.append("shared gold design contract incomplete: " + required)
    if "@import" in css or "url(https://" in css or "url(http://" in css:
        errors.append("visual design loads an external asset")
    if css.count("{") != css.count("}"):
        errors.append("visual design CSS braces are unbalanced")

    visual = manifest.get("visualFaceRefresh", {})
    if visual.get("publicPages") != list(PAGES) or visual.get("stylesheet") != "va-gold-design.css":
        errors.append("public visual inventory is incomplete")
    if visual.get("nativeFoundationUnchanged") is not True or visual.get("sourceStandingUnchanged") is not True:
        errors.append("visual-only release boundaries missing")

    for page in PAGES:
        try:
            html = (root / page).read_text(encoding="utf-8")
        except OSError:
            errors.append("public page missing: " + page)
            continue
        if "<main" not in html or "</main>" not in html or "<footer" not in html:
            errors.append("public page structure incomplete: " + page)
        if any(color in html.lower() for color in LEGACY_THEME):
            errors.append("old green branding visible in page source: " + page)
        if page == "index.html":
            for token in ("hero-crest", "mark-sigil", "Obsidian & Gold face"):
                if token not in html:
                    errors.append("homepage gold face missing: " + token)
            continue
        if '<body class="va-gold-site">' not in html:
            errors.append("internal page not on gold design system: " + page)
        if html.count('<link rel="stylesheet" href="va-gold-design.css">') != 1:
            errors.append("missing or duplicate shared gold stylesheet: " + page)
        for token in (
            'class="brand va-brand"',
            'class="va-sigil"',
            'class="va-name">V.A. — The Proof Estate',
            'class="va-tagline">Proof Before Power',
        ):
            if token not in html:
                errors.append("inconsistent site-wide brand: " + page + " " + token)
    return errors


if __name__ == "__main__":
    problems = verify()
    for issue in problems:
        print("PUBLIC VISUAL CONSISTENCY:", issue)
    if problems:
        raise SystemExit(1)
    print("PASS: five HTML pages share one gold identity; no obsolete green markers, external visual dependencies, or standing changes")
