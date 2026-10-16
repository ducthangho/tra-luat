import sys, importlib.util, pathlib, subprocess, os
sys.dont_write_bytecode=True
K=pathlib.Path('/home/user/rv773'); O=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('t',K/'ops/land_evidence_nguon_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
for args in t.DOT_BIEN:
 if args[0].startswith(('F01','F02','F03','F04','L5_doc')):
  print('OFFICIAL',args[0],t.chay_dot_bien(*args))
source=(K/'ops/land_evidence_nguon.py').read_text()
fixed=pathlib.Path('/tmp/rv773-null-fixed.py')
fixed.write_text(source.replace('if khoa is not None and khoa in da:', 'if k.tag != "tag:yaml.org,2002:merge" and khoa in da:'))
walker=pathlib.Path('/tmp/rv773-walker-fixed.py')
walker.write_text(source.replace('isinstance(nut, list) else ()','isinstance(nut, (list, tuple, set)) else ()'))
for name,hs,variant in [
 ('null',"null: 'measured — khong nguon'\nnull: ok\n",fixed),
 ('set',"x: !!set {'measured — khong nguon': null}\n",walker),
 ('omap',"x: !!omap [{a: 'measured — khong nguon'}]\n",walker),
]:
 with t.cay(hs,{'a.json':'{}'}) as g:
  for p in [K/'ops/land_evidence_nguon.py',variant]:
   r=subprocess.run(['python3.13','-B',str(p),'--root',str(g)],capture_output=True,text=True)
   print('AB',name,p.name,'rc',r.returncode,r.stdout.strip())
# Đi qua mọi ca trên bản gốc với chốt đã bỏ; dữ liệu chốt null không có trong test hiện hành.
for name,p in [('walker_support',walker),('null_key_support',fixed)]:
 results=[]
 for ca in t.CA:
  r=subprocess.run(['python3.13','-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',ca],capture_output=True,text=True,env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(p),PYTHONDONTWRITEBYTECODE='1'))
  results.append((ca,r.returncode))
 print('EXISTING_CASES',name,results)
