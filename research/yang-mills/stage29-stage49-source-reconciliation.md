# Yang–Mills Original Stage 29 → Stage 49 Source Reconciliation

Date: 2026-11-20  
Status: OBSERVED in a source-linked local replay; **not** an unrestricted mass-gap proof.

## Result

The original Stage 29 continuous-SU(2) Wilson-lattice implementation was recovered from the nested, hash-custodied Stage 83 master archive. A separate adapter translated its key convention (mu,x) and (mu,nu,x) to the exact-component predicate recorded at Stage 49. Original source files were not modified.

On the Stage 49 finite witness, the original Stage 29 plaquette and action methods reproduce:

- 1,024 links on the periodic four-dimensional L=4 lattice;
- Wilson action S_W/beta = 12;
- six bad plaquettes in the specified component;
- 66 link-sharing boundary plaquettes;
- target plaquette scalar trace 3/5;
- changed-condition control: replacing the designated defect link by identity makes the exact-component event false.

The distance condition used at Stage 29, ||I-U_p|| > sqrt(4/5), agrees with trace scalar < 3/5 away from equality. The Stage 49 target sits on the equality shell and is handled separately.

## Verification

- Three new cross-stage regression checks: PASS.
- All auxiliary continuance checks: **60/60 PASS**, Python unittest (2026-11-20).
- Original Stage 29 pytest suite: **not rerun** in this session because pytest is unavailable in the execution runtime.

## Boundary

This establishes an executable cross-stage finite-witness correspondence. It does **not** establish a general exact-sector probability, a controlled continuum limit, uniform spectral gap, or an unrestricted Yang–Mills theorem. The private native NEW K/URK substrate remains undisclosed and is not replaced by the public diagnostic adapter.

Next question: can a uniform, quantitatively bounded sector-weight estimate be proven under the unfrozen continuous-SU(2) measure, with explicit volume and coupling dependence?
