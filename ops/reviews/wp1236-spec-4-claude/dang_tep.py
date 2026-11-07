import sys, re, json
from pathlib import Path
import yaml
sys.path.insert(0,'ops'); import land_evidence_nguon as L
goc=Path('.').resolve()
hs=json.load(open('/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r4-claude/work/loi_khai_r3.json'))
RE_TOM=re.compile(r"^JOB \S+ .*sha256=[0-9a-f]{64} .*##\[error\]=\d+", re.M)
def dang(p):
    t=p.read_text(encoding='utf-8', errors='replace')
    lines=[l for l in t.splitlines() if l.strip()]
    if lines and lines[-1].startswith('MOC_GATE_OUTPUT:'): return 'danh_gia'
    if RE_TOM.search(t): return 'tom'
    return 'tu_do'
from collections import defaultdict
by=defaultdict(set); files=defaultdict(set)
pos_hs=[]
for h,rows in hs.items():
    tep=goc/'ops/land'/f'{h}-land-evidence.yaml'
    prov=goc/'ops/land'/f'{h}-provenance'
    # has provenance by schema?
    hasp=False
    if prov.is_dir():
        for p in prov.rglob('*.yaml'):
            try: x=yaml.safe_load(p.read_text(encoding='utf-8'))
            except Exception: continue
            if isinstance(x,dict) and x.get('schema')=='ci_provenance/1': hasp=True
    if not hasp: continue
    for path,dg,v in rows:
        if dg not in ('measured','passed'): continue
        pos_hs.append(h)
        for t in L.token_nguon(v):
            p=L.phan_giai(t, goc, prov, tep)
            if p is None: continue
            ps=[p] if p.is_file() else sorted(p.rglob('*'))
            for q in ps:
                if q.is_file() and q.suffix=='.txt':
                    d=dang(q); by[d].add(h); files[d].add(str(q))
print('ho so co prov + loi khai duong:', len(set(pos_hs)))
for d in ('danh_gia','tom','tu_do'):
    only=[h for h in by[d] if all(h not in by[o] for o in by if o!=d)]
    print(d, 'hs', len(by[d]), 'chi dang nay', len(only), 'tep', len(files[d]))
print('tu_do hs:', sorted(by['tu_do']))
print('tom hs:', sorted(by['tom']))
print('danh_gia hs:', sorted(by['danh_gia']))
