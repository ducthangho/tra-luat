"""Read a sealed Dispatcher authority snapshot outside the candidate checkout.

This module is candidate logic exercised offline.  It does not make the candidate a privileged
controller: operational promotion still requires an exact canonical SHA, a fresh external pin and
human audit.  The loader exists so the candidate can prove that authority is not selected by an
untrusted request, path, symlink or hard link.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import stat
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .errors import GatewayRejected, reject

MAX_AUTHORITY_BYTES = 64 * 1024
OID40 = re.compile(r"[0-9a-f]{40}\Z")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
LANE_ID = re.compile(r"(issue|pr):([1-9][0-9]*)\Z")
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/@-]{0,127}\Z")

_TOP_KEYS = frozenset(
    {"schema_version", "repository", "packet", "gateway_author", "lanes"}
)
_PACKET_KEYS = frozenset({"issue", "revision", "generation", "attempt"})
_LANE_KEYS = frozenset(
    {
        "kind",
        "number",
        "reviewed_sha",
        "lease_id",
        "lease_active",
        "verdict_enabled",
        "heartbeat_provider",
        "reviewer_provider",
    }
)
_SEAL = object()


@dataclass(frozen=True)
class PacketIdentity:
    issue: int
    revision: int
    generation: int
    attempt: int


@dataclass(frozen=True)
class LaneAuthority:
    lane_id: str
    kind: str
    number: int
    reviewed_sha: str
    lease_id: str
    lease_active: bool
    verdict_enabled: bool
    heartbeat_provider: str
    reviewer_provider: str


@dataclass(frozen=True)
class AuthoritySnapshot:
    """Immutable authority that can only be produced by this module's sealed loader."""

    repository: str
    packet: PacketIdentity
    gateway_author: str
    lanes: Mapping[str, LaneAuthority]
    _seal: object

    def __post_init__(self):
        if self._seal is not _SEAL:
            raise reject("candidate_authority", "authority must come from the sealed loader")
        object.__setattr__(self, "lanes", MappingProxyType(dict(self.lanes)))

    def is_sealed(self) -> bool:
        return self._seal is _SEAL


