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

FAIL-CLOSE LÀ MẶC ĐỊNH. Không đọc được review · tác giả rỗng · danh sách cho phép rỗng ·
hai bản ghi mâu thuẫn không phân biệt được thứ tự ⇒ ĐỎ, không phải "tha". `None != False`
— bài học xuyên suốt kho này.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
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

# BA state là QUYẾT ĐỊNH; `COMMENTED` và `PENDING` KHÔNG phải.
# Cross-review lượt 1 (`commented-pending-xoa-quyet-dinh-cu`, P1) đo được cả hai chiều hỏng
# của bản cũ — bản cũ lấy bản ghi MỚI NHẤT trước rồi mới xét state:
#   · `APPROVED` → `COMMENTED` ⇒ mất bản duyệt (CHẶN OAN);
#   · `CHANGES_REQUESTED` → `COMMENTED` ⇒ **gỡ mất yêu cầu sửa**, và một approval của người
#     khác đủ làm cổng XANH. Một lời bình KHÔNG phải quyết định gỡ yêu cầu sửa.
# `DISMISSED` thì CÓ: REST đổi CHÍNH bản ghi cũ sang state ấy khi bản duyệt bị gỡ, nên nó
# là quyết định "huỷ quyết định" — nằm trong tập cập nhật, không nằm trong `_TAN`/`_CHAN`.
_QUYET_DINH = ("APPROVED", "CHANGES_REQUESTED", "DISMISSED")
_TAN = ("APPROVED",)
_CHAN = ("CHANGES_REQUESTED",)

_MOI_TRANG = 100     # trần của GitHub cho `per_page`
_TRAN_TRANG = 20     # 20 x 100 = 2000 bản ghi; chạm trần là KHÔNG ĐO ĐƯỢC, không phải "hết"


class KhongDoDuoc(Exception):
    """Trạng thái THỨ BA: không ĐẠT, không KHÔNG-ĐẠT, mà KHÔNG BIẾT.

    Ở cổng fail-close, KHÔNG BIẾT phải ĐỎ. Có lớp riêng để chỗ gọi không thể vô tình đọc
    nó thành một giá trị bool — đúng bài học `None != False`."""


def _chuan(x):
    """Login GitHub KHÔNG phân biệt hoa thường. So sánh thô `!=` để lọt `DucThangHo` duyệt
    cho PR của `ducthangho` — tức tự duyệt mà cổng không thấy. Casefold, không `lower()`."""
    return str(x or "").strip().casefold()


def _ma_so(r):
    """`id` của bản ghi review, hoặc `None` khi không đọc được thành số nguyên.

    Dùng làm TIE-BREAK TẤT ĐỊNH cho hai bản ghi trùng `submitted_at`. Bản cũ dùng VỊ TRÍ
    TRONG MẢNG, và cross-review đo được hậu quả (`timestamp-trung-phu-thuoc-thu-tu-mang`,
    P2): cùng hai review mâu thuẫn, hoán vị thứ tự đầu vào cho hai phán quyết trái nhau.
    Một cổng mà đáp án phụ thuộc thứ tự JSON trả về thì không phải phép đo."""
    ma = (r or {}).get("id")
    if isinstance(ma, bool):        # bool LÀ int trong Python; `True` không phải một id
        return None
    try:
        return int(ma)
    except (TypeError, ValueError):
        return None


_RE_MOC = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})(\.\d+)?"
    r"(Z|[+-]\d{2}:?\d{2})$")


