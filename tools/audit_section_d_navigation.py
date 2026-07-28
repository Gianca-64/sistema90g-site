#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from collections import defaultdict, Counter
import argparse, json

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]; self._a=None; self._text=[]; self.robots=''; self.ids=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d: self.ids.append(d['id'])
        if tag=='meta' and d.get('name','').lower()=='robots': self.robots=d.get('content','')
        if tag=='a': self._a=d; self._text=[]
    def handle_data(self,data):
        if self._a is not None: self._text.append(data)
    def handle_endtag(self,tag):
        if tag=='a' and self._a is not None:
            self.links.append((self._a.get('href',''),' '.join(''.join(self._text).split()),self._a))
            self._a=None; self._text=[]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('root',nargs='?',default='.')
    ap.add_argument('--out')
    args=ap.parse_args()
    root=Path(args.root).resolve()
    files=sorted(root.glob('*.html'))+sorted((root/'approfondimenti').glob('*.html'))
    pages={p.relative_to(root).as_posix() for p in files}
    incoming=defaultdict(list); missing=[]; generic=[]; duplicates=[]; records={}
    for p in files:
        rel=p.relative_to(root).as_posix()
        parser=Parser(); parser.feed(p.read_text(encoding='utf-8',errors='ignore')); records[rel]=parser
        dup=[x for x,c in Counter(parser.ids).items() if c>1]
        if dup: duplicates.append({'page':rel,'ids':dup})
        for href,text,attrs in parser.links:
            low=text.lower().replace('→','').strip()
            if low in {'clicca qui','scopri','scopri di più','approfondisci','contattami','richiedi informazioni'} or low.startswith('parliamo del caso'):
                generic.append({'page':rel,'text':text,'href':href})
            if not href or href.startswith(('#','mailto:','tel:','javascript:')): continue
            u=urlsplit(href)
            if u.scheme and u.netloc and u.netloc not in {'sistema90g.it','www.sistema90g.it'}: continue
            path=unquote(u.path)
            base=root if path.startswith('/') or (u.scheme and u.netloc) else p.parent
            path=path.lstrip('/') or 'index.html'
            target=(base/path).resolve()
            try: t=target.relative_to(root).as_posix()
            except ValueError: continue
            if t.endswith('/'): t+='index.html'
            if t.endswith('.html'):
                incoming[t].append({'from':rel,'text':text,'href':href})
                if t not in pages: missing.append({'page':rel,'href':href,'target':t})
    orphans=[]
    for rel,parser in records.items():
        if 'noindex' not in parser.robots.lower() and rel not in {'index.html','404.html'} and not incoming.get(rel):
            orphans.append(rel)
    summary={
        'html_pages':len(files),
        'missing_internal_targets':len(missing),
        'indexable_orphans':len(orphans),
        'generic_cta_labels':len(generic),
        'duplicate_ids':len(duplicates),
        'service_related_sections':sum('data-section-d-related' in p.read_text(errors='ignore') for p in files)
    }
    if args.out:
        out=Path(args.out).resolve(); out.mkdir(parents=True,exist_ok=True)
        for name,data in [('summary.json',summary),('orphans.json',orphans),('missing-links.json',missing),('generic-labels.json',generic),('duplicate-ids.json',duplicates)]:
            (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if missing or orphans or generic or duplicates or summary['service_related_sections']!=9:
        raise SystemExit(1)
if __name__=='__main__': main()
