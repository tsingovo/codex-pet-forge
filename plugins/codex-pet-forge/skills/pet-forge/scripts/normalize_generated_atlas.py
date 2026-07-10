from __future__ import annotations

import argparse
import json
from pathlib import Path
from PIL import Image

from pet_common import ATLAS_H, ATLAS_W, CELL_H, CELL_W, USED_COUNTS, chroma_to_alpha, clear_unused_cells, parse_color, save_lossless


def main() -> None:
    ap = argparse.ArgumentParser(description="Normalize a generated Codex Desktop 8x9 pet atlas")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--webp-output")
    ap.add_argument("--chroma-key", default="#FF00FF")
    ap.add_argument("--json-out")
    args = ap.parse_args()

    source = Image.open(args.input).convert("RGBA")
    expected_ratio = ATLAS_W / ATLAS_H
    ratio_error = abs(source.width / source.height - expected_ratio) / expected_ratio
    if ratio_error > 0.04:
        raise SystemExit(f"generated atlas aspect ratio is incompatible: {source.size}")
    resized = source.resize((ATLAS_W, ATLAS_H), Image.Resampling.LANCZOS)
    atlas = chroma_to_alpha(resized, parse_color(args.chroma_key))
    clear_unused_cells(atlas)

    errors = []
    coverage = []
    for row, used in enumerate(USED_COUNTS):
        for col in range(used):
            cell = atlas.crop((col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H))
            visible = sum(1 for a in cell.getchannel("A").getdata() if a > 16)
            coverage.append({"row": row, "column": col, "visiblePixels": visible})
            if visible < 150:
                errors.append(f"required cell {row}:{col} is empty")

    save_lossless(atlas, Path(args.output), Path(args.webp_output) if args.webp_output else None)
    result = {"ok": not errors, "sourceSize": list(source.size), "outputSize": [ATLAS_W, ATLAS_H], "errors": errors, "coverage": coverage}
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
