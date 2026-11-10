"""Prepare only anonymously retrievable public source; never copy the rejected clone."""
import os,sys,json,hashlib,zipfile,io,urllib.request,urllib.parse,subprocess,shutil,datetime,concurrent.futures,traceback
from pathlib import Path
R=Path(r'D:\tl-win\wp1287-public-review2-20261110');I=R/'inputs';P=R/'repo';L=Path(r'D:\tl-win\KHOA.txt');N='wp1287-r16-g16-review-2';H='2a5803e17b7ca4910c7188bfcc2276190e2d0b4b';B='bf9914cb1a8e6f5047468f4d130b587015f8d73f';TREE='bfb2fad8df2634ae8dd4c839a4565b76d1cfae45'
def utc():return datetime.datetime.now(datetime.timezone.utc)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
assert os.environ.get('COMPUTERNAME')=='ASUS-LAPTOP';a=json.loads((R/'assignment-r16.json').read_text());assert utc()<datetime.datetime.fromisoformat(a['lease_expires_at_utc']);assert not (R/'invocation-r16.json').exists() and not (R/'runtime-r16.json').exists() and not P.exists() and not I.exists()
for n,key in [('run_review_r16.py','run_review_sha256'),('prompt-r16.txt','prompt_sha256'),('SPEC-r16.md','spec_sha256'),('sandbox_preflight_public.py','sandbox_preflight_sha256'),('public-provenance.json','public_provenance_sha256')]:assert sha(R/n)==a[key]
assert not L.read_text(encoding='utf-8-sig').strip(),'HOST_BUSY'
start=utc();expiry=min(start+datetime.timedelta(minutes=90),datetime.datetime.fromisoformat(a['lease_expires_at_utc']));line='\t'.join([N,start.isoformat(),expiry.isoformat(),'Public-source-only independent review prep',start.isoformat()]);L.write_text(line,encoding='utf-8');assert L.read_text()==line
proof=json.loads((R/'public-provenance.json').read_text());sources=[];steps=[]
env=os.environ.copy()
for k in list(env):
 if k.startswith(('TL_','GIT_')) or any(t in k.upper() for t in ['TOKEN','SECRET','PASSWORD','API_KEY','MASTER_KEY']) or k=='CODEX_AUTH_JSON':env.pop(k,None)
