from pathlib import Path

PATCHES = {
    "errori-progetto-cucina.html": {
        "marker": '<div class="s90g-guide__links">',
        "insert": '<h2>Quando serve passare dalla guida alla verifica del progetto</h2><p>Se uno di questi errori riguarda una cucina già disegnata o un preventivo già ricevuto, la verifica più utile è quella fatta sul materiale reale: misure disponibili, composizione proposta, aperture, impianti ed eventuali vincoli dell’ambiente. In quel caso il percorso coerente è la <a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Seconda Opinione</a>. Se invece la cucina deve ancora essere definita, conviene partire dal <a href="/progetto-cucina-sistema90g.html">Progetto Cucina 90G</a>.</p>',
        "mode": "before",
    },
    "montaggio-allacciamenti-cucina-cosa-chiarire.html": {
        "marker": '<section class="s90g-shell s90g-guide-cta">',
        "insert": '<section class="s90g-shell s90g-guide-cta"><h2>Prima dell’ordine conviene distinguere fornitura, montaggio e lavori accessori</h2><p>Le voci relative a consegna, montaggio, allacciamenti, modifiche impiantistiche e opere murarie non sono sempre comprese nello stesso modo. Se il preventivo è già disponibile, una <a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Seconda Opinione</a> può aiutare a leggere insieme progetto e condizioni prima della firma.</p></section>',
        "mode": "before",
    },
    "voci-escluse-preventivo-cucina.html": {
        "marker": '<p><a href="/analisi-preventiva.html#percorso">Valuta la tua cucina →</a></p>',
        "insert": '<h2>Le esclusioni contano quanto il prezzo finale</h2><p>Due preventivi con importi simili possono coprire attività diverse. Per confrontarli occorre verificare che siano chiare consegna, montaggio, allacciamenti, lavorazioni del top, accessori, eventuali rilievi e opere non comprese. Quando hai già il preventivo, il percorso più coerente è la <a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Seconda Opinione</a>.</p>',
        "mode": "before",
    },
    "materiali-finiture-cucina-guide.html": {
        "marker": '<section class="s90g-shell s90g-guide-cta">',
        "insert": '<section class="s90g-shell s90g-guide-cta"><h2>Quando le finiture fanno parte del progetto</h2><p>Ante, top, pavimento, luce e colori vanno letti insieme alla composizione. Se la cucina deve ancora essere progettata, queste scelte possono essere sviluppate con il <a href="/progetto-cucina-sistema90g.html">Progetto Cucina 90G</a> e l’add-on <a href="/scelta-finiture-cucina.html">Finiture e materiali</a>.</p></section>',
        "mode": "before",
    },
}

for filename, spec in PATCHES.items():
    path = Path(filename)
    text = path.read_text()
    heading = spec["insert"].split("</h2>", 1)[0].split("<h2>", 1)[-1]
    if heading in text:
        print(f"SKIP {filename}: già aggiornato")
        continue
    if spec["marker"] not in text:
        raise SystemExit(f"Marker non trovato in {filename}")
    if spec["mode"] == "before":
        text = text.replace(spec["marker"], spec["insert"] + spec["marker"], 1)
    else:
        text = text.replace(spec["marker"], spec["marker"] + spec["insert"], 1)
    path.write_text(text)
    print(f"OK {filename}")

print("Search Everywhere: terzo lotto collegamenti commerciali contestuali completato.")
