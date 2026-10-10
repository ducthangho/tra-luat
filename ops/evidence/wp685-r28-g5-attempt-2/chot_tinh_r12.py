# chot_tinh_r12.py - CHOT TINH cua dac ta wp685 r12 (§7 B2). MA KIEM THUAN cua dac ta: executor chay NGUYEN VAN
# (trich bang may tu dac ta, doi chieu sha256 cua khoi), KHONG dan xuat lai.
# Dung: python3.11 chot_tinh_r12.py <launcher.py NEN> <launcher.py UNG VIEN> <launcher_test.py UNG VIEN>
# Ma thoat: 0 = DAT (ung vien qua moi luat VA moi doi chung DO dung luat); 1 = ung vien DO; 2 = co doi chung
# khong DO dung luat hay khong dung duoc (chot mat rang); 3 = dau vao hong (doc/parse nen, hinh dang nen la,
# DANG_DOC_QA7 thieu hay ngoai danh sach).
# Luat (ma luat dung dau moi dong loi):
#   H  ba ham canh: CA nut `def` (decorator, chu ky, docstring, than) BANG nen theo AST sau DUNG phep doi cua dang
#      doc da khai, va chi trong than nhanh `if he == "Linux":`. Chu thich `#` khong vao AST nen dat o dau cung duoc.
#   K  (chi dang bytes) bieu thuc dung khoa `linux:` la cho trong: chi ghep `sau[19]` DUNG mot lan bang f-string,
#      `+`, `.decode(...)`, `int()`, `str()`.
#   M  muc module: moi cau lenh ngoai bon ham (`_con_song` va ba ham canh) BANG nen theo AST, tru gia tri chuoi cua
#      `VERSION`; chi duoc THEM cau `def` ten moi (khong trung ten muc module cua nen, khong trung ten dung san).
#   T1..T7 `_con_song` va moi `def` moi: T1 khong global/nonlocal; T2 khong import (nen khong co); T3 ten toan cuc
#      doc duoc thuoc {ten toan cuc cua `_con_song` nen} + TEN_THEM + ten cac `def` moi; T4 khong thuoc tinh dunder;
#      T5 khong gan/xoa thuoc tinh hay chi so; T6 thuoc tinh cua ten toan cuc chi la cap (ten, thuoc tinh) co trong
#      `_con_song` nen; T7 decorator, chu ky cua `_con_song` BANG nen, `def` moi khong decorator, khong gia tri mac dinh.
import ast
import builtins
import copy
import hashlib
import symtable
import sys

CANH = ("_khoa_danh_tinh", "_thanh_vien_nhom", "_chup_cay")
TU_DO = "_con_song"
BON = CANH + (TU_DO,)
# Hinh dang nen trong than nhanh Linux: [loi goi .read_text() khong doi so, hang ")", hang "Z", f-string "linux:..."]
HINH = {"_khoa_danh_tinh": [1, 1, 0, 1], "_thanh_vien_nhom": [1, 1, 1, 0], "_chup_cay": [1, 1, 1, 1]}
DANG_CHO_PHEP = (("read_text", (), {"encoding": "latin-1"}), ("read_bytes", (), {}))
TEN_THEM = ("UnicodeDecodeError", "bytes", "int", "len", "isinstance", "bool")
KHE = "KHE_KHOA_TU_DO"
NL = chr(10)


class Hong(Exception):
    pass


def so(a, b, d):
    """So cau truc hai cay AST (khong so vi tri dong/cot); tra (ma, duong) o cho lech dau tien, None neu bang."""
    if isinstance(a, ast.Name) and a.id == KHE:
        return None if khoa_hop_le(b) else ("K", d)
    if isinstance(a, ast.AST):
        if type(a) is not type(b):
            return ("=", d + " " + type(a).__name__ + "/" + type(b).__name__)
        for f in a._fields:
            r = so(getattr(a, f, None), getattr(b, f, None), d + "." + f)
            if r:
                return r
        return None
    if isinstance(a, list):
        if not isinstance(b, list) or len(a) != len(b):
            return ("=", d + " so phan tu")
        for i, (x, y) in enumerate(zip(a, b)):
            r = so(x, y, d + "[" + str(i) + "]")
            if r:
                return r
        return None
    return None if (type(a) is type(b) and a == b) else ("=", d + " " + repr(a)[:30] + "/" + repr(b)[:30])


