#!/usr/bin/env python3
"""Bộ test tự đứng cho `ops/kiem_nhan_hint.py` (packet #752, đặc tả `ops/specs/no-p3-cong-cu-ho-so-r4.md`).

Dựng cây tạm, gọi CLI trong tiến trình con. In ĐÚNG MỘT dòng chỉ gồm `đạt/tổng` (đơn vị: ca test) — mẫu
`^(\\d+)/(\\d+)$` mà #763 đăng ký; ca đỏ in dòng `DO <ca>: …`; ca không đo được trên nền này (chỉ Windows thiếu
symlink) in `BO QUA <ca>: …`, không tính đạt và bị trừ khỏi tổng. Chạy: python -B ops/kiem_nhan_hint_test.py
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


class BoQua(Exception):
    """Ca không đo được trên nền này: in riêng, KHÔNG tính đạt, trừ khỏi tổng (PR #918, F752-02)."""


def _cho_phep_bo_qua():
    """Chỉ Windows được tha thiếu symlink (thiếu quyền tạo); POSIX mà không tạo được là ĐỎ."""
    return os.name == "nt"


def ca_symlink_treo():
    def _khong_tao_duoc(ly_do):
        if _cho_phep_bo_qua():
            raise BoQua(ly_do)
        raise AssertionError(f"nền POSIX không tạo được symlink: {ly_do}")

    if not hasattr(os, "symlink"):
        _khong_tao_duoc("os.symlink vắng")
    goc = _cay({})
    try:
        try:
            os.symlink(goc / "khong-co", goc / "ops/reviews/treo-HINT.patch")
        except OSError as e:
            _khong_tao_duoc(f"{type(e).__name__}: {e}")
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


def _anh_chup(goc):
    """{đường dẫn: byte | None (= thư mục)} — so cả NỘI DUNG, không chỉ tập tên (PR #918, F752-01)."""
    return {p.relative_to(goc).as_posix(): (None if p.is_dir() else p.read_bytes()) for p in goc.rglob("*")}


def ca_glob_va_khong_ghi():
    goc = _cay({"ops/reviews/a/HINT.patch": f"{NHAN}\n", "ops/reviews/b/x-HINT.patch": "--- a\n+++ b\n"})
    try:
        truoc = _anh_chup(goc)
        rc, _, out, _ = _chay(goc, json_out=False)
        assert rc == 0, f"rc {rc}"
        assert sum(1 for d in out.splitlines() if GLOB in d.split()) == 1, "không có đúng một dòng mang token glob"
        assert _anh_chup(goc) == truoc, "công cụ đã ghi/sửa tệp (lượt đầu ra chữ)"
        _, kq, _, _ = _chay(goc)
        assert kq["phamvi_glob"] == GLOB, kq["phamvi_glob"]
        sau = _anh_chup(goc)
        assert sau == truoc, f"công cụ đã ghi/sửa tệp (lượt --json): {sorted(k for k in set(sau) | set(truoc) if sau.get(k) != truoc.get(k))}"
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


# Tự kiểm F752-02/F752-03: GIỮ NGUYÊN `_cho_phep_bo_qua` thật; chỉ thay `os` CỦA MODULE test bằng proxy cục bộ (đổi
# `os.name` toàn cục làm hỏng pathlib/tempfile) mang `name` giả và `symlink` hoặc ném lỗi, hoặc VẮNG hẳn.
_TU_KIEM = (
    "import importlib.util, os, sys\n"
    "s = importlib.util.spec_from_file_location('t', {tep!r}); m = importlib.util.module_from_spec(s)\n"
    "s.loader.exec_module(m)\n"
    "class _Os:\n"
    "    name = {ten!r}\n"
    "    def __getattr__(self, k):\n"
    "        if k == 'symlink':\n"
    "            if {che_do!r} == 'vang': raise AttributeError(k)\n"
    "            def _hong(*a, **kw): raise PermissionError('gia lap')\n"
    "            return _hong\n"
    "        return getattr(os, k)\n"
    "m.os = _Os()\n"
    "goi = []\n"
    "_cu = m._chay\n"
    "m._chay = lambda *a, **k: (goi.append(1), _cu(*a, **k))[1]\n"
    "m.CA = [m.ca_symlink_treo]\n"
    "rc = m.main()\n"
    "print('GOI_CONG_CU', len(goi))\n"
    "sys.exit(rc)\n"
)

# Kỳ vọng ĐỘC LẬP với mã đang thử (không tính từ `_cho_phep_bo_qua`): (nền, dạng hỏng) → (rc, dòng N/N, nhãn dòng ca).
_MA_TRAN_TU_KIEM = {
    ("nt", "loi"): (0, "0/0", "BO QUA ca_symlink_treo:"),
    ("nt", "vang"): (0, "0/0", "BO QUA ca_symlink_treo:"),
    ("posix", "loi"): (1, "0/1", "DO ca_symlink_treo:"),
    ("posix", "vang"): (1, "0/1", "DO ca_symlink_treo:"),
}


def ca_tu_kiem_bo_qua_symlink():
    """Khoá F752-02/F752-03: không tạo được symlink (ném lỗi HOẶC vắng API) thì ca KHÔNG được tính đạt và công cụ
    không được gọi — Windows bỏ qua tường minh, POSIX ĐỎ; chính sách nền đo bằng hàm THẬT trên proxy `os.name`."""
    for (ten, che_do), (rc_cho, dong_cho, nhan) in _MA_TRAN_TU_KIEM.items():
        ma = _TU_KIEM.format(tep=str(Path(__file__).resolve()), ten=ten, che_do=che_do)
        p = subprocess.run([sys.executable, "-B", "-c", ma], capture_output=True, text=True, encoding="utf-8", timeout=60)
        dong, nhan_ca = p.stdout.splitlines(), f"{ten}/{che_do}"
        assert p.returncode == rc_cho, f"{nhan_ca}: rc {p.returncode} (cần {rc_cho}); {p.stdout[-300:]}{p.stderr[-300:]}"
        assert dong_cho in dong and "1/1" not in dong, f"{nhan_ca}: {dong}"
        assert "GOI_CONG_CU 0" in dong, f"{nhan_ca}: công cụ bị gọi dù không tạo được symlink: {dong}"
        assert sum(1 for d in dong if d.startswith(nhan)) == 1, f"{nhan_ca}: thiếu dòng {nhan!r}: {dong}"


CA = [ca_b4_rang_l5, ca_symlink_treo, ca_doc_duoc_het_rc0, ca_glob_va_khong_ghi, ca_b7_root_sai,
      ca_tu_kiem_bo_qua_symlink]


def main():
    dat, bo_qua = 0, 0
    for ca in CA:
        try:
            ca()
            dat += 1
        except BoQua as e:  # không đo được trên nền này: in riêng, trừ khỏi tổng, KHÔNG tính đạt
            bo_qua += 1
            print(f"BO QUA {ca.__name__}: {e}")
        except Exception as e:  # ca đỏ vì bất kỳ lý do nào đều là đỏ; in tên ca và lý do
            print(f"DO {ca.__name__}: {type(e).__name__}: {e}")
    tong = len(CA) - bo_qua
    print(f"{dat}/{tong}")
    return 0 if dat == tong else 1


if __name__ == "__main__":
    sys.exit(main())
