# -*- coding: utf-8 -*-
"""tl_core.fetch_web — I3 (v1.34.5): tách NGUYÊN VĂN cụm web-discovery/fetch từ scripts/tl.py
(fetch-route/batch/links, find-doc, tvpl-url, external-ingest, link-priority, frontier-expand + _fetch_plan/
_external_ingest_plan/_frontier_*). Hạ tầng discovery DÙNG CHUNG QT-5 (_query_variants/_google_site_url/
_discovery_links/_official_rank + _FETCH_SOURCES/_DISCOVERY_SITES/HOPNAP_FOLDER_ID) GIỮ Ở TL.
Hành vi khoá bởi r72a wiring-test (VBHN-first, dedup-action, markdown links)."""
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
import zipfile    # noqa: F401
from pathlib import Path  # noqa: F401

_TL = None


def bind(tl_module) -> None:
    """REBASE __globals__ từng hàm đã chuyển về namespace SỐNG của tl (khuôn I1/I2)."""
    global _TL
    _TL = tl_module
    import types
    g = globals()
    tg = tl_module.__dict__
    for _n, _fn in list(g.items()):
        if isinstance(_fn, types.FunctionType) and _fn.__module__ == __name__ and _n != "bind":
            _re = types.FunctionType(_fn.__code__, tg, _n, _fn.__defaults__, _fn.__closure__)
            _re.__kwdefaults__ = _fn.__kwdefaults__
            _re.__doc__ = _fn.__doc__
            _re.__module__ = __name__
            g[_n] = _re



def _external_ingest_plan(url: str, *, fmt: str = "", source_kind: str = "unknown", action: str = "discover",
                          cat: str = "", folder: str = "", notebook: str = "", name: str = "",
                          sohieu: str = "", year: str = "", trichyeu: str = "", convert: bool = True,
                          confirm: str = "") -> dict:
    """Pure guard for external/web/NLM-native ingest. Never mutates Drive/NLM."""
    action_l = (action or "discover").strip().lower().replace("-", "_")
    source_l = (source_kind or "unknown").strip().lower()
    fclass = _external_format_class(fmt, url)
    warnings, errors = [], []
    if action_l in {"research_import", "source_add", "source_add_url", "nlm_direct", "nlm_import"}:
        errors += ["DIRECT_NLM_IMPORT_FORBIDDEN", "RESEARCH_IMPORT_DISCOVERY_ONLY", "QT3_REQUIRED_BEFORE_NLM"]
    if _looks_like_new_target(notebook) or _looks_like_new_target(folder):
        errors.append("NEW_NOTEBOOK_OR_FOLDER_FORBIDDEN_BY_DEFAULT")
    if fclass == "pdf" and not convert:
        errors.append("PDF_RAW_NLM_FORBIDDEN_CONVERT_REQUIRED")
    if fclass == "pdf":
        warnings.append("PDF_ONLY_ALLOWED_AFTER_DRIVE_CONVERT_OR_TEXT_EXTRACTION")
    if source_l not in {"official", "primary", "gov", "chinhphu", "congbao", "vbpl"}:
        warnings.append("SOURCE_NOT_OFFICIAL_FIRST_REVIEW_REQUIRED")
    missing_surface = []
    for key, val in [("cat", cat), ("notebook", notebook), ("folder", folder), ("standard_name", name), ("sohieu", sohieu), ("trichyeu", trichyeu)]:
        if not (val or "").strip():
            missing_surface.append(key)
    if missing_surface:
        warnings.append("CONFIRM_SURFACE_INCOMPLETE:" + ",".join(missing_surface))
    if action_l not in {"discover", "discovery", "search", "qt3_plan"} and confirm != "yes":
        errors.append("CONFIRM_REQUIRED_WEB_INGEST_DESTINATION")
    steps = [
        "research_start/research_status chỉ dùng để phát hiện URL ứng viên; không research_import/source_add(url) làm bản dùng",
        "link tải cho người dùng ưu tiên TVPL → LuatVietnam → Công báo → official khác; canonical lưu/đối chiếu vẫn official-first",
        "chọn nguồn official-first; ưu tiên docx/GDoc-convertible; PDF chỉ dùng sau khi đưa về Drive và convert/extract text",
        "surface cho người dùng duyệt: URL, official/secondary, định dạng, cat, folder/notebook đích, tên chuẩn, số hiệu/năm/trích yếu",
        "Drive ingest/copy_convert → standardize_name → organize vào cat hiện hữu → verify list/manifest",
        "sau verify mới nlm_push vào notebook ĐANG DÙNG; không tạo notebook/folder mới trừ khi người dùng yêu cầu rõ",
    ]
    return {
        "ok": not errors,
        "gate": "EXTERNAL_INGEST_GATE",
        "action": action_l,
        "url": url,
        "format_class": fclass,
        "source_kind": source_kind or "unknown",
        "destination": {"cat": cat, "folder": folder or "CURRENT_CORPUS_FOLDER", "notebook": notebook or "CURRENT_NOTEBOOK", "standard_name": name},
        "metadata": {"sohieu": sohieu, "issue_year": year, "trichyeu": trichyeu},
        "warnings": warnings,
        "errors": errors,
        "required_steps": steps,
        "note": "Đồng ý tìm nguồn KHÁC đồng ý ghi vào corpus/NLM. Mọi thao tác ghi cần confirm riêng.",
    }


