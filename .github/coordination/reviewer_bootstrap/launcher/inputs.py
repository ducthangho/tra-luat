"""Sealed, read-only, single-link coordination inputs (Issue 125 §4.2, final paragraph).

The launcher accepts configuration only from files the Dispatcher sealed *outside* the candidate
checkout.  Everything in this module exists to make one sentence true: the code under review cannot
choose the inputs that govern how it is reviewed.

The generic hardening — regular file, exactly one hard link, no symlink, no identity change between
``lstat`` and ``open``, sealed read-only, outside the tree — is RA-02's
:mod:`oracle.safe_io`, reused rather than re-implemented.  RA-02 already paid for the drift that
comes from keeping three private copies of that logic, and a fourth copy here would be the same
mistake with a new file name.

What this module adds is the part RA-02 did not need and Windows does: reparse points, alternate
data streams, DOS device names and traversal in the *path text* itself.  Those are rejected on the
spelling of the path, before any handle is opened, because ``NUL`` and ``config.json:payload`` are
answered by the OS rather than by the filesystem — by the time an ``open`` succeeds, the check has
already been bypassed.
"""

from __future__ import annotations

import json
import os
import pathlib
import stat
from collections.abc import Sequence

from oracle.safe_io import read_regular_single_link, require_outside_tree

from .errors import LauncherRejected, reject

MAX_INPUT_BYTES = 256 * 1024

# Reserved DOS device names.  Windows resolves these regardless of the directory they appear in, and
# regardless of an extension or trailing dots and spaces, so the comparison strips both.
_DOS_DEVICES = frozenset(
    {"CON", "PRN", "AUX", "NUL", "CLOCK$"}
    | {"COM%d" % index for index in range(1, 10)}
    | {"LPT%d" % index for index in range(1, 10)}
)

_FILE_ATTRIBUTE_REPARSE_POINT = 0x400


def _error(message: str) -> LauncherRejected:
    return reject("sealed_input", message)


def _is_dos_device(component: str) -> bool:
    base = component.split(".", 1)[0].rstrip(" .").upper()
    return base in _DOS_DEVICES


def _check_path_text(path_text: str, label: str) -> pathlib.Path:
    """Reject the path on its spelling before touching the filesystem."""
    if not isinstance(path_text, str) or not path_text:
        raise _error("%s must be a non-empty path string" % label)
    if "\x00" in path_text:
        raise _error("%s carries a NUL byte" % label)

    path = pathlib.Path(path_text)
    if not path.is_absolute():
        raise _error("%s must be an absolute path" % label)

    parts = path.parts
    for index, component in enumerate(parts):
        # The first component of an absolute Windows path is the drive or UNC root; its colon is
        # structural, not a stream separator.
        if index == 0:
            continue
        if component in (".", ".."):
            raise _error("%s carries a traversal component" % label)
        if ":" in component:
            raise _error("%s names an alternate data stream" % label)
        if _is_dos_device(component):
            raise _error("%s names a reserved DOS device" % label)
    return path


def _check_not_reparse_point(path: pathlib.Path, label: str) -> None:
    """Windows reparse points are not symlinks and ``S_ISLNK`` does not see all of them.

    A junction (``mklink /J``) has ``FILE_ATTRIBUTE_REPARSE_POINT`` set while still reporting as a
    directory, so a check written only against ``S_ISLNK`` walks straight through one.
    """
    try:
        info = path.lstat()
    except OSError as exc:
        raise _error("%s cannot be inspected: %s" % (label, exc)) from exc
    attributes = getattr(info, "st_file_attributes", 0)
    if attributes & _FILE_ATTRIBUTE_REPARSE_POINT:
        raise _error("%s is a reparse point" % label)
    if stat.S_ISLNK(info.st_mode):
        raise _error("%s is a symbolic link" % label)


def read_sealed_bytes(
    path_text: str,
    label: str,
    *,
    candidate_root: str,
    max_bytes: int = MAX_INPUT_BYTES,
) -> bytes:
    """Read one sealed coordination input, or reject by category."""
    path = _check_path_text(path_text, label)
    require_outside_tree(path, candidate_root, label, _error)
    _check_not_reparse_point(path, label)
    data = read_regular_single_link(path, label, _error, require_readonly=True)
    if len(data) > max_bytes:
        raise _error("%s exceeds the %d byte ceiling" % (label, max_bytes))
    return data


def read_sealed_json(
    path_text: str,
    label: str,
    *,
    candidate_root: str,
    required_keys: Sequence[str] = (),
) -> dict[str, object]:
    """Read and parse one sealed JSON coordination input."""
    data = read_sealed_bytes(path_text, label, candidate_root=candidate_root)
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _error("%s is not valid UTF-8 JSON: %s" % (label, exc)) from exc
    if not isinstance(value, dict):
        raise _error("%s must be a JSON object" % label)
    missing = [key for key in required_keys if key not in value]
    if missing:
        raise _error("%s is missing required keys: %s" % (label, ", ".join(sorted(missing))))
    return value


def seal(path: pathlib.Path, data: bytes) -> None:
    """Write a fixture the way the Dispatcher seals a real one: LF bytes, then read-only.

    Used by the offline controls so that the *positive* cases exercise the same reader as the
    negative ones.  A positive case that bypasses the reader proves nothing about the reader.
    """
    path.write_bytes(data)
    path.chmod(stat.S_IREAD)


def describe(entries: dict[str, str]) -> dict[str, object]:
    """Evidence for the artifact set: which inputs were read and from where.

    Paths are recorded; contents are not.  A sealed input can carry a launch configuration whose
    values are uninteresting and whose size is not, and the artifact set already stores a SHA-256 for
    anything whose bytes matter.
    """
    return {
        "sealed_inputs": [
            {"label": label, "path": os.fspath(path)} for label, path in sorted(entries.items())
        ],
        "reader": "oracle.safe_io.read_regular_single_link",
        "require_readonly": True,
        "require_outside_candidate_tree": True,
    }
