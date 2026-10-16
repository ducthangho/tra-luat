import importlib.util, os, sys, json, pathlib
R = pathlib.Path(sys.argv[1]); d = R / ".claude/dev"
def nap(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
T = nap(d / "doc_receipt_thu_hoi_test.py", "t"); M = nap(d / "doc_receipt_thu_hoi.py", "m")
anh = lambda: (sys.get_int_max_str_digits(), os.environ.get("PYTHONINTMAXSTRDIGITS"))
truoc = anh(); T.ca(M, "so_dai_vuot", T._SO(T.LIM + 1), ("K1",)); sau_ok = anh()
try:
    T.ca(M, "sai", T.ma(T.FIX), ("K1",)); loi = None
except T.TinHieuChotCa as e:
    loi = "TinHieuChotCa"
print(json.dumps({"truoc": truoc, "sau_ok": sau_ok, "sau_nem": anh(), "nem": loi, "khoi_phuc": truoc == sau_ok == anh()}))
