#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cổng: NGƯỜI DUYỆT phải khác NGƯỜI TẠO PR — packet #348 (TACH-DANH-TINH-GITHUB).

VÌ SAO CỔNG NÀY KHÁC MỌI CHỐT TRƯỚC ĐÓ TRONG KHO. PR #343 (packet #338) đo được và khai
thẳng: phiên chạy bằng credential CỦA CHỦ KHO, nên mọi chốt dựng trong kho đều là chốt chủ
kho tự dựng cho chính mình — `guard --action merge` chặn một NHÃN VAI, không chặn một
THẨM QUYỀN. Cổng này chạy trên RUNNER CỦA GITHUB bằng `GITHUB_TOKEN`, KHÔNG bằng credential
của phiên. Phiên không thể làm nó xanh bằng lời khai: muốn xanh thì phải thật sự tồn tại một
bản duyệt mang login KHÁC. Đó là cơ chế đầu tiên ở đây không tự chứng nhận.

VÀ NÓ VẪN CHƯA ĐỦ MỘT MÌNH — nói ngay để không ai đọc mạnh hơn sự thật: khi chưa có nửa
NGOÀI kho (danh tính chạy-việc không phải admin + `master` siết kèm ô "không cho bypass"),
cổng này là KHUYẾN NGHỊ. Admin bypass được required check, và chưa ai đánh dấu nó required.
Nửa trong kho là thứ để nửa ngoài CÓ CÁI MÀ ĐÒI. Xem `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md`.

FAIL-CLOSE LÀ MẶC ĐỊNH. Không đọc được review · tác giả rỗng · danh sách cho phép rỗng ⇒
ĐỎ, không phải "tha". `None != False` — bài học xuyên suốt kho này.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):        # console cp1258 giết cả lượt chạy trước khi
    sys.stdout.reconfigure(encoding="utf-8")  # logic kịp sai — bài học 12-08-2026
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# DANH SÁCH CHO PHÉP, không phải danh sách cấm. Kho này đã trả giá đúng một lần cho hình
# dạng ngược lại (`lease-authority-spoof`: cấm hai chuỗi `claude`/`codex` thì
# `codex-dispatcher`, `ai-codex-bot`, `cödex` đều lọt — "phân biệt CÁCH VIẾT, không phân
# biệt THẨM QUYỀN"). Ở đây tập người có thể duyệt là HỮU HẠN và BIẾT TRƯỚC.
#
# Đo 27-08-2026 (`list_repository_collaborators`): ducthangho=admin · code2nguyen=write.
# `ducthangho` NẰM TRONG danh sách và điều đó KHÔNG làm cổng vô nghĩa: luật "khác tác giả"
# mới là thứ làm việc. Phiên chạy bằng credential của `ducthangho`, nên khi phiên mở PR thì
# chỉ `code2nguyen` thoả được — tức đúng một danh tính mà phiên KHÔNG cầm.
NGUOI_DUOC_DUYET = ("ducthangho", "code2nguyen")

_TAN = ("APPROVED",)
_CHAN = ("CHANGES_REQUESTED",)


def _chuan(x):
    """Login GitHub KHÔNG phân biệt hoa thường. So sánh thô `!=` để lọt `DucThangHo` duyệt
    cho PR của `ducthangho` — tức tự duyệt mà cổng không thấy. Casefold, không `lower()`."""
    return str(x or "").strip().casefold()