def cmd_external_ingest(a) -> int:
    out = _external_ingest_plan(
        a.url, fmt=a.format or "", source_kind=a.source_kind or "unknown", action=a.action,
        cat=a.cat or "", folder=a.folder or "", notebook=a.notebook or "", name=a.name or "",
        sohieu=a.sohieu or "", year=a.year or "", trichyeu=a.trichyeu or "", convert=not a.no_convert,
        confirm=a.confirm or "",
    )
    if a.json:
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"[{out['gate']}] ok={out['ok']} action={out['action']} format={out['format_class']} source={out['source_kind']}")
        for e in out["errors"]:
            print(f"ERROR: {e}")
        for w in out["warnings"]:
            print(f"WARN: {w}")
        print("Quy trình bắt buộc:")
        for i, st in enumerate(out["required_steps"], 1):
            print(f"  {i}) {st}")
        print(out["note"])
    return 0 if out.get("ok") else 2


def cmd_link_priority(a) -> int:
    out = {
        "rule": "TẢI FILE ưu tiên ĐỊNH DẠNG docx>doc>pdf ⇒ nguồn TVPL/LuatVietnam (docx) trước, official sau. CANONICAL/HIỆU-LỰC vẫn official-first (vbpl/Công báo). Auto-fetch: tl fetch-route/fetch-batch.",
        "format_priority": ["docx", "doc", "pdf"],
        "priority": ["thuvienphapluat.vn", "luatvietnam.vn", "vbpl.vn", "congbao.chinhphu.vn", "official_other", "other"],
        "links": _download_link_plan(a.urls or []),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2) if a.json else "\n".join(f"{x['rank']} {x['source']} {x['url']}" for x in out["links"]))
    return 0


def _frontier_candidates(classed: list, mapped_norm: set) -> list:
    """PURE (test offline): từ ref đã phân loại (_classify_ref) → ứng viên FRONTIER dedup theo số hiệu + ưu tiên
    (amending=1 > VBHN=2 > dẫn-chiếu=3). in_corpus = flag∈{OK,OUTDATED} & có canonical. KHÔNG đụng manifest/mạng."""
    seen, out = set(), []
    for c in classed:
        shn = norm_sohieu(c.get("sohieu") or "")
        if not shn or shn in seen:
            continue
        seen.add(shn)
        prio = 1 if shn in (mapped_norm or set()) else (2 if "VBHN" in shn.upper() else 3)
        in_corpus = c.get("flag") in ("OK", "OUTDATED") and bool(c.get("canonical"))
        out.append({"sohieu": c.get("sohieu"), "sohieu_norm": shn, "name_phrase": c.get("name_phrase", ""),
                    "flag": c.get("flag"), "in_corpus": in_corpus,
                    "canonical_sohieu": (c.get("canonical") or {}).get("sohieu"),
                    "source": "xref", "priority": prio})
    out.sort(key=lambda x: (x["priority"], x["sohieu_norm"]))
    return out


