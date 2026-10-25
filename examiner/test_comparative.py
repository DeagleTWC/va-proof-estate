#!/usr/bin/env python3
"""Positive, negative, mismatch, and forged-receipt regression checks."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

from adversarial_matrix import run_matrix, sha
from compare_reports import compare
from evidence_custody import make, verify
from session_challenge import run as session_run
from verify_matrix import integrity_check

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class PublicComparisonTests(unittest.TestCase):
    def test_matrix_comparison_and_frozen_custody(self):
        good = run_matrix([PYTHON, str(ROOT / "examiner/example_layer.py")], 20261024, 1)
        bad = run_matrix([PYTHON, str(ROOT / "examiner/negative_layer.py")], 20261024, 1)
        result = compare(good, bad, "adapter-A", "adapter-B")
        self.assertEqual(result["case_count"], 9)
        self.assertGreater(result["differing_results"], 0)
        self.assertFalse(result["native_VA_proof_established"])
        self.assertFalse(result["independent_execution_verified"])
        with tempfile.TemporaryDirectory() as folder:
            report = Path(folder) / "report.json"
            report.write_text(json.dumps(good, sort_keys=True), encoding="utf-8")
            record = make(report, "participant A", "examiner A", "bounded-adapter-A")
            self.assertEqual(verify(record, report)["status"], "LOCAL_REPORT_BYTES_AND_STRUCTURE_VERIFIED")
            report.write_text(json.dumps(good, sort_keys=True) + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                verify(record, report)
        other = run_matrix([PYTHON, str(ROOT / "examiner/example_layer.py")], 20261025, 1)
        with self.assertRaises(ValueError):
            compare(good, other, "adapter-A", "adapter-B")
        with self.assertRaises(ValueError):
            compare(good, bad, "same", "same")

    def test_self_rehashed_false_pass_is_rejected(self):
        report = run_matrix([PYTHON, str(ROOT / "examiner/example_layer.py")], 20261024, 1)
        altered = copy.deepcopy(report)
        altered["cases"][0]["passed"] = False
        item = altered["cases"][0]
        item["receipt_sha256"] = sha({k: v for k, v in item.items() if k != "receipt_sha256"})
        altered["pass_count"] = sum(int(i["passed"]) for i in altered["cases"])
        altered["report_sha256"] = sha({k: v for k, v in altered.items() if k != "report_sha256"})
        with self.assertRaises(ValueError):
            integrity_check(altered)

    def test_session_comparison_and_cross_protocol_rejection(self):
        ok = session_run([PYTHON, str(ROOT / "examiner/session_reference.py")], 20261024, 1)
        unsafe = session_run([PYTHON, str(ROOT / "examiner/session_broken.py")], 20261024, 1)
        result = compare(ok, unsafe, "system A", "system B")
        self.assertEqual(result["case_count"], 27)
        self.assertGreater(result["differing_results"], 0)
        matrix = run_matrix([PYTHON, str(ROOT / "examiner/example_layer.py")], 20261024, 1)
        with self.assertRaises(ValueError):
            compare(ok, matrix, "system A", "system B")


if __name__ == "__main__":
    unittest.main()
