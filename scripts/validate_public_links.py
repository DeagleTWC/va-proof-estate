#!/usr/bin/env python3
"""Check internal public-site and Markdown links, without fetching remote content.

Validates published navigation, not native True Zero/NEW-K mathematics.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOC_EXTENSIONS = {".md", ".html"}
HTTP_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript", "blob"}
INLINE_LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\((<[^>\n]+>|[^\s)]+)(?:\s+[^)]+)?\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)", re.MULTILINE)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])


def remove_fenced_code(text):
    result = []
    fence = None
    for line in text.splitlines():
        match = FENCE.match(line)
        if match:
            delim = match.group(1)
            if fence is None:
                fence = (delim[0], len(delim))
            elif delim[0] == fence[0] and len(delim) >= fence[1]:
                fence = None
            result.append("")
        else:
            result.append("" if fence else line)
    return "\n".join(result)


def documentation_files(root):
    try:
        raw = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"])
        paths = [root / x.decode("utf-8") for x in raw.split(b"\0") if x]
    except (OSError, subprocess.CalledProcessError):
        paths = list(root.rglob("*"))
    return sorted(p for p in paths if p.is_file() and p.suffix.lower() in DOC_EXTENSIONS
                  and not any(x in {".git", "node_modules"} for x in p.parts))


def inspect(root=ROOT, scope=None):
    root = Path(root).resolve()
    errors = []
    cache = {}
    docs = scope if scope is not None else documentation_files(root)
    for path in docs:
        path = Path(path)
        try:
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{path}: unreadable document: {exc}")
            continue
        if path.suffix.lower() == ".html":
            parser = LinkParser()
            parser.feed(raw)
            links = parser.links
        else:
            clean = remove_fenced_code(raw)
            links = [x.group(1).strip("<>") for x in INLINE_LINK.finditer(clean)]
            links += [x.group(1).strip("<>") for x in REFERENCE_LINK.finditer(clean)]
        for ref in links:
            if not ref or ref.startswith(("{{", "{%", "${")):
                continue
            try:
                url = urlsplit(ref)
            except ValueError:
                errors.append(f"{path.relative_to(root)}: malformed URL {ref!r}")
                continue
            if url.scheme.lower() in HTTP_SCHEMES or url.netloc or ref.startswith("//"):
                continue
            if url.scheme:
                continue
            if url.path:
                decoded = unquote(url.path)
                if "\x00" in decoded:
                    errors.append(f"{path.relative_to(root)}: null byte in URL")
                    continue
                if decoded.startswith("/va-proof-estate/"):
                    target = root / decoded[len("/va-proof-estate/"):]
                elif decoded == "/va-proof-estate/" or decoded == "/":
                    target = root / "index.html"
                elif decoded.startswith("/"):
                    # Repository is served at /va-proof-estate; other absolute paths are external-root.
                    continue
                else:
                    target = path.parent / decoded
                target = target.resolve()
                if not target.is_relative_to(root):
                    errors.append(f"{path.relative_to(root)}: link escapes repository: {ref}")
                    continue
                if target.is_dir():
                    target = target / "index.html"
                if not target.is_file():
                    errors.append(f"{path.relative_to(root)}: missing linked file: {ref}")
                    continue
            else:
                target = path
            if url.fragment and target.suffix.lower() == ".html":
                if target not in cache:
                    try:
                        dest = LinkParser()
                        dest.feed(target.read_text(encoding="utf-8"))
                        cache[target] = dest.ids
                    except (OSError, UnicodeDecodeError) as exc:
                        errors.append(f"{path.relative_to(root)}: unreadable linked HTML: {exc}")
                        continue
                if unquote(url.fragment) not in cache[target]:
                    errors.append(f"{path.relative_to(root)}: missing HTML anchor: {ref}")
    return errors


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    args = p.parse_args()
    faults = inspect(args.root)
    for fault in faults:
        print("LINK ERROR:", fault)
    print(f"PUBLIC LINK AUDIT: {len(faults)} error(s)")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
