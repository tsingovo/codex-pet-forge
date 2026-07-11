# Codex Pet Forge handoff

## Mandatory update rule

**Every future behavior, script, prompt, plugin metadata, dependency, test, license, release, or GitHub change must update this document in the same commit.** Add the date, change summary, validation evidence, risks, and next action.

## Project identity

- Repository: `codex-pet-forge`
- Purpose: package a Codex plugin that turns a user reference image into a validated Codex Desktop 8x9 pet.
- Current release: `v0.2.6` (within-action structural median gate prepared)
- Baseline commits: `77673a1 feat: add Codex Pet Forge fast pet plugin`; `014bb12 docs: add copyright notice and maintenance handoff`
- Maintainer copyright: `Copyright (c) 2026 HASEE`
- License: Apache-2.0 with project notice in `NOTICE`; upstream attribution in `UPSTREAM.md`.

## Current architecture

```text
one user reference
  -> prepare_identity_locked_run.py (file-based prompt pack + exact strip guides)
  -> canonical.png (immutable full-body rig)
  -> turnaround.png (eight orthographic identity anchors)
  -> 9 exact complete-row jobs (meaningful pose + multi-frame expression timelines)
  -> validate_row_strip.py for every row
  -> assemble_rows.py -> despill_chroma_edges.py -> validate_atlas.py
  -> make_contact_sheet.py + make_motion_previews.py
  -> write_pet_manifest.py + install_pet.py --replace (no backup when requested)
```

Fast one-atlas generation remains draft-only. Production repair regenerates only the complete failed row; isolated body-part repair and missing-frame duplication/grouping are forbidden.

### 2026-07-11 — Desktop 8×9 runtime-compatibility repair / Desktop 8×9 runtime compatibility repair

- 中文：用户反馈 GPT娘 在实际 Codex 中出现 1/2/3 个人串帧、向右拖拽变瘦变高。根因已确认：旧版安装了 1536×2288 的 11 行图集，而桌面端固定按 `background-size: 800% 900%` 切 8×9 单元格，纵向重采样会把相邻行串入动画。
- English: The user reported 1/2/3-character frame mixing and a tall/thin right-drag pose. Root cause is confirmed: the former 1536×2288 eleven-row sheet was installed while Desktop slices a fixed 8×9 grid with `background-size: 800% 900%`, so vertical resampling mixes neighboring rows.
- 中文：产品默认格式已改为 `1536×1872`、8×9、`spriteVersionNumber: 1`；生成、归一化、逐行装配、安装、联系表、动图预览、行替换、验证器与测试均已改为桌面端契约。11 行转台仅允许作为离线 QA，不得安装。
- English: The product default is now `1536×1872`, 8×9, and `spriteVersionNumber: 1`; generation, normalization, row assembly, installation, contact sheets, motion previews, row replacement, validator, and tests now use the Desktop contract. Eleven-row turnarounds are offline QA only and cannot be installed.
- 中文：GPT娘 样例已裁切为 9 行实际桌面图集，重新生成联系表和直接安装包；验证器报告 `desktop_installable: true`、每行中位可见高度均为 194px、无透明 RGB 残留及无错误。
- English: The GPT娘 sample is now a nine-row Desktop atlas with regenerated contact sheet and direct package; the validator reports `desktop_installable: true`, 194px median visible height in every row, no hidden transparent RGB, and no errors.
- 中文：验证证据：`python -m unittest discover -s tests -v` 通过 6 项（新增 11 行安装图集拒绝测试）；样例图集通过完整桌面验证。待下一步：发布 v0.2.0，并以无备份覆盖方式安装至真实 Codex。
- English: Verification evidence: all six unit tests pass (including the new eleven-row install-atlas rejection test), and the sample atlas passes full Desktop validation. Next action: publish v0.2.0 and replace the real Codex pet in place with no backup.

### 2026-07-11 — 统一头顶安全框与尺寸注册 / Uniform head-safe box and scale registration

