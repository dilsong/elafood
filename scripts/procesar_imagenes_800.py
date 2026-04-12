# -*- coding: utf-8 -*-
"""
Normaliza fotos bajo Imagenes/: 800×800 px, 1:1, recorte centrado sin estirar.

- Recorte cuadrado por el lado menor (exceso centrado descartado).
- Redimensionado uniforme a 800×800 (LANCZOS).
- RGBA/P: se compone sobre fondo blanco (mejor para comida y JPEG).
- JPEG: calidad 95, subsampling=0. PNG/WEBP: compresión sin pérdida agresiva.

Uso (desde la raíz del repo):
    python scripts/procesar_imagenes_800.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGENES_DIR = BASE_DIR / "Imagenes"
TARGET = 800
# Blanco: mejor contraste con platos y con texto oscuro en la app.
BG = (255, 255, 255)
ALLOWED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def _as_rgb(img: Image.Image) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    if img.mode in ("RGBA", "LA"):
        base = Image.new("RGB", img.size, BG)
        base.paste(img, mask=img.split()[-1])
        return base
    if img.mode == "P":
        img = img.convert("RGBA")
        base = Image.new("RGB", img.size, BG)
        base.paste(img, mask=img.split()[-1])
        return base
    if img.mode != "RGB":
        return img.convert("RGB")
    return img


def square_center_resize(img: Image.Image) -> Image.Image:
    img = _as_rgb(img)
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    cropped = img.crop((left, top, left + side, top + side))
    return cropped.resize((TARGET, TARGET), Image.Resampling.LANCZOS)


def save_inplace(path: Path, rgb: Image.Image) -> None:
    suf = path.suffix.lower()
    if suf in (".jpg", ".jpeg"):
        rgb.save(path, "JPEG", quality=95, optimize=True, subsampling=0)
    elif suf == ".png":
        rgb.save(path, "PNG", optimize=True)
    elif suf == ".webp":
        rgb.save(path, "WEBP", quality=92, method=6)
    elif suf == ".bmp":
        rgb.save(path, "BMP")
    else:
        rgb.save(path)


def iter_image_files(root: Path):
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() not in ALLOWED_SUFFIXES:
            continue
        yield p


def main() -> int:
    if not IMAGENES_DIR.is_dir():
        print(f"No existe la carpeta: {IMAGENES_DIR}", file=sys.stderr)
        return 1

    n = 0
    for path in iter_image_files(IMAGENES_DIR):
        try:
            with Image.open(path) as im:
                im.load()
                out = square_center_resize(im)
            save_inplace(path, out)
        except OSError as e:
            print(f"[omitir] {path}: {e}", file=sys.stderr)
            continue
        rel = path.relative_to(BASE_DIR)
        print(f"OK {rel} -> {TARGET}x{TARGET}")
        n += 1

    print(f"Total procesadas: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
