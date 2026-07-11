# Codex Desktop playback contract

Verified read-only against Codex Desktop `26.707.3748.0`.

## Automatic idle

The host enters `idle` automatically whenever no other mascot state is active.
It plays exactly row 0 columns 0-5 in a loop. Base durations are:

`280, 110, 110, 140, 140, 320 ms`

The current host multiplies each idle duration by 6, producing:

`1680, 660, 660, 840, 840, 1920 ms`

Total loop duration is `6600 ms`. Column 6 is not a neutral fallback and is not
referenced. A useful pet must therefore make all six slow phases readable without
large random gestures: inhale, blink start, closed-eye smile, reopen with tiny
head/gaze shift, warm exhale, and exact calm return.

## Active states

For a non-idle state, the host plays that state's configured frame sequence three
times, then appends the slow idle sequence and loops from the beginning of the
active sequence. Custom `pet.json` files cannot change frame counts, durations,
repeat count, or event mappings in the current Desktop build.

Quality and token consequences:

- generate only six idle figures, never a seventh unused neutral figure
- use every host-referenced cell with distinct, evenly phased artwork
- do not spend tokens inventing unsupported FPS or animation manifest fields
- encode visible idle personality inside the six automatic frames
