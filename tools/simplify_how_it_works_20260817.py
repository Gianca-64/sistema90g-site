from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'analisi-preventiva.html'
s = p.read_text(encoding='utf-8')

start = s.find('<section class="s90g-path-section" id="percorso">')
end = s.find('</main>', start)
if start < 0 or end < 0:
    raise SystemExit('ERRORE: sezione percorso o chiusura main non trovata.')

new_section = '''<section class="s90g-path-section" id="percorso"><div class="s90g-shell"><div class="s90g-path-intro"><p class="s90g-eyebrow">Tre situazioni</p><h2>Parti da dove si trova oggi la tua cucina.</h2><p>Non devi scegliere tra molti servizi. Riconosci la situazione e apri il percorso corrispondente: prezzo e contenuti sono visibili prima della richiesta.</p></div><div class="s90g-route-grid"><article class="s90g-route-card"><p class="s90g-eyebrow">Devi ancora progettarla</p><h3>Progetto Cucina Sistema 90G · 145 €</h3><p>Una base progettuale indipendente prima della scelta del rivenditore. Nel Portale puoi aggiungere solo gli approfondimenti che ti servono.</p><a class="s90g-link" href="/progetto-cucina-sistema90g.html">Scopri il Progetto Cucina →</a></article><article class="s90g-route-card"><p class="s90g-eyebrow">Hai già progetto o preventivo</p><h3>Seconda Opinione · da 127 €</h3><p>Un dubbio preciso oppure un controllo completo prima di firmare o confermare l'ordine.</p><a class="s90g-link" href="/seconda-opinione-cucina.html">Scopri la Seconda Opinione →</a></article><article class="s90g-route-card"><p class="s90g-eyebrow">Hai già una cucina</p><h3>Restyling cucina esistente · 79 €</h3><p>Decidi cosa mantenere, cosa modificare e quali verifiche affidare al fornitore senza riprogettare tutto.</p><a class="s90g-link" href="/restyling-cucina-esistente.html">Scopri il Restyling →</a></article></div></div></section><section class="s90g-dark-band"><div class="s90g-shell"><p class="s90g-eyebrow">Lavori nel settore?</p><h2>Il percorso professionale è separato.</h2><p>Rivenditori, architetti, geometri, interior designer, imprese e agenzie accedono a pagine dedicate, senza mescolare il loro percorso con quello del cliente privato.</p><div class="s90g-actions"><a class="s90g-button primary" href="/professionisti.html"><span>Vai ai Professionisti</span><span>→</span></a><a class="s90g-button" href="/rivenditori-cucine.html"><span>Vai ai Rivenditori</span><span>→</span></a></div></div></section>'''

s = s[:start] + new_section + s[end:]

s = s.replace('<p class="s90g-lead">Devi ancora progettare la cucina? Hai già un progetto o un preventivo? Vuoi rinnovare una cucina esistente? In tre passaggi individui il percorso pertinente prima di inserire dati personali o avviare una richiesta.</p>', '<p class="s90g-lead">Devi ancora progettare la cucina? Hai già un progetto o un preventivo? Vuoi rinnovare una cucina esistente? Scegli la situazione e vai direttamente al percorso pertinente.</p>')
s = s.replace('<h2>Prima la situazione, poi il percorso.</h2><p>Indica chi presenta la richiesta e a che punto si trova la cucina. Il percorso distingue progettazione, Seconda Opinione su una proposta esistente e Restyling di una cucina già installata.</p>', '<h2>Prima la situazione, poi il percorso.</h2><p>Per un privato bastano tre domande: devi ancora progettare, hai già una proposta oppure vuoi rinnovare una cucina esistente?</p>')
s = s.replace('<script src="portal-config.js"></script><script src="role-case-path.js?v=20260817c"></script>', '')

p.write_text(s, encoding='utf-8')
print('OK: Come funziona semplificata in tre percorsi diretti + accesso professionale separato.')
