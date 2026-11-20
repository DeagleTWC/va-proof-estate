# Yang–Mills: SU(2) Haar-Cap Refinement of the Exact One-Link Bound

Date: 2026-11-20. Evidence class: OBSERVED (public auxiliary derivation and tests). Original NEW K/URK source remains unchanged and undisclosed.

## Theorem at finite-volume conditional scope

Fix every link except the single physical link shared by the six original Stage 49 bad plaquettes Γ, and retain the target's exact scalar shell c=3/5. If T is the sum of the six source-extracted SU(2) staples, let r=||T||≤6. For normalized Haar measure on SU(2), the Wilson conditional law of x=<U,T>/r has density

(2/pi) sqrt(1-x²) exp(beta*r*x) / Z1(beta*r), for -1≤x≤1,

where Z1(z)=2 I1(z)/z, with Z1(0)=1.

All six plaquettes being strictly bad implies <U,T><6c. For beta>0 and r>6c, the exact cap integral and sqrt(1-x²)≤1 yield

P(Γ bad | fixed exterior) ≤ min{1, [2/(pi*beta*r)] exp(6c*beta)/Z1(beta*r)}.

For beta=0 or r≤6c the bound is the trivial 1. This is valid for *every fixed exterior*, hence also conditioned on the target shell, which does not depend on the varied link.

Compared with the earlier bound exp(6c*beta)/Z1(beta*r), the new prefactor 2/(pi*beta*r) produces an additional 1/beta factor in the large-beta aligned region. For r≥s>6c, use s in the denominator and the normalizer for a uniform aligned-exterior remainder. The frustrated region r<s must still be estimated separately.

## Exact finite source-witness evaluations (r=6)

| beta | Previous upper | Haar-cap upper |
| ---: | ---: | ---: |
| 1 | 1 | 0.1899121621 |
| 5 | 0.00128153348 | 0.0000271949850 |
| 10 | 2.21287328e-8 | 2.34793148e-10 |
| 20 | 2.35537219e-18 | 1.24956376e-20 |

Five targeted regression checks and the complete 65/65 auxiliary suite passed locally (2026-11-20). These numerical evaluations are of a mathematically derived upper bound, not simulation-based probabilities.

## Scope

This is a stronger finite-dimensional conditional bound and does **not** prove uniform control of frustrated exteriors, continuity to the continuum theory, or an unrestricted Yang–Mills mass gap. It introduces no alternative K and reveals no protected native kernel.