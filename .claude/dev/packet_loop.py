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
import contextlib
import contextvars
import functools
import hashlib
import hmac
import html
import importlib.util
import io
import json
import os
import platform
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

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
CAN_CU_RE = re.compile(r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/(issues|pull)/[0-9]+#issuecomment-[0-9]+\Z")
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
    # #812 connector: init để trống surface/transport không phải giấy phép khai trái lease đã ghi — trường KHAI phải khớp lease.
    lease = st["ngu_canh_lease"].get(role) if isinstance(st.get("ngu_canh_lease"), dict) else None
    if isinstance(lease, dict) and any(lease.get(f) is not None and actual[f] is not None and actual[f] != lease[f]
                                       for f in ("provider", "model_family", "execution_surface", "transport")):
        _die(RC_PROVIDER, f"{role} runtime identity khác lease: {actual!r} != {lease!r}")

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
    # #812 M2: packet áp ADR-0054 — `record-review` (biên nhận H) vào; cửa ra `accept` thuộc #834.
    "approved_pending": (),
    # #813 M2/M3: vào bằng `mo-lai --nguyen-nhan connector`, ra CHỈ bằng `chu-kho-duyet` — không cạnh `transition` nào.
    "cho_chu_kho": (),
    "accepted": (),
    "blocked": (),
}

