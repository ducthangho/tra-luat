import tempfile,subprocess
from pathlib import Path
import replay_probe_recheck as h
for vals in [('true','false'),('false',),('false','true')]:
 with tempfile.TemporaryDirectory(prefix='r5-git-promisor-') as d:
  base=Path(d);src=base/'src';src.mkdir();k=h.t._kho_cau(src);(src/'f.txt').write_text('foreign\n');k['g']('add','f.txt');k['g']('commit','-qm','F');oid=k['g']('rev-parse','HEAD');k['g']('config','uploadpack.allowAnySHA1InWant','true');k['g']('config','uploadpack.allowFilter','true');dst=base/'dst';dst.mkdir();q=h.t._kho_cau(dst);q['g']('remote','add','archive',src.as_uri())
  for val in vals:q['g']('config','--add','remote.archive.promisor',val)
  r=subprocess.run(['git','-c','protocol.allow=never','-c','protocol.file.allow=always','-C',str(dst),'cat-file','-t',oid],capture_output=True,text=True)
  h.log(vals=vals,effective=h.git(dst,'config','--type=bool','--get','remote.archive.promisor'),catfile_rc=r.returncode,out=r.stdout,err=r.stderr)
