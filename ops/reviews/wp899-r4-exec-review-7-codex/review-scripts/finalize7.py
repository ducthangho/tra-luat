from pathlib import Path
import json,subprocess,ast,hashlib,os,sys
R=Path('.review').resolve();root=R.parent
j=lambda n:json.loads((R/n).read_text())
required=['suite','audit','replay','checks','frontier6-targeted','frontier7-final','frontier7b','proofs7','proof-repairs','equivalence-new','nested-equivalence','env-equivalence','extras7','replay-more']
for name in required:
 d=j(name+'.json');assert d['returncode']==0,(name,d)
for z in j('replay-more7-results.json'):
 d=j(z['label']+'.json');assert d['returncode']==0,(z['label'],d)
assert all(z['rc']==0 or z['label'].endswith('composite_current.py') for z in j('remaining5-results.json'))
assert all(z['rc']==0 for z in j('legacy-after-suite6-results.json'))
cmds=[['git','rev-parse','--show-toplevel'],['git','rev-parse','HEAD','HEAD^{tree}'],['git','status','--porcelain=v1','--untracked-files=all'],['git','diff','--check','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'],['git','diff','--binary'],['git','diff','--cached','--binary']]
recs=[]
for c in cmds:
 p=subprocess.run(c,capture_output=True);recs.append({'command':c,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()});assert p.returncode==0,recs[-1]
assert recs[0]['stdout'].strip()==str(root)
assert recs[1]['stdout'].splitlines()==['9b329bfab0b38a821992a7105d479ca44bed389b','f107d82b2fd68d432f1298621d729de7ec2dd62e']
assert all(not recs[n]['stdout'] for n in [2,3,4,5])
(R/'final-git7.json').write_text(json.dumps(recs,ensure_ascii=False,indent=2))
n=next(x for x in ast.parse((R/'setup7.py').read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='snapshot')
exec(compile(ast.Module(body=[n],type_ignores=[]),'snapshot-only7','exec'))
end=snapshot();(R/'snapshot-end7.json').write_text(json.dumps(end,ensure_ascii=False,indent=2));start=j('snapshot-start.json')
a,b=start['files'],end['files'];diff={k:{'before':a.get(k),'after':b.get(k)} for k in set(a)|set(b) if a.get(k)!=b.get(k)}
comp={'head_tree_diff_index_equal':start['git']==end['git'],'files_start':len(a),'files_end':len(b),'outside_review_delta':diff,'equal':not diff and start['git']==end['git']}
(R/'snapshot-comparison7.json').write_text(json.dumps(comp,ensure_ascii=False,indent=2));assert comp['equal'],comp
for script in ['inventory7.py','write_verdict7.py']:
 p=subprocess.run([sys.executable,'-B',str(R/script)],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));(R/(script+'.stdout')).write_bytes(p.stdout);(R/(script+'.stderr')).write_bytes(p.stderr);assert p.returncode==0,(script,p.stdout,p.stderr)
v=(R/'VERDICT.md').read_text();assert v.startswith('verdict: changes_requested\nreviewed_sha: 9b329bfab0b38a821992a7105d479ca44bed389b\n')
assert all(f'| A{i} |' in v for i in range(1,28));assert all(f'| F{i:02d} ' in v for i in range(1,12))
files={}
for p in sorted(R.rglob('*')):
 if p.is_file() and not p.is_symlink() and p.name not in ('evidence-manifest7.json',):
  b=p.read_bytes();files[str(p.relative_to(R))]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(R/'evidence-manifest7.json').write_text(json.dumps({'reviewed_sha':recs[1]['stdout'].splitlines()[0],'tree':recs[1]['stdout'].splitlines()[1],'note':'All test writers ended; excludes this manifest; finalizer stdout/outer wrapper receipts produced after this instant are not included. CLI rollout/launcher post-run receipt is external and pending.','files':files},ensure_ascii=False,indent=2))
print('SNAPSHOT',len(a),'files equal outside .review; git clean')
print('VERDICT',j('verdict-summary7.json'))
print('ARTIFACTS',len(files))
