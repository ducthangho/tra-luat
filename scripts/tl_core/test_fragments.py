# -*- coding: utf-8 -*-
"""Deterministic discovery/loading for packet-owned selftest fragments.

The public CLI remains ``scripts/tl.py --selftest``.  This deep internal
module owns filesystem ordering and the fragment contract; ``tl_selftest`` is
only the adapter that evaluates returned cases.
"""
from __future__ import annotations

import ast
from collections import Counter
from dataclasses import dataclass
import inspect
import json
import os
from pathlib import Path
import re
from typing import Callable, Iterable
import unicodedata


_GRANDFATHERED_DUPLICATES = {"r3_bust_cache_after_write": 2}
_PACKET_TEST_ID_PATTERN = r"wp[1-9][0-9]*_[a-z0-9]+(?:_[a-z0-9]+)*"
_LEGACY_TEST_ID_PATTERN = r"r[1-9][0-9]{0,3}[a-z]?_[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*"
_FRAGMENT_NAME_RE = re.compile(_PACKET_TEST_ID_PATTERN + r"[.]py\Z")
_TEST_ID_RE = re.compile(_PACKET_TEST_ID_PATTERN + r"\Z")
_LEGACY_TEST_ID_RE = re.compile(_LEGACY_TEST_ID_PATTERN + r"\Z")
_TEST_ID_POINTER_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:" + _LEGACY_TEST_ID_PATTERN + "|" + _PACKET_TEST_ID_PATTERN
    + r")(?![A-Za-z0-9_])")
_BUNDLED_MODULE_NAME = "tl_test_fragments_bundled.py"
_BUNDLED_RELATIVE_PATH = f"scripts/{_BUNDLED_MODULE_NAME}"


class FragmentError(RuntimeError):
    """Base class for diagnosable fragment discovery/load failures."""

    def __init__(self, code: str, fragment: str = "", detail: str = ""):
        self.code = code
        self.fragment = fragment
        self.detail = detail
        message = ":".join(part for part in (code, fragment, detail) if part)
        super().__init__(message)


class FragmentPathError(FragmentError):
    """A candidate path escaped or violated fragment topology."""


class FragmentSyntaxError(FragmentError):
    """A fragment could not be decoded or compiled."""


class FragmentReadError(FragmentError):
    """A validated fragment path could not be read."""


class FragmentImportError(FragmentError):
    """Top-level fragment execution failed."""


class FragmentExecutionError(FragmentError):
    """A loaded fragment case failed while the harness evaluated it."""


class FragmentContractError(FragmentError):
    """A loaded fragment did not satisfy the TEST_ID/run interface."""


class FragmentDuplicateError(FragmentError):
    """A fragment path or test ID collided with an existing registration."""


@dataclass(frozen=True)
class FragmentCase:
    """One loaded fragment case at the ``tl_selftest`` adapter seam."""

    test_id: str
    run: Callable[[object], object]
    source_path: Path


@dataclass(frozen=True)
class TestIdEntry:
    """One resolvable test registration in the shared namespace."""

    test_id: str
    kind: str
    source_path: Path | None = None


@dataclass(frozen=True)
class TestIdIndex:
    """Deterministic resolver for legacy and packet-owned test IDs."""

    entries: tuple[TestIdEntry, ...]

    def resolve(self, test_id: str) -> TestIdEntry | None:
        if type(test_id) is not str:
            return None
        return next((entry for entry in self.entries if entry.test_id == test_id), None)


def _stable_name(path: Path) -> tuple[str, str]:
    name = unicodedata.normalize("NFC", path.name)
    return name.casefold(), name


def _validate_existing_ids(existing_ids: Iterable[str]) -> set[str]:
    counts = Counter(str(test_id) for test_id in existing_ids)
    for test_id, count in counts.items():
        allowed = _GRANDFATHERED_DUPLICATES.get(test_id, 1)
        if count > allowed:
            raise FragmentDuplicateError("DUPLICATE_TEST_ID", test_id, str(count))
    return set(counts)


def _test_id_kind(test_id: str) -> str | None:
    if _LEGACY_TEST_ID_RE.fullmatch(test_id):
        return "legacy"
    if _TEST_ID_RE.fullmatch(test_id):
        return "packet"
    return None


