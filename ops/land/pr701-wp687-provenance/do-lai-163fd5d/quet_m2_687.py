"""Phep quet M2 (spec r3 §3) tren BYTES DA LAND: chay THAT moi ca trong CA (tru t125 — no tu sinh hai lan chay toan
suite) voi nen `nt` MO PHONG (`_ly_do_bo_qua_workflow` ep nen='nt', dung cach t193.nem_nt va drv.py cua reviewer r3),
dem ca nem `BoQuaNen` va cap (tep, job). So voi SO_BO_QUA cua tep.

Dung: python3 -B quet_m2_687.py <cay_day_du> <tep_json_ra>
Gioi han (khai): mo phong chi doi nhanh nen qua `_ly_do_bo_qua_workflow`; mot ca chi nem khi os.name=='nt' THAT o
noi khac thi phep quet khong thay (grep `raise BoQuaNen`: hai diem that 2757/10870 + ca gia).
"""
import contextlib
import importlib.util
import io
import json
import sys
import time
from pathlib import Path

root, ra = sys.argv[1], sys.argv[2]
sys.argv = [root + "/ops/lease_publish_test.py"]
sys.path.insert(0, root + "/ops")
spec = importlib.util.spec_from_file_location("lpt", root + "/ops/lease_publish_test.py")
m = importlib.util.module_from_spec(spec)
sys.modules["lpt"] = m
spec.loader.exec_module(m)
goc = m._ly_do_bo_qua_workflow
m._ly_do_bo_qua_workflow = lambda t, j, nen=None, job=None: goc(t, j, nen=nen or "nt", job=job)
res, t0 = {}, time.time()
for fn in list(m.CA):
    nm = fn.__name__
    if nm.startswith("t125"):
        res[nm] = ["BO_KHOI_QUET"]
        continue
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            fn()
        res[nm] = ["QUA"]
    except m.BoQuaNen as e:
        res[nm] = ["NEM", str(Path(e.tep).resolve()), e.ten_job]
    except BaseException as e:  # noqa: BLE001
        res[nm] = ["KHAC", type(e).__name__, str(e)[:160]]
nem = {k: v for k, v in res.items() if v[0] == "NEM"}
so = {k: [str(Path(v[0]).resolve()), v[1]] for k, v in m.SO_BO_QUA.items()}
tom = {"so_ca": len(m.CA), "QUA": sum(v[0] == "QUA" for v in res.values()), "NEM": len(nem),
       "KHAC": sorted(k for k, v in res.items() if v[0] == "KHAC"), "BO_KHOI_QUET": [k for k, v in res.items()
                                                                                    if v[0] == "BO_KHOI_QUET"],
       "tap_nem_bang_so": sorted(nem) == sorted(so) and all(nem[k][1:] == so[k] for k in so if k in nem),
       "nem_ngoai_so": sorted(set(nem) - set(so)), "so_khong_nem": sorted(set(so) - set(nem)),
       "cap_nem": sorted({(v[1], v[2]) for v in nem.values()}), "giay": round(time.time() - t0, 1)}
json.dump({"tom": tom, "res": res}, open(ra, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(json.dumps(tom, ensure_ascii=False))
