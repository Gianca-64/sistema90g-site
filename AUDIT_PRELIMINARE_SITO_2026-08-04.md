# Sistema 90G — Audit preliminare del sito

**Data:** 4 agosto 2026  
**Repository:** `Gianca-64/sistema90g-site`  
**Baseline verificata:** `main` — commit `a92328fa914cf01330a41b800be056d6f8d79716`  
**Issue di riferimento:** #16  
**Classificazione:** P1 — pubblico controllato  
**Esito:** **DA RIVEDERE**

## 1. Obiettivo

Verificare che il sito sia pronto ad accogliere una base più ampia di pagine, articoli, FAQ e contenuti evergreen senza moltiplicare incoerenze, duplicazioni, percorsi poco leggibili o regressioni tecniche.

L’audit riguarda la struttura pubblica, la leggibilità, i percorsi di conversione, la coerenza tra pubblico e servizio, l’indicizzazione, i collegamenti interni e la pull request #15. Non valuta né pubblica procedure riservate del Metodo Sistema 90G.

## 2. Fonti esaminate

- repository `main` e file pubblici correnti;
- sito pubblico `https://sistema90g.it/`;
- `sitemap.xml`, `image-sitemap.xml`, `robots.txt` e `.htaccess`;
- pagine Home, Servizi, Percorso guidato, Metodo, Professionisti, Agenzie, Rivenditori e Privacy;
- configurazione del portale e matrice pubblica dei servizi;
- script interno `tools/audit_release.py`;
- pull request #15 `Marketing: percorso inbound per professionisti`.

## 3. Quadro sintetico

Il sito dispone già di una buona baseline: posizionamento leggibile, navigazione coerente, pagine servizio, casi reali, canonical, redirect e percorso guidato con servizi e prezzi vigenti.

Non è però ancora opportuno avviare un’espansione editoriale ampia. Prima devono essere risolti tre blocchi:

1. informativa privacy non allineata allo stato reale del portale;
2. regressioni e dipendenze non chiuse nella PR #15;
3. assenza di controlli automatici obbligatori sui nuovi contributi.

## 4. Inventario pubblico verificato

La sitemap contiene **59 URL indicizzabili**:

- **27** pagine di casi singoli;
- **6** pagine archivio/categoria dei casi;
- **2** approfondimenti editoriali;
- pagine istituzionali, servizi, pubblici professionali e percorso guidato.

La struttura è quindi già ampia ma sbilanciata sui casi. Il prossimo ciclo non deve aumentare principalmente il numero dei casi: deve rafforzare pagine autorevoli per pubblico, problema e decisione.

## 5. Punti già solidi — MANTENERE

### Posizionamento

La Home, la pagina Metodo e le pagine servizio presentano Sistema 90G come analisi preventiva indipendente, distinguendo controllo, limiti, ruolo umano e assenza di provvigioni.

### Percorso guidato

Il percorso separa ruolo, situazione, servizio e prezzo prima dell’inserimento dei dati personali. La matrice corrente contiene i servizi e i prezzi approvati.

### Indicizzazione di base

- `robots.txt` consente la scansione e collega le due sitemap;
- `.htaccess` governa HTTPS, dominio senza `www`, Home canonica e redirect delle vecchie rotte;
- la sitemap principale è coerente con la struttura pubblica corrente;
- le pagine principali usano canonical e metadati sociali.

### Navigazione e responsabilità

Le pagine principali collegano servizi, casi, Metodo, professionisti e percorso guidato. I limiti verso tecnici, progettisti e rivenditori sono generalmente dichiarati.

## 6. Criticità bloccanti — CORREGGERE PRIMA DEI NUOVI CONTENUTI

### B1 — Privacy non allineata al portale attivo

La Privacy Policy, aggiornata al 20 luglio 2026, dichiara ancora che il percorso non raccoglie dati personali durante l’attivazione del portale. La configurazione pubblica corrente indica invece il portale come attivo e abilitato alla raccolta della richiesta iniziale.

**Azione richiesta:** aggiornare l’informativa prima di aggiungere nuovi moduli o nuovi percorsi di acquisizione. Devono essere chiariti stato reale, dati raccolti, finalità, base giuridica, consensi separati, conservazione, destinatari e diritti.

### B2 — PR #15 non pronta al merge

La PR #15 è correttamente in stato Draft, ma al momento introduce regressioni e dipendenze non chiuse.

Correzioni obbligatorie:

