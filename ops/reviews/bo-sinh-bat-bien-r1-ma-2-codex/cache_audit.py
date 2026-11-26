from pathlib import Path
import importlib.util,json,os,hashlib
w=Path(__file__).resolve().parent;r=w/'head'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
p=r/'ops/land_evidence_nguon_test.py';src=p.read_text()
anchor='return goi\n    khong_khop =';assert src.count(anchor)==1
rows=[]
for label,s in [('cached',src),('uncached',src.replace(anchor,'return ham\n    khong_khop ='))]:
 sp=importlib.util.spec_from_file_location('b_'+label,p);b=importlib.util.module_from_spec(sp);exec(compile(s,str(p),'exec'),b.__dict__)
 old=b.nap;inputs=[];cases=[];oldcase=b.chay_ca
 def nap():
  m=old();main=m.main
  def observe(args):
   path=Path(args[args.index('--tep')+1]);pvs=path.parent/b.PROV
   payload=(path.read_bytes(),*((f.relative_to(path.parent).as_posix(),f.read_bytes()) for f in sorted(pvs.rglob('*')) if f.is_file()))
   inputs.append(hashlib.sha256(repr(payload).encode()).hexdigest())
   return main(args)
  m.main=observe;return m
 def case(name):
  start=len(inputs);out=oldcase(name)
  if name.startswith('c36'):cases.append(dict(case=name,rc=out[0],output=out[1],samples=inputs[start:]))
  return out
 b.nap=nap;b.chay_ca=case
 out=b.chay_ca('c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o')
 rows.append(dict(label=label,rc=out[0],output=out[1],cases=cases))
 (w/'cache-audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 print(label,out,'samples',len(inputs),'cases',len(cases),flush=True)
print('exact_L8_input_sequence_and_results_equal',rows[0]['cases']==rows[1]['cases'],flush=True)
