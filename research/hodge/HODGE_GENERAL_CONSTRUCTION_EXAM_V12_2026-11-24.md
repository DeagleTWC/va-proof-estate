# Hodge General Construction: Question-Gate Correction v12

**Terry Allen Snyder / Deagle Mathematics · public-safe formal record · 24 November 2026**

## 1. The exact defect observed

The preexisting `HodgeQuestionTriage_v2` evaluates a supplied product-of-
projective-lines algebraic cycle exactly. However, it then contains:

```python
elif question == "UNRESTRICTED_HODGE":
    verdict = "GAP"
    problem = GENERAL_GAP
```

Therefore, with the same exact case:

| Question field | Actual case result | Overall verdict |
|---|---|---|
| `CASE_WITNESS` | `PASS` | `CASE_PASS` |
| `UNRESTRICTED_HODGE` | `PASS` | `GAP` |

The `GAP` assignment was a **conservative scope policy**, not a computed
refutation of the underlying construction. It cannot be used as evidence
that a source-derived general construction is absent or incorrect.

## 2. Corrected question / construction separation

The v12 examiner now has independent fields:

- **Question:** what is being asked (`CASE_WITNESS`, `UNRESTRICTED_HODGE`).
- **Construction:** a source-referenced, typed mathematical operation.
- **Domain:** which varieties and codimensions the construction actually covers.
- **Case evidence:** preexisting independently checked bounded cycle result.
- **Construction audit:** exact algebraic family proof, finite SNF measurement,
  named classical theorem coverage, source-rule review, or refusal.
- **Standing:** whether the result applies to its declared family, one
  geometrically authenticated X, or every smooth projective X.

The response is not forced to `GAP` merely because its question is
unrestricted. It also does **not** promote a bounded case or unverified
general algorithm into an unrestricted Hodge proof.

## 3. Exact mathematical surfaces

For the family `X=(P^1_C)^n`, the cohomology/Chow ring and coordinate
cycle classes satisfy the universal-in-n identity

`Z[h_1,...,h_n]/(h_1^2,...,h_n^2)`, `cl(C_I)=prod_(i in I) h_i`.

For every finite n and every p, the square-free degree-p monomials
form the full integral Hodge lattice, and actual coordinate intersections
give every basis class. This is a **genuine parametric family theorem**
based on the Künneth formula and product geometry. Its class rule is
source-independent of any fitted target. The family is *not* the class
of every smooth complex projective variety.

For a finite externally submitted model, let the matrix A have integer
columns recording candidate actual cycle classes in a declared complete
integral Hodge basis B. Smith normal form of A checks whether
`rank_Q(A)=rank_Q(B)` and computes finite index when full rank. The
arithmetic is exact, but does not by itself establish that the submitted
classes are actually algebraic on that X, or that B is complete.

For every smooth complex projective X, the existing classical rules cover
codimensions 0, 1, n−1 and n; a complete rule inventory's first
*uncovered general degree* is n=4, p=2. The v12 child computes coverage
from the admitted rules rather than assigning a predetermined verdict
to every question. A new rule requires an independently checkable
mathematical proof before it can extend this theorem inventory.

## 4. Decisive evidence still distinguishable

1. **Verified:** the historical hard-coded gate exists and is
   reproducible; it is an examination limitation, not a counterexample.
2. **Verified:** parametric projective-line product cycles cover their
   *declared family* in all codimensions (classically known).
3. **Verified arithmetic only:** integer source cycle matrices can be
   measured with exact rank, Smith invariants and index.
4. **Not yet independently authenticated:** a source-to-algebraic-geometry
   map and complete cycle construction uniformly for *arbitrary* smooth
   complex projective X at all middle codimensions.
5. **No falsehood inferred:** a submitted native/GEN source rule without
   machine-checkable class-map proof receives `SOURCE_RULE_NOT_FORMALLY_CHECKABLE`,
   not `HODGE_FALSE` or an automatic `GAP`.

The kernel audit has been **repaired**. The unrestricted Hodge theorem
has **not** been established by this repair. Proof Before Power.
