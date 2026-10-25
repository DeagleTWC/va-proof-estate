#!/usr/bin/env python3
"""Fail-closed public status guard for a privately retained historical engineering ZIP."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(test, message):
    if not test:
        raise ValueError(message)


def check(data):
    require(data.get("schema") == "deagle-v12-original-v1.2-private-custody-verification/1.0",
            "Original proof status schema changed")
    require(data.get("historicalEngineeringIdentity") == "DEPLOY_BUILD_V1_2",
            "Older engineering artifact relabeled as current runtime")
    require(data.get("currentSystemIdentityNotThisArtifact") == "V.A. V12",
            "Current system identity distinction removed")
    require(data.get("sourceClass") == "PRIVATE_ORIGINAL_ENGINEERING_ARCHIVE",
            "Protected source custody changed")
    require(data.get("verificationClass") == "CUSTODIAN_LOCAL_ORIGINAL_BYTES_AND_PACKAGE_CHECKS",
            "Verification wrongly promoted to independent witness")
    for attr in (
        "twoOriginalLibraryCopiesCompared", "twoOriginalLibraryCopiesIdentical",
        "originalSuppliedVerifierExecutedOnControlledExtract",
        "originalSuppliedTamperTestExecutedOnControlledExtract",
        "postTestPackageDataHashesStillMatched", "sourceExactDigestRetainedPrivate",
        "nonPromotion"
    ):
        require(data.get(attr) is True, "Missing recorded bounded verification: " + attr)
    for attr in (
        "originalSourceSha256ReleasedInThisPublicRecord",
        "originalZipBytesReleasedInThisPublicRecord",
        "originalFreezeDateAuthenticatedFromOriginal"
    ):
        require(data.get(attr) is False, "Unverified source release/freeze field promoted: " + attr)
    expected = {
        "originalZipSizeBytes": 18955,
        "manifestFileOrAggregateChecksMatched": 10,
        "archivedFileEntries": 22,
        "originalFixtureCases": 8,
        "originalBoundaryResults": 8,
        "originalEnforcementReceipts": 8,
        "originalReplayRecords": 8,
        "originalSuppliedVerifierExitCode": 0,
        "originalSuppliedTamperExitCode": 0,
        "originalSuppliedVerifierResult": "PASS",
    }
    for attr, value in expected.items():
        require(type(data.get(attr)) == type(value) and data[attr] == value,
                "Original archived result altered: " + attr)
    ceiling = {
        "originalArchivedEngineeringEvidence": "LOCALLY VERIFIED",
        "realWorldPilotEffect": "NOT ESTABLISHED BY THIS SOURCE",
        "authenticIndependentHumanReview": "NOT ESTABLISHED BY THIS RUN",
        "nativeV12Result": "NOT INFERRED",
        "originalPublicCarrierAdmission": "NOT AUTHORIZED OR ATTACHED",
        "physicalKCD": "SEPARATE UNEXAMINED TRACK",
    }
    for attr, val in ceiling.items():
        require(data.get("proofBoundary", {}).get(attr) == val,
                "Proof boundary inflated: " + attr)
    original_index = json.loads(
        (ROOT / "proofs/historical/PUBLIC-CARRIER-REGISTER.json").read_text(encoding="utf-8"))
    require(original_index.get("entries") == [],
            "Original run register changed; evaluate new release rights first")
    return data["originalFixtureCases"]


def main():
    p = ROOT / "proofs/V1.2-ORIGINAL-SOURCE-VERIFICATION.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    count = check(data)
    print("PASS: real private original engineering evidence status retained, cases:", count)


if __name__ == "__main__":
    main()
