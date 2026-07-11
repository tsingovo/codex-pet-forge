# Codex Desktop atlas contract

- Canvas: `1536x1872` RGBA.
- Grid: 8 columns x 9 rows.
- Cell: `192x208`.
- Manifest: `spriteVersionNumber: 1`.
- Fully transparent pixels must have RGB `(0,0,0)`.
- This is a runtime contract, not just a validator preference: the current
  desktop renderer uses `background-size: 800% 900%`. Never install an 11-row
  sheet; it will be vertically resampled and can mix character rows.

| Row | Runtime state | Used columns | Visual purpose |
|---:|---|---:|---|
| 0 | idle | 0-5 | six slow automatic idle phases; columns 6-7 are unused |
| 1 | running-right | 0-7 | drag toward screen-right |
| 2 | running-left | 0-7 | drag toward screen-left |
| 3 | waving | 0-3 | greeting/attention |
| 4 | jumping | 0-4 | actual mouse-hover curiosity reaction |
| 5 | failed | 0-7 | soft failure/deflated reaction |
| 6 | waiting | 0-5 | waiting for user input/approval |
| 7 | running | 0-5 | active processing; stable hand-under-chin thinking |
| 8 | review | 0-5 | inspect/pleased confirmation |

## Playback invariants

- Row 0 columns 0-5 are the complete automatic idle loop used when no other state is active. Columns 6-7 must be transparent because the current host never references them.
- Runtime frame counts and playback cadence are host-controlled. A pet cannot declare a custom FPS in `pet.json`.
- Smoothness therefore requires every available runtime frame to be distinct, evenly phased, and loop-compatible; duplicating a pose lowers effective frame rate and is rejected.
- Expressive rows 0 and 3-8 must develop the face across multiple frames, not reserve expression for one isolated frame.
