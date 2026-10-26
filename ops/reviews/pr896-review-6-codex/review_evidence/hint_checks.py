from pathlib import Path
import concurrent.futures,json,os,subprocess,yaml,hashlib,ast
from audit import ROOT,OUT,SHA,record
copy=Path((OUT/'copy-path.txt').read_text());dest=OUT/'hint-validation';dest.mkdir(exist_ok=True)
commands={'t26':['python3','ops/lease_publish_test.py','--chi-ca=t26_'],'t27':['python3','ops/lease_publish_test.py','--chi-ca=t27_'],'t138':['python3','ops/lease_publish_test.py','--chi-ca=t138_'],'bien_nhan_v2':['python3','ops/bien_nhan_v2.py','--root','.'],'land':['python3','ops/land_evidence_nguon.py','--root','.'],'doctrine':['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'],'doc_claims':['python3','scripts/tl.py','doc-claims-check','--json']}
def run(item):
 k,cmd=item;p=subprocess.run(cmd,cwd=copy,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 (dest/(k+'.stdout')).write_text(p.stdout);(dest/(k+'.stderr')).write_text(p.stderr)
 return k,{'rc':p.returncode,'summary':json.loads(p.stdout).get('ok') if k=='doc_claims' else '\n'.join(p.stdout.strip().splitlines()[-2:])}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=dict(pool.map(run,commands.items()))
(dest/'checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(json.dumps(results,ensure_ascii=False,indent=2))
errors=[]
from audit import UniqueLoader
for name in json.loads((OUT/'hint-paths.json').read_text()):
 if name.endswith('.yaml'):
  d=yaml.load((copy/name).read_text(),Loader=UniqueLoader);ids=[c['id'] for c in d.get('verdict_usage_caveats',[])];assert len(ids)==len(set(ids))
for p in (ROOT/'ops/reviews').glob('*.receipt.yaml'):
 d=yaml.safe_load(p.read_text());vp=d['verdict_path'];assert (ROOT/vp).read_bytes()==(copy/vp).read_bytes()
 if d['schema_version']==1:assert p.read_bytes()==(copy/p.relative_to(ROOT)).read_bytes()
for d in json.loads((OUT/'land-surfaces.json').read_text()):assert hashlib.sha256((copy/d['verdict']).read_bytes()).hexdigest()==d['sha256']
record(13,'Kiểm lại hint bằng ca có sẵn và bảo toàn byte','python3 review_evidence/hint_checks.py',json.dumps(results,ensure_ascii=False,indent=2)+'\nUnique-key YAML parse passed; caveat IDs unique; all review verdict bytes and all v1 receipt bytes unchanged; three land verdict hashes unchanged.','KHÔNG PHẢI LỖI của hint; kết quả chỉ trên clone')
