"""Đề xuất cho vế (5)/A14-S3b: (i) thêm vào gián điệp các thân MỘT DÒNG KHÔNG LF (dạng plain scalar thật của 25/30 bước luật); (ii) A14-S3b
chạy mỗi vế của bảng cả bản BỎ LF cuối. Đo: mọi biến đổi T của thu_goi_v6 có bị bắt không. Chạy từ gốc kho: python3 -I ../work/v6/thu_goi_de_xuat_v6.py"""
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import thu_goi_v6 as G, gram
X = "python ops/x.py"
GD_THEM = [(v, sh) for v in [f"{X} || true", f"{X} || :", f"{X} || exit 0", f"{X} &", f"! {X}", f"{X}\r\n", f"{X}\t", f"python  ops/x.py",
                             f" {X}", f"{X} "] for sh in (None, "bash")]
S3B_KHONG_LF = [(r[:-1], s) for r, s in G.S3B if type(r) is str and r.endswith("\n")]
kq = {}
for ten, f in G.T.items():
    kq[ten] = {"gian_diep_cu": G.dem_doi(f, G.GD), "gian_diep_them": G.dem_doi(f, GD_THEM),
               "S3b_cu": G.dem_lech(f, G.S3B) + G.dem_lech(f, G.S3B_MAU), "S3b_khong_lf": G.dem_lech(f, S3B_KHONG_LF)}
    print(f"{ten:28} {kq[ten]}")
print("S3b bo LF:", len(S3B_KHONG_LF), "ve them; tham chieu nhan trong do:", sum(gram.cu_phap_run(r, s) is None for r, s in S3B_KHONG_LF))
json.dump(kq, open(os.path.join(D, "thu_goi_de_xuat_v6.json"), "w"), ensure_ascii=False, indent=1)
sys.exit(1 if any(v["gian_diep_them"] == 0 and v["S3b_khong_lf"] == 0 and v["gian_diep_cu"] == 0 and v["S3b_cu"] == 0 for v in kq.values()) else 0)