- aggiungere `interesse-professionale.html` alla sitemap solo quando la funzione è realmente operativa;
- aggiornare la Privacy Policy con una sezione coerente dedicata al modulo;
- ripristinare footer standard, collegamento alla proprietà intellettuale, gestione cookie e avviso finale nelle pagine modificate;
- conservare dati strutturati, metadati Open Graph/Twitter e riferimenti Organization/Person/WebSite già presenti;
- mantenere gli attributi di tracciamento e instradamento delle CTA correnti;
- aggiungere una validazione client completa e accessibile dei campi obbligatori;
- richiedere email e consenso quando l’azione scelta presuppone una risposta;
- rendere il comportamento di reinvio realmente idempotente;
- non mostrare messaggi tecnici provenienti direttamente dal backend;
- verificare endpoint, CORS, anti-abuso, persistenza, deduplicazione e registrazione dell’origine;
- impedire il deploy della pagina indicizzabile finché il backend non è verificato.

La nuova immagine dedicata ai rivenditori è coerente con l’obiettivo della pagina e può essere mantenuta, purché restino invariati metadata, footer e tracciamento.

### B3 — Audit esistente non obbligatorio in GitHub

Il repository contiene `tools/audit_release.py` e test del percorso guidato, ma il commit corrente non espone controlli di stato o workflow eseguiti.

**Azione richiesta:** aggiungere una GitHub Action obbligatoria per pull request che esegua almeno:

- audit delle pagine e degli asset;
- parità canonical/sitemap;
- controllo di navigazione e footer;
- test del percorso guidato e della matrice prezzi;
- controllo dei vecchi termini e dei link locali;
- verifica che una nuova pagina indicizzabile abbia privacy, metadata, canonical e sitemap coerenti.

## 7. Lacune strutturali — COMPLETARE PRIMA DELL’ESPANSIONE AMPIA

### S1 — Mancano destinazioni professionali dedicate

La pagina `professionisti.html` collega direttamente soltanto agenzie immobiliari e rivenditori. Il percorso guidato riconosce anche interior designer, architetti/geometri e imprese, ma non esistono ancora pagine autorevoli dedicate a questi pubblici.

**Pagine da predisporre:**

1. Architetti, interior designer e geometri;
2. Imprese di costruzione e ristrutturazione.

Ogni pagina deve spiegare problema, complementarità, limiti, servizio pertinente e azione successiva senza assumere un tono commerciale.

### S2 — Biblioteca pubblica troppo concentrata sui casi

Con 33 URL legati ai casi e solo 2 approfondimenti, il sito dimostra esperienza ma copre ancora poco le domande informative che precedono la scelta.

**Direzione corretta:** creare contenuti evergreen per decisione e problema, collegati a servizi e casi pertinenti. Non pubblicare checklist complete o procedure replicabili.

### S3 — Aggiornamenti e date non uniformi

Solo una parte degli URL in sitemap espone `lastmod`. Le pagine soggette a cambiamenti commerciali, tecnici o normativi dovrebbero avere data di aggiornamento visibile e coerente con la sitemap.

## 8. Mappa delle decisioni sulle pagine

### Mantenere come baseline

- Home;
- Servizi;
- Analisi preventiva / percorso guidato;
- Metodo e uso dell’AI;
- pagine dei sei servizi privati;
- archivio e categorie dei casi;
- Agenzie immobiliari;
- Rivenditori di cucine;
- Proprietà intellettuale.

### Correggere prima dell’espansione

- Privacy Policy;
- Professionisti;
- PR #15 e nuova pagina di manifestazione d’interesse;
- sitemap e image sitemap dopo l’approvazione di nuove pagine;
- controlli automatici GitHub.

### Creare dopo le correzioni bloccanti

- pagina per architetti, interior designer e geometri;
- pagina per imprese;
- checklist pubblica orientativa prima di approvare un progetto cucina;
- contenuti evergreen sulle decisioni prima dell’ordine, dati mancanti, interferenze d’uso e lettura dei preventivi;
- FAQ collegate alle pagine servizio.

## 9. Sequenza operativa proposta

1. Correggere e approvare Privacy Policy.
2. Portare la PR #15 a conformità oppure separare la sola immagine rivenditori dal percorso inbound.
3. Introdurre audit automatico obbligatorio su GitHub.
4. Completare le due pagine professionali mancanti.
5. Definire mappa interna dei primi 20 temi evergreen e relativi collegamenti.
6. Pubblicare il primo ciclo soltanto dopo approvazione umana e verifica post-deploy.

## 10. Criterio di chiusura dell’intervento

L’audit preliminare potrà essere dichiarato concluso quando:

- la Privacy Policy descrive il processo reale;
- la PR #15 non introduce regressioni e il backend è verificato;
- i test automatici risultano obbligatori e superati;
- sono approvate le destinazioni professionali mancanti;
- esiste una mappa delle pagine da creare con priorità e collegamenti;
- nessuna modifica è stata pubblicata senza revisione umana.

## 11. Esito finale

**DA RIVEDERE**

Il sito è una base valida, ma l’espansione massiva dei contenuti deve attendere la chiusura dei blocchi B1–B3. Le correzioni indicate non richiedono di rifare il sito: servono a proteggere coerenza, affidabilità e capacità di crescita.
