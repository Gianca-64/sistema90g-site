from pathlib import Path

p = Path('rinnovare-cucina-senza-cambiarla.html')
s = p.read_text()

repls = {
    '<h2>Mantenere la struttura e cambiare solo alcune parti</h2>':
    '<h2>Mantenere la struttura della cucina e cambiare solo alcune parti</h2>',

    '<h2>Maniglie: piccolo intervento, effetto non sempre piccolo</h2>':
    '<h2>Cambiare le maniglie per rinnovare la cucina</h2>',

    '<h2>Top e schienale: attenzione alla compatibilità</h2>':
    '<h2>Rinnovare top e schienale della cucina: attenzione alla compatibilità</h2>',

    '<h2>Una cucina in legno datata va necessariamente eliminata?</h2>':
    '<h2>Come rinnovare una cucina in legno datata senza eliminarne il carattere</h2>',
}

changed = 0
for old, new in repls.items():
    if new in s:
        print('SKIP:', new)
        continue
    if old not in s:
        raise SystemExit(f'Marker non trovato: {old}')
    s = s.replace(old, new, 1)
    changed += 1
    print('OK:', new)

if changed:
    p.write_text(s)

print(f'Search Everywhere: pilastro Restyling rafforzato in {changed} heading semantici.')
