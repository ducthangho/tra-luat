# -*- coding: utf-8 -*-
"""ci_phamvi_test.py — PHAN CHUNG chay duoc cho `ci_phamvi.py`. Moi luat mot ca, moi ca
mot DOT BIEN giet dung no. Mot ca chi khang dinh `rc=0` la mot loi khai, khong phai phep do.

DOT BIEN CHAY TREN BAN SAO (`git worktree add --detach`), KHONG tren cay that: mot luot bi
cat giua chung de lai tep meo va luot sau doc ban meo lam ban goc. Da sap dung vay.

DOI CHUNG TRUOC, HIEU SO SAU: moi ca dang "dot bien X phai lam DO" deu chay ban SACH truoc
va doi no XANH — do sach khong doi chung thi khong tach duoc "do vi dot bien" voi "do san".
N3 va N5 con mot lop nua: sau khi thay ca DO, chung ap THEM mot dot bien vao dung chot ma
ca ay nham toi roi doi ca tro lai XANH, de biet ca do CHOT DO chu khong do thu khac.

Chay `python .github/checks/ci_phamvi_test.py` — ton ~4 phut vi N2 chay `tl selftest` 2 luot.
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


@ca
def t1_sach_kiem_bam_xanh(ws):
    rc, out = chay(ws, "--kiem-bam")
    assert rc == 0, f"doi chung kiem-bam phai xanh, duoc rc={rc}: {out}"


@ca
def t2_sach_kiem_doc_xanh(ws):
    rc, out = chay(ws, "--kiem-doc", "--buoc", "workflow-audit")
    assert rc == 0, f"doi chung kiem-doc phai xanh, duoc rc={rc}: {out}"


@ca
def n1_ma_bo_ops_thi_do(ws):
    """Chi dot bien MA (`_RELEASE_EXCLUDE_DIRS`), KHONG dong vao bang. Cong van phai DO —
    do la thu phan biet "doc ma" voi "doc lai chinh loi khai cua minh"."""
    thay(ws, RELEASE, '"ops",', "")
    rc, out = chay(ws, "--kiem-bam")
    assert rc != 0, f"bo ops khoi _RELEASE_EXCLUDE_DIRS ma cong van xanh: {out}"
    assert "ops" in out, f"thong diep khong neu ten nhom ops: {out}"


@ca
def n2_bang_bo_docs_cua_tl_selftest_thi_do(ws):
    rc, out = chay(ws, "--kiem-doc", "--buoc", "tl-selftest")
    assert rc == 0, f"doi chung tl-selftest phai xanh, duoc rc={rc}: {out}"
    thay(ws, CHECK, '"doc": {"docs", "CLAUDE.md", ".claude", ".github"}',
         '"doc": {"CLAUDE.md", ".claude", ".github", ".githooks"}')
    rc, out = chay(ws, "--kiem-doc", "--buoc", "tl-selftest")
    assert rc != 0, f"hoan vi tap DOC cua tl-selftest ma van xanh: {out}"
    assert "docs" in out, f"chieu 'doc ma khong khai' phai IN RA ten nhom, duoc: {out}"
    assert ".githooks" in out, f"chieu 'khai ma khong doc' khong bat: {out}"


@ca
def n3_khong_do_duoc_thi_do(ws):
    """Hook khong cai duoc => KHONG DO DUOC, KHONG duoc im lang thanh doc_lap."""
    thay(ws, CHECK, '_so = os.environ.get("CI_PHAMVI_SO")', "_so = None")
    rc, out = chay(ws, "--kiem-doc", "--buoc", "workflow-audit")
    assert rc != 0, f"hook hong ma cong van xanh: {out}"
    assert "KHONG DO DUOC" in out, f"thieu chu KHONG DO DUOC: {out}"
    # lop hai: go dung chot vua do => ca phai tro lai xanh, chung minh ca do CHOT DO.
    thay(ws, CHECK, 'return [f"KHONG DO DUOC: audit hook khong cai duoc cho buoc {buoc}"]',
         "return []")
    rc, out = chay(ws, "--kiem-doc", "--buoc", "workflow-audit")
    assert rc == 0, f"go chot KHONG DO DUOC ma ca khong doi => ca do thu khac: {out}"


@ca
def n4_nhom_bia_thi_do(ws):
    thay(ws, CHECK, '"ops": "ops",', '"ops": "ops", "khong-co-that": "khong-co-that",')
    rc, out = chay(ws, "--kiem-bam")
    assert rc != 0, f"nhom tro vao thu khong co tren dia ma van xanh: {out}"
    assert "khong-co-that" in out, f"thong diep khong neu ten nhom bia: {out}"


@ca
def n5_ops_van_doc_lap(ws):
    """`ops/**` phai DOC LAP voi ca 4 buoc. Ca chieu-tha khong chet bang dot bien go chot;
    thu giet no la `bao_gio_cung_phu_thuoc`. Va dot bien ay phai KHONG lam N1/N4 do —
    neu no lam moi ca cung do thi no khong chung minh duoc ca nay do dung thu no nham."""
    rc, out = chay(ws, "--bang", "--buoc", "workflow-audit")
    assert rc == 0 and '"ops": "doc_lap"' in out, f"ops phai doc_lap tren cay sach: {out}"
    assert '"ops": "phu_thuoc"' not in out, f"ops bi bat oan tren cay sach: {out}"
    thay(ws, CHECK, '    if buoc in BUOC_BAM:\n        return DOC_LAP if nhom in ngoai_goi else PHU_THUOC',
         "    return PHU_THUOC")
    rc, out = chay(ws, "--bang", "--buoc", "workflow-audit")
    assert '"ops": "doc_lap"' not in out, f"bao_gio_cung_phu_thuoc ma N5 khong doi: {out}"
    for co in (["--kiem-bam"], ["--kiem-doc", "--buoc", "doc-claims-check"]):
        rc, out = chay(ws, *co)
        assert rc == 0, f"dot bien N5 lam {co} do => no khong chi giet N5: {out}"


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
