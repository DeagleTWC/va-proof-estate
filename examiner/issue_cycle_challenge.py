#!/usr/bin/env python3
"""Issue a fresh synthetic challenge against a prior unedited public GitHub freeze comment."""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from independent_challenge import check_freeze, check_challenge, issue, save, sha

REPO = "DeagleTWC/va-proof-estate"
SCHEMA = "DEAGLE-ISSUANCE-1"
CEILING = "GITHUB-ANCHORED SYNTHETIC CHALLENGE ONLY; NOT EXTERNAL EFFECT OR NATIVE V.A."


def parse_freeze(body):
    if not isinstance(body, str) or len(body.encode("utf8")) > 12000:
        raise ValueError("missing or oversized public freeze comment")
    try:
        freeze = json.loads(body.strip())
    except (ValueError, TypeError) as exc:
        raise ValueError("freeze comment must contain only the complete JSON object") from exc
    if type(freeze) is not dict:
        raise ValueError("freeze must be JSON object")
    check_freeze(freeze)
    return freeze


def utc(raw):
    if not isinstance(raw, str):
        raise ValueError("missing GitHub timestamp")
    try:
        d = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid GitHub timestamp") from exc
    if d.tzinfo is None:
        raise ValueError("timestamp requires explicit timezone")
    return d.astimezone(timezone.utc)


def issue_from_comment(comment, actor, run_id, attempt, commit, family, rounds, now=None):
    if type(comment) is not dict:
        raise ValueError("GitHub comment must be JSON object")
    cid = comment.get("id")
    if type(cid) is not int or cid < 1:
        raise ValueError("invalid issue comment ID")
    expected_issue = "https://api.github.com/repos/" + REPO + "/issues/1"
    expected_comment = "https://github.com/" + REPO + "/issues/1#issuecomment-" + str(cid)
    if comment.get("issue_url") != expected_issue or comment.get("html_url") != expected_comment:
        raise ValueError("freeze comment not on Cycle 001")
    author = (comment.get("user") or {}).get("login")
    if not isinstance(author, str) or not author or not actor or actor.casefold() == author.casefold():
        raise ValueError("issuer must be distinct GitHub account from freeze author")
    created, edited = utc(comment.get("created_at")), utc(comment.get("updated_at"))
    if created != edited:
        raise ValueError("edited freeze comment refused")
    now = now or datetime.now(timezone.utc)
    if created >= now:
        raise ValueError("freeze not published before challenge")
    if type(run_id) is not int or run_id < 1 or type(attempt) is not int or attempt < 1:
        raise ValueError("invalid Actions run")
    if not isinstance(commit, str) or re.fullmatch("[0-9a-f]{40}", commit) is None:
        raise ValueError("invalid source commit")
    frozen = parse_freeze(comment.get("body"))
    challenge = issue(frozen, family, rounds)
    check_challenge(frozen, challenge)
    snapshot = {"id": cid, "issue_url": expected_issue, "html_url": expected_comment,
                "user_login": author, "created_at": comment["created_at"],
                "updated_at": comment["updated_at"], "body": comment["body"]}
    receipt = {
        "schema": SCHEMA, "repo": REPO, "cycle_issue": 1,
        "comment_id": cid, "comment_url": expected_comment, "comment_author": author,
        "comment_body_sha256": hashlib.sha256(comment["body"].encode()).hexdigest(),
        "freeze_sha256": frozen["freeze_sha256"],
        "challenge_sha256": challenge["challenge_sha256"],
        "fixture_sha256": challenge["fixture_sha256"],
        "issuer": actor, "run_id": run_id, "run_attempt": attempt,
        "head_sha": commit, "issued_at": now.isoformat(),
        "freeze_created_at": created.isoformat(),
        "standing": CEILING, "authenticated_independent_examiner": False,
        "native_VA_execution": False, "physical_KCD_execution": False,
        "challenge_only_no_examination": True,
        "run_identity_requires_external_GitHub_verification": True
    }
    receipt["receipt_sha256"] = sha(receipt)
    return frozen, challenge, receipt, snapshot


