"""Do THAT N2 cua #1342 r2 (spec WP1174-WINDOWS-BACKEND-r2 §4 N2) tren Linux, ngoai kho; chi doc blob qua git show.
Dung: python -X utf8 -B n2_1384.py <clone_day_du_lich_su> <B> <H> <P> <M>
  B = OID base trong lease (641108c), H = exact head (c10d071), P = cha thu nhat cua merge, M = merge (d1ca71a).
Helper `_additive1342r2` nap tu packet_loop_test.py cua HEAD (dung spec: "nap .claude/dev/packet_loop_test.py cua head").
Doi chung (phai []): (B,H), (P,M); tu kiem: (B,B), (B, B + mot ham `_1174_win_x` hop le), (H,H).
Doi chung helper r1: `_additive1342(B,B)` phai KHAC [] (ly do can M7).
Phan chung tren blob H, moi bien the doi MOT thu, phai KHAC []:
  (n2a) sua mot byte trong than `_1174_win_api` (ham r1); (n2b) sua mot byte trong than `_1174_lock`;
  (n2c) them `@contextlib.contextmanager` vao `_1174_win_lock`.
Moi cap (tim, thay) phai khop DUNG MOT cho; khong khop => KHONG_DO (khong tinh)."""
import json, pathlib, subprocess, sys, tempfile, warnings
warnings.simplefilter("ignore", SyntaxWarning)
SRC, B, H, P, M = sys.argv[1:6]
SRC = pathlib.Path(SRC)
F, FT = ".claude/dev/packet_loop.py", ".claude/dev/packet_loop_test.py"
g = lambda r, f=F: subprocess.run(["git", "-C", str(SRC), "show", f"{r}:{f}"], capture_output=True, check=True).stdout

_TMP = tempfile.TemporaryDirectory()
_d = pathlib.Path(_TMP.name) / "h"
subprocess.run(["git", "clone", "-q", "--no-hardlinks", "--no-checkout", str(SRC), str(_d)], check=True)
subprocess.run(["git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", H], cwd=_d, check=True)
sys.dont_write_bytecode = True
sys.path.insert(0, str(_d / ".claude/dev"))
import packet_loop_test as T  # noqa: E402  (ban o exact head H)
assert pathlib.Path(T.__file__).resolve().parent == (_d / ".claude/dev").resolve(), T.__file__

bao = {"B": B, "H": H, "P": P, "M": M, "helper_tu": f"{H}:{FT}", "doi_chung": {}, "tu_kiem": {}, "phan_chung": {}}


def doi(buf, tim, thay):
    n = buf.count(tim)
    if n != 1:
        return None, f"KHONG_DO: mau khop {n} lan"
    return buf.replace(tim, thay), None


bb, hb = g(B), g(H)
bao["doi_chung"]["B_H"] = T._additive1342r2(bb, hb)
bao["doi_chung"]["P_M"] = T._additive1342r2(g(P), g(M))
bao["doi_chung"]["helper_r1__additive1342_B_B"] = T._additive1342(bb, bb)
bao["tu_kiem"]["B_B"] = T._additive1342r2(bb, bb)
_cong, _l = doi(bb, b"\ndef _1174_win_open(c, k, text, access, share, flags):\n",
                b"\ndef _1174_win_x(a=1, *, b=None):\n    return a\n\n\ndef _1174_win_open(c, k, text, access, share, flags):\n")
# chen mot khoi top-level hop le GIUA hai def san co (dung hinh dang mot khoi moi), khong noi vao cuoi tep
bao["tu_kiem"]["B_cong_ham_1174_win_x"] = _l or T._additive1342r2(bb, _cong)
bao["tu_kiem"]["H_H"] = T._additive1342r2(hb, hb)
PC = {
    "n2a_mot_byte_than__1174_win_api": (b'    k = c.WinDLL("kernel32", use_last_error=True)\n', b'    k = c.WinDLL("kernel33", use_last_error=True)\n'),
    "n2b_mot_byte_than__1174_lock": (b'        _1174_require(stat.S_ISREG(os.fstat(fd).st_mode), "fixed lock must be regular")\n',
                                     b'        _1174_require(stat.S_ISREG(os.fstat(fd).st_mode), "fixed lock must be regulas")\n'),
    "n2c_contextmanager_vao__1174_win_lock": (b"\ndef _1174_win_lock(path):\n", b"\n@contextlib.contextmanager\ndef _1174_win_lock(path):\n"),
}
for ten, (tim, thay) in PC.items():
    bien, loi = doi(hb, tim, thay)
    if loi:
        bao["phan_chung"][ten] = {"ket_qua": loi}
        continue
    kq = T._additive1342r2(bb, bien)
    bao["phan_chung"][ten] = {"additive": kq, "ket_qua": "DO_DUNG" if kq else "SONG"}

ok = (bao["doi_chung"]["B_H"] == [] and bao["doi_chung"]["P_M"] == [] and bao["doi_chung"]["helper_r1__additive1342_B_B"] != []
      and all(v == [] for v in bao["tu_kiem"].values()) and all(v.get("ket_qua") == "DO_DUNG" for v in bao["phan_chung"].values()))
bao["TONG"] = "DAT" if ok else "KHONG_DAT"
print(json.dumps(bao, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)
