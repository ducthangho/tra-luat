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
    3  chạm trần — hết attempt, same-failure, hoặc trần vòng review/lời gọi codex (ADR-0037)
    4  vi phạm cross-provider
    5  dấu vết comment không hợp lệ — chưa đăng ký, sai transition, hoặc đã dùng
    6  doctrine-scan bắt được cụm từ bị cấm trong adapter
    7  guard chặn cứng một hành vi trong bảng
    8  trạng thái không hợp lệ — transition sai, lượt đang mở, init đè state
   12  `kiem-gate`: gate bắt buộc không XANH trên head (gồm cả KHÔNG ĐO ĐƯỢC)

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
# #775 Review Rescue (ADR-0037): trần vòng (ADR-0048) + lời gọi codex (§12); trục → (khoá dùng, khoá trần).
MAC_DINH_TRAN_VONG_REVIEW = 10
MAC_DINH_TRAN_CODEX = 2
TRUC_TRAN = {"vong_review": ("review_rounds_used", "review_rounds_limit"),
             "codex_review_calls": ("codex_review_calls_used", "codex_review_calls_limit")}
CAN_CU_RE = re.compile(r"^https://github\.com/[^/]+/[^/]+/(issues|pull)/[0-9]+#issuecomment-[0-9]+$")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
CANH_BAO_V1 = "CẢNH BÁO: bộ đếm SUY RA từ state v1, có thể THẤP hơn thật"

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
RC_BIEN_NHAN = 11
RC_GATE = 12

PROVIDER_FAMILIES = {"claude": "claude", "codex": "openai", "google_antigravity": None}
PROVIDERS = tuple(PROVIDER_FAMILIES)
MODEL_FAMILIES = ("claude", "openai", "gemini")
RUNTIME_CAPABILITIES = {
    "claude": {"claude_code": ("machine/local",)},
    # machine/local là cách khai legacy của Codex CLI/Desktop; service chỉ nhận machine.
    "codex": {"codex_cli": ("machine", "machine/local"),
              "codex_desktop": ("machine", "machine/local"),
              "codex_service": ("machine",)},
    "google_antigravity": {"antigravity": ("machine/local",)},
}


def _identity(provider, model_family=None, surface=None, transport=None):
    if provider not in PROVIDERS:
        _die(RC_ARG, f"provider phải thuộc {PROVIDERS}")
    family = model_family.strip() if isinstance(model_family, str) else model_family
    surface = surface.strip() if isinstance(surface, str) else surface
    transport = transport.strip() if isinstance(transport, str) else transport
    if surface == "" or transport == "":
        _die(RC_ARG, "execution_surface/transport đã khai không được rỗng")
    if provider == "google_antigravity" and not all((family, surface, transport)):
        _die(RC_ARG, "google_antigravity cần model_family, execution_surface và transport")
    family = family or PROVIDER_FAMILIES[provider]
    if family not in MODEL_FAMILIES:
        _die(RC_ARG, f"model_family phải thuộc {MODEL_FAMILIES}")
    if provider != "google_antigravity" and family != PROVIDER_FAMILIES[provider]:
        _die(RC_ARG, f"{provider} không thể khai model_family={family!r}")
    capabilities = RUNTIME_CAPABILITIES[provider]
    if surface is not None and surface not in capabilities:
        _die(RC_ARG, f"{provider} không hỗ trợ execution_surface={surface!r}")
    allowed_transports = (capabilities[surface] if surface is not None else
                          {t for options in capabilities.values() for t in options})
    if transport is not None and transport not in allowed_transports:
        _die(RC_ARG, f"{provider} không hỗ trợ transport={transport!r} trên {surface!r}")
    return {"provider": provider, "model_family": family,
            "execution_surface": surface,
            "transport": transport}


def _check_runtime_identity(a, st, role):
    expected = st.get(f"{role}_identity")
    if expected is None:
        if st[role] == "google_antigravity":
            _die(RC_STATE, f"{role} thiếu identity trong state")
        return
    actual = _identity(a.provider, a.model_family, a.execution_surface, a.transport)
    if any(expected.get(field) is not None and actual[field] != expected[field]
           for field in ("provider", "model_family", "execution_surface", "transport")):
        _die(RC_PROVIDER, f"{role} runtime identity khác state: {actual!r} != {expected!r}")

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
SHA_RE = re.compile(r"^[0-9a-f]{40}\Z")

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
    if d is not None and (not isinstance(d, dict) or not {"thieu_bat_buoc", "chua_xac_thuc", "he_dieu_hanh"} <= d.keys()):
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
    try:  # #775 bộ đọc NGHIÊM: lệch hình dạng hay bất biến sổ/bộ đếm ⇒ RC_STATE, không traceback, không đoán
        st = json.loads(p.read_text(encoding="utf-8"))
        for role in ("executor", "reviewer"):
            identity = st.get(f"{role}_identity")
            if identity is not None and (type(identity) is not dict or role == "reviewer" and st["reviewer"] == "codex" and identity.get("model_family", PROVIDER_FAMILIES["codex"]) != "openai"):
                raise ValueError(f"{role}_identity")
        can_duoi = _la_codex(st) * sum(r.get("provider") == st["reviewer"] for r in st["reviews"])
        if type(st["schema_version"]) is int and st["schema_version"] == 1:  # M6: SUY bộ đếm = cận DƯỚI ở trên — suy 0 là fail-open
            st.update(schema_version=2, review_rounds_used=len(st["reviews"]), codex_review_calls_used=can_duoi,
                      codex_calls=[], nang_tran=[], review_rounds_limit=MAC_DINH_TRAN_VONG_REVIEW,
                      codex_review_calls_limit=MAC_DINH_TRAN_CODEX, dem_tu_suy=True, attempt_open=st.get("attempt_open", False), reviewing_head_sha=st.get("reviewing_head_sha"))
        goi, posts, anchor = st["codex_calls"], st["posts"], st.get("attempt_anchor")
        pending = next((h.get("event") != "record_rescue" or h.get("mo_lai") is not True for h in reversed(st["history"]) if h.get("event") in ("blocked_rescue_required", "record_rescue")), False)
        vi_pham = [ten for ten, dung in (  # mỗi bất biến MỘT phần tử ⇒ mỗi cái một đột biến riêng
            ("schema", type(st["schema_version"]) is int and st["schema_version"] == 2 and type(st["packet"]) is int and st["packet"] == packet and st["state"] in CHUYEN_HOP_LE and type(st["mission"]) is int and st["executor"] in PROVIDERS and (st["reviewing_head_sha"] is None or SHA_RE.match(st["reviewing_head_sha"]))),
            ("bo-dem", all(type(st[k]) is int for k in ("attempts_used", "attempts_limit", "same_failure_limit")) and st["attempts_used"] >= 0 and all(type(st[u]) is int is type(st[t]) and st[u] >= 0 < st[t] for u, t in TRUC_TRAN.values())),
            ("so", all(type(st[k]) is list for k in ("codex_calls", "nang_tran", "reviews", "history"))
                   and all(r.get("provider") == st["reviewer"] and type(r.get("attempt")) is int for r in st["reviews"])
                   and all(type(h) is dict for h in st["history"]) and type(st.get("dem_tu_suy", False)) is bool and type(st["attempt_open"]) is bool
                   and type(st.get("finding_counts")) is dict and all(type(n) is int and n >= 0 for n in st["finding_counts"].values())),
            ("posts", type(posts) is dict and all(type(r) is dict and type(r["for"]) is str and (r["consumed_by"] is None or type(r["consumed_by"]) is str) for r in posts.values())),
            ("anchor", anchor is None or type(anchor) is dict and type(anchor["attempt"]) is int and type(anchor["consumed"]) is bool and re.fullmatch(r"[0-9a-f]{32}", anchor["nonce"]) and re.fullmatch(r"[0-9a-f]{64}", st["hmac_key"])),
            ("findings", st["finding_counts"] == {fid: sum(fid in r.get("finding_ids", []) for r in st["reviews"]) for r in st["reviews"] for fid in r.get("finding_ids", [])}),
            ("loi-goi", all(set(g) == {"run_id", "head", "da_dung"} and RUN_ID_RE.match(g["run_id"])
                            and SHA_RE.match(g["head"]) and type(g["da_dung"]) is bool for g in goi)),
            ("dem-goi", len({g["run_id"] for g in goi}) == len(goi) <= st["codex_review_calls_used"] >= can_duoi + sum(not g["da_dung"] for g in goi)),
            ("dem-vong", st["review_rounds_used"] == len(st["reviews"])),
            ("checkpoint", pending == (st.get("ly_do") == "rescue_required")), ("truc", st.get("ly_do") != "rescue_required" or st["state"] == "blocked" and st["truc"] in TRUC_TRAN and st["truc"] == next(  # mốc chạm trần MỚI NHẤT
                h["truc"] for h in reversed(st["history"]) if h.get("event") == "blocked_rescue_required"))) if not dung]
    except (ValueError, TypeError, KeyError, AttributeError, StopIteration) as e:
        vi_pham = [f"{type(e).__name__}: {e}"]
    if vi_pham:
        _die(RC_STATE, f"state hỏng ({', '.join(vi_pham)}) — không đoán: {p}")
    return st


