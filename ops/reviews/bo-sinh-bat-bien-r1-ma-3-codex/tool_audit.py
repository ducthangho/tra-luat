from pathlib import Path
import importlib.util, json, sys, subprocess
w=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('table',w/'bang_toan_tu.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
r=w/'tool-copy';subprocess.run(['git','clone','-q',str(w/'head'),str(r)],check=True)
rows=[]
for label,tep,ca,old,new in [
 ('comment-survives',t.A,t.A136,'# #1539: MIỀN','# reviewer comment #1539: MIỀN'),
 ('syntax-error',t.A,t.A136,'def kiem_bo_sinh(bo_sinh):','def kiem_bo_sinh(bo_sinh) BROKEN:'),
 ('outer-TypeError',t.A,t.A136,'    that, a135, cam_3, nho =','    raise TypeError("REVIEW_INJECTED_OUTER")\n    that, a135, cam_3, nho ='),
 ('inner-TypeError',t.A,t.A136,'    for cam, bo_loai, so, vang in BO_SINH_MONG:','    raise TypeError("REVIEW_INJECTED_INNER")\n    for cam, bo_loai, so, vang in BO_SINH_MONG:'),
 ('wrong-case-DO',t.A,t.A136,'def chay_ca(ten):\n','def chay_ca(ten):\n    return 3, \"DO:UNRELATED:injected\"\n'),
]:
 row=dict(label=label,cu=old,moi=new,**t.mot(r,tep,ca,old,new));rows.append(row);print(row,flush=True)
(w/'tool-audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
# Test main return code and real table generation for live/error instead of only calling mot.
for label,neo,moi in [('live','# #1539: MIỀN','# reviewer comment #1539: MIỀN'),('error','def kiem_bo_sinh(bo_sinh):','def kiem_bo_sinh(bo_sinh) BROKEN:')]:
 t.M=[('review-control',t.A,t.A136,neo,{'bo':moi})];t.TD={};sys.argv=['bang_toan_tu.py','--goc',str(w/'head'),'--ra',str(w/f'tool-main-{label}'),'--song-song','1'];rc=t.main();print('MAIN',label,rc,flush=True)
 rows.append(dict(label='main-'+label,rc=rc))
(w/'tool-audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
