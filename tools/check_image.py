#!/usr/bin/env python3
"""Objective, machine-checkable QA for a generated illustration.

Usage:
  python tools/check_image.py <image.png> [--aspect 16:9] [--min-white 0.35]

Checks (objective — they complement, not replace, the human/vision QA in
references/qa-checklist.md):
  - aspect ratio matches the target (default 16:9), within a relative tolerance
  - fraction of near-white background pixels >= --min-white (default 0.35)
    (needs Pillow; the check is SKIPPED with a notice if Pillow is absent)

Exit: 0 = all checks pass; 1 = a check failed; 2 = usage / file error.

The label-text check (did the handwritten words render correctly?) stays a
runtime vision/OCR read-back by the agent — see references/qa-checklist.md —
because that needs to compare against the *intended* labels, which only the
generating agent knows.
"""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path


def png_size(path: Path) -> tuple[int, int]:
    """Read width/height from the PNG IHDR chunk (stdlib only)."""
    with path.open("rb") as f:
        header = f.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file (bad signature)")
    if len(header) < 24:
        raise ValueError(f"file too short to be a valid PNG ({len(header)} bytes)")
    width, height = struct.unpack(">II", header[16:24])
    if width == 0 or height == 0:
        raise ValueError("PNG reports a zero dimension")
    return width, height


def white_fraction(path: Path, threshold: int = 245) -> float | None:
    """Fraction of pixels with R,G,B all >= threshold. None if Pillow is unavailable."""
    try:
        from PIL import Image
    except ImportError:
        return None
    with Image.open(path) as im:
        if im.mode in ("RGBA", "LA", "PA"):
            # composite transparency against WHITE (Pillow's default is black), so a
            # transparent-background PNG isn't miscounted as all-white -> false PASS
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.convert("RGBA").split()[-1])
            rgb = bg
        else:
            rgb = im.convert("RGB")
        total = rgb.width * rgb.height
        if total == 0:
            return 0.0
        white = sum(
            1 for r, g, b in rgb.getdata()
            if r >= threshold and g >= threshold and b >= threshold
        )
    return white / total


def parse_aspect(s: str) -> float:
    a, sep, b = s.partition(":")
    if not sep:
        raise ValueError(f"aspect must look like W:H, got {s!r}")
    try:
        num, denom = int(a), int(b)
    except ValueError:
        raise ValueError(f"aspect W and H must be integers, got {s!r}")
    if denom == 0:
        raise ValueError(f"aspect denominator must be non-zero, got {s!r}")
    return num / denom


def main() -> int:
    ap = argparse.ArgumentParser(description="Objective QA for a generated illustration.")
    ap.add_argument("image", type=Path)
    ap.add_argument("--aspect", default="16:9", help="target aspect ratio W:H (default 16:9)")
    ap.add_argument("--min-white", type=float, default=0.35, help="min near-white fraction (default 0.35)")
    ap.add_argument("--tol", type=float, default=0.04, help="aspect relative tolerance (default 0.04)")
    args = ap.parse_args()

    if not args.image.exists():
        print(f"ERROR: {args.image} does not exist", file=sys.stderr)
        return 2
    try:
        w, h = png_size(args.image)
        target = parse_aspect(args.aspect)
    except (OSError, ValueError, struct.error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    failures: list[str] = []

    actual = w / h
    if abs(actual - target) / target > args.tol:
        failures.append(f"aspect {w}x{h} = {actual:.3f} differs from {args.aspect} ({target:.3f}) by > {args.tol:.0%}")
    else:
        print(f"OK   aspect {w}x{h} = {actual:.3f} ~= {args.aspect}")

    wf = white_fraction(args.image)
    skipped = wf is None
    if skipped:
        print("SKIP white-space ratio (Pillow not installed; `pip install pillow` to enable)")
    elif wf < args.min_white:
        failures.append(f"white-space {wf:.0%} < required {args.min_white:.0%} (frame too full)")
    else:
        print(f"OK   white-space {wf:.0%} >= {args.min_white:.0%}")

    if failures:
        for f in failures:
            print(f"FAIL {f}")
        return 1
    print("PASS (whitespace check skipped — install Pillow for the full gate)" if skipped else "PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
