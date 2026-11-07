import collections
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone

import yaml

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'cay-kho'
EVIDENCE = ROOT / 'review-evidence'
EVIDENCE.mkdir(exist_ok=True)
HEAD = '3b430923c88f67041ce79ce9b2f8aac0e53a28b4'
P1 = 'd5d3c8ffc021db8a99c366c7520b4f063cd27ab8'
MASTER = '5fe92c1390ca1723d19f374bd364487f013986a1'
BASE = '1f0941e9bba1d1d517eda4174167b81963c06bd5'
SPEC_HASH = '8f4f89a1414fd009f5a16be358925332c6c576a132710f5819e5cce7e778f5ce'
WF = '.github/workflows/ops-publish-lease.yml'
PYBIN = ROOT.parent / 'py312/bin'
ENV = dict(os.environ)
ENV.update(PATH=f'{PYBIN}:/root/.local/bin:' + ENV['PATH'],
           PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1', GIT_OPTIONAL_LOCKS='0')


def now():
    return datetime.now(timezone.utc).isoformat()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def verdict():
    return yaml.safe_load((ROOT / 'VERDICT.md').read_text(encoding='utf-8'))


def save(value):
    (ROOT / 'VERDICT.md').write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False,
                                                width=100), encoding='utf-8')


def record(value):
    v = verdict()
    v.setdefault('phep_do', []).append(value)
    save(v)


def run(ident, args, cwd=REPO, check=True):
    start = time.monotonic()
    log = EVIDENCE / f'{ident}.log'
    with log.open('wb') as output:
        child = subprocess.run(args, cwd=cwd, env=ENV, stdout=output, stderr=subprocess.STDOUT)
    content = log.read_text(encoding='utf-8', errors='replace')
    row = dict(id=ident, lenh=args, cwd=str(cwd), rc=child.returncode,
               trang_thai='passed' if child.returncode == 0 else 'failed',
               giay=round(time.monotonic() - start, 3), log=str(log.relative_to(ROOT)),
               ket_qua=content if len(content) < 8000 else content[-4000:])
    dump(EVIDENCE / f'{ident}.json', row)
    record(row)
    print(json.dumps({k: row[k] for k in ('id', 'rc', 'giay', 'log')}, ensure_ascii=False), flush=True)
    if check and child.returncode != 0:
        raise RuntimeError(f'{ident}: rc={child.returncode}; {content[-3000:]}')
    return content


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO, env=ENV)