def _frontier_doc_text(a):
    """Đọc nội dung target cho frontier-expand: --text-file (offline) HOẶC <gdoc|sohieu> (deep-resolve → cache
    extract_<gid>.txt → exporttext). Trả (text, gid, name). text='' nếu không đọc được/entry thô."""
    if getattr(a, "text_file", None):
        try:
            return Path(a.text_file).read_text(encoding="utf-8", errors="replace"), None, a.text_file
        except Exception:
            return "", None, a.text_file
    target = getattr(a, "target", None)
    if not target:
        return "", None, ""
    gid, name = target, target
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
        _de, _dgid, _dname, _ = _resolve_deep_target(target, entries)
        if _de is not None:
            gid = _dgid or gid; name = _dname or name
    except Exception:
        pass
    if _is_raw_no_gdoc_name(name):
        return "", gid, name
    text = ""
    try:
        _cf = _cache_file(f"extract_{gid}.txt")
        if _cf.exists():
            _ct = _cf.read_text(encoding="utf-8", errors="replace")
            if _ct.strip():
                # r267 (P15 — đo 30-07): twin của `cmd_xref`; xem chú thích ở lookup_ops. Thiếu U1 ⇒
                # frontier-expand/rasoat-loop bóc thiếu dẫn chiếu trên CÙNG cache mà `_read_doc_text` bóc đủ.
                text = _sanitize_export_text(_strip_font_runs(_ct))
    except Exception:
        text = ""
    if not text:
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
            # A1 (v1.33.10): GWS-FIRST — _read_doc_text (cache→direct-media→transport→exporttext) thay vì
            # gọi thẳng exporttext (frontier-expand từng chết theo khi webapp thiếu scope).
            text = _read_doc_text(gid, getattr(a, "config", None))
        except Exception:
            text = ""
    return text, gid, name


