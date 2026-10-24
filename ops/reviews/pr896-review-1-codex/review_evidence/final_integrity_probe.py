import hashlib
import json
import os
from pathlib import Path
import subprocess

root=Path.cwd()
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
def run(*a):
    return subprocess.run(['git',*a],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
head=run('rev-parse','HEAD').stdout.decode().strip()
tree=run('rev-parse','HEAD^{tree}').stdout.decode().strip()
print('HEAD:',head)
print('tree:',tree)
assert head=='816f43988eb3012726120ad00166a989cc2b9af6'
assert tree=='3da0ce24590dfcf2e60805b2bef76687cdd64405'
for args in (('status','--porcelain=v1','--untracked-files=all','--ignored'),('diff','--exit-code'),('diff','--cached','--exit-code')):
    r=run(*args)
    print('git '+' '.join(args)+f': rc={r.returncode}; output={r.stdout.decode()!r}; stderr={r.stderr.decode()!r}')
    assert r.returncode==0 and not r.stdout
data=run('ls-tree','-r','-z','HEAD').stdout
checked=0
failures=[]
for record in data.split(b'\0'):
    if not record: continue
    meta,name=record.split(b'\t',1)
    mode,kind,oid=meta.split()
    if kind!=b'blob': continue
    file=root/os.fsdecode(name)
    body=os.fsencode(os.readlink(file)) if mode==b'120000' else file.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest().encode()
    if actual!=oid: failures.append(os.fsdecode(name))
    checked+=1
print('tracked blob content compared to HEAD:',checked,'; mismatches=',failures)
for name in failures:
    attrs=run('check-attr','text','eol','filter','--',name).stdout.decode()
    blob=run('show','HEAD:'+name).stdout
    body=(root/name).read_bytes()
    oid=run('rev-parse','HEAD:'+name).stdout.decode().strip()
    filtered=run('hash-object','--path='+name,name).stdout.decode().strip()
    print(attrs,end='')
    print(name, 'work CRLF=',body.count(b'\r\n'),'blob CRLF=',blob.count(b'\r\n'),
          'normalize_CRLF_matches=',body.replace(b'\r\n',b'\n')==blob,'filtered_hash_matches=',filtered==oid)
    assert 'eol: crlf' in attrs and 'filter: unspecified' in attrs
    assert body.replace(b'\r\n',b'\n')==blob and filtered==oid
print('5200 raw matches + 3 declared CRLF checkout matches = 5203 correct files')
base='1ccc31498b7d37c12305e8f1b5bf2d1fc217b92e'
actual=run('diff',base,head).stdout
supplied=(root.parent/'diff.patch').read_bytes()
print('provided diff.patch equals git diff base head:',actual==supplied)
assert actual==supplied
print('actual numstat:')
print(run('diff','--numstat',base,head).stdout.decode(),end='')
print('Reviewed source remains exact; only report/evidence/hint written outside cay-kho/.')
print('Snapshot equality does not prove absence of temporary historical writes; commands were constrained to read-only source and external scratch.')