def snapshot(name):
    files, dirs = {}, {}
    for parent, subdirs, names in os.walk(REPO, followlinks=False):
        for name0 in sorted(subdirs + names):
            path = Path(parent) / name0
            rel = str(path.relative_to(REPO))
            info = path.lstat()
            row = {'mode': stat.S_IMODE(info.st_mode)}
            if path.is_symlink():
                row.update(kind='symlink', target=os.readlink(path))
            elif path.is_dir():
                dirs[rel] = row
                continue
            elif path.is_file():
                row.update(kind='file', size=info.st_size,
                           sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            else:
                row['kind'] = 'special'
            files[rel] = row
    result = dict(files=files, dirs=dirs, head=git('rev-parse', 'HEAD').decode().strip(),
                  tree=git('rev-parse', 'HEAD^{tree}').decode().strip(),
                  status=git('status', '--porcelain=v1', '--untracked-files=all', '--ignored').decode())
    dump(EVIDENCE / f'snapshot-{name}.json', result)
    return result


def preflight():
    save(dict(verdict='pending', reviewed_sha=HEAD, base_sha=MASTER, patch_base_sha=BASE,
              findings=[], phep_do=[], review_axes=['spec', 'standards_security'],
              reviewer=dict(provider='openai_codex', vai_tro='Reviewer độc lập, offline lượt 3',
                            model='GPT-6 theo runtime; model ID/effort của launcher không đo độc lập',
                            execution_surface='Agent API với shell cục bộ (codex_service)',
                            transport='machine/local tools; không gọi GitHub',
                            run_nguon='scratchpad/runs/51d21cd5/prompt.snapshot'),
              bat_dau_utc=now()))
    initial_path = EVIDENCE / 'snapshot-initial.json'
    initial = json.loads(initial_path.read_text(encoding='utf-8')) if initial_path.exists() else snapshot('initial')
    assert initial['head'] == HEAD and initial['status'] == ''
    assert hashlib.sha256((ROOT / 'SPEC.md').read_bytes()).hexdigest() == SPEC_HASH
    assert git('show', '-s', '--format=%P', HEAD).decode().split() == [P1, MASTER]
    assert git('config', '--get', 'core.abbrev').decode().strip() == '7'
    assert git('cat-file', '-t', MASTER).decode().strip() == 'commit'
    record(dict(id='preflight_wrapper_initial', lenh='python -B review_checks.py preflight (bản đầu)',
                rc=1, trang_thai='failed_do_script_reviewer',
                ket_qua='Script ban đầu giả định clone có ref origin/master; git rev-parse origin/master rc=128. '
                        'Không đổi ref hoặc fetch; dùng exact master OID do prompt cung cấp và kiểm object/ancestry/tree độc lập. '
                        'Không xác minh master hiện tại trên GitHub trong review offline.'))
    run('master_ancestor', ['git', 'merge-base', '--is-ancestor', MASTER, HEAD])
    run('base_ancestor_master', ['git', 'merge-base', '--is-ancestor', BASE, MASTER])
    v = verdict()
    v['reviewed_tree'] = initial['tree']
    v['moi_truong'] = dict(PATH_them_dau=[str(PYBIN), '/root/.local/bin'],
                           bien_them={k: ENV[k] for k in ('PYTHONDONTWRITEBYTECODE', 'PYTHONUNBUFFERED', 'GIT_OPTIONAL_LOCKS')},
                           sandbox='workspace-write; cay-kho được đối xử read-only; scratch/evidence ở ngoài kho')
    save(v)
    record(dict(id='preflight', lenh='python -B review_checks.py preflight', rc=0,
                trang_thai='passed', ket_qua=dict(head=HEAD, tree=initial['tree'],
                parents=[P1, MASTER], spec_sha256=SPEC_HASH, core_abbrev=7,
                status='clean', files=len(initial['files']), dirs=len(initial['dirs'])),
                log='review-evidence/snapshot-initial.json'))


def static():
    patch1 = git('diff', '--binary', '--full-index', BASE, P1)
    patch3 = git('diff', '--binary', '--full-index', MASTER, HEAD)
    (EVIDENCE / 'measured-patch-luot2.patch').write_bytes(patch1)
    (EVIDENCE / 'measured-patch-vs-master.patch').write_bytes(patch3)
    assert patch1 == patch3
    assert git('diff', BASE, P1) == (ROOT / 'diff_luot2.patch').read_bytes()
    assert git('diff', MASTER, HEAD) == (ROOT / 'diff_vs_master.patch').read_bytes()
    assert git('merge-base', P1, MASTER).decode().strip() == BASE
    assert git('diff', '--name-only', BASE, P1).decode().splitlines() == [WF]
    assert git('rev-parse', f'{BASE}:{WF}') == git('rev-parse', f'{MASTER}:{WF}')
    # Reconstruct exactly master + the previously approved workflow blob, hashing Git trees
    # in memory. Neither an index nor Git objects are written into the reviewed repository.
    replacement = git('rev-parse', f'{P1}:{WF}').decode().strip()

    def expected_tree(oid, parts):
        entries = []
        replaced = 0
        for entry in git('ls-tree', '-z', oid).split(b'\0'):
            if not entry:
                continue
            meta, name0 = entry.split(b'\t', 1)
            mode, kind, old_oid = meta.split()
            new_oid = old_oid.decode()
            if name0.decode() == parts[0]:
                replaced += 1
                if len(parts) == 1:
                    assert kind == b'blob'
                    new_oid = replacement
                else:
                    assert kind == b'tree'
                    new_oid = expected_tree(new_oid, parts[1:])
            entries.append(f'{int(mode, 8):o}'.encode() + b' ' + name0 + b'\0' + bytes.fromhex(new_oid))
        assert replaced == 1
        raw = b''.join(entries)
        return hashlib.sha1(b'tree ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

    expected = expected_tree(MASTER, WF.split('/'))
    actual = git('rev-parse', f'{HEAD}^{{tree}}').decode().strip()
    assert expected == actual
    delta = git('diff', '--name-status', BASE, MASTER).decode().splitlines()
    assert delta and all(line.startswith('A\tops/land/') for line in delta)
    master_changes = [line.split('\t', 1)[1] for line in delta]
    (EVIDENCE / 'master-new-paths.txt').write_text('\n'.join(delta) + '\n', encoding='utf-8')
    sensitive_paths = [WF, 'ops/lease_publish.py', 'ops/lease_publish_test.py',
                       '.github/workflows/ci.yml', 'ops/bash_nen.py',
                       'ops/chay_lease_publish_test.sh', 'ops/cai_actionlint.sh']
    unchanged = {p: git('rev-parse', f'{BASE}:{p}') == git('rev-parse', f'{MASTER}:{p}')
                 for p in sensitive_paths}
    assert all(unchanged.values())
    old = yaml.safe_load(git('show', f'{MASTER}:{WF}'))
    new = yaml.safe_load(git('show', f'{HEAD}:{WF}'))
    steps = new['jobs']['dang']['steps']
    setups = [i for i, step in enumerate(steps)
              if str(step.get('uses', '')).startswith('actions/setup-python@')]
    assert len(setups) == 1
    idx = setups[0]
    assert steps[idx] == {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}
    co = [i for i, step in enumerate(steps) if str(step.get('uses', '')).startswith('actions/checkout@')]
    py = [i for i, step in enumerate(steps) if 'python3' in str(step.get('run', ''))]
    assert idx == co[0] + 1 and all(idx < i for i in py)
    without = copy.deepcopy(new)
    del without['jobs']['dang']['steps'][idx]
    assert without == old
    ci = yaml.safe_load(git('show', f'{HEAD}:.github/workflows/ci.yml'))
    ci_pins = [s for j in ci['jobs'].values() for s in j.get('steps', [])
               if str(s.get('uses', '')).startswith('actions/setup-python@')]
    assert ci_pins and all(s['uses'] == 'actions/setup-python@v5' and
                          s['with']['python-version'] == '3.12' for s in ci_pins)
    assert git('show', f'{P1}:{WF}') == git('show', f'{HEAD}:{WF}')
    comments = [line[1:].strip() for line in patch3.decode().splitlines()
                if line.startswith('+') and not line.startswith('+++') and line[1:].lstrip().startswith('#')]
    assert not any('${{' in line for line in comments)
    result = dict(expected_tree=expected, actual_tree=actual,
                  patch_full_index_byte_equal=True,
                  patch_sha256=hashlib.sha256(patch3).hexdigest(),
                  supplied_patches_match=True, merge_base=BASE,
                  master_new_file_count=len(master_changes), master_only_adds_ops_land=True,
                  master_unchanged_blobs=unchanged, setup_index=idx,
                  python3_run_indices=py, remove_setup_equals_master=True,
                  ci_matching_pins=len(ci_pins), workflow_equals_luot2=True,
                  added_comments=comments, Actions_expression_in_added_comments=False)
    dump(EVIDENCE / 'static.json', result)
    record(dict(id='merge_and_static', lenh='python -B review_checks.py static', rc=0,
                trang_thai='passed', ket_qua=result, log='review-evidence/static.json'))
    print(json.dumps(result, ensure_ascii=False), flush=True)


def quick():
    probe = "import sys,yaml,shutil,json; d=dict(executable=sys.executable,version=sys.version,PyYAML=yaml.__version__,tools={x:shutil.which(x) for x in ('python','python3','actionlint','shellcheck')}); print(json.dumps(d)); assert sys.version_info[:2]==(3,12); assert yaml.__version__=='6.0.3'; assert all(d['tools'].values())"
    run('python_tools', ['python3', '-c', probe], ROOT)
    run('A1', ['python3', str(ROOT / 'a1_check.py'), str(REPO / WF)], ROOT)
    run('A3_shellcheck', ['shellcheck', '--version'], ROOT)
    run('A3_actionlint_version', ['actionlint', '-version'], ROOT)
    run('A3', ['actionlint', WF])
    numstat = run('A4', ['git', 'diff', '--numstat', MASTER, HEAD])
    assert numstat.splitlines() == [f'8\t0\t{WF}']
    run('A5_diff_check', ['git', 'diff', '--check', MASTER, HEAD])


def a2():
    record(dict(id='A2_start', lenh=['python3', 'ops/lease_publish_test.py'], cwd=str(REPO),
                rc=None, trang_thai='running', bat_dau_utc=now(), log='review-evidence/A2.log'))
    output = run('A2', ['python3', 'ops/lease_publish_test.py'])
    summaries = re.findall(r'^lease_publish: (\d+)/(\d+) đạt; đã chạy=(\d+), bỏ qua=(\d+)\s*$', output, re.M)
    assert len(summaries) == 1, summaries
    passed, total, ran, skipped = map(int, summaries[0])
    assert passed == total == ran and total > 0 and skipped == 0
    ins = re.findall(r'^>>> vao (\S+) ', output, re.M)
    outs = re.findall(r'^<<< ra (\S+) \S+s (\S+)\s*$', output, re.M)
    assert len(ins) == len(outs) == total
    assert all(status == 'QUA' for _, status in outs)
    assert collections.Counter(ins) == collections.Counter(name for name, _ in outs)
    assert len(set(ins)) == total
    required = [next(name for name, _ in outs if name.startswith(prefix))
                for prefix in ('t24_', 't33_', 't125_', 't191_')]
    result = dict(tong_ket=f'lease_publish: {passed}/{total} đạt; đã chạy={ran}, bỏ qua={skipped}',
                  vao=len(ins), ra_QUA=len(outs), ca_bat_buoc_QUA=required)
    dump(EVIDENCE / 'A2-positive-evidence.json', result)
    record(dict(id='A2_positive_evidence', lenh='python -B review_checks.py A2 (đọc tổng kết neo đầu dòng và marker)',
                rc=0, trang_thai='passed', ket_qua=result, log='review-evidence/A2-positive-evidence.json'))
    print(json.dumps(result, ensure_ascii=False), flush=True)


def final_snapshot():
    end = snapshot('final')
    initial = json.loads((EVIDENCE / 'snapshot-initial.json').read_text(encoding='utf-8'))
    changed = [key for key in end if end[key] != initial[key]]
    result = dict(changed_sections=changed, files=len(end['files']), dirs=len(end['dirs']),
                  head=end['head'], tree=end['tree'], status=end['status'],
                  gioi_han='Hai mốc không đổi nội dung/mode/symlink/thư mục/.git; không chứng minh không từng ghi rồi hoàn nguyên.')
    dump(EVIDENCE / 'read-only-final.json', result)
    record(dict(id='read_only_final', lenh='python -B review_checks.py final_snapshot',
                rc=0 if not changed else 1, trang_thai='passed' if not changed else 'failed',
                ket_qua=result, log='review-evidence/read-only-final.json'))
    assert not changed, changed
    print(json.dumps(result, ensure_ascii=False), flush=True)


def finish():
    v = verdict()
    required = ('master_ancestor', 'base_ancestor_master', 'preflight', 'merge_and_static',
                'python_tools', 'A1', 'A3_shellcheck', 'A3_actionlint_version', 'A3', 'A4',
                'A5_diff_check', 'A2', 'A2_positive_evidence', 'read_only_final')
    for ident in required:
        measurements = [row for row in v['phep_do'] if row['id'] == ident]
        assert measurements and measurements[-1]['rc'] == 0 and measurements[-1]['trang_thai'] == 'passed', ident
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    a2_result = json.loads((EVIDENCE / 'A2-positive-evidence.json').read_text(encoding='utf-8'))
    readonly = json.loads((EVIDENCE / 'read-only-final.json').read_text(encoding='utf-8'))
    assert not readonly['changed_sections']
    v['phep_do'] = [row for row in v['phep_do'] if row['id'] != 'A2_start']
    v['phep_do'].extend([
        dict(id='A5_selftest', lenh='python scripts/tl.py --selftest', rc=None,
             trang_thai='not_run', ket_qua='Không bắt buộc theo prompt.snapshot lượt 3; không nhận là pass.'),
        dict(id='A6', lenh='Đo LIVE trên GitHub Actions sau land', rc=None,
             trang_thai='not_run', ket_qua='Thuộc phiên điều phối; review này offline, không push hoặc gọi GitHub.')])
    v['gioi_han'] = [x for x in v['gioi_han'] if not x.startswith('A2 đang chạy;')]
    v['gioi_han'].append('Snapshot đầu/cuối giữ nguyên hash, mode, symlink, danh sách thư mục, HEAD/tree/status và .git. '
                         'Đây là so sánh hai mốc, không chứng minh không từng ghi rồi hoàn nguyên; sandbox thực tế là workspace-write.')
    v['tong_hop'] = dict(P0_mo=0, P1_mo=0, P2_mo=0, P3_mo=0, P3_dong=1,
                        F1='closed; ĐÃ VÁ THẬT',
                        merge='Sạch; tree kỳ vọng == reviewed_tree; không đổi thêm ngoài bản vá đã duyệt',
                        master='86 tệp thêm trong ops/land/; không đổi runtime/workflow/installer/wrapper',
                        ancestry='5fe92c1390ca1723d19f374bd364487f013986a1 là tổ tiên của reviewed_sha; rc=0',
                        A1='DAT; rc=0', A2=a2_result, A3='actionlint rc=0; ShellCheck 0.9.0 có mặt',
                        A4='Chỉ .github/workflows/ops-publish-lease.yml; +8/-0',
                        A5='git diff --check rc=0; selftest tl.py not_run theo chỉ thị',
                        A6='not_run — LIVE sau land thuộc điều phối',
                        checkout_cuoi=f"{readonly['files']} tệp và {readonly['dirs']} thư mục giữ nguyên ở hai mốc; HEAD/tree/status/.git không đổi")
    v['ket_luan'] = ('Approve nội dung merge commit trên exact SHA ' + HEAD +
                    ' theo chỉ thị review offline lượt 3. Cây bằng master 5fe92c1 cộng bản vá đã approve ở d5d3c8f, '
                    'master là tổ tiên và không làm bản vá mất tác dụng. Mọi phép đo bắt buộc lượt 3 đạt; '
                    'không có finding mới P0/P1/P2/P3 mở. Không sửa cay-kho, không push, không gọi GitHub. '
                    'Verdict không thay A6, receipt assurance hoặc quyền merge/land.')
    v['hoan_tat_utc'] = now()
    v['verdict'] = 'approve'
    save(v)
    artifacts = [ROOT / 'VERDICT.md', ROOT / 'review_checks.py', ROOT / 'SPEC.md',
                 ROOT / 'a1_check.py', ROOT / 'VERDICT_luot2.md']
    artifacts += sorted(p for p in EVIDENCE.iterdir() if p.is_file() and p.name != 'artifacts-sha256.json')
    dump(EVIDENCE / 'artifacts-sha256.json', {
        str(path.relative_to(ROOT)): dict(size=path.stat().st_size,
                                         sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        for path in artifacts})
    reread = verdict()
    assert reread['verdict'] == 'approve' and reread['reviewed_sha'] == HEAD
    print(json.dumps(dict(verdict=reread['verdict'], reviewed_sha=HEAD,
                          reviewed_tree=reread['reviewed_tree'], A2=a2_result,
                          readonly=readonly), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    {'preflight': preflight, 'static': static, 'quick': quick,
     'A2': a2, 'final_snapshot': final_snapshot, 'finish': finish}[sys.argv[1]]()
