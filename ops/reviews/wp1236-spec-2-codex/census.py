import ast
import collections
import hashlib
import importlib.util
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1] / 'repo'
WORK = Path(__file__).resolve().parent
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

nguon = module('nguon', 'ops/land_evidence_nguon.py')
land = module('land', 'ops/kiem_ho_so_land.py')
EXCEPT = {'gate_output_nguon', 'gate_output_nguon_va_gioi_han', 'moc_gate_output_rc_disposition'}
TOKEN = re.compile(r'\s*([a-z_]+)(?=$|[\s—\-:(,.;])')
def walk(x, path='$', parents=()):
    if isinstance(x, dict):
        parents = (x,) + parents
        for k,v in x.items():
            here = path + '.' + str(k)
            if isinstance(k, str) and ('gate_output' in k.casefold() or 'gate-output' in k.casefold()):
                yield here,k,v,parents
            yield from walk(v,here,parents)
    elif isinstance(x,list):
        for i,v in enumerate(x):
            yield from walk(v,path+f'[{i}]',parents)

keys, kinds, states = collections.Counter(), collections.Counter(), collections.Counter()
rows=[]
provs=[]
anchors=[]
for p in sorted((ROOT/'ops/land').glob('*-land-evidence.yaml')):
    data=yaml.safe_load(p.read_bytes())
    entries=list(walk(data))
    claims=[]
    for path,k,v,parents in entries:
        keys[k]+=1
        if k.casefold() in EXCEPT:
            continue
        mat=TOKEN.match(v.casefold()) if isinstance(v,str) else None
        tok=mat[1] if mat else None
        kind=tok if tok in {'passed','measured','not_measured'} else 'chuoi_khac' if isinstance(v,str) else type(v).__name__
        kinds[kind]+=1
        claims.append((path,kind))
        if tok in {'passed','measured'}:
            run=next((a['run_id'] for a in parents if 'run_id' in a),None)
            head=next(({k:a[k] for k in ('sha','head_sha','merge_commit') if k in a} for a in parents if any(k in a for k in ('sha','head_sha','merge_commit'))),None)
            anchors.append({'record':p.name,'path':path,'run':run,'head':head,'value':v})
    pd=p.parent/(p.name.removesuffix('-land-evidence.yaml')+'-provenance')
    pv=[]
    for f in sorted(pd.rglob('*.yaml')):
        try:
            d=yaml.safe_load(f.read_bytes())
        except Exception:
            continue
        if isinstance(d,dict) and d.get('schema')=='ci_provenance/1':
            pv.append(f)
            provs.append((f,d))
            states.update(j['trang_thai'] for j in d['moc']['gate_output']['jobs'])
    l6=land._xet_mot_tep(p,yaml)
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    l5=nguon.MIEN_TRU_CUTOVER.get(p.name)==digest
    rows.append({'record':p.name.removesuffix('-land-evidence.yaml'),'claims':claims,'provenance':len(pv),'l6':l6[0],'landed':l6[2],'l5':l5})

print('RECORDS',len(rows),'PROVENANCE_RECORDS',sum(r['provenance']>0 for r in rows),'PROVENANCE_FILES',len(provs))
print('KEYS',dict(keys))
print('KINDS',dict(kinds))
print('JOB_STATES',dict(states))
with_claim=[r for r in rows if r['claims']]
active=[r for r in with_claim if any(k!='not_measured' for _,k in r['claims'])]
print('CLAIMS_RECORDS',len(with_claim),'ACTIVE_RECORDS',len(active),'ACTIVE_CLAIMS',sum(k!='not_measured' for r in active for _,k in r['claims']))
print('ACTIVE_WITH_PROV',sum(r['provenance']>0 for r in active),'ACTIVE_NO_PROV',sum(r['provenance']==0 for r in active),'ACTIVE_L5',sum(r['l5'] for r in active))
red=[r for r in active if not r['l5']]
print('L8_ROWS',len(red))
spec=(ROOT.parent/'SPEC.md').read_text()
table={p[0]:p for line in spec.splitlines() if line.startswith('| pr') and len(p:=[x.strip() for x in line.strip('|').split('|')])==7}
diff=[]
for r in red:
    row=table.get(r['record'])
    actual=[r['record'],str(r['provenance']),r['l6'],str(len(r['claims'])),', '.join(sorted({k for _,k in r['claims']})), 'ĐỎ','MIỄN']
    if not row or row[:4]!=actual[:4] or set(row[4].replace('chuỗi khác','chuoi_khac').split(', '))!=set(actual[4].split(', ')) or row[5:]!=actual[5:]:
        diff.append({'spec':row,'actual':actual})
print('L8_TABLE_DIFF',diff,'EXTRA_ROWS',sorted(set(table)-{r['record'] for r in red}))
landed=[r for r in rows if r['landed']]
print('L7_LANDED',len(landed),'WITH_CLAIM',sum(bool(r['claims']) for r in landed),'WITHOUT_CLAIM',sum(not r['claims'] for r in landed))
job_set_diff=[]
for f,d in provs:
    ids={str(j['job_id']) for j in d['moc']['gate_output']['jobs'] if j['conclusion']!='skipped'}
    if ids!={str(k) for k in d['log_day_du']}:
        job_set_diff.append(str(f.relative_to(ROOT)))
print('PROVENANCE_JOB_SET_DIFF',job_set_diff)
print('POSITIVE_ANCHORS',len(anchors),'NO_RUN',sum(a['run'] is None for a in anchors),'WITH_HEAD',sum(a['head'] is not None for a in anchors))
for a in anchors:
    if a['run'] is not None:
        print('ANCHOR',a['record'],a['path'],'run=',a['run'],'head=',a['head'])
(WORK/'census.json').write_text(json.dumps({'rows':rows,'anchors':anchors},ensure_ascii=False,indent=2,default=str))
