import importlib.util,json,shutil,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path('/tmp/rv812-r5-hint-final');sys.path.insert(0,str(repo/'.claude/dev'))
s=importlib.util.spec_from_file_location('hint_delta_tests',repo/'.claude/dev/packet_loop_test.py');t=importlib.util.module_from_spec(s);sys.modules[s.name]=t;s.loader.exec_module(t)
out=Path(tempfile.mkdtemp(prefix='review812-r5-hint-delta-'));names={'r812_r5_review_role','r812_r5_review_assurance'}
for label,script in [('exact_head',Path('/tmp/rv812-r5-suite/.claude/dev/packet_loop.py')),('hint',t.CANONICAL)]:
 r=t.chay_suite(script,out/label,names);print(json.dumps({'baseline':label,'targets':r},ensure_ascii=False),flush=True)
for name in ['r812_r4_bo_dep_vang','r812_r5_drop_role','r812_r5_drop_assurance']:
 a,b,targets=t.MUTANTS[name];src=t.CANONICAL.read_text();d=out/name;d.mkdir()
 for old,new in t._cap_thay_the(a,b):
  assert old in src,(name,old);src=src.replace(old,new,1)
 p=d/'packet_loop.py';p.write_text(src);shutil.copyfile(t.HERE/'launcher.py',d/'launcher.py')
 r=t.chay_suite(p,d/'cases',set(targets));print(json.dumps({'mutant':name,'targets':r},ensure_ascii=False),flush=True)
print(json.dumps({'scratch':str(out)}),flush=True)
