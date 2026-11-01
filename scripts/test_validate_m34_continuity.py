#!/usr/bin/env python3
"""Negative controls for the public continuity validator; synthetic file tampering only."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_m34_continuity import ROOT, validate


class ContinuityIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="va-continuity-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        index = json.loads((ROOT / "milestones/M33-EVIDENCE-CONTINUITY.json").read_text(encoding="utf-8"))
        paths = {
            "milestones/M33-EVIDENCE-CONTINUITY.json",
            "milestones/DEAGLE-TRUE-ZERO-BOT-CONTINUITY.json",
            "proof-estate-manifest.json",
            "proofs/CLAIM-TO-CARRIER.json",
            "index.html",
            "README.md",
        }
        for row in index["progression"]:
            paths.add(str((Path("milestones") / (row.get("path") or row.get("record"))).as_posix()))
        for row in index["carriers"]:
            paths.add(str((Path("milestones") / row["path"]).as_posix()))
        for path in paths:
            source = (ROOT / path).resolve()
            relative = source.relative_to(ROOT)
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    def modify(self, path, fn):
        target = self.root / path
        doc = json.loads(target.read_text(encoding="utf-8"))
        fn(doc)
        target.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

    def test_intact_metadata_is_accepted(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_original_reference_is_detected(self):
        (self.root / "proofs/HISTORICAL-PILOT-CARRIER-CROSSWALK.md").unlink()
        self.assertTrue(any("Missing linked carrier" in x for x in validate(self.root)))

    def test_stale_bot_handoff_is_detected(self):
        self.modify("milestones/DEAGLE-TRUE-ZERO-BOT-CONTINUITY.json",
                    lambda d: d["continuity"].update({"current": "M31", "next_on_request": "M32"}))
        self.assertTrue(any("Bot continuity snapshot is stale" in x for x in validate(self.root)))

    def test_publication_is_not_promoted_to_empirical_proof(self):
        self.modify("milestones/M33-EVIDENCE-CONTINUITY.json",
                    lambda d: d["progression"][5].update({"classification": "independently_reproduced"}))
        self.assertTrue(any("promoted as empirical proof" in x for x in validate(self.root)))

    def test_claim_standing_drift_is_detected(self):
        self.modify("proofs/CLAIM-TO-CARRIER.json",
                    lambda d: d["entries"][1].update({"standing": "OBSERVED"}))
        self.assertTrue(any("DECLARED count differs" in x for x in validate(self.root)))

    def test_foundation_invariant_drift_is_detected(self):
        self.modify("milestones/M33-EVIDENCE-CONTINUITY.json",
                    lambda d: d["foundation"].update({"invariant": "altered"}))
        self.assertTrue(any("lineage invariant changed" in x for x in validate(self.root)))

    def test_homepage_navigation_missing_is_detected(self):
        path = self.root / "index.html"
        s = path.read_text(encoding="utf-8").replace('id="evidence-continuity"', 'id="removed-route"')
        path.write_text(s, encoding="utf-8")
        self.assertTrue(any("Homepage lacks public evidence navigation" in x for x in validate(self.root)))

    def test_carrier_escape_is_detected(self):
        self.modify("milestones/M33-EVIDENCE-CONTINUITY.json",
                    lambda d: d["carriers"][0].update({"path": "../../../../etc/passwd"}))
        self.assertTrue(any("escapes repository" in x for x in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
