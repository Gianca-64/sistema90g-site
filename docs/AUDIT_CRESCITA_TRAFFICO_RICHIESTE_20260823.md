# Sistema 90G — Audit crescita traffico e richieste

Data: 2026-08-23
Branch: `strategy/free-entry-organic-20260823`

## Obiettivo

Aumentare contemporaneamente:

1. visite **qualificate** da persone che stanno progettando, acquistando, verificando o modificando una cucina;
2. richieste di **valutazione iniziale gratuita**;
3. conversione delle richieste pertinenti nei tre servizi canonici: Consulenza 90G, Verifica 90G, Progetto Cucina 90G.

L'audit non misura il successo dal numero di pagine pubblicate o dal traffico generico. Ogni intervento deve essere giudicato sul percorso:

`query/problema reale → pagina utile → fiducia/prova → valutazione gratuita → eventuale servizio`

## Vincoli

- niente campagne pubblicitarie;
- niente spam o pubblicazione seriale di link;
- mantenere chiaro il confine tra valore gratuito e servizio professionale;
- non inventare volumi di ricerca o dati Search Console non disponibili;
- non creare pagine solo per occupare una parola chiave;
- conservare gli URL storici utili quando hanno valore SEO, ma riallinearne contenuto e percorso commerciale.

---

# P0 — Coerenza tecnica e indicizzazione

## 1. Free Entry come ingresso canonico

Stato: **in corso / quasi completato**.

Ingresso canonico:

`/analisi-preventiva.html#richiedi`

La valutazione iniziale deve precedere qualunque acquisto. Sono stati riallineati pagine principali, casi reali, guide ad alta intenzione, professionisti, rivenditori e landing storiche.

Residui individuati durante l'audit:

- `_redirects`: `/richiesta.html` puntava ancora a `#percorso` → corretto;
- `.htaccess`: stesso residuo → corretto;
- `navigation-conversion.js`: catalogo/prezzi legacy e fallback `#percorso` → corretto;
- `chi-e-sistema90g.html`: CTA finale legacy → corretta;
- `metodo-sistema90g.html`: CTA finale legacy → corretta;
- test automatici che proteggevano il catalogo precedente → riallineati al contratto Free Entry.

## 2. Sitemap e segnali di aggiornamento

Stato: **in corso**.

Le pagine modificate nel ramo Free Entry devono avere `lastmod` coerente con il reale aggiornamento del 23 agosto 2026. Non aggiornare artificialmente le pagine non modificate.

Prima tranche già aggiornata nella sitemap. Al termine dell'audit va eseguita una normalizzazione finale dei `lastmod` per tutte e sole le pagine effettivamente toccate.

## 3. URL con `.html` e URL senza estensione

Stato: **da verificare prima del deploy**.

Le canonical dichiarate nelle pagine esaminate usano URL `.html`. I risultati pubblici mostrano però anche varianti senza `.html`.

Prima di introdurre redirect globali è necessario verificare il comportamento reale di Cloudflare in produzione, per evitare loop o redirect incompatibili con la piattaforma. Obiettivo finale: una sola URL indicizzabile per contenuto, canonical coerente e nessun segnale contraddittorio.

## 4. Quality gate

Stato: **non ancora dichiarato verde**.

Il ramo non va integrato o pubblicato fino all'esecuzione reale del quality gate completo. Le verifiche statiche e i contratti automatici sono stati riallineati, ma il workflow deve ancora essere eseguito nel contesto GitHub/CI disponibile.

---

# P1 — Conversione delle pagine ad alta intenzione

## Principio

La CTA non deve essere identica ovunque. Deve nascere dal problema della pagina.

Esempi:

- preventivo → `Sottoponi gratuitamente il preventivo`;
- isola/passaggi → `Sottoponi gratuitamente il progetto`;
- elettrodomestico → invio di progetto, modello e scheda tecnica;
- materiali/finiture → CTA più discreta, perché la pagina è anche informativa;
- caso reale → `Hai un problema simile?`.

## Pagine già riallineate

- valutazione iniziale;
- contatti;
- professionisti;
- rivenditori;
- casi reali e archivio casi;
- preventivi e confronto preventivi;
- misure/passaggi;
- isola;
- prima di firmare l'ordine;
- elettrodomestici da incasso;
- top/materiali;
- sconto/valore reale;
- voci escluse;
- rilievo misure;
- verifica indipendente;
- rinnovare cucina esistente;
- sostituzione elettrodomestici;
- pagine esempio/prova;
- Metodo 90G;
- Chi sono.

## Da controllare nel giro finale

- hub `progettare-cucina-guide.html`;
- hub elettrodomestici/impianti;
- hub materiali/finiture;
- pagine progettazione create il 18 agosto non ancora toccate dal Free Entry;
- pagine micro-problema del 14 agosto con CTA potenzialmente generiche.

---

# P1 — Matrice iniziale delle opportunità SEO

Questa matrice ordina le opportunità in base a **intenzione commerciale**, **pertinenza Sistema 90G**, **copertura già esistente** e **capacità di generare una valutazione gratuita**. Non rappresenta volumi di ricerca: questi dovranno essere confermati con Search Console o altri dati reali quando disponibili.

