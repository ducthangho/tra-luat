# -*- coding: utf-8 -*-
"""tl_core.chunking — Pha D (v1.33.57): tách NGUYÊN VĂN từ scripts/tl.py (kế hoạch nợ-kỹ-thuật D).

Public CLI vẫn là scripts/tl.py (stub ủy quyền). Nhận helper dùng chung của tl qua `bind(tl_module)`
(copy-globals, bỏ tên đã có — xem tl_core.workflow docstring). KHÔNG đọc bare mutable-global của tl.
"""
from __future__ import annotations

import argparse   # noqa: F401
import datetime   # noqa: F401
import hashlib    # noqa: F401
import json       # noqa: F401
import os         # noqa: F401
import re         # noqa: F401
import shutil     # noqa: F401
import subprocess # noqa: F401
import sys        # noqa: F401
import tempfile   # noqa: F401
import time       # noqa: F401
import unicodedata  # noqa: F401
import zipfile    # noqa: F401
from pathlib import Path  # noqa: F401

_TL = None


def bind(tl_module) -> None:
    global _TL
    _TL = tl_module
    g = globals()
    for _n in dir(tl_module):
        if _n.startswith("__") or _n in g:
            continue
        g[_n] = getattr(tl_module, _n)



def _chunk_records_from_text(text: str, *, name: str, max_chars: int) -> tuple[str, list[dict]]:
    records: list[dict] = []
    article_pat = re.compile(r"(?im)^\s*(Điều\s+\d+[a-zA-Z]?\s*[\.:].*)$")
    def _is_heading(m):
        # v1.33.56 (PH2-08): text pdftotext/wrap — tham chiếu 'quy định tại\nĐiều 5. của…' đứng đầu dòng
        # nhưng KHÔNG phải heading. Heading thật: dòng trước trống hoặc kết thúc bằng dấu kết câu.
        if m.start() == 0:
            return True
        prev = text[:m.start()].rstrip("\n")
        if not prev:
            return True
        last = prev.rsplit("\n", 1)[-1].rstrip()
        return (not last) or last[-1] in ".;:!?…)\u201d\u00bb"
    matches = [m for m in article_pat.finditer(text) if _is_heading(m)]
    if matches:
        boundaries = [(m.start(), (matches[i+1].start() if i+1 < len(matches) else len(text)), m.group(1).strip()) for i, m in enumerate(matches)]
        group_start = None; group_end = None; group_title = None; start_dieu = None; end_dieu = None
        for start, end, title in boundaries:
            dm = re.search(r"Điều\s+(\d+)", title)
            dno = int(dm.group(1)) if dm else None
            if group_start is not None and (end - group_start) > max_chars:
                chunk_text = text[group_start:group_end]
                records.append({"index": len(records)+1, "title": group_title or f"part{len(records)+1}", "start_char": group_start, "end_char": group_end, "start_dieu": start_dieu, "end_dieu": end_dieu, "chars": len(chunk_text), "text": chunk_text})
                group_start = None; group_end = None; group_title = None; start_dieu = None; end_dieu = None
            if group_start is None:
                group_start = start; group_title = title[:120]; start_dieu = dno
            group_end = end; end_dieu = dno
        if group_start is not None:
            chunk_text = text[group_start:group_end]
            records.append({"index": len(records)+1, "title": group_title or f"part{len(records)+1}", "start_char": group_start, "end_char": group_end, "start_dieu": start_dieu, "end_dieu": end_dieu, "chars": len(chunk_text), "text": chunk_text})
        return "by_article", records
    # v1.34.38 (#2 log phiên Chỉ thị): văn kiện Đảng/Đề án dài KHÔNG có Điều → trước đây rơi thẳng về cắt mù
    # by_paragraph_budget (có thể cắt GIỮA một Phần/Mục — phải dò tay ranh giới rồi tự dựng manifest). Nay thêm
    # strategy by_heading: nhận diện heading kiểu Mục (PHẦN thứ nhất/I/1 · Chương I/1 · Mục 1/I) đứng đầu dòng,
    # cùng guard _is_heading (dòng trước trống/kết câu — né trích dẫn 'tại Mục 3 của…' wrap đầu dòng); cần ≥2
    # heading mới dùng (1 heading = cả file, budget xử tốt hơn). Gộp heading liên tiếp theo max_chars như by_article.
    # [ \t] thay \s trong pattern: \s nuốt newline → title dính cả dòng sau (bug bắt khi viết r100).
    heading_pat = re.compile(
        r"(?im)^[ \t]*((?:phần[ \t]+(?:thứ[ \t]+\S+|[ivxlcd]+|\d+)|chương[ \t]+[ivxlcd\d]+|mục[ \t]+[ivxlcd\d]+)\b[ \t]*[\.:—-]?[^\n]*)$")
    def _is_muc_heading(m):
        # Heading kiểu Mục nhận thêm tín hiệu DÒNG TRỐNG ngay trước (đề án/văn kiện hay kết đoạn bằng
        # bảng/số liệu không dấu chấm — guard kết-câu của by_article một mình sẽ loại oan).
        if m.start() == 0 or re.search(r"\n[ \t]*\n\Z", text[:m.start()]):
            return True
        return _is_heading(m)
    hmatches = [m for m in heading_pat.finditer(text) if _is_muc_heading(m)]
    if len(hmatches) >= 2:
        boundaries = [(m.start(), (hmatches[i+1].start() if i+1 < len(hmatches) else len(text)), m.group(1).strip())
                      for i, m in enumerate(hmatches)]
        # preamble (tên đề án/quốc hiệu trước heading đầu) đi cùng chunk 1 — mất nó là mất tiêu đề văn kiện trong RAG
        boundaries[0] = (0, boundaries[0][1], boundaries[0][2])
        group_start = None; group_end = None; group_title = None
        for start, end, title in boundaries:
            if group_start is not None and (end - group_start) > max_chars:
                chunk_text = text[group_start:group_end]
                records.append({"index": len(records)+1, "title": group_title or f"part{len(records)+1}",
                                "start_char": group_start, "end_char": group_end,
                                "chars": len(chunk_text), "text": chunk_text})
                group_start = None; group_end = None; group_title = None
            if group_start is None:
                group_start = start; group_title = title[:120]
            group_end = end
        if group_start is not None:
            chunk_text = text[group_start:group_end]
            records.append({"index": len(records)+1, "title": group_title or f"part{len(records)+1}",
                            "start_char": group_start, "end_char": group_end,
                            "chars": len(chunk_text), "text": chunk_text})
        return "by_heading", records
    block_pat = re.compile(r".+?(?:\n\s*\n|\Z)", re.S)
    blocks = [(m.start(), m.end(), m.group(0)) for m in block_pat.finditer(text) if m.group(0).strip()]
    group_start = None; group_end = None
    for start, end, block in blocks:
        if group_start is not None and (end - group_start) > max_chars:
            chunk_text = text[group_start:group_end]
            records.append({"index": len(records)+1, "title": f"part{len(records)+1:02d}", "start_char": group_start, "end_char": group_end, "chars": len(chunk_text), "text": chunk_text})
            group_start = None; group_end = None
        if group_start is None:
            group_start = start
        group_end = end
    if group_start is not None:
        chunk_text = text[group_start:group_end]
        records.append({"index": len(records)+1, "title": f"part{len(records)+1:02d}", "start_char": group_start, "end_char": group_end, "chars": len(chunk_text), "text": chunk_text})
    return "by_paragraph_budget", records


