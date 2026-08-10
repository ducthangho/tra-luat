"""Bộ quét TĨNH của lõi RA-01: cài đặt và khai báo phạm vi phủ, ở CÙNG một chỗ.

Trước đây ba mảnh nằm ba nơi: logic quét ở `selftest.py`, metadata phủ ở `guards.py`, và lời hứa
ở README. Chúng đã TRÔI LỆCH thật - `covered` tuyên bố phủ constant argv trong khi `gh.exe` và
dạng shell-string vẫn lọt, và không dạng nào nằm trong `not_covered`. Bên quên cập nhật chính là
bên công bố một claim rộng hơn thứ mình phủ, nên cài đặt và claim phải sống cạnh nhau: sửa bộ quét
mà không đụng `COVERAGE` ngay bên dưới là một việc phải CỐ Ý mới làm được.

Counter-test vẫn ở `selftest.py` có chủ đích. Một module tự chứng minh mình đúng thì phép chứng
minh chết cùng lúc với thứ nó chứng minh.

Module này KHÔNG import mạng, KHÔNG chạy tiến trình con, và chỉ đọc AST.
"""

import ast
import os
import re


FORBIDDEN_IMPORTS = {
    "socket", "ssl", "http", "urllib", "urllib2", "urllib3", "requests", "httpx",
    "ftplib", "smtplib", "telnetlib", "xmlrpc", "asyncio", "aiohttp",
    "anthropic", "openai", "google", "boto3", "botocore",
}

# Binary có khả năng tự ra mạng. Bắt theo argv[0] hằng - đủ để chặn `subprocess.run(["gh", ...])`,
# và KHÔNG hứa bắt được argv dựng động (xem `COVERAGE['not_covered']`).
NETWORK_TOOLS = {"gh", "curl", "wget", "git", "ssh", "scp", "nc", "ncat", "openssl", "pip", "npm"}


# Phạm vi phủ của BỘ QUÉT TĨNH, khai ở đây để CLI `coverage` in ra được như dữ liệu thay vì
# chôn trong docstring của suite. Một bộ quét tĩnh không bao giờ phủ hết; điều bắt buộc là nó
# phải NÓI phần nó không phủ.
COVERAGE = {
    "covered": (
        "plain import / from-import of a forbidden module",
        "importlib.import_module and __import__ with a constant target, including builtins.__import__",
        "module aliases: import subprocess as sp / from subprocess import run as r",
        "one level of variable aliasing: runner = sp.run then runner([...])",
        "subprocess calls whose argv[0] is a constant network tool",
        "the same calls written with keyword arguments: run(args=[...]), import_module(name=...)",
        "Windows executable suffixes on argv[0]: gh.exe, curl.cmd, wget.bat",
        "shell-string form: subprocess.run('gh api /user', shell=True) - first token only",
        "os.system / os.popen",
    ),
    "not_covered": (
        "a shell string whose first token is not the real binary (env VAR=1 gh, sh -c '...')",
        "import target computed at runtime: importlib.import_module(name_from_variable)",
        "argv built dynamically: subprocess.run([tool_var, ...])",
        "indirection through getattr(subprocess, 'run') or a dict/list of callables",
        "variable aliasing chained more than one level, or rebound inside a branch",
        "eval / exec / compile, ctypes, direct syscalls",
    ),
    "real_boundary": "a network namespace (unshare -n) - static scanning is a smoke alarm, not a wall",
}


def _parse_dir(directory):
    for name in sorted(os.listdir(directory)):
        if name.endswith(".py"):
            with open(os.path.join(directory, name), "r", encoding="utf-8") as fh:
                yield name, ast.parse(fh.read(), filename=name)


def _scan_forbidden_imports(directory, allowed):
    """Liệt kê (tệp, module) import bị cấm trong `directory`, bỏ qua cặp nằm trong `allowed`."""
    offenders = []
    for name, tree in _parse_dir(directory):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                roots = [(node.module or "").split(".")[0]]
            else:
                continue
            for module in roots:
                if module in FORBIDDEN_IMPORTS and (name, module) not in allowed:
                    offenders.append((name, module))
    return offenders


