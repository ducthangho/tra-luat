from pathlib import Path
import importlib.util,json,hashlib,sys,pickle,yaml
w=Path(__file__).resolve().parent;r=w/'head';p=r/'ops/land_evidence_nguon_test.py';src=p.read_text()
rows=[]
def load(p,s,name):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);exec(compile(s,str(p),'exec'),m.__dict__);return m
for mode,s in [('cached',src),('uncached',src.replace('    return goi\n','    return ham\n'))]:
 assert src.count('    return goi\n')==1
 b=load(p,s,'b_'+mode);oldnap=b.nap;inputs=[];cases=[];allcases=[]
 def nap():
  m=oldnap();original=m.main
  def main(args):
   path=Path(args[args.index('--tep')+1]);prov=path.parent/b.PROV
   payload=(path.read_bytes(),*((f.relative_to(path.parent).as_posix(),f.read_bytes()) for f in sorted(prov.rglob('*')) if f.is_file()))
   inputs.append(hashlib.sha256(repr(payload).encode()).hexdigest());return original(args)
  m.main=main;return m
 b.nap=nap;oldcase=b.chay_ca
 def case(name):
  st=len(inputs);rc,dong=oldcase(name);entry=dict(case=name,rc=rc,output=dong,inputs=inputs[st:]);allcases.append(entry);return rc,dong
 b.chay_ca=case
 def prof(frame,event,arg):
  if event=='return' and frame.f_code.co_name=='chay_ca' and str(frame.f_locals.get('ten','')).startswith('a'):
   cases.append({'case':frame.f_locals['ten'],'result':arg})
 sys.setprofile(prof)
 out1=b.chay_ca('c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a');out2=b.chay_ca('c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o')
 sys.setprofile(None)
 rows.append(dict(mode=mode,c36=out1,c40=out2,calls=allcases,a_calls=cases,cache_size=len(b.NHO_YAML)))
 (w/'cache-review.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(mode,out1,out2,'L8 inputs',len(inputs),'cache',len(b.NHO_YAML),flush=True)
print('exact input and result equality',rows[0]['calls']==rows[1]['calls'],rows[0]['a_calls']==rows[1]['a_calls'],flush=True)
b=load(p,src,'cache_unit');calls=[]
def ham(x,**kw):calls.append((x,kw));return yaml.safe_load(x)
f=b.nho_dem('safe_load',ham)
(w/'yaml-one.yaml').write_bytes(b'a: [1]\n');(w/'yaml-two.yaml').write_bytes(b'a: [2]\n');x=(w/'yaml-one.yaml').read_bytes();y=(w/'yaml-two.yaml').read_bytes();first=f(x);first['a'].append(9);checks={'one_byte_different':sum(a!=c for a,c in zip(x,y))==1,'first':first,'reread':f(x),'other':f(y),'underlying_calls':len(calls)}
f2=b.nho_dem('other_name',ham);f2(x);checks['name_separated']=len(calls)==3
f(x,extra_flag=1) if False else None
# kwargs partition without relying on unsupported yaml args
q=b.nho_dem('kwargs',lambda x,**k:k);checks['kwargs_values']=[q(x,z=1),q(x,z=2)]
f3=b.nho_dem('safe_dump',yaml.safe_dump);doc={'a':1};normal=f3(doc);binary=pickle.dumps(doc);cached_binary=f3(binary)
checks['out_of_actual_domain_type_collision']={'cached':cached_binary,'actual':yaml.safe_dump(binary),'different':cached_binary!=yaml.safe_dump(binary)}
(w/'cache-unit.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2));print(checks,flush=True)
# a136 cache bypass: trace every a135 return with cache on/off, exact same generator variants.
ap=r/'ops/gate_output_doi_chieu_test.py';asrc=ap.read_text();anchor='return nho.get((cam, tuple(bo))) or nho.setdefault((cam, tuple(bo)), that(cam, bo))';assert asrc.count(anchor)==1
ars=[]
for mode,s in [('cached',asrc),('uncached',asrc.replace(anchor,'return that(cam, bo)'))]:
 a=load(ap,s,'a_'+mode);trace=[]
 def prof(frame,event,arg):
  if event=='return' and frame.f_code.co_name=='chay_ca':trace.append(dict(case=frame.f_locals['ten'],result=arg))
 sys.setprofile(prof);out=a.chay_ca('a136_a135_do_khi_bo_sinh_lech_mien');sys.setprofile(None)
 ars.append(dict(mode=mode,out=out,calls=trace));print('a136',mode,out,flush=True)
(w/'a136-cache.json').write_text(json.dumps(ars,ensure_ascii=False,indent=2))
# Inspect closure-local cache without altering repository files.
a=load(ap,asrc,'a_cache_closure');captured=[]
def prof(frame,event,arg):
 if event=='return' and frame.f_code.co_name=='a136_a135_do_khi_bo_sinh_lech_mien':captured.append(frame.f_locals.copy())
sys.setprofile(prof);out=a.chay_ca('a136_a135_do_khi_bo_sinh_lech_mien');sys.setprofile(None)
loc=captured[0];goc=loc['goc'];nho=loc['nho'];before=len(nho);v1=goc('X',());v2=goc('Y',());distinct_keys=('X',()) in nho and ('Y',()) in nho
try:v1[0]='A';immutable=False
except TypeError:immutable=True
# A second a136 invocation owns a different dictionary, so it cannot borrow old mutant data.
captured=[];sys.setprofile(prof);out2=a.chay_ca('a136_a135_do_khi_bo_sinh_lech_mien');sys.setprofile(None)
report={'first_rc':out[0],'second_rc':out2[0],'one_byte_arguments_have_distinct_keys':distinct_keys,'cache_size_before':before,'tuple_result':isinstance(v1,tuple),'cannot_mutate_result':immutable,'fresh_dictionary_per_call':captured[0]['nho'] is not nho,'keys_argument_inventory':[repr(x) for x in nho]}
(w/'a136-cache-unit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(report,flush=True)
