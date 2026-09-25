#!/usr/bin/env python3
"""Sổ test sống: kiểm phạm vi, lời gọi CI, rc và bằng chứng dương."""
import argparse
import concurrent.futures
import contextlib
import datetime
import io
import json
import os
import pathlib
import re
import shlex
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import threading
import time

import yaml

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="backslashreplace")

ROOT = pathlib.Path(__file__).resolve().parents[2]
GOC = (".claude/dev", ".claude/hooks", ".githooks", ".github/checks", "scripts/tl_core")
OPS_REVIEWS = "ops/reviews/"
MOI_TRUONG_CI = "github-actions/linux"
MOI_TRUONG_WINDOWS = "github-actions/windows"
MOI_TRUONG_DA_BIET = frozenset({MOI_TRUONG_CI, MOI_TRUONG_WINDOWS})
LAUNCHER_WORKFLOW = ROOT / ".github/workflows/launcher-windows.yml"
CI_WORKFLOW = ROOT / ".github/workflows/ci.yml"
MOI = {
    ".claude/dev/chon_reviewer_test.py": r"(?s)nền: (\d+)/(\d+) đạt.*TỔNG: ĐẠT",
    ".claude/dev/gh_readback_test.py": r"gh_readback tests: (\d+)/(\d+) ca QUA \(hong 0\)",
    ".claude/dev/mcp_gh_test.py": r"(?s)CA\s+: (\d+)/(\d+) đạt · 0 đỏ · ĐẠT.*ĐỘT BIẾN.*ĐẠT.*TỔNG: ĐẠT",
    ".claude/dev/mcp_github_doc_test.py": r"mcp_github_doc tests: (\d+)/(\d+) ca QUA \(hong 0, bo qua 0\)",
    ".claude/dev/probe_mang_test.py": r"(?s)tự đột biến cổng: 9/9 chết.*named mutant probe_missing_tool_executes_git: 1/1 chết.*nền: 11/11 đạt.*TỔNG: ĐẠT",
    # GIU NGUYEN `\d+` — M4 dong bang hanh vi Linux, va mau nay la duong Linux di qua.
    # Lo #319 (`0/0 bi giet` lot vi `bang_chung_xanh` chi soi hai nhom CA) CO THAT va
    # co SAN tu base, nhung bit no o day la doi hanh vi Linux — ngoai pham vi packet
    # #456. Chot tuong duong duoc dat o duong WINDOWS (`MOI_WINDOWS`), la noi dot bien
    # bat buoc cua A2 thuc su bieu hien. Lo phia Linux de lai cho packet ke.
    ".claude/hooks/pretooluse_guard_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
    ".claude/hooks/subagent_ghi_detect_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
    "ops/nhanh_don_duoc_test.py": r"^(\d+)/(\d+)$",
}
# Tap mau THAY THE, chi dung khi nen dang chay la Windows. Windows nhan HAI dang:
#   (a) dong da cat dot bien;  (b) dong Linux day du — ai do chay tay do du van DAT (A3).
# CA HAI deu doi so dot bien KHAC 0 (`[1-9]\d*`). Do la chot tuong duong `len(DOT_BIEN)>0`
# o tang so dang ky, va la thu giet dot bien bat buoc thu hai cua A2 (nhanh Windows in
# `DOT BIEN 0/0 bi giet`). Dat o DAY chu khong o `MOI` vi dot bien ay bieu hien tren
# WINDOWS; siet `MOI` se doi hanh vi Linux, trai M4 (finding P2 cross-review luot 1).
MOI_WINDOWS = {
    ".claude/hooks/pretooluse_guard_test.py": (
        r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN [1-9]\d* muc KHONG DO TREN WINDOWS"
        r".*TONG: DAT",
        r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN [1-9]\d*/[1-9]\d* bi giet"
        r".*TONG: DAT",
    ),
}
CACH_LY = {}
DA_NOI = {
    ".claude/dev/ci_dang_ky_test.py",
    ".claude/dev/codex_cred_test.py", ".claude/dev/gate_lifecycle_test.py",
    ".claude/dev/idiom_py_test.py", ".claude/dev/launcher_test.py",
    ".claude/dev/packet_loop_test.py", ".githooks/eol_policy_test.py",
    ".githooks/pre_push_test.py", ".github/checks/ci_phamvi_test.py",
    "ops/bien_nhan_v2_test.py",
    "ops/cong_cu_test.py", "ops/lease_publish_test.py",
    "scripts/tl_core/command_registry_test.py",
}
DANG_KY = set(MOI) | DA_NOI


def tim(root):
    """Trả (test sống, hiện vật, vị trí lạ); ops chỉ nhận tệp mức đỉnh."""
    song, hien_vat, la = set(), set(), set()
    for p in root.rglob("*_test.py"):
        q = p.relative_to(root).as_posix()
        if q.startswith(OPS_REVIEWS):
            hien_vat.add(q)
        elif any(q.startswith(g + "/") for g in GOC) or (q.startswith("ops/") and q.count("/") == 1):
            song.add(q)
        else:
            la.add(q)
    return song, hien_vat, la


def bi_tat(x): return x is False or (isinstance(x, str) and x.strip().lower() in ("false", "${{ false }}"))


def _runner_matrix_dung(expr):
    if not isinstance(expr, str) or "fromJSON(" not in expr:
        return False
    compact = re.sub(r"\s+", " ", expr)
    if not all(x in compact for x in ("github.event_name", "workflow_dispatch",
                                       "inputs.runner_set", "windows-only")):
        return False
    try:
        arrays = [json.loads(x) for x in re.findall(r"'(\[[^']*\])'", expr)]
    except json.JSONDecodeError:
        return False
    return arrays == [["windows-latest"], ["windows-latest", "ubuntu-latest"]]


def _python_matrix_dung(expr):
    if not isinstance(expr, str):
        return False
    compact = re.sub(r"\s+", " ", expr)
    windows = re.search(r"matrix\.os\s*==\s*'windows-latest'.*'3\.13'.*'3\.11'", compact)
    ubuntu = re.search(r"matrix\.os\s*==\s*'ubuntu-latest'.*'3\.11'.*'3\.13'", compact)
    return bool(windows or ubuntu)


def loi_launcher_windows(source=None):
    source = LAUNCHER_WORKFLOW.read_text(encoding="utf-8") if source is None else source
    try:
        data = yaml.safe_load(source) or {}
    except yaml.YAMLError as e:
        return [f"launcher Windows YAML lỗi: {e}"], 1
    triggers = data.get("on", data.get(True))
    if not isinstance(triggers, dict):
        return ["launcher Windows thiếu trigger map"], 1
    dispatch = triggers.get("workflow_dispatch")
    runner = ((dispatch or {}).get("inputs") or {}).get("runner_set") if isinstance(dispatch, dict) else None
    expected = {"required": True, "default": "windows-only", "type": "choice",
                "options": ["windows-only", "windows-and-ubuntu"]}
    job = ((data.get("jobs") or {}).get("launcher") or {})
    matrix = ((job.get("strategy") or {}).get("matrix") or {}).get("os")
    setup = next((s for s in (job.get("steps") or [])
                  if isinstance(s, dict) and s.get("uses") == "actions/setup-python@v5"), {})
    checks = [
        (isinstance(runner, dict) and all(runner.get(k) == v for k, v in expected.items()),
         "launcher Windows sai hợp đồng workflow_dispatch.runner_set"),
        (all(name in triggers for name in ("push", "pull_request")),
         "launcher Windows thiếu hợp đồng non-dispatch"),
        (_runner_matrix_dung(matrix), "launcher Windows sai ánh xạ runner dispatch/non-dispatch"),
        (_python_matrix_dung((setup.get("with") or {}).get("python-version")),
         "launcher Windows sai ánh xạ Python Windows=3.13 Ubuntu=3.11"),
    ]
    return [message for ok, message in checks if not ok], len(checks)


_TIEN_TO_CAI = (["pip"], ["pip3"], ["uv", "pip"],
                ["python", "-m", "pip"], ["python3", "-m", "pip"])
_TUY_CHON_AN_TOAN = frozenset({"--quiet", "-q", "--no-cache-dir",
                               "--disable-pip-version-check", "--no-input"})
_TEN_GOI = re.compile(r"^([A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?)(?:\[([A-Za-z0-9](?:[A-Za-z0-9._,-]*[A-Za-z0-9])?)\])?(.*)$")
_TRINH_PY = re.compile(r"^python(?:3(?:\.\d+)?)?$")

def _cuoi_thay_lenh(run, start):
    """Tìm biên $(...) theo quote/ngoặc; không thực thi nội dung."""
    i, depth, quote, word = start + 2, 1, "", False
    while i < len(run):
        c = run[i]
        if c == "\\" and quote != "'":
            word |= run[i + 1:i + 2] != "\n"
            i += 2
            continue
        if quote:
            if c == quote: quote = ""
        elif c == "#" and not word:
            end = run.find("\n", i)
            i = len(run) if end < 0 else end
            continue
        elif c in "'\"": quote = c
        elif c == "(": depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0: return i
        word = bool(quote) or c not in " \t\n;|&()"
        i += 1
    raise ValueError("command substitution chưa đóng")


def _kiem_khuon_shell(items):
    """Opaque vẫn phải thuộc grammar: list, if/then/elif/else/fi, nhóm { list; }.
    Mỗi condition/body phải có lệnh; không nhận compound trong condition hoặc header lồng inline.
    """
    stack = []
    for argv, op, key in items:
        tail = argv[1:] if key else argv
        if key in ("if", "{"):
            if stack and stack[-1][1] == "condition": raise ValueError("compound trong condition ngoài miền")
            stack.append([key, "condition" if key == "if" else "group", False])
        elif key in ("then", "elif", "else", "fi", "}"):
            if not stack: raise ValueError("từ khóa đóng không có khối")
            frame = stack[-1]
            expected = {"then": {"condition"}, "elif": {"body"}, "else": {"body"},
                        "fi": {"body", "else"}, "}": {"group"}}[key]
            if frame[1] not in expected or not frame[2]: raise ValueError("khối sai thứ tự hoặc rỗng")
            if key in ("fi", "}"):
                if tail: raise ValueError("đối số sau từ khóa đóng")
                stack.pop()
                if stack: stack[-1][2] = True
                continue
            frame[1], frame[2] = {"then": "body", "elif": "condition", "else": "else"}[key], False
        elif key or argv[0] in _KHUNG_SHELL:
            raise ValueError("cấu trúc shell ngoài miền")
        if key and not tail and op != "\n": raise ValueError("header thiếu lệnh")
        if key and tail and tail[0] in _KHUNG_SHELL: raise ValueError("header lồng inline ngoài miền")
        if tail and stack: stack[-1][2] = True
    if stack: raise ValueError("khối shell chưa đóng")


def _dong_logic(run, depth=0):
    """Lexer đóng cho lệnh trực tiếp và cấu trúc opaque do _kiem_khuon_shell nhận.
    Giữ cờ ngoài miền cùng argv; không dựng argv bằng split() khi lexer thất bại.
    Heredoc là dữ liệu của lệnh gọi: bỏ qua thân, không nhận mã nhúng thành lệnh shell.
    """
    if depth > 16: raise ValueError("lồng command substitution ngoài miền")
    out, cur, quote, bad, before, here, i = [], "", "", False, False, None, 0
    need, compound, word, items = False, False, False, []
    def emit(op=""):
        nonlocal cur, bad, before, need, compound, word
        argv = shlex.split(cur)
        if op not in ("", "\n", ";", "&", "&&", "|", "||"): raise ValueError("toán tử ngoài miền")
        if not argv and op not in ("", "\n"): raise ValueError("thiếu lệnh")
        if argv:
            key = argv[0] if argv[0] in _KHUNG_SHELL and re.match(re.escape(argv[0]) + r"(?:\s|$)", cur.lstrip()) else ""
            if need and key in ("then", "elif", "else", "fi", "}"): raise ValueError("thiếu toán hạng trước từ khóa")
            items.append((argv, op, key))
            need = op in ("&&", "||", "|")
        after = op not in ("", "\n", ";", "&&")
        compound |= after
        if argv: out.append((argv, bad or before or after))
        cur, bad, before, word = "", False, after, False
    run = run or ""
    while i < len(run):
        c = run[i]
        if not quote and ord(c) < 32 and c not in "\n\t":
            raise ValueError("ký tự điều khiển ngoài miền")
        if c == "\\" and quote != "'":
            if i + 1 == len(run): raise ValueError("escape chưa đóng")
            nxt = run[i + 1]
            if not quote and ord(nxt) < 32 and nxt not in "\n\t":
                raise ValueError("ký tự điều khiển escape ngoài miền")
            if nxt != "\n": cur += c + nxt; word = True
            i += 2; continue
        if quote != "'" and c == "$":
            while run[i + 1:i + 3] == "\\\n": run = run[:i + 1] + run[i + 3:]
            nxt = run[i + 1:i + 2]
            if nxt == "[" or (not quote and nxt in ("'", '"')):
                raise ValueError("expansion ngoài miền")
        if quote != "'" and run[i:i + 2] == "${":
            m = re.match(r"\$\{[A-Za-z_][A-Za-z0-9_]*(?::-[A-Za-z0-9_ ./+-]*)?\}", run[i:])
            if m is None: raise ValueError("parameter expansion ngoài miền hoặc chưa đóng")
            cur += "__THAM_SO__"; bad = True; word = True; i += m.end()
            continue
        if quote != "'" and run[i:i + 2] == "$(":
            end = _cuoi_thay_lenh(run, i)
            inner = _dong_logic(run[i + 2:end], depth + 1)
            if any(_nhan_lenh(t).related for t, _ in inner):
                raise ValueError("lệnh liên quan trong command substitution ngoài miền")
            # Chỉ giá trị opaque được bỏ qua; argv động của installer vẫn mang cờ bad.
            cur += "__THAY_LENH__"; bad = True; word = True; i = end + 1
            continue
        if quote != "'" and c == "`": raise ValueError("backtick ngoài miền")
        if quote:
            cur += c
            if c == quote: quote = ""
            elif quote == '"' and c in "$`": bad = True
        elif c in "'\"":
            quote = c; cur += c
        elif c == "#" and not word:
            while i < len(run) and run[i] != "\n": i += 1
            continue
        elif c in "()":
            raise ValueError("ngoặc trần ngoài miền lệnh đơn")
        elif run[i:i + 2] == "<<":
            m = re.match(r"<<(-?)[ \t]*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2", run[i:])
            if m is None or here is not None: raise ValueError("heredoc ngoài miền")
            if i + m.end() < len(run) and run[i + m.end()] not in " \t\n;&|<>": raise ValueError("delimiter heredoc ngoài miền")
            here = (m[3], bool(m[1]), bool(m[2])); bad = True; word = True; cur += " <heredoc>"
            i += m.end(); continue
        elif c in "<>":
            end = i + 1
            while end < len(run) and run[end] in "<>": end += 1
            if run[i:end] not in ("<", ">", ">>"): raise ValueError("redirect ngoài miền")
            target = end
            while target < len(run):
                if run[target] in " \t": target += 1
                elif run[target:target + 2] == "\\\n": target += 2
                else: break
            if target == len(run) or run[target] in "\n;|&<>#": raise ValueError("redirect thiếu đích")
            cur += run[i:end]; bad = True; word = False; i = end
            continue
        elif c in ";&|\n":
            end = i + 1
            if c != "\n":
                while end < len(run) and run[end] in ";&|": end += 1
            emit(run[i:end]); i = end
            if c == "\n" and here:
                tag, tabs, quoted = here; here = None
                carry = ""
                while i < len(run):
                    end = run.find("\n", i); end = len(run) if end < 0 else end
                    line = run[i:end]; i = min(end + 1, len(run))
                    if not carry and (line.lstrip("\t") if tabs else line) == tag: break
                    scan_line = line.lstrip("\t") if tabs else line
                    logical = carry + scan_line
                    if not quoted and ("$(" in logical or "`" in logical):
                        raise ValueError("heredoc có command substitution ngoài miền")
                    slashes = len(logical) - len(logical.rstrip("\\"))
                    carry = logical[:-1] if not quoted and slashes % 2 else ""
                else: raise ValueError("heredoc chưa đóng")
            continue
        else:
            cur += c
            if c in "$`()<>*?[]{}": bad = True
            if c in "{}": compound = True
        word = bool(quote) or c not in " \t"
        i += 1
    if quote or here: raise ValueError("trích dẫn chưa đóng")
    emit()
    if need: raise ValueError("thiếu vế phải toán tử")
    _kiem_khuon_shell(items)
    control = {"if", "then", "elif", "else", "fi", "for", "while", "until", "do", "done", "case", "esac", "function", "select", "coproc", "time", "!", "[[", "]]"}
    conditional = compound or any(t[0] in control for t, _ in out)
    return [(t, b or conditional) for t, b in out]

