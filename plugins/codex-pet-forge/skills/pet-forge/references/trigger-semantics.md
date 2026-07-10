# Runtime trigger semantics

Verified against Codex Desktop `26.707.3748.0` local frontend resources.

- Pointer enter/hover selects the state named `jumping` (atlas row 4).
- Drag selection examines horizontal movement only.
- Horizontal delta `>= 4` selects `running-right`.
- Horizontal delta `<= -4` selects `running-left`.
- Vertical delta marks a drag as moved but does not select an animation state.
- After a horizontal state is selected, later vertical-only movement can retain it.

Therefore:

- Never put a vertical-lift animation in row 4; it will play on hover.
- Never promise a vertical-drag animation from pet assets alone.
- Treat state names as compatibility identifiers, not literal motion descriptions.
- Keep these facts isolated here because future Codex builds may change them.
