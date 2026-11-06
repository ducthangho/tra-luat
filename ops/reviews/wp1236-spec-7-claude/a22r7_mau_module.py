import importlib.util
from pathlib import Path
_sp = importlib.util.spec_from_file_location("ci_provenance_x", Path(__file__).with_name("ci_provenance.py"))
cp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(cp)
#DOI_CHUNG#
def kiem(): return cp.X
