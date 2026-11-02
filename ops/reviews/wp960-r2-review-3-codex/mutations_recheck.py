import importlib.util,json,os,shutil,sys,tempfile,time
from pathlib import Path
ORIGIN=Path(__file__).resolve().parent/'cay-kho'
M={
 'u1-rc-check':('    if p.returncode not in sach or p.stderr.strip():\n','    if p.stderr.strip():\n'),
 'u2-default-commit':('            if lo != "commit":\n','            if False:\n'),
 'u3-ambiguous':('    if len(commit) > 1:\n','    if False:\n'),
 'u4-preserve-status':('    return p.returncode, p.stdout\n','    return 0, p.stdout\n'),
 'u5-exception-boundary':('        raise KhongDoDuoc(f"không gọi được `git {args[0]}`: {type(ex).__name__}: {ex}") from ex\n','        raise\n'),
 'u6-absence-config':('"config", "--get", "extensions.partialclone", sach=(0, 1)','"config", "--get", "extensions.partialclone", sach=(0,)'),
 'u7-absence-symref':('"symbolic-ref", "-q", ref, sach=(0, 1)','"symbolic-ref", "-q", ref, sach=(0,)'),
}
def emit(**kw):print(json.dumps(kw,ensure_ascii=False),flush=True)
for name in sys.argv[1:]:
 with tempfile.TemporaryDirectory(prefix='r3-mutant-') as tmp:
  dst=Path(tmp)/'repo';shutil.copytree(ORIGIN,dst,ignore=shutil.ignore_patterns('__pycache__'))
  src=dst/'ops/bien_nhan_v2.py';s=src.read_text();a,z=M[name];assert s.count(a)==1,(name,s.count(a));src.write_text(s.replace(a,z))
  spec=importlib.util.spec_from_file_location('test_'+name.replace('-','_'),dst/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
  start=time.perf_counter();red=[];passed=0
  for fn in t.CA:
   tt,ct=t._chay_1(fn)
   if tt=='qua':passed+=1
   else:red.append((fn.__name__,tt,ct));emit(mutant=name,case=fn.__name__,status=tt,detail=ct)
  emit(mutant=name,passed=passed,total=len(t.CA),red=red,seconds=round(time.perf_counter()-start,3))