def _doi_so_python(tok):
    if not tok or not _TRINH_PY.fullmatch(tok[0]): return None
    i = 1
    while i < len(tok):
        if tok[i] in ("-u", "-B", "-I", "-E", "-s", "-S", "-O", "-OO", "-q"): i += 1
        elif tok[i:i + 2] == ["-X", "utf8"]: i += 2
        else: break
    return tok[i:]

def _lenh_ruff(tok):
    for prefix in (["ruff"], ["uv", "run", "ruff"], ["uvx", "ruff"]):
        if tok[:len(prefix)] == prefix: return tok[len(prefix):]
    p = _doi_so_python(tok) or []
    if p[:2] == ["-m", "ruff"]: return p[2:]
    if p[:1] == ["-mruff"]: return p[1:]
    return None

def _chuan_ten(t):
    return re.sub(r"[-_.]+", "-", t.lower())

class _LenhRuff:
    """Một kết quả nhận dạng dùng chung; KHONG chỉ được cấp cho dạng đã nhận biết."""
    def __init__(self, kind="KHONG", probe=False, registry=0, related=False):
        self.kind, self.probe, self.registry, self.related = kind, probe, registry, related


# Đây là grammar của lệnh ngoài phạm vi cài đặt, không phải danh sách cấm installer.
# Chương trình/script được gọi là opaque theo chỉ thị chủ kho; không giải nghĩa thân.
_LENH_OPAQUE = frozenset({
    "git", "echo", "printf", "cat", "set", "test", "[", "exit", "return", "true", "false",
    "mkdir", "pwd", "ls", "wc", "sed", "awk", "rg", "chmod", "chown", "id", "cp", "mv", "rm", "sleep",
    "actionlint", "shellcheck", "bash", "sh", "pwsh", "powershell", "node",
})
_KHUNG_SHELL = frozenset({"if", "then", "elif", "else", "fi", "for", "while", "until", "do", "done",
                         "case", "esac", "function", "select", "coproc", "time", "!", "{", "}"})


def _ten_tep(t):
    return t.replace("\\", "/").rsplit("/", 1)[-1]


def _cai_truc_tiep(args):
    """Nhận dạng họ installer đã xảy ra TRƯỚC khi kiểm grammar đối số."""
    if args in (["--version"], ["-V"]):
        return _LenhRuff(related=True)
    if args[:1] != ["install"]:
        return _LenhRuff("KHONG_PHAN_TICH_DUOC", related=True)
    args = args[1:]
    reqs = [t for t in args if not t.startswith("-")]
    if not reqs or any(t.startswith("-") and t not in _TUY_CHON_AN_TOAN for t in args):
        return _LenhRuff("KHONG_PHAN_TICH_DUOC", related=True)
    parsed = [_TEN_GOI.fullmatch(t) for t in reqs]
    if any(m is None or m[3].startswith("[") for m in parsed):
        return _LenhRuff("KHONG_PHAN_TICH_DUOC", related=True)
    if any(m[2] and any(not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?", x)
                       for x in m[2].split(",")) for m in parsed):
        return _LenhRuff("KHONG_PHAN_TICH_DUOC", related=True)
    ruff = [m for m in parsed if _chuan_ten(m[1]) == "ruff"]
    if not ruff:
        # Các package khác chỉ nhận tên/extras và pin literal; URL/file/marker là ngoài miền.
        valid = all(not m[3] or re.fullmatch(r"==[A-Za-z0-9.+_-]+", m[3]) for m in parsed)
        return _LenhRuff("KHONG" if valid else "KHONG_PHAN_TICH_DUOC", related=True)
    if len(reqs) != 1:
        return _LenhRuff("KHONG_PHAN_TICH_DUOC", related=True)
    return _LenhRuff("GHIM" if ruff[0][3] == "==0.15.15" else "KHONG_GHIM", related=True)


def _nhan_lenh(tok):
    """Phân hoạch đóng: invocation được nhận, chương trình opaque, hoặc ngoài miền."""
    unknown = _LenhRuff("KHONG_PHAN_TICH_DUOC", related=True)
    if not tok:
        return _LenhRuff()
    if tok[0] in _KHUNG_SHELL:
        inner = _nhan_lenh(tok[1:])
        return unknown if inner.related else inner
    if tok[0] == "sudo":
        inner = _nhan_lenh(tok[1:])
        return unknown if inner.related else inner
    py = _doi_so_python(tok)
    if py is not None:
        if py[:1] in (["-c"], ["-"]) or py in (["--version"], ["-V"], ["--help"], ["-h"]):
            return _LenhRuff()
        if py[:2] == ["-m", "py_compile"]:
            return _LenhRuff()
        if py[:2] == ["-m", "pip"]:
            return _cai_truc_tiep(py[2:])
        if py[:1] == ["-mpip"]:
            return _cai_truc_tiep(py[1:])
        module = py[:2] == ["-m", "ci_dang_ky_test"] or py[:1] == ["-mci_dang_ky_test"]
        file = bool(py) and _ten_tep(py[0]) == "ci_dang_ky_test.py"
        if module or file:
            tail = py[2:] if py[:1] == ["-m"] else py[1:]
            return _LenhRuff(registry=1 if tail == ["--chay"] else -1, related=True)
        if py and not py[0].startswith("-") and _ten_tep(py[0]).endswith(".py"):
            return _LenhRuff()
    probe = _lenh_ruff(tok)
    if probe is not None:
        return _LenhRuff(probe=probe == ["--version"], related=True)
    if tok[0] in ("pip", "pip3"):
        return _cai_truc_tiep(tok[1:])
    if tok[:2] == ["uv", "pip"]:
        return _cai_truc_tiep(tok[2:])
    # Ngoài whitelist không được suy KHONG từ việc không nhìn thấy token Ruff.
    # Vì vậy global option, đường dẫn executable lạ và installer chưa biết đều đỏ,
    # kể cả khi tên package nằm trong đối số động hoặc requirements file.
    if tok[0] in _LENH_OPAQUE or _ten_tep(tok[0]).endswith((".sh", ".ps1", ".py", ".js")):
        return _LenhRuff()
    if all(re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t) for t in tok):
        return _LenhRuff()
    return unknown


def _doc_run_ruff(run):
    """Một lần tokenize/nhận dạng cho cả ba consumer: pin, probe và registry."""
    order = {"KHONG": 0, "GHIM": 1, "KHONG_GHIM": 2, "KHONG_PHAN_TICH_DUOC": 3}
    result, trace, pinned, probe, registry, any_probe = "KHONG", None, False, False, 0, False
    try:
        commands = _dong_logic(run)
    except ValueError as exc:
        return "KHONG_PHAN_TICH_DUOC", str(exc), False, -1, False
    for tok, bad in commands:
        item = _nhan_lenh(tok)
        kind = "KHONG_PHAN_TICH_DUOC" if bad and item.related else item.kind
        if order[kind] > order[result]:
            result, trace = kind, " ".join(tok)
        if kind == "GHIM":
            pinned = True
        if not bad and item.probe and pinned:
            probe = True
        any_probe |= not bad and item.probe
        flag = -1 if bad and item.registry else item.registry
        if flag == -1 or registry == -1:
            registry = -1
        elif flag == 1:
            registry = 1
    return result, trace, probe, registry, any_probe


def _phan_loai_cai_ruff(run):
    return _doc_run_ruff(run)[:2]


def _buoc_co_dieu_kien(step):
    return step.get("if") is not None


def _shell_trong_mien(data, job, step):
    """Giải ưu tiên step → job → workflow; khai shell thì phải là chuỗi trong miền."""
    try:
        scopes = (step, job.get("defaults", {}).get("run", {}), data.get("defaults", {}).get("run", {}))
    except AttributeError:
        return False
    if any(not isinstance(scope, dict) for scope in scopes): return False
    for scope in scopes:
        if "shell" in scope:
            if scope["shell"] in ("pwsh", "powershell"):
                body = step.get("run", "")
                lines = body.split("\n") if body else []
                if body.endswith("\n"): lines.pop()
                return bool(lines) and all(re.fullmatch(
                    r"[ \t]*[A-Za-z_][A-Za-z0-9_./-]*(?:[ \t]+[A-Za-z0-9_./:=+-]+)*[ \t]*", line)
                    and line.split()[0].lower() not in _KHUNG_SHELL | {"return", "exit"} for line in lines)
            return scope["shell"] in ("bash", "sh")
    return True


def _doc_buoc_ruff(data, job, step):
    # Ngôn ngữ phải được nhận TRƯỚC khi đọc thân: không dùng kết quả misparse để miễn kiểm.
    if "run" in step and not _shell_trong_mien(data, job, step):
        return "KHONG_PHAN_TICH_DUOC", "shell ngoài miền", False, -1, False
    return _doc_run_ruff(step.get("run", ""))


