import contextlib,importlib.util,io,json,os,pathlib,subprocess,sys,tempfile
root=pathlib.Path.cwd();out=root/'.review';os.environ['TMPDIR']=str(out/'tmp');tempfile.tempdir=os.environ['TMPDIR']
sp=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(sp);sp.loader.exec_module(t)
m=t.nap(); rows=[]
# Reuse the already supplied non-UTF8 byte fixture of c34_git_blob_that.
with tempfile.TemporaryDirectory(prefix='review_commit_encoding_') as d:
    def git(*a,data=None):
        r=subprocess.run(['git','-C',d,*a],input=data,capture_output=True,check=True);return r.stdout.strip().decode('ascii')
    git('init','-q');tree=git('mktree',data=b'')
    blob_results=[]
    for blob_name,data in [('utf8_blob',b'fixture\n'),('non_utf8_blob',b'\xff\n')]:
        blob_oid=git('hash-object','-w','--stdin',data=data)
        try:blob_result=m.git_cuc_bo(blob_oid,goc=d);blob_error=None
        except Exception as e:blob_result=None;blob_error=type(e).__name__+': '+str(e)
        blob_results.append({'case':blob_name,'sha':blob_oid,'expected':None,'actual':blob_result,'error':blob_error})
    (out/'git-noncommit-encoding-results.json').write_text(json.dumps(blob_results,ensure_ascii=False,indent=2)+'\n')
    header=(f'tree {tree}\nauthor Fixture <fixture@example.invalid> 0 +0000\ncommitter Fixture <fixture@example.invalid> 0 +0000\n').encode('ascii')
    for name,enc,body in [('utf8','UTF-8',b'fixture\n'),('latin1','ISO-8859-1',b'\xff\n')]:
        oid=git('hash-object','-t','commit','-w','--stdin',data=header+('encoding '+enc+'\n\n').encode('ascii')+body)
        objtype=git('cat-file','-t',oid)
        native_metadata=git('show','--no-patch','--format=%T%n%P',oid)
        native_message=subprocess.run(['git','-C',d,'log','-1','--format=%B','--encoding=UTF-8',oid],capture_output=True,check=True).stdout
        try: result=m.git_cuc_bo(oid,goc=d);error=None
        except Exception as e: result=None;error=type(e).__name__+': '+str(e)
        expected={'tree':tree,'parents':[]}
        row={'case':name,'sha':oid,'git_type':objtype,'declared_encoding':enc,'native_git_metadata':native_metadata,'native_git_message_utf8_hex':native_message.hex(),'expected':expected,'actual':result,'error':error}
        def check():t.bang(result==expected,f'{name}: parents/tree must not depend on commit-message encoding; {error or result}')
        try:check();row['test_rc']=0;row['test_output']=''
        except t.TinHieuChotCa as e:row['test_rc']=3;row['test_output']='DO:r955_git_commit_message_encoding:'+str(e)
        # End-to-end main, real Git metadata reader, existing stateful REST/log fixture.
        lg=t.LINUX.replace(t.H,oid);j=t.job(1,steps=t.buoc_rest(lg,t.wf_tu()))
        rest=t.RestGia({'id':5,'run_attempt':1,'event':'push','head_sha':oid,'path':'.github/workflows/ci.yml','check_suite_id':9},[j],{1:lg})
        buf=io.StringIO()
        with t.moi_tam() as moi,contextlib.redirect_stdout(buf):
            try:
                rc=m.main(['thu','--repo','o/r','--run','5','--attempt','1','--out',str(pathlib.Path(d)/('out_'+name))],goi=rest,git=lambda sha:m.git_cuc_bo(sha,goc=d),moi_tu=moi,wf=lambda sha,path:None)
                row['main_rc']=rc;row['main_error']=None
            except Exception as e:row['main_rc']=None;row['main_error']=type(e).__name__+': '+str(e)
        row['main_stdout']=buf.getvalue()
        cmd=[sys.executable,'-B','.review/encoding_child.py',d,oid]
        child=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        row['child_command']=cmd;row['child_rc']=child.returncode
        row['child_stdout']=child.stdout.decode();row['child_stderr']=child.stderr.decode()
        criterion_cmd=[sys.executable,'-B','.review/encoding_criterion.py',d,oid,tree]
        criterion=subprocess.run(criterion_cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        row['criterion_command']=criterion_cmd;row['criterion_rc']=criterion.returncode
        row['criterion_stdout']=criterion.stdout.decode();row['criterion_stderr']=criterion.stderr.decode()
        rows.append(row)
(out/'git-commit-encoding-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))
