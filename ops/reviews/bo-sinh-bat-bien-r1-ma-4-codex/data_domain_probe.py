from pathlib import Path
import importlib.util,json,os
w=Path(__file__).resolve().parent;p=w/'head/ops/gate_output_doi_chieu_test.py';rows=[]
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
for idx in range(5):
 s=importlib.util.spec_from_file_location('a',p);a=importlib.util.module_from_spec(s);s.loader.exec_module(a);old=a.BO_SINH_MONG
 a.BO_SINH_MONG=old[:idx]+old[idx+1:]
 out=a.chay_ca('a136_a135_do_khi_bo_sinh_lech_mien');row=dict(mutation='remove-constant-entry',index=idx+1,argument=[old[idx][0],old[idx][1]],rc=out[0],output=out[1]);rows.append(row);print(row,flush=True)
s=importlib.util.spec_from_file_location('a',p);a=importlib.util.module_from_spec(s);s.loader.exec_module(a);a.BO_SINH_MONG=(*a.BO_SINH_MONG[:4],a.BO_SINH_MONG[1]);out=a.chay_ca('a136_a135_do_khi_bo_sinh_lech_mien');rows.append(dict(mutation='replace-fifth-with-second-keep-five',rc=out[0],output=out[1]));print(rows[-1],flush=True)
(w/'data-domain.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
