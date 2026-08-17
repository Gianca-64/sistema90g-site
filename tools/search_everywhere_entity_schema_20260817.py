#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ORG_ID = "https://sistema90g.it/#organization"
WEBSITE_ID = "https://sistema90g.it/#website"


def compact(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def replace_jsonld(path, graph):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    pat = re.compile(r'<script type="application/ld\+json">.*?</script>', re.S)
    matches = pat.findall(s)
    if len(matches) != 1:
        raise SystemExit(f"ERRORE {path}: atteso 1 blocco JSON-LD, trovati {len(matches)}")
    block = '<script type="application/ld+json">' + compact({"@context":"https://schema.org","@graph":graph}) + '</script>'
    s = pat.sub(block, s, count=1)
    p.write_text(s, encoding="utf-8")
    print(f"OK schema: {path}")


def insert_after(path, needle, addition, marker):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    if marker in s:
        print(f"SKIP visibile {path}: già presente {marker}")
        return
    if needle not in s:
        raise SystemExit(f"ERRORE {path}: punto inserimento non trovato per {marker}")
    s = s.replace(needle, needle + addition, 1)
    p.write_text(s, encoding="utf-8")
    print(f"OK visibile: {path} -> {marker}")


def insert_before(path, needle, addition, marker):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    if marker in s:
        print(f"SKIP visibile {path}: già presente {marker}")
        return
    if needle not in s:
        raise SystemExit(f"ERRORE {path}: punto inserimento non trovato per {marker}")
    s = s.replace(needle, addition + needle, 1)
    p.write_text(s, encoding="utf-8")
    print(f"OK visibile: {path} -> {marker}")


# ------------------------------------------------------------------
# HOME: completa l'entità canonica con il logo ufficiale del sito.
# ------------------------------------------------------------------
p = ROOT / "index.html"
s = p.read_text(encoding="utf-8")
old = '"email":"info@sistema90g.it","areaServed"'
new = '"email":"info@sistema90g.it","logo":{"@type":"ImageObject","url":"https://sistema90g.it/images/favicon-512.png"},"areaServed"'
if new not in s:
    if old not in s:
        raise SystemExit("ERRORE index.html: Organization canonica non trovata")
    s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8")
    print("OK entity: index.html logo Organization")
else:
    print("SKIP entity: index.html logo già presente")


# ------------------------------------------------------------------
# PROGETTO CUCINA: aggiunge FAQ visibile + graph coerente.
# ------------------------------------------------------------------
project_faq = '''<section class="s90g-section" id="faq-progetto-cucina"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">Domande sul Progetto Cucina</p><h2>Tre chiarimenti prima di configurarlo.</h2></div></div><div class="s90g-offer-grid"><article class="s90g-offer-card"><h3>Quanto costa Progetto Cucina Sistema 90G?</h3><p>Il progetto base costa 145 €. Puoi aggiungere Finiture e materiali a 47 € oppure Sviluppo avanzato a 145 €. Gli add-on estendono lo stesso progetto e non sono servizi separati.</p></article><article class="s90g-offer-card"><h3>Il progetto Sistema 90G sostituisce quello del rivenditore?</h3><p>No. Il rivenditore scelto mantiene rilievo definitivo, verifica di fattibilità, adattamento alla modularità del marchio, preventivo e ordine.</p></article><article class="s90g-offer-card"><h3>Devo scegliere gli add-on?</h3><p>No. Il progetto base da 145 € è completo nel proprio perimetro. Gli add-on servono solo quando vuoi approfondire finiture oppure sviluppare maggiormente visualizzazioni, revisione e fascicolo conclusivo.</p></article></div></div></section>'''
insert_before(
    "progetto-cucina-sistema90g.html",
    '<section class="s90g-final">',
    project_faq,
    'id="faq-progetto-cucina"'
)

project_url = "https://sistema90g.it/progetto-cucina-sistema90g.html"
project_graph = [
    {
        "@type":"Service","@id":project_url+"#service",
        "name":"Progetto Cucina Sistema 90G",
        "serviceType":"Progettazione cucina indipendente prima della scelta del rivenditore",
        "description":"Base progettuale indipendente personalizzabile con add-on per finiture e sviluppo avanzato.",
        "provider":{"@id":ORG_ID},
        "areaServed":{"@type":"Country","name":"Italia"},
        "offers":{"@type":"Offer","price":"145","priceCurrency":"EUR","availability":"https://schema.org/InStock"},
        "url":project_url
    },
    {
        "@type":"WebPage","@id":project_url+"#webpage","url":project_url,
        "name":"Progetto Cucina Sistema 90G | Da 145 € con add-on",
        "description":"Progetto Cucina Sistema 90G: base progettuale indipendente da 145 € prima di scegliere il rivenditore, personalizzabile con add-on per finiture e sviluppo avanzato.",
        "isPartOf":{"@id":WEBSITE_ID},"about":{"@id":ORG_ID},
        "mainEntity":{"@id":project_url+"#service"},
        "breadcrumb":{"@id":project_url+"#breadcrumb"},"inLanguage":"it-IT"
    },
    {
        "@type":"BreadcrumbList","@id":project_url+"#breadcrumb",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":"https://sistema90g.it/"},
            {"@type":"ListItem","position":2,"name":"Servizi","item":"https://sistema90g.it/servizi.html"},
            {"@type":"ListItem","position":3,"name":"Progetto Cucina Sistema 90G","item":project_url}
        ]
    },
    {
        "@type":"FAQPage","@id":project_url+"#faq",
        "mainEntity":[
            {"@type":"Question","name":"Quanto costa Progetto Cucina Sistema 90G?","acceptedAnswer":{"@type":"Answer","text":"Il progetto base costa 145 euro. Puoi aggiungere Finiture e materiali a 47 euro oppure Sviluppo avanzato a 145 euro. Gli add-on estendono lo stesso progetto e non sono servizi separati."}},
            {"@type":"Question","name":"Il progetto Sistema 90G sostituisce quello del rivenditore?","acceptedAnswer":{"@type":"Answer","text":"No. Il rivenditore scelto mantiene rilievo definitivo, verifica di fattibilità, adattamento alla modularità del marchio, preventivo e ordine."}},
            {"@type":"Question","name":"Devo scegliere gli add-on?","acceptedAnswer":{"@type":"Answer","text":"No. Il progetto base da 145 euro è completo nel proprio perimetro. Gli add-on servono solo quando vuoi approfondire finiture oppure sviluppare maggiormente visualizzazioni, revisione e fascicolo conclusivo."}}
        ]
    }
]
replace_jsonld("progetto-cucina-sistema90g.html", project_graph)


