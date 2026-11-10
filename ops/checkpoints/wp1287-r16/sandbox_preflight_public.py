import os,json,subprocess,ctypes,hashlib
from pathlib import Path
R=Path(r'D:\tl-win\wp1287-public-review2-20261110');P=R/'repo';G=r'C:\Program Files\Git\cmd\git.exe'
b=ctypes.create_unicode_buffer(256);n=ctypes.c_ulong(256);assert ctypes.windll.advapi32.GetUserNameW(b,ctypes.byref(n))
env={'SystemRoot':r'C:\Windows','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'NUL','GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0'}
results=[]
for trusted in [False,True]:
 prefix=[G,'--no-optional-locks','-c','core.fsmonitor=false']
 if trusted:prefix+=['-c','safe.directory='+str(P).replace('\\','/')]
 prefix+=['-C',str(P)]
 for label,args in [('head',['rev-parse','HEAD']),('tree',['rev-parse','HEAD^{tree}']),('ancestry',['merge-base','--is-ancestor','bf9914cb1a8e6f5047468f4d130b587015f8d73f','HEAD']),('status',['status','--porcelain']),('scope',['diff','--name-only','bf9914cb1a8e6f5047468f4d130b587015f8d73f','HEAD']),('diffcheck',['diff','--check','bf9914cb1a8e6f5047468f4d130b587015f8d73f','HEAD']),('numstat',['diff','--numstat','bf9914cb1a8e6f5047468f4d130b587015f8d73f','HEAD'])]:
  p=subprocess.run(prefix+args,env=env,capture_output=True);results.append({'exact_path_command_scope_trust':trusted,'test':label,'rc':p.returncode,'stdout':p.stdout.decode(errors='replace').strip(),'dubious_ownership':'dubious ownership' in p.stderr.decode(errors='replace')})
positive=[x for x in results if x['exact_path_command_scope_trust']];assert all(x['rc']==0 for x in positive);assert positive[0]['stdout']=='2a5803e17b7ca4910c7188bfcc2276190e2d0b4b' and positive[1]['stdout']=='bfb2fad8df2634ae8dd4c839a4565b76d1cfae45' and not positive[3]['stdout']
assert all(x['rc']==128 for x in results[:4]);assert b.value=='CodexSandboxOffline'
manifest=json.loads((R/'inputs/MANIFEST.json').read_text());assert len(manifest['files'])==18
for x in manifest['files']:
 p=R/'inputs'/x['name'];assert p.stat().st_size==x['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
assert sum(int(row.split()[0]) for row in positive[-1]['stdout'].splitlines())==377
print(json.dumps({'actual_sandbox_user':b.value,'all_positive_pass':True,'negative_control_pass':True,'public_files_verified':18,'model_invoked':False,'global_configuration_modified':False,'candidate_modified':False,'results':results}),flush=True)
