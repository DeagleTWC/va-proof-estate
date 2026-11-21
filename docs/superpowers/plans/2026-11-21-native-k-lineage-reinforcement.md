# Native NEW K Source-Lineage Reinforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent current hub material from regressing to old-K language or silently importing byte-identical public reference modules as native V.A.

**Architecture:** A read-only Python provenance validator and its negative-control tests; a public-safe evidence note; one CI step. Preserve original archive and research content.

**Tech Stack:** Python 3.11 standard library, GitHub Actions YAML.

**Spec:** `docs/superpowers/specs/2026-11-21-native-k-lineage-reinforcement-design.md`

## Global Constraints

- Corrected NEW K / True Zero / URK are the current foundation.
- Existing historical math/source artifacts remain unchanged, including older formulations.
- Kamanaka originals remain externally attributed and are not copied or redistributed.
- Private Library originals and native executable operators never enter GitHub.
- The validator attests only public-source identity and policy consistency, not native execution.

## Review Focus

- A current site page says old K is operative: reject.
- A matching R19/Kamanaka Python module is added: reject.
- A mapped outside source claims native V.A. execution: reject.
- An unrelated/new local Python module is added: allow.
- Historical mathematics are not treated as current runtime or rewritten.

## Task 1: Local native-lineage validation

**Files:** Create `scripts/test_validate_native_source_lineage.py`; `scripts/validate_native_source_lineage.py`.

**Interfaces:** `validate(root: Path, reference_fingerprints: frozenset[str] | None = None) -> dict[str, int]`; `git_blob_sha1(content: bytes) -> str`.

- [ ] Write unittest negative controls for old-K substitution, exact-source-module reintroduction, false native source promotion, and allowed unrelated source.
- [ ] Run the tests to observe expected import/feature failures.
- [ ] Implement minimal standard-library validator checking current pages, manifesto, source register, and six pinned source fingerprints.
- [ ] Run targeted tests and complete existing foundation/attribution validators.

## Task 2: Evidence trace and CI

**Files:** Create `proofs/NATIVE-NEW-K-LINEAGE-REINFORCEMENT.md`; modify `.github/workflows/public-proof-integrity.yml`.

**Interfaces:** CI runs `python scripts/validate_native_source_lineage.py` then `python -m unittest discover -s scripts -p 'test_validate_native_source_lineage.py' -v`.

- [ ] Add a bounded 2026-11-21 source attribution record with six matched blob SHA-1 values and no personal blame, direction or native-proof assertion.
- [ ] Wire the validator into existing main/PR proof-integrity job.
- [ ] Re-run targeted test and existing attribution/foundation tests; check diff and commit only scoped files.
