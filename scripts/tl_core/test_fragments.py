# -*- coding: utf-8 -*-
"""Deterministic discovery/loading for packet-owned selftest fragments.

The public CLI remains ``scripts/tl.py --selftest``.  This deep internal
module owns filesystem ordering and the fragment contract; ``tl_selftest`` is
only the adapter that evaluates returned cases.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import inspect
import os
from pathlib import Path
import re
from typing import Callable, Iterable
import unicodedata


_GRANDFATHERED_DUPLICATES = {"r3_bust_cache_after_write": 2}
_FRAGMENT_NAME_RE = re.compile(r"wp[1-9][0-9]*_[a-z0-9]+(?:_[a-z0-9]+)*[.]py\Z")
_TEST_ID_RE = re.compile(r"wp[1-9][0-9]*_[a-z0-9]+(?:_[a-z0-9]+)*\Z")


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


def _load_one(path: Path) -> FragmentCase:
    try:
        source = path.read_text(encoding="utf-8")
        code = compile(source, path.name, "exec", dont_inherit=True)
    except OSError as exc:
        raise FragmentReadError("FRAGMENT_READ", path.name, type(exc).__name__) from exc
    except (SyntaxError, UnicodeError) as exc:
        raise FragmentSyntaxError("FRAGMENT_SYNTAX", path.name, type(exc).__name__) from exc

    namespace = {"__file__": str(path), "__name__": f"_tl_test_fragment_{path.stem}", "__package__": None}
    try:
        exec(code, namespace)
    except BaseException as exc:
        raise FragmentImportError("FRAGMENT_IMPORT", path.name) from exc

    test_id = namespace.get("TEST_ID")
    run = namespace.get("run")
    if type(test_id) is not str or not _TEST_ID_RE.fullmatch(test_id) or not callable(run):
        raise FragmentContractError("FRAGMENT_CONTRACT", path.name)
    try:
        if (inspect.iscoroutinefunction(run) or inspect.isgeneratorfunction(run)
                or inspect.isasyncgenfunction(run)):
            raise TypeError("run(tl_module) must be synchronous")
        inspect.signature(run).bind(object())
    except BaseException as exc:
        raise FragmentContractError(
            "FRAGMENT_CONTRACT", path.name, "run(tl_module)") from exc
    if test_id != path.stem:
        raise FragmentContractError("PATH_ID_MISMATCH", path.name, test_id)

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


def load_fragment_cases(fragment_root: str | Path, *, existing_ids: Iterable[str] = (),
                        candidate_paths: Iterable[str | Path] | None = None) -> tuple[FragmentCase, ...]:
    """Discover and load fragment cases in locale-independent filename order.

    ``candidate_paths`` is the explicit discovery adapter used by generator
    and path-negative tests; every entry remains constrained to a direct
    child of ``fragment_root``.
    """
    root = Path(fragment_root)
    existing = _validate_existing_ids(existing_ids)
    if not root.exists():
        if candidate_paths is not None:
            raise FragmentPathError("INVALID_FRAGMENT_ROOT", "<missing>")
        return ()
    if not root.is_dir():
        raise FragmentPathError("INVALID_FRAGMENT_ROOT", "<not-directory>")
    try:
        root = root.resolve(strict=True)
    except OSError as exc:
        raise FragmentPathError("INVALID_FRAGMENT_ROOT", "<unresolvable>") from exc

    loaded: list[FragmentCase] = []
    seen = set(existing)
    raw_candidates = list(root.iterdir()) if candidate_paths is None else list(candidate_paths)
    raw_candidates.sort(key=lambda candidate: _stable_name(Path(candidate)))
    paths = [_candidate_path(root, candidate) for candidate in raw_candidates]
    path_keys = [unicodedata.normalize("NFC", os.path.normcase(str(path))) for path in paths]
    duplicate_paths = [path for path, count in Counter(path_keys).items() if count > 1]
    if duplicate_paths:
        raise FragmentDuplicateError("DUPLICATE_FRAGMENT_PATH", Path(duplicate_paths[0]).name)

    for path in sorted(paths, key=_stable_name):
        fragment = _load_one(path)
        if fragment.test_id in seen:
            raise FragmentDuplicateError("DUPLICATE_TEST_ID", fragment.test_id, "2")
        seen.add(fragment.test_id)
        loaded.append(fragment)
    return tuple(loaded)
