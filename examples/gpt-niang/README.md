# GPT娘 身份锁定样例 / GPT娘 identity-locked example

本样例先确认一张标准全身形象，再以该形象生成所有动作行。
This sample approves one canonical full-body character before generating every action row from it.

| 参考图 / Reference | 标准形象 / Canonical | 最终联系表 / Final contact sheet |
| --- | --- | --- |
| ![参考](reference.png) | ![标准](canonical.png) | ![联系表](contact-sheet.png) |

## 直接安装 / Direct install

下载并解压 [gpt-niang-pet.zip](gpt-niang-pet.zip)，再将其中的 `gpt-niang` 文件夹复制到 Codex 宠物目录。
Download and extract [gpt-niang-pet.zip](gpt-niang-pet.zip), then copy its `gpt-niang` folder to the Codex pets directory.

```powershell
Copy-Item .\gpt-niang "$HOME\.codex\pets\gpt-niang" -Recurse -Force
```

图集已通过 v2 结构、透明背景、脚底基线与跨行高度漂移校验；安装前仍建议查看联系表。
The atlas passed v2 geometry, transparency, baseline, and cross-row height-drift checks; review the contact sheet before installation.

代码采用 Apache-2.0；本样例的角色参考图不因代码许可而自动获得再分发权。
The code is Apache-2.0; this sample's character reference does not automatically receive redistribution rights through the code license.