def _moc(luc):
    """`submitted_at` → `datetime` có múi giờ. Không đọc được ⇒ `KhongDoDuoc`.

    BẢN ĐẦU SO BẰNG CHUỖI, và cross-review lượt 2 đo được nó FAIL-OPEN (F3): một bản
    `APPROVED` lúc `12:00:00+07:00` (= 05:00Z) so với `CHANGES_REQUESTED` lúc `06:00:00Z`
    — bản chặn MUỘN HƠN THẬT — cho `"12:00…+07" > "06:00…Z"` theo thứ tự chuỗi, nên cổng
    chọn bản duyệt làm "mới nhất" và trả XANH. Tie-break bằng `id` không cứu được: nó chỉ
    chạy khi hai chuỗi BẰNG NHAU.

    NÓI ĐÚNG PHẠM VI, vì reviewer đã nói đúng và không nên đọc mạnh hơn: REST của GitHub trả
    `submitted_at` với độ chính xác GIÂY và hậu tố `Z`, cố định độ rộng — nên với dữ liệu
    THẬT hiện nay, so chuỗi bằng so thời gian, và lỗ này **chưa với tới được**. Thứ được vá
    ở đây là một **GIẢ ĐỊNH ĐỊNH DẠNG KHÔNG AI KHAI**, đúng loại giả định mà kho này đắt giá
    nhất khi để im. Parse rồi so thì luật không còn phụ thuộc vào việc GitHub giữ nguyên
    định dạng."""
    t = str(luc or "").strip()
    m = _RE_MOC.match(t)
    if not m:
        raise KhongDoDuoc("mốc thời gian không đọc được: %r" % (luc,))
    try:
        return datetime.datetime.fromisoformat(t.replace("Z", "+00:00"))
    except ValueError as e:
        raise KhongDoDuoc("mốc thời gian không đọc được: %r (%s)" % (luc, e)) from None


def _quyet_dinh_cuoi(ban_ghi):
    """Quyết định CÒN HIỆU LỰC của MỘT người: `(state, commit_id)`, hoặc `None` nếu không có.

    `ban_ghi` = danh sách `(luc, ma, state, commit_id)` đã lọc chỉ còn state QUYẾT ĐỊNH.
    Ném `KhongDoDuoc` khi hai bản ghi cùng mốc thời gian mâu thuẫn nhau mà `id` không tách
    được — thà ĐỎ còn hơn ĐẠT vì tình cờ."""
    if not ban_ghi:
        return None
    luc_max = max(x[0] for x in ban_ghi)
    dong = [x for x in ban_ghi if x[0] == luc_max]
    if len(dong) == 1:
        return dong[0][2], dong[0][3]
    ma = [x[1] for x in dong]
    if all(x is not None for x in ma) and len(set(ma)) == len(ma):
        thang = max(dong, key=lambda x: x[1])
        return thang[2], thang[3]
    khac = {(x[2], x[3]) for x in dong}
    if len(khac) == 1:
        return next(iter(khac))
    raise KhongDoDuoc(
        "%d bản ghi quyết định cùng mốc %r mà `id` không tách được, và chúng MÂU THUẪN: %s"
        % (len(dong), luc_max, sorted(khac)))


