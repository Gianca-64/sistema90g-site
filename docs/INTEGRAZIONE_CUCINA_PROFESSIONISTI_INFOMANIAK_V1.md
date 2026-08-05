# Integrazione sito cucina, professionisti e Infomaniak — v1

Data: 5 agosto 2026
Stato: integrazione tecnica, pacchetti e contratto di collaudo completati nei rami separati; rilascio non autorizzato

## Obiettivo

Consolidare senza cambiare priorità:

- sito pubblico focalizzato sulla cucina;
- portale e backend come fonte autorevole di servizi, prezzi e Privacy;
- Console privata come destinazione delle richieste cucina;
- percorso professionale secondario conservato come archivio Marketing;
- nessuna conversione automatica di un interesse professionale in caso.

## Regole vincolanti

1. La home e la navigazione restano focalizzate sulla cucina.
2. Il percorso professionale resta secondario, separato dalle richieste cucina e non indicizzato fino all’approvazione finale.
3. Una manifestazione d’interesse professionale non crea clienti, richieste di servizio o casi.
4. Il passaggio da interesse professionale a caso richiede una richiesta concreta e una decisione umana esplicita nella Console.
5. Il backend resta la fonte autorevole per catalogo, prezzi, tempi, versioni Privacy e idempotenza.
6. Sito e browser inviano soltanto identificativi e dati dichiarati dall’utente; non sono fonte autorevole per prezzo o perimetro.
7. La Console online resta privata e in modalità fail-closed quando `APP_PASSWORD` non è configurata.
8. Nessun merge, migrazione o deploy senza verifica integrata e approvazione esplicita.

## Stato dei blocchi

### 1. Contratto cucina — completato nel ramo

- catalogo canonico `S90G-K01`, `K02`, `K03`, `K11`, `K12`, `K21`;
- versione catalogo `2026.08.05-v1`;
- snapshot servizio trasferito dal backend alla Console;
- codice database K21 allineato a `analisi-progetto-cucina-rivenditore`;
- compatibilità mantenuta con gli alias precedenti;
- nuova richiesta HTTP 201 e replay idempotente HTTP 200.

### 2. Portale cucina — completato nel ramo

- posizionamento cucina e dichiarazione di indipendenza;
- configurazione e catalogo letti dal backend;
- gestione di ruolo, servizio e quantità mancanti o non validi;
- rimozione dall’URL dei dati non autorevoli su prezzo, titolo e tempi;
- versione Privacy accettata conservata e inclusa nel fingerprint.

### 3. Percorso professionale secondario — predisposto ma inattivo

- endpoint e archivio dedicati, separati dalle richieste cucina;
- nuova manifestazione HTTP 201 e replay HTTP 200;
- versione Privacy mostrata obbligatoria e verificata dal backend;
- modulo sito con `data-active="false"` e senza endpoint;
- `noindex,nofollow,noarchive` nell’HTML e in `X-Robots-Tag`;
- sitemap dedicata vuota e non richiamata da `robots.txt`;
- informativa dedicata ancora dichiarata come bozza non pubblicabile;
- nessun collegamento pubblico dalla pagina professionisti.

### 4. Console — completato nel ramo

- importazione del contratto canonico e dello snapshot servizio;
- archivio `Interessi professionali` distinto dai casi;
- origine, consensi, stato, prossima azione e cronologia conservati;
- conversione in caso consentita soltanto dopo lo stato `Richiesta concreta ricevuta` e comando umano esplicito;
- nessuna creazione automatica di casi durante l’importazione;
- build Next.js standalone per Infomaniak verificata;
- pacchetto privo di database operativi, import CSV, seed desktop e configurazioni private;
- vecchio intake `/richiesta` e `/api/public-request` archiviato con HTTP 410;
- portali cliente con token non pubblici per impostazione predefinita;
- eventuale apertura dei portali cliente subordinata al flag esplicito `S90G_PUBLIC_CLIENT_PORTAL=1`;
- route canoniche usate anche nel profilo online;
- adattatori `*-online` storici disponibili soltanto con `S90G_LEGACY_ONLINE_ADAPTERS=1`;
- persistenza online di collaudo definita come SQLite in `S90G_DATA_DIR` esterna alla release;
- smoke test standalone superato con Basic Auth, SQLite vuoto e un solo processo.

### 5. Pacchetti di collaudo — completati nei rami

#### Backend

