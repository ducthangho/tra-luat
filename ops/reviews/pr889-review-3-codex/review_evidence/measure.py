import ast
import contextlib
import io
import itertools
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import types

import yaml

SHA = '094e8d17ae4dfcf21dca63702c9262267bdc072c'
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / 'cay-kho'
assert Path.cwd().resolve() == REPO

def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()

assert git('rev-parse', 'HEAD') == SHA

def source(path, sha=SHA):
    return subprocess.check_output(['git', 'show', sha + ':' + path], text=True)

ci_source = source('.github/workflows/ci.yml')
wf = yaml.safe_load(ci_source)
jobs = wf['jobs']
events = wf.get('on', wf.get(True))


def extract(path, names, namespace):
    tree = ast.parse(source(path), filename=path)
    nodes = [x for x in tree.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name in names]
    assert {x.name for x in nodes} == set(names)
    for x in nodes:
        x.decorator_list = []
    code = compile(ast.Module(body=nodes, type_ignores=[]), path, 'exec')
    exec(code, namespace)
    return namespace


def evaluator():
    return extract('ops/lease_publish_test.py', ['_danh_gia_bieu_thuc_chuan_bi'], {'re': re})['_danh_gia_bieu_thuc_chuan_bi']


def chuanbi():
    f = evaluator()
    expr = jobs['chuan-bi']['outputs']['os']
    config = events['workflow_dispatch']['inputs']['runner_set']
    print('runner_set:', json.dumps(config, ensure_ascii=False, sort_keys=True))
    for name, ctx in [
        ('dispatch windows-only', {'event_name': 'workflow_dispatch', 'inputs': {'runner_set': 'windows-only'}}),
        ('dispatch default', {'event_name': 'workflow_dispatch', 'inputs': {'runner_set': config['default']}}),
        ('dispatch missing input', {'event_name': 'workflow_dispatch'}),
        ('dispatch other', {'event_name': 'workflow_dispatch', 'inputs': {'runner_set': 'unknown'}}),
        ('push master', {'event_name': 'push', 'ref': 'refs/heads/master'}),
        ('push other ref expression only', {'event_name': 'push', 'ref': 'refs/heads/example'}),
        ('PR ordinary', {'event_name': 'pull_request', 'labels': ['docs']}),
        ('PR windows label', {'event_name': 'pull_request', 'labels': ['windows']}),
    ]:
        print(name + ': ' + json.dumps(f(expr, ctx), separators=(',', ':')))
    for event, labels in [('push', []), ('pull_request', []), ('pull_request', ['windows'])]:
        ctx = {'event_name': event, 'labels': labels}
        assert f(expr, ctx) == f(expr, dict(ctx, inputs={'runner_set': 'windows-only'}))
    print('input windows-only cannot alter push/PR: PASS (3 cases)')
    print('push trigger:', json.dumps(events['push']))
    print('pull_request trigger:', json.dumps(events['pull_request']))
    print('other dispatch value: evaluator only; choice input does not list unknown')


def expand(job, os_values):
    matrix = job['strategy']['matrix']
    axes = {k: (os_values if k == 'os' else v) for k, v in matrix.items() if k not in ('include', 'exclude')}
    assert all(isinstance(v, list) for v in axes.values()), axes
    result = []
    for row in itertools.product(*axes.values()):
        item = dict(zip(axes, row))
        if not any(all(item.get(k) == v for k, v in exclusion.items()) for exclusion in matrix.get('exclude', [])):
            result.append(item)
    assert not matrix.get('include'), 'unhandled include'
    return result


def topology():
    for jid in ['gate-cong-cu', 'gate-cong-cu-gop']:
        job = jobs[jid]
        print(jid + ' exclude: ' + json.dumps(job['strategy']['matrix'].get('exclude'), ensure_ascii=False))
        print(jid + ' job-if: ' + str(job.get('if')))
        for os_values in [['windows-latest'], ['ubuntu-latest', 'windows-latest']]:
            print(jid + ' ' + json.dumps(os_values) + ' -> ' + json.dumps(expand(job, os_values), separators=(',', ':')))
    job_if = jobs['gate-cong-cu-gop']['if']
    match = re.fullmatch(r"\$\{\{\s*!cancelled\(\)\s*&&\s*contains\(fromJson\(needs\.chuan-bi\.outputs\.os\),\s*'([^']+)'\)\s*\}\}", job_if)
    assert match, job_if
    for os_values in [['windows-latest'], ['ubuntu-latest'], ['ubuntu-latest', 'windows-latest']]:
        for cancelled in [False, True]:
            measured = (not cancelled) and match.group(1) in json.loads(json.dumps(os_values))
            print(f'gop predicate os={os_values} cancelled={cancelled} -> {measured}')
    print('MEASURED: YAML exclusions and job predicate false for windows-only, regardless of cancellation.')
    print('NOT MEASURED: actual GitHub scheduler conclusion=skipped at this SHA (offline; no API calls).')
    for jid, job in jobs.items():
        if jid.startswith('gate') and jid not in ('gate-cong-cu', 'gate-cong-cu-gop'):
            rows = expand(job, ['windows-latest'])
            print(f'other {jid}: windows_rows={len(rows)} job-if={job.get("if")} runs-on={job.get("runs-on")}')


