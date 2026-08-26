#!/usr/bin/env python3
"""In ba mã thoát cho ba kênh mạng. Không sửa gì, không cần đối số.

Sinh ra vì cross-review đòi bảng mạng trong `docs/GOI_AGENT_DA_NEN.md` phải TÁI LẬP ĐƯỢC;
trước đó probe chỉ được mô tả bằng văn xuôi và gọi là `P`. Ba lượt cho ba cột của bảng ấy:

    python3 .claude/dev/probe_mang.py                                  # đối chứng, ngoài codex
    codex sandbox -c sandbox_mode=workspace-write -- python3 ...      # cột mặc định
    codex sandbox -c sandbox_mode=workspace-write \
      -c sandbox_workspace_write.network_access=true -- python3 ...    # cột bật mạng

`codex sandbox` chạy thẳng một lệnh trong sandbox, không có lượt model ở giữa, nên tất định.
Số in ra KHÔNG phải bất biến an ninh — chúng phụ thuộc phiên bản và cấu hình; đọc như QUAN SÁT
CÓ ĐIỀU KIỆN ĐO, đúng như mục doctrine dặn."""
import socket, subprocess, urllib.request


def ma_thoat(viec) -> int:
    """0 nếu lọt, 1 nếu bị chặn. Nuốt lỗi CÓ CHỦ Ý: ta đo chặn hay không, không đo lỗi gì."""
    try:
        viec()
        return 0
    except Exception:
        return 1


print("bind     ", ma_thoat(lambda: socket.socket().bind(("127.0.0.1", 0))))
print("urllib   ", ma_thoat(lambda: urllib.request.urlopen("https://api.github.com", timeout=8)))
print("ls-remote", subprocess.run(["git", "ls-remote", "https://github.com/git/git"],
                                  capture_output=True, timeout=60).returncode)
