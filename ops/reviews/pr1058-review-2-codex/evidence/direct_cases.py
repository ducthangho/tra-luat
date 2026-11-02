import importlib.util
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location('review_lease_cases', root/'ops/lease_publish_test.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
cases = [f for f in m.CA if f.__name__.startswith(('t26_', 't27_'))]
assert len(cases) == 3, [f.__name__ for f in cases]
for f in cases:
    f()
    print('PASS', f.__name__)
print('PASS 3/3 direct functions')