def _dotted(node):
    """Tên chấm của một biểu thức gọi (`importlib.import_module`), hoặc None."""
    bits = []
    while isinstance(node, ast.Attribute):
        bits.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        bits.append(node.id)
        return ".".join(reversed(bits))
    return None


def _const_str(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _alias_map(tree):
    """Bảng alias của một tệp: alias module -> module thật, và alias hàm -> 'module.hàm'.

    Không có bảng này thì `import subprocess as sp` + `sp.run(["gh", ...])` cho `offenders=[]`,
    và bộ quét chỉ bắt được kẻ tấn công không biết đổi tên - tức là không bắt được ai.
    """
    modules, funcs = {}, {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                modules[alias.asname or root] = root
        elif isinstance(node, ast.ImportFrom):
            module = (node.module or "").split(".")[0]
            for alias in node.names:
                funcs[alias.asname or alias.name] = "%s.%s" % (module, alias.name)

    # Một tầng alias qua BIẾN: `runner = sp.run` rồi `runner([...])`. Bản trước mù với đường này,
    # nên đổi tên hai lần là thoát - và "đổi tên hai lần" không phải kỹ thuật cao siêu gì.
    for _ in range(3):  # lặp vài lượt để `a = sp; b = a.run` cũng hội tụ
        changed = False
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name):
                continue
            resolved = _resolve_call(node.value, modules, funcs)
            if resolved and funcs.get(target.id) != resolved:
                # Chỉ nhận alias trỏ tới thứ ta THỰC SỰ quan tâm, để không nuốt mọi phép gán.
                root = resolved.split(".")[0]
                if root in FORBIDDEN_IMPORTS or root in ("subprocess", "importlib", "os", "builtins"):
                    funcs[target.id] = resolved
                    if "." not in resolved:
                        modules[target.id] = resolved
                    changed = True
        if not changed:
            break
    return modules, funcs


def _resolve_call(func_node, modules, funcs):
    """Tên gọi đã CANONICAL hoá qua bảng alias, hoặc None."""
    dotted = _dotted(func_node)
    if dotted is None:
        return None
    head, _dot, rest = dotted.partition(".")
    if not rest:
        resolved = funcs.get(head, head)
    else:
        base = funcs.get(head) or modules.get(head, head)
        resolved = "%s.%s" % (base, rest)
    # `builtins.__import__` và `__import__` là CÙNG một hàm; ghi hai tên cho cùng một thứ là mời
    # người ta đi vòng qua tên còn lại.
    if resolved.startswith("builtins."):
        resolved = resolved[len("builtins."):]
    return resolved


_WINDOWS_EXEC_SUFFIXES = (".exe", ".com", ".bat", ".cmd", ".ps1")


def _tool_name(argv0):
    """Tên công cụ đã chuẩn hoá từ argv[0], hoặc None.

    Hai dạng bản trước bỏ lọt, cả hai đều là cách gọi hoàn toàn bình thường:
      `gh.exe`                    - đuôi thực thi của Windows;
      `subprocess.run("gh api /user", shell=True)` - argv là MỘT chuỗi lệnh, không phải danh sách.
    Chặn `gh` mà không chặn `gh.exe` là một lệnh cấm chỉ có hiệu lực trên POSIX.
    """
    if not argv0:
        return None
    # Dạng shell string: lấy token đầu. Không cố parse shell - chỉ cần biết binary nào được gọi.
    head = argv0.strip().split()[0] if argv0.strip() else ""
    head = os.path.basename(head.replace("\\", "/"))
    lowered = head.lower()
    for suffix in _WINDOWS_EXEC_SUFFIXES:
        if lowered.endswith(suffix):
            head = head[: -len(suffix)]
            break
    return head.lower() or None


def _scan_escape_paths(directory, allowed):
    """Đường thoát mà `Import`/`ImportFrom` KHÔNG thấy (finding wp77-g1-sec-02).

    Bắt ba lớp: import động có đích hằng, gọi tiến trình ngoài với argv[0] hằng nằm trong
    NETWORK_TOOLS, và `os.system`/`os.popen`.
    """
    offenders = []
    for name, tree in _parse_dir(directory):
        modules, funcs = _alias_map(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            called = _resolve_call(node.func, modules, funcs)
            # Tham số KEYWORD là cùng một lời gọi: `subprocess.run(args=[...])` và
            # `importlib.import_module(name="requests")` hợp lệ y hệt dạng vị trí. Chỉ đọc
            # `node.args` là bỏ lọt một nửa cách gọi hợp lệ của chính stdlib.
            keywords = {kw.arg: kw.value for kw in node.keywords if kw.arg}
            if called in ("importlib.import_module", "__import__") and (node.args or keywords):
                target = _const_str(node.args[0] if node.args else keywords.get("name"))
                if target and target.split(".")[0] in FORBIDDEN_IMPORTS:
                    entry = (name, "dynamic-import:%s" % target.split(".")[0])
                    if entry not in allowed:
                        offenders.append(entry)
            if called in ("os.system", "os.popen"):
                entry = (name, "shell:%s" % called)
                if entry not in allowed:
                    offenders.append(entry)
            if called and called.split(".")[0] == "subprocess" and (node.args or keywords):
                first = node.args[0] if node.args else keywords.get("args")
                argv0 = _const_str(first)
                if argv0 is None and isinstance(first, (ast.List, ast.Tuple)) and first.elts:
                    argv0 = _const_str(first.elts[0])
                tool = _tool_name(argv0)
                if tool in NETWORK_TOOLS:
                    entry = (name, "subprocess:%s" % tool)
                    if entry not in allowed:
                        offenders.append(entry)
    return offenders


_SENSITIVE_LITERAL = re.compile(r"^(GH_TOKEN|GITHUB_TOKEN|GITHUB_PAT|AWS_|ANTHROPIC_|OPENAI_)")


def _scan_unguarded_env_access(path):
    """Truy cập biến nhạy cảm NGOÀI một khối `with ... EnvGuard(...)` (finding wp77-g1-spec-02).

    Auditor chỉ ra `selftest.py:509` tự đọc đúng các biến cần bảo vệ TRƯỚC khi cài guard ở `:513`.
    Một suite làm vậy đang tự tay tạo ra lần đọc mà nó tuyên bố là không có. Phép quét này biến
    "đừng làm thế nữa" thành ràng buộc kiểm được.
    """
    with open(path, "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename=os.path.basename(path))
    modules, funcs = _alias_map(tree)

    guarded = []
    for node in ast.walk(tree):
        if isinstance(node, ast.With):
            if any("EnvGuard" in (_dotted(i.context_expr.func) or "")
                   for i in node.items if isinstance(i.context_expr, ast.Call)):
                guarded.append((node.body[0].lineno, node.end_lineno))

    def inside_guard(lineno):
        return any(start <= lineno <= end for start, end in guarded)

    offenders = []

    def note(lineno, what):
        if not inside_guard(lineno):
            offenders.append((lineno, what))

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            called = _resolve_call(node.func, modules, funcs)
            if called in ("os.getenv", "os.environ.get", "os.environ.pop", "os.environ.setdefault"):
                literal = _const_str(node.args[0]) if node.args else None
                if literal and _SENSITIVE_LITERAL.match(literal.upper()):
                    note(node.lineno, "%s(%r)" % (called, literal))
            if called in ("os.environ.update", "os.environ.copy"):
                note(node.lineno, "%s(...)" % called)
        elif isinstance(node, ast.Subscript) and _resolve_call(node.value, modules, funcs) == "os.environ":
            literal = _const_str(node.slice)
            if literal and _SENSITIVE_LITERAL.match(literal.upper()):
                note(node.lineno, "os.environ[%r]" % literal)
    return offenders
