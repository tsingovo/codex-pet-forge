from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Distinguish atlas cell clipping from Codex overlay-window bounds clipping"
    )
    parser.add_argument("atlas")
    parser.add_argument("--chroma-key", default="#FF00FF")
    parser.add_argument("--json-out")
    args = parser.parse_args()

    atlas = Path(args.atlas).expanduser().resolve()
    validator = Path(__file__).with_name("validate_atlas.py")
    with tempfile.TemporaryDirectory() as temp:
        report_path = Path(temp) / "validation.json"
        process = subprocess.run(
            [
                sys.executable,
                str(validator),
                str(atlas),
                "--chroma-key",
                args.chroma_key,
                "--json-out",
                str(report_path),
            ],
            text=True,
            capture_output=True,
        )
        validation = json.loads(report_path.read_text(encoding="utf-8"))

    used = [cell for cell in validation.get("cells", []) if cell.get("used")]
    safe_edges = bool(used) and all(
        cell.get("top_safe_padding", 0) >= 10
        and cell.get("bottom_safe_padding", 0) >= 8
        and cell.get("left_safe_padding", 0) >= 4
        and cell.get("right_safe_padding", 0) >= 4
        for cell in used
    )
    asset_safe = process.returncode == 0 and validation.get("desktop_installable") is True and safe_edges
    result = {
        "ok": asset_safe,
        "atlas": str(atlas),
        "asset_safe": asset_safe,
        "desktop_installable": validation.get("desktop_installable", False),
        "all_used_cells_inside_safe_box": safe_edges,
        "classification": (
            "host-overlay-bounds-desynchronization-likely"
            if asset_safe
            else "atlas-or-cell-geometry-failure"
        ),
        "guidance": (
            "The atlas is fully inside every 192x208 cell. If clipping appears only after split-screen "
            "or cross-display dragging and recovers after another drag, treat it as a Codex overlay "
            "BrowserWindow bounds/layout synchronization issue; do not regenerate character art."
            if asset_safe
            else "Repair the reported atlas validation errors before attributing clipping to the host."
        ),
        "validation_errors": validation.get("errors", []),
    }
    if args.json_out:
        Path(args.json_out).expanduser().resolve().write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if asset_safe else 1)


if __name__ == "__main__":
    main()
