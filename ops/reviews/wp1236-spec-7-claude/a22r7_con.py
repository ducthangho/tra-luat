"""Tien trinh con A22 r7: 3 lop. argv: goc_cay che_do(cho_phep|cam_py_r6)"""
import sys, importlib.machinery, importlib.util, fnmatch
from pathlib import Path
GOC = Path(sys.argv[1]).resolve(); CHE_DO = sys.argv[2]
CAM = [(GOC / 'ops/kiem_ho_so_land.py').resolve(), (GOC / 'ops/land_evidence_nguon.py').resolve()]
ghi, mo = [], []
g_exec = importlib.machinery.SourceFileLoader.exec_module
def exec_boc(self, m): ghi.append(Path(self.path).resolve()); return g_exec(self, m)
importlib.machinery.SourceFileLoader.exec_module = exec_boc
g_spec = importlib.util.spec_from_file_location
def spec_boc(name, loc=None, *a, **k):
    if loc is not None: ghi.append(Path(loc).resolve())
    return g_spec(name, loc, *a, **k)
importlib.util.spec_from_file_location = spec_boc
def hook(ev, args):
    if ev == 'open' and isinstance(args[0], (str, bytes)) or (ev == 'open' and hasattr(args[0], '__fspath__')):
        try: p = Path(args[0] if not isinstance(args[0], bytes) else args[0].decode()).resolve()
        except Exception: return
        try: rel = p.relative_to(GOC).as_posix()
        except ValueError: return
        if p.suffix in ('.py', '.pyc'): mo.append(rel)
sys.addaudithook(hook)
sp = g_spec("gate_output_doi_chieu", GOC / 'ops/gate_output_doi_chieu.py')
m = importlib.util.module_from_spec(sp); sys.modules['gate_output_doi_chieu'] = m; sp.loader.exec_module(m)
m.kiem()
lop1 = any(p in CAM for p in ghi)
lop2 = any(getattr(x, '__file__', None) and Path(x.__file__).resolve() in CAM for x in list(sys.modules.values()))
if CHE_DO == 'cho_phep':
    OK = ['ops/gate_output_doi_chieu.py', 'ops/ci_provenance.py', 'ops/__pycache__/gate_output_doi_chieu.*.pyc', 'ops/__pycache__/ci_provenance.*.pyc']
    vi_pham = [r for r in mo if not any(fnmatch.fnmatchcase(r, o) for o in OK)]
else:
    vi_pham = [r for r in mo if (GOC / r).resolve() in CAM]
print(f"lop1={lop1!s:5} lop2={lop2!s:5} lop3={bool(vi_pham)!s:5} mo={sorted(set(mo))}")
