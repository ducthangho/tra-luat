# kiem_nhan_r12.py - moi nhan `KHÔNG ĐO ĐƯỢC` trong dac ta (ke ca bi ngat dong) phai o MOT trong ba dang:
# (i) ngay sau nhan (sau dau ** neu co) la " (lý do N" voi N trong danh sach DONG 1..5 cua §10;
# (ii) ngay truoc nhan la dau nhay kep: TRICH nhan cua mot revision hay luot cu;
# (iii) ngay truoc nhan la dau backtick: NHAC ten nhan (dinh nghia, luat, hang cua mot phep do).
import sys
t = " ".join(open(sys.argv[1], encoding="utf-8").read().split())
N = "KHÔNG ĐO ĐƯỢC"
i, sai, dem = t.find(N), [], 0
while i >= 0:
    dem += 1
    sau = t[i + len(N):].lstrip("*")
    co_ly_do = sau.startswith(" (lý do ") and sau[8:9] in ("1", "2", "3", "4", "5")
    if not (co_ly_do or t[i - 1:i] in (chr(34), chr(96))):
        sai.append(t[max(0, i - 70):i + len(N) + 25])
    i = t.find(N, i + 1)
print("nhan:", dem, "| sai dang:", len(sai))
for s in sai:
    print("   ", s)
sys.exit(1 if sai else 0)
