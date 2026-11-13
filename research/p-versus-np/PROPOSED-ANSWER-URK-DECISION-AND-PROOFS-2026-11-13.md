# V.A. / True-Zero — P versus NP: Proposed Native Decision Formula and Proof-Carrying Public Kernel

**Research author:** Terry Allen Snyder  
**Public research release:** 13 November 2026  
**Research identity:** Veritas Aegis (V.A.), True-Zero / Universal Resolving Kernel (URK)  
**Publication standing:** Author-proposed mathematical answer and reproducible public evidence for independent examination. The preserved NEW K is a separate protected source, not replaced by the public kernel.

## 1. Proposed answer and decision object

The author's proposal is that the corrected native NEW K serves as a common mathematical decision foundation: a problem is encoded into the native mathematical space, resolved under its invariants, and returned with a consequence-bearing decision and verifiable proof witnesses. Applied to 3-SAT, the central proposed interface is

[
oxed{mathcal D_{m NEW}(F)=operatorname{dec}!ig(K_{m NEW}(operatorname{enc}(F))ig)in{0,1}.}
]

Here (F) is *arbitrary* finite 3-CNF, not a limited test suite. The proposed semantic correspondence is

[
oxed{orall Fin3mathrm{CNF}:quad
mathcal D_{m NEW}(F)=1iff F	ext{ has a satisfying Boolean assignment}.}
]

The public route below exposes exact decision mathematics, SAT/UNSAT proof witnesses, and test procedures without disclosing the original protected NEW K. This release does not ascribe a particular unconditional P=NP or P≠NP verdict to the protected source without quoting and evaluating its actual theorem.

## 2. Exact generating formula

For (F=igwedge_{j=1}^{m} C_j) on (n) Boolean variables and assignment (ain{0,1}^n), let (v_a(ell)) be the truth value of literal (ell) and define

[
e_j(a)=prod_{ellin C_j}(1-v_a(ell)),qquad
N(F)=sum_{ain{0,1}^n}prod_{j=1}^{m}ig(1-e_j(a)ig).
]

The empty-clause product is 1, as required. Then (N(F)) is **exactly the number of satisfying assignments**, and therefore

[
oxed{mathcal D(F)=mathbf 1[N(F)>0].}
	ag{A}
]

*Proof:* For each assignment, (e_j(a)=1) exactly if clause (C_j) is false. Hence (prod_j(1-e_j(a))) equals 1 exactly for a satisfying assignment. Summing counts all such assignments once.

Equation (A) specifies the desired answer for every finite 3-SAT instance. Evaluation by raw summation is exponential; a more efficient evaluator must be justified independently.

## 3. Public proof-carrying child kernel

The source-preserved public v3 code performs Davis–Putnam variable elimination, with independent SAT assignment or UNSAT resolution certificates.

Partition clauses into (G) (not mentioning (x)), ({xee A_i}) and ({
eg xee B_j}). Then

[
oxed{exists x,Fiff Glandigwedge_{i,j}(A_iee B_j).}
	ag{B}
]

*Proof:* Every assignment satisfying the left side makes each resolvent true. Conversely, from any assignment satisfying the right side, set (x=1) if a positive residual (A_i) is false, and (x=0) otherwise. The resolvents guarantee all remaining clauses are satisfied.

Repeated application of (B) either yields a valid assignment (reconstructed in reverse elimination order) or an empty-clause resolution refutation. A verifier checks proof steps and the final Boolean decision independently. These are genuine mathematical certificates, not screenshots or success counters.

## 4. Derived structural complexity theorem

For a fixed elimination order (pi), let (w_i) be the number of as-yet-uneliminated neighbors of variable (i) in the filled primal graph, and (w=max_i w_i). Since each neighbor has three clause-presence states (positive, negative, absent), a deduplicating eliminator encounters at most (3^{w_i}) different positive residual clauses and (3^{w_i}) negative residual clauses.

Consequently, for this specified public algorithm,

[
oxed{P(F,pi)le sum_i9^{w_i}le n9^w,}
quad
oxed{S(F,pi)le sum_i3^{w_i},}
	ag{C}
]

where (P) is the number of resolution-pair checks and (S) is the number of newly derived distinct non-tautological resolution clauses. With appropriate polynomial-cost data structures, the decision method has bit-complexity (operatorname{poly}(|F|)9^w). When an elimination order of logarithmic induced width is supplied, this is polynomial in input size.

