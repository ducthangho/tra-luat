"""Tripwire cho ranh giới của chính packet (acceptance §3, mục "Ranh giới" và "Fake GitHub store").

Hai tripwire, mỗi cái đều có ĐỐI CHỨNG DƯƠNG trong selftest:

  EnvAccessRecorder / EnvGuard - ghi lại MỌI lần đọc biến môi trường TRONG tiến trình **và** mọi
                                 lần biến nhạy cảm được trao cho TIẾN TRÌNH CON.
  NetworkGuard                 - mọi lời gọi mạng ném lỗi ĐÍCH DANH ngay lập tức, KHÔNG treo.

Vì sao bắt buộc có đối chứng dương: một detector chết cũng báo "sạch". "Không phát hiện lần đọc
nào" chỉ có nghĩa khi đã chứng minh detector CÓ bắt được một lần đọc cố ý. Đây đúng bài học
"sạch vì chẳng chạy gì" ghi ở Mission #76 §4 (RA-02).

──────────────────────────────────────────────────────────────────────────────
CLAIM ĐƯỢC THU HẸP CÓ CHỦ ĐÍCH (finding wp77-g1-sec-02)
──────────────────────────────────────────────────────────────────────────────
g1 tuyên bố NetworkGuard chặn "mọi lối ra mạng của stdlib". Auditor phá được: một tham chiếu
`socket.socket` chụp TRƯỚC khi vào guard vẫn tạo được socket, và `guard.attempts` vẫn rỗng.

Bản này làm hai việc, không chỉ một:

  1. **Mở rộng phủ** - vá `__init__` của CHÍNH LỚP `socket.socket` (chứ không chỉ gán lại thuộc
     tính module), nên tham chiếu đã cache trước guard cũng bị chặn; và mọi đường đều ghi vào
     `attempts`, nên `attempts` trở thành tín hiệu phủ thật chứ không phải trang trí.
  2. **Thu hẹp claim** - `NetworkGuard.COVERAGE` khai BẰNG MÁY cái gì được phủ và cái gì KHÔNG.
     Ranh giới thật của "không có lối ra mạng" là **network namespace** (`unshare -n`), không phải
     monkeypatch trong cùng tiến trình. Guard này là tripwire tiện dụng chạy được ở mọi nơi; nó
     KHÔNG phải sandbox, và selftest có test đòi `not_covered` phải khác rỗng để không ai lặng lẽ
     nâng claim trở lại.
"""

import os
import socket
import subprocess
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
    """Nhận cả khoá `str` lẫn `bytes`.

    Thiếu nhánh bytes thì `str(b"GH_TOKEN")` ra `"b'GH_TOKEN'"` - không khớp tiền tố nào, nên
    `os.environb` và một `env=` dạng bytes truyền cho `Popen` đi qua sạch: không ghi nhận, không
    scrub. Bằng chứng "không đọc credential" khi đó chỉ đúng cho một nửa kiểu dữ liệu.
    """
    if isinstance(name, (bytes, bytearray)):
        name = bytes(name).decode("utf-8", "replace")
    upper = str(name).upper()
    return any(upper.startswith(p) for p in SENSITIVE_PREFIXES)


# Phạm vi phủ của BỘ QUÉT TĨNH, khai ở đây để CLI `coverage` in ra được như dữ liệu thay vì
# chôn trong docstring của suite. Một bộ quét tĩnh không bao giờ phủ hết; điều bắt buộc là nó
# phải NÓI phần nó không phủ.
STATIC_SCANNER_COVERAGE = {
    "covered": (
        "plain import / from-import of a forbidden module",
        "importlib.import_module and __import__ with a constant target, including builtins.__import__",
        "module aliases: import subprocess as sp / from subprocess import run as r",
        "one level of variable aliasing: runner = sp.run then runner([...])",
        "subprocess calls whose argv[0] is a constant network tool",
        "the same calls written with keyword arguments: run(args=[...]), import_module(name=...)",
        "os.system / os.popen",
    ),
    "not_covered": (
        "import target computed at runtime: importlib.import_module(name_from_variable)",
        "argv built dynamically: subprocess.run([tool_var, ...])",
        "indirection through getattr(subprocess, 'run') or a dict/list of callables",
        "variable aliasing chained more than one level, or rebound inside a branch",
        "eval / exec / compile, ctypes, direct syscalls",
    ),
    "real_boundary": "a network namespace (unshare -n) - static scanning is a smoke alarm, not a wall",
}


