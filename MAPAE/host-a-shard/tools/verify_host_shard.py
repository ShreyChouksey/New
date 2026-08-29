#!/usr/bin/env python3
"""Verify an exact MAPAE Host-a-Shard TXT file locally or over HTTPS."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

ADDRESS_RE = re.compile(r"^bc1q[023456789acdefghjklmnpqrstuvwxyz]{38}$")


def read_bytes(source: str) -> bytes:
    if source.startswith(("https://", "http://")):
        request = urllib.request.Request(
            source,
            headers={"User-Agent": "MAPAE-Shard-Verifier/1.0"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status != 200:
                raise RuntimeError(f"HTTP status {response.status}")
            return response.read()
    return Path(source).read_bytes()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="local path or public HTTP(S) URL")
    parser.add_argument("expected_sha256", help="expected lowercase SHA-256")
    args = parser.parse_args()

    data = read_bytes(args.source)
    digest = hashlib.sha256(data).hexdigest()
    lines = data.decode("ascii").splitlines()

    problems: list[str] = []
    if digest != args.expected_sha256.lower():
        problems.append(f"SHA-256 mismatch: got {digest}")
    if not data.endswith(b"\n"):
        problems.append("missing final LF")
    if len(lines) != 100:
        problems.append(f"expected 100 lines, got {len(lines)}")

    invalid = [
        (line_number, line)
        for line_number, line in enumerate(lines, start=1)
        if not ADDRESS_RE.fullmatch(line)
    ]
    if invalid:
        problems.append(f"{len(invalid)} malformed address line(s)")
    if len(set(lines)) != len(lines):
        problems.append("duplicate address inside shard")

    print(f"bytes={len(data)}")
    print(f"lines={len(lines)}")
    print(f"sha256={digest}")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    print("PASS: exact MAPAE shard verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
