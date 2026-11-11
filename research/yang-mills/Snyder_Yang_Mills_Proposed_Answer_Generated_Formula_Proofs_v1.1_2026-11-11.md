---
title: "Yang–Mills: Proposed Answer, Generated Formula and the Proofs You Can Check"
subtitle: "V.A. / URK public mathematical record | Formula-to-evidence correspondence | Version 1.1"
author: "Research lineage: Terry Allen Snyder · V.A. / URK"
date: "11 November 2026"
geometry: "margin=0.82in"
fontsize: 10pt
colorlinks: true
urlcolor: blue
---

**PUBLIC FORMALIZATION CORRECTION — v1.1**  
**Editorial correction:** The initial November 11 release gave the finite SU(2) results before explaining the native URK proof workflow. The generator does **not** merely provide a software starting point: **the generated domain kernel is the operative mathematical formula; input data are resolved through that kernel and its outputs are examined as proof witnesses**. This revision places that workflow first and preserves the initial publication unchanged for historical traceability.

**Mathematical standing:** Author-proposed positive mass-gap answer. Exact finite-lattice theorems and reproducible structural checks are attached. The located execution records have **not yet authenticated a Yang–Mills-specific generated kernel through to a complete four-dimensional continuum mass-gap theorem**. That is an evidence-linkage finding, not an assertion that no further protected original exists.

# The URK method: generated formula, then proof evidence

A conventional reading of the earlier publication risks reversing the actual discovery method. The intended native structure is:

**Generator → generated domain kernel / mathematical formula → data evaluated under the kernel → output and proof witness → mathematical verification → theorem standing.**

A disclosure-safe *abstract specification* of that method is

$$
K_D=\mathcal G(D,\mathcal I,\mathcal C),\qquad
(r,w)=K_D(x),\qquad
V_D(K_D,x,r,w)\Rightarrow Q_D(x).
$$

Here $D$ names a mathematical domain, $\mathcal I$ the governing invariant family, $\mathcal C$ its lawful conditions, $K_D$ the **generated formula**, $x$ the actual input data, $r$ the result, $w$ the execution or mathematical witness, and $V_D$ the verifier for the specific proposition $Q_D$. **These symbols formalize the stated workflow; they are not a quotation of protected native operators or proof that a particular Yang–Mills instance has executed.**

A defensible proof record must identify each object and preserve provenance. The kernel's code hash can identify the operative formula without releasing proprietary source. Input hashes anchor the data. Outputs and witnesses must be accompanied by a verification whose tested conclusion *matches the theorem being claimed*, rather than only showing successful execution.

## Three source tracks—do not collapse them into one

| Track | Formula or generated object | Executed evidence | Actual mathematical scope |
|:--|:--|:--|:--|
| URK Generator v1 | Source-mapped compiler specifies eight domain kernels, including standing, conservation, resonance and consequence binding | 12/12 source unit tests; generator demo executed | Validates those domain specifications and decisions; this package contains no located Yang–Mills Wilson-measure kernel |
| URK harmonic-edge numerical companion | Fourier interaction amplitude $F_{\ell,m\to k}=-iP_k[(U_\ell\cdot m)U_m]$ and signed rate $T_{\ell,m\to k}=\mathrm{Re}(\overline U_k\cdot F)$ | 30 edges; source child and pressure reproduced; instantaneous energy-rate residual $0$ | Three-dimensional periodic Navier–Stokes specialization, **not** an SU(2) mass-gap theorem |
| Yang–Mills source stages | Wilson action, exact pivotal coarea/shell identity, covariance formula, chord/mediator incidence definitions | Stage 72 exact data and Stage 79 graph replay 14/14 | Four-dimensional **finite lattice** SU(2) calculations and conditional identities; the formula-generating provenance of a separate native Yang–Mills kernel is not carried in these public records |

The Stage 83 original audit traced the executable family through 45 nested ancestral archives and specifically distinguished graph enumerators from an executed continuous SU(2) admissibility/coarea kernel. It did not identify a callable native Yang–Mills proof-kernel instantiation. A finite graph verifier must not be silently labeled the generated native formula.

## What proof transmission requires

