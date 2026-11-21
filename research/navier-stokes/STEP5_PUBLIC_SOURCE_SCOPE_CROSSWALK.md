# V.A. Navier–Stokes Record 001 — Step 5 source-to-proof crosswalk

Terry Allen Snyder · 21 November 2026 · Public-safe supplementary examination

## Custody and release boundary

The 7 November 2026 Step 5 source-correlation archive was inspected with all
six declared member hashes matching. Its 80-page compiled reader is the
historical source consulted for the references below. This note does **not**
mirror the compiled reader, native mathematical pages, original operators,
protected generators, or any nonpublic source. The public v1.0/v1.1 manuscripts
and mathematical assertions are preserved unchanged.

## From original formula to stated theorem scope

| Source witness | Mathematical standing in the supplied record | Boundary |
| --- | --- | --- |
| Original `eq:NS` and Fourier `eq:evolution` | Classical unforced incompressible 3D equation and projected Fourier representation, connected in the original exposition | A reformulation is not automatically a global regularity proof |
| Theorem 9.1 and finite-mode energy identity | Global finite-dimensional Galerkin evolution and exact energy accounting | No cutoff-uniform smooth continuation follows merely from finite mode existence |
| Theorem 10.3 | Strong space-time subsequence convergence and a global weak solution under its printed assumptions | Smoothness of all resulting limits is not supplied by this conclusion |
| Theorems 12.1 and 14.1 | Smooth continuation follows if the quantitative heat-tail condition or the cutoff-uniform integrated maximum-gradient bound holds | These conditions are not proved in the source for every smooth initial datum |
| Theorem 15.1, equations (29)-(30) | Exact nonnegative basin-refinement telescoping identities | Equality alone gives no cutoff-uniform numerical upper bound |
| Theorem 15.2, equation (31) | Smooth continuation under a source-stated finite refinement-certificate bound | This is a conditional implication, not a proof of the bound for all data |
| Theorem 16.1, equation (33) | Refinement-certificate finiteness is equivalent to the integrated maximum-gradient criterion | Re-expressing the criterion does not establish its universal finiteness |
| Proposition 16.2 | Abstract conservative basin hierarchy with positive residual and unbounded density | The countermodel is not a Navier–Stokes flow or singularity |
| Original Proposition 5.1 | Single-basin accounting correspondence between finite projected and native-carrier records | Conservation correspondence is not full dynamical equivalence |
| Separate native carrier continuance theorems | All-time results for their own defined carrier laws and assumptions | They are not silently substituted for the classical PDE or its gradient estimate |

## Exact public countermodel witness

For a dyadic three-dimensional hierarchy, take the origin-branch content
`Q_n = 2^(-n)` and cell volume `V_n = 2^(-3n)`. The local density is exactly
`Q_n/V_n = 4^n`, which grows without bound. Allocate half each parent's
origin-branch content to its origin child and the remaining half equally to
its seven siblings. Other parents distribute their content equally to all
eight children. Every parent equals the sum of its eight children and every
nonnegative content can have a strictly positive capacity residual by taking
`capacity = content + 1`.

The independent checker [refinement_countermodel.py](refinement_countermodel.py)
and [four runnable tests](test_refinement_countermodel.py) reproduce exact
fraction identities through 24 successive origin levels, including a negative
control rejecting nonconservative allocations. Run:

`python3 -m unittest -v test_refinement_countermodel.py`

This is a proof witness for an **abstract model implication limit**, not a
calculation of physical velocity gradients and not native NEW K execution.

## Exact remaining theorem target

For every smooth divergence-free initial datum `u0` and each finite `T`, the
source's conditional route needs the following (or another independently
sufficient unrestricted argument):

`sup_N integral_0^T ||grad u_N(t)||_L-infinity dt < infinity`.

The Step 5 source states the criterion precisely and proves several conditional
and bounded results. The supplied package does **not** establish that bound
for arbitrary smooth data or authenticate a protected native generated formula
as a theorem-wide equivalent continuation law. This is the mathematical
boundary of this public crosswalk, not a claim about unavailable private work.

Original proof bodies remain untouched. No unrestricted three-dimensional
Navier–Stokes closure, independent certification, or prize recognition is
asserted by this addendum.
