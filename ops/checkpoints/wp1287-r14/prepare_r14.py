"""Revalidate existing untouched clone and issue fresh scoped review deadline; no model."""
import os,sys,json,hashlib,datetime,subprocess,shutil
from pathlib import Path
R=Path(r'D:\tl-win\wp1287-H2-formal-20261110');L=Path(r'D:\tl-win\KHOA.txt');N='wp1287-r14-g14-review-1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
assert os.environ.get('COMPUTERNAME')=='ASUS-LAPTOP';assert not (R/'invocation.json').exists() and not (R/'runs').exists();assert not (R/'invocation-r14.json').exists() and not (R/'runs-r14').exists();assert not L.read_text(encoding='utf-8-sig').strip()
v=json.loads((R/'runtime.json').read_text());a=json.loads((R/'assignment-r14.json').read_text());auth=json.loads((R/'authorization-scope-r14.json').read_text());assert auth['candidate_full_private_clone']==v['candidate']
assert sha(R/'run_review_r14.py')==a['run_review_sha256'] and sha(R/'prompt-r14.txt')==a['prompt_sha256'] and sha(R/'SPEC-r14.md')==a['spec_sha256'];assert sha(v['launcher'])==v['launcher_sha256'] and sha(v['codex'])==v['codex_sha256'];assert sha(R/'review.zip')==auth['review_archive']['sha256']
manifest=json.loads((R/'inputs/MANIFEST.json').read_text());assert len(manifest['files'])==20
for name,x in manifest['files'].items():p=R/'inputs'/name;assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0';git=shutil.which('git');assert git
def read(*args):return subprocess.check_output([git,'-C',v['workspace'],*args],env=env,timeout=60).decode('utf-8').strip()
assert read('rev-parse','HEAD')==v['candidate'] and read('rev-parse','HEAD^{tree}')==v['tree'] and not read('status','--porcelain')
for name in ['package.json','package-lock.json','SKILL.md']:assert sha(Path(v['workspace'])/'.agents/skills/playwright-browser'/name)==sha(R/'inputs/candidate'/name)
now=datetime.datetime.now(datetime.timezone.utc);expiry=now+datetime.timedelta(minutes=90);deadline=(now+datetime.timedelta(minutes=45)).strftime('%Y-%m-%dT%H:%M:%SZ')
line='\t'.join([N,now.isoformat(),expiry.isoformat(),'WP1287 same-scope confirmed formal review1',now.isoformat()]);assert not L.read_text(encoding='utf-8-sig').strip();L.write_text(line,encoding='utf-8');assert L.read_text()==line
v.update(prompt_sha256=a['prompt_sha256'],spec_sha256=a['spec_sha256'],deadline_utc=deadline,lock_nonce=N,lock_expiry=expiry.isoformat(),model_invoked=False,authorization_scope_sha256=sha(R/'authorization-scope-r14.json'))
save(R/'runtime-r14.json',v);proof={'at':now.isoformat(),'same_scope_direct_confirmation_recorded':True,'candidate':v['candidate'],'tree':v['tree'],'clone_clean':True,'inputs_verified':20,'source_hashes_match':True,'launcher_and_cli_hashes_match':True,'prior_model_invocations':0,'deadline_utc':deadline,'model_invoked':False};save(R/'fresh-preflight-r14.json',proof);print(json.dumps(proof),flush=True)
