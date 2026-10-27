from pathlib import Path
import subprocess, json, os, concurrent.futures
base=Path.cwd(); root=base/'cay-kho'; out=base/'review_evidence'
commands={ 't26':['python3','ops/lease_publish_test.py','--chi-ca=t26_'], 't27':['python3','ops/lease_publish_test.py','--chi-ca=t27_'], 't138':['python3','ops/lease_publish_test.py','--chi-ca=t138_'], 'bien_nhan_v2':['python3','ops/bien_nhan_v2.py','--root','.'], 'land':['python3','ops/land_evidence_nguon.py','--root','.'], 'doctrine':['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'], 'doc_claims':['python3','scripts/tl.py','doc-claims-check','--json'] }
def run(item):
 k,c=item
 p=subprocess.run(c,cwd=root,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 for suffix,data in [('stdout',p.stdout),('stderr',p.stderr),('rc',str(p.returncode))]: (out/(k+'.'+suffix)).write_text(data)
 summary=p.stdout[-1600:] if k!='doc_claims' else {x:json.loads(p.stdout).get(x) for x in ['ok','strict']}
 return k, {'command':c,'rc':p.returncode,'summary':summary,'stderr':p.stderr[-500:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=dict(pool.map(run,commands.items()))
(out/'checks.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
print(json.dumps(results,indent=2,ensure_ascii=False))
