#!/usr/bin/env python3
"""Offline, read-only probes of cay-kho; evidence/artifacts live beside it."""
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

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'cay-kho'
WF = REPO / '.github/workflows/ci.yml'
RAW = WF.read_text()
W = yaml.safe_load(RAW)
J = W['jobs']


def extract(path, names, namespace=None):
    source = (REPO / path).read_text()
    tree = ast.parse(source)
    ns = {} if namespace is None else namespace
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names:
            exact = ast.get_source_segment(source, n)
            exec(compile(exact, str(REPO / path), 'exec'), ns)
            print(f'AST exact {path}:{n.lineno}-{n.end_lineno} {n.name}')
    return ns


def evaluator():
    return extract('ops/lease_publish_test.py', {'_danh_gia_bieu_thuc_chuan_bi'}, {'re': re})['_danh_gia_bieu_thuc_chuan_bi']


def expand(matrix, oses):
    if not matrix:
        return []
    axes = {k: (oses if k == 'os' else v) for k, v in matrix.items() if k not in ('exclude', 'include')}
    rows = [dict(zip(axes, values)) for values in itertools.product(*axes.values())]
    return [row for row in rows if not any(all(row.get(k) == v for k, v in exc.items()) for exc in matrix.get('exclude', []))]


def expression():
    ev = evaluator()
    expr = J['chuan-bi']['outputs']['os']
    default = W.get('on', W.get(True))['workflow_dispatch']['inputs']['runner_set']['default']
    print('REAL outputs.os =', expr)
    print('runner_set.default =', default)
    for tag, context in [
        ('push master', dict(event_name='push', ref='refs/heads/master', labels=[])),
        ('dispatch windows-only', dict(event_name='workflow_dispatch', inputs={'runner_set': 'windows-only'})),
        ('dispatch default', dict(event_name='workflow_dispatch', inputs={'runner_set': default})),
        ('dispatch missing inputs', dict(event_name='workflow_dispatch')),
        ('PR without label', dict(event_name='pull_request', labels=[])),
        ('PR windows label', dict(event_name='pull_request', labels=['windows'])),
        ('push with irrelevant windows-only input', dict(event_name='push', ref='refs/heads/master', inputs={'runner_set': 'windows-only'})),
    ]:
        print(tag, '=>', json.dumps(ev(expr, context)))
    for sha in ('e63961f', 'HEAD'):
        blob = subprocess.check_output(['git', 'show', f'{sha}:.github/workflows/ci.yml'], cwd=REPO, text=True)
        print(sha, 'workflow-identical-to-checkout =', blob == RAW)


def windows():
    matrix = J['gate-cong-cu']['strategy']['matrix']
    print('matrix =', json.dumps(matrix, ensure_ascii=False))
    for oses in (['windows-latest'], ['ubuntu-latest', 'windows-latest']):
        print('expanded', oses, '=>', expand(matrix, oses))
    ns = extract('ops/cong_cu_test.py', {'nen_bo_qua_dot_bien', 'dat_windows', 'dong_windows', 'BoQuaMoiTruong', 'main', '_doc_che_do', 't51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi'},
                 {'_TEN_NEN': 'nt', '_BIEN_BAN_KINH': 'CONG_CU_TEST_BAN_KINH', '_BIEN_MANH': 'CONG_CU_TEST_MANH', '_BIEN_MANH_RA': 'CONG_CU_TEST_MANH_RA', '_TRAN_MANH': 16})
    for platform in ('nt', 'posix', 'java'):
        print('nen_bo_qua_dot_bien', platform, '=>', ns['nen_bo_qua_dot_bien'](platform))
    for values in ((61, 0, 470), (0, 0, 470), (61, 1, 470), (61, 0, 0)):
        print('dat_windows', values, '=>', ns['dat_windows'](*values))
    print('dong_windows =>', ns['dong_windows'](60, 61, 470))
    events = []
    def passed_first(): events.append('first')
    def skipped_middle():
        events.append('middle')
        raise ns['BoQuaMoiTruong']('fake missing capability')
    def passed_last(): events.append('last')
    def failed_middle():
        events.append('middle-fail')
        raise AssertionError('fake baseline failure')
    def forbidden(*a, **kw):
        events.append('MUTATION_OR_WRITE_CALLED')
        raise AssertionError('must stop before mutation/write on nt shard')
    shard_env = {k: v.replace('${{ matrix.manh }}', '0') for k, v in J['gate-cong-cu']['steps'][7]['env'].items()}
    print('real shard env at Windows shard 0 =', shard_env, '=>', ns['_doc_che_do'](shard_env))
    print('real gate env =', J['gate']['steps'][7]['env'], '=>', ns['_doc_che_do'](J['gate']['steps'][7]['env']))
    ns.update(os=types.SimpleNamespace(environ=shard_env),
              _chay_tien_kiem=lambda fn: None, batch_behavior_test=lambda: None,
              python_alias_behavior_test=lambda: None, DOT_BIEN={'fake-mutant': None},
              _phan_manh=forbidden, _phong_con=forbidden, _ket_thuc_manh=forbidden, _van_tay=forbidden,
              _cong_tren_cay_that=forbidden)
    print('main AST, fake nt + real shard mode, real main/helpers, fake cases/prechecks; no native Windows execution:')
    for tag, cases in [('all-pass', [passed_first, passed_last]), ('one-skipped', [passed_first, skipped_middle, passed_last]), ('one-failed', [passed_first, failed_middle, passed_last]), ('all-skipped', [skipped_middle])]:
        events.clear()
        ns['CA'] = cases
        rc = ns['main']()
        print('scenario', tag, 'rc=', rc, 'events=', events)
    ns['Path'] = lambda path: types.SimpleNamespace(exists=lambda: False)
    events.clear()
    ns['CA'] = [passed_first, ns['t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi'], passed_last]
    rc = ns['main']()
    print('scenario REAL t51 absent-/bin/sh rc=', rc, 'events=', events)
    try:
        ns['t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi']()
    except ns['BoQuaMoiTruong'] as ex:
        print('REAL t51 AST + fake absent /bin/sh =>', type(ex).__name__, str(ex))
    source = (REPO / 'ops/cong_cu_test.py').read_text().splitlines()
    for first, last in ((5996, 6011), (8891, 8919)):
        for line in range(first, last + 1): print(f'{line}: {source[line-1]}')


