#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
standardize_name.py — Chuẩn hóa & kiểm tra tên file/folder VBQPPL (v1.9.9.12)

Convention:
  Google Doc : <Loại>_<Số>-<Năm>-<CơQuan>_<Tên_rút_gọn>          (không extension)
  File gốc   : <Loại>_<Số>-<Năm>-<CơQuan>_<Tên_rút_gọn>.<ext>    (cùng tên + ext)
  Cat folder : <NN>_<Chủ_đề>                                      (NN = 2 chữ số cat)

Dùng:
  # Sinh tên chuẩn cho Google Doc
  python standardize_name.py --type Luat --number "113/2025/QH15" --name "Dân số"
      -> Luat_113-2025-QH15_Dan_so

  # Sinh tên file gốc (có extension)
  python standardize_name.py --type Luat --number "113/2025/QH15" --name "Dân số" --ext docx
      -> Luat_113-2025-QH15_Dan_so.docx

  # Kiểm tra một tên hiện có có đúng chuẩn không
  python standardize_name.py --check "D09_L113_Luat-Dan-so.docx" \
      --type Luat --number "113/2025/QH15" --name "Dân số"
      -> FAIL + tên đề xuất

  # Sinh tên folder cat
  python standardize_name.py --folder --cat 09 --name "Dân số"
      -> 09_Dan_so

  # JSON output (cho script khác gọi)
  python standardize_name.py --type Luat --number "113/2025/QH15" --name "Dân số" --json
