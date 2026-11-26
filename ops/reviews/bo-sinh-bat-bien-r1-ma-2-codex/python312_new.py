from pathlib import Path
import subprocess,json,os,time
w=Path(__file__).resolve().parent;env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'));rows=[]
for file,case in [('ops/land_evidence_nguon_test.py','c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a'),('ops/land_evidence_nguon_test.py','c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o'),('ops/gate_output_doi_chieu_test.py','a135_bo_sinh_dung_mien_dac_ta'),('ops/gate_output_doi_chieu_test.py','a136_a135_do_khi_bo_sinh_lech_mien')]:
 cmd=['/usr/bin/python3.12','-B',file,'--mot-ca',case];t=time.monotonic();p=subprocess.run(cmd,cwd=w/'head',env=env,capture_output=True,text=True)
 rows.append(dict(command=cmd,rc=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=time.monotonic()-t));(w/'python312-new.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(case,p.returncode,flush=True)
