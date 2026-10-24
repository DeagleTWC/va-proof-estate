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

## Evidence ceiling: important

**What this actually shows:** a supplied adapter returned suitable decisions and requested simulated effects for these six declared packets. The examiner generated deterministic local results.

**What this does not show:** no native V.A. execution; no real payment; no alternate-route closure outside the modeled routes; no physical apparatus, sensor, actuator, or measured non-formation; no production certification; no independent third-party reproduction; and no validation of the truth of the adapter's private internals.

A real-world claim requires a fixed artifact, complete consequence-bearing route, independent effect measurement, changed-condition and negative controls, retained receipts, replay, and an independent reviewer where applicable. **A self-reported REFUSE is not by itself proof of non-formation.** Report any actual bypass with an exact artifact version, input, effect observation, receipt and reproduction procedure.

## Bring your own implementation, not our IP

Participants can keep their work private and run this locally. Publish only a release-cleared adapter, bounded results and reproducible challenge packet, if desired. No secret, customer data, private substrate, private mechanical drawings, proprietary mathematics, executable actuator access, or sensitive enterprise infrastructure is requested.

**Review path:** [Examination standard](../proofs/EXAMINATION-STANDARD.md) | [Fixed-carrier issue intake](https://github.com/DeagleTWC/va-proof-estate/issues/new?template=bounded-proof-review.md) | [Physical witness requirements](PHYSICAL-WITNESS.md).

**The public Proof Estate is a curated present examination surface, not the whole underlying scientific, engineering, pilot or historical record.**
