import os,sys,json,subprocess,hashlib,platform
from pathlib import Path
R=Path(__file__).resolve().parent
out={'runtime':{'os':platform.platform(),'python':sys.version,'executable':sys.executable},'commands':[]}
commands=[['git','remote','get-url','origin'],['git','rev-parse','HEAD','HEAD^{tree}','HEAD^'],['git','symbolic-ref','-q','--short','HEAD'],['git','rev-parse','--is-shallow-repository'],['git','merge-base','--is-ancestor','dc657149941f9db3ab2afc6fb6462ba4827bf18f','HEAD'],['git','diff','--numstat','dc657149941f9db3ab2afc6fb6462ba4827bf18f','HEAD'],['git','diff','--check','dc657149941f9db3ab2afc6fb6462ba4827bf18f','HEAD'],['git','config','--get','core.abbrev'],['git','--version'],['codex','--version'],[sys.executable,'-B','-m','ruff','--version']]
for cmd in commands:
 p=subprocess.run(cmd,capture_output=True); out['commands'].append({'command':cmd,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()})
for label,args in [('full',['git','diff','dc657149941f9db3ab2afc6fb6462ba4827bf18f','HEAD']),('delta',['git','diff','HEAD^','HEAD'])]:
 p=subprocess.run(args,capture_output=True); (R/f'{label}.patch').write_bytes(p.stdout)
out['specs']={str(p):{'bytes':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (R.parent/'.review-input').glob('*.md')}
thread=os.environ.get('CODEX_THREAD_ID'); out['thread_id']=thread
if thread:
 for p in Path('/root/.codex/sessions').rglob('*'+thread+'*.jsonl'):
  meta=[]
  for line in p.open():
   try: v=json.loads(line)
   except ValueError: continue
   pl=v.get('payload',{})
   if v.get('type')=='session_meta': meta.append({k:pl.get(k) for k in ('id','originator','cli_version','model_provider')})
   if v.get('type')=='turn_context': meta.append({k:pl.get(k) for k in ('model','effort','model_reasoning_effort')})
  out['identity']={'source':str(p),'metadata':meta}
(R/'preflight.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(out,ensure_ascii=False,indent=2))
