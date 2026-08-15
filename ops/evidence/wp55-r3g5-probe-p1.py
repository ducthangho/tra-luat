#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe BỐN finding P1 của verdict lượt 6 (codex, lease wp55-r3-review-6-codex-20260814).

Chạy: python3 probe-p1.py <đường dẫn packet_loop.py>
Đọc rc THẬT của TỪNG lệnh, không qua pipe.

    ok    hành vi ĐÚNG như yêu cầu sau khi vá
    LOI   còn sai
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(sys.argv[1]).resolve()

SACH = ("# Adapter demo\n\n**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §13.\n\n"
        "Dưới đây chỉ có cú pháp của nền.\n")


def run(args, state_dir=None):
    cmd = [sys.executable, "-B", str(SCRIPT)]
    if state_dir is not None:
        cmd += ["--state-dir", str(state_dir)]
    cmd += [str(a) for a in args]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout, p.stderr


def repo_gia(tmp: Path, noi_dung: str, ten: str) -> Path:
    r = tmp / ten
    (r / ".claude" / "skills" / "x").mkdir(parents=True, exist_ok=True)
    (r / ".claude" / "skills" / "x" / "SKILL.md").write_text(noi_dung, encoding="utf-8")
    return r


def han_tuong_lai(gio=4):
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc) + timedelta(hours=gio)).strftime("%Y-%m-%dT%H:%M:%SZ")


def dung_toi_reviewing(sd, head="a" * 40):
    """init → record-lease → begin-attempt → transition reviewing. Trả rc từng bước."""
    b = []
    b.append(("init", run(["init", "--packet", 55, "--mission", 54,
                           "--executor", "claude", "--reviewer", "codex"], sd)[0]))
    b.append(("record-lease", run(["record-lease", "--packet", 55, "--lease-id", "wp55-probe",
                                   "--granted-by", "ducthangho",
                                   "--evidence", "https://github.com/o/r/issues/55#issuecomment-1",
                                   "--expires-utc", han_tuong_lai()], sd)[0]))
    b.append(("begin-attempt", run(["begin-attempt", "--packet", 55,
                                    "--provider", "claude"], sd)[0]))
    b.append(("record-post", run(["record-post", "--packet", 55, "--for", "reviewing",
                                  "--comment-id", "7770000001"], sd)[0]))
    b.append(("transition-reviewing", run(["transition", "--packet", 55, "--to", "reviewing",
                                           "--comment-id", "7770000001",
                                           "--head-sha", head], sd)[0]))
    return b


def state(sd):
    return json.loads((sd / "wp55.json").read_text(encoding="utf-8"))


KQ = []


def ghi(pid, ten, dat, chi_tiet):
    KQ.append((pid, ten, dat, chi_tiet))
    print(f"{'ok ' if dat else 'LOI'}  {pid:<6} {ten:<46} {chi_tiet}")


def p1_transition_bypass(tmp):
    """F1 · reviewing→running bằng `transition` phải bị CHẶN."""
    sd = tmp / "f1_sd"
    sd.mkdir(parents=True, exist_ok=True)
    dung_toi_reviewing(sd)
    rc_post, _, _ = run(["record-post", "--packet", 55, "--for", "running",
                         "--comment-id", "7770000002"], sd)
    rc_back, _, _ = run(["transition", "--packet", 55, "--to", "running",
                         "--comment-id", "7770000002"], sd)
    st = state(sd)
    ghi("F1", "reviewing→running qua transition bị chặn", rc_back != 0,
        f"back_to_running_rc={rc_back} (đòi != 0) · state={st['state']} · "
        f"attempts_used={st['attempts_used']} · reviews={len(st['reviews'])}")
    return rc_back


