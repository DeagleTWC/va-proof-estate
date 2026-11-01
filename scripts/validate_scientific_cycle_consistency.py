#!/usr/bin/env python3
"""Check dated scientific-cycle continuity is not silently replaced by old status flags.

This is document-control verification only; never certifies a native scientific result.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    root = Path(root)
    errors = []

    def read(path):
        try:
            return (root / path).read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"Missing source {path}: {exc}")
            return ""

    def load(path):
        try:
            return json.loads(read(path))
        except (ValueError, TypeError) as exc:
            errors.append(f"Invalid JSON {path}: {exc}")
            return {}

    cycle = load("proofs/SCIENTIFIC-CYCLE-CURRENT.json")
    record = cycle.get("authoritativeCurrentCycle", {})
    if record.get("priorCycleTransition") != "CHAT_CHANGE_PAUSE_CLEARED_AND_HANDOFF_RELEASED":
        errors.append("M27 administrative handoff closure missing from dated control")
    if record.get("currentCycle") != "M28" or record.get("currentCycleState") != "OPEN_FOR_ACTIVE_SCIENTIFIC_WORK":
        errors.append("October 28 dated scientific-control source altered")
    if record.get("M28ScientificResultCertifiedByThisRecord") is not False:
        errors.append("Dated M28 opening incorrectly promoted to certified scientific result")

    dated = cycle.get("datedSnapshotInterpretation", {})
    if dated.get("controlDate") != "2026-10-28" or dated.get("latestScientificStageDeterminedByThisFile") is not False:
        errors.append("Dated October 28 control wrongly presented as current-stage evidence")
    if dated.get("doNotResetLaterRecordedProgression") is not True or dated.get("noAutomaticHold") is not True:
        errors.append("Later scientific work is not protected against dated-snapshot reset")
    snapshot = load("proofs/VA-ORIGINAL-CAPABILITY-RECOVERY.json")
    if snapshot.get("historicalSnapshotAsOfDate") != "2026-10-26":
        errors.append("Historical source inventory date missing")
    if (snapshot.get("historicalScientificM27"), snapshot.get("historicalScientificM28")) != ("HOLD", "NOT_OPEN"):
        errors.append("Dated source inventory status was rewritten")
    if snapshot.get("notCurrentCycleStatus") is not True or (
        snapshot.get("currentCycleSource") != "proofs/SCIENTIFIC-CYCLE-CURRENT.json"
    ):
        errors.append("Historical source inventory not distinguished from current cycle")
    if "scientificM27" in snapshot or "scientificM28" in snapshot:
        errors.append("Ambiguous unscoped current-cycle flags reintroduced into historical snapshot")

    for path in ("README.md", "proofs/README.md", "proofs/VA-ORIGINAL-CAPABILITY-RECOVERY.md"):
        content = read(path)
        if "M27 HOLD; M28 NOT OPEN" in content or "Scientific M27 HOLD; M28 not open." in content:
            errors.append(f"Misleading active scientific HOLD in {path}")
        if "SCIENTIFIC-CYCLE-CURRENT.json" not in content:
            errors.append(f"Missing governing dated cycle link in {path}")

    workflow = read(".github/workflows/public-proof-integrity.yml")
    if '"M28Authorized":false' in workflow or '"M27Completed":false' in workflow:
        errors.append("CI artifact still emits ambiguous unscoped scientific-cycle flags")
    if '"M28AuthorizedByThisCI":false' not in workflow or (
        '"recordType":"PUBLIC_CI_OBSERVATION_NOT_SCIENTIFIC_CYCLE_CONTROL"' not in workflow
    ):
        errors.append("CI artifact is not explicitly scoped to CI-only authority")

    index = load("milestones/M33-EVIDENCE-CONTINUITY.json")
    rows = index.get("progression", [])
    for row in rows:
        if row.get("id") in {"M30", "M31", "M32", "M33", "M34", "M35"} and (
            row.get("classification") != "publication_support_not_empirical_result"
        ):
            errors.append(f"{row['id']} publication activity promoted without empirical carrier")
    timeline = index.get("datedScientificReconciliation", {})
    later = timeline.get("laterM29", {})
    if timeline.get("snapshotAsOf") != "2026-10-28" or later.get("status") != "LATER_PROGRESS_REPORTED":
        errors.append("M28 dated snapshot and M29 later continuity no longer reconciled")
    if timeline.get("noResetOfLaterWork") is not True or timeline.get("noNewCertification") is not True:
        errors.append("M29 progression incorrectly reset or elevated to new proof")
    if later.get("nativeResultCarrierAttachedByThisIndex") is not False:
        errors.append("Secondary M29 reference incorrectly promoted to native evidence")
    if not any(row.get("id") == "M29" and row.get("classification") == "secondary_continuity_reference" for row in rows):
        errors.append("M29 later secondary reference missing or reclassified")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print("SCIENCE-CONTINUITY ERROR:", problem)
        raise SystemExit(1)
    print("PASS: dated scientific cycle, public support status and historical snapshot are separated")
