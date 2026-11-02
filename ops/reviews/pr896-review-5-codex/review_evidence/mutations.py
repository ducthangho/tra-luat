import json
import os
from pathlib import Path
import re
import subprocess
import yaml

BASE = Path(__file__).resolve().parent
COPY = Path((BASE / 'copy-path.txt').read_text().strip())
SHA = '1a276a15192013fdb1e472db409133b53ac57944'
assert subprocess.check_output(['git', '-C', str(COPY), 'rev-parse', 'HEAD']).decode().strip() == SHA
readme = COPY / 'ops/reviews/README.md'
receipt = COPY / 'ops/reviews/pr526-review-3-codex-verdict.receipt.yaml'
legacy = COPY / 'ops/reviews/pr896-review-4-legacy-caveats.yaml'
originals = {p: p.read_bytes() for p in [readme, receipt, legacy]}
row = next(l for l in readme.read_text().splitlines(keepends=True) if l.startswith('| `pr526-review-3-codex-verdict.md` | `SURFACE-TU-KHAI'))
legacyrow = next(l for l in readme.read_text().splitlines(keepends=True) if l.startswith('| `slice-b-c-review-2-codex-verdict.md` | `SURFACE-TU-KHAI'))
text = receipt.read_text()
node = yaml.compose(text)
v = next(v for k,v in node.value if k.value == 'verdict_usage_caveats')
c = v.value[-1]
start = c.start_mark.index
end = c.end_mark.index
# Remove the caveat including its indentation, retaining a valid empty YAML list.
lines = text.splitlines(keepends=True)
before = ''.join(lines[:c.start_mark.line])
after = ''.join(lines[c.end_mark.line:])
if len(v.value) == 1:
    before = before.replace('verdict_usage_caveats:\n', 'verdict_usage_caveats: []\n')
removed = text[len(before):] if False else ''.join(lines[c.start_mark.line:c.end_mark.line])
legacytext = legacy.read_text()
legacynode = yaml.compose(legacytext)
legacys = next(v for k,v in legacynode.value if k.value == 'caveats')
lc = legacys.value[-1]
llines = legacytext.splitlines(keepends=True)
variants = [
    ('remove-new-pr526-readme-row', readme, readme.read_text().replace(row, '', 1)),
    ('remove-new-pr526-receipt-caveat', receipt, before + after),
    ('remove-new-slice-legacy-readme-row', readme, readme.read_text().replace(legacyrow, '', 1)),
    ('remove-new-slice-supplementary-caveat', legacy, ''.join(llines[:lc.start_mark.line] + llines[lc.end_mark.line:])),
]
results = []
try:
    for name, target, modified in variants:
        for p,data in originals.items():
            p.write_bytes(data)
        target.write_text(modified)
        if target.suffix == '.yaml':
            yaml.safe_load(target.read_text())
        current = []
        for prefix in ['t26_', 't27_', 't138_']:
            cmd = ['python3', 'ops/lease_publish_test.py', '--chi-ca=' + prefix]
            r = subprocess.run(cmd, cwd=COPY, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, capture_output=True, text=True)
            (BASE / (name + '-' + prefix + '.log')).write_text(r.stdout + r.stderr)
            summary = next((l for l in r.stdout.splitlines() if l.startswith('lease_publish:')), 'NO_SUMMARY')
            details = [l for l in r.stdout.splitlines() if any(w in l for w in ['caveat', 'cảnh báo', 'thiếu', 'FAIL', 'TRƯỢT'])]
            current.append({'case': prefix, 'rc': r.returncode, 'summary': summary, 'details': details})
        result = {'mutation': name, 'path': str(target.relative_to(COPY)), 'removed_bytes': len(originals[target]) - len(target.read_bytes()), 'tests': current}
        results.append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
        with (BASE.parent / 'VERDICT.md').open('a') as f:
            f.write('\n- Đột biến clone `' + name + '` ⇒ ' + '; '.join(x['case'] + ' rc' + str(x['rc']) + ' ' + x['summary'] for x in current) + '.\n')
finally:
    for p,data in originals.items():
        p.write_bytes(data)
print('copy_status_after_restore=' + subprocess.check_output(['git', '-C', str(COPY), 'status', '--porcelain=v1']).decode().strip())
(BASE / 'mutations.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
