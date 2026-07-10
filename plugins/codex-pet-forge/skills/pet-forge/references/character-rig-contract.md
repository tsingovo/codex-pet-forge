# Character rig and motion contract

## One-reference input

The user supplies exactly one reference image. The workflow derives two internal assets before any animation: `canonical.png` (the immutable front model) and `turnaround.png` (eight orthographic directions). Users are never asked to provide extra model sheets.

## Immutable model structure

Treat the character like one rigged 3D model rendered into sprites. Lock these properties after canonical approval:

- head height as the unit; total body height and shoulder/hip width in head units
- face outline, eye spacing/size, nose/mouth placement, ear position
- neck, shoulder, upper/lower arm, hand, thigh, calf, and shoe proportions
- hairstyle parting, front/side/back hair masses, curls, ribbons, ears, horns, or tail roots
- every garment layer, hem length, sleeve volume, seam, buckle, bow, badge, and asymmetric ornament
- palette, outline weight, material shading, camera projection, practical sprite height, and shoe baseline

An action may deform cloth/hair naturally but may not add, remove, swap sides, resize, or redesign a structure.

## Complete-frame rule

Every occupied cell contains exactly one complete character from highest hair/effect to both shoes. Reject a row when the model returns fewer figures than requested, multiple figures in one slot, neighboring fragments, cropped anatomy, disconnected limbs, or a replacement foot/face copied from another generation. Regenerate the complete row; never compensate by grouping, duplicating, or patching isolated body parts.

## Motion and expression

- Use every runtime frame. Adjacent frames must be distinct, evenly phased, and lead naturally into the next frame and back to frame 0.
- Each action has a physical intention and a beginning, development, and return. Random limb motion is not animation.
- Expression is a timeline, not a single accent frame. At least three frames in every expressive row must change eyes, brows, and/or mouth naturally.
- Keep body mass stable. Movement comes from joint rotation, weight shift, cloth/hair follow-through, gaze, and expression—not character scaling.
- Row 0 is the automatic idle loop when no other state is active: breathing, blink, tiny gaze change, return. It must visibly animate while staying calm.
- Codex runtime frame counts and playback cadence are fixed by the host. Smoothness comes from using all available frames without duplicates, not by inventing unsupported manifest FPS settings.

## Direction model

Direction rows are rotations of the same rig under an orthographic camera. Preserve height, head/body ratio, clothing construction, and the physical side of asymmetric decorations through all 16 angles. Do not mirror asymmetric characters as a shortcut.

## Token discipline

Quality gates are never shortened. Token savings come from storing the canonical contract, prompts, frame timelines, and QA reports in files; the chat reports only selected paths, concrete failures, and final results. Generate only failed complete rows again—not the full pet and not isolated cells.
