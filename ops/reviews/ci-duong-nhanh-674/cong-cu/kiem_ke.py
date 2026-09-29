#!/usr/bin/env python3
"""kiem_ke.py — kiem ke DEM TU CAU TRUC cua ops/ci_duong_nhanh_test.py (KHONG ghim so). Chay trong `cay/`: python3 -B ../goi/kiem_ke.py"""
import collections, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
tep = Path("ops/ci_duong_nhanh_test.py")
g = {"__name__": "kiem_ke", "__file__": str(tep.resolve())}
exec(compile(tep.read_text(encoding="utf-8"), str(tep.resolve()), "exec"), g)
CA, DB = g["CA"], g["DOT_BIEN"]
nhom = g["phan_hoach_ca"]()   # nguon duy nhat cua phan ra (ham trong tep test; ca t96 canh tinh khong giao nhau/phu kin)
print("CA tong:", len(CA), "| phan hoach:", {k: len(v) for k, v in nhom.items()}, "| cong lai:", sum(len(v) for v in nhom.values()))
print("ca tu kiem:", nhom["tu_kiem"])
print("DOT_BIEN tong:", len(DB), "| tep bi dot bien:", dict(collections.Counter(tv[0] for _, tv, _ in DB)))
print("so dot bien theo ca dich dau tien:", dict(collections.Counter(d[0] for _, _, d in DB)))
print("tu kiem phan hang: MAU_RC =", len(g["MAU_RC"]), "| TU_KIEM_DOT_BIEN =", len(g["TU_KIEM_DOT_BIEN"]),
      "(khong nam trong DOT_BIEN)")
print("IF_BUOC_CHUAN (buoc mang if theo job):", {j: len(d) for j, d in g["IF_BUOC_CHUAN"].items()})
print("BO_QUA (buoc bi bo theo che_do):", {j: len(d) for j, d in g["BO_QUA"].items()})
print("CA_DU_LIEU_CHUAN:", len(g["CA_DU_LIEU_CHUAN"]), "ca:", list(g["CA_DU_LIEU_CHUAN"]))
m = g["nap_module"]()
t0 = time.time(); loi = m.kiem_ca_du_lieu(Path("."), __import__("subprocess").run); print("ba ca du lieu tren kho that: loi =", loi, f"| {time.time() - t0:.1f}s (may nay)")