def os_steps():
    found = []
    for jid, job in jobs.items():
        for n, step in enumerate(job.get('steps', []), 1):
            cond = str(step.get('if', ''))
            if re.search(r'\b(?:runner|matrix)\.os\b', cond):
                found.append((jid, n, step.get('name', step.get('uses')), cond))
    for jid, n, name, cond in found:
        print(f'{jid} step={n} {name}: {cond}')
    print('total:', len(found))
    print('with runner.os:', sum('runner.os' in x[3] for x in found))
    print('with matrix.os:', sum('matrix.os' in x[3] for x in found))
    raw = [(i, s.strip()) for i, s in enumerate(ci_source.splitlines(), 1) if re.search(r'\bif:.*\b(?:runner|matrix)\.os\b', s)]
    print('raw source lines:', json.dumps(raw, ensure_ascii=False))
    assert len(raw) == len(found)


def windows_main():
    class BoQuaMoiTruong(Exception):
        pass
    namespace = extract('ops/cong_cu_test.py', ['main', 'nen_bo_qua_dot_bien', 'dat_windows', 'dong_windows'], {
        '_TEN_NEN': 'nt', 'os': types.SimpleNamespace(environ={'CONG_CU_TEST_MANH': '0/8'}),
        'BoQuaMoiTruong': BoQuaMoiTruong,
    })
    print('nen_bo_qua_dot_bien(nt,posix,java):', [namespace['nen_bo_qua_dot_bien'](x) for x in ('nt', 'posix', 'java')])
    print('dat_windows(cases,errors,mutants):', [(x, namespace['dat_windows'](*x)) for x in [(2, 0, 3), (0, 0, 3), (2, 1, 3), (2, 0, 0)]])
    namespace.update(_doc_che_do=lambda env: ('manh', (0, 8, Path('/never-written'))),
                     batch_behavior_test=object(), python_alias_behavior_test=object(), DOT_BIEN=['a', 'b', 'c'])
    for scenario in ('all-pass', 'one-skip', 'one-fail', 'all-skip', 'precheck-skip'):
        trace = []
        def passing():
            trace.append('passing')
        def second():
            trace.append('second')
            if scenario in ('one-skip', 'all-skip'):
                raise BoQuaMoiTruong('fixture missing capability')
            if scenario == 'one-fail':
                raise AssertionError('fixture assertion')
        def first_skip():
            trace.append('first_skip')
            raise BoQuaMoiTruong('fixture missing capability')
        def forbidden(*args, **kwargs):
            raise AssertionError('mutation or artifact path reached')
        namespace.update(CA=[first_skip if scenario == 'all-skip' else passing, second],
                         _chay_tien_kiem=(lambda fn: ('precheck', 'fixture missing') if scenario == 'precheck-skip' else None),
                         _phan_manh=forbidden, _phong_con=forbidden, _ket_thuc_manh=forbidden,
                         _cong_tren_cay_that=forbidden)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = namespace['main']()
        print(f'scenario={scenario} rc={rc} visited={trace}')
        print(out.getvalue().strip())
        assert rc == (0 if scenario in ('all-pass', 'one-skip') else 1)
        assert len(trace) == 2
    print('AST source main: so_ca = len(CA) - len(bo_qua) present:', 'so_ca = len(CA) - len(bo_qua)' in source('ops/cong_cu_test.py'))
    print('SCOPE: executes exact AST control flow with synthetic CA on Linux; does not run real Windows CA.')


def history():
    print('base full:', git('rev-parse', 'e63961f'))
    print('base ancestor rc:', subprocess.run(['git', 'merge-base', '--is-ancestor', 'e63961f', SHA]).returncode)
    print('tree:', git('rev-parse', 'HEAD^{tree}'))
    print('patch matches:', subprocess.check_output(['git', 'diff', 'e63961f', SHA, '--', 'CLAUDE.md']) == (ROOT / 'diff.patch').read_bytes())
    for path in ['.github/workflows/ci.yml', 'ops/cong_cu_test.py', 'ops/lease_publish_test.py']:
        print(path + ' base=head:', source(path, 'e63961f') == source(path))
    print('commits base..HEAD:')
    print(git('log', '--format=%h %ad %s', '--date=short', 'e63961f..' + SHA))
    print('extra change over 8d5cccb:')
    print(git('diff', '8d5cccb', SHA, '--', 'CLAUDE.md'))
    for pattern in ['#878', '#879']:
        print('history ' + pattern + ':')
        print(git('log', '--all', '--format=%h %ad %s', '--date=short', '--grep=' + pattern, '-8'))


if __name__ == '__main__':
    {'chuanbi': chuanbi, 'topology': topology, 'os-steps': os_steps,
     'windows-main': windows_main, 'history': history}[sys.argv[1]]()
