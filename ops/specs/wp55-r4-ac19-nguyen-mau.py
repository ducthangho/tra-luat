#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  NGUYÊN MẪU NÀY ĐÃ BỊ BỎ. GIỮ LÀM HỒ SƠ, KHÔNG PHẢI ĐỂ CÀI.                      ║
# ╚══════════════════════════════════════════════════════════════════════════════════╝
#
# Chủ kho chốt 2026-08-15: AC 19 của revision 4 BỎ HẲN MIỄN TRỪ, không dùng cơ chế khối
# chứng cứ mà tệp này dựng thử.
#
# Nguyên mẫu chạy được 9/9 — nó KHÔNG bị bỏ vì hỏng. Nó bị bỏ vì đo ra rằng nó không có
# người dùng nào: chỗ duy nhất trên cây đã merge cần miễn trừ đã được xử lý ở `c47a439`
# bằng cách VIẾT LẠI CÂU, và cross-review duyệt. Một cơ chế không có người dùng là một cơ
# chế chưa ai kiểm.
#
# Giữ tệp lại vì nó là bằng chứng cho một lựa chọn đã cân nhắc chứ không phải bỏ qua, và
# vì nếu sau này có ca thật cần miễn trừ thì đây là điểm xuất phát đã đo được.
"""NGUYÊN MẪU AC 19 MỚI — kiểm hợp đồng CƠ HỌC có cài được không.

Không phải bản vá. Chỉ trả lời một câu: khuôn "khối chứng cứ khai báo" có đóng được
BỐN phản ví dụ mà bốn lượt review đã tìm ra, mà KHÔNG bắt oan ca thật, hay không.
Nếu nguyên mẫu này không đóng được thì spec revision 4 sai và phải sửa TRƯỚC khi cấp lease.
"""
import re

RE_MO = re.compile(
    r'^[ \t]*<!--[ \t]*ac19:evidence\b(?P<thuoc_tinh>[^>]*?)-->[ \t]*$', re.MULTILINE)
RE_DONG = re.compile(r'^[ \t]*<!--[ \t]*/ac19:evidence[ \t]*-->[ \t]*$', re.MULTILINE)
RE_NGUON = re.compile(r'nguồn\s*=\s*"([^"]+)"')
RE_DANG_NGUON = re.compile(r'^[^@\s]+@[0-9a-f]{7,40}:\d+(?:-\d+)?$')

N_TOI_DA = 12   # CHỐT bởi chủ kho 2026-08-15
M_TOI_DA = 3    # CHỐT bởi chủ kho 2026-08-15


def khoi_chung_cu(raw: str):
    """Trả `(tập dòng được miễn, danh sách lỗi hình thức)`.

    Lỗi hình thức làm cổng ĐỎ — thiếu thẻ đóng, thiếu `nguồn`, sai dạng, lồng nhau,
    quá dài, quá nhiều. Miễn trừ hỏng khuôn KHÔNG được im lặng bỏ qua.
    """
    dong = raw.split("\n")
    mo = [(m.start(), m.group("thuoc_tinh")) for m in RE_MO.finditer(raw)]
    dong_cua = [m.start() for m in RE_DONG.finditer(raw)]
    loi, mien = [], set()

    if len(mo) > M_TOI_DA:
        loi.append(f"quá {M_TOI_DA} khối chứng cứ trong một tệp ({len(mo)})")

    for i, (vt, thuoc_tinh) in enumerate(mo):
        so_mo = raw.count("\n", 0, vt) + 1
        ke_tiep = mo[i + 1][0] if i + 1 < len(mo) else len(raw)
        dong_hop_le = [d for d in dong_cua if vt < d < ke_tiep]
        if not dong_hop_le:
            loi.append(f"dòng {so_mo}: khối chứng cứ THIẾU thẻ đóng")
            continue
        so_dong_ket = raw.count("\n", 0, dong_hop_le[0]) + 1
        m = RE_NGUON.search(thuoc_tinh)
        if not m:
            loi.append(f"dòng {so_mo}: khối chứng cứ thiếu thuộc tính `nguồn`")
            continue
        if not RE_DANG_NGUON.match(m.group(1)):
            loi.append(f"dòng {so_mo}: `nguồn` sai dạng: {m.group(1)!r}")
            continue
        than = so_dong_ket - so_mo - 1
        if than > N_TOI_DA:
            loi.append(f"dòng {so_mo}: khối chứng cứ {than} dòng, tối đa {N_TOI_DA}")
            continue
        mien.update(range(so_mo, so_dong_ket + 1))
    return mien, loi


