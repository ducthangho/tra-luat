from pathlib import Path
import concurrent.futures,json,os,subprocess,re,yaml
from audit import OUT,ROOT,record
copy=Path((OUT/'copy-path.txt').read_text());dest=OUT/'hint-validation';dest.mkdir(exist_ok=True);env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
expected=json.loads((OUT/'hint-paths.json').read_text());actual=subprocess.check_output(['git','-C',str(copy),'diff','--name-only']).decode().splitlines();assert sorted(actual)==sorted(expected),(actual,expected)
commands=json.loads((OUT/'checks.json').read_text());results={}
def run(item):
 k,v=item;cmd=v['command'];p=subprocess.run(cmd,cwd=copy,env=env,capture_output=True,text=True)
 for suffix,data in [('stdout',p.stdout),('stderr',p.stderr),('rc',str(p.returncode))]:(dest/(k+'.'+suffix)).write_text(data)
 summary=json.dumps({k:json.loads(p.stdout)[k] for k in ['ok','strict']}) if k=='doc_claims' else '\n'.join(p.stdout.strip().splitlines()[-2:])
 return k,{'rc':p.returncode,'summary':summary,'command':cmd}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=dict(pool.map(run,commands.items()))
(dest/'checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
summary='\n'.join(' '.join(v['command'])+' | rc='+str(v['rc'])+' | '+v['summary'] for v in results.values());print(summary)
record(14,'Đo lại hint bằng ca và cổng sẵn có trên clone','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/hint_checks.py; seven existing commands with cwd <copy>',summary,'KHÔNG PHẢI LỖI của hint' if all(x['rc']==0 for x in results.values()) else 'CẦN KIỂM TRA HINT')
