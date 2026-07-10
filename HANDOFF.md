# Codex Pet Forge handoff

## Mandatory update rule

**Every future behavior, script, prompt, plugin metadata, dependency, test, license, release, or GitHub change must update this document in the same commit.** Add the date, change summary, validation evidence, risks, and next action.

## Project identity

- Repository: `codex-pet-forge`
- Purpose: package a Codex plugin that turns a user reference image into a validated Codex v2 pet.
- Current release: `v0.1.5` (GPT娘 identity-locked rebuild in progress)
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

- Release archives: sibling files through `F:\桌面\小学期\codex-pet-forge-v0.1.3.zip` are historical releases; generate `F:\桌面\小学期\codex-pet-forge-v0.1.4.zip` from the final v0.1.4 commit before upload.
- GitHub remote: public repository `https://github.com/tsingovo/codex-pet-forge`; `origin` has been configured.
- Authentication: GitHub account `tsingovo` is connected. The repository-local `.gh-auth/` directory holds transient CLI configuration and is ignored; never commit or archive it.
- Published baseline: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.0` (tag and source ZIP asset). Main branch is the source of truth.
- Published sample release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.1`, with both `codex-pet-forge-v0.1.1.zip` and the direct `gpt-niang-pet.zip` asset. Confirm the public repository/release pages and both assets are reachable after publication.
- Published repair release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.2`, with the corrected `gpt-niang-pet.zip` and source archive. Verify both artifacts are reachable after publication.
- Published guard release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.3`, with the registration-validation guard and current GPT娘 sample package.
- Published identity-lock release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.4`, with the canonical-character workflow and current GPT娘 sample package.

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
- 2026-07-10 — GPT娘 hover and drag alignment repair
  - Change: regenerated the complete five-frame hover-curiosity row after a reported detached/relocated foot, then regenerated the complete eight-frame right-drag row and deterministically mirrored it for the left-drag row after a reported running offset. Rebuilt the sample ZIP and replaced the local `gpt-niang` pet with backup.
  - Validation: inspected the final contact sheet visually: every hover/running frame has full legs and shoes below the skirt, no clipped limbs or loose shoe components, and the question mark only appears above the hair in its intended hover frame. `validate_atlas.py --require-v2` passed with zero errors/warnings; `install_pet.py --replace --backup` returned `ok: true`.
  - Risk: generated character clothing still includes reference-inspired emblem details; the existing sample asset-rights notice remains mandatory. Do not repair individual foot cells—regenerate and replace the entire action row.
  - Next action: run plugin validation, commit/push, tag `v0.1.2`, create the release with the updated direct package, and verify the public assets.
- 2026-07-10 — registration guard for future pets
  - Change: added a visible-alpha baseline-drift check to `validate_atlas.py`; it rejects action rows whose sprite bottoms diverge by more than 18 pixels, an objective signal for detached shoes, missing feet, or sliced-body registration. Updated the skill to require a complete-row regeneration rather than a one-cell limb patch.
  - Validation: the corrected GPT娘 atlas passes the new guard and all existing structural/chroma validation.
  - Limitation: this is a preventive gate, not a guarantee that every generated pose is artistically correct. The mandatory contact-sheet visual review remains required before installation.
  - Next action: tag/push v0.1.3, release the source archive and current direct GPT娘 package, then verify public assets.
- 2026-07-11 — identity-locked character workflow
  - Change: introduced `prepare_identity_locked_run.py` and `references/identity-lock.md`. Production flow now creates and approves one canonical full-body character first, then requires that exact canonical image as input for every complete action/look row. Fast one-atlas generation is now explicitly draft-only. The fast prompt also now specifies a row-0 master model rather than independent character redraws.
  - Validator: added cross-row median visible-height drift checking for standard rows 0–8 (default 12% relative to idle), complementing the existing per-row baseline guard. It rejects evident practical-scale/proportion changes; final face/outfit/head-ratio review stays manual.
  - Validation: identity-locked preparation smoke test succeeded; corrected GPT娘 atlas passes the new height and baseline gates; unit tests and plugin validation pass.
  - Trade-off: consistent production animation requires one canonical generation plus coherent full-row generations. It uses more visual jobs than draft mode, but avoids spending time repairing a different character in every action.
  - Next action: tag/push and release v0.1.4; keep fast mode only for early previews, and install only after identity-locked contact-sheet approval.
- 2026-07-11 — local Codex plugin activation
  - Change: added marketplace `tsingovo/codex-pet-forge` and installed `codex-pet-forge@codex-pet-forge` into the real user Codex home at `C:\Users\HASEE\.codex`; active marketplace version is `0.1.4`.
  - Validation: `codex plugin list` reported `installed, enabled` for `codex-pet-forge@codex-pet-forge` version `0.1.4`.
  - Next action: restart/refresh Codex before invoking the identity-locked workflow in a new task.
- 2026-07-11 — GPT娘 identity-locked rebuild and bilingual documentation
  - Change: rebuilt GPT娘 from a newly approved canonical full-body character, generated the action/look rows with that canonical image as sole identity input, validated and installed the new v2 package. Replaced the GitHub showcase assets and direct ZIP. Rewrote root and sample README content so each Chinese explanation immediately precedes its English equivalent.
  - Validation: v2 validator passed; final contact sheet visually reviewed for consistent character scale, complete limbs, empty cells, and direction coverage. Local replacement installed with backup, then the backup folder was deleted to avoid duplicate Codex pets.
  - Next action: commit, tag/push v0.1.5, create the release, attach source and GPT娘 ZIP assets, and verify GitHub presentation.
