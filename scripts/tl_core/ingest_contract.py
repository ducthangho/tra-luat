# -*- coding: utf-8 -*-
"""Pure contracts shared by every ingest entrypoint.

This module deliberately performs no Drive/registry/NLM I/O.  A plan is a
canonical commitment to the exact source bytes, destination and options.  The
write adapters may only execute a plan after explicit confirmation.
"""
from __future__ import annotations

import hashlib
import json
import unicodedata
import zipfile
from pathlib import Path
from typing import Any, Iterable

PLAN_SCHEMA = "ingest_plan.v2"
MAX_DIRECT_UPLOAD_BYTES = 35 * 1024 * 1024
_CONFIRM_VALUE = "yes"


def _nfc(value: Any) -> Any:
    """Normalize text without changing business meaning or path separators."""
    if isinstance(value, dict):
        return {unicodedata.normalize("NFC", str(k)): _nfc(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_nfc(v) for v in value]
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    return value


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        _nfc(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    """Hash a source exactly once using bounded memory."""
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while True:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _hash_payload(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def build_ingest_plan(
    source_path: str | Path,
    *,
    target_scope: str,
    canonical_name: str,
    profile: str,
    options: dict[str, Any] | None = None,
    source_kind: str = "local",
    source_id: str = "",
    source_sha256: str = "",
) -> dict[str, Any]:
    path = Path(source_path)
    if not path.is_file():
        return {"ok": False, "schema": PLAN_SCHEMA, "error": "SOURCE_NOT_FILE", "file": str(path)}
    size = path.stat().st_size
    source_hash = str(source_sha256 or "").strip() or sha256_file(path)
    identity_payload = {
        "content_hash": source_hash,
        "target_scope": str(target_scope or ""),
        "canonical_name": str(canonical_name or ""),
        "profile": str(profile or ""),
    }
    identity = _hash_payload(identity_payload)
    committed = {
        "schema": PLAN_SCHEMA,
        "source": {
            "kind": str(source_kind or "local"),
            "source_id": str(source_id or ""),
            "sha256": source_hash,
            "size": size,
        },
        "identity": identity_payload,
        "identity_hash": identity,
        "options": _nfc(dict(options or {})),
    }
    return {
        "ok": True,
        **committed,
        "plan_hash": _hash_payload(committed),
        "file": str(path),
    }


def identity_hash_for_drive_source(
    drive_id: str, *, target_scope: str, canonical_name: str, profile: str
) -> str:
    """v1.34.52 (F-04/D2 — grill GAS 2.21.2l 2026-07-15): identity_hash cho nguồn ĐÃ TRÊN DRIVE
    (ingest-missing — không có bytes cục bộ để hash trực tiếp). Dùng CHUNG payload shape + hàm hash
    với :func:`build_ingest_plan` (content_hash = sha256(drive_id) thay vì sha256(bytes)) — MỘT khái
    niệm identity_hash cho mọi đường ingest, không thêm thuật toán hash mới."""
    content_hash = sha256_bytes(str(drive_id or "").strip().encode("utf-8"))
    identity_payload = {
        "content_hash": content_hash,
        "target_scope": str(target_scope or ""),
        "canonical_name": str(canonical_name or ""),
        "profile": str(profile or ""),
    }
    return _hash_payload(identity_payload)


def build_remote_plan(
    source_id: str,
    *,
    target_scope: str,
    canonical_name: str,
    profile: str,
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Plan a legacy remote source whose bytes cannot be read locally.

    This is intentionally marked ``identity_strength=metadata``.  New ingest
    paths must use :func:`build_ingest_plan` after fetching and hashing bytes.
    """
    if not str(source_id or "").strip():
        return {"ok": False, "schema": PLAN_SCHEMA, "error": "SOURCE_ID_REQUIRED"}
    source_token = _hash_payload({"source_id": str(source_id)})
    identity_payload = {
        "content_hash": source_token,
        "target_scope": str(target_scope or ""),
        "canonical_name": str(canonical_name or ""),
        "profile": str(profile or ""),
    }
    committed = {
        "schema": PLAN_SCHEMA,
        "source": {"kind": "remote-id", "source_id": str(source_id), "sha256": None, "size": None},
        "identity": identity_payload,
        "identity_hash": _hash_payload(identity_payload),
        "identity_strength": "metadata",
        "options": _nfc(dict(options or {})),
    }
    return {"ok": True, **committed, "plan_hash": _hash_payload(committed)}


def authorize_apply(
    *,
    apply: bool,
    confirm: str | None,
    expected_plan_hash: str | None,
    actual_plan_hash: str,
    resume_plan_hash: str | None = None,
) -> dict[str, Any]:
    """Fail closed unless apply is bound to the reviewed plan.

    A resume journal may supply the expected hash, but confirmation remains
    mandatory because resume can still perform external writes.
    """
    if not apply:
        return {"ok": True, "mode": "DRY", "plan_hash": actual_plan_hash}
    if str(confirm or "").strip().lower() != _CONFIRM_VALUE:
        return {"ok": False, "error": "CONFIRM_REQUIRED", "expected": _CONFIRM_VALUE}
    expected = str(expected_plan_hash or "").strip()
    resumed = False
    if not expected and resume_plan_hash:
        expected = str(resume_plan_hash).strip()
        resumed = True
    if not expected:
        return {"ok": False, "error": "EXPECTED_PLAN_HASH_REQUIRED", "actual_plan_hash": actual_plan_hash}
    if expected != actual_plan_hash:
        return {
            "ok": False,
            "error": "PLAN_HASH_MISMATCH",
            "expected_plan_hash": expected,
            "actual_plan_hash": actual_plan_hash,
        }
    return {"ok": True, "mode": "APPLY", "plan_hash": actual_plan_hash, "authorized_by_resume": resumed}


def validate_source_file(
    path: str | Path,
    *,
    allowed_exts: Iterable[str],
    direct_upload: bool = True,
    max_upload_bytes: int = MAX_DIRECT_UPLOAD_BYTES,
) -> dict[str, Any]:
    """Validate extension, cheap magic bytes and direct-upload capacity."""
    p = Path(path)
    if not p.is_file():
        return {"ok": False, "error": "SOURCE_NOT_FILE", "file": str(p)}
    ext = p.suffix.lower()
    allowed = {str(x).lower() for x in allowed_exts}
    if ext not in allowed:
        return {"ok": False, "error": "UNSUPPORTED_EXTENSION", "ext": ext, "allowed": sorted(allowed)}
    size = p.stat().st_size
    if size <= 0:
        return {"ok": False, "error": "SOURCE_EMPTY", "size": size}
    if direct_upload and size > int(max_upload_bytes):
        return {
            "ok": False,
            "error": "DIRECT_UPLOAD_LIMIT_EXCEEDED",
            "size": size,
            "max_bytes": int(max_upload_bytes),
            "remediation": "Use an environment-provided large-file conversion/chunk source policy.",
        }
    with p.open("rb") as stream:
        head = stream.read(1024)
    ole = bytes.fromhex("D0CF11E0A1B11AE1")
    # v1.34.45 (audit merge): tolerate a leading UTF-8 BOM / whitespace so spec-valid PDFs and
    # RTFs whose signature is not at byte 0 (accepted by pdfplumber/pypdf) are not falsely rejected.
    debom = head.lstrip(b"\xef\xbb\xbf")
    magic_ok = True
    if ext == ".pdf":
        magic_ok = b"%PDF-" in head[:1024]
    elif ext in {".doc", ".xls"}:
        magic_ok = head.startswith(ole)
    elif ext in {".docx", ".xlsx", ".odt"}:
        magic_ok = head.startswith(b"PK\x03\x04") and zipfile.is_zipfile(p)
    elif ext == ".rtf":
        magic_ok = debom.lstrip().startswith(b"{\\rtf")
    elif ext in {".txt", ".md"}:
        magic_ok = b"\x00" not in head
    if not magic_ok:
        return {"ok": False, "error": "SOURCE_MAGIC_MISMATCH", "ext": ext, "magic_hex": head[:8].hex()}
    if ext in {".docx", ".xlsx", ".odt"}:
        required = {
            ".docx": {"[Content_Types].xml", "word/document.xml"},
            ".xlsx": {"[Content_Types].xml", "xl/workbook.xml"},
            ".odt": {"mimetype", "content.xml"},
        }[ext]
        try:
            with zipfile.ZipFile(p, "r") as zf:
                names = {unicodedata.normalize("NFC", n.replace("\\", "/")) for n in zf.namelist()}
                missing = sorted(required - names)
                if missing:
                    return {"ok": False, "error": "SOURCE_CONTAINER_STRUCTURE_INVALID", "ext": ext,
                            "missing": missing}
                # Reject a tiny wrapper around an unexpectedly huge XML member.
                for member in required:
                    info = zf.getinfo(member)
                    if info.file_size > max(64 * 1024 * 1024, int(max_upload_bytes)):
                        return {"ok": False, "error": "SOURCE_CONTAINER_MEMBER_TOO_LARGE", "ext": ext,
                                "member": member, "size": info.file_size}
        except (OSError, KeyError, zipfile.BadZipFile) as exc:
            return {"ok": False, "error": "SOURCE_CONTAINER_READ_FAILED", "ext": ext,
                    "detail": f"{type(exc).__name__}: {exc}"}
    return {"ok": True, "ext": ext, "size": size, "direct_upload": bool(direct_upload)}
