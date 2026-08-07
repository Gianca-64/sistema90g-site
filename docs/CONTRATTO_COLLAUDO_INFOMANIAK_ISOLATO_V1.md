# Contratto di collaudo Infomaniak isolato — Sistema 90G v1

Data: 5 agosto 2026  
Stato: **documento operativo; nessuna risorsa creata e nessun rilascio autorizzato**

## 1. Scopo

Definire l’ambiente e i criteri necessari per collaudare, senza dati reali e senza attivazione pubblica, il flusso:

```text
sito cucina di collaudo
→ portale/backend PHP di collaudo
→ API protetta
→ Console privata Node.js di collaudo
→ SQLite isolato
→ ACK al backend
```

Il contratto non autorizza:

- creazione di siti, domini o database su Infomaniak;
- caricamento di pacchetti;
- applicazione di migrazioni remote;
- uso di casi, clienti, email o documenti reali;
- collegamento del sito pubblico al percorso professionale;
- merge delle PR di integrazione;
- rilascio in produzione.

## 2. Decisioni architetturali confermate

### 2.1 Sito pubblico

- resta statico e focalizzato sulla cucina;
- invia al portale soltanto identificativi canonici e dati dichiarati dall’utente;
- non è fonte autorevole per prezzi, tempi o perimetro;
- il pacchetto di collaudo esclude integralmente il percorso professionale ancora non approvato.

### 2.2 Portale e backend

- restano applicazione PHP con database MariaDB separato;
- sono la fonte autorevole per catalogo, prezzi, Privacy, idempotenza e stato remoto;
- espongono API pubbliche limitate e API Console autenticate;
- non condividono direttamente il database con la Console.

### 2.3 Console privata

- viene collaudata come applicazione Next.js standalone su un sito Node.js separato;
- resta protetta da Basic Auth e in modalità fail-closed;
- usa le route canoniche della Console;
- usa SQLite come fonte operativa nel collaudo;
- comunica con il backend esclusivamente tramite API HTTPS protetta;
- non usa gli adattatori Supabase storici;
- mantiene un solo processo Node attivo;
- conserva il database e gli allegati in una directory persistente esterna al pacchetto applicativo.

### 2.4 Percorso professionale

- resta secondario e separato dalle richieste cucina;
- nel sito resta disattivato, non collegato e non indicizzato;
- l’endpoint dedicato può essere provato soltanto con chiamate sintetiche di collaudo;
- ogni manifestazione resta un record Marketing;
- nessun record diventa automaticamente richiesta di servizio o caso.

## 3. Prerequisiti bloccanti

Prima di creare l’ambiente occorre verificare nel Manager Infomaniak che il prodotto disponibile consenta un sito Node.js con:

- selezione della versione Node.js;
- directory di esecuzione configurabile;
- comando di avvio configurabile;
- porta fornita tramite variabile `PORT`;
- dominio o sottodominio separato;
- certificato HTTPS;
- log di esecuzione e comandi start, stop e restart;
- directory persistente scrivibile dall’applicazione.

Configurazione Node richiesta dal codice corrente:

```text
Versione Node.js: 22 LTS
Directory di esecuzione: radice del pacchetto Console
Comando di build remoto: nessuno, pacchetto già compilato
Comando di avvio: node server.js
Porta: valore assegnato dal Manager tramite PORT
Hostname applicativo: 0.0.0.0 oppure valore richiesto dal runtime Infomaniak
Processi applicativi: 1
```

Se il prodotto Infomaniak disponibile non offre queste condizioni, il collaudo si interrompe. Non sono ammessi workaround sul sito PHP pubblico, Vercel o nuovi fornitori senza una nuova decisione esplicita.

Fonti ufficiali Infomaniak verificate:

- https://www.infomaniak.com/it/assistenza/faq/2537/creare-un-sito-nodejs-con-infomaniak
- https://www.infomaniak.com/en/support/faq/2535/modify-the-configuration-of-a-nodejs-site
- https://www.infomaniak.com/en/hosting/nodejs-hosting
- https://www.infomaniak.com/en/support/faq/250/backup-andor-restore-data

