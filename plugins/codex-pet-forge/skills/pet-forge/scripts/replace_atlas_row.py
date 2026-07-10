from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image

from pet_common import ATLAS_H, ATLAS_W, CELL_H, CELL_W, USED_COUNTS, chroma_to_alpha, clear_unused_cells, parse_color, save_lossless


def main() -> None:
    ap = argparse.ArgumentParser(description="Replace one row of a Codex v2 atlas")
    ap.add_argument("--base", required=True)
    ap.add_argument("--row", type=int, required=True, choices=range(11))
    ap.add_argument("--strip", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--png-output")
    ap.add_argument("--chroma-key", default="#FF00FF")
    args = ap.parse_args()

    atlas = Image.open(args.base).convert("RGBA")
    if atlas.size != (ATLAS_W, ATLAS_H):
        raise SystemExit(f"base atlas must be {ATLAS_W}x{ATLAS_H}")
    count = USED_COUNTS[args.row]
    strip = Image.open(args.strip).convert("RGBA")
    expected_ratio = (count * CELL_W) / CELL_H
    if abs(strip.width / strip.height - expected_ratio) / expected_ratio > 0.08:
        raise SystemExit(f"strip aspect ratio does not match {count} frames")
    strip = strip.resize((count * CELL_W, CELL_H), Image.Resampling.LANCZOS)
    strip = chroma_to_alpha(strip, parse_color(args.chroma_key))
    y0 = args.row * CELL_H
    atlas.paste((0, 0, 0, 0), (0, y0, ATLAS_W, y0 + CELL_H))
    atlas.alpha_composite(strip, (0, y0))
    clear_unused_cells(atlas)
    save_lossless(atlas, Path(args.png_output) if args.png_output else None, Path(args.output))
    print(f"replaced row {args.row} with {count} frames -> {args.output}")


if __name__ == "__main__":
    main()
