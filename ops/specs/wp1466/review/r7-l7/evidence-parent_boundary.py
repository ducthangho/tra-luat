from pathlib import Path
import sys,os,subprocess,json,datetime
O=Path(__file__).resolve().parent;k=O/'tmp/closed-inputs/os_startup/kho';TK=O/'sc/tien_kiem.py'
env=dict(os.environ,PYTHONPATH=str(k),PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'),GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='commit.gpgsign',GIT_CONFIG_VALUE_0='false')
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat())
rows=[]
for name,flags in [('external_nonisolated_nosite_nofrozen',('-S','-X','frozen_modules=off')),('external_isolated_nosite_nofrozen',('-I','-S','-X','frozen_modules=off')),('external_nonisolated_nosite_frozen',('-S',)),('external_isolated_normal',('-I',))]:
 cmd=[sys.executable,'-B','-v',*flags,str(TK),'origin/master'];r=subprocess.run(cmd,cwd=k,env=env,capture_output=True,text=True);trace=[x for x in r.stderr.splitlines() if str(k/'os.py') in x]
 (O/(name+'.log')).write_text(r.stdout+r.stderr)
 row=dict(name=name,command=cmd,rc=r.returncode,local_os=bool(trace),trace=trace,stdout=r.stdout,stop=[x for x in r.stderr.splitlines() if 'KHÔNG ĐO ĐƯỢC' in x]);rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
cmd=[sys.executable,'-B','-S','-X','frozen_modules=off','-c','import sys; print("OS_PRELOADED", "os" in sys.modules)'];r=subprocess.run(cmd,cwd=k,env=env,capture_output=True,text=True);print('PRE_SCRIPT',cmd,'RC',r.returncode,r.stdout.strip())
(O/'parent-boundary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