def merger():
    job = J['gate-cong-cu-gop']
    print('needs =', job['needs'])
    print('job.if =', job['if'])
    print('matrix =', job['strategy']['matrix'])
    for oses in (['windows-latest'], ['ubuntu-latest'], ['ubuntu-latest', 'windows-latest']):
        for cancelled in (False, True):
            print('os=', oses, 'cancelled=', cancelled,
                  'job-condition(!cancelled && ubuntu in os)=', not cancelled and 'ubuntu-latest' in oses,
                  'expanded-if-forced=', expand(job['strategy']['matrix'], oses))
    for n, line in enumerate(RAW.splitlines(), 1):
        if 582 <= n <= 598: print(f'{n}: {line}')
    print('Measured: YAML condition false and forced matrix empty for windows-only.')
    print('NOT MEASURED: GitHub server job.if-before-matrix scheduling, actual skipped state/run ID/attempt/runner.')
    print('Reasoned expectation: job.if evaluated before strategy.matrix means skipped; exclude alone does not prove skipped.')


def census():
    for name, job in J.items():
        matrix = job.get('strategy', {}).get('matrix')
        print(name, json.dumps({'runs-on': job.get('runs-on'), 'needs': job.get('needs'), 'job.if': job.get('if'), 'matrix': matrix, 'windows-only matrix rows': expand(matrix, ['windows-latest'])}, ensure_ascii=False))
    print('Job definitions:', len(J), '; gate* definitions:', sum(name.startswith('gate') for name in J))
    print('windows-only includes fixed Ubuntu chuan-bi; input removes Ubuntu MATRIX rows only.')
    print('Declared job rows are not evidence of an allocated Windows runner or completed steps.')


def steps():
    root = yaml.compose(RAW)
    jobs = next(v for k, v in root.value if k.value == 'jobs')
    runner = []
    matrix = []
    all_shells = {}
    all_coe = []
    os_refs = []
    for jobnode, job in jobs.value:
        jobname = jobnode.value
        stepseq = next((v for k, v in job.value if k.value == 'steps'), None)
        if stepseq is None: continue
        for i, stepnode in enumerate(stepseq.value):
            step = J[jobname]['steps'][i]
            cond = str(step.get('if', ''))
            line = stepnode.start_mark.line + 1
            row = [jobname, i + 1, line, step.get('name', step.get('uses')), cond]
            if re.search(r'runner\s*(?:\.\s*os|\[\s*[\'"]os[\'"]\s*\])', cond, re.I): runner.append(row)
            if re.search(r'matrix\s*(?:\.\s*os|\[\s*[\'"]os[\'"]\s*\])', cond, re.I): matrix.append(row)
            shell = str(step.get('shell', '(runner default)'))
            all_shells[shell] = all_shells.get(shell, 0) + 1
            if 'continue-on-error' in step: all_coe.append([jobname, i + 1, step['continue-on-error'], cond])
            if re.search(r'(RUNNER_OS|runner\s*[.\[]|matrix\s*[.\[]|Windows|windows-latest)', json.dumps(step, ensure_ascii=False)):
                os_refs.append(row)
    print('step if runner.os count =', len(runner))
    for row in runner: print(json.dumps(row, ensure_ascii=False))
    print('step if matrix.os =', matrix)
    print('shell census =', all_shells)
    print('continue-on-error =', all_coe)
    print('all step OS references (including script/env/name) =')
    for row in os_refs: print(json.dumps(row, ensure_ascii=False))
    print('raw OS/alternate-syntax references:')
    for line, text in enumerate(RAW.splitlines(), 1):
        if re.search(r'runner\s*[.\[]|matrix\s*[.\[]|RUNNER_OS|continue-on-error|^\s*shell:', text, re.I): print(f'{line}: {text}')
    print('Explicit bash/pwsh chooses interpreter; no implicit Windows skip inferred from shell choice.')