def _build_test_id_index(existing_ids: Iterable[str],
                         fragment_entries: Iterable[TestIdEntry]) -> TestIdIndex:
    registered = tuple(str(test_id) for test_id in existing_ids)
    fragments = tuple(fragment_entries)
    _validate_existing_ids((*registered, *(fragment.test_id for fragment in fragments)))

    entries: dict[str, TestIdEntry] = {}
    for test_id in registered:
        kind = _test_id_kind(test_id)
        if kind is not None:
            entries.setdefault(test_id, TestIdEntry(test_id=test_id, kind=kind))
    for fragment in fragments:
        if not _TEST_ID_RE.fullmatch(fragment.test_id) or fragment.kind != "packet":
            name = fragment.source_path.name if fragment.source_path else fragment.test_id
            raise FragmentContractError("FRAGMENT_CONTRACT", name)
        entries[fragment.test_id] = fragment
    return TestIdIndex(tuple(sorted(entries.values(), key=lambda entry: entry.test_id)))


def build_test_id_index(existing_ids: Iterable[str],
                        fragment_cases: Iterable[FragmentCase] = ()) -> TestIdIndex:
    """Build the resolver from runtime-validated fragment cases."""
    return _build_test_id_index(existing_ids, (
        TestIdEntry(test_id=fragment.test_id, kind="packet", source_path=fragment.source_path)
        for fragment in fragment_cases))


def find_test_id_pointers(text: str) -> tuple[tuple[str, int], ...]:
    """Return canonical test-ID tokens with offsets from one documentation span."""
    return tuple((match.group(0), match.start()) for match in _TEST_ID_POINTER_RE.finditer(text))


def discover_harness_test_ids(selftest_path: str | Path) -> tuple[str, ...]:
    """Read literal registrations for an existence index of the selftest harness.

    Static source can contain the same ID in mutually exclusive branches. Runtime
    collision enforcement remains in ``load_fragment_cases(existing_ids=...)``.
    """
    path = Path(selftest_path)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
    except OSError as exc:
        raise FragmentReadError("TEST_ID_INDEX_READ", path.name) from exc
    except (SyntaxError, UnicodeError) as exc:
        raise FragmentSyntaxError("TEST_ID_INDEX_SYNTAX", path.name) from exc

    found: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        value = None
        if isinstance(node.func, ast.Name) and node.func.id == "_t110":
            value = node.args[0]
        elif (isinstance(node.func, ast.Attribute) and node.func.attr == "append"
              and isinstance(node.func.value, ast.Name) and node.func.value.id == "cases"
              and isinstance(node.args[0], ast.Tuple) and node.args[0].elts):
            value = node.args[0].elts[0]
        if (isinstance(value, ast.Constant) and type(value.value) is str
                and _test_id_kind(value.value) is not None):
            found.add(value.value)
    return tuple(sorted(found))


def _candidate_path(root: Path, candidate: str | Path) -> Path:
    raw = Path(candidate)
    if ".." in raw.parts:
        raise FragmentPathError("PATH_TRAVERSAL", raw.name or "<path>")
    path = raw if raw.is_absolute() else root / raw
    if path.is_symlink():
        raise FragmentPathError("PATH_TRAVERSAL", path.name, "symlink")
    try:
        resolved = path.resolve(strict=True)
        relative = resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise FragmentPathError("PATH_TRAVERSAL", path.name or "<path>") from exc
    if len(relative.parts) != 1 or not resolved.is_file() or not _FRAGMENT_NAME_RE.fullmatch(resolved.name):
        raise FragmentPathError("INVALID_FRAGMENT_PATH", relative.as_posix())
    return resolved


