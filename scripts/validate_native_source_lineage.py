#!/usr/bin/env python3
"""Fail-closed public-source guard; never executes or imports native kernels.

This identifies exact-byte reintroductions of a known *reference* code family,
not behavioral clones, authorship, direction of copying, or native performance.
"""
import hashlib
import json
import re
from html import unescape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Six public Git blob identities independently matched against the privately
# retained R19 cybersecurity packet on 2026-11-21. No source bytes included.
REFERENCE_MODULE_SHA1 = frozenset({
    "b6d1350a82e05d20e91badda51bb3b2fe2e786cb",  # models.py
    "210eb125fcc1c6d8c5e550e855b04d419239287e",  # api.py
    "6e5f2754317cfc26bdd3c819ef4fda34fe495c44",  # receipt.py
    "91d3dc21c8901d08efd2cdf82bb7dcb80c301116",  # resolver.py
    "49ddb8f413db045be617f36c0a6a70c2b5347728",  # reality_kernel.py
    "6879359604324795ef82188b00c8d2be7b71c84e",  # thermo_gate.py
})

CURRENT_PAGES = {
    "index.html": "NEW corrected K",
    "foundation.html": "Corrected NEW K",
    "end-to-end.html": "NEW corrected K",
}
REQUIRED_FOUNDATION = "True Zero / corrected NEW K / Elements Basin / URK"


def git_blob_sha1(content: bytes) -> str:
    prefix = b"blob " + str(len(content)).encode("ascii") + b"\0"
    return hashlib.sha1(prefix + content).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(root: Path, reference_fingerprints: frozenset[str] | None = None) -> dict[str, int]:
    root = root.resolve()
    fingerprints = REFERENCE_MODULE_SHA1 if reference_fingerprints is None else reference_fingerprints

    manifest = json.loads((root / "proof-estate-manifest.json").read_text(encoding="utf-8"))
    reviewer = manifest.get("publicReviewerRoute", {})
    require(reviewer.get("primaryFoundation") == REQUIRED_FOUNDATION,
            "Current public-reviewer foundation changed away from corrected NEW K")
    require(reviewer.get("protectedConstructionPublished") is False,
            "Public hub must not publish protected native construction")

    for filename, marker in CURRENT_PAGES.items():
        page = (root / filename).read_text(encoding="utf-8")
        require(marker in page, "Current NEW K identity missing: " + filename)
        require(not re.search(r"\bold[\s-]*k\b", unescape(page), flags=re.IGNORECASE),
                "Current page assigns old K to the operative floor: " + filename)

    register = json.loads((root / "proofs/VA-ORIGINAL-CAPABILITY-RECOVERY.json")
                          .read_text(encoding="utf-8"))
    references = register.get("sourceReferences")
    require(isinstance(references, list) and len(references) == 36,
            "Source reference inventory changed without lineage review")
    for entry in references:
        require(entry.get("sourceOwnerAtSnapshot") == "Kamanaka5502"
                and entry.get("standing") == "PUBLIC_SOURCE_REFERENCE_ONLY"
                and entry.get("implementationCopied") is False
                and entry.get("nativeVAEvidence") is False,
                "An outside source is silently promoted, copied, or reattributed")

    code_files = 0
    for path in root.rglob("*.py"):
        require(not path.is_symlink(),
                "Python symlink cannot bypass native-source comparison: " + str(path.relative_to(root)))
        if not path.is_file():
            continue
        code_files += 1
        require(git_blob_sha1(path.read_bytes()) not in fingerprints,
                "Found byte-matched reference module where native V.A. code is expected: "
                + str(path.relative_to(root)))

    return {
        "current_foundation_pages": len(CURRENT_PAGES),
        "external_references_checked": len(references),
        "code_files_checked": code_files,
        "reference_module_matches": 0,
    }


if __name__ == "__main__":
    result = validate(ROOT)
    print("PASS: active hub retains corrected NEW K; outside sources stay references")
    print("PASS: exact-byte reference source is not imported as native code", result)
