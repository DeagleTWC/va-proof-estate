#!/usr/bin/env python3
"""Synthetic-only source revision negative controls; never historical measurements."""
import copy
import json
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from check_historical_receipt_revision import compare_revisions

CASES = ("EXECUTE", "REFUSE", "ESCALATE")

def fixture(latencies, run_id="SYNTHETIC_RUN", ids=None):
    archive = {}
    rows = []
    ids = ids or ["SYNTH_RCP_" + c for c in CASES]
    for c, ms, rid in zip(CASES, latencies, ids):
        x = {"receipt_id": rid, "decision": c, "timestamp": "SYNTHETIC_TIME",
             "state_hash": "SYNTHETIC_STATE_" + c, "receipt_sig": "SYNTHETIC_NOT_SIGNATURE_" + c,
             "commit_boundary": "attending_signoff" if c == "EXECUTE" else "not_reached",
             "bindability": {"commit_allowed": c == "EXECUTE"},
             "constraints": {"latency_ms": ms}}
        archive[c.lower() + "_receipt_connected.json"] = x
        rows.append({"case": c, "outcome": c, "receipt_id": rid,
                     "latency_ms_observed": ms,
                     "commit_boundary_reached": c == "EXECUTE"})
    archive["capture_completed.json"] = {"run_id": run_id, "cases": rows}
    return archive

def pack(path, d, root="synthetic_private"):
    with ZipFile(path, "w", ZIP_DEFLATED) as z:
        for name, val in d.items():
            content = val if isinstance(val, str) else json.dumps(val, sort_keys=True) + "\n"
            z.writestr(root + "/" + name, content)

def refused(a, b, why):
    try:
        compare_revisions(a,b)
    except (ValueError, KeyError, TypeError):
        return
    raise AssertionError("Expected fail-closed: " + why)

def main():
    with tempfile.TemporaryDirectory(prefix="synthetic-receipt-revision-") as tmp:
        p, q = (Path(tmp)/"v1.zip", Path(tmp)/"v2.zip")
        one = fixture([10,20,30])
        two = fixture([11,22,33])
        pack(p,one);pack(q,two)
        result = compare_revisions(p,q)
        assert result["caseRecordsCompared"] == 3
        assert result["byteRevisionsUnderReusedReceiptIds"] == 3
        assert result["provenanceReviewRequired"]
        assert all(x["signatureTextReused"] and x["stateHashTextReused"] for x in result["sourceRecords"])
        assert not result["independentProtectedEffectMeasured"]
        # Unchanged individual receipt can be distinguished from changed record.
        two2 = copy.deepcopy(one)
        two2["capture_completed.json"]["review_version"] = 2
        pack(q, two2)
        r2 = compare_revisions(p,q)
        assert r2["byteRevisionsUnderReusedReceiptIds"] == 0
        assert not r2["provenanceReviewRequired"]
        # Fresh receipt identity under changed bytes must not be mislabeled reused.
        fresh = fixture([11,22,33], ids=["SYNTH_NEW_" + x for x in CASES])
        pack(q, fresh)
        rf = compare_revisions(p,q)
        assert rf["byteRevisionsUnderReusedReceiptIds"] == 0
        assert all(not x["receiptIdReused"] for x in rf["sourceRecords"])
        # Tampering with run provenance or capture binding fails closed.
        bad = copy.deepcopy(two)
        bad["capture_completed.json"]["run_id"] = "DIFFERENT_RUN"
        pack(q,bad);refused(p,q,"different run ID")
        bad = copy.deepcopy(two)
        bad["capture_completed.json"]["cases"][0]["receipt_id"] = "MISMATCH"
        pack(q,bad);refused(p,q,"capture receipt mismatch")
        bad = copy.deepcopy(two)
        bad["refuse_receipt_connected.json"]["receipt_id"] = bad["execute_receipt_connected.json"]["receipt_id"]
        pack(q,bad);refused(p,q,"duplicate receipt ID")
        bad = copy.deepcopy(two)
        bad["refuse_receipt_connected.json"] = '{"receipt_id":"a","receipt_id":"b"}'
        pack(q,bad);refused(p,q,"duplicate JSON key")
        # Unsafe archive path and source member duplicate detection.
        with ZipFile(q,"w",ZIP_DEFLATED) as z:
            z.writestr("synthetic_private/../escape.json", "{}")
        refused(p,q,"path traversal")
        with ZipFile(q,"w",ZIP_DEFLATED) as z:
            z.writestr("synthetic_private/same.json", "{}")
            z.writestr("synthetic_private/same.json", "{}")
        refused(p,q,"duplicate archive path")
        # Real source structure is checked *inside each version*, not assumed
        # from matching receipt IDs or revised source hashes.
        more_tests = [
            ("decision contradicts case", "refuse_receipt_connected.json",
             lambda x: x.update(decision="EXECUTE")),
            ("receipt latency contradicts capture", "execute_receipt_connected.json",
             lambda x: x["constraints"].update(latency_ms=1111)),
            ("captured effect boundary forged", "capture_completed.json",
             lambda x: x["cases"][1].update(commit_boundary_reached=True)),
            ("receipt binding contradicts case", "escalate_receipt_connected.json",
             lambda x: x["bindability"].update(commit_allowed=True)),
            ("receipt consequence boundary contradicts case", "execute_receipt_connected.json",
             lambda x: x.update(commit_boundary="not_reached")),
            ("signature-like label absent", "refuse_receipt_connected.json",
             lambda x: x.pop("receipt_sig")),
            ("timestamp absent", "execute_receipt_connected.json",
             lambda x: x.pop("timestamp")),
            ("invalid latency type", "capture_completed.json",
             lambda x: x["cases"][0].update(latency_ms_observed=True)),
        ]
        for label, item, mutate in more_tests:
            bad = copy.deepcopy(two)
            mutate(bad[item])
            pack(q, bad)
            refused(p, q, label)
        pack(q, two)
        assert compare_revisions(p, q)["byteRevisionsUnderReusedReceiptIds"] == 3
        print(f"PASS: 3 synthetic revision classifications + {6+len(more_tests)} synthetic negative controls")
        print("PASS: no original run, independent observer, external effect or signature qualified")

if __name__ == "__main__":
    main()
