# Sistema 90G — Invariante tempo operatore

Questa regola è vincolante per ChatGPT, Codex e ogni nuova conversazione tecnica relativa al repository.

L'operatore umano deve dedicare il proprio tempo a casi, persone, contenuti, strategia, decisioni e collaudi reali. Non deve diventare il ponte operativo tra ChatGPT e Codex né il runner manuale di Git, audit, test, build, deploy o diagnostica ripetitiva.

Quando un gate composto da più audit/test fallisce, usare una diagnosi batch: raccogliere in una sola esecuzione tutti i fallimenti indipendenti disponibili, distinguere residui legacy da regressioni reali, raggruppare le correzioni meccaniche già decise in un solo incarico Codex, rieseguire il gate solo dopo il batch e restituire un unico rapporto compatto.

Coinvolgere l'operatore solo per decisioni funzionali/progettuali/commerciali, verifiche visive reali, autenticazioni o autorizzazioni di sistema, informazioni non recuperabili dagli strumenti o scelte con conseguenze reali. Non coinvolgerlo per Terminale, Git, lettura log, audit, test, build, copia di errori uno alla volta o modifiche meccaniche già specificate.

ChatGPT deve fare la diagnosi più ampia possibile prima di delegare e minimizzare il numero di passaggi richiesti all'operatore. Codex resta esecutore, ma quando riceve un mandato di diagnosi batch deve continuare a raccogliere gli esiti indipendenti anche dopo un fallimento, senza correggere autonomamente ciò che non è stato autorizzato.

Una procedura tecnica è ben progettata quando l'operatore riceve idealmente una sola richiesta di intervento all'inizio o alla fine del batch, non una richiesta per ogni errore intermedio.
