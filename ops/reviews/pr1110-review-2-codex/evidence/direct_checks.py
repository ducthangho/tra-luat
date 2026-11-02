import importlib.util,sys,traceback
from pathlib import Path
root=Path(sys.argv[1]).resolve(); sys.path.insert(0,str(root/'ops'))
spec=importlib.util.spec_from_file_location('lease_tests', root/'ops/lease_publish_test.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ns=sorted(n for n in vars(m) if n.startswith(('t26_','t27_')) and callable(getattr(m,n)))
assert len(ns)==3, ns
bad=[]
for n in ns:
 try:
  getattr(m,n)(); print('PASS '+n,flush=True)
 except Exception as e:
  bad.append(n); print('FAIL '+n+': '+str(e),flush=True)
print(f'RESULT {len(ns)-len(bad)}/{len(ns)} PASS',flush=True)
sys.exit(bool(bad))