def loi_ruff_ci(source=None):
    """M7/A7: chỉ lệnh trực tiếp trong YAML, không suy hành vi bên trong script được gọi.
    Miền: các mẫu argv tĩnh dưới đây và lệnh opaque trong grammar đóng của _dong_logic;
    mọi run ngoài grammar đều bị từ chối trước khi phân loại cài đặt, không mô phỏng runtime.
    Opaque: _LENH_OPAQUE, script/Python -c/stdin, assignment; không đọc thân script/env.
    List nhận newline/;/&&/||/|/& đủ hai vế, redirect </>/>> có đích, if/then/elif/else/fi
    và { list; } cân bằng với condition/body khác rỗng; compound chỉ dành cho opaque.
    Parameter nhận $TEN (ASCII), $0..$9/$@/$*/$#/$?/$-/$! /$$, ${TEN} hoặc ${TEN:-literal}
    với literal gồm chữ/số/_/space/./slash/+/-; kể cả trong nháy kép. $[ bị từ chối cả trong
    nháy kép; $' và $" ngoài nháy bị từ chối (không hỗ trợ ANSI-C/locale/arithmetic).
    Ngoài các tiền tố expansion được kiểm, $ là literal; quote/escape giữ dữ liệu nguyên dạng.
    Quoting và nối dòng theo POSIX hạn chế nêu trên.
    $(...) chỉ nhận lệnh opaque được phân tích đệ quy; backtick và heredoc động bị từ chối.
    Ngoặc trần, C0 ngoài nháy (trừ tab/newline) bị từ chối; dữ liệu nháy/heredoc giữ nguyên.
    Comment chỉ mở tại đầu từ chưa quote/escape, kể cả trong $(...).
    Shell không khai hoặc bash/sh dùng grammar trên. pwsh/powershell chỉ nhận ít nhất một
    invocation/dòng LF bằng từ ASCII theo _shell_trong_mien, không quote/expansion/toán tử/khối;
    không hỗ trợ cú pháp PowerShell tổng quát. Shell khác/null/template ngoài miền.
    Mọi bước run đều qua chốt shell trước khi phân tích thân, kể cả thân opaque/rỗng.
    Cài: pip/pip3, uv pip, python [cờ] -m pip + install + cờ cho phép + một Ruff requirement.
    Extras phải quote; global option trước install bị từ chối, không biến thành KHONG.
    Probe: ruff / python [cờ] -m ruff / uv run ruff / uvx ruff, hậu tố đúng --version.
    Registry: python [cờ] <đường dẫn ci_dang_ky_test.py> hoặc -m ci_dang_ky_test, đúng --chay.
    """
    source = CI_WORKFLOW.read_text(encoding="utf-8") if source is None else source
    try: data = yaml.safe_load(source) or {}
    except yaml.YAMLError as e: return [f"CI YAML lỗi khi kiểm Ruff: {e}"], 1
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), dict): return ["CI YAML thiếu jobs"], 3
    if any(not isinstance(j, dict) or not isinstance(j.get("steps"), list) for j in data["jobs"].values()):
        return ["CI YAML jobs/steps ngoài miền"], 3
    jobs = data["jobs"]
    if any(not isinstance(s, dict) or ("run" in s and not isinstance(s["run"], str))
           for j in jobs.values() for s in j["steps"]):
        return ["CI YAML step/run ngoài miền"], 3
    steps = {jn: [s for s in j.get("steps", []) if isinstance(s, dict)] for jn, j in jobs.items()}
    parsed = {jn: [_doc_buoc_ruff(data, jobs[jn], s) for s in bs] for jn, bs in steps.items()}
    kinds = {jn: [p[0] for p in ps] for jn, ps in parsed.items()}
    for jn, ks in kinds.items():
        for i, kind in enumerate(ks):
            if kind != "KHONG" and (_buoc_co_dieu_kien(steps[jn][i]) or jobs[jn].get("if") is not None):
                ks[i] = "KHONG_PHAN_TICH_DUOC"
    installs = [jn for jn, ks in kinds.items() if any(k != "KHONG" for k in ks)]
    bad_pin = [jn for jn in installs if "GHIM" not in kinds[jn] or any(k not in ("KHONG", "GHIM") for k in kinds[jn])]
    bad_probe = []
    for jn in installs:
        pinned, probed = False, False
        for i, kind in enumerate(kinds[jn]):
            if not _buoc_co_dieu_kien(steps[jn][i]):
                probed |= parsed[jn][i][2] or (pinned and parsed[jn][i][4])
                pinned |= kind == "GHIM"
        if not probed: bad_probe.append(jn)
    registry = {jn: [p[3] for p in ps] for jn, ps in parsed.items()}
    callers = [jn for jn, flags in registry.items() if 1 in flags]
    before = False
    if len(callers) == 1 and not any(-1 in flags for flags in registry.values()):
        jn = callers[0]; gi = registry[jn].index(1)
        ri = next((i for i, k in enumerate(kinds[jn]) if k == "GHIM"), -1)
        before = (0 <= ri < gi and not _buoc_co_dieu_kien(steps[jn][gi])
                  and jobs[jn].get("if") is None)
    outside = [f"{jn}/bước {i + 1}" for jn, ks in kinds.items() for i, k in enumerate(ks) if k == "KHONG_PHAN_TICH_DUOC"]
    reason = f"; ngoài miền cú pháp: {outside}" if outside else ""
    checks = [
        (installs and not bad_pin, f"CI không chứng minh ghim Ruff 0.15.15 (job: {bad_pin or 'không job nào cài Ruff'}{reason})"),
        (installs and not bad_probe, f"CI không in probe Ruff --version (job: {bad_probe or 'không job nào cài Ruff'})"),
        (before, "CI không provision Ruff trước test registry trong cùng job "
                 f"(job chạy test registry: {callers or 'KHÔNG CÓ'})"),
    ]
    return [message for ok, message in checks if not ok], len(checks)

def giet_windows_311_launcher_workflow(source):
    anchor = "'3.13'"
    if source.count(anchor) != 1:
        return False
    mutant = source.replace(anchor, "'3.11'", 1)
    return bool(loi_launcher_windows(mutant)[0])

def kiem(root=ROOT, registry=DANG_KY, workflows=None, cach_ly=CACH_LY):
    song, _, la = tim(root)
    loi = []
    loi += ["test sống chưa đăng ký: " + x for x in sorted(song - registry)]
    loi += ["mục đăng ký không có tệp: " + x for x in sorted(registry - song)]
    loi += ["test ở vị trí chưa biết: " + x for x in sorted(la)]
    loi += ["cách ly không nằm trong sổ: " + x for x in sorted(set(cach_ly) - registry)]
    for x, no in cach_ly.items():
        if not all(no.get(k) for k in ("slug", "ly_do", "moi_truong", "log")):
            loi.append("cách ly thiếu slug, lý do, môi trường hoặc log: " + x)
        elif no["moi_truong"] not in MOI_TRUONG_DA_BIET:
            loi.append("cách ly có môi trường không hợp lệ: " + x)
    if workflows is None:
        runs = []
        for p in (root / ".github/workflows").glob("*.yml"):
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            for job in (data.get("jobs") or {}).values():
                if not isinstance(job, dict) or bi_tat(job.get("if")): continue
                for step in (job.get("steps") or []):
                    if isinstance(step, dict) and not bi_tat(step.get("if")) and isinstance(step.get("run"), str):
                        runs.extend(line for line in step["run"].splitlines()
                                    if not line.lstrip().startswith("#"))
        workflows = "\n".join(runs)
    for x in sorted(DA_NOI):
        if x == ".claude/dev/ci_dang_ky_test.py":
            co = "python .claude/dev/ci_dang_ky_test.py --chay" in workflows
        elif x == "ops/lease_publish_test.py":
            co = "ops/chay_lease_publish_test.sh" in workflows
        else:
            co = x in workflows
        if not co:
            loi.append("CI không gọi mục đăng ký: " + x)
    if "python .claude/dev/ci_dang_ky_test.py --chay" not in workflows:
        loi.append("CI không gọi nhóm đăng ký mới")
    return loi, len(song), len(registry)


def bang_chung_xanh(text, mau):
    m = re.search(mau, text, re.M)
    if not m:
        return False
    return not m.groups() or len(m.groups()) != 2 or (int(m.group(1)) > 0 and m.group(1) == m.group(2))


def moi_truong_hien_tai(env=os.environ):
    """Chỉ nhận diện khi cả hai dấu hiệu runner chuẩn cùng khớp."""
    if env.get("GITHUB_ACTIONS") == "true" and env.get("RUNNER_OS") in ("Linux", "Windows"):
        return f"github-actions/{env['RUNNER_OS'].lower()}"
    return None


def nen_la_windows(ten_nen=None):
    """Nen CHAY THAT cua tien trinh nay — KHONG phai nen CI khai trong bien moi truong.

    Phai hoi `os.name`, dung hoi `moi_truong_hien_tai()`: bo test con chay CUNG mot OS
    voi so dang ky nay, va no quyet dinh in dong Windows theo `os.name`. Neu hoi bien CI
    thi mot luot chay TAY tren may Windows (khong co GITHUB_ACTIONS) se bi coi la
    khong-Windows, va dong hop le cua no bi cham DO — do la lam tron XUONG, cung ho voi
    loi lam tron LEN ma `dem_la_do` sinh ra de chan.
    """
    return (os.name if ten_nen is None else ten_nen) == "nt"


def mau_theo_nen(path, mau, la_windows):
    """Tap mau duoc chap nhan cho `path` tren nen dang chay.

    Windows dung tap THAY THE trong `MOI_WINDOWS` — KHONG kem `mau` goc. Co chu dich:
    tap ay da chua dang Linux (sieu chat hon), nen A3 "dong Linux tren nen Windows van
    DAT" van giu, DONG THOI `0/0 bi giet` bi tu choi tren Windows. Neu kem ca `mau` goc
    thi mau long se nhan `0/0` va dot bien bat buoc thu hai cua A2 SONG.

    Nen khac: chi `mau` goc, khong doi mot chut nao so voi base (M4).
    """
    mau_nen = MOI_WINDOWS.get(path)
    return list(mau_nen) if (la_windows and mau_nen) else [mau]


def cach_ly_chap_nhan(ok, da_neo, hien_tai):
    """OS đã biết khác neo dùng kết quả thật; nền lạ vẫn không được làm tròn lên."""
    if hien_tai is None:
        return None
    if hien_tai == da_neo:
        return not ok
    return ok if hien_tai in MOI_TRUONG_DA_BIET else None


def trong_ci(env=os.environ):
    """Có đang chạy TRONG CI không — ĐỘC LẬP với `moi_truong_hien_tai`.

    Hai câu hỏi khác nhau và phải hỏi riêng: `moi_truong_hien_tai` hỏi *"nền nào"*
    và đòi CẢ `RUNNER_OS == Linux`, nên trên `windows-latest` nó trả None. Nếu dùng
    nó để suy ra "có ở CI không" thì Windows bị coi là ngoài CI và cổng lại làm tròn
    lên đúng như cũ.
    """
    return env.get("GITHUB_ACTIONS") == "true"


def dem_la_do(chap_nhan, o_trong_ci):
    """Phán quyết CÓ TÍNH LÀ ĐỎ KHÔNG — bất biến nằm ở TẦNG TIÊU THỤ.

    `cach_ly_chap_nhan` đã trung thực trả None cho trạng thái thứ ba, và đột biến
    `r4-khong-do-duoc-thanh-dat` canh đúng điều đó. Nhưng chỗ LÀM TRÒN LÊN nằm ở nơi
    TIÊU THỤ giá trị ấy, nên bất biến phải được cưỡng chế ở đây, nếu không ta chỉ có
    thêm một bảo chứng giả thứ hai (#401).

    None trong CI ⇒ ĐỎ (fail-closed). None ngoài CI ⇒ không đỏ: chạy cục bộ cũng giải
    ra None, làm đỏ ở đó thì mọi lượt `--chay` trên máy lập trình viên đỏ vĩnh viễn.
    """
    if chap_nhan is None:
        return bool(o_trong_ci)
    return not chap_nhan


# CI-SONG-SONG-REGISTRY-G5-MOT-LAN r1 (#637): M1–M3, M6, M7. Hằng số trong W1 theo spec M3.
GIAY_TOI_DA_MOT_BO, GIAY_CHO_CAY_DUNG, BIEN_WORKERS, _RE_ISO_UTC = 1800, 10, "CI_DANG_KY_WORKERS", re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z$")


