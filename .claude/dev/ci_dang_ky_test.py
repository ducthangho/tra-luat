#!/usr/bin/env python3
"""Sổ test sống: kiểm phạm vi, lời gọi CI, rc và bằng chứng dương."""
import argparse
import concurrent.futures
import contextlib
import datetime
import hashlib
import io
import json
import math
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
    ".claude/dev/doc_receipt_thu_hoi_test.py": r'^doc_receipt_thu_hoi tests: ([1-9]\d*)/(\1) ca QUA · ([1-9]\d*)/(\3) dot bien GIET$',
    ".claude/dev/chon_reviewer_test.py": r"(?s)nền: (\d+)/(\d+) đạt.*TỔNG: ĐẠT",
    ".claude/dev/gh_readback_test.py": r"gh_readback tests: (\d+)/(\d+) ca QUA \(hong 0\)",
    ".claude/dev/mcp_gh_test.py": r"(?s)CA\s+: (\d+)/(\d+) đạt · 0 đỏ · ĐẠT.*ĐỘT BIẾN.*ĐẠT.*TỔNG: ĐẠT",
    ".claude/dev/mcp_github_doc_test.py": r"mcp_github_doc tests: (\d+)/(\d+) ca QUA \(hong 0, bo qua 0\)",
    ".claude/dev/probe_mang_test.py": r"(?s)tự đột biến cổng: 9/9 chết.*named mutant probe_missing_tool_executes_git: 1/1 chết.*nền: 11/11 đạt.*TỔNG: ĐẠT",
    # GIU NGUYEN `\d+` — M4 dong bang hanh vi Linux, va mau nay la duong Linux di qua.
    # Lo #319 (`0/0 bi giet` lot vi `bang_chung_xanh` chi soi hai nhom CA) CO THAT va
    # co SAN tu base, nhung bit no o day la doi hanh vi Linux — ngoai pham vi packet
    # #456. Chot tuong duong duoc dat o duong WINDOWS (`MOI_WINDOWS`), la noi dot bien
    # bat buoc cua A2 thuc su bieu hien. Lo phia Linux: #647 dong o tang che do du
    # (`MAU_DAY_DU`), mau nay van giu nguyen.
    ".claude/hooks/pretooluse_guard_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
    ".claude/hooks/subagent_ghi_detect_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
    "ops/nhanh_don_duoc_test.py": r"^(\d+)/(\d+)$",
    "ops/kiem_ho_so_land_test.py": r"^(\d+)/(\d+)$",
    "ops/kiem_nhan_hint_test.py": r"^(\d+)/(\d+)$",
    "ops/land_evidence_nguon_test.py": r"(?ms)\A(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b).*^CA: ([1-9]\d*)/(\1) dat\nDOT BIEN: ([1-9]\d*)/\3 bi giet dung ly do\nTU KIEM PHAN HANG: DAT \(\d+ dot bien\)\nTONG: DAT\n?\Z",
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
    "ops/ci_duong_nhanh_test.py",
    "ops/cong_cu_test.py", "ops/lease_publish_test.py",
    "scripts/tl_core/command_registry_test.py",
}
DANG_KY = set(MOI) | DA_NOI


def _git_bo_qua(root, ds, chay=subprocess.run):
    """Tệp Git BỎ QUA và KHÔNG tracked trong `ds`.
    WP748 r18 (G5 g17: k01 đỏ vì gương `.codex/hooks/*_test.py` bị `.gitignore` mà
    `rglob` vẫn thấy, ra "vị trí chưa biết") — fix. `check-ignore` mặc định KHÔNG báo
    tệp đã tracked, nên test tracked vẫn hiện. Fail-close: không phải gốc kho Git,
    hoặc git không chạy/không đo được (rc ngoài 0/1) ⇒ rỗng, mọi tệp vẫn được đếm."""
    if not ds or not (root / ".git").exists():
        return set()
    try:
        r = chay(["git", "-C", str(root), "check-ignore", "-z", "--stdin"],
                 input="".join(x + "\0" for x in ds), capture_output=True, text=True,
                 encoding="utf-8", errors="surrogateescape", timeout=120)
    except (OSError, subprocess.SubprocessError):
        return set()
    if r.returncode not in (0, 1):
        return set()
    return set(r.stdout.split("\0")) & set(ds)


def tim(root, chay=subprocess.run):
    """Trả (test sống, hiện vật, vị trí lạ); ops chỉ nhận tệp mức đỉnh.
    Tệp Git bỏ qua mà không tracked không thuộc cây ⇒ không đếm (xem `_git_bo_qua`)."""
    song, hien_vat, la = set(), set(), set()
    ds = sorted(p.relative_to(root).as_posix() for p in root.rglob("*_test.py"))
    bo_qua = _git_bo_qua(root, ds, chay)
    for q in ds:
        if q in bo_qua:
            continue
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
    def _job_if_duoc_phep(jn):
        j = jobs[jn]
        return (jn == "gate-registry" and j.get("if") == "${{ !cancelled() }}"
                and j.get("needs") == ["chuan-bi", "gate-nhanh-gop"])
    for jn, ks in kinds.items():
        for i, kind in enumerate(ks):
            if kind != "KHONG" and (_buoc_co_dieu_kien(steps[jn][i])
                                     or (jobs[jn].get("if") is not None and not _job_if_duoc_phep(jn))):
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
                  and (jobs[jn].get("if") is None or _job_if_duoc_phep(jn)))
    outside = [f"{jn}/bước {i + 1}" for jn, ks in kinds.items() for i, k in enumerate(ks) if k == "KHONG_PHAN_TICH_DUOC"]
    reason = f"; ngoài miền cú pháp: {outside}" if outside else ""
    checks = [
        (installs and not bad_pin, f"CI không chứng minh ghim Ruff 0.15.15 (job: {bad_pin or 'không job nào cài Ruff'}{reason})"),
        (installs and not bad_probe, f"CI không in probe Ruff --version (job: {bad_probe or 'không job nào cài Ruff'})"),
        (before, "CI không provision Ruff trước test registry trong cùng job "
                 f"(job chạy test registry: {callers or 'KHÔNG CÓ'})"),
    ]
    return [message for ok, message in checks if not ok], len(checks)

