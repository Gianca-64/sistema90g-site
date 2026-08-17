from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 1) Consolidamento delle vecchie pagine commerciali nella nuova Seconda Opinione.
redirects = ROOT / '_redirects'
s = redirects.read_text(encoding='utf-8')
lines = [
    '/controllo-mirato.html /seconda-opinione-cucina.html 301',
    '/analisi-completa.html /seconda-opinione-cucina.html 301',
]
for line in lines:
    if line not in s:
        s = s.rstrip() + '\n' + line + '\n'
redirects.write_text(s, encoding='utf-8')
print('OK _redirects: consolidate le due vecchie landing nella Seconda Opinione.')

# 2) Sitemap: solo URL commerciali canonici e date aggiornate per le pagine appena riviste.
sitemap = ROOT / 'sitemap.xml'
s = sitemap.read_text(encoding='utf-8')
for legacy in [
    '  <url><loc>https://sistema90g.it/analisi-completa.html</loc></url>\n',
    '  <url><loc>https://sistema90g.it/controllo-mirato.html</loc></url>\n',
]:
    s = s.replace(legacy, '')

updates = {
    '<url><loc>https://sistema90g.it/</loc><lastmod>2026-08-16</lastmod></url>':
    '<url><loc>https://sistema90g.it/</loc><lastmod>2026-08-17</lastmod></url>',
    '<url><loc>https://sistema90g.it/servizi.html</loc><lastmod>2026-08-16</lastmod></url>':
    '<url><loc>https://sistema90g.it/servizi.html</loc><lastmod>2026-08-17</lastmod></url>',
    '<url><loc>https://sistema90g.it/analisi-preventiva.html</loc><lastmod>2026-08-16</lastmod></url>':
    '<url><loc>https://sistema90g.it/analisi-preventiva.html</loc><lastmod>2026-08-17</lastmod></url>',
    '<url><loc>https://sistema90g.it/seconda-opinione-cucina.html</loc><lastmod>2026-08-16</lastmod></url>':
    '<url><loc>https://sistema90g.it/seconda-opinione-cucina.html</loc><lastmod>2026-08-17</lastmod></url>',
    '<url><loc>https://sistema90g.it/restyling-cucina-esistente.html</loc></url>':
    '<url><loc>https://sistema90g.it/restyling-cucina-esistente.html</loc><lastmod>2026-08-17</lastmod></url>',
}
for old, new in updates.items():
    s = s.replace(old, new)
sitemap.write_text(s, encoding='utf-8')
print('OK sitemap.xml: rimossi URL legacy e aggiornati lastmod delle pagine chiave.')

# 3) ChatGPT Search: rende esplicito l'accesso di OAI-SearchBot.
robots = ROOT / 'robots.txt'
s = robots.read_text(encoding='utf-8')
block = 'User-agent: OAI-SearchBot\nAllow: /\n\n'
if 'User-agent: OAI-SearchBot' not in s:
    s = block + s
robots.write_text(s, encoding='utf-8')
print('OK robots.txt: OAI-SearchBot esplicitamente autorizzato.')

print('\nSearch Everywhere foundation completata.')
