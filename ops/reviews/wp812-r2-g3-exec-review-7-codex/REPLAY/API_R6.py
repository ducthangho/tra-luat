from pathlib import Path
import sys,importlib.util,json,tempfile
sys.dont_write_bytecode=True
repo=Path('/tmp/rv812-r7-suite');sys.path.insert(0,str(repo/'.claude/dev'))
s=importlib.util.spec_from_file_location('r6_api_t',repo/'.claude/dev/packet_loop_test.py');t=importlib.util.module_from_spec(s);sys.modules[s.name]=t;s.loader.exec_module(t)
out=Path(tempfile.mkdtemp(prefix='wp812-r6-api-'))
# Full CLI, only a present-but-unusable canonical API is changed.
for key in ('ASSURANCE_CAN_DOC_LAP','HO_MODEL_CHO_PHEP','_thieu','_neo_git','_nguon_tra_model','_giai_ho_model_reviewer','_giai_ho_model_executor','_chuoi','_chuan_hoa_provider'):
 for door in ('lease','review'):
  d=out/(door+'-'+key);d.mkdir();c=t.Ctx(t.CANONICAL,d)
  def change(w):
   p=w/'ops/bien_nhan_v2.py';p.write_text(p.read_text()+'\n'+key+' = None\n');t._g(w,'add','ops/bien_nhan_v2.py');t._g(w,'commit','-qm','ordinary incompatible API');t._g(w,'push','-q','origin','master');t._g(w,'fetch','-q','origin')
  if door=='lease':rc,sd,e,before=t._r812(c,'lease',truoc_lease=change)
  else:
   rc,sd,e,before=t._r812(c,'review');assert rc==0,e
   (sd/'wp55.json').write_bytes(before);w=d/'kho/w';change(w)
   rc,_,e=t.run(t.CANONICAL,['record-review','--packet',55,'--provider','codex','--verdict','approve','--reviewed-sha',json.loads(before)['reviewing_head_sha'],'--codex-call','g1','--bien-nhan',d/'bn.yaml','--root',w],sd)
  raw=(sd/'wp55.json').read_bytes();print(json.dumps(dict(api=key,door=door,rc=rc,unchanged=raw==before,traceback=b'Traceback' in e,error=e.decode('utf-8','replace')),ensure_ascii=False),flush=True)
print(json.dumps({'scratch':str(out)}),flush=True)