def _safe_chunk_stem(name: str) -> str:
    s = unicodedata.normalize("NFKD", name or "chunk")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("._-")
    return s[:100] or "chunk"


def _chunk_plan_from_text(text: str, *, name: str, mode: str, max_chars: int) -> dict:
    sha = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    if mode == "vbqppl-canonical":
        return {"ok": False, "schema": "chunk_plan.v2", "mode": mode, "source_hash": sha, "error": "DO_NOT_SPLIT_VBQPPL_CANONICAL", "chunks": [], "apply_enabled": False}
    strategy, records = _chunk_records_from_text(text, name=name, max_chars=max_chars)
    chunks = []
    safe_base = _safe_chunk_stem(name)
    for r in records:
        c = {k: v for k, v in r.items() if k != "text"}
        c["text_preview"] = r.get("text", "")[:160]
        c["sha256"] = hashlib.sha256((r.get("text") or "").encode("utf-8", errors="replace")).hexdigest()
        c["expected_name"] = f"{safe_base}__part{r['index']:02d}" + (f"__Dieu_{r.get('start_dieu')}-{r.get('end_dieu')}" if r.get("start_dieu") else "")
        chunks.append(c)
    return {"ok": bool(chunks), "schema": "chunk_plan.v2", "mode": mode, "source_hash": sha, "strategy": strategy, "max_chars": max_chars, "total_chars": len(text), "chunk_count": len(chunks), "chunks": chunks, "apply_enabled": True, "note": "chunk-apply local chỉ tạo chunk files + manifest; chưa ghi Drive/NLM."}