env.update(GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',GCM_INTERACTIVE='never',PYTHONDONTWRITEBYTECODE='1')
def get(url):
 u=urllib.parse.urlsplit(url);assert u.scheme=='https' and not u.username and not u.password
 assert (u.hostname=='api.github.com' and u.path=='/repos/ducthangho/tra-luat') or (u.hostname=='raw.githubusercontent.com' and u.path.startswith('/ducthangho/tra-luat/'))
 req=urllib.request.Request(url,headers={'User-Agent':'wp1287-public-source-review'});assert 'Authorization' not in req.headers
 with urllib.request.urlopen(req,timeout=45) as r:
  assert r.status==200 and urllib.parse.urlsplit(r.url).hostname==u.hostname;return r.read()
git=shutil.which('git');assert git

def run(label,args,timeout=300):
 p=subprocess.run([git,'-c','credential.helper=','-c','http.extraHeader=',*args],cwd=R,env=env,capture_output=True,timeout=timeout);(R/(label+'.stdout')).write_bytes(p.stdout);(R/(label+'.stderr')).write_bytes(p.stderr);steps.append({'label':label,'rc':p.returncode});assert p.returncode==0,(label,p.returncode);return p.stdout.decode('utf-8',errors='replace').strip()
try:
 meta=json.loads(get(proof['repository']['url']));assert meta['private'] is False and meta['visibility']=='public';I.mkdir()
 zinfo=proof['handoff_archive'];data=get(zinfo['url']);assert len(data)==zinfo['bytes'] and hashlib.sha256(data).hexdigest()==zinfo['sha256']
 with zipfile.ZipFile(io.BytesIO(data)) as z:bundle=z.read(zinfo['extracted_member'])
 assert hashlib.sha256(bundle).hexdigest()==zinfo['bundle_sha256'];(I/'candidate-H2.bundle').write_bytes(bundle);sources.append({'name':'candidate-H2.bundle','public_url':zinfo['url'],'archive_member':zinfo['extracted_member'],'sha256':zinfo['bundle_sha256'],'bytes':len(bundle),'anonymous':True})
 def download(x):
  assert Path(x['name']).name==x['name'];b=get(x['url']);assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'];(I/x['name']).write_bytes(b);return {'name':x['name'],'public_url':x['url'],'bytes':len(b),'sha256':x['sha256'],'anonymous':True}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:sources+=list(ex.map(download,proof['files']))
 assert len(sources)==18;save(I/'MANIFEST.json',{'source_class':'verified_public_only','files':sources,'private_local_clone_copied':False,'private_native_logs_copied':False});save(I/'PUBLIC-PROVENANCE.json',proof)
 run('public-clone',['clone','--no-checkout','--single-branch','--branch','master','--config','core.autocrlf=false','--config','core.longpaths=true','--config','core.abbrev=7','https://github.com/ducthangho/tra-luat.git',str(P)])
 assert run('origin',['-C',str(P),'remote','get-url','origin'])=='https://github.com/ducthangho/tra-luat.git'
 assert (P/'.git').is_dir() and not (P/'.git/objects/info/alternates').exists()
 run('public-base',['-C',str(P),'cat-file','-e',B+'^{commit}'])
 run('public-bundle-verify',['-C',str(P),'bundle','verify',str(I/'candidate-H2.bundle')])
 run('public-bundle-import',['-C',str(P),'fetch',str(I/'candidate-H2.bundle'),'refs/heads/agent/wp1287-r3-g3-codex:refs/heads/review/wp1287-public-h2'])
 run('public-checkout',['-C',str(P),'checkout','--detach',H]);assert run('origin-preserved',['-C',str(P),'remote','get-url','origin'])=='https://github.com/ducthangho/tra-luat.git'
 assert run('head',['-C',str(P),'rev-parse','HEAD'])==H and run('tree',['-C',str(P),'rev-parse','HEAD^{tree}'])==TREE and not run('clean',['-C',str(P),'status','--porcelain'])
 root=run('root',['-C',str(P),'rev-list','--max-parents=0','HEAD']);assert root=='394e93468fc8d84ec20938e6df8fb7ab72b2cc37'
 assert sorted(run('scope',['-C',str(P),'diff','--name-only',B,H]).splitlines())==['.agents/skills/playwright-browser/'+n for n in ['SKILL.md','package-lock.json','package.json']]
 launcher=P/'.claude/dev/launcher.py';assert sha(launcher)=='fbf5ac3e9a88d7f7ac4fa892a3aac115752e8e7f133c8a3eb947834a215dee23'
 shim=shutil.which('codex.cmd');assert shim;exes=list((Path(shim).parent/'node_modules/@openai/codex').rglob('codex.exe'));assert len(exes)==1;exe=exes[0];ver=subprocess.check_output([str(exe),'--version'],env=env).decode().strip();assert ver=='codex-cli 0.155.1'
 probe_args=[str(exe),'--disable','memories','-c','memories.use_memories=false','-c','memories.generate_memories=false']
 fp=subprocess.run(probe_args+['features','list'],env=env,capture_output=True,timeout=30);assert fp.returncode==0
 memory_line=[s for s in fp.stdout.decode().splitlines() if s.split() and s.split()[0]=='memories'];assert len(memory_line)==1 and memory_line[0].split()[-1]=='false'
 sp=subprocess.run(probe_args+['sandbox','--permission-profile',':read-only','-C',str(P),sys.executable,'-I','-B',str(R/'sandbox_preflight_public.py')],env=env,capture_output=True,timeout=120);(R/'sandbox-preflight.stdout').write_bytes(sp.stdout);(R/'sandbox-preflight.stderr').write_bytes(sp.stderr);assert sp.returncode==0,('actual_sandbox_probe',sp.returncode)
 sandbox=json.loads(sp.stdout.decode());assert sandbox['all_positive_pass'] and sandbox['negative_control_pass'] and sandbox['public_files_verified']==18;save(R/'sandbox-capability-r16.json',sandbox)
 deadline=(utc()+datetime.timedelta(minutes=45)).strftime('%Y-%m-%dT%H:%M:%SZ')
 rt={'workspace':str(P),'input_root':str(I),'candidate':H,'tree':TREE,'root_commit':root,'launcher':str(launcher),'launcher_sha256':sha(launcher),'codex':str(exe),'codex_sha256':sha(exe),'codex_version':ver,'python':sys.executable,'prompt_sha256':a['prompt_sha256'],'spec_sha256':a['spec_sha256'],'deadline_utc':deadline,'public_source_only':True,'no_rejected_local_clone_copied':True,'lock_nonce':N,'lock_expiry':expiry.isoformat(),'model_invoked':False,'public_inputs':18,'actual_sandbox_preflight_pass':True,'memories_disabled_feature_verified':True};save(R/'runtime-r16.json',rt)
 result={'bootstrap_rc':0,'source_class':'verified_public_only','public_inputs':18,'anonymous_source_checks':True,'candidate':H,'tree':TREE,'clone_clean':True,'private_local_objects_copied':False,'model_invoked':False,'deadline_utc':deadline};save(R/'public-preflight-r16.json',result);print(json.dumps(result),flush=True)
except BaseException as e:
 save(R/'bootstrap-failure-r16.json',{'at':utc().isoformat(),'error_type':type(e).__name__,'traceback':traceback.format_exc(),'steps':steps,'model_invoked':False})
 if L.read_text(encoding='utf-8-sig').split('\t')[0]==N:L.write_bytes(b'')
 print(json.dumps({'bootstrap_rc':2,'error_type':type(e).__name__,'steps':steps,'model_invoked':False,'lock_released':not L.read_bytes()}),flush=True);sys.exit(2)
