from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins" / "codex-pet-forge" / "skills" / "pet-forge" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from pet_common import ATLAS_H, ATLAS_W, CELL_H, CELL_W, USED_COUNTS


class PetForgeTests(unittest.TestCase):
    def run_script(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPTS / name), *args], check=True, text=True, capture_output=True)

    def make_generated_atlas(self, path: Path) -> None:
        image = Image.new("RGB", (1024, 1536), (255, 0, 255))
        draw = ImageDraw.Draw(image)
        cell_w, cell_h = 1024 / 8, 1536 / 11
        for row, used in enumerate(USED_COUNTS):
            for col in range(used):
                cx = int((col + 0.5) * cell_w)
                y0 = int(row * cell_h + 15)
                y1 = int((row + 1) * cell_h - 15)
                draw.ellipse((cx - 24, y0, cx + 24, y1), fill=(20 + row * 8, 80, 160))
        image.save(path)

    def test_prepare_normalize_manifest_and_install_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            reference = root / "ref.png"
            Image.new("RGB", (300, 400), "white").save(reference)
            run = root / "run"
            self.run_script("prepare_fast_pet.py", "--reference", str(reference), "--pet-name", "Momo", "--output-dir", str(run))
            self.assertTrue((run / "generation-prompt.md").is_file())
            with Image.open(run / "atlas-layout-guide.png") as guide:
                self.assertEqual(guide.size, (ATLAS_W, ATLAS_H))

            generated = run / "generated-atlas.png"
            self.make_generated_atlas(generated)
            self.run_script("normalize_generated_atlas.py", "--input", str(generated), "--output", str(run / "spritesheet.png"), "--webp-output", str(run / "spritesheet.webp"))
            self.run_script(
                "despill_chroma_edges.py",
                str(run / "spritesheet.png"),
                "--output",
                str(run / "spritesheet.png"),
                "--webp-output",
                str(run / "spritesheet.webp"),
                "--chroma-key",
                "#FF00FF",
                "--json-out",
                str(run / "chroma-report.json"),
            )
            with Image.open(run / "spritesheet.webp") as atlas:
                self.assertEqual(atlas.size, (ATLAS_W, ATLAS_H))
                self.assertEqual(atlas.mode, "RGBA")
                unused = atlas.crop((7 * CELL_W, 0, 8 * CELL_W, CELL_H))
                self.assertEqual(unused.getchannel("A").getbbox(), None)
            self.run_script(
                "validate_atlas.py",
                str(run / "spritesheet.webp"),
                "--require-v2",
                "--chroma-key",
                "#FF00FF",
                "--json-out",
                str(run / "validation.json"),
            )
            self.assertTrue(json.loads((run / "validation.json").read_text(encoding="utf-8"))["ok"])

            self.run_script("write_pet_manifest.py", "--pet-id", "momo", "--display-name", "Momo", "--description", "Test pet", "--output", str(run / "pet.json"))
            manifest = json.loads((run / "pet.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["spriteVersionNumber"], 2)
            result = self.run_script("install_pet.py", "--package-dir", str(run), "--codex-home", str(root / ".codex"), "--dry-run")
            self.assertTrue(json.loads(result.stdout)["ok"])

    def test_trigger_contract_is_explicit(self) -> None:
        text = (ROOT / "plugins" / "codex-pet-forge" / "skills" / "pet-forge" / "references" / "trigger-semantics.md").read_text(encoding="utf-8")
        self.assertIn("Pointer enter/hover selects", text)
        self.assertIn("horizontal movement only", text)
        self.assertIn("does not select an animation state", text)


if __name__ == "__main__":
    unittest.main()