def git(*args):
    r = subprocess.run(['git', *args], cwd=REPO, text=True, capture_output=True)
    print('$ git', ' '.join(args))
    print(r.stdout + r.stderr, end='')
    print('rc=', r.returncode)
    return r


def history():
    for sha in ('5585abe', '747f983', 'be00ef7', 'e63961f', '8d5cccb'):
        git('show', '--no-patch', '--format=%H%n%aI%n%s%n%b', sha)
    for sha in ('5585abe', 'be00ef7'):
        git('merge-base', '--is-ancestor', sha, 'e63961f')
        git('show', '--format=', sha, '--', '.github/workflows/ci.yml')
    for path in ('.github/workflows/ci.yml', 'ops/cong_cu_test.py'):
        print('base and reviewed blobs', path)
        git('rev-parse', 'e63961f:' + path, 'HEAD:' + path)
    print('No local exact-run receipt found under filenames wp878/wp879/pr880/pr883; commit comments are source claims, not independent Actions runtime evidence.')


def show_lines(path, first, last):
    print(path)
    for n, line in enumerate((REPO / path).read_text().splitlines(), 1):
        if first <= n <= last: print(f'{n}: {line}')


def contradictions():
    show_lines('CLAUDE.md', 156, 198)
    show_lines('CLAUDE.md', 810, 821)
    show_lines('CLAUDE.md', 914, 917)
    print('Every manual/two-platform phrase in CLAUDE.md:')
    for n, line in enumerate((REPO / 'CLAUDE.md').read_text().splitlines(), 1):
        if re.search(r'workflow_dispatch|gọi tay|hai nền', line): print(f'{n}: {line}')
    ev = evaluator()
    historic = yaml.safe_load(subprocess.check_output(['git', 'show', '9e9a74b:.github/workflows/ci.yml'], cwd=REPO, text=True))
    print('9e9a74b real dispatch os =', ev(historic['jobs']['chuan-bi']['outputs']['os'], dict(event_name='workflow_dispatch')))
    for first, last in ((880, 893), (950, 959), (968, 985)):
        show_lines('docs/PROTOCOL_DA_PHIEN.md', first, last)
    show_lines('docs/adr/0049-cong-hai-nen-truoc-phat-hanh-khong-phai-moi-lan-land.md', 1, 60)
    launcher = yaml.safe_load((REPO / '.github/workflows/launcher-windows.yml').read_text())
    print('launcher pull_request trigger =', launcher.get('on', launcher.get(True))['pull_request'])
    print('launcher job.if =', launcher['jobs']['launcher']['if'])
    print('c) old two-platform claim is explicitly dated 22-10 at 9e9a74b; new lines supersede it, not an unconditional present-day claim.')
    print('No OTHER unconditional "manual dispatch => two platforms" statement found in CLAUDE.md.')
    print('API-only-platform lesson is historical; labeled launcher exists; platform-specific cloud lesson agrees that different OS coverage is not interchangeable.')
    print('Protocol distinguishes skipped/not_measured from passed: baseline skipped cases must remain explicit (finding). ADR-0049 does not say dispatch Windows replaces local release gates.')


