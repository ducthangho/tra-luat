"""Reproduce C01 on unmodified code using benign A/a Git directories.
Linux control + explicit filesystem casefold simulation; NOT a native Windows test.
No symlinks, traversal paths, product changes, or network.
"""
from pathlib import Path
import sys,copy,json,io,contextlib,tarfile,tempfile,hashlib
R=Path(__file__).resolve().parent.parent/'repo';W=R.parent/'work';sys.path.insert(0,str(R/'.claude/dev'))
import packet_loop_test as T
import packet_loop as P
with tempfile.TemporaryDirectory(dir=W/'tmp',prefix='case_directory_') as td:
 c=T.Ctx(T.CANONICAL,Path(td))
 def build(w,m):
  for n in ('A','a'):(w/T._D2B_PROV/n).mkdir()
  (w/T._D2B_PROV/'A/note.txt').write_bytes(b'note\n')
  T._d2b_readback(w,m,T._D2B_PROV+'/a')
 x=T._d1106_kho(c,o=build)
 change=T._d2b_mien(readback_thu_muc=T._D2B_PROV+'/A')
 rc,o,e=T._d1106_chay(c,x,change) # also writes bb.yaml/ls.yaml consumed below
 result={'reviewed_sha':'2439922c67a091c53e277c9e0b13d8fc04089453','product_sha256':hashlib.sha256(T.CANONICAL.read_bytes()).hexdigest(),'linux_control':{'rc':rc,'stdout':o.decode(),'stderr':e.decode()}}
 original_extract=tarfile.TarFile.extractall;original_Path=P.Path
 class FoldPath(type(Path())):
  def __truediv__(self,other):return super().__truediv__(str(other).casefold())
 def extract_fold(self,path='.',members=None,**kw):
  ms=[copy.copy(t) for t in (members if members is not None else self.getmembers())]
  for t in ms:t.name=t.name.casefold()
  return original_extract(self,path,members=ms,**kw)
 P.Path=FoldPath;tarfile.TarFile.extractall=extract_fold
 so,se=io.StringIO(),io.StringIO()
 try:
  with contextlib.redirect_stdout(so),contextlib.redirect_stderr(se):
   try:
    rc=P.main(['--state-dir',str(c.sd()),'kiem-dong-wp','--root',str(x['w']),'--bien-ban',str(x['goc']/'bb.yaml'),'--lease',str(x['goc']/'ls.yaml')])
   except SystemExit as ex:rc=ex.code
 finally:P.Path=original_Path;tarfile.TarFile.extractall=original_extract
 result['case_insensitive_simulation']={'rc':rc,'stdout':so.getvalue(),'stderr':se.getvalue(),'scope':'Only archive name and path lookup case folding; all Git operations, bytes, schema, D1-D4, module and D2b code are real.'}
 oid=x['bb']['gate_output_nguon']['oid'];raw=T._g(x['w'],'ls-tree','-r','-t',oid,'--',T._D2B_PROV+'/A',T._D2B_PROV+'/a');result['tree']=raw
 assert result['linux_control']['rc']==12 and 'mien:readback' in result['linux_control']['stderr']
 assert rc==0 and 'D2b ĐẠT mien' in so.getvalue() and 'ĐÓNG ĐƯỢC WP' in so.getvalue()
 (W/'case_directory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
