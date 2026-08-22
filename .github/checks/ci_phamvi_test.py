# -*- coding: utf-8 -*-
"""ci_phamvi_test.py — PHAN CHUNG chay duoc cho `ci_phamvi.py`. Moi luat mot ca, moi ca mot
DOT BIEN giet dung no; mot ca chi khang dinh `rc=0` la loi khai, khong phai phep do.

DOT BIEN CHAY TREN BAN SAO (`git worktree add --detach`), KHONG tren cay that: mot luot bi cat
giua chung de lai tep meo va luot sau doc ban meo lam ban goc. Da sap dung vay. DOI CHUNG
TRUOC, HIEU SO SAU: moi ca "dot bien X phai lam DO" deu chay ban SACH truoc va doi no XANH —
do sach khong doi chung thi khong tach duoc "do vi dot bien" voi "do san". N3/N5/N6 con mot
lop nua: sau khi thay ca DO, chung ap THEM dot bien vao dung chot ca ay nham toi roi doi ca tro
lai XANH, de biet ca do CHOT DO chu khong do thu khac.
Chay `python .github/checks/ci_phamvi_test.py` — ton ~4 phut vi N2 chay `tl selftest` 2 luot.
"""
from __future__ import annotations

import os
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


def chay(ws: Path, *args, them_env=None):
    r = subprocess.run([sys.executable, CHECK, *args], cwd=str(ws),
                       env={**os.environ, **(them_env or {})}, capture_output=True, text=True)
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
def t1_sach_kiem_bam_xanh(ws):
    rc, out = chay(ws, "--kiem-bam")
    assert rc == 0, f"doi chung kiem-bam phai xanh, duoc rc={rc}: {out}"


@ca
def t2_sach_kiem_doc_xanh(ws):
    rc, out = chay(ws, "--kiem-doc", "--buoc", "workflow-audit")
    assert rc == 0, f"doi chung kiem-doc phai xanh, duoc rc={rc}: {out}"


@ca
def n1_ma_bo_ops_thi_do(ws):
    """Dot bien MA, KHONG dong vao bang: thu phan biet "doc ma" voi "doc lai loi khai cua minh"."""
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
    thay(ws, CHECK, 'return [f"KHONG DO DUOC: buoc {buoc} — {do_duoc}"]', "return []")
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
    """`ops/**` phai DOC LAP voi ca 4 buoc. Ca chieu-tha khong chet bang dot bien go chot; thu
    giet no la `bao_gio_cung_phu_thuoc` — va dot bien ay phai KHONG lam N1/N4 do."""
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


@ca
def n6_lenh_dich_hong_thi_khong_do_duoc(ws):
    """Lenh dich thoat khac 0 sau khi hook nap => tap doc MOT PHAN, gia dang phep do sach (#247)."""
    thay(ws, CHECK, '"workflow-audit", "--strict", "--json"', '"workflow-audit", "--co-nay-khong-co"')
    for co in (["--kiem-doc"], ["--bang"]):
        rc, out = chay(ws, *co, "--buoc", "workflow-audit")
        assert rc != 0, f"lenh dich thoat khac 0 ma {co} van xanh: {out}"
        assert "KHONG DO DUOC" in out, f"{co} thieu chu KHONG DO DUOC: {out}"
    thay(ws, CHECK, "    if r.returncode != 0:", "    if False:")
    rc, out = chay(ws, "--kiem-doc", "--buoc", "workflow-audit")
    assert rc == 0, f"go chot rc ma ca khong doi => ca do thu khac: {out}"


@ca
def n7_khong_che_sitecustomize_san(ws):
    """Python chi nap MOT `sitecustomize`; dung ten ay la CHE ban san co. Hook di bang
    `usercustomize` => ban san VAN chay. Dau vet phai la TEP, khong phai env: env ke thua tu
    cha nen ban dau viet bang env va dot bien SONG SOT — ca do khong do gi (codex, #247)."""
    (ws / "sc").mkdir(exist_ok=True)
    moc = ws / "sc" / "moc.txt"
    (ws / "sc" / "sitecustomize.py").write_text(f"open({str(moc)!r},'a').write('x')\n", "utf-8")
    rc, out = chay(ws, "--kiem-doc", "--buoc", "workflow-audit", them_env={
        "PYTHONPATH": str(ws / "sc"), "PYTHONDONTWRITEBYTECODE": "1"})
    n = len(moc.read_text()) if moc.exists() else 0
    assert n >= 2, f"sitecustomize san chi chay {n} lan (cha) => bi che o tien trinh DO: {out}"
    assert not list((ws / "scripts").rglob("__pycache__")), "da boc PYTHONDONTWRITEBYTECODE"


@ca
def n8_da_co_usercustomize_thi_khong_do_duoc(ws):
    """Khe `usercustomize` cung MOT-KHE-MOT-TEN, va tam_p chen dau PYTHONPATH nen ta LUON
    thang => doi ten khong cuu duoc, chi doi cho lo (vong 3, codex #247). Che ban san co thi
    phai KHONG DO DUOC chu khong duoc do tiep roi cong bo `doc_lap`."""
    (ws / "uc").mkdir(exist_ok=True)
    (ws / "uc" / "usercustomize.py").write_text("x = 1\n", "utf-8")
    for co in (["--kiem-doc"], ["--bang"]):
        rc, out = chay(ws, *co, "--buoc", "workflow-audit", them_env={"PYTHONPATH": str(ws / "uc")})
        assert rc != 0 and "KHONG DO DUOC" in out, f"che usercustomize san ma {co} xanh: {out}"
    thay(ws, CHECK, 'if any(d.startswith("#CHE") for d in dong):', "if False:")
    rc, out = chay(ws, "--kiem-doc", "--buoc", "workflow-audit",
                   them_env={"PYTHONPATH": str(ws / "uc")})
    assert rc == 0, f"go chot #CHE ma ca khong doi => ca do thu khac: {out}"


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
