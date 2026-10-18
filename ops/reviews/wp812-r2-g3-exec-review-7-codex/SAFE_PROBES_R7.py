import copy,importlib.util,json,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path('/tmp/rv812-r7-suite');sys.path.insert(0,str(repo/'.claude/dev'))
s=importlib.util.spec_from_file_location('r7_safe_t',repo/'.claude/dev/packet_loop_test.py');t=importlib.util.module_from_spec(s);sys.modules[s.name]=t;s.loader.exec_module(t)
out=Path(tempfile.mkdtemp(prefix='rv812-r7-safe-'));d=out/'comments';d.mkdir()
rc,sd,e,before=t._r812(t.Ctx(t.CANONICAL,d),'lease');assert rc==0,e
p=d/'cm.json';cm=json.loads(p.read_text());w=d/'kho/w'
def lease(name,comment,extra=()):
 (sd/'wp55.json').write_bytes(before);p.write_text(json.dumps(comment))
 rc,_,e=t.run(t.CANONICAL,['record-lease','--packet',55,'--lease-ref','origin/ops/wp55-spec','--lease-path','ops/leases/l.yaml','--lease-comments',p,'--root',w,*extra],sd)
 print(json.dumps({'probe':name,'rc':rc,'unchanged':(sd/'wp55.json').read_bytes()==before,'traceback':b'Traceback' in e,'error':e.decode('utf-8','replace')},ensure_ascii=False),flush=True)
lease('positive-comment',cm)
for url in ('https://example.org/repos/o/r/issues/55','ordinary/o/r/issues/55','https://api.github.com/repos/different/o/r/issues/55'):
 x=copy.deepcopy(cm);x[0]['issue_url']=url;lease('comment-url-'+url,x)
lease('mixed-paths-complete',cm,('--lease-id','legacy','--granted-by','ducthangho','--evidence','ordinary authority','--expires-utc','2026-10-19T10:00:00Z'))
lease('mixed-paths-empty-old-option',cm,('--lease-id',''))
print(json.dumps({'scratch':str(out)}),flush=True)
