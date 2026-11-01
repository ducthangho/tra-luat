import hashlib
import json
import os
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
HEAD='907c474e5dd22b2f389e8c342e7c79c6fbcb760e'
BASE='3574cb07dba8a8f7f32384ee3d1d3dfbf3a4f70e'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
errors=[]
snapshots={}
for folder in ['cay-kho','work/head','work/base','work/mutant']:
    root=HERE/folder
    def git(*args):return subprocess.check_output(['git','-c','core.abbrev=7',*args],cwd=root,env=env).decode().strip()
    status=git('status','--porcelain=v1','--untracked-files=all','--ignored')
    head=git('rev-parse','HEAD')
    snapshots[folder]={'head':head,'tree':git('rev-parse','HEAD^{tree}'),'status_including_ignored':status}
    if status or head!=(BASE if folder=='work/base' else HEAD):errors.append(folder)

reports={}
for filename in ['preflight','archive','receipt','readme-history']:
    r=json.loads((HERE/'evidence'/f'{filename}.json').read_text())
    reports[filename]=r.get('errors',[])
    errors.extend(reports[filename])
gate_results={}
for label in ['head','base']:
    r=json.loads((HERE/'evidence'/f'{label}-gates.json').read_text())
    gate_results[label]={k:v['rc'] for k,v in r.items()}
    if any(v['rc'] for v in r.values()):errors.append('gates '+label)
mutation=json.loads((HERE/'evidence/mutation.json').read_text())
if not (mutation['restored_bytewise'] and mutation['bien-nhan']['rc']==1 and mutation['direct']['rc']==1):errors.append('mutation')
identical_logs={name:(HERE/'evidence'/f'head-{name}.log').read_bytes()==(HERE/'evidence'/f'base-{name}.log').read_bytes() for name in ['land','doctrine','diff-check']}
warnings={label:[line.split('SyntaxWarning:',1)[-1] for line in (HERE/'evidence'/f'{label}-direct.log').read_text().splitlines() if 'SyntaxWarning:' in line] for label in ['head','base']}
output={'repositories':snapshots,'reports_errors':reports,'gate_rc':gate_results,
        'mutation_restored':mutation['restored_bytewise'],'identical_head_base_logs':identical_logs,
        'syntax_warnings_equal':warnings['head']==warnings['base'],'errors':errors}
(HERE/'evidence/final-integrity.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(output,ensure_ascii=False))
raise SystemExit(bool(errors))
