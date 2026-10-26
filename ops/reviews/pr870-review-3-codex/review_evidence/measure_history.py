import json
import subprocess

import yaml

SHA = '06a50c5feea77c2654f31edd26efeed7eeee62f5'
def show(path, sha=SHA):
    return subprocess.check_output(['git', 'show', f'{sha}:{path}'], text=True)

for sha in ('d1258fe', 'd705623'):
    print(subprocess.check_output(['git', 'show', '-s', '--format=%H %cI %s', sha], text=True).strip())
    result = subprocess.run(['git', 'merge-base', '--is-ancestor', sha, SHA])
    print(f'ancestor {sha}: rc={result.returncode}')
    assert result.returncode == 0
old = yaml.safe_load(show('.github/workflows/ci.yml', 'd1258fe^'))
new = yaml.safe_load(show('.github/workflows/ci.yml', 'd705623'))
for name in ('gate', 'gate-registry', 'gate-packet-loop'):
    print(f'before #548 {name}.matrix.os={old["jobs"][name]["strategy"]["matrix"]["os"]}')
    print(f'after #548 {name}.matrix.os={new["jobs"][name]["strategy"]["matrix"]["os"]}')
    assert "github.ref == 'refs/heads/master'" in old['jobs'][name]['strategy']['matrix']['os']
expr = new['jobs']['chuan-bi']['outputs']['os']
print(f'after #548 chuan-bi.outputs.os={expr}')
assert 'github.ref' not in expr
assert 'fromJSON(' not in expr and 'fromJson(' not in expr
print('HEAD ci.yml packet marker:', next(line.strip() for line in show('.github/workflows/ci.yml').splitlines() if 'packet #548' in line))
print('HEAD CLAUDE.md old claim at base:', next(line.strip() for line in show('CLAUDE.md', '9e9a74b').splitlines() if 'còn master chạy CẢ' in line))
for name in ('3a3a3ca', '3f6c694', '4ae43f0'):
    print(subprocess.check_output(['git', 'show', '-s', '--format=%H %cI %s', name], text=True).strip())
fix = show('ops/land/pr848-wp744-land-evidence.yaml', '4ae43f0')
for line in fix.splitlines():
    if 'r4323607674' in line or "jobs: '23/23" in line:
        print('historical fix 4ae43f0:', line.strip())
rc = subprocess.run(['git', 'merge-base', '--is-ancestor', '4ae43f0', SHA]).returncode
print(f'4ae43f0 ancestor of candidate: rc={rc} (fix exists before candidate date, on separate branch)')
for line in show('ops/land/pr848-wp744-land-evidence.yaml').splitlines():
    if "jobs: '23/23" in line:
        print('HEAD land record:', line.strip())
paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', SHA], text=True).splitlines()
matching = [p for p in paths if any(s in p for s in ('pr859', 'pr865', 'pr870-review-1', 'pr870-review-2'))]
print('HEAD paths named pr859/pr865/pr870-review-1/pr870-review-2:', matching)
print('PR #865 association and actual GitHub comment body: NOT_MEASURED (no archived PR/comment at candidate; network forbidden)')
print('Do not infer that #865 is merged at candidate: current land record still contains the old quote.')
