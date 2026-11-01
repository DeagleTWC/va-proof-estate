#!/usr/bin/env python3
"""Public V.A. proof-estate documentation integrity; NOT a NEW-K runtime proof."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = "milestones/M33-EVIDENCE-CONTINUITY.json"
VALID_STANDINGS = {"DECLARED", "OBSERVED", "INDEPENDENTLY REPRODUCED"}


def validate(root=ROOT):
    root = Path(root).resolve()
    errors = []

    def load(relative):
        try:
            return json.loads((root / relative).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"Unreadable/invalid JSON {relative}: {exc}")
            return {}

    def carrier(base, relative, context):
        if not isinstance(relative, str) or not relative or "\\" in relative or "://" in relative:
            errors.append(f"Invalid carrier for {context}: {relative!r}")
            return
        target = (root / base / relative).resolve()
        if not target.is_relative_to(root):
            errors.append(f"Carrier path escapes repository for {context}: {relative}")
        elif not target.is_file():
            errors.append(f"Missing linked carrier for {context}: {relative}")
        elif (root / base / relative).is_symlink():
            errors.append(f"Symlinked carrier disallowed for {context}: {relative}")

    data = load(INDEX_PATH)
    entries = data.get("progression", [])
    if not isinstance(entries, list) or [x.get("id") for x in entries if isinstance(x, dict)] != [
        f"M{i}" for i in range(27, 36)
    ]:
        errors.append("Expected distinct historical/support index entries M27–M35")
        entries = []
    for row in entries:
        milestone = row["id"]
        source = row.get("path") or row.get("record")
        carrier("milestones", source, milestone)
        if milestone in {"M27", "M28"}:
            if row.get("classification") != "dated_scientific_cycle_control":
                errors.append(f"{milestone} scientific control wrongly categorized")
        elif milestone == "M29":
            if row.get("classification") != "secondary_continuity_reference":
                errors.append("M29 secondary historical reference misrepresented")
        elif row.get("classification") != "publication_support_not_empirical_result":
            errors.append(f"{milestone} publication work promoted as empirical proof")

    for row in data.get("carriers", []):
        if not isinstance(row, dict):
            errors.append("Malformed carrier entry")
            continue
        carrier("milestones", row.get("path"), row.get("role"))

    policy = data.get("evidence_policy", {})
    for key in ("preserve_original_classification", "do_not_infer_independent_reproduction",
                "do_not_invent_hold", "distinguish_historical_record_from_public_attachment",
                "no_scientific_completion_inferred_from_publication_milestone",
                "no_privileged_instructions_or_disclosures"):
        if policy.get(key) is not True:
            errors.append(f"Evidence-continuity safeguard not enabled: {key}")
    if data.get("foundation", {}).get("invariant") != "The face may vary. The floor must not.":
        errors.append("Computational lineage invariant changed")
    if data.get("history", {}).get("formalization") != "recorded_completed":
        errors.append("Completed formalization record changed")
    if data.get("history", {}).get("external_pilots") != "historical_external_pilots_recorded":
        errors.append("Historical external pilot record changed")
    if data.get("last_published_support_milestone") != "M35":
        errors.append("Publication support index has stale terminal record")

    bot = load("milestones/DEAGLE-TRUE-ZERO-BOT-CONTINUITY.json")
    c = bot.get("continuity", {})
    if "M35" not in c.get("current", "") or c.get("next_on_request", "unexpected") is not None:
        errors.append("Bot continuity snapshot is stale or asserts automatic next milestone")
    if bot.get("project", {}).get("invariant") != data.get("foundation", {}).get("invariant"):
        errors.append("Cross-bot handoff changed the foundation invariant")

    manifest = load("proof-estate-manifest.json")
    register = load("proofs/CLAIM-TO-CARRIER.json")
    rows = register.get("entries", [])
    if not isinstance(rows, list):
        errors.append("Invalid claim-to-carrier entries")
        rows = []
    if len(rows) != manifest.get("expandedRegister", {}).get("count"):
        errors.append("Manifest claim count differs from claim register")
    counts = Counter(x.get("standing") for x in rows if isinstance(x, dict))
    if not set(counts).issubset(VALID_STANDINGS):
        errors.append("Unexpected claim evidence classification")
    if counts.get("DECLARED", 0) != manifest.get("expandedRegister", {}).get("standing", {}).get("DECLARED"):
        errors.append("Manifest DECLARED count differs from register")
    if sum(x.get("nativeVAEvidence") is True for x in rows if isinstance(x, dict)) != 0 and (
        register.get("nativeRuntimeReceiptsAttached", 0) == 0
    ):
        errors.append("Native evidence marked present without declared native receipt")
    if register.get("nativeRuntimeReceiptsAttached") != manifest.get("nativeRuntimeReceiptsAttached"):
        errors.append("Native receipt count differs between public registers")
    if "INDEPENDENTLY REPRODUCED" not in manifest.get("evidenceStatusVocabulary", []):
        errors.append("Public evidence vocabulary incomplete")

    home = (root / "index.html")
    try:
        html = home.read_text(encoding="utf-8")
        for expected in ("id=\"evidence-continuity\"", "milestones/M33-EVIDENCE-CONTINUITY.json",
                         "proofs/HISTORICAL-PILOT-CARRIER-CROSSWALK.md"):
            if expected not in html:
                errors.append(f"Homepage lacks public evidence navigation: {expected}")
    except OSError as exc:
        errors.append(f"Cannot inspect public homepage: {exc}")
    try:
        readme = (root / "README.md").read_text(encoding="utf-8")
        if "Current scientific sequence:** **M27 HOLD; M28 not opened." in readme:
            errors.append("README retains contradictory outdated project-wide HOLD statement")
        if "milestones/M36-CORRECTION" in readme:
            errors.append("README links unauthorized M36 material")
    except OSError as exc:
        errors.append(f"Cannot inspect README: {exc}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for p in problems:
            print("FAIL:", p)
        raise SystemExit(1)
    print("PASS: public continuity references, publication/proof distinctions, evidence classifications, site routes")
    print("NOTE: this checks metadata and links only—not native True Zero / corrected NEW-K execution.")
