from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str):
    p = ROOT / path
    s = p.read_text()
    if old not in s:
        raise SystemExit(f"ERRORE {path}: blocco atteso non trovato: {old[:90]}")
    p.write_text(s.replace(old, new, 1))
    print(f"OK {path}")

# 1) Altezza pensili
replace_once(
    "altezza-pensili-spazio-top-cucina.html",
    '<p class="s90g-lead">La distanza tra top e pensili va valutata insieme a ergonomia, illuminazione e componenti tecnici.</p>',
    '<p class="s90g-lead">La distanza tra top e pensili va valutata insieme a ergonomia, illuminazione e componenti tecnici.</p><div class="s90g-prose"><h2>In breve: quanto devono essere alti i pensili della cucina?</h2><p>Non esiste una quota unica valida per tutte le cucine. Altezza del top, statura di chi usa la cucina, profondità dei pensili, cappa, prese, schienale e sistemi di apertura devono essere letti insieme. Una quota corretta è quella che mantiene accessibili i ripiani e lascia il piano di lavoro comodo e ben illuminato.</p><h2>Cosa significa in pratica</h2><p>Prima di fissare i pensili conviene verificare la cucina completa in sezione: top finito, eventuale alzatina o schienale, prese, illuminazione sottopensile e ingombri della cappa. Spostare i pensili dopo che impianti e rivestimenti sono stati definiti può creare adattamenti inutili.</p></div>'
)

# 2) Prese e impianti
replace_once(
    "prese-impianti-cucina.html",
    '<p class="s90g-lead">Impianti e progetto devono essere letti insieme prima delle opere definitive.</p>',
    '<p class="s90g-lead">Impianti e progetto devono essere letti insieme prima delle opere definitive.</p><div class="s90g-prose"><h2>In breve: quando vanno definite prese e impianti della cucina?</h2><p>Le predisposizioni dovrebbero essere confermate quando la disposizione della cucina e i modelli principali degli elettrodomestici sono sufficientemente definiti. Disegnare prese, acqua e scarichi senza conoscere basi, colonne, vani tecnici e apparecchi reali aumenta il rischio di interferenze.</p><h2>Cosa significa in pratica</h2><p>Il controllo utile non riguarda soltanto la posizione sulla parete, ma anche ciò che occuperà quello spazio: cassetti, schienali, fianchi, zoccoli, vani di ventilazione, spine e tubazioni. Le quote definitive vanno quindi coordinate con il progetto esecutivo del fornitore e con le schede tecniche dei componenti scelti.</p></div>'
)

# 3) Piano induzione
replace_once(
    "piano-induzione-cucina.html",
    '<p class="s90g-lead">La scelta del piano a induzione va coordinata con impianto elettrico, mobile, piano di lavoro e posizione nella composizione.</p>',
    '<p class="s90g-lead">La scelta del piano a induzione va coordinata con impianto elettrico, mobile, piano di lavoro e posizione nella composizione.</p><div class="s90g-prose"><h2>In breve: cosa controllare prima di scegliere un piano a induzione?</h2><p>Vanno verificati potenza disponibile, alimentazione richiesta dal modello, dimensioni del foro nel top, ventilazione, spazio sotto l’apparecchio e posizione rispetto a bordi, pareti e zone operative. Il dato commerciale in centimetri non basta per stabilire se il piano è compatibile con la cucina.</p><h2>Cosa significa in pratica</h2><p>La scheda tecnica del modello scelto deve essere letta insieme al mobile e al top. Cassetti, forno sottostante, spessori e passaggi d’aria possono cambiare la fattibilità dell’installazione. Anche la posizione sul piano di lavoro incide sulla superficie libera che resta per preparazione e appoggio.</p></div>'
)
replace_once(
    "piano-induzione-cucina.html",
    'Scopri il Seconda Opinione · dubbio preciso →',
    'Seconda Opinione · dubbio preciso →'
)

# 4) Elettrodomestici incasso
replace_once(
    "elettrodomestici-incasso-misure-cucina.html",
    '<p class="s90g-lead">Le dimensioni commerciali non descrivono sempre tutto ciò che serve per integrare correttamente un elettrodomestico nella cucina.</p>',
    '<p class="s90g-lead">Le dimensioni commerciali non descrivono sempre tutto ciò che serve per integrare correttamente un elettrodomestico nella cucina.</p><div class="s90g-prose"><h2>In breve: perché le misure nominali degli elettrodomestici non bastano?</h2><p>Perché la misura commerciale descrive solo una parte dell’ingombro. Per l’incasso contano anche vano richiesto, profondità effettiva, ventilazione, collegamenti, apertura delle porte e quote indicate dal produttore. Due apparecchi dichiarati della stessa misura possono richiedere condizioni di installazione diverse.</p><h2>Cosa significa in pratica</h2><p>Prima dell’ordine è utile associare a ogni elettrodomestico il modello preciso e la relativa scheda tecnica. Questo permette di verificare se mobile, fianchi, zoccolo, pannelli e passaggi tecnici sono compatibili prima che la composizione diventi definitiva.</p></div>'
)

# 5) Cappa
replace_once(
    "cappa-aspirazione-cucina.html",
    '<p class="s90g-lead">La cappa non va scelta solo per estetica o portata dichiarata: il risultato dipende da scarico, ricircolo, posizione e compatibilita con la composizione.</p>',
    '<p class="s90g-lead">La cappa non va scelta solo per estetica o portata dichiarata: il risultato dipende da scarico, ricircolo, posizione e compatibilita con la composizione.</p><div class="s90g-prose"><h2>In breve: come capire se una cappa è adatta alla cucina?</h2><p>Non basta confrontare la portata dichiarata. Occorre verificare se lavora con scarico esterno o ricircolo, quale percorso devono seguire i condotti, dove viene posizionata rispetto al piano cottura e quali vincoli impongono pensili, controsoffitti e predisposizioni. Anche manutenzione e rumore incidono sull’uso reale.</p><h2>Cosa significa in pratica</h2><p>Una cappa efficace dipende dal sistema completo. Curve, lunghezza e sezione del condotto possono ridurre le prestazioni rispetto ai dati di catalogo; nei sistemi filtranti diventano importanti qualità e manutenzione dei filtri. Per questo la scelta va verificata nel progetto reale, non isolatamente.</p></div>'
)

# 6) Lavello sotto finestra
replace_once(
    "lavello-sotto-finestra-cucina.html",
    '<p class="s90g-lead">La posizione può funzionare bene, ma va verificata insieme a quota del piano, davanzale, rubinetto e movimento dell\'infisso.</p>',
    '<p class="s90g-lead">La posizione può funzionare bene, ma va verificata insieme a quota del piano, davanzale, rubinetto e movimento dell\'infisso.</p><div class="s90g-prose"><h2>In breve: si può mettere il lavello sotto una finestra?</h2><p>Sì, ma solo se l’apertura reale dell’infisso resta compatibile con rubinetto, piano di lavoro e davanzale. La verifica deve usare quote finite e il modello di miscelatore previsto: pochi centimetri possono determinare se l’anta si apre completamente oppure no.</p><h2>Cosa significa in pratica</h2><p>Prima dell’ordine conviene controllare la traiettoria dell’anta, l’altezza del rubinetto, eventuali maniglie, la quota del davanzale e lo spazio necessario per pulizia e manutenzione. Se uno di questi dati è ancora indicativo, la compatibilità non può essere considerata definitiva.</p></div>'
)

print("Search Everywhere: primo lotto guide tecniche ampliato e reso più citabile.")