- 中文：为解决部分动作头发贴顶或被悬浮窗轻微截断，新增 `register_cells_to_safe_box` 和独立脚本 `register_atlas_safe_box.py`；所有安装帧保持原始宽高比，统一到 184px 可见高度、固定 198px 鞋底基线、10px 鞋底缓冲，并产生至少 14px 的实际头顶缓冲。
- English: To prevent hair from touching the cell top or being slightly clipped by the overlay, added `register_cells_to_safe_box` and `register_atlas_safe_box.py`; all install frames preserve aspect ratio, use a uniform 184px visible height, fixed 198px shoe baseline, 10px shoe clearance, and at least 14px actual head clearance.
- 中文：安全框注册已接入整图归一化、逐行装配和单行替换三个路径；验证器新增头顶最小 10px、鞋底最小 8px 的硬门槛，并新增贴顶头部拒绝测试。
- English: Safe-box registration now runs in full-atlas normalization, row assembly, and single-row replacement; the validator adds hard minimums of 10px above the head and 8px below the shoes, plus a top-touching head rejection test.
- 中文：GPT娘 已重新注册并通过验证：9 行中位可见高度全部为 184px、透明 RGB 残留为 0、无错误；联系表和全部 9 行 8 FPS 预览已重建。
- English: GPT娘 was re-registered and passes validation: all nine rows have a 184px median visible height, transparent RGB residue is zero, and there are no errors; the contact sheet and all nine 8 FPS previews were rebuilt.

### 2026-07-11 — v0.2.0 发布与本地覆盖 / v0.2.0 publication and local replacement

- 中文：`main` 已同步到 GitHub，`v0.2.0` 标签与 Release 已发布；资产为 `codex-pet-forge-v0.2.0.zip` 和 `gpt-niang-pet.zip`，Release 说明继续遵循中文在前、英文在后的双语格式。
- English: `main` is synchronized to GitHub, and the `v0.2.0` tag and Release are published with `codex-pet-forge-v0.2.0.zip` and `gpt-niang-pet.zip`; release notes retain Chinese-first, English-second bilingual ordering.
- 中文：真实 Codex marketplace 已升级，旧的 `codex-pet-forge@0.1.9` 已移除并安装 `0.2.0`；GPT娘 使用 `--replace` 无备份覆盖，本地仅存在一个 `gpt-niang` 目录。
- English: The real Codex marketplace was upgraded, `codex-pet-forge@0.1.9` was removed and `0.2.0` installed; GPT娘 was replaced in place with `--replace` and no backup, leaving exactly one `gpt-niang` directory.

### 2026-07-11 — 人物连通完整性与有效帧率门槛 / Character connectivity and effective-frame-rate gates

- 中文：图集验证器新增四邻域 alpha 主体连通分析，默认要求至少 97% 可见像素属于最大人物主体，并记录组件数、最大组件占比及游离像素占比；用于拦截断手断脚、游离鞋子、邻格残片和额外小人物。
- English: Atlas validation now performs four-neighbor alpha connectivity analysis, requiring at least 97% of visible pixels to belong to the largest character component by default, while recording component count, largest-component share, and detached share; this catches detached hands, feet, shoes, neighboring fragments, and extra small figures.
- 中文：新增左右边至少 4px 安全区，并计算整个闭环的动作步长变异系数；默认 CV 超过 0.65 即拒绝，以避免单帧突跳或不均匀相位降低有效帧率。
- English: Added minimum 4px left/right safety zones and cyclic motion-step coefficient of variation; CV above 0.65 is rejected by default to prevent abrupt one-frame jumps or uneven phases from lowering effective frame rate.
- 中文：新增游离残片和不均匀动作步长失败测试；GPT娘 全部运行帧通过新门槛，最大游离可见占比仅 0.46%，所有动作 CV 为 0.11–0.31。
- English: Added failure tests for detached fragments and uneven motion steps; every GPT娘 runtime frame passes the new gates, with a maximum detached visible share of only 0.46% and motion CV values from 0.11 to 0.31.

### 2026-07-11 — 分屏拖动固定矩形裁切诊断 / Split-screen fixed-rectangle clipping diagnosis

