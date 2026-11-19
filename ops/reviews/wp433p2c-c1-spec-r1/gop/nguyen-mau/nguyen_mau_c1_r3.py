# Nguyen mau r2 bo phan loai duong Windows (KHONG phai ma thi cong)
import ntpath, re
B = chr(92)
_SEP = "\\/"
_TEN_TB = re.compile(r"(CON|PRN|AUX|NUL|COM[0-9¹²³]|LPT[0-9¹²³]|CONIN\$|CONOUT\$) *(\..*)?", re.I)
def _tp_sai(t):
    if re.search(r'[<>:"|?*\x01-\x1f]', t): return "ky_tu_cam"
    if re.search(r'[\ud800-\udfff]', t): return "ky_tu_cam"
    if t.endswith((".", " ")): return "cuoi_cham_cach"
    if _TEN_TB.fullmatch(t): return "ten_thiet_bi"
    return None
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
        for t in m.groups():
            if (ly := _tp_sai(t)): return (ly,)
        if m[2].upper() == "IPC$": return ("unc_ipc",)
        loai, goc = "unc", B * 2 + m[1] + B + m[2] + B
    elif d == "":
        if p[0] in _SEP: return ("goc_o",)
        loai, goc = "tuong_doi", None
    else:
        return ("o_khac",)
    tp = tuple(t for t in re.split(r"[\\/]", r) if t not in ("", "."))
    if ".." in tp: return ("hai_cham",)
    for t in tp:
        if (ly := _tp_sai(t)): return (ly,)
    return (loai, goc, tp)
def chuan(p, cwd, unc=False):
    a = phan_loai(p)
    if a[0] == "tuong_doi":
        c = phan_loai(cwd)
        if c[0] not in ("o_tuyet_doi", "unc"): return "ly_do:cwd"
        a = (c[0], c[1], c[2] + a[2])
    if a[0] not in ("o_tuyet_doi", "unc"): return "ly_do:" + a[0]
    if a[0] == "unc" and not unc: return "ly_do:unc_dong"
    if not a[2]: return "ly_do:goc_rong"
    return (a[1], a[2])
N1 = ["C:"+B+"x","C:/x","c:"+B+"x","C:"+B+"a/b"+B+"c",B*2+"server"+B+"share"+B+"x","//server/share/x","/"+B+"server"+B+"share"+B+"x","fake","C:"+B+"x"+B+"."+B+"y"+B*2,"D:"+B+"Quốc hội"+B+"tra-luat",
"a\x00b","   ",B*2+"?"+B+"C:"+B+"x","//?/C:/x",B*2+"?"+B+"UNC"+B+"s"+B+"sh",B*2+"."+B+"pipe"+B+"x","//./C:/x",B+"??"+B+"C:"+B+"x","C:","D:fake",B+"fake","/fake",B*2+"server",B*2+"server"+B,B*3+"server"+B+"share",B*2+"server"+B*2+"share","1:"+B+"x",
"C:"+B+"a"+B+".."+B+"b","a/../b","..","C:"+B+"x:ads","C:"+B+"a|b","C:"+B+"a."+B+"b","C:"+B+"a ","C:"+B+"CON","C:"+B+"nul.txt","C:"+B+"com1"+B+"x",
"C:"+B+"NUL .txt","C:"+B+"CONIN$",B*2+"server."+B+"share"+B+"x",B*2+"server"+B+"sh:a"+B+"x",B*2+"server"+B+"IPC$"+B+"x",B*2+"server"+B+"share"+B*2+"x","C:"+B+"a\ud800b","C:"+B+" a","C:"+B+"COM0",B*2+"server."+B+"share"+B+".."]
CW = B*2+"s"+B+"sh"+B+"d"
N2 = [("fake","C:"+B+"cwd",False),("a"+B+"b","c:/cwd",False),("fake",CW,True),("fake","D:rel",False),("fake",B*2+"?"+B+"C:"+B+"cwd",False),("C:"+B,"C:"+B+"cwd",False),
(B*2+"server"+B+"share","C:"+B+"cwd",True),("x\n"+B+"..","C:"+B+"cwd",False),("x","C:"+B,False),("fake",CW,False),(B*2+"server"+B+"share"+B+"x","C:"+B+"cwd",None),
(".","C:"+B+"cwd",False),(".","C:"+B,False)]
if __name__ == "__main__":
    for i, p in enumerate(N1, 1): print("p%02d" % i, repr(p), "->", phan_loai(p))
    for i, (p, c, u) in enumerate(N2, 1): print("q%02d" % i, repr(p), repr(c), u, "->", repr(chuan(p, c) if u is None else chuan(p, c, u)))
