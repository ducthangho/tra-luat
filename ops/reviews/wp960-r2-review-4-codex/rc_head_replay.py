import os,shutil,tempfile
from pathlib import Path
import replay_probe_recheck as h
with tempfile.TemporaryDirectory(prefix='r3-rc-witness-') as td:
 root=Path(td); p=root/'repo';p.mkdir();k,sha,al=h.anc(p)
 git_real=shutil.which('git');scripts=root/'bin';scripts.mkdir();stub=scripts/'git'
 stub.write_text('#!/bin/sh\nfor arg do\n if [ "$arg" = "merge-base" ]; then exit 128; fi\ndone\nexec '+git_real+' "$@"\n');stub.chmod(0o755)
 env={'PATH':str(scripts)+os.pathsep+os.environ.get('PATH','')}
 h.log(healthy=h.raw(p,al),git_error=h.git(p,'merge-base','--is-ancestor',sha,'master',env=env))
 for no in ((),(h.KEY,)):h.log(gate='head',debt=bool(no),result=h.raw(p,al,no,env=env))