def phan_quyet(tac_gia, reviews, cho_phep=NGUOI_DUOC_DUYET, head_sha=None):
    """Trả `(đạt, lý do)`.

    Vị từ THUẦN, nhận dữ liệu làm ĐỐI SỐ — đó là điều kiện để nó có ca BIẾT TRƯỚC ĐÁP ÁN.
    Bài học `MOC_MO_HO_CO_SAN` (PR #343): một vị từ chỉ chạy trên dữ liệu thật thì nhánh
    "báo xấu" chưa từng chạy, và đột biến làm nó luôn-tha sẽ không giết được ca nào.

    `reviews`: danh sách bản ghi review của GitHub. `None` = KHÔNG ĐỌC ĐƯỢC (khác danh sách
    RỖNG, nghĩa là đọc được và không có review nào).

    `head_sha`: BẢN DUYỆT PHẢI THUỘC VỀ ĐÚNG COMMIT ĐANG XÉT. Không có ràng buộc này thì
    duyệt xong rồi đẩy thêm commit là qua được cổng với một bản duyệt cho MÃ KHÁC — tức
    cổng đo một thứ đã hết hạn. GitHub có tuỳ chọn "dismiss stale approvals", nhưng đó là
    một Ô TRONG CÀI ĐẶT KHO, không phải thuộc tính của cổng này; dựa vào nó là dựa vào thứ
    nằm ngoài tầm cổng, và chính packet này sinh ra vì lối dựa ấy.
    `head_sha=None` = KHÔNG neo (dùng cho ca test vị từ thuần); đường CLI luôn truyền.
    """
    if reviews is None:
        return False, "KHÔNG ĐO ĐƯỢC: không đọc được danh sách review"
    ta = _chuan(tac_gia)
    if not ta:
        return False, "KHÔNG ĐO ĐƯỢC: không xác định được tác giả PR"
    cho = {_chuan(x) for x in (cho_phep or ()) if _chuan(x)}
    if not cho:
        return False, "danh sách người được duyệt RỖNG — cổng không có nghĩa"

    # GOM THEO NGƯỜI, CHỈ LẤY STATE QUYẾT ĐỊNH. GitHub cho một người duyệt rồi đổi ý; cộng
    # dồn mọi bản ghi thì một `APPROVED` đã bị thay bằng `CHANGES_REQUESTED` vẫn tính là
    # duyệt. Nhưng lọc "mới nhất" TRƯỚC khi lọc state thì một lời bình mới hơn xoá mất
    # quyết định cũ — xem chú thích ở `_QUYET_DINH`. Lọc state TRƯỚC, chọn mới nhất SAU.
    theo_nguoi = {}
    for r in reviews:
        u = (r or {}).get("user") or {}
        ai = _chuan(u.get("login"))
        if not ai:
            continue
        # Login của bot GitHub luôn mang hậu tố `[bot]` nên KHÔNG trùng được login người —
        # tức đây là chốt cho một ca CHƯA CHỨNG MINH ĐƯỢC là xảy ra thật, nói thẳng thế.
        # `type` thiếu thì coi là `User`: nó là trường TUỲ CHỌN trong hợp đồng, và fail-close
        # trên một trường tuỳ chọn là tự chặn cổng thật để đổi lấy một mối đe doạ giả định.
        if str(u.get("type") or "User") != "User":
            continue
        st = str((r or {}).get("state") or "").upper()
        if st not in _QUYET_DINH:
            continue
        try:
            luc = _moc((r or {}).get("submitted_at"))
        except KhongDoDuoc as e:
            # Mốc hỏng là KHÔNG ĐO ĐƯỢC cho CẢ phán quyết, không phải "bỏ qua bản ghi này":
            # bỏ qua nghĩa là một bản CHANGES_REQUESTED có mốc lạ biến mất khỏi phép tính.
            return False, "KHÔNG ĐO ĐƯỢC: %s — %s" % (ai, e)
        theo_nguoi.setdefault(ai, []).append(
            (luc, _ma_so(r), st, str((r or {}).get("commit_id") or "")))

    moi_nhat = {}
    for ai, bg in theo_nguoi.items():
        try:
            qd = _quyet_dinh_cuoi(bg)
        except KhongDoDuoc as e:
            return False, "KHÔNG ĐO ĐƯỢC: %s — %s" % (ai, e)
        if qd:
            moi_nhat[ai] = qd

    chan = sorted(a for a, (st, _c) in moi_nhat.items() if st in _CHAN and a in cho)
    if chan:
        return False, "có yêu cầu SỬA chưa gỡ từ: " + ", ".join(chan)

    def _dung_commit(c):
        # Neo thì phải neo CHẶT: bản ghi thiếu `commit_id` mà đang có `head_sha` để so là
        # KHÔNG ĐO ĐƯỢC, và KHÔNG ĐO ĐƯỢC không được đọc thành ĐẠT.
        return True if not head_sha else (c == str(head_sha))

    tan = sorted(a for a, (st, c) in moi_nhat.items()
                 if st in _TAN and a in cho and a != ta and _dung_commit(c))
    if not tan:
        cu_ky = sorted(a for a, (st, c) in moi_nhat.items()
                       if st in _TAN and a in cho and a != ta and not _dung_commit(c))
        if cu_ky:
            return False, ("bản duyệt của %s thuộc commit KHÁC head hiện tại — đã cũ"
                           % ", ".join(cu_ky))
        tu_duyet = [a for a, (st, _c) in moi_nhat.items() if st in _TAN and a == ta]
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


