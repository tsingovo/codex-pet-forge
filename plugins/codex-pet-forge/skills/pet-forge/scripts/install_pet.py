from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

from pet_common import ATLAS_H, ATLAS_W, slugify


def main() -> None:
    ap = argparse.ArgumentParser(description="Atomically install a validated Codex pet package")
    ap.add_argument("--package-dir", required=True)
    ap.add_argument("--codex-home")
    ap.add_argument("--replace", action="store_true")
    ap.add_argument("--backup", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    package = Path(args.package_dir).expanduser().resolve()
    manifest_path = package / "pet.json"
    sheet_path = package / "spritesheet.webp"
    if not manifest_path.is_file() or not sheet_path.is_file():
        raise SystemExit("package must contain pet.json and spritesheet.webp")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    required = {"id", "displayName", "description", "spriteVersionNumber", "spritesheetPath"}
    if not required.issubset(manifest) or manifest["spriteVersionNumber"] != 1:
        raise SystemExit("invalid desktop pet manifest: spriteVersionNumber must be 1 (8x9 atlas)")
    with Image.open(sheet_path) as image:
        if image.size != (ATLAS_W, ATLAS_H) or image.mode != "RGBA":
            raise SystemExit(f"spritesheet must be RGBA {ATLAS_W}x{ATLAS_H}")

    home = Path(args.codex_home).expanduser().resolve() if args.codex_home else Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve()
    pets = home / "pets"
    target = pets / slugify(manifest["id"])
    result = {"ok": True, "target": str(target), "dryRun": args.dry_run}
    if args.dry_run:
        print(json.dumps(result))
        return
    pets.mkdir(parents=True, exist_ok=True)
    if target.exists() and not args.replace:
        raise SystemExit(f"pet already exists: {target}; use --replace")
    if target.exists() and args.backup:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = pets / f"{target.name}.backup-{stamp}"
        shutil.copytree(target, backup)
        result["backup"] = str(backup)

    staging = Path(tempfile.mkdtemp(prefix=f".{target.name}-", dir=pets))
    try:
        shutil.copy2(manifest_path, staging / "pet.json")
        shutil.copy2(sheet_path, staging / "spritesheet.webp")
        if target.exists():
            shutil.rmtree(target)
        staging.replace(target)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    print(json.dumps(result))


if __name__ == "__main__":
    main()
