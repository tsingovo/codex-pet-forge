# Runtime overlay clipping boundary

Verified read-only against Codex Desktop `26.707.3748.0` on Windows.

- The Desktop legacy avatar page uses a full-window root with `overflow-hidden`.
- Drag events send screen coordinates to the main process, which chooses a display,
  recalculates layout, and applies BrowserWindow content bounds.
- Element-size changes may be deferred while a moved-window persistence timer is active.
- The native composition path uses `overflow-visible`, but pet packages cannot select
  or configure the host presentation path.

Therefore, clipping that appears only after split-screen/cross-display dragging,
stays inside a fixed screen rectangle, and recovers after another drag is evidence
of transient host overlay-window bounds/layout desynchronization. It is not evidence
that a spritesheet cell is missing pixels when all cell safety gates pass.

Asset-side mitigation:

- install only the exact 1536x1872 8x9 Desktop atlas
- register every complete figure into the conservative inner safe box
- require top, bottom, left, and right padding on every used cell
- run `diagnose_overlay_clipping.py` before regenerating artwork

Never patch or redistribute Codex `app.asar`. A host-level fix belongs upstream.
