#!/usr/bin/env python3
"""Offline pilot-source role and SHA-256 audit. NEVER proves outcomes or publishes private carriers."""
import argparse
import hashlib
import json
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "va-private-multi-pilot-audit/1.0"
OUTSCHEMA = "va-private-pilot-source-audit-report/1.0"
ID = re.compile(r"^PILOT-LOCAL-[A-Z0-9-]{2,80}$")
HEX = re.compile(r"^[0-9a-f]{64}$")
ROLES = {
    "PILOT_SCOPE_OR_SPEC", "ORIGINAL_FREEZE", "BUILD_VERIFICATION_REPORT",
    "LIVE_RUN_RESULT", "BOUNDARY_RECEIPT", "REPLAY_RECORD",
    "CHANGED_CONDITION", "NEGATIVE_CONTROL", "ACCEPTANCE_DECISION", "INDEPENDENT_REVIEW",
}
STAGES = {
    "SOURCE_INVENTORIED": set(),
    "BUILD_VERIFICATION_PACKET_PRESENT": {"ORIGINAL_FREEZE", "BUILD_VERIFICATION_REPORT"},
    "LIVE_RUN_PACKET_PRESENT": {"PILOT_SCOPE_OR_SPEC", "LIVE_RUN_RESULT", "BOUNDARY_RECEIPT", "REPLAY_RECORD"},
    "ACCEPTANCE_PACKET_PRESENT": {"PILOT_SCOPE_OR_SPEC", "LIVE_RUN_RESULT", "BOUNDARY_RECEIPT", "REPLAY_RECORD",
                                  "ACCEPTANCE_DECISION"},
    "INDEPENDENT_PACKET_PRESENT": {"PILOT_SCOPE_OR_SPEC", "LIVE_RUN_RESULT", "BOUNDARY_RECEIPT", "REPLAY_RECORD",
                                   "ACCEPTANCE_DECISION", "CHANGED_CONDITION", "NEGATIVE_CONTROL"},
}
BLOCK = 1024 * 1024


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def digest_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(BLOCK), b""):
            h.update(chunk)
    return h.hexdigest()


def checked_file(root, relative, digest):
    require(isinstance(relative, str) and relative and "\\" not in relative, "Nonportable/empty source path")
    rel = Path(relative)
    require(not rel.is_absolute() and ".." not in rel.parts and rel.as_posix() == relative,
            "Source path must remain an exact normalized relative path")
    root = root.resolve()
    candidate = root
    for bit in rel.parts:
        candidate /= bit
        require(not candidate.is_symlink(), "Symlinked source path refused")
    path = candidate.resolve()
    require(path.is_relative_to(root), "Source path escapes selected root")
    require(path.is_file() and stat.S_ISREG(path.stat().st_mode), "Original evidence file unavailable")
    require(isinstance(digest, str) and HEX.fullmatch(digest), "Invalid expected source SHA-256")
    before = path.stat()
    measured = digest_file(path)
    after = path.stat()
    require((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns),
            "Original source changed during audit")
    require(measured == digest, "Original source file SHA-256 mismatch")
    return measured