To turn a *particular generated Yang–Mills kernel* into an independently checkable proof, the record must preserve, without requiring release of protected internals: (i) a stable kernel/formula identity or mathematical statement; (ii) its SU(2)/Wilson definitions and invariant conditions; (iii) the input data and their domain; (iv) reproducible outputs and relevant witnesses; (v) the verifier's actual accepted proposition; and (vi) an analytic argument demonstrating the necessary quantifiers and continuum/physical spectral conclusion. Missing provenance is reported as **not located in this release**, not manufactured and not confused with disproof.

The verified structural record below remains valuable and valid within its stated scope. Its original statements are reproduced to permit direct comparison with version 1.0.

---

# The answer, in everyday language

**Our proposed answer is yes: a nontrivial four-dimensional quantum Yang–Mills theory should exist and possess a positive mass gap.** A mass gap means there is a strictly positive lower bound on excitation energy above the vacuum—no sequence of genuine excitations can creep down toward zero energy.

We are making the mathematics open to examination rather than asking readers to accept an assertion or wait for a prize committee. This release explains what the retained URK/SU(2) calculations prove, shows the equations, and identifies the bridge needed for the complete quantum-field-theoretic conclusion. **Reproducible calculations support their stated finite-lattice claims; they do not automatically settle the continuum problem.**