def cmd_chunk_plan(a) -> int:
    path = Path(a.file)
    if not path.exists():
        out = {"ok": False, "schema": "chunk_plan.v2", "error": "FILE_NOT_FOUND", "file": str(path)}
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    text, warns = _read_local_text_for_analysis(path, max_chars=10_000_000)   # v1.33.56 (PH2-05): = cap apply/verify
    if not text:
        out = {"ok": False, "schema": "chunk_plan.v2", "error": "NO_TEXT_AVAILABLE", "warnings": warns, "file": str(path)}
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    out = _chunk_plan_from_text(text, name=a.name or path.stem, mode=a.mode, max_chars=a.max_chars)
    out["file"] = str(path)
    out["warnings"] = warns
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2


def cmd_chunk_apply(a) -> int:
    path = Path(a.file)
    out = {"ok": False, "schema": "chunk_apply.v1", "file": str(path), "mode": a.mode, "warnings": [], "chunks": []}
    if a.mode == "vbqppl-canonical":
        out["warnings"].append("DO_NOT_SPLIT_VBQPPL_CANONICAL")
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    if not path.exists():
        out["warnings"].append("FILE_NOT_FOUND")
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    text, warns = _read_local_text_for_analysis(path, max_chars=10_000_000)
    out["warnings"].extend(warns)
    if not text:
        out["warnings"].append("NO_TEXT_AVAILABLE")
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    name = a.name or path.stem
    source_hash = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    if getattr(a, "expected_hash", None) and a.expected_hash != source_hash:
        out["warnings"].append("SOURCE_HASH_CHANGED")
        out["expected_hash"] = a.expected_hash; out["source_hash"] = source_hash
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    strategy, records = _chunk_records_from_text(text, name=name, max_chars=a.max_chars)
    od = Path(a.out_dir) if getattr(a, "out_dir", None) else path.parent / f"{_safe_chunk_stem(name)}_chunks"
    od.mkdir(parents=True, exist_ok=True)
    manifest = {"schema": "chunk_manifest.v1", "source_file": str(path), "source_hash": source_hash, "mode": a.mode, "strategy": strategy, "name": name, "max_chars": a.max_chars, "chunk_count": len(records), "chunks": []}
    safe_base = _safe_chunk_stem(name)
    for r in records:
        expected = f"{safe_base}__part{r['index']:02d}" + (f"__Dieu_{r.get('start_dieu')}-{r.get('end_dieu')}" if r.get("start_dieu") else "")
        chunk_path = od / f"{expected}.md"
        chunk_hash = hashlib.sha256((r.get("text") or "").encode("utf-8", errors="replace")).hexdigest()
        header = {
            "source_file": str(path), "source_hash": source_hash, "mode": a.mode, "chunk_index": r["index"],
            "chunk_count": len(records), "start_char": r.get("start_char"), "end_char": r.get("end_char"),
            "start_dieu": r.get("start_dieu"), "end_dieu": r.get("end_dieu"), "chunk_sha256": chunk_hash,
            "canonical": False, "note": "VBQPPL chunks are helper sources for NLM only, not legal canonical." if a.mode.startswith("vbqppl") else "Profile chunk for query quality.",
        }
        body = "---\n" + json.dumps(header, ensure_ascii=False, indent=2) + "\n---\n\n" + (r.get("text") or "")
        _write_text_atomic(chunk_path, body)
        item = {k: v for k, v in r.items() if k != "text"}
        item.update({"expected_name": expected, "path": str(chunk_path), "sha256": chunk_hash})
        manifest["chunks"].append(item)
        out["chunks"].append(item)
    manifest_path = od / "chunk_manifest.json"
    _write_text_atomic(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2))
    out.update({"ok": True, "out_dir": str(od), "manifest": str(manifest_path), "source_hash": source_hash, "strategy": strategy, "chunk_count": len(records)})
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0


