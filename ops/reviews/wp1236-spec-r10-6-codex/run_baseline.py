import os, importlib.util, json, sys, time
from review_measure import W,R,C,save
os.environ['TMPDIR']=str(W/'tmp');sys.dont_write_bytecode=True
p=C/'ops/gate_output_doi_chieu_test.py';s=importlib.util.spec_from_file_location('native_baseline',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
t=time.monotonic();out=[]
for k in m.CA:
 rc,d=m.chay_ca(k);out.append({'case':k,'rc':rc,'output':d});save('baseline_cases.json',out);print(k,rc,flush=True)
save('baseline_summary.json',{'cases':len(out),'pass':sum(x['rc']==0 for x in out),'seconds':time.monotonic()-t,'loader':'yaml.safe_load unchanged'})
assert len(out)==36 and all(x['rc']==0 for x in out)
print('BASELINE_36_36',flush=True)
