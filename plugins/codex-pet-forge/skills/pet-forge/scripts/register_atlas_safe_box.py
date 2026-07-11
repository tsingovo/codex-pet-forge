from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from pet_common import ATLAS_H, ATLAS_W, register_cells_to_safe_box, save_lossless


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Uniformly register every Codex Desktop sprite with head and shoe safety padding"
    )
    parser.add_argument("atlas")
    parser.add_argument("--output", required=True, help="Lossless WebP output")
    parser.add_argument("--png-output")
    args = parser.parse_args()

    with Image.open(Path(args.atlas).expanduser().resolve()) as opened:
        atlas = opened.convert("RGBA")
    if atlas.size != (ATLAS_W, ATLAS_H):
        raise SystemExit(f"atlas must be {ATLAS_W}x{ATLAS_H}, got {atlas.width}x{atlas.height}")
    atlas = register_cells_to_safe_box(atlas)
    save_lossless(
        atlas,
        Path(args.png_output).expanduser().resolve() if args.png_output else None,
        Path(args.output).expanduser().resolve(),
    )
    print(f"registered Desktop safe box -> {args.output}")


if __name__ == "__main__":
    main()
