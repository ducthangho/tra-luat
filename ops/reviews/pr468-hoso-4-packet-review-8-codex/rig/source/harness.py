import contextlib, hashlib, importlib.util, io, json, pathlib, re, sys
BASE = pathlib.Path(__file__).resolve().parents[1]
OUT = BASE / 'do-review'
ROOT = BASE / 'cay-kho'

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m

s = (BASE / 'tai-lieu/LO-319-LINUX-BANG-CHUNG-XANH.md').read_text()
a = s.index('### Thiết kế H')
b = s.index('### Ca đang khoá', a)
blocks = re.findall(r'```python\n(.*?)\n```', s[a:b], re.S)
assert len(blocks) == 2
for name, code in zip(('h_tong.py', 'h_predicate.py'), blocks):
    (OUT / name).write_text(code + '\n')
H = {'re': re}
for code in blocks:
    exec(code, H)
C = module(BASE / 'tai-lieu/ci_dang_ky_test.py', 'consumer_review')
C.ROOT = ROOT
BASE_MOI = C.MOI.copy()
BASE_WINDOWS = C.MOI_WINDOWS.copy()
BASE_FN = C.bang_chung_xanh
C.bang_chung_xanh = H['bang_chung_xanh']
C.MOI = {p:(span, H['TONG'][p]) for p,span in BASE_MOI.items()}
C.MOI_WINDOWS = {p:tuple((span,H['TONG_WINDOWS'][p][i]) for i,span in enumerate(spans)) for p,spans in BASE_WINDOWS.items()}

def replay(path, text, mau=None, rc=0, windows=False, base=False):
    fn = C.bang_chung_xanh
    win = C.MOI_WINDOWS
    if base:
        C.bang_chung_xanh = BASE_FN
        C.MOI_WINDOWS = BASE_WINDOWS
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return C.chay_moi(moi={path: mau if mau is not None else (BASE_MOI[path] if base else C.MOI[path])}, cach_ly={},
                chay_mot=lambda _: (rc, text), doc_moi_truong=lambda: C.MOI_TRUONG_WINDOWS if windows else C.MOI_TRUONG_CI,
                doc_trong_ci=lambda: True, doc_nen_windows=lambda: windows)
    finally:
        C.bang_chung_xanh = fn
        C.MOI_WINDOWS = win

if __name__ == '__main__':
    print(json.dumps({'blocks':len(blocks), 'sha256_no_final_newline':[hashlib.sha256(x.encode()).hexdigest() for x in blocks],
        'sha256_with_final_newline':[hashlib.sha256((x+'\n').encode()).hexdigest() for x in blocks],
        'moi':len(C.MOI), 'windows_forms':sum(map(len,C.MOI_WINDOWS.values()))}, indent=2))
