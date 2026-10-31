from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import yaml

root = Path(__file__).resolve().parents[1] / 'cay-kho'
provenance = root / 'ops/land/pr1041-wp1037-provenance'
land = yaml.safe_load((root / 'ops/land/pr1041-wp1037-land-evidence.yaml').read_text())
def load(name):
    return json.loads((provenance / name).read_text())
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])

for suffix in ['41033737059', '41069257658-a1', '41069257658-a2']:
    run = load('readback-run-' + suffix + '.json')
    jobs = load('readback-jobs-' + suffix + '.json')
    print('RUN', suffix, {k: run[k] for k in ['id', 'run_attempt', 'event', 'head_sha', 'status', 'conclusion', 'path']}, 'REPOSITORY', run['repository']['full_name'])
    print('JOBS', suffix, 'TOTAL', jobs['total_count'], 'LENGTH', len(jobs['jobs']), 'CONCLUSIONS', dict(Counter(j['conclusion'] for j in jobs['jobs'])), 'LABELS', dict(Counter(tuple(j['labels']) for j in jobs['jobs'])))
    print('JOBS_IDENTITY', suffix, 'RUN_IDS', sorted({j['run_id'] for j in jobs['jobs']}), 'HEAD_SHAS', sorted({j['head_sha'] for j in jobs['jobs']}), 'ATTEMPTS', sorted({j['run_attempt'] for j in jobs['jobs']}))
    for job in jobs['jobs']:
        if job['conclusion'] == 'failure':
            print('FAILED_JOB', job['id'], job['name'], 'RUNNER', job['runner_id'], job['labels'], 'FAILED_STEPS', [(s['number'], s['name'], s['conclusion']) for s in job['steps'] if s['conclusion'] == 'failure'])
            print('SHELLCHECK_STEPS', job['id'], [(s['number'], s['name'], s['conclusion']) for s in job['steps'] if 'shellcheck' in s['name']])
        if job['name'] == 'gate-ops (windows-latest)':
            print('WINDOWS_OPS_JOB', job['id'], 'RUNNER', job['runner_id'], job['labels'], 'CONCLUSION', job['conclusion'])
    print('RERUN_METADATA', suffix, {k: v for k, v in run.items() if 'rerun' in k or 'previous_attempt' in k})

pr = load('readback-pr-1041.json')
print('PR', {k: pr.get(k) for k in ['number', 'state', 'merged', 'merged_at', 'merge_commit_sha']}, 'MERGED_BY', pr['merged_by']['login'], 'HEAD', pr['head']['sha'], 'BASE', pr['base']['sha'])
comment = load('readback-comment-6529010520.json')
print('AUTHORIZATION_COMMENT', comment['id'], comment['user']['login'], comment['author_association'], comment['created_at'], 'CONTAINS_FULL_AUTHORIZED_HEAD', land['authorized_head_sha'] in comment['body'], 'BODY', repr(comment['body']))
merge = land['merge_commit']
print('MERGE_GIT', git('show', '-s', '--format=%H%n%T%n%P%n%cI', merge).decode().strip())
print('MERGE_IDENTITY_MATCH', git('rev-parse', merge + '^{tree}').decode().strip() == land['merge_commit_tree'], git('show', '-s', '--format=%P', merge).decode().split() == land['merge_commit_parents'])
before = git('diff', pr['base']['sha'], pr['head']['sha'])
after = git('diff', merge + '^1', merge)
print('DIFF_EQUAL', before == after, 'SHA256', hashlib.sha256(before).hexdigest(), 'NUMSTAT', git('diff', '--numstat', merge + '^1', merge).decode().strip())
runs = load('readback-runs-b29da0b.json')
if isinstance(runs, dict):
    runs = runs['workflow_runs']
print('MASTER_RUNS_COUNT', len(runs))
for run in runs:
    print('MASTER_RUN', {k: run.get(k) for k in ['id', 'run_attempt', 'name', 'event', 'head_sha', 'status', 'conclusion', 'created_at', 'updated_at']})

for check in land['pre_merge_checks'] + land['post_merge_checks']:
    refs = check.get('nguon', [])
    if isinstance(refs, str): refs = [refs]
    for ref in refs:
        path = provenance / ref
        if ref.startswith('../'): path = root / 'ops' / ref.removeprefix('../')
        print('CHECK_SOURCE_EXISTS', check['name'], ref, path.is_file())

for token in ['runner thieu shellcheck', 'cai_cong_cu.sh', '1045', 'runner_set', 'windows-only', 'rerun_failed_jobs', 'rerun-failed-jobs']:
    print('SOURCE_TOKEN', repr(token), 'FILES', [p.relative_to(provenance).as_posix() for p in provenance.rglob('*') if p.is_file() and token in p.read_text()])
a1 = load('readback-jobs-41069257658-a1.json')['jobs']
a2 = load('readback-jobs-41069257658-a2.json')['jobs']
print('RERUN_JOB_ID_INTERSECTION', sorted({j['id'] for j in a1} & {j['id'] for j in a2}))
for j in a2:
    previous = next(x for x in a1 if x['name'] == j['name'])
    if j['name'] == 'chuan-bi' or j['name'] == 'gate-ops (windows-latest)':
        print('RERUN_PREVIOUS_SUCCESS', j['name'], 'A1', previous['id'], previous['conclusion'], previous['started_at'], 'A2', j['id'], j['conclusion'], j['started_at'])
print('CI_PROVENANCE_LIMIT', 'REST run/jobs + merge snapshot; no checkout log, workflow-definition identity readback, or command/rc/N/N job output; no GraphQL403 raw response')