- workflow manuale vincolato al ramo integrato;
- lint e test prima del confezionamento;
- manifesto SHA-256 generato sul contenuto effettivo;
- esclusione di `.env`, configurazioni private e workflow;
- nessun accesso a Infomaniak e nessun deploy.

#### Sito

- pacchetto statico cucina verificabile;
- percorso professionale non approvato escluso integralmente;
- manifesto SHA-256 generato e verificato;
- artefatto disponibile soltanto con avvio manuale e conferma esplicita;
- nessun deploy automatico.

#### Console

- build standalone con `S90G_INFOMANIAK_BUILD=1`;
- modelli, regole e schemi statici versionati ammessi;
- dati operativi, casi, CSV, database e segreti esclusi;
- manifesto e archivio verificati;
- runtime provato con SQLite sintetico esterno al pacchetto;
- artefatto disponibile soltanto con avvio manuale e conferma esplicita;
- nessun deploy automatico.

### 6. Contratto di collaudo isolato — completato

Documento operativo:

`docs/CONTRATTO_COLLAUDO_INFOMANIAK_ISOLATO_V1.md`

Definisce:

- separazione di sito, backend, MariaDB, Console e SQLite;
- requisiti Node.js e avvio standalone;
- variabili private e confini pubblici;
- dati sintetici ammessi;
- sequenza sito → backend → Console → ACK;
- backup, integrità, pulizia e rollback;
- condizioni di arresto;
- tre Gate di autorizzazione distinti.

Checklist preliminare:

`docs/GATE1_VERIFICA_CAPACITA_INFOMANIAK_V1.md`

Il Gate 1 verifica soltanto le capacità del prodotto Infomaniak e non autorizza la creazione di risorse.

## Verifiche automatiche correnti

### Backend

- `Integration contract`: superato;
- `Verifica backend`: superato;
- lint PHP, test, MariaDB, HTTP end-to-end e confezionamento CI: superati.

### Sito

- `Audit kitchen focus`: superato;
- `E2E kitchen focus`: superato;
- `Verifica interesse professionale`: superato;
- `Prepara rilascio sito Infomaniak`: superato;
- `Verifica contratto collaudo Infomaniak`: aggiunto;
- desktop, mobile e accessibilità inclusi.

### Console

- `Verifica contratto cucina`: superato;
- `Verifica interessi professionali`: superato;
- `Prepara Console standalone Infomaniak`: superato;
- `Verifica confine Console privata`: superato;
- smoke test standalone con SQLite isolato: superato;
- build completa e standalone incluse.

## Blocchi ancora necessari prima di qualsiasi rilascio

1. eseguire il Gate 1 senza creare risorse, verificando il prodotto Infomaniak disponibile;
2. approvare il testo definitivo dell’informativa Privacy professionisti;
3. decidere se e quando rendere attivo il percorso professionale secondario;
4. ottenere autorizzazione esplicita alla creazione dell’ambiente vuoto di collaudo;
5. predisporre l’ambiente Infomaniak senza dati reali;
6. applicare le migrazioni soltanto dopo il Gate 2;
7. collaudare sul runtime reale:
   `sito → portale → backend → Console → ACK`;
8. verificare autenticazione, backup, rollback, log e persistenza della Console privata;
9. sottoporre esito e piano di rollback all’approvazione esplicita;
10. solo dopo il Gate 3: merge coordinato e rilascio Infomaniak.

## Stato di pubblicazione

- PR sito #23: aperta, bozza, non unita;
- PR backend #6: aperta, bozza, non unita;
- PR Console #20: aperta, bozza, non unita;
- nessun artefatto manuale di rilascio avviato;
- nessuna risorsa di collaudo creata;
- nessun deploy o migrazione remota eseguiti;
- percorso professionale non attivo e non indicizzato;
- Console online non attivata.

## Prossimo macro-blocco del programma

Eseguire il **Gate 1 — verifica delle capacità Infomaniak**, senza salvare modifiche nel Manager e senza creare risorse.

L’esito deve confermare o sospendere:

- disponibilità del sito Node.js;
- versione Node compatibile;
- comando `node server.js` e variabile `PORT`;
- sottodominio separato e HTTPS;
- directory persistente privata;
- singolo processo applicativo;
- backend PHP e MariaDB isolabili;
- backup file e database.

Solo dopo il rapporto Gate 1 potrà essere richiesta l’autorizzazione alla creazione dell’ambiente vuoto.
