# Sistema 90G — Sito pubblico — istruzioni per agenti

## Ruoli permanenti

Questa divisione è vincolante anche per il Sito pubblico di Sistema 90G.

### ChatGPT = direzione
ChatGPT mantiene:
- ragionamento e decisioni;
- architettura e programmazione;
- UX e strategia;
- contenuti, posizionamento e linee editoriali;
- definizione delle modifiche;
- valutazione dei rischi;
- verifica finale.

### Codex locale = operatore tecnico
Codex esegue sul Mac le attività meccaniche già definite:
- Git e sincronizzazione del repository;
- ricerca e modifiche ripetitive autorizzate;
- audit e verifiche;
- build/package del sito;
- deploy Cloudflare con la procedura canonica;
- raccolta di log ed errori.

Codex non è una seconda regia. Non deve decidere autonomamente architettura, UX, strategia, testi pubblici, SEO, servizi o cambiamenti di comportamento. Se incontra una scelta non prevista, un conflitto, un working tree non pulito o un errore che richiede interpretazione, si ferma e riferisce.

### Operatore umano
Nell'uso quotidiano normale l'operatore lavora con ChatGPT e non deve usare Terminale, Git, build o deploy. Un intervento manuale sul Mac è ammesso solo in situazioni eccezionali realmente necessarie, per esempio autorizzazioni di sistema, autenticazioni o recuperi infrastrutturali.

## Separazione dei sistemi
Il Sito è indipendente da Console e Configuratore. Non usare branch, script, build, Worker o configurazioni degli altri repository.

Repository: `Gianca-64/sistema90g-site`
Branch canonico: `main`

## Contenuti pubblici
Per qualsiasi intervento che crei o modifichi testi pubblici, pagine, articoli, FAQ, CTA o contenuti SEO, leggere e applicare prima:

`docs/LINEE_EDITORIALI_SITO_SISTEMA90G.md`

Le linee editoriali sono un requisito del sito. Evitare template linguistici rigidi, CTA ripetute e strutture editoriali uniformi. La qualità e la naturalezza del testo prevalgono sulla ripetizione meccanica di pattern SEO.

Le procedure interne complete di Sistema 90G restano nel repository privato della Console e non devono essere copiate nel sito pubblico.

## Regola Git
Prima di operazioni automatiche:
1. branch `main`;
2. working tree pulito;
3. `git fetch origin`;
4. solo fast-forward verso `origin/main`;
5. nessun reset, stash automatico, clean o force-push.

## Deploy
Il deploy ordinario deve usare esclusivamente la procedura locale verificata del repository. Non usare GitHub Actions come meccanismo ordinario di pubblicazione.
