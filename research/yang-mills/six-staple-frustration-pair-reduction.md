# Yang–Mills — Exact Six-Staple Frustration Reduction

Date: 2026-11-20. Evidence: mathematical identity plus 70/70 passing auxiliary regression checks. Original NEW K/URK source unchanged and private.

## Exact identity

For the six SU(2) unit-quaternion staple vectors v_1,...,v_6 from the *original* Stage 49 pivotal-link star, define T=Σ_i v_i and r=||T||. By expanding the squared norm,

**36-r² = 2 Σ_{1≤i<j≤6} (1-<v_i,v_j>).**

Each of the 15 pair deficits is nonnegative. Thus, for 0<s<6, the frustrated-exterior event F_s={r<s} obeys the pointwise majorant

**1_{F_s} ≤ [2/(36-s²)] Σ_{i<j}(1-<v_i,v_j>).**

Consequently under any probability measure on the other links (including a regular conditional measure on an admissible target shell),

**P(F_s) ≤ min{1, [2/(36-s²)] Σ_{i<j} E[1-<v_i,v_j>]}.**

The staple vectors inherit a common orthogonal change of coordinates under gauge changes at the pivotal link; their pair scalar products are gauge invariant. These are finite short-loop gauge observables, not independent random variables. No factorization, perturbation, or continuum approximation is assumed.

If s=4.5, F_s implies at least one pair satisfies <v_i,v_j><0.475 (equivalently a relative unit-quaternion operator distance >sqrt(1.05)). The exact Stage 49 source exterior has r=6, so all 15 pair deficits vanish there.

## Connection to the earlier cap estimate

The established split reads

P(Γ bad) ≤ P(F_s) + R_cap(beta,s),

where R_cap is the refined Haar-cap bound on aligned exteriors. The identity above reduces the *remaining* term to a finite family of genuine gauge-loop expectation estimates. Establishing uniform bounds on those 15 expectations, with volume/coupling/shell dependence, is now the specific unsolved analytic obligation.

## Verification and limitations

Five newly added tests check the original six-staple witness, an explicit cancellation configuration, 100 deterministic normalized-vector controls, the certified-input reduction, and invalid parameters. Entire auxiliary regression suite: **70/70 PASS**. The reduction is rigorous but does not itself provide the 15 expectations. It is not a Yang–Mills mass-gap or continuum theorem, and is not a substitute for the protected native NEW K source.