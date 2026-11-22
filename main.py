#!/usr/bin/env python3
"""The picture that tastes of one ingredient.

Writes one image of food — a single ingredient, a glistening chunk of
golden honeycomb with thick amber honey dripping off it, on dark slate
under warm light — to /output/entry.png.

The picture is bundled with this program as ``entry.png`` sitting next
to this file. The program validates the bundled asset, copies it to the
output path, and re-verifies the copy before reporting success.

Rules honoured:
- Python 3 standard library only; no network, no randomness.
- Fully deterministic: the same input always produces the same output.
"""

from __future__ import annotations

import os
import shutil
import struct
import sys

ASSET_NAME = "entry.png"
OUTPUT_PATH = "/output/entry.png"
MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message: str) -> "SystemExit":
    """Print an error to stderr and exit non-zero."""
    print(f"error: {message}", file=sys.stderr)
    return SystemExit(1)


def read_png_dimensions(path: str) -> tuple[int, int]:
    """Return (width, height) parsed from a PNG file's IHDR chunk.

    Raises ValueError on anything that is not a well-formed PNG header.
    """
    with open(path, "rb") as handle:
        header = handle.read(33)
        # A complete PNG ends with the 12-byte IEND chunk; a truncated
        # download or copy would fail this check.
        handle.seek(-12, os.SEEK_END)
        trailer = handle.read(12)
    if len(header) < 33:
        raise ValueError("file too short to be a PNG")
    if header[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file (bad magic bytes)")
    if header[12:16] != b"IHDR":
        raise ValueError("not a PNG file (missing IHDR chunk)")
    width, height = struct.unpack(">II", header[16:24])
    if width == 0 or height == 0:
        raise ValueError("PNG has a zero dimension")
    if trailer != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        raise ValueError("PNG is truncated (missing IEND chunk)")
    return width, height


def validate_png(path: str, label: str) -> tuple[int, int, int]:
    """Check one PNG against the competition gates.

    Returns (width, height, size_bytes). Exits non-zero on any failure.
    """
    if not os.path.isfile(path):
        raise SystemExit(fail(f"{label} not found: {path}"))
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit(
            fail(f"{label} is {size} bytes, over the {MAX_BYTES} byte limit")
        )
    try:
        width, height = read_png_dimensions(path)
    except (OSError, ValueError) as exc:
        raise SystemExit(fail(f"{label} failed PNG validation: {exc}"))
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise SystemExit(
            fail(
                f"{label} is {width}x{height}px, over the "
                f"{MAX_DIMENSION}x{MAX_DIMENSION}px limit"
            )
        )
    return width, height, size


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    asset_path = os.path.join(script_dir, ASSET_NAME)

    # 1. Validate the bundled picture before touching the output.
    width, height, size = validate_png(asset_path, "bundled asset")

    # 2. Make sure the output directory exists, then copy the asset.
    output_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(asset_path, OUTPUT_PATH)
    os.chmod(OUTPUT_PATH, 0o644)

    # 3. Re-verify the written output: size and dimensions must match.
    out_width, out_height, out_size = validate_png(OUTPUT_PATH, "output")
    if (out_width, out_height, out_size) != (width, height, size):
        raise SystemExit(
            fail(
                "output mismatch: expected "
                f"{width}x{height}px / {size} bytes, got "
                f"{out_width}x{out_height}px / {out_size} bytes"
            )
        )

    print(
        f"success: wrote {OUTPUT_PATH} "
        f"({width}x{height}px, {size} bytes) — "
        "one picture of food, a single ingredient: golden honeycomb."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
