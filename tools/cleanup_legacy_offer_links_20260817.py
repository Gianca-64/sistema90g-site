from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Skip generated/development areas: only source HTML files in the repository root
html_files = [p for p in ROOT.glob('*.html') if p.is_file()]

changed = []
for p in html_files:
    s = p.read_text()
    original = s

    # Canonical destinations for the new commercial architecture.
    replacements = {
        'href="/controllo-mirato.html"': 'href="/seconda-opinione-cucina.html#livelli-seconda-opinione"',
        'href="controllo-mirato.html"': 'href="/seconda-opinione-cucina.html#livelli-seconda-opinione"',
        'href="/analisi-completa.html"': 'href="/seconda-opinione-cucina.html#livelli-seconda-opinione"',
        'href="analisi-completa.html"': 'href="/seconda-opinione-cucina.html#livelli-seconda-opinione"',
        'href="/acquisto-assistito-cucina.html"': 'href="/progetto-cucina-sistema90g.html"',
        'href="acquisto-assistito-cucina.html"': 'href="/progetto-cucina-sistema90g.html"',
    }
    for old, new in replacements.items():
        s = s.replace(old, new)

    # Align visible labels where the old services still appear in source copy.
    text_replacements = {
        'Controllo mirato': 'Seconda Opinione · dubbio preciso',
        'Analisi completa': 'Seconda Opinione · controllo completo',
        'Acquisto Assistito Cucina 90G': 'Progetto Cucina 90G',
        'Acquisto assistito': 'Progetto Cucina',
    }
    for old, new in text_replacements.items():
        s = s.replace(old, new)

    if s != original:
        p.write_text(s)
        changed.append(p.name)

print(f"File HTML aggiornati: {len(changed)}")
for name in changed:
    print(f" - {name}")
print("Bonifica globale vecchia architettura commerciale completata.")
