#!/usr/bin/env python3
"""Negative controls for public reviewer navigation / evidence promotion."""
from __future__ import annotations
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from validate_reviewer_route import ROOT, validate


class ReviewerRouteTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="va-reviewer-route-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for path in ("reviewer-route.html", "index.html", "proofs/CLAIM-TO-CARRIER.json"):
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / path, target)
        claims = json.loads((self.root / "proofs/CLAIM-TO-CARRIER.json").read_text(encoding="utf-8"))["entries"]
        for claim in claims:
            carrier = claim.get("carrier") or claim.get("sourceTextCarrier") or claim.get("publicHistoricalSourceText")
            if carrier:
                target = self.root / carrier
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("fixture original present", encoding="utf-8")

    def alter(self, original, replacement):
        f = self.root / "reviewer-route.html"
        s = f.read_text(encoding="utf-8")
        self.assertIn(original, s)
        f.write_text(s.replace(original, replacement, 1), encoding="utf-8")

    def test_live_route_is_consistent(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_keyboard_skip_link_is_rejected(self):
        self.alter('class="skip" href="#main"', 'class="skip" href="#wrong"')
        self.assertTrue(any("keyboard skip link" in p for p in validate(self.root)))

    def test_falsified_observation_is_rejected(self):
        self.alter('data-status="DECLARED"', 'data-status="OBSERVED"')
        self.assertTrue(any("standing" in p for p in validate(self.root)))

    def test_missing_carrier_is_rejected(self):
        (self.root / "proofs/VA-AD-001/run.py").unlink()
        self.assertTrue(any("missing/unsafe original public source" in p for p in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
