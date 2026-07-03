from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
import re

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
IMAGES.mkdir(exist_ok=True)
VERSION = "20260703-visual3"

INK = (31, 38, 35)
MUTED = (92, 101, 96)
GREEN = (55, 88, 67)
WARM = (166, 137, 101)
PAPER = (247, 245, 239)
RED = (145, 73, 60)


def font(size: int, bold: bool = False, italic: bool = False):
    candidates = []
    if bold:
        candidates += ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    if italic:
        candidates += ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"]
    candidates += ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def paper(width: int, height: int, seed: int) -> Image.Image:
    rng = random.Random(seed)
    img = Image.new("RGB", (width, height), PAPER)
    px = img.load()
    for y in range(height):
        fade = int(6 * y / max(height - 1, 1))
        for x in range(width):
            n = rng.randint(-4, 4)
            px[x, y] = (
                max(0, min(255, PAPER[0] + n - fade)),
                max(0, min(255, PAPER[1] + n - fade)),
                max(0, min(255, PAPER[2] + n - fade)),
            )
    return img.filter(ImageFilter.GaussianBlur(0.35))


def line(draw: ImageDraw.ImageDraw, points, fill=INK, width=2):
    draw.line(points, fill=fill, width=width, joint="curve")


def arrow(draw: ImageDraw.ImageDraw, start, end, fill=INK, width=3):
    line(draw, [start, end], fill, width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 16
    for delta in (2.6, -2.6):
        p = (
            end[0] + length * math.cos(angle + delta),
            end[1] + length * math.sin(angle + delta),
        )
        line(draw, [end, p], fill, width)


def title_block(draw: ImageDraw.ImageDraw, title: str, subtitle: str, width: int):
    draw.rounded_rectangle((34, 28, min(width - 34, 570), 105), radius=15, fill=(252, 251, 247), outline=(70, 76, 72), width=2)
    draw.text((58, 43), title.upper(), font=font(27, bold=True), fill=INK)
    draw.text((58, 78), subtitle.upper(), font=font(12), fill=MUTED)


def note(draw: ImageDraw.ImageDraw, xy, text: str, anchor=(0, 0), color=INK):
    x, y = xy
    box = draw.textbbox((x, y), text, font=font(20, italic=True))
    pad = 10
    draw.rounded_rectangle((box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad), radius=10, fill=(250, 249, 244, 235))
    draw.text((x, y), text, font=font(20, italic=True), fill=color)
    if anchor != (0, 0):
        arrow(draw, (x + (box[2] - box[0]) // 2, y - 4), anchor, color, 2)


def dimension(draw: ImageDraw.ImageDraw, x1, x2, y, text: str):
    line(draw, [(x1, y), (x2, y)], INK, 2)
    line(draw, [(x1, y - 13), (x1, y + 13)], INK, 2)
    line(draw, [(x2, y - 13), (x2, y + 13)], INK, 2)
    tw = draw.textbbox((0, 0), text, font=font(18, italic=True))[2]
    draw.text(((x1 + x2 - tw) / 2, y - 30), text, font=font(18, italic=True), fill=INK)


def sketch_overlay(img: Image.Image, seed: int):
    rng = random.Random(seed)
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    for _ in range(28):
        y = rng.randint(int(h * 0.18), int(h * 0.88))
        x1 = rng.randint(25, int(w * 0.3))
        x2 = rng.randint(int(w * 0.7), w - 25)
        draw.line((x1, y, x2, y + rng.randint(-5, 5)), fill=(50, 58, 54, 35), width=1)
    for _ in range(20):
        x = rng.randint(30, w - 30)
        draw.line((x, int(h * 0.18), x + rng.randint(-15, 15), int(h * 0.9)), fill=(50, 58, 54, 24), width=1)


def room_shell(draw: ImageDraw.ImageDraw, w: int, h: int, tint=(224, 222, 215)):
    left, top, right, bottom = int(w * 0.13), int(h * 0.20), int(w * 0.88), int(h * 0.82)
    back_bottom = int(h * 0.66)
    draw.polygon([(left, top), (right, top), (right, back_bottom), (left, back_bottom)], fill=(249, 248, 244), outline=INK)
    draw.polygon([(left, top), (int(w * 0.06), bottom), (left, back_bottom)], fill=(214, 213, 208), outline=INK)
    draw.polygon([(right, top), (int(w * 0.95), bottom), (right, back_bottom)], fill=(203, 202, 196), outline=INK)
    draw.polygon([(left, back_bottom), (right, back_bottom), (int(w * 0.95), bottom), (int(w * 0.06), bottom)], fill=tint, outline=INK)
    for i in range(1, 7):
        yy = back_bottom + (bottom - back_bottom) * i / 7
        line(draw, [(int(w * 0.06 + (left - w * 0.06) * i / 7), yy), (int(w * 0.95 - (w * 0.95 - right) * i / 7), yy)], (117, 121, 117), 1)
    return left, top, right, back_bottom, bottom


def scene_kitchen(w, h, seed, title, note_a, note_b, variant=0):
    img = paper(w, h, seed)
    draw = ImageDraw.Draw(img, "RGBA")
    title_block(draw, title, "Sistema 90G · analisi preventiva", w)
    left, top, right, back_bottom, bottom = room_shell(draw, w, h, (228, 225, 218))
    unit_y = int(h * 0.31)
    unit_h = int(h * 0.22)
    cols = 5
    x0, x1 = int(w * 0.25), int(w * 0.80)
    cw = (x1 - x0) / cols
    for i in range(cols):
        fill = (238, 237, 233) if i != cols - 1 else (129, 108, 82)
        draw.rectangle((x0 + i * cw, unit_y, x0 + (i + 1) * cw - 3, unit_y + unit_h), fill=fill, outline=INK, width=2)
    draw.rectangle((x0, unit_y + unit_h + 8, x1, unit_y + unit_h + 37), fill=(189, 184, 174), outline=INK, width=2)
    island = [
        (int(w * 0.37), int(h * 0.59)),
        (int(w * 0.69), int(h * 0.59)),
        (int(w * 0.74), int(h * 0.78)),
        (int(w * 0.31), int(h * 0.78)),
    ]
    draw.polygon(island, fill=(172, 174, 171), outline=INK)
    draw.rectangle((int(w * 0.35), int(h * 0.55), int(w * 0.71), int(h * 0.60)), fill=(211, 205, 194), outline=INK, width=2)
    for i in range(3):
        cx = int(w * (0.42 + i * 0.10))
        cy = int(h * 0.76)
        draw.ellipse((cx - 18, cy - 15, cx + 18, cy + 4), fill=(112, 96, 77), outline=INK)
        line(draw, [(cx, cy + 3), (cx, int(h * 0.88))], INK, 3)
    if variant % 2 == 0:
        draw.polygon([(int(w * 0.43), int(h * 0.79)), (int(w * 0.66), int(h * 0.79)), (int(w * 0.72), int(h * 0.91)), (int(w * 0.37), int(h * 0.91))], fill=(226, 224, 219), outline=RED)
        arrow(draw, (int(w * 0.24), int(h * 0.84)), (int(w * 0.78), int(h * 0.84)), RED, 4)
    note(draw, (48, int(h * 0.72)), note_a, (int(w * 0.43), int(h * 0.72)), RED)
    note(draw, (int(w * 0.72), int(h * 0.19)), note_b, (int(w * 0.78), int(h * 0.40)), INK)
    dimension(draw, int(w * 0.24), int(w * 0.80), int(h * 0.94), f"{3.60 + variant * 0.18:.2f} m")
    sketch_overlay(img, seed)
    return img


def scene_open(w, h, seed, title, note_a, note_b, variant=0):
    img = paper(w, h, seed)
    draw = ImageDraw.Draw(img, "RGBA")
    title_block(draw, title, "Sistema 90G · spazio vissuto", w)
    left, top, right, back_bottom, bottom = room_shell(draw, w, h, (231, 229, 223))
    draw.rectangle((int(w * 0.22), int(h * 0.28), int(w * 0.43), int(h * 0.56)), fill=(190, 208, 211), outline=INK, width=2)
    sofa = (int(w * 0.26), int(h * 0.58), int(w * 0.53), int(h * 0.72))
    draw.rounded_rectangle(sofa, radius=15, fill=(165, 162, 154), outline=INK, width=2)
    draw.rectangle((int(w * 0.66), int(h * 0.39), int(w * 0.82), int(h * 0.56)), fill=(211, 208, 200), outline=INK, width=2)
    draw.ellipse((int(w * 0.56), int(h * 0.63), int(w * 0.76), int(h * 0.76)), fill=(174, 148, 111), outline=INK, width=2)
    for x in (0.59, 0.70):
        line(draw, [(int(w * x), int(h * 0.73)), (int(w * x), int(h * 0.84))], INK, 3)
    path = [(int(w * 0.10), int(h * 0.80)), (int(w * 0.38), int(h * 0.70)), (int(w * 0.61), int(h * 0.83)), (int(w * 0.88), int(h * 0.69))]
    draw.line(path, fill=GREEN, width=6)
    for i in range(len(path) - 1):
        arrow(draw, path[i], path[i + 1], GREEN, 3)
    note(draw, (50, int(h * 0.69)), note_a, path[1], GREEN)
    note(draw, (int(w * 0.69), int(h * 0.23)), note_b, (int(w * 0.72), int(h * 0.57)), INK)
    dimension(draw, int(w * 0.19), int(w * 0.84), int(h * 0.94), f"{7.80 + variant * 0.22:.2f} m")
    sketch_overlay(img, seed)
    return img


def scene_bath(w, h, seed, title, note_a, note_b, variant=0):
    img = paper(w, h, seed)
    draw = ImageDraw.Draw(img, "RGBA")
    title_block(draw, title, "Sistema 90G · bagno e impianti", w)
    left, top, right, back_bottom, bottom = room_shell(draw, w, h, (226, 225, 219))
    draw.rectangle((int(w * 0.27), int(h * 0.30), int(w * 0.45), int(h * 0.66)), fill=(196, 210, 211), outline=INK, width=2)
    draw.rounded_rectangle((int(w * 0.54), int(h * 0.54), int(w * 0.66), int(h * 0.69)), radius=35, fill=(246, 245, 241), outline=INK, width=2)
    draw.rounded_rectangle((int(w * 0.72), int(h * 0.42), int(w * 0.82), int(h * 0.68)), radius=14, fill=(244, 243, 239), outline=INK, width=2)
    draw.rectangle((int(w * 0.47), int(h * 0.35), int(w * 0.66), int(h * 0.43)), fill=(210, 202, 190), outline=INK, width=2)
    swing = [(int(w * 0.84), int(h * 0.69)), (int(w * 0.74), int(h * 0.82)), (int(w * 0.66), int(h * 0.88))]
    draw.line(swing, fill=RED, width=5)
    note(draw, (42, int(h * 0.69)), note_a, (int(w * 0.60), int(h * 0.66)), RED)
    note(draw, (int(w * 0.70), int(h * 0.22)), note_b, (int(w * 0.78), int(h * 0.52)), INK)
    dimension(draw, int(w * 0.24), int(w * 0.82), int(h * 0.94), f"{2.40 + variant * 0.10:.2f} m")
    sketch_overlay(img, seed)
    return img


def scene_plan(w, h, seed, title, note_a, note_b, variant=0):
    img = paper(w, h, seed)
    draw = ImageDraw.Draw(img, "RGBA")
    title_block(draw, title, "Sistema 90G · distribuzione", w)
    x0, y0, x1, y1 = int(w * 0.19), int(h * 0.19), int(w * 0.82), int(h * 0.82)
    draw.rectangle((x0, y0, x1, y1), fill=(251, 250, 247), outline=INK, width=6)
    walls = [
        ((0.48, 0.19), (0.48, 0.82)),
        ((0.48, 0.47), (0.82, 0.47)),
        ((0.19, 0.53), (0.48, 0.53)),
    ]
    for a, b in walls:
        line(draw, [(int(w * a[0]), int(h * a[1])), (int(w * b[0]), int(h * b[1]))], INK, 6)
    draw.rectangle((int(w * 0.24), int(h * 0.27), int(w * 0.39), int(h * 0.41)), fill=(205, 196, 181), outline=INK, width=2)
    draw.rectangle((int(w * 0.57), int(h * 0.27), int(w * 0.74), int(h * 0.40)), fill=(203, 211, 211), outline=INK, width=2)
    draw.rectangle((int(w * 0.26), int(h * 0.62), int(w * 0.43), int(h * 0.75)), fill=(183, 166, 144), outline=INK, width=2)
    draw.rectangle((int(w * 0.57), int(h * 0.57), int(w * 0.72), int(h * 0.73)), fill=(225, 221, 213), outline=INK, width=2)
    path = [(int(w * 0.20), int(h * 0.84)), (int(w * 0.44), int(h * 0.70)), (int(w * 0.56), int(h * 0.80)), (int(w * 0.83), int(h * 0.62))]
    draw.line(path, fill=GREEN, width=6)
    note(draw, (35, int(h * 0.69)), note_a, path[1], GREEN)
    note(draw, (int(w * 0.70), int(h * 0.18)), note_b, (int(w * 0.68), int(h * 0.55)), INK)
    dimension(draw, x0, x1, int(h * 0.92), f"{6.20 + variant * 0.30:.2f} m")
    sketch_overlay(img, seed)
    return img


def scene_quote(w, h, seed, title, note_a, note_b, variant=0):
    img = paper(w, h, seed)
    draw = ImageDraw.Draw(img, "RGBA")
    title_block(draw, title, "Sistema 90G · costo e valore", w)
    draw.rounded_rectangle((int(w * 0.18), int(h * 0.18), int(w * 0.60), int(h * 0.82)), radius=14, fill=(251, 250, 247), outline=INK, width=3)
    for i in range(6):
        y = int(h * (0.29 + i * 0.075))
        line(draw, [(int(w * 0.23), y), (int(w * 0.54), y)], (126, 134, 129), 2)
        draw.rectangle((int(w * 0.24), y - 13, int(w * (0.33 + 0.03 * (i % 3))), y + 4), fill=(143 + i * 6, 120 + i * 5, 91 + i * 4))
    draw.rounded_rectangle((int(w * 0.68), int(h * 0.25), int(w * 0.84), int(h * 0.60)), radius=18, fill=(66, 76, 80), outline=INK, width=3)
    draw.rectangle((int(w * 0.71), int(h * 0.30), int(w * 0.81), int(h * 0.38)), fill=(211, 222, 222))
    for r in range(3):
        for c in range(3):
            cx = int(w * (0.72 + c * 0.04))
            cy = int(h * (0.44 + r * 0.06))
            draw.ellipse((cx, cy, cx + 20, cy + 20), fill=(232, 232, 228))
    note(draw, (40, int(h * 0.69)), note_a, (int(w * 0.40), int(h * 0.57)), RED)
    note(draw, (int(w * 0.66), int(h * 0.16)), note_b, (int(w * 0.76), int(h * 0.33)), INK)
    dimension(draw, int(w * 0.20), int(w * 0.84), int(h * 0.92), "voci · quantità · esclusioni")
    sketch_overlay(img, seed)
    return img


def scene_bedroom(w, h, seed, title, note_a, note_b, variant=0):
    img = paper(w, h, seed)
    draw = ImageDraw.Draw(img, "RGBA")
    title_block(draw, title, "Sistema 90G · camera", w)
    left, top, right, back_bottom, bottom = room_shell(draw, w, h, (228, 225, 219))
    draw.rounded_rectangle((int(w * 0.27), int(h * 0.49), int(w * 0.59), int(h * 0.73)), radius=15, fill=(196, 188, 177), outline=INK, width=2)
    draw.rectangle((int(w * 0.30), int(h * 0.53), int(w * 0.42), int(h * 0.62)), fill=(246, 244, 239), outline=INK)
    draw.rectangle((int(w * 0.44), int(h * 0.53), int(w * 0.56), int(h * 0.62)), fill=(246, 244, 239), outline=INK)
    draw.rectangle((int(w * 0.68), int(h * 0.29), int(w * 0.83), int(h * 0.68)), fill=(139, 115, 88), outline=INK, width=2)
    for x in (0.73, 0.78):
        line(draw, [(int(w * x), int(h * 0.29)), (int(w * x), int(h * 0.68))], (226, 216, 202), 2)
    path = [(int(w * 0.59), int(h * 0.80)), (int(w * 0.72), int(h * 0.72)), (int(w * 0.86), int(h * 0.70))]
    draw.line(path, fill=GREEN, width=6)
    note(draw, (45, int(h * 0.68)), note_a, path[0], GREEN)
    note(draw, (int(w * 0.70), int(h * 0.20)), note_b, (int(w * 0.76), int(h * 0.52)), INK)
    dimension(draw, int(w * 0.22), int(w * 0.84), int(h * 0.94), f"{4.00 + variant * 0.18:.2f} m")
    sketch_overlay(img, seed)
    return img


def save(img: Image.Image, name: str, size=(1200, 760)):
    img = img.resize(size, Image.Resampling.LANCZOS)
    img.save(IMAGES / name, "JPEG", quality=90, optimize=True, progressive=True)


CASES = [
    ("caso-lavastoviglie-passaggio-2026.jpg", scene_kitchen, "Cucina · passaggio", "sportello aperto", "passaggio reale?", 1),
    ("caso-ingresso-living-2026.jpg", scene_open, "Open space · ingresso", "percorso principale", "privacy e tavolo", 2),
    ("caso-cucina-tre-lati-2026.jpg", scene_kitchen, "Cucina compatta", "ante aperte", "centro stanza", 3),
    ("caso-preventivo-valore-2026.jpg", scene_quote, "Preventivo cucina", "materiali e lavorazioni", "cosa compone il totale?", 4),
    ("caso-isola-passaggi-2026.jpg", scene_kitchen, "Cucina con isola", "sedute in uso", "spazio di manovra", 5),
    ("caso-secondo-bagno-2026.jpg", scene_bath, "Secondo bagno", "accesso e sanitari", "impianti da verificare", 6),
    ("caso-open-space-tv-2026.jpg", scene_open, "Open space", "tv, divano e luce", "percorso quotidiano", 7),
    ("caso-lavello-finestra-2026.jpg", scene_kitchen, "Lavello sotto finestra", "rubinetto e anta", "apertura infisso", 8),
    ("caso-scala-planimetria-2026.jpg", scene_plan, "Scala interna", "partenza e sbarco", "la pianta cambia", 9),
    ("caso-percorso-centrale-2026.jpg", scene_plan, "Distribuzione", "stanze aperte", "percorso centrale", 10),
    ("caso-terza-camera-2026.jpg", scene_plan, "Redistribuzione", "nuova camera", "zona giorno residua", 11),
    ("caso-profondita-angolo-2026.jpg", scene_kitchen, "Cucina ad angolo", "profondità 75 cm", "accesso interno", 12),
    ("caso-bagno-lavatrice-2026.jpg", scene_bath, "Bagno e lavanderia", "porta più larga", "spazio utile", 13),
    ("caso-cabina-armadio-2026.jpg", scene_bedroom, "Camera da letto", "cabina e passaggi", "la forma decide", 14),
    ("caso-divano-letto-2026.jpg", scene_open, "Piccolo appartamento", "giorno e notte", "funzioni in conflitto", 15),
]

for filename, maker, title, a, b, seed in CASES:
    save(maker(1200, 760, seed, title, a, b, seed % 4), filename)

HEROES = {
    "hero-home-90g-2026.jpg": scene_open(1600, 1000, 101, "Analisi preventiva", "spazi in uso", "decisioni da chiarire", 1),
    "hero-cucina-90g-2026.jpg": scene_kitchen(1600, 1000, 102, "Controllo cucina", "aperture e passaggi", "prima dell'ordine", 2),
    "hero-planimetria-90g-2026.jpg": scene_plan(1600, 1000, 103, "Verifica planimetria", "funzioni e percorsi", "prima dei lavori", 3),
    "hero-preventivo-90g-2026.jpg": scene_quote(1600, 1000, 104, "Analisi preventivo", "voci e materiali", "valore ottenuto", 1),
    "hero-casi-90g-2026.jpg": scene_open(1600, 1000, 105, "Casi analizzati", "problemi reali", "conseguenze concrete", 2),
    "hero-chi-sono-90g-2026.jpg": scene_kitchen(1600, 1000, 106, "Sistema 90G", "controllo indipendente", "prima di decidere", 3),
}
for filename, image in HEROES.items():
    save(image, filename, (1600, 1000))

# Rimuove eventuali frammenti tecnici creati durante le prove.
for part in (ROOT / "tools").glob("visual-reference.part*"):
    part.unlink(missing_ok=True)

case_page_map = {
    "caso-lavastoviglie-passaggio-cucina.html": "caso-lavastoviglie-passaggio-2026.jpg",
    "caso-ingresso-tavolo-living.html": "caso-ingresso-living-2026.jpg",
    "caso-cucina-piccola-tre-lati.html": "caso-cucina-tre-lati-2026.jpg",
    "caso-preventivo-cucina-sconto-valore.html": "caso-preventivo-valore-2026.jpg",
    "caso-isola-passaggi-cucina.html": "caso-isola-passaggi-2026.jpg",
    "caso-secondo-bagno-impianti-spazio.html": "caso-secondo-bagno-2026.jpg",
    "caso-open-space-tv-divano-passaggi.html": "caso-open-space-tv-2026.jpg",
    "caso-lavello-sotto-finestra-aperture.html": "caso-lavello-finestra-2026.jpg",
    "caso-scala-interna-terrazzo-planimetria.html": "caso-scala-planimetria-2026.jpg",
    "caso-open-space-percorso-centrale.html": "caso-percorso-centrale-2026.jpg",
    "caso-terza-camera-zona-giorno.html": "caso-terza-camera-2026.jpg",
    "caso-cucina-profondita-75-angolo.html": "caso-profondita-angolo-2026.jpg",
    "caso-bagno-lavatrice-dieci-centimetri.html": "caso-bagno-lavatrice-2026.jpg",
    "caso-cabina-armadio-camera-irregolare.html": "caso-cabina-armadio-2026.jpg",
    "caso-divano-letto-soggiorno-tre-persone.html": "caso-divano-letto-2026.jpg",
}

collection = ROOT / "casi-analizzati.html"
text = collection.read_text(encoding="utf-8")
for page_name, image_name in case_page_map.items():
    pattern = r'(<article><img class="case-card-image" src=")[^"]+("[^>]*>.*?<a class="text-link" href="' + re.escape(page_name) + r'")'
    text, count = re.subn(pattern, rf'\1images/{image_name}?v={VERSION}\2', text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"Card non trovata per {page_name}")
text = re.sub(r'(<figure class="premium-image"><img src=")[^"]+', rf'\1images/hero-casi-90g-2026.jpg?v={VERSION}', text, count=1)
collection.write_text(text, encoding="utf-8")

page_heroes = {
    "index.html": "hero-home-90g-2026.jpg",
    "controllo-progetto-cucina.html": "hero-cucina-90g-2026.jpg",
    "verifica-planimetria-distribuzione-casa.html": "hero-planimetria-90g-2026.jpg",
    "analisi-preventivo-cucina.html": "hero-preventivo-90g-2026.jpg",
    "chi-e-sistema90g.html": "hero-chi-sono-90g-2026.jpg",
}
page_heroes.update(case_page_map)

for page_name, image_name in page_heroes.items():
    page = ROOT / page_name
    if not page.exists():
        continue
    html = page.read_text(encoding="utf-8")
    replacement = f'images/{image_name}?v={VERSION}'
    patterns = [
        r'(<figure class="premium-image">\s*<img src=")[^"]+',
        r'(<section class="hero[^>]*>.*?<img[^>]*src=")[^"]+',
    ]
    changed = False
    for pattern in patterns:
        html, count = re.subn(pattern, rf'\1{replacement}', html, count=1, flags=re.S)
        if count:
            changed = True
            break
    if changed:
        page.write_text(html, encoding="utf-8")

manifest = ROOT / "images" / "VISUAL-MANIFEST-2026.txt"
manifest.write_text("\n".join(sorted([name for name, *_ in CASES] + list(HEROES.keys()))) + "\n", encoding="utf-8")
print(f"Creati {len(CASES)} visual caso e {len(HEROES)} visual hero.")
