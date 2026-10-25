# Milestone 14 — Earlier integration and connected-run records recovered

**Source position:** Actual archived **April 2026 completed capture and receipt records** were recovered from the Library. They predate the October public Proof Estate and are **not** newly generated site simulations. Their original ZIP bytes remain private. The [machine-readable bounded review](HISTORICAL-RUN-RECONCILIATION.json) preserves this distinction.

## Four distinct historical source objects examined

| Source | Original file stage | Actual archived content examined | Safe finding |
| --- | --- | --- | --- |
| Three-case integration completed v1 | Historical integration **simulation** | Filled EXECUTE, REFUSE, ESCALATE capture, three original receipt records and constrained closeout | Three recorded outcomes and their receipt fields cross-check. The source itself calls this a *simulation*. |
| Connected-environment executed v1 | First connected-environment completed capture | Filled three-case capture, three original receipt objects, constrained disposition | Original recorded decisions, binding flags, reported latencies and receipt identifiers agree within this version. |
| Connected-environment executed v2 | **Revised** completed capture | Revised three-case capture/receipts and constrained disposition | The **same connected run identifier** as v1 remains; latencies have changed, so this is **not a second independently identified pilot**. |
| Pilot-expansion readiness v2 | Later bounded readiness decision | Explicit constraints, revised latency references, proposed next expansion | Its recorded latency values match **connected v2**, and it conditions widening on unresolved identity, storage, rollback and budget locks. This is **not a completed widened pilot**. |

The two connected archives share one recorded run identity. The three captured decision classes were EXECUTE, REFUSE and ESCALATE. Across the three source packages **nine archived case entries** were cross-checked for internal agreement. Those entries do **not** mean nine distinct pilots, nine independently reproduced tests, or three cryptographically authenticated effect measurements.

### Original-source checks performed

- Recovered original ZIP bytes of the three recorded capture families and the separately archived v2 readiness record.
- Read the actual case observations, decision receipts and closeouts without executing archived code or contacting real customer systems.
- Matched each capture row to the original receipt's case decision, receipt ID, reported latency, binding flag and commit-boundary status.
- Confirmed that, **in those records**, only EXECUTE reports reaching the commit boundary; REFUSE and ESCALATE report non-binding paths.
- Checked the three source replay fields claiming **held** and connected-version fields claiming **chain valid**. **These fields were read, not independently replayed or cryptographically verified.**
- Detected changed reported latencies between connected v1 and v2, retained the same recorded run identity, and matched v2's values to the following readiness record.
- Preserved the disposition **GO_WITH_CONSTRAINTS**; it is not an unconditional operational promotion.

The connected v1 original identifies its capture author as **assistant**, and its archived `receipt_sig` fields contain named string tokens rather than a separately authenticated signature chain. Neither signature authenticity nor external-person independence was established from these files. Likewise, the presence of an EXECUTE receipt does not measure real-world protected effect, and a REFUSE string does not independently prove non-formation across other routes.

## Repeat the source examination, without publishing protected originals

The [historical run-lineage examiner](../scripts/verify_historical_run_lineage.py) is a **read-only, local ZIP scanner**, not an execution environment. It rejects misaligned capture/receipt fields, unsafe archive paths, bad reported latencies, missing decision classes and readiness mismatch. It treats same-ID connected v1/v2 as *revisions* and never silently counts them as separate independent pilots.

```sh
python scripts/verify_historical_run_lineage.py \
  --integration "/private/real_integration_completed_v1.zip" \
  --connected-v1 "/private/connected_environment_executed_v1.zip" \
  --connected-v2 "/private/connected_environment_executed_v2.zip" \
  --readiness-v2 "/private/pilot_expansion_readiness_v2.zip" \
  --out "/private/local-run-source-audit.json"
```

The original files remain under their custodian's control. The local output is **PRIVATE**, includes original source SHA-256 values and run identity, and must **not be uploaded to a public GitHub issue**. The public CI runs [artificial negative fixtures](../scripts/test_historical_run_lineage.py) only; these do not pretend to be historical test results.

## Milestone boundary

**Now locally established:** these actual earlier source files contain filled three-case integration/connected records and distinct version history; the cross-file receipt and outcome fields agree; the v2 readiness record refers to the revised connected capture; all reviewed closeouts impose constraints.

**Not established by these source objects:** independently measured external effects, authenticated receipt-chain signatures, separate human witnesses, public release permission, verified customer hospital deployment, a completed widened pilot, native V.A. V12 standing, or physical KCD examination.

This is not a finding that no other pilots happened. It is a bounded examination of these **specific recovered records**, with source-custody release still required before any complete original is publicly attached. See the [historical carrier release gate](historical/ADMISSION-GUIDE.md), [bring-your-own workflow review](../examiner/BYO-WORKFLOW-EVIDENCE.md), and [earlier V1.2 original engineering verification](V1.2-ORIGINAL-SOURCE-VERIFICATION.md).

**Preserve originals, failures, revisions and unresolved routes. Never inflate evidence counts.**
