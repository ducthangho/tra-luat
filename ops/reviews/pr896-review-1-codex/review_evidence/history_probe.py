from collections import Counter
import json
from pathlib import Path
import subprocess
import yaml

def git(*a):
    return subprocess.check_output(['git',*a],text=True)

for sha in ('d705623^','d705623','5f288ea','747f983','e63961f','6ac385f'):
    print('HISTORY',git('show','-s','--format=%h %cI %s',sha).strip())
    wf = yaml.safe_load(git('show',f'{sha}:.github/workflows/ci.yml'))
    outputs = wf['jobs'].get('chuan-bi',{}).get('outputs',{})
    if outputs:
        print('chuan-bi.outputs.os:', outputs['os'])
    else:
        print('before chuan-bi matrix:', wf['jobs']['gate']['strategy']['matrix']['os'])
    clause = git('show', f'{sha}:CLAUDE.md').splitlines()
    ix = next((i for i,s in enumerate(clause) if '· **(c)' in s),None)
    if ix is not None:
        print('CLAUDE.md (c) first lines:', '\n'.join(clause[ix:ix+6]))
    print('gate-cong-cu.exclude:',wf['jobs'].get('gate-cong-cu',{}).get('strategy',{}).get('matrix',{}).get('exclude'))

print('three changes: #548 removed master; #878 added dispatch windows-only; #879 reduced Windows G5.')
print('git history for correction #865:')
print(git('show','-s','--format=%H%n%P%n%B','fa362fd').strip())
patch = git('show','4ae43f0','--','ops/land/pr848-wp744-land-evidence.yaml')
print('correction 4ae43f0 relevant lines:')
for line in patch.splitlines():
    if any(s in line for s in ('23/23','4323607674','connector P1')):
        print(line)
old = git('show','3f6c694:ops/land/pr848-wp744-land-evidence.yaml')
print('3f6c694 original assertion:', next(x for x in old.splitlines() if "jobs: '23/23" in x))

p = Path('ops/land/pr848-wp744-provenance')
run = json.loads((p/'readback-run-39354156843.json').read_text())
jobs = json.loads((p/'readback-jobs-39354156843.json').read_text())
print('run 39354156843:',{k:run.get(k) for k in ('id','path','event','head_branch','head_sha','status','conclusion','created_at')})
jj = jobs['jobs']
print('jobs count:',jobs['total_count'],len(jj),'unique ids=',len({j['id'] for j in jj}))
print('labels:',dict(Counter(tuple(j['labels']) for j in jj)))
print('conclusions:',dict(Counter(j['conclusion'] for j in jj)),'runner_id0=',sum(j['runner_id']==0 for j in jj))
assert run['id']==39354156843 and run['event']=='push' and run['head_branch']=='master' and run['head_sha']=='3a3a3caca5de4934ff53851feb6994c2c7b84ad5'
assert jobs['total_count']==len(jj)==len({j['id'] for j in jj})==23
assert all(j['labels']==['ubuntu-latest'] and j['runner_id']>0 and j['conclusion']=='success' for j in jj)

p870 = Path('ops/land/pr870-claude-md-bai-hoc-c-provenance')
for f in sorted(p870.glob('readback-jobs-*.json')):
    data = json.loads(f.read_text())['jobs']
    zero = [j for j in data if j['runner_id']==0]
    print(f.name, 'jobs=',len(data),'runner_id0=',len(zero),'zero steps=',Counter(len(j['steps']) for j in zero),'zero conclusions=',Counter(j['conclusion'] for j in zero))
print('Raw GitHub comment r4323607674/P1 author: KHÔNG ĐO ĐƯỢC; committed correction attributes it, raw comment absent.')
print('PR #109 historical second-P2 claim (unchanged context):')
print(git('log','HEAD','-4','--format=%h %s','--grep=#109').strip())
print('Measurement dates 22/23-10 are author timing declarations; file behavior independently re-evaluated, actual local execution time then not recoverable.')
