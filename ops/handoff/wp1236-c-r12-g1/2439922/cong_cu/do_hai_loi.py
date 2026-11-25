"""Do hanh vi khi bien ban VUA sai duong dan VUA co OID khong tren remote, tren mot clone (doi so: goc clone). In rc + moi dong stderr/stdout."""
import sys, tempfile
from pathlib import Path
goc = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(goc / ".claude/dev"))
import packet_loop_test as T  # noqa: E402
with tempfile.TemporaryDirectory() as td:
    c = T.Ctx(T.CANONICAL, Path(td))
    x = T._d1106_kho(c, day=False)
    for nhan, doi in (("duong_dan_sai + oid_khong_tren_remote", T._NG(tep="x")), ("chi oid_khong_tren_remote", None), ("mien: duong dan sai + oid", T._d2b_mien(readback_thu_muc="x"))):
        rc, o, e = T._d1106_chay(c, x, doi)
        print(f"[{nhan}] rc={rc}", "| stdout:", [d for d in o.decode().splitlines()], "| stderr:", [d.strip() for d in e.decode().splitlines()])
