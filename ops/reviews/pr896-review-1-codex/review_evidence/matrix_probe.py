import ast
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import yaml

repo = Path.cwd()
spec = importlib.util.spec_from_file_location('review_lp', repo / 'ops/lease_publish_test.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
source = (repo / 'ops/lease_publish_test.py').read_text()
tree = ast.parse(source)
for name in ('t161_M3_chot_nguon_duy_nhat_ma_tran_ci', 't162_M4_evaluator_toi_gian_chuan_bi'):
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    calls = [n.func.id for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
    print(f'{name}: lines {node.lineno}-{node.end_lineno}; direct evaluator calls={calls.count("_danh_gia_bieu_thuc_chuan_bi")}; assertions bang={calls.count("bang")}')
raw = yaml.safe_load((repo / '.github/workflows/ci.yml').read_text())
expr = raw['jobs']['chuan-bi']['outputs']['os']
contexts = [
    ('push master', dict(event_name='push', ref='refs/heads/master', labels=[])),
    ('PR thường', dict(event_name='pull_request', ref='refs/pull/1/merge', labels=['docs'])),
    ('PR windows', dict(event_name='pull_request', ref='refs/pull/1/merge', labels=['windows'])),
    ('dispatch absent', dict(event_name='workflow_dispatch', ref='refs/heads/master', labels=[])),
    ('dispatch default', dict(event_name='workflow_dispatch', ref='refs/heads/master', labels=[], inputs={'runner_set':'windows-and-ubuntu'})),
    ('dispatch windows-only', dict(event_name='workflow_dispatch', ref='refs/heads/master', labels=[], inputs={'runner_set':'windows-only'})),
]
for sha in ('e63961f', '816f43988eb3012726120ad00166a989cc2b9af6'):
    wf = yaml.safe_load(subprocess.check_output(['git', 'show', f'{sha}:.github/workflows/ci.yml'], text=True))
    ex = wf['jobs']['chuan-bi']['outputs']['os']
    print(f'COMMIT {sha} expression={ex}')
    for label, ctx in contexts:
        print(f'  {label}: {m._danh_gia_bieu_thuc_chuan_bi(ex, ctx)}')

original_evaluator = m._danh_gia_bieu_thuc_chuan_bi
seen = []
def trace(ex, ctx):
    try:
        result = original_evaluator(ex, ctx)
    except ValueError:
        if ex == expr:
            seen.append((ctx, 'ValueError'))
        raise
    if ex == expr:
        seen.append((ctx, result))
    return result
m._danh_gia_bieu_thuc_chuan_bi = trace
with contextlib.redirect_stdout(io.StringIO()):
    m.t162_M4_evaluator_toi_gian_chuan_bi()
m._danh_gia_bieu_thuc_chuan_bi = original_evaluator
print('TRACE t162 actual expression calls: ' + str(len(seen)))
for ctx, result in seen:
    print('  ' + json.dumps(ctx, ensure_ascii=False, sort_keys=True) + ' => ' + json.dumps(result))

mutations = {}
def mutated(name):
    d = copy.deepcopy(raw)
    mutations[name] = d
    return d
mutated('baseline')
d = mutated('push_master_gets_windows')
d['jobs']['chuan-bi']['outputs']['os'] = expr.replace("|| contains(", "|| github.ref == 'refs/heads/master' || contains(", 1)
d = mutated('remove_windows_only_branch')
d['jobs']['chuan-bi']['outputs']['os'] = re.sub(r"\(github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only'\)\s*&&\s*'\[\"windows-latest\"\]'\s*\|\|\s*", '', expr, count=1)
d = mutated('PR_windows_becomes_linux')
d['jobs']['chuan-bi']['outputs']['os'] = expr.replace(".name, 'windows'", ".name, 'linux'", 1)
d = mutated('dispatch_windows_only_becomes_both')
d['jobs']['chuan-bi']['outputs']['os'] = expr.replace("&& '[\"windows-latest\"]'", "&& '[\"ubuntu-latest\",\"windows-latest\"]'", 1)
d = mutated('output_wrapped_fromJSON')
d['jobs']['chuan-bi']['outputs']['os'] = "${{ fromJSON('[\"ubuntu-latest\"]') }}"
d = mutated('independent_job_os')
d['jobs']['gate']['strategy']['matrix']['os'] = ['ubuntu-latest']
d = mutated('remove_Windows_shard1_exclusion')
d['jobs']['gate-cong-cu']['strategy']['matrix']['exclude'].remove({'os':'windows-latest','manh':1})
d = mutated('remove_gop_if')
del d['jobs']['gate-cong-cu-gop']['if']
original_here = m.HERE
with tempfile.TemporaryDirectory(prefix='pr896-matrix-') as td:
    root = Path(td)
    (root / 'ops').mkdir()
    (root / '.github/workflows').mkdir(parents=True)
    m.HERE = root / 'ops'
    for name, data in mutations.items():
        (root / '.github/workflows/ci.yml').write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
        results = []
        for fn in (m.t161_M3_chot_nguon_duy_nhat_ma_tran_ci, m.t162_M4_evaluator_toi_gian_chuan_bi):
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    fn()
                result = 'PASS'
            except Exception as ex:
                result = 'FAIL ' + type(ex).__name__ + ': ' + str(ex).splitlines()[0]
            results.append(fn.__name__.split('_')[0] + '=' + result)
        print(f'MUTATION {name}: ' + '; '.join(results))
m.HERE = original_here