def doc_het_review(goc, token, doc=None, tran=_TRAN_TRANG, moi_trang=_MOI_TRANG):
    """Đọc HẾT các trang review. Không đọc hết được thì ném `KhongDoDuoc`.

    Bản cũ gọi đúng một lần `reviews?per_page=100` rồi phán quyết trên thứ nhận được.
    Cross-review đo thẳng (`reviews-qua-100-bi-cat-va-fail-open`, P1): với 101 bản ghi mà
    bản thứ 101 là `CHANGES_REQUESTED`, `phan_quyet` trên TẬP ĐỦ trả ĐỎ còn đường CLI nhìn
    100 bản đầu in `XANH` và `rc=0`. Cắt im lặng ở trang đầu là fail-OPEN: một PR chỉ cần
    đủ ồn ào là đẩy được quyết định chặn ra khỏi tầm nhìn của cổng.

    Đi bằng SỐ TRANG chứ không bám `Link`: điều kiện dừng khi ấy là "trang ngắn hơn
    `per_page`" — đọc được từ CHÍNH dữ liệu, không phải từ một header có thể vắng. Vẫn giữ
    hai chốt fail-close: TRẦN số trang (máy chủ trả mãi trang đầy thì dừng và báo KHÔNG ĐO
    ĐƯỢC, không lặp vô hạn) và phát hiện URL LẶP (một bản vá hỏng làm `trang` không tăng
    thì lộ ra ngay thay vì quay vòng).

    `doc` cho phép ca test bơm nguồn dữ liệu — vị từ chỉ chạy trên mạng thật là vị từ không
    có ca biết trước đáp án.
    """
    doc = doc or _api
    het, da_goi, trang = [], set(), 1
    while True:
        if trang > tran:
            raise KhongDoDuoc(
                "review vượt trần %d trang x %d — không đọc hết được, không kết luận"
                % (tran, moi_trang))
        url = "%s/reviews?per_page=%d&page=%d" % (goc, moi_trang, trang)
        if url in da_goi:
            raise KhongDoDuoc("phân trang LẶP lại URL: %s" % url)
        da_goi.add(url)
        lo = doc(url, token)
        if not isinstance(lo, list):
            raise KhongDoDuoc("phản hồi review không phải danh sách: %s" % type(lo).__name__)
        het.extend(lo)
        if len(lo) < moi_trang:
            return het
        trang += 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--kho", required=True, help="owner/repo")
    ap.add_argument("--pr", required=True, type=int)
    ap.add_argument("--tac-gia", default=None,
                    help="login tác giả; thiếu thì hỏi API (fail-close nếu hỏi hỏng)")
    ap.add_argument("--head-sha", default=None,
                    help="sha head PR; bản duyệt phải thuộc đúng commit này")
    a = ap.parse_args()
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    if not token:
        print("ĐỎ: KHÔNG ĐO ĐƯỢC — thiếu GH_TOKEN/GITHUB_TOKEN")
        return 2
    goc = "https://api.github.com/repos/%s/pulls/%d" % (a.kho, a.pr)
    tac_gia, reviews = a.tac_gia, None
    try:
        if not tac_gia:
            tac_gia = ((_api(goc, token) or {}).get("user") or {}).get("login")
        reviews = doc_het_review(goc, token)
    except (urllib.error.URLError, OSError, ValueError, KhongDoDuoc) as e:
        # KHÔNG nuốt: API hỏng là KHÔNG ĐO ĐƯỢC, và KHÔNG ĐO ĐƯỢC phải ĐỎ.
        print("ĐỎ: KHÔNG ĐO ĐƯỢC — API lỗi: %s: %s" % (type(e).__name__, e))
        return 2
    dat, ly = phan_quyet(tac_gia, reviews, head_sha=a.head_sha)
    print(("XANH: " if dat else "ĐỎ: ") + ly)
    if not dat:
        print("      tác giả=%r · số bản ghi review=%d · được phép duyệt=%s"
              % (tac_gia, len(reviews), ", ".join(NGUOI_DUOC_DUYET)))
    return 0 if dat else 1


if __name__ == "__main__":
    sys.exit(main())
