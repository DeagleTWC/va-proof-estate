# URK harmonic-edge rate generator — quantitative companion to Continuation 77

**Classification:** New public-safe numerical specialization / verification aid, **not** a modification of the original URK mathematical generator, **not** a protected native NEW-K implementation, and **not** a global Navier–Stokes closure proof.

## Source continuity

- *UNIVERSAL RESOLVING KERNEL GENERATOR v0.1* (Samantha Revita & Terry Snyder) supplies candidate generation, truth, conservation, capacity/remaining margin, lawful shape, harmonic coherence, and the distinction **generation is not promotion**. It **does not specify a numerical harmonic edge-rate function**.
- *NAV–URK Continuation 77* supplies an explicitly specialized 3D periodic phase lattice. Every directed pair of phases `ell, m` generates a child `k = ell + m`. We calculate a rate from its explicit formula, rather than introduce an arbitrary tuning coefficient.

## Numeric definitions

For nonzero `k = ell + m`, the ordered candidate interaction has instantaneous complex **amplitude-change rate**

`F[ell,m -> k] = -i * P_k[(U_ell · m) U_m]`, where `P_k v = v - k(k · v)/|k|²`.

The **signed kinetic-energy rate at child k**, attributable to this ordered pair at this snapshot, is

`T[ell,m -> k] = Re[conj(U_k) · F[ell,m -> k]]`.

The mode's **viscous-to-heat conversion rate** is `Q[k] = nu |k|² |U_k|²` in normalized periodic-volume averages. For input t=0 under the Continuation 77 small-data conditions, the paper derives a *conditional* all-time **local** integrated heating bound `4 epsilon²`. This program does not calculate a full time trajectory.

**Important:** A newly generated unoccupied child (`U_k = 0` at the snapshot) has **zero instantaneous kinetic-energy transfer rate**, although `F` can be nonzero. The second time derivative of child kinetic energy at t=0 from its generated amplitude is `|F_total|²`. Do not misreport zero instantaneous transfer as a nonexistent interaction.

## URK check/proof boundaries

This numerical artifact checks the input's `k·U_k = 0` divergence compatibility and `U_-k = conjugate(U_k)` reality compatibility; rejects invalid inputs; computes an instantaneous Fourier phase pair-rate map; audits snapshot nonlinear energy-rate balance; and reports the candidate class as **DREAM_OR_PAUSE_PENDING_ORIGINAL_URK_INVARIANT_CHECKS**. It **does not** implement the original URK's full native standing decision, consequence binding, or protected mathematical construction. Rates are not themselves authorization.

For a finite supplied snapshot, the computed edge graph is finite. No claim is made that it exhausts all future harmonic descendants or proves a global continuation theorem. A valid smallness flag describes **the supplied initial state** under the mathematical assumptions of Continuation 77, not arbitrary states.

## Run

Python 3 standard library only:

```bash
python urk_harmonic_edge_rates.py --demo --example-input urk_harmonic_edge_input.json --output urk_harmonic_edge_rates_example.json
python urk_harmonic_edge_rates.py --input urk_harmonic_edge_input.json --output my_rates.json
```

Input `modes` is a list of `{ "k": [kx, ky, kz], "u": [[re, im], [re, im], [re, im]] }`, with viscosity and optional `rho`. Input must include both ± phase partners for real fields.

## Exact source reproduction

Using Continuation 77's `eta = 1/1024`, `nu = 1`, and `e^rho = 2`:

- Initial norm `epsilon = 17 sqrt(2) / 512 = 0.04695630968816916`, which is below the stated `nu/8 = 0.125`.
- Child at `k=(1,2,0)` has summed amplitude rate `(-3/10485760, 3/20971520, i/4194304)`.
- Corresponding pressure carrier is `i/5242880`.
- Initial total heat conversion rate in normalized volume is `1.33514404296875e-05`.
- Small-data conditional local total heat capacity ceiling is `4 epsilon² = 289/32768`.

The program asserts numerical correspondence to the source's exact child and pressure values. These numerical checks do not independently prove the fixed-point theorem or the unrestricted large-data case.

## Research target

To seek the unrestricted 3D closure, a follow-up must establish a bound on **the evolving infinite lattice's signed, frequency-resolved transfers**, consistent with the unchanged equations, **without assuming the small-data condition**. This static edge generator makes transfer mechanisms measurable on test inputs; it does not provide that missing bound.
