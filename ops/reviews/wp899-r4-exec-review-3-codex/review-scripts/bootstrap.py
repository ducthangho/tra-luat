from pathlib import Path
import os,sys,subprocess,json,hashlib,shutil
R=Path('.review').resolve(); root=Path.cwd()
os.environ['PYTHONDONTWRITEBYTECODE']='1'
for n in ('tmp','cache'): (R/n).mkdir(exist_ok=True)
for n in (1,2):
 src=root/f'.review-input/r4-luot{n}'; dst=R/f'prior{n}'; dst.mkdir(exist_ok=True)
 for p in src.glob('*.py'):
  s=p.read_text().replace('root=R.parent','root=Path.cwd()').replace('root = R.parent','root = Path.cwd()')
  # child replay scripts keep the explicitly assigned checkout; all writes in their own directory.
  (dst/p.name).write_text(s)
 for sub in ('old1','old2'):
  shutil.copytree(src/sub,dst/sub,dirs_exist_ok=True)
  for p in (dst/sub).rglob('*.py'):
   s=p.read_text().replace('root=R.parent','root=Path.cwd()').replace('root = R.parent','root = Path.cwd()')
   p.write_text(s)
shutil.copy2(root/'.review-input/r4-luot2/run.py',R/'run.py')
shutil.copy2(root/'.review-input/r4-luot2/snapshot.py',R/'snapshot.py')
shutil.copy2(root/'.review-input/r4-luot2/audit_mutants.py',R/'audit_mutants.py')
def run(cmd):
 p=subprocess.run(cmd,capture_output=True); return {'command':cmd,'rc':p.returncode,'stdout':p.stdout.decode('utf8','replace'),'stderr':p.stderr.decode('utf8','replace')}
cmds=[['git',*a] for a in [('remote','get-url','origin'),('rev-parse','HEAD','HEAD^{tree}','HEAD^'),('rev-parse','--is-shallow-repository'),('merge-base','--is-ancestor','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),('diff','--check','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),('diff','--numstat','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),('config','--get','core.abbrev'),('status','--short')]]
cmds += [[sys.executable,'--version'], ['git','--version'], ['codex','--version'], [sys.executable,'-m','ruff','--version']]
receipts=[run(c) for c in cmds]
for a,name in [(('diff','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),'full.patch'),(('diff','52e9573','HEAD'),'delta.patch')]:
 p=subprocess.run(['git',*a],capture_output=True); (R/name).write_bytes(p.stdout)
specs={}
for p in (root/'.review-input').glob('wp899-r*.md'):
 b=p.read_bytes();specs[p.name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(R/'preflight.json').write_text(json.dumps({'commands':receipts,'specs':specs},ensure_ascii=False,indent=2))
print(json.dumps({'commands':receipts,'specs':specs},ensure_ascii=False,indent=2))
