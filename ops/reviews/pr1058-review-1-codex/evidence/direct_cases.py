import importlib.util, sys
from pathlib import Path
p=Path(sys.argv[1]).resolve()/'ops/lease_publish_test.py'
spec=importlib.util.spec_from_file_location('review_lease_publish_test',p)
m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m)
fs=[getattr(m,n) for n in sorted(vars(m)) if n.startswith(('t26_','t27_')) and callable(getattr(m,n))]
assert len(fs)==3, [f.__name__ for f in fs]
for f in fs:
    f()
    print('PASS',f.__name__,flush=True)
print(f'PASS {len(fs)}/{len(fs)} direct functions')
