from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import hashlib
import html
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "IMAGE-AUDIT.md"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif", ".avif"}
IGNORED_NAMES = {"logo-90g.jpg", "favicon-512.png"}


def strip_query(src: str) -> str:
    return src.split("?", 1)[0].split("#", 1)[0]


def title_of(text: str, fallback: str) -> str:
    m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    return html.unescape(re.sub(r"\s+", " ", m.group(1)).strip()) if m else fallback


def context_before(text: str, position: int) -> str:
    before = text[:position]
    matches = list(re.finditer(r"<(h1|h2|h3|p)[^>]*>(.*?)</\1>", before, re.I | re.S))
    if not matches:
        return "—"
    raw = re.sub(r"<[^>]+>", " ", matches[-1].group(2))
    return html.unescape(re.sub(r"\s+", " ", raw).strip())[:140] or "—"


def image_dimensions(path: Path) -> str:
    if path.suffix.lower() == ".svg":
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")[:4000]
            vb = re.search(r"viewBox=[\"']([^\"']+)", text, re.I)
            if vb:
                return f"viewBox {vb.group(1)}"
            width = re.search(r"width=[\"']([^\"']+)", text, re.I)
            height = re.search(r"height=[\"']([^\"']+)", text, re.I)
            if width or height:
                return f"{width.group(1) if width else '?'} × {height.group(1) if height else '?'}"
        except OSError:
            pass
    return "—"


html_files = sorted(ROOT.glob("*.html"))
image_files = sorted(
    p for p in (ROOT / "images").glob("**/*")
    if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
)

refs: list[dict[str, str]] = []
missing: list[tuple[str, str]] = []
runtime_overrides: list[tuple[str, str]] = []

img_re = re.compile(r"<img\b([^>]*?)>", re.I | re.S)
src_re = re.compile(r"\bsrc=[\"']([^\"']+)[\"']", re.I)
alt_re = re.compile(r"\balt=[\"']([^\"']*)[\"']", re.I | re.S)
class_re = re.compile(r"\bclass=[\"']([^\"']*)[\"']", re.I)

for page in html_files:
    text = page.read_text(encoding="utf-8", errors="ignore")
    page_title = title_of(text, page.name)
    for match in img_re.finditer(text):
        attrs = match.group(1)
        src_match = src_re.search(attrs)
        if not src_match:
            continue
        src = html.unescape(src_match.group(1).strip())
        if src.startswith(("data:", "http://", "https://")):
            local = ""
        else:
            local = strip_query(src).lstrip("/")
        alt_match = alt_re.search(attrs)
        class_match = class_re.search(attrs)
        alt = html.unescape(alt_match.group(1).strip()) if alt_match else ""
        classes = class_match.group(1).strip() if class_match else ""
        context = context_before(text, match.start())
        role = "brand" if "brand" in classes or Path(local).name in IGNORED_NAMES else "content"
        refs.append({"page": page.name, "title": page_title, "src": src, "local": local, "alt": alt, "classes": classes, "context": context, "role": role})
        if local and not (ROOT / local).exists():
            missing.append((page.name, src))

for script in sorted(ROOT.glob("*.js")):
    text = script.read_text(encoding="utf-8", errors="ignore")
    for pattern in (r"\.src\s*=", r"setAttribute\(\s*[\"']src", r"querySelectorAll\([^\n]*img"):
        if re.search(pattern, text, re.I):
            runtime_overrides.append((script.name, pattern))

content_refs = [r for r in refs if r["role"] == "content" and r["local"]]
by_image: dict[str, list[dict[str, str]]] = defaultdict(list)
by_page: dict[str, list[dict[str, str]]] = defaultdict(list)
for ref in content_refs:
    by_image[ref["local"]].append(ref)
    by_page[ref["page"]].append(ref)

reused = {image: uses for image, uses in by_image.items() if len(uses) > 1}
pages_without_images = [page.name for page in html_files if page.name not in by_page]
pages_with_multiple = {page: uses for page, uses in by_page.items() if len(uses) > 1}

