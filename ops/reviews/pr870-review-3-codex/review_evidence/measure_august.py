import ast
from fnmatch import fnmatchcase
import json
import re
import subprocess

import yaml

SHA = '06a50c5feea77c2654f31edd26efeed7eeee62f5'
def show(path, sha=SHA):
    return subprocess.check_output(['git', 'show', f'{sha}:{path}'], text=True)

source = ast.parse(show('ops/lease_publish_test.py'))
node = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == '_danh_gia_bieu_thuc_chuan_bi')
namespace = {'re': re}
exec(compile(ast.Module(body=[node], type_ignores=[]), '<isolated-AST>', 'exec'), namespace)
evaluate = namespace[node.name]
commits = subprocess.check_output(['git', 'rev-list', '--first-parent', '--merges', 'e344e7c^..3d67128'], text=True).splitlines()
print(f'first-parent merges in historical batch e344e7c..3d67128: {len(commits)}')
assert len(commits) == 6
for commit in reversed(commits):
    print(subprocess.check_output(['git', 'show', '-s', '--format=%h %cI %s', commit], text=True).strip())
    wf = yaml.safe_load(show('.github/workflows/ci.yml', commit))
    expr = wf['jobs']['gate']['strategy']['matrix']['os'].strip()[3:-2].strip()
    wrapped = re.fullmatch(r'fromJSON\((.*)\)', expr, re.DOTALL)
    assert wrapped
    expr = wrapped.group(1).strip()
    pr = evaluate(expr, {'event_name': 'pull_request', 'ref': 'refs/pull/example/merge', 'labels': []})
    push = evaluate(expr, {'event_name': 'push', 'ref': 'refs/heads/master', 'labels': []})
    assert pr == ['ubuntu-latest'] and push == ['ubuntu-latest', 'windows-latest']
    changes = subprocess.check_output(['git', 'diff', '--name-only', f'{commit}^1', commit], text=True).splitlines()
    launcher_paths = [p for p in changes if fnmatchcase(p, '.claude/dev/**') or p == '.github/workflows/launcher-windows.yml']
    print(f'  old regular_PR={pr} old push_master={push} changes_matching_current_launcher_push_paths={launcher_paths}')

for sha in ('05170b4', '3736fc0'):
    print(subprocess.check_output(['git', 'show', '-s', '--format=%h %cI %s%n%b', sha], text=True).strip())

print('Historical labels, workflow_dispatch absence and first-ever Windows execution: NOT_MEASURED (no archived runs for the six PRs).')
data = json.loads(show('ops/land/pr848-wp744-provenance/readback-jobs-39354156843.json'))
for job in data['jobs']:
    for step in job.get('steps', []):
        if step['name'] == 'PR head contains required EOL base':
            print(f'actual run 39354156843 / {job["name"]} / {step["name"]}: status={step["status"]} conclusion={step["conclusion"]}')
            assert step['conclusion'] == 'skipped'
