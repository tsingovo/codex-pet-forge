# Identity-lock contract

Every production pet has exactly one approved **master character**. Treat that master as a reusable animation model, not as inspiration for independently redrawn poses.

## Required sequence

1. Generate one calm, front-facing, full-body canonical image from the user reference on a flat chroma-key background.
2. Approve its face, head-to-body ratio, hair silhouette, outfit construction, palette, shoes, and practical scale.
3. Attach that approved canonical image to **every** action-row and look-direction generation request. It is the primary identity input; the original user image is secondary provenance only.
4. Request pose-only changes. Do not ask the model to redesign, reinterpret, age/de-age, re-proportion, or restyle the character.
5. After each row, run structural validation and inspect the row beside the canonical image. If head/body scale, face, hair, clothing, or shoe construction drifts, reject and regenerate the entire row.

## Prompt clause (include verbatim in every row job)

```text
IDENTITY LOCK: The attached canonical full-body sprite is the sole character model.
Clone this exact same character into the requested pose sequence: identical head-to-body ratio,
face/eye shape, hairstyle and hair length, outfit cut, palette, shoes, line weight, practical
scale, and baseline. Change only pose, expression, gaze, or the explicitly requested limb
position. Do not redraw a variant, change proportions, add/remove garments, or change the
character's apparent age or body type.
```

## Acceptance gates

- Standard rows 0–8 must keep practical visible height within the validator's identity-height-drift limit relative to idle.
- Every row must preserve the same baseline and pass the per-row baseline-drift check.
- Direction rows may change apparent width for rotation, but must retain the master face, clothing, and scale.
- Passing numeric checks is necessary but not sufficient: contact-sheet visual review remains the final identity gate.