hashes: dict[str, list[Path]] = defaultdict(list)
for path in image_files:
    try:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes[digest].append(path)
    except OSError:
        pass
binary_duplicates = [paths for paths in hashes.values() if len(paths) > 1]
used = {r["local"] for r in refs if r["local"]}
unused = [p for p in image_files if p.relative_to(ROOT).as_posix() not in used and p.name not in IGNORED_NAMES]

lines: list[str] = [
    "# Audit immagini — Sistema 90G", "",
    "Audit automatico secondo il criterio funzionale definito in `STANDARD_IMMAGINI_SISTEMA90G.md`.",
    "Il numero di immagini per pagina non è un vincolo numerico: zero, una o più immagini sono ammesse se coerenti con la funzione editoriale.", "",
    "## Riepilogo", "",
    f"- Pagine HTML controllate: **{len(html_files)}**",
    f"- File immagine presenti: **{len(image_files)}**",
    f"- Immagini di contenuto pubblicate: **{len(content_refs)}**",
    f"- Asset riutilizzati in più punti (da valutare, non errore): **{len(reused)}**",
    f"- Pagine senza immagini di contenuto (informativo): **{len(pages_without_images)}**",
    f"- Pagine con più immagini di contenuto (informativo): **{len(pages_with_multiple)}**",
    f"- Riferimenti mancanti: **{len(missing)}**",
    f"- Gruppi di file binari identici: **{len(binary_duplicates)}**",
    f"- Immagini non utilizzate: **{len(unused)}**", "",
    "## Mappa pagina → immagine → contesto", "",
    "| Pagina | Immagine | Contesto vicino | Alt |", "|---|---|---|---|"
]
for ref in content_refs:
    lines.append(f"| `{ref['page']}` | `{ref['local']}` | {ref['context'].replace('|', '/')} | {ref['alt'].replace('|', '/')} |")
lines += ["", "## Asset riutilizzati — verifica editoriale", ""]
if reused:
    for image, uses in sorted(reused.items()):
        lines.append(f"### `{image}` — {len(uses)} utilizzi")
        lines.append("")
        for use in uses:
            lines.append(f"- `{use['page']}` — {use['context']}")
        lines.append("")
else:
    lines += ["Nessun asset riutilizzato in più punti.", ""]

lines += ["## Pagine senza immagini — informativo", ""]
lines += [f"- `{page}`" for page in pages_without_images] if pages_without_images else ["Nessuna."]
lines += ["", "## Pagine con più immagini — informativo", ""]
if pages_with_multiple:
    for page, uses in sorted(pages_with_multiple.items()):
        lines.append(f"- `{page}` — {len(uses)} immagini")
else:
    lines.append("Nessuna.")

lines += ["", "## Riferimenti mancanti", ""]
if missing:
    lines += [f"- `{page}` → `{src}`" for page, src in missing]
else:
    lines.append("Nessun riferimento mancante.")

lines += ["", "## Script che possono cambiare immagini nel browser", ""]
if runtime_overrides:
    for script, pattern in runtime_overrides:
        lines.append(f"- `{script}` contiene un pattern di sostituzione immagini: `{pattern}`")
else:
    lines.append("Nessuno script modifica dinamicamente gli attributi `src` delle immagini.")

lines += ["", "## Esito automatico", ""]
if missing or runtime_overrides:
    lines.append("**NON CONFORME** — esistono riferimenti mancanti o override runtime da verificare.")
else:
    lines.append("**CONFORME** — nessun riferimento mancante o override runtime. Quantità e riusi restano valutazioni editoriali, non errori numerici.")

REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Report creato: {REPORT}")
print(f"reused={len(reused)} pages_without_images={len(pages_without_images)} pages_with_multiple={len(pages_with_multiple)} missing={len(missing)} runtime_overrides={len(runtime_overrides)}")