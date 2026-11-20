import pathlib,json,importlib.util,yaml,copy,sys,tempfile,shutil
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo'
def load(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
t=load(r/'ops/gate_output_doi_chieu_test.py','t');g=load(r/'ops/gate_output_doi_chieu.py','g');real=next((r/'ops/land').glob('pr1378*-land-evidence.yaml'));base=yaml.safe_load(real.read_bytes())
def neutral(x):
 if isinstance(x,dict):
  for k,v in x.items():
   c=g._chuan(k)
   if 'gateoutput' in c and c not in g.PHI_LOI_KHAI:x[k]='not_measured'
   else:neutral(v)
 elif isinstance(x,list):
  for v in x:neutral(v)
neutral(base)
changes=[('control',None),('head',lambda y:y['moc']['run'].update(head_sha='0'*40)),('run',lambda y:y['moc']['run'].update(run_id=y['moc']['run']['run_id']+1)),('attempt',lambda y:y.update(attempt_yeu_cau=2)),('schema',lambda y:y.update(schema='ci_provenance/2')),('event',lambda y:y['moc']['run'].update(event='workflow_dispatch')),('path',lambda y:y['moc']['run'].update(loi_khai_rest_path='.github/workflows/other.yml')),('run_flag',lambda y:y['moc']['run'].update(trang_thai='not_measured')),('jobs_flag',lambda y:y['moc']['gate_output']['tap_jobs'].update(trang_thai='not_measured')),('checkout_empty',lambda y:y['moc'].update(checkout=[])),('jobs_missing',lambda y:y['moc']['gate_output']['jobs'].pop()),('job_name',lambda y:y['moc']['gate_output']['jobs'][0].update(name='changed')),('job_conclusion',lambda y:y['moc']['gate_output']['jobs'][0].update(conclusion='cancelled')),('job_labels',lambda y:y['moc']['gate_output']['jobs'][0].update(labels=['changed'])),('log_hash',lambda y:next(iter(y['log_day_du'].values())).update(sha256='0'*64)),('duplicate_job',lambda y:y['moc']['gate_output']['jobs'].append(copy.deepcopy(y['moc']['gate_output']['jobs'][0])))]
rows=[]
for name,fp in changes:
 with t.mini('T-v3-pass',None,fp) as (f,d):
  new=d/pathlib.Path(t.FX['T-v3-pass'][0]).name;f.rename(new);doc=copy.deepcopy(base);doc['gate_output']='passed — '+new.name;vp=g.kiem_ho_so(doc,d);ok=(not vp) if name=='control' else bool(vp);row={'name':name,'violations':vp,'ok':ok};rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
# The same real record with no matching provenance and all allowed negative tokens.
for tk in ['passed','measured','not_measured','not_run','skipped','failed']:
 with t.mini('T-v3-pass') as (f,d):
  new=d/pathlib.Path(t.FX['T-v3-pass'][0]).name;f.rename(new);(d/'prov.yaml').unlink();doc=copy.deepcopy(base);doc['gate_output']=tk+' — '+new.name;vp=g.kiem_ho_so(doc,d);row={'name':'missing_prov:'+tk,'violations':vp,'ok':bool(vp)};rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
variants={x['id']:x for x in map(json.loads,(w/'extra_mutants.jsonl').read_text().splitlines())}; contrasts=[]
for n in ['phi_substring','phi_skip_descendants','waiver_no_strip','waiver_head_truthy']:
 p=w/'contrast_modules'/(n+'.py');p.write_text(variants[n]['src']);m=load(p,n)
 with tempfile.TemporaryDirectory() as dd:
  d=pathlib.Path(dd)
  if n.startswith('phi_'):
   doc=copy.deepcopy(base);doc['landed']=False
   if n=='phi_substring':doc['moc_gate_output_nguon']='passed — missing.txt'
   else:doc['gate_output_nguon']={'gate_output':'passed — missing.txt'}
   a,b=g.kiem_ho_so(doc,d),m.kiem_ho_so(doc,d)
  else:
   rb=t.rb(t.DONG);v=t.URL+' '+t.SHA;head=None
   if n=='waiver_no_strip':rb['body']='  '+rb['body']+'  '
   else:head=''
   (d/'readback-case-issuecomment-123.json').write_text(json.dumps(rb));a,b=g.kiem_mien(v,d,head),m.kiem_mien(v,d,head)
  contrasts.append({'id':n,'original':a,'mutant':b,'different':a!=b})
(w/'consumer_matrix.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(w/'extra_contrasts.json').write_text(json.dumps(contrasts,ensure_ascii=False,indent=2));print('EXTRA',json.dumps(contrasts,ensure_ascii=False));sys.exit(0 if all(x['ok'] for x in rows) else 1)
