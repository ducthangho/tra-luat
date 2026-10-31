import ast
import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / 'cay-kho'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
SOURCE = REPO / 'ops/bien_nhan_v2_test.py'

def load(path=SOURCE):
    spec = importlib.util.spec_from_file_location('review_suite', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def case(s, prefix):
    return next(f for f in s.CA if f.__name__.startswith(prefix + '_'))

def clean(s):
    s.bnv2 = s._BNV2_THAT
    s.CONG = Path(s._BNV2_THAT.__file__)
    while s._TAM_DOT_BIEN:
        shutil.rmtree(s._TAM_DOT_BIEN.pop())

def focused():
    s = load()
    names = sorted({n.args[0].value for n in ast.walk(ast.parse(SOURCE.read_bytes())) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'do' and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str) and any(n.args[0].value.startswith(f'm{i}_') for i in range(142,158))})
    output = []
    chay, sach = s._chay_1, s._sach_hoan_toan
    for name in names:
        events = []
        def trace(fn):
            r = chay(fn)
            events.append({'case': fn.__name__, 'status': r[0], 'detail': r[1]})
            return r
        def dc(fn):
            r = sach(fn)
            events.append({'control': fn.__name__, 'clean': r[0], 'detail': r[1]})
            return r
        s._chay_1, s._sach_hoan_toan = trace, dc
        rows = s._dot_bien(chi={name})
        assert len(rows) == 1 and rows[0][0] == name and rows[0][2] and rows[0][3] == 'giet_that' and not rows[0][5] and rows[0][6], rows
        assert any(e.get('clean') is True for e in events), events
        assert s.bnv2 is s._BNV2_THAT and not s._TAM_DOT_BIEN
        output.append({'name': name, 'row': rows[0], 'events': events})
    s._chay_1, s._sach_hoan_toan = chay, sach
    (ROOT / 'evidence/focused.json').write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(f'FOCUSED: {len(output)}/{len(output)} giet_that, controls clean')

def mutate(s, name, old, new, target, also=()):
    before = {p: hashlib.sha256((REPO/p).read_bytes()).hexdigest() for p in ('ops/bien_nhan_v2.py', 'ops/bien_nhan_v2_test.py')}
    baseline = s._chay_1(case(s, target))
    assert baseline[0] == 'qua', baseline
    try:
        s._dot_bien_tep(old, new)
        result = s._chay_1(case(s, target))
        others = {c: s._chay_1(case(s, c)) for c in also}
        control = s._sach_hoan_toan(case(s, 'c18'))
        assert result[0] == 'giet_that' and control[0], (result, control)
        record = {'mutation': name, 'old': old, 'new': new, 'target': case(s,target).__name__, 'baseline': baseline, 'result': result, 'non_targets': others, 'control': control}
        print(json.dumps(record, ensure_ascii=False))
    finally:
        clean(s)
    assert all(hashlib.sha256((REPO/p).read_bytes()).hexdigest() == b for p,b in before.items())
    return record

def extra():
    s = load()
    rows = []
    rows.append(mutate(s, 'own-gate-reverse-order', '    return sorted(ds)\n', '    return sorted(ds, reverse=True)\n', 'c99'))
    rows.append(mutate(s, 'glob-restore-C3', 'ds = [p for p in tm.iterdir() if p.name.lower().endswith(".receipt.yaml")]', 'ds = list(tm.glob("*.receipt.yaml"))', 'c101'))
    rows.append(mutate(s, 'm153-reference-c100-chot7', '    except OSError as ex:\n        raise KhongDoDuoc(f"không đọc được trạng thái', '    except Exception as ex:\n        raise KhongDoDuoc(f"không đọc được trạng thái', 'c100', also=('c99',)))
    # Suite-file mutation is a byte copy; the existing c98 itself calls _dot_bien(chi={m81})
    # and the real _dot_bien_tep, so the failure checks the entire reporting wire.
    with tempfile.TemporaryDirectory(prefix='review-suite-mutation-') as t:
        dest = Path(t)
        for rel in ('ops/bien_nhan_v2.py', 'ops/bien_nhan_v2_test.py', *s.NGUON_PHU):
            (dest/rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO/rel, dest/rel)
        path = dest/'ops/bien_nhan_v2_test.py'
        original = path.read_text()
        old = 'print("\\n".join(_dong_ket_qua_dot_bien(nhan, ten, ca_dich, tt, mo_ta, dat, ct)))'
        new = 'print("\\n".join(_dong_ket_qua_dot_bien(nhan, ten, ca_dich, tt, mo_ta, True, ct)))'
        assert original.count(old) == 1
        copied = load(path)
        baseline = copied._chay_1(case(copied, 'c98'))
        assert baseline[0] == 'qua', baseline
        path.write_text(original.replace(old, new))
        mutated = load(path)
        result = mutated._chay_1(case(mutated, 'c98'))
        control = mutated._sach_hoan_toan(case(mutated, 'c18'))
        assert result[0] == 'giet_that' and control[0], (result, control)
        assert not mutated._TAM_DOT_BIEN
        record = {'mutation': 'own-suite-force-report-success', 'old': old, 'new': new, 'target': case(mutated,'c98').__name__, 'baseline': baseline, 'result': result, 'control': control}
        print(json.dumps(record, ensure_ascii=False))
        rows.append(record)
    (ROOT/'evidence/extra.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    print('EXTRA: 4/4 giet_that, controls clean')

def branches():
    s = load()
    original_bang = s.bang
    rows = []
    for prefix in ('C1a:', 'chỉ-x:', 'C1b:'):
        calls = []
        def selected(condition, message):
            if message.startswith(prefix):
                calls.append({'condition': bool(condition), 'message': message})
                original_bang(condition, message)
        s.bang = selected
        baseline = s._chay_1(case(s, 'c101'))
        assert baseline[0] == 'qua' and len(calls) == 1 and calls[0]['condition'], (baseline,calls)
        baseline_observation = list(calls)
        calls.clear()
        try:
            s._dot_bien_tep('if p.name.lower().endswith(".receipt.yaml")]', 'if p.name.endswith(".receipt.yaml")]')
            result = s._chay_1(case(s, 'c101'))
            assert result[0] == 'giet_that' and len(calls) == 1 and not calls[0]['condition'], (result,calls)
            row = {'branch': prefix, 'baseline': baseline, 'baseline_observation': baseline_observation, 'result': result, 'observation': calls[0]}
            print(json.dumps(row, ensure_ascii=False))
            rows.append(row)
        finally:
            clean(s)
    s.bang = original_bang
    (ROOT/'evidence/branches.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    print('BRANCHES: 3/3 baseline qua; 3/3 m142 giet_that at selected existing assertion')

if __name__ == '__main__':
    {'focused': focused, 'extra': extra, 'branches': branches}[sys.argv[1]]()
