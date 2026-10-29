from pathlib import Path
import importlib.util,sys,tempfile,shutil,json,time
BASE=Path('/tmp/wp960-r4-copy')
mutations={
'u1-health-probe-rc':('    if p.returncode != 0:\n','    if False:\n'),
'u2-health-probe-environment':('    p = _chay_git(root, ("rev-parse", "--git-dir"))\n','    p = subprocess.run(["git", "-C", str(root), "rev-parse", "--git-dir"], capture_output=True, text=True)\n'),
'u2b-health-probe-environment':('timeout=timeout, env=_env_git())','timeout=timeout, env=(os.environ if tuple(args) == ("rev-parse", "--git-dir") else _env_git()))'),
'u3-query-environment':('    p = _chay_git(root, args, vao, timeout)\n','    p = subprocess.run(["git", "-C", str(root), *args], input=vao, capture_output=True, text=True, timeout=timeout)\n'),
'u4-health-baseline-overwrite':('    _NEN_STDERR[str(root)] = frozenset(d for d in p.stderr.splitlines() if d.strip())\n','    _NEN_STDERR.setdefault(str(root), frozenset(d for d in p.stderr.splitlines() if d.strip()))\n'),
'u5-prefix-boundary':('t[0].startswith(tuple(r + "/" for r in _REF_MAC_DINH))','t[0].startswith(_REF_MAC_DINH)'),
'u6-newline-stderr':('if d.strip() and d not in nen]','if d and d not in nen]'),
}
for name in (sys.argv[1:] or mutations):
 a,z=mutations[name]
 with tempfile.TemporaryDirectory(prefix='r4-mutant-'+name+'-') as d:
  dst=Path(d)/'repo';shutil.copytree(BASE,dst,symlinks=True)
  f=dst/'ops/bien_nhan_v2.py';s=f.read_text();assert s.count(a)==1,(name,s.count(a));f.write_text(s.replace(a,z))
  spec=importlib.util.spec_from_file_location('review_tests',dst/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
  red=[];start=time.monotonic()
  for fn in t.CA:
   tt,ct=t._chay_1(fn)
   if tt!='qua':red.append((fn.__name__,tt,ct))
  print(json.dumps(dict(mutant=name,count=len(t.CA),passed=len(t.CA)-len(red),red=red,seconds=round(time.monotonic()-start,3)),ensure_ascii=False),flush=True)
