from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from pet_common import slugify


IDENTITY_CLAUSE = """IDENTITY LOCK: The attached canonical full-body sprite is the sole character model.
Clone this exact same character into the requested pose sequence: identical head-to-body ratio,
face/eye shape, hairstyle and hair length, outfit cut, palette, shoes, line weight, practical
scale, and baseline. Change only pose, expression, gaze, or the explicitly requested limb
position. Do not redraw a variant, change proportions, add/remove garments, or change the
character's apparent age or body type."""


def main() -> None:
    ap = argparse.ArgumentParser(description="Prepare an identity-locked Codex pet run")
    ap.add_argument("--reference", required=True)
    ap.add_argument("--pet-name", required=True)
    ap.add_argument("--pet-id")
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    reference = Path(args.reference).expanduser().resolve()
    if not reference.is_file():
        raise SystemExit(f"reference not found: {reference}")
    out = Path(args.output_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    copied = out / f"reference{reference.suffix.lower() or '.png'}"
    shutil.copy2(reference, copied)

    canonical = f"""# Canonical character image for {args.pet_name}

Use the attached reference only as identity/style grounding. Create exactly one calm, front-facing,
full-body chibi sprite on a perfectly flat #FF00FF background. This is the permanent master model
for every future animation row. Keep generous padding; include intact legs and shoes; no text,
logos, UI, props, floor, shadow, or scenery. Do not make an atlas.

The next stage will attach this approved output as `canonical.png` to every pose-generation job.
"""
    rows = f"""# Row generation contract for {args.pet_name}

Attach both `canonical.png` and the listed row layout guide to every row job. The original reference
is not sufficient after this point; `canonical.png` is mandatory.

{IDENTITY_CLAUSE}

Generate one complete coherent horizontal row at a time. Keep all frames centered on one baseline.
If any frame changes the character model or has a detached/cropped limb, reject the whole row and
regenerate it; never paste a single replacement foot, face, or hair fragment into an otherwise
approved row.
"""
    (out / "canonical-generation-prompt.md").write_text(canonical, encoding="utf-8")
    (out / "row-generation-contract.md").write_text(rows, encoding="utf-8")
    (out / "identity-lock.json").write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "petId": args.pet_id or slugify(args.pet_name),
                "displayName": args.pet_name,
                "reference": copied.name,
                "canonicalOutput": "canonical.png",
                "requiredInputsForEveryRow": ["canonical.png"],
                "identityLock": True,
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"ok": True, "runDir": str(out), "canonicalPrompt": str(out / "canonical-generation-prompt.md")}, ensure_ascii=True))


if __name__ == "__main__":
    main()
