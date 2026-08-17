from pathlib import Path

ROOT = Path.cwd()


def replace_once(path, old, new, label):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    if new in s:
        print(f"SKIP {path}: {label} già presente")
        return
    if old not in s:
        raise SystemExit(f"ERRORE {path}: punto non trovato per {label}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")
    print(f"OK {path}: {label}")


# 1) Errori progetto: risposta autonoma subito dopo l'introduzione.
replace_once(
    "errori-progetto-cucina.html",
    '<p class="s90g-guide__intro">Un progetto può apparire corretto nel render e mostrare problemi solo quando si considerano aperture, persone in movimento, elettrodomestici in uso e misure reali. Prima della conferma conviene verificare il funzionamento della cucina, non soltanto il suo aspetto.</p>',
    '<p class="s90g-guide__intro">Un progetto può apparire corretto nel render e mostrare problemi solo quando si considerano aperture, persone in movimento, elettrodomestici in uso e misure reali. Prima della conferma conviene verificare il funzionamento della cucina, non soltanto il suo aspetto.</p><section class="s90g-callout" aria-labelledby="errori-in-breve"><h2 id="errori-in-breve">In breve: quali errori conviene controllare prima dell\'ordine?</h2><p>I controlli più importanti riguardano misure reali, passaggi con ante ed elettrodomestici aperti, isole e penisole, installazione degli elettrodomestici, impianti, coerenza del preventivo e scelta delle finiture. Il punto è verificare come questi elementi funzionano insieme nell\'uso quotidiano, non soltanto come appaiono nel render.</p></section>',
    "risposta breve"
)

# 2) Confronto preventivi: risposta diretta + Article/FAQ coerenti con il testo visibile.
p = ROOT / "confrontare-due-preventivi-cucina.html"
s = p.read_text(encoding="utf-8")
lead = '<p class="s90g-lead">Due rivenditori possono proporre soluzioni diverse perché lavorano con prodotti, modularità, servizi e impostazioni differenti. Per questo il confronto più utile parte da ciò che ciascuna proposta comprende.</p>'
answer = lead + '<section class="s90g-callout" aria-labelledby="confronto-in-breve"><h2 id="confronto-in-breve">In breve: come si confrontano due preventivi cucina?</h2><p>Prima si rende comparabile ciò che viene fornito: composizione, materiali, elettrodomestici, top, lavorazioni, trasporto, montaggio, servizi, inclusioni ed esclusioni. Solo dopo ha senso confrontare il prezzo finale, perché due totali diversi possono riferirsi a cucine e condizioni diverse.</p></section>'
if answer not in s:
    if lead not in s:
        raise SystemExit("ERRORE confrontare-due-preventivi-cucina.html: lead non trovato")
    s = s.replace(lead, answer, 1)

if 'type="application/ld+json"' not in s:
    marker = '</head>'
    schema = '<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Article","@id":"https://sistema90g.it/confrontare-due-preventivi-cucina.html#article","headline":"Confrontare due preventivi cucina","description":"Come confrontare due preventivi cucina rendendo comparabili composizione, materiali, elettrodomestici, servizi, inclusioni ed esclusioni prima del prezzo.","mainEntityOfPage":"https://sistema90g.it/confrontare-due-preventivi-cucina.html","author":{"@type":"Person","name":"Gian Carlo Primo"},"publisher":{"@id":"https://sistema90g.it/#organization"},"inLanguage":"it-IT"},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Come si confrontano due preventivi cucina?","acceptedAnswer":{"@type":"Answer","text":"Prima si rende comparabile ciò che viene fornito: composizione, materiali, elettrodomestici, top, lavorazioni, trasporto, montaggio, servizi, inclusioni ed esclusioni. Solo dopo ha senso confrontare il prezzo finale."}}]}]}</script>'
    s = s.replace(marker, schema + marker, 1)
p.write_text(s, encoding="utf-8")
print("OK confrontare-due-preventivi-cucina.html: risposta breve + schema")

# 3) Prima della firma: risposta breve coerente con le FAQ già marcate.
replace_once(
    "prima-di-firmare-ordine-cucina.html",
    '<p class="s90g-lead">La firma è il momento in cui molte decisioni sviluppate nelle settimane precedenti vengono riunite in un unico ordine. Una rilettura finale serve soprattutto ad allineare cliente e rivenditore sulla stessa soluzione.</p>',
    '<p class="s90g-lead">La firma è il momento in cui molte decisioni sviluppate nelle settimane precedenti vengono riunite in un unico ordine. Una rilettura finale serve soprattutto ad allineare cliente e rivenditore sulla stessa soluzione.</p><section class="s90g-callout" aria-labelledby="firma-in-breve"><h2 id="firma-in-breve">In breve: cosa chiarire prima di firmare l\'ordine della cucina?</h2><p>Verifica con il rivenditore che progetto aggiornato, rilievo, moduli, elettrodomestici, top, finiture, trasporto, montaggio, altri servizi, tempi e condizioni descrivano tutti la stessa cucina. Se una modifica è intervenuta durante lo sviluppo, deve risultare anche nei documenti che stai confermando.</p></section>',
    "risposta breve"
)