class NetworkAccessBlocked(RuntimeError):
    """Ném khi có bất kỳ lời gọi mạng nào. Đích danh, tức thời - không timeout, không treo."""


class EnvAccessRecorder(MutableMapping):
    """Bọc os.environ và ghi lại mọi khoá được ĐỌC.

    Bọc chính `os.environ` là đủ cho cả `os.getenv` (nó gọi `environ.get`) và
    `os.environ[...]` / `.get` / `in`.

    Lưu ý ngữ nghĩa: `sensitive_reads()` bao gồm CẢ hai đường - đọc trong tiến trình, và trao
    biến nhạy cảm cho tiến trình con. Trao credential cho child ít nhất cũng tệ ngang đọc nó, nên
    gộp chung vào một câu trả lời thay vì để người đọc phải hỏi hai lần.
    """

    def __init__(self, wrapped, note_into=None):
        self._wrapped = wrapped
        # `note_into` cho phép recorder của `os.environb` ghi vào CÙNG sổ với recorder của
        # `os.environ`: hai mapping, một câu trả lời.
        self._sink = note_into
        self.reads = [] if note_into is None else note_into.reads
        self.child_env_exposures = [] if note_into is None else note_into.child_env_exposures

    def _note(self, key):
        if isinstance(key, bytes):
            key = key.decode("utf-8", "replace")
        self.reads.append(str(key))

    @staticmethod
    def _text(value):
        """Tên biến luôn báo cáo dạng text, dù env dùng khoá bytes - `b'GH_TOKEN'` không phải tên."""
        if isinstance(value, (bytes, bytearray)):
            return bytes(value).decode("utf-8", "replace")
        return str(value)

    def note_child_exposure(self, key, argv0):
        """Ghi nhận một biến nhạy cảm suýt (hoặc đã) đi vào environment của tiến trình con."""
        self.child_env_exposures.append({"name": self._text(key), "child": self._text(argv0)})
        self._note(key)

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

    def copy(self):
        """`os.environ.copy()` phải còn dùng được khi recorder đang thay chỗ nó.

        `MutableMapping` KHÔNG cấp `.copy()`, nên bản trước làm `os.environ.copy()` ném
        AttributeError - và thư viện con hay gọi đúng thứ đó ngay trước khi tạo subprocess. Một
        guard làm hỏng code lành là guard sẽ bị gỡ ra, nên nó phải trong suốt.

        Sao chép là một lần ĐỌC TOÀN BỘ environment, kể cả biến nhạy cảm, nên nó được ghi nhận -
        im lặng ở đây sẽ là một lối đọc credential không ai thấy.
        """
        return self._snapshot()

    def _snapshot(self):
        snapshot = dict(self._wrapped)
        for key in snapshot:
            if is_sensitive(key):
                self._note(key)
        return snapshot

    # `dict | mapping` (PEP 584). `MutableMapping` KHÔNG cấp các toán tử này, nên bản trước
    # `os.environ | {}` chạy bình thường NGOÀI guard và ném TypeError DƯỚI guard. Một guard chỉ
    # hoạt động khi không ai dùng cú pháp hiện đại thì không phải guard, chỉ là bẫy.
    def __or__(self, other):
        merged = self._snapshot()
        merged.update(other)
        return merged

    def __ror__(self, other):
        merged = dict(other)
        merged.update(self._snapshot())
        return merged

    def __ior__(self, other):
        for key, value in dict(other).items():
            self._wrapped[key] = value
        return self

    # ── truy vấn ────────────────────────────────────────────────────────────
    def sensitive_reads(self):
        """Danh sách (đã khử trùng lặp, giữ thứ tự) các khoá nhạy cảm đã bị đọc hoặc bị trao đi."""
        seen, out = set(), []
        for key in self.reads:
            if is_sensitive(key) and key not in seen:
                seen.add(key)
                out.append(key)
        return out


