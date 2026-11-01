#!/usr/bin/env python3
"""Negative controls for formal-record source/carrier traceability."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_public_formal_sources import ROOT, validate

SOURCES = [
    "index.html",
    "proofs/CLAIM-TO-CARRIER.json",
    "proofs/SOURCE-ESTATE.md",
    "proofs/sources/true-zero-consequence-systems-science-v1.2.3-extracted.md",
]


class FormalSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="va-formal-source-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for source in SOURCES:
            path = self.root / source
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / source, path)

    def test_current_formal_sources_match(self):
        self.assertEqual(validate(self.root), [])

    def test_bad_original_hash_rejected(self):
        p = self.root / "index.html"
        s = p.read_text(encoding="utf-8").replace(
            "b629104cbcb541f26e5b78a3468f0621ac759ed1f46da2903ad95315fa4b759c",
            "0" * 64, 1)
        p.write_text(s, encoding="utf-8")
        self.assertTrue(any("differs from registered" in x for x in validate(self.root)))

    def test_missing_transcript_rejected(self):
        (self.root / SOURCES[-1]).unlink()
        self.assertTrue(any("transcript path" in x for x in validate(self.root)))

    def test_false_source_absence_rejected(self):
        p = self.root / "index.html"
        p.write_text(p.read_text(encoding="utf-8") + "\nindividual source hash not bundled",
                     encoding="utf-8")
        self.assertTrue(any("False source-hash" in x for x in validate(self.root)))

    def test_evidence_promotion_rejected(self):
        p = self.root / "proofs/CLAIM-TO-CARRIER.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        next(x for x in d["entries"] if x["id"] == "VA-F02")["standing"] = "OBSERVED"
        p.write_text(json.dumps(d), encoding="utf-8")
        self.assertTrue(any("wrongly promoted" in x for x in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