def cmd_frontier_expand(a) -> int:
    """VÒNG LẶP RÀ SOÁT: trích MỌI văn bản được DẪN CHIẾU trong 1 văn bản (cross-ref + footnote sửa đổi + inline) →
    ứng viên FRONTIER (dedup số hiệu, ưu tiên amending>VBHN>dẫn-chiếu) + cờ in_corpus. DISCOVERY/REPORT-ONLY, KHÔNG RAG
    (mọi số hiệu/tên từ extract_refs/footnote). `missing_in_corpus` = ứng viên cần nạp (đầu vào `ingest-missing`/discovery).
    rc=0 (phát hiện ≠ lỗi); --strict → rc=1 nếu có missing. --text-file để chạy OFFLINE."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    text, gid, name = _frontier_doc_text(a)
    if not text:
        print("[tl] frontier-expand: chưa đọc được nội dung (cần <gdoc|sohieu> + gws/webapp, hoặc --text-file).", file=sys.stderr)
        return 2
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception:
        entries = []
    fnmap = resolve_footnote_amendments(text, entries=entries)
    mapped = {norm_sohieu(s) for s in fnmap.get("mapped_sohieu", [])}
    chain = mapped | {norm_sohieu(s) for s in fnmap.get("footnote_sohieu", [])} | {norm_sohieu(s) for s in fnmap.get("header_sohieu", [])}
    refs = extract_refs(text)
    classed = [_classify_ref(r, entries, {s.replace("/", "-") for s in chain}) for r in refs]
    frontier = _frontier_candidates(classed, mapped)
    seen = {f["sohieu_norm"] for f in frontier}
    for s in sorted(mapped):                       # luật SỬA base từ footnote (có thể không nằm trong refs trực tiếp)
        if s and s not in seen:
            seen.add(s)
            present = any(_sohieu_query_hits_entry(s, norm_sohieu(_entry_sohieu(e)))
                          or _sohieu_query_hits_entry(s, _sohieu_key_entry(e)) for e in entries)   # v1.33.47: +bare-VBHN
            frontier.append({"sohieu": s, "sohieu_norm": s, "name_phrase": "", "flag": "OK" if present else "MISSING",
                             "in_corpus": present, "canonical_sohieu": s if present else None,
                             "source": "footnote", "priority": 1})
    frontier.sort(key=lambda x: (x["priority"], x["sohieu_norm"]))
    try:
        inline = _scan_inline_amendments(text) or []
    except Exception:
        inline = []
    missing = [f["sohieu"] for f in frontier if not f["in_corpus"]]
    out = {"ok": True, "gate": "frontier-expand", "base": name, "drive_id": gid, "refs_found": len(refs),
           "frontier_count": len(frontier), "missing_in_corpus": missing, "inline_amendment_count": len(inline),
           "frontier": frontier}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== frontier-expand {name[:38]} · {len(frontier)} ứng viên · {len(missing)} THIẾU corpus ==")
        for f in frontier:
            mk = "·" if f["in_corpus"] else "✗"
            print(f"  {mk} [P{f['priority']}] {f['sohieu']:18s} {(f.get('name_phrase') or '')[:26]:26s} {f['flag']}"
                  + (f" → {f['canonical_sohieu']}" if f.get("canonical_sohieu") else ""))
        if missing:
            print(f"  THIẾU (đầu vào ingest-missing): {', '.join(missing[:12])}")
    return 1 if (getattr(a, "strict", False) and missing) else 0


def cmd_tvpl_url(a) -> int:
    """Dựng URL tìm kiếm TVPL + in luồng auto-download (Claude Code/Cowork + Claude in Chrome đã login VIP).
    Bước Chrome do agent điều khiển; tl lo bước tìm-URL + (sau khi tải) ingest. KHÔNG nhập mật khẩu hộ."""
    import urllib.parse as _up
    q = (getattr(a, "sohieu", None) or getattr(a, "query", None) or "").strip()
    if not q:
        print("[tl] tvpl-url cần <số hiệu>|--query", file=sys.stderr); return 2
    out = {
        "ok": True, "sohieu": q,
        "search_url": "https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=" + _up.quote(q),
        "flow_claude_code": [
            "1. Claude in Chrome (Browser đã ĐĂNG NHẬP TVPL VIP): navigate search_url → mở đúng trang /van-ban/ theo số hiệu.",
            "2. Click tab 'Tải về' → link 'Tải Văn bản tiếng Việt (docx)' → file về ~/Downloads (HỎI người dùng trước khi tải).",
            "3. Bash: lấy *.docx mới nhất trong ~/Downloads (vd: ls -t ~/Downloads/*.docx | head -1).",
            "4. Upload Drive _HOP_NAP: Drive MCP create_file (contentMimeType docx → convert GDoc) HOẶC webapp importext.",
            "5. Chuẩn hóa tên → move cat → tl preflight <số hiệu> → source_add (VBQPPL-2 nếu base đầy) → tl push-overflow → verify.",
        ],
        "note": "TVPL chặn fetch server-side (403/CORS) → CHỈ trình duyệt đã đăng nhập tải được. Mật khẩu do người dùng tự nhập (không nhập hộ).",
    }
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0


def _fetch_plan(q: str) -> list:
    """PURE: kế hoạch nguồn tải đã xếp theo ưu tiên FORMAT (docx>doc>pdf) → TVPL/LVN trước, official sau.
    DISCOVERY: ưu tiên Google `site:` (tốt hơn search nội bộ) → ra ĐÚNG trang văn bản; kèm search nội bộ làm phụ.
    Mỗi nguồn kèm biến thể truy vấn VBHN-first (hợp nhất → mới nhất → gốc)."""
    import urllib.parse as _up
    variants = _query_variants(q)
    rows = []
    for s in _FETCH_SOURCES:
        internal = [s["search"].replace("{q}", _up.quote(v) if ("keyword=" in s["search"] or "keywords=" in s["search"]) else v)
                    for v in variants]
        google = [_google_site_url(v, s["source"]) for v in variants]
        rows.append({"source": s["source"], "expected_format": s["fmt"], "fmt_rank": _FMT_RANK[s["fmt"]],
                     "login_required": s["login"], "quota_limited": s["quota"], "free": not s["login"],
                     "discover": "google_site",  # cách tìm khuyến nghị
                     "google_search": google[0], "google_search_variants": google,
                     "internal_search": internal[0], "internal_search_variants": internal, "recipe": s["recipe"]})
    rows.sort(key=lambda r: (r["fmt_rank"], 0 if r["login_required"] else 1))  # docx trước; cùng format ưu tiên nguồn docx
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return {"query_variants": variants, "google_global": _google_site_url(variants[0]), "sources": rows}


def cmd_fetch_route(a) -> int:
    """RESOLVE + DEDUP + kế hoạch tải official-first (ưu tiên docx>doc>pdf). Advisory — không tải.
    F9 (r192, đề xuất #9 — khuôn 10b nổi hơn): «phê duyệt nạp theo skill ≠ phê duyệt TỰ TẢI nguồn gated»
    ⇒ MẶC ĐỊNH dừng ở LINK BẤM-ĐƯỢC cho người dùng tự tải (khuôn C2(b) của fetch-links); recipe TỰ TẢI
    (fetch_plan cho agent chạy Chrome) CHỈ xuất khi có cờ tường minh --auto-download-approved — người vận
    hành gõ SAU khi người dùng đồng ý trong phiên, không bao giờ là mặc định."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    q = (getattr(a, "query", None) or getattr(a, "sohieu", None) or "").strip()
    if not q:
        print("[tl] fetch-route cần <số hiệu|tên>", file=sys.stderr); return 2
    dedup, _ = _dedup_status(q)
    plan = _fetch_plan(q)
    if not getattr(a, "auto_download_approved", False):
        dl_md = []
        for s in plan["sources"]:
            gurl = (s.get("google_search_variants") or [plan["google_global"]])[0]
            dl_md.append(f"- [Tải .{s['expected_format']} {q} — {s['source']} (cần đăng nhập)]({gurl})")
        dl_md.append(f"- [Tìm toàn cục (Google) — “{plan['query_variants'][0]}”]({plan['google_global']})")
        out = {"ok": True, "query": q, "dedup": dedup, "mode": "ask_first_links",
               "download_links_markdown": dl_md, "upload_link_markdown": _hopnap_upload_md(),
               "note": ("F9/10b HỎI TRƯỚC: đưa link bấm-được cho NGƯỜI DÙNG tự tải (nguồn gated cần đăng "
                        "nhập); muốn agent TỰ tải phải hỏi người dùng trong phiên rồi chạy lại với "
                        "--auto-download-approved. in_corpus_active=true ⇒ dedup, chỉ tải nếu cần bản mới hơn.")}
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
        return 0
    out = {"ok": True, "query": q, "dedup": dedup, "mode": "auto_fetch_plan", "fetch_plan": plan,
           "note": ("FORMAT docx>doc>pdf ⇒ TVPL/LuatVietnam (docx) trước → vbpl (doc) → Công báo (pdf). "
                    "Official (vbpl) để xác minh BẢN ĐÚNG + HIỆU-LỰC. in_corpus_active=true ⇒ dedup, chỉ tải nếu cần bản mới hơn.")}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0


def cmd_fetch_batch(a) -> int:
    """Điều phối danh sách: dedup + kế hoạch tải/route + checkpoint cuốn chiếu. DRY mặc định (không tải).
    Bước tải thật do agent chạy qua Chrome (throttle ~--delay + jitter, concurrency 1)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    items = list(getattr(a, "items", None) or [])
    if getattr(a, "file", None):
        items += [ln.strip() for ln in Path(a.file).read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]
    if not items:
        print("[tl] fetch-batch cần <số hiệu...> hoặc --file", file=sys.stderr); return 2
    plan = []
    for q in items:
        dedup, _ = _dedup_status(q)
        if dedup.get("in_corpus_active"):
            action = "SKIP_DEDUP"          # khớp số hiệu → chắc chắn đã có
        elif dedup.get("likely_in_corpus"):
            action = "REVIEW_DEDUP"        # khớp tên → khả năng đã có, xác nhận số hiệu trước khi tải
        else:
            action = "FETCH"
        plan.append({"query": q, "in_corpus_active": dedup.get("in_corpus_active"),
                     "likely_in_corpus": dedup.get("likely_in_corpus"), "action": action,
                     "dedup_hits": dedup.get("hits", [])[:2],
                     "fetch_plan": _fetch_plan(q) if action != "SKIP_DEDUP" else None})
    ckpt = {"version": VERSION, "delay": getattr(a, "delay", 4), "jitter": getattr(a, "jitter", 2),
            "concurrency": 1, "total": len(plan), "to_fetch": sum(1 for p in plan if p["action"] == "FETCH"),
            "review": sum(1 for p in plan if p["action"] == "REVIEW_DEDUP"),
            "skip_dedup": sum(1 for p in plan if p["action"] == "SKIP_DEDUP"), "items": plan}
    cf = _cache_file("fetch_queue.json")
    try:
        cf.parent.mkdir(parents=True, exist_ok=True); cf.write_text(json.dumps(ckpt, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
    if getattr(a, "json", False):
        print(json.dumps(ckpt, ensure_ascii=False, indent=2))
    else:
        print(f"== fetch-batch (DRY) · {ckpt['total']} mục · FETCH={ckpt['to_fetch']} · REVIEW={ckpt['review']} · SKIP_DEDUP={ckpt['skip_dedup']} · throttle {ckpt['delay']}s+jitter{ckpt['jitter']} ==")
        for p in plan:
            srcs = (p["fetch_plan"] or {}).get("sources") if p["fetch_plan"] else None
            top = (srcs[0]["source"] + "→" + srcs[0]["expected_format"]) if srcs else "—"
            print(f"  [{p['action']:11s}] {p['query']:22s} nguồn ưu tiên: {top}")
        print(f"checkpoint: {cf}")
    return 0


def cmd_fetch_links(a) -> int:
    """MANUAL/C2(b): trả LINK markdown BẤM-ĐƯỢC để NGƯỜI DÙNG tự qua login-gate tải docx + link _HOP_NAP để tải lên.
    C4: nhãn '[Tải .docx <số hiệu> — <nguồn> (cần đăng nhập)](url)'; KHÔNG in URL trần. VBHN-first ('hợp nhất'). C3: env-aware."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    q = (getattr(a, "query", None) or getattr(a, "sohieu", None) or "").strip()
    if not q:
        print("[tl] fetch-links cần <số hiệu|tên>", file=sys.stderr); return 2
    env = _runtime_env(getattr(a, "env", None))
    dedup, _ = _dedup_status(q)
    plan = _fetch_plan(q)
    variants = plan["query_variants"]
    # DOWNLOAD: ưu tiên nguồn gated docx (TVPL/LuatVietnam) — discovery qua Google site: (search nội bộ kém) → trang văn bản.
    dl_md = []
    for s in plan["sources"]:
        gurl = (s.get("google_search_variants") or [plan["google_global"]])[0]   # variant[0] = '... hợp nhất'
        dl_md.append(f"- [Tải .{s['expected_format']} {q} — {s['source']} (cần đăng nhập)]({gurl})")
    dl_md.append(f"- [Tìm toàn cục (Google) — “{variants[0]}”]({plan['google_global']})")
    up_md = _hopnap_upload_md()
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "query": q, "runtime_env": env, "query_variants": variants, "discover": "google_site",
                          "dedup": {"in_corpus_active": dedup.get("in_corpus_active"), "likely_in_corpus": dedup.get("likely_in_corpus")},
                          "download_links_markdown": dl_md, "upload_link_markdown": up_md,
                          "hopnap_folder_id": HOPNAP_FOLDER_ID,
                          "ask_first": env in ("code", "cowork")}, ensure_ascii=False, indent=2))
    else:
        if dedup.get("in_corpus_active") or dedup.get("likely_in_corpus"):
            print(f"[lưu ý] '{q}' có thể ĐÃ trong corpus (dedup) — kiểm tra trước khi tải lại.")
        if env in ("code", "cowork"):
            print(f"[env={env}] C2(a): HỎI người dùng \"Bạn có muốn tôi tự động tải các file này về không?\" trước khi tự tải.")
            print("  Nếu người dùng muốn tự làm → dùng các link bấm-được dưới đây (nhánh C2(b)).")
        print(f"① Link TẢI XUỐNG (qua login-gate, ưu tiên .docx · VBHN-first) cho '{q}':")
        print("\n".join(dl_md))
        print("② Link TẢI LÊN (thả file .docx đã tải vào Drive):")
        print(up_md)
        print("(Sau khi tải lên _HOP_NAP → chạy `tl ingest-local` để convert/đặt tên/cat/register/nlm-add.)")
    return 0


