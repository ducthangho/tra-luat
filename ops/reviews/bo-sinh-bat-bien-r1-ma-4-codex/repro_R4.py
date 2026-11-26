"""Independent R4 repro: always fresh clone below work/tmp; never changes reviewed repo."""
from pathlib import Path
import tempfile,subprocess,os,sys,json
w=Path(__file__).resolve().parent;os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
A='ops/gate_output_doi_chieu_test.py';B='ops/land_evidence_nguon_test.py';rows=[]
with tempfile.TemporaryDirectory(dir=w/'tmp',prefix='repro-R4-') as d:
 r=Path(d)/'repo';subprocess.run(['git','clone','-q',str(w/'head'),str(r)],check=True)
 original={p:(r/p).read_text() for p in [A,B]}
 cases={A:['a135_bo_sinh_dung_mien_dac_ta','a136_a135_do_khi_bo_sinh_lech_mien'],B:['c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong','c39_c37_do_khi_bo_sinh_lech_mien']}
 changes=[('ASCII-NUL-lost',B,[("vu_tru = [*map(chr, range(128)),","vu_tru = [chr(0x81), *map(chr, range(1, 128)),")]),('fifth-argument-lost',A,[('_mau_loai_unicode("\\r\\n", {"Cs"})','_mau_loai_unicode("\\r", {"Cs"})'),('("\\r\\n", ("Cs",), 30, ("Cs",))','("\\r", ("Cs",), 30, ("Cs",))')])]
 for label,p,edits in changes:
  for side in ['healthy','mutant']:
   s=original[p]
   if side=='mutant':
    for old,new in edits:
     assert s.count(old)==1,(label,old,s.count(old));s=s.replace(old,new)
   (r/p).write_text(s)
   for ca in cases[p]:
    q=subprocess.run([sys.executable,'-B',p,'--mot-ca',ca],cwd=r,capture_output=True,text=True)
    row=dict(probe=label,side=side,case=ca,rc=q.returncode,stdout=q.stdout,stderr=q.stderr,edits=edits);rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
   (r/p).write_text(original[p])
(w/'repro-R4.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
