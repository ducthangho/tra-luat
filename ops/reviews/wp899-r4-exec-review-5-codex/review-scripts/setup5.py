from pathlib import Path
import shutil,subprocess,sys,os,json,hashlib
R=Path('.review').resolve();root=R.parent
for x in ('tmp','cache'): (R/x).mkdir(exist_ok=True)
# Reuse prior measurement code only, never historical verdict emitters.
for p in (root/'.review-input/r4-luot4').glob('*.py'):
 if p.name not in ('setup_current.py','bootstrap.py','finalize_review.py','write_verdict_current.py'):
  s=p.read_text().replace('len(base)==47','len(base)==48').replace('len(rows)==13','len(rows)==13')
  (R/p.name).write_text(s)
for n in (1,2):
 shutil.copytree(root/f'.review-input/r4-luot4/prior{n}',R/f'prior{n}',dirs_exist_ok=True)
 for p in (R/f'prior{n}').rglob('*.py'):
  s=p.read_text().replace('47/47','48/48').replace('46/47','47/48').replace('155/155','209/209')
  p.write_text(s)
for p in R.glob('*.py'):
 if p.name=='setup5.py':continue
 s=p.read_text().replace('47/47','48/48').replace('46/47','47/48').replace('155/155','209/209')
 p.write_text(s)
def run(c):
 p=subprocess.run(c,capture_output=True);return {'command':c,'rc':p.returncode,'stdout':p.stdout.decode('utf8','replace'),'stderr':p.stderr.decode('utf8','replace')}
a=[run(['git',*v]) for v in [('remote','get-url','origin'),('rev-parse','HEAD','HEAD^{tree}','HEAD^'),('branch','--show-current'),('merge-base','--is-ancestor','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),('diff','--check','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),('diff','--numstat','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),('diff','--numstat','HEAD^','HEAD'),('config','--get','core.abbrev'),('rev-parse','--is-shallow-repository'),('status','--short')]]
a += [run(c) for c in [[sys.executable,'--version'],['git','--version'],['codex','--version'],[sys.executable,'-m','ruff','--version']]]
h={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (root/'.review-input').glob('wp899-r*.md')}
assert h['wp899-r4.md']['sha256']=='be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45'
(R/'preflight5.json').write_text(json.dumps({'commands':a,'specs':h},ensure_ascii=False,indent=2));print(json.dumps({'commands':a,'specs':h},ensure_ascii=False,indent=2))
for v,n in [(('diff','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'),'full.patch'),(('diff','HEAD^','HEAD'),'delta.patch')]:
 (R/n).write_bytes(subprocess.run(['git',*v],capture_output=True,check=True).stdout)
