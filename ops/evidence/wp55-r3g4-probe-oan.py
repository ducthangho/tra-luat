#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đo chiều BẮT OAN — AC 19. Mọi ca ở đây PHẢI rc=0 (tha).

Mỗi lớp chuẩn hoá thêm ở AC 18 có ít nhất một ca bắt-oan tương ứng.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(sys.argv[1]).resolve()

SACH = ("# Adapter demo\n\n**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §13.\n\n"
        "Dưới đây chỉ có cú pháp của nền.\n")

# Ca THẬT đang làm gate đỏ: CLAUDE.md master dòng 80-84, nguyên văn.
# Cụm `người có thẩm quyền` bị NGẮT DÒNG giữa `người có` / `thẩm quyền`,
# trong một câu KỂ LẠI kết quả đo — không phải chép bảng vai trò §2.
THAT = (
    "biệt THẨM QUYỀN. Danh sách cấm phải đoán trước mọi cách viết của kẻ gian "
    "(dấu nối, tiền tố, hậu tố,\n"
    "  đồng tự Unicode, tổ hợp dấu) nên **thua từ trong thiết kế**; danh sách cho "
    "phép chỉ phải liệt kê một\n"
    "  tập nhỏ và biết trước. Đo được ở `v1.36.68` (PR #104): ba tên tấn công "
    "`rc=0` → `rc=4`, người có\n"
    "  thẩm quyền vẫn `rc=0`. Kèm chốt: đột biến **nới danh sách cho phép để chứa "
    "tên tấn công** phải làm\n"
    "  ca đích ĐỎ — không có đột biến ấy thì không biết ca đang đo danh sách hay "
    "đo thứ khác.\n"
)

CA = [
    ("O1", "THẬT/ngắt dòng", "CLAUDE.md master 80-84 nguyên văn — văn xuôi kể kết quả đo", THAT),
    ("O2", "term/văn xuôi", "dùng cụm 'người có thẩm quyền' giữa câu",
     "Chỉ người có thẩm quyền mới cấp được lease; phiên worker thì không.\n"),
    ("O3", "term/văn xuôi", "'người có thẩm quyền' ngắt dòng trong câu khác",
     "Quyết định này thuộc về người có\nthẩm quyền, không thuộc phiên này.\n"),
    ("O4", "entity lồng", "&amp;#58; render ra &#58; NGUYÊN VĂN, không phải dấu hai chấm",
     "Ghi chú: merged&amp;#58; PR đã vào nhánh đích\n"),
    ("O5", "đồng tự", "văn bản Nga THẬT — gấp đồng tự không được sinh cụm cấm",
     "Пример текста на русском языке: локальный контроллер работает.\n"),
    ("O6", "đồng tự", "văn bản Hy Lạp THẬT",
     "Παράδειγμα κειμένου στα ελληνικά για δοκιμή.\n"),
    ("O7", "dash", "từ có gạch nối thông thường trong văn xuôi",
     "Quy trình cross-review chạy end-to-end với cấu hình read-only.\n"),
    ("O8", "html tag", "mẫu code có dấu < > không phải tag",
     "Chạy: `python tl.py --json` rồi so `a < b > c` trong shell.\n"),
    ("O9", "html tag", "tag HTML bình thường quanh chữ vô hại",
     "Xem <b>tài liệu</b> và <i>ghi chú</i> ở docs/.\n"),
    ("O10", "link", "link Markdown bình thường",
     "Đọc [protocol](docs/PROTOCOL_DA_PHIEN.md) và [changelog](CHANGELOG.md).\n"),
    ("O11", "backslash", "escape Markdown bình thường",
     "Ký tự \\* và \\_ phải escape khi viết Markdown.\n"),
    ("O12", "Cf", "văn bản tiếng Việt đầy đủ dấu — lọc Cf không được nuốt dấu",
     "Điều 5 quy định: người sử dụng lao động phải trả lương đúng hạn.\n"),
    ("O13", "NFKC", "trích dẫn có dấu câu toàn rộng, vô hại",
     "Trích nguồn CJK：文書の内容はここにあります。\n"),
    ("O14", "trỏ đúng cách", "adapter TRỎ về protocol, không chép",
     "Ngưỡng và bảng vai trò: xem `docs/PROTOCOL_DA_PHIEN.md` §2 và §12.\n"),
    ("O15", "term/bảng khác", "bảng Markdown KHÔNG phải bảng vai trò",
     "| cột | giá trị |\n|---|---|\n| thời gian | 5 phút |\n"),
]


def do(noi_dung: str, tmp: Path, ten: str) -> tuple[int, str]:
    r = tmp / ten
    (r / ".claude" / "skills" / "demo").mkdir(parents=True, exist_ok=True)
    (r / ".claude" / "skills" / "demo" / "SKILL.md").write_text(
        SACH + "\n" + noi_dung, encoding="utf-8", newline="\n")
    p = subprocess.run([sys.executable, str(SCRIPT), "doctrine-scan", "--root", str(r)],
                       capture_output=True)
    return p.returncode, p.stderr.decode("utf-8", "replace").strip()


def main() -> int:
    oan, ok = [], 0
    with tempfile.TemporaryDirectory(prefix="probe_oan_") as td:
        tmp = Path(td)
        print(f"{'id':<5} {'lớp':<16} {'rc':<4} kết  mô tả")
        print("-" * 100)
        for cid, lop, mota, noi_dung in CA:
            rc, err = do(noi_dung, tmp, cid)
            if rc == 0:
                ket = "ok  "
                ok += 1
            else:
                ket = "OAN "
                oan.append(cid)
            print(f"{cid:<5} {lop:<16} {rc:<4} {ket} {mota}")
            if rc != 0:
                print(f"      └─ {err.splitlines()[0] if err else ''}")
    print("-" * 100)
    print(f"đạt {ok}/{len(CA)} · BẮT OAN: {oan or 'không'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
