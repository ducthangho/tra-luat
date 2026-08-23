#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Máy trạng thái cưỡng chế stop conditions cho work packet (protocol đa phiên).

Quy tắc, schema và tiêu chí hoàn tất KHÔNG nằm ở đây — chúng nằm ở
`docs/PROTOCOL_DA_PHIEN.md`. Tệp này chỉ CƯỠNG CHẾ vài chốt bằng mã thoát khác 0,
vì văn bản không kiểm được còn tiến trình thì kiểm được.

Ranh giới: KHÔNG chạm remote (không `git push`, không `gh`, không đọc secrets).
Nó giữ state cục bộ và phát VĂN BẢN comment; phiên Claude mới là bên đăng.

Mã thoát
    0  ok
    2  sai đối số — slug sai dạng, thiếu finding-id, lý do void ngoài allowlist
    3  chạm trần — hết attempt, hoặc một finding-id lặp tới same-failure limit
    4  vi phạm cross-provider
    5  dấu vết comment không hợp lệ — chưa đăng ký, sai transition, hoặc đã dùng
    6  doctrine-scan bắt được cụm từ bị cấm trong adapter
    7  guard chặn cứng một hành vi trong bảng
    8  trạng thái không hợp lệ — transition sai, lượt đang mở, init đè state

Ba cơ chế dưới đây là LÕI của revision 2. Chúng thay ba cơ chế mà ba lượt review
liên tiếp chứng minh là sai từ thiết kế — chi tiết ở phần chú thích từng chỗ.
"""

from __future__ import annotations

import argparse
import hmac
import html
import json
import os
import platform
import re
import secrets
import subprocess
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from launcher import ky_ban_ghi_luot

# --- Ngưỡng ------------------------------------------------------------------
# Hai số này KHÔNG do tệp này đặt ra; chúng là mặc định thừa kế từ envelope của
# mission và được truyền vào lúc `init`. Để mặc định ở đây chỉ để lệnh chạy được
# khi người gọi không khai; envelope của mission mới là nguồn.
MAC_DINH_TRAN_ATTEMPT = 3
MAC_DINH_TRAN_SAME_FAILURE = 2

# --- Mã thoát ----------------------------------------------------------------
RC_OK = 0
RC_ARG = 2
RC_TRAN = 3
RC_PROVIDER = 4
RC_TRACE = 5
RC_DOCTRINE = 6
RC_GUARD = 7
RC_STATE = 8
RC_ADR = 9
RC_MOI_TRUONG = 10

PROVIDERS = ("claude", "codex")

# CHỐT THẬT của `--granted-by` — danh sách CHO PHÉP, không phải danh sách cấm.
#
# Vì sao đổi: cross-review lượt 4 (codex, 14-08-2026) tìm ra `lease-authority-spoof`
# P1 — chốt cũ (còn lại ở `PROVIDERS` phía trên) chỉ từ chối ĐÚNG hai chuỗi
# `claude`/`codex`, nên `codex-dispatcher`, `ai-codex-bot`, `cödex` đều lọt qua và
# tự cấp được lease. Nguyên văn kết luận của reviewer: *"distinguishes spelling,
# not authority"* — phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN. Cùng khuyết
# tật đã vá ở tầng cửa đăng, `ops/lease_publish.py::NGUOI_CO_THAM_QUYEN` — đây là
# tầng cục bộ song song, cùng luật.
#
# Danh sách cấm phải đoán trước mọi cách viết của kẻ gian — thua từ trong thiết
# kế. Danh sách cho phép chỉ phải liệt kê những người CÓ thẩm quyền, một tập nhỏ
# và biết trước.
#
# NÓI THẲNG GIỚI HẠN, đừng để ai đọc rộng hơn thực tế: danh sách này chứng minh
# cái TÊN được phép cấp lease, KHÔNG chứng minh đúng người đó đã gõ. Khác với
# `ops/lease_publish.py`, tệp NÀY chạy CỤC BỘ (không phải trong GitHub Actions),
# nên KHÔNG có `GITHUB_ACTOR` để neo danh tính — lớp neo GitHub-xác-thực đó chỉ
# có mặt ở cửa đăng, không có mặt ở đây. Sửa danh sách này phải qua một commit có
# review.
NGUOI_CO_THAM_QUYEN = ("ducthangho",)

# Hành vi bị chặn cứng. Bảng này KHÔNG có cờ nới — có cờ nới là không có chốt.
HANH_VI_CHAN = (
    "merge",
    "deploy",
    "live",
    "secrets",
    "force-push",
    "delete-branch",
    "delete-worktree",
    "edit-other-spec",
)

# Lý do được hoàn lượt. Allowlist đóng — không nhận lý do tự chế.
LY_DO_VOID = ("quota", "rate_limit", "infrastructure", "permission")
LY_DO_CAN_BANG_CHUNG = ("infrastructure", "permission")
NGUONG_TUOI_BANG_CHUNG_GIAY = 3600
BIEN_BANG_CHUNG = "TL_MOI_TRUONG_JSON"

# State machine cục bộ của một packet đang chạy. Tên đầy đủ và ngữ nghĩa của
# từng state thuộc protocol; ở đây chỉ có phần executor thực sự đi qua.
#
# `accepted` CỐ Ý KHÔNG có mặt làm đích của bất kỳ chuyển động nào ở bảng này.
# Nó chỉ được ghi bởi `record-review --verdict approve`, tức là ĐÚNG MỘT ĐƯỜNG.
# Bài học phải trả giá: khi `accepted` còn là đích hợp lệ của `transition`, một
# lệnh `transition --to accepted` kèm comment-id hợp lệ đi thẳng vào `accepted`
# với `reviews: []` và `accepted_sha: null` — tức mỏ neo SHA vừa dựng bị vô hiệu
# hoàn toàn. Canh từng cửa một là thua; chỉ để lại MỘT cửa mới thắng.
# Đừng thêm "accepted" vào đây, kể cả cho tiện.
CHUYEN_HOP_LE = {
    # `leased` KHÔNG phải đích của bất kỳ chuyển động nào ở bảng này — cùng lý do
    # với `accepted` ngay trên, và cùng bài học "canh từng cửa là thua, chỉ để lại
    # MỘT cửa mới thắng". Đường duy nhất vào `leased` là `record-lease`, nơi đòi
    # uỷ quyền + dấu vết + hạn.
    "awaiting_lease": (),
    "leased": ("running",),
    "running": ("reviewing",),
    # `reviewing` KHÔNG còn đường ra bằng `transition` — kể cả về `running`.
    #
    # Finding `review-transition-bypasses-record-review` (cross-review lượt 6, codex,
    # 15-08-2026): bản trước cho `reviewing → running`, nên gõ ba lệnh
    # `transition reviewing` → `transition running` → `transition reviewing` là quay
    # lại review mà KHÔNG hề gọi `record-review`. Đã ĐO trên head `e6e4b73`: cả ba
    # rc=0, kết ở `state=reviewing attempts_used=1 reviews=[] finding_counts={}`.
    # Nghĩa là lặp review↔fix VÔ HẠN trong cùng một attempt, không tăng phép đếm
    # finding, không chạm trần attempt lẫn same-failure — vô hiệu hoá đúng hai thứ
    # AC 3 và AC 4 tồn tại để cưỡng chế.
    #
    # Đường ra khỏi `reviewing` do VERDICT điều khiển, không do người gõ `transition`:
    # `record-review` tự đặt state (`approve`→accepted, `changes_requested`→running,
    # `blocked`→blocked) SAU khi đã đếm finding và kiểm trần. Đây là lần thứ BA cùng
    # một bài học trong tệp này — `accepted`, rồi `leased`, giờ tới `reviewing`:
    # canh từng cửa là thua, chỉ để lại MỘT cửa mới thắng.
    "reviewing": (),
    "accepted": (),
    "blocked": (),
}

# Các state chỉ được ghi bởi luồng review, không bao giờ bởi `transition`.
# `reviewing` không nằm đây vì nó VÀO được bằng `transition` (từ `running`); thứ bị
# cấm là đường RA. Bảng `CHUYEN_HOP_LE` ở trên đã cưỡng chế điều đó.
STATE_CHI_DO_REVIEW_GHI = ("accepted",)

# --- (a) same-failure theo ID ỔN ĐỊNH ----------------------------------------
# Vì sao không dùng vân tay văn xuôi: ba lượt review liên tiếp lách được nó bằng
# ".", rồi "=="/"!=", rồi "!". Mỗi lượt lại có một ký tự mới — chuẩn hoá văn xuôi
# là cuộc đuổi bắt không có đáy. Ở đây KHOÁ là slug do reviewer khai; mô tả chỉ
# là chú thích và KHÔNG tham gia vào khoá. Mọi mẹo ký tự trở nên vô nghĩa vì
# không còn chỗ nào cho ký tự tác động tới phép đếm.
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# --- (b) dấu vết comment ------------------------------------------------------
# ID do GitHub TRẢ VỀ lúc đăng: id số, hoặc node id dạng "IC_kwDO...".
COMMENT_ID_RE = re.compile(r"^(?:[0-9]{6,}|[A-Za-z]{2}_[A-Za-z0-9_-]{10,})$")

# Bằng chứng review gắn EXACT SHA — git oid đầy đủ, không nhận dạng rút gọn.
SHA_RE = re.compile(r"^[0-9a-f]{40}$")

# --- (c) danh sách cụm từ doctrine BỊ CẤM trong adapter ------------------------
# Đây là "đáy đo" mà revision 1 không có. Ba lượt review đều kết luận "adapter
# chép doctrine" bằng mắt, và ba lượt đều bắt lại được — vì tiêu chí đọc bằng mắt
# không có ngưỡng. Danh sách này khai TƯỜNG MINH cái gì bị coi là bản sao, và
# `doctrine-scan` biến nó thành mã thoát.
#
# Khớp sau khi chuẩn hoá NFC + casefold + gộp khoảng trắng. Ở đây chuẩn hoá là
# ĐÚNG HƯỚNG (ngược với vân tay văn xuôi): khớp rộng chỉ làm adapter phải viết
# lại cho mỏng hơn, tức là sai về phía an toàn.
FORBIDDEN_DOCTRINE_PHRASES = {
    "nguong-so-stop-conditions": [
        "3 attempt/packet",
        "45 phút/run",
        "tối đa 20 packet",
        "độ sâu kế nhiệm 5",
        "30 agent invocation",
        "360 cloud minute",
        "max_attempts_per_packet",
        "same_failure_limit",
        "max_run_minutes",
        "max_agent_invocations",
        "max_successor_depth",
        "max_parallel_workers",
    ],
    "ten-state-machine-day-du": [
        "proposed → ready → leased → running → reviewing → accepted → integrated → landed",
        "paused | blocked | cancelled | stale",
    ],
    "bang-vai-tro-muc-2": [
        "dispatcher/reconciler",
        "local controller",
        "land operator",
        "apply job",
        "người có thẩm quyền",
        "phiên land",
        # Ô nội dung của bảng vai trò — tên vai không thôi thì quá hẹp, vì chép
        # cả DÒNG mới là chép doctrine.
        "sửa đúng effective write set trên branch của generation",
        "reconcile durable inbox, chuyển state, cấp/thu hồi lease",
        "đọc code, chạy kiểm tra read-only trên exact sha",
        "start/pause/resume/reroute/override/authorize/apply/deploy",
    ],
    "dinh-nghia-trang-thai-hoan-tat": [
        "merged: pr đã vào nhánh đích",
        "integrated: packet pr đã vào mission integration branch",
        "landed: kết quả đã vào canonical",
        "complete: toàn mission đã readback canonical",
    ],
}

# --- (c2) hạng NGÔN NGỮ THƯỜNG — ĐÃ BỎ ở revision 4 ---------------------------
#
# Từng có một hạng riêng cho cụm danh từ tiếng Việt phổ thông, được tha khi bị ngắt
# qua dòng trong văn xuôi kể lại một phép đo. Revision 4 BỎ HẲN nó: danh sách cấm
# không còn miễn trừ nào, ở bất kỳ hình dạng nào.
#
# VÌ SAO BỎ — sáu lượt cross-review, mỗi lượt một xấp xỉ hẹp hơn, mỗi xấp xỉ vẫn có
# phản ví dụ đo được:
#     "có ngữ cảnh doctrine"        -> heading trần lọt          (lượt 6)
#     "không nằm gọn trong một dòng" -> heading ngắt dòng lọt     (lượt 7)
#     "có chữ ở hai phía"            -> wrapper hai ký tự lọt     (lượt 9)
#     "có dấu hiệu phép đo"          -> phân số trong văn xuôi lọt (lượt 10)
# Reviewer lượt 10 nói thẳng: tiếp tục thêm marker từ vựng chỉ DỜI cửa lọt. Con lắc
# sáu lần đánh quá là con lắc của MIỄN TRỪ, không phải của bản vá.
#
# Chỗ DUY NHẤT trên cây đã merge từng cần miễn trừ là `CLAUDE.md` dòng 82 của master.
# Nó được xử lý bằng cách VIẾT LẠI CÂU (`c44b2d4`, land qua PR #129 thành `18da1da`),
# cross-review duyệt, không finding. Một cơ chế không còn người dùng là một cơ chế
# chưa ai kiểm — nên nó bị xoá thay vì để mục trong tệp.
#
# HỢP ĐỒNG MỚI, một câu: adapter cần kể lại một phép đo có chứa cụm cấm thì VIẾT LẠI
# CÂU. Cái giá khai thẳng — văn xuôi thật kể lại phép đo, có cụm cấm ngắt dòng, nay ĐỎ.
#
# NẾU MỘT REVISION SAU MỞ LẠI MIỄN TRỪ, ba lớp lỗi này quay lại ngay và đây là danh
# sách kiểm sẵn (cả ba đã đo, cả ba tự đóng khi bỏ miễn trừ):
#     doctrine-indented-code-block-bypass          khối mã thụt lề CommonMark
#     doctrine-comment-erases-fence-closer-bypass  comment xoá rào đóng thật
#     doctrine-html-table-token-context-bypass     token bảng trong script/thuộc tính


def _cung_hoa_stdout() -> None:
    """Ép stdout/stderr về UTF-8 để lệnh không chết khi bị CAPTURE.

    Lỗi THẬT đã đo ở vòng review 3: chạy qua subprocess có capture stdout dưới
    codepage không phải UTF-8, `next-comment` cho rc=1 và stdout RỖNG với
    `UnicodeEncodeError: 'charmap' codec can't encode character`. Nghĩa là lệnh
    trung tâm của "mọi transition ghi comment" không chạy được bằng đúng cách
    adapter hướng dẫn. Không có dòng này thì mọi ca cp1252/cp1258 đỏ lại.
    """
    for luong in (sys.stdout, sys.stderr):
        try:
            luong.reconfigure(encoding="utf-8", errors="backslashreplace")
        except Exception:  # pragma: no cover - nền quá cũ thì thà chạy tiếp
            pass


# --- chuẩn hoá doctrine: MỘT MỐI cho CẢ HAI VẾ so khớp -------------------------
#
# VÌ SAO VIẾT LẠI CẢ TẦNG, KHÔNG VÁ THÊM MỘT LỚP (AC 18):
# `doctrine-scan` đã thua NĂM vòng liên tiếp, mỗi vòng một hình dạng ký tự mới
# (dấu `.` → `==`/`!=`/`!` → nháy ngược Markdown → ZWSP + HTML entity → ký tự
# tương thích toàn rộng). Mỗi lần vá đúng hình dạng vừa bị chỉ ra, lần sau lộ
# hình dạng kế tiếp. Nên revision 3 CẤM cách vá theo hình dạng: phải xuất DANH
# SÁCH ĐÓNG các lớp trước, rồi vá MỘT LƯỢT ở tầng cho cả danh sách.
#
# Danh sách đóng đã đo trên bản CHƯA VÁ (40 ca, 18 LỌT). Spec chỉ nêu lớp NFKC;
# đo ra thêm 5 nhóm nữa mà spec KHÔNG nêu — đồng tự Cyrillic/Hy Lạp, nháy cong
# xen giữa, biến thể mũi tên/dash, tag+comment HTML, link Markdown, backslash
# escape. Vá riêng NFKC sẽ đóng 6/18 và để lại 12.

# Bỏ HẲN: trang trí Markdown và mọi loại nháy. Nháy cong `’` xen giữa từ
# (`mer’ged`) là một lớp lách đã đo — bỏ nháy làm nó vô hiệu.
_BO_HAN = str.maketrans("", "", "`*~\"'\u2018\u2019\u201a\u201b\u201c\u201d\u201e\u201f")

# Quy về MỘT khoảng trắng: gạch dưới, mọi biến thể hyphen/dash, khoảng trắng
# không ngắt. GỘP chứ KHÔNG XOÁ — bản trước xoá `_`, nên `same_failure_limit`
# thành `samefailurelimit` còn `same failure limit` giữ nguyên khoảng trắng:
# HAI CHUỖI KHÔNG KHỚP NHAU, trái hẳn điều chú thích bản trước tuyên bố. Gộp về
# khoảng trắng làm `_`, `-`, en-dash và khoảng trắng thành MỘT mối thật, và giữ
# nguyên ranh giới từ nên không mở thêm cửa cho dương tính giả.
_PHAN_CACH = {ord(c): " " for c in "_\u00a0-\u2010\u2011\u2012\u2013\u2014\u2015\u2212"}

# Đồng tự Cyrillic/Hy Lạp → Latin. Chỉ chữ THƯỜNG (chạy SAU casefold) và chỉ
# những chữ TRÙNG HÌNH, không gấp bừa cả bảng chữ cái — gấp rộng sẽ băm nát văn
# bản Nga/Hy Lạp thật và sinh dương tính giả (ca O5/O6 giữ chiều này).
_DONG_TU = str.maketrans({
    "\u0430": "a", "\u0432": "b", "\u0435": "e", "\u043a": "k", "\u043c": "m",
    "\u043d": "h", "\u043e": "o", "\u0440": "p", "\u0441": "c", "\u0442": "t",
    "\u0443": "y", "\u0445": "x", "\u0456": "i", "\u0458": "j", "\u0455": "s",
    "\u04bb": "h", "\u0501": "d", "\u051b": "q", "\u051d": "w",
    "\u03b1": "a", "\u03b5": "e", "\u03b9": "i", "\u03ba": "k", "\u03bd": "v",
    "\u03bf": "o", "\u03c1": "p", "\u03c4": "t", "\u03c5": "u", "\u03c7": "x",
})

# Biến thể mũi tên → `→`. Dòng state machine của protocol dùng `→`; một mũi tên
# DÀI `⟶` render gần như y hệt nhưng NFKC không gộp.
_MUI_TEN = str.maketrans({
    "\u27f6": "\u2192", "\u21d2": "\u2192", "\u27f9": "\u2192",
    "\u2794": "\u2192", "\u279c": "\u2192", "\u2799": "\u2192",
    "\u2b95": "\u2192", "\u21fe": "\u2192",
})

# Comment HTML: `mer<!-- x -->ged` render ra `merged`.
_RE_COMMENT_HTML = re.compile(r"<!--.*?-->", re.DOTALL)
# Tag HTML: `mer<b>ged</b>` render ra `merged`. ĐÒI tên tag NGAY SAU `<` (không
# cho khoảng trắng chen vào), nên `a < b > c` trong một mẫu shell KHÔNG bị coi là
# tag — đó là ràng buộc bắt-oan O8 của lớp này.
#
# Finding `doctrine-html-quoted-angle-bypass` (cross-review lượt 6, codex): bản
# trước dùng `[^<>]*` cho phần thuộc tính, tức CẤM ký tự `>` theo VỊ TRÍ. Nhưng
# `>` nằm hợp lệ trong một giá trị thuộc tính có nháy, nên
# `mer<span title=">">ged:</span>` không khớp regex ⇒ tag không bị gỡ ⇒ `rc=0`,
# trong khi trình duyệt render ra đúng cụm cấm. Đã ĐO trên `e6e4b73`: rc=0, còn
# tag thường và ASCII trần đều rc=6.
#
# Chữa đúng tầng: phân tích phần thuộc tính theo CẤU TRÚC — chuỗi trong nháy kép,
# chuỗi trong nháy đơn, hoặc ký tự thường — thay vì cấm một ký tự. Cùng cách này
# xử lý luôn `<` trong thuộc tính (lớp I3), thứ bản trước cũng để lọt.
_RE_TAG_HTML = re.compile(
    r"""</?[A-Za-z][A-Za-z0-9-]*"""      # `<tag` hoặc `</tag`
    r"""(?:\s+(?:"[^"]*"|'[^']*'|[^>"'])*)?"""  # thuộc tính: nháy kép | nháy đơn | ký tự thường
    r"""\s*/?>""",                        # `>` hoặc `/>`
    re.VERBOSE,
)
# Link/ảnh Markdown: `[merged](#a)` render ra `merged`. Phần đích cho phép MỘT cấp
# ngoặc lồng — `[merged](#a(b))` là link hợp lệ trong Markdown, và bản trước dùng
# `[^()\n]*` nên không khớp, tag không bị rút, cụm cấm lọt (lớp I6, đã ĐO rc=0).
_RE_LINK_MD = re.compile(r"!?\[([^\]\n]*)\]\((?:[^()\n]|\([^()\n]*\))*\)")
_RE_LINK_REF = re.compile(r"!?\[([^\]\n]*)\]\[[^\]\n]*\]")
# Backslash escape: `merged\:` render ra `merged:`.
_RE_ESCAPE = re.compile(r"\\([!-/:-@\[-`{-~])")


