import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
S = Path(__file__).resolve().parent
R = S/'cay-kho'
B = S/'base-cay-kho'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
def run(args, cwd, check=False):
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, check=check)
if not B.exists():
    run(['git','clone','--shared','--no-checkout',str(R),str(B)], S, True)
    refs = run(['git','for-each-ref','--format=%(objectname) %(refname)','refs/remotes/origin/'],R,True).stdout.splitlines()
    for ref in refs:
        oid, name = ref.split()
        if name != 'refs/remotes/origin/HEAD':
            run(['git','update-ref',name,oid],B,True)
    origin = run(['git','remote','get-url','origin'],R,True).stdout.strip()
    run(['git','remote','set-url','origin',origin],B,True)
    run(['git','checkout','--detach','afc82f6d7447eb76fc8adbe46c1be90be88d331f'],B,True)
run(['git','config','core.abbrev','7'],B,True)
commands = {
 'bien-nhan':['python3','ops/bien_nhan_v2.py','--root','.'],
 'land':['python3','ops/land_evidence_nguon.py','--root','.'],
 'direct':['python3',str(S/'direct_cases.py'),'.'],
 'doctrine':['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'],
 'diff-check':['git','diff','--check'],
 'range-check':['git','diff','--check','afc82f6d7447eb76fc8adbe46c1be90be88d331f','HEAD'],
}
def gate(side,root,name,args):
    p = run(args,root)
    path = S/'evidence'/f'{side}-{name}.log'
    path.write_text(f'command: {args!r}\nrc: {p.returncode}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}')
    return dict(side=side,gate=name,command=args,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    fs = [pool.submit(gate,side,root,name,args) for side,root in [('head',R),('base',B)] for name,args in commands.items()]
    results = [f.result() for f in fs]
(S/'evidence/gates.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
for r in results:
    print(r['side'],r['gate'],'rc='+str(r['rc']),r['stdout'].strip()[-900:],r['stderr'].strip()[-500:])
sys.exit(int(any(r['rc'] for r in results)))