def _discover_fragment_paths(fragment_root: str | Path, *,
                             candidate_paths: Iterable[str | Path] | None = None) -> tuple[Path, ...]:
    """Validate and order direct-child fragment paths without executing source."""
    root = Path(fragment_root)
    if not root.exists():
        if candidate_paths is not None:
            raise FragmentPathError("INVALID_FRAGMENT_ROOT", "<missing>")
        return ()
    if not root.is_dir():
        raise FragmentPathError("INVALID_FRAGMENT_ROOT", "<not-directory>")
    try:
        root = root.resolve(strict=True)
        raw_candidates = list(root.iterdir()) if candidate_paths is None else list(candidate_paths)
    except OSError as exc:
        raise FragmentPathError("INVALID_FRAGMENT_ROOT", "<unreadable>") from exc
    raw_candidates.sort(key=lambda candidate: _stable_name(Path(candidate)))
    paths = [_candidate_path(root, candidate) for candidate in raw_candidates]
    path_keys = [unicodedata.normalize("NFC", os.path.normcase(str(path))) for path in paths]
    duplicate_paths = [path for path, count in Counter(path_keys).items() if count > 1]
    if duplicate_paths:
        raise FragmentDuplicateError("DUPLICATE_FRAGMENT_PATH", Path(duplicate_paths[0]).name)
    return tuple(sorted(paths, key=_stable_name))


def _compile_fragment_source(path: Path, source: str) -> tuple[str, object, ast.Module]:
    """Normalize and compile one validated source span without executing it."""
    try:
        source = source.replace("\r\n", "\n").replace("\r", "\n")
        tree = ast.parse(source, filename=path.name)
        code = compile(tree, path.name, "exec", dont_inherit=True)
    except (SyntaxError, UnicodeError) as exc:
        raise FragmentSyntaxError("FRAGMENT_SYNTAX", path.name) from exc
    return source, code, tree


def _read_fragment_source(path: Path) -> tuple[str, object, ast.Module]:
    """Read and compile one fragment without executing it."""
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise FragmentReadError("FRAGMENT_READ", path.name) from exc
    except UnicodeError as exc:
        raise FragmentSyntaxError("FRAGMENT_SYNTAX", path.name) from exc
    return _compile_fragment_source(path, source)


def _literal_fragment_test_id(path: Path, tree: ast.Module) -> str:
    """Apply the one declared-ID contract shared by metadata and runtime paths."""
    values = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "TEST_ID"
                   for target in node.targets):
                values.append(node.value)
        elif (isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
              and node.target.id == "TEST_ID"):
            values.append(node.value)
    if (len(values) != 1 or not isinstance(values[0], ast.Constant)
            or type(values[0].value) is not str or not _TEST_ID_RE.fullmatch(values[0].value)):
        raise FragmentContractError("FRAGMENT_CONTRACT", path.name, "literal TEST_ID")
    test_id = values[0].value
    if test_id != path.stem:
        raise FragmentContractError("PATH_ID_MISMATCH", path.name, test_id)
    return test_id


def _read_fragment_metadata(path: Path) -> tuple[object, str]:
    """Compile source and read literal TEST_ID metadata without executing it."""
    _, code, tree = _read_fragment_source(path)
    return code, _literal_fragment_test_id(path, tree)


def discover_fragment_test_ids(fragment_root: str | Path) -> tuple[TestIdEntry, ...]:
    """Discover fragment IDs for read-only consumers without executing fragment code."""
    entries = []
    for path in _discover_fragment_paths(fragment_root):
        _, test_id = _read_fragment_metadata(path)
        entries.append(TestIdEntry(test_id=test_id, kind="packet", source_path=path))
    return tuple(entries)


def _load_compiled_fragment(path: Path, code: object, tree: ast.Module) -> FragmentCase:
    """Execute one already-compiled fragment through the sole runtime contract."""
    namespace = {"__file__": str(path), "__name__": f"_tl_test_fragment_{path.stem}", "__package__": None}
    try:
        exec(code, namespace)
    except BaseException as exc:
        raise FragmentImportError("FRAGMENT_IMPORT", path.name) from exc

    declared_test_id = _literal_fragment_test_id(path, tree)
    test_id = namespace.get("TEST_ID")
    run = namespace.get("run")
    if type(test_id) is not str or test_id != declared_test_id or not callable(run):
        raise FragmentContractError("FRAGMENT_CONTRACT", path.name)
    try:
        if (inspect.iscoroutinefunction(run) or inspect.isgeneratorfunction(run)
                or inspect.isasyncgenfunction(run)):
            raise TypeError("run(tl_module) must be synchronous")
        inspect.signature(run).bind(object())
    except BaseException as exc:
        raise FragmentContractError(
            "FRAGMENT_CONTRACT", path.name, "run(tl_module)") from exc
    def guarded_run(tl_module: object) -> bool:
        try:
            result = run(tl_module)
            if (inspect.isawaitable(result) or inspect.isgenerator(result)
                    or inspect.isasyncgen(result)):
                if inspect.iscoroutine(result) or inspect.isgenerator(result):
                    result.close()
                detail = f"deferred-result:{type(result).__name__}"
                raise FragmentExecutionError("FRAGMENT_EXECUTION", path.name, detail)
            return bool(result)
        except FragmentExecutionError:
            raise
        except BaseException as exc:
            raise FragmentExecutionError("FRAGMENT_EXECUTION", path.name) from exc

    return FragmentCase(test_id=test_id, run=guarded_run, source_path=path)


