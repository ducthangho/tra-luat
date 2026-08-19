#!/usr/bin/env python3
"""Exec-form bridge cho SessionStart: đọc env trước, tìm bash CHẠY ĐƯỢC, rồi gọi hook.

Không dùng shell để khởi động bridge. Trên Windows, `bash` đầu PATH có thể là WSL
shim trả Access denied trong khi Git Bash tốt vẫn tồn tại ở Program Files.
(Xem docs/incidents/2026-08-15-launcher-codex-github-toolchain.md — nguyên nhân
gốc số 4; cùng họ bài học t106 của launcher: binary hỏng đầu PATH không được che
binary tốt phía sau.)

Port từ nhánh codex/gate-lifecycle đã khai tử (blob ea85526b, tag
archive/codex-gate-lifecycle-ec8d08c) qua packet GLS-B1. Khác bản gốc HAI điểm,
đều khai:
1. Trần thời gian chạy hook đọc từ TL_HOOK_TIMEOUT_GIAY (mặc định 600) để
   phản chứng rc=124 đo được trong test mà không chờ 10 phút.
2. Tra env KHÔNG phân biệt hoa thường (`_lay_env`): bản gốc `env.get("ProgramFiles")`
   LUÔN trượt trên Windows vì `dict(os.environ)` viết hoa khoá thành `PROGRAMFILES`,
   nên fallback Program Files chạy bằng default cứng bất kể env — bug tiềm ẩn vô
   hình ở production (default trùng thực tế) mà t124 spawn thật bắt được.
Chốt tương ứng: t122–t127 trong .claude/dev/launcher_test.py.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def _lay_env(env: dict[str, str], ten: str, mac_dinh: str = "") -> str:
    """Tra env không phân biệt hoa thường — `dict(os.environ)` Windows viết hoa khoá."""
    if ten in env:
        return env[ten]
    for k, v in env.items():
        if k.upper() == ten.upper():
            return v
    return mac_dinh


def _ung_vien_bash(env: dict[str, str]) -> list[str]:
    ra: list[str] = []

    def them(x) -> None:
        if not x:
            return
        s = str(x)
        if os.path.normcase(os.path.abspath(s)) not in {
                os.path.normcase(os.path.abspath(y)) for y in ra}:
            ra.append(s)

    for muc in _lay_env(env, "PATH").split(os.pathsep):
        if muc:
            try:
                them(shutil.which("bash", path=muc))
            except OSError:
                pass
    if platform.system() == "Windows":
        pf = _lay_env(env, "ProgramFiles", r"C:\Program Files")
        them(Path(pf) / "Git" / "bin" / "bash.exe")
        them(Path(pf) / "Git" / "usr" / "bin" / "bash.exe")
    return [x for x in ra if Path(x).is_file()]


def _tran_giay(env: dict[str, str]) -> float:
    """Trần chạy hook. Sai/âm/rỗng thì về 600 — bridge chẩn đoán không được chết vì config."""
    try:
        v = float(env.get("TL_HOOK_TIMEOUT_GIAY", "") or 600)
    except ValueError:
        return 600.0
    return v if v > 0 else 600.0


def main() -> int:
    env = dict(os.environ)  # PHẢI là thao tác runtime đầu tiên, trước resolve/probe
    env["TL_LAUNCHER_ENV_DA_DOC"] = "1"
    project = Path(env.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
    script = project / ".claude" / "hooks" / "session-start.sh"
    if not script.is_file():
        print(f"[session-start] HONG: khong thay hook {script}")
        return 12
    loi = []
    for bash in _ung_vien_bash(env):
        try:
            probe = subprocess.run([bash, "--version"], stdin=subprocess.DEVNULL,
                                   capture_output=True, text=True, env=env, timeout=5,
                                   encoding="utf-8", errors="replace")
        except (OSError, subprocess.SubprocessError) as e:
            loi.append(f"{bash}: {type(e).__name__}")
            continue
        if probe.returncode != 0 or not ((probe.stdout or "") + (probe.stderr or "")).strip():
            loi.append(f"{bash}: rc={probe.returncode}")
            continue
        try:
            return subprocess.run([bash, str(script)], cwd=project, env=env,
                                  stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
                                  timeout=_tran_giay(env)).returncode
        except subprocess.TimeoutExpired:
            print("[session-start] HONG: hook vuot han "
                  f"{_tran_giay(env):g}s")
            return 124
        except OSError as e:
            loi.append(f"{bash}: {type(e).__name__}")
    print("[session-start] HONG: khong co bash chay duoc; " + "; ".join(loi[:3]))
    return 12


if __name__ == "__main__":
    sys.exit(main())
