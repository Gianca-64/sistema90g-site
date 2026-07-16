# Audit sito Sistema 90G

**Data:** 11 luglio 2026  
**Stato:** verifica tecnica e contenutistica iniziale  
**Repository verificato:** `Gianca-64/sistema90g-site`  
**Dominio verificato:** `https://sistema90g.it`

## 1. Architettura corretta

- Hosting e pubblicazione: Cloudflare.
- Database e dati applicativi: Supabase.
- Repository: GitHub.
- Console e portali: repository `Gianca-64/90g-console` pubblicato su Cloudflare.
- Tauri, SQLite, GitHub Pages e Vercel non appartengono più all'architettura attiva.

## 2. Elementi già coerenti

La home comunica correttamente molti principi del Metodo:

- analisi preventiva indipendente;
- problemi non evidenti e costi tardivi;
- rapporto tra persone, aperture, percorsi, materiali, impianti e funzioni;
- simulazione dell'uso quotidiano;
- distinzione tra elementi verificabili e controlli riservati ai professionisti abilitati;
- assenza di garanzia artificiale di trovare sempre un errore;
- priorità alla decisione del cliente.

La pagina dei casi presenta criticità concrete, conseguenze d'uso e limiti dichiarati. Il portale pubblico risulta collegato alla Console Cloudflare.

## 3. Incoerenze critiche da correggere

### 3.1 Identità ancora legata alla progettazione

Nella testata del repository compare ancora:

`PROGETTAZIONE · ANALISI PREVENTIVA`

La nuova identità stabilisce che Sistema 90G non nasce come servizio di progettazione, ma come sistema diagnostico degli ambienti e delle decisioni. La parola “progettazione” può creare aspettative errate e responsabilità non coerenti.

### 3.2 Servizio “Progetto da zero” in conflitto con il Metodo

La home presenta ancora il servizio “Progetto da zero” e lo descrive come sviluppo della distribuzione e del progetto. Questa promessa contraddice direttamente il principio appena definito: Sistema 90G diagnostica, individua criticità, valuta conseguenze e indica direzioni di miglioramento, senza sostituirsi alla progettazione professionale.

Prima di modificare il testo va completato l'audit dei servizi e deciso se:

- eliminare il livello;
- trasformarlo in “Diagnosi iniziale da zero” o nome equivalente;
- limitarlo alla costruzione del quadro decisionale e delle verifiche, senza progetto esecutivo.

### 3.3 Email non aggiornata

La home pubblica e il markup strutturato contengono ancora:

`sistema90g@icloud.com`

L'indirizzo operativo definito è:

`info@sistema90g.it`

La correzione deve essere applicata in tutte le pagine HTML, nei dati strutturati, nelle policy, nel footer e negli eventuali script.

### 3.4 Informativa privacy con infrastruttura superata

La Privacy Policy indica ancora GitHub Pages tra i servizi di hosting. Il sito è invece su Cloudflare. L'informativa deve essere aggiornata indicando l'infrastruttura effettiva e verificando anche il ruolo di Supabase per i dati inviati attraverso il portale.

Questa è una correzione tecnica necessaria, ma il testo finale richiede verifica privacy professionale.

### 3.5 WhatsApp ancora presente come canale principale

La home pubblica mostra ancora il collegamento “Chat WhatsApp” e la Privacy Policy cita WhatsApp come canale di contatto. Il flusso operativo deciso prevede il portale pubblico come canale principale per la raccolta dei casi. WhatsApp può restare solo se svolge un ruolo secondario chiaramente definito.

### 3.6 Nuovo posizionamento non ancora completo

Il sito parla già di persone e uso reale, ma non esprime ancora con sufficiente chiarezza i principi nuovi:

- ascolto prima della diagnosi;
- comprensione delle abitudini rilevanti;
- centralità della relazione tra persona e ambiente;
- diagnosi motivata prima delle possibili soluzioni;
- linguaggio semplice e comprensibile;
- Sistema 90G costruito sul Metodo e sulla Biblioteca Diagnostica, non “creato dall'AI”.

## 4. Verifiche tecniche sul dominio pubblico

### Confermate

- Home raggiungibile.
- Pagina casi raggiungibile.
- Privacy Policy raggiungibile.
- Collegamenti verso il portale pubblico presenti.
- Banner cookie presente.
- Pagine indicizzabili con canonical e metadati principali.

### Non ancora confermate

- Corretta ricezione e salvataggio di una richiesta dal portale pubblico.
- Percorso completo sito → portale → Supabase → Console.
- Resa mobile di tutte le pagine.
- Assenza di collegamenti interni rotti su tutte le pagine.
- Coerenza effettiva di tutte le immagini con il Manuale Immagini.
- Deployment Cloudflare dell'ultima versione del repository.
- Presenza di eventuali copie o repository concorrenti pubblicati.

## 5. Ordine corretto degli interventi

1. Confermare quale repository alimenta realmente `sistema90g.it`.
2. Verificare il deployment Cloudflare e il branch effettivo.
3. Correggere email e riferimenti infrastrutturali superati.
4. Verificare il percorso completo del portale pubblico con Supabase.
5. Concludere l'audit dei servizi, soprattutto “Progetto da zero”.
6. Riscrivere il posizionamento del sito secondo il Metodo diagnostico.
7. Aggiornare Privacy e Cookie Policy con infrastruttura reale.
8. Eseguire audit collegamenti, mobile, SEO, accessibilità e immagini.
9. Pubblicare su Cloudflare.
10. Verificare ogni modifica sul dominio pubblico prima di dichiararla completata.

## 6. Decisione operativa

Non eseguire una riscrittura estesa della home prima di aver riallineato i servizi. È invece sicuro procedere subito con:

- sostituzione dell'email obsoleta;
- rimozione dei riferimenti a GitHub Pages;
- verifica dei collegamenti al portale Cloudflare;
- eliminazione di eventuali riferimenti a Vercel, Tauri e SQLite;
- controllo del repository realmente pubblicato.

La modifica del servizio “Progetto da zero” deve essere trattata come decisione commerciale e di posizionamento, non come semplice correzione testuale.
