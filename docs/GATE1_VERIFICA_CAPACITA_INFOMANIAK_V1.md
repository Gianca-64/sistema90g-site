# Gate 1 — Verifica capacità Infomaniak v1

Data: 5 agosto 2026  
Stato: **verifica preliminare; non creare risorse**

## Obiettivo

Accertare che il prodotto Infomaniak disponibile possa ospitare l’ambiente di collaudo isolato definito in:

`docs/CONTRATTO_COLLAUDO_INFOMANIAK_ISOLATO_V1.md`

Questa verifica non autorizza l’aggiunta di siti, sottodomini, database, utenti, token o file.

## Evidenze necessarie dal Manager

Aprire il prodotto di hosting destinato al progetto e documentare, senza salvare modifiche, le seguenti schermate.

### 1. Disponibilità sito Node.js

Percorso indicativo:

```text
Manager Infomaniak
→ Hosting
→ prodotto interessato
→ Aggiungi sito
→ Tecnologie avanzate
```

Verificare la presenza dell’opzione **Node.js**.

Evidenza richiesta:

- screenshot della scelta tecnologia;
- nome del prodotto o tipo di hosting visibile;
- numero di siti disponibili, quando mostrato;
- nessun clic finale su creazione o conferma.

### 2. Versioni Node.js disponibili

Aprire soltanto la schermata informativa o di configurazione preliminare del sito Node.js.

Verificare:

- disponibilità di Node.js 22 LTS oppure versione LTS compatibile da sottoporre a prova;
- possibilità di selezionare o modificare la versione;
- nessuna installazione avviata.

### 3. Configurazione applicazione

Verificare che l’interfaccia consenta di impostare:

```text
Directory di esecuzione
Comando di build
Comando di avvio
Porta di ascolto tramite PORT
Variabili d’ambiente
```

Configurazione prevista, da non salvare in questa fase:

```text
Build: nessuno
Start: node server.js
Porta: variabile PORT del Manager
```

### 4. Dominio e HTTPS

Verificare che sia possibile:

- associare un sottodominio separato;
- attivare un certificato HTTPS;
- mantenere il sito non collegato dal sito pubblico;
- visualizzare log e stato start/stop/restart.

Non creare il sottodominio durante la verifica.

### 5. Directory persistente privata

Verificare, tramite documentazione del prodotto o informazioni del Manager, che il sito Node.js disponga di uno spazio file persistente nel quale creare una directory:

```text
<S90G_DATA_DIR>/90g.sqlite
```

La directory deve essere:

- esterna alla release;
- non servita pubblicamente;
- scrivibile dal processo Node;
- persistente dopo restart e sostituzione del pacchetto;
- inclusa in una procedura di backup o ripristino verificabile.

### 6. Un solo processo applicativo

Verificare che l’ambiente permetta di mantenere una sola istanza attiva della Console. Il collaudo SQLite non deve usare più processi o repliche concorrenti sullo stesso database.

### 7. Backend PHP e MariaDB isolati

Verificare, senza crearli, che siano disponibili:

- una directory o un sito PHP separato per il backend di collaudo;
- un database MariaDB dedicato;
- un utente database dedicato;
- backup e ripristino del database;
- accesso HTTPS al backend di collaudo.

## Dati da non mostrare negli screenshot

Prima di condividere le immagini, nascondere o ritagliare:

- password;
- token;
- chiavi SSH;
- stringhe di connessione;
- email personali non necessarie;
- identificativi che autorizzano accessi;
- contenuti di database o file reali.

Il nome del prodotto, il tipo di hosting, le tecnologie disponibili e le opzioni generali possono restare visibili.

## Esito Gate 1

### Superato

Il Gate 1 è superato quando risultano confermati:

- sito Node.js disponibile;
- versione Node compatibile;
- start command e `PORT` configurabili;
- HTTPS e sottodominio separato;
- directory persistente privata;
- singolo processo applicativo;
- backend PHP e MariaDB isolabili;
- backup disponibili.

### Sospeso

Il Gate 1 resta sospeso quando una capacità non è chiaramente verificabile. Non si procede per supposizione.

### Non superato

Il Gate 1 non è superato quando manca una delle condizioni essenziali, in particolare:

- nessun sito Node.js disponibile;
- filesystem non persistente;
- impossibilità di proteggere la Console;
- impossibilità di isolare database e backend;
- obbligo di usare più processi sullo stesso SQLite.

In caso di esito negativo non si crea alcuna risorsa e non si cambia automaticamente architettura o fornitore.

## Rapporto minimo da produrre

```text
Prodotto Infomaniak verificato:
Tipo di hosting:
Sito Node.js disponibile: sì/no
Node 22 LTS disponibile: sì/no/da provare
Start command configurabile: sì/no
PORT gestita dal Manager: sì/no
Variabili ambiente: sì/no
HTTPS: sì/no
Sottodominio separato: sì/no
Directory persistente privata: sì/no/da verificare
Singolo processo: sì/no/da verificare
PHP staging separabile: sì/no
MariaDB staging separabile: sì/no
Backup file: sì/no
Backup database: sì/no
Esito Gate 1: superato/sospeso/non superato
Note:
```

## Passaggio successivo

Solo dopo il rapporto Gate 1 e una nuova autorizzazione esplicita si potrà predisporre l’ambiente vuoto di collaudo. Nessuna migrazione o richiesta sintetica rientra nel Gate 1.
