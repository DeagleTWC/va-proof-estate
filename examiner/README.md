# Bring Your Own Work — Local Seam Examiner

**Your work stays yours. The protected V.A. foundation stays private.**

This is a **public, synthetic, executable examination interface** for engineers who want to test a bounded adapter of their own work against fixed consequence-boundary cases. It follows the earlier public Kamanaka style of a seam-facing, falsifiable test without granting outsiders custody of the underlying system.

**Nothing here is the native V.A. runtime, the proprietary mathematical floor, the Elements Basin, the Universal Resolving Kernel, or an actual deployment.** Do not interpret a pass as evidence that V.A. was run, or that a participant's technology is safe in production. The toy example is not a derivative of the protected native implementation.

## Run in a local checkout

Requires Python 3.9+; no third-party packages and **no internet connection**. Run only adapters you trust in your own environment; the examiner executes the supplied command as a subprocess.

```sh
python examiner/byo_seam.py --out local-report.json --adapter python examiner/example_layer.py
```

Expected with the toy example: **6 of 6 local synthetic checks**. To test your own layer, replace the command after `--adapter` with your local executable. The adapter receives one JSON packet through stdin and must print one JSON response on stdout.

Example input:

```json
{"protocol":"DEAGLE-BYO-SEAM-1","case_id":"SUB-002","case":{"candidate_id":"req-002","authority_active":true,"evidence_current":true,"authorized_target":"vendor-A","attempted_target":"vendor-B","route":"primary"}}
```

Expected adapter output for a refusal:

```json
{"case_id":"SUB-002","decision":"REFUSE","effect_request":null}
```

For an allowed attempt, return `"decision":"EXECUTE"` and an `"effect_request":{"target":"vendor-A"}` object. This is an **interface contract**, not the disclosure of a native governing algorithm. The examiner, not the adapter, records its **simulated** in-memory effect list.

## Fixed examiner cases

| Case | Examination | Expected |
| --- | --- | --- |
| EXEC-001 | Exact authorized candidate | EXECUTE and simulated effect |
| SUB-002 | Beneficiary/command substitution | REFUSE; no simulated effect |
| REV-003 | Authority removed | REFUSE; no simulated effect |
| STALE-004 | Evidence becomes stale | REFUSE; no simulated effect |
| ROUTE-005 | Substitution attempted on secondary route | REFUSE; no simulated effect |
| PATH-006 | Same valid candidate on secondary route | EXECUTE and simulated effect |

A receipt is generated for every case using canonical JSON and SHA-256, and the suite fingerprint identifies the fixed fixtures. Preserve an untouched report and rerun on the same machine for basic repeatability. If source changes, record the new version separately. Re-running the reference adapter does not confer independent witness status.

## Generated changed-condition matrix (independent interface test)

The starter six-case set is intentionally small and public. The second route generates a larger synthetic test matrix from a seed, changing the candidate identity and target for each cohort. It examines primary and secondary routes, command substitution, authority removal, stale evidence, multiple simultaneous failures, and exact repetition.

```sh
python examiner/adversarial_matrix.py --seed 20261024 --rounds 4 --out matrix-report.json --adapter python examiner/example_layer.py
python examiner/verify_matrix.py matrix-report.json --adapter python examiner/example_layer.py
```

Expected for the published **toy reference adapter**: **36/36** generated local cases (nine per cohort), with each packet sent twice. An intentionally unsafe adapter is provided so reviewers can see that failure is actually reported:

```sh
python examiner/adversarial_matrix.py --seed 20261024 --rounds 4 --out unsafe-report.json --adapter python examiner/negative_layer.py
```

This unsafe invocation **must exit nonzero** and records **8/36 passing** local cases. Automated checks also alter an archived response and verify that its receipt/report integrity check fails. `--seed` is repeatable: replacing it with a fresh locally chosen integer yields a different matrix, but the seed must be retained with the report.

**Challenge strength and limitation:** generated targets and paired changed-condition inputs reduce reliance on a single memorized example. Because the protocol and test oracle are public, a trivial imitation can still pass. Re-running the adapter as a separate subprocess does not prove long-lived autonomous state. A SHA-256 receipt detects alteration relative to its recorded digest, **not authorship, independent witnessing or actual external effect**. The examiner never controls real payment, data or hardware consequences. A production claim requires a separate real consequence-bearing witness.

**External layer ownership:** the participant writes an adapter *locally*, controls its code and decides what results to publish. The site accepts bounded observations for examination; it does not accept private proprietary internals or run arbitrary uploaded code on a V.A. server.

**Physical mechanism index:** [PH-01 through PH-04 public-safe engineering classes](PHYSICAL-MECHANISMS.md) distinguish corrected KCD from its one candidate EM embodiment and identify the independent evidence still required for physical standing.

## Persistent-session authority challenge — separate public test

