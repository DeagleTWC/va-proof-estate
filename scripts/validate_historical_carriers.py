#!/usr/bin/env python3
"""Public historical-carrier integrity preflight. Never assigns factual proof standing."""
import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID_PATTERN = re.compile(r"^HIST-[A-Z0-9][A-Z0-9-]{2,63}$")
DIGEST = re.compile(r"^[a-f0-9]{64}$")
ALLOWED_SOURCE = {"PILOT", "FREEZE", "ENGINEERING_LAYER"}
ALLOWED_STANDING = {
    "SOURCE_RECORDED",
    "PUBLIC_BOUNDED_OBSERVATION",
    "PUBLIC_INDEPENDENT_REPRODUCTION",
}
REQUIRED_ENTRY_FIELDS = {
    "schema", "id", "sourceKind", "original", "publication",
    "evidence", "independent", "protectedOriginalRemainsPrivate",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value, field):
    require(isinstance(value, str) and value.strip() and len(value) <= 1200,
            "Missing or invalid " + field)


def digest(value, field):
    require(isinstance(value, str) and DIGEST.fullmatch(value) is not None,
            "Missing or malformed SHA-256 for " + field)


def date_value(value, field):
    nonempty(value, field)
    require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is not None,
            "Date must be YYYY-MM-DD: " + field)
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Invalid calendar date: " + field) from exc


def safe_file(root, rel, expected, field):
    nonempty(rel, field)
    require(rel.startswith("proofs/historical/carriers/"), "Carrier path outside approved public area: " + field)
    pure = Path(rel)
    require(not pure.is_absolute() and ".." not in pure.parts, "Unsafe carrier path: " + field)
    path = (root / pure).resolve()
    require(path.is_relative_to(root.resolve()), "Carrier escapes root: " + field)
    require(path.is_file(), "Public evidence bytes not attached: " + field)
    digest(expected, field + " SHA-256")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    require(actual == expected, "Altered/mismatching public bytes: " + field)


