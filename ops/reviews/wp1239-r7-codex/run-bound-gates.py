import pathlib,subprocess,sys,hashlib,platform,os,json,datetime,time
p=pathlib.Path('/workspace/scratch/proxima-p0-20261105/r7-runtime'); r=pathlib.Path('/workspace/scratch/wp1239-r6-g5-validation'); H='4c319cc4f71b2f9a5c69a4b1be75e1add5f8aeaa'; S='9607e3eba96b2ce091e34196cbb8ede31a521ff9'
def git(*a):return subprocess.check_output(['git','-C',str(r),*a]).decode().strip()
def sha(f):return hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
assert git('rev-parse','HEAD')==H and git('rev-parse','HEAD^{tree}')=='539a02f355c4ade3cee7c99efa327a4a729e79bb'
assert not (p/'bound-gates-start.json').exists(),'Do not duplicate gate run'
py=str(pathlib.Path(sys.executable).resolve()); env=os.environ.copy()
for k in ('TL_MASTER_KEY','TL_TOKEN','TL_WEBAPP','CODEX_AUTH_JSON'):env.pop(k,None)
env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONPYCACHEPREFIX=str(p/'bound-gates-pycache'))
meta={'head':H,'tree':git('rev-parse','HEAD^{tree}'),'base':S,'cwd':str(r),'runner':{'hostname':platform.node(),'os':platform.platform(),'uname':list(platform.uname()),'pid':os.getpid(),'python_executable':py,'python_executable_sha256':sha(py),'python_version':sys.version,'git_version':subprocess.check_output(['git','--version']).decode().strip()},'harness':{'path':str(pathlib.Path(__file__).resolve()),'sha256':sha(__file__)},'code_identity':{'tl_py_sha256':sha(r/'scripts/tl.py'),'lease_publish_py_sha256':sha(r/'ops/lease_publish.py'),'git_tree':git('rev-parse','HEAD^{tree}')},'reason':'F2 from independent blocked review: produce complete gate execution identity on unchanged H7; no model call','start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operations':[]}
(p/'bound-gates-start.json').write_text(json.dumps(meta,indent=2)+'\n')
cmds=[('full-selftest',[py,'-B','scripts/tl.py','--selftest']),('canonical-admission',[py,'-B','ops/lease_publish.py','kiem-thu-hoi-github',H,'--canonical-base',S,'--nhanh-mac-dinh','master','--root',str(r),'--receipt',str(p/'bound-admission.json')])]
for name,cmd in cmds:
 f=p/(name+'-bound.log'); t=time.monotonic(); start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with f.open('wb') as out:q=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=subprocess.STDOUT)
 b=f.read_bytes(); item={'name':name,'argv':cmd,'cwd':str(r),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'duration_seconds':time.monotonic()-t,'rc':q.returncode,'log_path':str(f),'log_bytes':len(b),'log_sha256':sha(f),'positive_marker':('== tl selftest 1777/1777 ==' if name=='full-selftest' else 'THU_HOI_ADMISSION TAP_THU_HOI_RONG'),'marker_present':(b'== tl selftest 1777/1777 ==' if name=='full-selftest' else b'THU_HOI_ADMISSION TAP_THU_HOI_RONG') in b};meta['operations'].append(item);(p/'bound-gates-progress.json').write_text(json.dumps(meta,indent=2)+'\n'); assert q.returncode==0 and item['marker_present']
meta.update(end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),end_head=git('rev-parse','HEAD'),end_tree=git('rev-parse','HEAD^{tree}'),tracked_status=git('status','--porcelain=v1','--untracked-files=no'),python_executable_sha256_after=sha(py),harness_sha256_after=sha(__file__))
assert meta['end_head']==H and meta['end_tree']==meta['tree'] and not meta['tracked_status']
(p/'bound-gates-receipt.json').write_text(json.dumps(meta,indent=2)+'\n');print('Bound execution gates passed; pending independent acceptance of F2 remediation',flush=True)
