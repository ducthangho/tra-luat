#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NGUYÊN MẪU: tiền kiểm công cụ, sinh NHÃN thay vì văn xuôi.

Luận điểm: một bài học nằm trong tệp `.md` là tri thức BỊ ĐỘNG — nó đòi agent phải
(a) biết nó tồn tại, (b) tìm ra nó, (c) áp đúng lúc. Ba bước ấy hỏng cả ba trong
phiên 15–16/08. Chữa bằng cách biến mỗi bài học thành MỘT NHÃN DO LỆNH SINH RA.

Bốn nhãn, ý nghĩa CỐ ĐỊNH:
  DUNG_DUOC      đã gọi thật và thành công — bằng chứng DƯƠNG
  CO_MAT         nhị phân/tệp tồn tại, CHƯA chứng minh gọi được
  HONG           đã gọi thật và thất bại, kèm lý do đo được
  KHONG_CO       không tìm thấy

Chốt cốt lõi: KHÔNG nhãn nào được suy ra từ `--version`, `login status`, hay tài
liệu. `CO_MAT` là mức trần cho mọi phép kiểm không gọi thật.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

HAN = 25


def _chay(lenh, dau_vao=None):
    try:
        p = subprocess.run(lenh, capture_output=True, text=True, timeout=HAN,
                           input=dau_vao, encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, f"quá hạn {HAN}s"
    except (OSError, subprocess.SubprocessError) as e:
        return 127, f"{type(e).__name__}"


def kiem_git():
    if not shutil.which("git"):
        return "KHONG_CO", "không có git"
    rc, ra = _chay(["git", "ls-remote", "--exit-code", "origin", "HEAD"])
    if rc == 0:
        return "DUNG_DUOC", "ls-remote origin OK — đọc/ghi remote được"
    return "CO_MAT", f"nhị phân có, remote KHÔNG với tới: rc={rc} {ra.strip()[:60]}"


def kiem_rg():
    if not shutil.which("rg"):
        return "KHONG_CO", "không có rg — codex và Claude Code đều gọi nó để tìm mã"
    rc, ra = _chay(["rg", "--version"])
    if rc != 0:
        return "HONG", f"rc={rc}"
    # gọi THẬT: tìm một chuỗi trong stdin
    rc, ra = _chay(["rg", "-c", "xin-chao"], dau_vao="xin-chao\nkhac\n")
    return ("DUNG_DUOC", "tìm được trên stdin") if rc == 0 else ("HONG", f"rc={rc}")


def kiem_claude():
    if not shutil.which("claude"):
        return "KHONG_CO", "không có claude CLI"
    rc, ra = _chay(["claude", "--version"])
    if rc != 0:
        return "HONG", f"--version rc={rc}"
    # có credential trên đĩa không — CHƯA phải bằng chứng gọi được
    p = os.path.expanduser("~/.claude/.credentials.json")
    return ("CO_MAT", f"{ra.strip()[:40]} · credential trên đĩa"
            if os.path.exists(p) else f"{ra.strip()[:40]} · KHÔNG thấy credential")


def kiem_codex():
    if not shutil.which("codex"):
        return "KHONG_CO", "không có codex CLI"
    rc, ra = _chay(["codex", "login", "status"], dau_vao="")
    if rc != 0:
        return "HONG", f"login status rc={rc}"
    # `login status` CHỈ ĐỌC TỆP. Đã đo 16-08: trả "Logged in" cho token ĐÃ THU HỒI.
    # Nên trần của nó là CO_MAT. Muốn DUNG_DUOC phải gọi thật — xem `--goi-that`.
    return "CO_MAT", f"{ra.strip().splitlines()[0][:46]} · login status CHỈ đọc tệp"


def kiem_codex_that():
    if not shutil.which("codex"):
        return "KHONG_CO", "không có codex CLI"
    rc, ra = _chay(["codex", "exec", "-s", "read-only", "--skip-git-repo-check",
                    "Tra loi dung mot tu: OK"], dau_vao="")
    thap = ra.lower()
    for dau in ("token_revoked", "refresh_token_invalidated", "token_invalidated",
                "401 unauthorized", "please log in again", "could not be refreshed"):
        if dau in thap:
            return "HONG", f"credential BỊ TỪ CHỐI ({dau})"
    return ("DUNG_DUOC", "gọi thật thành công") if rc == 0 else ("HONG", f"rc={rc}")


def kiem_github_mcp():
    """CHỖ NÀY LÀ LÝ DO CẢ TỆP NÀY TỒN TẠI.

    Tri thức "dùng api.githubcopilot.com/mcp/, KHÔNG dùng api.github.com" đã nằm
    trong kho từ 14-08 — nhưng chỉ trong hai tệp prompt, dưới dạng văn xuôi. Nó
    KHÔNG có trong `launcher.py doctor` (đo được: `githubcopilot` xuất hiện 0 lần).
    Hậu quả 16-08: một phiên đo `api.github.com`, thấy 403, kết luận "GitHub bị
    chặn", và làm việc cả ngày trên kết luận sai ấy.
    """
    tok = os.environ.get("GITHUB_PAT", "").strip()
    if not tok:
        return "KHONG_CO", "GITHUB_PAT chưa đặt"
    if not shutil.which("curl"):
        return "KHONG_CO", "không có curl"
    goi = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                      "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                                 "clientInfo": {"name": "tien-kiem", "version": "1"}}})
    rc, ra = _chay(["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}",
                    "-X", "POST", "https://api.githubcopilot.com/mcp/",
                    "-H", f"Authorization: Bearer {tok}",
                    "-H", "Content-Type: application/json",
                    "-H", "Accept: application/json, text/event-stream",
                    "-d", goi])
    ma = ra.strip()[-3:]
    if ma == "200":
        return "DUNG_DUOC", "api.githubcopilot.com/mcp/ HTTP 200 — dùng công cụ MCP"
    if ma == "401":
        return "HONG", "HTTP 401 — GITHUB_PAT sai hoặc hết hạn"
    return "HONG", f"HTTP {ma} — KHÔNG kết luận 'GitHub bị chặn' trước khi đọc thân phản hồi"


BANG = [
    ("git", kiem_git), ("rg", kiem_rg), ("claude", kiem_claude),
    ("codex", kiem_codex), ("github-mcp", kiem_github_mcp),
]


def main(argv) -> int:
    that = "--goi-that" in argv
    if that:
        BANG.insert(4, ("codex(gọi thật)", kiem_codex_that))
    ket = {}
    print(f"{'công cụ':<16} {'nhãn':<12} chi tiết")
    print("-" * 92)
    for ten, fn in BANG:
        nhan, vi = fn()
        ket[ten] = nhan
        print(f"{ten:<16} {nhan:<12} {vi}")
    print("-" * 92)
    if not that:
        print("CHƯA gọi thật codex — thêm `--goi-that` để nâng CO_MAT lên DUNG_DUOC/HONG.")
    xau = [k for k, v in ket.items() if v == "HONG"]
    print(f"\nHỎNG: {xau or 'không'}")
    return 1 if xau else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
