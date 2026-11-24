"""Public-safe, exact Fourier movement candidate generator for 3D Navier--Stokes.

This is a NEW bounded mathematical specialization of the disclosed URK
generate/check/classify principle, not the protected native URK generator.
It does not prove global smoothness or finite-time blowup.

For a finite symmetric Fourier set, incompressibility constrains each
velocity coefficient to k-perpendicular movement.  The generator projects
every ordered triad into that admissible plane and verifies the resulting
unforced Galerkin energy law with exact rational arithmetic.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from typing import Mapping


K = tuple[int, int, int]


@dataclass(frozen=True)
class Q:
    """A complex rational; no floating-point arithmetic is admitted."""

    re: Fraction = Fraction(0)
    im: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        for term in (self.re, self.im):
            if isinstance(term, bool) or not isinstance(term, (int, Fraction)):
                raise TypeError("coefficients must be exact rationals")
        object.__setattr__(self, "re", Fraction(self.re))
        object.__setattr__(self, "im", Fraction(self.im))

    def __add__(self, other: Q) -> Q:
        return Q(self.re + other.re, self.im + other.im)

    def __neg__(self) -> Q:
        return Q(-self.re, -self.im)

    def __sub__(self, other: Q) -> Q:
        return self + -other

    def __mul__(self, other: Q | int | Fraction) -> Q:
        if isinstance(other, (int, Fraction)) and not isinstance(other, bool):
            return Q(self.re * other, self.im * other)
        if isinstance(other, Q):
            return Q(self.re * other.re - self.im * other.im,
                     self.re * other.im + self.im * other.re)
        return NotImplemented

    __rmul__ = __mul__

    def conj(self) -> Q:
        return Q(self.re, -self.im)

    def norm2(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def wire(self) -> list[str]:
        return [str(self.re), str(self.im)]


ZERO = Q()
MINUS_I = Q(0, -1)
Vec = tuple[Q, Q, Q]


def dot(a: Vec, b: Vec) -> Q:
    return sum((a[i] * b[i] for i in range(3)), ZERO)


def vadd(a: Vec, b: Vec) -> Vec:
    return tuple(a[i] + b[i] for i in range(3))  # type: ignore[return-value]


def scale(a: Vec, q: Q | Fraction | int) -> Vec:
    return tuple(a[i] * q for i in range(3))  # type: ignore[return-value]


def mode_key(k: K) -> str:
    return ",".join(map(str, k))


def projection(k: K, v: Vec) -> Vec:
    """Exact Leray projection, the admissible k-perpendicular movement."""
    if len(k) != 3 or any(type(x) is not int for x in k) or k == (0, 0, 0):
        raise ValueError("wavevector must be a nonzero integer triple")
    k2 = sum(x * x for x in k)
    kv = sum((v[i] * k[i] for i in range(3)), ZERO)
    return tuple(v[i] - kv * Fraction(k[i], k2) for i in range(3))  # type: ignore[return-value]


def _verify_input(modes: Mapping[K, Vec], viscosity: Fraction,
                  density: Fraction, capacity: Fraction | None) -> None:
    if not isinstance(viscosity, Fraction) or viscosity <= 0:
        raise ValueError("viscosity must be a positive exact Fraction")
    if not isinstance(density, Fraction) or density <= 0:
        raise ValueError("mass density must be a positive exact Fraction")
    if capacity is not None and (not isinstance(capacity, Fraction) or capacity < 0):
        raise ValueError("kinetic capacity must be a nonnegative exact Fraction")
    if not modes:
        raise ValueError("a nonempty symmetric mode set is required")
    for k, u in modes.items():
        if (not isinstance(k, tuple) or len(k) != 3
                or any(type(x) is not int for x in k) or k == (0, 0, 0)):
            raise ValueError("invalid Fourier wavevector")
        if not isinstance(u, tuple) or len(u) != 3 or any(not isinstance(x, Q) for x in u):
            raise ValueError("each Fourier velocity must be a Q triple")
        counterpart = tuple(-x for x in k)
        if counterpart not in modes or modes[counterpart] != tuple(x.conj() for x in u):
            raise ValueError("missing or contradictory real-field conjugate mode")
        if sum((u[i] * k[i] for i in range(3)), ZERO) != ZERO:
            raise ValueError("velocity violates incompressible movement constraint")


def generate(modes: Mapping[K, Vec], *, viscosity: Fraction = Fraction(1),
             mass_density: Fraction = Fraction(1),
             kinetic_capacity: Fraction | None = None,
             requested_claim: str = "FINITE_GALERKIN_IDENTITY") -> dict:
    """Generate all ordered triads, check invariants, and gate claim standing.

    RUN means the displayed finite-Galerkin identity is exact.  Requests
    for continuum/global claims are PAUSE, even when every finite gate
    passes. A changed claim cannot inherit proof from a weaker witness.
    """
    _verify_input(modes, viscosity, mass_density, kinetic_capacity)
    if requested_claim not in ("FINITE_GALERKIN_IDENTITY", "UNRESTRICTED_REGULARITY",
                               "FINITE_TIME_BLOWUP"):
        raise ValueError("unrecognized theorem scope")

    ordered = sorted(modes)
    children = {
        tuple(l[i] + m[i] for i in range(3))
        for l in ordered for m in ordered
        if tuple(l[i] + m[i] for i in range(3)) != (0, 0, 0)
    }
    # Critically, children not occupied in the initial state are generated,
    # not silently deleted by a chosen output cutoff.
    output_modes = sorted(set(ordered) | children)
    nonlinear: dict[K, Vec] = {k: (ZERO, ZERO, ZERO) for k in output_modes}
    pair_count = 0
    nonzero_pairs = 0
    for l in ordered:
        for m in ordered:
            k = tuple(l[i] + m[i] for i in range(3))
            if k == (0, 0, 0):
                continue
            pair_count += 1
            scalar = sum((m[i] * modes[l][i] for i in range(3)), ZERO)
            projected = scale(projection(k, scale(modes[m], scalar)), MINUS_I)
            nonlinear[k] = vadd(nonlinear[k], projected)
            if any(c != ZERO for c in projected):
                nonzero_pairs += 1

    advective_transfer = sum((dot(tuple(x.conj() for x in modes[k]), nonlinear[k]).re
                              for k in ordered), Fraction(0))
    dissipation = viscosity * mass_density * sum(
        (sum(x * x for x in k) * sum(c.norm2() for c in modes[k]) for k in ordered),
        Fraction(0))
    # E = rho/2 sum |U_k|^2. For the projected equation:
    # E' = rho Re sum conj(U_k) dot (N_k - nu |k|^2 U_k).
    energy_derivative = mass_density * advective_transfer - dissipation
    energy_residual = energy_derivative + dissipation
    initial_energy = mass_density * sum(
        (sum(c.norm2() for c in modes[k]) for k in ordered),
        Fraction(0)) / 2
    margin = None if kinetic_capacity is None else kinetic_capacity - initial_energy
    transversality = all(
        sum((k[i] * nonlinear[k][i] for i in range(3)), ZERO) == ZERO
        for k in output_modes)
    gates = {
        "reality_and_incompressibility": True,
        "projected_triad_transversality": transversality,
        "nonlinear_energy_cancellation": advective_transfer == 0,
        "exact_kinetic_dissipation_balance": energy_residual == 0,
        "declared_capacity_if_supplied": None if margin is None else margin >= 0,
    }
    if any(x is False for x in list(gates.values())[:4]):
        raise ArithmeticError("generated candidate failed an exact invariant")
    finite_scope = requested_claim == "FINITE_GALERKIN_IDENTITY"
    capacity_rejected = margin is not None and margin < 0
    result = {
        "schema": "va.ns.public_urk_movement_specialization.v1",
        "scope": requested_claim,
        "standing": "ABORT" if capacity_rejected else ("RUN" if finite_scope else "PAUSE"),
        "native_parent_authenticated": False,
        "unrestricted_proof": False,
        "generator_source": "URK generate/check/classify; public finite-mode specialization",
        "viscosity": str(viscosity),
        "mass_density": str(mass_density),
        "kinetic_capacity": None if kinetic_capacity is None else str(kinetic_capacity),
        "initial_kinetic_energy": str(initial_energy),
        "remaining_capacity": None if margin is None else str(margin),
        "mode_count": len(ordered),
        "generated_output_mode_count": len(output_modes),
        "ordered_pair_count": pair_count,
        "nonzero_projected_pair_count": nonzero_pairs,
        "input_modes": {mode_key(k): [c.wire() for c in modes[k]] for k in ordered},
        "generated_nonlinear_rates": {
            mode_key(k): [c.wire() for c in nonlinear[k]] for k in output_modes
        },
        "advective_energy_transfer": str(advective_transfer),
        "viscous_dissipation": str(dissipation),
        "kinetic_energy_derivative": str(energy_derivative),
        "energy_balance_residual": str(energy_residual),
        "gates": gates,
        "refusal_reason": (
            "Initial kinetic burden exceeds declared capacity." if capacity_rejected else
            None if finite_scope else
            "Finite-mode witnesses do not imply a cutoff-uniform continuum theorem."
        ),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["receipt_sha256"] = sha256(canonical.encode("utf-8")).hexdigest()
    return result


def verify_receipt(receipt: dict) -> bool:
    """Verify the receipt against fresh source-derived regeneration, not its hash alone."""
    try:
        modes = {}
        for key, velocity in receipt["input_modes"].items():
            k = tuple(int(x) for x in key.split(","))
            modes[k] = tuple(Q(Fraction(c[0]), Fraction(c[1])) for c in velocity)
        regenerated = generate(modes, viscosity=Fraction(receipt["viscosity"]),
                               mass_density=Fraction(receipt["mass_density"]),
                               kinetic_capacity=(None if receipt["kinetic_capacity"] is None
                                                 else Fraction(receipt["kinetic_capacity"])),
                               requested_claim=receipt["scope"])
        return regenerated == receipt
    except (ValueError, TypeError, KeyError, ArithmeticError, IndexError):
        return False


def demo_modes() -> dict[K, Vec]:
    """An intentionally empty child receives a nonzero generated rate."""
    seeds = {
        (1, 0, 0): (ZERO, Q(1), ZERO),
        (0, 2, 0): (Q(1), ZERO, ZERO),
        (1, 2, 0): (ZERO, ZERO, ZERO),
    }
    return {**seeds, **{tuple(-x for x in k): v for k, v in seeds.items()}}


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="generate a reproducible six-mode receipt")
    parser.add_argument("--verify", type=Path, help="replay a saved JSON receipt")
    parser.add_argument("--claim", default="FINITE_GALERKIN_IDENTITY",
                        choices=("FINITE_GALERKIN_IDENTITY", "UNRESTRICTED_REGULARITY",
                                 "FINITE_TIME_BLOWUP"))
    parser.add_argument("--capacity", type=Fraction, help="optional exact kinetic-energy capacity")
    args = parser.parse_args()
    if args.verify:
        with args.verify.open(encoding="utf-8") as handle:
            saved = json.load(handle)
        if not verify_receipt(saved):
            parser.error("receipt replay refused: source-derived output differs")
        print("REPLAY VERIFIED", saved["receipt_sha256"])
    elif args.demo:
        print(json.dumps(generate(demo_modes(), kinetic_capacity=args.capacity,
                                  requested_claim=args.claim), indent=2, sort_keys=True))
    else:
        parser.error("choose --demo or --verify PATH")
