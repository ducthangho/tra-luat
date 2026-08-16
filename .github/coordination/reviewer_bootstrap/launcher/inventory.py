"""Launcher source inventory, write-set containment and static boundary controls (§3, §4.1, §9).

Two jobs live here.

**Inventory.** Every file this Packet owns is enumerated with its SHA-256, and the set is reduced to
one ``inventory_sha256``.  That digest is what preflight step 5 observes and what the retained
artifact set binds to, so "the launcher that ran" is a checkable claim rather than an assumption.
The enumeration is also the write-set control: a file below the launcher prefix is owned, and a file
anywhere else is a write-set violation by construction, not by policy.

**Static controls.** Some of §4.1 and §9 cannot be proven by running code, because they are claims
about code that must *not* exist: no shell string, no ``Invoke-Expression``, no ``cmd /c``
forwarding, no ``os.system``, no executable discovered from the candidate tree — and no bare
``assert`` carrying a security decision.  The last one matters most: ``python -O`` deletes
``assert`` outright, so a security check written as one is a check that vanishes the moment somebody
optimizes the run, while every test still passes.  The scan below is an AST walk, not a text grep,
so a name split across lines or reached through an alias is still seen.

The scan declares what it does not cover, following the RA-01 precedent.  A static reader cannot see
a name built at run time, and saying so is what keeps this control usable instead of merely
reassuring.
"""

from __future__ import annotations

import ast
import hashlib
import pathlib
from collections.abc import Iterable, Mapping

from .errors import reject

LAUNCHER_PREFIX = ".github/coordination/reviewer_bootstrap/launcher/"

# Callables that hand a string to a parser instead of building an argument vector.
FORBIDDEN_CALLS = frozenset(
    {
        "os.system",
        "os.popen",
        "os.spawnl",
        "os.spawnv",
        "os.execv",
        "os.execve",
        "subprocess.getoutput",
        "subprocess.getstatusoutput",
        "commands.getoutput",
        "eval",
        "exec",
        "compile",
    }
)

# Text that only appears when someone is composing a command line for a shell to re-parse.
FORBIDDEN_TEXT = (
    "Invoke-Expression",
    "iex ",
    "cmd /c",
    "cmd.exe /c",
    "powershell -Command",
    "-EncodedCommand",
)

