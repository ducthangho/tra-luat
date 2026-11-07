"""Q7 + la_run_land + attempt_yeu_cau tren moi tep provenance that. Chay tu repo: python -I -B ../work/q7_r6.py [ref]"""
import yaml, collections, sys, subprocess
from pathlib import Path
ref = sys.argv[1] if len(sys.argv) > 1 else None
def lay():
    if ref is None:
        for p in Path('ops/land').rglob('*.yaml'):
            yield str(p), p.read_text(encoding='utf-8')
    else:
        ds = subprocess.run(['git', 'ls-tree', '-r', '--name-only', ref, 'ops/land'], capture_output=True, text=True).stdout.split()
        for d in ds:
            if d.endswith('.yaml'):
                yield d, subprocess.run(['git', 'show', f'{ref}:{d}'], capture_output=True, text=True).stdout
files = []
for p, t in lay():
    try: x = yaml.safe_load(t)
    except Exception: continue
    if isinstance(x, dict) and x.get('schema') == 'ci_provenance/1': files.append((p, x))
print('ref', ref, 'tep', len(files), 'ho so', len({p.split('/')[2] for p, _ in files}))
dem = collections.Counter(); win = collections.defaultdict(set); att = collections.Counter()
for p, x in sorted(files):
    r = x['moc']['run']
    jobs = x['moc']['gate_output']['jobs']
    T = [j for j in jobs if j.get('conclusion') != 'skipped']
    labs = collections.Counter(l for j in T for l in (j.get('labels') or []) if 'latest' in l)
    dem[(r.get('loi_khai_rest_path'), r.get('event'), 'T', len(T), tuple(sorted(labs.items())))] += 1
    hs = p.split('/')[2]
    if any('windows' in l for l in labs): win[hs].add((r.get('loi_khai_rest_path').split('/')[-1], r.get('event')))
    att[(type(x.get('attempt_yeu_cau')).__name__, x.get('attempt_yeu_cau') == r.get('run_attempt') if 'run_attempt' in r else 'no run_attempt')] += 1
    la_land = r.get('loi_khai_rest_path') == '.github/workflows/ci.yml' and r.get('event') == 'push'
    dem[('la_run_land', la_land)] += 1
for k, v in sorted(dem.items(), key=str): print(v, k)
print('ho so co job windows:', {k: sorted(v) for k, v in sorted(win.items())})
print('attempt_yeu_cau (kieu, ==moc.run.run_attempt):', dict(att))
print('khoa moc.run:', sorted(set().union(*[set(x['moc']['run']) for _, x in files])))
print('khoa goc:', sorted(set().union(*[set(x) for _, x in files])))
