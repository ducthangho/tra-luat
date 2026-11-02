from pathlib import Path
import hashlib,subprocess,json
root=Path('cay-kho');sha='3a52e6d194d08a755793cf449f393fb15b56757b'
for args in [('rev-parse','HEAD','HEAD^{tree}'),('status','--short'),('diff','--check','44884446f71c89e25f9a72ac58e4f597db63c1ba','HEAD')]:
 p=subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True);print(json.dumps(dict(command=list(args),rc=p.returncode,out=p.stdout,err=p.stderr)))
for name in ['ops/bien_nhan_v2.py','ops/bien_nhan_v2_test.py','ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md']:
 actual=(root/name).read_bytes();blob=subprocess.check_output(['git','-C',str(root),'show',sha+':'+name]);print(json.dumps(dict(path=name,byte_identical=actual==blob,sha256=hashlib.sha256(actual).hexdigest())))
for name in ['c86','m94']:
 for line in Path('evidence/suite.log').read_text().splitlines():
  if name+'_' in line:print(line)