def _la_codex(st: dict) -> bool:  # #775: tên provider VÀ họ model; state cũ thiếu identity ⇒ họ mặc định của codex
    return st["reviewer"] == "codex" and (st.get("reviewer_identity") or {}).get("model_family", "openai") == "openai"


def _vao_rescue(state_dir: Path, st: dict, truc: str, ngu_canh: str) -> None:
    u, t = TRUC_TRAN[truc]
    st.update(state="blocked", ly_do="rescue_required", truc=truc)
    st["history"].append({"event": "blocked_rescue_required", "truc": truc, "used": st[u], "limit": st[t]})
    _save(state_dir, st); _die(RC_TRAN, f"{ngu_canh}: {truc} {st[u]}/{st[t]} — Review Rescue Checkpoint: dừng, hỏi chủ kho"
                  + (f"\n{CANH_BAO_V1}" if st.get("dem_tu_suy") else ""))


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
    if min(a.review_rounds_limit, a.codex_review_calls_limit) <= 0:  # #775 M1
        _die(RC_ARG, "--review-rounds-limit/--codex-review-calls-limit phải là số nguyên DƯƠNG")
    executor_identity = _identity(a.executor, a.executor_model_family,
                                  a.executor_execution_surface, a.executor_transport)
    reviewer_identity = _identity(a.reviewer, a.reviewer_model_family,
                                  a.reviewer_execution_surface, a.reviewer_transport)
    # Cross-provider: chặn NGAY từ init, không đợi tới lúc ghi review.
    if a.executor == a.reviewer or executor_identity["model_family"] == reviewer_identity["model_family"]:
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
        "schema_version": 2, "review_rounds_used": 0, "codex_review_calls_used": 0, "codex_calls": [], "nang_tran": [],
        "review_rounds_limit": a.review_rounds_limit, "codex_review_calls_limit": a.codex_review_calls_limit,
        "packet": a.packet,
        "mission": a.mission,
        "executor": a.executor,
        "reviewer": a.reviewer,
        "executor_identity": executor_identity,
        "reviewer_identity": reviewer_identity,
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
    _check_runtime_identity(a, st, "executor")
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
    _check_runtime_identity(a, st, "reviewer")

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

    goi = None
    if _la_codex(st):
        goi = next((g for g in st["codex_calls"] if g["run_id"] == a.codex_call), None)
        if goi is None:
            _die(RC_TRACE, f"--codex-call {a.codex_call!r} không trỏ lời gọi nào đã `record-codex-call`")
        if goi["head"] != a.reviewed_sha:
            _die(RC_TRACE, f"lời gọi {a.codex_call!r} chạy trên head {goi['head']}, không phải review này")
        if goi["da_dung"]:
            _die(RC_TRACE, f"lời gọi {a.codex_call!r} đã neo một review — mỗi lời gọi MỘT lần")

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
    st["review_rounds_used"] += 1
    if goi is not None:
        goi["da_dung"] = True
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

    if a.verdict != "approve":  # approve KHÔNG BAO GIỜ kích rescue
        for truc, (u, t) in TRUC_TRAN.items():
            if st[u] >= st[t]:
                _vao_rescue(state_dir, st, truc, f"review {a.verdict} chưa approve")

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


