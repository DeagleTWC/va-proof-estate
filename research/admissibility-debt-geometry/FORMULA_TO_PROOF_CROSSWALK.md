# ADG: original source → proposed formalization → proof/result

This crosswalk does not overwrite or rewrite the author's original `MATH SOLUTIONS.txt`. Each row distinguishes source content from added mathematical requirements.

| Original source section | Original formula/proposal | Manuscript output | Status |
|---|---|---|---|
| 1 | `D(x) <= D_max` | State-sublevel geometry, regular-boundary theorem | Proved under continuity/regular-value assumptions |
| 2 | `dD/dt = kappa` | Augmented trajectory debt and compatibility condition | Proved with local integrability / chain rule |
| 3 | Integral equals debt cap | First-hit theorem, exact equality on first contact | Proved with continuous cumulative debt |
| 4 | Constant stress lifetime | `tau=(B-d0)/k0`, and zero-stress case | Proved |
| 5 | `kappa(x) ~ 1/abs(x-xc)` | Temporal power-law integrability and transverse-approach log theorem | Proved with approach-rate condition |
| 6 | Irreversibility | No return to strict cumulative-debt reserve | Proved for debt coordinate |
| 7 | In admissible set ⇒ stable | Counterexample, not rebranded as theorem | Original claim needs additional dynamical hypotheses |
| 8 | `S_f=S_m-E[G]` | Exact bias removal and unchanged variance under constant subtraction | Proved; improved signal depth is not automatic |
| 9 | Largest tensor eigenvalue threshold | Symmetric PSD-growth eigenvalue monotonicity and hit bounds | Proved with matrix hypotheses |
| 10 | Minimize accumulated debt | Existence of minimizer on compact feasible path set | Proved under compactness and continuity |
| 11 | Domain independence | Conditional modeling scope | Proposed application program, not a universal theorem |

## Exact example child output

- `output/PREPARED_CONTRACT.json`: frozen scalar and tensor inputs, source SHA-256, contract SHA-256.
- `output/EXACT_EXAMPLE_CERTIFICATES_AND_RECEIPTS.json`: five rational calculation witnesses, five example-scope certificates, five linked receipts.
- `reproducibility/verify_exact_output.py`: independent rational recomputation, chain and source-hash verification, in-memory tamper negative control.

**No third-party audit, external certificate, patent grant, or unrestricted physical law is asserted.**
