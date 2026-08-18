from pathlib import Path
from html import unescape
import re

DIST = Path('dist')

CLUSTERS = {
    'PREVENTIVO / FIRMA': [
        ('preventivo confrontabile', ['preventivo cucina', 'confrontare', 'fornitura equivalente']),
        ('prima della firma', ['prima di firmare', 'ordine cucina']),
        ('esclusioni', ['voci escluse', 'esclusioni', 'allacciamenti']),
    ],
    'RILIEVO / FUORI SQUADRA': [
        ('rilievo definitivo', ['rilievo', 'prima dell ordine', 'misure reali']),
        ('modifiche dopo rilievo', ['dopo il rilievo', 'progetto', 'preventivo']),
        ('fuori squadra', ['fuori squadra', 'pareti', 'top']),
    ],
    'MONTAGGIO / RESPONSABILITA': [
        ('montaggio e allacciamenti', ['montaggio', 'allacciamenti', 'chi fa cosa']),
        ('servizi inclusi', ['trasporto', 'montaggio', 'allacciamenti', 'compresi']),
    ],
    'ELETTRODOMESTICI': [
        ('misure reali incasso', ['misure nominali', 'vano', 'scheda tecnica']),
        ('elettrodomestici nel preventivo', ['marca e modello', 'preventivo', 'elettrodomestici']),
        ('frigorifero vicino parete', ['frigorifero', 'parete', 'cassetti']),
    ],
    'ISOLA / PENISOLA / PASSAGGI': [
        ('isola', ['isola', '90 o 100 cm', 'passaggi']),
        ('penisola', ['penisola', 'sgabelli', 'passaggio']),
        ('lavastoviglie aperta', ['lavastoviglie', 'spazio davanti', 'passaggio']),
        ('tavolo e sedute', ['tavolo', 'dietro una sedia', 'sedute']),
    ],
    'INTERFERENZE SPECIFICHE': [
        ('lavello sotto finestra', ['lavello sotto finestra', 'rubinetto', 'infisso']),
        ('forno microonde colonna', ['forno', 'microonde', 'altezza']),
        ('piano induzione', ['piano a induzione', 'impianto elettrico']),
        ('cappa', ['cappa', 'aspirazione', 'scarico']),
    ],
}

TAG_RE = re.compile(r'<[^>]+>')
SPACE_RE = re.compile(r'\s+')
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.I | re.S)
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
CANON_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', re.I)

def clean(s):
    s = TAG_RE.sub(' ', s)
    return SPACE_RE.sub(' ', unescape(s)).strip().lower()

pages = []
for path in sorted(DIST.glob('*.html')):
    raw = path.read_text(errors='ignore')
    if 'noindex' in raw.lower() or not CANON_RE.search(raw):
        continue
    title = clean(TITLE_RE.search(raw).group(1)) if TITLE_RE.search(raw) else ''
    h1 = clean(H1_RE.search(raw).group(1)) if H1_RE.search(raw) else ''
    pages.append({'file': path.name, 'title': title, 'h1': h1, 'text': clean(raw)})

print(f'Pagine indicizzabili analizzate: {len(pages)}')
print('\n=== COPERTURA PER CLUSTER ===')

cluster_results = []
for cluster, intents in CLUSTERS.items():
    intent_results = []
    for label, terms in intents:
        ranked = []
        for p in pages:
            title_hits = sum(t in p['title'] for t in terms)
            h1_hits = sum(t in p['h1'] for t in terms)
            text_hits = sum(t in p['text'] for t in terms)
            score = title_hits * 4 + h1_hits * 3 + text_hits
            if score:
                ranked.append((score, p['file']))
        ranked.sort(key=lambda x: (-x[0], x[1]))
        best = ranked[0] if ranked else (0, '—')
        status = 'FORTE' if best[0] >= 10 else 'PARZIALE' if best[0] >= 6 else 'DEBOLE' if best[0] > 0 else 'SCOPERTO'
        intent_results.append((status, label, best))
    strong = sum(r[0] == 'FORTE' for r in intent_results)
    partial = sum(r[0] == 'PARZIALE' for r in intent_results)
    weak = sum(r[0] in {'DEBOLE','SCOPERTO'} for r in intent_results)
    cluster_status = 'FORTE' if weak == 0 and partial <= 1 else 'PARZIALE' if weak <= 1 else 'DA SVILUPPARE'
    cluster_results.append((cluster_status, cluster, intent_results))
    print(f'\n{cluster_status} — {cluster}')
    for status, label, best in intent_results:
        print(f'  {status:8} | {label:30} | {best[1]} (score {best[0]})')

print('\n=== PRIORITA RESIDUE ===')
found = False
for cluster_status, cluster, intents in cluster_results:
    for status, label, best in intents:
        if status in {'DEBOLE','SCOPERTO'}:
            found = True
            print(f'- [{status}] {cluster} -> {label} | miglior candidato: {best[1]}')
if not found:
    print('- Nessun gap forte nei cluster analizzati.')

print('\n=== RIEPILOGO CLUSTER ===')
for status, cluster, _ in cluster_results:
    print(f'- {status}: {cluster}')

print('\nAudit cluster Search Everywhere completato.')