def provenance():
    print('All cong_cu_test.py workflow invocations and their mode env:')
    for name, job in J.items():
        for s in job.get('steps', []):
            if 'ops/cong_cu_test.py' in str(s.get('run', '')):
                print(name, 'step=', s.get('name'), 'step.if=', s.get('if'), 'env=', s.get('env'), 'run=', repr(s.get('run')))
    print('Main gate checkout (real YAML):')
    for s in J['gate']['steps']:
        if str(s.get('uses', '')).startswith('actions/checkout'):
            print(json.dumps(s, ensure_ascii=False))
    show_lines('.github/workflows/ci.yml', 130, 148)
    show_lines('.github/workflows/ci.yml', 284, 318)
    show_lines('.github/workflows/ci.yml', 864, 869)
    print('gate-nhanh-manh has Windows rows and targeted mutants: "no mutation radius" in the new text is scoped to cong_cu_test, not every mutation test in the repository.')
    print('Same PR branch head alone does not establish same tested checkout: PR may test synthetic merge; dispatch tests selected ref. Need exact checkout/head/tree/runtime evidence per protocol 10.2.2.')
    print('No current native Windows execution, GitHub API jobs/logs, actual Ubuntu mutant killing, or exact paired-run provenance was measured here (offline read-only review).')


MODES = {
    'expression': (1, 'Ba nhánh outputs.os và mặc định runner_set', expression, 'KHÔNG PHẢI LỖI: ma trận đo khớp; windows-only không bao gồm các job ma trận Ubuntu, không loại job chuan-bi Ubuntu cố định.'),
    'windows': (2, 'Mảnh Windows, vị từ và luồng ca nền', windows, 'LỖI: main vẫn có thể xanh khi một ca nền BoQuaMoiTruong, nên không chứng minh mọi ca nền đã đạt; chi tiết finding bên dưới. Không phóng vòng đột biến ở nhánh nt/manh.'),
    'merger': (3, 'Gom Ubuntu, ma trận rỗng và skip', merger, 'KHÔNG ĐO ĐƯỢC trạng thái GitHub thực. Điều kiện YAML false với windows-only; theo thứ tự job.if trước matrix thì dự kiến skipped; exclude riêng lẻ tạo ma trận rỗng, không đủ để gọi skipped.'),
    'census': (4, 'Toàn bộ job, matrix, exclude và job.if', census, 'KHÔNG PHẢI LỖI ở MỨC KHAI BÁO JOB: ngoài gate-cong-cu-gop, mọi gate* có hàng Windows; vẫn phụ thuộc chuan-bi/thành công dependency/hủy. Không nhận hàng matrix là bằng chứng thực thi.'),
    'steps': (5, 'Kiểm đếm step.if và đường bỏ qua khác', steps, 'KHÔNG PHẢI LỖI: đúng 6 step.if theo runner.os, gồm 2 biểu thức bọc ${{ }}; không có step.if theo matrix.os, không có continue-on-error riêng cho Windows. shell bash/pwsh không tự bỏ bước Windows.'),
    'history': (6, 'Truy nguồn SHA, packet #878/#879 và chú thích', history, 'KHÔNG PHẢI LỖI: commit #878/#879 đều là tổ tiên e63961f; lời trích đúng commit/chú thích và workflow/code không đổi từ base tới reviewed_sha. Không lấy chú thích skipped làm bằng chứng runtime.'),
    'contradictions': (7, 'Đối chiếu doctrine, lời khai cũ và ADR-0049', contradictions, 'LỖI về phạm vi ca nền đạt như HƯỚNG 2 (cùng một finding); không tạo finding cho lời khai lịch sử có neo ngày/SHA, không thấy câu gọi tay => hai nền vô điều kiện khác. Quy tắc cùng SHA/hai nền trước phát hành vẫn giữ.'),
    'provenance': (10, 'Phạm vi bán kính, default checkout và cùng head', provenance, 'KHÔNG PHẢI LỖI ở yêu cầu cùng head và giới hạn cong_cu; cần checkout identity để áp dụng. KHÔNG ĐO ĐƯỢC kết quả Windows/Ubuntu thật hay paired-run identity trên reviewed_sha.'),
}


def run(mode):
    number, title, fn, conclusion = MODES[mode]
    output = io.StringIO()
    with contextlib.redirect_stdout(output): fn()
    text = output.getvalue()
    (ROOT / 'evidence' / f'{number:02}-{mode}.txt').write_text(text + 'probe_rc=0\n')
    with (ROOT / 'VERDICT.md').open('a') as report:
        report.write(f'HƯỚNG {number}: {title}\n\n  giả thuyết : Đối chiếu trực tiếp khẳng định trong 9 dòng mới với cấu hình và mã tại reviewed_sha.\n  lệnh       : từ cay-kho/: `python3 -B ../audit_review.py {mode}`\n  output     :\n\n```text\n{text}probe_rc=0\n```\n\n  kết luận   : {conclusion}\n\n')
    print(text, end='')


if __name__ == '__main__':
    run(sys.argv[1])
