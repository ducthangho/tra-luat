import pathlib,subprocess,os,time,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1]/'repo';W=R.parent/'work';E=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(W/'tmp'))
jobs=[('ledger',['python3','-B',str(R.parent/'bang_chung/ledger/ledger_mien.py'),str(R),str(W/'ledger.md'),str(W/'ledger-o.json'),str(W/'ledger-c36.jsonl')]),('c37-audit',['python3','-B',str(R.parent/'lich_su/audit_c37.py')]),('law9-artifacts',['python3','-B',str(R.parent/'lich_su/law9_audit.py')])]
out=[]
for name,args in jobs:
 t=time.monotonic();p=subprocess.run(args,cwd=R,env=E,capture_output=True)
 (W/(name+'.stdout.log')).write_bytes(p.stdout);(W/(name+'.stderr.log')).write_bytes(p.stderr)
 d=dict(name=name,command=args,rc=p.returncode,status='passed' if p.returncode==0 else 'failed',seconds=time.monotonic()-t,stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),stderr_sha256=hashlib.sha256(p.stderr).hexdigest(),stdout_log=name+'.stdout.log',stderr_log=name+'.stderr.log',tested_sha='bca55c1cd09c57180d60b05d5ca1813828ae1d10');out.append(d)
 (W/(name+'-result.json')).write_text(json.dumps(d,indent=2));print(name,p.returncode,p.stdout.decode(errors='replace')[-500:],p.stderr.decode(errors='replace')[-200:],flush=True)
 if p.returncode:break
(W/'confirm-evidence.json').write_text(json.dumps(out,indent=2))
