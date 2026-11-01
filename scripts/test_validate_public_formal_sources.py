#!/usr/bin/env python3
"""Negative controls for source-linked public True Zero / corrected NEW-K claims."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_public_formal_sources import ROOT, validate

SOURCE_PATHS = [
    "index.html",
    "proof-estate-manifest.json",
    "proofs/CLAIM-TO-CARRIER.json",
    "proofs/SOURCE-ESTATE.md",
    "proofs/sources/true-zero-consequence-systems-science-v1.2.3-extracted.md",
    "proofs/sources/shift-proof-estate-challenge-standard-v1-extracted.md",
    "proofs/sources/shift-public-proof-path-v2-extracted.md",
    "proofs/sources/independent-reviewer-standard-v1-extracted.md",
]
SOURCE_HASH = "b629104cbcb541f26e5b78a3468f0621ac759ed1f46da2903ad95315fa4b759c"


class SourceLinkedClaimsTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="va-public-source-linked-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for source in SOURCE_PATHS:
            target = self.root / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / source, target)

    def alter_text(self, source, target, new, count=1):
        path = self.root / source
        text = path.read_text(encoding="utf-8")
        self.assertIn(target, text)
        path.write_text(text.replace(target, new, count), encoding="utf-8")

    def alter_json(self, source, callback):
        path = self.root / source
        doc = json.loads(path.read_text(encoding="utf-8"))
        callback(doc)
        path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

    def test_all_nine_claims_and_four_pdf_hashes_match(self):
        self.assertEqual(validate(self.root), [])

    def test_wrong_pdf_hash_in_frontend_rejected(self):
        self.alter_text("index.html", SOURCE_HASH, "0" * 64)
        self.assertTrue(any("differs from registered" in x for x in validate(self.root)))

    def test_source_link_omission_rejected(self):
        self.alter_text("index.html", "link.href=record.sourceTextCarrier", "link.href='#'")
        self.assertTrue(any("Public claim links/exports" in x for x in validate(self.root)))

    def test_missing_original_transcript_rejected(self):
        (self.root / "proofs/sources/true-zero-consequence-systems-science-v1.2.3-extracted.md").unlink()
        self.assertTrue(any("transcript does not identify" in x for x in validate(self.root)))

    def test_false_source_absence_rejected(self):
        path = self.root / "index.html"
        path.write_text(path.read_text(encoding="utf-8") + "\nindividual source hash not bundled\n",
                        encoding="utf-8")
        self.assertTrue(any("False source-hash" in x for x in validate(self.root)))

    def test_formal_evidence_promotion_rejected(self):
        self.alter_json("proofs/CLAIM-TO-CARRIER.json",
                        lambda d: next(r for r in d["entries"] if r["id"] == "VA-F02").update(
                            {"standing": "OBSERVED"}))
        self.assertTrue(any("incorrectly promoted" in x for x in validate(self.root)))

    def test_unlinked_native_source_rejected(self):
        self.alter_text("index.html", "proofs/sources/true-zero-consequence-systems-science-v1.2.3-extracted.md",
                        "proofs/sources/forged.md", count=3)
        self.assertTrue(any("front-end sourceTextCarrier differs" in x for x in validate(self.root)))

    def test_incomplete_original_hash_manifest_rejected(self):
        self.alter_json("proof-estate-manifest.json",
                        lambda d: d["sourceOriginalPdfSHA256"].pop(
                            "Public_Independent_Reviewer_Qualification_Standard_v1.0(2).pdf"))
        self.assertTrue(any("four recorded identities" in x for x in validate(self.root)))

    def test_malformed_claim_object_separator_rejected(self):
        self.alter_text("index.html", "',sourceTextCarrier:", "',,sourceTextCarrier:", count=3)
        self.assertTrue(any("malformed JavaScript separator" in x for x in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
