"""Do A22 cua r5: boc SourceFileLoader.exec_module + spec_from_file_location roi nap tep dich bang 4 cach."""
import sys, importlib.machinery, importlib.util, runpy
from pathlib import Path
DICH = (Path(__file__).parent / 'a22' / 'dich.py').resolve()
ghi = []
goc_exec = importlib.machinery.SourceFileLoader.exec_module
def exec_boc(self, m): ghi.append(Path(self.path).resolve()); return goc_exec(self, m)
importlib.machinery.SourceFileLoader.exec_module = exec_boc
goc_spec = importlib.util.spec_from_file_location
def spec_boc(name, loc=None, *a, **k): ghi.append(Path(loc).resolve()); return goc_spec(name, loc, *a, **k)
importlib.util.spec_from_file_location = spec_boc
mo = []
sys.addaudithook(lambda ev, args: mo.append(Path(args[0]).resolve()) if ev == 'open' and isinstance(args[0], str) and args[0].endswith('dich.py') else None)
def bat(ten, f):
    ghi.clear(); mo.clear(); f()
    thay_file = any(getattr(m, '__file__', None) and Path(m.__file__).resolve() == DICH for m in list(sys.modules.values()))
    print(f'{ten:28} wrapper_ghi={DICH in ghi!s:5} sys.modules___file__={thay_file!s:5} audit_open={DICH in mo}')
    sys.modules.pop('dich', None)
sys.path.insert(0, str(DICH.parent))
bat('import dich', lambda: __import__('dich'))
def c2():
    s = importlib.util.spec_from_file_location('x', DICH); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
bat('spec_from_file_location', c2)
bat('runpy.run_path', lambda: runpy.run_path(str(DICH)))
bat('exec(compile(open()))', lambda: exec(compile(open(DICH).read(), str(DICH), 'exec'), {}))
