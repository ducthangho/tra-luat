"""A22 r6 (3 lop: boc loader + quet __file__ + audit open) khi da co .pyc cua tep dich."""
import sys, importlib.machinery, importlib.util, runpy
from pathlib import Path
DICH = (Path(__file__).parent / 'a22b' / 'dich.py').resolve()
PYC = Path(importlib.util.cache_from_source(str(DICH)))
ghi, mo, mo_tat_ca = [], [], []
goc_exec = importlib.machinery.SourceFileLoader.exec_module
def exec_boc(self, m): ghi.append(Path(self.path).resolve()); return goc_exec(self, m)
importlib.machinery.SourceFileLoader.exec_module = exec_boc
goc_spec = importlib.util.spec_from_file_location
def spec_boc(name, loc=None, *a, **k): ghi.append(Path(loc).resolve()); return goc_spec(name, loc, *a, **k)
importlib.util.spec_from_file_location = spec_boc
def hook(ev, args):
    if ev == 'open' and isinstance(args[0], str):
        p = Path(args[0]).resolve(); mo_tat_ca.append(p)
        if p == DICH: mo.append(p)
sys.addaudithook(hook)
def bat(ten, f):
    ghi.clear(); mo.clear(); mo_tat_ca.clear(); f()
    thay_file = any(getattr(m, '__file__', None) and Path(m.__file__).resolve() == DICH for m in list(sys.modules.values()))
    print(f'{ten:34} wrapper={DICH in ghi!s:5} __file__={thay_file!s:5} audit_open_dung_duong_dan={bool(mo)!s:5} audit_thay_pyc={PYC.resolve() in mo_tat_ca}')
    sys.modules.pop('dich', None)
sys.path.insert(0, str(DICH.parent))
print('pyc ton tai:', PYC.exists())
bat('import dich (co pyc)', lambda: __import__('dich'))
bat('runpy.run_path(pyc)', lambda: runpy.run_path(str(PYC)))
