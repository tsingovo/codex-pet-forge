from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from pet_common import ATLAS_H, ATLAS_W, CELL_H, CELL_W, USED_COUNTS, register_cells_to_safe_box, save_lossless


def main() -> None:
    ap = argparse.ArgumentParser(description="Assemble nine approved Codex Desktop row strips")
    ap.add_argument("--rows-dir", required=True)
    ap.add_argument("--output", required=True, help="Lossless WebP output")
    ap.add_argument("--png-output")
    args = ap.parse_args()

    rows_dir = Path(args.rows_dir).expanduser().resolve()
    atlas = Image.new("RGBA", (ATLAS_W, ATLAS_H), (0, 0, 0, 0))
    for row, count in enumerate(USED_COUNTS):
        path = rows_dir / f"row-{row:02d}.png"
        if not path.is_file():
            raise SystemExit(f"missing approved row: {path}")
        strip = Image.open(path).convert("RGBA")
        expected = (count * CELL_W, CELL_H)
        if strip.size != expected:
            raise SystemExit(f"row {row} must be {expected[0]}x{expected[1]}, got {strip.width}x{strip.height}")
        atlas.alpha_composite(strip, (0, row * CELL_H))
    atlas = register_cells_to_safe_box(atlas)
    save_lossless(atlas, Path(args.png_output).resolve() if args.png_output else None, Path(args.output).resolve())
    print(f"assembled 9 approved desktop rows -> {args.output}")


if __name__ == "__main__":
    main()
