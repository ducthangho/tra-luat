import importlib.util, pathlib, json, collections, re
R=pathlib.Path.cwd(); W=R.parent/'work'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
t=load('review_test',R/'ops/land_evidence_nguon_test.py'); d=load('review_dc',R/'ops/gate_output_doi_chieu.py')
original=t.nap; rows=[]; current=''
def nap():
 m=original(); f=m.l8
 def traced(tep,b,doc,prov,goc):
  rec={'case':current,'doc':doc,'module_real':(goc/'ops/gate_output_doi_chieu.py').exists() and (goc/'ops/gate_output_doi_chieu.py').read_bytes()==t.DOI_CHIEU.encode(),'claims':d.loi_khai(doc)}
  try: rec['result']=f(tep,b,doc,prov,goc); return rec['result']
  except BaseException as e: rec['exception']=type(e).__name__; raise
  finally: rows.append(rec)
 m.l8=traced; return m
t.nap=nap
rcs={}
for name in t.CA:
 if name.startswith(tuple('c'+str(i)+'_' for i in range(24,33))):
  current=name; rcs[name]=t.chay_ca(name)
real=[r for r in rows if r['module_real']]
claims=[(r,p,v) for r in real for p,v in r['claims']]
waived=[(r,p,v) for r,p,v in claims if d.token(v)=='owner_waived']
summary={'case_results':rcs,'real_calls':len(real),'token_counts':dict(collections.Counter(d.token(v) for r,p,v in claims)), 'waiver_calls':[{'case':r['case'],'value':v,'result':r.get('result')} for r,p,v in waived], 'new_case_claims':[{'case':r['case'],'claims':r['claims'],'doc':r['doc'],'result':r.get('result')} for r in real if not r['case'].startswith('c24')]}
(W/'matrix-observed.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=str)+'\n')
(W/'matrix-raw.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2,default=str)+'\n')
print('case results',rcs);print('real calls',len(real),'tokens',summary['token_counts']); print('waiver calls',summary['waiver_calls'])
assert all(v[0]==0 for v in rcs.values())
