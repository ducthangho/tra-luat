#!/usr/bin/env python3
"""Read-only probes; run from cay-kho; append actual evidence outside checkout."""
import ast
import collections
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys

SHA = '06a50c5feea77c2654f31edd26efeed7eeee62f5'
OUT = Path(__file__).resolve().parent
ROWS = []

def git(*args):
    return subprocess.check_output(['git', *args], text=True)

def blob(path, rev=SHA):
    return git('show', f'{rev}:{path}')

def yaml_at(path, rev=SHA):
    import yaml
    return yaml.safe_load(blob(path, rev))

def row(claim, stated, measured, match='Có'):
    ROWS.append((claim, stated, measured, match))

def snapshot():
    root = Path.cwd()
    files = {}
    for base, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d != '.git')
        for name in sorted(names):
            p = Path(base) / name
            key = str(p.relative_to(root))
            files[key] = ('symlink:' + os.readlink(p)) if p.is_symlink() else hashlib.sha256(p.read_bytes()).hexdigest()
    for rel in ('.git/HEAD', '.git/index', '.git/config', '.git/packed-refs'):
        p = root / rel
        if p.is_file():
            files[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return {'head': git('rev-parse', 'HEAD').strip(), 'tree': git('rev-parse', 'HEAD^{tree}').strip(),
            'status': git('status', '--porcelain=v1', '--untracked-files=all', '--ignored'),
            'diff': git('diff', '--binary'), 'cached_diff': git('diff', '--cached', '--binary'), 'files': files}

def preflight():
    snap = snapshot()
    (OUT / 'review-snapshot-before.json').write_text(json.dumps(snap, ensure_ascii=False, indent=2))
    print('HEAD=' + snap['head'])
    print('tree=' + snap['tree'])
    print('is_shallow=' + git('rev-parse', '--is-shallow-repository').strip())
    print('core.abbrev=' + git('config', '--get', 'core.abbrev').strip())
    print('status_with_ignored=' + repr(snap['status']))
    print('snapshot_hashed_files=' + str(len(snap['files'])))
    diff = git('diff', '9e9a74b', SHA, '--', 'CLAUDE.md')
    provided = (OUT / 'diff.patch').read_text()
    print('provided_diff_matches_exact_SHA=' + str(diff == provided))
    print('numstat=' + git('diff', '--numstat', '9e9a74b', SHA).strip())
    print('HEAD_message=' + git('show', '-s', '--format=%s', SHA).strip())
    assert snap['head'] == SHA and not snap['status'] and diff == provided
    row('Đối tượng review và diff', '06a50c5…; base 9e9a74b; CLAUDE.md +21/-9', 'preflight: HEAD/tree, cây đầy đủ, diff byte-match, numstat 21/9')

def evaluator(rev=SHA):
    source = blob('ops/lease_publish_test.py', rev)
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_danh_gia_bieu_thuc_chuan_bi')
    exact = ast.get_source_segment(source, node)
    namespace = {'re': re}
    exec(compile(exact, f'{rev}:ops/lease_publish_test.py:{node.lineno}', 'exec'), namespace)
    return exact, namespace[node.name]

def matrix():
    exact, fn = evaluator()
    (OUT / 'extracted-evaluator.py').write_text(exact + '\n')
    print('AST_EXTRACTED_FUNCTION_BEGIN\n' + exact + '\nAST_EXTRACTED_FUNCTION_END')
    data = yaml_at('.github/workflows/ci.yml')
    expr = data['jobs']['chuan-bi']['outputs']['os']
    print('REAL_EXPRESSION=' + repr(expr))
    old_expr = yaml_at('.github/workflows/ci.yml', '9e9a74b')['jobs']['chuan-bi']['outputs']['os']
    print('expression_same_as_9e9a74b=' + str(expr == old_expr))
    cases = [
        ('push master', 'push', 'refs/heads/master', []),
        ('PR thường', 'pull_request', 'refs/pull/870/merge', ['docs']),
        ('PR windows', 'pull_request', 'refs/pull/870/merge', ['windows']),
        ('dispatch master', 'workflow_dispatch', 'refs/heads/master', []),
        ('dispatch feature', 'workflow_dispatch', 'refs/heads/review-probe', []),
        ('PR nhãn khác', 'pull_request', 'refs/pull/870/merge', ['windows-other'])]
    for name, event, ref, labels in cases:
        ctx = dict(event_name=event, ref=ref, labels=labels)
        result = fn(expr, ctx)
        print(name + ': ' + json.dumps(ctx, ensure_ascii=False) + ' => ' + json.dumps(result))
        expected = ['ubuntu-latest', 'windows-latest'] if event == 'workflow_dispatch' or 'windows' in labels else ['ubuntu-latest']
        assert result == expected
    for job, spec in data['jobs'].items():
        print(f'ci_job={job}; runs-on={spec.get("runs-on")}; matrix={json.dumps(spec.get("strategy", {}).get("matrix", {}), ensure_ascii=False)}')
    row('outputs.os: push master / PR thường', '[ubuntu-latest]', 'matrix: cả hai ca = [ubuntu-latest]')
    row('outputs.os: PR nhãn windows / workflow_dispatch', '[ubuntu-latest, windows-latest]', 'matrix: PR windows, dispatch master và dispatch feature đều đúng')
    row('Mốc đo 22-10-2026 trên 9e9a74b', 'Cùng biểu thức tại head review', 'matrix: expression_same_as_9e9a74b=True; ngày commit head = 22-10-2026')
    row('P2 cũ master-windows-bo-sot-dispatch', 'Giới hạn vào Windows tự động khi push master', 'matrix: push master một OS, dispatch master hai OS; câu hệ quả giới hạn PR/push')

def readback():
    prefix = 'ops/land/pr848-wp744-provenance/'
    data = json.loads(blob(prefix + 'readback-jobs-39354156843.json'))
    jobs = data['jobs']
    print('total_count=' + str(data['total_count']) + '; len(jobs)=' + str(len(jobs)))
    print('unique_job_ids=' + str(len({j['id'] for j in jobs})))
    print('labels=' + repr(dict(collections.Counter(tuple(j['labels']) for j in jobs))))
    print('conclusions=' + repr(dict(collections.Counter(j['conclusion'] for j in jobs))))
    print('windows_labels=' + str(sum(any('windows' in s.lower() for s in j['labels']) for j in jobs)))
    for key in ('run_id', 'head_sha', 'head_branch', 'workflow_name', 'run_attempt'):
        print(key + '=' + repr(sorted({j[key] for j in jobs})))
    run = json.loads(blob(prefix + 'readback-run-39354156843.json'))
    print('run_metadata=' + json.dumps({k: run.get(k) for k in ('id', 'path', 'event', 'head_sha', 'head_branch', 'created_at', 'run_started_at', 'conclusion', 'run_attempt')}, ensure_ascii=False))
    for j in jobs:
        print(f'{j["id"]}: {j["name"]}: {j["labels"]}: {j["conclusion"]}')
    assert data['total_count'] == len(jobs) == 23
    assert all(j['labels'] == ['ubuntu-latest'] for j in jobs)
    row('Run 39354156843', '23 job; 23 nhãn ubuntu-latest; 0 Windows', 'readback: total_count=len=unique_ids=23; labels {(ubuntu-latest,):23}; Windows=0')
    row('Run: workflow, event, SHA, ngày', 'ci.yml; push master; 3a3a3ca; 20-10-2026', 'readback: metadata path=.github/workflows/ci.yml; event=push; head_branch=master; 3a3a3caca5de4934ff53851feb6994c2c7b84ad5; 2026-10-20')

def launcher():
    data = yaml_at('.github/workflows/launcher-windows.yml')
    events = data.get('on', data.get(True))
    print('launcher_events=' + json.dumps(events, ensure_ascii=False))
    job = data['jobs']['launcher']
    print('launcher_if=' + job['if'])
    print('launcher_matrix=' + job['strategy']['matrix']['os'])
    print('launcher_runs_on=' + job['runs-on'])
    for step in job['steps']:
        if 'run' in step:
            print('step=' + step.get('name', '') + '; run_first=' + step['run'].splitlines()[0])
    assert events['push']['branches'] == ['master']
    assert events['push']['paths'] == ['.claude/dev/**', '.github/workflows/launcher-windows.yml']
    assert events['pull_request']['types'] == ['opened', 'synchronize', 'reopened', 'labeled']
    assert events['pull_request']['paths'] == ['.claude/dev/**']
    # Evaluate the exact two-way matrix expression, rejecting unfamiliar syntax.
    expr = job['strategy']['matrix']['os']
    found = re.fullmatch(r"\$\{\{ fromJSON\(github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only' && '([^']+)' \|\| '([^']+)'\) \}\}", expr)
    assert found, expr
    for event, inputs in [('push', None), ('pull_request', None), ('workflow_dispatch', 'windows-only'), ('workflow_dispatch', 'windows-and-ubuntu')]:
        result = json.loads(found.group(1 if event == 'workflow_dispatch' and inputs == 'windows-only' else 2))
        print(f'launcher {event} runner_set={inputs}: {result}')
    row('Windows tự động khi push master', 'launcher-windows.yml; paths .claude/dev/** hoặc chính workflow', 'launcher: push.branches=[master]; push.paths khớp cả hai path')
    row('Ma trận launcher cho push/PR', 'windows-latest + ubuntu-latest', 'launcher: push và pull_request hai OS; dispatch mặc định windows-only (phạm vi riêng)')
    row('Launcher: PR nhãn windows và labeled', 'Job chỉ chạy nếu PR có nhãn; types chứa labeled', 'launcher: if và types khớp; PR còn lọc paths=.claude/dev/**')
    row('Launcher chỉ đo lane launcher', 'KHÔNG phải gate ci.yml', 'launcher: liệt kê toàn bộ run; doctor, launcher_test, probes; không gọi battery gate của ci.yml')

def workflows():
    paths = git('ls-tree', '--name-only', SHA, '.github/workflows/').splitlines()
    print('workflow_count=' + str(len(paths)))
    extras = []
    for path in paths:
        data = yaml_at(path)
        print(path + ': events=' + repr(list(data.get('on', data.get(True, {})))))
        for name, spec in data.get('jobs', {}).items():
            print('  ' + name + ': runs-on=' + str(spec.get('runs-on')) + '; uses=' + str(spec.get('uses')) + '; matrix=' + json.dumps(spec.get('strategy', {}).get('matrix', {}), ensure_ascii=False))
            if Path(path).name not in ('ci.yml', 'launcher-windows.yml'):
                extras.append((path, name, spec.get('runs-on')))
    assert len(paths) == 7
    assert all(runner == 'ubuntu-latest' for _, _, runner in extras)
    print('other_workflows_all_ubuntu=' + str(len(extras)))
    row('Mọi workflow còn lại', 'ci-dot-bien-du và ops-* đều ubuntu-latest', f'workflows: liệt kê đủ 7 tệp tại SHA; 5 workflow còn lại, toàn bộ {len(extras)} định nghĩa job ubuntu-latest')

def events():
    data = yaml_at('.github/workflows/ci.yml')
    ev = data.get('on', data.get(True))
    print('ci_events=' + json.dumps(ev, ensure_ascii=False))
    print('pull_request_types_explicit=' + str(isinstance(ev['pull_request'], dict) and 'types' in ev['pull_request']))
    assert ev['pull_request'] is None
    step = next(s for s in data['jobs']['gate']['steps'] if s.get('name') == 'PR head contains required EOL base')
    print('EOL_step=' + json.dumps(step, ensure_ascii=False))
    condition = step['if'].strip()
    if condition.startswith('${{') and condition.endswith('}}'):
        condition = condition[3:-2].strip()
    assert condition == "github.event_name == 'pull_request'"
    jobs = json.loads(blob('ops/land/pr848-wp744-provenance/readback-jobs-39354156843.json'))['jobs']
    print('EOL_in_push_readback=' + json.dumps([(j['name'], s['name'], s['conclusion']) for j in jobs for s in j['steps'] if s['name'] == 'PR head contains required EOL base'], ensure_ascii=False))
    print('historical_PR109_commits:')
    for rev in ('05170b4', '3736fc0', '9796f67'):
        print(git('show', '-s', '--format=%H %cI %s', rev).strip())
        print('ancestor_of_reviewed=' + str(subprocess.run(['git', 'merge-base', '--is-ancestor', rev, SHA]).returncode == 0))
    for rev in ('05170b4', '3736fc0'):
        print(git('show', '--format=', rev, '--', 'CLAUDE.md'))
    row('ci.yml: mặc định pull_request, không labeled', 'Không khai types; gắn nhãn đơn thuần không sinh ci.yml run', 'events: pull_request=null, types absent; commit 3736fc0 trong PR109 đã ghi nhận cùng bẫy')
    row('Cách dùng nhãn windows', 'Cần synchronize/reopened hoặc thêm types:labeled', 'events+matrix: workflow có pull_request mặc định; evaluator đọc nhãn khi workflow được kích hoạt')
    row('EOL step trên lượt master', 'PR head contains required EOL base bị skipped', 'events: if đúng github.event_name==pull_request; readback push thực tế EOL=skipped')
    row('Hai P2 lịch sử PR109', '05170b4: điều kiện Windows; 3736fc0: labeled không kích hoạt', 'events: git show cả hai sửa và merge 9796f67 (PR109); không có raw comment reviewer trong bundle', 'Khớp sửa; comment gốc KHÔNG ĐO ĐƯỢC')

def history():
    for rev in ('3a3a3ca', '3f6c694', '9e9a74b', 'b38fce8', '06a50c5', 'd1258fe', '6d46e6f', '4ae43f0'):
        print('$ git show -s --format="%H %cI %P %s" ' + rev)
        print(git('show', '-s', '--format=%H %cI %P %s', rev).strip())
        ancestor = subprocess.run(['git', 'merge-base', '--is-ancestor', rev, SHA]).returncode
        print('ancestor_of_reviewed_SHA_rc=' + str(ancestor))
    evidence_path = 'ops/land/pr848-wp744-land-evidence.yaml'
    for rev in ('3f6c694', SHA, '4ae43f0'):
        print(f'$ git show {rev}:{evidence_path} [lọc run 39354156843]')
        for line in blob(evidence_path, rev).splitlines():
            if 'run_id: 39354156843' in line or 'r4323607674' in line:
                print(line)
    for rev in ('d1258fe', '6d46e6f'):
        print('$ git show --format=short ' + rev + ' -- .github/workflows/ci.yml')
        print(git('show', '--format=short', rev, '--', '.github/workflows/ci.yml'))
    print('independent_comment_readback_at_reviewed_SHA:')
    grep = subprocess.run(['git', 'grep', '-n', '-I', '-e', '4323607674', SHA, '--', ':!CLAUDE.md'], text=True, capture_output=True)
    print('git grep -n -I -e 4323607674 SHA -- :!CLAUDE.md rc=' + str(grep.returncode))
    print(grep.stdout or '(không có bản đọc lại độc lập của comment này trong cây review)')
    print('correction_diff_4ae43f0:')
    print(git('show', '--format=short', '4ae43f0', '--', evidence_path))
    print('LIMIT: 4ae43f0 là object sửa có trước thời điểm head, không phải ancestor của head. Không dùng nó thay nội dung HEAD. Không gọi mạng để xác minh PR865 hoặc comment r4323607674.')
    row('Commit 3a3a3ca', 'Merge PR848 ngày 20-10-2026', 'history: git show = 3a3a3caca5de4934ff53851feb6994c2c7b84ad5; hai parent; Merge pull request #848; 2026-10-20')
    row('Commit 3f6c694 trích đúng jobs', "jobs: '23/23 success (gom windows)'", 'history: git show blob tại 3f6c694 và head đều có nguyên văn trích dẫn')
    row('Packet548: tên và bỏ vế master', 'CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND', 'history: d1258fe bỏ điều kiện master ở các matrix, thêm chuan-bi; 6d46e6f sửa output thành chuỗi. Cả hai là ancestor')
    row('Codex connector P1 PR859 / r4323607674', 'Bắt lỗi khai gom windows', 'history: có commit sửa 4ae43f0 ghi cùng nguồn, nhưng git grep tại SHA không có raw comment độc lập', 'KHÔNG ĐO ĐƯỢC trực tiếp comment/actor/severity')
    row('Sửa ở PR865', 'Bản sửa gom windows', 'history: object 4ae43f0 tồn tại và đúng phép sửa, chưa là ancestor của head; không có PR readback tại SHA', 'Khớp bản sửa; số PR KHÔNG ĐO ĐƯỢC trực tiếp')

def consistency():
    for path in ('CLAUDE.md', 'docs/PROTOCOL_DA_PHIEN.md'):
        source = blob(path)
        print('FILE=' + path)
        for no, line in enumerate(source.splitlines(), 1):
            if re.search(r'windows|ubuntu|ci\.yml|workflow_dispatch', line, re.I):
                print(f'{no}: {line}')
    proto = blob('docs/PROTOCOL_DA_PHIEN.md').splitlines()
    for first, last in ((944, 981), (988, 995), (1040, 1045)):
        print(f'PROTOCOL_L{first}-{last}:')
        for no in range(first, last + 1):
            print(f'{no}: {proto[no - 1]}')
    print('INTERPRETATION: protocol yêu cầu chứng cứ theo context/OS và parity Windows–Linux khi land; không khai mọi push master tự sinh full gate Windows. Chỉ chọn runner hoặc dispatch không tự chứng minh gate đã chạy/đã pass.')
    row('Nội bộ CLAUDE.md', 'Đoạn mới không giữ doctrine mọi push master đều có Windows', 'consistency: quét toàn tệp mọi windows/ubuntu/ci.yml/dispatch; câu cũ dòng159 là trích lịch sử, launcher dòng803–811 đúng scope launcher')
    row('So với protocol', 'Phân biệt đo CI với yêu cầu gate hai nền khi land/phát hành', 'consistency: §10.2.2–10.2.4 yêu cầu identity/evidence; L1043 parity Windows–Linux là nghĩa vụ, không khai trigger push master')

def historical():
    print('PR109_original_text:')
    original = blob('CLAUDE.md', '9796f67')
    for no, line in enumerate(original.splitlines(), 1):
        if any(s in line for s in ('sáu', '14-08', 'windows', 'Windows')):
            print(f'{no}: {line}')
    print('merge_commits_14Aug_on_first_parent_of_PR109:')
    merges = git('log', '9796f67^1', '--first-parent', '--merges', '--since=2026-08-13T17:00:00Z', '--until=2026-08-14T17:00:00Z', '--format=%H').splitlines()
    for rev in reversed(merges):
        print(git('show', '-s', '--format=%h %cI %s', rev).strip())
        names = git('diff', '--name-only', rev + '^1', rev).splitlines()
        print('changed_paths=' + repr(names))
    for rev in ('9796f67', SHA):
        ci = yaml_at('.github/workflows/ci.yml', rev)
        prep = ci['jobs'].get('chuan-bi', {})
        expr = prep.get('outputs', {}).get('os') or ci['jobs']['gate']['strategy']['matrix']['os']
        print(f'ci_os_at_{rev}=' + expr)
    print('LIMIT: Git tree không lưu mọi lần dispatch, nhãn PR hoặc sáu run cụ thể của phiên 14-08. Không suy sáu merge = sáu Windows execution từ matrix. Câu sáu lần vốn có từ PR109; diff mới đặt nó vào bối cảnh lịch sử.')
    row('Đợt 14-08: khi ấy còn vế master', 'Ma trận cũ chọn Windows khi master', 'historical: ci.yml tại 9796f67 có github.ref==refs/heads/master; tại SHA review không còn')
    row('Đợt 14-08: không dùng nhãn/dispatch, sáu lần đo Windows đầu tiên', 'Sáu lần merge trong đợt', 'historical: trích nguồn PR109 và liệt kê commit/path ngày14-08; không có đủ raw run/nhãn để chứng minh số sáu và lần đầu', 'KHÔNG ĐO ĐƯỢC lịch sử execution; không coi là đã xác minh')
    row('Nay cùng tình huống không đo Windows qua ci.yml PR/push', 'Không nhãn, không dispatch thì chỉ Ubuntu', 'matrix+historical: đúng trong phạm vi ci.yml đã giới hạn ở câu hệ quả; launcher vẫn phụ thuộc path như dòng169–172')

def scope():
    old = blob('ops/reviews/pr870-review-1-codex-verdict.md', '7a2eecf')
    start = old.index('### master-windows-bo-sot-dispatch')
    end = old.index('\n## ', start)
    print('PRIOR_VERDICT_SOURCE=7a2eecf:ops/reviews/pr870-review-1-codex-verdict.md (chỉ dùng làm tài liệu lượt1, không thay cây runtime của SHA review)')
    print(old[start:end])
    print('$ git diff b38fce8 ' + SHA + ' -- CLAUDE.md')
    print(git('diff', 'b38fce8', SHA, '--', 'CLAUDE.md'))
    base = blob('CLAUDE.md', '9e9a74b')
    print('BASE_OLD_QUOTE:')
    for no, line in enumerate(base.splitlines(), 1):
        if 158 <= no <= 166:
            print(f'{no}: {line}')
    current = blob('CLAUDE.md')
    assert 'Windows tự động khi push master hiện chỉ đến từ' in current
    assert 'các lượt PR và push hậu merge\n  của `ci.yml` theo ma trận hiện tại chỉ đo Ubuntu' in current
    assert 'gate của mã đó KHÔNG BAO GIỜ' not in current
    assert 'CHỈ KHI `github.event_name' in current and 'HOẶC PR mang nhãn `windows`' in current
    print('SCOPE_FIX_ASSERTIONS=passed (cả hai vị trí của finding cũ; ngoại lệ dispatch/label vẫn còn)')
    print('AUTHOR_CAUSATION: có doctrine cũ và biên bản sai cùng tồn tại; không có transcript đủ chứng minh doctrine đã gây lời khai của executor 3f6c694.')
    print('AUTHOR_MEASUREMENT_DATE: base/head commits ngày 22-10-2026; không có transcript gốc chứng minh tác giả thực chạy phép đo vào ngày ấy.')
    row('Trích doctrine cũ', 'Bản cũ viết PR Ubuntu, master Ubuntu+Windows', 'scope: git show 9e9a74b:CLAUDE.md L158–166 xác nhận nguyên ý và điều kiện')
    row('P2 cũ: cả hai vị trí', 'Thu hẹp L169 và L173–174', 'scope: git diff b38fce8..SHA đúng hai chỗ; assertions giữ dispatch/label; matrix xác nhận phản ví dụ cũ')
    row('Doctrine cũ gây biên bản khai sai', 'Tác giả kể quan hệ nguyên nhân', 'scope+history: chứng minh văn bản và lời khai sai cùng tồn tại; không có transcript ý định executor', 'Suy luận tác giả; quan hệ nhân quả KHÔNG ĐO ĐƯỢC')
    row('Đọc nhãn thay suy từ tên event', 'Nhãn từng job cho biết nền của lượt đó', 'readback+matrix: 23 nhãn thật; cùng ref master nhưng push/dispatch chọn OS khác; chỉ là nhận định về nhãn, không chứng minh mọi gate pass')
    row('Muốn Windows gate: dispatch trên ref', 'Đường chắc chắn chọn Windows theo cấu hình', 'matrix+events: trigger dispatch tồn tại, không lọc ref trong output os; chưa chạy GitHub Actions thật')

def gate_scope():
    data = yaml_at('.github/workflows/ci.yml')
    for name, spec in data['jobs'].items():
        for step in spec.get('steps', []):
            if 'release-verify' in step.get('name', ''):
                print(name + ': ' + json.dumps({k: step.get(k) for k in ('name', 'if', 'run')}, ensure_ascii=False))
    proto = blob('docs/PROTOCOL_DA_PHIEN.md').splitlines()
    t3 = next(line for line in proto if line.startswith('| T3 |'))
    assert 'Windows + Linux' in t3
    print('PROTOCOL_T3=' + t3)
    adr = blob('docs/adr/0049-cong-hai-nen-truoc-phat-hanh-khong-phai-moi-lan-land.md')
    print('ADR0049_RELEVANT:')
    for no, line in enumerate(adr.splitlines(), 1):
        if 'ci.yml' in line or 'launcher-windows' in line or 'workflow_dispatch' in line:
            print(f'{no}: {line}')
    row('Cùng ma trận OS không có nghĩa gate PR/master giống nhau', 'Tiêu đề chỉ mô tả outputs.os', 'gate_scope: LAND release-verify vẫn if ref==master, WORKER if ref!=master; title mới chỉ khai chính sách OS chung')
    row('Protocol T3 và ADR0049', 'Không hủy nghĩa vụ gate Windows trước land/phát hành', 'gate_scope: T3 full hai nền, ADR0049 cổng deploy tại chỗ; không mâu thuẫn với trigger ci.yml hiện hành')

def sandbox_end():
    before = json.loads((OUT / 'review-snapshot-before.json').read_text())
    after = snapshot()
    (OUT / 'review-snapshot-after.json').write_text(json.dumps(after, ensure_ascii=False, indent=2))
    added = sorted(set(after['files']) - set(before['files']))
    removed = sorted(set(before['files']) - set(after['files']))
    changed = sorted(k for k in before['files'].keys() & after['files'].keys() if before['files'][k] != after['files'][k])
    for key in ('head', 'tree', 'status', 'diff', 'cached_diff'):
        print(key + '_same=' + str(before[key] == after[key]))
    print('final_HEAD=' + after['head'])
    print('final_tree=' + after['tree'])
    print('final_status_with_ignored=' + repr(after['status']))
    print('files_hashed=' + str(len(after['files'])))
    print('added=' + repr(added))
    print('removed=' + repr(removed))
    print('changed=' + repr(changed))
    print('all_snapshot_equal=' + str(before == after))
    assert before == after
    row('Checkout chỉ đọc', 'Không sửa cay-kho; không network/push', 'sandbox_end: snapshot toàn tệp + symlink + HEAD/tree/index/config + status tracked/untracked/ignored bằng nhau; 0 added/removed/changed')

def gates():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TL_CACHE_DIR=str(OUT / 'gate-cache'))
    checks = [
        ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'],
        ['python3', 'scripts/tl.py', 'doc-claims-check', '--json']]
    for args in checks:
        result = subprocess.run(args, text=True, capture_output=True, env=env)
        label = 'doctrine-scan' if 'doctrine-scan' in args else 'doc-claims-check'
        print('COMMAND=' + ' '.join(args))
        print('STDOUT:\n' + result.stdout)
        print('STDERR:\n' + result.stderr)
        print('RC=' + str(result.returncode))
        (OUT / (label + '.stdout')).write_text(result.stdout)
        (OUT / (label + '.stderr')).write_text(result.stderr)
        assert result.returncode == 0
        if label == 'doc-claims-check':
            parsed = json.loads(result.stdout)
            assert parsed['ok'] is True
            print('KẾT LUẬN doc-claims-check: passed; ok=true')
            row('Cổng doc-claims-check', 'rc=0 và ok=true', 'gates: rc=0; JSON ok=true')
        else:
            assert '0 chỗ chép doctrine' in result.stdout
            print('KẾT LUẬN doctrine-scan: passed; 0 chỗ chép doctrine')
            row('Cổng doctrine-scan', 'rc=0, sạch', 'gates: rc=0; output sạch, 0 chỗ chép doctrine')

