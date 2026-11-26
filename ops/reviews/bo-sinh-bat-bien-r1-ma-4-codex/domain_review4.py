from pathlib import Path
import subprocess,sys,os,json
w=Path(__file__).resolve().parent;r=Path(__import__('tempfile').mkdtemp(dir=w/'tmp',prefix='domain-review-'))/'repo';os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
subprocess.run(['git','clone','-q',str(w/'head'),str(r)],check=True)
A='ops/gate_output_doi_chieu_test.py';B='ops/land_evidence_nguon_test.py';src={p:(r/p).read_text() for p in [A,B]};rows=[]
c37='c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong';c39='c39_c37_do_khi_bo_sinh_lech_mien';c40='c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o';a136='a136_a135_do_khi_bo_sinh_lech_mien'
changes=[('missing-ASCII-NUL-replaced-U0081',B,'vu_tru = [*map(chr, range(128)),','vu_tru = [chr(0x81), *map(chr, range(1, 128)),',[c37,c39,c40], '2.1.1:128 ASCII'),('missing-ASCII-DEL-replaced-U0081',B,'vu_tru = [*map(chr, range(128)),','vu_tru = [*map(chr, range(127)), chr(0x81),',[c37,c39], '2.1.1:128 ASCII'),('total-plus2',B,'len(vu_tru) == 158 and','len(vu_tru) == 160 and',[c39],'2.1.1'),('count-minus2',B,'len(van_tay) == mong - lap','len(van_tay) == mong - lap - 2',[c40],'2.2.1'),('branch-true',B,'if tru is not None:','if True:',[c40],'2.2.2'),('branch-false',B,'if tru is not None:','if False:',[c40],'2.2.2'),('drop-final-bang',A,'bang(not lech, f"bộ sinh','bang(True, f"bộ sinh',[a136],'2.3.1')]
for label,p,old,new,cases,clause in changes:
 assert src[p].count(old)==1
 try:
  (r/p).write_text(src[p].replace(old,new))
  for ca in cases:
   q=subprocess.run([sys.executable,'-B',p,'--mot-ca',ca],cwd=r,capture_output=True,text=True)
   row=dict(id=label,path=p,old=old,new=new,case=ca,clause=clause,rc=q.returncode,stdout=q.stdout,stderr=q.stderr);rows.append(row);(w/'domain-review4.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(row,flush=True)
 finally:(r/p).write_text(src[p])
