#!/usr/bin/env python3
"""Máy trạng thái cho vòng lặp executor<->reviewer của protocol đa phiên.

F3-03 (ADR: docs/PROTOCOL_DA_PHIEN.md §12 stop conditions, §13 hợp đồng ba skill).

Vì sao là SCRIPT chứ không phải mấy dòng markdown: trần vòng lặp chỉ có giá trị khi
CHỨNG MINH được nó dừng. Markdown khai "tối đa 3 lượt" không kiểm được; tiến trình
thoát khác 0 thì kiểm được — xem `packet_loop_test.py`, mỗi chốt có một phản chứng.

Ngưỡng KHÔNG tự đặt: lấy từ envelope của mission #48
(`max_attempts_per_packet: 3`, `same_failure_limit: 2`).

Script này TUYỆT ĐỐI không chạm remote: không gọi git push, không gọi gh, không đọc
secrets. Nó chỉ giữ state + phát VĂN BẢN comment; phiên Claude là đường ghi remote duy
nhất (một audit trail một chỗ). Nhờ vậy codex chạy được nó trong sandbox workspace-write.

Mã thoát — đọc TRỰC TIẾP, đừng đọc qua pipe:
  0  cho phép đi tiếp
  2  sai cú pháp / thiếu state
  3  DỪNG theo chốt an toàn (chạm trần, blocked, hành vi cấm)  -> cần người
  4  vi phạm cross-provider
  5  còn comment chưa đăng lên Issue (chặn advance để transition không mất dấu)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA = "packet_loop.v1"

# Envelope mission #48 — KHÔNG sửa ở đây; đổi ngưỡng là đổi spec của mission.
MAX_ATTEMPTS = 3
SAME_FAILURE_LIMIT = 2

PROVIDERS = ("claude", "codex")

# Hành vi CHỈ người mới được làm. Vòng lặp tự do tới TRƯỚC merge, không hơn.
FORBIDDEN_ACTIONS = {
    "merge": "merge vào master",
    "deploy": "deploy Package",
    "live": "gọi LIVE",
    "secrets": "đọc/ghi secrets",
    "force-push": "force-push",
    "delete-branch": "xoá branch",
    "delete-worktree": "xoá worktree",
    "edit-other-spec": "sửa spec của mission/packet khác",
}

RC_OK, RC_USAGE, RC_STOP, RC_PROVIDER, RC_UNPOSTED = 0, 2, 3, 4, 5


def _fingerprint(text: str) -> str:
    """Vân tay nội dung của một finding.

    Chuẩn hoá trước khi băm để "cùng một lỗi, diễn đạt lệch vài khoảng trắng / hoa
    thường" vẫn đếm là MỘT. Không cố làm ngữ nghĩa — chỉ cần đủ để trần đếm đúng thứ
    nó hứa đếm; reviewer diễn đạt lại hoàn toàn thì đó là finding khác, và test
    `case_finding_khac_nhau_khong_bi_chan` khoá đúng hành vi đó.
    """
    norm = re.sub(r"\s+", " ", text.strip().casefold())
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:12]


def _state_path(state_dir: Path, packet: int) -> Path:
    return state_dir / f"wp{packet}.json"


def _load(state_dir: Path, packet: int) -> dict:
    p = _state_path(state_dir, packet)
    if not p.exists():
        _die(RC_USAGE, f"CHUA_INIT: không thấy {p}. Chạy `init` trước.")
    return json.loads(p.read_text(encoding="utf-8"))


def _save(state_dir: Path, st: dict) -> None:
    p = _state_path(state_dir, st["packet"])
    p.parent.mkdir(parents=True, exist_ok=True)
    # LF cứng + newline cuối: tệp state cũng đi qua policy EOL canonical của F2.
    p.write_text(json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                 encoding="utf-8", newline="\n")


def _die(rc: int, msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(rc)


def _queue(st: dict, body: str) -> None:
    st["pending_comments"].append(body)


def _require_posted(st: dict) -> None:
    """Chặn mọi transition khi còn comment chưa đăng.

    Đây là thứ biến "mọi transition ghi comment vào Issue" từ lời hứa thành cơ chế:
    quên đăng thì vòng lặp KHÔNG đi tiếp được, chứ không phải trôi im lặng rồi mất dấu
    trong context phiên.
    """
    if st["pending_comments"]:
        _die(RC_UNPOSTED,
             f"CON_{len(st['pending_comments'])}_COMMENT_CHUA_DANG: đăng lên Issue "
             f"#{st['packet']} rồi chạy `mark-posted --url <url>` trước khi đi tiếp.")


def cmd_init(a, state_dir: Path) -> int:
    if a.executor == a.reviewer:
        _die(RC_PROVIDER,
             f"CROSS_PROVIDER_VI_PHAM: executor và reviewer cùng là `{a.executor}`. "
             "Quy tắc: executor claude => reviewer codex, và ngược lại.")
    for who, prov in (("executor", a.executor), ("reviewer", a.reviewer)):
        if prov not in PROVIDERS:
            _die(RC_USAGE, f"PROVIDER_LA: {who}=`{prov}` không thuộc {PROVIDERS}")
    p = _state_path(state_dir, a.packet)
    if p.exists() and not a.force:
        _die(RC_USAGE, f"DA_TON_TAI: {p} — dùng --force nếu thật sự muốn dựng lại.")
    st = {
        "schema": SCHEMA,
        "packet": a.packet,
        "mission": a.mission,
        "executor": a.executor,
        "reviewer": a.reviewer,
        "state": "ready",
        "attempts": [],
        "findings": {},
        "pending_comments": [],
        "posted": [],
        "max_attempts": MAX_ATTEMPTS,
        "same_failure_limit": SAME_FAILURE_LIMIT,
    }
    _queue(st, f"Vòng lặp mở cho `wp{a.packet}` (mission #{a.mission}). "
               f"executor `{a.executor}` · reviewer `{a.reviewer}` — cross-provider đạt. "
               f"Trần: {MAX_ATTEMPTS} lượt review↔fix, same-failure-limit {SAME_FAILURE_LIMIT}. "
               f"Dừng cứng trước merge/deploy/LIVE.")
    _save(state_dir, st)
    print(json.dumps({"ok": True, "state": st["state"], "packet": a.packet}, ensure_ascii=False))
    return RC_OK


def cmd_begin_attempt(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    _require_posted(st)
    if st["state"] == "blocked":
        _die(RC_STOP, f"BLOCKED: wp{a.packet} đã dừng — cần người gỡ, không tự đi tiếp.")
    used = len(st["attempts"])
    if used >= st["max_attempts"]:
        st["state"] = "blocked"
        _queue(st, f"**DỪNG — chạm trần {st['max_attempts']} lượt review↔fix.** "
                   f"Đã dùng {used}/{st['max_attempts']}. Vòng lặp không tự đi tiếp; cần người quyết.")
        _save(state_dir, st)
        _die(RC_STOP, f"TRAN_LUOT: đã dùng {used}/{st['max_attempts']} lượt. DỪNG, báo người.")
    if a.provider != st["executor"]:
        _die(RC_PROVIDER,
             f"CROSS_PROVIDER_VI_PHAM: lượt executor phải do `{st['executor']}` chạy, "
             f"không phải `{a.provider}`.")
    st["attempts"].append({"n": used + 1, "role": "executor", "provider": a.provider})
    st["state"] = "running"
    _queue(st, f"Lượt **{used + 1}/{st['max_attempts']}** — executor `{a.provider}` bắt đầu.")
    _save(state_dir, st)
    print(json.dumps({"ok": True, "attempt": used + 1, "of": st["max_attempts"]}, ensure_ascii=False))
    return RC_OK


def cmd_void_attempt(a, state_dir: Path) -> int:
    """Trả lại lượt vừa mở khi nó chết vì quota/rate-limit, KHÔNG phải vì nội dung.

    §8 protocol: "Lỗi quota/rate-limit không tiêu thụ attempt nội dung". Không có lệnh
    này thì hai lần provider nghẹt là đủ đốt sạch trần 3 lượt trong khi executor chưa
    kịp sai lần nào — trần bảo vệ nhầm thứ nó phải bảo vệ.

    Bảng lý do là ALLOWLIST cố ý: không cho "vì tôi thấy lượt đó không đáng tính".
    """
    hop_le = {"quota", "rate_limit", "provider_error"}
    if a.reason not in hop_le:
        _die(RC_USAGE, f"LY_DO_LA: `{a.reason}` không thuộc {sorted(hop_le)}. "
                       "Lỗi NỘI DUNG thì phải tiêu thụ lượt.")
    st = _load(state_dir, a.packet)
    if not st["attempts"]:
        _die(RC_USAGE, "KHONG_CO_LUOT_DE_TRA.")
    bo = st["attempts"].pop()
    st["state"] = "ready"
    _queue(st, f"Lượt {bo['n']} ({bo['provider']}) **không tiêu thụ attempt** — lý do "
               f"`{a.reason}`, không phải lỗi nội dung (§8 protocol). "
               f"Còn {st['max_attempts'] - len(st['attempts'])}/{st['max_attempts']} lượt.")
    _save(state_dir, st)
    print(json.dumps({"ok": True, "attempts_used": len(st["attempts"])}, ensure_ascii=False))
    return RC_OK


def cmd_record_review(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    _require_posted(st)
    if st["state"] == "blocked":
        _die(RC_STOP, f"BLOCKED: wp{a.packet} đã dừng — cần người gỡ.")
    if a.provider != st["reviewer"]:
        _die(RC_PROVIDER,
             f"CROSS_PROVIDER_VI_PHAM: review phải do `{st['reviewer']}` chạy, "
             f"không phải `{a.provider}`.")
    if a.verdict == "approve":
        st["state"] = "awaiting_merge"
        _queue(st, f"Review `approve` bởi `{a.provider}`. "
                   f"**DỪNG trước merge** — vòng lặp hết quyền ở đây, cần chủ kho duyệt.")
        _save(state_dir, st)
        print(json.dumps({"ok": True, "state": st["state"]}, ensure_ascii=False))
        return RC_OK

    if not a.finding:
        _die(RC_USAGE, "THIEU_FINDING: verdict khác `approve` phải kèm ít nhất một --finding.")
    hit = []
    for text in a.finding:
        fp = _fingerprint(text)
        rec = st["findings"].setdefault(fp, {"count": 0, "text": text.strip()})
        rec["count"] += 1
        hit.append((fp, rec["count"], rec["text"]))
    st["state"] = "reviewing"
    lap = [f"`{fp}` ×{n}" for fp, n, _ in hit]
    _queue(st, f"Review `{a.verdict}` bởi `{a.provider}` — {len(hit)} finding: {', '.join(lap)}.")

    lap_limit = [(fp, n, t) for fp, n, t in hit if n >= st["same_failure_limit"]]
    if lap_limit:
        st["state"] = "blocked"
        chi_tiet = "; ".join(f"`{fp}` lặp {n} lần: {t[:120]}" for fp, n, t in lap_limit)
        _queue(st, f"**DỪNG — same-failure-limit {st['same_failure_limit']}.** {chi_tiet}. "
                   f"Cùng một lỗi lặp lại nghĩa là vòng lặp không sửa nổi nó; đốt thêm lượt là "
                   f"đốt ngân sách. Cần người.")
        _save(state_dir, st)
        _die(RC_STOP, f"SAME_FAILURE_LIMIT: {chi_tiet}")
    _save(state_dir, st)
    print(json.dumps({"ok": True, "state": st["state"],
                      "findings": [{"fp": fp, "count": n} for fp, n, _ in hit]},
                     ensure_ascii=False))
    return RC_OK


def cmd_guard(a, state_dir: Path) -> int:
    """Chặn cứng — KHÔNG đọc state, KHÔNG có cờ nới.

    Cố ý không nhận `--force`: một chốt có đường vòng là một chốt không tồn tại.
    Muốn merge/deploy thì người làm, ngoài vòng lặp.
    """
    ly_do = FORBIDDEN_ACTIONS.get(a.action)
    if ly_do is None:
        _die(RC_USAGE, f"HANH_VI_LA: `{a.action}` không có trong bảng. "
                       f"Biết: {sorted(FORBIDDEN_ACTIONS)}")
    _die(RC_STOP, f"CAM_TRONG_VONG_LAP: {ly_do}. Vòng lặp tự do tới TRƯỚC merge, không hơn — "
                  f"việc này do người làm sau khi duyệt.")
    return RC_STOP  # không tới được; giữ cho type-checker khỏi than


def cmd_mark_posted(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    if not st["pending_comments"]:
        _die(RC_USAGE, "KHONG_CO_GI_CHUA_DANG.")
    body = st["pending_comments"].pop(0)
    st["posted"].append({"url": a.url, "body": body})
    _save(state_dir, st)
    print(json.dumps({"ok": True, "con_lai": len(st["pending_comments"])}, ensure_ascii=False))
    return RC_OK


def cmd_status(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    print(json.dumps({
        "ok": st["state"] != "blocked",
        "packet": st["packet"], "state": st["state"],
        "attempts_used": len(st["attempts"]), "max_attempts": st["max_attempts"],
        "same_failure_limit": st["same_failure_limit"],
        "findings": {fp: r["count"] for fp, r in st["findings"].items()},
        "pending_comments": len(st["pending_comments"]),
        "executor": st["executor"], "reviewer": st["reviewer"],
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return RC_OK if st["state"] != "blocked" else RC_STOP


def cmd_where(a, state_dir: Path) -> int:
    """In đường dẫn state dir dưới dạng JSON ASCII — kênh KHÔNG MẤT MÁT.

    Không phải tiện ích: trên máy Windows này stdout/stderr qua pipe là **cp1258**, nên mọi
    chuỗi có dấu (kho nằm dưới `D:\\Quốc hội\\…`) bị méo khi bên đọc decode UTF-8. `json.dumps`
    mặc định `ensure_ascii=True` nên đường dẫn ra thành `\\uXXXX` — thuần ASCII, đọc lại đúng
    từng ký tự. Test dựa vào ĐÂY chứ không parse câu lỗi tiếng Việt.
    """
    sys.stdout.write(json.dumps({"state_dir": str(state_dir)}) + "\n")
    return RC_OK


def cmd_next_comment(a, state_dir: Path) -> int:
    st = _load(state_dir, a.packet)
    if not st["pending_comments"]:
        _die(RC_USAGE, "KHONG_CO_COMMENT_CHO_DANG.")
    sys.stdout.write(st["pending_comments"][0] + "\n")
    return RC_OK


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="packet_loop", description=__doc__.split("\n")[0])
    p.add_argument("--state-dir", default=None,
                   help="thư mục state; mặc định `.claude/dev/.state` cạnh script")
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("init"); q.set_defaults(fn=cmd_init)
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--mission", type=int, required=True)
    q.add_argument("--executor", required=True)
    q.add_argument("--reviewer", required=True)
    q.add_argument("--force", action="store_true")

    q = sub.add_parser("begin-attempt"); q.set_defaults(fn=cmd_begin_attempt)
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--provider", required=True)

    q = sub.add_parser("record-review"); q.set_defaults(fn=cmd_record_review)
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--provider", required=True)
    q.add_argument("--verdict", required=True,
                   choices=["approve", "changes_requested", "blocked"])
    q.add_argument("--finding", action="append", default=[])

    q = sub.add_parser("void-attempt"); q.set_defaults(fn=cmd_void_attempt)
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--reason", required=True)

    q = sub.add_parser("guard"); q.set_defaults(fn=cmd_guard)
    q.add_argument("--action", required=True)

    q = sub.add_parser("mark-posted"); q.set_defaults(fn=cmd_mark_posted)
    q.add_argument("--packet", type=int, required=True)
    q.add_argument("--url", required=True)

    q = sub.add_parser("status"); q.set_defaults(fn=cmd_status)
    q.add_argument("--packet", type=int, required=True)

    q = sub.add_parser("next-comment"); q.set_defaults(fn=cmd_next_comment)
    q.add_argument("--packet", type=int, required=True)

    sub.add_parser("where").set_defaults(fn=cmd_where)
    return p


def main(argv=None) -> int:
    a = build_parser().parse_args(argv)
    # `.tl_state` chứ không phải `.state`: tên NÀY đã được `.gitignore:22` phủ sẵn (doctrine
    # v1.34.2 — "runtime artifact, không vào repo/manifest"). Đo rồi mới đổi: bản đầu dùng
    # `.state` làm `git status` bẩn ngay lượt chạy đầu tiên, mà trong kho này cây bẩn kéo theo
    # cả gate. Chữa bằng cách tái dùng tên đã ignore, KHÔNG sửa `.gitignore` — path đó nằm
    # ngoài write-set của packet.
    state_dir = Path(a.state_dir) if a.state_dir else Path(__file__).resolve().parent / ".tl_state"
    return a.fn(a, state_dir)


if __name__ == "__main__":
    sys.exit(main())
