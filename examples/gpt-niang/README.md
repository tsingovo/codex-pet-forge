# GPT娘 sample pet

A ready-to-use Codex v2 pet package created from the reference image shown below.

## Preview

| Reference supplied for this sample | Generated Codex v2 pet atlas |
| --- | --- |
| ![GPT娘 reference](reference.png) | ![GPT娘 contact sheet](contact-sheet.png) |

## Install directly

1. Download [`gpt-niang-pet.zip`](gpt-niang-pet.zip) from this folder or from the matching GitHub release.
2. Extract it, then copy the contained `gpt-niang` folder into your Codex pets directory:

   ```powershell
   Copy-Item .\gpt-niang "$HOME\.codex\pets\gpt-niang" -Recurse -Force
   ```

3. Restart Codex or refresh the pet list, then select **GPT娘**.

The package contains a `spriteVersionNumber: 2` manifest and a validated 8x11 WebP atlas. The animation includes hover curiosity, waiting, gentle failure, hand-under-chin thinking, review, horizontal drag, and look directions.

### v0.1.2 animation repair

The hover-curiosity and both horizontal-drag rows were regenerated as complete rows to correct a reported misplaced/cropped foot. Do not mix individual cells from older packages with this version.

## Asset notice

The code in this repository is Apache-2.0. This example's character reference was supplied by the project user for this demonstration; do not treat the repository code license as permission to reuse third-party character art, trademarks, or reference images outside the rights you hold.
