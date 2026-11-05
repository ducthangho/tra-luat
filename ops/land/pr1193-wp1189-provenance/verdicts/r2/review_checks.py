"""Offline measurements; writes evidence only in the review directory."""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

import yaml

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'cay-kho'
EVIDENCE = ROOT / 'review-evidence'
EVIDENCE.mkdir(exist_ok=True)
BASE = '1f0941e9bba1d1d517eda4174167b81963c06bd5'
PREV = '3ca0da3b94a3078199ca8712bc26aa3b04009226'
HEAD = 'd5d3c8ffc021db8a99c366c7520b4f063cd27ab8'
WF = '.github/workflows/ops-publish-lease.yml'
PYBIN = ROOT.parent / 'py312/bin'
ENV = dict(os.environ, PATH=f'{PYBIN}:/root/.local/bin:' + os.environ['PATH'],
           PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1', GIT_OPTIONAL_LOCKS='0')


def git(*args):
    return subprocess.check_output(['git', '--no-optional-locks', '-C', str(REPO), *args], env=ENV)


def record(id_, command, rc, result, status=None, **extra):
    report_path = ROOT / 'VERDICT.md'
    report = yaml.safe_load(report_path.read_text())
    item = dict(id=id_, lenh=command, rc=rc, trang_thai=status or ('passed' if rc == 0 else 'failed'),
                ket_qua=result, **extra)
    report['phep_do'].append(item)
    report_path.write_text(yaml.safe_dump(report, allow_unicode=True, sort_keys=False), encoding='utf-8')
    print(yaml.safe_dump(item, allow_unicode=True, sort_keys=False), flush=True)


def command(id_, argv, cwd=ROOT, positive=None):
    start = time.monotonic()
    with (EVIDENCE / f'{id_}.log').open('w', encoding='utf-8') as log:
        p = subprocess.run(argv, cwd=cwd, env=ENV, stdout=log, stderr=subprocess.STDOUT)
    output = (EVIDENCE / f'{id_}.log').read_text(encoding='utf-8', errors='replace')
    status = 'passed' if p.returncode == 0 else 'failed'
    result = output.strip() or 'Không có diagnostic.'
    if positive:
        matches = list(re.finditer(positive, output))
        ok = p.returncode == 0 and len(matches) == 1
        if matches:
            m = matches[-1]
            ok = ok and int(m['ok']) == int(m['total']) > 0 and int(m['skip']) == 0
            if 'run' in m.groupdict():
                ok = ok and int(m['run']) == int(m['total'])
            result = m.group(0)
        else:
            result = output[-4000:]
        status = 'passed' if ok else 'failed'
    record(id_, shlex.join(map(str, argv)), p.returncode, result, status,
           cwd=str(cwd), giay=round(time.monotonic() - start, 3), log=f'review-evidence/{id_}.log')
    return p.returncode == 0 and status == 'passed'


def snapshot():
    files = {}
    dirs = []
    for p in sorted(REPO.rglob('*')):
        name = p.relative_to(REPO).as_posix()
        if p.is_symlink():
            files[name] = {'symlink': os.readlink(p)}
        elif p.is_file():
            files[name] = {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'mode': p.stat().st_mode}
        elif p.is_dir():
            dirs.append(name)
    return {'files': files, 'dirs': dirs}


def preflight():
    initial = snapshot()
    (EVIDENCE / 'snapshot-initial.json').write_text(json.dumps(initial, sort_keys=True))
    head = git('rev-parse', 'HEAD').decode().strip()
    tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
    status = git('status', '--porcelain=v1', '--untracked-files=all', '--ignored').decode()
    spec_hash = hashlib.sha256((ROOT / 'SPEC.md').read_bytes()).hexdigest()
    lease = yaml.safe_load((ROOT / 'LEASE.yaml').read_text())
    assert head == HEAD and git('rev-parse', BASE).decode().strip() == BASE
    assert spec_hash == '8f4f89a1414fd009f5a16be358925332c6c576a132710f5819e5cce7e778f5ce'
    assert spec_hash == lease['spec_sha256'] == lease['spec_hash']
    assert (lease['packet_id'], lease['revision'], lease['generation']) == ('LEASE-PUBLISH-GHIM-PYTHON', 1, 1)
    assert lease['base_sha'] == lease['immutable_acceptance_baseline'] == BASE
    assert lease['effective_review_class'] == lease['review_class'] == 'sensitive'
    assert lease['reviewer_provider'] == 'openai_codex'
    assert sorted(lease['write_set']) == [WF, 'ops/handoff/wp1189-g1-claude.md']
    assert hashlib.sha256(('\n'.join(sorted(lease['write_set']))+'\n').encode()).hexdigest() == lease['write_set_hash']
    assert datetime.now(timezone.utc) < datetime.fromisoformat(lease['lease_expires_at_utc'])
    assert not status, repr(status)
    assert git('diff', '--no-ext-diff', '--no-textconv', BASE, HEAD) == (ROOT/'diff.patch').read_bytes()
    assert git('diff', '--no-ext-diff', '--no-textconv', PREV, HEAD) == (ROOT/'delta_luot1_luot2.patch').read_bytes()
    assert (REPO/WF).read_bytes() == git('show', f'{HEAD}:{WF}')
    record('preflight', 'PY312 -B review_checks.py preflight; git rev-parse/status/diff; sha256sum SPEC.md', 0,
           f'HEAD={head}; tree={tree}; SPEC sha256={spec_hash}; r1/g1, lease còn hạn, sensitive, write_set_hash và hai patch khớp; status sạch; snapshot {len(initial["files"])} tệp.',
           base_sha=BASE, reviewed_tree=tree)


def static():
    prior = git('show', f'{PREV}:{WF}').decode()
    current = git('show', f'{HEAD}:{WF}').decode()
    base = yaml.safe_load(git('show', f'{BASE}:{WF}'))
    old = yaml.safe_load(prior)
    new = yaml.safe_load(current)
    assert old == new
    names = git('diff', '--name-only', PREV, HEAD).decode().splitlines()
    assert names == [WF]
    import difflib
    delta = list(difflib.ndiff(prior.splitlines(), current.splitlines()))
    changed = [x for x in delta if x[:2] in ('+ ', '- ')]
    assert len(changed) == 4 and all(x[2:].lstrip().startswith('#') for x in changed)
    inserted = [x[2:] for x in changed if x.startswith('+ ')]
    assert all('${{' not in x for x in inserted)
    assert 'bản trên runner chưa đo, A6' in '\n'.join(inserted)
    steps = new['jobs']['dang']['steps']
    idx = [i for i, s in enumerate(steps) if str(s.get('uses', '')).startswith('actions/setup-python@')]
    assert len(idx) == 1
    i = idx[0]
    assert steps[i] == {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}
    assert i == 1 and steps[i-1]['uses'] == 'actions/checkout@v4'
    assert steps[i+1]['name'] == 'cài PyYAML'
    py = [n for n, s in enumerate(steps) if 'python3' in str(s.get('run', ''))]
    assert py and all(n > i for n in py)
    restored = copy.deepcopy(new)
    del restored['jobs']['dang']['steps'][i]
    assert restored == base
    ci = yaml.safe_load((REPO/'.github/workflows/ci.yml').read_text())
    ci_py = [s for j in ci['jobs'].values() for s in j.get('steps', [])
             if str(s.get('uses', '')).startswith('actions/setup-python@')]
    assert len(ci_py) == 8
    assert all(s['uses'] == 'actions/setup-python@v5' and s['with']['python-version'] == '3.12' for s in ci_py)
    new_comments = [x[1:] for x in (ROOT/'diff.patch').read_text().splitlines() if x.startswith('+') and not x.startswith('+++') and x[1:].lstrip().startswith('#')]
    assert not any('${{' in x for x in new_comments)
    result = {'yaml_safe_load_luot1_equals_luot2': True, 'delta_changed_lines': changed,
              'Actions_expression_in_new_comments': False, 'setup_index': i,
              'python3_run_indices': py, 'remove_setup_equals_base': True,
              'ci_setup_python_matching': len(ci_py)}
    (EVIDENCE/'static.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    record('delta_F1_static', 'PY312 -B review_checks.py static (git show hai SHA + yaml.safe_load + diff từng dòng)', 0,
           result, log='review-evidence/static.json')
    report_path = ROOT/'VERDICT.md'
    report = yaml.safe_load(report_path.read_text())
    report['findings'] = [dict(id='F1', severity='P3', trang_thai='closed',
        tep_dong=f'{WF}:74', mo_ta='Đã bỏ khẳng định Python hệ điều hành của runner là 3.14; chú thích tách kết quả tái hiện tại chỗ 3.13/3.14 khỏi bản trên runner chưa đo (A6), khớp SPEC §1 S4 và §7. Không có biểu thức Actions trong chú thích mới.',
        bang_chung='review-evidence/static.json; yaml.safe_load(lượt 1) == yaml.safe_load(lượt 2); delta đúng hai dòng bỏ/hai dòng thêm và đều là chú thích.')]
    report_path.write_text(yaml.safe_dump(report, allow_unicode=True, sort_keys=False), encoding='utf-8')


def gates():
    checks = [
        command('python_tools', ['python3', '-c', "import sys,yaml,shutil; print(sys.executable); print(sys.version); print('PyYAML='+yaml.__version__); print('python='+str(shutil.which('python'))); print('python3='+str(shutil.which('python3'))); print('actionlint='+str(shutil.which('actionlint'))); print('shellcheck='+str(shutil.which('shellcheck'))); assert sys.version_info[:2]==(3,12); assert yaml.__version__=='6.0.3'; assert shutil.which('actionlint'); assert shutil.which('shellcheck')"]),
        command('A1', [str(PYBIN/'python'), 'a1_check.py', 'cay-kho/'+WF]),
        command('A3_tools', ['shellcheck', '--version']),
        command('A3_actionlint_version', ['actionlint', '-version']),
        command('A3', ['actionlint', 'cay-kho/'+WF]),
        command('A4', ['git', 'diff', '--numstat', BASE, HEAD], cwd=REPO),
        command('A5_diff_check', ['git', 'diff', '--check', BASE, HEAD], cwd=REPO),
    ]
    numstat = git('diff', '--numstat', BASE, HEAD).decode()
    assert numstat == (ROOT/'numstat.txt').read_text() == f'8\t0\t{WF}\n'
    assert all(checks)


def a2():
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    ok = command('A2', ['python3', 'ops/lease_publish_test.py'], cwd=REPO,
                 positive=r'(?m)^lease_publish: (?P<ok>\d+)/(?P<total>\d+) đạt; đã chạy=(?P<run>\d+), bỏ qua=(?P<skip>\d+)[ \t\r]*$')
    if not ok:
        raise SystemExit(1)


def context():
    import ast
    from urllib.parse import urlsplit
    branch = git('branch', '--show-current').decode().strip() or 'DETACHED (review snapshot)'
    remote = git('remote', 'get-url', 'origin').decode().strip()
    parsed = urlsplit(remote)
    public_remote = (parsed.hostname or '') + parsed.path if parsed.scheme else remote
    result = dict(branch=branch, root_commit=git('rev-list', '--max-parents=0', 'HEAD').decode().strip(),
                  remote_without_credentials=public_remote, git_dir=git('rev-parse', '--git-dir').decode().strip(),
                  core_abbrev=git('config', '--get', 'core.abbrev').decode().strip())
    assert result['core_abbrev'] == '7'
    record('repository_context', 'PY312 -B review_checks.py context; git branch --show-current/rev-list/remote/rev-parse/config', 0, result)
    nonstdlib = set()
    for path in ('ops/lease_publish.py', 'ops/lease_publish_test.py', 'ops/bash_nen.py'):
        for node in ast.walk(ast.parse((REPO/path).read_text())):
            if isinstance(node, ast.Import):
                names = [a.name.split('.')[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [(node.module or '').split('.')[0]]
            else:
                continue
            nonstdlib.update(x for x in names if x and x not in sys.stdlib_module_names)
    record('dependency_scan', 'PY312 -B review_checks.py context (ast.walk các import của lease_publish.py/test.py/bash_nen.py)', 0,
           f'Import ngoài stdlib: {sorted(nonstdlib)}. bash_nen là module nội bộ; PyYAML==6.0.3 được cài qua python3 -m pip sau bước setup.')


def a2_evidence():
    output = (EVIDENCE/'A2.log').read_text(encoding='utf-8')
    totals = list(re.finditer(r'(?m)^lease_publish: (\d+)/(\d+) đạt; đã chạy=(\d+), bỏ qua=(\d+)[ \t\r]*$', output))
    assert len(totals) == 1
    total = tuple(map(int, totals[0].groups()))
    assert total[0] == total[1] == total[2] > 0 and total[3] == 0
    entries = re.findall(r'(?m)^>>> vao (\S+) ', output)
    exits = re.findall(r'(?m)^<<< ra (\S+) [0-9.]+s (\S+)$', output)
    assert len(entries) == len(exits) == total[0] and len(set(entries)) == len(entries)
    assert entries == [x[0] for x in exits] and all(x[1] == 'QUA' for x in exits)
    specific = [x[0] for x in exits if x[0].startswith(('t24_', 't33_', 't125_', 't191_'))]
    assert len(specific) == 4
    record('A2_positive_evidence', 'PY312 -B review_checks.py a2_evidence (đọc tổng kết neo đầu dòng và marker toàn suite)', 0,
           dict(tong_ket=totals[0].group(0), vao=len(entries), ra_QUA=len(exits), ca_bat_buoc_QUA=specific), log='review-evidence/A2.log')


def final_snapshot():
    initial = json.loads((EVIDENCE/'snapshot-initial.json').read_text())
    current = snapshot()
    (EVIDENCE/'snapshot-final.json').write_text(json.dumps(current, sort_keys=True))
    changes = [p for p in sorted(set(initial['files']) | set(current['files']))
               if initial['files'].get(p) != current['files'].get(p)]
    assert not changes, changes
    assert initial['dirs'] == current['dirs']
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert not git('status', '--porcelain=v1', '--untracked-files=all', '--ignored')
    record('read_only_final', 'PY312 -B review_checks.py final_snapshot; git status --porcelain=v1 --untracked-files=all --ignored', 0,
           f'{len(current["files"])} tệp, gồm .git và tracked/untracked/ignored, giữ nguyên hash/mode/symlink; danh sách thư mục, HEAD và status không đổi ở hai mốc.', log='review-evidence/snapshot-final.json')


if __name__ == '__main__':
    {'preflight': preflight, 'static': static, 'gates': gates, 'A2': a2,
     'context': context, 'a2_evidence': a2_evidence, 'final_snapshot': final_snapshot}[sys.argv[1]]()