- 中文：只读审计 Codex Desktop `26.707.3748.0` 打包代码确认：旧悬浮页根节点使用 `h-screen w-screen overflow-hidden`；拖动跨显示区域时主进程重新选择 display、计算 layout 并设置 BrowserWindow bounds，而元素尺寸更新可能在 moved-window 定时器期间延迟。固定矩形裁切且继续拖动可恢复，符合宿主窗口边界与布局短暂失步。
- English: Read-only inspection of packaged Codex Desktop `26.707.3748.0` confirms that the legacy overlay root uses `h-screen w-screen overflow-hidden`; cross-display dragging makes the main process reselect a display, calculate layout, and set BrowserWindow bounds, while element-size updates may be deferred during the moved-window timer. Fixed-rectangle clipping that recovers after more dragging matches transient host window-bounds/layout desynchronization.
- 中文：新增 `runtime-overlay-clipping.md` 和 `diagnose_overlay_clipping.py`，在全部 192×208 单元格安全时输出 `host-overlay-bounds-desynchronization-likely`，防止错误重生角色图；不修改或分发 Codex `app.asar`。
- English: Added `runtime-overlay-clipping.md` and `diagnose_overlay_clipping.py`, which reports `host-overlay-bounds-desynchronization-likely` when every 192×208 cell is safe, preventing unnecessary character regeneration; Codex `app.asar` is neither modified nor redistributed.
- 中文：资产侧缓解进一步收紧为统一 176px 可见高度、14px 鞋底缓冲和 16px 横向装配安全框；这不能替代宿主修复，但能降低短暂窗口裁切对人物头发和四肢的影响。
- English: Asset-side mitigation is tightened to a uniform 176px visible height, 14px shoe clearance, and 16px horizontal assembly safe box; this does not replace a host fix, but reduces the impact of transient window clipping on hair and limbs.

### 2026-07-11 — v0.2.1 发布与本地覆盖 / v0.2.1 publication and local replacement

- 中文：GitHub `main`、`v0.2.1` 标签和公开 Release 已同步，包含源码 ZIP 与 GPT娘 直装包；发布说明继续保持每段中文在对应英文之前。
- English: GitHub `main`, the `v0.2.1` tag, and the public Release are synchronized with source ZIP and direct GPT娘 package; every release-note Chinese paragraph remains before its matching English paragraph.
- 中文：9 项单元测试全部通过；GPT娘 诊断报告为 `asset_safe: true`、`desktop_installable: true`、`host-overlay-bounds-desynchronization-likely`，九行动作中位高度均为 176px。
- English: All nine unit tests pass; GPT娘 diagnosis reports `asset_safe: true`, `desktop_installable: true`, and `host-overlay-bounds-desynchronization-likely`, with a 176px median height in all nine action rows.
- 中文：真实 Codex 插件已由 0.2.0 升级到 0.2.1，GPT娘 已无备份覆盖；样例与安装图集 SHA256 完全一致，本地仍只有一个 `gpt-niang` 目录。
- English: The real Codex plugin was upgraded from 0.2.0 to 0.2.1 and GPT娘 replaced without backup; sample and installed atlas SHA256 values match exactly, and only one `gpt-niang` directory remains.

### 2026-07-11 — 宿主真实六帧自动待机 / Runtime-accurate six-frame automatic idle

