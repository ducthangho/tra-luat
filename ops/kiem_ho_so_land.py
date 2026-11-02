#!/usr/bin/env python3
"""Luật L-6 cho hồ sơ land — packet #752, đặc tả đóng băng `ops/specs/no-p3-cong-cu-ho-so-r4.md` (sha256 a98d09e8…).

Hồ sơ `ops/land/*-land-evidence.yaml` (không đệ quy; tên tệp là QUY ƯỚC) mang `landed` `is True` phải có ở MỨC GỐC:
  · `authorized_head_sha`: `str`, `re.fullmatch(r"[0-9a-f]{40}")` (không `re.match` + `$`: `$` khớp trước LF cuối);
  · `authorization_url`: `str`, `startswith("https://github.com/ducthangho/tra-luat/")` (không `in`) và chứa một trong
    `#issuecomment-` · `#pullrequestreview-` · `#discussion_r`.
`landed` đọc ở `trang_thai_packet.landed` khi có khoá `trang_thai_packet`, không thì ở mức gốc (kiểu a); `landed` khác `True`
(kể cả chuỗi `"true"`, số `1`) ⇒ không landed theo kiểu a.
wp981 r2 (spec `ops/specs/wp981-r2.md`, sha256 3d026415…) — kiểu b: khoá MỨC GỐC khớp `re.fullmatch(r"landed_\\d{8}")` là một
*khối landed*; giá trị không phải ánh xạ ⇒ `LOI`. Hồ sơ landed khi kiểu a `is True` HOẶC có khối mang `landed` `is True`;
không cái nào ⇒ `BO_QUA`. Mỗi khối `landed` `is True` phải có `quyet_dinh_chu_kho` là ánh xạ, `trang_thai == "da_duyet"` và
`comment` thoả đúng điều kiện `authorization_url` ở trên. Hồ sơ CHỈ landed theo kiểu b KHÔNG bị đòi `authorization_url`
mức gốc (thẩm quyền lấy từ `comment` của khối; `pr870`/`pr889` ghi `KHONG_AP_DUNG`); hồ sơ landed kiểu a giữ nguyên luật cũ,
kể cả khi có thêm khối. `authorized_head_sha` mức gốc luôn bắt buộc. Dòng báo cáo ghi landed đọc từ đâu.

Mã thoát, ưu tiên 2 > 3 > 1 > 0: 2 tham số sai (kể cả `--root` không phải thư mục / thiếu `ops/land`, kiểm TRƯỚC khi
quét); 3 không đọc được tệp/YAML (byte không UTF-8, thư mục mang tên hồ sơ, YAML hỏng, thẻ lạ), gốc hoặc
`trang_thai_packet` sai kiểu, thiếu PyYAML, hoặc một khoá miễn trừ trỏ tệp vắng; 1 có tệp `TRUOT` ngoài miễn trừ; 0 sạch.

Công cụ BÁO, không sửa hồ sơ nào. Dùng: python ops/kiem_ho_so_land.py --root . [--json]
"""
import argparse
import json
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

THU_MUC = "ops/land"
PHAMVI_GLOB = "ops/land/*-land-evidence.yaml"
TIEN_TO_URL = "https://github.com/ducthangho/tra-luat/"
MANH_URL = ("#issuecomment-", "#pullrequestreview-", "#discussion_r")
RE_SHA = re.compile(r"[0-9a-f]{40}")
RE_KHOI = re.compile(r"landed_\d{8}")  # wp981: khối landed kiểu b, chỉ ở mức gốc

# Hằng miễn trừ: ĐÚNG MỘT mục (mục tiêu 1). Hàm chính nhận danh sách làm tham số để test tiêm `{}`.
MIEN_TRU = {
    "ops/land/pr672-wp574-land-evidence.yaml": "hồ sơ của packet khác, ghi trước luật L-6; sửa ở packet riêng",
}


def _url_hop_le(url):
    return isinstance(url, str) and url.startswith(TIEN_TO_URL) and any(m in url for m in MANH_URL)


def _menh_de_truot(doc, doi_url_goc=True):
    """Trả danh sách tên khoá trượt (rỗng = đạt). Chỉ đọc MỨC GỐC; không ép kiểu, không tìm lồng.
    wp981: `doi_url_goc=False` CHỈ cho hồ sơ landed thuần kiểu b."""
    truot = []
    sha = doc.get("authorized_head_sha")
    if not (isinstance(sha, str) and RE_SHA.fullmatch(sha)):
        truot.append("authorized_head_sha")
    if doi_url_goc and not _url_hop_le(doc.get("authorization_url")):
        truot.append("authorization_url")
    return truot


def _khoi_truot(ten, kb):
    """wp981 M2: tên khoá trượt của một khối landed `landed is True`."""
    q = kb.get("quyet_dinh_chu_kho")
    if not isinstance(q, dict):
        return [f"{ten}.quyet_dinh_chu_kho"]
    truot = []
    tt = q.get("trang_thai")
    if not (isinstance(tt, str) and tt == "da_duyet"):
        truot.append(f"{ten}.quyet_dinh_chu_kho.trang_thai")
    if not _url_hop_le(q.get("comment")):
        truot.append(f"{ten}.quyet_dinh_chu_kho.comment")
    return truot


