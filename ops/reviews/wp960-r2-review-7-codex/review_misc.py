import ast
import sys
from review_common import SCRATCH, SOURCE, emit, invoke, load_tests, run

mode = sys.argv[1]
if mode == 'baseline':
    head = load_tests()
    base = load_tests(SCRATCH / 'base')
    head.bnv2 = base.bnv2
    for name in ('c86', 'c89', 'c87', 'c88'):
        invoke(head, name)
elif mode == 'm1-static':
    tree = ast.parse((SOURCE / 'ops/bien_nhan_v2.py').read_text())
    forbidden = [(n.lineno, n.name) for n in ast.walk(tree)
                 if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                 and (n.name.startswith('_moc_') or n.name in ('_commit_them_cau', '_co_cau'))]
    keys = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Constant) and n.value == 'dung_tai']
    emit(forbidden_functions=forbidden, dung_tai_literal_lines=keys)
elif mode == 'citation-window':
    for direction, new in [('before', 'cua = dong_tep[max(0, j - 2):j + 2]'),
                            ('after', 'cua = dong_tep[max(0, j - 1):j + 3]')]:
        t = load_tests(SCRATCH / 'hint')
        original = t._kho_surface
        def fixture(root, d, rj, verdict):
            if ('provider: openai_codex\n\nexecution_surface' in verdict
                    or 'execution_surface: codex_service\n\nprovider:' in verdict):
                verdict = verdict.replace('provider:', 'source:')
            return original(root, d, rj, verdict)
        t._kho_surface = fixture
        emit(variant='HEAD', direction=direction)
        assert invoke(t, 'c88')[0] == 'qua'
        t._dot_bien_tep('cua = dong_tep[max(0, j - 1):j + 2]', new)
        emit(variant='mutant', direction=direction)
        assert invoke(t, 'c88')[0] == 'giet_that'
elif mode == 'final-state':
    import hashlib
    import os
    env = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}
    for args in (['status', '--porcelain=v1', '--ignored'], ['diff', '--quiet'],
                 ['diff', '--cached', '--quiet'], ['rev-parse', 'HEAD', 'HEAD^{tree}'],
                 ['symbolic-ref', 'refs/remotes/origin/HEAD'],
                 ['rev-parse', 'refs/remotes/origin/master']):
        assert run(['git', *args], env=env).returncode == 0
    for rel in ('ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md', 'ops/bien_nhan_v2.py', 'ops/bien_nhan_v2_test.py'):
        emit(file=rel, sha256=hashlib.sha256((SOURCE / rel).read_bytes()).hexdigest(),
             equals_initial_copy=(SOURCE / rel).read_bytes() == (SCRATCH / 'head' / rel).read_bytes())