# Các state chỉ được ghi bởi luồng review, không bao giờ bởi `transition`.
# `reviewing` không nằm đây vì nó VÀO được bằng `transition` (từ `running`); thứ bị
# cấm là đường RA. Bảng `CHUYEN_HOP_LE` ở trên đã cưỡng chế điều đó.
STATE_CHI_DO_REVIEW_GHI = ("accepted", "approved_pending", "cho_chu_kho")

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
    tx = globals().get("_1174_TRANSACTION")
    if tx is None and not p.exists():
        _die(RC_STATE, f"chưa có state cho packet {packet} — chạy `init` trước ({p})")
    try:  # #775 bộ đọc NGHIÊM: lệch hình dạng hay bất biến sổ/bộ đếm ⇒ RC_STATE, không traceback, không đoán
        if tx is not None:
            _1174_require(Path(state_dir).resolve() == tx["directory"] and packet == tx["state"]["packet"], "transaction namespace")
            st = json.loads(_1174_bytes(tx["state"]))
        else:
            st = json.loads(p.read_text(encoding="utf-8"))
        if type(st) is dict and st.get("format") == "packet_state_retired.v1":
            _die(RC_STATE, "state retired: packet_state_retired.v1; reconciliation required")
        for role in ("executor", "reviewer"):
            identity = st.get(f"{role}_identity")
            if identity is not None and (type(identity) is not dict or role == "reviewer" and st["reviewer"] == "codex" and identity.get("model_family", PROVIDER_FAMILIES["codex"]) != "openai"):
                raise ValueError(f"{role}_identity")
        can_duoi = _la_codex(st) * sum(r.get("provider") == st["reviewer"] for r in st["reviews"])
        if type(st["schema_version"]) is int and st["schema_version"] == 1 and not st.keys() & {"review_rounds_used", "review_rounds_limit", "codex_review_calls_used", "codex_review_calls_limit", "codex_calls", "nang_tran", "dem_tu_suy"}:  # M6: SUY bộ đếm = cận DƯỚI ở trên — suy 0 là fail-open
            st.update(schema_version=2, review_rounds_used=len(st["reviews"]), codex_review_calls_used=can_duoi,
                      codex_calls=[], nang_tran=[], review_rounds_limit=MAC_DINH_TRAN_VONG_REVIEW,
                      codex_review_calls_limit=MAC_DINH_TRAN_CODEX, dem_tu_suy=True, attempt_open=st.get("attempt_open", False), reviewing_head_sha=st.get("reviewing_head_sha"))
        goi, posts, anchor = st["codex_calls"], st["posts"], st.get("attempt_anchor")
        pending = next((h.get("event") != "record_rescue" or h.get("mo_lai") is not True for h in reversed(st["history"]) if h.get("event") in ("blocked_rescue_required", "record_rescue")), False)
        vi_pham = [ten for ten, dung in (  # mỗi bất biến MỘT phần tử ⇒ mỗi cái một đột biến riêng
            ("schema", type(st["schema_version"]) is int and st["schema_version"] == (3 if tx is not None else 2) and type(st["packet"]) is int and st["packet"] == packet and st["state"] in CHUYEN_HOP_LE and type(st["mission"]) is int and st["executor"] in PROVIDERS and (st["reviewing_head_sha"] is None or SHA_RE.match(st["reviewing_head_sha"]))),
            ("bo-dem", all(type(st[k]) is int for k in ("attempts_used", "attempts_limit", "same_failure_limit")) and st["attempts_used"] >= 0 and all(type(st[u]) is int is type(st[t]) and st[u] >= 0 < st[t] for u, t in TRUC_TRAN.values())),
            ("so", all(type(st[k]) is list for k in ("codex_calls", "nang_tran", "reviews", "history"))
                   and all(r.get("provider") == st["reviewer"] and type(r.get("attempt")) is int for r in st["reviews"])
                   and all(type(h) is dict for h in st["history"]) and type(st.get("dem_tu_suy", False)) is bool and type(st["attempt_open"]) is bool
                   and type(st.get("finding_counts")) is dict and all(type(n) is int and n >= 0 for n in st["finding_counts"].values())),
            ("posts", type(posts) is dict and all(type(r) is dict and type(r["for"]) is str and (r["consumed_by"] is None or type(r["consumed_by"]) is str) for r in posts.values())),
            ("anchor", anchor is None or type(anchor) is dict and type(anchor["attempt"]) is int and type(anchor["consumed"]) is bool and re.fullmatch(r"[0-9a-f]{32}", anchor["nonce"]) and re.fullmatch(r"[0-9a-f]{64}", st["hmac_key"])),
            ("findings", st["finding_counts"] == {fid: sum(fid in r.get("finding_ids", []) for r in so) for so in [[*st["reviews"], *(  # #813: + sự kiện `mo_lai`
                h for h in st["history"] if h.get("event") == "mo_lai")]] for r in so for fid in r.get("finding_ids", [])}),
            ("loi-goi", all(set(g) == {"run_id", "head", "da_dung"} and RUN_ID_RE.match(g["run_id"])
                            and SHA_RE.match(g["head"]) and type(g["da_dung"]) is bool for g in goi)),
            ("dem-goi", len({g["run_id"] for g in goi}) == len(goi) <= st["codex_review_calls_used"] >= can_duoi + sum(not g["da_dung"] for g in goi)),
            ("dem-vong", st["review_rounds_used"] == len(st["reviews"])),
            ("adr0054", type(st.get("luat_adr0054", False)) is bool and (st.get("luat_adr0054") is not True or type(st.get("ngu_canh_lease")) is dict)
                        and (st["state"] != "approved_pending" or _pending_human_lane(st) and SHA_RE.match(str(st.get("pending_sha"))) and type(st.get("bien_nhan_approve")) is dict)
                        and (st.get("luat_adr0054") is not True or _nc_hop_le(st["ngu_canh_lease"]))),
            ("mo-lai", _quyen_hop_le(st.get("mo_lai_tu"), "nguyen_nhan", NGUYEN_NHAN_MO_LAI) and _quyen_hop_le(st.get("checkpoint_day"), "sha256", None)
                       and (st["state"] != "cho_chu_kho" or _pending_human_lane(st) and (st.get("mo_lai_tu") or {}).get("nguyen_nhan") == "connector")),
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
    tx = globals().get("_1174_TRANSACTION")
    if tx is not None:
        _1174_require(not tx.get("read_only", False), "read-only state context")
        _1174_require(Path(state_dir).resolve() == tx["directory"] and st["packet"] == tx["state"]["packet"], "transaction save namespace")
        tx["proposal"] = json.loads(_1174_bytes(st))
        return
    state_dir.mkdir(parents=True, exist_ok=True)
    p = _state_path(state_dir, st["packet"])
    # Mọi lỗi serialization/encoding là lỗi đầu vào: đo TRƯỚC khi mở/truncate state.
    try:
        raw = (json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    except (ValueError, TypeError, UnicodeError) as ex:
        _die(RC_STATE, f"state không mã hoá được: {type(ex).__name__}")
    p.write_bytes(raw)


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
    try:
        return d.astimezone(timezone.utc)
    except OverflowError:
        _die(RC_ARG, f"--expires-utc vượt biên UTC: {chuoi!r}")


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
    moi, cu = (a.lease_ref, a.lease_path, a.lease_comments), (a.lease_id, a.granted_by, a.evidence, a.expires_utc)
    moi_co = any(x is not None for x in moi)
    cu_co = any(x is not None for x in cu)
    if moi_co == cu_co or not all(moi if moi_co else cu):  # #812 M1: hai đường LOẠI TRỪ nhau
        _die(RC_ARG, "chọn ĐÚNG một đường: --lease-ref/--lease-path/--lease-comments HOẶC "
                     "--lease-id/--granted-by/--evidence/--expires-utc, đủ cờ của đường ấy")
    _xet_dung(state_dir, st, "record-lease")
    if st["state"] != "awaiting_lease":
        _die(RC_STATE,
             f"chỉ ghi được lease khi packet đang 'awaiting_lease'; hiện là {st['state']!r}. "
             f"Ghi đè lease của một packet đang chạy là hồi sinh một lượt đã cạn.")
    if moi_co:
        return _record_lease_ref(a, state_dir, st)
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
    st["luat_adr0054"] = False  # I9: đường cũ LUÔN luật cũ — chế độ chỉ xác định ở đường lease ref
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
    if not isinstance(st.get("hmac_key"), str) or not re.fullmatch(r"[0-9a-f]{64}", st["hmac_key"]):
        _die(RC_STATE, "state thiếu/hỏng khoá toàn vẹn — không nâng cấp state cũ ngầm")
    anh = _kiem_anh_moi_truong(getattr(a, "bang_chung_moi_truong", None)
                               or os.environ.get(BIEN_BANG_CHUNG), can_sach=True)
    _xet_dung(state_dir, st, "begin-attempt")  # I4: sau khi mọi đầu vào đã được xác thực
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


def _pending_human_lane(st):
    """Historical activation or the current admission already verified under lock.

    The transaction admission comes from the canonical resolver, never a stored
    opt-in bit. Keep the observed global ADR-0054 policy unchanged in the journal.
    """
    tx = globals().get("_1174_TRANSACTION")
    admission = tx.get("admission") if type(tx) is dict else None
    scoped = (type(admission) is dict and st.get("schema_version") == 3 and
        all(st.get(k) == admission[k] for k in ("packet", "mission", "generation")) and
        st.get("enrollment_id") == admission["enrollment"]["id"] and
        st.get("binding_sha256") == admission["enrollment"]["binding_sha256"] and
        _nc_hop_le(st.get("ngu_canh_lease")) and
        st["ngu_canh_lease"]["generation"] == admission["generation"] and
        type(st.get("lease")) is dict and st["lease"]["lease_id"] == st["ngu_canh_lease"]["lease_id"])
    return st.get("luat_adr0054") is True or scoped


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

    # #812 M2: packet áp ADR-0054 ghi MỌI verdict qua biên nhận H; `--verdict` một mình không đủ.
    bn = _du_dieu_kien_approve(st, a) if _pending_human_lane(st) else None
    _xet_dung(state_dir, st, "record-review")  # I4: chỉ sau khi MỌI đầu vào đã được xác thực

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

    _xet_dung(state_dir, st, "record-review", a, cham_tran)  # M4: kết quả đã ghi sổ ⇒ xét dừng

    st["state"] = {"approve": "approved_pending" if bn and a.verdict == "approve" else "accepted", "changes_requested": "running", "blocked": "blocked"}[a.verdict]
    if bn and a.verdict == "approve":
        st.update(pending_sha=a.reviewed_sha, bien_nhan_approve=bn)
    elif a.verdict == "approve":
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
    u, t = TRUC_TRAN.get(st.get("truc"), ("", ""))  # mở lại chỉ khi trần > đã dùng VÀ có bản ghi M4 ĐỦ HÌNH DẠNG (người nâng, căn cứ, trần cũ < mới) khớp trần hiện tại
    mo = (nang := a.quyet_dinh == "nang_tran") and st[t] > st[u] and any(type(n) is dict and n.get("truc") == st["truc"] and n.get("tran_moi") == st[t] and type(n.get("tran_cu")) is int and n["tran_cu"] < st[t] and n.get("ai_nang") in NGUOI_CO_THAM_QUYEN and bool(CAN_CU_RE.match(str(n.get("can_cu")))) for n in st["nang_tran"])
    st["history"].append(dict(event="record_rescue", quyet_dinh=a.quyet_dinh, truc=st.get("truc"), can_cu=a.can_cu, mo_lai=mo))
    if mo:
        st["state"] = "running"; del st["ly_do"], st["truc"]
    _save(state_dir, st)
    if nang and not mo:
        _die(RC_STATE, f"trục {st['truc']} chưa có bản ghi nâng trần khớp trần hiện tại và lớn hơn số đã dùng — chạy `nang-tran` trước")
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
        if s == "0063":
            for anchor in ADR0063_ANCHORS:
                if anchor not in than_adr:
                    loi.append(f"ADR-0063: thiếu contract anchor {anchor}")
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
# #788 (spec `ops/specs/wp788.md`): run cùng TÊN có thể đến từ workflow khác — neo `app` không phân
# biệt được (đo `bb8c0c4`: cả 30 run cùng `app.id`), neo `check_suite.id` thì được. Và
# `total_count` vắng/0/âm từng làm phép kiểm thiếu trang im lặng bỏ qua (P1 connector PR #777).
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
        snapshots = (globals().get("_1174_TRANSACTION") or {}).get("input_snapshots", {})
        raw = snapshots[str(duong)] if str(duong) in snapshots else Path(duong).read_bytes()
        d = json.loads(raw.decode("utf-8"),
                       object_pairs_hook=_cam_khoa_trung, parse_constant=_cam_hang_ngoai_json)
    except (OSError, UnicodeDecodeError, ValueError, RecursionError) as ex:
        hong(f"không đọc được như JSON ({type(ex).__name__}: {ex})")
    trang = d if isinstance(d, list) else [d]
    if not trang:
        hong("list trang RỖNG — không có bằng chứng nào")
    runs: list[dict] = []
    khai: list[int] = []
    for i, tr in enumerate(trang):
        if not isinstance(tr, dict) or not isinstance(tr.get("check_runs"), list):
            hong(f"trang {i} không phải object có `check_runs` là list")
        # #788 N5: vắng `total_count` là KHÔNG biết đã đủ trang — không phải "đủ".
        tc = tr.get("total_count", _VANG)
        if tc is _VANG:
            hong(f"trang {i} thiếu `total_count` — không biết đã đủ trang chưa")
        if type(tc) is not int or tc < 0:
            hong(f"trang {i}: `total_count` không phải số nguyên ≥ 0: {tc!r}")
        khai.append(tc)
        for j, r in enumerate(tr["check_runs"]):
            if not isinstance(r, dict):
                hong(f"trang {i} check_runs[{j}] không phải object")
            # `type(...) in kieu`, KHÔNG `isinstance`: `True` là `int` theo isinstance.
            sai = [k for k, kieu in _TRUONG_CHECK_RUN if type(r.get(k, _VANG)) not in kieu]
            if sai:
                hong(f"trang {i} check_runs[{j}] thiếu/sai kiểu trường {sai}")
            # #788 N2: MỌI phần tử, không chỉ run bắt buộc.
            cs = r.get("check_suite", _VANG)
            if not isinstance(cs, dict) or type(cs.get("id", _VANG)) is not int:
                hong(f"trang {i} check_runs[{j}] `check_suite` không phải object có `id` số nguyên: {cs!r}")
            runs.append(r)
    # #788 F01 (H3): cùng `id` là cùng MỘT check-run; danh tính mâu thuẫn mà để bước lọc tên/suite
    # bỏ bản lệch thì cấp xanh giả — kiểm ở ĐÂY, nơi còn mọi bản ghi của mọi trang, trước mọi lọc.
    danh_tinh: dict = {}
    for r in runs:
        dt = (r["name"], r["check_suite"]["id"], r["head_sha"])
        if danh_tinh.setdefault(r["id"], dt) != dt:
            hong(f"id {r['id']} mang hai danh tính {danh_tinh[r['id']]!r} và {dt!r} — bằng chứng mâu thuẫn")
    tong_khai = khai[0]
    if any(t != tong_khai for t in khai):
        hong(f"các trang khai `total_count` khác nhau {khai} — không phải cùng một lần lấy")
    # Thiếu trang thì lượt MỚI NHẤT có thể nằm ở trang chưa lấy — xanh khi ấy là xanh giả.
    # THỪA id cũng không phải một lần lấy trọn vẹn (ghép tệp?) — đòi BẰNG ĐÚNG, không `<`.
    so_id = len({r["id"] for r in runs})
    if so_id != tong_khai:
        hong(f"`total_count` khai {tong_khai} mà có {so_id} id — "
             + ("thiếu trang (`--paginate --slurp`)" if so_id < tong_khai else "THỪA id, không phải một lần lấy"))
    return runs


def cmd_kiem_gate(a, state_dir: Path) -> int:
    if not SHA_RE.fullmatch(a.head):
        _die(RC_ARG, f"--head phải là SHA 40 ký tự hex thường, được {a.head!r}")
    # `[0-9]`, KHÔNG `\d`: `int()` nhận cả chữ số Unicode.
    if not re.fullmatch(r"[1-9][0-9]*", a.check_suite):
        _die(RC_ARG, f"--check-suite phải là số nguyên dương thập phân (không dấu, không số 0 đầu), "
                     f"được {a.check_suite!r}")
    try:
        suite = int(a.check_suite)
    except ValueError:   # F02: vượt trần chữ số của `int()`; `json` chịu đúng trần ấy nên không id
        suite = a.check_suite   # nào khớp — giữ CHUỖI (≠ mọi int) ⇒ VẮNG, không traceback
    ten_bb = list(dict.fromkeys(a.bat_buoc))   # trùng tên ⇒ tính MỘT lần, giữ thứ tự
    # F04 (chủ kho chốt 18-10): tên chứa ký tự ngắt dòng (mọi thứ `splitlines()` cắt) bị TỪ CHỐI —
    # dòng cảnh báo N4 in tên nguyên văn, và chỉ tên bắt buộc được in, nên nó luôn là MỘT dòng.
    if any(not t.strip() or t.splitlines() != [t] for t in ten_bb):
        _die(RC_ARG, "--bat-buoc không được rỗng hoặc chứa ký tự xuống dòng")
    runs = _doc_check_runs(a.check_runs)
    # N4: run cùng tên ở suite KHÁC là producer khác — bỏ qua, nhưng nói ra. Chỉ tên bắt buộc.
    for ten_cb in ten_bb:
        # id PHÂN BIỆT (F05: bản lặp là một run); tên NGUYÊN VĂN trong nháy đơn (F04: không `!r`).
        khac = sorted({r["id"] for r in runs if r["name"] == ten_cb and r["check_suite"]["id"] != suite})
        if khac:
            print(f"CẢNH BÁO: '{ten_cb}' có {len(khac)} run ở suite khác "
                  f"({', '.join(map(str, khac))}) — bỏ qua", file=sys.stderr)
    do: list[str] = []
    xanh: list[str] = []
    for ten in ten_bb:
        cung = [r for r in runs if r["name"] == ten]   # khớp TUYỆT ĐỐI
        cung = [r for r in cung if r["check_suite"]["id"] == suite]   # #788 N3: chỉ suite đã neo
        if not cung:
            do.append(f"{ten!r}: VẮNG — không check-run nào mang đúng tên này trong suite {suite}")
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
    print(f"gate XANH trên {a.head} (suite {suite}): " + " · ".join(xanh))
    return RC_OK


# --- #812 MAY-ADR-0054-a (r2 `ops/specs/wp812-r2.md` + phần chung, I1–I11; `accept`/I7 ở #834). Đ = git do CHÍNH tiến trình này
# fetch/ls-remote · H = lease/biên nhận qua validator CANON (cả phụ thuộc) chép từ `origin/master` · R = readback người gọi lấy. I4: `_die` TRƯỚC `_save`.
ADR0054_TEP = "docs/adr/0054-push-mot-lan-dung-va-theo-hang-va-review-theo-lop.md"
LUAT_0054_RE = re.compile(rb"^luat_push_va_dung_va: ADR-0054@([0-9a-f]{40})$", re.M)
HANG_LOP = ("P0", "P1", "P2", "P3")
CHECK_BAT_BUOC = tuple((".github/workflows/ci.yml", f"{j} (ubuntu-latest)") for j in ("gate", "gate-cong-cu-gop", "gate-ops", "gate-packet-loop", "gate-registry"))
BOT_LEASE, RC_DANG_GIU_LEASE = "github-actions[bot]", 11  # `ops/lease_publish.py::RC_DANG_GIU` — `ai-dang-giu` có người giữ
CANON = ("ops/lease_publish.py", "ops/bien_nhan_v2.py", ".claude/dev/launcher.py", "AGENTS.md", "docs/PROTOCOL_DA_PHIEN.md")  # validator + nguồn nó đọc
HO_CANON = {"claude": "claude", "openai": "gpt", "gemini": "gemini"}  # MODEL_FAMILIES → `bien_nhan_v2.HO_MODEL_CHO_PHEP`
REPO_RE = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/issues/([0-9]+)#issuecomment-[0-9]{1,30}\Z")
KHOA_NGU_CANH = ("lease_id", "lease_ref", "lease_oid", "lease_path", "repo", "branch", "generation", "spec_hash", "assurance_target",
                 "executor", "reviewer", "required_checks")


_1174_SCOPED = contextvars.ContextVar("wp1174_scoped", default=False)


def _1174_scoped(fn):
    @functools.wraps(fn)
    def scoped(*args, **kwargs):
        token = _1174_SCOPED.set(True)
        try:
            return fn(*args, **kwargs)
        finally:
            _1174_SCOPED.reset(token)
    return scoped


def _git_do(root: Path, *args, deadline=None) -> tuple[int, bytes]:
    try:
        remaining=300 if deadline is None else min(300,deadline-time.time())
        if remaining<=0:return -1,b""
        scoped = _1174_SCOPED.get() or deadline is not None
        p = subprocess.run(["git", *(["--no-replace-objects"] if scoped else []), "-C", str(root), *args],
                           **({"env": _1174_git_env()} if scoped else {}), capture_output=True, timeout=remaining)
        if deadline is not None and time.time()>=deadline:return -1,b""
        return p.returncode, p.stdout
    except (OSError, subprocess.SubprocessError, ValueError):
        return -1, b""


@contextlib.contextmanager
def _canon(root: Path, oid: str | None = None):
    """Validator CANON (+ nguồn nó đọc) từ `origin/master`; `oid` ⇒ thêm `snap/` là worktree Git tách rời TẠI lease OID (cùng refs
    với kho, để validator đo bia mộ/ref). Dọn sạch kể cả khi `_die` ném SystemExit."""
    td = Path(tempfile.mkdtemp(prefix="pl812-canon-"))
    try:
        for p in CANON:
            rc, b = _git_do(root, "show", f"refs/remotes/origin/master:{p}")
            if rc != 0 or not b:
                _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: không đọc được {p} trên origin/master")
            (td / p).parent.mkdir(parents=True, exist_ok=True), (td / p).write_bytes(b)
        if oid and _git_do(root, "worktree", "add", "-q", "--detach", str(td / "snap"), oid)[0]:
            _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: không dựng được worktree tại {oid[:12]}")
        yield td
    finally:
        if (td / "snap").exists():
            _git_do(root, "worktree", "remove", "--force", str(td / "snap"))
        shutil.rmtree(td, ignore_errors=True)


def _nap(td: Path, ten: str):
    spec = importlib.util.spec_from_file_location(f"{ten}_canon", td / "ops" / f"{ten}.py")
    try:
        spec.loader.exec_module(m := importlib.util.module_from_spec(spec))
    except Exception as ex:  # loader canon: lỗi nguồn phải có mã thoát được kiểm soát
        _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: nạp validator canon {ten}: {type(ex).__name__}")
    api = ("PROVIDER_NGUON_HONG", "ASSURANCE_CAN_DOC_LAP", "HO_MODEL_CHO_PHEP", "_thieu", "_neo_git",
           "_nguon_tra_model", "_giai_ho_model_reviewer", "_giai_ho_model_executor", "_chuoi", "_chuan_hoa_provider")
    if ten == "bien_nhan_v2" and any(not hasattr(m, k) for k in api):
        _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: validator canon {ten} thiếu giao diện")
    if ten == "bien_nhan_v2":
        tap = ("ASSURANCE_CAN_DOC_LAP", "HO_MODEL_CHO_PHEP")
        if (any(type(getattr(m, k)) not in (set, frozenset) or not getattr(m, k)
                or not all(type(x) is str and x for x in getattr(m, k)) for k in tap)
                or any(not callable(getattr(m, k)) for k in api[3:])):
            _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: validator canon {ten} giao diện sai kiểu")
    return m


def _chay_canon(*args, **kwargs):
    try:
        if _1174_SCOPED.get():
            kwargs.setdefault("env", _1174_git_env())
        return subprocess.run(*args, **kwargs)
    except (OSError, subprocess.SubprocessError, ValueError) as ex:
        _die(RC_GUARD, f"KHÔNG ĐO ĐƯỢC: chạy validator canon: {type(ex).__name__}")


def _ten_provider(p):
    """Bí danh canon (`launcher._PROVIDER_BI_DANH`, `_TRANSPORT_CONTRACTS`: `anthropic_claude`/`openai_codex`) → tên của `PROVIDERS`."""
    import launcher
    if type(p) is not str:
        return None
    p = p.strip()  # I8: bản chiếu identity lease
    p = dict(launcher._PROVIDER_BI_DANH).get(p, p)
    return next((lenh[0] for prov, lenh, *_ in launcher._TRANSPORT_CONTRACTS if prov == p and lenh[0] in PROVIDERS), p)


def _ds_duong(v) -> list:
    if type(v) is not list or not all(type(x) is str for x in v):
        raise TypeError(f"write set không phải list chuỗi: {v!r}")  # sai kiểu ⇒ KHÔNG_XÁC_ĐỊNH, không bỏ qua
    return v


def _chuan_duong(p: str) -> str:
    """§5: một biểu diễn cho mọi cách viết — bỏ `planned:`, separator `/`, NFC, casefold, bỏ `./`; tuyệt đối/`..` ⇒ ValueError (không đo được)."""
    q = unicodedata.normalize("NFC", p.removeprefix("planned:").strip().replace("\\", "/")).casefold()
    parts = [x for x in q.split("/") if x not in ("", ".")]
    if not parts or q.startswith("/") or ".." in parts or ":" in parts[0]:
        raise ValueError(f"đường dẫn ngoài miền §5: {p!r}")
    return "/".join(parts)


def _bieu_dien_duong(p: str, root: Path) -> set[str]:
    """§5: kiểm mọi đường, cả khi không có đối thủ; giữ cả tên khai và đích symlink/parent."""
    q = p.removeprefix("planned:").strip().replace("\\", "/")
    if "." in q.split("/"):
        raise ValueError(f"đường dẫn có thành phần '.': {p!r}")
    if any(c in q for c in "*?[]"):
        raise ValueError(f"write set không nhận glob: {p!r}")
    ten = _chuan_duong(p)  # kiểm absolute/.. TRƯỚC phép resolve
    goc = root.resolve()
    dich = (goc / q).resolve(strict=False).relative_to(goc)
    return {ten, _chuan_duong(dich.as_posix())}


def _dich_trong_cay(root: Path, rev: str, p: str) -> str:
    """§5 theo CÂY Git tại `rev` (không theo checkout): phân giải symlink từng thành phần; thoát gốc/vòng/không đọc được ⇒ ValueError."""
    phan, ra, buoc = p.removeprefix("planned:").strip().replace("\\", "/").split("/"), [], 0
    while phan:
        x = phan.pop(0)
        if x in ("", "."):
            continue
        if x == "..":
            if not ra:
                raise ValueError(f"symlink thoát gốc tại {rev}: {p!r}")
            ra.pop()
            continue
        # §5: thành phần khớp entry THẬT của cây theo NFC + casefold (không theo byte) — `ALIAS` vẫn là symlink `alias`.
        rc, ls = _git_do(root, "ls-tree", "-z", rev, *(("--", "/".join(ra) + "/") if ra else ()))
        if rc:
            raise ValueError(f"không đọc được cây {rev} cho {p!r}")
        khoa = lambda s: unicodedata.normalize("NFC", s).casefold()  # noqa: E731
        khop = [(meta, ten.rsplit("/", 1)[-1]) for meta, _, ten in (e.partition("\t") for e in ls.decode("utf-8", "surrogateescape").split("\0") if e)
                if khoa(ten.rsplit("/", 1)[-1]) == khoa(x)]
        if len(khop) > 1:
            raise ValueError(f"thành phần {x!r} khớp nhiều entry tại {rev}: {[t for _, t in khop]}")
        x = khop[0][1] if khop else x
        if khop and khop[0][0].startswith("120000 "):
            rc, dich = _git_do(root, "cat-file", "blob", f"{rev}:{'/'.join([*ra, x])}")
            buoc += 1
            if rc or buoc > 40 or dich.startswith(b"/"):
                raise ValueError(f"symlink không phân giải được tại {rev}: {p!r}")
            phan = dich.decode("utf-8", "surrogateescape").split("/") + phan
        else:
            ra.append(x)
    return _chuan_duong("/".join(ra))


def _giao(a: str, b: str) -> bool:
    """§5: giao nhau khi bằng nhau hoặc một bên là prefix thư mục của bên kia — so trên biểu diễn chuẩn hoá."""
    a, b = _chuan_duong(a), _chuan_duong(b)
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def _nc_hop_le(nc) -> bool:
    """Lược đồ LỒNG của ngữ cảnh lease trong state — thiếu/sai hình dạng ⇒ `_load` báo state hỏng, không traceback ở cửa sau."""
    return (type(nc) is dict and set(nc) == set(KHOA_NGU_CANH) and type(nc["generation"]) is int and nc["generation"] > 0
            and all(type(nc[k]) is str and nc[k].strip() for k in ("lease_id", "lease_ref", "lease_path", "branch", "spec_hash", "assurance_target"))
            and type(nc["lease_oid"]) is str and bool(SHA_RE.match(nc["lease_oid"])) and type(nc["repo"]) is str
            and bool(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", nc["repo"]))
            and all(type(nc[v]) is dict and set(nc[v]) == {"provider", "model_family", "execution_surface", "transport"}
                    and nc[v]["provider"] in PROVIDERS and nc[v]["model_family"] in MODEL_FAMILIES
                    and (nc[v]["execution_surface"] is None or type(nc[v]["execution_surface"]) is str
                         and nc[v]["execution_surface"] in RUNTIME_CAPABILITIES[nc[v]["provider"]])
                    and (nc[v]["transport"] is None or type(nc[v]["transport"]) is str
                         and nc[v]["transport"] in {t for surface, ts in RUNTIME_CAPABILITIES[nc[v]["provider"]].items()
                                                   if nc[v]["execution_surface"] in (None, surface) for t in ts}) for v in ("executor", "reviewer"))
            and type(nc["required_checks"]) is list and all(type(x) in (list, tuple) and len(x) == 2 and all(type(y) is str and y for y in x)
                                                             for x in nc["required_checks"]))


def _ngu_canh_lease(l: dict, ref: str, oid: str, path: str, repo: str) -> dict:
    """M1: hàm DUY NHẤT dựng tập khoá ngữ cảnh lease (`KHOA_NGU_CANH`; `record-lease` ghi, `record-review` đọc)."""
    rc = l.get("required_checks", [])
    if type(rc) is not list or not all(type(x) is list and len(x) == 2 and all(type(s) is str and s for s in x) for x in rc):
        _die(RC_ARG, "lease `required_checks` phải là list các cặp [workflow, job]")
    return {"lease_id": l["lease_id"], "lease_ref": ref, "lease_oid": oid, "lease_path": path, "repo": repo,
            "branch": l["branch"], "generation": l["generation"], "spec_hash": l["spec_hash"], "assurance_target": l["assurance_target"],
            "executor": _identity(_ten_provider(l.get("provider")), l.get("model_family"), l.get("execution_surface"), l.get("transport")),
            "reviewer": _identity(_ten_provider(l.get("reviewer")), l.get("reviewer_model_family"), l.get("reviewer_execution_surface"), l.get("reviewer_transport")),
            "required_checks": sorted({tuple(x) for x in CHECK_BAT_BUOC} | {tuple(x) for x in rc})}


def _che_do_0054(root: Path, spec: bytes) -> bool:
    """Đúng MỘT dòng khai + ba phép đo land-OID của ADR-0052 (đường dẫn ADR-0054) + đã kích hoạt; không đo được ⇒ False."""
    khai = LUAT_0054_RE.findall(spec)
    if len(khai) != 1:
        return False
    oid, m = khai[0].decode(), "refs/remotes/origin/master"
    chuoi, ls, pr = _git_do(root, "rev-list", "--first-parent", m), _git_do(root, "ls-tree", "-z", m, "docs/adr/"), _git_do(root, "show", f"{m}:docs/PROTOCOL_DA_PHIEN.md")
    nfc = lambda b: unicodedata.normalize("NFC", b.decode("utf-8", "replace"))  # noqa: E731
    dong20 = [d for d in nfc(pr[1]).splitlines() if re.match(r"^\|\s*`ADR-0054`\s*\|", d)]
    # wp929 (số 0055 đã thuộc ADR trần lời gọi Codex, #919) — ADR kích hoạt nhận theo CỤM khai, không theo số tệp; đúng MỘT tệp.
    # Chỉ blob tệp thường: `git show` của tree in tên con, của symlink in đích — cụm nằm trong TÊN không phải lời khai (review #1 P2)
    adr = [_git_do(root, "show", f"{m}:{t}") for k, _, t in (e.partition("\t") for e in ls[1].decode("utf-8", "replace").split("\0"))
           if k.split(" ")[:2] in (["100644", "blob"], ["100755", "blob"]) and re.fullmatch(r"docs/adr/[0-9]{4}-[^/]+\.md", t) and t != ADR0054_TEP]
    kich = [b for rc, b in adr if "kích hoạt `ADR-0054`" in nfc(b)]
    return (_git_do(root, "rev-parse", "--is-shallow-repository") == (0, b"false\n")
            and _git_do(root, "cat-file", "-e", f"{oid}:{ADR0054_TEP}")[0] == 0
            and _git_do(root, "cat-file", "-e", f"{oid}^1:{ADR0054_TEP}")[0] != 0
            and chuoi[0] == 0 and oid.encode() in chuoi[1].split()
            and ls[0] == 0 and all(rc == 0 for rc, _ in adr) and len(kich) == 1
            and pr[0] == 0 and len(dong20) == 1 and "chưa kích hoạt" not in dong20[0].casefold())


def _verify_lease_ref(a, st: dict):
    """M1 đường MỚI: lease từ ref REMOTE vừa fetch; I2 (H check trên snapshot tại lease OID · Đ ai-dang-giu · R comment workflow);
    đặc tả theo `spec_hash`; ghi ngữ cảnh lease rồi MỚI xác định chế độ."""
    import yaml
    root, m = Path(a.root), re.fullmatch(r"origin/([A-Za-z0-9._/-]+)", a.lease_ref)
    if not m or ".." in a.lease_ref or _git_do(root, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")[0]:
        _die(RC_ARG, f"--lease-ref phải là origin/<nhánh> và `git fetch origin` phải chạy được: {a.lease_ref!r}")
    xa, gan = _git_do(root, "ls-remote", "origin", f"refs/heads/{m[1]}"), _git_do(root, "rev-parse", "-q", "--verify", f"refs/remotes/origin/{m[1]}^{{commit}}")
    oid = gan[1].decode().strip()
    if xa[0] or gan[0] or xa[1].split() != [oid.encode(), f"refs/heads/{m[1]}".encode()]:
        _die(RC_GUARD, f"{a.lease_ref} không có trên remote hoặc lệch ls-remote — lease ở ref cục bộ không có thẩm quyền")
    rc, raw = _git_do(root, "show", f"{oid}:{a.lease_path}")
    try:
        l = yaml.safe_load(raw) if rc == 0 else None
    except (yaml.YAMLError, RecursionError):
        l = None
    kieu = {"lease_id": str, "branch": str, "spec_path": str, "spec_hash": str, "assurance_target": str, "granted_on_instruction": str,
            "prompt_path": str, "generation": int, "packet_issue": int}
    ten_id = ("model_family", "execution_surface", "transport", "reviewer_model_family", "reviewer_execution_surface", "reviewer_transport")
    ws = (l.get("effective_write_set") if "effective_write_set" in l else l.get("write_set")) if isinstance(l, dict) else None
    mr = REPO_RE.fullmatch(str(l.get("granted_on_instruction"))) if isinstance(l, dict) else None
    if not isinstance(l, dict) or any(type(l.get(k)) is not t for k, t in kieu.items()) or l["packet_issue"] != st["packet"] or not mr \
            or mr[2].lstrip("0") != str(st["packet"]) or type(ws) is not list or not ws or not all(type(x) is str and x for x in ws) \
            or any(PurePosixPath(l[k]).is_absolute() or ".." in PurePosixPath(l[k]).parts for k in ("prompt_path", "spec_path")) \
            or l.get("role") != "executor" or l["generation"] < 1 or any(k in l and (type(l[k]) is not str or not l[k].strip()) for k in ten_id) \
            or any(t is str and not l[k].strip() for k, t in kieu.items()) or type(l.get("write_set")) is not list or not l["write_set"] \
            or not all(type(x) is str and x for x in l["write_set"]):
        _die(RC_ARG, f"lease {a.lease_path} tại {oid[:12]} hỏng: sai kiểu/miền {sorted(kieu)} + role/identity, khác packet {st['packet']}, "
                     f"không có write set, đường dẫn thoát gốc, hoặc granted_on_instruction không trỏ chính Packet Issue")
    lid = l["lease_id"]
    with _canon(root, oid) as td:
        (td / "lease.yaml").write_bytes(raw)
        p = _chay_canon([*(lp := [sys.executable, str(td / "ops" / "lease_publish.py")]), "check", str(td / "lease.yaml"), "--root", str(td / "snap")], capture_output=True)
        if p.returncode:  # I2(H) trên worktree Git TẠI lease OID, không trên worktree của ứng viên
            _die(RC_GUARD, f"I2(H): lease_publish check rc={p.returncode}: {p.stderr.decode('utf-8', 'replace').strip()[-300:]}")
        bnv_lease = _nap(td, "bien_nhan_v2")
        if bnv_lease.PROVIDER_NGUON_HONG is not None:
            _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: nguồn canon hỏng: {bnv_lease.PROVIDER_NGUON_HONG}")
        if l["assurance_target"] not in bnv_lease.ASSURANCE_CAN_DOC_LAP:
            _die(RC_ARG, f"assurance_target {l['assurance_target']!r} ngoài miền của protocol")
        for duong in l["write_set"]:  # I2(Đ): sau fetch đủ ref, lease này là người giữ DUY NHẤT từng đường dẫn KHAI BÁO…
            p = _chay_canon([*lp, "ai-dang-giu", duong.removeprefix("planned:"), "--root", str(root)], capture_output=True)
            if p.returncode != RC_DANG_GIU_LEASE or p.stdout.decode("utf-8", "replace").strip().splitlines()[-1:] != [f"NGƯỜI_GIỮ 1: {lid}"]:
                _die(RC_GUARD, f"I2(Đ): ai-dang-giu {duong} không trả {lid} là người giữ duy nhất (rc={p.returncode})")
        try:  # …và KHÔNG lease còn hiệu lực nào khác GIAO write set HIỆU LỰC (§5 chuẩn hoá, prefix hai chiều, cả write_set lẫn effective_write_set)
            lpm = _nap(td, "lease_publish")
            cac = lpm._quet_lease_toan_kho(root, chan_nhanh_tut_sau=True)
            giu = lambda x: [y for k in ("write_set", "effective_write_set") for y in _ds_duong(x.get(k, []))]  # noqa: E731
            # Đối xứng: write_set ∪ effective_write_set của CẢ HAI bên, không để effective che tập khai.
            # Symlink phân giải theo checkout VÀ theo cây của cả hai lease (snapshot lease này + ref lease kia) — topology chỉ có
            # trong một ref không được lọt vì checkout của người gọi thiếu nó (#812 connector).
            bd = lambda x, revs: _bieu_dien_duong(x, root) | {_dich_trong_cay(root, r, x) for r in revs}  # noqa: E731
            for x in giu(l):  # §5 cả khi không có đối thủ: đường dẫn không đo được ⇒ KHÔNG_XÁC_ĐỊNH
                bd(x, (oid,))
            giao_nhau = []
            for m in cac:
                other = m["lease"]
                if lpm._lease_id_quet(other.get("lease_id")) == lid or lpm._phan_loai_lease(other) != "CÒN_HẠN" or lpm._bia_mo_doi_xung(other, cac) is True:
                    continue
                revs = (oid, m["ref"])
                paths = set().union(*(bd(x, revs) for x in giu(other)))
                own_m = set().union(*(bd(x, revs) for x in giu(l)))
                if any(_giao(x, y) for x in own_m for y in paths):
                    giao_nhau.append(f"{m['ref']}:{m['path']}")
            giao_nhau = sorted(set(giao_nhau))
        except Exception as ex:  # noqa: BLE001 — không đo được ⇒ không có thẩm quyền
            _die(RC_GUARD, f"I2(Đ): KHÔNG_XÁC_ĐỊNH khi quét lease toàn kho: {type(ex).__name__}: {str(ex)[:300]}")
        if giao_nhau:
            _die(RC_GUARD, f"I2(Đ): lease khác còn hiệu lực giao write set của {lid}: {giao_nhau}")
    try:
        cm = json.JSONDecoder(parse_constant=_cam_hang_ngoai_json, object_pairs_hook=_cam_khoa_trung).decode((raw_cm := Path(a.lease_comments).read_bytes()).decode("utf-8"))
    except (OSError, ValueError, RecursionError) as ex:
        _die(RC_ARG, f"KHÔNG ĐO ĐƯỢC: {a.lease_comments}: {type(ex).__name__}")
    ds = [c for t in (cm if isinstance(cm, list) else [cm]) for c in (t if isinstance(t, list) else [t])]
    if not any(isinstance(c, dict) and isinstance(c.get("user"), dict) and c["user"].get("login") == BOT_LEASE
               and c.get("issue_url") in (f"https://api.github.com/repos/{mr[1]}/issues/{st['packet']}", f"https://github.com/{mr[1]}/issues/{st['packet']}")
               and re.search(rf"^lease_id: {re.escape(lid)}$", str(c.get("body", "")), re.M) for c in ds):
        _die(RC_GUARD, f"I2(R): không comment nào của {BOT_LEASE} trên issue #{st['packet']} chứa `lease_id: {lid}` — workflow chưa đăng")
    rc, spec = _git_do(root, "show", f"{oid}:{l['spec_path']}")
    if rc or hashlib.sha256(spec).hexdigest() != l["spec_hash"]:
        _die(RC_ARG, f"đặc tả {l['spec_path']} tại {oid[:12]} lệch `spec_hash` của lease")
    nc = _ngu_canh_lease(l, a.lease_ref, oid, a.lease_path, mr[1])
    if not _nc_hop_le(json.loads(json.dumps(nc))):  # CÙNG lược đồ mà `_load` đọc lại — không ghi một state mà lần đọc sau gọi là hỏng
        _die(RC_ARG, f"ngữ cảnh lease dựng từ {a.lease_path} không qua lược đồ state")
    for vai in ("executor", "reviewer"):
        if any(v is not None and nc[vai][k] != v for k, v in (st.get(f"{vai}_identity") or {}).items()):
            _die(RC_PROVIDER, f"{vai} của lease {nc[vai]!r} khác state {st.get(f'{vai}_identity')!r}")
    lease = _kiem_luoc_do_lease({"lease_id": lid, "granted_by": l.get("granted_by"), "evidence": l["granted_on_instruction"], "expires_utc": l.get("lease_expires_at_utc")}, RC_ARG)
    che_do = _che_do_0054(root, spec)
    return dict(lease=lease, context=nc, mode=che_do, comments_sha256=hashlib.sha256(raw_cm).hexdigest())


def _record_lease_ref(a, state_dir: Path, st: dict) -> int:
    return _apply_lease_ref(a, state_dir, st, _verify_lease_ref(a, st))


def _apply_lease_ref(a, state_dir, st, facts):
    lease, nc, che_do = facts["lease"], facts["context"], facts["mode"]
    lid, oid = lease["lease_id"], nc["lease_oid"]
    st.update(lease=lease, state="leased", luat_adr0054=che_do, ngu_canh_lease=nc)
    st["history"].append({"event": "record_lease_ref", "lease_id": lid, "lease_oid": oid, "luat_adr0054": che_do,
                          "lease_comments_sha256": facts["comments_sha256"]})
    _save(state_dir, st)
    print(f"đã ghi lease {lid} từ {a.lease_ref}@{oid[:12]} — luat_adr0054={che_do} — state leased")
    return RC_OK


def _du_dieu_kien_approve(st: dict, a) -> dict:
    """M2 — vị từ DÙNG CHUNG cho MỌI verdict của packet áp ADR-0054: verdict TRONG biên nhận H phải khớp `--verdict`; biên nhận qua
    `_thieu` + `_neo_git` của validator canon (nguồn hỏng ⇒ từ chối); I8: danh tính chuẩn hoá (bí danh canon) khớp lease ở cả hai vai —
    provider, và surface/transport khi biên nhận khai; họ theo `model_family` lease khai; I10; bảng lớp đúng lược đồ; approve không còn
    P0–P2; verdict âm chỉ dùng slug có trong bảng lớp (I11)."""
    import yaml
    try:
        d = yaml.safe_load(raw := Path(a.bien_nhan).read_bytes())
    except Exception as ex:  # noqa: BLE001 — thiếu cờ/tệp/YAML hỏng đều là KHÔNG ĐO ĐƯỢC
        _die(RC_BIEN_NHAN, f"packet áp ADR-0054: review phải kèm --bien-nhan đọc được ({type(ex).__name__})")
    with _canon(Path(a.root)) as td:
        bnv = _nap(td, "bien_nhan_v2")
        if bnv.PROVIDER_NGUON_HONG is not None or not set(HO_CANON.values()) <= bnv.HO_MODEL_CHO_PHEP:
            _die(RC_BIEN_NHAN, f"KHÔNG ĐO ĐƯỢC: validator canon thiếu nguồn ({bnv.PROVIDER_NGUON_HONG}) hoặc HO_CANON trôi khỏi miền canon")
        d = d if isinstance(d, dict) else {}
        nc, lop = st["ngu_canh_lease"], d.get("bang_lop")
        mri = d["model_reviewer_identity"] if isinstance(d.get("model_reviewer_identity"), dict) else {}
        mei = d["model_executor_identity"] if isinstance(d.get("model_executor_identity"), dict) else {}
        # Dùng ĐÚNG bảng nguồn mà canon tra cho cả hai vai, kể cả fallback top-level và bí danh.
        kieu_sai = [f"{vai}.{pre}{k}" for vai in ("reviewer", "executor") for x, pre in bnv._nguon_tra_model(d, vai)[1]
                    for k in ("provider", "surface", "transport", "model_family", "ho_model", "canonical_model", "model", "model_evidence",
                              "bang_chung_model", "model_evidence_ref", "telemetry_path", "nguoi_audit", "audit_actor")
                    if pre + k in x and (type(x[pre + k]) is not str or not x[pre + k].strip())]
        kieu_sai += [f"model_{vai}_identity" for vai in ("reviewer", "executor")
                     if f"model_{vai}_identity" in d and type(d[f"model_{vai}_identity"]) is not dict]
        # `_thieu` còn đọc các tham chiếu CÓ tiền tố ngay bên trong khối executor.
        kieu_sai += [f"executor.{k}" for k in ("executor_model_evidence_ref", "executor_telemetry_path", "executor_nguoi_audit", "executor_audit_actor")
                     if k in mei and (type(mei[k]) is not str or not mei[k].strip())]
        kieu_sai += [f"reviewer.{k}" for k in ("che_do", "session_run_id", "KHONG_do_duoc")
                     if k in mri and (type(mri[k]) is not str or not mri[k].strip())]
        if "phien_doc_lap" in mri and type(mri["phien_doc_lap"]) is not bool:
            kieu_sai.append("reviewer.phien_doc_lap")
        if type(d.get("schema_version")) is not int:
            kieu_sai.append("schema_version")
        if kieu_sai:  # có mặt mà sai kiểu KHÔNG phải vắng — dừng trước mọi phép chuẩn hoá/fallback
            _die(RC_BIEN_NHAN, f"biên nhận {a.bien_nhan}: trường danh tính sai kiểu/rỗng {kieu_sai}")
        # Chỉ chuẩn hoá bản chiếu dùng để SO; schema/Git/hash vẫn đo biên nhận nguyên byte.
        import ast
        cay = ast.parse((td / ".claude/dev/launcher.py").read_text(encoding="utf-8"))
        bd_bm = dict(next(ast.literal_eval(n.value) for n in cay.body if isinstance(n, ast.Assign)
                          and len(n.targets) == 1 and getattr(n.targets[0], "id", "") == "_BE_MAT_BI_DANH"))
        p_chuan = lambda x: _ten_provider(bnv._chuan_hoa_provider(bnv._chuoi(x) or ""))  # noqa: E731
        bm_chuan = lambda x: bd_bm.get(bnv._chuoi(x), bnv._chuoi(x))  # noqa: E731
        ho = lambda vai: HO_CANON[nc[vai]["model_family"]]  # noqa: E731 — họ LEASE KHAI, đổi sang miền canon của bien_nhan_v2
        ho_rev, ho_exec = bnv._giai_ho_model_reviewer(d)[0], bnv._giai_ho_model_executor(d)
        lop_ok = type(lop) is list and all(type(x) is dict and type(x.get("slug")) is str and SLUG_RE.fullmatch(x["slug"])
                                           and x.get("hang") in HANG_LOP for x in lop) and len({x["slug"] for x in lop}) == len(lop)
        try:
            neo = bnv._neo_git(Path(a.root), Path(a.bien_nhan).name, d) if d else (["không phải ánh xạ"], [])
            thieu = list(bnv._thieu(d) if d else [])
        except Exception as ex:  # H hỏng/không đo được vẫn phải giữ state và mã thoát có kiểm soát.
            _die(RC_BIEN_NHAN, f"KHÔNG ĐO ĐƯỢC: kiểm biên nhận canon: {type(ex).__name__}")
        loi = thieu + neo[0] + neo[1] + [ten for ten, dung in (
            ("verdict", d.get("verdict") == a.verdict), ("role", d.get("role") == "reviewer"),
            ("packet", type(d.get("packet_issue")) is int and d["packet_issue"] == st["packet"]),
            ("generation", type(d.get("generation")) is int and d["generation"] == nc["generation"]),
            ("reviewed_sha", d.get("reviewed_sha") == a.reviewed_sha), ("spec_hash", d.get("spec_hash") == nc["spec_hash"]),
            ("lease_id", d.get("lease_id") == nc["lease_id"]), ("assurance", d.get("assurance") == nc["assurance_target"]),
            ("provider-reviewer", p_chuan(mri.get("provider")) == nc["reviewer"]["provider"]),
            ("provider-executor", p_chuan(mei.get("provider", d.get("executor_provider"))) == nc["executor"]["provider"]),
            ("ho-reviewer", bool(ho_rev) and ho_rev == ho("reviewer")), ("ho-executor", bool(ho_exec) and ho_exec == ho("executor")),
            ("surface", nc["reviewer"]["execution_surface"] is not None and bm_chuan(mri.get("surface")) == nc["reviewer"]["execution_surface"]),
            ("transport", nc["reviewer"]["transport"] is not None and bnv._chuoi(mri.get("transport")) == nc["reviewer"]["transport"]),
            ("executor-surface-transport", all((bm_chuan(mei[k]) if k == "surface" else bnv._chuoi(mei[k])) == nc["executor"][f] for k, f in (("surface", "execution_surface"), ("transport", "transport")) if k in mei)),
            ("khac-ho", nc["assurance_target"] != "cross_approved" or ho_rev != ho_exec), ("bang-lop", lop_ok),
            ("con-P0-P2", lop_ok and (a.verdict != "approve" or not any(x["hang"] in HANG_LOP[:3] for x in lop))),
            ("slug-ngoai-bang", lop_ok and set(a.finding_id or []) <= {x["slug"] for x in lop}),
            # same-failure đếm theo `--finding-id`: verdict âm phải khai ĐỦ mọi lớp của bảng, bỏ một lớp tái diễn là né trần.
            ("thieu-lop-am", lop_ok and (a.verdict == "approve" or {x["slug"] for x in lop} <= set(a.finding_id or [])))) if not dung]
    if loi:
        _die(RC_BIEN_NHAN, f"biên nhận {a.bien_nhan} không đủ điều kiện {a.verdict}: {loi}")
    return {"tep": str(a.bien_nhan), "sha256": hashlib.sha256(raw).hexdigest(), "p3": sorted(x["slug"] for x in lop if x["hang"] == "P3"), "lop": lop}


# --- #834 MAY-ADR-0054-a2 (`ops/specs/wp834.md` + phần chung): cửa `accept` (approved_pending → accepted), I7 readback CI/connector, I11.
APP_CHECK, BOT_CONNECTOR, EP_CONNECTOR = "github-actions", "chatgpt-codex-connector[bot]", ("reviews", "review_comments", "issue_comments")
API_GH = "https://api.github.com/repos/"
BADGE_RE = re.compile(r"!\[([^\]]*?)\s*Badge\]", re.I)  # nhận diện TRƯỜNG badge độc lập với miền giá trị — `Q1`, `P 1` vẫn là badge (I3)


def _doc_json(duong: str, rc: int) -> tuple:
    try:
        snapshots = (globals().get("_1174_TRANSACTION") or {}).get("input_snapshots", {})
        b = snapshots[str(duong)] if str(duong) in snapshots else Path(duong).read_bytes()
        return json.JSONDecoder(parse_constant=_cam_hang_ngoai_json, object_pairs_hook=_cam_khoa_trung).decode(b.decode("utf-8")), hashlib.sha256(b).hexdigest()
    except (OSError, ValueError, RecursionError) as ex:  # UnicodeDecodeError là ValueError
        _die(rc, f"KHÔNG ĐO ĐƯỢC: {duong}: {type(ex).__name__}: {ex}")


def _trang_du(d, khoa: str, nhan: str) -> list:
    """I7: một lần lấy (mọi trang cùng `total_count`) · id int · tập id PHÂN BIỆT = `total_count` · cùng id thì CÙNG nội dung
    (bản mâu thuẫn bị từ chối trước mọi lọc/lập map, không tự chọn một vế). Trả một bản mỗi id."""
    cac = d if type(d) is list else [d]
    ok = bool(cac) and all(isinstance(t, dict) and isinstance(t.get(khoa), list) and type(t.get("total_count")) is int for t in cac)
    ds = [x for t in cac for x in t[khoa]] if ok else []
    if not ok or not all(isinstance(x, dict) and type(x.get("id")) is int for x in ds) or {t["total_count"] for t in cac} != {len({x["id"] for x in ds})}:
        _die(RC_GATE, f"KHÔNG ĐO ĐƯỢC: {nhan}: cần trang {{`{khoa}`, `total_count`}} cùng một lần lấy, id int, tập id phân biệt = total_count")
    moi = {}
    for x in ds:
        if json.dumps(moi.setdefault(x["id"], x), sort_keys=True) != json.dumps(x, sort_keys=True):
            _die(RC_GATE, f"{nhan}: id {x['id']} mang hai nội dung — bằng chứng mâu thuẫn")
    return list(moi.values())


def _neo_connector(k: str, x: dict, head: str, biet: set):
    """I7 neo head theo endpoint: 'hien' · 'cu' (neo head KHÁC hợp lệ) · 'hong' (thiếu/sai/mơ hồ) · None (issue comment không khai).
    Issue comment (dạng connector `**Reviewed commit:** `sha``): phần còn lại của DÒNG sau MỖI nhãn phải đúng một SHA 7–40 hex (backtick
    đủ cặp hoặc không), mọi khai cùng một phía; tiền tố chỉ là head khi không SHA nào khác đã biết trong readback (`biet`) cùng tiền tố."""
    if k != "issue_comments":
        # v1.x #1106 (PR #1116: P2 4435201341 viết trên b2f318e mà commit_id bị GitHub DỜI sang head mới vì push không đổi dòng nó bám) —
        # review comment neo theo `original_commit_id` (commit nơi finding được VIẾT); `commit_id` chỉ là chỗ nó còn áp được.
        c = x["original_commit_id"] if k == "review_comments" and "original_commit_id" in x else x.get("commit_id")
        return "hien" if c == head else "cu" if type(c) is str and SHA_RE.fullmatch(c) else "hong"
    khai = [re.fullmatch(r"(`?)([0-9a-f]{7,40})\1", t.strip()) for t in re.findall(r"Reviewed commit:(?:\*\*)?([^\n]*)", x["body"])]
    if not khai:
        return None
    if not all(khai) or any(head.startswith(t[2]) and any(b != head and b.startswith(t[2]) for b in biet) for t in khai):
        return "hong"
    phia = {head.startswith(t[2]) for t in khai}
    return "hong" if len(phia) > 1 else "hien" if phia == {True} else "cu"


def _doc_connector(duong: str, repo: str, pr: int, head: str, p0p2: list | None = None) -> tuple:
    """I7 — neo MỘT kho + MỘT PR + MỘT head; đủ trang theo tập id của TỪNG endpoint. Dạng: {"repo","pr","head_sha", <endpoint>: trang
    {"total_count","items"}}. Xong = review hoàn tất (không PENDING) trên head, hoặc kết luận `Reviewed commit:` neo head; finding đọc ở
    CẢ BA endpoint, hạng miền đóng (I3); mục của head cũ hợp lệ được bỏ qua, neo thiếu/sai/mơ hồ thì không đạt.
    Trả ((endpoint, id) P3 còn mở, mốc id lớn nhất theo endpoint). #813 `mo-lai` truyền `p0p2` (list): P0–P2 trên head được GOM vào đó thay vì
    từ chối, và connector chưa xong không phải lỗi; `accept` không truyền nên giữ đúng hợp đồng cũ."""
    d, _ = _doc_json(duong, RC_GATE)
    if not isinstance(d, dict) or (d.get("repo"), d.get("pr"), d.get("head_sha")) != (repo, pr, head):
        _die(RC_GATE, f"readback connector không neo đúng ({repo}, PR {pr}, {head})")
    ep = {k: _trang_du(d.get(k), "items", f"connector {k}") for k in EP_CONNECTOR}
    for k, v in ep.items():
        url, dung = ("issue_url", f"{API_GH}{repo}/issues/{pr}") if k == "issue_comments" else ("pull_request_url", f"{API_GH}{repo}/pulls/{pr}")
        if not all(x.get(url) == dung and isinstance(x.get("user"), dict) and type(x.get("body")) is str for x in v):
            _die(RC_GATE, f"connector {k}: phần tử không thuộc {repo} PR {pr} hoặc thiếu user/body")
    biet = {c for v in ep.values() for x in v for c in [x.get("commit_id"), x.get("original_commit_id"), *re.findall(r"\b[0-9a-f]{40}\b", x["body"])] if type(c) is str and SHA_RE.fullmatch(c)}
    cua = {k: [(x, _neo_connector(k, x, head, biet)) for x in v if x["user"].get("login") == BOT_CONNECTOR] for k, v in ep.items()}
    if hong := [(k, x["id"]) for k, v in cua.items() for x, n in v if n == "hong"]:
        _die(RC_GATE, f"connector: mục của {BOT_CONNECTOR} có neo head thiếu/sai/mơ hồ {hong}")
    if not (any(n == "hien" for _, n in cua["issue_comments"])
            or any(n == "hien" and x.get("state") in ("APPROVED", "COMMENTED", "CHANGES_REQUESTED") for x, n in cua["reviews"])) and p0p2 is None:
        _die(RC_GATE, f"connector chưa xong trên {head}: không review hoàn tất/kết luận nào của {BOT_CONNECTOR}")  # I3: bằng chứng dương rỗng
    p3 = []
    for k in EP_CONNECTOR:
        for x, n in cua[k]:
            hang = set(BADGE_RE.findall(x["body"]))
            if n is None and hang:
                _die(RC_GATE, f"connector issue comment {x['id']} có finding mà không neo head")
            if n == "hien" and (hang or k == "review_comments" or x.get("state") == "CHANGES_REQUESTED"):
                if len(hang) != 1 or not hang <= set(HANG_LOP):
                    _die(RC_GATE, f"connector {k} {x['id']}: hạng ngoài miền {HANG_LOP}: {sorted(hang)}")
                if p0p2 is not None and hang != {"P3"}:
                    p0p2.append((k, x["id"]))
                    continue
                if hang != {"P3"}:
                    _die(RC_GATE, f"connector {k} {x['id']} còn {sorted(hang)} trên {head} — DỪNG, hỏi chủ kho")
                p3.append((k, x["id"]))
    return p3, {k: max((x["id"] for x in v), default=None) for k, v in ep.items()}


def _kiem_ci(a, nc: dict, h: str, state_dir: Path, ket=("success",)) -> dict:
    """I7 — CI: check bắt buộc = (app, workflow, job); chỉ attempt MỚI NHẤT của run MỚI NHẤT trên head, đúng kho; job của attempt ấy
    trỏ đúng check-run (cùng kho, app, suite), check-run ấy là bản MỚI NHẤT cùng tên trong suite, và luật `kiem-gate` xanh trên nó.
    #813 `mo-lai ci-do` dùng CHÍNH phép chọn ngữ cảnh này với `ket = CI_DO_THAT` (kết luận đỏ, miền đóng) thay cho xanh."""
    do, nhan = ket != ("success",), "chưa xanh" if ket == ("success",) else "không đỏ thật"
    wr, sha_wr = _doc_json(a.workflow_runs, RC_GATE)
    runs = _trang_du(wr, "workflow_runs", "workflow_runs")
    if not all(type(r.get("path")) is str and type(r.get("head_sha")) is str and isinstance(r.get("repository"), dict)
               and type(r["repository"].get("full_name")) is str for r in runs):  # #813 M5: TRƯỚC lọc — run hỏng không được rơi khỏi bộ lọc
        _die(RC_GATE, "KHÔNG ĐO ĐƯỢC: workflow_runs: mọi run phải có path/head_sha là chuỗi và repository là object có full_name chuỗi")
    moi_tep = [j for f in a.workflow_jobs for j in _trang_du(_doc_json(f, RC_GATE)[0], "jobs", f"workflow_jobs {f}")]  # đủ trang THEO TỪNG tệp
    jobs = _trang_du({"total_count": len({j["id"] for j in moi_tep}), "jobs": moi_tep}, "jobs", "workflow_jobs (gộp các tệp)")
    if not all(type(j.get("run_id")) is int and type(j.get("run_attempt")) is int and j["run_attempt"] > 0
               and all(type(j.get(k)) is str for k in ("name", "head_sha", "status", "check_run_url")) for j in jobs):  # bool/float ≠ int (I3)
        _die(RC_GATE, "KHÔNG ĐO ĐƯỢC: workflow_jobs: run_id/run_attempt phải là int thật (> 0), name/head_sha/status/check_run_url là chuỗi")
    _doc_check_runs(a.check_runs)  # lược đồ + đủ trang của `kiem-gate`; dưới đây thêm: cùng id ⇒ CÙNG nội dung (app, url…)
    cr = {r["id"]: r for r in _trang_du(_doc_json(a.check_runs, RC_GATE)[0], "check_runs", "check_runs")}
    for wf in sorted({w for w, _ in nc["required_checks"]}):
        ung = [r for r in runs if r.get("path") == wf and r.get("head_sha") == h and isinstance(r.get("repository"), dict) and r["repository"].get("full_name") == nc["repo"]]
        run = max(ung, key=lambda r: r["id"]) if ung else {}
        suite, ten_bb = run.get("check_suite_id"), [j for w, j in nc["required_checks"] if w == wf]
        if type(suite) is not int or type(run.get("run_attempt")) is not int or run["run_attempt"] < 1:
            _die(RC_GATE, f"VẮNG: không run {wf} nào trên {h} trong {nc['repo']} (hoặc thiếu check_suite_id/run_attempt)")
        if run.get("status") != "completed" or run.get("conclusion") not in ket or any(j["run_id"] == run["id"] and j["run_attempt"] > run["run_attempt"] for j in jobs):
            _die(RC_GATE, f"{wf}: run {run['id']} attempt {run['run_attempt']} {nhan} hoặc jobs có attempt mới hơn: {run.get('status')}/{run.get('conclusion')}")
        for ten_j in ten_bb:
            jj = [j for j in jobs if (j.get("run_id"), j.get("run_attempt"), j.get("head_sha"), j.get("name")) == (run["id"], run["run_attempt"], h, ten_j)]
            if not jj:
                _die(RC_GATE, f"VẮNG: {wf} / {ten_j!r} không có job trên attempt {run['run_attempt']} của run {run['id']}")
            job = max(jj, key=lambda j: j["id"])
            m = re.fullmatch(rf"{re.escape(API_GH + nc['repo'])}/check-runs/([1-9][0-9]*)", job["check_run_url"])
            r = next((x for i, x in cr.items() if str(i) == m[1]), None) if m else None  # so CHUỖI: không `int()` trên số chữ số tuỳ ý
            if job.get("status") != "completed" or job.get("conclusion") not in ket or r is None or r["name"] != ten_j or r["check_suite"]["id"] != suite:
                _die(RC_GATE, f"{wf} / {ten_j!r}: job attempt mới nhất {nhan} hoặc không trỏ check-run của suite {suite} trong {nc['repo']}")
            if r.get("url") != f"{API_GH}{nc['repo']}/check-runs/{r['id']}":
                _die(RC_GATE, f"{wf} / {ten_j!r}: check-run {r['id']} thuộc kho khác {nc['repo']}")
            if (r.get("app") if isinstance(r.get("app"), dict) else {}).get("slug") != APP_CHECK:
                _die(RC_GATE, f"{wf} / {ten_j!r}: check-run {r['id']} không từ app {APP_CHECK!r}")
            if r["id"] != max(x["id"] for x in cr.values() if x["name"] == ten_j and x["check_suite"]["id"] == suite):
                _die(RC_GATE, f"{wf} / {ten_j!r}: suite {suite} có check-run mới hơn {r['id']} không thuộc job của attempt mới nhất")
            if do and (r["status"] != "completed" or r["conclusion"] not in ket or r["head_sha"] != h):  # nhánh đỏ không qua `kiem-gate` ⇒ tự so head
                _die(RC_GATE, f"{wf} / {ten_j!r}: check-run {r['id']} {nhan}: {r['status']}/{r['conclusion']}")
        if do:
            continue
        cmd_kiem_gate(argparse.Namespace(head=h, check_suite=str(suite), bat_buoc=ten_bb, check_runs=a.check_runs), state_dir)
    return {"workflow_runs_sha256": sha_wr, "check_runs_sha256": _doc_json(a.check_runs, RC_GATE)[1],
            "workflow_jobs_sha256": [_doc_json(f, RC_GATE)[1] for f in a.workflow_jobs]}


def _slug_connector(st: dict, a, h: str, p3: list) -> list:
    """I11: slug của finding connector lấy từ bảng lớp biên nhận H (ứng viên: packet, generation, pending_sha, spec_hash), mỗi lớp P3
    khai `connector_refs` [[endpoint, id], ...] phủ ĐÚNG tập (endpoint, id) P3 — không khoá bằng id số do executor đặt."""
    if not a.bien_nhan_connector:
        _die(RC_BIEN_NHAN, f"connector có P3 {p3} — cần --bien-nhan-connector (bảng lớp do reviewer ký)")
    lop = _du_dieu_kien_approve(st, argparse.Namespace(root=a.root, bien_nhan=a.bien_nhan_connector, verdict="approve", reviewed_sha=h, finding_id=None))["lop"]
    lop = [x for x in lop if "connector_refs" in x]
    refs = [tuple(r) for x in lop for r in (x["connector_refs"] if type(x["connector_refs"]) is list else [None])
            if type(r) is list and len(r) == 2 and r[0] in EP_CONNECTOR and type(r[1]) is int]
    if any(x["hang"] != "P3" or type(x["connector_refs"]) is not list or not x["connector_refs"] for x in lop) \
            or len(refs) != sum(len(x["connector_refs"]) for x in lop) or sorted(refs) != sorted(p3):
        _die(RC_BIEN_NHAN, f"bảng lớp H phải phủ ĐÚNG từng (endpoint, id) P3 của connector {sorted(p3)}, mỗi cặp một lần")
    return sorted({x["slug"] for x in lop})


def cmd_accept(a, state_dir: Path) -> int:
    """M1: (Đ) đầu nhánh lease trên remote = `pending_sha`; CI bắt buộc xanh (I7); connector xong, không P0–P2; mọi P3 còn mở (offline +
    connector, slug từ H) có ĐÚNG một quyết định đủ trường + lý do. Mọi đầu vào xác thực TRƯỚC `_xet_dung` và trước lần ghi duy nhất (I4/I5)."""
    st = _load(state_dir, a.packet)
    if st["state"] != "approved_pending" or not _pending_human_lane(st):
        _die(RC_STATE, f"accept chỉ chạy từ 'approved_pending' của packet áp ADR-0054 (đang {st['state']!r})")
    nc, h, root, p3_off = st["ngu_canh_lease"], st["pending_sha"], Path(a.root), st["bien_nhan_approve"].get("p3")
    if not {tuple(x) for x in CHECK_BAT_BUOC} <= {tuple(x) for x in nc["required_checks"]} or type(p3_off) is not list \
            or not all(type(s) is str and SLUG_RE.fullmatch(s) for s in p3_off):
        _die(RC_STATE, "state hỏng: required_checks thiếu hằng CHECK_BAT_BUOC, hoặc bien_nhan_approve.p3 không phải list slug")
    xa = _git_do(root, "ls-remote", "origin", f"refs/heads/{nc['branch']}")
    if xa[0] or xa[1].split() != [h.encode(), f"refs/heads/{nc['branch']}".encode()]:
        _die(RC_TRACE, f"đầu nhánh {nc['branch']} trên remote ≠ pending_sha {h}")
    sha_ci = _kiem_ci(a, nc, h, state_dir)
    p3_cn, moc = _doc_connector(a.connector, nc["repo"], a.pr, h)
    slug_cn = _slug_connector(st, a, h, p3_cn) if p3_cn else []
    con_mo = {("offline", s) for s in p3_off} | {("connector", s) for s in slug_cn}
    qd, truong = (_doc_json(a.quyet_dinh_p3, RC_ARG)[0] if a.quyet_dinh_p3 else []), {"nguon", "khoa", "ten_no", "owner", "huong", "ly_do"}
    if (type(qd) is not list or not all(type(q) is dict and set(q) == truong and all(type(v) is str and v.strip() for v in q.values()) for q in qd)
            or sorted((q["nguon"], q["khoa"]) for q in qd) != sorted(con_mo)):
        _die(RC_ARG, f"P3 còn mở {sorted(con_mo)} phải có ĐÚNG một quyết định {sorted(truong)} mỗi mục")
    moi = {**st, "state": "accepted", "accepted_sha": h, "moc_connector": moc, "quyet_dinh_p3": qd, "history": [*st["history"], {
        "event": "accept", "accepted_sha": h, "pr": a.pr, "moc_connector": moc, "connector_sha256": _doc_json(a.connector, RC_GATE)[1], **sha_ci}]}
    try:  # state dự kiến phải mã hoá được TRƯỚC `_xet_dung` (I5: mọi đầu vào xác thực xong) — vd surrogate đơn trong quyết định P3
        json.dumps(moi, ensure_ascii=False).encode("utf-8")
    except (ValueError, TypeError, UnicodeError) as ex:
        _die(RC_ARG, f"quyết định P3 / state dự kiến không mã hoá được UTF-8: {type(ex).__name__}")
    _xet_dung(state_dir, st, "accept")
    _save(state_dir, moi)
    print(f"accepted {h} — {len(qd)} quyết định P3, mốc connector {moc}")
    return RC_OK


# --- #813 MAY-ADR-0054-b (`ops/specs/wp813-r2.md` + phần chung): `mo-lai` (approved_pending → running | cho_chu_kho) · `chu-kho-duyet`.
NGUYEN_NHAN_MO_LAI, CI_DO_THAT, PHAM_VI_CHECKPOINT = ("ci-do", "connector"), ("failure", "timed_out", "startup_failure"), ("cho_phep_va", "cho_phep_day")
CUA_DI_TIEP = ("begin-attempt", "mo-lai", "chu-kho-duyet")  # I5: cửa đưa packet đi tiếp mà bộ đếm same-failure đã chạm phải chặn
KHOA_CHECKPOINT = {"packet_issue": int, "generation": int, "spec_hash": str, "head_sha": str, "pham_vi": list, "nguoi_quyet": str, "neo": str}


def _quyen_hop_le(q, khoa: str, mien) -> bool:
    """I6: quyền phái sinh (`mo_lai_tu`, `checkpoint_day`) neo (nguyên nhân | sha256 hiện vật, generation, sha) — hoặc vắng."""
    return q is None or (type(q) is dict and set(q) == {khoa, "generation", "sha"} and type(q[khoa]) is str and (mien is None or q[khoa] in mien)
                         and type(q["generation"]) is int and type(q["sha"]) is str and bool(SHA_RE.match(q["sha"])))


def cmd_mo_lai(a, state_dir: Path) -> int:
    """M2 — `ci-do`: từ approved_pending (head = pending_sha), mọi check khai trong biên nhận là check ĐỎ THẬT trên head và connector không
    còn P0–P2 ⇒ running. `connector`: (endpoint, id) của biên nhận phủ BẰNG ĐÚNG P0–P2 connector trên head ⇒ cho_chu_kho, từ approved_pending
    hoặc từ running khi quyền mở lại hiện hành là `ci-do` cùng generation, cùng head. Slug từ bảng lớp biên nhận H (I11), cộng bộ đếm
    same-failure; quyền `mo_lai_tu` bị THAY (I6). Mọi đầu vào xác thực TRƯỚC `_xet_dung` và lần ghi duy nhất (I4/I5)."""
    st = _load(state_dir, a.packet)
    nc, ml, connector = st.get("ngu_canh_lease"), st.get("mo_lai_tu"), a.nguyen_nhan == "connector"
    sau_ml = next((st["history"][i:] for i in range(len(st["history"]) - 1, -1, -1) if st["history"][i].get("event") == "mo_lai"), [])
    tu_ci = connector and st["state"] == "running" and ml is not None and ml["nguyen_nhan"] == "ci-do" and ml["generation"] == (nc or {}).get("generation") \
        and not any(x.get("event") == "begin_attempt" for x in sau_ml)  # connector PR #969: quyền ci-do hết dùng được khi đã mở lượt mới
    if not _pending_human_lane(st) or not (st["state"] == "approved_pending" or tu_ci):
        _die(RC_STATE, f"mo-lai {a.nguyen_nhan} không chạy từ {st['state']!r} (đòi approved_pending của packet áp ADR-0054"
                       + (", hoặc running mở lại bằng ci-do cùng generation, chưa mở lượt mới)" if connector else ")"))
    h = ml["sha"] if tu_ci else st["pending_sha"]
    if not a.finding_id:
        _die(RC_ARG, "mo-lai phải có ít nhất một --finding-id (I3: tập bằng chứng dương rỗng ⇒ không đạt)")
    bn = _du_dieu_kien_approve(st, argparse.Namespace(root=a.root, bien_nhan=a.bien_nhan, verdict="changes_requested", reviewed_sha=h, finding_id=a.finding_id))
    khoa = "connector_refs" if connector else "check_refs"
    dung = (lambda r: type(r) is list and len(r) == 2 and r[0] in EP_CONNECTOR and type(r[1]) is int) if connector else (
        lambda r: type(r) is list and len(r) == 2 and all(type(y) is str and y.strip() for y in r))  # ci-do: [workflow, job] — định danh I7
    refs = [tuple(r) for x in bn["lop"] for r in (x.get(khoa) if type(x.get(khoa)) is list else [None]) if dung(r)]
    if any(type(x.get(khoa)) is not list or not x[khoa] or connector and x["hang"] not in HANG_LOP[:3] for x in bn["lop"]) \
            or len(refs) != sum(len(x[khoa]) for x in bn["lop"]) or len(set(refs)) != len(refs):
        _die(RC_BIEN_NHAN, f"bảng lớp H: mỗi lớp phải có `{khoa}` khác rỗng, đúng dạng, không lặp" + (" và hạng P0–P2" if connector else ""))
    p02 = []
    _doc_connector(a.connector, nc["repo"], a.pr, h, p02)
    if connector and sorted(refs) != sorted(p02):
        _die(RC_BIEN_NHAN, f"connector: `connector_refs` phải phủ BẰNG ĐÚNG P0–P2 trên {h}: {sorted(p02)}")
    if not connector and p02:
        _die(RC_GATE, f"ci-do: connector còn P0–P2 {sorted(p02)} trên {h} — dùng --nguyen-nhan connector")
    sha_ci = {}
    if not connector:
        if not (a.workflow_runs and a.workflow_jobs and a.check_runs):
            _die(RC_ARG, "mo-lai ci-do phải có --workflow-runs, --workflow-jobs, --check-runs (readback như `accept`, trên head)")
        sha_ci = _kiem_ci(a, {**nc, "required_checks": [list(r) for r in refs]}, h, state_dir, CI_DO_THAT)  # I7: run/attempt/job/check-run mới nhất
    slugs = sorted({x["slug"] for x in bn["lop"]})
    moi = {**st, "state": "cho_chu_kho" if connector else "running", "attempt_open": False, "reviewing_head_sha": None,
           "mo_lai_tu": {"nguyen_nhan": a.nguyen_nhan, "generation": nc["generation"], "sha": h},
           "finding_counts": {**st["finding_counts"], **{s: st["finding_counts"].get(s, 0) + 1 for s in slugs}},
           "history": [*st["history"], {"event": "mo_lai", "nguyen_nhan": a.nguyen_nhan, "sha": h, "generation": nc["generation"], "finding_ids": slugs,
                                        "refs": [list(r) for r in refs], "bien_nhan_sha256": bn["sha256"],
                                        "connector_sha256": _doc_json(a.connector, RC_GATE)[1], **sha_ci}]}
    _xet_dung(state_dir, moi, "mo-lai")  # bộ đếm vừa ghi chạm trần ⇒ ghi sổ đủ rồi blocked (I4)
    _save(state_dir, moi)
    print(f"mo-lai {a.nguyen_nhan} trên {h} — finding {slugs}, state {moi['state']}")
    return RC_OK


def cmd_chu_kho_duyet(a, state_dir: Path) -> int:
    """M3 (Đ): hiện vật checkpoint đọc từ `origin/master` SAU khi máy tự fetch và khớp `ls-remote` — chỉ thứ chủ kho đã merge. `cho_phep_va`:
    rời cho_chu_kho về running, head = sha đã mở lại (tiêu thụ `mo_lai_tu`). `cho_phep_day`: ở approved_pending, head = pending_sha ⇒ ghi
    quyền riêng `checkpoint_day` cho #816, không đổi state. Mỗi (hiện vật, phạm vi) dùng MỘT lần (I6)."""
    import yaml
    st, root = _load(state_dir, a.packet), Path(a.root)
    pv = {"cho_chu_kho": "cho_phep_va", "approved_pending": "cho_phep_day"}.get(st["state"])
    if not _pending_human_lane(st) or pv is None:
        _die(RC_STATE, f"chu-kho-duyet chỉ chạy ở cho_chu_kho / approved_pending của packet áp ADR-0054 (đang {st['state']!r})")
    p = PurePosixPath(a.checkpoint_path)
    if p.parts[:2] != ("ops", "checkpoints") or len(p.parts) < 3 or ".." in p.parts or p.suffix != ".yaml":
        _die(RC_ARG, f"--checkpoint-path phải là ops/checkpoints/<tên>.yaml: {a.checkpoint_path!r}")
    m = "refs/remotes/origin/master"
    if _git_do(root, "fetch", "-q", "origin", f"+refs/heads/master:{m}")[0]:
        _die(RC_GUARD, "KHÔNG ĐO ĐƯỢC: `git fetch origin master` không chạy được")
    xa, gan = _git_do(root, "ls-remote", "origin", "refs/heads/master"), _git_do(root, "rev-parse", "-q", "--verify", f"{m}^{{commit}}")
    if xa[0] or gan[0] or xa[1].split() != [gan[1].strip(), b"refs/heads/master"]:
        _die(RC_GUARD, "origin/master cục bộ lệch ls-remote — không đọc checkpoint từ ref chưa đo")
    rc, raw = _git_do(root, "show", f"{gan[1].decode().strip()}:{a.checkpoint_path}")
    try:
        d = yaml.safe_load(raw) if rc == 0 else None
    except (RecursionError, yaml.YAMLError):  # thứ tự khác `_record_lease_ref` để mốc đột biến #812 khớp đúng một chỗ
        d = None
    if rc or type(d) is not dict or set(d) != set(KHOA_CHECKPOINT) or any(type(d[k]) is not t for k, t in KHOA_CHECKPOINT.items()) \
            or not d["pham_vi"] or not all(type(x) is str and x in PHAM_VI_CHECKPOINT for x in d["pham_vi"]):  # I3: miền đóng TỪNG phần tử
        _die(RC_GUARD, f"checkpoint {a.checkpoint_path} không có trên origin/master hoặc sai lược đồ {sorted(KHOA_CHECKPOINT)}")
    ml, sha = st.get("mo_lai_tu"), hashlib.sha256(raw).hexdigest()
    h = ml["sha"] if pv == "cho_phep_va" else st["pending_sha"]
    loi = [ten for ten, dung in (
        ("packet", d["packet_issue"] == st["packet"]), ("generation", d["generation"] == st["ngu_canh_lease"]["generation"]),
        ("spec_hash", d["spec_hash"] == st["ngu_canh_lease"]["spec_hash"]),  # I10: đủ (packet, generation, sha, spec_hash)
        ("head_sha", d["head_sha"] == h), ("nguoi_quyet", d["nguoi_quyet"] in NGUOI_CO_THAM_QUYEN),
        ("neo", bool(REPO_RE.fullmatch(d["neo"]))), ("pham_vi", pv in d["pham_vi"]),
        ("da_dung", not any(x.get("event") == "chu_kho_duyet" and (x.get("sha256"), x.get("pham_vi")) == (sha, pv) for x in st["history"]))) if not dung]
    if loi:
        _die(RC_GUARD, f"checkpoint {a.checkpoint_path} không mở được {pv} trên {h}: {loi}")
    su_kien = {"event": "chu_kho_duyet", "pham_vi": pv, "sha256": sha, "head_sha": h, "checkpoint_path": a.checkpoint_path}
    moi = {**st, "history": [*st["history"], su_kien], **({"state": "running", "mo_lai_tu": None} if pv == "cho_phep_va" else
                                                           {"checkpoint_day": {"sha256": sha, "generation": d["generation"], "sha": h}})}
    _xet_dung(state_dir, moi, "chu-kho-duyet")
    _save(state_dir, moi)
    print(f"chu-kho-duyet {pv} trên {h} — state {moi['state']}")
    return RC_OK


def _xet_dung(state_dir: Path, st: dict, cua: str, a=None, cham_tran=()) -> None:
    """I5 (M4): hàm DUY NHẤT xét MỌI điều kiện dừng (trần lượt, trần vòng, same-failure, rescue sau review), gọi SAU khi đầu vào của cửa
    đã được xác thực (I4). `a`/`cham_tran` = đối số review + finding chạm trần, khi kết quả lượt đã ghi sổ. Packet áp ADR-0054 không bị trần vòng chặn
    TRƯỚC khi cửa khép ghi kết quả (I5); packet cũ giữ đúng hành vi cũ (I9)."""
    if cua == "begin-attempt" and st["attempts_used"] >= st["attempts_limit"]:
        st.update(state="blocked", history=[*st["history"], {"event": "blocked_attempts_exhausted", "at_attempt": st["attempts_used"]}])
        _save(state_dir, st)
        _die(RC_TRAN, f"đã dùng hết {st['attempts_used']}/{st['attempts_limit']} lượt — packet về blocked. Ghi failure evidence + handoff rồi dừng; reroute là việc của bên điều phối.")
    if cua == "record-review" and a is None and not _pending_human_lane(st):
        if st["review_rounds_used"] >= st["review_rounds_limit"]:  # review MỚI khi trần vòng đã chạm (state v1 cũ / sửa tay) ⇒ rescue, kể cả approve
            _vao_rescue(state_dir, st, "vong_review", "review vượt trần vòng")
    if cua in CUA_DI_TIEP and not cham_tran:  # #813 M1: bộ đếm đã chạm (kể cả vừa cộng ở `mo-lai`) chặn cửa đi tiếp; cửa khép không ở đây
        cham_tran = sorted(f for f, n in st["finding_counts"].items() if n >= st["same_failure_limit"])
    if cham_tran:
        st.update(state="blocked", history=[*st["history"], {"event": "blocked_same_failure", "finding_ids": cham_tran}])
        _save(state_dir, st)
        chi_tiet = ", ".join(f"{f}×{st['finding_counts'][f]}" for f in cham_tran)
        _die(RC_TRAN, f"cùng finding-id lặp tới trần ({chi_tiet}; trần {st['same_failure_limit']}) "
                      f"— packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.")
    if a is not None:
        if a.verdict != "approve":  # approve KHÔNG BAO GIỜ kích rescue
            for truc, (u, t) in reversed(TRUC_TRAN.items()):  # codex chạm trần TRƯỚC (lúc record-codex-call) ⇒ xét trước (ADR-0048)
                if st[u] >= st[t]:
                    _vao_rescue(state_dir, st, truc, f"review {a.verdict} chưa approve")


def cmd_status(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    print(json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True))
    if st.get("dem_tu_suy"):
        print(CANH_BAO_V1, file=sys.stderr)
    return RC_OK


def cmd_where(a, state_dir: Path) -> int:
    print(f"thư mục state đang dùng: {state_dir}")
    return RC_OK


# --- #1106 ADR-0060 packet C (`ops/specs/DIEU-KIEN-MERGE-CONG-r1.md`): `kiem-merge`, `kiem-dong-wp` — KHÔNG đọc/ghi state, độc lập ADR-0054.
# Mỗi điều kiện đo riêng; mọi điều kiện thiếu được liệt kê (M6), không dừng ở cái đầu tiên.
ADR0060_TEP = "docs/adr/0060-dieu-kien-merge-va-moc-ready.md"
LUAT_0060_RE = re.compile(rb"^dieu_kien_merge: ADR-0060@([0-9a-f]{40})$", re.M)
CHU_KHO, MOC_10_2_2, DAT_MOC = "ducthangho", ("run", "checkout", "workflow_definition", "gate_output"), ("passed", "owner_waived")
WIN_TU_KHOA = ("os.name", "sys.platform", "platform.system", "subprocess", "encoding=", "os.sep", "pathlib")
DUOI_MA, DUOI_THU_DONG = (".py", ".ps1", ".sh", ".cmd", ".bat"), (".md", ".yaml", ".yml", ".json", ".txt", ".log")
DOT_BIEN_DU_TEP = ".github/workflows/ci-dot-bien-du.yml"  # #1120 K7: nguồn `full_mutant_audit` của ADR-0060 M9


def _yaml_cay(b: bytes):
    """Kiểm trên CÂY NODE trước khi dựng dict: khoá phải là scalar chuỗi, không trùng trong một mapping, không alias."""
    import yaml
    class Nap(yaml.SafeLoader):  # timestamp giữ nguyên CHUỖI: so `lease_until` theo đúng chữ, không theo datetime đã chuẩn hoá
        yaml_implicit_resolvers = {k: [r for r in v if r[0] != "tag:yaml.org,2002:timestamp"] for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}
    s = b.decode("utf-8")
    try:
        if any(isinstance(e, yaml.AliasEvent) or getattr(e, "anchor", None) for e in yaml.parse(s)):
            raise ValueError("YAML có anchor/alias")
        cho = [yaml.compose(s)]
    except yaml.YAMLError as ex:
        raise ValueError(f"YAML hỏng: {type(ex).__name__}") from None
    while cho:
        n = cho.pop()
        if isinstance(n, yaml.MappingNode):
            khoa = [k.value if isinstance(k, yaml.ScalarNode) and k.tag == "tag:yaml.org,2002:str" else None for k, _ in n.value]
            if None in khoa or len(set(khoa)) != len(khoa):
                raise ValueError(f"khoá YAML trùng hoặc không phải chuỗi: {khoa}")
            cho += [v for _, v in n.value]
        elif isinstance(n, yaml.SequenceNode):
            cho += n.value
    try:  # chỉ dựng giá trị SAU khi cây sạch; tag hỏng (`!!bool nope`) ném lỗi constructor ⇒ lỗi đầu vào, không traceback
        return yaml.load(s, Loader=Nap)
    except (yaml.YAMLError, KeyError, AttributeError, TypeError, ValueError) as ex:
        raise ValueError(f"YAML hỏng: {type(ex).__name__}") from None


def _dk(ten: str, fn, thieu: list):
    """Chạy một điều kiện; `_die` bên trong (vd `_kiem_ci`) bị bắt thành một dòng thiếu thay vì kết thúc lệnh."""
    loi = io.StringIO()
    try:
        with contextlib.redirect_stderr(loi), contextlib.redirect_stdout(io.StringIO()):
            return fn()
    except SystemExit:
        thieu.append(f"{ten}: {' '.join(loi.getvalue().split())[:400] or 'đỏ'}")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as ex:
        thieu.append(f"{ten}: KHÔNG ĐO ĐƯỢC ({type(ex).__name__}: {ex})"[:400])


def _diff_raw(root: Path, b: str, h: str) -> list:
    """`git diff --raw --no-renames -z B..H` ⇒ [(mode, đường dẫn)]; git lỗi ⇒ ValueError (KHÔNG ĐO ĐƯỢC, không phải "không chạm")."""
    rc, raw = _git_do(root, "diff", "--raw", "--no-renames", "-z", b, h)
    if rc:
        raise ValueError("không đo được diff base..head")
    t = raw.decode("utf-8", "surrogateescape").split("\0")
    return [(t[i].split()[1] if t[i].split()[1] != "000000" else t[i].split()[0][1:], t[i + 1]) for i in range(0, len(t) - 1, 2) if t[i].startswith(":")]


def _cham_m9(root: Path, b: str, h: str) -> bool:
    """#1120 ADR-0060 M9: diff chạm `.claude/dev/**`, `ops/**/*.py` hoặc `.github/workflows/**`."""
    return any(p.startswith((".claude/dev/", ".github/workflows/")) or (p.startswith("ops/") and p.endswith(".py")) for _, p in _diff_raw(root, b, h))


def _phan_loai_windows(root: Path, b: str, h: str, spec: bytes) -> str:
    """ADR-0060 M3, đúng thứ tự, dừng ở bước đầu khớp."""
    tep = _diff_raw(root, b, h)
    if not tep:
        raise ValueError("không đo được diff base..head")
    duoi = lambda p: PurePosixPath(p).suffix.lower()  # noqa: E731
    if all(p.startswith(("ops/reviews/", "ops/land/")) and m == "100644" and (duoi(p) in DUOI_THU_DONG or PurePosixPath(p).name == "SHA256SUMS") for m, p in tep):
        return "not_required"
    ma = [p for _, p in tep if duoi(p) in (".py", ".ps1", ".sh", ".yml")]
    rc, d = _git_do(root, "diff", "-U0", b, h, "--", *ma) if ma else (0, b"")
    if rc:
        raise ValueError("không đo được dòng thêm (git diff -U0)")
    them = [x for x in d.decode("utf-8", "replace").splitlines() if x.startswith("+") and not x.startswith("+++")]
    if (any(duoi(p) in (".ps1", ".cmd", ".bat", ".sh") or p.startswith(("scripts/deploy-", ".claude/dev/", ".github/workflows/")) for _, p in tep)
            or any(k in x for x in them for k in WIN_TU_KHOA) or re.search(rb"^windows: required$", spec, re.M)):
        return "required"
    if all(duoi(p) == ".md" or (p.startswith(("docs/", "ops/land/", "ops/reviews/", "ops/specs/")) and duoi(p) not in DUOI_MA) for _, p in tep):
        return "not_required"
    return "unknown"


def _dong_chu_kho(duong, tho=False) -> list[str]:
    """Các dòng của MỘT comment readback chỉ khi tác giả là `CHU_KHO` (hằng trong mã, không có cờ đổi). `tho`: giữ nguyên dòng (#1120 K7
    khớp `^full_mutant_audit: H mien$` đúng chữ, chỉ tách ở LF/CRLF — review offline lượt 1+3 F03: `strip()`/`splitlines()` sửa dòng)."""
    if not duong:
        return []
    d = _doc_json(duong, RC_GATE)[0]
    if not isinstance(d, dict) or not isinstance(d.get("user"), dict) or d["user"].get("login") != CHU_KHO or type(d.get("body")) is not str:
        raise ValueError(f"comment không phải của chủ kho {CHU_KHO}")
    return [x if tho else x.strip() for x in (re.split(r"\r?\n", d["body"]) if tho else d["body"].splitlines())]  # lượt 3 F03: splitlines tách cả \v \f \x85 \u2028…


# ADR-0063: authoritative spec and human evidence remain separate from model artifacts.
ADR0062_OID = "1f0941e9bba1d1d517eda4174167b81963c06bd5"
ADR0062_TIME = "2026-11-04T08:36:24Z"
ADR0063_TEP = "docs/adr/0063-merge-spec-ref-va-human-audit.md"
ADR0063_ANCHORS = ("spec_ref", "spec_sha256_required", "human_exact_head_audit.v1", "human_audit_transition.v1", "M5/M12", "first-parent", "2026-11-04T08:36:24Z", "K0/K2/K3/K5/K6/K7", "thời hạn review")


def _adr0063_landed(root):
    """Use committed first-parent introduction, with readable complete history."""
    master = "refs/remotes/origin/master"
    rc, fp = _git_do(root, "rev-list", "--first-parent", master)
    born_rc, born = _git_do(root, "log", "--first-parent", "--diff-merges=first-parent", "--no-patch", "--no-renames", "--diff-filter=A", "--format=%H", master, "--", ADR0063_TEP)
    if rc or born_rc or _git_do(root, "rev-parse", "--is-shallow-repository") != (0, b"false\n"):
        raise ValueError("ADR0063 first-parent history không đo được")
    for oid in born.decode().split():
        parent_rc, parent_file = _git_do(root, "ls-tree", "-r", f"{oid}^1", "--", ADR0063_TEP)
        intro_rc, intro = _git_do(root, "show", f"{oid}:{ADR0063_TEP}")
        current_rc, current = _git_do(root, "show", f"{master}:{ADR0063_TEP}")
        if (oid.encode() in fp.split() and not parent_rc and not parent_file and not intro_rc and not current_rc
                and all(anchor.encode() in intro and anchor.encode() in current for anchor in ADR0063_ANCHORS)):
            return
    raise ValueError("ADR0063 chưa land với contract đầy đủ trên first-parent master")


def _spec_merge(root, h, path, lease):
    def blob(oid):
        rc, spec = _git_do(root, "show", f"{oid}:{path}")
        if rc or hashlib.sha256(spec).hexdigest() != lease.get("spec_hash"):
            raise ValueError("spec blob/hash không khớp lease")
        return spec
    if "spec_ref" not in lease:
        return blob(h)
    _adr0063_landed(root)
    if type(lease.get("packet_id")) is not str or not lease["packet_id"] or type(lease.get("revision")) is not int or lease["revision"] < 1:
        raise ValueError("spec lease packet_id/revision sai kiểu")
    if "spec_sha256_required" in lease and lease["spec_sha256_required"] != lease["spec_hash"]:
        raise ValueError("spec_sha256_required khác spec_hash")
    ref = lease["spec_ref"]
    m = re.fullmatch(r"refs/heads/[^\s@:\\]+@([0-9a-f]{40})", ref) if isinstance(ref, str) else None
    if not m or _git_do(root, "check-ref-format", ref.split("@")[0])[0] or lease.get("spec_path") != path or not path or PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts:
        raise ValueError("spec_ref phải ghim OID40 và spec_path đúng nguồn")
    spec = blob(m[1])
    visible, errors = _che_khong_render(spec.decode("utf-8"))
    if errors: raise ValueError("spec Markdown không đóng rào/comment")
    declaration = r'''(?:- )?(?:packet_id: [^\s;'"](?:[^;\r\n]*[^\s;'"])?|revision: [1-9][0-9]*)'''
    inline = r'''- packet_id: [^\s;'"](?:[^;\r\n]*[^\s;'"])?; revision: [1-9][0-9]*;(?: [^\r\n]*\S)?'''
    heading = r"# [A-Za-z0-9_-]+ r[1-9][0-9]* (?:—|–|-) \S(?:.*\S)?"
    if b"\r" in spec:
        raise ValueError("spec identity cần LF")
    for line in visible.split("\n"):
        if re.match(r"(?i)\s*(?:-\s*)?(?:packet_id|revision)\s*:", line) and not (re.fullmatch(declaration, line) or re.fullmatch(inline, line)):
            raise ValueError("spec identity declaration sai grammar")
        if len(re.findall(r"(?i)\b(?:packet_id|revision)\s*:", line)) > 2 and re.fullmatch(inline, line):
            raise ValueError("spec identity declaration lặp trong inline")
        if re.match(r"(?i)\s*# .* r[0-9]\S*", line) and not re.fullmatch(heading, line):
            raise ValueError("spec identity H1 sai grammar")
    for key in ("packet_id", "revision"):
        values = re.findall(rf"(?m)^(?:- )?{key}: ([^;\n]+)", visible)
        if key == "revision":
            values += re.findall(r"(?m)^- packet_id: [^;\n]+; revision: ([0-9]+);", visible)
        headings = re.findall(r"(?m)^# ([A-Za-z0-9_-]+) r([1-9][0-9]*) (?:—|–|-) .+$", visible)
        values = list(dict.fromkeys(values + [t[0 if key == "packet_id" else 1] for t in headings]))
        if values != [str(lease.get(key))]:
            raise ValueError(f"spec {key} không khớp lease")
    present_rc, present = _git_do(root, "ls-tree", "-r", h, "--", path)
    if present_rc:
        raise ValueError("spec H presence không đo được")
    if present and blob(h) != spec:
        raise ValueError("hai nguồn spec khác bytes")
    return spec


def _owner_record(path, repo, pr, schema):
    if not path:
        raise ValueError("thiếu owner comment")
    d = _doc_json(path, RC_GATE)[0]
    if not isinstance(d, dict):
        raise ValueError("owner comment phải là object")
    url = f"https://github.com/{repo}/pull/{pr}#issuecomment-{d.get('id')}"
    issue_comment_url = f"https://github.com/{repo}/issues/{pr}#issuecomment-{d.get('id')}"
    # Packet #1254: GitHub rewrites only the display URL when an issue becomes a PR.
    allowed_urls = (url, issue_comment_url) if schema == "human_exact_head_audit.v1" else (url,)
    if not (repo == "ducthangho/tra-luat" and type(d.get("id")) is int and d["id"] > 0
            and isinstance(d.get("user"), dict) and d["user"].get("login") == CHU_KHO and d["user"].get("type") == "User"
            and d.get("author_association") == "OWNER" and d.get("issue_url") == f"https://api.github.com/repos/{repo}/issues/{pr}"
            and d.get("html_url") in allowed_urls):
        raise ValueError("owner comment origin/identity không hợp lệ")
    for key in ("created_at", "updated_at"):
        if not isinstance(d.get(key), str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", d[key]):
            raise ValueError("comment timestamp sai")
        datetime.strptime(d[key], "%Y-%m-%dT%H:%M:%SZ")
    if not isinstance(d.get("body"), str):
        raise ValueError("owner body phải là string")
    record = _yaml_cay(d["body"].encode("utf-8"))
    if not isinstance(record, dict) or record.get("schema") != schema:
        raise ValueError("owner record schema không hợp lệ")
    if schema == "human_exact_head_audit.v1" and record.get("audit_source") == issue_comment_url:
        # Normalize a parsed copy only; raw body, identity and timestamps stay untouched.
        record = dict(record, audit_source=url)
    return record, d, url


def _human_merge(a, root, lease, spec, p3):
    _adr0063_landed(root)
    if spec is None or type(lease.get("packet_id")) is not str or not lease["packet_id"]:
        raise ValueError("human audit thiếu spec/packet identity")
    r, comment, url = _owner_record(a.human_audit_comment, a.repo, a.pr, "human_exact_head_audit.v1")
    rc, tree = _git_do(root, "rev-parse", f"{a.head}^{{tree}}")
    bound = dict(packet=lease.get("packet_id"), revision=lease.get("revision"), generation=lease.get("generation"), pr=a.pr,
                 reviewed_sha=a.head, reviewed_tree=tree.decode().strip(), spec_sha256=hashlib.sha256(spec).hexdigest())
    expected = dict(schema="human_exact_head_audit.v1", **bound, verdict="approve", assurance="human_audited",
                    review_axes=["spec", "standards_security"], open_findings=r.get("open_findings"), audit_source=url)
    if rc or set(r) != set(expected) or any(type(r[k]) is not type(v) or r[k] != v for k, v in expected.items()) or not all(bound.values()) or any(type(bound[k]) is not int or bound[k] < 1 for k in ("revision", "generation", "pr")):
        raise ValueError("human audit exact bindings/verdict không khớp")
    findings = r["open_findings"]
    if not isinstance(findings, list):
        raise ValueError("open_findings phải là list")
    for f in findings:
        if not isinstance(f, dict) or set(f) != {"slug", "severity"} or not isinstance(f.get("slug"), str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", f["slug"]) or f.get("severity") not in ("P0", "P1", "P2", "P3"):
            raise ValueError("finding schema sai")
        if f["severity"] != "P3":
            raise ValueError("human audit còn P0–P2")
        p3.append(("human", f["slug"]))
    if not a.human_remote_run:
        raise ValueError("thiếu human remote run")
    run = _doc_json(a.human_remote_run, RC_GATE)[0]
    if not isinstance(run, dict):
        raise ValueError("human remote run phải là object")
    run_url = f"https://github.com/{a.repo}/actions/runs/{run.get('id')}"
    if not (type(run.get("id")) is int and run["id"] > 0 and run.get("repository", {}).get("full_name") == a.repo
            and run.get("head_sha") == a.head and run.get("html_url") == run_url and type(run.get("event")) is str and bool(run["event"])):
        raise ValueError("human remote run repo/head/origin sai")
    runs = _trang_du(_doc_json(a.workflow_runs, RC_GATE)[0], "workflow_runs", "human workflow_runs")
    if any(not isinstance(r.get("repository"), dict) or type(r["repository"].get("full_name")) is not str or not r["repository"]["full_name"]
           for r in runs if r.get("head_sha") == a.head):
        raise ValueError("human same-head K2 run thiếu repository identity")
    same_head = [r for r in runs if r.get("head_sha") == a.head and r.get("repository", {}).get("full_name") == a.repo]
    if not same_head:
        raise ValueError("human run không có trong tập K2 đầy đủ")
    times = []
    for candidate in same_head:
        if (candidate["id"] < 1 or candidate.get("html_url") != f"https://github.com/{a.repo}/actions/runs/{candidate['id']}"
                or type(candidate.get("event")) is not str or not candidate["event"]):
            raise ValueError("human K2 run origin sai")
        times.append(_doc_han_utc(candidate["created_at"]))
    remote_time = _doc_han_utc(run["created_at"])
    if remote_time != min(times) or not any(all(candidate.get(k) == run.get(k) for k in ("id", "head_sha", "repository", "html_url", "event", "created_at")) for candidate in same_head):
        raise ValueError("human remote run phải là run sớm nhất trong tập K2 đầy đủ")
    if remote_time >= _doc_han_utc(ADR0062_TIME):
        if _doc_han_utc(comment["updated_at"]) >= remote_time:
            if _1174_SCOPED.get():
                raise _1174Error("candidate mới cần human review trước push M5/M12", "FAIL")
            raise ValueError("candidate mới cần human review trước push M5/M12")
        return
    tr, _, tr_url = _owner_record(a.human_transition_comment, a.repo, a.pr, "human_audit_transition.v1")
    expected_tr = dict(schema="human_audit_transition.v1", **bound, adr0062_oid=ADR0062_OID, remote_run=run_url,
                       disposition="accept_post_push_audit", reason=tr.get("reason"), transition_source=tr_url)
    fp_rc, fp = _git_do(root, "rev-list", "--first-parent", "refs/remotes/origin/master")
    parent_rc, parent_file = _git_do(root, "ls-tree", "-r", f"{ADR0062_OID}^1", "--", "docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md")
    if (set(tr) != set(expected_tr) or any(type(tr[k]) is not type(v) or tr[k] != v for k, v in expected_tr.items())
            or not isinstance(tr["reason"], str) or not tr["reason"].strip() or fp_rc or ADR0062_OID.encode() not in fp.split()
            or _git_do(root, "cat-file", "-e", f"{ADR0062_OID}:docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md")[0]
            or parent_rc or parent_file
):
        raise ValueError("transition owner/bindings/mốc first-parent/ADR0063 chưa land")


def cmd_kiem_merge(a, state_dir: Path) -> int:
    if not (all(SHA_RE.fullmatch(x) for x in (a.head, a.base)) and re.fullmatch(r"[^/\s]+/[^/\s]+", a.repo)):
        _die(RC_ARG, "--head/--base phải là SHA 40 hex, --repo dạng chủ/kho")
    root, h, thieu, p3 = Path(a.root), a.head, [], []
    try:  # đầu vào YAML hỏng là lỗi ĐỐI SỐ, không phải một điều kiện đỏ
        lease = _yaml_cay(Path(a.lease).read_bytes())
    except (OSError, ValueError, UnicodeDecodeError) as ex:
        _die(RC_ARG, f"không đọc được --lease: {ex}")
    if not isinstance(lease, dict):
        _die(RC_ARG, "--lease phải là mapping")

    def k0():
        if a.base == h or _git_do(root, "merge-base", "--is-ancestor", a.base, h)[0] or _git_do(root, "merge-base", "--is-ancestor", a.base, "refs/remotes/origin/master")[0]:
            _die(RC_GATE, "base không phải tổ tiên của head và của origin/master, hoặc base = head")
        x = _git_do(root, "ls-remote", "origin", f"refs/pull/{a.pr}/head")
        if x[0] or x[1].split()[:1] != [h.encode()]:
            _die(RC_GATE, f"PR head hiện hành ≠ {h}")

    def k1():
        spec = _spec_merge(root, h, a.spec, lease)
        khai = re.findall(rb"^dieu_kien_merge:[^\n]*$", spec, re.M)
        if not khai:
            return spec
        oid_khop = LUAT_0060_RE.fullmatch(khai[0]) if len(khai) == 1 else None
        oid = oid_khop.group(1).decode() if oid_khop else None
        if not (oid and _git_do(root, *("rev-parse", "--is-shallow-repository")) == (0, b"false\n")
                and _git_do(root, "cat-file", "-e", f"{oid}:{ADR0060_TEP}")[0] == 0 and _git_do(root, "cat-file", "-e", f"{oid}^1:{ADR0060_TEP}")[0] != 0
                and (fp := _git_do(root, "rev-list", "--first-parent", "refs/remotes/origin/master"))[0] == 0 and oid.encode() in fp[1].split()):
            _die(RC_GATE, f"K1: {len(khai)} dòng khai dieu_kien_merge; cần 0 hoặc đúng 1 dòng hợp lệ với OID land ADR-0060 trên first-parent master")
        return spec

    def k4():
        if a.human_audit_comment:
            if spec is None:
                raise ValueError("K4 human cần K1 hợp lệ")
            _human_merge(a, root, lease, spec, p3)
        if not (a.offline_run_json or a.offline_stdout):
            if a.human_audit_comment:
                return
            raise ValueError("thiếu review model hoặc human độc lập")
        if not (a.offline_run_json and a.offline_stdout):
            raise ValueError("thiếu cặp --offline-run-json/--offline-stdout")
        r = _doc_json(a.offline_run_json, RC_GATE)[0]
        out = Path(a.offline_stdout).read_bytes()
        dong = [x for x in out.decode("utf-8").splitlines() if x.strip()]
        if not (isinstance(r, dict) and r.get("head") == h and r.get("trang_thai") == "xong" and type(r.get("ma_thoat")) is int and r["ma_thoat"] == 0
                and r.get("stdout_sha256") == hashlib.sha256(out).hexdigest() and dong and dong[-1].strip() == "KET_LUAN: approve"):
            _die(RC_GATE, "review offline chưa approve đúng head (run.json head/trang_thai/ma_thoat/stdout_sha256 hoặc dòng KET_LUAN)")

    def k5():
        mo = {f"{k}:{i}" for k, i in p3} | set(a.p3_offline or [])
        mien = [m[1] for x in _dong_chu_kho(a.chu_kho_comment) for m in [re.fullmatch(rf"mien_p3: {h} (\S+)", x)] if m]
        if mo and (len(mien) != 1 or set(mien[0].split(",")) != mo):
            _die(RC_GATE, f"P3 còn mở {sorted(mo)} chưa có đúng một dòng `mien_p3: {h} …` của chủ kho phủ ĐÚNG tập ấy")

    def k6(spec):
        loai = _phan_loai_windows(root, a.base, h, spec)
        dong = _dong_chu_kho(a.chu_kho_comment) if loai != "not_required" else []
        if loai == "unknown" and f"windows: {h} not_required" not in dong:
            _die(RC_GATE, "Windows `unknown` chưa được chủ kho chốt")
        if loai == "required" and f"windows: {h} mien" not in dong:
            w = _doc_json(a.windows_json, RC_GATE)[0] if a.windows_json else {}
            ts = w.get("tests") if isinstance(w, dict) else None
            if not (w.get("sha") == h and w.get("os") == "Windows" and isinstance(ts, list) and ts and all(isinstance(x, dict) and type(x.get("id")) is str and x["id"] for x in ts)
                    and len({x.get("id") for x in ts}) == len(ts) and all(x.get("ket_qua") == "passed" for x in ts)):
                _die(RC_GATE, "Windows `required`: thiếu lượt ứng viên xanh (sha = head, os Windows, tests khác rỗng, mọi ca passed) hoặc dòng miễn")

    def k7():  # #1120 ADR-0060 M9: run `ci-dot-bien-du.yml` success ĐÚNG H với mọi job của đúng run_id/run_attempt, hoặc dòng miễn của chủ kho
        try:
            mien = bool(a.chu_kho_comment) and f"full_mutant_audit: {h} mien" in _dong_chu_kho(a.chu_kho_comment, tho=True)
        except ValueError:  # lượt 4 F25: comment KHÔNG của chủ kho không cấp miễn, cũng không phủ quyết nhánh (b) run xanh
            mien = False
        if not _cham_m9(root, a.base, h) or mien:
            return
        if not (a.dot_bien_du_runs and a.dot_bien_du_jobs):
            _die(RC_GATE, "diff chạm vùng M9 mà thiếu --dot-bien-du-runs/--dot-bien-du-jobs và dòng miễn `full_mutant_audit: H mien` của chủ kho")
        runs = _trang_du(_doc_json(a.dot_bien_du_runs, RC_GATE)[0], "workflow_runs", "--dot-bien-du-runs")
        # review offline lượt 1 F01/F02: MỖI tệp jobs là một lần lấy của MỘT (run_id, run_attempt) — trang đủ đo trên ĐÚNG tập dùng để quyết
        # định; định danh phải đúng kiểu int ở cả hai phía (bool/float bằng nhau với int dưới `==`); một run/attempt không được ở hai tệp.
        nhom = {}
        for p in a.dot_bien_du_jobs:
            js = _trang_du(_doc_json(p, RC_GATE)[0], "jobs", f"--dot-bien-du-jobs {p}")
            khoa = {(j.get("run_id"), j.get("run_attempt")) for j in js}
            if not all(type(j.get("run_id")) is int and type(j.get("run_attempt")) is int for j in js) or len(khoa) > 1 or khoa & nhom.keys():
                _die(RC_GATE, f"--dot-bien-du-jobs {p}: phải là jobs của đúng MỘT run_id + run_attempt (int), không lặp ở tệp khác")
            nhom.update(dict.fromkeys(khoa, js))
        xanh = lambda x: x.get("status") == "completed" and x.get("conclusion") == "success"  # noqa: E731
        for r in runs:
            js = nhom.get((r["id"], r["run_attempt"])) if type(r.get("run_attempt")) is int else None
            if r.get("path") == DOT_BIEN_DU_TEP and r.get("head_sha") == h and xanh(r) and js and all(map(xanh, js)):
                return
        _die(RC_GATE, f"không run `{DOT_BIEN_DU_TEP}` nào success tại {h} với mọi job (đúng run_id + run_attempt) success")

    _dk("K0 đầu vào neo", k0, thieu)
    spec = _dk("K1 hiệu lực M10", k1, thieu)
    _dk("K2 CI", lambda: _kiem_ci(a, {"required_checks": [list(x) for x in CHECK_BAT_BUOC], "repo": a.repo}, h, state_dir), thieu)
    p3 += (_dk("K3 connector", lambda: _doc_connector(a.connector, a.repo, a.pr, h), thieu) or ([], None))[0]
    _dk("K4 review offline", k4, thieu)
    if not any(x.startswith("K3") for x in thieu):
        _dk("K5 P3", k5, thieu)
    if spec is not None:
        _dk("K6 Windows", lambda: k6(spec), thieu)
    _dk("K7 full_mutant_audit", k7, thieu)
    if thieu:
        for x in thieu:
            print(f"  THIẾU  {x}", file=sys.stderr)
        _die(RC_GATE, "CHƯA ĐỦ ĐIỀU KIỆN MERGE: thiếu " + "; ".join(x.split(":")[0] for x in thieu))
    print(f"ĐỦ ĐIỀU KIỆN MERGE trên {h}")
    return RC_OK


def cmd_kiem_dong_wp(a, state_dir: Path) -> int:
    root, thieu = Path(a.root), []
    hex64, url = re.compile(r"[0-9a-f]{64}\Z"), re.compile(r"https://github\.com/\S+\Z")
    so = lambda v: type(v) is int and v >= 1  # noqa: E731
    try:
        bb, ls = _yaml_cay(Path(a.bien_ban).read_bytes()), _yaml_cay(Path(a.lease).read_bytes())
    except (OSError, ValueError, UnicodeDecodeError) as ex:
        _die(RC_ARG, f"không đọc được biên bản/lease: {type(ex).__name__}: {ex}")
    if not (isinstance(bb, dict) and isinstance(ls, dict)):
        _die(RC_ARG, "biên bản và lease phải là mapping")
    chuoi = lambda v, r=None: type(v) is str and bool(v.strip()) and (r is None or bool(r.fullmatch(v)))  # noqa: E731
    luat = {"packet": chuoi, "revision": so, "generation": so, "spec_hash": lambda v: chuoi(v, hex64), "head_da_review": lambda v: chuoi(v, SHA_RE),
            "tree_h": lambda v: chuoi(v, SHA_RE), "review": lambda v: isinstance(v, dict), "windows": lambda v: isinstance(v, dict),
            "duyet_chu_kho": lambda v: chuoi(v, url), "merge_commit": lambda v: chuoi(v, SHA_RE), "tree_m": lambda v: chuoi(v, SHA_RE),
            "ci_master": lambda v: isinstance(v, dict) and so(v.get("run_id")) and chuoi(v.get("conclusion")),
            "nghiem_thu": lambda v: isinstance(v, dict) and bool(v), "lease_cuoi": chuoi, "landed": lambda v: type(v) is bool,
            "moc_10_2_2": lambda v: isinstance(v, dict) and sorted(v) == sorted(MOC_10_2_2)}
    if sai := [k for k, f in luat.items() if not f(bb.get(k))]:
        thieu.append(f"D1 trường M8: thiếu hoặc sai kiểu {sai}")
    elif not (bb["landed"] is True and all(v in DAT_MOC for v in bb["moc_10_2_2"].values())
              and all(v in DAT_MOC for v in bb["nghiem_thu"].values()) and bb["ci_master"]["conclusion"] == "success"):
        thieu.append("D2 chưa land: landed, bốn mốc, nghiệm thu và CI master phải cùng đạt")
    if not sai:
        m, hh = bb["merge_commit"], bb["head_da_review"]
        g = lambda *x: (lambda r: r[1].decode().split() if r[0] == 0 else ["<git lỗi>"])(_git_do(root, *x))  # noqa: E731 — rc ≠ 0 ⇒ không khớp
        if (g("rev-parse", f"{m}^2") != [hh] or g("rev-parse", f"{hh}^{{tree}}") != [bb["tree_h"]] or g("rev-parse", f"{m}^{{tree}}") != [bb["tree_m"]]
                or m not in g("rev-list", "--first-parent", "refs/remotes/origin/master")):
            thieu.append("D3 git: merge_commit^2/tree_h/tree_m/first-parent master không khớp")
        try:
            het = datetime.strptime(str(ls.get("lease_until")), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc)
        except (ValueError, OverflowError):
            het = False
        if not (ls.get("lease_id") == bb["lease_cuoi"] and ls.get("packet_id") == bb["packet"] and ls.get("generation") == bb["generation"]
                and type(ls.get("generation")) is int and het):
            thieu.append("D4 lease: không khớp lease_cuoi/packet/generation hoặc lease_until chưa qua")
    if thieu:
        for x in thieu:
            print(f"  THIẾU  {x}", file=sys.stderr)
        _die(RC_GATE, "CHƯA ĐÓNG ĐƯỢC WP: thiếu " + "; ".join(x.split(" ")[0] for x in thieu))
    print(f"ĐÓNG ĐƯỢC WP {bb['packet']} — merge {bb['merge_commit']}")
    return RC_OK


# WP1174 r7: pure lineage grammar. These validators do not grant runtime authority.
_W1174_KEYS = frozenset(("origin", "enrollment_id", "binding_sha256", "active_generation",
                        "phase", "witness_revision", "high_water", "pending_adoption", "suspended", "history"))
_P1174_KEYS = frozenset(("adoption_id", "generation", "binding_sha256", "canonical_path", "source_sha256", "cutover_started"))
_H1174_KEYS = frozenset(("terminal_kind", "adoption_id", "binding_sha256", "generation", "canonical_path",
                        "as_of_revision", "as_of_sha256", "terminal_disposition"))
_T1174_DISPOSITIONS = {"adopted": "resume_forward", "aborted": "abandon_before_cutover",
                       "aborted_intent": "abandon_before_prepare"}


class _1174Error(ValueError):
    def __init__(self, reason, status="UNKNOWN"):
        super().__init__("WP1174 UNKNOWN: " + reason)
        self.status = status


def _1174_require(ok, reason):
    if not ok:
        status = ("input_rejected" if reason.startswith("input_rejected:") else
                  reason if reason in ("revision_rejected", "legacy_changed") else
                  "FAIL" if reason == "publication evidence FAIL" else "UNKNOWN")
        raise _1174Error(reason, status)


def _1174_int(value):
    return type(value) is int and value >= 0


def _1174_hash(value):
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value, re.ASCII) is not None


def _1174_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def _1174_json(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            _1174_require(key not in value, "duplicate JSON key")
            value[key] = item
        return value
    def constant(_):
        raise ValueError("WP1174 UNKNOWN: nonfinite JSON")
    _1174_require(type(raw) is bytes, "JSON bytes required")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except (UnicodeError, json.JSONDecodeError) as ex:
        raise ValueError("WP1174 UNKNOWN: invalid JSON encoding/syntax") from ex
    _1174_require(_1174_bytes(value) == raw, "noncanonical JSON bytes")
    return value


def _1174_identity(node):
    _1174_require(type(node.get("adoption_id")) is str and re.fullmatch(
        r"[a-z0-9][a-z0-9._-]{0,127}", node["adoption_id"], re.ASCII) is not None, "adoption ID")
    _1174_require(_1174_int(node.get("generation")), "generation integer")
    _1174_require(_1174_hash(node.get("binding_sha256")), "operation binding hash")
    path = node.get("canonical_path")
    _1174_require(type(path) is str and path and str(Path(path)) == path and Path(path).is_absolute()
                  and ".." not in Path(path).parts, "canonical target path")


def _1174_pending(node, expected=None):
    _1174_require(type(node) is dict and set(node) == _P1174_KEYS, "pending keyset")
    _1174_identity(node)
    _1174_require(_1174_hash(node["source_sha256"]) and type(node["cutover_started"]) is bool,
                  "pending source/intent")
    if expected is not None:
        _1174_require(type(expected) is dict and set(expected) == _P1174_KEYS and all(
            type(node[k]) is type(expected[k]) and node[k] == expected[k] for k in _P1174_KEYS),
            "pending operation differs from resolved binding")
    return node


def _1174_history(nodes, g0):
    _1174_require(type(nodes) is list, "history list")
    seen = {key: set() for key in ("generation", "canonical_path", "adoption_id")}
    previous = g0
    for node in nodes:
        _1174_require(type(node) is dict and set(node) == _H1174_KEYS, "history keyset")
        _1174_identity(node)
        kind = node["terminal_kind"]
        _1174_require(type(kind) is str and kind in _T1174_DISPOSITIONS and
                      node["terminal_disposition"] == _T1174_DISPOSITIONS[kind], "history terminal disposition")
        _1174_require(node["generation"] > previous, "history generation order")
        previous = node["generation"]
        for key in seen:
            _1174_require(node[key] not in seen[key], "history duplicate " + key)
            seen[key].add(node[key])
        if kind == "aborted_intent":
            _1174_require(node["as_of_revision"] is None and node["as_of_sha256"] is None,
                          "aborted intent has no target image")
        else:
            _1174_require(_1174_int(node["as_of_revision"]) and _1174_hash(node["as_of_sha256"]),
                          "terminal target revision/hash")
    return nodes


def _1174_reserved(enrollment_id, binding_sha256, g0):
    return dict(origin="fresh_init", enrollment_id=enrollment_id, binding_sha256=binding_sha256,
                active_generation=g0, phase="reserved", witness_revision=0, high_water=None,
                pending_adoption=None, suspended=False, history=[])


def _1174_witness(raw, enrollment_id, binding_sha256, g0, pending=None):
    """Validate r20's four rows using enrollment facts already resolved by the caller.

    No filesystem, OS probe, normalization or authority acquisition occurs here.
    """
    _1174_require(type(enrollment_id) is str and enrollment_id and _1174_hash(binding_sha256)
                  and _1174_int(g0), "resolved enrollment facts")
    w = _1174_json(raw)
    _1174_require(type(w) is dict and set(w) == _W1174_KEYS, "witness keyset")
    _1174_require(type(w["origin"]) is str and w["origin"] in ("fresh_init", "imported_lineage")
                  and type(w["phase"]) is str and w["phase"] in ("reserved", "initialized"), "witness origin/phase")
    _1174_require(type(w["enrollment_id"]) is str and w["enrollment_id"] == enrollment_id
                  and _1174_hash(w["binding_sha256"]) and w["binding_sha256"] == binding_sha256,
                  "witness enrollment binding")
    _1174_require(_1174_int(w["active_generation"]) and _1174_int(w["witness_revision"]), "witness integer types")
    _1174_require(type(w["suspended"]) is bool, "witness suspended type")
    history = _1174_history(w["history"], g0)
    if w["pending_adoption"] is not None:
        _1174_pending(w["pending_adoption"], pending)
    adopted = [n for n in history if n["terminal_kind"] == "adopted"]
    _1174_require(w["suspended"] == bool(history and history[-1]["terminal_kind"] in
                  ("aborted", "aborted_intent")), "suspended does not match terminal history")
    if w["phase"] == "reserved":
        _1174_require(w["high_water"] is None and w["active_generation"] == g0 and not adopted,
                      "reserved active/high_water/history")
        if w["origin"] == "fresh_init":
            _1174_require(raw == _1174_bytes(_1174_reserved(enrollment_id, binding_sha256, g0)),
                          "fresh reserved exact image")
        else:
            _1174_require(bool(history) or w["pending_adoption"] is not None, "imported reserved needs pending")
            if not history:
                _1174_require(w["pending_adoption"]["cutover_started"] is False or w["witness_revision"] > 0,
                              "initial imported intent must be false")
    else:
        water = w["high_water"]
        _1174_require(type(water) is dict and set(water) == {"generation", "state_revision", "state_sha256"}
                      and _1174_int(water["generation"]) and _1174_int(water["state_revision"])
                      and _1174_hash(water["state_sha256"]) and water["generation"] == w["active_generation"],
                      "initialized high_water")
        _1174_require(w["witness_revision"] >= 1 and
                      w["active_generation"] == (adopted[-1]["generation"] if adopted else g0)
                      and (w["origin"] != "imported_lineage" or bool(adopted)), "initialized active generation")
    if w["pending_adoption"] is not None:
        node = _1174_pending(w["pending_adoption"], pending)
        _1174_require(node["generation"] > max([w["active_generation"], *[n["generation"] for n in history]])
                      and all(node[k] != old[k] for old in history for k in ("canonical_path", "adoption_id")),
                      "pending collides with lineage")
    else:
        _1174_require(pending is None, "resolved pending missing")
    return w


def _1174_tombstone(packet, source_generation, target_generation, adoption_id, source_sha256, binding_sha256):
    _1174_require(type(packet) is int and packet > 0 and _1174_int(source_generation)
                  and _1174_int(target_generation) and target_generation > source_generation, "tombstone generations")
    _1174_require(type(adoption_id) is str and re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,127}", adoption_id,
                  re.ASCII) is not None and _1174_hash(source_sha256) and _1174_hash(binding_sha256), "tombstone identity")
    return _1174_bytes(dict(format="packet_state_retired.v1", packet_id=packet, from_generation=source_generation,
                           to_generation=target_generation, adoption_id=adoption_id,
                           source_sha256=source_sha256, binding_sha256=binding_sha256))


def _1174_witness_transition(before, after, enrollment_id, binding_sha256, g0, action):
    """Prevalidate the exact witness proposal; callers must separately validate target proposals.

    This is a pure predicate. A valid transition has neither write nor dispatch authority.
    """
    new = _1174_witness(after, enrollment_id, binding_sha256, g0)
    if before is None:
        _1174_require(action in ("fresh_enrollment", "imported_enrollment") and
                      new["witness_revision"] == 0 and new["phase"] == "reserved" and
                      new["active_generation"] == g0 and not new["history"] and not new["suspended"],
                      "initial witness publication")
        _1174_require((action == "fresh_enrollment" and new["origin"] == "fresh_init") or
                      (action == "imported_enrollment" and new["origin"] == "imported_lineage" and
                       new["pending_adoption"] is not None and new["pending_adoption"]["cutover_started"] is False),
                      "initial witness origin/pending")
        return new
    old = _1174_witness(before, enrollment_id, binding_sha256, g0)
    _1174_require(new["witness_revision"] == old["witness_revision"] + 1, "witness revision step")
    _1174_require(all(new[k] == old[k] for k in ("origin", "enrollment_id", "binding_sha256")),
                  "immutable witness enrollment")
    changed = {k for k in _W1174_KEYS if new[k] != old[k]} - {"witness_revision"}
    _1174_require(new["history"][:len(old["history"])] == old["history"], "append-only history")
    if action == "resume_init":
        _1174_require(old["origin"] == "fresh_init" and old["phase"] == "reserved" and
                      new["phase"] == "initialized" and new["high_water"]["state_revision"] == 0 and
                      changed == {"phase", "high_water"}, "resume initialization transition")
    elif action == "adopt_pending":
        _1174_require(old["pending_adoption"] is None and (old["phase"] == "initialized" or
                      (old["origin"] == "imported_lineage" and old["phase"] == "reserved" and
                       bool(old["history"]) and old["suspended"])) and new["pending_adoption"] is not None and
                      new["pending_adoption"]["cutover_started"] is False and changed == {"pending_adoption"},
                      "adoption initial whitelist")
    elif action == "cutover_intent":
        p, q = old["pending_adoption"], new["pending_adoption"]
        _1174_require(p is not None and p["cutover_started"] is False and
                      q == dict(p, cutover_started=True) and changed == {"pending_adoption"}, "monotonic cutover intent")
    elif action in ("abandon_before_prepare", "abandon_before_cutover", "adopt_finalize"):
        p = old["pending_adoption"]
        _1174_require(p is not None and new["pending_adoption"] is None and
                      len(new["history"]) == len(old["history"]) + 1, "terminal history append")
        node = new["history"][-1]
        _1174_require(all(node[k] == p[k] for k in ("adoption_id", "binding_sha256", "generation", "canonical_path")),
                      "terminal operation binding")
        if action == "adopt_finalize":
            water = new["high_water"]
            _1174_require(p["cutover_started"] is True and node["terminal_kind"] == "adopted" and
                          new["phase"] == "initialized" and new["active_generation"] == p["generation"] and
                          water == dict(generation=p["generation"], state_revision=node["as_of_revision"],
                                        state_sha256=node["as_of_sha256"]) and not new["suspended"] and
                          changed <= {"phase", "active_generation", "high_water", "pending_adoption", "history", "suspended"},
                          "adoption finalize transition")
        else:
            _1174_require(p["cutover_started"] is False and node["terminal_disposition"] == action and
                          changed <= {"pending_adoption", "history", "suspended"} and new["suspended"],
                          "abandon transition")
    elif action == "ordinary":
        _1174_require(old["phase"] == "initialized" and old["pending_adoption"] is None and not old["suspended"] and
                      new["high_water"]["state_revision"] == old["high_water"]["state_revision"] + 1 and
                      changed == {"high_water"}, "ordinary high_water transition")
    else:
        raise ValueError("WP1174 UNKNOWN: unknown witness action")
    return new


def _1174_read(path):
    """Read one regular file without following the leaf; reject observed identity drift."""
    import stat
    path = Path(path)
    _1174_require(hasattr(os, "O_NOFOLLOW"), "O_NOFOLLOW unavailable")
    entry = path.lstat()
    _1174_require(stat.S_ISREG(entry.st_mode), "nonregular file")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        opened = os.fstat(fd)
        identity = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        _1174_require(stat.S_ISREG(opened.st_mode) and identity(entry) == identity(opened), "file identity at open")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            raw = stream.read()
        _1174_require(identity(opened) == identity(os.fstat(fd)) == identity(path.lstat()), "file identity after read")
        return raw
    finally:
        os.close(fd)


def _1174_fsyncdir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)



def _1174_recheck_durable(path, raw):
    """Re-establish file and parent durability of a visible reused image under lock."""
    global _1174_IO_STARTED
    path = Path(path)
    _1174_require(_1174_read(path) == raw, "reused artifact bytes changed")
    _1174_IO_STARTED = True
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        before = path.lstat()
        opened = os.fstat(fd)
        _1174_require((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino), "reused artifact identity")
        os.fsync(fd)
        _1174_fsyncdir(path.parent)
        _1174_require((opened.st_dev, opened.st_ino) == (path.lstat().st_dev, path.lstat().st_ino) and
                      _1174_read(path) == raw, "reused artifact durable readback")
    finally:
        os.close(fd)


def _1174_persist(path, raw, *, create):
    """Durable complete-temp publication. The transaction must hold its fixed lock.

    Failure deliberately leaves the durable prefix; the caller must not dispatch or retry.
    Only create uses hard-link no-replace; updates never unlink the final path.
    """
    import stat
    path = Path(path)
    _1174_require(type(raw) is bytes and type(create) is bool, "persist bytes/mode")
    if not create:
        _1174_require(stat.S_ISREG(path.lstat().st_mode), "update target regular file")
    else:
        try:
            path.lstat()
        except FileNotFoundError:
            pass
        else:
            raise FileExistsError(str(path))
    temporary = None
    try:
        fd, temporary = tempfile.mkstemp(prefix=".wp1174-", dir=path.parent)
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        _1174_fsyncdir(path.parent)
        if create:
            os.link(temporary, path, follow_symlinks=False)
        else:
            os.replace(temporary, path)
            temporary = None
        _1174_fsyncdir(path.parent)
        if temporary is not None:
            os.unlink(temporary)
            temporary = None
            _1174_fsyncdir(path.parent)
        _1174_require(_1174_read(path) == raw, "persist exact readback")
    finally:
        if temporary is not None:
            # Only our unlinked temporary image is removed, never a published final image.
            os.unlink(temporary)


@contextlib.contextmanager
def _1174_lock(path):
    import fcntl
    import stat
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_CLOEXEC | os.O_NOFOLLOW, 0o600)
    try:
        _1174_require(stat.S_ISREG(os.fstat(fd).st_mode), "fixed lock must be regular")
        fcntl.flock(fd, fcntl.LOCK_EX)
        _1174_require((os.fstat(fd).st_dev, os.fstat(fd).st_ino) ==
                      (Path(path).lstat().st_dev, Path(path).lstat().st_ino), "fixed lock identity")
        yield fd
    finally:
        os.close(fd)


def _1174_platform(os_name, fs_name, magic):
    return os_name == "Linux" and (fs_name, magic) in (("ext4", 0xEF53), ("xfs", 0x58465342))


def _1174_mount(path):
    """Return measured mountinfo and statfs facts; no name-only filesystem inference."""
    import ctypes
    path = Path(path)
    _1174_require(platform.system() == "Linux" and path.is_absolute() and path.resolve() == path,
                  "native Linux canonical path required")
    matches = []
    for line in Path("/proc/self/mountinfo").read_text(encoding="utf-8").splitlines():
        left, right = line.split(" - ", 1)
        fields = left.split()
        mountpoint = re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), fields[4])
        if Path(mountpoint) == path or Path(mountpoint) in path.parents:
            matches.append((len(Path(mountpoint).parts), fields[0], fields[2], mountpoint, right.split()[0]))
    _1174_require(bool(matches), "mountinfo path unresolved")
    depth = max(row[0] for row in matches)
    active = [row for row in matches if row[0] == depth]
    _1174_require(len(active) == 1, "ambiguous active mount identity")
    _, mount_id, device, mountpoint, fs_name = active[0]
    # Linux statfs starts with a native signed long f_type. Oversized aligned storage
    # avoids depending on libc's architecture-specific trailing statfs fields.
    buffer = (ctypes.c_long * 64)()
    libc = ctypes.CDLL(None, use_errno=True)
    libc.statfs.argtypes = (ctypes.c_char_p, ctypes.c_void_p)
    libc.statfs.restype = ctypes.c_int
    if libc.statfs(os.fsencode(path), ctypes.byref(buffer)) != 0:
        raise OSError(ctypes.get_errno(), "statfs")
    return dict(mount_id=mount_id, device=device, mountpoint=mountpoint, filesystem=fs_name,
                magic=int(buffer[0]), st_dev=path.stat().st_dev)


def _1174_probe(root):
    """Native capability measurements; an unsupported mount is an error, never a skip."""
    root = Path(root)
    facts = _1174_mount(root)
    _1174_require(_1174_platform(platform.system(), facts["filesystem"], facts["magic"]),
                  "unsupported native filesystem: " + facts["filesystem"])
    outcomes = {}
    with tempfile.TemporaryDirectory(prefix=".wp1174-probe-", dir=root) as temporary:
        directory = Path(temporary)
        _1174_require(_1174_mount(directory) == facts, "probe mount identity")
        first, second, lock = (directory / n for n in ("first", "second", "lock"))
        _1174_persist(first, b"complete-one\n", create=True)
        outcomes["file_fsync_directory_fsync_readback"] = _1174_read(first) == b"complete-one\n"
        os.link(first, second, follow_symlinks=False)
        try:
            os.link(first, second, follow_symlinks=False)
        except FileExistsError:
            outcomes["link_no_replace_eexist"] = _1174_read(second) == b"complete-one\n"
        else:
            outcomes["link_no_replace_eexist"] = False
        _1174_persist(first, b"complete-two\n", create=False)
        outcomes["replace"] = _1174_read(first) == b"complete-two\n" and _1174_read(second) == b"complete-one\n"
        with _1174_lock(lock) as fd:
            outcomes["cloexec"] = not os.get_inheritable(fd)
            code = ("import fcntl,os,sys; f=os.open(sys.argv[1],os.O_RDWR); "
                    "\ntry: fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)"
                    "\nexcept BlockingIOError: sys.exit(23)"
                    "\nsys.exit(24)")
            child = subprocess.run([sys.executable, "-B", "-c", code, str(lock)],
                                   capture_output=True, timeout=10, close_fds=True)
            outcomes["lock_contention_process"] = child.returncode == 23 and not child.stdout and not child.stderr
        outcomes["fixed_lock_retained"] = lock.is_file()
        outcomes["mount_identity"] = _1174_mount(directory) == facts
        outcomes["tripwire"] = _1174_read(first) == b"complete-two\n"
    _1174_require(all(outcomes.values()), "native capability probe failed: " + repr(outcomes))
    return dict(facts=facts, outcomes=outcomes, native_seam_used=False)


def _1174_status(status, guard=False):
    """Closed result table; only one pair of status/rc can authorize dispatch."""
    success = {"completed_no_dispatch", "already_completed_no_dispatch", "reserved_for_dispatch"}
    rejected = {"UNKNOWN", "durability_unknown", "legacy_changed", "revision_rejected", "admission_rejected"}
    if guard:
        _1174_require(status in {"PASS", "FAIL", "UNKNOWN", "admission_rejected", "input_rejected"}, "unknown guard status")
        return (0 if status == "PASS" else 2 if status == "input_rejected" else 12), False
    _1174_require(status in success | rejected | {"input_rejected", "quota_exhausted"}, "unknown mutator status")
    rc = 0 if status in success else 2 if status == "input_rejected" else 3 if status == "quota_exhausted" else 8
    return rc, status == "reserved_for_dispatch"


_1174_REPO = "ducthangho/tra-luat"
_1174_REGISTRATION_KEYS = frozenset(("schema", "mission", "mission_revision", "mission_plan_sha256",
    "packet", "revision", "generation", "spec_ref", "spec_path", "spec_sha256", "admission_ref",
    "admission_path", "admission_sha256", "enrollment_id", "binding_sha256", "expires_utc", "revoked"))
_1174_ADMISSION_KEYS = frozenset(("schema", "mission", "mission_revision", "mission_plan_sha256", "packet",
    "contract_id", "revision", "generation", "base", "enrollment", "lineage", "operation", "allowance", "expires_utc"))


def _1174_time(value):
    _1174_require(type(value) is str and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", value),
                  "UTC timestamp required")
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _1174_registration(value, packet, revision, generation, now):
    _1174_require(type(value) is dict and set(value) == _1174_REGISTRATION_KEYS, "registration keyset")
    _1174_require(value["schema"] == "wp1174_registration.v1" and type(value["revoked"]) is bool and
                  not value["revoked"] and _1174_time(value["expires_utc"]) > now, "expired/revoked registration")
    _1174_require(value["mission"] == 1172 and type(value["mission"]) is int and all(
        type(value[k]) is int and value[k] > 0 for k in ("packet", "revision", "generation", "mission_revision")) and
        (value["packet"], value["revision"], value["generation"]) == (packet, revision, generation), "registration scope")
    _1174_require(all(_1174_hash(value[k]) for k in ("mission_plan_sha256", "spec_sha256", "admission_sha256", "binding_sha256"))
                  and type(value["enrollment_id"]) is str and bool(value["enrollment_id"]), "registration hashes/enrollment")
    for prefix in ("spec", "admission"):
        ref, path = value[prefix + "_ref"], value[prefix + "_path"]
        _1174_require(type(ref) is str and re.fullmatch(r"refs/heads/[A-Za-z0-9._/-]+@[0-9a-f]{40}", ref)
                      and ".." not in ref and type(path) is str and path and not PurePosixPath(path).is_absolute()
                      and ".." not in PurePosixPath(path).parts and str(PurePosixPath(path)) == path, "immutable descriptor")
    return value


_1174_ADMISSION_TYPES = {
    "schema":str,"mission":int,"mission_revision":int,"mission_plan_sha256":str,"packet":int,"revision":int,"generation":int,
    "contract_id":str,"base":str,"enrollment":dict,"lineage":dict,"operation":(dict,type(None)),"allowance":dict,"expires_utc":str}
_1174_ENROLLMENT_TYPES = {
    "id":str,"binding_sha256":str,"coordinator_id":str,"boot_id":str,"root":str,"root_device":int,"root_inode":int,
    "mount_id":str,"mount_device":str,"filesystem":str,"magic":int,"state_path":str,"witness_path":str,"lock_path":str,
    "initial_state_path":str,"legacy_source_path":(str,type(None)),"legacy_source_sha256":(str,type(None)),"g0":int,"origin":str,
    "initial_state_projection":dict,"private_seed_path":str,"private_seed_sha256":str,"git_root":str,"journal_root":str,
    "producer_handoffs":list,"quiescent":bool}
_1174_OPERATION_TYPES = {"adoption_id":str,"generation":int,"binding_sha256":str,"canonical_path":str,"source_sha256":str,"cutover_started":bool}
_1174_LINEAGE_TYPES = {"predecessor_generation":(int,type(None)),"source_path":(str,type(None)),"source_sha256":(str,type(None))}
_1174_ALLOWANCE_TYPES = {"window_id":str,"starts_utc":str,"ends_utc":str,"attempts_limit":int,"review_rounds_limit":int,"codex_review_calls_limit":int}


def _1174_field_types(admission):
    for prefix,record,schema in (("",admission,_1174_ADMISSION_TYPES),("enrollment.",admission.get("enrollment"),_1174_ENROLLMENT_TYPES),
            ("lineage.",admission.get("lineage"),_1174_LINEAGE_TYPES),("allowance.",admission.get("allowance"),_1174_ALLOWANCE_TYPES),
            ("operation.",admission.get("operation"),_1174_OPERATION_TYPES)):
        if prefix=="operation." and record is None:continue
        _1174_require(type(record) is dict and set(record)==set(schema),"field record keyset "+prefix)
        for field,kind in schema.items():
            path=prefix+field
            expected=kind if type(kind) is tuple else (kind,)
            _1174_require(type(record[field]) in expected,"field type "+path)


def _1174_admission(raw, registration, now):
    """Closed payload validation after immutable-byte and current-authority verification."""
    a = _1174_json(raw)
    _1174_require(type(a) is dict and set(a) == _1174_ADMISSION_KEYS,
                  "admission keyset/schema")
    _1174_field_types(a)
    _1174_require(a["schema"] == "wp1174_admission.v1", "admission schema")
    for key in ("mission", "mission_revision", "packet", "revision", "generation", "mission_plan_sha256"):
        _1174_require(type(a[key]) is type(registration[key]) and a[key] == registration[key], "admission scope " + key)
    _1174_require(type(a["contract_id"]) is str and a["contract_id"] and type(a["base"]) is str and
                  SHA_RE.fullmatch(a["base"]) and _1174_time(a["expires_utc"]) > now and
                  _1174_time(a["expires_utc"]) <= _1174_time(registration["expires_utc"]), "admission contract/base/expiry")
    e = a["enrollment"]
    _1174_require(type(e) is dict and set(e) == {"id", "binding_sha256", "coordinator_id", "boot_id", "root",
                  "root_device", "root_inode", "mount_id", "mount_device", "filesystem", "magic", "state_path",
                  "witness_path", "lock_path", "initial_state_path", "legacy_source_path", "legacy_source_sha256",
                  "g0", "origin", "initial_state_projection", "private_seed_path", "private_seed_sha256",
                  "git_root", "journal_root", "producer_handoffs", "quiescent"},
                  "enrollment keyset")
    _1174_require(e["id"] == registration["enrollment_id"] and e["binding_sha256"] == registration["binding_sha256"]
                  and all(type(e[k]) is str and e[k] for k in ("id", "coordinator_id", "boot_id", "mount_id", "mount_device"))
                  and all(_1174_int(e[k]) for k in ("root_device", "root_inode", "magic", "g0")) and
                  e["origin"] in ("fresh_init", "imported_lineage") and type(e["quiescent"]) is bool and e["quiescent"]
                  and type(e["producer_handoffs"]) is list and bool(e["producer_handoffs"]) and all(
                      type(x) is str and x for x in e["producer_handoffs"]), "enrollment identity/quiescence")
    _1174_require(type(e["initial_state_projection"]) is dict and "hmac_key" not in e["initial_state_projection"]
                  and _1174_hash(e["private_seed_sha256"]) and type(e["filesystem"]) is str
                  and e["filesystem"] in ("ext4", "xfs"), "enrollment projection/seed/filesystem")
    for key in ("root", "journal_root", "git_root", "state_path", "witness_path", "lock_path", "initial_state_path", "private_seed_path"):
        _1174_require(type(e[key]) is str and Path(e[key]).is_absolute() and str(Path(e[key])) == e[key]
                      and ".." not in Path(e[key]).parts, "enrollment canonical paths")
    _1174_require(e["state_path"] == str(Path(e["journal_root"]) / f"wp{a['packet']}.json"), "journal Packet path")
    _1174_require(len({e[k] for k in ("state_path", "witness_path", "lock_path", "private_seed_path")}) == 4 and all(
        Path(e[k]).parent == Path(e["root"]) for k in ("witness_path", "lock_path", "private_seed_path")), "enrollment fixed lineage paths")
    _1174_require((e["legacy_source_path"] is None and e["legacy_source_sha256"] is None) or
                  (type(e["legacy_source_path"]) is str and Path(e["legacy_source_path"]).is_absolute()
                   and _1174_hash(e["legacy_source_sha256"])), "legacy source types")
    lineage = a["lineage"]
    _1174_require(type(lineage) is dict and set(lineage) == {"predecessor_generation", "source_path", "source_sha256"}, "lineage keyset")
    for source in (lineage["source_path"], e["legacy_source_path"]):
        _1174_require(source is None or (type(source) is str and Path(source).is_absolute()
                      and str(Path(source)) == source and ".." not in Path(source).parts and "//" not in source),
                      "source canonical paths")
    if lineage["predecessor_generation"] is None:
        _1174_require(lineage["source_path"] is None and lineage["source_sha256"] is None and
                      e["origin"] == "fresh_init" and a["generation"] == e["g0"] and
                      e["state_path"] == e["initial_state_path"], "fresh lineage sentinel/path equality")
    else:
        _1174_require(_1174_int(lineage["predecessor_generation"]) and
                      lineage["predecessor_generation"] < a["generation"] and _1174_hash(lineage["source_sha256"])
                      and type(lineage["source_path"]) is str and Path(lineage["source_path"]).is_absolute()
                      and e["state_path"] not in (lineage["source_path"], e["initial_state_path"]), "predecessor binding/target alias")
    _1174_require(all(e[k] not in (e["initial_state_path"], lineage["source_path"]) for k in
                  ("private_seed_path", "lock_path", "witness_path")), "lineage artifact alias")
    operation = a["operation"]
    _1174_require(operation is None or (type(operation) is dict and set(operation) == _P1174_KEYS), "operation schema")
    if operation is not None:
        _1174_pending(operation)
        _1174_require(operation["generation"] == a["generation"] and operation["canonical_path"] == e["state_path"] and
                      operation["source_sha256"] == lineage["source_sha256"] and not operation["cutover_started"], "operation source/generation")
    allowance = a["allowance"]
    _1174_require(type(allowance) is dict and set(allowance) == {"window_id", "starts_utc", "ends_utc", "attempts_limit",
                  "review_rounds_limit", "codex_review_calls_limit"} and type(allowance["window_id"]) is str and allowance["window_id"] and
                  _1174_time(allowance["starts_utc"]) <= now < _1174_time(allowance["ends_utc"]) <= _1174_time(a["expires_utc"])
                  and all(type(allowance[k]) is int and allowance[k] > 0 for k in
                      ("attempts_limit", "review_rounds_limit", "codex_review_calls_limit")), "allowance window/limits")
    return a


def _1174_source_binding(witness, admission, observed_path, raw, *, recovery=False):
    """Read-only initial-adoption source predicate; no high_water repair is allowed."""
    e, lineage = admission["enrollment"], admission["lineage"]
    digest = hashlib.sha256(raw).hexdigest()
    _1174_require(digest == lineage["source_sha256"] and observed_path == lineage["source_path"], "source immutable bytes/path")
    if witness is not None and witness["phase"] == "initialized":
        adopted = [n for n in witness["history"] if n["terminal_kind"] == "adopted"]
        active_path = adopted[-1]["canonical_path"] if adopted else e["initial_state_path"]
        water = witness["high_water"]
        _1174_require((recovery or witness["pending_adoption"] is None) and lineage["predecessor_generation"] == witness["active_generation"]
                      and observed_path == active_path and digest == water["state_sha256"], "initialized source high_water/path")
        state = _1174_json(raw)
        _1174_require(type(state) is dict and type(state.get("schema_version")) is int and state["schema_version"] == 3
                      and type(state.get("packet")) is int and state["packet"] == admission["packet"]
                      and type(state.get("mission")) is int and state["mission"] == admission["mission"]
                      and _1174_int(state.get("generation")) and state["generation"] == witness["active_generation"]
                      and _1174_int(state.get("state_revision")) and state["state_revision"] == water["state_revision"],
                      "initialized source state generation/revision/identity")
        _1174_require(state.get("enrollment_id") == e["id"] and state.get("binding_sha256") == e["binding_sha256"],
                      "initialized source lineage identity")
    else:
        _1174_require(e["origin"] == "imported_lineage" and lineage["predecessor_generation"] == e["g0"]
                      and observed_path == e["legacy_source_path"] and digest == e["legacy_source_sha256"], "legacy enrollment source")
        if witness is not None:
            if recovery:
                _1174_require(witness["origin"] == "imported_lineage" and witness["phase"] == "reserved" and
                    all(n["terminal_kind"] in ("aborted", "aborted_intent") for n in witness["history"]), "legacy recovery branch")
            else:
                _1174_require(witness["origin"] == "imported_lineage" and witness["phase"] == "reserved" and
                          witness["pending_adoption"] is None and witness["suspended"] and bool(witness["history"])
                          and all(n["terminal_kind"] in ("aborted", "aborted_intent") for n in witness["history"]), "legacy retry branch")
        state = json.loads(raw.decode("utf-8"), object_pairs_hook=_cam_khoa_trung, parse_constant=_cam_hang_ngoai_json)
        _1174_require(type(state) is dict and type(state.get("schema_version")) is int and state["schema_version"] == 2
                      and type(state.get("packet")) is int and state["packet"] == admission["packet"]
                      and type(state.get("mission")) is int and state["mission"] == admission["mission"], "legacy source v2 identity")
    _1174_tripwire(state, e["g0"])
    return state


def _1174_api_env():
    env=os.environ.copy()
    env.pop("GH_HOST",None);env.pop("GH_REPO",None)
    env["GH_HOST"]="github.com"
    return env


def _1174_process(argv, *, cwd, deadline, max_bytes, env=None):
    """Read bounded pipes and kill only this process group on timeout/overflow."""
    import selectors
    import signal
    _1174_require(time.time()<deadline and type(max_bytes) is int and max_bytes>0,"transport deadline/byte budget")
    child=subprocess.Popen(argv,cwd=str(cwd),env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        close_fds=True,start_new_session=True)
    streams={child.stdout:bytearray(),child.stderr:bytearray()}
    try:
        with selectors.DefaultSelector() as selector:
            for pipe in streams:
                os.set_blocking(pipe.fileno(),False);selector.register(pipe,selectors.EVENT_READ)
            size=0
            while selector.get_map():
                remaining=deadline-time.time()
                _1174_require(remaining>0,"transport deadline")
                for key,_ in selector.select(min(remaining,0.1)):
                    raw=os.read(key.fileobj.fileno(),min(65536,max_bytes-size+1))
                    if not raw:selector.unregister(key.fileobj)
                    else:
                        size+=len(raw)
                        _1174_require(size<=max_bytes,"transport byte budget")
                        streams[key.fileobj].extend(raw)
            _1174_require(time.time()<deadline,"transport deadline")
            child.wait(timeout=max(0.001,deadline-time.time()))
        return subprocess.CompletedProcess(argv,child.returncode,bytes(streams[child.stdout]),bytes(streams[child.stderr]))
    finally:
        # The leader may already have exited while a descendant owns a pipe.
        # This session/group belongs only to this invocation, including cleanup.
        try:os.killpg(child.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        if child.poll() is None:child.wait(timeout=5)
        for pipe in streams:pipe.close()


def _1174_api(endpoint, *, root, deadline, max_bytes=30*1024*1024, on_bytes=None):
    _1174_require(type(endpoint) is str and (endpoint=="repos/"+_1174_REPO or endpoint.startswith("repos/"+_1174_REPO+"/")) and
        ".." not in endpoint and "\\" not in endpoint and Path(root).is_absolute(),"scoped API endpoint/root")
    result=_1174_process(["gh","api","--hostname","github.com",endpoint],cwd=Path(root),deadline=deadline,max_bytes=max_bytes,env=_1174_api_env())
    if on_bytes is not None:on_bytes(len(result.stdout)+len(result.stderr))
    _1174_require(time.time()<deadline and result.returncode==0,"scoped API unavailable/deadline")
    try:return json.loads(result.stdout.decode("utf-8"),object_pairs_hook=_cam_khoa_trung,parse_constant=_cam_hang_ngoai_json)
    except (UnicodeError,ValueError) as ex:raise ValueError("WP1174 UNKNOWN: scoped API JSON") from ex


def _1174_comments(packet, root):
    started, count, comments = time.monotonic(), 0, []
    deadline=time.time()+120
    for page in range(1, 101):
        _1174_require(time.monotonic() - started < 120, "authority collection deadline")
        measured=[]
        batch = _1174_api(f"repos/{_1174_REPO}/issues/{packet}/comments?per_page=100&page={page}",root=root,deadline=deadline,max_bytes=30*1024*1024-count,on_bytes=measured.append)
        _1174_require(time.time()<deadline and time.monotonic()-started<120,"authority collection deadline")
        _1174_require(type(batch) is list and len(batch) <= 100 and all(type(c) is dict for c in batch), "authority pagination")
        count += sum(measured) if measured else len(json.dumps(batch).encode("utf-8"))
        _1174_require(count <= 30 * 1024 * 1024, "authority collection byte budget")
        comments.extend(batch)
        if len(batch) < 100:
            return comments
    raise ValueError("WP1174 UNKNOWN: authority pagination incomplete")


def _1174_installed_mission(comments, admission, now):
    """Read the existing installed-decision wrapper; frozen proposed fields stay unchanged."""
    installed = []
    for c in comments:
        body = c.get("body")
        if not (type(body) is str and body.startswith("## Mission #1172 — Installed revision ") and
                c.get("user", {}).get("login") == CHU_KHO and c.get("user", {}).get("type") == "User" and
                c.get("author_association") == "OWNER"):
            continue
        ident = c.get("id")
        _1174_require(type(ident) is int and ident > 0 and c.get("issue_url") ==
            f"https://api.github.com/repos/{_1174_REPO}/issues/1172" and c.get("html_url") ==
            f"https://github.com/{_1174_REPO}/issues/1172#issuecomment-{ident}", "Mission installed decision origin")
        heading = re.match(r"## Mission #1172 — Installed revision ([1-9][0-9]*)\n", body)
        hashes = re.findall(r"Plan SHA256 `([0-9a-f]{64})`", body)
        blocks = re.findall(r"(?m)^```json\n(.*?)^```[ \t]*$", body, re.S)
        _1174_require(heading is not None and len(hashes) == len(blocks) == 1, "Mission installed wrapper")
        raw = blocks[0].encode("utf-8")
        _1174_require(hashlib.sha256(raw).hexdigest() == hashes[0], "Mission installed exact plan bytes")
        plan = json.loads(raw.decode("utf-8"), object_pairs_hook=_cam_khoa_trung,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite plan")))
        _1174_require(type(plan) is dict and type(plan.get("revision")) is int and
                      plan["revision"] == int(heading[1]) and plan.get("mission_id") == "gh-1172", "Mission installed identity")
        installed.append((_1174_time(c.get("updated_at")), ident, hashes[0], plan))
    _1174_require(bool(installed), "no current installed Mission decision")
    _, ident, digest, plan = max(installed, key=lambda row: row[:2])
    _1174_require(plan["revision"] == admission["mission_revision"] and digest == admission["mission_plan_sha256"],
                  "Mission installed revision/hash")
    graph = plan.get("packet_graph")
    _1174_require(type(graph) is list and all(type(row) is dict for row in graph), "Mission registered graph")
    matches = [row for row in graph if type(row.get("packet")) is int and row["packet"] == admission["packet"]]
    _1174_require(len(matches) == 1 and all(type(matches[0].get(k)) is type(admission[k]) and
                  matches[0][k] == admission[k] for k in ("revision", "generation", "contract_id")), "Mission registered Packet")
    exception = plan.get("routing_history", {}).get("previous_exception", {})
    _1174_require(exception.get("actual_human_audit_required") is True and
                  _1174_time(exception.get("hard_expiry_utc")) > now, "Mission route expiry/human requirement")
    return plan, ident


def _1174_git_env():
    selectors = {"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY",
                 "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_REPLACE_REF_BASE"}
    return {k: v for k, v in os.environ.items() if k not in selectors and not k.startswith("GIT_CONFIG_")}


@_1174_scoped
def _1174_git_view(root):
    root = Path(root)
    _1174_require(root.is_absolute() and root.resolve(strict=True) == root and (root / ".git").is_dir(),
                  "explicit enrolled Git root required")
    for name in ("info/grafts", "objects/info/alternates", "objects/info/http-alternates", "shallow"):
        _1174_require(not os.path.lexists(root / ".git" / name), "untrusted Git view: " + name)
    _1174_require(_git_do(root, "for-each-ref", "--format=%(refname)", "refs/replace/") == (0, b""),
                  "untrusted Git view: replace refs")
    _1174_require(_git_do(root, "rev-parse", "--is-shallow-repository") == (0, b"false\n"), "untrusted Git view: shallow")
    _1174_require(_git_do(root, "rev-parse", "--show-toplevel") == (0, os.fsencode(root) + b"\n"), "Git root identity")


@contextlib.contextmanager
def _1174_git_snapshot(root):
    _1174_git_view(root)
    rc, endpoint = _git_do(root, "remote", "get-url", "origin")
    _1174_require(rc == 0 and endpoint.strip() in (b"https://github.com/ducthangho/tra-luat.git",
                  b"https://github.com/ducthangho/tra-luat", b"git@github.com:ducthangho/tra-luat.git"), "canonical endpoint")
    with tempfile.TemporaryDirectory(prefix="wp1174-facts-") as temporary:
        snapshot = Path(temporary) / "repo"
        child = subprocess.run(["git", "--no-replace-objects", "clone", "--quiet", "--no-hardlinks", "--no-checkout",
                                endpoint.decode().strip(), str(snapshot)], env=_1174_git_env(), capture_output=True, timeout=120)
        _1174_require(child.returncode == 0, "canonical snapshot unavailable")
        _1174_git_view(snapshot)
        yield snapshot


def _1174_rollout(root):
    rc, raw = _git_do(root, "show", "refs/remotes/origin/master:.claude/dev/packet_loop.py")
    _1174_require(rc == 0 and raw == Path(__file__).read_bytes(), "consumer not current landed canonical code")


@_1174_scoped
def _1174_resolve(root, packet, revision, generation, admission_file, identities=None):
    with _1174_git_snapshot(root) as snapshot:
        _1174_rollout(snapshot)
        admission, facts = _1174_resolve_snapshot(snapshot, packet, revision, generation, admission_file, identities)
        _1174_require(admission["enrollment"]["git_root"] == str(root), "enrolled Git root identity")
        if _1174_same_family(admission["enrollment"]["initial_state_projection"]):
            _1174_policy_head(root, facts["owner_policy"])
        return admission, facts


def _1174_same_family(state):
    return (state["executor"] == state["reviewer"] or
            state["executor_identity"]["model_family"] == state["reviewer_identity"]["model_family"])


def _1174_owner_policy(root, admission, lease, spec_sha256, comments):
    """Resolve an immutable policy through the verified lease and owner API fact.

    Context/profile records are owner-audited platform evidence, not measured
    serving-model identity. Neither FILE nor a caller boolean can supply them.
    """
    descriptor = lease.get("owner_review_policy")
    _1174_require(type(descriptor) is dict and set(descriptor) == {"ref", "path", "sha256", "decision_id"},
                  "owner-scoped policy descriptor required")
    ref, sep, oid = descriptor["ref"].partition("@") if type(descriptor.get("ref")) is str else ("", "", "")
    _1174_require(sep == "@" and SHA_RE.fullmatch(oid) and _git_do(root, "check-ref-format", ref)[0] == 0 and
        type(descriptor["path"]) is str and not PurePosixPath(descriptor["path"]).is_absolute() and
        ".." not in PurePosixPath(descriptor["path"]).parts and _1174_hash(descriptor["sha256"]) and
        type(descriptor["decision_id"]) is int and descriptor["decision_id"] > 0, "owner-scoped policy descriptor")
    rc, raw = _git_do(root, "show", oid + ":" + descriptor["path"])
    _1174_require(rc == 0 and hashlib.sha256(raw).hexdigest() == descriptor["sha256"], "owner-scoped policy immutable bytes")
    policy = _1174_json(raw)
    keys = {"schema", "policy_id", "owner", "packet", "mission", "revision", "generation", "spec_ref", "spec_sha256",
            "lease_id", "expires_utc", "comparison", "source", "reviewer", "head", "tree", "assurance"}
    _1174_require(type(policy) is dict and set(policy) == keys and policy["schema"] == "wp1174_owner_review_policy.v1" and
        policy["policy_id"] == "WP1174-E2-R21-CODEX-PAIR" and policy["owner"] == CHU_KHO and
        all(type(policy[k]) is int and policy[k] == admission[k] == v for k, v in
            (("packet", 1174), ("mission", 1172), ("revision", 21), ("generation", 18))) and
        policy["spec_ref"] == lease["spec_ref"] and policy["spec_sha256"] == spec_sha256 == lease["spec_hash"] ==
            "0e5b03b860a778d9b59ae4290b00ed205c8d690cf7e083037ea8634d7336a33b" and
        policy["lease_id"] == lease["lease_id"] == "wp1174-r21-g18-codex" and policy["assurance"] == "same_provider_approved" and
        policy["comparison"] == "same_model_configured_effort_v1", "owner-scoped policy scope/spec/lease")
    now = datetime.now(timezone.utc)
    _1174_require(now < _1174_time(policy["expires_utc"]) <= _1174_time(lease["lease_expires_at_utc"]) and
        _1174_time(policy["expires_utc"]) <= min(_1174_time(admission["expires_utc"]),
            _1174_time("2026-11-09T14:20:32+00:00")), "owner-scoped policy expired")
    decisions = [c for c in comments if type(c) is dict and c.get("id") == descriptor["decision_id"]]
    _1174_require(len(decisions) == 1, "owner-scoped policy decision missing")
    decision = decisions[0]
    _1174_require(decision.get("user", {}).get("login") == CHU_KHO and decision.get("user", {}).get("type") == "User" and
        decision.get("author_association") == "OWNER" and
        decision.get("issue_url") == f"https://api.github.com/repos/{_1174_REPO}/issues/1174" and
        decision.get("html_url") == f"https://github.com/{_1174_REPO}/issues/1174#issuecomment-{descriptor['decision_id']}" and
        decision.get("body") == "WP1174_OWNER_POLICY_V1 sha256:" + descriptor["sha256"], "owner-scoped policy owner decision")
    context_keys = {"context_id", "parent_context_id", "checkout_id", "read_only", "provider", "model_family",
                    "execution_surface", "transport", "configured_model", "configured_effort", "evidence_id"}
    source, reviewer = policy["source"], policy["reviewer"]
    for role, context in (("executor", source), ("reviewer", reviewer)):
        _1174_require(type(context) is dict and set(context) == context_keys and
            all(type(context[k]) is str and bool(context[k].strip()) for k in context_keys - {"parent_context_id", "read_only"}) and
            context["parent_context_id"] is None and type(context["read_only"]) is bool and
            context["provider"] == "codex" and context["model_family"] == "openai" and
            context["execution_surface"] == "codex_service" and context["transport"] == "machine" and
            {k: context[k] for k in ("provider", "model_family", "execution_surface", "transport")} ==
                admission["enrollment"]["initial_state_projection"][role + "_identity"], "owner-scoped policy context identity")
    _1174_require(source["context_id"] != reviewer["context_id"] and source["checkout_id"] != reviewer["checkout_id"] and
        source["evidence_id"] != reviewer["evidence_id"] and reviewer["read_only"] is True and
        source["configured_model"] == reviewer["configured_model"] and
        source["configured_effort"] == "medium" and reviewer["configured_effort"] == "high", "owner-scoped policy independent stronger reviewer")
    _1174_require(type(policy["head"]) is str and SHA_RE.fullmatch(policy["head"]) and
        type(policy["tree"]) is str and SHA_RE.fullmatch(policy["tree"]), "owner-scoped policy H/tree")
    return dict(policy=policy, sha256=descriptor["sha256"])


def _1174_policy_head(root, authority, head=None):
    policy = authority["policy"]
    rc, actual = _git_do(root, "rev-parse", "HEAD")
    tc, tree = _git_do(root, "rev-parse", policy["head"] + "^{tree}")
    _1174_require(rc == tc == 0 and actual.decode().strip() == policy["head"] and
        tree.decode().strip() == policy["tree"] and (head is None or head == policy["head"]), "owner-scoped policy stale H/tree")


def _1174_i2_identity(pinned, identities):
    keys = ("executor_identity", "reviewer_identity")
    if identities is not None:
        _1174_require(all(identities[k] == pinned[k] for k in keys), "journal/grant I2 identity mismatch")
        return {k: identities[k] for k in keys}
    return {k: pinned[k] for k in keys}


@_1174_scoped
def _1174_resolve_snapshot(root, packet, revision, generation, admission_file, identities=None):
    """Discover the existing canonical lease/spec chain; FILE is only a byte copy.

    There is no separate enrollment registry. A Packet with no admitted descriptor
    in its current immutable spec remains blocked, including the source WP1174 lease.
    """
    root = Path(root)
    rc, endpoint = _git_do(root, "remote", "get-url", "origin")
    _1174_require(rc == 0 and endpoint.strip() in (b"https://github.com/ducthangho/tra-luat.git",
                  b"https://github.com/ducthangho/tra-luat", b"git@github.com:ducthangho/tra-luat.git"), "canonical endpoint")
    _1174_require(_git_do(root, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")[0] == 0, "canonical fetch")
    rc, remote = _git_do(root, "ls-remote", "origin", "refs/heads/master")
    lc, local = _git_do(root, "rev-parse", "refs/remotes/origin/master")
    _1174_require(rc == lc == 0 and remote.split() == [local.strip(), b"refs/heads/master"], "current canonical ref")
    with _canon(root) as canonical:
        lp = _nap(canonical, "lease_publish")
        repo = _1174_api(f"repos/{_1174_REPO}",root=root,deadline=time.time()+120)
        _1174_require(type(repo) is dict and repo.get("full_name") == _1174_REPO and repo.get("default_branch") == "master",
                      "canonical GitHub identity")
        permission = _1174_api(f"repos/{_1174_REPO}/collaborators/{CHU_KHO}/permission",root=root,deadline=time.time()+120)
        _1174_require(type(permission) is dict and permission.get("permission") in ("admin", "maintain") and
                      permission.get("user", {}).get("login") == CHU_KHO, "owner maintain permission")
        comments = _1174_comments(packet, root)
        all_leases = lp._quet_lease_toan_kho(root, chan_nhanh_tut_sau=True)
        _1174_require(type(all_leases) is list and all(type(row) is dict and type(row.get("lease")) is dict
                      for row in all_leases), "canonical lease collection")
        registered = [row for row in all_leases if all(type(row["lease"].get(k)) is int and row["lease"][k] == v
            for k, v in (("packet_issue", packet), ("revision", revision), ("generation", generation))) and
            lp._phan_loai_lease(row["lease"]) == "CÒN_HẠN" and lp._bia_mo_doi_xung(row["lease"], all_leases) is None]
        _1174_require(len(registered) == 1, "no unique current canonical Packet lease/spec")
        row, now = registered[0], datetime.now(timezone.utc)
        lease_rc, lease_oid_raw = _git_do(root, "rev-parse", row["ref"])
        lease_oid = lease_oid_raw.decode().strip()
        _1174_require(lease_rc == 0 and SHA_RE.fullmatch(lease_oid), "canonical lease ref OID")
        lease = row["lease"]
        _1174_require(type(lease.get("spec_ref")) is str and "@" in lease["spec_ref"], "canonical immutable spec required")
        spec_oid = lease["spec_ref"].rsplit("@", 1)[1]
        spec = _spec_merge(root, spec_oid, lease.get("spec_path"), lease)
        visible, errors = _che_khong_render(spec.decode("utf-8"))
        _1174_require(not errors, "canonical spec render")
        descriptor = {}
        for key in ("ref", "path", "sha256"):
            values = re.findall(rf"(?m)^admission_{key}: ([^\s]+)$", visible)
            _1174_require(len(values) == 1, "no unique admission descriptor in canonical spec")
            descriptor["admission_" + key] = values[0]
        ref, separator, oid = descriptor["admission_ref"].partition("@")
        _1174_require(separator == "@" and SHA_RE.fullmatch(oid) and _git_do(root, "check-ref-format", ref)[0] == 0,
                      "admission immutable ref")
        rc, raw = _git_do(root, "show", f"{oid}:{descriptor['admission_path']}")
        _1174_require(rc == 0 and hashlib.sha256(raw).hexdigest() == descriptor["admission_sha256"], "immutable descriptor blob/hash")
        payload = _1174_json(raw)
        _1174_require(type(payload) is dict and type(payload.get("enrollment")) is dict, "admission payload identity")
        registration = dict(schema="wp1174_registration.v1", **{k: payload.get(k) for k in
            ("mission", "mission_revision", "mission_plan_sha256", "packet", "revision", "generation")},
            spec_ref=lease["spec_ref"], spec_path=lease["spec_path"], spec_sha256=lease["spec_hash"], **descriptor,
            enrollment_id=payload["enrollment"].get("id"), binding_sha256=payload["enrollment"].get("binding_sha256"),
            expires_utc=lease.get("lease_expires_at_utc"), revoked=False)
        # The closed intermediate below is derived from the verified spec graph,
        # never accepted as a caller-provided registration or a new trust root.
        _1174_registration(registration, packet, revision, generation, now)
        _1174_require(Path(admission_file).read_bytes() == raw, "FILE differs from immutable admission")
        admission = _1174_admission(raw, registration, now)
        _1174_require(re.findall(r"\bcontract_id: ([A-Za-z0-9_.-]+)", visible) == [admission["contract_id"]] and
                      re.findall(r"\bmission_plan_sha256: ([0-9a-f]{64})", visible) == [admission["mission_plan_sha256"]],
                      "spec contract/Mission binding")
        baseline = re.findall(r"(?m)^(?:- )?immutable_acceptance_baseline: ([0-9a-f]{40})$", visible)
        _1174_require(baseline == [admission["base"]], "spec baseline binding")
        # I2 is a verifier here: it neither fabricates a journal nor commits a lease.
        with tempfile.TemporaryDirectory(prefix="wp1174-authority-") as td:
            directory = Path(td).resolve()
            readback = directory / "comments.json"
            readback.write_bytes(_1174_bytes(comments))
            pinned = admission["enrollment"]["initial_state_projection"]
            st = dict(packet=packet, **_1174_i2_identity(pinned, identities))
            remote_ref = re.sub(r"^refs/(?:remotes/origin|heads)/", "", row["ref"])
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    verified = _verify_lease_ref(argparse.Namespace(root=str(root), lease_ref="origin/" + remote_ref,
                        lease_path=row["path"], lease_comments=str(readback)), st)
                _1174_require(type(verified) is dict and verified["lease"]["lease_id"] == lease["lease_id"] and
                    verified["context"]["lease_oid"] == lease_oid, "canonical lease verification")
            except SystemExit as ex:
                raise ValueError("WP1174 UNKNOWN: canonical I2 verification rc=" + str(ex.code)) from ex
        _, installed_id = _1174_installed_mission(_1174_comments(1172, root), admission, now)
        return admission, dict(canonical_oid=local.decode().strip(), spec_sha256=registration["spec_sha256"],
                               admission_sha256=registration["admission_sha256"], mission_install_id=installed_id,
                               lease_id=lease["lease_id"], lease=lease, spec=spec, verified_i2=verified,
                               lease_oid=lease_oid,
                               lease_ref="origin/" + remote_ref, lease_path=row["path"], comments=comments,
                               owner_policy=(_1174_owner_policy(root, admission, lease, registration["spec_sha256"], comments)
                                   if _1174_same_family(pinned) else None))


_1174_MUTATORS = ("init", "record-lease", "begin-attempt", "void-attempt", "record-review", "transition",
    "record-codex-call", "nang-tran", "record-rescue", "record-post", "accept", "mo-lai", "chu-kho-duyet", "adopt-state")
_1174_IMPLEMENTATION_COMPLETE = True
_1174_OWNER_POLICY = contextvars.ContextVar("wp1174_owner_policy", default=None)

_1174_CORE = frozenset("schema_version review_rounds_used codex_review_calls_used codex_calls nang_tran review_rounds_limit codex_review_calls_limit packet mission executor reviewer executor_identity reviewer_identity state lease attempts_used attempts_limit same_failure_limit finding_counts attempt_open attempt_anchor hmac_key reviewing_head_sha accepted_sha reviews posts history state_revision generation enrollment_id binding_sha256 adoption scoped_review human_acceptance".split())
_1174_OPTIONAL = {"luat_adr0054": bool, "ngu_canh_lease": dict, "dem_tu_suy": bool,
    "ly_do": str, "truc": str, "pending_sha": str, "bien_nhan_approve": dict,
    "mo_lai_tu": dict, "checkpoint_day": dict, "moc_connector": dict, "quyet_dinh_p3": list}
_1174_OPTIONAL_WRITES = {"record-lease": {"luat_adr0054", "ngu_canh_lease"},
    "record-rescue": {"ly_do", "truc"}, "record-review": {"pending_sha", "bien_nhan_approve", "ly_do", "truc"},
    "record-codex-call": {"ly_do", "truc"}, "begin-attempt": {"ly_do", "truc"},
    "accept": {"moc_connector", "quyet_dinh_p3"}, "mo-lai": {"mo_lai_tu"},
    "chu-kho-duyet": {"checkpoint_day", "mo_lai_tu"}}
_1174_CORE_WRITES = {"record-lease": {"lease", "state", "history"},
    "begin-attempt": {"attempts_used", "state", "attempt_open", "reviewing_head_sha", "attempt_anchor", "history"},
    "void-attempt": {"attempts_used", "attempt_open", "attempt_anchor", "state", "reviewing_head_sha", "history"},
    "record-review": {"scoped_review", "human_acceptance", "attempt_open", "review_rounds_used", "codex_calls", "reviews", "finding_counts", "state", "accepted_sha", "history"},
    "transition": {"state", "reviewing_head_sha", "posts", "history"},
    "record-codex-call": {"codex_review_calls_used", "codex_calls", "state", "history"},
    "nang-tran": {"attempts_limit", "review_rounds_limit", "codex_review_calls_limit", "nang_tran"},
    "record-rescue": {"state", "history"}, "record-post": {"posts"},
    "accept": {"human_acceptance", "state", "accepted_sha", "history"},
    "mo-lai": {"state", "attempt_open", "reviewing_head_sha", "finding_counts", "history"},
    "chu-kho-duyet": {"state", "history"}}


def _1174_derive_key(seed, enrollment_id, binding_sha256, packet, g0):
    _1174_require(type(seed) is bytes and len(seed) == 32, "private seed length")
    info = _1174_bytes(dict(enrollment_id=enrollment_id, binding_sha256=binding_sha256, packet=packet, g0=g0))
    prk = hmac.new(b"tra-luat/WP1174/v3-hmac-key/HKDF-SHA256/v1", seed, hashlib.sha256).digest()
    return hmac.new(prk, info + b"\x01", hashlib.sha256).hexdigest()


def _1174_seed(e):
    import stat
    path = Path(e["private_seed_path"])
    try:
        before = path.lstat()
        _1174_require(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode) == 0o600 and
                      before.st_uid == os.geteuid() and before.st_nlink == 1, "private seed ownership/mode/nlink")
        raw = _1174_read(path)
        after = path.lstat()
        _1174_require((before.st_dev, before.st_ino, before.st_mode, before.st_nlink, before.st_uid) ==
                      (after.st_dev, after.st_ino, after.st_mode, after.st_nlink, after.st_uid), "private seed metadata drift")
        _1174_require(len(raw) == 32 and hashlib.sha256(raw).hexdigest() == e["private_seed_sha256"], "private seed fingerprint")
        return raw

    except OSError as ex:
        raise ValueError("WP1174 UNKNOWN: private seed read/lstat") from ex


def _1174_initial(admission):
    e, p = admission["enrollment"], admission["enrollment"]["initial_state_projection"]
    # The keyset and defaults come from canonical code, never from the public projection.
    _1174_require(set(p) == _1174_CORE - {"hmac_key"}, "initial projection keyset")
    defaults = dict(schema_version=3, review_rounds_used=0, codex_review_calls_used=0, codex_calls=[], nang_tran=[],
        packet=admission["packet"], mission=admission["mission"], state="awaiting_lease", lease=None,
        attempts_used=0, finding_counts={}, attempt_open=False, attempt_anchor=None, reviewing_head_sha=None,
        accepted_sha=None, reviews=[], posts={}, history=[], state_revision=0, generation=e["g0"],
        enrollment_id=e["id"], binding_sha256=e["binding_sha256"], adoption=None, scoped_review=None, human_acceptance=None,
        **{k: admission["allowance"][k] for k in ("attempts_limit", "review_rounds_limit", "codex_review_calls_limit")})
    _1174_require(all(type(p[k]) is type(v) and p[k] == v for k, v in defaults.items()) and
                  type(p["same_failure_limit"]) is int and p["same_failure_limit"] > 0, "initial projection defaults/allowance")
    for role in ("executor", "reviewer"):
        ident = p[role + "_identity"]
        _1174_require(type(ident) is dict and set(ident) == {"provider", "model_family", "execution_surface", "transport"}
                      and ident == _identity(p[role], ident["model_family"], ident["execution_surface"], ident["transport"]),
                      "initial projection identity")
    _1174_require(not _1174_same_family(p) or _1174_OWNER_POLICY.get() is not None,
                  "initial owner-scoped same-family policy required")
    state = dict(p, hmac_key=_1174_derive_key(_1174_seed(e), e["id"], e["binding_sha256"], admission["packet"], e["g0"]))
    return _1174_bytes(_1174_state(_1174_bytes(state), admission))


def _1174_state(raw, admission, generation=None):
    """Validate the complete legacy payload as well as the v3 binding before use."""
    global _1174_TRANSACTION
    state = _1174_json(raw)
    e = admission["enrollment"]
    _1174_require(type(state) is dict and state.get("schema_version") == 3 and type(state["schema_version"]) is int and
        state.get("enrollment_id") == e["id"] and state.get("binding_sha256") == e["binding_sha256"] and
        type(state.get("generation")) is int and state["generation"] == (admission["generation"] if generation is None else generation) and
        _1174_int(state.get("state_revision")) and state.get("mission") == admission["mission"], "state v3 binding")
    _1174_require(_1174_CORE <= set(state) <= _1174_CORE | set(_1174_OPTIONAL), "state closed keyset")
    _1174_require(all(type(state[k]) is kind or k in ("mo_lai_tu", "checkpoint_day") and state[k] is None
                  for k, kind in _1174_OPTIONAL.items() if k in state), "state optional type/absence")
    _1174_require(_1174_hash(state["hmac_key"]), "state HMAC key")
    if state["adoption"] is not None:
        _1174_adoption_record(state["adoption"], admission)
    _1174_require(not _1174_same_family(state) or _1174_OWNER_POLICY.get() is not None, "state owner-scoped same-family policy required")
    _1174_lifecycle_records(state, admission)
    for role in ("executor", "reviewer"):
        _1174_require(state[role] == e["initial_state_projection"][role] and
                      state[role + "_identity"] == e["initial_state_projection"][role + "_identity"], "state immutable provider identity")
    previous = globals().get("_1174_TRANSACTION")
    directory = Path(e["journal_root"])
    _1174_TRANSACTION = dict(directory=directory, state=state, proposal=None, admission=admission)
    try:
        _load(directory, admission["packet"])
    except SystemExit as ex:
        raise ValueError("WP1174 UNKNOWN: full state validation rc=" + str(ex.code)) from ex
    finally:
        _1174_TRANSACTION = previous
    return state


def _1174_alive(admission):
    authority = _1174_OWNER_POLICY.get()
    if _1174_same_family(admission["enrollment"]["initial_state_projection"]):
        _1174_require(authority is not None and all(authority["policy"][k] == admission[k]
            for k in ("packet", "mission", "revision", "generation")), "owner-scoped policy active binding")
        _1174_require(datetime.now(timezone.utc) < _1174_time(authority["policy"]["expires_utc"]), "owner-scoped policy expired")
        _1174_policy_head(Path(admission["enrollment"]["git_root"]), authority)
    now=datetime.now(timezone.utc)
    _1174_require(now < _1174_time(admission["expires_utc"]) and
        _1174_time(admission["allowance"]["starts_utc"]) <= now < _1174_time(admission["allowance"]["ends_utc"]),"authority expired before publication/dispatch")


def _1174_runtime(a, admission):
    e, root = admission["enrollment"], Path(admission["enrollment"]["root"])
    _1174_require(str(root.resolve(strict=True)) == str(root) and root.is_dir(), "root canonical directory")
    observed = root.stat()
    _1174_require((observed.st_dev, observed.st_ino) == (e["root_device"], e["root_inode"]), "root identity")
    _1174_require(Path("/proc/sys/kernel/random/boot_id").read_text().strip() == e["boot_id"] and
                  a.coordinator_id == e["coordinator_id"], "boot/coordinator readmission")
    mount = _1174_mount(root)
    _1174_require(_1174_platform(platform.system(), mount["filesystem"], mount["magic"]) and all(
        mount[k] == e[v] for k, v in (("mount_id", "mount_id"), ("device", "mount_device"),
        ("filesystem", "filesystem"), ("magic", "magic"))), "enrolled native mount")
    _1174_require(str(Path(e["journal_root"]).resolve(strict=True)) == e["journal_root"], "journal root canonical")
    paths = [e[key] for key in ("state_path", "witness_path", "lock_path", "initial_state_path", "private_seed_path")]
    paths.extend(source for source in (admission["lineage"]["source_path"], e["legacy_source_path"]) if source is not None)
    for value in paths:
        path = Path(value)
        _1174_require(str(path.resolve(strict=False)) == str(path) and
                      _1174_mount(path.parent) == mount, "path topology drift")
    return mount


def _1174_pair(admission, witness, raw):
    e = admission["enrollment"]
    state = _1174_state(raw, admission)
    _1174_require(witness["phase"] == "initialized" and witness["active_generation"] == admission["generation"] and
        witness["pending_adoption"] is None and not witness["suspended"] and witness["high_water"] == dict(
        generation=state["generation"], state_revision=state["state_revision"], state_sha256=hashlib.sha256(raw).hexdigest()),
        "state/witness high_water mismatch")
    active = next((n["canonical_path"] for n in reversed(witness["history"]) if n["terminal_kind"] == "adopted"), e["initial_state_path"])
    _1174_require(e["state_path"] == active, "active target path")
    _1174_require(not witness["history"] or state["adoption"] is not None and state["adoption"]["phase"] == "adopted",
                  "active adoption phase")
    _1174_tripwire(state, e["g0"])
    return state


def _1174_commit_witness(before, after, admission, action):
    e = admission["enrollment"]
    raw = _1174_bytes(after)
    _1174_witness_transition(before, raw, e["id"], e["binding_sha256"], e["g0"], action)
    return raw


def _1174_write(path, raw, *, create):
    global _1174_IO_STARTED
    _1174_IO_STARTED = True
    _1174_persist(path, raw, create=create)


_1174_PAYLOAD_KEYS = frozenset(("source_snapshot", "source_sha256", "source_path", "predecessor_generation",
    "target_projection", "tombstone", "tombstone_sha256", "operation"))


def _1174_adoption_record(record, admission):
    _1174_require(type(record) is dict and set(record) == {"phase", "payload", "payload_sha256", "cutover_started"}
                  and type(record["phase"]) is str and record["phase"] in ("prepared", "adopted", "aborted")
                  and type(record["cutover_started"]) is bool, "adoption record schema")
    p = record["payload"]
    _1174_require(type(p) is dict and set(p) == _1174_PAYLOAD_KEYS and _1174_hash(record["payload_sha256"])
                  and hashlib.sha256(_1174_bytes(p)).hexdigest() == record["payload_sha256"], "adoption immutable payload hash/keyset")
    _1174_require(all(type(p[k]) is str for k in ("source_snapshot", "source_path", "tombstone")) and
                  type(p["target_projection"]) is dict and _1174_int(p["predecessor_generation"]), "adoption payload types")
    _1174_pending(p["operation"])
    _1174_require(p["operation"] == admission["operation"] and p["source_path"] == admission["lineage"]["source_path"] and
                  p["source_sha256"] == admission["lineage"]["source_sha256"] and
                  p["predecessor_generation"] == admission["lineage"]["predecessor_generation"] and
                  _1174_CORE - {"adoption"} <= set(p["target_projection"]) <=
                  (_1174_CORE - {"adoption"}) | set(_1174_OPTIONAL), "adoption immutable binding/projection")
    source, tombstone = p["source_snapshot"].encode("utf-8"), p["tombstone"].encode("utf-8")
    _1174_require(hashlib.sha256(source).hexdigest() == p["source_sha256"] == p["operation"]["source_sha256"] and
                  hashlib.sha256(tombstone).hexdigest() == p["tombstone_sha256"] and tombstone == _1174_tombstone(
                  admission["packet"], p["predecessor_generation"], p["operation"]["generation"],
                  p["operation"]["adoption_id"], p["source_sha256"], p["operation"]["binding_sha256"]), "adoption source/tombstone bytes")
    _1174_require(p == _1174_adopt_payload(admission, source), "adoption deterministic source projection")
    _1174_require(record["phase"] != "adopted" or record["cutover_started"], "adopted requires intent")
    _1174_require(record["phase"] != "aborted" or not record["cutover_started"], "aborted forbids intent")
    return record


def _1174_adopt_payload(admission, source):
    e, operation, lineage = admission["enrollment"], admission["operation"], admission["lineage"]
    st = json.loads(source.decode("utf-8"), object_pairs_hook=_cam_khoa_trung, parse_constant=_cam_hang_ngoai_json)
    _1174_require(type(st) is dict and st.get("schema_version") in (2, 3) and "hmac_key" in st, "adoption source schema")
    projection = dict(st, schema_version=3, generation=admission["generation"], state_revision=0,
        enrollment_id=e["id"], binding_sha256=e["binding_sha256"], adoption=None, scoped_review=None, human_acceptance=None)
    _1174_state(_1174_bytes(projection), admission)
    del projection["adoption"]
    tombstone = _1174_tombstone(admission["packet"], lineage["predecessor_generation"], operation["generation"],
                               operation["adoption_id"], operation["source_sha256"], operation["binding_sha256"])
    return dict(source_snapshot=source.decode("utf-8"), source_sha256=hashlib.sha256(source).hexdigest(),
        source_path=lineage["source_path"], predecessor_generation=lineage["predecessor_generation"], target_projection=projection,
        tombstone=tombstone.decode("utf-8"), tombstone_sha256=hashlib.sha256(tombstone).hexdigest(), operation=operation)


def _1174_adopt_image(payload, phase, intent, revision, admission):
    record = dict(phase=phase, payload=payload, payload_sha256=hashlib.sha256(_1174_bytes(payload)).hexdigest(), cutover_started=intent)
    image = dict(payload["target_projection"], state_revision=revision, adoption=record)
    raw = _1174_bytes(image)
    _1174_state(raw, admission)
    return raw


def _1174_tripwire(state, g0=None):
    """Validate the entire immutable predecessor chain and every live tombstone.

    The active record alone cannot fence a cached writer of an older generation.
    Never derive the expected retired bytes from the live predecessor file.
    """
    current, path, seen = state, None, set()
    identity = {k: state[k] for k in ("packet", "mission", "executor", "reviewer", "executor_identity", "reviewer_identity")}
    while current.get("adoption") is not None:
        record = current["adoption"]
        _1174_require(type(record) is dict and set(record) == {"phase", "payload", "payload_sha256", "cutover_started"}
            and record["phase"] == "adopted" and record["cutover_started"] is True, "retired lineage record")
        p = record["payload"]
        _1174_require(type(p) is dict and set(p) == _1174_PAYLOAD_KEYS and
            _1174_hash(record["payload_sha256"]) and hashlib.sha256(_1174_bytes(p)).hexdigest() == record["payload_sha256"],
            "retired lineage payload hash/keyset")
        _1174_pending(p["operation"])
        op = p["operation"]
        _1174_require(type(p["source_path"]) is str and Path(p["source_path"]).is_absolute() and
            str(Path(p["source_path"])) == p["source_path"] and p["source_path"] not in seen and
            _1174_int(p["predecessor_generation"]) and _1174_int(current.get("generation")) and
            p["predecessor_generation"] < current["generation"] == op["generation"] and
            (path is None or op["canonical_path"] == path), "retired lineage path/generation/operation")
        seen.add(p["source_path"])
        _1174_require(type(p["source_snapshot"]) is str and type(p["tombstone"]) is str and
            hashlib.sha256(p["source_snapshot"].encode("utf-8")).hexdigest() == p["source_sha256"] == op["source_sha256"] and
            hashlib.sha256(p["tombstone"].encode("utf-8")).hexdigest() == p["tombstone_sha256"] and
            p["tombstone"].encode("utf-8") == _1174_tombstone(state["packet"], p["predecessor_generation"], op["generation"],
                op["adoption_id"], p["source_sha256"], op["binding_sha256"]), "retired lineage snapshot/tombstone binding")
        source_raw = p["source_snapshot"].encode("utf-8")
        predecessor = json.loads(source_raw, object_pairs_hook=_cam_khoa_trung, parse_constant=_cam_hang_ngoai_json)
        _1174_require(type(predecessor) is dict and type(predecessor.get("schema_version")) is int and
            predecessor["schema_version"] in (2, 3) and all(predecessor.get(k) == v for k, v in identity.items()),
            "retired lineage source identity/schema")
        if predecessor["schema_version"] == 3:
            _1174_require(_1174_bytes(predecessor) == source_raw and
                _1174_CORE <= set(predecessor) <= _1174_CORE | set(_1174_OPTIONAL) and
                predecessor["generation"] == p["predecessor_generation"] and _1174_int(predecessor["generation"]) and
                _1174_int(predecessor["state_revision"]) and predecessor["enrollment_id"] == state["enrollment_id"] and
                predecessor["binding_sha256"] == state["binding_sha256"], "retired lineage v3 binding")
        projection = dict(predecessor, schema_version=3, generation=current["generation"], state_revision=0,
            enrollment_id=state["enrollment_id"], binding_sha256=state["binding_sha256"], scoped_review=None, human_acceptance=None)
        projection.pop("adoption", None)
        _1174_require(p["target_projection"] == projection, "retired lineage deterministic projection")
        _1174_require(_1174_read(Path(p["source_path"])) == p["tombstone"].encode("utf-8"), "legacy_changed")
        current, path = predecessor, p["source_path"]
    if g0 is not None and current.get("schema_version") == 3:
        _1174_require(current.get("generation") == g0, "retired lineage genesis generation")


def _1174_adopt(a, admission, witness_raw):
    _1174_alive(admission)
    e, op, lineage = admission["enrollment"], admission["operation"], admission["lineage"]
    _1174_require(op is not None and lineage["predecessor_generation"] is not None and
                  a.adoption_id == op["adoption_id"] and e["quiescent"] and bool(e["producer_handoffs"]), "adoption authority/quiescence")
    target, source, wp = Path(e["state_path"]), Path(lineage["source_path"]), Path(e["witness_path"])
    witness = _1174_witness(witness_raw, e["id"], e["binding_sha256"], e["g0"]) if witness_raw is not None else None
    _1174_require(a.expected_witness_revision == (str(witness["witness_revision"]) if witness else "absent"), "revision_rejected")
    exists = os.path.lexists(target)
    target_raw = _1174_read(target) if exists else None
    pending = witness["pending_adoption"] if witness else None
    terminal = next((n for n in witness["history"] if n["adoption_id"] == op["adoption_id"]), None) if witness else None
    if a.mode == "initial":
        _1174_require(a.expected_source_sha256 == op["source_sha256"] and a.target_generation == op["generation"] and
                      pending is None and terminal is None and not exists, "initial adoption target/pending/history")
        source_raw = _1174_read(source)
        _1174_source_binding(witness, admission, str(source), source_raw)
        payload = _1174_adopt_payload(admission, source_raw)
    else:
        _1174_require(a.adoption_id == op["adoption_id"] and witness is not None, "recovery operation identity")
        if pending is None:
            _1174_require(terminal is not None and all(terminal[k] == op[k] for k in
                ("adoption_id", "binding_sha256", "generation", "canonical_path")) and
                terminal["terminal_disposition"] == a.disposition, "terminal replay disposition/identity")
            _1174_require(terminal == witness["history"][-1], "terminal replay lineage advanced")
            if terminal["terminal_kind"] == "aborted_intent":
                _1174_require(not exists and _1174_read(source) and
                    hashlib.sha256(_1174_read(source)).hexdigest() == lineage["source_sha256"], "terminal absent/source")
            else:
                _1174_require(exists and hashlib.sha256(target_raw).hexdigest() == terminal["as_of_sha256"] or
                    terminal["terminal_kind"] == "adopted" and exists, "terminal target hash")
                st = _1174_state(target_raw, admission)
                _1174_tripwire(json.loads(st["adoption"]["payload"]["source_snapshot"], object_pairs_hook=_cam_khoa_trung, parse_constant=_cam_hang_ngoai_json))
                if terminal["terminal_kind"] == "adopted":
                    _1174_pair(admission, witness, target_raw)
                    _1174_tripwire(st)
            _1174_recheck_durable(source, _1174_read(source))
            if exists:
                _1174_recheck_durable(target, target_raw)
            _1174_recheck_durable(wp, witness_raw)
            _1174_alive(admission)
            return "already_completed_no_dispatch"
        _1174_pending(pending, dict(op, cutover_started=pending["cutover_started"]))
        if target_raw is None:
            _1174_require(not pending["cutover_started"], "missing target after cutover intent")
            source_raw = _1174_read(source)
            _1174_require(hashlib.sha256(source_raw).hexdigest() == lineage["source_sha256"], "recovery source hash")
            payload = _1174_adopt_payload(admission, source_raw)
        else:
            st = _1174_state(target_raw, admission)
            record = _1174_adoption_record(st["adoption"], admission)
            payload = record["payload"]
            _1174_require(payload == _1174_adopt_payload(admission, payload["source_snapshot"].encode("utf-8")),
                          "recovery immutable source projection")
            _1174_require(target_raw == _1174_adopt_image(payload, record["phase"], record["cutover_started"],
                {("prepared", False): 0, ("prepared", True): 1, ("adopted", True): 2, ("aborted", False): 1}.get(
                (record["phase"], record["cutover_started"]), -1), admission), "recovery exact target image")
        _1174_source_binding(witness, admission, payload["source_path"],
                             payload["source_snapshot"].encode("utf-8"), recovery=True)
    images = {key: _1174_adopt_image(payload, phase, intent, revision, admission) for key, phase, intent, revision in
              (("prepared", "prepared", False, 0), ("intent", "prepared", True, 1), ("adopted", "adopted", True, 2), ("aborted", "aborted", False, 1))}
    old_source, retired = payload["source_snapshot"].encode("utf-8"), payload["tombstone"].encode("utf-8")
    source_now = _1174_read(source)
    _1174_require(source_now in (old_source, retired), "source changed before recovery")
    disposition = "resume_forward" if a.mode == "initial" else a.disposition
    if disposition != "resume_forward":
        _1174_require(pending is not None and not pending["cutover_started"] and source_now == old_source and
            ((disposition == "abandon_before_prepare" and not exists) or (disposition == "abandon_before_cutover" and
             target_raw in (images["prepared"], images["aborted"]))), "abandon phase/intent")
        kind = "aborted_intent" if not exists else "aborted"
        final_raw = None if not exists else images["aborted"]
        action = disposition
    else:
        _1174_require(target_raw is None or target_raw in (images["prepared"], images["intent"], images["adopted"]), "resume phase")
        _1174_require(source_now == old_source or pending is not None and pending["cutover_started"] and
                      target_raw in (images["intent"], images["adopted"]), "tombstone requires durable intent")
        kind, final_raw, action = "adopted", images["adopted"], "adopt_finalize"
    # Prevalidate every proposed image/transition before the first persistent write.
    chain = []
    current_raw = witness_raw
    current = witness
    if pending is None:
        if current is None:
            current = dict(_1174_reserved(e["id"], e["binding_sha256"], e["g0"]), origin="imported_lineage", pending_adoption=op)
            step = "imported_enrollment"
        else:
            current = dict(current, witness_revision=current["witness_revision"] + 1, pending_adoption=op)
            step = "adopt_pending"
        next_raw = _1174_commit_witness(current_raw, current, admission, step)
        chain.append((next_raw, current_raw is None))
        current_raw = next_raw
    if disposition == "resume_forward" and not current["pending_adoption"]["cutover_started"]:
        current = dict(current, witness_revision=current["witness_revision"] + 1, pending_adoption=dict(op, cutover_started=True))
        next_raw = _1174_commit_witness(current_raw, current, admission, "cutover_intent")
        intent_raw = next_raw
        current_raw = next_raw
    else:
        intent_raw = None
    node = dict(terminal_kind=kind, **{k: op[k] for k in ("adoption_id", "binding_sha256", "generation", "canonical_path")},
        as_of_revision=None if final_raw is None else (2 if kind == "adopted" else 1),
        as_of_sha256=None if final_raw is None else hashlib.sha256(final_raw).hexdigest(), terminal_disposition=disposition)
    final = dict(current, witness_revision=current["witness_revision"] + 1, pending_adoption=None,
                 history=[*current["history"], node], suspended=kind != "adopted")
    if kind == "adopted":
        final.update(phase="initialized", active_generation=op["generation"], high_water=dict(generation=op["generation"],
                     state_revision=2, state_sha256=node["as_of_sha256"]))
    final_witness = _1174_commit_witness(current_raw, final, admission, action)
    if a.mode == "recovery":
        _1174_recheck_durable(source, source_now)
        if target_raw is not None:
            _1174_recheck_durable(target, target_raw)
        _1174_recheck_durable(wp, witness_raw)
    _1174_probe(Path(e["root"]))
    _1174_alive(admission)
    for raw, create in chain:
        _1174_write(wp, raw, create=create)
    if disposition == "resume_forward":
        if not exists:
            _1174_write(target, images["prepared"], create=True)
            target_raw = images["prepared"]
        if intent_raw is not None:
            _1174_write(wp, intent_raw, create=False)
        if target_raw == images["prepared"]:
            _1174_write(target, images["intent"], create=False)
        if source_now == old_source:
            _1174_write(source, retired, create=False)
        else:
            # A prior process may have died after replacing the source but
            # before its directory fsync completed.  Readable tombstone bytes
            # alone do not prove that rename durable; re-establish the barrier
            # before publishing the terminal witness.
            _1174_fsyncdir(source.parent)
        if target_raw != images["adopted"]:
            _1174_write(target, images["adopted"], create=False)
    elif final_raw is not None and target_raw != final_raw:
        _1174_write(target, final_raw, create=False)
    if kind == "adopted":
        _1174_tripwire(_1174_json(final_raw))
    _1174_write(wp, final_witness, create=False)
    _1174_require(_1174_read(wp) == final_witness and (final_raw is None or _1174_read(target) == final_raw), "adoption final readback")
    _1174_alive(admission)
    return "completed_no_dispatch"


def _1174_initialize(a, admission, witness_raw):
    _1174_alive(admission)
    e = admission["enrollment"]
    _1174_require(admission["lineage"] == dict(predecessor_generation=None, source_path=None, source_sha256=None) and
                  admission["operation"] is None and e["origin"] == "fresh_init", "init predecessor/history")
    target, witness_path = Path(e["state_path"]), Path(e["witness_path"])
    initial = _1174_initial(admission)
    state = _1174_state(initial, admission)
    _1174_require(state["state"] == "awaiting_lease" and state["state_revision"] == 0 and state["generation"] == e["g0"] and
                  state["lease"] is None and not state["attempt_open"] and state["history"] == [], "granted initial image")
    _1174_require(a.mission == admission["mission"] and all(state[k] == admission["allowance"][k] for k in
                  ("attempts_limit", "review_rounds_limit", "codex_review_calls_limit")), "init granted allowance/Mission")
    for role in ("executor", "reviewer"):
        identity = _identity(getattr(a, role), getattr(a, role + "_model_family"),
                             getattr(a, role + "_execution_surface"), getattr(a, role + "_transport"))
        _1174_require(identity == state[role + "_identity"] and state[role] == getattr(a, role), "init granted provider identity")
    reserved = _1174_reserved(e["id"], e["binding_sha256"], e["g0"])
    reserved_raw = _1174_bytes(reserved)
    exists = os.path.lexists(target)
    if a.mode == "fresh":
        _1174_require(a.expected_revision == "absent" and a.expected_witness_revision is None and
                      witness_raw is None and not exists, "fresh init absence/revision")
    else:
        if witness_raw is not None:
            observed = _1174_witness(witness_raw, e["id"], e["binding_sha256"], e["g0"])
            _1174_require(a.expected_witness_revision == str(observed["witness_revision"]), "revision_rejected")
        _1174_require(a.expected_revision is None and witness_raw == reserved_raw and
                      (not exists or _1174_read(target) == initial), "resume-init exact reserved/full target")
    final = dict(reserved, phase="initialized", witness_revision=1, high_water=dict(generation=e["g0"],
        state_revision=0, state_sha256=hashlib.sha256(initial).hexdigest()))
    first = _1174_commit_witness(None, reserved, admission, "fresh_enrollment")
    last = _1174_commit_witness(reserved_raw, final, admission, "resume_init")
    if witness_raw is not None:
        _1174_recheck_durable(witness_path, witness_raw)
    if exists:
        _1174_recheck_durable(target, initial)
    _1174_probe(Path(e["root"]))
    _1174_alive(admission)
    if witness_raw is None:
        _1174_write(witness_path, first, create=True)
    if not exists:
        _1174_write(target, initial, create=True)
    _1174_write(witness_path, last, create=False)
    _1174_pair(admission, _1174_witness(_1174_read(witness_path), e["id"], e["binding_sha256"], e["g0"]), _1174_read(target))
    _1174_alive(admission)
    return "completed_no_dispatch"


@_1174_scoped
def _1174_ordinary(a, directory, admission, witness_raw, facts=None):
    global _1174_TRANSACTION
    _1174_alive(admission)
    e = admission["enrollment"]
    _1174_require(witness_raw is not None and a.expected_witness_revision is None and
                  type(a.expected_revision) is str and re.fullmatch(r"0|[1-9][0-9]*", a.expected_revision), "ordinary revision namespace")
    witness = _1174_witness(witness_raw, e["id"], e["binding_sha256"], e["g0"])
    state = _1174_pair(admission, witness, _1174_read(Path(e["state_path"])))
    _1174_require(state["state_revision"] == int(a.expected_revision), "revision_rejected")
    # The legacy reducer runs only after the scoped pair and tripwire checks;
    # review and accept add their scoped evidence before any durable write.
    _1174_tripwire(state)
    _1174_require(a.cmd != "record-lease" or a.lease_ref is not None, "scoped lease requires canonical I2")
    previous = globals().get("_1174_TRANSACTION")
    tx = dict(directory=directory, state=state, proposal=None, admission=admission)
    _1174_TRANSACTION = tx
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                rc = (_1174_review(a, directory, admission) if a.cmd == "record-review" else
                      _1174_accept(a, directory, admission) if a.cmd == "accept" else
                      _1174_record_lease(a, directory, state, admission, facts) if a.cmd == "record-lease" else a.fn(a, directory))
            except SystemExit as ex:
                rc = ex.code
        _1174_require(type(rc) is int and rc in (0, 3) and tx["proposal"] is not None, "legacy predicate rejected")
        new = tx["proposal"]
        new.update(schema_version=3, state_revision=state["state_revision"] + 1)
        raw = _1174_bytes(new)
        _1174_postimage(state, new, a.cmd, admission)
        after = dict(witness, witness_revision=witness["witness_revision"] + 1, high_water=dict(
            generation=admission["generation"], state_revision=new["state_revision"], state_sha256=hashlib.sha256(raw).hexdigest()))
        water = _1174_commit_witness(witness_raw, after, admission, "ordinary")
        _1174_require(_1174_read(Path(e["witness_path"])) == witness_raw, "witness changed during preflight")
        if state["adoption"] is not None:
            payload = state["adoption"]["payload"]
            _1174_recheck_durable(Path(payload["source_path"]), payload["tombstone"].encode("utf-8"))
        _1174_recheck_durable(Path(e["state_path"]), _1174_bytes(state))
        _1174_recheck_durable(Path(e["witness_path"]), witness_raw)
        _1174_probe(directory)
        _1174_alive(admission)
        _1174_write(Path(e["state_path"]), raw, create=False)
        _1174_write(Path(e["witness_path"]), water, create=False)
        _1174_pair(admission, _1174_witness(_1174_read(Path(e["witness_path"])), e["id"], e["binding_sha256"], e["g0"]),
                      _1174_read(Path(e["state_path"])))
        _1174_tripwire(new)
        _1174_alive(admission)
        return "quota_exhausted" if rc == 3 else "reserved_for_dispatch" if a.cmd in ("begin-attempt", "record-codex-call") else "completed_no_dispatch"
    finally:
        _1174_TRANSACTION = previous


def _1174_record_lease(a, directory, state, admission, facts):
    state = _load(directory, a.packet)
    _1174_require(type(facts) is dict and "verified_i2" in facts, "scoped lease authority missing")
    verified = facts["verified_i2"]
    context = verified["context"]
    lease = facts["lease"]
    _1174_require(a.lease_ref == facts["lease_ref"] == context["lease_ref"] and
        a.lease_path == facts["lease_path"] == context["lease_path"] and
        context["lease_oid"] == facts["lease_oid"] and
        verified["lease"]["lease_id"] == facts["lease_id"] == lease["lease_id"] and
        all(type(lease.get(k)) is int and lease[k] == admission[k] == getattr(a,k) for k in ("revision", "generation")) and
        context["generation"] == admission["generation"] and
        not any(getattr(a, k, None) is not None for k in ("lease_id", "granted_by", "evidence", "expires_utc")),
        "scoped lease authority mismatch")
    _1174_require(type(a.lease_comments) is str and _1174_read_json(a.lease_comments) == facts["comments"],
        "scoped lease comments differ from API")
    _1174_require(verified["comments_sha256"] == hashlib.sha256(_1174_bytes(facts["comments"])).hexdigest(),
        "scoped lease API receipt binding")
    _1174_require(state["state"] == "awaiting_lease", "scoped lease state")
    _xet_dung(directory, state, "record-lease")
    return _apply_lease_ref(a, directory, state, verified)


def _1174_postimage(old, new, command, admission):
    _1174_state(_1174_bytes(old), admission)
    _1174_state(_1174_bytes(new), admission)
    _1174_require(all(old[k] == new[k] for k in ("hmac_key", "packet", "mission", "generation", "enrollment_id", "binding_sha256",
                  "executor", "reviewer", "executor_identity", "reviewer_identity", "adoption")), "immutable state fields")
    changed = {k for k in set(old) | set(new) if (k in old) != (k in new) or old.get(k) != new.get(k)}
    _1174_require(changed - set(_1174_OPTIONAL) <= _1174_CORE_WRITES[command] | {"state_revision"}, "core command whitelist")
    _1174_require(changed & set(_1174_OPTIONAL) <= _1174_OPTIONAL_WRITES.get(command, set()), "optional command whitelist")
    _1174_require(new["state_revision"] == old["state_revision"] + 1 and all(new[k] >= old[k] for k in
                  ("review_rounds_used", "codex_review_calls_used", "attempts_limit", "review_rounds_limit", "codex_review_calls_limit")),
                  "state counter/revision monotonicity")
    _1174_require(all(new[k] <= admission["allowance"][k] for k in ("attempts_limit", "review_rounds_limit", "codex_review_calls_limit")), "approved allowance ceiling")
    _1174_require(new["attempts_used"] >= old["attempts_used"] or command == "void-attempt" and
                  new["attempts_used"] == old["attempts_used"] - 1 and old["attempt_open"] and not new["attempt_open"], "attempt counter transition")
    for key in ("history", "reviews", "nang_tran"):
        _1174_require(new[key][:len(old[key])] == old[key], "append-only state " + key)
    _1174_require(len(new["codex_calls"]) >= len(old["codex_calls"]) and all(
        n["run_id"] == p["run_id"] and n["head"] == p["head"] and (not p["da_dung"] or n["da_dung"])
        for p, n in zip(old["codex_calls"], new["codex_calls"])), "append-only call identity/consumption")


# These records are state projections of verified evidence, never authority roots.
_1174_REVIEW_KEYS = frozenset("schema head identity verdict finding_ids receipt_sha256 assurance call_id".split())
_1174_HUMAN_KEYS = frozenset("schema head tree pr spec_sha256 audit_comment_id audit_updated_at audit_sha256 collector_sha256 assurance".split())
_1174_COLLECTOR_KEYS = frozenset("schema repo_id repo head audit_comment_id audit_updated_at audit_sha256 started_utc ended_utc query_scope ref_scope event_scope raw_snapshot_sha256 cursor_coverage dag_coverage earliest residual_classes status".split())


def _1174_lifecycle_records(state, admission):
    review, human = state["scoped_review"], state["human_acceptance"]
    if review is not None:
        _1174_require(type(review) is dict and set(review) == _1174_REVIEW_KEYS and
            review["schema"] == "wp1174_scoped_review.v1" and type(review["head"]) is str and SHA_RE.fullmatch(review["head"]) and
            review["identity"] == state["reviewer_identity"] and review["verdict"] in ("approve", "changes_requested", "blocked") and
            type(review["finding_ids"]) is list and len(review["finding_ids"]) == len(set(review["finding_ids"])) and
            all(type(x) is str and SLUG_RE.fullmatch(x) for x in review["finding_ids"]) and
            _1174_hash(review["receipt_sha256"]) and (review["assurance"] == "advisory_review" or review["assurance"] == "same_provider_approved" and
                _1174_OWNER_POLICY.get() is not None and review["head"] == _1174_OWNER_POLICY.get()["policy"]["head"]) and
            (review["call_id"] is None or type(review["call_id"]) is str and any(
                x["run_id"] == review["call_id"] and x["head"] == review["head"] and x["da_dung"] for x in state["codex_calls"])),
            "scoped review closed record")
    if human is not None:
        _1174_require(type(human) is dict and set(human) == _1174_HUMAN_KEYS and
            human["schema"] == "wp1174_human_acceptance.v1" and human["assurance"] == "human_audited" and
            type(human["head"]) is str and SHA_RE.fullmatch(human["head"]) and
            type(human["tree"]) is str and SHA_RE.fullmatch(human["tree"]) and
            type(human["pr"]) is int and human["pr"] > 0 and
            type(human["audit_comment_id"]) is int and human["audit_comment_id"] > 0 and
            all(_1174_hash(human[k]) for k in ("spec_sha256", "audit_sha256", "collector_sha256")) and
            _1174_time(human["audit_updated_at"]) is not None and state["accepted_sha"] == human["head"],
            "human acceptance closed record")


def _1174_review(a, directory, admission):
    st = _load(directory, a.packet)
    _1174_require(_pending_human_lane(st),"scoped review requires canonical pending/human lane")
    _1174_require(type(a.bien_nhan) is str and bool(a.bien_nhan), "review receipt required")
    receipt_path = Path(a.bien_nhan)
    before = receipt_path.stat()
    raw = receipt_path.read_bytes()
    signature = lambda st: (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
    authority = _1174_OWNER_POLICY.get() if _1174_same_family(st) else None
    if authority is not None:
        _1174_policy_head(Path(a.root), authority, a.reviewed_sha)
    service = st["reviewer_identity"]["execution_surface"] == "codex_service"
    if not service:
        with tempfile.TemporaryDirectory(prefix="wp1174-receipt-") as temporary:
            copy = Path(temporary) / "receipt"
            copy.write_bytes(raw)
            args = argparse.Namespace(**vars(a))
            args.bien_nhan = str(copy)
            rc = cmd_record_review(args, directory)
        proposal = _1174_TRANSACTION["proposal"]
        if a.verdict == "approve":
            proposal["bien_nhan_approve"]["tep"] = a.bien_nhan
    else:
        _1174_require(st["state"] == "reviewing" and st["attempt_open"] and st["attempts_used"] > 0 and
            a.reviewed_sha == st["reviewing_head_sha"], "advisory attempt/head")
        _check_runtime_identity(a, st, "reviewer")
        _1174_require(a.provider == st["reviewer"], "advisory provider")
        record = _1174_json(raw)
        expected = dict(schema="wp1174_service_advisory.v1", head=a.reviewed_sha,
            identity=st["reviewer_identity"], verdict=a.verdict, finding_ids=sorted(set(a.finding_id or [])), assurance="advisory_review")
        if authority is not None:
            policy = authority["policy"]
            expected.update(schema="wp1174_owner_scoped_review.v1", assurance="same_provider_approved",
                policy_sha256=authority["sha256"], tree=policy["tree"], source_context_id=policy["source"]["context_id"],
                reviewer_context_id=policy["reviewer"]["context_id"])
        _1174_require(type(record) is dict and record == expected and set(record) == set(expected) and
            all(type(x) is str and SLUG_RE.fullmatch(x) for x in record["finding_ids"]) and
            (a.verdict != "changes_requested" or bool(record["finding_ids"])), "advisory receipt closed bindings")
        call = next((x for x in st["codex_calls"] if x["run_id"] == a.codex_call), None)
        _1174_require(call is not None and not call["da_dung"] and call["head"] == a.reviewed_sha, "advisory call reservation/replay")
        _xet_dung(directory, st, "record-review")
        call["da_dung"] = True
        st["attempt_open"] = False
        st["review_rounds_used"] += 1
        st["reviews"].append(dict(attempt=st["attempts_used"], provider=a.provider, verdict=a.verdict,
            reviewed_sha=a.reviewed_sha, finding_ids=record["finding_ids"], finding_descs=list(a.finding_desc or [])))
        for slug in record["finding_ids"]:
            st["finding_counts"][slug] = st["finding_counts"].get(slug, 0) + 1
        _xet_dung(directory, st, "record-review", a, [x for x in record["finding_ids"] if st["finding_counts"][x] >= st["same_failure_limit"]])
        st["state"] = {"approve": "approved_pending", "changes_requested": "running", "blocked": "blocked"}[a.verdict]
        if a.verdict == "approve":
            _1174_require(_pending_human_lane(st), "advisory canonical lease required")
            st.update(pending_sha=a.reviewed_sha, bien_nhan_approve=dict(p3=[]))
        st["history"].append(dict(event="record_review", verdict=a.verdict, reviewed_sha=a.reviewed_sha, finding_ids=record["finding_ids"]))
        _save(directory, st)
        proposal, rc = _1174_TRANSACTION["proposal"], 0
    _1174_require(signature(receipt_path.stat()) == signature(before), "review receipt changed during validation")
    proposal["scoped_review"] = dict(schema="wp1174_scoped_review.v1", head=a.reviewed_sha,
        identity=st["reviewer_identity"], verdict=a.verdict, finding_ids=sorted(set(a.finding_id or [])),
        receipt_sha256=hashlib.sha256(raw).hexdigest(), assurance="same_provider_approved" if authority is not None else "advisory_review", call_id=a.codex_call)
    proposal["human_acceptance"] = None
    return rc


def _1174_collect(fetch, root, head, audit, repo_id, *, deadline=None):
    """Bounded re-collection; incomplete retained history never becomes residual."""
    start = datetime.now(timezone.utc)
    end = min(start.timestamp() + 180, deadline if deadline is not None else start.timestamp() + 180)
    scope = ("events", "git/matching-refs/heads", "git/matching-refs/tags", "pulls?state=all")
    snapshots, coverage, introductions = {}, {}, []
    last_status,dag,earliest = "UNKNOWN",False,None
    for attempt in range(3):
        if time.time() >= end:
            break
        began, size, pages, complete = time.monotonic(), 0, 0, True
        pass_end=min(end,time.time()+120)
        snapshots, coverage, introductions = {}, {}, []
        for family in scope:
            values = []
            for page in range(1, 101):
                if pages >= 100 or time.monotonic() - began > 120 or time.time() >= end:
                    complete = False
                    break
                separator = "&" if "?" in family else "?"
                measured=[]
                try:
                    rows = fetch(f"repos/{_1174_REPO}/{family}{separator}per_page=100&page={page}",deadline=pass_end,max_bytes=30*1024*1024-size,on_bytes=measured.append)
                except (ValueError,subprocess.TimeoutExpired,OSError):
                    complete=False
                    break
                if time.time()>=pass_end or time.monotonic()-began>=120:
                    complete=False
                    break
                pages += 1
                _1174_require(type(rows) is list, "collector page type")
                size += sum(measured) if measured else len(_1174_bytes(rows))
                if size > 30 * 1024 * 1024:
                    complete = False
                    break
                values.extend(rows)
                if len(rows) < 100:
                    coverage[family] = page
                    break
            else:
                complete = False
            snapshots[family] = values
        # Events must cover the complete interval since the immutable audit. API
        # retention without an earlier boundary is UNKNOWN, even with empty pages.
        events = snapshots.get("events", [])
        boundary = any(type(x) is dict and _1174_time(x.get("created_at")) <= _1174_time(audit["updated_at"]) for x in events)
        dag = True
        preimages = []
        for event in events:
            if time.time()>=pass_end:dag=False;complete=False;break
            _1174_require(type(event) is dict and type(event.get("id")) is str and
                type(event.get("repo")) is dict and event["repo"].get("name") == _1174_REPO, "collector event identity")
            if event.get("type") != "PushEvent":
                if event.get("type") in ("CreateEvent", "PullRequestEvent"):
                    dag = False
                continue
            payload = event.get("payload", {})
            after, before = payload.get("head"), payload.get("before")
            if not (type(after) is str and SHA_RE.fullmatch(after) and type(before) is str and SHA_RE.fullmatch(before)):
                dag = False
                continue
            # Zero is the absence of a ref at creation/deletion, never a commit.
            # A preimage proves publication no later than this event, so it can
            # reject an earlier audit but cannot establish a first-push timestamp.
            matches = {}
            for side, oid in (("before", before), ("after", after)):
                if oid == "0" * 40:
                    matches[side] = False
                    continue
                rc, _ = _git_do(root, "cat-file", "-e", oid + "^{commit}", deadline=pass_end)
                relation, _ = _git_do(root, "merge-base", "--is-ancestor", head, oid, deadline=pass_end) if rc == 0 else (-1, b"")
                if time.time() >= pass_end:
                    dag = False; complete = False; break
                if relation not in (0, 1):
                    dag = False
                matches[side] = relation == 0
            preaudit = _1174_time(event["created_at"]) <= _1174_time(audit["updated_at"])
            if matches.get("after") or matches.get("before") and preaudit:
                introductions.append(dict(id=event["id"], time=event["created_at"], ref=payload.get("ref"),
                    actor=event.get("actor", {}).get("login"), before=before, after=after))
            if matches.get("before") and not preaudit:
                preimages.append((before, event["created_at"]))
        for oid, observed_at in preimages:
            if not any(x["after"] == oid and _1174_time(x["time"]) < _1174_time(observed_at) for x in introductions):
                dag = False
        # Every currently observable ref/PR must be accounted for by the DAG;
        # unsupported introductions cannot silently be called server residuals.
        for family in scope[1:]:
            for row in snapshots.get(family, []):
                if time.time()>=pass_end:dag=False;complete=False;break
                oid = row.get("head", {}).get("sha") if family.startswith("pulls") else row.get("object", {}).get("sha")
                if not (type(oid) is str and SHA_RE.fullmatch(oid)):
                    dag = False
                    continue
                relation, _ = _git_do(root, "merge-base", "--is-ancestor", head, oid,deadline=pass_end)
                if time.time()>=pass_end:dag=False;complete=False;break
                if relation not in (0, 1) or relation == 0 and not any(x["after"] == oid for x in introductions):
                    dag = False
        earliest = min(introductions, key=lambda x: (x["time"], x["id"])) if introductions else None
        if time.time()>=pass_end or time.monotonic()-began>=120:complete=False;dag=False
        last_status = ("FAIL" if earliest and _1174_time(earliest["time"]) <= _1174_time(audit["updated_at"]) else
            "RECORDED_EARLIEST_MATCH" if time.time()<pass_end and complete and boundary and dag and earliest else "UNKNOWN")
        if last_status != "UNKNOWN":
            break
    return dict(schema="wp1174_publication_receipt.v1", repo_id=repo_id, repo=_1174_REPO, head=head,
        audit_comment_id=audit["id"], audit_updated_at=audit["updated_at"], audit_sha256=hashlib.sha256(_1174_bytes(audit)).hexdigest(),
        started_utc=start.strftime("%Y-%m-%dT%H:%M:%SZ"), ended_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), query_scope=list(scope),
        ref_scope=["refs/heads/*", "refs/tags/*"], event_scope="repository_publication", raw_snapshot_sha256=hashlib.sha256(_1174_bytes(snapshots)).hexdigest(),
        cursor_coverage=coverage, dag_coverage=bool(dag), earliest=earliest,
        residual_classes=["server_unpublished_activity", "fork_object_storage_outside_repo_scope"], status=last_status)


def _1174_collector_receipt(receipt, head, audit, repo_id):
    _1174_require(type(receipt) is dict and set(receipt) == _1174_COLLECTOR_KEYS and
        receipt["schema"] == "wp1174_publication_receipt.v1" and receipt["repo"] == _1174_REPO and
        type(receipt["repo_id"]) is int and receipt["repo_id"] == repo_id and receipt["head"] == head and
        receipt["audit_comment_id"] == audit["id"] and receipt["audit_updated_at"] == audit["updated_at"] and
        receipt["audit_sha256"] == hashlib.sha256(_1174_bytes(audit)).hexdigest() and
        receipt["query_scope"] == ["events", "git/matching-refs/heads", "git/matching-refs/tags", "pulls?state=all"] and
        receipt["ref_scope"] == ["refs/heads/*", "refs/tags/*"] and receipt["event_scope"] == "repository_publication" and
        receipt["residual_classes"] == ["server_unpublished_activity", "fork_object_storage_outside_repo_scope"] and
        _1174_hash(receipt["raw_snapshot_sha256"]) and type(receipt["dag_coverage"]) is bool and
        type(receipt["cursor_coverage"]) is dict and receipt["status"] in ("RECORDED_EARLIEST_MATCH", "FAIL", "UNKNOWN") and
        _1174_time(receipt["started_utc"]) <= _1174_time(receipt["ended_utc"]), "collector receipt closed bindings")
    _1174_require(set(receipt["cursor_coverage"]) <= set(receipt["query_scope"]) and
        all(type(v) is int and 1<=v<=100 for v in receipt["cursor_coverage"].values()),"collector cursor schema")
    earliest=receipt["earliest"]
    _1174_require(earliest is None or (type(earliest) is dict and set(earliest)=={"id","time","ref","actor","before","after"} and
        all(type(earliest[k]) is str and earliest[k] for k in earliest) and
        SHA_RE.fullmatch(earliest["before"]) and SHA_RE.fullmatch(earliest["after"]) and
        earliest["ref"].startswith(("refs/heads/","refs/tags/")) and _1174_time(earliest["time"]) is not None),"collector earliest schema")
    _1174_require(receipt["status"]!="RECORDED_EARLIEST_MATCH" or
        earliest is not None and receipt["dag_coverage"] and set(receipt["cursor_coverage"])==set(receipt["query_scope"]),"collector success completeness")
    return receipt


def _1174_read_json(path):
    return json.loads(Path(path).read_bytes().decode("utf-8"), object_pairs_hook=_cam_khoa_trung,
        parse_constant=_cam_hang_ngoai_json)


def _1174_human_runs(a, head, deadline):
    _1174_require(type(a.human_remote_run) is str and type(a.workflow_runs) is str, "human run files required")
    claimed = _1174_read_json(a.human_remote_run)
    _1174_require(type(claimed) is dict and type(claimed.get("id")) is int and claimed["id"] > 0, "human run id")
    size = 0
    def fetch(endpoint):
        nonlocal size
        measured = []
        value = _1174_api(endpoint, root=Path(a.root), deadline=deadline,
            max_bytes=30*1024*1024-size, on_bytes=measured.append)
        size += sum(measured) if measured else len(_1174_bytes(value))
        _1174_require(time.time() < deadline and size <= 30*1024*1024, "human run readback budget")
        return value
    run = fetch(f"repos/{_1174_REPO}/actions/runs/{claimed['id']}")
    _1174_require(_1174_bytes(run) == _1174_bytes(claimed), "human remote run current readback mismatch")
    rows, total = [], None
    for page in range(1, 101):
        data = fetch(f"repos/{_1174_REPO}/actions/runs?head_sha={head}&per_page=100&page={page}")
        _1174_require(type(data) is dict and type(data.get("total_count")) is int and data["total_count"] >= 0 and
            type(data.get("workflow_runs")) is list and len(data["workflow_runs"]) <= 100,
            "human run pagination")
        total = data["total_count"] if total is None else total
        _1174_require(data["total_count"] == total, "human run pagination changed")
        rows.extend(data["workflow_runs"])
        if len(rows) >= total or len(data["workflow_runs"]) < 100:
            break
    _1174_require(len(rows) == total and all(type(x) is dict and type(x.get("id")) is int for x in rows) and
        len({x["id"] for x in rows}) == total, "human run pagination incomplete")
    caller = _trang_du(_1174_read_json(a.workflow_runs), "workflow_runs", "scoped human workflow_runs")
    key = lambda row: row["id"]
    _1174_require(_1174_bytes(sorted(rows, key=key)) == _1174_bytes(sorted(caller, key=key)),
        "human workflow set current readback mismatch")
    return run, dict(total_count=total, workflow_runs=rows)


@_1174_scoped
def _1174_human_evidence(a, admission, head):
    current, facts = _1174_resolve(Path(a.root), a.packet, a.revision, a.generation, a.admission)
    _1174_require(current == admission, "human authority changed")
    args = argparse.Namespace(**vars(a))
    args.head, args.repo = head, _1174_REPO
    p3 = []
    _1174_require(facts["lease"].get("packet_id") == "wp" + str(admission["packet"]) and
        all(type(facts["lease"].get(k)) is int and facts["lease"][k] == admission[k] for k in ("revision", "generation")), "human canonical scope")
    _1174_require(_git_do(Path(a.root),"rev-parse","refs/remotes/origin/master") ==
        (0,(facts["canonical_oid"]+"\n").encode()),"human canonical Git snapshot stale")
    collection_end = min(time.time()+180, _1174_time(admission["expires_utc"]).timestamp())
    run, runs = _1174_human_runs(args, head, min(collection_end, time.time()+120))
    receipt_path = getattr(a, "publication_receipt", None) or getattr(a, "receipt", None)
    receipt_raw = Path(receipt_path).read_bytes()
    comment_bytes = 0
    def comment_readback(ident):
        nonlocal comment_bytes
        measured = []
        observed = _1174_api(f"repos/{_1174_REPO}/issues/comments/{ident}", root=Path(args.root),
            deadline=collection_end, max_bytes=30*1024*1024-comment_bytes, on_bytes=measured.append)
        raw = _1174_bytes(observed)
        comment_bytes += sum(measured) if measured else len(raw)
        _1174_require(time.time() < collection_end and comment_bytes <= 30*1024*1024,
            "human comment readback budget")
        return raw
    # All owner inputs are captured before canonical validation. Only these
    # server-verified bytes reach the verifier, collector and acceptance record.
    with tempfile.TemporaryDirectory(prefix="wp1174-human-snapshot-") as temporary:
        snapshots = {}
        for field, schema in (("human_audit_comment", "human_exact_head_audit.v1"),
                              ("human_transition_comment", "human_audit_transition.v1")):
            original = getattr(args, field, None)
            if original is None:
                continue
            raw = Path(original).read_bytes()
            path = Path(temporary) / field
            path.write_bytes(raw)
            _, claimed, _ = _owner_record(path, _1174_REPO, args.pr, schema)
            verified_raw = comment_readback(claimed["id"])
            _1174_require(time.time() < collection_end and verified_raw == _1174_bytes(claimed),
                "human comment current readback mismatch")
            path.write_bytes(verified_raw)
            snapshots[field] = (verified_raw, claimed["id"])
            setattr(args, field, str(path))
        _1174_require("human_audit_comment" in snapshots, "human audit snapshot required")
        for field, value in (("human_remote_run", run), ("workflow_runs", runs)):
            path = Path(temporary) / field
            path.write_bytes(_1174_bytes(value))
            setattr(args, field, str(path))
        _human_merge(args, Path(args.root), facts["lease"], facts["spec"], p3)
        _1174_require(not p3, "human findings remain")
        _, audit, _ = _owner_record(args.human_audit_comment, _1174_REPO, args.pr, "human_exact_head_audit.v1")
        for field, (verified_raw, _) in snapshots.items():
            _1174_require(Path(getattr(args, field)).read_bytes() == verified_raw, "verified human snapshot changed")
        _1174_require(_1174_bytes(audit) == snapshots["human_audit_comment"][0], "verified audit snapshot changed")
    repo = _1174_api("repos/" + _1174_REPO,root=Path(a.root),deadline=collection_end)
    _1174_require(type(repo.get("id")) is int and repo["id"] > 0 and repo.get("full_name") == _1174_REPO, "collector repository")
    collected = _1174_collect(lambda endpoint,**limits: _1174_api(endpoint,root=Path(a.root),**limits), Path(a.root), head, audit, repo["id"],
        deadline=collection_end)
    for verified_raw, ident in snapshots.values():
        _1174_require(comment_readback(ident) == verified_raw, "human comment changed during validation")
    supplied = _1174_collector_receipt(_1174_json(receipt_raw), head, audit, repo["id"])
    # Observation timestamps can differ across two collections. All immutable
    # evidence/coverage must agree; neither caller status nor hash grants trust.
    keys = _1174_COLLECTOR_KEYS - {"started_utc", "ended_utc"}
    _1174_require(collected["status"] != "FAIL", "publication evidence FAIL")
    _1174_require(all(supplied[k] == collected[k] for k in keys) and collected["status"] == "RECORDED_EARLIEST_MATCH" and
        collected["dag_coverage"] is True and collected["earliest"] is not None, "publication evidence UNKNOWN/FAIL")
    rc, tree = _git_do(Path(a.root), "rev-parse", head + "^{tree}")
    _1174_require(rc == 0, "human tree unavailable")
    return dict(schema="wp1174_human_acceptance.v1", head=head, tree=tree.decode().strip(), pr=a.pr,
        spec_sha256=facts["spec_sha256"], audit_comment_id=audit["id"], audit_updated_at=audit["updated_at"],
        audit_sha256=collected["audit_sha256"], collector_sha256=hashlib.sha256(_1174_bytes(collected)).hexdigest(), assurance="human_audited")


def _1174_accept(a, directory, admission):
    st = _load(directory, a.packet)
    _1174_require(st["state"] == "approved_pending" and st["scoped_review"] is not None and
        st["scoped_review"]["head"] == st.get("pending_sha") and st["scoped_review"]["verdict"] == "approve", "accept requires scoped review")
    human = _1174_human_evidence(a, admission, st["pending_sha"])
    fields = ("workflow_runs", "check_runs", "connector", "bien_nhan_connector", "quyet_dinh_p3")
    paths = [getattr(a, field, None) for field in fields] + list(a.workflow_jobs or [])
    snapshots = {str(path): Path(path).read_bytes() for path in paths if path is not None}
    _1174_TRANSACTION["input_snapshots"] = snapshots
    try:
        rc = cmd_accept(a, directory)
    finally:
        _1174_TRANSACTION.pop("input_snapshots", None)
    _1174_TRANSACTION["proposal"]["human_acceptance"] = human
    return rc


@_1174_scoped
def _1174_guard(a):
    try:
        _1174_require(type(a.packet) is int and a.packet > 0 and type(a.revision) is int and a.revision > 0 and
            type(a.generation) is int and a.generation > 0 and Path(a.root).is_absolute() and SHA_RE.fullmatch(a.head) and
            type(a.admission) is str and bool(a.admission) and a.expected_revision is None and a.expected_witness_revision is None, "input_rejected: guard arguments")
        admission, _ = _1174_resolve(Path(a.root), a.packet, a.revision, a.generation, a.admission)
        _1174_runtime(a, admission)
    except (Exception, SystemExit) as ex:
        return _1174_emit("input_rejected" if isinstance(ex, _1174Error) and ex.status == "input_rejected" else "admission_rejected", str(ex), guard=True)
    try:
        _1174_human_evidence(a, admission, a.head)
        return _1174_emit("PASS", guard=True)
    except (Exception, SystemExit) as ex:
        return _1174_emit("FAIL" if isinstance(ex, _1174Error) and ex.status == "FAIL" else "UNKNOWN", str(ex), guard=True)


def _1174_input(a):
    _1174_require(all(type(getattr(a, k, None)) is int and getattr(a, k) > 0 for k in ("packet", "revision", "generation"))
                  and type(a.coordinator_id) is str and bool(a.coordinator_id) and
                  type(a.root) is str and Path(a.root).is_absolute(), "input_rejected: scoped identity/root")
    revision, witness = a.expected_revision, a.expected_witness_revision
    integer = lambda x: type(x) is str and re.fullmatch(r"0|[1-9][0-9]*", x) is not None
    if a.cmd == "init":
        valid = (a.mode == "fresh" and revision == "absent" and witness is None or
                 a.mode == "resume-initialization" and revision is None and integer(witness))
    elif a.cmd == "adopt-state":
        valid = revision is None and ((a.mode == "initial" and (witness == "absent" or integer(witness)) and
            a.expected_source_sha256 is not None and a.target_generation == a.generation and a.disposition is None) or
            (a.mode == "recovery" and integer(witness) and a.adoption_id is not None and a.disposition is not None and
             a.expected_source_sha256 is None and a.target_generation is None))
    else:
        valid = integer(revision) and witness is None
    _1174_require(valid, "input_rejected: revision namespace/mode")


def _1174_emit(status, detail=None, guard=False):
    rc, dispatch = _1174_status(status, guard)
    print(json.dumps(dict(status=status, dispatch_allowed=dispatch, detail=detail), ensure_ascii=False, sort_keys=True))
    return rc


@_1174_scoped
def _1174_readonly(a, state_dir):
    """Read enrolled v3 through the same authority/pair validators, without a writer."""
    global _1174_TRANSACTION
    previous = globals().get("_1174_TRANSACTION")
    policy_token = _1174_OWNER_POLICY.set(None)
    try:
        _1174_require(a.expected_revision is None and a.expected_witness_revision is None,
                      "read-only revision namespace")
        _1174_require(all(type(getattr(a, k, None)) is int and getattr(a, k) > 0
            for k in ("packet", "revision", "generation")) and type(a.root) is str and Path(a.root).is_absolute(),
            "read-only scoped identity/root")
        admission, first_facts = _1174_resolve(Path(a.root), a.packet, a.revision, a.generation, a.admission)
        _1174_OWNER_POLICY.set(first_facts.get("owner_policy"))
        e = admission["enrollment"]
        _1174_require(state_dir.resolve() == Path(e["journal_root"]) and os.path.lexists(e["lock_path"]),
                      "read-only enrolled directory/lock")
        _1174_runtime(a, admission)
        with _1174_lock(Path(current_lock := e["lock_path"])):
            current, facts = _1174_resolve(Path(a.root), a.packet, a.revision, a.generation, a.admission)
            _1174_require(current == admission and facts.get("owner_policy") == first_facts.get("owner_policy"), "authority changed under lock")
            _1174_runtime(a, admission)
            witness = _1174_witness(_1174_read(Path(e["witness_path"])), e["id"], e["binding_sha256"], e["g0"])
            state = _1174_pair(current, witness, _1174_read(Path(e["state_path"])))
            _1174_tripwire(state)
            _1174_alive(admission)
            _1174_TRANSACTION = dict(directory=state_dir.resolve(), state=state, proposal=None, admission=admission, read_only=True)
            return a.fn(a, state_dir)
    except (Exception, SystemExit) as ex:
        return _1174_emit("UNKNOWN", f"{type(ex).__name__}: {ex}")
    finally:
        _1174_TRANSACTION = previous
        _1174_OWNER_POLICY.reset(policy_token)


@_1174_scoped
def _1174_command(a, state_dir):
    global _1174_IO_STARTED
    _1174_IO_STARTED = False
    status, detail = "UNKNOWN", None
    policy_token = _1174_OWNER_POLICY.set(None)
    try:
        _1174_input(a)
        _1174_require(platform.system() == "Linux", "unsupported native operating system")
        _1174_require(_1174_IMPLEMENTATION_COMPLETE,
                      "implementation inventory unavailable")
        admission, first_facts = _1174_resolve(Path(a.root), a.packet, a.revision, a.generation, a.admission)
        _1174_OWNER_POLICY.set(first_facts.get("owner_policy"))
        e = admission["enrollment"]
        directory = Path(e["journal_root"])
        _1174_require(state_dir.resolve() == directory, "state directory differs from enrollment")
        _1174_runtime(a, admission)
        with _1174_lock(Path(e["lock_path"])):
            identities = (_1174_state(_1174_read(Path(e["state_path"])), admission) if
                          a.cmd not in ("init", "adopt-state") else None)
            current, facts = _1174_resolve(Path(a.root), a.packet, a.revision, a.generation, a.admission, identities)
            _1174_require(current == admission and facts.get("owner_policy") == first_facts.get("owner_policy"), "authority changed under lock")
            _1174_runtime(a, current)
            witness_raw = _1174_read(Path(e["witness_path"])) if os.path.lexists(e["witness_path"]) else None
            if a.cmd == "init":
                status = _1174_initialize(a, admission, witness_raw)
            elif a.cmd == "adopt-state":
                status = _1174_adopt(a, admission, witness_raw)
            else:
                status = _1174_ordinary(a, directory, admission, witness_raw, facts)
    except (Exception, SystemExit) as ex:
        # Boundary includes canonical Chan, TimeoutExpired and parser failures;
        # process kill/KeyboardInterrupt still cannot produce a success record.
        detail = f"{type(ex).__name__}: {ex}"
        status = ("durability_unknown" if _1174_IO_STARTED else ex.status if isinstance(ex, _1174Error) and
                  ex.status in ("input_rejected", "revision_rejected", "legacy_changed") else "UNKNOWN")
    finally:
        _1174_OWNER_POLICY.reset(policy_token)
    return _1174_emit(status, detail)


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
    q.add_argument("--lease-id", help="định danh lease bên điều phối đã cấp")
    q.add_argument("--granted-by",
                   help=f"bên CÓ THẨM QUYỀN đã cấp. KHÔNG được là {PROVIDERS} — "
                        f"agent không tự cấp cho mình")
    q.add_argument("--evidence",
                   help="dấu vết bền để đối chiếu (URL/ID comment nơi lease được cấp)")
    q.add_argument("--expires-utc",
                   help="hạn lease, ISO8601 CÓ múi giờ, ví dụ 2026-08-13T18:30:00Z")
    for co, mo_ta in (("--lease-ref", "#812 đường mới: origin/<nhánh> chứa tệp lease"), ("--lease-path", "tệp lease trong ref"),
                      ("--lease-comments", "JSON comment của Packet Issue (readback R)"), ("--root", "gốc kho git")):
        q.add_argument(co, help=mo_ta, default="." if co == "--root" else None)
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
    q.add_argument("--bien-nhan", help="#812: biên nhận review (YAML v2 + bang_lop) — bắt buộc với packet áp ADR-0054")
    q.add_argument("--root", default=".", help="gốc kho git (đọc validator canon từ origin/master)")
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
                       help="gate bắt buộc phải XANH THẬT trên head, trong đúng check suite (đọc JSON check-runs)",
                       epilog="Mã thoát: 0 mọi tên bắt buộc xanh · 2 sai đối số · "
                              "12 gate không xanh trên head hoặc KHÔNG ĐO ĐƯỢC.")
    q.add_argument("--head", required=True, help="SHA 40 ký tự của head cần kiểm")
    q.add_argument("--check-runs", required=True, dest="check_runs",
                   help="tệp JSON: object có `check_runs`, hoặc list trang (`--slurp`)")
    q.add_argument("--bat-buoc", action="append", required=True, dest="bat_buoc",
                   help="tên check-run bắt buộc, khớp TUYỆT ĐỐI; lặp lại được")
    q.add_argument("--check-suite", required=True, dest="check_suite",
                   help="id suite của CHÍNH lượt workflow cần kiểm: `GET actions/runs/<run_id>` → "
                        "`check_suite_id`; chỉ run thuộc suite này được xét. Tệp check-runs lấy với "
                        "`filter=all` (mọi lần chạy lại, không chỉ lần mới nhất)")
    q.set_defaults(fn=cmd_kiem_gate)

    q = sub.add_parser("accept", help="#834: approved_pending → accepted (packet áp ADR-0054); readback R do người gọi lấy trên pending_sha")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--root", default=".")
    q.add_argument("--pr", type=int, required=True)
    q.add_argument("--workflow-runs", required=True, help="trang `actions/runs?head_sha=` (`workflow_runs`, `total_count`)")
    q.add_argument("--workflow-jobs", required=True, action="append", help="trang `actions/runs/<id>/attempts/<n>/jobs` (`jobs`, `total_count`); lặp mỗi run")
    q.add_argument("--check-runs", required=True, help="trang check-runs của head, `filter=all`")
    q.add_argument("--connector", required=True, help="JSON {repo, pr, head_sha, reviews|review_comments|issue_comments: trang {total_count, items}}")
    q.add_argument("--bien-nhan-connector", help="biên nhận H: bang_lop[].connector_refs = [[endpoint, id], ...] (bắt buộc khi connector có P3)")
    q.add_argument("--quyet-dinh-p3", help="JSON list {nguon: offline|connector, khoa: slug, ten_no, owner, huong, ly_do}")
    q.set_defaults(fn=cmd_accept)

    for flag in ("--human-audit-comment", "--human-remote-run", "--human-transition-comment", "--publication-receipt"):
        q.add_argument(flag)
    q = sub.add_parser("mo-lai", help="#813: approved_pending → running (ci-do) | cho_chu_kho (connector); slug từ biên nhận H, readback R trên head")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--root", default=".")
    q.add_argument("--pr", type=int, required=True)
    q.add_argument("--nguyen-nhan", required=True, choices=NGUYEN_NHAN_MO_LAI)
    q.add_argument("--bien-nhan", required=True, help="biên nhận H verdict changes_requested trên head: bang_lop[].connector_refs | check_refs [[workflow, job], ...]")
    q.add_argument("--finding-id", action="append", help="slug của bảng lớp biên nhận; khai ĐỦ mọi lớp, ít nhất một")
    q.add_argument("--connector", required=True, help="JSON như `accept --connector`, neo đúng head")
    q.add_argument("--workflow-runs", help="như `accept` (bắt buộc với ci-do)")
    q.add_argument("--workflow-jobs", action="append", help="như `accept`; lặp mỗi run (bắt buộc với ci-do)")
    q.add_argument("--check-runs", help="trang check-runs của head, `filter=all` (bắt buộc với ci-do)")
    q.set_defaults(fn=cmd_mo_lai)

    q = sub.add_parser("chu-kho-duyet", help="#813: rời cho_chu_kho (cho_phep_va) | ghi quyền cho_phep_day — checkpoint trên origin/master")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--root", default=".")
    q.add_argument("--checkpoint-path", required=True, help="ops/checkpoints/<tên>.yaml, đọc tại origin/master sau khi máy tự fetch")
    q.set_defaults(fn=cmd_chu_kho_duyet)

    q = sub.add_parser("kiem-merge", help="#1106 ADR-0060: đủ điều kiện bỏ draft/merge trên head H? (K0–K7, không state)")
    for x in ("--root", "--repo", "--head", "--base", "--spec", "--lease", "--workflow-runs", "--check-runs", "--connector", "--offline-run-json", "--offline-stdout"):
        q.add_argument(x, required=x not in ("--root", "--offline-run-json", "--offline-stdout"), default="." if x == "--root" else None)
    for x in ("--human-audit-comment", "--human-transition-comment", "--human-remote-run"):
        q.add_argument(x, help="ADR-0063: raw API owner audit/transition comment hoặc run readback")
    q.add_argument("--pr", type=int, required=True)
    q.add_argument("--workflow-jobs", required=True, action="append")
    q.add_argument("--p3-offline", action="append", help="khoá P3 còn mở từ review offline; lặp")
    q.add_argument("--chu-kho-comment", help="readback JSON một comment của chủ kho (dòng `mien_p3:` / `windows:` / `full_mutant_audit:`)")
    q.add_argument("--windows-json", help="{sha, os: Windows, tests: [{id, ket_qua}]} của lượt ứng viên")
    q.add_argument("--dot-bien-du-runs", help="#1120 K7: readback trang `actions/workflows/ci-dot-bien-du.yml/runs?head_sha=H`")
    q.add_argument("--dot-bien-du-jobs", action="append", help="#1120 K7: readback trang `actions/runs/<id>/jobs`; lặp")
    q.set_defaults(fn=cmd_kiem_merge)

    q = sub.add_parser("adopt-state", help="scoped adoption management; recovery requires exact witness identity")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--root", default=".")
    q.add_argument("--mode", choices=("initial", "recovery"), required=True)
    q.add_argument("--adoption-id", required=True)
    q.add_argument("--expected-source-sha256")
    q.add_argument("--target-generation", type=int)
    q.add_argument("--disposition", choices=("resume_forward", "abandon_before_cutover", "abandon_before_prepare"))
    q.set_defaults(fn=None)
    q = sub.add_parser("guard-first-publication", help="read-only canonical admission/audit/publication guard")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--root", required=True)
    q.add_argument("--receipt", required=True)
    q.add_argument("--pr", type=int, required=True)
    q.add_argument("--head", required=True)
    q.add_argument("--human-audit-comment", required=True)
    q.add_argument("--human-remote-run", required=True)
    q.add_argument("--human-transition-comment")
    q.add_argument("--workflow-runs", required=True)
    q.set_defaults(fn=None)
    for name in (*_1174_MUTATORS, "guard-first-publication"):
        command = sub.choices[name]
        for flag in ("--admission", "--expected-revision", "--expected-witness-revision", "--coordinator-id"):
            command.add_argument(flag)
        command.add_argument("--revision", type=int)
        command.add_argument("--generation", type=int)
        if name == "init":
            command.add_argument("--root", default=".")
            command.add_argument("--mode", choices=("fresh", "resume-initialization"), default="fresh")
        elif not any(option.dest == "root" for option in command._actions):
            command.add_argument("--root", default=".")

    q = sub.add_parser("kiem-dong-wp", help="#1106 ADR-0060 M8: biên bản sổ sách + lease đủ để đóng WP? (D1–D4, không state)")
    q.add_argument("--root", default=".")
    q.add_argument("--bien-ban", required=True, help="khối YAML của biên bản M8")
    q.add_argument("--lease", required=True, help="tệp lease cuối của packet")
    q.set_defaults(fn=cmd_kiem_dong_wp)

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

    for name in ("status", "next-comment"):
        command = sub.choices[name]
        for flag in ("--admission", "--expected-revision", "--expected-witness-revision", "--coordinator-id"):
            command.add_argument(flag)
        command.add_argument("--root", default=".")
        command.add_argument("--revision", type=int)
        command.add_argument("--generation", type=int)
    sub.add_parser("where", help="in thư mục state").set_defaults(fn=cmd_where)
    return p


def main(argv=None) -> int:
    _cung_hoa_stdout()
    arguments = list(sys.argv[1:] if argv is None else argv)
    scoped_syntax = any(arg.split("=", 1)[0] in {"--admission", "--revision", "--generation", "--coordinator-id",
                        "--expected-revision", "--expected-witness-revision", "--mode"} for arg in arguments)
    try:
        a = build_parser().parse_args(arguments)
    except SystemExit as ex:
        if scoped_syntax and ex.code != 0:
            return _1174_emit("input_rejected", "scoped argument syntax")
        raise
    if a.cmd in ("status", "next-comment") and getattr(a, "admission", None) is not None:
        return _1174_readonly(a, Path(a.state_dir))
    if a.cmd in ("status", "next-comment") and scoped_syntax:
        return _1174_emit("input_rejected", "scoped flags require admission")
    if a.cmd == "guard-first-publication":
        return _1174_guard(a)
    if a.cmd in _1174_MUTATORS and getattr(a, "admission", None) is not None:
        return _1174_command(a, Path(a.state_dir))
    if a.cmd in _1174_MUTATORS and scoped_syntax:
        return _1174_emit("input_rejected", "scoped flags require admission")
    if a.cmd == "adopt-state":
        _die(RC_ARG, "adopt-state requires --admission")
    return a.fn(a, Path(a.state_dir))


if __name__ == "__main__":
    sys.exit(main())
