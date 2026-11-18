"""Do THAT phan Linux con la loi khai cua N1/N3/N4 cho #1342 r2 (spec WP1174-WINDOWS-BACKEND-r2 §4), ngoai kho, ban sao tam.
Dung: python -X utf8 -B n134_1384.py <clone_day_du_lich_su> <B> <H> <M>
  B = OID base trong lease (641108c), H = exact head (c10d071), M = merge (d1ca71a).
N1: MUTANTS cua packet_loop_test.py o H bang CHINH XAC o B (cung tap khoa, cung repr gia tri), moi ban nap trong TIEN TRINH RIENG;
    phan chung: doi ten mot khoa trong ban H, giu nguyen so luong => phep so phai DO.
N3: ca `wp1342_additive_byte_preserved` tren cay lam viec o M phai DAT (doi chung); phan chung: chen loi goi `_1174_win_lock(path)`
    vao than `_1174_lock` => ca phai DO va loi phai la assertion vế N3 ("N3 trên CÂY LÀM VIỆC").
N4: ca `wp1342_pure_lock_persist_refuse` (M4) tren M phai DAT (doi chung); phan chung: xoa dong kiem kieu "persist bytes/mode"
    o `_1174_win_persist` => ca phai DO va loi phai la AssertionError cua `_reject1174` (ly do doi thanh thong bao khac).
Moi cap (tim, thay) phai khop DUNG MOT cho; khong khop => KHONG_DO (khong tinh)."""
import json, pathlib, subprocess, sys, tempfile
SRC, B, H, M = sys.argv[1:5]
SRC = pathlib.Path(SRC)
F = ".claude/dev/packet_loop.py"
bao = {"B": B, "H": H, "M": M, "n1": {}, "n3": {}, "n4": {}}

MUT = ("import sys,json;sys.path.insert(0,'.claude/dev');import packet_loop_test as T;"
       "print('MUT_JSON '+json.dumps({k:repr(v) for k,v in T.MUTANTS.items()}))")
LENH = ("import sys,tempfile,pathlib,json;sys.path.insert(0,'.claude/dev');import packet_loop_test as T;"
        "k=T.chay_suite(T.CANONICAL,pathlib.Path(tempfile.mkdtemp()),set(sys.argv[1:]));"
        "print('KQ_JSON '+json.dumps({n:(None if v is None else [type(v).__name__,str(v)[:900]]) for n,v in k.items()}))")


def doi(buf, tim, thay):
    n = buf.count(tim)
    if n != 1:
        return None, f"KHONG_DO: mau khop {n} lan"
    return buf.replace(tim, thay), None


def clone(tmp, ten, rev):
    d = pathlib.Path(tmp) / ten
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", "--no-checkout", str(SRC), str(d)], check=True)
    subprocess.run(["git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", rev], cwd=d, check=True)
    subprocess.run(["git", "config", "core.abbrev", "7"], cwd=d, check=True)
    return d


def mutants(goc):
    p = subprocess.run([sys.executable, "-X", "utf8", "-B", "-c", MUT], cwd=goc, capture_output=True, text=True, timeout=600)
    for d in p.stdout.splitlines():
        if d.startswith("MUT_JSON "):
            return json.loads(d[9:])
    raise SystemExit(f"khong nap duoc MUTANTS o {goc}: rc {p.returncode} {p.stderr[-600:]}")


def chay(goc, ca):
    p = subprocess.run([sys.executable, "-X", "utf8", "-B", "-c", LENH, ca], cwd=goc, capture_output=True, text=True, timeout=900)
    kq = None
    for d in p.stdout.splitlines():
        if d.startswith("KQ_JSON "):
            kq = json.loads(d[8:])
    return {"rc": p.returncode, "kq": kq, "stderr_cuoi": p.stderr[-800:]}


def phan_chung(d, tim, thay, ca, dau):
    f = d / F
    goc = f.read_bytes()
    bien, loi = doi(goc, tim, thay)
    if loi:
        return {"ket_qua": loi}
    f.write_bytes(bien)
    try:
        r = chay(d, ca)
    finally:
        f.write_bytes(goc)
    v = (r["kq"] or {}).get(ca)
    dung = bool(v) and v[0] == "str" and v[1].startswith(dau)
    r["ket_qua"] = "DO_DUNG" if dung else ("SONG" if v is None and r["kq"] else "KHONG_DO")
    return r


with tempfile.TemporaryDirectory() as tmp:
    mb, mh = mutants(clone(tmp, "b", B)), mutants(clone(tmp, "h", H))
    bao["n1"]["so_luong"] = {"B": len(mb), "H": len(mh)}
    bao["n1"]["bang_nhau"] = mb == mh
    k0 = sorted(mh)[0]
    mh2 = dict(mh)
    mh2[k0 + "__doi_ten"] = mh2.pop(k0)
    bao["n1"]["phan_chung_doi_ten_khoa"] = {"khoa": k0, "so_luong": len(mh2), "bang_nhau": mb == mh2,
                                           "ket_qua": "DO_DUNG" if (len(mh2) == len(mb) and mb != mh2) else "SONG"}
    d = clone(tmp, "m", M)
    C3, C4 = "wp1342_additive_byte_preserved", "wp1342_pure_lock_persist_refuse"
    bao["n3"]["doi_chung_sach"] = chay(d, C3)
    bao["n3"]["chen_goi__1174_win_lock_vao__1174_lock"] = phan_chung(
        d, b"def _1174_lock(path):\n    import fcntl\n    import stat\n",
        b"def _1174_lock(path):\n    import fcntl\n    import stat\n    _1174_win_lock(path)\n", C3, "AssertionError: ('N3 trên CÂY LÀM VIỆC'")
    bao["n4"]["doi_chung_sach"] = chay(d, C4)
    bao["n4"]["xoa_kiem_kieu_persist_o__1174_win_persist"] = phan_chung(
        d, b"    import ntpath\n    _1174_require(type(raw) is bytes and type(create) is bool, \"persist bytes/mode\")\n",
        b"    import ntpath\n", C4, "AssertionError")

ok = (bao["n1"]["bang_nhau"] and bao["n1"]["phan_chung_doi_ten_khoa"]["ket_qua"] == "DO_DUNG"
      and (bao["n3"]["doi_chung_sach"]["kq"] or {}).get(C3, 1) is None and bao["n3"]["chen_goi__1174_win_lock_vao__1174_lock"]["ket_qua"] == "DO_DUNG"
      and (bao["n4"]["doi_chung_sach"]["kq"] or {}).get(C4, 1) is None and bao["n4"]["xoa_kiem_kieu_persist_o__1174_win_persist"]["ket_qua"] == "DO_DUNG")
bao["TONG"] = "DAT" if ok else "KHONG_DAT"
print(json.dumps(bao, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)
