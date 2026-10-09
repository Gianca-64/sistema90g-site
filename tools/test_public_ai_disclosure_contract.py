#!/usr/bin/env python3
"""Regression: public AI disclosures must match human-approved technical workflow."""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")
required = {
    "metodo-sistema90g.html": ["formulazione linguistica della risposta", "revisionate e approvate dall'operatore", "responsabilità finale"],
    "en/method.html": ["wording of the response", "reviewed and approved", "final responsibility"],
    "proprieta-intellettuale.html": ["formulazione linguistica delle risposte", "revisionate e approvate", "contributo creativo umano"],
    "en/intellectual-property.html": ["wording of responses", "reviewed and approved", "human creative contribution"],
}
obsolete = ["utilizzata solo per produrre immagini", "used only to produce images", "or generate answers for clients"]
errors = []
for rel, phrases in required.items():
    path = root / rel
    if not path.is_file():
        errors.append(f"{rel}: missing")
        continue
    content = path.read_text(encoding="utf-8")
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", content)).lower()
    for phrase in phrases:
        if phrase.lower() not in plain:
            errors.append(f"{rel}: missing {phrase}")
    for phrase in obsolete:
        if phrase.lower() in plain:
            errors.append(f"{rel}: obsolete {phrase}")
if errors:
    print("AI DISCLOSURE CONTRACT: FAIL")
    for error in errors:
        print("FAIL:", error)
    raise SystemExit(1)
print("AI DISCLOSURE CONTRACT: PASS (IT/EN)")