## 4. Risorse isolate da predisporre solo dopo autorizzazione

I nomi definitivi non vengono stabiliti in questo documento. L’ambiente dovrà comprendere:

| Componente | Risorsa isolata richiesta | Divieto |
|---|---|---|
| Sito | destinazione statica di collaudo non indicizzata | non sostituire il sito pubblico |
| Backend | directory/app PHP di collaudo | non sovrascrivere il backend attivo |
| Database backend | MariaDB vuoto e dedicato | non usare il database operativo |
| Console | sito Node.js privato dedicato | non esporre senza Basic Auth |
| Dati Console | directory persistente vuota | non copiare il SQLite canonico del Mac |
| Token API | token Console esclusivo del collaudo | non riusare token di produzione |
| Log | log separati e cancellabili | non mescolare con log operativi |
| Backup | area privata separata | non collocare backup nella web root |

## 5. Configurazione Console di collaudo

Le variabili devono essere archiviate soltanto nel gestore privato dell’ambiente Infomaniak. Non devono entrare nel repository, negli artefatti o nei rapporti pubblici.

```text
NODE_ENV=production
HOSTNAME=0.0.0.0
PORT=<assegnata da Infomaniak>

APP_USER=<utente collaudo>
APP_PASSWORD=<password forte e univoca>

DATA_BACKEND=sqlite
DATA_WRITE_MODE=sqlite
S90G_DATA_DIR=<directory assoluta privata e persistente>

S90G_PUBLIC_CLIENT_PORTAL=0
S90G_LEGACY_ONLINE_ADAPTERS=0

PORTAL_API_BASE_URL=<URL HTTPS backend collaudo>
PORTAL_API_TOKEN=<token esclusivo collaudo>
PORTAL_CONSOLE_ID=console-infomaniak-collaudo
PORTAL_API_TIMEOUT_MS=15000
PORTAL_FILE_MAX_BYTES=26214400
```

Devono restare assenti:

```text
S90G_DESKTOP
S90G_DESKTOP_BUILD
S90G_LOCAL_CONSOLE
SUPABASE_PROJECT_URL
SUPABASE_URL
SUPABASE_SECRET_KEY
```

Le variabili pubbliche Supabase eventualmente incorporate come placeholder durante la compilazione non autorizzano né attivano l’uso di Supabase. Le route canoniche devono rispondere con fonte `sqlite`.

## 6. Persistenza SQLite della Console

### 6.1 Directory

`S90G_DATA_DIR` deve:

- essere assoluta;
- essere esterna alla directory del pacchetto e delle release;
- essere privata e non servita dal web server;
- appartenere all’utente che esegue Node.js;
- essere scrivibile soltanto dal processo autorizzato;
- sopravvivere a restart e sostituzione della release.

Il database atteso è:

```text
<S90G_DATA_DIR>/90g.sqlite
```

Le aree file vengono create sotto la stessa radice, tra cui:

```text
backups/
case-images/
client-deliveries/
client-invoices/
client-materials/
preliminary-uploads/
projects/
```

### 6.2 Concorrenza

Il database usa SQLite in modalità WAL. Nel collaudo è ammesso un solo processo Node e una sola Console operativa. Non sono ammessi bilanciamento orizzontale, repliche attive o due istanze che scrivono sullo stesso file.

### 6.3 Backup

Il codice dispone di backup SQLite coerente tramite API `db.backup`, seguito da `PRAGMA integrity_check`. Il collaudo deve verificare:

1. creazione del backup nella directory privata `backups/`;
2. esito `ok` dell’integrità;
3. presenza del file con dimensione maggiore di zero;
4. capacità di aprire la copia in sola lettura;
5. conservazione massima prevista di 30 backup applicativi;
6. disponibilità anche del meccanismo di ripristino Infomaniak previsto per i file del sito o dell’hosting.

Il ripristino non viene provato sui dati operativi: si usa soltanto il database sintetico di collaudo.

## 7. Configurazione backend di collaudo

Il backend deve usare un database MariaDB vuoto e credenziali dedicate. Configurazione minima:

