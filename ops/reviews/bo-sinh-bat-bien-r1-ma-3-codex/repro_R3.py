"""Reproduce R3-01 and omitted predicates; fresh disposable clone on every invocation."""
from pathlib import Path
import importlib.util,json,os,subprocess,sys,tempfile
w=Path(__file__).resolve().parent
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
A='ops/gate_output_doi_chieu_test.py';B='ops/land_evidence_nguon_test.py';rows=[]
with tempfile.TemporaryDirectory(dir=w/'tmp',prefix='repro-R3-') as d:
 r=Path(d)/'repo';subprocess.run(['git','clone','-q',str(w/'head'),str(r)],check=True)
 orig={p:(r/p).read_text() for p in [A,B]}
 for label,p,old,new,case in [
  ('omit-fourth',A,'for cam, bo_loai, so, vang in BO_SINH_MONG:','for cam, bo_loai, so, vang in BO_SINH_MONG[:3] + BO_SINH_MONG[4:]:','a136_a135_do_khi_bo_sinh_lech_mien'),
  ('omit-fifth',A,'for cam, bo_loai, so, vang in BO_SINH_MONG:','for cam, bo_loai, so, vang in BO_SINH_MONG[:-1]:','a136_a135_do_khi_bo_sinh_lech_mien'),
  ('final-bang-invert',A,'bang(not lech, f"bộ sinh','bang(lech, f"bộ sinh','a136_a135_do_khi_bo_sinh_lech_mien'),
  ('domain-branch-invert',B,'if tru is not None:','if tru is None:','c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o')]:
  assert orig[p].count(old)==1
  try:
   (r/p).write_text(orig[p].replace(old,new))
   q=subprocess.run([sys.executable,'-B',p,'--mot-ca',case],cwd=r,capture_output=True,text=True)
   row=dict(probe=label,case=case,rc=q.returncode,stdout=q.stdout,stderr=q.stderr);rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
  finally:(r/p).write_text(orig[p])
(w/'repro-R3.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
assert [x['rc'] for x in rows]==[0,0,3,3]
