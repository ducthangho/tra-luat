import ast
import contextlib
import hashlib
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
OUT = Path(__file__).resolve().parent
EVIDENCE = OUT / 'review_evidence'
EVIDENCE.mkdir(exist_ok=True)


def git(*args):
    return subprocess.check_output(['git', *args], text=True)


def source(path, rev=SHA):
    return git('show', f'{rev}:{path}')


def workflow(rev=SHA):
    return yaml.safe_load(source('.github/workflows/ci.yml', rev))


def extract(path, names, namespace):
    tree = ast.parse(source(path))
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    for n in nodes:
        n.decorator_list = []
    exec(compile(ast.Module(body=nodes, type_ignores=[]), f'{SHA}:{path}', 'exec'), namespace)
    return namespace


def os_eval():
    return extract('ops/lease_publish_test.py', ['_danh_gia_bieu_thuc_chuan_bi'], {'re': re})['_danh_gia_bieu_thuc_chuan_bi']


def expand(job, os_list):
    m = job['strategy']['matrix']
    dims = {k: os_list if k == 'os' else v for k, v in m.items() if k not in ('exclude', 'include')}
    rows = [dict(zip(dims, x)) for x in itertools.product(*dims.values())]
    return [x for x in rows if not any(all(x.get(k) == v for k, v in e.items()) for e in m.get('exclude', []))]


def dispatch():
    w = workflow()
    settings = (w.get('on') or w.get(True))['workflow_dispatch']['inputs']['runner_set']
    print('runner_set=' + json.dumps(settings, ensure_ascii=False, sort_keys=True))
    assert settings['default'] == 'windows-and-ubuntu'
    f = os_eval()
    expr = w['jobs']['chuan-bi']['outputs']['os']
    print('AST source=ops/lease_publish_test.py:_danh_gia_bieu_thuc_chuan_bi')
    u, win = 'ubuntu-latest', 'windows-latest'
    cases = [('workflow_dispatch', x, [], [win] if x == 'windows-only' else [u, win])
             for x in ('windows-only', 'windows-and-ubuntu', 'other', '', None)]
    cases += [('push', x, [], [u]) for x in (None, 'windows-only')]
    cases += [('pull_request', x, labels, [u, win] if 'windows' in labels else [u])
              for x in (None, 'windows-only') for labels in ([], ['windows'])]
    for event, runner, labels, expected in cases:
        ctx = {'event_name': event, 'ref': 'refs/heads/master', 'labels': labels}
        if runner is not None:
            ctx['inputs'] = {'runner_set': runner}
        actual = f(expr, ctx)
        print(json.dumps({'event': event, 'runner_set': runner, 'labels': labels, 'os': actual}, ensure_ascii=False))
        assert actual == expected
    assert source('.github/workflows/ci.yml', 'e63961f') == source('.github/workflows/ci.yml')
    print(f'PASS: {len(cases)} cases; ci.yml at e63961f == reviewed SHA')


def matrix():
    w = workflow()
    for os_list in (['windows-latest'], ['ubuntu-latest', 'windows-latest'], ['ubuntu-latest']):
        rows = expand(w['jobs']['gate-cong-cu'], os_list)
        print('os=' + json.dumps(os_list) + ' gate-cong-cu=' + json.dumps(rows, sort_keys=True))
        assert [r['manh'] for r in rows if r['os'] == 'windows-latest'] == ([0] if 'windows-latest' in os_list else [])
        assert [r['manh'] for r in rows if r['os'] == 'ubuntu-latest'] == (list(range(8)) if 'ubuntu-latest' in os_list else [])
    for name, job in w['jobs'].items():
        if name.startswith('gate'):
            assert job['strategy']['matrix']['os'] == '${{ fromJson(needs.chuan-bi.outputs.os) }}'
            rows = expand(job, ['windows-latest'])
            print(f'{name}: Windows cells={len(rows)}; job-if={job.get("if", "<absent>")}')
            if name != 'gate-cong-cu-gop':
                assert rows
    print('PASS: matrix excludes only Windows shards 1..7 and Windows aggregator')


