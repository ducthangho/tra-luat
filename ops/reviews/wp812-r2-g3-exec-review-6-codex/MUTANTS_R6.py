import importlib.util,sys,tempfile,json,shutil,concurrent.futures
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path('/tmp/wp812-r6-suite');sys.path.insert(0,str(repo/'.claude/dev'))
s=importlib.util.spec_from_file_location('r6_mutants_t',repo/'.claude/dev/packet_loop_test.py');t=importlib.util.module_from_spec(s);sys.modules[s.name]=t;s.loader.exec_module(t)
source=t.CANONICAL.read_text();out=Path(tempfile.mkdtemp(prefix='wp812-r6-mutants-'));names={n for n,_ in t.CASES if n.startswith('r812_')}
mutants={
'family_executor':('("ho-executor", bool(ho_exec) and ho_exec == ho("executor"))','("ho-executor", True)'),
'family_reviewer':('("ho-reviewer", bool(ho_rev) and ho_rev == ho("reviewer"))','("ho-reviewer", True)'),
'activation_protocol':('and pr[0] == 0 and len(dong20) == 1 and "chưa kích hoạt" not in dong20[0].casefold()', 'and True'),
'workflow_author':('c["user"].get("login") == BOT_LEASE','True'),
'workflow_issue':('str(c.get("issue_url", "")).endswith(f"/{mr[1]}/issues/{st[\'packet\']}")','True'),
'workflow_lease_id':('re.search(rf"^lease_id: {re.escape(lid)}$", str(c.get("body", "")), re.M)','True'),
}
# Avoid the shared template cache in concurrent threads: distinct processes below.
if len(sys.argv)>1:
 name=sys.argv[1];a,b=mutants[name];assert source.count(a)==1,(name,source.count(a));d=out/name;d.mkdir();p=d/'packet_loop.py';p.write_text(source.replace(a,b,1));shutil.copyfile(t.HERE/'launcher.py',d/'launcher.py');r=t.chay_suite(p,d/'cases',names);print(json.dumps(dict(mutant=name,total=len(r),passed=sum(v is None for v in r.values()),errors={n:v for n,v in r.items() if v is not None},scratch=str(out)),ensure_ascii=False),flush=True)
else:
 import subprocess
 dest=Path.cwd()/'OWN_MUTANTS';dest.mkdir(exist_ok=True)
 def one(name):
  with (dest/(name+'.jsonl')).open('wb') as o,(dest/(name+'.stderr')).open('wb') as e:
   p=subprocess.run([sys.executable,__file__,name],stdout=o,stderr=e)
  return {'name':name,'rc':p.returncode}
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
  for r in ex.map(one,mutants):print(json.dumps(r),flush=True)
