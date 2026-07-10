# Codex Pet Forge handoff

## Mandatory update rule

**Every future behavior, script, prompt, plugin metadata, dependency, test, license, release, or GitHub change must update this document in the same commit.** Add the date, change summary, validation evidence, risks, and next action.

## Project identity

- Repository: `codex-pet-forge`
- Purpose: package a Codex plugin that turns a user reference image into a validated Codex v2 pet.
- Current release: `v0.1.0` (published on GitHub)
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

- Release archive: sibling file `F:\桌面\小学期\codex-pet-forge-v0.1.0.zip`, regenerated with `git archive` from the final release commit before upload.
- GitHub remote: public repository `https://github.com/tsingovo/codex-pet-forge`; `origin` has been configured.
- Authentication: GitHub account `tsingovo` is connected. The repository-local `.gh-auth/` directory holds transient CLI configuration and is ignored; never commit or archive it.
- Published release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.0` (tag and ZIP asset). Main branch is the source of truth.
- Release verification: confirm the public repository page, `v0.1.0` release page, and ZIP asset are reachable after each publication.

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
