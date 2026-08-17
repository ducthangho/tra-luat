"""Static boundary of the envelope package: what this code is allowed to be able to do.

The scan is purely structural.  Every rule fires on an `Import`, a `Call`, an attribute chain or
an `Assert` node — never on raw source text — which is what lets this module carry the forbidden
names in its own tables without accusing itself.  A text scanner cannot do that, and the version
of it that special-cases its own file is a scanner with a hole in the exact shape of the file an
attacker would edit.

Alias resolution is BORROWED from RA-01 (`core/scanner.py`), not re-implemented.  That resolver
already learned that `import subprocess as sp` and `runner = sp.run` must canonicalise to the same
name; a private second copy here would relearn it late.  The reuse is measured, not promised:
`selftest.py::POS-018` fails if these names stop being the same objects.

COVERAGE says what the scan does NOT see.  A static scan is a smoke alarm, and the honest way to
own that is to write down where it is deaf.
"""

from __future__ import annotations

import ast
import pathlib

from core import scanner as core_scanner

from .errors import reject

_alias_map = core_scanner._alias_map
_resolve_call = core_scanner._resolve_call
_dotted = core_scanner._dotted

COVERAGE = {
    "covered": (
        "import / from-import of any module outside the closed allowlist, by named class",
        "one level of module and function aliasing, inherited from core/scanner.py",
        "constant-target dynamic import through importlib.import_module or __import__",
        "os process, shell and filesystem-mutation calls by exact dotted name",
        "Windows process and Job Object APIs by call name",
        "durable-store, claim, lease and delegation operations by call name",
        "ambient environment reads through os.environ / os.getenv anywhere in the prefix",
        "assert statements in every file, including this suite",
        "imports of a flat launcher module outside launcher.envelope",
        "relative imports that climb above this package with two dots or more",
    ),
    "not_covered": (
        "capability reached through getattr with a computed name, or a table of callables",
        "aliasing chained deeper than core/scanner.py resolves",
        "a helper the package imports legitimately that itself spawns a process",
        "anything reached from a string built at runtime",
    ),
    "real_boundary": "the packet write set plus review: this scan is evidence, not enforcement",
}

# Sibling modules this package is allowed to reach.  Anything else in core/, oracle/, gateway/ or
# sandbox/ is a boundary crossing, including the ones that would be convenient.
SANCTIONED_SIBLING_MODULES = frozenset(
    {"oracle.safe_io", "oracle.trusted_inventory", "core.scanner", "core.guards"}
)
SIBLING_PACKAGE_ROOTS = frozenset({"core", "oracle", "gateway", "sandbox"})

ALLOWED_IMPORT_ROOTS = frozenset(
    {
        "__future__",
        "ast",
        "collections",
        "contextlib",
        "copy",
        "dataclasses",
        "hashlib",
        "inspect",
        "io",
        "json",
        "os",
        "pathlib",
        "re",
        "stat",
        "sys",
        "tempfile",
        "types",
        "typing",
        "unittest",
    }
)

# Named classes, so the report says WHY a module is refused instead of only that it is.
IMPORT_CLASSES = {
    "network_or_github_client": frozenset(core_scanner.FORBIDDEN_IMPORTS)
    | frozenset({"httplib", "urllib3", "websockets", "paramiko", "github", "githubkit"}),
    "process_spawn": frozenset(
        {
            "subprocess",
            "multiprocessing",
            "concurrent",
            "threading",
            "signal",
            "pty",
            "tty",
            "ctypes",
            "winreg",
            "_winapi",
            "msvcrt",
            "resource",
            "sched",
        }
    ),
    "shell_execution": frozenset({"shlex", "shutil", "pipes", "commands"}),
    "dynamic_code": frozenset({"importlib", "imp", "pickle", "marshal", "runpy", "code", "codeop"}),
}

FENCED_LAUNCHER_ROOTS = frozenset(
    {"launcher_bootstrap", "reviewer_launcher", "claude_launcher", "wp125_launcher", "flat_launcher"}
)
ENVELOPE_PACKAGE = "launcher.envelope"

