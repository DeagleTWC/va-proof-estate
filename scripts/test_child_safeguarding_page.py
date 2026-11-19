#!/usr/bin/env python3
"""Public-safe child-safeguarding examination page contract tests.

These tests validate published wording and navigation, not a V.A. kernel.
"""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ChildSafeguardingPageTests(unittest.TestCase):
    def test_review_route_links_to_public_case(self):
        reviewer = (ROOT / "reviewer-route.html").read_text(encoding="utf-8")
        self.assertIn('href="child-safeguarding.html"', reviewer)

    def test_public_case_has_explicit_evidence_ceiling(self):
        page = (ROOT / "child-safeguarding.html").read_text(encoding="utf-8")
        for phrase in (
            "CHILD-GOV-KERN-1",
            "DECLARED — EXAMINATION SPECIFICATION",
            "No observed V.A. child-safeguarding run",
            "No independent reproduction",
            "No real children or personal records",
            "Positive control",
            "Negative control",
            "Changed condition",
            "Alternate routes",
            "Independent replay",
            "What would falsify this case?",
            "Human responsibility and appeal",
            "What child-safeguarding groups can lead",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, page)

    def test_no_claim_of_deployment_or_live_collection(self):
        page = (ROOT / "child-safeguarding.html").read_text(encoding="utf-8")
        for forbidden in ("Deployable now", "certified child protection", "<script", "<form"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, page)
        self.assertIn('href="https://github.com/DeagleTWC/va-proof-estate/issues/new?template=bounded-proof-review.md"', page)


if __name__ == "__main__":
    unittest.main()
