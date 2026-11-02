"""Behavioral witnesses for reviewer mutants, each copied exact HEAD."""
import ast
import json
import os
import subprocess
from pathlib import Path
ROOT=Path('/tmp/wp960-r2-l2-copy')
module=ast.parse(Path('new_mutations.py').read_text())
changes=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='M' for x in n.targets))
for name,script,mode in [('n1-vang-stat','probe_r2.py','symlinks'),('n2-vang-oserror','probe_r2.py','symlinks'),('n3-peel-rc','probe_objects.py','objects'),('n4-ref-show-error','probe_r2.py','refs'),('n7-peel-noncommit','probe_objects.py','collisions')]:
 dest=Path('/tmp/wp960-r2-l2-witness-'+name)
 subprocess.run(['git','clone','--shared','--no-checkout','--quiet',str(ROOT),str(dest)],check=True)
 subprocess.run(['git','-C',str(dest),'checkout','--quiet','--detach','ae0d06c23fb777545fd7547a07d9f368e4122f49'],check=True)
 f=dest/'ops/bien_nhan_v2.py';s=f.read_text();old,new=changes[name];assert s.count(old)==1;f.write_text(s.replace(old,new))
 with open('evidence/witness-'+name+'.log','w') as out:
  q=subprocess.run(['python3','-u',script,mode],stdout=out,stderr=subprocess.STDOUT,env=dict(os.environ,WP960_REVIEW_COPY=str(dest),PYTHONDONTWRITEBYTECODE='1'))
 print(json.dumps(dict(mutation=name,runner_rc=q.returncode,log='evidence/witness-'+name+'.log')),flush=True)
