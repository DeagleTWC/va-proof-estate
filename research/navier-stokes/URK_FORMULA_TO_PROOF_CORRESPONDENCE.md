# Navier–Stokes: URK Formula-to-Proof Correspondence (v1.1)

**Author:** Terry Allen Snyder · V.A. / URK mathematical research. **Release:** 11 November 2026.

## Correct operating order

**Generator → generated domain kernel (the mathematical formula) → admissible input data → execution → result and witness → hypothesis-checked derivation → mathematical conclusion.**

The kernel is not merely software that assists an unrelated formula. In the native URK construction, the generated kernel **is the operative formula** through which data are resolved. For public-scope review, the formula identity, input and output hashes, witness and proved assertion must be cross-linked. The abstract notation below describes the intended proof transmission and is not disclosure of protected native algebra:

- `K_D = G(D, I, C)` — generate a domain formula under invariant family I and conditions C.
- `(r, w) = K_D(x)` — resolve admissible domain input x into result r and witness w.
- `V_D(K_D, x, r, w)` — verify the witness against the declared proposition and its required quantifiers.
- A proof of the full theorem requires an independently checkable argument that the verified witnesses entail the theorem over its **entire stated domain**, not only selected computations.

## The available source tracks and what each establishes

| Track | Formula and data | Execution and witness | Proof standing |
|---|---|---|---|
| **Original native URK mathematical generator** | Original *Universal Resolving Kernel Generator v0.1*, attributed in the supplied companion README to Samantha Revita and Terry Snyder; protected operators and native outputs are outside this public release | Source documentation records the native generation→admission distinction | **Framework lineage; original Navier–Stokes-specific generated-kernel source and proof-witness binding not authenticated in these public files** |
| **Supplied domain generator v1 archive** | `urk_kernel_generator_v1.zip`, SHA-256 `5b3b635195fc5fb49db53f3a35b44d670ac5c57cfc4018358f7220da4b7ba30c` | 12/12 tests reproduced separately; creates eight governance/domain specifications | Kernel generation demonstrated, **not identified as the Navier–Stokes differential formula generator** |
| **Quantitative harmonic-edge specialization (public-safe source)** | `04_PUBLIC_COMPANION/urk_harmonic_edge_rates.py` implements the stated Continuation 77 finite-snapshot Fourier formula; six-mode input `04_PUBLIC_COMPANION/urk_harmonic_edge_input.json` | 30 ordered harmonic edges, byte-identical archived output, constrained input and zero snapshot energy-balance residual | **Exact source-to-input-to-output numerical correspondence on the supplied finite snapshot**; it is expressly a companion and not the protected URK kernel |
| **Unmodified original classical manuscript** | Original rendered pages 5–15 and partial Part II LaTeX source, already hosted in the 8 Nov 2026 version 1.0 | Fourier–Galerkin identities, named hypotheses, original theorem text, and independent 122/250-mode midpoint comparator (17/17 previous checks) | Original **classical formulation and proof sections**, preserved verbatim; numerical comparisons do not independently prove unrestricted global smoothness |

The **original public 11-page PDF remains untouched**. The November 11 addendum improves **identity and evidence binding**, not the historical mathematics or the rights boundary.

## The mathematical formula evaluated by the public-safe companion

On the periodic three-dimensional torus, for zero-mean divergence-free modes `U_k` satisfying `k·U_k=0` and `U_-k=conj(U_k)`, the projected nonlinear Fourier formula is

`F_(ell,m→k) = -i P_k ((U_ell · m) U_m)`, with `k=ell+m ≠ 0` and `P_k(v)=v-k(k·v)/|k|²`.

For the finite supplied snapshot, the signed kinetic-energy transfer rate is

`T_(ell,m→k) = Re(conj(U_k)·F_(ell,m→k))`.

Viscous-to-heat rate is `Q_k = nu |k|² |U_k|²`. The public script uses the given six-mode input; it is not an all-time propagator. A generated child can have nonzero amplitude derivative but zero **instantaneous** kinetic transfer while unoccupied, and must not be described as absent.

### Finite-mode energy identity and its proof

For a smooth, divergence-free real periodic Galerkin field `u`, orthogonal projection onto the retained divergence-free Fourier subspace preserves its inner product against `u`. Therefore the nonlinear term obeys

`Re Σ_k conj(U_k) · N_k(U) = -Re <u, (u·∇)u> = -(1/2)∫ div(u)|u|² dx = 0`,

by periodic integration by parts and `div(u)=0`. Thus, for the projected finite-mode differential equation,

`d/dt [ (1/2) Σ |U_k|² ] = - nu Σ |k|² |U_k|²`.

This is an **exact finite-mode identity**, not an unrestricted regularity proof. The public companion tests its **instantaneous** numerical consequence on the supplied initial data, not the physical all-time or infinite-cutoff conclusion.

### Reproduced numerical witness (11 Nov 2026)

- Six supplied Fourier input modes and **30 ordered interactions**.
- `epsilon = 17 sqrt(2)/512 = 0.04695630968816916 < nu/8 = 0.125` at `nu=1`.
- Initial viscous-to-heat rate `0.0000133514404296875`.
- Instantaneous nonlinear energy transfer sum `0`, kinetic/heat balance residual `0`.
- Child `k=(1,2,0)` amplitude derivative `(-3/10485760, 3/20971520, i/4194304)` and pressure carrier `i/5242880` in the original companion README.
- The generated example JSON is **byte-for-byte equal** to the archived companion example, SHA-256 `3be2cad99b8b66441b9ca62a3db7dfec53a59bc56201f8636556076282496258`.
- `epsilon` is an initial-data smallness diagnostic under the source-stated Continuation 77 conditions, not a proof of all large-data global smoothness.

## What the original release proves, and what it does not

The original classical pages and source-derived identities must remain primary mathematical references. A finite-mode ODE energy identity, an instantaneous harmonic edge-rate map and the independent finite-mode 17/17 replay do not jointly establish unrestricted three-dimensional regularity. In particular, there is **no publicly authenticated native generated-kernel → all admissible smooth initial data → uniform-in-cutoff continuation and regularity proof** in the files tied to this addendum. This states a **public source coverage limit**, not that protected original work cannot exist.

## Independent examination

1. Get the original unchanged 11-page PDF from the Navier–Stokes page.
2. Extract the v1.1 public source and evidence ZIP.
3. Run `python VERIFY_PUBLIC_EDGE_WITNESS.py` using Python 3 standard library.
4. Inspect `04_PUBLIC_COMPANION/urk_harmonic_edge_rates.py`, the original input, recorded example and your regenerated byte-identical result.
5. Examine the original classical equations and identify exactly which mathematical proposition each numerical witness supports.

**Public identity:** this addendum supplies no protected native new-K operator or proprietary generator source. Hashes identify retained artifacts but do not certify theorem correctness.
