# V.A. / URK movement kernel — public-safe Navier–Stokes specialization v1

Terry Allen Snyder · public companion examination · 24 November 2026

## Why this kernel is upstream of the individual witnesses

The disclosed URK generation principle is **generate → check → classify →
promote/refuse**. This companion generates *all* ordered Fourier interactions
from a chosen finite candidate state, then checks whether the generated
movement remains inside the physical constraint and exact kinetic accounting.
It does not manually repair individual child rates after inspection.

This is **new public-safe code**, not a copy, authentication, or publication of
the protected NEW K/URK parent generator. The Library's "Universal Resolving
Kernel Generator v0.1" is a written rule specification, not independently
executable source. The existing source-locked classical proof record and its
historical tests remain unchanged.

## One generator, five checks, one decision boundary

Take constant mass density \(\rho>0\), viscosity \(\nu>0\), a finite,
zero-free symmetric mode set \(\Lambda\subset\mathbb Z^3\), and a real
divergence-free Fourier field \(U\). For every \(k\in\Lambda\), admissible
movement belongs to the plane \(k\cdot U_k=0\). Its exact orthogonal
projector is

\[
P_k v=v-k\frac{k\cdot v}{|k|^2}.
\]

Generate the projected nonlinear contribution by **exhaustive ordered pair
enumeration**, without selecting a favored child or branch:

\[
N_k(U)=-iP_k\sum_{\ell+m=k}(U_\ell\cdot m)U_m,
\qquad \dot U_k=N_k(U)-\nu|k|^2U_k.
\]

The mass-weighted kinetic burden and *optionally declared* capacity are

\[
E_\rho=\frac\rho2\sum_{k\in\Lambda}|U_k|^2,\qquad
\Phi=C-E_\rho.
\]

Here \(C\) is an externally **specified candidate capacity**, not a newly
discovered physical constant. Density scales the energy burden; the
incompressibility constraint supplies the allowed movement plane. Do not infer
that this specialization establishes URK's broader mass-to-constraint law.

The five checks are:

1. Real-field conjugacy and incompressibility of every input mode.
2. Transversality of every generated nonlinear output.
3. Exact cancellation of total nonlinear energy transfer.
4. Exact mass-weighted kinetic/dissipation balance.
5. Nonnegative remaining capacity **if** a capacity was declared.

The common decision boundary returns `RUN` for the proved **finite projected
identity**, `ABORT` when a declared capacity is exceeded, and `PAUSE` for an
unrestricted regularity or blowup claim. An omitted capacity is recorded as
unknown, never silently treated as sufficient for physical deployment.

For admissible finite states, summation by parts establishes exactly

\[
\frac{dE_\rho}{dt}=-\rho\nu\sum_{k\in\Lambda}|k|^2|U_k|^2.
\]

The implementation uses only rational complex arithmetic and provides a
SHA-256 receipt of the ordered input, every generated nonlinear rate, all
checks, decision scope, and output. Verification recomputes from the inputs;
altering a receipt's claims, rates, or hash is rejected.

## Run and replay

From the repository root:

```bash
python research/navier-stokes/05_REPRODUCIBILITY/urk_movement_kernel_v1.py --demo \
  > /tmp/urk_ns_movement_receipt.json
python research/navier-stokes/05_REPRODUCIBILITY/urk_movement_kernel_v1.py \
  --verify /tmp/urk_ns_movement_receipt.json
python research/navier-stokes/05_REPRODUCIBILITY/urk_movement_kernel_v1.py \
  --demo --capacity 1 --claim UNRESTRICTED_REGULARITY
python -m unittest discover -s research/navier-stokes/05_REPRODUCIBILITY \
  -p 'test_urk_movement_kernel_v1.py' -v
```

The six-mode example includes an initially empty child whose velocity-change
rate is nonzero even though its instantaneous energy transfer is zero.
Negative controls reject incorrect conjugates, non-solenoidal states,
invalid physical parameters, exceeded capacity, false global promotion,
tampered rates, and tampered receipts.

## What this does **not** establish

Finite-dimensional Galerkin systems and their exact energy identity do not
rule out concentration as the cutoff grows. For unrestricted unforced
regularity, one would still need an independently proven cutoff-uniform
continuation bound (or a different sound resolution). No continuum
equivalence for a protected native generator is asserted here. The original
source crosswalk in `STEP5_PUBLIC_SOURCE_SCOPE_CROSSWALK.md` retains its
unresolved statement and is not overwritten by this kernel.
