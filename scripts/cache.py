#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cache.py — tiện ích cache tối thiểu mà ingest_to_cache.py import (cache_dir, find).
Tra cứu theo so_hieu HOẶC aliases (vd hỏi Luật gốc 89/2025/QH15 trúng record VBHN)."""
import json, os, re
from pathlib import Path

DEFAULT = os.environ.get("TRA_LUAT_CACHE", str(Path.home() / ".tra_luat_cache"))


def cache_dir(d=None) -> str:
    p = Path(d or DEFAULT)
    (p / "docs").mkdir(parents=True, exist_ok=True)
    return str(p)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def find(so_hieu: str, d=None):
    """→ doc record đầy đủ (kèm articles) khớp so_hieu/number_symbol/aliases, hoặc None."""
    key = _norm(so_hieu)
    matches = []
    for f in sorted(Path(cache_dir(d), "docs").glob("*.json"), key=lambda p: p.as_posix()):
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        cands = [doc.get("so_hieu", ""), doc.get("number_symbol", "")] + \
                list(doc.get("aliases", []) or [])
        if any(_norm(c) == key for c in cands if c):
            matches.append((f, doc))
    if len(matches) > 1:
        raise RuntimeError(f"CACHE_IDENTITY_CONFLICT:{key}:{[p.name for p, _ in matches]}")
    return matches[0][1] if matches else None


def get_article(so_hieu: str, n, d=None):
    doc = find(so_hieu, d)
    if not doc:
        return None
    return doc.get("articles", {}).get(str(n))


def get_doc(query: str, cache_dir_path: str = ""):
    """[tra_cuu --cache-id] tìm doc trong cache theo số hiệu/number_symbol/alias → doc dict (có structure[]),
    hoặc None. Dùng chung logic find() (cache docs do ingest_to_cache ghi có cả structure[] + articles{})."""
    return find(query, cache_dir_path or None)


def get_record(key_or_symbol: str, cache_dir_path: str = ""):
    """[tra_cuu] index record freshness/status (verified_at/doc_status/fetched_at…) cho doc. Overlay CHƯA có index
    riêng tách khỏi doc → trả None; tra_cuu BỎ QUA cache_meta khi None (vẫn chạy, chỉ ít cảnh báo freshness)."""
    return None
