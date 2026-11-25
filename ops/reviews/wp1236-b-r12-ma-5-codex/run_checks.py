import subprocess,pathlib,os,json,time,hashlib,concurrent.futures
R=pathlib.Path(__file__).resolve().parents[1]/'repo'; W=R.parent/'work'
E=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(W/'tmp'),RUFF_CACHE_DIR=str(W/'ruff-cache'),GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='core.abbrev',GIT_CONFIG_VALUE_0='7')
base=W/'ruff-base';base.mkdir(exist_ok=True)
files=['ops/land_evidence_nguon.py','ops/land_evidence_nguon_test.py']
for f in files:(base/pathlib.Path(f).name).write_bytes(subprocess.check_output(['git','show','f602325574c62184caf16309631f5f680ca5cee2:'+f],cwd=R))
checks={'suite':['python3','-B',files[1]],'tree':['python3','-B',files[0],'--root','.'],'ruff':['python3','-m','ruff','check','--no-cache','--select','F',*files],'ruff-base':['python3','-m','ruff','check','--no-cache','--select','F',*[str(base/pathlib.Path(f).name) for f in files]],'diff-check':['git','diff','--check','f602325574c62184caf16309631f5f680ca5cee2','HEAD'],'numstat':['git','diff','--numstat','f602325574c62184caf16309631f5f680ca5cee2','HEAD'],'ruff-version':['python3','-m','ruff','--version'],'runtime':['python3','-B','-c','import sys,platform,yaml; print(sys.executable); print(sys.version); print(platform.platform()); print("PyYAML",yaml.__version__)'],'ruff-contract':['python3','-B','-c','import runpy,sys; m=runpy.run_path(".claude/dev/ci_dang_ky_test.py"); e,n=m["loi_ruff_ci"](); print("RUFF_CONTRACT",n,e); sys.exit(bool(e) or n == 0)']}
def run(item):
 name,args=item;t=time.monotonic();p=subprocess.run(args,cwd=R,env=E,capture_output=True)
 (W/(name+'.stdout.log')).write_bytes(p.stdout);(W/(name+'.stderr.log')).write_bytes(p.stderr)
 d={'name':name,'command':args,'rc':p.returncode,'seconds':round(time.monotonic()-t,3),'status':'passed' if p.returncode==0 else 'failed','stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'stdout_log':name+'.stdout.log','stderr_log':name+'.stderr.log','tested_sha':'bca55c1cd09c57180d60b05d5ca1813828ae1d10'}
 (W/(name+'-result.json')).write_text(json.dumps(d,indent=2));print(name,p.returncode,p.stdout.decode(errors='replace')[-600:],p.stderr.decode(errors='replace')[-200:],flush=True);return d
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,checks.items()))
(W/'checks.json').write_text(json.dumps(results,indent=2))
