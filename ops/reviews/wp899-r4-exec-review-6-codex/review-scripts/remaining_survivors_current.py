from pathlib import Path
import os,json,sys,importlib.util,contextlib
import yaml
R=Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
rows=[]
@contextlib.contextmanager
def source(name):
 old=os.environ.get('CI_PROVENANCE_MA'); oldma=t.MA
 t.MA=R/('mutants' if name=='L3_endgroup_startswith' else 'frontier')/(name+'.py') if name else root/'ops/ci_provenance.py'
 if name:os.environ['CI_PROVENANCE_MA']=str(R/('mutants' if name=='L3_endgroup_startswith' else 'frontier')/(name+'.py'))
 else:os.environ.pop('CI_PROVENANCE_MA',None)
 try:yield
 finally:
  t.MA=oldma
  if old is None:os.environ.pop('CI_PROVENANCE_MA',None)
  else:os.environ['CI_PROVENANCE_MA']=old
for name,scenario in [('dd_output_dedupe','duplicate'),('L3_endgroup_startswith','suffix')]:
 rec={'mutant':name,'scenario':scenario,'observed':[]}
 for mut in (None,name):
  with source(mut):
   if scenario=='nonstr':
    w=t.wf_tu(t.X,buoc_them={'name':'K','run':5})
    p=t.g1(w,t.buoc('5','THU: 4/4 dat'),sua=lambda st:st[2].update(name='K'),w_rest=t.wf_tu(t.X))
   elif scenario=='duplicate':p=t.g1(t.wf_tu(t.X+'\n'+t.X),t.khoi([t.X,t.X],'THU: 4/4 dat'))
   else:
    b=t.buoc(t.X,'THU: 4/4 dat');b[3]+='suffix';p=t.g1(t.wf_tu(t.X),b)
   rec['observed'].append({'source':mut or 'HEAD','gate':t.gate(p)})
 rows.append(rec)
# Compare both original/weak predicate before and after shell and in output.
equal=[]
for position in (0,1,2,3,4,5):
 b=t.buoc(t.X,'THU: 4/4 dat');b.insert(position,t.T+' ##[group]details')
 pair=[]
 for mut in (None,'log_nested_after_only'):
  with source(mut):pair.append(t.gate(t.g1(t.wf_tu(t.X),b)))
 equal.append({'position':position,'same_output':pair[0]==pair[1],'gate':pair[0]})
assert all(x['same_output'] for x in equal)
(R/'remaining-survivor-details.json').write_text(json.dumps({'rows':rows,'nested_equivalence':equal},ensure_ascii=False,indent=2))
for r in rows:print(r['mutant'],[(x['gate']['ghep_buoc'],x['gate']['kich_ban']['buoc_xac_thuc'],x['gate']['dau_duong']) for x in r['observed']])
print('nested equivalence',len(equal),'/',len(equal))
