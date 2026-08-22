# -*- coding: utf-8 -*-
"""ci_phamvi.py — BANG PHU THUOC ve BAM: buoc bam goi <-> nhom duong dan.

Kho chua co cho nao ghi buoc CI nao phu thuoc thu muc nao, nen moi cau "bo buoc nay co an
toan khong" deu tra loi bang phong doan. Tep nay ghi NUA BANG do va tu kiem no; no KHONG
doi mot dong hanh vi CI nao.

Su that KHONG do bang cach ke tay ma DAN XUAT tu `_RELEASE_EXCLUDE_*` trong
`scripts/tl_core/release.py`: tep khong vao goi thi khong doi bam goi, nen buoc bam doc lap
voi no THEO KIEN TRUC. Bang duoi day chi la LOI KHAI; lech thi BANG sai chu khong phai ma.

VE DOC (buoc chay HANH VI nhu `tl selftest`, `doc-claims-check` doc thu muc nao) CO Y VANG
MAT o day — xem "## Vi sao thieu ve DOC" cuoi tep. Dung suy tu su vang mat ay rang cac buoc
ay doc lap voi thu gi: BANG NAY KHONG NOI GI VE CHUNG.

BA TRANG THAI, khong phai hai: dan xuat that bai (khong nap duoc `tl_core.release`) trong y
het mot phep do sach neu chi nhin rc, nen no la `khong_do_duoc` va lam cong DO.

Dung:  --kiem-bam | --bang
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]

PHU_THUOC, DOC_LAP, KHONG_DO_DUOC = "phu_thuoc", "doc_lap", "khong_do_duoc"

# Ten nhom la thu duoc IN RA khi cong do, nen phai tra cuu duoc, khong phai mot chi so.
NHOM = {"ops": "ops", "docs": "docs", "CLAUDE.md": "CLAUDE.md",
        ".claude": ".claude", ".githooks": ".githooks", ".github": ".github"}

# KHAI nhom nao nam NGOAI goi phat hanh. `kiem_bam` dan xuat su that tu ma roi doi chieu.
NGOAI_GOI = {"ops", "docs", "CLAUDE.md", ".claude", ".githooks", ".github"}
BUOC_BAM = ("release-check", "release-verify", "release-bundle")


def loai_tru_tu_ma(goc: Path):
    """DAN XUAT tap nhom nam ngoai goi bang cach HOI CHINH `_build_release_manifest`.
    Tra None = KHONG DO DUOC."""
    duong = str(goc / "scripts")
    if duong not in sys.path:
        sys.path.insert(0, duong)
    for ten in [m for m in sys.modules if m == "tl_core" or m.startswith("tl_core.")]:
        del sys.modules[ten]
    try:
        from tl_core import release as R
        trong_goi = {f["path"] for f in R._build_release_manifest(goc)["files"]}
    except Exception:
        return None          # nap/dung hong => KHONG duoc im lang coi nhu "khong loai tru gi"
    # KHONG chep lai luat loai tru nua. Ba finding lien tiep tren tep nay deu cung mot hinh
    # dang: ban chep cua ta troi lech khoi `_release_should_include` — bo qua cay con cua mot
    # THU MUC ten `CLAUDE.md` (#251), roi BAT OAN mot symlink (cung #251). Va ke ca chep dung
    # vi tu van chua du: symlink-toi-thu-muc bi loai la nho `rglob` KHONG di xuyen symlink,
    # tuc do PHEP DUYET quyet dinh chu khong rieng vi tu. Nen hoi thang thu that: nhom nam
    # ngoai goi khi KHONG duong dan nao tai/duoi no lot vao manifest.
    return {n for n, d in NHOM.items()
            if not any(x == d or x.startswith(d + "/") for x in trong_goi)}


def phan_loai(nhom: str, ngoai_goi) -> str:
    """Diem quyet dinh DUY NHAT cua bang. Ba trang thai, khong phai hai."""
    if ngoai_goi is None:
        return KHONG_DO_DUOC
    return DOC_LAP if nhom in ngoai_goi else PHU_THUOC


def kiem_nhom_ton_tai(goc: Path) -> list:
    """Nhom tro vao thu khong co tren dia la con tro chet (cung luat protocol §20)."""
    return [f"nhom bia: {n} -> {d} khong co tren dia"
            for n, d in sorted(NHOM.items()) if not (goc / d).exists()]


def kiem_bam(goc: Path) -> list:
    """Bang vs MA. Doi chieu HAI CHIEU: khai thua va khai thieu deu la sai lech."""
    dan_xuat = loai_tru_tu_ma(goc)
    if dan_xuat is None:
        return ["KHONG DO DUOC: khong nap duoc tl_core.release de dan xuat _RELEASE_EXCLUDE_*"]
    return ([f"bang khai NGOAI GOI nhung ma KHONG loai tru: {n}"
             for n in sorted(NGOAI_GOI - dan_xuat)]
            + [f"ma loai tru nhung bang KHONG khai NGOAI GOI: {n}"
               for n in sorted(dan_xuat - NGOAI_GOI)])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="bang phu thuoc buoc BAM <-> nhom duong dan")
    for c in ("--kiem-bam", "--bang"):
        ap.add_argument(c, action="store_true")
    a = ap.parse_args(argv)
    if not (a.kiem_bam or a.bang):
        ap.error("chon it nhat mot trong --kiem-bam / --bang")

    loi = kiem_nhom_ton_tai(GOC)
    if a.kiem_bam:
        loi += kiem_bam(GOC)
    if a.bang:
        ngoai = loai_tru_tu_ma(GOC)
        bang = {"ve": "bam", "ve_doc": "khong_co_trong_slice_nay",
                "buoc": {b: {n: phan_loai(n, ngoai) for n in sorted(NHOM)} for b in BUOC_BAM}}
        print(json.dumps(bang, ensure_ascii=True, indent=2, sort_keys=True))
        loi += [f"buoc {b} nhom {n}: KHONG DO DUOC" for b, v in bang["buoc"].items()
                for n, t in sorted(v.items()) if t == KHONG_DO_DUOC]

    for d in loi:
        print("DO: " + d)
    if loi:
        print(f"DO: {len(loi)} sai lech")
        return 1
    print("OK ci_phamvi (ve BAM)")
    return 0


# ## Vi sao thieu ve DOC
#
# Ve DOC tung duoc do bang audit hook (`sys.addaudithook`) nap qua PYTHONPATH. Bon vong
# review chung minh co che ay KHONG the trung thuc, va moi ban va chi lo ra tang ke tiep:
#   1. lenh dich hong sau khi hook nap => tap doc MOT PHAN, gia dang phep do sach
#   2. hook CHE `sitecustomize` san co  3. doi sang `usercustomize` van CHE ban san co
#   4. va nang nhat: `sitecustomize` cung `.pth` thuc thi TRUOC `usercustomize`, nen doc
#      cua chung VO HINH — bao toan hook khong co nghia la DO duoc no.
# Do duoc tren PR #247: mot `sitecustomize` doc `ops/` van cho `"ops": "doc_lap"`, rc=0.
#
# Thu tu khoi dong Python la co dinh (`.pth` -> `sitecustomize` -> `usercustomize` -> ma
# nguoi dung) nen hook o khe cuoi KHONG bao gio thay duoc thu chay truoc no. Day la gioi han
# KIEN TRUC, khong phai loi vá duoc. Ve DOC vi vay o lai Remediation Slice, voi hai duong da
# biet: cai tracer TRUOC `site` init (`.pth` trong user-site tam), hoac bo han startup-hook
# va de `tl selftest` TU KHAI tap doc tung ca (dac ta da carve-out thanh packet rieng).
#
# CANH BAO cho nguoi doc so B2 cua dac ta: cac so 440/243/67/107 do bang DUNG co che nay,
# nen chung dung o moi truong khoi dong TRAN — khong phai hang so vo dieu kien.
if __name__ == "__main__":
    sys.exit(main())
