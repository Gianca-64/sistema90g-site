from pathlib import Path
from html import unescape
import re

DIST = Path('dist')

# Intenti emersi dalla ricerca esterna sul momento decisionale
# casa in costruzione/ristrutturazione -> progetto cucina -> impianti/tracce.
INTENTS = [
    ('progetto-prima-impianti', 'Devo progettare la cucina prima di fare gli impianti?', ['progettare', 'cucina', 'impianti'], ['impianti']),
    ('quando-iniziare-cucina', 'Quando iniziare a progettare la cucina in costruzione o ristrutturazione?', ['quando', 'progettare', 'cucina'], ['progettare']),
    ('quanto-definitivo-prima-tracce', 'Quanto deve essere definito il progetto prima delle tracce?', ['progetto', 'definito', 'tracce'], ['tracce', 'predisposizioni']),
    ('schema-impianti-cucina', 'Chi prepara lo schema impianti della cucina?', ['schema', 'impianti', 'cucina'], ['schema', 'impianti']),
    ('precisione-prese-scarichi', 'Quanto devono essere precise prese, acqua e scarichi?', ['prese', 'acqua', 'scarichi'], ['prese', 'scarichi']),
    ('impianti-prima-cucina', 'Cosa succede se gli impianti vengono fatti prima del progetto cucina?', ['impianti', 'prima', 'progetto'], ['impianti']),
    ('isola-impianti', 'Isola con acqua o cottura: cosa predisporre prima?', ['isola', 'acqua', 'cottura'], ['isola']),
    ('preliminare-vs-esecutivo', 'Differenza tra progetto preliminare e progetto esecutivo del rivenditore', ['progetto preliminare', 'progetto esecutivo', 'rivenditore'], ['progetto preliminare', 'progetto esecutivo']),
    ('modifiche-dopo-predisposizioni', 'Cosa può ancora cambiare dopo che gli impianti sono predisposti?', ['modifiche', 'impianti', 'predisposizioni'], ['predisposizioni']),
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
print('\n=== PROGETTO PRIMA DEL CANTIERE: COPERTURA INTENTI ===')

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
        # Gli H2/H3 rappresentano sotto-intenti centrali nelle pagine pilastro:
        # un heading che contiene tutti i termini distintivi deve poter raggiungere
        # la soglia FORTE senza costringere title/H1 al keyword stuffing.
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

print('\n=== PRIORITA CLUSTER PRE-CANTIERE ===')
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

print('\nAudit Search Everywhere pre-cantiere completato.')