def check_private_manifest(data, root):
    require(isinstance(data, dict) and data.get("schema") == SCHEMA, "Wrong audit manifest schema")
    require(data.get("classification") == "PRIVATE_LOCAL_SOURCE_REVIEW_DO_NOT_PUBLISH",
            "Missing private source custody label")
    require(data.get("releaseApproval") is False, "Public release status cannot be set in this private auditor")
    pilots = data.get("pilots")
    require(isinstance(pilots, list) and pilots, "No individual pilot lanes supplied")
    names, result = set(), []
    for lane in pilots:
        require(isinstance(lane, dict), "Each pilot must have its own lane")
        name = lane.get("localId")
        require(isinstance(name, str) and ID.fullmatch(name) and name not in names,
                "Duplicate or invalid local pilot lane ID")
        names.add(name)
        require(lane.get("sourceType") == "HISTORICAL_PILOT_OR_FREEZE", "Invalid source type")
        stage = lane.get("claimedStage")
        require(stage in STAGES, "Unrecognized evidence source stage")
        files = lane.get("artifacts")
        require(isinstance(files, list) and len(files) > 0 and len(files) <= 100,
                "Pilot must declare 1–100 original artifact references")
        roles, paths, review_ids = [], set(), set()
        for art in files:
            require(isinstance(art, dict) and art.get("role") in ROLES, "Unknown evidence role")
            role, path = art["role"], art.get("path")
            require(isinstance(path, str) and path not in paths, "Duplicate/incomplete source path")
            paths.add(path)
            checked_file(root, path, art.get("sha256"))
            roles.append(role)
            if role == "INDEPENDENT_REVIEW":
                reviewer = art.get("reviewerId")
                require(isinstance(reviewer, str) and reviewer.strip() and reviewer not in review_ids,
                        "Incomplete or duplicate declared reviewer identity")
                review_ids.add(reviewer)
            else:
                require(art.get("reviewerId") in (None, ""), "Reviewer metadata attached to wrong source role")
        present = set(roles)
        required = STAGES[stage]
        require(required.issubset(present), "Claimed evidence stage lacks source roles: " + stage)
        if stage == "INDEPENDENT_PACKET_PRESENT":
            require(len(review_ids) >= 2, "Two separately declared review packets required")
        # A stronger stage requires a full corresponding source packet, not a proposal label.
        result.append({
            "localId": name,
            "declaredPacketStage": stage,
            "sourceFilesFingerprintMatched": len(files),
            "sourceRoleClassesPresent": sorted(present),
            "missingForLiveRunPacket": sorted(STAGES["LIVE_RUN_PACKET_PRESENT"] - present),
            "roleAssignmentIsUnverified": True,
            "independentHumanIdentityIsUnverified": True,
            "actualConsequenceOutcomeIsUnverified": True,
            "publicationAuthorized": False,
        })
    return sorted(result, key=lambda x: x["localId"])


def write_exclusive(output, payload):
    path = Path(output).absolute()
    require(not path.exists() and not path.is_symlink(), "Private audit result already exists; will not overwrite")
    require(path.parent.is_dir(), "Output folder does not exist")
    text = (json.dumps(payload, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
    except BaseException:
        try:
            path.unlink()
        except OSError:
            pass
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit", choices=["audit"])
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        require(root.is_dir() and not args.root.is_symlink(), "Selected private original root is missing or symbolic")
        # Private manifest and generated report must not be placed in original-source directory.
        require(not args.out.absolute().resolve().is_relative_to(root), "Private report must be outside original-source root")
        require(not args.manifest.absolute().resolve().is_relative_to(root), "Private intake manifest must be outside original-source root")
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        lanes = check_private_manifest(data, root)
        report = {
            "schema": OUTSCHEMA,
            "classification": "PRIVATE_LOCAL_SOURCE_REVIEW_DO_NOT_PUBLISH",
            "generatedAtUTC": datetime.now(timezone.utc).isoformat(),
            "notOriginalFreezeDate": True,
            "noRealWorldOutcomeOrIndependentStatusAssigned": True,
            "publicationAuthorization": "NONE_BY_THIS_TOOL",
            "numberOfLocallyReviewedLanesNotTotalPilots": len(lanes),
            "lanes": lanes,
            "notice": "Exact source hashes matched local bytes under declared roles; source truth, dates, claims, reviewer identities, actual consequence and release rights still need human custody examination. Do not publish this PRIVATE report.",
        }
        write_exclusive(args.out, report)
        print("PASS: private source file fingerprints checked for", len(lanes), "separate local lanes")
        print("PRIVATE report written. No pilot passed, witness verified or publication authorized by this tool.")
    except (ValueError, KeyError, TypeError, FileNotFoundError, OSError, json.JSONDecodeError) as exc:
        parser.exit(2, "REFUSED: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
