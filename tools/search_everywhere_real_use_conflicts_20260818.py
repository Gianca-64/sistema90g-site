from pathlib import Path

patches = {
    "isola-cucina-distanze-passaggi.html": {
        "marker": '<p class="intro">La domanda utile non è soltanto se l\'isola entra nella stanza, ma se la cucina continua a funzionare quando ante, cassetti, elettrodomestici e sedute sono in uso.</p>',
        "insert": '<section class="s90g-callout" aria-labelledby="isola-in-breve"><h2 id="isola-in-breve">In breve: 90 o 100 cm tra isola e cucina possono bastare?</h2><p>Possono bastare in alcune configurazioni, ma la misura da sola non è sufficiente per decidere. Bisogna verificare cosa si apre sui due lati, se il passaggio resta utilizzabile con lavastoviglie, cassetti o forno aperti, quante persone usano contemporaneamente la cucina e se ci sono sedute. Il riferimento corretto non è una quota universale, ma lo spazio residuo durante l’uso reale.</p></section>'
    },
    "lavastoviglie-cucina-aperture-passaggi.html": {
        "marker": '<p class="s90g-lead">Una lavastoviglie chiusa occupa poco spazio visivo. Aperta, invece, può cambiare completamente il passaggio e interferire con altri elementi.</p>',
        "insert": '<section class="s90g-callout" aria-labelledby="lavastoviglie-in-breve"><h2 id="lavastoviglie-in-breve">In breve: quanto spazio serve davanti alla lavastoviglie?</h2><p>Non basta lo spazio necessario ad abbassare l’anta. Va considerato anche il corpo della persona che carica o scarica, l’eventuale passaggio alle spalle e ciò che può aprirsi sul lato opposto. Se davanti c’è un’isola, una parete o un’altra fila di mobili, la verifica deve essere fatta con la lavastoviglie realmente aperta.</p></section>'
    },
    "frigorifero-cucina-vicino-parete.html": {
        "marker": '<p class="s90g-lead">Una colonna frigo può sembrare corretta in pianta ma diventare scomoda se la parete limita l\'angolo di apertura o impedisce di estrarre completamente cassetti e ripiani.</p>',
        "insert": '<section class="s90g-callout" aria-labelledby="frigo-in-breve"><h2 id="frigo-in-breve">In breve: quanto spazio lasciare tra frigorifero e parete?</h2><p>Non esiste una distanza valida per tutti i modelli. Lo spazio laterale deve permettere l’angolo di apertura richiesto dal frigorifero e l’estrazione completa di cassetti e ripiani, tenendo conto anche di anta, maniglia e ventilazione. La verifica va quindi fatta sul modello effettivamente previsto e sulla sua scheda tecnica.</p></section>'
    }
}

for name, spec in patches.items():
    p = Path(name)
    s = p.read_text()
    heading = spec["insert"].split("</h2>",1)[0].split("<h2",1)[-1]
    if spec["insert"] in s:
        print(f"SKIP {name}: già aggiornato")
        continue
    if spec["marker"] not in s:
        raise SystemExit(f"Marker non trovato in {name}")
    s = s.replace(spec["marker"], spec["marker"] + spec["insert"], 1)
    p.write_text(s)
    print(f"OK {name}")

print("Search Everywhere: conflitti d'uso reali rafforzati su isola, lavastoviglie e frigorifero.")
