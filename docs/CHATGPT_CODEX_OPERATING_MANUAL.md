# Sistema 90G — Manuale operativo ChatGPT + Codex — Sito pubblico

## Scopo
Questo documento rende ogni nuova conversazione sul Sito immediatamente operativa. Va letto insieme ad `AGENTS.md` e a `docs/LINEE_EDITORIALI_SITO_SISTEMA90G.md` prima di modificare pagine, testi, SEO, Free Entry o deploy.

## Ruoli
**ChatGPT = regia:** strategia, architettura, UX, contenuti, SEO, priorità, decisioni e verifica finale.

**Codex locale = operatore:** Terminale, Git, ricerca file, modifiche meccaniche autorizzate, verifiche ripetitive, build/package/deploy con procedure già esistenti, raccolta log.

**Operatore umano:** approva decisioni e verifica il sito reale. Non deve eseguire Terminale/Git/build quando Codex può farlo.

Codex non deve decidere autonomamente testi pubblici, posizionamento, CTA, architettura informativa, servizi, prezzi o strategie SEO.

## Invariante tempo operatore — obbligatoria
Leggere e applicare anche `docs/OPERATOR_TIME_INVARIANT.md`.

L'operatore umano non deve diventare il ponte operativo tra ChatGPT e Codex. È vietato trasformare una verifica tecnica in una sequenza ripetitiva di micro-task e copia/incolla di errori quando i controlli indipendenti possono essere raccolti nello stesso batch.

Regola predefinita: **batch-first**. Prima di richiedere un nuovo intervento umano, ChatGPT/Codex devono raccogliere tutti i fallimenti indipendenti ragionevolmente disponibili, raggruppare le correzioni meccaniche già determinate e produrre un unico rapporto compatto. Coinvolgere l'operatore solo per decisioni reali, autorizzazioni di sistema, dati non recuperabili o collaudi umani.

## Apertura di ogni nuova chat
Prima di intervenire:
1. leggere `AGENTS.md`, questo manuale, `docs/OPERATOR_TIME_INVARIANT.md` e le linee editoriali;
2. verificare repository, branch, working tree, HEAD locale/remoto e file reali coinvolti;
3. non assumere che una modifica descritta in una chat precedente sia già pubblicata;
4. distinguere stato verificato, ipotesi, decisione e prossimo passo;
5. non rifare audit già chiusi senza nuova evidenza;
6. non copiare processi interni della Console nel sito pubblico.

## Repository canonico
Remoto: `Gianca-64/sistema90g-site`.
Branch canonico: `main`.
La posizione locale va verificata da Codex dal remote Git; non inventarla se non è già documentata nell'ambiente.

## Working copy e lavori paralleli
La working copy usata per deploy ordinario deve restare sul branch canonico. Se una lavorazione parallela richiede un branch diverso, Codex deve usare una working copy/worktree separata e non contaminare la copia destinata alla pubblicazione.

Non cambiare branch della copia canonica per comodità se questo può interferire con deploy o altre chat.

## Protocollo di delega a Codex
Ogni task locale deve indicare: obiettivo, repository, branch, file consentiti, modifiche autorizzate, controlli da eseguire, condizioni di stop e output finale.

Sequenza standard: **verifica → delta minimo → controlli → raccolta batch degli esiti → rapporto → stop**.

Codex non deve correggere automaticamente problemi fuori scope, installare dipendenze o cambiare infrastruttura per “far passare” un controllo. Se il mandato autorizza una diagnosi batch, un singolo controllo fallito non obbliga a interrompere gli altri controlli indipendenti.

## Gestione conversazioni
Una nuova chat deve proseguire dallo stato reale del repository, non dalla memoria soltanto. Le decisioni già consolidate non vanno riaperte senza nuova evidenza concreta.

Sito, Console, Portale e Configuratore restano separati. Non riutilizzare comandi, branch, Worker o configurazioni di altri repository.

Quando la richiesta riguarda contenuti pubblici, ChatGPT mantiene la decisione finale su tono, messaggio, struttura, CTA e valore per l'utente; Codex può applicare modifiche testuali solo quando sono già state definite con precisione.

## Invarianti editoriali e commerciali
- problema della persona prima del servizio;
- Free Entry come primo aiuto utile, non come preventivatore aggressivo;
- niente esposizione del metodo proprietario interno;
- neutralità verso marchi terzi;
- niente testi meccanici o CTA ripetute;
- non trasformare ogni richiesta in vendita;
- AI come supporto interno, non come centro del posizionamento.

## Git e deploy
Prima di operare: branch `main`, working tree pulito, `git fetch origin`, solo fast-forward. Mai reset hard, clean distruttivo, stash automatico o force push.

Il deploy deve usare esclusivamente la procedura locale già verificata del repository. Se la procedura reale non è chiara, Codex deve fermarsi e riportare i file/configurazioni trovati; non inventare un comando di deploy.

## Stop conditions
Codex si ferma se trova branch inatteso, modifiche locali estranee, divergenza non fast-forward, dipendenze/configurazioni non documentate, errore che richiede una scelta editoriale/strategica, credenziali o rischio di modifica a sistemi diversi dal Sito. Un singolo test/audit fallito non è una stop condition se il mandato autorizza la raccolta batch degli altri controlli indipendenti.

## Rapporto Codex
Riportare: branch/HEAD, working tree, file toccati, verifiche eseguite, esito build/deploy se previsto, elenco compatto dei fallimenti raccolti nel batch e attività non completate.

## Chiusura
Una modifica al Sito è conclusa solo dopo verifica del diff, controlli previsti e, se pubblicata, verifica reale della pagina. La decisione finale resta nella conversazione ChatGPT.