import importlib.util,json,shutil,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path('/tmp/rv812-r5-suite');sys.path.insert(0,str(repo/'.claude/dev'))
s=importlib.util.spec_from_file_location('own_mutant_tests',repo/'.claude/dev/packet_loop_test.py');t=importlib.util.module_from_spec(s);sys.modules[s.name]=t;s.loader.exec_module(t)
mutations={
 'role':('(\"role\", d.get(\"role\") == \"reviewer\")','(\"role\", True)'),
 'assurance':('(\"assurance\", d.get(\"assurance\") == nc[\"assurance_target\"])','(\"assurance\", True)'),
}
name=sys.argv[1];old,new=mutations[name];source=t.CANONICAL.read_text();assert source.count(old)==1
out=Path(tempfile.mkdtemp(prefix='review812-r5-mut-'+name+'-'));p=out/'packet_loop.py';p.write_text(source.replace(old,new,1));shutil.copyfile(t.HERE/'launcher.py',out/'launcher.py')
names={n for n,_ in t.CASES if n.startswith('r812_')};r=t.chay_suite(p,out/'cases',names)
print(json.dumps({'mutant':name,'total':len(r),'passed':sum(e is None for e in r.values()),'errors':{n:str(e) for n,e in r.items() if e is not None},'scratch':str(out)},ensure_ascii=False),flush=True)
