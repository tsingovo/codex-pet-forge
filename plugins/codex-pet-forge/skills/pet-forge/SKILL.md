---
name: pet-forge
description: Create, validate, repair, preview, and install identity-locked Codex Desktop 8x9 pets from one user-supplied character reference image. Use when a user asks to turn an image, drawing, avatar, anime character, mascot, or original character into a coherent animated pet, or asks to package or repair a custom 1536x1872 pet atlas.
---

# Pet Forge

Create a Codex Desktop 8x9 pet from exactly one user reference image with deterministic prompt preparation, identity locking, animation QA, packaging, and installation. Production pets behave like one rigged model rendered in different poses; the one-atlas path is draft-only. Eleven-row turnarounds are offline-only QA artifacts and are never installed.

## Runtime

Before running scripts, locate Python 3.10+ with Pillow. In Codex Desktop, call `load_workspace_dependencies` and use its exact Python path. Otherwise use a virtual environment with `pip install -r requirements.txt` from the repository root.

Set:

```text
SKILL_DIR=<absolute path to this skill>
PYTHON=<absolute Python executable>
```

## Identity-locked workflow (required for production)

Use this workflow whenever the user expects a coherent finished pet. It prevents the common failure where each action becomes a differently proportioned character.

1. Read `references/identity-lock.md`, `references/character-rig-contract.md`, `references/trigger-semantics.md`, `references/atlas-contract.md`, `references/runtime-playback-contract.md`, and `references/runtime-overlay-clipping.md`.
2. Prepare the run:

```powershell
& $PYTHON "$SKILL_DIR/scripts/prepare_identity_locked_run.py" `
  --reference <absolute-image-path> `
  --pet-name <display-name> `
  --output-dir <absolute-run-dir>
```

3. Follow `<run>/pet-workflow.json`: generate and approve `canonical.png`, then generate/approve the exact eight-view `turnaround.png`.
4. Run the listed row prompt files one at a time, attaching both internal identity assets. Require the exact figure count; never group/duplicate figures to compensate for a missing pose.
5. Run `validate_row_strip.py` on every normalized row, assemble only complete approved rows with `assemble_rows.py`, then validate with `validate_atlas.py`. Reject duplicate frames, multi-character cells, baseline/height drift, and chroma/geometry failures.
   Assembly automatically performs uniform Desktop safe-box registration: 176px visible height, fixed shoe baseline, and hard four-edge padding. Never bypass it by copying row strips directly into the install package.
6. Render both `make_contact_sheet.py` and `make_motion_previews.py --fps 8`. Inspect the still identity comparison and every real loop; do not install if anatomy ratios, face, hair, garment layers/ornaments, practical scale, motion meaning, loop continuity, or expression continuity changes between rows.
7. Row 0 columns 0-5 are the automatically triggered idle loop when no other state is active. Require readable breathing/blink/tiny head-tilt/gaze/smile/return phases tuned for the host's 6.6-second slow loop; columns 6-7 remain transparent because the current host never references them.

Compact QA commands:

```powershell
& $PYTHON "$SKILL_DIR/scripts/validate_row_strip.py" <run>/rows/row-00.png --row 0
& $PYTHON "$SKILL_DIR/scripts/assemble_rows.py" --rows-dir <run>/rows `
  --output <run>/spritesheet.webp --png-output <run>/spritesheet.png
& $PYTHON "$SKILL_DIR/scripts/validate_atlas.py" <run>/spritesheet.webp `
  --chroma-key '#FF00FF' --json-out <run>/validation.json
& $PYTHON "$SKILL_DIR/scripts/make_motion_previews.py" <run>/spritesheet.webp `
  --output-dir <run>/motion-previews --fps 8
```

## Fast draft workflow

1. Inspect the user's reference image. Treat it as identity/style grounding, not as a ready sprite.
2. Read `references/trigger-semantics.md` and `references/atlas-contract.md`.
3. Prepare a run:

```powershell
& $PYTHON "$SKILL_DIR/scripts/prepare_fast_pet.py" `
  --reference <absolute-image-path> `
  --pet-name <display-name> `
  --output-dir <absolute-run-dir>
