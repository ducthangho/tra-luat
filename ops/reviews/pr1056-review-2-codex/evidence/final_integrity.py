from pathlib import Path
import subprocess,hashlib
b=Path(__file__).resolve().parent.parent;head='047eaa4d26a5bb1e702199c870f42480aebed673'
for name in ('cay-kho','review-copy'):
 r=b/name
 for args in [['rev-parse','HEAD','HEAD^{tree}'],['status','--short','--untracked-files=all','--ignored=matching'],['diff','--exit-code'],['diff','--cached','--exit-code'],['diff','--check'],['config','core.abbrev']]:
  p=subprocess.run(['git','-C',str(r),*args],capture_output=True,text=True);print(name,'git',' '.join(args),'rc',p.returncode,'stdout',p.stdout.strip() or '(empty)','stderr',p.stderr.strip() or '(empty)')
 paths=subprocess.check_output(['git','-C',str(r),'diff','--name-only','6db9341',head],text=True).splitlines();ok=sum((r/p).read_bytes()==subprocess.check_output(['git','-C',str(r),'show',head+':'+p]) for p in paths);print(name,'ALL_CHANGED_FILES_EQUAL_HEAD',ok,'/',len(paths))
r=b/'cay-kho'
paths=subprocess.check_output(['git','-C',str(r),'diff','--name-only','6db9341','7333f97'],text=True).splitlines();ok=sum((r/p).read_bytes()==subprocess.check_output(['git','-C',str(r),'show','7333f97:'+p]) for p in paths);print('ORIGINAL_ARTIFACT_COMMIT_FILES_EQUAL',ok,'/',len(paths))
raw=subprocess.check_output(['git','-C',str(r),'diff','1aae17b',head]);print('SUPPLIED_PATCH_EQUAL',raw==(b/'diff-tu-luot1.patch').read_bytes(),'BYTES',len(raw))
prompt=(b/'PROMPT.md').read_bytes();snap=(b/'run/6ad116a8/prompt.snapshot').read_bytes();print('CURRENT_PROMPT_SNAPSHOT_EQUAL',prompt==snap,'PROMPT_BYTES',len(prompt),'SHA256',hashlib.sha256(prompt).hexdigest())
