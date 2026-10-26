# Milestone 27 — Protected-target readback qualifier hardening (v1.1)

**Review checkpoint:** 2026-10-26  
**Class:** Public-safe, local engineering verification record  
**Consequence standing:** **HOLD** — no new native V.A. external-effect measurement or authenticated independent witness admitted  
**M28 status:** NOT OPEN

## Reproduced v1.0 qualification defects

An examination of the previously published M27 v1.0 source-record preflight identified two concrete consistency defects. Both were demonstrated using synthetic inputs; neither demonstration was a native system run.

1. **Refused case starting after effect formation:** v1.0 accepted a REFUSE case whose protected target read `1 → 1`. Unchanged bytes were not sufficient to establish protected **non-effect** because the prohibited effect was already present before the refused attempt. The originally published synthetic fixture used this configuration and passed its local consistency checks.
2. **Metadata-only change mistaken for protected effect:** after recomputing legitimate fixture hashes, v1.0 accepted an ALLOW case with raw before/after captures differing only in a timestamp and reporting the same `protected_effect: false` state. Its reported `permittedReadbackChanged: true` meant changed **raw container bytes**, not changed protected state.

The earlier v1.0 result was always bounded as `SOURCE_RECORDS_INTERNALLY_CONSISTENT_HUMAN_QUALIFICATION_PENDING`, with M27 completion and independent external proof set false. The defects therefore concerned *qualification of claimed internal state differences*, **not** automatic public standing promotion.

## v1.1 correction, with prior history preserved

The public checker, local synthetic tests and examiner guide were revised at their existing paths, with original v1.0 bytes preserved through repository history. v1.1 explicitly refuses v1.0 schema inputs rather than silently promoting them.

- A single named protected-state observable must define baseline and permitted-effect values before the paired examination.
- **Both** ALLOW and REFUSE target observations must begin at that baseline.
- ALLOW must end at the declared permitted-effect state; REFUSE must remain at baseline.
- Each capture is hash-bound and supplies a uniquely identified acquisition, source case/route/target/instrument, acquisition sequence, observable identity and typed observed-state value. Raw capture file metadata variations are not interpreted as a protected effect.
- Manifest, decision receipt, snapshot, original-source hash and uncovered routes remain explicitly bound; no instrument, human qualification, disclosure right or native lineage is authenticated by a JSON value.

## Verification and scope

**Local synthetic suite:** `28/28 PASS` on 2026-10-26. This includes the original negative controls, already-effected refused baseline, metadata-only allowed false positive, wrong measured observable, target substitution, capture-ID reuse, acquisition mismatch, unexpected effect value and schema downgrade. The corrected records were subsequently fetched from the estate and compared byte-for-byte with tested local sources.

| Public artifact | Local SHA-256 of v1.1 bytes |
| --- | --- |
| `scripts/preflight_m27_target_readback.py` | `8c0c5e546931a4adf6adb107710e09c080687fb206b58981cca9b65a144fa7e3` |
| `scripts/test_preflight_m27_target_readback.py` | `f27464c5defcebaf3dc67a188c7169b0e2dab28ef4f63688cb9a38323ed88cfa` |
| `proofs/M27-TARGET-READBACK-PREFLIGHT.md` | `9cf55e361604ae509a3b24a4bd2df498feb4dc571b1f3cd15f749d495b01700d` |

No private pilot archive, original receipt, customer-identifying data, corrected-K construction, native source, protected instrument trace or credential was published in this correction.

## Remaining qualification / next admissible action

M27 still requires authentic, separately acquired before/after protected-target measurements for an authorized frozen native route, with defensible source custody, positive and negative controls, instrument provenance, independent examiner identification, actual route coverage, exact-source hashes and an approved safe extract. A device-produced normalized capture envelope requires human verification against its **unaltered underlying instrument original**; the format cannot authenticate itself. The public-interest seven-gate release charter controls any original evidence publication. Until qualified permitted effect and refused non-effect are available, M27 is **HOLD** and M28 is **not open**.