def _positive_int(value: object, category: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise reject(category, "authority contains an invalid positive integer")
    return value


def _exact_keys(value: object, keys: frozenset[str], category: str) -> dict[str, object]:
    if not isinstance(value, dict) or frozenset(value) != keys:
        raise reject(category, "authority object has missing or extra keys")
    if not all(isinstance(key, str) for key in value):
        raise reject(category, "authority keys must be strings")
    return value


def _parse_authority(value: object) -> AuthoritySnapshot:
    top = _exact_keys(value, _TOP_KEYS, "authority_schema")
    if top["schema_version"] != 1 or isinstance(top["schema_version"], bool):
        raise reject("authority_schema", "authority schema revision is not supported")
    repository = top["repository"]
    author = top["gateway_author"]
    if not isinstance(repository, str) or not REPOSITORY.fullmatch(repository):
        raise reject("authority_schema", "authority repository identity is invalid")
    if not isinstance(author, str) or not SAFE_ID.fullmatch(author):
        raise reject("authority_schema", "authority author identity is invalid")

    packet_value = _exact_keys(top["packet"], _PACKET_KEYS, "authority_schema")
    packet = PacketIdentity(
        issue=_positive_int(packet_value["issue"], "authority_schema"),
        revision=_positive_int(packet_value["revision"], "authority_schema"),
        generation=_positive_int(packet_value["generation"], "authority_schema"),
        attempt=_positive_int(packet_value["attempt"], "authority_schema"),
    )

    lanes_value = top["lanes"]
    if not isinstance(lanes_value, dict) or not lanes_value or len(lanes_value) > 64:
        raise reject("authority_schema", "authority must declare one to sixty-four lanes")
    lanes: dict[str, LaneAuthority] = {}
    seen_heads: dict[str, str] = {}
    for lane_id, raw_lane in lanes_value.items():
        if not isinstance(lane_id, str):
            raise reject("authority_schema", "authority lane identifiers must be strings")
        match = LANE_ID.fullmatch(lane_id)
        if match is None:
            raise reject("authority_schema", "authority lane identifier is invalid")
        lane = _exact_keys(raw_lane, _LANE_KEYS, "authority_schema")
        kind = lane["kind"]
        number = _positive_int(lane["number"], "authority_schema")
        reviewed_sha = lane["reviewed_sha"]
        lease_id = lane["lease_id"]
        if kind not in ("issue", "pr") or kind != match.group(1):
            raise reject("authority_schema", "authority lane kind disagrees with its identifier")
        if number != int(match.group(2)):
            raise reject("authority_schema", "authority lane number disagrees with its identifier")
        if not isinstance(reviewed_sha, str) or not OID40.fullmatch(reviewed_sha):
            raise reject("authority_schema", "authority reviewed SHA is not exact")
        if not isinstance(lease_id, str) or not SAFE_ID.fullmatch(lease_id):
            raise reject("authority_schema", "authority lease identifier is invalid")
        if not isinstance(lane["lease_active"], bool) or not isinstance(
            lane["verdict_enabled"], bool
        ):
            raise reject("authority_schema", "authority lane booleans are invalid")
        heartbeat_provider = lane["heartbeat_provider"]
        reviewer_provider = lane["reviewer_provider"]
        if heartbeat_provider not in ("claude", "codex"):
            raise reject("authority_schema", "authority heartbeat provider is invalid")
        if reviewer_provider not in ("claude", "codex", "human"):
            raise reject("authority_schema", "authority reviewer provider is invalid")
        if reviewed_sha in seen_heads:
            raise reject("authority_schema", "one reviewed SHA is ambiguously bound to two lanes")
        seen_heads[reviewed_sha] = lane_id
        lanes[lane_id] = LaneAuthority(
            lane_id=lane_id,
            kind=kind,
            number=number,
            reviewed_sha=reviewed_sha,
            lease_id=lease_id,
            lease_active=lane["lease_active"],
            verdict_enabled=lane["verdict_enabled"],
            heartbeat_provider=heartbeat_provider,
            reviewer_provider=reviewer_provider,
        )
    return AuthoritySnapshot(repository, packet, author, lanes, _SEAL)


def _safe_read_authority(path: pathlib.Path) -> bytes:
    try:
        before = path.lstat()
    except OSError as exc:
        raise reject("authority_missing", "sealed authority cannot be inspected") from exc
    if stat.S_ISLNK(before.st_mode):
        raise reject("authority_symlink", "sealed authority must not be a symlink")
    if not stat.S_ISREG(before.st_mode):
        raise reject("authority_nonregular", "sealed authority must be a regular file")
    if before.st_nlink != 1:
        raise reject("authority_hardlink", "sealed authority must have exactly one hard link")
    if before.st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH):
        raise reject("authority_writable", "sealed authority must be read-only")
    if before.st_size > MAX_AUTHORITY_BYTES:
        raise reject("authority_oversized", "sealed authority exceeds its byte limit")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        with os.fdopen(descriptor, "rb") as handle:
            opened = os.fstat(handle.fileno())
            if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
                raise reject("authority_changed", "sealed authority changed identity while opening")
            if opened.st_nlink != 1:
                raise reject("authority_hardlink", "sealed authority gained another hard link")
            raw = handle.read(MAX_AUTHORITY_BYTES + 1)
    except GatewayRejected:
        raise
    except OSError as exc:
        raise reject("authority_unreadable", "sealed authority could not be read safely") from exc
    if len(raw) > MAX_AUTHORITY_BYTES:
        raise reject("authority_oversized", "sealed authority exceeds its byte limit")
    return raw


def load_authority(
    trusted_root: pathlib.Path | str,
    relative_path: str,
    *,
    candidate_root: pathlib.Path | str,
) -> AuthoritySnapshot:
    """Load one read-only, single-link snapshot outside the candidate checkout.

    The caller supplies a trusted root and a relative locator.  An untrusted operation request is
    never allowed to supply either value; the gateway accepts only the returned sealed object.
    """

    root = pathlib.Path(trusted_root)
    candidate = pathlib.Path(candidate_root).resolve()
    if not root.is_absolute():
        raise reject("authority_path", "trusted authority root must be absolute")
    if not isinstance(relative_path, str) or "\\" in relative_path:
        raise reject("authority_path", "authority locator must be a safe POSIX relative path")
    pure = pathlib.PurePosixPath(relative_path)
    if pure.is_absolute() or not pure.parts or any(part in ("", ".", "..") for part in pure.parts):
        raise reject("authority_path", "authority locator must be a safe relative path")
    if len(pure.parts) != 1:
        raise reject("authority_path", "authority locator must be a direct child of the trusted root")
    root = root.resolve()
    target = root.joinpath(*pure.parts)
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise reject("authority_path", "authority locator escapes the trusted root") from exc
    resolved = target.resolve(strict=False)
    if resolved.parent != root:
        raise reject("authority_path", "authority locator resolves outside the trusted root")
    if resolved == candidate or resolved.is_relative_to(candidate):
        raise reject("candidate_authority", "authority must live outside the candidate checkout")
    raw = _safe_read_authority(target)
    try:
        text = raw.decode("utf-8", errors="strict")
        value = json.loads(text)
    except (UnicodeError, ValueError) as exc:
        raise reject("authority_encoding", "authority must be strict UTF-8 JSON") from exc
    return _parse_authority(value)
