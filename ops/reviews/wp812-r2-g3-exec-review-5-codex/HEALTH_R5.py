import importlib.util,json,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path('/tmp/rv812-r5-suite');sys.path.insert(0,str(repo/'.claude/dev'))
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
t=load('health_tests',repo/'.claude/dev/packet_loop_test.py');v=load('health_validator',repo/'ops/bien_nhan_v2.py')
out=Path(tempfile.mkdtemp(prefix='review812-r5-health-'))
def probe(name,path,transform):
 d=out/name;d.mkdir();health={}
 def mutate(w):
  p=w/path;p.write_text(transform(p.read_text()));t._g(w,'add',path);t._g(w,'commit','-qm','ordinary invalid source fixture');t._g(w,'push','-q','origin','master')
  if path!='ops/bien_nhan_v2.py':health['provider_source_error']=load('health_'+name,w/'ops/bien_nhan_v2.py').PROVIDER_NGUON_HONG
 rc,sd,e,before=t._r812(t.Ctx(t.CANONICAL,d),'lease',truoc_lease=mutate)
 raw=(sd/'wp55.json').read_bytes();st=json.loads(raw)
 print(json.dumps(dict(probe=name,rc=rc,state=st['state'],mode=st.get('luat_adr0054'),unchanged=raw==before,traceback=b'Traceback' in e,error=e.decode('utf-8','replace'),**health),ensure_ascii=False),flush=True)
probe('launcher_missing_contract','.claude/dev/launcher.py',lambda s:s.replace('_TRANSPORT_CONTRACTS = (','_TRANSPORT_CONTRACTS_MISSING = (',1))
phrase=next(x[2] for x in v._NEO_LUAT_CHEP_TAY if x[0]=='ASSURANCE_CUA_MO_HINH')
probe('protocol_missing_rule','docs/PROTOCOL_DA_PHIEN.md',lambda s:s.replace(phrase,'ordinary missing rule',1))
probe('receipt_module_missing_api','ops/bien_nhan_v2.py',lambda s:'# ordinary invalid module\n')
probe('receipt_module_syntax','ops/bien_nhan_v2.py',lambda s:'ordinary invalid syntax\n')
print(json.dumps({'scratch':str(out)}),flush=True)
