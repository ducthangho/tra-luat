# -*- coding: utf-8 -*-
"""tl_core.doc_identity — A2 (v1.34.63, kế hoạch `ke-hoach-dedup-corpus-B1-2026-07-18.md` ADR-A2-1..4):
module IDENTITY NỘI DUNG dùng chung — 1 NGUỒN SỰ THẬT cho so-cặp văn bản (`tl doc-compare`) và engine
dedup trục nội dung (`tl dedup-corpus` — B1 gọi CÙNG helper, KHÔNG copy). Nền tảng từ nỗi đau data-op
2026-07-16 (~10 script tay: content-hash 2 GDoc, bow-Jaccard 155-2018 _v2 0.983 / 25-2021 _MyPham 0.992).

Recipe (ADR-A2-2): content-hash = NFC + `_strip_font_runs` + lowercase + gộp whitespace — GIỮ DẤU + DẤU
CÂU (không strip accents; bản mất-dấu là việc C-#9, không phải identity). BoW = tách `\\w+` trên text đã
norm (GIỮ dấu, bỏ dấu câu). Ngưỡng NEAR T=0.95 mặc định (`--near-threshold`) = ngưỡng chung dải NEAR B1.
Verdict: IDENTICAL (md5 bytes HOẶC content-hash — cả hai đòi giá trị KHÔNG rỗng, fail-closed) / NEAR
(jaccard ≥ T, không exact) / DIFFERENT. `_compare_signals` có `sohieu_differs` = RAW SIGNAL mislabel —
A2 KHÔNG kết luận tên nào đúng (content-verify là việc B1 ADR-3).

CLI `tl doc-compare <a> <b>` (ADR-A2-4): input auto-detect drive_id | sohieu | name | LOCAL-PATH
(file tồn tại → local = pre-ingest dedup check, bất biến #5 — KHÔNG cần manifest/boot); NLM-ĐỘC-LẬP
(không đụng notebooklm); đọc text qua `_doc_text_any` (A1 v1.34.60). Hàm rebase lên namespace tl (khuôn
I1/I2) — import dưới chỉ để đọc-hiểu tĩnh."""
from __future__ import annotations

import hashlib      # noqa: F401
import json         # noqa: F401
import os           # noqa: F401
import re           # noqa: F401
import sys          # noqa: F401
import unicodedata  # noqa: F401
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


def _doc_norm(text: str) -> str:
    """ADR-A2-2: chuẩn hóa content-identity — NFC → lọc dòng font-run (tái dùng `_strip_font_runs`, KHÔNG
    viết lại) → lowercase → gộp whitespace/newline. GIỮ dấu tiếng Việt + dấu câu (khác `_strip_accents`
    của lớp classify — identity so NGUYÊN VĂN, chỉ bỏ nhiễu trình bày)."""
    s = unicodedata.normalize("NFC", str(text or ""))
    s = _strip_font_runs(s)
    s = s.lower()
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\s*\n\s*", "\n", s)
    return s.strip()


def _content_hash(text: str) -> str:
    """sha256 của `_doc_norm(text)` — bắt dup khi md5 bytes KHÁC (2 GDoc convert) nhưng text hệt.
    Rỗng (sau norm) → '' — KHÔNG trả sha-của-rỗng để 2 bản không-đọc-được không giả 'identical' (fail-closed)."""
    n = _doc_norm(text)
    return hashlib.sha256(n.encode("utf-8")).hexdigest() if n else ""


def _bow_tokens(text) -> set:
    """Tập từ bag-of-words trên text đã `_doc_norm` — GIỮ dấu ('được' ≠ 'duoc'), bỏ dấu câu (\\w+).
    Loại nhiễu rsid/markup đã xử ở tầng đọc (docx unzip strip-tag)."""
    if isinstance(text, (set, frozenset)):
        return set(text)
    return set(re.findall(r"\w+", _doc_norm(text)))


def _bow_jaccard(a, b) -> float:
    """|A∩B| / |A∪B| trên tập từ (nhận str HOẶC set token đã tính sẵn — B1 cache bow theo did).
    Một trong hai rỗng → 0.0 (không giả NEAR trên text không đọc được)."""
    ta, tb = _bow_tokens(a), _bow_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def _sohieu_cmp_key(sohieu) -> str:
    """Khóa so sánh số hiệu (khuôn `_sohieu_key_entry`): norm_sohieu trên chuỗi đã đổi _ → -."""
    s = str(sohieu or "").strip()
    return norm_sohieu(s.replace("_", "-")) if s else ""


