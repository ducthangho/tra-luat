import importlib.util,json,shutil,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path(sys.argv[1]);sys.path.insert(0,str(repo/'.claude/dev'))
s=importlib.util.spec_from_file_location('r7_hint_t',repo/'.claude/dev/packet_loop_test.py');t=importlib.util.module_from_spec(s);sys.modules[s.name]=t;s.loader.exec_module(t)
out=Path(tempfile.mkdtemp(prefix='rv812-r7-hint-check-'));source=t.CANONICAL.read_text();names={n for n,_ in t.CASES if n.startswith('r812_r7_')}
r=t.chay_suite(t.CANONICAL,out/'baseline',names);print(json.dumps({'baseline':r,'scratch':str(out)},ensure_ascii=False),flush=True)
for n,(old,new,targets) in t.MUTANTS.items():
 if not n.startswith('r812_r7_') and n!='r812_r6_workflow_issue':continue
 d=out/n;d.mkdir();s=source
 for a,b in t._cap_thay_the(old,new):assert s.count(a)==1,(n,a,s.count(a));s=s.replace(a,b,1)
 p=d/'packet_loop.py';p.write_text(s);shutil.copyfile(t.HERE/'launcher.py',d/'launcher.py')
 print(json.dumps({'mutant':n,'results':t.chay_suite(p,d/'cases',set(targets))},ensure_ascii=False),flush=True)
