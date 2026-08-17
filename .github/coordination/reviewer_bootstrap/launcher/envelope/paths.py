"""External path admission for the launch envelope.

Every path that reaches the argument vector, the working directory or a `PATH`-like environment
value passes through here first.  The checks are split in two halves on purpose:

  * `check_path_text` is pure text and runs on BOTH platform spellings.  A Windows device name,
    an alternate data stream or a UNC share must reject with its own named category when the
    suite runs on POSIX too, otherwise "hostile spellings are rejected" would only be true on the
    machine that happened to run the gate.
  * `inspect_*` is filesystem identity: symlink, reparse point, hard link, write bits, regular
    file, directory.  These need a real `lstat` and are never inferred from the string.

The order inside `check_path_text` is load-bearing: the absolute-path test runs LAST, because a
hostile spelling that is also non-absolute must still report the hostile category rather than the
bland one.
"""

from __future__ import annotations

import os
import pathlib
import re
import stat

from oracle.safe_io import require_outside_tree

from .errors import reject

MAX_PATH_CHARACTERS = 4096

# The candidate checkout is derived from this file, never from a caller argument.  A trusted root
# that the caller may choose is not a boundary: it is a knob that turns the boundary off.
HERE = pathlib.Path(__file__).resolve().parent
CANDIDATE_ROOT = HERE.parents[4]

_DRIVE_PREFIX = re.compile(r"[A-Za-z]:")
_SEPARATORS = re.compile(r"[\\/]+")
_CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f]")
_UNC_OR_DEVICE_PREFIX = ("\\\\", "//", "\\/", "/\\")

# Win32 keeps these names reserved in every directory, and `NUL` in particular swallows writes
# without failing.  A launcher that accepts one of them as a config path reports success while
# nothing was ever configured.
_RESERVED_DEVICE_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$", "CLOCK$"}
    | {"COM%d" % index for index in range(1, 10)}
    | {"LPT%d" % index for index in range(1, 10)}
)

_FILE_ATTRIBUTE_REPARSE_POINT = 0x400


def _segments(value: str) -> list[str]:
    """Path segments under both separator conventions, with a trailing separator forgiven.

    A trailing separator is a legal spelling of the same directory, so it must normalise instead
    of rejecting; an interior `..` must reject even when written with the other platform's slash.
    """

    stripped = value.rstrip("\\/")
    if not stripped or _DRIVE_PREFIX.fullmatch(stripped):
        stripped = value
    parts = _SEPARATORS.split(stripped)
    if parts and parts[0] == "":
        parts = parts[1:]
    return parts


def check_path_text(value: object, label: str) -> str:
    """Reject hostile spellings by named category before any filesystem call."""

    if not isinstance(value, str):
        raise reject("path_not_string", "%s must be a string path" % label)
    if not value:
        raise reject("path_empty", "%s must not be empty" % label)
    if len(value) > MAX_PATH_CHARACTERS:
        raise reject("path_oversized_text", "%s exceeds the path length limit" % label)
    if _CONTROL_CHARACTERS.search(value) is not None:
        raise reject("path_control_character", "%s contains a control character" % label)
    if value.startswith("-"):
        # An argument vector element that begins with a dash is an option, whatever the caller
        # meant it to be.  Rejecting the spelling is cheaper than proving no consumer parses it.
        raise reject("path_option_smuggling", "%s must not begin with an option dash" % label)
    if value.startswith(_UNC_OR_DEVICE_PREFIX):
        raise reject("path_unc_or_device_namespace", "%s uses a UNC or device namespace" % label)

    remainder = value[2:] if _DRIVE_PREFIX.match(value) else value
    if ":" in remainder:
        raise reject("path_alternate_data_stream", "%s carries a stream or drive suffix" % label)

    for segment in _segments(value):
        if segment == "..":
            raise reject("path_traversal", "%s contains a traversal segment" % label)
        if segment == ".":
            raise reject("path_traversal", "%s contains a current-directory segment" % label)
        if segment.split(".")[0].upper() in _RESERVED_DEVICE_NAMES:
            raise reject("path_reserved_device", "%s names a reserved device" % label)

    if not pathlib.PurePath(value).is_absolute():
        raise reject("path_not_absolute", "%s must be an absolute path" % label)
    return value


def _reject_linked_ancestors(target: pathlib.Path, label: str) -> None:
    """A symlinked or reparsed parent relocates the whole sealed directory in one move.

    Checking only the final component would leave that move invisible, so every existing ancestor
    is inspected as well.
    """

    for ancestor in target.parents:
        try:
            info = ancestor.lstat()
        except OSError:
            continue
        if stat.S_ISLNK(info.st_mode):
            raise reject("path_symlink_ancestor", "%s has a symlinked parent directory" % label)
        if getattr(info, "st_file_attributes", 0) & _FILE_ATTRIBUTE_REPARSE_POINT:
            raise reject("path_reparse_ancestor", "%s has a reparse-point parent" % label)


def admit_external_path(value: object, label: str) -> pathlib.Path:
    """Text checks, candidate-tree exclusion and ancestor identity, in that order.

    The returned path is NORMALISED but not link-resolved.  Resolving first would be the quiet
    end of symlink control: `resolve()` on a symlink hands back its target, so the `lstat` that
    was supposed to see a link sees a perfectly ordinary regular file instead.  The candidate-tree
    check below still runs against the resolved form — there a link must not become a way in.
    """

    text = check_path_text(value, label)
    declared = pathlib.Path(os.path.normpath(text))
    require_outside_tree(
        declared,
        CANDIDATE_ROOT,
        label,
        lambda _message: reject(
            "path_inside_candidate", "%s must live outside the candidate checkout" % label
        ),
    )
    _reject_linked_ancestors(declared, label)
    return declared


def _identity(target: pathlib.Path, label: str):
    try:
        info = target.lstat()
    except OSError as exc:
        raise reject("path_missing", "%s cannot be inspected" % label) from exc
    if stat.S_ISLNK(info.st_mode):
        raise reject("path_symlink", "%s must not be a symlink" % label)
    if getattr(info, "st_file_attributes", 0) & _FILE_ATTRIBUTE_REPARSE_POINT:
        raise reject("path_reparse_point", "%s must not be a reparse point" % label)
    return info


def inspect_sealed_file(target: pathlib.Path, label: str, *, max_bytes: int):
    """Regular, read-only, single-link and bounded, measured on the real filesystem."""

    info = _identity(target, label)
    if not stat.S_ISREG(info.st_mode):
        raise reject("path_not_regular", "%s must be a regular file" % label)
    if info.st_nlink != 1:
        raise reject("path_hardlink", "%s must have exactly one hard link" % label)
    if info.st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH):
        raise reject("path_writable", "%s must be sealed read-only" % label)
    if info.st_size > max_bytes:
        raise reject("path_oversized", "%s exceeds its byte limit" % label)
    return info


def inspect_directory(target: pathlib.Path, label: str):
    """A working directory is a real directory, not a link to one."""

    info = _identity(target, label)
    if not stat.S_ISDIR(info.st_mode):
        raise reject("path_not_directory", "%s must be a directory" % label)
    return info
