"""Exact controls for the source's abstract nested-basin countermodel."""

from fractions import Fraction
import unittest

from refinement_countermodel import origin_state, conserves


class RefinementCountermodelTests(unittest.TestCase):
    def test_exact_origin_branch(self):
        for depth in (0, 1, 2, 8):
            with self.subTest(depth=depth):
                state = origin_state(depth)
                self.assertEqual(state["mass"], Fraction(1, 2**depth))
                self.assertEqual(state["volume"], Fraction(1, 8**depth))
                self.assertEqual(state["density"], 4**depth)
                self.assertEqual(state["capacity_residual"], 1)

    def test_parent_child_conservation(self):
        for depth in range(24):
            parent=origin_state(depth)
            origin_child=origin_state(depth+1)
            other=parent["mass"] / 14
            self.assertTrue(conserves(parent["mass"], (origin_child["mass"],)*(1)+(other,)*7))
            self.assertEqual(origin_child["density"], 4*parent["density"])

    def test_negative_conservation_control(self):
        self.assertFalse(conserves(Fraction(1), (Fraction(1,2), Fraction(1,8))))
        self.assertFalse(conserves(Fraction(1), (Fraction(1,2),)*8))

    def test_invalid_depth(self):
        for depth in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                origin_state(depth)


if __name__ == "__main__":
    unittest.main()
