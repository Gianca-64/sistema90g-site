# Audit sito Sistema 90G — Parte 2 (13 luglio 2026)

Segue `AUDIT_SITO_SISTEMA90G_2026-07-13.md`, dopo le prime correzioni (link portale, email/tagline, "Progetto da zero", pagina Metodo). Copre i 6 punti richiesti: link Metodo in home (fatto), linee guida Google per la ricerca AI, testi, immagini, struttura/navigazione, chiarezza di posizionamento.

## 1. Linee guida Google per la ricerca con AI

Il 15 maggio 2026 Google ha pubblicato la sua prima guida ufficiale ("Optimising your website for generative AI features on Google Search", Google Search Central). I punti chiave:

- **Non serve una strategia separata.** Le pagine che funzionano su AI Overviews e AI Mode sono le stesse che funzionano nella ricerca classica: niente "AEO"/"GEO" come discipline a parte.
- **Nessun file o markup speciale.** Non servono `llms.txt`, markup dedicato all'AI, né la suddivisione dei contenuti in blocchi piccoli "per l'AI". I dati strutturati (schema.org) restano utili per i rich results classici, ma non sono richiesti per comparire nelle funzioni AI.
- **Contenuto "non-commodity".** Google privilegia contenuti con punto di vista ed esperienza diretta, non liste generiche. I casi analizzati di Sistema 90G (episodi reali con misure e conseguenze concrete) sono esattamente il tipo di contenuto che Google definisce di valore, molto meglio di un articolo generico "10 consigli per la cucina".
- **E-E-A-T (Esperienza, Competenza, Autorevolezza, Fiducia)**: la Fiducia è il fattore più importante secondo Google. Qui il sito ha un punto debole reale, vedi punto 3.

In sintesi: il sito non ha bisogno di modifiche tecniche per "piacere all'AI" — deve semplicemente essere chiaro, ben strutturato e credibile, cosa che vale comunque per i visitatori umani.

