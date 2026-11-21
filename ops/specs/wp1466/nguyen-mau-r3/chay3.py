import os, sys, pathlib, tempfile, inspect, json, time
here = pathlib.Path(__file__).parent.resolve(); cay = here / "cay"; che_do = sys.argv[1]
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
tmp = here / "tmp" / che_do; tmp.mkdir(parents=True, exist_ok=True); os.environ["TMPDIR"] = str(tmp); tempfile.tempdir = str(tmp)
sys.path.insert(0, str(cay / ".claude/dev")); os.chdir(cay)
import packet_loop_test as t, packet_loop_test_manh as sh
moi = [n for n, _ in t.CASES if n.startswith("doctrine_inv_")]
def lq(ten, fn):
    if ten.startswith(("doctrine_", "ac18_", "ac19_")): return True
    try: return "doctrine" in inspect.getsource(fn)
    except Exception: return False
if che_do == "ca":
    chon = [n for n, f in t.CASES if lq(n, f)]; kq = {}; t0 = time.time()
    for n in chon: kq.update(t.chay_suite(t.CANONICAL, tmp / "ca", chi_chay={n}))
    do = {k: str(v)[:230] for k, v in kq.items() if v is not None}
    print("MOI", len(moi), "HO DOCTRINE", len(chon), "DAT", sum(v is None for v in kq.values()), "KHONG DAT", len(do), "giay", round(time.time() - t0))
    for k, v in list(do.items())[:8]: print("  ", k, "→", v)
else:
    mm = {k for k in t.MUTANTS if k.startswith(sys.argv[2] if len(sys.argv) > 2 else ("inv_", "t1466_"))}
    print("CA MOI", len(moi), "DOT BIEN MOI", len(mm), flush=True)
    kq = sh.chay(t, set(moi) | {"doctrine_scan_repo_that_sach", "doctrine_scan_sach_xanh"}, lambda ten: mm & set(ten))
    print("KET QUA manh.chay:", (kq[0], len(kq[1]), kq[2], kq[3]))
