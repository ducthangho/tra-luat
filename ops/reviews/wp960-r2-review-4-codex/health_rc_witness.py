import os,shutil,tempfile
from pathlib import Path
import replay_probe_recheck as h
with tempfile.TemporaryDirectory(prefix='r4-health-rc-') as td:
 root=Path(td);p=root/'repo';p.mkdir();k,sha,al=h.anc(p)
 bindir=root/'bin';bindir.mkdir();real=shutil.which('git');(bindir/'git').write_text('#!/bin/sh\ncase "$*" in *"rev-parse --git-dir"*) exit 3;; esac\nexec '+real+' "$@"\n');(bindir/'git').chmod(0o755);env={'PATH':str(bindir)+os.pathsep+os.environ['PATH']}
 for debt in [(),(h.KEY,)]:h.log(gate='head',debt=bool(debt),result=h.raw(p,al,debt,env=env))
 mutant=root/'mutant';shutil.copytree(h.COPY,mutant,symlinks=True);f=mutant/'ops/bien_nhan_v2.py';s=f.read_text();a='    if p.returncode != 0:\n';assert s.count(a)==1;f.write_text(s.replace(a,'    if False:\n'));old=h.b.__file__;h.b.__file__=str(f)
 try:
  for debt in [(),(h.KEY,)]:h.log(gate='u1-health-probe-rc',debt=bool(debt),result=h.raw(p,al,debt,env=env))
 finally:h.b.__file__=old
