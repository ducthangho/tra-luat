"""So phân rã chi phí bộ A giữa nen và sau (các tệp json của phan_ra_a.py). In tổng theo pha, các ca/đột biến lệch nhiều nhất.
Dùng: python3 so_phan_ra.py <dir>   (đọc nen-*.json, sau-*.json)"""
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

d = Path(sys.argv[1])
ve = {v: [json.loads(p.read_text()) for p in sorted(d.glob(f"{v}-*.json"))] for v in ("nen", "sau")}
print("TONG (moi mau):")
for v, ms in ve.items():
    for i, m in enumerate(ms, 1):
        t = m["tong"]
        print(f"  {v}-{i}: wall {t['wall']:.1f}s · cpu {t['cpu']:.1f}s · cpu_con {t['cpu_con']:.1f}s · cpu+con {t['cpu'] + t['cpu_con']:.1f}s · rc {t['rc']}")


def gom(m, khoa):
    out = defaultdict(float)
    for s in m["so"]:
        out[khoa(s)] += s["wall"] if False else 0
        out[khoa(s)] += s["cpu"] + s["cpu_con"]
    return out


def theo(v, khoa):   # trung vị qua các mẫu
    ms = [gom(m, khoa) for m in ve[v]]
    keys = set().union(*ms)
    return {k: statistics.median(m.get(k, 0.0) for m in ms) for k in keys}


print("\nCPU+con theo PHA (trung vi qua mau):")
pn, ps = theo("nen", lambda s: s["pha"]), theo("sau", lambda s: s["pha"])
for k in sorted(set(pn) | set(ps)):
    print(f"  {k:9s} nen {pn.get(k, 0):7.1f}s · sau {ps.get(k, 0):7.1f}s · delta {ps.get(k, 0) - pn.get(k, 0):+6.1f}s")
print(f"  {'TONG':9s} nen {sum(pn.values()):7.1f}s · sau {sum(ps.values()):7.1f}s · delta {sum(ps.values()) - sum(pn.values()):+6.1f}s")
for pha in ("CA", "DOT_BIEN"):
    n, s = theo("nen", lambda x, p=pha: (x["pha"], x["ten"])), theo("sau", lambda x, p=pha: (x["pha"], x["ten"]))
    rows = [(k[1], n.get(k), s.get(k)) for k in set(n) | set(s) if k[0] == pha]
    moi = [r for r in rows if r[1] is None]
    rows = sorted((r for r in rows if r[1] is not None and r[2] is not None), key=lambda r: abs(r[2] - r[1]), reverse=True)
    print(f"\n{pha}: chi co o sau: " + ", ".join(f"{r[0]} {r[2]:.2f}s" for r in moi))
    print(f"{pha}: 8 muc lech nhieu nhat (cpu+con, trung vi): " + " · ".join(f"{r[0]} {r[1]:.2f}->{r[2]:.2f}" for r in rows[:8]))
    if rows:
        print(f"{pha}: tong lech cac muc chung: {sum(r[2] - r[1] for r in rows):+.2f}s tren {len(rows)} muc")
