"""Filesystem semantics models only. No edits to product code; scratch-only benign paths."""
import pathlib,os,sys,json,tempfile,tarfile,unicodedata,copy,importlib.util,contextlib,io
W=pathlib.Path(__file__).resolve().parent;R=W.parent/'repo'
os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['TMPDIR']=str(W/'tmp');tempfile.tempdir=str(W/'tmp')
sys.path.insert(0,str(R/'.claude/dev'));import packet_loop_test as T
# Capture both streams without replacing Git calls; only filesystem semantics are modeled.
def invoke(script,args,sd,env=None,lenh="plain"):
 sp=importlib.util.spec_from_file_location("review_product",script)
 m=importlib.util.module_from_spec(sp);sys.path.insert(0,str(script.parent));sp.loader.exec_module(m)
 walk=os.walk;out,err=io.StringIO(),io.StringIO();rc=0
 if lenh=="tep":
  os.walk=lambda *a,**k: ((g,[n for n in ds if not os.path.islink(os.path.join(g,n))],fs+[n for n in ds if os.path.islink(os.path.join(g,n))]) for g,ds,fs in walk(*a,**k))
 try:
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
   try:m.main(["--state-dir",str(sd),*map(str,args)])
   except SystemExit as e:rc=e.code
 finally:os.walk=walk
 return rc,out.getvalue().encode(),err.getvalue().encode()
T._rev_list_loi=invoke
out=[]
for scenario in ('case','nfc','backslash','missing','file_parent'):
 d=W/'models'/scenario;d.mkdir(parents=True,exist_ok=True);c=T.Ctx(T.CANONICAL,d)
 def fixture(w,m):
  p=w/T._D2B_PROV
  dirname='é' if scenario=='nfc' else 'sub'
  (p/dirname).mkdir();(p/dirname/'x').write_bytes(b'x')
  if scenario=='backslash':(p/dirname/'leaf').mkdir();(p/dirname/'leaf'/'x').write_bytes(b'x')
  if scenario=='file_parent':(p/'note.txt').write_bytes(b'x')
  target={'case':'SUB','nfc':'e\u0301','backslash':r'sub\leaf','missing':'absent/../sub','file_parent':'note.txt/../sub'}[scenario]
  return {T._D2B_PROV+'/d':target}
 x=T._d1106_kho(c,o=fixture)
 original_named_filter=tarfile._NAMED_FILTERS['data']; original_filter=tarfile.data_filter; original_extract=tarfile.TarFile.extractall; original_readlink=os.readlink
 raw={};observed=[]
 def retained(member,dest):
  filtered=original_filter(member,dest)
  if member.issym():filtered=filtered.replace(linkname=member.linkname)
  return filtered
 def extract(self,path='.',*a,**kw):
  result=original_extract(self,path,*a,**kw)
  if scenario in ('case','nfc','backslash'):
   for member in self.getmembers():
    if member.issym() and member.name.endswith('/d'):
     p=pathlib.Path(path)/member.name;old=original_readlink(p)
     # Model one case-insensitive or canonical-equivalent name lookup.
     dest='é' if scenario=='nfc' else 'sub/leaf' if scenario=='backslash' else 'sub'
     p.unlink();os.symlink(dest,p,target_is_directory=True)
     raw[str(p)]=old
     observed.append(dict(raw_target=old,physical_target=dest,referent_is_directory=p.is_dir()))
  else:
   for member in self.getmembers():
    if member.issym() and member.name.endswith('/d'):
     p=pathlib.Path(path)/member.name
     observed.append(dict(raw_target=original_readlink(p),referent_is_directory=p.is_dir(),is_symlink=p.is_symlink(),referent_exists=p.exists()))
  return result
 def readlink(p,*a,**kw):return raw.get(str(p),original_readlink(p,*a,**kw))
 try:
  tarfile._NAMED_FILTERS['data']=retained;tarfile.data_filter=retained;tarfile.TarFile.extractall=extract;os.readlink=readlink
  for label,script in [('previous',W/'previous/packet_loop.py'),('head',T.CANONICAL)]:
   c.script=script
   for model in ('plain', 'tep'):
    observed.clear()
    rc,o,e=T._d1106_chay(c,x,git_loi=model)
    out.append(dict(scenario=scenario,code=label,walk_model=model or 'native',rc=rc,stdout=o.decode(),stderr=e.decode(),observed=observed.copy(),model='retained link text; case/NFC referent alias when requested; walk_model names separate file classification model'))
    print(scenario,label,model,rc,e.decode().strip(),flush=True)
 finally:tarfile._NAMED_FILTERS['data']=original_named_filter;tarfile.data_filter=original_filter;tarfile.TarFile.extractall=original_extract;os.readlink=original_readlink
(W/'models.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