_OS_PROCESS_CALLS = frozenset(
    {
        "os.system",
        "os.popen",
        "os.fork",
        "os.forkpty",
        "os.posix_spawn",
        "os.posix_spawnp",
        "os.startfile",
        "os.kill",
        "os.abort",
    }
    | {"os.exec%s" % suffix for suffix in ("l", "le", "lp", "lpe", "v", "ve", "vp", "vpe")}
    | {"os.spawn%s" % suffix for suffix in ("l", "le", "lp", "lpe", "v", "ve", "vp", "vpe")}
)
_OS_MUTATION_CALLS = frozenset(
    {
        "os.chmod",
        "os.chown",
        "os.remove",
        "os.unlink",
        "os.rmdir",
        "os.rename",
        "os.replace",
        "os.link",
        "os.symlink",
        "os.mkdir",
        "os.makedirs",
        "os.removedirs",
        "os.truncate",
        "os.write",
        "os.putenv",
        "os.unsetenv",
        "os.open",
        "os.fdopen",
    }
)
_DYNAMIC_CALLS = frozenset({"eval", "exec", "compile", "__import__", "importlib.import_module"})
_BARE_FORBIDDEN_CALLS = frozenset({"eval", "exec", "compile", "__import__", "open", "input", "breakpoint"})

# Matched on the call's last name component: these have no non-hostile spelling in this package.
_WINDOWS_PROCESS_APIS = frozenset(
    {
        "CreateProcessW",
        "CreateProcessA",
        "ShellExecuteW",
        "WinExec",
        "OpenProcess",
        "TerminateProcess",
        "CreateJobObjectW",
        "AssignProcessToJobObject",
        "SetInformationJobObject",
        "TerminateJobObject",
    }
)
_DURABLE_STATE_APIS = frozenset(
    {
        "post_heartbeat",
        "create_heartbeat",
        "post_verdict",
        "create_verdict",
        "acquire_lease",
        "renew_lease",
        "release_lease",
        "record_claim",
        "write_ledger",
        "append_ledger",
        "handle_transport",
        "dispatch_packet",
        "delegate_packet",
    }
)
_FILESYSTEM_MUTATION_METHODS = frozenset(
    {
        "write_text",
        "write_bytes",
        "touch",
        "mkdir",
        "makedirs",
        "chmod",
        "unlink",
        "rmdir",
        "rmtree",
        "symlink_to",
        "hardlink_to",
        "mkdtemp",
        "mkstemp",
    }
)
_AMBIENT_ENVIRONMENT = frozenset({"os.environ", "os.getenv", "os.environb", "os.environ.get"})


def _finding(filename: str, category: str, detail: str, lineno: int) -> dict[str, object]:
    return {"file": filename, "category": category, "detail": detail, "line": lineno}


def _classify_import(full: str, extra: str) -> tuple[str, str] | None:
    """Return (category, detail) when the imported name is refused, else None."""

    candidates = {full}
    if extra:
        candidates.add("%s.%s" % (full, extra))
    if candidates & SANCTIONED_SIBLING_MODULES:
        return None
    root = full.split(".")[0]
    if root == "launcher":
        if full == ENVELOPE_PACKAGE or full.startswith(ENVELOPE_PACKAGE + "."):
            return None
        return ("fenced_launcher_import", full)
    if root in FENCED_LAUNCHER_ROOTS:
        return ("fenced_launcher_import", full)
    for category, members in IMPORT_CLASSES.items():
        if root in members:
            return (category, full)
    if root in SIBLING_PACKAGE_ROOTS:
        return ("package_boundary", full)
    if root in ALLOWED_IMPORT_ROOTS:
        return None
    return ("import_not_allowed", full)


