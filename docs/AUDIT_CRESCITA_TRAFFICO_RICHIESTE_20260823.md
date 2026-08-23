# Sistema 90G — Audit crescita traffico e richieste

Data: 2026-08-23
Branch: `strategy/free-entry-organic-20260823`

## Obiettivo

Aumentare contemporaneamente:

1. visite **qualificate** da persone che stanno progettando, acquistando, verificando o modificando una cucina;
2. richieste di **valutazione iniziale gratuita**;
3. conversione delle richieste pertinenti nei tre servizi canonici: Consulenza 90G, Verifica 90G, Progetto Cucina 90G.

L'audit non misura il successo dal numero di pagine pubblicate o dal traffico generico. Ogni intervento deve essere giudicato sul percorso:

`problema reale → pagina utile → fiducia/prova → valutazione gratuita → eventuale servizio`

## Vincoli

- niente campagne pubblicitarie;
- niente spam o pubblicazione seriale di link;
- mantenere chiaro il confine tra valore gratuito e servizio professionale;
- non inventare volumi di ricerca o dati Search Console non disponibili;
- non creare pagine solo per occupare una parola chiave;
- conservare gli URL storici utili quando hanno valore SEO, ma riallinearne contenuto e percorso commerciale;
- non costruire cluster editoriali che abbiano l'effetto principale di promuovere marchi terzi;
- i marchi possono essere citati solo quando necessari per un caso concreto o una verifica specifica, in modo neutrale e subordinato al problema dell'utente.

---

# P0 — Coerenza tecnica e indicizzazione

## 1. Free Entry come ingresso canonico

Ingresso canonico:

`/analisi-preventiva.html#richiedi`

La valutazione iniziale deve precedere qualunque acquisto. Sono stati riallineati pagine principali, casi reali, guide ad alta intenzione, professionisti, rivenditori e landing storiche.

Residui già corretti:

- `_redirects`: `/richiesta.html` puntava a `#percorso`;
- `.htaccess`: stesso residuo;
- `navigation-conversion.js`: catalogo/prezzi legacy e fallback `#percorso`;
- `chi-e-sistema90g.html`: CTA finale legacy;
- `metodo-sistema90g.html`: CTA finale legacy;
- test automatici che proteggevano il catalogo precedente.

## 2. Sitemap e segnali di aggiornamento

Le pagine realmente modificate nel ramo devono avere `lastmod` coerente con l'aggiornamento del 23 agosto 2026. Non aggiornare artificialmente le pagine non modificate.

## 3. URL con `.html` e URL senza estensione

Le canonical dichiarate nelle pagine esaminate usano URL `.html`. I risultati pubblici mostrano anche varianti senza `.html`.

Prima di introdurre redirect globali è necessario verificare il comportamento reale di Cloudflare in produzione, per evitare loop o redirect incompatibili. Obiettivo finale: una sola URL indicizzabile per contenuto, canonical coerente e nessun segnale contraddittorio.

## 4. Quality gate

Il ramo non va integrato o pubblicato fino all'esecuzione reale del quality gate completo. Le verifiche statiche e i contratti automatici sono stati riallineati, ma il workflow deve ancora essere eseguito nel contesto GitHub/CI disponibile.

---

# P1 — Conversione delle pagine ad alta intenzione

## Principio

La CTA non deve essere identica ovunque. Deve nascere dal problema della pagina.

Esempi:

- preventivo → `Sottoponi gratuitamente il preventivo`;
- isola/passaggi → `Sottoponi gratuitamente il progetto`;
- elettrodomestico → invio di progetto, modello e scheda tecnica;
- materiali/finiture → CTA più discreta;
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
- Chi sono;
- hub progettazione;
- hub elettrodomestici/impianti;
- hub materiali/finiture;
- hub preventivo/acquisto;
- varie guide tecniche che erano content island.

---

# P1 — Matrice opportunità SEO brand-neutral

La matrice ordina le opportunità in base a **intenzione commerciale**, **pertinenza Sistema 90G**, **copertura già esistente** e **capacità di generare una valutazione gratuita**. Non rappresenta volumi di ricerca.

| Cluster/problema | Intento | Copertura attuale | Azione | Priorità |
|---|---|---|---|---|
| progetto cucina prima dell'ordine | molto alto | forte | consolidare internal linking + Free Entry | P1 |
| progetto creato con planner online | molto alto | nuovo | pagina neutrale + collegamenti a misure/aperture/rilievo | P1 |
| preventivo cucina / confronto preventivi | molto alto | forte | consolidare cluster + casi reali | P1 |
| misure, passaggi, aperture | alto | forte | collegare guide ↔ casi ↔ valutazione | P1 |
| isola / penisola / open space | alto | forte | rafforzare casi e CTA contestuali | P1 |
| rilievo misure / prima di firmare | molto alto | presente | collegamento forte alla valutazione | P1 |
| elettrodomestici da incasso / compatibilità | alto | forte | ampliare solo su problemi reali | P1 |
| elettrodomestici acquistati separatamente | alto | presente | rafforzare compatibilità, responsabilità e montaggio | P1 |
| montaggio / posa / allacciamenti | alto quando nasce un problema | presente | audit conversione e collegamenti | P1 |
| progetto modificato dopo il rilievo | molto alto | parziale | valutare pagina/FAQ dedicata se supportata da casi reali | P1 |
| differenza tra progetto digitale e ambiente reale | alto | nuovo/parziale | presidiare senza citare marchi | P1 |
| top / materiali / finiture | medio-alto | forte | CTA discreta + Consulenza 90G | P2 |
| cucina esistente / restyling | medio-alto | presente | consolidare Consulenza vs Progetto | P2 |
| query di sola ispirazione estetica | medio-basso | presente | non inseguire traffico generico | P3 |

---

# Regola brand-neutral

La ricerca operativa può continuare a intercettare richieste contenenti nomi di marchi, perché il problema dell'utente può essere pertinente a Sistema 90G.

Il sito pubblico segue però una logica diversa:

`problema dell'utente → criterio indipendente → eventuale valutazione gratuita`

Non:

`marchio → cluster di pagine sul marchio → traffico`

Esempi di contenuti ammessi:

- controllare un progetto cucina creato con un planner online;
- verificare un progetto prima dell'ordine;
- capire se un elettrodomestico acquistato separatamente è compatibile con il progetto;
- capire cosa cambia quando il progetto viene modificato dopo il rilievo;
- distinguere misure nominali, misure reali e ingombri di apertura;
- verificare una cucina modulare rispetto a pareti, passaggi e vincoli reali.

I nomi commerciali possono comparire solo quando indispensabili per un caso specifico e senza trasformare il sito in una fonte promozionale del produttore.

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

# Ordine operativo aggiornato

1. chiudere residui P0 e quality gate;
2. completare bonifica content island e legacy CTA;
3. rafforzare internal linking dei cluster esistenti;
4. sviluppare solo gap brand-neutral ad alta intenzione;
5. pubblicare il ramo Free Entry solo dopo gate verde;
6. verificare canonical/redirect e indicizzazione reale post-deploy;
7. richiedere/accelerare nuova scansione delle pagine prioritarie attraverso gli strumenti Google disponibili;
8. misurare richieste per landing e non solo traffico totale;
9. espandere i contenuti solo sulla base di query e problemi reali osservati.
