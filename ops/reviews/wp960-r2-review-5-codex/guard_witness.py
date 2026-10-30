from pathlib import Path
import tempfile,os,shutil,importlib.util
import replay_probe_recheck as h
for name,a,z,mode in [('u1','    if con:\n','    if False:\n','stderr'),('u2','    nong = _git_do(root, "rev-parse", "--is-shallow-repository")[1].strip()','    nong = _chay_git(root, ("rev-parse", "--is-shallow-repository")).stdout.strip()','rc')]:
 t=h.t;old=t.bnv2;t._dot_bien_tep(a,z);mod=t.bnv2;t.bnv2=old
 with tempfile.TemporaryDirectory(prefix='r5-guard-witness-') as d:
  base=Path(d);p=base/'repo';p.mkdir();k,sha,al=h.anc(p);bindir=base/'bin';bindir.mkdir();f=bindir/'git';real=shutil.which('git')
  script='#!/usr/bin/env python3\nimport sys,subprocess\na=sys.argv[1:]\nif a[-2:]==["rev-parse","--is-shallow-repository"]:\n print("false")\n'
  script+=(' print("error: cannot inspect repository state",file=sys.stderr)\n sys.exit(0)\n' if mode=='stderr' else ' sys.exit(3)\n')
  script+='sys.exit(subprocess.run(['+repr(real)+',*a]).returncode)\n';f.write_text(script);f.chmod(0o755)
  for debt in ((),(h.KEY,)):
   for label,m in [('head',old),('mutant',mod)]:
    h.b=m
    try:h.log(mutant=name,module=label,debt=bool(debt),result=h.raw(p,al,debt,env={'PATH':str(bindir)+os.pathsep+os.environ['PATH']}))
    finally:h.b=old
 for p in t._TAM_DOT_BIEN:shutil.rmtree(p,ignore_errors=True)
 t._TAM_DOT_BIEN.clear()
