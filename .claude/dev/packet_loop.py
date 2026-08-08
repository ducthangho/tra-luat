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

# Kho mà transition được phép ghi vào. Không suy ra từ `git remote` cho có vẻ tổng quát:
# reviewer chạy trong sandbox KHÔNG phải kho git, và một chốt chỉ hoạt động khi có kho thì
# không phải chốt. Hằng số ở đây là deterministic và đọc được bằng mắt.
REPO = "ducthangho/tra-luat"

# Máy trạng thái THẬT SỰ là một máy trạng thái. Cross-review vòng 2 (provider codex) bắt
# được: bản trước chỉ kiểm `blocked`, nên `approve` chạy được từ `ready` khi CHƯA có lượt
# nào (rc=0, `attempts_used=0`), và `begin-attempt` mở lại được từ `awaiting_merge` — tức
# packet đã duyệt xong vẫn quay lại chạy tiếp. Bảng dưới đây là nguồn duy nhất cho câu hỏi
# "lệnh này được phép chạy từ trạng thái nào".
TRANSITION_HOP_LE = {
    # `reviewing` = vừa bị `changes_requested`, executor được mở lượt sửa tiếp.
    "begin-attempt": ("ready", "reviewing"),
    # Chỉ review được thứ ĐANG chạy. Chặn `approve` khi chưa ai làm gì, và chặn review lại
    # một packet đã `awaiting_merge`.
    "record-review": ("running",),
    # Chỉ trả được lượt CHƯA bị review. Sau `record-review` thì lượt đó đã tiêu thụ nội
    # dung — vòng 2 chỉ ra chuỗi `begin-attempt → record-review → void-attempt` lặp ba lần
    # làm `attempts_used` đứng yên ở 1, tức trần 3 lượt vô hiệu bằng lối khác.
    "void-attempt": ("running",),
}


def _kiem_transition(st: dict, lenh: str) -> None:
    if st["state"] == "blocked":
        _die(RC_STOP, f"BLOCKED: wp{st['packet']} đã dừng — cần người gỡ, không tự đi tiếp.")
    hop_le = TRANSITION_HOP_LE[lenh]
    if st["state"] not in hop_le:
        _die(RC_STOP, f"TRANSITION_LA: `{lenh}` không chạy được từ state `{st['state']}` "
                      f"(chỉ từ {list(hop_le)}).")


def _fingerprint(text: str) -> str:
    """Vân tay nội dung của một finding.

    Chuẩn hoá trước khi băm để "cùng một lỗi, diễn đạt lệch vài khoảng trắng / hoa
    thường / dấu câu" vẫn đếm là MỘT. Không cố làm ngữ nghĩa — chỉ cần đủ để trần đếm
    đúng thứ nó hứa đếm; reviewer diễn đạt lại hoàn toàn thì đó là finding khác, và test
    `case_finding_khac_nhau_khong_bi_chan` khoá đúng hành vi đó.

    Chuẩn hoá đi qua HAI lần sửa, và lần thứ hai là hồi quy do chính lần thứ nhất:

    · vòng 1 (codex): `"manifest lech"` vs `"manifest lech."` ra HAI vân tay ⇒ trần
      same-failure lách được chỉ bằng một dấu chấm, kể cả khi không ai cố tình.
    · vòng 2 (codex): bản vá xoá SẠCH ký tự không phải chữ/số thì `state == blocked` và
      `state != blocked` ra CÙNG vân tay ⇒ hai finding thật sự khác nhau bị gộp, vòng lặp
      chết oan ở lượt 2. Chặt một chiều mà hỏng chiều kia thì tệ hơn là không sửa.

    Nên chỉ bỏ dấu câu CÂU và ký tự trích dẫn; giữ nguyên TOÁN TỬ. Đặc biệt KHÔNG bỏ `!`:
    bỏ nó thì `a != b` thành `a = b`, trùng luôn với `a = b` — đúng lớp lỗi vừa sửa.
    """
    bo = set(".,;:?\"'`()[]{}«»“”‘’")
    sach = "".join(" " if c in bo else c for c in text.casefold())
    return hashlib.sha256(re.sub(r"\s+", " ", sach).strip().encode("utf-8")).hexdigest()[:12]


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


