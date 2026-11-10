"""Prepare independent exact-H clone and verify frozen inputs; no model invocation."""
import os,sys,json,hashlib,base64,zipfile,shutil,subprocess,datetime,runpy,traceback
from pathlib import Path
R=Path(r'D:\tl-win\wp1287-H2-formal-20261110');INPUT=R/'inputs';REPO=R/'repo';SOURCE=Path(r'D:\Quốc hội\tra-luat');OLD=Path(r'D:\tl-win\wp1287-five-file-advisory-20261110');LOCK=Path(r'D:\tl-win\KHOA.txt');NONCE='wp1287-r13-g13-review-1'
H='2a5803e17b7ca4910c7188bfcc2276190e2d0b4b';B='bf9914cb1a8e6f5047468f4d130b587015f8d73f';TREE='bfb2fad8df2634ae8dd4c839a4565b76d1cfae45';ROOT_COMMIT='394e93468fc8d84ec20938e6df8fb7ab72b2cc37'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def utc():return datetime.datetime.now(datetime.timezone.utc)
assert os.environ.get('COMPUTERNAME')=='ASUS-LAPTOP' and not (R/'runtime.json').exists()
env=os.environ.copy()
for k in list(env):
 if k.startswith('TL_') or any(t in k.upper() for t in ['TOKEN','SECRET','PASSWORD','API_KEY','MASTER_KEY']) or k=='CODEX_AUTH_JSON':env.pop(k,None)
env.update(GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',PYTHONDONTWRITEBYTECODE='1')
git=shutil.which('git');assert git
v=json.loads((OLD/'runtime.json').read_text());launcher=Path(v['launcher']);exe=Path(v['codex']);assert sha(launcher)=='fbf5ac3e9a88d7f7ac4fa892a3aac115752e8e7f133c8a3eb947834a215dee23';assert sha(exe)==v['codex_sha256']
version=subprocess.check_output([str(exe),'--version'],env=env).decode().strip();assert version=='codex-cli 0.155.1'
helptext=subprocess.check_output([str(exe),'exec','--help'],env=env).decode();assert all(x in helptext for x in ['--ephemeral','--sandbox','--json','--output-last-message'])
m=runpy.run_path(str(launcher));home=m['_codex_home_hieu_luc']()
with m['_KhoCodex'](home) as store:
 rejected,_=m['_doc_rejected'](store);data=store.read();assert data is not None;m['_doc_auth_bytes'](data);assert m['_credential_id'](data) not in rejected
assert not LOCK.read_text(encoding='utf-8-sig').strip(),'HOST_BUSY'
start=utc();expiry=start+datetime.timedelta(minutes=90);line='\t'.join([NONCE,start.isoformat(),expiry.isoformat(),'WP1287 formal review1 preparation',start.isoformat()]);LOCK.write_text(line,encoding='utf-8');assert LOCK.read_text()==line
commands=[]
def run(label,args,cwd=SOURCE,timeout=300):
 r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,timeout=timeout);(R/(label+'.stdout')).write_bytes(r.stdout);(R/(label+'.stderr')).write_bytes(r.stderr);commands.append({'label':label,'rc':r.returncode});assert r.returncode==0,(label,r.returncode);return r.stdout.decode('utf-8',errors='replace').strip()
