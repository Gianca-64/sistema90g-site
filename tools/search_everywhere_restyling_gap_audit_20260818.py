from pathlib import Path
from html import unescape
import re

DIST = Path('dist')

INTENTS = [
    ('rinnovare-senza-cambiarla', 'Come rinnovare la cucina senza cambiarla', ['rinnovare', 'cucina', 'senza cambiarla']),
    ('quando-conviene-restyling', 'Quando conviene rinnovare invece di sostituire la cucina', ['conviene', 'restyling', 'sostituire']),
    ('cambiare-ante', 'Cambiare o sostituire le ante della cucina', ['ante', 'cucina', 'sostituire']),
    ('cambiare-colore-ante', 'Cambiare colore alle ante della cucina', ['colore', 'ante', 'cucina']),
    ('cambiare-top', 'Cambiare il top senza sostituire la cucina', ['top', 'cucina', 'sostituire']),
    ('cambiare-maniglie', 'Cambiare le maniglie per rinnovare la cucina', ['maniglie', 'cucina', 'rinnovare']),
    ('rinnovare-schienale', 'Rinnovare lo schienale della cucina', ['schienale', 'cucina', 'rinnovare']),
    ('cucina-legno-datata', 'Rinnovare una cucina in legno datata', ['cucina', 'legno', 'rinnovare']),
    ('riutilizzare-struttura', 'Mantenere la struttura e cambiare solo alcune parti', ['struttura', 'mantenere', 'cucina']),
    ('restyling-elettrodomestici', 'Aggiornare elettrodomestici in una cucina esistente', ['elettrodomestici', 'cucina esistente', 'aggiornare']),
]

TAG_RE = re.compile(r'<[^>]+>')
SPACE_RE = re.compile(r'\s+')
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.I | re.S)
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
CANON_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', re.I)


def clean_html(s):
    s = TAG_RE.sub(' ', s)
    s = unescape(s)
    return SPACE_RE.sub(' ', s).strip().lower()

pages = []
for path in sorted(DIST.glob('*.html')):
    raw = path.read_text(errors='ignore')
    if 'noindex' in raw.lower():
        continue
    if not CANON_RE.search(raw):
        continue
    title_m = TITLE_RE.search(raw)
    h1_m = H1_RE.search(raw)
    pages.append({
        'file': path.name,
        'title': clean_html(title_m.group(1)) if title_m else '',
        'h1': clean_html(h1_m.group(1)) if h1_m else '',
        'text': clean_html(raw),
    })

print(f'Pagine indicizzabili analizzate: {len(pages)}')
print('\n=== RESTYLING: COPERTURA INTENTI ===')

weak = []
for slug, label, terms in INTENTS:
    ranked = []
    for p in pages:
        th = sum(1 for t in terms if t in p['title'])
        hh = sum(1 for t in terms if t in p['h1'])
        tx = sum(1 for t in terms if t in p['text'])
        score = th * 4 + hh * 3 + tx
        if score:
            ranked.append((score, p))
    ranked.sort(key=lambda x: (-x[0], x[1]['file']))
    best = ranked[0] if ranked else None
    if not best:
        status = 'SCOPERTO'
    elif best[0] >= 10:
        status = 'FORTE'
    elif best[0] >= 6:
        status = 'PARZIALE'
    else:
        status = 'DEBOLE'
    best_txt = f"{best[1]['file']} (score {best[0]})" if best else '—'
    print(f'{status:8} | {label} | {best_txt}')
    if status != 'FORTE':
        weak.append((status, label, ranked[:3]))

print('\n=== PRIORITA RESTYLING ===')
if not weak:
    print('- Nessun gap forte nel cluster Restyling.')
else:
    for status, label, ranked in weak:
        print(f'[{status}] {label}')
        if ranked:
            for score, p in ranked:
                print(f"  - {p['file']} | score {score} | TITLE: {p['title']}")
        else:
            print('  - nessuna pagina candidata')

print('\nAudit Restyling Search Everywhere completato.')
