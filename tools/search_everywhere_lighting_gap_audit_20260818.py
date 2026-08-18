from pathlib import Path
from html import unescape
import re

DIST = Path('dist')

INTENTS = [
    ('punti-luce-cucina', 'Dove posizionare i punti luce in cucina?', ['punti luce', 'cucina', 'posizionare'], ['punti luce', 'illuminazione']),
    ('piano-lavoro-ombre', 'Come illuminare il piano di lavoro senza creare ombre?', ['piano di lavoro', 'ombre', 'illuminare'], ['piano di lavoro', 'ombre']),
    ('sottopensile-led', 'Come predisporre e usare la luce LED sottopensile?', ['led', 'sottopensile', 'cucina'], ['sottopensile', 'led']),
    ('cucina-senza-pensili', 'Come illuminare una cucina senza pensili?', ['cucina', 'senza pensili', 'illuminare'], ['senza pensili']),
    ('isola-penisola-luce', 'Come illuminare isola o penisola senza lasciare zone buie?', ['isola', 'penisola', 'illuminare'], ['isola', 'penisola']),
    ('generale-vs-funzionale', 'Come combinare luce generale e luce funzionale in cucina?', ['luce generale', 'luce funzionale', 'cucina'], ['luce generale', 'luce funzionale']),
    ('predisposizioni-prima-impianto', 'Quando definire l illuminazione della cucina rispetto all impianto elettrico?', ['illuminazione', 'impianto elettrico', 'cucina'], ['impianto elettrico', 'illuminazione']),
    ('lumen-kelvin-cri', 'Lumen Kelvin e CRI: cosa conta davvero per la cucina?', ['lumen', 'kelvin', 'cri'], ['lumen', 'kelvin', 'cri']),
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
    if 'noindex' in raw.lower():
        continue
    if not CANON_RE.search(raw):
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
print('\n=== ILLUMINAZIONE CUCINA: COPERTURA INTENTI ===')

weak = []
for slug, label, terms, signatures in INTENTS:
    ranked = []
    for p in pages:
        th = sum(1 for t in terms if t in p['title'])
        hh = sum(1 for t in terms if t in p['h1'])
        sh = sum(1 for t in terms if t in p['h23'])
        tx = sum(1 for t in terms if t in p['text'])
        signature_structured = any(
            s in p['title'] or s in p['h1'] or s in p['h23']
            for s in signatures
        )
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

print('\n=== PRIORITA CLUSTER ILLUMINAZIONE ===')
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

print('\nAudit Search Everywhere illuminazione cucina completato.')
