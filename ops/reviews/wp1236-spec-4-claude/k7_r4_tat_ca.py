import sys, yaml, collections, subprocess
sys.path.insert(0, sys.argv[1]); sys.argv=[sys.argv[0]]
import k7_r4 as K
from pathlib import Path
files=[]
for p in Path('ops/land').rglob('*.yaml'):
    try: x=yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception: continue
    if isinstance(x,dict) and x.get('schema')=='ci_provenance/1': files.append((p,x))
print('tep provenance', len(files), 'ho so', len({p.relative_to('ops/land').parts[0] for p,_ in files}))
ev=collections.Counter((x['moc']['run']['event'], x['moc']['run'].get('loi_khai_rest_path')) for _,x in files); print(dict(ev))
tong=collections.Counter()
for p,x in sorted(files):
    r=x['moc']['run']
    if r.get('loi_khai_rest_path')!='.github/workflows/ci.yml': continue
    sha={c.get('sha') for c in (x['moc'].get('checkout') or []) if c.get('trang_thai')=='passed'}
    if len(sha)!=1: print(p, 'SHA checkout', sha); tong['khong_sha']+=1; continue
    wf=K.wf_tai(next(iter(sha)))
    n,dem,chi=K.k7_run(x,wf)
    loai=collections.Counter()
    for _,l in chi:
        for e in (l if isinstance(l,list) else [l]): loai[e.split(':')[0]]+=1
    ok = dem.get('job_khong_qua',0)==0 and dem.get('khong_luat',0)==0 and n>0
    tong[('qua' if ok else 'truot', r['event'])]+=1
    print(f"{str(p.parent.parent.name if p.parent.name=='ci' else p.parent.name)[:40]:40} {r['event']:17} sha={next(iter(sha))[:7]} J={n:2} {dict(dem)} {dict(loai)}")
print(dict(tong))
