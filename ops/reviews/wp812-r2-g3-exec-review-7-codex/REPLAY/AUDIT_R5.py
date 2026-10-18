#!/usr/bin/env python3
"""Independent benign input audit. All fixtures and state are disposable."""
import copy, importlib.util, json, sys, tempfile
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path('/tmp/rv812-r7-suite');sys.path.insert(0,str(repo/'.claude/dev'))
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
t=load('r5_tests',repo/'.claude/dev/packet_loop_test.py');v=load('r5_receipt',repo/'ops/bien_nhan_v2.py')
import yaml
out=Path(tempfile.mkdtemp(prefix='review812-r5-own-'))
def report(name,rc,sd,e,before,**kw):
 raw=(sd/'wp55.json').read_bytes()
 print(json.dumps(dict(probe=name,rc=rc,state=json.loads(raw)['state'],unchanged=raw==before,traceback=b'Traceback' in e,error=e.decode('utf-8','replace'),**kw),ensure_ascii=False),flush=True)
d=out/'receipt';d.mkdir();rc,sd,e,before=t._r812(t.Ctx(t.CANONICAL,d),'review');assert rc==0,e
p=d/'bn.yaml';bn=yaml.safe_load(p.read_bytes());w=d/'kho/w'
assert v._thieu(bn)==[] and v._neo_git(w,p.name,bn)==([],[])
report('positive-H',rc,sd,e,before,thieu=[],neo=[[],[]])
def review(n,b,identity=False):
 (sd/'wp55.json').write_bytes(before);p.write_text(yaml.safe_dump(b))
 rc,_,e=t.run(t.CANONICAL,['record-review','--packet',55,'--provider','codex','--verdict','approve','--reviewed-sha',bn['reviewed_sha'],'--codex-call','g1','--bien-nhan',p,'--root',w],sd)
 report(n,rc,sd,e,before,thieu=v._thieu(b),neo=v._neo_git(w,p.name,b))
for key in ('che_do','KHONG_do_duoc','phien_doc_lap'):
 for value in ([],{},'false' if key=='phien_doc_lap' else False):
  b=copy.deepcopy(bn);b['model_reviewer_identity'][key]=value
  review('reviewer-'+key+'-'+type(value).__name__,b)
b=copy.deepcopy(bn);b['model_reviewer_identity'].update(phien_doc_lap=True,KHONG_do_duoc='ordinary explanation')
review('positive-redundant-attestation',b)
b['model_reviewer_identity']['session_run_id']=[]
review('reviewer-session-run-id-list',b)
for key in ('executor_model_evidence_ref','executor_telemetry_path','executor_nguoi_audit','executor_audit_actor'):
 b=copy.deepcopy(bn);b['model_executor_identity']={'model_family':'claude','model_evidence':'do_may','model_evidence_ref':'r',key:[]}
 review('nested-'+key+'-list',b)
# Nested executor prefix keys are read by canon in addition to unprefixed ones.
b=copy.deepcopy(bn);b['model_executor_identity']={'model_family':'claude','model_evidence':'do_may','executor_model_evidence_ref':'r'}
review('positive-prefixed-reference',b)
b=copy.deepcopy(bn);b['model_reviewer_identity']['provider']=' openai_codex '
review('canonical-padded-provider',b)
b=copy.deepcopy(bn);b['model_reviewer_identity']['surface']=' codex_cli '
review('canonical-padded-surface',b)
b=copy.deepcopy(bn);b['model_reviewer_identity']['transport']=' machine '
review('canonical-padded-transport',b)
# Canonical surface alias is an ordinary supported identity spelling.
b=copy.deepcopy(bn);b['model_executor_identity']={'surface':'claude_code_cli','transport':'machine/local'}
review('canonical-surface-alias',b)
def lease(n,mut=None,bien=''):
 dd=out/n;dd.mkdir();rc,ss,ee,bb=t._r812(t.Ctx(t.CANONICAL,dd),'lease',bien=bien,truoc_lease=mut);report(n,rc,ss,ee,bb)
lease('positive-lease')
lease('canon-content-invalid',bien='thieu_nguon')
# Prefix receipt reference shape is tested against a full valid tuple above.
print(json.dumps({'scratch':str(out)}),flush=True)
