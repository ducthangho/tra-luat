# -*- coding: utf-8 -*-
"""tl_core.extract_cache — I3 (v1.34.5): tách NGUYÊN VĂN 3 lệnh đọc-nguyên-văn/cache từ scripts/tl.py
(cmd_extract / cmd_cache_build / cmd_cache_snapshot). Hạ tầng đọc DÙNG CHUNG (_read_doc_text/_cache_file/
_title_block_from_text/extract_dieu/extract_refs/_sanitize_export_text/_profile_cache_dir…) GIỮ Ở TL —
ranh giới đo bằng đếm-tham-chiếu-ngoài-cụm (16/13/6… call-site). Hành vi khoá bởi r72a wiring-test."""
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



def _extract_resolve_entries(a) -> list:
    """r180 S3: tập entries cho resolve --sohieu của extract — dưới PROFILE thì ĐỌC CỘNG NỀN vbqppl
    (mirror base-also của reg-query; doctrine «Nền VBQPPL luôn bật»). Profile trước, nền bổ sung,
    dedup drive_id, hit nền mang scope='vbqppl' (_merge_base_entries). Hố phiên vận hành 21-07:
    `extract 52-2025-VPQH --profile "Luật BHXH"` fail dù dòng nền đang sống."""
    ents = _manifest_entries(refresh=getattr(a, "refresh", False))
    if _active_profile() != DEFAULT_PROFILE and _base_also_enabled(a):
        try:
            _b, _berr = _base_manifest_entries(getattr(a, "config", None))
            ents = _merge_base_entries(ents, _b or [])
            if _berr:
                print(f"[tl] ⚠ base-also (extract): manifest nền có lỗi ({_berr}) — hit nền có thể thiếu.",
                      file=sys.stderr)
        except Exception as _be:  # noqa: BLE001 — nền hỏng thì resolve trên profile, KHÔNG nuốt im lặng
            print(f"[tl] ⚠ base-also (extract): không đọc được manifest nền ({_be}) — resolve trên profile.",
                  file=sys.stderr)
    return ents


