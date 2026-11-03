#!/usr/bin/env python3
"""Validate distinct static social PNGs and their declared public share metadata.

This validates presentation media, not a native V.A. execution or scientific standing.
"""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://deagletwc.github.io/va-proof-estate/"
PAGES = {
    "consequence-challenge.html": "challenge/authority-1200x630.png",
    "challenge/standing.html": "challenge/standing-1200x630.png",
    "challenge/authority.html": "challenge/authority-1200x630.png",
    "challenge/alternate-route.html": "challenge/alternate-route-1200x630.png",
}


class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = {}

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return
        attributes = dict(attrs)
        key = attributes.get("property") or attributes.get("name")
        if key:
            self.tags[key] = attributes.get("content")


def inspect_png(image_path: Path):
    raw = image_path.read_bytes()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n", f"{image_path}: invalid PNG signature"
    pos = 8
    chunks = []
    while pos < len(raw):
        assert pos + 12 <= len(raw), f"{image_path}: truncated PNG chunk"
        length = struct.unpack(">I", raw[pos:pos+4])[0]
        name = raw[pos+4:pos+8]
        assert len(raw) >= pos + 12 + length, f"{image_path}: truncated PNG body"
        body = raw[pos+8:pos+8+length]
        checksum = struct.unpack(">I", raw[pos+8+length:pos+12+length])[0]
        assert checksum == zlib.crc32(name + body) & 0xffffffff, f"{image_path}: CRC mismatch"
        chunks.append((name, body))
        pos += length + 12
    assert pos == len(raw)
    assert chunks[0][0] == b"IHDR" and chunks[-1][0] == b"IEND"
    w,h,depth,color_type,compression,filter_type,interlace = struct.unpack(">IIBBBBB",chunks[0][1])
    assert (w,h,depth,color_type,compression,filter_type,interlace)==(1200,630,4,3,0,0,0), f"{image_path}: incorrect preview format"
    assert any(t == b"PLTE" for t,_ in chunks), f"{image_path}: palette absent"
    data = b"".join(body for name,body in chunks if name == b"IDAT")
    decompressed = zlib.decompress(data)
    assert len(decompressed) == (w//2+1)*h, f"{image_path}: malformed image payload"
    assert all(decompressed[row*(w//2+1)] == 0 for row in range(h)), f"{image_path}: unexpected scanline filter"
    assert len(set(decompressed)) > 8, f"{image_path}: placeholder or empty preview image"
    return hashlib.sha256(raw).hexdigest()


def validate():
    errors = []
    images = {}
    for html_file, image_file in PAGES.items():
        try:
            page = (ROOT / html_file).read_text(encoding="utf-8")
            parser = MetaParser()
            parser.feed(page)
            for tag in ("og:image","og:image:secure_url","twitter:image"):
                if parser.tags.get(tag) != BASE + image_file:
                    raise ValueError(f"{html_file}: {tag} does not reference expected image")
            if parser.tags.get("og:image:type") != "image/png":
                raise ValueError(f"{html_file}: image type is not PNG")
            if parser.tags.get("og:image:width") != "1200" or parser.tags.get("og:image:height") != "630":
                raise ValueError(f"{html_file}: OG dimensions are not 1200x630")
            if not parser.tags.get("og:image:alt") or parser.tags.get("twitter:image:alt") != parser.tags.get("og:image:alt"):
                raise ValueError(f"{html_file}: accessibility descriptions missing or mismatched")
            images[image_file] = inspect_png(ROOT/image_file)
        except (OSError, ValueError, AssertionError) as exc:
            errors.append(str(exc))
    if len(images) != 3 or len(set(images.values())) != 3:
        errors.append("Three distinct challenge image identities were not established")
    return errors


if __name__ == "__main__":
    problems = validate()
    for problem in problems:
        print("SOCIAL MEDIA ASSET ERROR:", problem)
    if problems:
        raise SystemExit(1)
    print("PASS: three distinct 1200x630 PNG previews, byte-level CRC/decompression and canonical share metadata")
