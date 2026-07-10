from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import median

from PIL import Image, ImageChops

from pet_common import CELL_H, CELL_W, USED_COUNTS


def difference(first: Image.Image, second: Image.Image) -> float:
    data = ImageChops.difference(first.convert("RGBA"), second.convert("RGBA")).tobytes()
    return sum(data) / (len(data) * 255) if data else 0.0


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate one normalized complete animation row")
    ap.add_argument("strip")
    ap.add_argument("--row", type=int, required=True, choices=range(9))
    ap.add_argument("--json-out")
    ap.add_argument("--min-frame-difference", type=float, default=0.002)
    ap.add_argument("--max-visible-width", type=int, default=180)
    ap.add_argument("--max-baseline-drift", type=int, default=18)
    args = ap.parse_args()

    path = Path(args.strip).expanduser().resolve()
    image = Image.open(path).convert("RGBA")
    count = USED_COUNTS[args.row]
    errors: list[str] = []
    expected = (count * CELL_W, CELL_H)
    if image.size != expected:
        errors.append(f"expected normalized strip {expected[0]}x{expected[1]}, got {image.width}x{image.height}")

    frames: list[Image.Image] = []
    bottoms: list[int] = []
    heights: list[int] = []
    if image.size == expected:
        for column in range(count):
            frame = image.crop((column * CELL_W, 0, (column + 1) * CELL_W, CELL_H))
            frames.append(frame)
            bbox = frame.getchannel("A").getbbox()
            if bbox is None:
                errors.append(f"column {column} is empty")
                continue
            width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            bottoms.append(bbox[3]); heights.append(height)
            if width > args.max_visible_width:
                errors.append(f"column {column} visible width {width}px exceeds {args.max_visible_width}px; likely multiple figures/fragments")
        if bottoms and max(bottoms) - min(bottoms) > args.max_baseline_drift:
            errors.append(f"baseline drift {max(bottoms) - min(bottoms)}px exceeds {args.max_baseline_drift}px")

    differences = []
    if len(frames) == count:
        differences = [difference(frames[i], frames[(i + 1) % count]) for i in range(count)]
        duplicate_after = [i for i, value in enumerate(differences) if value < args.min_frame_difference]
        if duplicate_after:
            errors.append(f"duplicate/near-duplicate transitions after columns {duplicate_after}")

    result = {
        "ok": not errors, "file": str(path), "row": args.row, "frames": count,
        "median_visible_height": median(heights) if heights else None,
        "frame_differences": [round(value, 6) for value in differences],
        "errors": errors,
    }
    if args.json_out:
        Path(args.json_out).expanduser().resolve().write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
