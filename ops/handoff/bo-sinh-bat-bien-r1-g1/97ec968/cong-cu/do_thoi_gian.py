"""Đo thời gian hai bộ test (mục 4 đặc tả) trên hai clone nen/sau: N cặp, TUẦN TỰ, đảo thứ tự xen kẽ (cặp lẻ nen→sau, cặp chẵn sau→nen).
Ghi cho MỖI lượt: thời gian tường và CPU của cây tiến trình con (getrusage RUSAGE_CHILDREN, gồm mọi tiến trình con của bộ test) — CPU ít
nhạy với tải máy hơn thời gian tường. Công bố MỌI mẫu. Dùng: python3 -B do_thoi_gian.py <thư mục chứa nen/ và sau/> <thư mục ra> <N>
"""
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path

goc, ra, n = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
ra.mkdir(parents=True, exist_ok=True)
BO = (("B", "ops/land_evidence_nguon_test.py"), ("A", "ops/gate_output_doi_chieu_test.py"))
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
so = []
for ve in ("nen", "sau"):
    h = subprocess.run(["git", "-C", str(goc / ve), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    b = subprocess.run(["git", "-C", str(goc / ve), "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    print(f"== {ve} {h} ban={len(b.splitlines())}", flush=True)
for cap in range(1, n + 1):
    thu_tu = ("nen", "sau") if cap % 2 else ("sau", "nen")
    for bo, tep in BO:
        for ve in thu_tu:
            r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
            t0, bat_dau = time.perf_counter(), time.strftime("%H:%M:%SZ", time.gmtime())
            p = subprocess.run([sys.executable, "-B", tep], cwd=goc / ve, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
            wall = time.perf_counter() - t0
            r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
            cpu = (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime)
            (ra / f"{bo}-{ve}-cap{cap}.log").write_text(p.stdout + p.stderr, encoding="utf-8")
            duoi = [d for d in p.stdout.splitlines() if d.startswith(("CA:", "DOT BIEN:", "TU KIEM", "TONG:"))]
            so.append({"cap": cap, "bo": bo, "ve": ve, "bat_dau": bat_dau, "wall": round(wall, 2), "cpu": round(cpu, 2), "rc": p.returncode, "duoi": duoi})
            print(f"cap {cap} | {bo} | {ve} | rc={p.returncode} | wall {wall:.1f}s | cpu {cpu:.1f}s | {' · '.join(duoi)}", flush=True)
(ra / "thoi_gian.json").write_text(json.dumps(so, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nDELTA (sau - nen) tung cap:")
for bo, tran in (("B", 30), ("A", 5)):
    for cap in range(1, n + 1):
        x = {s["ve"]: s for s in so if s["bo"] == bo and s["cap"] == cap}
        dw, dc = x["sau"]["wall"] - x["nen"]["wall"], x["sau"]["cpu"] - x["nen"]["cpu"]
        print(f"  bo {bo} cap {cap}: wall {x['nen']['wall']:.1f} -> {x['sau']['wall']:.1f} ({dw:+.1f}s) · cpu {x['nen']['cpu']:.1f} -> {x['sau']['cpu']:.1f} ({dc:+.1f}s) · tran +{tran}s · {'TRONG TRAN' if dw <= tran else 'VUOT TRAN (wall)'}")
print("XONG TRON VEN do_thoi_gian")
