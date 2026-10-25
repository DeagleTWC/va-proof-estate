# Measurement Coverage Worksheet — Public Examiner Blank

**Purpose:** A release-safe checklist for establishing whether an observed bounded result can be attributed to an identified system under declared conditions, including a refusal/non-effect. **Completing this form is not proof.** Original instrumentation, logs and independent custody are required. This form must not contain proprietary construction, private corrected-K operators, customer data, credentials or private signing keys.

## A. Identity and scope

| Field | Record / source reference |
| --- | --- |
| Bounded claim ID and precise observable proposition | |
| Native V.A., KCD Program A, other physical, or synthetic-only track | |
| Source file/revision, hash algorithm, digest and custodian | |
| Frozen build/apparatus identifier and authorized release scope | |
| Candidate action and claimed permitted or prohibited consequence | |
| Declared accessible environment, boundary and excluded routes | |
| Distinct observation operator(s) and reviewer role(s) | |

## B. Measurement chain

| Requirement | Instrument/source, calibration evidence, uncertainty or explicit gap |
| --- | --- |
| Directly observable effect **and** intended non-effect | |
| Detector/sensor identity, independent chain and raw carrier | |
| Sensor coverage: locations, regions and relevant field classes | |
| Calibration reference, baseline, noise floor and drift | |
| Resolution, sampling and event-order correlation | |
| Uncertainty bound and threshold justified before examination | |
| Detector blind spots, saturation, masking and fail-open behavior | |
| Alternate pathways and bypass influence inventory | |
| Custody of exact original measurement bytes and digests | |

## C. Changed-condition series

| Case | Frozen material condition | Intended result | Observed result | Raw carrier hash | Excluded/bypassed route checked |
| --- | --- | --- | --- | --- | --- |
| Baseline present-standing condition | | | | | |
| Material standing removed/revoked | | | | | |
| Substituted/replayed input or candidate | | | | | |
| Alternate reachable route attempted | | | | | |
| Explicit negative control | | | | | |
| Same-condition replay | | | | | |

## D. Independent examination and disposition

Record the second examiner's independently attributable identity, authorization, distinct measurement path/environment, original data custody, exact reproducible procedure, signed report/public key, discrepancies and preserved failed trials. Record any material uncertainty not bounded by the measurement chain.

**Disposition choices:** `INSUFFICIENT_CARRIER`; `METADATA_ONLY`; `SYNTHETIC_LOCAL_ONLY`; `OBSERVED_BOUNDED`; `INDEPENDENTLY_REPRODUCED_BOUNDED`; `REFUTED_OR_CONTRADICTED`.

The higher two statuses require **real effect-bearing original carriers**. Neither a complete form, an adapter pass, nor signatures alone qualifies. No reviewer should equate an unmeasured refusal decision with independently measured prevention of all possible consequences.

## E. Publication control

Before release verify the custodian's approval, redaction without loss of event identity, independent original retention, non-disclosure of protected implementation, and accurate claim ceiling. Link exact public carriers only after these checks.

Related: [Evidence dependency map](EVIDENCE-DEPENDENCIES.md) · [Milestone ledger](MILESTONE-LEDGER.md) · [Examination standard](EXAMINATION-STANDARD.md).
