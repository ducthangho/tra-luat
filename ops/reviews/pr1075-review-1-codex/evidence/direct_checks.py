import importlib.util
import json
import sys
import traceback
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'ops'))
spec = importlib.util.spec_from_file_location('review_gate_tests', root / 'ops/lease_publish_test.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
results = []
for name in sorted(n for n in vars(module) if n.startswith(('t26_', 't27_'))):
    try:
        getattr(module, name)()
        result = {'name': name, 'status': 'PASS'}
    except Exception as exc:
        result = {'name': name, 'status': 'FAIL', 'exception': type(exc).__name__, 'message': str(exc)}
        traceback.print_exc()
    results.append(result)
    print(json.dumps(result, ensure_ascii=False), flush=True)
assert len(results) == 3, results
sys.exit(int(any(r['status'] != 'PASS' for r in results)))
