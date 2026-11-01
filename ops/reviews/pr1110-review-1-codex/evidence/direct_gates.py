import importlib.util
import json
import sys
import traceback
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'ops'))
spec = importlib.util.spec_from_file_location('independent_lease_tests', root / 'ops/lease_publish_test.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
results = []
for name in sorted(n for n in vars(module) if n.startswith(('t26_', 't27_'))):
    try:
        getattr(module, name)()
        results.append({'name': name, 'result': 'PASS'})
    except Exception as ex:
        results.append({'name': name, 'result': 'FAIL', 'error': str(ex)})
        traceback.print_exc()
print(json.dumps(results, ensure_ascii=False, indent=2))
assert len(results) == 3
sys.exit(int(any(x['result'] != 'PASS' for x in results)))
