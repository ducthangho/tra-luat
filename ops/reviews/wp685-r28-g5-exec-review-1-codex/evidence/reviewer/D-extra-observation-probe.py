import importlib.util
import json
from pathlib import Path
import sys

module_path = Path(__file__).resolve().parents[1] / 'executor/bang_chung_aw_d.py'
spec = importlib.util.spec_from_file_location('reviewer_aw_probe', module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
unexpected = ('B2-parse', 'unexpected-unit')
recorded = {module.T156:list(module.DON_VI_156) + [unexpected], module.T157:list(module.DON_VI_157)}
result = module.doi_chieu(recorded)
accepted = not result[0] and not result[1]
print(json.dumps({'probe':'synthetic comparator input', 'unexpected_unit':unexpected, 'result':result, 'accepted':accepted}))
print('DEFECT_REPRODUCED' if accepted else 'DEFECT_NOT_REPRODUCED')
sys.exit(0 if accepted else 1)
