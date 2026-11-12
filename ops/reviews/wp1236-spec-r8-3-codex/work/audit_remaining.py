import copy, importlib.util, json, os, sys, tempfile, types
from pathlib import Path
W=Path(__file__).resolve().parent;R=W.parent/'repo'
sys.dont_write_bytecode=True;sys.path[:0]=[str(W),str(W/'reference')]
os.environ['GATE_OUTPUT_DOI_CHIEU_GOC']=str(R);tempfile.tempdir=str(W/'tmp')
import gate_output_doi_chieu_test as t
import gram
from dot_bien_r8 import DB, dung
from probes_r8 import AM, DUONG
sp=importlib.util.spec_from_file_location('remaining_g1',W/'gate_output_doi_chieu.py')
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
src=(W/'gate_output_doi_chieu.py').read_text()
old='''elif ly := che_do_shell(str(y.get("run", "")), y.get("shell")):
                nm.append(f"{ly}:{s['name'][:30]}")'''
new='''elif ly := cu_phap_run(y.get("run"), y.get("shell")):
                nm.append(f"cu_phap_run:{ly}:{p['name']}:{s['name']}")'''
model=types.ModuleType('r8_remaining');model.__file__=str(W/'gate_output_doi_chieu.py')
exec(compile(src.replace(old,new),model.__file__,'exec'),model.__dict__);model.cu_phap_run=gram.cp
p=copy.deepcopy(t._f_nhanh());text=t.van(p,chi_success=True)
tt,why=model.kiem(text,p,t.goc())
missing=[x for x in why if x.startswith('thieu_job_bat_buoc:')]
assert tt=='not_measured' and len(missing)==8
run_kinds=[]
for path in ['.github/workflows/ci.yml','.github/workflows/launcher-windows.yml']:
    for event in ['push','workflow_dispatch']:
        got=m.la_run_land({'moc':{'run':{'event':event,'loi_khai_rest_path':path}}})
        assert got==(path=='.github/workflows/ci.yml' and event=='push')
        run_kinds.append((path,event,got))
mut=dung(phai_ong=gram.W)
broken=[k for k,(r,s) in DUONG.items() if mut(r,s)!=gram.cp(r,s)]
assert broken==['d_ong_bash_trai_hong','d_ong_bash_phai_hong']
reasons=(gram.cp(None,'pwsh'),DB['m-S19_dao_thu_tu_1_2'][0](None,'pwsh'))
assert reasons==('lenh_ngoai_cu_phap','shell_ngoai_cu_phap')
result={'G16_run_41397205258':{'status':tt,'missing_required':missing},'G17_la_run_land':run_kinds,
 'H04_order':reasons,'m_S12_prime':broken,'DONG_numeric_patterns':sum(lo=='DONG' and bool(__import__('re').compile(r).groups) for rule in m.LUAT_v1['MUC'] for b in rule['buoc'] for lo,r in b['dau_hieu']),
 'DONG_numeric_groups':sum(__import__('re').compile(r).groups for rule in m.LUAT_v1['MUC'] for b in rule['buoc'] for lo,r in b['dau_hieu'] if lo=='DONG')}
print(json.dumps(result,ensure_ascii=False,indent=2))
(W/'remaining.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
