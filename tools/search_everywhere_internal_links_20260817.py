from pathlib import Path

FILES = [
    Path("progettare-cucina-guide.html"),
    Path("preventivo-acquisto-cucina-guide.html"),
]

repls = {
    '/controllo-mirato.html': '/seconda-opinione-cucina.html#livelli-seconda-opinione',
    '/analisi-completa.html': '/seconda-opinione-cucina.html#livelli-seconda-opinione',
    'il <a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Controllo mirato</a> concentra l\'analisi su quella criticità. Per verificare l\'intero progetto, usa l\'<a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Analisi completa</a>.':
    'la <a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Seconda Opinione</a> prevede due livelli: dubbio preciso per un punto circoscritto oppure controllo completo per leggere insieme progetto, misure e preventivo.',
    '<a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Controllo mirato →</a><a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Analisi completa →</a>':
    '<a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Seconda Opinione · dubbio preciso →</a><a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Seconda Opinione · controllo completo →</a>',
}

for path in FILES:
    s = path.read_text()
    before = s
    for old, new in repls.items():
        s = s.replace(old, new)
    if s == before:
        print(f"NESSUNA MODIFICA: {path}")
    else:
        path.write_text(s)
        print(f"OK: {path}")

print("Search Everywhere internal linking aggiornato.")
