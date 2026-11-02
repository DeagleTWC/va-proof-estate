#!/usr/bin/env python3
"""Check public static pages for unintended network transmission surfaces.

Conservative static audit only: passing does NOT certify absence of all security bugs.
"""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PAGES = ("index.html", "foundation.html", "end-to-end.html", "reviewer-route.html")
NETWORK_JS = [
    re.compile(pattern, re.I)
    for pattern in (
        r"\bfetch\s*\(",
        r"\bXMLHttpRequest\b",
        r"\bsendBeacon\s*\(",
        r"\bWebSocket\s*\(",
        r"\bEventSource\s*\(",
        r"\bimportScripts\s*\(",
        r"\bnew\s+Image\s*\(",
    )
]


class InspectionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.script_parts = []
        self.inside_script = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "script":
            if attributes.get("src"):
                self.errors.append("externally loaded script element")
            self.inside_script = True
        elif tag in {"iframe", "object", "embed"}:
            self.errors.append(f"embedded active content: {tag}")
        elif tag == "form":
            if attributes.get("action") or attributes.get("method", "").lower() == "post":
                self.errors.append("form has network submission target/method")
        elif tag == "base" and attributes.get("href"):
            self.errors.append("base tag alters navigation and relative URLs")
        elif tag == "meta" and attributes.get("http-equiv", "").lower() == "refresh":
            self.errors.append("automatic document redirect")
        for k, value in attrs:
            if k.lower().startswith("on") and value and re.search(r"\bfetch\s*\(|XMLHttpRequest|sendBeacon", value, re.I):
                self.errors.append("inline handler contains network operation")

    def handle_endtag(self, tag):
        if tag == "script":
            self.inside_script = False

    def handle_data(self, data):
        if self.inside_script:
            self.script_parts.append(data)


def validate(root=ROOT):
    errors = []
    for path in PUBLIC_PAGES:
        try:
            html = (Path(root) / path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{path}: unreadable: {exc}")
            continue
        doc = InspectionParser()
        doc.feed(html)
        errors.extend(f"{path}: {e}" for e in doc.errors)
        scripts = "\n".join(doc.script_parts)
        for pattern in NETWORK_JS:
            if pattern.search(scripts):
                errors.append(f"{path}: outbound runtime primitive matched: {pattern.pattern}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for issue in problems:
            print("PUBLIC SAFETY-SURFACE ISSUE:", issue)
        raise SystemExit(1)
    print("PASS: no external runtime scripts, network submission forms, or known outbound JS primitives in public pages")
    print("Limit: static pattern audit; not a complete security proof of the site or underlying native system")
