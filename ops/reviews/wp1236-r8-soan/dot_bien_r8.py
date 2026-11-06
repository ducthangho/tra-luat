"""Kiểm bảng disposition đột biến của K7-S (ops/specs/wp1236-r8.md, mục A14-S) trên cài đặt THAM CHIẾU gram.py: mỗi đột biến
phải làm ca đích (một khoá của AM trong probes_r8.py) chuyển từ bị-từ-chối sang được-nhận, và không làm ca dương nào hỏng.
Đây là phép đo của phiên soạn trên cài đặt tham chiếu, KHÔNG thay bảng đột biến của executor trên module thật."""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gram
from probes_r8 import AM, DUONG   # noqa: E402  (probes_r8 chạy Bash khi import — tách phần dữ liệu)


def dung(P=gram.P, W=gram.W, DANG=None, sep=" ", flags=re.ASCII, khop="fullmatch", bo_lf="mot", nhieu_dong=False,
         ong_shell=("bash",), shell_ok=(None, "bash", "sh"), phai_ong=None, dao_thu_tu=False, ong_sep=r" \| "):
    DANG = DANG or rf"(?:python {P}\.py|bash {P}\.sh|pwsh -NoProfile -File {P}\.ps1)"
    LENH = rf"{DANG}(?:{sep}{W})*"
    phai = phai_ong or LENH
    don, ong = re.compile(LENH, flags), re.compile(rf"{LENH}(?:{ong_sep}{phai})+", flags)

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
    "m-S9p_pwsh_mo": (dung(DANG=rf"(?:python {gram.P}\.py|bash {gram.P}\.sh|pwsh(?: {gram.W})+)"), "g_pwsh_command"),
    "m-S9q_noprofile_tuy_chon": (dung(DANG=rf"(?:python {gram.P}\.py|bash {gram.P}\.sh|pwsh(?: -NoProfile)? -File {gram.P}\.ps1)"), "g_pwsh_thieu_noprofile"),
    "m-S9d_P_gach_dau": (dung(P=r"[A-Za-z0-9_.-][A-Za-z0-9_./-]*"), "g_P_gach_dau"),
    "m-S9e_duoi_bat_ky": (dung(DANG=rf"(?:python|bash|pwsh -NoProfile -File) {gram.P}\.(?:py|sh|ps1)"), "g_bash_duoi_py"),
    "m-S9f_python_bo_duoi": (dung(DANG=rf"(?:python {gram.P}|bash {gram.P}\.sh|pwsh -NoProfile -File {gram.P}\.ps1)"), "g_python_khong_duoi"),
    "m-S9g_pwsh_duoi_bat_ky": (dung(DANG=rf"(?:python {gram.P}\.py|bash {gram.P}\.sh|pwsh -NoProfile -File {gram.P}\.(?:ps1|py))"), "g_pwsh_duoi_py"),
    "m-S7c_ong_khong_cach": (None, "g_ong_khong_cach"),
}
DB["m-S7c_ong_khong_cach"] = (dung(ong_sep=r" ?\| ?"), "g_ong_khong_cach")
for c in ";&|!(){}$`'\"\\<>#*?[]~\t\n\r+,@%^":
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




# --- Đột biến lớp I01 (reviewer Claude vòng 2 r8): chết ở KHO SINH (A14-S6), không cần một vế viết tay cho từng cái ---
def _don_mo(mau):   # mau(LENH) -> regex DON đột biến
    def f(run, shell):
        if type(run) is not str:
            return "lenh_ngoai_cu_phap"
        if shell not in (None, "bash", "sh"):
            return "shell_ngoai_cu_phap"
        b = run[:-1] if run.endswith("\n") else run
        if re.fullmatch(mau(gram.LENH), b, re.ASCII):
            return None
        if gram.RE_ONG.fullmatch(b):
            return None if shell == "bash" else "ong_khong_bash_tuong_minh"
        return "lenh_ngoai_cu_phap"
    return f


DB_SINH = {
    "m-S7d_tach_ong_hai_gach": dung(ong_sep=r" \|\|? "),
    "m-S7e_tach_ong_nhieu_gach": dung(ong_sep=r" \|+ "),
    "m-S7f_tach_ong_va": dung(ong_sep=r" [|&] "),
    "m-S7g_don_va_cuoi": _don_mo(lambda L: rf"{L}(?: &)?"),
    "m-S7h_don_cham_than_dau": _don_mo(lambda L: rf"(?:! )?{L}"),
    "m-S7i_don_hoac_lenh": _don_mo(lambda L: rf"{L}(?: \|\| {L})*"),
}


