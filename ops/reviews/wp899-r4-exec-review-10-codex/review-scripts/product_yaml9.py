import hashlib, importlib.util, json, os, pathlib, subprocess, sys, tempfile
R=pathlib.Path(__file__).resolve().parent;root=R.parent
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
t=load(root/'ops/ci_provenance_test.py','test9');m=load(root/'ops/ci_provenance.py','product9')
if len(sys.argv)>1 and sys.argv[1]=='child':
 d=json.loads((R/'yaml-fixture9.json').read_text());key=sys.argv[2];x=d['cases'][key]
 m.ROOT=pathlib.Path(d['git_root'])
 jobs=x['jobs'];rest=t.RestGia(x['run'],jobs,{1:x['log']},run_id=5)
 with t.moi_tam({t.DUONG_GIA:r'^THU: (\d+)/(\d+) dat$'}) as moi:
  raise SystemExit(m.main(['thu','--repo','o/r','--run','5','--attempt','1','--out',str(R/('yaml-out-'+key))],
                 goi=rest,git=lambda sha:m.git_cuc_bo(sha,goc=m.ROOT),wf=lambda sha,path:m.git_blob(sha,path,goc=m.ROOT),moi_tu=moi))
gitroot=R/'yaml-git';gitroot.mkdir(exist_ok=True)
receipts=[]
def git(*args,data=None):
 p=subprocess.run(['git','-C',str(gitroot),*args],input=data,capture_output=True,env=dict(os.environ,
   GIT_AUTHOR_NAME='Offline review',GIT_AUTHOR_EMAIL='review@example.invalid',GIT_COMMITTER_NAME='Offline review',
   GIT_COMMITTER_EMAIL='review@example.invalid',GIT_AUTHOR_DATE='2026-10-25T00:00:00Z',GIT_COMMITTER_DATE='2026-10-25T00:00:00Z'))
 receipts.append({'command':p.args,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()});assert p.returncode==0
 return p.stdout.decode().strip()
git('init','-q');fixture={'git_root':str(gitroot),'cases':{}}
for key,scalar in [('valid_quoted','"2026-02-30"'),('invalid_date','2026-02-30'),('invalid_hour','2026-01-01T99:00:00Z'),
                   ('invalid_int','!!int xyz'),('invalid_float','!!float abc'),('invalid_bool','!!bool maybe'),
                   ('empty_int',"!!int ''"),('empty_float',"!!float ''"),('invalid_timestamp','!!timestamp abc')]:
 van='name: '+scalar+'\n'+t.wf_tu(t.X)
 blob=git('hash-object','-w','--stdin',data=van.encode());tree=git('mktree',data=f'100644 blob {blob}\twf.yml\n'.encode())
 sha=git('commit-tree',tree,'-m','Offline reader fixture')
 lg=t.log_voi(t.buoc(t.X,'THU: 4/4 dat')).replace(t.H,sha)
 run={'id':5,'run_attempt':1,'event':'push','head_sha':sha,'path':'wf.yml','check_suite_id':9}
 job=t.job(1,steps=t.buoc_rest(lg,t.wf_tu(t.X)))
 fixture['cases'][key]={'run':run,'jobs':[job],'log':lg,'workflow':van,'blob_oid':blob,'checkout_sha':sha,
     'workflow_sha256':hashlib.sha256(van.encode()).hexdigest()}
(R/'yaml-fixture9.json').write_text(json.dumps(fixture,ensure_ascii=False,indent=2));results=[]
for key,x in fixture['cases'].items():
 cmd=[sys.executable,'-B',str(__file__),'child',key];p=subprocess.run(cmd,capture_output=True)
 (R/f'yaml-{key}.stdout.txt').write_bytes(p.stdout);(R/f'yaml-{key}.stderr.txt').write_bytes(p.stderr)
 results.append({'case':key,'command':cmd,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),
      'workflow_sha256':x['workflow_sha256'],'checkout_sha':x['checkout_sha'],'blob_oid':x['blob_oid']})
report={'git_commands':receipts,'results':results}
(R/'product-yaml9-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps([{k:x[k] for k in ('case','rc','stdout','checkout_sha')} for x in results],ensure_ascii=False,indent=2))
assert results[0]['rc']==0 and 'gate=passed' in results[0]['stdout']
assert all(x['rc']==0 and 'gate=not_measured' in x['stdout'] for x in results[1:])
