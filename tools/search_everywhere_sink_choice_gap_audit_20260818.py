from pathlib import Path
from html import unescape
import re
import unicodedata

DIST = Path('dist')

INTENTS = [
    ('una-o-due-vasche', 'Meglio lavello cucina a una vasca o due vasche?', ['lavello','una vasca','due vasche'], ['una vasca','due vasche']),
    ('vasca-e-mezza', 'Quando conviene un lavello a una vasca e mezza?', ['lavello','vasca e mezza'], ['vasca e mezza']),
    ('gocciolatoio', 'Serve davvero il gocciolatoio nel lavello cucina?', ['lavello','gocciolatoio'], ['gocciolatoio']),
    ('lavastoviglie', 'Con la lavastoviglie servono ancora due vasche?', ['lavastoviglie','due vasche'], ['lavastoviglie','due vasche']),
    ('piano-lavoro', 'Meglio rinunciare al gocciolatoio per avere più piano di lavoro?', ['gocciolatoio','piano di lavoro'], ['gocciolatoio','piano di lavoro']),
    ('pentole-grandi', 'Una vasca grande è più comoda per pentole e teglie?', ['lavello','vasca grande','pentole'], ['vasca grande','pentole']),
    ('base-mobile', 'Quanto incide la dimensione della base lavello sulla scelta?', ['lavello','base lavello','dimensione'], ['base lavello']),
    ('scelta-uso-reale', 'Come scegliere il lavello in base a uso reale e abitudini?', ['lavello','abitudini','uso'], ['lavello','abitudini']),
]

TAG_RE = re.compile(r'<[^>]+>')
SPACE_RE = re.compile(r'\s+')
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.I | re.S)
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
H23_RE = re.compile(r'<h[23][^>]*>(.*?)</h[23]>', re.I | re.S)
CANON_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', re.I)

def normalize(s):
    s = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in s if not unicodedata.combining(c))

def clean_html(s):
    s = TAG_RE.sub(' ', s)
    s = unescape(s)
    s = normalize(s)
    return SPACE_RE.sub(' ', s).strip().lower()

pages=[]
for path in sorted(DIST.glob('*.html')):
    raw=path.read_text(errors='ignore')
    if 'noindex' in raw.lower() or not CANON_RE.search(raw):
        continue
    title_m=TITLE_RE.search(raw); h1_m=H1_RE.search(raw)
    h23=' '.join(clean_html(x) for x in H23_RE.findall(raw))
    pages.append({'file':path.name,'title':clean_html(title_m.group(1)) if title_m else '', 'h1':clean_html(h1_m.group(1)) if h1_m else '', 'h23':h23, 'text':clean_html(raw)})

print(f'Pagine indicizzabili analizzate: {len(pages)}')
print('\n=== SCELTA LAVELLO CUCINA: COPERTURA INTENTI ===')
weak=[]
for slug,label,terms,signatures in INTENTS:
    ranked=[]
    for p in pages:
        th=sum(1 for t in terms if t in p['title'])
        hh=sum(1 for t in terms if t in p['h1'])
        sh=sum(1 for t in terms if t in p['h23'])
        tx=sum(1 for t in terms if t in p['text'])
        structured=all(any(s in field for field in (p['title'],p['h1'],p['h23'])) for s in signatures)
        score=th*5+hh*4+sh*3+tx
        if score:
            ranked.append((score,structured,p))
    ranked.sort(key=lambda x:(-int(x[1]),-x[0],x[2]['file']))
    best=ranked[0] if ranked else None
    if not best: status='SCOPERTO'
    elif best[1] and best[0]>=12: status='FORTE'
    elif best[0]>=7: status='PARZIALE'
    else: status='DEBOLE'
    best_txt=f"{best[2]['file']} (score {best[0]})" if best else '—'
    print(f'{status:8} | {label} | {best_txt}')
    if status!='FORTE': weak.append((status,label,ranked[:3]))

print('\n=== PRIORITA CLUSTER SCELTA LAVELLO ===')
if not weak:
    print('- Nessun gap forte nel cluster analizzato.')
else:
    for status,label,ranked in weak:
        print(f'[{status}] {label}')
        if ranked:
            for score,structured,p in ranked:
                marker='struttura-ok' if structured else 'solo-corpo/parziale'
                print(f"  - {p['file']} | score {score} | {marker} | TITLE: {p['title']}")
        else:
            print('  - nessuna pagina candidata')
print('\nAudit Search Everywhere scelta lavello completato.')
