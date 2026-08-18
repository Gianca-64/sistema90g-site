from pathlib import Path
from html import unescape
import re

DIST = Path('dist')

INTENTS = [
    ('rivenditore-o-parte', 'Conviene comprare gli elettrodomestici dal rivenditore cucina o a parte?', ['elettrodomestici','rivenditore','parte'], ['rivenditore','parte']),
    ('pacchetto-prezzo', 'Il pacchetto elettrodomestici proposto dal venditore vale il prezzo?', ['pacchetto','elettrodomestici','prezzo'], ['pacchetto','prezzo']),
    ('stesso-modello-online', 'Come confrontare lo stesso elettrodomestico nel preventivo e online?', ['elettrodomestico','preventivo','online'], ['preventivo','online']),
    ('montaggio-responsabilita', 'Se compro gli elettrodomestici a parte, cosa cambia per montaggio e responsabilità?', ['elettrodomestici','montaggio','responsabilita'], ['montaggio','responsabilita']),
    ('prodotti-esterni', 'Il rivenditore può montare elettrodomestici acquistati altrove?', ['rivenditore','montare','altrove'], ['montare','altrove']),
    ('marca-o-modello', 'Conta più la marca o il modello specifico dell elettrodomestico?', ['marca','modello','elettrodomestico'], ['marca','modello']),
    ('pacchetto-stessa-marca', 'Un pacchetto di elettrodomestici della stessa marca è davvero un vantaggio?', ['pacchetto','stessa','marca'], ['pacchetto','marca']),
    ('sovrapprezzo-rivenditore', 'Quando il sovrapprezzo del rivenditore può essere giustificato?', ['sovrapprezzo','rivenditore','giustificato'], ['sovrapprezzo','rivenditore']),
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

pages=[]
for path in sorted(DIST.glob('*.html')):
    raw=path.read_text(errors='ignore')
    if 'noindex' in raw.lower() or not CANON_RE.search(raw):
        continue
    title_m=TITLE_RE.search(raw); h1_m=H1_RE.search(raw)
    h23=' '.join(clean_html(x) for x in H23_RE.findall(raw))
    pages.append({'file':path.name,'title':clean_html(title_m.group(1)) if title_m else '', 'h1':clean_html(h1_m.group(1)) if h1_m else '', 'h23':h23, 'text':clean_html(raw)})

print(f'Pagine indicizzabili analizzate: {len(pages)}')
print('\n=== PACCHETTO ELETTRODOMESTICI / ACQUISTO SEPARATO: COPERTURA INTENTI ===')
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

print('\n=== PRIORITA CLUSTER PACCHETTO ELETTRODOMESTICI ===')
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
print('\nAudit Search Everywhere pacchetto elettrodomestici completato.')
