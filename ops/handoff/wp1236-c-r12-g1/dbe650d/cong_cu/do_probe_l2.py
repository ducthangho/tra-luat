"""Chay lai phep do cua reviewer luot 2 (probe_case_directory.py: thu muc `A/note.txt` + `a/readback…`, bien ban mien tro `…/A`) tren mot checkout:
(1) doi chung Linux phan biet hoa/thuong; (2) mo phong extraction + tra cuu KHONG phan biet hoa/thuong (cung hai cho va nhu reviewer).
Khong assert: chi in rc va dong D2b. dung: do_probe_l2.py <goc checkout>"""
import contextlib, copy, io, sys, tarfile, tempfile, warnings
from pathlib import Path

warnings.simplefilter("ignore")
R = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(R / ".claude/dev"))
import packet_loop_test as T  # noqa: E402
import packet_loop as P  # noqa: E402

with tempfile.TemporaryDirectory() as td:
    c = T.Ctx(T.CANONICAL, Path(td))

    def build(w, m):
        for n in ("A", "a"):
            (w / T._D2B_PROV / n).mkdir()
        (w / T._D2B_PROV / "A/note.txt").write_bytes(b"note\n")
        T._d2b_readback(w, m, T._D2B_PROV + "/a")
    x = T._d1106_kho(c, o=build)
    rc, o, e = T._d1106_chay(c, x, T._d2b_mien(readback_thu_muc=T._D2B_PROV + "/A"))
    loc = lambda s: [d.strip() for d in s.splitlines() if "D2b" in d or "ĐÓNG ĐƯỢC" in d]  # noqa: E731
    print(f"(1) doi chung Linux      : rc={rc} {loc(o.decode() + e.decode())}")
    bung, goc_Path = tarfile.TarFile.extractall, P.Path

    class FoldPath(type(Path())):
        def __truediv__(self, other):
            return super().__truediv__(str(other).casefold())

    def bung_gop(self, path=".", members=None, **kw):
        ms = [copy.copy(t) for t in (members if members is not None else self.getmembers())]
        for t in ms:
            t.name = t.name.casefold()
        return bung(self, path, members=ms, **kw)
    P.Path, tarfile.TarFile.extractall = FoldPath, bung_gop
    so, se = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(so), contextlib.redirect_stderr(se):
            try:
                rc = P.main(["--state-dir", str(c.sd()), "kiem-dong-wp", "--root", str(x["w"]), "--bien-ban", str(x["goc"] / "bb.yaml"), "--lease", str(x["goc"] / "ls.yaml")])
            except SystemExit as ex:
                rc = ex.code
    finally:
        P.Path, tarfile.TarFile.extractall = goc_Path, bung
    print(f"(2) mo phong gop hoa/thuong: rc={rc} {loc(so.getvalue() + se.getvalue())}")