def cmd_chunk_verify(a) -> int:
    mp = Path(a.manifest)
    out = {"ok": False, "schema": "chunk_verify.v1", "manifest": str(mp), "checks": [], "warnings": []}
    if not mp.exists():
        out["warnings"].append("MANIFEST_NOT_FOUND")
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    try:
        man = json.loads(mp.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        out["warnings"].append(f"MANIFEST_INVALID:{type(e).__name__}:{e}")
        print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
    def check(name, ok, detail=""):
        out["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    chunks = man.get("chunks") or []
    check("manifest_schema", man.get("schema") == "chunk_manifest.v1", str(man.get("schema")))
    check("chunk_count_match", int(man.get("chunk_count") or -1) == len(chunks), f"{man.get('chunk_count')} vs {len(chunks)}")
    src = Path(man.get("source_file") or "")
    if src.exists():
        txt, _warns = _read_local_text_for_analysis(src, max_chars=10_000_000)
        src_hash = hashlib.sha256(txt.encode("utf-8", errors="replace")).hexdigest() if txt else ""
        check("source_hash_unchanged", src_hash == man.get("source_hash"), src_hash[:12])
    else:
        out["warnings"].append("SOURCE_FILE_NOT_FOUND_SKIP_HASH_CHECK")
    for item in chunks:
        cp = Path(item.get("path") or "")
        exists = cp.exists()
        check(f"chunk_{item.get('index')}_exists", exists, str(cp))
        if exists:
            raw = cp.read_text(encoding="utf-8", errors="replace")
            # v1.33.56 (PH2-07): neo delimiter theo DÒNG '---' đứng riêng — split('---',2) trần vỡ khi
            # source_file path trong header chứa chuỗi '---' (cắt ngay giữa JSON → hash sai oan).
            _fm = re.match(r"\A---\n.*?\n---\n", raw, re.S)
            content = raw[_fm.end():] if _fm else raw
            if _fm:
                if content.startswith("\n"):
                    content = content[1:]
            h = hashlib.sha256(content.encode("utf-8", errors="replace")).hexdigest()
            check(f"chunk_{item.get('index')}_hash", h == item.get("sha256"), h[:12])
    out["ok"] = all(c["ok"] for c in out["checks"])
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2


def _load_chunk_manifest(manifest_path: str) -> tuple[dict|None, list[str]]:
    mp = Path(manifest_path)
    if not mp.exists():
        return None, ["MANIFEST_NOT_FOUND"]
    try:
        return json.loads(mp.read_text(encoding="utf-8", errors="replace")), []
    except Exception as e:  # noqa: BLE001
        return None, [f"MANIFEST_INVALID:{type(e).__name__}:{e}"]


def _profile_ingest_chunks_plan(a) -> dict:
    verify = _run_child_tl(["chunk-verify", a.manifest, "--json"])
    man, warnings = _load_chunk_manifest(a.manifest)
    out = {"ok": bool(verify.get("ok")) and man is not None, "schema": "chunk_ingest_bridge.v1", "manifest": a.manifest,
           "apply": bool(getattr(a, "apply", False)), "verification": verify, "warnings": warnings, "planned_child_commands": [],
           "idempotency": _idempotency_contract_for_workflow("chunk_ingest"),
           "note": "Bridge không ghi trực tiếp; apply chỉ gọi lại profile-ingest từng chunk đã verify."}
    if not man:
        return out
    out.update({"manifest_mode": man.get("mode"), "source_file": man.get("source_file"), "source_hash": man.get("source_hash"), "chunk_count": len(man.get("chunks") or [])})
    if man.get("mode") != "profile":
        out["ok"] = False
        out["warnings"].append("ONLY_PROFILE_CHUNKS_CAN_BE_INGESTED_IN_STAGE4")
    profile = getattr(a, "profile", None)
    for item in (man.get("chunks") or []):
        cp = item.get("path")
        expected = item.get("expected_name") or Path(cp or "chunk").stem
        child = ["profile-ingest", str(cp), "--name", expected, "--source-quality", "digital", "--json"]
        if profile:
            child += ["--profile", profile]
        if getattr(a, "allow_default", False):
            child.append("--allow-default")
        if getattr(a, "skip_live_check", False):
            child.append("--skip-live-check")
        if getattr(a, "apply", False):
            child.append("--apply")
        out["planned_child_commands"].append({"chunk_index": item.get("index"), "path": cp, "expected_name": expected, "command": child})
    if not out["planned_child_commands"]:
        out["ok"] = False; out["warnings"].append("NO_CHUNKS_IN_MANIFEST")
    return out


def cmd_profile_ingest_chunks(a) -> int:
    ok, err = _bridge_confirm_apply(a, what="profile-ingest-chunks")
    if not ok:
        print(_json_dumps(err, deterministic=_deterministic_enabled(a))); return 2
    plan = _profile_ingest_chunks_plan(a)
    if not getattr(a, "apply", False):
        print(_json_dumps(plan, deterministic=_deterministic_enabled(a))); return 0 if plan.get("ok") else 2
    if not plan.get("ok"):
        print(_json_dumps(plan, deterministic=_deterministic_enabled(a))); return 2
    results = []
    for rec in plan.get("planned_child_commands", []):
        r = _run_child_tl(rec["command"])
        r.update({"chunk_index": rec.get("chunk_index"), "path": rec.get("path"), "expected_name": rec.get("expected_name")})
        results.append(r)
        if not r.get("ok") and not getattr(a, "continue_on_error", False):
            break
    out = {**plan, "schema": "chunk_ingest_bridge_apply.v1", "results": results, "ok": bool(results) and all(r.get("ok") for r in results)}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2
