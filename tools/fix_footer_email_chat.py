from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_EMAIL = "sistema90g@icloud.com"

changed = []
for path in sorted(ROOT.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    original = text

    # Corregge indirizzi email visibili e link mailto.
    text = re.sub(r"mailto:[^\"']+", f"mailto:{OFFICIAL_EMAIL}", text, flags=re.I)
    text = re.sub(r"info@sistema90g\.it", OFFICIAL_EMAIL, text, flags=re.I)
    text = re.sub(r"sistema90g@sistema90g\.it", OFFICIAL_EMAIL, text, flags=re.I)

    # Rimuove tutti i link WhatsApp residui, lasciando solo il pulsante flottante ufficiale.
    def keep_only_chat_button(match: re.Match) -> str:
        tag = match.group(0)
        if "s90g-chat-button" in tag:
            return tag
        return ""

    text = re.sub(
        r"<a\b[^>]*href=[\"'][^\"']*(?:wa\.me|whatsapp)[^\"']*[\"'][^>]*>.*?</a>",
        keep_only_chat_button,
        text,
        flags=re.I | re.S,
    )

    # Elimina eventuali testi orfani rimasti in fondo pagina.
    text = re.sub(r"\s*Domande rapide\s*", "", text, flags=re.I)
    text = re.sub(r"\s*Chat WhatsApp\s*(?=<|$)", "", text, flags=re.I)

    # Ripristina il testo corretto nel solo pulsante flottante se il passaggio precedente lo ha svuotato.
    text = re.sub(
        r'(<a\b[^>]*class=["\'][^"\']*s90g-chat-button[^"\']*["\'][^>]*>)(\s*)(</a>)',
        r'\1Chat WhatsApp\3',
        text,
        flags=re.I,
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        changed.append(path.name)

print(f"Pagine corrette: {len(changed)}")
for name in changed:
    print(f" - {name}")

# Verifica finale.
errors = []
for path in sorted(ROOT.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    if re.search(r"info@sistema90g\.it|sistema90g@sistema90g\.it", text, flags=re.I):
        errors.append(f"email vecchia: {path.name}")
    links = re.findall(r"<a\b[^>]*href=[\"'][^\"']*(?:wa\.me|whatsapp)[^\"']*[\"'][^>]*>.*?</a>", text, flags=re.I | re.S)
    non_official = [link for link in links if "s90g-chat-button" not in link]
    if non_official:
        errors.append(f"link WhatsApp residuo: {path.name}")

if errors:
    raise SystemExit("\n".join(errors))

print("Verifica superata: email corretta e nessun link WhatsApp residuo.")
