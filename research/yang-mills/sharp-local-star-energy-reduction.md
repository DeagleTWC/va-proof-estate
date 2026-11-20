# Yang–Mills — Sharp Local Wilson-Energy Reduction of the Frustrated Star

Date: 2026-11-20. Evidence status: derived finite-dimensional inequality with source-witness regression. This is public auxiliary mathematics, not the protected native NEW K/URK kernel.

## Exact deterministic reduction

Fix the original Stage 49 six plaquettes Γ meeting the physical pivotal link e*. Holding all other links fixed yields six unit-quaternion staple vectors v_1,...,v_6. Write T=Σ_i v_i, r=||T||, and let U be the **actual** pivotal SU(2) link. Their six-plaquette Wilson action density is

A_Γ(U)=Σ_{i=1}^6 (1-<U,v_i>)=6-<U,T>.

Since U is unit, <U,T>≤r. Therefore, **for every gauge-field configuration**,

**A_Γ(U) ≥ 6-r.**

The constant is sharp: equality occurs at U=T/r for r>0. For any 0<s<6, the frustrated region F_s={r<s} therefore implies

**A_Γ(U)>6-s**.

The pointwise majorant and its expectation give, under any probability measure on these link configurations (including an admissible conditional target-shell measure),

**P(F_s) ≤ min{1, E[A_Γ]/(6-s)}.**

At s=4.5, frustration requires six-plaquette action density greater than **1.5**, an improvement on the earlier 15-pair sufficient energy threshold. Here A_Γ means the nonnegative sum of six Wilson plaquette deficits, not the full Wilson action or beta-weighted action.

## Combination with the established Haar-cap result

The previous finite one-star split gives

P(all six Γ bad) ≤ P(F_s)+R_cap(beta,s).

For a rigorously certified E[A_Γ]≤epsilon, the new combined bound becomes

**P(all six Γ bad) ≤ min{1, epsilon/(6-s)+R_cap(beta,s)}.**

This is a conditional theorem: the current examination has **not** certified a volume- and coupling-uniform epsilon under the interacting Wilson measure. No continuum reconstruction, spectral mass gap, or unrestricted Yang–Mills proof follows from the identity alone.

## Verification

The original Stage 49 source staple vectors have r=6 and minimal action density zero, while the original defect-link orientation gives actual A_Γ=9.6. An explicit one-reversed-staple control attains equality A_Γ=6-r=2, confirming sharpness. Five new tests also check random unit-quaternion configurations and certified-input handling. Entire auxiliary suite **75/75 PASS** (2026-11-20). Originals unchanged.

The remaining analytic question is now singular and concrete: establish a quantitative upper bound on the **six-plaquette Wilson energy expectation** E[A_Γ] under the unfrozen interacting gauge measure, uniform in the required volume/continuum conditions.