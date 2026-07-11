from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from pet_common import slugify


LOCK = (
    "Use canonical.png and turnaround.png as one immutable character rig. Preserve exact head/body "
    "ratio, face and eye geometry, hair silhouette and parting; preserve neck/shoulder/hip width, "
    "upper/lower arm, hand, thigh/calf, leg and shoe lengths and volumes in the same head units; "
    "preserve collar/sleeve/cuff/waist/hem construction, every seam/layer/ornament and its physical "
    "side, palette, line weight, practical height, and shoe "
    "baseline. Keep the complete hair/head inside the cell with at least 12px clear space above it "
    "and at least 10px below the shoes. Rotate joints and shift weight; never scale the head, torso, "
    "limbs, hands, shoes, clothing, or whole character. Change only pose, gaze, and expression. One "
    "complete character per cell."
)

ROWS = [
    (0, "idle", 6, "Exactly six runtime idle frames tuned for Codex's slow 6.6-second loop: calm inhale and attentive eyes; blink begins; eyes closed with a soft smile; eyes reopen with a tiny 3-degree head tilt and gaze shift; restrained warm smile while exhaling; return to the exact calm start. Make every phase readable but subtle, develop the face across at least three frames, and close the loop smoothly."),
    (1, "drag-right", 8, "Eight evenly phased three-quarter-right drag steps: contact; down; passing; lift; contact; down; passing; lift. Natural focused/relaxed/blink face changes across the sequence; same body volume and baseline."),
    (2, "drag-left", 8, "Eight evenly phased three-quarter-left drag steps using the left turnaround anchor: contact; down; passing; lift; contact; down; passing; lift. Preserve asymmetric ornaments on their physical side; do not mirror unless the character is symmetric."),
    (3, "greeting", 4, "Four meaningful greeting poses: notice and smile; hand rises with open eyes; warm wave with happy eyes; hand lowers with relaxed smile. Expression changes in every frame."),
    (4, "hover-curiosity", 5, "Five hover-curiosity poses, never jumping: notice; raised brow; small o-mouth and 10-degree head tilt; questioning look with one small question mark touching hair; gentle return. Full body and changing expression in all frames."),
    (5, "failed", 8, "Eight gradual soft-failure poses: surprise; worried eyes; shoulders lower; gaze drops; small pout; brief closed eyes; recover breath; calm-but-sad return. No detached symbols; face evolves across the whole row."),
    (6, "waiting", 6, "Six user-input waiting poses: attentive; tiny head tilt; hopeful eyes; patient blink; slight asking smile; return attentive. This is distinct from ordinary idle and changes expression across the row."),
    (7, "thinking", 6, "Six stable hand-under-chin thinking poses: focused; eyes shift; brow narrows; small realization; restrained smile; focused return. Same hand stays under chin and body does not swing; face changes in every frame."),
    (8, "review", 6, "Six review poses: focus; careful look; blink; understanding; pleased eyes; small satisfied smile. No new props; expression develops continuously."),
]


def write_prompt(path: Path, title: str, body: str) -> None:
    path.write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8")


