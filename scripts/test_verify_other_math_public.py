"""Adversarial checks for the remaining public mathematics CI gate."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from verify_other_math_public import (
    build_public_receipts,
    validate_egyptian_log,
    validate_pnp_report,
    validate_yang_replay,
    verify_adg_source_and_examples,
)


ROOT = Path(__file__).resolve().parents[1] / "remainder"


class OtherMathPublicTests(unittest.TestCase):
    def test_preserved_adg_original_accepts_only_line_ending_normalization(self):
        with TemporaryDirectory() as td:
            report = verify_adg_source_and_examples(ROOT, Path(td))
            self.assertEqual(report["standing"], "ORIGINAL_ZIP_CUSTODY_REPLAYED")
            self.assertEqual(report["original_source_sha256"],
                             "789779f75e72400ecb807019cb4c8a55cc5e08969cdcf2d5dc998621899efaa7")
            self.assertEqual(report["repository_mirror_difference"], "CRLF_TO_LF_ONLY")
            self.assertEqual(report["exact_rational_witnesses"], 5)

    def test_modified_adg_mirror_is_refused(self):
        original = ROOT / "research/admissibility-debt-geometry/source/MATH_SOLUTIONS_original_unchanged.txt"
        with TemporaryDirectory() as td:
            changed = Path(td) / "changed-source.txt"
            changed.write_bytes(original.read_bytes().replace(b"Admissibility", b"Altered-Source", 1))
            with self.assertRaisesRegex(ValueError, "mirror"):
                verify_adg_source_and_examples(ROOT, Path(td) / "output", mirror=changed)

    def test_truncated_yang_check_list_is_refused(self):
        with self.assertRaisesRegex(ValueError, "14"):
            validate_yang_replay({"passed": 13, "total": 14, "checks": {"fake": True}})

    def test_egyptian_empty_test_run_is_refused(self):
        with self.assertRaisesRegex(ValueError, "four"):
            validate_egyptian_log("TAP version 13\n1..0\n# tests 0\n# pass 0\n# fail 0\n")

    def test_egyptian_count_prefix_does_not_pass_as_four_tests(self):
        with self.assertRaisesRegex(ValueError, "four"):
            validate_egyptian_log("TAP version 13\n1..40\n# tests 40\n# pass 40\n# fail 0\n# skipped 0\n")

    def test_pnp_negative_controls_cannot_disappear(self):
        with self.assertRaisesRegex(ValueError, "10"):
            validate_pnp_report({"independent_trace_replays": 364,
                                 "negative_controls_rejected": 0,
                                 "SAT": 134, "UNSAT": 230,
                                 "historical_native_examinations_reexecuted": 0,
                                 "prior_v2_cases_reexecuted": 0})

    def test_replay_carries_400_observations_and_seven_receipt_files(self):
        with TemporaryDirectory() as td:
            output = Path(td) / "remainder-evidence"
            summary = build_public_receipts(ROOT, output)
            self.assertEqual(summary["counts"], {
                "yang_incidence_checks": 14,
                "yang_bridge_cases": 3,
                "adg_exact_examples": 5,
                "egyptian_unit_tests": 4,
                "pnp_independent_traces": 364,
                "pnp_adversarial_refusals": 10,
                "total_public_observations": 400,
            })
            self.assertEqual(summary["standing"], "PUBLIC_BOUND_EVIDENCE_ONLY")
            self.assertFalse(summary["native_newk_authenticated"])
            self.assertFalse(summary["unrestricted_theorems_certified"])
            self.assertEqual(len(summary["output_sha256"]), 6)
            for name in ("adg-custody.json", "yang-incidence.json", "yang-bridge.log",
                         "egyptian-tests.log", "pnp-new-receipts.json",
                         "pnp-test-report.json", "audit-summary.json"):
                self.assertTrue((output / name).is_file(), name)
            self.assertEqual(json.loads((output / "audit-summary.json").read_text()), summary)
            with self.assertRaises(FileExistsError):
                build_public_receipts(ROOT, output)


if __name__ == "__main__":
    unittest.main()
