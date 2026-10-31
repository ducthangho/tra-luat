from pathlib import Path
import subprocess,concurrent.futures,json
r=Path(__file__).resolve().parents[1]
names=['version-identity-oracle', 'cli-version-identity-oracle', 'cli-case-identity-oracle', 'node-major-oracle', 'numeric-identity-oracle', 'zip-numeric-identity-oracle', 'unknown-target-oracle']
def run(n):
 c=['python3','-u',str(r/'probes'/(n+'.py'))]
 p=subprocess.run(c,capture_output=True,text=True,cwd=r,timeout=240)
 (r/'evidence'/(n+'-round15.log')).write_text(p.stdout+p.stderr)
 z=dict(name=n,rc=p.returncode,command=c,tail=(p.stdout+p.stderr).splitlines()[-2:]);print(json.dumps(z,ensure_ascii=False),flush=True);return z
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,names))
(r/'evidence/identities-round15-drivers.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