# ------------------------------------------------------------------
# SECONDA OPINIONE: breadcrumb visibile + entità collegate.
# ------------------------------------------------------------------
second_url = "https://sistema90g.it/seconda-opinione-cucina.html"
second_hero_end = '</figure></div></section>'
second_breadcrumb = '<div class="s90g-breadcrumb"><div class="s90g-shell"><a href="/">Home</a> → <a href="/servizi.html">Servizi</a> → Seconda Opinione cucina</div></div>'
insert_after("seconda-opinione-cucina.html", second_hero_end, second_breadcrumb, '→ Seconda Opinione cucina</div>')

second_graph = [
    {
        "@type":"Service","@id":second_url+"#service",
        "name":"Seconda Opinione cucina",
        "serviceType":"Controllo indipendente di progetto e preventivo cucina prima dell'ordine",
        "description":"Seconda Opinione indipendente su un dubbio preciso oppure controllo completo di progetto, misure e preventivo cucina prima dell'ordine.",
        "provider":{"@id":ORG_ID},"areaServed":{"@type":"Country","name":"Italia"},"url":second_url
    },
    {
        "@type":"WebPage","@id":second_url+"#webpage","url":second_url,
        "name":"Seconda opinione progetto cucina prima dell'ordine | Sistema 90G",
        "description":"Hai già un progetto o preventivo cucina? Prima dell'ordine puoi richiedere un controllo indipendente: dubbio preciso 127 € oppure controllo completo 253 €.",
        "isPartOf":{"@id":WEBSITE_ID},"about":{"@id":ORG_ID},
        "mainEntity":{"@id":second_url+"#service"},
        "breadcrumb":{"@id":second_url+"#breadcrumb"},"inLanguage":"it-IT"
    },
    {
        "@type":"BreadcrumbList","@id":second_url+"#breadcrumb",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":"https://sistema90g.it/"},
            {"@type":"ListItem","position":2,"name":"Servizi","item":"https://sistema90g.it/servizi.html"},
            {"@type":"ListItem","position":3,"name":"Seconda Opinione cucina","item":second_url}
        ]
    },
    {
        "@type":"FAQPage","@id":second_url+"#faq",
        "mainEntity":[
            {"@type":"Question","name":"Quando serve una seconda opinione sul progetto cucina?","acceptedAnswer":{"@type":"Answer","text":"Quando hai già una proposta o un preventivo e vuoi chiarire un dubbio specifico oppure leggere nel complesso progetto, misure, uso quotidiano e preventivo prima dell'ordine."}},
            {"@type":"Question","name":"Quanto costa controllare un progetto cucina?","acceptedAnswer":{"@type":"Answer","text":"La Seconda Opinione prevede due livelli: dubbio preciso a 127 euro e controllo completo a 253 euro. Entrambi prevedono un tempo standard entro 2 giorni lavorativi dal materiale completo e dalla conferma."}},
            {"@type":"Question","name":"Che cosa posso inviare per il controllo?","acceptedAnswer":{"@type":"Answer","text":"Puoi inviare render, planimetria, misure, prospetti, preventivo e fotografie dell'ambiente. Le informazioni che richiedono rilievo definitivo, verifica tecnica o conferma del rivenditore vengono indicate come punti da verificare con il soggetto competente."}},
            {"@type":"Question","name":"Sistema 90G sostituisce il rivenditore?","acceptedAnswer":{"@type":"Answer","text":"No. Sistema 90G aggiunge una lettura indipendente. Rilievo definitivo, modularità del marchio, fattibilità, preventivo, ordine, montaggio e garanzia restano al rivenditore e agli altri professionisti coinvolti."}}
        ]
    }
]
replace_jsonld("seconda-opinione-cucina.html", second_graph)