def cmd_find_doc(a) -> int:
    """Primitive TÌM VĂN BẢN trên web = Google `site:` + VBHN-first (dùng chung; thay search nội bộ kém).
    Khác fetch-links (thiên về tải): find-doc để ĐỊNH VỊ/tra cứu nhanh trang văn bản trên mọi nguồn."""
    q = (getattr(a, "query", None) or getattr(a, "sohieu", None) or "").strip()
    if not q:
        print("[tl] find-doc cần <số hiệu|tên>", file=sys.stderr); return 2
    d = _discovery_links(q)
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "query": q, **d}, ensure_ascii=False, indent=2))
    else:
        print(f"Tìm '{q}' qua GOOGLE site: (VBHN-first — thử 'hợp nhất' trước):")
        print("\n".join(d["links_markdown"]))
    return 0

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


def _external_format_class(fmt: str | None, url: str | None = None) -> str:
    raw = (fmt or "").strip().lower()
    u = (url or "").lower()
    if not raw:
        for ext in (".docx", ".doc", ".rtf", ".odt", ".pdf", ".html", ".htm"):
            if ext in u.split("?")[0]:
                raw = ext.lstrip(".")
                break
    if raw in {"gdoc", "google-doc", "google_docs", "google doc"}:
        return "gdoc"
    if raw in {"docx", "doc", "rtf", "odt"}:
        return "docx_convertible"
    if raw == "pdf":
        return "pdf"
    if raw in {"html", "htm", "text", "txt"}:
        return "text_html"
    return raw or "unknown"

