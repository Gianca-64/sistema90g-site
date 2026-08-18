from pathlib import Path
from html import unescape
import re

ROOT = Path('.')
DIST = ROOT / 'dist'

INTENTS = [
    ('progetto-prima-showroom', 'Come prepararsi prima di andare in showroom', ['prima del preventivo', 'prima del rivenditore', 'showroom', 'progetto cucina']),
    ('errori-progetto', 'Quali errori controllare nel progetto cucina', ['errori', 'progetto cucina', 'prima dell ordine']),
    ('confronto-preventivi', 'Come confrontare due preventivi cucina', ['confrontare', 'due preventivi', 'preventivo cucina']),
    ('prima-firma', 'Cosa controllare prima di firmare l ordine cucina', ['prima di firmare', 'ordine cucina', 'prima dell ordine']),
    ('voci-escluse', 'Cosa può essere escluso dal preventivo cucina', ['esclusioni', 'voci escluse', 'montaggio', 'allacciamenti']),
    ('rilievo-misure', 'Quando fare il rilievo misure definitivo', ['rilievo misure', 'rilievo', 'misure cucina']),
    ('modifiche-dopo-rilievo', 'Cosa succede se il progetto cambia dopo il rilievo', ['dopo il rilievo', 'modifiche', 'rilievo']),
    ('impianti-prima-ordine', 'Quando definire prese acqua scarichi e impianti', ['prese', 'impianti', 'acqua', 'scarico']),
    ('isola-distanze', 'Quanto spazio serve intorno a un isola cucina', ['isola', 'distanze', 'passaggi']),
    ('penisola-distanze', 'Quanto spazio serve intorno a una penisola cucina', ['penisola', 'distanze', 'passaggi']),
    ('lavastoviglie-passaggio', 'Quanto spazio serve con lavastoviglie aperta', ['lavastoviglie', 'aperture', 'passaggi']),
    ('frigo-parete', 'Quanto spazio serve tra frigorifero e parete', ['frigorifero', 'parete', 'apertura']),
    ('forno-colonna', 'A che altezza mettere forno e microonde', ['forno', 'microonde', 'altezza']),
    ('piano-induzione', 'Cosa verificare prima di scegliere il piano induzione', ['piano', 'induzione', 'impianto elettrico']),
    ('cappa', 'Come scegliere la cappa in base alla cucina reale', ['cappa', 'aspirazione', 'scarico']),
    ('top-materiale', 'Come scegliere il materiale del top cucina', ['top cucina', 'materiale', 'lavorazioni']),
    ('ante-materiale', 'Come scegliere il materiale delle ante cucina', ['ante cucina', 'materiale', 'manutenzione']),
    ('finiture-luce', 'Come scegliere finiture e colori in base alla luce', ['finiture', 'luce', 'pavimento', 'opaca', 'lucida']),
    ('montaggio-allacciamenti', 'Cosa comprende montaggio e chi fa gli allacciamenti', ['montaggio', 'allacciamenti', 'compreso']),
    ('seconda-opinione', 'Quando serve una seconda opinione sulla cucina', ['seconda opinione', 'dubbio concreto', 'prima della decisione']),
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
    title_m = TITLE_RE.search(raw)
    h1_m = H1_RE.search(raw)
    canon_m = CANON_RE.search(raw)
    if not canon_m:
        continue
    title = clean_html(title_m.group(1)) if title_m else ''
    h1 = clean_html(h1_m.group(1)) if h1_m else ''
    text = clean_html(raw)
    pages.append({'file': path.name, 'title': title, 'h1': h1, 'text': text})

print(f'Pagine indicizzabili analizzate: {len(pages)}')
print('\n=== COPERTURA INTENTI AD ALTA INTENZIONE ===')

scores = []
for slug, label, terms in INTENTS:
    ranked = []
    for p in pages:
        title_hits = sum(1 for t in terms if t in p['title'])
        h1_hits = sum(1 for t in terms if t in p['h1'])
        text_hits = sum(1 for t in terms if t in p['text'])
        score = title_hits * 4 + h1_hits * 3 + text_hits
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
    scores.append((status, slug, label, best, ranked[:3]))
    best_txt = f"{best[1]['file']} (score {best[0]})" if best else '—'
    print(f'{status:8} | {label} | {best_txt}')

print('\n=== PRIORITA DI CRESCITA ===')
for status, slug, label, best, ranked in scores:
    if status in {'SCOPERTO', 'DEBOLE', 'PARZIALE'}:
        print(f'[{status}] {label}')
        if ranked:
            for score, p in ranked:
                print(f"  - {p['file']} | score {score} | TITLE: {p['title']}")
        else:
            print('  - nessuna pagina candidata')

print('\n=== INTENTI GIA FORTI ===')
for status, slug, label, best, ranked in scores:
    if status == 'FORTE':
        print(f"- {label} -> {best[1]['file']}")

print('\nAudit gap di crescita Search Everywhere completato.')
