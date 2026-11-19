# Bo chay dot bien nguyen mau C1: neo dung 1 lan, so luot dau doi mau voi dich khai, rc != 0 khi lech
import io, contextlib, sys
src = open(sys.argv[1], encoding="utf-8").read()
DB = [
 ("db_nt_bo_nul", '    if "\\x00" in p: return ("nul",)\n', "", "p09"),
 ("db_nt_bo_trang", '    if p.strip() == "": return ("trang",)\n', "", "p10"),
 ("db_nt_bo_win32", '    if re.match(r"[\\\\/]{2}\\?[\\\\/]", p): return ("thiet_bi_win32",)\n', "", "p11"),
 ("db_nt_bo_dos", '    if re.match(r"[\\\\/]{2}\\.[\\\\/]", p): return ("thiet_bi_dos",)\n', "", "p14"),
 ("db_nt_bo_nt", '    if re.match(r"[\\\\/]\\?\\?[\\\\/]", p): return ("nt_doi_tuong",)\n', "", "p16"),
 ("db_nt_bo_unc", '    if p[:1] in tuple(_SEP) and p[1:2] in tuple(_SEP): return ("unc",)\n', "", "p21"),
 ("db_nt_unc_chi_gach_nguoc", 'if p[:1] in tuple(_SEP) and p[1:2] in tuple(_SEP): return ("unc",)', 'if p[:2] == B * 2: return ("unc",)', "p22"),
 ("db_nt_o_tran", '        if r == "": return ("o_tran",)\n', '        if r == "": r = "\\\\"\n', "p17"),
 ("db_nt_o_tuong_doi", '        if r[0] not in _SEP: return ("o_tuong_doi",)\n', "", "p18"),
 ("db_nt_o_chi_hoa", 're.fullmatch(r"[A-Za-z]:", d)', 're.fullmatch(r"[A-Z]:", d)', "p03"),
 ("db_nt_khong_hoa_o", "d.upper() + B", "d + B", "p03"),
 ("db_nt_goc_o_tuyet_doi", '        if p[0] in _SEP: return ("goc_o",)\n', "", "p19"),
 ("db_nt_chi_gach_nguoc", 're.split(r"[\\\\/]", r)', 're.split(r"[\\\\]", r)', "p02"),
 ("db_nt_bo_hai_cham", '    if ".." in tp: return ("hai_cham",)\n', "", "p28"),
 ("db_nt_bo_ky_tu_cam", """    if re.search(r'[<>:"|?*\\x01-\\x1f]', t): return "ky_tu_cam"\n""", "", "p31"),
 ("db_nt_bo_surrogate", "    if re.search(r'[\\ud800-\\udfff]', t): return \"ky_tu_cam\"\n", "", "p33"),
 ("db_nt_bo_dieu_khien", "\\x01-\\x1f]', t)", "]', t)", "p34"),
 ("db_nt_bo_cuoi_cham", '    if t.endswith((".", " ")): return "cuoi_cham_cach"\n', "", "p35"),
 ("db_nt_bo_ten_tb", '    if _TEN_TB.fullmatch(t): return "ten_thiet_bi"\n', "", "p37"),
 ("db_nt_ten_tb_khong_cach", r"\$) *(\..*)?", r"\$)(\..*)?", "p40"),
 ("db_nt_bo_conin", r"|CONIN\$|CONOUT\$", "", "p41"),
 ("db_nt_o_khac_nhan", '    else:\n        return ("o_khac",)\n', '    else:\n        loai, goc = "o_tuyet_doi", d + B\n', "p27"),
 ("db_nt_cwd_khong_kiem", '        if c[0] != "o_tuyet_doi": return "ly_do:" + repr(cwd)[:200]\n', '        if c[0] != "o_tuyet_doi": return chuan(ntpath.join(cwd, p), cwd, loai_o)\n', "q03"),
 ("db_nt_goc_rong", '    if not a[2]: return "ly_do:" + repr(x)[:200]\n', "", "q06"),
 ("db_nt_bo_loai_o", '    if loai_o(a[1]) not in (2, 3): return "ly_do:" + repr(x)[:200]\n', "", "q11"),
 ("db_nt_loai_o_moi_loai", "if loai_o(a[1]) not in (2, 3):", "if loai_o(a[1]) == 4:", "q12"),
 ("db_nt_bo_removable", "if loai_o(a[1]) not in (2, 3):", "if loai_o(a[1]) != 3:", "q13"),
 ("db_nt_loai_o_chi_tuyet_doi", "if loai_o(a[1]) not in (2, 3):", "if x is p and loai_o(a[1]) not in (2, 3):", "q14"),
 ("db_nt_dao_ky_tu_cuoi", """    if re.search(r'[<>:"|?*\\x01-\\x1f]', t): return "ky_tu_cam"\n    if re.search(r'[\\ud800-\\udfff]', t): return "ky_tu_cam"\n    if t.endswith((".", " ")): return "cuoi_cham_cach"\n""", """    if t.endswith((".", " ")): return "cuoi_cham_cach"\n    if re.search(r'[<>:"|?*\\x01-\\x1f]', t): return "ky_tu_cam"\n    if re.search(r'[\\ud800-\\udfff]', t): return "ky_tu_cam"\n""", "p43"),
 ("db_nt_dao_cuoi_ten_tb", '    if t.endswith((".", " ")): return "cuoi_cham_cach"\n    if _TEN_TB.fullmatch(t): return "ten_thiet_bi"\n', '    if _TEN_TB.fullmatch(t): return "ten_thiet_bi"\n    if t.endswith((".", " ")): return "cuoi_cham_cach"\n', "p44"),
 ("db_nt_cam_nbsp_del", "\\x01-\\x1f]', t)", "\\x01-\\x1f\\x7f\\u00a0]', t)", "p45"),
 ("db_nt_loai_o_nhan_0", "if loai_o(a[1]) not in (2, 3):", "if loai_o(a[1]) not in (0, 2, 3):", "q15"),
 ("db_nt_loai_o_nhan_1", "if loai_o(a[1]) not in (2, 3):", "if loai_o(a[1]) not in (1, 2, 3):", "q16"),
 ("db_nt_loai_o_nhan_6", "if loai_o(a[1]) not in (2, 3):", "if loai_o(a[1]) not in (2, 3, 6):", "q17"),
 ("db_nt_thanh_phan_truoc_namespace", '    if "\\x00" in p: return ("nul",)\n', '    if "\\x00" in p: return ("nul",)\n    for t in re.split(r"[\\\\/]", p)[1:]:\n        if t not in ("", ".", "..") and (ly := _tp_sai(t)): return (ly,)\n', "p11"),
 ("db_nt_bo_cat_200", '    if a[0] != "o_tuyet_doi": return "ly_do:" + repr(p)[:200]\n', '    if a[0] != "o_tuyet_doi": return "ly_do:" + repr(p)\n', "q18"),
]
def chay(s):
    b = io.StringIO()
    with contextlib.redirect_stdout(b): exec(compile(s, "nm", "exec"), {"__name__": "__main__"})
    return b.getvalue().splitlines()
base, loi = chay(src), 0
for k, a, b, dich in DB:
    n = src.count(a)
    if n != 1:
        print(k, "NEO", n); loi += 1; continue
    try:
        out = chay(src.replace(a, b))
    except Exception as e:
        print(k, "NEM", type(e).__name__, e); loi += 1; continue
    d = [x.split()[0] for x, y in zip(base, out) if x != y]
    ok = bool(d) and d[0] == dich
    loi += not ok
    print(k, "dich", dich, "luot_do", d, "OK" if ok else "LECH")
print("TONG", len(DB), "LECH", loi)
sys.exit(1 if loi else 0)
