from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from pet_common import CELL_H, CELL_W, SIDE_SAFE_PADDING, USED_COUNTS, save_lossless


def parse_row_scale(value: str) -> tuple[int, float]:
    try:
        row_text, scale_text = value.split("=", 1)
        row, scale = int(row_text), float(scale_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected ROW=SCALE, for example 6=1.14") from exc
    if row < 0 or row >= len(USED_COUNTS):
        raise argparse.ArgumentTypeError(f"row must be 0-{len(USED_COUNTS) - 1}")
    if not 0.75 <= scale <= 1.25:
        raise argparse.ArgumentTypeError("scale must be within 0.75-1.25")
    return row, scale


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Apply an explicitly reviewed horizontal model-width correction to complete action rows."
    )
    ap.add_argument("atlas")
    ap.add_argument("--row-scale", action="append", type=parse_row_scale, required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--png-output")
    args = ap.parse_args()

    source = Image.open(args.atlas).convert("RGBA")
    if source.size != (8 * CELL_W, 9 * CELL_H):
        raise SystemExit(f"expected 1536x1872 Desktop atlas, got {source.size}")
    result = source.copy()
    applied: list[str] = []
    for row, scale in args.row_scale:
        for column in range(USED_COUNTS[row]):
            box = (column * CELL_W, row * CELL_H, (column + 1) * CELL_W, (row + 1) * CELL_H)
            cell = source.crop(box)
            bbox = cell.getchannel("A").getbbox()
            if bbox is None:
                raise SystemExit(f"row {row} column {column} is empty")
            sprite = cell.crop(bbox)
            width = round(sprite.width * scale)
            max_width = CELL_W - 2 * SIDE_SAFE_PADDING
            if width > max_width:
                raise SystemExit(
                    f"row {row} column {column} would become {width}px wide, exceeding {max_width}px safe width"
                )
            resized = sprite.resize((max(1, width), sprite.height), Image.Resampling.LANCZOS)
            repaired = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
            repaired.alpha_composite(resized, ((CELL_W - resized.width) // 2, bbox[1]))
            result.paste((0, 0, 0, 0), box)
            result.alpha_composite(repaired, (column * CELL_W, row * CELL_H))
        applied.append(f"{row}={scale:.4f}")

    save_lossless(
        result,
        Path(args.png_output).expanduser().resolve() if args.png_output else None,
        Path(args.output).expanduser().resolve(),
    )
    print(f"applied reviewed row width corrections: {', '.join(applied)}")


if __name__ == "__main__":
    main()