class NetworkGuard:
    """Context manager: mọi lối ra mạng qua module `socket` ném NetworkAccessBlocked đích danh.

    Đọc `COVERAGE` trước khi dùng kết quả của guard này làm bằng chứng cho bất cứ điều gì.
    """

    # Khai BẰNG MÁY, không phải văn xuôi trong docstring: test đòi `not_covered` khác rỗng.
    COVERAGE = {
        "covered": (
            "socket.socket(...) via the module attribute",
            "socket.socket(...) via a reference cached BEFORE the guard (class __init__ patched)",
            "socket.create_connection / getaddrinfo / gethostbyname",
            "anything layered on the socket module (http.client, urllib, ...)",
        ),
        "not_covered": (
            "direct use of the C extension _socket.socket (cannot be patched from Python)",
            "child processes: a subprocess has its own interpreter and its own socket module",
            "non-socket egress (a helper binary such as curl/gh doing its own syscalls)",
            "os.system / ctypes / raw syscalls",
        ),
        "real_boundary": "network namespace (unshare -n) - this guard is a tripwire, not a sandbox",
    }

    _MODULE_FUNCS = ("create_connection", "getaddrinfo", "gethostbyname")

    def __init__(self):
        self._saved_funcs = {}
        self._saved_socket_cls = None
        self._saved_socket_init = None
        self.attempts = []

    def _blocker(self, label):
        def _fn(*args, **kwargs):
            self.attempts.append(label)
            raise NetworkAccessBlocked(
                "network access blocked by NetworkGuard: socket.%s(%r)" % (label, args)
            )

        return _fn

    def __enter__(self):
        guard = self

        class _BlockedSocket:
            """Thay thế thuộc tính module. Ném ngay khi khởi tạo - không có đường tới syscall."""

            def __init__(self, *args, **kwargs):
                guard.attempts.append("socket")
                raise NetworkAccessBlocked(
                    "network access blocked by NetworkGuard: socket.socket(%r, %r)" % (args, kwargs)
                )

        for name in self._MODULE_FUNCS:
            self._saved_funcs[name] = getattr(socket, name)
            setattr(socket, name, self._blocker(name))

        # Đây là điểm g1 thủng: gán lại THUỘC TÍNH MODULE không đụng tới tham chiếu đã cache.
        # Vá `__init__` của chính lớp thì tham chiếu cache cũng đi qua đây.
        self._saved_socket_cls = socket.socket
        self._saved_socket_init = socket.socket.__init__

        def _blocked_init(sock_self, *args, **kwargs):
            guard.attempts.append("socket.__init__")
            raise NetworkAccessBlocked(
                "network access blocked by NetworkGuard: socket.socket.__init__(%r, %r)"
                % (args, kwargs)
            )

        self._saved_socket_cls.__init__ = _blocked_init
        socket.socket = _BlockedSocket
        self.blocked_socket_type = _BlockedSocket
        return self

    def __exit__(self, *exc):
        for name, original in self._saved_funcs.items():
            setattr(socket, name, original)
        self._saved_funcs.clear()
        if self._saved_socket_cls is not None:
            self._saved_socket_cls.__init__ = self._saved_socket_init
            socket.socket = self._saved_socket_cls
            self._saved_socket_cls = None
            self._saved_socket_init = None
        return False