def verify(frozen, challenge, receipt, snapshot):
    check_challenge(frozen, challenge)
    if receipt.get("schema") != SCHEMA or receipt.get("receipt_sha256") != sha(
            {k:v for k,v in receipt.items() if k != "receipt_sha256"}):
        raise ValueError("issuance record checksum mismatch")
    if receipt.get("repo") != REPO or receipt.get("cycle_issue") != 1:
        raise ValueError("wrong issuance cycle")
    if (receipt.get("freeze_sha256") != frozen["freeze_sha256"]
        or receipt.get("challenge_sha256") != challenge["challenge_sha256"]
        or receipt.get("fixture_sha256") != challenge["fixture_sha256"]):
        raise ValueError("frozen challenge identity mismatch")
    if type(snapshot) is not dict or snapshot.get("id") != receipt.get("comment_id"):
        raise ValueError("snapshot comment mismatch")
    if snapshot.get("html_url") != receipt.get("comment_url") or snapshot.get("user_login") != receipt.get("comment_author"):
        raise ValueError("snapshot author mismatch")
    if snapshot.get("issue_url") != "https://api.github.com/repos/" + REPO + "/issues/1":
        raise ValueError("snapshot issue mismatch")
    if utc(snapshot.get("created_at")) != utc(receipt.get("freeze_created_at")) or utc(snapshot.get("updated_at")) != utc(snapshot.get("created_at")):
        raise ValueError("snapshot chronology mismatch")
    if hashlib.sha256(snapshot["body"].encode()).hexdigest() != receipt.get("comment_body_sha256"):
        raise ValueError("comment body altered")
    if parse_freeze(snapshot["body"]) != frozen:
        raise ValueError("freeze mismatches comment snapshot")
    if utc(receipt.get("issued_at")) <= utc(snapshot["created_at"]):
        raise ValueError("challenge precedes freeze")
    if receipt.get("issuer", "").casefold() == snapshot["user_login"].casefold():
        raise ValueError("no issuer separation")
    for flag in ("authenticated_independent_examiner", "native_VA_execution", "physical_KCD_execution"):
        if receipt.get(flag) is not False:
            raise ValueError("unauthorized proof promotion")
    if receipt.get("standing") != CEILING or receipt.get("challenge_only_no_examination") is not True:
        raise ValueError("incorrect evidence standing")
    return {"status": "LOCAL_ISSUANCE_PACKET_VALID", "challenge_sha256": challenge["challenge_sha256"],
            "independent_examiner": False, "native_VA_execution": False}


def main():
    parser = argparse.ArgumentParser(description="GitHub-anchored post-freeze synthetic challenge issuer")
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("issue")
    for arg in ("comment-json", "actor", "run-id", "attempt", "commit", "family", "rounds", "out"):
        p.add_argument("--" + arg, required=True)
    v = sub.add_parser("verify")
    v.add_argument("--dir", required=True)
    args = parser.parse_args()
    try:
        if args.action == "issue":
            comment = json.loads(Path(args.comment_json).read_text(encoding="utf8"))
            a, b, c, d = issue_from_comment(comment, args.actor, int(args.run_id),
                                             int(args.attempt), args.commit, args.family,
                                             int(args.rounds))
            dest = Path(args.out)
            dest.mkdir(parents=True, exist_ok=True)
            for name, value in (("freeze.json", a), ("challenge.json", b),
                                ("issuance.json", c), ("comment-snapshot.json", d)):
                save(dest / name, value)
            result = verify(a, b, c, d)
            note = ("Cycle 001 fresh challenge issued.\n\nFreeze: " + a["freeze_sha256"] +
                    "\n\nChallenge: " + b["challenge_sha256"] +
                    "\n\nFamily: " + b["family"] + "; rounds: " + str(b["rounds"]) +
                    "; seed: " + str(b["seed"]) +
                    "\n\nGitHub Actions artifact: https://github.com/" + REPO +
                    "/actions/runs/" + str(args.run_id) +
                    "\n\nThis is only issuance of a synthetic challenge, not independent evidence or native V.A. testing.\n")
            (dest / "issue-reply.md").write_text(note, encoding="utf8")
        else:
            dest = Path(args.dir)
            result = verify(*(json.loads((dest / name).read_text(encoding="utf8")) for name in
                              ("freeze.json", "challenge.json", "issuance.json", "comment-snapshot.json")))
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, AssertionError) as exc:
        print("ISSUANCE REFUSED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
