from pathlib import Path
import re
from html import unescape
from difflib import SequenceMatcher

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

if not DIST.exists():
    raise SystemExit("ERRORE: dist/ non esiste. Esegui prima bash tools/build_cloudflare.sh")

STOP = {
    'sistema','90g','cucina','cucine','come','cosa','prima','della','delle','degli','dello','del','dei','gli','le','la','il','un','una','e','di','da','in','per','con','su','al','alla','alle','agli','nel','nella','nelle','nei','tra','fra','piu','più','guida'
}

COMMERCIAL = {
    'progetto': '/progetto-cucina-sistema90g.html',
    'seconda': '/seconda-opinione-cucina.html',
    'restyling': '/restyling-cucina-esistente.html',
}

KEY_TERMS = {
    'preventivo': {'preventivo','preventivi','sconto','ordine','firma','offerta','prezzo'},
    'progetto': {'progetto','progettare','progettazione','errori','verifica'},
    'misure-passaggi': {'misure','passaggi','distanze','aperture','ingombri','ergonomia'},
    'isola-penisola': {'isola','penisola','sgabelli','sedute'},
    'elettrodomestici-impianti': {'lavastoviglie','frigorifero','forno','microonde','induzione','cappa','impianti','prese','elettrodomestici'},
    'materiali-finiture': {'materiali','finiture','top','ante','colore','piano'},
    'spazi': {'piccola','angolo','open','space','tavolo','profondita','profondità'},
}


def strip_tags(s):
    s = re.sub(r'<script\b[^>]*>.*?</script>', ' ', s, flags=re.I|re.S)
    s = re.sub(r'<style\b[^>]*>.*?</style>', ' ', s, flags=re.I|re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', unescape(s)).strip()


def first(pattern, s):
    m = re.search(pattern, s, flags=re.I|re.S)
    return strip_tags(m.group(1)) if m else ''


def norm(s):
    s = unescape(s).lower()
    s = re.sub(r'[^a-zàèéìòù0-9]+', ' ', s)
    words = [w for w in s.split() if w not in STOP and len(w) > 2]
    return ' '.join(words)


def tokens(s):
    return set(norm(s).split())

pages = []
for p in sorted(DIST.glob('*.html')):
    text = p.read_text(errors='ignore')
    robots = first(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']*)', text)
    if p.name == '404.html' or 'noindex' in robots.lower():
        continue
    title = first(r'<title>(.*?)</title>', text)
    h1 = first(r'<h1[^>]*>(.*?)</h1>', text)
    desc = first(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', text)
    if not desc:
        desc = first(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']description["\']', text)
    canonical = first(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']*)', text)
    lead = first(r'<p[^>]+class=["\'][^"\']*(?:s90g-lead|intro|s90g-guide__intro)[^"\']*["\'][^>]*>(.*?)</p>', text)
    if not lead:
        lead = first(r'<h1[^>]*>.*?</h1>\s*<p[^>]*>(.*?)</p>', text)
    bodytxt = strip_tags(text)
    page_tokens = tokens(' '.join([title,h1,desc,lead]))
    clusters = [name for name, kws in KEY_TERMS.items() if page_tokens & kws]
    commercial_links = [name for name, url in COMMERCIAL.items() if url in text]
    pages.append({
        'file': p.name, 'title': title, 'h1': h1, 'desc': desc, 'canonical': canonical,
        'lead': lead, 'tokens': page_tokens, 'clusters': clusters,
        'commercial': commercial_links, 'words': len(bodytxt.split())
    })

print(f"Pagine indicizzabili analizzate: {len(pages)}")

print("\n=== PAGINE SENZA COLLEGAMENTO AI 3 PERCORSI ===")
no_com = [x for x in pages if not x['commercial'] and x['file'] not in {'index.html','servizi.html','analisi-preventiva.html','professionisti.html','rivenditori-cucine.html','contatti.html'}]
for x in no_com:
    print(f"{x['file']} | {x['title']}")
if not no_com: print("NESSUNA")

print("\n=== PAGINE MOLTO CORTE (<180 parole) ===")
short = [x for x in pages if x['words'] < 180]
for x in short:
    print(f"{x['words']:>3} | {x['file']} | {x['title']}")
if not short: print("NESSUNA")

print("\n=== POSSIBILI SOVRAPPOSIZIONI TITLE/H1 ===")
pairs = []
for i, a in enumerate(pages):
    for b in pages[i+1:]:
        na = norm(a['title'] + ' ' + a['h1'])
        nb = norm(b['title'] + ' ' + b['h1'])
        if not na or not nb: continue
        jac = len(set(na.split()) & set(nb.split())) / max(1, len(set(na.split()) | set(nb.split())))
        seq = SequenceMatcher(None, na, nb).ratio()
        score = max(jac, seq)
        if score >= 0.72:
            pairs.append((score,a,b))
for score,a,b in sorted(pairs, key=lambda x:x[0], reverse=True):
    print(f"{score:.2f} | {a['file']} <-> {b['file']}")
    print(f"     A: {a['title']} | H1: {a['h1']}")
    print(f"     B: {b['title']} | H1: {b['h1']}")
if not pairs: print("NESSUNA")

print("\n=== CLUSTER AD ALTA DENSITA ===")
for cluster in KEY_TERMS:
    group = [x for x in pages if cluster in x['clusters']]
    if len(group) >= 4:
        print(f"\n[{cluster}] {len(group)} pagine")
        for x in group:
            print(f" - {x['file']} | {x['title']}")

print("\n=== PAGINE COMMERCIALI: COERENZA TITLE/H1 ===")
for fname in ['progetto-cucina-sistema90g.html','seconda-opinione-cucina.html','restyling-cucina-esistente.html']:
    x = next((p for p in pages if p['file']==fname), None)
    if x:
        print(f"{fname}\n  TITLE: {x['title']}\n  H1:    {x['h1']}\n  LEAD:  {x['lead'][:220]}")

print("\nAudit semantico Search Everywhere completato.")
