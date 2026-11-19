# Nguyen mau phan loai duong Windows (KHONG phai ma thi cong) - do de kiem thiet ke dac ta
import ntpath, re, sys
B = chr(92)
_SEP = "\\/"
_TEN_TB = re.compile(r"(CON|PRN|AUX|NUL|COM[0-9¹²³]|LPT[0-9¹²³])(\..*)?", re.I)
def phan_loai(p):
    if "\x00" in p: return ("nul",)
    if p.strip() == "": return ("trang",)
    if re.match(r"[\\/]{2}\?[\\/]", p): return ("thiet_bi_win32",)
    if re.match(r"[\\/]{2}\.[\\/]", p): return ("thiet_bi_dos",)
    if re.match(r"[\\/]\?\?[\\/]", p): return ("nt_doi_tuong",)
    d, r = ntpath.splitdrive(p)
    if re.fullmatch(r"[A-Za-z]:", d):
        if r == "": return ("o_tran",)
        if r[0] not in _SEP: return ("o_tuong_doi",)
        loai, goc = "o_tuyet_doi", d.upper() + B
    elif d[:1] in tuple(_SEP) and d[1:2] in tuple(_SEP):
        m = re.fullmatch(r"[\\/]{2}([^\\/]+)[\\/]([^\\/]+)", d)
        if not m: return ("unc_thieu_share",)
        loai, goc = "unc", B * 2 + m[1] + B + m[2] + B
    elif d == "":
        if p[0] in _SEP: return ("goc_o",)
        loai, goc = "tuong_doi", None
    else:
        return ("o_khac",)
    tp = tuple(t for t in re.split(r"[\\/]", r) if t not in ("", "."))
    for t in tp:
        if t == "..": return ("hai_cham",)
    for t in tp:
        if re.search(r'[<>:"|?*\x01-\x1f]', t): return ("ky_tu_cam",)
        if t[-1] in ". ": return ("cuoi_cham_cach",)
        if _TEN_TB.fullmatch(t.split(".")[0] if False else t): return ("ten_thiet_bi",)
    return (loai, goc, tp)
def chuan(p, cwd):
    a = phan_loai(p)
    if a[0] == "tuong_doi":
        c = phan_loai(cwd)
        if c[0] not in ("o_tuyet_doi", "unc"): return "cwd:" + c[0]
        a = (c[0], c[1], c[2] + a[2])
    if a[0] not in ("o_tuyet_doi", "unc"): return a[0]
    if not a[2]: return "goc_rong"
    return a[1] + B.join(a[2])
N1=[('p01', 'C:\\x'), ('p02', 'c:/x'), ('p03', 'C:\\a/b\\c'), ('p04', '\\\\server\\share\\x'), ('p05', '//server/share/x'), ('p06', '/\\server\\share\\x'), ('p07', 'fake'), ('p08', 'C:\\x\\.\\y\\\\'), ('p09', 'a\x00b'), ('p10', '   '), ('p11', '\\\\?\\C:\\x'), ('p12', '//?/C:/x'), ('p13', '\\\\?\\UNC\\s\\sh'), ('p14', '\\\\.\\pipe\\x'), ('p15', '//./C:/x'), ('p16', '\\??\\C:\\x'), ('p17', 'C:'), ('p18', 'D:fake'), ('p19', '\\fake'), ('p20', '/fake'), ('p21', '\\\\server'), ('p22', '\\\\server\\'), ('p23', '\\\\\\server\\share'), ('p24', '\\\\server\\\\share'), ('p25', '1:\\x'), ('p26', 'C:\\a\\..\\b'), ('p27', 'a/../b'), ('p28', '..'), ('p29', 'C:\\x:ads'), ('p30', 'C:\\a|b'), ('p31', 'C:\\a.\\b'), ('p32', 'C:\\a '), ('p33', 'C:\\CON'), ('p34', 'C:\\nul.txt'), ('p35', 'C:\\com1\\x')]
for i,p in N1: print(i, repr(p), '->', phan_loai(p))
N2=[('q01', 'fake', 'C:\\cwd'), ('q02', 'a\\b', 'c:/cwd'), ('q03', 'fake', '\\\\s\\sh\\d'), ('q04', 'fake', 'D:rel'), ('q05', 'fake', '\\\\?\\C:\\cwd'), ('q06', 'C:\\', 'C:\\cwd'), ('q07', '\\\\server\\share', 'C:\\cwd'), ('q08', 'x\n\\..', 'C:\\cwd'), ('q09', 'x', 'C:\\')]
for i,p,c in N2: print(i, repr(p), repr(c), '->', repr(chuan(p,c)))
