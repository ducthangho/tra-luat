import os,sys,subprocess,json,hashlib,time
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1'
S=Path(__file__).resolve().parent; E=S/'evidence'; name=sys.argv[1]; R=S/'work'/name
cmds=[('bien-nhan',['python3','ops/bien_nhan_v2.py','--root','.']),('land',['python3','ops/land_evidence_nguon.py','--root','.']),('direct',['python3',str(S/'direct_checks.py'),'.']),('doctrine',['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.']),('diff-check',['git','diff','--check','fb74c6e','HEAD'])]
rows=[]
for label,cmd in cmds:
 t=time.monotonic(); p=subprocess.run(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=E/f'{name}-{label}.log'; log.write_bytes(p.stdout)
 r={'label':label,'cwd':str(R),'command':cmd,'rc':p.returncode,'seconds':round(time.monotonic()-t,3),'log':str(log.relative_to(S)),'sha256':hashlib.sha256(p.stdout).hexdigest()}; rows.append(r)
 print(json.dumps(r,ensure_ascii=False),flush=True); print(p.stdout.decode()[-1700:],flush=True)
(E/f'{name}-gates.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
sys.exit(any(x['rc'] for x in rows))
