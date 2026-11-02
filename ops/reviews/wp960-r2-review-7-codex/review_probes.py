import json
import subprocess
import sys
import tempfile
from pathlib import Path
from review_common import case, emit, invoke, load_tests, run

t = load_tests()
real = t.bnv2
mode = sys.argv[1]


def cli_pair(root, al, key):
    rows = []
    for debt in (False, True):
        rc, stderr = t._chay_cli(root, al, {key} if debt else ())
        emit(debt=debt, rc=rc, stderr=stderr)
        rows.append(rc)
    return rows


if mode == 'r6-witness':
    for kind, old, new in (
        ('wrong-oid', ' or ra[0] != oid40', ''),
        ('wrong-type', ' or ra[1] not in ("commit", "tag", "tree", "blob")', ''),
        ('mixed-context', 'if len(x) == 40 or _oid_tron(x):', 'if len(x) == 40:'),
    ):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            t.bnv2 = real
            k = t._kho_cau(root)
            if kind == 'mixed-context':
                token = '12ab34c'
                assert real._commit_cua(root, token) is None
            else:
                sha = t._commit_tien_to_so(root, k, str.isalpha, 'chu', 30000)
                k['g']('merge', '-q', '--no-ff', sha, '-m', 'merge')
                token = sha[:7]
                emit(token=token, resolved=real._commit_cua(root, token))
            al = t._ghi_bn_cau(root, k, {'r.receipt.yaml': t._bn_cau(1, f'anchor:\n    mo_ta: Ban {token} chua vao master.\n')})
            run(['git', 'fsck', '--full'], cwd=root)
            for variant in ('HEAD', 'mutant'):
                t.bnv2 = real
                if variant == 'mutant':
                    t._dot_bien_tep(old, new)
                mod = t.bnv2
                saved = mod._chay_git
                if kind != 'mixed-context':
                    def injected(root_, args, vao=None, timeout=60):
                        p = saved(root_, args, vao, timeout)
                        if args[0] == 'cat-file' and any('--batch-check' in a for a in args):
                            assert p.returncode == 0 and not p.stderr
                            requested = vao.strip()
                            value = 'b' * 40 + ' commit\n' if kind == 'wrong-oid' else requested + ' nonsense\n'
                            return subprocess.CompletedProcess(p.args, 0, value, '')
                        return p
                    mod._chay_git = injected
                emit(witness=kind, variant=variant, fixture=root)
                pair = cli_pair(root, al, ('r.receipt.yaml', 'anchor.mo_ta', mod.LUAT_ANCESTRY))
                emit(witness=kind, variant=variant, pair=pair)
                mod._chay_git = saved
elif mode == 'surface-errors':
    for name, payload in [('json-invalid', b'{'), ('utf8-invalid', b'\xff'),
                          ('array', b'[]'), ('null', b'null'),
                          ('empty-surface', b'{"execution_surface":""}')]:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            d, _ = t._bn_surface('ops/reviews/v/run.json', '')
            al = t._kho_surface(root, d, '{"execution_surface":"codex_cli"}',
                                'provider: openai_codex\nexecution_surface: codex_service\n')
            (root / 'ops/reviews/v/run.json').write_bytes(payload)
            emit(witness=name)
            assert cli_pair(root, al, ('r.receipt.yaml', 'verdict_path', real.LUAT_SURFACE)) == [2, 2]
elif mode == 'window-fixture':
    original = t._kho_surface
    saved_cli = t._kiem_cau
    needle = 'Bang do: thay dong verdict thanh `execution_surface: codex_service`.\n'
    def fixture(root, d, rj, verdict):
        if needle in verdict:
            verdict = verdict.replace(needle, needle + '\nprovider: openai_codex\n')
            emit(fixture_mutation='provider only two lines after execution_surface', verdict=verdict)
        return original(root, d, rj, verdict)
    def observed(*a, **kw):
        rc, errors, stats = saved_cli(*a, **kw)
        emit(rc=rc, errors=errors, unknown=stats.get('chua_do'))
        return rc, errors, stats
    t._kho_surface, t._kiem_cau = fixture, observed
    for name in ('HEAD', 'mutant'):
        t.bnv2 = real
        if name == 'mutant':
            t._dot_bien_tep('cua = dong_tep[max(0, j - 1):j + 2]', 'cua = dong_tep[max(0, j - 1):j + 3]')
        emit(variant=name)
        invoke(t, 'c88')
elif mode == 'stderr':
    for kind in ('same-error-wrong-ancestry', 'health-error', 'health-rc3', 'old-probe-only'):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            k = t._kho_cau(root)
            al = t._ghi_bn_cau(root, k, {'r.receipt.yaml': t._bn_cau(1, f'anchor:\n    mo_ta: Commit {k["M"][:7]} chua vao master.\n')})
            saved = real._chay_git
            def fault(root_, args, vao=None, timeout=60):
                p = saved(root_, args, vao, timeout)
                trigger = (kind == 'same-error-wrong-ancestry' and args[0] == 'merge-base') or (
                    kind.startswith('health-') and '--is-shallow-repository' in args) or (
                    kind == 'old-probe-only' and '--git-dir' in args)
                if not trigger:
                    return p
                return subprocess.CompletedProcess(p.args, 3 if kind == 'health-rc3' else 1,
                                                   'false\n' if kind.startswith('health') else '',
                                                   '' if kind == 'health-rc3' else 'error: same probe diagnostic\n')
            real._chay_git = fault
            emit(witness=kind)
            pair = cli_pair(root, al, ('r.receipt.yaml', 'anchor.mo_ta', real.LUAT_ANCESTRY))
            real._chay_git = saved
            assert pair == ([1, 0] if kind == 'old-probe-only' else [2, 2])
