"""Exact positive, adversarial, and replay controls for the movement kernel."""

from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import unittest

from urk_movement_kernel_v1 import Q, ZERO, generate, projection, verify_receipt


def seed():
    # Two interacting real transverse modes, plus an initially empty child.
    a, b, c = (1, 0, 0), (0, 2, 0), (1, 2, 0)
    velocity = {a: (ZERO, Q(1), ZERO),
                b: (Q(1), ZERO, ZERO),
                c: (ZERO, ZERO, ZERO)}
    return {**velocity, **{tuple(-x for x in k): v for k, v in velocity.items()}}


def original_source_seed():
    path = (Path(__file__).resolve().parent.parent /
            "04_PUBLIC_COMPANION" / "urk_harmonic_edge_input.json")
    source = json.loads(path.read_text(encoding="utf-8"))
    return {tuple(row["k"]): tuple(Q(Fraction(str(c[0])), Fraction(str(c[1])))
                                   for c in row["u"]) for row in source["modes"]}


class KernelTests(unittest.TestCase):
    def test_parent_constraint_projection_is_exact(self):
        v = projection((1, 2, 0), (Q(2), Q(1), ZERO))
        self.assertEqual(v, (Q(Fraction(6, 5)), Q(Fraction(-3, 5)), ZERO))

    def test_regeneration_creates_nonzero_empty_child_rate(self):
        receipt = generate(seed())
        self.assertEqual(receipt["standing"], "RUN")
        self.assertEqual(receipt["generated_nonlinear_rates"]["1,2,0"],
                         [["0", "-6/5"], ["0", "3/5"], ["0", "0"]])
        self.assertEqual(receipt["advective_energy_transfer"], "0")
        self.assertEqual(receipt["energy_balance_residual"], "0")
        self.assertGreater(receipt["nonzero_projected_pair_count"], 0)
        self.assertTrue(verify_receipt(receipt))

    def test_archived_six_mode_source_exactly_regenerated(self):
        receipt = generate(original_source_seed())
        self.assertEqual(receipt["mode_count"], 6)
        self.assertEqual(receipt["ordered_pair_count"], 30)
        self.assertEqual(receipt["generated_nonlinear_rates"]["1,2,0"],
                         [["-3/10485760", "0"],
                          ["3/20971520", "0"], ["0", "1/4194304"]])
        self.assertEqual(receipt["energy_balance_residual"], "0")
        self.assertTrue(verify_receipt(receipt))

    def test_all_generated_children_match_archived_numerical_specialization(self):
        source_path = (Path(__file__).resolve().parent.parent /
                       "04_PUBLIC_COMPANION" / "urk_harmonic_edge_rates.py")
        input_path = source_path.with_name("urk_harmonic_edge_input.json")
        spec = importlib.util.spec_from_file_location("archived_edges", source_path)
        self.assertIsNotNone(spec)
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        numerical = old.compute(json.loads(input_path.read_text(encoding="utf-8")))
        exact = generate(original_source_seed())
        self.assertEqual(numerical["generated_ordered_edge_count"], 30)
        self.assertEqual(len(numerical["phases"]), exact["generated_output_mode_count"])
        for item in numerical["phases"]:
            key = ",".join(str(k) for k in item["phase"])
            rates = exact["generated_nonlinear_rates"][key]
            for i in range(3):
                for j in range(2):
                    self.assertAlmostEqual(float(Fraction(rates[i][j])),
                                           item["nonlinear_amplitude_rate"][i][j],
                                           places=14, msg=key)

    def test_reordering_input_does_not_change_receipt(self):
        modes = seed()
        self.assertEqual(generate(modes), generate(dict(reversed(list(modes.items())))))

    def test_mass_density_scales_energy_not_movement(self):
        a = generate(seed(), mass_density=Fraction(1))
        b = generate(seed(), mass_density=Fraction(2))
        self.assertEqual(b["generated_nonlinear_rates"], a["generated_nonlinear_rates"])
        self.assertEqual(Fraction(b["viscous_dissipation"]),
                         2 * Fraction(a["viscous_dissipation"]))

    def test_mass_and_capacity_define_exact_remaining_room(self):
        r = generate(seed(), mass_density=Fraction(2),
                     kinetic_capacity=Fraction(5))
        self.assertEqual(r["initial_kinetic_energy"], "4")
        self.assertEqual(r["remaining_capacity"], "1")
        self.assertTrue(r["gates"]["declared_capacity_if_supplied"])
        self.assertEqual(r["standing"], "RUN")
        self.assertTrue(verify_receipt(r))

    def test_insufficient_remaining_room_aborts_candidate(self):
        r = generate(seed(), kinetic_capacity=Fraction(1))
        self.assertEqual(r["remaining_capacity"], "-1")
        self.assertEqual(r["standing"], "ABORT")
        self.assertFalse(r["gates"]["declared_capacity_if_supplied"])
        self.assertTrue(verify_receipt(r))

    def test_missing_conjugate_refused(self):
        modes = seed()
        del modes[(-1, 0, 0)]
        with self.assertRaisesRegex(ValueError, "conjugate"):
            generate(modes)

    def test_contradictory_conjugate_refused(self):
        modes = seed()
        modes[(-1, 0, 0)] = (ZERO, Q(2), ZERO)
        with self.assertRaisesRegex(ValueError, "conjugate"):
            generate(modes)

    def test_non_solenoidal_movement_refused(self):
        modes = seed()
        modes[(1, 0, 0)] = (Q(1), ZERO, ZERO)
        modes[(-1, 0, 0)] = (Q(1), ZERO, ZERO)
        with self.assertRaisesRegex(ValueError, "incompressible"):
            generate(modes)

    def test_zero_viscosity_refused(self):
        with self.assertRaisesRegex(ValueError, "viscosity"):
            generate(seed(), viscosity=Fraction(0))

    def test_negative_mass_density_refused(self):
        with self.assertRaisesRegex(ValueError, "mass density"):
            generate(seed(), mass_density=Fraction(-1))

    def test_float_input_refused(self):
        with self.assertRaises(TypeError):
            Q(0.1)

    def test_global_regular_claim_is_paused(self):
        r = generate(seed(), requested_claim="UNRESTRICTED_REGULARITY")
        self.assertEqual(r["standing"], "PAUSE")
        self.assertFalse(r["unrestricted_proof"])
        self.assertTrue(verify_receipt(r))

    def test_blowup_claim_is_paused(self):
        r = generate(seed(), requested_claim="FINITE_TIME_BLOWUP")
        self.assertEqual(r["standing"], "PAUSE")

    def test_claim_cannot_be_lifted_by_receipt_edit(self):
        r = generate(seed())
        r["standing"] = "RUN"
        r["scope"] = "UNRESTRICTED_REGULARITY"
        self.assertFalse(verify_receipt(r))

    def test_tampered_nonlinear_rate_refused(self):
        r = generate(seed())
        r["generated_nonlinear_rates"]["1,2,0"][0][1] = "999"
        self.assertFalse(verify_receipt(r))

    def test_receipt_hash_tampering_refused(self):
        r = generate(seed())
        r["receipt_sha256"] = "0" * 64
        self.assertFalse(verify_receipt(r))


if __name__ == "__main__":
    unittest.main()
