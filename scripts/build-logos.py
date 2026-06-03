#!/usr/bin/env python3
"""
Gera lockups BTECH oficiais: símbolo (hexágono) + wordmark B + TECH.

Símbolo: assets/btech-mark-exact.png (referência visual aprovada)
Tipografia: Century Gothic Bold (B) + Regular (TECH) — assets/fonts/GOTHIC*.ttf
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"
SYMBOL_SRC = ASSETS / "btech-mark-exact.png"
SYMBOL_SVG = ASSETS / "logo-symbol-official.svg"
FONT_B = FONTS / "GOTHICB.ttf"
FONT_TECH = FONTS / "GOTHIC.ttf"

# Proporções do manual / arte enviada
STACKED_SYMBOL_TO_TEXT_WIDTH = 0.62
STACKED_SYMBOL_TEXT_GAP_RATIO = 0.22
HORIZONTAL_SYMBOL_TEXT_GAP_RATIO = 0.32


def load_symbol() -> Image.Image:
    if SYMBOL_SRC.exists():
        return Image.open(SYMBOL_SRC).convert("RGBA")
    out = ASSETS / "_symbol-tmp.png"
    subprocess.run(
        ["rsvg-convert", "-w", "687", str(SYMBOL_SVG), "-o", str(out)],
        check=True,
    )
    return Image.open(out).convert("RGBA")


def render_wordmark(height: int, fill: tuple[int, int, int, int]) -> Image.Image:
    font_b = ImageFont.truetype(str(FONT_B), height)
    font_t = ImageFont.truetype(str(FONT_TECH), height)
    b = "B"
    tech = "TECH"
    draw_probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox_b = draw_probe.textbbox((0, 0), b, font=font_b)
    bbox_t = draw_probe.textbbox((0, 0), tech, font=font_t)
    w = (bbox_b[2] - bbox_b[0]) + (bbox_t[2] - bbox_t[0])
    h = max(bbox_b[3] - bbox_b[1], bbox_t[3] - bbox_t[1])
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    x = 0
    draw.text((x - bbox_b[0], -bbox_b[1]), b, font=font_b, fill=fill)
    x += bbox_b[2] - bbox_b[0]
    draw.text((x - bbox_t[0], -bbox_t[1]), tech, font=font_t, fill=fill)
    return canvas


def compose_stacked(symbol: Image.Image, word: Image.Image) -> Image.Image:
    sym_w = max(1, int(word.width * STACKED_SYMBOL_TO_TEXT_WIDTH))
    sym_h = int(sym_w * (symbol.height / symbol.width))
    sym = symbol.resize((sym_w, sym_h), Image.Resampling.LANCZOS)
    gap = max(6, int(sym.height * STACKED_SYMBOL_TEXT_GAP_RATIO))
    w = max(sym.width, word.width)
    h = sym.height + gap + word.height
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(sym, ((w - sym.width) // 2, 0), sym)
    canvas.paste(word, ((w - word.width) // 2, sym.height + gap), word)
    return canvas


def compose_horizontal(symbol: Image.Image, word: Image.Image, text_h: int = 42) -> Image.Image:
    word_s = word.resize(
        (int(word.width * text_h / word.height), text_h),
        Image.Resampling.LANCZOS,
    )
    sym_h = int(text_h * 1.12)
    sym_w = int(sym_h * (symbol.width / symbol.height))
    sym = symbol.resize((sym_w, sym_h), Image.Resampling.LANCZOS)
    gap = max(8, int(text_h * HORIZONTAL_SYMBOL_TEXT_GAP_RATIO))
    w = sym.width + gap + word_s.width
    h = max(sym.height, word_s.height)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(sym, (0, (h - sym.height) // 2), sym)
    canvas.paste(word_s, (sym.width + gap, (h - word_s.height) // 2), word_s)
    return canvas


def save_png(im: Image.Image, path: Path, scale2x: bool = True) -> None:
    im.save(path)
    if scale2x:
        im.resize((im.width * 2, im.height * 2), Image.Resampling.LANCZOS).save(
            path.with_name(path.stem + "@2x" + path.suffix)
        )


def write_svg_lockups() -> None:
    stacked_svg = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 220 200" role="img" aria-label="BTECH">
  <image xlink:href="btech-mark-exact.png" x="34" y="0" width="152" height="132" preserveAspectRatio="xMidYMid meet"/>
  <text x="110" y="178" text-anchor="middle" font-family="Century Gothic, AppleGothic, sans-serif" font-size="42" fill="#0a0a0a" letter-spacing="0.02em">
    <tspan font-weight="700">B</tspan><tspan font-weight="400">TECH</tspan>
  </text>
</svg>"""
    horiz_svg = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 320 72" role="img" aria-label="BTECH">
  <image xlink:href="btech-mark-exact.png" x="0" y="4" width="62" height="64" preserveAspectRatio="xMidYMid meet"/>
  <text x="78" y="50" font-family="Century Gothic, AppleGothic, sans-serif" font-size="40" fill="#0a0a0a" letter-spacing="0.02em">
    <tspan font-weight="700">B</tspan><tspan font-weight="400">TECH</tspan>
  </text>
</svg>"""
    (ASSETS / "logo-btech-stacked.svg").write_text(stacked_svg, encoding="utf-8")
    (ASSETS / "logo-btech-horizontal.svg").write_text(horiz_svg, encoding="utf-8")


def main() -> None:
    if not FONT_B.exists() or not FONT_TECH.exists():
        sys.exit("Fontes GOTHIC.ttf / GOTHICB.ttf não encontradas em assets/fonts/")

    symbol = load_symbol()
    word_dark = render_wordmark(44, (10, 10, 10, 255))
    word_light = render_wordmark(44, (255, 255, 255, 255))

    stacked = compose_stacked(symbol, word_dark)
    horiz = compose_horizontal(symbol, word_dark)
    stacked_light = compose_stacked(symbol, word_light)
    horiz_light = compose_horizontal(symbol, word_light)

    save_png(stacked, ASSETS / "logo-btech-stacked-oficial.png")
    save_png(horiz, ASSETS / "logo-btech-horizontal-oficial.png")
    save_png(stacked_light, ASSETS / "logo-btech-stacked-oficial-light.png")
    save_png(horiz_light, ASSETS / "logo-btech-horizontal-oficial-light.png")

    sym_400 = symbol.resize((400, int(400 * symbol.height / symbol.width)), Image.Resampling.LANCZOS)
    sym_400.save(ASSETS / "logo-symbol-oficial.png")

    icon = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    sym_icon = symbol.resize((320, int(320 * symbol.height / symbol.width)), Image.Resampling.LANCZOS)
    icon.paste(sym_icon, ((512 - sym_icon.width) // 2, (512 - sym_icon.height) // 2), sym_icon)
    icon.save(ASSETS / "logo-icon-oficial.png")

    subprocess.run(
        ["rsvg-convert", "-w", "100", str(SYMBOL_SVG), "-o", str(ASSETS / "logo-icon.svg")],
        check=True,
    )

    write_svg_lockups()
    print("OK", "stacked", stacked.size, "horizontal", horiz.size)


if __name__ == "__main__":
    main()
