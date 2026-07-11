from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from PIL import Image, ImageDraw

from pet_common import ATLAS_H, ATLAS_W, CELL_H, CELL_W, COLS, ROWS, slugify

ROW_LABELS = [
    "idle (6 runtime frames)", "drag right", "drag left", "greeting", "hover curious",
    "failed", "waiting", "thinking chin", "review",
]


def create_guide(path: Path) -> None:
    image = Image.new("RGB", (ATLAS_W, ATLAS_H), (255, 0, 255))
    draw = ImageDraw.Draw(image)
    for row in range(ROWS):
        for col in range(COLS):
            x0, y0 = col * CELL_W, row * CELL_H
            draw.rectangle((x0 + 3, y0 + 3, x0 + CELL_W - 4, y0 + CELL_H - 4), outline=(255, 255, 255), width=2)
            draw.rectangle((x0 + 18, y0 + 16, x0 + CELL_W - 19, y0 + CELL_H - 17), outline=(0, 40, 70), width=2)
            draw.text((x0 + 8, y0 + 7), f"{row}:{col}", fill=(0, 0, 0))
        draw.text((8, row * CELL_H + CELL_H - 22), ROW_LABELS[row], fill=(0, 0, 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def prompt(name: str) -> str:
    return f"""# Generate one complete Codex Desktop pet atlas for {name}

Use the character reference as the only identity/style source. Use the layout guide only for slot order and safe padding; do not copy its lines, labels, numbers, or text.

Create one portrait atlas on a perfectly flat solid #FF00FF background, arranged as exactly 8 columns x 9 rows (1536x1872 final). Every slot contains one complete separated full-body chibi sprite, centered and padded, with all hair/head pixels at least 12px below the cell top and shoes at least 10px above the cell bottom. First establish the row-0 column-0 character as the master model, then clone that exact same character model into every other slot: identical head-to-body ratio, face/eye shape, hairstyle and length, outfit cut, palette, shoes, line weight, practical scale, and baseline. Change only pose, gaze, expression, or the explicitly requested limb position. Do not redraw a variant, change proportions, add/remove garments, or change apparent age/body type. No scenery, floor, shadows, text, UI, labels, visible grid, guide marks, detached effects, or cropped limbs.

If the reference shows only a face, bust, or partial body, preserve every visible identity cue and infer unseen clothing, legs, and footwear conservatively as a simple coherent extension of the visible design. Do not invent logos, weapons, complex props, or a second character.

Rows, top to bottom:
0 idle: exactly six readable slow-loop frames—inhale/attentive eyes, blink start, soft closed-eye smile, reopen with tiny head tilt and gaze shift, restrained warm smile/exhale, exact calm return; columns 6-7 empty.
1 horizontal drag right: eight right-facing pulled/locomotion frames.
2 horizontal drag left: eight left-facing pulled/locomotion frames.
3 greeting: four small wave frames; remaining slots empty.
4 actual mouse hover: five frames noticing the pointer, one raised eyebrow, tiny o mouth, cute 10-degree head tilt, slow blink, partial return. One small question mark may appear in middle frames only if its lower tip touches hair/hood. Remaining slots empty. Do not jump or lift.
5 failed: eight soft deflated reaction frames, no red X or detached symbols.
6 waiting: six expectant user-input frames with a restrained head tilt; remaining slots empty.
7 active thinking: six frames with the same screen-right hand stably under the chin, other arm relaxed, head/body fixed; animate only eyes, lids, brows and tiny mouth. No repeated head swing. Remaining slots empty.
8 review: six focused-to-pleased inspection frames; remaining slots empty.

Viewer coordinates are absolute: right means nose/pupils toward the image-right edge; left means image-left. Keep all characters the same practical scale and baseline. Output artwork only on flat magenta, without any visible construction marks.
"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Prepare a one-generation Codex pet run")
    ap.add_argument("--reference", required=True)
    ap.add_argument("--pet-name", required=True)
    ap.add_argument("--pet-id")
    ap.add_argument("--description", default="A custom Codex pet created from a reference image.")
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    reference = Path(args.reference).expanduser().resolve()
    if not reference.is_file():
        raise SystemExit(f"reference not found: {reference}")
    out = Path(args.output_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    ext = reference.suffix.lower() or ".png"
    copied = out / f"reference{ext}"
    shutil.copy2(reference, copied)
    guide = out / "atlas-layout-guide.png"
    create_guide(guide)
    (out / "generation-prompt.md").write_text(prompt(args.pet_name), encoding="utf-8")
    request = {
        "schemaVersion": 1,
        "petId": args.pet_id or slugify(args.pet_name),
        "displayName": args.pet_name,
        "description": args.description,
        "reference": copied.name,
        "layoutGuide": guide.name,
        "generatedAtlas": "generated-atlas.png",
        "chromaKey": "#FF00FF",
        "spriteVersionNumber": 1,
    }
    (out / "pet-request.json").write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
    # ASCII-safe stdout avoids mojibake in Windows shells; UTF-8 files retain display names.
    print(json.dumps({"ok": True, "runDir": str(out), "prompt": str(out / "generation-prompt.md")}, ensure_ascii=True))


if __name__ == "__main__":
    main()
