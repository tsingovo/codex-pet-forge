#!/usr/bin/env python3
"""Validate a Codex pet spritesheet atlas."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from statistics import median

from PIL import Image, ImageChops, ImageFilter

COLUMNS = 8
ROWS = 9
EXTENDED_ROWS = 11
CELL_WIDTH = 192
CELL_HEIGHT = 208
ATLAS_WIDTH = COLUMNS * CELL_WIDTH
ATLAS_HEIGHT = ROWS * CELL_HEIGHT
EXTENDED_ATLAS_HEIGHT = EXTENDED_ROWS * CELL_HEIGHT
ROW_BY_INDEX = {
    # Desktop's idle row owns seven populated cells: six loop poses plus the
    # neutral/rest frame used by the host's return-to-idle path.
    0: ("idle", 7),
    1: ("running-right", 8),
    2: ("running-left", 8),
    3: ("waving", 4),
    4: ("jumping", 5),
    5: ("failed", 8),
    6: ("waiting", 6),
    7: ("running", 6),
    8: ("review", 6),
    9: ("look-000-to-157.5", 8),
    10: ("look-180-to-337.5", 8),
}
EXTENDED_NEUTRAL_LOOK_FRAME = (0, 6)


def parse_hex_color(value: str) -> tuple[int, int, int]:
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        raise SystemExit(f"invalid chroma key color: {value}; expected #RRGGBB")
    return tuple(int(value[index : index + 2], 16) for index in (1, 3, 5))


def alpha_nonzero_count(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return sum(alpha.histogram()[1:])


def transparent_rgb_residue_count(image: Image.Image) -> int:
    rgba = image.convert("RGBA")
    data = rgba.tobytes()
    count = 0
    for index in range(0, len(data), 4):
        red, green, blue, alpha = data[index : index + 4]
        if alpha == 0 and (red or green or blue):
            count += 1
    return count


def color_distance(
    red: int,
    green: int,
    blue: int,
    key: tuple[int, int, int],
) -> float:
    return math.sqrt((red - key[0]) ** 2 + (green - key[1]) ** 2 + (blue - key[2]) ** 2)


def opaque_chroma_key_count(
    image: Image.Image,
    chroma_key: tuple[int, int, int],
    threshold: float,
) -> int:
    rgba = image.convert("RGBA")
    data = rgba.tobytes()
    count = 0
    for index in range(0, len(data), 4):
        red, green, blue, alpha = data[index : index + 4]
        if alpha > 16 and color_distance(red, green, blue, chroma_key) <= threshold:
            count += 1
    return count


def is_chroma_contaminated(
    color: tuple[int, int, int],
    chroma_key: tuple[int, int, int],
    distance_threshold: float,
) -> bool:
    return color_distance(*color, chroma_key) <= distance_threshold


def chroma_fringe_count(
    image: Image.Image,
    *,
    chroma_key: tuple[int, int, int],
    distance_threshold: float,
    edge_radius: int,
    alpha_minimum: int,
) -> int:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    visible = [value > 0 for value in alpha.getdata()]
    transparent = Image.new("L", alpha.size)
    transparent.putdata([255 if not value else 0 for value in visible])
    expanded = transparent.filter(ImageFilter.MaxFilter(edge_radius * 2 + 1))
    return sum(
        alpha_value >= alpha_minimum
        and nearby_transparency > 0
        and is_chroma_contaminated(
            color[:3],
            chroma_key,
            distance_threshold,
        )
        for color, alpha_value, nearby_transparency in zip(
            rgba.getdata(), alpha.getdata(), expanded.getdata()
        )
    )


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    """Return the visible-alpha bounds for registration checks."""
    return image.getchannel("A").getbbox()


def mean_frame_difference(first: Image.Image, second: Image.Image) -> float:
    """Return normalized mean absolute RGBA difference in the range 0..1."""
    diff = ImageChops.difference(first.convert("RGBA"), second.convert("RGBA"))
    data = diff.tobytes()
    return sum(data) / (len(data) * 255) if data else 0.0


def coarse_palette(image: Image.Image) -> list[float]:
    """Return a 4x4x4 normalized RGB histogram for visible opaque pixels."""
    bins = [0] * 64
    total = 0
    for red, green, blue, alpha in image.convert("RGBA").getdata():
        if alpha <= 128:
            continue
        bins[(red // 64) * 16 + (green // 64) * 4 + blue // 64] += 1
        total += 1
    return [value / total for value in bins] if total else [0.0] * 64


def total_variation(first: list[float], second: list[float]) -> float:
    return sum(abs(a - b) for a, b in zip(first, second)) / 2


def vertical_mass_profile(image: Image.Image) -> list[float]:
    alpha = image.convert("RGBA").getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return [0.0, 0.0, 0.0]
    alpha = alpha.crop(bbox)
    total = sum(alpha.histogram()[1:])
    if not total:
        return [0.0, 0.0, 0.0]
    return [
        sum(alpha.crop((0, round(index * alpha.height / 3), alpha.width, round((index + 1) * alpha.height / 3))).histogram()[1:]) / total
        for index in range(3)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("atlas")
    parser.add_argument("--json-out")
    parser.add_argument("--min-used-pixels", type=int, default=50)
    parser.add_argument("--near-opaque-threshold", type=float, default=0.95)
    parser.add_argument("--chroma-key", default="#00FF00")
    parser.add_argument("--chroma-leak-threshold", type=float, default=36.0)
    parser.add_argument("--max-chroma-leak-pixels", type=int, default=400)
    parser.add_argument("--chroma-fringe-threshold", type=float, default=96.0)
    parser.add_argument("--chroma-fringe-edge-radius", type=int, default=2)
    parser.add_argument("--chroma-fringe-alpha-minimum", type=int, default=16)
    parser.add_argument("--max-chroma-fringe-pixels", type=int, default=0)
    parser.add_argument(
        "--max-baseline-drift",
        type=int,
        default=18,
        help="Maximum visible-bottom difference across the used frames of one row (pixels).",
    )
    parser.add_argument(
        "--max-identity-height-drift",
        type=float,
        default=0.12,
        help="Maximum relative median visible-height drift of standard rows 1-8 versus idle.",
    )
    parser.add_argument(
        "--max-visible-width",
        type=int,
        default=180,
        help="Maximum visible width per cell; catches multiple sprites packed into one frame.",
    )
    parser.add_argument(
        "--min-top-safe-padding",
        type=int,
        default=10,
        help="Minimum transparent pixels above every used sprite; rejects hair/head clipping risk.",
    )
    parser.add_argument(
        "--min-bottom-safe-padding",
        type=int,
        default=8,
        help="Minimum transparent pixels below every used sprite in its 208px cell.",
    )
    parser.add_argument(
        "--min-frame-difference",
        type=float,
        default=0.002,
        help="Minimum normalized difference between adjacent frames; rejects duplicate animation frames.",
    )
    parser.add_argument(
        "--min-expressive-transitions",
        type=int,
        default=2,
        help="Minimum changed head-region transitions in expressive rows.",
    )
    parser.add_argument(
        "--max-step-outlier-ratio",
        type=float,
        default=3.0,
        help="Maximum action-frame step difference relative to the row median; catches abrupt jumps.",
    )
    parser.add_argument(
        "--max-palette-drift",
        type=float,
        default=0.25,
        help="Maximum coarse visible-color histogram drift versus idle frame 0.",
    )
    parser.add_argument(
        "--max-proportion-profile-drift",
        type=float,
        default=0.15,
        help="Maximum top/middle/bottom visible-mass drift versus idle frame 0.",
    )
    parser.add_argument("--allow-opaque", action="store_true")
    parser.add_argument("--allow-near-opaque-used-cells", action="store_true")
    parser.add_argument("--allow-chroma-leak", action="store_true")
    parser.add_argument("--allow-chroma-fringe", action="store_true")
    parser.add_argument(
        "--allow-extended-qa",
        action="store_true",
        help="Allow a 1536x2288 eleven-row offline QA sheet. It is never desktop-installable.",
    )
    # Kept only so older automation gets an explicit compatibility error rather
    # than silently shipping an atlas the Desktop renderer cannot slice.
    parser.add_argument("--require-v2", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    atlas_path = Path(args.atlas).expanduser().resolve()
    chroma_key = parse_hex_color(args.chroma_key)
    errors: list[str] = []
    warnings: list[str] = []
    near_opaque_used_cells: dict[str, list[int]] = defaultdict(list)
    row_bottoms: dict[int, list[tuple[int, int]]] = defaultdict(list)
    row_heights: dict[int, list[int]] = defaultdict(list)
    row_animation_cells: dict[int, list[Image.Image]] = defaultdict(list)
    cells: list[dict[str, object]] = []

    try:
        with Image.open(atlas_path) as opened:
            source_mode = opened.mode
            source_format = opened.format
            image = opened.convert("RGBA")
    except Exception as exc:  # noqa: BLE001
        result = {"ok": False, "errors": [f"could not open atlas: {exc}"], "warnings": []}
        print(json.dumps(result, indent=2))
        raise SystemExit(1) from exc

    expected_heights = {ATLAS_HEIGHT}
    if args.allow_extended_qa:
        expected_heights.add(EXTENDED_ATLAS_HEIGHT)
    if args.require_v2:
        errors.append("--require-v2 is retired: Codex Desktop requires a 1536x1872 8x9 install atlas")
    if image.width != ATLAS_WIDTH or image.height not in expected_heights:
        expected = (
            f"{ATLAS_WIDTH}x{ATLAS_HEIGHT} for a Codex Desktop pet"
            if not args.allow_extended_qa
            else f"{ATLAS_WIDTH}x{ATLAS_HEIGHT} (desktop) or {ATLAS_WIDTH}x{EXTENDED_ATLAS_HEIGHT} (offline QA only)"
        )
        errors.append(f"expected {expected}, got {image.width}x{image.height}")

    if source_format not in {"PNG", "WEBP"}:
        errors.append(f"expected PNG or WebP, got {source_format}")

    if "A" not in source_mode and not args.allow_opaque:
        errors.append("atlas does not have an alpha channel")

    row_count = image.height // CELL_HEIGHT
    is_extended_atlas = image.height == EXTENDED_ATLAS_HEIGHT
    for row_index in range(row_count):
        state, frame_count = ROW_BY_INDEX[row_index]
        for column_index in range(COLUMNS):
            left = column_index * CELL_WIDTH
            top = row_index * CELL_HEIGHT
            cell = image.crop((left, top, left + CELL_WIDTH, top + CELL_HEIGHT))
            nontransparent = alpha_nonzero_count(cell)
            used = column_index < frame_count or (
                is_extended_atlas and (row_index, column_index) == EXTENDED_NEUTRAL_LOOK_FRAME
            )
            cell_info = {
                "state": state,
                "row": row_index,
                "column": column_index,
                "used": used,
                "nontransparent_pixels": nontransparent,
            }
            bbox = alpha_bbox(cell)
            if bbox is not None:
                cell_info["visible_bbox"] = list(bbox)
            chroma_leak_pixels = opaque_chroma_key_count(
                cell,
                chroma_key,
                args.chroma_leak_threshold,
            )
            cell_info["opaque_chroma_key_pixels"] = chroma_leak_pixels
            chroma_fringe_pixels = chroma_fringe_count(
                cell,
                chroma_key=chroma_key,
                distance_threshold=args.chroma_fringe_threshold,
                edge_radius=args.chroma_fringe_edge_radius,
                alpha_minimum=args.chroma_fringe_alpha_minimum,
            )
            cell_info["chroma_fringe_pixels"] = chroma_fringe_pixels
            cells.append(cell_info)
            if column_index < frame_count:
                row_animation_cells[row_index].append(cell)
            if used and nontransparent < args.min_used_pixels:
                errors.append(
                    f"{state} row {row_index} column {column_index} is empty or too sparse ({nontransparent} pixels)"
                )
            if used and bbox is not None:
                # A detached/missing foot or a sliced body often shifts the alpha
                # bottom dramatically. Check the entire action row below instead
                # of accepting a structurally valid but visibly misregistered cell.
                row_bottoms[row_index].append((column_index, bbox[3]))
                row_heights[row_index].append(bbox[3] - bbox[1])
                visible_width = bbox[2] - bbox[0]
                top_padding = bbox[1]
                bottom_padding = CELL_HEIGHT - bbox[3]
                cell_info["top_safe_padding"] = top_padding
                cell_info["bottom_safe_padding"] = bottom_padding
                if top_padding < args.min_top_safe_padding:
                    errors.append(
                        f"{state} row {row_index} column {column_index} has only {top_padding}px "
                        f"above the visible head/hair (minimum {args.min_top_safe_padding}px); "
                        "run uniform safe-box registration to prevent Desktop overlay clipping"
                    )
                if bottom_padding < args.min_bottom_safe_padding:
                    errors.append(
                        f"{state} row {row_index} column {column_index} has only {bottom_padding}px "
                        f"below the shoes (minimum {args.min_bottom_safe_padding}px)"
                    )
                if visible_width > args.max_visible_width:
                    errors.append(
                        f"{state} row {row_index} column {column_index} visible width is "
                        f"{visible_width}px (limit {args.max_visible_width}px); this usually means "
                        "multiple characters or neighboring-frame fragments were packed into one cell"
                    )
            if used and chroma_leak_pixels > args.max_chroma_leak_pixels:
                message = (
                    f"{state} row {row_index} column {column_index} has {chroma_leak_pixels} "
                    f"opaque pixels near chroma key {args.chroma_key}; this usually means "
                    "the sprite background was not removed"
                )
                if args.allow_chroma_leak:
                    warnings.append(message)
                else:
                    errors.append(message)
            if used and chroma_fringe_pixels > args.max_chroma_fringe_pixels:
                message = (
                    f"{state} row {row_index} column {column_index} has {chroma_fringe_pixels} "
                    f"visible edge pixels contaminated by chroma key {args.chroma_key}"
                )
                if args.allow_chroma_fringe:
                    warnings.append(message)
                else:
                    errors.append(message)
            if used and nontransparent > CELL_WIDTH * CELL_HEIGHT * args.near_opaque_threshold:
                near_opaque_used_cells[f"{state} row {row_index}"].append(column_index)
            if not used and nontransparent != 0:
                errors.append(
                    f"{state} row {row_index} unused column {column_index} is not transparent ({nontransparent} pixels)"
                )

    for row_label, columns in near_opaque_used_cells.items():
        message = (
            f"{row_label} has {len(columns)} nearly opaque used cells; "
            "this usually means the sprite has a non-transparent background"
        )
        if args.allow_near_opaque_used_cells:
            warnings.append(message)
        else:
            errors.append(message)

    for row_index, values in row_bottoms.items():
        if len(values) < 2:
            continue
        bottoms = [bottom for _, bottom in values]
        drift = max(bottoms) - min(bottoms)
        if drift > args.max_baseline_drift:
            state, _ = ROW_BY_INDEX[row_index]
            columns = ", ".join(str(column) for column, _ in values)
            errors.append(
                f"{state} row {row_index} visible baseline drift is {drift}px across columns "
                f"{columns} (limit {args.max_baseline_drift}px); repair the complete row to avoid "
                "detached feet or sliced-body registration"
            )

    identity_height_medians = {
        row_index: median(values)
        for row_index, values in row_heights.items()
        if values
    }
    # Rows 0-8 should be the same animation model. Direction rows intentionally
    # change apparent width/contour, so visual review rather than this scalar gate
    # owns them. Height drift still catches a newly redrawn tall/short character.
    idle_height = identity_height_medians.get(0)
    if idle_height:
        for row_index in range(1, 9):
            row_height = identity_height_medians.get(row_index)
            if row_height is None:
                continue
            drift = abs(row_height - idle_height) / idle_height
            if drift > args.max_identity_height_drift:
                state, _ = ROW_BY_INDEX[row_index]
                errors.append(
                    f"{state} row {row_index} median visible height is {row_height}px versus idle "
                    f"{idle_height}px ({drift:.1%} drift; limit {args.max_identity_height_drift:.1%}); "
                    "regenerate this complete row using the approved canonical character image"
                )

    identity_reference = image.crop((0, 0, CELL_WIDTH, CELL_HEIGHT))
    reference_palette = coarse_palette(identity_reference)
    reference_profile = vertical_mass_profile(identity_reference)
    identity_metrics: dict[str, object] = {}
    for row_index in range(row_count):
        state, frame_count = ROW_BY_INDEX[row_index]
        row_metrics = []
        for column_index in range(frame_count):
            cell = image.crop((column_index * CELL_WIDTH, row_index * CELL_HEIGHT, (column_index + 1) * CELL_WIDTH, (row_index + 1) * CELL_HEIGHT))
            palette_drift = total_variation(reference_palette, coarse_palette(cell))
            profile_drift = total_variation(reference_profile, vertical_mass_profile(cell))
            row_metrics.append({
                "column": column_index,
                "palette_drift": round(palette_drift, 6),
                "proportion_profile_drift": round(profile_drift, 6),
            })
            if palette_drift > args.max_palette_drift:
                errors.append(
                    f"{state} row {row_index} column {column_index} palette drift is {palette_drift:.1%} "
                    f"(limit {args.max_palette_drift:.1%}); verify immutable outfit/hair/skin colors"
                )
            if profile_drift > args.max_proportion_profile_drift:
                errors.append(
                    f"{state} row {row_index} column {column_index} vertical body-mass drift is {profile_drift:.1%} "
                    f"(limit {args.max_proportion_profile_drift:.1%}); verify head/torso/leg proportions"
                )
        identity_metrics[str(row_index)] = {"state": state, "cells": row_metrics}

    motion_metrics: dict[str, object] = {}
    expressive_rows = {0, 3, 4, 5, 6, 7, 8}
    for row_index, frames in row_animation_cells.items():
        if len(frames) < 2:
            continue
        state, _ = ROW_BY_INDEX[row_index]
        differences = [
            mean_frame_difference(frames[index], frames[(index + 1) % len(frames)])
            for index in range(len(frames))
        ]
        duplicates = [index for index, value in enumerate(differences) if value < args.min_frame_difference]
        if duplicates:
            errors.append(
                f"{state} row {row_index} has duplicate/near-duplicate transitions after columns "
                f"{', '.join(map(str, duplicates))} (minimum {args.min_frame_difference:.4f}); "
                "use every runtime frame with a distinct meaningful pose/expression"
            )
        row_median = median(differences)
        if row_index <= 8 and row_median > 0:
            outliers = [index for index, value in enumerate(differences) if value > row_median * args.max_step_outlier_ratio]
            if outliers:
                errors.append(
                    f"{state} row {row_index} has abrupt motion transitions after columns "
                    f"{', '.join(map(str, outliers))}; regenerate evenly phased complete-row motion"
                )
        head_differences: list[float] = []
        if row_index in expressive_rows:
            heads = [frame.crop((0, 0, CELL_WIDTH, 120)) for frame in frames]
            head_differences = [
                mean_frame_difference(heads[index], heads[(index + 1) % len(heads)])
                for index in range(len(heads))
            ]
            expressive_transitions = sum(value >= args.min_frame_difference for value in head_differences)
            if expressive_transitions < args.min_expressive_transitions:
                errors.append(
                    f"{state} row {row_index} changes the head/expression region in only "
                    f"{expressive_transitions} transitions (minimum {args.min_expressive_transitions}); "
                    "expression must evolve naturally across multiple frames"
                )
        motion_metrics[str(row_index)] = {
            "state": state,
            "frame_differences": [round(value, 6) for value in differences],
            "head_differences": [round(value, 6) for value in head_differences],
        }

    alpha_count = alpha_nonzero_count(image)
    if alpha_count == ATLAS_WIDTH * ATLAS_HEIGHT:
        message = "atlas is fully opaque; custom pets require a transparent sprite background"
        if args.allow_opaque:
            warnings.append(message)
        else:
            errors.append(message)

    transparent_rgb_residue = transparent_rgb_residue_count(image)
    if transparent_rgb_residue:
        errors.append(
            f"atlas has {transparent_rgb_residue} fully transparent pixels with non-zero RGB residue"
        )

    result = {
        "ok": not errors,
        "file": str(atlas_path),
        "format": source_format,
        "mode": source_mode,
        "columns": COLUMNS,
        "rows": row_count,
        "sprite_version_number": 2 if is_extended_atlas else 1,
        "desktop_installable": not is_extended_atlas,
        "width": image.width,
        "height": image.height,
        "transparent_rgb_residue_pixels": transparent_rgb_residue,
        "identity_height_medians": identity_height_medians,
        "motion_metrics": motion_metrics,
        "identity_metrics": identity_metrics,
        "errors": errors,
        "warnings": warnings,
        "cells": cells,
    }

    if args.json_out:
        Path(args.json_out).expanduser().resolve().write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )

    print(json.dumps({k: v for k, v in result.items() if k != "cells"}, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
