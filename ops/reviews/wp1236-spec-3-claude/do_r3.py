import sys, re, json, collections
from pathlib import Path
import yaml
goc=Path('.').resolve()
sys.path.insert(0,str(goc/'ops')); import land_evidence_nguon as L
def norm(k): return ''.join(ch for ch in k.casefold() if ch.isalnum())
def walk(n):
    if isinstance(n,dict):
        for k,v in n.items():
            yield k,v,n
            yield from walk(v)
    elif isinstance(n,list):
        for v in n: yield from walk(v)
tot=0; mc=0; mc40=0; khong=[]
keys=collections.Counter(); keys_all=collections.Counter()
for tep in sorted((goc/'ops/land').glob('*-land-evidence.yaml')):
    tot+=1
    du=L.nap_yaml(yaml, tep.read_bytes())
    if isinstance(du,dict) and 'merge_commit' in du:
        mc+=1
        if isinstance(du['merge_commit'],str) and re.fullmatch(r'[0-9a-f]{40}',du['merge_commit']): mc40+=1
    else: khong.append(tep.name)
    for k,v,m in walk(du):
        if isinstance(k,str) and 'gateoutput' in norm(k): keys[k]+=1
print('tong',tot,'merge_commit goc',mc,'40hex',mc40,'khong:',khong)
print('khoa gateoutput (chuan hoa) trong land-evidence:',dict(keys))
# toan bo yaml duoi ops/land
for p in (goc/'ops/land').rglob('*.y*ml'):
    try: du=yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception: continue
    for k,v,m in walk(du):
        if isinstance(k,str) and 'gateoutput' in norm(k): keys_all[k]+=1
print('khoa gateoutput trong moi yaml ops/land:',dict(keys_all))
