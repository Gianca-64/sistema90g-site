#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
SITE='https://sistema90g.it'
OLD_PORTALS=['sistema90g-console.sistema90g.workers.dev','sistema90g-public-requests.sistema90g.workers.dev']
BANNED=['Veneta Cucine','Finiture arredo','Restyling arredo esistente','Redistribuzione interni','Progetto interni da zero','€147','72 ore','5 giorni lavorativi','tre livelli','188 casi']
SERVICE_EXPECTED={
 'controllo-mirato.html':'Controllo mirato',
 'analisi-completa.html':'Analisi completa',
 'progetto-da-zero.html':'Studio preliminare degli spazi',
 'scelta-finiture-casa.html':'Scelta Finiture cucina',
 'restyling-cucina-esistente.html':'Restyling cucina esistente',
 'acquisto-assistito-cucina.html':'Acquisto Assistito Cucina 90G',
 'controllo-progetto-cucina.html':'Verifica professionale progetto cucina',
 'verifica-planimetria-distribuzione-casa.html':'Verifica preliminare dell’immobile',
 'analisi-unita-varianti.html':'Analisi di più unità o varianti',
}
CASE_EXCLUDE={'caso-open-space.html','caso-passaggio-lavastoviglie.html','caso-verificato-isola-forno-passaggi.html'}
COLLECTIONS={'casi-analizzati.html','casi-camere-contenimento.html','casi-cucina.html','casi-distribuzione-casa.html','casi-soggiorno-open-space.html','casi-spazi-servizio.html','servizi.html'}
PRICE_MATRIX={
 'scelta-finiture-cucina':47,'restyling-cucina-esistente':79,'controllo-mirato':127,'analisi-completa':253,'acquisto-assistito-cucina':290,'studio-preliminare-spazi':560,'verifica-preliminare-immobile':149,'analisi-unita-varianti':110,'verifica-progetto-cucina':150
}
issues=[]
htmls=sorted(ROOT.glob('*.html')); indexable=[]; canonicals={}; menus=Counter(); guided_total=guided_complete=0; portal_static=[]
for p in htmls:
 raw=p.read_text('utf-8',errors='replace'); soup=BeautifulSoup(raw,'html.parser')
 robots=soup.find('meta',attrs={'name':'robots'}); idx=not robots or 'noindex' not in (robots.get('content') or '').lower()
 if idx:indexable.append(p)
 if not soup.html or soup.html.get('lang')!='it':issues.append((p.name,'html lang missing/not it'))
 if '€' in raw:issues.append((p.name,'static euro price found; prices must be rendered only at step 3'))
 for old_portal in OLD_PORTALS:
  if old_portal in raw:issues.append((p.name,'obsolete portal endpoint found',old_portal))
 if idx:
  if len(soup.find_all('h1'))!=1:issues.append((p.name,'expected exactly one H1',len(soup.find_all('h1'))))
  if not soup.title or not soup.title.get_text(strip=True):issues.append((p.name,'missing title'))
  for name in ['description','robots','twitter:card','twitter:title','twitter:description','twitter:image']:
   if not soup.find('meta',attrs={'name':name}):issues.append((p.name,'missing meta',name))
  for prop in ['og:title','og:description','og:type','og:url','og:image','og:site_name','og:locale']:
   if not soup.find('meta',attrs={'property':prop}):issues.append((p.name,'missing Open Graph',prop))
  canonical=soup.find('link',rel='canonical')
  if not canonical or not canonical.get('href'):issues.append((p.name,'missing canonical'))
  else:
   if canonical['href'] in canonicals:issues.append((p.name,'duplicate canonical',canonical['href'],canonicals[canonical['href']]))
   canonicals[canonical['href']]=p.name
  schema=soup.find_all('script',type='application/ld+json')
  if len(schema)!=1:issues.append((p.name,'expected one static JSON-LD block',len(schema)))
  else:
   try:
    data=json.loads(schema[0].get_text());graph=data.get('@graph',[]);types=[n.get('@type') for n in graph if isinstance(n,dict)]
    if data.get('@context')!='https://schema.org':issues.append((p.name,'schema context'))
    for required in ['Organization','Person','WebSite']:
     if required not in types:issues.append((p.name,'schema missing',required))
    if not {'WebPage','AboutPage','ContactPage','CollectionPage','CreativeWork'}.intersection(types):issues.append((p.name,'schema missing page entity',types))
    if p.name.startswith('caso-') and p.name not in CASE_EXCLUDE:
     if 'Article' not in types:issues.append((p.name,'case schema missing Article'))
     if 'BreadcrumbList' not in types:issues.append((p.name,'case schema missing BreadcrumbList'))
    if p.name in COLLECTIONS:
     if 'CollectionPage' not in types or 'ItemList' not in types:issues.append((p.name,'collection schema incomplete',types))
    if p.name in SERVICE_EXPECTED:
     services=[n for n in graph if isinstance(n,dict) and n.get('@type')=='Service']
     if len(services)!=1:issues.append((p.name,'expected one Service node',len(services)))
     else:
      if services[0].get('name')!=SERVICE_EXPECTED[p.name]:issues.append((p.name,'wrong service name',services[0].get('name')))
      if 'offers' in services[0]:issues.append((p.name,'price offer must not be exposed in descriptive schema'))
   except Exception as e:issues.append((p.name,'invalid JSON-LD',str(e)))
 nav=soup.select_one('nav.s90g-nav')
 if nav:menus[tuple((a.get('href',''),a.get_text(' ',strip=True)) for a in nav.find_all('a'))]+=1
 for a in soup.find_all('a',href=True):
  href=a['href']
  if a.has_attr('data-start-path'):
   guided_total+=1; req=['data-content-type','data-cta-position','data-service']
   if all(a.has_attr(x) for x in req) and 'analisi-preventiva.html' in href:guided_complete+=1
   else:issues.append((p.name,'guided CTA incomplete',a.get_text(' ',strip=True),href,[x for x in req if not a.has_attr(x)]))
  clean=href.split('#',1)[0].split('?',1)[0]
  if not clean or clean.startswith(('https://','http://','mailto:','tel:','javascript:')) or clean=='#':continue
  if not (ROOT/clean).exists():issues.append((p.name,'broken internal link',href))
 for img in soup.find_all('img'):
  if img.get('alt') is None:issues.append((p.name,'image missing alt',img.get('src')))
  src=(img.get('src') or '').split('?',1)[0]
  if src and not src.startswith(('http://','https://','data:')):
   if not (ROOT/src).exists():issues.append((p.name,'missing local image',src))
   if not img.get('width') or not img.get('height'):issues.append((p.name,'image missing intrinsic dimensions',src))
   if not img.get('loading') or not img.get('decoding'):issues.append((p.name,'image missing loading/decoding hints',src))
 for tag,attr in [('link','href'),('script','src')]:
  for item in soup.find_all(tag):
   val=item.get(attr)
   if not val or val.startswith(('http://','https://','data:')):continue
   clean=val.split('?',1)[0]
   if not (ROOT/clean).exists():issues.append((p.name,f'missing local {tag}',val))
