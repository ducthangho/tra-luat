"""Read-only probes on genuine local evidence; no fabricated attack inputs."""
import ast
from collections import Counter
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import yaml

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE / 'repo'
WORK = BASE / 'work'

def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

cp = load('prov_probe', ROOT / 'ops/ci_provenance.py')
pd = ROOT / 'ops/land/pr1231-wp1105-provenance/ci'
prov = yaml.safe_load((pd / 'provenance.yaml').read_bytes())
jobs = json.loads((pd / 'jobs.json').read_bytes())['jobs']
run = prov['moc']['run']
wf = cp.doc_wf(cp.git_blob(run['head_sha'], run['loi_khai_rest_path'], ROOT))
results = Counter()
for j in jobs:
    trace = (pd / f"jobs/{j['id']}.trich.txt").read_text().splitlines()
    result, pairs = cp.ghep_buoc(j, cp.tach_buoc(trace), wf, '')
    results[(result['trang_thai'], result.get('ly_do'))] += 1
print('ghep_buoc original + real REST + real header traces:', dict(results))
print('NOTE: only matching headers tested; traces are not complete logs.')

blocked_steps = []
for j in prov['moc']['gate_output']['jobs']:
    k = cp.ghep_job(j['name'], wf)
    for i,b in enumerate(wf['jobs'][k]['steps']):
        if b.get('run') == 'python .claude/dev/ci_dang_ky_test.py --chay':
            matches = [s for s in j['buoc'] if s['name']==cp.ten_du_kien(b)]
            print('F-ok registry step:',json.dumps({'job':j['name'],'name':cp.ten_du_kien(b),'REST':matches,'chan_buoc':cp.chan_buoc(wf,k,i),'extra_keys':sorted(set(b)-cp.KHOA_BUOC)},ensure_ascii=False))
            blocked_steps.append((k,i))

for p in ('ops/ci_provenance.py','ops/kiem_ho_so_land.py'):
    dst = WORK / 'canon_import' / p
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_bytes(subprocess.check_output(['git','-C',str(ROOT),'show','refs/remotes/origin/master:'+p]))
canon_cp = load('cp_canon_probe',WORK/'canon_import/ops/ci_provenance.py')
canon_ld = load('ld_canon_probe',WORK/'canon_import/ops/kiem_ho_so_land.py')
cw = canon_cp.doc_wf(cp.git_blob(run['head_sha'],run['loi_khai_rest_path'],ROOT))
print('canon existing dependencies import:', 'OK', 'registry needed at import:', (WORK/'canon_import/.claude/dev/ci_dang_ky_test.py').exists())
for k,i in blocked_steps:
    print('canon function calls:',canon_cp.ghep_job('gate-registry (ubuntu-latest)',cw),canon_cp.ten_du_kien(cw['jobs'][k]['steps'][i]),'chan_buoc=',canon_cp.chan_buoc(cw,k,i))

for path in sorted((ROOT/'ops/land').glob('*-land-evidence.yaml')):
    d=yaml.safe_load(path.read_bytes())
    pd=path.with_name(path.name.removesuffix('-land-evidence.yaml')+'-provenance')
    for p in pd.rglob('*.yaml'):
        z=yaml.safe_load(p.read_bytes())
        if not isinstance(z,dict) or z.get('schema')!='ci_provenance/1': continue
        r=z['moc']['run']
        if r['head_sha']==d.get('merge_commit') and any('windows-latest' in (j.get('labels') or []) for j in z['moc']['gate_output']['jobs']):
            print('Windows run at ROOT merge_commit:',path.name,'run=',r['run_id'],'workflow=',r['loi_khai_rest_path'])

tree=ast.parse((ROOT/'ops/land/pr1231-wp1105-provenance/danh_gia_gate.py').read_text())
assign=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'JSON_OK','TL_SELFTEST','TL_SELFTEST_PATS','LUAT'} for t in n.targets)]
ns={}
exec(compile(ast.Module(body=assign,type_ignores=[]),'rule_constants','exec'),ns)
print('original rule inventory:',len(ns['LUAT']),'jobs',sum(len(b) for _,b in ns['LUAT']),'steps',sum(len(p) for _,b in ns['LUAT'] for _,p in b),'markers')
count=Counter()
for job in wf['jobs'].values():
    for b in job.get('steps',[]):
        if 'run' in b:
            count['run']+=1
            count['named']+='name' in b
print('F-that workflow run/name counts:',dict(count))
