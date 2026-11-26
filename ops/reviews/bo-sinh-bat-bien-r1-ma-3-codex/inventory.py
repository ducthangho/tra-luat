from pathlib import Path
import ast,json,subprocess
w=Path(__file__).resolve().parent;r=w/'head'
rows=[]
for path in ['ops/land_evidence_nguon_test.py','ops/gate_output_doi_chieu_test.py']:
 text=(r/path).read_text();tree=ast.parse(text)
 targets={'c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a','c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong','c39_c37_do_khi_bo_sinh_lech_mien','c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o','a135_bo_sinh_dung_mien_dac_ta','a136_a135_do_khi_bo_sinh_lech_mien','kiem_bo_sinh','nap_sua','nho_dem','ky_tu_ngoai_ascii'}
 for fn in tree.body:
  if isinstance(fn,ast.FunctionDef) and fn.name in targets:
   for n in ast.walk(fn):
    if isinstance(n,(ast.Compare,ast.BoolOp,ast.If,ast.IfExp,ast.UnaryOp,ast.For)) or isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'bang','any','all','bool'}:
     rows.append(dict(file=path,function=fn.name,line=n.lineno,type=type(n).__name__,expr=ast.get_source_segment(text,n)))
(w/'clause-inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for x in rows:
 if x['function'] in {'kiem_bo_sinh','nho_dem','ky_tu_ngoai_ascii','nap_sua'}:print(x)
# Finite independent exhaustive proof checks for the four equivalent cases.
res={}
res['c37.tong/le']=all(((n==158 and d==158)==(n<=158 and d==158)) for n in range(165) for d in range(n+1))
res['c37.khac_nhau/ge']=all(((n==158 and d==158)==(n==158 and d>=158)) for n in range(165) for d in range(n+1))
res['a135.lap_category/le']=all(((n==d)==(n<=d)) for n in range(40) for d in range(n+1))
res['a135.cuoi.duy_nhat/le']=all(((n-b==1)==(n-b<=1)) for n in range(1,40) for b in range(n))
(w/'equivalence-checks.json').write_text(json.dumps(res,indent=2));print(res)
