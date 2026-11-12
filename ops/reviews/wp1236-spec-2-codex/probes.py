import ast
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]/'repo'
WORK=Path(__file__).resolve().parent
source=(ROOT/'ops/land/pr1231-wp1105-provenance/danh_gia_gate.py').read_text()
tree=ast.parse(source)
env={}
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'JSON_OK','TL_SELFTEST','TL_SELFTEST_PATS','LUAT'} for t in node.targets):
        exec(compile(ast.Module(body=[node],type_ignores=[]),'<LUAT literals>','exec'),env)
luat=env['LUAT']
patterns=[p for _,steps in luat for _,pats in steps for p in pats]
print('LUAT',len(luat),'STEP_TYPES',sum(len(s) for _,s in luat),'PATTERNS',len(patterns),'KINDS',dict(collections.Counter('JSON_OK' if p=='JSON_OK' else p.split(':')[0] if p.startswith(('CUOI:','KHONG:')) else 'DONG' for p in patterns)))
p=ROOT/'ops/land/pr1231-wp1105-provenance/ci/provenance.yaml'
data=yaml.safe_load(p.read_bytes())
run=data['moc']['run']
wfbytes=subprocess.run(['git','-C',str(ROOT),'show',run['head_sha']+':.github/workflows/ci.yml'],capture_output=True,check=True).stdout
wf=yaml.safe_load(wfbytes)
print('RUN',run['run_id'],'HEAD',run['head_sha'],'ATTEMPT',data['attempt_yeu_cau'])
for job in data['moc']['gate_output']['jobs']:
    if not job['name'].startswith(('chuan-bi','gate-packet-loop','gate-registry')):
        continue
    f=p.parent/data['log_day_du'][job['job_id']]['trich']
    headers=[re.sub(r'^.*?##\[group\]','',l) for l in f.read_text().splitlines() if '##[group]Run ' in l]
    names={s['name']:s['conclusion'] for s in job['buoc']}
    kind=job['name'].split(' (')[0]
    for s in wf['jobs'][kind]['steps']:
        command=s.get('run','')
        if any(x in command for x in ('ci_duong_nhanh.py','packet_loop_test.py','ci_dang_ky_test.py')):
            header='Run '+command.splitlines()[0]
            print('K7',json.dumps({'job_id':job['job_id'],'job':job['name'],'cmd':command.splitlines()[0], 'header_in_log':header in headers,'expected_by_spec':header,'rest_name':s.get('name'),'rest_conclusion':names.get(s.get('name')),'k7_match':header in names,'shell':s.get('shell'),'job_defaults':wf['jobs'][kind].get('defaults'),'workflow_defaults':wf.get('defaults')},ensure_ascii=False))

# Read authentic records only; no altered evidence is constructed.
doc=yaml.safe_load((ROOT/'ops/land/pr1023-wp1009-r4-land-evidence.yaml').read_bytes())
print('NEO_RUN_EXAMPLE',json.dumps({'merge_commit':doc['merge_commit'],'pre_merge':[{k:x[k] for k in ('run_id','run_attempt','sha') if k in x} for x in doc['pre_merge_checks'] if 'moc_gate_output' in x], 'post_merge':[{k:x[k] for k in ('run_id','run_attempt','sha') if k in x} for x in doc['post_merge_checks'] if 'moc_gate_output' in x]},ensure_ascii=False))

for cmd in [
    ['python','-B','ops/land_evidence_nguon.py','--root','.'],
    ['python','-B','ops/kiem_ho_so_land.py','--root','.'],
    ['python','-B','.claude/dev/packet_loop.py','doctrine-scan','--root','.'],
    ['python','-B','-m','ruff','check','--no-cache','--select','F','--output-format','json','.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py','ops/land_evidence_nguon.py','ops/land_evidence_nguon_test.py','ops/kiem_ho_so_land.py','ops/kiem_ho_so_land_test.py','.claude/dev/ci_dang_ky_test.py'],
]:
    out=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    name='ruff' if 'ruff' in cmd else Path(cmd[2]).stem
    (WORK/(name+'.txt')).write_text(out.stdout+out.stderr)
    if name=='ruff':
        summary=dict(collections.Counter((Path(x['filename']).name,x['code']) for x in json.loads(out.stdout)))
    else:
        summary=out.stdout.splitlines()[-2:]
    print('BASELINE',name,'rc',out.returncode,summary)

for path in ('ops/land_evidence_nguon.py','ops/land_evidence_nguon_test.py','ops/kiem_ho_so_land.py','ops/kiem_ho_so_land_test.py'):
    print('LINES',path,len((ROOT/path).read_text().splitlines()))