def khoa_hop_le(e):
    if not isinstance(e, ast.expr):
        return False
    n = 0
    for x in ast.walk(e):
        if isinstance(x, ast.Subscript):
            s = x.slice
            if not (isinstance(x.value, ast.Name) and x.value.id == "sau" and isinstance(s, ast.Constant)
                    and type(s.value) is int and s.value == 19):
                return False
            n += 1
        elif isinstance(x, ast.Call):
            f = x.func
            if not ((isinstance(f, ast.Name) and f.id in ("int", "str"))
                    or (isinstance(f, ast.Attribute) and f.attr == "decode")):
                return False
        elif isinstance(x, ast.Name):
            if x.id not in ("sau", "int", "str"):
                return False
        elif isinstance(x, ast.Attribute):
            if x.attr != "decode":
                return False
        elif not isinstance(x, (ast.JoinedStr, ast.FormattedValue, ast.Constant, ast.BinOp, ast.Add, ast.Load,
                                ast.keyword)):
            return False
    return n == 1


def la_linux(n):
    t = getattr(n, "test", None)
    return (isinstance(n, ast.If) and isinstance(t, ast.Compare) and isinstance(t.left, ast.Name)
            and t.left.id == "he" and len(t.ops) == 1 and isinstance(t.ops[0], ast.Eq)
            and len(t.comparators) == 1 and isinstance(t.comparators[0], ast.Constant)
            and t.comparators[0].value == "Linux")


class DoiKhoa(ast.NodeTransformer):
    def __init__(self, khe):
        self.n, self.khe = 0, khe

    def visit_JoinedStr(self, x):
        if x.values and isinstance(x.values[0], ast.Constant) and str(x.values[0].value).startswith("linux:"):
            self.n += 1
            if self.khe:
                return ast.Name(id=KHE, ctx=ast.Load())
        return x


def mong_doi(ham, dang):
    """Ham nen sau phep doi DUY NHAT duoc phep, CHI trong than nhanh `if he == "Linux":`."""
    e = copy.deepcopy(ham)
    nhanh = [n for n in ast.walk(e) if la_linux(n)]
    if len(nhanh) != 1:
        raise Hong(ham.name + ": nen co " + str(len(nhanh)) + " nhanh Linux")
    ten, a, k = dang
    la_bytes = ten == "read_bytes"
    dk = DoiKhoa(la_bytes)
    nhanh[0].body = [dk.visit(c) for c in nhanh[0].body]
    dem = [0, 0, 0, dk.n]
    for c in nhanh[0].body:
        for x in ast.walk(c):
            if (isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute) and x.func.attr == "read_text"
                    and not x.args and not x.keywords):
                dem[0] += 1
                x.func.attr = ten
                x.args = [ast.Constant(value=v) for v in a]
                x.keywords = [ast.keyword(arg=kk, value=ast.Constant(value=vv)) for kk, vv in k.items()]
            elif isinstance(x, ast.Constant) and type(x.value) is str and x.value in (")", "Z"):
                dem[1 if x.value == ")" else 2] += 1
                if la_bytes:
                    x.value = x.value.encode()
    if dem != HINH[ham.name]:
        raise Hong(ham.name + ": hinh dang nen " + str(dem) + " != " + str(HINH[ham.name]))
    return e


def la_def(n):
    return isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))


def dinh(t):
    d = {}
    for n in t.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            d.setdefault(n.name, []).append(n)
    return d


def toan_cuc(tb):
    ra = set()
    for s in tb.get_symbols():
        if s.is_global() or s.is_declared_global():
            ra.add(s.get_name())
    for c in tb.get_children():
        ra |= toan_cuc(c)
    return ra


