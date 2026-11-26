"""Benign path conformance fixtures, scratch repositories only; no product mutation."""
import pathlib,sys,os,json,tarfile,importlib.util,contextlib,io,tempfile
W=pathlib.Path(__file__).resolve().parent;R=W.parent/'repo'
os.environ['TMPDIR']=str(W/'tmp');tempfile.tempdir=str(W/'tmp')
sys.path.insert(0,str(R/'.claude/dev'));import packet_loop_test as T
out=[]
scenarios=['regular','executable','nested','dot','double_slash','parent','missing_parent','file_parent','chain_parent','literal_backslash','backslash_parent','case','nfd','homoglyph','nonutf_exact','nonutf_missing','empty','gitlink','export_ignore']
for scenario in scenarios:
 d=W/('paths-'+sys.version.split()[0])/scenario;d.mkdir(parents=True,exist_ok=True);c=T.Ctx(T.CANONICAL,d)
 def fixture(w,m):
  p=w/T._D2B_PROV;(p/'sub').mkdir();(p/'sub/keep.txt').write_bytes(b'ordinary fixture\n');(p/'note.txt').write_bytes(b'ordinary fixture\n')
  target={'regular':'note.txt','executable':'note.txt','nested':'../note.txt','dot':'./note.txt','double_slash':'sub//keep.txt','parent':'sub/../note.txt','missing_parent':'absent/../note.txt','file_parent':'note.txt/../note.txt','chain_parent':'first/../note.txt','literal_backslash':r'a\b.txt','backslash_parent':r'a\b/../note.txt','case':'NOTE.TXT','nfd':'e\u0301.txt','homoglyph':'nоte.txt','nonutf_exact':os.fsdecode(b'raw-\xff.txt'),'nonutf_missing':os.fsdecode(b'raw-\xfe.txt'),'empty':'','gitlink':'module','export_ignore':'note.txt'}[scenario]
  if scenario=='executable':(p/'note.txt').chmod(0o755)
  if scenario=='literal_backslash':(p/target).write_bytes(b'ordinary fixture\n')
  if scenario=='backslash_parent':(p/r'a\b').mkdir();(p/r'a\b'/'x').write_bytes(b'x')
  if scenario=='nfd':(p/'é.txt').write_bytes(b'x')
  if scenario.startswith('nonutf'):(p/os.fsdecode(b'raw-\xff.txt')).write_bytes(b'x')
  if scenario=='chain_parent':os.symlink('note.txt',p/'first')
  if scenario=='export_ignore':(w/'.gitattributes').write_text(T._D2B_PROV+'/note.txt export-ignore\n')
  link=p/('sub/link' if scenario=='nested' else 'link')
  if scenario=='empty':return {str(link.relative_to(w)):''}
  os.symlink(target,link)
  if scenario=='gitlink':T._g(w,'update-index','--add','--cacheinfo',f'160000,{m},{T._D2B_PROV}/module')
 x=T._d1106_kho(c,o=fixture)
 rc,o,e=T._d1106_chay(c,x)
 row=dict(scenario=scenario,runtime=sys.version,mode='native',rc=rc,stdout=o.decode(),stderr=e.decode());out.append(row);print(scenario,'native',rc,flush=True)
 # Model an older/native extractor preserving safe link text: data_filter checks first, only normalization is undone.
 if scenario in ['dot','double_slash','parent','missing_parent','file_parent','chain_parent','backslash_parent']:
  sp=importlib.util.spec_from_file_location('path_product',T.CANONICAL);M=importlib.util.module_from_spec(sp);sp.loader.exec_module(M)
  original=tarfile.data_filter;named=tarfile._NAMED_FILTERS['data'];extract=tarfile.TarFile.extractall;observed=[]
  def retained(member,dest):
   z=original(member,dest)
   return z.replace(linkname=member.linkname) if member.issym() else z
  def capture(self,path='.',*a,**kw):
   z=extract(self,path,*a,**kw)
   for member in self.getmembers():
    if member.issym():
     p=pathlib.Path(path)/member.name;observed.append(dict(name=member.name,target=os.readlink(p),exists=p.exists(),is_file=p.is_file(),is_dir=p.is_dir()))
   return z
  so,se=io.StringIO(),io.StringIO();tarfile.data_filter=retained;tarfile._NAMED_FILTERS['data']=retained;tarfile.TarFile.extractall=capture
  try:
   with contextlib.redirect_stdout(so),contextlib.redirect_stderr(se):
    try:rc=M.main(['--state-dir',str(c.sd()),'kiem-dong-wp','--root',str(x['w']),'--bien-ban',str(x['goc']/'bb.yaml'),'--lease',str(x['goc']/'ls.yaml')])
    except SystemExit as ex:rc=ex.code
  finally:tarfile.data_filter=original;tarfile._NAMED_FILTERS['data']=named;tarfile.TarFile.extractall=extract
  out.append(dict(scenario=scenario,mode='retained_safe_link_text',rc=rc,stdout=so.getvalue(),stderr=se.getvalue(),observed=observed));print(scenario,'retained',rc,flush=True)
(W/('paths-'+sys.version.split()[0]+'.json')).write_text(json.dumps(out,ensure_ascii=True,indent=2))
