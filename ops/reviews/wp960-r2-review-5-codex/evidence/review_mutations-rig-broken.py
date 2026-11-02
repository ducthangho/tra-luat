from pathlib import Path
import importlib.util,sys,json,time,shutil
BASE=Path('/tmp/wp960-r5-copy')
mutations={
'u1-bo-stderr':('    if con:\n','    if False:\n'),
'u2-bo-bien-suc-khoe':('    nong = _git_do(root, "rev-parse", "--is-shallow-repository")[1].strip()','    nong = _chay_git(root, ("rev-parse", "--is-shallow-repository")).stdout.strip()'),
'u3-bo-kiem-dang-bool':('        if gt not in ("true", "false"):\n','        if False:\n'),
'u4-bo-chuan-hoa-bool':('"config", "--type=bool", "--get-regexp"','"config", "--get-regexp"'),
'u5-bo-loc-env':('if not k.startswith("GIT_") or k in _GIT_GIU}', 'if True}'),
'u6-bo-chan-promisor-true':('        if gt == "true":','        if False:'),
}
for name in sys.argv[1:] or mutations:
 sp=importlib.util.spec_from_file_location('review_tests',BASE/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(sp);sp.loader.exec_module(t)
 a,z=mutations[name];t._dot_bien_tep(a,z)
 red=[];start=time.monotonic()
 try:
  for fn in t.CA:
   tt,ct=t._chay_1(fn)
   if tt!='qua':red.append((fn.__name__,tt,ct))
  print(json.dumps(dict(mutant=name,match_count=1,count=len(t.CA),passed=len(t.CA)-len(red),red=red,seconds=round(time.monotonic()-start,3)),ensure_ascii=False),flush=True)
 finally:
  for p in t._TAM_DOT_BIEN:shutil.rmtree(p,ignore_errors=True)
