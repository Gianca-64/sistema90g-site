#!/usr/bin/env python3

from pathlib import Path
import sys

root = (
    Path(sys.argv[1])
    if len(sys.argv) > 1
    else Path("dist")
)

if not root.is_dir():
    raise SystemExit(
        f"ERRORE: directory pubblica non trovata: {root}"
    )

retired = [
    "professionisti.html",
    "professionisti-progetto-cucina.html",
    "agenzie-immobiliari-cucina.html",
    "rivenditori-cucine.html",
    "controllo-progetto-cucina.html",
]

removed = []

for name in retired:
    path = root / name

    if path.is_file():
        path.unlink()
        removed.append(name)

print(
    "B2B public retirement:",
    len(removed),
    "pagine rimosse dal dist"
)

for name in removed:
    print(" -", name)
