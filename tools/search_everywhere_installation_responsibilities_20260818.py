from pathlib import Path

files = {
    "montaggio-allacciamenti-cucina-cosa-chiarire.html": {
        "marker": '<article class="s90g-guide-group"><h2>Cosa chiedere al rivenditore?</h2>',
        "insert": '<article class="s90g-guide-group"><h2>Checklist pratica: chi fa cosa?</h2><ul><li><strong>Montaggio mobili:</strong> assemblaggio, fissaggio e regolazioni della composizione.</li><li><strong>Posa e lavorazioni del top:</strong> verifica se tagli, fori, giunzioni e sigillature sono compresi.</li><li><strong>Installazione elettrodomestici:</strong> chiarisci se comprende solo il posizionamento o anche il collegamento.</li><li><strong>Allacciamenti idrici ed elettrici:</strong> verifica chi li esegue, se sono inclusi e con quali limiti.</li><li><strong>Smaltimento e imballi:</strong> controlla cosa viene ritirato e cosa resta a carico del cliente.</li><li><strong>Lavori impiantistici o murari:</strong> distinguere un semplice collegamento da una modifica dell’impianto o dell’ambiente.</li></ul><p>Il punto non è che tutte queste attività debbano essere comprese nello stesso servizio, ma che siano attribuite chiaramente prima della consegna.</p></article>',
    },
    "voci-escluse-preventivo-cucina.html": {
        "marker": '<h2>Le esclusioni contano quanto il prezzo finale</h2>',
        "insert": '<h2>Montaggio e allacciamenti: due voci da non confondere</h2><p>Montare la cucina e collegarla agli impianti non sono necessariamente la stessa attività. Nel preventivo conviene distinguere montaggio dei mobili, installazione degli elettrodomestici, posa del top, collegamenti idrici ed elettrici, eventuali modifiche degli impianti e smaltimenti. Per una checklist pratica vedi <a href="/montaggio-allacciamenti-cucina-cosa-chiarire.html">chi fa cosa tra montaggio e allacciamenti</a>.</p>',
    },
}

for name, spec in files.items():
    p = Path(name)
    s = p.read_text()
    if spec["insert"] in s:
        print(f"SKIP {name}: già aggiornato")
        continue
    if spec["marker"] not in s:
        raise SystemExit(f"Marker non trovato in {name}")
    s = s.replace(spec["marker"], spec["insert"] + spec["marker"], 1)
    p.write_text(s)
    print(f"OK {name}")

print("Search Everywhere: montaggio, allacciamenti e responsabilità rafforzati.")