def aggregator():
    job = workflow()['jobs']['gate-cong-cu-gop']
    cond = job['if']
    expected = "${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}"
    assert cond == expected
    assert job['strategy']['matrix']['exclude'] == [{'os': 'windows-latest'}]
    print('job-if=' + cond)
    print('exclude=' + json.dumps(job['strategy']['matrix']['exclude']))
    for values in (['windows-latest'], ['ubuntu-latest'], ['ubuntu-latest', 'windows-latest']):
        for cancelled in (False, True):
            enabled = not cancelled and 'ubuntu-latest' in values
            print(json.dumps({'os': values, 'cancelled': cancelled, 'local_job_if': enabled,
                              'expanded_matrix': expand(job, values)}))
    print('PASS: windows-only => if=false, no Ubuntu matrix cell; local inference: job skipped')
    print('KHÔNG ĐO ĐƯỢC: actual GitHub check-run conclusion/runner/log at reviewed SHA (no network; no dispatch performed)')


def steps():
    w = workflow()
    tree = yaml.compose(source('.github/workflows/ci.yml'))
    job_node = next(v for k, v in tree.value if k.value == 'jobs')
    lines = {}
    for key, node in job_node.value:
        for k, v in node.value:
            if k.value == 'steps':
                for i, step in enumerate(v.value):
                    for sk, sv in step.value:
                        if sk.value == 'if':
                            lines[(key.value, i)] = sv.start_mark.line + 1
    count = 0
    for name, job in w['jobs'].items():
        for i, step in enumerate(job.get('steps', [])):
            cond = str(step.get('if', ''))
            if re.search(r'\b(?:runner|matrix)\.os\b', cond):
                count += 1
                label = step.get('name', step.get('uses'))
                print(f'{count}. ci.yml:{lines[(name, i)]} {name} / {label}: {cond}')
    print(f'COUNT={count} (runner.os OR matrix.os in step if; comments/runs-on excluded)')
    assert count == 6


def windows():
    names = ['BoQuaMoiTruong', 'nen_bo_qua_dot_bien', 'dat_windows', 'dong_windows', '_doc_che_do', 'main']
    ns = extract('ops/cong_cu_test.py', names, {})
    ns.update(_TEN_NEN='nt', _BIEN_BAN_KINH='CONG_CU_TEST_BAN_KINH', _BIEN_MANH='CONG_CU_TEST_MANH',
              _BIEN_MANH_RA='CONG_CU_TEST_MANH_RA', _TRAN_MANH=16)
    for platform in ('nt', 'posix', 'java'):
        print(f'nen_bo_qua_dot_bien({platform!r})={ns["nen_bo_qua_dot_bien"](platform)}')
    for args in ((2, 0, 1), (0, 0, 1), (2, 1, 1), (2, 0, 0)):
        print(f'dat_windows{args}={ns["dat_windows"](*args)}')
    def forbidden(*a, **kw):
        raise RuntimeError('FORBIDDEN: mutation/shard/write/real-tree gate reached')
    for name in ('_phan_manh', '_phong_con', '_ket_thuc_manh', '_cong_tren_cay_that', '_ban_kinh_moi_dot_bien'):
        ns[name] = forbidden
    def marker():
        pass
    marker.__name__ = 'batch_behavior_test'
    ns['batch_behavior_test'] = marker
    ns['python_alias_behavior_test'] = marker
    cases = [(['pass', 'pass', 'skip'], False, True, 0),
             (['skip', 'skip', 'skip'], False, True, 1),
             (['pass', 'fail', 'skip'], False, True, 1),
             (['pass', 'error', 'skip'], False, True, 1),
             (['pass', 'pass', 'skip'], True, True, 1),
             (['pass', 'pass', 'skip'], False, False, 1)]
    for modes, pre_skip, mutants, expected in cases:
        visited = []
        def make(index, mode):
            def fn():
                visited.append(index)
                if mode == 'skip':
                    raise ns['BoQuaMoiTruong']('capability unavailable (controlled fixture)')
                if mode == 'fail':
                    raise AssertionError('controlled red baseline')
                if mode == 'error':
                    raise RuntimeError('controlled baseline exception')
            fn.__name__ = f'baseline_{index}_{mode}'
            return fn
        ns['CA'] = [make(i, x) for i, x in enumerate(modes)]
        ns['DOT_BIEN'] = {'dummy_mutant': None} if mutants else {}
        ns['os'] = types.SimpleNamespace(environ={'CONG_CU_TEST_MANH': '0/8', 'CONG_CU_TEST_MANH_RA': 'never-written.txt'})
        ns['_chay_tien_kiem'] = lambda fn: ('precheck', 'controlled missing capability') if pre_skip else None
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            rc = ns['main']()
        print(f'CASE modes={modes}; precheck_skip={pre_skip}; mutant_table_nonempty={mutants}; rc={rc}; visited={visited}')
        print(capture.getvalue().strip())
        assert rc == expected and visited == list(range(len(modes)))
        if modes == ['pass', 'pass', 'skip']:
            assert 'cong_cu_test: 2/2 đạt; tổng=3, bỏ qua=1' in capture.getvalue()
    print('PASS: unmodified AST main visits all fixtures, skips deducted, zero executed cases/red/precheck/empty mutants fail, no mutation or shard write')
    print('SCOPE: Linux controlled execution of Windows branch; real Windows baseline suite NOT RUN')