- 中文：只读核对 Codex Desktop `26.707.3748.0` 动画表确认：待机只播放第 0 行第 0–5 格，基础时长 `280/110/110/140/140/320ms` 均乘以 6，总循环约 6.6 秒；第 6 格从未被引用。
- English: Read-only verification of Codex Desktop `26.707.3748.0` confirms that idle plays only row 0 columns 0-5; base durations `280/110/110/140/140/320ms` are each multiplied by 6 for a roughly 6.6-second loop, and column 6 is never referenced.
- 中文：新增 `runtime-playback-contract.md`，把待机生成从七姿势减少到六姿势，并按慢速真实节奏重写为呼吸、眨眼、闭眼微笑、轻歪头视线、温和吐气微笑、精确回稳；第 6–7 格强制透明。
- English: Added `runtime-playback-contract.md`, reduced idle generation from seven poses to six, and rewrote the slow real cadence as breathing, blink, closed-eye smile, tiny head/gaze shift, warm exhale smile, and exact return; columns 6-7 are forced transparent.
- 中文：这使待机无需额外事件即可由宿主自动触发，同时删除一张永不播放的生成姿势，降低生图时间和提示 Token，不牺牲任何运行帧质量。
- English: This makes idle automatically host-triggered without an extra event while deleting one never-played generated pose, reducing generation time and prompt tokens without sacrificing any runtime frame quality.
- 中文：同时修复动作预览器仍保留旧 11 行计数的问题；现在直接复用唯一 `USED_COUNTS` 契约，并在生成前清理旧 `row-*.gif`，避免残留方向 GIF 误导用户。
- English: Also fixed the motion preview renderer retaining the old eleven-row counts; it now reuses the single `USED_COUNTS` contract and removes stale `row-*.gif` files before rendering, preventing obsolete direction GIFs from misleading users.

### 2026-07-11 — v0.2.2 发布与本地覆盖 / v0.2.2 publication and local replacement

- 中文：GitHub `main`、`v0.2.2` 标签与公开 Release 已同步，发布地址为 `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.2.2`；源码 ZIP 与 GPT娘直装包均已上传，说明保持每段中文在对应英文之前。
- English: GitHub `main`, the `v0.2.2` tag, and the public Release are synchronized at `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.2.2`; both source ZIP and direct GPT娘 package are uploaded, with every Chinese paragraph before its matching English paragraph.
- 中文：完整 9 项测试通过；GPT娘图集验证零错误、零警告，九行动作中位高度均为 176px，分屏裁切诊断为资产安全且疑似宿主窗口边界同步问题；动作预览严格为 9 个 GIF，待机 GIF 为宿主真实使用的 6 帧。
- English: All nine tests pass; the GPT娘 atlas validates with zero errors and warnings, all nine rows have a 176px median visible height, split-screen clipping diagnosis reports asset-safe host-window-bounds desynchronization, and motion previews contain exactly nine GIFs with the host-accurate six-frame idle.
- 中文：真实 Codex 插件已升级到 `0.2.2`，GPT娘使用 `--replace` 无备份覆盖；样例与安装图集 SHA256 同为 `F4D56054C6859EA3F9AC607A94927E2AC245F37B87D0F870A00526E38CE358F2`，本地仅有一个 `gpt-niang` 目录。
- English: The real Codex plugin is upgraded to `0.2.2`, and GPT娘 is replaced in place with `--replace` and no backup; sample and installed atlas SHA256 are both `F4D56054C6859EA3F9AC607A94927E2AC245F37B87D0F870A00526E38CE358F2`, with exactly one local `gpt-niang` directory.

### 2026-07-11 — 八段身体与服装结构锁 / Eight-band body and garment structure lock

