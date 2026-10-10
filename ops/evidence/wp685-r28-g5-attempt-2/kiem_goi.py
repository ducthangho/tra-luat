"""wp685 r28 g5 attempt 2 — kiểm ĐỦ của gói bằng chứng (VERDICT lượt 1, ED-immutable-artifact-missing).
Dùng: python3 kiem_goi.py <thư mục gói> [--tu-kiem]
Đỏ khi: thiếu tệp BẮT BUỘC; SHA256SUMS.txt thiếu/thừa dòng so với tệp có thật trong gói (trừ chính nó); băm lệch;
`chot_tinh_r12.py` khác băm khối đặc tả. `sha256sum -c` không đủ vì manifest tự nhất quán vẫn có thể THIẾU tệp.
--tu-kiem: chép gói ra thư mục tạm, xoá `chot_tinh_r12.py` (giữ manifest đã có dòng của nó, rồi cả bản manifest đã bỏ
dòng ấy) — cả hai phải ĐỎ."""
import hashlib
import shutil
import sys
import tempfile
from pathlib import Path

BAT_BUOC = ["BAO_CAO.md", "chot_tinh_r12.py", "trich_chot_tinh.py", "bang_chung_aw_d.py", "phan_chung_d.py",
            "bang_chung_e.py", "san_windows.py", "sau_ca.sh", "chay_log.sh", "chay_b6.sh", "chay_b6_tuan_tu.sh", "chay_b1_b5.sh",
            "kiem_goi.py", "log/bang_D_python3.11.json", "log/bang_D_python3.12.json",
            "log/bang_E_python3.11.json", "log/bang_E_python3.12.json"]
BAT_BUOC_LOG = ["B1-B4_B8_cay", "B1-B4_B8_nen_testuv", "B2_chot_tinh", "B5_AW_D", "B5_E", "B5_D_phan_chung",
                "B6_suite_nen", "B6_suite_cay", "B6_dotbien_nen", "B6_dotbien_cay"]
CHOT_TINH_SHA = "add42b31beeaece6e3cf546d3915a153099bfe7a232995b0e1546bbd4a5735b6"


def kiem(goc):
    loi = []
    goc = Path(goc)
    can = list(BAT_BUOC) + [f"log/{b}_{py}.log" for b in BAT_BUOC_LOG for py in ("python3.11", "python3.12")]
    can += ["log/B4_san_windows.log", "log/B6_ruff_nen.log", "log/B6_ruff_cay.log", "log/B6_git_numstat_grep.log"]
    for c in can:
        if not (goc / c).is_file():
            loi.append(f"thieu tep bat buoc {c}")
    m = goc / "SHA256SUMS.txt"
    if not m.is_file():
        return loi + ["thieu SHA256SUMS.txt"]
    ghi = {}
    for d in m.read_text(encoding="utf-8").splitlines():
        h, _, p = d.partition("  ")
        if p in ghi:
            loi.append(f"manifest lap {p}")
        ghi[p] = h
    that = {str(p.relative_to(goc)) for p in goc.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt"}
    for p in sorted(that - set(ghi)):
        loi.append(f"tep khong co trong manifest {p}")
    for p in sorted(set(ghi) - that):
        loi.append(f"manifest co ma tep vang {p}")
    for p in sorted(that & set(ghi)):
        if hashlib.sha256((goc / p).read_bytes()).hexdigest() != ghi[p]:
            loi.append(f"bam lech {p}")
    ct = goc / "chot_tinh_r12.py"
    if ct.is_file() and hashlib.sha256(ct.read_bytes()).hexdigest() != CHOT_TINH_SHA:
        loi.append("chot_tinh_r12.py khac bam khoi dac ta")
    return loi


if __name__ == "__main__":
    goc = Path(sys.argv[1])
    loi = kiem(goc)
    for x in loi:
        print("DO:", x)
    print(f"KIEM GOI: {'DAT' if not loi else 'DO'} ({len(loi)} loi)")
    rc = 1 if loi else 0
    if "--tu-kiem" in sys.argv:
        with tempfile.TemporaryDirectory() as t:
            for ten, bo_dong in (("giu-dong-manifest", False), ("bo-dong-manifest", True)):
                b = Path(t) / ten
                shutil.copytree(goc, b)
                (b / "chot_tinh_r12.py").unlink()
                if bo_dong:
                    mf = b / "SHA256SUMS.txt"
                    mf.write_text("".join(d + "\n" for d in mf.read_text(encoding="utf-8").splitlines()
                                          if not d.endswith("  chot_tinh_r12.py")), encoding="utf-8")
                l2 = kiem(b)
                ok = any("chot_tinh_r12.py" in x for x in l2)
                print(f"TU KIEM [{ten}] xoa chot_tinh_r12.py: {'DO dung' if ok else 'KHONG DO'} {l2}")
                rc |= 0 if ok else 2
    sys.exit(rc)
