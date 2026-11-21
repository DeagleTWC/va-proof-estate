"""Public-safe exact abstract basin countermodel, adapted from source Prop. 16.2.

This checks a conservative hierarchy with diverging local density. It is NOT
a Navier–Stokes velocity solution, a native URK kernel, or a blow-up example.
No private operator or native source implementation is included.
"""

from fractions import Fraction


def origin_state(depth: int) -> dict:
    """Give exact carried mass, basin volume, density, and standing residual."""
    if type(depth) is not int or depth < 0:
        raise ValueError("depth must be a nonnegative integer")
    mass = Fraction(1, 2**depth)
    volume = Fraction(1, 8**depth)
    density = mass / volume
    capacity = mass + 1
    return {
        "mass": mass,
        "volume": volume,
        "density": density,
        "capacity_residual": capacity - mass,
    }


def conserves(parent: Fraction, children: tuple[Fraction, ...]) -> bool:
    """Check exact, nonnegative parent-to-child content conservation."""
    return (
        isinstance(parent, Fraction)
        and parent >= 0
        and len(children) == 8
        and all(isinstance(c, Fraction) and c >= 0 for c in children)
        and sum(children, Fraction(0)) == parent
    )


if __name__ == "__main__":
    for n in range(0, 9):
        s = origin_state(n)
        print(f"depth={n} mass={s['mass']} volume={s['volume']} "
              f"density={s['density']} residual={s['capacity_residual']}")
    print("Classification: EXACT_ABSTRACT_BASIN_ONLY / NO_NS_PROOF / NO_NATIVE_BIND")
