from pathlib import Path
import hashlib
import json
import re
import subprocess

SANDBOX = Path(__file__).resolve().parent.parent
REPO = SANDBOX / 'cay-kho'
BASE = '5f3855eaf47e024b6c63f8923f64d8f80c5de707'
HEAD = '9aa725c72b6b38263de366ce34a80fb384a522a0'
SPEC = 'ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r2.md'
ADR = 'docs/adr/0058-windows-local-han-khoa-va-pham-vi-may.md'
PROTO = 'docs/PROTOCOL_DA_PHIEN.md'
checks = []

def git(*args):
    p = subprocess.run(['git', *args], cwd=REPO, capture_output=True)
    assert p.returncode == 0, (args, p.returncode, p.stderr)
    return p.stdout

def check(name, condition, detail):
    checks.append({'check': name, 'passed': bool(condition), 'detail': detail})
    print(json.dumps(checks[-1], ensure_ascii=False))
    assert condition, name

spec = (REPO / SPEC).read_text()
adr = (REPO / ADR).read_text()
proto = (REPO / PROTO).read_text()
check('head', git('rev-parse', 'HEAD').decode().strip() == HEAD, HEAD)
check('base-is-parent', git('rev-parse', 'HEAD^').decode().strip() == BASE, BASE)
spec_hash = hashlib.sha256((REPO / SPEC).read_bytes()).hexdigest()
check('frozen-spec', spec_hash == '4c92ecbf38fb7f5f97ddea64ed4a43f1cbc9e7a826e87fd8c234dc7e25677c2b', spec_hash)
check('spec-unchanged-from-base', git('show', BASE + ':' + SPEC) == (REPO / SPEC).read_bytes(), SPEC)
actual = git('diff', BASE, HEAD)
check('supplied-diff', actual == (SANDBOX / 'diff.patch').read_bytes(), hashlib.sha256(actual).hexdigest())
numstat = git('diff', '--numstat', BASE, HEAD).decode().splitlines()
stats = [row.split('\t') for row in numstat]
check('write-set', {row[2] for row in stats} == {ADR, PROTO}, numstat)
added = sum(int(row[0]) for row in stats)
check('size', len(stats) <= 2 and added <= 120, {'files': len(stats), 'added': added, 'deleted': sum(int(row[1]) for row in stats)})
old_adr = 'docs/adr/0057-windows-local-may-chu-kho.md'
check('ADR-0057-identical-blob', git('rev-parse', BASE + ':' + old_adr) == git('rev-parse', HEAD + ':' + old_adr), git('rev-parse', HEAD + ':' + old_adr).decode().strip())

def rows(text):
    return {parts[1].strip(): [part.strip() for part in parts[2:-1]]
            for line in text.splitlines()
            if re.match(r'^\| D[789] \|', line)
            for parts in [line.split('|')]}

for label in ['D7', 'D8', 'D9']:
    s = rows(spec)[label]
    a = rows(adr)[label]
    check(label + '-event', s[0] == a[0], a[0])
    # Compare the complete measurement cell, allowing the one non-semantic comma.
    norm = lambda x: re.sub(r'[,\s]+', ' ', x).strip()
    check(label + '-measurement', norm(s[1]) == norm(a[1]), a[1])
    check(label + '-numeric-tokens', re.findall(r'\d+', s[1]) == re.findall(r'\d+', a[1]), re.findall(r'\d+', a[1]))
    check(label + '-quoted-identifiers', re.findall(r'`([^`]+)`', s[1]) == re.findall(r'`([^`]+)`', a[1]), re.findall(r'`([^`]+)`', a[1]))

old = git('show', BASE + ':' + PROTO).decode()
old_pointer = 'Quy ước sử dụng máy Windows local của chủ kho nằm tại `ADR-0057`.'
new_pointer = 'Quy ước sử dụng máy Windows local của chủ kho nằm tại `ADR-0057` và `ADR-0058`.'
check('pointer-location', proto.index('### 10.2 ') < proto.index(new_pointer) < proto.index('## 11. '), 'protocol:1015')
old_row = next(line for line in old.splitlines() if line.startswith('| `ADR-0057` |'))
new_row = next(line for line in proto.splitlines() if line.startswith('| `ADR-0057` |'))
old_cells = old_row.split('|')
new_cells = new_row.split('|')
check('only-ADR-0057-description-cell', all(a == b for i, (a, b) in enumerate(zip(old_cells, new_cells)) if i != 2) and len(old_cells) == len(new_cells) and new_cells[2] == old_cells[2].rstrip() + '; phạm vi và khoá sửa bởi `ADR-0058` ', new_row)
new_adr_rows = [line for line in proto.splitlines() if line.startswith('| `ADR-0058` |')]
check('exactly-one-ADR-0058-row', len(new_adr_rows) == 1, new_adr_rows)
check('ADR-0058-gate-column', new_adr_rows[0].split('|')[4].strip() == 'không cổng — kỷ luật executor', new_adr_rows[0].split('|')[4].strip())
expected = old.replace(old_pointer, new_pointer).replace(old_row, new_row + '\n' + new_adr_rows[0])
check('protocol-only-allowed-edits', proto == expected, 'neutral pointer; ADR-0057 description; one ADR-0058 row')
for short in ['9666771', '10446ff', 'f4d15ed']:
    oid = git('rev-parse', '--verify', short + '^{commit}').decode().strip()
    check('commit-' + short, oid.startswith(short), oid)

output = {'checks': checks, 'passed': len(checks), 'failed': 0}
(SANDBOX / 'evidence' / 'audit_spec.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
print('audit_spec:', len(checks), 'passed, 0 failed')
