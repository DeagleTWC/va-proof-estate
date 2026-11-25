"""Regression checks for the read-only Navier public evidence runner."""

import json
import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from verify_navier_public_evidence import (
    build_public_receipts,
    validate_edge_receipt,
    validate_midpoint_receipt,
    validate_source_tree,
    validate_unittest_result,
)


ROOT = Path(__file__).resolve().parents[1] / "research" / "navier-stokes"


class NavierEvidenceVerificationTests(unittest.TestCase):
    def test_missing_inputs_are_refused(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "missing"):
                validate_source_tree(Path(tmp))

    def test_changed_frozen_source_is_refused(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "navier-stokes"
            shutil.copytree(ROOT, root)
            original = root / "05_REPRODUCIBILITY/original_edge_rate_input_unmodified.json"
            original.write_text(original.read_text() + "\n")
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                validate_source_tree(root)

    def test_zero_discovered_tests_are_refused(self):
        with self.assertRaisesRegex(ValueError, "19"):
            validate_unittest_result("Ran 0 tests in 0.000s\n\nOK\n", expected=19)

    def test_partial_edge_receipt_is_refused(self):
        with self.assertRaisesRegex(ValueError, "11"):
            validate_edge_receipt({"passed": 10, "total": 11, "checks": {"false_pass": False}})

    def test_midpoint_claim_promotion_is_refused(self):
        with self.assertRaisesRegex(ValueError, "scope"):
            validate_midpoint_receipt({
                "status": "PASS",
                "counts": {"passed": 17, "failed": 0, "total": 17},
                "checks": [{"passed": True}] * 17,
                "scope": "Unrestricted regularity proved for all smooth data",
            })

    def test_fresh_run_binds_all_51_checks_to_sources_and_replays(self):
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "navier-public-receipts"
            summary = build_public_receipts(ROOT, out)
            self.assertEqual(summary["checks"], {
                "edge": 11, "movement": 19, "refinement": 4, "midpoint": 17,
                "passed": 51, "total": 51,
            })
            self.assertEqual(summary["standing"], "FINITE_PUBLIC_EVIDENCE_ONLY")
            self.assertFalse(summary["native_generator_authenticated"])
            self.assertFalse(summary["unrestricted_regularity_certified"])
            self.assertEqual(len(summary["source_sha256"]), 12)
            for name in ("edge.json", "midpoint.json", "movement-receipt.json",
                         "movement-tests.log", "refinement-tests.log", "source-sha256.json",
                         "audit-summary.json"):
                self.assertTrue((out / name).is_file(), name)
            self.assertEqual(json.loads((out / "audit-summary.json").read_text()), summary)
            with self.assertRaises(FileExistsError):
                build_public_receipts(ROOT, out)

    def test_relative_receipt_directory_is_resolved_before_subprocess(self):
        with TemporaryDirectory(dir=".") as tmp:
            out = Path(os.path.relpath(tmp, Path.cwd())) / "navier-relative"
            self.assertFalse(out.is_absolute())
            result = build_public_receipts(ROOT, out)
            self.assertEqual(result["checks"]["passed"], 51)
            self.assertTrue((out / "midpoint.json").is_file())


if __name__ == "__main__":
    unittest.main()