def cmd_extract(a) -> int:
    """B2 token-saving: exporttext ra ĐĨA → regex Điều → in đúng Điều.
    Có thể truyền GDoc id trực tiếp hoặc `--sohieu` để tự chọn canonical từ manifest."""
    gdoc_id = a.gdoc_id
    _extract_canon = None
    # A1 (false-404): positional KHÔNG phải gdoc-id thật (id Drive ≥20 ký tự alnum) → coi như SỐ HIỆU/tên, định tuyến --sohieu.
    # `tl extract 109-2025-QH15` trước báo "File not found: 109-2025-QH15"; nay tự resolve canonical từ manifest.
    if gdoc_id and not re.fullmatch(r"[A-Za-z0-9_\-]{20,}", gdoc_id):
        a.sohieu = a.sohieu or gdoc_id
        gdoc_id = None
    # Review v70: truyền CẢ positional id-shaped LẪN --sohieu → ƯU TIÊN --sohieu (ý định rõ); bỏ positional để
    # path --sohieu chạy (trước đây positional 'che' --sohieu → --sohieu không bao giờ được resolve).
    if gdoc_id and a.sohieu:
        print(f"[tl] có cả positional '{gdoc_id[:14]}…' lẫn --sohieu '{a.sohieu}' → dùng --sohieu.", file=sys.stderr)
        gdoc_id = None
    # v1.34.40 A.1 (log Chỉ thị — extract TRẢ SAI VĂN BẢN im lặng, ca PL01): positional DẠNG-ID KHÔNG deep-resolve
    # trước export nữa — id thật LUÔN thắng (resolver cũ coi id hợp lệ như query fuzzy → ghi đè id → export nhầm
    # văn bản khác + cache bẩn, mà rc=0). Trước export CHỈ tra EXACT drive_id trong manifest lấy metadata
    # (draft-warning + sohieu cho cache consolidated) — exact-match tất định, không bao giờ đổi id.
    # Ca tên-giống-id (false-404 cũ 'Luat_113-2025-QH15_Dan_so') xử SAU: export NOT_FOUND → deep-resolve fallback.
    _id_positional = bool(gdoc_id and not a.sohieu)
    if _id_positional:
        try:
            _ents = _manifest_entries(refresh=a.refresh)
            _exact = next((e for e in _ents if str(_entry_drive_id(e) or "").strip() == gdoc_id), None)
            if _exact is not None:
                _extract_canon = _exact
        except Exception as _me:  # noqa: BLE001 — metadata best-effort, KHÔNG nuốt im lặng
            print(f"[tl] ⚠ không đọc được manifest (bỏ metadata canonical, export vẫn chạy): {_me}", file=sys.stderr)
    if not gdoc_id and a.sohieu:
        try:
            _ents = _extract_resolve_entries(a)   # r180 S3: profile + CỘNG NỀN (base-also)
            canon, gdoc_id, _nm, hits = _resolve_deep_target(a.sohieu, _ents)
        except Exception as e:
            print(f"[tl] không đọc được manifest để resolve --sohieu: {e}", file=sys.stderr)
            return 1
        if not canon:
            print(f"[tl] không tìm thấy văn bản cho --sohieu/query={a.sohieu!r}", file=sys.stderr)
            return 1
        if _entry_raw_no_gdoc(canon):
            return _emit_raw_no_gdoc(_entry_name(canon), getattr(a, "json", False))
        _extract_canon = canon
        print(f"[tl] canonical: { _entry_name(canon) } | sohieu={_entry_sohieu(canon)} | "
              f"cat={_entry_cat(canon)} | nlm={bool(_entry_nlm(canon))} | candidates={len(hits)}",
              file=sys.stderr)
    if not gdoc_id:
        print("[tl] cần gdoc_id hoặc --sohieu <số hiệu/tên>", file=sys.stderr)
        return 1
    if _extract_canon is not None and _entry_is_draft(_extract_canon):
        print(f"[tl] ⚠ {DRAFT_WARNING}: nguồn đang đọc là dự thảo, không được viện dẫn như văn bản có hiệu lực.",
              file=sys.stderr)
    # v1.29.7 (log NĐ131 #3): ƯU TIÊN cache CONSOLIDATED do `tl cache-build` dựng (KHÔNG dính cap ~200k của export
    # — ca thật: văn bản 185 Điều bị cắt ở Điều 26, không lấy được Điều 40/130). Có cache → dựng text từ articles.
    text, src = None, None
    _sh_cache = norm_sohieu(str(a.sohieu or (_entry_sohieu(_extract_canon) if _extract_canon else "") or ""))
    if _sh_cache:
        try:
            _cdoc = _imp("cache").find(_sh_cache)
            _arts = (_cdoc or {}).get("articles") or {}
            if _arts:
                def _artkey(k):
                    m = re.match(r"(\d+)([a-z]*)", str(k).strip().lower())
                    return (int(m.group(1)), m.group(2)) if m else (10**9, str(k))
                _parts = []
                for n in sorted(_arts.keys(), key=_artkey):
                    t = str(_arts[n] or "").strip()
                    _parts.append(t if re.match(r"^\s*Điều\s", t) else f"Điều {n}. {t}")
                text, src = "\n\n".join(_parts), f"cache-build consolidated ({len(_arts)} điều, no-cap)"
        except Exception:  # noqa: BLE001
            text = None
    # Đọc nguyên văn: ƯU TIÊN transport→gws (export GDoc→text trực tiếp, BỎ QUA webapp `exporttext` vốn
    # lỗi OAuth scope `script.external_request`). Fallback webapp exporttext nếu transport/gws không sẵn.
    def _read_fulltext(_fid):
        """Trả (text, src, err) — err gộp cả 2 tầng để phân loại NOT_FOUND vs lỗi mạng/auth (A.1 v1.34.40)."""
        _t, _s, _e = None, None, ""
        try:
            rr = _imp("transport").drive_op("read", file_id=_fid, limit=2_000_000)
            if isinstance(rr, dict) and rr.get("ok") and rr.get("text") is not None:
                _t, _s = rr.get("text", ""), "gws/transport"
            elif isinstance(rr, dict):
                _e = str(rr.get("error") or "")
        except Exception as ex:  # noqa: BLE001
            _e = f"{type(ex).__name__}: {ex}"
            if getattr(a, "debug", False):
                print(f"[tl] transport read lỗi (sẽ thử exporttext): {ex}", file=sys.stderr)
        if _t is None:
            r = _gas().get("exporttext", fileId=_fid)
            if r.get("ok"):
                _t, _s = r.get("text", ""), "webapp exporttext"
            else:
                _e = (_e + " | " if _e else "") + str(r.get("error") or "")
        return _t, _s, _e

    if text is None:
        text, src, _err = _read_fulltext(gdoc_id)
        # v1.34.40 A.1 fallback false-404: positional dạng-id nhưng Drive báo NOT_FOUND (= chắc chắn KHÔNG phải
        # id thật, ví dụ tên file 'Luat_113-2025-QH15_Dan_so' ≥20 ký tự) → deep-resolve MỘT lần như trước.
        # CHỈ khi NOT_FOUND — lỗi mạng/auth/scope KHÔNG resolve (resolve lúc đó là đoán mò trên input hợp lệ).
        if text is None and _id_positional and re.search(
                r"not\s*found|404|khong tim thay|no such file", _strip_accents(_err or "").lower()):
            try:
                _ents = _manifest_entries(refresh=a.refresh)
                _canon, _did, _nm, _hits = _resolve_deep_target(gdoc_id, _ents)
            except Exception as _re:  # noqa: BLE001
                _canon, _did, _hits = None, None, []
                print(f"[tl] ⚠ deep-resolve fallback lỗi: {_re}", file=sys.stderr)
            if _canon is not None and _entry_raw_no_gdoc(_canon):
                return _emit_raw_no_gdoc(_entry_name(_canon), getattr(a, "json", False))
            if _canon is not None and _did and _did != gdoc_id:
                print(f"[tl] positional KHÔNG phải Drive-id thật (NOT_FOUND) → coi là tên/số hiệu, canonical: "
                      f"{ _entry_name(_canon) } | sohieu={_entry_sohieu(_canon)} | cat={_entry_cat(_canon)} | "
                      f"nlm={bool(_entry_nlm(_canon))} | candidates={len(_hits)}", file=sys.stderr)
                _extract_canon = _canon
                gdoc_id = _did
                if _entry_is_draft(_canon):
                    print(f"[tl] ⚠ {DRAFT_WARNING}: nguồn đang đọc là dự thảo, không được viện dẫn như văn bản "
                          f"có hiệu lực.", file=sys.stderr)
                text, src, _err = _read_fulltext(gdoc_id)
        if text is None:
            print(f"[tl] đọc nguyên văn LỖI (gws/transport + webapp exporttext): {_err}\n"
                  f"     → webapp exporttext thiếu OAuth scope → cần gws (transport): bootstrap + gws auth ở "
                  f"Code/Cowork (tl gws-ping).\n"
                  f"     → hoặc file .docx/.pdf: copy_convert sang Google Doc trước.", file=sys.stderr)
            return 1
    text = _sanitize_export_text(_strip_font_runs(text))   # U1 v1.31.2: + diệt surrogate/control-byte (lọc dòng rác font như cũ)
    _profile_cache_dir().mkdir(parents=True, exist_ok=True)
    disk = Path(a.out) if a.out else _cache_file(f"extract_{gdoc_id}.txt")
    disk.write_text(text, encoding="utf-8")   # toàn văn nằm trên ĐĨA, KHÔNG vào context
    print(f"[tl] {len(text)} ký tự → {disk} (0 token vào context) [nguồn: {src}]")
    # A4: exporttext webapp CAP ~200k ký tự → khi chạm cap, văn bản DÀI có thể bị CẮT (không phải đủ 200k). Cảnh báo rõ.
    if len(text) >= 199000 and not str(src or "").startswith("cache-build"):
        print(f"[tl] ⚠ độ dài chạm CAP export (~200k ký tự) — văn bản DÀI có thể bị CẮT (không phải đủ {len(text)}). "
              f"Chạy `tl cache-build {(_sh_cache or '<sohieu>')}` (no-cap) rồi extract LẠI — extract tự dùng cache đó (v1.29.7).",
              file=sys.stderr)
    rc = 0
    if getattr(a, "find", None):
        for term in a.find:
            hits = _find_nfc(text, term, getattr(a, "find_window", 120) or 120)
            print(f"\n===== FIND NFC: {term!r} — {len(hits)} hit(s) =====")
            if not hits:
                print("[tl] KHÔNG thấy chuỗi sau NFC normalize (tránh dùng grep trần với tiếng Việt có dấu).")
                rc = 1
            for h in hits[:10]:
                print(f"- @{h['pos']}: …{h['snippet']}…")
            if len(hits) > 10:
                print(f"  ... còn {len(hits)-10} hit(s), dùng file trên đĩa để soi tiếp.")
    if not a.dieu:
        if not getattr(a, "find", None):
            print("[tl] (chưa --dieu/--find) — chỉ lưu đĩa. Thêm --dieu N hoặc --find 'chuỗi' để verify.")
        return rc
    _last_dieu = max((int(x) for x in re.findall(r"(?m)^\s*Điều\s+(\d+)", text)), default=0)
    for n in a.dieu:
        block = extract_dieu(text, n)
        print(f"\n===== Điều {n} =====")
        if block:
            print(block)
        else:
            # #3: phân biệt CẮT-CỤT (export cap ~200k ký tự) với SAI CẤU TRÚC. Nếu Điều yêu cầu > Điều cao nhất đọc
            # được, HOẶC text dài gần ngưỡng cap → nghi truncation, KHÔNG đổ cho cấu trúc; chỉ đường lấy TOÀN VĂN.
            if _last_dieu and (int(str(n).rstrip("abcđ") or 0) > _last_dieu or len(text) >= 190000):
                print(f"[tl] KHÔNG thấy Điều {n}: Điều CAO NHẤT đọc được = {_last_dieu}, độ dài = {len(text):,} ký tự. "
                      f"NGHI VĂN BẢN BỊ CẮT (export-text webapp cap ~200k ký tự) — KHÔNG phải sai cấu trúc. "
                      f"Lấy TOÀN VĂN: `tl cache-build <sốhiệu> --gdoc-id {gdoc_id}` (exportdocx, không cap) hoặc đọc {disk}.")
            else:
                print(f"[tl] KHÔNG thấy Điều {n} (kiểm cấu trúc / bản đúng?). Điều cao nhất = {_last_dieu or '?'}, len = {len(text):,}.")
            rc = 1
    return rc


