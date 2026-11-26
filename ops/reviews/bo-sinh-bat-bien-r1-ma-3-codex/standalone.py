from pathlib import Path
import subprocess,os,sys,json,time
w=Path(__file__).resolve().parent;env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'));case='c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a';cmd=[sys.executable,'-B','ops/land_evidence_nguon_test.py','--mot-ca',case];t=time.monotonic();r=subprocess.run(cmd,cwd=w/'head',env=env,capture_output=True,text=True);out={'command':cmd,'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'seconds':time.monotonic()-t};(w/'standalone.json').write_text(json.dumps(out,indent=2));print(out)