def skip_sources():
    raw = source('ops/cong_cu_test.py')
    tree = ast.parse(raw)
    occurrences = []
    for fn in tree.body:
        if isinstance(fn, ast.FunctionDef):
            for node in ast.walk(fn):
                if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name) and node.exc.func.id == 'BoQuaMoiTruong':
                    if node.exc.args and isinstance(node.exc.args[0], ast.Constant):
                        msg = node.exc.args[0].value
                        if '/bin/' in str(msg) or 'actionlint' in str(msg):
                            occurrences.append((fn.name, node.lineno, msg))
    for row in occurrences:
        print(json.dumps(row, ensure_ascii=False))
    assert any('/bin/sh' in x[2] for x in occurrences)
    print('exact denominator formula present=' + str('so_ca = len(CA) - len(bo_qua)' in raw))
    assert 'so_ca = len(CA) - len(bo_qua)' in raw
    old = git('diff', '8d5cccb', SHA, '--', 'CLAUDE.md')
    print(old.strip())
    print('PASS: capability skips are explicit; both edited statements now limit claim to non-skipped baselines')


def history():
    print(git('show', '-s', '--format=%H %aI %cI %s', 'e63961f').strip())
    for path in ('.github/workflows/ci.yml', 'ops/cong_cu_test.py'):
        a, b = source(path, 'e63961f'), source(path)
        print(f'{path}: base-equals-reviewed={a == b}; sha256={hashlib.sha256(b.encode()).hexdigest()}')
        assert a == b
    print(git('log', '-n', '4', '--format=%h %ad %s', '--date=short', 'e63961f', '--', '.github/workflows/ci.yml', 'ops/cong_cu_test.py').strip())
    for rev, pr in [('5585abe', '#878'), ('be00ef7', '#879'), ('ab25106', '#879')]:
        p = subprocess.run(['git', 'merge-base', '--is-ancestor', rev, SHA])
        print(f'{rev} ({pr}) ancestor_of_reviewed: rc={p.returncode}')
        assert p.returncode == 0
    historical = workflow('9e9a74b')['jobs']['chuan-bi']['outputs']['os']
    f = os_eval()
    print('9e9a74b historical windows-only dispatch=' + json.dumps(f(historical, {'event_name': 'workflow_dispatch', 'inputs': {'runner_set': 'windows-only'}})))
    print('PASS: claims dated e63961f still hold at reviewed SHA; #878/#879 ancestry verified')


