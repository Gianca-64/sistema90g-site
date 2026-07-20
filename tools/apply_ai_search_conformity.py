#!/usr/bin/env python3
"""Apply SEO / AI-search conformity improvements to the static Sistema 90G site.

The script is intentionally deterministic and only uses facts already visible on each page.
It adds:
- coherent JSON-LD (Organization, WebSite, WebPage, Service, Article, CollectionPage, ItemList, BreadcrumbList);
- social metadata fallbacks;
- image intrinsic dimensions and loading hints;
- semantic breadcrumbs for case pages and case collections.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup, Tag
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://sistema90g.it"
ORG_ID = f"{SITE}/#organization"
WEBSITE_ID = f"{SITE}/#website"
PERSON_ID = f"{SITE}/chi-e-sistema90g.html#person"
TODAY = "2026-07-20"

SERVICE_CONFIG = {
    "controllo-mirato.html": {
        "name": "Controllo mirato",
        "serviceType": "Verifica indipendente di un dubbio circoscritto su progetto, planimetria o preventivo",
        "price": "127",
        "output": "Risposta motivata sul problema concordato, conseguenze, dati mancanti e domande operative.",
        "audience": "Privati e professionisti con un dubbio circoscritto",
    },
    "analisi-completa.html": {
        "name": "Analisi completa",
        "serviceType": "Analisi indipendente di più aspetti collegati di progetto, spazi e preventivo",
        "price": "347",
        "output": "Mappa di criticità, conseguenze, compromessi, priorità, dati mancanti e domande operative.",
        "audience": "Privati e professionisti con un progetto o una proposta articolata",
    },
    "progetto-da-zero.html": {
        "name": "Studio preliminare degli spazi",
        "serviceType": "Studio preliminare delle funzioni e dell'organizzazione degli ambienti",
        "price": "797",
        "output": "Planimetria descrittiva, priorità, vincoli e indicazioni da sviluppare con il professionista incaricato.",
        "audience": "Privati e professionisti che devono impostare uno o più ambienti",
    },
    "scelta-finiture-casa.html": {
        "name": "Scelta Finiture cucina",
        "serviceType": "Confronto indipendente tra un massimo di due combinazioni di finiture cucina",
        "price": "47",
        "output": "Confronto motivato tra due alternative, rapporto con ambiente e luce, indicazione della direzione più equilibrata.",
        "audience": "Clienti con una cucina già impostata e due alternative da confrontare",
    },
    "restyling-cucina-esistente.html": {
        "name": "Restyling cucina esistente",
        "serviceType": "Valutazione preliminare per aggiornare una cucina esistente conservandone una parte",
        "price": "79",
        "output": "Direzione principale di restyling, elementi da conservare o modificare e verifiche da richiedere al fornitore.",
        "audience": "Clienti che vogliono aggiornare una cucina esistente",
    },
    "acquisto-assistito-cucina.html": {
        "name": "Acquisto Assistito Cucina 90G",
        "serviceType": "Sviluppo preliminare indipendente di una cucina nuova prima del progetto commerciale definitivo",
        "price": "390",
        "output": "Proposta funzionale, planimetria, prospetti, visualizzazione tridimensionale, render e fascicolo preliminare da adattare presso il rivenditore scelto.",
        "audience": "Clienti che devono acquistare una cucina nuova",
    },
}

PRO_SERVICE_CONFIG = {
    "agenzie-immobiliari.html": {
        "name": "Supporto Sistema 90G per agenzie immobiliari",
        "serviceType": "Analisi preliminare indipendente di immobili, planimetrie e potenzialità d'uso",
        "audience": "Agenzie immobiliari",
    },
    "rivenditori-cucine.html": {
        "name": "Supporto Sistema 90G per rivenditori di cucine",
        "serviceType": "Sviluppo preliminare indipendente per clienti di rivenditori di cucine",
        "audience": "Rivenditori di cucine e showroom",
    },
}

COLLECTION_PAGES = {
    "casi-analizzati.html": "Casi analizzati Sistema 90G",
    "casi-cucina.html": "Casi cucina e preventivi",
    "casi-soggiorno-open-space.html": "Casi soggiorno e open space",
    "casi-distribuzione-casa.html": "Casi distribuzione e trasformazioni della casa",
    "casi-camere-contenimento.html": "Casi camere, studio e contenimento",
    "casi-spazi-servizio.html": "Casi bagno, lavanderia e spazi di servizio",
}

GENERIC_TYPES = {
    "contatti.html": "ContactPage",
    "privacy-policy.html": "WebPage",
    "cookie-policy.html": "WebPage",
    "analisi-preventiva.html": "WebPage",
    "metodo-sistema90g.html": "AboutPage",
    "professionisti.html": "WebPage",
    "innovazioni.html": "WebPage",
    "esempio-fascicolo-cucina.html": "CreativeWork",
    "servizi.html": "WebPage",
    "analisi-preventivo-cucina.html": "WebPage",
    "controllo-progetto-cucina.html": "WebPage",
    "verifica-planimetria-distribuzione-casa.html": "WebPage",
    "render-fotorealistici-interni.html": "WebPage",
}

CASE_PREFIX = "caso-"
CASE_EXCLUDE = {"caso-open-space.html", "caso-passaggio-lavastoviglie.html", "caso-verificato-isola-forno-passaggi.html"}


def canonical_url(soup: BeautifulSoup, filename: str) -> str:
    tag = soup.find("link", rel=lambda x: x and "canonical" in x)
    if tag and tag.get("href"):
        return tag["href"]
    return f"{SITE}/" if filename == "index.html" else f"{SITE}/{filename}"


def meta_content(soup: BeautifulSoup, key: str, attr: str = "name") -> str:
    tag = soup.find("meta", attrs={attr: key})
    return (tag.get("content") or "").strip() if tag else ""


def title_text(soup: BeautifulSoup) -> str:
    return soup.title.get_text(" ", strip=True) if soup.title else "Sistema 90G"


def h1_text(soup: BeautifulSoup) -> str:
    h1 = soup.find("h1")
    return h1.get_text(" ", strip=True) if h1 else title_text(soup).split("|")[0].strip()


def absolute_image(soup: BeautifulSoup) -> str | None:
    og = meta_content(soup, "og:image", "property")
    if og:
        return og
    img = soup.find("main").find("img") if soup.find("main") and soup.find("main").find("img") else soup.find("img")
    if not img or not img.get("src"):
        return None
    src = img["src"].split("?", 1)[0]
    if src.startswith("http"):
        return src
    return f"{SITE}/{src.lstrip('./')}"


def org_node() -> dict:
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "Sistema 90G",
        "url": f"{SITE}/",
        "logo": {"@type": "ImageObject", "url": f"{SITE}/images/favicon-512.png"},
        "email": "info@sistema90g.it",
        "founder": {"@id": PERSON_ID},
        "areaServed": {"@type": "Country", "name": "Italia"},
    }


def person_node() -> dict:
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": "Gian Carlo Primo",
        "url": f"{SITE}/chi-e-sistema90g.html",
        "jobTitle": "Tecnico indipendente per analisi preventiva di progetti casa e cucina",
        "worksFor": {"@id": ORG_ID},
    }


def webpage_node(soup: BeautifulSoup, filename: str, page_type: str = "WebPage") -> dict:
    url = canonical_url(soup, filename)
    node = {
        "@type": page_type,
        "@id": f"{url}#webpage",
        "url": url,
        "name": title_text(soup),
        "headline": h1_text(soup),
        "description": meta_content(soup, "description"),
        "inLanguage": "it-IT",
        "isPartOf": {"@id": WEBSITE_ID},
        "publisher": {"@id": ORG_ID},
    }
    image = absolute_image(soup)
    if image:
        node["primaryImageOfPage"] = {"@type": "ImageObject", "url": image}
    return node


def website_node() -> dict:
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": f"{SITE}/",
        "name": "Sistema 90G",
        "description": "Analisi preventiva indipendente per progetti, spazi, preventivi e cucine.",
        "inLanguage": "it-IT",
        "publisher": {"@id": ORG_ID},
    }


def service_node(soup: BeautifulSoup, filename: str, cfg: dict, professional: bool = False) -> dict:
    url = canonical_url(soup, filename)
    node = {
        "@type": "Service",
        "@id": f"{url}#service",
        "name": cfg["name"],
        "serviceType": cfg["serviceType"],
        "description": meta_content(soup, "description"),
        "url": url,
        "provider": {"@id": ORG_ID},
        "areaServed": {"@type": "Country", "name": "Italia"},
        "audience": {"@type": "Audience", "audienceType": cfg["audience"]},
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceUrl": "https://sistema90g.it/analisi-preventiva.html#percorso",
            "availableLanguage": "Italiano",
        },
    }
    image = absolute_image(soup)
    if image:
        node["image"] = image
    if cfg.get("output"):
        node["serviceOutput"] = cfg["output"]
    if not professional and cfg.get("price"):
        node["offers"] = {
            "@type": "Offer",
            "url": url,
            "priceCurrency": "EUR",
            "price": cfg["price"],
            "availability": "https://schema.org/LimitedAvailability",
            "seller": {"@id": ORG_ID},
        }
    return node


def visible_breadcrumbs(soup: BeautifulSoup, filename: str) -> list[dict]:
    crumb = soup.select_one(".s90g-breadcrumb .s90g-shell")
    if not crumb:
        return []
    items = []
    position = 1
    for child in crumb.children:
        if isinstance(child, Tag) and child.name == "a" and child.get("href"):
            href = child["href"]
            url = href if href.startswith("http") else (f"{SITE}/" if href == "index.html" else f"{SITE}/{href}")
            items.append({"@type": "ListItem", "position": position, "name": child.get_text(" ", strip=True), "item": url})
            position += 1
        elif isinstance(child, Tag) and child.name == "span":
            items.append({"@type": "ListItem", "position": position, "name": child.get_text(" ", strip=True), "item": canonical_url(soup, filename)})
            position += 1
    return items


def breadcrumb_node(soup: BeautifulSoup, filename: str) -> dict | None:
    items = visible_breadcrumbs(soup, filename)
    if len(items) < 2:
        return None
    return {"@type": "BreadcrumbList", "@id": f"{canonical_url(soup, filename)}#breadcrumb", "itemListElement": items}


def item_list_node(soup: BeautifulSoup, filename: str) -> dict:
    seen = set()
    items = []
    for a in soup.find_all("a", href=True):
        href = a["href"].split("#", 1)[0]
        if not href.startswith(CASE_PREFIX) or not href.endswith(".html") or href in CASE_EXCLUDE or href in seen:
            continue
        target = ROOT / href
        if not target.exists():
            continue
        seen.add(href)
        target_soup = BeautifulSoup(target.read_text("utf-8", errors="replace"), "html.parser")
        items.append({
            "@type": "ListItem",
            "position": len(items) + 1,
            "url": f"{SITE}/{href}",
            "name": h1_text(target_soup),
        })
    return {
        "@type": "ItemList",
        "@id": f"{canonical_url(soup, filename)}#itemlist",
        "name": COLLECTION_PAGES[filename],
        "numberOfItems": len(items),
        "itemListElement": items,
    }


def article_graph(soup: BeautifulSoup, filename: str) -> list[dict]:
    old = None
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.get_text())
            if isinstance(data, dict) and data.get("@type") == "Article":
                old = data
                break
        except Exception:
            pass
    url = canonical_url(soup, filename)
    article = {
        "@type": "Article",
        "@id": f"{url}#article",
        "headline": (old or {}).get("headline") or h1_text(soup),
        "description": (old or {}).get("description") or meta_content(soup, "description"),
        "mainEntityOfPage": {"@id": f"{url}#webpage"},
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": ORG_ID},
        "inLanguage": "it-IT",
        "articleSection": (old or {}).get("articleSection") or "Casi analizzati",
    }
    image = (old or {}).get("image") or absolute_image(soup)
    if image:
        article["image"] = image
    if (old or {}).get("dateModified"):
        article["dateModified"] = old["dateModified"]
    graph = [org_node(), person_node(), website_node(), webpage_node(soup, filename), article]
    breadcrumb = breadcrumb_node(soup, filename)
    if breadcrumb:
        graph.append(breadcrumb)
    return graph


def add_case_breadcrumb_current(soup: BeautifulSoup) -> None:
    crumb_shell = soup.select_one(".s90g-breadcrumb .s90g-shell")
    if not crumb_shell or crumb_shell.find("span", attrs={"aria-current": "page"}):
        return
    crumb_shell.append(" → ")
    span = soup.new_tag("span")
    span["aria-current"] = "page"
    span.string = h1_text(soup)
    crumb_shell.append(span)
    outer = crumb_shell.parent
    if outer and outer.name == "div":
        outer.name = "nav"
        outer["aria-label"] = "Percorso di navigazione"


def add_collection_breadcrumb(soup: BeautifulSoup, filename: str) -> None:
    if soup.select_one(".s90g-breadcrumb"):
        return
    header = soup.find("header")
    main = soup.find("main")
    if not header or not main:
        return
    nav = soup.new_tag("nav")
    nav["class"] = ["s90g-breadcrumb"]
    nav["aria-label"] = "Percorso di navigazione"
    shell = soup.new_tag("div")
    shell["class"] = ["s90g-shell"]
    home = soup.new_tag("a", href="index.html")
    home.string = "Home"
    shell.append(home)
    shell.append(" → ")
    if filename != "casi-analizzati.html":
        cases = soup.new_tag("a", href="casi-analizzati.html")
        cases.string = "Casi analizzati"
        shell.append(cases)
        shell.append(" → ")
    current = soup.new_tag("span")
    current["aria-current"] = "page"
    current.string = h1_text(soup)
    shell.append(current)
    nav.append(shell)
    main.insert(0, nav)


def ensure_meta(soup: BeautifulSoup, attr: str, key: str, content: str) -> None:
    tag = soup.find("meta", attrs={attr: key})
    if not tag:
        tag = soup.new_tag("meta")
        tag[attr] = key
        if soup.head:
            soup.head.append(tag)
    tag["content"] = content


def image_dimensions(img: Tag) -> tuple[int, int] | None:
    src = (img.get("src") or "").split("?", 1)[0]
    if not src or src.startswith("http") or src.startswith("data:"):
        return None
    path = ROOT / src.lstrip("./")
    if not path.exists():
        return None
    try:
        if path.suffix.lower() == ".svg":
            text = path.read_text("utf-8", errors="replace")
            m = re.search(r"viewBox=[\"']\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)[\"']", text, re.I)
            if m:
                return max(1, round(float(m.group(1)))), max(1, round(float(m.group(2))))
            wm = re.search(r"\bwidth=[\"']([\d.]+)", text, re.I)
            hm = re.search(r"\bheight=[\"']([\d.]+)", text, re.I)
            if wm and hm:
                return max(1, round(float(wm.group(1)))), max(1, round(float(hm.group(1))))
            return None
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def improve_images(soup: BeautifulSoup) -> None:
    main = soup.find("main")
    main_images = main.find_all("img") if main else []
    first_content = next((i for i in main_images if i.get("alt", "").strip()), main_images[0] if main_images else None)
    for img in soup.find_all("img"):
        dims = image_dimensions(img)
        if dims:
            img["width"], img["height"] = str(dims[0]), str(dims[1])
        img["decoding"] = "async"
        if img is first_content:
            img["loading"] = "eager"
            img["fetchpriority"] = "high"
        else:
            img["loading"] = "lazy"
            img.attrs.pop("fetchpriority", None)


def set_aria_current(soup: BeautifulSoup, filename: str) -> None:
    nav = soup.select_one("nav.s90g-nav")
    if not nav:
        return
    for a in nav.find_all("a", href=True):
        a.attrs.pop("aria-current", None)
    target = filename
    if filename.startswith(CASE_PREFIX) or filename in COLLECTION_PAGES:
        target = "casi-analizzati.html"
    elif filename in SERVICE_CONFIG or filename in {"analisi-preventivo-cucina.html", "controllo-progetto-cucina.html", "verifica-planimetria-distribuzione-casa.html", "render-fotorealistici-interni.html"}:
        target = "servizi.html"
    elif filename in {"rivenditori-cucine.html", "agenzie-immobiliari.html"}:
        target = "professionisti.html"
    for a in nav.find_all("a", href=True):
        if a["href"].split("#", 1)[0] == target:
            a["aria-current"] = "page"


def build_graph(soup: BeautifulSoup, filename: str) -> list[dict]:
    if filename == "index.html":
        page = webpage_node(soup, filename)
        page["@type"] = "WebPage"
        page["about"] = [
            {"@type": "Thing", "name": "Analisi preventiva di progetti e spazi"},
            {"@type": "Thing", "name": "Cucine e arredamento"},
        ]
        return [org_node(), person_node(), website_node(), page]
    if filename == "chi-e-sistema90g.html":
        page = webpage_node(soup, filename, "AboutPage")
        page["mainEntity"] = {"@id": PERSON_ID}
        person = person_node()
        person["description"] = meta_content(soup, "description")
        image = absolute_image(soup)
        if image:
            person["image"] = image
        return [org_node(), website_node(), person, page]
    if filename in SERVICE_CONFIG:
        page = webpage_node(soup, filename)
        page["mainEntity"] = {"@id": f"{canonical_url(soup, filename)}#service"}
        return [org_node(), person_node(), website_node(), page, service_node(soup, filename, SERVICE_CONFIG[filename])]
    if filename in PRO_SERVICE_CONFIG:
        page = webpage_node(soup, filename)
        page["mainEntity"] = {"@id": f"{canonical_url(soup, filename)}#service"}
        return [org_node(), person_node(), website_node(), page, service_node(soup, filename, PRO_SERVICE_CONFIG[filename], professional=True)]
    if filename in COLLECTION_PAGES:
        page = webpage_node(soup, filename, "CollectionPage")
        page["mainEntity"] = {"@id": f"{canonical_url(soup, filename)}#itemlist"}
        graph = [org_node(), person_node(), website_node(), page, item_list_node(soup, filename)]
        breadcrumb = breadcrumb_node(soup, filename)
        if breadcrumb:
            graph.append(breadcrumb)
        return graph
    if filename.startswith(CASE_PREFIX) and filename not in CASE_EXCLUDE:
        return article_graph(soup, filename)
    if filename == "servizi.html":
        page = webpage_node(soup, filename)
        services = []
        for i, (service_file, cfg) in enumerate(SERVICE_CONFIG.items(), 1):
            services.append({"@type": "ListItem", "position": i, "url": f"{SITE}/{service_file}", "name": cfg["name"]})
        item = {"@type": "ItemList", "@id": f"{canonical_url(soup, filename)}#services", "name": "Servizi Sistema 90G", "numberOfItems": len(services), "itemListElement": services}
        page["mainEntity"] = {"@id": item["@id"]}
        return [org_node(), person_node(), website_node(), page, item]
    page_type = GENERIC_TYPES.get(filename, "WebPage")
    page = webpage_node(soup, filename, page_type)
    if filename == "professionisti.html":
        page["audience"] = [
            {"@type": "ProfessionalAudience", "audienceType": "Architetti e geometri"},
            {"@type": "BusinessAudience", "audienceType": "Rivenditori di cucine e agenzie immobiliari"},
        ]
    if filename == "esempio-fascicolo-cucina.html":
        page["creator"] = {"@id": PERSON_ID}
    return [org_node(), person_node(), website_node(), page]


def is_indexable(soup: BeautifulSoup) -> bool:
    robots = soup.find("meta", attrs={"name": "robots"})
    return not robots or "noindex" not in (robots.get("content") or "").lower()


def main() -> None:
    changed = 0
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text("utf-8", errors="replace")
        soup = BeautifulSoup(text, "html.parser")
        filename = path.name

        if filename.startswith(CASE_PREFIX) and filename not in CASE_EXCLUDE and is_indexable(soup):
            add_case_breadcrumb_current(soup)
        if filename in COLLECTION_PAGES and is_indexable(soup):
            add_collection_breadcrumb(soup, filename)

        improve_images(soup)
        set_aria_current(soup, filename)

        if is_indexable(soup):
            ensure_meta(soup, "property", "og:title", meta_content(soup, "og:title", "property") or title_text(soup))
            ensure_meta(soup, "property", "og:description", meta_content(soup, "og:description", "property") or meta_content(soup, "description"))
            ensure_meta(soup, "property", "og:type", meta_content(soup, "og:type", "property") or ("article" if filename.startswith(CASE_PREFIX) else "website"))
            ensure_meta(soup, "property", "og:url", meta_content(soup, "og:url", "property") or canonical_url(soup, filename))
            fallback_image = absolute_image(soup) or f"{SITE}/images/01_HOME_HERO.jpg"
            ensure_meta(soup, "property", "og:image", meta_content(soup, "og:image", "property") or fallback_image)
            ensure_meta(soup, "property", "og:site_name", "Sistema 90G")
            ensure_meta(soup, "property", "og:locale", "it_IT")
            ensure_meta(soup, "name", "twitter:card", "summary_large_image")
            ensure_meta(soup, "name", "twitter:title", meta_content(soup, "og:title", "property") or title_text(soup))
            ensure_meta(soup, "name", "twitter:description", meta_content(soup, "og:description", "property") or meta_content(soup, "description"))
            image = absolute_image(soup)
            if image:
                ensure_meta(soup, "name", "twitter:image", image)

            for script in soup.find_all("script", type="application/ld+json"):
                script.decompose()
            graph = build_graph(soup, filename)
            ld = soup.new_tag("script")
            ld["type"] = "application/ld+json"
            ld.string = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
            soup.head.append(ld)

        output = str(soup)
        if not output.startswith("<!DOCTYPE"):
            output = "<!DOCTYPE html>\n" + output
        path.write_text(output, "utf-8")
        changed += 1
    print(f"Updated {changed} HTML files")


if __name__ == "__main__":
    main()
