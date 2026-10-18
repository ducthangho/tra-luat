import importlib.util,json,shutil,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path('/tmp/rv812-r5-hint');sys.path.insert(0,str(repo/'.claude/dev'))
s=importlib.util.spec_from_file_location('hint_tests',repo/'.claude/dev/packet_loop_test.py');t=importlib.util.module_from_spec(s);sys.modules[s.name]=t;s.loader.exec_module(t)
out=Path(tempfile.mkdtemp(prefix='review812-r5-hint-check-'));names={n for n,_ in t.CASES if n.startswith('r812_')}
r=t.chay_suite(t.CANONICAL,out/'baseline',names)
print(json.dumps({'baseline':len(r),'errors':{n:str(e) for n,e in r.items() if e is not None}},ensure_ascii=False),flush=True)
source=t.CANONICAL.read_text()
for name,(a,b,targets) in t.MUTANTS.items():
 if not name.startswith('r812_'):continue
 d=out/name;d.mkdir();src=source
 try:
  for old,new in t._cap_thay_the(a,b):
   assert old in src,(name,old);src=src.replace(old,new,1)
  (p:=d/'packet_loop.py').write_text(src);shutil.copyfile(t.HERE/'launcher.py',d/'launcher.py')
  results=t.chay_suite(p,d/'cases',set(targets))
  print(json.dumps({'mutant':name,'targets':{n:str(e) if e is not None else None for n,e in results.items()}},ensure_ascii=False),flush=True)
 except Exception as ex:print(json.dumps({'mutant':name,'error':str(ex)},ensure_ascii=False),flush=True)
print(json.dumps({'scratch':str(out)}),flush=True)
