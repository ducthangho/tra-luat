"""Đo trên đầu vào đã có; không dựng hồ sơ hay nội dung tấn công."""
from pathlib import Path
import collections
import importlib.util
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[1] / 'repo'
WORK = Path(__file__).resolve().parent
data = json.loads((WORK / 'census.json').read_text())
non_scalar = [u for u in data['unusual'] if u['key'].lower() in ('gate_output', 'moc_gate_output') and isinstance(u['value'], (dict, list))]
print('NON_SCALAR_GATE_KEYS:', len(non_scalar), 'keys in', len({u['file'] for u in non_scalar}), 'records')
for u in non_scalar:
    print(u['file'], u['yaml'], type(u['value']).__name__)

p = ROOT / 'ops/land/pr1231-wp1105-provenance/danh_gia_gate.py'
s = importlib.util.spec_from_file_location('danhgia', p)
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
print('LUAT:', len(m.LUAT), 'job types,', sum(len(xs) for _, xs in m.LUAT), 'steps,', sum(len(ps) for _, xs in m.LUAT for _, ps in xs), 'patterns')
special = collections.Counter(p.split(':', 1)[0] for _, xs in m.LUAT for _, ps in xs for p in ps if p.startswith(('CUOI:', 'KHONG:')) or p == 'JSON_OK')
print('LUAT_SPECIAL:', dict(special))
# Dòng thật từ tệp kết quả đang có, so hai phép khớp trong tiêu chí A5.
txt = (ROOT / 'ops/land/pr1231-wp1105-provenance/danh-gia-gate-output-42032872356.txt').read_text()
line = re.search(r'bundle sha256 = [0-9a-f]{64}', txt).group()
pat = r'^bundle sha256 = [0-9a-f]{64}$'
for label, value in [('full', line), ('cut', line[:70])]:
    print('A5', label, 'fullmatch=', bool(re.fullmatch(pat, value)), 'search=', bool(re.search(pat, value)))
line = re.search(r'cong_cu_test: [^|\n]+', txt).group().strip()
pat = dict(m.LUAT)['gate-cong-cu ('][0][1][0]
print('PREFIX_RULE_ON_REAL_LINE:', repr(pat), 'fullmatch=', bool(re.fullmatch(pat, line)), 'search=', bool(re.search(pat, line)))

for a in data['artifacts']:
    if a['hash_match']:
        h = (ROOT/a['path']).read_text().splitlines()[0]
        d = yaml.safe_load((ROOT/a['hash_match'][0]).read_bytes())
        if d['moc']['run']['head_sha'] not in h:
            print('HASH_MATCH_BUT_NOT_EXACT_HEAD:', a['path'], 'jobs=', a['jobs'], 'header=', h)

for rev in ('936744e', '7f22121'):
    p = WORK/rev/'ops/land/pr1127-wp1120-provenance/ci/gate-output-41356691133.txt'
    jobs = []
    for line in p.read_text().splitlines():
        if line.startswith('JOB '):
            jobs.append([line, 0, 0])
        elif jobs and line.strip():
            jobs[-1][1] += 1
            if line.startswith('    OK  '):
                jobs[-1][2] += 1
    print('HISTORY', rev, 'jobs=', len(jobs), 'empty_total=', sum(n == 0 for _, n, _ in jobs),
          'empty_gate_only=', sum(n == 0 and ' chuan-bi ' not in l for l, n, _ in jobs),
          'gate_ubuntu_OK=', [ok for l, _, ok in jobs if 'gate (ubuntu-latest)' in l])
