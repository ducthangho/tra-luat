"""Validation for the sealed, read-only Dispatcher authority bundle.

No Mission, Packet, generation, commit, or hash value is compiled into this
module.  The caller supplies independently measured observations; the sealed
bundle supplies the expected durable authority.  Equality is checked at every
leaf before any oracle evaluation starts.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import stat
from typing import Mapping

OID40 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class AuthorityError(RuntimeError):
    """The sealed bundle is malformed, mutable, stale, or mismatched."""


def _read_sealed(path: pathlib.Path) -> bytes:
    try:
        before = path.lstat()
    except OSError as exc:
        raise AuthorityError("authority bundle cannot be inspected: %s" % exc) from exc
    if not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(before.st_mode):
        raise AuthorityError("authority bundle must be a regular non-symlink file")
    if before.st_nlink != 1:
        raise AuthorityError("authority bundle must have exactly one hard link")
    if before.st_mode & 0o222:
        raise AuthorityError("authority bundle must be sealed read-only")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as handle:
            opened = os.fstat(handle.fileno())
            if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                raise AuthorityError("authority bundle changed identity while opening")
            return handle.read()
    except AuthorityError:
        raise
    except OSError as exc:
        raise AuthorityError("authority bundle cannot be read safely: %s" % exc) from exc


def _walk_differences(expected: object, actual: object, path: str = "") -> list[str]:
    if isinstance(expected, Mapping) and isinstance(actual, Mapping):
        differences = []
        expected_keys = set(expected)
        actual_keys = set(actual)
        for key in sorted(expected_keys - actual_keys, key=str):
            differences.append((path + "." if path else "") + str(key) + " missing")
        for key in sorted(actual_keys - expected_keys, key=str):
            differences.append((path + "." if path else "") + str(key) + " unexpected")
        for key in sorted(expected_keys & actual_keys, key=str):
            child = (path + "." if path else "") + str(key)
            differences.extend(_walk_differences(expected[key], actual[key], child))
        return differences
    if type(expected) is not type(actual) or expected != actual:
        return [path + " changed"]
    return []


def _require_hashes(value: object, path: str = "") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = (path + "." if path else "") + str(key)
            if key in ("head", "tree", "commit_sha", "file_git_oid"):
                if not isinstance(child, str) or not OID40.fullmatch(child):
                    raise AuthorityError("%s must be an exact lowercase 40-hex Git oid" % child_path)
            if str(key).endswith("sha256") or key in ("plan_hash", "spec_hash"):
                if not isinstance(child, str) or not SHA256.fullmatch(child):
                    raise AuthorityError("%s must be an exact lowercase SHA-256" % child_path)
            _require_hashes(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _require_hashes(child, "%s[%d]" % (path, index))


def load_and_verify(path: pathlib.Path | str, observations: Mapping[str, object]) -> dict[str, object]:
    raw = _read_sealed(pathlib.Path(path))
    try:
        bundle = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise AuthorityError("authority bundle is not strict UTF-8 JSON: %s" % exc) from exc
    if not isinstance(bundle, dict) or bundle.get("schema_version") != 1:
        raise AuthorityError("authority bundle must be a schema_version 1 object")
    actual = dict(bundle)
    actual.pop("schema_version", None)
    expected = dict(observations)
    differences = _walk_differences(expected, actual)
    if differences:
        raise AuthorityError("authority mismatch: %s" % ", ".join(differences))
    _require_hashes(actual)
    return bundle
