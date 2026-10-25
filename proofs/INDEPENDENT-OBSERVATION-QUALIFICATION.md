# Milestone 15 — Independently Signed Consequence Observation Qualification

**Purpose:** Qualify *evidence* from historical V.A. pilots and applicant-owned real workflows, without confusing a recorded decision, verified archive, signed statement, actual external consequence, and qualified independent witness.

## Historical evidence brought forward

The earlier original V1.2 engineering archive has a reproduced eight-case verifier and tamper check. The later April integration and connected-environment records have completed three-case capture/receipt source files and constrained closeouts, but the v1 and v2 connected packages refer to **the same recorded run**. This history is genuine work that predates the October Proof Estate. None of these particular local archive records alone authenticates the external observer, cryptographic signature, physical side-effect formation or actual human independence. The recorded “replay held” field is **not** a witnessed rerun.

The [historical review of externally submitted engineering](THIRD-PARTY-EVIDENCE.md) remains separately creditable *as a technical review of the submitter's work*, subject to rights and original-carrier admission. It is **not** a third-party reproduction of native V.A. without evidence of that different examination.

## Three necessary custody objects

1. **Frozen system/source object:** original source identity, exact SHA-256 from original custodian, contemporaneous freeze record, protected consequence and complete route inventory. The original may remain in authorized private custody.
2. **Execution and effect original:** fixed challenge, case outcome, original enforcement receipt, independent measurement of the actual protected effect/non-effect, any alternative paths, material-condition change and independently attempted replay. A response label is not an effect measurement.
3. **Independently attributable examiner records:** separate people, identities and qualifications established through human verification; affiliations/conflicts disclosed; measurements retained separately; each examiner signs exact original statement bytes and binds the same frozen object, challenge, receipt, condition, effect route and measurement digest.

A detached cryptographic signature verifies that a particular **key** signed the referenced bytes. It cannot alone prove who controls the key, whether the human reviewer is independent, whether the instrument is calibrated, or whether the effect is real. For this reason the automated result is *never* “independently reproduced.”

## Run the local, data-only preflight

Install Python 3.11+ and **OpenSSL**. The standalone public checker has no Python dependencies and never executes user-uploaded workflows.

Prepare one private directory:

```text
private-independent-review/
  manifest.json
  challenge.json
  receipts/
    allowed.json
    refused.json
    changed.json
  measurements/
    <case>-<observer>.json
  statements/
    <case>-<observer>.json
    <case>-<observer>.json.sig
  keys/
    observer-1-public.pem
    observer-2-public.pem
```

**Never put private keys in this directory** if it may be shared. Each examiner keeps their private signing key under separate custody; only the public signing keys, statements, signatures, receipts and permission-cleared measurements enter a qualified public extract. Applicants must have authority to test every effect route they examine.

The immutable `manifest.json` uses schema `va-independent-observation-bundle/1.0`. It declares:
- `classification: PRIVATE_CUSTODIAL_REVIEW`, `releaseAuthorized: false`, `independentHumanWitnessStatus: NOT_AUTHENTICATED`.
- `originalFrozenSHA256`, `challenge: {path,sha256}`, `cases`, and `unexaminedNegativeRoutes`.
- Every case binds `caseId`, `kind` (ALLOW / REFUSE / CHANGED), `candidateId`, `governingConditionSHA256`, `route`, `decision`, `receipt: {path,sha256}` and **two** `witnesses`.
- A CHANGED case references a preceding ALLOW `caseId` through `changedFrom` with the same candidate and different governing condition digest.
- Each witness entry references `statement`, `signature`, and `publicKey`, each with an exact path and file SHA-256.
- The immutable challenge source itself declares `schema: va-witness-challenge/1.0`, `challengeId`, `originalFrozenSHA256`, and `declaredRoutes`. Unexamined negative routes must be explicitly preserved, even when a partial test passes.

Each *signed witness statement* uses schema `va-independent-effect-statement/1.0` and binds `observerId`, `affiliationAndConflicts`, `caseId`, `candidateId`, `challengeId`, `challengeSHA256`, `originalFrozenSHA256`, `originalReceiptSHA256`, `governingConditionSHA256`, `declaredRoute`, `effectObserved`, `instrumentId`, `measurementMethod`, `methodology`, `measurementExternalToDecisionLabel: true`, `measurement: {path,sha256}`, and exact `independenceDeclaration` string:
`I conducted this observation separately; affiliations and conflicts are disclosed.`

The source `measurement` JSON must use schema `va-external-effect-measurement/1.0` and preserve `caseId`, `observerId`, `observedRoute`, `effectObserved`, `instrumentId`, and an inspectable `sourceDescription`. The data-only verifier validates relationships and byte digests, not actual instrument truth.

To sign an examiner statement (on the examiner's machine, **outside** shared evidence storage):

```sh
openssl pkey -in "/secure/observer-private.pem" -pubout -out "keys/observer-public.pem"
openssl dgst -sha256 -sign "/secure/observer-private.pem" \
  -out "statements/allowed-observer-1.json.sig" "statements/allowed-observer-1.json"
```

Every file referenced by the manifest must have its actual SHA-256 recorded; any modification after signing invalidates its hash or signature.

Run:

```sh
python scripts/verify_independent_witnesses.py \
  --packet "/private/private-independent-review" \
  --original "/private/unchanged-original-source.zip" \
  --out "/private/independent-preflight-private.json"
```

The optional `--original` verifies the *actual original bytes* against the manifest's declared source SHA-256. Omitting it leaves `frozenOriginalBytesRechecked=false` in the report. **A present-day hash check cannot authenticate the historical creation or freeze date.**

## Machine gates and human gates

The checker verifies, in a **single local packet**: two distinct signing keys and declared reviewer identifiers *per case*, real detached OpenSSL signatures, exact SHA-256 of each statement and separate measurement file, positive permitted effect, refused/no-effect, changed-condition same-candidate binding, original receipt source identity, and unresolved negative routes. It rejects changed bytes, re-signed claims against the wrong original, repeated keys, missing controls and invented route closure.

**A successful local result means only `SIGNED_RECORDS_INTERNALLY_BOUND_HUMAN_QUALIFICATION_PENDING`.** The machine cannot establish whether two keys belong to the same person or organization. A qualified independent review must inspect actual original chronology, external instruments, route completeness, authentic operator and examiner identities, conflict disclosures, privacy, source ownership and customer release permission.

Human disposition then applies a bounded choice: **NOT ESTABLISHED**, **HOLD**, **NARROW**, **PUBLIC BOUNDED OBSERVATION** or **INDEPENDENTLY REPRODUCED** — the last only when qualified evidence truly supports it and publication is separately authorized. None can be granted by altering JSON status fields.

## Public Proof Estate route

The [BYO workflow evidence desk](../examiner/BYO-WORKFLOW-EVIDENCE.md) already accepts authorized applicants and maintains original-workflow ownership. The additional [independent observation candidate issue form](https://github.com/DeagleTWC/va-proof-estate/issues/new?template=independent-effect-review.yml) lets a candidate request examination without exposing protected source, customer identity, private keys or raw confidential measurements.

**Public carrier admission is a separate action.** The [historical carrier register](historical/PUBLIC-CARRIER-REGISTER.json) still requires authorization for a specifically bounded extract, **separate original and extract hashes**, original custody and an identified human reviewer. The [qualification status register](INDEPENDENT-WITNESS-STATUS.json) does not elevate previously recovered M13/M14 source records to an independently reproduced native V.A. result.

**An operational claim reaches only as far as the independently observed and authorized consequence.**