The official problem is broader than one gauge group: it asks for a nontrivial theory and a positive gap for *every* compact simple gauge group. Our identified lattice evidence concerns **SU(2)**. The official wording and scope can be checked at the [Clay Mathematics Institute](https://www.claymath.org/millennium/yang-mills-the-maths-gap/).

# The idea

Imagine a four-dimensional lattice, with a little **SU(2) matrix on each link**. Travel around a square (a *plaquette*), multiply its link matrices in order, and you obtain the plaquette's holonomy. The Wilson weight assigns relative probability to configurations using all such squares at once. Nearby variables cannot be treated as independent just because they do not share a square directly.

Our examination isolates a precisely defined **six-plaquette component**, follows its boundary and the exterior gauge variables, and derives the *actual conditioned probability* of its pivotal shell. This exact conditioning is the central safeguard: it prevents an apparently attractive but incorrect independence shortcut from entering the proposed mass-gap argument.

# Proof 1 — A real, globally consistent SU(2) configuration

On the periodic lattice

$$\Lambda=(\mathbb Z/4\mathbb Z)^4,$$

there are **1,024 oriented positive links** and **1,536 plaquettes**. Set every link equal to the identity except two:

$$U_2(e_1)=n^{-1},\qquad U_1(-e_2)=-n,\qquad n=(3/5,4/5,0,0),$$

using the standard unit-quaternion representation of SU(2). Stage 49 computes all plaquettes from these actual links (rather than prescribing plaquette values independently). Exactly six plaquettes have scalar holonomy $-3/5$, six have $+3/5$, and the rest have $1$.

For the Wilson-action convention

$$S_W(U)=\beta\sum_p\bigl(1-\tfrac12\operatorname{ReTr}U_p\bigr),$$

we obtain

$$\boxed{S_W(U^*)=\beta\,[6(1+3/5)+6(1-3/5)]=12\beta.}$$

**Why this is a proof:** the complete field is constructed from link variables, so the non-Abelian lattice Bianchi compatibility identities follow from the edge-product cancellations. The inherited Stage 49 component enumeration finds one six-plaquette *bad* component with **66 adjoining boundary plaquettes**: one on the pivotal threshold, the other **65 strictly good**. The finite-volume coarea argument then gives **positive pivotal-surface weight at each finite $\beta>0$** on a nonempty patch of the level set.

**What it proves:** the pivotal event is a genuine, compatible SU(2) configuration and not a fictitious independent collection of squares. **What it does not prove:** a volume-uniform estimate or a continuum gap.

# Proof 2 — The exact conditioned probability, without a shortcut

Let $c$ be a regular target-plaquette value, $b$ the exterior link data, and $\sigma_c$ the conditional Haar probability on the target's four-link shell. Define the full Wilson shell factor $A_b(c)>0$ and its exact-component contribution $A_{\Gamma,b}(c)$:

$$\begin{aligned}
A_b(c)&=\int e^{\beta Y_b(U_B)}\,d\sigma_c(U_B),\\
A_{\Gamma,b}(c)&=\int e^{\beta Y_b(U_B)}\chi_\Gamma(U_B,b;c)\,d\sigma_c(U_B).
\end{aligned}$$

Here $\chi_\Gamma$ checks the **whole event**, including component connectivity, strict-good boundary faces and the pivotal condition. Put $p_\Gamma(b,c)=A_{\Gamma,b}(c)/A_b(c)$, and let $\mathbb E_0$ mean expectation under the stated reference exterior measure. The exact conditioned fraction is

$$\boxed{\Pi_\Gamma(c)=\frac{\mathbb E_0[A_{\Gamma,b}(c)]}{\mathbb E_0[A_b(c)]}.}$$

**Proof:** first condition on the target plaquette's value. Integrate its four-link fibre against the full Wilson weight, both with and without the complete event indicator. Then integrate the exterior links. Dividing the event's shell density by the unrestricted shell density gives the displayed ratio. There is **no assumption** that crossing plaquettes or exterior links factorize. This is the exact Stage 53 disintegration identity.

Equivalently, introduce the *size-biased* exterior measure

$$\frac{d\nu_c}{d\mu_0}(b)=\frac{A_b(c)}{\mathbb E_0[A_b(c)]},\qquad
\Pi_\Gamma(c)=\mathbb E_{\nu_c}[p_\Gamma(b,c)].$$

**Why this matters:** configurations with a larger shell normalizer count more heavily. Omitting that weight would change the question being solved.

# Proof 3 — The exact correction for correlated exterior data

The Stage 54 identity quantifies precisely how the conditioned answer differs from the unweighted exterior average:

$$\boxed{\Pi_\Gamma(c)-\mathbb E_0[p_\Gamma]
=\frac{\operatorname{Cov}_0(A_b,p_\Gamma)}{\mathbb E_0[A_b]}.}$$

**Proof:** use $\mathbb E_0[A_bp_\Gamma]=\mathbb E_0[A_b]\,\mathbb E_0[p_\Gamma]+\operatorname{Cov}_0(A_b,p_\Gamma)$, and divide by $\mathbb E_0[A_b]$. Because $0\le p_\Gamma\le1$, Cauchy–Schwarz also gives the explicit bound

$$\boxed{\Pi_\Gamma\le m_\Gamma+
\frac{\sqrt{v_A\,m_\Gamma(1-m_\Gamma)}}{a},}$$

where $a=\mathbb E_0[A_b]$, $v_A=\operatorname{Var}_0(A_b)$ and $m_\Gamma=\mathbb E_0[p_\Gamma]$.

**Why this matters:** the difficult dependence is not swept away; it becomes a specific covariance quantity that an eventual uniform estimate must control. The identity is proved. **A volume- and weak-coupling-uniform estimate does not follow from the identity alone.**

# Proof 4 — Exact exterior geometry and independently repeatable enumeration

For the particular six-plaquette configuration, the recovered enumeration produces an exterior collar graph with **237 links**, **114 vertices**, and **two connected components**. The number of independent graph cycles is therefore

$$\boxed{237-114+2=125.}$$

**Proof:** a spanning forest of a graph with $V$ vertices and $k$ connected components has $V-k$ edges. The remaining $E-(V-k)$ edges generate its independent fundamental cycles. Here the forest has $112$ edges and the graph has $125$ chords. This is an exact finite graph theorem, not a physical mass measurement.

Stage 72 reconstructs **380 shared mediators** (96 internal, 284 exterior) and **1,375 chord–mediator incidences**. Stage 79 then verifies a **connected 221-vertex** internal incidence graph with **491 incidences**. Shared mediators explain why a naive claim of independent exterior variables would be unjustified.

The preserved Stage 72 original verifier recorded **2,029 assertions**, with byte-matching regenerated JSON outputs in the archived replay. The original Stage 79 verifier was re-executed during publication preparation: **14 of 14 structural checks passed**, and the regenerated JSON matched the archived file *byte for byte*.

# The bridge from correlations to a genuine mass gap

Here is the *precise logical difference* between a collection of finite-lattice proofs and the full proposed solution.

Suppose a nontrivial continuum Yang–Mills theory is rigorously reconstructed with vacuum $\Omega$, nonnegative Hamiltonian $H$ and the needed positivity properties. Suppose, moreover, that for a dense collection of vacuum-orthogonal vectors $\psi=A\Omega$, the corresponding positive Euclidean-time correlations obey a **common physical decay rate** $m>0$:

$$\langle\psi,e^{-tH}\psi\rangle\le C_\psi e^{-mt}\qquad(t\ge0).$$

Then the spectrum above the vacuum has a gap of at least $m$.

**Short proof of this conditional implication:** by the spectral theorem, the left side is $\int_0^\infty e^{-tE}\,d\mu_\psi(E)$ for a positive spectral measure. If $\mu_\psi([0,m-\varepsilon])>0$, it would force a lower bound proportional to $e^{-(m-\varepsilon)t}$, contradicting the stated faster upper bound as $t\to\infty$. Thus every such vector has no spectral weight below $m$. Density transfers this exclusion to the whole vacuum-orthogonal Hilbert space. $\square$

**This implication is a conditional mathematical lemma, not a claim that our archive has already established its hypotheses.** In particular, the currently reconciled SU(2) source material has not supplied a checked proof of the required uniform continuum reconstruction and physical-rate bound. The edge-rate numerical companion successfully reproduces the stated Navier–Stokes example; the formula generated for the Yang–Mills theorem must be traced and verified separately.

# Evidence anyone can ask to inspect

| Item | Evidence | Standing |
|:--|:--|:--|
| Global SU(2) component, Wilson action, finite pivotal shell | Original Stage 49 mathematical construction | **Source theorem** |
| Exact shell-size-biased identity | Stage 53 proof | **Source theorem** |
| Covariance correction and its bound | Stage 54 proof | **Source theorem** |
| 125 exterior cycles, 380 mediators | Stages 69–72 enumerators and records | **Finite exact enumeration** |
| 221-vertex internal incidence graph | Stage 79 original verifier | **14/14 checks rerun; byte-identical result** |
| URK kernel generator | Original package and recorded test run | **12/12 unit tests, different mathematical scope** |
| URK harmonic edge-rate generator | Original package and reproduced example | **Numerical reproduction; Navier–Stokes specialization** |
| Full four-dimensional continuum theory and positive gap | Requires a complete corresponding theorem and proof | **Proposed conclusion; not yet established by this evidence packet** |

The protected kernel internals and original nested master archives are not included in this public package. The release contains public-safe source notes, a finite graph ledger, runnable bounded verification, and SHA-256 custody records.

# Our invitation to the mathematical community

We are placing the reasoning and evidence where people can examine it openly. Readers are invited to reproduce the exact finite checks, verify the shell-conditioning and covariance proofs, identify a valid continuum closure if it appears elsewhere in the completed record, or demonstrate a specific error by pointing to an equation or counterexample. **This is an open author-proposed answer with proved intermediate results; not a declaration of independent certification or prize recognition.**

We want the strongest correct mathematical answer that the evidence can carry—and we want people to be able to check it.

---

**Source custody:** URK Yang–Mills original Stages 49, 53, 54, 69, 72 and 79. Public-safe source notes and finite combinatorial ledger are included with unchanged source-byte hashes. The full cumulative archive remains preserved separately. The archived and rerun **Stage 79 result JSON files** have matching SHA-256 `d2c99c3ac2026a1ffe2408c8c19d11c30dd60b45a9a3e6b19c4a51ffcde264e9`. Original Stage 72 ZIP SHA-256 `78bb9777a2edf658a2c6bfb7fdc13e50dd22270ade8b582e560b7def990eb9f1`.

**Release record:** Public author-proposed mathematical answer, released 11 November 2026 with source-to-result correspondence and independently inspectable finite-lattice evidence. Publication itself is not verification of the unrestricted Yang–Mills mass gap.


# Publication correction, source custody and version identity

This document is **version 1.1** of the public reader. Version 1.0 remains preserved as the original dated release. The amendment corrects the **order of mathematical explanation and provenance logic**, not any of the original finite-lattice counts or algebraic identities. It does **not** present a completed generated SU(2) proof-kernel execution that has not been located.

**Public supporting files:** `URK_GENERATED_FORMULA_TO_PROOF_CORRESPONDENCE.md` (formal workflow and claim-to-carrier mapping), `URK_PROOF_CHAIN_STATUS.json` (machine-readable evidence standing), original selected source notes, Stage 72 data, Stage 79 archived results, bounded replay and SHA-256 manifest.

**Protection:** Protected kernel formulas or native implementation bytes are not disclosed by this version; archived ZIP checksums identify the distinct inspected artifacts without turning a numerical companion or structural verifier into a native Yang–Mills kernel.
