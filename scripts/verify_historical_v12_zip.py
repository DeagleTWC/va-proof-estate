#!/usr/bin/env python3
"""Read-only V1.2 engineering proof ZIP integrity verifier. Does not execute archived code."""
import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import PurePosixPath
from zipfile import ZipFile, BadZipFile

MAX_FILES = 120
MAX_MEMBER = 2_000_000
MAX_TOTAL = 10_000_000
HEX = re.compile(r"^[a-f0-9]{64}$")
HASHED_FILES = {
    "corridor_registry_hash": "corridor_registry.json",
    "policy_registry_hash": "policy_registry.json",
    "hash_fixture_set": "fixtures/fixture_set_v1.json",
    "hash_boundary_results": "outputs/boundary_results.json",
    "hash_receipt_chain": "outputs/enforcement_receipts.json",
    "hash_replay_results": "outputs/replay_records.json",
    "hash_verification_report": "reports/V1_2_certificate_verification_report.json",
    "hash_verify_package_script": "verify_package.py",
    "hash_tamper_test_script": "tamper_test.py",
}
OUTCOME_CLASSES = {"EXECUTE", "REFUSE", "REVOKE", "HALT", "PAUSE", "NARROW", "REDIRECT"}


def demand(test, msg):
    if not test:
        raise ValueError(msg)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def verify_zip(path):
    # Reads data only. No extraction, import or subprocess execution of applicant files.
    with ZipFile(path) as z:
        entries = z.infolist()
        demand(0 < len(entries) <= MAX_FILES, "Unsafe number of ZIP entries")
        names = [q.filename for q in entries]
        demand(len(set(names)) == len(names), "Duplicate archive path")
        total = 0
        raw = {}
        roots = set()
        for q in entries:
            name = q.filename
            pp = PurePosixPath(name)
            demand(not pp.is_absolute() and ".." not in pp.parts and
                   "\\" not in name and not name.startswith("/") and
                   len(name) < 240, "Unsafe ZIP path")
            demand(len(pp.parts) >= 2, "Unexpected top-level source")
            roots.add(pp.parts[0])
            demand(q.flag_bits & 1 == 0, "Encrypted source refused")
            demand(stat.S_IFMT(q.external_attr >> 16) != stat.S_IFLNK,
                   "Symlinked source refused")
            demand(q.file_size <= MAX_MEMBER and q.compress_size <= MAX_MEMBER,
                   "ZIP member exceeds byte bound")
            total += q.file_size
            demand(total <= MAX_TOTAL, "Expanded ZIP exceeds safety bound")
            if not q.is_dir():
                short = "/".join(pp.parts[1:])
                demand(short and short not in raw, "Duplicate content file")
                raw[short] = z.read(q)
        demand(len(roots) == 1, "Original must have one immutable package root")
    def parsed(name):
        demand(name in raw, "Missing original: " + name)
        return json.loads(raw[name].decode("utf-8"))

    m = parsed("manifest.json")
    demand(m.get("frozen_contract_version") == "DEPLOY_BUILD_V1_2",
           "Original contract version mismatch")
    for field, rel in HASHED_FILES.items():
        demand(rel in raw and HEX.fullmatch(m.get(field, "")),
               "Incomplete manifest file control: " + field)
        demand(digest(raw[rel]) == m[field], "Original data or script changed: " + rel)
    schema = {x.split("/")[-1]: digest(y) for x, y in sorted(raw.items())
              if x.startswith("schemas/") and x.endswith(".json")}
    demand(len(schema) >= 1, "Schema source family missing")
    demand(digest(canonical(schema)) == m.get("hash_schemas"),
           "Schema aggregate changed")

    fixture = parsed("fixtures/fixture_set_v1.json")
    boundaries = parsed("outputs/boundary_results.json")
    receipts = parsed("outputs/enforcement_receipts.json")
    replays = parsed("outputs/replay_records.json")
    report = parsed("reports/V1_2_certificate_verification_report.json")
    cases = fixture.get("cases")
    demand(isinstance(cases, list) and len(cases) == 8, "Original fixture count not eight")
    for group, label in [(boundaries, "boundaries"), (receipts, "receipts"), (replays, "replays")]:
        demand(isinstance(group, list) and len(group) == 8, label + " must have eight originals")
    ids = [c["case_id"] for c in cases]
    demand(len(set(ids)) == 8, "Original case identifiers not distinct")
    demand([x["case_id"] for x in boundaries] == ids and
           [x["case_id"] for x in receipts] == ids and
           [x["case_id"] for x in replays] == ids,
           "Original cases/receipts/replay misaligned")
    previous = "GENESIS"
    for cid, boundary, receipt, replay in zip(ids, boundaries, receipts, replays):
        outcome = boundary.get("boundary_outcome")
        demand(outcome in OUTCOME_CLASSES, "Unknown archived boundary outcome")
        demand(boundary.get("consequence_binds") is (outcome == "EXECUTE"),
               "Non-EXECUTE can bind protected consequence")
        demand(receipt.get("boundary_outcome") == outcome and
               receipt.get("boundary_decision_id") == boundary.get("boundary_decision_id"),
               "Boundary receipt disagrees with source")
        demand(receipt.get("prev_receipt_hash") == previous,
               "Original receipt chain interrupted")
        require_hash = receipt.get("receipt_hash")
        demand(isinstance(require_hash, str) and HEX.fullmatch(require_hash),
               "Original receipt digest invalid")
        recompute = dict(receipt)
        del recompute["receipt_hash"]
        demand(digest(canonical(recompute)) == require_hash,
               "Receipt hash fails independent recomputation")
        previous = require_hash
        demand(replay.get("receipt_id") == receipt.get("receipt_id") and
               replay.get("replay_determinant") == receipt.get("replay_determinant"),
               "Replay source link disagrees")
        demand(replay.get("expected_boundary_outcome") == outcome and
               replay.get("replayed_boundary_outcome") == outcome and
               replay.get("replay_match") is True,
               "Archived replay disagrees")
    demand(report.get("package_status") == "PASS" and report.get("verifier_exit_code") == 0,
           "Archived verification report does not say PASS")
    demand(report.get("tamper_test_exit_code") == 0, "Original archived tamper report not accepted")
    return {
        "status": "ARCHIVE_DATA_CONSISTENCY_PASS",
        "originalBytesLocallyInspected": True,
        "archiveSha256": digest(__import__("pathlib").Path(path).read_bytes()),
        "packageVersion": "DEPLOY_BUILD_V1_2",
        "manifestEntryHashesChecked": len(HASHED_FILES) + 1,
        "caseCount": len(cases),
        "receiptHashChainRecomputed": True,
        "replayRecordsCrossChecked": True,
        "originalVerificationReportStatus": report["package_status"],
        "originalTamperReportExitCode": report["tamper_test_exit_code"],
        "archivedVerifierExecutedByThisTool": False,
        "observedRealWorldEffect": False,
        "independentWitnessAuthenticated": False,
        "nativeV12StandingPromoted": False,
        "publicReleaseAuthorizedByThisTool": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", required=True, help="Private historical ZIP held on your machine")
    parser.add_argument("--out", help="Private result JSON path outside original; refuses overwrite")
    parser.add_argument("--expected-sha256", help="Known original ZIP SHA-256 from separate authenticated custody record")
    args = parser.parse_args()
    try:
        report = verify_zip(args.zip)
        if args.expected_sha256:
            demand(HEX.fullmatch(args.expected_sha256) and
                   args.expected_sha256 == report["archiveSha256"],
                   "ZIP original digest mismatch against separately fixed reference")
        if args.out:
            from pathlib import Path
            import os
            p = Path(args.out).absolute()
            fd = os.open(str(p), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as w:
                json.dump(report, w, indent=2)
                w.write("\n")
        print(json.dumps(report, indent=2))
    except (ValueError, KeyError, TypeError, BadZipFile, OSError, UnicodeError) as exc:
        parser.exit(2, "REFUSED: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
