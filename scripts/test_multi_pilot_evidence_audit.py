#!/usr/bin/env python3
"""Synthetic negative-control coverage for private multi-pilot intake. Not a pilot."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from multi_pilot_evidence_audit import check_private_manifest

EXEC = Path(__file__).with_name("multi_pilot_evidence_audit.py")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def reject(data, root, reason):
    try:
        check_private_manifest(data, root)
    except (ValueError, KeyError, TypeError, OSError):
        return
    raise AssertionError("Missing fail-closed rejection: " + reason)


def run(root, manifest, report, expected=True):
    r = subprocess.run([sys.executable, str(EXEC), "audit", "--root", str(root),
                        "--manifest", str(manifest), "--out", str(report)],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if expected and r.returncode:
        raise AssertionError("Audit unexpectedly refused: " + r.stderr)
    if not expected and r.returncode == 0:
        raise AssertionError("Audit unexpectedly admitted invalid/mutated source")


def main():
    with tempfile.TemporaryDirectory(prefix="va-synthetic-pilot-audit-") as base:
        base = Path(base)
        root = base / "PRIVATE-SYNTHETIC-ORIGINALS"
        root.mkdir()
        (root / "separate-lanes").mkdir()
        def art(name, role, reviewer=None):
            path = root / "separate-lanes" / name
            payload = ("SYNTHETIC REGRESSION ONLY; NOT AN ORIGINAL PILOT " + name).encode()
            path.write_bytes(payload)
            item = {"role": role, "path": "separate-lanes/" + name, "sha256": sha(payload)}
            if reviewer:
                item["reviewerId"] = reviewer
            return item

        plan = art("scope.txt", "PILOT_SCOPE_OR_SPEC")
        freeze = art("original-build.bin", "ORIGINAL_FREEZE")
        verifier = art("build-verifier.json", "BUILD_VERIFICATION_REPORT")
        live = art("live-result.json", "LIVE_RUN_RESULT")
        receipt = art("receipt.json", "BOUNDARY_RECEIPT")
        replay = art("replay.json", "REPLAY_RECORD")
        neg = art("negative-case.json", "NEGATIVE_CONTROL")
        changed = art("changed-case.json", "CHANGED_CONDITION")
        acceptance = art("acceptance.json", "ACCEPTANCE_DECISION")
        rev1 = art("reviewer-one.json", "INDEPENDENT_REVIEW", "SYNTHETIC_REVIEWER_01")
        rev2 = art("reviewer-two.json", "INDEPENDENT_REVIEW", "SYNTHETIC_REVIEWER_02")
        def lane(id, stage, entries):
            return {"localId": id, "sourceType": "HISTORICAL_PILOT_OR_FREEZE",
                    "claimedStage": stage, "artifacts": entries}
        data = {
            "schema": "va-private-multi-pilot-audit/1.0",
            "classification": "PRIVATE_LOCAL_SOURCE_REVIEW_DO_NOT_PUBLISH",
            "releaseApproval": False,
            "pilots": [
                lane("PILOT-LOCAL-01", "SOURCE_INVENTORIED", [plan]),
                lane("PILOT-LOCAL-02", "BUILD_VERIFICATION_PACKET_PRESENT", [freeze, verifier]),
                lane("PILOT-LOCAL-03", "LIVE_RUN_PACKET_PRESENT", [plan, live, receipt, replay]),
            ],
        }
        checked = check_private_manifest(data, root)
        assert len(checked) == 3
        assert all(x["actualConsequenceOutcomeIsUnverified"] is True for x in checked)
        assert all(x["publicationAuthorized"] is False for x in checked)
        manifest, report = base / "private-manifest.json", base / "private-report.json"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        run(root, manifest, report)
        result = json.loads(report.read_text(encoding="utf-8"))
        assert result["classification"].startswith("PRIVATE")
        assert result["numberOfLocallyReviewedLanesNotTotalPilots"] == 3
        assert not any("separate-lanes/" in json.dumps(x) for x in result["lanes"])
        assert (report.stat().st_mode & 0o077) == 0
        run(root, manifest, report, expected=False)  # cannot overwrite private report
        mutations = []
        x = copy.deepcopy(data)
        x["pilots"][0]["claimedStage"] = "LIVE_RUN_PACKET_PRESENT"
        mutations.append((x, "proposed scope cannot become live run"))
        x = copy.deepcopy(data)
        x["pilots"][1]["claimedStage"] = "ACCEPTANCE_PACKET_PRESENT"
        mutations.append((x, "verified build base is not pilot acceptance"))
        x = copy.deepcopy(data)
        x["pilots"][2]["claimedStage"] = "INDEPENDENT_PACKET_PRESENT"
        mutations.append((x, "live packet not independent"))
        x = copy.deepcopy(data)
        x["pilots"].append(copy.deepcopy(x["pilots"][0]))
        mutations.append((x, "duplicate pilot"))
        x = copy.deepcopy(data)
        x["pilots"][2]["artifacts"][0]["sha256"] = "0"*64
        mutations.append((x, "altered source bytes"))
        x = copy.deepcopy(data)
        x["pilots"][0]["artifacts"][0]["path"] = "../outside.txt"
        mutations.append((x, "path traversal"))
        x = copy.deepcopy(data)
        x["releaseApproval"] = True
        mutations.append((x, "private-to-public flag"))
        x = copy.deepcopy(data)
        x["pilots"][2]["artifacts"].append(copy.deepcopy(x["pilots"][2]["artifacts"][0]))
        mutations.append((x, "duplicate file path"))
        x = copy.deepcopy(data)
        x["pilots"][0]["artifacts"][0]["role"] = "AUTHORIZED_RESULT_BY_WORDS"
        mutations.append((x, "unknown role"))
        for mutation, reason in mutations:
            reject(mutation, root, reason)
        x = copy.deepcopy(data)
        x["pilots"].append(lane("PILOT-LOCAL-04", "INDEPENDENT_PACKET_PRESENT",
                                [plan, live, receipt, replay, changed, neg, acceptance, rev1, rev2]))
        with_review = check_private_manifest(x, root)
        assert len(with_review) == 4
        assert with_review[-1]["independentHumanIdentityIsUnverified"] is True
        x["pilots"][-1]["artifacts"][-1]["reviewerId"] = "SYNTHETIC_REVIEWER_01"
        reject(x, root, "same declared examiner")
        (root / "separate-lanes" / "linked.bin").symlink_to(root / "separate-lanes" / "original-build.bin")
        x = copy.deepcopy(data)
        x["pilots"][0]["artifacts"][0]["path"] = "separate-lanes/linked.bin"
        reject(x, root, "symlink")
        print("PASS: multiple isolated pilot source lanes and explicit evidence packet classes")
        print("PASS: nine synthetic false-promotion/data-integrity mutations, overwrite and symlink rejected")
        print("PASS: reviewer-name presence never converted into independent-person proof")


if __name__ == "__main__":
    main()
