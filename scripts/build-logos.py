#!/usr/bin/env python3
"""Gera lockups BTECH com símbolo oficial + Century Gothic (B negrito, TECH regular)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"
SYMBOL_PATH = ASSETS / "logo-symbol-oficial.png"
FONT_REG = FONTS / "GOTHIC.ttf"
FONT_BOLD = FONTS / "GOTHICB.ttf"


def fonts(size: int) -> tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont]:
    return (
        ImageFont.truetype(FONT_BOLD, size),
        ImageFont.truetype(FONT_REG, size),
    )


def measure_btech(
    draw: ImageDraw.ImageDraw, size: int, bold_all: bool = False
) -> tuple[int, int]:
    b_font, r_font = fonts(size)
    if bold_all:
        w = int(draw.textlength("BTECH", font=b_font))
    else:
        w = int(draw.textlength("B", font=b_font) + draw.textlength("TECH", font=r_font))
    return w, size + int(size * 0.15)


def draw_btech(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    size: int,
    fill: tuple[int, int, int, int] = (0, 0, 0, 255),
    bold_all: bool = False,
    anchor: str = "lt",
) -> None:
    b_font, r_font = fonts(size)
    if bold_all:
        draw.text((x, y), "BTECH", font=b_font, fill=fill, anchor=anchor)
        return
    if anchor != "lt":
        w, _ = measure_btech(draw, size, False)
        if anchor == "mm":
            x -= w // 2
        elif anchor == "ma":
            x -= w // 2
    draw.text((x, y), "B", font=b_font, fill=fill)
    draw.text((x + draw.textlength("B", font=b_font), y), "TECH", font=r_font, fill=fill)


def _measure_consultoria(
    draw: ImageDraw.ImageDraw, size: int, tracking: float = 0.38
) -> int:
    font = ImageFont.truetype(FONT_REG, size)
    gap = size * tracking
    cx = 0
    for ch in "CONSULTORIA":
        cx += draw.textlength(ch, font=font) + gap
    return int(cx - gap)


def draw_consultoria(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    size: int,
    fill: tuple[int, int, int, int],
    tracking: float = 0.38,
) -> int:
    """Desenha CONSULTORIA com tracking; retorna largura total."""
    font = ImageFont.truetype(FONT_REG, size)
    word = "CONSULTORIA"
    gap = size * tracking
    cx = x
    for ch in word:
        draw.text((cx, y), ch, font=font, fill=fill)
        cx += draw.textlength(ch, font=font) + gap
    return int(cx - x - gap)


def load_symbol(target_width: int) -> Image.Image:
    sym = Image.open(SYMBOL_PATH).convert("RGBA")
    scale = target_width / sym.width
    h = int(sym.height * scale)
    return sym.resize((target_width, h), Image.Resampling.LANCZOS)


def stacked(
    symbol_w: int = 200,
    text_size: int = 52,
    gap: int | None = None,
    dark: bool = False,
) -> Image.Image:
    sym = load_symbol(symbol_w)
    gap = gap if gap is not None else int(text_size * 0.28)
    dummy = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(dummy)
    tw, th = measure_btech(d, text_size, bold_all=dark)
    consult_h = 0
    if dark:
        consult_h = int(text_size * 0.42) + int(text_size * 0.2)

    w = max(sym.width, tw) + 16
    h = sym.height + gap + th + consult_h + 16
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    sx = (w - sym.width) // 2
    canvas.paste(sym, (sx, 8), sym)
    ty = 8 + sym.height + gap
    fill = (255, 255, 255, 255) if dark else (0, 0, 0, 255)
    draw_btech(draw, w // 2, ty, text_size, fill=fill, bold_all=dark, anchor="ma")
    if dark:
        sub_size = int(text_size * 0.38)
        sub_y = ty + th + int(text_size * 0.12)
        sub_w = _measure_consultoria(draw, sub_size, tracking=0.32)
        draw_consultoria(draw, (w - sub_w) // 2, sub_y, sub_size, fill, tracking=0.32)
    return canvas


def horizontal(text_size: int = 44, symbol_h: int | None = None) -> Image.Image:
    sym = Image.open(SYMBOL_PATH).convert("RGBA")
    dummy = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(dummy)
    tw, th = measure_btech(d, text_size)
    symbol_h = symbol_h or th
    scale = symbol_h / sym.height
    sym_s = sym.resize((int(sym.width * scale), symbol_h), Image.Resampling.LANCZOS)
    gap = int(text_size * 0.45)
    w = sym_s.width + gap + tw
    h = max(sym_s.height, th)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    canvas.paste(sym_s, (0, (h - sym_s.height) // 2), sym_s)
    draw_btech(draw, sym_s.width + gap, (h - th) // 2, text_size)
    return canvas


def icon(size: int = 512) -> Image.Image:
    sym = load_symbol(size - 32)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(sym, ((size - sym.width) // 2, (size - sym.height) // 2), sym)
    return canvas


def save_all() -> None:
    outputs = {
        "logo-btech-stacked-oficial.png": stacked(200, 52),
        "logo-btech-stacked-oficial@2x.png": stacked(400, 104),
        "logo-btech-stacked-dark.png": stacked(200, 48, dark=True),
        "logo-btech-horizontal-oficial.png": horizontal(44),
        "logo-btech-horizontal-oficial@2x.png": horizontal(88),
        "logo-icon-oficial.png": icon(512),
    }
    for name, img in outputs.items():
        path = ASSETS / name
        img.save(path, optimize=True)
        print("wrote", path, img.size)


if __name__ == "__main__":
    save_all()
