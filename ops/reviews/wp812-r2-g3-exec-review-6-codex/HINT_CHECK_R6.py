from pathlib import Path
import importlib.util,json,sys,tempfile,shutil
sys.dont_write_bytecode=True
repo=Path('/tmp/wp812-r6-hint');sys.path.insert(0,str(repo/'.claude/dev'))
s=importlib.util.spec_from_file_location('r6_hint_tests',repo/'.claude/dev/packet_loop_test.py');t=importlib.util.module_from_spec(s);sys.modules[s.name]=t;s.loader.exec_module(t)
root=Path(tempfile.mkdtemp(prefix='wp812-r6-hint-check-'));source=t.CANONICAL.read_text()
names={n for n,_ in t.CASES if n.startswith('r812_')}
r=t.chay_suite(t.CANONICAL,root/'baseline',names)
print(json.dumps(dict(step='hint_baseline',total=len(r),passed=sum(e is None for e in r.values()),errors={n:e for n,e in r.items() if e is not None}),ensure_ascii=False),flush=True)
new={n for n in names if n.startswith('r812_r6_')}
r=t.chay_suite(Path('/tmp/wp812-r6-suite/.claude/dev/packet_loop.py'),root/'exact_head_new_tests',new)
print(json.dumps(dict(step='exact_head_new_tests',total=len(r),passed=sum(e is None for e in r.values()),errors={n:e for n,e in r.items() if e is not None}),ensure_ascii=False),flush=True)
for name,(a,b,targets) in t.MUTANTS.items():
 if not name.startswith('r812_'):continue
 mutated=source
 for old,replacement in t._cap_thay_the(a,b):
  assert old in mutated,(name,old);mutated=mutated.replace(old,replacement,1)
 d=root/name;d.mkdir();p=d/'packet_loop.py';p.write_text(mutated);shutil.copyfile(t.HERE/'launcher.py',d/'launcher.py')
 r=t.chay_suite(p,d/'cases',set(targets))
 print(json.dumps(dict(step='hint_mutant',mutant=name,targets=r),ensure_ascii=False),flush=True)
print(json.dumps(dict(scratch=str(root))),flush=True)