"""
import argparse
import json
import re
import sys
import unicodedata

# Ánh xạ loại văn bản -> tiền tố chuẩn
TYPE_PREFIX = {
    "luat": "Luat",
    "bo luat": "BLuat",
    "bluat": "BLuat",
    "bo_luat": "BLuat",
    "nghi dinh": "ND",
    "nd": "ND",
    "thong tu": "TT",
    "tt": "TT",
    "nghi quyet": "NQ",
    "nq": "NQ",
    "quyet dinh": "QD",
    "qd": "QD",
    "phap lenh": "PL",
    "pl": "PL",
    "van ban hop nhat": "VBHN",
    "vbhn": "VBHN",
    "ket luan": "KL",
    "kl": "KL",
    "chi thi": "CT",
    "ct": "CT",
    "hien phap": "HP",
    "hp": "HP",
    "thong tu lien tich": "TTLT",
    "ttlt": "TTLT",
}


def strip_accents(s: str) -> str:
    """Bỏ dấu tiếng Việt, giữ chữ cái Latin cơ bản. Đ/đ -> D/d."""
    s = s.replace("Đ", "D").replace("đ", "d")
    nf = unicodedata.normalize("NFD", s)
    return "".join(c for c in nf if unicodedata.category(c) != "Mn")


def normalize_type(t: str) -> str:
    """Chuẩn hóa loại văn bản về tiền tố."""
    if not t:
        return ""
    key = strip_accents(t).strip().lower()
    if key in TYPE_PREFIX:
        return TYPE_PREFIX[key]
    # Đã là tiền tố hợp lệ?
    canon = {v.lower(): v for v in TYPE_PREFIX.values()}
    if key in canon:
        return canon[key]
    # Fallback: viết hoa chữ đầu, bỏ ký tự lạ
    return re.sub(r"[^A-Za-z]", "", t.title()) or "VB"


def normalize_number(num: str) -> str:
    """113/2025/QH15 -> 113-2025-QH15 ; 18/VBHN-VPQH -> 18-VBHN-VPQH."""
    if not num:
        return ""
    s = strip_accents(num).strip()
    # Thay mọi dấu / và khoảng trắng thừa bằng -
    s = re.sub(r"\s*/\s*", "-", s)
    s = re.sub(r"\s+", "-", s)
    # Gộp nhiều - liên tiếp
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s


def normalize_name(name: str) -> str:
    """Dân số -> Dan_so ; bỏ dấu, _ thay khoảng trắng, bỏ ký tự lạ.

    Bug E (log rà 71 luật): tên CHUẨN (GoogleDoc canonical) KHÔNG mang đuôi file. Nếu `name` lỡ kèm
    .doc/.docx/.pdf/.gdoc/.txt/.html (vd 'Bao_hiem_y_te.docx') → bỏ đuôi TRƯỚC khi chuẩn hoá, tránh
    rò '.docx'/'_docx' vào tên (5 luật trong log: 57/60/67-2024, 91-2015, 91-2025)."""
    if not name:
        return ""
    s = strip_accents(name).strip()
    s = re.sub(r"\.(docx?|pdf|gdoc|txt|html?)$", "", s, flags=re.I)   # bỏ đuôi file nếu lỡ kèm
    # Bỏ ký tự không phải chữ/số/khoảng trắng
    s = re.sub(r"[^\w\s]", " ", s, flags=re.ASCII)
    s = re.sub(r"\s+", "_", s.strip())
    s = re.sub(r"_{2,}", "_", s).strip("_")
    return s


def normalize_cat(cat: str) -> str:
    """9 -> 09 ; '09' -> '09' ; giữ QUARANTINE."""
    if not cat:
        return ""
    c = str(cat).strip()
    if c.upper() == "QUARANTINE":
        return "QUARANTINE"
    if c.isdigit():
        return f"{int(c):02d}"
    return c


def build_doc_name(vtype: str, number: str, name: str) -> str:
    """Sinh tên Google Doc chuẩn (không extension)."""
    parts = [normalize_type(vtype), normalize_number(number)]
    nm = normalize_name(name)
    base = "_".join(p for p in parts if p)
    if nm:
        base = f"{base}_{nm}"
    return base


def build_file_name(vtype: str, number: str, name: str, ext: str) -> str:
    """Sinh tên file gốc chuẩn (có extension)."""
    base = build_doc_name(vtype, number, name)
    ext = (ext or "").lstrip(".").lower()
    return f"{base}.{ext}" if ext else base


def build_folder_name(cat: str, name: str) -> str:
    """Sinh tên folder cat chuẩn."""
    return f"{normalize_cat(cat)}_{normalize_name(name)}"


def main():
    ap = argparse.ArgumentParser(description="Chuẩn hóa & kiểm tra tên VBQPPL")
    ap.add_argument("--type", default="", help="Loại văn bản (Luat, ND, TT, NQ, VBHN...)")
    ap.add_argument("--number", default="", help='Số hiệu, vd "113/2025/QH15"')
    ap.add_argument("--name", default="", help='Tên rút gọn / chủ đề, vd "Dân số"')
    ap.add_argument("--ext", default="", help="Extension file gốc (docx/pdf/doc) — bỏ trống = Google Doc")
    ap.add_argument("--folder", action="store_true", help="Sinh tên folder cat (cần --cat + --name)")
    ap.add_argument("--cat", default="", help="Mã cat 2 chữ số cho --folder")
    ap.add_argument("--check", default="", help="Tên hiện có để kiểm tra đúng chuẩn không")
    ap.add_argument("--json", action="store_true", help="Xuất JSON")
    args = ap.parse_args()

    # Chế độ folder
    if args.folder:
        expected = build_folder_name(args.cat, args.name)
        if args.check:
            ok = args.check.strip() == expected
            out = {"mode": "folder", "ok": ok, "current": args.check.strip(), "expected": expected}
        else:
            out = {"mode": "folder", "expected": expected}
        _emit(out, args.json)
        return

    # Chế độ file / doc
    if args.ext:
        expected = build_file_name(args.type, args.number, args.name, args.ext)
        mode = "file"
    else:
        expected = build_doc_name(args.type, args.number, args.name)
        mode = "doc"

    if args.check:
        cur = args.check.strip()
        # So sánh không phân biệt extension nếu check là doc
        ok = cur == expected
        out = {"mode": mode, "ok": ok, "current": cur, "expected": expected}
        if not ok:
            out["suggestion"] = expected
    else:
        out = {"mode": mode, "expected": expected}

    _emit(out, args.json)


def _emit(out: dict, as_json: bool):
    if as_json:
        print(json.dumps(out, ensure_ascii=False))
        return
    mode = out.get("mode")
    if "ok" in out:
        status = "PASS" if out["ok"] else "FAIL"
        print(f"[{status}] ({mode})")
        print(f"  current : {out.get('current','')}")
        print(f"  expected: {out.get('expected','')}")
        if not out["ok"]:
            print(f"  => đổi tên thành: {out.get('suggestion', out.get('expected',''))}")
        sys.exit(0 if out["ok"] else 1)
    else:
        print(out.get("expected", ""))


if __name__ == "__main__":
    main()


# ===== v2.0: quy tắc tên theo chuẩn đã chốt 12/06/2026 =====
import os as _os, json as _json
def _load_taxonomy():
    here = _os.path.dirname(_os.path.abspath(__file__))
    for p in (_os.path.join(here, "linhvuc_phapdien.json"),
              _os.path.join(here, "..", "references", "linhvuc_phapdien.json")):
        if _os.path.exists(p):
            return _json.load(open(p, encoding="utf-8"))
    return None

def build_vbhn_name(number: str, loai_goc: str, chude: str) -> str:
    """VBHN_09-VBHN-VPQH_Luat_Dau_tu — KHÔNG kèm chuỗi goc/sdbs (nằm ở trường goc)."""
    return f"VBHN_{normalize_number(number)}_{normalize_type(loai_goc)}_{normalize_name(chude)}"

def build_suadoi_name(number: str, targets: list) -> str:
    """1 đích -> Luat_<so>_sua_doi_<slug đích>; >=2 -> Luat_<so>_sua_doi_<N>_luat (cat 46)."""
    n = normalize_number(number)
    if len(targets) == 1:
        return f"Luat_{n}_sua_doi_{normalize_name(targets[0])}"
    return f"Luat_{n}_sua_doi_{len(targets)}_luat"

def folder_of(code: str) -> str:
    tax = _load_taxonomy()
    if tax and code in tax.get("chude", {}):
        return tax["chude"][code]["folder"]
    return normalize_cat(code)
