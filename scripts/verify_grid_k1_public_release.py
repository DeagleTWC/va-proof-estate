#!/usr/bin/env python3
"""Verify GRID-K1 public publication/custody crosswalk without opening protected sources.

This checks release metadata and public artifact hashes; exact-rational replay,
receipt integrity and negative controls are independently checked by the
read-only reproducibility/verify_exact_output.py script.
"""
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GRID = REPO / "research" / "grid-k1"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def main():
    manifest = load(GRID / "PUBLIC_RELEASE_MANIFEST.json")
    index = load(REPO / "research" / "mathematics" / "INDEX.json")
    contract = load(GRID / "output" / "PREPARED_CONTRACT.json")
    crosswalk = (GRID / "FORMULA_TO_PROOF_CROSSWALK.md").read_text(encoding="utf-8")
    release_id = "grid-k1-2026-11-11"
    matches = [e for e in index["entries"] if e.get("id") == release_id]
    require(len(matches) == 1, "Expected one GRID-K1 mathematics index entry")
    entry = matches[0]

    require(manifest["publication_status"] == "PUBLIC_RESEARCH_RELEASE",
            "Publication status is not the released public research record")
    require(manifest["source_status_original"] == "approval_draft",
            "Original parent source standing changed")
    require(not manifest["original_sources_in_public_package"],
            "Public release must not represent private original source as distributed")
    require(not (GRID / "sources").exists(),
            "Private source directory must not be published")
    require("**Standing:** Public research release v1.0" in crosswalk,
            "Crosswalk publication standing contradicts public manifest")
    require("not a published Deagle research record" not in crosswalk,
            "Stale unpublished crosswalk text detected")
    require("not the protected URK generator" in crosswalk,
            "Native-vs-demonstrator boundary missing from crosswalk")
    require(entry["manifest"] == "research/grid-k1/PUBLIC_RELEASE_MANIFEST.json",
            "Index manifest path mismatch")
    require(entry["record"] == manifest["site_path"],
            "Index public research route mismatch")
    require(entry["original_sources_public"] is False,
            "Index source disclosure status mismatch")
    require(entry["pdf_hosted"] is True, "Index published PDF flag absent")
    require(manifest["certificate_count"] == manifest["receipt_count"] == manifest["witness_count"] == 7,
            "Published case-count claim changed")
    require(len(contract["scenarios"]) == 7, "Frozen scenario count changed")

    source_hashes = manifest["source_sha256"]
    source_custody = contract["source_custody"]
    require(source_hashes["Critical_Infrastructure_Continuity_Kernel_v1.json"]
            == source_custody["continuity_kernel_json_sha256"], "Kernel source digest mismatch")
    require(source_hashes["1886f847-cbfc-4955-8884-8ca6235568b2.docx"]
            == source_custody["world_kernel_atlas_docx_sha256"], "Atlas source digest mismatch")

    pdf = entry["pdf_filename"]
    archive = Path(entry["supporting_archive"]).name
    require(pdf in manifest["files"] and archive in manifest["files"],
            "Published PDF or evidence archive missing in manifest")
    require(entry["pdf_sha256"] == manifest["files"][pdf]["sha256"],
            "Index PDF digest mismatch")
    require(entry["supporting_archive_sha256"] == manifest["files"][archive]["sha256"],
            "Index evidence archive digest mismatch")
    for name, metadata in manifest["files"].items():
        path = GRID / name
        require(path.is_file(), f"Release artifact missing: {name}")
        data = path.read_bytes()
        require(len(data) == metadata["bytes"], f"Release byte length mismatch: {name}")
        require(hashlib.sha256(data).hexdigest() == metadata["sha256"],
                f"Release SHA-256 mismatch: {name}")

    public_index = (REPO / "mathematics.html").read_text(encoding="utf-8")
    public_record = (REPO / manifest["site_path"]).read_text(encoding="utf-8")
    require(manifest["site_path"] in public_index,
            "GRID-K1 research page absent from mathematics public index")
    require(pdf in public_index and archive in public_index,
            "Public mathematics index lacks download links")
    require(pdf in public_record and archive in public_record,
            "Public GRID-K1 page lacks download links")
    print("PASS: GRID-K1 public release, source custody, 7-case claim ceiling,")
    print("      signed-off public artifact identities and navigation correspondence.")
    print("NOTE: private originals are intentionally not checked by this public test.")

if __name__ == "__main__":
    main()
