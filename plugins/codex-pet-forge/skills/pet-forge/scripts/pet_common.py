from __future__ import annotations

import re
from pathlib import Path
from PIL import Image

# Codex Desktop slices its pet background with a fixed 8 x 9 CSS grid.
# Keep this as the default product contract.  Eleven-row sheets are useful
# as offline turnaround QA artifacts, but must never be installed as the
# desktop pet atlas: the renderer will vertically resample them and mix rows.
COLS, ROWS = 8, 9
CELL_W, CELL_H = 192, 208
ATLAS_W, ATLAS_H = COLS * CELL_W, ROWS * CELL_H
USED_COUNTS = (7, 8, 8, 4, 5, 8, 6, 6, 6)
TARGET_VISIBLE_HEIGHT = 176
BOTTOM_SAFE_PADDING = 14
SIDE_SAFE_PADDING = 16


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "custom-pet"


def parse_color(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise ValueError("color must be #RRGGBB")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def clear_hidden_rgb(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    data = [(0, 0, 0, 0) if a == 0 else (r, g, b, a) for r, g, b, a in rgba.getdata()]
    rgba.putdata(data)
    return rgba


def save_lossless(image: Image.Image, png_path: Path | None, webp_path: Path | None) -> None:
    image = clear_hidden_rgb(image)
    if png_path:
        png_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(png_path, "PNG")
    if webp_path:
        webp_path.parent.mkdir(parents=True, exist_ok=True)
        # `exact=True` preserves the deliberately cleared RGB=(0,0,0) under
        # alpha=0; without it libwebp may synthesize hidden RGB during encoding.
        image.save(webp_path, "WEBP", lossless=True, method=6, exact=True)


def clear_unused_cells(image: Image.Image) -> None:
    for row, used in enumerate(USED_COUNTS):
        y0 = row * CELL_H
        for col in range(used, COLS):
            x0 = col * CELL_W
            image.paste((0, 0, 0, 0), (x0, y0, x0 + CELL_W, y0 + CELL_H))


def register_cells_to_safe_box(image: Image.Image) -> Image.Image:
    """Uniformly fit every used sprite into the Desktop overlay safe box.

    The Desktop renderer clips a fixed 192x208 background cell.  Generated
    figures that nearly touch the cell top can lose hair pixels in the floating
    overlay even though the atlas itself is valid.  Normalize every complete
    figure to one visible height and one shoe baseline without changing aspect
    ratio; this also removes cross-action size popping.
    """
    registered = Image.new("RGBA", image.size, (0, 0, 0, 0))
    max_width = CELL_W - 2 * SIDE_SAFE_PADDING
    baseline = CELL_H - BOTTOM_SAFE_PADDING
    for row, used in enumerate(USED_COUNTS):
        for col in range(used):
            box = (col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)
            cell = image.crop(box).convert("RGBA")
            bbox = cell.getchannel("A").getbbox()
            if bbox is None:
                continue
            sprite = cell.crop(bbox)
            scale = min(TARGET_VISIBLE_HEIGHT / sprite.height, max_width / sprite.width)
            width = max(1, round(sprite.width * scale))
            height = max(1, round(sprite.height * scale))
            sprite = sprite.resize((width, height), Image.Resampling.LANCZOS)
            x = col * CELL_W + (CELL_W - width) // 2
            y = row * CELL_H + baseline - height
            registered.alpha_composite(sprite, (x, y))
    clear_unused_cells(registered)
    return clear_hidden_rgb(registered)


def chroma_to_alpha(image: Image.Image, key: tuple[int, int, int], transparent: int = 18, opaque: int = 105) -> Image.Image:
    rgba = image.convert("RGBA")
    out = []
    for r, g, b, source_a in rgba.getdata():
        distance = ((r - key[0]) ** 2 + (g - key[1]) ** 2 + (b - key[2]) ** 2) ** 0.5
        if distance <= transparent:
            alpha = 0
        elif distance >= opaque:
            alpha = source_a
        else:
            alpha = round(source_a * (distance - transparent) / (opaque - transparent))
        out.append((0, 0, 0, 0) if alpha == 0 else (r, g, b, alpha))
    rgba.putdata(out)
    return rgba
