#!/usr/bin/env python3
"""Bộ đo nghiệm thu của ops/specs/wp1555-r1.md (N1–N5). Chạy: python ops/specs/wp1555-r1-do.py [--root .]

Chỉ đọc. In một dòng ĐẠT/ĐỎ cho mỗi tiêu chí, thoát 0 khi mọi tiêu chí ĐẠT, 1 khi có tiêu chí ĐỎ.
Khớp trên văn bản đã nối dòng trong phạm vi TỪNG đoạn (L6 b): khoảng trắng liên tiếp, kể cả xuống dòng
trong cùng đoạn, gộp thành một dấu cách; không nối qua dòng trống.
"""
import argparse
import re
import sys
from pathlib import Path

ADR = "docs/adr/0060-dieu-kien-merge-va-moc-ready.md"
PROTO = "docs/PROTOCOL_DA_PHIEN.md"
SKILL = ".claude/skills/land-packets/SKILL.md"

# Câu MỚI (vế dương) và câu CŨ (vế âm), từng vị trí.
N1_MOI = ("**1 cổng** (packet C, #1106): `.claude/dev/packet_loop.py kiem-merge` (điều kiện bỏ draft/merge K0–K7 và K2b) "
          "và `kiem-dong-wp` (đóng WP D1–D4 và D2b), không đọc state. K2b (#1462) là làn G5, chỉ chạy khi K2 không đỏ; "
          "D2b (#1236 đợt C) đối chiếu lời khai `gate_output` dương của biên bản M8 với tệp đánh giá tại `oid` trên remote, "
          "chỉ chạy khi D1 đạt và `gate_output` là `passed` hoặc `owner_waived`.")
N1_CU = "(điều kiện bỏ draft/merge K0–K7) và `kiem-dong-wp` (đóng WP D1–D4), không đọc state."
N2_MOI = "`packet_loop.py` `kiem-merge` (K0–K7 và K2b), `kiem-dong-wp` (D1–D4 và D2b)"
N2_CU = "`packet_loop.py` `kiem-merge` (K0–K7), `kiem-dong-wp` (D1–D4)"
N3_MOI = "review/audit, K0–K7 và K2b, full Linux M9 hoặc target canary sau land."
N3_CU = "review/audit, K0–K7, full Linux M9 hoặc target canary sau land."
N4_MOI = ("chạy `python3 .claude/dev/packet_loop.py kiem-merge …` (K0–K7 và K2b; K7 = M9", "`kiem-dong-wp --bien-ban <YAML M8> --lease <lease cuối>` (D1–D4 và D2b).")
N4_CU = ("chạy `python3 .claude/dev/packet_loop.py kiem-merge …` (K0–K7; K7 = M9", "`kiem-dong-wp --bien-ban <YAML M8> --lease <lease cuối>` (D1–D4).")

# N5: mọi lời khai dải chốt, cả dạng gạch nối, gạch ngang và chữ (L6 d).
DAI = re.compile(r"\b(?:K0|D1)\s*(?:[–—-]|đến|tới)\s*(?:K7|D4)\b")
# Tập vị trí ĐƯỢC PHÉP sau thi công: (tệp, số lần xuất hiện của DAI), đếm từng tệp (L6 c).
# Mỗi lần xuất hiện ở ba tệp write set phải có " và K2b"/" và D2b" ngay sau dải.
N5_MONG = {ADR: 2, PROTO: 3, SKILL: 2}
# Miễn có chủ đích (mục ngoai_pham_vi của đặc tả): ví dụ minh hoạ và mã.
N5_MIEN = {"docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md": 1, ".claude/dev/packet_loop.py": 2}
N5_LOAI = ("ops/", "references/changelog_archive/", ".claude/dev/fixtures/", ".git/", "claude-code-best-practice/")


def doan(text: str) -> list:
    return [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n[ \t]*\n", text)]


def co(text: str, cau: str) -> int:
    return sum(p.count(cau) for p in doan(text))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    root = Path(ap.parse_args().root)
    doc = lambda p: (root / p).read_text(encoding="utf-8")  # noqa: E731
    kq = []
    adr, proto, skill = doc(ADR), doc(PROTO), doc(SKILL)
    kq.append(("N1", co(adr, N1_MOI) == 1 and co(adr, N1_CU) == 0, f"mới={co(adr, N1_MOI)} cũ={co(adr, N1_CU)}"))
    dong = [ln for ln in proto.split("\n") if ln.startswith("| `ADR-0060` |")]
    o = [c.strip() for c in dong[0].strip().strip("|").split("|")] if len(dong) == 1 else []
    kq.append(("N2", len(dong) == 1 and len(o) == 4 and o[3] == N2_MOI and N2_CU not in proto,
               f"dòng ADR-0060={len(dong)} ô_cổng={o[3] if len(o) == 4 else '-'!r}"))
    kq.append(("N3", co(proto, N3_MOI) == 1 and co(proto, N3_CU) == 0, f"mới={co(proto, N3_MOI)} cũ={co(proto, N3_CU)}"))
    m4 = [co(skill, x) for x in N4_MOI] + [co(skill, x) for x in N4_CU]
    kq.append(("N4", m4 == [1, 1, 0, 0], f"mới={m4[:2]} cũ={m4[2:]}"))
    dem, sai = {}, []
    for f in sorted(root.rglob("*")):
        r = f.relative_to(root).as_posix()
        if not f.is_file() or r.startswith(N5_LOAI) or f.suffix not in (".md", ".py", ".yml", ".yaml", ".txt", ".sh", ".ps1", ""):
            continue
        try:
            t = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if r.endswith("_test.py") or r == "ops/specs/wp1555-r1-do.py":
            continue
        for mm in DAI.finditer(re.sub(r"\s+", " ", t)):
            dem[r] = dem.get(r, 0) + 1
            if r in N5_MONG and not re.sub(r"\s+", " ", t)[mm.end():mm.end() + 8].startswith((" và K2b", " và D2b")):
                sai.append(f"{r}:{mm.group(0)!r} thiếu hậu tố")
    mong = {**N5_MONG, **N5_MIEN}
    kq.append(("N5", dem == mong and not sai, f"đếm={dem} mong={mong} sai={sai}"))
    for ten, dat, ct in kq:
        print(f"{ten} {'ĐẠT' if dat else 'ĐỎ'}  {ct}")
    return 0 if all(d for _, d, _ in kq) else 1


if __name__ == "__main__":
    sys.exit(main())