def cmd_record_codex_call(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    if not _la_codex(st):  # connector P2: reviewer khác codex không tiêu ngân sách codex, không kích rescue giả
        _die(RC_PROVIDER, f"reviewer {st['reviewer']!r} không phải codex — không có lời gọi codex để ghi")
    if st["state"] != "reviewing":
        _die(RC_STATE, f"chỉ ghi lời gọi codex khi state 'reviewing' (đang {st['state']!r})")
    if a.head != st["reviewing_head_sha"]:
        _die(RC_TRACE, f"--head {a.head!r} KHÔNG khớp head đưa ra review ({st['reviewing_head_sha']})")
    if not RUN_ID_RE.match(a.run_id) or any(g["run_id"] == a.run_id for g in st["codex_calls"]):
        _die(RC_ARG, f"--run-id {a.run_id!r} sai dạng hoặc đã ghi")
    if st["codex_review_calls_used"] >= st["codex_review_calls_limit"]:
        _vao_rescue(state_dir, st, "codex_review_calls", "lời gọi codex bị CHẶN TRƯỚC")
    st["codex_review_calls_used"] += 1
    st["codex_calls"].append({"run_id": a.run_id, "head": a.head, "da_dung": False})
    _save(state_dir, st)
    print(f"đã ghi lời gọi codex {a.run_id} — {st['codex_review_calls_used']}/{st['codex_review_calls_limit']}")
    return RC_OK


def cmd_nang_tran(a, state_dir: Path) -> int:
    """#775 M4. LỜI KHAI, KHÔNG PHẢI BẰNG CHỨNG: không đọc GitHub, chỉ kiểm HÌNH DẠNG `--can-cu` và cái TÊN."""
    st = _load(state_dir, a.packet)
    if (a.ai_nang or "").strip() not in NGUOI_CO_THAM_QUYEN:
        _die(RC_GUARD, f"--ai-nang {a.ai_nang!r} ngoài danh sách CHO PHÉP {NGUOI_CO_THAM_QUYEN}")
    u, t = TRUC_TRAN[a.truc]
    if a.tran_moi <= st[t] or not CAN_CU_RE.match(a.can_cu):
        _die(RC_ARG, f"--tran-moi phải > trần {st[t]} và --can-cu phải là URL issuecomment GitHub")
    st["nang_tran"].append(dict(truc=a.truc, tran_cu=st[t], tran_moi=a.tran_moi, ai_nang=a.ai_nang.strip(), can_cu=a.can_cu))
    st[t] = a.tran_moi; _save(state_dir, st)
    print(f"đã nâng trần {a.truc} lên {a.tran_moi} (đã dùng {st[u]}) — LỜI KHAI, không phải bằng chứng")
    return RC_OK


def cmd_record_rescue(a, state_dir: Path) -> int:
    """#775 M5: cửa DUY NHẤT ra khỏi blocked-vì-rescue (CHUYEN_HOP_LE không đổi); chỉ nang_tran ĐÃ nâng mở lại."""
    st = _load(state_dir, a.packet)
    if st["state"] != "blocked" or st.get("ly_do") != "rescue_required":
        _die(RC_STATE, f"record-rescue chỉ cho blocked vì rescue_required (đang {st['state']!r})")
    if not CAN_CU_RE.match(a.can_cu):
        _die(RC_ARG, f"--can-cu {a.can_cu!r} phải là URL issuecomment GitHub")
    mo = (nang := a.quyet_dinh == "nang_tran") and st[TRUC_TRAN[st["truc"]][1]] > st[TRUC_TRAN[st["truc"]][0]]
    st["history"].append(dict(event="record_rescue", quyet_dinh=a.quyet_dinh, truc=st.get("truc"), can_cu=a.can_cu, mo_lai=mo))
    if mo:
        st["state"] = "running"; del st["ly_do"], st["truc"]
    _save(state_dir, st)
    if nang and not mo:
        _die(RC_STATE, f"trục {st['truc']} chưa được nâng quá số đã dùng — chạy `nang-tran` trước")
    print(f"đã ghi rescue {a.quyet_dinh} — state {st['state']}")
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


# ── #338: HẠ LỜI KHAI xuống đúng hạng bằng chứng ─────────────────────────────────────────
# Bản trước nói: "Đây là cổng của người có quyền, không phải của phiên worker", và chú thích
# nói "Chốt có đường vòng là chốt không tồn tại."
#
# CẢ HAI CÂU ĐỀU SAI VỀ HIỆU LỰC, và câu thứ hai tự nêu tiêu chí mà chính nó trượt:
#   · đường vòng CÓ THẬT — merge qua MCP. Đã đi 9 lần trên `master` trong một phiên, 4 lần
#     có tự khai `rc=7` trong thông điệp merge, 5 lần không;
#   · và cổng này KHÔNG phân biệt được thẩm quyền. Đo 2026-08-26:
#       get_me                     -> {"login":"ducthangho","id":12748935}
#       master.protected           -> true  (nhánh DUY NHẤT được bảo vệ)
#     CỐ Ý KHÔNG ghi mẫu số. Bản đầu ghi "trong 222" và con số ấy trôi trong vòng
#     một giờ (đo cùng ngày: 223 rồi 225) vì nhánh `ops/**` sinh và bị xoá liên
#     tục. Một mẫu số hết hạn nhanh hơn câu chứa nó thì nó chỉ làm câu ấy sai.
#     Thứ có ý nghĩa là "đúng một nhánh được bảo vệ", không phải tỷ lệ.
#     Phiên chạy bằng credential CỦA CHỦ KHO. Nên "cổng của người có quyền" mô tả một phép
#     kiểm không tồn tại: nó chặn một NHÃN VAI, không chặn một THẨM QUYỀN.
#
# Kho này đã làm đúng động tác ấy một lần và nó đúng — packet #324 pha A2: không chứng minh
# được "read-only" thì BỎ CHỮ "read-only", chứ không vá lần thứ năm. Ở đây cũng vậy.
#
# CƠ CHẾ CÒN THIẾU, viết thẳng vào đây để ai đọc `rc=7` cũng đọc luôn cái chưa có:
#   TÁCH DANH TÍNH — cấp phiên một token KHÔNG có quyền merge, giữ quyền merge ở một danh
#   tính người. Đó là thay đổi HẠ TẦNG, không phải thay đổi mã; không write set nào chứa
#   được nó, và phiên này ĐO ĐƯỢC là mình không kiểm chứng nổi (`/repos/…/protection` trả
#   403 với 0 header GitHub — proxy chặn theo ĐƯỜNG DẪN).
# Chừng nào chưa có nó, MỌI chốt dựng trong kho đều là chốt chủ kho tự dựng cho chính mình,
# và phiên kế thừa đúng thẩm quyền ấy. Đừng vá tiếp ở tầng này.
#
# CÂU TRÊN CHỈ ĐÚNG VỚI GITHUB — đo 2026-08-27, và phép đo này nói CHỖ NÀO cần sửa:
#     ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN          CHƯA ĐẶT
#     /root/.claude/.credentials.json                   KHÔNG có credential Anthropic nào
#     CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR = '4'     credential đi bằng FILE DESCRIPTOR
#     CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST    = '1'     host giữ, không phải phiên
#     `ls /proc/<shell con>/fd/` -> chỉ 0,1,2           fd 4 KHÔNG xuống tiến trình con
#     GITHUB_PAT                                        biến THƯỜNG, 93 ký tự, đọc thẳng được
# Tức mô hình "credential mà phiên KHÔNG phát lại được" ĐÃ CHẠY SẴN trong container này cho
# đường Anthropic; nó chỉ chưa được áp cho đường GitHub. "Tách danh tính" vì thế KHÔNG phải
# một giả thuyết kiến trúc — nó là ÁP CÙNG CÁCH ĐỐI XỬ cho GitHub.
#
# VÀ MỘT CÁM DỖ PHẢI TỪ CHỐI: có `CLAUDE_CODE_USER_EMAIL` / `..._ACCOUNT_UUID` /
# `..._ORGANIZATION_UUID` trong môi trường. ĐỪNG đọc chúng để quyết định uỷ quyền. Chúng là
# biến MÔI TRƯỜNG THƯỜNG — phiên đọc được thì phiên cũng ĐẶT được cho tiến trình con. Đó là
# lời khai của host cho khách, không phải bằng chứng cho một chốt chạy BÊN TRONG khách; dùng
# chúng ở đây thì yếu hệt một cờ `--uy-quyen`, tức đúng D1 đã bị bác.
#
# CHƯA ĐO, và cố ý không đo: container chạy `root`, nên rất có thể `root` đọc được
# `/proc/<pid cha>/fd/4`. Thử điều đó nghĩa là ĐỌC MỘT CREDENTIAL, mà `CLAUDE.md` cấm. Nên
# ranh giới fd ấy đứng ở trạng thái KHÔNG ĐO ĐƯỢC — nếu vượt được thì nó là QUY ƯỚC, không
# phải tường. Đừng đọc câu trên mạnh hơn thế.
_KHAI_UY_QUYEN = "uy_quyen_merge.jsonl"


def cmd_guard(a, state_dir: Path) -> int:
    _die(
        RC_GUARD,
        f"hành vi {a.action!r} KHÔNG được phép ở vai executor.\n"
        f"\n"
        f"ĐÂY LÀ LỜI NHẮC, KHÔNG PHẢI PHÉP KIỂM THẨM QUYỀN. Cổng này chặn một NHÃN VAI; nó\n"
        f"KHÔNG phân biệt được uỷ quyền thật với một phiên tự cho phép mình, vì phiên chạy\n"
        f"bằng credential của chủ kho (đo 2026-08-26: `get_me` -> ducthangho). Cơ chế còn\n"
        f"thiếu là TÁCH DANH TÍNH — xem #338, và xem chú thích ngay trên hàm này.\n"
        f"\n"
        f"Được chủ kho uỷ quyền thật thì ghi lại cho ĐẾM ĐƯỢC:\n"
        f"  packet_loop.py ghi-uy-quyen --action {a.action} --nguoi-cap <ai> \\\n"
        f"      --bang-chung <url> --head-sha <sha40>\n"
        f"Ghi xong cổng này VẪN trả {RC_GUARD} — nó không mở khoá được thứ nó không kiểm được.",
    )
    return RC_GUARD  # pragma: no cover


def cmd_ghi_uy_quyen(a, state_dir: Path) -> int:
    """Ghi một KHAI BÁO uỷ quyền vào sổ máy đọc được.

    ĐÂY LÀ LỜI KHAI, KHÔNG PHẢI BẰNG CHỨNG — phiên tự gõ được lệnh này, y hệt nó tự gõ
    được câu văn xuôi trong thông điệp merge hôm nay. Cái nó mua KHÔNG phải sự thật, mà là
    KHẢ NĂNG ĐẾM: đo 2026-08-26 cho 9 merge / 4 tự khai / *ai làm* KHÔNG ĐO ĐƯỢC, và chính
    cái không-đo-được ấy là lý do việc này xảy ra 9 lần mà không ai thấy con số.
    Một tần suất KHÔNG BIẾT thành một tần suất BIẾT. Chỉ vậy, và nói đúng chỉ vậy."""
    if not SHA_RE.match(a.head_sha or ""):
        _die(RC_ARG, f"--head-sha phải là sha40, nhận {a.head_sha!r}")
    # DÙNG LẠI danh sách CHO PHÉP đã có, không dựng danh sách cấm mới. Kho này đã trả giá
    # đúng một lần cho việc ấy (`lease-authority-spoof` P1: `codex-dispatcher`, `ai-codex-bot`,
    # `cödex` đều lọt vì chốt cũ từ chối đúng hai chuỗi) — xem chú thích ở `NGUOI_CO_THAM_QUYEN`.
    if (a.nguoi_cap or "").strip() not in NGUOI_CO_THAM_QUYEN:
        _die(RC_GUARD,
             f"--nguoi-cap {a.nguoi_cap!r} không nằm trong danh sách CHO PHÉP "
             f"({', '.join(NGUOI_CO_THAM_QUYEN)}). Và nhắc lại giới hạn đã ghi ở đó: danh "
             f"sách này chứng minh cái TÊN được phép cấp, KHÔNG chứng minh đúng người đó "
             f"đã gõ — tệp này chạy CỤC BỘ, không có `GITHUB_ACTOR` để neo danh tính.")
    state_dir.mkdir(parents=True, exist_ok=True)
    ban_ghi = {
        "event": "uy_quyen_merge_KHAI_BAO",
        "action": a.action,
        "nguoi_cap": a.nguoi_cap,
        "bang_chung": a.bang_chung,
        "head_sha": a.head_sha,
        "ghi_boi": "packet_loop",
        "la_loi_khai_khong_phai_bang_chung": True,
    }
    with (state_dir / _KHAI_UY_QUYEN).open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(ban_ghi, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"đã ghi KHAI BÁO uỷ quyền {a.action!r} cho head {a.head_sha[:12]} "
          f"(cấp bởi {a.nguoi_cap}) — đây là LỜI KHAI, không phải bằng chứng")
    return RC_OK


def cmd_doi_chieu_uy_quyen(a, state_dir: Path) -> int:
    """Đếm merge trên một nhánh so với khai báo đã ghi. Biến KHÔNG ĐO ĐƯỢC thành SỐ.

    Lệnh này KHÔNG ngăn được gì và không giả vờ ngăn. Nó trả lời đúng một câu hỏi mà hôm
    nay không ai trả lời được: *bao nhiêu lần merge có khai, bao nhiêu lần không*."""
    # `--first-parent` KHONG phai tuy chon. Thieu no, lenh dem ca merge nam BEN TRONG nhanh
    # phu nhu mot merge "tren master". Do duoc trong dung cua so cua Issue #338:
    #     git rev-list --count --merges                c35ae1c..origin/master  -> 10
    #     git rev-list --count --merges --first-parent c35ae1c..origin/master  ->  9
    # Con so `9` toi khai o luot 1 do bang mot lenh KHAC voi lenh toi giao — cross-review
    # bat dung cho ay. "Merge tren nhanh X" nghia la merge tren duong CHA THU NHAT cua X;
    # muon dem toan DAG thi phai la mot che do co TEN KHAC, khong duoc am tham doi nghia.
    if not a.since:
        _die(RC_ARG,
             "--since la BAT BUOC: khong co bien, lenh dem TOAN BO lich su theo "
             "duong cha thu nhat (do tren kho nay 27-08-2026: 193 merge) va con so "
             "ay khong tai lap duoc giua hai luot.")
    r = subprocess.run(["git", "-C", a.root, "rev-parse", "--verify", a.since + "^{commit}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        _die(RC_ARG, f"--since {a.since!r} khong phai commit doc duoc")
    bien_day_du = r.stdout.strip()
    r = subprocess.run(["git", "-C", a.root, "log", "--merges", "--first-parent",
                        "--format=%H%x09%s", bien_day_du + ".." + a.nhanh],
                       capture_output=True, text=True)
    if r.returncode != 0:
        _die(RC_ARG, f"không đọc được lịch sử git: {(r.stderr or '').strip()[:200]}")
    merges = [x.split("\t", 1) for x in r.stdout.splitlines() if x.strip()]
    # SO KHAI — thieu so thi KHONG DO DUOC, KHONG phai 0. So mac dinh nam trong
    # `.claude/.packet_state/`, ma thu muc ay bi `.gitignore` loai (`.gitignore:32`), nen
    # mot clone/phien moi KHONG phan biet duoc "khong co khai bao" voi "so khong duoc
    # chuyen sang" — tra ve 0 la doc cai IM LANG thanh mot phep do. `None != False`.
    so = Path(a.so) if getattr(a, "so", None) else (state_dir / _KHAI_UY_QUYEN)
    khai: dict[str, dict] = {}
    bo_qua: list[str] = []
    if not so.is_file():
        _die(RC_STATE,
             f"KHONG DO DUOC: khong thay so khai bao tai {so}. Day KHONG phai 'khong co "
             f"khai bao nao' — so mac dinh nam trong thu muc bi .gitignore loai, nen mot "
             f"clone moi se khong co no. Tro so BEN bang --so, hoac chap nhan la chua do.")
    if True:
        for stt, dong in enumerate(so.read_text(encoding="utf-8").splitlines(), 1):
            if not dong.strip():
                continue
            try:
                d = json.loads(dong)
            except json.JSONDecodeError:
                # CỐ Ý không viết `except ValueError:` ở đây, dù JSONDecodeError là con của
                # nó. Lý do KHÔNG phải phong cách: bảng đột biến của bộ test khớp CHUỖI CON
                # (`str.replace(moc, ..., 1)`), nên một dòng 12 dấu cách `except ValueError:`
                # CHỨA mốc 8 dấu cách của đột biến `bien_nhan_bo_nhanh_valueerror`. Code này
                # nằm TRƯỚC `bien-nhan` trong tệp ⇒ đột biến sẽ sửa NHẦM dòng này và trở
                # thành vô hiệu, còn ca đích thì XANH mà không đo gì.
                # ĐO ĐƯỢC: mốc khớp 1 chỗ trên master, 2 chỗ khi có dòng ấy.
                continue
            # KIEM LUOC DO. Ban truoc chi doi co truong `head_sha`, nen mot ban ghi cua
            # action KHAC, hoac mot dong JSON viet tay, cung duoc tinh la khai bao merge.
            thieu = [k for k in ("event", "action", "nguoi_cap", "bang_chung", "head_sha")
                     if not d.get(k)]
            if thieu:
                bo_qua.append(f"dong {stt}: thieu {'/'.join(thieu)}")
                continue
            if d.get("event") != "uy_quyen_merge_KHAI_BAO":
                bo_qua.append(f"dong {stt}: event={d.get('event')!r} khong phai khai bao")
                continue
            if d.get("action") != a.action:
                bo_qua.append(f"dong {stt}: action={d.get('action')!r} != {a.action!r}")
                continue
            if d.get("nguoi_cap") not in NGUOI_CO_THAM_QUYEN:
                bo_qua.append(f"dong {stt}: nguoi_cap={d.get('nguoi_cap')!r} ngoai danh sach")
                continue
            if not SHA_RE.match(str(d.get("head_sha"))):
                bo_qua.append(f"dong {stt}: head_sha khong phai sha40")
                continue
            khai[d["head_sha"]] = d
    # Một merge được coi là CÓ KHAI khi khai báo neo vào ĐÚNG head đã merge (cha thứ hai),
    # không phải vào commit merge. Neo sai chỗ thì con số vô nghĩa.
    co_khai, khong = [], []
    for sha, tieu_de in merges:
        p2 = subprocess.run(["git", "-C", a.root, "rev-parse", sha + "^2"],
                            capture_output=True, text=True).stdout.strip()
        # CHI cha thu hai. Ban truoc chu thich noi "khong phai commit merge" nhung MA lai
        # nhan CA HAI — loi khai va hanh vi lech nhau, va ca test mang ten ay khong he dung
        # mot ban ghi neo vao commit merge de do chieu do. Luc KHAI thi commit merge CHUA
        # TON TAI, nen neo vao no la neo vao thu chua co.
        (co_khai if p2 in khai else khong).append((sha, tieu_de))
    print(f"cua so: {bien_day_du}..{a.nhanh} (first-parent)")
    print(f"so khai bao: {so}")
    if bo_qua:
        print(f"BO QUA {len(bo_qua)} ban ghi khong hop luoc do:")
        for x in bo_qua[:10]:
            print(f"      {x}")
    print(f"merge trên {a.nhanh}: {len(merges)}")
    print(f"  CÓ khai báo    : {len(co_khai)}")
    print(f"  KHÔNG khai báo : {len(khong)}")
    for sha, td in khong[:20]:
        print(f"      {sha[:12]}  {td[:80]}")
    print("LƯU Ý: 'có khai báo' nghĩa là CÓ NGƯỜI GÕ LỆNH GHI, không nghĩa là đã được duyệt.")
    print("Phiên tự gõ được lệnh ấy. Con số này đo TẦN SUẤT, không đo THẨM QUYỀN.")
    return RC_OK


# Số từ tối thiểu để nguồn đối chiếu có nghĩa. Dưới ngưỡng này thì tập n-gram rỗng
# hoặc gần rỗng, và cổng sẽ "sạch" vì KHÔNG ĐO ĐƯỢC chứ không vì cây sạch.
_PROTO_TU_TOI_THIEU = 200


def _doc_nguon_protocol(root: Path) -> list[str]:
    """Văn bản logic của `docs/PROTOCOL_DA_PHIEN.md` DƯỚI `root` (bỏ code fence).

    FAIL-CLOSE, và đây là điểm khác bản trước. Bản trước trả `[]` cho BỐN tình huống
    khác hẳn nhau — tệp vắng, không đọc được, quá ngắn, rỗng sau khi bỏ fence — rồi
    người gọi viết `if proto_words:` nên cả bốn đều thành "bỏ qua trong im lặng". Đo
    được cả bốn: chép nguyên văn 25 từ vào adapter mà cổng vẫn `rc=0`. Một cổng tự tắt
    khi thiếu nguồn là cổng không tồn tại đúng lúc nó cần nhất.

    Chính hàm `cmd_doctrine_scan` đã fail-close cho tệp ĐÍCH (`_die(RC_ARG, ...)` khi
    `read_text` ném) — bản trước đặt chính sách NGƯỢC LẠI cho tệp NGUỒN, cùng một cặp
    ngoại lệ, cách nhau mười lăm dòng.

    KHÔNG còn fallback ra `Path(__file__).parents[2]`. Fallback ấy làm `--root` KHÔNG
    điều khiển cơ sở so sánh: quét cây X mà đo theo protocol của cây chứa SCRIPT. Cùng
    hình dạng với lỗi `t24` đã ghi trong `CLAUDE.md`. Đo được: hai ca test mới đỏ CHỈ
    nhờ fallback này, vì `_repo_gia` không hề dựng `docs/`.
    """
    p = root / "docs" / "PROTOCOL_DA_PHIEN.md"
    if not p.is_file():
        _die(RC_ARG, f"KHÔNG ĐO ĐƯỢC: thiếu nguồn đối chiếu {p} — `doctrine-scan` so "
                     f"adapter với protocol DƯỚI `--root`; không có nó thì phép đo "
                     f"không tồn tại, và `rc=0` ở đây sẽ là lời khai sai")
    try:
        raw = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        _die(RC_ARG, f"KHÔNG ĐO ĐƯỢC: không đọc được nguồn đối chiếu {p}: {e}")
    khong_code = re.sub(r"```[\s\S]*?```", " ", raw)
    phang, _ = _phang_ca_tep(khong_code)
    tu = phang.split()
    if len(tu) < _PROTO_TU_TOI_THIEU:
        _die(RC_ARG, f"KHÔNG ĐO ĐƯỢC: nguồn đối chiếu {p} chỉ còn {len(tu)} từ sau khi "
                     f"bỏ code fence (tối thiểu {_PROTO_TU_TOI_THIEU}) — tập n-gram quá "
                     f"nghèo để kết luận, `rc=0` sẽ là 'chưa đo' chứ không phải 'sạch'")
    return tu


def cmd_doctrine_scan(a, state_dir: Path) -> int:
    root = Path(a.root)
    muc_tieu: list[Path] = []
    skills = root / ".claude" / "skills"
    if skills.is_dir():
        muc_tieu.extend(sorted(skills.rglob("*.md")))
    agents_skills = root / ".agents" / "skills"
    if agents_skills.is_dir():
        muc_tieu.extend(sorted(agents_skills.rglob("*.md")))
    claude_md = root / "CLAUDE.md"
    if claude_md.is_file():
        muc_tieu.append(claude_md)
    for extra in a.path or []:
        muc_tieu.append(Path(extra))

    proto_words = _doc_nguon_protocol(root)
    proto_cache: dict[int, set[tuple[str, ...]]] = {}

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

        # `proto_words` luôn khác rỗng: `_doc_nguon_protocol` fail-close.
        # Giữ nhánh này thì cửa thứ năm lại mở ra trong im lặng.
        if True:
            file_words = phang.split()
            is_claude_md = (f.name == "CLAUDE.md")
            # Ngưỡng n-gram: 10 từ cho skills/adapters, 15 từ cho CLAUDE.md.
            # VÌ SAO CLAUDE.md CẦN NGƯỠNG 15 (đo được, không phải võ đoán — LỚP 4):
            # CLAUDE.md có dẫn chứng câu bài học nguyên văn dài đúng 13 từ từ protocol
            # ("cùng họ cổng vắng mặt trông giống cổng xanh, đổi đối tượng: một").
            # Đo trên master: ngưỡng 10 có 11 hits, 11 có 7 hits, 12 có 4 hits,
            # 13 có 2 hits, 14 có 0 hits, 15 có 0 hits. Ngưỡng 15 là cận an toàn
            # tối thiểu để không bắt oan câu dẫn giải bài học trong CLAUDE.md,
            # trong khi vẫn chặn đứng việc sao chép đoạn dài (>= 15 từ).
            # Các adapter trong .claude/skills và .agents/skills không được dẫn giải
            # câu chữ dài như vậy nên giữ ngưỡng nghiêm ngặt 10 từ.
            threshold = 15 if is_claude_md else 10
            if len(file_words) >= threshold and len(proto_words) >= threshold:
                if threshold not in proto_cache:
                    proto_cache[threshold] = {
                        tuple(proto_words[i : i + threshold])
                        for i in range(len(proto_words) - threshold + 1)
                    }
                proto_set = proto_cache[threshold]
                matched_indices = set()
                for i in range(len(file_words) - threshold + 1):
                    ngram = tuple(file_words[i : i + threshold])
                    if ngram in proto_set:
                        for idx in range(i, i + threshold):
                            matched_indices.add(idx)

                if matched_indices:
                    word_spans = []
                    cur_pos = 0
                    for w in file_words:
                        idx = phang.find(w, cur_pos)
                        word_spans.append((idx, idx + len(w)))
                        cur_pos = idx + len(w)

                    sorted_indices = sorted(matched_indices)
                    ranges = []
                    start = sorted_indices[0]
                    prev = sorted_indices[0]
                    for idx in sorted_indices[1:]:
                        if idx == prev + 1:
                            prev = idx
                        else:
                            ranges.append((start, prev))
                            start = idx
                            prev = idx
                    ranges.append((start, prev))

                    for start_w, end_w in ranges:
                        so_tu = end_w - start_w + 1
                        bat_dau_char = word_spans[start_w][0]
                        dong_dinh = _dong_tai(ban_do, bat_dau_char)
                        doan_chep = " ".join(file_words[start_w : end_w + 1])
                        dinh.append((str(f), "chep-protocol", f"({so_tu} từ) {doan_chep[:60]}...", dong_dinh))

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


def _la_dang_commit(s: str) -> bool:
    """Chuỗi này có THỂ là một commit sha không?

    KHÔNG hỏi "commit ấy có tồn tại không" — `packet_loop.py` chạy được ở cây không có
    lịch sử ấy, và hỏi git là mở một phụ thuộc mới cho một phép đếm. Chỉ hỏi HÌNH DẠNG:
    hex, dài từ 7 (độ viết tắt ngắn nhất git chấp) tới 64 (sha256).
    """
    return 7 <= len(s) <= 64 and all(c in "0123456789abcdef" for c in s)


def _be_rong_oid_cua_kho(root: Path) -> tuple[int, ...]:
    """Hỏi object format; không hỏi được thì giữ phép phân loại cũ."""
    try:
        p = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel", "--show-object-format"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=5,
        )
        ket_qua = p.stdout.removesuffix("\n").rsplit("\n", 1)
        if p.returncode != 0:
            return (40, 64)
        if len(ket_qua) != 2:
            return (40, 64)
        dong_dau = ket_qua[0]
        try:
            cung_goc = Path(dong_dau).resolve() == root.resolve()
        except ValueError:
            return (40, 64)
        if not cung_goc:
            return (40, 64)
    except (OSError, RuntimeError, subprocess.SubprocessError):
        return (40, 64)
    return {"sha1": (40,), "sha256": (64,)}.get(ket_qua[1].strip(), (40, 64))


def _khoa_neo_cac_sha(ds: list[dict], root: Path) -> list[str]:
    """Chuẩn hoá cách viết SHA theo object format; mơ hồ thì KHÔNG ĐO ĐƯỢC.

    Chuỗi bằng nhau cùng khoá. Một viết tắt chỉ nhập với OID đầy đủ (SHA-1 40 hoặc
    SHA-256 64 ký tự) khi đúng MỘT OID trong tập bắt đầu bằng nó. Không có OID đầy đủ
    mà hai cách viết lồng tiền tố, hoặc một viết tắt khớp nhiều OID, thì không đủ dữ
    liệu để phán chúng cùng hay khác commit — không được tự chọn một xô.
    """
    shas = [str(d.get("reviewed_sha") or "").strip().lower() for d in ds]
    hop_le = sorted({s for s in shas if _la_dang_commit(s)})
    be_rong_oid = _be_rong_oid_cua_kho(root)
    day_du = [s for s in hop_le if len(s) in be_rong_oid]
    khoa_theo_sha = {}
    for sha in hop_le:
        ung_vien_day_du = [s for s in day_du if s.startswith(sha)]
        if len(ung_vien_day_du) > 1:
            _die(RC_BIEN_NHAN, "KHÔNG ĐO ĐƯỢC: `reviewed_sha` viết tắt "
                 f"{sha!r} khớp nhiều OID đầy đủ: {ung_vien_day_du}")
        if ung_vien_day_du:
            khoa_theo_sha[sha] = ung_vien_day_du[0]
            continue
        long_nhau = [s for s in hop_le if s != sha
                     and (s.startswith(sha) or sha.startswith(s))]
        if long_nhau:
            _die(RC_BIEN_NHAN, "KHÔNG ĐO ĐƯỢC: các `reviewed_sha` viết tắt lồng "
                 f"tiền tố nhưng không có OID đầy đủ phân giải: {[sha, *long_nhau]}")
        khoa_theo_sha[sha] = sha
    return [khoa_theo_sha.get(sha, "__khong_neo_duoc__") for sha in shas]


def _verdict_trong_kho(thu_muc: Path, gia_tri) -> bool:
    """`verdict_path` có trỏ một tệp THẬT nằm TRONG `ops/reviews` của chính kho này không?

    Bản đầu chỉ hỏi `(root / verdict_path).is_file()`, và cross-review lượt 2 của #298 phá
    được bằng HAI đường — cả hai đã tái hiện, `rc=0` ở nơi phải `rc=11`:

      · ĐƯỜNG DẪN TUYỆT ĐỐI. `pathlib` định nghĩa `a / "/x"` == `Path("/x")` — vế trái bị
        VỨT. Nên một biên nhận trỏ `/tmp/bất-kỳ.md` khiến phép kiểm hoá ra hỏi về chính tệp
        ngoài kho ấy, và nó có thật, nên biên nhận được tính là một vòng review hợp lệ.
      · SYMLINK. `is_file()` đi THEO liên kết, nên `ops/reviews/link.md -> /ngoài/kho.md`
        cũng đạt.

    Cả hai biến bộ lọc mồ côi thành phép đo "có một tệp nào đó tồn tại ở đâu đó" thay vì
    "verdict nằm trong kho này". Chốt đúng phải neo vào CÂY, không vào sự tồn tại:
    từ chối đường dẫn tuyệt đối, `resolve()` để đi hết symlink, rồi đòi đích cuối nằm
    trong `ops/reviews`. Ba trạng thái: trong · ngoài · không phân giải được — hai cái sau
    đều KHÔNG được tính.
    """
    s = str(gia_tri or "").strip()
    if not s or Path(s).is_absolute():
        return False
    try:
        dich = (thu_muc.parent.parent / s).resolve(strict=True)
        goc = thu_muc.resolve(strict=True)
    except (OSError, RuntimeError):
        return False
    try:
        dich.relative_to(goc)
    except ValueError:
        return False
    return dich.is_file()


def _doc_bien_nhan(thu_muc: Path) -> list:
    """Đọc mọi `*.receipt.yaml`. YAML hỏng ⇒ KHÔNG ĐO ĐƯỢC, KHÔNG phải "không có".

    Ba trạng thái, không phải hai. Một bộ đếm trả `0` cho cả "chưa ai ghi biên nhận" lẫn
    "không đọc được thư mục" là bộ đếm nói dối đúng lúc nó cần nói thật: hai câu ấy đòi hai
    hành động ngược nhau (ghi biên nhận · sửa môi trường), mà con số thì giống hệt.
    """
    try:
        import yaml
    except ModuleNotFoundError:
        _die(RC_BIEN_NHAN,
             "KHÔNG ĐO ĐƯỢC: thiếu PyYAML nên không đọc được biên nhận nào. Đây KHÔNG "
             "phải 'packet có 0 biên nhận'. Cài: pip install PyYAML")
    ds = []
    for f in sorted(thu_muc.glob("*.receipt.yaml")):
        try:
            # Bộ đếm chỉ so scalar theo TỪ VỰNG. SafeLoader áp luật kiểu YAML 1.1,
            # biến `0123456` thành số bát phân 42798 và phá chính khoá SHA.
            d = yaml.load(f.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        except Exception as ex:  # noqa: BLE001 — mọi lỗi đọc đều là KHÔNG ĐO ĐƯỢC
            _die(RC_BIEN_NHAN, f"KHÔNG ĐO ĐƯỢC: {f.name} không đọc được như YAML: {ex}")
        if not isinstance(d, dict):
            _die(RC_BIEN_NHAN, f"KHÔNG ĐO ĐƯỢC: {f.name} không phải một ánh xạ YAML")
        d["_tep"] = f.name
        ds.append(d)
    return ds


def cmd_bien_nhan(a, state_dir: Path) -> int:
    """B2 — đếm biên nhận review; B3 — ĐỎ khi packet có 0 biên nhận `role: reviewer`.

    VÌ SAO CÓ (đo được, không phải lo xa): kho ĐÃ có bộ đếm bền — `ops/reviews/*.receipt.yaml`
    nằm trong git nên sống sót container — và ĐÃ có hai cổng `t26`/`t27` gác nó. Nhưng `t27`
    duyệt `glob("*-verdict.md")`, tức nó gác thứ ĐÃ được ghi ra đĩa và mù hoàn toàn với
    verdict chưa ai viết. Packet #249 chạy BỐN vòng cross-review, để lại **0** biên nhận, và
    suite vẫn 98/98 xanh. Chuỗi `doctor-github-mcp` trước đó mất **năm** lượt y hệt — biên
    nhận đầu tiên của kho tự khai điều ấy ở dòng đầu.

    PHẠM VI — bản đầu của docstring này khai RỘNG HƠN thứ lệnh cưỡng chế, và cross-review lượt 1
    của #298 bắt đúng chỗ đó (`s2-dem-tep-tu-nhan-reviewer`, P2): nó khai "nói đúng bằng thứ nó
    cưỡng chế" trong khi chỉ lọc dict YAML theo `packet_id` + `role`, nên HAI biên nhận trùng
    một vòng, cùng trỏ vào một `verdict_path` KHÔNG TỒN TẠI, vẫn được đếm là 2 và qua cổng.

    Nay phạm vi là: một biên nhận chỉ được TÍNH khi (a) `role: reviewer`, (b) khớp packet bằng
    SO BẰNG chuỗi trên `packet_id` hoặc `packet_slug` — không phải chuỗi con, và (c) `verdict_path`
    trỏ một tệp CÓ THẬT NẰM TRONG `ops/reviews` (không phải đường dẫn tuyệt đối, không qua symlink
    ra ngoài). Biên nhận trùng khoá neo đếm là MỘT.

    ĐƠN VỊ ĐẾM KHÔNG PHẢI "VÒNG REVIEW" mà là **số biên nhận PHÂN BIỆT ĐƯỢC**. Khoá neo
    giữ nguyên scalar YAML rồi chuẩn hoá viết tắt vào đúng một OID đầy đủ cùng tiền tố;
    thiếu/rỗng/sai dạng gom hết về MỘT xô, còn tiền tố mơ hồ làm cổng ĐỎ.

    MỘT chỗ hở còn lại: hiện vật cục bộ chỉ chứng minh có biên nhận + verdict tự khai,
    không chứng minh commit tồn tại hoặc có bao nhiêu vòng review đã thật sự chạy. Đóng
    khoảng ấy đòi hỏi authority ngoài hai tệp (git/GitHub); lệnh này cố ý không mở phụ
    thuộc git và có 0 đường ra mạng, nên không được gọi số đếm này là số vòng review.
    """
    # NGƯỠNG 0 HOẶC ÂM BIẾN CỔNG THÀNH CỔNG TỰ TẮT — `--toi-thieu 0` cho `rc=0` trên một
    # packet có 0 biên nhận, tức đúng ca B3 sinh ra để bắt. Một cổng tắt được bằng chính cờ
    # của nó thì không phải cổng.
    if a.toi_thieu < 1:
        _die(RC_ARG, f"--toi-thieu phải >= 1 (nhận {a.toi_thieu}): ngưỡng 0 hoặc âm làm cổng "
                     f"luôn xanh, kể cả khi packet có 0 biên nhận nào")
    root = Path(a.root)
    thu_muc = root / "ops" / "reviews"

    # "Không thấy thì bỏ qua" là cách một ca ĐẠT mà không ĐO gì (bài học `t24`).
    # Chỉ tha khi cây rõ ràng là bản sao rời; trong kho thật mà thiếu thì ĐỎ.
    if not thu_muc.is_dir():
        if (root / ".git").exists():
            _die(RC_BIEN_NHAN,
                 f"KHÔNG ĐO ĐƯỢC: kho thật mà không có {thu_muc} — không phải 'sạch'")
        print(f"bien-nhan: bỏ qua — {thu_muc} không có và cây không phải kho git")
        return RC_OK

    ds = _doc_bien_nhan(thu_muc)
    muon = None if a.packet is None else str(a.packet).strip()

    def khop(d) -> bool:
        if muon is None:
            return True
        return muon in {str(d.get("packet_id") or "").strip(),
                        str(d.get("packet_slug") or "").strip()}

    hop = [d for d in ds if khop(d)]
    # Đếm theo VAI, không theo TỆP. Một biên nhận `role: executor` nằm cùng thư mục KHÔNG
    # chứng minh có ai review — đó là trục phân biệt, và `bien_nhan_chi_dem_role_reviewer`
    # là ca khoá nó.
    rv = [d for d in hop if str(d.get("role") or "").strip() == "reviewer"]

    # MỒ CÔI: biên nhận trỏ vào một verdict KHÔNG TỒN TẠI không chứng minh có ai review — nó
    # chứng minh có ai ghi một tệp YAML. `t26` của `ops/lease_publish_test.py` đã gác chuyện này
    # cho các biên nhận ĐANG có mặt, nhưng lệnh này chạy được ở cây không có bộ test ấy, nên nó
    # phải tự đo chứ không mượn.
    mo_coi = [d for d in rv
              if not _verdict_trong_kho(thu_muc, d.get("verdict_path"))]
    that = [d for d in rv if d not in mo_coi]

    # TRÙNG VÒNG: hai biên nhận cùng `reviewed_sha` là cùng MỘT vòng ghi hai lần. Đếm chúng là 2
    # thì `--toi-thieu` lấp được bằng cách chép tệp — cổng đo SỐ TỆP chứ không đo SỐ VÒNG.
    thay, vong = set(), []
    khoa_theo_bien_nhan = _khoa_neo_cac_sha(that, root)
    for d, khoa in zip(that, khoa_theo_bien_nhan):
        # KHOÁ VÒNG PHẢI LÀ THỨ NEO ĐƯỢC VÀO MỘT COMMIT — không phải một chuỗi tự khai.
        #
        # Bệnh này đã có NĂM dạng. Chốt ở BIÊN CHUẨN HOÁ thay vì nối thêm một nhánh:
        #   (1) lượt 1 — đếm theo TỆP: hai biên nhận cùng `reviewed_sha` tính là 2.
        #   (2) lượt 2 — vẫn theo TỆP ở nhánh THIẾU sha: khoá rơi về
        #       `f"__khong_sha__{tệp}"`, nên chép tệp là nhân số vòng.
        #   (3) lượt 3 — theo GIÁ TRỊ TỰ KHAI: `reviewed_sha` CÓ mặt nhưng là rác
        #       (`rac-1`, `rac-2`, …). Ba chuỗi rác khác nhau ⇒ 3 vòng, `rc=0`.
        #
        #   (4) cùng OID đầy đủ + viết tắt từng là hai khoá;
        #   (5) YAML từng đổi scalar toàn số thành int trước khi khoá nhìn thấy nó.
        # `_doc_bien_nhan` giữ từ vựng; `_khoa_neo_cac_sha` lập lớp tương đương tiền tố
        # có đúng một OID đầy đủ. Dữ liệu mơ hồ là KHÔNG ĐO ĐƯỢC, không phải một con số.
        if khoa in thay:
            continue
        thay.add(khoa)
        vong.append(d)

    nhan = "mọi packet" if muon is None else f"packet {muon!r}"
    print(f"bien-nhan: {nhan} — {len(vong)} biên nhận PHÂN BIỆT ĐƯỢC "
          f"(từ {len(that)} biên nhận `role: reviewer` hợp lệ / {len(hop)} khớp packet "
          f"/ {len(ds)} toàn thư mục)")
    for d in vong:
        print(f"  {d.get('verdict', '?')!s:20s} luot={d.get('luot', '?')!s:3s} "
              f"{str(d.get('reviewed_sha') or '?')[:12]}  {d['_tep']}")
    for d in mo_coi:
        print(f"  BỎ (mồ côi) verdict_path không có thật: "
              f"{str(d.get('verdict_path') or '?')!r}  {d['_tep']}")
    if len(that) > len(vong):
        print(f"  GỘP {len(that) - len(vong)} biên nhận trùng KHOÁ NEO — cùng "
              f"một khoá ghi nhiều lần, đếm MỘT")

    if len(vong) < a.toi_thieu:
        _die(RC_BIEN_NHAN,
             f"{nhan}: {len(vong)} biên nhận PHÂN BIỆT ĐƯỢC, đòi tối thiểu {a.toi_thieu}. "
             f"Một vòng review không để lại biên nhận là một vòng không ai tra được sau khi "
             f"container chết — và không cổng nào khác thấy điều đó.")
    return RC_OK


# --- #770 `kiem-gate`: gate trên head cuối phải XANH THẬT ----------------------------
#
# VÌ SAO CÓ: trong vòng vá, lượt `gate` tự chạy bị HUỶ theo chỉ thị, và trên giao diện lượt
# huỷ với lượt xanh cùng hiện là "completed". Hỏi "có check nào completed không" là hỏi
# chỗ tiện tay. Lệnh này đọc JSON check-runs do NGƯỜI GỌI lấy (không gọi mạng) và chỉ
# nhận đúng một kết luận: DANH SÁCH CHO PHÉP `completed` + `success` + đúng head. Danh
# sách cấm (`cancelled`, `failure`…) thua từ trong thiết kế — `stale`, `neutral`, `null`…
# đều lọt. Nó là cổng ĐỌC BẰNG CHỨNG, không xác thực nguồn của tệp.
_TRUONG_CHECK_RUN = (("id", (int,)), ("name", (str,)), ("head_sha", (str,)),
                     ("status", (str,)), ("conclusion", (str, type(None))))
_VANG = object()


def _cam_khoa_trung(cap: list) -> dict:
    """Khoá trùng ở BẤT KỲ tầng nào: decoder mặc định giữ vế cuối, tức tự chọn một vế
    của bằng chứng mâu thuẫn (`conclusion` cancelled rồi success ⇒ xanh). Cross-review #777 F01."""
    d: dict = {}
    for k, v in cap:
        if k in d:
            raise ValueError(f"khoá trùng {k!r} — bằng chứng mâu thuẫn")
        d[k] = v
    return d


def _cam_hang_ngoai_json(ten: str):
    raise ValueError(f"hằng {ten} không thuộc JSON chuẩn")


def _doc_check_runs(duong: str) -> list[dict]:
    """Đọc tệp check-runs; mọi chỗ không chắc là `KHÔNG ĐO ĐƯỢC` + `RC_GATE`, không đoán."""
    def hong(ly_do: str) -> None:
        _die(RC_GATE, f"KHÔNG ĐO ĐƯỢC: {duong}: {ly_do}")

    try:
        d = json.loads(Path(duong).read_text(encoding="utf-8"),
                       object_pairs_hook=_cam_khoa_trung, parse_constant=_cam_hang_ngoai_json)
    except (OSError, UnicodeDecodeError, ValueError, RecursionError) as ex:
        hong(f"không đọc được như JSON ({type(ex).__name__}: {ex})")
    trang = d if isinstance(d, list) else [d]
    if not trang:
        hong("list trang RỖNG — không có bằng chứng nào")
    runs: list[dict] = []
    tong_khai = 0
    for i, tr in enumerate(trang):
        if not isinstance(tr, dict) or not isinstance(tr.get("check_runs"), list):
            hong(f"trang {i} không phải object có `check_runs` là list")
        tc = tr.get("total_count", _VANG)
        if tc is not _VANG:
            if type(tc) is not int:
                hong(f"trang {i}: `total_count` không phải số nguyên: {tc!r}")
            tong_khai = max(tong_khai, tc)
        for j, r in enumerate(tr["check_runs"]):
            if not isinstance(r, dict):
                hong(f"trang {i} check_runs[{j}] không phải object")
            # `type(...) in kieu`, KHÔNG `isinstance`: `True` là `int` theo isinstance.
            sai = [k for k, kieu in _TRUONG_CHECK_RUN if type(r.get(k, _VANG)) not in kieu]
            if sai:
                hong(f"trang {i} check_runs[{j}] thiếu/sai kiểu trường {sai}")
            runs.append(r)
    # Thiếu trang thì lượt MỚI NHẤT có thể nằm ở trang chưa lấy — xanh khi ấy là xanh giả.
    so_id = len({r["id"] for r in runs})
    if so_id < tong_khai:
        hong(f"`total_count` khai {tong_khai} mà chỉ có {so_id} id — thiếu trang (`--paginate --slurp`)")
    return runs


def cmd_kiem_gate(a, state_dir: Path) -> int:
    if not SHA_RE.fullmatch(a.head):
        _die(RC_ARG, f"--head phải là SHA 40 ký tự hex thường, được {a.head!r}")
    ten_bb = list(dict.fromkeys(a.bat_buoc))   # trùng tên ⇒ tính MỘT lần, giữ thứ tự
    if any(not t.strip() for t in ten_bb):
        _die(RC_ARG, "--bat-buoc không được rỗng")
    runs = _doc_check_runs(a.check_runs)
    do: list[str] = []
    xanh: list[str] = []
    for ten in ten_bb:
        cung = [r for r in runs if r["name"] == ten]   # khớp TUYỆT ĐỐI
        if not cung:
            do.append(f"{ten!r}: VẮNG — không check-run nào mang đúng tên này")
            continue
        # Lượt bị huỷ rồi chạy lại: chỉ lượt `id` LỚN NHẤT có quyền nói. Trùng id thì
        # MỌI bản ghi của id ấy đều phải xanh — không tự chọn một bản.
        id_max = max(r["id"] for r in cung)
        for r in (r for r in cung if r["id"] == id_max):
            hop_le = (r["status"] == "completed" and r["conclusion"] == "success"
                      and r["head_sha"] == a.head)
            if not hop_le:
                do.append(f"{ten!r} id={r['id']}: status={r['status']!r} "
                          f"conclusion={r['conclusion']!r} head_sha={r['head_sha']!r}")
                break
        else:
            xanh.append(f"{ten} id={id_max}")
    if do:
        for dong in do:
            print(f"  ĐỎ  {dong}", file=sys.stderr)
        _die(RC_GATE, f"gate KHÔNG xanh trên {a.head}: {len(do)}/{len(ten_bb)} tên bắt buộc đỏ")
    print(f"gate XANH trên {a.head}: " + " · ".join(xanh))
    return RC_OK


def cmd_status(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    print(json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True))
    if st.get("dem_tu_suy"):
        print(CANH_BAO_V1, file=sys.stderr)
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
            "9 bảng ADR §20 lệch với docs/adr/ · 12 gate không xanh trên head."
        ),
    )
    p.add_argument("--state-dir", default=".claude/.packet_state", help="nơi giữ state cục bộ")
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("init", help="khởi tạo state cho một packet")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--mission", type=int, required=True)
    q.add_argument("--executor", required=True)
    q.add_argument("--reviewer", required=True)
    for role in ("executor", "reviewer"):
        q.add_argument(f"--{role}-model-family")
        q.add_argument(f"--{role}-execution-surface")
        q.add_argument(f"--{role}-transport")
    q.add_argument("--attempts-limit", type=int, default=MAC_DINH_TRAN_ATTEMPT)
    q.add_argument("--same-failure-limit", type=int, default=MAC_DINH_TRAN_SAME_FAILURE)
    q.add_argument("--review-rounds-limit", type=int, default=MAC_DINH_TRAN_VONG_REVIEW)
    q.add_argument("--codex-review-calls-limit", type=int, default=MAC_DINH_TRAN_CODEX)
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
    q.add_argument("--model-family")
    q.add_argument("--execution-surface")
    q.add_argument("--transport")
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
    q.add_argument("--model-family")
    q.add_argument("--execution-surface")
    q.add_argument("--transport")
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
    q.add_argument("--codex-call", help="run_id của record-codex-call (bắt buộc khi reviewer codex)")
    q.set_defaults(fn=cmd_record_review)

    q = sub.add_parser("record-codex-call", help="ghi lời gọi review codex; chặn TRƯỚC khi vượt trần")
    q.add_argument("--packet", type=int, required=True)
    for co in ("--head", "--run-id"):
        q.add_argument(co, required=True)
    q.set_defaults(fn=cmd_record_codex_call)

    q = sub.add_parser("nang-tran", help="nâng trần một trục (LỜI KHAI, không phải bằng chứng)")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--truc", required=True, choices=tuple(TRUC_TRAN))
    q.add_argument("--tran-moi", type=int, required=True)
    for co in ("--ai-nang", "--can-cu"):
        q.add_argument(co, required=True)
    q.set_defaults(fn=cmd_nang_tran)

    q = sub.add_parser("record-rescue", help="quyết định Review Rescue Checkpoint")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--quyet-dinh", required=True, choices=("nang_tran", "tach_stable_slice", "revision", "dung"))
    q.add_argument("--can-cu", required=True)
    q.set_defaults(fn=cmd_record_rescue)

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

    q = sub.add_parser("ghi-uy-quyen",
                       help="ghi KHAI BÁO uỷ quyền (lời khai, KHÔNG phải bằng chứng)")
    q.add_argument("--action", required=True, choices=HANH_VI_CHAN)
    q.add_argument("--nguoi-cap", required=True,
                   help="bên CÓ THẨM QUYỀN đã cấp; không được là tên provider")
    q.add_argument("--bang-chung", required=True, help="URL/ID dấu vết bền")
    q.add_argument("--head-sha", required=True, help="sha40 CHÍNH XÁC được uỷ quyền")
    q.set_defaults(fn=cmd_ghi_uy_quyen)

    q = sub.add_parser("doi-chieu-uy-quyen",
                       help="đếm merge so với khai báo — biến KHÔNG ĐO ĐƯỢC thành SỐ")
    q.add_argument("--root", default=".")
    q.add_argument("--nhanh", default="origin/master")
    q.add_argument("--since", required=True,
                   help="BAT BUOC — bien duoi cua cua so; khong co thi so khong tai lap duoc")
    q.add_argument("--action", default="merge", choices=HANH_VI_CHAN)
    q.add_argument("--so", help="so khai bao BEN (mac dinh: trong state-dir, bi gitignore)")
    q.set_defaults(fn=cmd_doi_chieu_uy_quyen)

    q = sub.add_parser("doctrine-scan", help="bắt adapter chép doctrine")
    q.add_argument("--root", default=".")
    q.add_argument("--path", action="append", help="quét thêm tệp cụ thể")
    q.set_defaults(fn=cmd_doctrine_scan)

    q = sub.add_parser("adr-song",
                       help="bảng §20 của protocol phải phủ hết docs/adr/")
    q.add_argument("--root", default=".")
    q.set_defaults(fn=cmd_adr_song)

    q = sub.add_parser("kiem-gate",
                       help="gate bắt buộc phải XANH THẬT trên head (đọc JSON check-runs)",
                       epilog="Mã thoát: 0 mọi tên bắt buộc xanh · 2 sai đối số · "
                              "12 gate không xanh trên head hoặc KHÔNG ĐO ĐƯỢC.")
    q.add_argument("--head", required=True, help="SHA 40 ký tự của head cần kiểm")
    q.add_argument("--check-runs", required=True, dest="check_runs",
                   help="tệp JSON: object có `check_runs`, hoặc list trang (`--slurp`)")
    q.add_argument("--bat-buoc", action="append", required=True, dest="bat_buoc",
                   help="tên check-run bắt buộc, khớp TUYỆT ĐỐI; lặp lại được")
    q.set_defaults(fn=cmd_kiem_gate)

    q = sub.add_parser("bien-nhan",
                       help="đếm biên nhận review; ĐỎ khi packet có 0 biên nhận reviewer")
    q.add_argument("--root", default=".")
    q.add_argument("--packet", help="số hiệu hoặc slug; bỏ trống = mọi packet")
    q.add_argument("--toi-thieu", type=int, default=1,
                   dest="toi_thieu", help="số biên nhận reviewer tối thiểu (mặc định 1)")
    q.set_defaults(fn=cmd_bien_nhan)

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
