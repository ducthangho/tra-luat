import datetime
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

import yaml

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'cay-kho'
EVIDENCE = ROOT / 'review-evidence'
EVIDENCE.mkdir(exist_ok=True)
HEAD = '275869169e134758bb145565d28f0b0897a92f87'
MASTER = '358451e80b573d148807717bece3fd973915fbad'
MERGE = 'ccf77900e698727d9d5987414bc85def40f0c17c'
OLD = '3b430923c88f67041ce79ce9b2f8aac0e53a28b4'
PATCH2 = 'd5d3c8ffc021db8a99c366c7520b4f063cd27ab8'
PATCHBASE = '1f0941e9bba1d1d517eda4174167b81963c06bd5'
WF = '.github/workflows/ops-publish-lease.yml'
SPEC = 'ops/specs/lease-publish-ghim-python-r1.md'
SPEC_HASH = '8f4f89a1414fd009f5a16be358925332c6c576a132710f5819e5cce7e778f5ce'
PYBIN = ROOT.parent / 'py312/bin'
ENV = dict(os.environ, PATH=f'{PYBIN}:/root/.local/bin:' + os.environ['PATH'],
           PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1', GIT_OPTIONAL_LOCKS='0')


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def state():
    return yaml.safe_load((ROOT / 'VERDICT.md').read_text(encoding='utf-8'))


def write_state(obj):
    (ROOT / 'VERDICT.md').write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=110), encoding='utf-8')


def record(item):
    obj = state()
    obj.setdefault('phep_do', []).append(item)
    write_state(obj)


def git(*args, ok=True):
    p = subprocess.run(['git', *args], cwd=REPO, env=ENV, capture_output=True)
    if ok and p.returncode:
        raise RuntimeError((args, p.returncode, p.stderr.decode('utf-8', 'replace')))
    return p


def run(label, args, cwd=REPO):
    started = time.monotonic()
    path = EVIDENCE / (label + '.log')
    with path.open('wb') as log:
        p = subprocess.run(args, cwd=cwd, env=ENV, stdout=log, stderr=subprocess.STDOUT)
    output = path.read_text(encoding='utf-8', errors='replace')
    result = dict(id=label, lenh=args, cwd=str(cwd), rc=p.returncode,
                  trang_thai='passed' if p.returncode == 0 else 'failed',
                  giay=round(time.monotonic() - started, 3), log=str(path.relative_to(ROOT)),
                  ket_qua=output[-6000:])
    dump(EVIDENCE / (label + '.json'), result)
    record(result)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return result


def snapshot(label):
    entries = {}
    for base, dirs, files in os.walk(REPO, followlinks=False):
        for name in sorted(dirs + files):
            p = Path(base) / name
            s = p.lstat()
            key = p.relative_to(REPO).as_posix()
            item = {'mode': stat.S_IMODE(s.st_mode)}
            if stat.S_ISLNK(s.st_mode):
                item.update(kind='symlink', target=os.readlink(p))
            elif stat.S_ISDIR(s.st_mode):
                item.update(kind='dir')
            elif stat.S_ISREG(s.st_mode):
                h = hashlib.sha256()
                with p.open('rb') as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b''):
                        h.update(block)
                item.update(kind='file', size=s.st_size, sha256=h.hexdigest())
            else:
                raise AssertionError(f'special entry: {p}')
            entries[key] = item
    obj = dict(head=git('rev-parse', 'HEAD').stdout.decode().strip(),
               tree=git('rev-parse', 'HEAD^{tree}').stdout.decode().strip(),
               status=git('status', '--porcelain=v1', '--untracked-files=all').stdout.decode(),
               index_diff=git('diff', '--cached', '--binary', '--full-index').stdout.decode(),
               worktree_diff=git('diff', '--binary', '--full-index').stdout.decode(), entries=entries)
    dump(EVIDENCE / (label + '.json'), obj)
    summary = {k: v for k, v in obj.items() if k != 'entries'}
    summary.update(files=sum(v['kind'] != 'dir' for v in entries.values()),
                   dirs=sum(v['kind'] == 'dir' for v in entries.values()))
    if label == 'snapshot-initial':
        assert obj['head'] == HEAD and not obj['status'] and not obj['index_diff'] and not obj['worktree_diff'], summary
    else:
        before = json.loads((EVIDENCE / 'snapshot-initial.json').read_text())
        delta = [k for k in before if before[k] != obj[k]]
        summary['changed_sections'] = delta
        summary['changed_paths'] = [k for k in before['entries'].keys() | entries.keys()
                                    if before['entries'].get(k) != entries.get(k)]
        assert not delta, summary
    record(dict(id=label, lenh='python -B review_checks.py ' + label, rc=0,
                trang_thai='passed', log=f'review-evidence/{label}.json', ket_qua=summary))
    print(json.dumps(summary, ensure_ascii=False), flush=True)