if len(menus)!=1:issues.append(('GLOBAL','multiple navigation variants',[(count,menu) for menu,count in menus.items()]))
for p in list(ROOT.glob('*.html'))+list(ROOT.glob('*.js'))+list(ROOT.glob('*.css')):
 text=p.read_text('utf-8',errors='replace')
 for term in BANNED:
  if term.lower() in text.lower():issues.append((p.name,'banned/outdated commercial term',term))
 for old_portal in OLD_PORTALS:
  if old_portal in text:issues.append((p.name,'obsolete portal endpoint found',old_portal))
# Guided page mechanics
path=soup=BeautifulSoup((ROOT/'analisi-preventiva.html').read_text('utf-8'),'html.parser')
if not soup.find(id='s90g-role-path'):issues.append(('analisi-preventiva.html','guided form missing'))
if not soup.find(id='s90g-result-price'):issues.append(('analisi-preventiva.html','step 3 price output missing'))
if not soup.find('script',src=re.compile('portal-config.js')):issues.append(('analisi-preventiva.html','portal config script missing'))
if not soup.find('script',src=re.compile('role-case-path.js')):issues.append(('analisi-preventiva.html','guided script missing'))
portaljs=(ROOT/'portal-config.js').read_text('utf-8') if (ROOT/'portal-config.js').exists() else ''
if 'enabled: false' not in portaljs:issues.append(('portal-config.js','portal must remain disabled for pre-launch publication'))
if 'https://sistema90g-portale.simply-winspace.it/' not in portaljs:issues.append(('portal-config.js','temporary Register.it trial URL missing'))
rolejs=(ROOT/'role-case-path.js').read_text('utf-8')
for sid,price in PRICE_MATRIX.items():
 if sid not in rolejs or not re.search(rf"(?:price|unitPrice):{price}\b",rolejs):issues.append(('role-case-path.js','approved price missing/wrong',sid,price))
if "minUnits:3" not in rolejs:issues.append(('role-case-path.js','minimum 3 units missing'))
if "requester_role" not in rolejs or "case_context" not in rolejs:issues.append(('role-case-path.js','Console routing parameters missing'))
privacy=(ROOT/'privacy-consent.js').read_text('utf-8')
for token in ['s90gPrepareGuidedPathLinks','guided_path_open','guided_path_result']:
 if token not in privacy:issues.append(('privacy-consent.js','guided path tracking/routing missing',token))
# XML parity
ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}
try:sitemap_urls={e.text.strip() for e in ET.parse(ROOT/'sitemap.xml').findall('.//sm:loc',ns)}
except Exception as e:sitemap_urls=set();issues.append(('sitemap.xml','invalid XML',str(e)))
try:ET.parse(ROOT/'image-sitemap.xml')
except Exception as e:issues.append(('image-sitemap.xml','invalid XML',str(e)))
if sitemap_urls!=set(canonicals):issues.append(('sitemap.xml','parity mismatch',{'missing':sorted(set(canonicals)-sitemap_urls),'extra':sorted(sitemap_urls-set(canonicals))}))
print(f'HTML files: {len(htmls)}');print(f'Indexable pages: {len(indexable)}');print(f'Unique menu variants: {len(menus)}');print(f'Guided CTAs: {guided_complete}/{guided_total} complete');print(f'Issues: {len(issues)}')
for issue in issues:print(' -',issue)
if issues:sys.exit(1)
print('RELEASE AUDIT: PASS')
