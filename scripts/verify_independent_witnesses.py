#!/usr/bin/env python3
"""Verify signed external observation *records*, not effects or human independence.

Requires local OpenSSL. Reads data only; never executes applicant workflows.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

HEX = re.compile(r"^[a-f0-9]{64}$")
IDENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{2,100}$")
SCHEMA = "va-independent-observation-bundle/1.0"
CASES = {"ALLOW", "REFUSE", "CHANGED"}
METHODS = {"PHYSICAL_INSTRUMENT", "SEPARATE_SYSTEM_AUDIT", "INDEPENDENT_OBSERVER_LOG"}
MAX_FILE = 1_000_000
MAX_CASES = 30


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def hash_bytes(data):
    return hashlib.sha256(data).hexdigest()


def checked_file(root, ref, label):
    need(isinstance(ref, dict), "Missing source: " + label)
    p, digest = ref.get("path"), ref.get("sha256")
    need(isinstance(p, str) and p and len(p) < 250 and "\\" not in p,
         "Bad file path: " + label)
    relative = Path(p)
    need(not relative.is_absolute() and ".." not in relative.parts
         and relative.as_posix() == p, "Unsafe source path: " + label)
    need(isinstance(digest, str) and HEX.fullmatch(digest), "Missing SHA-256: " + label)
    q = root
    for name in relative.parts:
        q = q / name
        need(not q.is_symlink(), "Symlink refused: " + label)
    q = q.resolve()
    need(q.is_relative_to(root) and q.is_file(), "Missing source: " + label)
    need(q.stat().st_size <= MAX_FILE, "Oversized source: " + label)
    raw = q.read_bytes()
    need(hash_bytes(raw) == digest, "Original source bytes mismatch: " + label)
    return q, raw


def read_json(root, ref, label):
    _, data = checked_file(root, ref, label)
    try:
        obj = json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ValueError("Unparseable original JSON: " + label) from exc
    need(isinstance(obj, dict), "Original JSON must be object: " + label)
    return obj


def verify_sig(root, public_ref, signature_ref, statement_ref):
    public, public_bytes = checked_file(root, public_ref, "public key")
    sig, _ = checked_file(root, signature_ref, "detached signature")
    statement, _ = checked_file(root, statement_ref, "signed statement")
    need(public.suffix.lower() == ".pem" and sig.suffix.lower() == ".sig"
         and statement.suffix.lower() == ".json", "Wrong signature carrier types")
    need(b"BEGIN PUBLIC KEY" in public_bytes and b"PRIVATE KEY" not in public_bytes,
         "Public signature key must not contain private credentials")
    try:
        check = subprocess.run(
            ["openssl", "dgst", "-sha256", "-verify", str(public),
             "-signature", str(sig), str(statement)],
            capture_output=True, text=True, check=False, timeout=8
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError("Local OpenSSL verification unavailable") from exc
    need(check.returncode == 0 and "Verified OK" in check.stdout,
         "Detached cryptographic signature did not verify")
    # Key bytes distinguish cryptographic identities, not people.
    return hash_bytes(public_bytes)


def validate(root, private_original=None):
    root = Path(root).absolute()
    need(root.is_dir() and not root.is_symlink(), "Local bundle folder missing/symlinked")
    root = root.resolve()
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    need(manifest.get("schema") == SCHEMA, "Wrong independent record schema")
    need(manifest.get("releaseAuthorized") is False and
         manifest.get("classification") == "PRIVATE_CUSTODIAL_REVIEW",
         "This private checker cannot confer release permission")
    need(manifest.get("independentHumanWitnessStatus") == "NOT_AUTHENTICATED",
         "Human independence cannot be self-attested into existence")
    frozen = manifest.get("originalFrozenSHA256")
    need(isinstance(frozen, str) and HEX.fullmatch(frozen), "Missing original frozen identity")
    original_checked = False
    if private_original:
        orig = Path(private_original).absolute()
        need(orig.is_file() and not orig.is_symlink(), "Original frozen object unavailable")
        need(orig.stat().st_size <= 1_000_000_000, "Frozen object too large for this checker")
        h = hashlib.sha256()
        with orig.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        need(h.hexdigest() == frozen, "Actual frozen original differs from signed source identity")
        original_checked = True
    challenge_ref = manifest.get("challenge")
    challenge = read_json(root, challenge_ref, "frozen challenge")
    need(challenge.get("schema") == "va-witness-challenge/1.0",
         "Challenge must use fixed schema")
    challenge_id = challenge.get("challengeId")
    need(isinstance(challenge_id, str) and IDENT.fullmatch(challenge_id),
         "Missing immutable challenge ID")
    need(challenge.get("originalFrozenSHA256") == frozen,
         "Challenge targets a different source")
    routes = challenge.get("declaredRoutes")
    need(isinstance(routes, list) and routes and len(routes) <= 20
         and all(isinstance(r, str) and IDENT.fullmatch(r) for r in routes)
         and len(routes) == len(set(routes)), "Declared effect routes missing/duplicate")
    cases = manifest.get("cases")
    need(isinstance(cases, list) and 3 <= len(cases) <= MAX_CASES, "No bounded three-control trial set")
    identities = set()
    seen_cids, obs_types, observed_negative_routes = set(), set(), set()
    public_keys, observer_to_keys = {}, {}
    prior_cases = {}
    witness_packets = 0
    used_measurements = set()
    for item in cases:
        need(isinstance(item, dict), "Missing case carrier")
        cid, kind = item.get("caseId"), item.get("kind")
        need(isinstance(cid, str) and IDENT.fullmatch(cid) and cid not in seen_cids,
             "Duplicate/invalid case ID")
        seen_cids.add(cid)
        need(kind in CASES, "Unknown original control class")
        obs_types.add(kind)
        candidate = item.get("candidateId")
        need(isinstance(candidate, str) and IDENT.fullmatch(candidate),
             "Original candidate identity missing")
        cond = item.get("governingConditionSHA256")
        need(isinstance(cond, str) and HEX.fullmatch(cond),
             "Original condition digest missing")
        route = item.get("route")
        need(route in routes, "Case effect route undeclared in challenge")
        decision = item.get("decision")
        need(decision == ("EXECUTE" if kind == "ALLOW" else "REFUSE"),
             "Positive or denied control incorrectly classified")
        if kind == "CHANGED":
            original = prior_cases.get(item.get("changedFrom"))
            need(original is not None and original["kind"] == "ALLOW",
                 "Changed-condition original ALLOW case missing or ordered after change")
            need(original["candidate"] == candidate and original["condition"] != cond,
                 "Changed-condition must vary condition, not candidate")
        receipt = read_json(root, item.get("receipt"), "original receipt")
        need(receipt.get("caseId") == cid and receipt.get("candidateId") == candidate
             and receipt.get("decision") == decision and
             receipt.get("governingConditionSHA256") == cond,
             "Source receipt and case identity disagree")
        receipt_digest = item["receipt"]["sha256"]
        witnesses = item.get("witnesses")
        need(isinstance(witnesses, list) and len(witnesses) == 2,
             "Exactly two separate signed witness sources per case required")
        case_keys, case_observers = set(), set()
        for w in witnesses:
            need(isinstance(w, dict), "Witness carrier missing")
            statement_ref = w.get("statement")
            stmt = read_json(root, statement_ref, "signed witness statement")
            need(stmt.get("schema") == "va-independent-effect-statement/1.0",
                 "Unknown independent observation format")
            observer = stmt.get("observerId")
            need(isinstance(observer, str) and IDENT.fullmatch(observer) and
                 observer not in case_observers, "Duplicate/missing claimed observer")
            case_observers.add(observer)
            key_fp = verify_sig(root, w.get("publicKey"), w.get("signature"), statement_ref)
            need(key_fp not in case_keys, "Both witness statements use same cryptographic key")
            case_keys.add(key_fp)
            if key_fp in public_keys:
                need(public_keys[key_fp] == observer, "One key relabeled as another person")
            public_keys[key_fp] = observer
            if observer in observer_to_keys:
                need(observer_to_keys[observer] == key_fp, "One observer rotates identity key without declared requalification")
            observer_to_keys[observer] = key_fp
            need(stmt.get("caseId") == cid and stmt.get("candidateId") == candidate,
                 "Signed statement bound to another candidate or case")
            need(stmt.get("challengeSHA256") == challenge_ref["sha256"]
                 and stmt.get("originalFrozenSHA256") == frozen
                 and stmt.get("originalReceiptSHA256") == receipt_digest
                 and stmt.get("governingConditionSHA256") == cond,
                 "Signed statement not bound to the identical original/challenge/receipt")
            need(stmt.get("declaredRoute") == route and stmt.get("challengeId") == challenge_id,
                 "Signed statement route/challenge mismatch")
            expected = kind == "ALLOW"
            need(type(stmt.get("effectObserved")) is bool and stmt["effectObserved"] == expected,
                 "Signed observed effect contradicts bounded positive/negative case")
            need(stmt.get("measurementExternalToDecisionLabel") is True,
                 "Witness source measures only decision label, not protected consequence")
            need(stmt.get("measurementMethod") in METHODS,
                 "Missing instrument/system audit observation class")
            need(isinstance(stmt.get("methodology"), str) and len(stmt["methodology"].strip()) >= 12,
                 "Instrument methodology undisclosed")
            need(stmt.get("independenceDeclaration") ==
                 "I conducted this observation separately; affiliations and conflicts are disclosed.",
                 "Witness self-declaration missing")
            need(isinstance(stmt.get("affiliationAndConflicts"), str) and
                 len(stmt["affiliationAndConflicts"].strip()) >= 3, "Affiliations/conflicts undisclosed")
            meas_ref = stmt.get("measurement")
            measurement_path = meas_ref.get("path") if isinstance(meas_ref, dict) else None
            need(measurement_path not in used_measurements, "Witnesses share a measurement original")
            used_measurements.add(measurement_path)
            measurement = read_json(root, meas_ref, "external measurement")
            need(measurement.get("schema") == "va-external-effect-measurement/1.0"
                 and measurement.get("caseId") == cid
                 and measurement.get("observedRoute") == route
                 and measurement.get("effectObserved") is expected,
                 "Measurement contradicts signed result or route")
            need(measurement.get("observerId") == observer
                 and measurement.get("instrumentId") == stmt.get("instrumentId"),
                 "Claimed effect measurement not attributable to signing observer/instrument")
            need(isinstance(measurement.get("sourceDescription"), str) and
                 len(measurement["sourceDescription"].strip()) >= 12,
                 "No raw measurement source description")
            witness_packets += 1
        if not expected:
            observed_negative_routes.add(route)
        prior_cases[cid] = {"kind": kind, "candidate": candidate, "condition": cond}
    need(CASES.issubset(obs_types), "Positive, refusal and material-change cases required")
    need(len(public_keys) >= 2, "No distinct cryptographic reviewer sources")
    gaps = sorted(set(routes) - observed_negative_routes)
    declared_gaps = manifest.get("unexaminedNegativeRoutes")
    need(declared_gaps == gaps, "Unexamined negative routes not explicitly accounted for")
    return {
        "schema": "va-independent-witness-local-preflight/1.0",
        "result": "SIGNED_RECORDS_INTERNALLY_BOUND_HUMAN_QUALIFICATION_PENDING",
        "casesChecked": len(cases),
        "detachedWitnessSignaturesVerified": witness_packets,
        "uniqueClaimedObserverIds": len(observer_to_keys),
        "uniquePublicKeys": len(public_keys),
        "frozenOriginalBytesRechecked": original_checked,
        "changedConditionControlsPresent": True,
        "negativeEffectRoutesDeclared": sorted(observed_negative_routes),
        "knownUnexaminedNegativeRoutes": gaps,
        "declaredRouteCoverageComplete": not gaps,
        "humanWitnessIndependenceAuthenticated": False,
        "externalConsequencesIndependentlyValidatedByThisTool": False,
        "sourceEffectInstrumentsQualifiedByThisTool": False,
        "originalFreezeChronologyAuthenticated": False,
        "nativeV12EvidenceAutomaticallyPromoted": False,
        "publicationAuthorized": False,
        "note": "Detached signatures prove control of the supplied public keys over the original statement bytes, not that the keys belong to independent qualified people or that recorded effects are real. Human review must authenticate custody, methods, raw independent sensing, conflicts, routes and lawful release."
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--packet", required=True, help="Private local evidence packet directory")
    p.add_argument("--original", help="Optional actual frozen source file to compare with declared SHA-256")
    p.add_argument("--out", help="Private report path outside original source packet; refuses overwrite")
    args = p.parse_args()
    try:
        report = validate(args.packet, args.original)
        if args.out:
            dest = Path(args.out).absolute()
            need(not dest.is_symlink() and not dest.exists(), "Output exists or is symlink")
            need(not dest.resolve().is_relative_to(Path(args.packet).resolve()),
                 "Private report must be outside input packet")
            fd = os.open(str(dest), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
                f.write("\n")
        print(json.dumps(report, indent=2))
    except (ValueError, KeyError, TypeError, OSError, UnicodeError, json.JSONDecodeError) as err:
        p.exit(2, "REFUSED: " + str(err) + "\n")


if __name__ == "__main__":
    main()