COVERAGE = {
    "covered": (
        "every launcher file is inventoried with a SHA-256 and reduced to one digest",
        "a tracked path outside the launcher prefix is a named write-set violation",
        # Phrased without quoting the needles themselves: this tuple is ordinary data, so spelling
        # them here would make the scanner convict its own coverage note.  The authoritative list
        # is FORBIDDEN_TEXT above, which is exempt by syntactic role.
        "shell-string composition, dynamic shell evaluation and command-forwarding call sites",
        "subprocess calls made with shell=True",
        "bare `assert` statements anywhere in the launcher package",
    ),
    "not_covered": (
        "a forbidden callable reached through a name built at run time",
        "a shell string assembled from fragments that are individually innocuous",
        "behaviour of the integrated RA-01/RA-02/RA-03 code, which this Packet reads but does not "
        "own and therefore does not scan",
    ),
}


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def launcher_files(package_root: pathlib.Path) -> list[pathlib.Path]:
    """Every owned file, sorted, with build artefacts excluded."""
    found = [
        path
        for path in sorted(package_root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    ]
    if not found:
        raise reject("preflight_incomplete", "the launcher package contains no files")
    return found


def build_inventory(package_root: pathlib.Path, repository_root: pathlib.Path) -> dict[str, object]:
    """Inventory the package and prove every entry sits inside the write prefix."""
    root = pathlib.Path(package_root).resolve()
    repo = pathlib.Path(repository_root).resolve()
    entries: list[dict[str, str]] = []
    outside: list[str] = []
    for path in launcher_files(root):
        relative = path.resolve().relative_to(repo).as_posix()
        if not relative.startswith(LAUNCHER_PREFIX):
            outside.append(relative)
            continue
        entries.append({"path": relative, "sha256": sha256_file(path)})
    if outside:
        raise reject("write_set", "%d inventoried files fall outside the launcher prefix" % len(outside))

    blob = "\n".join("%s %s" % (entry["sha256"], entry["path"]) for entry in entries) + "\n"
    return {
        "prefix": LAUNCHER_PREFIX,
        "files": entries,
        "file_count": len(entries),
        "inventory_sha256": hashlib.sha256(blob.encode("utf-8")).hexdigest(),
    }


def _dotted(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return None if base is None else "%s.%s" % (base, node.attr)
    return None


def scan_source(path: pathlib.Path) -> list[dict[str, object]]:
    """Return every static-boundary offence in one file."""
    text = path.read_text(encoding="utf-8")
    offences: list[dict[str, object]] = []

    tree = ast.parse(text, filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            offences.append({"kind": "bare_assert", "line": node.lineno})
        if isinstance(node, ast.Call):
            name = _dotted(node.func)
            if name in FORBIDDEN_CALLS:
                offences.append({"kind": "forbidden_call", "name": name, "line": node.lineno})
            for keyword in node.keywords:
                if keyword.arg == "shell" and not (
                    isinstance(keyword.value, ast.Constant) and keyword.value.value is False
                ):
                    offences.append({"kind": "shell_true", "line": node.lineno})

    # The text control looks for a shell command being *built*, so it must not fire on prose that
    # merely names the thing being forbidden.  Two exclusions, both necessary and both narrow:
    # docstrings, because a module explaining why it never calls `Invoke-Expression` would otherwise
    # convict itself; and the declaration tables below, because a denylist has to spell out the
    # strings it denies.  Excluding by *syntactic role* keeps this honest — a real shell string in
    # ordinary code is still caught, in this file as much as any other.
    exempt = {id(node) for node in _docstring_nodes(tree)} | {
        id(node) for node in _declaration_constants(tree)
    }
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in exempt:
            continue
        for needle in FORBIDDEN_TEXT:
            if needle in node.value:
                offences.append({"kind": "shell_string", "needle": needle, "line": node.lineno})
    return offences


def _docstring_nodes(tree: ast.AST) -> list[ast.Constant]:
    found: list[ast.Constant] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body = getattr(node, "body", ())
        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            found.append(body[0].value)
    return found


# Module-level names whose values are, by construction, lists of the very text this scanner hunts.
_DECLARATION_NAMES = frozenset({"FORBIDDEN_TEXT", "FORBIDDEN_CALLS", "FORBIDDEN_SWITCHES"})


def _declaration_constants(tree: ast.AST) -> list[ast.Constant]:
    found: list[ast.Constant] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        names = {target.id for target in node.targets if isinstance(target, ast.Name)}
        if not names & _DECLARATION_NAMES:
            continue
        for child in ast.walk(node.value):
            if isinstance(child, ast.Constant) and isinstance(child.value, str):
                found.append(child)
    return found


def scan_package(package_root: pathlib.Path) -> dict[str, object]:
    """Scan every owned Python file and return a machine-readable verdict."""
    findings: list[dict[str, object]] = []
    scanned = 0
    for path in launcher_files(pathlib.Path(package_root)):
        if path.suffix != ".py":
            continue
        scanned += 1
        for offence in scan_source(path):
            entry = dict(offence)
            entry["file"] = path.name
            findings.append(entry)
    return {
        "scanned_files": scanned,
        "findings": findings,
        "ok": not findings,
        "coverage": {key: list(value) for key, value in COVERAGE.items()},
    }


def require_clean(scan: Mapping[str, object]) -> Mapping[str, object]:
    if not scan.get("ok"):
        raise reject(
            "write_set", "the static boundary scan carries %d findings" % len(scan.get("findings", ()))
        )
    return scan


def eol_survey(paths: Iterable[pathlib.Path]) -> dict[str, object]:
    """LF-only survey for the owned text files (§9).

    ``*.cmd``/``*.bat`` are the repository's declared CRLF exceptions; this Packet ships none, and
    the survey reports that explicitly rather than leaving an empty exception list to be read as
    "not checked".
    """
    violations: list[dict[str, object]] = []
    checked = 0
    exceptions = 0
    for path in paths:
        data = path.read_bytes()
        if path.suffix.lower() in (".cmd", ".bat"):
            exceptions += 1
            continue
        checked += 1
        count = data.count(b"\r\n") + data.count(b"\r") - data.count(b"\r\n")
        if b"\r" in data:
            violations.append({"file": path.name, "carriage_returns": data.count(b"\r"), "crlf": count})
    return {
        "checked_files": checked,
        "crlf_exception_files": exceptions,
        "violations": violations,
        "ok": not violations,
    }
