import contextlib, importlib.util, io, json, os, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t8',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();rows=[]
for name,old,new,prefix in t.DOT_BIEN:
    if name not in ('A7_bo_dong_dem','A7_gop_rest_vao_12'):continue
    assert src.count(old)==1;path=R/(name+'.py');path.write_text(src.replace(old,new));case=next(c for c in t.CA if c.split('_')[0]==prefix)
    for label,ma in [('head',root/'ops/ci_provenance.py'),('mutant',path)]:
        cmd=[sys.executable,'-B',str(root/'ops/ci_provenance_test.py'),'--mot-ca',case];p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(ma)),timeout=300);output=(p.stdout+p.stderr).decode();rows.append({'criterion':'A7','name':name,'case':case,'source':label,'command':cmd,'rc':p.returncode,'output':output,'rank':t.phan_hang(p.returncode,output,case)})
fake=[]
for rc,text,target in [(0,'','c'),(4,'HONG:c:AttributeError','c'),(3,'DO:other:failed','c'),(3,'DO:c:failed','c')]:fake.append({'rc':rc,'output':text,'target':target,'rank':t.phan_hang(rc,text,target)})
called=[]
def fake_case(c):
    called.append(c)
    if len(called)==1:return 4,'HONG:'+c+':AttributeError'
    return 3,'DO:'+c+':intentional'
t.chay_ca=fake_case;buf=io.StringIO()
with contextlib.redirect_stdout(buf):rc=t.main(['--tat-ca-ca'])
observed=json.loads(buf.getvalue());assert rc==0 and len(observed)==len(called)==2 and observed[0][1]==4 and observed[1][1]==3
report={'A7':rows,'classifier':fake,'stop_after_first_rc3':{'main_rc':rc,'calls':called,'json':observed}}
(R/'criteria8-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2));assert all(x['rc']==(0 if x['source']=='head' else 3) for x in rows)
