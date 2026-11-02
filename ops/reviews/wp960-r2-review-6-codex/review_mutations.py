import ast
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path
import shutil
import sys
from review_checks import ROOT, TMP, record

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
VARIANTS = {
    'v1-batch-oid': (' or ra[0] != oid40', '', 'c94_'),
    'v2-batch-type': (' or ra[1] not in ("commit", "tag", "tree", "blob")', '', 'c94_'),
    'v3-mixed-context': ('if len(x) == 40 or _oid_tron(x):', 'if len(x) == 40:', 'c71_'),
    'v4-window-before': ('cua = dong_tep[max(0, j - 1):j + 2]', 'cua = dong_tep[j:j + 2]', 'c88_'),
    'v5-commit-case': ('r"\\bcommit\\s*\\Z", re.IGNORECASE', 'r"\\bcommit\\s*\\Z"', 'c87_'),
}

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def official():
    t = load(TMP / 'head/ops/bien_nhan_v2_test.py', 'targets')
    env = t.__dict__.copy()
    env.update(DC='c18_neo_git_DUNG_thi_qua', C91='c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no',
               C94='c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC', C95='c95_moi_truong_git_KHONG_doi_ket_qua_do')
    rows = []
    def do(name, change, target, detail, doi_chung=None, **kw):
        old, cong = t.bnv2, t.CONG
        try:
            change()
            fn = next(f for f in t.CA if f.__name__ == target)
            state, why = t._chay_1(fn)
            control = t._chay_1(next(f for f in t.CA if f.__name__ == doi_chung)) if doi_chung else None
            row = dict(mutant=name, target=target, state=state, reason=why, control=control)
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
        finally:
            t.bnv2, t.CONG = old, cong
            while t._TAM_DOT_BIEN:
                shutil.rmtree(t._TAM_DOT_BIEN.pop(), ignore_errors=True)
    env['do'] = do
    selected = {78, 94, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 129, 130, 131, 132, 133, 134, 135, 136}
    tree = ast.parse((TMP / 'head/ops/bien_nhan_v2_test.py').read_text())
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'do' and isinstance(n.args[0], ast.Constant):
            name = n.args[0].value
            number = int(re.match(r'm(\d+)', name)[1])
            if number in selected:
                eval(compile(ast.Expression(n), 'official-mutant', 'eval'), env)
    assert all(r['state'] == 'giet_that' and (not r['control'] or r['control'][0] == 'qua') for r in rows)
    record('Hướng 3 — mutant chính thức và răng đúng ca', f'Lệnh `python3 -B -u review_mutations.py official`: {len(rows)}/{len(rows)} mutant được chọn trả `giet_that`; đối chứng c18 đều `qua`. Bao gồm m134→c95/promisor_tat, m135→c94/promisor-gia-tri-la, m136→c95/git_dir_khac. Log nguyên nhân assertion: `evidence/official-mutants.log`.')

def own(name):
    before, after, target = VARIANTS[name]
    dr = TMP / name
    assert not dr.exists(), dr
    shutil.copytree(ROOT, dr, symlinks=True)
    p = dr / 'ops/bien_nhan_v2.py'
    src = p.read_text()
    assert src.count(before) == 1, (name, src.count(before))
    p.write_text(src.replace(before, after))
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    t = load(dr / 'ops/bien_nhan_v2_test.py', 'own_' + name)
    fn = next(f for f in t.CA if f.__name__.startswith(target))
    state, why = t._chay_1(fn)
    print(json.dumps(dict(mutant=name, before=before, after=after, target=fn.__name__, state=state, reason=why), ensure_ascii=False), flush=True)
    if state == 'qua':
        red = []
        for f in t.CA:
            result = t._chay_1(f)
            if result[0] != 'qua':
                red.append((f.__name__, result))
            print(f.__name__, result, flush=True)
        print(json.dumps(dict(summary=name, total=len(t.CA), passed=len(t.CA)-len(red), red=red), ensure_ascii=False), flush=True)
    else:
        assert state == 'giet_that', (state, why)
        print('control', t._chay_1(t.c18_neo_git_DUNG_thi_qua), flush=True)
    assert hashlib.sha256(p.read_bytes()).hexdigest() == digest
    print('mutant_source_unchanged=true', flush=True)

if __name__ == '__main__':
    official() if sys.argv[1] == 'official' else own(sys.argv[1])
