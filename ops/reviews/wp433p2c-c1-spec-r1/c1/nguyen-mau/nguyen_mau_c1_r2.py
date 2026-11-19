# Nguyen mau C1 (KHONG phai ma thi cong): phan loai duong Windows thuan ntpath, UNC/o mang luon tu choi
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
    if p[:1] in tuple(_SEP) and p[1:2] in tuple(_SEP): return ("unc",)
    d, r = ntpath.splitdrive(p)
    if re.fullmatch(r"[A-Za-z]:", d):
        if r == "": return ("o_tran",)
        if r[0] not in _SEP: return ("o_tuong_doi",)
        loai, goc = "o_tuyet_doi", d.upper() + B
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
def chuan(p, cwd, loai_o=lambda g: 3):
    a, x = phan_loai(p), p
    if a[0] == "tuong_doi":
        c = phan_loai(cwd)
        if c[0] != "o_tuyet_doi": return "ly_do:" + repr(cwd)
        a, x = (c[0], c[1], c[2] + a[2]), cwd
    if a[0] != "o_tuyet_doi": return "ly_do:" + repr(p)
    if not a[2]: return "ly_do:" + repr(x)
    if loai_o(a[1]) not in (2, 3): return "ly_do:" + repr(x)
    return (a[1], a[2])
N1 = ["C:"+B+"x","C:/x","c:"+B+"x","C:"+B+"a/b"+B+"c","fake","C:"+B+"x"+B+"."+B+"y"+B*2,"D:"+B+"Quốc hội"+B+"tra-luat","C:"+B+" a",
"a\x00b","   ",B*2+"?"+B+"C:"+B+"x","//?/C:/x",B*2+"?"+B+"UNC"+B+"s"+B+"sh",B*2+"."+B+"pipe"+B+"x","//./C:/x",B+"??"+B+"C:"+B+"x","C:","D:fake",B+"fake","/fake",
B*2+"server"+B+"share"+B+"x","//server/share/x","/"+B+"server"+B+"share"+B+"x",B*2+"server",B*3+"server"+B+"share",B*2+"server"+B*2+"share","1:"+B+"x",
"C:"+B+"a"+B+".."+B+"b","a/../b","..","C:"+B+"x:ads","C:"+B+"a|b","C:"+B+"a\ud800b","C:"+B+"a\x01b","C:"+B+"a."+B+"b","C:"+B+"a ",
"C:"+B+"CON","C:"+B+"nul.txt","C:"+B+"com1"+B+"x","C:"+B+"NUL .txt","C:"+B+"CONIN$","C:"+B+"COM0","C:"+B+"a<.","C:"+B+"CON.x ","C:"+B+"a\x7fb\u00a0"]
N2 = [("fake","C:"+B+"cwd",3),("a"+B+"b","c:/cwd",3),("fake",B*2+"s"+B+"sh"+B+"d",3),("fake","D:rel",3),("fake",B*2+"?"+B+"C:"+B+"cwd",3),("C:"+B,"C:"+B+"cwd",3),
("x\n"+B+"..","C:"+B+"cwd",3),("x","C:"+B,3),(".","C:"+B+"cwd",3),(".","C:"+B,3),("Z:"+B+"x","C:"+B+"cwd",4),("E:"+B+"x","C:"+B+"cwd",5),("F:"+B+"x","C:"+B+"cwd",2),("fake","Z:"+B+"cwd",4),("G:"+B+"x","C:"+B+"cwd",0),("H:"+B+"x","C:"+B+"cwd",1),("R:"+B+"x","C:"+B+"cwd",6)]
if __name__ == "__main__":
    for i, p in enumerate(N1, 1): print("p%02d" % i, repr(p), "->", phan_loai(p))
    for i, (p, c, t) in enumerate(N2, 1): print("q%02d" % i, repr(p), repr(c), t, "->", repr(chuan(p, c, lambda g, t=t: t)))