def p1_void_attempt_zero(tmp):
    """F2 · void-attempt phải trả state về chạy được; record-review phải đòi lượt đang mở."""
    sd = tmp / "f2_sd"
    sd.mkdir(parents=True, exist_ok=True)
    dung_toi_reviewing(sd)
    rc_void, _, _ = run(["void-attempt", "--packet", 55, "--reason", "quota"], sd)
    st1 = state(sd)
    rc_begin, _, _ = run(["begin-attempt", "--packet", 55, "--provider", "claude"], sd)
    ghi("F2a", "sau void-attempt, begin-attempt KHÔNG kẹt cứng", rc_void == 0 and rc_begin == 0,
        f"void_rc={rc_void} · attempts_used_sau_void={st1['attempts_used']} · "
        f"state_sau_void={st1['state']} · begin_rc={rc_begin} (đòi 0)")

    # Đường thứ hai: void rồi ghi review approve NGAY, không mở lượt lại.
    sd2 = tmp / "f2b_sd"
    sd2.mkdir(parents=True, exist_ok=True)
    dung_toi_reviewing(sd2)
    run(["void-attempt", "--packet", 55, "--reason", "quota"], sd2)
    rc_rev, _, _ = run(["record-review", "--packet", 55, "--provider", "codex",
                        "--verdict", "approve", "--reviewed-sha", "a" * 40], sd2)
    st2 = state(sd2)
    so_luot = st2["reviews"][0]["attempt"] if st2["reviews"] else None
    ghi("F2b", "record-review KHÔNG duyệt được bằng lượt số 0",
        rc_rev != 0 and st2["state"] != "accepted",
        f"record_review_rc={rc_rev} (đòi != 0) · state={st2['state']} "
        f"(đòi != accepted) · reviews[0].attempt={so_luot}")
    return rc_void, rc_begin, rc_rev


CA_DOCTRINE = [
    # (id, mô tả, nội dung bơm, rc ĐÚNG)
    ("F3a", "quoted angle `<span title=\">\">` phải BẮT",
     'Ghi chú: mer<span title=">">ged:</span> PR đã vào nhánh đích', 6),
    ("F3b", "nền: tag thường `<span title=\"x\">` vẫn BẮT",
     'Ghi chú: mer<span title="x">ged:</span> PR đã vào nhánh đích', 6),
    ("F3c", "nền: ASCII nguyên văn vẫn BẮT",
     "Ghi chú: merged: PR đã vào nhánh đích", 6),
    ("F4a", "heading TRẦN chép nguyên cụm phải BẮT",
     "## Người có thẩm quyền", 6),
    ("F4b", "dòng TRẦN chép nguyên cụm phải BẮT",
     "Người có thẩm quyền", 6),
    ("F4c", "ô BẢNG chép cụm vẫn BẮT (không lùi)",
     "| Người có thẩm quyền | vai trò cấp lease |", 6),
    ("F4d", "BẮT OAN: văn xuôi kể lại kết quả đo phải THA",
     "Đo ở `v1.36.68` (PR #104): ba tên tấn công `rc=0` → `rc=4`, người có\n"
     "thẩm quyền vẫn `rc=0`. Kèm chốt: đột biến nới danh sách phải làm ca đích ĐỎ.", 0),
    ("F4e", "BẮT OAN: cụm giữa câu văn xuôi phải THA",
     "Chỉ người có thẩm quyền mới cấp được lease; phiên worker thì không.", 0),
]


def p1_doctrine(tmp):
    for pid, ten, nd, doi in CA_DOCTRINE:
        r = repo_gia(tmp, SACH + "\n" + nd + "\n", ten=f"d_{pid}")
        rc, _, _ = run(["doctrine-scan", "--root", str(r)])
        ghi(pid, ten, rc == doi, f"rc={rc} (đòi {doi})")


def main():
    with tempfile.TemporaryDirectory(prefix="probe_p1_") as td:
        tmp = Path(td)
        print(f"probe P1 · script={SCRIPT}")
        print("-" * 100)
        p1_transition_bypass(tmp)
        p1_void_attempt_zero(tmp)
        p1_doctrine(tmp)
    print("-" * 100)
    dat = sum(1 for *_, d, _ in KQ if d)
    print(f"đạt {dat}/{len(KQ)}")
    return 0 if dat == len(KQ) else 1


if __name__ == "__main__":
    sys.exit(main())
