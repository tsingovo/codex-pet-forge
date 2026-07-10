# Codex v2 atlas contract

- Canvas: `1536x2288` RGBA.
- Grid: 8 columns x 11 rows.
- Cell: `192x208`.
- Manifest: `spriteVersionNumber: 2`.
- Fully transparent pixels must have RGB `(0,0,0)`.

| Row | Runtime state | Used columns | Visual purpose |
|---:|---|---:|---|
| 0 | idle | 0-6 | calm breathing/blinking; column 6 is neutral fallback |
| 1 | running-right | 0-7 | drag toward screen-right |
| 2 | running-left | 0-7 | drag toward screen-left |
| 3 | waving | 0-3 | greeting/attention |
| 4 | jumping | 0-4 | actual mouse-hover curiosity reaction |
| 5 | failed | 0-7 | soft failure/deflated reaction |
| 6 | waiting | 0-5 | waiting for user input/approval |
| 7 | running | 0-5 | active processing; stable hand-under-chin thinking |
| 8 | review | 0-5 | inspect/pleased confirmation |
| 9 | look A | 0-7 | 000, 022.5, 045, 067.5, 090, 112.5, 135, 157.5 |
| 10 | look B | 0-7 | 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5 |

`000` means up. `090` means screen-right. `180` means down. `270` means screen-left.

## Playback invariants

- Row 0 columns 0-5 are the automatic idle loop used when no other action state is active; column 6 is the neutral fallback, not a seventh idle phase.
- Runtime frame counts and playback cadence are host-controlled. A pet cannot declare a custom FPS in `pet.json`.
- Smoothness therefore requires every available runtime frame to be distinct, evenly phased, and loop-compatible; duplicating a pose lowers effective frame rate and is rejected.
- Expressive rows 0 and 3-8 must develop the face across multiple frames, not reserve expression for one isolated frame.
