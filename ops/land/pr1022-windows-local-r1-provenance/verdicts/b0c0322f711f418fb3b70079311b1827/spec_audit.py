import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'cay-kho'
BASE = '96667715996d41bc45e70a64fbaa8996de20f6a0'
HEAD = 'fff91390dafb3b8a16e6d11a7243dce036618260'

def git(*args):
    p = subprocess.run(['git', '-C', str(REPO), *args], capture_output=True, text=True)
    assert p.returncode == 0, (args, p.returncode, p.stderr)
    return p.stdout

spec_path = 'ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r1.md'
adr_path = 'docs/adr/0057-windows-local-may-chu-kho.md'
proto_path = 'docs/PROTOCOL_DA_PHIEN.md'
spec = (REPO / spec_path).read_text(encoding='utf-8')
adr = (REPO / adr_path).read_text(encoding='utf-8')
proto = (REPO / proto_path).read_text(encoding='utf-8')
assert git('rev-parse', 'HEAD').strip() == HEAD
assert hashlib.sha256((REPO / spec_path).read_bytes()).hexdigest() == (
    '377ecea689043fcab4d007d65d9592bd28819fa37983796e0c1b75b2c154e715')
assert git('diff', BASE, HEAD).encode() == (ROOT / 'diff.patch').read_bytes()
numstat = [line.split('\t') for line in git('diff', '--numstat', BASE, HEAD).splitlines()]
write_block = re.search(r'\nwrite_set:\n((?:- [^\n]+\n)+)',
                        (ROOT / 'lease.yaml').read_text()).group(1)
write_set = [line[2:] for line in write_block.splitlines()]
assert {row[2] for row in numstat} == set(write_set) == {proto_path, adr_path}
assert len(numstat) <= 2 and sum(int(row[0]) for row in numstat) <= 140

def table(text):
    return {parts[1].strip(): [p.strip() for p in parts[2:-1]]
            for line in text.splitlines()
            if (parts := line.split('|')) and re.match(r'^\| D[1-6] \|', line)}

spec_rows, adr_rows = table(spec), table(adr)
assert set(spec_rows) == set(adr_rows) == {f'D{i}' for i in range(1, 7)}
measurements = []
for key in sorted(spec_rows):
    baseline, candidate = spec_rows[key][1], adr_rows[key][1]
    # Compare every numeric token in the measurement cell; prose is reviewed separately.
    numbers_before, numbers_after = [re.findall(r'\d+(?:[/:.]\d+)*', text)
                                     for text in (baseline, candidate)]
    assert numbers_before == numbers_after, key
    measurements.append({'row': key, 'spec_measurement': baseline,
                         'adr_measurement': candidate, 'numeric_tokens_equal': True})

section20 = proto.split('## 20.', 1)[1]
rows57 = [line for line in section20.splitlines() if line.startswith('| `ADR-0057` |')]
assert len(rows57) == 1
assert rows57[0].split('|')[-2].strip() == 'không cổng — kỷ luật executor'
added = [line[1:] for line in git('diff', '--unified=0', BASE, HEAD, '--', proto_path).splitlines()
         if line.startswith('+') and not line.startswith('+++')]
assert len(added) == 2
pointer = next(line for line in added if not line.startswith('|'))
assert pointer in proto.split('### 10.2 ', 1)[1].split('## 11.', 1)[0]

refs = {}
for sha in ('1cc847d', 'e9967f0'):
    refs[sha] = git('show', '-s', '--format=%H %s', sha).strip()
for pr in ('1010', '1020'):
    refs[f'PR#{pr}'] = git('log', '--all', '--fixed-strings',
                          '--grep=Merge pull request #' + pr + ' ',
                          '--format=%H %s').strip()
    assert refs[f'PR#{pr}']
for name, relative, token in (
    ('t192_S8', 'ops/lease_publish_test.py', 'def t192_S8_'),
    ('c91', 'ops/bien_nhan_v2_test.py', 'def c91_'),
    ('c93', 'ops/bien_nhan_v2_test.py', 'def c93_'),
    ('c96', 'ops/bien_nhan_v2_test.py', 'def c96_'),
    ('r929', '.claude/dev/packet_loop_test.py', 'def _r929_xoa_blob'),
):
    text = (REPO / relative).read_text(encoding='utf-8')
    assert token in text
    refs[name] = relative + ':' + str(text[:text.index(token)].count('\n') + 1)
for heading in ('## 8. ', '#### 10.2.2 ', '#### 10.2.3 '):
    assert heading in proto

gate_paths = ['ops/lease_publish.py', '.claude/dev/packet_loop.py',
              '.claude/dev/launcher.py', '.claude/dev/gate_lifecycle.py',
              '.github/workflows/ci.yml', '.github/workflows/ops-publish-lease.yml']
gate_hits = []
for relative in gate_paths:
    text = (REPO / relative).read_text(encoding='utf-8')
    for token in ('KHOA.txt', 'do-luong.csv', 'list_devices', 'không đo local'):
        if token in text:
            gate_hits.append([relative, token])
assert not gate_hits

report = {'head': HEAD, 'tree': git('rev-parse', 'HEAD^{tree}').strip(),
          'numstat': numstat, 'files': len(numstat),
          'added_lines': sum(int(row[0]) for row in numstat),
          'write_set': write_set, 'measurements': measurements,
          'section20_row_count': len(rows57), 'section20_row': rows57[0],
          'protocol_added_lines': added, 'pointer_line': proto.splitlines().index(pointer) + 1,
          'references_verified_locally': refs, 'gate_paths_scanned': gate_paths,
          'gate_hits': gate_hits,
          'limits': ['Numeric comparison does not prove causality of Windows measurements.',
                     'Frozen spec is the source for D1-D6; Windows logs are not supplied.',
                     'PR #1014, packet #1006, #1017, mission #748 and authority comment '
                     'are not independently read back from GitHub.']}
(ROOT / 'evidence/spec-audit.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: report[k] for k in ('head', 'tree', 'files', 'added_lines',
      'section20_row_count', 'pointer_line', 'gate_hits')}, ensure_ascii=False))
print('D1-D6: 6/6 measurement cells have identical numeric tokens; prose reviewed against frozen spec.')
print('References and gate scan: evidence/spec-audit.json')
