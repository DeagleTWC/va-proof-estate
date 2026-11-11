# GRID-K1 — source → mathematical object → result

**Author:** Terry Allen Snyder · V.A. / Deagle  
**Prepared:** 11 November 2026  
**Standing:** Author-review draft; not a published Deagle research record.

Original Library sources are unchanged, identified by exact SHA-256. The author-custody archive retains both originals. **The public-ready bundle intentionally excludes the full source JSON and World Kernel Atlas DOCX** because they include draft architecture and other kernels; their disclosure remains the author's decision. This crosswalk is not a replacement for either original source.

| Source | Source statement / field | Mathematically formalized carrier | Evidence status |
|---|---|---|---|
| World Kernel Atlas | GRID-K1: Infrastructure Continuity Kernel, power/water/telecom, cascade exposure, hidden maintenance debt | Finite directed service-capacity network and monitored debt reserve | Source declaration → conditional formal model |
| Critical Infrastructure Continuity Kernel v1.0 | `approval_draft` | Retained exact original source status | No production claim |
| `continuity_corridor_profile` | Participating domains, graph, loads, degradation, reroutes | G=(V,E), service demands q, capacities c_e(m,xi), mode requirements | Defined |
| `infrastructure_authority_envelope` | Scope, signature, permissions, time window | Trusted predicate A(m,xi) | Assumed external verification; not cryptographically proved |
| `live_state_surface` | State, lag, synchronization, operational evidence | Attested state xi, trust predicate F(xi) | Input requirement, not field sensor proof |
| `maintenance_debt_state` | Debt and slow failure exposure | d_e^+=d_e+Delta_e, Delta_e>=0, strict reserve d_e^+<B_e | Proved monotone under stated assumption; exact rational examples |
| `dependency_graph` | Coupled domains and service prerequisites | Directed prerequisite set P, availability flags z_v | Defined; conditional guard |
| `CONTINUE` | Lawful continuation | Baseline demand, capacity, conservation, debt, authority, freshness | C01 passes; C02 refused after cut failure |
| `DEGRADE` | Lawful reduced-service mode | Vector minimum q>=q_min plus all normal guards | C03 passes; C06 refused on debt |
| `REROUTE` | Alternate lawful corridor | Full graph feasibility after authorized standby enabling | C04 passes; C05 and C07 refused |
| `ESCALATE`, `HALT`, `REFUSE` | Non-admission consequences | REFUSE is modeled; ESCALATE and HALT remain separately defined disposition states | REFUSE demonstrated; other two untested |
| `continuity_receipt` | Run/decision IDs, authority and state basis, failure reasons, timestamp | Hash-linked proof certificates and receipts | Seven exact example receipts; no claim of external cryptographic signature |
| `critical_failure_classes_closed` | Several proposed cascade classes | Finite cut obstruction and a conditional pre-effect invariant theorem | These **do not** certify closure of every declared failure class |
| `no_side_path_to_high_consequence_actuation` | Architecture constraint | No-bypass requirement explicitly assumed by conditional invariant theorem | Deployment test open |

## Main mathematical obligations

1. **Necessary cut inequality** — if sink demands exceed an applicable cut's capacity, the demanded single-commodity flow is impossible.
2. **Exact constructive witnesses** — admitted examples satisfy every modeled edge and balance constraint, service minimum, authority and debt check.
3. **Conditional invariant preservation** — valid initial states remain valid across admitted transitions *if* all execution paths enforce complete and correct next-state guards.
4. **Monotone debt reserve** — debt without a reset cannot return below a strict cap once reached.
5. **Multi-domain non-export in the modeled graph** — all shared capacities are checked globally; no guarantees extend to omitted dependencies.

## Run record

- Frozen contract: `output/PREPARED_CONTRACT.json`.
- One exact run: `output/EXACT_WITNESSES_CERTIFICATES_RECEIPTS.json`.
- Seven scenario-scoped certificates; seven hash-linked receipts.
- Exact arithmetic uses Python's standard `fractions.Fraction`.
- Read-only separately implemented replay verifier: `reproducibility/verify_exact_output.py`.
- One documented tamper negative control.
- All arithmetic code is a **public-safe reference demonstrator**, not the protected URK generator or installed GRID-K1 runtime.

## Limits that must accompany any publication

The network is a synthetic conserved service-flow abstraction; no electromagnetic grid equations, water hydraulics, telecom packet dynamics, field actuators, real-world timebase attestation, deployed no-bypass enforcement, external independent review, or production certification are demonstrated.
