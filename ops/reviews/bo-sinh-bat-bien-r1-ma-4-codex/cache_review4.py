from pathlib import Path
import importlib.util,sys,json,os,time,gc,weakref
w=Path(__file__).resolve().parent;r=w/'head';os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'));p=r/'ops/gate_output_doi_chieu_test.py'
def load():
 sp=importlib.util.spec_from_file_location('cache_a',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
allrows={};cost=[]
for enabled in [True,False]:
 m=load();rows=[]
 if not enabled:m._bo_sinh_nho=lambda f,cam,bo=():tuple(f(cam,bo))
 def profile(frame,event,arg):
  if event=='return' and frame.f_code.co_name=='chay_ca':rows.append(dict(case=frame.f_locals.get('ten'),rc=arg[0],output=arg[1]))
 sys.setprofile(profile)
 for case in ['a135_bo_sinh_dung_mien_dac_ta','a136_a135_do_khi_bo_sinh_lech_mien']:
  start=time.perf_counter();out=m.chay_ca(case);cost.append(dict(cache=enabled,case=case,seconds=time.perf_counter()-start,rc=out[0],output=out[1]))
 sys.setprofile(None);allrows[str(enabled)]=rows
assert allrows['True']==allrows['False']
m=load();calls=[];refs=[]
for i in range(1000):
 f=lambda cam,bo=(),i=i:(str(i),)
 refs.append(weakref.ref(f));assert m._bo_sinh_nho(f,'x')==(str(i),)
del f;gc.collect()
unit=dict(strong_function_refs=sum(ref() is not None for ref in refs),keys=len(m._NHO_BO_SINH),cache_trace_equal=True)
s=['original'];f=lambda cam,bo=():s
first=m._bo_sinh_nho(f,'x');s[0]='changed';unit['source_list_does_not_contaminate']=m._bo_sinh_nho(f,'x')==('original',)
try:first[0]='mutate'
except TypeError:unit['returned_tuple_immutable']=True
# Same function and different arguments must remain distinct; objects remain strongly held.
f=lambda cam,bo=():(cam,*bo)
unit['argument_keys_separate']=m._bo_sinh_nho(f,'x',('Cs',))!=m._bo_sinh_nho(f,'x',())!=m._bo_sinh_nho(f,'y',())
(w/'cache-review4.json').write_text(json.dumps(dict(traces=allrows,cost=cost,unit=unit),ensure_ascii=False,indent=2));print(unit)
# True extra-case cost in the same process, without profiler overhead, three runs.
for i in range(3):
 m=load();st=time.perf_counter();a=m.chay_ca('a135_bo_sinh_dung_mien_dac_ta');b=m.chay_ca('a136_a135_do_khi_bo_sinh_lech_mien');cost.append(dict(sample=i,combined_seconds=time.perf_counter()-st,a=a,b=b))
(w/'new-code-cost.json').write_text(json.dumps(cost,ensure_ascii=False,indent=2));print(cost)
