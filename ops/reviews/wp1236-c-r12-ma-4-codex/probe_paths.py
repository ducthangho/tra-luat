import pathlib,sys,os,json,subprocess,tempfile,importlib.util,contextlib,io,unicodedata
W=pathlib.Path(__file__).resolve().parent; R=W.parent/'repo'
os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['TMPDIR']=str(W/'tmp');tempfile.tempdir=str(W/'tmp')
sys.path.insert(0,str(R/'.claude/dev'))
import packet_loop_test as T
old=W/'previous';old.mkdir(exist_ok=True)
for name in ('packet_loop.py','launcher.py'):
 (old/name).write_bytes(subprocess.check_output(['git','show','dbe650d:.claude/dev/'+name],cwd=R))
# Benign fixture variants, entirely within a disposable provenance directory.
variants={
 'direct':('sub',{}),
 'case_target':('SUB',{}),
 'nfc_target':('e\u0301',{'é/x':b'x'}),
 'chain':('e',{'e':'sub'}),
 'cycle':('e',{'e':'d'}),
 'nested':('sub',{}),
 'missing_component':('absent/../sub',{}),
 'file_component':('note.txt/../sub',{'note.txt':b'x'}),
 'file_link':('note.txt',{'note.txt':b'x'}),
 'yaml_link':('note.txt',{'note.txt':b'x'}),
 'slash_target':('sub/leaf',{'sub/leaf/x':b'x'}),
 'root':('../../..',{}),
}
result=[]
for name,(target,extra) in variants.items():
 p=W/('paths-'+sys.version.split()[0])/name;p.mkdir(parents=True,exist_ok=True)
 c=T.Ctx(T.CANONICAL,p)
 def fixture(w,m):
  base=T._D2B_PROV
  (w/base/'sub').mkdir()
  (w/base/'sub/x').write_bytes(b'x')
  if name=='nested':
   (w/base/'inner/sub').mkdir(parents=True);(w/base/'inner/sub/x').write_bytes(b'x')
  links={base+('/inner/d' if name=='nested' else '/d.yaml' if name=='yaml_link' else '/d'):target}
  for path,v in extra.items():
   if isinstance(v,bytes):
    z=w/base/path;z.parent.mkdir(parents=True,exist_ok=True);z.write_bytes(v)
   else: links[base+'/'+path]=v
  return links
 x=T._d1106_kho(c,o=fixture)
 for label,script in [('previous',old/'packet_loop.py'),('head',T.CANONICAL)]:
  for model in (False,'tep'):
   c.script=script
   rc,out,err=T._d1106_chay(c,x,git_loi=model)
   row=dict(case=name,code=label,model=model or 'native_linux',rc=rc,stdout=out.decode(),stderr=err.decode())
   result.append(row);print(name,label,model,rc,err.decode().strip()[:180],flush=True)
 (W/('paths-'+sys.version.split()[0]+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2))
