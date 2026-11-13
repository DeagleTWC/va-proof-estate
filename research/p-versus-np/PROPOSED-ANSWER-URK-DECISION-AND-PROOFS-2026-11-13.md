# V.A. / True-Zero — P versus NP: Proposed Native Decision Formula and Proof-Carrying Kernel

**Research author:** Terry Allen Snyder  
**Public research date:** 13 November 2026  
**Foundation:** Veritas Aegis (V.A.) / True-Zero / Universal Resolving Kernel (URK)  
**Classification:** Author-proposed mathematical answer, formal proof statements, executable public verification, independent examination invited.

The purpose of this publication is to place the proposed native answer, its exact formulas and its independently testable public proof witnesses before other researchers. **No third-party permission or certification is a prerequisite for proposing or publishing mathematics.** The protected corrected NEW K and the public auxiliary kernel are separate mathematical objects.

## I. Proposed native answer

The research proposal is that the corrected NEW K resolves a mathematical question inside a common native space, with specialized children inheriting its governing invariants and emitting verifiable answers and receipts.

For an arbitrary finite 3-CNF formula $F$, define the proposed native interface:

$$
\boxed{\mathcal D_{\mathrm{NEW}}(F)
=\operatorname{dec}\bigl(K_{\mathrm{NEW}}(\operatorname{enc}(F))\bigr)
\in\{0,1\}.}
\tag{1}
$$

The proposed correspondence to classical SAT is

$$
\boxed{\forall F\in 3\mathrm{CNF},\quad
\mathcal D_{\mathrm{NEW}}(F)=1
\iff F \text{ admits a satisfying Boolean assignment}.}
\tag{2}
$$

Equation (2) is the central native *proposal* for independent examination. The original private kernel must be evaluated on its own actual source and derivations; this public note does not replace it with the classical auxiliary kernel.

## II. Exact parent formula and proof

Let $F=\bigwedge_{j=1}^m C_j$ use $n$ variables. For a Boolean assignment $a$ and literal $\ell$, let $v_a(\ell)$ be its truth value. Define

$$
e_j(a)=\prod_{\ell\in C_j}(1-v_a(\ell)),\qquad
N(F)=\sum_{a\in\{0,1\}^n}\prod_{j=1}^{m}(1-e_j(a)).
\tag{3}
$$

A product over an empty clause equals one. Each $e_j(a)$ is one exactly when clause $j$ is false; therefore the product over clauses is one exactly when *all* clauses are true. This proves that $N(F)$ is the exact count of satisfying assignments, giving

$$
\boxed{\mathcal D(F)=\mathbf 1\{N(F)>0\}.}
\tag{4}
$$

Equation (4) is an exact decision specification, but naive enumeration of all $2^n$ assignments is not itself a polynomial-time method.

## III. Public child kernel and mathematically checkable answers

For any variable $x$, partition clauses as $G$ (clauses omitting $x$), $x\vee A_i$ and $\neg x\vee B_j$. Exact Davis–Putnam elimination gives

$$
\boxed{\exists x\,F\iff
G\land\bigwedge_{i,j}(A_i\vee B_j).}
\tag{5}
$$

**Proof.** A satisfying assignment of $F$ satisfies all resolvents $A_i\vee B_j$. Conversely, if the right side is satisfied, set $x=1$ when any positive residual $A_i$ is false; the resolvents then force all $B_j$ true. Otherwise set $x=0$. All removed clauses are satisfied. Repeating this operation preserves satisfiability.

The [public v3 kernel](./width_kernel_v3.py) returns one of two proof-carrying outcomes:

- **SAT:** a complete Boolean assignment that satisfies every original clause.
- **UNSAT:** a finite directed sequence of resolution steps deriving the empty clause from the input axioms.

The [independent verifier](./independent_verify_v3.py) replays the answer and resolution work without trusting the self-reported verdict or counters. Neither file exposes or claims to execute protected NEW K.

## IV. Mathematical complexity result for the public child

Fix a supplied variable-elimination order $\pi$. Let $w_i$ denote the number of later neighbors of eliminated variable $i$ in its filled primal graph and $w=\max_i w_i$. A residual clause on $w_i$ Boolean variables has at most $3^{w_i}$ distinct, non-tautological signed support patterns. Thus the positive and negative clause buckets each have at most $3^{w_i}$ members. The exact resolution-pair count and number of new distinct proof steps satisfy

