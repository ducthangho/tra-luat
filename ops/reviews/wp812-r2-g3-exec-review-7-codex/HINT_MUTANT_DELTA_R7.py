import importlib.util,json,shutil,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path('/tmp/rv812-r7-hint');sys.path.insert(0,str(repo/'.claude/dev'))
s=importlib.util.spec_from_file_location('r7_mutant_delta_t',repo/'.claude/dev/packet_loop_test.py');t=importlib.util.module_from_spec(s);sys.modules[s.name]=t;s.loader.exec_module(t)
out=Path(tempfile.mkdtemp(prefix='rv812-r7-mutant-delta-'));source=t.CANONICAL.read_text()
for n in ('r812_r5_raw_provider','r812_r7_lease_raw_provider'):
 old,new,targets=t.MUTANTS[n];d=out/n;d.mkdir();ss=source
 r=t.chay_suite(t.CANONICAL,d/'baseline',set(targets));print(json.dumps({'baseline_for':n,'results':r},ensure_ascii=False),flush=True)
 for a,b in t._cap_thay_the(old,new):assert ss.count(a)==1,(n,a);ss=ss.replace(a,b,1)
 p=d/'packet_loop.py';p.write_text(ss);shutil.copyfile(t.HERE/'launcher.py',d/'launcher.py')
 print(json.dumps({'mutant':n,'results':t.chay_suite(p,d/'cases',set(targets))},ensure_ascii=False),flush=True)