KIM = "người có thẩm quyền"
CA = [
    # (id, đòi_miễn, mô tả, nội dung)
    ("E1", True, "khối chứng cứ ĐÚNG khuôn — ca thật CLAUDE.md",
     '<!-- ac19:evidence nguồn="CLAUDE.md@2531366:82-83" lý-do="kể lại kết quả đo" -->\n'
     'Đo được ở `v1.36.68`: ba tên tấn công `rc=0` → `rc=4`, người có\n'
     'thẩm quyền vẫn `rc=0`.\n'
     '<!-- /ac19:evidence -->'),
    ("E2", False, "THIẾU thẻ đóng ⇒ lỗi hình thức, không miễn",
     '<!-- ac19:evidence nguồn="CLAUDE.md@2531366:82-83" -->\n'
     'người có\nthẩm quyền'),
    ("E3", False, "thiếu thuộc tính nguồn",
     '<!-- ac19:evidence -->\nngười có\nthẩm quyền\n<!-- /ac19:evidence -->'),
    ("E4", False, "nguồn sai dạng",
     '<!-- ac19:evidence nguồn="linh tinh" -->\n'
     'người có\nthẩm quyền\n<!-- /ac19:evidence -->'),
    # BỐN PHẢN VÍ DỤ của bốn lượt review — không cái nào có khối chứng cứ ⇒ KHÔNG miễn
    ("R7", False, "lượt 7: heading ngắt dòng", "## Người có\nthẩm quyền"),
    ("R9", False, "lượt 9: wrapper hai ký tự", "x người có\nthẩm quyền y"),
    ("R10a", False, "lượt 10: marker rc= không phải phép đo",
     "Tham số rc= được mô tả trước khi chép người có\nthẩm quyền là vai trò."),
    ("R10b", False, "lượt 10: phân số 1/2 trong văn xuôi",
     "Một nửa (1/2) tài liệu chép người có\nthẩm quyền là vai trò."),
    ("R10c", False, "lượt 10: khối mã thụt lề",
     "    Đo được rc=0: người có\n    thẩm quyền là vai trò."),
]


def main() -> int:
    print(f"{'id':<6} {'đòi miễn':<9} {'được':<7} {'':<5} mô tả")
    print("-" * 84)
    hong = []
    for cid, doi, mota, nd in CA:
        mien, loi = khoi_chung_cu(nd)
        # cụm nằm ở dòng nào?
        dong_co_kim = {i for i, d in enumerate(nd.split("\n"), 1)
                       if any(k in d.lower() for k in ("người có", "thẩm quyền"))}
        duoc_mien = bool(dong_co_kim) and dong_co_kim <= mien and not loi
        ok = duoc_mien == doi
        if not ok:
            hong.append(cid)
        print(f"{cid:<6} {str(doi):<9} {str(duoc_mien):<7} {'ok' if ok else 'HỎNG':<5} {mota}")
        if loi:
            print(f"       └─ lỗi hình thức: {loi[0]}")
    print("-" * 84)
    print(f"đạt {len(CA) - len(hong)}/{len(CA)} · hỏng: {hong or 'không'}")
    return 1 if hong else 0


if __name__ == "__main__":
    raise SystemExit(main())
