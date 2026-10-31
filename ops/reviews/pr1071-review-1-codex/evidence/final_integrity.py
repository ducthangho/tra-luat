import hashlib
import json
import os
from pathlib import Path
import subprocess

s=Path(__file__).resolve().parent
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
errors=[]
def git(root,*args):
    return subprocess.check_output(['git',*args],cwd=s/root,env=env).decode().strip()
statuses={root:git(root,'status','--porcelain=v1','--untracked-files=all','--ignored') for root in ('cay-kho','base-copy','mutation-copy')}
head=git('cay-kho','rev-parse','HEAD')
if head!='01044616f0258e41608feac5b01f80770beec7a5':errors.append('head_changed')
if any(statuses.values()):errors.append(['dirty',statuses])
measurements={}
for name in ('bytes','receipts','readme','context'):
    obj=json.loads((s/f'evidence/{name}.json').read_text())
    measurements[name]=len(obj['errors'])
    if obj['errors']:errors.append([name,obj['errors']])
gates={}
for label in ('head','base'):
    rows=json.loads((s/f'evidence/{label}-gates.json').read_text())
    gates[label]={row['name']:row['rc'] for row in rows}
    if any(gates[label].values()):errors.append([label,gates[label]])
mutants=json.loads((s/'evidence/mutations.json').read_text())
for obj in mutants:
    for name in ('bien-nhan','direct'):
        v=obj['results'][name]
        if v['rc']!=1 or not v['names_target']:errors.append(['mutation_not_killed',obj['round'],name])
equality={name:(s/f'evidence/base-{name}.log').read_bytes()==(s/f'evidence/head-{name}.log').read_bytes() for name in ('land','doctrine','diff-check')}
result={'head':head,'tree':git('cay-kho','rev-parse','HEAD^{tree}'),'statuses':statuses,
        'gate_rc':gates,'measurement_error_counts':measurements,'equal_gate_logs':equality,
        'mutation_rounds':len(mutants),'errors':errors}
(s/'evidence/final-integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
