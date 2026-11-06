"""K1 + K3 (checkout tung job J) cua r5 tren moi tep provenance that. Chay tu repo: python -I -B ../work/k13_r5.py"""
import yaml, collections
from pathlib import Path
files = []
for p in Path('ops/land').rglob('*.yaml'):
    try: x = yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception: continue
    if isinstance(x, dict) and x.get('schema') == 'ci_provenance/1': files.append((p, x))
print('tep', len(files), 'ho so', len({p.relative_to('ops/land').parts[0] for p, _ in files}))
dem = collections.Counter()
for p, x in sorted(files):
    r = x['moc']['run']
    k1 = (r.get('trang_thai') == 'passed', r.get('repo') == 'ducthangho/tra-luat', r.get('event'))
    dem[('K1', k1)] += 1
    jobs = x['moc']['gate_output']['jobs']
    T = [j for j in jobs if j.get('conclusion') != 'skipped']
    J = [j for j in T if 'ubuntu-latest' in (j.get('labels') or []) and j['name'] != 'chuan-bi']
    co = {}
    for c in x['moc'].get('checkout') or []:
        co.setdefault(c.get('job_id'), []).append(c)
    sha = {c.get('sha') for c in x['moc'].get('checkout') or [] if c.get('trang_thai') == 'passed'}
    thieu = [j['name'] for j in J if not any(c.get('trang_thai') == 'passed' and c.get('sha') in sha and len(sha) == 1 for c in co.get(j.get('job_id') or j.get('id'), []))]
    khoa_id = 'job_id' if 'job_id' in (jobs[0] if jobs else {}) else 'id'
    if r.get('loi_khai_rest_path') == '.github/workflows/ci.yml':
        dem[('ci.yml', r.get('event'), 'J', len(J), 'sha', len(sha), 'job J thieu checkout', len(thieu))] += 1
    cb = [j for j in T if j['name'] == 'chuan-bi']
    for j in cb:
        st = [(b['name'], b['conclusion']) for b in (j.get('buoc') or []) if 'phan loai' in b['name']]
        dem[('chuan-bi buoc phan loai', tuple(st))] += 1
for k, v in sorted(dem.items(), key=str): print(v, k)
print('khoa id job trong gate_output.jobs:', sorted(set().union(*[set(j) for _, x in files for j in x['moc']['gate_output']['jobs']])))
print('khoa checkout:', sorted(set().union(*[set(c) for _, x in files for c in (x['moc'].get('checkout') or [])])))
