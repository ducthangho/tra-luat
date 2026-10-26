import importlib.util,json,time
from pathlib import Path
r=Path('.review');s=importlib.util.spec_from_file_location('t',Path('ops/ci_provenance_test.py'));t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
with (r/'case-progress.txt').open('w') as f:
 for c in t.CA:
  start=time.time();f.write('START '+c+'\n');f.flush();rc,o=t.chay_ca(c);f.write(json.dumps({'case':c,'rc':rc,'seconds':time.time()-start,'output':o})+'\n');f.flush()
