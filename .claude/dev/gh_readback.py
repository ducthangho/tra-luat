#!/usr/bin/env python3
"""gh_readback.py — đăng nội dung lên GitHub rồi CHỨNG MINH thứ ĐÃ ĐẾN khớp từng byte.

VÌ SAO CÓ TỆP NÀY (mỗi mục là một lần đã trả giá, ngày 17–18/08/2026)

1. TẦNG VẬN CHUYỂN ĂN MẤT NỘI DUNG, IM LẶNG.
   Đăng PR body chứa `git cat-file -e HEAD:<path>`. Lời gọi trả THÀNH CÔNG. Bản đã
   đến mất sạch `<path>` — nó bị xử lý như một thẻ HTML và bị xoá. Các dấu `>` khác
   trong cùng body vẫn còn (dạng `&gt;`), nên đây là XOÁ chứ không phải escape.
   Câu lệnh trong tài liệu thành `git cat-file -e HEAD:` — ai chép về sẽ chạy hỏng.
   Chỉ lộ vì đã đọc ngược body về và diff. Cùng họ với sự cố `co\\u0308dex` ở PR #92:
   một lớp mà ta không coi là lớp.

2. DÒ BẰNG CÁCH GÕ TAY CHUỖI TIẾNG VIỆT = BÁO ĐỘNG GIẢ.
   Hai lần liên tiếp báo "MẤT" cho nội dung còn nguyên, chỉ vì chuỗi dò gõ sai dấu
   (`MAT 0` vs `MẤT 0`, `KHỢP` vs `KHỚP`). Phép kiểm đúng là DIFF TOÀN VĂN, không
   phải spot-check bằng mắt và bàn phím.

3. BẢN CỤC BỘ TRÔI LỆCH BẢN ĐÃ ĐĂNG.
   Sửa thẳng trong đối số lời gọi mà quên cập nhật tệp nguồn ⇒ lần sửa SAU đăng lại
   từ tệp cũ và xoá âm thầm phần đã thêm. Nên nguồn PHẢI là một TỆP, và sau khi đăng
   phải đối chiếu tệp ấy với bản đã đến.

4. `rc` SAU PIPE LÀ MÃ CỦA LỆNH CUỐI.
   `gh workflow run ... | tail -3; echo rc=$?` in `rc=0` trong khi `gh` ăn HTTP 503
   và không có lượt chạy nào được tạo. Đúng bệnh CLAUDE.md dặn ("cổng xanh nhờ rc=0
   là cổng CÓ THỂ BỊ LỪA") — và vẫn dẫm.

MÃ THOÁT
  0  khớp từng byte
  2  tham số sai
  3  gọi GitHub thất bại (rc thật của `gh`, không phải của lệnh sau pipe)
  5  ĐÃ ĐĂNG NHƯNG LỆCH — in unified diff; đây là ca tệ nhất và phải ồn ào
  6  tệp nguồn không đọc được / rỗng
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import subprocess
import sys
from pathlib import Path

MA_OK, MA_THAM_SO, MA_GOI, MA_LECH, MA_NGUON = 0, 2, 3, 5, 6


def _chay(*doi_so: str, dau_vao: str | None = None) -> tuple[int, str, str]:
    """Chạy lệnh, trả (rc THẬT, stdout, stderr). KHÔNG shell, KHÔNG pipe.

    Đây là chốt cho bẫy số 4 ở đầu tệp: không có lệnh nào đứng sau để nuốt mã thoát.
    """
    try:
        p = subprocess.run(list(doi_so), input=dau_vao, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=180)
    except FileNotFoundError:
        return (127, "", f"khong tim thay: {doi_so[0]}")
    except subprocess.TimeoutExpired:
        return (124, "", "qua han 180s")
    except OSError as e:
        return (127, "", str(e))
    return (p.returncode, p.stdout, p.stderr)


def _chuan(s: str) -> str:
    """Chuẩn hoá TỐI THIỂU trước khi so: CRLF→LF và bỏ newline cuối.

    CHỈ hai thứ đó. Mọi chuẩn hoá thêm (gộp khoảng trắng, NFC, casefold) sẽ GIẤU đúng
    loại mất mát mà công cụ này sinh ra để bắt — xem bẫy số 1.
    """
    return s.replace("\r\n", "\n").rstrip("\n")


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _doc_body(kho: str, so: int, loai: str) -> tuple[int, str, str]:
    duong = f"repos/{kho}/pulls/{so}" if loai == "pr" else f"repos/{kho}/issues/{so}"
    rc, out, err = _chay("gh", "api", duong, "--jq", ".body")
    return rc, out, err


def _canh_bao_ky_tu(s: str) -> list[str]:
    """Cảnh báo TRƯỚC khi đăng về những thứ đã từng bị tầng vận chuyển ăn."""
    ra = []
    import re
    the = sorted(set(re.findall(r"<[A-Za-z_][A-Za-z0-9_.-]*>", s)))
    if the:
        ra.append(f"co {len(the)} chuoi dang the HTML se BI XOA: {the[:6]}")
    if "\\u" in s:
        ra.append("co chuoi thoat kieu \\uXXXX — tang van chuyen co the GIAI MA no")
    return ra


def lenh_dang(a) -> int:
    nguon = Path(a.file)
    if not nguon.is_file():
        print(f"khong doc duoc tep nguon: {nguon}", file=sys.stderr)
        return MA_NGUON
    noi_dung = nguon.read_text(encoding="utf-8")
    if not noi_dung.strip():
        print("tep nguon RONG — tu choi dang", file=sys.stderr)
        return MA_NGUON

    for c in _canh_bao_ky_tu(noi_dung):
        print(f"  CANH BAO: {c}")

    if not a.chi_kiem:
        payload = json.dumps({"body": noi_dung}, ensure_ascii=False)
        duong = (f"repos/{a.repo}/pulls/{a.number}" if a.loai == "pr"
                 else f"repos/{a.repo}/issues/{a.number}")
        rc, out, err = _chay("gh", "api", "--method", "PATCH", duong,
                             "--input", "-", dau_vao=payload)
        if rc != 0:
            print(f"gh PATCH that bai rc={rc}: {(err or out)[:400]}", file=sys.stderr)
            return MA_GOI
        print(f"  da goi PATCH, rc={rc}")

    rc, den, err = _doc_body(a.repo, a.number, a.loai)
    if rc != 0:
        print(f"doc nguoc that bai rc={rc}: {(err or den)[:400]}", file=sys.stderr)
        return MA_GOI

    n, d = _chuan(noi_dung), _chuan(den)
    print(f"  sha256 nguon  = {_sha(n)}")
    print(f"  sha256 DA DEN = {_sha(d)}")
    if n == d:
        print(f"  KHOP TUNG BYTE ({len(d.encode())} bytes)")
        return MA_OK
    print("  *** LECH — thu da den KHAC thu da gui ***", file=sys.stderr)
    for dong in list(difflib.unified_diff(n.split("\n"), d.split("\n"),
                                          "nguon", "da_den", lineterm=""))[:80]:
        print(dong, file=sys.stderr)
    return MA_LECH


def lenh_chay(a) -> int:
    """Chạy một lệnh và in rc THẬT. Chốt cho bẫy số 4."""
    if not a.lenh:
        print("thieu lenh sau `--`", file=sys.stderr)
        return MA_THAM_SO
    rc, out, err = _chay(*a.lenh)
    if out:
        print(out, end="" if out.endswith("\n") else "\n")
    if err:
        print(err, end="" if err.endswith("\n") else "\n", file=sys.stderr)
    print(f"  rc_that={rc}")
    return rc


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="gh_readback.py", allow_abbrev=False,
                                description="dang len GitHub roi CHUNG MINH thu da den")
    sub = p.add_subparsers(dest="lenh_con", required=True)

    d = sub.add_parser("body", help="dang body tu TEP roi doc nguoc va diff")
    d.add_argument("--repo", required=True, metavar="OWNER/REPO")
    d.add_argument("--number", required=True, type=int)
    d.add_argument("--file", required=True, help="TEP nguon — khong nhan noi dung inline")
    d.add_argument("--loai", choices=["pr", "issue"], default="pr")
    d.add_argument("--chi-kiem", action="store_true",
                   help="khong dang, chi doc nguoc va diff voi tep")
    d.set_defaults(fn=lenh_dang)

    r = sub.add_parser("run", help="chay lenh va in rc THAT (khong qua pipe)")
    r.add_argument("lenh", nargs=argparse.REMAINDER)
    r.set_defaults(fn=lenh_chay)

    a = p.parse_args(argv)
    if getattr(a, "lenh", None) and a.lenh and a.lenh[0] == "--":
        a.lenh = a.lenh[1:]
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
