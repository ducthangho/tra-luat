from pathlib import Path
import subprocess,sys,os,json,hashlib,stat
R=Path('.review').resolve(); root=R.parent
for x in ('tmp','cache'): (R/x).mkdir(exist_ok=True)
def snapshot():
 paths=subprocess.run(['git','ls-files','-z','--cached','--others','--exclude-standard'],capture_output=True,check=True).stdout.split(b'\0')
 paths+=subprocess.run(['git','ls-files','-z','--others','--ignored','--exclude-standard'],capture_output=True,check=True).stdout.split(b'\0')
 data={}
 for b in sorted(set(paths)):
  if not b:continue
  p=Path(os.fsdecode(b))
  if p.parts[0] in ('.review',):continue
  if p.is_symlink():data[str(p)]={'link':os.readlink(p)}
  elif p.is_file():data[str(p)]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 return {'files':data,'git':{x:subprocess.run(['git',*v],capture_output=True).stdout.decode() for x,v in {'head':['rev-parse','HEAD'],'tree':['rev-parse','HEAD^{tree}'],'status':['status','--porcelain=v1','--untracked-files=all'],'diff':['diff','--binary'],'index':['diff','--cached','--binary']}.items()}}
(R/'snapshot-start.json').write_text(json.dumps(snapshot(),ensure_ascii=False,indent=2))
cmds=[['git',*v] for v in [('remote','get-url','origin'),('rev-parse','HEAD','HEAD^{tree}','HEAD^'),('branch','--show-current'),('merge-base','--is-ancestor','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),('diff','--check','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),('diff','--numstat','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),('diff','--numstat','HEAD^','HEAD'),('config','--get','core.abbrev'),('rev-parse','--is-shallow-repository'),('status','--short')]]
cmds += [[sys.executable,'--version'],['git','--version'],['codex','--version'],[sys.executable,'-m','ruff','--version'],[sys.executable,'-B','-c','import yaml,platform;print(yaml.__version__,platform.platform())']]
a=[]
for c in cmds:
 p=subprocess.run(c,capture_output=True);a.append({'command':c,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()})
h={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (root/'.review-input').glob('wp899-r*.md')}
assert h['wp899-r4.md']['sha256']=='be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45'
(R/'preflight6.json').write_text(json.dumps({'commands':a,'specs':h},ensure_ascii=False,indent=2))
for v,n in [(('diff','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),'full.patch'),(('diff','HEAD^','HEAD'),'delta.patch')]:
 (R/n).write_bytes(subprocess.run(['git',*v],capture_output=True,check=True).stdout)
(R/'run.py').write_bytes((root/'.review-input/r4-luot5/run.py').read_bytes())
print(json.dumps({'commands':a,'specs':h},ensure_ascii=False,indent=2))
