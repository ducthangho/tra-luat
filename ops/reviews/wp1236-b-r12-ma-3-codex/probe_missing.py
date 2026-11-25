from pathlib import Path
import importlib.util,json,unicodedata
R=Path.cwd();W=R.parent/'work'
s=importlib.util.spec_from_file_location('t',R/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
header='# Danh gia Gate output run 10 attempt 20 head '+'a'*40+' — (danh_gia_gate.py sha256 '+'a'*64+')'
lines=[header,'JOB 31 ten [nhan] conclusion=success log_sha256='+'a'*64+' -> passed: x','JOB 42 x: skipped (khong tinh)','JOB 53 y: skipped -> not_measured (khong suy pass)','MOC_GATE_OUTPUT: passed (1/2 job co dau hieu duong)']
rows=[]
def check(label,ls,reason):
 filename='danh-gia-gate-output-10.txt';doc={'gate_output':f'measured — {filename}'}
 rc,out=t.chay(json.dumps(doc),{filename:'\n'.join(ls)},doi_chieu=t.DOI_CHIEU)
 got=t.dong_l8(out);want=[f'$.gate_output: danh_gia_khong_passed:{filename}:not_measured:{reason}']
 rows.append({'label':label,'rc':rc,'expected':want,'actual':got,'passed':rc==1 and got==want})
check('control syntax valid',lines,'bo_sinh_la')
for i in [2,3]:
 prefix='JOB '+('42' if i==2 else '53')+' ';suffix=lines[i][len(prefix)+1:]
 for label,name,reason in [('empty','','dong_la'),('nonBMP','𐐀','bo_sinh_la'),('delimiter inside name','a: skipped (khong tinh) b','bo_sinh_la')]:
  ls=lines.copy();ls[i]=prefix+name+suffix;check(f'skip {i} {label}',ls,reason)
# These data probes are not product code mutations.
for label,tail,reason in [('nonBMP','𐐀','bo_sinh_la'),('embedded LF','\nx','dau_tep_sai')]:
 ls=lines.copy();ls[0]=ls[0].replace('— (','— '+tail+'(');check('header tail '+label,ls,reason)
for label,value,reason in [('empty','','bo_sinh_la'),('nonBMP','𐐀','bo_sinh_la'),('forbidden bracket',']','dong_la')]:
 ls=lines.copy();ls[1]=ls[1].replace('[nhan]','['+value+']');check('label '+label,ls,reason)
(W/'missing-probes.json').write_text(json.dumps(rows,ensure_ascii=True,indent=2));print(json.dumps(rows,ensure_ascii=True,indent=2));assert all(r['passed'] for r in rows)
