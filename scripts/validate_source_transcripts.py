#!/usr/bin/env python3
"""Validate searchable public PDF text extractions without treating them as original PDFs."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("shift-proof-estate-challenge-standard-v1-extracted.md", "3d355e5e67e1205833a39275c51370481bacfec234fd90aa73178683e137e5a6", 15, list(range(1,16))),
    ("true-zero-consequence-systems-science-v1.2.3-extracted.md", "b629104cbcb541f26e5b78a3468f0621ac759ed1f46da2903ad95315fa4b759c", 17, list(range(2,18))),
    ("independent-reviewer-standard-v1-extracted.md", "a3a8dd7c9fd3fda44a62eba1c6ae116344853faef94ae4db5a76902e5681f9c9", 7, list(range(1,8))),
]

def main():
    for name, original_hash, total, expected in SOURCES:
        path = ROOT / "proofs" / "sources" / name
        text = path.read_text(encoding="utf-8")
        assert original_hash in text, name + ": original PDF digest missing"
        found = [int(x) for x in re.findall(r"^## Source PDF page (\d+) of (\d+)$", text, flags=re.M)
                 if x[1] == str(total)]
        assert found == expected, f"{name}: page coverage mismatch: {found}"
        assert "Not" in text and "original PDF" in text
        assert len(text) > 5000
        print("PASS:", name, f"extracted PDF pages {found[0]}–{found[-1]}/{total}")
    mapping = (ROOT / "proofs" / "SOURCE-TO-CLAIM-MAP.md").read_text(encoding="utf-8")
    for name, _, _, _ in SOURCES:
        assert name in mapping, "Missing crosswalk target: " + name
    print("PASS: original-document identity, page extraction and source crosswalk")
if __name__ == "__main__":
    main()
