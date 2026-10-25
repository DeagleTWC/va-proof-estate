#!/usr/bin/env python3
"""Negative controls for release-safe historic freeze identity; no real sources exposed."""
import copy
import hashlib
import json
import tempfile
from pathlib import Path

from validate_historical_carriers import validate_entry, validate_register


def hashbytes(payload):
    return hashlib.sha256(payload).hexdigest()


def reject(entry, root, reason):
    try:
        validate_entry(entry, root)
    except (ValueError, KeyError, TypeError, OSError):
        return
    raise AssertionError("Expected fail-closed rejection for " + reason)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        identifier = "HIST-SYNTHETIC-TEST-01"
        folder = root / "proofs/historical/carriers" / identifier
        folder.mkdir(parents=True)
        fixture = b"SYNTHETIC REGRESSION BYTES; NOT AN ORIGINAL PILOT OR FREEZE\n"
        path = folder / "public-extract.txt"
        path.write_bytes(fixture)
        source = hashbytes(b"synthetic imaginary original; no historical identity")
        payload = {
            "schema": "va-historical-carrier-entry/1.0",
            "id": identifier,
            "sourceKind": "FREEZE",
            "original": {
                "sourceDesignation": "SYNTHETIC TEST ONLY",
                "originalArtifactId": "NOT A REAL ORIGINAL",
                "originalFreezeDate": "2026-02-01",
                "originalSHA256": source,
                "originalCustodian": "TEST FIXTURE",
                "originalPilotOrRunId": None,
            },
            "publication": {
                "releaseAuthorizationId": "SYNTHETIC-CI-ONLY",
                "releaseClearedBy": "FAKE TEST AUTHORITY",
                "authorizedScope": "This synthetic unit test only",
                "extractPreparedDate": "2026-10-25",
                "publicExtractPath": f"proofs/historical/carriers/{identifier}/public-extract.txt",
                "publicExtractSHA256": hashbytes(fixture),
            },
            "evidence": {
                "standing": "SOURCE_RECORDED",
                "boundedClaim": "This synthetic bytes-only example tests validation",
                "conditionScope": "No external consequence",
                "routeCoverageLimits": "No routes are tested",
                "positiveObservation": None,
                "negativeObservation": None,
                "changedCondition": None,
                "receiptReplay": None,
                "observationFile": None,
                "observationSHA256": None,
                "negativeControlFile": None,
                "negativeControlSHA256": None,
                "replayFile": None,
                "replaySHA256": None,
            },
            "independent": {"reviewerPackets": [], "independenceReviewId": None},
            "protectedOriginalRemainsPrivate": True,
        }
        assert validate_entry(payload, root) == identifier
        bad = copy.deepcopy(payload);bad["publication"]["publicExtractSHA256"] = "0"*64
        reject(bad, root, "tampered payload")
        bad = copy.deepcopy(payload);bad["publication"]["releaseAuthorizationId"] = ""
        reject(bad, root, "no release authorization")
        bad = copy.deepcopy(payload);bad["original"]["originalFreezeDate"] = "2026-11-01"
        reject(bad, root, "retroactive historical freeze chronology")
        bad = copy.deepcopy(payload);bad["publication"]["publicExtractPath"] = "../../outside.txt"
        reject(bad, root, "path traversal")
        bad = copy.deepcopy(payload);bad["evidence"]["standing"] = "PUBLIC_BOUNDED_OBSERVATION"
        reject(bad, root, "unmeasured outcome promoted")
        bad = copy.deepcopy(payload);bad["evidence"]["standing"] = "PUBLIC_INDEPENDENT_REPRODUCTION"
        reject(bad, root, "fabricated independent promotion")
        bad = copy.deepcopy(payload);bad["id"] = "HIST-BAD-02"
        reject(bad, root, "misbound public carrier path")
        bad = copy.deepcopy(payload);bad["protectedOriginalRemainsPrivate"] = False
        reject(bad, root, "protected source disclosure guard")
        print("PASS: synthetic candidate accepted locally; eight invalid mutations rejected")
    validate_register(Path(__file__).resolve().parents[1])
    print("PASS: public release register is distinct from original historical event inventory")


if __name__ == "__main__":
    main()
