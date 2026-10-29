from pathlib import Path
import importlib.util,tempfile,shutil,json
import replay_probe_recheck as h
for mutant in [False,True]:
 with tempfile.TemporaryDirectory(prefix='r4-baseline-refresh-') as d:
  base=Path(d);repo=base/'repo';repo.mkdir();k,sha,al=h.anc(repo)
  if mutant:
   copy=base/'copy';shutil.copytree(h.COPY,copy,symlinks=True);f=copy/'ops/bien_nhan_v2.py';s=f.read_text();a='    _NEN_STDERR[str(root)] = frozenset(d for d in p.stderr.splitlines() if d.strip())\n';z='    _NEN_STDERR.setdefault(str(root), frozenset(d for d in p.stderr.splitlines() if d.strip()))\n';assert s.count(a)==1;f.write_text(s.replace(a,z));sp=importlib.util.spec_from_file_location('test_refresh',copy/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(sp);sp.loader.exec_module(t)
  else:t=h.t
  r1=t._chay_cli(repo,al);k['g']('config','core.fsyncObjectFiles','true');r2=t._chay_cli(repo,al);h.log(mutant=mutant,before=r1,after=r2)
