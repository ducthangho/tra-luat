import importlib.util,json,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path('/tmp/rv812-r7-suite');sys.path.insert(0,str(repo/'.claude/dev'))
s=importlib.util.spec_from_file_location('r7_lease_identity_t',repo/'.claude/dev/packet_loop_test.py');t=importlib.util.module_from_spec(s);sys.modules[s.name]=t;s.loader.exec_module(t)
out=Path(tempfile.mkdtemp(prefix='rv812-r7-lease-identity-'))
for name,change in [('positive',None),('padded-executor',{'provider':' claude ','executor':' claude '}),('padded-reviewer',{'reviewer':' codex '}),('padded-alias-executor',{'provider':' anthropic_claude ','executor':' anthropic_claude '}),('padded-alias-reviewer',{'reviewer':' openai_codex '})]:
 d=out/name;d.mkdir();rc,sd,e,b=t._r812(t.Ctx(t.CANONICAL,d),'lease',truoc_lease=(lambda w:t._r812_doi_lease(w,change)) if change else None)
 print(json.dumps({'probe':name,'rc':rc,'unchanged':(sd/'wp55.json').read_bytes()==b,'error':e.decode('utf-8','replace')},ensure_ascii=False),flush=True)
print(json.dumps({'scratch':str(out)}),flush=True)