def extract_refs(text: str) -> list:
    """Bóc các viện dẫn 'Luật/Bộ luật/… [số hiệu]' trong thân + footnote. NFC-normalize trước.
    Trả [{raw, name_phrase, sohieu, loai}] — DEDUP theo SỐ HIỆU (P1-3: MỘT phán quyết / số hiệu / run; B: hết
    'phantom' 1 số hiệu xuất hiện 2-3 lần do mệnh đề chuyển tiếp). name_phrase đã cắt prose; giữ bản SẠCH nhất."""
    txt = unicodedata.normalize("NFC", text or "")
    by_sh: dict[str, dict] = {}
    for m in _REF_RE.finditer(txt):
        sh = norm_sohieu(m.group("sh"))
        if not sh:
            continue
        name = _clean_ref_name_phrase((m.group("name") or "").strip(" -–—\t"))
        rec = {"raw": m.group(0).strip()[:90], "name_phrase": name, "sohieu": sh,
               "loai": (m.group("loai") or "").strip()}
        prev = by_sh.get(sh)
        # Giữ MỘT bản / số hiệu: ưu tiên bản có name_phrase (sau khi cắt prose) hơn bản rỗng; giữa 2 tên → bản ĐẦU.
        if prev is None or (not prev.get("name_phrase") and rec["name_phrase"]):
            by_sh[sh] = rec
    return list(by_sh.values())

