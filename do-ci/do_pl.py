# do-ci/do_pl.py — NHANH DO TAM, khong merge. Bam gio tung ca / tung dot bien cua
# .claude/dev/packet_loop_test.py ma KHONG sua tep test: nap module, boc tung ham ca
# trong CASES bang bo bam gio, moc vao _phan_loai_dot_bien de danh dau dau moi dot bien,
# roi goi main() nhu CI goi.
#
#   --manh i/N : chi chay ca nen co chi so % N == i va dot bien co chi so % N == i
#                (mo phong chia manh; so loi "thieu ca bat buoc" o che do nay la DO CHIA,
#                khong phai loi that — doc truong `ca_do` thay vi rc).
#   --out TEP  : ghi JSON ket qua (dat NGOAI cay kho de khong lam ban snapshot).
import argparse
import functools
import importlib.util
import json
import os
import platform
import sys
import time
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--manh")
ap.add_argument("--out", required=True)
a = ap.parse_args()

ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT / ".claude" / "dev"
TEST = DEV / "packet_loop_test.py"
sys.path.insert(0, str(DEV))
sys.argv = [str(TEST)]

T0 = time.perf_counter()
spec = importlib.util.spec_from_file_location("packet_loop_test", TEST)
m = importlib.util.module_from_spec(spec)
sys.modules["packet_loop_test"] = m
spec.loader.exec_module(m)
T_IMPORT = time.perf_counter() - T0

I = N = None
if a.manh:
    I, N = (int(x) for x in a.manh.split("/"))

REC = []          # (dot_bien|None, ca, do_sau, giay, dat)
MUT = []          # [ten, bat_dau, ket_thuc]
STATE = {"mut": None, "depth": 0}


def boc(ten, fn):
    @functools.wraps(fn)
    def w(c):
        STATE["depth"] += 1
        t = time.perf_counter()
        dat = False
        try:
            r = fn(c)
            dat = True
            return r
        finally:
            REC.append((STATE["mut"], ten, STATE["depth"], time.perf_counter() - t, dat))
            STATE["depth"] -= 1
    return w


m.CASES = [(n, boc(n, f)) for n, f in m.CASES]

_goc_pl = m._phan_loai_dot_bien


def _pl(ten_mut, *x, **k):
    if sys._getframe(1).f_code.co_name == "_legacy_main":
        now = time.perf_counter()
        if MUT and MUT[-1][2] is None:
            MUT[-1][2] = now
        MUT.append([ten_mut, now, None])
        STATE["mut"] = ten_mut
    return _goc_pl(ten_mut, *x, **k)


m._phan_loai_dot_bien = _pl

if N:
    m.MUTANTS = {k: v for j, (k, v) in enumerate(m.MUTANTS.items()) if j % N == I}
    _goc_cs = m.chay_suite

    def _cs(script, tmp, chi_chay=None):
        if chi_chay is None and Path(tmp).name == "baseline":
            ten = [n for n, _ in m.CASES]
            chi_chay = {n for j, n in enumerate(ten) if j % N == I}
        return _goc_cs(script, tmp, chi_chay)

    m.chay_suite = _cs

T_MAIN = time.perf_counter()
rc = None
loi_main = None
try:
    rc = m.main()
except BaseException as ex:  # noqa: BLE001 — do dac, khong phai gate
    loi_main = f"{type(ex).__name__}: {ex}"
T_END = time.perf_counter()
if MUT and MUT[-1][2] is None:
    MUT[-1][2] = T_END

t_mut0 = MUT[0][1] if MUT else T_END
nen = [r for r in REC if r[0] is None and r[2] == 1]
out = dict(
    os=platform.system(), nproc=os.cpu_count(),
    affinity=len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None,
    manh=a.manh, rc=rc, loi_main=loi_main,
    giay_import=T_IMPORT, giay_nen=t_mut0 - T_MAIN, giay_dot_bien=T_END - t_mut0, giay_tong=T_END - T0,
    so_ca_nen=len(nen), so_ca_nen_do=sum(1 for r in nen if not r[4]),
    ca_nen=[dict(ca=r[1], giay=round(r[3], 3), dat=r[4]) for r in nen],
    ca_long=[dict(ca=r[1], do_sau=r[2], giay=round(r[3], 3)) for r in REC if r[0] is None and r[2] > 1],
    dot_bien=[dict(ten=t, giay=round(e - b, 3)) for t, b, e in MUT],
    ca_trong_dot_bien=[dict(dot_bien=r[0], ca=r[1], giay=round(r[3], 3), dat=r[4]) for r in REC if r[0] is not None and r[2] == 1],
)
Path(a.out).write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")

# --- tom tat ra log ---------------------------------------------------------------------
print("\n=== DO_PL TOM TAT ===")
print(f"os={out['os']} nproc={out['nproc']} affinity={out['affinity']} manh={a.manh} rc={rc} loi_main={loi_main}")
print(f"import={T_IMPORT:.1f}s nen={out['giay_nen']:.1f}s dot_bien={out['giay_dot_bien']:.1f}s tong={out['giay_tong']:.1f}s")
print(f"ca nen chay={len(nen)} do={out['so_ca_nen_do']} · dot bien={len(MUT)}")
print("-- 40 ca nen cham nhat (giay):")
for r in sorted(nen, key=lambda r: -r[3])[:40]:
    print(f"  {r[3]:8.2f}  {r[1]}{'' if r[4] else '  [DO]'}")
cum = {}
for r in nen:
    p = r[1].split("_")[0]
    cum[p] = cum.get(p, 0) + r[3]
print("-- tong theo tien to ten ca (top 25):")
for p, s in sorted(cum.items(), key=lambda kv: -kv[1])[:25]:
    print(f"  {s:8.1f}  {p}")
print("-- 30 dot bien cham nhat (giay):")
for t, b, e in sorted(MUT, key=lambda x: -(x[2] - x[1]))[:30]:
    print(f"  {e - b:8.2f}  {t}")
ca_mut = {}
for r in REC:
    if r[0] is not None and r[2] == 1:
        ca_mut[r[1]] = ca_mut.get(r[1], 0) + r[3]
print("-- ca ton nhieu giay nhat TRONG pha dot bien (cong don, top 25):")
for k, s in sorted(ca_mut.items(), key=lambda kv: -kv[1])[:25]:
    print(f"  {s:8.1f}  {k}")
print(f"-- tong giay ca trong pha dot bien = {sum(ca_mut.values()):.1f}s / pha dot bien {out['giay_dot_bien']:.1f}s")
