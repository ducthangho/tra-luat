"""Driver TRONG TIEN TRINH cho MOT ca dich tren mot cay (ban sao tam). In MOT dong JSON cuoi.

Lop A cua bo phan hang (lop B = khop chuoi ky vong, lop C = CLI --chi-ca: o do_l5_687.py):
  CHOT    = ngoai le la TinHieuChotCa (lop rieng cua tep) nem tu `chot()`, HOAC AssertionError TRAN nem tu `bang()`,
            VA khung cua CHINH ca dich nam tren traceback.
  DO_KHAC = moi ngoai le khac (TypeError, KeyError, NotImplementedError, ...), hoac khung cuoi khong phai chot/bang,
            hoac khung ca dich vang mat — KHONG duoc tinh giet.
  QUA     = ca chay het khong nem.
Dua tren mut/mdrv.py cua reviewer r3 (spec-goc/mdrv.py), them: ten lop day du, chuoi MRO, thong diep dai hon.
"""
import contextlib
import importlib.util
import io
import json
import sys
import traceback

root, pref = sys.argv[1], sys.argv[2]
sys.argv = [root + "/ops/lease_publish_test.py"]
sys.path.insert(0, root + "/ops")
spec = importlib.util.spec_from_file_location("lpt", root + "/ops/lease_publish_test.py")
m = importlib.util.module_from_spec(spec)
sys.modules["lpt"] = m
try:
    spec.loader.exec_module(m)
except BaseException as e:  # noqa: BLE001
    print(json.dumps([{"ca": pref, "A": "LOAD_FAIL", "cls": type(e).__name__, "msg": str(e)[:300]}], ensure_ascii=False))
    sys.exit(0)
fns = [f for f in m.CA if f.__name__.startswith(pref)]
out = []
if not fns:
    out.append({"ca": pref, "A": "KHONG_CO_CA"})
for fn in fns:
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            fn()
        out.append({"ca": fn.__name__, "A": "QUA"})
    except BaseException as e:  # noqa: BLE001
        tb = traceback.extract_tb(e.__traceback__)
        last = tb[-1].name if tb else ""
        inca = any(f.name == fn.__name__ for f in tb)
        la_chot = isinstance(e, m.TinHieuChotCa) and last == "chot"
        la_bang = type(e) is AssertionError and last == "bang"
        a = "CHOT" if (la_chot or la_bang) and inca else "DO_KHAC"
        out.append({"ca": fn.__name__, "A": a, "cls": type(e).__name__, "mro_chot": isinstance(e, m.TinHieuChotCa),
                    "last": last, "inca": inca, "msg": str(e)[:600].replace("\n", " ")})
print(json.dumps(out, ensure_ascii=False))
