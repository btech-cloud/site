#!/usr/bin/env python3
"""Extrai lockups BTECH do PDF oficial (Canva) — fonte única da verdade."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOURCE = ASSETS / "source" / "logo-btech-canva.pdf"
FALLBACK_PDF = Path(
    "/home/ubuntu/.cursor/projects/workspace/uploads/Design_sem_nome_1_6595.pdf"
)


def render_pdf(pdf: Path, dpi: int = 300) -> Image.Image:
    import subprocess
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    out = tmp / "page"
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(out)],
        check=True,
        capture_output=True,
    )
    page = Image.open(f"{out}-1.png").convert("RGBA")
    return page


def content_bbox(im: Image.Image, threshold: int = 250, margin: int = 40) -> tuple[int, int, int, int]:
    arr = np.array(im.convert("RGB"))
    mask = (arr < threshold).any(axis=2)
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return 0, 0, im.width, im.height
    return (
        max(0, int(xs.min()) - margin),
        max(0, int(ys.min()) - margin),
        min(im.width, int(xs.max()) + margin),
        min(im.height, int(ys.max()) + margin),
    )


def extract_from_page(page: Image.Image) -> tuple[Image.Image, Image.Image, Image.Image]:
    stacked = page.crop(content_bbox(page))
    w, h = stacked.size
    rgb = np.array(stacked.convert("RGB"))
    y0 = int(h * 0.78)
    region = rgb[y0:]
    col_has = (region < 100).any(axis=0)
    row_has = (region < 100).any(axis=1)
    cols = np.where(col_has)[0]
    rows = np.where(row_has)[0]
    pad = 12
    word = stacked.crop(
        (
            int(cols[0]) - pad,
            y0 + int(rows[0]) - pad,
            int(cols[-1]) + pad,
            y0 + int(rows[-1]) + pad,
        )
    )
    sym = stacked.crop((0, 0, w, y0 - 20))
    sym = sym.crop(content_bbox(sym, margin=8))
    return stacked, sym, word


def compose_horizontal(sym: Image.Image, word: Image.Image, word_h: int = 56) -> Image.Image:
    word_s = word.resize(
        (int(word.width * word_h / word.height), word_h),
        Image.Resampling.LANCZOS,
    )
    sym_h = int(word_h * 1.12)
    sym_s = sym.resize(
        (int(sym.width * sym_h / sym.height), sym_h),
        Image.Resampling.LANCZOS,
    )
    gap = 20
    w = sym_s.width + gap + word_s.width
    h = max(sym_s.height, word_s.height)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(sym_s, (0, (h - sym_s.height) // 2), sym_s)
    out.paste(word_s, (sym_s.width + gap, (h - word_s.height) // 2), word_s)
    return out


def save_all(pdf: Path) -> None:
    page = render_pdf(pdf)
    stacked, sym, word = extract_from_page(page)
    horiz = compose_horizontal(sym, word)

    stacked.save(ASSETS / "logo-btech-stacked-oficial.png")
    stacked.resize((stacked.width * 2, stacked.height * 2), Image.Resampling.LANCZOS).save(
        ASSETS / "logo-btech-stacked-oficial@2x.png"
    )
    horiz.save(ASSETS / "logo-btech-horizontal-oficial.png")
    horiz.resize((horiz.width * 2, horiz.height * 2), Image.Resampling.LANCZOS).save(
        ASSETS / "logo-btech-horizontal-oficial@2x.png"
    )
    sym.save(ASSETS / "logo-symbol-oficial.png")

    sym_icon = sym.copy()
    sym_icon.thumbnail((480, 480), Image.Resampling.LANCZOS)
    icon = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    icon.paste(sym_icon, ((512 - sym_icon.width) // 2, (512 - sym_icon.height) // 2), sym_icon)
    icon.save(ASSETS / "logo-icon-oficial.png")

    print("PDF:", pdf)
    print("stacked", stacked.size, "horizontal", horiz.size, "symbol", sym.size)


if __name__ == "__main__":
    pdf = SOURCE if SOURCE.exists() else FALLBACK_PDF
    if not pdf.exists():
        sys.exit(f"PDF não encontrado: {pdf}")
    save_all(pdf)
