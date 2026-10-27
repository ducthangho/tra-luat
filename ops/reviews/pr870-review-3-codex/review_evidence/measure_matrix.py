import ast
import hashlib
import json
import re
import subprocess

import yaml

SHA = '06a50c5feea77c2654f31edd26efeed7eeee62f5'

def show(path, sha=SHA):
    return subprocess.check_output(['git', 'show', f'{sha}:{path}'], text=True)

source = show('ops/lease_publish_test.py')
tree = ast.parse(source)
node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_danh_gia_bieu_thuc_chuan_bi')
isolated = ast.get_source_segment(source, node)
namespace = {'re': re}
exec(compile(ast.Module(body=[node], type_ignores=[]), '<isolated-AST>', 'exec'), namespace)
evaluate = namespace[node.name]
print(f'AST extracted {node.name}, lines {node.lineno}-{node.end_lineno}; no module import')
print(f'function_sha256={hashlib.sha256(isolated.encode()).hexdigest()}')

cases = [
    ('push-master', {'event_name': 'push', 'ref': 'refs/heads/master', 'labels': []}),
    ('PR-regular', {'event_name': 'pull_request', 'ref': 'refs/pull/870/merge', 'labels': []}),
    ('PR-other-label', {'event_name': 'pull_request', 'ref': 'refs/pull/870/merge', 'labels': ['docs']}),
    ('PR-windows', {'event_name': 'pull_request', 'ref': 'refs/pull/870/merge', 'labels': ['windows']}),
    ('dispatch-master', {'event_name': 'workflow_dispatch', 'ref': 'refs/heads/master', 'labels': []}),
    ('dispatch-feature', {'event_name': 'workflow_dispatch', 'ref': 'refs/heads/review', 'labels': []}),
]
for sha in (SHA, '9e9a74b'):
    workflow = yaml.safe_load(show('.github/workflows/ci.yml', sha))
    expression = workflow['jobs']['chuan-bi']['outputs']['os']
    print(f'\nSHA={sha}\noutputs.os={expression}')
    for label, context in cases:
        actual = evaluate(expression, context)
        expected = ['ubuntu-latest', 'windows-latest'] if label in ('PR-windows', 'dispatch-master', 'dispatch-feature') else ['ubuntu-latest']
        assert actual == expected, (label, actual, expected)
        print(f'{label}: {json.dumps(actual)} PASS')
    jobs = workflow['jobs']
    print(f'ci_jobs={len(jobs)}')
    for name, job in jobs.items():
        print(f'{name}: runs-on={job.get("runs-on")} matrix.os={job.get("strategy", {}).get("matrix", {}).get("os")} if={job.get("if", "(none)")}')
        if name != 'chuan-bi':
            assert job['strategy']['matrix']['os'] == '${{ fromJson(needs.chuan-bi.outputs.os) }}'
            assert job['runs-on'] == '${{ matrix.os }}'

assert show('.github/workflows/ci.yml') == show('.github/workflows/ci.yml', '9e9a74b')
print('\nci.yml at reviewed SHA == ci.yml at claimed base: True')
