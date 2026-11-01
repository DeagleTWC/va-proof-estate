#!/usr/bin/env python3
"""Negative controls for dated scientific-cycle continuity audit."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_scientific_cycle_consistency import ROOT, validate

FILES = [
    "proofs/SCIENTIFIC-CYCLE-CURRENT.json",
    "proofs/VA-ORIGINAL-CAPABILITY-RECOVERY.json",
    "milestones/M33-EVIDENCE-CONTINUITY.json",
    "README.md",
    "proofs/README.md",
    "proofs/VA-ORIGINAL-CAPABILITY-RECOVERY.md",
    ".github/workflows/public-proof-integrity.yml",
]


class CycleContinuityTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="va-cycle-continuity-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for file in FILES:
            path = self.root / file
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / file, path)

    def change_json(self, path, callback):
        file = self.root / path
        item = json.loads(file.read_text(encoding="utf-8"))
        callback(item)
        file.write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")

    def test_dated_continuity_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_old_current_hold_statement_rejected(self):
        path = self.root / "proofs/README.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nM27 HOLD; M28 NOT OPEN\n", encoding="utf-8")
        self.assertTrue(any("Misleading active" in x for x in validate(self.root)))

    def test_historical_source_cannot_override_current_cycle(self):
        self.change_json("proofs/VA-ORIGINAL-CAPABILITY-RECOVERY.json",
                         lambda d: d.update({"notCurrentCycleStatus": False}))
        self.assertTrue(any("not distinguished" in x for x in validate(self.root)))

    def test_m28_opening_cannot_be_called_empirically_certified(self):
        self.change_json("proofs/SCIENTIFIC-CYCLE-CURRENT.json",
                         lambda d: d["authoritativeCurrentCycle"].update({
                             "M28ScientificResultCertifiedByThisRecord": True
                         }))
        self.assertTrue(any("incorrectly promoted" in x for x in validate(self.root)))

    def test_publication_is_not_experimental_proof(self):
        self.change_json("milestones/M33-EVIDENCE-CONTINUITY.json",
                         lambda d: d["progression"][-1].update({
                             "classification": "empirical_scientific_pass"
                         }))
        self.assertTrue(any("without empirical carrier" in x for x in validate(self.root)))

    def test_ci_metadata_not_a_project_wide_authority(self):
        file = self.root / ".github/workflows/public-proof-integrity.yml"
        s = file.read_text(encoding="utf-8")
        s = s.replace('"M28AuthorizedByThisCI":false', '"M28Authorized":false')
        file.write_text(s, encoding="utf-8")
        self.assertTrue(any("unscoped scientific-cycle flags" in x for x in validate(self.root)))

    def test_dated_m28_does_not_reset_later_work(self):
        self.change_json("proofs/SCIENTIFIC-CYCLE-CURRENT.json",
                         lambda d: d["datedSnapshotInterpretation"].update({
                             "doNotResetLaterRecordedProgression": False
                         }))
        self.assertTrue(any("dated-snapshot reset" in x for x in validate(self.root)))

    def test_m29_reference_not_promoted_into_native_result(self):
        self.change_json("milestones/M33-EVIDENCE-CONTINUITY.json",
                         lambda d: d["datedScientificReconciliation"]["laterM29"].update({
                             "nativeResultCarrierAttachedByThisIndex": True
                         }))
        self.assertTrue(any("incorrectly promoted" in x for x in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