def provenance():
    ns = extract('ops/cong_cu_test.py', ['_doc_che_do', '_van_tay'], {'subprocess': subprocess, 'Path': Path})
    tree = ast.parse(source('ops/cong_cu_test.py'))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Tuple) and [getattr(x, 'id', '') for x in target.elts] == ['_BIEN_BAN_KINH', '_BIEN_MANH', '_BIEN_MANH_RA']:
                    for key, value in zip(target.elts, ast.literal_eval(node.value)):
                        ns[key.id] = value
                elif isinstance(target, ast.Name) and target.id == '_TRAN_MANH':
                    ns[target.id] = ast.literal_eval(node.value)
                elif isinstance(target, ast.Name) and target.id == '_TEN_NEN':
                    print('_TEN_NEN source=' + ast.unparse(node.value))
                    assert ast.unparse(node.value) == 'os.name'
    w = workflow()
    for name, job in w['jobs'].items():
        for step in job.get('steps', []):
            if 'ops/cong_cu_test.py' in step.get('run', ''):
                env = dict(w.get('env', {}), **job.get('env', {}), **step.get('env', {}))
                env = {k: v.replace('${{ matrix.manh }}', '0') if isinstance(v, str) else v for k, v in env.items()}
                mode = '--gop' if '--gop' in step['run'] else ns['_doc_che_do'](env)
                print(f'{name}: mode={mode}; command={step["run"].strip()!r}')
                if name == 'gate':
                    assert mode == ('gate', None)
                elif name == 'gate-cong-cu':
                    assert mode == ('manh', (0, 8, 'manh/manh-0.txt'))
    print('fixed chuan-bi runner=' + w['jobs']['chuan-bi']['runs-on'])
    assert w['jobs']['chuan-bi']['runs-on'] == 'ubuntu-latest'
    ns.update(GOC=Path.cwd(), TEP_TEST=Path.cwd() / 'ops/cong_cu_test.py')
    fingerprint = ns['_van_tay']()
    print('actual local fingerprint=' + json.dumps(fingerprint, sort_keys=True))
    assert fingerprint['head'] == SHA
    assert fingerprint['sha256_test'] == hashlib.sha256(source('ops/cong_cu_test.py').encode()).hexdigest()
    print('Scope: windows-only removes Ubuntu from os output; chuan-bi itself still uses Ubuntu.')
    print('Scope: mutation radius claim concerns cong_cu_test.py; other suites may run their own mutants on Windows.')
    print('Same head requires exact tested checkout identity. A PR synthetic merge and a dispatch of its branch may differ.')
    print('KHÔNG ĐO ĐƯỢC: paired native Ubuntu/Windows runs and exact checkout identities at this SHA (offline).')
    print('PASS: only Ubuntu shards retain the full G5 mutation-radius path in this CI configuration.')


def previous_finding():
    prior = source('ops/reviews/pr889-review-1-codex-verdict.md', '9ff20c2')
    slug = 'windows-green-does-not-prove-all-baselines'
    finding_headers = [line for line in prior.splitlines() if line.startswith('### ') and re.search(r'\[P[0-3]\]', line)]
    print('prior-finding-headers=' + json.dumps(finding_headers, ensure_ascii=False))
    assert len(finding_headers) == 1 and slug in finding_headers[0]
    ns = extract('ops/cong_cu_test.py', ['BoQuaMoiTruong', 'nen_bo_qua_dot_bien', 'dat_windows', 'dong_windows', 'main',
                   't51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi'], {})
    class AbsentPath:
        def __init__(self, path):
            assert path == '/bin/sh'
        def exists(self):
            return False
    ns.update(Path=AbsentPath, _TEN_NEN='nt', DOT_BIEN={'fixture_mutant': None}, os=types.SimpleNamespace(environ={}))
    def passed():
        pass
    ns.update(CA=[passed, ns['t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi'], passed],
              batch_behavior_test=passed, python_alias_behavior_test=passed,
              _chay_tien_kiem=lambda fn: None, _doc_che_do=lambda env: ('manh', (0, 8, 'never-written.txt')))
    rc = ns['main']()
    print(f'actual t51 with missing /bin/sh + two passing fixtures: rc={rc}')
    assert rc == 0
    doc = source('CLAUDE.md')
    for number, line in enumerate(doc.splitlines(), 1):
        if 180 <= number <= 191:
            print(f'CLAUDE.md:{number}: {line}')
    assert 'duyệt toàn bộ ca nền rồi DỪNG (ca thiếu năng lực vẫn có thể `BỎ QUA`' in doc
    assert 'các ca nền KHÔNG bị bỏ qua đạt trên Windows' in doc
    assert 'phải đọc riêng các dòng `BỎ QUA` trong log' in doc
    print(f'{slug}: ĐÃ VÁ THẬT in both sentences; extra final-sentence edit preserves the measured scope.')


