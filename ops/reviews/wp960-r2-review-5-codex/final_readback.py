from pathlib import Path
import subprocess,hashlib,json
root=Path('cay-kho').resolve();sha='6dca85f463c6ce551eb8c27ff2d94b7a102e2fdf'
def g(*args):
 p=subprocess.run(['git','--no-optional-locks','-C',str(root),*args],capture_output=True,text=True)
 print(json.dumps(dict(command=['git',*args],rc=p.returncode,out=p.stdout,err=p.stderr),ensure_ascii=False))
 assert p.returncode==0
 return p.stdout.strip()
assert g('rev-parse','HEAD')==sha
g('rev-parse','HEAD^{tree}','--is-shallow-repository')
assert g('status','--short')==''
g('diff','--check','44884446f71c89e25f9a72ac58e4f597db63c1ba','HEAD')
g('diff','--numstat','44884446f71c89e25f9a72ac58e4f597db63c1ba','HEAD','--','ops/bien_nhan_v2.py','ops/bien_nhan_v2_test.py')
for f in ('ops/bien_nhan_v2.py','ops/bien_nhan_v2_test.py','ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md'):
 data=(root/f).read_bytes();blob=subprocess.check_output(['git','-C',str(root),'show',f'{sha}:{f}']);copy=(Path('/tmp/wp960-r5-copy')/f).read_bytes()
 print(json.dumps(dict(path=f,sha256=hashlib.sha256(data).hexdigest(),matches_reviewed_blob=data==blob,baseline_copy_matches=data==copy)))
 assert data==blob==copy
