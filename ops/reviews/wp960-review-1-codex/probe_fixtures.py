"""Chạy lại builder fixture sẵn có tại SHA review, chỉ đổi fixture trên cây tạm."""
import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path('/tmp/wp960-review-copy')
s = importlib.util.spec_from_file_location('tests', ROOT / 'ops/bien_nhan_v2_test.py')
t = importlib.util.module_from_spec(s)
s.loader.exec_module(t)
b = t.bnv2

def show(label, root, al, no=frozenset()):
    try:
        rc, loi, tk = t._kiem_cau(root, al, no)
        print(label, json.dumps({'rc': rc, 'loi': loi, 'chua_do': tk['chua_do'],
                                'surface_chua_do': tk['surface_chua_do']}, ensure_ascii=False), flush=True)
    except Exception as ex:
        print(label, type(ex).__name__, str(ex)[:180], flush=True)

def al_now(root):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (root / b.THU_MUC).glob('*.receipt.yaml')}

def anchors():
    for style in ('plain', 'folded', 'literal', 'list'):
        with tempfile.TemporaryDirectory(prefix='wp960-anchor-') as d:
            root = Path(d); k = t._kho_cau(root); m = k['M'][:7]
            scalar = {'plain': f'    mo_ta: Commit {m} chua vao master.\n',
                      'folded': f'    mo_ta: >-\n      Commit {m} chua vao master.\n',
                      'literal': f'    mo_ta: |\n      Commit {m} chua vao master.\n',
                      'list': f'    mo_ta:\n      - Commit {m} chua vao master.\n'}[style]
            original = t._bn_cau(1, 'anchor:\n' + scalar)
            al = t._ghi_bn_cau(root, k, {'r.receipt.yaml': original})
            first = k['g']('rev-parse', 'HEAD')
            (root / 'bump').write_text('later\n')
            k['g']('add', '-A'); k['g']('commit', '-qm', 'later than original sentence')
            later = k['g']('rev-parse', 'HEAD')
            p = root / b.THU_MUC / 'r.receipt.yaml'
            print(f'anchor-{style} first={first} later={later}', flush=True)
            p.write_text(original + f'    dung_tai: {later}\n')
            show(f'anchor-{style}-add-anchor-only', root, al_now(root))
            p.write_text(original.replace('chua vao', 'chua  vao') + f'    dung_tai: {later}\n')
            show(f'anchor-{style}-same-sentence-whitespace', root, al_now(root))
            k['g']('add', '-A'); k['g']('commit', '-qm', 'format old sentence and add late anchor')
            show(f'anchor-{style}-after-commit', root, al_now(root))
            if style == 'plain':
                reformat = original.replace(f'mo_ta: Commit {m} chua vao master.', f'mo_ta: "Commit {m} chua vao master."')
            elif style in ('folded', 'literal'):
                reformat = original.replace('      Commit', '        Commit')
            else:
                reformat = original.replace(f'- Commit {m} chua vao master.', f'- "Commit {m} chua vao master."')
            import yaml
            same = yaml.safe_load(original)['anchor']['mo_ta'] == yaml.safe_load(reformat)['anchor']['mo_ta']
            print(f'anchor-{style}-exact-scalar-equal={same}', flush=True)
            p.write_text(reformat + f'    dung_tai: {later}\n')
            k['g']('add', '-A'); k['g']('commit', '-qm', 'YAML-only formatting with identical scalar value')
            show(f'anchor-{style}-YAML-only-format', root, al_now(root))

def surfaces():
    for mode in ('mismatch', 'json-invalid', 'json-list', 'json-missing-field',
                 'json-absent', 'verdict-invalid-utf8', 'verdict-absent',
                 'upper-case', 'two-fields-same-line', 'prose-mentions'):
        with tempfile.TemporaryDirectory(prefix='wp960-surface-') as d:
            root = Path(d)
            data, _ = t._bn_surface('ops/reviews/v/run.json', '')
            t._cay(root, {'r.receipt.yaml': data})
            rp = root / 'ops/reviews/v/run.json'; rp.parent.mkdir(parents=True)
            vp = root / 'ops/reviews/v.md'
            rp.write_text(json.dumps({'execution_surface': 'codex_cli'}))
            vp.write_text('execution_surface: codex_service\n')
            if mode == 'json-invalid': rp.write_text('{')
            if mode == 'json-list': rp.write_text('[]')
            if mode == 'json-missing-field': rp.write_text('{}')
            if mode == 'json-absent': rp.unlink()
            if mode == 'verdict-invalid-utf8': vp.write_bytes(b'\xff')
            if mode == 'verdict-absent': vp.unlink()
            if mode == 'upper-case': vp.write_text('EXECUTION_SURFACE: CODEX_SERVICE\n')
            if mode == 'two-fields-same-line': vp.write_text('execution_surface: codex_cli; execution_surface: codex_service\n')
            if mode == 'prose-mentions': vp.write_text('execution_surface: codex_cli (truoc day codex_service)\n')
            show('surface-' + mode, root, al_now(root))
            if mode in ('json-invalid', 'json-list', 'verdict-invalid-utf8', 'json-absent'):
                show('surface-debt-' + mode, root, al_now(root),
                     {('r.receipt.yaml', 'verdict_path', b.LUAT_SURFACE)})