try:
 raw=base64.b64decode((R/'review.zip.b64').read_text(encoding='utf-8-sig'),validate=True);assert len(raw)==71799 and hashlib.sha256(raw).hexdigest()=='7b39622017c4f8b0b062ac4f6643ccc971dcb77b9358a16b2ca6f29b4912c460';(R/'review.zip').write_bytes(raw)
 assert not INPUT.exists() and not REPO.exists();INPUT.mkdir()
 with zipfile.ZipFile(R/'review.zip') as z:
  assert sum(x.file_size for x in z.infolist())<4*1024*1024
  for x in z.infolist():
   p=Path(x.filename);assert not p.is_absolute() and '..' not in p.parts and not x.is_dir() and (x.external_attr>>16)&0o170000==0o100000
   target=INPUT/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(x))
 manifest=json.loads((INPUT/'MANIFEST.json').read_text());assert len(manifest['files'])==20
 for name,entry in manifest['files'].items():p=INPUT/name;assert p.stat().st_size==entry['bytes'] and sha(p)==entry['sha256']
 run('base-present',[git,'cat-file','-e',B+'^{commit}'])
 run('clone',[git,'clone','--no-hardlinks','--no-checkout','--config','core.autocrlf=false','--config','core.longpaths=true',str(SOURCE),str(REPO)])
 run('bundle-verify',[git,'bundle','verify',str(INPUT/'candidate-H2.bundle')],REPO)
 run('bundle-import',[git,'fetch',str(INPUT/'candidate-H2.bundle'),'refs/heads/agent/wp1287-r3-g3-codex:refs/heads/review/wp1287-h2-r13'],REPO)
 run('checkout',[git,'checkout','--detach',H],REPO)
 run('remove-remote',[git,'remote','remove','origin'],REPO)
 assert run('head',[git,'rev-parse','HEAD'],REPO)==H and run('tree',[git,'rev-parse','HEAD^{tree}'],REPO)==TREE
 assert run('root',[git,'rev-list','--max-parents=0','HEAD'],REPO)==ROOT_COMMIT
 assert not run('status',[git,'status','--porcelain'],REPO)
 expected=['.agents/skills/playwright-browser/'+n for n in ['SKILL.md','package-lock.json','package.json']]
 assert sorted(run('scope',[git,'diff','--name-only',B,H],REPO).splitlines())==expected
 for name in ['package.json','package-lock.json','SKILL.md']:assert sha(REPO/'.agents/skills/playwright-browser'/name)==sha(INPUT/'candidate'/name)
 assign=json.loads((R/'assignment.json').read_text());assert sha(R/'prompt.txt')==assign['prompt_sha256'] and sha(R/'SPEC-r13.md')==assign['spec_sha256']
 deadline=(utc()+datetime.timedelta(minutes=45)).strftime('%Y-%m-%dT%H:%M:%SZ')
 cmd=[sys.executable,str(launcher),'check','--workspace',str(REPO),'--expected-root-commit',ROOT_COMMIT,'--expected-head',H,'--require-clean','--prompt-file',str(R/'prompt.txt'),'--expected-prompt-sha256',assign['prompt_sha256'],'--deadline-utc',deadline,'--json']
 result=run('canonical-check',cmd,R)
 runtime={'workspace':str(REPO),'input_root':str(INPUT),'candidate':H,'tree':TREE,'root_commit':ROOT_COMMIT,'launcher':str(launcher),'launcher_sha256':sha(launcher),'codex':str(exe),'codex_sha256':sha(exe),'codex_version':version,'python':sys.executable,'prompt_sha256':assign['prompt_sha256'],'spec_sha256':assign['spec_sha256'],'deadline_utc':deadline,'lock_nonce':NONCE,'lock_expiry':expiry.isoformat(),'model_invoked':False,'inputs_verified':20,'source_write_set':[],'commands':commands}
 save(R/'runtime.json',runtime);print(json.dumps({'bootstrap_rc':0,'head':H,'tree':TREE,'clean':True,'independent_clone':True,'inputs_verified':20,'source_hashes_match':True,'launcher_hash_matches':True,'offline_readiness':True,'codex_version':version,'python_version':sys.version.split()[0],'deadline_utc':deadline,'model_invoked':False}),flush=True)
except BaseException as e:
 save(R/'bootstrap-failure.json',{'at':utc().isoformat(),'error_type':type(e).__name__,'traceback':traceback.format_exc(),'commands':commands,'model_invoked':False})
 if LOCK.read_text(encoding='utf-8-sig').split('\t')[0]==NONCE:LOCK.write_bytes(b'')
 print(json.dumps({'bootstrap_rc':2,'error_type':type(e).__name__,'commands':commands,'lock_released':not LOCK.read_bytes(),'model_invoked':False}),flush=True);sys.exit(2)