def loi_ci_dispatch_windows(source=None):
    """#878: hợp đồng `workflow_dispatch.inputs.runner_set` của `ci.yml` — cùng từ vựng với launcher, nhưng MẶC ĐỊNH
    giữ hai nền (đổi mặc định là quyết định riêng của chủ kho, Q3 spec wp878). Biểu thức `os` của `chuan-bi` phải đọc
    input ấy và trả đúng ba mảng theo thứ tự: chỉ Windows · hai nền · chỉ Ubuntu."""
    source = CI_WORKFLOW.read_text(encoding="utf-8") if source is None else source
    try:
        data = yaml.safe_load(source) or {}
    except yaml.YAMLError as e:
        return [f"ci.yml YAML lỗi: {e}"], 1
    triggers = data.get("on", data.get(True))
    dispatch = triggers.get("workflow_dispatch") if isinstance(triggers, dict) else None
    runner = ((dispatch or {}).get("inputs") or {}).get("runner_set") if isinstance(dispatch, dict) else None
    expected = {"required": False, "default": "windows-and-ubuntu", "type": "choice",
                "options": ["windows-and-ubuntu", "windows-only"]}
    expr = ((((data.get("jobs") or {}).get("chuan-bi") or {}).get("outputs")) or {}).get("os")
    compact = re.sub(r"\s+", " ", expr) if isinstance(expr, str) else ""
    try:
        arrays = [json.loads(x) for x in re.findall(r"'(\[[^']*\])'", compact)]
    except json.JSONDecodeError:
        arrays = None
    checks = [
        (isinstance(runner, dict) and all(runner.get(k) == v for k, v in expected.items()),
         "ci.yml sai hợp đồng workflow_dispatch.runner_set"),
        ("github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only'" in compact,
         "ci.yml: os của chuan-bi không đọc inputs.runner_set == 'windows-only' trong nhánh dispatch"),
        (arrays == [["windows-latest"], ["ubuntu-latest", "windows-latest"], ["ubuntu-latest"]],
         f"ci.yml: os của chuan-bi sai ba mảng chỉ-Windows · hai nền · chỉ-Ubuntu (thấy {arrays})"),
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
# #643 (chủ kho chọn "b", PR #644): 3600 → 4500. Đo run 36208617323, N=2 chế độ đủ: `nhanh_don_duoc_test` 3306,45 s = 92 %
# trần cũ. KHÔNG bảo đảm cả job dưới `timeout-minutes` (nay 105): bộ ấy còn chờ worker trống (run trên: bắt đầu sau 337 s),
# Windows ép N=1 ⇒ dài hơn; trần job là trần NGOÀI. Ca `p643-tran-bo-nho-hon-timeout-job` chỉ khoá trần bộ < trần job.
# #705 (CI-REGISTRY-NANG-TRAN-BO-DAY-DU, chủ kho Q4): 4500 → 5400, job 90 → 105 phút. `nhanh_don_duoc_test` chế độ đủ:
# 3645 s xanh (run 36642392330) rồi > 4500 s ĐỎ ba lần (36696528580 ×2, 36839918701) — runner chậm 22–42 % (hai bộ vô can
# cùng lượt: `pretooluse_guard_test` 914 → 1213–1300 s, `subagent_ghi_detect_test` 316 → 386–400 s), KHÔNG phải bộ chậm đi
# (delta tại chỗ 7b308bc 4604 s / 423b4ba 4586 s). 3645 × 1,42 ≈ 5180 ⇒ 5400 chỉ dư ~4 % — MỎNG; giải pháp bền là chia mảnh.
GIAY_TOI_DA_MOT_BO, GIAY_CHO_CAY_DUNG, BIEN_WORKERS, BIEN_MOC = 5400, 10, "CI_DANG_KY_WORKERS", "CI_DANG_KY_MOC"


def _gio_utc(): return datetime.datetime.now(datetime.timezone.utc)
def _iso(dt): return dt.astimezone(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


# CI-REGISTRY-DOT-BIEN-THEO-DIFF r1 (#643): M1 kế hoạch theo diff (fail-closed), M2 bằng chứng chế độ, M4 chốt env.
# LỆCH protocol :839-840 CÓ DUYỆT (spec §2): chỉ VÒNG ĐỘT BIẾN của bộ trong `NHE` bị bỏ; T1..T8 và mọi bộ khác chạy mọi
# lượt. Cờ nhẹ là cờ SẴN CÓ của bộ (`ops/nhanh_don_duoc_test.py:5184`), không sửa bộ nào.
# #647 (CI-REGISTRY-PRETOOLUSE-CHE-DO-NHE r1): mở rộng lệch ấy sang `pretooluse_guard_test` — cờ mới của bộ, cùng luật vùng.
# #651 (CI-REGISTRY-THU-HEP-VUNG r1): bộ thứ ba `subagent_ghi_detect_test`, cùng luật vùng + `.claude/settings.json`.
_PTG, _SGD = ".claude/hooks/pretooluse_guard_test.py", ".claude/hooks/subagent_ghi_detect_test.py"
NHE = {"ops/nhanh_don_duoc_test.py": {"NHANH_DON_DUOC_KHONG_DOT_BIEN": "1"},
       _PTG: {"PRETOOLUSE_GUARD_KHONG_DOT_BIEN": "1"}, _SGD: {"SUBAGENT_GHI_DETECT_KHONG_DOT_BIEN": "1"}}
_DONG_DU_HOOK = r"^TONG: CA \d+/\d+ dat · DOT BIEN (\d+)/(\d+) bi giet$"
MAU_DAY_DU = {"ops/nhanh_don_duoc_test.py": r"^MUTANT: giet = (\d+) · khong giet = 0 · khong do duoc = 0 / tong (\d+)$",
              _PTG: _DONG_DU_HOOK, _SGD: _DONG_DU_HOOK}
# Mẫu RIÊNG của chế độ nhẹ, chỉ được cộng thêm khi kế hoạch là nhẹ. Bộ vắng mặt ⇒ mẫu `MOI` tự nó đã chấp nhận dòng nhẹ.
# #651 M1 (P2 #649 r4111733460): bộ CÓ mặt ở đây mà in dòng khớp `MAU_DAY_DU` lúc nhẹ ⇒ ĐỎ — cờ rò hoặc nhánh hồi quy.
_DONG_NHE_HOOK = r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN [1-9]\d* muc CHE DO NHE — do khi diff cham vung.*TONG: DAT"
MAU_NHE = {_PTG: _DONG_NHE_HOOK, _SGD: _DONG_NHE_HOOK}
# #651 M2: `ci_dang_ky_test.py` ra khỏi vùng (bộ chọn tự canh bằng `phan_chung` mọi lượt); `.github/**` → riêng `ci.yml`.
# Phần chốt nới ra được bù bằng lượt ĐỦ hằng tuần `ci-dot-bien-du.yml` (chốt `loi_workflow_dot_bien_du`).
VUNG_CHUNG = (".github/workflows/ci.yml", "requirements.txt")
# Tệp/tiền tố NGOÀI cặp bộ/đích. `_PTG`: mutant chạy lại `t15`/`t33` ⇒ `--kiem-bang` ⇒ `tl.py tool-inventory` + `--help`;
# audit hook `open` (d4a84ef): 32 tệp, TẤT CẢ dưới `scripts/` ⇒ tiền tố cả lớp. Đó là kiểm kê `--kiem-bang`, KHÔNG phải
# toàn vòng: `t11` chạy `ruff check .` (~264 tệp, Codex lượt 4) — NGOÀI VÙNG CÓ CHỦ ĐÍCH; ca nền chạy mọi lượt, lượt tuần bù.
VUNG_THEM = {_SGD: (".claude/settings.json",)}
TIEN_TO_THEM = {_PTG: ("scripts/",)}
# Review connector PR #645 (P2): fallback :833-836 phải giữ cho workflow/security/runner (`.github/**`) và cấu hình
# TOÀN CỤC ở gốc kho (`pyproject.toml`, `sitecustomize.py`, manifest…) — không chỉ 5 đường của `VUNG_CHUNG`.
# Codex CLI lượt 1 trên feeee4ed: script thiết lập runner của `gate-registry` nằm NGOÀI `.github/` (`cai_actionlint.sh`
# ghi GITHUB_PATH ⇒ đổi cách tìm git/tar); `cai_cong_cu.sh` đọc `ops/cong_cu.yaml`. Chốt `loi_vung_thiet_lap` dẫn
# xuất từ ci.yml để một bước cài MỚI mà quên vùng thì ĐỎ. Tài liệu gốc: danh sách CHO PHÉP, tệp gốc lạ vẫn ⇒ ĐỦ.
TIEN_TO_CHUNG = ("ops/cai_", "ops/cong_cu")
LENH_REGISTRY = frozenset({"git config --global core.autocrlf false", "git config --global core.eol lf",
                           "git config --global core.abbrev 7", "actions/checkout@v4", "actions/setup-python@v5",
                           "python -m pip install --quiet PyYAML==6.0.3 jsonschema==4.26.0", "bash ops/cai_actionlint.sh",
                           "bash ops/cai_cong_cu.sh shellcheck", "bash ops/cai_cong_cu.sh rg",
                           "python ops/cong_cu.py kiem-tra --json", "python -m pip install --quiet ruff==0.15.15",
                           "ruff --version", "python .claude/dev/ci_dang_ky_test.py --chay"})
BAM_GATE_REGISTRY = "89516cf77c3ce734feadf348bfea8180254c67e8e8ec62a48e2f6ea1dc038452"
# WP748 r16: hai job nay la `targeted_mutant_gate` (NHANH_DON_DUOC_DICH, gom `--gop-dich`, tran 30 phut).
BAM_GATE_NHANH = "fe061a50668af83b6c9b6939f881ba37a30083bc72a27b52c2e02350835d626b"
GOC_TAI_LIEU = frozenset({"AGENTS.md", "CHANGELOG.md", "CLAUDE.md", "CONTEXT.md", "INSTALL.md", "README.md", "SKILL.md"})


def _cham_vung(x, vung):
    return x in vung or x.startswith(TIEN_TO_CHUNG) or ("/" not in x and x not in GOC_TAI_LIEU)
DAY_DU, CHE_DO_NHE, BIEN_SU_KIEN, BIEN_GOC, BIEN_DAU = "day_du", "nhe", "CI_DANG_KY_SU_KIEN", "CI_DANG_KY_GOC", "CI_DANG_KY_DAU"
ENV_REGISTRY = {BIEN_WORKERS: "2", BIEN_SU_KIEN: "${{ github.event_name }}",
                BIEN_GOC: "${{ github.event.pull_request.base.sha || github.event.before }}",
                BIEN_DAU: "${{ github.event.pull_request.head.sha || github.sha }}",
                "CI_DANG_KY_DOT_BIEN_MANH": "ops/nhanh_don_duoc_test.py",
                "CI_DANG_KY_GOP_KQ": "${{ needs.gate-nhanh-gop.result }}"}


def doc_ket_qua_gop(env=os.environ):
    """Vắng ngoài ci.yml (lượt tuần/local); khi CI ghim biến thì chỉ success là đạt."""
    raw = env.get("CI_DANG_KY_GOP_KQ")
    return None if raw is None else raw == "success"


def doc_diff(env=os.environ, chay=subprocess.run, kho=ROOT):
    """M1: tập đường dẫn đổi, hoặc None = KHÔNG ĐO ĐƯỢC (⇒ đủ). Ba trạng thái: tập · rỗng · None. `--no-renames` để
    đổi tên KHỎI vùng cũng tính là chạm vùng; SHA phải 40 hex thường, khác toàn-0 (push tạo nhánh) ⇒ không nhét cờ.
    Push: GOC phải là TỔ TIÊN của DAU — force-push lùi/phân kỳ thì ba chấm bỏ sót phía GOC (review Codex P1) ⇒ đủ."""
    su_kien, goc, dau = (env.get(k) or "" for k in (BIEN_SU_KIEN, BIEN_GOC, BIEN_DAU))
    if su_kien not in ("push", "pull_request") or not all(re.fullmatch(r"[0-9a-f]{40}", x) and x.strip("0") for x in (goc, dau)):
        return None
    try:
        if su_kien == "push" and chay(["git", "merge-base", "--is-ancestor", goc, dau], cwd=kho, capture_output=True).returncode:
            return None
        r = chay(["git", "diff", "--name-only", "--no-renames", "-z", f"{goc}...{dau}"], cwd=kho, capture_output=True)
    except Exception:
        return None
    return None if r.returncode else {x for x in r.stdout.decode("utf-8", "surrogateescape").split("\0") if x}


# #661 M4: CHỈ lượt tuần đặt biến này (ci.yml CẤM qua `loi_env_registry`); đột biến ĐỦ do job mảnh + gom (M5).
BIEN_MANH, BO_MANH, JOB_MANH, JOB_GOP, SO_MANH = ("CI_DANG_KY_DOT_BIEN_MANH", "ops/nhanh_don_duoc_test.py",
                                                  "dot-bien-manh", "dot-bien-gop", 8)   # WP748 r16: full audit 8 manh


def doc_bien_manh(env=os.environ):
    """M4: vắng/rỗng ⇒ None; ĐÚNG `BO_MANH` ⇒ nó; khác ⇒ ValueError (registry ĐỎ trước khi chạy bộ nào)."""
    raw = env.get(BIEN_MANH) or None
    if raw not in (None, BO_MANH):
        raise ValueError(f"{BIEN_MANH}={raw!r} ngoài miền {{vắng, {BO_MANH!r}}}")
    return raw


def ke_hoach(doi, nhe=NHE, manh=None):
    """M1: bộ → (chế độ, lý do). Chỉ bộ có trong `nhe` mới có thể nhẹ, và chỉ khi diff đo được mà không chạm vùng.
    #661 M4: `manh` (từ `doc_bien_manh`) ⇒ bộ ấy nhẹ bất kể diff; hai bộ kia không đổi."""
    kh = {}
    for p in nhe:
        vung = {p, p[:-len("_test.py")] + ".py", *VUNG_CHUNG, *VUNG_THEM.get(p, ())}
        cham = None if doi is None else sorted(x for x in doi if _cham_vung(x, vung) or x.startswith(TIEN_TO_THEM.get(p, ())))
        kh[p] = ((DAY_DU, "không đo được diff hoặc sự kiện không phải push/pull_request") if cham is None
                 else (DAY_DU, "diff chạm " + ", ".join(cham)) if cham else (CHE_DO_NHE, "diff không chạm vùng đột biến"))
    if manh:
        kh[manh] = (CHE_DO_NHE, "vòng đột biến do job mảnh + gom (ci-dot-bien-du.yml)")
    return kh


def env_theo_che_do(path, che_do):
    """M2: nhẹ ⇒ ĐẶT cờ; đủ ⇒ GỠ cờ dù cha có — cờ rò từ cha không được lặng lẽ biến đủ thành nhẹ."""
    return {k: (v if che_do == CHE_DO_NHE else None) for k, v in NHE.get(path, {}).items()}


def bam_gate_registry(data):
    """Băm TOÀN BỘ định nghĩa job `gate-registry` + `env`/`defaults` cấp workflow (JSON sắp khoá)."""
    d = data or {}
    goi = {"job": (d.get("jobs") or {}).get("gate-registry"), "env": d.get("env"), "defaults": d.get("defaults")}
    return hashlib.sha256(json.dumps(goi, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def bam_gate_nhanh(data):
    """Ghim trọn hai job mảnh/gom chịu trách nhiệm cho cờ nhẹ của registry."""
    jobs = (data or {}).get("jobs") or {}
    goi = {k: jobs.get(k) for k in ("gate-nhanh-manh", "gate-nhanh-gop")}
    return hashlib.sha256(json.dumps(goi, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def loi_gate_nhanh(data):
    jobs = (data or {}).get("jobs") or {}
    loi = [] if bam_gate_nhanh(data) == BAM_GATE_NHANH else ["hai job mảnh/gom nhanh_don_duoc lệch cấu hình ghim"]
    if (jobs.get("gate-registry") or {}).get("needs") != ["chuan-bi", "gate-nhanh-gop"]:
        loi.append("gate-registry không phụ thuộc phép gom đủ mảnh")
    return loi


def loi_vung_thiet_lap(data):
    """Bước của `gate-registry` theo danh sách CHO PHÉP từng chữ, VÀ cả job đóng băng bằng băm. Ba lượt Codex CLI liên
    tiếp vá một lối lại lọt lối khác (regex → `cd`/`working-directory` → `env.BASH_ENV`): liệt kê lối vào là thua từ
    thiết kế, nên mọi đổi của job (env, shell, defaults…) ⇒ ĐỎ cho tới khi ai đó cập nhật `BAM_GATE_REGISTRY` + vùng."""
    buoc = ((((data or {}).get("jobs") or {}).get("gate-registry") or {}).get("steps") or [])
    loi = [] if bam_gate_registry(data) == BAM_GATE_REGISTRY else [
        f"gate-registry đổi (băm {bam_gate_registry(data)}): rà vùng đột biến rồi cập nhật BAM_GATE_REGISTRY"]
    loi += [f"gate-registry: bước có working-directory: {b.get('name')}" for b in buoc if "working-directory" in b]
    loi += [f"gate-registry: lệnh ngoài danh sách cho phép: {x!r}" for b in buoc for x in _dong_lenh(b) if x not in LENH_REGISTRY]
    return loi + ([] if buoc else ["không thấy bước nào của gate-registry"])


def loi_env_registry(data):
    """M4: đúng MỘT bước registry, `env:` BẰNG ĐÚNG `ENV_REGISTRY` (thừa, thiếu, lệch chữ ⇒ ĐỎ)."""
    buoc = [b for v in ((data or {}).get("jobs") or {}).values() for b in (v or {}).get("steps") or []
            if "python .claude/dev/ci_dang_ky_test.py --chay" in _dong_lenh(b)]
    if len(buoc) != 1:
        return [f"phải có đúng một bước registry, thấy {len(buoc)}"]
    return [] if buoc[0].get("env") == ENV_REGISTRY else [f"env bước registry lệch: {buoc[0].get('env')}"]


WF_DOT_BIEN_DU = ROOT / ".github/workflows/ci-dot-bien-du.yml"
# GHIM (Codex CLI): cron bất kỳ lọt lịch năm (lượt 2); `name`/job id tự do lọt biểu thức hỏng (lượt 4).
CRON_DOT_BIEN_DU, TEN_WF_DU, JOB_DU = "17 19 * * 6", "đột biến đủ (hằng tuần)", "dot-bien-du"


def loi_actionlint(tep, tim=shutil.which, chay=subprocess.run):
    """#651 M4 (Codex lượt 5): dict sau `safe_load` mù YAML thô (`on:`/`true:` cùng thành True, khoá trùng bị nuốt) ⇒ W3
    qua `actionlint` THẬT trên tệp thô. Vắng công cụ (tên giả ⇒ FileNotFoundError) / lỗi chạy ⇒ KHÔNG ĐO ĐƯỢC ⇒ ĐỎ."""
    try:
        r = chay([tim("actionlint") or "actionlint-VANG", "-no-color", str(tep)], capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        return [f"KHÔNG ĐO ĐƯỢC: actionlint {type(e).__name__} — fail-close"]
    return [] if r.returncode == 0 else [f"actionlint rc={r.returncode}: " + " | ".join((r.stdout + r.stderr).splitlines()[:3])]


def loi_workflow_dot_bien_du(data, ci):
    """#651 M4: lượt ĐỦ hằng tuần. Danh sách CHO PHÉP ở mọi tầng; bước so BẰNG ĐÚNG `gate-registry` của `ci.yml` (trích từ
    CHÍNH hai tệp, không chép) trừ `env` bước registry = chỉ `CI_DANG_KY_WORKERS` ⇒ vắng biến diff ⇒ `ke_hoach` ĐỦ."""
    d, loi = data or {}, []
    if set(map(str, d)) - {"name", "on", "True", "permissions", "jobs"} or d.get("name") != TEN_WF_DU:
        loi.append(f"khoá cấp workflow ngoài danh sách cho phép: {sorted(map(str, d))}")
    on = d.get("on", d.get(True))  # PyYAML đọc khoá trần `on` thành True
    lich = on.get("schedule") if isinstance(on, dict) else None
    if not isinstance(on, dict) or set(on) != {"schedule", "workflow_dispatch"} or on["workflow_dispatch"] is not None:
        loi.append(f"`on` phải đúng schedule + workflow_dispatch trần: {on!r}")
    elif lich != [{"cron": CRON_DOT_BIEN_DU}]:
        loi.append(f"schedule phải đúng [{{cron: {CRON_DOT_BIEN_DU!r}}}] (hằng tuần): {lich!r}")
    if d.get("permissions") != {"contents": "read"}:
        loi.append(f"permissions phải đúng contents: read: {d.get('permissions')!r}")
    jobs, goc = d.get("jobs") or {}, (((ci or {}).get("jobs") or {}).get("gate-registry") or {})
    if set(jobs) != {JOB_DU, JOB_MANH, JOB_GOP} or not isinstance(jobs[JOB_DU], dict):
        return loi + [f"phải đúng ba job {JOB_DU}/{JOB_MANH}/{JOB_GOP}, thấy {sorted(map(str, jobs))}"]
    job = jobs[JOB_DU]
    if set(job) != {"runs-on", "timeout-minutes", "env", "steps"} or job["runs-on"] != "ubuntu-latest":
        loi.append(f"job: khoá {sorted(job)} / runs-on {job.get('runs-on')!r} ngoài danh sách cho phép")
    loi += [f"job: {k} lệch gate-registry" for k in ("timeout-minutes", "env") if not _bang_kieu(job.get(k), goc.get(k))]
    ky_vong = json.loads(json.dumps(goc.get("steps") or []))
    reg = [b for b in ky_vong if "python .claude/dev/ci_dang_ky_test.py --chay" in _dong_lenh(b)]
    if len(reg) != 1:
        return loi + [f"gate-registry của ci.yml có {len(reg)} bước registry, cần đúng một"]
    reg[0]["env"] = {BIEN_WORKERS: "2", BIEN_MANH: BO_MANH}
    loi += [] if _bang_kieu(job.get("steps"), ky_vong) else [f"bước lệch gate-registry của ci.yml (env registry chỉ được {reg[0]['env']})"]
    return loi + [f"job {j} lệch hình GHIM (#661 M5)" for j, v in zip((JOB_MANH, JOB_GOP), _job_manh_gop(goc)) if not _bang_kieu(jobs[j], v)]


def _bang_kieu(a, b):
    """`==` có xét KIỂU ở mọi tầng: `False == 0`, `90.0 == 90` làm matrix/số sai kiểu lọt (Codex #661 lượt 1 F01)."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(_bang_kieu(a[k], b[k]) for k in a)
    return len(a) == len(b) and all(map(_bang_kieu, a, b)) if isinstance(a, list) else a == b


def _job_manh_gop(goc):
    """#661 M5: hai job GHIM trọn; bước python + `env` TRÍCH từ `gate-registry`; matrix và N cùng từ `SO_MANH`."""
    dau = [{"uses": "actions/checkout@v4"}] + json.loads(json.dumps((goc.get("steps") or [])[2:3]))
    env, m = goc.get("env"), "${{ matrix.manh }}"
    # WP748 r16: full_mutant_audit ~73 800 s noi tiep (g12) => 8 manh x ~2,6 h => tran 360 (tran job GitHub).
    manh = {"runs-on": "ubuntu-latest", "timeout-minutes": 360, "env": env,
            "strategy": {"fail-fast": False, "matrix": {"manh": list(range(SO_MANH))}},
            "steps": dau + [{"name": "đột biến một mảnh", "run": "python ops/nhanh_don_duoc_test.py",
                             "env": {"NHANH_DON_DUOC_DICH": f"{m}/{SO_MANH}", "NHANH_DON_DUOC_DICH_RA": f"manh/manh-{m}.json",
                                     "NHANH_DON_DUOC_DICH_DU": "1"}},
                            {"uses": "actions/upload-artifact@v4", "with": {
                                "name": f"dot-bien-manh-{m}", "path": f"manh/manh-{m}.json", "if-no-files-found": "error"}}]}
    gop = {"needs": JOB_MANH, "runs-on": "ubuntu-latest", "timeout-minutes": 10,
           "steps": dau + [{"uses": "actions/download-artifact@v4",
                            "with": {"pattern": "dot-bien-manh-*", "path": "manh", "merge-multiple": True}},
                           {"name": "gom mảnh", "run": "python ops/nhanh_don_duoc_test.py --gop-du manh"}]}
    return manh, gop


def doc_so_worker(env=os.environ, la_windows=None):
    """M3 miền N: vắng/rỗng ⇒ 1; đúng một chữ số 1–8 ⇒ N; khác ⇒ ValueError. Windows ⇒ 1 (Q6)."""
    raw = env.get(BIEN_WORKERS) or "1"
    if not re.fullmatch(r"[1-8]", raw):
        raise ValueError(f"{BIEN_WORKERS}={raw!r} ngoài miền 1–8")
    return 1 if nen_la_windows(la_windows) else int(raw)


def _pid_song(pid, pgid=None, moc=None):
    """PID KHÔNG-zombie (zombie = đã chết) mang `pid`, thuộc nhóm `pgid`, hoặc mang dấu `moc` trong environ: con cháu
    đã `setsid` thoát nhóm vẫn thừa kế dấu (PR #640 P2); dấu ngẫu nhiên nên không giết nhầm PID tái dùng."""
    proc, dau = pathlib.Path("/proc"), f"{BIEN_MOC}={moc}".encode()
    if not proc.is_dir():  # POSIX không /proc: không lọc được zombie ⇒ nghiêng về "còn sống" (ĐỎ)
        return [0] * (not subprocess.call(["kill", "-0", f"-{pgid}" if pid is None else str(pid)], stderr=subprocess.DEVNULL))
    ra = []
    for d in ([proc / str(pid)] if pgid is None else proc.glob("[0-9]*")):
        with contextlib.suppress(OSError, IndexError, ValueError):
            f = (d / "stat").read_text().rsplit(")", 1)[1].split()
            if f[0] != "Z" and (pgid is None or int(f[2]) == pgid or (moc and dau in (d / "environ").read_bytes())):
                ra.append(int(d.name))
    return ra


def _chay_co_lap(argv, cwd=ROOT, goc_tam=None, gioi_han=GIAY_TOI_DA_MOT_BO, env_doi=None):
    """M2+M3: một bộ, một subprocess, BẢN SAO env có TMPDIR/TEMP/TMP riêng; không đụng
    `os.environ`/cwd của cha. Trả `(rc, ban_in, loi_ha_tang)`; `loi_ha_tang` khác None ⇒ ĐỎ.
    #643: `env_doi` đặt khoá (giá trị chuỗi) hoặc GỠ khoá (None) trên bản sao ấy."""
    tam, posix, moc = pathlib.Path(tempfile.mkdtemp(prefix="bo-", dir=goc_tam)), os.name != "nt", os.urandom(8).hex()
    env = dict(os.environ, TMPDIR=str(tam), TEMP=str(tam), TMP=str(tam), **{BIEN_MOC: moc})
    env = {k: v for k, v in {**env, **(env_doi or {})}.items() if v is not None}
    rc, ban_in, loi, p = -1, "", None, None
    try:
        p = subprocess.Popen(argv, cwd=cwd, env=env, text=True, encoding="utf-8", errors="backslashreplace",
                             stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             start_new_session=posix)
        ban_in, _ = p.communicate(timeout=gioi_han)
        if posix and _pid_song(None, p.pid, moc):  # cha thoát mà con cháu còn chạy ngoài vòng quản lý (review lượt 4)
            raise ChildProcessError("con cháu còn sống sau khi bộ thoát")
    except Exception as e:  # MỌI lỗi sau khởi chạy đi CHUNG đường dừng: giết cả nhóm, chờ ≤ 10 s, rồi mới dọn
        loi = (f"hết giờ {gioi_han} giây" if isinstance(e, subprocess.TimeoutExpired)
               else f"khởi chạy/chờ thất bại: {type(e).__name__}: {e}")
        if p is not None:
            han = time.monotonic() + GIAY_CHO_CAY_DUNG
            with contextlib.suppress(OSError):  # Windows: taskkill /T là nỗ lực, KHÔNG xác nhận được (Q6)
                os.killpg(p.pid, signal.SIGKILL) if posix else subprocess.call(
                    ["taskkill", "/T", "/F", "/PID", str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for q in (_pid_song(None, p.pid, moc) if posix else []):
                with contextlib.suppress(OSError): os.kill(q, signal.SIGKILL)
            with contextlib.suppress(Exception):
                p.kill(); ban_in = p.communicate(timeout=GIAY_CHO_CAY_DUNG)[0] or ban_in
            while posix and _pid_song(None, p.pid, moc) and time.monotonic() < han:
                time.sleep(0.05)
            if p.returncode is None or not posix or _pid_song(None, p.pid, moc):
                loi += "; KHÔNG xác nhận được cả cây tiến trình đã dừng"
    rc = p.returncode if p is not None and isinstance(p.returncode, int) else rc
    with contextlib.suppress(OSError):
        shutil.rmtree(tam)
    if tam.exists():
        loi = (loi + "; " if loi else "") + f"dọn thư mục tạm thất bại: {tam} còn"
    return rc, ban_in or "", loi


def _chay_that(path, goc_tam=None, che_do=DAY_DU):
    return _chay_co_lap([sys.executable, path], goc_tam=goc_tam, env_doi=env_theo_che_do(path, che_do))


def chay_moi(moi=MOI, cach_ly=CACH_LY, chay_mot=_chay_that,
             doc_moi_truong=moi_truong_hien_tai, doc_trong_ci=trong_ci,
             doc_nen_windows=nen_la_windows, so_worker=1, dong_ho=_gio_utc, bao_cao=None, kh=None):
    """Năm tham số sau là ĐƯỜNG NỐI ĐỂ ĐO, không phải cấu hình: phản chứng phải gọi
    được chính hàm này với bộ chạy giả, nếu không tầng tiêu thụ lại không ai canh.

    `doc_nen_windows` là seam thứ năm, thêm cho packet #456: nếu nền chỉ đọc được
    qua `os.name` thật thì phản chứng A3 phải có máy Windows mới chạy được, tức là
    không ai canh — đúng thứ bốn seam kia sinh ra để tránh.

    #637: `so_worker` = trần bộ ĐANG chạy; `dong_ho` = seam M1; `bao_cao` nhận JSON (không in ở
    đây ⇒ log nghiệp vụ giữ nguyên master, A5). Log theo thứ tự `MOI`; lỗi hạ tầng không qua `CACH_LY`.
    #643: `kh` = kế hoạch `ke_hoach()`; bộ vắng mặt ⇒ ĐỦ. Chế độ đủ của bộ trong `MAU_DAY_DU` đòi thêm dòng dương."""
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

    ex, muc = concurrent.futures.ThreadPoolExecutor(max_workers=so_worker), []
    tuong_lai = [ex.submit(_mot, path) for path, _ in ds]
    for (path, mau), tl in zip(ds, tuong_lai):
        rc, ban_in, loi, bd, kt = tl.result()
        che_do = (kh or {}).get(path, (DAY_DU,))[0]
        muc.append({"duong_dan": path, "rc": rc, "giay": round((kt - bd).total_seconds(), 3),
                    "bat_dau_utc": _iso(bd), "ket_thuc_utc": _iso(kt), "che_do": che_do})
        print(ban_in, end="")
        if loi is not None:
            print(f"CI_DANG_KY {path}: ĐỎ — LỖI HẠ TẦNG: {loi}, rc={rc}")
            do += 1
            continue
        ok = rc == 0 and any(bang_chung_xanh(ban_in, m)
                             for m in mau_theo_nen(path, mau, la_windows)
                             + ([MAU_NHE[path]] if che_do == CHE_DO_NHE and path in MAU_NHE else []))
        # #647: Windows không chạy đột biến của bộ có trong `MOI_WINDOWS` ⇒ không đòi dòng đủ ở đó.
        if (ok and che_do == DAY_DU and path in MAU_DAY_DU and not (la_windows and path in MOI_WINDOWS)
                and not bang_chung_xanh(ban_in, MAU_DAY_DU[path])):
            print(f"CI_DANG_KY {path}: chế độ đủ mà THIẾU dòng MUTANT dương")
            ok = False
        # #651 M1: nhẹ mà in dòng ĐỦ (bất kể số, cả Windows) ⇒ vòng đột biến vẫn chạy ⇒ ĐỎ.
        if ok and che_do == CHE_DO_NHE and path in MAU_NHE and re.search(MAU_DAY_DU[path], ban_in, re.M):
            print(f"CI_DANG_KY {path}: chế độ nhẹ mà VẪN in dòng đột biến ĐỦ — cờ nhẹ không có tác dụng")
            ok = False
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
    ex.shutdown()
    if bao_cao is not None:
        bao_cao.update(ke_hoach={p: {"che_do": c, "ly_do": ly} for p, (c, ly) in (kh or {}).items()},
                       N=so_worker, so_lop_logic=os.cpu_count(), bo=muc, so_lop_dung_duoc=len(os.sched_getaffinity(0))
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
        # WP748 r19 (cung lop Codex P2 o nhanh_don_duoc_test) — NaN/Infinity qua duoc `< 0`; int KHONG goi isfinite (OverflowError).
        g = m.get("giay")
        if type(m.get("rc")) is not int or not (type(g) is int or (type(g) is float and math.isfinite(g))) or g < 0:
            loi.append(f"rc/giay sai: {m.get('duong_dan')}")
        with contextlib.suppress(TypeError, ValueError):  # PARSE rồi so thời điểm, không so chuỗi (PR #640 P2)
            mo = [datetime.datetime.fromisoformat(x[:-1] + "+00:00") for x in mo if x.endswith("Z")]
        if len(mo) != 2 or not all(isinstance(x, datetime.datetime) for x in mo) or mo[1] < mo[0]:
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


G5_SELFTEST, G5_PROBE = "python ops/cong_cu_test.py", "python ops/cong_cu.py kiem-tra --json"
# #668: bán kính đột biến của `cong_cu_test` chia `SO_MANH_G5` job mảnh + một job gom. Mọi giá trị dưới đây GHIM, so
# BẰNG ĐÚNG (danh sách CHO PHÉP): `N` của env mảnh, matrix, tên/mẫu artifact và `if` của gom không được trôi lệch nhau.
JOB_G5_MANH, JOB_G5_GOP, SO_MANH_G5 = "gate-cong-cu", "gate-cong-cu-gop", 8
JOB_G5 = ("gate", "gate-registry", "gate-packet-loop", JOB_G5_MANH, JOB_G5_GOP)
G5_GOP = "python ops/cong_cu_test.py --gop manh"
G5_LENH = {"gate": [G5_PROBE, G5_SELFTEST], JOB_G5_MANH: [G5_PROBE, G5_SELFTEST], JOB_G5_GOP: [G5_GOP]}
G5_ENV = {"gate": {"CONG_CU_TEST_BAN_KINH": "manh"},
          JOB_G5_GOP: {"CONG_CU_TEST_GOP_CHE_DO": "${{ needs.chuan-bi.outputs.che_do }}"},   # wp892: gom đọc che_do
          JOB_G5_MANH: {"CONG_CU_TEST_MANH": f"${{{{ matrix.manh }}}}/{SO_MANH_G5}",
                        "CONG_CU_TEST_MANH_RA": "manh/manh-${{ matrix.manh }}.txt"}}
# wp879 (#879): Windows chỉ còn mảnh 0 và chỉ chạy ca nền ⇒ không ghi tệp mảnh, không tải lên, không có job gom Windows.
G5_MANH_LOAI = [{"os": "windows-latest", "manh": k} for k in range(1, SO_MANH_G5)]
# wp892 (#892): PR chỉ đổi hồ sơ ⇒ 8 mảnh `skipped`. Ghim NGUYÊN chuỗi: dạng `== 'day_du'` thì `che_do` rỗng/vắng cũng bỏ mảnh.
G5_MANH_IF = "${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"
G5_TAI_LEN = {"if": "runner.os != 'Windows'", "uses": "actions/upload-artifact@v4", "with": {
    "name": "gate-cong-cu-manh-${{ matrix.os }}-${{ matrix.manh }}", "path": "manh/manh-${{ matrix.manh }}.txt",
    "if-no-files-found": "error"}}
G5_TAI_VE = {"uses": "actions/download-artifact@v4", "with": {
    "pattern": "gate-cong-cu-manh-${{ matrix.os }}-*", "path": "manh", "merge-multiple": True}}
G5_GOP_IF = "${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}"
G5_GOP_NEEDS, G5_GOP_LOAI = ["chuan-bi", JOB_G5_MANH], [{"os": "windows-latest"}]
G5_THIET_LAP = frozenset({"git config --global core.autocrlf false", "git config --global core.eol lf", "git config --global core.abbrev 7",
                          "python -m pip install --quiet PyYAML==6.0.3 jsonschema==4.26.0", "bash ops/cai_actionlint.sh",
                          "bash ops/cai_cong_cu.sh shellcheck", "bash ops/cai_cong_cu.sh rg",
                          "actions/checkout@v4", "actions/setup-python@v5"})
# #668 F3 (Codex lượt 2, P1): tách dòng như BASH — chỉ `\n`, và chỉ cắt `space`/`tab` (blank của Bash). `splitlines()` cắt cả
# VT/FF/`\x1c`–`\x1e`/`\x85`/U+2028/U+2029/CR, nên `# x<VT>python ops/cong_cu_test.py --gop manh` hiện ra một lệnh gom mà
# Bash coi trọn là CHÚ THÍCH ⇒ bước gom rc=0 mà không gom gì. Mọi lệch còn lại (NBSP/VT ở đầu, CR/VT ở cuối) đều làm
# Bash chạy một lệnh KHÁC lệnh ghim ⇒ không tìm thấy lệnh hay sai đối số ⇒ ĐỎ, tức lệch về phía fail-closed.
def _dong_lenh(b): return [b.get("uses")] * ("uses" in b) + [x.strip(" \t") for x in str(b.get("run", "")).split("\n") if x.strip(" \t") and not x.lstrip(" \t").startswith("#")]
# #668 F1 (Codex lượt 1, P1): lệnh đúng chưa phải lệnh CHẠY. `shell: bash -n {0}` chỉ kiểm cú pháp ⇒ `--gop` rc=0 mà không
# gom gì; `defaults.run.shell`, `working-directory`, env kế thừa, `with.ref` của checkout là những lối khác cùng hình dạng.
# Nên NGỮ NGHĨA THỰC THI của job G5 cũng theo danh sách CHO PHÉP: khoá job/bước, shell, env, `with`, `runs-on`, matrix os.
G5_JOB_ENV = {"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
G5_KHOA_JOB = frozenset({"needs", "strategy", "runs-on", "timeout-minutes", "env", "steps"})
G5_KHOA_BUOC = frozenset({"name", "run", "shell", "env", "uses", "with"})
G5_WITH = {"actions/checkout@v4": ({}, {"fetch-depth": 0}), "actions/setup-python@v5": ({"python-version": "3.12"},)}
G5_OS = "${{ fromJson(needs.chuan-bi.outputs.os) }}"


def _loi_thuc_thi_g5(j, v, buoc):
    """Lỗi ngữ nghĩa thực thi của job G5 `j` trên các bước `buoc` (từ đầu tới HẾT bước G5; job mới: mọi bước)."""
    _if_duoc = {"if"} if j in (JOB_G5_GOP, JOB_G5_MANH, "gate-registry") else set()
    loi = [f"{j}: khoá job ngoài danh sách cho phép: {sorted(set(v) - G5_KHOA_JOB - _if_duoc)}"] \
        if set(v) - G5_KHOA_JOB - _if_duoc else []
    st = v.get("strategy") or {}
    if v.get("env") != G5_JOB_ENV or v.get("runs-on") != "${{ matrix.os }}" or set(st) != {"fail-fast", "matrix"} \
            or st.get("fail-fast") is not False or (st.get("matrix") or {}).get("os") != G5_OS:
        loi.append(f"{j}: env/runs-on/strategy cấp job lệch hình dạng ghim")
    for b in buoc:
        ten = b.get("name") or b.get("uses")
        # #668 F10 (Codex lượt 4, P1 — lần thứ BA của lớp này): GitHub nội suy `${{ }}` trên TOÀN thân `run` trước khi
        # Bash đọc, kể cả trong chú thích, nên một `fromJSON` hằng sinh được xuống dòng + lệnh mới mà ta đã bỏ đi cùng
        # chú thích. Không vá theo từng biến thể nữa: thân `run` của job G5 chỉ được có ký tự IN ĐƯỢC + `\n`, và không
        # biểu thức nào. Khi ấy thứ ta đọc (tách `\n`, cắt space/tab) CHÍNH LÀ thứ Bash đọc — đóng F3 lẫn F10 theo cấu trúc.
        than = str(b.get("run", ""))
        if "${{" in than or any(not (c == "\n" or c.isprintable()) for c in than):
            loi.append(f"{j}: bước {ten!r} có biểu thức GitHub hoặc ký tự không in được trong `run`")
        khoa = G5_KHOA_BUOC | ({"if"} if b == G5_TAI_LEN else set())   # wp879: `if` CHỈ ở đúng bước tải lên đã ghim
        if set(b) - khoa or b.get("shell", "bash") != "bash":
            loi.append(f"{j}: bước {ten!r} có khoá/shell ngoài danh sách cho phép: {sorted(set(b) - khoa)} shell={b.get('shell')!r}")
        elif "uses" in b and b.get("with", {}) not in G5_WITH.get(b["uses"], (b.get("with", {}),)):
            loi.append(f"{j}: bước {ten!r} có `with` lệch ghim: {b.get('with')}")
        elif "env" in b and not re.search(r"(?<![A-Za-z0-9_])cong_cu", str(b.get("run", ""))) and set(b["env"]) != {"AL_VER"}:
            loi.append(f"{j}: bước thiết lập {ten!r} có env ngoài AL_VER: {sorted(b['env'])}")
    return loi


def _loi_g5_manh_gop(j, v, buoc, i):
    """#668: phần RIÊNG của hai job mảnh/gom — matrix, `needs`, `if`, và bước artifact, mọi thứ so BẰNG ĐÚNG."""
    ma = ((v.get("strategy") or {}).get("matrix") or {})
    if j == JOB_G5_MANH:
        loi = [] if (ma.get("manh") == list(range(SO_MANH_G5)) and set(ma) == {"os", "manh", "exclude"}
                     and ma.get("exclude") == G5_MANH_LOAI) else [
            f"{j}: matrix phải đúng os + manh {list(range(SO_MANH_G5))} + exclude {G5_MANH_LOAI}, thấy {ma}"]
        loi += [] if v.get("needs") == "chuan-bi" and v.get("if") == G5_MANH_IF else [
            f"{j}: needs/if phải đúng 'chuan-bi'/{G5_MANH_IF!r}, thấy {v.get('needs')!r}/{v.get('if')!r}"]
        return loi + ([] if buoc[i + 1:] == [G5_TAI_LEN] else [f"{j}: sau bước G5 phải đúng MỘT bước tải lên {G5_TAI_LEN}"])
    loi = [] if set(ma) == {"os", "exclude"} and ma.get("exclude") == G5_GOP_LOAI else [
        f"{j}: matrix phải đúng os + exclude {G5_GOP_LOAI}, thấy {ma}"]
    loi += [] if v.get("needs") == G5_GOP_NEEDS and v.get("if") == G5_GOP_IF else [
        f"{j}: needs/if phải đúng {G5_GOP_NEEDS}/{G5_GOP_IF!r}, thấy {v.get('needs')!r}/{v.get('if')!r}"]
    loi += [] if i + 1 == len(buoc) else [f"{j}: bước gom phải là bước CUỐI"]
    return loi + ([] if [b for b in buoc[:i] if "download-artifact" in str(b.get("uses", ""))] == [G5_TAI_VE] else
                  [f"{j}: trước bước gom phải có đúng MỘT bước tải về {G5_TAI_VE}"])


def loi_g5_workflow(data):
    """M6 theo HÌNH DẠNG BƯỚC + danh sách CHO PHÉP (review tại chỗ lượt 1–3: nhận diện theo văn bản lọt ba lần): mỗi job G5
    đúng MỘT bước chạm `ops/cong_cu`, lệnh BẰNG ĐÚNG `G5_LENH` (mặc định [probe]), `env` BẰNG ĐÚNG `G5_ENV` (mặc định
    vắng), vô điều kiện; trước nó chỉ lệnh thiết lập (gom: thêm đúng bước tải về). #668: job mảnh/gom qua `_loi_g5_manh_gop`."""
    jobs = (data or {}).get("jobs") or {}
    loi = [f"thiếu job {j}" for j in JOB_G5 if j not in jobs]
    loi += [f"workflow có khoá `{k}` cấp workflow — kế thừa vào mọi job G5" for k in ("defaults", "env") if k in (data or {})]
    for j, v in jobs.items():
        buoc = (v or {}).get("steps") or []
        cham = [i for i, b in enumerate(buoc) if re.search(r"(?<![A-Za-z0-9_])cong_cu", str(b.get("run", "")))]
        if j not in JOB_G5 or len(cham) != 1:
            loi += [f"{j}: phải có đúng một bước G5 (chỉ ở {JOB_G5}), thấy {len(cham)}"] if cham or j in JOB_G5 else []
        elif _dong_lenh(buoc[cham[0]]) != G5_LENH.get(j, [G5_PROBE]):
            loi.append(f"{j}: bước G5 sai hình dạng: {_dong_lenh(buoc[cham[0]])}")
        elif buoc[cham[0]].get("env") != G5_ENV.get(j):
            loi.append(f"{j}: env bước G5 phải BẰNG ĐÚNG {G5_ENV.get(j)}, thấy {buoc[cham[0]].get('env')}")
        # #668 F14 (Codex lượt 5): VẮNG `shell` KHÔNG phải Bash — trên Windows mặc định là `pwsh`, và PowerShell lấy mã
        # thoát của lệnh CUỐI, nên probe đỏ + selftest xanh có thể thành bước xanh. Bước G5 phải KHAI RÕ `shell: bash`.
        elif buoc[cham[0]].get("shell") != "bash":
            loi.append(f"{j}: bước G5 phải khai rõ `shell: bash` (thấy {buoc[cham[0]].get('shell')!r})")
        elif {"if", "continue-on-error"} & (set(buoc[cham[0]]) | (set(v) - {"if"}
              if j == JOB_G5_GOP or (j == JOB_G5_MANH and v.get("if") == G5_MANH_IF)
              or (j == "gate-registry" and v.get("if") == "${{ !cancelled() }}"
                                         and v.get("needs") == ["chuan-bi", "gate-nhanh-gop"]) else set(v))):
            loi.append(f"{j}: bước G5 có điều kiện hoặc được phép bỏ qua lỗi")
        elif any(not set(_dong_lenh(b)) <= (G5_THIET_LAP | {G5_TAI_VE["uses"]} if j == JOB_G5_GOP else G5_THIET_LAP)
                 for b in buoc[:cham[0]]):
            loi.append(f"{j}: có lệnh ngoài danh sách thiết lập đứng trước probe G5")
        else:
            moi = j in (JOB_G5_MANH, JOB_G5_GOP)
            loi += _loi_thuc_thi_g5(j, v, buoc if moi else buoc[:cham[0] + 1])
            loi += _loi_g5_manh_gop(j, v, buoc, cham[0]) if moi else []
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
        # WP748 r18 (G5 g17 k01 đỏ vì gương `.codex/` bị Git bỏ qua) — hai chiều trên kho Git
        # thật: bỏ qua+không tracked ⇒ không đếm; KHÔNG bỏ qua, hoặc tracked dù nằm trong
        # thư mục bị bỏ qua, hoặc git không đo được ⇒ vẫn là "vị trí chưa biết".
        g = base / "git-bo-qua"
        (g / ".claude/dev").mkdir(parents=True)
        (g / ".github/workflows").mkdir(parents=True)
        (g / ".claude/dev/a_test.py").touch()
        (g / ".codex/hooks").mkdir(parents=True)
        (g / ".codex/hooks/x_test.py").touch()
        (g / ".gitignore").write_text(".codex/\n", encoding="utf-8")
        def _git(*a):
            subprocess.run(["git", "-C", str(g), *a], check=True, capture_output=True, timeout=120)
        _git("init", "-q")
        reg_g, wf_g = {".claude/dev/a_test.py"}, "python .claude/dev/ci_dang_ky_test.py --chay"
        old = set(DA_NOI)
        try:
            DA_NOI.clear()
            _them("r18-git-bo-qua-khong-dem", not kiem(g, reg_g, wf_g)[0]
                  and ".codex/hooks/x_test.py" not in tim(g)[2])
            def _git_hong(*a, **k): return subprocess.CompletedProcess(a, 128, "", "fatal")
            def _git_vang(*a, **k): raise OSError("git vang")
            _them("r18-git-hong-van-thay", ".codex/hooks/x_test.py" in tim(g, _git_hong)[2]
                  and ".codex/hooks/x_test.py" in tim(g, _git_vang)[2])
            kg = base / "khong-git"
            (kg / ".codex/hooks").mkdir(parents=True); (kg / ".codex/hooks/x_test.py").touch()
            (kg / ".gitignore").write_text(".codex/\n", encoding="utf-8")
            _them("r18-khong-git-van-thay", ".codex/hooks/x_test.py" in tim(kg)[2])
            (g / "la").mkdir(); (g / "la/y_test.py").touch()
            _them("r18-khong-bo-qua-van-la", any("la/y_test.py" in x for x in kiem(g, reg_g, wf_g)[0]))
            (g / "la/y_test.py").unlink()
            _git("add", "-f", ".codex/hooks/x_test.py")
            _them("r18-tracked-trong-thu-muc-bo-qua-van-la",
                  any(".codex/hooks/x_test.py" in x for x in kiem(g, reg_g, wf_g)[0]))
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
    # M4 cua #456 giu o tang MAU (`MOI` y het base, hai ca duoi). Lo #319 phia Linux nay DONG o tang CHE DO:
    # #647 M2 bat che do du doi `MAU_DAY_DU` (x/x, x>0) — `0/0` KHONG con duoc nhan tren Linux.
    _them("p456-linux-0-tren-0-nay-DO-boi-647", _dem_nen(_RONG456, False) == 1)
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
    # #878: hợp đồng runner_set của ci.yml — bản thật sạch; hai đột biến (đổi mặc định sang windows-only, bỏ option
    # windows-only) đều phải ĐỎ. Neo phải có đúng một lần, kẻo đột biến không đổi gì mà vẫn tính là "giết".
    _neo_md, _neo_op = "default: windows-and-ubuntu", "          - windows-only\n"
    _them("ci-dispatch-runner-set-that-sach", bool(ci_source) and not loi_ci_dispatch_windows(ci_source)[0])
    _them("ci-dispatch-runner-set-mac-dinh-windows-only-DO", ci_source.count(_neo_md) == 1 and bool(
          loi_ci_dispatch_windows(ci_source.replace(_neo_md, "default: windows-only", 1))[0]))
    _them("ci-dispatch-runner-set-bo-option-DO", ci_source.count(_neo_op) == 1 and bool(
          loi_ci_dispatch_windows(ci_source.replace(_neo_op, "", 1))[0]))
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
        "bat_dau_utc": "2026-09-25T08:00:03.000Z", "ket_thuc_utc": "2026-09-25T08:00:04.500Z", "che_do": DAY_DU})
    _them("p637-A1-json-hop-le", not loi_json_thoi_gian(_bc, _M) and _bc["N"] == 1)
    for _t, _f in (("bo-mot-muc", lambda b: b.pop()), ("rc-sai-kieu", lambda b: b[0].update(rc="0")),
                   ("giay-am", lambda b: b[0].update(giay=-1)), ("moc-khong-utc", lambda b: b[0].update(
                       bat_dau_utc="2026-09-25T08:00:00")), ("moc-dao", lambda b: b[0].update(
                       bat_dau_utc=b[0]["ket_thuc_utc"], ket_thuc_utc=b[0]["bat_dau_utc"])),
                   ("moc-lich-khong-ton-tai", lambda b: b[0].update(bat_dau_utc="2026-99-99T99:99:99.000Z")),
                   ("giay-nan", lambda b: b[0].update(giay=float("nan"))), ("giay-inf", lambda b: b[0].update(
                       giay=float("inf"))), ("giay-am-inf", lambda b: b[0].update(giay=float("-inf")))):
        _j = json.loads(json.dumps(_bc)); _f(_j["bo"])
        _them("p637-A1-" + _t, bool(loi_json_thoi_gian(_j, _M)))
    _j["bo"] = [{**m, "bat_dau_utc": "2026-09-25T08:00:00Z", "ket_thuc_utc": "2026-09-25T08:00:00.100Z"} for m in _bc["bo"]]
    _them("p637-A1-do-chinh-xac-khac-van-dung", not loi_json_thoi_gian(_j, _M))
    _j["bo"] = [{**m, "giay": 2} for m in _bc["bo"]]          # WP748 r19: giay int huu han van DUNG
    _them("p637-A1-giay-int-van-dung", not loi_json_thoi_gian(_j, _M))
    _j["bo"] = [{**m, "giay": 10 ** 400} for m in _bc["bo"]]  # int json khong lo: DUNG, khong duoc nem OverflowError
    try:
        _kq = not loi_json_thoi_gian(_j, _M)
    except OverflowError:
        _kq = False
    _them("p637-A1-giay-int-khong-lo-khong-nem", _kq)
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
            _rc, _bi, _loi = _chay_co_lap([sys.executable, "-c", "import subprocess as s,sys;print(s.Popen([sys.executable,'-c','import time;"
                                           "time.sleep(60)'],stdout=s.DEVNULL,stderr=s.DEVNULL).pid)"], goc_tam=_g, gioi_han=30)
            _them("p637-A3c-con-chau-song-sau-khi-bo-thoat-la-do", "còn sống" in (_loi or "") and not _pid_song(int(_bi.split()[0])))
            _rc, _bi, _loi = _chay_co_lap([sys.executable, "-c", "import subprocess as s,sys;print(s.Popen([sys.executable,'-c','import time;time.sleep(60)'],start_new_session=True,stdout=s.DEVNULL,stderr=s.DEVNULL).pid)"], goc_tam=_g, gioi_han=30)
            _them("p637-A3c-chau-setsid-thoat-nhom-van-bi-bat", "còn sống" in (_loi or "") and not _pid_song(int(_bi.split()[0])))
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
    for _i, _r in enumerate(("python -m ops.cong_cu_test", "python ops//cong_cu_test.py", "cd ops && python cong_cu_test.py")):
        _them(f"p637-A7-goi-tuong-duong-{_i}", _hong_wf("gate-registry", lambda b, i: b.insert(i + 1, {"run": _r})))
    _them("p637-A7-thieu-job", bool(loi_g5_workflow({"jobs": {k: v for k, v in _wf0["jobs"].items() if k != "gate-packet-loop"}})))
    _them("p637-A7-selftest-trong-echo", _hong_wf("gate", lambda b, i: b[i].update(run=b[i]["run"].replace(G5_SELFTEST, f"echo '{G5_SELFTEST}'"))))
    _them("p637-A7-probe-trong-heredoc", _hong_wf("gate-registry", lambda b, i: b[i].update(run=f"cat <<'EOF'\n{G5_PROBE}\nEOF\n")))
    _them("p637-A7-nang-doi-ten-cai-truoc-probe", _hong_wf("gate-registry", lambda b, i: b.insert(i, {"name": "cài registry", "run": "python .claude/dev/ci_dang_ky_test.py --chay"})))
    _them("p637-A7-uses-truoc-probe", _hong_wf("gate-registry", lambda b, i: b.insert(i, {"uses": "docker://python:3.12", "with": {"args": "scripts/tl.py --selftest"}})))
    _them("p637-A7-probe-continue-on-error", _hong_wf("gate-registry", lambda b, i: b[i].update({"continue-on-error": True})))
    _them("p637-A7-job-continue-on-error", bool(loi_g5_workflow({"jobs": {**_wf0["jobs"], "gate": {**_wf0["jobs"]["gate"], "continue-on-error": True}}})))
    _them("p637-A7-nhan-doi-selftest-trong-gate", _hong_wf("gate", lambda b, i: b.insert(i + 1, {"run": G5_SELFTEST})))
    # ── #668 A6: job mảnh/gom — mỗi hình dạng lệch một ca, sửa trên BẢN SAO của ci.yml thật. ──
    def _hong_job(j, f):
        w = json.loads(json.dumps(_wf0)); v = w["jobs"][j]; b = v["steps"]
        f(v, b, next(i for i, x in enumerate(b) if re.search(r"(?<![A-Za-z0-9_])cong_cu", str(x.get("run", "")))))
        return bool(loi_g5_workflow(w))
    _M, _G = JOB_G5_MANH, JOB_G5_GOP
    def _moi_mau(i, b, **kv): b[i] = {**b[i], **kv}
    for _t, _j, _f in (
            ("gate-thieu-env-ban-kinh", "gate", lambda v, b, i: b[i].pop("env")),
            ("gate-env-ban-kinh-la", "gate", lambda v, b, i: _moi_mau(i, b, env={"CONG_CU_TEST_BAN_KINH": "du"})),
            ("gate-env-thua-bien", "gate", lambda v, b, i: b[i]["env"].update({"CONG_CU_TEST_MANH": "0/8"})),
            ("registry-co-env-ban-kinh", "gate-registry", lambda v, b, i: _moi_mau(i, b, env={"CONG_CU_TEST_BAN_KINH": "manh"})),
            ("manh-sai-n", _M, lambda v, b, i: b[i]["env"].update({"CONG_CU_TEST_MANH": "${{ matrix.manh }}/7"})),
            ("manh-thieu-ra", _M, lambda v, b, i: b[i]["env"].pop("CONG_CU_TEST_MANH_RA")),
            ("manh-thieu-selftest", _M, lambda v, b, i: _moi_mau(i, b, run=G5_PROBE)),
            ("manh-matrix-thieu", _M, lambda v, b, i: v["strategy"]["matrix"].update({"manh": list(range(SO_MANH_G5 - 1))})),
            ("manh-matrix-thua", _M, lambda v, b, i: v["strategy"]["matrix"].update({"manh": list(range(SO_MANH_G5 + 1))})),
            ("manh-matrix-khoa-la", _M, lambda v, b, i: v["strategy"]["matrix"].update({"include": [{"manh": 9}]})),
            ("manh-job-if", _M, lambda v, b, i: v.update({"if": "${{ !cancelled() }}"})),
            ("manh-buoc-continue", _M, lambda v, b, i: _moi_mau(i, b, **{"continue-on-error": True})),
            ("manh-bo-tai-len", _M, lambda v, b, i: b.pop(i + 1)),
            ("manh-tai-len-khong-loi", _M, lambda v, b, i: b[i + 1]["with"].update({"if-no-files-found": "warn"})),
            ("manh-them-buoc-sau", _M, lambda v, b, i: b.append({"run": "true"})),
            ("gop-khong-needs-manh", _G, lambda v, b, i: v.update({"needs": "chuan-bi"})),
            ("gop-khong-if", _G, lambda v, b, i: v.pop("if")),
            ("gop-if-always", _G, lambda v, b, i: v.update({"if": "${{ always() }}"})),
            ("gop-lenh-khac", _G, lambda v, b, i: _moi_mau(i, b, run="python ops/cong_cu_test.py --gop khac")),
            ("gop-co-env", _G, lambda v, b, i: _moi_mau(i, b, env={"CONG_CU_TEST_BAN_KINH": "manh"})),
            ("gop-bo-tai-ve", _G, lambda v, b, i: b.pop(next(k for k, x in enumerate(b) if "download" in str(x.get("uses"))))),
            ("gop-tai-ve-mau-khac", _G, lambda v, b, i: b[i - 1]["with"].update({"pattern": "gate-cong-cu-manh-*"})),
            ("gop-hai-tai-ve", _G, lambda v, b, i: b.insert(i, dict(b[i - 1]))),
            ("gop-buoc-sau-gom", _G, lambda v, b, i: b.append({"run": "true"})),
            ("gop-matrix-them-manh", _G, lambda v, b, i: v["strategy"]["matrix"].update({"manh": [0]})),
            # wp879 N4: Windows quay về 8 mảnh / chỉ loại một phần · Linux còn 1 mảnh · tải lên mất `if` · gom quay về os động
            # hoặc mất điều kiện ubuntu (lượt `windows-only` sẽ ĐỎ oan vì thiếu mảnh).
            ("wp879-windows-8-manh", _M, lambda v, b, i: v["strategy"]["matrix"].pop("exclude")),
            ("wp879-windows-loai-thieu", _M, lambda v, b, i: v["strategy"]["matrix"]["exclude"].pop()),
            ("wp879-linux-1-manh", _M, lambda v, b, i: v["strategy"]["matrix"]["exclude"].extend(
                {"os": "ubuntu-latest", "manh": k} for k in range(1, SO_MANH_G5))),
            ("wp879-tai-len-khong-if", _M, lambda v, b, i: b[i + 1].pop("if")),
            ("wp879-gop-khong-loai-windows", _G, lambda v, b, i: v["strategy"]["matrix"].pop("exclude")),
            ("wp879-gop-loai-ubuntu", _G, lambda v, b, i: v["strategy"]["matrix"].update({"exclude": [{"os": "ubuntu-latest"}]})),
            ("wp879-gop-if-cu", _G, lambda v, b, i: v.update({"if": "${{ !cancelled() }}"})),
            # wp892 N2: if mảnh bị bỏ / đảo sang `== 'day_du'` (che_do rỗng ⇒ bỏ mảnh) / so lỏng; env gom bị bỏ / lấy nguồn khác.
            ("wp892-manh-bo-if", _M, lambda v, b, i: v.pop("if")),
            ("wp892-manh-if-day-du", _M, lambda v, b, i: v.update({"if": "${{ needs.chuan-bi.outputs.che_do == 'day_du' }}"})),
            ("wp892-manh-if-contains", _M, lambda v, b, i: v.update({"if": "${{ !contains(needs.chuan-bi.outputs.che_do, 'duong') }}"})),
            ("wp892-gop-bo-env", _G, lambda v, b, i: b[i].pop("env")),
            ("wp892-gop-env-hang", _G, lambda v, b, i: b[i].update({"env": {"CONG_CU_TEST_GOP_CHE_DO": "duong_nhanh"}})),
            ("wp892-gop-env-ten-khac", _G, lambda v, b, i: b[i].update({"env": {"CONG_CU_TEST_CHE_DO": "${{ needs.chuan-bi.outputs.che_do }}"}})),
            ("wp879-gop-if-windows", _G, lambda v, b, i: v.update(
                {"if": "${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'windows-latest') }}"})),
    ):
        _them(f"p668-A6-{_t}", _hong_job(_j, _f))
    for _j in (_M, _G):
        _them(f"p668-A6-thieu-job-{_j}", bool(loi_g5_workflow({"jobs": {k: v for k, v in _wf0["jobs"].items() if k != _j}})))
    # #668 F1: lệnh đúng mà KHÔNG chạy — shell/defaults/working-directory/env kế thừa/with. Mỗi lối một ca.
    _BN = "bash -n {0}"
    for _t, _j, _f in (
            ("gop-shell-chi-cu-phap", _G, lambda v, b, i: _moi_mau(i, b, shell=_BN)),
            ("manh-shell-chi-cu-phap", _M, lambda v, b, i: _moi_mau(i, b, shell=_BN)),
            ("gate-shell-chi-cu-phap", "gate", lambda v, b, i: _moi_mau(i, b, shell=_BN)),
            ("registry-shell-chi-cu-phap", "gate-registry", lambda v, b, i: _moi_mau(i, b, shell=_BN)),
            ("manh-shell-sh", _M, lambda v, b, i: _moi_mau(i, b, shell="sh")),
            ("gop-job-defaults-shell", _G, lambda v, b, i: v.update({"defaults": {"run": {"shell": _BN}}})),
            ("gate-job-defaults-shell", "gate", lambda v, b, i: v.update({"defaults": {"run": {"shell": _BN}}})),
            ("manh-working-directory", _M, lambda v, b, i: _moi_mau(i, b, **{"working-directory": "ops"})),
            ("manh-thiet-lap-working-directory", _M, lambda v, b, i: _moi_mau(0, b, **{"working-directory": "ops"})),
            ("manh-job-env-ban-kinh", _M, lambda v, b, i: v["env"].update({"CONG_CU_TEST_BAN_KINH": "manh"})),
            ("gate-job-env-thua", "gate", lambda v, b, i: v["env"].update({"BASH_ENV": "x"})),
            ("gop-runs-on-co-dinh", _G, lambda v, b, i: v.update({"runs-on": "ubuntu-latest"})),
            ("manh-matrix-os-co-dinh", _M, lambda v, b, i: v["strategy"]["matrix"].update({"os": ["ubuntu-latest"]})),
            ("manh-fail-fast", _M, lambda v, b, i: v["strategy"].update({"fail-fast": True})),
            ("gop-checkout-ref", _G, lambda v, b, i: b[1].update({"with": {"ref": "master"}})),
            ("manh-python-khac", _M, lambda v, b, i: b[2].update({"with": {"python-version": "3.11"}})),
            ("gate-thiet-lap-env-la", "gate", lambda v, b, i: b[i - 1].update({"env": {"BASH_ENV": "x"}})),
            ("manh-job-container", _M, lambda v, b, i: v.update({"container": "python:3.12"})),
    ):
        _them(f"p668-F1-{_t}", _hong_job(_j, _f))
    for _k, _v in (("defaults", {"run": {"shell": _BN}}), ("env", {"CONG_CU_TEST_BAN_KINH": "manh"})):
        _them(f"p668-F1-workflow-{_k}", bool(loi_g5_workflow({**_wf0, _k: _v})))
    # #668 F3: mọi ký tự `splitlines()` coi là xuống dòng mà Bash KHÔNG coi — giấu lệnh gom/lệnh mảnh trong một chú thích.
    for _ch in ("\x0b", "\x0c", "\r", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"):
        for _j, _lenh in ((_G, G5_GOP), (_M, G5_PROBE + "\n" + G5_SELFTEST), ("gate", G5_PROBE + "\n" + G5_SELFTEST)):
            _them(f"p668-F3-{_j}-chu-thich-nuot-U{ord(_ch):04X}",
                  _hong_job(_j, lambda v, b, i, c=_ch, l=_lenh: _moi_mau(i, b, run="# x" + c + l.replace("\n", "\n# x" + c))))
    _them("p668-F3-nbsp-truoc-chu-thich-la-lenh-la", _hong_job(_G, lambda v, b, i: _moi_mau(i, b, run="\u00a0# x\n" + G5_GOP)))
    # #668 F10: biểu thức GitHub trong `run` (kể cả trong chú thích) — mô tả của Codex lượt 4, dựng thành ca ở đây.
    _BT = "# ${{ fromJSON('\"\\nexit 0\\n\"') }}\n"
    for _t, _j, _f in (
            ("gop-chu-thich-fromjson", _G, lambda v, b, i: _moi_mau(i, b, run=_BT + G5_GOP)),
            ("manh-chu-thich-fromjson", _M, lambda v, b, i: _moi_mau(i, b, run=_BT + b[i]["run"])),
            ("gate-chu-thich-fromjson", "gate", lambda v, b, i: _moi_mau(i, b, run=_BT + b[i]["run"])),
            ("registry-chu-thich-fromjson", "gate-registry", lambda v, b, i: _moi_mau(i, b, run=_BT + b[i]["run"])),
            ("gate-thiet-lap-chu-thich-fromjson", "gate", lambda v, b, i: _moi_mau(0, b, run=_BT + b[0]["run"])),
            ("gop-chu-thich-bien-matrix", _G, lambda v, b, i: _moi_mau(i, b, run="# ${{ matrix.os }}\n" + G5_GOP)),
            ("manh-tab-dau-lenh", _M, lambda v, b, i: _moi_mau(i, b, run="\t" + b[i]["run"])),
    ):
        _them(f"p668-F10-{_t}", _hong_job(_j, _f))
    # #668 F14: bước G5 bỏ `shell` ⇒ Windows chạy bằng pwsh ⇒ ĐỎ ở mọi job G5.
    for _j in JOB_G5:
        _them(f"p668-F14-{_j}-vang-shell", _hong_job(_j, lambda v, b, i: b[i].pop("shell")))
    _them("p637-A8-khong-ung-vien", chon_so_worker({1: 100, 2: 101, 4: 102}) is None)
    _them("p637-A8-dung-bien", chon_so_worker({1: 200, 2: 110, 4: 100}) == 2)
    _them("p637-A8-vuot-bien", chon_so_worker({1: 200, 2: 110.5, 4: 100}) == 4)
    _them("p637-A8-trung-vi-khong-phai-trung-binh", chon_so_worker({1: [300, 100, 200], 2: [90, 500, 80], 4: [95, 95, 1]}) == 2)
    # ── #643: A1–A4. doc_diff qua `chay` giả; env qua tiến trình con THẬT; bằng chứng qua CHÍNH `chay_moi`. ──
    class _R:
        def __init__(s, rc, out): s.returncode, s.stdout = rc, out
    _A, _B, _P, _K = "a" * 40, "b" * 40, "ops/nhanh_don_duoc_test.py", "NHANH_DON_DUOC_KHONG_DOT_BIEN"

    def _dd(e, rc=0, out=b"x\0y\0", ghi=None):
        return doc_diff({BIEN_SU_KIEN: "push", BIEN_GOC: _A, BIEN_DAU: _B, **e},
                        lambda argv, **kw: (ghi.append(argv) if ghi is not None else None) or _R(rc, out))
    _them("p643-A1-push-doc-duoc", _dd({}) == {"x", "y"})
    _them("p643-A1-pull-request-doc-duoc", _dd({BIEN_SU_KIEN: "pull_request"}) == {"x", "y"})
    _them("p643-A1-diff-rong-la-tap-rong", _dd({}, out=b"") == set())
    for _t, _e in (("schedule", {BIEN_SU_KIEN: "schedule"}), ("dispatch", {BIEN_SU_KIEN: "workflow_dispatch"}),
                   ("su-kien-vang", {BIEN_SU_KIEN: ""}), ("goc-toan-0", {BIEN_GOC: "0" * 40}), ("goc-vang", {BIEN_GOC: ""}),
                   ("dau-39", {BIEN_DAU: "b" * 39}), ("dau-hoa", {BIEN_DAU: "B" * 40}), ("goc-la-co", {BIEN_GOC: "--output=/x"})):
        _them("p643-A1-khong-do-duoc-" + _t, _dd(_e) is None)
    _them("p643-A1-git-rc-khac-0", _dd({BIEN_SU_KIEN: "pull_request"}, rc=128) is None)
    _them("p643-A1-push-khong-phai-to-tien", doc_diff({BIEN_SU_KIEN: "push", BIEN_GOC: _A, BIEN_DAU: _B},
                                                        lambda argv, **kw: _R(int("merge-base" in argv), b"x\0")) is None)
    _them("p643-A1-git-nem", doc_diff({BIEN_SU_KIEN: "push", BIEN_GOC: _A, BIEN_DAU: _B},
                                      lambda *a, **k: (_ for _ in ()).throw(OSError("không có git"))) is None)
    _g, _h = [], []
    _dd({}, ghi=_g)
    _dd({BIEN_SU_KIEN: "pull_request"}, ghi=_h)
    _dif = ["git", "diff", "--name-only", "--no-renames", "-z", f"{_A}...{_B}"]
    _them("p643-A1-argv-git-push", _g == [["git", "merge-base", "--is-ancestor", _A, _B], _dif])
    _them("p643-A1-argv-git-pr", _h == [_dif])
    with tempfile.TemporaryDirectory() as _k:  # git THẬT: tiến, lùi (force-push), phân kỳ
        _gk = lambda *a: subprocess.run(["git", "-C", _k, "-c", "user.name=t", "-c", "user.email=t@t", *a],
                                        capture_output=True, text=True, check=True).stdout.strip()
        _gk("init", "-q"); _t = pathlib.Path(_k, "ops"); _t.mkdir()
        _c = []
        for _i, _f in enumerate(("ops/nhanh_don_duoc.py", "ops/nhanh_don_duoc.py", "docs.md")):
            if _i == 2: _gk("checkout", "-q", _c[0])
            pathlib.Path(_k, _f).write_text(str(_i)); _gk("add", "-A"); _gk("commit", "-qm", str(_i)); _c.append(_gk("rev-parse", "HEAD"))
        _dt = lambda g, d, sk="push": doc_diff({BIEN_SU_KIEN: sk, BIEN_GOC: g, BIEN_DAU: d}, kho=_k)
        _them("p643-A1-git-that-tien", _dt(_c[0], _c[1]) == {"ops/nhanh_don_duoc.py"})
        _them("p643-A1-git-that-force-push-lui", _dt(_c[1], _c[0]) is None)
        _them("p643-A1-git-that-force-push-phan-ky", _dt(_c[1], _c[2]) is None)
        _them("p643-A1-git-that-pr-ba-cham", _dt(_c[1], _c[2], "pull_request") == {"docs.md"})
    for _t, _doi, _cd in (("khong-do-duoc", None, DAY_DU), ("rong", set(), CHE_DO_NHE),
                          ("ngoai-vung", {"docs/x.md", _P + "c", "ops/nhanh_don_duoc.pyi"}, CHE_DO_NHE),
                          ("cham-bo", {_P}, DAY_DU), ("cham-dich", {"docs/x.md", "ops/nhanh_don_duoc.py"}, DAY_DU),
                          *((f"cham-chung-{_i}", {_v}, DAY_DU) for _i, _v in enumerate(VUNG_CHUNG)),
                          # #651 M2: workflow khác, `.github/checks/**`, bộ chọn, settings ⇒ NHẸ (bù bằng lượt đủ hằng tuần).
                          ("workflow-khac-nhe", {"docs/x.md", ".github/workflows/khac.yml"}, CHE_DO_NHE),
                          ("workflow-dot-bien-du-nhe", {".github/workflows/ci-dot-bien-du.yml"}, CHE_DO_NHE),
                          ("github-checks-nhe", {".github/checks/x.py"}, CHE_DO_NHE),
                          ("bo-chon-nhe", {".claude/dev/ci_dang_ky_test.py"}, CHE_DO_NHE),
                          ("settings-nhe", {".claude/settings.json"}, CHE_DO_NHE),
                          ("ci-yml-van-du", {".github/workflows/ci.yml"}, DAY_DU),
                          ("goc-pyproject", {"pyproject.toml"}, DAY_DU), ("goc-sitecustomize", {"sitecustomize.py"}, DAY_DU),
                          ("tai-lieu-va-ma-khac-van-nhe", {"docs/x.md", "ops/khac.py", "scripts/tl.py", "CLAUDE.md/x"}, CHE_DO_NHE),
                          ("tai-lieu-goc-van-nhe", {"README.md", "CLAUDE.md", "CHANGELOG.md"}, CHE_DO_NHE),
                          ("goc-md-la", {"POLICY.md"}, DAY_DU), ("goc-manifest", {"RELEASE_MANIFEST.json"}, DAY_DU),
                          *((f"thiet-lap-{_i}", {_v}, DAY_DU) for _i, _v in enumerate(
                              ("ops/cai_actionlint.sh", "ops/cai_cong_cu.sh", "ops/cong_cu.py", "ops/cong_cu.yaml")))):
        _them("p643-A1-ke-hoach-" + _t, ke_hoach(_doi)[_P][0] == _cd)
    _them("p643-A1-chi-bo-trong-NHE", set(ke_hoach(set())) == set(NHE) <= set(MOI) and set(MAU_DAY_DU) == set(NHE))
    _py, _cu = [sys.executable, "-c", f"import os; print(repr(os.environ.get({_K!r})))"], os.environ.get(_K)
    os.environ[_K] = "cha"
    try:
        _du, _nh = (_chay_co_lap(_py, env_doi=env_theo_che_do(_P, c))[1].strip() for c in (DAY_DU, CHE_DO_NHE))
    finally:
        os.environ.pop(_K) if _cu is None else os.environ.__setitem__(_K, _cu)
    _them("p643-A2-du-go-co-ro-tu-cha", _du == "None")
    _them("p643-A2-nhe-dat-co", _nh == "'1'")
    _them("p643-A2-bo-khong-trong-NHE-khong-doi-env", env_theo_che_do("a_test.py", CHE_DO_NHE) == {})
    _MUT = "MUTANT: giet = 10 · khong giet = 0 · khong do duoc = 0 / tong 10\n"

    def _kq(out, cd=None):
        with contextlib.redirect_stdout(io.StringIO()):
            return chay_moi(moi={_P: MOI[_P]}, cach_ly={}, chay_mot=lambda p: (0, out), doc_moi_truong=lambda: MOI_TRUONG_CI,
                            doc_trong_ci=lambda: True, doc_nen_windows=lambda: False, kh=cd and {_P: (cd, "giả")})
    _them("p643-A3-du-chi-co-8-8-la-do", _kq("8/8\n", DAY_DU) == 1)
    _them("p643-A3-mac-dinh-la-du", _kq("8/8\n") == 1)
    _them("p643-A3-du-co-mutant-dat", _kq("8/8\n" + _MUT, DAY_DU) == 0)
    _them("p643-A3-nhe-8-8-dat", _kq("8/8\n", CHE_DO_NHE) == 0)
    _them("p651-A1-nhanh-don-duoc-nhe-dong-mutant-van-dat", _kq("8/8\n" + _MUT, CHE_DO_NHE) == 0)  # không trong MAU_NHE
    _them("p643-A3-du-mutant-song-la-do", _kq("8/8\n" + _MUT.replace("khong giet = 0", "khong giet = 1"), DAY_DU) == 1)
    _them("p643-A3-du-mutant-0-la-do", _kq("8/8\n" + _MUT.replace("10", "0"), DAY_DU) == 1)
    _them("p643-A3-du-mutant-lech-tong-la-do", _kq("8/8\n" + _MUT.replace("tong 10", "tong 11"), DAY_DU) == 1)
    # ── #647: A2 qua CHÍNH `chay_moi` (dòng in giống bộ thật), A3 qua `ke_hoach`, env qua `env_theo_che_do`. ──
    _NH = "TONG: CA 41/41 dat · DOT BIEN 34 muc CHE DO NHE — do khi diff cham vung\nTONG: DAT\n"
    _DU = "TONG: CA 41/41 dat · DOT BIEN 34/34 bi giet\nTONG: DAT\n"
    _WI = "TONG: CA 41/41 dat · DOT BIEN 34 muc KHONG DO TREN WINDOWS — do tren ubuntu-latest\nTONG: DAT\n"

    def _kp(out, cd=None, win=False, path=_PTG):
        with contextlib.redirect_stdout(io.StringIO()):
            return chay_moi(moi={path: MOI[path]}, cach_ly={}, chay_mot=lambda p: (0, out), doc_moi_truong=lambda: MOI_TRUONG_CI,
                            doc_trong_ci=lambda: True, doc_nen_windows=lambda: win, kh=cd and {path: (cd, "giả")})
    for _t, _kqp in (("nhe-dong-nhe-dat", _kp(_NH, CHE_DO_NHE) == 0), ("nhe-dong-du-do", _kp(_DU, CHE_DO_NHE) == 1),
                     ("du-chi-dong-nhe-do", _kp(_NH, DAY_DU) == 1), ("mac-dinh-dong-nhe-do", _kp(_NH) == 1),
                     ("du-dong-du-dat", _kp(_DU, DAY_DU) == 0), ("du-0-0-do", _kp(_DU.replace("34/34", "0/0"), DAY_DU) == 1),
                     ("du-song-do", _kp(_DU.replace("34/34", "33/34"), DAY_DU) == 1),
                     ("nhe-bang-rong-do", _kp(_NH.replace("34 muc", "0 muc"), CHE_DO_NHE) == 1),
                     ("nhe-thieu-ca-do", _kp(_NH.replace("41/41", "38/41"), CHE_DO_NHE) == 1),
                     ("nhe-dong-windows-tren-linux-do", _kp(_WI, CHE_DO_NHE) == 1),
                     ("windows-du-dong-windows-dat", _kp(_WI, DAY_DU, True) == 0),
                     ("windows-du-dong-du-dat", _kp(_DU, DAY_DU, True) == 0),
                     ("windows-du-dong-nhe-do", _kp(_NH, DAY_DU, True) == 1),  # miễn MAU_DAY_DU ⇒ chỉ MAU_NHE canh
                     ("mau-nhe-khong-rao-sang-bo-khac", _kp(_NH, CHE_DO_NHE, path=_P) == 1),
                     # #651 M1 (P2 #649): nhẹ + dòng đủ ⇒ ĐỎ ở mọi nền, bất kể số, kể cả khi dòng nhẹ cũng có mặt.
                     ("651-nhe-dong-du-mutant-song-do", _kp(_DU.replace("34/34", "33/34"), CHE_DO_NHE) == 1),
                     ("651-nhe-ca-hai-dong-do", _kp(_NH + _DU, CHE_DO_NHE) == 1),
                     ("651-windows-nhe-dong-du-do", _kp(_DU, CHE_DO_NHE, True) == 1),
                     ("651-windows-nhe-dong-windows-dat", _kp(_WI, CHE_DO_NHE, True) == 0),
                     ("651-windows-nhe-dong-nhe-dat", _kp(_NH, CHE_DO_NHE, True) == 0)):
        _them("p647-A2-" + _t, _kqp)
    # ── #651 M3: bộ thứ ba qua CHÍNH `chay_moi`/`ke_hoach`/`env_theo_che_do`. ──
    _NS, _DS = _NH.replace("41/41", "44/44").replace("34 muc", "25 muc"), _DU.replace("41/41", "44/44").replace("34/34", "25/25")
    for _t, _kqp in (("nhe-dong-nhe-dat", _kp(_NS, CHE_DO_NHE, path=_SGD) == 0),
                     ("nhe-dong-du-do", _kp(_DS, CHE_DO_NHE, path=_SGD) == 1),
                     ("du-dong-du-dat", _kp(_DS, DAY_DU, path=_SGD) == 0),
                     ("du-chi-dong-nhe-do", _kp(_NS, DAY_DU, path=_SGD) == 1),
                     ("du-0-0-do", _kp(_DS.replace("25/25", "0/0"), DAY_DU, path=_SGD) == 1),
                     ("windows-du-dong-du-dat", _kp(_DS, DAY_DU, True, path=_SGD) == 0),
                     ("windows-du-chi-dong-nhe-do", _kp(_NS, DAY_DU, True, path=_SGD) == 1),  # không miễn: không trong MOI_WINDOWS
                     ("nhe-bang-rong-do", _kp(_NS.replace("25 muc", "0 muc"), CHE_DO_NHE, path=_SGD) == 1)):
        _them("p651-M3-" + _t, _kqp)
    for _t, _doi, _cd in (("cham-hook", {".claude/hooks/subagent_ghi_detect.py"}, DAY_DU), ("cham-bo", {_SGD}, DAY_DU),
                          ("cham-settings", {".claude/settings.json"}, DAY_DU), ("cham-chung", {"requirements.txt"}, DAY_DU),
                          ("bo-chon-nhe", {".claude/dev/ci_dang_ky_test.py"}, CHE_DO_NHE),
                          ("hook-khac", {".claude/hooks/pretooluse_guard.py"}, CHE_DO_NHE), ("tai-lieu", {"docs/x.md"}, CHE_DO_NHE)):
        _them("p651-M3-ke-hoach-" + _t, ke_hoach(_doi).get(_SGD, ("vắng",))[0] == _cd)
    _them("p651-M3-settings-chi-vung-bo-subagent", ke_hoach({".claude/settings.json"}).get(_PTG, ("vắng",))[0] == CHE_DO_NHE)
    for _t, _doi, _cd in (("tl-py", {"scripts/tl.py"}, DAY_DU), ("registry", {"scripts/tl_core/command_registry.py"}, DAY_DU),
                          ("tl-gws", {"scripts/tl_gws.py"}, DAY_DU), ("tl-core-khac", {"scripts/tl_core/x/y.py"}, DAY_DU),
                          ("tien-to-gia-nhe", {"scripts_x/tl.py", "docs/scripts/tl.py"}, CHE_DO_NHE)):
        _them("p651-P2-ptg-kiem-bang-" + _t, ke_hoach(_doi).get(_PTG, ("vắng",))[0] == _cd)
    _them("p651-P2-tl-core-chi-vung-ptg", ke_hoach({"scripts/tl_core/command_registry.py"}).get(_SGD, ("vắng",))[0] == CHE_DO_NHE
          and ke_hoach({"scripts/tl.py"}).get(_P, ("vắng",))[0] == CHE_DO_NHE)
    _them("p651-M3-env", env_theo_che_do(_SGD, CHE_DO_NHE) == {"SUBAGENT_GHI_DETECT_KHONG_DOT_BIEN": "1"}
          and env_theo_che_do(_SGD, DAY_DU) == {"SUBAGENT_GHI_DETECT_KHONG_DOT_BIEN": None})
    _them("p651-M3-mau-nhe-va-day-du-cho-bo-subagent", _SGD in MAU_NHE and _SGD in MAU_DAY_DU and _SGD in MOI)
    # ── #651 M4: lượt đủ hằng tuần, trích từ CHÍNH hai tệp YAML. ──
    _wd0 = yaml.safe_load(WF_DOT_BIEN_DU.read_text(encoding="utf-8"))
    _them("p651-M4-workflow-that-dat", not loi_workflow_dot_bien_du(_wd0, _wf0))

    def _hong_du(f):
        w = json.loads(json.dumps(_wd0, default=str).replace('"true":', '"on":'))
        f(w, next(iter(w["jobs"].values())))
        return bool(loi_workflow_dot_bien_du(w, _wf0))
    _them("p651-M4-ban-json-van-dat", not _hong_du(lambda w, j: None))  # khoá `on` dạng chuỗi cũng nhận

    def _buoc_reg(j): return next(b for b in j["steps"] if "ci_dang_ky_test.py --chay" in str(b.get("run", "")))
    for _t, _f in (("them-push", lambda w, j: w["on"].update(push=None)), ("them-pull-request", lambda w, j: w["on"].update(pull_request=None)),
                   ("bo-schedule", lambda w, j: w["on"].pop("schedule")), ("schedule-rong", lambda w, j: w["on"].update(schedule=[])),
                   ("schedule-hang-nam", lambda w, j: w["on"].update(schedule=[{"cron": "17 19 1 1 *"}])),
                   ("schedule-them-cron", lambda w, j: w["on"]["schedule"].append({"cron": "0 0 1 1 *"})),
                   ("bo-dispatch", lambda w, j: w["on"].pop("workflow_dispatch")),
                   ("env-workflow-co-nhe", lambda w, j: w.update(env={"NHANH_DON_DUOC_KHONG_DOT_BIEN": "1"})),
                   ("defaults-workflow", lambda w, j: w.update(defaults={"run": {"shell": "bash"}})),
                   ("env-job-co-nhe", lambda w, j: j["env"].update(PRETOOLUSE_GUARD_KHONG_DOT_BIEN="1")),
                   ("env-reg-su-kien", lambda w, j: _buoc_reg(j)["env"].update({BIEN_SU_KIEN: "push"})),
                   ("env-reg-co-nhe", lambda w, j: _buoc_reg(j)["env"].update(SUBAGENT_GHI_DETECT_KHONG_DOT_BIEN="1")),
                   ("env-reg-N-1", lambda w, j: _buoc_reg(j)["env"].update({BIEN_WORKERS: "1"})),
                   ("troi-ghim-pip", lambda w, j: j["steps"][3].update(run=j["steps"][3]["run"].replace("6.0.3", "6.0.2"))),
                   ("them-buoc", lambda w, j: j["steps"].insert(0, {"run": "true"})),
                   ("buoc-continue-on-error", lambda w, j: _buoc_reg(j).update({"continue-on-error": True})),
                   ("job-if", lambda w, j: j.update({"if": "false"})), ("job-windows", lambda w, j: j.update({"runs-on": "windows-latest"})),
                   ("timeout-lech", lambda w, j: j.update({"timeout-minutes": 5})),
                   ("permissions-ghi", lambda w, j: w.update(permissions={"contents": "write"})), ("hai-job", lambda w, j: w["jobs"].update(khac=j)),
                   ("khoa-la", lambda w, j: w.update({"run-name": "x"})),
                   ("concurrency", lambda w, j: w.update(concurrency={"group": "${{ fromJSON(github.event_name) }}"})),
                   ("name-bieu-thuc", lambda w, j: w.update(name="${{ broken() }}")),
                   ("job-id-la", lambda w, j: w.update(jobs={"1invalid": w["jobs"].pop(JOB_DU)}))):
        _them("p651-M4-" + _t + "-do", _hong_du(_f))

    def _j(w, ten): return w["jobs"][ten]
    for _t, _f in (("thieu-gop", lambda w, j: w["jobs"].pop(JOB_GOP)), ("gop-khong-needs", lambda w, j: _j(w, JOB_GOP).pop("needs")),
                   ("matrix-3", lambda w, j: _j(w, JOB_MANH)["strategy"]["matrix"].update(manh=[0, 1, 2])),
                   ("manh-sai-N", lambda w, j: _j(w, JOB_MANH)["steps"][2]["env"].update(NHANH_DON_DUOC_DICH="${{ matrix.manh }}/3")),
                   ("manh-bo-co-du", lambda w, j: _j(w, JOB_MANH)["steps"][2]["env"].pop("NHANH_DON_DUOC_DICH_DU")),
                   ("gop-targeted", lambda w, j: _j(w, JOB_GOP)["steps"][-1].update(run="python ops/nhanh_don_duoc_test.py --gop-dich manh")),
                   ("manh-if", lambda w, j: _j(w, JOB_MANH).update({"if": "false"})),
                   ("manh-continue-on-error", lambda w, j: _j(w, JOB_MANH).update({"continue-on-error": True})),
                   ("gop-if", lambda w, j: _j(w, JOB_GOP).update({"if": "always()"})),
                   ("gop-lenh-khac", lambda w, j: _j(w, JOB_GOP)["steps"][-1].update(run="true")),
                   ("matrix-bool", lambda w, j: _j(w, JOB_MANH)["strategy"]["matrix"].update(manh=[False, True] + list(range(2, SO_MANH)))),
                   ("matrix-float", lambda w, j: _j(w, JOB_MANH)["strategy"]["matrix"].update(manh=[0.0] + list(range(1, SO_MANH)))),
                   ("manh-timeout-float", lambda w, j: _j(w, JOB_MANH).update({"timeout-minutes": 360.0})),
                   ("du-fetch-depth-false", lambda w, j: j["steps"][1]["with"].update({"fetch-depth": False})),
                   # #705 F4: SUY từ ci.yml — hằng tay trôi khỏi trần thật thì ca thắng nhờ GIÁ TRỊ, thôi đo KIỂU.
                   ("du-timeout-float", lambda w, j: j.update({"timeout-minutes": float(_wf0["jobs"]["gate-registry"]["timeout-minutes"])})),
                   ("env-reg-thieu-manh", lambda w, j: _buoc_reg(j)["env"].pop(BIEN_MANH)),
                   ("env-reg-thua", lambda w, j: _buoc_reg(j)["env"].update(X="1"))):
        _them("p661-M5-" + _t + "-do", _hong_du(_f))
    _them("p661-M4-ke-hoach", all(ke_hoach(_d, manh=BO_MANH)[_P] == (CHE_DO_NHE, "vòng đột biến do job mảnh + gom (ci-dot-bien-du.yml)")
                                  and ke_hoach(_d, manh=BO_MANH)[_PTG] == ke_hoach(_d)[_PTG] for _d in (None, set(), {_P})))
    _them("p661-M4-doc-bien", [doc_bien_manh(e) for e in ({}, {BIEN_MANH: ""}, {BIEN_MANH: BO_MANH})] == [None, None, BO_MANH])
    for _v in (BO_MANH + " ", "ops/nhanh_don_duoc.py", _PTG):
        _n = 0
        with contextlib.suppress(ValueError): _n = doc_bien_manh({BIEN_MANH: _v}); _n = None
        _them(f"p661-M4-gia-tri-la-do-{_v!r}", _n is not None)
    _r = subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve()), "--chay"], capture_output=True, text=True,
                        env=dict(os.environ, **{BIEN_MANH: "ops/x.py", BIEN_WORKERS: "2"}), timeout=120)
    _them("p661-M4-main-do-truoc-khi-chay", _r.returncode == 2 and "TỔNG: ĐỎ" in _r.stdout and "CI_DANG_KY_KE_HOACH" not in _r.stdout)
    _them("p651-M4-rong-do", bool(loi_workflow_dot_bien_du(None, _wf0)))
    _them("p651-M4-ci-yml-doi-thi-do", bool(loi_workflow_dot_bien_du(_wd0, {"jobs": {}})))
    with tempfile.TemporaryDirectory() as _d:  # Codex lượt 5: YAML THÔ mà `safe_load` làm mất dấu ⇒ dict XANH, actionlint ĐỎ
        _tho, _w = WF_DOT_BIEN_DU.read_text(encoding="utf-8"), pathlib.Path(_d, "w.yml")
        for _t, _a, _b in (("goc", "", ""), ("on-thanh-true", "\non:\n", "\ntrue:\n"), ("khoa-True-rac", "\npermissions:", '\n"True": rac\npermissions:'),
                           ("cron-trung", '    - cron: "17', '    - cron: "0 0 1 1 *"\n      cron: "17'),
                           ("timeout-trung", "    timeout-minutes: 150\n", "    timeout-minutes: 5\n    timeout-minutes: 150\n")):
            _w.write_text(_v := _tho.replace(_a, _b, 1) if _a else _tho, encoding="utf-8")
            _them(f"p651-M4-yaml-tho-{_t}", not loi_actionlint(_w) if not _a else (
                _v != _tho and not loi_workflow_dot_bien_du(yaml.safe_load(_v), _wf0) and bool(loi_actionlint(_w))))
    _them("p651-M4-actionlint-vang-hoac-nem-do", all(loi_actionlint(WF_DOT_BIEN_DU, **_k) for _k in (
        {"tim": lambda _: None}, {"chay": lambda *a, **k: (_ for _ in ()).throw(OSError("x"))})))
    for _t, _doi, _cd in (("cham-hook", {".claude/hooks/pretooluse_guard.py"}, DAY_DU), ("cham-bo", {_PTG}, DAY_DU),
                          ("cham-chung", {"requirements.txt"}, DAY_DU), ("tai-lieu", {"docs/x.md"}, CHE_DO_NHE),
                          ("hook-khac", {".claude/hooks/subagent_ghi_detect.py"}, CHE_DO_NHE),
                          ("dich-bo-kia", {"ops/nhanh_don_duoc.py"}, CHE_DO_NHE)):
        _them("p647-A3-ke-hoach-" + _t, ke_hoach(_doi).get(_PTG, ("vắng",))[0] == _cd)  # .get: mất khoá ⇒ ĐỎ, không ném
    _them("p647-A3-hai-bo-doc-lap", ke_hoach({".claude/hooks/pretooluse_guard.py"})[_P][0] == CHE_DO_NHE)
    _them("p647-M2-env", env_theo_che_do(_PTG, CHE_DO_NHE) == {"PRETOOLUSE_GUARD_KHONG_DOT_BIEN": "1"}
          and env_theo_che_do(_PTG, DAY_DU) == {"PRETOOLUSE_GUARD_KHONG_DOT_BIEN": None})
    _them("p647-M2-mau-nhe-chi-cho-bo-trong-NHE", set(MAU_NHE) <= set(NHE))

    def _hong_env(f):
        w = json.loads(json.dumps(_wf0))
        f(next(b for b in w["jobs"]["gate-registry"]["steps"] if "ci_dang_ky_test.py --chay" in str(b.get("run", ""))), w)
        return bool(loi_env_registry(w))
    _them("p643-A4-workflow-that-dat", not loi_env_registry(_wf0))
    _them("p643-vung-thiet-lap-that-dat", not loi_vung_thiet_lap(_wf0))
    def _hong_reg(f):
        w = json.loads(json.dumps(_wf0)); f(w["jobs"]["gate-registry"]["steps"]); return bool(loi_vung_thiet_lap(w))
    for _i, _b in enumerate(({"run": "python scripts/tl_boot.py"}, {"run": "python scripts/'tl_boot.py'"},
                             {"run": "cd scripts\npython tl_boot.py"}, {"run": "python tl_boot.py", "working-directory": "scripts"},
                             {"run": "bash ./ops/cai_actionlint.sh"}, {"uses": "actions/cache@v4"})):
        _them(f"p643-vung-thiet-lap-buoc-la-{_i}-do", _hong_reg(lambda b: b.insert(0, dict(_b))))
    _them("p643-vung-thiet-lap-khong-co-buoc-do", bool(loi_vung_thiet_lap({"jobs": {}})))
    _them("p643-vung-thiet-lap-lenh-hop-le-doi-thu-muc-do", _hong_reg(lambda b: b.insert(0, {
        "run": "python ops/cong_cu.py kiem-tra --json", "working-directory": "scripts"})))
    _them("p643-vung-thiet-lap-bash-env-buoc-do", _hong_reg(lambda b: b[4].setdefault("env", {}).update(BASH_ENV="x.sh")))
    for _k, _v in (("env", {"BASH_ENV": "x.sh"}), ("defaults", {"run": {"shell": "bash"}})):
        _w = json.loads(json.dumps(_wf0)); _w[_k] = _v
        _them(f"p643-vung-thiet-lap-{_k}-cap-workflow-do", bool(loi_vung_thiet_lap(_w)))
    _w = json.loads(json.dumps(_wf0)); _w["jobs"]["gate-registry"].setdefault("defaults", {"run": {"working-directory": "scripts"}})
    _them("p643-vung-thiet-lap-defaults-cap-job-do", bool(loi_vung_thiet_lap(_w)))
    _w = json.loads(json.dumps(_wf0)); _w["jobs"]["gate"]["steps"].append({"run": "true"})
    _them("p643-vung-thiet-lap-job-khac-doi-van-dat", not loi_vung_thiet_lap(_w))
    # #651 M2: bộ chọn `ci_dang_ky_test.py` được miễn có chủ đích (tự canh bằng `phan_chung`; lượt đủ hằng tuần bù).
    _them("p643-lenh-registry-deu-trong-vung", all(_cham_vung(t, set(VUNG_CHUNG)) for x in LENH_REGISTRY
                                                   for t in x.split() if "/" in t and "@" not in t
                                                   and t != ".claude/dev/ci_dang_ky_test.py"))
    # #705: đo trần tới communicate qua đường runtime, không chỉ giá trị hằng.
    def _tran_runtime_dung():
        from unittest.mock import Mock, patch
        p = Mock(returncode=0, pid=1234567)
        p.communicate.return_value = ("", None)
        with patch.object(subprocess, "Popen", return_value=p), patch.dict(globals(), {"_pid_song": lambda *a: []}):
            ket_qua = _chay_that("bo-gia.py")
        return ket_qua == (0, "", None) and p.communicate.call_args.kwargs.get("timeout") == GIAY_TOI_DA_MOT_BO
    _them("p643-tran-bo-nho-hon-timeout-job", GIAY_TOI_DA_MOT_BO == 5400
          and GIAY_TOI_DA_MOT_BO < 60 * _wf0["jobs"]["gate-registry"]["timeout-minutes"] and _tran_runtime_dung())
    for _k in ENV_REGISTRY:
        _them(f"p643-A4-thieu-{_k}", _hong_env(lambda b, w: b["env"].pop(_k)))
        _them(f"p643-A4-lech-{_k}", _hong_env(lambda b, w: b["env"].update({_k: b["env"][_k] + " "})))
    _them("p643-A4-thua-khoa", _hong_env(lambda b, w: b["env"].update(X="1")))
    _them("p748-M4-ci-yml-bo-bien-manh-do", _hong_env(lambda b, w: b["env"].pop(BIEN_MANH)))
    _them("p748-gop-ket-qua-vang-ngoai-ci", doc_ket_qua_gop({}) is None)
    _them("p748-gop-ket-qua-success", doc_ket_qua_gop({"CI_DANG_KY_GOP_KQ": "success"}) is True)
    for _kq in ("", "failure", "skipped", "cancelled"):
        _them("p748-gop-ket-qua-" + (_kq or "rong") + "-do",
              doc_ket_qua_gop({"CI_DANG_KY_GOP_KQ": _kq}) is False)
    _them("p748-manh-gop-cau-hinh-that-dat", not loi_gate_nhanh(_wf0))
    for ten, sua in (
        ("thieu-manh", lambda w: w["jobs"].pop("gate-nhanh-manh")),
        ("thieu-gop", lambda w: w["jobs"].pop("gate-nhanh-gop")),
        ("thieu-phan-hoach", lambda w: w["jobs"]["gate-nhanh-manh"]["strategy"]["matrix"].update(manh=[0, 1, 2, 3, 4, 5, 6])),
        ("bo-bien-manh", lambda w: w["jobs"]["gate-nhanh-manh"]["steps"][3]["env"].pop("NHANH_DON_DUOC_DICH")),
        ("bo-gop-khoi-needs", lambda w: w["jobs"]["gate-registry"].update(needs="chuan-bi")),
    ):
        w = json.loads(json.dumps(_wf0))
        try:
            sua(w)
            _them("p748-manh-gop-" + ten, bool(loi_gate_nhanh(w)))
        except (KeyError, IndexError, TypeError):
            _them("p748-manh-gop-" + ten, False)
    _them("p643-A4-N-1", _hong_env(lambda b, w: b["env"].update({BIEN_WORKERS: "1"})))
    _them("p643-A4-bo-env", _hong_env(lambda b, w: b.pop("env")))
    _them("p643-A4-hai-buoc-registry", _hong_env(lambda b, w: w["jobs"]["gate"]["steps"].append(dict(b))))
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
            so_worker, manh = doc_so_worker(), doc_bien_manh()
        except ValueError as e:
            print("ĐỎ:", e); print("TỔNG: ĐỎ")
            return 2
        if doc_ket_qua_gop() is False:
            print("ĐỎ: job gom mảnh nhanh_don_duoc chưa success")
            print("TỔNG: ĐỎ")
            return 2
    if ns.mutant:
        killed = giet_windows_311_launcher_workflow(LAUNCHER_WORKFLOW.read_text(encoding="utf-8"))
        print(f"MUTANT {ns.mutant}: {'GIẾT' if killed else 'SỐNG'}")
        return 0 if killed else 1
    loi, tren_cay, trong_so = kiem()
    launcher_loi, launcher_chot = loi_launcher_windows()
    ruff_loi, ruff_chot = loi_ruff_ci()
    ci_disp_loi, _ = loi_ci_dispatch_windows()
    loi += launcher_loi
    loi += ci_disp_loi
    loi += ruff_loi
    wf = yaml.safe_load(CI_WORKFLOW.read_text(encoding="utf-8"))
    loi += ["G5 (M6): " + x for x in loi_g5_workflow(wf)] + ["ENV registry (#643 M4): " + x for x in loi_env_registry(wf)] \
        + ["VÙNG thiết lập (#643): " + x for x in loi_vung_thiet_lap(wf)] \
        + ["NHANH mảnh/gom (#748): " + x for x in loi_gate_nhanh(wf)]
    try:  # tệp rỗng ⇒ None ⇒ chốt vẫn chạy và ĐỎ; chỉ lỗi đọc/phân tích mới đi nhánh này
        loi_du = loi_workflow_dot_bien_du(yaml.safe_load(WF_DOT_BIEN_DU.read_text(encoding="utf-8")), wf)
    except (OSError, yaml.YAMLError) as e:
        loi_du = [f"không đọc được {WF_DOT_BIEN_DU.name}: {type(e).__name__}"]
    loi += ["ĐỘT BIẾN ĐỦ (#651 M4): " + x for x in loi_du + loi_actionlint(WF_DOT_BIEN_DU)]
    for x in loi: print("ĐỎ:", x)
    print(f"ĐĂNG KÝ: {tren_cay}/{trong_so}")
    print(f"TRẠNG THÁI: chan={trong_so - len(CACH_LY)} cach_ly={len(CACH_LY)}")
    print(f"LAUNCHER WINDOWS: {launcher_chot - len(launcher_loi)}/{launcher_chot} hợp đồng")
    print(f"RUFF CI: {ruff_chot - len(ruff_loi)}/{ruff_chot} hợp đồng")
    ok = not loi and tren_cay == trong_so and phan_chung()
    if ns.chay:
        bc, kh = {}, ke_hoach(doc_diff(), manh=manh)
        for p, (cd, ly) in kh.items(): print(f"CI_DANG_KY_KE_HOACH {p}: {cd} — {ly}")
        ok = chay_moi(so_worker=so_worker, bao_cao=bc, kh=kh,
                      chay_mot=lambda p: _chay_that(p, che_do=kh.get(p, (DAY_DU,))[0])) == 0 and ok
        print("CI_DANG_KY_THOI_GIAN " + json.dumps(bc, ensure_ascii=False))
        loi_js = loi_json_thoi_gian(bc)
        for x in loi_js: print("ĐỎ: JSON thời gian:", x)
        ok = ok and not loi_js
    print("TỔNG:", "ĐẠT" if ok else "ĐỎ")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
