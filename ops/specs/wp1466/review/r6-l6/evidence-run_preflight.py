from pathlib import Path
import os,sys,subprocess,json,datetime
O=Path(__file__).resolve().parent
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'),GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='commit.gpgsign',GIT_CONFIG_VALUE_0='false')
tasks=[('fx33',[sys.executable,'-B',str(O/'sc/fx_tien_kiem.py'),str(O),str(O/'base/ops/lease_publish.py')]),('extra-r5',[sys.executable,'-B',str(O/'preflight_extra.py')]),('mutants',[sys.executable,'-B',str(O/'sc/dot_bien.py'),str(O),str(O/'base/ops/lease_publish.py')])]
data=[]
for name,cmd in tasks:
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/f'{name}.log').open('w') as f: r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env)
 data.append(dict(name=name,command=cmd,utc=t,rc=r.returncode));(O/'preflight-results.json').write_text(json.dumps(data,indent=2))
 print(name,'rc',r.returncode,flush=True)
