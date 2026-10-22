# VA-AD-001 — Changed authority before protected effect

**Publication location:** DeagleTWC / V.A. Proof Estate, with no external runtime or Kamanaka repository dependency.

**What this actually is:** A small, runnable, self-contained **synthetic examiner fixture**, not the protected native V.A. runtime and not a pilot. It demonstrates a public testing procedure, not a verified V.A. operational result.

## The exact question

Given an authorized candidate whose authority is later revoked, does a protected mock effect occur? A decision word saying "REFUSE" is insufficient; compare the independently captured **before and after mock state**.

## Run on a clean machine

Python 3 standard library only; no package installation, external services, credentials, or customers.

```sh
python3 proofs/VA-AD-001/run.py > result.json
```

From this repository's root, inspect `result.json`. Repeat the command and compare it with the saved [local fixture report](./local-fixture-report.json). The runner asserts actual state observations, checks receipt digests, and repeats the same cases deterministically.

## Four cases

| Case | Conditions | Expected decision | Expected observed mock effect |
| --- | --- | --- | --- |
| Positive control | Active authority, approved candidate, valid evidence | ADMIT | Yes |
| No authority | Missing authority | REFUSE | No |
| Changed condition | Originally approved candidate, authority REVOKED | REFUSE | No |
| Stale evidence | Active authority, evidence invalid | REFUSE | No |

The only load-bearing difference between positive and changed-condition cases is the authority value. In each run the script records the mock state before and after, returns an explicit decision, and fingerprints the resulting record.

## Proof ceiling — do not overpromote

- **Observed here:** One local execution of this illustrative test fixture; four cases passed, the same-condition replay comparison passed, and self-hashed receipts passed.
- **Not observed here:** Native V.A. execution; hardware effects; a live downstream integration; a Kamanaka test run; an original January 2026 pilot packet; a customer's production state; independent third-party reproduction.
- **Technical limitation:** The mock effect is confined to a single in-process route. Its observer is the same Python process, not a separately instrumented independent witness. It does not establish that every alternate route is closed.

**Falsification for this fixture:** A non-admitted case mutates the protected mock state; an admitted case fails to show the declared effect; repeated identical conditions diverge; or a receipt fails verification. These are specimen tests, not claims about protected V.A.

## What a native V.A. evidence promotion requires

An original, cleared carrier tied to the tested native build and run identity; specified conditions and candidate; measured actual effect/non-effect at the binding boundary; changed-condition test; original immutable receipts; replay; and separately attributed independent reproduction if actually completed.

**Open evidence. Protected construction.** Nothing here releases proprietary mathematics, substrate mechanics, pilot customer data, or rights to reconstruct V.A.
