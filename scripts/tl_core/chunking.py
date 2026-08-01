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
        if (not last) or last[-1] in ".;:!?…)\u201d\u00bb":
            return True
        # v1.35.66 (r230): guard PH2-08 CHẶN OAN tiêu đề đứng ngay sau DÒNG CƠ CẤU không có dấu kết câu
        # ("Chương I" / "NHỮNG QUY ĐỊNH CHUNG" / "Mục 1"). Ca thật: Luật BHXH 41/2024 — `Điều 1.` nằm
        # ngay sau `NHỮNG QUY ĐỊNH CHUNG` ⇒ bị loại ⇒ rơi khỏi MỌI chunk (mất 750 ký tự: khối đầu
        # văn bản + trọn Điều 1) mà `warnings` vẫn RỖNG.
        if re.match(r"(?i)^\s*(chương|mục|phần|tiểu\s+mục)\b", last):
            return True
        return last == last.upper() and len(last) <= 120   # dòng TOÀN HOA = tiêu đề cơ cấu
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
        # v1.35.66 (r230) BẢO TOÀN NỘI DUNG: chunk chỉ chạy TỪ tiêu đề đầu tiên, nên mọi thứ đứng
        # trước nó (khối đầu văn bản: cơ quan ban hành, SỐ HIỆU, tên luật, căn cứ — và cả một Điều bị
        # `_is_heading` loại oan) BIẾN MẤT không dấu vết. Đo trên Luật BHXH 41/2024: total 183.428 ký
        # tự nhưng tổng chunk chỉ 182.678 ⇒ hụt 750, `warnings` RỖNG. Nay gắn phần đầu vào chunk 1 —
        # bất biến: tổng ký tự các chunk == tổng ký tự nguồn.
        if records and boundaries and boundaries[0][0] > 0:
            head = text[:boundaries[0][0]]
            if head.strip():
                r0 = records[0]
                r0["text"] = head + r0["text"]
                r0["start_char"] = 0
                r0["chars"] = len(r0["text"])
        return "by_article", records
    # v1.34.38 (#2 log Chỉ thị) + v1.34.40 C.1 REDESIGN (log: chunk 191k lọt qua max-chars 90k + Phần V bị gộp
    # mất ranh giới): strategy by_heading cho văn kiện Đảng/Đề án KHÔNG có Điều. LUẬT MỚI (grill 2026-07-13):
    #   (1) heading CẤP CAO NHẤT xuất hiện (PHẦN > Chương > Mục) KHÔNG BAO GIỜ gộp với nhau — 1 section/chunk
    #       (ranh giới tự nhiên thắng budget-packing; RAG trích dẫn theo Phần);
    #   (2) section VƯỢT max_chars → tách CON theo heading cấp dưới trong section (đệ quy xuống numbered `1.`);
    #       cấp dưới gộp liên tiếp theo budget như cũ; hết cấp → cắt paragraph-budget, title 'X (i/n)';
    #   (3) mọi mảnh sinh từ section vượt budget mang flag CHUNK_SPLIT_OVER_BUDGET (không im lặng).
    # Guard heading: dòng-trống-ngay-trước HOẶC kết-câu (khuôn _is_heading); [ \t] thay \s (né nuốt newline).
    _HEAD_LEVELS = (
        re.compile(r"(?im)^[ \t]*(phần[ \t]+(?:thứ[ \t]+\S+|[ivxlcd]+|\d+)\b[ \t]*[\.:—-]?[^\n]*)$"),
        re.compile(r"(?im)^[ \t]*(chương[ \t]+[ivxlcd\d]+\b[ \t]*[\.:—-]?[^\n]*)$"),
        re.compile(r"(?im)^[ \t]*(mục[ \t]+[ivxlcd\d]+\b[ \t]*[\.:—-]?[^\n]*)$"),
        re.compile(r"(?m)^[ \t]*(\d+(?:\.\d+)*[\.\)][ \t]+\S[^\n]*)$"),   # numbered 1. / 1.1. / 2) — CHỈ làm cấp tách con
    )

    def _guarded(pat, lo, hi):
        out = []
        for m in pat.finditer(text, lo, hi):
            if m.start() == lo or re.search(r"\n[ \t]*\n\Z", text[lo:m.start()]) or _is_heading(m):
                out.append((m.start(), m.group(1).strip()))
        return out

    def _emit(lo, hi, title, flags):
        rec = {"index": len(records) + 1, "title": (title or f"part{len(records)+1}")[:120],
               "start_char": lo, "end_char": hi, "chars": hi - lo, "text": text[lo:hi]}
        if flags:
            rec["flags"] = list(flags)
        records.append(rec)

    def _budget_cut(lo, hi, title, flags):
        # hết cấp heading → cắt theo đoạn văn trong [lo,hi), title 'X (i/n)' — không bao giờ cắt giữa đoạn
        spans, gs = [], lo
        for bm in re.finditer(r".+?(?:\n\s*\n|\Z)", text[lo:hi], re.S):
            be = lo + bm.end()
            if be - gs > max_chars and gs < lo + bm.start():
                spans.append((gs, lo + bm.start())); gs = lo + bm.start()
        spans.append((gs, hi))
        for i, (s0, s1) in enumerate(spans, 1):
            _emit(s0, s1, f"{title} ({i}/{len(spans)})" if len(spans) > 1 else title, flags)

    def _emit_section(lo, hi, title, lvl, over):
        flags = ("CHUNK_SPLIT_OVER_BUDGET",) if over else ()
        if hi - lo <= max_chars:
            _emit(lo, hi, title, flags); return
        for nxt in range(lvl + 1, len(_HEAD_LEVELS)):
            subs = _guarded(_HEAD_LEVELS[nxt], lo, hi)
            if subs:
                bounds = [(lo, subs[0][0], title)] if subs[0][0] > lo else []
                bounds += [(s, (subs[i+1][0] if i+1 < len(subs) else hi), f"{title} · {t}"[:120])
                           for i, (s, t) in enumerate(subs)]
                # cấp dưới GỘP liên tiếp theo budget (chỉ cấp cao nhất mới cấm gộp)
                gs, ge, gt = None, None, None
                for s0, s1, t in bounds:
                    if gs is not None and s1 - gs > max_chars:
                        _emit_section(gs, ge, gt, nxt, True); gs = None
                    if gs is None:
                        gs, gt = s0, t
                    ge = s1
                if gs is not None:
                    _emit_section(gs, ge, gt, nxt, True)
                return
        _budget_cut(lo, hi, title, ("CHUNK_SPLIT_OVER_BUDGET",))

    _top_lvl, _tops = None, []
    for _lv in range(3):                       # numbered (idx 3) KHÔNG làm cấp cao nhất
        _tops = _guarded(_HEAD_LEVELS[_lv], 0, len(text))
        if len(_tops) >= 2:
            _top_lvl = _lv; break
    if _top_lvl is not None:
        _sects = [(s, (_tops[i+1][0] if i+1 < len(_tops) else len(text)), t) for i, (s, t) in enumerate(_tops)]
        _sects[0] = (0, _sects[0][1], _sects[0][2])   # preamble (tên đề án) đi cùng chunk 1
        for s0, s1, t in _sects:
            _emit_section(s0, s1, t, _top_lvl, s1 - s0 > max_chars)
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