def _load_one(path: Path) -> FragmentCase:
    _, code, tree = _read_fragment_source(path)
    return _load_compiled_fragment(path, code, tree)


def load_fragment_cases(fragment_root: str | Path, *, existing_ids: Iterable[str] = (),
                        candidate_paths: Iterable[str | Path] | None = None) -> tuple[FragmentCase, ...]:
    """Discover and load fragment cases in locale-independent filename order.

    ``candidate_paths`` is the explicit discovery adapter used by generator
    and path-negative tests; every entry remains constrained to a direct
    child of ``fragment_root``.
    """
    existing = _validate_existing_ids(existing_ids)
    loaded: list[FragmentCase] = []
    seen = set(existing)
    paths = _discover_fragment_paths(fragment_root, candidate_paths=candidate_paths)
    for path in paths:
        fragment = _load_one(path)
        if fragment.test_id in seen:
            raise FragmentDuplicateError("DUPLICATE_TEST_ID", fragment.test_id, "2")
        seen.add(fragment.test_id)
        loaded.append(fragment)
    return tuple(loaded)


def _read_bundled_sources(bundled_path: str | Path) -> tuple[tuple[str, str], ...]:
    """Read the generated data-only adapter without importing or executing it."""
    path = Path(bundled_path)
    if not path.is_file():
        raise FragmentReadError("BUNDLED_MODULE_MISSING", _BUNDLED_RELATIVE_PATH)
    try:
        source = path.read_text(encoding="utf-8")
        source = source.replace("\r\n", "\n").replace("\r", "\n")
        tree = ast.parse(source, filename=path.name)
    except OSError as exc:
        raise FragmentReadError("BUNDLED_MODULE_READ", _BUNDLED_RELATIVE_PATH) from exc
    except (SyntaxError, UnicodeError) as exc:
        raise FragmentSyntaxError("BUNDLED_MODULE_SYNTAX", _BUNDLED_RELATIVE_PATH) from exc

    body = list(tree.body)
    if (body and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and type(body[0].value.value) is str):
        body.pop(0)
    assignment = body[0] if len(body) == 1 else None
    if (not isinstance(assignment, ast.Assign) or len(assignment.targets) != 1
            or not isinstance(assignment.targets[0], ast.Name)
            or assignment.targets[0].id != "BUNDLED_FRAGMENT_SOURCES"):
        raise FragmentContractError(
            "BUNDLED_MODULE_CONTRACT", _BUNDLED_RELATIVE_PATH, "data-only assignment")
    try:
        raw_entries = ast.literal_eval(assignment.value)
    except (SyntaxError, TypeError, ValueError) as exc:
        raise FragmentContractError(
            "BUNDLED_MODULE_CONTRACT", _BUNDLED_RELATIVE_PATH, "literal sources") from exc
    if type(raw_entries) is not tuple:
        raise FragmentContractError(
            "BUNDLED_MODULE_CONTRACT", _BUNDLED_RELATIVE_PATH, "sources tuple")

    entries: list[tuple[str, str]] = []
    for item in raw_entries:
        if (type(item) is not tuple or len(item) != 2
                or type(item[0]) is not str or type(item[1]) is not str
                or not _FRAGMENT_NAME_RE.fullmatch(item[0])):
            raise FragmentContractError(
                "BUNDLED_MODULE_CONTRACT", _BUNDLED_RELATIVE_PATH, "source entry")
        entries.append(item)
    names = [name for name, _ in entries]
    portable_keys = [unicodedata.normalize("NFC", name).casefold() for name in names]
    if (len(set(portable_keys)) != len(portable_keys)
            or names != sorted(names, key=lambda name: _stable_name(Path(name)))):
        raise FragmentContractError(
            "BUNDLED_MODULE_CONTRACT", _BUNDLED_RELATIVE_PATH, "source order")
    return tuple(entries)


