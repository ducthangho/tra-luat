from pathlib import Path
import hashlib,json,ast
R=Path('.review').resolve();root=R.parent;rows=[]
for n in (1,2,3,4):
 for p in sorted((root/f'.review-input/r4-luot{n}').glob('*.py')):
  role='verification'
  if p.name in ('write_verdict.py','write_current_verdict.py','final_check.py','finalize_current.py','run.py','snapshot.py','emit.py','preflight.py','bootstrap.py','prepare.py','adapt_prior.py','make_frontier2.py','extend_cases.py'):role='historical_setup_or_rendering'
  rows.append({'round':n,'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':role})
(R/'prior-script-inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
# Keep a raw-anchor audit separate from transparently rebased scripts.
src=(root/'ops/ci_provenance.py').read_text();anchors=[]
for name in ('frontier.py','frontier2.py'):
 tree=ast.parse((root/'.review-input/r4-luot3'/name).read_text())
 node=next(z for z in tree.body if isinstance(z,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='M' for t in z.targets))
 for name,old,new in ast.literal_eval(node.value):anchors.append({'name':name,'old':old,'new':new,'raw_anchor_count':src.count(old),'replacement_equal_current':src.count(new)==1 if src.count(old)==0 else False})
(R/'raw-frontier-anchors.json').write_text(json.dumps(anchors,ensure_ascii=False,indent=2))
print('script inventory',len(rows),'raw anchors',len(anchors),'obsolete',[a['name'] for a in anchors if a['raw_anchor_count']!=1])
