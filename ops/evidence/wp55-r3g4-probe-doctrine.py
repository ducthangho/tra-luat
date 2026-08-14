#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đo DANH SÁCH ĐÓNG các lớp lách doctrine-scan — AC 18.

Chạy TRƯỚC khi vá. Mỗi lớp: một biến thể RENDER RA đúng cụm bị cấm, đo rc thật.
    rc=6  bắt được
    rc=0  LỌT
"""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(sys.argv[1]).resolve()

SACH = ("# Adapter demo\n\n**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §13.\n\n"
        "Dưới đây chỉ có cú pháp của nền.\n")

# Cụm đích, nguyên văn từ FORBIDDEN_DOCTRINE_PHRASES.
T_MERGED = "merged: PR đã vào nhánh đích"
T_EFFECT = "sửa đúng effective write set trên branch của generation"
T_NGUONG = "3 attempt/packet"
T_DISPAT = "dispatcher/reconciler"
T_PAUSED = "paused | blocked | cancelled | stale"
T_LOCAL = "local controller"
T_SAMEFL = "same_failure_limit"

# (id, lớp, mô tả, nội dung bơm vào adapter, kỳ vọng ĐÚNG: 6=phải bắt, 0=phải tha)
CA = [
    # --- nền: phải bắt, chứng minh phép đo có đáy -----------------------------
    ("A0", "nền", "ASCII nguyên văn", T_MERGED, 6),
    ("Z0", "nền", "adapter sạch", "chỉ trỏ về protocol", 0),

    # --- A. NFKC vs NFC --------------------------------------------------------
    ("A1", "NFKC", "hai chấm TOÀN RỘNG U+FF1A", "merged： PR đã vào nhánh đích", 6),
    ("A2", "NFKC", "chữ TOÀN RỘNG", "ｍｅｒｇｅｄ： PR đã vào nhánh đích", 6),
    ("A3", "NFKC", "chữ số TRÒN ③", "③ attempt/packet", 6),
    ("A4", "NFKC", "chữ số MŨ ³", "³ attempt/packet", 6),
    ("A5", "NFKC", "ligature ﬀ U+FB00", "sửa đúng eﬀective write set trên branch của generation", 6),
    ("A6", "NFKC", "solidus TOÀN RỘNG U+FF0F", "dispatcher／reconciler", 6),
    ("A7", "NFKC", "gạch dưới TOÀN RỘNG U+FF3F", "same＿failure＿limit", 6),
    ("A8", "NFKC", "vạch đứng TOÀN RỘNG U+FF5C", "paused ｜ blocked ｜ cancelled ｜ stale", 6),
    ("A9", "NFKC", "khoảng trắng KHÔNG NGẮT U+00A0", "local controller", 6),

    # --- B. ký tự định dạng Cf -------------------------------------------------
    ("B1", "Cf", "ZWSP U+200B", "mer​ged: PR đã vào nhánh đích", 6),
    ("B2", "Cf", "ZWNJ U+200C", "mer‌ged: PR đã vào nhánh đích", 6),
    ("B3", "Cf", "ZWJ U+200D", "mer‍ged: PR đã vào nhánh đích", 6),
    ("B4", "Cf", "WORD JOINER U+2060", "mer⁠ged: PR đã vào nhánh đích", 6),
    ("B5", "Cf", "SOFT HYPHEN U+00AD", "mer­ged: PR đã vào nhánh đích", 6),
    ("B6", "Cf", "BOM/ZWNBSP U+FEFF", "mer﻿ged: PR đã vào nhánh đích", 6),

    # --- C. HTML entity --------------------------------------------------------
    ("C1", "entity", "thập phân &#58;", "merged&#58; PR đã vào nhánh đích", 6),
    ("C2", "entity", "thập lục &#x3A;", "merged&#x3A; PR đã vào nhánh đích", 6),
    ("C3", "entity", "có tên &colon;", "merged&colon; PR đã vào nhánh đích", 6),
    ("C4", "entity", "thiếu ; — &#58", "merged&#58 PR đã vào nhánh đích", 6),
    ("C5", "entity", "LỒNG &amp;#58; — render ra &#58;, PHẢI THA", "merged&amp;#58; PR đã vào nhánh đích", 0),

    # --- D. đồng tự Cyrillic / Hy Lạp -----------------------------------------
    ("D1", "đồng tự", "Cyrillic е U+0435 trong merged", "mеrged: PR đã vào nhánh đích", 6),
    ("D2", "đồng tự", "Cyrillic о U+043E trong local controller", "lоcal controller", 6),
    ("D3", "đồng tự", "Hy Lạp ο U+03BF trong local controller", "lοcal controller", 6),
    ("D4", "đồng tự", "Cyrillic а U+0430 trong paused", "pаused | blocked | cancelled | stale", 6),

    # --- E. nháy cong ----------------------------------------------------------
    ("E1", "nháy", "nháy cong bao quanh cụm", "“merged: PR đã vào nhánh đích”", 6),
    ("E2", "nháy", "nháy đơn cong xen giữa", "mer’ged: PR đã vào nhánh đích", 6),

    # --- F. biến thể dash / mũi tên -------------------------------------------
    ("F1", "dash", "mũi tên DÀI U+27F6 thay →",
     "proposed ⟶ ready ⟶ leased ⟶ running ⟶ reviewing ⟶ accepted "
     "⟶ integrated ⟶ landed", 6),
    ("F2", "dash", "en-dash thay hyphen trong cụm có gạch", "same–failure–limit", 6),

    # --- G. cấu trúc Markdown / HTML ------------------------------------------
    ("G1", "markdown", "nhấn mạnh GIỮA TỪ mer*g*ed", "mer*g*ed: PR đã vào nhánh đích", 6),
    ("G2", "markdown", "tag HTML xen giữa <b>", "mer<b>ged</b>: PR đã vào nhánh đích", 6),
    ("G3", "markdown", "comment HTML xen giữa", "mer<!-- x -->ged: PR đã vào nhánh đích", 6),
    ("G4", "markdown", "link/anchor [merged](#a)", "[merged](#a): PR đã vào nhánh đích", 6),
    ("G5", "markdown", "ô BẢNG chứa nguyên cụm", "| merged: PR đã vào nhánh đích | x |", 6),
    ("G6", "markdown", "trong code fence", "```\nmerged: PR đã vào nhánh đích\n```", 6),
    ("G7", "markdown", "backslash escape merged\\:", "merged\\: PR đã vào nhánh đích", 6),
    ("G8", "markdown", "ngắt dòng GIỮA cụm (đã có ở r2)", "merged: PR đã vào\nnhánh đích", 6),

    # --- H. tổ hợp dấu / thứ tự chuẩn hoá -------------------------------------
    ("H1", "tổ hợp dấu", "đích viết bằng dấu TỔ HỢP U+0301",
     "merged: PR đã vào nhánh dɩch".replace("dɩ", "đí"), 6),
    ("H2", "tổ hợp dấu", "nhánh viết dạng phân rã NFD",
     "merged: PR đã vào nhánh đích", 6),
]


def do(noi_dung: str, tmp: Path, ten: str) -> int:
    r = tmp / ten
    (r / ".claude" / "skills" / "demo").mkdir(parents=True, exist_ok=True)
    (r / ".claude" / "skills" / "demo" / "SKILL.md").write_text(
        SACH + "\nGhi chú: " + noi_dung + "\n", encoding="utf-8", newline="\n")
    p = subprocess.run([sys.executable, str(SCRIPT), "doctrine-scan", "--root", str(r)],
                       capture_output=True)
    return p.returncode


def main() -> int:
    lot, oan, ok = [], [], 0
    with tempfile.TemporaryDirectory(prefix="probe_") as td:
        tmp = Path(td)
        print(f"{'id':<4} {'lớp':<12} {'rc':<4} {'đòi':<4} kết  mô tả")
        print("-" * 100)
        for cid, lop, mota, noi_dung, doi in CA:
            rc = do(noi_dung, tmp, cid)
            if rc == doi:
                ket, n = "ok  ", 1
                ok += 1
            elif doi == 6 and rc == 0:
                ket, n = "LỌT ", 0
                lot.append(cid)
            elif doi == 0 and rc == 6:
                ket, n = "OAN ", 0
                oan.append(cid)
            else:
                ket, n = "?!  ", 0
                lot.append(cid)
            print(f"{cid:<4} {lop:<12} {rc:<4} {doi:<4} {ket} {mota}")
    print("-" * 100)
    print(f"đạt {ok}/{len(CA)} · LỌT: {lot or 'không'} · BẮT OAN: {oan or 'không'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
