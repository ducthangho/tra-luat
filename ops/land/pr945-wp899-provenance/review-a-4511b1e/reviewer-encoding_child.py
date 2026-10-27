import importlib.util,pathlib,sys
root=pathlib.Path.cwd();sp=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(sp);sp.loader.exec_module(t)
m=t.nap();d,oid=sys.argv[1:];lg=t.LINUX.replace(t.H,oid);j=t.job(1,steps=t.buoc_rest(lg,t.wf_tu()))
rest=t.RestGia({'id':5,'run_attempt':1,'event':'push','head_sha':oid,'path':'.github/workflows/ci.yml','check_suite_id':9},[j],{1:lg})
with t.moi_tam() as moi:
    raise SystemExit(m.main(['thu','--repo','o/r','--run','5','--attempt','1','--out',str(pathlib.Path(d)/'child_out')],goi=rest,git=lambda sha:m.git_cuc_bo(sha,goc=d),moi_tu=moi,wf=lambda sha,path:None))
