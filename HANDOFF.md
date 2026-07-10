# Codex Pet Forge handoff

## Mandatory update rule

**Every future behavior, script, prompt, plugin metadata, dependency, test, license, release, or GitHub change must update this document in the same commit.** Add the date, change summary, validation evidence, risks, and next action.

## Project identity

- Repository: `codex-pet-forge`
- Purpose: package a Codex plugin that turns a user reference image into a validated Codex v2 pet.
- Current release: `v0.1.1` (published on GitHub)
- Baseline commits: `77673a1 feat: add Codex Pet Forge fast pet plugin`; `014bb12 docs: add copyright notice and maintenance handoff`
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

- Release archives: sibling file `F:\桌面\小学期\codex-pet-forge-v0.1.0.zip` remains the baseline release; generate `F:\桌面\小学期\codex-pet-forge-v0.1.1.zip` from the final v0.1.1 commit before upload.
- GitHub remote: public repository `https://github.com/tsingovo/codex-pet-forge`; `origin` has been configured.
- Authentication: GitHub account `tsingovo` is connected. The repository-local `.gh-auth/` directory holds transient CLI configuration and is ignored; never commit or archive it.
- Published baseline: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.0` (tag and source ZIP asset). Main branch is the source of truth.
- Published sample release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.1`, with both `codex-pet-forge-v0.1.1.zip` and the direct `gpt-niang-pet.zip` asset. Confirm the public repository/release pages and both assets are reachable after publication.

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
- 2026-07-10 — GitHub publication preparation
  - Change: created public remote `tsingovo/codex-pet-forge`, updated README installation command, and protected repository-local GitHub CLI configuration with `.gitignore`.
  - Validation: authenticated GitHub API identity returned `tsingovo`; `origin` points to the public repository.
  - Risk: Windows Git initially failed HTTPS push using the system Schannel backend; use the GitHub connector/API or the repository-local OpenSSL override, never store an access token in Git configuration.
  - Next action: complete push and GitHub release, then replace this entry's next action with permanent release evidence.
- 2026-07-10 — GitHub v0.1.0 publication
  - Change: pushed `main` to `https://github.com/tsingovo/codex-pet-forge`, created the `v0.1.0` release, and attached the source archive `codex-pet-forge-v0.1.0.zip`.
  - Validation: GitHub release and repository API checks completed after publication.
  - Risk: for this Windows environment, Git HTTPS push requires the repository-local OpenSSL backend and transient Basic authorization header; do not persist the token. GitHub CLI API calls remain usable through `.gh-auth/`.
  - Next action: for every future change, update this handoff document in the same commit, run the listed checks, push `main`, and create a new versioned release/archive.
- 2026-07-10 — Marketplace visibility clarification
  - Change: documented that the public GitHub marketplace is visible to anyone, but it is not automatically indexed by Codex global plugin search; users must add `tsingovo/codex-pet-forge` once before it appears in their local plugin list.
  - Validation: command names verified with `codex plugin --help` (`marketplace`, `list`, and `add`).
  - Risk: marketplace discovery behavior is controlled by Codex; if a future official directory/index becomes available, update this README section and this handoff in the same commit.
  - Next action: push this documentation clarification to `main`; no release asset change is required.
- 2026-07-10 — GPT娘 fast-workflow sample audit
  - Change: exercised the public marketplace installation command in a sandboxed Codex runtime and ran the fast workflow against a user-provided anime character reference.
  - Validation: marketplace add/plugin add succeeded in the sandbox; the generated atlas was structurally normalized to v2 (`1536x2288`, `8x11`) and `validate_atlas.py --require-v2` passed after chroma removal and cell cleanup.
  - Risk: the image model returned only ten source bands and did not preserve exact cell registration. A temporary structural repair was sufficient for validator coverage but the final contact-sheet visual QA found horizontal clipping and a duplicated thinking/review pose. **Do not install or release that sample.**
  - Next action: improve the fast prompt/layout strategy or use the reliable row-by-row fallback for a production GPT娘; require contact-sheet visual approval before running `install_pet.py`.
- 2026-07-10 — GPT娘 production sample and package
  - Change: completed a second reconstruction with per-sprite component registration to prevent cell clipping, replaced the thinking row with a generated hand-under-chin strip, validated the final v2 atlas, and installed it as `C:\Users\HASEE\.codex\pets\gpt-niang`.
  - Validation: `validate_atlas.py --require-v2` passed with zero warnings/errors; the final contact sheet was visually reviewed for slot clipping, empty-cell cleanup, hover question-mark attachment, and row coverage. `install_pet.py --replace --backup` returned `ok: true`.
  - Publication: added `examples/gpt-niang/` containing the reference image, contact sheet, `pet.json`, `spritesheet.webp`, and directly usable `gpt-niang-pet.zip`; README now links the showcase and install flow.
  - Asset caveat: code remains Apache-2.0, but example/reference-character rights are not granted by the code license. Preserve this caveat whenever publishing character samples supplied by users.
  - Next action: commit/push the sample files and attach `gpt-niang-pet.zip` to a GitHub release so users can install without cloning.
- 2026-07-10 — v0.1.1 packaging
  - Change: bumped the marketplace plugin manifest from `0.1.0` to `0.1.1` so clients can distinguish the published sample update.
  - Validation: plugin validation must pass again before tagging; GitHub release must contain the full source archive plus the direct GPT娘 package.
  - Risk: the sample asset package is a convenience artifact, not a grant of rights to external character references; retain the example asset notice.
  - Next action: archive the final commit, tag/push `v0.1.1`, create the GitHub release, attach both ZIP files, and verify the public assets.
