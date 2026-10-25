import os,sys,subprocess,json
from pathlib import Path
R=Path(__file__).resolve().parent
rows=[]
for case in ('r4_F02_env_metadata','r4_F02_mixed_color','F02_collision_other_job','F02_missing_endgroup','git_workflow_source','control_simple'):
    cmd=[sys.executable,'-B',str(R/'review_cases.py'),case]; p=subprocess.run(cmd,capture_output=True)
    rows.append({'case':case,'command':cmd,'rc':p.returncode,'output':(p.stdout+p.stderr).decode()})
for name in ('git_ignore_sha','git_always_unavailable'):
    case='git_workflow_source'; cmd=[sys.executable,'-B',str(R/'review_cases.py'),case]
    p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(R/'extra-mutants'/f'{name}.py')))
    rows.append({'mutant':name,'case':case,'command':cmd,'rc':p.returncode,'output':(p.stdout+p.stderr).decode(),'rank':'GIET' if p.returncode==3 and f'DO:{case}:' in p.stdout.decode() else 'OTHER'})
(R/'review-cases.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(rows,ensure_ascii=False,indent=2))
