# Bo chay dot bien cho nguyen mau r2: neo dung 1 lan, so luot dau voi ky vong, rc != 0 khi lech
import io, contextlib, sys
src = open(sys.argv[1], encoding="utf-8").read()
DB = [  # (id, neo, thay, luot dich ky vong)
 ("db_nt_bo_nul", '    if "\\x00" in p: return ("nul",)\n', "", "p11"),
 ("db_nt_bo_trang", '    if p.strip() == "": return ("trang",)\n', "", "p12"),
 ("db_nt_bo_win32", '    if re.match(r"[\\\\/]{2}\\?[\\\\/]", p): return ("thiet_bi_win32",)\n', "", "p13"),
 ("db_nt_bo_dos", '    if re.match(r"[\\\\/]{2}\\.[\\\\/]", p): return ("thiet_bi_dos",)\n', "", "p16"),
 ("db_nt_bo_nt", '    if re.match(r"[\\\\/]\\?\\?[\\\\/]", p): return ("nt_doi_tuong",)\n', "", "p18"),
 ("db_nt_o_tran", '        if r == "": return ("o_tran",)\n', '        if r == "": r = "\\\\"\n', "p19"),
 ("db_nt_o_tuong_doi", '        if r[0] not in _SEP: return ("o_tuong_doi",)\n', "", "p20"),
 ("db_nt_o_chi_hoa", 're.fullmatch(r"[A-Za-z]:", d)', 're.fullmatch(r"[A-Z]:", d)', "p03"),
 ("db_nt_khong_hoa_o", "d.upper() + B", "d + B", "p03"),
 ("db_nt_goc_o_tuyet_doi", '        if p[0] in _SEP: return ("goc_o",)\n', "", "p21"),
 ("db_nt_unc_share_rong", 'r"[\\\\/]{2}([^\\\\/]+)[\\\\/]([^\\\\/]+)"', 'r"[\\\\/]{2}([^\\\\/]+)[\\\\/]?([^\\\\/]*)"', "p23"),
 ("db_nt_chi_gach_nguoc", 're.split(r"[\\\\/]", r)', 're.split(r"[\\\\]", r)', "p02"),
 ("db_nt_bo_hai_cham", '    if ".." in tp: return ("hai_cham",)\n', "", "p28"),
 ("db_nt_bo_ky_tu_cam", """    if re.search(r'[<>:"|?*\\x01-\\x1f]', t): return "ky_tu_cam"\n""", "", "p31"),
 ("db_nt_bo_cuoi_cham", '    if t.endswith((".", " ")): return "cuoi_cham_cach"\n', "", "p33"),
 ("db_nt_bo_ten_tb", '    if _TEN_TB.fullmatch(t): return "ten_thiet_bi"\n', "", "p35"),
 ("db_nt_ten_tb_khong_cach", r"\$) *(\..*)?", r"\$)(\..*)?", "p38"),
 ("db_nt_bo_conin", r"|CONIN\$|CONOUT\$", "", "p39"),
 ("db_nt_bo_surrogate", "    if re.search(r'[\\ud800-\\udfff]', t): return \"ky_tu_cam\"\n", "", "p44"),
 ("db_nt_unc_bo_kiem_ten", "        for t in m.groups():\n            if (ly := _tp_sai(t)): return (ly,)\n", "", "p40"),
 ("db_nt_bo_ipc", '        if m[2].upper() == "IPC$": return ("unc_ipc",)\n', "", "p42"),
 ("db_nt_o_khac_nhan", '    else:\n        return ("o_khac",)\n', '    else:\n        loai, goc = "o_tuyet_doi", d + B\n', "p27"),
 ("db_nt_cwd_khong_kiem", '        if c[0] not in ("o_tuyet_doi", "unc"): return "ly_do:cwd"\n', '        if c[0] not in ("o_tuyet_doi", "unc"): return chuan(ntpath.join(cwd, p), cwd, unc)\n', "q04"),
 ("db_nt_goc_rong", '    if not a[2]: return "ly_do:goc_rong"\n', "", "q06"),
 ("db_nt_bo_kiem_unc", '    if a[0] == "unc" and not unc: return "ly_do:unc_dong"\n', "", "q10"),
 ("db_nt_unc_mo_som", "def chuan(p, cwd, unc=False):", "def chuan(p, cwd, unc=True):", "q11"),
 ("db_nt_bo_dieu_khien", "\\x01-\\x1f]', t)", "]', t)", "p48"),
 ("db_nt_dao_thu_tu_unc", "        for t in m.groups():\n            if (ly := _tp_sai(t)): return (ly,)\n        if m[2].upper() == \"IPC$\": return (\"unc_ipc\",)\n        loai, goc = \"unc\", B * 2 + m[1] + B + m[2] + B\n",
  "        loai, goc = \"unc\", B * 2 + m[1] + B + m[2] + B\n        if \"..\" in re.split(r\"[\\\\/]\", r): return (\"hai_cham\",)\n        for t in m.groups():\n            if (ly := _tp_sai(t)): return (ly,)\n        if m[2].upper() == \"IPC$\": return (\"unc_ipc\",)\n", "p47"),
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
