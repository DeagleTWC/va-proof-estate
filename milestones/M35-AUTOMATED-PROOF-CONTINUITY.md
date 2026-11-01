# M35 — Automated Proof Estate Continuity

**Date:** 2026-11-01  
**Status:** CI workflow committed; execution results remain specific to the code version and GitHub Actions run  
**HOLD:** None

M35 connects the [M34 public continuity validator](../scripts/validate_m34_continuity.py) to [GitHub Actions](../.github/workflows/m35-continuity.yml). The workflow runs on changes to milestone records, proof carriers, examiner files, or the validator, as well as manual dispatch.

The check guards the updated historical/publication evidence-continuity index, link targets, completed-formalization record, historical external-pilot references, and the computational invariant. A CI failure signals a documentation/integrity issue; it does **not** automatically negate prior scientific results or impose a new scientific HOLD.

This workflow does not perform native True Zero / corrected NEW-K execution or independently certify external pilots. It preserves evidence classes and private construction.

**Scope:** Publication-support automation only; it does not certify new scientific milestones or approve publication of conversation records.  
**Invariant:** The face may vary. The floor must not.
