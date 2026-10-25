#!/usr/bin/env python3
"""Read-only audit of original release ZIP member hash closure.

This does NOT execute archived code, claim historical freeze chronology, authenticate
a person, measure real-world effects, or approve source publication. Results are
PRIVATE: they contain original source filenames and digests.
"""
import argparse
import hashlib
import json
import os
import re
import stat
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, BadZipFile

HEX = re.compile(r"^[a-f0-9]{64}$")
EXECUTABLE_ENDINGS = (".py", ".js", ".mjs", ".cjs", ".ts", ".sh",
                      ".bash", ".ps1", ".bat", ".command", ".exe")
MAX_FILES = 2500
MAX_ENTRY = 100_000_000
MAX_EXPANDED = 500_000_000


def require(condition, description):
    if not condition:
        raise ValueError(description)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def examine(original, index_name="RELEASE_HASHES.json", fixed_archive_sha=None):
    original = Path(original)
    require(original.is_file() and not original.is_symlink(), "Original ZIP missing/symlinked")
    archive_bytes = original.read_bytes()
    zip_sha = sha(archive_bytes)
    if fixed_archive_sha is not None:
        require(isinstance(fixed_archive_sha, str) and HEX.fullmatch(fixed_archive_sha),
                "Invalid original independently fixed SHA-256")
        require(zip_sha == fixed_archive_sha, "Original ZIP fails external custody digest")
    require(isinstance(index_name, str) and 0 < len(index_name) <= 160,
            "Hash-index filename invalid")
    require("/" not in index_name and "\\" not in index_name and ".." not in index_name,
            "Index cannot escape archive root")

    with ZipFile(original) as z:
        entries = z.infolist()
        require(1 < len(entries) <= MAX_FILES, "Invalid archive member count")
        names = [e.filename for e in entries]
        require(len(names) == len(set(names)), "Duplicate ZIP source member")
        raw, expanded = {}, 0
        for entry in entries:
            name = entry.filename
            pp = PurePosixPath(name)
            require(not pp.is_absolute() and ".." not in pp.parts
                    and "\\" not in name and len(name) < 300,
                    "Unsafe original ZIP member path")
            require(entry.flag_bits & 1 == 0, "Encrypted source refused")
            require(stat.S_IFMT(entry.external_attr >> 16) != stat.S_IFLNK,
                    "Original ZIP symlink refused")
            require(0 <= entry.file_size <= MAX_ENTRY and
                    0 <= entry.compress_size <= MAX_ENTRY, "Source member oversize")
            expanded += entry.file_size
            require(expanded <= MAX_EXPANDED, "Unsafe expanded ZIP total")
            if entry.is_dir():
                continue
            require(name not in raw, "Duplicate original source path")
            raw[name] = z.read(entry)
        require(index_name in raw, "Release hash index not present")
        try:
            registry = json.loads(raw[index_name].decode("utf-8"))
        except (UnicodeError, ValueError) as err:
            raise ValueError("Unreadable source hash-index JSON") from err
        require(isinstance(registry, dict), "Hash index must be a flat object")
        require(index_name not in registry, "Self-referential hash index unsupported")
        for name, digest in registry.items():
            pp = PurePosixPath(name)
            require(isinstance(name, str) and not pp.is_absolute()
                    and ".." not in pp.parts and "\\" not in name and name and
                    isinstance(digest, str) and HEX.fullmatch(digest),
                    "Unsafe or non-SHA256 release index entry")
        present = set(raw) - {index_name}
        declared = set(registry)
        mismatched = sorted(n for n in present & declared if sha(raw[n]) != registry[n])
        missing = sorted(declared - present)
        unindexed = sorted(present - declared)
        unindexed_executable = sorted(x for x in unindexed
                                      if x.lower().endswith(EXECUTABLE_ENDINGS))
        passed = not (mismatched or missing or unindexed)
        return {
            "schema": "va-release-archive-seal-audit/1.0",
            "result": "INTERNAL_SOURCE_HASH_CLOSURE_PASS" if passed else "HOLD_INCOMPLETE_OR_ALTERED_RELEASE_SEAL",
            "originalArchiveSHA256": zip_sha,
            "originalCustodyDigestCompared": fixed_archive_sha is not None,
            "archiveMembers": len(raw),
            "hashIndexEntries": len(registry),
            "verifiedMemberHashes": len(present & declared) - len(mismatched),
            "declaredButMissing": missing,
            "registeredButDigestMismatch": mismatched,
            "unindexedOriginalMembers": unindexed,
            "unindexedExecutableMembers": unindexed_executable,
            "hashIndexSelfExcludedByDesign": True,
            "originalBytesModified": False,
            "archivedCodeExecuted": False,
            "qualifiedNativeVAWitnessAuthenticated": False,
            "observedExternalConsequenceVerified": False,
            "productionStandingConferred": False,
            "sourceRedistributionAuthorized": False,
            "note": "Exact manifest closure checks only the internal consistency of one archive. Even a complete seal is not an external historical freeze, independent observer, native V.A. run, physical effect, reviewer identity or disclosure approval."
        }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archive", required=True)
    p.add_argument("--index", default="RELEASE_HASHES.json")
    p.add_argument("--expected-archive-sha256",
                   help="A digest from separate earlier trustworthy custody, not a value newly copied from the ZIP")
    p.add_argument("--out", help="New PRIVATE JSON file, outside the input archive")
    args = p.parse_args()
    try:
        audit = examine(args.archive, args.index, args.expected_archive_sha256)
        if args.out:
            output = Path(args.out).absolute()
            original = Path(args.archive).absolute()
            require(not output.exists() and not output.is_symlink()
                    and output != original and output.parent != original.parent,
                    "Refuse overwrite or output alongside protected original")
            fd = os.open(str(output), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as out:
                json.dump(audit, out, indent=2)
                out.write("\n")
        print(json.dumps(audit, indent=2))
        if audit["result"] != "INTERNAL_SOURCE_HASH_CLOSURE_PASS":
            p.exit(2, "HOLD: original internal source seal is incomplete or differs from recorded digests\n")
    except (ValueError, TypeError, KeyError, OSError, BadZipFile) as err:
        p.exit(2, "REFUSED: " + str(err) + "\n")


if __name__ == "__main__":
    main()
