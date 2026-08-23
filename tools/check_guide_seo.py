from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "guide-cucina-sitemap.xml"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

errors = []
warnings = []


def check(pattern, html, label, path):
    if not re.search(pattern, html, flags=re.I | re.S):
        errors.append(f"{path}: manca {label}")


root = ET.parse(SITEMAP).getroot()
urls = [el.text.strip() for el in root.findall("sm:url/sm:loc", NS) if el.text]

for url in urls:
    name = url.rstrip("/").split("/")[-1]
    path = ROOT / name
    if not path.exists():
        errors.append(f"{name}: URL in sitemap ma file assente")
        continue
    html = path.read_text(encoding="utf-8", errors="ignore")
    check(r"<title>[^<]+</title>", html, "title", name)
    check(r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"'][^\"']+[\"']", html, "meta description", name)
    check(r"<link[^>]+rel=[\"']canonical[\"'][^>]+href=[\"']https://sistema90g\.it/[^\"']+[\"']", html, "canonical assoluto", name)
    check(r"<h1[^>]*>.*?</h1>", html, "H1", name)
    if "/analisi-preventiva.html#richiedi" not in html:
        errors.append(f"{name}: manca ingresso Free Entry #richiedi")
    if "/analisi-preventiva.html#percorso" in html:
        errors.append(f"{name}: contiene CTA legacy #percorso")
    if "application/ld+json" not in html:
        warnings.append(f"{name}: schema JSON-LD non ancora presente")

if warnings:
    print("AVVISI SEO:")
    for item in warnings:
        print(f"- {item}")

if errors:
    print("ERRORI SEO:")
    for item in errors:
        print(f"- {item}")
    sys.exit(1)

print(f"SEO guide OK: {len(urls)} pagine controllate")
