import audit as A
import pathlib, subprocess, sys, json
T=A.T
row=next(r for r in T.DB if r[0]=='M5g')
source=(A.DEV/'doc_receipt_thu_hoi_test.py').read_text()
needle='if re.match(r"\\s*K4\\b", x)'; assert source.count(needle)==1
assert row[4].count('"\\tK4:S fresh"')==1
for name,condition in [('head',needle),('r7_filter','if re.match(r"K4\\b", x)'),('r6_filter','if x.startswith("K4: ")')]:
 d=A.OUT/('m5g_'+name)/'.claude/dev';d.mkdir(parents=True,exist_ok=True)
 test=d/'doc_receipt_thu_hoi_test.py';test.write_text(source.replace(needle,condition))
 for f in ('doc_receipt_thu_hoi.py','ci_dang_ky_test.py'):(d/f).write_bytes((A.DEV/f).read_bytes())
 U=A.load(test,'test_'+name)
 mp=d/'payload.py';mp.write_text(A.edit(row[3],row[4]));m=A.load(mp,'payload_'+name)
 def run_case(module,case):
  try:U.chay_ca(module,mp,{case});return 'pass'
  except Exception as e:return type(e).__name__+': '+str(e)
 positive=run_case(m,'duong_fixture');target=run_case(m,'k4_base');baseline=run_case(A.M,'k4_base');disp=U.chay_dot_bien(A.SRC,row)
 A.emit(kind='M5g_discrimination',filter=name,baseline=baseline,positive=positive,target=target,disposition=disp,payload=row[4],result=m.kiem_json(T.ma(T.FIX),kho=T.KHO,nhanh='master',base_hien_hanh=T.X40,head_hien_hanh=T.H))
 assert baseline==positive=='pass'
 assert disp==(('witness_killed','giet') if name=='head' else ('unresolved','song'))
 assert target.startswith('TinHieuChotCa: k4_base: ly do K4 sai nghia:') if name=='head' else target=='pass'
 if name!='head':
  cmd=[sys.executable,'-B',str(test)];p=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
  (A.OUT/('m5g_'+name+'.log')).write_text(p.stdout+p.stderr)
  A.emit(kind='M5g_old_filter_suite',filter=name,command=cmd,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
  assert p.returncode==1 and 'M5g k4_mau_thuan: song' in p.stdout and '161/162 dot bien GIET' in p.stdout and 'unresolved 1' in p.stdout
