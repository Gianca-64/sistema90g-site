#!/usr/bin/env python3

from pathlib import Path
import sys

root = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else "dist"
)

retired = [
    "seconda-opinione-cucina.html",
    "sviluppo-avanzato-progetto-cucina.html",
    "scelta-finiture-cucina.html",
    "restyling-cucina-esistente.html",
    "acquisto-assistito-cucina.html",
    "controllo-mirato.html",
    "analisi-completa.html",
    "esempio-fascicolo-cucina.html",
]

removed = 0

for name in retired:
    p = root / name

    if p.exists():
        p.unlink()
        removed += 1
        print(
            "RETIRED:",
            name,
        )
    else:
        print(
            "ALREADY ABSENT:",
            name,
        )

print(
    "LEGACY OFFER PAGES REMOVED:",
    removed,
)
