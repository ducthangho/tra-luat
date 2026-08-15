#!/usr/bin/env python3
"""Exec-form bridge cho SessionStart: đọc env trước, tìm bash CHẠY ĐƯỢC, rồi gọi hook.

Không dùng shell để khởi động bridge. Trên Windows, `bash` đầu PATH có thể là WSL
shim trả Access denied trong khi Git Bash tốt vẫn tồn tại ở Program Files.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def _ung_vien_bash(env: dict[str, str]) -> list[str]:
    ra: list[str] = []

    def them(x) -> None:
        if not x:
            return
        s = str(x)
        if os.path.normcase(os.path.abspath(s)) not in {
                os.path.normcase(os.path.abspath(y)) for y in ra}:
            ra.append(s)

    for muc in env.get("PATH", "").split(os.pathsep):
        if muc:
            try:
                them(shutil.which("bash", path=muc))
            except OSError:
                pass
    if platform.system() == "Windows":
        pf = env.get("ProgramFiles", r"C:\Program Files")
        them(Path(pf) / "Git" / "bin" / "bash.exe")
        them(Path(pf) / "Git" / "usr" / "bin" / "bash.exe")
    return [x for x in ra if Path(x).is_file()]


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
                                  timeout=600).returncode
        except subprocess.TimeoutExpired:
            print("[session-start] HONG: hook vuot han 600s")
            return 124
        except OSError as e:
            loi.append(f"{bash}: {type(e).__name__}")
    print("[session-start] HONG: khong co bash chay duoc; " + "; ".join(loi[:3]))
    return 12


if __name__ == "__main__":
    sys.exit(main())
