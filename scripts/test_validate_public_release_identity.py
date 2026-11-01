#!/usr/bin/env python3
"""Release-lineage and publication-version negative controls."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_public_release_identity import ROOT, validate


PATHS = [
    "proof-estate-manifest.json",
    "index.html",
    "foundation.html",
    "README.md",
    "proofs/VERSION-IDENTITY.md",
    "proofs/MILESTONE-LEDGER.md",
]


class PublicReleaseIdentityTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="va-release-identity-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for path in PATHS:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / path, target)

    def mutate(self, mutate):
        target = self.root / "proof-estate-manifest.json"
        obj = json.loads(target.read_text(encoding="utf-8"))
        mutate(obj)
        target.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")

    def test_current_release_is_consistent(self):
        self.assertEqual(validate(self.root), [])

    def test_changed_homepage_is_detected(self):
        target = self.root / "index.html"
        target.write_text(target.read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")
        self.assertTrue(any("byte digest" in x for x in validate(self.root)))

    def test_stale_manifest_disambiguation_is_detected(self):
        self.mutate(lambda d: d["versionDisambiguation"].update({"publicationRelease": "2.0"}))
        self.assertTrue(any("publication release is stale" in x for x in validate(self.root)))

    def test_history_cannot_be_relabelled(self):
        self.mutate(lambda d: d["previousWebsiteRelease"].update({"release": "0.0"}))
        self.assertTrue(any("retained history" in x for x in validate(self.root)))

    def test_challenge_schema_is_distinct_from_site_version(self):
        self.mutate(lambda d: d["versionDisambiguation"].update({"challengePacketSchema": "VA-CHALLENGE-2.2"}))
        self.assertTrue(any("schema and website" in x for x in validate(self.root)))

    def test_foundation_page_cannot_use_stale_release(self):
        path = self.root / "foundation.html"
        s = path.read_text(encoding="utf-8").replace("WEBSITE RELEASE 2.2", "RELEASE 2.0")
        path.write_text(s, encoding="utf-8")
        self.assertTrue(any("foundation.html lacks" in x for x in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
