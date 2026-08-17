from pathlib import Path

PATCHES = {
    "preventivo-cucina-guida.html": {
        "marker": '<p class="s90g-lead">Il totale finale non basta per capire se un preventivo è completo e confrontabile. Prima dell\'ordine conviene verificare cosa è realmente compreso.</p>',
        "insert": '<section class="s90g-callout" aria-labelledby="preventivo-in-breve"><h2 id="preventivo-in-breve">In breve: come capire se un preventivo cucina è davvero confrontabile?</h2><p>Il totale non basta. Per confrontare due proposte bisogna verificare che descrivano una fornitura equivalente: moduli, misure, finiture, top, elettrodomestici, accessori, trasporto, montaggio, rilievo ed eventuali esclusioni. Se cambia anche uno solo di questi elementi, cambia anche il significato del prezzo finale.</p></section>'
    },
    "rilievo-misure-cucina-prima-ordine.html": {
        "marker": '<p class="s90g-lead">Una base progettuale può essere sviluppata su quote disponibili o indicative. Prima dell\'ordine, il rivenditore verifica l\'ambiente e adatta la soluzione alle misure reali, alla propria modularità e ai prodotti scelti.</p>',
        "insert": '<section class="s90g-callout" aria-labelledby="rilievo-in-breve"><h2 id="rilievo-in-breve">In breve: quando va fatto il rilievo definitivo della cucina?</h2><p>Va fatto quando l’ambiente è abbastanza definito da poter misurare ciò che inciderà davvero sulla fornitura e comunque prima dell’ordine esecutivo. Oltre alle pareti, possono contare fuori squadra, aperture, davanzali, pilastri, impianti, rivestimenti e quote finite. Se il rilievo modifica il progetto, progetto e preventivo devono essere aggiornati in modo coerente prima della firma.</p></section>'
    },
    "prima-di-firmare-ordine-cucina.html": {
        "marker": '<p><a href="/preventivo-cucina-guida.html">Come leggere il preventivo cucina →</a></p>',
        "insert": '<p><a href="/rilievo-misure-cucina-prima-ordine.html">Rilievo misure cucina: quando farlo e cosa controllare →</a></p>'
    },
    "montaggio-allacciamenti-cucina-cosa-chiarire.html": {
        "marker": '<p class="s90g-lead">Ogni rivenditore può organizzare servizi e figure coinvolte in modo diverso. Per questo è utile leggere ciò che è compreso nella propria offerta e chiedere chiarimenti quando una voce non è esplicita.</p>',
        "insert": '<section class="s90g-callout" aria-labelledby="montaggio-in-breve"><h2 id="montaggio-in-breve">In breve: il montaggio cucina comprende sempre gli allacciamenti?</h2><p>No. Trasporto, montaggio dei mobili, posa del top, installazione degli elettrodomestici e collegamenti agli impianti possono essere compresi, esclusi o affidati a figure diverse. Prima della firma conviene quindi verificare nel preventivo chi fa cosa, quali attività sono incluse e quali richiedono professionisti o costi separati.</p></section>'
    },
}

for filename, spec in PATCHES.items():
    path = Path(filename)
    text = path.read_text()
    if spec["insert"] in text:
        print(f"SKIP {filename}: già aggiornato")
        continue
    if spec["marker"] not in text:
        raise SystemExit(f"Marker non trovato in {filename}")
    text = text.replace(spec["marker"], spec["marker"] + spec["insert"], 1)
    path.write_text(text)
    print(f"OK {filename}")

# Rafforza il percorso sequenziale tra le quattro fasi.
links = {
    "preventivo-cucina-guida.html": ('<p><a href="/prima-di-firmare-ordine-cucina.html">Prima di firmare l\'ordine cucina →</a></p>', '<p><a href="/rilievo-misure-cucina-prima-ordine.html">Rilievo misure cucina prima dell\'ordine →</a></p><p><a href="/prima-di-firmare-ordine-cucina.html">Prima di firmare l\'ordine cucina →</a></p>'),
    "rilievo-misure-cucina-prima-ordine.html": ('<a href="/prima-di-firmare-ordine-cucina.html">Prima della firma →</a>', '<a href="/preventivo-cucina-guida.html">Leggere il preventivo →</a><a href="/prima-di-firmare-ordine-cucina.html">Prima della firma →</a>'),
    "montaggio-allacciamenti-cucina-cosa-chiarire.html": ('<a href="/prima-di-firmare-ordine-cucina.html">Prima di firmare l\'ordine →</a>', '<a href="/rilievo-misure-cucina-prima-ordine.html">Rilievo misure →</a><a href="/prima-di-firmare-ordine-cucina.html">Prima di firmare l\'ordine →</a>'),
}

for filename, (old, new) in links.items():
    path = Path(filename)
    text = path.read_text()
    if new in text:
        continue
    if old not in text:
        raise SystemExit(f"Link marker non trovato in {filename}")
    path.write_text(text.replace(old, new, 1))

print("Search Everywhere: cluster prima dell'ordine rafforzato.")
