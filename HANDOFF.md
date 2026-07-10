# Codex Pet Forge handoff

## Mandatory update rule

**Every future behavior, script, prompt, plugin metadata, dependency, test, license, release, or GitHub change must update this document in the same commit.** Add the date, change summary, validation evidence, risks, and next action.

## Project identity

- Repository: `codex-pet-forge`
- Purpose: package a Codex plugin that turns a user reference image into a validated Codex v2 pet.
- Current release: `v0.1.8` (published one-reference canonical-rig and motion QA upgrade)
- Baseline commits: `77673a1 feat: add Codex Pet Forge fast pet plugin`; `014bb12 docs: add copyright notice and maintenance handoff`
- Maintainer copyright: `Copyright (c) 2026 HASEE`
- License: Apache-2.0 with project notice in `NOTICE`; upstream attribution in `UPSTREAM.md`.

## Current architecture

```text
one user reference
  -> prepare_identity_locked_run.py (file-based prompt pack + exact strip guides)
  -> canonical.png (immutable full-body rig)
  -> turnaround.png (eight orthographic identity anchors)
  -> 11 exact complete-row jobs (meaningful pose + multi-frame expression timelines)
  -> validate_row_strip.py for every row
  -> assemble_rows.py -> despill_chroma_edges.py -> validate_atlas.py
  -> make_contact_sheet.py + make_motion_previews.py
  -> write_pet_manifest.py + install_pet.py --replace (no backup when requested)
```

Fast one-atlas generation remains draft-only. Production repair regenerates only the complete failed row; isolated body-part repair and missing-frame duplication/grouping are forbidden.

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
- Rig contract: `plugins/codex-pet-forge/skills/pet-forge/references/character-rig-contract.md`
- One-reference prompt pack: `plugins/codex-pet-forge/skills/pet-forge/scripts/prepare_identity_locked_run.py`
- Row/atlas motion validators: `validate_row_strip.py`, `validate_atlas.py`
- Motion QA renderer: `make_motion_previews.py`
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

