import tempfile,shutil
from pathlib import Path
import replay_probe_recheck as h
with tempfile.TemporaryDirectory(prefix='r4-health-env-') as d:
 base=Path(d);p=base/'repo';p.mkdir();k,sha,al=h.anc(p);env={'GIT_DIR':str(base/'nonexistent.git')}
 h.log(gate='head',result=h.raw(p,al,env=env))
 dst=base/'mutant';shutil.copytree(h.COPY,dst,symlinks=True);f=dst/'ops/bien_nhan_v2.py';s=f.read_text();a='timeout=timeout, env=_env_git())';z='timeout=timeout, env=(os.environ if tuple(args) == ("rev-parse", "--git-dir") else _env_git()))';assert s.count(a)==1;f.write_text(s.replace(a,z));old=h.b.__file__;h.b.__file__=str(f)
 try:h.log(gate='u2b-health-probe-environment',result=h.raw(p,al,env=env))
 finally:h.b.__file__=old
