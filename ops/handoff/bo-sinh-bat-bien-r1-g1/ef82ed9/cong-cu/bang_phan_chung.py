"""In dòng `DO:` QUAN SÁT ĐƯỢC của từng phản chứng: chạy các ca phản chứng (c39, c40 của test đợt B; a136 của test đợt A) và ghi lại
mọi lời gọi `chay_ca` BÊN TRONG chúng (tên ca đích, rc, dòng). Chỉ đọc; không sửa tệp nào. Dùng: python3 -B bang_phan_chung.py <gốc kho>"""
import runpy
import sys
from pathlib import Path

goc = Path(sys.argv[1]).resolve()
for tep, cac_ca in (("ops/land_evidence_nguon_test.py", ("c39_c37_do_khi_bo_sinh_lech_mien", "c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o")),
                    ("ops/gate_output_doi_chieu_test.py", ("a136_a135_do_khi_bo_sinh_lech_mien",))):
    sys.argv = [str(goc / tep)]
    g = runpy.run_path(str(goc / tep), run_name="bang_phan_chung")
    that = g["chay_ca"]
    for ca in cac_ca:
        so = []

        def ghi(ten, _so=so):
            rc, dong = that(ten)
            _so.append((ten, rc, dong))
            return rc, dong
        nap_sua_that = g.get("nap_sua")

        def nap_sua_ghi(*x, _so=so):   # ban sao trong bo nho goi chay_ca RIENG cua no: boc lai de ghi (ten duoc danh dau "[ban sua]")
            mod = nap_sua_that(*x)
            if hasattr(mod, "chay_ca"):
                goc_mod = mod.chay_ca

                def ghi_mod(ten):
                    rc, dong = goc_mod(ten)
                    _so.append((ten + " [ban sua trong bo nho]", rc, dong))
                    return rc, dong
                mod.chay_ca = ghi_mod
            return mod
        g["CA"][ca].__globals__["chay_ca"] = ghi
        if nap_sua_that:
            g["CA"][ca].__globals__["nap_sua"] = nap_sua_ghi
        try:
            rc, dong = that(ca)
        finally:
            g["CA"][ca].__globals__["chay_ca"] = that
            if nap_sua_that:
                g["CA"][ca].__globals__["nap_sua"] = nap_sua_that
        print(f"## {tep} :: {ca} -> rc={rc} {dong[:200]}")
        for i, (ten, r, d) in enumerate(so):
            print(f"{i:02d} | {ten} | rc={r} | {d[:260] if d else '(xanh, khong in gi)'}")
        print(f"   tong: {len(so)} loi goi ben trong; rc=3: {sum(r == 3 for _, r, _ in so)}; rc=0: {sum(r == 0 for _, r, _ in so)}; rc=4: {sum(r == 4 for _, r, _ in so)}")