def bang_ham(top, ten):
    v = [c for c in top.get_children() if c.get_name() == ten and str(c.get_type()).lower().endswith("function")]
    return v[0] if len(v) == 1 else None


def la_version(n):
    return (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
            and n.targets[0].id == "VERSION" and isinstance(n.value, ast.Constant) and type(n.value.value) is str)


class Nen:
    def __init__(self, t):
        self.t = t
        d = dinh(t)
        for h in BON:
            if len(d.get(h, [])) != 1:
                raise Hong("nen: " + h + " khong phai dung mot def muc module")
        self.ham = {h: d[h][0] for h in BON}
        top = symtable.symtable(ast.unparse(t), "nen", "exec")
        self.ten_module = {s.get_name() for s in top.get_symbols()} | set(dir(builtins))
        self.g = toan_cuc(bang_ham(top, TU_DO))
        f = self.ham[TU_DO]
        self.cap = {(x.value.id, x.attr) for x in ast.walk(f)
                    if isinstance(x, ast.Attribute) and isinstance(x.value, ast.Name) and x.value.id in self.g}
        self.imp = [ast.dump(x) for x in ast.walk(f) if isinstance(x, (ast.Import, ast.ImportFrom))]


def kiem(nen, u, dang):
    loi = []
    d = dinh(u)
    for h in BON:
        if len(d.get(h, [])) != 1:
            loi.append("M " + h + ": " + str(len(d.get(h, []))) + " def muc module, phai dung 1")
    for h in CANH:
        if len(d.get(h, [])) == 1:
            r = so(mong_doi(nen.ham[h], dang), d[h][0], h)
            if r:
                loi.append(("K " if r[0] == "K" else "H ") + r[1])
    moi, giu_u = [], []
    for n in u.body:
        if la_def(n) and n.name in BON:
            continue
        if isinstance(n, ast.FunctionDef) and n.name not in nen.ten_module:
            moi.append(n)
            continue
        giu_u.append(n)
    giu_n = [n for n in nen.t.body if not (la_def(n) and n.name in BON)]
    ten_moi = [n.name for n in moi]
    if len(set(ten_moi)) != len(ten_moi):
        loi.append("M def moi trung ten: " + ",".join(sorted(ten_moi)))
    vn = [n for n in giu_n if la_version(n)]
    if len(vn) == 1:        # CHI gia tri chuoi cua VERSION duoc doi: chuan hoa ve nen truoc khi so
        giu_u = [ast.Assign(targets=n.targets, value=vn[0].value) if la_version(n) else n for n in giu_u]
    r = so(giu_n, giu_u, "muc module")
    if r:
        i = r[1][len("muc module["):].split("]")[0] if r[1].startswith("muc module[") else ""
        x = giu_u[int(i)] if i.isdigit() and int(i) < len(giu_u) else None
        loi.append("M " + r[1] + " | dong ung vien " + str(getattr(x, "lineno", "?")))
    top = symtable.symtable(ast.unparse(u), "ung_vien", "exec")
    cho = nen.g | set(TEN_THEM) | set(ten_moi)
    ds = ([d[TU_DO][0]] if len(d.get(TU_DO, [])) == 1 else []) + moi
    for f in ds:
        tb = bang_ham(top, f.name)
        if tb is None:
            loi.append("T3 " + f.name + ": khong tim thay bang ky hieu")
            continue
        g = toan_cuc(tb)
        for n in ast.walk(f):
            dong = " dong " + str(getattr(n, "lineno", "?"))
            if isinstance(n, (ast.Global, ast.Nonlocal)):
                loi.append("T1 " + f.name + ":" + dong + " " + type(n).__name__ + " " + ",".join(n.names))
            elif isinstance(n, (ast.Import, ast.ImportFrom)) and ast.dump(n) not in nen.imp:
                loi.append("T2 " + f.name + ":" + dong + " import")
            elif isinstance(n, ast.Attribute):
                if n.attr.startswith("__") and n.attr.endswith("__"):
                    loi.append("T4 " + f.name + ":" + dong + " ." + n.attr)
                if not isinstance(n.ctx, ast.Load):
                    loi.append("T5 " + f.name + ":" + dong + " gan/xoa ." + n.attr)
                if isinstance(n.value, ast.Name) and n.value.id in g and (n.value.id, n.attr) not in nen.cap:
                    loi.append("T6 " + f.name + ":" + dong + " " + n.value.id + "." + n.attr)
            elif isinstance(n, ast.Subscript) and not isinstance(n.ctx, ast.Load):
                loi.append("T5 " + f.name + ":" + dong + " gan/xoa chi so")
        la = sorted(g - cho)
        if la:
            loi.append("T3 " + f.name + ": ten toan cuc ngoai danh sach " + ",".join(la))
        if f.name == TU_DO:
            for fld in ("decorator_list", "args", "returns"):
                r = so(getattr(nen.ham[TU_DO], fld), getattr(f, fld), TU_DO + "." + fld)
                if r:
                    loi.append("T7 " + r[1])
        elif f.decorator_list or f.args.defaults or any(x is not None for x in f.args.kw_defaults):
            loi.append("T7 " + f.name + ": def moi co decorator hay gia tri mac dinh")
    return loi


