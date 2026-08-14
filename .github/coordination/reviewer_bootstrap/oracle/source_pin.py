"""Pre-import validation of the Dispatcher-pinned trusted source checkout.

Tệp này là BOOTSTRAP: nó chạy trước khi bất kỳ module ứng viên nào được import,
nên nó cố ý KHÔNG import `oracle.safe_io` hay `oracle.trusted_inventory` ở mức
module — bản sao ngoài do Dispatcher đặt phải chạy được một mình.  Hai hằng bị
lặp lại vì lý do đó (`TRUSTED_PREFIXES`, gốc bootstrap) được ĐỐI CHIẾU với bản
khai báo duy nhất trong `trusted_inventory.py` ngay trong `verify()`, sau khi
từng byte của cây tin cậy đã được đối chiếu với blob Git của commit đã ghim.
"""

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

REVIEWER_BOOTSTRAP_ROOT = ".github/coordination/reviewer_bootstrap"
SOURCE_PIN_RELATIVE = REVIEWER_BOOTSTRAP_ROOT + "/oracle/source_pin.py"
TRUSTED_INVENTORY_RELATIVE = REVIEWER_BOOTSTRAP_ROOT + "/oracle/trusted_inventory.py"
PINNED_CORPUS_RELATIVE = REVIEWER_BOOTSTRAP_ROOT + "/oracle/corpus.json"
TRUSTED_PREFIXES = (
    REVIEWER_BOOTSTRAP_ROOT + "/oracle/",
    REVIEWER_BOOTSTRAP_ROOT + "/sandbox/",
)
OID40 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
AUTHORITY_FLOOR_KEYS = (
    "mission_issue",
    "mission_revision_min",
    "packet_issue",
    "packet_revision_min",
    "packet_generation_min",
)
TARGET_PIN_KEYS = ("ref", "head", "tree", "schema_inventory_sha256")


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
            # Chen symlink giữa lstat và open là ca TOCTOU kinh điển; chỉ so
            # (dev, ino) trên chính descriptor đang giữ mới bắt được.
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


