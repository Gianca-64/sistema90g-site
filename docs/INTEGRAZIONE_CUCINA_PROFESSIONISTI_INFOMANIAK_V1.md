# Integrazione sito cucina, professionisti e Infomaniak — v1

Data: 5 agosto 2026
Stato: integrazione tecnica e pacchetti di collaudo completati nei rami separati; rilascio non autorizzato

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
- eventuale apertura dei portali cliente subordinata al flag esplicito `S90G_PUBLIC_CLIENT_PORTAL=1`.

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
- artefatto disponibile soltanto con avvio manuale e conferma esplicita;
- nessun deploy automatico.

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
- desktop, mobile e accessibilità inclusi.

### Console

- `Verifica contratto cucina`: superato;
- `Verifica interessi professionali`: superato;
- `Prepara Console standalone Infomaniak`: superato;
- `Verifica confine Console privata`: superato;
- build completa e standalone incluse.

## Blocchi ancora necessari prima di qualsiasi rilascio

1. approvare il testo definitivo dell’informativa Privacy professionisti;
2. decidere se e quando rendere attivo il percorso professionale secondario;
3. predisporre un ambiente di collaudo Infomaniak senza dati reali;
4. confermare il runtime Node supportato per la Console standalone;
5. definire dominio o sottodominio privato, terminazione HTTPS e gestione delle credenziali Basic Auth;
6. applicare le migrazioni soltanto nell’ambiente di collaudo autorizzato;
7. collaudare sul runtime reale:
   `sito → portale → backend → Console → ACK`;
8. verificare autenticazione, backup, rollback, log e persistenza della Console privata;
9. verificare che i portali cliente restino chiusi, salvo futura autorizzazione specifica;
10. sottoporre esito e piano di rollback all’approvazione esplicita;
11. solo dopo l’approvazione: merge coordinato e rilascio Infomaniak.

## Stato di pubblicazione

- PR sito #23: aperta, bozza, non unita;
- PR backend #6: aperta, bozza, non unita;
- PR Console #20: aperta, bozza, non unita;
- nessun artefatto manuale di rilascio avviato;
- nessun deploy o migrazione remota eseguiti;
- percorso professionale non attivo e non indicizzato;
- Console online non attivata.

## Prossimo macro-blocco del programma

Preparare il **contratto di collaudo dell’ambiente Infomaniak isolato**, con:

- inventario delle configurazioni necessarie;
- requisiti del runtime Node della Console;
- domini, HTTPS e confini pubblici/privati;
- procedura di backup e rollback;
- dati sintetici di prova;
- sequenza di migrazione controllata;
- test HTTP e browser end-to-end;
- verifica importazione e ACK nella Console;
- criteri di accettazione e rapporto finale per l’approvazione;
- nessuna attivazione pubblica.
