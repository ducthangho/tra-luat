# -*- coding: utf-8 -*-
"""ci_phamvi_test.py — PHAN CHUNG chay duoc cho `ci_phamvi.py` (ve BAM).

Moi luat mot ca, moi ca mot DOT BIEN giet dung no; mot ca chi khang dinh `rc=0` la loi khai,
khong phai phep do. DOT BIEN CHAY TREN BAN SAO (`git worktree add --detach`), KHONG tren cay
that: mot luot bi cat giua chung de lai tep meo va luot sau doc ban meo lam ban goc.

DOI CHUNG TRUOC, HIEU SO SAU: moi ca "dot bien X phai lam DO" deu chay ban SACH truoc va doi
no XANH — do sach khong doi chung thi khong tach duoc "do vi dot bien" voi "do san".

`khoi_phuc` don `__pycache__` truoc MOI ca: ca truoc de lai `.pyc` cua `release.py` da dot
bien thi ca sau co the chay MA CU — co che CLAUDE.md ghi la tung tuoc rang moi mutant.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
CHECK = ".github/checks/ci_phamvi.py"
RELEASE = "scripts/tl_core/release.py"
CA = []


def ca(f):
    CA.append(f)
    return f


def chay(ws: Path, *args):
    r = subprocess.run([sys.executable, CHECK, *args], cwd=str(ws),
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def thay(ws: Path, tep: str, cu: str, moi: str):
    """Dot bien neo mot lan duy nhat — neo truot thi DUNG, dung doan."""
    p = ws / tep
    s = p.read_text(encoding="utf-8")
    if s.count(cu) != 1:
        raise AssertionError(f"neo dot bien truot: {cu!r} xuat hien {s.count(cu)} lan trong {tep}")
    p.write_text(s.replace(cu, moi), encoding="utf-8")


def khoi_phuc(ws: Path):
    subprocess.run(["git", "checkout", "--", RELEASE], cwd=str(ws), capture_output=True)
    shutil.copy2(GOC / CHECK, ws / CHECK)
    for d in (ws / "scripts").rglob("__pycache__"):  # .pyc cu => ca sau chay MA CU
        shutil.rmtree(d, ignore_errors=True)


@ca
def t1_sach_thi_xanh(ws):
    for co in (["--kiem-bam"], ["--bang"]):
        rc, out = chay(ws, *co)
        assert rc == 0, f"doi chung {co} phai xanh, duoc rc={rc}: {out}"


@ca
def n1_ma_bo_ops_thi_do(ws):
    """Dot bien MA, KHONG dong vao bang: thu phan biet "doc ma" voi "doc lai loi khai cua minh"."""
    thay(ws, RELEASE, '"ops",', "")
    rc, out = chay(ws, "--kiem-bam")
    assert rc != 0, f"bo ops khoi _RELEASE_EXCLUDE_DIRS ma cong van xanh: {out}"
    assert "ops" in out, f"thong diep khong neu ten nhom ops: {out}"


@ca
def n2_nhom_bia_thi_do(ws):
    thay(ws, CHECK, '"ops": "ops",', '"ops": "ops", "khong-co-that": "khong-co-that",')
    rc, out = chay(ws, "--kiem-bam")
    assert rc != 0, f"nhom tro vao thu khong co tren dia ma van xanh: {out}"
    assert "khong-co-that" in out, f"thong diep khong neu ten nhom bia: {out}"


@ca
def n3_khong_dan_xuat_duoc_thi_do(ws):
    """Trang thai THU BA co rang: nap hong KHONG duoc im lang thanh "khong loai tru gi"."""
    thay(ws, CHECK, "        from tl_core import release as R", "        raise ImportError('gia')")
    for co in (["--kiem-bam"], ["--bang"]):
        rc, out = chay(ws, *co)
        assert rc != 0, f"dan xuat hong ma {co} van xanh: {out}"
        assert "KHONG DO DUOC" in out, f"{co} thieu chu KHONG DO DUOC: {out}"
    # lop hai: go dung chot vua do => ca phai tro lai xanh, chung minh ca do CHOT DO.
    thay(ws, CHECK, "        return None          #", "        return set(NHOM)     #")
    rc, out = chay(ws, "--kiem-bam")
    assert rc == 0, f"go chot KHONG DO DUOC ma ca khong doi => ca do thu khac: {out}"


@ca
def n4_ops_van_doc_lap(ws):
    """Chieu BAT OAN co ca rieng. Ca chieu-tha khong chet bang dot bien go chot; thu giet no
    la dot bien SIET THEM (`bao_gio_cung_phu_thuoc`) — va no phai KHONG lam n1/n2 do."""
    rc, out = chay(ws, "--bang")
    assert rc == 0 and '"ops": "doc_lap"' in out, f"ops phai doc_lap tren cay sach: {out}"
    assert '"ops": "phu_thuoc"' not in out, f"ops bi bat oan tren cay sach: {out}"
    thay(ws, CHECK, "    return DOC_LAP if nhom in ngoai_goi else PHU_THUOC", "    return PHU_THUOC")
    rc, out = chay(ws, "--bang")
    assert '"ops": "doc_lap"' not in out, f"bao_gio_cung_phu_thuoc ma n4 khong doi: {out}"
    rc, out = chay(ws, "--kiem-bam")
    assert rc == 0, f"dot bien n4 lam --kiem-bam do => no khong chi giet n4: {out}"


def main() -> int:
    with tempfile.TemporaryDirectory() as tam:
        ws = Path(tam) / "ws"
        subprocess.run(["git", "worktree", "add", "--detach", str(ws), "HEAD"],
                       cwd=str(GOC), check=True, capture_output=True)
        try:
            dat = 0
            for f in CA:
                khoi_phuc(ws)
                try:
                    f(ws)
                except AssertionError as e:
                    print(f"  [DO] {f.__name__}: {e}")
                else:
                    dat += 1
                    print(f"  [OK] {f.__name__}")
            print(f"== ci_phamvi_test {dat}/{len(CA)} ==")
            return 0 if dat == len(CA) else 1
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(ws)],
                           cwd=str(GOC), capture_output=True)


if __name__ == "__main__":
    sys.exit(main())