def _chunk_ingest_target(chunk_path: str | None) -> tuple[str | None, str | None]:
    """r251 — đường tệp mà `profile-ingest` THỰC SỰ nhận, tính TRƯỚC và KHÔNG ghi gì.

    Trả `(ingest_path, materialize_from)`. Chunk `.md` ⇒ `.docx` cùng thư mục (đường mà
    `_chunk_md_to_docx` sẽ sinh ở bước apply); tệp khác ⇒ giữ nguyên, `materialize_from=None`.
    Tách riêng để PLAN và APPLY dùng CÙNG một phép suy đường — plan in ra lệnh nào thì
    apply chạy đúng lệnh đó (xem `_profile_ingest_chunks_plan`).
    """
    if not chunk_path:
        return chunk_path, None
    p = Path(chunk_path)
    if p.suffix.lower() == ".md":
        return str(p.with_suffix(".docx")), str(p)
    return str(p), None


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
        # r251: PLAN phải in ĐÚNG lệnh mà apply chạy. Trước đây plan in đường `.md` của chunk, nhưng
        # `profile-ingest` KHÔNG nhận `.md` ⇒ ai chạy tay y nguyên lệnh trong plan ăn `rc=2
        # UNSUPPORTED_EXTENSION` và kết luận pipeline chunk gãy — trong khi apply thì chạy được nhờ cầu
        # nối r231 vật chất hoá `.docx`. Plan `ok:true` mà lệnh của nó không chạy nổi là plan NÓI DỐI.
        ingest_path, materialize_from = _chunk_ingest_target(cp)
        child = ["profile-ingest", str(ingest_path), "--name", expected, "--source-quality", "digital", "--json"]
        if profile:
            child += ["--profile", profile]
        # r299 (P16-F11, cùng họ với `ocr.py`): `--config` cũng phải đi theo xuống con. Cầu nối nằm
        # trong `_CREDS_LAZY_CMDS` nên `main()` không áp hộ; thiếu nó thì con TỰ DÒ `_config_candidates`
        # và có thể ghi vào scope khác scope người gõ đã chỉ cho lệnh cha.
        _cfg299 = getattr(a, "config", None)
        if _cfg299:
            child += ["--config", str(_cfg299)]
        if getattr(a, "allow_default", False):
            child.append("--allow-default")
        if getattr(a, "skip_live_check", False):
            child.append("--skip-live-check")
        # r299 (P16-F26): `--apply` TRẦN ⇒ `authorize_apply` (ingest_contract) trả `CONFIRM_REQUIRED`
        # 100% vì nó đòi CẢ `--confirm yes` LẪN `--expected-plan-hash`. Nghĩa là
        # `profile-ingest-chunks --apply` CHƯA BAO GIỜ chạy được. `ocr.py` đã vá ĐÚNG bệnh này từ
        # v1.34.53/C1 bằng khuôn HAI BƯỚC (`_bridge_run_child_apply`: chạy DRY lấy `plan_hash` → apply
        # kèm `--expected-plan-hash`), và khuôn đó ĐÃ re-export sang namespace tl ⇒ ở đây gọi thẳng.
        # Sót nhánh này đúng là bài học "vá một reader chưa phải vá xong bẫy".
        # `command_dry` LUÔN có; `command` chỉ khác khi apply — giữ y khuôn `planned_child_dry` /
        # `planned_child_command` của `ocr.py`, và ĐƯỜNG TỆP vẫn ở index 1 ở CẢ HAI (guard r251).
        rec = {"chunk_index": item.get("index"), "path": cp, "expected_name": expected,
               "command_dry": list(child),
               "command": (child + ["--apply", "--confirm", "yes"]) if getattr(a, "apply", False) else list(child)}
        if materialize_from:
            rec["materialize_from"] = materialize_from
            rec["materialize_note"] = ("chunk `.md` được vật chất hoá thành `.docx` (stdlib zipfile+XML) "
                                       "NGAY TRƯỚC khi gọi profile-ingest — chạy tay thì tạo .docx trước.")
        out["planned_child_commands"].append(rec)
    if not out["planned_child_commands"]:
        out["ok"] = False; out["warnings"].append("NO_CHUNKS_IN_MANIFEST")
    return out


