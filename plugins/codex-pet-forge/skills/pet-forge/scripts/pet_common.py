from __future__ import annotations

import re
from pathlib import Path
from PIL import Image

COLS, ROWS = 8, 11
CELL_W, CELL_H = 192, 208
ATLAS_W, ATLAS_H = COLS * CELL_W, ROWS * CELL_H
USED_COUNTS = (7, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)


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
        image.save(webp_path, "WEBP", lossless=True, method=6)


def clear_unused_cells(image: Image.Image) -> None:
    for row, used in enumerate(USED_COUNTS):
        y0 = row * CELL_H
        for col in range(used, COLS):
            x0 = col * CELL_W
            image.paste((0, 0, 0, 0), (x0, y0, x0 + CELL_W, y0 + CELL_H))


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