def phan_quyet(tac_gia, reviews, cho_phep=NGUOI_DUOC_DUYET):
    """Trả `(đạt, lý do)`.

    Vị từ THUẦN, nhận dữ liệu làm ĐỐI SỐ — đó là điều kiện để nó có ca BIẾT TRƯỚC ĐÁP ÁN.
    Bài học `MOC_MO_HO_CO_SAN` (PR #343): một vị từ chỉ chạy trên dữ liệu thật thì nhánh
    "báo xấu" chưa từng chạy, và đột biến làm nó luôn-tha sẽ không giết được ca nào.

    `reviews`: danh sách bản ghi review của GitHub. `None` = KHÔNG ĐỌC ĐƯỢC (khác danh sách
    RỖNG, nghĩa là đọc được và không có review nào).
    """
    if reviews is None:
        return False, "KHÔNG ĐO ĐƯỢC: không đọc được danh sách review"
    ta = _chuan(tac_gia)
    if not ta:
        return False, "KHÔNG ĐO ĐƯỢC: không xác định được tác giả PR"
    cho = {_chuan(x) for x in (cho_phep or ()) if _chuan(x)}
    if not cho:
        return False, "danh sách người được duyệt RỖNG — cổng không có nghĩa"

    # CHỈ TÍNH REVIEW MỚI NHẤT CỦA MỖI NGƯỜI. GitHub cho một người duyệt rồi đổi ý; cộng
    # dồn mọi bản ghi thì một `APPROVED` đã bị thay bằng `CHANGES_REQUESTED` vẫn tính là
    # duyệt. Thứ tự lấy theo `submitted_at`, và bản ghi thiếu mốc thời gian thì lùi về thứ
    # tự xuất hiện — API trả theo thời gian tăng dần.
    moi_nhat = {}
    for i, r in enumerate(reviews):
        ai = _chuan((r or {}).get("user", {}).get("login"))
        if not ai:
            continue
        khoa = ((r or {}).get("submitted_at") or "", i)
        if ai not in moi_nhat or khoa > moi_nhat[ai][0]:
            moi_nhat[ai] = (khoa, str((r or {}).get("state") or "").upper())

    chan = sorted(a for a, (_, st) in moi_nhat.items() if st in _CHAN and a in cho)
    if chan:
        return False, "có yêu cầu SỬA chưa gỡ từ: " + ", ".join(chan)

    tan = sorted(a for a, (_, st) in moi_nhat.items()
                 if st in _TAN and a in cho and a != ta)
    if not tan:
        tu_duyet = [a for a, (_, st) in moi_nhat.items() if st in _TAN and a == ta]
        if tu_duyet:
            return False, ("chỉ có TỰ DUYỆT (%s) — cần một danh tính KHÁC" % ta)
        return False, ("chưa có bản duyệt nào từ danh tính khác `%s` trong %s"
                       % (ta, ", ".join(sorted(cho))))
    return True, "đã duyệt bởi danh tính khác tác giả: " + ", ".join(tan)


def _api(duong, token):
    req = urllib.request.Request(duong, headers={
        "Authorization": "Bearer %s" % token, "Accept": "application/vnd.github+json",
        "User-Agent": "tl-duyet-danh-tinh"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--kho", required=True, help="owner/repo")
    ap.add_argument("--pr", required=True, type=int)
    ap.add_argument("--tac-gia", default=None,
                    help="login tác giả; thiếu thì hỏi API (fail-close nếu hỏi hỏng)")
    a = ap.parse_args()
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    if not token:
        print("ĐỎ: KHÔNG ĐO ĐƯỢC — thiếu GH_TOKEN/GITHUB_TOKEN")
        return 2
    goc = "https://api.github.com/repos/%s/pulls/%d" % (a.kho, a.pr)
    tac_gia, reviews = a.tac_gia, None
    try:
        if not tac_gia:
            tac_gia = (_api(goc, token).get("user") or {}).get("login")
        reviews = _api(goc + "/reviews?per_page=100", token)
    except (urllib.error.URLError, OSError, ValueError) as e:
        # KHÔNG nuốt: API hỏng là KHÔNG ĐO ĐƯỢC, và KHÔNG ĐO ĐƯỢC phải ĐỎ.
        print("ĐỎ: KHÔNG ĐO ĐƯỢC — API lỗi: %s: %s" % (type(e).__name__, e))
        return 2
    dat, ly = phan_quyet(tac_gia, reviews)
    print(("XANH: " if dat else "ĐỎ: ") + ly)
    if not dat:
        print("      tác giả=%r · số bản ghi review=%d · được phép duyệt=%s"
              % (tac_gia, len(reviews), ", ".join(NGUOI_DUOC_DUYET)))
    return 0 if dat else 1


if __name__ == "__main__":
    sys.exit(main())