def cmd_cache_build(a) -> int:
    """B2: wrapper `tl` cho ingest_to_cache.py — dựng cache CẤU TRÚC `docs/<sh>--consolidated.json` mà `tl rasoat
    worksheet` cần (worksheet báo "chạy ingest_to_cache.py trước" nhưng KHÔNG có subcommand tl nào sinh ra nó).
    Chain: `tl cache-build <sh> --gdoc-id <id>` (hoặc `--input <file>`). Tự nạp webapp/token (config). Cờ còn lại
    chuyển thẳng cho ingest_to_cache.py (--goc/--method/--nlm-source-id/--vbhn-first…)."""
    sh = getattr(a, "sohieu", None)
    rest = list(getattr(a, "rest", None) or [])
    if not sh and not ({"-h", "--help"} & set(rest)):
        print("[tl] cache-build cần <số hiệu> (vd `tl cache-build 19/VBHN-VPQH --gdoc-id <id>`).", file=sys.stderr)
        return 2
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))   # set TL_WEBAPP/TL_TOKEN cho script con tự nạp (B3)
    except (Exception, SystemExit):
        pass     # --input file cục bộ thì không cần webapp
    name = "ingest_to_cache"
    target = _healed_script_path(name) or str(HERE / "ingest_to_cache.py")
    if not os.path.exists(target):
        print(f"[tl] cache-build: không thấy {target} (script optional chưa có trong overlay).", file=sys.stderr)
        return 2
    args = (["--so-hieu", sh] if sh else []) + rest
    return subprocess.call([sys.executable, target] + args)


