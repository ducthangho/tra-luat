#!/usr/bin/env python3
"""Đo mạng ra ngoài qua BA kênh độc lập, mỗi kênh in `TEN=MA_THOAT`.

Quy ước: 0 = lọt, khác 0 = bị chặn. Đây là QUAN SÁT về hành vi sandbox đang
chạy, KHÔNG phải bất biến an ninh — xem docs/MANG_SANDBOX_CODEX.md. Script
không đọc biến môi trường, không tự đổi hành vi theo nơi chạy.

Mỗi hàm bắt MỌI Exception CÓ CHỦ ĐÍCH (ta đo chặn hay không, không đo lỗi
gì) và quy về một mã thoát khác 0 — phản chứng đi kèm (probe_mang_test.py)
chứng minh việc nuốt lỗi này không nuốt NHẦM một lỗi khác thành "bị chặn".
"""
import socket
import subprocess
import sys
import urllib.request

MA_LOT = 0
MA_CHAN = 1


def kenh_bind_loopback():
    """socket.bind loopback — không ra mạng, dùng làm đối chứng nội bộ."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("127.0.0.1", 0))
            s.listen(1)
        finally:
            s.close()
        return MA_LOT
    except Exception:  # bind
        return MA_CHAN


def kenh_urlopen(url="https://api.github.com", timeout=5.0):
    """urllib.request.urlopen ra ngoài."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            resp.read(1)
        return MA_LOT
    except Exception:  # urlopen
        return MA_CHAN


def kenh_git_ls_remote(url="https://github.com/ducthangho/tra-luat.git", timeout=10.0):
    """git ls-remote ra ngoài — quy về mã thoát tiến trình con."""
    try:
        ket_qua = subprocess.run(
            ["git", "ls-remote", url, "HEAD"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
        )
        return MA_LOT if ket_qua.returncode == 0 else MA_CHAN
    except Exception:  # ls_remote
        return MA_CHAN


def main():
    ket_qua = {
        "bind_loopback": kenh_bind_loopback(),
        "urlopen": kenh_urlopen(),
        "git_ls_remote": kenh_git_ls_remote(),
    }
    for ten, ma in ket_qua.items():
        print(f"{ten}={ma}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
