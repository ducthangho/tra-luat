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
CA = ["C:"+B+"x", "c:/x", "C:", "D:fake", B+"fake", B*2+"server"+B+"share"+B+"x", B*2+"server"+B+"share", B*2+"server", B*2+"server"+B,
      B*2+"?"+B+"C:"+B+"x", "//?/C:/x", B*2+"."+B+"pipe"+B+"x", B+"??"+B+"C:"+B+"x", B*2+"?"+B+"UNC"+B+"s"+B+"sh", "//server/share/x", "/"+B+"server"+B+"share"+B+"x",
      "C:"+B+"a"+B+".."+B+"b", "a/../b", "..", "C:"+B+"a/b"+B+"c", "C:"+B+"x:ads", B*3+"server"+B+"share", B*2+"server"+B*2+"share", "C:"+B+"CON", "C:"+B+"nul.txt", "C:"+B+"a."+B+"b", "C:"+B+"a ", "1:"+B+"x", "fake", "C:"+B, "a\x00b", "   ", "C:"+B+"x"+B+"."+B+"y"+B*2]
for p in CA:
    print(repr(p), "->", chuan(p, "C:"+B+"cwd"))
