from __future__ import annotations

import json
import math
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
        image = Image.new("RGB", (1024, 1248), (255, 0, 255))
        draw = ImageDraw.Draw(image)
        cell_w, cell_h = 1024 / 8, 1248 / 9
        for row, used in enumerate(USED_COUNTS):
            for col in range(used):
                phase = 2 * math.pi * col / used
                cx = int((col + 0.5) * cell_w + 5 * math.cos(phase))
                dy = int(5 * math.sin(phase))
                y0 = int(row * cell_h + 15 + dy)
                y1 = int((row + 1) * cell_h - 15 + dy)
                color_shift = round(10 * math.sin(phase))
                second_shift = round(10 * math.cos(phase))
                draw.ellipse((cx - 24, y0, cx + 24, y1), fill=(40, 90 + color_shift, 160 + second_shift))
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
                unused = atlas.crop((6 * CELL_W, 0, 7 * CELL_W, CELL_H))
                self.assertEqual(unused.getchannel("A").getbbox(), None)
            self.run_script(
                "validate_atlas.py",
                str(run / "spritesheet.webp"),
                "--allow-chroma-fringe",
                "--chroma-key",
                "#FF00FF",
                "--json-out",
                str(run / "validation.json"),
            )
            self.assertTrue(json.loads((run / "validation.json").read_text(encoding="utf-8"))["ok"])

            rows_dir = run / "rows"
            rows_dir.mkdir()
            with Image.open(run / "spritesheet.png") as opened:
                atlas_png = opened.convert("RGBA")
            for row, count in enumerate(USED_COUNTS):
                atlas_png.crop((0, row * CELL_H, count * CELL_W, (row + 1) * CELL_H)).save(rows_dir / f"row-{row:02d}.png")
            self.run_script(
                "assemble_rows.py", "--rows-dir", str(rows_dir),
                "--output", str(run / "reassembled.webp"), "--png-output", str(run / "reassembled.png"),
            )
            self.run_script(
                "validate_atlas.py", str(run / "reassembled.webp"), "--allow-chroma-fringe",
                "--chroma-key", "#FF00FF", "--json-out", str(run / "reassembled-validation.json"),
            )
            self.assertTrue(json.loads((run / "reassembled-validation.json").read_text(encoding="utf-8"))["ok"])

            self.run_script("write_pet_manifest.py", "--pet-id", "momo", "--display-name", "Momo", "--description", "Test pet", "--output", str(run / "pet.json"))
            manifest = json.loads((run / "pet.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["spriteVersionNumber"], 1)
            result = self.run_script("install_pet.py", "--package-dir", str(run), "--codex-home", str(root / ".codex"), "--dry-run")
            self.assertTrue(json.loads(result.stdout)["ok"])

    def test_trigger_contract_is_explicit(self) -> None:
        text = (ROOT / "plugins" / "codex-pet-forge" / "skills" / "pet-forge" / "references" / "trigger-semantics.md").read_text(encoding="utf-8")
        self.assertIn("Pointer enter/hover selects", text)
        self.assertIn("horizontal movement only", text)
        self.assertIn("does not select an animation state", text)

    def test_identity_locked_prompt_pack_uses_one_reference_and_idle_timeline(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            reference = root / "single-reference.png"
            Image.new("RGB", (300, 400), "white").save(reference)
            run = root / "run"
            self.run_script(
                "prepare_identity_locked_run.py",
                "--reference", str(reference),
                "--pet-name", "Momo",
                "--output-dir", str(run),
            )
            workflow = json.loads((run / "pet-workflow.json").read_text(encoding="utf-8"))
            self.assertTrue(workflow["oneReferenceOnly"])
            self.assertEqual(workflow["userInputs"], ["reference.png"])
            self.assertEqual(len(workflow["jobs"]), 9)
            self.assertEqual(workflow["structuralIdentityGate"]["bands"], 8)
            self.assertEqual(workflow["structuralIdentityGate"]["maxSilhouetteWidthDrift"], 0.11)
            self.assertEqual(workflow["structuralIdentityGate"]["maxWithinRowSilhouetteDrift"], 0.025)
            self.assertEqual(workflow["expressionContinuityGate"]["minHeadRegionTransitions"], 3)
            self.assertTrue(workflow["expressionContinuityGate"]["rejectsSingleFrameAccent"])
            self.assertEqual(workflow["retryPolicy"]["scope"], "failed-complete-row-only")
            self.assertIn("full-atlas-regeneration", workflow["retryPolicy"]["forbidden"])
            budget = json.loads((run / "prompt-budget.json").read_text(encoding="utf-8"))
            self.assertLessEqual(budget["lockCharacters"], 520)
            self.assertGreaterEqual(budget["estimatedSavedPromptTokensPerRun"], 550)
            self.assertEqual(budget["qualityGatesRemoved"], 0)
            self.assertTrue((run / "prompts" / "01-turnaround.md").is_file())
            self.assertEqual(workflow["jobs"][0]["requiredInputs"][-1], "guides/row-00.png")
            with Image.open(run / "guides" / "row-00.png") as guide:
                self.assertEqual(guide.size, (6 * CELL_W, CELL_H))
            idle = (run / "prompts" / "row-00-idle.md").read_text(encoding="utf-8")
            self.assertIn("six runtime idle frames", idle)
            self.assertIn("no duplicate frames", idle)

    def test_validator_rejects_duplicate_animation_frame(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            generated = root / "generated.png"
            self.make_generated_atlas(generated)
            self.run_script(
                "normalize_generated_atlas.py", "--input", str(generated),
                "--output", str(root / "atlas.png"), "--webp-output", str(root / "atlas.webp"),
            )
            with Image.open(root / "atlas.png") as opened:
                atlas = opened.convert("RGBA")
            duplicate = atlas.crop((0, CELL_H, CELL_W, 2 * CELL_H))
            atlas.paste((0, 0, 0, 0), (CELL_W, CELL_H, 2 * CELL_W, 2 * CELL_H))
            atlas.alpha_composite(duplicate, (CELL_W, CELL_H))
            atlas.save(root / "duplicate.png")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_atlas.py"), str(root / "duplicate.png"), "--allow-chroma-fringe"],
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate/near-duplicate", result.stdout)

    def test_validator_rejects_palette_identity_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            generated = root / "generated.png"
            self.make_generated_atlas(generated)
            self.run_script(
                "normalize_generated_atlas.py", "--input", str(generated),
                "--output", str(root / "atlas.png"), "--webp-output", str(root / "atlas.webp"),
            )
            with Image.open(root / "atlas.png") as opened:
                atlas = opened.convert("RGBA")
            box = (0, 3 * CELL_H, CELL_W, 4 * CELL_H)
            cell = atlas.crop(box)
            recolored = [(250, 220, 20, alpha) if alpha > 0 else (0, 0, 0, 0) for _, _, _, alpha in cell.getdata()]
            cell.putdata(recolored)
            atlas.paste((0, 0, 0, 0), box)
            atlas.alpha_composite(cell, (0, 3 * CELL_H))
            atlas.save(root / "palette-drift.png")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_atlas.py"), str(root / "palette-drift.png"), "--allow-chroma-fringe"],
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("palette drift", result.stdout)

    def test_validator_rejects_shoulder_torso_and_clothing_scale_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            generated = root / "generated.png"
            self.make_generated_atlas(generated)
            self.run_script(
                "normalize_generated_atlas.py", "--input", str(generated),
                "--output", str(root / "atlas.png"), "--webp-output", str(root / "atlas.webp"),
            )
            with Image.open(root / "atlas.png") as opened:
                atlas = opened.convert("RGBA")
            # Keep height, baseline, palette, connectivity, and safe margins valid,
            # but replace one pose with an implausibly wide body/outfit. The new
            # eight-band structural profile must reject what a height-only gate
            # would accept as the same character.
            box = (0, 3 * CELL_H, CELL_W, 4 * CELL_H)
            atlas.paste((0, 0, 0, 0), box)
            draw = ImageDraw.Draw(atlas)
            draw.ellipse((10, 3 * CELL_H + 16, 181, 3 * CELL_H + 191), fill=(40, 90, 160, 255))
            path = root / "body-outfit-scale-drift.png"
            atlas.save(path)
            result = subprocess.run(
                [
                    sys.executable, str(SCRIPTS / "validate_atlas.py"), str(path),
                    "--allow-chroma-fringe", "--max-silhouette-width-drift", "1",
                ],
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("changes body/outfit scale within the action row", result.stdout)

    def test_desktop_validator_rejects_eleven_row_install_atlas(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            # A valid-looking 11-row sheet must still be rejected by default:
            # Desktop CSS slices exactly 8x9 and would mix vertical rows.
            atlas = Image.new("RGBA", (ATLAS_W, 11 * CELL_H), (0, 0, 0, 0))
            for row, count in enumerate((*USED_COUNTS, 8, 8)):
                for column in range(count):
                    ImageDraw.Draw(atlas).ellipse(
                        (column * CELL_W + 48, row * CELL_H + 24, column * CELL_W + 144, row * CELL_H + 184),
                        fill=(40, 90, 160, 255),
                    )
            path = root / "eleven-row.png"
            atlas.save(path)
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_atlas.py"), str(path), "--allow-chroma-fringe"],
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("1536x1872", result.stdout)

    def test_validator_rejects_head_touching_cell_top(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            generated = root / "generated.png"
            self.make_generated_atlas(generated)
            self.run_script(
                "normalize_generated_atlas.py", "--input", str(generated),
                "--output", str(root / "atlas.png"), "--webp-output", str(root / "atlas.webp"),
            )
            with Image.open(root / "atlas.png") as opened:
                atlas = opened.convert("RGBA")
            cell = atlas.crop((0, 0, CELL_W, CELL_H))
            bbox = cell.getchannel("A").getbbox()
            self.assertIsNotNone(bbox)
            sprite = cell.crop(bbox)
            atlas.paste((0, 0, 0, 0), (0, 0, CELL_W, CELL_H))
            atlas.alpha_composite(sprite, ((CELL_W - sprite.width) // 2, 0))
            path = root / "head-clipped-risk.png"
            atlas.save(path)
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_atlas.py"), str(path), "--allow-chroma-fringe"],
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("above the visible head/hair", result.stdout)

    def test_validator_rejects_detached_sprite_fragment(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            generated = root / "generated.png"
            self.make_generated_atlas(generated)
            self.run_script(
                "normalize_generated_atlas.py", "--input", str(generated),
                "--output", str(root / "atlas.png"), "--webp-output", str(root / "atlas.webp"),
            )
            with Image.open(root / "atlas.png") as opened:
                atlas = opened.convert("RGBA")
            # Simulate an isolated shoe/limb fragment inside the safe cell.
            ImageDraw.Draw(atlas).rectangle((8, 150, 31, 181), fill=(40, 90, 160, 255))
            path = root / "detached-fragment.png"
            atlas.save(path)
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_atlas.py"), str(path), "--allow-chroma-fringe"],
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("outside the main connected character", result.stdout)

    def test_validator_reports_uneven_motion_steps(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            generated = root / "generated.png"
            self.make_generated_atlas(generated)
            self.run_script(
                "normalize_generated_atlas.py", "--input", str(generated),
                "--output", str(root / "atlas.png"), "--webp-output", str(root / "atlas.webp"),
            )
            result = subprocess.run(
                [
                    sys.executable, str(SCRIPTS / "validate_atlas.py"), str(root / "atlas.png"),
                    "--allow-chroma-fringe", "--max-motion-step-cv", "0.01",
                ],
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("motion-step variation", result.stdout)

    def test_validator_rejects_expression_confined_to_one_frame(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            generated = root / "generated.png"
            self.make_generated_atlas(generated)
            self.run_script(
                "normalize_generated_atlas.py", "--input", str(generated),
                "--output", str(root / "atlas.png"), "--webp-output", str(root / "atlas.webp"),
            )
            with Image.open(root / "atlas.png") as opened:
                atlas = opened.convert("RGBA")
            row = 6
            head = atlas.crop((0, row * CELL_H, CELL_W, row * CELL_H + 120))
            # Preserve distinct lower-body motion in every frame, but make the
            # head identical except for column 3. This produces only the enter
            # and exit transitions of a single-frame expression accent.
            for column in (1, 2, 4, 5):
                box = (column * CELL_W, row * CELL_H, (column + 1) * CELL_W, row * CELL_H + 120)
                atlas.paste((0, 0, 0, 0), box)
                atlas.alpha_composite(head, (column * CELL_W, row * CELL_H))
            path = root / "one-frame-expression.png"
            atlas.save(path)
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_atlas.py"), str(path), "--allow-chroma-fringe"],
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("changes the head/expression region in only 2 transitions", result.stdout)

    def test_reviewed_row_width_repair_preserves_height_and_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            generated = root / "generated.png"
            self.make_generated_atlas(generated)
            self.run_script(
                "normalize_generated_atlas.py", "--input", str(generated),
                "--output", str(root / "atlas.png"), "--webp-output", str(root / "atlas.webp"),
            )
            self.run_script(
                "register_row_widths.py", str(root / "atlas.webp"),
                "--row-scale", "6=1.10", "--output", str(root / "repaired.webp"),
            )
            with Image.open(root / "atlas.webp") as opened:
                before = opened.convert("RGBA").crop((0, 6 * CELL_H, CELL_W, 7 * CELL_H)).getchannel("A").getbbox()
            with Image.open(root / "repaired.webp") as opened:
                after = opened.convert("RGBA").crop((0, 6 * CELL_H, CELL_W, 7 * CELL_H)).getchannel("A").getbbox()
            self.assertIsNotNone(before)
            self.assertIsNotNone(after)
            self.assertEqual(before[1], after[1])
            self.assertEqual(before[3], after[3])
            self.assertGreater(after[2] - after[0], before[2] - before[0])


if __name__ == "__main__":
    unittest.main()
