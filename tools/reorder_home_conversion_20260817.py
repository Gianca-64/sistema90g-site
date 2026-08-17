from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "index.html"
s = p.read_text(encoding="utf-8")

# 1) CTA header: più coerente con la nuova architettura a tre percorsi.
s = s.replace(
    '<a class="s90g-header-cta" href="/analisi-preventiva.html#percorso"><span>VALUTA LA TUA CUCINA</span><span>→</span></a>',
    '<a class="s90g-header-cta" href="/analisi-preventiva.html#percorso"><span>TROVA IL TUO PERCORSO</span><span>→</span></a>',
    1,
)

# 2) Sposta il blocco "Tre situazioni, tre percorsi chiari" subito dopo l'hero.
marker = '<h2>Tre situazioni, tre percorsi chiari.</h2>'
pos = s.find(marker)
if pos < 0:
    raise SystemExit('ERRORE: blocco Tre situazioni non trovato.')

section_start = s.rfind('<section class="s90g-section">', 0, pos)
section_end = s.find('</section>', pos)
if section_start < 0 or section_end < 0:
    raise SystemExit('ERRORE: limiti sezione Tre situazioni non trovati.')
section_end += len('</section>')
block = s[section_start:section_end]

# Rimuove il blocco dalla posizione attuale.
s = s[:section_start] + s[section_end:]

# Trova la fine dell'hero e inserisce subito dopo.
hero_pos = s.find('<section class="s90g-hero">')
if hero_pos < 0:
    raise SystemExit('ERRORE: hero non trovato.')
hero_end = s.find('</section>', hero_pos)
if hero_end < 0:
    raise SystemExit('ERRORE: fine hero non trovata.')
hero_end += len('</section>')
s = s[:hero_end] + '\n' + block + s[hero_end:]

p.write_text(s, encoding='utf-8')
print('OK: Home riordinata per conversione.')
print('Ordine iniziale: Hero -> Tre percorsi -> Cosa ricevi -> Obiezione/rivenditore.')
print('CTA header: TROVA IL TUO PERCORSO.')