def scan_source(source: str, filename: str, *, allow_filesystem_mutation: bool = False) -> list[dict[str, object]]:
    """Scan one module's source and return every named finding.

    `allow_filesystem_mutation` is the single concession: the suite has to create and seal its own
    fixtures, so the mutation rule is applied to implementation modules only.  It is not a trust
    flag for anything else — every other rule holds for every file under the prefix.
    """

    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as exc:
        raise reject("boundary_unparsable", "%s cannot be parsed" % filename) from exc

    modules, funcs = _alias_map(tree)
    findings: list[dict[str, object]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            findings.append(
                _finding(filename, "security_assert", "assert", node.lineno)
            )
        elif isinstance(node, ast.Import):
            for alias in node.names:
                verdict = _classify_import(alias.name, "")
                if verdict is not None:
                    findings.append(_finding(filename, verdict[0], verdict[1], node.lineno))
        elif isinstance(node, ast.ImportFrom):
            if node.level == 1:
                # A sibling module inside this package: in scope by construction.
                continue
            if node.level:
                # `from ..x import y` climbs OUT of the package while looking local.  Two dots is
                # the shortest way to reach the flat launcher this Packet is fenced away from.
                findings.append(
                    _finding(filename, "package_boundary", "relative level %d" % node.level, node.lineno)
                )
                continue
            module = node.module or ""
            for alias in node.names:
                verdict = _classify_import(module, alias.name)
                if verdict is not None:
                    findings.append(_finding(filename, verdict[0], verdict[1], node.lineno))
        elif isinstance(node, ast.Call):
            called = _resolve_call(node.func, modules, funcs) or ""
            basename = called.split(".")[-1]
            root = called.split(".")[0]
            if called in _OS_PROCESS_CALLS or root == "subprocess":
                findings.append(_finding(filename, "process_spawn", called, node.lineno))
            elif isinstance(node.func, ast.Name) and node.func.id == "open":
                # Every file this package reads goes through the hardened sealed reader.  A bare
                # `open` is the one call that would quietly reintroduce an unchecked read.
                findings.append(_finding(filename, "unmediated_file_read", called, node.lineno))
            elif called in _DYNAMIC_CALLS or (
                isinstance(node.func, ast.Name) and node.func.id in _BARE_FORBIDDEN_CALLS
            ):
                findings.append(_finding(filename, "dynamic_code", called, node.lineno))
            elif basename in _WINDOWS_PROCESS_APIS:
                findings.append(_finding(filename, "windows_process_api", called, node.lineno))
            elif basename in _DURABLE_STATE_APIS:
                findings.append(_finding(filename, "durable_state_operation", called, node.lineno))
            elif called in _AMBIENT_ENVIRONMENT:
                findings.append(_finding(filename, "ambient_environment_read", called, node.lineno))
            elif not allow_filesystem_mutation and (
                called in _OS_MUTATION_CALLS or basename in _FILESYSTEM_MUTATION_METHODS
            ):
                findings.append(_finding(filename, "filesystem_mutation", called, node.lineno))
        elif isinstance(node, ast.Attribute):
            dotted = _dotted(node) or ""
            if dotted in _AMBIENT_ENVIRONMENT:
                findings.append(_finding(filename, "ambient_environment_read", dotted, node.lineno))

    findings.sort(key=lambda item: (item["file"], item["line"], item["category"], item["detail"]))
    return findings


HERE = pathlib.Path(__file__).resolve().parent
SUITE_FILENAME = "selftest.py"


def implementation_modules(root: pathlib.Path | None = None) -> list[pathlib.Path]:
    base = HERE if root is None else pathlib.Path(root)
    return [path for path in sorted(base.glob("*.py")) if path.name != SUITE_FILENAME]


def scan_prefix(root: pathlib.Path | None = None) -> dict[str, object]:
    """Scan every module under the prefix and return the complete finding list."""

    base = HERE if root is None else pathlib.Path(root)
    findings: list[dict[str, object]] = []
    scanned: list[str] = []
    for path in sorted(base.glob("*.py")):
        source = path.read_text(encoding="utf-8")
        scanned.append(path.name)
        findings.extend(
            scan_source(
                source,
                path.name,
                allow_filesystem_mutation=path.name == SUITE_FILENAME,
            )
        )
    return {"scanned": scanned, "findings": findings, "clean": not findings}
