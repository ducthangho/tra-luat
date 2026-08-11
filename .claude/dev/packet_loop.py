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
    8  transition không hợp lệ theo state machine

Ba cơ chế dưới đây là LÕI của revision 2. Chúng thay ba cơ chế mà ba lượt review
liên tiếp chứng minh là sai từ thiết kế — chi tiết ở phần chú thích từng chỗ.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
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
CHUYEN_HOP_LE = {
    "leased": ("running",),
    "running": ("reviewing",),
    "reviewing": ("accepted", "running", "blocked"),
    "accepted": (),
    "blocked": (),
}

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


def _chuan_hoa(text: str) -> str:
    """NFC + casefold + gộp khoảng trắng — dùng CHỈ cho doctrine-scan."""
    text = unicodedata.normalize("NFC", text).casefold()
    return " ".join(text.split())


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
    if p.exists() and not a.force_new:
        _die(RC_STATE, f"state đã tồn tại: {p}")
    st = {
        "schema_version": 1,
        "packet": a.packet,
        "mission": a.mission,
        "executor": a.executor,
        "reviewer": a.reviewer,
        "state": "leased",
        "attempts_used": 0,
        "attempts_limit": a.attempts_limit,
        "same_failure_limit": a.same_failure_limit,
        "finding_counts": {},
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


def cmd_begin_attempt(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    if a.provider != st["executor"]:
        _die(
            RC_PROVIDER,
            f"provider {a.provider!r} không phải executor của packet này ({st['executor']!r})",
        )
    # Lượt đầu đi từ 'leased'; lượt rework đi từ 'running' sau changes_requested.
    if st["state"] not in ("leased", "running"):
        _die(RC_STATE, f"không mở được lượt từ state {st['state']!r}")
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

    st["reviews"].append(
        {
            "attempt": st["attempts_used"],
            "provider": a.provider,
            "verdict": a.verdict,
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
    st["history"].append({"event": "record_review", "verdict": a.verdict, "finding_ids": ids_duy_nhat})
    _save(state_dir, st)
    print(
        f"đã ghi review {a.verdict} bởi {a.provider} — "
        f"{len(ids_duy_nhat)} finding, state {st['state']}"
    )
    return RC_OK


def cmd_transition(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    _kiem_chuyen(st, a.to)
    so = _tieu_thu_comment_id(st, a.comment_id, a.to)
    so["consumed_by"] = a.to
    truoc = st["state"]
    st["state"] = a.to
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
        for i, dong in enumerate(raw.splitlines(), 1):
            norm = _chuan_hoa(dong)
            for nhom, cum_list in FORBIDDEN_DOCTRINE_PHRASES.items():
                for cum in cum_list:
                    if _chuan_hoa(cum) in norm:
                        dinh.append((str(f), nhom, cum, i))

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
            "7 hành vi bị chặn cứng · 8 transition không hợp lệ."
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
    q.add_argument("--force-new", action="store_true")
    q.set_defaults(fn=cmd_init)

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
