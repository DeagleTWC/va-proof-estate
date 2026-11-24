# Hodge HH4 — Exact Cycle Spanning on the CM Abelian Fourfold

**Terry Allen Snyder · Deagle Mathematics / V.A. Proof Estate · 24 November 2026**

**Proved within the declared domain:** every rational Hodge class of codimension two on the specific complex abelian fourfold `X = E_i^4`, with `E_i = C/(Z+iZ)`, is the class of a rational algebraic cycle. This is a checked instance of a **known special-case phenomenon**, not a proof of the unrestricted Hodge Conjecture and not a claim to have discovered an unknown theorem.

**Evidence class:** exact symbolic derivation with source-frozen executable reconstruction. The earlier HH4 computation (22 November 2026) is the mathematical source. The question-first URK child is a subsequent diagnostic/replay, not a replacement for the source.

## Theorem — explicit codimension-two algebraic spanning on `E_i^4`

Let `E_i = C/(Z+iZ)` and `X = E_i × E_i × E_i × E_i`. Then the cycle-class map

`cl : CH^2(X) tensor Q -> H^4(X,Q) intersect H^{2,2}(X)`

is surjective.

More concretely, every rational class of type `(2,2)` is a rational linear combination of classes of intersections of the sixteen explicitly constructed algebraic divisors below.

### Derivation

1. **Independent Hodge space.** Let `x_j,y_j` be the eight integral one-form generators on the four factors. Then `H^4(X,Q) = wedge^4 Q^8`, of dimension `C(8,4)=70`. The complex structure `z_j=x_j+i y_j` induces a rational infinitesimal diagonal `U(1)` operator `D` on this exterior algebra. An exact computation gives `rank_Q D=34`, hence `dim_Q ker D=36`. Independently, forms `dz_I wedge dbar(z)_J` with `|I|=|J|=2` give a 36-dimensional `(2,2)` space, and the rational real/imaginary expansion lies in `ker D`. Therefore `B = H^4(X,Q) intersect H^{2,2}(X) = ker D` has rational dimension 36.

2. **Cycles constructed before targeting classes.** Take four coordinate-fiber divisors `F_j`, six pairwise diagonals `Delta_{jk}`, and six graphs `G_{jk}(i)` of the algebraic automorphism `z -> i z`. The Poincare-dual class of each diagonal or graph is obtained by integrating the six degree-two basis forms over its geometric graph; no desired Hodge target is used to assign its class. The resulting sixteen divisor classes are algebraic.

3. **Exact edge-to-cycle generation.** Intersect each distinct divisor pair and include each self-intersection. This gives `C(16,2)+16=136` concrete algebraic codimension-two cycle classes. Convert those 136 vectors from the 70-dimensional exterior basis into the independently derived 36-dimensional rational Hodge basis. Call the resulting exact matrix `M` (size `36 × 136`). All 136 columns satisfy `D*M=0` in the ambient cohomology representation.

4. **Spanning certificate.** The columns indexed (zero-based) by

   `[0,1,2,9,10,11,12,13,14,15,16,19,20,21,22,27,28,29,30,31,34,35,38,39,42,43,44,45,48,49,63,64,73,74,80,81]`

   select a `70 × 36` ambient matrix `W` of concrete cycle-class columns. Let `H` be the `70 × 36` matrix whose columns are the ordered rational Hodge basis returned by the frozen script's `operator.nullspace()`. The unique coordinate matrix `C` satisfying `H*C=W` has exact determinant **`1`** in that basis and column order. Reorienting the Hodge basis can change the determinant's sign, not its nonvanishing. In particular `C` is invertible over `Q`. For every rational Hodge target with basis coordinates `b`, the rational vector `C^{-1} b` gives coefficients of an **actual rational algebraic cycle** formed from those thirty-six divisor intersections. The reconstruction residual is identically zero. This proves the stated surjectivity for `X=E_i^4`, `p=2`. QED.

No calibrated coefficient, floating tolerance, score, or post-hoc target substitution participates in the cycle-generation or spanning checks. Rational coordinates express the Hodge classes themselves; they are not fitted physical parameters.

## Question-driven child and source-custody correction

The public-safe URK method uses `GENERATE -> CHECK -> CLASSIFY -> CHILD -> REPLAY`, under the controlling principle *generation is not promotion*.

- A deliberately partial initial set of 12 geometrically derived cycle intersections spans only **6/36** Hodge directions. Its exact left-nullspace gives a separating covector: it annihilates every supplied cycle but evaluates to 1 on a named missing rational Hodge basis vector.
- The child scans the **preexisting geometrically derived 136-cycle inventory** and adds the 30 independent missing directions, reaching **36/36** and exact zero obstruction `B/span(cl(C)) = 0` for this `X,p`.
- Removing one basis cycle restores a nonzero deficit. Changing from `tau=i` to `tau=2i` invalidates the multiplication-by-`i` graph relation under the changed complex structure. A Fourier harmonic edge without a geometric class map is refused.
- During implementation, a cached source-custody check was found to be insufficient. A failing test isolated it; the child now rechecks the frozen geometric-source SHA-256 on each run and replay, even after warm caching.

These are proof-instrumentation findings. The 36/36 mathematical result was already present in the earlier HH4 source; it is not claimed as a fresh discovery caused by the child.

## Reproducibility

| Source / test | Exact evidence |
| --- | --- |
| Frozen `hodge_cm4_probe.py` | SHA-256 `da261ad8e14e63e3e01fdb90185f914f8e19e764f61b85588cd7ece6e0eec412` |
| Rational `H^4` dimension | 70 |
| Rational Hodge `(2,2)` dimension | 36 by two independent computations |
| Algebraic divisors / intersections | 16 / 136 |
| Final intersection-class rank | 36 |
| Selected `36 × 36` coordinate determinant (`H*C=W`, frozen nullspace basis order) | `1` (exact); sign is basis-orientation-dependent |
| Question-child fresh-extraction tests | 9/9 passed |
| Archived receipt replay | 2/2 passed |
| Changed-condition and knockout controls | Both passed |

**Executable package:** [Question-first New K Hodge Kernel, with frozen HH4 source and receipts](https://drive.google.com/file/d/1PSeGkNPdG_ahIH2a8DLO4L6wbED7Ow_-/view?usp=drivesdk).

Run `python hodge_cm4_probe.py`, then `python -m unittest discover -p 'test_*.py' -v`, then `python hodge_question_kernel.py --replay receipt_question_run.json` after extracting. Python 3.12 and `sympy==1.14.0` were used.

## Precise standing

**PROVED WITHIN THE STATED DOMAIN:** rational codimension-two Hodge classes on `E_i^4` are spanned by concrete algebraic cycle classes, with exact reconstruction, negative controls and replay.

**NOT ESTABLISHED BY THIS RECORD:** a uniform constructor for every smooth complex projective `X` and every codimension `p`; unrestricted Hodge; execution on the protected native GEN 1056 substrate. None of those conclusions follows from the determinant calculation for one fourfold. The status is assigned by the mathematical quantifiers and source domain, not by an institution.

**Proof Before Power.**