def tree_map(ref):
    result = {}
    for entry in git('ls-tree', '-rz', '--full-tree', ref).stdout.split(b'\0'):
        if entry:
            meta, name = entry.split(b'\t', 1)
            mode, typ, oid = meta.decode().split()
            result[name.decode()] = (mode, typ, oid)
    return result


def hash_tree(entries):
    root = {}
    for path, entry in entries.items():
        sub = root
        parts = path.split('/')
        for part in parts[:-1]:
            sub = sub.setdefault(part, {})
        sub[parts[-1]] = entry

    def walk(node):
        data = b''
        for name, value in sorted(node.items(), key=lambda kv: (kv[0] + ('/' if isinstance(kv[1], dict) else '')).encode()):
            if isinstance(value, dict):
                mode, oid = '40000', walk(value)
            else:
                mode, _, oid = value
                mode = mode.lstrip('0')
            data += mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(oid)
        return hashlib.sha1(b'tree ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    return walk(root)


def static_checks():
    numstat = git('diff', '--numstat', MASTER, HEAD).stdout
    (EVIDENCE / 'numstat.log').write_bytes(numstat)
    rows = [r.split('\t') for r in numstat.decode().splitlines()]
    assert len(rows) == 2 and rows[0] == ['8', '0', WF] and rows[1][2] == SPEC and rows[1][1] == '0', rows
    assert git('merge-base', '--is-ancestor', MASTER, HEAD, ok=False).returncode == 0
    assert git('show', '-s', '--format=%P', MERGE).stdout.decode().strip() == OLD + ' ' + MASTER
    assert git('show', '-s', '--format=%P', HEAD).stdout.decode().strip() == MERGE
    master, old, merge, head = (tree_map(x) for x in (MASTER, OLD, MERGE, HEAD))
    approved = git('show', f'{PATCH2}:{WF}').stdout
    assert approved == git('show', f'{OLD}:{WF}').stdout == git('show', f'{HEAD}:{WF}').stdout == (REPO / WF).read_bytes()
    expected_merge = dict(master, **{WF: old[WF]})
    assert merge == expected_merge
    expected_merge_tree = hash_tree(expected_merge)
    assert expected_merge_tree == git('rev-parse', f'{MERGE}^{{tree}}').stdout.decode().strip()
    spec = git('show', f'{HEAD}:{SPEC}').stdout
    assert spec == (ROOT / 'SPEC.md').read_bytes() == (REPO / SPEC).read_bytes()
    assert hashlib.sha256(spec).hexdigest() == SPEC_HASH
    assert head == dict(merge, **{SPEC: head[SPEC]})
    assert hash_tree(head) == git('rev-parse', f'{HEAD}^{{tree}}').stdout.decode().strip()
    patch = git('diff', '--binary', '--full-index', MASTER, HEAD, '--', WF).stdout
    patch2 = git('diff', '--binary', '--full-index', PATCHBASE, PATCH2, '--', WF).stdout
    patch3 = git('diff', '--binary', '--full-index', '5fe92c1390ca1723d19f374bd364487f013986a1', OLD, '--', WF).stdout
    assert patch == patch2 == patch3
    (EVIDENCE / 'workflow-approved.patch').write_bytes(patch)
    (EVIDENCE / 'measured-vs-master.patch').write_bytes(git('diff', MASTER, HEAD).stdout)
    (EVIDENCE / 'measured-delta-luot3-luot4.patch').write_bytes(git('diff', OLD, HEAD).stdout)
    supplied = {}
    for name, measured in [('diff_vs_master.patch', 'measured-vs-master.patch'), ('delta_luot3_luot4.patch', 'measured-delta-luot3-luot4.patch')]:
        supplied[name] = (ROOT / name).read_bytes() == (EVIDENCE / measured).read_bytes()
    candidate = yaml.safe_load((REPO / WF).read_bytes())
    base_yaml = yaml.safe_load(git('show', f'{MASTER}:{WF}').stdout)
    steps = candidate['jobs']['dang']['steps']
    setup = [i for i, v in enumerate(steps) if str(v.get('uses', '')).startswith('actions/setup-python@')]
    assert len(setup) == 1
    new_step = steps.pop(setup[0])
    assert candidate == base_yaml
    assert new_step == {'uses': 'actions/setup-python@v5', 'with': {'python-version': '3.12'}}
    ci_steps = [s for j in yaml.safe_load(git('show', f'{HEAD}:.github/workflows/ci.yml').stdout)['jobs'].values()
                for s in j.get('steps', []) if str(s.get('uses', '')).startswith('actions/setup-python@')]
    assert len(ci_steps) == 8 and all(s['uses'] == new_step['uses'] and s['with']['python-version'] == '3.12' for s in ci_steps)
    common = git('merge-base', OLD, MASTER).stdout.decode().strip()
    master_changes = git('diff', '--name-status', common, MASTER).stdout.decode()
    (EVIDENCE / 'master-changes.log').write_text(master_changes, encoding='utf-8')
    merge_delta = git('diff', '--name-status', OLD, MERGE).stdout.decode()
    (EVIDENCE / 'merge-delta.log').write_text(merge_delta, encoding='utf-8')
    common_tree = tree_map(common)
    changed_master = {p for p in common_tree.keys() | master.keys() if common_tree.get(p) != master.get(p)}
    changed_merge = {p for p in old.keys() | merge.keys() if old.get(p) != merge.get(p)}
    assert changed_master == changed_merge
    result = dict(head=HEAD, reviewed_tree=hash_tree(head), merge=MERGE, merge_parents=[OLD, MASTER],
                  merge_base=common, master_ancestor=True, numstat=rows,
                  spec_sha256=hashlib.sha256(spec).hexdigest(), spec_bytes=len(spec),
                  spec_equals_supplied=True, workflow_equals_luot2_luot3=True,
                  workflow_patch_byte_equal=True, workflow_patch_sha256=hashlib.sha256(patch).hexdigest(),
                  expected_merge_tree=expected_merge_tree, merge_tree_equals_master_with_approved_workflow=True,
                  merge_delta_equals_master_delta=True, master_changed_paths=len(changed_master),
                  merge_only_master_content=True, head_only_adds_spec=True,
                  yaml_remove_setup_equals_master=True, setup_step=new_step, setup_index=setup[0],
                  ci_matching_python_pins=len(ci_steps), supplied_patches_match=supplied,
                  core_abbrev=git('config', '--get', 'core.abbrev').stdout.decode().strip())
    assert result['core_abbrev'] == '7'
    dump(EVIDENCE / 'static.json', result)
    record(dict(id='static', lenh='python -B review_checks.py static', rc=0,
                trang_thai='passed', log='review-evidence/static.json', ket_qua=result))
    print(json.dumps(result, ensure_ascii=False), flush=True)


def quick():
    run('python-tools', [str(PYBIN / 'python'), '-c',
        'import sys,yaml,shutil,json; d=dict(executable=sys.executable,version=sys.version,PyYAML=yaml.__version__,tools={x:shutil.which(x) for x in ("python","python3","actionlint","shellcheck")}); print(json.dumps(d)); assert sys.version_info[:2]==(3,12); assert yaml.__version__=="6.0.3"; assert all(d["tools"].values())'], ROOT)
    run('A1', [str(PYBIN / 'python'), str(ROOT / 'a1_check.py'), str(REPO / WF)], ROOT)
    run('A3-shellcheck', ['shellcheck', '--version'], ROOT)
    run('A3-actionlint-version', ['actionlint', '-version'], ROOT)
    run('A3', ['actionlint', WF])
    run('A5-diff-check', ['git', 'diff', '--check', MASTER, HEAD])
    run('doctrine-scan', ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'])


def suite():
    result = run('A2', ['python3', 'ops/lease_publish_test.py'])
    output = (EVIDENCE / 'A2.log').read_text(encoding='utf-8', errors='replace')
    summaries = re.findall(r'^lease_publish: (\d+)/(\d+) đạt; đã chạy=(\d+), bỏ qua=(\d+)\s*$', output, re.M)
    enters = re.findall(r'^>>> vao (\S+) ', output, re.M)
    leaves = re.findall(r'^<<< ra (\S+) \S+s (QUA|DO|BO_QUA)$', output, re.M)
    must = ['t24_workflow_KHONG_duoc_nhet_dau_skip_ci_vao_commit', 't33_workflow_dang_lease_phai_qua_actionlint',
            't125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor', 't191_MOI_chot_cua_kiem_deu_duoc_t190_phu_o_nhanh_DA_DANG']
    assert result['rc'] == 0 and len(summaries) == 1, (result['rc'], summaries)
    n, total, ran, skips = map(int, summaries[0])
    assert n == total == ran == len(enters) == len(leaves) and n > 0 and skips == 0
    assert len(set(enters)) == len(enters) and all(v == 'QUA' for _, v in leaves)
    assert all((name, 'QUA') in leaves for name in must)
    positive = dict(tong_ket=f'lease_publish: {n}/{total} đạt; đã chạy={ran}, bỏ qua={skips}',
                    vao=len(enters), ra_QUA=len(leaves), ca_bat_buoc_QUA=must)
    dump(EVIDENCE / 'A2-positive-evidence.json', positive)
    record(dict(id='A2-positive-evidence', lenh='python -B review_checks.py A2', rc=0,
                trang_thai='passed', log='review-evidence/A2-positive-evidence.json', ket_qua=positive))
    print(json.dumps(positive, ensure_ascii=False), flush=True)


def init():
    write_state(dict(verdict='pending', reviewed_sha=HEAD, base_sha=MASTER, review_axes=['spec', 'standards_security'],
                     reviewer=dict(provider='openai_codex', vai_tro='Reviewer độc lập, offline lượt 4',
                                   model='GPT-6 theo runtime; không đo độc lập model ID/effort của launcher',
                                   execution_surface='Agent API với shell cục bộ (codex_service)', transport='machine/local tools; không gọi GitHub'),
                     bat_dau_utc=now(), findings=[], phep_do=[],
                     moi_truong=dict(PATH_them_dau=[str(PYBIN), '/root/.local/bin'],
                                     bien_them={k: ENV[k] for k in ['PYTHONDONTWRITEBYTECODE', 'PYTHONUNBUFFERED', 'GIT_OPTIONAL_LOCKS']},
                                     sandbox='workspace-write; cay-kho được đối xử read-only; evidence ngoài kho',
                                     cloud_environment_status='Tool không có trong ALL_TOOLS; không thực hiện network'),
                     pham_vi='Prompt snapshot lượt 4: 5 nhiệm vụ, A4 được chủ kho nới thành 2 tệp theo chỉ thị; không push/không GitHub.'))


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'init':
        init()
    elif action in ('snapshot-initial', 'snapshot-final'):
        snapshot(action)
    elif action == 'static':
        static_checks()
    elif action == 'quick':
        quick()
    elif action == 'A2':
        suite()
    else:
        raise SystemExit(action)