def write_strip_guide(path: Path, count: int) -> None:
    image = Image.new("RGB", (count * 192, 208), (255, 0, 255))
    draw = ImageDraw.Draw(image)
    for column in range(count):
        x = column * 192
        draw.rectangle((x + 3, 3, x + 188, 204), outline=(255, 255, 255), width=2)
        draw.rectangle((x + 14, 10, x + 177, 199), outline=(0, 40, 70), width=2)
        draw.text((x + 8, 7), str(column), fill=(0, 0, 0))
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def main() -> None:
    ap = argparse.ArgumentParser(description="Prepare a one-reference, identity-locked Codex pet run")
    ap.add_argument("--reference", required=True)
    ap.add_argument("--pet-name", required=True)
    ap.add_argument("--pet-id")
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    reference = Path(args.reference).expanduser().resolve()
    if not reference.is_file():
        raise SystemExit(f"reference not found: {reference}")
    out = Path(args.output_dir).expanduser().resolve()
    jobs = out / "prompts"
    rows_dir = out / "rows"
    guides = out / "guides"
    jobs.mkdir(parents=True, exist_ok=True)
    rows_dir.mkdir(parents=True, exist_ok=True)
    guides.mkdir(parents=True, exist_ok=True)
    copied = out / f"reference{reference.suffix.lower() or '.png'}"
    shutil.copy2(reference, copied)

    write_prompt(jobs / "00-canonical.md", f"Canonical character for {args.pet_name}", f"""
Attach only `{copied.name}`. Create exactly one calm front-facing complete full-body chibi sprite on
flat #FF00FF. Infer unseen parts conservatively. This becomes an immutable rig: define one head unit,
total height in head units, shoulder/hand/leg/shoe proportions, hair volumes, every garment layer,
seam, ornament, and its physical side. Intact hands, legs, and shoes; no text, logos, UI, props,
floor, shadow, scenery, or extra character. Output one figure only as `canonical.png`.
""")
    write_prompt(jobs / "01-turnaround.md", f"Eight-view turnaround for {args.pet_name}", f"""
Attach `canonical.png` and `guides/turnaround.png` (layout only). {LOCK} Create exactly eight separated complete full-body turntable views in
one horizontal row on flat #FF00FF: front, front-right, right, back-right, back, back-left, left,
front-left. Same orthographic camera, scale, baseline, anatomy, clothing construction, and neutral
expression. No perspective zoom, crop, duplicate view, extra figure, grid, labels, or shadows.
Output `turnaround.png`; reject the job unless there are exactly eight figures.
    """)
    write_strip_guide(guides / "turnaround.png", 8)

    jobs_json = []
    for index, name, count, motion in ROWS:
        file_name = f"row-{index:02d}-{name}.md"
        guide_name = f"guides/row-{index:02d}.png"
        write_strip_guide(out / guide_name, count)
        write_prompt(jobs / file_name, f"Row {index}: {name}", f"""
Attach `canonical.png`, `turnaround.png`, and `{guide_name}` (layout only). {LOCK} Create exactly {count} separated complete
full-body sprites in one horizontal row on flat #FF00FF, ordered left-to-right with equal cell
spacing. {motion} Use every requested frame; no duplicate frames, missing figures, grouped figures,
neighbor fragments, crop, detached limbs/effects, text, grid, labels, floor, or shadow. The last
animation frame must transition naturally back to the first.
""")
        jobs_json.append({
            "row": index, "state": name, "frames": count,
            "prompt": f"prompts/{file_name}", "output": f"rows/row-{index:02d}.png",
            "requiredInputs": ["canonical.png", "turnaround.png", guide_name],
        })

    model = {
        "schemaVersion": 3,
        "petId": args.pet_id or slugify(args.pet_name),
        "displayName": args.pet_name,
        "userInputs": [copied.name],
        "canonicalOutput": "canonical.png",
        "turnaroundOutput": "turnaround.png",
        "desktopAtlas": {"columns": 8, "rows": 9, "width": 1536, "height": 1872},
        "identityLock": True,
        "oneReferenceOnly": True,
        "jobs": jobs_json,
        "qualityOrder": ["identity", "complete anatomy", "meaningful motion", "natural expression", "token economy"],
        "structuralIdentityGate": {
            "reference": "canonical.png",
            "bands": 8,
            "maxSilhouetteWidthDrift": 0.11,
            "covers": ["head", "shoulder/sleeve", "torso/hem", "legs", "shoes"],
        },
        "chatContract": "Keep prompts and QA results in files; report only paths, failed gates, and final status.",
    }
    (out / "pet-workflow.json").write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "runDir": str(out), "workflow": str(out / "pet-workflow.json"), "jobs": len(jobs_json) + 2}, ensure_ascii=True))


if __name__ == "__main__":
    main()
