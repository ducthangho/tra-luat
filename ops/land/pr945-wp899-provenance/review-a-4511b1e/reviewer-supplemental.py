import ast,collections,contextlib,hashlib,importlib.util,io,json,os,pathlib,subprocess,sys,tempfile,time
ROOT=pathlib.Path.cwd(); OUT=ROOT/'.review'; os.environ['TMPDIR']=str(OUT/'tmp');tempfile.tempdir=str(OUT/'tmp')
spec=importlib.util.spec_from_file_location('review_tests',ROOT/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
rows=[]
def save(): (OUT/'supplemental-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
def record(name,value):rows.append({'name':name,**value});save();print(name,json.dumps(value,ensure_ascii=False)[:600],flush=True)
for ca in ('c02_attempt_lech','c03_checkout_linux','c04_checkout_windows','c08_checkout_pr_parents','c17_ghi_nguyen_tu','c18_dem_not_measured','c19_rest_loi','c20_du_trang','c22_thieu_dinh_danh_khong_passed','c24_goi_that_loi_va_chuyen_huong','c33_trung_chu_khac_job','c36_ghep_lech_so','c37_ghep_lech_ten','c38_ghep_lech_gio','c39_ghep_job','c40_nhom_long','c41_buoc_uses','c42_github_env_cung_job','c43_khoi_khac_buoc','c52_tap_dong'):
    r=subprocess.run([sys.executable,'-B','ops/ci_provenance_test.py','--mot-ca',ca],capture_output=True)
    record(ca,{'command':[sys.executable,'-B','ops/ci_provenance_test.py','--mot-ca',ca],'rc':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()})
chosen=('A7_bo_dong_dem','A7_gop_rest_vao_12','F06_redirect_mang_token','A20i_zip_bo_dem_nhom','A20ii_zip_bo_dem_yaml','A21_bo_kiem_ten','A22_bo_kiem_gio','A22_khong_cat_giay','A23_lay_khoa_dau','A24_bo_luat_nhom_long','A25i_uses_sinh_marker','A25ii_zip_bo_dem_nhom','A26_bo_GITHUB_ENV','A26_GITHUB_ENV_toan_workflow','A27_khoi_bang_buoc_khac','A19_moi_ung_vien_trung_chu','A19_chan_doc_job_khac','L10_bat_lai_tuple_luot9')
for ten,cu,moi,dich in t.DOT_BIEN:
    if ten not in chosen: continue
    hang,ra=t.chay_dot_bien(ten,cu,moi,dich)
    record(ten,{'severity':{x['name']:x['severity_if_regressed'] for x in json.loads((OUT/'mutant-results.json').read_text())}[ten],'target_prefix':dich,'classification':hang,'output':ra})
for ten,cu,moi,dich,mong in t.TU_KIEM:
    hang,ra=t.chay_dot_bien(ten,cu,moi,dich);record(ten,{'expected':mong,'classification':hang,'output':ra})
ca='c18_dem_not_measured'
for rc,ra,mong in [(0,'','SONG_SOT'),(4,'HONG:'+ca+':AttributeError','TIN_DUNG_GIA'),(3,'DO:c19_rest_loi:x','TIN_DUNG_GIA'),(3,'DO:'+ca+':x','GIET')]:
    record('classifier_'+str(rc)+'_'+mong,{'rc_input':rc,'output_input':ra,'expected':mong,'actual':t.phan_hang(rc,ra,ca)})
m=t.nap(); errors=[]
for exc in (OverflowError,LookupError,TypeError,RuntimeError,OSError):
    old=m.yaml
    m.yaml=type('FakeYaml',(),{'safe_load':staticmethod(lambda v,exc=exc:(_ for _ in ()).throw(exc('review injected parse error')))})
    try: result=m.doc_wf('existing fixture');errors.append((exc.__name__,result))
    finally:m.yaml=old
record('parse_error_class',{'observations':errors})
src=(ROOT/'ops/ci_provenance.py').read_text();tree=ast.parse(src);f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='doc_wf');tr=f.body[1]
record('parse_try_scope',{'try_body_types':[type(n).__name__ for n in tr.body],'try_body_source':ast.unparse(tr.body[0]),'post_parse_return':ast.unparse(f.body[-1])})
record('D02_uses_multiline',{'actual':m.ten_du_kien({'uses':'./action\nsecond'}),'expected_full_value':'Run ./action\nsecond','disposition':'existing P3, owner decision in previous prompt'})
# Preserve real Git error without changing trust, permissions, signing policy or repository config.
with tempfile.TemporaryDirectory(prefix='review_git_probe_') as d:
    subprocess.run(['git','init','-q',d],check=True,capture_output=True)
    p=pathlib.Path(d)/'a';p.write_text('fixture\n')
    subprocess.run(['git','-C',d,'add','a'],check=True,capture_output=True)
    r=subprocess.run(['git','-C',d,'-c','user.name=t','-c','user.email=t@t','commit','-qm','fixture'],capture_output=True)
    record('registry_git_commit_probe',{'rc':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()})
record('complete',{'rows':len(rows)})
