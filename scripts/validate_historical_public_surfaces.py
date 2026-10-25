#!/usr/bin/env python3
"""Validate historical public source references without manufacturing freeze or pilot evidence."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    "elyria-one-proof",
    "elyria-pre-effect-enforcement-harness",
    "authority-revocation-witness",
    "scope-expiry-gate",
    "elyria-ai-revalidation-engine",
    "veritas-safechange",
]
SHA = re.compile(r"^[a-f0-9]{40}$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(name):
    return (ROOT / name).read_bytes()


def validate(data, source_text, manifest):
    require(data.get("schema") == "deagle-historical-public-surfaces/1.0", "schema changed")
    src = data["sourceDocument"]
    require(SHA256.fullmatch(src["pdfSHA256"]), "source PDF digest malformed")
    require(src["pdfSHA256"] in source_text, "source digest not in original-public transcription")
    require(src["transcription"] == "proofs/sources/shift-public-proof-path-v2-extracted.md", "unexpected source transcription")
    require("not" in src["primaryLocation"].lower() and "reviewer" in src["primaryLocation"].lower(),
            "review-route/non-integration ceiling removed")
    ctx = data["publicationContext"]
    require("pre-date" in ctx["historicalRecord"].lower() or "predate" in ctx["historicalRecord"].lower(),
            "preexisting historical record omitted")
    require("not the entirety" in ctx["sixSurfaceScope"].lower(), "six-surface selection misrepresented as entire history")
    require(ctx["originalNativeRunReceiptsAttachedHere"] == manifest["nativeRuntimeReceiptsAttached"],
            "native count incompatible with manifest")
    require(ctx["publicIndependentNativeReproductionsAttachedHere"] == manifest["independentlyReproducedRunsAttached"],
            "independent reproduction count incompatible with manifest")

    surfaces = data.get("selectedPublicSurfaces", [])
    require(len(surfaces) == len(EXPECTED), "public route changed without source revision")
    require([x["sourceOrder"] for x in surfaces] == list(range(1, 7)), "source order changed")
    require(len({x["repository"] for x in surfaces}) == 6, "duplicate original source repository")
    for surface, expected in zip(surfaces, EXPECTED):
        target = "Kamanaka5502/" + expected
        sha = surface["currentRevisionSnapshot"]["sha"]
        require(surface["repository"] == target, f"source mismatch: {target}")
        require(expected in source_text, f"source PDF missing reference: {expected}")
        require(surface["url"] == "https://github.com/" + target, f"unexpected source URL: {target}")
        require(SHA.fullmatch(sha) is not None and sha != "0"*40, f"invalid revision identity: {target}")
        require(surface["currentRevisionSnapshot"]["commitUrl"] == "https://github.com/" + target + "/commit/" + sha,
                f"revision link not bound: {target}")
        require(surface["declaredReviewPurpose"] and surface["publicLabel"], f"missing review scope: {target}")
        ceiling = surface["historyBoundary"].lower()
        require("not identified as the original historical freeze" in ceiling, f"freeze-ceiling missing: {target}")
        require("not mirrored" in surface["relationToCurrent"].lower(), f"wrong lineage: {target}")

    inv = data["originalHistoricalFreezeInventory"]
    entries = inv.get("entries", [])
    require(isinstance(entries, list) and inv["entryCount"] == len(entries), "freeze entries/count mismatch")
    require(ctx["verifiedOriginalHistoricalFreezeHashesAttachedInThisList"] == len(entries),
            "freeze hashes do not match original-carrier entries")
    require("not a statement that no freezes" in inv["note"].lower(), "missing-public != absence caveat lost")
    require(isinstance(inv["requiredFields"], list) and len(inv["requiredFields"]) >= 7, "original custody fields missing")
    # A future source-cleared original must be carried as an exact local file with its original digest and release decision.
    for entry in entries:
        for key in inv["requiredFields"]:
            require(entry.get(key), f"original freeze missing required field: {key}")
        path = entry.get("publicCarrierPath")
        digest = entry.get("publicCarrierSHA256")
        require(isinstance(path, str) and path.startswith("proofs/historical/") and ".." not in Path(path).parts,
                "unapproved historical carrier path")
        require(SHA256.fullmatch(digest or "") is not None, "original carrier hash invalid")
        require(hashlib.sha256(read(path)).hexdigest() == digest, "historical carrier bytes mismatch")
    return len(surfaces), len(entries)


def main():
    data = json.loads(read("proofs/HISTORICAL-PUBLIC-SURFACES.json"))
    source_text = read("proofs/sources/shift-public-proof-path-v2-extracted.md").decode("utf-8")
    manifest = json.loads(read("proof-estate-manifest.json"))
    surfaces, originals = validate(data, source_text, manifest)
    index = read("proofs/HISTORICAL-EVIDENCE-INDEX.md").decode("utf-8")
    for record in data["selectedPublicSurfaces"]:
        require(record["repository"] in index, "history index missing selected public surface: " + record["repository"])
    require("HISTORICAL-PUBLIC-SURFACES.json" in index, "machine-readable history registry not linked")
    print(f"PASS: {surfaces} indexed original public proof-route surfaces; {originals} source-admitted frozen originals")
    print("PASS: source-to-revision links, separated evidence status and original-custody gate")


if __name__ == "__main__":
    main()
