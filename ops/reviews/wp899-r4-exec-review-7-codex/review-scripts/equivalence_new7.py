from pathlib import Path
import runpy,importlib.util,json,yaml
R=Path(__file__).resolve().parent;root=R.parent;g=runpy.run_path(str(R/'frontier7.py'));out=R/'equivalent7';out.mkdir(exist_ok=True)
s=importlib.util.spec_from_file_location('t7eq',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
def load(p):
 s=importlib.util.spec_from_file_location('m7eq',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
mods={};records={}
for n,a,b in g['M']:
 if n not in ('mode_prior_strip_empty_run','log_header_full_timestamp_required'):continue
 p=out/(n+'.py');p.write_text(g['src'].replace(a,b));mods[n]=p
head=load(root/'ops/ci_provenance.py');mut=load(mods['mode_prior_strip_empty_run']);rs=[]
for v in (None,False,0,0.0,'',[],{},set(),b'',True,1,'echo hi','echo GITHUB_ENV','echo GITHUB_PATH',['GITHUB_ENV']):
 wf=yaml.safe_load(yaml.safe_dump({'jobs':{'j':{'steps':[{'run':v},{'run':t.X}]}}}));a,b=head.chan_buoc(wf,'j',1),mut.chan_buoc(wf,'j',1);rs.append({'value_type':type(v).__name__,'value':repr(v),'head':a,'mutant':b,'equal':a==b})
assert all(z['equal'] for z in rs);records['mode_prior_strip_empty_run']={'rows':rs,'argument':'All changed values are falsy safe YAML values. Their string forms contain neither source token; every truthy value is unchanged.'}
rs=[]
for prefix in (t.T+' ',t.T,'','2026-10-19T23:45:04Z ','2026-10-19T23:45:04.0Z ','2026-10-19T23:45:04 ','2026-10-19T23:45:04ZZ ','2026-10-19T23:45:04+00:00 '):
 pair=[]
 for p in (root/'ops/ci_provenance.py',mods['log_header_full_timestamp_required']):
  t.MA=p;b=t.buoc(t.X,'THU: 4/4 dat');b[0]=prefix+'##[group]Run '+t.X
  v=t.g1(t.wf_tu(t.X),b,sua=lambda st:st[2].update(started_at=t.T[:19]+'Z',completed_at=t.T[:19]+'Z'));pair.append(t.gate(v))
 rs.append({'prefix':prefix,'equal':pair[0]==pair[1],'ghep':[z['ghep_buoc'] for z in pair]})
assert all(z['equal'] for z in rs);records['log_header_full_timestamp_required']={'rows':rs,'argument':'A recognized valid timestamp gives the same gio. A raw non-timestamp Run header has an invalid first19 timestamp and already fails M12(c); a malformed timestamp that cannot be stripped does not open a Run group. Internal invalid gio values can differ, public output remains unchanged.'}
(R/'equivalence-new7-results.json').write_text(json.dumps(records,ensure_ascii=False,indent=2));print({k:len(v['rows']) for k,v in records.items()})
