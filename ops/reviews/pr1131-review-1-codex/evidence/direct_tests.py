import sys, importlib.util, traceback
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root/'ops'))
import lease_publish_test as m
failed = 0
for name in sorted(n for n in dir(m) if n.startswith(('t26_', 't27_'))):
    try:
        getattr(m, name)()
        print('PASS', name, flush=True)
    except Exception as e:
        failed += 1
        print('FAIL', name, repr(e), flush=True)
        traceback.print_exc()
raise SystemExit(bool(failed))
