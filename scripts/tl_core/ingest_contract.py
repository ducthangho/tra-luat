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

# r314 (ING-06): NGUỒN SỰ THẬT DUY NHẤT cho "đuôi nạp được". Trước đây tập này bị khai HAI LẦN, lệch
# nhau: ZIP planner (`zip_ingest._ALLOWED_INGEST_EXTS`) nhận thêm `.txt`/`.md`, còn child `ingest-local`
# (`_il_stage_plan` → `validate_source_file`) từ chối đúng hai đuôi đó bằng `UNSUPPORTED_EXTENSION`.
# Hệ quả: planner hứa một kế hoạch mà child CHẮC CHẮN không thực hiện được — member vào plan rồi chết
# ở bước sau, đúng lớp "nguồn sự thật nhân đôi" của sổ audit.
#
# Chọn THU planner về đúng năng lực child, KHÔNG nới child ra: nới nghĩa là cho phép upload `.txt`/`.md`
# rồi convert — đó là quyết định TÍNH NĂNG (đổi thứ được ghi vào corpus), không phải sửa lỗi lệch sổ.
# Muốn mở thì mở tường minh ở đây, một chỗ, và cả hai phía nhận cùng lúc.
INGEST_LOCAL_EXTS = frozenset({".doc", ".docx", ".pdf", ".rtf", ".odt"})


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
    """Hash a source exactly once using bounded memory.
    r187 (ADR-0004 WP7): ủy quyền engine — trong ingest_engine.run_scope() memo theo realpath
    (hash nguồn ĐÚNG 1 lần/run, kể cả child plan); ngoài scope hành vi cũ (tính mỗi lần gọi)."""
    from tl_core.ingest_engine import hash_file_once
    return hash_file_once(path, chunk_size=chunk_size)


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


def build_source_revision(
    provider: str, source_id: str, *, revision: str = "", version: str = "",
    checksum: str = "", observed_at: str = ""
) -> dict[str, Any]:
    """ADR-0011 (r184/ING-02): Source Revision — định danh NGUỒN + phiên bản NHÀ CUNG CẤP.
    KHÔNG PHẢI bằng chứng nội dung: `identity_strength='revision'` khi có revision/version/checksum,
    ngược lại 'metadata'. Chỉ byte-hash thật (build_ingest_plan) mới được mang `content_hash` —
    Source Revision không bao giờ nhét token vào slot content_hash."""
    sid = str(source_id or "").strip()
    if not sid:
        return {"ok": False, "error": "SOURCE_ID_REQUIRED"}
    strength = "revision" if (str(revision or "") or str(version or "") or str(checksum or "")) else "metadata"
    return {"ok": True, "schema": "source_revision.v1", "provider": str(provider or ""),
            "source_id": sid, "revision": str(revision or ""), "version": str(version or ""),
            "checksum": str(checksum or ""), "identity_strength": strength,
            "observed_at": str(observed_at or "")}


def claim_key_for_source(
    rev: dict, *, target_scope: str, canonical_name: str, profile: str
) -> str:
    """ADR-0011 (r184): khóa INGEST CLAIM (mutex chống ghi đồng thời xuyên host) từ một Source
    Revision. Payload KHÔNG có trường `content_hash` → không thể đội lốt Content Identity và không
    bao giờ được dùng cho no-op/dedup/replace. `observed_at` CỐ Ý loại khỏi khóa (mỗi host một
    timestamp — vào khóa là claim mất tác dụng)."""
    payload = {
        "claim": "ingest_claim.v1",
        "source_revision": {k: str((rev or {}).get(k) or "")
                            for k in ("schema", "provider", "source_id", "revision",
                                      "version", "checksum", "identity_strength")},
        "target_scope": str(target_scope or ""),
        "canonical_name": str(canonical_name or ""),
        "profile": str(profile or ""),
    }
    return _hash_payload(payload)


def identity_hash_for_drive_source(
    drive_id: str, *, target_scope: str, canonical_name: str, profile: str
) -> str:
    """r184 (ADR-0011 — ING-02): retype thành CLAIM KEY tường minh. Bản cũ (v1.34.52) nhét
    sha256(drive_id) vào slot `content_hash` cùng shape với build_ingest_plan — token định danh
    đội lốt bằng chứng nội dung (drive_id giữ nguyên nhưng revision đổi vẫn 'cùng nội dung').
    Nay: SourceRevision(gdrive, drive_id) → claim_key_for_source — chỉ hợp lệ làm khóa
    ingest_claim, KHÔNG dùng cho no-op/dedup/replace. Giá trị hash ĐỔI so với v1.34.52: hai host
    lệch phiên bản không khóa chéo nhau trong cửa sổ rollout (TTL claim 5' — chấp nhận, ghi rõ)."""
    rev = build_source_revision("gdrive", drive_id)
    if not rev.get("ok"):
        rev = {"schema": "source_revision.v1", "provider": "gdrive", "source_id": "",
               "revision": "", "version": "", "checksum": "", "identity_strength": "metadata"}
    return claim_key_for_source(rev, target_scope=target_scope,
                                canonical_name=canonical_name, profile=profile)


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
