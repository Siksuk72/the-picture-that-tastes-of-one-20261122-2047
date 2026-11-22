#!/usr/bin/env python3
"""The picture that tastes of one ingredient.

Entry for make.fun competition the-picture-that-tastes-of-one-20261122-2047.

The program ships one picture of food — a single ingredient, golden
honeycomb with honey dripping — as the bundled asset ``entry.png`` and
writes it to ``/output/entry.png``.  No network, no randomness, no
model calls: the output is byte-identical on every run.

Gate (from the competition rules):
  * /output/entry.png is a whole PNG or JPEG
  * at most 1,048,576 bytes
  * at most 1024 by 1024 pixels
"""

import os
import shutil
import struct
import sys

MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024
ASSET_NAME = "entry.png"
OUTPUT_PATH = "/output/entry.png"


def png_dimensions(path):
    """Return (width, height) of a PNG file, or None if not a PNG."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if header[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    asset = os.path.join(here, ASSET_NAME)

    if not os.path.isfile(asset):
        print(f"missing bundled image: {asset}", file=sys.stderr)
        return 1

    size = os.path.getsize(asset)
    if size > MAX_BYTES:
        print(f"bundled image too large: {size} bytes", file=sys.stderr)
        return 1

    dimensions = png_dimensions(asset)
    if dimensions is None:
        print("bundled image is not a PNG", file=sys.stderr)
        return 1
    width, height = dimensions
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        print(f"bundled image too big: {width}x{height}", file=sys.stderr)
        return 1

    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(asset, OUTPUT_PATH)
    os.chmod(OUTPUT_PATH, 0o644)

    # Confirm what landed is exactly what was checked above
    # (byte-identical copy: same size and same dimensions).
    written = os.path.getsize(OUTPUT_PATH)
    if written != size or png_dimensions(OUTPUT_PATH) != dimensions:
        print("output verification failed", file=sys.stderr)
        return 1
    print(f"wrote {OUTPUT_PATH}: {width}x{height} PNG, {size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