```

4. Read `<run>/generation-prompt.md`. Use `$imagegen` once, attaching:
   - `<run>/reference.png` as the canonical identity/style reference.
   - `<run>/atlas-layout-guide.png` as layout-only guidance.
5. Copy the selected output to `<run>/generated-atlas.png`.
6. Normalize and clean it:

```powershell
& $PYTHON "$SKILL_DIR/scripts/normalize_generated_atlas.py" `
  --input <run>/generated-atlas.png `
  --output <run>/spritesheet.png `
  --webp-output <run>/spritesheet.webp `
  --chroma-key '#FF00FF'

& $PYTHON "$SKILL_DIR/scripts/despill_chroma_edges.py" `
  <run>/spritesheet.png `
  --output <run>/spritesheet.png `
  --webp-output <run>/spritesheet.webp `
  --chroma-key '#FF00FF' `
  --json-out <run>/chroma-report.json
```

7. Validate and preview:

```powershell
& $PYTHON "$SKILL_DIR/scripts/validate_atlas.py" `
  <run>/spritesheet.webp --chroma-key '#FF00FF' `
  --json-out <run>/validation.json

& $PYTHON "$SKILL_DIR/scripts/make_contact_sheet.py" `
  <run>/spritesheet.webp --output <run>/contact-sheet.png
```

8. Inspect the contact sheet. Require exactly one complete character per used cell, recognizable identity, correct row semantics, no clipping, no copied grid, and no detached noise. The validator rejects excessive visible width, baseline drift, and identity-height drift. If a generator returns fewer poses than requested, reject/regenerate the complete row; never group, duplicate, or auto-segment source figures merely to reach the required frame count. A fast-draft atlas is not production-ready until it has passed the identity-locked review.
9. Write and install the package:

```powershell
& $PYTHON "$SKILL_DIR/scripts/write_pet_manifest.py" `
  --pet-id <slug> --display-name <name> --description <description> `
  --output <run>/pet.json

& $PYTHON "$SKILL_DIR/scripts/install_pet.py" `
  --package-dir <run> --replace
```

## Repair Only the Failed Row

Do not regenerate the full atlas when one row fails. Generate one horizontal strip using `references/row-repair-prompts.md`, then run:

```powershell
& $PYTHON "$SKILL_DIR/scripts/replace_atlas_row.py" `
  --base <run>/spritesheet.webp --row <0-8> `
  --strip <generated-row.png> --output <run>/spritesheet-repaired.webp `
  --chroma-key '#FF00FF'
```

Then run the single final despill pass, validation, contact-sheet review, and installation again.

## Hard Rules

- Never claim that vertical drag has a distinct animation. Current Codex drag selection uses horizontal delta only.
- Design row 4 (`jumping`) as mouse-hover curiosity, not vertical lift or athletic jumping.
- Design row 7 (`running`) as stable hand-under-chin thinking. Avoid repeated head swings.
- A question mark must touch or overlap hair/hood; reject detached punctuation.
- Preserve user identity and supplied art cues, but do not copy unrelated scenery, text, UI, or another character from expression references.
- Never modify Codex application files or `app.asar`.
- When clipping is fixed to a rectangle, appears only after split-screen/cross-display dragging, and recovers after another drag, run `diagnose_overlay_clipping.py`. If all cells pass, record it as host overlay bounds desynchronization and do not regenerate the character.
- Keep no backup when the user explicitly requests replacement without old copies; verify only one same-ID pet directory remains.
- Do not install unless `validate_atlas.py` passes and reports `desktop_installable: true`.
- Reject any used row containing duplicate/near-duplicate adjacent frames or only one expressive frame.
- Reject any cell with more than 3% visible pixels outside its main connected character, or any loop whose cyclic motion-step coefficient of variation exceeds 0.65.
- Reject fewer/more generated figures than requested; do not fill missing frames by duplicating, grouping, or isolated body-part repair.

## Modes

- **Identity-locked (default for finished pets):** one user reference produces an approved canonical image and eight-view turnaround, then one coherent row at a time with both identity anchors attached.
- **Fast draft:** one full-atlas generation, deterministic normalization, targeted row repair if needed; never install until it has passed identity-locked review.

Detailed format and prompts live under `references/`; do not repeat them in chat unless needed.
