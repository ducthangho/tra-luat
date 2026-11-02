#!/usr/bin/env python3
"""wp728 r2 — bộ sinh đột biến TẤT ĐỊNH cho M2' (spec §Rig).

Đọc wrapper, đòi dòng gọi thu hồi xuất hiện ĐÚNG 1 lần, thay bằng thân rỗng, ghi ra tệp
đích (tạo mới, không ghi đè), in sha256 của bản đột biến. Khớp != 1 ⇒ rc 3, không ghi gì.

Dùng:  python3 mutate.py <wrapper.ps1> <tep-dich.ps1>
"""
import hashlib
import os
import sys

GOC = "        if ($inRun) { [void](Invoke-ReapAdopted $direct) }"
THAY = "        if ($inRun) { }"


def dot_bien(du_lieu: bytes) -> tuple[bytes, int]:
    """Trả (bản đột biến, số dòng khớp). So NGUYÊN dòng, bỏ riêng ký tự xuống dòng ở cuối."""
    dong = du_lieu.splitlines(keepends=True)
    goc_b, thay_b = GOC.encode("utf-8"), THAY.encode("utf-8")
    vi_tri = [i for i, d in enumerate(dong) if d.rstrip(b"\r\n") == goc_b]
    if len(vi_tri) != 1:
        return b"", len(vi_tri)
    i = vi_tri[0]
    duoi = dong[i][len(goc_b):]
    dong[i] = thay_b + duoi
    return b"".join(dong), 1


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("dung: mutate.py <wrapper.ps1> <tep-dich.ps1>", file=sys.stderr)
        return 2
    with open(argv[1], "rb") as f:
        goc = f.read()
    ra, khop = dot_bien(goc)
    if khop != 1:
        print(f"KHONG_GHI: khop={khop} (doi dung 1)", file=sys.stderr)
        return 3
    fd = os.open(argv[2], os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "wb") as f:
        f.write(ra)
    print(f"khop=1 sha256_goc={hashlib.sha256(goc).hexdigest()} sha256_dot_bien={hashlib.sha256(ra).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
