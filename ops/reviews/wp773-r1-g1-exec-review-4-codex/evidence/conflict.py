import sys,importlib.util,contextlib,io,json
from pathlib import Path
K=Path('/home/user/rv773'); O=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('t',K/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
for ma in [t.MA,Path('/tmp/rv773-r4-conflict-off.py')]:
 s=importlib.util.spec_from_file_location('m',ma);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 p={'readback-pr-9001.json':t.RB_PR,'readback-pr-9002.json':t.RB_PR.replace('02:58:26','01:00:00')}
 with t.cay('pre_merge_checks: []\n',p) as root:
  (root/'ops/land'/t.TEN).rename(root/'ops/land/thu-land-evidence.yaml')
  (root/'ops/land'/t.PROV).rename(root/'ops/land/thu-provenance')
  rc,out=t.kiem(m,root)
  print(json.dumps(dict(ma=str(ma),rc=rc,output=out),ensure_ascii=False))