def _gio_utc(): return datetime.datetime.now(datetime.timezone.utc)
def _iso(dt): return dt.astimezone(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def doc_so_worker(env=os.environ, la_windows=None):
    """M3 miền N: vắng/rỗng ⇒ 1; đúng một chữ số 1–8 ⇒ N; khác ⇒ ValueError. Windows ⇒ 1 (Q6)."""
    raw = env.get(BIEN_WORKERS) or "1"
    if not re.fullmatch(r"[1-8]", raw):
        raise ValueError(f"{BIEN_WORKERS}={raw!r} ngoài miền 1–8")
    return 1 if nen_la_windows(la_windows) else int(raw)


def _pid_song(pid, pgid=None):
    """Có tiến trình KHÔNG-zombie mang `pid` (hoặc thuộc nhóm `pgid`)? ZOMBIE tính là đã chết:
    trong container PID 1 có thể không thu hồi cháu mồ côi, và `kill(pid, 0)` vẫn thành công."""
    proc = pathlib.Path("/proc")
    if not proc.is_dir():  # POSIX không /proc: không lọc được zombie ⇒ nghiêng về "còn sống" (ĐỎ)
        return not subprocess.call(["kill", "-0", f"-{pgid}" if pid is None else str(pid)], stderr=subprocess.DEVNULL)
    for st in ([proc / str(pid) / "stat"] if pgid is None else proc.glob("[0-9]*/stat")):
        try:
            f = st.read_text().rsplit(")", 1)[1].split()
        except (OSError, IndexError):
            continue
        if f[0] != "Z" and (pgid is None or int(f[2]) == pgid):
            return True
    return False


def _chay_co_lap(argv, cwd=ROOT, goc_tam=None, gioi_han=GIAY_TOI_DA_MOT_BO):
    """M2+M3: một bộ, một subprocess, BẢN SAO env có TMPDIR/TEMP/TMP riêng; không đụng
    `os.environ`/cwd của cha. Trả `(rc, ban_in, loi_ha_tang)`; `loi_ha_tang` khác None ⇒ ĐỎ."""
    tam, posix = pathlib.Path(tempfile.mkdtemp(prefix="bo-", dir=goc_tam)), os.name != "nt"
    env = dict(os.environ, TMPDIR=str(tam), TEMP=str(tam), TMP=str(tam))
    rc, ban_in, loi, p = -1, "", None, None
    try:
        p = subprocess.Popen(argv, cwd=cwd, env=env, text=True, encoding="utf-8", errors="backslashreplace",
                             stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             start_new_session=posix)
        ban_in, _ = p.communicate(timeout=gioi_han)
    except Exception as e:  # MỌI lỗi sau khởi chạy đi CHUNG đường dừng: giết cả nhóm, chờ ≤ 10 s, rồi mới dọn
        loi = (f"hết giờ {gioi_han} giây" if isinstance(e, subprocess.TimeoutExpired)
               else f"khởi chạy/chờ thất bại: {type(e).__name__}: {e}")
        if p is not None:
            han = time.monotonic() + GIAY_CHO_CAY_DUNG
            with contextlib.suppress(OSError):  # Windows: taskkill /T là nỗ lực, KHÔNG xác nhận được (Q6)
                os.killpg(p.pid, signal.SIGKILL) if posix else subprocess.call(
                    ["taskkill", "/T", "/F", "/PID", str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with contextlib.suppress(Exception):
                p.kill(); ban_in = p.communicate(timeout=GIAY_CHO_CAY_DUNG)[0] or ban_in
            while posix and _pid_song(None, p.pid) and time.monotonic() < han:
                time.sleep(0.05)
            if p.returncode is None or not posix or _pid_song(None, p.pid):
                loi += "; KHÔNG xác nhận được cả cây tiến trình đã dừng"
    rc = p.returncode if p is not None and isinstance(p.returncode, int) else rc
    with contextlib.suppress(OSError):
        shutil.rmtree(tam)
    if tam.exists():
        loi = (loi + "; " if loi else "") + f"dọn thư mục tạm thất bại: {tam} còn"
    return rc, ban_in or "", loi


def _chay_that(path, goc_tam=None):
    return _chay_co_lap([sys.executable, path], goc_tam=goc_tam)


def chay_moi(moi=MOI, cach_ly=CACH_LY, chay_mot=_chay_that,
             doc_moi_truong=moi_truong_hien_tai, doc_trong_ci=trong_ci,
             doc_nen_windows=nen_la_windows, so_worker=1, dong_ho=_gio_utc, bao_cao=None):
    """Năm tham số sau là ĐƯỜNG NỐI ĐỂ ĐO, không phải cấu hình: phản chứng phải gọi
    được chính hàm này với bộ chạy giả, nếu không tầng tiêu thụ lại không ai canh.

    `doc_nen_windows` là seam thứ năm, thêm cho packet #456: nếu nền chỉ đọc được
    qua `os.name` thật thì phản chứng A3 phải có máy Windows mới chạy được, tức là
    không ai canh — đúng thứ bốn seam kia sinh ra để tránh.

    #637: `so_worker` = trần bộ ĐANG chạy; `dong_ho` = seam M1; `bao_cao` nhận JSON (không in ở
    đây ⇒ log nghiệp vụ giữ nguyên master, A5). Log theo thứ tự `MOI`; lỗi hạ tầng không qua `CACH_LY`."""
    do = 0
    hien_tai = doc_moi_truong()
    o_trong_ci = doc_trong_ci()
    la_windows = doc_nen_windows()
    ds = list(moi.items())

    def _mot(path):
        bd = dong_ho()
        try:
            rc, ban_in, loi = (tuple(chay_mot(path)) + (None,))[:3]
        except Exception as e:
            rc, ban_in, loi = -1, "", f"ngoại lệ worker {type(e).__name__}: {e}"
        return rc, ban_in, loi, bd, dong_ho()

    muc = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=so_worker) as ex:
        tuong_lai = [ex.submit(_mot, path) for path, _ in ds]
        for (path, mau), tl in zip(ds, tuong_lai):
            rc, ban_in, loi, bd, kt = tl.result()
            muc.append({"duong_dan": path, "rc": rc, "giay": round((kt - bd).total_seconds(), 3),
                        "bat_dau_utc": _iso(bd), "ket_thuc_utc": _iso(kt)})
            print(ban_in, end="")
            if loi is not None:
                print(f"CI_DANG_KY {path}: ĐỎ — LỖI HẠ TẦNG: {loi}, rc={rc}")
                do += 1
                continue
            ok = rc == 0 and any(bang_chung_xanh(ban_in, m)
                                 for m in mau_theo_nen(path, mau, la_windows))
            if path in cach_ly:
                no = cach_ly[path]
                chap_nhan = cach_ly_chap_nhan(ok, no["moi_truong"], hien_tai)
                nen = hien_tai or "không xác định"
                if chap_nhan is None and o_trong_ci:
                    print(f"CI_DANG_KY {path}: ĐỎ — KHÔNG ĐO ĐƯỢC trong CI, môi trường={nen}, "
                          f"cách ly neo {no['moi_truong']}")
                elif chap_nhan is None:
                    print(f"CI_DANG_KY {path}: KHÔNG ĐO ĐƯỢC (ngoài CI) — môi trường={nen}")
                elif hien_tai != no["moi_truong"]:
                    print(f"CI_DANG_KY {path}: {'ĐẠT' if ok else 'ĐỎ'} — KHÔNG CÁCH LY trên {nen}, rc={rc}")
                elif not chap_nhan:
                    print(f"CI_DANG_KY {path}: ĐỎ — đã xanh, hãy gỡ khỏi cách ly")
                else:
                    print(f"CI_DANG_KY {path}: CÁCH LY rc={rc} nợ={no['slug']}")
                do += dem_la_do(chap_nhan, o_trong_ci)
            else:
                print(f"CI_DANG_KY {path}: {'ĐẠT' if ok else 'ĐỎ'} rc={rc}")
                do += not ok
    if bao_cao is not None:
        bao_cao.update(N=so_worker, so_lop_logic=os.cpu_count(), bo=muc, so_lop_dung_duoc=len(os.sched_getaffinity(0))
                       if hasattr(os, "sched_getaffinity") else None)
    return do


def loi_json_thoi_gian(js, moi=MOI):
    """A1: đúng một mục cho mỗi khoá `moi` (đếm lúc chạy), rc nguyên, giay ≥ 0, mốc ISO UTC, kt ≥ bd."""
    bo = js.get("bo") if isinstance(js, dict) else None
    if not isinstance(bo, list) or type(js.get("N")) is not int or not {"so_lop_logic", "so_lop_dung_duoc"} <= set(js):
        return ["thiếu bo/N/so_lop_*"]
    loi = [] if sorted(m.get("duong_dan") for m in bo) == sorted(moi) else ["mục không khớp một-một với MOI"]
    for m in bo:
        mo = [m.get(k) for k in ("bat_dau_utc", "ket_thuc_utc")]
        if type(m.get("rc")) is not int or type(m.get("giay")) not in (int, float) or m["giay"] < 0:
            loi.append(f"rc/giay sai: {m.get('duong_dan')}")
        if not all(isinstance(x, str) and _RE_ISO_UTC.match(x) for x in mo) or mo[1] < mo[0]:
            loi.append(f"mốc không phải ISO UTC hoặc đảo: {m.get('duong_dan')}")
    return loi


def chon_so_worker(trung_vi_theo_N):
    """M7/A8, hàm thuần: nhận trung vị (hoặc danh sách lượt ⇒ lấy trung vị) cho N ∈ {1,2,4}.
    Ứng viên = N ∈ {2,4} nhanh hơn hẳn N=1; t_min = trung vị nhỏ nhất của ứng viên; chọn N nhỏ
    nhất có trung vị ≤ 1,10 × t_min. Không ứng viên ⇒ None (DỪNG S2)."""
    tv = {n: statistics.median(t) if isinstance(t, (list, tuple)) else t
          for n, t in trung_vi_theo_N.items()}
    ung = {n: t for n, t in tv.items() if n in (2, 4) and t < tv[1]}
    t_min = min(ung.values(), default=None)
    return min((n for n, t in ung.items() if t * 100 <= 110 * t_min), default=None)


G5_SELFTEST, G5_PROBE, JOB_G5 = "python ops/cong_cu_test.py", "python ops/cong_cu.py kiem-tra --json", ("gate", "gate-registry", "gate-packet-loop")


def loi_g5_workflow(data):
    """M6: selftest G5 ở đúng MỘT job (`gate`); probe vô điều kiện ở cả ba job, trước lệnh nặng đầu.
    Theo DÒNG LỆNH (bỏ comment) và DANH SÁCH CHO PHÉP: dòng chạm `ops/cong_cu` phải BẰNG ĐÚNG một trong hai lệnh."""
    jobs, loi, co_self = (data or {}).get("jobs") or {}, [], []
    for j, v in jobs.items():
        dong = [(b, x.strip()) for b in ((v or {}).get("steps") or []) for x in str(b.get("run", "")).splitlines()
                if x.strip() and not x.lstrip().startswith("#")]
        co_self += [j] * sum(x == G5_SELFTEST for _, x in dong)
        loi += [f"{j}: dòng G5 ngoài danh sách cho phép: {x!r}" for _, x in dong if "ops/cong_cu" in x and x not in (G5_SELFTEST, G5_PROBE)]
        probe = [i for i, (_, x) in enumerate(dong) if x == G5_PROBE]
        nang = [i for i, (b, _) in enumerate(dong) if i not in probe
                and not str(b.get("name", "")).startswith(("cài ", "Force LF"))]
        if j not in JOB_G5: pass
        elif len(probe) != 1:
            loi.append(f"{j}: probe G5 phải có đúng một dòng lệnh, thấy {len(probe)}")
        elif "if" in dong[probe[0]][0] or "if" in v:
            loi.append(f"{j}: probe G5 có điều kiện")
        elif nang and nang[0] < probe[0]:
            loi.append(f"{j}: probe G5 đứng sau lệnh nặng '{dong[nang[0]][1]}'")
    if sorted(co_self) != ["gate"] or set(JOB_G5) - set(jobs):
        loi.append(f"selftest G5 phải có đúng một lời gọi, ở job gate; thấy {sorted(co_self)}")
    return loi


def phan_chung():
    """Mỗi chốt dùng một bản sao fixture riêng dưới /tmp."""
    # F02 luot 3 — MOT danh sach, MOT diem noi; ten va ket qua o CUNG mot tuple. Hai ban va truoc
    # giu HAI danh sach song song canh bang DO DAI, khong bat lech THU TU (bo ten cuoi ra 64/64
    # True, dao thu tu ra 65/65 True). Khong con `zip` — lop loi chet theo CAU TRUC.
    KQ = []
    def _them(ten, ok):
        if any(t == ten for t, _ in KQ):
            raise AssertionError(f"trung ten ca phan chung: {ten}")
        KQ.append((ten, bool(ok)))
    with tempfile.TemporaryDirectory(prefix="ci-dang-ky-") as d:
        base = pathlib.Path(d)
        for i, kind in enumerate(("thieu", "mat_tep", "mat_loi_goi", "vi_tri_la")):
            r = base / str(i)
            (r / ".claude/dev").mkdir(parents=True)
            (r / ".github/workflows").mkdir(parents=True)
            (r / ".claude/dev/a_test.py").touch()
            reg, wf = {".claude/dev/a_test.py"}, "python .claude/dev/ci_dang_ky_test.py --chay"
            old = set(DA_NOI)
            try:
                DA_NOI.clear()
                if kind == "thieu": reg.clear()
                elif kind == "mat_tep": reg.add(".claude/dev/mat_test.py")
                elif kind == "mat_loi_goi":
                    DA_NOI.add(".claude/dev/a_test.py"); wf = ""
                else:
                    (r / "la").mkdir(); (r / "la/x_test.py").touch()
                _them(("i-thieu-so", "ii-mat-tep", "iii-mat-loi-goi", "iv-vi-tri-la")[i], bool(kiem(r, reg, wf)[0]))
            finally:
                DA_NOI.clear(); DA_NOI.update(old)
        # (a) Bản sao sổ cách ly mất slug phải đỏ.
        mutant_cu = {".claude/dev/a_test.py": {"slug": "", "ly_do": "đỏ trên CI"}}
        _them("a-cach-ly-thieu-slug", bool(kiem(r, reg, wf, mutant_cu)[0]))
        mutant = {".claude/dev/a_test.py": {"slug": "nợ", "ly_do": "đỏ trên CI",
                                                "log": "log-r3"}}
        _them("r4-thieu-moi-truong", bool(kiem(r, reg, wf, mutant)[0]))
        # r5: neo môi trường ngoài đúng nguồn giá trị phải đỏ ở tầng cấu trúc.
        mutant = {".claude/dev/a_test.py": {"slug": "nợ", "ly_do": "đỏ trên CI",
                    "moi_truong": "github-actions/lin-typo", "log": "log-r3"}}
        _them("r5-moi-truong-sai-tap", any("môi trường không hợp lệ" in x for x in kiem(r, reg, wf, mutant)[0]))
        # r5: xoá run thật, giữ nguyên lệnh trong YAML comment vẫn phải đỏ.
        yml = r / ".github/workflows/comment.yml"
        yml.write_text("jobs:\n  x:\n    steps:\n      # - run: python .claude/dev/a_test.py\n", encoding="utf-8")
        old = set(DA_NOI); DA_NOI.clear(); DA_NOI.add(".claude/dev/a_test.py")
        try: _them("r5-comment-gia-loi-goi", any("CI không gọi mục" in x for x in kiem(r, reg)[0]))
        finally: DA_NOI.clear(); DA_NOI.update(old)
        old = set(DA_NOI); DA_NOI.clear(); DA_NOI.add(".claude/dev/a_test.py")
        for level in ("step", "job", "expr", "normal"):
            yml.write_text("jobs:\n  x:\n" + ("    if: false\n" if level == "job" else "") + "    steps:\n      - " + (("if: ${{ false }}\n        " if level == "expr" else "if: false\n        ") if level in ("step", "expr") else "") + "run: python .claude/dev/a_test.py\n", encoding="utf-8")
            found = any("CI không gọi mục" in x for x in kiem(r, reg)[0])
            _them({"step": "r5-step-if-false", "job": "r5-job-if-false",
                   "expr": "r5-step-if-literal-expr", "normal": "r5-normal-step"}[level],
                  found if level != "normal" else not found)
        DA_NOI.clear(); DA_NOI.update(old)
        # (b) Bản sao chương trình cách ly chuyển xanh phải bị yêu cầu gỡ.
        green = base / "green_test.py"
        green.write_text("print('1/1')\n", encoding="utf-8")
        p = subprocess.run([sys.executable, green], text=True, stdout=subprocess.PIPE)
        xanh = p.returncode == 0 and bang_chung_xanh(p.stdout, r"^(\d+)/(\d+)$")
        _them("b-cach-ly-chuyen-xanh", not cach_ly_chap_nhan(xanh, "github-actions/linux", "github-actions/linux"))
        # r4: bỏ phép so làm bản xanh bắn ở môi trường khác; đúng ra phải là None.
        _them("r4-bo-so-moi-truong", (not xanh) is not cach_ly_chap_nhan(xanh, "github-actions/linux", None))
        # r4: đột biến đổi trạng thái thứ ba thành ĐẠT phải bị bắt.
        _them("r4-khong-do-duoc-thanh-dat", cach_ly_chap_nhan(xanh, "github-actions/linux", None) is None and True is not None)
    # Hai chiều bằng chứng: rc đỏ dù có dòng xanh; rc xanh nhưng thiếu dòng xanh.
    _them("rc-do-ban-in-xanh", not (1 == 0 and bang_chung_xanh("TỔNG: ĐẠT", r"TỔNG: ĐẠT")))
    _them("rc-xanh-thieu-ban-in", not (0 == 0 and bang_chung_xanh("", r"TỔNG: ĐẠT")))
    # r6 (#401): VỊ TỪ trung thực rồi mà NƠI TIÊU THỤ vẫn làm tròn lên được — đó là
    # khuyết tật đã sống sót qua r4 và r5. Nên canh cả hai tầng.
    _them("r6-vi-tu-none-trong-ci-la-do", dem_la_do(None, True) is True)
    _them("r6-vi-tu-none-ngoai-ci-khong-do", dem_la_do(None, False) is False)
    _them("r6-vi-tu-da-xanh-van-do", dem_la_do(False, False) is True)
    _them("r6-vi-tu-cach-ly-hop-le-khong-do", dem_la_do(True, True) is False)
    # r6: `trong_ci` phải ĐỘC LẬP với `moi_truong_hien_tai` — thiếu RUNNER_OS vẫn là CI,
    # còn không có GITHUB_ACTIONS thì dù có RUNNER_OS vẫn KHÔNG phải CI.
    _them("r6-trong-ci-khong-doi-runner-os", trong_ci({"GITHUB_ACTIONS": "true"}) is True)
    _them("r6-thieu-github-actions-khong-phai-ci", trong_ci({"RUNNER_OS": "Linux"}) is False)
    _them("r6-github-actions-false-khong-phai-ci", trong_ci({"GITHUB_ACTIONS": "false", "RUNNER_OS": "Linux"}) is False)
    _them("wp430-nhan-linux", moi_truong_hien_tai({"GITHUB_ACTIONS": "true", "RUNNER_OS": "Linux"}) == MOI_TRUONG_CI)
    _them("wp430-nhan-windows", moi_truong_hien_tai({"GITHUB_ACTIONS": "true", "RUNNER_OS": "Windows"}) == MOI_TRUONG_WINDOWS)
    _them("wp430-runner-la-fail-close", moi_truong_hien_tai({"GITHUB_ACTIONS": "true", "RUNNER_OS": "macOS"}) is None)
    _them("wp430-windows-xanh-that", cach_ly_chap_nhan(True, MOI_TRUONG_CI, MOI_TRUONG_WINDOWS) is True)
    _them("wp430-windows-do-that", cach_ly_chap_nhan(False, MOI_TRUONG_CI, MOI_TRUONG_WINDOWS) is False)
    # r6: TẦNG TIÊU THỤ — gọi chính `chay_moi` với bộ chạy giả. Gỡ phép cộng ở đó ra thì
    # ba ca này ĐỎ; đó là điều mà đột biến canh-vị-từ `r4-khong-do-duoc-thanh-dat` KHÔNG
    # bắt được, và là lý do nợ N6 lọt cổng trên windows-latest.
    gia_moi = {"gia_test.py": r"^(\d+)/(\d+)$"}
    gia_no = {"gia_test.py": {"slug": "gia", "ly_do": "gia",
                              "moi_truong": "github-actions/linux", "log": "gia"}}

    def _dem(o_trong_ci, nen, rc_ban_in, neo=MOI_TRUONG_CI):
        no = {"gia_test.py": {**gia_no["gia_test.py"], "moi_truong": neo}}
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            count = chay_moi(moi=gia_moi, cach_ly=no, chay_mot=lambda _p: rc_ban_in,
                             doc_moi_truong=lambda: nen, doc_trong_ci=lambda: o_trong_ci)
        return count, out.getvalue()

    # PHỦ TRỌN MIỀN ĐẾM, không vá lẻ từng ô. Hình dạng "tầng tiêu thụ hở một ô" đã
    # xuất hiện BA lần trong chính packet này: (1) khuyết tật gốc — trạng thái thứ ba
    # không được đếm; (2) finding P1 cross-review lượt 1 trên `dc72c16b` — nhánh
    # `chap_nhan is False` không ca nào đi qua `chay_moi`, đột biến `do += chap_nhan
    # is None and o_trong_ci` sống sót 27/27; (3) finding P1 lượt 2 trên `9ab5eb36` —
    # ô `(True, ngoài CI)` còn hở, đột biến sống sót 29/29. Cả ba đã tái lập được.
    # `PROTOCOL §12`: cùng hình dạng lần thứ BA thì phải xem lại CÁCH LÀM, không vá
    # lần thứ tư. Nên canh bằng BẢNG TRỌN MIỀN: 3 giá trị `chap_nhan` × 2 giá trị
    # `o_trong_ci` = 6 ô, mỗi ô một ca đi qua chính `chay_moi`. Thêm giá trị mới vào
    # miền mà quên ca thì bảng này hở lộ ra ngay, khác hẳn danh sách ca rời rạc.
    #
    # Cách dựng từng ô: `chap_nhan is None` cần nền KHÁC neo; `True` cần nền KHỚP neo
    # và bộ test ĐỎ (cách ly còn hiệu lực); `False` cần nền KHỚP neo và bộ test XANH
    # (đã hết nợ, phải đòi gỡ khỏi cách ly).
    MIEN_DEM = [(None, True, 1, "none-trong-ci"), (None, False, 0, "none-ngoai-ci"),
                (True, True, 0, "cach-ly-hop-le-trong-ci"), (True, False, 0, "cach-ly-hop-le-ngoai-ci"),
                (False, True, 1, "da-xanh-trong-ci"), (False, False, 1, "da-xanh-ngoai-ci")]
    for _cn, _ci, _mong, _o in MIEN_DEM:
        _nen = None if _cn is None else "github-actions/linux"
        _kq = (0, "1/1\n") if _cn is False else (1, "0/1\n")
        _them("r6-TIEU-THU-o-" + _o, _dem(_ci, _nen, _kq)[0] == _mong)
    known = _dem(True, MOI_TRUONG_WINDOWS, (1, "0/1\n"))
    unknown = _dem(True, "github-actions/macos", (1, "0/1\n"))
    windows = _dem(True, MOI_TRUONG_WINDOWS, (1, "0/1\n"), MOI_TRUONG_WINDOWS)
    _them("wp430-known-other-consumer", known[0] == 1 and "KHÔNG CÁCH LY" in known[1])
    _them("wp430-unknown-consumer", unknown[0] == 1 and "KHÔNG ĐO ĐƯỢC" in unknown[1])
    _them("wp430-windows-anchor-positive", windows[0] == 0 and "CÁCH LY" in windows[1])
    _them("wp430-unknown-predicate", cach_ly_chap_nhan(True, MOI_TRUONG_CI, "github-actions/macos") is None)
    # ── packet #456: SO DANG KY PHAN BIET DUOC NEN ────────────────────────────────────
    # Di qua chinh `chay_moi`, khong goi thang `mau_theo_nen`: khuyet tat "lam tron" nam o
    # NOI TIEU THU gia tri, va do la bai hoc r6/#401 da tra gia ba lan trong tep nay.
    # HAI CHIEU, khong phai mot: dong Windows tren Linux phai DO, VA dong Linux tren
    # Windows phai DAT (Windows do du bang tay thi khong duoc phat).
    _P456 = ".claude/hooks/pretooluse_guard_test.py"
    _WIN456 = ("TONG: CA 39/39 dat · DOT BIEN 34 muc KHONG DO TREN WINDOWS"
               " — do tren ubuntu-latest\nTONG: DAT\n")
    _LNX456 = "TONG: CA 39/39 dat · DOT BIEN 34/34 bi giet\nTONG: DAT\n"
    # `0/0 bi giet` = tap RONG thoa `not song` (#319). Tren WINDOWS phai DO — do la dot
    # bien bat buoc thu hai cua A2. Tren LINUX no VAN DUOC NHAN, y het base: lo #319 phia
    # Linux co san tu truoc, va bit no o day la doi hanh vi Linux — trai M4. Ca duoi khoa
    # ca hai chieu ay, ke ca chieu "van con lo", de khong ai vo tinh siet roi pha M4.
    _RONG456 = "TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet\nTONG: DAT\n"
    # Mau Linux NGUYEN BAN cua base — neo cung, khong doc tu `MOI` (doc tu `MOI` thi
    # sua `MOI` se keo ca ca test di theo, va ca test thanh guong soi chinh no).
    _MAU_BASE456 = (r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet"
                    r".*TONG: DAT")

    def _dem_nen(ban_in, la_windows):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            return chay_moi(moi={_P456: MOI[_P456]}, cach_ly={},
                            chay_mot=lambda _p: (0, ban_in),
                            doc_moi_truong=lambda: MOI_TRUONG_CI,
                            doc_trong_ci=lambda: True,
                            doc_nen_windows=lambda: la_windows)

    _them("p456-dong-windows-tren-linux-la-DO", _dem_nen(_WIN456, False) == 1)
    _them("p456-dong-windows-tren-windows-DAT", _dem_nen(_WIN456, True) == 0)
    _them("p456-dong-linux-tren-windows-DAT", _dem_nen(_LNX456, True) == 0)
    _them("p456-dong-linux-tren-linux-khong-doi", _dem_nen(_LNX456, False) == 0)
    _them("p456-dot-bien-0-tren-0-DO-tren-windows", _dem_nen(_RONG456, True) == 1)
    # M4: duong Linux phai giong BASE tung dau vao, ke ca dau vao xau.
    _them("p456-linux-nhan-0-tren-0-Y-HET-base", _dem_nen(_RONG456, False) == 0)
    _them("p456-mau-linux-KHONG-DOI-so-voi-base", MOI[_P456] == _MAU_BASE456)
    _them("p456-linux-A-B-tung-dau-vao-khop-base",
          all(bang_chung_xanh(x, MOI[_P456]) is bang_chung_xanh(x, _MAU_BASE456)
              for x in (_LNX456, _RONG456, _WIN456)))
    try:
        launcher_source = LAUNCHER_WORKFLOW.read_text(encoding="utf-8")
        ci_source = CI_WORKFLOW.read_text(encoding="utf-8")
    except OSError:
        launcher_source = ci_source = ""        # doc khong duoc = DO, khong phai bo qua
    _them("windows_311_launcher_workflow",
          bool(launcher_source) and giet_windows_311_launcher_workflow(launcher_source))
    _them("launcher-semantic-spacing", bool(launcher_source) and not loi_launcher_windows(
          launcher_source.replace("fromJSON(", "fromJSON( ", 1))[0])
    # Doi DUNG LOAI thong diep, khong phai `bool(loi)`: bo ghim lam CA ghim LAN probe do, nen ca
    # cu van xanh khi da XOA HAN chot ghim — do duoc 102/102 (luot 8, P2 #2).
    _them("ruff-pin-required", bool(ci_source) and any("ghim Ruff" in m for m in
          loi_ruff_ci(ci_source.replace("ruff==0.15.15", "ruff", 1))[0]))
    _them("ruff-version-probe-required", bool(ci_source) and any("probe Ruff" in m for m in
          loi_ruff_ci(ci_source.replace("ruff --version", "ruff --help", 1))[0]))
    _ruff = {"name": "cài Ruff 0.15.15 và in probe dương",
             "run": "python -m pip install --quiet ruff==0.15.15\nruff --version\n"}
    _reg = {"name": "test registry", "run": "python .claude/dev/ci_dang_ky_test.py --chay"}
    _khac = {"name": "khác", "run": "python x.py"}
    def _p(lenh): return {"name": "cài Ruff (biến thể)", "run": lenh + "\nruff --version\n"}
    _probe_truoc = {"name": "cài Ruff (probe trước)",  # probe dat TRUOC lenh cai
                    "run": "ruff --version\npython -m pip install --quiet ruff==0.15.15\n"}
    def _wf(jobs, env=None, defaults=None):
        d = {"on": "push", "jobs": jobs}
        if env: d["env"] = env
        if defaults is not None: d["defaults"] = defaults
        return yaml.safe_dump(d, sort_keys=False)
    _FX = [
        ("chua-tach-tuong-thich-lui", {"gate": {"steps": [_ruff, _khac, _reg]}}, None, 0),
        ("da-tach-dung", {"gate": {"steps": [_ruff, _khac]}, "gate-registry": {"steps": [_ruff, _reg]}}, None, 0),
        ("da-tach-thieu-ruff", {"gate": {"steps": [_ruff, _khac]}, "gate-registry": {"steps": [_khac, _reg]}}, None, 1),
        ("da-tach-ruff-sau-registry", {"gate": {"steps": [_ruff, _khac]}, "gate-registry": {"steps": [_reg, _ruff]}}, None, 1),
        ("khong-job-nao-chay-registry", {"gate": {"steps": [_ruff, _khac]}}, None, 1),
        ("hai-job-chay-registry", {"gate": {"steps": [_ruff, _reg]}, "gate-registry": {"steps": [_ruff, _reg]}}, None, 1),
        ("probe-truoc-cai", {"gate": {"steps": [_ruff, _khac]},   # THU TU trong cung than `run`
                             "gate-registry": {"steps": [_probe_truoc, _reg]}}, None, 1),
    ]
    _g = {"steps": [_ruff, _khac]}
    _pm = dict(_ruff, run="python -m pip install --quiet ruff==0.15.15\npython -m ruff --version\n")
    _pc = dict(_ruff, run="python -m pip install --quiet ruff==0.15.15\nruff   --version\n")
    _toml = dict(_ruff, run='python -m pip install --quiet ruff==0.15.15\nprintf "%s\\n" "[lint]\n'
                            'select = [\\"E\\"]  # chu thich" > ruff.toml\nruff --version\n')
    _nhay = dict(_ruff, run='python -m pip install --quiet ruff==0.15.15\necho "a ; b && c | d"\n'
                            'ruff --version\n')
    _tab = dict(_reg, run="python .claude/dev/ci_dang_ky_test.py\t--chay")
    _pmm = dict(_ruff, run="python -m pip install --quiet ruff==0.15.15\npython -mruff --version\n")
    _FX += [
        ("probe-dang-module", {"gate": _g, "gate-registry": {"steps": [_pm, _reg]}}, None, 0),
        ("probe-thua-khoang-trang", {"gate": _g, "gate-registry": {"steps": [_pc, _reg]}}, None, 0),
        ("toml-nhieu-dong-va-thang", {"gate": _g, "gate-registry": {"steps": [_toml, _reg]}}, None, 0),
        ("toan-tu-trong-dau-nhay", {"gate": _g, "gate-registry": {"steps": [_nhay, _reg]}}, None, 0),
        ("registry-ngan-bang-tab", {"gate": _g, "gate-registry": {"steps": [_ruff, _tab]}}, None, 0),
        ("probe-mruff-lien", {"gate": _g, "gate-registry": {"steps": [_pmm, _reg]}}, None, 0),
    ]
    for _t, _b in [("buoc-if-false", {"if": "false"}), ("if-so-khong", {"if": "0"}),
                   ("if-bieu-thuc-false", {"if": "${{false}}"}),
                   ("if-chi-linux", {"if": "runner.os == 'Linux'"})]:
        _FX.append((_t, {"gate": {"steps": [_ruff]},
                         "gate-registry": {"steps": [dict(_ruff, **_b), _reg]}}, None, 1))
    _PIN = "python -m pip install ruff==0.15.15"
    _KPT = "KHONG_PHAN_TICH_DUOC"
    for _t, _run, _nhan in [
            ("ghim-chuan", _PIN, "GHIM"),
            ("tien-to-pip", "pip install ruff==0.15.15", "GHIM"),
            ("tien-to-pip3", "pip3 install ruff==0.15.15", "GHIM"),
            ("tien-to-uv-pip", "uv pip install ruff==0.15.15", "GHIM"),
            ("tien-to-python3", "python3 -m pip install ruff==0.15.15", "GHIM"),
            ("tuy-chon-quiet", "python -m pip install --quiet ruff==0.15.15", "GHIM"),
            ("tuy-chon-q", "python -m pip install -q ruff==0.15.15", "GHIM"),
            ("tuy-chon-no-cache-dir", "python -m pip install --no-cache-dir ruff==0.15.15", "GHIM"),
            ("tuy-chon-disable-pip-version-check",
             "python -m pip install --disable-pip-version-check ruff==0.15.15", "GHIM"),
            ("tuy-chon-no-input", "python -m pip install --no-input ruff==0.15.15", "GHIM"),
            ("ten-hoa-thuong", "python -m pip install Ruff==0.15.15", "GHIM"),
            ("extras", 'python -m pip install "ruff[all]==0.15.15"', "GHIM"),
            ("noi-dong", "python -m pip install \\\n  ruff==0.15.15", "GHIM"),
            ("chay-ruff-khong-phai-cai", "ruff check .", "KHONG"),
            ("chay-module", "python -m ruff --version", "KHONG"),
            ("chay-module-py3", "python3 -m ruff check .", "KHONG"),
            ("chay-uv-run", "uv run ruff --version", "KHONG"),
            ("chay-uvx", "uvx ruff check .", "KHONG"),
            ("chay-co-trinh-u", "python3 -u -m ruff --version", "KHONG"),
            ("chay-co-trinh-B", "python -B -m ruff check .", "KHONG"),
            ("chay-co-trinh-X", "python3 -X utf8 -m ruff --version", "KHONG"),
            ("chay-mruff-lien", "python3 -mruff --version", "KHONG"),
            ("ghep-toan-tu-va", _PIN + " && ruff --version", "GHIM"),
            ("ghep-toan-tu-cham-phay", _PIN + " ; ruff --version", "GHIM"),
            ("comment-khong-tinh", "# " + _PIN, "KHONG"),
            ("khong-ghim", "python -m pip install ruff", "KHONG_GHIM"),
            ("toan-tu-lon-hon", 'python -m pip install "ruff>=0.16"', "KHONG_GHIM"),
            ("toan-tu-la", 'python -m pip install "ruff<>0.16"', "KHONG_GHIM"),
            ("extras-khong-ghim", 'python -m pip install "ruff[all]"', "KHONG_GHIM"),
            ("co-gan-bang", "python -m pip install --target=tmp ruff==0.15.15", _KPT),
            ("co-ngan-lien", "python -m pip install -ttmp ruff==0.15.15", _KPT),
            ("co-chua-biet", "python -m pip install --no-such-flag ruff==0.15.15", _KPT),
            ("cai-them-goi-khac", _PIN + " requests", _KPT),
            ("hai-ban-ruff", _PIN + ' "ruff>=0.16"', _KPT),
            ("go-cai", _PIN + "\npip uninstall -y ruff", _KPT),
            ("trinh-ngoai-khuon", _PIN + "\npdm remove ruff", _KPT),
            ("upgrade-sau-ghim", _PIN + "\npython -m pip install --upgrade ruff", _KPT),
            ("tuy-chon-truoc-install", "python -m pip --quiet install ruff==0.15.15", _KPT)]:
        _them("nhan-" + _t, _phan_loai_cai_ruff(_run + "\nruff --version\n")[0] == _nhan)
    _them("tap-tien-to-khop-ky-vong", list(_TIEN_TO_CAI) == [
        ["pip"], ["pip3"], ["uv", "pip"], ["python", "-m", "pip"], ["python3", "-m", "pip"]])
    _them("tap-tuy-chon-khop-ky-vong", _TUY_CHON_AN_TOAN == {
        "--quiet", "-q", "--no-cache-dir", "--disable-pip-version-check", "--no-input"})
    # Miền M7 đã chốt ở Issue #463 comment 5651040630: lệnh trực tiếp; ngoài miền phải đỏ.
    for _t, _run, _want in [
        ("module-sai-hoa", _PIN + "\npython -m Ruff --version", 1),
        ("module-extras", _PIN + "\npython -m 'ruff[all]' --version", 1),
        ("probe-help-version", _PIN + "\nruff --help --version", 1),
        ("probe-subcommand-version", _PIN + "\nruff check --version", 1),
        ("extras-sai-ky-tu", "pip install 'ruff[!]==0.15.15'\nruff --version", 1),
        ("extras-dau-phay-treo", "pip install 'ruff[all,]==0.15.15'\nruff --version", 1),
        ("quote-chua-dong", _PIN + "\nruff --version\n'", 1),
        ("noi-giua-token", "pi\\\np install ruff==0.15.15\nruff --version", 0),
        ("ansi-c-ngoai-mien", "pip install $'ruff==0.15.15'\nruff --version", 1),
        ("probe-truoc-va-sau", "ruff --version\n" + _PIN + "\nruff --version", 0),
        ("or-ngoai-mien", _PIN + " || ruff --version", 1),
        ("pipe-ngoai-mien", _PIN + " | ruff --version", 1),
        ("background-ngoai-mien", _PIN + " & ruff --version", 1),
        ("requirement-dong", 'pip install "$PACKAGE"\nruff --version', 1),
        ("extras-glob-khong-quote", "pip install ruff[all]==0.15.15\nruff --version", 1),
    ]:
        _FX.append((_t, {"gate": {"steps": [{"run": _run}, _reg]}}, None, _want))
    for _t, _run in [("and-thieu-trai", "&& " + _PIN), ("and-thieu-phai", _PIN + " &&"),
                     ("than-ham", "f() {\n" + _PIN + "\n}"), ("nhom-lenh", "{\n" + _PIN + "\n}"),
                     ("ten-goi-dong", 'pip install "r${X}ff==0.15.15"'), ("dau-cham-phay-rong", "; " + _PIN)]:
        _FX.append((_t, {"gate": {"steps": [_ruff, {"run": _run}, _reg]}}, None, 1))
    _FX += [
        ("registry-module", {"gate": {"steps": [_ruff, {"run": "python -m ci_dang_ky_test --chay"}]}}, None, 0),
        ("registry-if", {"gate": {"steps": [_ruff, dict(_reg, **{"if": "false"})]}}, None, 1),
        ("toml-if-vo-can", {"gate": {"steps": [_ruff, {"if": "false", "run": "printf x > ruff.toml"}, _reg]}}, None, 0),
        ("heredoc-la-du-lieu", {"gate": {"steps": [_ruff, {"run": "cat <<'END'\npip install ruff==0.15.14\nEND\n"}, _reg]}}, None, 0),
    ]
    # Lớp nhận dạng: một job đúng KHÔNG được che installer ngoài miền ở job khác.
    for _t, _run in [
        ("pip-global-dong", 'pip --quiet install "$PACKAGE"'),
        ("module-global-dong", 'python -m pip --quiet install "$PACKAGE"'),
        ("python-flag-dong", 'python -u -m pip install "$PACKAGE"'),
        ("pip3-global-dong", 'pip3 -q install "$PACKAGE"'),
        ("uv-global-dong", 'uv --quiet pip install "$PACKAGE"'),
        ("uv-pip-global-dong", 'uv pip --quiet install "$PACKAGE"'),
        ("executable-path", '/usr/bin/pip install "$PACKAGE"'),
        ("executable-exe", 'pip.exe install "$PACKAGE"'),
        ("installer-la", 'poetry add "$PACKAGE"'),
        ("trinh-dong", '"$INSTALLER" install ruff'),
        ("requirement-file", "pip install -r requirements.txt"),
        ("dependency-file", "pip install ./wheel.whl"),
        ("prefix-env", 'env PACKAGE=ruff pip install "$PACKAGE"'),
        ("prefix-assignment", 'PACKAGE=ruff pip install "$PACKAGE"'),
        ("prefix-command", 'command pip install "$PACKAGE"'),
        ("prefix-sudo", 'sudo pip install "$PACKAGE"'),
        ("thay-lenh-assignment", 'X=$(pip install "$PACKAGE")'),
        ("thay-lenh-echo", 'echo "$(python -m pip install ruff)"'),
        ("thay-lenh-long", 'echo "$(echo "$(pip install ruff)")"'),
        ("backtick", 'echo `pip install ruff`'),
        ("heredoc-dong", 'cat <<END\n$(pip install ruff)\nEND\n'),
    ]:
        _FX.append((_t, {"gate": {"steps": [_ruff, _reg]},
                         "khac": {"steps": [{"run": _run}]}}, None, 1))
    # Đối chứng dương cho ranh giới script/dữ liệu; không đọc thân script hay env.
    for _t, _run in [
        ("script-opaque", "bash setup.sh"),
        ("python-c-opaque", "python -c 'print(\"pip install ruff\")'"),
        ("python-file-opaque", "python setup.py"),
        ("assignment-opaque", 'PACKAGE="ruff==0.15.14"'),
        ("du-lieu-thay-lenh", "echo '$(pip install ruff)'"),
        ("thay-lenh-opaque", 'ID="$(id -u)"'),
        ("thay-lenh-git", 'HEAD_SHA=$(git rev-parse HEAD)'),
        ("goi-khac-tinh", "pip install PyYAML==6.0.3 jsonschema==4.26.0"),
    ]:
        _FX.append((_t, {"gate": {"steps": [_ruff, {"run": _run}, _reg]}}, None, 0))
    for _t, _prefix in [("python-u", "python -u -m pip"), ("python-X", "python -X utf8 -m pip"),
                        ("python-B", "python3 -B -m pip"), ("python-minor", "python3.12 -m pip"),
                        ("mpip-lien", "python -mpip")]:
        _FX.append((_t, {"gate": {"steps": [_p(_prefix + " install ruff==0.15.15"), _reg]}}, None, 0))
    _install, _probe = {"run": _PIN}, {"run": "ruff --version"}
    for _t, _steps, _want in [
        ("probe-buoc-sau", [_install, _probe, _reg], 0),
        ("probe-hai-phia", [_probe, _install, _probe, _reg], 0),
        ("probe-chi-buoc-truoc", [_probe, _install, _reg], 1),
        ("probe-buoc-co-dieu-kien", [_install, dict(_probe, **{"if": "false"}), _reg], 1),
        ("registry-cung-buoc-ngoai-mien", [{"run": _PIN + "\nruff --version\n" + _reg["run"]}], 1),
        ("run-sai-kieu", [_ruff, {"run": ["pip", "install", "ruff"]}, _reg], 1),
        ("step-sai-kieu", [_ruff, "pip install ruff", _reg], 1),
    ]:
        _FX.append((_t, {"gate": {"steps": _steps}}, None, _want))
    _FX.append(("registry-job-co-dieu-kien", {"gate": {"if": "false", "steps": [_ruff, _reg]}}, None, 1))
    for _shell in ("python", "cmd", "bash {0}", "${{ matrix.shell }}"):
        _FX.append(("shell-ngoai-mien-" + _shell,
                    {"gate": {"steps": [dict(_ruff, shell=_shell), _reg]}}, None, 1))
    _FX.append(("shell-job-ngoai-mien", {"gate": {"defaults": {"run": {"shell": "python"}},
                                               "steps": [_ruff, _reg]}}, None, 1))
    _FX.append(("shell-step-uu-tien", {"gate": {"defaults": {"run": {"shell": "python"}},
                      "steps": [dict(_ruff, shell="bash"), dict(_reg, shell="bash")]}}, None, 0))
    # R12: vỏ ngôn ngữ không được miễn kiểm chỉ vì thân trông như dữ liệu/script.
    for _si, _shell in enumerate(("python", "cmd", "bash {0}", "${{ matrix.shell }}")):
        for _bi, _body in enumerate(("x=1", "echo hi", "python setup.py", "")):
            _FX.append((f"shell-vo-can-{_si}-{_bi}", {"gate": {"steps": [
                _ruff, {"shell": _shell, "run": _body}, _reg]}}, None, 1))
    # R16: assignment không thuộc miền argv ASCII của PowerShell; hai đối chứng POSIX giữ xanh.
    for _shell in ("bash", "sh", "pwsh", "powershell"):
        _ngoai = _shell not in ("bash", "sh")
        _FX.append(("shell-vo-can-" + ("ngoai-mien-" if _ngoai else "hop-le-") + _shell,
                    {"gate": {"steps": [_ruff, {"shell": _shell, "run": "x=1"}, _reg]}}, None, int(_ngoai)))
    for _shell in ("pwsh", "powershell"):
        for _i, (_body, _want) in enumerate((("if true; then echo hi; fi", 1), ("", 1), (_PIN, 0),
                                            ("pwsh -NoProfile -File scripts/don-nhanh_test.ps1", 0))):
            _FX.append((f"shell-carrier-{_shell}-{_i}", {"gate": {"steps": [
                _ruff, {"shell": _shell, "run": _body}, _reg]}}, None, _want))
        for _level in ("job", "workflow"):
            _defaults = {"run": {"shell": _shell}}
            _job = {"steps": [_ruff, {"run": "if true; then echo hi; fi"}, _reg],
                    **({"defaults": _defaults} if _level == "job" else {})}
            _errors = loi_ruff_ci(_wf({"gate": _job}, defaults=_defaults if _level == "workflow" else None))[0]
            _them(f"ruff-ci-shell-carrier-{_shell}-{_level}", bool(_errors))
        for _i, _body in enumerate(("return +", "exit -", "IF true", "echo 'text'", 'echo "$X"',
                                   "echo hi | wc", "echo hi\necho", "echo hi\n\n")):
            _FX.append((f"shell-carrier-boundary-{_shell}-{_i}", {"gate": {"steps": [
                _ruff, {"shell": _shell, "run": _body}, _reg]}}, None, int(_i != 6)))
    # R17: cô lập từng lớp ký tự; đối chứng dương và biên LF đi qua consumer thật.
    for _shell in ("pwsh", "powershell"):
        _am = ["echo $X", 'echo "ok"', "echo hi; wc", "echo {x}", "2fa.sh x", "echo a&echo b"]
        _am += ["echo a" + c + "b" for c in "!\"#$%&'()*,;<>?@[\\]^`{|}~\x7fé\u00a0"]
        _am += [c + "file.sh arg" for c in "0123456789./-"]
        _am += ["file" + c + ".sh arg" for c in ":=+"]
        _am += ["echo hi" + c + "echo ok" for c in "\v\f\x1c\x1d\x1e\r\x85\u2028\u2029"]
        _am += ["\necho hi", "echo hi\n\necho ok", "echo hi\n\n", "\n"]
        _duong = ["echo hi\n", "echo hi\necho ok\n", "echo\taA09_./:=+-", "_x.sh arg",
                  "X.sh arg", "a0_./-a.sh arg", " \techo hi \t"]
        for _want, _bodies in ((1, _am), (0, _duong)):
            for _i, _body in enumerate(_bodies):
                _FX.append((f"shell-carrier-alphabet-{_shell}-{_want}-{_i}", {"gate": {"steps": [
                    _ruff, {"shell": _shell, "run": _body}, _reg]}}, None, _want))
    # Cùng vị từ -1 phải được tiêu thụ cả khi job phụ không có một lệnh cài nào.
    for _i, _tail in enumerate(("", " --help", " --chay --mutant windows_311_launcher_workflow")):
        _FX.append((f"registry-ngoai-hop-dong-job-phu-{_i}", {
            "gate": {"steps": [_ruff, _reg]}, "phu": {"steps": [
                {"run": "python .claude/dev/ci_dang_ky_test.py" + _tail}]}}, None, 1))
    for _t, _jobs, _defaults, _want in [
        ("workflow-shell-ngoai-mien", {"gate": {"steps": [_ruff, _reg]}}, {"run": {"shell": "python"}}, 1),
        ("workflow-shell-hop-le", {"gate": {"steps": [_ruff, _reg]}}, {"run": {"shell": "bash"}}, 0),
        ("job-de-workflow", {"gate": {"defaults": {"run": {"shell": "bash"}}, "steps": [_ruff, _reg]}},
         {"run": {"shell": "python"}}, 0),
        ("step-de-hai-cap", {"gate": {"defaults": {"run": {"shell": "cmd"}},
         "steps": [dict(_ruff, shell="bash"), dict(_reg, shell="bash")]}}, {"run": {"shell": "python"}}, 0),
        ("workflow-shell-null", {"gate": {"steps": [_ruff, _reg]}}, {"run": {"shell": None}}, 1),
        ("job-shell-null", {"gate": {"defaults": {"run": {"shell": None}}, "steps": [_ruff, _reg]}}, None, 1),
        ("step-shell-null", {"gate": {"steps": [dict(_ruff, shell=None), _reg]}}, None, 1),
        ("workflow-run-sai-kieu", {"gate": {"steps": [_ruff, _reg]}}, {"run": []}, 1),
    ]:
        _errors = loi_ruff_ci(_wf(_jobs, defaults=_defaults))[0]
        _them("ruff-ci-" + _t, bool(_errors) == bool(_want))
    for _t, _step in [("lexer", {"run": "echo hi 2>&1"}), ("shell", {"shell": "python", "run": "x=1"})]:
        _errors = loi_ruff_ci(_wf({"gate": {"steps": [_ruff, _step, _reg]}}))[0]
        _them("ruff-ci-nguyen-nhan-" + _t,
              any("ngoài miền cú pháp" in m and "gate/bước 2" in m for m in _errors))
    # R13 lexical-boundary: consumer tự từ chối; không mượn lỗi runtime của shell.
    for _t, _run in [
        ("cr-installer", "pip\rinstall ruff==0.15.15\nruff --version"),
        ("cr-probe", _PIN + "\nruff\r--version"),
        ("cr-pin", _PIN + "\r\nruff --version"),
        ("cr-prefix", "python\r-m\rpip install ruff==0.15.15\nruff --version"),
    ]:
        _FX.append((_t, {"gate": {"steps": [{"run": _run}, _reg]}}, None, 1))
    for _t, _run, _want in [
        ("ngoac-sau-dollar-escape", r"echo \$(pip install ruff)", 1),
        ("comment-nuot-ngoac", "V=$(echo hi # )\nX=1", 1),
        ("comment-dong-sau", "V=$(echo hi # )\n)", 0),
        ("hash-trong-tu", "V=$(echo hi#)", 0),
        ("hash-sau-blank-escape", r"V=$(echo hi\ #)", 0),
        ("hash-sau-nhay", "V=$(echo ''#)", 0),
        ("hash-sau-escape-noi-dong", "V=$(echo hi\\\n#)", 0),
        ("hash-sau-blank-noi-dong", "V=$(echo hi \\\n# )", 1),
        ("ngoac-tran-opaque", "echo hi (there)", 1),
        ("ngoac-escape-opaque", r"echo hi \(there\)", 0),
        ("hash-sau-blank-escape-khong-che-cai", r"echo hi\ #; pip install ruff", 1),
    ]:
        _FX.append((_t, {"gate": {"steps": [_ruff, {"run": _run}, _reg]}}, None, _want))
    for _i, _c in enumerate(("\r", "\f", "\v", "\0") + tuple(chr(n) for n in range(32) if n not in (0, 9, 10, 11, 12, 13))):
        for _t, _run, _want in [("tran", "echo hi" + _c, 1), ("escape", "echo hi\\" + _c, 1),
                               ("nhay", "echo 'hi" + _c + "'", 0),
                               ("heredoc", "cat <<'END'\n" + _c + "\nEND\n", 0)]:
            _FX.append((f"c0-{_i}-{_t}", {"gate": {"steps": [_ruff, {"run": _run}, _reg]}}, None, _want))
    # R15: cú pháp ngoài miền không được KHONG hóa qua lệnh opaque.
    for _op in (";", "&", "&&", "|", "||", ";;", ";;;", "&&||", "|&", "|||"):
        for _pos, _run, _want in [("dau", _op + " echo hi", 1),
                                 ("giua", "echo hi " + _op + " echo ok", int(_op not in (";", "&", "&&", "|", "||"))),
                                 ("cuoi", "echo hi " + _op, int(_op not in (";", "&")))]:
            _FX.append((f"syntax-op-{_op}-{_pos}", {"gate": {"steps": [_ruff, {"run": _run}, _reg]}}, None, _want))
    for _t, _run, _want in [
        ("and-or", "echo hi && || echo hi", 1), ("pipe-comment", "echo hi | # x", 1),
        ("or-noi-dong", "echo hi ||\n# x\necho ok", 0), ("pipe-noi-dong", "echo hi |\nwc -l", 0),
        ("redirect-eof", "echo hi >", 1), ("redirect-comment", "echo hi > # x", 1),
        ("redirect-list", "echo hi > ; echo ok", 1), ("redirect-append-eof", "echo hi >>", 1),
        ("redirect-input-eof", "cat <", 1), ("redirect-input", "cat < file", 0),
        ("redirect-noi-dong-eof", "echo hi > \\\n", 1),
        ("redirect-noi-dong-comment", "echo hi > \\\n# x", 1),
        ("redirect-noi-dong-dich", "echo hi > \\\nfile", 0),
        ("heredoc-delimiter-ghep", "cat <<'END'foo\nx\nEND\n", 1),
        ("redirect-target", "echo hi > file", 0), ("redirect-append", "echo hi >> file", 0),
        ("redirect-fd", "echo hi 2>/dev/null", 0), ("redirect-quoted", "echo '>'", 0),
        ("redirect-unsupported", "echo hi <> file", 1),
        ("command-substitution-depth-limit", "X=" + "$(echo " * 17 + "hi" + ")" * 17, 1),
        ("escape-eof", "echo hi\\", 1),
        ("second-heredoc", "cat <<'A' <<'B'\nx\nB\n", 1),
        ("heredoc-dynamic-delimiter", "cat <<$X\nx\n$X\n", 1),
        ("heredoc-backtick", "cat <<END\n`pip install ruff`\nEND\n", 1),
        ("heredoc-continuation-substitution", "cat <<END\nx $\\\n(pip install ruff)\nEND\n", 1),
        ("heredoc-even-backslash-no-join", "cat <<END\nx $\\\\\n(echo data)\nEND\n", 0),
        ("heredoc-quoted-no-join", "cat <<'END'\nx $\\\n(pip install ruff)\nEND\n", 0),
        ("heredoc-continuation-hides-terminator", "cat <<END\nx\\\nEND\n", 1),
        ("heredoc-dash-tab-continuation-substitution", "cat <<-END\n\tx $\\\n\t(pip install ruff)\n\tEND\n", 1),
        ("heredoc-dash-space-no-strip", "cat <<-END\nx $\\\n (echo data)\n\tEND\n", 0),
        ("heredoc-pending-at-eof", "cat <<'END'", 1),
        ("heredoc-unclosed", "cat <<'E'\nx\n", 1),
        ("parameter-eof", "V=${x", 1), ("parameter-double", 'echo "${x"', 1),
        ("parameter-single", "echo '${x'", 0), ("parameter-ok", "V=${X}", 0),
        ("parameter-fallback", 'echo "${X:-KHONG CO}"', 0), ("parameter-unsupported", "echo ${X:?bad}", 1),
        ("if-eof", "if echo hi", 1), ("then-orphan", "then echo hi", 1),
        ("fi-orphan", "echo hi; fi", 1), ("if-body-eof", "if echo hi; then echo yes", 1),
        ("if-empty-cond", "if; then echo hi; fi", 1), ("if-empty-body", "if true; then; fi", 1),
        ("if-empty-cond-nl", "if\nthen echo hi; fi", 1), ("if-empty-body-nl", "if true; then\nfi", 1),
        ("if-wrong-phase", "if true; else echo hi; fi", 1),
        ("fi-tail", "if true; then echo hi; fi echo bad", 1),
        ("if-cond-compound", "if if true; then echo hi; fi; then echo bye; fi", 1),
        ("if-inline-header", "if true; then if false; then echo hi; fi; fi", 1),
        ("if-nested-body", "if true; then\nif false; then echo hi; fi\nfi", 0),
        ("if-empty-else", "if true; then echo hi; else; fi", 1),
        ("if-then-operand", "if true && then echo hi; fi", 1),
        ("if-ok", "if true; then echo hi; else echo bye; fi", 0),
        ("elif-ok", "if true; then echo a; elif false; then echo b; fi", 0),
        ("group-eof", "{ echo hi", 1), ("group-orphan", "echo hi; }", 1),
        ("group-empty", "{\n}", 1), ("group-ok", "echo hi || { cat file; exit 1; }", 0),
        ("group-pipe-incomplete", "{ echo hi |\n}", 1),
    ]:
        _FX.append(("syntax-" + _t, {"gate": {"steps": [_ruff, {"run": _run}, _reg]}}, None, _want))
    # R16: ca cô lập từng chốt; không để một lỗi khuôn khác che đột biến của chốt ấy.
    for _t, _run in [
        ("header-group-semicolon", "{ ; echo hi; }"), ("header-group-and", "{ && echo hi; }"),
        ("inline-header-isolated", "if true; then if false; fi"),
        ("condition-compound-isolated", "if true\nif false; then echo a; fi\nthen echo b; fi"),
    ]:
        _FX.append(("guard-" + _t, {"gate": {"steps": [_ruff, {"run": _run}, _reg]}}, None, 1))
    for _i, _key in enumerate(("for", "while", "until", "do", "done", "case", "esac", "function",
                               "select", "coproc", "time", "!", '"fi"', r"\f\i")):
        _FX.append((f"guard-unsupported-keyword-{_i}", {"gate": {"steps": [
            _ruff, {"run": _key + " echo hi"}, _reg]}}, None, 1))
    for _i, _target in enumerate(("\nwc", "; echo ok", "| wc", "& echo ok", "< file", "> file", "# comment")):
        _FX.append((f"guard-redirect-boundary-{_i}", {"gate": {"steps": [
            _ruff, {"run": "echo hi > " + _target}, _reg]}}, None, 1))
    for _i, _run in enumerate(("echo $[1+2", "X=$[", 'echo "$[1+2"', "echo $[1+2]",
                               "echo $'\\'", "echo $'ok'", 'echo $"ok"', "echo $((1+2))")):
        _FX.append((f"guard-expansion-outside-{_i}", {"gate": {"steps": [
            _ruff, {"run": _run}, _reg]}}, None, 1))
    for _i, _suffix in enumerate(("[1+2", "{X", "'\\'", '"ok"')):
        _FX.append((f"guard-expansion-continuation-{_i}", {"gate": {"steps": [
            _ruff, {"run": "echo $\\\n" + _suffix}, _reg]}}, None, 1))
    for _i, _run in enumerate(("echo '$[1+2'", r"echo \$[1+2", 'echo "$"', "echo $",
                               'echo "$\'ok\'"', "echo '$\"ok\"'", r"echo \$\'ok\'")):
        _FX.append((f"guard-expansion-data-{_i}", {"gate": {"steps": [
            _ruff, {"run": _run}, _reg]}}, None, 0))
    for _i, _parameter in enumerate(("$X", "$NAME_2", "$0", "$9", "$@", "$*", "$#", "$?", "$-", "$!", "$$")):
        for _j, _run in enumerate(("echo " + _parameter, 'echo "' + _parameter + '"', "V=" + _parameter)):
            _FX.append((f"parameter-bare-{_i}-{_j}", {"gate": {"steps": [
                _ruff, {"run": _run}, _reg]}}, None, 0))
    for _ten, _jobs, _env, _mong in _FX:
        _loi = len(loi_ruff_ci(_wf(_jobs, _env))[0])
        _them("ruff-ci-" + _ten, (_loi == 0) if _mong == 0 else (_loi >= 1))
    # ── #637: A1–A5, A7, A8 đi qua CHÍNH `chay_moi`/`_chay_co_lap`; đột biến mã đo ngoài cây (PR). ──
    for _t, _e, _n, _nen in (("rong", "", 1, "posix"), ("1", "1", 1, "posix"), ("4", "4", 4, "posix"),
                             ("8", "8", 8, "posix"), ("vang", None, 1, "posix"), ("windows-luon-1", "4", 1, "nt")):
        _them("p637-A4-N-" + _t, doc_so_worker({} if _e is None else {BIEN_WORKERS: _e}, _nen) == _n)
    for _v in ("0", "-1", "9", "abc", " 2", "2.0"):
        _n = 0
        with contextlib.suppress(ValueError):
            _n = doc_so_worker({BIEN_WORKERS: _v}, "posix"); _n = None
        _them(f"p637-A4-N-sai-{_v!r}", _n is not None)
    _M = {f"{c}_test.py": r"^(\d+)/(\d+)$" for c in "abcde"}
    _NO = {"e_test.py": {"slug": "gia", "ly_do": "gia", "moi_truong": MOI_TRUONG_CI, "log": "gia"}}

    def _gia(path):
        time.sleep({"a": .3, "b": .2, "c": .1}.get(path[0], 0))
        if path[0] == "d": raise RuntimeError("worker hỏng")
        return {"b": (1, "1/1\n"), "e": (-9, "treo\n", "hết giờ 1800 giây")}.get(path[0], (0, "1/1\n"))

    def _log(moi, chay_mot=_gia, **kw):
        out, bc = io.StringIO(), {}
        with contextlib.redirect_stdout(out):
            d = chay_moi(moi=moi, cach_ly=_NO, chay_mot=chay_mot, doc_moi_truong=lambda: MOI_TRUONG_CI,
                         doc_trong_ci=lambda: True, doc_nen_windows=lambda: False, bao_cao=bc, **kw)
        return d, out.getvalue(), bc
    _L3 = "1/1\nCI_DANG_KY a_test.py: ĐẠT rc=0\n1/1\nCI_DANG_KY b_test.py: ĐỎ rc=1\n1/1\nCI_DANG_KY c_test.py: ĐẠT rc=0\n"
    _L5 = _L3 + ("CI_DANG_KY d_test.py: ĐỎ — LỖI HẠ TẦNG: ngoại lệ worker RuntimeError: worker hỏng, rc=-1\n"
                 "treo\nCI_DANG_KY e_test.py: ĐỎ — LỖI HẠ TẦNG: hết giờ 1800 giây, rc=-9\n")
    _them("p637-A5-mac-dinh-giong-master", _log({k: _M[k] for k in "a_test.py b_test.py c_test.py".split()})[:2] == (1, _L3))
    _them("p637-A3-N1-thu-tu-MOI-va-ha-tang-khong-qua-cach-ly", _log(_M, so_worker=1)[:2] == (3, _L5))
    _them("p637-A3-N4-cung-log-cung-phan-quyet", _log(_M, so_worker=4)[:2] == (3, _L5))
    _t0, _nhip = datetime.datetime(2026, 9, 25, 8, tzinfo=datetime.timezone.utc), iter(range(99))
    _bc = _log(_M, dong_ho=lambda: _t0 + datetime.timedelta(seconds=1.5 * next(_nhip)))[2]
    _them("p637-A1-clock-gia-khop-chinh-xac", _bc["bo"][1] == {
        "duong_dan": "b_test.py", "rc": 1, "giay": 1.5,
        "bat_dau_utc": "2026-09-25T08:00:03.000Z", "ket_thuc_utc": "2026-09-25T08:00:04.500Z"})
    _them("p637-A1-json-hop-le", not loi_json_thoi_gian(_bc, _M) and _bc["N"] == 1)
    for _t, _f in (("bo-mot-muc", lambda b: b.pop()), ("rc-sai-kieu", lambda b: b[0].update(rc="0")),
                   ("giay-am", lambda b: b[0].update(giay=-1)), ("moc-khong-utc", lambda b: b[0].update(
                       bat_dau_utc="2026-09-25T08:00:00")), ("moc-dao", lambda b: b[0].update(
                       bat_dau_utc=b[0]["ket_thuc_utc"], ket_thuc_utc=b[0]["bat_dau_utc"]))):
        _j = json.loads(json.dumps(_bc)); _f(_j["bo"])
        _them("p637-A1-" + _t, bool(loi_json_thoi_gian(_j, _M)))
    _cv, _st = threading.Condition(), {"act": 0, "max": 0, "goi": []}
    def _tran(path):
        with _cv:
            _st["act"] += 1; _st["max"] = max(_st["max"], _st["act"]); _st["goi"].append(path)
            _cv.notify_all(); _cv.wait_for(lambda: _st["act"] >= 2, 2); _cv.wait_for(lambda: _st["act"] > 2, .3)
            _st["act"] -= 1
        return 0, "1/1\n"
    _M4 = {k: _M[k] for k in "a_test.py b_test.py c_test.py d_test.py".split()}
    _log(_M4, chay_mot=_tran, so_worker=2)
    _them("p637-A3b-tran-N-va-chong-lap", _st["max"] == 2 and sorted(_st["goi"]) == sorted(_M4))
    with tempfile.TemporaryDirectory() as _g, tempfile.TemporaryDirectory() as _hen:
        _env0, _SCR = dict(os.environ), (
            "import os,pathlib,sys,time,tempfile;t=pathlib.Path(tempfile.gettempdir());h=pathlib.Path(sys.argv[2]);(t/'x.txt')"
            ".write_text(sys.argv[1]);(h/sys.argv[1]).touch()\nwhile len(list(h.iterdir()))<2: time.sleep(.05)\n"
            "print(sys.argv[1],(t/'x.txt').read_text(),os.environ['TMPDIR'])")
        _o = _log({"A": "^A A ", "B": "^B B "}, so_worker=2, chay_mot=lambda p: _chay_co_lap(
            [sys.executable, "-c", _SCR, p, _hen], goc_tam=_g, gioi_han=60))[1]
        _td = re.findall(r"^[AB] [AB] (.+)$", _o, re.M)
        _them("p637-A2-khong-dung-nhau", "CI_DANG_KY A: ĐẠT" in _o and "CI_DANG_KY B: ĐẠT" in _o)
        _them("p637-A2-tmpdir-rieng", len(set(_td)) == 2 and all(pathlib.Path(x).parent == pathlib.Path(_g) for x in _td))
        _them("p637-A2-da-don", not any(pathlib.Path(_g).iterdir()))
        _them("p637-A2-environ-cha-khong-doi", dict(os.environ) == _env0)
    if os.name != "nt":  # A3c KHÔNG ĐO TRÊN WINDOWS (Q6): killpg//proc là đường POSIX
        _ngoai = subprocess.Popen([sys.executable, "-c", "import time;time.sleep(60)"])
        with tempfile.TemporaryDirectory() as _g:
            _t = time.monotonic()
            _rc, _bi, _loi = _chay_co_lap([sys.executable, "-c", "import subprocess,sys,time;c=subprocess.Popen("
                                           "[sys.executable,'-c','import time;time.sleep(120)']);print(c.pid,flush=True);"
                                           "time.sleep(120)"], goc_tam=_g, gioi_han=2)
            _chau = int(_bi.split()[0]) if _bi.split() else -1
            _them("p637-A3c-het-gio-la-loi-ha-tang", _loi is not None and "hết giờ 2" in _loi)
            _them("p637-A3c-chau-da-chet", _chau > 0 and not _pid_song(_chau))
            _them("p637-A3c-dung-trong-han", time.monotonic() - _t < 2 + GIAY_CHO_CAY_DUNG + 3)
            _them("p637-A3c-da-don", not any(pathlib.Path(_g).iterdir()))
            _rc, _bi, _loi = _chay_co_lap([sys.executable, "-c", "import time;time.sleep(60)"], goc_tam=_g, gioi_han="x")
            _them("p637-A3c-loi-khac-het-gio-van-giet-va-cho", _rc == -signal.SIGKILL and "TypeError" in (_loi or "")
                  and not any(pathlib.Path(_g).iterdir()))
        _them("p637-A3c-ngoai-cay-khong-bi-dung", _ngoai.poll() is None)
        _ngoai.kill(); _ngoai.wait()
    _wf0 = yaml.safe_load(CI_WORKFLOW.read_text(encoding="utf-8"))
    def _hong_wf(j, f):
        w = json.loads(json.dumps(_wf0)); b = w["jobs"][j]["steps"]
        f(b, next(i for i, x in enumerate(b) if G5_PROBE in str(x.get("run", ""))))
        return bool(loi_g5_workflow(w))
    _them("p637-A7-workflow-that-dat", not loi_g5_workflow(_wf0))
    _them("p637-A7-bo-probe", _hong_wf("gate-registry", lambda b, i: b.pop(i)))
    _them("p637-A7-probe-co-if", _hong_wf("gate-packet-loop", lambda b, i: b[i].update({"if": "always()"})))
    _them("p637-A7-probe-sau-buoc-nang", _hong_wf("gate-registry", lambda b, i: b.append(b.pop(i))))
    _them("p637-A7-nhan-doi-selftest", _hong_wf("gate-packet-loop", lambda b, i: b.insert(i, {"run": G5_SELFTEST})))
    _them("p637-A7-probe-bi-comment", _hong_wf("gate-registry", lambda b, i: b[i].update(run="# " + b[i]["run"])))
    _them("p637-A7-hai-selftest-mot-run", _hong_wf("gate", lambda b, i: b[i].update(run=b[i]["run"] + "\n" + G5_SELFTEST)))
    _them("p637-A7-nang-truoc-probe-cung-run", _hong_wf("gate-registry", lambda b, i: b[i].update(
        run="python .claude/dev/ci_dang_ky_test.py --chay\n" + b[i]["run"])))
    _them("p637-A7-comment-truoc-probe-khong-la-nang", not _hong_wf("gate-registry", lambda b, i: b[i].update(run="# x\n" + b[i]["run"])))
    _them("p637-A7-probe-doi-doi-so", _hong_wf("gate-registry", lambda b, i: b[i].update(run=G5_PROBE.replace("--json", "--help"))))
    _them("p637-A7-selftest-trong-echo", _hong_wf("gate", lambda b, i: b[i].update(run=b[i]["run"].replace(G5_SELFTEST, f"echo '{G5_SELFTEST}'"))))
    _them("p637-A7-nhan-doi-selftest-trong-gate", _hong_wf("gate", lambda b, i: b.insert(i + 1, {"run": G5_SELFTEST})))
    _them("p637-A8-khong-ung-vien", chon_so_worker({1: 100, 2: 101, 4: 102}) is None)
    _them("p637-A8-dung-bien", chon_so_worker({1: 200, 2: 110, 4: 100}) == 2)
    _them("p637-A8-vuot-bien", chon_so_worker({1: 200, 2: 110.5, 4: 100}) == 4)
    _them("p637-A8-trung-vi-khong-phai-trung-binh", chon_so_worker({1: [300, 100, 200], 2: [90, 500, 80], 4: [95, 95, 1]}) == 2)
    # Bang ten KHONG con ton tai: 47 ten cu tung nam o day, cach cho sinh ket qua hang tram dong —
    # chinh nguon lech F02 to cao. Nay ten VA ket qua o CUNG mot `_them`, khong con `zip` de cat im.
    for ten, ok in KQ:
        print(f"ĐỘT BIẾN {ten}: {'ĐỎ đúng' if ok else 'LỌT'}")
    print(f"PHẢN CHỨNG: {sum(ok for _, ok in KQ)}/{len(KQ)} đỏ đúng")
    return all(ok for _, ok in KQ)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chay", action="store_true")
    ap.add_argument("--mutant", choices=("windows_311_launcher_workflow",))
    ns = ap.parse_args()
    if ns.chay:  # A4: N sai ⇒ ĐỎ TRƯỚC khi chạy bộ nào
        try:
            so_worker = doc_so_worker()
        except ValueError as e:
            print("ĐỎ:", e); print("TỔNG: ĐỎ")
            return 2
    if ns.mutant:
        killed = giet_windows_311_launcher_workflow(LAUNCHER_WORKFLOW.read_text(encoding="utf-8"))
        print(f"MUTANT {ns.mutant}: {'GIẾT' if killed else 'SỐNG'}")
        return 0 if killed else 1
    loi, tren_cay, trong_so = kiem()
    launcher_loi, launcher_chot = loi_launcher_windows()
    ruff_loi, ruff_chot = loi_ruff_ci()
    loi += launcher_loi
    loi += ruff_loi
    loi += ["G5 (M6): " + x for x in loi_g5_workflow(yaml.safe_load(CI_WORKFLOW.read_text(encoding="utf-8")))]
    for x in loi: print("ĐỎ:", x)
    print(f"ĐĂNG KÝ: {tren_cay}/{trong_so}")
    print(f"TRẠNG THÁI: chan={trong_so - len(CACH_LY)} cach_ly={len(CACH_LY)}")
    print(f"LAUNCHER WINDOWS: {launcher_chot - len(launcher_loi)}/{launcher_chot} hợp đồng")
    print(f"RUFF CI: {ruff_chot - len(ruff_loi)}/{ruff_chot} hợp đồng")
    ok = not loi and tren_cay == trong_so and phan_chung()
    if ns.chay:
        bc = {}
        ok = chay_moi(so_worker=so_worker, bao_cao=bc) == 0 and ok
        print("CI_DANG_KY_THOI_GIAN " + json.dumps(bc, ensure_ascii=False))
        loi_js = loi_json_thoi_gian(bc)
        for x in loi_js: print("ĐỎ: JSON thời gian:", x)
        ok = ok and not loi_js
    print("TỔNG:", "ĐẠT" if ok else "ĐỎ")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