- 中文：现有高度与三段纵向质量门槛无法充分识别“身高相同但肩膀、袖子、躯干、衣摆、腿和鞋被重画”的人物漂移；新增八段归一化轮廓宽度指纹，以标准待机第 0 帧为结构基准，默认平均漂移超过 `0.11` 即拒绝。
- English: Existing height and three-band vertical-mass gates cannot fully detect a same-height character whose shoulders, sleeves, torso, hem, legs, or shoes were redrawn; added an eight-band normalized silhouette-width fingerprint using canonical idle frame 0 as the structure reference, rejecting mean drift above `0.11` by default.
- 中文：生成锁已细化到头单位下的肩/髋宽、上下臂、手掌、大腿/小腿、腿长、鞋长和服装层级尺寸；每行必须重新使用同一 canonical 与对应转台方向，不允许用上一条动画结果继续衍生，避免误差逐行累积。
- English: The generation lock now explicitly freezes shoulder/hip width, upper/lower arms, palms, thighs/calves, leg and shoe lengths, and garment-layer dimensions in head units; every row must reuse the same canonical and matching turnaround view rather than deriving from a previous animation result, preventing row-by-row error accumulation.
- 中文：新增默认门槛失败测试，证明在高度、基线、配色、连通性和四边安全区仍合格时，异常放大的身体/衣物轮廓仍会被拒绝；完整 10 项测试、技能校验、插件校验与 GPT娘样例验证均已通过。
- English: Added a default-gate failure test proving that an abnormally enlarged body/outfit silhouette is rejected even when height, baseline, palette, connectivity, and four-edge safety zones remain valid; all ten tests, skill validation, plugin validation, and GPT娘 sample validation pass.
- 中文：GitHub `main`、`v0.2.3` 标签与公开 Release 已同步：`https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.2.3`，源码与 GPT娘直装包均已上传，发布说明维持中文段落在对应英文之前。
- English: GitHub `main`, the `v0.2.3` tag, and the public Release are synchronized at `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.2.3`; source and direct GPT娘 packages are uploaded, with every Chinese paragraph before its matching English paragraph.
- 中文：真实 Codex 插件已升级到 `0.2.3`，GPT娘再次使用 `--replace` 无备份覆盖；样例与安装图集哈希一致，本地仍只有一个 `gpt-niang` 目录。
- English: The real Codex plugin is upgraded to `0.2.3`, and GPT娘 is again replaced in place with `--replace` and no backup; sample and installed atlas hashes match, with exactly one local `gpt-niang` directory.

### 2026-07-11 — 拒绝单帧闪现表情 / Reject single-frame expression flashes

- 中文：原默认门槛允许两次头部变化，导致“相同脸 → 单帧特殊脸 → 相同脸”的孤立表情仍可通过；最低头部区域变化次数现从 2 提升为 3，明确拒绝只形成进入/退出两次变化的单帧表情。
- English: The former default allowed two head changes, so an isolated “same face → one special face → same face” accent could pass; the minimum head-region transition count is now raised from two to three, explicitly rejecting a single-frame expression with only enter/exit changes.
- 中文：工作流 JSON 新增 `expressionContinuityGate`，覆盖待机、招呼、悬停疑惑、失败、等待、托腮思考与复核行；生成规则与文档统一要求表情在至少三次相邻帧变化中自然发展。
- English: Workflow JSON now includes `expressionContinuityGate` for idle, greeting, hover curiosity, failed, waiting, hand-under-chin thinking, and review rows; generation rules and documentation consistently require expression to evolve naturally across at least three adjacent-frame transitions.
- 中文：新增保持下半身动作不同、但让头部仅在一帧变化的失败测试，证明门槛针对表情时间线而不是依赖整帧重复检测；完整 11 项测试、技能校验、插件校验与 GPT娘样例重验全部通过。
- English: Added a failure test that keeps lower-body motion distinct while changing the head in only one frame, proving the gate targets the expression timeline rather than relying on whole-frame duplicate detection; all eleven tests, skill validation, plugin validation, and GPT娘 sample revalidation pass.
- 中文：GitHub `main`、`v0.2.4` 标签与公开 Release 已同步：`https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.2.4`；源码与 GPT娘直装包均已上传，发布说明继续遵守中文段落在对应英文之前。
- English: GitHub `main`, the `v0.2.4` tag, and the public Release are synchronized at `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.2.4`; source and direct GPT娘 packages are uploaded, with every Chinese paragraph before its matching English paragraph.
- 中文：真实 Codex 插件已升级到 `0.2.4`，GPT娘以 `--replace` 无备份覆盖；样例与安装图集哈希一致，本地仅有一个 `gpt-niang` 目录。
- English: The real Codex plugin is upgraded to `0.2.4`, and GPT娘 is replaced with `--replace` and no backup; sample and installed atlas hashes match, with exactly one local `gpt-niang` directory.

### 2026-07-11 — 无损提示压缩与最小重试包 / Lossless prompt compaction and minimal retry packet

