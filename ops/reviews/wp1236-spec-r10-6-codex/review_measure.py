import os, sys, json, hashlib, subprocess, time, platform
from pathlib import Path
W=Path(__file__).resolve().parent; R=W.parent/'repo'; C=W.parent/'ma_r9_git'
def sha(b): return hashlib.sha256(b).hexdigest()
def save(name,obj): (W/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def snap():
 out={}
 for label,root in [('repo',R),('ma_r9_git',C)]:
  files={}
  for d,ds,fs in os.walk(root):
   ds[:]=[x for x in ds if x!='.git']
   for f in fs:
    p=Path(d)/f
    if p.is_symlink(): files[str(p.relative_to(root))]=['link',os.readlink(p)]
    elif p.is_file(): files[str(p.relative_to(root))]=['file',p.stat().st_mode,sha(p.read_bytes())]
  git={}
  for args in [['rev-parse','HEAD','HEAD^{tree}'],['status','--porcelain=v1','--untracked-files=all','--ignored=matching'],['diff','--binary'],['diff','--cached','--binary'],['remote','get-url','origin'],['config','--get','core.abbrev'],['rev-parse','--is-shallow-repository']]:
   p=subprocess.run(['git','-C',str(root),*args],capture_output=True); git[' '.join(args)]={'rc':p.returncode,'out':p.stdout.decode(),'err':p.stderr.decode()}
  out[label]={'files':files,'git':git}
 return out
if __name__=='__main__':
 save(sys.argv[1],snap()); print('SNAPSHOT_COMPLETE',sys.argv[1])