def _chuan_hoa(text: str) -> str:
    """Quy một đoạn văn bản về DẠNG HIỂN THỊ, để so khớp doctrine.

    Dùng CHỈ cho doctrine-scan, và áp cho **CẢ HAI VẾ** — văn bản quét lẫn cụm
    cấm đều đi qua đúng hàm này. Ở đây chuẩn hoá rộng là ĐÚNG HƯỚNG, ngược hẳn
    với phép đếm finding: khớp rộng chỉ buộc adapter viết mỏng hơn (sai về phía
    an toàn), còn khớp rộng ở finding-id sẽ gộp oan hai lỗi khác nhau.

    Thứ tự các bước CÓ LÝ DO, đừng đảo:

      1. bỏ comment HTML, rồi bỏ tag HTML;
      2. rút text của link/ảnh Markdown, gỡ backslash escape;
      3. `html.unescape` — ĐẶT SAU bước 1 có chủ đích: `&lt;b&gt;` hiển thị
         NGUYÊN VĂN `<b>` chứ không phải một tag, nên nó phải thoát khỏi bước bỏ
         tag trước rồi mới được giải;
      4. **NFKC**, không phải NFC. NFC theo ĐỊNH NGHĨA không đụng tới ký tự
         tương thích, nên `：` toàn rộng, `ｍｅｒｇｅｄ`, `③`, `³`, `／`, `＿`, `｜`
         đều lọt. Đây là sai ở LỰA CHỌN DẠNG CHUẨN, không phải sót một trường hợp;
      5. bỏ ký tự hạng `Cf` (ZWSP/ZWNJ/ZWJ/WORD JOINER/soft hyphen/BOM);
      6. `casefold`, rồi gấp đồng tự (chỉ chữ thường), gấp mũi tên;
      7. bỏ trang trí + nháy, gộp phân cách về khoảng trắng, gộp khoảng trắng.

    AN TOÀN — `html.unescape` giải entity ĐÚNG MỘT LẦN (một lượt quét tuyến tính
    trên chuỗi GỐC, không quét lại phần vừa thay), KHÔNG lặp tới điểm bất động.
    Giải LẶP sẽ biến `&amp;#58;` — thứ hiển thị NGUYÊN VĂN `&#58;`, KHÔNG phải
    dấu hai chấm — thành dấu hai chấm thật và sinh DƯƠNG TÍNH GIẢ trên cụm
    `merged: ...`. Đã ĐO: `html.unescape("&amp;#58;")` → `"&#58;"`.
    """
    # KHÔNG gỡ comment/tag HTML ở đây: việc đó làm TRỌN ở `_dong_sau_khi_go`, tầng
    # duy nhất thấy được cấu trúc trải nhiều dòng. Để hai nơi cùng gỡ thì một đột
    # biến gỡ chốt ở nơi này vẫn xanh nhờ nơi kia — bộ test mất độ phân giải, đúng
    # bệnh `ac18-mutation-not-per-class` mà cross-review lượt 6 vừa bắt.
    text = _RE_LINK_MD.sub(r"\1", text)
    text = _RE_LINK_REF.sub(r"\1", text)
    text = _RE_ESCAPE.sub(r"\1", text)
    text = html.unescape(text)
    text = unicodedata.normalize("NFKC", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Cf")
    text = text.casefold().translate(_DONG_TU).translate(_MUI_TEN)
    text = text.translate(_BO_HAN).translate(_PHAN_CACH)
    return " ".join(text.split())


def _dong_sau_khi_go(raw: str):
    """Gỡ comment/tag HTML — KỂ CẢ loại trải nhiều dòng — trả `[(số dòng, text)]`.

    Vì sao phải làm ở tầng này chứ không trong `_chuan_hoa`: `_chuan_hoa` chạy theo
    TỪNG DÒNG, nên một tag mở ở dòng này đóng ở dòng sau không nằm gọn trong dòng
    nào cả và KHÔNG BAO GIỜ khớp regex. Đã ĐO trên `e6e4b73`, cả hai lọt `rc=0`:

        mer<span                          |  mer<!--
          class="x">ged: PR đã vào…       |    ghi chú
                                          |  -->ged: PR đã vào…

    VÀ PHẢI NUỐT LUÔN XUỐNG DÒNG. Bản vá đầu của lượt này thay vùng bị gỡ bằng đúng
    số `\\n` nó chứa, định giữ số dòng cho thông điệp lỗi. Đo lại thì vẫn lọt: chỗ
    nối hai mảnh thành `mer ged`, trong khi trình duyệt render `merged` LIỀN — xuống
    dòng nằm bên trong một tag không phải chỗ ngắt từ. Giữ số dòng bằng cách ấy là
    đổi một lỗ lấy một lỗ.
    Nên: nuốt cả xuống dòng, và mang số dòng theo bằng bản đồ — dòng ra mang số của
    dòng nó BẮT ĐẦU. Thông điệp `tệp:dòng` vẫn chỉ đúng chỗ.
    """
    vung = []
    for rx in (_RE_COMMENT_HTML, _RE_TAG_HTML):
        vung.extend(m.span() for m in rx.finditer(raw))
    vung.sort()
    gop: list[list[int]] = []
    for s, e in vung:
        if gop and s <= gop[-1][1]:
            gop[-1][1] = max(gop[-1][1], e)
        else:
            gop.append([s, e])

    ket, cur, cur_dong, so_dong, gi = [], [], None, 1, 0
    for i, ch in enumerate(raw):
        while gi < len(gop) and gop[gi][1] <= i:
            gi += 1
        trong_vung = gi < len(gop) and gop[gi][0] <= i < gop[gi][1]
        if ch == "\n":
            if not trong_vung:                    # xuống dòng THẬT: chốt dòng lại
                ket.append((cur_dong or so_dong, "".join(cur)))
                cur, cur_dong = [], None
            so_dong += 1                          # nằm trong vùng gỡ ⇒ nối tiếp
            continue
        if trong_vung:
            continue
        if cur_dong is None:
            cur_dong = so_dong
        cur.append(ch)
    if cur:
        ket.append((cur_dong or so_dong, "".join(cur)))
    return ket


def _phang_ca_tep(raw: str):
    """Ép CẢ TỆP về một chuỗi chuẩn hoá, kèm bản đồ vị trí → số dòng.

    Vì sao không so từng dòng: quét theo DÒNG VẬT LÝ thì một câu doctrine bị
    xuống dòng theo lối Markdown bình thường sẽ lọt sạch — đã ĐO, 3/3 cụm thử
    (state machine ngắt trước "accepted", định nghĩa `merged`, ô bảng vai trò)
    đều cho rc=0. Ngắt dòng là thứ người viết làm vô thức, nên chốt nào thua nó
    thì thua thường xuyên, không phải hiếm.

    Đây là lớp lách THỨ HAI liên tiếp bị bắt ở cùng một cơ chế (trước đó là dấu
    nháy ngược). Nên lần này chữa tận gốc: so trên VĂN BẢN LOGIC, không phải trên
    cách nó được bẻ dòng.
    """
    # Gỡ cấu trúc TRẢI NHIỀU DÒNG trước: vòng lặp dưới chuẩn hoá theo từng dòng nên
    # không thấy được thứ bắc cầu qua hai dòng (lớp I4/I5).
    phang, khuc = _khuc_chuan(_dong_sau_khi_go(raw))
    return phang, [(bat_dau, so_dong) for bat_dau, _het, so_dong, _n in khuc]



_RE_DAU_DONG = re.compile(r"^\s*(?:#{1,6}|>+|[-*+]|\d+[.)])\s*")
def _go_dau_dong(s: str) -> str:
    """Gỡ dấu đầu dòng Markdown lặp tới hết (`> - `, `## `, `1. `)."""
    truoc = None
    while truoc != s:
        truoc = s
        s = _RE_DAU_DONG.sub("", s, count=1)
    return s


def _khuc_chuan(dong_sach):
    """Nối các dòng ĐÃ GỠ DẤU ĐẦU DÒNG thành một chuỗi, kèm khúc của từng dòng.

    VÌ SAO GỠ DẤU ĐẦU DÒNG Ở ĐÂY — lượt review 7 đóng được heading và bullet
    nhưng ba ca trích dẫn vẫn lọt, và lý do KHÁC hẳn: `_chuan_hoa("> Người có")`
    giữ nguyên dấu `>`, nên chuỗi phẳng ra `> người có > thẩm quyền` và cụm cấm
    KHÔNG khớp một lần nào. Không phải miễn trừ tha nhầm — là scanner không thấy.
    Đo được: `'người có thẩm quyền' in _phang_ca_tep('> Người có\n> thẩm quyền')`
    trả `False`. Dấu `-` thì tình cờ bị `_PHAN_CACH` nuốt, `>` `#` `1.` thì không;
    lỗ này chỉ tồn tại nhờ sự KHÔNG NHẤT QUÁN ấy.

    Gỡ ở tầng phẳng hoá — dùng chung cho cả quét lẫn miễn trừ — thì hai nơi không
    thể lệch nhau. Lệch nhau là đúng cái bẫy: miễn trừ tính offset trên một chuỗi,
    quét tìm trên một chuỗi khác, và số dòng trong thông điệp lỗi trỏ sai chỗ.
    """
    phan, khuc, vi_tri = [], [], 0
    for so_dong, dong in dong_sach:
        n = _go_dau_dong(_chuan_hoa(dong))
        if not n:
            continue
        if phan:
            phan.append(" ")
            vi_tri += 1
        khuc.append((vi_tri, vi_tri + len(n), so_dong, n))
        phan.append(n)
        vi_tri += len(n)
    return "".join(phan), khuc


def _dong_tai(ban_do, offset: int) -> int:
    """Vị trí trong chuỗi phẳng → số dòng gốc gần nhất."""
    so = ban_do[0][1] if ban_do else 0
    for bat_dau, so_dong in ban_do:
        if bat_dau > offset:
            break
        so = so_dong
    return so


def _doc_anh_moi_truong(duong):
    if not duong or not Path(duong).is_file():
        return None, f"không có ảnh môi trường: {duong!r}"
    try:
        d = json.loads(Path(duong).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return None, f"ảnh môi trường không đọc được ({type(e).__name__})"
    if not isinstance(d, dict) or not {"thieu_bat_buoc", "chua_xac_thuc", "he_dieu_hanh"} <= d.keys():
        return None, "ảnh môi trường thiếu trường của `doctor --json`"
    return d, ""


def _kiem_anh_moi_truong(duong, can_sach: bool, d=None, *, kiem_tuoi=True) -> dict:
    """Nền dùng chung; tuổi chỉ ở begin-attempt, nơi touch vẫn qua mặt được."""
    d, loi = _doc_anh_moi_truong(duong) if d is None else (d, "")
    if not isinstance(d, dict) or not {"thieu_bat_buoc", "chua_xac_thuc", "he_dieu_hanh"} <= d.keys():
        d, loi = None, "ảnh môi trường thiếu trường của `doctor --json`"
    if d is None:
        _die(RC_MOI_TRUONG, f"KHÔNG ĐỌC ĐƯỢC: {loi}")
    if d["he_dieu_hanh"] != platform.system():
        _die(RC_MOI_TRUONG, f"ảnh thuộc nền khác: {d['he_dieu_hanh']!r}")
    if kiem_tuoi and (tuoi := time.time() - Path(duong).stat().st_mtime) > NGUONG_TUOI_BANG_CHUNG_GIAY:
        _die(RC_MOI_TRUONG, f"ảnh môi trường cũ {int(tuoi)}s — chụp lại `doctor --json`")
    if can_sach and (d.get("thieu_bat_buoc") or []):
        _die(RC_MOI_TRUONG, f"môi trường thiếu công cụ: {d['thieu_bat_buoc']}")
    return d


def _kiem_bang_chung_may(duong, ly_do: str, anchor: dict, hmac_key: str) -> None:
    """Nhận ảnh doctor tươi hoặc run.json buộc đúng lượt; không tin một trường rời."""
    if not isinstance(hmac_key, str) or not re.fullmatch(r"[0-9a-f]{64}", hmac_key):
        _die(RC_MOI_TRUONG, "state thiếu/hỏng khoá toàn vẹn của lượt")
    try:
        d = json.loads(Path(duong).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        _die(RC_MOI_TRUONG, f"KHÔNG ĐỌC ĐƯỢC bằng chứng máy: {type(e).__name__}")
    if not isinstance(d, dict) or not d.get("nonce") or not d.get("chu_ky"):
        _die(RC_MOI_TRUONG, "bằng chứng máy không có neo lượt — dùng "
             "`--khong-co-bang-chung` (có ghi sổ)")
    if isinstance(d, dict):
        if d["nonce"] != anchor["nonce"]:
            _die(RC_MOI_TRUONG, "neo thuộc lượt khác")
        if not isinstance(d["chu_ky"], str) or not re.fullmatch(r"[0-9a-f]{64}", d["chu_ky"]):
            _die(RC_MOI_TRUONG, "bản ghi đã bị sửa sau khi launcher ghi")
        try:
            mong = ky_ban_ghi_luot(d, hmac_key)
        except (TypeError, ValueError):
            _die(RC_MOI_TRUONG, "bản ghi đã bị sửa sau khi launcher ghi")
        if not hmac.compare_digest(d["chu_ky"], mong):
            _die(RC_MOI_TRUONG, "bản ghi đã bị sửa sau khi launcher ghi")
        if "trang_thai" in d or "run_id" in d:
            if d.get("void_reason") != ly_do:
                _die(RC_MOI_TRUONG, f"bản ghi buộc cho {d.get('void_reason')!r}, không phải {ly_do!r}")
            if d.get("trang_thai") not in ("qua_han", "hong"):
                _die(RC_MOI_TRUONG, "bản ghi không mang phán quyết lỗi hạ tầng")
            return
    d = _kiem_anh_moi_truong(duong, can_sach=False, d=d, kiem_tuoi=False)
    truong = "thieu_bat_buoc" if ly_do == "infrastructure" else "chua_xac_thuc"
    if not (d.get(truong) or []):
        _die(RC_MOI_TRUONG, f"ảnh doctor không chứng minh {ly_do!r}")


def _die(rc: int, msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(rc)


def _state_path(state_dir: Path, packet: int) -> Path:
    return state_dir / f"wp{packet}.json"


def _load(state_dir: Path, packet: int) -> dict:
    p = _state_path(state_dir, packet)
    if not p.exists():
        _die(RC_STATE, f"chưa có state cho packet {packet} — chạy `init` trước ({p})")
    return json.loads(p.read_text(encoding="utf-8"))


def _save(state_dir: Path, st: dict) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    p = _state_path(state_dir, st["packet"])
    p.write_text(
        json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _kiem_chuyen(st: dict, den: str) -> None:
    hien = st["state"]
    if den not in CHUYEN_HOP_LE.get(hien, ()):
        _die(
            RC_STATE,
            f"transition không hợp lệ: {hien} → {den} "
            f"(hợp lệ từ {hien}: {', '.join(CHUYEN_HOP_LE.get(hien, ())) or 'không còn'})",
        )


def _tieu_thu_comment_id(st: dict, comment_id: str | None, cho: str) -> dict:
    """Đòi một ID comment ĐÃ ĐĂNG KÝ, đúng transition, và CHƯA dùng.

    Vì sao không kiểm URL bằng regex: vòng 1 nhận chuỗi bất kỳ, vòng 2 lọt ".."
    và repo khác, vòng 3 lọt alias `pull`/`issues` và số 0 đứng đầu. Regex trên
    URL không bao giờ chứng minh được comment CÓ THẬT — luôn còn một alias nữa.

    KHAI THẲNG GIỚI HẠN: tiến trình này KHÔNG gọi mạng, nên nó KHÔNG xác minh
    được ID có tồn tại trên GitHub hay không. Đây là SỔ TAY, không phải xác minh.
    Thứ nó BẢO ĐẢM chỉ gồm hai điều, và đừng đọc nó rộng hơn thế:
      1. ID phải được ghi vào sổ bằng `record-post` TRƯỚC — ID chưa từng ghi bị
         từ chối, nên không dán đại một con số vào `transition` được;
      2. mỗi ID dùng đúng MỘT lần cho ĐÚNG transition đã khai — không tái sử
         dụng một comment thật để tiêu thụ hai transition.
    """
    if not comment_id:
        _die(RC_TRACE, f"thiếu --comment-id: transition '{cho}' phải có dấu vết bền đã đăng")
    so = st["posts"].get(comment_id)
    if so is None:
        _die(
            RC_TRACE,
            f"comment id {comment_id!r} chưa có trong sổ — đăng comment rồi ghi lại bằng "
            f"`record-post --for {cho} --comment-id <id GitHub trả về>`",
        )
    if so["for"] != cho:
        _die(
            RC_TRACE,
            f"comment id {comment_id!r} đã đăng ký cho transition {so['for']!r}, "
            f"không dùng lại cho {cho!r} được",
        )
    if so["consumed_by"] is not None:
        _die(
            RC_TRACE,
            f"comment id {comment_id!r} đã bị tiêu thụ bởi transition {so['consumed_by']!r} "
            f"— mỗi ID chỉ dùng MỘT lần",
        )
    return so


# --- lệnh ---------------------------------------------------------------------


def cmd_init(a, state_dir: Path) -> int:
    if a.executor not in PROVIDERS or a.reviewer not in PROVIDERS:
        _die(RC_ARG, f"provider phải thuộc {PROVIDERS}")
    # Cross-provider: chặn NGAY từ init, không đợi tới lúc ghi review.
    if a.executor == a.reviewer:
        _die(
            RC_PROVIDER,
            f"executor và reviewer cùng là {a.executor!r} — mặc định phải khác nền "
            f"(mức assurance khác nhau, xem protocol §8)",
        )
    p = _state_path(state_dir, a.packet)
    # KHÔNG có `--force-new`, và đừng thêm lại. Cờ đó ghi đè state cũ nên nó xoá
    # sạch attempts_used/finding_counts và đưa một packet ĐÃ blocked về leased —
    # tức là đường vòng qua đúng cái trần mà tệp này tồn tại để cưỡng chế. Tiến
    # trình này không biết revision/generation và không có uỷ quyền của bên điều
    # phối, nên nó KHÔNG phân biệt được reroute hợp lệ với hồi sinh một lease đã
    # cạn. Reroute là việc của bên điều phối: cấp generation mới với state-dir mới.
    if p.exists():
        _die(
            RC_STATE,
            f"state đã tồn tại: {p}. Không ghi đè — reroute phải là generation mới "
            f"do bên điều phối cấp, với --state-dir mới.",
        )
    st = {
        "schema_version": 1,
        "packet": a.packet,
        "mission": a.mission,
        "executor": a.executor,
        "reviewer": a.reviewer,
        # `awaiting_lease`, KHÔNG phải `leased`. Bản trước ghi thẳng `leased` ở đây,
        # nghĩa là bất kỳ ai gõ được `init` đều tự cấp cho mình một lease hợp lệ rồi
        # `begin-attempt` sang `running` — đường vòng qua đúng doctrine "không tự cấp
        # lease", và acceptance #55 r2 đòi chặn TỪ init. Review cross-provider
        # (codex, 14-08-2026) tái hiện được bằng `init --packet 999999 --mission
        # 888888`: rc=0, state `leased`. `init` chỉ khai HÌNH DẠNG của packet; uỷ
        # quyền là chuyện của `record-lease`.
        "state": "awaiting_lease",
        "lease": None,
        "attempts_used": 0,
        "attempts_limit": a.attempts_limit,
        "same_failure_limit": a.same_failure_limit,
        "finding_counts": {},
        "attempt_open": False,
        "attempt_anchor": None,
        "hmac_key": secrets.token_hex(32),
        "reviewing_head_sha": None,
        "accepted_sha": None,
        "reviews": [],
        "posts": {},
        "history": [],
    }
    _save(state_dir, st)
    print(
        f"đã khởi tạo packet {a.packet} (mission {a.mission}) — "
        f"executor {a.executor}, reviewer {a.reviewer}, state {st['state']}"
    )
    return RC_OK


def _doc_han_utc(chuoi: str) -> datetime:
    """Đọc mốc UTC dạng ISO8601. Sai dạng thì CHẶN, không đoán."""
    s = (chuoi or "").strip()
    if not s:
        _die(RC_ARG, "--expires-utc rỗng")
    try:
        d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        _die(RC_ARG, f"--expires-utc không đọc được: {chuoi!r} "
                     f"(cần ISO8601, ví dụ 2026-08-13T18:30:00Z)")
    if d.tzinfo is None:
        # KHÔNG đoán múi giờ của người gõ: "hết hạn 18:30" mà không nói múi là hai
        # mốc cách nhau tới 26 giờ. Một lease sai 26 giờ thì chốt hạn thành trang trí.
        _die(RC_ARG, f"--expires-utc phải kèm múi giờ (thêm 'Z'): {chuoi!r}")
    return d.astimezone(timezone.utc)


# Cửa sổ hạn hợp lệ của một lease. Chặn `expires_utc` năm 9999 — một lease sống
# tới năm 9999 làm chốt hạn thành trang trí, mà bản trước nhận nó (`rc=0`).
GIOI_HAN_HAN_NGAY = 366
KHOA_LEASE = ("lease_id", "granted_by", "evidence", "expires_utc")


def _kiem_luoc_do_lease(lease, rc_hinh_dang: int) -> dict:
    """HÀM KIỂM CHUNG — nguồn sự thật DUY NHẤT về lược đồ lease (AC 21).

    `record-lease` và `begin-attempt` gọi ĐÚNG hàm này trên ĐÚNG một cấu trúc.
    Bản trước để hai chỗ tự kiểm rời nhau: `record-lease` đòi đủ bốn khoá, còn
    `begin-attempt` chỉ đòi `lease` truthy VÀ có `expires_utc` — nên nó nhận một
    state mà `record-lease` KHÔNG BAO GIỜ sinh ra được. Đã ĐO trên bản trước:
    11 hình dạng sai LỌT (`rc=0`) và 5 hình dạng vỡ thành TRACEBACK THÔ (`rc=1`),
    trong đó có cả lease TỰ CẤP (`granted_by: "claude"`) và lease cấp bởi tên
    ngoài allowlist — hai thứ `record-lease` chặn thẳng. Đó là finding
    `partial-lease-authority-bypass`.

    `rc_hinh_dang` chỉ nói lỗi ĐẾN TỪ ĐÂU, không đổi phép kiểm: `record-lease`
    nhận từ đối số dòng lệnh (`RC_ARG`), `begin-attempt` đọc từ state trên đĩa
    (`RC_STATE`). Lỗi thẩm quyền luôn `RC_GUARD`, lỗi mốc thời gian luôn `RC_ARG`,
    lease chết luôn `RC_STATE` — giống hệt nhau ở cả hai đường gọi.

    Mọi hình dạng sai thoát CÓ KIỂM SOÁT. KHÔNG traceback: một chốt vỡ bằng
    traceback là chốt chưa fail-closed, nó chỉ đang vỡ.
    """
    if isinstance(lease, bool) or not isinstance(lease, dict):
        _die(rc_hinh_dang,
             f"'lease' phải là một đối tượng có đủ {list(KHOA_LEASE)}; "
             f"nhận được kiểu {type(lease).__name__!r}. State thiếu/hỏng lease là "
             f"CŨ hoặc BỊ SỬA TAY — KHÔNG mở lượt ngầm trên nó.")
    thieu = [k for k in KHOA_LEASE if k not in lease]
    if thieu:
        _die(rc_hinh_dang,
             f"'lease' thiếu khoá {thieu} — lược đồ đủ là {list(KHOA_LEASE)}. "
             f"Kiểm SỰ TỒN TẠI một khoá không phải kiểm TRỌN LƯỢC ĐỒ.")
    # KHOÁ THỪA cũng là lược đồ SAI — cross-review lượt 9, finding
    # `lease-schema-allows-extra-keys`. Bản trước chỉ kiểm THIẾU, nên một state có đủ
    # bốn khoá cộng `unexpected: true` vẫn mở được lượt (`rc=0`). Đó lặp lại ĐÚNG tiêu
    # chí mà AC 21 đặt ra để bắt bệnh cũ: `begin-attempt` nhận một state mà
    # `record-lease` KHÔNG BAO GIỜ sinh ra được — nó chỉ dựng đúng bốn khoá này.
    #
    # Lược đồ khép kín thì phải khép CẢ HAI chiều. Khoá thừa tuy hiện bị bỏ qua nên
    # chưa thành đường lách quyền, nhưng nó là chỗ để một trường lạ nằm im trong state
    # rồi được đọc bởi một phiên bản sau — bịt trước rẻ hơn bịt sau.
    thua = [k for k in lease if k not in KHOA_LEASE]
    if thua:
        _die(rc_hinh_dang,
             f"'lease' có khoá THỪA {sorted(thua)} — lược đồ đủ là {list(KHOA_LEASE)}, "
             f"không hơn. `record-lease` chỉ sinh ra đúng bốn khoá ấy, nên một state "
             f"mang khoá lạ là state BỊ SỬA TAY, không phải state do đường hợp lệ tạo.")
    for k in ("lease_id", "granted_by", "evidence"):
        v = lease[k]
        if not isinstance(v, str):
            _die(rc_hinh_dang,
                 f"'lease.{k}' phải là chuỗi, nhận kiểu {type(v).__name__!r}")
        if not v.strip():
            _die(rc_hinh_dang, f"'lease.{k}' rỗng")
    nguoi_cap = lease["granted_by"].strip()
    # Chốt CỐT LÕI, giữ nguyên thứ tự của bản trước để thông điệp gọi đúng tên
    # bệnh: chốt PROVIDERS trước, chốt allowlist sau. Một agent tự ký cho chính
    # mình thì thứ ghi ra không phải lease, chỉ là lời tự khai đội lốt uỷ quyền.
    if nguoi_cap.lower() in PROVIDERS:
        _die(RC_GUARD,
             f"--granted-by {nguoi_cap!r} là tên một provider — agent KHÔNG tự cấp lease "
             f"cho mình được (xem doctrine 'không tự cấp lease')")
    if unicodedata.normalize("NFC", nguoi_cap).lower() not in NGUOI_CO_THAM_QUYEN:
        _die(RC_GUARD,
             f"--granted-by {nguoi_cap!r} KHÔNG nằm trong danh sách người có thẩm quyền "
             f"{list(NGUOI_CO_THAM_QUYEN)} — danh sách CẤM không bao giờ đủ (cross-review "
             f"14-08-2026, finding lease-authority-spoof), nên chốt này đòi tên phải ĐƯỢC "
             f"PHÉP chứ không chỉ 'không bị cấm'. Thêm người cấp mới = sửa "
             f"NGUOI_CO_THAM_QUYEN qua một commit có review.")
    exp = lease["expires_utc"]
    if not isinstance(exp, str):
        _die(rc_hinh_dang,
             f"'lease.expires_utc' phải là chuỗi ISO8601, nhận kiểu {type(exp).__name__!r}")
    han = _doc_han_utc(exp)
    bay_gio = datetime.now(timezone.utc)
    if han.year < 1970:
        _die(RC_STATE, f"'lease.expires_utc' trước 1970 ({han.isoformat()}) — mốc vô nghĩa")
    if han <= bay_gio:
        _die(RC_STATE,
             f"lease hết hạn lúc {han.isoformat()} — không dùng được; xin lease mới, "
             f"đừng coi một lease chết là có quyền")
    if (han - bay_gio).days > GIOI_HAN_HAN_NGAY:
        _die(RC_STATE,
             f"'lease.expires_utc' {han.isoformat()} xa quá {GIOI_HAN_HAN_NGAY} ngày — "
             f"một lease gần như vĩnh viễn làm chốt hạn thành trang trí")
    return {
        "lease_id": lease["lease_id"].strip(),
        "granted_by": nguoi_cap,
        "evidence": lease["evidence"].strip(),
        "expires_utc": han.isoformat(),
    }


def cmd_record_lease(a, state_dir: Path) -> int:
    """GHI HỘ một lease do bên có thẩm quyền cấp — không phải tự cấp.

    Tiến trình này không cấp được lease cho ai. Nó chỉ ghi lại một quyết định đã
    có ở nơi khác, kèm dấu vết bền để đối chiếu. Ba thứ bắt buộc, mỗi thứ bịt một
    đường lách: người cấp (không được là provider), dấu vết (để đối chiếu được),
    và hạn (để lease không sống mãi).
    """
    st = _load(state_dir, a.packet)
    if st["state"] != "awaiting_lease":
        _die(RC_STATE,
             f"chỉ ghi được lease khi packet đang 'awaiting_lease'; hiện là {st['state']!r}. "
             f"Ghi đè lease của một packet đang chạy là hồi sinh một lượt đã cạn.")
    # Dựng ứng viên rồi đưa qua ĐÚNG hàm kiểm chung. Không tự kiểm ở đây nữa —
    # hai chỗ tự kiểm rời nhau CHÍNH LÀ finding `partial-lease-authority-bypass`.
    lease = _kiem_luoc_do_lease(
        {
            "lease_id": a.lease_id,
            "granted_by": a.granted_by,
            "evidence": a.evidence,
            "expires_utc": a.expires_utc,
        },
        RC_ARG,
    )
    st["lease"] = lease
    st["state"] = "leased"
    st["history"].append({"event": "record_lease", "lease_id": lease["lease_id"],
                          "granted_by": lease["granted_by"],
                          "expires_utc": lease["expires_utc"]})
    _save(state_dir, st)
    print(f"đã ghi lease {lease['lease_id']} (cấp bởi {lease['granted_by']}, "
          f"hết hạn {lease['expires_utc']}) — state {st['state']}")
    return RC_OK


def cmd_begin_attempt(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    # Lượt đầu đi từ 'leased'; lượt rework đi từ 'running' sau changes_requested.
    if st["state"] not in ("leased", "running"):
        _die(RC_STATE, f"không mở được lượt từ state {st['state']!r}")
    # FAIL-CLOSED, không fail-open. Bản trước kiểm hạn CHỈ khi `lease` có mặt
    # (`if lease and lease.get("expires_utc")`), nên state thiếu `lease` bỏ qua
    # TOÀN BỘ phép kiểm và lọt thẳng vào 'running'. Finding `legacy-lease-bypass`
    # (cross-review lượt 4, codex, 14-08-2026) tái lập bằng chính state do
    # entrypoint TRƯỚC (`22d2cc9`) sinh ra: `state: leased` mà KHÔNG có trường
    # `lease` — bản đó ghi thẳng `leased` trong `init`, chưa có khái niệm ghi hộ
    # lease riêng. `leased`/`running` mà thiếu `lease` hợp lệ là state CŨ hoặc
    # HỎNG: đường DUY NHẤT vào `leased` là `record-lease` (xem `CHUYEN_HOP_LE`),
    # nên một state ở hai trạng thái này mà không có lease là mâu thuẫn trực tiếp
    # với bất biến đó — chặn, KHÔNG nâng cấp ngầm. Di trú state cũ là việc TƯỜNG
    # MINH, có uỷ quyền của bên điều phối (generation mới + record-lease thật),
    # không phải việc lặng lẽ của `begin-attempt`.
    # ĐÚNG hàm kiểm mà `record-lease` dùng, trên ĐÚNG lược đồ đó. Không có phép
    # kiểm riêng ở đây: mọi state mà hàm này từ chối là state `record-lease`
    # KHÔNG BAO GIỜ sinh ra được, nên nhận nó là mở một đường vòng quanh chính
    # cửa uỷ quyền. Hàm chung cũng kiểm lại THẨM QUYỀN người cấp, vì một lease
    # tự cấp còn nguyên trong state vẫn là lease tự cấp lúc mở lượt.
    _kiem_luoc_do_lease(st.get("lease"), RC_STATE)
    if a.provider != st["executor"]:
        _die(
            RC_PROVIDER,
            f"provider {a.provider!r} không phải executor của packet này ({st['executor']!r})",
        )
    # Một lượt ĐANG MỞ thì không mở thêm được. Thiếu chốt này, gõ `begin-attempt`
    # bốn lần liên tiếp sẽ đốt sạch trần dù chưa lượt nào chạy xong — trần bị
    # tiêu bởi thao tác lặp, không phải bởi công việc thật.
    if st["attempt_open"]:
        _die(
            RC_STATE,
            f"lượt {st['attempts_used']} đang mở — đóng nó bằng một review trước đã. "
            f"Gọi lại begin-attempt không mở lượt mới và không tiêu thêm trần.",
        )
    if st["attempts_used"] >= st["attempts_limit"]:
        st["state"] = "blocked"
        st["history"].append({"event": "blocked_attempts_exhausted", "at_attempt": st["attempts_used"]})
        _save(state_dir, st)
        _die(
            RC_TRAN,
            f"đã dùng hết {st['attempts_used']}/{st['attempts_limit']} lượt — packet về blocked. "
            f"Ghi failure evidence + handoff rồi dừng; reroute là việc của bên điều phối.",
        )
    if not isinstance(st.get("hmac_key"), str) or not re.fullmatch(r"[0-9a-f]{64}", st["hmac_key"]):
        _die(RC_STATE, "state thiếu/hỏng khoá toàn vẹn — không nâng cấp state cũ ngầm")
    anh = _kiem_anh_moi_truong(getattr(a, "bang_chung_moi_truong", None)
                               or os.environ.get(BIEN_BANG_CHUNG), can_sach=True)
    st["attempts_used"] += 1
    st["state"] = "running"
    st["attempt_open"] = True
    # Head cũ hết hiệu lực ngay khi mở lượt mới: có commit mới thì bản duyệt
    # trước không còn nói về cây đang có nữa.
    st["reviewing_head_sha"] = None
    st["attempt_anchor"] = {"attempt": st["attempts_used"], "nonce": secrets.token_hex(16),
                            "consumed": False, "opened_at": time.time()}
    st["history"].append({"event": "begin_attempt", "attempt": st["attempts_used"],
                          "nen": anh["he_dieu_hanh"]})
    _save(state_dir, st)
    print(f"bắt đầu lượt {st['attempts_used']}/{st['attempts_limit']} — "
          f"nonce={st['attempt_anchor']['nonce']} — state {st['state']}")
    return RC_OK


def cmd_void_attempt(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    if a.reason not in LY_DO_VOID:
        _die(RC_ARG, f"lý do {a.reason!r} không thuộc allowlist {LY_DO_VOID}")
    anchor = st.get("attempt_anchor")
    if isinstance(anchor, dict) and anchor.get("consumed"):
        _die(RC_MOI_TRUONG, "bản ghi này đã dùng để hoàn một lượt rồi")
    if st["attempts_used"] <= 0 or not st.get("attempt_open") or not isinstance(anchor, dict):
        _die(RC_STATE, "chưa có lượt nào để hoàn")
    # Lượt ĐÃ được review thì không hoàn được — nếu không, mọi lượt hỏng đều
    # biến thành "quota" và trần trở thành trang trí.
    if st["reviews"] and st["reviews"][-1]["attempt"] == st["attempts_used"]:
        _die(
            RC_STATE,
            f"lượt {st['attempts_used']} đã có review — không hoàn được lượt đã tiêu thụ nội dung",
        )
    if bool(a.bang_chung) == bool(a.khong_co_bang_chung):
        _die(RC_MOI_TRUONG, "chọn đúng một: --bang-chung hoặc --khong-co-bang-chung")
    if a.bang_chung:
        if a.reason not in LY_DO_CAN_BANG_CHUNG:
            _die(RC_MOI_TRUONG, f"{a.reason!r} không có bằng chứng máy; dùng cửa có người duyệt")
        _kiem_bang_chung_may(a.bang_chung, a.reason, anchor, st["hmac_key"])
    else:
        if a.ai_cho_phep not in NGUOI_CO_THAM_QUYEN or not (a.can_cu or "").strip():
            _die(RC_MOI_TRUONG, "--khong-co-bang-chung đòi --ai-cho-phep hợp lệ và --can-cu")
        st["history"].append({"event": "void_khong_co_bang_chung", "reason": a.reason,
                              "ai_cho_phep": a.ai_cho_phep, "can_cu": a.can_cu})
    anchor["consumed"] = True
    st["attempts_used"] -= 1
    # Đóng luôn lượt đang mở. Thiếu dòng này thì hoàn lượt vì quota lại KHOÁ CỨNG
    # packet: trần đã trả về nhưng `attempt_open` còn bật nên không mở lại được
    # lượt nào — biến một lỗi hạ tầng tạm thời thành ngõ cụt vĩnh viễn.
    st["attempt_open"] = False
    # …và phải RỜI `reviewing`, không chỉ đóng cờ.
    #
    # Finding `void-reviewing-accepts-attempt-zero` (cross-review lượt 6, codex):
    # bản trước giảm `attempts_used` và tắt `attempt_open` nhưng để state nguyên ở
    # `reviewing`. Hậu quả đo được trên `e6e4b73`: `void-attempt` rc=0 đưa
    # `attempts_used` về 0 mà vẫn `state=reviewing`; `begin-attempt` rc=8 (không mở
    # được lượt từ `reviewing`) nên packet KẸT CỨNG; rồi `record-review --verdict
    # approve` rc=0 đưa thẳng sang `accepted` với `reviews[0].attempt=0` — một bản
    # duyệt của LƯỢT KHÔNG TỒN TẠI.
    #
    # AC 8 đòi trả quota mà không tiêu attempt. Nó KHÔNG cho phép packet vừa kẹt
    # vừa được accepted bằng review của attempt 0. Trả về `running` là trạng thái
    # chạy được: `begin-attempt` mở lại lượt bình thường.
    if st["state"] == "reviewing":
        st["state"] = "running"
        # Head cũ hết hiệu lực: lượt đã bị hoàn thì bản duyệt neo vào nó cũng vậy.
        st["reviewing_head_sha"] = None
    st["history"].append({"event": "void_attempt", "reason": a.reason})
    _save(state_dir, st)
    print(f"đã hoàn một lượt vì {a.reason} — còn dùng {st['attempts_used']}/{st['attempts_limit']}")
    return RC_OK


def cmd_chup_anh_doctor(a, state_dir: Path) -> int:
    """Chụp doctor rồi ký trong tiến trình này; khoá HMAC không đi qua argv."""
    st = _load(state_dir, a.packet); anchor = st.get("attempt_anchor")
    if not st.get("attempt_open") or not isinstance(anchor, dict) or anchor.get("consumed"):
        _die(RC_STATE, "không có lượt đang mở để neo ảnh doctor")
    try:
        kq = subprocess.run([sys.executable, str(Path(__file__).with_name("launcher.py")),
                             "doctor", "--json"], capture_output=True)
        d = json.loads(kq.stdout)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        _die(RC_MOI_TRUONG, f"không chụp được `doctor --json`: {type(e).__name__}")
    if not isinstance(d, dict) or not {"thieu_bat_buoc", "chua_xac_thuc", "he_dieu_hanh"} <= d.keys():
        _die(RC_MOI_TRUONG, "ảnh môi trường thiếu trường của `doctor --json`")
    d.update(nonce=anchor["nonce"], attempt=anchor["attempt"])
    d["chu_ky"] = ky_ban_ghi_luot(d, st["hmac_key"])
    out = Path(a.out)
    if out.exists():
        _die(RC_ARG, f"không ghi đè ảnh đã có: {out}")
    try:
        out.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as e:
        _die(RC_MOI_TRUONG, f"không ghi được ảnh doctor: {e}")
    print(f"đã chụp ảnh doctor có neo lượt tại {a.out}")
    return RC_OK


def cmd_record_review(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    if st["state"] != "reviewing":
        _die(RC_STATE, f"chỉ ghi review khi state là 'reviewing' (đang là {st['state']!r})")
    if a.provider != st["reviewer"]:
        _die(
            RC_PROVIDER,
            f"reviewer {a.provider!r} sai nền — packet này đòi {st['reviewer']!r}",
        )

    # LỚP THỨ HAI của `void-reviewing-accepts-attempt-zero`, độc lập với chốt trong
    # `cmd_void_attempt`. Một bản duyệt phải nói về một LƯỢT CÓ THẬT: có lượt đang
    # mở, và số lượt lớn hơn 0. Bản trước không đòi gì trong hai điều đó, nên một
    # state đã hoàn hết lượt vẫn `approve` được và ghi `reviews[0].attempt = 0`.
    #
    # Hai lớp, hai ca, không phủ nhau: gỡ chốt ở `cmd_void_attempt` thì state kẹt
    # lại `reviewing` và CHỐT NÀY chặn; gỡ chốt này thì `void` đã đưa về `running`
    # nên chốt state ở trên chặn. Muốn lọt phải gỡ CẢ HAI — đó là ý đồ.
    if not st["attempt_open"]:
        _die(RC_STATE,
             "không có lượt nào đang mở — bản duyệt phải nói về một lượt CÓ THẬT. "
             "Lượt đã bị hoàn (`void-attempt`) hoặc đã được review rồi.")
    if st["attempts_used"] <= 0:
        _die(RC_STATE,
             f"attempts_used = {st['attempts_used']} — không ghi được review cho "
             f"lượt số 0. Mở lượt bằng `begin-attempt` trước.")

    # Bản duyệt phải neo ĐÚNG head đã đưa ra review. Không có chốt này thì
    # `approve` đưa packet sang 'accepted' mà chẳng nói về commit nào — và một
    # commit chưa ai đọc vẫn được coi là đã duyệt.
    if not a.reviewed_sha:
        _die(RC_TRACE, "record-review phải khai --reviewed-sha (exact head đã đọc)")
    if not SHA_RE.match(a.reviewed_sha):
        _die(RC_TRACE, f"--reviewed-sha {a.reviewed_sha!r} phải là git oid 40 ký tự hex thường")
    if a.reviewed_sha != st["reviewing_head_sha"]:
        _die(
            RC_TRACE,
            f"--reviewed-sha {a.reviewed_sha} KHÔNG khớp head đã đưa ra review "
            f"({st['reviewing_head_sha']}). Head đổi ⇒ bản duyệt cũ hết hiệu lực, "
            f"phải vào lại 'reviewing' với head mới.",
        )

    ids = list(a.finding_id or [])
    if a.verdict == "changes_requested" and not ids:
        _die(RC_ARG, "verdict changes_requested phải có ít nhất một --finding-id SLUG")
    for fid in ids:
        if not SLUG_RE.match(fid):
            _die(
                RC_ARG,
                f"--finding-id {fid!r} sai dạng slug kebab-case (^[a-z0-9]+(-[a-z0-9]+)*$). "
                f"KHÔNG tự suy ID từ mô tả — ID phải do reviewer khai.",
            )

    # (c) cùng ID lặp TRONG MỘT review chỉ tính MỘT lần: dedup trước khi đếm.
    # Không có bước này thì reviewer nhắc lại một lỗi hai lần trong cùng một
    # lượt sẽ chặn oan ngay lượt đầu — đúng lỗi đã đo ở vòng 3.
    ids_duy_nhat = sorted(set(ids))

    st["attempt_open"] = False
    st["reviews"].append(
        {
            "attempt": st["attempts_used"],
            "provider": a.provider,
            "verdict": a.verdict,
            "reviewed_sha": a.reviewed_sha,
            "finding_ids": ids_duy_nhat,
            # (d) mô tả CHỈ để đọc. Nó không tham gia phép đếm, nên hai mô tả
            # khác nhau cùng một ID vẫn là một finding.
            "finding_descs": list(a.finding_desc or []),
        }
    )

    cham_tran = []
    for fid in ids_duy_nhat:
        st["finding_counts"][fid] = st["finding_counts"].get(fid, 0) + 1
        if st["finding_counts"][fid] >= st["same_failure_limit"]:
            cham_tran.append(fid)

    if cham_tran:
        st["state"] = "blocked"
        st["history"].append({"event": "blocked_same_failure", "finding_ids": cham_tran})
        _save(state_dir, st)
        chi_tiet = ", ".join(f"{f}×{st['finding_counts'][f]}" for f in cham_tran)
        _die(
            RC_TRAN,
            f"cùng finding-id lặp tới trần ({chi_tiet}; trần {st['same_failure_limit']}) "
            f"— packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; "
            f"ghi failure evidence + handoff rồi dừng.",
        )

    st["state"] = {"approve": "accepted", "changes_requested": "running", "blocked": "blocked"}[a.verdict]
    if a.verdict == "approve":
        st["accepted_sha"] = a.reviewed_sha
    st["history"].append(
        {"event": "record_review", "verdict": a.verdict,
         "reviewed_sha": a.reviewed_sha, "finding_ids": ids_duy_nhat}
    )
    _save(state_dir, st)
    print(
        f"đã ghi review {a.verdict} bởi {a.provider} — "
        f"{len(ids_duy_nhat)} finding, state {st['state']}"
    )
    return RC_OK


def cmd_transition(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    # Chặn TƯỜNG MINH trước khi tra bảng, để thông điệp nói đúng lý do thay vì
    # rơi vào lỗi "transition không hợp lệ" chung chung.
    if a.to in STATE_CHI_DO_REVIEW_GHI:
        _die(
            RC_STATE,
            f"{a.to!r} KHÔNG đạt được bằng `transition`. Chỉ `record-review --verdict approve` "
            f"ghi được state này, vì nó phải neo `--reviewed-sha` khớp head đã đưa ra review. "
            f"Có đường vòng vào đây là mỏ neo SHA coi như không tồn tại.",
        )
    _kiem_chuyen(st, a.to)
    # Vào 'reviewing' phải có một lượt ĐANG MỞ. Thiếu chốt này, sau một lượt
    # changes_requested (state 'running', attempt_open False) vẫn quay lại
    # 'reviewing' được mà không mở lượt mới — nên hai review dồn vào CÙNG một
    # attempt, và lặp một finding đủ khoá cứng packet trong khi mới tiêu 1 lượt.
    if a.to == "reviewing" and not st["attempt_open"]:
        _die(
            RC_STATE,
            "vào 'reviewing' phải có một lượt đang mở — chạy `begin-attempt` trước. "
            "Không có chốt này thì hai review dồn vào cùng một lượt.",
        )
    # Vào 'reviewing' phải khai ĐÚNG head đang đưa ra review. Đây là mỏ neo mà
    # bản duyệt sẽ phải khớp: bất biến của protocol là bằng chứng review gắn
    # exact SHA, head đổi thì bản duyệt cũ hết hiệu lực.
    if a.to == "reviewing":
        if not a.head_sha:
            _die(RC_TRACE, "vào 'reviewing' phải khai --head-sha (exact head đưa ra review)")
        if not SHA_RE.match(a.head_sha):
            _die(RC_TRACE, f"--head-sha {a.head_sha!r} phải là git oid 40 ký tự hex thường")
    so = _tieu_thu_comment_id(st, a.comment_id, a.to)
    so["consumed_by"] = a.to
    truoc = st["state"]
    st["state"] = a.to
    if a.to == "reviewing":
        st["reviewing_head_sha"] = a.head_sha
    st["history"].append(
        {"event": "transition", "from": truoc, "to": a.to, "comment_id": a.comment_id}
    )
    _save(state_dir, st)
    print(f"đã chuyển {truoc} → {a.to}, neo vào comment {a.comment_id}")
    return RC_OK


def cmd_record_post(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    if not COMMENT_ID_RE.match(a.comment_id):
        _die(
            RC_TRACE,
            f"comment id {a.comment_id!r} sai dạng — phải là id số hoặc node id GitHub trả về "
            f"lúc đăng (ví dụ 5258163128 hoặc IC_kwDOAbc123).",
        )
    if a.comment_id in st["posts"]:
        _die(RC_TRACE, f"comment id {a.comment_id!r} đã có trong sổ — không ghi trùng")
    st["posts"][a.comment_id] = {"for": a.For, "consumed_by": None}
    _save(state_dir, st)
    print(f"đã ghi sổ comment {a.comment_id} cho transition {a.For}")
    return RC_OK


def cmd_next_comment(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    print(
        f"### packet wp{st['packet']} · mission #{st['mission']}\n"
        f"\n"
        f"- state hiện tại: `{st['state']}`\n"
        f"- lượt đã dùng: {st['attempts_used']}/{st['attempts_limit']}\n"
        f"- executor `{st['executor']}` · reviewer `{st['reviewer']}`\n"
        f"- finding đã đếm: "
        + (", ".join(f"`{k}`×{v}" for k, v in sorted(st["finding_counts"].items())) or "chưa có")
        + "\n\nĐăng khối này lên Issue, rồi ghi lại ID GitHub trả về bằng `record-post`."
    )
    return RC_OK


def cmd_guard(a, state_dir: Path) -> int:
    # Không có cờ nới, không có biến môi trường mở khoá, không có ngoại lệ theo
    # actor. Chốt có đường vòng là chốt không tồn tại.
    _die(
        RC_GUARD,
        f"hành vi {a.action!r} bị chặn cứng ở vai executor. "
        f"Đây là cổng của người có quyền, không phải của phiên worker.",
    )
    return RC_GUARD  # pragma: no cover


def cmd_doctrine_scan(a, state_dir: Path) -> int:
    root = Path(a.root)
    muc_tieu: list[Path] = []
    skills = root / ".claude" / "skills"
    if skills.is_dir():
        muc_tieu.extend(sorted(skills.rglob("*.md")))
    claude_md = root / "CLAUDE.md"
    if claude_md.is_file():
        muc_tieu.append(claude_md)
    for extra in a.path or []:
        muc_tieu.append(Path(extra))

    dinh: list[tuple[str, str, str, int]] = []
    for f in muc_tieu:
        try:
            raw = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            _die(RC_ARG, f"không đọc được {f}: {e}")
        phang, ban_do = _phang_ca_tep(raw)
        for nhom, cum_list in FORBIDDEN_DOCTRINE_PHRASES.items():
            for cum in cum_list:
                kim = _chuan_hoa(cum)
                if not kim:
                    continue
                # KHÔNG CÓ MIỄN TRỪ NÀO (AC 19, revision 4). Cụm cấm khớp ở bất kỳ
                # hình dạng nào — liền dòng, ngắt dòng, trong khối mã, trong bảng,
                # trong tag, sau chuẩn hoá — đều là chép doctrine.
                tu = phang.find(kim)
                while tu != -1:
                    dinh.append((str(f), nhom, cum, _dong_tai(ban_do, tu)))
                    tu = phang.find(kim, tu + len(kim))

    if dinh:
        for f, nhom, cum, i in dinh:
            print(f"{f}:{i}: [{nhom}] chép doctrine: {cum!r}", file=sys.stderr)
        _die(
            RC_DOCTRINE,
            f"{len(dinh)} chỗ chép doctrine trong adapter. Adapter chỉ được TRỎ về "
            f"docs/PROTOCOL_DA_PHIEN.md, không nhắc lại nội dung ở đó.",
        )
    print(f"doctrine-scan: sạch — đã quét {len(muc_tieu)} tệp, 0 chỗ chép doctrine")
    return RC_OK


# --- adr-song: bảng định tuyến ADR trong protocol phải PHỦ HẾT docs/adr/ ---------
#
# VÌ SAO CÓ CỔNG NÀY. Trước 22-08-2026 protocol trỏ ADR bằng một dòng PHẠM VI
# (`ADR-0017 đến ADR-0035`). Phạm vi phải được người sửa tay mỗi lần thêm ADR, và
# đo được ngày ấy: 45 ADR tồn tại, protocol nhắc tên 4, trọn `0036`–`0045` nằm
# ngoài — trong đó ba ADR người giữ kho vừa duyệt. Đây là con trỏ chết thứ SÁU
# cùng hình dạng trong kho (bốn cái ở PR #230, một cái là docstring `t34` trỏ
# `t42` đã bị gỡ). Chữa bằng cách viết lại dòng ấy là chữa cái thứ sáu và chờ cái
# thứ bảy; nên thay bằng một BẢNG mà máy đòi đầy đủ.
#
# ĐÂY LÀ DANH SÁCH CHO PHÉP, KHÔNG PHẢI DANH SÁCH CẤM. Cổng không đoán ADR nào
# "đáng" có mặt — nó đòi MỌI tệp `docs/adr/*.md` có đúng một dòng. Bài học
# `v1.36.68`: danh sách cấm phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN.
#
# CỔNG KHÔNG PHÁN XỬ HIỆU LỰC TỪ CHUỖI `Trạng thái`. Đo được bốn cách viết cho
# cùng một nghĩa, và `ADR-0036` ghi "Superseded một phần bởi ADR-0041" — khớp
# tiền tố `Superseded` sẽ loại một ADR VẪN CÒN HIỆU LỰC. Cổng chỉ đòi dòng ấy
# ĐỌC ĐƯỢC; hiệu lực là việc của người đọc bảng.
# --- che vùng KHÔNG RENDER trước khi coi bất cứ gì là metadata sống -------------
#
# FINDING cross-review (codex, P2 trên PR #233, head `d17019628f`): regex đa dòng
# đọc thẳng tệp thô, nên một dòng bảng `ADR-NNNN` hay một dòng `Trạng thái` nằm
# TRONG khối mã có rào hoặc TRONG comment HTML vẫn được tính là metadata sống.
# Đã tái hiện đủ BA ca trước khi vá, tất cả trả `rc=0` trong khi bảng RENDER ra
# không có dòng nào:
#   A1 dòng bảng chỉ nằm giữa ``` ```      A2 dòng bảng chỉ nằm giữa <!-- -->
#   A3 dòng `Trạng thái` của ADR chỉ nằm giữa ``` ```
#
# Cùng họ `_MARKER_NO` của `t43`: đọc CHUỖI thay vì đọc CẤU TRÚC. Khác chiều —
# ở đây nhận nhầm làm cổng báo PHỦ ĐỦ trong khi bảng thật còn thiếu.
#
# CHE, KHÔNG XOÁ: mỗi dòng bị che thành khoảng trắng CÙNG ĐỘ DÀI, nên vị trí và
# số dòng không xê dịch — `_dong_tai` và mọi phép cắt §20 vẫn đúng.
#
# RÀO HỎNG THÌ ĐỎ, không phải "che tới hết tệp rồi thôi": một rào không đóng sẽ
# nuốt mọi metadata phía sau, tức biến lỗi định dạng thành cổng câm.
# TÁCH MỞ và ĐÓNG — chúng KHÔNG cùng luật, và bản trước gộp chúng làm một.
#
# FINDING cross-review lượt 3 (codex, P2 trên head `ef19e3b075`): bản trước khớp
# TIỀN TỐ, nên một dòng như "```not-a-close" bị tính là rào ĐÓNG. Codex dựng chuỗi
# rào xen kẽ — mở · "```not-a-close" · dòng bảng GIẢ · hai rào nữa — làm `adr-song`
# trả `rc=0` trong khi Markdown RENDER ra giữ dòng giả ấy nằm trong khối mã. Đã tái
# hiện trước khi vá.
#
# Luật CommonMark, và mỗi vế dưới đây có một ca:
#   · rào ĐÓNG: cùng loại ký tự, độ dài KHÔNG NGẮN HƠN rào mở, và sau đó CHỈ được
#     có khoảng trắng. "```x" KHÔNG đóng được gì.
#   · rào MỞ bằng BACKTICK: info string không được chứa backtick ("```js`x" không
#     mở khối nào). Rào mở bằng NGÃ thì info string tuỳ ý — "~~~ a`b" là hợp lệ.
#
# Hai luật ngược chiều nhau: một cái làm cổng CHẶT hơn, một cái làm nó RỘNG hơn.
# Gộp thành một regex là cách bản trước sai.
_RAO_MO = re.compile(r"^ {0,3}(`{3,}|~{3,})([^\n]*)$")
_RAO_DONG = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")


def _che_khong_render(raw: str) -> tuple:
    """Trả (văn bản đã che, danh sách vấn đề). Độ dài và số dòng giữ nguyên."""
    van_de: list[str] = []
    dong = raw.split("\n")
    ra: list[str] = []
    rao = None          # ký tự rào đang mở, hoặc None
    rao_dong = 0
    for i, d in enumerate(dong, 1):
        if rao is None:
            m = _RAO_MO.match(d)
            # backtick mở: info string có backtick thì KHÔNG phải rào mở
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                rao, rao_dong = m.group(1), i
                ra.append(" " * len(d))
                continue
            ra.append(d)
        else:
            ra.append(" " * len(d))
            # đóng: cùng loại, không ngắn hơn, và SAU ĐÓ CHỈ khoảng trắng
            mc = _RAO_DONG.match(d)
            if mc and mc.group(1)[0] == rao[0] and len(mc.group(1)) >= len(rao):
                rao = None
    if rao is not None:
        van_de.append(f"rào khối mã mở ở dòng {rao_dong} không được đóng")
    t = "\n".join(ra)

    # comment HTML — che SAU khi che rào, vì `<!--` trong khối mã chỉ là chữ.
    ra2, i, n = [], 0, len(t)
    while True:
        j = t.find("<!--", i)
        if j == -1:
            ra2.append(t[i:])
            break
        k = t.find("-->", j + 4)
        ra2.append(t[i:j])
        if k == -1:
            van_de.append(f"comment HTML mở ở vị trí {j} không được đóng")
            ra2.append("".join(" " if c != "\n" else "\n" for c in t[j:]))
            break
        ra2.append("".join(" " if c != "\n" else "\n" for c in t[j:k + 3]))
        i = k + 3
    return "".join(ra2), van_de


# DÒNG BẢNG chỉ được tính khi nó THUỘC MỘT BẢNG — không phải khi nó "trông giống".
#
# ĐO ĐƯỢC, và nó bác lập luận của chính tôi. Bản trước đếm mọi dòng khớp
# `^| \`ADR-NNNN\` |` ở cột 0, ở BẤT KỲ đâu trong §20. Tôi từng lập luận rằng dù
# vậy chốt chính (N tệp = N dòng) vẫn bắt được rủi ro THẬT là "quên một dòng",
# vì kẻ khai thác phải CỐ Ý thêm dòng giả. Sai. Đo sáu dạng, mỗi dạng đặt một
# dòng giả cho đúng cái ADR đang thiếu — `<pre>` `<div>` `<script>` `<textarea>`
# `<p>` và một dòng TRẦN sau đoạn văn — CẢ SÁU cho `rc=0`. Dòng giả LẤP CHỖ của
# dòng bị quên, nên chốt chính không còn bắt được gì.
#
# Dạng cuối đáng chú ý nhất vì không có HTML nào: một dòng `|…|` đứng sau một
# đoạn văn KHÔNG render thành hàng bảng (GFM đòi header + dòng phân cách), nhưng
# bản trước vẫn đếm. Vậy lỗ không phải "HTML" — mà là chưa bao giờ hỏi dòng ấy có
# thuộc một BẢNG không.
#
# CHỮA Ở TẦNG, không vá thêm một dạng: tìm BẢNG (dòng tiêu đề `| ADR |` + dòng
# phân cách), rồi chỉ đọc các dòng `|` LIỀN MẠCH ngay sau đó. Mọi dòng ngoài khối
# liền mạch ấy — trong HTML, trong văn xuôi, ở đâu cũng vậy — không được tính.
# Đây KHÔNG phải bộ phân tích Markdown; nó chỉ định vị đúng một cấu trúc đã biết.
_ADR_BANG_TIEU_DE = re.compile(r"^\|\s*ADR\s*\|")
_ADR_BANG_PHAN_CACH = re.compile(r"^\|[\s:|-]+\|\s*$")
_ADR_O_DAU = re.compile(r"^\|\s*`ADR-(\d{4})`\s*\|")
# GIỮ LẠI bản cũ CHỈ để đột biến `adr_dem_moi_dong_giong_hang_bang` có mỏ neo ổn
# định. Nó KHÔNG được dùng ở đường chạy thật — dùng lại là dựng lại đúng cái lỗ
# mà mười ca `quen_dong_*` sinh ra để chặn.
_ADR_O_DAU_CU = re.compile(r"^\|\s*`ADR-(\d{4})`\s*\|", re.M)


def _hang_adr_trong_bang(than: str) -> list:
    """Số ADR của các dòng NẰM TRONG một bảng có tiêu đề `| ADR |`.

    Trả về theo thứ tự gặp, KHÔNG khử trùng — phép đếm dòng trùng ở tầng trên
    cần thấy cả hai lần.
    """
    dong = than.split("\n")
    ra: list = []
    i = 0
    while i < len(dong):
        if (_ADR_BANG_TIEU_DE.match(dong[i]) and i + 1 < len(dong)
                and _ADR_BANG_PHAN_CACH.match(dong[i + 1])):
            j = i + 2
            while j < len(dong) and dong[j].startswith("|"):
                m = _ADR_O_DAU.match(dong[j])
                if m:
                    ra.append(m.group(1))
                j += 1
            i = j
            continue
        i += 1
    return ra
# Bó về CỘT 0: đo được 44/45 tệp ADR thật đặt dòng này ở cột 0 (tệp còn lại là
# nợ `ADR-0016-THIEU-DONG-TRANG-THAI`, không có dòng nào). Cho thụt lề tuỳ ý thì
# một khối mã thụt 4 dấu cách cũng lọt — mà khối mã thụt lề KHÔNG có rào để che.
_ADR_TRANG_THAI = re.compile(
    r"^[-*]\s*\*\*Tr[aạ]ng th[aá]i:?\*\*:?\s*(\S.*)$", re.M | re.I
)
_ADR_MUC = re.compile(r"^##\s*20\.\s", re.M)
_ADR_MUC_KE = re.compile(r"^##\s", re.M)

# NỢ CÓ TÊN `ADR-0016-THIEU-DONG-TRANG-THAI`, xem `ops/NO_KY_THUAT.md`. Liệt kê
# TƯỜNG MINH từng số: một ADR MỚI thiếu dòng `Trạng thái` vẫn phải ĐỎ, và có
# phản chứng cho đúng điều đó. Danh sách này chỉ được co lại, không được nới.
_ADR_THA_THIEU_TRANG_THAI = frozenset({"0016"})

# DẠNG TÊN TỆP ADR — bó CHẶT, và có lý do đo được. Bản đầu gom tệp bằng
# `{f.name[:4]: f for f in glob("*.md")}`: hai tệp cùng bốn chữ số đầu thì cái sau
# ĐÈ cái trước trong dict, nên `0001-goc.md` + `0001-ban-sao.md` cho ra **một** mục.
# Cross-review (codex, P2 trên PR #233, head `cbd14439bb`) bắt được; đã dựng phản
# chứng: 2 tệp trên đĩa, cổng in "1 ADR trên đĩa, 1 dòng trong §20" và trả `rc=0`.
#
# Chỗ đau nhất không phải con số sai mà là NÓ PHÁ ĐÚNG BẰNG CHỨNG DƯƠNG: hai số
# "bằng nhau" đều rút ra từ CÙNG cái map đã bị nuốt, nên chúng bằng nhau bất kể có
# bao nhiêu tệp bị nuốt. Hai số chỉ là bằng chứng khi chúng đến từ HAI phép đếm
# ĐỘC LẬP. Nay đếm trên DANH SÁCH tệp, và số trùng làm cổng ĐỎ trước khi gom map.
#
# `f.name[:4].isdigit()` cũ còn im lặng bỏ mọi tên khác dạng — một ADR đặt tên sai
# (`045-thieu-mot-so.md`) biến mất không dấu vết. Nay: khớp dạng thì là ADR; nằm
# trong danh sách CHO PHÉP dưới đây thì cố ý không phải ADR; còn lại là trạng thái
# thứ ba `không đo được` và phải ĐỎ.
_ADR_TEN_TEP = re.compile(r"^(\d{4})-[0-9a-z]([0-9a-z-]*[0-9a-z])?\.md$")
_ADR_TEP_KHONG_PHAI_ADR = frozenset({"README.md"})


def cmd_adr_song(a, state_dir: Path) -> int:
    root = Path(a.root)
    thu_muc = root / "docs" / "adr"
    proto = root / "docs" / "PROTOCOL_DA_PHIEN.md"

    # "Không thấy thì bỏ qua" là cách một ca ĐẠT mà không ĐO gì (bài học `t24`).
    # Chỉ tha khi cây rõ ràng là bản sao rời; trong kho thật mà thiếu thì ĐỎ.
    if not thu_muc.is_dir():
        if (root / ".git").exists():
            _die(RC_ADR, f"kho thật mà không có {thu_muc} — không đo được, không phải sạch")
        print(f"adr-song: bỏ qua — {thu_muc} không có và cây không phải kho git")
        return RC_OK
    if not proto.is_file():
        _die(RC_ADR, f"không có {proto} — không đo được")

    cap: list[tuple[str, Path]] = []
    la: list[str] = []
    for f in sorted(thu_muc.iterdir()):
        if f.is_file() and f.name in _ADR_TEP_KHONG_PHAI_ADR:
            continue
        m2 = _ADR_TEN_TEP.match(f.name) if f.is_file() else None
        if m2 is None:
            la.append(f.name)
            continue
        cap.append((m2.group(1), f))
    if la:
        for x in sorted(la):
            print(f"{thu_muc}/{x}: không khớp {_ADR_TEN_TEP.pattern} và không thuộc "
                  f"danh sách cho phép {sorted(_ADR_TEP_KHONG_PHAI_ADR)} — không đo được",
                  file=sys.stderr)
        _die(RC_ADR, f"{len(la)} mục trong {thu_muc} không phân loại được")
    if not cap:
        _die(RC_ADR, f"{thu_muc} không có tệp ADR nào — không đo được")

    raw, van_de = _che_khong_render(proto.read_text(encoding="utf-8"))
    if van_de:
        for x in van_de:
            print(f"{proto}: {x}", file=sys.stderr)
        _die(RC_ADR, f"{proto} có vùng không render hỏng — không đo được")
    m = _ADR_MUC.search(raw)
    if not m:
        _die(RC_ADR, f"{proto} không có §20 (bảng định tuyến ADR) — cổng này không có gì để đo")
    ke = _ADR_MUC_KE.search(raw, m.end())
    than = raw[m.start(): ke.start() if ke else len(raw)]

    trong_bang: list[str] = _hang_adr_trong_bang(than)
    loi: list[str] = []

    theo_so: dict[str, list[Path]] = {}
    for s, f in cap:
        theo_so.setdefault(s, []).append(f)
    for s, fs in sorted(theo_so.items()):
        if len(fs) > 1:
            loi.append(
                f"ADR-{s}: {len(fs)} tệp cùng số — {[x.name for x in fs]}. Một dòng §20 "
                f"không phủ được nhiều tệp; đổi tên hoặc gộp trước khi chạy lại"
            )

    trung = sorted({s for s in trong_bang if trong_bang.count(s) > 1})
    for s in trung:
        loi.append(f"ADR-{s}: có {trong_bang.count(s)} dòng trong §20 — phải đúng MỘT")

    co = set(trong_bang)
    for s in sorted(set(theo_so) - co):
        loi.append(f"ADR-{s}: có tệp `{theo_so[s][0].name}` mà KHÔNG có dòng nào trong §20")
    for s in sorted(co - set(theo_so)):
        loi.append(f"ADR-{s}: §20 có dòng mà KHÔNG có tệp trong docs/adr/ — con trỏ chết")

    for s, f in sorted(cap):
        than_adr, vd = _che_khong_render(f.read_text(encoding="utf-8"))
        if vd:
            loi.append(f"ADR-{s}: `{f.name}` — {vd[0]}; không đo được")
            continue
        if _ADR_TRANG_THAI.search(than_adr):
            continue
        if s in _ADR_THA_THIEU_TRANG_THAI:
            continue
        loi.append(
            f"ADR-{s}: `{f.name}` không có dòng `Trạng thái` đọc được — "
            f"trạng thái thứ ba (không đo được) làm cổng ĐỎ, không làm nó xanh"
        )

    if loi:
        for d in loi:
            print(d, file=sys.stderr)
        _die(RC_ADR, f"{len(loi)} chỗ lệch giữa docs/adr/ và §20 của {proto}")
    print(
        f"adr-song: sạch — {len(cap)} ADR trên đĩa, {len(trong_bang)} dòng trong §20, khớp 1–1"
        + (f" (tha thiếu trạng thái: {sorted(_ADR_THA_THIEU_TRANG_THAI)})"
           if _ADR_THA_THIEU_TRANG_THAI else "")
    )
    return RC_OK


def cmd_status(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    print(json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True))
    return RC_OK


def cmd_where(a, state_dir: Path) -> int:
    print(f"thư mục state đang dùng: {state_dir}")
    return RC_OK


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="packet_loop.py",
        description=(
            "Cưỡng chế vài stop condition của work packet bằng mã thoát. "
            "Quy tắc đầy đủ ở docs/PROTOCOL_DA_PHIEN.md — tệp này không nhắc lại chúng."
        ),
        epilog=(
            "Mã thoát: 0 ok · 2 sai đối số · 3 chạm trần · 4 sai provider · "
            "5 dấu vết comment không hợp lệ · 6 adapter chép doctrine · "
            "7 hành vi bị chặn cứng · 8 trạng thái không hợp lệ · "
            "9 bảng ADR §20 lệch với docs/adr/."
        ),
    )
    p.add_argument("--state-dir", default=".claude/.packet_state", help="nơi giữ state cục bộ")
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("init", help="khởi tạo state cho một packet")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--mission", type=int, required=True)
    q.add_argument("--executor", required=True)
    q.add_argument("--reviewer", required=True)
    q.add_argument("--attempts-limit", type=int, default=MAC_DINH_TRAN_ATTEMPT)
    q.add_argument("--same-failure-limit", type=int, default=MAC_DINH_TRAN_SAME_FAILURE)
    q.set_defaults(fn=cmd_init)

    q = sub.add_parser("record-lease",
                       help="GHI HỘ lease do bên có thẩm quyền cấp (awaiting_lease → leased)")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--lease-id", required=True, help="định danh lease bên điều phối đã cấp")
    q.add_argument("--granted-by", required=True,
                   help=f"bên CÓ THẨM QUYỀN đã cấp. KHÔNG được là {PROVIDERS} — "
                        f"agent không tự cấp cho mình")
    q.add_argument("--evidence", required=True,
                   help="dấu vết bền để đối chiếu (URL/ID comment nơi lease được cấp)")
    q.add_argument("--expires-utc", required=True,
                   help="hạn lease, ISO8601 CÓ múi giờ, ví dụ 2026-08-13T18:30:00Z")
    q.set_defaults(fn=cmd_record_lease)

    q = sub.add_parser("begin-attempt", help="mở một lượt executor")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--provider", required=True)
    q.add_argument("--bang-chung-moi-truong",
                   help=f"ảnh launcher doctor --json; thiếu thì đọc ${BIEN_BANG_CHUNG}")
    q.set_defaults(fn=cmd_begin_attempt)

    q = sub.add_parser("void-attempt", help="hoàn lượt vì lỗi hạ tầng/quota")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--reason", required=True, help=f"một trong {LY_DO_VOID}")
    q.add_argument("--bang-chung", help="ảnh doctor hoặc run.json có neo lượt")
    q.add_argument("--khong-co-bang-chung", action="store_true",
                   help="cửa có người duyệt và ghi sổ")
    q.add_argument("--ai-cho-phep", help=f"phải thuộc {NGUOI_CO_THAM_QUYEN}")
    q.add_argument("--can-cu", help="căn cứ người duyệt cho phép hoàn lượt")
    q.set_defaults(fn=cmd_void_attempt)

    q = sub.add_parser("chup-anh-doctor", help="chụp và ký doctor cho lượt đang mở")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--out", required=True)
    q.set_defaults(fn=cmd_chup_anh_doctor)

    q = sub.add_parser("record-review", help="ghi một lượt review")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--provider", required=True)
    q.add_argument("--verdict", required=True, choices=("approve", "changes_requested", "blocked"))
    q.add_argument("--reviewed-sha", help="exact head đã đọc; phải khớp head đưa ra review")
    q.add_argument(
        "--finding-id",
        action="append",
        help="slug kebab-case ổn định, ví dụ url-alias. Lặp lại được. Đây là KHOÁ đếm.",
    )
    q.add_argument(
        "--finding-desc",
        action="append",
        help="mô tả tự do, CHỈ để đọc — không tham gia phép đếm.",
    )
    q.set_defaults(fn=cmd_record_review)

    q = sub.add_parser("transition", help="chuyển state, đòi dấu vết comment bền")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--to", required=True)
    q.add_argument("--comment-id", help="ID GitHub trả về, đã ghi sổ bằng record-post")
    q.add_argument("--head-sha", help="bắt buộc khi --to reviewing: exact head đưa ra review")
    q.set_defaults(fn=cmd_transition)

    q = sub.add_parser("record-post", help="ghi sổ ID comment GitHub trả về lúc đăng")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--for", dest="For", required=True, help="transition mà comment này chứng minh")
    q.add_argument("--comment-id", required=True)
    q.set_defaults(fn=cmd_record_post)

    q = sub.add_parser("next-comment", help="in văn bản comment để người đăng")
    q.add_argument("--packet", type=int, required=True)
    q.set_defaults(fn=cmd_next_comment)

    q = sub.add_parser("guard", help="chặn cứng hành vi ngoài vai executor")
    q.add_argument("--action", required=True, choices=HANH_VI_CHAN)
    q.set_defaults(fn=cmd_guard)

    q = sub.add_parser("doctrine-scan", help="bắt adapter chép doctrine")
    q.add_argument("--root", default=".")
    q.add_argument("--path", action="append", help="quét thêm tệp cụ thể")
    q.set_defaults(fn=cmd_doctrine_scan)

    q = sub.add_parser("adr-song",
                       help="bảng §20 của protocol phải phủ hết docs/adr/")
    q.add_argument("--root", default=".")
    q.set_defaults(fn=cmd_adr_song)

    q = sub.add_parser("status", help="in state đầy đủ")
    q.add_argument("--packet", type=int, required=True)
    q.set_defaults(fn=cmd_status)

    sub.add_parser("where", help="in thư mục state").set_defaults(fn=cmd_where)
    return p


def main(argv=None) -> int:
    _cung_hoa_stdout()
    a = build_parser().parse_args(argv)
    return a.fn(a, Path(a.state_dir))


if __name__ == "__main__":
    sys.exit(main())