def _query_variants(q: str) -> list:
    """VBHN-FIRST: với truy vấn theo TÊN luật → thử '<tên> hợp nhất' TRƯỚC, rồi '<tên> mới nhất', rồi tên gốc.
    Truy vấn theo SỐ HIỆU → tìm thẳng số (không thêm keyword)."""
    if _looks_like_sohieu_query(q):
        return [q]
    ql = _strip_accents(q).lower()
    if "hop nhat" in ql or "moi nhat" in ql:
        return [q]                     # người dùng đã nêu rõ → tôn trọng nguyên trạng
    return [f"{q} hợp nhất", f"{q} mới nhất", q]   # VBHN-first

def _google_site_url(query: str, site: str | None = None) -> str:
    """Google search URL (ưu tiên dùng Google vì search nội bộ TVPL/LVN kém). site=None → Google toàn cục."""
    import urllib.parse as _up
    q = f"site:{site} {query}" if site else query
    return "https://www.google.com/search?q=" + _up.quote(q)

def _runtime_env(override: str | None = None) -> str:
    """C3: RUNTIME_ENV ∈ {code, cowork, chat}. Heuristic env-var; KHÔNG chắc → 'chat' (an toàn = đưa link, không tự tải)."""
    v = (override or "").strip().lower()
    if v in ("code", "cowork", "chat"):
        return v
    import os
    ev = (os.environ.get("TL_RUNTIME_ENV") or "").strip().lower()
    if ev in ("code", "cowork", "chat"):
        return ev
    if os.environ.get("CLAUDE_COWORK") or os.environ.get("COWORK"):
        return "cowork"
    if os.environ.get("CLAUDECODE") or os.environ.get("CLAUDE_CODE_ENTRYPOINT") or os.environ.get("CLAUDE_CODE"):
        return "code"
    return "chat"   # mặc định an toàn (C3)
