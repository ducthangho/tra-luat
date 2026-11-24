from pathlib import Path
import importlib.util,json
R=Path.cwd();W=R.parent/'work'
s=importlib.util.spec_from_file_location('t',R/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
p=t.prov_that();hs=json.dumps({'gate_output':'passed — '+t.DG});rows=[]
for label,old,new,reason in [('control',None,None,None),('header','# Danh gia Gate output','# Broken gate output','dau_tep_sai'),('job','\nJOB ','\nXOB ','dong_la'),('summary','\nMOC_GATE_OUTPUT:','\nXOC_GATE_OUTPUT:','dong_la,thieu_moc')]:
 q=dict(p)
 if old:
  assert old in q[t.DG]
  q[t.DG]=q[t.DG].replace(old,new,1)
 rc,out=t.chay(hs,q,doi_chieu=t.DOI_CHIEU)
 expected=[] if not reason else [f'$.gate_output: danh_gia_khong_passed:{t.DG}:not_measured:{reason}']
 actual=t.dong_l8(out);ok=(rc,actual)==(1 if reason else 0,expected)
 rows.append({'label':label,'rc':rc,'expected':expected,'actual':actual,'passed':ok});print(label,rc,actual,ok)
(W/'grammar-probes.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
assert all(x['passed'] for x in rows)
print('TOTAL 4/4')
