#!/usr/bin/env python3
"""Adversarial tests for the data-only Aperture original-byte preflight."""
import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).with_name("verify_packet.py")
spec = importlib.util.spec_from_file_location("aperture_verifier", MODULE)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)

class ApertureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        files = ["pos-sensor.txt", "pos-receipt.txt", "neg-sensor.txt", "neg-receipt.txt",
                 "change-sensor.txt", "change-receipt.txt", "replay-sensor.txt",
                 "replay-receipt.txt", "witness-statement.txt"]
        self.originals = []
        for n in files:
            content = ("synthetic-fixture-only: " + n).encode()
            (self.root / n).write_bytes(content)
            self.originals.append({"file": n, "sha256": hashlib.sha256(content).hexdigest()})
        controls = []
        for kind, prefix, condition, outcome in [
            ("POSITIVE", "pos", "base", True), ("NEGATIVE", "neg", "revoked", False),
            ("CHANGED", "change", "changed", False), ("REPLAY", "replay", "base", True)]:
            controls.append({"kind": kind, "condition_id": condition, "measured_effect": outcome,
                             "measurement_file": prefix + "-sensor.txt",
                             "receipt_file": prefix + "-receipt.txt"})
        self.packet = {
            "schema": "VA-APERTURE-1", "packet_id": "SYNTHETIC-TEST-ONLY", "standing": "DECLARED_ONLY",
            "freeze": {"artifact_id": "fixture", "owner_id": "applicant", "artifact_sha256": "a" * 64,
                       "frozen_at": "2026-11-03T10:00:00Z", "anchor": "https://example.org/frozen"},
            "challenge": {"id": "chall-1", "examiner_id": "examiner",
                          "issued_at": "2026-11-03T11:00:00Z", "condition_summary": "Unknown changed condition"},
            "boundary": {"protected_effect": "test-only indicator",
                         "observation_scope": "fixture text only",
                         "alternate_routes": ["primary", "secondary"]},
            "controls": controls, "originals": self.originals,
            "witness": {"id": "witness", "statement_file": "witness-statement.txt"},
        }
    def verify(self, packet=None):
        return verifier.verify_packet(self.packet if packet is None else packet, self.root)
    def test_valid_synthetic_preflight_does_not_promote(self):
        result = self.verify()
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["standing"], "DECLARED_ONLY")
        self.assertIn("NOT NATIVE", result["ceiling"])
    def test_changed_measurement_must_match_original_digest(self):
        (self.root / "change-sensor.txt").write_text("tampered")
        self.assertFalse(self.verify()["ok"])
    def test_missing_original_refused(self):
        (self.root / "neg-sensor.txt").unlink()
        self.assertFalse(self.verify()["ok"])
    def test_original_path_traversal_refused(self):
        p = copy.deepcopy(self.packet)
        p["originals"][0]["file"] = "../escape"
        self.assertFalse(self.verify(p)["ok"])
    def test_duplicate_original_refused(self):
        p = copy.deepcopy(self.packet)
        p["originals"].append(p["originals"][0])
        self.assertFalse(self.verify(p)["ok"])
    def test_self_certification_refused(self):
        p = copy.deepcopy(self.packet)
        p["standing"] = "INDEPENDENTLY_REPRODUCED"
        self.assertFalse(self.verify(p)["ok"])
        p = copy.deepcopy(self.packet)
        p["independent_reproduced"] = True
        self.assertFalse(self.verify(p)["ok"])
    def test_preset_success_not_required(self):
        p = copy.deepcopy(self.packet)
        p["controls"][0]["measured_effect"] = False
        self.assertTrue(self.verify(p)["ok"]) # falsification must be reportable
    def test_incomplete_controls_refused(self):
        p = copy.deepcopy(self.packet)
        p["controls"].pop()
        self.assertFalse(self.verify(p)["ok"])
    def test_bad_chronology_refused(self):
        p = copy.deepcopy(self.packet)
        p["challenge"]["issued_at"] = p["freeze"]["frozen_at"]
        self.assertFalse(self.verify(p)["ok"])
    def test_changed_not_changed_refused(self):
        p = copy.deepcopy(self.packet)
        p["controls"][2]["condition_id"] = "base"
        self.assertFalse(self.verify(p)["ok"])
    def test_replay_not_base_refused(self):
        p = copy.deepcopy(self.packet)
        p["controls"][3]["condition_id"] = "other"
        self.assertFalse(self.verify(p)["ok"])
    def test_cross_control_evidence_reuse_refused(self):
        p = copy.deepcopy(self.packet)
        p["controls"][1]["receipt_file"] = "pos-receipt.txt"
        self.assertFalse(self.verify(p)["ok"])
    def test_no_independent_identity_conferred(self):
        p = copy.deepcopy(self.packet)
        p["challenge"]["examiner_id"] = "applicant"
        self.assertFalse(self.verify(p)["ok"])
    def test_symlink_original_refused(self):
        target = self.root / "pos-sensor.txt"
        target.unlink()
        target.symlink_to(self.root / "neg-sensor.txt")
        self.assertFalse(self.verify()["ok"])
    def test_schema_change_refused(self):
        p = copy.deepcopy(self.packet)
        p["schema"] = "VA-APERTURE-2"
        self.assertFalse(self.verify(p)["ok"])
    def test_cli_run_success_and_failure(self):
        p = self.root / "packet.json"
        p.write_text(json.dumps(self.packet), encoding="utf-8")
        self.assertEqual(verifier.main([str(p), "--originals", str(self.root)]), 0)
        p.write_text("{}")
        self.assertEqual(verifier.main([str(p), "--originals", str(self.root)]), 2)

if __name__=="__main__":
    unittest.main()