META = {
 'preflight': (1, 'Neo exact SHA, độ đầy đủ cây và phạm vi diff', 'Diff hoặc checkout có thể không phải head được giao.', 'KHÔNG PHẢI LỖI'),
 'matrix': (2, 'Chạy nguyên evaluator trích bằng AST trên biểu thức thật', 'Có thể còn nhánh Windows bị bỏ sót; P2 cũ có thể chưa đóng.', 'KHÔNG PHẢI LỖI'),
 'readback': (3, 'Đếm readback độc lập bằng nhãn runner và định danh run', 'Số 23 hoặc nhận định không Windows có thể sai, lẫn tên job với nhãn runner.', 'KHÔNG PHẢI LỖI'),
 'launcher': (4, 'Cò, lọc path, nhãn, ma trận và phạm vi launcher', 'Launcher có thể chạy cho mọi push hoặc bị mô tả sai như full gate.', 'KHÔNG PHẢI LỖI'),
 'workflows': (5, 'Liệt kê toàn bộ workflow tại exact SHA', 'Có thể còn workflow tự chạy Windows ngoài launcher.', 'KHÔNG PHẢI LỖI'),
 'events': (6, 'Bẫy labeled, hai P2 PR109 và bước EOL skipped', 'Điều kiện trigger hoặc tên/if bước EOL có thể đã thay đổi.', 'KHÔNG PHẢI LỖI'),
 'history': (7, 'Kiểm SHA lịch sử, packet548, trích biên bản và nguồn PR859/865', 'Tên/SHA/trích dẫn có thể bịa, hoặc lời kể đã được sửa có thể vượt chứng cứ cục bộ.', 'KHÔNG ĐO ĐƯỢC'),
 'consistency': (8, 'Quét toàn CLAUDE.md và đối chiếu protocol', 'Doctrine cũ có thể còn ở chỗ khác, hoặc mô tả runtime mâu thuẫn yêu cầu gate.', 'KHÔNG PHẢI LỖI'),
 'historical': (9, 'Đối chứng đợt 14-08, sáu merge và Windows lần đầu', 'Câu lịch sử có thể đã bị biến thành lời khẳng định runtime hiện hành.', 'KHÔNG ĐO ĐƯỢC'),
 'gates': (10, 'Hai cổng bắt buộc, tách rc với bằng chứng dương', 'Tài liệu có thể bị doctrine-scan hoặc doc-claims-check bác.', 'KHÔNG PHẢI LỖI'),
 'scope': (11, 'Đóng lớp P2 cũ ở mọi vị trí và kiểm các lời giải thích', 'Bản vá có thể chỉ thay một câu, để lại diễn đạt tuyệt đối hoặc bỏ ngoại lệ.', 'KHÔNG PHẢI LỖI'),
 'gate_scope': (12, 'Cùng chính sách OS với sự khác nhau giữa gate PR và land', 'Tiêu đề mới có thể khiến quy tắc bộ bước PR và land mâu thuẫn với nhau.', 'KHÔNG PHẢI LỖI'),
 'sandbox_end': (13, 'So snapshot nội dung đầu/cuối, kể cả ignored và index', 'Phép đo có thể đã làm đổi checkout hoặc định danh SHA.', 'KHÔNG PHẢI LỖI'),
}

