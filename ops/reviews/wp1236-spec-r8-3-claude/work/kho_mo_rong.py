"""Thử đề xuất: kho mở rộng = hạt giống gồm năm LENH (ba dạng DANG) + ống 2 và 3 thành phần; (1) chèn mỗi ký tự KT vào MỌI vị trí
của mỗi hạt và thay mỗi dấu cách; (2) chèn mỗi TOKEN (toán tử, tuỳ chọn -s -n -h -c -u, từ khoá) ở MỌI ranh giới token; (3) thay mỗi
dấu tách ` | ` bằng mỗi toán tử OP2. Chỉ đo vế (a) (lệch tham chiếu) cho 6 đột biến sống sót + 32 đột biến lớp I01."""
import os, sys, json
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "soan"); sys.path.insert(0, S); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gram, sinh_r8, dot_bien_r8
from song_sot_v3 import MUT
L = sinh_r8.LENH
hat = list(L) + [f"{a} | {b}" for a in L for b in L] + [f"{a} | {b} | {c}" for a in L[:3] for b in L[1:4] for c in L[2:]]
TOK = ["||", "&&", ";", "&", "|", "|&", "!", "-s", "-n", "-h", "-c", "-u", "-m", "--", "time", "exec", "A=1", "{", "}", "(", ")", "#", ">x", "2>&1"]
out = set()
for h in hat:
    for c in sinh_r8.KT:
        for i in range(len(h) + 1): out.add(h[:i] + c + h[i:])
        out.add(h.replace(" ", c))
    t = h.split(" ")
    for i in range(len(t) + 1):
        for x in TOK: out.add(" ".join(t[:i] + [x] + t[i:]))
    parts = h.split(" | ")
    for j in range(1, len(parts)):
        for op in sinh_r8.OP2:
            for sep in (f" {op} ", op):
                out.add(" | ".join(parts[:j]) + sep + " | ".join(parts[j:]))
kho = sorted(out)
n = len(kho) * 6
kq = {"hat": len(hat), "than": len(kho), "dau_vao": n}
ds = {**MUT, **dot_bien_r8.DB_SINH}
for ten, f in ds.items():
    kq[ten] = sum(f(r, s) != gram.cu_phap_run(r, s) for t in kho for s in sinh_r8.SHELL for r in (t, t + "\n"))
nhan = sum(gram.cu_phap_run(r, s) is None for t in kho for s in sinh_r8.SHELL for r in (t, t + "\n"))
kq["tham_chieu_nhan"] = nhan
json.dump(kq, open("kho_mo_rong.json", "w"), ensure_ascii=False, indent=1)
print({k: v for k, v in kq.items() if not k.startswith("m-S")}); print("32 lop I01 bi bat:", sum(kq[k] > 0 for k in dot_bien_r8.DB_SINH), "/", len(dot_bien_r8.DB_SINH))
