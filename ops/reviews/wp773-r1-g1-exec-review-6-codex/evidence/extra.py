import sys, pathlib, importlib.util, os, subprocess
sys.dont_write_bytecode=True
K=pathlib.Path('/home/user/rv773'); O=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('t',K/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
for name,old,new,ca in [('l2-content','if not any(mau.search(nd) for nd in noi_dung):','if False:','c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van')]:
 src=(K/'ops/land_evidence_nguon.py').read_text(); assert src.count(old)==1
 p=pathlib.Path('/tmp/rv773-r6-'+name+'.py');p.write_text(src.replace(old,new))
 r=subprocess.run([sys.executable,'-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',ca],capture_output=True,text=True,env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(p)))
 print(name,r.returncode,r.stdout,r.stderr)
print('violation distribution no-exemption', {law:(O/'no-exemption.log').read_text().count('  '+law+' ') for law in ['L1','L2','L3']})
