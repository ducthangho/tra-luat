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
import html
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

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
    "reviewing": ("running", "blocked"),
    "accepted": (),
    "blocked": (),
}

# Các state chỉ được ghi bởi luồng review, không bao giờ bởi `transition`.
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


# Ký tự TRANG TRÍ của Markdown, bị bỏ trước khi so. Không có bước này thì chép
# nguyên một dòng doctrine kèm dấu nháy ngược là lọt: `merged`: … không khớp
# "merged: …". Đã ĐO: 5/9 dòng doctrine THẬT lọt lưới chỉ vì lớp trang trí này.
# Bỏ cả gạch dưới nên `same_failure_limit` và `same failure limit` quy về một mối
# — hai vế đều đi qua cùng phép chuẩn hoá nên vẫn khớp nhau.
_TRANG_TRI = str.maketrans("", "", "`*_~")


def _chuan_hoa(text: str) -> str:
    """Giải HTML entity + bỏ ký tự định dạng vô hình + NFC + casefold + bỏ trang
    trí Markdown + gộp khoảng trắng.

    Dùng CHỈ cho doctrine-scan. Ở đây chuẩn hoá rộng là ĐÚNG HƯỚNG, ngược hẳn
    với phép đếm finding: khớp rộng chỉ buộc adapter viết mỏng hơn (sai về phía
    an toàn), còn khớp rộng ở finding-id sẽ gộp oan hai lỗi khác nhau.

    Hai lớp đầu vá `doctrine-rendering-bypass` (cross-review lượt 4, codex,
    14-08-2026): bản trước xử lý trang trí Markdown và khoảng trắng, nhưng KHÔNG
    xử lý ký tự định dạng vô hình lẫn HTML entity, nên `mer<ZWSP>ged: ...` và
    `merged&#58; ...` đều lọt (`rc=0`) dù cả hai RENDER RA đúng cụm bị cấm.

      1. `html.unescape` giải entity — `&#58;` → `:`, `&amp;` → `&`, v.v. — để câu
         gõ bằng entity và câu gõ bằng ký tự thật quy về một mối.
      2. Bỏ ký tự thuộc phạm trù Unicode `Cf` (định dạng — gồm `U+200B` zero-width
         space, `U+200C`/`U+200D` ZWNJ/ZWJ, `U+FEFF` BOM, `U+00AD` soft hyphen…):
         những ký tự này KHÔNG hiển thị nhưng vẫn chia cắt được một chuỗi khớp.

    AN TOÀN — nói thẳng, đừng lặp: `html.unescape` giải entity ĐÚNG MỘT LẦN (nó
    thay thế trên chuỗi GỐC bằng một lượt quét tuyến tính, không quét lại phần vừa
    thay), không lặp tới điểm bất động. Giải LẶP sẽ biến `&amp;#58;` — thứ hiển
    thị NGUYÊN VĂN `&#58;` trong Markdown/HTML, KHÔNG phải dấu hai chấm — thành
    dấu hai chấm thật, và sinh DƯƠNG TÍNH GIẢ trên cụm `merged: ...`. Đã ĐO:
    `html.unescape("&amp;#58;")` → `"&#58;"`, không phải `":"`.
    """
    text = html.unescape(text)
    text = unicodedata.normalize("NFC", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Cf")
    text = text.casefold().translate(_TRANG_TRI)
    return " ".join(text.split())


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
    phan, ban_do, vi_tri = [], [], 0
    for so_dong, dong in enumerate(raw.splitlines(), 1):
        n = _chuan_hoa(dong)
        if not n:
            continue
        if phan:
            phan.append(" ")
            vi_tri += 1
        ban_do.append((vi_tri, so_dong))
        phan.append(n)
        vi_tri += len(n)
    return "".join(phan), ban_do


def _dong_tai(ban_do, offset: int) -> int:
    """Vị trí trong chuỗi phẳng → số dòng gốc gần nhất."""
    so = ban_do[0][1] if ban_do else 0
    for bat_dau, so_dong in ban_do:
        if bat_dau > offset:
            break
        so = so_dong
    return so


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
    nguoi_cap = (a.granted_by or "").strip()
    if not nguoi_cap:
        _die(RC_ARG, "--granted-by rỗng")
    # Chốt CỐT LÕI. Một agent tự ký cho chính mình thì thứ ghi ra không phải lease,
    # chỉ là lời tự khai đội lốt uỷ quyền. §2: start/authorize thuộc bên CÓ THẨM
    # QUYỀN; tiến trình này chỉ ghi hộ. So khớp không phân biệt hoa thường vì
    # "Claude" và "claude" là cùng một lời tự khai.
    if nguoi_cap.lower() in PROVIDERS:
        _die(RC_GUARD,
             f"--granted-by {nguoi_cap!r} là tên một provider — agent KHÔNG tự cấp lease "
             f"cho mình được (xem doctrine 'không tự cấp lease')")
    # CHỐT THẬT: phải NẰM TRONG danh sách cho phép, không chỉ "không nằm trong danh
    # sách cấm" ở trên. Đây là chỗ `codex-dispatcher` / `ai-codex-bot` / `cödex`
    # từng lọt (finding `lease-authority-spoof`, xem chú thích ở `NGUOI_CO_THAM_QUYEN`).
    if nguoi_cap.lower() not in NGUOI_CO_THAM_QUYEN:
        _die(RC_GUARD,
             f"--granted-by {nguoi_cap!r} KHÔNG nằm trong danh sách người có thẩm quyền "
             f"{list(NGUOI_CO_THAM_QUYEN)} — danh sách CẤM không bao giờ đủ (cross-review "
             f"14-08-2026, finding lease-authority-spoof), nên chốt này đòi tên phải ĐƯỢC "
             f"PHÉP chứ không chỉ 'không bị cấm'. Thêm người cấp mới = sửa "
             f"NGUOI_CO_THAM_QUYEN qua một commit có review.")
    if not (a.evidence or "").strip():
        _die(RC_ARG, "--evidence rỗng — lease phải có dấu vết bền để đối chiếu")
    han = _doc_han_utc(a.expires_utc)
    if han <= datetime.now(timezone.utc):
        _die(RC_STATE,
             f"lease đã hết hạn ngay lúc ghi ({han.isoformat()}) — xin lease mới, "
             f"đừng ghi một lease chết rồi coi như có quyền")
    st["lease"] = {
        "lease_id": a.lease_id,
        "granted_by": nguoi_cap,
        "evidence": a.evidence.strip(),
        "expires_utc": han.isoformat(),
    }
    st["state"] = "leased"
    st["history"].append({"event": "record_lease", "lease_id": a.lease_id,
                          "granted_by": nguoi_cap, "expires_utc": han.isoformat()})
    _save(state_dir, st)
    print(f"đã ghi lease {a.lease_id} (cấp bởi {nguoi_cap}, hết hạn {han.isoformat()}) "
          f"— state {st['state']}")
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
    lease = st.get("lease")
    if not lease or not lease.get("expires_utc"):
        _die(RC_STATE,
             f"state {st['state']!r} không có 'lease' hợp lệ — 'leased'/'running' chỉ "
             f"đạt được qua `record-lease`, nên state thiếu lease là CŨ hoặc HỎNG. "
             f"KHÔNG mở lượt ngầm trên state đó; cần một đường di trú tường minh, có "
             f"uỷ quyền, do bên điều phối cấp (generation mới + record-lease thật).")
    het = _doc_han_utc(lease["expires_utc"])
    if het <= datetime.now(timezone.utc):
        _die(RC_STATE,
             f"lease {lease.get('lease_id')!r} đã hết hạn lúc {het.isoformat()} — "
             f"không mở lượt mới được; xin lease mới từ bên điều phối")
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
    st["attempts_used"] += 1
    st["state"] = "running"
    st["attempt_open"] = True
    # Head cũ hết hiệu lực ngay khi mở lượt mới: có commit mới thì bản duyệt
    # trước không còn nói về cây đang có nữa.
    st["reviewing_head_sha"] = None
    st["history"].append({"event": "begin_attempt", "attempt": st["attempts_used"]})
    _save(state_dir, st)
    print(f"bắt đầu lượt {st['attempts_used']}/{st['attempts_limit']} — state {st['state']}")
    return RC_OK


def cmd_void_attempt(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    if a.reason not in LY_DO_VOID:
        _die(RC_ARG, f"lý do {a.reason!r} không thuộc allowlist {LY_DO_VOID}")
    if st["attempts_used"] <= 0:
        _die(RC_STATE, "chưa có lượt nào để hoàn")
    # Lượt ĐÃ được review thì không hoàn được — nếu không, mọi lượt hỏng đều
    # biến thành "quota" và trần trở thành trang trí.
    if st["reviews"] and st["reviews"][-1]["attempt"] == st["attempts_used"]:
        _die(
            RC_STATE,
            f"lượt {st['attempts_used']} đã có review — không hoàn được lượt đã tiêu thụ nội dung",
        )
    st["attempts_used"] -= 1
    # Đóng luôn lượt đang mở. Thiếu dòng này thì hoàn lượt vì quota lại KHOÁ CỨNG
    # packet: trần đã trả về nhưng `attempt_open` còn bật nên không mở lại được
    # lượt nào — biến một lỗi hạ tầng tạm thời thành ngõ cụt vĩnh viễn.
    st["attempt_open"] = False
    st["history"].append({"event": "void_attempt", "reason": a.reason})
    _save(state_dir, st)
    print(f"đã hoàn một lượt vì {a.reason} — còn dùng {st['attempts_used']}/{st['attempts_limit']}")
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
            "7 hành vi bị chặn cứng · 8 trạng thái không hợp lệ."
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
    q.set_defaults(fn=cmd_begin_attempt)

    q = sub.add_parser("void-attempt", help="hoàn lượt vì lỗi hạ tầng/quota")
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--reason", required=True, help=f"một trong {LY_DO_VOID}")
    q.set_defaults(fn=cmd_void_attempt)

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
