from collections import Counter
import hashlib
import json
import subprocess

SHA = '06a50c5feea77c2654f31edd26efeed7eeee62f5'
prefix = 'ops/land/pr848-wp744-provenance/'
def show(path, sha=SHA):
    return subprocess.check_output(['git', 'show', f'{sha}:{path}'])

raw = show(prefix + 'readback-jobs-39354156843.json')
data = json.loads(raw)
jobs = data['jobs']
print('total_count=', data['total_count'], 'len(jobs)=', len(jobs))
print('labels=', dict(Counter(tuple(j['labels']) for j in jobs)))
print('conclusions=', dict(Counter(j['conclusion'] for j in jobs)))
print('run_ids=', sorted({j['run_id'] for j in jobs}))
print('head_shas=', sorted({j['head_sha'] for j in jobs}))
print('Windows_jobs=', sum(any('windows' in x.lower() for x in j['labels']) for j in jobs))
print('started_dates=', sorted({j['started_at'][:10] for j in jobs}))
print('unique_job_ids=', len({j['id'] for j in jobs}))
print('positive_runner_ids=', sum(j.get('runner_id', 0) > 0 for j in jobs))
assert len({j['id'] for j in jobs}) == 23
assert all(j.get('runner_id', 0) > 0 and j['head_sha'] == '3a3a3caca5de4934ff53851feb6994c2c7b84ad5' for j in jobs)
assert data['total_count'] == len(jobs) == 23
assert all(j['labels'] == ['ubuntu-latest'] and j['run_id'] == 39354156843 and j['conclusion'] == 'success' for j in jobs)
manifest = show(prefix + 'SHA256SUMS').decode()
for filename in ('readback-jobs-39354156843.json', 'readback-run-39354156843.json'):
    digest = hashlib.sha256(show(prefix + filename)).hexdigest()
    assert f'{digest}  ./{filename}' in manifest
    print(f'SHA256SUMS {filename}: PASS {digest}')
    print(f'same bytes at 3f6c694 {filename}: {show(prefix + filename, "3f6c694") == show(prefix + filename)}')
    assert show(prefix + filename, '3f6c694') == show(prefix + filename)
run = json.loads(show(prefix + 'readback-run-39354156843.json'))
print('run=', json.dumps({k: run[k] for k in ('id', 'path', 'event', 'head_branch', 'head_sha', 'created_at', 'conclusion')}, ensure_ascii=False))
for commit in ('3a3a3ca', '3f6c694'):
    print(subprocess.check_output(['git', 'show', '-s', '--format=%H %cI %s%nparents: %P', commit], text=True).strip())
    rc = subprocess.run(['git', 'merge-base', '--is-ancestor', commit, SHA]).returncode
    print(f'ancestor_of_reviewed_sha {commit}: rc={rc}')
    assert rc == 0
old = show('ops/land/pr848-wp744-land-evidence.yaml', '3f6c694').decode()
for line in old.splitlines():
    if '39354156843' in line:
        print('git show 3f6c694:ops/land/pr848-wp744-land-evidence.yaml:', line.strip())
assert "jobs: '23/23 success (gom windows)'" in old
