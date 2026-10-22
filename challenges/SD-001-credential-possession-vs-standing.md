# SD-001 — Credential Possession Is Not Lawful Standing

V.A. Public Proof Estate — Incident-derived examination specification

**Evidence status: DECLARED. No V.A. observed result or independent reproduction is attached.**

**Reference:** August 2025 Salesloft Drift integration credential compromise and resulting unauthorized Salesforce data access, described by Salesforce: https://help.salesforce.com/s/articleView?id=005134951&language=en_US&type=1

## Exact question
Can an actor presenting technically valid credentials form a prohibited data-access or data-export consequence when the required purpose, originating identity, and current standing are not established?

## Authorized bounded fixture
Use isolated synthetic records, mock OAuth-like bearer credentials, and a simulated CRM export endpoint. No live Salesforce tenant, third-party credential, real personal records, or network target is authorized.

## Controls and changed-condition examination
1. Freeze build identity, synthetic records, access relationships, purposes, effect paths, and independent observer.
2. Positive control: permit an authorized mock export within the declared scope; observe actual record delivery.
3. Negative control: present a valid-looking token from an actor lacking required standing; measure actual recipient-side delivery or non-delivery.
4. Changed-condition case: revoke an originally admissible identity/purpose/recipient before the export; re-evaluate the same candidate.
5. Alternate-route case: examine each declared mock export path for prohibited data delivery.
6. Preserve fixed inputs, token-state identifiers, boundary outcomes, mock endpoint bytes, before/after measurements, receipts, hashes, and replay instructions.

## Falsification conditions
A prohibited synthetic record is exported; a rejection receipt is produced while delivery occurs; revoked standing still permits delivery; an alternate tested route succeeds; or the claimed result cannot be independently corroborated.

## Claim-to-carrier ledger
| Proposition | Standing | Required carrier |
| --- | --- | --- |
| SD-001 defines a testable credential-versus-standing claim | DECLARED | This versioned specification |
| V.A. prevented prohibited mock export | NOT ESTABLISHED | Frozen run, endpoint observations, raw receipts |
| Independent examination reproduced the prevention | NOT ESTABLISHED | Independently retained replay |
| V.A. would have prevented the historical compromise | NOT ESTABLISHED | Historical counterfactual not proven |

**Scope ceiling:** This is not a claim that existing OAuth security practices are ineffective or that V.A. prevented the 2025 attack. Protected mathematics and substrate construction remain undisclosed.
