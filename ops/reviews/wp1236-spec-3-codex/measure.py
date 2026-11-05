import ast
import collections
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE / 'repo'
WORK = BASE / 'work'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def snapshot():
    result = {}
    for p in sorted(ROOT.rglob('*')):
        if p.is_file():
            result[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result

if sys.argv[1] in ('before', 'after'):
    current = snapshot()
    if sys.argv[1] == 'before':
        (WORK / 'snapshot.json').write_text(json.dumps(current))
        print('snapshot files:', len(current))
    else:
        old = json.loads((WORK / 'snapshot.json').read_text())
        print('snapshot files:', len(current), 'delta:', [p for p in sorted(set(old)|set(current)) if old.get(p) != current.get(p)])
    sys.exit(0)

import yaml
ng = load('nguon', ROOT / 'ops/land_evidence_nguon.py')
ld = load('land', ROOT / 'ops/kiem_ho_so_land.py')
cp = load('ci_provenance', ROOT / 'ops/ci_provenance.py')

def visit(node, path='$'):
    if isinstance(node, dict):
        for k, v in node.items():
            yield path, k, v, node
            yield from visit(v, path + '.' + str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from visit(v, path + f'[{i}]')

def norm(k):
    return ''.join(c for c in str(k).casefold() if c.isalnum())

skip = {'gateoutputnguon', 'gateoutputnguonvagioihan', 'mocgateoutputrcdisposition'}
def kind(v):
    if isinstance(v, dict): return 'mapping'
    if isinstance(v, list): return 'list'
    if isinstance(v, str):
        m = re.match(r'\s*([a-z_]+)(?=$|[\s—\-:(,.;])', v.casefold())
        return m[1] if m and m[1] in {'measured','passed','not_measured'} else 'chuoi_khac'
    return type(v).__name__

if sys.argv[1] == 'census':
    print('time:', datetime.datetime.now(datetime.timezone.utc).isoformat())
    files = sorted((ROOT / 'ops/land').glob('*-land-evidence.yaml'))
    keys, forms = collections.Counter(), collections.Counter()
    claims, nonnm, exempt, l8, landed, withprov, provs, extra, merge = [], [], [], [], [], [], [], [], []
    rows = []
    styles = collections.defaultdict(set)
    stylepaths = collections.defaultdict(list)
    for p in files:
        doc = yaml.safe_load(p.read_bytes())
        if 'merge_commit' in doc: merge.append(p.name)
        entries = list(visit(doc))
        found = [(pa,k,v,m) for pa,k,v,m in entries if 'gateoutput' in norm(k) and norm(k) not in skip]
        for pa,k,v,m in entries:
            if 'gate_output' in str(k).casefold(): keys[k] += 1
            if 'gateoutput' in norm(k) and 'gate_output' not in str(k).casefold(): extra.append((p.name,pa,k))
        for pa,k,v,m in found: forms[kind(v)] += 1
        if found: claims.append(p.name)
        significant = [x for x in found if kind(x[2]) != 'not_measured']
        if significant: nonnm.append(p.name)
        matched = ng.MIEN_TRU_CUTOVER.get(p.name) == hashlib.sha256(p.read_bytes()).hexdigest()
        if significant and p.name in ng.MIEN_TRU_CUTOVER:
            exempt.append((p.name, matched))
        if significant and not matched: l8.append(p.name)
        pd = p.with_name(p.name.removesuffix('-land-evidence.yaml')+'-provenance')
        plist = []
        for q in sorted(pd.rglob('*.yaml')):
            qd = yaml.safe_load(q.read_bytes())
            if isinstance(qd, dict) and qd.get('schema') == 'ci_provenance/1':
                plist.append((q,qd))
        if plist: withprov.append(p.name)
        provs += plist
        outcome = ld._xet_mot_tep(p, yaml)
        if outcome[2]: landed.append((p.name,bool(found)))
        if significant and not matched:
            rows.append((p.name.removesuffix('-land-evidence.yaml'),len(plist),outcome[0],len(found),sorted({kind(x[2]) for x in found})))
        if plist and significant:
            for pa,k,v,m in found:
                if not isinstance(v,str) or kind(v) not in ('measured','passed'): continue
                for token in ng.token_nguon(v):
                    q = ng.phan_giai(token, ROOT, pd, p)
                    if not q or q.suffix != '.txt' or 'gate' not in q.name or 'phan-chung' in q.name: continue
                    text = q.read_text()
                    style = ('danh_gia' if re.search(r'^MOC_GATE_OUTPUT:',text,re.M) else 'tom' if re.search(r'^JOB .*sha256=[0-9a-f]{64} ##\[error\]=',text,re.M) else 'tu_do')
                    styles[p.name].add(style)
                    stylepaths[p.name].append((style,str(q.relative_to(ROOT))))
    print('files:',len(files),'keys:',dict(keys),'forms:',dict(forms),'total:',sum(forms.values()))
    print('claims:',len(claims),'non_not_measured:',len(nonnm),'non_not_measured_values:',sum(v for k,v in forms.items() if k!='not_measured'))
    print('root_merge_commit:',len(merge),'new_keys_after_normalization:',extra)
    print('L5 candidates:',exempt,'effective:',sum(ok for _,ok in exempt))
    print('L8 red:',len(l8),'rows:',json.dumps(rows,ensure_ascii=False))
    print('L7 landed:',len(landed),'with_claim:',sum(x[1] for x in landed),'without_claim:',sum(not x[1] for x in landed))
    print('provenance dossiers/files:',len(withprov),len(provs),'non_not_measured_with_prov:',len(set(nonnm)&set(withprov)))
    statuses = collections.Counter(j.get('trang_thai') for _,d in provs for j in d['moc']['gate_output']['jobs'])
    print('job statuses:',dict(statuses))
    print('event/workflow/job counts:',dict(collections.Counter((d['moc']['run']['event'],d['moc']['run']['loi_khai_rest_path'],len(d['moc']['gate_output']['jobs'])) for _,d in provs)))
    print('full logs equal active jobs:',sum(set(d['log_day_du'])=={j['job_id'] for j in d['moc']['gate_output']['jobs'] if j['conclusion']!='skipped'} for _,d in provs),'/',len(provs))
    for st in ('danh_gia','tom','tu_do'):
        print('style',st,'dossiers',sum(st in v for v in styles.values()),'only',sum(v=={st} for v in styles.values()))
    print('style paths:',json.dumps(stylepaths,ensure_ascii=False))
    print('push master runs:',[(d['moc']['run']['run_id'],len(d['moc']['gate_output']['jobs']),sorted({str(j['labels']) for j in d['moc']['gate_output']['jobs']})) for _,d in provs if d['moc']['run']['event']=='push'])

elif sys.argv[1] == 'steps':
    prov = yaml.safe_load((ROOT/'ops/land/pr1231-wp1105-provenance/ci/provenance.yaml').read_bytes())
    r = prov['moc']['run']
    wf = cp.doc_wf(cp.git_blob(r['head_sha'],r['loi_khai_rest_path'],ROOT))
    tree = ast.parse((ROOT/'ops/land/pr1231-wp1105-provenance/danh_gia_gate.py').read_text())
    selected = [n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'JSON_OK','TL_SELFTEST','TL_SELFTEST_PATS','LUAT'} for t in n.targets)]
    ns = {}
    exec(compile(ast.Module(body=selected,type_ignores=[]),'rules','exec'),ns)
    print('run:',r)
    counts = collections.Counter()
    for job in prov['moc']['gate_output']['jobs']:
        k = cp.ghep_job(job['name'],wf)
        luat = next((b for pre,b in ns['LUAT'] if job['name'].startswith(pre)),[])
        for marker,pats in luat:
            command_marker = 'tl.py --selftest' if marker == ns['TL_SELFTEST'] else marker
            matches = [(i,b) for i,b in enumerate(wf['jobs'][k]['steps']) if command_marker in b.get('run','')]
            for i,b in matches:
                name = cp.ten_du_kien(b)
                rest = [s for s in job['buoc'] if s['name']==name]
                blocked = cp.chan_buoc(wf,k,i)
                coe = b.get('continue-on-error',False)
                pipe = '|' in b.get('run','')
                pipefail = 'pipefail' in b.get('run','') or 'pipefail' in b.get('shell','') or b.get('shell')=='bash'
                counts['rule_instances'] += 1
                counts['rest_unique_success'] += len(rest)==1 and rest[0]['conclusion']=='success'
                counts['blocked'] += blocked
                if blocked or coe or pipe and not pipefail or len(rest)!=1:
                    print('K7 problem:',json.dumps({'job':job['name'],'step':name,'rest':rest,'blocked':blocked,'continue-on-error':coe,'pipe':pipe,'pipefail':pipefail,'yaml':b},ensure_ascii=False))
            if len(matches)!=1: print('mapping count:',job['name'],marker,len(matches))
    print('counts:',dict(counts))
    print('ghep_buoc provenance:',dict(collections.Counter((j.get('ghep_buoc',{}).get('trang_thai'),j.get('ghep_buoc',{}).get('ly_do')) for j in prov['moc']['gate_output']['jobs'])))
    print('wf job default/env:',{k:{a:v for a,v in j.items() if a in ('defaults','env')} for k,j in wf['jobs'].items()})