# ------------------------------------------------------------------
# RESTYLING: breadcrumb + FAQ visibile + graph completo.
# ------------------------------------------------------------------
rest_url = "https://sistema90g.it/restyling-cucina-esistente.html"
rest_breadcrumb = '<div class="s90g-breadcrumb"><div class="s90g-shell"><a href="/">Home</a> → <a href="/servizi.html">Servizi</a> → Restyling cucina esistente</div></div>'
insert_after("restyling-cucina-esistente.html", second_hero_end, rest_breadcrumb, '→ Restyling cucina esistente</div>')

rest_faq = '''<section class="s90g-section" id="faq-restyling"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">Domande sul Restyling</p><h2>Prima di decidere che cosa cambiare.</h2></div></div><div class="s90g-offer-grid"><article class="s90g-offer-card"><h3>Quando è adatto il Restyling cucina?</h3><p>Quando la cucina è già installata e vuoi aggiornare alcune parti senza ripensare completamente distribuzione, funzioni e impianti.</p></article><article class="s90g-offer-card"><h3>Che materiale devo inviare?</h3><p>Fotografie generali e di dettaglio, misure disponibili, informazioni su marca o modello quando note e indicazione di ciò che vuoi conservare o modificare.</p></article><article class="s90g-offer-card"><h3>Il Restyling comprende rilievo e preventivo?</h3><p>No. Non comprende rilievo, progetto esecutivo, ricerca del fornitore, preventivo, ordine o garanzia sui componenti.</p></article></div></div></section>'''
insert_before("restyling-cucina-esistente.html", '<section class="s90g-final">', rest_faq, 'id="faq-restyling"')

rest_graph = [
    {
        "@type":"Service","@id":rest_url+"#service","name":"Restyling cucina esistente",
        "serviceType":"Valutazione indipendente per aggiornare una cucina esistente",
        "description":"Direzione di restyling per definire elementi da conservare, modificare e verificare con il fornitore.",
        "provider":{"@id":ORG_ID},"areaServed":{"@type":"Country","name":"Italia"},
        "offers":{"@type":"Offer","price":"79","priceCurrency":"EUR","availability":"https://schema.org/InStock"},"url":rest_url
    },
    {
        "@type":"WebPage","@id":rest_url+"#webpage","url":rest_url,
        "name":"Restyling cucina esistente · 79 € | Sistema 90G",
        "description":"Restyling cucina esistente a 79 €: definisci che cosa conservare, che cosa modificare e quali verifiche chiedere al fornitore prima di intervenire.",
        "isPartOf":{"@id":WEBSITE_ID},"about":{"@id":ORG_ID},
        "mainEntity":{"@id":rest_url+"#service"},"breadcrumb":{"@id":rest_url+"#breadcrumb"},"inLanguage":"it-IT"
    },
    {
        "@type":"BreadcrumbList","@id":rest_url+"#breadcrumb",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":"https://sistema90g.it/"},
            {"@type":"ListItem","position":2,"name":"Servizi","item":"https://sistema90g.it/servizi.html"},
            {"@type":"ListItem","position":3,"name":"Restyling cucina esistente","item":rest_url}
        ]
    },
    {
        "@type":"FAQPage","@id":rest_url+"#faq",
        "mainEntity":[
            {"@type":"Question","name":"Quando è adatto il Restyling cucina?","acceptedAnswer":{"@type":"Answer","text":"Quando la cucina è già installata e vuoi aggiornare alcune parti senza ripensare completamente distribuzione, funzioni e impianti."}},
            {"@type":"Question","name":"Che materiale devo inviare?","acceptedAnswer":{"@type":"Answer","text":"Fotografie generali e di dettaglio, misure disponibili, informazioni su marca o modello quando note e indicazione di ciò che vuoi conservare o modificare."}},
            {"@type":"Question","name":"Il Restyling comprende rilievo e preventivo?","acceptedAnswer":{"@type":"Answer","text":"No. Non comprende rilievo, progetto esecutivo, ricerca del fornitore, preventivo, ordine o garanzia sui componenti."}}
        ]
    }
]
replace_jsonld("restyling-cucina-esistente.html", rest_graph)

print("\nSearch Everywhere Entity & Schema completata.")
