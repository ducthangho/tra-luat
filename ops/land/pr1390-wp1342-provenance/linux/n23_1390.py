"""Do THAT phan chung N2/N3 cua #1342 r3 (spec WP1174-WINDOWS-BACKEND-r3 §5) tren Linux, trong ban sao tam (ngoai kho).
Dung: python -X utf8 -B n23_1390.py <clone_day_du_lich_su> <B> <H> <P> <M>
N2: _additive1342r2(blob B, blob H) va (blob P, blob M) phai [] (doi chung); phan chung tren blob H, moi bien the doi MOT thu:
    (n2a) sua mot byte than ham r1 `_1174_win_read`; (n2b) sua mot byte than ham r2 `_1174_win_lock`;
    (n2c) them decorator vao ham moi r3 `_1174_win_seed_acl` => phai KHAC [].
N3: ca `wp1342_additive_byte_preserved` tren cay lam viec o M phai DAT (doi chung); phan chung: chen loi goi `_1174_win_seed(e)`
    vao than `_1174_seed` cua cay lam viec => ca phai DO va loi phai la assertion vế N3 ("N3 trên CÂY LÀM VIỆC").
Moi cap (tim, thay) phai khop DUNG MOT cho; khong khop => KHONG_DO (khong tinh)."""
import json, pathlib, subprocess, sys, tempfile, warnings
warnings.simplefilter("ignore", SyntaxWarning)
SRC, B, H, P, M = sys.argv[1:6]
SRC = pathlib.Path(SRC)
F = ".claude/dev/packet_loop.py"
g = lambda r: subprocess.run(["git", "-C", str(SRC), "show", f"{r}:{F}"], capture_output=True, check=True).stdout
sys.path.insert(0, str(SRC / ".claude/dev"))
import packet_loop_test as T  # noqa: E402  (ban o SRC; chi dung ham thuan _additive1342r2)

bao = {"B": B, "H": H, "P": P, "M": M, "n2": {}, "n3": {}}


def doi(buf, tim, thay):
    n = buf.count(tim)
    if n != 1:
        return None, f"KHONG_DO: mau khop {n} lan"
    return buf.replace(tim, thay), None


hb, bb = g(H), g(B)
bao["n2"]["doi_chung_B_H"] = T._additive1342r2(bb, hb)
bao["n2"]["doi_chung_P_M"] = T._additive1342r2(g(P), g(M))
N2 = {
    "n2a_mot_byte_than_ham_r1__1174_win_read": (b"    text = os.fspath(path)\n    _1174_require(_1174_win_path(text), \"Windows drive path required\")\n    c, w, k = _1174_win_api()\n    handle = _1174_win_open(c, k, text, 0x80000000, 1, 0x00200000)\n",
                                                b"    text = os.fspath(path)\n    _1174_require(_1174_win_path(text), \"Windows drive path required\")\n    c, w, k = _1174_win_api()\n    handle = _1174_win_open(c, k, text, 0x80000000, 1, 0x00200001)\n"),
    "n2b_mot_byte_than_ham_r2__1174_win_lock": (b"    GENERIC_READ|GENERIC_WRITE, share READ|WRITE (no DELETE), OPEN_ALWAYS on the reparse point itself, handle not\n",
                                                b"    GENERIC_READ|GENERIC_WRITE, share READ|WRITE (no DELETE), OPEN_ALWAYS on the reparse point itself, handle nat\n"),
    "n2c_decorator_vao_ham_moi_r3__1174_win_seed_acl": (b"\ndef _1174_win_seed_acl(sddl, user_sid):\n",
                                                        b"\n@functools.lru_cache\ndef _1174_win_seed_acl(sddl, user_sid):\n"),
}
for ten, (tim, thay) in N2.items():
    bien, loi = doi(hb, tim, thay)
    if loi:
        bao["n2"][ten] = {"ket_qua": loi}
        continue
    kq = T._additive1342r2(bb, bien)
    bao["n2"][ten] = {"additive": kq, "ket_qua": "DO_DUNG" if kq else "SONG"}

LENH = ("import sys,tempfile,pathlib,json;sys.path.insert(0,'.claude/dev');import packet_loop_test as T;"
        "k=T.chay_suite(T.CANONICAL,pathlib.Path(tempfile.mkdtemp()),set(sys.argv[1:]));"
        "print('KQ_JSON '+json.dumps({n:(None if v is None else [type(v).__name__,str(v)[:900]]) for n,v in k.items()}))")
CA = "wp1342_additive_byte_preserved"


def chay(goc):
    p = subprocess.run([sys.executable, "-X", "utf8", "-B", "-c", LENH, CA], cwd=goc, capture_output=True, text=True, timeout=900)
    kq = None
    for d in p.stdout.splitlines():
        if d.startswith("KQ_JSON "):
            kq = json.loads(d[8:])
    return {"rc": p.returncode, "kq": kq, "stderr_cuoi": p.stderr[-800:]}


with tempfile.TemporaryDirectory() as tmp:
    d = pathlib.Path(tmp) / "m"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(SRC), str(d)], check=True)
    subprocess.run(["git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", M], cwd=d, check=True)
    subprocess.run(["git", "config", "core.abbrev", "7"], cwd=d, check=True)
    bao["n3"]["doi_chung_sach"] = chay(d)
    f = d / F
    goc = f.read_bytes()
    bien, loi = doi(goc, b"def _1174_seed(e):\n    import stat\n", b"def _1174_seed(e):\n    import stat\n    _1174_win_seed(e)\n")
    if loi:
        bao["n3"]["n3_chen_goi__1174_win_seed_trong__1174_seed"] = {"ket_qua": loi}
    else:
        f.write_bytes(bien)
        r = chay(d)
        v = (r["kq"] or {}).get(CA)
        # chay_suite luu loi dang CHUOI "AssertionError: ..." (khuon dot_bien_linux_1390.py) => v = ["str", "AssertionError: ..."]
        dung = bool(v) and v[0] == "str" and v[1].startswith("AssertionError: ('N3 trên CÂY LÀM VIỆC'")
        r["ket_qua"] = "DO_DUNG" if dung else ("SONG" if v is None and r["kq"] else "KHONG_DO")
        bao["n3"]["n3_chen_goi__1174_win_seed_trong__1174_seed"] = r
        f.write_bytes(goc)

print(json.dumps(bao, ensure_ascii=False, indent=1))
