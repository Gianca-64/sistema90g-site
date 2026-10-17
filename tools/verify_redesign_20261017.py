#!/usr/bin/env python3
"""Contract for the approved immersive Home and native service disclosures.

Presentation-specific v1 assertions are replaced; global commercial, privacy,
AI search, internationalisation and accessibility build gates remain unchanged.
"""
from pathlib import Path
from html.parser import HTMLParser
import re, sys, json
ROOT=Path(__file__).resolve().parents[1]
page=sys.argv[1]
s=(ROOT/page).read_text()
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.headings=0;self.mains=0;self.links=[];self.images=[]
    def handle_starttag(self,t,a):
        a=dict(a)
        if 'id' in a:self.ids.append(a['id'])
        self.headings+=t=='h1';self.mains+=t=='main'
        if t=='a':self.links.append(a.get('href',''))
        if t=='img':self.images.append(a)
p=Page();p.feed(s)
assert p.headings==1 and p.mains==1, 'One H1 and one main required'
assert len(p.ids)==len(set(p.ids)), 'Duplicate IDs'
assert 'noindex' not in s and 'data:image/' not in s
assert 'rel="canonical"' in s and 'hreflang="en-GB"' in s
assert 'privacy-consent.js' in s
assert '/analisi-preventiva.html#richiedi' in p.links
assert not re.search(r'\bon(?:click|load|change)\s*=',s,re.I)
for block in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S):json.loads(block)
css=(ROOT/'s90g-immersive-20261017.css').read_text()
assert 'prefers-reduced-motion' in css and ':focus-visible' in css
if page=='index.html':
    assert len(re.findall(r'data-index="[012]"',s))==3
    for id in ['stage','closed-photo','photo','intro','story','spots','back','next','esempio']:assert id in p.ids,id
    for text in ['Assistenza indipendente','Scena illustrativa generata','VERIFICATO','DA VERIFICARE','NON DETERMINABILE','Non è un caso cliente','Gian Carlo Primo']:assert text in s,text
    for im in p.images:
        assert im.get('alt') and im.get('width') and im.get('height')
    assert any(i.get('fetchpriority')=='high' for i in p.images)
    js=(ROOT/'s90g-immersive-20261017.js').read_text()
    for marker in ['Escape','preventScroll','aria-expanded','vista90g_hotspot','window.gtag']:assert marker in js
else:
    ids=['scelta','preventivo','verifica','progetto','premontaggio','problema']
    prices=['99','169','199','399','229','199']
    for id,price in zip(ids,prices):
        block=re.search(r'<details id="'+id+r'">(.*?)</details>',s,re.S)
        assert block,id
        for marker in [price+' €','Materiali utili','Confini del servizio','dal materiale completo e dal pagamento.']:assert marker in block[1],(id,marker)
    assert '39 € per vista' in s
    assert 'Percorso Acquisto Cucina 90G' in s
print('PASS — redesign:',page,'semantic structure, content, entry links and accessibility hooks')
