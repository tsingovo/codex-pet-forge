# Codex Pet Forge / Codex 宠物锻造器

将人物参考图转换为经验证的 Codex v2 动态宠物。
Turn a character reference image into a validated Codex v2 animated pet.

> 版权所有 © 2026 HASEE。详见 NOTICE 与 LICENSE。
> Copyright (c) 2026 HASEE. See [NOTICE](NOTICE) and [LICENSE](LICENSE).

## 生产级身份锁定 / Production identity lock

正式宠物先生成并确认一张标准全身形象；后续每个动作行都必须以它为唯一角色依据，只允许改变姿势与表情。
A production pet starts with one approved canonical full-body image; every action row must use it as the sole character model and may change only pose/expression.

这会固定头身比、脸型、发型、服装、鞋子、配色、线条、实际尺寸和脚底基线；快速整图生成仅用于草稿。
This locks head/body ratio, face, hair, outfit, shoes, palette, line weight, practical scale, and baseline; fast full-atlas generation is draft-only.

## 安装插件 / Install the plugin

先添加公开市场，再安装插件。
Add the public marketplace, then install the plugin.

```powershell
codex plugin marketplace add tsingovo/codex-pet-forge
codex plugin add codex-pet-forge@codex-pet-forge
```

该市场不会自动出现在 Codex 全局搜索中；每位用户添加一次后，会出现在自己的插件列表。
This marketplace is not automatically indexed by Codex global search; after each user adds it once, it appears in that user's plugin list.

## 使用方式 / How to use

上传人物参考图后，要求 Codex 使用 Pet Forge 的“身份锁定工作流”。
Upload a character reference image, then ask Codex to use Pet Forge's identity-locked workflow.

示例提示词：`根据这张图创建宠物。先确认标准全身形象，再逐行动作生成；所有动作必须锁定同一头身比和服装。`
Example prompt: `Create a pet from this image. Approve a canonical full-body character first, then generate actions row by row; lock the same proportions and outfit in every action.`

验证器会检查图集尺寸、透明背景、空单元格、脚底基线和跨行动作的可见高度漂移；安装前仍必须检查联系表。
The validator checks atlas geometry, transparency, empty cells, shoe baseline, and cross-row visible-height drift; the contact sheet still requires review before installation.

## GPT娘样例 / GPT娘 example

仓库提供完整的 GPT娘 身份锁定样例，包括原始参考、标准形象、最终联系表和可直接安装包。
The repository includes a complete identity-locked GPT娘 example with its source reference, canonical character, final contact sheet, and direct install package.

| 参考图 / Reference | 标准形象 / Canonical model | 最终图集 / Final atlas |
| --- | --- | --- |
| ![参考图](examples/gpt-niang/reference.png) | ![标准形象](examples/gpt-niang/canonical.png) | ![最终图集](examples/gpt-niang/contact-sheet.png) |

可从 [gpt-niang-pet.zip](examples/gpt-niang/gpt-niang-pet.zip) 下载并解压，然后将 `gpt-niang` 文件夹复制到 `$HOME/.codex/pets/gpt-niang`。
Download and extract [gpt-niang-pet.zip](examples/gpt-niang/gpt-niang-pet.zip), then copy the `gpt-niang` folder to `$HOME/.codex/pets/gpt-niang`.

## 许可与交接 / License and handoff

代码和文档采用 Apache-2.0；用户参考图及角色资产不因代码许可而自动获得再分发权。
Code and documentation use Apache-2.0; user reference art and character assets do not automatically receive redistribution rights through the code license.

每次涉及行为、脚本、提示词、版本、许可证或 GitHub 的修改，都必须同一提交更新 [HANDOFF.md](HANDOFF.md)。
Every change to behavior, scripts, prompts, versions, licensing, or GitHub must update [HANDOFF.md](HANDOFF.md) in the same commit.
