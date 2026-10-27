"""Đối chứng hành vi của từng chốt bị gỡ, dùng builder fixture sẵn có."""
import ast
import hashlib
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path('/tmp/wp960-review-copy')
s = importlib.util.spec_from_file_location('tests', ROOT / 'ops/bien_nhan_v2_test.py')
t = importlib.util.module_from_spec(s); s.loader.exec_module(t)
nodes = ast.parse(Path('probe_mutations.py').read_text()).body
mutations = next(ast.literal_eval(n.value) for n in nodes if isinstance(n, ast.Assign)
                 and any(isinstance(x, ast.Name) and x.id == 'MUTATIONS' for x in n.targets))

def path(number):
    b = t.bnv2
    with tempfile.TemporaryDirectory(prefix='wp960-guard-path-') as d:
        root = Path(d); k = t._kho_cau(root); h = k['M']
        if number == 4:
            data, _ = t._bn_surface('ops/reviews/v/run.json', '')
            t._cay(root, {'r.receipt.yaml': data})
            rp = root / 'ops/reviews/v/run.json'; rp.parent.mkdir(parents=True)
            rp.write_text('{}')
            (root / 'ops/reviews/v.md').write_text('execution_surface: codex_service\n')
            p = root / b.THU_MUC / 'r.receipt.yaml'
            al = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()}
        else:
            marker = k['B0'][:7] if number == 1 else k['B0']
            text = f'anchor:\n    mo_ta: Commit {h[:7]} chua vao master.\n'
            if number in (1, 5): text += f'    dung_tai: {marker}\n'
            receipts = {'r.receipt.yaml': t._bn_cau(1, text)}
            if number == 2:
                receipts = {'r.receipt.yaml': t._bn_cau(1, f'anchor:\n    mo_ta: Ban va {h} chua duoc review lai.\n'),
                            'r2.receipt.yaml': t._bn_cau('unknown', '', h)}
            al = t._ghi_bn_cau(root, k, receipts)
        old_git = b._git
        if number in (3, 5):
            operation = 'merge-base' if number == 3 else 'blame'
            b._git = lambda r, *a, **kw: (127, 'injected ' + operation + ' error') if a[0] == operation else old_git(r, *a, **kw)
        try:
            try:
                rc, errors, stats = t._kiem_cau(root, al)
                return {'rc': rc, 'errors': errors, 'unknown': stats['chua_do']}
            except Exception as ex:
                return {'exception': type(ex).__name__, 'detail': str(ex)}
        finally:
            b._git = old_git

for i, (name, old, new) in enumerate(mutations[:5], 1):
    baseline = path(i)
    module, product = t.bnv2, t.CONG
    try:
        t._dot_bien_tep(old, new)
        mutated = path(i)
    finally:
        t.bnv2, t.CONG = module, product
        while t._TAM_DOT_BIEN:
            shutil.rmtree(t._TAM_DOT_BIEN.pop())
    print(name, json.dumps({'baseline': baseline, 'mutated': mutated}, ensure_ascii=False), flush=True)