class EnvGuard:
    """Cài EnvAccessRecorder vào os.environ, VÀ phủ luôn đường tiến trình con.

    Vì sao phải phủ subprocess (finding wp77-g1-spec-02): `os.environ` chỉ là bản sao phía Python.
    `subprocess.run(..., env=None)` KHÔNG đọc nó - child kế thừa environment ở tầng OS qua execve.
    Auditor bơm `GH_TOKEN` rồi cho child đọc và in ra đúng marker, trong khi `sensitive_reads()`
    vẫn rỗng. Recorder ở parent không thể thấy điều đó, nên phải chặn ở CHỖ TẠO child.

    Xử lý: mọi `subprocess.Popen` đi qua đây đều bị **scrub** biến nhạy cảm khỏi environment của
    child (fail-closed: credential không bao giờ tới child), và mỗi biến bị scrub được ghi vào
    recorder. Nghĩa là suite không chỉ *phát hiện* được đường này - nó còn *đóng* đường này.

    `inject=` là bookkeeping của CHÍNH guard, không phải "code under test đọc credential": guard
    lưu/khôi phục giá trị cũ qua mapping thô TRƯỚC khi recorder được cài. Nhờ vậy test không còn
    phải tự `os.environ.get(...)` các biến cần bảo vệ ngay trước khi cài guard - đó là dòng
    `selftest.py:509` mà auditor đã chỉ ra.
    """

    COVERAGE = {
        "covered": (
            "in-process reads through os.environ / os.getenv",
            "os.environ.copy() and the PEP 584 union operators (| and |=)",
            "os.environb on POSIX - the bytes-keyed second view of the same environment",
            "environment handed to children created via subprocess.Popen (run/call/check_output)",
        ),
        "not_covered": (
            "os.execve / posix_spawn called directly, bypassing subprocess",
            "credentials already read into a variable before the guard was installed",
            "a saved reference to the real os.environ captured before the guard",
            "files on disk holding credentials (this guard watches the environment only)",
        ),
        "real_boundary": "a process started without the credential in its environment at all",
    }

    def __init__(self, inject=None, guard_subprocess=True, scrub_child_env=True):
        self.recorder = None
        self._saved_environ = None
        self._inject = dict(inject or {})
        self._restore = {}
        self._guard_subprocess = bool(guard_subprocess)
        self._scrub_child_env = bool(scrub_child_env)
        self._saved_popen = None
        self._saved_environb = None

    # ── phủ subprocess ──────────────────────────────────────────────────────
    # Popen(args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd,
    #       env, ...) - `env` là tham số thứ 11. Trong `_GuardedPopen.__init__`, `args` đã bị tách
    # ra riêng nên phần còn lại bắt đầu từ `bufsize`: chỉ số của `env` là 9, KHÔNG phải 10.
    _ENV_INDEX_IN_REST = 9

    def _effective_env(self, rest, kwargs):
        """Lấy `env` dù nó được truyền bằng keyword hay bằng vị trí."""
        if "env" in kwargs:
            return kwargs["env"], "kw"
        if len(rest) > self._ENV_INDEX_IN_REST:
            return rest[self._ENV_INDEX_IN_REST], "pos"
        return None, "absent"

    def _install_subprocess_guard(self):
        recorder = self.recorder
        self._saved_popen = subprocess.Popen
        saved_popen = self._saved_popen

        class _GuardedPopen(saved_popen):
            def __init__(inner, args, *rest, **kwargs):
                env, where = self._effective_env(rest, kwargs)
                # `env=None` nghĩa là child kế thừa environment ở tầng OS. Đọc mapping THÔ chứ
                # không đọc qua recorder: recorder sẽ ghi mọi khoá thành "lần đọc" và làm nhiễu
                # đúng cái tín hiệu ta đang muốn giữ sạch.
                inherited = self._saved_environ if env is None else env
                argv0 = args[0] if isinstance(args, (list, tuple)) and args else args
                scrubbed = {}
                for key, value in dict(inherited).items():
                    if is_sensitive(key):
                        recorder.note_child_exposure(key, argv0)
                        continue
                    scrubbed[key] = value
                # PHÁT HIỆN và SCRUB là hai việc TÁCH RỜI. Ghi nhận ở trên chạy luôn; scrub thì
                # tuỳ chọn. Vì sao phải tách: khi guard vừa phát hiện vừa bịt, một phép thử "child
                # có đọc credential không" trở thành FALSE-GREEN - child không bao giờ nhận marker
                # nên chẳng chứng minh được gì, và một mutant cho code đọc GH_TOKEN vẫn xanh. Suite
                # dùng scrub_child_env=False khi cần chứng minh chính khả năng PHÁT HIỆN.
                if self._scrub_child_env:
                    if where == "pos":
                        rest = list(rest)
                        rest[self._ENV_INDEX_IN_REST] = scrubbed
                        rest = tuple(rest)
                    else:
                        kwargs["env"] = scrubbed
                super().__init__(args, *rest, **kwargs)

        subprocess.Popen = _GuardedPopen

    def __enter__(self):
        self._saved_environ = os.environ
        # Bookkeeping của guard, chạy TRƯỚC khi recorder tồn tại - cố ý không đếm là "lần đọc".
        for key, value in self._inject.items():
            self._restore[key] = self._saved_environ.get(key)
            self._saved_environ[key] = value
        self.recorder = EnvAccessRecorder(self._saved_environ)
        os.environ = self.recorder
        # POSIX có `os.environb` - MỘT mapping thứ hai vào cùng environment, khoá dạng bytes.
        # Không bọc nó thì `os.environb[b"GH_TOKEN"]` là một lối đọc credential mà recorder mù hoàn
        # toàn, và bằng chứng "không đọc biến nhạy cảm" chỉ đúng cho một nửa API.
        self._saved_environb = getattr(os, "environb", None)
        if self._saved_environb is not None:
            os.environb = EnvAccessRecorder(self._saved_environb, note_into=self.recorder)
        if self._guard_subprocess:
            self._install_subprocess_guard()
        return self.recorder

    def __exit__(self, *exc):
        if self._saved_popen is not None:
            subprocess.Popen = self._saved_popen
            self._saved_popen = None
        if self._saved_environb is not None:
            os.environb = self._saved_environb
            self._saved_environb = None
        os.environ = self._saved_environ
        for key, value in self._restore.items():
            if value is None:
                self._saved_environ.pop(key, None)
            else:
                self._saved_environ[key] = value
        self._restore.clear()
        return False
