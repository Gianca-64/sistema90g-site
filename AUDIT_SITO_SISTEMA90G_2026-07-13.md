# Audit sito Sistema 90G — 13 luglio 2026

Segue l'audit del 11 luglio 2026 (`AUDIT_SITO_SISTEMA90G_2026-07-11.md`). Ho verificato quali punti di quell'audit sono ancora aperti oggi, e ho aggiunto struttura, testi e immagini su tutto il sito (56 pagine HTML). Nessuna modifica è stata applicata: questo è solo il quadro, le correzioni si decidono insieme dopo.

## 1. Stato dei punti aperti dall'audit dell'11 luglio

Tutti ancora presenti, verificati oggi su tutte le pagine:

- **Email obsoleta**: `sistema90g@icloud.com` compare ancora in tutte le 55 pagine che hanno un footer. Zero pagine usano `info@sistema90g.it`.
- **WhatsApp come canale visibile**: il pulsante "Chat WhatsApp" è ancora presente in 22 pagine (soprattutto quelle sul template vecchio, vedi punto 2).
- **Tagline "PROGETTAZIONE · ANALISI PREVENTIVA"**: ancora nell'intestazione di 37 pagine.
- **Privacy Policy con infrastruttura superata**: cita ancora GitHub Pages tra i servizi di hosting.
- **"Progetto da zero" in conflitto con il Metodo**: confermato, vedi punto 3.

Una correzione **fatta oggi, non dall'audit dell'11**: i link del portale pubblico in tutte le pagine ora puntano a `sistema90g.it/richiesta.html` invece che alla console Cloudflare (causavano un popup di login ai visitatori).

## 2. Due sistemi grafici coesistono sullo stesso sito

Ho trovato due "famiglie" di pagine, tecnicamente diverse:

- **Template nuovo** (`sistema90g-visual-2026.css`, classi `s90g-*`): usato in 37 pagine, tra cui home, richiesta, contatti, chi sono, i tre servizi (Controllo mirato, Analisi completa, Progetto da zero) e 19 pagine caso. È il template coerente con l'aspetto attuale del sito.
- **Template vecchio** (`style.css` + `sistema90g-refresh.css` + `sistema90g-final-images.css`, classi `premium-*`/`site-*`): usato in circa 18 pagine, tra cui `metodo-sistema90g.html`, diverse pagine "scena-*", "micro-caso-*", e alcune pagine caso più vecchie. Queste pagine hanno ancora il pulsante WhatsApp fisso, la vecchia intestazione e in alcuni casi link diversi nel menu.

Un visitatore che passa da una pagina nuova a una vecchia (o viceversa, tramite un link interno o un risultato di ricerca) nota un cambio di stile e di menu evidente.

## 3. "Progetto da zero" promette ancora un prodotto di progettazione

Il servizio da €797 si presenta come costruzione di "una nuova proposta" con sezioni "Impostazione", "Priorità", "Proposta" e la frase "una proposta coerente da sviluppare". Anche i dati strutturati (schema.org) lo classificano come `"serviceType": "Progettazione preliminare indipendente di ambienti interni"`.

Per confronto, gli altri due livelli restano diagnostici nel linguaggio: Analisi completa (€347) parla di "una mappa chiara delle criticità e delle decisioni ancora aperte", non di una proposta da realizzare.

Questo è esattamente il punto che l'audit dell'11 luglio segnalava come "decisione commerciale, non correzione testuale": va deciso se questo livello resta un servizio di progettazione (e quindi va gestito con responsabilità professionali diverse) o se va trasformato in una diagnosi/quadro decisionale come gli altri due.

## 4. La pagina "Metodo Sistema90G" non descrive il Metodo attuale

`metodo-sistema90g.html` è interamente dedicata a un solo scenario (lavastoviglie, sgabelli, frigorifero in cucina) e non menziona: i tre livelli di servizio, gli ambienti coperti, la distinzione tra diagnosi e stile, il ruolo dell'AI solo per l'estrazione. È rimasta ferma a una versione precedente e molto più ristretta del progetto, mentre `come-funziona.html` (non ancora controllata in dettaglio) potrebbe già coprire meglio l'architettura reale — da verificare quale delle due pagine il sito intende usare come riferimento del Metodo.

