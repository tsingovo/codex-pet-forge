# GPT娘 身份锁定样例 / GPT娘 identity-locked example

本样例只接收一张用户参考图，内部生成标准全身形象和八方向转台，再以同一个人物结构生成所有动作行。
This sample accepts one user reference, internally derives a canonical full-body model and eight-view turnaround, then generates every action row from the same character structure.

| 参考图 / Reference | 标准形象 / Canonical | 八方向转台 / Turnaround | 最终联系表 / Final contact sheet |
| --- | --- | --- | --- |
| ![参考](reference.png) | ![标准](canonical.png) | ![转台](turnaround.png) | ![联系表](contact-sheet.png) |

## 动作预览 / Motion previews

以下 GIF 按 8 FPS 展示实际帧序列，用于检查待机触发、悬停疑惑和托腮思考的动作与表情连续性。
The GIFs below render the real frame sequences at 8 FPS to review motion and expression continuity for automatic idle, hover curiosity, and hand-under-chin thinking.

| 待机 / Idle | 悬停疑惑 / Hover curiosity | 托腮思考 / Thinking |
| --- | --- | --- |
| ![待机](motion-previews/row-00-idle.gif) | ![悬停](motion-previews/row-04-hover-curiosity.gif) | ![思考](motion-previews/row-07-thinking.gif) |

## 直接安装 / Direct install

下载并解压 [gpt-niang-pet.zip](gpt-niang-pet.zip)，再将其中的 `gpt-niang` 文件夹复制到 Codex 宠物目录。
Download and extract [gpt-niang-pet.zip](gpt-niang-pet.zip), then copy its `gpt-niang` folder to the Codex pets directory.

```powershell
Copy-Item .\gpt-niang "$HOME\.codex\pets\gpt-niang" -Recurse -Force
```

图集已通过桌面端 `1536×1872` / 8×9 结构、透明背景、单格人物数量、脚底基线、跨行高度、重复帧和动作连续性校验；安装前仍建议查看联系表与动作预览。
The atlas passed Desktop `1536×1872` / 8×9 geometry, transparency, per-cell figure count, baseline, cross-row height, duplicate-frame, and motion-continuity checks; review the contact sheet and motion previews before installation.

所有运行帧现已统一为 176px 可见高度并放入保守内安全框，降低桌面悬浮窗轻微裁切头发及分屏拖动窗口失步时的影响。
All runtime frames now use a uniform 176px visible height inside a conservative inner safe box, reducing hair clipping and the impact of transient overlay-window desynchronization during split-screen dragging.

代码采用 Apache-2.0；本样例的角色参考图不因代码许可而自动获得再分发权。
The code is Apache-2.0; this sample's character reference does not automatically receive redistribution rights through the code license.
