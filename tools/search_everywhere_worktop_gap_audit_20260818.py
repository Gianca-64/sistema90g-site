from pathlib import Path
from html import unescape
import re

DIST = Path('dist')

# Intenti emersi dalla ricerca esterna su piano di lavoro, colonne e uso reale.
INTENTS = [
    ('quanto-piano-lavoro', 'Quanto piano di lavoro serve davvero in cucina?', ['piano di lavoro', 'cucina'], ['piano di lavoro']),
    ('piano-continuo', 'È meglio avere un piano di lavoro continuo tra lavello e cottura?', ['piano di lavoro', 'lavello', 'cottura'], ['piano di lavoro', 'lavello']),
    ('forno-colonna-vs-piano', 'Forno in colonna o più piano di lavoro?', ['forno', 'colonna', 'piano di lavoro'], ['forno', 'piano di lavoro']),
    ('dispensa-vs-piano', 'Meglio una colonna dispensa o più piano di lavoro?', ['dispensa', 'colonna', 'piano di lavoro'], ['dispensa', 'piano di lavoro']),
    ('piccoli-elettrodomestici', 'Dove mettere macchina del caffè e piccoli elettrodomestici senza perdere il piano?', ['macchina del caffè', 'piccoli elettrodomestici', 'piano di lavoro'], ['piccoli elettrodomestici', 'macchina del caffè']),
    ('spazio-appoggio-forno', 'Serve uno spazio di appoggio vicino al forno?', ['spazio', 'appoggio', 'forno'], ['appoggio', 'forno']),
    ('spazio-laterale-cottura', 'Quanto spazio libero lasciare vicino al piano cottura?', ['spazio', 'piano cottura', 'cucina'], ['piano cottura']),
]

TAG_RE = re.compile(r'<[^>]+>')
SPACE_RE = re.compile(r'\s+')
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.I | re.S)
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
H23_RE = re.compile(r'<h[23][^>]*>(.*?)</h[23]>', re.I | re.S)
CANON_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', re.I)


def clean_html(s):
    s = TAG_RE.sub(' ', s)
    s = unescape(s)
    return SPACE_RE.sub(' ', s).strip().lower()

pages = []
for path in sorted(DIST.glob('*.html')):
    raw = path.read_text(errors='ignore')
    if 'noindex' in raw.lower() or not CANON_RE.search(raw):
        continue
    title_m = TITLE_RE.search(raw)
    h1_m = H1_RE.search(raw)
    h23 = ' '.join(clean_html(x) for x in H23_RE.findall(raw))
    pages.append({
        'file': path.name,
        'title': clean_html(title_m.group(1)) if title_m else '',
        'h1': clean_html(h1_m.group(1)) if h1_m else '',
        'h23': h23,
        'text': clean_html(raw),
    })

print(f'Pagine indicizzabili analizzate: {len(pages)}')
print('\n=== PIANO DI LAVORO CUCINA: COPERTURA INTENTI ===')

weak = []
for slug, label, terms, signatures in INTENTS:
    ranked = []
    for p in pages:
        th = sum(1 for t in terms if t in p['title'])
        hh = sum(1 for t in terms if t in p['h1'])
        sh = sum(1 for t in terms if t in p['h23'])
        tx = sum(1 for t in terms if t in p['text'])
        signature_structured = any(s in p['title'] or s in p['h1'] or s in p['h23'] for s in signatures)
        score = th * 5 + hh * 4 + sh * 3 + tx
        if score:
            ranked.append((score, signature_structured, p))
    ranked.sort(key=lambda x: (-int(x[1]), -x[0], x[2]['file']))
    best = ranked[0] if ranked else None
    if not best:
        status = 'SCOPERTO'
    elif best[1] and best[0] >= 12:
        status = 'FORTE'
    elif best[0] >= 7:
        status = 'PARZIALE'
    else:
        status = 'DEBOLE'
    best_txt = f"{best[2]['file']} (score {best[0]})" if best else '—'
    print(f'{status:8} | {label} | {best_txt}')
    if status != 'FORTE':
        weak.append((status, label, ranked[:3]))

print('\n=== PRIORITA CLUSTER PIANO DI LAVORO ===')
if not weak:
    print('- Nessun gap forte nel cluster analizzato.')
else:
    for status, label, ranked in weak:
        print(f'[{status}] {label}')
        if ranked:
            for score, structured, p in ranked:
                marker = 'struttura-ok' if structured else 'solo-corpo'
                print(f"  - {p['file']} | score {score} | {marker} | TITLE: {p['title']}")
        else:
            print('  - nessuna pagina candidata')

print('\nAudit Search Everywhere piano di lavoro cucina completato.')
