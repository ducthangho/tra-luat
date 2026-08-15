#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ma trận CODEPAGE — AC 14. Sinh từ DANH SÁCH LỆNH CON THẬT (duyệt parser).

Liệt kê tay là thứ vừa để lọt `void-attempt`. Ở đây danh sách lệnh con lấy
THẲNG từ `build_parser()` của chính tệp đang đo, nên thêm một lệnh con mới mà
quên ma trận thì phép đo này ĐỎ chứ không im lặng.

Chạy: python3 probe-codepage.py <đường dẫn packet_loop.py>
"""
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(sys.argv[1]).resolve()

SACH = ("# Adapter demo\n\n**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §13.\n\n"
        "Dưới đây chỉ có cú pháp của nền.\n")

# Lệnh con CỐ Ý không in stdout khi thành công. Khai TƯỜNG MINH kèm lý do, và
# phép đo dưới đây CHỨNG MINH lời khai (đòi stdout rỗng + rc khác 0).
KHONG_CO_STDOUT = {"guard": "luôn _die(RC_GUARD) — chỉ ghi stderr, không có đường thành công"}


def liet_ke_lenh_con(script: Path):
    """Duyệt parser THẬT, không liệt kê tay."""
    spec = importlib.util.spec_from_file_location("pl_probe", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    import argparse
    ten = []
    for act in mod.build_parser()._actions:
        if isinstance(act, argparse._SubParsersAction):
            ten.extend(act.choices.keys())
    return sorted(ten)


def han_tuong_lai(gio=4):
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc) + timedelta(hours=gio)).strftime("%Y-%m-%dT%H:%M:%SZ")


def kich_ban(sd, repo):
    """Mỗi phần tử: (tên lệnh con, argv). Phủ MỌI lệnh con có stdout."""
    sha = "%040x" % 1
    return [
        ("where", ["where"], None),
        ("init", ["init", "--packet", "55", "--mission", "54",
                  "--executor", "claude", "--reviewer", "codex"], sd),
        ("record-lease", ["record-lease", "--packet", "55", "--lease-id", "wp55-cp",
                          "--granted-by", "ducthangho",
                          "--evidence", "https://github.com/o/r/issues/55#issuecomment-1",
                          "--expires-utc", han_tuong_lai()], sd),
        ("begin-attempt", ["begin-attempt", "--packet", "55", "--provider", "claude"], sd),
        # void-attempt in stdout tiếng Việt ("đã hoàn một lượt vì …") — ĐÂY LÀ
        # LỆNH MA TRẬN CŨ BỎ SÓT. Hoàn rồi mở lại để kịch bản đi tiếp.
        ("void-attempt", ["void-attempt", "--packet", "55", "--reason", "quota"], sd),
        ("__mo_lai", ["begin-attempt", "--packet", "55", "--provider", "claude"], sd),
        ("next-comment", ["next-comment", "--packet", "55"], sd),
        ("record-post", ["record-post", "--packet", "55", "--for", "reviewing",
                         "--comment-id", "7770000009"], sd),
        ("transition", ["transition", "--packet", "55", "--to", "reviewing",
                        "--comment-id", "7770000009", "--head-sha", sha], sd),
        ("record-review", ["record-review", "--packet", "55", "--provider", "codex",
                           "--verdict", "changes_requested", "--reviewed-sha", sha,
                           "--finding-id", "loi-co-dau-tieng-viet",
                           "--finding-desc", "mô tả có dấu tiếng Việt"], sd),
        ("status", ["status", "--packet", "55"], sd),
        ("doctrine-scan", ["doctrine-scan", "--root", str(repo)], None),
    ]


def run(args, sd, env_extra):
    import os
    cmd = [sys.executable, "-B", str(SCRIPT)]
    if sd is not None:
        cmd += ["--state-dir", str(sd)]
    cmd += [str(a) for a in args]
    env = dict(os.environ)
    env.update(env_extra)
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    return p.returncode, p.stdout, p.stderr


def main():
    tat_ca = liet_ke_lenh_con(SCRIPT)
    print(f"probe CODEPAGE · script={SCRIPT}")
    print(f"lệnh con THẬT trong parser ({len(tat_ca)}): {', '.join(tat_ca)}")

    can_do = [t for t in tat_ca if t not in KHONG_CO_STDOUT]
    print(f"cần có stdout ({len(can_do)}): {', '.join(can_do)}")
    for t, ly_do in KHONG_CO_STDOUT.items():
        print(f"khai KHÔNG stdout: {t} — {ly_do}")
    print("-" * 100)

    loi = 0
    with tempfile.TemporaryDirectory(prefix="probe_cp_") as td:
        tmp = Path(td)

        # 1. Lời khai "guard không có stdout" phải được CHỨNG MINH, không tin suông.
        for t in KHONG_CO_STDOUT:
            rc, o, e = run([t, "--action", "merge"], None, {"PYTHONIOENCODING": "cp1252"})
            dat = rc != 0 and not o.strip()
            print(f"{'ok ' if dat else 'LOI'}  chứng minh {t!r} không có stdout: "
                  f"rc={rc} stdout={'rỗng' if not o.strip() else 'CÓ'}")
            loi += 0 if dat else 1

        # 2. Ma trận thật.
        for cp in ("cp1252", "cp1258"):
            sd = tmp / f"sd_{cp}"
            sd.mkdir(parents=True, exist_ok=True)
            repo = tmp / f"repo_{cp}"
            (repo / ".claude" / "skills" / "x").mkdir(parents=True, exist_ok=True)
            (repo / ".claude" / "skills" / "x" / "SKILL.md").write_text(SACH, encoding="utf-8")

            phu = set()
            for ten, args, sdir in kich_ban(sd, repo):
                rc, o, e = run(args, sdir, {"PYTHONIOENCODING": cp})
                if ten.startswith("__"):
                    continue
                phu.add(ten)
                dat = rc == 0 and bool(o.strip())
                if not dat:
                    loi += 1
                print(f"{'ok ' if dat else 'LOI'}  [{cp}] {ten:<16} rc={rc} "
                      f"stdout={'có' if o.strip() else 'RỖNG'}"
                      + ("" if dat else f" stderr={e.strip()[:120]!r}"))

            thieu = [t for t in can_do if t not in phu]
            if thieu:
                loi += len(thieu)
                print(f"LOI  [{cp}] ma trận BỎ SÓT lệnh con: {thieu}")
            else:
                print(f"ok   [{cp}] ma trận phủ ĐỦ {len(phu)}/{len(can_do)} lệnh con có stdout")
        print("-" * 100)
        print(f"{'ĐẠT' if loi == 0 else f'{loi} lỗi'}")
    return 0 if loi == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
