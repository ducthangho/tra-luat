import importlib.util, sys, traceback
from pathlib import Path
p=Path(sys.argv[1]).resolve()/'ops'/'lease_publish_test.py'
sys.path.insert(0,str(p.parent))
spec=importlib.util.spec_from_file_location('review_gate_tests',p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
bad=0
for name in sorted(n for n in vars(m) if n.startswith(('t26_','t27_')) and callable(getattr(m,n))):
    try:
        getattr(m,name)()
        print('PASS',name)
    except Exception:
        bad+=1
        print('FAIL',name)
        traceback.print_exc()
sys.exit(bool(bad))
