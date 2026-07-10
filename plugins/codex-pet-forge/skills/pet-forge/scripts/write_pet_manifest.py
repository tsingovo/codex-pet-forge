from __future__ import annotations

import argparse
import json
from pathlib import Path

from pet_common import slugify


def main() -> None:
    ap = argparse.ArgumentParser(description="Write a Codex Desktop-compatible pet.json")
    ap.add_argument("--pet-id", required=True)
    ap.add_argument("--display-name", required=True)
    ap.add_argument("--description", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    data = {
        "id": slugify(args.pet_id),
        "displayName": args.display_name,
        "description": args.description,
        # Desktop currently has a fixed 8x9 renderer.  Version 1 makes that
        # contract explicit and prevents a 11-row terminal-only atlas from
        # being mistaken for a desktop sprite sheet.
        "spriteVersionNumber": 1,
        "spritesheetPath": "spritesheet.webp",
    }
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(data, ensure_ascii=True))


if __name__ == "__main__":
    main()
