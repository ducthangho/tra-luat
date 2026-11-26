"""Scratch-only benign file mode, ordering, and raw backslash conformance checks."""
import pathlib,sys,os,json,tempfile
W=pathlib.Path(__file__).resolve().parent;R=W.parent/'repo';tempfile.tempdir=str(W/'tmp');os.environ['TMPDIR']=str(W/'tmp')
sys.path.insert(0,str(R/'.claude/dev'));import packet_loop_test as T
out=[]
for scenario in ['gitlink','backslash_nested','backslash_directory','backslash_executable','yaml_link','symlink_before_k1']:
 d=W/'modes'/scenario;d.mkdir(parents=True,exist_ok=True);c=T.Ctx(T.CANONICAL,d)
 def fixture(w,m):
  p=w/T._D2B_PROV
  if scenario.startswith('backslash'):
   if scenario=='backslash_nested':
    (p/'sub').mkdir();(p/'sub'/r'a\b.txt').write_bytes(b'x');os.symlink(r'a\b.txt',p/'sub/link')
   elif scenario=='backslash_directory':
    (p/r'a\b').mkdir();(p/r'a\b'/'x.txt').write_bytes(b'x');os.symlink(r'a\b/x.txt',p/'link')
   else:
    (p/r'a\b.txt').write_bytes(b'x');(p/r'a\b.txt').chmod(0o755);os.symlink(r'a\b.txt',p/'link')
  elif scenario=='yaml_link':
   (p/'ordinary.txt').write_bytes(b'x');os.symlink('ordinary.txt',p/'link.yaml')
  elif scenario=='symlink_before_k1':
   os.symlink('missing',p/'link');(w/T._D2B_TEP).write_bytes(b'ordinary invalid evaluation\n')
  else:os.symlink('module',p/'link')
 def after(w,oid,bb):
  if scenario!='gitlink':return
  T._g(w,'checkout','-q','hs');T._g(w,'update-index','--add','--cacheinfo',f'160000,{bb["merge_commit"]},{T._D2B_PROV}/module');T._g(w,'commit','-qm','gitlink fixture');oid=T._g(w,'rev-parse','HEAD');T._g(w,'push','-q','origin','HEAD:refs/heads/ops/x');T._g(w,'checkout','-q','master');T._g(w,'fetch','-q','origin');bb['gate_output_nguon']['oid']=oid
 x=T._d1106_kho(c,o=fixture,sau=after);rc,o,e=T._d1106_chay(c,x)
 tree=T._g(x['w'],'ls-tree','-r','-t',x['bb']['gate_output_nguon']['oid'],'--',T._D2B_PROV)
 out.append(dict(scenario=scenario,rc=rc,stdout=o.decode(),stderr=e.decode(),tree=tree));print(scenario,rc,e.decode().strip(),flush=True)
(W/'modes.json').write_text(json.dumps(out,ensure_ascii=True,indent=2))
