#!/usr/bin/env python3
"""Read-only cross-revision source identity examiner. Data-only; no runtime execution.

Checks source-byte continuity; never authenticates a signature, observer or effect.
All output from private originals remains PRIVATE, including hashes and file paths.
"""
import argparse
import hashlib
import json
import os
import stat
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, BadZipFile

LIMIT_MEMBERS = 60
LIMIT_EXPANDED = 3_000_000
RECEIPTS = ("execute_receipt_connected.json", "refuse_receipt_connected.json",
            "escalate_receipt_connected.json")


def demand(condition, why):
    if not condition:
        raise ValueError(why)


def unique_json_pairs(pairs):
    d = {}
    for key, value in pairs:
        demand(key not in d, "Duplicate JSON key")
        d[key] = value
    return d


def read_archive(path):
    path = Path(path)
    demand(path.is_file() and not path.is_symlink(), "Source must be a regular non-symlink file")
    raw = path.read_bytes()
    demand(len(raw) <= LIMIT_EXPANDED, "Source archive exceeds bound")
    with ZipFile(path) as z:
        infos = z.infolist()
        demand(1 <= len(infos) <= LIMIT_MEMBERS, "Archive member count outside bound")
        demand(len({i.filename for i in infos}) == len(infos), "Duplicate source member path")
        names = {}
        root = None
        expanded = 0
        for i in infos:
            p = PurePosixPath(i.filename)
            demand(not p.is_absolute() and "\\" not in i.filename and ".." not in p.parts
                   and len(p.parts) >= 2, "Unsafe archive member path")
            demand(not i.flag_bits & 1, "Encrypted archive refused")
            demand(stat.S_IFMT(i.external_attr >> 16) != stat.S_IFLNK,
                   "Symlink archive member refused")
            demand(i.file_size <= LIMIT_EXPANDED, "Oversize member")
            expanded += i.file_size
            demand(expanded <= LIMIT_EXPANDED, "Archive expanded size exceeds bound")
            demand(root is None or root == p.parts[0], "Archive spans different roots")
            root = p.parts[0]
            if i.is_dir():
                continue
            short = "/".join(p.parts[1:])
            demand(short not in names, "Repeated logical source path")
            demand(short.endswith((".json", ".md", ".txt")), "Unexpected source member type")
            names[short] = z.read(i)
    return hashlib.sha256(raw).hexdigest(), names


def obj(raw):
    val = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_json_pairs)
    demand(isinstance(val, dict), "Expected JSON object")
    return val


def compare_revisions(v1_path, v2_path):
    h1, a = read_archive(v1_path)
    h2, b = read_archive(v2_path)
    demand(h1 != h2, "Identical archives are not a changed-byte revision")
    demand("capture_completed.json" in a and "capture_completed.json" in b,
           "Missing original capture source")
    one, two = obj(a["capture_completed.json"]), obj(b["capture_completed.json"])
    run_one, run_two = one.get("run_id"), two.get("run_id")
    demand(isinstance(run_one, str) and bool(run_one.strip()) and run_one == run_two,
           "Same source run lineage not established")
    for d, archive in ((one, a), (two, b)):
        rows = d.get("cases")
        demand(isinstance(rows, list) and len(rows) == 3, "Three-case capture required")
        demand([r.get("case") for r in rows] == ["EXECUTE", "REFUSE", "ESCALATE"],
               "Expected three distinct decision classes")
        rec_ids = [obj(archive[name]).get("receipt_id") for name in RECEIPTS if name in archive]
        demand(len(rec_ids) == 3 and len(set(rec_ids)) == 3 and all(
            isinstance(x, str) and bool(x.strip()) for x in rec_ids),
            "Receipts must be present and uniquely identified")
        demand([r.get("receipt_id") for r in rows] == rec_ids,
               "Capture/receipt ID mapping changed inside source")
    results = []
    for name in RECEIPTS:
        left, right = a[name], b[name]
        x, y = obj(left), obj(right)
        same_id = x.get("receipt_id") == y.get("receipt_id")
        same_bytes = left == right
        flags = {
            "originalBytesIdentical": same_bytes,
            "receiptIdReused": same_id,
            "timestampTextReused": x.get("timestamp") == y.get("timestamp"),
            "stateHashTextReused": x.get("state_hash") == y.get("state_hash"),
            "signatureTextReused": x.get("receipt_sig") == y.get("receipt_sig"),
            "byteRevisionUnderReusedReceiptId": same_id and not same_bytes,
            "signedStateProvenanceAuthenticated": False,
            "externalTargetEffectQualified": False,
        }
        results.append({"case": name.split("_")[0].upper(),
                        "sourceSHA256v1": hashlib.sha256(left).hexdigest(),
                        "sourceSHA256v2": hashlib.sha256(right).hexdigest(),
                        **flags})
    changed = sum(x["byteRevisionUnderReusedReceiptId"] for x in results)
    return {
        "schema": "va-private-archived-receipt-revision/1.0",
        "classification": "PRIVATE_SOURCE_AUDIT_DO_NOT_PUBLISH",
        "firstOriginalArchiveSHA256": h1,
        "secondOriginalArchiveSHA256": h2,
        "sameDeclaredRunId": True,
        "sourceRunIdIntentionallyWithheldFromSummary": True,
        "caseRecordsCompared": len(results),
        "byteRevisionsUnderReusedReceiptIds": changed,
        "provenanceReviewRequired": changed > 0,
        "sourceRecords": results,
        "replayedActualRuntime": False,
        "independentProtectedEffectMeasured": False,
        "nativeVAScientificMilestoneClosed": False,
        "interpretation": ("An unchanged textual receipt ID, state hash or signature label "
                           "is not a substitute for original byte continuity or separately "
                           "authenticated revision custody. A changed record is not by itself "
                           "proof of an invalid execution or improper edit."),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connected-v1", required=True)
    parser.add_argument("--connected-v2", required=True)
    parser.add_argument("--out", help="new private result file (exclusive create)")
    a = parser.parse_args()
    try:
        report = compare_revisions(a.connected_v1, a.connected_v2)
        if a.out:
            p = Path(a.out)
            demand(not p.exists() and not p.is_symlink(), "Do not overwrite existing evidence")
            fd = os.open(str(p), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
                f.write("\n")
        print("PASS: same-run archive pair examined without executing archived code")
        print("Provenance review required:", report["provenanceReviewRequired"])
        print("Changed-source receipts reusing IDs:", report["byteRevisionsUnderReusedReceiptIds"])
        print("No independent external effect or cryptographic signature inferred")
    except (ValueError, KeyError, TypeError, OSError, BadZipFile, UnicodeError) as e:
        parser.exit(2, "REFUSED: " + str(e) + "\n")


if __name__ == "__main__":
    main()