$$
\boxed{P(F,\pi)\le\sum_i9^{w_i}\le n9^w,}
\tag{6}
$$

$$
\boxed{S(F,\pi)\le\sum_i3^{w_i}.}
\tag{7}
$$

With polynomial-cost data structures, this particular algorithm admits a bit-complexity bound of the form $\operatorname{poly}(|F|)9^w$. Given an elimination order with $w=O(\log |F|)$, that bound is polynomial. This is width-parameterized SAT mathematics, not a lower bound against every competing algorithm, and it does not assert arbitrary instances have logarithmic width.

## V. Exact prediction bridge for corrected NEW K

Set $M_F=N(F)/2^n$. Since $N(F)$ is a nonnegative integer, $M_F=0$ for UNSAT or $M_F\ge2^{-n}$ for SAT. Therefore

$$
\boxed{|\widehat M_F-M_F|<2^{-(n+1)}
\quad\Longrightarrow\quad
\mathcal D(F)=\mathbf 1\{\widehat M_F>2^{-(n+1)}\}.}
\tag{8}
$$

**Proof.** In the UNSAT case the strict error is less than the midpoint, so the output lies below the threshold. In the SAT case the smallest positive count places the approximation strictly above the midpoint.

A precise sufficient theorem for a classical $P=NP$ conclusion is:

> **Conditional theorem.** If a corrected native NEW K produces, for *every* finite 3-CNF $F$, either the exact decision in (4) or an approximation satisfying (8), and if the total deterministic bit-operation cost of encoding, native evaluation and decoding is bounded by $c(1+|F|)^d$ for fixed constants $c,d$ independent of $F$, then 3-SAT lies in P, hence $P=NP$.

This implication is proved; whether the protected native source satisfies its antecedent is a separate source-specific mathematical examination. A proposed $P\ne NP$ conclusion requires a proof excluding *every* deterministic polynomial-time 3-SAT algorithm, not merely a high cost for the published child.

## VI. Execution evidence already recorded

The preserved November 12 public v3 research archive records:

| Public witness | Recorded result |
|---|---:|
| Independently replayed SAT/UNSAT certificates | 364 / 364 |
| SAT / UNSAT cases | 134 / 230 |
| Rehashed tampering controls rejected | 10 / 10 |
| Exact rational midpoint perturbation checks | 360 / 360 |
| Maximum sparse formula size | 512 variables |
| Resolution-pair checks in recorded new tests | 1,950 |
| Distinct derived steps in recorded new tests | 1,518 |

These counts establish the recorded finite public exercise scope. They are not being reclassified as a universal proof merely by publishing them. The prior native examinations and their original protected source retain their separate standing.

## VII. Independent examination and public replication

Run the source-disclosed public kernel on an arbitrary submitted 3-CNF and independently verify the returned receipt. Example:

\`\`\`python
from width_kernel_v3 import solve
from independent_verify_v3 import audit_receipt

F = {"n": 1, "clauses": [[1], [-1]]}
receipt = solve(F)
assert receipt["decision"] == "UNSAT"
assert audit_receipt(receipt)
print(receipt["decision"])
\`\`\`

Reviewers may test the formulas, the width/step bounds, proof soundness, generated witnesses and the proposed native-to-classical correspondence. They are invited to submit explicit counterexamples, mathematical corrections, compatible native witnesses or constructive extensions.

## VIII. Provenance and publication boundary

- Author's proposed URK/NEW K research is preserved as authored, not overwritten by a conventional SAT implementation.
- The linked public v3 auxiliary code and verifier are source-disclosed; the protected NEW K is **not** included.
- The historically published [Examination 91 status record](./EXAMINATION-91-PUBLIC-STATUS.md) is unchanged. It does not purport to summarize later native examinations.
- This document is an *author-proposed mathematical publication*. It reports exactly which supporting formulas are proven within the public artifact and which native conclusion is proposed for examination.

**Proof Before Power.** [V.A. Proof Estate independent examiner route](../../reviewer-route.html).