def _kiem_url_comment(url: str, packet: int, da_dung: set) -> None:
    """Bắt buộc URL comment là thật, thuộc ĐÚNG kho + ĐÚNG Issue, và CHƯA từng dùng.

    Ba lớp, mỗi lớp do một lượt review chéo bắt được:

    · vòng 1: `--url https://example.invalid/not-posted` rc=0 rồi advance được ⇒ "dấu vết
      bền" chỉ cần một chuỗi bất kỳ.
    · vòng 2: bản vá đầu dùng `[\\w.-]+` cho owner/repo, mà `.` nằm trong lớp đó nên
      `https://github.com/../repo/issues/205#issuecomment-1` LỌT, và repo của người khác
      (`attacker/repo`) cũng lọt. Nay ghim thẳng `REPO` — transition của packet này chỉ có
      một chỗ hợp lệ để nằm.
    · vòng 2: MỘT url tái dùng cho HAI body khác nhau đều rc=0 ⇒ `mark-posted` không chứng
      minh được body nào đã đăng. Nay một URL chỉ tiêu thụ được một comment.

    Vẫn không xác minh comment CÓ THẬT trên GitHub (script cố ý không chạm mạng) — nhưng ba
    lớp trên đã loại sạch lớp "gõ đại cho qua".
    """
    mau = re.compile(r"\Ahttps://github\.com/" + re.escape(REPO)
                     + r"/(?:issues|pull)/(\d+)#issuecomment-(\d+)\Z")
    m = mau.match(url)
    if not m:
        _die(RC_USAGE, f"URL_COMMENT_LA: `{url}` không đúng dạng "
                       f"`https://github.com/{REPO}/issues/<n>#issuecomment-<id>`.")
    if int(m.group(1)) != packet:
        _die(RC_USAGE, f"URL_SAI_ISSUE: comment trỏ Issue #{m.group(1)} nhưng packet là "
                       f"wp{packet}. Transition phải ghi vào ĐÚNG Issue của packet.")
    if url in da_dung:
        _die(RC_USAGE, f"URL_TAI_DUNG: `{url}` đã dùng cho một comment khác. "
                       "Mỗi transition là một comment riêng — một URL không chứng minh được hai body.")


def cmd_init(a, state_dir: Path) -> int:
    if a.executor == a.reviewer:
        _die(RC_PROVIDER,
             f"CROSS_PROVIDER_VI_PHAM: executor và reviewer cùng là `{a.executor}`. "
             "Quy tắc: executor claude => reviewer codex, và ngược lại.")
    for who, prov in (("executor", a.executor), ("reviewer", a.reviewer)):
        if prov not in PROVIDERS:
            _die(RC_USAGE, f"PROVIDER_LA: {who}=`{prov}` không thuộc {PROVIDERS}")
    p = _state_path(state_dir, a.packet)
    if p.exists():
        # KHÔNG có `--force`. Review chéo vòng 1 (provider codex) bắt được: `init --force`
        # xoá sạch lịch sử VÀ đổi được vai, nên executor cũ tự review chính việc mình vừa
        # làm — vừa lách cross-provider vừa reset trần. Dựng lại vòng lặp là hành vi của
        # NGƯỜI: xoá tệp state bằng tay, một việc nhìn thấy được, không phải một cờ.
        _die(RC_USAGE, f"DA_TON_TAI: {p}. Vòng lặp đang chạy thì KHÔNG dựng lại được — "
                       "muốn bắt đầu lại thì người xoá tệp state bằng tay.")
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
    _kiem_transition(st, "begin-attempt")
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
    # Ba chốt, do hai lượt review chéo bắt được — đây là lệnh bị đục nhiều nhất:
    # · vòng 1: nó bỏ qua `_require_posted` VÀ đặt state về `ready`, nên sau khi chạm trần
    #   (`begin-attempt` rc=3, state `blocked`) chỉ cần gọi nó một lần là GỠ ĐƯỢC blocked.
    # · vòng 2: nó vẫn chạy được từ `reviewing`, tức hoàn lại một lượt ĐÃ bị review — chuỗi
    #   `begin-attempt → record-review → void-attempt` lặp mãi mà `attempts_used` đứng yên.
    # `_kiem_transition` bịt cả hai: chỉ `running` mới trả lượt được, và `blocked` thì dừng.
    _require_posted(st)
    _kiem_transition(st, "void-attempt")
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
    _kiem_transition(st, "record-review")
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
    if a.verdict == "blocked":
        # Review chéo vòng 1 (provider codex): bản đầu coi `blocked` y hệt
        # `changes_requested` ⇒ reviewer nói "blocked, cần người" mà state vẫn `reviewing`
        # và vòng lặp chạy tiếp như không có gì. Verdict mạnh nhất mà không có hiệu lực
        # thì reviewer mất đúng cái phanh của mình.
        for text in a.finding:
            fp = _fingerprint(text)
            rec = st["findings"].setdefault(fp, {"count": 0, "text": text.strip()})
            rec["count"] += 1
        st["state"] = "blocked"
        _queue(st, f"**DỪNG — reviewer `{a.provider}` ra verdict `blocked`.** "
                   f"{'; '.join(t.strip()[:160] for t in a.finding)}. Cần người quyết.")
        _save(state_dir, st)
        _die(RC_STOP, "VERDICT_BLOCKED: reviewer yêu cầu dừng, không tự đi tiếp.")
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
    _kiem_url_comment(a.url, a.packet, {p["url"] for p in st["posted"]})
    if not st["pending_comments"]:
        _die(RC_USAGE, "KHONG_CO_GI_CHUA_DANG.")
    # FIFO — `pop(0)`, KHÔNG phải `pop()`. Comment phải khớp đúng transition sinh ra nó;
    # lấy từ cuối là gán nhầm URL cho body, và audit trail gán nhầm còn tệ hơn không có.
    # Cross-review vòng 2 chỉ ra suite chưa khoá thứ tự này (mutation `pop(0)→pop()` sống sót).
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
