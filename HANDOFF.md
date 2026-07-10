# Codex Pet Forge handoff

## Mandatory update rule

**Every future behavior, script, prompt, plugin metadata, dependency, test, license, release, or GitHub change must update this document in the same commit.** Add the date, change summary, validation evidence, risks, and next action.

## Project identity

- Repository: `codex-pet-forge`
- Purpose: package a Codex plugin that turns a user reference image into a validated Codex v2 pet.
- Current release: `v0.1.0` (unpublished local baseline)
- Baseline commit: `77673a1 feat: add Codex Pet Forge fast pet plugin`
- Maintainer copyright: `Copyright (c) 2026 HASEE`
- License: Apache-2.0 with project notice in `NOTICE`; upstream attribution in `UPSTREAM.md`.

## Current architecture

```text
reference image
  -> prepare_fast_pet.py (reference copy, layout guide, compact generation prompt)
  -> one image-generation job (fast mode)
  -> normalize_generated_atlas.py
  -> despill_chroma_edges.py
  -> validate_atlas.py + make_contact_sheet.py
  -> write_pet_manifest.py + install_pet.py
```

If the complete atlas fails, use `replace_atlas_row.py` to repair only one horizontal action row.

## Non-negotiable runtime facts

Source: `plugins/codex-pet-forge/skills/pet-forge/references/trigger-semantics.md`, verified against Codex Desktop `26.707.3748.0` local frontend code.

- Row 4 state name `jumping` is actually selected by pointer hover. It must show curiosity, not lifting or athletic jumping.
- Drag uses `deltaX` only: positive -> row 1, negative -> row 2.
- Pure vertical dragging has no independently selectable animation state.
- Row 7 state name `running` is used as quiet processing: stable screen-right hand under chin, no repeated head swing.
- Do not patch Codex `app.asar`; this repository only packages pet assets and deterministic tools.

## Key paths

- Plugin manifest: `plugins/codex-pet-forge/.codex-plugin/plugin.json`
- Marketplace manifest: `.agents/plugins/marketplace.json`
- Skill: `plugins/codex-pet-forge/skills/pet-forge/SKILL.md`
- Fast generator prompt: `plugins/codex-pet-forge/skills/pet-forge/scripts/prepare_fast_pet.py`
- Contract: `plugins/codex-pet-forge/skills/pet-forge/references/atlas-contract.md`
- Tests: `tests/test_pet_forge.py`

## Verification commands

```powershell
$PY = 'C:\Users\HASEE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $PY -m unittest discover -s tests -v
python C:\Users\HASEE\.codex\skills\.system\skill-creator\scripts\quick_validate.py plugins\codex-pet-forge\skills\pet-forge
python C:\Users\HASEE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py plugins\codex-pet-forge
```

Also test a temporary marketplace installation before release:

```powershell
$env:CODEX_HOME = "$PWD\.codex-test"
codex plugin marketplace add $PWD --json
codex plugin add codex-pet-forge@codex-pet-forge --json
codex plugin list --json
```

Remove `.codex-test` after verification; do not commit it.

## Release state and upload

- Release archive: sibling file `F:\桌面\小学期\codex-pet-forge-v0.1.0.zip` generated with `git archive` from the baseline commit.
- GitHub remote: not configured yet.
- Upload blocker at last audit: GitHub CLI has no local authenticated account despite the user reporting a connected GitHub plugin; no GitHub connector tool was exposed in this task runtime.
- Safe next action after authentication: create the GitHub repository, add `origin`, push `main`, then create a `v0.1.0` GitHub release using the ZIP archive.

## Change log

### 2026-07-10 - v0.1.0 baseline

- Created installable Codex Marketplace/plugin layout.
- Implemented one-atlas fast workflow plus targeted row repair, validation, preview, manifest writing, and atomic installer.
- Documented the real hover/drag runtime semantics.
- Added copyright notice, Apache-2.0 license, upstream attribution, and asset-rights boundary.
- Added end-to-end synthetic atlas test and trigger-contract test.
- Validation evidence: unit tests pass; skill validator passes; plugin validator passes; temporary local marketplace installation and plugin add/list pass; independent forward test prepared a run successfully.
- Risks: a single full-atlas generation can still drift on complex/asymmetric characters; use reliable one-row repair. Partial face-only references require conservative inference for unseen clothing/body.
- Next action: publish to GitHub after authenticated repository creation, then replace `OWNER` in README install examples with the actual GitHub owner/repository.
