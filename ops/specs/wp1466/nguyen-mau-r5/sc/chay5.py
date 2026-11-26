"""Bộ chạy của người soạn r5 (dựa trên chay4.py/chay_cu.py của r4). Dùng: python -B chay5.py <cây> <tmp> ca|moi|cu|adr"""
import os, sys, pathlib, tempfile, inspect, time
cay, tmp, che_do = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve(), sys.argv[3]
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
tmp = tmp / che_do; tmp.mkdir(parents=True, exist_ok=True); os.environ["TMPDIR"] = str(tmp); tempfile.tempdir = str(tmp)
sys.path.insert(0, str(cay / ".claude/dev")); os.chdir(cay)
import packet_loop_test as t, packet_loop_test_manh as sh
moi = [n for n, _ in t.CASES if n.startswith("doctrine_inv_")]
def lq(ten, fn):
    if ten.startswith(("doctrine_", "ac18_", "ac19_")): return True
    try: return "doctrine" in inspect.getsource(fn)
    except Exception: return False
ho_cu = {n for n, f in t.CASES if lq(n, f) and not n.startswith("doctrine_inv_")}
print("CA MOI", len(moi), "HO CU", len(ho_cu), "CASES", len(t.CASES), "TEN KHAC NHAU", len({n for n, _ in t.CASES}), "MUTANTS", len(t.MUTANTS), flush=True)
t0 = time.time()
if che_do in ("ca", "adr"):
    chon = (sorted(ho_cu) + moi + ["moc_dot_bien_phai_khop_DUNG_MOT_CHO"]) if che_do == "ca" else [n for n, _ in t.CASES if n.startswith("adr_song_")]
    kq = {}
    for n in chon: kq.update(t.chay_suite(t.CANONICAL, tmp / "ca", chi_chay={n}))
    do = {k: str(v)[:300] for k, v in kq.items() if v is not None}
    print("CHON", len(chon), "CHAY", len(kq), "DAT", sum(v is None for v in kq.values()), "KHONG DAT", len(do), "giay", round(time.time() - t0))
    for k, v in list(do.items())[:20]: print("  ", k, "→", v)
elif che_do == "moi":
    mm = {k for k in t.MUTANTS if k.startswith(("inv_", "t1466_"))}
    print("DOT BIEN MOI", len(mm), flush=True)
    kq = sh.chay(t, set(moi) | {"doctrine_scan_repo_that_sach", "doctrine_scan_sach_xanh", "moc_dot_bien_phai_khop_DUNG_MOT_CHO"}, lambda ten: mm & set(ten))
    print("KET QUA manh.chay:", (kq[0], len(kq[1]), kq[2], kq[3]), "giay", round(time.time() - t0))
elif che_do == "cu":
    cu = {k for k, v in t.MUTANTS.items() if not k.startswith(("inv_", "t1466_")) and set(v[2]) & ho_cu}
    print("DOT BIEN CU co dich trong ho", len(cu), flush=True)
    kq = sh.chay(t, ho_cu, lambda ten: cu & set(ten))
    print("KET QUA manh.chay:", (kq[0], len(kq[1]), kq[2], kq[3]), "giay", round(time.time() - t0))
