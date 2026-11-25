import os, sys, pathlib, tempfile, inspect
here = pathlib.Path(__file__).parent.resolve(); cay = here / "cay"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
tmp = here / "tmp" / "cu"; tmp.mkdir(parents=True, exist_ok=True); os.environ["TMPDIR"] = str(tmp); tempfile.tempdir = str(tmp)
sys.path.insert(0, str(cay / ".claude/dev")); os.chdir(cay)
import packet_loop_test as t, packet_loop_test_manh as sh
def lq(ten, fn):
    if ten.startswith(("doctrine_", "ac18_", "ac19_")): return True
    try: return "doctrine" in inspect.getsource(fn)
    except Exception: return False
ho = {n for n, f in t.CASES if lq(n, f) and not n.startswith("doctrine_inv_")}
cu = {k for k, v in t.MUTANTS.items() if not k.startswith(("inv_", "t1466_")) and set(v[2]) & ho}
print("HO CU", len(ho), "DOT BIEN CU co dich trong ho", len(cu), flush=True)
kq = sh.chay(t, ho, lambda ten: cu & set(ten))
print("KET QUA manh.chay:", (kq[0], len(kq[1]), kq[2], kq[3]))
