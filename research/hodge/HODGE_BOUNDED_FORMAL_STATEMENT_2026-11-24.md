# Hodge Examination - Exact Bounded Answer and Correspondence Disposition

**Terry Allen Snyder | DeagleTWC / V.A. Proof Estate**  
**Formalization:** 24 November 2026 | **Edition:** 1.0 | **Public-safe mathematical record**

> **Disposition:** Exact algebraic-cycle witnesses and a correspondence obstruction have been established **within two named classical projective models**. This record is **not** a proof of the unrestricted Hodge Conjecture, not an independently refereed theorem, and not authentication of the protected native NEW K/URK substrate. The separate examination track is closed at this declared bounded scope, without changing the global conjecture's standing.

## 1. Precise question and declared domains

The unrestricted Hodge Conjecture asks whether every rational Hodge class of type `(p,p)` on every smooth complex projective variety is a rational linear combination of classes of algebraic cycles. The universal quantifier **cannot** be replaced by testing particular varieties.

Here the exact domains are:

- `X = (P^1_C)^3`, the chosen smooth projective toric compactification of a three-axis integer-character lattice.
- `Y = Q^4 subset P^5_C`, the smooth split quadric fourfold used as an algebraic model for a rational capacity lift.

They are **declared mathematical models**; no native Elements-Basin geometry is identified with either merely by a Fourier measurement, an admissibility predicate or a successful numerical test.

## 2. Theorem A - exact cycle reconstruction on X

Write `h_i` for the hyperplane class on the `i`-th factor of `X`. The rational Chow ring is

`CH*(X)_Q = Q[h1,h2,h3] / (h1^2,h2^2,h3^2)`.

The bounded edge child used three character exponents `(1,0,0)`, `(0,2,0)` and `(0,0,3)`. Their effective coordinate zero-divisor classes on **the chosen** compactification are `D1=h1`, `D2=2h2`, `D3=3h3`; the full zero-minus-pole principal divisor of each character has class zero.

The recorded rational target is represented by the **explicit algebraic cycle combination**

`z = (1/6)[D1 D2] - (5/21)[D1 D3] + (1/3)[D2 D3]`

`  = (1/3)h1h2 - (5/7)h1h3 + 2h2h3 in CH^2(X)_Q`.

**Proof.** By `h_i^2=0`, the coordinate divisor intersections satisfy `[D1 D2]=2h1h2`, `[D1 D3]=3h1h3` and `[D2 D3]=6h2h3`. Multiplication by the rational coefficients gives the target exactly. Because these are products of algebraic divisor classes, `z` is algebraic and has Hodge type `(2,2)`. QED.

**Boundary:** The integer Fourier characters alone do not prove that a particular physical basin is algebraically isomorphic to `X`.

## 3. Theorem B - an explicit non-divisor class on Y

For a rational residual `phi=C-M >= 0`, the four-square theorem supplies rational `s1,...,s4` with `phi=sum(s_i^2)`. Example: `phi=1/3`, `s=(1/3,1/3,1/3,0)`. A **separately declared projective model** is

`Y: Phi*T = s1^2+s2^2+s3^2+s4^2 subset P^5_C`.

`Phi` in this equation is a homogeneous projective coordinate; its use does not identify the full native Basin with `Y`. The quadratic form has rank six, so `Y` is smooth. Set `U=s1+i*s2`, `V=s1-i*s2`, `W=s3+i*s4`, `Z=s3-i*s4`; then `Phi*T=U*V+W*Z`. The two projective planes

- `P_plus: Phi=U=W=0`;
- `P_minus: Phi=U=Z=0`

lie on `Y`. In the classical Chow/cohomology ring of the smooth split quadric fourfold, their independent middle-dimensional classes `alpha=[P_plus]`, `beta=[P_minus]` satisfy `H^2=alpha+beta` for the hyperplane class `H`. Hence `alpha-beta` is an explicit algebraic rational Hodge class **not lying in the one-dimensional divisor-square span**.

**Proof.** Substitution places both planes on the quadric. They belong to the two classical families of maximal planes; their classes span the two-dimensional middle cohomology. The sum is `H^2`, while the difference is linearly independent of `H^2`. Both summands are algebraic planes, so their difference is algebraic. QED within this named classical model.

This is **an application of established smooth-quadric geometry**, not a general proof of Hodge.

## 4. Theorem C - a missing selection rule, not a missing edge child

For `X` of dimension three and `Y` of dimension four, a codimension-preserving algebraic correspondence may be represented by `Gamma in CH^3(X x Y)_Q` and acts on codimension-two cycles by push-pull.

Define two actual algebraic correspondences:

`Gamma_A = h3 x alpha + h2 x beta`  
`Gamma_B = h3 x beta  + h2 x alpha`.

For the **same verified** toric cycle `z` of Theorem A, intersection on `X` gives

