"""Exact source-bound model-gate, changed-condition, and replay tests."""

from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from consequence_signature_child_v1 import generate, verify_receipt, example_candidates


PDF = Path(__file__).with_name(
    "Universal_Resolving_Structure_Consequence_Signature_Calculus_v1_2026-04-30.pdf"
)


def candidate():
    return {
        "state_id": "x0", "restart_id": "r0",
        "viable_by_restart": {"r1": [], "r0": ["x1", "x0"]},
        "capacity": "7/2", "burden": "2", "admissibility": "0",
        "authority": "1", "breach": "0", "coherence": "5/4",
        "minimum_coherence": "1",
        "derivatives": {"reserve": "0", "admissibility": "0", "authority": "0",
                        "viability": "0", "breach": "0", "coherence": "0"},
    }


class ConsequenceSignatureChildTests(unittest.TestCase):
    def gate(self, item):
        return generate(item, source_pdf=PDF)

    def test_original_binding_conjunction_produces_exact_bind(self):
        receipt = self.gate(candidate())
        self.assertEqual(receipt["standing"], "BIND")
        self.assertTrue(receipt["bind_criterion_satisfied"])
        self.assertEqual(receipt["signature"]["remaining_capacity"], "3/2")
        self.assertEqual(len(receipt["invariants"]), 5)
        self.assertTrue(all(receipt["invariants"].values()))
        self.assertFalse(receipt["warning"])
        self.assertFalse(receipt["native_generator_authenticated"])
        self.assertTrue(verify_receipt(receipt, source_pdf=PDF))

    def test_capacity_overrun_refuses(self):
        q = candidate();q["burden"] = "4"
        self.assertEqual(self.gate(q)["standing"], "REFUSE")

    def test_admissibility_refuses(self):
        q = candidate();q["admissibility"] = "-1/10"
        self.assertFalse(self.gate(q)["invariants"]["capacity_and_admissibility"])

    def test_revoked_standing_refuses_before_consequence(self):
        q = candidate();q["authority"] = "0"
        r = self.gate(q)
        self.assertEqual(r["standing"], "REFUSE")
        self.assertFalse(r["invariants"]["standing"])
        self.assertNotEqual(r["receipt_sha256"], self.gate(candidate())["receipt_sha256"])

    def test_missing_viable_restart_corridor_refuses(self):
        q = candidate();q["restart_id"] = "r1"
        self.assertFalse(self.gate(q)["invariants"]["viability"])

    def test_nonzero_breach_refuses(self):
        q = candidate();q["breach"] = "1/3"
        self.assertEqual(self.gate(q)["standing"], "REFUSE")

    def test_coherence_below_declared_floor_refuses(self):
        q = candidate();q["minimum_coherence"] = "3/2"
        self.assertFalse(self.gate(q)["invariants"]["coherence"])

    def test_derivative_warning_pauses_even_when_bind_conjunction_holds(self):
        q = candidate();q["derivatives"]["reserve"] = "-1/10"
        r = self.gate(q)
        self.assertTrue(r["bind_criterion_satisfied"])
        self.assertTrue(r["warning"])
        self.assertEqual(r["standing"], "PAUSE")

    def test_rising_breach_derivative_pauses(self):
        q = candidate();q["derivatives"]["breach"] = "1/5"
        self.assertEqual(self.gate(q)["standing"], "PAUSE")

    def test_hard_refusal_dominates_warning(self):
        q = candidate();q["authority"] = "0";q["derivatives"]["reserve"] = "-1"
        self.assertEqual(self.gate(q)["standing"], "REFUSE")

    def test_input_order_and_viability_order_do_not_change_receipt(self):
        q = candidate()
        reversed_q = dict(reversed(list(q.items())))
        reversed_q["viable_by_restart"] = {"r0": ["x0", "x1"], "r1": []}
        self.assertEqual(self.gate(q), self.gate(reversed_q))

    def test_float_or_missing_derivative_is_refused(self):
        q = candidate();q["burden"] = 0.1
        with self.assertRaises((TypeError, ValueError)):
            self.gate(q)
        q = candidate();del q["derivatives"]["coherence"]
        with self.assertRaises(ValueError):
            self.gate(q)

    def test_forged_claim_rate_or_hash_fails_source_regeneration(self):
        for field,value in (("standing", "BIND"), ("receipt_sha256", "0"*64),
                            ("native_generator_authenticated", True)):
            q = candidate();q["authority"] = "0"
            r = self.gate(q)
            r[field] = value
            self.assertFalse(verify_receipt(r, source_pdf=PDF), field)

    def test_wrong_source_pdf_refused(self):
        with TemporaryDirectory() as td:
            wrong = Path(td) / "wrong.pdf";wrong.write_bytes(b"wrong math")
            with self.assertRaisesRegex(ValueError, "source"):
                generate(candidate(), source_pdf=wrong)

    def test_three_deterministic_demo_receipts_replay_and_existing_dir_refused(self):
        with TemporaryDirectory() as td:
            output = Path(td) / "receipts"
            script = Path(__file__).with_name("consequence_signature_child_v1.py")
            r = subprocess.run([sys.executable, str(script), "--demo", "--receipt-dir",
                                str(output), "--source-pdf", str(PDF)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            for standing in ("BIND", "REFUSE", "PAUSE"):
                file = output / (standing.lower() + "-receipt.json")
                self.assertTrue(file.exists(), standing)
                v = subprocess.run([sys.executable, str(script), "--verify", str(file),
                                    "--source-pdf", str(PDF)],capture_output=True,text=True)
                self.assertEqual(v.returncode, 0, v.stderr)
            second = subprocess.run([sys.executable, str(script), "--demo", "--receipt-dir",
                                     str(output), "--source-pdf", str(PDF)],
                                    capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)


if __name__ == "__main__":
    unittest.main()
