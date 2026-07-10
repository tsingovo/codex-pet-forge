---
name: pet-forge
description: Create, validate, repair, preview, and install Codex v2 pets from user-supplied character reference images. Use when a user asks to turn an image, drawing, avatar, anime character, mascot, or original character into a Codex pet, or asks to package or repair a custom 1536x2288 pet atlas. Defaults to a one-image fast atlas workflow and falls back to one-row repair only when validation fails.
---

# Pet Forge

Create a Codex v2 pet from a reference image with deterministic normalization, QA, packaging, and installation. Production pets use an identity-locked canonical character; the one-atlas path is only a quick draft.

## Runtime

Before running scripts, locate Python 3.10+ with Pillow. In Codex Desktop, call `load_workspace_dependencies` and use its exact Python path. Otherwise use a virtual environment with `pip install -r requirements.txt` from the repository root.

Set:

```text
SKILL_DIR=<absolute path to this skill>
PYTHON=<absolute Python executable>
```

## Identity-locked workflow (required for production)

Use this workflow whenever the user expects a coherent finished pet. It prevents the common failure where each action becomes a differently proportioned character.

1. Read `references/identity-lock.md`.
2. Prepare the run:

```powershell
& $PYTHON "$SKILL_DIR/scripts/prepare_identity_locked_run.py" `
  --reference <absolute-image-path> `
  --pet-name <display-name> `
  --output-dir <absolute-run-dir>
```

3. Generate and approve one canonical full-body sprite using `canonical-generation-prompt.md`, then save it as `<run>/canonical.png`.
4. Attach `<run>/canonical.png` to every row job and include the exact identity-lock clause from `row-generation-contract.md`. Generate each complete action row, never isolated cells.
5. Assemble with `replace_atlas_row.py`, then validate with `validate_atlas.py --require-v2`. The validator rejects excessive baseline drift and identity-height drift in standard rows.
6. Inspect the final contact sheet against `canonical.png`. Do not install if the face, head/body ratio, hair, outfit, shoes, or practical scale changes between rows.

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
  <run>/spritesheet.webp --require-v2 --chroma-key '#FF00FF' `
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
  --package-dir <run> --replace --backup
```

## Repair Only the Failed Row

Do not regenerate the full atlas when one row fails. Generate one horizontal strip using `references/row-repair-prompts.md`, then run:

```powershell
& $PYTHON "$SKILL_DIR/scripts/replace_atlas_row.py" `
  --base <run>/spritesheet.webp --row <0-10> `
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
- Back up an existing same-ID pet before replacement.
- Do not install unless `validate_atlas.py --require-v2` passes.

## Modes

- **Identity-locked (default for finished pets):** one approved canonical character image, then one coherent row at a time with that same canonical image attached to every job.
- **Fast draft:** one full-atlas generation, deterministic normalization, targeted row repair if needed; never install until it has passed identity-locked review.

Detailed format and prompts live under `references/`; do not repeat them in chat unless needed.