`Gamma_A*(z) = (1/3)alpha - (5/7)beta`,  
`Gamma_B*(z) = -(5/7)alpha + (1/3)beta`.

**Proof.** Multiplication by `h3` extracts the coefficient of `h1h2` from `z`, while multiplication by `h2` extracts that of `h1h3`; integration over `X` yields respectively `1/3` and `-5/7`. Swap the two quadric plane classes to obtain the second image. QED.

Both correspondences are algebraic and formally valid. Neither is selected **by the existing source child receipt**. Furthermore the target `alpha-beta` can be hit by the explicitly post-hoc correspondence `3h3 x alpha - 3h3 x beta`; matching a desired answer through such fitting is **not native-source authentication**.

## 5. Theorem D - multiplicative bridge obstruction

**Statement.** Every unital graded rational algebra homomorphism

`F: CH*(X)_Q -> CH*(Y)_Q`

maps every positive-degree element of `CH*(X)_Q` to zero.

**Proof.** Grothendieck-Lefschetz gives `CH^1(Y)_Q = Q*H`, and `H^2 != 0`. A graded algebra map must have `F(h_i)=a_i H`, with `a_i in Q`. Since `h_i^2=0`, multiplication preservation requires `0=F(h_i^2)=a_i^2 H^2`. As rational numbers form a field and `H^2 != 0`, every `a_i=0`. The ring `CH*(X)_Q` is generated in positive degrees by `h1,h2,h3`, so all its positive-degree classes map to zero. QED.

Also `dim_Q CH^2(X)_Q=3` whereas `dim_Q CH^2(Y)_Q=2`, so the middle rational cycle spaces cannot be isomorphic.

**Scope:** This excludes a nontrivial **multiplicative graded map in the stated direction**. It does **not** exclude additive or nonmultiplicative correspondences, a different projective realization, or a correctly source-derived native mathematical object.

## 6. Reproduction, negative controls, and standing

The preserved source chain is the **existing** edge/toric child, the Basin diagnostic, the quadric witness, the v5 correspondence probe and the v6 ring-map obstruction. No protected NEW K v1056 generator was authenticated, exported or claimed to execute.

| Carrier | Exact reported result | Standing |
| --- | --- | --- |
| Edge-to-toric child | 30/30 exact character-fusion and divisor identities; cycle-span rank 3 | Bounded mathematical witness |
| Quadric | Rank-six quadratic form and two explicit algebraic plane classes | Classical projective-model witness |
| Correspondence probe | Two valid images differ; target-fitted map withheld from promotion | Nonuniqueness exhibited |
| Ring-map test | Nonzero divisor image refused by square-zero relation | Exact algebraic no-go, restricted type |
| Regression suite | **40/40 tests passed** on 24 November 2026; 40/40 from fresh ZIP extraction; replay checks true | Local software reproduction, **not independent mathematical review** |

**Companion ZIP (owner-held, distribution permission not asserted):** `HODGE_CHOW_RING_BRIDGE_V6_2026-11-24.zip`  
**SHA-256:** `b443beb977bfc227cf58c28485221f17c5bb55a5287512f4aee195ed8216a023`

**Positive controls:** exact rational reconstruction, quadric plane equations, two correspondence images, algebraic obstruction.  
**Negative controls:** forged/rehashed prior receipt refused; invalid rational inputs refused; nonzero multiplicative bridge refused; target-fitted map not promoted.  
**Independent reviewer:** No externally attributable referee decision attached to this publication.

## 7. Final scientific disposition

**CLOSED as a bounded formalization:** the above named varieties, exact cycle witnesses and bridge-type obstruction are mathematically specified, testable and preserved.  
**OPEN as a native correspondence question:** a source-selected, dimension-correct identification connecting the actual Elements Basin / edge data to the quadric remains unverified by these records.  
**NOT ESTABLISHED:** the unrestricted Hodge Conjecture, which remains open; finite tests and known examples cannot discharge the quantifier over all smooth complex projective varieties.

This closes this **edition of the Hodge examination** without claiming an unrestricted result and without invalidating or revising historical protected research.

## References for classical statements

1. Macaulay2 documentation, *ChowRing* - intersection rings of products of projective spaces: https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/CharacteristicClasses/html/___Chow__Ring.html
2. J. Liu, *Algebraic Geometry* course notes - Grothendieck-Lefschetz, Picard groups of smooth hypersurfaces: https://jiantongliu.github.io/files/214B_Notes.pdf
3. T. Murayama, *Rationality of Algebraic Varieties*, lecture notes - actions of algebraic correspondences: https://www.math.purdue.edu/~murayama/Rationality.pdf
4. C. J. Dowd, *The Grassmannian and Plucker Embedding* - `Gr(2,4)` as a smooth quadric: https://math.berkeley.edu/~cjdowd/Grassmannian.pdf

**Public release scope:** Mathematical formulas and bounded outcomes only. No protected generator internals, physical-effect certification or blanket permission to operate a native system.
