import sys, re, yaml, collections
from pathlib import Path
sys.path.insert(0,'ops'); import land_evidence_nguon as L
RE_TOK=re.compile(r"\s*([a-z_]+)(?=$|[\s—\-:(,.;])")
def norm(k): return ''.join(c for c in k.casefold() if c.isalnum())
PHI={"gateoutputnguon","gateoutputnguonvagioihan","mocgateoutputrcdisposition"}
H40=re.compile(r'[0-9a-f]{40}')
MOC={'run','checkout','workflow_definition','gate_output'}
def walk(n, chain=()):
    if isinstance(n,dict):
        for k,v in n.items():
            yield n,k,v,chain
            yield from walk(v, chain+(n,))
    elif isinstance(n,list):
        for v in n: yield from walk(v, chain)   # list khong phai mapping cha
st=collections.Counter()
for tep in sorted(Path('ops/land').glob('*-land-evidence.yaml')):
    gt=tep.name[:-19]; du=L.nap_yaml(yaml,tep.read_bytes())
    root_mc = du.get('merge_commit') if isinstance(du,dict) else None
    for m,k,v,chain in walk(du):
        if not (isinstance(k,str) and 'gateoutput' in norm(k) and norm(k) not in PHI): continue
        if not isinstance(v,str): continue
        mm=RE_TOK.match(v.casefold())
        if not mm or mm.group(1) not in ('passed','measured','owner_waived'): continue
        neo=None
        if isinstance(m.get('run_id'),int):
            hk=[x for x in ('sha','head_sha','merge_commit') if x in m]
            ra=m.get('run_attempt')
            neo=('r1', m['run_id'], ra, [m[x] for x in hk])
            ok = isinstance(ra,int) and len(hk)==1 and isinstance(m[hk[0]],str) and H40.fullmatch(m[hk[0]])
            land = ok and m[hk[0]]==root_mc
        elif MOC <= set(m):
            cha = chain[-1] if chain else None
            cm = (cha or {}).get('ci_master') if isinstance(cha,dict) else None
            neo=('r2', (cm or {}).get('run_id') if isinstance(cm,dict) else None, (cm or {}).get('run_attempt') if isinstance(cm,dict) else None, (cha or {}).get('merge_commit'))
            ok = isinstance(cm,dict) and isinstance(cm.get('run_id'),int) and isinstance(cm.get('run_attempt'),int) and isinstance(cha.get('merge_commit'),str)
            land = ok and cha.get('merge_commit')==root_mc
        else:
            ok=False; land=False; neo=('thieu_neo',)
        st[(neo[0], 'ok' if ok else 'hong')]+=1
        print(f"{gt[:30]:30} {k:16} {neo[0]:9} ok={bool(ok)} land={bool(land)} neo={neo[1:]}"[:200])
print(dict(st))