def _compile_bundled_entries(
        bundled_path: str | Path) -> tuple[tuple[Path, object, ast.Module], ...]:
    """Compile every generated source once through the shared fragment contract."""
    path = Path(bundled_path)
    entries = []
    for name, source in _read_bundled_sources(path):
        virtual_path = path.parent / "test_fragments" / name
        _, code, tree = _compile_fragment_source(virtual_path, source)
        entries.append((virtual_path, code, tree))
    return tuple(entries)


def discover_bundled_test_ids(bundled_path: str | Path) -> tuple[TestIdEntry, ...]:
    """Index generated sources without executing packet fragment code."""
    entries = []
    for virtual_path, _, tree in _compile_bundled_entries(bundled_path):
        test_id = _literal_fragment_test_id(virtual_path, tree)
        entries.append(TestIdEntry(
            test_id=test_id, kind="packet", source_path=virtual_path))
    return tuple(entries)


def load_bundled_fragment_cases(bundled_path: str | Path, *,
                                existing_ids: Iterable[str] = ()) -> tuple[FragmentCase, ...]:
    """Load generated sources through the same contract as dev fragments."""
    seen = _validate_existing_ids(existing_ids)
    loaded = []
    for virtual_path, code, tree in _compile_bundled_entries(bundled_path):
        fragment = _load_compiled_fragment(virtual_path, code, tree)
        if fragment.test_id in seen:
            raise FragmentDuplicateError("DUPLICATE_TEST_ID", fragment.test_id, "2")
        seen.add(fragment.test_id)
        loaded.append(fragment)
    return tuple(loaded)


def _runtime_fragment_topology(scripts_root: str | Path) -> tuple[str, Path | None]:
    """Select the sole active source without losing bundle cases to an empty dev root."""
    scripts = Path(scripts_root)
    fragment_root = scripts / "test_fragments"
    if fragment_root.exists() and _discover_fragment_paths(fragment_root):
        return "dev", fragment_root
    bundled_path = scripts / _BUNDLED_MODULE_NAME
    if bundled_path.exists():
        return "bundle", bundled_path
    return "none", None


def load_runtime_fragment_cases(scripts_root: str | Path, *,
                                existing_ids: Iterable[str] = ()) -> tuple[FragmentCase, ...]:
    """Prefer auditable dev fragments; fall back to the release bundled adapter."""
    topology, path = _runtime_fragment_topology(scripts_root)
    if path is None:
        return ()
    if topology == "dev":
        return load_fragment_cases(path, existing_ids=existing_ids)
    if topology == "bundle":
        return load_bundled_fragment_cases(path, existing_ids=existing_ids)
    return ()


def generate_bundled_module_bytes(fragment_root: str | Path, *,
                                  candidate_paths: Iterable[str | Path] | None = None) -> bytes:
    """Render validated fragment sources as a deterministic data-only module."""
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Generated by tl_core.test_fragments; do not edit."""',
        "",
        "BUNDLED_FRAGMENT_SOURCES = (",
    ]
    for path in _discover_fragment_paths(fragment_root, candidate_paths=candidate_paths):
        source, _, tree = _read_fragment_source(path)
        _literal_fragment_test_id(path, tree)
        name_literal = json.dumps(path.name, ensure_ascii=False)
        source_literal = json.dumps(source, ensure_ascii=False)
        lines.append(f"    ({name_literal}, {source_literal}),")
    lines.append(")")
    return ("\n".join(lines) + "\n").encode("utf-8")


def load_test_id_index(repo_root: str | Path) -> TestIdIndex:
    """Load the shared index without executing packet fragment code."""
    root = Path(repo_root)
    registered = discover_harness_test_ids(root / "scripts" / "tl_selftest.py")
    topology, path = _runtime_fragment_topology(root / "scripts")
    if path is None:
        return _build_test_id_index(registered, ())
    if topology == "dev":
        fragments = discover_fragment_test_ids(path)
    elif topology == "bundle":
        fragments = discover_bundled_test_ids(path)
    else:
        fragments = ()
    return _build_test_id_index(registered, fragments)