- Release archives: sibling files through `F:\桌面\小学期\codex-pet-forge-v0.1.7.zip` are historical releases; generate `F:\桌面\小学期\codex-pet-forge-v0.1.8.zip` from the final v0.1.8 commit before upload.
- GitHub remote: public repository `https://github.com/tsingovo/codex-pet-forge`; `origin` has been configured.
- Authentication: GitHub account `tsingovo` is connected. The repository-local `.gh-auth/` directory holds transient CLI configuration and is ignored; never commit or archive it.
- Published baseline: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.0` (tag and source ZIP asset). Main branch is the source of truth.
- Published sample release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.1`, with both `codex-pet-forge-v0.1.1.zip` and the direct `gpt-niang-pet.zip` asset. Confirm the public repository/release pages and both assets are reachable after publication.
- Published repair release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.2`, with the corrected `gpt-niang-pet.zip` and source archive. Verify both artifacts are reachable after publication.
- Published guard release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.3`, with the registration-validation guard and current GPT娘 sample package.
- Published identity-lock release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.4`, with the canonical-character workflow and current GPT娘 sample package.
- Published one-reference rig release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.8`, with the source archive and validated direct GPT娘 package.

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
  - Release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.5` publishes both the source archive and updated `gpt-niang-pet.zip`.
  - Next action: use the installed v0.1.5 workflow for future pets; retain Chinese-first/English-second documentation when adding or revising GitHub explanations.

- 2026-07-11 — GPT娘 right-drag scale repair
  - Change: regenerated the complete right-drag row as a three-quarter pose to match canonical practical scale; validated and reinstalled, deleting the backup to prevent duplicates. GitHub sample package updated.
  - Validation: v2 validator passes with equal 194px median visible height across rows 0-10.


- 2026-07-11 — GPT娘向右拖拽单角色修复 / GPT娘 single-character right-drag repair
  - 中文：确认 v0.1.6 源图只生成 7 个相连人物，自动分割把多个角色塞入单帧；废弃该行，改为将已批准的向左整行整体镜像为向右整行，确保每格一个角色且体型完全一致。
  - English: Confirmed that the v0.1.6 source returned only seven touching figures and automatic segmentation packed multiple characters into cells; discarded that row and mirrored the approved complete left-drag row to produce the right-drag row, guaranteeing one character per cell and identical proportions.
  - 中文：新增单格最大可见宽度校验，并规定生成数量不足时必须整行重生，禁止通过分组或复制补足帧数。
  - English: Added a maximum visible-width validator and a rule that insufficient generated poses require complete-row regeneration; grouping or duplicating figures to fill frame counts is prohibited.
  - 中文：最终图集通过 v2、透明度、基线、跨行高度和单格宽度校验，并已重新安装且删除备份目录。
  - English: The final atlas passes v2, transparency, baseline, cross-row height, and per-cell width validation; it was reinstalled and the backup directory was removed.
- 2026-07-11 — 本地插件升级 / Local plugin upgrade
  - 中文：真实用户 Codex 已升级并启用 codex-pet-forge 0.1.7。
  - English: The real user Codex installation was upgraded to and enabled codex-pet-forge 0.1.7.

- 2026-07-11 — 单参考图人物骨架与动作质量升级 / One-reference rig and motion-quality upgrade
  - 中文：产品入口保持只需一张用户参考图；`prepare_identity_locked_run.py` 现在生成标准人物、八方向正交转台、11 条逐行动作提示、精确帧位布局和逐帧动作/表情时间线。标准形象锁定头身比、脸型、手脚与四肢比例、发型体积、每层衣物及非对称装饰。
  - English: The product still accepts one user reference only; `prepare_identity_locked_run.py` now emits canonical-model, eight-view turnaround, eleven complete-row prompts, exact slot guides, and per-frame motion/expression timelines. The canonical rig locks head/body ratio, face, limb/hand/shoe proportions, hair volumes, garment layers, and asymmetric ornaments.
  - 中文：新增 `character-rig-contract.md`、`validate_row_strip.py`、`assemble_rows.py` 与 `make_motion_previews.py`；图集验证器新增重复帧、动作突跳和多帧头部变化检查。Codex 播放节奏由主程序固定，因此产品通过用满帧位、均匀相位和无重复帧提高有效流畅度，不伪造不存在的 FPS 清单字段。
  - English: Added `character-rig-contract.md`, `validate_row_strip.py`, `assemble_rows.py`, and `make_motion_previews.py`; atlas validation now checks duplicate frames, abrupt motion steps, and multi-frame head-region changes. Codex playback cadence is host-controlled, so effective smoothness comes from full frame use, even phases, and no duplicates rather than an unsupported manifest FPS field.
  - 中文：明确第 0 行会在无其他状态时自动触发呼吸—眨眼—视线—回稳待机循环；第 6 行仍是等待用户输入。所有情绪动作必须在至少三帧中发展表情，动作必须有起势、发展和回位。
  - English: Clarified that row 0 automatically triggers the breathing-blink-gaze-return idle loop while no other state is active; row 6 remains user-input waiting. Every expressive action develops across at least three frames and has anticipation, development, and return.
  - 中文：现有 GPT娘 的两条方向行原先各有一个复制帧，已分别用标准形象、旧方向参考和精确 8 格布局重生；新方向行每格唯一、194px 统一高度、无重复帧，完整 v2 验证通过并以无备份方式覆盖安装。本地只保留 `gpt-niang` 一个目录。
  - English: The existing GPT娘 direction rows each contained one duplicated frame; both were regenerated using the canonical model, prior direction reference, and exact eight-slot guides. The new direction cells are unique, share a 194px height, pass full v2 validation, and were installed in-place without backup; only the `gpt-niang` directory remains locally.
  - 中文：GitHub 样例新增八方向转台与 8 FPS 待机/悬停/思考 GIF；所有新增 README 英文说明继续遵守中文在前、英文在后的规则。
  - English: The GitHub sample now includes the eight-view turnaround and 8 FPS idle/hover/thinking GIFs; all new README explanations continue to place Chinese before the corresponding English.
- 2026-07-11 — v0.1.8 发布与本地启用 / v0.1.8 release and local activation
  - 中文：GitHub v0.1.8 已公开发布，包含源码 ZIP 和已验证的 GPT娘 直装包；发布说明继续采用中文在前、英文在后的格式。
  - English: GitHub v0.1.8 is publicly released with the source ZIP and validated direct GPT娘 package; release notes continue the Chinese-first, English-second format.
  - 中文：真实用户 Codex 已升级并启用 `codex-pet-forge@0.1.8`；宠物目录只保留 `C:\Users\HASEE\.codex\pets\gpt-niang`，无旧备份目录。
  - English: The real user Codex installation now runs `codex-pet-forge@0.1.8`; only `C:\Users\HASEE\.codex\pets\gpt-niang` remains, with no old backup directory.
  - 中文：发布前证据包括 11 条行级验证全部通过、重新装配图集通过、4 项单元测试通过、技能/插件验证通过、临时 marketplace 安装为 0.1.8、GitHub 两个发布资产均已上传。
  - English: Pre-release evidence includes all eleven row validators passing, reassembled atlas validation passing, four unit tests passing, skill/plugin validation passing, temporary marketplace installation at 0.1.8, and both GitHub release assets uploaded.
