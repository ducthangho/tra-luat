"""A6 — đơn điệu so với base: đột biến nào base GIẾT (có khoá đỏ) thì nguyên mẫu/C cũng phải GIẾT.
Dùng: python3 doi_chieu_don_dieu.py <đầu ra ma_tran trên base> <đầu ra ma_tran trên C>. Thoát 0 khi không ca nào yếu đi."""
import re, sys


def doc(p):
    kq = {}
    for dong in open(p, encoding="utf-8"):
        m = re.match(r"(DAT|SAI) (\S+) run=(True|False) so_nhan=(\d+) do=(\S*)", dong)
        if m:
            kq[m.group(2)] = set(filter(None, m.group(5).split(",")))
    return kq


base, c = doc(sys.argv[1]), doc(sys.argv[2])
yeu = sorted(t for t, do in base.items() if do and t in c and not c[t])
thieu = sorted(t for t, do in base.items() if do and t not in c and not t.startswith("a7_"))
print("DON_DIEU: base giet %d ca do duoc; C yeu di %d; C thieu %d" % (sum(1 for d in base.values() if d), len(yeu), len(thieu)))
for t in yeu:
    print("YEU_DI", t, "base do=" + ",".join(sorted(base[t])))
for t in thieu:
    print("THIEU", t)
sys.exit(1 if yeu or thieu else 0)
