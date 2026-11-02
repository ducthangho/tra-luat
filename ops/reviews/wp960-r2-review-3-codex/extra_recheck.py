import json,os,shutil,subprocess,tempfile,zlib
from pathlib import Path
import probe_recheck as h
b=h.b;t=h.t

def extra():
 for name in (__import__('sys').argv[2:] or ('replace-drop-parent','graft-silent','foreign-git-dir','missing-alternate','broken-commit-graph','pack-corrupt','packed-ref-broken')):
  with tempfile.TemporaryDirectory(prefix='r3-extra-') as tmp:
   p=Path(tmp)/'repo';p.mkdir();k,sha,al=h.anc(p,which='B0' if name!='foreign-git-dir' else 'M')
   before=h.raw(p,al);h.log(name=name,phase='before',result=before)
   env={}
   if name=='replace-drop-parent':
    src=p/'.git/objects'/k['M'][:2]/k['M'][2:]
    data=zlib.decompress(src.read_bytes()).split(b'\0',1)[1].replace(b'parent '+k['B0'].encode()+b'\n',b'')
    new=h.git(p,'hash-object','-t','commit','-w','--stdin',inp=data.decode())['out']
    h.log(name=name,create_replacement=h.git(p,'replace',k['M'],new),replacement=new,fsck=h.git(p,'fsck','--full'))
   if name=='graft-silent':
    (p/'.git/info/grafts').write_text(k['M']+'\n');k['g']('config','advice.graftFileDeprecated','false')
   if name=='foreign-git-dir':
    q=Path(tmp)/'other';q.mkdir();other=t._kho_cau(q);other['g']('update-ref','refs/heads/master',other['X'])
    env={'GIT_DIR':str(q/'.git')}
   if name=='missing-alternate':
    (p/'.git/objects/info/alternates').write_text('/tmp/r3-nonexistent-object-directory\n')
   if name=='broken-commit-graph':
    k['g']('commit-graph','write','--reachable');f=p/'.git/objects/info/commit-graph';content=bytearray(f.read_bytes());content[0:4]=b'NOPE';f.chmod(0o644);f.write_bytes(content)
   if name=='pack-corrupt':
    k['g']('repack','-ad');pack=next((p/'.git/objects/pack').glob('*.pack'));data=bytearray(pack.read_bytes());data[25]^=0xff;pack.chmod(0o644);pack.write_bytes(data)
   if name=='packed-ref-broken':
    k['g']('pack-refs','--all');f=p/'.git/packed-refs';f.write_text(f.read_text()+'not-an-oid refs/remotes/origin/master\n')
   h.log(name=name,health=h.git(p,'rev-parse','--is-shallow-repository',env=env),candidates=h.git(p,'rev-parse','--disambiguate='+sha[:7],env=env),kind=h.git(p,'cat-file','--batch-check=%(objectname) %(objecttype)',inp=sha+'\n',env=env),refs=h.git(p,'for-each-ref','--format=%(refname) %(objectname) %(objecttype)',*b._REF_MAC_DINH,env=env),ancestor=h.git(p,'merge-base','--is-ancestor',sha,'refs/heads/master',env=env))
   for no in ((),(h.KEY,)):
    h.log(name=name,phase='after',debt=bool(no),result=h.raw(p,al,no,env=env))
   if name=='replace-drop-parent':
    h.log(name=name,no_replace_ancestor=h.git(p,'merge-base','--is-ancestor',sha,'refs/heads/master',env={'GIT_NO_REPLACE_OBJECTS':'1'}))

def clean_corpus():
 p=Path("/tmp/wp960-r3-recheck-clean")
 if not p.exists(): shutil.copytree(h.COPY,p)
 for env in ({'GIT_TRACE':'1'},{'GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'core.fsyncObjectFiles','GIT_CONFIG_VALUE_0':'true'}):
  r=subprocess.run(['python3','-B',str(p/'ops/bien_nhan_v2.py'),'--root',str(p)],capture_output=True,text=True,env={**os.environ,**env})
  h.log(env=env,rc=r.returncode,out=r.stdout,err=r.stderr)
 refs=h.git(p,'show-ref','refs/heads/master');h.log(existing_remote=refs)
 tip=h.git(p,'rev-parse','HEAD')['out'];h.log(add_ref=h.git(p,'update-ref','refs/heads/master/topic',tip))
 r=subprocess.run(['python3','-B',str(p/'ops/bien_nhan_v2.py'),'--root',str(p)],capture_output=True,text=True)
 h.log(added_ref_rc=r.returncode,out=r.stdout,err=r.stderr)
 h.log(delete_ref=h.git(p,'update-ref','-d','refs/heads/master/topic'))

if __name__=='__main__':
 import sys
 globals()[sys.argv[1]]()