```text
PORTAL_APP_ENV=staging
PORTAL_REQUIRE_HTTPS=1
PORTAL_ALLOW_HTTP_LOCAL=0

DB_HOST=<host collaudo>
DB_PORT=3306
DB_DATABASE=<database collaudo>
DB_USERNAME=<utente collaudo>
DB_PASSWORD=<password collaudo>

PORTAL_CURSOR_SECRET=<segreto collaudo>
PORTAL_LOG_HASH_SALT=<segreto collaudo>
PORTAL_PRIVACY_VERSION=<versione approvata per il test>
PORTAL_PUBLIC_INTAKE_RATE_LIMIT_PER_MINUTE=20
PORTAL_PUBLIC_INTAKE_IDEMPOTENCY_TTL_HOURS=720
```

Il token della Console deve:

- appartenere soltanto a `console-infomaniak-collaudo`;
- essere salvato nel backend soltanto come hash SHA-256;
- essere trasmesso alla Console tramite configurazione privata;
- essere revocato alla chiusura del collaudo.

## 8. Migrazioni di collaudo

Prima dell’applicazione si esegue il backup del database MariaDB vuoto o di base. Le migrazioni ammesse sono soltanto quelle già verificate nel ramo:

```text
003_console_api_shared_hosting_v1.sql
004_public_intake_v1.sql
005_professional_interests_v1.sql
```

Sequenza:

1. verificare tabella delle migrazioni;
2. applicare soltanto le versioni mancanti;
3. verificare tabelle, indici e vincoli;
4. registrare hash dei file SQL applicati;
5. non eseguire SQL manuale non versionato;
6. non applicare migrazioni al database operativo.

## 9. Dati sintetici obbligatori

Tutti i record devono essere riconoscibili e cancellabili.

Formato raccomandato:

```text
Nome: COLLAUDO SISTEMA90G
Email: collaudo+<timestamp>@example.test
Titolo: [COLLAUDO] verifica cucina sintetica
Organizzazione: ORGANIZZAZIONE COLLAUDO
Testo: nessun riferimento a persone, immobili o pratiche reali
```

Allegati ammessi:

- file artificiali creati per il test;
- nessuna foto reale;
- nessun progetto, preventivo, documento fiscale o dato personale reale.

## 10. Sequenza di collaudo

### Fase A — infrastruttura, senza scritture funzionali

1. verificare HTTPS dei tre componenti;
2. verificare che la Console senza credenziali risponda HTTP 401;
3. verificare che credenziali errate rispondano HTTP 401;
4. verificare che `/richiesta` e `/api/public-request` rispondano HTTP 410;
5. verificare che i portali cliente restino protetti;
6. verificare che il percorso professionale non sia presente nel pacchetto sito;
7. verificare che il backend risponda a `GET /api/public/v1/config` con HTTP 200;
8. verificare log e assenza di errori di avvio.

### Fase B — inizializzazione Console

1. avviare una sola istanza Node;
2. accedere con Basic Auth;
3. verificare `source=sqlite` nelle route che espongono la fonte;
4. verificare la creazione di `90g.sqlite` nella directory persistente;
5. eseguire `PRAGMA integrity_check`;
6. riavviare l’applicazione;
7. verificare che database e stato persistano;
8. creare e verificare un backup applicativo.

### Fase C — richiesta cucina end-to-end

1. aprire il sito di collaudo;
2. scegliere uno dei servizi canonici cucina;
3. verificare che l’URL invii soltanto i parametri ammessi;
4. inviare la richiesta sintetica;
5. verificare HTTP 201;
6. ripetere lo stesso invio con la stessa chiave;
7. verificare HTTP 200 e stessi `requestId` e `requestCode`;
8. inviare contenuto diverso con la stessa chiave;
9. verificare HTTP 409;
10. importare la richiesta nella Console;
11. verificare `serviceId`, `serviceCode`, snapshot, importo, valuta e quantità;
12. verificare che non esista un duplicato locale;
13. inviare ACK;
14. verificare che il backend non riproponga la stessa versione alla medesima Console.

### Fase D — interesse professionale separato

La pagina pubblica resta inattiva. Il test avviene chiamando direttamente l’endpoint di collaudo:

