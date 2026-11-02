import importlib.util
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'ops'))
spec = importlib.util.spec_from_file_location('lease_publish_test', root / 'ops/lease_publish_test.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
failed = 0
for name in sorted(vars(m)):
    if name.startswith(('t26_', 't27_')) and callable(getattr(m, name)):
        try:
            getattr(m, name)()
            print('PASS', name)
        except Exception as e:
            failed += 1
            print('FAIL', name, type(e).__name__, str(e))
sys.exit(bool(failed))
