"""Do hanh vi D2b duoi dot bien d2b_mC11_bo_mode (bo kiem mode) tren cac bien the symlink/mode cua cong_d2b_c5_mode, so voi ban goc.
In (rc, ly do THIEU D2b | dong KHONG DO DUOC, dong D2b stdout). dung: do_mc11.py <goc checkout>"""
import sys, tempfile, warnings
from pathlib import Path

warnings.simplefilter("ignore")
R = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(R / ".claude/dev"))
import packet_loop_test as T  # noqa: E402

nguon = T.CANONICAL.read_text(encoding="utf-8")
tim, thay, _ = T.MUTANTS["d2b_mC11_bo_mode"]
assert nguon.count(tim) == 1
BT = [("tep_la_symlink", T._NG(tep=T._D2B_L("lk5", "danh-gia-gate-output-1.txt"))), ("thu_muc_la_symlink", T._NG(tep=f"ops/land/lk-provenance/{T._D2B_F}")),
      ("mien_thu_muc_la_tep", T._d2b_mien(readback_thu_muc=T._D2B_TEP))]
with tempfile.TemporaryDirectory() as td:
    for ten, src in (("goc", nguon), ("mC11", nguon.replace(tim, thay))):
        d = Path(td) / ten
        d.mkdir()
        (d / "packet_loop.py").write_text(src, encoding="utf-8", newline="\n")
        (d / "launcher.py").write_text((R / ".claude/dev/launcher.py").read_text(encoding="utf-8"), encoding="utf-8")
        (d / "t").mkdir()
        c = T.Ctx(d / "packet_loop.py", d / "t")
        x = T._d1106_kho(c, o=T._d2b_cay)
        for nhan, doi in BT:
            rc, o, e = T._d1106_chay(c, x, doi)
            dong = lambda b: [s.strip() for s in b.decode().split("\n")]  # noqa: E731
            print(f"{ten:5} {nhan:22} rc={rc} {[s for s in dong(e) if s.startswith(('THIẾU  D2b', 'KHÔNG ĐO'))]} {[s[:60] for s in dong(o) if s.startswith('D2b')]}")
