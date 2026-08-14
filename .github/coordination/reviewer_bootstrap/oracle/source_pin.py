"""Pre-import validation of the Dispatcher-pinned trusted source checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import stat
import subprocess
import sys
from typing import Sequence

SOURCE_PIN_RELATIVE = ".github/coordination/reviewer_bootstrap/oracle/source_pin.py"
TRUSTED_INVENTORY_RELATIVE = (
    ".github/coordination/reviewer_bootstrap/oracle/trusted_inventory.py"
)
TRUSTED_PREFIXES = (
    ".github/coordination/reviewer_bootstrap/oracle/",
    ".github/coordination/reviewer_bootstrap/sandbox/",
)
OID40 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class SourcePinError(RuntimeError):
    """The checkout cannot be bound to the external Dispatcher pin."""


def _fail(message: str) -> SourcePinError:
    return SourcePinError(message)


def _git(root: pathlib.Path, *args: str, binary: bool = False):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
    )
    if proc.returncode != 0:
        stderr = proc.stderr if isinstance(proc.stderr, str) else proc.stderr.decode("utf-8", "replace")
        raise _fail("git %s failed rc=%d: %s" % (" ".join(args), proc.returncode, stderr.strip()))
    return proc.stdout


def _read_regular_single_link(path: pathlib.Path, label: str) -> bytes:
    try:
        before = path.lstat()
    except OSError as exc:
        raise _fail("%s cannot be inspected: %s" % (label, exc)) from exc
    if not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(before.st_mode):
        raise _fail("%s is not a regular non-symlink file" % label)
    if before.st_nlink != 1:
        raise _fail("%s must have exactly one hard link" % label)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as handle:
            opened = os.fstat(handle.fileno())
            if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
                raise _fail("%s changed identity while opening" % label)
            return handle.read()
    except SourcePinError:
        raise
    except OSError as exc:
        raise _fail("%s cannot be read safely: %s" % (label, exc)) from exc


def _safe_relative(value: object) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise _fail("trusted source path must be a non-empty POSIX relative path")
    pure = pathlib.PurePosixPath(value)
    if pure.is_absolute() or any(part in ("", ".", "..") for part in pure.parts):
        raise _fail("unsafe trusted source path: %s" % value)
    if not any(value.startswith(prefix) for prefix in TRUSTED_PREFIXES):
        raise _fail("trusted source path outside the two RA-02 prefixes: %s" % value)
    return value


def _load_pin(path: pathlib.Path) -> dict[str, object]:
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        raise _fail("Dispatcher pin cannot be inspected: %s" % exc) from exc
    if mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH):
        raise _fail("Dispatcher pin must be sealed read-only")
    raw = _read_regular_single_link(path, "Dispatcher pin")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise _fail("Dispatcher pin is not strict UTF-8 JSON: %s" % exc) from exc
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise _fail("Dispatcher pin must be a schema_version 1 object")
    return value


def _tree_entry(root: pathlib.Path, head: str, relative: str) -> tuple[str, str, str]:
    out = str(_git(root, "ls-tree", head, "--", relative)).strip()
    if not out or "\t" not in out:
        raise _fail("trusted source is absent from the pinned commit: %s" % relative)
    meta, returned = out.split("\t", 1)
    pieces = meta.split()
    if len(pieces) != 3 or returned != relative or pieces[1] != "blob":
        raise _fail("trusted source is not one exact Git blob: %s" % relative)
    return pieces[0], pieces[1], pieces[2]


def measure(repo_root: str, candidate_head: str, source_paths: Sequence[str]) -> dict[str, object]:
    if not OID40.fullmatch(candidate_head):
        raise _fail("candidate_head must be an exact lowercase 40-hex Git oid")
    root = pathlib.Path(repo_root).resolve()
    top = pathlib.Path(str(_git(root, "rev-parse", "--show-toplevel")).strip()).resolve()
    if top != root:
        raise _fail("repo_root is not the exact Git top-level")
    actual_head = str(_git(root, "rev-parse", "HEAD")).strip()
    if actual_head != candidate_head:
        raise _fail("candidate checkout HEAD does not match the declared commit")
    tree = str(_git(root, "rev-parse", candidate_head + "^{tree}")).strip()

    paths = tuple(sorted(_safe_relative(item) for item in source_paths))
    if len(paths) != len(set(paths)) or not paths:
        raise _fail("trusted source inventory must be non-empty and duplicate-free")
    tracked = set()
    for prefix in TRUSTED_PREFIXES:
        output = str(_git(root, "ls-tree", "-r", "--name-only", candidate_head, "--", prefix))
        tracked.update(line for line in output.splitlines() if line)
    if tracked != set(paths):
        raise _fail(
            "trusted source path inventory mismatch: missing=%s extra=%s"
            % (sorted(tracked - set(paths)), sorted(set(paths) - tracked))
        )

    entries = []
    for relative in paths:
        disk = _read_regular_single_link(root / pathlib.PurePosixPath(relative), relative)
        mode, _kind, oid = _tree_entry(root, candidate_head, relative)
        blob = _git(root, "cat-file", "blob", oid, binary=True)
        if disk != blob:
            raise _fail("trusted source bytes differ from the declared Git blob: %s" % relative)
        entries.append(
            {
                "path": relative,
                "mode": mode,
                "git_blob": oid,
                "sha256": hashlib.sha256(disk).hexdigest(),
                "bytes": len(disk),
            }
        )
    payload = {
        "schema_version": 1,
        "candidate_head": candidate_head,
        "candidate_tree": tree,
        "entries": entries,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["trusted_source_inventory_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def verify(repo_root: str, candidate_head: str, pin_path: str) -> dict[str, object]:
    root = pathlib.Path(repo_root).resolve()
    expected_bootstrap = (root / pathlib.PurePosixPath(SOURCE_PIN_RELATIVE)).resolve()
    if pathlib.Path(__file__).resolve() != expected_bootstrap:
        raise _fail("trusted bootstrap is not executing from the candidate checkout")
    pin = _load_pin(pathlib.Path(pin_path))
    paths_value = pin.get("trusted_source_paths")
    if not isinstance(paths_value, list) or not all(isinstance(item, str) for item in paths_value):
        raise _fail("Dispatcher pin trusted_source_paths must be a string list")
    measured = measure(repo_root, candidate_head, paths_value)
    candidate = pin.get("candidate")
    if not isinstance(candidate, dict):
        raise _fail("Dispatcher pin candidate block is missing")
    comparisons = {
        "candidate.head": (candidate.get("head"), candidate_head),
        "candidate.tree": (candidate.get("tree"), measured["candidate_tree"]),
        "trusted_source_inventory_sha256": (
            pin.get("trusted_source_inventory_sha256"),
            measured["trusted_source_inventory_sha256"],
        ),
    }
    changed = [name for name, pair in comparisons.items() if pair[0] != pair[1]]
    if changed:
        raise _fail("Dispatcher source pin mismatch: changed=%s" % changed)

    inventory_path = root / pathlib.PurePosixPath(TRUSTED_INVENTORY_RELATIVE)
    namespace: dict[str, object] = {}
    exec(compile(_read_regular_single_link(inventory_path, TRUSTED_INVENTORY_RELATIVE), str(inventory_path), "exec"), namespace)
    declared = tuple(namespace.get("TRUSTED_SOURCE_PATHS", ()))
    if tuple(paths_value) != declared:
        raise _fail("Dispatcher path list does not equal the pinned trusted inventory declaration")
    return measured


def _output(value: dict[str, object]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("measure", "verify"):
        item = sub.add_parser(name)
        item.add_argument("--repo-root", required=True)
        item.add_argument("--candidate-head", required=True)
        if name == "verify":
            item.add_argument("--pin", required=True)
        else:
            item.add_argument("--paths-json", required=True)
    run_parser = sub.add_parser("run-oracle")
    run_parser.add_argument("--repo-root", required=True)
    run_parser.add_argument("--candidate-head", required=True)
    run_parser.add_argument("--pin", required=True)
    run_parser.add_argument("--durable-facts", required=True)
    run_parser.add_argument("--target-root", required=True)
    run_parser.add_argument("--corpus", required=True)
    run_parser.add_argument("--sandbox-report", required=True)
    run_parser.add_argument("--output-root", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command in ("verify", "run-oracle"):
            result = verify(args.repo_root, args.candidate_head, args.pin)
        else:
            paths = json.loads(args.paths_json)
            if not isinstance(paths, list):
                raise _fail("paths-json must decode to a list")
            result = measure(args.repo_root, args.candidate_head, paths)
    except SourcePinError as exc:
        _output({"schema_version": 1, "ok": False, "error": {"name": "SourcePinError", "message": str(exc)}})
        return 2
    if args.command == "run-oracle":
        if str(PARENT := pathlib.Path(__file__).resolve().parent.parent) not in sys.path:
            sys.path.insert(0, str(PARENT))
        from oracle import oracle

        try:
            report = oracle.evaluate(
                repo_root=args.repo_root,
                candidate_head=args.candidate_head,
                authority_bundle=args.pin,
                durable_facts=args.durable_facts,
                target_root=args.target_root,
                corpus_path=args.corpus,
                sandbox_report=args.sandbox_report,
                output_root=args.output_root,
                source_binding=result,
            )
        except (oracle.OracleError, ValueError, RuntimeError) as exc:
            _output(
                {
                    "schema_version": 1,
                    "ok": False,
                    "error": {"name": type(exc).__name__, "message": str(exc)},
                }
            )
            return 3
        _output(report)
        return 0
    _output({"schema_version": 1, "ok": True, "source_binding": result})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