# 4) Misure e passaggi: risposta autonoma + consolidamento commerciale.
p = ROOT / "misure-passaggi-cucina.html"
s = p.read_text(encoding="utf-8")
intro = '<p class="intro">Una cucina non si valuta soltanto dalla somma delle larghezze dei mobili. Le misure devono descrivere anche ciò che succede quando si apre una lavastoviglie, si usa un cassetto, si passa dietro una persona o si accede al frigorifero.</p>'
intro_new = intro + '<section class="s90g-callout" aria-labelledby="misure-in-breve"><h2 id="misure-in-breve">In breve: quali misure contano davvero in cucina?</h2><p>Non conta una sola distanza standard: vanno letti insieme spazio libero, aperture di ante ed elettrodomestici, porte e finestre, profondità dei mobili, sedute e percorsi delle persone. La stessa quota può essere sufficiente in una configurazione e creare interferenze in un\'altra.</p></section>'
if intro_new not in s:
    if intro not in s:
        raise SystemExit("ERRORE misure-passaggi-cucina.html: intro non trovato")
    s = s.replace(intro, intro_new, 1)
old = '<h2>Dal dubbio alla verifica</h2><p>Se il problema riguarda una singola misura o interferenza può bastare un <a href="/controllo-mirato.html">Controllo mirato</a>. Se misure, aperture, composizione e percorsi vanno letti insieme, è più coerente l\'<a href="/analisi-completa.html">Analisi completa</a>.</p>'
new = '<h2>Dal dubbio alla verifica</h2><p>Se hai già un progetto o un preventivo, la <a href="/seconda-opinione-cucina.html">Seconda Opinione</a> prevede due livelli: “dubbio preciso” quando vuoi verificare una singola misura o interferenza, e “controllo completo” quando misure, aperture, composizione e percorsi devono essere letti insieme.</p>'
if old in s:
    s = s.replace(old, new, 1)
elif new not in s:
    raise SystemExit("ERRORE misure-passaggi-cucina.html: blocco commerciale non trovato")
p.write_text(s, encoding="utf-8")
print("OK misure-passaggi-cucina.html: risposta breve + Seconda Opinione")

# 5) Quando serve la verifica: contenuto più citabile + Article schema, senza duplicare la landing.
p = ROOT / "quando-verifica-indipendente-cucina.html"
s = p.read_text(encoding="utf-8")
lead = '<p class="s90g-lead">Non ogni acquisto ha bisogno di un\'analisi esterna. In molti casi è sufficiente il confronto con il proprio rivenditore o professionista. Una seconda opinione acquista valore quando rimane un dubbio specifico che si vuole capire meglio prima della decisione.</p>'
answer = lead + '<section class="s90g-callout" aria-labelledby="seconda-opinione-in-breve"><h2 id="seconda-opinione-in-breve">In breve: quando può servire una seconda opinione sulla cucina?</h2><p>Può essere utile quando, dopo il confronto con il rivenditore, resta un dubbio concreto su progetto, misure, passaggi, elettrodomestici o preventivo, oppure quando vuoi rileggere l\'insieme prima dell\'ordine. Non serve invece a sostituire rilievo definitivo, fattibilità, adattamento al marchio o responsabilità del punto vendita.</p></section>'
if answer not in s:
    if lead not in s:
        raise SystemExit("ERRORE quando-verifica-indipendente-cucina.html: lead non trovato")
    s = s.replace(lead, answer, 1)
if 'type="application/ld+json"' not in s:
    marker = '</head>'
    schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","@id":"https://sistema90g.it/quando-verifica-indipendente-cucina.html#article","headline":"Quando può essere utile una seconda opinione sulla cucina","description":"Quando una seconda opinione può chiarire dubbi su progetto o preventivo cucina senza sostituire il rivenditore.","mainEntityOfPage":"https://sistema90g.it/quando-verifica-indipendente-cucina.html","author":{"@type":"Person","name":"Gian Carlo Primo"},"publisher":{"@id":"https://sistema90g.it/#organization"},"inLanguage":"it-IT"}</script>'
    s = s.replace(marker, schema + marker, 1)
p.write_text(s, encoding="utf-8")
print("OK quando-verifica-indipendente-cucina.html: risposta breve + Article")

print("Search Everywhere: guide ad alta intenzione rese più citabili.")