def _chunk_md_to_docx(md_path: str) -> str:
    """v1.35.67 (r231) — VÁ KHỚP NỐI GÃY của chính pipeline chunk.

    `chunk-apply` ghi `.md`, nhưng `profile-ingest` chỉ nhận doc/docx/odt/pdf/rtf/xls/xlsx
    ⇒ `profile-ingest-chunks` gọi con luôn rc=2 (`UNSUPPORTED_EXTENSION`) — pipeline đứt ở đúng
    chỗ nối nó lại. Nới allowlist là SAI hướng (mở cửa cho .md bất kỳ vào corpus); thay vào đó
    cầu nối tự vật chất hoá chunk thành .docx.

    Viết .docx bằng `zipfile` + XML thuần — KHÔNG thêm phụ thuộc (requirements.txt: stdlib-only).
    Front-matter JSON của chunk được giữ thành đoạn đầu (dấu vết xuất xứ + sha256), thân giữ NGUYÊN VĂN.
    """
    raw = Path(md_path).read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta_txt, body = (m.group(1), m.group(2).lstrip("\n")) if m else ("", raw)
    try:
        meta = json.loads(meta_txt) if meta_txt else {}
    except Exception:
        meta = {}
    head = ""
    if meta:
        head = ("[chunk %s/%s · Điều %s-%s · sha256 %s]" % (
            meta.get("chunk_index"), meta.get("chunk_count"),
            meta.get("start_dieu"), meta.get("end_dieu"), str(meta.get("chunk_sha256", ""))[:16]))

    def _esc(t: str) -> str:
        return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

    paras = ([head] if head else []) + body.split("\n")
    body_xml = "".join(
        '<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % _esc(line) for line in paras)
    doc_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
               '<w:body>%s</w:body></w:document>' % body_xml)
    ctypes = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
              '<Default Extension="xml" ContentType="application/xml"/>'
              '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.'
              'wordprocessingml.document.main+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
            'officeDocument" Target="word/document.xml"/></Relationships>')
    out = str(Path(md_path).with_suffix(".docx"))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ctypes)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc_xml)
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
    # v1.34.40 B.3 (log Chỉ thị — nạp 9 chunk >600s buffer đến cuối → timeout tưởng thất bại dù 9/9 đã lên
    # Drive): STREAM tiến độ per-chunk ra stderr (khuôn profile-doctor --deep v1.34.30) + resume_command khi
    # đứt giữa chừng — child profile-ingest có dedup-gate nên chạy lại an toàn (chunk đã lên bị chặn trùng).
    results = []
    _cmds = plan.get("planned_child_commands", [])
    _n = len(_cmds)
    _resume_note = None
    for _i, rec in enumerate(_cmds, 1):
        print(f"[chunks] ({_i}/{_n}) {rec.get('expected_name')} …", file=sys.stderr, flush=True)
        _cmd = list(rec["command"])
        # r231: profile-ingest không nhận .md ⇒ vật chất hoá .docx trước khi gọi con.
        # r251: lệnh trong `rec` ĐÃ trỏ .docx (do plan tính qua `_chunk_ingest_target`), nên ở đây chỉ
        # còn việc TẠO tệp đó từ `materialize_from`. Guard: đường sinh ra phải TRÙNG đường đã in trong
        # plan — lệch nghĩa là hai phép suy đường đã trôi khỏi nhau, và plan lại nói dối lần nữa.
        _src_md = rec.get("materialize_from")
        if _src_md and Path(_src_md).is_file():
            _made = _chunk_md_to_docx(_src_md)
            if _made != _cmd[1]:
                results.append({"ok": False, "error": "MATERIALIZE_PATH_MISMATCH", "made": _made,
                                "planned": _cmd[1], "chunk_index": rec.get("chunk_index"),
                                "path": rec.get("path"), "expected_name": rec.get("expected_name")})
                _resume_note = (f"Đứt ở chunk {_i}/{_n}: đường .docx vật chất hoá ({_made}) LỆCH đường "
                                f"trong plan ({_cmd[1]}) — không chạy con để tránh nạp sai tệp.")
                break
        # r299 (P16-F26): chạy HAI BƯỚC — DRY lấy `plan_hash` của CHÍNH plan con rồi apply kèm
        # `--expected-plan-hash`. Bridge không thể biết trước hash đó (nó tất định theo NỘI DUNG chunk,
        # mà chunk vừa được vật chất hoá xong ở ngay trên), nên phải chèn lúc CHẠY. Fail ở DRY thì
        # dừng TRƯỚC mọi side-effect và trả nguyên kết quả DRY để chẩn được.
        r, _dry_fail = _bridge_run_child_apply({"planned_child_dry": list(rec["command_dry"]),
                                                "planned_child_command": _cmd})
        if _dry_fail is not None:
            r = {**r, "child_dry_result": _dry_fail}      # cùng tên khoá với `ocr.py` — một hợp đồng
        r.update({"chunk_index": rec.get("chunk_index"), "path": rec.get("path"), "expected_name": rec.get("expected_name")})
        results.append(r)
        print("[chunks-jsonl] " + json.dumps({"i": _i, "n": _n, "ok": bool(r.get("ok")),
                                              "name": rec.get("expected_name")}, ensure_ascii=False),
              file=sys.stderr, flush=True)
        if not r.get("ok") and not getattr(a, "continue_on_error", False):
            _resume_note = (f"Đứt ở chunk {_i}/{_n}. Chạy lại CÙNG LỆNH — child profile-ingest có dedup-gate "
                            f"(chunk đã lên bị chặn trùng, an toàn); hoặc thêm --continue-on-error để bỏ qua lỗi lẻ.")
            break
    out = {**plan, "schema": "chunk_ingest_bridge_apply.v1", "results": results,
           "ok": bool(results) and len(results) == _n and all(r.get("ok") for r in results)}
    if _resume_note:
        out["resume_command"] = _resume_note
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out.get("ok") else 2
