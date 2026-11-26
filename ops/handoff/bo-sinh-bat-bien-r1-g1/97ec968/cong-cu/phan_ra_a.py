"""Phân rã chi phí bộ test đợt A (ops/gate_output_doi_chieu_test.py) theo pha và theo ca, trong MỘT tiến trình. Chỉ đọc; không sửa tệp nào.

Ghi cho mỗi ca (pha CA), mỗi đột biến (pha DOT_BIEN) và mỗi tự kiểm (pha TU_KIEM): thời gian tường, CPU của chính tiến trình, CPU của
tiến trình con (getrusage RUSAGE_CHILDREN). CPU ít nhạy với tải máy hơn thời gian tường.
Dùng: python3 -B phan_ra_a.py <gốc clone> <tệp json ra>
"""
import json
import os
import resource
import runpy
import sys
import time
from pathlib import Path

goc, ra = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
os.chdir(goc)
sys.argv = [str(goc / "ops/gate_output_doi_chieu_test.py")]
g = runpy.run_path(sys.argv[0], run_name="phan_ra")
G = g["main"].__globals__


def con():
    r = resource.getrusage(resource.RUSAGE_CHILDREN)
    return r.ru_utime + r.ru_stime


so = []


def boc(pha, ham, ten_fn):
    def goi(*x):
        t, c, k = time.perf_counter(), time.process_time(), con()
        kq = ham(*x)
        so.append({"pha": pha, "ten": ten_fn(x), "wall": time.perf_counter() - t, "cpu": time.process_time() - c, "cpu_con": con() - k})
        return kq
    return goi


that_ca, that_db = G["chay_ca"], G["chay_dot_bien"]
dang_tu_kiem = [False]
G["chay_ca"] = boc("CA", that_ca, lambda x: x[0])
db = boc("DOT_BIEN", that_db, lambda x: x[0])
tk = boc("TU_KIEM", that_db, lambda x: x[0])
G["chay_dot_bien"] = lambda *x: (tk if x[0] in {t[0] for t in G["TU_KIEM"]} else db)(*x)
t0, c0, k0 = time.perf_counter(), time.process_time(), con()
rc = G["main"]([])
tong = {"wall": time.perf_counter() - t0, "cpu": time.process_time() - c0, "cpu_con": con() - k0, "rc": rc}
ra.write_text(json.dumps({"goc": str(goc), "tong": tong, "so": so}, ensure_ascii=False, indent=0), encoding="utf-8")
print(json.dumps(tong), file=sys.stderr)