def ham_cua(t, ten):
    v = [n for n in t.body if la_def(n) and n.name == ten]
    if len(v) != 1:
        raise Hong("khong dung duoc doi chung: " + ten + " co " + str(len(v)) + " def")
    return v[0]


def cau(s):
    return ast.parse(s).body


def dc_nen(nen, u):
    return copy.deepcopy(nen.t)


def dc_tach(nen, u):
    t = copy.deepcopy(u)
    x = [n for n in ast.walk(ham_cua(t, "_khoa_danh_tinh")) if isinstance(n, ast.Attribute) and n.attr == "rindex"]
    if len(x) != 1:
        raise Hong("khong dung duoc doi chung tach: " + str(len(x)) + " .rindex")
    x[0].attr = "index"
    return t


def dc_deco(nen, u):
    t = copy.deepcopy(u)
    ham_cua(t, "_thanh_vien_nhom").decorator_list.append(ast.parse("_chup_cay", mode="eval").body)
    return t


def dc_gan_lai(nen, u):
    t = copy.deepcopy(u)
    i = t.body.index(ham_cua(t, "_thanh_vien_nhom"))
    t.body[i + 1:i + 1] = cau("_thanh_vien_nhom = _thanh_vien_nhom")
    return t


def dc_def_trung(nen, u):
    t = copy.deepcopy(u)
    t.body += cau("def Path():" + NL + "    return None")
    return t


def dc_con_song(dong):
    def dung(nen, u):
        t = copy.deepcopy(u)
        f = ham_cua(t, TU_DO)
        f.body[0:0] = cau(dong)
        return t
    return dung


def dc_mac_dinh(nen, u):
    t = copy.deepcopy(u)
    f = ham_cua(t, TU_DO)
    if len(f.args.defaults) != 1:
        raise Hong("khong dung duoc doi chung mac dinh")
    f.args.defaults[0] = ast.Constant(value=1)
    return t


def dc_phu(nen, u):
    t = copy.deepcopy(u)
    t.body += cau("def _dc_ham_moi():" + NL + "    global os" + NL + "    return None")
    return t


def dc_khoa(nen, u):
    t = copy.deepcopy(u)
    f = ham_cua(t, "_khoa_danh_tinh")
    v = [n for n in ast.walk(f) if isinstance(n, ast.Return) and n.value is not None
         and any(isinstance(s, ast.Subscript) and isinstance(s.slice, ast.Constant) and s.slice.value == 19
                 for s in ast.walk(n.value))]
    if len(v) != 1:
        raise Hong("khong dung duoc doi chung khoa")
    v[0].value = ast.parse(chr(34) + "linux:" + chr(34) + " + str(pid)", mode="eval").body
    return t


