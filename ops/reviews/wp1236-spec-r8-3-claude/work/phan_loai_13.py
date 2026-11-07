"""Phân loại 'nhan_ma_nuot_loi' của 13 đột biến lớp I01: rc 0 + DA_CHAY (nuốt thật) hay DA_CHAY vắng (không chạy)."""
import os, sys, json, collections
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "soan"); sys.path.insert(0, S)
import dot_bien_r8, sinh_r8
out = {}
for ten, f in dot_bien_r8.DB_SINH.items():
    kq, lech, hong = sinh_r8.main(f)
    if not hong: continue
    c = collections.Counter("nuot_that" if (rc == 0 and dc) else ("khong_chay_rc0" if rc == 0 else "khong_chay_rc_khac_0") for (_, _, _, rc, dc) in hong)
    out[ten] = {"nhan_ma_nuot_loi": kq["nhan_ma_nuot_loi"], **c, "vd": [(r, s, rc, dc) for (r, s, k, rc, dc) in hong[:2]]}
json.dump(out, open("phan_loai_13.json", "w"), ensure_ascii=False, indent=1)
for k, v in out.items(): print(k, {a: b for a, b in v.items() if a != "vd"}, v["vd"][0])