def _ong_giua_mo(run, shell):   # J01 Codex vòng 3: chỉ kiểm thành phần ĐẦU và CUỐI của ống, thành phần giữa là chuỗi W bất kỳ
    if type(run) is not str:
        return "lenh_ngoai_cu_phap"
    if shell not in (None, "bash", "sh"):
        return "shell_ngoai_cu_phap"
    b = run[:-1] if run.endswith("\n") else run
    if gram.RE_DON.fullmatch(b):
        return None
    if re.fullmatch(rf"{gram.LENH}(?: \| [A-Za-z0-9_./=: -]+)* \| {gram.LENH}", b, re.ASCII):
        return None if shell == "bash" else "ong_khong_bash_tuong_minh"
    return "lenh_ngoai_cu_phap"


DB_SINH["m-S7j_ong_giua_mo"] = _ong_giua_mo
# Claude J01 vòng 3: sáu cài đặt sống qua bản kho trước
DB_SINH["v3a_bash_P_bat_ky"] = dung(DANG=rf"(?:python {gram.P}\.py|bash \S+\.sh|pwsh -NoProfile -File {gram.P}\.ps1)")
DB_SINH["v3b_pwsh_P_bat_ky"] = dung(DANG=rf"(?:python {gram.P}\.py|bash {gram.P}\.sh|pwsh -NoProfile -File \S+\.ps1)")
DB_SINH["v3c_bash_tuy_chon"] = dung(DANG=rf"(?:python {gram.P}\.py|bash(?: -[a-z]+)* {gram.P}\.sh|pwsh -NoProfile -File {gram.P}\.ps1)")
DB_SINH["v3d_python_tuy_chon"] = dung(DANG=rf"(?:python(?: -[A-Za-z]+)* {gram.P}\.py|bash {gram.P}\.sh|pwsh -NoProfile -File {gram.P}\.ps1)")


def _ong_duoi(mau):
    def f(run, shell):
        if type(run) is not str:
            return "lenh_ngoai_cu_phap"
        if shell not in (None, "bash", "sh"):
            return "shell_ngoai_cu_phap"
        b = run[:-1] if run.endswith("\n") else run
        if gram.RE_DON.fullmatch(b):
            return None
        if re.fullmatch(mau, b, re.ASCII):
            return None if shell == "bash" else "ong_khong_bash_tuong_minh"
        return "lenh_ngoai_cu_phap"
    return f


DB_SINH["v3f_ong_hoac_cuoi"] = _ong_duoi(rf"{gram.LENH}(?: \| {gram.LENH})+(?: \|\| {gram.LENH})?")
DB_SINH["v3h_ong_cham_than"] = _ong_duoi(rf"{gram.LENH}(?: \| (?:! )?{gram.LENH})+")
for c in ";&|!(){}$`'\"\\<>#*?[]~+,@%^":
    lop = r"[A-Za-z0-9_./" + re.escape(c) + "-]*"
    Pc = r"[A-Za-z0-9_.]" + lop
    DB_SINH[f"m-S15[{ord(c):02x}]_P_moi_nhanh"] = dung(P=Pc)
    DB_SINH[f"m-S15b[{ord(c):02x}]_P_nhanh_bash"] = dung(DANG=rf"(?:python {gram.P}\.py|bash {Pc}\.sh|pwsh -NoProfile -File {gram.P}\.ps1)")
    DB_SINH[f"m-S15p[{ord(c):02x}]_P_nhanh_pwsh"] = dung(DANG=rf"(?:python {gram.P}\.py|bash {gram.P}\.sh|pwsh -NoProfile -File {Pc}\.ps1)")


def main_sinh():
    import sinh_r8
    hong, bang = 0, []
    for ten, f in DB_SINH.items():
        kq, lech, nuot = sinh_r8.main(f)
        giet = kq["lech_tham_chieu"] > 0
        bang.append({"dot_bien": ten, **kq, "giet": giet})
        hong += not giet
    print(json.dumps({"dot_bien_sinh": len(DB_SINH), "giet_o_kho_sinh": sum(b["giet"] for b in bang),
                      "co_than_nhan_ma_nuot_loi": sum(b["nuot_loi"] > 0 for b in bang),
                      "chi_khong_chay": sum(b["nuot_loi"] == 0 and b["khong_chay"] > 0 for b in bang)}))
    json.dump(bang, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dot_bien_sinh_r8.json"), "w"), ensure_ascii=False, indent=1)
    return hong


if __name__ == "__main__":
    if sys.argv[1:] == ["--sinh"]:
        sys.exit(1 if main_sinh() else 0)
    main()
