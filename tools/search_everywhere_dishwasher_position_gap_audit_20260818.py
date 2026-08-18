from pathlib import Path
from html import unescape
import re

DIST = Path('dist')

INTENTS = [
    ('vicino-lavello', 'Dove mettere la lavastoviglie rispetto al lavello?', ['lavastoviglie','lavello'], ['lavastoviglie','lavello']),
    ('destra-sinistra', 'Meglio lavastoviglie a destra o a sinistra del lavello?', ['lavastoviglie','destra','sinistra','lavello'], ['lavastoviglie','lavello']),
    ('vicino-angolo', 'Si può mettere la lavastoviglie vicino a un angolo cucina?', ['lavastoviglie','angolo','cucina'], ['lavastoviglie','angolo']),
    ('sportello-passaggio', 'Cosa succede se lo sportello aperto della lavastoviglie blocca il passaggio?', ['lavastoviglie','sportello','passaggio'], ['lavastoviglie','passaggio']),
    ('vicino-forno', 'Lavastoviglie vicino al forno: cosa verificare?', ['lavastoviglie','forno'], ['lavastoviglie','forno']),
    ('sotto-cottura', 'Si può mettere la lavastoviglie sotto il piano cottura?', ['lavastoviglie','piano cottura'], ['lavastoviglie','piano cottura']),
    ('attacchi-scarico', 'Quanto può essere distante la lavastoviglie da acqua e scarico?', ['lavastoviglie','acqua','scarico'], ['lavastoviglie','scarico']),
    ('carico-scarico', 'Come progettare la zona lavaggio per caricare e scaricare la lavastoviglie comodamente?', ['lavastoviglie','caricare','scaricare','lavello'], ['lavastoviglie','lavello']),
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
print('\n=== POSIZIONE LAVASTOVIGLIE: COPERTURA INTENTI ===')

weak = []
for slug, label, terms, signatures in INTENTS:
    ranked = []
    for p in pages:
        th = sum(1 for t in terms if t in p['title'])
        hh = sum(1 for t in terms if t in p['h1'])
        sh = sum(1 for t in terms if t in p['h23'])
        tx = sum(1 for t in terms if t in p['text'])
        signature_structured = all(s in (p['title'] + ' ' + p['h1'] + ' ' + p['h23']) for s in signatures)
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

print('\n=== PRIORITA CLUSTER POSIZIONE LAVASTOVIGLIE ===')
if not weak:
    print('- Nessun gap forte nel cluster analizzato.')
else:
    for status, label, ranked in weak:
        print(f'[{status}] {label}')
        if ranked:
            for score, structured, p in ranked:
                marker = 'struttura-ok' if structured else 'solo-corpo/parziale'
                print(f"  - {p['file']} | score {score} | {marker} | TITLE: {p['title']}")
        else:
            print('  - nessuna pagina candidata')

print('\nAudit Search Everywhere posizione lavastoviglie completato.')
