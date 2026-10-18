import importlib.util,json,shutil,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path('/tmp/rv812-r7-suite');sys.path.insert(0,str(repo/'.claude/dev'))
s=importlib.util.spec_from_file_location('r7_mutants_t',repo/'.claude/dev/packet_loop_test.py');t=importlib.util.module_from_spec(s);sys.modules[s.name]=t;s.loader.exec_module(t)
mutants={
'lease_packet': (' or l["packet_issue"] != st["packet"]',''),
'lease_paths_exclusive': ('if any(moi) == any(cu) or not all(moi if any(moi) else cu):','if not all(moi if any(moi) else cu):'),
'lease_instruction_packet': (' or mr[2].lstrip("0") != str(st["packet"])',''),
'lease_identity_matches_init': ('if any(v is not None and nc[vai][k] != v for k, v in (st.get(f"{vai}_identity") or {}).items()):','if False:'),
'activation_adr_name': (' and "ADR-0054" in nfc(a55[1])',''),
}
name=sys.argv[1];old,new=mutants[name];source=t.CANONICAL.read_text();assert source.count(old)==1,(name,source.count(old))
out=Path(tempfile.mkdtemp(prefix='rv812-r7-mut-'+name+'-'));p=out/'packet_loop.py';p.write_text(source.replace(old,new,1));shutil.copyfile(t.HERE/'launcher.py',out/'launcher.py')
names={n for n,_ in t.CASES if n.startswith('r812_')};r=t.chay_suite(p,out/'cases',names)
print(json.dumps({'mutant':name,'total':len(r),'passed':sum(v is None for v in r.values()),'errors':{n:str(v) for n,v in r.items() if v is not None},'scratch':str(out)},ensure_ascii=False),flush=True)
