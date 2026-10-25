#!/usr/bin/env python3
"""Bộ test tự đứng cho `ops/kiem_nhan_hint.py` (packet #752, đặc tả `ops/specs/no-p3-cong-cu-ho-so-r4.md`).

Dựng cây tạm, gọi CLI trong tiến trình con. In ĐÚNG MỘT dòng chỉ gồm `đạt/tổng` (đơn vị: ca test) — mẫu
`^(\\d+)/(\\d+)$` mà #763 đăng ký; ca đỏ in dòng `DO <ca>: …`. Chạy: python -B ops/kiem_nhan_hint_test.py
Phủ nghiệm thu B4 · B5 (glob, không ghi tệp) trên cây tạm · B7.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

TOOL = Path(__file__).resolve().parent / "kiem_nhan_hint.py"
GLOB = "ops/reviews/**/*HINT.patch"
NHAN = "chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit"


def _chay(root, json_out=True):
    p = subprocess.run([sys.executable, "-B", str(TOOL), "--root", str(root)] + (["--json"] if json_out else []),
                       capture_output=True, text=True, encoding="utf-8", timeout=120)
    kq = json.loads(p.stdout) if json_out and p.returncode != 2 else None
    return p.returncode, kq, p.stdout, p.stderr


def _cay(tep):
    """{đường dẫn tương đối: str | bytes | None (= thư mục)}. Luôn có ops/reviews/."""
    goc = Path(tempfile.mkdtemp(prefix="kiem-nhan-hint-"))
    (goc / "ops/reviews").mkdir(parents=True)
    for rel, nd in tep.items():
        p = goc / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if nd is None:
            p.mkdir()
        elif isinstance(nd, bytes):
            p.write_bytes(nd)
        else:
            p.write_text(nd, encoding="utf-8")
    return goc


# (đường dẫn, nội dung, loại cần)
B4 = [
    ("ops/reviews/a/HINT.patch", f"# {NHAN}\n--- a\n+++ b\n", "CO_NHAN"),
    ("ops/reviews/x-HINT.patch", f"{NHAN}\n", "CO_NHAN"),
    ("ops/reviews/b/x-HINT.patch", "# chưa chạy, xem lại sau\n--- a\n+++ b\n", "KHONG_DU_DIEU_KIEN_PATCH_AS_HINT"),
    ("ops/reviews/c/HINT.patch", "# " + NHAN[: -len(" commit")] + "\n--- a\n", "KHONG_DU_DIEU_KIEN_PATCH_AS_HINT"),
    ("ops/reviews/d/HINT.patch", "", "RONG"),
    ("ops/reviews/e/HINT.patch", "\n\n", "RONG"),
    ("ops/reviews/f/HINT.patch", b"# \xff\xfe\n", "KHONG_DOC_DUOC"),
    ("ops/reviews/g/x-HINT.patch", None, "KHONG_DOC_DUOC"),
]


def ca_b4_rang_l5():
    goc = _cay({d: nd for d, nd, _ in B4})
    try:
        rc, kq, _, err = _chay(goc)
        assert rc == 3, f"rc {rc} (cần 3 vì có KHONG_DOC_DUOC); {err[-300:]}"
        assert "Traceback" not in err, "traceback"
        theo = {t["duong_dan"]: t["loai"] for t in kq["tep"]}
        assert len(theo) == len(B4), f"{len(theo)} tệp (cần {len(B4)}): {sorted(theo)}"
        for d, _, cho in B4:
            assert theo[d] == cho, f"{d}: {theo[d]} (cần {cho})"
        dem_cho = {k: sum(1 for *_, c in B4 if c == k) for k in kq["dem"]}
        assert kq["dem"] == dem_cho, (kq["dem"], dem_cho)
    finally:
        shutil.rmtree(goc)


def ca_symlink_treo():
    if not hasattr(os, "symlink"):
        return
    goc = _cay({})
    try:
        try:
            os.symlink(goc / "khong-co", goc / "ops/reviews/treo-HINT.patch")
        except OSError:
            return  # nền không cho tạo symlink (Windows thiếu quyền): ca không áp dụng
        rc, kq, _, _ = _chay(goc)
        assert rc == 3 and [t["loai"] for t in kq["tep"]] == ["KHONG_DOC_DUOC"], (rc, kq and kq["tep"])
    finally:
        shutil.rmtree(goc)


def ca_doc_duoc_het_rc0():
    goc = _cay({d: nd for d, nd, cho in B4 if cho != "KHONG_DOC_DUOC"})
    try:
        rc, kq, _, _ = _chay(goc)
        assert rc == 0, f"rc {rc} (cần 0 — công cụ báo cáo, không phải cổng)"
        assert kq["dem"]["KHONG_DOC_DUOC"] == 0 and len(kq["tep"]) == 6, kq["dem"]
    finally:
        shutil.rmtree(goc)


def ca_glob_va_khong_ghi():
    goc = _cay({"ops/reviews/a/HINT.patch": f"{NHAN}\n"})
    try:
        truoc = sorted(p.relative_to(goc).as_posix() for p in goc.rglob("*"))
        rc, _, out, _ = _chay(goc, json_out=False)
        assert rc == 0, f"rc {rc}"
        assert sum(1 for d in out.splitlines() if GLOB in d.split()) == 1, "không có đúng một dòng mang token glob"
        _, kq, _, _ = _chay(goc)
        assert kq["phamvi_glob"] == GLOB, kq["phamvi_glob"]
        sau = sorted(p.relative_to(goc).as_posix() for p in goc.rglob("*"))
        assert truoc == sau, f"công cụ đã ghi tệp: {sorted(set(sau) - set(truoc))}"
    finally:
        shutil.rmtree(goc)


def ca_b7_root_sai():
    tam = Path(tempfile.mkdtemp(prefix="kiem-nhan-hint-root-"))
    try:
        tep = tam / "mot-tep"
        tep.write_text("x\n", encoding="utf-8")
        rong = tam / "rong"
        rong.mkdir()
        for ten, r in (("khong-ton-tai", tam / "khong-co"), ("tep", tep), ("rong", rong)):
            for js in (False, True):
                p = subprocess.run([sys.executable, "-B", str(TOOL), "--root", str(r)] + (["--json"] if js else []),
                                   capture_output=True, text=True, encoding="utf-8", timeout=60)
                assert p.returncode == 2, f"{ten}: rc {p.returncode} (cần 2)"
                assert "ĐẾM" not in p.stdout and '"dem"' not in p.stdout, f"{ten}: in dòng đếm"
    finally:
        shutil.rmtree(tam)


CA = [ca_b4_rang_l5, ca_symlink_treo, ca_doc_duoc_het_rc0, ca_glob_va_khong_ghi, ca_b7_root_sai]


def main():
    dat = 0
    for ca in CA:
        try:
            ca()
            dat += 1
        except Exception as e:  # ca đỏ vì bất kỳ lý do nào đều là đỏ; in tên ca và lý do
            print(f"DO {ca.__name__}: {type(e).__name__}: {e}")
    print(f"{dat}/{len(CA)}")
    return 0 if dat == len(CA) else 1


if __name__ == "__main__":
    sys.exit(main())
