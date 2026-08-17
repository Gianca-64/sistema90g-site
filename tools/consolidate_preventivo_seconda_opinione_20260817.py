from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = "/seconda-opinione-cucina.html"
LEGACY = "/analisi-preventivo-cucina.html"

# 1) Redirect permanente della vecchia landing commerciale.
redirects = ROOT / "_redirects"
s = redirects.read_text()
rule = f"{LEGACY} {TARGET} 301"
if rule not in s:
    if not s.endswith("\n"):
        s += "\n"
    s += rule + "\n"
    redirects.write_text(s)
    print("OK _redirects: aggiunto 301 analisi preventivo -> Seconda Opinione")
else:
    print("SKIP _redirects: redirect gia presente")

# 2) Rimuove l'URL legacy dalla sitemap principale.
sitemap = ROOT / "sitemap.xml"
s = sitemap.read_text()
old = "  <url><loc>https://sistema90g.it/analisi-preventivo-cucina.html</loc></url>\n"
old2 = "  <url><loc>https://sistema90g.it/analisi-preventivo-cucina.html</loc><lastmod>2026-08-17</lastmod></url>\n"
if old in s:
    s = s.replace(old, "")
elif old2 in s:
    s = s.replace(old2, "")
elif "analisi-preventivo-cucina.html" in s:
    raise SystemExit("ERRORE: formato sitemap inatteso per analisi-preventivo-cucina.html")
sitemap.write_text(s)
print("OK sitemap.xml: rimosso URL legacy")

# 3) Consolida TUTTI i link HTML interni verso la landing ritirata.
changed = []
for p in ROOT.glob("*.html"):
    if p.name == "analisi-preventivo-cucina.html":
        continue
    s = p.read_text()
    original = s
    s = s.replace('href="/analisi-preventivo-cucina.html"', f'href="{TARGET}"')
    s = s.replace('href="analisi-preventivo-cucina.html"', f'href="{TARGET}"')
    if s != original:
        p.write_text(s)
        changed.append(p.name)

# 4) Riallinea la guida principale sul preventivo alla nuova offerta.
p = ROOT / "preventivo-cucina-guida.html"
s = p.read_text()
old_text = "Se vuoi verificare struttura, voci, esclusioni e coerenza dell'offerta, il percorso più diretto è l'<a href=\"/seconda-opinione-cucina.html\">Analisi preventivo cucina</a>. Se vuoi controllare anche il progetto nel suo insieme, valuta l'<a href=\"/analisi-completa.html\">Analisi completa</a>."
new_text = "Se vuoi verificare struttura, voci, esclusioni e coerenza dell'offerta, il percorso commerciale corretto è la <a href=\"/seconda-opinione-cucina.html\">Seconda Opinione</a>: puoi scegliere il livello “dubbio preciso” quando la domanda è circoscritta oppure il “controllo completo” quando preventivo e progetto vanno letti insieme."
if old_text in s:
    s = s.replace(old_text, new_text, 1)
elif "analisi-completa.html" in s:
    s = s.replace('l\'<a href="/analisi-completa.html">Analisi completa</a>', 'la <a href="/seconda-opinione-cucina.html">Seconda Opinione</a>')
p.write_text(s)

print("Link interni aggiornati:", ", ".join(changed) if changed else "nessuno")
print("Consolidamento Analisi preventivo -> Seconda Opinione completato.")
