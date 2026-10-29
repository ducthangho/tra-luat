from pathlib import Path
import importlib.util,sys,json,time,shutil
BASE=Path('/tmp/wp960-r5-copy')
mutations={
'u1-bo-stderr':('    if con:\n','    if False:\n'),
'u2-bo-bien-suc-khoe':('    nong = _git_do(root, "rev-parse", "--is-shallow-repository")[1].strip()','    nong = _chay_git(root, ("rev-parse", "--is-shallow-repository")).stdout.strip()'),
'u3-bo-kiem-dang-bool':('        if gt not in ("true", "false"):\n','        if False:\n'),
'u4-bo-chuan-hoa-bool':('"config", "--type=bool", "--get-regexp"','"config", "--get-regexp"'),
'u5-bo-loc-env':('if not k.startswith("GIT_") or k in _GIT_GIU}', 'if True}'),
'u7-giu-GIT_DIR':('_GIT_GIU = frozenset({"GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_EXEC_PATH"})', '_GIT_GIU = frozenset({"GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_EXEC_PATH", "GIT_DIR"})'),
'u6-bo-chan-promisor-true':('        if gt == "true":','        if False:'),
}
for name in sys.argv[1:] or mutations:
 import tempfile
 with tempfile.TemporaryDirectory(prefix='r5-mutant-'+name+'-') as d:
  dst=Path(d)/'repo';shutil.copytree(BASE,dst,symlinks=True)
  f=dst/'ops/bien_nhan_v2.py';a,z=mutations[name];s=f.read_text();assert s.count(a)==1,(name,s.count(a));f.write_text(s.replace(a,z))
  sp=importlib.util.spec_from_file_location('review_tests',dst/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(sp);sp.loader.exec_module(t)
  red=[];start=time.monotonic()
  print(json.dumps(dict(start=name,source=str(dst),match_count=1)),flush=True)
  for i,fn in enumerate(t.CA,1):
   tt,ct=t._chay_1(fn)
   if tt!='qua':red.append((fn.__name__,tt,ct))
   if i%10==0:print(json.dumps(dict(progress=name,completed=i,red_count=len(red))),flush=True)
  assert f.read_text()==s.replace(a,z),'source changed during suite'
  print(json.dumps(dict(mutant=name,match_count=1,count=len(t.CA),passed=len(t.CA)-len(red),red=red,seconds=round(time.monotonic()-start,3)),ensure_ascii=False),flush=True)
