#!/usr/bin/env python3
"""Luật L-5 cho tệp HINT — packet #752, đặc tả đóng băng `ops/specs/no-p3-cong-cu-ho-so-r4.md` (sha256 a98d09e8…).

Mỗi tệp khớp `ops/reviews/**/*HINT.patch` xếp đúng MỘT loại:
  · `RONG` — nội dung sau `strip()` rỗng;
  · `CO_NHAN` — chứa NGUYÊN VĂN nhãn đầy đủ của PROTOCOL §8 (ràng buộc 1; dòng 651–652 @ `1d7e642`, nối bằng một dấu cách);
  · `KHONG_DU_DIEU_KIEN_PATCH_AS_HINT` — không chứa nhãn ấy (chỉ đo ràng buộc 1, không đo 2 và 3);
  · `KHONG_DOC_DUOC` — giải mã UTF-8 nghiêm lỗi hoặc mọi `OSError` (thư mục mang tên ấy, symlink treo, quyền).

Công cụ BÁO CÁO, không phải cổng, không ghi tệp nào. Mã thoát: 0 đọc được hết; 2 tham số sai (kể cả `--root` không
phải thư mục hoặc không chứa `ops/reviews` — 0 tệp không phải "sạch"); 3 có `KHONG_DOC_DUOC`.

Dùng: python ops/kiem_nhan_hint.py --root . [--json]
"""
import argparse
import json
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

THU_MUC = "ops/reviews"
PHAMVI_GLOB = "ops/reviews/**/*HINT.patch"
NHAN = "chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit"
LOAI = ("CO_NHAN", "KHONG_DU_DIEU_KIEN_PATCH_AS_HINT", "RONG", "KHONG_DOC_DUOC")


def xep_loai(tep):
    """Trả (loai, ly_do). Không để ngoại lệ đọc tệp thoát ra ngoài."""
    try:
        van_ban = tep.read_bytes().decode("utf-8")
    except UnicodeDecodeError as e:
        return "KHONG_DOC_DUOC", f"không phải UTF-8 (byte {e.start})"
    except OSError as e:
        return "KHONG_DOC_DUOC", f"không đọc được ({type(e).__name__})"
    if not van_ban.strip():
        return "RONG", "rỗng sau strip()"
    if NHAN in van_ban:
        return "CO_NHAN", "có nhãn patch-as-hint đầy đủ"
    return "KHONG_DU_DIEU_KIEN_PATCH_AS_HINT", "thiếu nhãn patch-as-hint đầy đủ (ràng buộc 1, PROTOCOL §8)"


def kiem(root):
    tep_list = []
    dem = {k: 0 for k in LOAI}
    for tep in sorted((root / THU_MUC).glob("**/*HINT.patch")):
        loai, ly_do = xep_loai(tep)
        dem[loai] += 1
        tep_list.append({"duong_dan": tep.relative_to(root).as_posix(), "loai": loai, "ly_do": ly_do})
    rc = 3 if dem["KHONG_DOC_DUOC"] else 0
    return rc, {"tep": tep_list, "dem": dem, "phamvi_glob": PHAMVI_GLOB}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Luật L-5 cho ops/reviews/**/*HINT.patch (báo cáo, không ghi).")
    ap.add_argument("--root", required=True, help="gốc kho")
    ap.add_argument("--json", action="store_true", help="in JSON")
    a = ap.parse_args(argv)
    root = Path(a.root)
    if not root.is_dir() or not (root / THU_MUC).is_dir():
        print(f"LỖI THAM SỐ: --root {a.root!r} không phải thư mục hoặc không chứa {THU_MUC}/", file=sys.stderr)
        return 2
    rc, kq = kiem(root)
    kq["rc"] = rc
    if a.json:
        print(json.dumps(kq, ensure_ascii=False, indent=1))
        return rc
    print(f"pham vi: {PHAMVI_GLOB}")
    for t in kq["tep"]:
        print(f"{t['loai']} {t['duong_dan']} — {t['ly_do']}")
    print("ĐẾM: " + " · ".join(f"{k} {v}" for k, v in kq["dem"].items()) + f" · tổng {len(kq['tep'])} · rc={rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
