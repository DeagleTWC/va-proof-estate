# Bring Your Own Workflow — Evidence Examination

**Your workflow remains yours. The Proof Estate examines evidence; it does not claim ownership or execute your code.**

Any outside person or team may bring a workflow **they have authority to examine**. It can be an enterprise workflow, a boundary candidate, a historic third-party implementation, or an independently run constrained real-world corridor. The site supports both the existing synthetic adapter challenge and a distinct **read-only real-workflow evidence route**.

## Choose the examination route

| Route | What is submitted or run | Standing it can reach |
| --- | --- | --- |
| **Interface behavior** | [Six-case local adapter](README.md), [generated matrix](README.md#generated-changed-condition-matrix-independent-interface-test), or [persistent-session local adapter](README.md#persistent-session-authority-challenge--separate-public-test) | Locally observed **synthetic interface** behavior only |
| **Real workflow evidence** | [Data-only verifier](byo_workflow_evidence.py) reads a locally frozen manifest, original case files, decision receipts, and independent effect-observer *records* | Local packet integrity and internal observation **consistency**; original effects and independence still need human examination |
| **External technical reviewer** | Frozen external original, separately retained challenge, negative controls, independent examiner-authored report | Bounded finding after identity, custody, scope and independent reproduction are checked |
| **Historic third-party review** | The original dated external-submission carrier and the actual bounded disposition under release authorization | Attributable historic review in its own scope, **not** an independent native V.A. result unless V.A. itself was examined |
| **Physical consequence** | Instrumented physical original, calibration, uncertainty, route coverage and reproduced observations | Physical qualification only after distinct qualified examination; metadata alone is not proof |

**A real-world consequence must be observed outside the submitting software's decision label.** A declaration of `REFUSE` without coverage of the protected state is incomplete. Unknown alternate paths stay explicitly unresolved.

## Process a privately owned real workflow locally

Requires Python 3.11+, no third-party dependencies, network or hosted execution. Prepare a **data-only** directory with:

```text
private-workflow-packet/
  manifest.json
  workflow.json
  cases/
    allowed.json
    refused.json
    changed.json
    replay.json                 (recommended)
  evidence/
    <case>-receipt.json
    <case>-observer.json
```

Create a **runnable synthetic example packet** on your own machine before preparing your original workflow:
```sh
python examiner/byo_workflow_sample.py --out "/private/synthetic-byo-example"
python examiner/byo_workflow_evidence.py --packet "/private/synthetic-byo-example"
```

This demonstration contains fabricated data and simulated effects; it is explicitly **not** an independent third-party or native V.A. proof. Then use [the sample builder](byo_workflow_sample.py) and [negative-control tests](test_byo_workflow_evidence.py) as the exact data grammar. The minimum three **different original cases** are an admitted positive consequence, a negative/refused case with no effect observed, and a changed-condition refusal tied to the same candidate as the positive case. The optional fourth replay references the original receipt SHA-256.

Each referenced file has a declared SHA-256 in its parent carrier; `manifest.json` has `schema: deagle-byo-workflow-evidence/1.0`, `packetCustody: PARTICIPANT_OWNED_LOCAL`, `externalEffectStanding: UNVERIFIED`, `releaseAuthorized: false`, `workflowId`, `workflow: {path, sha256}`, and `cases: [{path, sha256}, ...]`.

The workflow describes the bounded `protectedConsequence` and `declaredRoutes`. Each case declares a candidate, governed condition digest, declared route, decision, actual `effectObserved` claim, distinct receipt file, and distinct effect-measurement file. Refused and changed cases must not report formed protected effect. The changed case refers back to its allowed original; a replay binds the unchanged condition and original receipt hash.

Run:

```sh
python examiner/byo_workflow_evidence.py --packet "/private/workflow-packet" --out "/private/local-examination.json"
```

**The script never executes workflow code or contacts your infrastructure.** It checks file identity, hashes, relationships, declared routes, negative observations, changed conditions and replay consistency. Its success result is **`LOCAL_DATA_CONSISTENCY_ONLY`**, not a conclusion that effects actually occurred or that the reviewer was independent. A receipt is not its own external observer. Reviewer competence, actual sensor coverage, independence, customer permission, causal exclusion of alternate effects and commercial standing remain for an actual qualified examiner.

The report is written only outside the packet, without overwriting previous reports. The source directory remains under your custody.

## Bring it to the public Proof Estate

1. **Freeze your own original source before challenge issuance.** Keep original bytes, conditions, case IDs and original receipts; derive the SHA-256 values. Do not retroactively manufacture a freeze.
2. **Run the applicable local examiner.** Preserve success and failure records; retain rejected and unresolved alternative routes.
3. **Use [the public BYO workflow evidence submission](https://github.com/DeagleTWC/va-proof-estate/issues/new?template=byo-workflow-evidence.yml)**. Share only a non-confidential scope statement, bounded claim, exact permitted public carrier URL(s)/digest(s), and redacted verifier output.
4. **If the original is private**, do not upload it to a public GitHub issue. Use only a privately agreed, authorized review process and a release-cleared extract. Posting a hash does not authorize public disclosure.
5. **The examiner fixes the object** and determines which checks require execution, independent sensing, changed inputs or route challenges. Review may conclude **HOLD**, **NARROW**, **NOT ESTABLISHED**, **BOUNDARILY OBSERVED**, or **INDEPENDENTLY REPRODUCED**, but no self-reported local pass grants that last class.
6. **Third-party review credit** attaches to the actual dated frozen artifact, examiner identity and affiliation, original signed disposition, reproducibility and custody record — not to the existence of a public form.

## Prior examination history

The custodian has historical records of external-submitted frozen engineering work and bounded technical review, with original packages and correspondence retained outside this GitHub release. Those examinations may be reviewed as their *own* historical objects. The currently released website **does not** publish or reproduce those private submissions, confer external-reviewer independence without attribution, or convert third-party software test passes into native V.A. proof.

The review route is useful precisely because a scoped PASS can coexist with a distinct **HOLD/NOT YET HOLDS AT SEAM** disposition. Review outcomes must retain unresolved routes, observed failures and earlier frozen bytes. When publication rights are settled, use [the historical release gate](../proofs/historical/ADMISSION-GUIDE.md) and [the original review standard](../proofs/EXAMINATION-STANDARD.md).

**Open evidence. Protected construction. Independent consequence observation before promotion.**

## Historical source revision test

For participants or historians with their own lawful source archives, the [Milestone 14 read-only connected-run lineage examiner](../scripts/verify_historical_run_lineage.py) demonstrates a source-level audit pattern: bind each completed case to a retained receipt; identify revisions using unchanged run IDs, rather than double-counting them; and compare downstream readiness records to the correct preceding version. The three-case historical verification is **not** a public upload of the original pilot package and does not confer independent effect standing. Applicants may use this process on their own archives locally before presenting separately release-cleared evidence through the BYO issue route.
