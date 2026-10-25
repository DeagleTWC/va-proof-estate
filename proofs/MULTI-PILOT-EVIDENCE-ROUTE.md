# Milestone 09 — Multiple Pilots, Real Workflow, Original Evidence

**Public reading route.** V.A. / The Shift has historical engineering layers, original freezes and multiple pilot activities predating this website. The six earlier GitHub examination surfaces are **not** a complete inventory of those activities and cannot substitute for original pilot records.

## Source recovery and admissibility

Controlled source review confirms that historical materials can occupy materially different stages: a bounded workflow proposal, a frozen and tested build proof base, a pilot deployment specification, a pilot execution packet, a recorded live result, an accepted pilot, or an independently reproduced test. **One stage does not silently grant the next.**

An original source may record acceptance controls for a frozen engineering proof package while the associated live-pilot run sheet is still awaiting its first run. Both facts can coexist. This is not a contradiction, a demotion of previously tested work, or proof that other pilots did not run. The precise source identities, customer details and private result packets remain protected unless release has been authorized.

## Parallel pilot lanes, not one reset history

| Existing evidence lane | Evidence objects a reviewer should locate | What does not automatically follow |
| --- | --- | --- |
| **Original engineering freeze** | Immutable original artifact ID, frozen bytes/digest, author/custodian, test input, original verification report | A build test is not automatically a live customer-pilot outcome |
| **Live-workflow pilot** | Actual configured workflow and bounded consequence; executed case, original receipt, replay and operational observation | A signed offer, scope document or blank result record is not a completed live run |
| **Changed-condition pilot verification** | Original permitted case, changed material condition, denied/non-effect observation and scope of alternate paths | Refusal decision alone does not measure no-effect in every route |
| **Commercial pilot acceptance** | Specific signed acceptance, date, criteria, exceptions, and results; customer release rights | A successful engineering verifier does not prove customer acceptance or production rights |
| **Independent reproduction** | Distinct reviewer identity, frozen same original, independently retained results and negative controls | Two signatures or stated reviewers do not alone establish independence |
| **Current native V12** | V12-specific frozen identity, native observation and custodian clearance | An earlier V1.2 engineering freeze or a similarly named project cannot become V12 merely by relabeling |
| **Physical KCD** | Separately instrumented physical apparatus, measured consequence, calibration, negative controls and independent repetition | Neither a software receipt nor earlier V.A. pilot grants physical KCD standing |

**Do not count** GitHub repositories, PDF proposals, published site milestones or file hashes as the number of prior pilots. A historical original may remain confidential while its existence and phase are preserved in a private custody record.

## Milestone 09 local tool

The public code includes a [private multi-pilot evidence-router](../scripts/multi_pilot_evidence_audit.py) and [synthetic regression tests](../scripts/test_multi_pilot_evidence_audit.py). It inspects file fingerprints and whether each *declared evidence role* has actual source bytes, separately for each locally named pilot. It does not contact the network, upload files, execute those originals, or treat a user-assigned role as verified outcome truth.

Use the [private manifest template](pilots/PRIVATE-REVIEW-TEMPLATE.json) as a starting point **outside** the public repository and fill it from the actual source records. Never place customer names, original partner workflow details, protected source, secrets or private result material into GitHub.

```bash
python scripts/multi_pilot_evidence_audit.py audit --root "/private/source-folder" --manifest "/private/pilot-review.json" --out "/private/private-audit-result.json"
```

The report is explicitly **PRIVATE**, not an admissible public proof packet. Missing artifacts, altered digests, unsafe paths, unsupported promotion, duplicate pilot IDs or an attempted output overwrite are rejected. Claim-stage checks are structural; a human must still inspect whether a purported receipt is genuine, whether a positive or refused physical effect actually occurred, and whether the witness is independent.

Only a separate, approved [historical carrier public-release procedure](historical/ADMISSION-GUIDE.md) can admit public-safe extracts into this website. Preserve each historical original unchanged with its own freeze identity, distinguish any later public extract, and retain contradictory, unsuccessful and incomplete results rather than rewriting them.

## Current publication ceiling

The website does not yet expose the user's complete private historical pilot corpus. Its public files do **not** establish the number of historically executed pilots, the outcomes of all earlier workflows, or independently reproduced native V12 consequences. Milestone 09 prepares the path to inspect them under custody, rather than resetting their history or using synthetic fixtures to fill missing original evidence.

**FUNCTION MUST BE OPEN TO EXAMINATION. CONSTRUCTION NEED NOT BE OPEN TO RECONSTRUCTION.**