def measurement():
    for mode in ('git-fails', 'merge-base-fails', 'branch-missing', 'moc-missing-object', 'yaml-cycle'):
        with tempfile.TemporaryDirectory(prefix='wp960-errors-') as d:
            root = Path(d); k = t._kho_cau(root)
            original = t._bn_cau(1, f'anchor:\n    mo_ta: Commit {k["M"][:7]} chua vao master.\n')
            if mode == 'moc-missing-object': original += '    dung_tai: ' + '1234abcd' * 5 + '\n'
            if mode == 'yaml-cycle': original += 'cycle: &self [*self]\n'
            al = t._ghi_bn_cau(root, k, {'r.receipt.yaml': original})
            oldgit = b._git
            try:
                if mode == 'git-fails': b._git = lambda *a, **kw: (127, 'injected git error')
                if mode == 'merge-base-fails':
                    b._git = lambda r, *a, **kw: (128, 'injected merge-base error') if a[0] == 'merge-base' else oldgit(r, *a, **kw)
                if mode == 'branch-missing': k['g']('branch', '-m', 'different')
                show(mode, root, al)
                if mode == 'yaml-cycle':
                    run = subprocess.run(['python3', str(ROOT / 'ops/bien_nhan_v2.py'), '--root', str(root)], capture_output=True, text=True)
                    print('yaml-cycle-CLI', json.dumps({'rc': run.returncode, 'stderr_tail': run.stderr.splitlines()[-3:]}, ensure_ascii=False), flush=True)
            finally:
                b._git = oldgit

def candidates():
    with tempfile.TemporaryDirectory(prefix='wp960-oid-') as d:
        root = Path(d); k = t._kho_cau(root)
        real = 'ecebffe9675d0952f3a0ab65eaa44087853a26bc'
        # Chỉ fetch từ bản sao trên filesystem, không dùng mạng.
        k['g']('fetch', '-q', str(ROOT), real)
        k['g']('update-ref', 'refs/remotes/origin/master', real)
        print('oid-prefix-resolves', k['g']('rev-parse', '--verify', real[:7] + '^{commit}'), flush=True)
        for oid in (real, real[:8], real[:7], 'deadbeef'):
            p = root / b.THU_MUC / 'r.receipt.yaml'; p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(t._bn_cau(1, f'anchor:\n    mo_ta: Commit {oid} chua vao master.\n'))
            k['g']('add', '-A'); k['g']('commit', '-qm', 'candidate ' + oid)
            show('oid-' + oid, root, al_now(root))

def acceptance():
    import os
    old = t._cay
    def observed(root, *a, **kw):
        value = old(root, *a, **kw)
        env = dict(os.environ, GIT_CEILING_DIRECTORIES=str(root.parent))
        r = subprocess.run(['git', '-C', str(root), 'rev-parse', '--verify', 'HEAD'],
                           capture_output=True, text=True, env=env)
        print('c73-fixture-history', json.dumps({'git_rc': r.returncode,
            'git_HEAD_exists': (root / '.git/HEAD').exists(), 'stderr': r.stderr.strip()}, ensure_ascii=False))
        return value
    t._cay = observed
    try:
        print('c73-existing-case', t._chay_1(t.c73_A4_surface_verdict_doi_chieu_run_json))
    finally:
        t._cay = old

def a3_mutation():
    import shutil
    old_module, old_product, old_check = t.bnv2, t.CONG, t._kiem_cau
    def observed(*a, **kw):
        value = old_check(*a, **kw)
        print('m78-actual-fields', [x.split('`')[1] for x in value[1]], flush=True)
        return value
    try:
        t._dot_bien_tep('return [c for c in _RE_CAU.split(" ".join(van.split())) if c]',
                       'return [c for dong in van.splitlines() for c in _RE_CAU.split(dong) if c]')
        t._kiem_cau = observed
        print('m78-existing-c72', t._chay_1(t.c72_A3_bien_the_co_dau_khong_dau_xuong_dong_deu_bi_nhan), flush=True)
    finally:
        t.bnv2, t.CONG, t._kiem_cau = old_module, old_product, old_check
        while t._TAM_DOT_BIEN:
            shutil.rmtree(t._TAM_DOT_BIEN.pop())

if __name__ == '__main__':
    import sys
    {'anchors': anchors, 'surfaces': surfaces, 'measurement': measurement, 'candidates': candidates, 'acceptance': acceptance, 'a3': a3_mutation}[sys.argv[1]]()
