import tempfile,subprocess,types
from pathlib import Path
import probe_recheck as h
b=h.b;t=h.t
source=subprocess.run(['git','-C',str(h.ROOT/'cay-kho'),'show','ae0d06c23fb777545fd7547a07d9f368e4122f49:ops/bien_nhan_v2.py'],capture_output=True,text=True,check=True).stdout
old=types.ModuleType('old');old.__file__=b.__file__;exec(compile(source,old.__file__,'exec'),old.__dict__)
for target in ('M','X'):
 with tempfile.TemporaryDirectory(prefix='r3-tag-') as tmp:
  p=Path(tmp);k=t._kho_cau(p);k['g']('tag','-a','release','-m','release',k[target]);tag=k['g']('rev-parse','refs/tags/release')
  al=t._ghi_bn_cau(p,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: Commit {tag[:7]} chua vao master.\n')})
  h.log(target=target,tag=tag,peel=h.git(p,'rev-parse',tag+'^{commit}'),old=old._commit_cua(p,tag[:7]),new=b._commit_cua(p,tag[:7]),old_full=old._commit_cua(p,tag),new_full=b._commit_cua(p,tag),head_cli=h.raw(p,al))
