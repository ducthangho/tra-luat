"""Sealed controller inputs: exact bytes, exact digest, and a second look before we commit.

The hardened low-level reader is NOT re-implemented here.  `oracle/safe_io.py` already owns the
`lstat` + `O_NOFOLLOW` + (dev, ino) comparison that closes the TOCTOU window between inspecting a
path and opening it, and WP122 pays the same reuse: a second private copy of that reader is the
copy that silently drifts.  What this module adds is the layer above it — size ceilings per input
kind, controller digest verification, and the re-read that makes a swap after validation visible.
"""

from __future__ import annotations

import hashlib
import pathlib
import re
from dataclasses import dataclass

from oracle.safe_io import read_regular_single_link

from .errors import reject
from .paths import inspect_sealed_file

MAX_PLAN_BYTES = 64 * 1024
MAX_DOCUMENT_BYTES = 1024 * 1024
MAX_EXECUTABLE_BYTES = 256 * 1024 * 1024

SHA256_HEX = re.compile(r"[0-9a-f]{64}\Z")


@dataclass(frozen=True)
class SealedInput:
    """One controller-selected file, bound to the bytes that were actually read."""

    label: str
    path: str
    sha256: str
    size: int
    max_bytes: int

    def as_evidence(self) -> dict[str, object]:
        return {"label": self.label, "path": self.path, "sha256": self.sha256, "size": self.size}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def expected_digest(value: object, label: str) -> str:
    if not isinstance(value, str) or SHA256_HEX.fullmatch(value) is None:
        raise reject("plan_schema", "%s digest must be lowercase hexadecimal SHA-256" % label)
    return value


def read_sealed_bytes(target: pathlib.Path, label: str, *, max_bytes: int) -> bytes:
    """The single internal seam a test double may stand in for.

    It performs filesystem identity checks and reads exact bytes.  It takes no trust flag, no
    pre-computed observation and no callback: a double replaces the BYTES, which is exactly the
    hostile power the re-read below has to survive.
    """

    info = inspect_sealed_file(target, label, max_bytes=max_bytes)
    raw = read_regular_single_link(
        target,
        label,
        lambda _message: reject("sealed_input_unreadable", "%s could not be read safely" % label),
        require_readonly=True,
    )
    if len(raw) != info.st_size:
        # Two different causes land here and both must be loud rather than plausible.  One is a
        # truncation or replacement racing the read.  The other is Windows text mode: the shared
        # reader opens without `O_BINARY`, so a file holding CRLF comes back shorter than its own
        # `st_size` and its digest would be a confident hash of bytes that are not on disk.
        # Comparing the length against the inspected size turns that into a named refusal.
        raise reject("sealed_input_short_read", "%s did not read back its own byte count" % label)
    if len(raw) > max_bytes:
        raise reject("path_oversized", "%s exceeds its byte limit" % label)
    return raw


def load_sealed_input(
    target: pathlib.Path,
    label: str,
    *,
    max_bytes: int,
    sha256: str,
) -> SealedInput:
    """Read the file and bind the record to the bytes that were actually there.

    The content itself is not returned.  This package needs to know that a sealed input IS what
    the controller said it is; it has no business reading the prompt or the settings, and a return
    value nobody needs is a return value somebody eventually logs.
    """

    raw = read_sealed_bytes(target, label, max_bytes=max_bytes)
    actual = digest(raw)
    if actual != sha256:
        raise reject("sealed_input_digest", "%s does not match its controller digest" % label)
    return SealedInput(
        label=label,
        path=str(target),
        sha256=actual,
        size=len(raw),
        max_bytes=max_bytes,
    )


def reverify(sealed: SealedInput) -> None:
    """Read the file again and demand the same bytes.

    Validation that happens once describes the filesystem at one instant.  The controller input
    is re-read after the whole envelope has been assembled so that a path or content replacement
    performed during assembly cannot ride out on an envelope that was already approved.
    """

    raw = read_sealed_bytes(pathlib.Path(sealed.path), sealed.label, max_bytes=sealed.max_bytes)
    if len(raw) != sealed.size or digest(raw) != sealed.sha256:
        raise reject("sealed_input_replaced", "%s was replaced after validation" % sealed.label)
