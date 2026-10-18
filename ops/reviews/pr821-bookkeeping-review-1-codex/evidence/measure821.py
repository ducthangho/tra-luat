from pathlib import Path
import json,subprocess,collections
r=Path('/home/user/rv773');p=r/'ops/land/pr779-wp775-provenance'
load=lambda n:json.loads((p/n).read_text())
for f in p.glob('readback-run-*.json'):
 x=load(f.name);print(f.name,{k:x.get(k) for k in ['id','head_sha','conclusion','run_attempt','created_at','updated_at','run_started_at','check_suite_id']})
for f in p.glob('readback-jobs*.json'):
 x=load(f.name);print(f.name,x['total_count'],[(j['name'],j['conclusion'],j.get('started_at'),j.get('completed_at')) for j in x['jobs']])
x=load('readback-check-runs-f9d84d7.json')['check_runs']
for suite in [105821166384,105821159612]:
 names=sorted(set(j['name'] for j in x if j['check_suite']['id']==suite));print('SUITE',suite,names)
 cmd=['python3.13','-B',str(r/'.claude/dev/packet_loop.py'),'kiem-gate','--head','f9d84d70fb46540bbecfae963c9afb4a2b48984d','--check-runs',str(p/'readback-check-runs-f9d84d7.json'),'--check-suite',str(suite)]
 for n in names:cmd+=['--bat-buoc',n]
 z=subprocess.run(cmd,capture_output=True,text=True);print(z.stdout,'rc=',z.returncode)
for f in ['readback-pr-779.json','readback-codex-connector-receipt-6236575036.json','readback-codex-connector-state-779.json']:
 x=load(f);print(f)
 if f=='readback-pr-779.json':print('keys',list(x));print({k:x.get(k) for k in ['merged','merged_at','merged_by','merge_commit_sha','mergeable','mergeable_state']});print('head',x['head']['sha'])
 else:print(json.dumps(x,ensure_ascii=False))
listed=[s.split(None,1)[1].removeprefix('./') for s in (p/'SHA256SUMS').read_text().splitlines()];actual={str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and f.name!='SHA256SUMS'}
print('SETS',len(listed),len(actual),'missing',actual-set(listed),'extra',set(listed)-actual,'duplicates',len(listed)-len(set(listed)))
for i in [775,*range(804,811)]:
 x=load(f'readback-issue-{i}.json');print(i, {k:x.get(k) for k in ['state','state_reason','closed_at','title']})
