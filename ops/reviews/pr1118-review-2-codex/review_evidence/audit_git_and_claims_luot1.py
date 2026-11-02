import base64
import collections
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
REPO = ROOT / 'cay-kho'
PROV = REPO / 'ops/land/pr1065-vm-cap-nhat-cong-cu-provenance'
RAW = ROOT / 'raw-rest'


def git(*args):
    return subprocess.run(['git', '-C', str(REPO), *args], check=True, capture_output=True).stdout


def read(path):
    return json.loads(path.read_text())


print('HEAD/tree', git('rev-parse', 'HEAD', 'HEAD^{tree}').decode().strip())
print('merge-base', git('merge-base', 'HEAD', 'origin/master').decode().strip())
print('core.abbrev', git('config', '--get', 'core.abbrev').decode().strip())
print('diff.patch exact match', git('diff', '3bdd987', 'HEAD') == (ROOT / 'diff.patch').read_bytes())
print('numstat exact match', git('diff', '--numstat', '3bdd987', 'HEAD') == (ROOT / 'numstat.txt').read_bytes())
c = read(RAW / 'commit-4397ee6.json')
assert git('rev-parse', '4397ee6^{tree}').decode().strip() == c['commit']['tree']['sha']
assert git('show', '-s', '--format=%P', '4397ee6').decode().split() == [x['sha'] for x in c['parents']]
numstat = git('diff', '--numstat', '4397ee6^1', '4397ee6').decode().splitlines()
assert [(line.split('\t')[2], int(line.split('\t')[0]), int(line.split('\t')[1])) for line in numstat] == [
    (x['filename'], x['additions'], x['deletions']) for x in c['files']]
print('merge4397ee6 git matches raw parents/tree/files:', c['commit']['tree']['sha'])
print('\nFIRST-PARENT')
print(git('log', '--first-parent', '--reverse', '--format=%H %P %s', '4397ee6..3bdd987').decode().strip())
for commit in ('165b27a', '2cea625', '3bdd987'):
    print('DELTA', commit)
    print(git('diff', '--numstat', commit + '^1', commit).decode().strip())
print('protected paths delta', repr(git('diff', '--name-status', '4397ee6', '3bdd987', '--',
      'ops/vm/', 'ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml').decode()))
for a, b in [('4397ee6', '3bdd987'), ('3bdd987', '180039c'), ('cb39aca', '40609d4')]:
    p = subprocess.run(['git', '-C', str(REPO), 'merge-base', '--is-ancestor', a, b])
    print('ancestor', a, b, 'exit_code', p.returncode)

print('\nCOMMENTS')
comment = next(x for x in read(RAW / 'comments-1111.json') if x['id'] == 6555093642)
head = read(RAW / 'pull-1111.json')['head']['sha']
assert head in comment['body']
print('comment', comment['id'], 'created_at', comment['created_at'], 'head', head)
print('head commit time', git('show', '-s', '--format=%cI', head).decode().strip())
print('merged_at', read(RAW / 'pull-1111.json')['merged_at'])

print('\nMASTER RUN TIMELINE (raw list includes all 4 run IDs)')
runs = read(RAW / 'runs-master-push.json')['workflow_runs']
for x in sorted([x for x in runs if x['id'] in (41285898441, 41287486328, 41289716885, 41290009265)], key=lambda x: x['created_at']):
    print(x['id'], x['head_sha'], x['path'], x['event'], x['status'], x['conclusion'], x['created_at'], x['updated_at'])
print('workflow concurrency at 4397ee6:')
workflow = git('show', '4397ee6:.github/workflows/ci.yml').decode()
start = workflow.index('concurrency:')
print(workflow[start:workflow.index('\njobs:', start)].strip())

print('\nSOURCE TIME ANOMALY (not an inferred cause)')
run = read(RAW / 'run-41290009265.json')
jobs = read(RAW / 'jobs-41290009265.json')['jobs']
print('run created_at/run_started_at', run['created_at'], run['run_started_at'])
print('jobs started before run.created_at', sum(x['started_at'] < run['created_at'] for x in jobs), '/', len(jobs))
print('jobs completed before run.created_at', sum(x['completed_at'] < run['created_at'] for x in jobs), '/', len(jobs))
print('earliest job started_at', min(x['started_at'] for x in jobs))
print('all raw job run_id correct', all(x['run_id'] == run['id'] for x in jobs))
print('all raw job attempts match', all(x['run_attempt'] == run['run_attempt'] for x in jobs))
print('job step conclusions', dict(collections.Counter(s['conclusion'] for x in jobs for s in x['steps'])))

print('\nVM STATIC HASHES (installed bytes not available)')
for path in ['ops/vm/cap-nhat-cong-cu.ps1', 'ops/cong_cu.yaml', 'requirements.txt']:
    data = git('show', 'cb39aca:' + path)
    print('cb39aca:' + path, hashlib.sha256(data).hexdigest(), 'same at merge1091', data == git('show', '40609d4:' + path))
print('script Sunday 02:30/2 weeks:', next(line.strip() for line in git('show', 'cb39aca:ops/vm/cap-nhat-cong-cu.ps1').decode().splitlines() if '$tHT = New-ScheduledTaskTrigger' in line))

print('\nEXISTING FOUR ANCHORS (41173244891 only)')
contents = read(PROV / 'readback-contents-ci-yml-3dfb973.json')
data = base64.b64decode(contents['content'])
print('workflow blob', contents['sha'], 'git', git('rev-parse', '3dfb973:.github/workflows/ci.yml').decode().strip())
print('workflow bytes exact match', data == git('show', '3dfb973:.github/workflows/ci.yml'), 'SHA256', hashlib.sha256(data).hexdigest())
jobs = read(PROV / 'readback-jobs-41173244891.json')['jobs']
print('old jobs', len(jobs), 'success', sum(x['conclusion'] == 'success' for x in jobs),
      'steps', dict(collections.Counter(s['conclusion'] for x in jobs for s in x['steps'])))
text = (PROV / 'gate-output-41173244891.txt').read_text()
print('old extracted logs', sum(line.startswith('== job ') for line in text.splitlines()),
      'checkout SHA occurrences', sum(line.strip() == "checkout: ['3dfb9731ceda05afbcec4e803a919c4df5e2e5a2']" for line in text.splitlines()),
      'Run steps', sum(line.strip().startswith('- Run:') for line in text.splitlines()))
print('new run files present', [p.name for p in sorted(PROV.glob('*41290009265*'))])
print('new run GraphQL/log/checkout artifacts: none among changed files or provenance filenames; REST metadata only')
