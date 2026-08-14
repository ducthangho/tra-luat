#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đo LỖ loại trừ phiên của `packet_loop.py` — successor `packet-session-mutex`.

Đo TRƯỚC khi vá, cùng doctrine với AC 18 của wp55: một lỗ chưa đo được thì bản vá
chỉ là niềm tin. Ba hình dạng, mỗi cái một phép thử chạy được.

    H1  hai tiến trình ĐỒNG THỜI cùng mở lượt trên CÙNG state-dir
    H2  hai phiên KHÁC container: không có state dùng chung nào
    H3  lease không mang định danh PHIÊN đang giữ

Dùng: python3 probe_mutex.py <đường-dẫn-packet_loop.py>
"""
import json
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

PL = Path(sys.argv[1]).resolve()
PKT = 9100


def _han_sau(gio=4):
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc) + timedelta(hours=gio)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _dung_state(sd: Path):
    subprocess.run([sys.executable, str(PL), "--state-dir", str(sd), "init",
                    "--packet", str(PKT), "--mission", "54",
                    "--executor", "claude", "--reviewer", "codex"],
                   capture_output=True, check=True)
    subprocess.run([sys.executable, str(PL), "--state-dir", str(sd), "record-lease",
                    "--packet", str(PKT), "--lease-id", "wp9100-mutex-probe",
                    "--granted-by", "ducthangho", "--evidence",
                    "https://github.com/o/r/issues/9100#issuecomment-1234567890",
                    "--expires-utc", _han_sau()],
                   capture_output=True, check=True)


def h1(n=8) -> None:
    """N tiến trình cùng gọi `begin-attempt` một lúc. ĐÚNG phải có ĐÚNG MỘT cái thắng."""
    print("### H1 · đồng thời mở lượt trên CÙNG state-dir")
    with tempfile.TemporaryDirectory() as td:
        sd = Path(td) / "st"
        sd.mkdir(parents=True)
        _dung_state(sd)

        rao = threading.Barrier(n)
        ket = [None] * n

        def chay(i):
            rao.wait()          # ép N tiến trình xuất phát cùng lúc
            p = subprocess.run(
                [sys.executable, str(PL), "--state-dir", str(sd), "begin-attempt",
                 "--packet", str(PKT), "--provider", "claude"],
                capture_output=True)
            ket[i] = p.returncode

        ts = [threading.Thread(target=chay, args=(i,)) for i in range(n)]
        [t.start() for t in ts]
        [t.join() for t in ts]

        thang = [i for i, rc in enumerate(ket) if rc == 0]
        st = json.loads((sd / f"wp{PKT}.json").read_text(encoding="utf-8"))
        print(f"  tiến trình chạy      : {n}")
        print(f"  số cái THẮNG (rc=0)  : {len(thang)}   ← ĐÚNG phải là 1")
        print(f"  attempts_used ghi lại: {st['attempts_used']}   ← ĐÚNG phải bằng số cái thắng")
        print(f"  history có {len(st['history'])} mục begin_attempt: "
              f"{sum(1 for h in st['history'] if h.get('event') == 'begin_attempt')}")
        if len(thang) > 1:
            print(f"  ⇒ LỖ: {len(thang)} lượt mở song song trên MỘT packet")
        if st["attempts_used"] < len(thang):
            print(f"  ⇒ LỖ NẶNG HƠN: đếm THIẾU {len(thang) - st['attempts_used']} lượt "
                  f"(ghi đè mù) ⇒ TRẦN attempt bị vô hiệu")
        print()


def h2() -> None:
    """Hai phiên khác container = hai state-dir rời nhau, không có gì nối chúng."""
    print("### H2 · hai phiên KHÁC container")
    with tempfile.TemporaryDirectory() as td:
        a, b = Path(td) / "phienA", Path(td) / "phienB"
        for sd in (a, b):
            sd.mkdir(parents=True)
            _dung_state(sd)
            subprocess.run([sys.executable, str(PL), "--state-dir", str(sd), "begin-attempt",
                            "--packet", str(PKT), "--provider", "claude"], capture_output=True)
        sa = json.loads((a / f"wp{PKT}.json").read_text(encoding="utf-8"))
        sb = json.loads((b / f"wp{PKT}.json").read_text(encoding="utf-8"))
        print(f"  phiên A: state={sa['state']!r} attempts_used={sa['attempts_used']}")
        print(f"  phiên B: state={sb['state']!r} attempts_used={sb['attempts_used']}")
        print("  ⇒ LỖ: cả hai cùng 'running', mỗi phiên tin mình là duy nhất. "
              "Không có khoá nào để hỏi.")
        print("  ⇒ state KHÔNG nằm trong kho ⇒ không có nguồn chung để loại trừ.")
        print()


def h3() -> None:
    """Lease định danh LƯỢT, không định danh PHIÊN đang giữ lượt."""
    print("### H3 · lease không mang định danh phiên")
    with tempfile.TemporaryDirectory() as td:
        sd = Path(td) / "st"
        sd.mkdir(parents=True)
        _dung_state(sd)
        st = json.loads((sd / f"wp{PKT}.json").read_text(encoding="utf-8"))
        khoa = sorted(st["lease"].keys())
        print(f"  khoá trong lease: {khoa}")
        co = [k for k in khoa if "session" in k or "holder" in k or "phien" in k]
        print(f"  khoá định danh phiên: {co or 'KHÔNG CÓ'}")
        print("  ⇒ LỖ: hai phiên cùng cầm một `lease_id` hợp lệ là trạng thái "
              "KHÔNG phân biệt được với một phiên.")
        print()


if __name__ == "__main__":
    print(f"đo trên: {PL}\n")
    h1()
    h2()
    h3()