def gate(command):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', TL_CACHE_DIR=str(EVIDENCE / 'tl_cache'))
    p = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if '--json' in command and p.returncode == 0:
        (EVIDENCE / 'doc-claims-check.json').write_text(p.stdout, encoding='utf-8')
        data = json.loads(p.stdout)
        print(json.dumps({k: data[k] for k in ('ok', 'schema', 'files_scanned', 'flags', 'advisory_count', 'layers_skipped', 'strict')}, ensure_ascii=False, indent=2))
        print('Full raw JSON: ../review_evidence/doc-claims-check.json')
    else:
        print(p.stdout.rstrip())
    print(f'COMMAND_RC={p.returncode}')
    assert p.returncode == 0
    if '--json' in command:
        assert json.loads(p.stdout)['ok'] is True
        print('ASSERT ok=true: PASS')


CASES = {
    'dispatch': ('2', 'Đánh giá os và mặc định runner_set bằng AST', 'Nhánh windows-only có thể lấn push/PR hoặc mặc định không còn hai nền.', dispatch),
    'matrix': ('3', 'Khai triển mọi ma trận gate trên Windows', 'Windows có thể còn mảnh 1..7 hoặc một gate khác cũng mất job.', matrix),
    'aggregator': ('4', 'Điều kiện job gom và giới hạn quan sát không mạng', 'windows-only có thể khởi động job gom hoặc sinh lỗi ma trận rỗng.', aggregator),
    'steps': ('5', 'Đếm điều kiện OS ở cấp bước bằng YAML', 'Số 6 có thể đếm sót matrix.os hoặc lẫn điều kiện ngoài bước.', steps),
    'windows': ('6', 'Chạy nguyên hàm main nhánh Windows với đối chứng', 'Bỏ qua bị tính đạt, không duyệt hết ca hoặc Windows vẫn đo đột biến/ghi mảnh.', windows),
    'skip_sources': ('7', 'Nguồn bỏ qua do thiếu năng lực và câu sửa ngoài hint', 'Câu sửa cuối vẫn rộng hơn tập ca nền thực chạy.', skip_sources),
    'history': ('8', 'Kiểm SHA lịch sử và nguồn #878/#879', 'Tài liệu viện e63961f nhưng cấu hình đã khác tại reviewed SHA.', history),
    'doctrine': ('9', 'Cổng doctrine-scan', 'Đoạn mới có thể vi phạm cổng doctrine.', lambda: gate(['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'])),
    'doc_claims': ('10', 'Cổng doc-claims-check', 'Đoạn mới có thể chứa tham chiếu cơ học sai.', lambda: gate(['python3', 'scripts/tl.py', 'doc-claims-check', '--json'])),
    'provenance': ('11', 'Phạm vi G5, cấu hình chế độ thật và cùng head', 'Một lời khai có thể bị hiểu rộng sang job chuẩn bị hoặc bán kính của bộ test khác.', provenance),
    'previous_finding': ('12', 'Đối chiếu finding trước bằng ca t51 thật', 'Câu sửa thêm ngoài hint có thể tái tạo overclaim ca nền.', previous_finding),
}


if __name__ == '__main__':
    key = sys.argv[1]
    number, title, hypothesis, fn = CASES[key]
    stream, rc = io.StringIO(), 0
    try:
        with contextlib.redirect_stdout(stream):
            assert git('rev-parse', 'HEAD').strip() == SHA
            fn()
    except Exception:
        import traceback
        traceback.print_exc(file=stream)
        rc = 1
    output = stream.getvalue()
    (EVIDENCE / f'{key}.txt').write_text(output, encoding='utf-8')
    report = OUT / 'VERDICT.md'
    with report.open('a', encoding='utf-8') as f:
        f.write(f'### HƯỚNG {number}: {title}\n\n- giả thuyết: {hypothesis}\n'
                f'- lệnh (từ `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 ../review_measure.py {key}`. '
                f'Mã đo lưu nguyên tại `../review_measure.py`; nguồn đọc bằng `git show {SHA}:<tệp>`.\n'
                f'- output thật:\n\n```text\n{output.rstrip()}\n```\n\n- rc: {rc}.\n'
                f'- kết luận: {"KHÔNG PHẢI LỖI" if rc == 0 else "CHƯA KẾT LUẬN — xem lỗi phép đo"}'
                f'{" về cấu hình; KHÔNG ĐO ĐƯỢC trạng thái thực trên GitHub không mạng" if key == "aggregator" else ""}.\n\n')
    print(output, end='')
    sys.exit(rc)