Fonti: [Google Search Central – AI features and your website](https://developers.google.com/search/docs/appearance/ai-features), [Google Search Central – Optimising for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [Search Engine Journal](https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/).

## 2. Testi: coerenza col Metodo

Oltre a quanto già corretto (email, tagline, Progetto da zero, pagina Metodo), un punto emerge chiaro rileggendo `chi-e-sistema90g.html`: il testo descrive bene l'indipendenza e il metodo, ma **non indica mai una qualifica, un percorso o un'esperienza specifica** di Gian Carlo Primo (quanti anni, che formazione, che tipo di casi ha già seguito). Per l'E-E-A-T di Google — e per la fiducia di un visitatore che sta per pagare un controllo prima di firmare un contratto — questo è il punto più debole del sito. Non ho aggiunto nulla io: sono informazioni che solo tu puoi fornire, e vanno scritte con attenzione.

Le altre pagine controllate (professionisti.html, agenzie-immobiliari.html, analisi-preventiva.html) restano coerenti nel linguaggio diagnostico.

## 3. Immagini: corrispondenza con il contesto

Ho aperto un campione di immagini per verificarle davvero, non solo per nome file. Due risultati opposti:

**Buone, da tenere come riferimento di stile**: l'hero della home (`01_HOME_HERO.png`) e l'immagine finale di "Chi sono" (`12_CHI_SONO_CASO.png`) sono annotate con misure reali e callout diagnostici ("percorsi da verificare", "passaggio effettivo 62 cm") — coerentissime con il Metodo, ed è lo stile che identifica il sito.

**Un problema serio**: l'immagine hero di `chi-e-sistema90g.html` (`09_CHI_SONO_HERO.png`) non è una foto di Gian Carlo, ma un'illustrazione generica in stile fotorealistico di un uomo non identificato, con testo integrato nell'immagine stessa ("CHI SONO", "ANALISI, ESPERIENZA E SGUARDO INDIPENDENTE", "Mi occupo di progettazione d'interni...") che è scollegato dal vero testo della pagina e usa ancora la parola "progettazione". Proprio sulla pagina che dovrebbe costruire fiducia personale, il visitatore vede un'immagine generica al posto di una persona reale — è l'opposto di quello che serve per l'E-E-A-T di cui al punto 1. Consiglio di sostituirla con una foto reale (anche semplice) o con un'immagine nello stesso stile diagnostico-annotato delle altre pagine, senza volti generici né testo integrato.

**Un problema minore**: l'immagine del caso "Lavastoviglie aperta e passaggio bloccato" (`images/final/case-01-dishwasher.jpg`) mostra un'isola cucina con uno sportello generico aperto, non un'apertura di lavastoviglie chiaramente riconoscibile — il collegamento visivo col titolo del caso è debole.

Non ho aperto le altre ~95 immagini una per una: se vuoi, posso fare un secondo giro mirato solo sulle immagini dei 25 casi pubblicati.

## 4. Struttura e navigabilità

Il menu principale ha 6 voci (Chi sono, Cosa faccio, I servizi, I casi analizzati, Per agenzie, Contatti) e ora anche il link al Metodo dalla home. Ma il sito ha **due pagine importanti e ben scritte che non sono raggiungibili da nessun menu**:

- `professionisti.html` ("Collaborazioni professionali") — pensata per un pubblico diverso (professionisti del settore), zero link in entrata da nessuna pagina.
- Le 4 pagine orfane già segnalate nella Parte 1 (`caso-open-space.html`, `caso-passaggio-lavastoviglie.html`, `caso-verificato-isola-forno-passaggi.html`, `centro-casi-reali.html`).

Se "professionisti.html" è un pubblico che vuoi davvero servire, andrebbe aggiunta almeno una voce di menu o un link da "Per agenzie"/Contatti. Altrimenti nessuno lo trova, nemmeno Google (non essendo linkata da nessuna parte, viene scoperta solo se è nella sitemap).

Resta inoltre aperto il punto della Parte 1: due sistemi grafici diversi convivono (37 pagine nuove, il resto vecchie).

## 5. Chiarezza: cosa facciamo, perché, chi siamo, con cosa, per chi

Verificando home, Chi sono, Cosa faccio e Servizi insieme:

- **Cosa facciamo**: chiaro. Analisi preventiva indipendente di planimetrie, progetti, preventivi prima di ordinare o firmare.
- **Perché**: chiaro. Evitare costi tardivi, conflitti d'uso e compromessi scoperti solo dopo l'acquisto/i lavori.
- **Chi siamo**: parzialmente chiaro — c'è un nome e una dichiarazione di indipendenza, ma non l'esperienza/qualifica (vedi punto 2) e l'immagine sbagliata (vedi punto 3).
- **Con quali strumenti**: qui il sito è debole. Non si menziona mai, in nessuna pagina pubblica, che dietro c'è un motore diagnostico a regole con una biblioteca di conoscenza tracciata (ora lo fa solo la nuova pagina Metodo, che però non era linkata fino a oggi). Il visitatore medio non sa se dietro c'è "solo esperienza personale" o anche un sistema strutturato — la seconda cosa è un punto di forza che oggi non emerge quasi da nessuna parte tranne la pagina Metodo appena riscritta.
- **A chi ci rivolgiamo**: il sito parla principalmente a privati che stanno per firmare o ordinare qualcosa. Esistono anche pagine per agenzie immobiliari e per professionisti, ma quest'ultima non è collegata (punto 4), quindi di fatto il sito comunica un solo pubblico principale.

## 6. Priorità consigliate

1. Foto/immagine reale su "Chi sono" — il problema di fiducia più visibile.
2. Aggiungere qualifica/esperienza reale nel testo di "Chi sono" — serve il tuo contributo.
3. Decidere se linkare `professionisti.html` da qualche parte o toglierlo dal sito.
4. Valutare se e come comunicare più esplicitamente il "motore a regole" come strumento, non solo come pagina isolata.
5. Restanti punti della Parte 1 (pagine orfane, doppio sistema grafico, casi mancanti per alcuni ambienti).
