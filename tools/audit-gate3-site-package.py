#!/usr/bin/env python3
from pathlib import Path

workflow = Path('.github/workflows/gate3-site-isolato.yml').read_text(encoding='utf-8')
doc = Path('docs/GATE3_SITO_ISOLATO_V1.md').read_text(encoding='utf-8')
portal_config = Path('portal-config.js').read_text(encoding='utf-8')

checks = {
    'workflow test portal': 'portale-test.sistema90g.it' in workflow,
    'workflow noindex': 'noindex, nofollow, noarchive' in workflow,
    'workflow robots': 'Disallow: /' in workflow,
    'workflow excludes professional page': 'interesse-professionale.html' in workflow,
    'workflow forbids real data': 'real_data=forbidden' in workflow,
    'workflow forbids public deploy': 'public_deploy=forbidden' in workflow,
    'workflow artifact': 'actions/upload-artifact@v4' in workflow,
    'workflow no remote deploy command': all(
        token not in workflow for token in ('rsync ', 'scp ', 'ssh ', 'ftp ', 'lftp ')
    ),
    'documentation isolation': 'ambiente di collaudo isolato' in doc.lower(),
    'documentation no merge': 'nessun merge' in doc.lower(),
    'documentation no deploy': 'nessun deploy' in doc.lower(),
    'documentation synthetic only': 'richieste sintetiche' in doc.lower(),
    'production config unchanged': "https://portale.sistema90g.it/portal.html" in portal_config,
    'production config not test': 'portale-test.sistema90g.it' not in portal_config,
}

failed = [name for name, passed in checks.items() if not passed]
if failed:
    raise SystemExit('GATE3_SITE_AUDIT_FAILED: ' + ', '.join(failed))

print('GATE3_SITE_PACKAGE_STATIC_OK')