- 中文：逐行动作提示中重复十次的身份锁由 742 字符压缩到 518 字符，保留头身、脸眼、头发、肩髋、四肢/手脚长度体积、服装结构/饰品侧别、配色线条、实际高度、基线与安全区全部约束；每次完整生产流程约减少 560 个提示 Token，未删除质量门槛。
- English: The identity lock repeated across ten image jobs is compacted from 742 to 518 characters while retaining every head/body, face/eye, hair, shoulder/hip, limb/hand/shoe length-volume, garment/ornament-side, palette/line, practical-height, baseline, and safe-box invariant; one production run saves roughly 560 prompt tokens with no quality gate removed.
- 中文：`prompt-budget.json` 记录每个提示的字符数、保守 Token 上限、节省量与 `qualityGatesRemoved: 0`；`pet-workflow.json.retryPolicy` 规定失败时只复用原 canonical/turnaround 重做完整失败行，聊天只返回失败行、门槛、提示路径和最终状态。
- English: `prompt-budget.json` records per-prompt characters, a conservative token ceiling, savings, and `qualityGatesRemoved: 0`; `pet-workflow.json.retryPolicy` requires reusing the original canonical/turnaround to regenerate only the complete failed row, while chat reports only failed row, gates, prompt path, and final status.
- 中文：新增契约测试把身份锁上限固定为 520 字符、单流程至少节省 550 个估算提示 Token，并证明单参考输入与全部质量门槛保持不变；完整 11 项测试、技能校验、插件校验及 GPT娘预算审计均通过。
- English: Added contract tests capping the identity lock at 520 characters, requiring at least 550 estimated prompt tokens saved per run, and proving one-reference input plus all quality gates remain intact; all eleven tests, skill validation, plugin validation, and GPT娘 budget audit pass.
- 中文：GitHub `main`、`v0.2.5` 标签与公开 Release 已同步：`https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.2.5`；源码和 GPT娘直装包均已上传，说明继续采用中文段落在对应英文之前。
- English: GitHub `main`, the `v0.2.5` tag, and the public Release are synchronized at `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.2.5`; source and direct GPT娘 packages are uploaded, with each Chinese paragraph before its matching English paragraph.
- 中文：真实 Codex 插件已升级到 `0.2.5`，GPT娘以 `--replace` 无备份覆盖；样例与安装图集哈希一致，本地仅有一个 `gpt-niang` 目录。
- English: The real Codex plugin is upgraded to `0.2.5`, and GPT娘 is replaced with `--replace` and no backup; sample and installed atlas hashes match, with exactly one local `gpt-niang` directory.

### 2026-07-11 — 同一动作行内的严格体型锁 / Strict within-action body-scale lock

