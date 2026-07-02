#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mcp_bridge.py — GĐ1: backend transport Drive cho env CHAT (Google Drive MCP / NotebookLM MCP).

Bối cảnh (RUNBOOK §A0): env Chat KHÔNG chạy shell/binary/tl.py → transport Drive = Drive MCP, do
CHÍNH Claude gọi tool MCP (không phải Python). Vì vậy Python in-process KHÔNG thực thi được MCP:
  - call(op, **kw)  → raise DeferToMCP (mang theo spec để lớp trên/agent gọi tool).
  - spec(op, **kw)  → {"backend":"mcp", "tool": <tên tool>, "args": {...}} — đối xứng interface gws_bridge,
                       dùng cho: (a) hướng dẫn Chat gọi đúng tool; (b) parity-test (Claude gọi rồi đối chứng).

Tên tool MCP có tiền tố server-id (đổi theo phiên kết nối) → lấy từ env TL_DRIVE_MCP_PREFIX nếu có,
mặc định = prefix Drive MCP hiện hành. `tool_basename` luôn ổn định để khớp khi prefix đổi.
"""
from __future__ import annotations
import json, os
from typing import Any

# Prefix server Drive MCP hiện hành (đổi theo phiên → override bằng env TL_DRIVE_MCP_PREFIX).
DEFAULT_DRIVE_MCP_PREFIX = "mcp__51b3e10f-6a36-461d-9f47-fa5b90b393ce__"


class DeferToMCP(RuntimeError):
    """Op cần MCP nhưng đang chạy trong Python (Code/Cowork). Mang .spec để agent gọi tool MCP."""
    def __init__(self, spec: dict):
        super().__init__(f"DeferToMCP: gọi tool MCP `{spec.get('tool')}` (env Chat / parity-test).")
        self.spec = spec


def _prefix() -> str:
    return os.environ.get("TL_DRIVE_MCP_PREFIX") or DEFAULT_DRIVE_MCP_PREFIX


# op → (tool_basename, hàm dựng args). Chỉ Drive read (nhóm A) ở GĐ1; ghi (B/C) → GĐ2/GĐ3.
def _args_files_get(file_id: str, **_) -> dict:
    # excludeContentSnippets: get-meta CHỈ lấy metadata — chặn Drive MCP trả contentSnippet (đã thấy LỘ
    # token webapp khi get-meta file config). gws/GAS không trả nội dung → cũng giữ parity sạch.
    return {"fileId": file_id, "excludeContentSnippets": True}


def _args_search(q: str, page_size: int = 100, **_) -> dict:
    # LƯU Ý cú pháp Drive MCP: dùng `title contains '...'` (KHÔNG `name`); chuỗi single-quote.
    return {"query": q, "pageSize": page_size}


def _args_read(file_id: str, include_comments: bool = False, **_) -> dict:
    return {"fileId": file_id, "includeComments": bool(include_comments)}


def _args_upload(name: str, parents=None, text_content: str | None = None,
                 base64_content: str | None = None, mime: str | None = None,
                 convert_to: str | None = None, **_) -> dict:
    """create_file: Chat tạo file từ NỘI DUNG (không có FS local). text/plain → tự convert GDoc;
    convert_to=None + mime → giữ nguyên type (disableConversionToGoogleType)."""
    a: dict[str, Any] = {"title": name}
    if parents:
        a["parentId"] = parents[0] if isinstance(parents, (list, tuple)) else parents
    if text_content is not None:
        a["textContent"] = text_content
    elif base64_content is not None:
        a["base64Content"] = base64_content
    if mime:
        a["contentMimeType"] = mime
    if convert_to is None and mime:
        a["disableConversionToGoogleType"] = True
    return a


def _args_copy(file_id: str, name: str | None = None, parents=None, **_) -> dict:
    a: dict[str, Any] = {"fileId": file_id}
    if name:
        a["title"] = name
    if parents:
        a["parentId"] = parents[0] if isinstance(parents, (list, tuple)) else parents
    return a


_OP_TOOL = {
    "files_get":   ("get_file_metadata", _args_files_get),
    "files_list":  ("search_files", _args_search),
    "search":      ("search_files", _args_search),
    "read":        ("read_file_content", _args_read),       # NL text (Chat đọc GDoc)
    "download":    ("download_file_content", lambda file_id, mime="text/plain", **_:
                    {"fileId": file_id, "exportMimeType": mime}),  # base64 đúng-byte (parity)
    "upload":      ("create_file", _args_upload),           # nhóm B (GĐ2): tạo file từ nội dung
    "copy_convert": ("copy_file", _args_copy),              # LƯU Ý: copy_file KHÔNG đổi mimeType (xem ghi chú)
}

# Ghi rủi ro (nhóm C) ở Chat: theo doctrine 3-env, DEFER về Code/Cowork (hygiene/business-logic Python).
_DEFER_WRITE = {"move", "rename", "trash", "restore"}
# Ghi chú: copy_convert qua copy_file CHỈ sao chép cùng-type (Drive MCP không có cờ convert). Để docx→GDoc
# thực thụ ở Chat, dùng create_file (text/plain → auto GDoc) hoặc DEFER Code/Cowork (gws files copy có convert).


def spec(op: str, **kw) -> dict:
    """Trả spec tool MCP cho op (không thực thi). Dùng cho hướng dẫn Chat + parity-test."""
    if op in _DEFER_WRITE:
        return {"backend": "mcp", "op": op, "defer": "Code/Cowork",
                "note": f"[{op}] ghi corpus — Chat KHÔNG tự chạy; defer Code/Cowork (gws_bridge)."}
    ent = _OP_TOOL.get(op)
    if ent is None:
        raise KeyError(f"mcp_bridge: op chưa map tool MCP: {op}")
    basename, argf = ent
    return {"backend": "mcp", "op": op,
            "tool_basename": basename, "tool": _prefix() + basename,
            "args": argf(**kw)}


def call(op: str, **kw):
    """Python KHÔNG gọi được MCP → raise DeferToMCP(spec). (Ở env Chat, Claude gọi tool theo spec.)"""
    raise DeferToMCP(spec(op, **kw))


# ───────────────────────── chuẩn hoá kết quả MCP → parity ─────────────────────────
def normalize_file(meta: dict) -> dict:
    """Đưa kết quả get_file_metadata (Drive MCP) về cùng shape gws_bridge.normalize_file.
    Drive MCP có thể trả id/name/mimeType/md5Checksum/parents (tuỳ field) — map mềm dẻo."""
    meta = meta or {}
    size = meta.get("size") or meta.get("sizeBytes") or meta.get("fileSize")
    parents = meta.get("parents") or meta.get("parentIds") or meta.get("parentId") or []
    if isinstance(parents, str):
        parents = [parents]
    return {
        "id": meta.get("id") or meta.get("fileId"),
        "name": meta.get("name") or meta.get("title"),
        "mimeType": meta.get("mimeType"),
        "size": str(size) if size is not None else None,
        "md5": meta.get("md5Checksum") or meta.get("md5"),
        "parents": list(parents),
        "trashed": bool(meta.get("trashed", False)),
        "modifiedTime": meta.get("modifiedTime"),
    }
