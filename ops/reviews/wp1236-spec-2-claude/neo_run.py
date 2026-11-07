import sys, re, json
from pathlib import Path
import yaml
sys.path.insert(0,'ops'); import land_evidence_nguon as L
TAP={"passed","measured"}
RE_TOK=re.compile(r"\s*([a-z_]+)(?=$|[\s—\-:(,.;])")
MIEN={"gate_output_nguon","gate_output_nguon_va_gioi_han","moc_gate_output_rc_disposition"}
SHAK=("sha","head_sha","merge_commit")
def walk(n, chain=()):
    if isinstance(n, dict):
        for k,v in n.items():
            yield n, k, v, chain
            yield from walk(v, chain+((n,k),))
    elif isinstance(n, list):
        for i,v in enumerate(n): yield from walk(v, chain+((n,i),))
def prov_runs(gt):
    d=Path('ops/land')/f"{gt}-provenance"; out={}
    if d.is_dir():
        for p in d.rglob('*.yaml'):
            try: x=yaml.safe_load(p.read_text(encoding='utf-8'))
            except Exception: continue
            if isinstance(x,dict) and x.get('schema')=='ci_provenance/1':
                out.setdefault(x['moc']['run']['run_id'],[]).append((str(p), x['moc']['run']['head_sha'], x.get('attempt_yeu_cau')))
    return out
stats={'co_run':0,'thieu':0,'run_khong_co_prov':0,'run_co_prov':0}
for tep in sorted(Path('ops/land').glob('*-land-evidence.yaml')):
    gt=tep.name[:-len('-land-evidence.yaml')]
    du=L.nap_yaml(yaml, tep.read_bytes())
    pr=prov_runs(gt)
    for m,k,v,chain in walk(du):
        if not (isinstance(k,str) and ('gate_output' in k.casefold() or 'gate-output' in k.casefold()) and k not in MIEN): continue
        if not isinstance(v,str): continue
        mm=RE_TOK.match(v.casefold())
        if not mm or mm.group(1) not in TAP: continue
        # mappings: m then ancestors (dicts only) nearest first
        anc=[m]+[c for c,_ in reversed(chain) if isinstance(c,dict) and c is not m]
        rid=None; src=None
        for i,a in enumerate(anc):
            if 'run_id' in a: rid=a['run_id']; src=i; break
        sha=None; ssrc=None
        for i,a in enumerate(anc):
            ks=[x for x in SHAK if x in a]
            if ks: sha={x:a[x] for x in ks}; ssrc=i; break
        path='$'+''.join(f".{c}" if isinstance(c,str) else f"[{c}]" for _,c in chain)+'.'+k
        if rid is None: stats['thieu']+=1
        else:
            stats['co_run']+=1
            if rid in pr: stats['run_co_prov']+=1
            else: stats['run_khong_co_prov']+=1
        provhead = [h for _,h,_ in pr.get(rid,[])] if isinstance(rid,int) else None
        print(f"{gt[:28]:28} {path[:58]:58} run_id={rid!r}@{src} prov={'Y' if rid in pr else 'N'} sha={sha}@{ssrc} provhead={[h[:8] for h in provhead] if provhead else None} runs_in_prov={sorted(pr)}"[:330])
print(stats)