def _positive_int(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise _fail("%s must be a positive integer" % label)
    return value


def pin_blocks(pin_path: str) -> dict[str, object]:
    """Đọc hai khối Dispatcher mà oracle bắt buộc phải có: target và sàn authority.

    Sàn authority KHÔNG được do ứng viên viết — thiếu nó thì §4.2 chỉ còn là so
    sánh tương đối giữa hai tệp cùng nguồn (R3 của verdict 5297249899).
    """
    pin = _load_pin(pathlib.Path(pin_path))
    target = pin.get("target")
    if not isinstance(target, dict) or set(target) != set(TARGET_PIN_KEYS):
        raise _fail("Dispatcher pin target block must contain exactly %s" % list(TARGET_PIN_KEYS))
    if not isinstance(target["ref"], str) or not target["ref"]:
        raise _fail("Dispatcher pin target.ref must be a non-empty ref name")
    for key in ("head", "tree"):
        if not isinstance(target[key], str) or not OID40.fullmatch(target[key]):
            raise _fail("Dispatcher pin target.%s must be an exact lowercase 40-hex Git oid" % key)
    if not isinstance(target["schema_inventory_sha256"], str) or not SHA256.fullmatch(
        target["schema_inventory_sha256"]
    ):
        raise _fail("Dispatcher pin target.schema_inventory_sha256 must be an exact lowercase SHA-256")
    floor = pin.get("authority_floor")
    if not isinstance(floor, dict) or set(floor) != set(AUTHORITY_FLOOR_KEYS):
        raise _fail("Dispatcher pin authority_floor must contain exactly %s" % list(AUTHORITY_FLOOR_KEYS))
    for key in AUTHORITY_FLOOR_KEYS:
        _positive_int(floor[key], "authority_floor.%s" % key)
    return {"target": dict(target), "authority_floor": dict(floor)}


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


def _pinned_inventory_namespace(root: pathlib.Path) -> dict[str, object]:
    inventory_path = root / pathlib.PurePosixPath(TRUSTED_INVENTORY_RELATIVE)
    namespace: dict[str, object] = {}
    exec(
        compile(
            _read_regular_single_link(inventory_path, TRUSTED_INVENTORY_RELATIVE),
            str(inventory_path),
            "exec",
        ),
        namespace,
    )
    return namespace


def verify(repo_root: str, candidate_head: str, pin_path: str) -> dict[str, object]:
    root = pathlib.Path(repo_root).resolve()
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

    # Đến đây từng byte của cây tin cậy đã khớp blob Git của commit đã ghim VÀ
    # digest kiểm kê đã khớp pin, nên exec bản khai báo là exec trên byte đã kiểm.
    namespace = _pinned_inventory_namespace(root)
    declared = tuple(namespace.get("TRUSTED_SOURCE_PATHS", ()))
    if tuple(paths_value) != declared:
        raise _fail("Dispatcher path list does not equal the pinned trusted inventory declaration")
    declared_prefixes = tuple(namespace.get("TRUSTED_PREFIXES", ()))
    if declared_prefixes != TRUSTED_PREFIXES:
        raise _fail(
            "bootstrap prefix fence and pinned inventory declaration disagree: bootstrap=%s declared=%s"
            % (list(TRUSTED_PREFIXES), list(declared_prefixes))
        )
    return measured


def _output(value: dict[str, object]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def _candidate_bootstrap_parent(repo_root: str) -> pathlib.Path:
    return pathlib.Path(repo_root).resolve() / pathlib.PurePosixPath(REVIEWER_BOOTSTRAP_ROOT)


def _require_external_bootstrap(repo_root: str) -> None:
    candidate_copy = (
        pathlib.Path(repo_root).resolve() / pathlib.PurePosixPath(SOURCE_PIN_RELATIVE)
    ).resolve()
    if pathlib.Path(__file__).resolve() == candidate_copy:
        raise _fail("oracle and sandbox execution require an external Dispatcher-pinned bootstrap")


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
    # Corpus mặc định là bản đã ghim TRONG cây tin cậy; cờ này chỉ cho phép trỏ
    # tới một BẢN SAO, và bản sao phải trùng byte, không được là corpus riêng.
    run_parser.add_argument("--corpus")
    run_parser.add_argument("--sandbox-report", required=True)
    run_parser.add_argument("--output-root", required=True)
    sandbox_parser = sub.add_parser("run-sandbox")
    sandbox_parser.add_argument("--repo-root", required=True)
    sandbox_parser.add_argument("--candidate-head", required=True)
    sandbox_parser.add_argument("--pin", required=True)
    sandbox_parser.add_argument("--repeat", type=int, default=1)
    sandbox_parser.add_argument("--output")
    args = parser.parse_args(argv)
    blocks: dict[str, object] = {}
    try:
        if args.command in ("run-oracle", "run-sandbox"):
            _require_external_bootstrap(args.repo_root)
        if args.command in ("verify", "run-oracle", "run-sandbox"):
            result = verify(args.repo_root, args.candidate_head, args.pin)
        else:
            paths = json.loads(args.paths_json)
            if not isinstance(paths, list):
                raise _fail("paths-json must decode to a list")
            result = measure(args.repo_root, args.candidate_head, paths)
        if args.command == "run-oracle":
            blocks = pin_blocks(args.pin)
    except SourcePinError as exc:
        _output({"schema_version": 1, "ok": False, "error": {"name": "SourcePinError", "message": str(exc)}})
        return 2
    candidate_parent = _candidate_bootstrap_parent(args.repo_root)
    if args.command in ("run-oracle", "run-sandbox") and str(candidate_parent) not in sys.path:
        sys.path.insert(0, str(candidate_parent))
    if args.command == "run-oracle":
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
                target_pin=blocks["target"],
                authority_floor=blocks["authority_floor"],
            )
        except Exception as exc:  # noqa: BLE001
            # §6.2 đòi BÁO CÁO ĐỎ CÓ CẤU TRÚC, không phải traceback trần: một
            # `TypeError` lọt ra ngoài từng cho rc=1 với stdout RỖNG (R4).
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
    if args.command == "run-sandbox":
        os.environ["RA02_SOURCE_PIN_VERIFIED"] = "1"
        os.environ["RA02_BOOTSTRAP_PATH"] = str(pathlib.Path(__file__).resolve())
        from sandbox import selftest

        sandbox_argv = [
            "--full",
            "--repo-root",
            args.repo_root,
            "--candidate-head",
            args.candidate_head,
            "--dispatcher-pin",
            args.pin,
            "--repeat",
            str(args.repeat),
        ]
        if args.output:
            sandbox_argv.extend(("--output", args.output))
        return selftest.main(sandbox_argv)
    _output({"schema_version": 1, "ok": True, "source_binding": result})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
