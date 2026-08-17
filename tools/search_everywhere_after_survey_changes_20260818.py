from pathlib import Path

p = Path("rilievo-misure-cucina-prima-ordine.html")
s = p.read_text()

if "Cosa fare se il progetto cambia dopo il rilievo?" in s:
    print("SKIP rilievo-misure-cucina-prima-ordine.html: già aggiornato")
else:
    old = '''<article class="s90g-guide-group"><h2>Perché il progetto può cambiare dopo il rilievo?</h2><p>È normale che una soluzione preliminare venga adattata. Le misure reali, la modularità del marchio, gli elettrodomestici scelti e i dettagli costruttivi possono richiedere variazioni senza modificare necessariamente l'impostazione generale della cucina.</p></article>'''
    new = '''<article class="s90g-guide-group"><h2>Perché il progetto può cambiare dopo il rilievo?</h2><p>È normale che una soluzione preliminare venga adattata. Le misure reali, la modularità del marchio, gli elettrodomestici scelti e i dettagli costruttivi possono richiedere variazioni senza modificare necessariamente l'impostazione generale della cucina.</p><h3>Cosa fare se il progetto cambia dopo il rilievo?</h3><p>Chiedi che la modifica venga spiegata in modo concreto: quale misura o vincolo l'ha resa necessaria, quali elementi della composizione cambiano e se cambiano anche prezzo, prodotti, lavorazioni o passaggi. Prima della firma, il progetto aggiornato e il preventivo devono descrivere la stessa soluzione.</p><ul><li>confronta il progetto prima e dopo il rilievo;</li><li>verifica quali moduli, tamponamenti, top o elettrodomestici sono cambiati;</li><li>controlla se la modifica incide su passaggi, aperture o impianti;</li><li>verifica che eventuali variazioni economiche siano leggibili nel preventivo finale;</li><li>chiedi chiarimenti prima dell'ordine se una modifica non è comprensibile.</li></ul><p>Se il dubbio riguarda la coerenza complessiva tra progetto aggiornato, misure e preventivo, puoi valutare una <a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Seconda Opinione · controllo completo</a>.</p></article>'''
    if old not in s:
        raise SystemExit("Marker non trovato in rilievo-misure-cucina-prima-ordine.html")
    s = s.replace(old, new, 1)
    p.write_text(s)
    print("OK rilievo-misure-cucina-prima-ordine.html")

print("Search Everywhere: modifiche dopo il rilievo rafforzate nella pagina pilastro.")
