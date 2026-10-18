#!/usr/bin/env python3
"""Exec-form bridge cho SessionStart: đọc env trước, tìm bash CHẠY ĐƯỢC, rồi gọi hook.

Không dùng shell để khởi động bridge. Trên Windows, `bash` đầu PATH có thể là WSL
shim trả Access denied trong khi Git Bash tốt vẫn tồn tại ở Program Files.
(Xem docs/incidents/2026-08-15-launcher-codex-github-toolchain.md — nguyên nhân
gốc số 4; cùng họ bài học t106 của launcher: binary hỏng đầu PATH không được che
binary tốt phía sau.)

Port từ nhánh codex/gate-lifecycle đã khai tử (blob ea85526b, tag
archive/codex-gate-lifecycle-ec8d08c) qua packet GLS-B1. Khác bản gốc BA điểm,
đều khai:
1. Trần thời gian chạy hook đọc từ TL_HOOK_TIMEOUT_GIAY (mặc định 600; rác/âm/
   "inf" đều về 600) để phản chứng rc=124 đo được trong test mà không chờ 10 phút.
2. Tra env KHÔNG phân biệt hoa thường (`_lay_env`): bản gốc `env.get("ProgramFiles")`
   LUÔN trượt trên Windows vì `dict(os.environ)` viết hoa khoá thành `PROGRAMFILES`,
   nên fallback Program Files chạy bằng default cứng bất kể env — bug tiềm ẩn vô
   hình ở production (default trùng thực tế) mà t124 spawn thật bắt được.
3. `_ep_utf8` ép stdout/stderr UTF-8 trước mọi print — thiếu nó, nhánh lỗi chết
   UnicodeEncodeError trên console cp1258 với đường dẫn có dấu (P2 review #173).
Chốt tương ứng: t122–t128 trong .claude/dev/launcher_test.py.
"""

from __future__ import annotations

import os
import platform
import runpy
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
    """Trần chạy hook. Sai/âm/rỗng/vô hạn thì về 600 — bridge chẩn đoán không được
    chết vì config, và "inf" cũng không được phép xoá kỷ luật 124 (P3 review #173)."""
    try:
        v = float(env.get("TL_HOOK_TIMEOUT_GIAY", "") or 600)
    except ValueError:
        return 600.0
    return v if 0 < v < float("inf") else 600.0


def _ep_utf8() -> None:
    """Ép stdout/stderr sang UTF-8 TRƯỚC khi in gì — bài học đầu bảng của launcher:
    console máy Việt là cp1258, một `print` đường dẫn có dấu ("Quốc hội") ném
    UnicodeEncodeError và giết cả lượt chạy trước khi logic kịp sai. Thiếu chốt
    này, nhánh lỗi của bridge trả rc=1 traceback thay vì rc=12 + chẩn đoán
    (P2 review PR #173 — đo thật, không phải suy). Chốt: t128."""
    for f in (sys.stdout, sys.stderr):
        try:
            f.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass


def _codex_chay_duoc(env: dict[str, str]) -> bool:
    """CÓ MẶT ≠ CHẠY ĐƯỢC (Codex lượt 2 G01): `shutil.which` thấy một shim hỏng (rc=127) vẫn trả
    đường dẫn, và bridge từng materialize ngay ⇒ rc=13 trước khi hook kịp cài lại CLI. Cùng
    phép thử với `co_chay` của hook: `--version` có hạn, đòi rc=0 VÀ có đầu ra. Child chạy với
    env ĐÃ gỡ snapshot."""
    duong = shutil.which("codex", path=_lay_env(env, "PATH"))
    if not duong:
        return False
    sach = {k: v for k, v in env.items() if k.upper() != "CODEX_AUTH_JSON"}
    try:
        p = subprocess.run([duong, "--version"], stdin=subprocess.DEVNULL, capture_output=True,
                           text=True, env=sach, timeout=8, encoding="utf-8", errors="replace")
    except (OSError, subprocess.SubprocessError):
        return False
    return p.returncode == 0 and bool(((p.stdout or "") + (p.stderr or "")).strip())


def _vat_chat_hoa(project: Path, snapshot: str | None) -> bool:
    """Chạy materializer của kho trong tiến trình này. `snapshot=None` ⇒ đọc os.environ (như cũ)."""
    try:
        launcher = runpy.run_path(str(project / ".claude/dev/launcher.py"))
        ket = launcher["chuan_bi_xac_thuc"](that_su=True, snapshot=snapshot)
        if not ket or not all(x.get("ok") for x in ket):
            raise ValueError("credential unavailable")
        return True
    except Exception:
        print("[session-start] HONG: khong chuan bi duoc Codex credential")
        return False
    finally:
        os.environ.pop("CODEX_AUTH_JSON", None)


def main() -> int:
    env = dict(os.environ)  # PHẢI là thao tác runtime đầu tiên, trước resolve/probe
    env["TL_LAUNCHER_ENV_DA_DOC"] = "1"
    _ep_utf8()              # ngay sau chụp env, TRƯỚC mọi print/probe
    project = Path(env.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
    script = project / ".claude" / "hooks" / "session-start.sh"
    if not script.is_file():
        print(f"[session-start] HONG: khong thay hook {script}")
        return 12
    # Run the repository materializer in this process before even bash --version.
    # The shell and all its descendants receive only the selected on-disk home.
    # wp484 g7 (Codex lượt 1 F04): chưa có `codex` trên PATH thì snapshot mới KHÔNG probe được,
    # và rc=13 ở đây chặn luôn bước `npm install` của hook — máy mới không bao giờ tự phục hồi.
    # Khi ấy HOÃN: hook chạy với môi trường đã gỡ snapshot (cài CLI), rồi mới materialize tại
    # đây. Snapshot thô vẫn KHÔNG bao giờ tới shell.
    hoan = None
    if _lay_env(env, "CODEX_AUTH_JSON") and env.get("CLAUDE_CODE_REMOTE") == "true":
        if not _codex_chay_duoc(env):
            hoan = _lay_env(env, "CODEX_AUTH_JSON")
        elif not _vat_chat_hoa(project, None):
            os.environ.pop("CODEX_AUTH_JSON", None)
            return 13
    os.environ.pop("CODEX_AUTH_JSON", None)
    env = {k: v for k, v in env.items() if k.upper() != "CODEX_AUTH_JSON"}
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
            rc = subprocess.run([bash, str(script)], cwd=project, env=env,
                                stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
                                timeout=_tran_giay(env)).returncode
            if hoan is not None and rc == 0 and not _vat_chat_hoa(project, hoan):
                return 13
            return rc
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
