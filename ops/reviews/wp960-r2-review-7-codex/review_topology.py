import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from review_common import BASE, HEAD, SCRATCH, SHA, SOURCE, emit, load_tests, run

t = load_tests()
mode = sys.argv[1]
if mode in ('ci', 'base', 'base-recheck'):
    root = SCRATCH / ('ci' if mode == 'ci' else 'base')
    if mode != 'base-recheck':
        shutil.copytree(HEAD, root)
    if mode.startswith('base'):
        assert run(['git', 'checkout', '-q', '--detach', BASE], cwd=root).returncode == 0
        assert run(['git', 'update-ref', 'refs/remotes/origin/master', BASE], cwd=root).returncode == 0
        assert run(['git', 'symbolic-ref', 'refs/remotes/origin/HEAD', 'refs/remotes/origin/master'], cwd=root).returncode == 0
        # Head code evaluating the unmodified corpus of the base lease.
        loi, tk = t.bnv2.kiem(root)
        emit(measure='HEAD code / base corpus', rc=t.bnv2._ma_thoat(loi, tk), errors=loi, stats=tk)
        # Also measure the original base code; the old surface definition has 3 extra debts.
        run([sys.executable, '-B', 'ops/bien_nhan_v2.py', '--root', '.'], cwd=root)
    else:
        assert run(['git', 'symbolic-ref', '--delete', 'refs/remotes/origin/HEAD'], cwd=root).returncode == 0
        master = run(['git', 'rev-parse', 'refs/remotes/origin/master'], cwd=root).stdout.strip()
        tree = run(['git', 'rev-parse', SHA + '^{tree}'], cwd=root).stdout.strip()
        env = {**os.environ, 'GIT_AUTHOR_NAME': 'review', 'GIT_AUTHOR_EMAIL': 'review@local',
               'GIT_COMMITTER_NAME': 'review', 'GIT_COMMITTER_EMAIL': 'review@local',
               'GIT_AUTHOR_DATE': '2026-10-29T06:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-29T06:00:00Z'}
        merge = run(['git', 'commit-tree', tree, '-p', master, '-p', SHA, '-m', 'local pull_request simulation'],
                    cwd=root, env=env).stdout.strip()
        assert run(['git', 'checkout', '-q', '--detach', merge], cwd=root).returncode == 0
        run(['git', 'rev-list', '--parents', '-n', '1', 'HEAD'], cwd=root)
        run(['git', 'rev-parse', 'HEAD^{tree}'], cwd=root)
        run(['git', 'rev-parse', '--is-shallow-repository'], cwd=root)
        run(['git', 'symbolic-ref', '-q', 'refs/remotes/origin/HEAD'], cwd=root)
        run(['git', 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/remotes/origin/master'], cwd=root)
        run([sys.executable, '-B', 'ops/bien_nhan_v2.py', '--root', '.'], cwd=root,
            env={**os.environ, 'GITHUB_EVENT_NAME': 'pull_request', 'GITHUB_SHA': merge})
elif mode == 'debt':
    m = t.bnv2
    loi, tk = m.kiem(HEAD, no_cau_lich_su=frozenset())
    keys = set(tk['vi_pham_cau'])
    emit(measure='empty debt / HEAD corpus', rc=m._ma_thoat(loi, tk), errors=len(loi),
         counts=Counter(k[2] for k in keys), unknown=tk['chua_do'],
         other_errors=[s for s in loi if not s.startswith('[L-')],
         keys_match_frozen=keys == set(m.NO_CAU_LICH_SU),
         file_missing=[k for k in m.NO_CAU_LICH_SU if not (HEAD / m.THU_MUC / k[0]).is_file()],
         subset_test=keys <= t.NO_CAU_DONG_BANG)
    assert m._ma_thoat(loi, tk) == 1 and len(loi) == 61 and keys == set(m.NO_CAU_LICH_SU)
elif mode == 'config':
    for value in ('false', 'no', 'off', 'true', 'yes', 'on'):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            k = t._kho_cau(root)
            al = t._ghi_bn_cau(root, k, {'r.receipt.yaml': t._bn_cau(1, f'anchor:\n    mo_ta: Commit {k["M"][:7]} chua vao master.\n')})
            k['g']('config', 'remote.archive.promisor', value)
            run(['git', 'fsck', '--full'], cwd=root)
            pairs = []
            for debt in (False, True):
                key = ('r.receipt.yaml', 'anchor.mo_ta', t.bnv2.LUAT_ANCESTRY)
                rc, stderr = t._chay_cli(root, al, {key} if debt else ())
                emit(config=value, debt=debt, rc=rc, stderr=stderr)
                pairs.append(rc)
            assert pairs == ([1, 0] if value in ('false', 'no', 'off') else [2, 2])
    for kind in ('alternates-env', 'alternates-file', 'linked-worktree'):
        with tempfile.TemporaryDirectory() as td:
            top = Path(td)
            root = top / 'repo'
            root.mkdir()
            k = t._kho_cau(root)
            al = t._ghi_bn_cau(root, k, {'r.receipt.yaml': t._bn_cau(1, f'anchor:\n    mo_ta: Commit {k["M"][:7]} chua vao master.\n')})
            env = {}
            if kind.startswith('alternates'):
                pool = top / 'object-pool'
                shutil.move(root / '.git/objects', pool)
                (root / '.git/objects/info').mkdir(parents=True)
                if kind.endswith('env'):
                    env['GIT_ALTERNATE_OBJECT_DIRECTORIES'] = str(pool)
                else:
                    (root / '.git/objects/info/alternates').write_text(str(pool) + '\n')
            else:
                target = top / 'linked'
                k['g']('worktree', 'add', '-q', '--detach', str(target), 'HEAD')
                root = target
            run(['git', 'fsck', '--full'], cwd=root, env={**os.environ, **env})
            for debt in (False, True):
                key = ('r.receipt.yaml', 'anchor.mo_ta', t.bnv2.LUAT_ANCESTRY)
                rc, stderr = t._chay_cli(root, al, {key} if debt else (), env=env)
                emit(config=kind, debt=debt, rc=rc, stderr=stderr)
                assert rc == (0 if debt else 1)