## 5. I casi pubblicati coprono solo una parte degli ambienti

Sui 25 casi pubblicati, la maggioranza riguarda la cucina (isola, lavastoviglie, cucina piccola, profondità 75 cm, preventivo cucina — più i doppioni di cui al punto 6). Compaiono anche bagno, cabina armadio, soggiorno, ingresso, scala/terrazzo. Non compare nessun caso su: camera bambini, studio, lavanderia, ripostiglio/dispensa, balconi/terrazzi, cantina/soffitta, garage, corridoi — ambienti che invece la Biblioteca della console copre già interamente. Se l'obiettivo è mostrare l'ampiezza reale del Metodo, andrebbero aggiunti casi anche in quelle aree.

## 6. Pagine duplicate/orfane rimaste online

Tre pagine caso più vecchie coprono lo stesso tema di pagine più recenti, con contenuto diverso ma stesso argomento, ancora online e ancora collegate tra loro (non più dal menu principale):

- `caso-open-space.html` — sovrapposto a `caso-open-space-percorso-centrale.html` e `caso-open-space-tv-divano-passaggi.html`
- `caso-passaggio-lavastoviglie.html` — sovrapposto a `caso-lavastoviglie-passaggio-cucina.html`
- `caso-verificato-isola-forno-passaggi.html` — sovrapposto a `caso-isola-passaggi-cucina.html`, non più linkato da nessuna pagina (raggiungibile solo con l'URL diretto)

Sono collegate anche da una quarta pagina, `centro-casi-reali.html`, che è un hub di casi separato da quello attuale (`casi-analizzati.html`) e non compare nel menu di navigazione.

Nessuna di queste quattro pagine è nella sitemap, quindi non è proposta attivamente nei motori di ricerca — ma `robots.txt` permette comunque a Google di indicizzarle se le trova tramite i link interni. Sono ancora sul template vecchio (email, WhatsApp, tagline "PROGETTAZIONE" inclusi).

## 7. Immagini: stato buono, nessun problema nuovo trovato

Il lavoro fatto il 4 luglio (`VISUAL-AUDIT-2026-07-04.md`, `IMAGE-AUDIT-FINALE.md`) risulta ancora valido: 15 casi con 15 immagini distinte, 6 hero uniche, nessuna sovrascrittura via JavaScript, nessun ritaglio forzato. Non ho trovato nuove incoerenze nelle immagini oltre a quanto già documentato. Le 4 pagine orfane del punto 6 non sono state incluse in quell'audit (sono precedenti alla mappa "finale").

## 8. Incoerenza da chiarire sull'hosting reale

L'audit dell'11 luglio dichiara che l'hosting è Cloudflare e che GitHub Pages "non appartiene più all'architettura attiva". Il repository contiene però ancora un file `CNAME` (convenzione tipica di GitHub Pages per un dominio personalizzato), e oggi stesso il sito ha effettivamente ripubblicato le pagine dopo un push su GitHub — comportamento coerente con GitHub Pages, non con un deploy Cloudflare manuale. Prima di scrivere nella Privacy Policy quale sia l'infrastruttura reale, vale la pena confermare se il dominio sia servito da GitHub Pages (con Cloudflare eventualmente solo come DNS/proxy) o davvero da Cloudflare Pages/Workers.

## 9. Ordine consigliato, se vuoi procedere

1. Email e tagline "PROGETTAZIONE" — correzione meccanica, stesso tipo di intervento già fatto oggi sui link, a basso rischio.
2. Decidere il destino di "Progetto da zero" (mantenere come servizio di progettazione con responsabilità dedicate, oppure riportarlo a un formato diagnostico) — decisione tua, non tecnica.
3. Decidere quale pagina è il vero riferimento del "Metodo" (`metodo-sistema90g.html` vs `come-funziona.html`) e allinearla.
4. Rimuovere, reindirizzare o aggiornare le 4 pagine orfane del punto 6.
5. Valutare nuovi casi per gli ambienti non ancora rappresentati.
6. Portare le pagine rimaste sul template vecchio al nuovo sistema grafico.
7. Confermare la reale infrastruttura di hosting e aggiornare la Privacy Policy di conseguenza.
