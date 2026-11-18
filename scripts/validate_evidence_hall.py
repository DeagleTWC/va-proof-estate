"""Verify the source and claim boundary of the static public Evidence Hall."""

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


EXPECTED = ("pre-effect", "authority", "scope", "changed-condition", "continuance")


class HallParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = {}
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("data-exhibit"):
            self.sections[attrs["data-exhibit"]] = attrs.get("data-standing")
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])


def validate_hall(repo_root: Path) -> list[str]:
    """Return human-readable errors; fail closed on missing artifacts and promotion."""
    errors = []
    reg_path = repo_root / "proofs/EVIDENCE-HALL-REGISTER.json"
    page_path = repo_root / "evidence-hall.html"
    if not reg_path.is_file() or not page_path.is_file():
        return ["Missing Evidence Hall register or page"]
    try:
        data = json.loads(reg_path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return ["Malformed Evidence Hall register"]
    exhibits = data.get("exhibits", [])
    if not isinstance(exhibits, list) or tuple(x.get("id") for x in exhibits if isinstance(x, dict)) != EXPECTED:
        errors.append("Expected five ordered exhibits")
        return errors
    if data.get("native_v12_run_attached") or data.get("native_independent_reproduction_attached"):
        errors.append("Unqualified native run promotion")
    if data.get("protected_construction_included"):
        errors.append("Protected construction must not be published")
    for exhibit in exhibits:
        if exhibit.get("standing") != "DECLARED" or exhibit.get("native_run_attached") is not False:
            errors.append(f"{exhibit['id']}: unqualified evidence promotion")
        if not isinstance(exhibit.get("sources"), list) or not exhibit["sources"]:
            errors.append(f"{exhibit['id']}: no source carriers")
            continue
        for item in exhibit["sources"]:
            p = item.get("path", "")
            if not isinstance(p, str) or not p.startswith("proofs/") or ".." in Path(p).parts or "://" in p:
                errors.append(f"{exhibit['id']}: nonlocal source {p}")
            elif not (repo_root / p).is_file():
                errors.append(f"{exhibit['id']}: missing original carrier {p}")
    fixture = data.get("fixture", {})
    if fixture.get("standing") != "OBSERVED" or "synthetic mock" not in fixture.get("scope", ""):
        errors.append("Fixture must be OBSERVED only within synthetic mock scope")
    if fixture.get("independent_reproduction") != "NOT ATTESTED":
        errors.append("Fixture independence not attested")
    for field in ("record", "runner", "verifier"):
        path = fixture.get(field, "")
        if not isinstance(path, str) or not path.startswith("proofs/VA-AD-001/") or not (repo_root / path).is_file():
            errors.append(f"Missing local fixture {field}")
    report_path = fixture.get("record", "")
    if isinstance(report_path, str) and (repo_root / report_path).is_file():
        try:
            report = json.loads((repo_root / report_path).read_text(encoding="utf-8"))
            cases = {c["case"]: c for c in report["cases"]}
            expected = {
                "positive-authorized": ("ADMIT", True, False),
                "negative-never-authorized": ("REFUSE", False, True),
                "changed-condition-revoked": ("REFUSE", False, True),
                "negative-stale-evidence": ("REFUSE", False, True),
            }
            for name, (decision, observed, unchanged) in expected.items():
                case = cases.get(name, {})
                if (case.get("decision") != decision or case.get("observed_mock_effect") is not observed
                        or (case.get("before_state_sha256") == case.get("after_state_sha256")) is not unchanged):
                    errors.append(f"{name}: recorded mock observation mismatch")
            if report.get("native_VA_execution") != "NOT TESTED" or report.get("independent_reproduction") != "NOT ATTESTED":
                errors.append("Fixture record scope mismatch")
        except (ValueError, KeyError, TypeError):
            errors.append("Malformed fixture result record")
    html = page_path.read_text(encoding="utf-8")
    parser = HallParser()
    parser.feed(html)
    if parser.sections != {ex["id"]: "DECLARED" for ex in exhibits}:
        errors.append("Displayed exhibits differ from documented evidence statuses")
    expected_links = {s["path"] for ex in exhibits for s in ex["sources"]}
    for required in expected_links:
        if required not in parser.links:
            errors.append(f"Missing source link on page: {required}")
    for href in parser.links:
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc or href.startswith("//"):
            errors.append(f"External Evidence Hall dependency: {href}")
            continue
        if not parsed.path and parsed.fragment:
            continue
        target = unquote(parsed.path)
        if not target or target.startswith("/") or ".." in Path(target).parts:
            errors.append(f"Unsafe Evidence Hall href: {href}")
        elif not (repo_root / target).exists() and target not in ("index.html", "reviewer-route.html"):
            errors.append(f"Broken local Evidence Hall href: {href}")
    return errors


if __name__ == "__main__":
    findings = validate_hall(Path(__file__).resolve().parents[1])
    for finding in findings:
        print(finding, file=sys.stderr)
    raise SystemExit(bool(findings))
