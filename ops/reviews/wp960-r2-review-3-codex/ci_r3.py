import json,os,subprocess
from pathlib import Path
root=Path(__file__).resolve().parent
src=root/'cay-kho';dst=Path('/tmp/wp960-r3-ci')
def run(*args,check=True,**kw):
 r=subprocess.run(args,text=True,capture_output=True,**kw)
 if check and r.returncode:raise RuntimeError((args,r.returncode,r.stderr))
 return r
run('git','clone','--no-hardlinks','--no-checkout',str(src),str(dst))
sha='934a5b063670acfbed410487d8244cd17d586d6e'
tree=run('git','-C',str(dst),'rev-parse',sha+'^{tree}').stdout.strip()
base=run('git','-C',str(dst),'rev-parse','2618eb4').stdout.strip()
env={**os.environ,'GIT_AUTHOR_NAME':'review','GIT_COMMITTER_NAME':'review','GIT_AUTHOR_EMAIL':'review@local','GIT_COMMITTER_EMAIL':'review@local','GIT_AUTHOR_DATE':'2026-10-27T00:00:00Z','GIT_COMMITTER_DATE':'2026-10-27T00:00:00Z'}
merge=run('git','-C',str(dst),'commit-tree',tree,'-p',base,'-p',sha,'-m','local CI merge simulation',env=env).stdout.strip()
run('git','-C',str(dst),'checkout','--detach',merge)
run('git','-C',str(dst),'update-ref','--no-deref','-d','refs/remotes/origin/HEAD')
run('git','-C',str(dst),'update-ref','refs/remotes/origin/master',base)
for args in [('rev-parse','HEAD','HEAD^{tree}'),('rev-list','--parents','-1','HEAD'),('rev-parse','--is-shallow-repository'),('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/origin/HEAD','refs/remotes/origin/master','refs/heads/master')]:
 r=run('git','-C',str(dst),*args);print(json.dumps(dict(command=args,rc=r.returncode,out=r.stdout,err=r.stderr)),flush=True)
r=run('python3','-B','ops/bien_nhan_v2.py','--root','.',cwd=dst,check=False)
print(json.dumps(dict(command='gate',rc=r.returncode,out=r.stdout,err=r.stderr),ensure_ascii=False),flush=True)
