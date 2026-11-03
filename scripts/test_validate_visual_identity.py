#!/usr/bin/env python3
"""Disposable negative controls for the V.A. public gold site presentation."""
import json
import shutil
import tempfile
from pathlib import Path

from validate_visual_identity import ROOT, PAGES, verify


def run() -> None:
    with tempfile.TemporaryDirectory(prefix="va-public-visual-") as d:
        root = Path(d)
        for path in (*PAGES, "va-gold-design.css", "proof-estate-manifest.json"):
            shutil.copy2(ROOT / path, root / path)

        assert verify(root) == [], verify(root)

        css_link = '<link rel="stylesheet" href="va-gold-design.css">'
        page = root / "foundation.html"
        text = page.read_text(encoding="utf-8")
        page.write_text(text.replace(css_link, "", 1), encoding="utf-8")
        assert any("missing or duplicate shared gold stylesheet" in x for x in verify(root))
        page.write_text(text, encoding="utf-8")

        page = root / "reviewer-route.html"
        text = page.read_text(encoding="utf-8")
        page.write_text(text.replace('class="va-sigil"', 'class="old-logo"', 1), encoding="utf-8")
        assert any("inconsistent site-wide brand" in x for x in verify(root))
        page.write_text(text, encoding="utf-8")

        page = root / "source-reading.html"
        text = page.read_text(encoding="utf-8")
        page.write_text(text.replace("</style>", ".test{color:#b6f2d4}</style>", 1), encoding="utf-8")
        assert any("old green branding visible" in x for x in verify(root))
        page.write_text(text, encoding="utf-8")

        manifest_file = root / "proof-estate-manifest.json"
        original_manifest = manifest_file.read_text(encoding="utf-8")
        record = json.loads(original_manifest)
        record["visualFaceRefresh"]["publicPages"] = ["index.html"]
        manifest_file.write_text(json.dumps(record), encoding="utf-8")
        assert any("public visual inventory is incomplete" in x for x in verify(root))
        manifest_file.write_text(original_manifest, encoding="utf-8")

        css = root / "va-gold-design.css"
        original_css = css.read_text(encoding="utf-8")
        css.write_text(original_css + "\\n@import url(https://untrusted.example/styles.css);\\n", encoding="utf-8")
        assert any("external asset" in x for x in verify(root))
        css.write_text(original_css, encoding="utf-8")
        assert verify(root) == [], verify(root)
    print("PASS: visual identity, gold-only palette, CSS custody and five synthetic negative controls")


if __name__ == "__main__":
    run()
