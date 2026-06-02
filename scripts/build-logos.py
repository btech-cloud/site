#!/usr/bin/env python3
"""
BTECH a partir do manual ABTECH (p.17 cartão de visitas).

Mantém: símbolo (SVG do manual), cores, TECH raster do manual, proporções.
Muda só: ABTECH → BTECH (remove o A; B negrito no lugar).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"
FONT_BOLD = FONTS / "GOTHICB.ttf"
SYMBOL_SVG = ASSETS / "logo-icon.svg"
MANUAL_PDF = ASSETS / "source" / "manual-abtech.pdf"
MANUAL_FALLBACK = Path(
    "/home/ubuntu/.cursor/projects/workspace/uploads/ManualABTECH-compactado_3ef1.pdf"
)
A_WIDTH_RATIO = 0.28
SYMBOL_TEXT_GAP = 0.015


def render_manual_page(pdf: Path, page: int = 17, dpi: int = 300) -> Image.Image:
    tmp = Path(tempfile.mkdtemp())
    out = tmp / "p"
    subprocess.run(
        ["pdftoppm", "-f", str(page), "-l", str(page), "-png", "-r", str(dpi), str(pdf), str(out)],
        check=True,
        capture_output=True,
    )
    return Image.open(f"{out}-{page}.png").convert("RGB")


def crop_business_card(page: Image.Image) -> Image.Image:
    w, h = page.size
    return page.crop((int(w * 0.06), int(h * 0.10), int(w * 0.44), int(h * 0.48)))


def find_text_band(card: Image.Image) -> tuple[int, int, int]:
    arr = np.array(card)
    text_y = int(card.height * 0.72)
    for y in range(int(card.height * 0.62), card.height):
        if (arr[y] < 200).any(axis=1).sum() > card.width * 0.08:
            text_y = y - 8
            break
    m = (arr[text_y:] < 200).any(axis=2)
    ys, xs = np.where(m)
    return text_y, int(xs.min()), int(xs.max() + 1)


def to_transparent(im: Image.Image) -> Image.Image:
    arr = np.array(im.convert("RGBA"))
    rgb = arr[:, :, :3]
    arr[(rgb > 220).all(axis=2), 3] = 0
    return Image.fromarray(arr)


def wordmark_btech_from_manual(card: Image.Image) -> Image.Image:
    text_y, x0, x1 = find_text_band(card)
    raw = card.crop((x0, text_y, x1, card.height))
    arr = np.array(raw)
    m = (arr < 200).any(axis=2)
    ys, xs = np.where(m)
    raw = raw.crop((int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)))
    aw = max(1, int(raw.width * A_WIDTH_RATIO))
    tech = to_transparent(raw.crop((aw, 0, raw.width, raw.height)))
    a_h = raw.crop((0, 0, aw, raw.height)).height

    fbold = ImageFont.truetype(FONT_BOLD, 80)
    for size in range(8, 320):
        f = ImageFont.truetype(FONT_BOLD, size)
        d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        bb = d.textbbox((0, 0), "B", font=f)
        if bb[3] - bb[1] >= a_h - 3:
            fbold = f
            break

    b_canvas = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    d = ImageDraw.Draw(b_canvas)
    bb = d.textbbox((0, 0), "B", font=fbold)
    d.text((-bb[0], -bb[1]), "B", font=fbold, fill=(0, 0, 0, 255))
    b_img = b_canvas.crop(b_canvas.getbbox())

    out = Image.new("RGBA", (b_img.width + tech.width, max(b_img.height, tech.height)), (0, 0, 0, 0))
    out.paste(b_img, (0, (out.height - b_img.height) // 2), b_img)
    out.paste(tech, (b_img.width, (out.height - tech.height) // 2), tech)
    return out


def render_symbol(width: int) -> Image.Image:
    out = Path(tempfile.gettempdir()) / "btech-symbol.png"
    subprocess.run(["rsvg-convert", "-w", str(width), str(SYMBOL_SVG), "-o", str(out)], check=True)
    return Image.open(out).convert("RGBA")


def compose_stacked(word: Image.Image, target_w: int = 220) -> Image.Image:
    sym = render_symbol(int(target_w * 0.92))
    gap = max(4, int(sym.height * SYMBOL_TEXT_GAP))
    scale = target_w / max(word.width, sym.width)
    word_s = word.resize((int(word.width * scale), int(word.height * scale)), Image.Resampling.LANCZOS)
    sym_s = sym.resize((int(sym.width * scale), int(sym.height * scale)), Image.Resampling.LANCZOS)
    w = max(sym_s.width, word_s.width)
    h = sym_s.height + gap + word_s.height
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(sym_s, ((w - sym_s.width) // 2, 0), sym_s)
    canvas.paste(word_s, ((w - word_s.width) // 2, sym_s.height + gap), word_s)
    return canvas


def compose_horizontal(word: Image.Image, height: int = 62) -> Image.Image:
    sym = render_symbol(int(height * 1.05))
    word_s = word.resize((int(word.width * height / word.height), height), Image.Resampling.LANCZOS)
    gap = int(height * 0.35)
    w = sym.width + gap + word_s.width
    h = max(sym.height, word_s.height)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(sym, (0, (h - sym.height) // 2), sym)
    canvas.paste(word_s, (sym.width + gap, (h - word_s.height) // 2), word_s)
    return canvas


def save_all(pdf: Path) -> None:
    card = crop_business_card(render_manual_page(pdf))
    word = wordmark_btech_from_manual(card)
    stacked = compose_stacked(word)
    horiz = compose_horizontal(word)

    stacked.save(ASSETS / "logo-btech-stacked-oficial.png")
    stacked.resize((stacked.width * 2, stacked.height * 2), Image.Resampling.LANCZOS).save(
        ASSETS / "logo-btech-stacked-oficial@2x.png"
    )
    horiz.save(ASSETS / "logo-btech-horizontal-oficial.png")
    horiz.resize((horiz.width * 2, horiz.height * 2), Image.Resampling.LANCZOS).save(
        ASSETS / "logo-btech-horizontal-oficial@2x.png"
    )
    render_symbol(400).save(ASSETS / "logo-symbol-oficial.png")
    sym = render_symbol(480)
    sym.thumbnail((480, 480), Image.Resampling.LANCZOS)
    icon = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    icon.paste(sym, ((512 - sym.width) // 2, (512 - sym.height) // 2), sym)
    icon.save(ASSETS / "logo-icon-oficial.png")
    print("OK manual:", pdf)
    print("  stacked", stacked.size, "horizontal", horiz.size)


if __name__ == "__main__":
    pdf = MANUAL_PDF if MANUAL_PDF.exists() else MANUAL_FALLBACK
    if not pdf.exists():
        sys.exit(f"Manual não encontrado: {pdf}")
    (ASSETS / "source").mkdir(parents=True, exist_ok=True)
    if not MANUAL_PDF.exists():
        import shutil

        shutil.copy(pdf, MANUAL_PDF)
    save_all(pdf)
