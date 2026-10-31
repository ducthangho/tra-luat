from pathlib import Path
import re
import yaml

root = Path(__file__).resolve().parents[1] / 'cay-kho'
readme = (root / 'ops/reviews/README.md').read_text()
toc = readme.split('## Mục lục', 1)[1]
caveats = readme.split('## Mục lục', 1)[0]
for n in (1, 2):
    name = f'wp1037-g1-codex-luot{n}-verdict.md'
    receipt_name = name.removesuffix('.md') + '.receipt.yaml'
    receipt = yaml.safe_load((root / 'ops/reviews' / receipt_name).read_text())
    rows = [line for line in toc.splitlines() if line.startswith('|') and f'`{name}`' in line]
    print('ROUND', n, 'TOC_COUNT', len(rows))
    for row in rows:
        print('TOC_ROW', row)
        print('VERDICT_IN_ROW', receipt['verdict'] in row, 'ASSURANCE_IN_ROW', receipt['assurance'] in row, 'SHA_IN_ROW', receipt['reviewed_sha'][:7] in row, 'BYTES_IN_ROW', str(receipt['verdict_bytes']) in row)
        for link in re.findall(r'\]\(([^)]+)\)', row):
            print('LINK', link, 'EXISTS', (root / 'ops/reviews' / link).exists())
    for c in receipt['verdict_usage_caveats']:
        matches = [line for line in caveats.splitlines() if line.startswith('|') and f'`{name}`' in line and f'`{c["id"]}`' in line]
        print('CAVEAT', n, c['id'], 'COUNT', len(matches))
new_files = sorted(p.relative_to(root).as_posix() for p in root.glob('ops/reviews/wp1037*'))
print('NEW_TOP_LEVEL_ENTRIES', new_files)