1. inviare una manifestazione sintetica con Privacy corrente;
2. verificare HTTP 201;
3. ripetere con stessa chiave e corpo;
4. verificare HTTP 200 e stesso `remoteId`;
5. usare stessa chiave con corpo differente;
6. verificare HTTP 409;
7. importare nella sezione Marketing della Console;
8. verificare che nessun record venga creato in `cases` o nelle richieste backend;
9. verificare ACK;
10. verificare che la conversione in caso resti impossibile senza stato `Richiesta concreta ricevuta` e comando umano.

### Fase E — pulizia

1. esportare il rapporto degli ID sintetici;
2. eliminare tutti i record sintetici dal backend di collaudo;
3. eliminare il SQLite di collaudo e i relativi backup, dopo il rapporto;
4. revocare il token API di collaudo;
5. rimuovere o disabilitare credenziali e sito Node di collaudo secondo la decisione finale;
6. verificare assenza di residui nei log, salvo quelli tecnici necessari al rapporto.

## 11. Criteri di accettazione

Il collaudo è superato soltanto quando tutti i punti seguenti sono veri:

- nessun dato reale è stato usato;
- sito, backend e Console sono isolati dai componenti operativi;
- Console protetta e fail-closed;
- un solo processo Node;
- SQLite persistente esterno alla release;
- backup SQLite integro;
- route canoniche con fonte SQLite;
- adattatori Supabase legacy spenti;
- richiesta cucina 201/200/409 corretta;
- importazione e ACK senza duplicati;
- interesse professionale separato e senza creazione automatica di casi;
- percorso professionale pubblico ancora inattivo;
- riavvio senza perdita di dati sintetici;
- rollback documentato e provabile;
- pulizia finale completata;
- rapporto firmato con hash delle release e dei file di migrazione.

## 12. Condizioni di arresto immediato

Il collaudo si interrompe senza procedere oltre quando:

- il piano non supporta il sito Node.js richiesto;
- il runtime non permette un solo processo controllato;
- la directory dati non è persistente o privata;
- la Console parte senza Basic Auth;
- una route usa Supabase nonostante la configurazione SQLite;
- un componente punta a database, token o URL operativi;
- il pacchetto contiene `.env`, database, CSV, casi o allegati reali;
- una manifestazione professionale crea automaticamente un caso;
- un test modifica il sito o il backend pubblico;
- backup o integrità non sono verificabili.

## 13. Rollback

### Console

1. arrestare il processo Node;
2. ripristinare la release precedente o rimuovere il sito di collaudo;
3. mantenere separata la directory dati per l’analisi;
4. ripristinare il backup SQLite sintetico quando necessario;
5. revocare il token backend;
6. verificare HTTP 401 o indisponibilità controllata del sottodominio.

### Backend

1. disabilitare l’app di collaudo;
2. ripristinare la directory backend dal backup;
3. ripristinare il database MariaDB di collaudo;
4. verificare le righe della tabella migrazioni;
5. non toccare il backend operativo.

### Sito

1. rimuovere esclusivamente la destinazione statica di collaudo;
2. verificare che il sito pubblico non sia cambiato;
3. mantenere il percorso professionale escluso.

## 14. Gate di autorizzazione

### Gate 1 — creazione ambiente

Richiede autorizzazione esplicita prima di creare siti, sottodomini, directory persistenti, database o token su Infomaniak.

### Gate 2 — migrazioni e test remoto

Richiede autorizzazione esplicita dopo la verifica dell’inventario e dei backup, prima di applicare migrazioni o inviare dati sintetici.

### Gate 3 — merge e rilascio

Richiede un’ulteriore autorizzazione esplicita dopo il rapporto di collaudo. Il superamento del test non autorizza automaticamente merge, deploy o attivazione pubblica.

## 15. Stato corrente

Alla data del documento:

- i pacchetti sono soltanto verificati in GitHub;
- gli artefatti manuali non sono stati generati;
- nessuna risorsa di collaudo è stata creata su Infomaniak;
- nessuna migrazione remota è stata applicata;
- nessun dato sintetico o reale è stato inviato;
- le PR #23, #6 e #20 restano aperte, in bozza e non unite.
