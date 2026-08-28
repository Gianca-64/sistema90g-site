#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

script_re = re.compile(
    r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S,
)


def without_deprecated_faq(data):
    changed = False
    if isinstance(data, dict):
        if data.get('@type') == 'FAQPage':
            return None, True
        if isinstance(data.get('@graph'), list):
            graph = []
            for node in data['@graph']:
                if isinstance(node, dict) and node.get('@type') == 'FAQPage':
                    changed = True
                    continue
                graph.append(node)
            if changed:
                data = dict(data)
                data['@graph'] = graph
    return data, changed

changed_files: list[str] = []
removed = 0
for path in root.rglob('*.html'):
    text = path.read_text('utf-8', errors='strict')
    touched = False

    def repl(match: re.Match[str]) -> str:
        nonlocal_touched = False
        raw = match.group(2).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)
        updated, changed = without_deprecated_faq(data)
        if not changed:
            return match.group(0)
        nonlocal_touched = True
        if updated is None:
            replacement = ''
        else:
            replacement = match.group(1) + json.dumps(updated, ensure_ascii=False, separators=(',', ':')) + match.group(3)
        repl.touched = getattr(repl, 'touched', False) or nonlocal_touched
        repl.removed = getattr(repl, 'removed', 0) + 1
        return replacement

    new_text = script_re.sub(repl, text)
    if getattr(repl, 'touched', False):
        touched = True
        removed += getattr(repl, 'removed', 0)
    if touched:
        path.write_text(new_text, 'utf-8')
        changed_files.append(str(path.relative_to(root)))

print(f'Semantica ricerca normalizzata: FAQPage rimossi {removed} in {len(changed_files)} file')
