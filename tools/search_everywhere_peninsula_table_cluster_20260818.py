from pathlib import Path


def replace_once(path, old, new):
    p = Path(path)
    s = p.read_text()
    if new in s:
        print(f"SKIP {path}: già aggiornato")
        return
    if old not in s:
        raise SystemExit(f"Marker non trovato in {path}")
    p.write_text(s.replace(old, new, 1))
    print(f"OK {path}")

replace_once(
    "penisola-cucina-distanze-passaggi.html",
    '<p class="s90g-lead">Una penisola può aumentare piano di lavoro e contenimento, ma può anche restringere il passaggio o creare interferenze se viene dimensionata senza considerare persone, sedute e aperture.</p>',
    '<p class="s90g-lead">Una penisola può aumentare piano di lavoro e contenimento, ma può anche restringere il passaggio o creare interferenze se viene dimensionata senza considerare persone, sedute e aperture.</p><section class="s90g-callout" aria-labelledby="penisola-in-breve"><h2 id="penisola-in-breve">In breve: quanto spazio serve attorno a una penisola con sgabelli?</h2><p>Non basta misurare il corridoio con gli sgabelli vuoti. Devi considerare una persona seduta, lo spazio per alzarsi, il passaggio alle spalle e le eventuali ante o cassetti vicini. Se la penisola sostituisce anche il tavolo, va verificato se funziona per l’uso quotidiano previsto, non solo per colazione o pasti veloci.</p></section>'
)

replace_once(
    "tavolo-vicino-cucina-spazi-sedute.html",
    '<h2>Cosa significa in pratica</h2><p>Una misura che sulla planimetria sembra sufficiente può diventare stretta nell’uso quotidiano. Conviene verificare il tavolo alla dimensione reale, la profondità delle sedute e le aperture degli elementi cucina più vicini, soprattutto in open space e ambienti compatti.</p>',
    '<h2>Cosa significa in pratica</h2><p>Una misura che sulla planimetria sembra sufficiente può diventare stretta nell’uso quotidiano. Conviene verificare il tavolo alla dimensione reale, la profondità delle sedute e le aperture degli elementi cucina più vicini, soprattutto in open space e ambienti compatti.</p><h2>Quanto spazio lasciare dietro una sedia?</h2><p>Non esiste una quota unica valida in ogni situazione: cambia se dietro la persona seduta c’è una parete, un semplice passaggio oppure il percorso principale della cucina. Il controllo corretto somma tavolo, sedia occupata e spazio necessario a chi deve passare, verificando anche le aperture della cucina più vicine.</p>'
)

print("Search Everywhere: penisola, tavolo e sedute rafforzati.")