This width-parameterized result is established SAT mathematics; its contribution here is the V.A. explicit proof, test receipts, and independent replay interface. Equation (C) does *not* assert that arbitrary 3-CNF always has logarithmic width.

## 5. Exact native-prediction bridge

Set

[
M_F=rac{N(F)}{2^n}.
]

Either (M_F=0) (UNSAT) or (M_Fge 2^{-n}) (SAT). Thus any exact or rigorously bounded approximation satisfying

[
oxed{|widehat M_F-M_F|<2^{-(n+1)}}
	ag{D}
]

permits the exact decision

[
oxed{mathcal D(F)=mathbf 1[widehat M_F>2^{-(n+1)}].}
	ag{E}
]

*Proof:* In the UNSAT case, (D) implies (widehat M_F<2^{-(n+1)}). In the SAT case, (D) and (M_Fge2^{-n}) imply (widehat M_F>2^{-(n+1)}). The strict inequality matters.

This is the precise public interface for testing a claimed NEW K prediction result: supply the approximation, its interval/error witness, a sound encoding and decoding, and a uniform accounting of bit operations.

### Consequence theorem (explicit quantifiers)

If the corrected native NEW K can, for every encoded finite 3-CNF (F), compute (mathcal D(F)) exactly—or calculate (widehat M_F) obeying (D)—with **uniform deterministic polynomial bit-time**, including native encoding, computation, and decoding, then 3-SAT belongs to P and hence (P=NP). This is a rigorously proved **conditional implication**, not a claim that the antecedent follows from the public v3 evaluator.

A proposed (P
e NP) route would instead require a universal lower-bound argument against all deterministic polynomial-time 3-SAT deciders, not only this particular eliminator. This release does not silently switch between the two routes.

## 6. Executed public evidence

The preserved November 12 v3 public package reports, for its own new checks (not the private historical examinations):

| Witness | Recorded outcome |
|---|---|
| Independently verified SAT/UNSAT certificates | 364 / 364 |
| SAT cases / UNSAT cases | 134 / 230 |
| Negative-control tampering attempts rejected | 10 / 10 |
| Exact rational midpoint perturbation checks | 360 / 360 |
| Maximum size of the sparse test formulas | 512 variables |
| Public v3 resolution-pair checks in these cases | 1,950 |
| Public v3 derived proof steps in these cases | 1,518 |

These counts support reproducibility and the tested scope, not by themselves a universal polynomial-time result. Historical native examinations, including their protected nested source and private mathematical claims, retain independent custody; this publication neither re-executes nor revises them.

**Reproduce the public kernel:** see [public v3 kernel](./width_kernel_v3.py) and [independent verifier](./independent_verify_v3.py). The verifier supports a JSON list of receipts generated by the kernel. This publication deliberately excludes proprietary NEW K code and unpublished source records.

## 7. Independent examination invitation

Examiners are invited to challenge or extend the work with a concrete formula, counterexample, a failed line of proof, an alternative native-to-classical correspondence, or an independently reproducible complexity witness.

Questions to test:
- Does each returned SAT assignment satisfy its source clauses, or does each UNSAT certificate derive the empty clause?
- Are the public resource bounds valid for their stated elimination order?
- Does an asserted corrected NEW K evaluator preserve the exact SAT decision for *every* 3-CNF?
- Is the claimed complexity measured in uniform classical bit operations, including all native transformations?

**Proof Before Power.** The objective is to make the author's proposed answer inspectable and extensible, not to require prior institutional acceptance.

## 8. Custody and limitations of this release

- Original NEW K/URK mathematical internals are protected and not published here.
- The public proof-carrying v3 kernel is an independently described auxiliary evaluator, not the original NEW K.
- Later private native examinations are neither invalidated nor certified by the contents of this public addendum.
- This addendum states the author's **proposed program**, exact supporting mathematical identities, public soundness theorem, and verified finite evidence. It makes no assertion of an independently authenticated unrestricted complexity conclusion without the corresponding source theorem.
- The prior published [Examination 91 custody note](./EXAMINATION-91-PUBLIC-STATUS.md) remains unchanged.

**Researcher contact and independent review:** [V.A. Proof Estate](../../reviewer-route.html).
