import ast,hashlib,importlib.util,json,os,pathlib,subprocess,sys,tempfile,time
root=pathlib.Path.cwd(); out=root/'.review'; os.environ['TMPDIR']=str(out/'tmp');tempfile.tempdir=os.environ['TMPDIR']
spec=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
goc=(root/'ops/ci_provenance.py').read_text(); folder=out/'mutants';folder.mkdir(exist_ok=True)
sev={'A7_bo_dong_dem':'P1','A7_gop_rest_vao_12':'P1','F06_redirect_mang_token':'P0','A20i_zip_bo_dem_nhom':'P0','A20ii_zip_bo_dem_yaml':'P0','A21_bo_kiem_ten':'P0','A22_bo_kiem_gio':'P0','A22_khong_cat_giay':'P1','A23_lay_khoa_dau':'P0','A24_bo_luat_nhom_long':'P0','A25i_uses_sinh_marker':'P1','A25ii_zip_bo_dem_nhom':'P0','A26_bo_GITHUB_ENV':'P0','A26_GITHUB_ENV_toan_workflow':'P1','A27_khoi_bang_buoc_khac':'P0','A19_moi_ung_vien_trung_chu':'P1','A19_chan_doc_job_khac':'P0','L10_bat_lai_tuple_luot9':'P2'}
results=[]
for name,old,new,prefix in t.DOT_BIEN:
    if name not in sev:continue
    target=next(c for c in t.CA if c.split('_')[0]==prefix)
    assert goc.count(old)==1
    src=goc.replace(old,new);compile(src,name,'exec'); p=folder/(name+'.py');p.write_text(src)
    cmd=[sys.executable,'-B','ops/ci_provenance_test.py','--mot-ca',target]
    r=subprocess.run(cmd,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(p),PYTHONDONTWRITEBYTECODE='1'))
    stdout=r.stdout.decode(errors='replace');stderr=r.stderr.decode(errors='replace'); (folder/(name+'.stdout.txt')).write_text(stdout);(folder/(name+'.stderr.txt')).write_text(stderr)
    correct=r.returncode==3 and stdout.startswith('DO:'+target+':')
    row={'name':name,'severity_if_regressed':sev[name],'target':target,'command':cmd,'mutant_source_sha256':hashlib.sha256(src.encode()).hexdigest(),'rc':r.returncode,'correct_target_TinHieuChotCa':correct,'classification':'GIET' if correct else 'SONG_SOT' if r.returncode==0 else 'TIN_DUNG_GIA','stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()};results.append(row)
    (out/'mutant-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');print(name,row['classification'],r.returncode,flush=True)
# D05: existing P3, move return under parse try; no production-file changes.
tr=ast.parse(goc);f=next(n for n in tr.body if isinstance(n,ast.FunctionDef) and n.name=='doc_wf');f.body[1].body.append(f.body.pop());wide=ast.unparse(ast.fix_missing_locations(tr));p=folder/'D05_wide_try.py';p.write_text(wide)
r=subprocess.run([sys.executable,'-B','ops/ci_provenance_test.py','--mot-ca','c52_tap_dong'],capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(p),PYTHONDONTWRITEBYTECODE='1'))
class OutsideParseError(Exception):pass
def observe(file):
    sp=importlib.util.spec_from_file_location('m',file);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
    def fake_type(v):raise OutsideParseError('outside parse')
    m.type=fake_type
    try:return {'returned':m.doc_wf('jobs: {}\n')}
    except OutsideParseError:return {'raised':'OutsideParseError'}
row={'name':'D05_wide_try','severity':'P3','catalogue_target':'c52_tap_dong','rc':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'head_fault_injection':observe(root/'ops/ci_provenance.py'),'mutant_fault_injection':observe(p)}
(out/'D05-results.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n');print(row,flush=True)