def validate_entry(entry, root):
    require(isinstance(entry, dict), "Entry must be an object")
    require(REQUIRED_ENTRY_FIELDS.issubset(entry), "Incomplete historical carrier entry")
    require(entry["schema"] == "va-historical-carrier-entry/1.0", "Wrong entry schema")
    identifier = entry["id"]
    require(isinstance(identifier, str) and ID_PATTERN.fullmatch(identifier) is not None,
            "Invalid historical public ID")
    require(entry["sourceKind"] in ALLOWED_SOURCE, "Invalid source kind")
    require(entry["protectedOriginalRemainsPrivate"] is True, "Protected original disclosure guard missing")

    original = entry["original"]
    for field in ("sourceDesignation", "originalArtifactId", "originalCustodian"):
        nonempty(original.get(field), "original." + field)
    historical_date = date_value(original.get("originalFreezeDate"), "original.originalFreezeDate")
    digest(original.get("originalSHA256"), "original.originalSHA256")
    if entry["sourceKind"] == "PILOT":
        nonempty(original.get("originalPilotOrRunId"), "original.originalPilotOrRunId")

    publication = entry["publication"]
    for field in ("releaseAuthorizationId", "releaseClearedBy", "authorizedScope"):
        nonempty(publication.get(field), "publication." + field)
    release_date = date_value(publication.get("extractPreparedDate"), "publication.extractPreparedDate")
    require(historical_date <= release_date, "Public extract cannot predate unchanged original freeze")
    prefix = "proofs/historical/carriers/" + identifier + "/"
    require(isinstance(publication.get("publicExtractPath"), str) and
            publication["publicExtractPath"].startswith(prefix),
            "Public extract must be isolated under its historical release ID")
    safe_file(root, publication["publicExtractPath"], publication.get("publicExtractSHA256"),
              "publication.publicExtractPath")

    evidence = entry["evidence"]
    status = evidence.get("standing")
    require(status in ALLOWED_STANDING, "Unsupported historic evidence status")
    for field in ("boundedClaim", "conditionScope", "routeCoverageLimits"):
        nonempty(evidence.get(field), "evidence." + field)
    attachments = [
        ("observationFile", "observationSHA256"),
        ("negativeControlFile", "negativeControlSHA256"),
        ("replayFile", "replaySHA256"),
    ]
    if status != "SOURCE_RECORDED":
        for field in ("positiveObservation", "negativeObservation", "changedCondition", "receiptReplay"):
            nonempty(evidence.get(field), "evidence." + field)
        for pathkey, hashkey in attachments:
            require(isinstance(evidence.get(pathkey), str) and
                    evidence[pathkey].startswith(prefix), "Missing approved observation path: " + pathkey)
            safe_file(root, evidence[pathkey], evidence.get(hashkey), "evidence." + pathkey)
    else:
        # Source-only publication cannot quietly carry an observed/implied promotion.
        for field in ("positiveObservation", "negativeObservation", "changedCondition", "receiptReplay"):
            require(evidence.get(field) is None, "Unadmitted observation in source-only entry: " + field)
        for pathkey, hashkey in attachments:
            require(evidence.get(pathkey) is None and evidence.get(hashkey) is None,
                    "Source-only record contains observed-result attachment: " + pathkey)

    independent = entry["independent"]
    reviewers = independent.get("reviewerPackets")
    require(isinstance(reviewers, list), "Invalid independent reviewer packet list")
    if status == "PUBLIC_INDEPENDENT_REPRODUCTION":
        nonempty(independent.get("independenceReviewId"), "independent.independenceReviewId")
        require(len(reviewers) >= 2, "Independent publication requires at least two real attributed reviewer packets")
        people = []
        for i, reviewer in enumerate(reviewers):
            nonempty(reviewer.get("reviewerIdentity"), f"independent.reviewerPackets[{i}].reviewerIdentity")
            nonempty(reviewer.get("originalCustodyReference"), f"independent.reviewerPackets[{i}].originalCustodyReference")
            safe_file(root, reviewer.get("publicPacketPath"), reviewer.get("publicPacketSHA256"),
                      f"independent.reviewerPackets[{i}].publicPacketPath")
            people.append(reviewer["reviewerIdentity"].casefold())
        require(len(set(people)) == len(people), "Duplicated declared reviewer identity")
    else:
        require(not reviewers and independent.get("independenceReviewId") is None,
                "Unadmitted independent review present in lower-status entry")
    return identifier


def validate_register(root):
    reg_path = root / "proofs/historical/PUBLIC-CARRIER-REGISTER.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    require(reg["schema"] == "va-historical-public-carriers/1.0", "Invalid public historical register")
    require(reg.get("publication") == "DeagleTWC/va-proof-estate", "Unexpected publication owner")
    require(reg.get("standingVocabulary") ==
            ["SOURCE_RECORDED", "PUBLIC_BOUNDED_OBSERVATION", "PUBLIC_INDEPENDENT_REPRODUCTION"],
            "Evidence classes modified")
    entries = reg.get("entries")
    require(isinstance(entries, list), "Historical entries must be a list")
    ids = [validate_entry(e, root) for e in entries]
    require(len(ids) == len(set(ids)), "Duplicate original carrier release ID")
    require("not a finding" in reg["distinctions"]["preExistingRecord"].lower() or
            "not a count" in reg["distinctions"]["preExistingRecord"].lower(),
            "Historical existence/public attachment separation lost")
    index = (root / "proofs/HISTORICAL-EVIDENCE-INDEX.md").read_text(encoding="utf-8")
    require("historical" in index.lower() and "freeze" in index.lower(), "Historical lineage index missing")
    print(f"PASS: {len(entries)} release-cleared public historic carriers indexed")
    print("PASS: metadata, byte integrity, custody and non-inheritance gates (not operational verification)")
    return ids


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, help="Local source entry to preflight before release")
    parser.add_argument("--root", type=Path, default=ROOT, help="Root of public-safe staging tree or repo")
    args = parser.parse_args()
    if args.candidate:
        data = json.loads(args.candidate.read_text(encoding="utf-8"))
        identity = validate_entry(data, args.root)
        print("PREFLIGHT PASS:", identity, "(byte and release-field checks only; no proof standing assigned)")
    else:
        validate_register(args.root)


if __name__ == "__main__":
    main()
