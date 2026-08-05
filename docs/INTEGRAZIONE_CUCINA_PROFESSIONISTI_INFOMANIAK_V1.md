# Integrazione sito cucina, professionisti e Infomaniak — v1

Data: 5 agosto 2026

Questo ramo raccoglie il sito cucina-first della PR #22 e dovrà assorbire in modo controllato:

- il percorso professionale prudenziale della PR #15;
- l'allineamento Privacy e stato portale della PR #19;
- il contratto reale del portale/backend definito nel repository privato `sistema90g-portale-backend`.

## Regole

1. La home e la navigazione restano focalizzate sulla cucina.
2. Il percorso professionale resta secondario, separato dalle richieste cucina e inizialmente non indicizzato.
3. La CTA cucina non va attivata pubblicamente prima del collaudo sito → portale → backend → Console → ACK.
4. Prezzi e titoli ricevuti dal browser sono informativi: il backend resta la fonte autorevole.
5. Privacy Policy, portale e funzioni effettivamente attive devono coincidere.
6. Nessun merge o deploy senza verifica integrata e approvazione esplicita.

## Conflitti da risolvere

- `index.html`: cucina-first contro stato prudenziale del portale;
- `portal-config.js`: attivo nella PR #22, sospeso nella PR #19;
- `professionisti.html`: deve assorbire il percorso inbound senza riaprire il posizionamento generalista;
- Privacy generale e informativa specifica professionisti;
- sitemap e indicizzazione del modulo professionale.

## Ordine

1. stabilizzare il contratto backend e il portale;
2. integrare il percorso professionale in stato inattivo;
3. aggiornare Privacy;
4. eseguire audit statico, browser, accessibilità e collegamenti;
5. collaudare end-to-end;
6. preparare il pacchetto Infomaniak senza pubblicarlo.
