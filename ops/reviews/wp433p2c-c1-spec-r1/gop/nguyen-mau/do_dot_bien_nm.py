import sys, io, contextlib
src = open(sys.argv[1], encoding="utf-8").read()
base_out = None
DB = {
 "db_nt_bo_win32": ('    if re.match(r"[\\\\/]{2}\\?[\\\\/]", p): return ("thiet_bi_win32",)\n', ""),
 "db_nt_bo_dos": ('    if re.match(r"[\\\\/]{2}\\.[\\\\/]", p): return ("thiet_bi_dos",)\n', ""),
 "db_nt_bo_nt": ('    if re.match(r"[\\\\/]\\?\\?[\\\\/]", p): return ("nt_doi_tuong",)\n', ""),
 "db_nt_o_tran": ('        if r == "": return ("o_tran",)\n', ""),
 "db_nt_o_tuong_doi": ('        if r[0] not in _SEP: return ("o_tuong_doi",)\n', ""),
 "db_nt_o_chi_hoa": ('re.fullmatch(r"[A-Za-z]:", d)', 're.fullmatch(r"[A-Z]:", d)'),
 "db_nt_khong_hoa_o": ('d.upper() + B', 'd + B'),
 "db_nt_goc_o_tuyet_doi": ('        if p[0] in _SEP: return ("goc_o",)\n', ""),
 "db_nt_unc_share_rong": ('r"[\\\\/]{2}([^\\\\/]+)[\\\\/]([^\\\\/]+)"', 'r"[\\\\/]{2}([^\\\\/]+)[\\\\/]?([^\\\\/]*)"'),
 "db_nt_chi_gach_nguoc": ('re.split(r"[\\\\/]", r)', 're.split(r"[\\\\]", r)'),
 "db_nt_bo_hai_cham": ('        if t == "..": return ("hai_cham",)\n', "        pass\n"),
 "db_nt_bo_ky_tu_cam": ("""        if re.search(r'[<>:"|?*\\x01-\\x1f]', t): return ("ky_tu_cam",)\n""", ""),
 "db_nt_bo_cuoi_cham": ('        if t[-1] in ". ": return ("cuoi_cham_cach",)\n', ""),
 "db_nt_bo_ten_tb": ('        if _TEN_TB.fullmatch(t.split(".")[0] if False else t): return ("ten_thiet_bi",)\n', ""),
 "db_nt_o_khac_nhan": ('    else:\n        return ("o_khac",)\n', '    else:\n        loai, goc = "o_tuyet_doi", d + B\n'),
 "db_nt_goc_rong": ('    if not a[2]: return "goc_rong"\n', ""),
}
def chay(s):
    b = io.StringIO()
    with contextlib.redirect_stdout(b): exec(compile(s, "nm", "exec"), {"__name__": "nm"})
    return b.getvalue().splitlines()
base = chay(src)
for k, (a, b) in DB.items():
    n = src.count(a)
    if n != 1: print(k, "NEO", n); continue
    try:
        out = chay(src.replace(a, b))
        print(k, "doi:", [y for x, y in zip(base, out) if x != y][:3])
    except Exception as e:
        print(k, "NEM:", type(e).__name__, e)
