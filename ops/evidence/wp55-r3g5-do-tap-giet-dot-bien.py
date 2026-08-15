#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ĐO tập ca mà mỗi đột biến thật sự giết, rồi so với tập KHAI trong MUTANTS.

Không đoán: in ra `THIEU` (khai mà không chết) và `THUA` (chết mà không khai).
"""
import pathlib
import sys
import tempfile

p = pathlib.Path(".claude/dev/packet_loop_test.py")
ns = {"__name__": "notmain", "__file__": str(p)}
exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), ns)

CANONICAL = ns["CANONICAL"]
MUTANTS = ns["MUTANTS"]
CASES = ns["CASES"]
chay_suite = ns["chay_suite"]

goc = CANONICAL.read_text(encoding="utf-8")
moi_ca = [t for t, _ in CASES]
chi = sys.argv[1:] or list(MUTANTS)

with tempfile.TemporaryDirectory(prefix="do_kill_") as td:
    tmp = pathlib.Path(td)
    for ten in chi:
        tim, thay, khai = MUTANTS[ten]
        sua = list(tim) if thay is None else [(tim, thay)]
        thieu_neo = [a for a, _ in sua if a not in goc]
        if thieu_neo:
            print(f"\n### {ten}\n  MO_NEO_KHONG_THAY: {thieu_neo[0]!r}", flush=True)
            continue
        nd = goc
        for a, b in sua:
            nd = nd.replace(a, b, 1)
        if nd == goc:
            print(f"\n### {ten}\n  KHONG_DOI", flush=True)
            continue
        d = tmp / ten
        d.mkdir(parents=True, exist_ok=True)
        m = d / "packet_loop.py"
        m.write_text(nd, encoding="utf-8", newline="\n")
        ket = chay_suite(m, d)
        chet = sorted(t for t in moi_ca if ket.get(t) is not None)
        khai_s = sorted(khai)
        thieu = [t for t in khai_s if t not in chet]
        thua = [t for t in chet if t not in khai_s]
        trang = "OK" if not thieu and not thua else "LECH"
        print(f"\n### {ten}  [{trang}] chết {len(chet)} / khai {len(khai_s)}", flush=True)
        if thieu:
            print(f"  THIEU (khai mà KHÔNG chết): {thieu}", flush=True)
        if thua:
            print(f"  THUA  (chết mà KHÔNG khai): {thua}", flush=True)
        print(f"  DO_DUOC = {chet}", flush=True)
