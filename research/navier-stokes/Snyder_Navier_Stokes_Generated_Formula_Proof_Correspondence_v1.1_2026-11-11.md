---
title: "Navier–Stokes: Generated Formula and Proof-Evidence Correspondence"
subtitle: "V.A. / URK public mathematical research | Version 1.1 methodology repair"
author: "Research lineage: Terry Allen Snyder · V.A. / URK"
date: "11 November 2026"
geometry: "margin=0.82in"
fontsize: 10pt
colorlinks: true
urlcolor: blue
---

**PUBLIC REPAIR — VERSION 1.1**  
**This is a versioned addition to the 8 November classical proof record, not a replacement of its original eleven mathematical pages.**

## The correction

The public site previously began with the classical Navier–Stokes derivations and independent numerical comparisons. That was an incomplete description of the intended native URK mathematical workflow:

> **URK generator → generated kernel (the operative mathematical formula) → admissible input data → execution → results and proof witnesses → mathematical verification.**

The generated kernel is not a peripheral numerical program. In the native method **the generated kernel is the formula**. Results receive mathematical standing only to the precise extent that the evidence and governing invariants establish the claimed proposition.

The original native implementation remains protected. The public witness examined here is an explicitly identified **numerical specialization**; it must not be confused with the original protected mathematical kernel.

## Formula identity and proof standing

For a mathematical domain $D$, an invariant family $\mathcal I$ and conditions $\mathcal C$, write the disclosure-safe *abstract* correspondence

$$
K_D=\mathcal G(D,\mathcal I,\mathcal C),\qquad
(r,w)=K_D(x),\qquad
V_D(K_D,x,r,w)\Rightarrow P_D(x).
$$

Here $K_D$ denotes the generated mathematical kernel/formula, $x$ its admissible data, $r$ its result and $w$ its witness. This is a **structural account of the URK method**, not an assertion that these symbols reproduce protected source code or that any finite replay resolves the unrestricted Navier–Stokes problem.

### Three distinct carriers

| Carrier | What was actually executed or preserved | What the evidence proves |
|:--|:--|:--|
| Native URK generator lineage | Original source method is described in the supplied companion README, but protected kernel internals and Navier–Stokes-domain output are excluded | The intended generator-to-formula relation, not an authenticated public unrestricted regularity theorem |
| Public-safe harmonic-edge numerical companion | Continuation 77 Fourier pair-rate formula, **six-mode input**, **30 interactions** and byte-identical output | Correct execution and finite-snapshot numerical correspondence |
| Classical 11-page original plus independent midpoint replay | Original classical equations and source excerpts; documented **17/17** bounded comparison checks | Classical formulation and finite-mode numerical checking, with unrestricted regularity not independently established |

## Mathematical formula evaluated on the public witness

For nonzero Fourier frequencies $k=\ell+m$ with $k\cdot U_k=0$ and $U_{-k}=\overline{U_k}$, the ordered nonlinear interaction is

$$
P_k v=v-\frac{k(k\cdot v)}{|k|^2},\qquad
\boxed{F_{\ell,m\to k}=-iP_k\bigl[(U_\ell\cdot m)U_m\bigr].}
$$

Its signed contribution to instantaneous kinetic-energy change at child frequency $k$ is

$$
T_{\ell,m\to k}=\operatorname{Re}\left(\overline{U_k}\cdot F_{\ell,m\to k}\right),\qquad
Q_k=\nu |k|^2|U_k|^2.
$$

A not-yet-occupied child can have $U_k=0$ and hence $T_{\ell,m\to k}=0$ while the amplitude-change rate $F_{\ell,m\to k}$ is nonzero. The public program makes this distinction; it is a snapshot calculation, **not a complete time evolution**.

## Proof of the finite-mode energy identity

Let $u$ be a smooth, real, divergence-free periodic Galerkin field. With $\mathcal P$ the orthogonal projection onto the retained incompressible Fourier modes, the nonlinear energy term is

$$
\operatorname{Re}\sum_k\overline{U_k}\cdot N_k(U)
=-\langle u,(u\cdot\nabla)u\rangle
=-\tfrac12\int_{\mathbb T^3}\nabla\cdot(u|u|^2)\,dx=0.
$$

The final integral is zero by periodicity and $\nabla\cdot u=0$. Consequently the **finite Galerkin system** satisfies

$$
\boxed{\frac{d}{dt}\left(\frac12\sum_k |U_k|^2\right)
=-\nu\sum_k |k|^2|U_k|^2.}
$$

This proves the energy equality **within the projected finite-mode model**. It does not justify an a priori bound for every arbitrary smooth datum uniformly over increasing cutoffs, nor prove unrestricted global smoothness.

## Reproduced evidence from the original supplied input

| Quantity | Reproduced value |
|:--|:--|
| Fourier modes in original seed | 6 |
| Ordered pair interactions | **30** |
| Initial smallness diagnostic | $\epsilon=17\sqrt2/512=0.04695630968816916$ |
| Source-stated smallness threshold ($\nu=1$) | $\nu/8=0.125$ |
| Viscous-to-heat rate | $1.33514404296875\times 10^{-5}$ |
| Instantaneous nonlinear energy transfer | $0$ |
| Kinetic/heat balance residual | **0** |
| Fresh numerical output vs archived example | **Exact byte match** |

The source companion also reports child $k=(1,2,0)$ amplitude-change rate $(-3/10485760,\ 3/20971520,\ i/4194304)$ and its pressure carrier $i/5242880$. Those are finite initial-state identities. The small-data continuation bound in Continuation 77 is an **inherited conditional statement**; this replay does not independently prove the original all-time theorem.

## Public reproducibility and original proof sources

Run after extracting the attached v1.1 ZIP:

```bash
python VERIFY_PUBLIC_EDGE_WITNESS.py
```

The standard-library-only verifier reruns the public edge-rate specialization, checks its exact source/input hashes and compares every byte of the generated result against the original archived example. It also checks the reported Fourier and energy-balance invariants. **This is a witness-checking program, not the protected native kernel.**

The separately preserved original source appears at:

- [Original classical Navier–Stokes proof extract, eleven pages](https://deagletwc.github.io/va-proof-estate/research/navier-stokes/Snyder_Classical_Navier_Stokes_Proof_Extract_11pp.pdf)
- [Original classical partial LaTeX excerpt](https://deagletwc.github.io/va-proof-estate/research/navier-stokes/ORIGINAL_PART_II_CLASSICAL_TEX_EXCERPT.tex)
- [Original independent finite-mode replay](https://deagletwc.github.io/va-proof-estate/research/navier-stokes/Deagle_Navier_Stokes_Classical_Public_2026-11-08.zip)

## The exact boundary of the proposed answer

**The identity of the generated mathematical kernel, its data inputs, execution output, proof witnesses and theorem scope must be examined together.** Reproducing a finite snapshot is valuable proof of that defined computation; it is not by itself a proof for every smooth three-dimensional Navier–Stokes initial state. A complete unrestricted result needs a valid global-in-time construction and bounds with the necessary continuum/limit and quantifier control, derived from the mathematical formula itself.

**Publication standing:** author-proposed mathematical research for independent examination; no certification, journal acceptance, unrestricted regularity determination or prize award asserted. The protected generator and native operators were not released.