The six-case and generated matrix examiners start a new process for each input. To make replay and state-transition behavior harder to ignore, the [persistent-session examiner](session_challenge.py) sends an entire sequence of JSON lines to **one running adapter process**. This is still a synthetic interface test, **not native V.A.**

```sh
python examiner/session_challenge.py --seed 20261024 --rounds 2 --out session-report.json --adapter python examiner/session_reference.py
python examiner/verify_session.py session-report.json --adapter python examiner/session_reference.py
```

The published toy reference is expected to return **54/54** passing events (27 per cohort). The cases include valid one-use ticket execution, second-use replay refusal, substituted target refusal, revocation, stale evidence, unauthorized secondary route, valid later primary route, expiry, capacity failure, cross-ticket injection and missing authority. Each cohort carries randomized ticket, candidate and target identities. The [broken sample](session_broken.py) intentionally executes attempted effects without respecting those constraints and **must fail**. The examiner separately checks reply identity, decision, requested simulated effect, report digests and exact local reproduction.

An adapter for this route reads one JSON packet per input line until end of file and writes exactly one JSON response per line. [Read the reference](session_reference.py) for the **public interface grammar only**; it is a toy and contains no protected native construction. `START` presents a ticket with an exact target, allowed routes and current conditions. `REVOKE`, `STALE` and `EXPIRE` change local state; `TRY` proposes an effect. A valid attempt consumes its ticket; a denied attempt does not create a simulated effect.

**Limit:** these inputs are generated and declared by the public examiner, and local toy adapters can be written to mimic its visible expectations. A passing adapter has not established external power custody, actual real-world route closure, physical non-formation, independent certification or V.A. native implementation.

## Physical-mechanism evidence preflight

Original records are identified in the [controlled public physical-mechanism index](PHYSICAL-MECHANISMS.md), without releasing construction. A [physical metadata preflight](physical_packet_preflight.py) helps prepare a **public-safe packet**, requiring custody approval, frozen artifact identifier and digest, measurement references, independent sensors, calibration, uncertainty, negative control, changed-condition examination, receipts and replay.

```sh
python examiner/physical_packet_preflight.py examiner/physical_packet_blank.json
```

The supplied blank packet is **supposed to fail**: it has no cleared measurements or release approval. No original experimental data or proprietary design is included. Even a metadata-complete packet is only **METADATA_PRESENT_UNVERIFIED**; the tool never authenticates observations or promotes a claim to proven physical consequence custody. Do not add private source, private mathematical construction, customer data, actuator instructions or unreleased blueprints.

## Evidence ceiling: important

**What this actually shows:** a supplied adapter returned suitable decisions and requested simulated effects for these six declared packets. The examiner generated deterministic local results.

**What this does not show:** no native V.A. execution; no real payment; no alternate-route closure outside the modeled routes; no physical apparatus, sensor, actuator, or measured non-formation; no production certification; no independent third-party reproduction; and no validation of the truth of the adapter's private internals.

A real-world claim requires a fixed artifact, complete consequence-bearing route, independent effect measurement, changed-condition and negative controls, retained receipts, replay, and an independent reviewer where applicable. **A self-reported REFUSE is not by itself proof of non-formation.** Report any actual bypass with an exact artifact version, input, effect observation, receipt and reproduction procedure.

## Bring your own implementation, not our IP

Participants can keep their work private and run this locally. Publish only a release-cleared adapter, bounded results and reproducible challenge packet, if desired. No secret, customer data, private substrate, private mechanical drawings, proprietary mathematics, executable actuator access, or sensitive enterprise infrastructure is requested.

**Review path:** [Examination standard](../proofs/EXAMINATION-STANDARD.md) | [Fixed-carrier issue intake](https://github.com/DeagleTWC/va-proof-estate/issues/new?template=bounded-proof-review.md) | [Physical witness requirements](PHYSICAL-WITNESS.md).

**The public Proof Estate is a curated present examination surface, not the whole underlying scientific, engineering, pilot or historical record.**

## Cross-foundation comparison and local custody — public-safe

[COMPARATIVE-EXAMINATION](COMPARATIVE-EXAMINATION.md) defines same-fixture comparisons and non-authenticating report custody. No executable uploads are accepted and external adapters remain on participant-controlled machines. Different reported outcomes do not establish relative architecture superiority, real consequence protection, or native V.A. behavior.

## Freeze-after-commit external examination

[Independent-examiner signed challenge](INDEPENDENT-CHALLENGE.md) creates a source-frozen candidate fingerprint, a **fresh examiner-issued seed**, reproducible locally observed synthetic output, and independently signed records from distinct declared examiners. It rejects altered signatures, unsupported standing, changed source bytes and mismatched challenge identities. Two signing keys do **not** authenticate two independent people or external consequences; examiners must separately establish original witness custody. Submit only release-cleared records through the [external examiner issue form](https://github.com/DeagleTWC/va-proof-estate/issues/new?template=external-independent-examination.md).
