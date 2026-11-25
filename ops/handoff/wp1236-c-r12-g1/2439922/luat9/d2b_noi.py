#!/usr/bin/env python3
"""Bo NOI cho luat 9 (wp1236 dot C): cho bo quet ghim `ops/reviews/wp1236-r10-soan/quet_dot_bien.py` (KHONG sua) do tren khoi D2b
cua `.claude/dev/packet_loop.py`. Cong cu DO dev-side cua executor, khong phai ma thi cong, khong nam trong write set.

Vi sao can: bo quet ghi ban dot bien ra tep `gate_output_doi_chieu.py`, dat bien `GATE_OUTPUT_DOI_CHIEU_MA`, va doi tep test co `CA` +
`chay_ca(ten) -> (rc, dong)` (rc 3 = GIET). `packet_loop_test.py` khong co giao dien ay, va `sinh` tren ca `packet_loop.py` (7,6k dong)
khong xong trong 600 s. Nen:

  trich  <packet_loop.py> <ra.py>   cat KHOI D2b (tu dong moc `# --- #1236 dot C` toi truoc `def cmd_kiem_dong_wp`) thanh module rieng
                                    de bo quet sinh manifest tren DUNG phan ma dot C them.
  (nap boi bo quet)                 `CA` = cac ca `cong_d2b_*` (tru ca tu kiem phan hang: no doc mo neo van ban cua ban goc);
                                    `chay_ca` ghep ban dot bien cua khoi vao `packet_loop.py` cua kho (bien WP1236C_GOC), chay DUNG
                                    `chay_suite` cua `packet_loop_test.py` cho mot ca. GIET (rc 3) chi khi bo phan hang cua chinh
                                    `packet_loop_test.py` ra GIET (ca nem `ChotB4(<ten ca>)`); CLI sap / dung fixture hong => rc 1 (HONG).
"""
import atexit, os, shutil, sys, tempfile
from pathlib import Path

DAU, CUOI = "# --- #1236 đợt C (`ops/specs/wp1236-r12.md`, mục *D2b chi tiết*): `moc_10_2_2.gate_output`", "def cmd_kiem_dong_wp(a, state_dir: Path) -> int:\n"


def cat(nguon):
    i, j = nguon.index(DAU), nguon.index(CUOI)
    if nguon.count(DAU) != 1 or nguon.count(CUOI) != 1 or i >= j:
        raise SystemExit("KHONG_DO_DUOC: moc khoi D2b khong khop dung mot cho")
    return i, j


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] != "trich":
        raise SystemExit(__doc__)
    s = Path(sys.argv[2]).read_text(encoding="utf-8")
    i, j = cat(s)
    Path(sys.argv[3]).write_text(s[i:j].rstrip("\n") + "\n", encoding="utf-8", newline="\n")
    print(f"TRICH {len(s[i:j].splitlines())} dong")
else:
    GOC = Path(os.environ["WP1236C_GOC"]).resolve()
    sys.path.insert(0, str(GOC / ".claude/dev"))
    import packet_loop_test as T  # noqa: E402

    _tam = Path(tempfile.mkdtemp(prefix="d2b_noi_"))
    atexit.register(shutil.rmtree, _tam, ignore_errors=True)
    _goc = T.CANONICAL.read_text(encoding="utf-8")
    _i, _j = cat(_goc)
    _khoi = Path(os.environ["GATE_OUTPUT_DOI_CHIEU_MA"]).read_text(encoding="utf-8")
    (_tam / "packet_loop.py").write_text(_goc[:_i] + _khoi.rstrip("\n") + "\n\n\n" + _goc[_j:], encoding="utf-8", newline="\n")
    (_tam / "launcher.py").write_text((T.HERE / "launcher.py").read_text(encoding="utf-8"), encoding="utf-8")
    CA = [t for t, _ in T.CASES if t.startswith("cong_d2b_") and t != "cong_d2b_tu_kiem_phan_hang"]
    if len(CA) < 14:
        raise SystemExit(f"KHONG_DO_DUOC: chi thay {len(CA)} ca cong_d2b_")

    def chay_ca(ten):
        v = T.chay_suite(_tam / "packet_loop.py", _tam / "ca", chi_chay={ten}).get(ten, "ca khong chay")
        return (0, "") if v is None else (3 if T._phan_loai_giet(v) == "GIET" else 1, str(v))
