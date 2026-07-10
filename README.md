# Codex Pet Forge

Turn an uploaded character image into a validated Codex v2 animated pet.

> Copyright (c) 2026 HASEE. See [NOTICE](NOTICE) and [LICENSE](LICENSE).

Pet Forge is a Codex plugin and skill. After installation, a user can attach a character image and say:

> Create a Codex pet from this image. Name it Momo.

Codex reads the bundled format and trigger rules, generates one complete fast atlas, normalizes it, validates it, shows a contact sheet, and installs the pet. If one state is poor, it regenerates only that row.

## Why this exists

- One primary image-generation job in fast mode.
- Prompts and format rules live in files instead of being repeated in chat.
- Deterministic atlas geometry, chroma cleanup, validation, preview, manifest writing, and installation.
- Correct runtime semantics: row 4 is mouse hover; drag selection is horizontal only.
- Anime-friendly expressions, including hover head tilt and stable hand-under-chin thinking.
- No user character artwork is bundled in this repository.

## What users get

1. Upload one character image.
2. Ask Codex to use Pet Forge.
3. Codex reads the bundled atlas contract and trigger rules.
4. AI produces a character-specific atlas from the reference.
5. Deterministic scripts normalize, clean, validate, preview, and install it.

The default fast path uses one primary generation job. A failed expression or motion is repaired as one row instead of rebuilding the whole pet.

## Install from GitHub

Install the published marketplace from `tsingovo/codex-pet-forge`:

```powershell
codex plugin marketplace add tsingovo/codex-pet-forge
codex plugin add codex-pet-forge@codex-pet-forge
```

Restart Codex or open a new task after installation.

For local development:

```powershell
codex plugin marketplace add "C:\path\to\codex-pet-forge"
codex plugin add codex-pet-forge@codex-pet-forge
```

## Use

Attach one reference image and ask Codex:

```text
Use Pet Forge to create a Codex pet from this image.
Name: Momo
Style: preserve the reference
```

Codex will follow `skills/pet-forge/SKILL.md` inside the plugin.

## Fast and reliable modes

### Fast (default)

1. Generate one full 8x11 atlas from the reference and layout guide.
2. Normalize to `1536x2288` RGBA.
3. Clear unused cells and chroma-key background.
4. Validate, preview, write `pet.json`, and install.

### Reliable fallback

If the fast atlas has identity drift, missing frames, or a poor expression, generate only the failed horizontal row and replace it with `replace_atlas_row.py`. Do not redo the whole pet.

## Actual Codex trigger mapping

| Row | Internal state | Actual design target |
|---:|---|---|
| 0 | idle | breathing/blinking |
| 1 | running-right | horizontal drag right |
| 2 | running-left | horizontal drag left |
| 3 | waving | greeting |
| 4 | jumping | **mouse-hover curiosity** |
| 5 | failed | deflated/error reaction |
| 6 | waiting | waits for user input |
| 7 | running | processing; stable chin-rest thinking |
| 8 | review | review/completion |
| 9-10 | look directions | 16 clockwise pointer looks |

Pure vertical dragging does not select an independent animation in the current Codex client. Pet Forge does not modify application files to change that behavior.

## Requirements

- Codex with plugin support
- Python 3.10+
- Pillow 10-12
- Image generation available to Codex

For standalone script development:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/codex-pet-forge/
  .codex-plugin/plugin.json
  skills/pet-forge/
    SKILL.md
    references/
    scripts/
tests/
```

## Licensing

The repository code and documentation are released under Apache-2.0 while retaining the author's copyright notice and attribution requirements. See `LICENSE`, `NOTICE`, and `UPSTREAM.md`. User reference images and generated characters are not automatically covered by the code license; see `ASSET_LICENSES.md`.

## Maintainer handoff

Before changing behavior, scripts, prompts, licensing, or release state, read and update [HANDOFF.md](HANDOFF.md) in the same commit. This is a required project rule.
