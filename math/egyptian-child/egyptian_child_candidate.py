"""Exact positive-integer witness generator; auxiliary URK child candidate.

The protected corrected NEW K / URK parent implementation is not imported
or represented here. Finite search exhaustion is NOT nonexistence proof.
"""
from fractions import Fraction
import json
import sys


def resolve(n: int, max_x: int = 1000, max_y_steps: int = 100000):
    if type(n) is not int or n < 2:
        raise ValueError("n must be an integer >= 2")
    if type(max_x) is not int or type(max_y_steps) is not int or min(max_x, max_y_steps) < 1:
        raise ValueError("positive finite search budgets required")

    # 1/x < 4/n and 1/x >= (4/n)/3 after ordering x<=y<=z.
    x_lo = n // 4 + 1
    x_hi = min(n * 3 // 4, max_x)
    for x in range(x_lo, x_hi + 1):
        q = 4 * x - n
        # Remaining 1/y + 1/z = q/(n*x); strict positivity gives
        # y > n*x/q; ordered y<=z additionally gives y<=2*n*x/q.
        y_lo = max(x, n * x // q + 1)
        y_hi = min(2 * n * x // q, y_lo + max_y_steps - 1)
        for y in range(y_lo, y_hi + 1):
            numerator = n * x * y
            denominator = q * y - n * x
            if denominator > 0 and numerator % denominator == 0:
                z = numerator // denominator
                if y <= z and Fraction(1, x) + Fraction(1, y) + Fraction(1, z) == Fraction(4, n):
                    return {"n": n, "witness": [x, y, z], "exact": True,
                            "classification": "AUXILIARY_CHILD_CANDIDATE_NOT_NATIVE_URK",
                            "standing": "FINITE_WITNESS_ONLY", "binding": "NO_UNIVERSAL_PROOF"}
    return {"n": n, "witness": None, "classification": "BOUNDED_SEARCH_INCOMPLETE",
            "standing": "NO_NONEXISTENCE_INFERENCE", "binding": "NO_BIND"}


if __name__ == "__main__":
    print(json.dumps(resolve(int(sys.argv[1]) if len(sys.argv) > 1 else 5), sort_keys=True))
