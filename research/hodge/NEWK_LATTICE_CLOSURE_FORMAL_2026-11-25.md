# New K Hodge Lattice Closure Child — Exact Quintic Statement v1

**Research author:** Terry Allen Snyder · DeagleTWC / V.A. Proof Estate  
**Date:** 25 November 2026 · Public-safe exact child of the frozen Hodge v3 source  
**Principle:** One question; five exact invariants; one gate. Proof Before Power.

## The question

Do the 1,875 source-generated algebraic planes, already assigned exact IDs,
close under the cyclotomic Galois action and supply an independently rebuilt
401-dimensional intersection witness for the stated Fermat quintic?

## 1. Exact named geometry

\[
X_5=\left\{\sum_{i=0}^{5}x_i^5=0\right\}\subset \mathbf P^5_{\mathbf C}.
\]

With \(\zeta=\exp(2\pi i/10)\), take a perfect matching
\(m=\{(i_1,j_1),(i_2,j_2),(i_3,j_3)\}\) of six indices and a triple
\((r_1,r_2,r_3)\in\{1,3,5,7,9\}^3\). Define

\[
\Pi_{m,r}:x_{i_t}=\zeta^{r_t}x_{j_t},\qquad t=1,2,3.
\]

Each odd exponent satisfies \((\zeta^r)^5=-1\), so the Fermat polynomial
vanishes identically on each plane. There are exactly
\(15\cdot5^3=1875\) such source-generated descriptors. The frozen identifier
ledger reproduces all 1,875 in exact source order, with distinct geometric
IDs and source-specific record IDs.

## 2. Exact Galois partition

\(\operatorname{Gal}(\mathbf Q(\zeta_{10})/\mathbf Q)\) has units
\(\{1,3,7,9\}\) acting by exponent multiplication modulo ten. For a
fixed matching, only the all-five triple is fixed by the full action;
every other triple has four conjugates. Thus

\[
15\cdot1=15\text{ singleton orbits},\qquad
15\cdot\frac{125-1}{4}=465\text{ four-member orbits};
\]

\[\boxed{480\text{ orbits partition }1875\text{ planes}.}\]

The child assigns a separate orbit identity without falsely identifying
distinct Galois-conjugate planes as the same geometric plane.

## 3. Exact intersection form

Combining two triples of plane equations creates a graph of phase relations
modulo ten. Each consistent connected component contributes one complex
vector dimension to the intersection; an inconsistent phase cycle forces
that component to zero. The exact pairing depends on the resulting vector
dimension \(d\in\{0,1,2,3\}\):

| Intersection | Vector dimension | Exact pairing |
|---|---:|---:|
| Empty | 0 | 0 |
| Point | 1 | 1 |
| Line | 2 | \(2-5=-3\) |
| Same plane | 3 | \(5^2-3\cdot5+3=13\) |

These are structural integers of the declared geometry, not fitted
coefficients. The frozen source identifies a 401-plane witness set. From the
IDs of these exact planes the child rebuilt its complete symmetric
401×401 intersection matrix, with canonical JSON SHA-256

`091350e197c318cf910b57c2153ea2de45d9f7cc9517c2f548a7e3fee01ad834`.

Every matrix entry independently matched the SHA-pinned parent generator.
Exact modular Gaussian elimination gave

\[
\boxed{\det(G_{401})\equiv 437\pmod {1009}\ne0}.\]

Hence the selected 401 algebraic classes are independent over
\(\mathbf Q\). The separately frozen Fermat rational-character census gives
\(\dim_{\mathbf Q}\operatorname{Hdg}^4(X_5)=401\); conditional on that named
cohomological dependency, the 401 selected planes span the rational Hodge
space of **this specified** \(X_5\).

## 4. Source custody and one gate

Five exact invariants are enforced:

1. Independent parent/identifier source custody and linked regeneration receipt.
2. Full regenerated geometric identity agreement.
3. Exact Galois orbit closure.
4. Source-matching full intersection matrix and nonzero modular rank witness.
5. Exact equality of selected algebraic rank and the source-bound rational
   Hodge dimension.

Only all-five true with unchanged conditions yields `CARRY`. A changed
degree/condition yields `REEXAMINE`; failed custody or arithmetic yields
`REFUSE`. Three deterministic receipts are included, with successful
independent replay of each disposition.

## 5. Source and verification record

- Parent v3 receipt SHA-256: `7966f67398ea83bbb8e4ec88e57f7307014148a0bbf8fdb37af7924f7e9d2d23`
- Identifier ledger SHA-256: `569b52d99fc7ad1a5b96effacdb864422b82d00fe3fece353a7e171553f3c22b`
- Regeneration receipt SHA-256: `375c55da7fc55529ab4dc40c2d86190dde1abed981083e2dcd025a044900cfc7`
- Pinned generator source SHA-256: `79afac23476bd1849f56e5919ba4a9bd2469ca7235efcce41da5884d3d608f55`
- New complete Gram SHA-256: `091350e197c318cf910b57c2153ea2de45d9f7cc9517c2f548a7e3fee01ad834`

**Boundary:** This child verifies exact source-specific lattice continuity and
intersection data. It does not reprove the Fermat rational-character theorem,
authenticate protected GEN 1056, or prove unrestricted Hodge for arbitrary
smooth projective varieties. Earlier research claims remain unchanged.