def cmd_cache_snapshot(a) -> int:
    """WS5: export/import snapshot manifest_index để giảm ~7-8s/phiên boot. Import có CỔNG treeHash:
    chỉ dùng nếu treeHash snapshot == treeHash manifest hiện hành (tránh cache cũ)."""
    idxp = _cache_file("manifest_index.json")
    if a.sub == "export":
        if not idxp.exists():
            print("[tl] cache-snapshot export: chưa có manifest_index (chạy `tl boot` trước).", file=sys.stderr); return 2
        outp = Path(getattr(a, "out", None) or "manifest_index.snapshot.json")
        data = json.loads(idxp.read_text(encoding="utf-8"))
        th = (data.get("_meta") or {}).get("treeHash")
        outp.write_text(json.dumps({"treeHash": th, "profile": _active_profile(), "index": data}, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({"ok": True, "exported": str(outp), "treeHash": th,
                          "entries": (data.get("_meta") or {}).get("entries_indexed")}, ensure_ascii=False, indent=2))
        return 0
    if a.sub == "import":
        snap = Path(getattr(a, "in_file", None) or "manifest_index.snapshot.json")
        if not snap.exists():
            print(f"[tl] cache-snapshot import: không thấy {snap}", file=sys.stderr); return 2
        sd = json.loads(snap.read_text(encoding="utf-8"))
        snap_th = sd.get("treeHash")
        if not getattr(a, "force", False):
            # cổng treeHash: lấy treeHash manifest hiện hành (1 call nhẹ manifest_export) rồi đối chiếu
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
            cur = _gas().get("manifest_export")
            cur_th = cur.get("treeHash")
            if cur_th and snap_th and cur_th != snap_th:
                print(json.dumps({"ok": False, "flag": "TREEHASH_MISMATCH", "snapshot": snap_th, "current": cur_th,
                                  "note": "snapshot CŨ so với corpus hiện tại — bỏ qua. Dùng --force nếu chắc chắn, hoặc `tl boot --refresh`."},
                                 ensure_ascii=False, indent=2), file=sys.stderr)
                return 1
        idxp.parent.mkdir(parents=True, exist_ok=True)
        idxp.write_text(json.dumps(sd.get("index") or {}, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({"ok": True, "imported_to": str(idxp), "treeHash": snap_th, "gated": not getattr(a, "force", False)},
                         ensure_ascii=False, indent=2))
        return 0
    print("[tl] cache-snapshot cần: export | import", file=sys.stderr); return 2

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


def extract_dieu(text: str, n: int) -> str | None:
    """Trích NGUYÊN VĂN Điều n: từ 'Điều n' tới 'Điều <kế tiếp>' (chịu số nhảy cóc)."""
    m = _DIEU_HEAD(n).search(text or "")
    if not m:
        return None
    end = len(text)
    nxt = _DIEU_ANY.search(text, m.end())
    if nxt:
        end = nxt.start()
    return text[m.start():end].strip()

def _find_nfc(text: str, term: str, window: int = 120) -> list[dict]:
    """Tìm chuỗi trong văn bản sau khi chuẩn hóa NFC + casefold.

    Dùng thay `grep` trần để tránh âm tính giả với tiếng Việt có dấu / tổ hợp Unicode.
    Trả về snippet từ văn bản đã NFC-normalize để phục vụ verify pháp lý.
    """
    hay = unicodedata.normalize("NFC", text or "")
    needle = unicodedata.normalize("NFC", term or "")
    if not needle:
        return []
    hay_cmp, needle_cmp = hay.casefold(), needle.casefold()
    out, start = [], 0
    while True:
        i = hay_cmp.find(needle_cmp, start)
        if i < 0:
            break
        a = max(0, i - window); b = min(len(hay), i + len(needle) + window)
        snip = hay[a:b].replace("\r", " ").replace("\n", " ")
        out.append({"pos": i, "snippet": snip})
        start = i + max(1, len(needle_cmp))
        if len(out) >= 50:
            break
    return out

def _sanitize_export_text(s: str) -> str:
    """U1 (v1.31.2 — log LIVE: driver bash vỡ capture vì 'byte không hợp UTF-8' trong output extract): làm sạch
    text export TRƯỚC khi ghi đĩa/in — (a) diệt lone-surrogate (rò từ decode errors=surrogateescape của các đường
    export/gws) bằng round-trip encode-replace; (b) bỏ control-char (giữ \\n \\t). stdout đã reconfigure
    errors='replace' từ lâu nhưng KHÔNG cứu được file --out + text chui vào JSON của driver."""
    s = str(s or "")
    try:
        s = s.encode("utf-8", errors="replace").decode("utf-8")
    except Exception:
        s = s.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", s)
