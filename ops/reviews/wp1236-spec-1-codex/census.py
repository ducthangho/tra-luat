import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1] / 'repo'
WORK = Path(__file__).resolve().parent

def module(path, name):
    s = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

nguon = module('ops/land_evidence_nguon.py', 'nguon')
land = module('ops/kiem_ho_so_land.py', 'land')
pos = re.compile(r'^(measured|passed)(?=$|\s|—|-|\(|:)', re.I)

def walk(obj, path='$'):
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f'{path}.{k}'
            yield p, k, v
            yield from walk(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f'{path}[{i}]')

records, unusual, artifacts = [], [], {}
states, prov_count = collections.Counter(), 0
for f in sorted((ROOT / 'ops/land').glob('*-land-evidence.yaml')):
    doc = yaml.safe_load(f.read_bytes())
    stem = f.name.removesuffix('-land-evidence.yaml')
    pd = f.with_name(stem + '-provenance')
    provs = []
    for p in sorted(pd.rglob('provenance.yaml')):
        d = yaml.safe_load(p.read_bytes())
        if isinstance(d, dict) and d.get('schema') == 'ci_provenance/1':
            provs.append((p, d))
            prov_count += 1
            for job in d['moc']['gate_output']['jobs']:
                states[job['trang_thai']] += 1
                if job['trang_thai'] != 'not_measured':
                    print('SPECIAL_STATUS', p.relative_to(ROOT), job['job_id'], job['trang_thai'])
    claims = []
    for path, k, v in walk(doc):
        recognized = isinstance(k, str) and k.casefold() in ('gate_output', 'moc_gate_output') and isinstance(v, str) and pos.match(v.strip())
        if recognized:
            sources = []
            for token in nguon.token_nguon(v):
                p = nguon.phan_giai(token, ROOT, pd, f)
                if p and p.is_file() and p.suffix == '.txt':
                    text = p.read_text(encoding='utf-8', errors='replace')
                    kind = 'danh_gia' if re.search(r'^MOC_GATE_OUTPUT:', text, re.M) else 'tom' if re.search(r'^JOB .* sha256=[0-9a-f]{64} ##\[error\]=', text, re.M) else 'tu_do'
                    job_hashes = dict(re.findall(r'^JOB (\d+) .*?\b(?:log_)?sha256=([0-9a-f]{64})', text, re.M))
                    matches = []
                    for pp, d in provs:
                        logs = {str(j): e['sha256'] for j, e in d['log_day_du'].items()}
                        if job_hashes and job_hashes == logs:
                            matches.append(str(pp.relative_to(ROOT)))
                    a = {'path': str(p.relative_to(ROOT)), 'kind': kind, 'jobs': len(job_hashes), 'hash_match': matches}
                    sources.append(a)
                    artifacts[a['path']] = a
            claims.append({'yaml': path, 'value': v, 'sources': sources})
        if isinstance(k, str) and 'gate_output' in k.casefold() and not recognized:
            unusual.append({'file': f.name, 'yaml': path, 'key': k, 'value': v})
        if isinstance(v, str) and 'gate_output' in v.casefold() and not recognized:
            unusual.append({'file': f.name, 'yaml': path, 'key': k, 'value': v})
    st, _, _ = land._xet_mot_tep(f, yaml)
    records.append({'file': stem, 'land': st, 'provs': [str(p.relative_to(ROOT)) for p, _ in provs], 'claims': claims})

print('TOTAL records=', len(records), 'records_with_provenance=', sum(bool(r['provs']) for r in records), 'provenance_files=', prov_count, 'states=', dict(states))
for group, with_prov in [('A', True), ('B', False)]:
    rows = [r for r in records if bool(r['provs']) == with_prov and r['claims']]
    print('TABLE', group, 'records=', len(rows), 'claims=', sum(len(r['claims']) for r in rows))
    for r in rows:
        kinds = sorted({s['kind'] for c in r['claims'] for s in c['sources']})
        anchored = sum(any(s['hash_match'] for s in c['sources']) for c in r['claims'])
        print(r['file'], r['land'], len(r['claims']), f"{anchored}/{len(r['claims'])}", ','.join(kinds))
for kind in ['danh_gia', 'tom', 'tu_do']:
    rows = [r for r in records if r['provs'] and any(s['kind'] == kind for c in r['claims'] for s in c['sources'])]
    alone = [r for r in rows if {s['kind'] for c in r['claims'] for s in c['sources']} == {kind}]
    print('KIND', kind, 'records=', len(rows), 'only=', len(alone), 'files=', ','.join(r['file'] for r in rows))
print('LANDED_WITHOUT_POSITIVE=', [r['file'] for r in records if r['land'] == 'DAT' and not r['claims']])
print('DANH_GIA_SCRIPTS=', collections.Counter(hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'ops/land').rglob('danh_gia_gate.py')))
for a in artifacts.values():
    if a['kind'] == 'tom':
        p = subprocess.run(['python', '-B', str(ROOT/'ops/land/pr1127-wp1120-provenance/ci/tom_gate_output.py'), 'kiem', str(ROOT/a['path'])], capture_output=True, text=True)
        print('TOM_KIEM', a['path'], 'rc=', p.returncode, p.stdout.strip())
payload = {'records': records, 'unusual': unusual, 'artifacts': list(artifacts.values())}
(WORK/'census.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
