from pathlib import Path
import sys,importlib.util,json,tempfile,copy
sys.dont_write_bytecode=True
repo=Path('/tmp/wp812-r6-suite');sys.path.insert(0,str(repo/'.claude/dev'))
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
t=load('r6_t',repo/'.claude/dev/packet_loop_test.py');v=load('r6_v',repo/'ops/bien_nhan_v2.py');import yaml
out=Path(tempfile.mkdtemp(prefix='wp812-r6-own-'));d=out/'review';d.mkdir();rc,sd,e,before=t._r812(t.Ctx(t.CANONICAL,d),'review');assert rc==0,e
p=d/'bn.yaml';bn=yaml.safe_load(p.read_bytes());w=d/'kho/w'
def report(name,rc,sd,e,before):
 raw=(sd/'wp55.json').read_bytes();print(json.dumps(dict(probe=name,rc=rc,state=json.loads(raw)['state'],unchanged=raw==before,traceback=b'Traceback' in e,error=e.decode('utf-8','replace')),ensure_ascii=False),flush=True)
report('positive-real-H',rc,sd,e,before)
for name,path,value in [('evidence_path_nul',['evidence_url'],bn['evidence_url']+'\x00'),('evidence_sha_nul',['evidence_url'],bn['evidence_url'].replace('/blob/','/blob/\x00')),('verdict_path_nul',['verdict_path'],'ops/reviews/v.md\x00'),('executor_top_surface',['executor_surface'],'antigravity'),('executor_top_transport',['executor_transport'],'human'),('assurance_dat_list',['assurance_dat'],[])]:
 b=copy.deepcopy(bn);b[path[0]]=value
 (sd/'wp55.json').write_bytes(before);p.write_text(yaml.safe_dump(b))
 rc,_,e=t.run(t.CANONICAL,['record-review','--packet',55,'--provider','codex','--verdict','approve','--reviewed-sha',bn['reviewed_sha'],'--codex-call','g1','--bien-nhan',p,'--root',w],sd);report(name,rc,sd,e,before)
# Make both anchor path declarations agree before varying their path syntax.
b=copy.deepcopy(bn);b['verdict_path']+='\x00';b['evidence_url']+='\x00'
(sd/'wp55.json').write_bytes(before);p.write_text(yaml.safe_dump(b))
rc,_,e=t.run(t.CANONICAL,['record-review','--packet',55,'--provider','codex','--verdict','approve','--reviewed-sha',bn['reviewed_sha'],'--codex-call','g1','--bien-nhan',p,'--root',w],sd);report('both-verdict-paths-nul',rc,sd,e,before)
for name,mut in [('write_set_nul',{'write_set':['x/a.py\x00']}),('effective_write_set_nul',{'effective_write_set':['x/a.py\x00']}),('lease_id_nul',{'lease_id':'wp55-r1-g1-claude\x00'}),('prompt_nul',{'prompt_path':'ops/specs/wp55-prompt.md\x00'}),('provider_falsy',{'provider':[]}),('executor_falsy',{'executor':[]}),('reviewer_falsy',{'reviewer':[]})]:
 dd=out/name;dd.mkdir();rc,ss,ee,bb=t._r812(t.Ctx(t.CANONICAL,dd),'lease',truoc_lease=lambda w:t._r812_doi_lease(w,mut));report(name,rc,ss,ee,bb)
print(json.dumps({'scratch':str(out)}),flush=True)
