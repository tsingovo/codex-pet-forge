from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from pet_common import CELL_H, CELL_W


RUNTIME_COUNTS = (6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)
STATE_NAMES = (
    "idle", "drag-right", "drag-left", "greeting", "hover-curiosity", "failed",
    "waiting", "thinking", "review", "look-a", "look-b",
)


def composite(frame: Image.Image) -> Image.Image:
    background = Image.new("RGBA", frame.size, (238, 241, 245, 255))
    background.alpha_composite(frame.convert("RGBA"))
    return background.convert("RGB")


def main() -> None:
    ap = argparse.ArgumentParser(description="Render per-row motion GIFs at an explicit QA frame rate")
    ap.add_argument("atlas")
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--fps", type=float, default=8.0)
    ap.add_argument("--loops", type=int, default=0, help="GIF loop count; 0 means infinite")
    args = ap.parse_args()
    if args.fps <= 0:
        raise SystemExit("fps must be positive")

    atlas = Image.open(Path(args.atlas).expanduser().resolve()).convert("RGBA")
    if atlas.size != (8 * CELL_W, 11 * CELL_H):
        raise SystemExit(f"expected 1536x2288 atlas, got {atlas.width}x{atlas.height}")
    out = Path(args.output_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    duration = max(20, round(1000 / args.fps))
    for row, count in enumerate(RUNTIME_COUNTS):
        frames = [
            composite(atlas.crop((column * CELL_W, row * CELL_H, (column + 1) * CELL_W, (row + 1) * CELL_H)))
            for column in range(count)
        ]
        target = out / f"row-{row:02d}-{STATE_NAMES[row]}.gif"
        frames[0].save(target, save_all=True, append_images=frames[1:], duration=duration, loop=args.loops, disposal=2)
    print(f"wrote 11 motion previews at {args.fps:g} fps -> {out}")


if __name__ == "__main__":
    main()