def _compare_signals(text_a, text_b, *, md5_a=None, md5_b=None, type_a=None, type_b=None,
                     sohieu_a=None, sohieu_b=None, T=0.95) -> dict:
    """ADR-A2-3: gom ĐỦ tín hiệu so-cặp → verdict. md5 (bytes, tin cả khi text rỗng) → content-hash
    (đòi CẢ HAI text không rỗng) → jaccard ≥ T → NEAR; còn lại DIFFERENT. `same_type`=None khi thiếu
    type (không đoán); `sohieu_differs` = raw signal (A2 KHÔNG kết luận tên đúng — việc B1 ADR-3)."""
    try:
        T = float(T) if T is not None else 0.95
    except (TypeError, ValueError):
        T = 0.95
    ta, tb = str(text_a or ""), str(text_b or "")
    md5_same = bool(md5_a and md5_b and str(md5_a) == str(md5_b))
    ha, hb = _content_hash(ta), _content_hash(tb)
    content_hash_same = bool(ha and hb and ha == hb)
    jac = round(_bow_jaccard(ta, tb), 4)
    same_type = (None if not (type_a and type_b) else str(type_a) == str(type_b))
    ka, kb = _sohieu_cmp_key(sohieu_a), _sohieu_cmp_key(sohieu_b)
    if md5_same or content_hash_same:
        verdict = "IDENTICAL"
    elif jac >= T:
        verdict = "NEAR"
    else:
        verdict = "DIFFERENT"
    return {"md5_same": md5_same, "content_hash_same": content_hash_same, "jaccard": jac,
            "same_type": same_type, "type_a": type_a or "", "type_b": type_b or "",
            "sohieu_a": str(sohieu_a or ""), "sohieu_b": str(sohieu_b or ""),
            "sohieu_differs": bool(ka and kb and ka != kb),
            "verdict": verdict, "threshold": T,
            "chars_a": len(ta), "chars_b": len(tb)}


def _doc_type_kind(mime: str, name: str) -> str:
    """Type cho định-nghĩa-trùng ADR-2 (2 GDoc | 2 docx CÙNG TYPE mới là dup; docx-gốc + GDoc-convert
    KHÔNG dup): gdoc | docx | pdf | txt | '' (không rõ — không đoán). Mirror route của `_doc_text_any`."""
    m, n = str(mime or "").lower(), str(name or "").lower()
    if "google-apps" in m:
        return "gdoc"
    if "wordprocessingml" in m or n.endswith(".docx"):
        return "docx"
    if "pdf" in m or n.endswith(".pdf"):
        return "pdf"
    if n.endswith((".txt", ".md")):
        return "txt"
    return ""


def _doc_compare_resolve(ref: str, entries) -> dict | None:
    """ADR-A2-4 auto-detect: file-tồn-tại → local (pre-ingest, không cần manifest); ~20+ ký tự dạng id
    Drive → drive_id (khớp exact manifest lấy metadata, id thật LUÔN thắng — bài học A.1 v1.34.40);
    còn lại → resolve sohieu exact (`_source_find`) rồi deep-resolve tên. Không ra → None (fail-closed)."""
    r = str(ref or "").strip()
    if not r:
        return None
    if os.path.isfile(r):
        p = Path(r)
        try:
            _b = p.read_bytes()
            _md5 = hashlib.md5(_b).hexdigest()
        except Exception:  # noqa: BLE001 — đọc được text vẫn so được (md5 chỉ là 1 tín hiệu)
            _md5 = ""
        return {"kind": "local", "id": str(p), "name": p.name,
                "sohieu": _parse_sohieu_from_name(p.name) or "",
                "md5": _md5, "type": _doc_type_kind("", p.name), "entry": None}
    ents = list(entries or [])
    if re.fullmatch(r"[A-Za-z0-9_\-]{20,}", r):
        e = next((x for x in ents if str(_entry_drive_id(x) or "").strip() == r), None)
        if e is None:
            return {"kind": "drive", "id": r, "name": "", "sohieu": "", "md5": "", "type": "", "entry": None}
    else:
        e = _source_find(ents, r)
        if e is None:
            try:
                e, _did, _nm, _hits = _resolve_deep_target(r, ents)
            except Exception:  # noqa: BLE001 — resolver lỗi = không resolve được, fail-closed phía dưới
                e = None
        if e is None:
            return None
    name = _entry_name(e)
    return {"kind": "drive", "id": _entry_drive_id(e), "name": name,
            "sohieu": _entry_sohieu(e) or _parse_sohieu_from_name(name) or "",
            "md5": _entry_md5(e), "type": _doc_type_kind(str(e.get("mime") or ""), name), "entry": e}


def _doc_compare_read(res: dict, *, refresh: bool = False) -> tuple:
    """Đọc text theo resolve: local docx → `_docx_unzip_text` (text THẬT — hết footgun binary);
    local pdf/txt/md → `_read_local_text_for_analysis`; drive → `_doc_text_any` (A1, cache extract).
    Trả (text, source) — fail → ('', '')."""
    if not res:
        return "", ""
    if res.get("kind") == "local":
        p = Path(res["id"])
        t = ""
        if res.get("type") == "docx":
            t = _docx_unzip_text(p)
        else:
            try:
                t, _w = _read_local_text_for_analysis(p)
            except Exception:  # noqa: BLE001 — không đọc được → fail-closed phía caller
                t = ""
        return (_strip_font_runs(t), "local") if t else ("", "")
    return _doc_text_any(res["id"], entry=res.get("entry"), refresh=refresh)