| Cluster | Intento | Copertura attuale | Azione | Priorità |
|---|---|---|---|---|
| progetto cucina prima dell'ordine | molto alto | forte | consolidare internal linking + Free Entry | P1 |
| preventivo cucina / confronto preventivi | molto alto | forte | consolidare cluster + casi reali | P1 |
| misure, passaggi, aperture | alto | forte | collegare guide ↔ casi ↔ valutazione | P1 |
| isola / penisola / open space | alto | forte | rafforzare casi e CTA contestuali | P1 |
| rilievo misure / prima di firmare | molto alto | presente | collegamento forte alla valutazione | P1 |
| elettrodomestici da incasso / compatibilità | alto | forte | ampliare solo su problemi reali | P1 |
| IKEA / METOD / planner IKEA | molto alto | assente | creare cluster iniziale utile e non promozionale | P1 |
| ENHET | medio-alto | assente | valutare contenuto comparativo/compatibilità | P1/P2 |
| montaggio / posa / allacciamenti | alto quando nasce un problema | presente | audit conversione e collegamenti | P1 |
| top / materiali / finiture | medio-alto | forte | CTA discreta + Consulenza 90G | P2 |
| cucina esistente / restyling | medio-alto | presente | consolidare Consulenza vs Progetto | P2 |
| query di sola ispirazione estetica | medio-basso | presente | non inseguire traffico generico | P3 |

---

# Primo cluster nuovo consigliato — IKEA / METOD / ENHET

## Perché

Le richieste su IKEA sono pertinenti quando riguardano una decisione reale sulla cucina e possono essere trattate indipendentemente dal marchio. Il sito oggi non presidia in modo specifico questo gruppo di problemi.

## Non creare

Una pagina generica `cucine IKEA` costruita solo per intercettare il marchio.

## Creare progressivamente solo se supportato da problemi reali

1. **Controllare un progetto cucina IKEA prima dell'ordine**
   - planner/progetto già esistente;
   - passaggi e aperture;
   - misure da verificare;
   - cosa deve confermare IKEA/rivenditore/installatore;
   - CTA: valutazione gratuita del caso.

2. **METOD: progetto, misure e compatibilità da controllare**
   - modularità come dato del produttore da non inventare;
   - relazione tra progetto, vano, pareti, aperture ed elettrodomestici;
   - rimando alle fonti IKEA per dati di prodotto variabili.

3. **Planner IKEA: cosa verificare prima di considerare il progetto definitivo**
   - distinzione tra rappresentazione del planner e rilievo reale;
   - interferenze, passaggi, aperture, impianti e fattibilità finale;
   - niente sostituzione del controllo IKEA/installatore.

4. **ENHET o METOD: quale sistema ha senso per il caso reale**
   - solo dopo verifica delle fonti aggiornate;
   - evitare confronti basati su caratteristiche non confermate.

Il cluster deve essere costruito con fonti ufficiali aggiornate per dimensioni, compatibilità e dati di prodotto.

---

# P2 — Autorità e internal linking

La base contenuti è già ampia. La priorità non è aumentare indiscriminatamente il numero di articoli, ma costruire cluster leggibili.

Schema raccomandato:

`hub → guida specifica → caso reale pertinente → valutazione gratuita`

E percorso inverso:

`caso reale → guida che spiega il criterio → valutazione gratuita`

I casi reali sono particolarmente importanti perché trasformano un'affermazione di competenza in una prova concreta del tipo di problema che viene analizzato.

---

# P2 — Distribuzione organica gratuita

Ogni contenuto nuovo deve poter produrre più formati senza diventare spam:

- articolo/guida sul sito;
- risposta contestuale a una domanda reale su Facebook o Reddit, quando le regole lo permettono;
- post proprietario Facebook;
- contenuto professionale LinkedIn se pertinente;
- visual sintetico per Pinterest/Instagram;
- eventuale video breve su un singolo criterio concreto.

La distribuzione non deve partire dal link da promuovere, ma dalla domanda reale a cui rispondere.

---

# Metriche da usare appena disponibili

## Visite qualificate

- landing page organiche;
- query che portano traffico;
- CTR dalle SERP;
- visite ai cluster ad alta intenzione;
- ingressi da social/community pertinenti.

## Conversione

- click verso valutazione gratuita per pagina e CTA;
- valutazioni gratuite avviate;
- valutazioni completate;
- quota di casi pertinenti;
- servizio proposto dopo la valutazione;
- acquisti per servizio;
- ricavo per origine/landing.

## Indicatore guida

Non ottimizzare per `sessioni` isolate. Ottimizzare progressivamente per:

`visite qualificate → valutazioni gratuite → casi pertinenti → clienti`

---

# Ordine operativo

1. chiudere residui P0 e quality gate;
2. pubblicare il ramo Free Entry solo dopo gate verde;
3. verificare canonical/redirect e indicizzazione reale post-deploy;
4. richiedere/accelerare nuova scansione delle pagine prioritarie attraverso gli strumenti Google disponibili;
5. chiudere audit conversione degli hub ancora non riallineati;
6. creare il primo contenuto IKEA ad alta intenzione solo con fonti ufficiali aggiornate;
7. rafforzare internal linking dei cluster esistenti;
8. misurare richieste per landing e non solo traffico totale;
9. espandere i contenuti solo sulla base di query e problemi reali osservati.
