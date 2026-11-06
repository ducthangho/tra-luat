"""Kiểm bảng disposition đột biến của K7-S (ops/specs/wp1236-r8.md, mục A14-S) trên cài đặt THAM CHIẾU gram.py: mỗi đột biến
phải làm ca đích (một khoá của AM trong probes_r8.py) chuyển từ bị-từ-chối sang được-nhận, và không làm ca dương nào hỏng.
Đây là phép đo của phiên soạn trên cài đặt tham chiếu, KHÔNG thay bảng đột biến của executor trên module thật."""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gram
from probes_r8 import AM, DUONG   # noqa: E402  (probes_r8 chạy Bash khi import — tách phần dữ liệu)


def dung(P=gram.P, W=gram.W, DANG=None, sep=" ", flags=re.ASCII, khop="fullmatch", bo_lf="mot", nhieu_dong=False,
         ong_shell=("bash",), shell_ok=(None, "bash", "sh"), phai_ong=None, dao_thu_tu=False):
    DANG = DANG or rf"(?:python {P}\.py|bash {P}\.sh|pwsh -NoProfile -File {P}\.ps1)"
    LENH = rf"{DANG}(?:{sep}{W})*"
    phai = phai_ong or LENH
    don, ong = re.compile(LENH, flags), re.compile(rf"{LENH}(?: \| {phai})+", flags)

    def f(run, shell):
        if dao_thu_tu and shell not in shell_ok:
            return "shell_ngoai_cu_phap"
        if type(run) is not str:
            return "lenh_ngoai_cu_phap"
        if shell not in shell_ok:
            return "shell_ngoai_cu_phap"
        b = {"mot": run[:-1] if run.endswith("\n") else run, "rstrip": run.rstrip("\n"), "strip": run.strip()}[bo_lf]
        dong = b.split("\n") if nhieu_dong else [b]
        k = lambda r, x: getattr(r, khop)(x)
        if all(k(don, x) for x in dong):
            return None
        if k(ong, b):
            return None if shell in ong_shell else "ong_khong_bash_tuong_minh"
        return "lenh_ngoai_cu_phap"
    return f


DB = {   # tên: (hàm đột biến, ca đích)
    "m-S1_nhieu_dong": (dung(nhieu_dong=True), "g_hai_lenh_hop_le"),
    "m-S2_rstrip_lf": (dung(bo_lf="rstrip"), "g_hai_lf_cuoi"),
    "m-S3_strip": (dung(bo_lf="strip"), "g_dau_cach_cuoi"),
    "m-S4_match": (dung(khop="match"), "g_cham_phay"),
    "m-S5_search": (dung(khop="search"), "g_gan_bien_dau"),
    "m-S6_unicode_w": (dung(P=r"[\w.][\w./-]*", W=r"[\w./=:-]+", flags=0), "g_chu_so_unicode"),
    "m-S7_khoang_trang": (dung(sep=r"\s+"), "g_tab_doi_so"),
    "m-S7b_nhieu_dau_cach": (dung(sep=" +"), "g_hai_dau_cach_doi_so"),
    "m-S8_ten_lenh_mo": (dung(DANG=rf"[A-Za-z0-9_./-]+"), "g_lenh_ngoai_ds"),
    "m-S9_doi_so_dau_mo": (dung(DANG=r"(?:python|bash|pwsh)"), "g_python_c_tran"),
    "m-S9b_bash_doi_so_dau_mo": (dung(DANG=rf"(?:python {gram.P}\.py|bash|pwsh -NoProfile -File {gram.P}\.ps1)"), "g_bash_c_tran"),
    "m-S9c_P_tuyet_doi": (dung(P=r"[A-Za-z0-9_./][A-Za-z0-9_./-]*"), "g_tuyet_doi"),
    "m-S10_ong_shell_vang": (dung(ong_shell=("bash", None)), "g_ong_khong_bash"),
    "m-S11_ong_sh": (dung(ong_shell=("bash", "sh")), "g_ong_sh"),
    "m-S12_ve_phai_mo": (dung(phai_ong=rf"{gram.W}(?: {gram.W})*"), "g_ong_toi_cat"),
    "m-S13_nhan_pwsh": (dung(shell_ok=(None, "bash", "sh", "pwsh")), "g_pwsh_shell"),
    "m-S19_dao_thu_tu_1_2": (dung(dao_thu_tu=True), "g_run_khong_phai_chuoi_pwsh"),
}
for c in ";&|!(){}$`'\"\\<>#*?[]~\t\n\r":
    DB[f"m-S14[{ord(c):02x}]"] = (dung(W=r"[A-Za-z0-9_./=:" + re.escape(c) + "-]+"), f"kt_{ord(c):02x}")


def main():
    hong, bang = 0, []
    for ten, (f, dich) in DB.items():
        r, s = AM[dich]
        giet = gram.cu_phap_run(r, s) is not None and f(r, s) != gram.cu_phap_run(r, s)   # đổi lý do (kể cả thành None) = ca đích đỏ
        duong_hong = [k for k, (r2, s2) in DUONG.items() if f(r2, s2) is not None]
        bang.append({"dot_bien": ten, "ca_dich": dich, "giet_ca_dich": giet, "lam_hong_ca_duong": duong_hong})
        hong += (not giet) or bool(duong_hong)
        print(f"{ten:28} {dich:22} {'GIET' if giet else 'SONG'} {duong_hong or ''}")
    print(json.dumps({"dot_bien": len(DB), "giet_dung_ca_dich": sum(b["giet_ca_dich"] for b in bang), "hong": hong}))
    json.dump(bang, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dot_bien_r8.json"), "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if hong else 0)


if __name__ == "__main__":
    main()
