# -*- coding: utf-8 -*-
"""ci_phamvi.py — BANG PHU THUOC giua buoc gate va nhom duong dan, cong tu dung lai bang.

Kho chua co cho nao ghi buoc CI nao phu thuoc thu muc nao, nen moi cau "bo buoc nay co an toan
khong" deu tra loi bang phong doan. Tep nay ghi bang ay va tu kiem no; no KHONG doi mot dong
hanh vi CI nao. Phep do YEU (them mot dong chu thich roi xem dau ra co doi khong) DA SAI BA
LAN — no chi bat duoc buoc bam noi dung, con `tl selftest`/`doc-claims-check` deu bao "an toan
de bo" trong khi doc `docs/` 69 tep. Nen chi dung hai phep do MANH: ve DOC = audit hook
(`sys.addaudithook`) nap qua PYTHONPATH nen MOI tien trinh con ke thua; ve BAM = DAN XUAT tu
`_RELEASE_EXCLUDE_*` — tep khong vao goi thi khong doi bam goi. BA TRANG THAI, khong phai hai:
phep do THAT BAI trong y het phep do SACH neu chi nhin rc, nen `khong_do_duoc` khong gop vao
`doc_lap`. Bang chi la LOI KHAI; su that o MA va o PHEP DO, lech thi BANG sai chu khong phai ma.
Dung:  --kiem-bam | --kiem-doc [--buoc X] | --bang [--buoc X]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]

PHU_THUOC, DOC_LAP, KHONG_DO_DUOC = "phu_thuoc", "doc_lap", "khong_do_duoc"

# Ten nhom la thu duoc IN RA khi cong do, nen phai tra cuu duoc, khong phai mot chi so.
NHOM = {"ops": "ops", "docs": "docs", "CLAUDE.md": "CLAUDE.md",
        ".claude": ".claude", ".githooks": ".githooks", ".github": ".github"}

# Ve DOC — KHAI tap nhom moi buoc doc; `kiem_doc` dung lai bang audit hook, lech => DO. So do
# 2026-08-22 tren master 195a478d: tl-selftest 440 tep (docs 69 · CLAUDE.md 1 · .claude 1 ·
# .github 1) · doc-claims-check 243 (docs 69 · CLAUDE.md 1) · workflow-audit 67 · golden-test 107.
BUOC = {
    "tl-selftest": {"lenh": ["scripts/tl.py", "--selftest"],
                    "doc": {"docs", "CLAUDE.md", ".claude", ".github"}},
    "doc-claims-check": {"lenh": ["scripts/tl.py", "doc-claims-check", "--strict", "--json"],
                         "doc": {"docs", "CLAUDE.md"}},
    "workflow-audit": {"lenh": ["scripts/tl.py", "workflow-audit", "--strict", "--json"],
                       "doc": set()},
    "golden-test": {"lenh": ["scripts/tl.py", "golden-test", "--json"], "doc": set()},
}

# Ve BAM — KHAI nhom nao nam NGOAI goi. `kiem_bam` dan xuat su that tu ma roi so.
NGOAI_GOI = {"ops", "docs", "CLAUDE.md", ".claude", ".githooks", ".github"}
BUOC_BAM = ("release-check", "release-verify", "release-bundle")

# `tl selftest` co ca phu thuoc nen => tap doc tren windows-latest CHUA DO; khai thay vi ngam.
NEN_DA_DO = "linux"

_NGUON_HOOK = """import os, sys
_so = os.environ.get("CI_PHAMVI_SO")
if _so:
    _fd = os.open(_so, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    os.write(_fd, b"#HOOK-OK\\n")
    def _h(su, args):
        if su in ("open", "os.open", "io.open") and args:
            p = args[0]
            p = p.decode("utf-8", "replace") if isinstance(p, bytes) else p
            if isinstance(p, str):
                try:
                    os.write(_fd, (p + "\\n").encode("utf-8", "replace"))
                except Exception:
                    pass
    sys.addaudithook(_h)
"""


def loai_tru_tu_ma(goc: Path) -> set:
    """DAN XUAT tap nhom nam ngoai goi tu `_RELEASE_EXCLUDE_*`. Khong ke tay."""
    duong = str(goc / "scripts")
    if duong not in sys.path:
        sys.path.insert(0, duong)
    for ten in [m for m in sys.modules if m == "tl_core" or m.startswith("tl_core.")]:
        del sys.modules[ten]
    from tl_core import release as R
    thu_muc, ten_tep = set(R._RELEASE_EXCLUDE_DIRS), set(R._RELEASE_EXCLUDE_NAMES_ANYWHERE)
    return {n for n, d in NHOM.items()
            if Path(d).parts[0] in thu_muc or Path(d).name in ten_tep}


def do_tap_doc(buoc: str, goc: Path):
    """Chay buoc THAT duoi audit hook. Tra TAP nhom doc duoc, hoac CHUOI ly do = KHONG DO DUOC."""
    with tempfile.TemporaryDirectory() as tam:
        tam_p = Path(tam)
        (tam_p / "sitecustomize.py").write_text(_NGUON_HOOK, encoding="utf-8")
        (so := tam_p / "so.txt").touch()
        env = dict(os.environ)
        env["CI_PHAMVI_SO"] = str(so)
        env["PYTHONPATH"] = os.pathsep.join(x for x in (str(tam_p), env.get("PYTHONPATH")) if x)
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        r = subprocess.run([sys.executable] + BUOC[buoc]["lenh"], cwd=str(goc), env=env,
                           capture_output=True, text=True)
        dong = so.read_text(encoding="utf-8", errors="replace").splitlines()
    if "#HOOK-OK" not in dong:
        return "audit hook khong cai duoc"
    if r.returncode != 0:
        # Lenh dich HONG sau khi hook nap => tap doc chi la MOT PHAN; voi buoc khai tap
        # rong thi phan ay cung rong, nen no GIA DANG mot phep do sach (codex bat, #247).
        return f"lenh dich thoat {r.returncode}"
    ra = set()
    for d in dong:
        if d.startswith("#"):
            continue
        p = Path(d)
        if not p.is_absolute():
            p = goc / p
        try:
            td = str(p.resolve().relative_to(goc))
        except (ValueError, OSError):
            continue
        ra |= {n for n, dn in NHOM.items() if td == dn or td.startswith(dn + "/")}
    return ra


def phan_loai(nhom: str, buoc: str, doc_do_duoc, ngoai_goi) -> str:
    """Diem quyet dinh DUY NHAT cua bang. Ba trang thai, khong phai hai."""
    if buoc in BUOC_BAM:
        return DOC_LAP if nhom in ngoai_goi else PHU_THUOC
    if not isinstance(doc_do_duoc, set):
        return KHONG_DO_DUOC
    return PHU_THUOC if nhom in doc_do_duoc else DOC_LAP


def kiem_nhom_ton_tai(goc: Path) -> list:
    """N4 — nhom tro vao thu khong co tren dia la con tro chet (cung luat protocol §20)."""
    return [f"nhom bia: {n} -> {d} khong co tren dia"
            for n, d in sorted(NHOM.items()) if not (goc / d).exists()]


def kiem_bam(goc: Path) -> list:
    """M2 — bang vs MA. Doi chieu hai chieu: khai thua va khai thieu deu la sai lech."""
    dan_xuat = loai_tru_tu_ma(goc)
    return ([f"bang khai NGOAI GOI nhung ma KHONG loai tru: {n}"
             for n in sorted(NGOAI_GOI - dan_xuat)]
            + [f"ma loai tru nhung bang KHONG khai NGOAI GOI: {n}"
               for n in sorted(dan_xuat - NGOAI_GOI)])


def kiem_doc(buoc: str, goc: Path) -> list:
    """M3 — bang vs PHEP DO. Thong diep phai NEU TEN nhom, khong chi dem so."""
    do_duoc = do_tap_doc(buoc, goc)
    if not isinstance(do_duoc, set):
        return [f"KHONG DO DUOC: buoc {buoc} — {do_duoc}"]
    khai = set(BUOC[buoc]["doc"])
    return ([f"buoc {buoc} DOC nhom chua khai: {n}" for n in sorted(do_duoc - khai)]
            + [f"buoc {buoc} khai DOC nhom nhung khong doc: {n}"
               for n in sorted(khai - do_duoc)])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="bang phu thuoc buoc CI <-> nhom duong dan")
    ap.add_argument("--kiem-bam", action="store_true")
    ap.add_argument("--kiem-doc", action="store_true")
    ap.add_argument("--bang", action="store_true")
    ap.add_argument("--buoc", choices=sorted(BUOC))
    ap.add_argument("--goc", default=str(GOC))
    a = ap.parse_args(argv)
    if not (a.kiem_bam or a.kiem_doc or a.bang):
        ap.error("chon it nhat mot trong --kiem-bam / --kiem-doc / --bang")
    goc = Path(a.goc).resolve()
    chon = [a.buoc] if a.buoc else sorted(BUOC)

    loi = kiem_nhom_ton_tai(goc)
    if a.kiem_bam:
        loi += kiem_bam(goc)
    if a.kiem_doc:
        loi += [d for b in chon for d in kiem_doc(b, goc)]
    if a.bang:
        ngoai = loai_tru_tu_ma(goc)
        bang = {"nen_da_do": NEN_DA_DO, "buoc": {}}
        for b in chon + list(BUOC_BAM):
            do_duoc = None if b in BUOC_BAM else do_tap_doc(b, goc)
            bang["buoc"][b] = {n: phan_loai(n, b, do_duoc, ngoai) for n in sorted(NHOM)}
        print(json.dumps(bang, ensure_ascii=True, indent=2, sort_keys=True))
        loi += [f"buoc {b} nhom {n}: KHONG DO DUOC" for b, v in bang["buoc"].items()
                for n, t in sorted(v.items()) if t == KHONG_DO_DUOC]

    for d in loi:
        print("DO: " + d)
    if loi:
        print(f"DO: {len(loi)} sai lech")
        return 1
    print("OK ci_phamvi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