- 中文：仅对照正面待机的全局轮廓允许合理的方向差异，但不足以严格识别同一次行走循环中某一帧突然变小、变瘦或衣物尺度变化；验证器现为每条动作行建立八段轮廓中位基准，单帧平均漂移超过 `0.025` 即拒绝。
- English: A global silhouette comparison against front idle allows legitimate direction differences but cannot strictly isolate one frame suddenly becoming smaller, thinner, or differently clothed within a gait; the validator now builds an eight-band median reference per action row and rejects per-frame mean drift above `0.025`.
- 中文：门槛与方向无关：三分之四视角可整体区别于正面，但头、肩袖、躯干衣摆、腿和鞋在本行动的各相位必须保持同一模型体积；失败信息直接指出具体行列并要求整行重生。
- English: The gate is direction-neutral: a three-quarter view may differ globally from the front, but head, shoulder/sleeve, torso/hem, leg, and shoe volumes must remain the same model across action phases; failures identify the exact row/column and require complete-row regeneration.
- 中文：GPT娘九行动作全部通过，新门槛最差值为 `0.016868`；专项测试关闭全局 `0.11` 门槛后仍能独立拦截单帧身体/服装异常放大。
- English: All nine GPT娘 actions pass, with a worst-case new-gate value of `0.016868`; the focused test disables the global `0.11` gate and still independently rejects a single enlarged body/outfit frame.
- 中文：应用户要求实际更新宠物而非只升级验证器：原先偏瘦的等待、托腮思考、复核行分别应用经人工审查的 `1.1467 / 1.1416 / 1.1302` 整行横向校正；三行全局结构漂移降至 `0.03` 以下，同时保持 176px 高度、18px 头顶、14px 鞋底和原动作/表情时间线。
- English: Per the user's request, the pet itself—not only the validator—is updated: the formerly thin waiting, hand-under-chin thinking, and review rows receive reviewed whole-row width factors `1.1467 / 1.1416 / 1.1302`; global structural drift for all three falls below `0.03` while preserving 176px height, 18px head clearance, 14px shoe clearance, and the original motion/expression timelines.
- 中文：新增 `register_row_widths.py`，仅允许 0.75–1.25 的显式人工审查整行系数，并拒绝超过横向安全框的结果；已重建 GPT娘联系表、9 个 GIF、验证报告、裁切诊断和直装包，新图集 SHA256 为 `DE0BF9482611FEC46282C6112C075E4D9DABE1BD56A08B1F5F29E4DA79088743`。下一步为完整测试、v0.2.6 发布与本地覆盖。
- English: Added `register_row_widths.py`, accepting only explicit reviewed 0.75–1.25 whole-row factors and rejecting results beyond the horizontal safe box; rebuilt the GPT娘 contact sheet, nine GIFs, validation report, clipping diagnosis, and direct package, with new atlas SHA256 `DE0BF9482611FEC46282C6112C075E4D9DABE1BD56A08B1F5F29E4DA79088743`. Next actions are full tests, v0.2.6 publication, and local replacement.

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
- Published identity-metric release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.1.9`, with palette/proportion guards, source archive, and the validated direct GPT娘 package.
- Published Desktop-safe release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.2.0`, with the 8×9 renderer fix, uniform head-safe registration, source archive, and corrected GPT娘 direct package.
- Published completeness/diagnostic release: `https://github.com/tsingovo/codex-pet-forge/releases/tag/v0.2.1`, with connected-component completeness, cyclic motion uniformity, split-screen overlay diagnosis, source archive, and corrected GPT娘 package.

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
- 2026-07-11 — 配色与纵向比例一致性门槛 / Palette and vertical-proportion consistency gates
  - 中文：`validate_atlas.py` 新增每格 4×4×4 可见 RGB 直方图，与标准待机帧计算总变差距离，默认超过 25% 即拒绝，用于拦截头发、肤色、衣物和装饰主配色漂移。
  - English: `validate_atlas.py` now computes a 4×4×4 visible RGB histogram per cell and total-variation distance from canonical idle; drift above 25% is rejected to catch primary hair, skin, garment, and ornament color changes.
  - 中文：新增人物可见 alpha 的上/中/下三段质量分布，与标准待机帧比较，默认超过 15% 即拒绝，用作头部、躯干和腿部比例突变的自动代理指标。
  - English: Added top/middle/bottom visible-alpha mass comparison against canonical idle; drift above 15% is rejected as an automated proxy for head, torso, and leg proportion changes.
  - 中文：GPT娘 新样例在全部 79 个运行帧上通过配色、纵向比例、194px 高度、基线、单人物、重复帧、动作连续性与表情变化门槛；4 项单元测试和插件验证再次通过。
  - English: The updated GPT娘 sample passes palette, vertical proportion, 194px height, baseline, one-character, duplicate-frame, motion-continuity, and expression-change gates across all 79 runtime frames; four unit tests and plugin validation pass again.
- 2026-07-11 — v0.1.9 发布与本地启用 / v0.1.9 release and local activation
  - 中文：GitHub v0.1.9 已公开发布并上传源码与 GPT娘 直装包；真实用户 Codex 已升级并启用 `codex-pet-forge@0.1.9`。
  - English: GitHub v0.1.9 is publicly released with source and direct GPT娘 assets; the real user Codex installation now runs `codex-pet-forge@0.1.9`.
  - 中文：本地宠物仍只保留 `gpt-niang` 一个目录，无旧备份；其图集内容未因验证器升级而改变，并继续通过新门槛。
  - English: Only the `gpt-niang` local directory remains with no backup; its atlas content was unchanged by the validator upgrade and continues to pass the new gates.
