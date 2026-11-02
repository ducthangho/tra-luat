import json,collections,subprocess,hashlib,yaml,re
from pathlib import Path
repo=Path('cay-kho');p=repo/'ops/land/pr1041-wp1037-provenance'
head='91466322f705658ed51b80c7c152f6b77f4f90c6';merge='b29da0bfe3bfb7a7be69136a1c5c40f82c088a93'
def git(*a):return subprocess.check_output(['git','-C',str(repo),*a])
for stem in ['41033737059','41069257658-a1','41069257658-a2']:
 r=json.loads((p/f'readback-run-{stem}.json').read_bytes());jobs=json.loads((p/f'readback-jobs-{stem}.json').read_bytes()); js=jobs['jobs']
 print('RUN',stem,'id',r['id'],'attempt',r['run_attempt'],'event',r['event'],'path',r['path'],'head_sha',r['head_sha'],'status',r['status'],'conclusion',r['conclusion'],'updated_at',r['updated_at'])
 print('JOBS',stem,'total_count',jobs['total_count'],'array_size',len(js),'conclusions',dict(collections.Counter(j['conclusion'] for j in js)),'head_sha_all_match',all(j['head_sha']==head for j in js),'run_attempts',sorted(set(j['run_attempt'] for j in js)))
 print('RUNNER_LABELS',stem,dict(collections.Counter(tuple(j['labels']) for j in js)))
 for j in js:
  if j['conclusion']!='success' or 'gate-ops' in j['name']:
   print('JOB',j['id'],j['name'],'conclusion',j['conclusion'],'labels',j['labels'],'runner_id',j['runner_id'],'started_at',j['started_at'],'completed_at',j['completed_at'])
  if j['conclusion']=='failure':
   print('FAILED_STEPS',[(s['number'],s['name'],s['conclusion']) for s in j['steps'] if s['conclusion']=='failure'])
   print('SHELLCHECK_STEPS',[(s['number'],s['name'],s['conclusion']) for s in j['steps'] if 'shellcheck' in s['name']])
  if 'gate-ops' in j['name']:
   print('GATE_OPS_STEPS',[(s['name'],s['conclusion']) for s in j['steps'] if any(x in s['name'].lower() for x in ['bien','lease','nhận','nhan'])])
for needle in ['runner thieu shellcheck','cai_cong_cu.sh','1045','255/255','runner_set','windows-only']:
 print('SOURCE_TOKEN',repr(needle),'FILES',[f.name for f in p.iterdir() if f.is_file() and needle in f.read_text()])
runs=json.loads((p/'readback-runs-b29da0b.json').read_text())
r=next(r for r in runs['workflow_runs'] if r['id']==41099184556)
print('POST_MERGE', {k:r.get(k) for k in ['id','run_attempt','event','head_sha','status','conclusion','updated_at']})
pr=json.loads((p/'readback-pr-1041.json').read_text());comment=json.loads((p/'readback-comment-6529010520.json').read_text())
print('PR',pr['number'],pr['merged'],pr['merged_at'],pr['merged_by']['login'],'head',pr['head']['sha'],'base',pr['base']['sha'],'merge',pr['merge_commit_sha'])
print('MERGE_OBJECT',git('show','-s','--format=%H %T %P',merge).decode().strip())
print('HEAD_TREE',git('rev-parse',head+'^{tree}').decode().strip())
for a,b in [(pr['base']['sha'],head),(merge+'^1',merge)]:
 patch=git('diff',a,b);print('DIFF',a,b,'sha256',hashlib.sha256(patch).hexdigest(),'numstat',git('diff','--numstat',a,b).decode().strip())
print('OWNER_COMMENT',comment['id'],comment['user']['login'],comment['author_association'],comment['created_at'],'contains_authorized_head',head in comment['body'] or head[:7] in comment['body'])
print('PARENTS2_EQUALS_REVIEWED',git('rev-parse',merge+'^2').decode().strip()==head)
land=yaml.safe_load((repo/'ops/land/pr1041-wp1037-land-evidence.yaml').read_text())
print('LANDED',land['trang_thai_packet']['landed'],'REVIEWER_ASSURANCE_81',land['assurance_81']['reviewer_assurance_81'])
def walk(v,path='$'):
 if isinstance(v,dict):
  for k,x in v.items():yield from walk(x,path+'.'+str(k))
 elif isinstance(v,list):
  for i,x in enumerate(v):yield from walk(x,path+f'[{i}]')
 elif isinstance(v,str) and re.match(r'^measured\b',v,re.I):yield path,v
for path,s in walk(land):print('MEASURED_CLAIM',path,s)
