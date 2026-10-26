# M27 — Original protected-target readback consistency preflight

**Public code / synthetic test controls only.** This is an examiner aid for the still-open **Milestone 27** evidence gate, **not an actual native V.A. execution, an original pilot receipt, an external instrument report, or a qualified independent witness**. Milestone 28 (causal changed-condition external consequence) is not opened by this work.

## Why this distinct M27 preflight exists

The estate already has a signed-statement checker for a fuller ALLOW / REFUSE / CHANGED witness packet: [`verify_independent_witnesses.py`](../scripts/verify_independent_witnesses.py). That checker binds declarations, signatures and referenced measurement files, but does not directly compare the content of raw **protected-target before/after readback bytes** for the M27 permitted/refused pair. This new checker performs that narrower, data-only comparison without pretending that digitally supplied values establish independent sensing or physical effect truth.

`../scripts/preflight_m27_target_readback.py`:

- Requires an unchanged declared original SHA-256 identity and **exactly one permitted and one refused** bounded case, with the same candidate, target and effect route, and distinguishable governing conditions.
- Verifies hashes of separately supplied raw target-capture files and their separately hash-bound pre/post observation records. Source files may not be shared between cases or stages.
- Requires recorded acquisition sequence to increase and separate readback declarations, not decision-label-as-measurement. **ALLOW** requires changed recorded target bytes; **REFUSE** requires unchanged recorded target bytes.
- Matches saved original decision receipts to candidate, route, target, condition, and frozen original identity; rejects route, receipt and capture substitution.
- Requires the declared unexamined route list to exactly match the uncovered routes, preserving gaps rather than declaring universal closure.
- Optionally rehashes the original frozen file with `--original`, rejecting any byte mismatch; no historical freeze date is inferred.
- Refuses source symlinks, traversals, tampering, missing captures and a packet that self-declares release or independent effect qualification.

## Private input layout

Place private source records under an examiner-controlled directory *outside the public repository*. Never populate the repository with actual private pilot ZIPs, partner/customer records, operational route names, secret instruments or protected native code.

```text
private-m27/
  manifest.json
  cases/
    permitted/
      receipt.json
      before.json
      before.bin
      after.json
      after.bin
    refused/
      receipt.json
      before.json
      before.bin
      after.json
      after.bin
```

The `manifest.json` uses `schema: va-m27-target-readback-candidate/1.0`, `classification: PRIVATE_CUSTODIAL_REVIEW`, `releaseAuthorized: false`, `independentEffectsQualified: false`, `originalFrozenSHA256`, `declaredRoutes`, `unexaminedRoutes` and a `cases` array. Each case supplies `caseId`, `kind` (`ALLOW` or `REFUSE`), `candidateId`, `route`, `targetId`, `observerId`, `instrumentId`, `governingConditionSHA256`, `readbackOutsideDecisionProcess: true` and `{path,sha256}` for `receipt`, `before` and `after`.

Each receipt records matching `caseId`, `candidateId`, `route`, `targetId`, `governingConditionSHA256`, `originalFrozenSHA256`, and the original `decision` (`EXECUTE` for ALLOW, `REFUSE` for REFUSE). Each snapshot uses `schema: va-m27-target-snapshot/1.0`, the case/stage (`before` or `after`), matching route/target/observer/instrument, `measurementSource: SEPARATE_TARGET_READBACK`, `decisionLabelIsMeasurement: false`, an `int` acquisition `sequence`, a human-inspectable `calibrationOrAuditReference`, `rawCapture: {path,sha256}`, and `readbackSHA256` of those original capture bytes.

**All path/digest values are literal source references, not assertions of independent observation.** An examiner must verify that the raw capture actually originated outside the controlled decision process and represents the protected target, not a copied label or generated test value. If the target state has multiple security-relevant outputs or alternate paths, include those as declared routes, preserve uncovered gaps, and retain private original acquisition traces for review.

## Local-only use

```sh
python3 scripts/preflight_m27_target_readback.py \
  --packet /private/m27-source \
  --original /private/unchanged-frozen-original.bin \
  --out /private/m27-readback-report.json

python3 -m unittest discover -s scripts -p 'test_preflight_m27_target_readback.py' -v
```

`--original` is optional and if omitted the report explicitly sets `frozenOriginalBytesRechecked: false`. `--out` creates a new output exclusively and refuses an existing path or a path inside the source packet. No applicant workflow is executed. The tests construct *only synthetic local bytes*; a passing test demonstrates validator behavior, **not a real instrument observation**.

## Standing / human gate

Even a completely consistent packet returns only:

`SOURCE_RECORDS_INTERNALLY_CONSISTENT_HUMAN_QUALIFICATION_PENDING`

The checker always sets `realWorldEffectIndependentlyProvedByThisTool`, `nativeVALineageQualified`, `instrumentTruthAuthenticated`, `independentObserverIdentityAuthenticated`, `M27CompletedByThisTool`, `M28AuthorizedByThisTool`, and `publicationAuthorized` to **false**. Real M27 acceptance still needs a separately identifiable, authorized frozen native source; independent acquisition of protected-target **permitted effect** and **refused non-effect**; adequate instrumentation, original records and route inventory; authentic examiners; actual custody; and human review. Original source and any proposed public extract require **separate exact-byte custody, owner/partner rights, safety, privacy and non-reconstruction authorization** under the [Public Interest Publication & Harm Prevention Charter](PUBLIC-INTEREST-PUBLICATION-CHARTER.md).

**Disposition:** public data-checking capability available; M27 real-consequence measurement **HOLD**; M28 **not started**.