def cmd_doc_compare(a) -> int:
    """A2 (v1.34.63): `tl doc-compare <a> <b>` — CLI MỎNG gọi `_compare_signals` (1 nguồn sự thật, B1 dùng
    chung). NLM-độc-lập; rc=0 cho MỌI verdict (IDENTICAL/NEAR/DIFFERENT); rc=2 CHỈ khi input không resolve
    /không đọc được text (fail-closed, không đoán). local×local chạy KHÔNG cần manifest (pre-ingest)."""
    try:   # lazy-creds offline-first (khuôn doc-text A1): cache/local chạy không token; export tự lo cred
        apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    except (SystemExit, Exception):  # noqa: BLE001
        pass
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (SystemExit, Exception):  # noqa: BLE001
        pass
    ra, rb = str(getattr(a, "ref_a", "") or "").strip(), str(getattr(a, "ref_b", "") or "").strip()
    if not ra or not rb:
        print(json.dumps({"ok": False, "error": "NEED_TWO_REFS",
                          "note": "doc-compare cần <a> <b> = drive_id | sohieu | name | local-path."},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    entries = []
    if not (os.path.isfile(ra) and os.path.isfile(rb)):   # local×local: KHÔNG đụng manifest (offline thuần)
        try:
            entries = _manifest_entries(refresh=getattr(a, "refresh", False))
        except Exception as e:  # noqa: BLE001
            print(json.dumps({"ok": False, "error": "MANIFEST_UNAVAILABLE", "detail": str(e)[:200],
                              "note": "resolve drive_id/sohieu/name cần manifest — chạy `tl boot` trước "
                                      "(local-path × local-path thì không cần)."},
                             ensure_ascii=False), file=sys.stderr)
            return 2
    A = _doc_compare_resolve(ra, entries)
    B = _doc_compare_resolve(rb, entries)
    for _ref, _res in ((ra, A), (rb, B)):
        if _res is None:
            print(json.dumps({"ok": False, "error": "RESOLVE_FAILED", "ref": _ref,
                              "note": "không khớp drive_id/sohieu/name nào trong manifest và không phải "
                                      "file local — kiểm chính tả hoặc `tl boot --refresh`."},
                             ensure_ascii=False), file=sys.stderr)
            return 2
    ta, sa = _doc_compare_read(A, refresh=getattr(a, "refresh", False))
    tb, sb = _doc_compare_read(B, refresh=getattr(a, "refresh", False))
    md5_pair = bool(A["md5"] and B["md5"] and A["md5"] == B["md5"])
    if (not ta or not tb) and not md5_pair:   # md5 bytes hệt → vẫn verdict được dù text kẹt
        print(json.dumps({"ok": False, "error": "TEXT_UNAVAILABLE",
                          "side": [r for r, t in (("a", ta), ("b", tb)) if not t],
                          "note": "không đọc được text (GDoc-export/docx-unzip/pdftotext) — kiểm quyền/"
                                  "định dạng bằng `tl doc-text <id>`."}, ensure_ascii=False), file=sys.stderr)
        return 2
    sig = _compare_signals(ta, tb, md5_a=A["md5"] or None, md5_b=B["md5"] or None,
                           type_a=A["type"] or None, type_b=B["type"] or None,
                           sohieu_a=A["sohieu"] or None, sohieu_b=B["sohieu"] or None,
                           T=getattr(a, "near_threshold", 0.95))
    env = {"ok": True, "schema": "doc_compare.v1",
           "a": {"kind": A["kind"], "id": A["id"], "name": A["name"], "sohieu": A["sohieu"],
                 "type": A["type"], "source": sa},
           "b": {"kind": B["kind"], "id": B["id"], "name": B["name"], "sohieu": B["sohieu"],
                 "type": B["type"], "source": sb},
           **sig, "nlm_independent": True}
    if not ta or not tb:
        env["flags"] = ["TEXT_UNAVAILABLE_MD5_ONLY"]   # verdict dựa bytes; text để trống — không đoán
    _out = getattr(a, "out", None)
    body = _json_dumps(env, deterministic=_deterministic_enabled(a))
    if _out:
        Path(_out).write_text(body + "\n", encoding="utf-8")
        print(f"[tl] doc-compare → {_out} (verdict={env['verdict']})")
        return 0
    if getattr(a, "json", False):
        print(body)
        return 0
    print(f"== doc-compare: {env['verdict']} (jaccard={env['jaccard']}, md5_same={env['md5_same']}, "
          f"content_hash_same={env['content_hash_same']}, same_type={env['same_type']}) ==")
    print(f"  a: [{A['kind']}] {A['name'] or A['id']} | sohieu={A['sohieu'] or '∅'} | type={A['type'] or '?'} | via {sa}")
    print(f"  b: [{B['kind']}] {B['name'] or B['id']} | sohieu={B['sohieu'] or '∅'} | type={B['type'] or '?'} | via {sb}")
    if env.get("sohieu_differs"):
        print("  ⚠ sohieu_differs=true — cùng nội dung nhưng số hiệu đăng ký khác (raw signal; "
              "phân xử tên đúng: `tl dedup-corpus` content-verify).")
    return 0
