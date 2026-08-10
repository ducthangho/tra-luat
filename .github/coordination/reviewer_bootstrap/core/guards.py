"""Tripwire cho ranh giới của chính packet (acceptance §3, mục "Ranh giới" và "Fake GitHub store").

Hai tripwire, mỗi cái đều có ĐỐI CHỨNG DƯƠNG trong selftest:

  EnvAccessRecorder - ghi lại MỌI lần đọc biến môi trường, để test chứng minh tiến trình
                      KHÔNG đọc GH_TOKEN/GITHUB_TOKEN/AWS_*.
  NetworkGuard      - mọi lời gọi mạng ném lỗi ĐÍCH DANH ngay lập tức, KHÔNG treo.

Vì sao bắt buộc có đối chứng dương: một detector chết cũng báo "sạch". "Không phát hiện lần đọc
nào" chỉ có nghĩa khi đã chứng minh detector CÓ bắt được một lần đọc cố ý. Đây đúng bài học
"sạch vì chẳng chạy gì" ghi ở Mission #76 §4 (RA-02).
"""

import os
import socket
from collections.abc import MutableMapping

# Tiền tố biến môi trường bị coi là nhạy cảm. Khớp theo tiền tố, không theo tên chính xác:
# AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN... đều phải bị bắt.
SENSITIVE_PREFIXES = (
    "GH_TOKEN",
    "GITHUB_TOKEN",
    "GITHUB_PAT",
    "AWS_",
    "ANTHROPIC_",
    "OPENAI_",
)


def is_sensitive(name):
    upper = str(name).upper()
    return any(upper.startswith(p) for p in SENSITIVE_PREFIXES)


class NetworkAccessBlocked(RuntimeError):
    """Ném khi có bất kỳ lời gọi mạng nào. Đích danh, tức thời - không timeout, không treo."""


class EnvAccessRecorder(MutableMapping):
    """Bọc os.environ và ghi lại mọi khoá được ĐỌC.

    Bọc chính `os.environ` là đủ cho cả `os.getenv` (nó gọi `environ.get`) và
    `os.environ[...]` / `.get` / `in`.
    """

    def __init__(self, wrapped):
        self._wrapped = wrapped
        self.reads = []

    def _note(self, key):
        self.reads.append(str(key))

    def __getitem__(self, key):
        self._note(key)
        return self._wrapped[key]

    def get(self, key, default=None):
        self._note(key)
        return self._wrapped.get(key, default)

    def __contains__(self, key):
        self._note(key)
        return key in self._wrapped

    def __setitem__(self, key, value):
        self._wrapped[key] = value

    def __delitem__(self, key):
        del self._wrapped[key]

    def __iter__(self):
        return iter(self._wrapped)

    def __len__(self):
        return len(self._wrapped)

    # ── truy vấn ────────────────────────────────────────────────────────────
    def sensitive_reads(self):
        """Danh sách (đã khử trùng lặp, giữ thứ tự) các khoá nhạy cảm đã bị đọc."""
        seen, out = set(), []
        for key in self.reads:
            if is_sensitive(key) and key not in seen:
                seen.add(key)
                out.append(key)
        return out


class _BlockedSocket:
    """Thay thế socket.socket. Ném ngay khi khởi tạo - không có đường tới syscall."""

    def __init__(self, *args, **kwargs):
        raise NetworkAccessBlocked(
            "network access blocked by NetworkGuard: socket.socket(%r, %r)" % (args, kwargs)
        )


class NetworkGuard:
    """Context manager: mọi lối ra mạng của stdlib ném NetworkAccessBlocked đích danh.

    Chặn ở tầng `socket` nên phủ luôn http.client / urllib / bất cứ thứ gì dựng trên nó.
    """

    _PATCHED = ("socket", "create_connection", "getaddrinfo", "gethostbyname")

    def __init__(self):
        self._saved = {}
        self.attempts = []

    def _blocker(self, label):
        def _fn(*args, **kwargs):
            self.attempts.append(label)
            raise NetworkAccessBlocked(
                "network access blocked by NetworkGuard: socket.%s(%r)" % (label, args)
            )

        return _fn

    def __enter__(self):
        for name in self._PATCHED:
            self._saved[name] = getattr(socket, name)
        socket.socket = _BlockedSocket
        for name in ("create_connection", "getaddrinfo", "gethostbyname"):
            setattr(socket, name, self._blocker(name))
        return self

    def __exit__(self, *exc):
        for name, original in self._saved.items():
            setattr(socket, name, original)
        self._saved.clear()
        return False


class EnvGuard:
    """Context manager cài EnvAccessRecorder vào os.environ và gỡ ra khi thoát."""

    def __init__(self):
        self.recorder = None
        self._saved = None

    def __enter__(self):
        self._saved = os.environ
        self.recorder = EnvAccessRecorder(self._saved)
        os.environ = self.recorder
        return self.recorder

    def __exit__(self, *exc):
        os.environ = self._saved
        return False