def _xet_mot_tep(tep, yaml):
    """Trả (trang_thai, ly_do, landed_la_true). trang_thai ∈ DAT · TRUOT · BO_QUA · LOI (LOI ⇒ rc 3)."""
    try:
        du_lieu = tep.read_bytes()
    except OSError as e:
        return "LOI", f"không đọc được tệp ({type(e).__name__})", False
    try:
        van_ban = du_lieu.decode("utf-8")
    except UnicodeDecodeError as e:
        return "LOI", f"không phải UTF-8 (byte {e.start})", False
    try:
        doc = yaml.safe_load(van_ban)
    except Exception as e:  # PR #918 (Codex P2): ngoài YAMLError, bộ dựng scalar còn ném ValueError
        # (`2026-13-01`), AttributeError (`!!timestamp 'x'`), RecursionError (lồng sâu) — cả lớp là "không đọc được"
        return "LOI", f"YAML không đọc được ({type(e).__name__})", False
    if not isinstance(doc, dict):
        return "LOI", f"gốc tài liệu không phải ánh xạ ({type(doc).__name__})", False
    if "trang_thai_packet" in doc:
        tp = doc["trang_thai_packet"]
        if not isinstance(tp, dict):
            return "LOI", f"trang_thai_packet không phải ánh xạ ({type(tp).__name__})", False
        landed, cho = tp.get("landed"), "trang_thai_packet.landed"
    else:
        landed, cho = doc.get("landed"), "landed (mức gốc)"
    khoi = sorted(k for k in doc if isinstance(k, str) and RE_KHOI.fullmatch(k))
    for k in khoi:
        if not isinstance(doc[k], dict):
            return "LOI", f"{k} không phải ánh xạ ({type(doc[k]).__name__})", False
    khoi_true = [k for k in khoi if doc[k].get("landed") is True]
    if landed is not True and not khoi_true:
        return "BO_QUA", f"{cho} = {landed!r}, không phải True; không khối landed_<ngày> nào landed True", False
    nguon = ([cho] if landed is True else []) + [f"{k}.landed" for k in khoi_true]
    truot = _menh_de_truot(doc, doi_url_goc=landed is True)
    for k in khoi_true:
        truot += _khoi_truot(k, doc[k])
    nguon_txt = "landed đọc từ " + ", ".join(nguon)
    if truot:
        return "TRUOT", f"trượt L-6 ở {', '.join(truot)} ({nguon_txt})", True
    tham_quyen = ["authorization_url"] if landed is True else []
    tham_quyen += [f"{k}.quyet_dinh_chu_kho" for k in khoi_true]
    return "DAT", f"đủ authorized_head_sha và {', '.join(tham_quyen)} ({nguon_txt})", True


def kiem(root, mien_tru):
    """Quét `ops/land/*-land-evidence.yaml` dưới `root`. Trả (rc, ket_qua) với rc ∈ 0 · 1 · 3."""
    try:
        import yaml  # nạp muộn để thiếu PyYAML ra rc 3, không phải traceback
    except ImportError:
        return 3, {"loi": "thiếu PyYAML", "tep": [], "n_dat": 0, "n_landed": 0, "n_mien_tru": 0,
                   "phamvi_glob": PHAMVI_GLOB}
    thu_muc = root / THU_MUC
    tep_list, co_loi, co_truot = [], False, False
    n_dat = n_landed = n_mien_tru = 0
    for tep in sorted(thu_muc.glob("*-land-evidence.yaml")):
        rel = tep.relative_to(root).as_posix()
        trang_thai, ly_do, la_true = _xet_mot_tep(tep, yaml)
        if la_true:
            n_landed += 1
        if trang_thai == "TRUOT" and rel in mien_tru:
            trang_thai, ly_do = "MIEN_TRU", f"{mien_tru[rel]} ({ly_do})"
            n_mien_tru += 1
        elif trang_thai == "TRUOT":
            co_truot = True
        elif trang_thai == "DAT":
            n_dat += 1
        elif trang_thai == "LOI":
            co_loi = True
        tep_list.append({"duong_dan": rel, "trang_thai": trang_thai, "ly_do": ly_do})
    vang = sorted(k for k in mien_tru if not (root / k).is_file())
    for k in vang:
        co_loi = True
        tep_list.append({"duong_dan": k, "trang_thai": "LOI", "ly_do": "miễn trừ trỏ tệp vắng"})
    rc = 3 if co_loi else (1 if co_truot else 0)
    return rc, {"tep": tep_list, "n_dat": n_dat, "n_landed": n_landed, "n_mien_tru": n_mien_tru,
                "phamvi_glob": PHAMVI_GLOB}


def main(argv=None, mien_tru=None):
    ap = argparse.ArgumentParser(description="Luật L-6 cho ops/land/*-land-evidence.yaml (báo cáo, không sửa).")
    ap.add_argument("--root", required=True, help="gốc kho")
    ap.add_argument("--json", action="store_true", help="in JSON")
    a = ap.parse_args(argv)
    root = Path(a.root)
    if not root.is_dir() or not (root / THU_MUC).is_dir():
        print(f"LỖI THAM SỐ: --root {a.root!r} không phải thư mục hoặc không chứa {THU_MUC}/", file=sys.stderr)
        return 2
    rc, kq = kiem(root, MIEN_TRU if mien_tru is None else mien_tru)
    kq["rc"] = rc
    if a.json:
        print(json.dumps(kq, ensure_ascii=False, indent=1))
        return rc
    if "loi" in kq:
        print(f"LOI {kq['loi']}")
    print(f"pham vi: {PHAMVI_GLOB} (không đệ quy)")
    for t in kq["tep"]:
        print(f"{t['trang_thai']} {t['duong_dan']} — {t['ly_do']}")
    print(f"TỔNG: {kq['n_dat']}/{kq['n_landed']} hồ sơ landed True đạt · {kq['n_mien_tru']} miễn trừ · rc={rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