def main():
    os.environ['GIT_OPTIONAL_LOCKS'] = '0'
    mode = sys.argv[1]
    number, title, hypothesis, conclusion = META[mode]
    buf = io.StringIO()
    rc = 0
    try:
        with contextlib.redirect_stdout(buf):
            globals()[mode]()
    except Exception:
        import traceback
        traceback.print_exc(file=buf)
        rc = 1
        conclusion = 'KHÔNG ĐO ĐƯỢC'
    output = buf.getvalue()
    (OUT / f'evidence-{mode}.txt').write_text(output + f'rc={rc}\n')
    report = OUT / 'VERDICT.md'
    content = report.read_text()
    if ROWS:
        rendered = ''.join('| ' + ' | '.join(str(v).replace('|', '&#124;').replace('\n', ' ') for v in values) + ' |\n' for values in ROWS)
        content = content.replace('\n## BẢNG SĂN', rendered + '\n## BẢNG SĂN', 1)
    content += f'\n### HƯỚNG {number}: {title}\n\nGiả thuyết: {hypothesis}\n\nLệnh (cwd=`cay-kho/`):\n\n```bash\nPYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py {mode}\n```\n\nOutput thật:\n\n```text\n{output}rc={rc}\n```\n\nKết luận: **{conclusion}**.\n'
    report.write_text(content)
    print(output + f'rc={rc}')
    return rc

if __name__ == '__main__':
    raise SystemExit(main())