DOI_CHUNG = [
    ("nen", "H", dc_nen),
    ("tach_ngoac_dau", "H", dc_tach),
    ("decorator", "H", dc_deco),
    ("gan_lai_muc_module", "M", dc_gan_lai),
    ("def_ten_cu", "M", dc_def_trung),
    ("global", "T1", dc_con_song("global os")),
    ("import", "T2", dc_con_song("import os")),
    ("setattr", "T3", dc_con_song("setattr(pid, 'x', 1)")),
    ("dunder", "T4", dc_con_song("pid.__class__")),
    ("gan_thuoc_tinh", "T5", dc_con_song("pid.x = 1")),
    ("thuoc_tinh_toan_cuc", "T6", dc_con_song("os.open")),
    ("mac_dinh", "T7", dc_mac_dinh),
    ("def_moi_global", "T1", dc_phu),
    ("khoa_bytes", "K", dc_khoa),
]


def doc_dang(src):
    v = [n for n in ast.parse(src).body if isinstance(n, ast.Assign) and len(n.targets) == 1
         and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "DANG_DOC_QA7"]
    if len(v) != 1:
        raise Hong("DANG_DOC_QA7: " + str(len(v)) + " phep gan muc module, phai dung 1")
    dang = ast.literal_eval(v[0].value)
    if dang not in DANG_CHO_PHEP:
        raise Hong("DANG_DOC_QA7 ngoai danh sach cho phep: " + repr(dang))
    return dang


def main(argv):
    if len(argv) != 4:
        print("dung: chot_tinh_r12.py <launcher.py nen> <launcher.py ung vien> <launcher_test.py ung vien>")
        return 3
    try:
        b = [open(p, "rb").read() for p in argv[1:4]]
        dang = doc_dang(b[2].decode("utf-8"))
        nen = Nen(ast.parse(b[0].decode("utf-8")))
        for h in CANH:
            mong_doi(nen.ham[h], dang)
    except (OSError, SyntaxError, ValueError, Hong) as e:
        print("DAU VAO HONG:", type(e).__name__, e)
        return 3
    print("CHOT TINH r12 | python", sys.version.split()[0], "| sha256 nen", hashlib.sha256(b[0]).hexdigest(),
          "| ung vien", hashlib.sha256(b[1]).hexdigest(), "| test", hashlib.sha256(b[2]).hexdigest(),
          "| DANG_DOC_QA7", repr(dang))
    try:
        u = ast.parse(b[1].decode("utf-8"))
    except (SyntaxError, ValueError) as e:
        print("UNG VIEN: DO 1 | P khong parse duoc:", e)
        return 1
    try:
        loi = kiem(nen, u, dang)
    except Hong as e:
        print("DAU VAO HONG:", e)
        return 3
    print("UNG VIEN:", "DAT" if not loi else "DO " + str(len(loi)) + " | " + " ; ".join(loi))
    hong_dc = 0
    for ten, ma, dung in DOI_CHUNG:
        if ma == "K" and dang[0] != "read_bytes":
            print("DOI CHUNG", ten, "[K]: khong ap dung (dang latin-1: bieu thuc khoa phai BANG nen, luat H)")
            continue
        try:
            moi = [x for x in kiem(nen, dung(nen, u), dang) if x not in loi]
        except Hong as e:
            print("DOI CHUNG", ten, "[" + ma + "]: KHONG DUNG DUOC |", e)
            hong_dc += 1
            continue
        dung_luat = bool(moi) and all(x.split(" ", 1)[0] == ma for x in moi)
        print("DOI CHUNG", ten, "[" + ma + "]:", "DO DUNG LUAT" if dung_luat else "KHONG DO DUNG LUAT",
              "|", " ; ".join(moi)[:200])
        hong_dc += 0 if dung_luat else 1
    rc = 1 if loi else (2 if hong_dc else 0)
    print("KET LUAN:", {0: "DAT", 1: "DO (ung vien)", 2: "DO (doi chung khong do dung luat)"}[rc], "| rc=" + str(rc))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
