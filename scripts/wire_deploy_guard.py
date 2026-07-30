#!/usr/bin/env python3
"""Nối CHỐT CHỐNG THỤT LÙI vào `upload-skill-to-Package.ps1` — script deploy nằm NGOÀI repo.

Vì sao cần công cụ riêng: `upload-skill-to-Package.ps1` ở `D:\\Quốc hội\\`, KHÔNG có trong repo, nên
phiên Claude không đọc/sửa được. Thay vì bảo người dùng tự chèn tay (dễ chèn sai chỗ, chèn SAU lệnh
drive-push thì chốt vô nghĩa), công cụ này tự tìm lệnh `drive-push` và chèn NGAY TRƯỚC nó.

Chèn khối TỰ CHỦ — tự đọc VERSION từ repo, KHÔNG dựa vào tên biến trong script của người dùng (không
đoán được `$ver` hay `$version` hay gì khác; đoán sai thì chốt chạy với version rỗng).

DRY mặc định. Ghi thật phải `--apply` (sao lưu `.bak` trước khi ghi).

    python scripts/wire_deploy_guard.py --repo "C:\\qh\\tra-luat"                     # DRY
    python scripts/wire_deploy_guard.py --repo "C:\\qh\\tra-luat" --apply             # ghi thật
    python scripts/wire_deploy_guard.py --path "D:\\QH\\up.ps1" --repo "C:\\qh\\tra-luat" --apply

rc 0 = xong (hoặc đã nối sẵn) · 2 = không nối được (không thấy drive-push / thiếu tệp)
"""
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import sys

BEGIN = "# >>> tra-luat deploy-guard (chốt chống thụt lùi — CLAUDE.md §Quy ước deploy mục 3) >>>"
END = "# <<< tra-luat deploy-guard <<<"

# Nhận diện lệnh gọi drive-push. Chỉ cần chuỗi 'drive-push' xuất hiện ở dòng KHÔNG phải chú thích —
# bao được mọi biến thể: `& python tl.py drive-push`, `py .\scripts\tl.py drive-push`, `tl drive-push`.
RX_PUSH = re.compile(r"(?<![\w-])drive-push(?![\w-])")


def _snippet(repo: str, indent: str) -> list[str]:
    body = [
        BEGIN,
        f"$tlGuardRepo = '{repo}'",
        "$tlGuardVer  = (Get-Content (Join-Path $tlGuardRepo 'VERSION') -Raw).Trim()",
        "& (Join-Path $tlGuardRepo 'scripts/deploy-guard.ps1') -Version $tlGuardVer",
        "if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }",
        END,
    ]
    return [indent + b for b in body]


def _read(path: pathlib.Path):
    """Đọc GIỮ NGUYÊN vỏ tệp: BOM và kiểu xuống dòng.

    Bài học đắt giá của repo này: viết lại tệp bằng text-mode làm CRLF→LF, mất đúng 1 byte/dòng và
    gate đỏ vì kích thước lệch. Script deploy của người dùng gần như chắc chắn là CRLF, có thể có BOM.
    """
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    if bom:
        raw = raw[3:]
    crlf = b"\r\n" in raw
    text = raw.decode("utf-8")
    if crlf:
        text = text.replace("\r\n", "\n")
    return text, crlf, bom


def _write(path: pathlib.Path, text: str, crlf: bool, bom: bool) -> None:
    if crlf:
        text = text.replace("\n", "\r\n")
    data = text.encode("utf-8")
    if bom:
        data = b"\xef\xbb\xbf" + data
    path.write_bytes(data)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Nối chốt chống thụt lùi vào script deploy ngoài repo")
    ap.add_argument("--path", default=r"D:\Quốc hội\upload-skill-to-Package.ps1",
                    help="đường dẫn upload-skill-to-Package.ps1")
    ap.add_argument("--repo", required=True,
                    help=r"đường dẫn repo tra-luat trên máy này, vd C:\qh\tra-luat "
                         "(khối chèn đọc VERSION + deploy-guard.ps1 từ đây)")
    ap.add_argument("--apply", action="store_true", help="GHI THẬT (mặc định DRY)")
    a = ap.parse_args(argv)

    target = pathlib.Path(a.path)
    if not target.is_file():
        print(f"✗ không thấy tệp: {target}", file=sys.stderr)
        print("  Sửa --path cho đúng chỗ script deploy của bạn.", file=sys.stderr)
        return 2

    repo = pathlib.Path(a.repo)
    guard = repo / "scripts" / "deploy-guard.ps1"
    # Kiểm ngay: --repo trỏ sai thì khối chèn sẽ chết lúc deploy, lúc đó khó lần ra nguyên nhân.
    if not guard.is_file():
        print(f"✗ --repo sai: không thấy {guard}", file=sys.stderr)
        print("  --repo phải là gốc repo tra-luat (chứa VERSION và scripts/deploy-guard.ps1).", file=sys.stderr)
        return 2
    if not (repo / "VERSION").is_file():
        print(f"✗ --repo sai: không thấy {repo / 'VERSION'}", file=sys.stderr)
        return 2

    text, crlf, bom = _read(target)
    lines = text.split("\n")

    if BEGIN in text:
        print(f"✓ ĐÃ nối sẵn — không làm gì (tìm thấy marker trong {target.name}).")
        print("  Muốn nối lại: xoá khối giữa hai dòng marker rồi chạy lại.")
        return 0

    # Tìm dòng gọi drive-push ĐẦU TIÊN, bỏ qua dòng chú thích.
    idx = None
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("#"):
            continue
        if RX_PUSH.search(ln):
            idx = i
            break
    if idx is None:
        print(f"✗ KHÔNG thấy lệnh `drive-push` nào trong {target}", file=sys.stderr)
        print("  Không đoán chỗ chèn — chèn sai chỗ (sau khi đã đẩy) thì chốt vô nghĩa.", file=sys.stderr)
        print("  Hãy tự chèn khối dưới đây ngay TRƯỚC lệnh đẩy Drive:", file=sys.stderr)
        for s in _snippet(str(repo), ""):
            print("    " + s, file=sys.stderr)
        return 2

    indent = lines[idx][: len(lines[idx]) - len(lines[idx].lstrip())]
    block = _snippet(str(repo), indent)
    new_lines = lines[:idx] + block + [""] + lines[idx:]

    print(f"Tệp   : {target}")
    print(f"Vỏ tệp: {'CRLF' if crlf else 'LF'}{' + BOM' if bom else ''} (giữ nguyên)")
    print(f"Chèn TRƯỚC dòng {idx + 1}: {lines[idx].strip()[:90]}")
    print("Khối sẽ chèn:")
    for s in block:
        print("  " + s)

    if not a.apply:
        print("\n[DRY] chưa ghi gì. Thêm --apply để ghi thật (sẽ sao lưu .bak).")
        return 0

    bak = target.with_suffix(target.suffix + ".bak")
    shutil.copy2(target, bak)
    _write(target, "\n".join(new_lines), crlf, bom)
    print(f"\n✓ ĐÃ GHI. Sao lưu: {bak}")
    print("  Kiểm ngay (chưa đẩy gì): chạy script deploy của bạn — chốt phải in 'Package HIỆN TẠI: …'")
    print(f"  Hoặc chạy chốt riêng: & '{guard}' -Version (Get-Content '{repo / 'VERSION'}').Trim()")
    return 0


if __name__ == "__main__":
    sys.exit(main())
