# -*- coding: utf-8 -*-
"""tl_core.lookup_ops — I6 (v1.34.9): tách NGUYÊN VĂN 16 lệnh tra cứu/quan hệ + helper riêng-cụm từ scripts/tl.py
(locate/source-map/status/relation-check+backfill/vbhn-check+verify+compare/xref/footnote-map/cluster/
rasoat×3/header-verify/dedup-check). ĐỘNG CƠ resolution `_source_map_one` + helper đa-module
(_dedup_status/_classify_ref/resolve_footnote_amendments/_relation_audit/_rq_relation_probe/
_scan_inline_amendments/_sohieu_query_hits_entry/_nlm_status_*) GIỮ Ở TL — ranh giới grilling 2026-07-09.
Hành vi khoá bởi r76a wiring + 59 điểm test sẵn của engine."""
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
    """REBASE __globals__ từng hàm đã chuyển về namespace SỐNG của tl (khuôn I1-I5)."""
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



def _vbhn_bare_key(key: str) -> str:
    """(v1.33.47 — đối chiếu fix v1.33.46 nhánh song song, ca thật 'VBHN 88 Quảng cáo ĐÃ CÓ mà lần nào chạy cũng
    báo thiếu'): dạng BARE `NN-VBHN-CƠQUAN` của một khóa VBHN — bỏ NĂM nếu có, giữ nguyên nếu vốn không năm; ''
    nếu không phải khóa VBHN. Gốc rễ false-negative HỆ THỐNG: web/footnote ghi số VBHN KHÔNG năm ('88/VBHN-VPQH')
    còn corpus lưu year-qualified ('88-2025-VBHN-VPQH' — bất biến PHẢI-CÓ-NĂM chống collision) → so exact/substring
    miss vì NĂM CHÈN GIỮA. CHỈ dùng cho KHỚP TRUY VẤN 1 chiều — TUYỆT ĐỐI không thay khóa canonical/registry
    (collision-detect + vbhn-year-fix dựa vào năm)."""
    k = norm_sohieu(key or "")
    m = _VBHN_WITHYEAR_RE.fullmatch(k)
    if m:
        return f"{m.group(1)}-VBHN-{m.group(3)}"
    return k if _VBHN_NOYEAR_RE.fullmatch(k) else ""


def _dang_bare_key(key: str) -> str:
    """v1.34.41 B.2 GĐ2 (grill D5 — khuôn `_vbhn_bare_key` y hệt): dạng BARE `NN-LOẠI-CƠQUAN` của khóa số
    Đảng/hành chính — bỏ NĂM nếu year-qualified (04-2026-CT-TW → 04-CT-TW), giữ nguyên nếu vốn không năm;
    '' nếu không phải khóa dạng này (khóa VBHN loại trừ — họ đó có bare-key riêng). CHỈ dùng KHỚP TRUY VẤN
    1 CHIỀU — TUYỆT ĐỐI không thay khóa canonical/registry (collision-detect qua khóa cần năm)."""
    k = norm_sohieu(key or "")
    if _VBHN_WITHYEAR_RE.fullmatch(k) or _VBHN_NOYEAR_RE.fullmatch(k):
        return ""
    m = re.fullmatch(r"(\d{1,5})-(?:20\d\d|19\d\d)-([A-Z][A-Z0-9]{1,5}-[A-Z0-9]{2,15})", k)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return k if re.fullmatch(r"\d{1,5}-[A-Z][A-Z0-9]{1,5}-[A-Z0-9]{2,15}", k) else ""


def cmd_locate(a) -> int:
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    q = a.query
    # CHỈ coi là SỐ HIỆU khi truy vấn THỰC SỰ giống số hiệu — nếu không, `norm_sohieu("bảo hiểm xã hội")` ra chuỗi
    # rác bị dùng như số hiệu → LOW_CONFIDENCE/NO_EXACT_SOHIEU giả (regression v1.22.54). Cụm danh từ → key rỗng → khớp tên.
    key = norm_sohieu(q) if _looks_like_sohieu_query(q) else ""
    # r179 T7 (doctrine «--json = cờ khoan dung» KHÔNG áp cho lệnh đọc lõi — locate bị driver batch parse
    # stdout tay): --json in ENVELOPE THẬT ở CẢ 3 nhánh (offline index / offline manifest / webapp find),
    # stdout sạch (narration text tắt). Row nền VBQPPL mang scope:'vbqppl' + cờ BASE_SCOPE_HIT (T5 MỘT từ vựng).
    _json179 = bool(getattr(a, "json", False))

    def _lrow179(o, base=False):
        flags = list(_title_flags(o))
        if key and norm_sohieu(_entry_sohieu(o)) != key:
            flags.append("NO_EXACT_SOHIEU")
        r = {"drive_id": _entry_drive_id(o), "name": _entry_name(o), "sohieu": _entry_sohieu(o),
             "cat": str(_entry_cat(o) or ""), "hieuluc": str(o.get("hieuluc") or o.get("hieu_luc") or ""),
             "nlm": _nlm_display(o), "flags": flags}
        if base:
            r["scope"] = "vbqppl"
            r["flags"] = list(dict.fromkeys(r["flags"] + ["BASE_SCOPE_HIT"]))
        return r

    def _lemit179(mode, rows_out, low_conf, found=None, **extra):
        out = {"ok": True, "schema": "locate.v1", "query": q, "mode": mode,
               "count": len(rows_out) if found is None else found,
               "shown": len(rows_out), "truncated": (found or len(rows_out)) > len(rows_out),
               "low_confidence": bool(low_conf), "rows": rows_out, **extra}
        if low_conf:
            out["warnings"] = list(dict.fromkeys(list(out.get("warnings") or [])
                                                 + ["LOW_CONFIDENCE_NO_EXACT_SOHIEU"]))
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    idx_path = _cache_file("manifest_index.json")
    # v1.29.4 (AUDIT #9 auto-refresh): cache quá hạn (>900s — quá cả trần cache đọc GAS 600s) → TỰ refresh manifest
    # (kèm rebuild index) thay vì âm thầm khớp trên dữ liệu cũ (nguồn báo-động-giả lặp lại các phiên rà). --trust-cache tắt.
    _age = _manifest_cache_age_seconds()
    if (not getattr(a, "trust_cache", False)) and (_age is None or _age > 900):
        try:
            print(f"[locate] cache manifest {'THIẾU' if _age is None else f'cũ {int(_age)}s'} → tự refresh (tắt: --trust-cache)…",
                  file=sys.stderr, flush=True)
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
            _load_manifest_full(refresh=True)
        except Exception:
            pass
    # A (v1.30.0): profile CỘNG VBQPPL — bật (mặc định ở profile dự án) thì quét THÊM nền VBQPPL, hit profile ưu tiên.
    _base_also = _base_also_enabled(a)
    # 1) index offline (so_hieu) — rẻ nhất. Base-also: BỎ shortcut này (index chỉ chứa scope profile —
    #    return sớm sẽ nuốt mất phần nền; nhánh 1b in đủ cả hai scope).
    if idx_path.exists() and not _base_also:
        try:
            idx = json.loads(idx_path.read_text(encoding="utf-8"))
            hits = idx.get("so_hieu", {}).get(key) or idx.get("so_hieu", {}).get(q)
            if hits and _json179:
                _lemit179("offline_index", [_lrow179(e) for e in hits], False,
                          warnings=["OFFLINE_CACHE_INDEX_MAY_LAG_LIVE"])
                return 0
            if hits:
                print(f"[offline index] {key}: {len(hits)} entry")
                for e in hits:
                    print(f"  - {e.get('name','')[:60]} | cat={e.get('cat','')} "
                          f"| hieuluc={e.get('hieuluc','')} | nlm={bool(e.get('nlm_source_id'))}")
                print("[tl] ⚠ OFFLINE CACHE (index) — có thể LỆCH registry live; đối chiếu `tl reg-query --sohieu <...> --refresh` "
                      "TRƯỚC khi kết luận (vd nghi shared-source: cùng drive_id ≠ nhiều dòng → thường là khớp-mờ cache, KHÔNG phải shared thật).")
                return 0
        except Exception:
            pass
    # 1b) manifest offline theo tên/số hiệu — giàu metadata hơn webapp find, có cờ cảnh báo nhãn sai/orphan.
    try:
        qn = _strip_accents(q).lower()
        qnk = _name_key(q)

        def _locate_match(e):
            sh = norm_sohieu(_entry_sohieu(e))
            nm = _strip_accents(_entry_name(e)).lower()
            nk = _name_key(_entry_name(e))
            # v1.33.47: sohieu khớp qua _sohieu_query_hits_entry (+bare-VBHN 1 chiều) trên CẢ sohieu field lẫn key entry
            return ((key and (_sohieu_query_hits_entry(key, sh) or _sohieu_query_hits_entry(key, _sohieu_key_entry(e))))
                    or (qn and qn in nm) or (qnk and nk and (qnk in nk or nk in qnk))
                    or _entry_query_match(q, e, include_subject=False))    # token/phrase: 'Luật Dân số' ↔ '...Dan_so'

        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
        mhits = [e for e in entries if _locate_match(e)]
        mhits.sort(key=lambda e: (_entry_score(e), -len(_title_flags(e))), reverse=True)
        bhits, berr = [], None
        if _base_also:
            b_entries, berr = _base_manifest_entries(getattr(a, "config", None))
            _seen = {_entry_drive_id(e) for e in mhits if _entry_drive_id(e)}
            bhits = [e for e in b_entries if _locate_match(e) and _entry_drive_id(e) not in _seen]
            bhits.sort(key=lambda e: (_entry_score(e), -len(_title_flags(e))), reverse=True)
        if _base_also and berr and not bhits:
            print(f"[tl] ⚠ base-also: không đọc được manifest nền VBQPPL ({berr}) — kết quả CHỈ scope profile.", file=sys.stderr)
        if (mhits or bhits) and _json179:
            # r179 T7: envelope máy-đọc — hit profile trước, hit nền sau (scope+BASE_SCOPE_HIT per-row).
            _exact = [e for e in (mhits + bhits) if key and norm_sohieu(_entry_sohieu(e)) == key]
            _rows179 = ([_lrow179(e) for e in mhits[:a.max]] + [_lrow179(e, base=True) for e in bhits[:a.max]])
            _lemit179("offline_manifest", _rows179, bool(key) and not _exact,
                      found=len(mhits) + len(bhits), profile_hits=len(mhits), base_hits=len(bhits),
                      warnings=(["OFFLINE_CACHE_MANIFEST_MAY_LAG_LIVE"]
                                + (["BASE_MANIFEST_READ_ERROR"] if (_base_also and berr) else [])))
            return 0
        if bhits and not mhits:
            print(f"[offline manifest] {q}: 0 entry trong profile '{_active_profile()}' — hit dưới là NỀN VBQPPL (TL_BASE_ALSO).")
        if mhits or bhits:
            # #10: truy vấn theo SỐ HIỆU nhưng KHÔNG có entry đúng số hiệu → kết quả CHỈ khớp MỜ theo tên → rủi ro
            # nhầm văn bản (vd `locate 142/2025/QH15` ra VBHN_74 Đấu thầu). Gắn cờ độ-tin-cậy rõ ràng.
            # A (v1.30.0): độ-tin-cậy tính trên CẢ 2 scope (exact ở nền cũng là exact — tránh LOW_CONFIDENCE giả).
            _exact = [e for e in (mhits + bhits) if key and norm_sohieu(_entry_sohieu(e)) == key]
            _low_conf = bool(key) and not _exact
            if mhits:
                print(f"[offline manifest] {q}: {len(mhits)} entry"
                      + ("  ⚠ LOW_CONFIDENCE (KHÔNG khớp đúng số hiệu — chỉ khớp mờ theo tên)" if _low_conf else ""))
            for e in mhits[:a.max]:
                flags = list(_title_flags(e))
                if key and norm_sohieu(_entry_sohieu(e)) != key:
                    flags.append("NO_EXACT_SOHIEU")
                warn = (" | WARN=" + ",".join(flags)) if flags else ""
                print(f"  - {_entry_name(e)[:70]} | sohieu={_entry_sohieu(e)} | cat={_entry_cat(e)} "
                      f"| hieuluc={e.get('hieuluc') or e.get('hieu_luc') or ''} | nlm={_nlm_display(e)}{warn}")
            if bhits:   # A: mục NỀN VBQPPL — bổ sung SAU hit profile (profile ưu tiên), đánh dấu scope rõ.
                print(f"[nền VBQPPL — TL_BASE_ALSO] +{len(bhits)} entry")
                for e in bhits[:a.max]:
                    flags = list(_title_flags(e))
                    if key and norm_sohieu(_entry_sohieu(e)) != key:
                        flags.append("NO_EXACT_SOHIEU")
                    warn = (" | WARN=" + ",".join(flags)) if flags else ""
                    # r179 T5: đánh dấu [nền] TỪNG DÒNG (MỘT từ vựng với reg-query text) — không chỉ header nhóm.
                    print(f"  ~ {_entry_name(e)[:70]} | sohieu={_entry_sohieu(e)} | cat={_entry_cat(e)} "
                          f"| hieuluc={e.get('hieuluc') or e.get('hieu_luc') or ''} | nlm={_nlm_display(e)}{warn} [nền]")
            if _low_conf:
                print(f"[tl] ⚠ KHÔNG có văn bản đúng số hiệu '{key}' trong manifest — các dòng trên CHỈ là khớp-mờ-tên, "
                      "ĐỪNG dùng làm nguồn nếu cần đúng số hiệu; xác minh QT-5/web hoặc kiểm số hiệu.")
            elif any(_title_flags(e) for e in (mhits + bhits)[:a.max]):
                print("[tl] Có WARN: chạy `tl status <sohieu>` và/hoặc `tl hygiene plan <query> --json` trước khi dùng làm nguồn rà soát.")
            print("[tl] ⚠ OFFLINE CACHE (manifest) — có thể LỆCH registry live; đối chiếu `tl reg-query --sohieu <...> --refresh` "
                  "để xác nhận drive_id/corpus/nlm THẬT trước khi kết luận (tránh báo động giả shared-source do khớp-mờ tên).")
            return 0
    except Exception as e:
        if getattr(a, "debug", False):
            print(f"[tl] bỏ qua manifest offline: {e}", file=sys.stderr)
    # 2) fallback webapp find (trả 'rows') — nhánh FULLTEXT dễ trả văn bản LẠC ĐỀ khi truy vấn số hiệu không có trong
    #    corpus (vd `locate 58/2014/QH13` → BHYT/Quảng cáo/Xuất bản). Gắn cờ độ-tin-cậy như nhánh offline (#10/Cowork).
    load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    g = _gas()
    r = g.get("find", q=q, max=a.max)
    rows = r.get("rows", [])
    _wf_exact = [o for o in rows if key and norm_sohieu(o.get("sohieu", "")) == key]
    _wf_low = bool(key) and rows and not _wf_exact
    if _json179:
        _lemit179("webapp_find", [_lrow179(o) for o in rows[:a.max]], _wf_low,
                  found=len(rows), tier=r.get("tier"))
        return 0 if rows else 1
    print(f"[webapp find tier={r.get('tier')}] {len(rows)} rows"
          + ("  ⚠ LOW_CONFIDENCE (KHÔNG khớp đúng số hiệu — fulltext lạc đề)" if _wf_low else ""))
    for o in rows[: a.max]:
        flags = list(_title_flags(o))
        if key and norm_sohieu(o.get("sohieu", "")) != key:
            flags.append("NO_EXACT_SOHIEU")
        warn = (" | WARN=" + ",".join(flags)) if flags else ""
        print(f"  - {o.get('name','')[:60]} | sohieu={o.get('sohieu','')} | cat={o.get('cat','')} "
              f"| nlm={bool(o.get('nlm_source_id'))}{warn}")
    if _wf_low:
        print(f"[tl] ⚠ KHÔNG có văn bản đúng số hiệu '{key}' — các dòng trên là fulltext LẠC ĐỀ, ĐỪNG kết luận corpus "
              "có/không có; xác minh QT-5/web theo số hiệu.")
    return 0 if rows else 1


def _find_amendment_candidates(qkey: str, direct: list[dict], by_name: list[dict], entries: list[dict]) -> list[dict]:
    """Tìm luật sửa đổi trong corpus kể cả khi registry thiếu quan hệ goc/sua_doi."""
    seed = direct or by_name
    subj: set[str] = set()
    for e in seed[:3]:
        subj |= _subject_tokens_for_entry(e)
    base_subject_text = _entry_subject_text(seed[0]) if seed else ""    # cho loại-trừ-chéo BHXH↔BHYT…
    base_rank = max((_vb_tier_rank(s) for s in seed[:5]), default=0)    # thứ bậc CAO NHẤT nhóm = VB ĐANG rà (chặn cấp-dưới-sửa-cấp-trên)
    out = []
    seen = {_entry_drive_id(e) for e in seed}
    for e in entries:
        did = _entry_drive_id(e) or str(id(e))
        if did in seen or not _is_amendment_like(e):
            continue
        if base_subject_text and _disc_conflict(base_subject_text, _entry_subject_text(e)):
            continue                                      # #3 log: BHYT/BHTN… chung "bảo hiểm" nhưng khác chế định → loại
        # P1-5 (log rà 71 luật): VĂN BẢN PHI QUY PHẠM lẫn corpus — sohieu=∅ VÀ tên mang dấu "góp ý/kiến nghị/
        # ý kiến" (vd "006. Agribank- góp ý … kiến nghị sửa đổi luật BHXH.pdf") = thư góp ý dự thảo, KHÔNG phải VB
        # sửa đổi → LOẠI (hết PAUSE giả). Bản sohieu=∅ khác (tên "SuaDoi…" chưa bóc số) vẫn liệt kê (confidence=low).
        _cand_sohieu = _entry_sohieu(e) or _parse_sohieu_from_name(_entry_name(e))
        # v1.29.6 (log rà 118 Luật — P0a): ứng viên amendment cho một VBQPPL phải là văn bản corpus SỐNG.
        # corpus=false (đã bị thay/tắt — vd Luat_51-2024 đã thay) KHÔNG BAO GIỜ là amendment sống → LOẠI.
        # cat 'Van_ban_thuong' (văn bản hành chính/nội bộ — vd bản góp ý Quy chế lao động HR) → LOẠI.
        if str(e.get("corpus") or "").lower() == "false":
            continue
        if "van ban thuong" in _strip_accents(str(_entry_cat(e) or "")).lower().replace("_", " "):
            continue
        # Gate theo SỐ HIỆU REGISTRY (không phải số bóc-từ-tên): "006. Góp ý Luật 64/2020 BHXH.pdf" có '64/2020'
        # TRONG TÊN nhưng registry sohieu RỖNG → vẫn là thư góp ý → LOẠI (nếu gate theo _cand_sohieu thì lọt).
        # v1.29.6 (P0a): mở rộng pattern PHI-QUY-PHẠM (ca thật 118 Luật): 'Lịch trình thẩm tra dự án Luật sửa đổi…'
        # (lịch họp) và 'YK_tham_gia_du_thao_…' (phiếu ý kiến) từng leo làm amendment → PAUSE giả. Chuẩn hoá '_'→' '
        # trước khi so (tên file dùng underscore làm keyword cũ 'gop y' không match 'gop_y').
        _nm_norm = _strip_accents(_entry_name(e)).lower().replace("_", " ")
        _nonnormative_name = any(kw in _nm_norm for kw in ("gop y", "kien nghi", "y kien", "lich trinh",
                                                           "tham tra", "du thao", "ke hoach hop", "chuong trinh hop"))
        if _nm_norm.startswith("yk "):          # 'YK_…' = phiếu Ý KIẾN — không bao giờ là VBQPPL, loại vô điều kiện
            continue
        if (not _entry_sohieu(e)) and _nonnormative_name:
            continue
        # #3 log (false-positive PAUSE): SAI THỨ BẬC — VB cấp dưới (NĐ/TT) KHÔNG thể là 'sửa đổi' của VB cấp trên
        # (Luật/Pháp lệnh). 118/2016/NĐ-CP sửa 1 NĐ ≠ sửa Luật BHYT. Chỉ lọc khi BIẾT rõ cả hai bậc & ứng viên thấp hơn.
        cand_rank = _vb_tier_rank(e)
        if base_rank and cand_rank and cand_rank < base_rank:
            continue

        refs = _goc_keys(e) | _ref_tokens(_field_text(e, _REF_KEYS + _META_TITLE_KEYS) + " " + _entry_name(e))
        etoks = _subject_tokens_for_entry(e)
        linked = bool(qkey and qkey in refs)
        overlap = len(subj & etoks)
        # #5: SIẾT nhiễu — non-linked phải overlap ≥ min(3, |subj|) (was hằng 2; overlap-2 kéo về NĐ khác lĩnh vực).
        # Neo theo ĐỘ DÀI subject để chủ đề tên ngắn (≤2 token: "Luật Đầu tư"…) không bị over-filter (critic).
        # linked (dẫn chiếu đúng số hiệu) = HIGH; non-linked = LOW (cần verify trước khi kết luận).
        if linked or (subj and overlap >= min(3, len(subj))):
            ee = dict(e)
            ee["_amendment_linked_to_query"] = linked
            ee["_amendment_subject_overlap"] = overlap
            # P1-5: HIGH chỉ khi linked ĐÚNG số hiệu VÀ ứng viên CÓ số hiệu hợp lệ; sohieu=∅ → luôn low (cần verify).
            ee["_amendment_confidence"] = "high" if (linked and _cand_sohieu) else "low"
            ee["_amendment_has_sohieu"] = bool(_cand_sohieu)
            # v1.29.6 (P0d): OMNIBUS 'sửa N luật' (tên không liệt kê luật đích — vd Luat_90-2025 sua_doi_8_luat) chỉ
            # được coi là amendment của base khi LINKED (base xuất hiện trong goc/sua_doi/refs của nó). Non-linked
            # omnibus khớp chủ đề trần từng bị gán cho 8 base nó KHÔNG sửa → PAUSE giả hàng loạt.
            ee["_amendment_omnibus"] = bool(re.search(r"sua[\s_]*doi[\s_]*\d+[\s_]*luat", _nm_norm))
            # v1.29.6 (P0b): NGƯỠNG PAUSE — candidate 'MẠNH' (đủ để DỪNG workflow) = dẫn chiếu ĐÚNG số hiệu base
            # (linked) / confidence=high. 100% ca PAUSE giả của log 118 Luật đều low+non-linked → chỉ REVIEW.
            ee["_amendment_strong"] = bool((linked or ee["_amendment_confidence"] == "high")
                                           and not (ee["_amendment_omnibus"] and not linked))
            out.append(ee)
    out.sort(key=lambda e: (_entry_score(e), e.get("_amendment_subject_overlap", 0)), reverse=True)
    # B3 (log rà): GỘP ứng viên TRÙNG SỐ HIỆU (bản GDoc/NLM + bản .docx/.pdf thô song song) → giữ bản điểm cao nhất
    # (đã sort desc nên bản đầu là GDoc/NLM). Tránh liệt kê 1 luật-sửa 2 lần (vd 57/2024 base + 57/2024.docx).
    _seen_sh, _dedup = set(), []
    for e in out:
        k = _sohieu_key_entry(e)
        if k and k in _seen_sh:
            continue
        if k:
            _seen_sh.add(k)
        _dedup.append(e)
    return _dedup


def cmd_source_map(a) -> int:
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    if a.refresh or not (_cache_file("manifest.json")).exists():
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=a.refresh)
    except Exception as e:
        print(f"[tl] source-map: không đọc được manifest: {e}", file=sys.stderr)
        return 1
    # A (v1.30.0): profile CỘNG VBQPPL — doctrine profile-first: chỉ khi profile MISS hoàn toàn mới tra tiếp
    # trên manifest NỀN; hit nền gắn scope='vbqppl' + cờ BASE_SCOPE_HIT (máy-đọc phân biệt, canonical profile luôn thắng).
    _base_entries_cache = None
    def _map_one_base_also(q):
        nonlocal _base_entries_cache
        item = _source_map_one(q, entries)
        if not _base_also_enabled(a):
            return item
        if item.get("canonical") or item.get("amendment_candidates") or item.get("direct_hits") or item.get("name_hits"):
            return item
        if _base_entries_cache is None:
            _base_entries_cache, _ = _base_manifest_entries(getattr(a, "config", None))
        if not _base_entries_cache:
            return item
        b_item = _source_map_one(q, _base_entries_cache)
        if not (b_item.get("canonical") or b_item.get("amendment_candidates") or b_item.get("direct_hits") or b_item.get("name_hits")):
            return item
        b_item["scope"] = "vbqppl"
        b_item["flags"] = list(dict.fromkeys(list(b_item.get("flags") or []) + ["BASE_SCOPE_HIT"]))
        b_item["flags_all"] = list(dict.fromkeys(list(b_item.get("flags_all") or []) + b_item["flags"]))
        b_item["review_reason"] = list(b_item.get("flags_all") or b_item["flags"])
        return b_item
    out = {"ok": True, "entries": len(entries), "items": [_map_one_base_also(q) for q in a.queries]}
    out["results"] = out["items"]   # §1.7: alias nhất quán tên key danh-sách-kết-quả giữa các lệnh (source-map/vbhn-check)
    out["flags"] = list(dict.fromkeys(f for item in out["items"] for f in (item.get("flags") or [])))
    out["flags_all"] = list(dict.fromkeys(f for item in out["items"] for f in (item.get("flags_all") or item.get("flags") or [])))
    out["review_reason"] = list(out["flags_all"])
    out["qt5_queries"] = list(dict.fromkeys(q for item in out["items"] for q in (item.get("qt5_queries") or [])))[:12]
    # 4D (v1.33.30 — MERGE bundle-29): TOP-LEVEL gộp-dedup candidates từ items — driver batch đọc 1 chỗ.
    _cand_top, _cand_seen_top = [], set()
    for item in out["items"]:
        for c in item.get("candidates") or []:
            _ck = c.get("drive_id") or c.get("sohieu_key") or c.get("name")
            if _ck and _ck not in _cand_seen_top:
                _cand_seen_top.add(_ck); _cand_top.append(c)
    out["candidates"] = _cand_top
    out["candidate_count"] = len(_cand_top)
    out["verdict"] = _aggregate_verdict(out["items"])
    if a.json or getattr(a, "out", None):
        _emit_json_payload(out, getattr(a, "out", None))
    else:
        print(f"== tl source-map — manifest entries={len(entries)} ==")
        for item in out["items"]:
            c = item.get("canonical")
            print(f"\n▸ {item['query']}  [{item['mode']}]")
            if c:
                warn = (" | WARN=" + ",".join(c.get("flags") or [])) if c.get("flags") else ""
                print(f"  RÀ SOÁT TRÊN: {c['name'][:90]} | sohieu={c['sohieu'] or '∅'} | cat={c['cat']} | nlm={c['nlm']}{warn}")
            else:
                print("  KHÔNG TÌM THẤY canonical trong manifest")
            for w in item.get("warnings") or []:
                print(f"  ⚠ {w}")
            for ac in item.get("amendment_candidates") or []:
                print(f"    AMENDMENT candidate: {ac.get('name','')[:90]} | sohieu={ac.get('sohieu') or '∅'} | linked={ac.get('linked_to_query')} | nlm={ac.get('nlm')}")
            for rc in item.get("risky_candidates") or []:
                e = rc.get("entry") or {}
                print(f"    WARN candidate: {e.get('name','')[:80]} | flags={','.join(rc.get('flags') or [])}")
    # v1.29.4 (#8 rc-doctrine): mặc định rc=0 (verdict = PHÁT HIỆN, không phải lỗi lệnh); --strict/--fail-on-finding
    # (CI) → rc=1 khi verdict REVIEW/PAUSE_AND_ASK_USER.
    if getattr(a, "strict", False) and str(out.get("verdict") or "") in ("REVIEW", "PAUSE_AND_ASK_USER"):
        return 1
    return 0 if out["ok"] else 1


def cmd_status(a) -> int:
    """CỔNG TIỀN-NẠP QT-2 — bọc preingest_gate.run_live (vb_status + quyết định).

    A3 (EXIT CODE): verdict ADD/SKIP/REVIEW là PHÁT HIỆN dữ liệu → rc=0 (không phá &&/CI; driver
    agentic không hiểu nhầm REVIEW = lệnh hỏng). Chỉ `--strict` mới rc=1 khi REVIEW (mirror xref)."""
    guarded = _status_amendment_registry_guard(a)
    if guarded is not None:
        res, rc = guarded
        if getattr(a, "json", False):
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(f"{res['decision']} — {res['reason']} — {res['surface']}")
            for act in res.get("actions") or []:
                print(" -", act)
        return rc
    pg = _need_base('preingest_gate')
    targets = [t for t in re.split(r"[;,]", a.targets or "") if t.strip()]
    strict = bool(getattr(a, "strict", False))
    # Tương thích module nền: chỉ truyền `strict` nếu run_live của nó NHẬN tham số đó (dùng inspect — KHÔNG nuốt
    # TypeError mù, để lỗi chữ ký THẬT vẫn nổi). Module cũ KHÔNG có `strict` → tự chuẩn hoá rc theo --strict bên dưới.
    import inspect
    try:
        _accepts_strict = "strict" in inspect.signature(pg.run_live).parameters
    except (TypeError, ValueError):
        _accepts_strict = False
    if _accepts_strict:
        rc = pg.run_live(a.sohieu, targets, a.amendment, a.vbhn, a.json, strict)
    else:
        rc = pg.run_live(a.sohieu, targets, a.amendment, a.vbhn, a.json)
    # Phòng thủ module nền cũ (rc=2 trên REVIEW): GIỮ ngữ nghĩa --strict — rc=1 khi --strict, rc=0 khi không.
    if rc == 2:
        rc = 1 if strict else 0
    return rc


def _status_amendment_registry_guard(a) -> tuple[dict, int] | None:
    """Guard offline cho `status <sohieu> --amendment`: nếu registry đã có số hiệu này trong corpus thì không ADD."""
    if not getattr(a, "amendment", False):
        return None
    q = str(getattr(a, "sohieu", "") or "").strip()
    if not q or not _looks_like_sohieu_query(q):
        return None
    qkey = norm_sohieu(q.replace("_", "-"))
    try:
        entries = _manifest_entries(refresh=bool(getattr(a, "refresh", False)))
    except Exception:
        return None
    hits = []
    for e in entries or []:
        sh = _sohieu_key_entry(e)
        if not sh:
            continue
        if not (_sohieu_query_hits_entry(qkey, sh) or _sohieu_query_hits_entry(sh, qkey)):
            continue
        if _entry_corpus_true(e) and _entry_row_kind(e) != "ref":
            hits.append(e)
    if not hits:
        return None
    hits.sort(key=lambda e: (_entry_on_nlm_live(e), _entry_score(e), _entry_name(e)), reverse=True)
    canonical = hits[0]
    on_nlm = _entry_on_nlm_live(canonical)
    decision = "SKIP" if on_nlm else "REVIEW"
    surface = "AMENDMENT_ALREADY_IN_CORPUS_ON_NLM" if on_nlm else "AMENDMENT_ALREADY_IN_CORPUS"
    reason = ("Văn bản sửa đổi đã có trong registry/corpus và đã trên NLM"
              if on_nlm else "Văn bản sửa đổi đã có trong registry/corpus; cần kiểm trạng thái NLM/hiệu lực")
    res = {
        "decision": decision,
        "verdict": decision,
        "reason": reason,
        "surface": surface,
        "flags": [surface, "NO_DUPLICATE_INGEST"],
        "canonical": _summ_entry_source_map(canonical),
        "registry_hits": [_summ_entry_source_map(e) for e in hits[:10]],
        "actions": [
            "KHÔNG nạp trùng văn bản sửa đổi này.",
            "Nếu cần rà nội dung, dùng canonical trong registry; nếu thiếu hiệu lực thì chạy `tl backfill-hieuluc`.",
            "Nếu nghi cache cũ, lặp lại với `tl status <sohieu> --amendment --refresh`.",
        ],
    }
    strict = bool(getattr(a, "strict", False))
    return res, (1 if strict and decision == "REVIEW" else 0)


def _relation_refs(e: dict) -> set[str]:
    return _goc_keys(e) | _ref_tokens(_field_text(e, _REF_KEYS + _META_TITLE_KEYS))


def _is_amendment_like(e: dict) -> bool:
    """Nhận diện văn bản sửa đổi/bổ sung kể cả khi registry chưa điền goc/sua_doi.

    Giữ rộng có kiểm soát: bắt cả tên file Việt Nam kiểu SuaDoi/SDBS và metadata tiếng Anh
    nếu corpus sau này có nhãn amendment/amended. Không coi VBHN là amendment.
    """
    if _is_vbhn_entry(e):
        return False
    text = _strip_accents(" ".join([
        _entry_name(e), str(e.get("loai") or ""), _field_text(e, _META_TITLE_KEYS + _REF_KEYS)
    ])).lower()
    compact = re.sub(r"[^a-z0-9]+", "", text)
    markers = (
        "sua doi", "bo sung", "sua doi bo sung", "mot so dieu",
        "luat sua doi", "nghi quyet sua doi", "thong tu sua doi",
        "amendment", "amended",
    )
    return any(x in text for x in markers) or any(x in compact for x in ("suadoi", "bosung", "suadoibosung", "sdbs", "motsodieu"))


def _header_verify_infer_cats(entry: dict) -> tuple[list[str], str]:
    """v1.33.20 (MERGE bundle-20 KIẾN TRÚC, sửa guard): CAT-inference DÙNG CHUNG cho header-verify check-4 +
    fix_suggest — 3 surface kiểm cat (cat-audit/corpus-audit/header-verify) cùng MỘT nguồn suy luận, cả 2 chiều
    (giữ-đúng-chỗ + bắt-nằm-nhầm-chỗ). Trả (cats, rule). SỬA 2 lỗi bản bundle-20 (phản chứng chạy được):
    - chiều ĐỀ XUẤT vào-46 chỉ đi text-pattern chặt (_omnibus_name_text); bundle dùng _omnibus_name_evidence
      (nhánh ≥2-refs) → 71-2020 SuaDoi_HIV goc+related nằm ĐÚNG 45 bị flag 45→46 (đúng lỗi r29 đã khoá 2 lần);
      refs-evidence CHỈ dùng chiều SUPPRESS (đang ở 46 thì giữ).
    - cat 00/23 (Đảng/điều ước): trả RỖNG = check KHÔNG ÁP DỤNG (mirror cat-audit skip) — bundle chỉ chắn 23
      khi tên khớp prefix treaty, doc trong 23/00 tên khác vẫn bị suy thô."""
    name = _entry_name(entry)
    cc = re.sub(r"\D", "", str(_entry_cat(entry)))[:2]
    if cc in ("00", "23"):
        return ([], f"cat-{cc}-not-applicable")
    if not _is_vbhn_entry(entry):
        if cc == "46" and (_omnibus_name_text(name) or _omnibus_name_evidence(entry)):
            return (["46"], "omnibus-46")          # SUPPRESS: evidence rộng (text + refs)
        if _omnibus_name_text(name):
            return (["46"], "omnibus-46")          # PROPOSE vào-46: text-pattern chặt, KHÔNG refs (r29)
    if _is_treaty_entry(entry):
        return (["23"], "treaty-23")               # điều ước nằm ngoài 23 → đề xuất về 23
    forced, rule = _cat_boundary_rule(name)
    if forced:
        return ([forced], rule or "boundary")
    return (_infer_cats(name) or [], "")


def _relation_candidate_flags(e: dict, base_key: str = "", subject: str = "") -> list[str]:
    flags = list(_title_flags(e))
    refs = _relation_refs(e)
    if base_key and base_key not in refs:
        flags.append("RELATION_METADATA_MISSING_GOC")
    if subject and _subject_score(e, subject) < 30:
        flags.append("SUBJECT_WEAK_MATCH")
    if _entry_nlm(e):
        status = str(e.get("nlm_status") or "").lower()
        if status and not _nlm_status_known(status):
            flags.append("NLM_STATUS_MISMATCH")
    else:
        flags.append("NOT_ON_NLM")
    out = []
    for f in flags:
        if f and f not in out:
            out.append(f)
    return out


def _relation_backfill_items(missing_links: list, entries: list) -> list:
    """KH1 Pha 1.5 (PURE, test offline): từ `missing_links` của _relation_audit → items reg_bulk.
    BACKFILL_GOC_ON_AMENDMENT → {drive_id, goc, _cols:'goc'}. BACKFILL_SUA_DOI_ON_BASE → {drive_id, sua_doi, _cols:'sua_doi'}
    (HỢP NHẤT với sua_doi HIỆN CÓ + dedup, KHÔNG đè mất quan hệ cũ)."""
    by_did = {_entry_drive_id(e): e for e in entries or []}
    items = []
    for ml in missing_links or []:
        did = ml.get("drive_id")
        if not did:
            continue
        if ml.get("action") == "BACKFILL_GOC_ON_AMENDMENT" and ml.get("set_goc"):
            items.append({"drive_id": did, "goc": ml["set_goc"], "_cols": "goc"})
        elif ml.get("action") == "BACKFILL_SUA_DOI_ON_BASE":
            e = by_did.get(did, {})
            cur = [x.strip() for x in re.split(r"[;,|]+", str(_entry_sua_doi(e) or "")) if x.strip()]
            merged = cur + [x for x in (ml.get("add") or []) if x and x not in cur]
            if merged:
                items.append({"drive_id": did, "sua_doi": ";".join(merged), "_cols": "sua_doi"})
    return items


def cmd_relation_backfill(a) -> int:
    """KH1 Pha 1.5 (cho KH2 Pha 2.3): GHI quan hệ sửa đổi mà relation-check ĐÃ phát hiện — set `goc` cho luật SỬA, append
    `sua_doi` cho luật GỐC (missing_links từ _relation_audit, tái dùng cổng chống dương-tính-giả). CHỈ backfill quan hệ ĐỦ
    ĐIỀU KIỆN (direct/ref-linked); ca chỉ-trùng-chủ-đề → BỎ vào review (xác minh tay). DRY mặc định; --apply ghi reg_bulk."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] relation-backfill: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    base = getattr(a, "base", None) or ""
    subject = getattr(a, "subject", None) or ""
    if not base and not subject:
        print("[tl] relation-backfill cần --base <sohieu> (hoặc --subject).", file=sys.stderr); return 2
    audit = _relation_audit(entries, base=base, subject=subject)
    items = _relation_backfill_items(audit.get("missing_links", []), entries)
    review = audit.get("subject_only_review", [])
    if getattr(a, "apply", False):
        _ok_gate, _ = _apply_gate(a, write_cols="goc,sua_doi")
        if not _ok_gate:
            return 2
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        except (Exception, SystemExit):
            pass
        g = _gas()
        run_id = _apply_journal_start("relation-backfill", {"n": len(items)})
        written = 0
        for it in items:
            col = it.get("_cols", "goc")
            v = _journaled_reg_write(run_id, g, [{k: val for k, val in it.items() if k != "_cols"}], col)
            if v.get("verified"):
                written += 1
        _invalidate_manifest_cache()
        _journal_append(run_id, {"t": "run_end", "ok": True, "counts": {"backfilled": written}})
        print(json.dumps({"ok": True, "base": base or subject, "backfilled": written, "proposed": len(items),
                          "journal": run_id, "subject_only_review": len(review)}, ensure_ascii=False))
        print(f"[tl] relation-backfill: ghi {written}/{len(items)} quan hệ; {len(review)} ca subject-only BỎ (xác minh tay). MANIFEST_STALE: cache cũ → chạy `tl boot --refresh` (hoặc `tl manifest` nếu đổi cây Drive).", file=sys.stderr)
        return 0
    out = {"ok": True, "mode": "DRY", "base": base or subject, "count": len(items),
           "backfill_items": [{k: v for k, v in it.items() if k != "_cols"} for it in items],
           "subject_only_review": review,
           "note": "DRY — --apply để ghi goc/sua_doi. Ca chỉ-trùng-chủ-đề KHÔNG auto-ghi (xác minh nguyên văn). Bắt thêm "
                   "quan hệ qua footnote-map VBHN: chạy `tl relation-check --base <x>` trước (đọc base)."}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== relation-backfill DRY · base={base or subject} · {len(items)} quan hệ đề xuất · {len(review)} subject-only BỎ ==")
        for it in items:
            act = ("goc=" + it.get("goc", "")) if "goc" in it else ("sua_doi+=" + (it.get("sua_doi", "")[:44]))
            print(f"  {it['drive_id'][:14]:14s} {act}")
        if review:
            print(f"  ({len(review)} ca chỉ-trùng-chủ-đề → xác minh tay, KHÔNG auto-ghi)")
        print("  → --apply để ghi.")
    return 0


def cmd_relation_check(a) -> int:
    """Soi quan hệ sửa đổi/VBHN đã có trong corpus nhưng registry thiếu goc/sua_doi."""
    if getattr(a, "refresh", False) or not (_cache_file("manifest.json")).exists():
        load_creds(getattr(a, "config", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] relation-check: không đọc được manifest: {e}", file=sys.stderr)
        return 1
    amendments = []
    for raw in getattr(a, "amendment", None) or []:
        amendments.extend([x.strip() for x in re.split(r"[;,|]+", raw) if x.strip()])
    # Cổng footnote-map (#8 HỢP NHẤT): lấy bản đồ sửa đổi cấp Điều của VBHN base làm nguồn XÁC THỰC. Ưu tiên
    # --footnote-source/--footnote-file; nếu KHÔNG có thì TỰ resolve base→VBHN gdoc rồi đọc (auto, best-effort) →
    # relation-check tự nêu footnote_amendments thay vì rỗng. Tắt: --no-auto-footnote.
    footnote_keys = None
    fn_full = None
    base_subject_omni = getattr(a, "subject", "") or getattr(a, "base", "") or ""
    fsrc = getattr(a, "footnote_source", None)
    ffile = getattr(a, "footnote_file", None)
    text = ""
    try:
        if ffile:
            text = Path(ffile).read_text(encoding="utf-8", errors="replace")
        elif fsrc:
            gid = fsrc
            if "/" in fsrc or not re.fullmatch(r"[A-Za-z0-9_\-]{20,}", fsrc):
                hits = resolve_identity(fsrc, entries, max_hits=1)
                if hits:
                    gid = _entry_drive_id(hits[0][0])
            load_creds(getattr(a, "config", None))
            text = _read_doc_text(gid, getattr(a, "config", None))
        elif getattr(a, "base", None) and not getattr(a, "no_auto_footnote", False):
            _be, _bg, _bs = _resolve_base_gdoc(getattr(a, "base", ""), entries)
            if _be is not None and _bg:
                base_subject_omni = _bs or base_subject_omni
                load_creds(getattr(a, "config", None))
                text = _read_doc_text(_bg, getattr(a, "config", None)) or ""
                if text and not a.json:
                    print(f"[tl] relation-check: tự đọc nguyên văn base '{_entry_name(_be)[:50]}' → footnote-map (auto; tắt: --no-auto-footnote).", file=sys.stderr)
    except (Exception, SystemExit) as e:  # noqa: BLE001 — load_creds có thể sys.exit khi thiếu creds → KHÔNG giết lệnh
        if not a.json:
            print(f"[tl] relation-check: không đọc được footnote text ({e}); bỏ qua cổng footnote (vẫn chặn subject-only).", file=sys.stderr)
        text = ""
    inline_amends: list[str] = []
    if text:
        fn_full = resolve_footnote_amendments(text, entries=entries)
        # CHỈ coi là sửa-đổi-base các số hiệu THỰC SỰ map vào 1 Điều base (mapped_sohieu = def is_amend + có amending_sohieu).
        # KHÔNG union footnote_sohieu (= MỌI số hiệu xuất hiện trong khối chú thích: dẫn chiếu/chuyển tiếp/"quy định tại
        # Luật X") — union đó bơm phồng footnote_only_amendments / FOOTNOTE_AMENDMENT_NOT_IN_CORPUS bằng luật chỉ-dẫn-chiếu.
        footnote_keys = set(fn_full.get("mapped_sohieu") or [])
        # ĐIỀU KHOẢN LỒNG: base text có thể chứa Điều "sửa đổi, bổ sung … của Luật … số X" → base SỬA X tại chỗ.
        # Surface quan hệ này (registry thường trống goc/sua_doi) để đề xuất backfill, kể cả khi base KHÔNG phải VBHN.
        inline_amends = _scan_inline_amendments(text)
    out = _relation_audit(entries, base=getattr(a, "base", "") or "", subject=getattr(a, "subject", "") or "", amendments=amendments, footnote_amend_keys=footnote_keys)
    if inline_amends:
        _bk = out.get("base_key")
        out["inline_amendments"] = [{"amended_sohieu": k,
                                     "in_corpus": any(_sohieu_query_hits_entry(k, _sohieu_key_entry(e)) for e in entries)}
                                    for k in inline_amends if k != _bk]   # v1.33.47: +bare-VBHN 1 chiều
        if out["inline_amendments"]:
            out["warnings"].append("INLINE_AMENDMENT_SCANNED: nguyên văn base có Điều 'sửa đổi, bổ sung của Luật … số X' "
                                   "(điều khoản lồng) — đề xuất backfill goc/sua_doi giữa base và các số hiệu trong inline_amendments; "
                                   "đọc nguyên văn xác minh trước khi ghi registry.")
    if fn_full:   # #8/#11: nêu RÕ các sửa đổi cấp Điều từ footnote + cờ OMNIBUS cross-domain
        fa = []
        for r in fn_full["dieu_level_amendment_map"]:
            _ash = r.get("amending_sohieu")
            _omni = _omnibus_cross_domain_note(_ash or "", base_subject_omni, entries)
            fa.append({"dieu": r.get("dieu"), "khoan": r.get("khoan"), "amending_sohieu": _ash,
                       # v1.33.47: +bare-VBHN 1 chiều (footnote hay ghi số VBHN không năm)
                       "in_corpus": (any(_sohieu_query_hits_entry(norm_sohieu(_ash).replace("/", "-"), _sohieu_key_entry(e))
                                         for e in entries) if _ash else None),
                       "pending_effect": r.get("pending_effect"), "hieu_luc": r.get("hieu_luc"),
                       **({"omnibus_note": _omni} if _omni else {})})
        out["footnote_amendments"] = fa
        out["omnibus_cross_domain"] = [x for x in fa if x.get("omnibus_note")]
    out["google_discovery"] = _discovery_links(out.get("subject") or out.get("base") or "")["links_markdown"]
    if a.json:
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== tl relation-check — base={out.get('base') or '∅'} subject={out.get('subject') or '∅'} ==")
        for w in out["warnings"]:
            print(f"⚠ {w}")
        for it in out["amendment_candidates"]:
            e = it["entry"]
            print(f"- SỬA ĐỔI: {e['name'][:90]} | sohieu={e['sohieu'] or '∅'} | nlm={e['nlm']} | flags={','.join(it['flags']) or 'OK'}")
        for it in out["vbhn_candidates"]:
            e = it["entry"]
            print(f"- VBHN: {e['name'][:90]} | sohieu={e['sohieu'] or '∅'} | nlm={e['nlm']} | flags={','.join(it['flags']) or 'OK'}")
        if out["missing_links"]:
            print("Hành động registry cần hỏi người dùng trước khi ghi:")
            for m in out["missing_links"]:
                print(f"  - {m}")
        if out.get("subject_only_review"):
            print("CHỈ trùng chủ đề (KHÔNG auto-backfill — xác minh nguyên văn thủ công):")
            for r in out["subject_only_review"]:
                print(f"  - {r['sohieu'] or '∅'} | {r['name']} → {r['note']}")
        if out.get("footnote_amendments"):
            print("SỬA ĐỔI CẤP ĐIỀU từ footnote-map của VBHN (đã hợp nhất — #8):")
            for fa in out["footnote_amendments"]:
                _mc = "?" if fa["in_corpus"] is None else ("✓corpus" if fa["in_corpus"] else "✗thiếu-corpus")
                _pe = " ⏳PENDING" if fa.get("pending_effect") else ""
                _om = " ⚠OMNIBUS" if fa.get("omnibus_note") else ""
                print(f"  - Điều {fa['dieu']} {('K'+fa['khoan']) if fa.get('khoan') else ''} ← {fa['amending_sohieu'] or '?'} {_mc}{_pe}{_om}")
        if out.get("omnibus_cross_domain"):
            print("⚠ OMNIBUS / SỬA-NHIỀU-LUẬT (luật sửa có tên khác lĩnh vực base — KHÔNG phải lỗi, đọc nguyên văn xác nhận):")
            for fa in out["omnibus_cross_domain"]:
                print(f"  - {fa['amending_sohieu']}: {fa['omnibus_note'].split(': ', 1)[-1][:120]}")
        if out.get("footnote_only_amendments"):
            print("Sửa đổi CÓ trong footnote-map của VBHN nhưng THIẾU trong corpus (nạp QT-5 trước khi kết luận):")
            for k in out["footnote_only_amendments"]:
                print(f"  - {k}")
        if out["vbhn_queries"]:
            print("Truy vấn VBHN ngoài corpus bắt buộc trước khi kết luận:")
            for q in out["vbhn_queries"]:
                print(f"  - {q}")
        if out.get("google_discovery"):
            print("Tìm trên web (GOOGLE site:, VBHN-first — ưu tiên cách này):")
            for ln in out["google_discovery"]:
                print(f"  {ln}")
    return 0


def _vbhn_goc_map(entries: list) -> dict:
    """PURE (v1.34.32 — VBHN-FIRST TẤT ĐỊNH): map `norm_sohieu(gốc/luật-sửa) → [sohieu VBHN corpus SẠCH phủ nó]`
    từ 2 field registry TẤT ĐỊNH: `goc` (';'-cách) + `sua_doi` dạng 'Hợp nhất từ: a, b' + pattern tên `goc_<sohieu>`.
    CHỈ tính VBHN corpus=true không-quarantine. KHÔNG fuzzy subject (gốc sự cố 46% false-positive sweep 2026-07-11)."""
    out = {}
    for e in entries or []:
        if _normalize_loai(str(e.get("loai") or "")) != "Văn bản hợp nhất":
            continue
        # r258 (P15, cùng gốc r257 — nửa CÒN LẠI của cùng một lệnh): map "đã phủ" này SUPPRESS
        # amendments_missing, nên khái niệm "in corpus" ở đây phải là LUẬT SERVER, giống cổng vbhn_broken.
        # `_entry_corpus_true` lệch HAI HƯỚNG, và hướng nguy hiểm là hướng ít ai để ý:
        #  · THIẾU `− ref`: dòng row_kind='ref' là dòng TRỎ-tham-chiếu, KHÔNG phải văn bản sở hữu, mà vẫn được
        #    tính là VBHN đã phủ ⇒ CHE MẤT amendments_missing THẬT. Chính hàm này lúc chọn base_docs đã viết
        #    `not _entry_corpus_true(e) or _entry_row_kind(e) == "ref"` — tác giả biết phải trừ ref, nửa map bỏ sót.
        #    Thiếu luôn `− loai='thuong'` (văn bản hành chính không bao giờ là VBHN phủ VBQPPL).
        #  · BỎ SÓT `corpus='vbqppl'` + `row_kind='overflow'`: server (tl boot) ĐẾM chúng là corpus, nên không
        #    tính là đã-phủ mới là dương-tính-giả amendments_missing (giục tải bản gốc đã có VBHN phủ).
        # Vế quarantine: `"_ZZZ_QUARANTINE" in cat` bỏ sót nhãn 'QUARANTINE' trơ ⇒ VBHN đã cách ly vẫn được
        # tính là phủ (che gap). Dùng helper — hướng SIẾT, an toàn.
        if not _entry_is_corpus_effective(e) or _is_quarantine_cat(_entry_cat(e)):
            continue
        vb_label = _entry_sohieu(e) or str(_entry_name(e) or "")[:40]
        keys = set()
        for part in re.split(r"[;,]", str(_entry_goc(e) or "")):
            if part.strip():
                keys.add(norm_sohieu(part.strip()))
        m = re.search(r"Hợp nhất từ:\s*(.+)", str(e.get("sua_doi") or ""))
        if m:
            for part in re.split(r"[;,]", m.group(1)):
                if part.strip():
                    keys.add(norm_sohieu(part.strip()))
        for mt in re.finditer(r"goc[_-]([0-9A-Za-z\-]{6,})", str(_entry_name(e) or ""), re.I):
            keys.add(norm_sohieu(mt.group(1)))
        for k in keys:
            if k:
                out.setdefault(k, []).append(vb_label)
    return out


def cmd_corpus_relation_sweep(a) -> int:
    """#T1 (v1.34.31 + VBHN-FIRST v1.34.32): BATCH `relation-check` trên toàn bộ Luật/NQ corpus (hoặc --loai/--cat
    lọc) — GỘP 'nguồn liên quan cần bổ sung' vào 1 báo cáo. VBHN-FIRST TẤT ĐỊNH (rà 2026-07-11 bắt 4/7 đề xuất sai +
    46% vbhn false-positive): (1) amendment thiếu NHƯNG chuỗi đã có VBHN corpus phủ (map `goc`/'Hợp nhất từ' registry)
    → `covered_by_vbhn`, KHÔNG vào sources_to_add; (2) `vbhn_broken` CHỈ giữ khi có GOC-TIE tất định (goc VBHN ứng
    viên ∩ {base ∪ các luật-sửa}) — hết matcher fuzzy subject gán VBHN Thư viện cho Luật Thủ đô; (3) base nằm trong
    chuỗi VBHN → `vbhn_first_self` (advisory: bản rời gốc/sửa-đổi là redundant với VBHN). STREAM per-doc stderr +
    resumable --skip + --out. READ-ONLY (qua chính cmd_relation_check — SCRIPT-REUSE #15). --deep đọc nguyên văn."""
    import argparse as _ap, io as _io, contextlib as _ctx
    if getattr(a, "refresh", False) or not (_cache_file("manifest.json")).exists():
        load_creds(getattr(a, "config", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] corpus-relation-sweep: không đọc được manifest: {e}", file=sys.stderr)
        return 1
    vbhn_goc = _vbhn_goc_map(entries)
    goc_by_drive_id = {}
    # r253: entry ĐẦY ĐỦ theo drive_id — cổng đủ-điều-kiện-vbhn_broken phải xét trên entry THẬT, không xét
    # trên bản `_summ_entry` (bản đó KHÔNG có `loai` nên luật server đọc thiếu trường và nghiêng về suppression).
    entry_by_drive_id = {}
    for e in entries:
        did = _entry_drive_id(e)
        if did:
            entry_by_drive_id[str(did)] = e
            ks = {norm_sohieu(p.strip()) for p in re.split(r"[;,]", str(_entry_goc(e) or "")) if p.strip()}
            ks |= {norm_sohieu(mt.group(1)) for mt in re.finditer(r"goc[_-]([0-9A-Za-z\-]{6,})",
                                                                  str(_entry_name(e) or ""), re.I)}
            if ks:
                goc_by_drive_id[str(did)] = ks
    loai_raw = getattr(a, "loai", None) or "Luật,Nghị quyết"
    loai_norm = {_normalize_loai(x.strip()) for x in re.split(r"[;,|]+", loai_raw) if x.strip()}
    cat_filter = (getattr(a, "cat", None) or "").strip()
    seen, base_docs = set(), []
    for e in entries:
        if not _entry_corpus_true(e) or _entry_row_kind(e) == "ref":
            continue
        sh = _entry_sohieu(e)
        if not sh:
            continue
        if loai_norm and _normalize_loai(str(e.get("loai") or "")) not in loai_norm:
            continue
        if cat_filter and not str(_entry_cat(e)).startswith(cat_filter):
            continue
        k = norm_sohieu(sh)
        if k in seen:
            continue
        seen.add(k)
        base_docs.append(e)
    base_docs.sort(key=lambda e: _entry_sohieu(e))
    total = len(base_docs)
    skip = max(0, int(getattr(a, "skip", 0) or 0))
    limit = int(getattr(a, "limit", 0) or 0)
    run = base_docs[skip:(skip + limit)] if limit > 0 else base_docs[skip:]
    deep = bool(getattr(a, "deep", False))
    results = []
    for idx, e in enumerate(run, 1):
        sh = _entry_sohieu(e)
        ns = _ap.Namespace(config=getattr(a, "config", None), profile=getattr(a, "profile", None),
                           base=sh, subject=str(e.get("title_vn") or ""), amendment=None,
                           footnote_source=None, footnote_file=None, no_auto_footnote=(not deep),
                           refresh=False, json=True, deterministic=False)
        buf = _io.StringIO()
        try:
            with _ctx.redirect_stdout(buf), _ctx.redirect_stderr(_io.StringIO()):
                cmd_relation_check(ns)
            rc = json.loads(buf.getvalue() or "{}")
        except Exception as ex:  # noqa: BLE001
            rc = {"ok": False, "error": f"{type(ex).__name__}: {ex}"}
        base_key = norm_sohieu(sh)
        inline_all = rc.get("inline_amendments") or []
        chain_keys = {base_key} | {norm_sohieu(str(ia.get("amended_sohieu") or "")) for ia in inline_all}
        chain_keys.discard("")
        # VBHN-FIRST (1): amendment thiếu-corpus NHƯNG đã có VBHN corpus phủ (goc-map tất định) → covered, KHÔNG fetch.
        amend_missing, amend_covered = [], []
        for ia in inline_all:
            if ia.get("in_corpus") is not False:
                continue
            _ak = norm_sohieu(str(ia.get("amended_sohieu") or ""))
            _cov = vbhn_goc.get(_ak)
            if _cov:
                amend_covered.append({**ia, "covered_by_vbhn": sorted(set(_cov))[:4]})
            else:
                amend_missing.append(ia)
        # VBHN-FIRST (2): vbhn_broken CHỈ khi GOC-TIE tất định — goc của VBHN ứng viên giao chuỗi {base ∪ luật-sửa}.
        # (Matcher subject của relation-check từng gán VBHN Thư viện cho Luật Thủ đô — 46% false-positive.)
        vbhn_broken, vbhn_dropped_no_tie = [], 0
        for vc in (rc.get("vbhn_candidates") or []):
            fl = vc.get("flags") or []
            ent = vc.get("entry") or {}
            # r257 (P15): cổng này TỪNG dùng 2 vị từ THÔ, cả hai lệch khuôn nhà — đúng lớp dương-tính-giả mà
            # VBHN-FIRST v1.34.32 sinh ra để diệt, chỉ khác chỗ.
            #  · `str(ent.get("corpus")) != "true"` là site DUY NHẤT trong repo so cột corpus mà KHÔNG chuẩn hoá
            #    (28 site khác đều .lower()/helper). Miền giá trị THẬT rộng hơn {true,false}: 'vbqppl' (luật
            #    server corpus∈{true,vbqppl} — hygiene 3015/3025, cli 359 nói thẳng `--corpus true` literal
            #    "bỏ sót vbqppl/overflow"), 'thuong', '', và mọi biến thể hoa/khoảng-trắng ⇒ VBHN corpus LÀNH bị
            #    coi là NGOÀI corpus, có goc-tie là vào sources_to_add giục tải lại thứ đã có.
            #    Dùng LUẬT SERVER (_entry_is_corpus_effective), KHÔNG dùng _entry_corpus_true — literal là bản SAI.
            #  · `"_ZZZ_QUARANTINE" in cat` bỏ sót biến thể nhãn 'QUARANTINE' trơ (thứ _is_quarantine_label_variant
            #    xác nhận có thật) ⇒ VBHN ĐÃ cách ly trong chuỗi base lọt lưới, KHÔNG được gắn cờ.
            # Hai vế đi NGƯỢC hướng nhau (corpus: bớt cờ · quarantine: thêm cờ) nên test r257 khoá CẢ HAI chiều.
            _full = entry_by_drive_id.get(str(ent.get("drive_id") or "")) or ent
            if not (any(f in ("RAW_NAME_NOT_NLM", "VBHN_MISSING_YEAR_OR_DATE") for f in fl)
                    or not _entry_is_corpus_effective(_full)
                    or _is_quarantine_cat(_entry_cat(_full))):
                continue
            _cand_goc = goc_by_drive_id.get(str(ent.get("drive_id") or ""), set())
            _cand_goc = _cand_goc | ({norm_sohieu(str(ent.get("sohieu") or ""))} - {""})
            if _cand_goc & chain_keys:
                vbhn_broken.append({"sohieu": ent.get("sohieu"), "name": str(ent.get("name") or "")[:60],
                                    "flags": fl, "goc_tie": sorted(_cand_goc & chain_keys)})
            else:
                vbhn_dropped_no_tie += 1
        # VBHN-FIRST (3): CHÍNH base nằm trong chuỗi hợp nhất của VBHN corpus → bản rời redundant (advisory).
        _self_cov = vbhn_goc.get(base_key) or []
        missing_links = rc.get("missing_links") or []
        has_gap = bool(amend_missing or vbhn_broken or missing_links)
        results.append({"sohieu": sh, "loai": str(e.get("loai") or ""), "name": str(_entry_name(e) or "")[:60],
                        "amendments_missing": amend_missing, "covered_by_vbhn": amend_covered,
                        "vbhn_broken": vbhn_broken,
                        **({"vbhn_dropped_no_tie": vbhn_dropped_no_tie} if vbhn_dropped_no_tie else {}),
                        **({"vbhn_first_self": sorted(set(_self_cov))[:4]} if _self_cov else {}),
                        "missing_links": missing_links,
                        "google_discovery": (rc.get("google_discovery") or [])[:3] if has_gap else [],
                        **({"error": rc["error"]} if rc.get("error") else {})})
        print(f"[sweep] ({skip + idx}/{total}) {sh}: "
              f"{len(amend_missing) + len(vbhn_broken) + len(missing_links)} gap(s)", file=sys.stderr, flush=True)
    to_add = []
    for r in results:
        for ia in r["amendments_missing"]:
            to_add.append({"needed_sohieu": ia.get("amended_sohieu"), "reason": "amended_base_not_in_corpus",
                           "for": r["sohieu"]})
        for vb in r["vbhn_broken"]:
            to_add.append({"needed_sohieu": vb.get("sohieu"), "reason": "vbhn_broken_or_quarantine",
                           "for": r["sohieu"], "flags": vb.get("flags")})
    done = skip + len(run)
    _covered_n = sum(len(r.get("covered_by_vbhn") or []) for r in results)
    _self_n = sum(1 for r in results if r.get("vbhn_first_self"))
    out = {"ok": True, "action": "corpus-relation-sweep", "mode": "DEEP" if deep else "FAST",
           "loai_filter": sorted(loai_norm), "total": total, "swept": len(run),
           "docs_with_gaps": sum(1 for r in results if r["amendments_missing"] or r["vbhn_broken"] or r["missing_links"]),
           "covered_by_vbhn_count": _covered_n, "vbhn_first_self_docs": _self_n,
           "sources_to_add_count": len(to_add), "sources_to_add": to_add, "per_doc": results,
           "note": "VBHN-FIRST: amendments_missing = VB bị base sửa, chưa có corpus VÀ chưa VBHN nào phủ (goc-map "
                   "tất định) — chỉ nhóm này cần fetch; covered_by_vbhn = thiếu bản rời nhưng VBHN đã phủ (KHÔNG "
                   "fetch); vbhn_broken = VBHN hỏng CÓ goc-tie với chuỗi base (fuzzy-subject đã loại); "
                   "vbhn_first_self = bản rời của base đã nằm trong chuỗi VBHN (ứng viên redundant, advisory)."}
    if done < total:
        _flags = ((" --deep" if deep else "")
                  + (f' --loai "{loai_raw}"' if getattr(a, "loai", None) else "")
                  + (f" --cat {cat_filter}" if cat_filter else ""))
        out["remaining"] = total - done
        out["resume_command"] = f"tl corpus-relation-sweep{_flags} --limit {limit or len(run)} --skip {done} --json"
    _o = getattr(a, "out", None)
    if _o:
        Path(_o).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        print(json.dumps({"ok": True, "out": _o, "total": total, "swept": len(run),
                          "sources_to_add_count": len(to_add), "docs_with_gaps": out["docs_with_gaps"],
                          **({"resume_command": out["resume_command"]} if out.get("resume_command") else {})},
                         ensure_ascii=False))
    else:
        print(json.dumps(out, ensure_ascii=False))
    return 0


def _amendments_covered_by_vbhn_date(vbhn: dict | None, amendments: list[dict]) -> tuple[bool, str | None, list[dict]]:
    """(port Codex hotfix) True khi VBHN ban hành ≥ TẤT CẢ luật-sửa. Cổng PHỤ hạ PAUSE cho luật-sửa CHƯA nằm trong
    chuỗi goc VBHN nhưng VBHN ra đời SAU (đã phản ánh) — bổ trợ cổng consolidation goc-chain.
    v1.29.6 (log 118 Luật — P0c: cổng im lặng vì manifest THIẾU ngày → 9/15 base-là-VBHN vẫn PAUSE giả): FALLBACK
    so theo NĂM khi thiếu full-date — năm VBHN từ issue_year/sohieu-key ('25-2026-VBHN-VPQH'→2026), năm luật-sửa từ
    sohieu-key ('90-2025-QH15'→2025). CHỈ cover khi năm VBHN > năm luật-sửa (STRICT — bằng năm = mơ hồ, không kết
    luận, an toàn). Full-date cả 2 phía vẫn so ngày như cũ (chính xác hơn)."""
    if not vbhn or not _is_vbhn_entry(vbhn) or not amendments:
        return False, None, []
    vbhn_date = _entry_issue_date_iso(vbhn)
    vbhn_year = _entry_issue_year(vbhn) or _sohieu_year(_sohieu_key_entry(vbhn))
    if not vbhn_date and not vbhn_year:
        return False, None, []
    _vbhn_label = vbhn_date or f"{vbhn_year} (year-only)"
    dated = []
    for e in amendments:
        d = _entry_issue_date_iso(e)
        if vbhn_date and d:
            if d > vbhn_date:
                return False, _vbhn_label, dated
            dated.append({"entry": e, "issue_date": d})
            continue
        # fallback NĂM (một trong hai phía thiếu full-date)
        ey = _sohieu_year(_sohieu_key_entry(e)) or _entry_issue_year(e)
        if not vbhn_year or not ey or ey >= vbhn_year:
            return False, _vbhn_label, dated      # thiếu năm / cùng-năm / mới hơn → KHÔNG kết luận covered (an toàn)
        dated.append({"entry": e, "issue_date": f"{ey} (year-only)"})
    return bool(dated), _vbhn_label, dated


def _source_map_flags(e: dict) -> list[str]:
    """Cờ HIỂN THỊ trong source-map. Một số cờ là hygiene toàn-cục (doctor/sweep), không phải lỗi riêng của luật đang rà."""
    return [f for f in _title_flags(e) if f not in _SRCMAP_GLOBAL_ONLY_FLAGS]


def _summ_entry_source_map(e: dict|None) -> dict|None:
    out = _summ_entry(e)
    if out is not None:
        out["flags"] = _source_map_flags(e)
    return out


def _source_map_verdict(item: dict) -> str:
    flags = set(item.get("flags") or _warning_codes(item.get("warnings") or []))
    if item.get("action_required") == "PAUSE_AND_ASK_USER" or "PAUSE_AND_ASK_USER" in flags:
        return "PAUSE_AND_ASK_USER"
    if not item.get("canonical") and not item.get("direct_hits") and not item.get("name_hits"):
        return "UNKNOWN_NOT_ABSENT"
    review = {
        "TITLE_OR_REGISTRY_WARN", "DIRTY_CANDIDATES", "GOC_SUBJECT_MISMATCH",
        "NO_VERIFIED_VBHN_IN_CORPUS", "QT5_WEB_REQUIRED", "LOW_CONFIDENCE_NAME_MATCH",
        "NAME_QUERY_SUBJECT_MISMATCH_NO_CANONICAL", "VBHN_REUSE_AMBIGUOUS_NO_CANONICAL",
        "VBHN_RECHECK_REQUIRED", "CORPUS_TRUE_NOT_ON_NLM", "DRAFT_NOT_EFFECTIVE",
        "AMENDMENT_CANDIDATE_LOW_CONFIDENCE",   # v1.29.6 P0b: weak candidates = REVIEW, không PAUSE
    }
    return "REVIEW" if flags & review else "OK"


def _vbhn_check_verdict(flags: list[str], has_main_candidates: bool) -> str:
    fs = set(flags or [])
    if "QT5_WEB_REQUIRED" in fs or "NO_CORPUS_MATCH_DO_NOT_CONCLUDE_ABSENT" in fs or "GOC_FILTER_NO_DIRECT_HIT" in fs:
        return "QT5_WEB_REQUIRED"
    if not has_main_candidates:
        return "UNKNOWN_NOT_ABSENT"
    if fs & {"CONTENT_VERIFY_REQUIRED", "SUBJECT_FILTER_WEAK", "GOC_NOT_EVIDENT_FILTERED"}:
        return "REVIEW"
    return "OK"


def cmd_header_verify(a) -> int:
    """G2 (cổng TÊN↔HEADER, HÀNG LOẠT): đọc HEADER thật → _verify_header_match (sohieu/title/loai/cat khớp registry).
    READ-ONLY (KHÔNG gán verified như confirm; bổ trợ confirm để soát 775 dòng cũ bắt DRIFT). --all|--sohieu|--drive-id|
    --cat NN. --fix-suggest gợi backfill (header_sohieu, cat suy tên, ngày/cơ quan từ header). rc=0 (phát hiện ≠ lỗi);
    --strict → rc=1 nếu có HEADER_MISMATCH. PHÂN BIỆT với title_mismatch (registry-doctor/hygiene = lệch metadata NỘI BỘ)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] header-verify: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    targets = _resolve_headerverify_targets(a, entries)
    if not targets:
        print("[tl] header-verify: không có target — dùng --all / --sohieu / --drive-id / --cat NN (+--limit).", file=sys.stderr); return 2
    results = []
    for e in targets:
        did = _entry_drive_id(e); nm = _entry_name(e)
        if _entry_raw_no_gdoc(e):
            results.append({"drive_id": did, "name": nm, "error": "ENTRY_RAW_NO_GDOC"}); continue
        try:
            txt = _read_doc_text(did, getattr(a, "config", None))
        except Exception as ex:  # noqa: BLE001
            results.append({"drive_id": did, "name": nm, "error": f"đọc header lỗi: {type(ex).__name__}"}); continue
        if not (txt or "").strip():
            results.append({"drive_id": did, "name": nm, "error": "header rỗng (kiểm gws/quyền)"}); continue
        vr = _verify_header_match(e, txt)
        row = {"drive_id": did, "name": nm, "sohieu": _entry_sohieu(e), "cat": _entry_cat(e),
               "ok": vr["ok"], "checks": vr["checks"], "mismatches": vr["mismatches"], "header_sohieu": vr["header_sohieu"]}
        if getattr(a, "fix_suggest", False):
            facts = _extract_header_facts(txt[: (getattr(a, "head_chars", None) or 6000)])
            # (B) engine CHUNG corpus-audit: thêm suggested_name/sohieu/cat + LỆNH sửa điền sẵn (propose-only), giữ khóa cũ.
            _ar = _corpus_audit_row(e, txt)
            # S-10 (v1.33.19): infer_cat CHỈ đề xuất khi check cat THẬT SỰ fail — cat pass/không-áp-dụng
            # (00/23/omnibus-46/boundary-confirmed) mà vẫn in ['34'] là mồi false recat cho driver.
            # v1.33.20 (MERGE bundle-20): dùng hàm chung + kèm infer_cat_rule máy-đọc giải thích nguồn suy luận.
            _fs_cats, _fs_rule = _header_verify_infer_cats(e)
            row["fix_suggest"] = {"backfill_sohieu": vr["header_sohieu"][:1],
                                  "infer_cat": (_fs_cats if vr["checks"].get("cat") is False else []),
                                  "infer_cat_rule": (_fs_rule if vr["checks"].get("cat") is False else ""),
                                  "issue_date": facts["issue_date"], "agency": facts["agency"],
                                  "proposals": _ar["proposals"]}
        results.append(row)
    mism = [r for r in results if (not r.get("error")) and r.get("ok") is False]
    err = [r for r in results if r.get("error")]
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "gate": "G2", "targets": len(results), "mismatch_count": len(mism),
                          "error_count": len(err), "results": results,
                          "header_mismatch": [r["drive_id"] for r in mism]}, ensure_ascii=False, indent=2))
    else:
        print(f"== header-verify (G2): {len(results)} target · {len(mism)} HEADER_MISMATCH · {len(err)} không đọc được ==")
        for r in results:
            if r.get("error"):
                print(f"  ✗ {r['name'][:55]} — {r['error']}"); continue
            mark = "✓ PASS" if r["ok"] else "✗ MISMATCH"
            cks = " ".join(f"{k}={'✓' if v else '✗'}" for k, v in r["checks"].items())
            print(f"  {mark}  {r['name'][:52]} | {cks}")
            for m in r["mismatches"]:
                print(f"        - {m}")
        print("  (READ-ONLY · gán verified: `tl confirm` · backfill: thêm --fix-suggest. KHÁC title_mismatch=lệch metadata nội bộ.)")
    return 1 if (getattr(a, "strict", False) and mism) else 0


def _rasoat_fallback_plan(sub: str, script: str, rest: list[str]) -> dict:
    """Kế hoạch đi vòng khi overlay thiếu script rà soát/backfill chuyên sâu.
    Đây không thay thế rasoat thật; nó giúp phiên trống không bị cụt workflow."""
    target = " ".join(rest).strip()
    return {
        "ok": False,
        "mode": "RASOAT_FALLBACK_PLAN",
        "missing_script": script,
        "subcommand": sub,
        "target_hint": target,
        "why": "Gói overlay chỉ có core runtime; rasoat/backfill chuyên sâu là optional script của bộ skill đầy đủ.",
        "safe_route": [
            "1) Chạy `tl boot` để dựng offline index; nếu boot lỗi thì dùng webapp find/manifest trực tiếp.",
            "2) Dùng `tl locate <số hiệu/tên>` để định vị canonical document trong corpus.",
            "3) Dùng webapp `exporttext`/`download` hoặc Drive MCP để lấy văn bản; dùng AI Tra Cứu Luật MCP để xác minh nguyên văn Điều/Khoản.",
            "4) Dùng NotebookLM MCP cho phân tích/tổng hợp; không coi NLM là nguồn nguyên văn duy nhất.",
            "5) Nếu cần pipeline tự động, cài bộ skill đầy đủ có script rasoat/backfill rồi chạy lại `tl rasoat ...`.",
        ],
        "suggested_commands": [
            "python scripts/tl.py doctor --deep",
            "python scripts/tl.py boot --json",
            "python scripts/tl.py locate <so-hieu-hoac-ten>",
            "python scripts/tl.py manifest --touched-drive --json",
        ],
    }


def _rasoat_map_positional(sub: str, rest) -> list:
    """#4: positional ĐẦU (số hiệu/file) → cờ chính của script rasoat đích (worksheet→--so-hieu, phuluc→--in),
    để `tl rasoat worksheet 18/VBHN-VPQH` chạy như `... --so-hieu 18/VBHN-VPQH`. No-op nếu đã có cờ / là -h / sub khác.

    r310: đường DISPATCH không còn dùng hàm này (positional/alias nay do argparse lo — `fills` +
    `flags:["--so-hieu","--sohieu","--so_hieu"]` trong RASOAT_SPECS). GIỮ lại vì nó là bản mô tả gọn nhất
    của quy ước positional, và ca `rasoat_worksheet_positional_maps_so_hieu` vẫn khoá quy ước đó."""
    rest = list(rest or [])
    # B1: ALIAS cờ — skill dùng `--sohieu` (không gạch) nhưng worksheet đòi `--so-hieu`; phuluc đòi `--in` thay `--file`.
    # Chuẩn hoá để KHỎI nhớ flag riêng từng script con (§14: dùng lệnh sẵn có, đừng bắt nhớ chi tiết). No-op nếu khác.
    _ALIAS = {"worksheet": {"--sohieu": "--so-hieu", "--so_hieu": "--so-hieu"},
              "phuluc": {"--file": "--in"}}.get(sub, {})
    if _ALIAS:
        rest = [_ALIAS.get(x, x) for x in rest]
    primary = {"worksheet": "--so-hieu", "phuluc": "--in"}.get(sub)
    if (primary and rest and not rest[0].startswith("-")
            and primary not in rest and not ({"-h", "--help"} & set(rest))):
        rest = [primary, rest[0]] + rest[1:]
    return rest


def _rasoat_autocache_worksheet(rest: list, a) -> None:
    """#3: `rasoat worksheet` cần docs/<sh>--<variant>.json. THIẾU → TỰ resolve <sh>→gdoc (manifest) rồi `cache-build`
    (auto-chain ingest) → hết "Không thấy cache, chạy ingest_to_cache.py". Best-effort: lỗi/không gdoc → worksheet tự báo."""
    try:
        sh = _flag_value(rest, "--so-hieu")
        if not sh:
            return
        variant = _flag_value(rest, "--variant") or "consolidated"
        cache_dir = _flag_value(rest, "--cache-dir") or str(CACHE)
        key = re.sub(r"[^a-z0-9]+", "-", sh.lower()).strip("-") + "--" + variant
        if (Path(cache_dir) / "docs" / (key + ".json")).exists():
            return                                        # đã có cache → khỏi dựng
        entries = _manifest_entries()
        _be, _bg, _ = _resolve_base_gdoc(sh, entries)
        if not _bg:
            print(f"[tl] rasoat worksheet: thiếu cache + KHÔNG resolve được gdoc cho {sh} → "
                  f"chạy `tl cache-build {sh} --gdoc-id <id>` thủ công.", file=sys.stderr)
            return
        print(f"[tl] rasoat worksheet: thiếu cache → TỰ dựng `tl cache-build {sh} --gdoc-id {_bg}`…", file=sys.stderr)
        cmd_cache_build(argparse.Namespace(sohieu=sh, rest=["--gdoc-id", _bg, "--variant", variant],
                                           config=getattr(a, "config", None), profile=getattr(a, "profile", None)))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] rasoat worksheet auto-cache bỏ qua ({type(e).__name__}: {e}).", file=sys.stderr)


def cmd_rasoat(a) -> int:
    """Passthrough tới script rà soát/backfill nếu có; nếu thiếu thì in fallback plan có cấu trúc.

    r310 (RAS-01 vế metadata/CLI · RAS-14) — ba thay đổi HÀNH VI, mỗi cái vá một lỗ:
      1. argv script con dựng từ NAMESPACE đã parse (`rasoat_child_argv`), không còn `argparse.REMAINDER`.
      2. `apply_profile_offline` chạy TRƯỚC dispatch — script con thừa hưởng đúng TL_PROFILE/scope. Trước
         đây `rasoat` nằm trong `_CREDS_LAZY_CMDS` nên `load_creds` KHÔNG chạy, và REMAINDER lại nuốt mất
         `--profile`: script con ghi registry theo scope NỀN dù người gõ đã chỉ định hồ sơ (RAS-14).
      3. Đường GHI đòi `--apply` TƯỜNG MINH. Thiếu `--apply` ⇒ bơm `dry_flag` của script con; script GHI
         mà KHÔNG có chế độ DRY ⇒ TỪ CHỐI (fail-CLOSED) chứ không chạy liều — "chạy trần" phải chỉ-đọc."""
    spec = _tl_registry.RASOAT_SPEC_BY_NAME.get(getattr(a, "sub", None) or "")
    if not spec:
        print(f"[tl] rasoat <sub> ∈ {list(_tl_registry.RASOAT_SPEC_BY_NAME)}", file=sys.stderr)
        return 1
    script = spec["script"]
    # (2) scope TRƯỚC dispatch — offline (rasoat là lệnh creds-lazy, không được đòi token ở đây).
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    apply_on = bool(getattr(a, "apply", False))
    # (3) cổng ghi fail-CLOSED: writer không có đường DRY thì KHÔNG có "chạy trần an toàn".
    if spec.get("writes") and not apply_on and not spec.get("dry_flag"):
        print(json.dumps({"ok": False, "error": "RASOAT_WRITE_NEEDS_APPLY", "sub": a.sub, "script": script,
                          "write_scope": spec["writes"],
                          "fix": f"`tl rasoat {a.sub} … --apply` để GHI; script con này KHÔNG có chế độ DRY "
                                 "nên chạy trần bị từ chối thay vì ghi im lặng."},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    rest = _tl_registry.rasoat_child_argv(spec, a, apply_on=apply_on)
    if a.sub == "worksheet" and not getattr(a, "no_auto_cache", False):
        _rasoat_autocache_worksheet(rest, a)        # #3: tự dựng cache nếu thiếu (auto-chain ingest)
    name = script[:-3] if script.endswith(".py") else script
    healed = _healed_script_path(name)          # gốc lành → bản gốc; cắt cụt/NUL → ghép từ _parts ra file tạm
    if healed:
        return subprocess.call([sys.executable, healed] + rest)
    fb = HERE / "_fallback" / script
    if fb.exists():
        return subprocess.call([sys.executable, str(fb)] + rest)
    plan = _rasoat_fallback_plan(a.sub, script, rest)
    # `--json` nay do tl NUỐT (vòng inject cuối build_parser) chứ không còn nằm trong `rest` — đọc namespace.
    if getattr(a, "json", False) or "--json" in rest:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(f"[tl] optional script chưa có: {script}. Đây là overlay core, không phải gói rasoat đầy đủ.", file=sys.stderr)
        print("[tl] Kênh đi vòng an toàn:", file=sys.stderr)
        for step in plan["safe_route"]:
            print("  - " + step, file=sys.stderr)
    return 2


def _is_high_amendment_subject(text: str) -> bool:
    t = re.sub(r"[_\-./]+", " ", _strip_accents(text or "").lower())   # chuẩn hoá _-./ → space (tên file dùng '_')
    return any(k in t for k in _HIGH_AMENDMENT_SUBJECTS)


def _qt5_queries(subject: str = "", goc: str = "", year: str = "") -> list[str]:
    """Sinh truy vấn QT-5 2-LƯỢT (S9, log 2026-07-01): LƯỢT 1 'hợp nhất' (phát hiện nhanh) + LƯỢT 2 BẮT BUỘC 'mới nhất' +
    NĂM HIỆN TẠI + Công báo (chống chốt VBHN LỖI THỜI — số VBHN tăng dần mỗi lần hợp nhất mới: 01→11→135, KHÔNG semver).

    Bài học thực tế: query đơn giản `luật <chủ đề> hợp nhất` nhiều khi tìm ra ngay, nhưng bản Google rank cao THƯỜNG là
    đời CŨ (nhiều backlink) → PHẢI chạy tiếp lượt-2 'mới nhất <năm>' + congbao.chinhphu.vn trước khi chốt canonical.
    """
    import datetime as _dt
    cur_year = _dt.date.today().year
    subject = (subject or "").strip()
    goc = (goc or "").strip()
    year = str(year or "").strip()
    high_velocity = _is_high_amendment_subject(subject) or _is_high_amendment_subject(goc)
    # Q1 (v1.33.35 — log rà 45 Luật: QT5_SUBJECT_NO_DIACRITICS — subject suy từ tên file ASCII 'Bo luat hinh
    # su' bị TRỘN với keyword CÓ DẤU 'hợp nhất' → query LAI, recall/exact-phrase kém). Chọn từ vựng keyword THEO
    # dấu của subject → query NHẤT QUÁN (subject không dấu → keyword cũng không dấu; Google chuẩn hoá dấu tiếng
    # Việt nên query đồng-nhất-không-dấu recall tốt hơn query lai). Không subject → mặc định CÓ DẤU (goc là số
    # hiệu, không có text để lệch). Advisory backfill title_vn vẫn giữ (bản có dấu + site:vbpl vẫn tối ưu nhất).
    _hd = _has_diacritics(subject) if subject else True
    _k_hn = "hợp nhất" if _hd else "hop nhat"
    _k_mn = "mới nhất" if _hd else "moi nhat"
    _k_vbhn = "văn bản hợp nhất" if _hd else "van ban hop nhat"
    _k_luat = "luật" if _hd else "luat"
    parts: list[str] = []
    if subject:
        plain = _strip_accents(subject).lower()
        law_subject = subject if ("luat" in plain or "luật" in subject.lower()) else f"{_k_luat} {subject}"
        # LƯỢT 1 — 'hợp nhất' (recall nhanh).
        parts.append(f"{subject} {_k_hn}")
        parts.append(f"{law_subject} {_k_hn}")
        parts.append(f'"{law_subject}" "{_k_hn}"')
        # S9 LƯỢT 2 BẮT BUỘC — 'mới nhất' + NĂM HIỆN TẠI + Công báo (official-first, ép tìm bản mới nhất).
        parts.append(f"{law_subject} {_k_hn} {_k_mn} {cur_year}")
        parts.append(f'"{subject}" "{_k_hn}" {cur_year}')
        parts.append(f'"{law_subject}" "{_k_vbhn}" {_k_mn}')
        parts.append(f'site:congbao.chinhphu.vn "{subject}" "{_k_hn}"')
        parts.append(f'site:congbao.chinhphu.vn "{subject}" {cur_year}')
        # S11 — tìm VBHN số LỚN HƠN / ngày SAU cùng cơ quan (VPQH) cho CÙNG luật (VBHN không tăng dần semver).
        parts.append(f'"{subject}" VBHN VPQH {cur_year}')
        # nguồn phụ phát hiện nhanh.
        parts.append(f'"{subject}" "{_k_vbhn}"')
        parts.append(f'site:thuvienphapluat.vn "{law_subject}" "{_k_hn}"')
        parts.append(f'site:luatvietnam.vn "{law_subject}" "{_k_hn}"')
    if goc:
        parts.append(f'"{subject}" "{goc}" "{_k_hn}"' if subject else f'"{goc}" "{_k_hn}"')
    if year and subject:
        parts.append(f'"{subject}" "VBHN" "{year}"')
    # Dedup giữ thứ tự. Nhóm high-velocity: đẩy các query 'mới nhất'/congbao LÊN ĐẦU (ưu tiên chạy trước).
    seen, out = set(), []
    for q in parts:
        q = q.strip()
        if q and q not in seen:
            seen.add(q); out.append(q)
    if high_velocity:
        # Q1: so bản STRIP-ACCENTS để bắt cả 'mới nhất' lẫn 'moi nhat' (query không dấu cho subject ASCII).
        out.sort(key=lambda q: 0 if ("moi nhat" in _strip_accents(q).lower() or "congbao" in q or str(cur_year) in q) else 1)
    return out


def cmd_vbhn_check(a) -> int:
    """QT-5: dò VBHN theo trích yếu + văn bản gốc + năm, không overclaim khi manifest miss."""
    if getattr(a, "refresh", False) or not (_cache_file("manifest.json")).exists():
        load_creds(getattr(a, "config", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] vbhn-check: không đọc được manifest: {e}", file=sys.stderr)
        return 1
    subject = getattr(a, "subject", "") or ""
    goc = getattr(a, "goc", "") or ""
    year = getattr(a, "year", "") or ""
    # vbhn positional-compat (tương thích runbook cũ): `tl vbhn-check "<trích yếu|số hiệu>"` → định tuyến goc/subject.
    target = getattr(a, "target", "") or ""
    # r179 T6 (log vận hành: tay quen `--sohieu` bị usage-error): --sohieu = ALIAS MỎNG của positional —
    # đi cùng đường định tuyến (số hiệu → goc; lỡ truyền trích yếu → subject, không gãy). Positional thắng nếu cả hai.
    if not target:
        target = getattr(a, "sohieu", "") or ""
    if target and not (subject or goc or year):
        if _looks_like_sohieu_query(target):
            goc = target
        else:
            subject = target
    derived_subject = ""
    if (not subject) and goc:
        gkey = norm_sohieu(goc)
        seeds = [e for e in entries if _sohieu_key_entry(e) == gkey]
        derived_subject = _derive_subject_from_entries(seeds)
        if derived_subject:
            subject = derived_subject
    scan = _vbhn_scan(entries)
    if getattr(a, "scan", False) and not (subject or goc or year):
        scan_flags = []
        if scan["collisions"]:
            scan_flags.append("VBHN_NUMBER_COLLISION")
        if scan["missing_subject"]:
            scan_flags.append("VBHN_MISSING_SUBJECT")
        out = {"ok": True, "mode": "scan", "vbhn_count": scan["vbhn_count"],
               "verdict": "REVIEW" if scan_flags else "OK", "flags": scan_flags,
               "collisions": [{"key": c["key"], "years": c["years"], "entries": [_summ_entry(e) for e in c["entries"]]} for c in scan["collisions"]],
               "missing_subject": [_summ_entry(e) for e in scan["missing_subject"][:50]]}
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
        return 0
    cands = _vbhn_candidates(entries, subject, goc, year)
    gkeys = {norm_sohieu(goc)} if goc else set()
    _flagged = [(e, _vbhn_quality_flags(e, subject, gkeys, year)) for e in cands]
    # §1.3 (log rà 108 lần): khi NGƯỜI DÙNG truyền --goc, ứng viên KHÔNG dẫn-chiếu goc (GOC_NOT_EVIDENT_IN_METADATA)
    # chỉ lọt nhờ trùng CHỦ ĐỀ lẻ (vd --goc 74/2025 "Việc làm" kéo Thanh niên/BLLĐ) → TÁCH sang uncertain_candidates để
    # KHÔNG nhầm là "đã lọc theo goc". Không truyền --goc → không có gì đối chiếu, giữ nguyên một danh sách.
    if gkeys:
        main_pairs = [(e, f) for e, f in _flagged if "GOC_NOT_EVIDENT_IN_METADATA" not in f]
        uncertain_pairs = [(e, f) for e, f in _flagged if "GOC_NOT_EVIDENT_IN_METADATA" in f]
    else:
        main_pairs, uncertain_pairs = _flagged, []
    main_cands = [e for e, _ in main_pairs]
    items = [{"entry": _summ_entry(e), "years": sorted(_entry_years(e)), "quality_flags": f} for e, f in main_pairs[:20]]
    uncertain_items = [{"entry": _summ_entry(e), "years": sorted(_entry_years(e)), "quality_flags": f} for e, f in uncertain_pairs[:20]]
    warnings = []
    # (port Codex) guard metadata yếu: mọi hit đều không lộ chủ đề trong metadata → KHÔNG dùng bare-number làm canonical.
    if subject and items and all("SUBJECT_NOT_EVIDENT_IN_METADATA" in it.get("quality_flags", []) for it in items):
        warnings.append("SUBJECT_FILTER_WEAK: mọi hit đều KHÔNG thể hiện rõ chủ đề trong metadata; không dùng "
                        "bare-number/metadata yếu làm canonical khi chưa verify nội dung.")
    if uncertain_items:
        warnings.append(f"GOC_NOT_EVIDENT_FILTERED: {len(uncertain_items)} ứng viên chỉ trùng CHỦ ĐỀ, KHÔNG dẫn-chiếu "
                        "goc đã cho — tách sang uncertain_candidates (verify trước khi tin; đừng coi là kết quả lọc theo goc).")
    if not cands:
        warnings.append("NO_CORPUS_MATCH_DO_NOT_CONCLUDE_ABSENT: không có hit trong manifest không có nghĩa là không có VBHN; chạy QT-5 ngoài corpus theo trích yếu + 'hợp nhất'.")
        warnings.append("QT5_WEB_REQUIRED: dùng qt5_queries bên dưới, ưu tiên nguồn chính thức/đáng tin.")
    elif not main_cands:
        warnings.append("GOC_FILTER_NO_DIRECT_HIT: không có ứng viên VBHN nào DẪN-CHIẾU goc đã cho; xem "
                        "uncertain_candidates (chỉ trùng chủ đề) và chạy QT-5 trước khi kết luận.")
        warnings.append("QT5_WEB_REQUIRED: dùng qt5_queries bên dưới, ưu tiên nguồn chính thức/đáng tin.")
    else:
        # A7 (giảm nhiễu) + P2-6 (log rà 71 luật): CHỈ ép CONTENT_VERIFY khi có RỦI RO THẬT cho ỨNG VIÊN NÀY.
        # GỐC RỄ nhiễu cũ: dùng `bool(scan["collisions"])` = collision TOÀN CORPUS → vì corpus có ~42 số VBHN tái
        # dùng ở đâu đó, cờ này LUÔN True ⇒ CONTENT_VERIFY_REQUIRED bật MÁY MÓC cho MỌI truy vấn (86 lần/log).
        # SỬA: chỉ tính collision CỦA CHÍNH số hiệu ứng viên đầu (`_self_collision`). Thêm: ứng viên ĐÃ verified
        # (`tl confirm`) + có NĂM + DUY NHẤT + không tự-collision → TIN (VBHN_METADATA_OK), khỏi ép verify lại.
        _top_entry = main_cands[0]
        _top_flags = set(items[0]["quality_flags"]) if items else set()
        _top_key = norm_sohieu(_entry_sohieu(_top_entry) or _parse_sohieu_from_name(_entry_name(_top_entry)))
        _self_collision = any(c["key"] == _top_key for c in scan["collisions"]) if _top_key else False
        _reuse_risk = (len(main_cands) > 1) or _self_collision or bool(_top_flags & {
            "VBHN_BARE_NUMBER", "VBHN_MISSING_YEAR_OR_DATE", "VBHN_NAME_MISSING_YEAR",
            "VBHN_NUMBER_REUSE_RISK", "VBHN_MINISTRY_MISSING_YEAR", "VBHN_MINISTRY_NAME_MISSING_YEAR"})
        _trusted = bool(_entry_confirmed(_top_entry)) and bool(_entry_years(_top_entry)) and len(main_cands) == 1 and not _self_collision
        if _reuse_risk and not _trusted:
            warnings.append("CONTENT_VERIFY_REQUIRED: phải chạy `tl vbhn-verify` hoặc verify tiêu đề + dòng hợp nhất trước khi tin (số VBHN có thể tái dùng theo năm / metadata chưa đủ).")
        else:
            warnings.append("VBHN_METADATA_OK: ứng viên duy nhất, năm + tiêu đề rõ — có thể tin (vẫn nên `tl vbhn-verify` nếu chốt canonical official-first).")
    # S9 (log 2026-07-01): cờ máy-đọc BẮT BUỘC xác minh BẢN MỚI NHẤT — chống chốt VBHN LỖI THỜI (ca BLHS 01/VBHN 2017 thay
    # vì 135/VBHN 2025). Google rank trang CŨ lên đầu; số VBHN TĂNG DẦN mỗi lần hợp nhất (01→11→135), KHÔNG semver.
    # S-8b (v1.33.16 — MERGE nhánh-4, đối xứng với S-8 source-map v1.33.15): luật RẤT MỚI (năm ≥ nay−2) CHƯA có
    # ứng viên VBHN nào trong corpus + KHÔNG thuộc nhóm dồn dập → hạ cờ latest thành INFO (QT5_WEB_REQUIRED giữ
    # nguyên — vẫn phải tìm web khi cần chốt, chỉ không phồng hàng lượt-2). Năm ĐỘNG thay hardcode 2024 nhánh-4.
    _latest_low = _vbhn_latest_low_priority_recent_law(subject, goc, year, bool(main_cands))
    if main_cands or (not _latest_low and any(w.startswith("QT5_WEB_REQUIRED")
                                              or w.startswith("GOC_FILTER_NO_DIRECT_HIT") for w in warnings)):
        warnings.append("VBHN_CANDIDATE_UNVERIFIED_LATEST: CHƯA xác minh đây là VBHN MỚI NHẤT — BẮT BUỘC chạy tiếp query "
                        "LƯỢT-2 (qt5_queries: 'mới nhất <năm>' + site:congbao.chinhphu.vn) + tìm số VBHN LỚN HƠN/ngày SAU "
                        "cùng VPQH trước khi chốt. Số VBHN tăng dần mỗi lần hợp nhất (01→11→135), KHÔNG semver.")
    elif _latest_low:
        warnings.append("VBHN_LATEST_LOW_PRIORITY_RECENT_LAW: luật ban hành rất mới, chưa có ứng viên VBHN trong "
                        "corpus và không thuộc nhóm high-velocity — vẫn chạy QT-5 khi cần chốt, nhưng KHÔNG đẩy "
                        "vào hàng latest lượt-2.")
    if _is_high_amendment_subject(subject) or _is_high_amendment_subject(goc):
        warnings.append("VBHN_HIGH_AMENDMENT_VELOCITY: luật thuộc nhóm SỬA ĐỔI DỒN DẬP (cải cách 2024-2026) — Google dễ trả "
                        "bản LỖI THỜI; BẮT BUỘC kiểm Công báo (congbao.chinhphu.vn) theo năm hiện tại, KHÔNG tin rank cao nhất.")
    # P0-1 (v1.31.0): subject KHÔNG DẤU (suy từ tên file ASCII) → recall site:vbpl/congbao kém — ADVISORY, không đổi
    # verdict; đường sửa gốc: `tl backfill-title-vn --apply` (điền trích yếu có dấu) hoặc truyền --subject tay.
    if subject and not _has_diacritics(subject):
        warnings.append("QT5_SUBJECT_NO_DIACRITICS: chủ đề suy ra KHÔNG có dấu (từ tên file) — query web recall kém; "
                        "truyền --subject \"<chủ đề có dấu>\" hoặc chạy `tl backfill-title-vn --apply` một lần.")
    _top_flags = list(dict.fromkeys(
        _warning_codes(warnings)
        + [f for it in items for f in (it.get("quality_flags") or [])]
        + [f for it in uncertain_items for f in (it.get("quality_flags") or [])]
    ))
    out = {"ok": True, "subject": subject or None, "derived_subject": derived_subject or None, "goc": goc or None, "year": year or None,
           "candidates": items, "results": items,
           "uncertain_candidates": uncertain_items, "weak_candidates": uncertain_items,   # weak_candidates = alias (tương thích Codex hotfix)
           "verdict": _vbhn_check_verdict(_top_flags, bool(main_cands)),
           "flags": _top_flags,
           "warnings": warnings, "qt5_queries": _qt5_queries(subject, goc, year),
           "google_discovery": _discovery_links(subject or derived_subject or goc or "")["links_markdown"],
           "vbhn_number_collisions": [{"key": c["key"], "years": c["years"], "entries": [_summ_entry(e) for e in c["entries"][:5]]} for c in scan["collisions"][:20]]}
    if a.json:
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== tl vbhn-check — subject={subject or '∅'} goc={goc or '∅'} year={year or '∅'} ==")
        for w in warnings:
            print(f"⚠ {w}")
        if items:
            for it in items:
                e = it["entry"]
                print(f"- {e['name'][:90]} | sohieu={e['sohieu'] or '∅'} | cat={e['cat']} | years={','.join(it['years']) or '∅'} | flags={','.join(it['quality_flags']) or 'OK'}")
        else:
            print("Không có ứng viên DẪN-CHIẾU goc trong manifest.")
        if uncertain_items:
            print(f"\n— uncertain ({len(uncertain_items)}): chỉ trùng chủ đề, KHÔNG dẫn-chiếu goc (verify trước khi tin):")
            for it in uncertain_items:
                e = it["entry"]
                print(f"  ? {e['name'][:88]} | sohieu={e['sohieu'] or '∅'} | flags={','.join(it['quality_flags']) or 'OK'}")
        if out.get("google_discovery"):
            print("\nTÌM WEB (GOOGLE site:, VBHN-first — ưu tiên cách này hơn search nội bộ):")
            for ln in out["google_discovery"]:
                print(f"  {ln}")
        print("\n(QT-5 query thô — nếu cần): " + " | ".join(out["qt5_queries"][:3]))
    # A3: "không có hit trong manifest" là PHÁT HIỆN (QT5_WEB_REQUIRED), KHÔNG phải lệnh lỗi → rc=0 (không phá &&/CI).
    return 0


def _vbhn_verify_flags(text: str, expect_title: str = "", expect_gocs: list[str] | None = None,
                       expect_year: str = "", head_chars: int = 5000) -> list[str]:
    text_nfc = unicodedata.normalize("NFC", text or "")
    head = text_nfc[: max(1000, int(head_chars or 5000))]
    full_norm = _strip_accents(text_nfc).lower()
    head_norm = _strip_accents(head).lower()
    flags = []
    if expect_title:
        q = _strip_accents(expect_title).lower()
        toks = _subject_tokens(expect_title)
        if q not in full_norm and not (toks and len(toks & _token_set(full_norm)) >= max(2, min(4, len(toks)))):
            flags.append("EXPECT_TITLE_NOT_FOUND")
    for g in expect_gocs or []:
        if norm_sohieu(g) not in _ref_tokens(text_nfc):
            if _strip_accents(g).lower().replace("/", "-") not in full_norm.replace("/", "-"):
                flags.append(f"EXPECT_GOC_NOT_FOUND:{g}")
    if expect_year and expect_year not in head and expect_year not in text_nfc[:20000]:
        flags.append("EXPECT_YEAR_NOT_FOUND")
    # VBHN chính thức (VPQH/bộ ngành) THƯỜNG không in cụm 'văn bản hợp nhất' ở header;
    # tín hiệu hợp-nhất là SỐ HIỆU 'Số: NN/VBHN-...'. Nhận cả hai để không gán nhầm bản tự ghép.
    vbhn_header = ("van ban hop nhat" in head_norm or "văn bản hợp nhất" in head.lower()
                   or re.search(r"so\s*:?\s*\d+\s*/\s*vbhn\b", head_norm) is not None)
    if not vbhn_header:
        flags.append("HEADER_NOT_CLEAR_VBHN")
    return flags


def _focus_block(text: str, focus: str) -> str:
    focus = (focus or "").strip()
    # r296 (P16-F15, cùng họ): `(\d+)\b` không nhận nổi focus "Điều 7a" ⇒ rơi thẳng xuống nhánh tìm-chuỗi
    # và trả về một CỬA SỔ ±1500/5000 ký tự thay vì đúng khối Điều — so sánh official↔candidate (:1449)
    # do đó đối chiếu nhầm vùng. Tách hậu tố chữ ra group RIÊNG: không hậu tố thì giữ nguyên đường
    # `extract_dieu` (khoá int, không đổi hợp đồng); CÓ hậu tố thì đi `_slice_dieu` — hàm nhận str và
    # sau r296 đã dừng đúng chỗ. (`_slice_dieu` là symbol của `nlm_ops`, resolve qua namespace tl sau
    # bind — cùng khuôn với mọi tham chiếu chéo module khác trong tệp này.)
    m = re.search(r"(?iu)\bĐiều\s+(\d+)([a-zđ]*)\b", focus)
    if m:
        if m.group(2):
            blk = _slice_dieu(text or "", m.group(1) + m.group(2))
            return "" if blk.startswith("[không thấy Điều") else blk
        return extract_dieu(text or "", int(m.group(1))) or ""
    pos = _strip_accents(text or "").lower().find(_strip_accents(focus).lower())
    if pos < 0:
        return ""
    return (text or "")[max(0, pos - 1500): pos + 5000]


def _vbhn_compare(official: str, candidate: str, focuses: list[str] | None = None) -> dict:
    off_n, cand_n = _norm_compare_text(official), _norm_compare_text(candidate)
    off_foot = sorted(set(re.findall(r"\[\d+\]", official or "")))
    cand_foot = sorted(set(re.findall(r"\[\d+\]", candidate or "")))
    flags = []
    if off_n != cand_n:
        flags.append("CONTENT_DIFF_PRESENT")
    if len(cand_foot) < len(off_foot):
        flags.append("CANDIDATE_MISSING_FOOTNOTES")
    focus_reports = []
    for f in focuses or []:
        ob, cb = _focus_block(official, f), _focus_block(candidate, f)
        orefs, crefs = _legal_refs(ob), _legal_refs(cb)
        fd = {
            "focus": f,
            "official_found": bool(ob),
            "candidate_found": bool(cb),
            "same_after_whitespace_norm": _norm_compare_text(ob) == _norm_compare_text(cb),
            "official_refs": orefs,
            "candidate_refs": crefs,
            "candidate_only_refs": [x for x in crefs if x not in orefs],
            "official_only_refs": [x for x in orefs if x not in crefs],
        }
        if not fd["same_after_whitespace_norm"]:
            flags.append(f"FOCUS_DIFF:{f}")
        if fd["candidate_only_refs"] or fd["official_only_refs"]:
            flags.append(f"FOCUS_REF_DIFF:{f}")
        focus_reports.append(fd)
    return {
        "ok": not flags,
        "flags": list(dict.fromkeys(flags)),
        "official_chars": len(official or ""),
        "candidate_chars": len(candidate or ""),
        "official_footnotes": off_foot,
        "candidate_footnotes": cand_foot,
        "focus": focus_reports,
        "note": "Nếu khác bản chính thức, lấy bản chính thức làm canonical; bản tự ghép chỉ để tham chiếu/quarantine.",
    }


def cmd_vbhn_verify(a) -> int:
    """Verify nội dung VBHN: tiêu đề/trích yếu/năm/gốc có khớp kỳ vọng không."""
    try:
        text, source = _read_verify_text(a)
    except Exception as e:
        print(f"[tl] vbhn-verify lỗi: {e}", file=sys.stderr)
        return 1
    flags = _vbhn_verify_flags(text, a.expect_title or "", a.expect_goc or [], a.expect_year or "", getattr(a, "head", 5000) or 5000)
    flags.extend(_vbhn_official_flags(text, getattr(a, "source_name", "") or source,
                                      getattr(a, "official_required", False),
                                      getattr(a, "allow_provisional", False)))
    flags = list(dict.fromkeys(flags))
    head = unicodedata.normalize("NFC", text or "")[: max(1000, int(getattr(a, "head", 5000) or 5000))]
    verdict, official, provisional = _vbhn_verdict(flags, getattr(a, "allow_provisional", False))
    out = {"ok": not flags, "verdict": verdict, "official": official, "provisional": provisional,
           "source": source, "chars": len(text or ""), "flags": flags,
           "head_sample": (head[:800] or None),
           "note": "OK nghĩa là qua gate sơ bộ. Với VBHN làm nguồn rà soát, vẫn ưu tiên bản chính thức người dùng nạp/nguồn VPQH; không tự ghép làm canonical."}
    print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    return 0 if out["ok"] else 2


def cmd_vbhn_compare(a) -> int:
    """So bản chính thức với bản ứng viên/tự ghép để phát hiện sai khác quy phạm."""
    try:
        official = Path(a.official_text).read_text(encoding="utf-8", errors="replace")
        candidate = Path(a.candidate_text).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"[tl] vbhn-compare lỗi đọc file: {e}", file=sys.stderr)
        return 1
    out = _vbhn_compare(official, candidate, getattr(a, "focus", None) or [])
    if a.json:
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== tl vbhn-compare — official={a.official_text} candidate={a.candidate_text} ==")
        for f in out["flags"]:
            print(f"⚠ {f}")
        print(f"official_chars={out['official_chars']} candidate_chars={out['candidate_chars']}")
        print(f"official_footnotes={len(out['official_footnotes'])} candidate_footnotes={len(out['candidate_footnotes'])}")
        for fr in out["focus"]:
            print(f"- {fr['focus']}: same={fr['same_after_whitespace_norm']} candidate_only_refs={fr['candidate_only_refs']} official_only_refs={fr['official_only_refs']}")
    return 0 if out["ok"] else 2


def _parse_footnote_def(n: str, body: str) -> dict:
    """B1: '[n] <target> được sửa/bổ sung theo <nguồn> của Luật … số <sh> [, có hiệu lực …]' → bản ghi độc lập.
    target = điều BỊ SỬA (dieu/khoan/diem); amending_sohieu lấy TRONG def (không 'luật gần nhất'); amending_vitri = vị trí NGUỒN."""
    low = body.lower()
    loai = ("bãi bỏ" if ("bãi bỏ" in low or "hủy bỏ" in low or re.search(r"\bđược\s+bỏ\b", low))
            else "thay thế" if "thay thế" in low
            else "bổ sung" if ("bổ sung" in low and "sửa đổi" not in low)
            else "sửa đổi" if "sửa đổi" in low else "")
    vm = _AMEND_VERB_RE.search(body)
    if vm:
        target_clause, rest = body[: vm.start()], body[vm.end():]
        tm = _POS_RE.search(target_clause)   # target CHỈ lấy trước động-từ-sửa (tránh vớ vị trí NGUỒN); thiếu → anchor thân điền
    else:
        target_clause = rest = body
        tm = _POS_RE.search(body)
    diem = _multi_diem(target_clause, tm.group(1) if tm else None)   # bắt CẢ DÃY điểm đích ("c và d"), không chỉ 1
    khoan = tm.group(2) if tm else None
    dieu = tm.group(3) if tm else None
    lm = _AMEND_LAW_RE.search(body)
    if lm:
        sh = norm_sohieu(lm.group(1))
    else:
        sm = _SOHIEU_RE.search(rest) or _SOHIEU_RE.search(body)
        sh = norm_sohieu(sm.group(1)) if sm else None
    cut = re.search(r"của\s+(?:Bộ\s+luật|Luật)\b", rest, re.IGNORECASE)
    sm2 = _POS_RE.search(rest[: cut.start()] if cut else rest)
    vitri = " ".join(p for p in [
        ("điểm " + sm2.group(1)) if sm2 and sm2.group(1) else None,
        ("khoản " + sm2.group(2)) if sm2 and sm2.group(2) else None,
        ("Điều " + sm2.group(3)) if sm2 and sm2.group(3) else None] if p) or None
    dm = _HL_DATE_RE.search(body) or _HL_DATE_VN_RE.search(body)   # số HOẶC "ngày D tháng M năm Y"
    hl = _date_from_effect_match(dm)
    # amendment THẬT: động-từ-sửa ở MỆNH ĐỀ CHÍNH — KHÔNG nằm sau "như sau:" (đoạn trích dẫn) và KHÔNG phải
    # "căn cứ ban hành" → loại [1] (căn cứ), [6] (trích Điều hiệu-lực-thi-hành của luật sửa).
    _ns = low.find("như sau")
    is_amend = bool(vm) and ("căn cứ ban hành" not in low) and not (0 <= _ns < vm.start())
    return {"marker": n, "dieu": dieu, "khoan": khoan, "diem": diem, "is_amend": is_amend,
            "amending_sohieu": sh, "amending_vitri": vitri, "hieu_luc": hl, "loai": loai, "footnote": body[:200]}


def _footnote_rel_kind(rec: dict) -> str:
    """Gắn nhãn HẠ-ƯU-TIÊN cho 1 bản ghi footnote-amend: 'CROSS_CUTTING' (omnibus sửa-nhiều-luật) |
    'PARTIAL_REPEAL' (bãi bỏ cục bộ 1 khoản/điểm) | '' (sửa chuyên đề thường). Chỉ đọc nguyên văn chú thích — KHÔNG
    cần corpus/base subject. CROSS_CUTTING thắng khi cả hai cùng khớp (omnibus là cờ đỏ lớn hơn)."""
    foot = _strip_accents(rec.get("footnote") or "")
    if _FOOTNOTE_CROSSCUT_RE.search(foot):
        return "CROSS_CUTTING"
    if rec.get("loai") == "bãi bỏ" and (rec.get("khoan") or rec.get("diem")):
        return "PARTIAL_REPEAL"
    return ""


def cmd_xref(a) -> int:
    """WS2: bóc dẫn chiếu trong 1 văn bản, giải về canonical (bộ danh tính WS1), gắn cờ
    MISSING/OUTDATED/SOHIEU_MISMATCH/OMNIBUS_LINK. REPORT-ONLY (không tự sửa văn bản)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    text = ""
    if getattr(a, "text_file", None):
        text = Path(a.text_file).read_text(encoding="utf-8", errors="replace")
    elif getattr(a, "target", None):
        # target = gdocId hoặc số hiệu → resolve canonical → exporttext (1 call webapp)
        gid = a.target
        _src_name = a.target
        try:
            entries = _manifest_entries(refresh=getattr(a, "refresh", False))
            # (HỢP NHẤT Codex) deep-resolve: ưu tiên GDoc/corpus/live, LUÔN thử by-name (tên DÀI không bị nhận
            # nhầm DriveId) → chốt bug C; KHÔNG còn chọn sidecar raw thắng GDoc (P0-1).
            _de, _dgid, _dname, _dhits = _resolve_deep_target(a.target, entries)
            if _de is not None:
                gid = _dgid or gid
                _src_name = _dname or _src_name
        except Exception:
            entries = []
        # P1: entry THÔ (tên có đuôi .docx/.pdf/.html) → KHÔNG export được → bỏ qua sạch, KHÔNG gọi webapp vô ích.
        if _is_raw_no_gdoc_name(_src_name):
            return _emit_raw_no_gdoc(_src_name, getattr(a, "json", False))
        # D (log rà: timeout văn bản lớn): TÁI DÙNG cache extract_<gid>.txt nếu có → KHÔNG export lại (Bộ luật
        # Dân sự xref+footnote-map+extract trước đây export 3 lần → timeout). Miss cache thì export như cũ.
        text = ""
        try:
            _cf = _cache_file(f"extract_{gid}.txt")
            if _cf.exists():
                _ct = _cf.read_text(encoding="utf-8", errors="replace")
                if _ct.strip():
                    # r267 (P15 — đo 30-07): CÙNG tệp cache `extract_<id>.txt` có tới BỐN reader; r266 mới
                    # đồng bộ hai (`_read_doc_text` + `_doc_text_any`). Thiếu U1 ở đây KHÔNG chỉ lệch byte —
                    # `\x0c` pdftotext nằm GIỮA một số hiệu làm regex nuốt qua ranh giới: đo được MẤT HẲN
                    # `59/2020/QH14` và gán NHẦM `01/2021/NĐ-CP` thành loai='Luật'. Đường này nuôi
                    # `missing_in_corpus`/`gaps_missing_in_corpus` ⇒ danh sách văn bản cần tải THIẾU âm thầm.
                    text = _sanitize_export_text(_strip_font_runs(_ct))
        except Exception:
            text = ""
        if not text:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
            # A1 (v1.33.10): GWS-FIRST thay vì gọi thẳng exporttext (chết cả lệnh khi webapp thiếu scope
            # script.external_request dù direct-media đang sống — ca xref BLDS/143 trong log).
            _t10 = _read_doc_text(gid, getattr(a, "config", None))
            r = {"ok": bool((_t10 or "").strip()), "text": _t10}
            if r.get("ok") is False or not r.get("text"):
                # P1: lỗi 'Export only supports Docs Editors files' = entry chưa GDoc → ENTRY_RAW_NO_GDOC rc=2 (gọn, không rò API thô).
                if _raw_no_gdoc(_src_name, r):
                    return _emit_raw_no_gdoc(_src_name, getattr(a, "json", False))
                print(json.dumps({"ok": False, "error": "không đọc được text (mọi đường cache/direct-media/gws/exporttext)",
                                  "detail": "chạy `tl doctor --deep` để kiểm scope script.external_request hoặc gws cred (MERGE Codex v1.33.11)"},
                                 ensure_ascii=False), file=sys.stderr)
                return 2
            text = r.get("text", "")
    else:
        print("[tl] xref cần <gdocId|số hiệu> hoặc --text-file", file=sys.stderr); return 2
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] xref: không đọc được manifest offline ({e}); chạy `tl boot` trước.", file=sys.stderr); return 2
    # B3: bản đồ sửa đổi cấp Điều từ footnote → base_goc_keys (chuỗi hợp nhất của chính VBHN đang xét) cho B1.
    fnmap = resolve_footnote_amendments(text, entries=entries)
    # L3/B1: chuỗi hợp nhất ĐẦY ĐỦ của chính VBHN = mapped(footnote→Điều) ∪ số hiệu trong khối chú thích ∪ preamble.
    mapped = set(fnmap.get("mapped_sohieu", []))
    chain = mapped | set(fnmap.get("footnote_sohieu", [])) | set(fnmap.get("header_sohieu", []))
    base_goc_keys = {s.replace("/", "-") for s in chain}
    refs = extract_refs(text)
    classed = [_classify_ref(r, entries, base_goc_keys) for r in refs]
    # L3/B2: rel_type 3 loại — SUA_DOI_BASE (sửa vào base, có map cấp Điều) / CHU_THICH_LICH_SU (chỉ trong
    # chú thích/preamble = lớp sửa lịch sử đã hợp nhất) / DAN_CHIEU_NOI_DUNG (dẫn chiếu nội dung luật khác).
    for c in classed:
        shn = norm_sohieu(c["sohieu"])
        if shn in mapped:
            c["rel_type"] = "SUA_DOI_BASE"
        elif shn in base_goc_keys:
            c["rel_type"] = "CHU_THICH_LICH_SU"
        else:
            c["rel_type"] = "DAN_CHIEU_NOI_DUNG"
    # OMNIBUS_LINK: văn bản đang xref sửa đồng thời nhiều văn bản (sua_doi/goc nhiều đích) — báo từ ref OUTDATED/nhiều đích
    omni = [c for c in classed if c["flag"] in ("OUTDATED", "SOHIEU_MISMATCH", "DOC_TEXT_SOHIEU_TYPO")]
    pending = [r for r in fnmap["dieu_level_amendment_map"] if r.get("pending_effect")]
    summary = {f: sum(1 for c in classed if c["flag"] == f) for f in ("OK", "MISSING", "OUTDATED", "SOHIEU_MISMATCH", "DOC_TEXT_SOHIEU_TYPO")}
    rel_summary = {t: sum(1 for c in classed if c.get("rel_type") == t) for t in ("SUA_DOI_BASE", "CHU_THICH_LICH_SU", "DAN_CHIEU_NOI_DUNG")}
    out = {"ok": True, "refs_found": len(refs), "summary": summary, "rel_summary": rel_summary, "refs": classed,
           "consolidation_chain": sorted(chain),
           "dieu_level_amendment_map": fnmap["dieu_level_amendment_map"], "footnote_count": fnmap["footnote_count"],
           "pending_effect_count": len(pending),
           "note": "report-only; rel_type: SUA_DOI_BASE=sửa vào base, CHU_THICH_LICH_SU=lớp sửa lịch sử đã hợp nhất (đừng coi là OUTDATED), DAN_CHIEU_NOI_DUNG=dẫn chiếu luật khác."}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"== tl xref · {len(refs)} dẫn chiếu · " + " ".join(f"{k}={v}" for k, v in summary.items())
              + " · rel " + "/".join(f"{t.split('_')[0]}={n}" for t, n in rel_summary.items()) + " ==")
        for c in classed:
            tag = c["flag"]
            mark = {"OK": "·", "MISSING": "✗", "OUTDATED": "⟳", "SOHIEU_MISMATCH": "≠", "DOC_TEXT_SOHIEU_TYPO": "⚠"}.get(tag, "?")
            rt = {"SUA_DOI_BASE": "SỬA", "CHU_THICH_LICH_SU": "LSỬ", "DAN_CHIEU_NOI_DUNG": "DCHIẾU"}.get(c.get("rel_type"), "")
            line = f"  {mark} [{tag:15s}] {rt:6s} {c['sohieu']:18s} {c.get('name_phrase','')[:30]}"
            if c.get("canonical"):
                line += f" → {c['canonical']['sohieu']}"
            if c.get("note"):
                line += f"  ({c['note']})"
            print(line)
        if omni:
            print(f"  [OMNIBUS/quan hệ] {len(omni)} dẫn chiếu cần truy mạng lưới sửa đổi (omnibus/VBHN).")
        if out["dieu_level_amendment_map"]:
            print(f"\n  Bản đồ sửa đổi cấp Điều (footnote, {out['footnote_count']} chú thích · pending={out['pending_effect_count']}):")
            for r in out["dieu_level_amendment_map"]:
                pe = " ⏳PENDING_EFFECT" if r.get("pending_effect") else ""
                print(f"    [{r['marker']}] Điều {r['dieu']} K{r['khoan'] or '?'} ← {r['amending_sohieu'] or '?'} ({r.get('amending_vitri') or ''}) HL {r.get('hieu_luc') or '?'} [{r.get('loai') or '?'}]{pe}")
    # A3: dẫn chiếu MISSING/MISMATCH/TYPO là PHÁT HIỆN dữ liệu (rà OK), KHÔNG phải lệnh lỗi → rc=0 mặc định (không phá && /CI).
    # Chỉ rc=1 khi truyền --strict (cho CI muốn fail-on-findings).
    if getattr(a, "strict", False) and (summary["SOHIEU_MISMATCH"] or summary["MISSING"] or summary["DOC_TEXT_SOHIEU_TYPO"]):
        return 1
    return 0


def _rasoat_dedup_push(frontier: list, seen: set, candidates: list) -> int:
    """PURE (test offline): đẩy ứng viên MỚI (sohieu chưa ∈ seen) vào frontier theo ưu tiên. Trả SỐ ứng viên MỚI
    (0 → dry_rounds++ ; >0 → dry_rounds=0). seen chống LẶP VÔ HẠN. frontier xếp ưu tiên (amending>VBHN>dẫn-chiếu)."""
    added = 0
    for c in candidates or []:
        k = c.get("sohieu_norm") or norm_sohieu(c.get("sohieu") or "")
        if not k or k in seen:
            continue
        seen.add(k); frontier.append(dict(c)); added += 1
    frontier.sort(key=lambda x: (x.get("priority", 9), x.get("sohieu_norm", "")))
    return added


def _rasoat_expand_text(text: str, entries: list) -> list:
    """LÕI frontier-expand trên 1 text CÓ SẴN (không mạng): refs+footnote → ứng viên frontier dedup. Dùng SEED + mở rộng."""
    fnmap = resolve_footnote_amendments(text, entries=entries)
    mapped = {norm_sohieu(s) for s in fnmap.get("mapped_sohieu", [])}
    chain = mapped | {norm_sohieu(s) for s in fnmap.get("footnote_sohieu", [])} | {norm_sohieu(s) for s in fnmap.get("header_sohieu", [])}
    classed = [_classify_ref(r, entries, {s.replace("/", "-") for s in chain}) for r in extract_refs(text)]
    return _frontier_candidates(classed, mapped)


def cmd_rasoat_loop(a) -> int:
    """VÒNG LẶP RÀ SOÁT KHÉP KÍN (orchestrator v1, REPORT-ONLY): SEED từ base → frontier-expand → đệ quy mở rộng ứng viên
    IN-CORPUS (đọc NGUYÊN VĂN từ cache/gws, KHÔNG RAG) → dedup `seen` chống lặp vô hạn → DỪNG khi frontier rỗng VÀ
    dry_rounds≥K (mặc định 2) hoặc chạm --max-iter. Xuất: hội tụ?, GAP (ngoài corpus → tải/KH3), in-corpus-chưa-NLM
    (→ `tl ingest-missing --apply`). KHÔNG tự mutate; đánh giá sâu từng cặp → `tl overlap`."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    K = getattr(a, "dry_rounds", None) or 2
    max_iter = getattr(a, "max_iter", None) or 12
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception:
        entries = []
    base_text, base_gid, base_name = _frontier_doc_text(a)
    if not base_text:
        print("[tl] rasoat-loop: chưa đọc được base (cần <gdoc|sohieu>+gws, hoặc --text-file).", file=sys.stderr); return 2
    seen, frontier, evaluated, gaps = set(), [], [], []
    _rasoat_dedup_push(frontier, seen, _rasoat_expand_text(base_text, entries))
    dry_rounds, it = 0, 0
    # r256 (P15 — repro: 5 ứng viên ngoài corpus, K=2 ⇒ báo 2/5 GAP, frontier_remaining=3, max_iter=12 CHƯA
    # HỀ chạm): `dry_rounds` KHÔNG được nằm trong điều kiện vòng. Docstring nói "DỪNG khi frontier rỗng VÀ
    # dry_rounds≥K" (AND) nhưng code cài OR ⇒ chạm K là thoát dù frontier còn. Nặng nhất: ứng viên NGOÀI
    # corpus cũng dry_rounds++ (dòng dưới) mà GAP chính là SẢN PHẨM của lệnh ⇒ càng tìm ra nhiều gap càng
    # dừng sớm, mất dữ liệu phát hiện IM LẶNG. `max_iter` vẫn là trần cứng duy nhất; `dry_rounds` giữ
    # nguyên vai trò tín hiệu hội tụ ở `converged` (frontier cạn toàn-gap ⇒ dry_rounds≥K ⇒ HỘI TỤ, đúng).
    # r295/T1-c (RAS-04 + RAS-10 — audit lõi 31-07): MỘT định nghĩa hội tụ duy nhất.
    #   khong_doc_duoc = ứng viên IN-CORPUS có bản đọc được NHƯNG đọc HỎNG (ném lỗi / ra rỗng)
    #                    — đếm RIÊNG, KHÔNG bao giờ đụng `dry_rounds`, và CHẶN `converged`
    #   khong_co_ban_doc = ứng viên IN-CORPUS không giải được GDoc id — CHỈ BÁO, không chặn hội tụ
    # ★ Ranh giới giữa hai sổ trên là RANH GIỚI PHẢI GIỮ: gộp "không có bản đọc" vào "đọc hỏng" làm đỏ
    #   `r256_no_infinite_loop_seen_dedup_holds` (harness của nó cho `_resolve_deep_target` trả gid=None
    #   và khoá `rc=0`) — bắt được lúc chạy full suite. Registry có dòng hợp lệ không kèm Drive (vd mới
    #   nạp NLM), coi đó là "lệnh hỏng" là siết quá tay và NGOÀI phạm vi phát hiện RAS-04 (nói về
    #   `_read_doc_text`). Vẫn phải NÓI RA — doctrine "no silent caps".
    #   dry_rounds     = CHỈ tăng khi đã đọc THÀNH CÔNG mà không sinh ứng viên mới
    #   converged      = frontier cạn VÀ không có ca không-đọc-được VÀ (dry_rounds ≥ K HOẶC chưa từng có
    #                    ứng viên nào ngay từ đầu)
    # Vì sao: `converged:true` là lời khẳng định "đã soi hết, không còn gì mới". Bản cũ gộp lỗi đọc vào
    # `dry_rounds` nên HAI lần đọc hỏng liên tiếp là đủ chạm K ⇒ lệnh tuyên bố HỘI TỤ, rc=0, trong khi
    # thực tế chưa hề nhìn vào hai văn bản đó — mất phát hiện IM LẶNG, đúng lớp bệnh r256 đã trả giá.
    # RAS-10 là vế còn lại của cùng một định nghĩa: frontier rỗng NGAY TỪ ĐẦU (base không dẫn đi đâu) là
    # hội tụ THẬT, không phải "chưa đủ vòng-cạn" — bản cũ trả `converged:false` mãi mãi vì dry_rounds=0<K.
    _co_ung_vien_ban_dau = bool(frontier)
    khong_doc_duoc, khong_co_ban_doc = [], []
    while frontier and it < max_iter:
        it += 1
        c = frontier.pop(0)
        evaluated.append(c.get("sohieu_norm"))
        if not c.get("in_corpus"):
            gaps.append(c); dry_rounds += 1; continue
        _sh295 = c.get("sohieu") or c.get("sohieu_norm")
        added, _hong = 0, ""
        try:
            _e, _gid, _, _ = _resolve_deep_target(_sh295, entries)
            if not _gid:
                khong_co_ban_doc.append(_sh295)      # không chặn hội tụ (xem ghi chú trên), vẫn báo
                dry_rounds += 1
                continue
            _t = _read_doc_text(_gid, getattr(a, "config", None)) or ""
            if not _t:
                _hong = "DOC_RA_RONG"
            else:
                added = _rasoat_dedup_push(frontier, seen, _rasoat_expand_text(_t, entries))
        except Exception as _err295:  # noqa: BLE001
            _hong = type(_err295).__name__ + ": " + str(_err295)[:120]
        if _hong:
            khong_doc_duoc.append({"sohieu": _sh295, "ly_do": _hong})
        else:
            dry_rounds = 0 if added else dry_rounds + 1
    in_corpus_no_nlm = []
    for k in seen:
        for e in entries:
            if ((norm_sohieu(_entry_sohieu(e)) == k or _sohieu_key_entry(e) == k)
                    and str(e.get("corpus") or "").lower() == "true" and not _entry_on_nlm_live(e)):
                in_corpus_no_nlm.append(k); break
    gap_sh = sorted({c.get("sohieu") for c in gaps if c.get("sohieu")})
    # r252: NÓI RÕ vì sao dừng (doctrine "no silent caps") — trước đây nhánh not-converged in cứng
    # "chạm max-iter" nên ca dừng-vì-dry bị chẩn đoán SAI, người đọc đi tăng --max-iter mà vô ích.
    stop_reason = ("max_iter" if it >= max_iter and frontier
                   else ("frontier_empty_ngay_tu_dau" if not _co_ung_vien_ban_dau else "frontier_empty"))
    _converged = ((not frontier) and not khong_doc_duoc
                  and (dry_rounds >= K or not _co_ung_vien_ban_dau))
    out = {"ok": not khong_doc_duoc, "gate": "rasoat-loop", "base": base_name, "iterations": it, "seen": len(seen),
           "evaluated": len(evaluated), "frontier_remaining": len(frontier),
           "stop_reason": stop_reason, "dry_rounds": dry_rounds, "max_iter": max_iter, "dry_rounds_target": K,
           "converged": _converged,
           "khong_doc_duoc": khong_doc_duoc, "khong_co_ban_doc": sorted(set(khong_co_ban_doc)),
           "gaps_missing_in_corpus": gap_sh, "in_corpus_not_on_nlm": sorted(set(in_corpus_no_nlm)),
           "note": "REPORT-ONLY: bản thiếu TRONG corpus chưa NLM → `tl ingest-missing --apply`; bản NGOÀI corpus (gaps) "
                   "→ discovery/tải (KH3, qua G1/G2/G3); đánh giá sâu từng cặp → `tl overlap`."}
    if khong_doc_duoc:
        # rc≠0 CHỈ ở ca này: lệnh KHÔNG LÀM ĐƯỢC VIỆC (có ứng viên không soi được ruột) — khác hẳn hai ca
        # "báo cáo trung thực" là chạm max_iter / chưa đủ vòng-cạn, hai ca đó GIỮ rc=0 như cũ.
        out["note"] = (f"CHƯA soi được ruột {len(khong_doc_duoc)} ứng viên IN-CORPUS ⇒ KHÔNG thể kết luận hội tụ. "
                       "Xử lý `khong_doc_duoc` (kiểm gws/cache, hoặc nạp bản đọc được) rồi chạy lại. " + out["note"])
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        # r295/T1-c: thêm nhánh chẩn đoán THỨ BA — trước đây ca không-đọc-được bị in nhầm thành
        # "chưa đủ vòng-cạn", người đọc đi tăng --dry-rounds mà vô ích (đúng lớp sai-chẩn-đoán r252 đã vá).
        _why252 = ("HỘI TỤ" if out["converged"] else
                   (f"KHÔNG kết luận được: {len(khong_doc_duoc)} ứng viên IN-CORPUS không soi được ruột"
                    if khong_doc_duoc else
                    (f"CHƯA hội tụ (chạm max-iter={max_iter}, còn {len(frontier)} ứng viên — tăng --max-iter)"
                     if stop_reason == "max_iter" else
                     f"frontier CẠN nhưng dry_rounds={dry_rounds} < {K} (chưa đủ vòng-cạn để chốt hội tụ)")))
        print(f"== rasoat-loop {base_name[:34]} · {it} vòng · seen={len(seen)} · {_why252} ==")
        print(f"  GAP ngoài corpus ({len(gap_sh)}): {', '.join(gap_sh[:12])}")
        if khong_doc_duoc:
            print(f"  KHÔNG đọc được ({len(khong_doc_duoc)}): "
                  + ", ".join(f"{x['sohieu']} [{x['ly_do']}]" for x in khong_doc_duoc[:8]))
        if out["in_corpus_not_on_nlm"]:
            print(f"  Trong corpus CHƯA NLM ({len(out['in_corpus_not_on_nlm'])}): {', '.join(out['in_corpus_not_on_nlm'][:10])} → tl ingest-missing --apply")
        print("  " + out["note"])
    return 2 if khong_doc_duoc else 0


def cmd_footnote_map(a) -> int:
    """B3: chỉ xuất bản đồ sửa đổi cấp Điều (footnote-resolver) cho 1 văn bản (gdocId|số hiệu|--text-file)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    text, entries = "", []
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))   # cho B2 fill hiệu_lực từ registry
    except Exception:
        entries = []
    if getattr(a, "text_file", None):
        text = Path(a.text_file).read_text(encoding="utf-8", errors="replace")
    elif getattr(a, "target", None):
        gid = a.target; _src_name = a.target
        # (HỢP NHẤT Codex) deep-resolve (ưu tiên GDoc/corpus/live, by-name luôn chạy → bug C/P0-1).
        _de, _dgid, _dname, _dhits = _resolve_deep_target(a.target, entries)
        if _de is not None:
            gid = _dgid or gid
            _src_name = _dname or _src_name
        # P1: entry THÔ (.docx/.pdf/.html) → bỏ qua sạch, KHÔNG đọc vô ích.
        if _is_raw_no_gdoc_name(_src_name):
            return _emit_raw_no_gdoc(_src_name, getattr(a, "json", False))
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        text = _read_doc_text(gid, getattr(a, "config", None))   # gws-first (bypass exporttext OAuth)
        if not text:
            # P1: đọc rỗng + entry thô → ENTRY_RAW_NO_GDOC rc=2 (thống nhất với xref/extract; tiền điều kiện đọc sâu chưa đạt).
            if _raw_no_gdoc(_src_name):
                return _emit_raw_no_gdoc(_src_name, getattr(a, "json", False))
            print(json.dumps({"ok": False, "error": "không đọc được text (gws/transport + exporttext)"}, ensure_ascii=False), file=sys.stderr); return 2
    else:
        print("[tl] footnote-map cần <gdocId|số hiệu> hoặc --text-file", file=sys.stderr); return 2
    fn = resolve_footnote_amendments(text, entries=entries)
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, **fn}, ensure_ascii=False, indent=2))
    else:
        rows = fn["dieu_level_amendment_map"]
        npend = fn.get("pending_effect_count", sum(1 for r in rows if r.get("pending_effect")))
        bpend = fn.get("body_pending_effect_count", 0)
        print(f"== footnote-map · {fn['footnote_count']} chú thích · {len(rows)} điểm sửa cấp Điều · pending={npend}"
              + (f" (body={bpend})" if bpend else "") + " ==")
        for r in rows:
            pe = " ⏳PENDING" if r.get("pending_effect") else ""
            rk = {"CROSS_CUTTING": " ⇄CẮT-NGANG(omnibus, hạ ưu tiên)", "PARTIAL_REPEAL": " ⊘BÃI-BỎ-CỤC-BỘ(hạ ưu tiên)"}.get(r.get("rel_kind"), "")
            dm = ("đ" + r["diem"] + " ") if r.get("diem") else ""
            print(f"  [{r['marker']}] Điều {r['dieu']} {('K'+r['khoan']) if r.get('khoan') else ''} ← {r['amending_sohieu'] or '?'} "
                  f"({dm}{r.get('amending_vitri') or ''}) HL {r.get('hieu_luc') or '?'} [{r.get('loai') or '?'}]{rk}{pe}")
        for b in fn.get("body_effective_dates") or []:
            pe = " ⏳PENDING" if b.get("pending_effect") else ""
            pos = (", ".join(b.get("positions") or []) or "toàn văn/điều khoản")
            print(f"  [BODY] {pos} HL {b.get('hieu_luc') or '?'}{pe} — {b.get('scope','')[:120]}")
    return 0


def cmd_dedup_check(a) -> int:
    """WS1: dedup theo MANIFEST OFFLINE. #3: TÁCH số hiệu khỏi query gộp → quét trùng SỐ HIỆU CHÍNH XÁC TRƯỚC
    (kể cả khi query có cả tên) → COLLISION nếu ≥2 thực thể cùng số hiệu (giữ CANONICAL, quarantine DUP)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] dedup-check: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    q = a.query
    qkeys = set()                                    # token giống số hiệu (có CHỮ) tách khỏi query
    for t in re.findall(r"[0-9][0-9A-Za-zĐ/\-]{2,}", q):
        nk = norm_sohieu(t)
        if nk and re.search(r"[A-ZĐ]", nk):
            qkeys.add(nk)
    exact_group = [e for e in entries if _sohieu_key_entry(e) in qkeys] if qkeys else []
    # VBHN-first (bất biến #1): nếu query LÀ BẢN GỐC của một VBHN (số hiệu KHÁC, vd 64/2020/QH14 ↔ 123-VBHN-VPQH)
    # thì canonical = VBHN, các bản gốc → SUPERSEDED. Dùng đúng điều kiện base-goc của _source_map_one để không
    # redirect nhầm (chỉ khi _vbhn_base_key == query, không phải 1 luật SỬA trong chuỗi). KHÔNG ảnh hưởng dedup thường.
    vbhn_first = sorted(
        [e for e in entries if _is_vbhn_entry(e) and (qkeys & _goc_keys(e)) and _vbhn_base_key(e) in qkeys],
        key=_entry_score, reverse=True) if qkeys else []
    vbhn_canon = vbhn_first[0] if vbhn_first else None
    canon = vbhn_canon if vbhn_canon is not None else (max(exact_group, key=_entry_score) if exact_group else None)
    def _dedup_role(e):
        if e is canon:
            return "CANONICAL"
        return "SUPERSEDED" if (vbhn_canon is not None and e in exact_group) else "DUP"
    roles = [{"sohieu": _entry_sohieu(e) or _sohieu_key_entry(e), "name": _entry_name(e)[:70], "cat": _entry_cat(e),
              "nlm": bool(_entry_nlm(e)), "role": _dedup_role(e)}
             for e in sorted(vbhn_first + exact_group, key=_entry_score, reverse=True)]
    hits = resolve_identity(q, entries, max_hits=6)
    if vbhn_canon is not None:
        verdict = "VBHN_FIRST"
    elif len(exact_group) >= 2:
        verdict = "COLLISION"
    elif exact_group or any("sohieu" in r for _, _, r in hits):
        verdict = "DUPLICATE"
    elif hits:
        verdict = "MAYBE"
    else:
        verdict = "NEW"
    out = {"ok": True, "query": q, "sohieu_keys": sorted(qkeys), "verdict": verdict,
           "exact_sohieu_collision": roles,
           # A6 (v1.33.9 — log rà: driver đọc `groups` thấy 0 → kết luận 'không trùng' SAI dù verdict=COLLISION):
           # alias vocab đồng bộ họ audit — cùng payload, 2 tên khoá quen thuộc.
           "groups": roles, "duplicates": roles,
           "fuzzy_candidates": [{"sohieu": _entry_sohieu(e), "name": _entry_name(e)[:70], "cat": _entry_cat(e),
                                 "nlm": bool(_entry_nlm(e)), "score": s, "match": r} for e, s, r in hits],
           "note": "VBHN_FIRST=query là BẢN GỐC của VBHN (số hiệu khác) → canonical=VBHN, các bản gốc→SUPERSEDED (quarantine qua `tl hygiene plan`); "
                   "COLLISION=≥2 thực thể CÙNG số hiệu → dọn (giữ CANONICAL, quarantine DUP qua `tl hygiene plan`); "
                   "DUPLICATE=trùng số hiệu/tên; MAYBE=khớp tên/alias (verify số+năm+loại+dòng đầu); NEW=chưa thấy."}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        print(f"{verdict} · {q} · số hiệu={sorted(qkeys) or '∅'} · exact={len(exact_group)} fuzzy={len(hits)}")
        for r in roles:
            print(f"  [{r['role']}] {r['sohieu']} | {r['name']} | nlm={r['nlm']} | cat={r['cat']}")
        for e, s, r in hits:
            print(f"  (fuzzy {s}) {_entry_sohieu(e) or '∅'} | {_entry_name(e)[:55]} | {r}")
    return 0


def cmd_cluster(a) -> int:
    """E2: tra cụm lĩnh vực — 'pháp luật về <X>' → số hiệu canonical (VBHN-first). Không tham số → liệt kê toàn bộ."""
    q = (getattr(a, "query", None) or "").strip()
    if not q:
        print(json.dumps({"ok": True, "clusters": _load_subject_clusters().get("clusters", {})}, ensure_ascii=False, indent=2))
        return 0
    r = _cluster_lookup(q)
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, **r}, ensure_ascii=False, indent=2))
    elif r["matches"]:
        for m in r["matches"]:
            print(f"  {m['subject']} → {m['sohieu']}  (cụm {m['cluster']}, base {m['base']})")
    else:
        print(f"  (không có ánh xạ cụm cho '{q}' — bổ sung references/subject_clusters.json)")
    return 0


def _rasoat_corpus_hieu_luc(e) -> bool:
    """PURE — r295/T1-c (RAS-13, audit lõi 31-07): một dòng registry có thuộc CORPUS HIỆU LỰC không.

    "Có trong corpus" phải hiểu là DÙNG ĐƯỢC để đối chiếu, không phải "có dòng nào mang số hiệu đó".
    Loại ĐÚNG BA thứ đã được chứng minh là dương-tính-giả:
      · `corpus` ghi rõ "false"  (bản đã cố ý HẠ khỏi corpus)
      · cat cách ly (`_is_quarantine_cat`: mọi biến thể 'quarantine'/'zzz')
      · `row_kind == "ref"` (dòng tham chiếu, không phải bản văn trong kho)

    ★ CỐ Ý KHÔNG dùng `_entry_corpus_true` (nó đòi == "true" nên coi THIẾU CỘT là ngoài corpus).
    Ở đây "thiếu cột" là KHÔNG BIẾT, mà biến không-biết thành "thiếu corpus" chính là ÂM TÍNH GIẢ —
    đúng thứ mà chốt S3 ngay trong `cmd_rasoat_chongcheo` ("KHÔNG có manifest → đừng khẳng định thiếu
    corpus") sinh ra để chặn. Siết thêm vế đó làm đỏ `cluster_dup_sohieu_disambig` (fixture không có
    cột `corpus`) — bắt được lúc chạy full suite, và đó là bằng chứng vế ấy nằm NGOÀI phát hiện RAS-13.

    Trước bản vá, `rasoat-chongcheo` so số hiệu trên TOÀN `entries` nên một bản đã hạ `corpus=false`
    hoặc đã đẩy vào quarantine vẫn làm lệnh kết luận "ĐÃ CÓ trong corpus" — giấu mất đúng khoảng trống
    mà lệnh sinh ra để tìm. Đặt thành hàm dùng chung để hai call-site (`_in_corpus` và
    `_resolve_cluster_member`) không thể trôi khỏi nhau như đã trôi.
    """
    try:
        return (str(e.get("corpus") or "").strip().lower() != "false"
                and not _is_quarantine_cat(_entry_cat(e))
                and _entry_row_kind(e) != "ref")
    except Exception:  # noqa: BLE001
        return False


def cmd_rasoat_chongcheo(a) -> int:
    """E1 (v1 — lớp DISCOVERY): dựng TẬP LIÊN QUAN của 1 base = cụm lĩnh vực (E2) + footnote-amend (B3 nếu có --target/--text-file)
    + kiểm hiện diện corpus + cờ PENDING_EFFECT. So sánh quy phạm (OVERLAP_SCOPE/CONFLICT_NORM/PRIORITY/STALE_REF/GAP)
    cần ĐỌC NGUYÊN VĂN đã verify — giai đoạn sau (không RAG)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    base = (getattr(a, "base", None) or getattr(a, "query", None) or "").strip()
    if not base:
        print("[tl] rasoat-chongcheo cần --base <số hiệu|tên>", file=sys.stderr); return 2
    cname, c = _cluster_for_base(base)
    if not c:
        lk = _cluster_lookup(base)
        if lk["matches"]:
            cname = lk["matches"][0]["cluster"]; c = (_load_subject_clusters().get("clusters") or {}).get(cname)
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception:
        entries = []
    corpus_loaded = bool(entries)        # S3: KHÔNG có manifest → đừng khẳng định "thiếu corpus" (âm tính giả)
    def _in_corpus(sh):
        if not corpus_loaded:
            return None                  # chưa nạp corpus → KHÔNG XÁC ĐỊNH (≠ thiếu)
        k = norm_sohieu(sh)
        # r255 (P15 — repro: cụm lao_dong_xa_hoi báo ✗thiếu cho VBHN ĐÃ CÓ): đi qua cổng bare-VBHN
        # v1.33.47 như relation-check (681/694) + frontier-expand (fetch_web 211) — footnote/cụm ghi số
        # VBHN KHÔNG năm ('19/VBHN-VPQH') còn corpus lưu year-qualified ('19-2025-VBHN-VPQH') nên so
        # exact MISS SẠCH. Docstring _sohieu_query_hits_entry nêu thẳng `in_corpus` là call-site của nó.
        # GIỮ vế cũ (so thô) — nới chỉ THÊM, không thay hành vi đang đúng.
        # r295/T1-c (RAS-13): lọc theo CORPUS-HIỆU-LỰC trước khi so số hiệu. Bản cũ so số hiệu trên TOÀN
        # `entries` nên một dòng `corpus=false` / cat quarantine / `row_kind=ref` cũng làm lệnh kết luận
        # "ĐÃ CÓ trong corpus" — tức giấu mất đúng thứ lệnh chồng-chéo sinh ra để tìm. Trục lọc này KHÁC
        # trục r255 (bare-VBHN, so số hiệu) nên hai vế cộng hưởng, không giẫm nhau.
        return any(_sohieu_query_hits_entry(k, _sohieu_key_entry(e))
                   or norm_sohieu(_entry_sohieu(e)) == k
                   for e in entries if _rasoat_corpus_hieu_luc(e))
    related = []
    if c:
        for subj, sh in (c.get("members") or {}).items():
            rm = _resolve_cluster_member(sh, subj, entries)   # disambiguate khi số hiệu trùng, VBHN-first
            related.append({"subject": subj, "sohieu": sh,
                            "in_corpus": (None if not corpus_loaded else rm["in_corpus"]),   # S3: corpus trống → unknown
                            "resolved_name": rm.get("name"), "drive_id": rm.get("drive_id"),
                            "hieuluc": rm.get("hieuluc"), "ambiguous": rm.get("ambiguous", False),
                            "rel": "CUM_LINH_VUC"})
    # footnote-amend: #8 HỢP NHẤT — đọc nguyên văn VBHN base để chạy footnote-map. Ưu tiên --text-file/--target; nếu
    # KHÔNG có thì TỰ resolve base→VBHN gdoc rồi đọc (auto-footnote, best-effort) → chongcheo hết rỗng dù không truyền tay.
    # Tắt bằng --no-auto-footnote (vd corpus offline / né webapp).
    fn_pending = []
    text = ""
    base_subject_for_omni = base
    if getattr(a, "text_file", None):
        text = Path(a.text_file).read_text(encoding="utf-8", errors="replace")
    elif getattr(a, "target", None):
        gid = a.target
        if "/" in a.target or not re.fullmatch(r"[A-Za-z0-9_\-]{20,}", a.target):
            hits = resolve_identity(a.target, entries, max_hits=1)
            if hits: gid = _entry_drive_id(hits[0][0])
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        text = _read_doc_text(gid, getattr(a, "config", None))   # gws-first (bypass exporttext OAuth)
    elif corpus_loaded and not getattr(a, "no_auto_footnote", False):
        _be, _bg, _bs = _resolve_base_gdoc(base, entries)
        if _be is not None and _bg:
            base_subject_for_omni = _bs or base
            try:
                load_creds(getattr(a, "config", None), getattr(a, "profile", None))
                text = _read_doc_text(_bg, getattr(a, "config", None)) or ""
                if text:
                    print(f"[tl] rasoat-chongcheo: tự đọc nguyên văn base '{_entry_name(_be)[:50]}' → chạy footnote-map (auto). "
                          "(Tắt: --no-auto-footnote)", file=sys.stderr)
            except (Exception, SystemExit) as e:  # noqa: BLE001 — load_creds có thể sys.exit khi thiếu creds → KHÔNG giết lệnh
                print(f"[tl] rasoat-chongcheo: auto-footnote bỏ qua ({type(e).__name__}: {e}); truyền --target để ép.", file=sys.stderr)
                text = ""
    if text:
        fm = resolve_footnote_amendments(text, entries=entries)   # B2: fill hiệu_lực từ registry
        for r in fm["dieu_level_amendment_map"]:
            _omni = _omnibus_cross_domain_note(r.get("amending_sohieu") or "", base_subject_for_omni, entries)
            related.append({"subject": f"sửa Điều {r['dieu']} {('K'+r['khoan']) if r.get('khoan') else ''}".strip(),
                            "sohieu": r.get("amending_sohieu"), "in_corpus": _in_corpus(r.get("amending_sohieu") or ""),
                            "rel": "SUA_DOI_CAP_DIEU", "pending_effect": r.get("pending_effect"), "hieu_luc": r.get("hieu_luc"),
                            **({"omnibus_note": _omni} if _omni else {})})
            if r.get("pending_effect"):
                fn_pending.append({"dieu": r["dieu"], "khoan": r.get("khoan"), "diem": r.get("diem"),
                                   "amending_sohieu": r.get("amending_sohieu"), "hieu_luc": r.get("hieu_luc")})
        # E1 liên-domain: base TỰ sửa luật KHÁC cấp Điều (điều khoản thi hành) → gộp vào tập liên quan
        # (footnote-map chỉ bắt incoming). cross_domain_amendment=True khi số hiệu bị sửa NGOÀI cụm base.
        _rel_keys = {norm_sohieu(r.get("sohieu") or "") for r in related}
        _clk = {norm_sohieu(_sh) for _sh in (c.get("members") or {}).values()} if c else set()
        for _sh in _scan_inline_amendments(text):
            if _sh in _rel_keys:
                continue
            _rel_keys.add(_sh)
            related.append({"subject": "base sửa luật khác (Điều)", "sohieu": _sh,
                            "in_corpus": _in_corpus(_sh), "rel": "LIEN_DOMAIN_AMENDMENT",
                            "cross_domain_amendment": _sh not in _clk})
    # A6 (log1): DEDUP `related` theo số hiệu — cùng sohieu lọt qua (cụm + footnote + inline) → đếm trùng (vd 85-2015 ×4).
    _seen_rel, _dedup = set(), []
    for r in related:
        rk = norm_sohieu(r.get("sohieu") or "")
        if rk and rk in _seen_rel:
            continue
        if rk:
            _seen_rel.add(rk)
        _dedup.append(r)
    related = _dedup
    # A1/A4 (log1): CỜ RÕ thay vì no-op IM LẶNG. BASE_NO_CLUSTER = chưa có cụm E2 cho lĩnh vực này → E1 phủ HẠN CHẾ (dựa
    # xref/footnote-map cấp Điều). BASE_UNRESOLVED = base là tên/file THÔ không số hiệu → auto-footnote-read rỗng lặng lẽ.
    rc_flags = []
    if not cname:
        rc_flags.append("BASE_NO_CLUSTER")
    # BASE_UNRESOLVED chỉ khi base KHÔNG định danh được (file thô có đuôi HOẶC tên-không-phải-số-hiệu mà cũng không có cụm) —
    # KHÔNG fire cho số hiệu hợp lệ ngoài cụm (vd 134/2025 chỉ thiếu cụm → BASE_NO_CLUSTER là đủ).
    if _is_raw_no_gdoc_name(base) or (corpus_loaded and not _looks_like_sohieu_query(base) and not cname and not text):
        rc_flags.append("BASE_UNRESOLVED")
    # #6: pending_effect ở ĐÂY = pending CẤP ĐIỀU (từ footnote), CHỈ có khi đã đọc nguyên văn. Chưa đọc → n/a
    # (KHÔNG phải 0 — tránh hiểu nhầm "không có gì chờ hiệu lực"). Khác `unresolved_refs` (pending hiện-diện-VB).
    read_text = bool(text)
    _unresolved = [r["sohieu"] for r in related if r["in_corpus"] is False]   # S3: CHỈ False (≠None)
    out = {"ok": True, "base": base, "cluster": cname, "corpus_loaded": corpus_loaded, "flags": rc_flags,
           "related_count": len(related),
           # A5 (log1): đổi tên "missing_in_corpus"→"unresolved_refs" (giữ alias cũ) — CHƯA kết luận vắng mặt (khớp `exists`=
           # UNKNOWN_NOT_ABSENT); phải verify bằng `tl exists`/`vbhn-check` QT-5 trước khi nạp, tránh tự mâu thuẫn 2 cổng.
           "unresolved_refs": _unresolved, "missing_in_corpus": _unresolved,
           "unresolved_refs_note": "số hiệu KHÔNG resolve trong manifest — CHƯA kết luận vắng mặt; verify `tl exists`/QT-5 trước khi nạp.",
           "corpus_unknown": (None if corpus_loaded else "corpus CHƯA NẠP — chạy `tl boot`; hiện-diện = KHÔNG XÁC ĐỊNH (≠thiếu)"),
           "pending_effect_scope": "article" if read_text else "unknown",
           "pending_effect_count": (len(fn_pending) if read_text else None),
           "pending_effect": fn_pending, "related": related,
           "omnibus_cross_domain": [r for r in related if r.get("omnibus_note")],   # #11: luật sửa-nhiều-luật chéo lĩnh vực
           "note": "v1 DISCOVERY: tập liên quan + hiện diện. pending_effect = pending CẤP ĐIỀU (footnote) — chỉ có khi "
                   "đã đọc nguyên văn (--target/--text-file/auto). KHÁC missing_in_corpus (thiếu VB). OMNIBUS_CROSS_DOMAIN = "
                   "luật sửa có tên khác lĩnh vực (sửa-nhiều-luật) → đọc nguyên văn. So quy phạm: `tl overlap`."}
    if getattr(a, "json", False):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        _pend = out["pending_effect_count"] if read_text else "n/a(chưa đọc nguyên văn)"
        _miss = "?(corpus chưa nạp)" if not corpus_loaded else len(out["unresolved_refs"])
        _fl = (" · ⚑" + ",".join(rc_flags)) if rc_flags else ""
        print(f"== rà soát chồng chéo (v1 discovery) · base={base} · cụm={cname or '∅'} · liên quan={len(related)} · chưa-resolve={_miss} · pending_điều={_pend}{_fl} ==")
        if "BASE_NO_CLUSTER" in rc_flags:
            print("  ⚑ BASE_NO_CLUSTER: chưa có cụm E2 cho lĩnh vực này → E1 phủ HẠN CHẾ; dựa `tl xref`/`footnote-map` cấp Điều (cân nhắc bổ sung subject_clusters.json).")
        if "BASE_UNRESOLVED" in rc_flags:
            print("  ⚑ BASE_UNRESOLVED: base là tên/file THÔ không số hiệu → KHÔNG đọc được nguyên văn; chuẩn hoá số hiệu (`standardize_name`+`register`) hoặc truyền `--target <gdocId>`.")
        if not corpus_loaded:
            print("  ⚠ CORPUS CHƯA NẠP (manifest trống) — hiện-diện = KHÔNG XÁC ĐỊNH (≠thiếu). Chạy `tl boot` rồi rà lại.")
        for r in related:
            pe = " ⏳PENDING" if r.get("pending_effect") else ""
            mc = "?corpus" if r["in_corpus"] is None else ("✓corpus" if r["in_corpus"] else "✗thiếu")
            amb = " ⚠TRÙNG-SỐ-HIỆU" if r.get("ambiguous") else ""
            omn = " ⚠OMNIBUS" if r.get("omnibus_note") else ""
            rn = f" → {r['resolved_name'][:46]}" if r.get("resolved_name") else ""
            print(f"  - [{r['rel']:16s}] {r['subject'][:34]:34s} → {r['sohieu'] or '?':16s} {mc}{pe}{amb}{omn}{rn}")
        _omni_rows = [r for r in related if r.get("omnibus_note")]
        if _omni_rows:
            print("  ⚠ OMNIBUS / SỬA-NHIỀU-LUẬT (tên luật sửa khác lĩnh vực base — KHÔNG phải lỗi, đọc nguyên văn để xác nhận):")
            for r in _omni_rows:
                print(f"     {r['subject']} ← {r['sohieu']}: {r['omnibus_note'].split(': ',1)[-1][:120]}")
        if fn_pending:
            print("  ⏳ HIỆU LỰC TƯƠNG LAI (B4 — mục theo dõi riêng, chưa áp dụng):")
            for p in fn_pending:
                print(f"     Điều {p['dieu']} {('K'+p['khoan']) if p.get('khoan') else ''} ← {p['amending_sohieu']}, hiệu lực {p['hieu_luc']}")
        _ov_target = getattr(a, "target", None) or base
        print(f"  → BƯỚC SO QUY PHẠM (OVERLAP/CONFLICT) nguyên văn 2 phía: `tl overlap {_ov_target} --with-source` "
              f"(trích Điều bị sửa + điều luật sửa; KHÔNG RAG).")
    return 0

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


def _base_also_enabled(a=None) -> bool:
    """A (v1.30.0): chế độ 'profile CỘNG VBQPPL' cho lệnh ĐỌC. Ưu tiên: cờ lệnh --base-also/--no-base-also >
    env TL_BASE_ALSO (do _apply_profile_env set theo config.profiles.<p>.baseAlso) > TẮT ở profile nền vbqppl."""
    v = getattr(a, "base_also", None) if a is not None else None
    if v is not None:
        return bool(v)
    if _active_profile() == DEFAULT_PROFILE:
        return False
    return (os.environ.get("TL_BASE_ALSO") or "").strip().lower() in ("1", "true", "yes", "on")

def _nlm_display(e: dict) -> str:
    """Hiển thị NLM STATUS-AWARE (đồng bộ locate ↔ reg-query): '-' không có source; 'removed' có source nhưng đã gỡ;
    'Y' đang sống. Trước đây locate in nlm=Y dù nlm_status=removed → lệch với reg-query (báo removed)."""
    if not _entry_nlm(e):
        return "-"
    return "removed" if _nlm_status_removed(str(e.get("nlm_status") or "")) else "Y"

def _flag_value(args: list, flag: str):
    """Lấy giá trị đi sau cờ `flag` trong list args (hỗ trợ `--flag val` và `--flag=val`). None nếu không có."""
    for i, x in enumerate(args):
        if x == flag and i + 1 < len(args):
            return args[i + 1]
        if x.startswith(flag + "="):
            return x.split("=", 1)[1]
    return None

def _read_verify_text(a) -> tuple[str, str]:
    text_file = getattr(a, "text_file", None)
    gdoc = getattr(a, "gdoc_id", None)
    sohieu = getattr(a, "sohieu", None)
    # vbhn positional-compat (tương thích runbook cũ): `tl vbhn-verify "<text-file|gdoc-id|số hiệu>"` → tự định tuyến.
    target = getattr(a, "target", None)
    if target and not (text_file or gdoc or sohieu):
        tp = Path(target)
        if tp.exists():
            text_file = str(tp)
        elif re.fullmatch(r"[A-Za-z0-9_\-]{20,}", target):
            gdoc = target
        else:
            sohieu = target
    if text_file:
        p = Path(text_file)
        return p.read_text(encoding="utf-8", errors="replace"), str(p)
    if not gdoc and sohieu:
        canon, _hits = _canonical_for_query(sohieu, refresh=getattr(a, "refresh", False))
        if canon:
            gdoc = _entry_drive_id(canon)
    if not gdoc:
        raise RuntimeError("cần --text-file hoặc --gdoc-id hoặc --sohieu resolve được")
    load_creds(getattr(a, "config", None))
    # A1 (v1.33.10 — log: xref/vbhn-verify chết 'thiếu scope script.external_request' TRONG KHI direct-media gws
    # đang SỐNG): đường đọc phải GWS-FIRST như extract/corpus-audit — _read_doc_text = cache → direct-media →
    # transport → exporttext CUỐI CÙNG; không gọi thẳng exporttext nữa.
    _txt = _read_doc_text(gdoc, getattr(a, "config", None))
    if not (_txt or "").strip():
        raise RuntimeError("đọc nguyên văn thất bại MỌI đường (cache/direct-media/gws/exporttext) — kiểm `tl gws-ping`; "
                           "webapp exporttext chỉ sống khi có scope script.external_request (fallback cuối).")
    return _txt, gdoc

def _norm_compare_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s or "")
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\s*\n\s*", "\n", s)
    return s.strip()

def _legal_refs(text: str) -> list[str]:
    """Rút các tham chiếu kiểu 'khoản 1 Điều 90' để bắt stale-ref trong bản tự ghép."""
    # r296 (P16-F15, cùng họ): `\d+\b` làm tham chiếu tới điều có HẬU TỐ CHỮ rơi mất HOÀN TOÀN —
    # "khoản 1 Điều 7a" không sinh ra ref nào (đo được). Hàm này dùng để BẮT stale-ref, nên bỏ sót ref là
    # fail-OPEN: bản tự ghép trỏ sai vào Điều 7a sẽ đi qua mà không ai thấy.
    out = []
    for m in re.finditer(r"(?iu)\b(?:khoản\s+\d+\s+)?Điều\s+\d+[a-zđ]*\b", text or ""):
        ref = re.sub(r"\s+", " ", m.group(0).strip())
        if ref not in out:
            out.append(ref)
    return out

def _date_from_effect_match(m) -> str | None:
    if not m:
        return None
    return f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"

def _multi_diem(target_clause: str, single):
    """footnote_multidiem: _POS_RE chỉ bắt 1 điểm (sát khoản) → "điểm c VÀ điểm d khoản 2 Điều 30" rơi mất "c".
    Bắt CẢ DÃY điểm đích → trả "c và d"; không phải dãy → giữ `single` (1 điểm) như cũ."""
    if not target_clause:
        return single
    s = _strip_accents(target_clause).lower()
    m = _DIEMLIST_RE.search(s)
    if m:
        items, seen = re.findall(r"\b([a-z]{1,3}\d?)\b", m.group(1)), []
        for x in items:
            if x not in ("va",) and x not in seen:
                seen.append(x)
        if len(seen) >= 2:
            return " và ".join(seen)
    return single

def _raw_no_gdoc(name: str = "", api_resp=None) -> bool:
    """P1: nhận diện 'entry THÔ chưa có bản GDoc' — theo đuôi tên HOẶC lỗi API 'Export only supports Docs Editors files'."""
    if _is_raw_no_gdoc_name(name):
        return True
    s = (json.dumps(api_resp, ensure_ascii=False).lower() if api_resp is not None else "")
    return "export only" in s or "docs editors" in s

def _emit_raw_no_gdoc(name: str, as_json: bool) -> int:
    """ENTRY_RAW_NO_GDOC → rc=2 (TIỀN ĐIỀU KIỆN đọc sâu CHƯA ĐẠT: entry thô, không export GDoc được) + STDOUT rõ.
    HỢP NHẤT P0-1: trước (bản Claude) rc=0 → caller agentic hiểu nhầm 'thành công, 0 dẫn chiếu' → bỏ sót luật;
    nay rc=2 + ok:false (đúng yêu cầu báo cáo 'chỉ-raw → rc≠0 + thông điệp stdout'). Resolver đã ưu tiên GDoc trước
    nên path này CHỈ chạy khi GENUINE raw-only (không có bản GDoc) → rc≠0 hợp lý, KHÔNG phá batch sai."""
    note = (f"ENTRY_RAW_NO_GDOC: '{(name or '?')[:60]}' là file THÔ (chưa có bản GDoc Google-native) → "
            f"`tl ingest-local`/convert sang GDoc trước khi rà sâu (xref/footnote-map/extract).")
    if as_json:
        print(json.dumps({"ok": False, "error": "ENTRY_RAW_NO_GDOC", "note": note}, ensure_ascii=False))
    else:
        print(f"[tl] {note}")
    return 2

def _read_doc_text(gdoc_id: str, config=None, *, use_cache: bool = True):
    """Đọc nguyên văn GDoc → text. THỨ TỰ: (B1) direct-media EXPORT text/plain bằng gws CRED (KHÔNG cần binary gws —
    chỉ cần ~/.config/gws/credentials.json → né GAS, hết spam FALLBACK) → transport→gws (binary) → webapp exporttext.
    Trả str (rỗng nếu lỗi mọi đường). v1.31.2: mọi nhánh qua _sanitize_export_text (U1).

    r183: `use_cache=False` cho đường ĐỌC-XEM markup (mark/raw) — cache extract_<id>.txt là bản CHUẨN
    (strip); dùng nó cho mark/raw là trả bản khác chế độ người dùng xin mà không nói gì."""
    # (D — log rà: timeout văn bản lớn) TÁI DÙNG cache text mà cmd_extract/cmd_cache_build đã ghi ra đĩa
    # (extract_<gdoc>.txt) TRƯỚC khi export lại → xref/footnote-map trên cùng văn bản (vd Bộ luật Dân sự)
    # không phải export lần 2 (hết timeout > 20s). Chỉ dùng khi cache CÓ + đọc được.
    try:
        _cf = _cache_file(f"extract_{gdoc_id}.txt")
        if use_cache and _cf.exists():
            _ct = _cf.read_text(encoding="utf-8", errors="replace")
            if _ct.strip():
                return _sanitize_export_text(_strip_font_runs(_ct))
    except Exception:
        pass
    # (1) direct-media export bằng cred — cred-only đủ, không cần `gws-bootstrap-cowork`/binary.
    # v1.33.0 (log rà 69 A3): cred đã chết auth (invalid_grant) 1 lần trong phiên → SKIP thẳng (circuit-breaker),
    # không retry-fail per-doc (~2-20s/doc × 69 làm batch vượt timeout shell).
    try:
        _tlg = _imp("tl_gws")
        _cred = _tlg._read_gws_cred()
        if _cred and not getattr(_tlg, "_CRED_AUTH_DEAD", False):
            with tempfile.TemporaryDirectory() as _d:
                _dst = os.path.join(_d, "doc.txt")
                _tlg._drive_media_download(gdoc_id, _dst, _cred, export_mime="text/plain")
                _txt = open(_dst, encoding="utf-8", errors="replace").read()
                if _txt.strip():
                    return _sanitize_export_text(_strip_font_runs(_txt))
    except Exception:
        pass
    # (2) transport→gws binary; (3) webapp exporttext (GAS).
    # v1.34.60 (A1 footgun-fix — bài học dedup 2026-07-16): file KHÔNG Docs-native (.docx) qua đường 'read'
    # có thể trả NGUYÊN BINARY zip ('PK\x03\x04…') như thể text → caller so char-count/verify trên rác binary.
    # Guard _text_looks_binary: payload binary → coi như KHÔNG đọc được (""); đường đúng cho .docx/.pdf là
    # `tl doc-text` (_doc_text_any: download + unzip word/document.xml / pdftotext).
    try:
        rr = _imp("transport").drive_op("read", file_id=gdoc_id, limit=2_000_000)
        if isinstance(rr, dict) and rr.get("ok") and rr.get("text") is not None:
            if not _text_looks_binary(rr.get("text", "")):
                return _sanitize_export_text(_strip_font_runs(rr.get("text", "")))
    except Exception:
        pass
    r = _gas().get("exporttext", fileId=gdoc_id)
    if r.get("ok") is False or _text_looks_binary(r.get("text", "")):
        return ""
    return _sanitize_export_text(_strip_font_runs(r.get("text", "")))


def _text_looks_binary(s: str) -> bool:
    """PURE (A1 v1.34.60): payload 'text' thực chất là BINARY — zip .docx ('PK\\x03\\x04'), PDF ('%PDF')
    hoặc chứa NUL trong 4KB đầu. Dùng làm guard mọi đường export-text trước khi trao cho caller."""
    if not s:
        return False
    return s[:4].startswith("PK\x03\x04") or s[:5].startswith("%PDF") or ("\x00" in s[:4096])


def _doc_text_fetch_binary(file_id: str, *, suffix: str = ".bin", export_mime: str | None = None):
    """A1 (v1.34.60): tải BINARY Drive → file tạm, trả Path hoặc None. Ưu tiên gws cred direct-media
    (1 hop, không b64, không cap 9MB — mẫu _read_doc_text B1); fallback transport download. Caller tự dọn.

    r183: `export_mime` để EXPORT file Google-native (Doc → .docx) — alt=media KHÔNG tải được Docs-native,
    phải đi /export. Đây là đường duy nhất lấy được markup sửa đổi của một Google Doc."""
    dst = Path(tempfile.mkdtemp(prefix="tl_doctext_")) / f"doc{suffix}"
    try:
        _tlg = _imp("tl_gws")
        _cred = _tlg._read_gws_cred()
        if _cred and not getattr(_tlg, "_CRED_AUTH_DEAD", False):
            _tlg._drive_media_download(file_id, str(dst), _cred, export_mime=export_mime)
            if dst.exists() and dst.stat().st_size > 0:
                return dst
    except Exception:  # noqa: BLE001
        pass
    try:
        _kw = {"dest": str(dst), "export_mime": export_mime} if export_mime else {"out": str(dst)}
        rr = _imp("transport").drive_op("download", file_id=file_id, **_kw)
        if isinstance(rr, dict) and rr.get("ok") and dst.exists() and dst.stat().st_size > 0:
            return dst
    except Exception:  # noqa: BLE001
        pass
    return None


_GDOC_DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

# r183 — câu cảnh báo cho nguồn Google Doc KHÔNG chứng minh được là đã lọc markup. Bẫy đo 23-07-2026:
# `--markup strip` trên Google Doc trả CHÍNH BẢN THÔ (chữ đã bỏ đọc thành quy phạm hiện hành) mà rc=0.
_GDOC_MARKUP_WARN = (
    "[markup] ⚠ KHÔNG CHỨNG MINH ĐƯỢC ĐÃ LỌC MARKUP ({fid}) — chế độ `--markup {mode}` không lọc được "
    "gì: {why}. Bản Google Doc trong kho THƯỜNG ĐÁNH RƠI markup sửa đổi khi convert (giữ CHỮ, mất "
    "gạch-bỏ) ⇒ KHÔNG được coi kết quả này là 'đã loại chữ đã bỏ', và KHÔNG dùng làm căn cứ trích dẫn "
    "dự thảo. Đường đúng: về .docx GỐC (`tl download <id> --export-mime {dm}` hoặc file gốc) rồi đọc "
    "lại; kiểm chứng bằng `--markup mark` (0 nhãn ⟦BỎ⟧ = không có dấu vết nào để lọc). "
    "Muốn CHẶN CỨNG thay vì cảnh báo: thêm `--markup-strict`.")


def _gdoc_docx_text(file_id: str, mode: str = "strip") -> tuple:
    """r183: đọc một Google Doc QUA BẢN EXPORT .docx để giữ được markup sửa đổi (w:strike/w:ins/w:del) —
    export text/plain của `_read_doc_text` san phẳng hết, nên `--markup` thành no-op IM LẶNG.
    Trả (text, stats) — ("", None) nếu không export/không đọc được (caller tự rơi về đường cũ + cảnh báo)."""
    p = _doc_text_fetch_binary(file_id, suffix=".docx", export_mime=_GDOC_DOCX_MIME)
    if p is None:
        return "", None
    try:
        with open(p, "rb") as _fh:
            if not _fh.read(4).startswith(b"PK\x03\x04"):   # export lỗi → HTML/JSON lỗi, không phải docx
                return "", None
        st = _imp("docx_markup").scan_file(p)
        t = _docx_unzip_text(p, mode or "strip")
        return (t, st) if t else ("", None)
    except Exception:  # noqa: BLE001
        return "", None
    finally:
        try:
            os.unlink(p)
            os.rmdir(Path(p).parent)
        except Exception:  # noqa: BLE001 — temp OS tự dọn
            pass


def _docx_unzip_text(path, mode: str = "strip") -> str:
    """PURE-ish (A1): bóc text THẬT từ .docx local = unzip word/document.xml + strip tag (mẫu
    _profile_read_probe_text v1.34.27 — không cần lib ngoài). </w:p> → newline giữ cấu trúc Điều.

    r182: strip-tag TRẦN giữ CẢ w:delText ⇒ `tl doc-text`/`tl extract` đọc chữ ĐÃ BỎ của dự thảo như
    quy phạm còn hiệu lực (sai ĐÚNG-SAI về nội dung pháp luật). Nay lọc markup TRƯỚC khi bóc tag.
    Mặc định `strip` vì text này ĐƯỢC CACHE + nuôi corpus: chữ đã bỏ tuyệt đối không được lẫn vào kho;
    người rà muốn thấy dấu vết thì `tl doc-text --markup mark` (đường đó không đụng cache)."""
    import zipfile as _zf
    try:
        from tl_core.ingest_engine import read_member_bounded   # r188 SEC-01: chống zip-bomb
        with _zf.ZipFile(path) as z:
            xml = read_member_bounded(z, "word/document.xml").decode("utf-8", errors="replace")
        _dm = _imp("docx_markup")
        xml, _st = _dm.strip_markup(xml, mode)
        _w = _dm.warn_line(_st, str(path))
        if _w:
            print(_w, file=sys.stderr)
        # r252: dùng CHUNG `plain_from_document_xml` — bản cũ bóc tag mà KHÔNG unescape entity nên
        # `&amp;`/`&lt;` chui nguyên văn vào text ĐƯỢC CACHE và NUÔI CORPUS (xem docstring hàm đó).
        return _dm.plain_from_document_xml(xml)
    except Exception:  # noqa: BLE001 — docx hỏng/mã hoá → coi như không đọc được
        return ""


def _markup_warn(fid: str, mode: str, why: str, meta=None) -> str:
    """r186 (tách từ `_doc_text_any` để `cmd_extract` DÙNG CHUNG — hai lệnh cùng bẫy thì phải cùng một
    câu cảnh báo, không được lệch chữ). In stderr + ghi `meta`; trả câu cảnh báo (rỗng nếu không cảnh
    báo). `raw` = đối chứng CÓ CHỦ ĐÍCH ⇒ im lặng là đúng; mọi chế độ LỌC mà không chứng minh được là
    đã lọc ⇒ phải nói."""
    _m = meta if isinstance(meta, dict) else {}
    if (mode or "").strip().lower() == "raw" or _m.get("markup_warning"):
        return ""
    w = _GDOC_MARKUP_WARN.format(fid=fid or "?", mode=mode, why=why, dm=_GDOC_DOCX_MIME)
    _m["markup_warning"] = w
    print(w, file=sys.stderr)
    return w


def _markup_cert_path(fid: str):
    """SIDECAR chứng nhận của cache `extract_<id>.txt` — nguồn sự thật 'text này ĐÃ qua docx_markup chưa'."""
    return _cache_file(f"extract_{fid}.txt.markup.json")


def _markup_cert_write(fid: str, *, filter_ran: bool, found: bool, source: str = "") -> None:
    """r183/r186: ghi chứng nhận CÙNG LÚC với cache chuẩn. Không có sidecar = cache cũ/đường text-plain
    ⇒ lần đọc sau CẢNH BÁO thay vì im lặng (đóng vòng poison extract → cache → doc-text → corpus)."""
    try:
        _p = _markup_cert_path(fid)
        _p.parent.mkdir(parents=True, exist_ok=True)
        _p.write_text(json.dumps({"v": "r183", "filter_ran": bool(filter_ran), "found": bool(found),
                                  "source": source}, ensure_ascii=False), encoding="utf-8")
    except Exception:  # noqa: BLE001 — chứng nhận best-effort; thiếu nó = cảnh báo, KHÔNG phải im lặng
        pass


def _markup_cert_read(fid: str) -> dict:
    try:
        _p = _markup_cert_path(fid)
        return (json.loads(_p.read_text(encoding="utf-8")) or {}) if _p.exists() else {}
    except Exception:  # noqa: BLE001
        return {}


def _text_thieu_khoi_dau(text) -> bool:
    """PURE (r215 — sổ lỗi `CACHE_BUILD_DANH_ROI_KHOI_DAU_VAN_BAN`): text VÀO THẲNG thân văn bản, tức
    KHÔNG có khối đầu (Quốc hiệu · cơ quan ban hành · `Số: …` · địa danh-ngày tháng · tên loại + trích
    yếu · khối `Căn cứ…`).

    Đây là cổng chặn cái đã trả giá THẬT hai lần: bản cache dựng-lại-từ-`articles` bắt đầu từ "Điều 1"
    ⇒ `_classify_doc_header` không còn gì để đọc trong vùng tiêu đề nên đi quét sâu 16k và **nhặt số
    hiệu từ THÂN** (ca VBHN Luật NSNN `89-2026` trả về `145/2025/QH15` — số của luật SỬA ĐỔI được liệt
    kê trong thân). Máy đoán thì phải nói là đang đoán.

    CỐ Ý hẹp và tất định: chỉ bắt khi ký tự đầu tiên có nghĩa là mốc cấu trúc THÂN (`Điều N.` /
    `Chương <La Mã>` / `Mục N`). Văn bản phụ lục độc lập (mở đầu `PHỤ LỤC`) hay văn bản có letterhead
    KHÔNG bị bắt ⇒ không đẻ báo động giả trên corpus đang chạy."""
    t = (text or "").lstrip()
    if not t:
        return False
    return bool(re.match(r"(?:Điều\s+\d+[a-zđ]*\s*\.|Chương\s+[IVXLC]+\b|Mục\s+\d+\b)", t))


def _doc_text_any(file_id: str, *, entry=None, refresh: bool = False, config=None,
                  markup: str = "strip", meta=None) -> tuple:
    """A1 (v1.34.60 — kế hoạch NLM-fallback E1–E3, TIỀN ĐỀ E1): MỘT đường đọc text cho MỌI định dạng.
    Route theo mime/tên (manifest entry): GDoc→export (_read_doc_text, giữ đường cũ); .docx→download+unzip
    word/document.xml; .pdf→download+pdftotext (_read_local_text_for_analysis). Không rõ định dạng → thử
    export rồi sniff binary. Đọc được → ghi cache extract_<id>.txt (chung khoá với extract/cache-build —
    lần sau khỏi export). Trả (text, source) với source ∈ {cache,gdoc,gdoc-docx,docx,pdf}; fail mọi
    đường → ("", "").

    r183 (bẫy IM LẶNG đo 23-07-2026): nhánh gdoc đi export text/plain — ĐÁNH RƠI mọi dấu vết sửa đổi ⇒
    `--markup` thành no-op mà vẫn rc=0 (đo: cả 3 chế độ 25.339 ký tự = BẢN THÔ, trong khi .docx gốc
    strip=21.131 ⇒ 4.405 ký tự chữ ĐÃ BỎ đọc thành quy phạm hiện hành, sinh 6 phát hiện SAI). Nay:
    (a) gdoc + strip/mark → EXPORT .docx rồi lọc qua docx_markup như nhánh .docx; (b) không lấy được
    markup (export fail / bản convert đã mất dấu vết / cache cũ không chứng nhận) → CẢNH BÁO TƯỜNG MINH
    ra stderr + khai vào `meta`, KHÔNG bao giờ trả kết quả im lặng như thể đã lọc.
    `meta` (dict, tuỳ chọn) nhận: markup_mode · markup_filter_ran · markup_found · markup_warning."""
    fid = str(file_id or "").strip()
    _mode = (markup or "strip").strip().lower()
    _meta = meta if isinstance(meta, dict) else {}
    _meta.update({"markup_mode": _mode, "markup_filter_ran": False, "markup_found": False,
                  "markup_warning": "", "khoi_dau_missing": False})

    def _mk_warn(why: str) -> None:
        _markup_warn(fid, _mode, why, _meta)      # r186: helper DÙNG CHUNG với cmd_extract

    def _kd_gate(t: str, source: str) -> None:
        """r215: mọi đường trả text đều đi qua đây — thiếu khối đầu thì NÓI RA, không phục vụ im lặng."""
        if not _text_thieu_khoi_dau(t):
            return
        _meta["khoi_dau_missing"] = True
        print(f"[tl] ⚠ [khoi-dau] text (nguồn: {source}) BẮT ĐẦU THẲNG từ thân văn bản — không có khối "
              f"đầu (số hiệu/ngày ban hành/cơ quan/căn cứ). KHÔNG dùng bản này để xác định danh tính "
              f"văn bản (`_classify_doc_header` sẽ đi nhặt số hiệu trong THÂN). Lấy bản đủ: "
              f"`tl doc-text {fid} --markup mark`, hoặc dựng lại cache bằng `tl cache-build`.",
              file=sys.stderr)

    if not fid:
        return "", ""
    # r182: chỉ chế độ CHUẨN (strip) mới được dùng/ghi cache — mark/raw là bản ĐỌC-XEM của người rà,
    # để lọt vào extract_<id>.txt sẽ bơm ⟦BỎ:…⟧ (hoặc chữ đã bỏ) vào corpus.
    _mk_canon = _mode == "strip"
    if not refresh and _mk_canon:
        try:
            _cf = _cache_file(f"extract_{fid}.txt")
            if _cf.exists():
                _ct = _cf.read_text(encoding="utf-8", errors="replace")
                if _ct.strip():
                    # r183: cache do đường export text/plain (cmd_extract TRƯỚC r186, hoặc doc-text
                    # TRƯỚC r183) ghi KHÔNG hề qua docx_markup. Không có sidecar ⇒ coi như CHƯA lọc.
                    _cert = _markup_cert_read(fid)
                    if _cert.get("filter_ran"):
                        _meta["markup_filter_ran"] = True
                        _meta["markup_found"] = bool(_cert.get("found"))
                    else:
                        _mk_warn("text lấy từ CACHE `extract_<id>.txt` KHÔNG kèm chứng nhận đã-lọc "
                                 "(cache cũ, hoặc do `tl extract` ghi từ export text/plain) — đọc lại "
                                 "bằng `--refresh`")
                    # r266 (v1.36.4 — đo drift 30-07): cache đọc ra phải qua ĐÚNG bộ lọc U1 như
                    # `_read_doc_text` đọc CÙNG tệp — không thì hai reader lệch byte, và control-char
                    # (\x0c pdftotext để lại trong cache cũ) chui vào JSON `text`/`--out` của doc-text.
                    _ct = _sanitize_export_text(_strip_font_runs(_ct))
                    _kd_gate(_ct, "cache")   # r215: đúng đường đã phục vụ ND 158 thiếu khối đầu
                    return _ct, "cache"
        except Exception:  # noqa: BLE001
            pass
    e = entry
    if e is None:
        try:
            e = next((x for x in _manifest_entries(refresh=False)
                      if str(x.get("drive_id") or x.get("gdoc_id") or "") == fid), None)
        except Exception:  # noqa: BLE001 — chưa boot/manifest → sniff mù vẫn chạy
            e = None
    mime = str((e or {}).get("mime") or "").lower()
    name = str((e or {}).get("name") or "").lower()
    if "google-apps" in mime:
        kind = "gdoc"
    elif "wordprocessingml" in mime or name.endswith(".docx"):
        kind = "docx"
    elif "pdf" in mime or name.endswith(".pdf"):
        kind = "pdf"
    else:
        kind = ""
    text, src = "", ""
    # r183 (a): Google Doc + chế độ LỌC → đi qua bản EXPORT .docx, là đường DUY NHẤT còn giữ được
    # w:strike/w:ins/w:del. Ưu tiên TRƯỚC export text/plain (vốn san phẳng hết ⇒ no-op im lặng).
    if kind == "gdoc" and _mode != "raw":
        _tg, _stg = _gdoc_docx_text(fid, _mode)
        if _tg:
            text, src = _tg, "gdoc-docx"
            _meta["markup_filter_ran"] = True
            _meta["markup_found"] = bool(_stg and any(_stg.values()))
            if not _meta["markup_found"]:
                _mk_warn("bản .docx export từ Google Doc KHÔNG mang dấu vết sửa đổi nào "
                         "(del=0, strike=0, ins=0) — không có gì để lọc")
    if not text and kind in ("gdoc", ""):
        # live-smoke 2026-07-16 bắt: máy lazy-creds → GAS trong _read_doc_text RAISE 'Thiếu TL_WEBAPP/
        # TL_TOKEN' — KHÔNG được xuyên thủng; nuốt để còn thử đường binary (gws cred direct không cần token).
        try:
            t = _read_doc_text(fid, config, use_cache=_mk_canon)
        except (SystemExit, Exception):  # noqa: BLE001
            t = ""
        if t and not _text_looks_binary(t):
            text, src = t, "gdoc"
            # r183 (b): đây là text/plain — docx_markup KHÔNG chạy được trên nó. Im lặng là hành vi cấm.
            _mk_warn("chỉ đọc được qua export text/plain (export .docx không dùng được) — định dạng "
                     "gạch-bỏ đã bị san phẳng nên bộ lọc markup KHÔNG chạy trên nguồn này")
    if not text and kind in ("docx", "pdf", ""):
        p = _doc_text_fetch_binary(fid, suffix={"docx": ".docx", "pdf": ".pdf"}.get(kind, ".bin"))
        if p is not None:
            try:
                with open(p, "rb") as _fh:
                    head = _fh.read(8)
                if kind == "docx" or (kind == "" and head.startswith(b"PK\x03\x04")):
                    t = _docx_unzip_text(p, _mode)
                    if t:
                        text, src = t, "docx"
                        _meta["markup_filter_ran"] = _mode != "raw"
                        try:   # r183: khai số đếm thật để caller/JSON nói được ĐÃ lọc cái gì
                            _dm2 = _imp("docx_markup")
                            _st2 = _dm2.scan_file(p)
                            # r316: TÁCH «không đọc được» khỏi «đọc được và có markup». Trước đây
                            # `any(...)` trên dict rỗng ⇒ markup_found=False, tức docx hỏng được
                            # khai là SẠCH. Nay khai riêng, và markup_found để True (fail-CLOSED:
                            # chưa-biết KHÔNG được lặng lẽ thành đã-sạch cho một tín hiệu pháp lý).
                            if _st2.get(_dm2.UNREADABLE):
                                _meta["markup_unreadable"] = True
                                _meta["markup_found"] = True
                            else:
                                _meta["markup_found"] = any(_st2.values())
                        except Exception:  # noqa: BLE001
                            pass
                elif kind == "pdf" or (kind == "" and head.startswith(b"%PDF")):
                    t, _w = _read_local_text_for_analysis(Path(p))
                    if t:
                        text, src = t, "pdf"
            except Exception:  # noqa: BLE001
                pass
            finally:
                try:
                    os.unlink(p)
                    os.rmdir(Path(p).parent)
                except Exception:  # noqa: BLE001 — temp OS tự dọn
                    pass
    if not text:
        return "", ""
    text = _sanitize_export_text(_strip_font_runs(text))   # r266: U1 áp MỌI nguồn (pdf/docx từng lọt \x0c)
    if _mk_canon:
        try:
            _cf = _cache_file(f"extract_{fid}.txt")
            _cf.parent.mkdir(parents=True, exist_ok=True)
            _cf.write_text(text, encoding="utf-8")
        except Exception:  # noqa: BLE001 — cache best-effort, không chặn kết quả
            pass
        # r183: SIDECAR chứng nhận — lần đọc cache sau biết text này ĐÃ qua docx_markup hay chưa.
        _markup_cert_write(fid, filter_ran=bool(_meta.get("markup_filter_ran")),
                           found=bool(_meta.get("markup_found")), source=src)
    _kd_gate(text, src)
    return text, src


def cmd_doc_text(a) -> int:
    """A1 (v1.34.60): `tl doc-text <fileId>` — MỘT lệnh đọc text mọi định dạng (GDoc/.docx/.pdf), cache
    extract_<id>.txt; --dieu cắt Điều; --out né tràn stdout; --refresh bỏ cache. Nền cho E1 corpus-fallback."""
    # OFFLINE-FIRST (bug máy-phụ-thuộc CI bắt 2026-07-16): gốc rễ THẬT là doc-text thiếu trong
    # _CREDS_LAZY_CMDS (tl.py) → main() load_creds sys.exit TRƯỚC handler — đã thêm allowlist.
    # Guard dưới là LƯỚI PHỤ defense-in-depth: mọi lỗi áp profile (config hỏng/SystemExit lạc) không
    # được chặn đường đọc CACHE vốn không cần creds; export/download phía sau tự fail sạch.
    try:
        apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    except (SystemExit, Exception):  # noqa: BLE001
        pass
    try:   # lazy-creds: có config thì nạp token cho đường GAS export; không config → cache/gws-cred vẫn chạy
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (SystemExit, Exception):  # noqa: BLE001
        pass
    fid = str(getattr(a, "file_id", "") or "").strip()
    _meta = {}
    text, src = _doc_text_any(fid, refresh=getattr(a, "refresh", False),
                              markup=str(getattr(a, "markup", "strip") or "strip"), meta=_meta)
    # r183: --markup-strict = KHÔNG chứng minh được đã lọc thì KHÔNG trả văn bản. Thà thiếu văn bản còn
    # hơn có văn bản mà người đọc tưởng đã loại chữ đã bỏ (bẫy 23-07: 6 phát hiện SAI từ bản thô).
    if _meta.get("markup_warning") and getattr(a, "markup_strict", False):
        print(json.dumps({"ok": False, "error": "MARKUP_UNVERIFIED", "file_id": fid, "source": src,
                          "markup_mode": _meta.get("markup_mode"),
                          "note": _meta.get("markup_warning")}, ensure_ascii=False), file=sys.stderr)
        return 3
    if not text:
        print(json.dumps({"ok": False, "error": "DOC_TEXT_UNAVAILABLE", "file_id": fid,
                          "note": "Không đọc được text (cache/GDoc-export/docx-unzip/pdftotext đều fail) — "
                                  "kiểm fileId/quyền, hoặc `tl download <id>` soi tay."},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    body = _slice_dieu(text, a.dieu) if getattr(a, "dieu", None) else text
    _mx = int(getattr(a, "max", 0) or 0)
    if getattr(a, "out", None):
        Path(a.out).write_text(body, encoding="utf-8")
        print(f"[tl] doc-text → {a.out} ({len(body)} ký tự, via {src})")
        return 0
    _cut = bool(_mx and len(body) > _mx)
    if getattr(a, "json", False):
        print(_json_dumps({"ok": True, "schema": "doc_text.v1", "file_id": fid, "source": src,
                           "chars": len(body), "dieu": getattr(a, "dieu", None) or None,
                           "truncated": _cut,
                           "markup_mode": _meta.get("markup_mode"),
                           "markup_filter_ran": bool(_meta.get("markup_filter_ran")),
                           "markup_found": bool(_meta.get("markup_found")),
                           "markup_warning": _meta.get("markup_warning") or None,
                           "khoi_dau_missing": bool(_meta.get("khoi_dau_missing")),   # r215
                           "text": body[:_mx] if _mx else body},
                          deterministic=_deterministic_enabled(a)))
        return 0
    print(body[:_mx] if _mx else body)
    # r183: cắt mà không báo ⇒ hai chế độ markup đều bị cắt về CÙNG số ký tự và trông y hệt nhau —
    # đúng cái đã suýt làm chẩn sai hôm 23-07 khi so độ dài strip vs raw.
    if _cut:
        print(f"[tl] ⚠ ĐẦU RA BỊ CẮT: in {_mx}/{len(body)} ký tự (--max {_mx}). So sánh độ dài/nội dung "
              f"giữa các chế độ trên bản bị cắt là VÔ NGHĨA — dùng `--max 0 --out <file>` để lấy toàn văn.",
              file=sys.stderr)
    return 0


def _cluster_lookup(q: str) -> dict:
    """E2: 'pháp luật về X' / tên lĩnh vực → {sohieu canonical, cluster, base}. Khớp token chứa nhau."""
    qn = _strip_accents(q or "").lower()
    qn = re.sub(r"\b(phap luat ve|phap luat|bo luat|luat)\b", " ", qn)
    qn = re.sub(r"\s+", " ", qn).strip()
    hits, seen = [], set()
    def _add(subject, sh, c, cname):
        key = (cname, sh)
        if sh and key not in seen:
            seen.add(key)
            hits.append({"subject": subject, "sohieu": sh, "cluster": cname,
                         "base": c.get("base"), "base_name": c.get("base_name")})
    for cname, c in (_load_subject_clusters().get("clusters") or {}).items():
        # B7: khớp TÊN CỤM / base_name → trả BASE (canonical VBHN). Vd "lao động" → lao_dong_xa_hoi → 18/VBHN-VPQH.
        cn = _strip_accents(cname.replace("_", " ")).lower()
        bn = _strip_accents(c.get("base_name") or "").lower()
        if qn and (qn in cn or cn in qn or (bn and (qn in bn or bn in qn))):
            _add(c.get("base_name") or cname, c.get("base"), c, cname)
        for subj, sh in (c.get("members") or {}).items():
            sjn = _strip_accents(subj).lower()
            if sjn and qn and (sjn in qn or qn in sjn):
                _add(subj, sh, c, cname)
    return {"query": q, "matches": hits}

def _cluster_for_base(base_sh: str):
    bn = norm_sohieu(base_sh or "").replace("/", "-")
    if not bn:
        return None, None
    clusters = (_load_subject_clusters().get("clusters") or {})
    # r255 (P15 — repro: `_cluster_for_base("18-2025-VBHN-VPQH") -> None` trong khi "18/VBHN-VPQH" -> cụm):
    # subject_clusters.json ghi 11/11 số VBHN KHÔNG NĂM, còn số hiệu người rà lấy từ locate/reg-query LÀ
    # dạng có năm (bất biến PHẢI-CÓ-NĂM) ⇒ KHOÁ CANONICAL chính là khoá THẤT BẠI, cụm=∅ + BASE_NO_CLUSTER
    # dù cụm có thật. Nới ĐÚNG 1 CHIỀU của _sohieu_query_hits_entry, gọi với GIÁ TRỊ CỤM Ở VAI "query"
    # (cụm là bên THIẾU năm) — chiều ngược helper cố ý không nới. Đây là KHỚP TRUY VẤN trên tệp cụm tay,
    # KHÔNG phải khoá canonical/registry (doctrine _vbhn_bare_key). KHÔNG sửa dữ liệu subject_clusters.json:
    # đổi sang dạng có năm là đổi dữ liệu, kéo theo _cluster_lookup + golden, ngoài phạm vi bản vá này.
    def _ckey_hits(x) -> bool:
        xk = norm_sohieu(x or "").replace("/", "-")
        return bool(xk) and (xk == bn or _sohieu_query_hits_entry(xk, bn))
    for cname, c in clusters.items():
        keys = [c.get("base", "")] + list(c.get("base_aliases") or [])   # khớp cả Luật GỐC (vd 45/2019→cụm BLLĐ)
        if any(_ckey_hits(x) for x in keys):
            return cname, c
    # A4: reverse-map qua THÀNH VIÊN cụm — input là số hiệu VBHN/thành viên (vd 19/VBHN-VPQH) cũng tìm ra cụm
    # (trước đây chỉ khớp base=Luật gốc → truyền số hiệu VBHN vào rasoat-chongcheo trả cụm=∅ dù cluster-theo-tên đúng).
    for cname, c in clusters.items():
        for sh in (c.get("members") or {}).values():
            if _ckey_hits(sh):                       # r251: cùng phép nới cho reverse-map qua THÀNH VIÊN cụm
                return cname, c
    return None, None

def _resolve_cluster_member(sh: str, subj: str, entries: list[dict]) -> dict:
    """Resolve số hiệu thành viên cụm → entry CỤ THỂ. Khi số hiệu TRÙNG (vd 14/VBHN-VPQH dùng cho CẢ ATVSLĐ
    lẫn NLĐ-đi-nước-ngoài): ưu tiên TÊN khớp chủ đề (subj) > còn-hiệu-lực > là VBHN > năm mới. GIỮ VBHN-first
    (chọn ĐÚNG bản hợp nhất của chủ đề, không tụt về Luật gốc)."""
    k = norm_sohieu(sh)
    # r255 (P15 — repro F1a: corpus có '19-2025-VBHN-VPQH' mà thành viên cụm '19/VBHN-VPQH' trả in_corpus=False):
    # so qua cổng bare-VBHN v1.33.47 + dùng _sohieu_key_entry (bắt cả entry sohieu RỖNG, số nằm trong TÊN).
    # GIỮ vế so thô. Hệ quả cố ý: `cands` rộng hơn ⇒ `ambiguous` có thể bật thêm — đúng nghĩa "số hiệu trỏ
    # ≥2 văn bản khác nhau", thà báo trùng-số-hiệu còn hơn báo THIẾU oan (lớp lỗi v1.33.47).
    _khop_so_hieu = [e for e in entries
                     if _sohieu_query_hits_entry(k, _sohieu_key_entry(e)) or norm_sohieu(_entry_sohieu(e)) == k]
    # r295/T1-c (RAS-13): khớp SỐ HIỆU chưa phải "có trong corpus". Lọc tiếp qua corpus-hiệu-lực — cùng
    # predicate với `_in_corpus` của `rasoat-chongcheo` để hai đường không trôi khỏi nhau (trước đây chỉ
    # nhánh `ambiguous` bên dưới biết tới quarantine, còn `in_corpus` thì không).
    cands = [e for e in _khop_so_hieu if _rasoat_corpus_hieu_luc(e)]
    if not cands:
        # NÓI RA khi có bản mang đúng số hiệu nhưng NGOÀI corpus-hiệu-lực — im lặng ở đây thì người đọc
        # tưởng kho chưa từng có văn bản này và đi tải lại bản đã cố ý hạ/cách ly.
        _ngoai = [{"name": _entry_name(e), "cat": _entry_cat(e), "corpus": str(e.get("corpus") or ""),
                   "row_kind": _entry_row_kind(e)} for e in _khop_so_hieu]
        return {"in_corpus": False, "ambiguous": False,
                **({"khop_so_hieu_ngoai_corpus": _ngoai} if _ngoai else {})}

    def _alive(e) -> int:
        hl = _strip_accents(str(e.get("hieuluc") or e.get("hieu_luc") or "")).lower()
        return 1 if ("hieu luc" in hl and "het" not in hl and "khong" not in hl) else 0

    def _yr(e) -> int:
        ys = [int(y) for y in _entry_years(e) if str(y).isdigit()]
        return max(ys) if ys else (_sohieu_year(_entry_sohieu(e)) or 0)

    subj_toks = _token_set(_strip_accents(subj or "").lower())
    best = max(cands, key=lambda e: (len(subj_toks & _token_set(_strip_accents(_entry_name(e)).lower())),
                                     _alive(e), 1 if _is_vbhn_entry(e) else 0, _yr(e)))
    # ambiguous CHỈ khi số hiệu trỏ ≥2 VĂN BẢN KHÁC NHAU thật (name-key khác nhau) — KHÔNG tính bản quarantine
    # hay bản trùng-lặp cùng tên (vd canonical + bản NLM/Drive cùng văn bản). Tránh nhãn nhiễu cho mọi thành viên.
    # r295/T1-c: `cands` nay ĐÃ qua `_rasoat_corpus_hieu_luc` (bao trùm cả vế quarantine ở đây), nên phép
    # lọc này thành thừa — GIỮ NGUYÊN có chủ đích làm chốt chặn tại chỗ: nếu ai đó nới `cands` trở lại thì
    # ý "không tính bản quarantine" của nhãn `ambiguous` vẫn còn hiệu lực, không im lặng mất theo.
    live = [e for e in cands if not _is_quarantine_cat(_entry_cat(e))] or cands
    distinct = {_name_key(_entry_name(e)) for e in live}
    return {"in_corpus": True, "name": _entry_name(best), "drive_id": _entry_drive_id(best),
            "hieuluc": best.get("hieuluc") or best.get("hieu_luc") or "",
            "ambiguous": len(distinct) > 1, "n_candidates": len(cands)}

def _omnibus_cross_domain_note(amending_sh: str, base_subject: str, entries: list[dict]) -> str | None:
    """#11: luật SỬA (amending_sh) có trong corpus nhưng TÊN/chủ đề khác hẳn base → nhiều khả năng là LUẬT SỬA-NHIỀU-LUẬT
    (omnibus, vd 84/2025 Luật Thanh tra sửa cả Luật BHXH). Trả note cảnh báo để KHÔNG hiểu nhầm là lỗi tên/đối chiếu;
    PHẢI đọc nguyên văn điều khoản sửa. None nếu cùng chủ đề (sửa-trong-lĩnh-vực bình thường) hoặc không có trong corpus."""
    if not amending_sh or not base_subject:
        return None
    k = norm_sohieu(amending_sh).replace("/", "-")
    hits = [e for e in entries if _sohieu_key_entry(e) == k]
    if not hits:
        return None                       # chưa có trong corpus → đã có cảnh báo khác (missing/QT-5)
    e = hits[0]
    # B3 (false-positive): CHỈ kết luận omnibus khi luật sửa CÓ chủ đề RÕ và KHÁC base. Tên số TRƠ
    # ("51_2024_QH15_505750", "46_2014_QH13_238506") → _subject_tokens RỖNG → sscore 0 KHÔNG phải vì khác lĩnh vực
    # mà vì THIẾU metadata → ĐỪNG gắn omnibus (51/2024, 46/2014 thực ra là luật sửa BHYT chuyên đề).
    e_subj_tokens = _subject_tokens(_entry_subject_text(e))
    if len(e_subj_tokens) < 2:
        return None                            # chủ đề luật sửa KHÔNG RÕ → không kết luận cross-domain
    if _subject_score(e, base_subject) < 30:   # CÓ chủ đề rõ NHƯNG khác lĩnh vực base → omnibus thật
        return (f"OMNIBUS_CROSS_DOMAIN: luật sửa {amending_sh} trong corpus = '{_entry_name(e)[:48]}' — TÊN CHÍNH khác "
                f"lĩnh vực base; nhiều khả năng là LUẬT SỬA-NHIỀU-LUẬT (sửa base trong số nhiều luật). ĐỪNG coi là lỗi "
                f"tên/đối chiếu; ĐỌC NGUYÊN VĂN điều khoản sửa để xác nhận quan hệ.")
    return None

def _resolve_base_gdoc(base: str, entries: list[dict]):
    """Resolve `base` (số hiệu|tên) → (entry canonical VBHN-first, gdoc_id, subject_text). Cho auto-footnote: đọc
    nguyên văn VBHN base để chạy footnote-map mà KHÔNG cần truyền --target tay. (entry, gid, subject) hoặc (None,'','')."""
    if not base:
        return None, "", ""
    item = _source_map_one(base, entries)
    can = None
    pool_ids = [c.get("drive_id") for c in [item.get("canonical")] if c]
    if pool_ids and pool_ids[0]:
        can = next((e for e in entries if _entry_drive_id(e) == pool_ids[0]), None)
    if can is None:                       # fallback: khớp số hiệu trực tiếp, ưu tiên VBHN
        k = norm_sohieu(base).replace("/", "-")
        cands = [e for e in entries if _sohieu_key_entry(e) == k]
        cands.sort(key=_entry_score, reverse=True)
        can = cands[0] if cands else None
    # C (log rà #70): entry có sohieu RỖNG nhưng corpus=true + có drive_id → fallback khớp trực tiếp theo
    # tên/drive_id (thay vì 404/File-not-found). Đọc sâu vẫn chạy được dù registry chưa backfill số hiệu.
    if can is None:
        for e in entries:
            if _entry_corpus_true(e) and _entry_drive_id(e) and base in (_entry_name(e), _entry_sohieu(e), _entry_drive_id(e)):
                can = e
                break
    if can is None:
        return None, "", ""
    return can, (_entry_drive_id(can) or ""), _entry_name(can)


# ══════════════ r213 (v1.35.49) — ĐỢT 5: hai lỗ hổng lượt rà LIVE 26-07 phơi ra ══════════════
# Cả hai là MẮT XÍCH BẮT BUỘC của lớp điều phối mà KHÔNG cổng máy nào phủ (sổ lỗi H7/H8 26-07):
#  (a) STATE_DRIVE_KHONG_CO_DUONG_GHI — WRITE_PATHS_v1 bắt state ở Drive `_meta/rasoat_state.json`
#      làm nguồn sự thật resume, nhưng gói LIVE KHÔNG có lệnh nào ghi một JSON tuỳ ý vào `_meta/`.
#      ĐO LẠI: mặt ghi ĐÃ CÓ và đang chạy THẬT trong sản xuất (_create_profile_manifest_json,
#      profile-index) = g.post("upload", mime=application/json, folderId=_meta, convert/register/
#      share="false", force="true") rồi MỚI dọn bản cũ. Thiếu là thiếu LỆNH, KHÔNG thiếu năng lực
#      ⇒ KHÔNG đổi GAS, KHÔNG thêm action `files_put`, và KHÔNG mượn cổng `profile-file-add
#      --apply` (mượn cổng đó = bắt người duyệt MỖI lần chốt state — đúng thứ phá nghiệm thu ≤2
#      lần xen của H7).
#  (b) THIEU_BUOC_GOP_MASTER_UNIT_SANG_BANG_MASTER — PHA 4 SẬP: khuôn §6 `master/<unit>.json` và
#      khuôn bảng master mà `rasoat_phuluc.py` đọc KHỚP ở tầng item (cùng 10 trường + anchor) nhưng
#      LỆCH ở tầng container (§6: `van_ban` là CHUỖI + phát hiện dưới `phat_hien`; bảng: `van_ban`
#      là DANH SÁCH metadata + `noi_dung` phẳng). Đợt 1–3 không định nghĩa bước "dồn" ⇒ định nghĩa
#      ở đây, MỘT nguồn chân lý dùng chung cho cả `tl rasoat-merge` lẫn `rasoat_phuluc.py`.

# I11: HẰNG re-export trực tiếp sang tl.py (hàm rebase đọc globals tl).
_RASOAT_STATE_ALLOWED = ("rasoat_state.json", "rasoat_approvals.json")
_RASOAT_BANG_SCHEMA = "mau_bang_tong_hop_phat_hien.v1"
# Ô metadata Phụ lục 03 KHÔNG suy được từ khuôn §6 — để RỖNG và báo lên, TUYỆT ĐỐI không bịa.
_RASOAT_VB_META_FIELDS = ("linh_vuc", "loai", "so_hieu", "ngay", "ten",
                          "hieu_luc_tu", "tinh_trang", "sua_doi_bo_sung", "ghi_chu")


def _rasoat_state_scope(name):
    """PURE (r213/a): CHỐT CHẶN phạm vi đường ghi state. Chỉ cho ghi ĐÚNG tên trong WRITE_PATHS_v1,
    và chỉ dạng basename (không đường dẫn) — để `state-put` không bao giờ thành cổng ghi Drive tổng
    quát. Trả (ok, ly_do).

    FAIL-CLOSED theo bài học r212 (guard ADR-0001 fail-open sống sót nhiều bản vì test đi qua bind):
    rỗng/None/có path/không thuộc danh sách ⇒ TỪ CHỐI. Không có nhánh "nghi ngờ thì cho qua"."""
    n = str(name or "").strip()
    if not n:
        return False, "STATE_NAME_EMPTY"
    if ("/" in n) or ("\\" in n) or n.startswith(".") or n != os.path.basename(n):
        return False, "STATE_NAME_HAS_PATH:" + n
    if n not in _RASOAT_STATE_ALLOWED:
        return False, "STATE_NAME_NOT_ALLOWED:" + n
    return True, "ok"


def _rasoat_sohieu_key(s):
    """PURE (r213/b): khoá so trùng số hiệu cho bảng master. TỰ CHỨA — import CỤC BỘ, không mượn
    helper nào sống nhờ globals của tl.

    Bẫy đã trả giá ngay khi viết r213: bản đầu dùng `_norm_compare_text`, chạy tốt qua `tl` (đã
    bind) nhưng NameError `unicodedata` khi `rasoat_phuluc.py` gọi thẳng — chính khuôn false-green
    "test qua bind không chứng minh đường sản xuất". Nhóm hàm _rasoat_* PHẢI chạy được ở CẢ HAI
    đường: trong tl (đã rebase globals) và import trần từ script con."""
    import re as _re
    import unicodedata as _ud
    return _re.sub(r"\s+", " ", _ud.normalize("NFC", str(s or "")).strip().upper()).replace("/", "-")


def _rasoat_la_ban_sao(name):
    """PURE (r216 — đo được 27-07 lượt rà 7): tên file có phải BẢN SAO LƯU không.

    `rasoat-merge --in <thư mục>` quét MỌI `*.json`, kể cả bản sao lưu. Một bản sao đặt nhầm trong
    `master/` đã làm bảng master phồng 40 → 53 phát hiện với 13 mã VD TRÙNG NHAU và HAI nguồn cùng
    `unit_id`, mà `_bo_qua` vẫn rỗng và rc=0 — phụ lục sinh ra từ đó đếm một phát hiện HAI lần.

    CỐ Ý HẸP: chỉ nhận khi tên có THÀNH PHẦN (ngăn bằng dấu chấm, KHÔNG tính thành phần ĐẦU) bắt
    đầu bằng `bak` hoặc `backup` — bắt `unit-003.bak.<gì đó>.json` và `unit-003.backup.json`.
    KHÔNG đoán theo `old`/`copy`/`cu`, và KHÔNG xét thành phần đầu (nên `bakery-2025.json` vẫn là
    phiếu thật). Đoán rộng ở đây là nuốt mất phiếu rà thật — đắt hơn hẳn cái nó phòng. Bản sao bị
    bỏ qua PHẢI được KHAI BÁO (`bo_qua_ban_sao`), không im lặng: bỏ qua im lặng chỉ là bẫy khác.

    ★Hai tiền tố phải viết TÁCH: `backup` KHÔNG bắt đầu bằng `bak` (b-a-c ≠ b-a-k) — bản đầu r216
    gộp làm một và test đỏ ngay, giữ ghi chú này để không ai "rút gọn" lại."""
    stem = str(name or "").strip()
    if stem.lower().endswith(".json"):
        stem = stem[:-5]
    return any(part.lower().startswith(("bak", "backup")) for part in stem.split(".")[1:])


def _rasoat_trung_lap(docs):
    """PURE (r216): bắt TRÙNG giữa các nguồn trước khi ghi đè bảng master. Trả dict
    {"key": [...], "unit_id": [...]}, mỗi mục nêu rõ giá trị trùng và các nguồn mang nó.

    Hai loại trùng, cùng một hậu quả — đếm hai lần mà không ai biết:
      · trùng `key` trong `noi_dung`  → một phát hiện vào phụ lục hai lần;
      · trùng `unit_id` giữa các file → hai phiếu cùng mô tả một đơn vị rà.
    Bên gọi FAIL-CLOSED: có trùng thì KHÔNG ghi, rc=2. Bảng master sai mà vẫn ghi đè thì lần chạy
    sau không còn bản đúng để đối chiếu."""
    keys, uids = {}, {}
    for ten, d in (docs or []):
        if not isinstance(d, dict):
            continue
        uid = str(d.get("unit_id") or "").strip()
        if uid:
            uids.setdefault(uid, []).append(ten)
        for x in ((d.get("phat_hien") or []) + (d.get("noi_dung") or [])):
            if isinstance(x, dict) and str(x.get("key") or "").strip():
                keys.setdefault(str(x["key"]).strip(), []).append(ten)
    return {"key": [{"gia_tri": k, "nguon": v} for k, v in keys.items() if len(v) > 1],
            "unit_id": [{"gia_tri": k, "nguon": v} for k, v in uids.items() if len(v) > 1]}


def _rasoat_check_lech(cu, moi):
    """PURE (r216): đối chiếu bảng master ĐANG CÓ với kết quả merge — cho chế độ `--check`.

    Chỉ so phần NỘI DUNG (`van_ban` theo số hiệu, `noi_dung` theo `key`); CỐ Ý bỏ qua `_nguon`/
    `_thieu_o_metadata`/`_bo_qua` vì chúng mang tên file nguồn, đổi theo chỗ chạy chứ không phải
    theo dữ liệu. Trả danh sách lệch, rỗng = trùng khớp."""
    lech = []
    a_nd = {str(x.get("key") or ""): x for x in (cu.get("noi_dung") or []) if isinstance(x, dict)}
    b_nd = {str(x.get("key") or ""): x for x in (moi.get("noi_dung") or []) if isinstance(x, dict)}
    for k in sorted(set(a_nd) - set(b_nd)):
        lech.append({"loai": "CHI_CO_O_BANG_MASTER", "key": k})
    for k in sorted(set(b_nd) - set(a_nd)):
        lech.append({"loai": "CHI_CO_O_KET_QUA_MERGE", "key": k})
    for k in sorted(set(a_nd) & set(b_nd)):
        o = sorted(f for f in set(a_nd[k]) | set(b_nd[k]) if a_nd[k].get(f) != b_nd[k].get(f))
        if o:
            lech.append({"loai": "KHAC_NOI_DUNG", "key": k, "o_lech": o})
    a_vb = {_rasoat_sohieu_key(x.get("so_hieu")) for x in (cu.get("van_ban") or []) if isinstance(x, dict)}
    b_vb = {_rasoat_sohieu_key(x.get("so_hieu")) for x in (moi.get("van_ban") or []) if isinstance(x, dict)}
    for s in sorted(a_vb - b_vb):
        lech.append({"loai": "VAN_BAN_CHI_CO_O_BANG_MASTER", "so_hieu": s})
    for s in sorted(b_vb - a_vb):
        lech.append({"loai": "VAN_BAN_CHI_CO_O_KET_QUA_MERGE", "so_hieu": s})
    return lech


def _rasoat_vong_doi_enums():
    """PURE (r300): từ vựng đóng của vòng đời hồ sơ — `RASOAT_PLAN_SCHEMA.md` §3/§7.

    CỐ Ý là HÀM chứ không phải hằng cấp module: `tl.py` bind COPY-globals (ADR-0002) và stub farm
    chỉ nhận callable — hằng module tham chiếu từ trong hàm sẽ KHÔNG resolve qua `tl` (r90/r81 bắt)."""
    return {"vong_doi": ("dang_ra", "tam_ngung", "da_dong", "da_dong_co_gioi_han"),
            "q_verify": ("cho_tra_no", "dat", "khong_dat", "no_treo"),
            "q_ingest": ("cho_tai", "cho_nguoi_tai", "dry_planned", "staged", "flipped",
                         "out_of_scope", "da_quyet", "da_quyet_va_thi_hanh")}


def _rasoat_vong_doi_findings(state):
    """PURE (r300): 6 điều kiện ĐÓNG HỒ SƠ — `references/RASOAT_PLAN_SCHEMA.md` §7.1.

    Vì sao là hàm chứ không phải prose: đo 01-08 trên hồ sơ thật `h7-3nd-bhxh-2025`, người thẩm tra
    chốt "đã đóng" mà state KHÔNG có khoá nào nói thế, còn treo 5 đầu mối (claim chưa nhả · 1 duyệt
    `cho_duyet` · 3 nợ kiểm chéo · 5 văn bản chưa lấy được · 7 trạng thái đã trôi thành câu văn xuôi).
    Prose không chặn được chuyện đó; hàm này chặn.

    Trả `{ve_hong: [...], du_dieu_kien: bool}` — `du_dieu_kien=True` ⇒ được đặt `da_dong`; False ⇒ CHỈ
    được `da_dong_co_gioi_han` **và** mỗi vế hỏng phải có mục trong `vong_doi.gioi_han_da_biet`
    (kiểm ở `_rasoat_vong_doi_dong_hop_le`). Hàm KHÔNG đọc đĩa, KHÔNG gọi mạng."""
    st = state if isinstance(state, dict) else {}

    def _q(k):
        return [x for x in (st.get(k) or []) if isinstance(x, dict)]

    _E = _rasoat_vong_doi_enums()
    ve = []
    if any(str(u.get("trang_thai")) in ("pending", "doing") for u in _q("q_units")):
        ve.append("q_units_con_pending_hoac_doing")
    if any(str(a.get("trang_thai")) == "cho_duyet" for a in _q("q_approvals")):
        ve.append("q_approvals_con_cho_duyet")
    qv = _q("q_verify")
    if any(str(v.get("trang_thai")) not in _E["q_verify"] for v in qv):
        ve.append("q_verify_thieu_trang_thai_enum")
    elif any(str(v.get("trang_thai")) == "cho_tra_no" for v in qv):
        ve.append("q_verify_con_cho_tra_no")
    if any(str(i.get("trang_thai")) not in _E["q_ingest"] for i in _q("q_ingest")):
        ve.append("q_ingest_trang_thai_ngoai_enum")
    elif any(str(i.get("trang_thai")) in ("cho_tai", "cho_nguoi_tai") for i in _q("q_ingest")):
        ve.append("q_ingest_con_van_ban_chua_lay_duoc")
    cl = st.get("session_claim")
    if not (cl is None or (isinstance(cl, dict) and cl.get("id") is None and cl.get("released_at"))):
        ve.append("session_claim_chua_nha")
    return {"ve_hong": ve, "du_dieu_kien": not ve}


def _rasoat_vong_doi_dong_hop_le(state):
    """PURE (r300): trạng thái `vong_doi` có KHỚP thực tế các hàng đợi không — fail-CLOSED.

    Chặn đúng ba kiểu tự lừa: (a) khai `da_dong` trong khi còn vế hỏng; (b) khai
    `da_dong_co_gioi_han` mà `gioi_han_da_biet` RỖNG (đóng im lặng — thứ đã xảy ra thật);
    (c) `trang_thai` ngoài enum."""
    st = state if isinstance(state, dict) else {}
    vd = st.get("vong_doi") if isinstance(st.get("vong_doi"), dict) else None
    if vd is None:
        return {"ok": True, "loi": [], "ghi_chu": "chưa khai vòng đời — hồ sơ đang rà"}
    loi = []
    tt = str(vd.get("trang_thai") or "")
    if tt not in _rasoat_vong_doi_enums()["vong_doi"]:
        loi.append(f"TRANG_THAI_NGOAI_ENUM:{tt}")
    f = _rasoat_vong_doi_findings(st)
    if tt == "da_dong" and not f["du_dieu_kien"]:
        loi.append("KHAI_DA_DONG_NHUNG_CON_VE_HONG:" + ",".join(f["ve_hong"]))
    if tt == "da_dong_co_gioi_han" and not (vd.get("gioi_han_da_biet") or []):
        loi.append("DA_DONG_CO_GIOI_HAN_NHUNG_GIOI_HAN_RONG")
    return {"ok": not loi, "loi": loi, "ve_hong": f["ve_hong"]}


def _rasoat_anchor_khuon():
    """PURE (r313/RAS-17): khuôn ĐÓNG của `anchor.doc_deps[]` — `RASOAT_PLAN_SCHEMA.md` §7.2.

    `text_hash` phải là HASH NỘI DUNG (`sha256:<64hex>`), KHÔNG phải địa chỉ định vị. Địa chỉ đi
    trường RIÊNG `locator` — hai thứ khác bản chất: hash đổi khi NỘI DUNG đổi (đó là điều Loop C cần
    biết), địa chỉ thì không. Nhét địa chỉ vào ô hash làm phép so «còn tươi?» luôn LỆCH ⇒ STALE giả.

    CỐ Ý là HÀM chứ không phải hằng cấp module — cùng lý do `_rasoat_vong_doi_enums`: `tl.py` bind
    COPY-globals (ADR-0002) và stub farm chỉ nhận callable; hằng module tra từ trong hàm KHÔNG resolve
    qua `tl` (r90/r81 bắt)."""
    return {"text_hash": r"^sha256:[0-9a-f]{64}$",
            # dấu hiệu ĐỊA CHỈ bị nhét vào ô hash — lấy từ chính dạng `cite` đang dùng
            # (`cache:18-2025-VBHN-VPQH#dieu54`), xem template MAU_BANG_TONG_HOP_PHAT_HIEN.json.
            "locator_dau_hieu": ("cache:", "drive:", "nlm:", "#", "/")}


def _rasoat_anchor_findings(units):
    """PURE (r313/RAS-17): phân loại TỪNG `anchor.doc_deps[]` trong các đơn vị rà.

    Vì sao cần: đo 01-08 trên hồ sơ `h7-3nd-bhxh-2025` — **82/82 `doc_deps` ĐIỀN ĐỦ, 0/82 khớp
    `sha256:<64hex>`**; ô `text_hash` đang chứa ĐỊA CHỈ ĐỊNH VỊ. «Điền đủ» nên không cổng nào kêu,
    mà Loop C chạy lên sẽ báo **STALE giả 100%** (`RASOAT_PLAN_SCHEMA.md` §7.2). Đây là lớp bệnh
    «trường có giá trị nhưng SAI LOẠI» — đếm rỗng/thiếu không bắt được, phải soi KHUÔN.

    Trả `{tong, ok, rong, locator_trong_hash, sai_khuon, co_locator, mau, san_sang}`.
    `san_sang=True` ⇔ có ít nhất 1 dep VÀ mọi dep đều `ok` — tiền đề DUY NHẤT để đặt
    `vong_doi.anchor_con_hieu_luc: true` (cưỡng chế ở `_rasoat_anchor_hop_le`).
    Hàm KHÔNG đọc đĩa, KHÔNG gọi mạng, KHÔNG sửa gì — chỉ ĐO."""
    k = _rasoat_anchor_khuon()
    rx = re.compile(k["text_hash"])
    tong = ok = rong = loc_in_hash = sai = co_loc = 0
    mau = []
    for u in (units if isinstance(units, list) else []):
        if not isinstance(u, dict):
            continue
        # nhận CẢ hai khuôn (§6 `phat_hien` lẫn bảng `noi_dung`) — cùng doctrine _rasoat_unit_shape
        rows = u.get("phat_hien") if isinstance(u.get("phat_hien"), list) else u.get("noi_dung")
        for r in (rows if isinstance(rows, list) else []):
            if not isinstance(r, dict):
                continue
            anc = r.get("anchor") if isinstance(r.get("anchor"), dict) else {}
            for dep in (anc.get("doc_deps") if isinstance(anc.get("doc_deps"), list) else []):
                tong += 1
                if not isinstance(dep, dict):
                    sai += 1
                    continue
                if str(dep.get("locator") or "").strip():
                    co_loc += 1
                th = str(dep.get("text_hash") or "").strip()
                if not th:
                    rong += 1
                    loai = "rong"
                elif rx.match(th):
                    ok += 1
                    continue
                elif any(s in th for s in k["locator_dau_hieu"]):
                    loc_in_hash += 1
                    loai = "locator_trong_hash"
                else:
                    sai += 1
                    loai = "sai_khuon"
                if len(mau) < 10:
                    mau.append({"so_hieu": str(dep.get("so_hieu") or ""), "loai": loai,
                                "text_hash": th[:80]})
    return {"tong": tong, "ok": ok, "rong": rong, "locator_trong_hash": loc_in_hash,
            "sai_khuon": sai, "co_locator": co_loc, "mau": mau,
            "san_sang": bool(tong) and ok == tong}


def _rasoat_anchor_hop_le(state, units=None):
    """PURE (r313/RAS-17): fail-CLOSED cho `vong_doi.anchor_con_hieu_luc` — `RASOAT_PLAN_SCHEMA.md` §7.2.

    TRƯỚC r313 KHÔNG mã nào cưỡng chế cờ này: nó chỉ sống trong prose + một ca selftest kiểm *tài liệu
    có nhắc chữ đó không*. Tức đúng lớp tự-lừa mà `_rasoat_vong_doi_dong_hop_le` sinh ra để chặn —
    khai `true` là Loop C chạy, không ai đối chiếu anchor có di trú thật chưa.

    Ba vế, mỗi vế chặn một kiểu:
      (a) khai `true` mà KHÔNG đưa đơn vị để kiểm ⇒ ĐỎ. Không kiểm được thì không được khai — im lặng
          tin lời khai chính là cách STALE giả lọt.
      (b) khai `true` mà anchor chưa `san_sang` ⇒ ĐỎ, kèm SỐ ĐẾM để biết còn bao xa.
      (c) khai `false` TƯỜNG MINH mà thiếu `ly_do_anchor` ⇒ ĐỎ (§7.2 «BỎ QUA hồ sơ và NÓI RA lý do»).
    Cờ VẮNG HẲN ⇒ ghi chú advisory, KHÔNG đỏ: hồ sơ đang rà chưa tới bước khai, đỏ ở đây là đỏ oan
    ngày đầu ⇒ guard sẽ bị vô hiệu hoá (bài học §0.8). Ratchet siết theo chiều khai SAI, không siết
    chiều CHƯA KHAI."""
    st = state if isinstance(state, dict) else {}
    vd = st.get("vong_doi") if isinstance(st.get("vong_doi"), dict) else None
    if vd is None:
        return {"ok": True, "loi": [], "findings": None,
                "ghi_chu": "chưa khai vòng đời — hồ sơ đang rà"}
    loi = []
    f = _rasoat_anchor_findings(units) if units is not None else None
    if vd.get("anchor_con_hieu_luc") is True:
        if f is None:
            loi.append("ANCHOR_KHAI_TRUE_NHUNG_KHONG_DUA_DON_VI_DE_KIEM")
        elif not f["san_sang"]:
            loi.append("ANCHOR_KHAI_TRUE_NHUNG_CHUA_DI_TRU:"
                       f"ok={f['ok']}/{f['tong']},locator_trong_hash={f['locator_trong_hash']},"
                       f"rong={f['rong']},sai_khuon={f['sai_khuon']}")
    elif "anchor_con_hieu_luc" in vd and not str(vd.get("ly_do_anchor") or "").strip():
        loi.append("ANCHOR_FALSE_NHUNG_THIEU_LY_DO")
    return {"ok": not loi, "loi": loi, "findings": f}


def _rasoat_anchor_quet(docs):
    """PURE (r321 — RAS-17 vế `rasoat-merge`): soi neo trên N phiếu và CHỈ ĐÍCH DANH từng ô hỏng.

    r313 đã dựng khuôn (`_rasoat_anchor_khuon`) + cưỡng chế cờ vòng đời (`_rasoat_anchor_hop_le`),
    nhưng đường mà bản kiểm lõi nêu ĐÍCH DANH — «`_rasoat_unit_shape` không chạm `anchor` ⇒
    `rasoat-merge` nuốt trọn» — vẫn chưa ai chạm. Đo trên master `c24a8b3` với hồ sơ BHXH thật
    (82/82 ô neo sai khuôn): `tl rasoat-merge` trả `ok:true`, 40 phát hiện, **không MỘT khoá nào**
    nhắc tới anchor. Cổng vòng đời không bịt được lỗ này: nó chỉ bắn khi hồ sơ đã khai `vong_doi`,
    còn merge chạy từ lượt rà đầu tiên.

    Khác `_rasoat_anchor_findings` (r313) ở MỤC ĐÍCH chứ không ở luật: hàm kia ĐẾM để phán cờ
    `anchor_con_hieu_luc`; hàm này gắn `nguon` + `key` để người sửa biết mở FILE NÀO, PHÁT HIỆN NÀO.
    Luật hợp lệ và từ vựng `loai` dùng CHUNG `_rasoat_anchor_khuon()` — một nguồn chân lý, không đẻ
    bộ từ vựng thứ hai rồi để hai bên trôi khỏi nhau.

    GIỮ THỨ TỰ đầu vào ⇒ tất định (điều kiện để golden/determinism khoá được)."""
    k = _rasoat_anchor_khuon()
    rx = re.compile(k["text_hash"])
    ra = []
    for ten, d in (docs or []):
        if not isinstance(d, dict) or _rasoat_unit_shape(d) != "unit_v1":
            continue
        for ph in (d.get("phat_hien") or []):
            if not isinstance(ph, dict):
                continue
            anc = ph.get("anchor") if isinstance(ph.get("anchor"), dict) else {}
            deps = anc.get("doc_deps") if isinstance(anc.get("doc_deps"), list) else []
            for i, dep in enumerate(deps):
                th = str(dep.get("text_hash") or "").strip() if isinstance(dep, dict) else ""
                if isinstance(dep, dict) and rx.match(th):
                    continue
                loai = ("sai_khuon" if not isinstance(dep, dict)
                        else "rong" if not th
                        else "locator_trong_hash" if any(s in th for s in k["locator_dau_hieu"])
                        else "sai_khuon")
                ra.append({"nguon": ten, "key": str(ph.get("key") or ""), "i": i,
                           "so_hieu": str(dep.get("so_hieu") or "") if isinstance(dep, dict) else "",
                           "loai": loai, "text_hash": th[:80]})
    return ra


def _rasoat_unit_shape(d):
    """PURE (r213/b): nhận diện khuôn MỘT file JSON rà soát — nguồn chân lý DUY NHẤT cho cả
    `tl rasoat-merge` lẫn `rasoat_phuluc.load_master`.

      'unit_v1' = khuôn §6 RASOAT_HOSO_LOOP (`master/<unit>.json`): phát hiện dưới `phat_hien`.
      'bang_v1' = khuôn `mau_bang_tong_hop_phat_hien.v1`: nội dung phẳng dưới `noi_dung`.
      'unknown' = KHÔNG nhận ra (kể cả khi có CẢ HAI khoá) ⇒ bên gọi phải FAIL-CLOSED, không đoán.

    Có cả `phat_hien` lẫn `noi_dung` = file lai/hỏng: trả 'unknown' chứ không tự chọn — đoán sai ở
    đây là nuốt mất phát hiện mà không ai biết."""
    if not isinstance(d, dict):
        return "unknown"
    has_ph = isinstance(d.get("phat_hien"), list)
    has_nd = isinstance(d.get("noi_dung"), list)
    if has_ph and not has_nd:
        return "unit_v1"
    if has_nd and not has_ph:
        return "bang_v1"
    return "unknown"


def _rasoat_unit_to_bang(d, nguon=""):
    """PURE (r213/b): quy đổi MỘT khuôn §6 sang mảnh khuôn bảng master.
    Trả (van_ban_rows, noi_dung_rows, thieu) — `thieu` = danh sách ô metadata Phụ lục 03 không suy
    ra được từ đơn vị rà (ngay/hieu_luc_tu/tinh_trang/loai…).

    KHÔNG BỊA: đơn vị rà chỉ biết số hiệu + tên văn bản; ngày ban hành/hiệu lực/tình trạng nằm ở
    registry, không nằm trong phiếu rà. Trường thiếu để RỖNG và ĐẨY LÊN để người điền — thà bảng
    có ô trống nhìn thấy được còn hơn ô bịa nhìn như thật. Đơn vị nào muốn đủ ô thì mang sẵn
    `van_ban_meta` (dict) — §6 chấp nhận, không bắt buộc.

    r216 — `loai_don_vi`: đơn vị ĐỐI CHIẾU / XUYÊN VĂN BẢN không phải một VBQPPL, nên KHÔNG được
    sinh dòng trong Mẫu 03-BN ("Danh mục VBQPPL thuộc đối tượng, phạm vi rà soát") — phát hiện thì
    vẫn gộp bình thường. Đo được 27-07: `unit-006` (rà khối Căn cứ ban hành của CẢ 4 nghị định) đẩy
    nhãn mô tả của chính nó vào danh mục thành "văn bản" thứ 5, tức một biểu mẫu trình Uỷ ban liệt
    kê một văn bản KHÔNG TỒN TẠI. `unit-004` thoát được CHỈ VÌ tình cờ đặt `van_ban` trùng số hiệu
    thật nên bị dedup nuốt đi — may, không phải do công cụ biết phân biệt.
    Mặc định (thiếu khoá) = giữ NGUYÊN hành vi cũ: chỉ đơn vị tự khai mới đổi cách xử lý."""
    loai = str((d or {}).get("loai_don_vi") or "").strip().lower()
    khong_sinh_dong = loai in ("doi_chieu", "xuyen_van_ban")
    sohieu = str((d or {}).get("van_ban") or "").strip()
    meta = (d or {}).get("van_ban_meta")
    row = {k: "" for k in _RASOAT_VB_META_FIELDS}
    if isinstance(meta, dict):
        for k in _RASOAT_VB_META_FIELDS:
            if meta.get(k) is not None:
                row[k] = str(meta.get(k) or "")
    row["so_hieu"] = row.get("so_hieu") or sohieu
    row["ten"] = row.get("ten") or str((d or {}).get("ten") or "")
    phat_hien = [x for x in ((d or {}).get("phat_hien") or []) if isinstance(x, dict)]
    # linh_vuc của văn bản: lấy theo lĩnh vực của phát hiện ĐẦU TIÊN (chỉ để gom nhóm bảng 03,
    # không phải kết luận phân loại) — rỗng thì để rasoat_phuluc rơi vào "(Chưa phân loại)".
    if not row.get("linh_vuc"):
        row["linh_vuc"] = next((str(x.get("linh_vuc") or "") for x in phat_hien if x.get("linh_vuc")), "")
    if khong_sinh_dong:
        # Không sinh dòng ⇒ cũng KHÔNG báo "ô metadata còn trống": đơn vị này không phải văn bản,
        # đòi nó điền ngày ban hành/hiệu lực là đòi thứ không tồn tại.
        return [], phat_hien, []
    thieu = [k for k in _RASOAT_VB_META_FIELDS if not str(row.get(k) or "").strip()]
    if thieu and nguon:
        row["ghi_chu"] = (row.get("ghi_chu") or "") + \
            ("; " if row.get("ghi_chu") else "") + "[rasoat-merge] ô trống cần điền: " + ", ".join(thieu)
    return ([row] if sohieu or row.get("ten") else []), phat_hien, thieu


def _rasoat_merge_units(docs):
    """PURE (r213/b): gộp N tài liệu (khuôn §6 và/hoặc khuôn bảng có sẵn) thành MỘT khuôn
    `mau_bang_tong_hop_phat_hien.v1` mà `rasoat_phuluc.py` đọc thẳng được.

    `docs` = [(ten_nguon, dict), …] — GIỮ THỨ TỰ đầu vào để kết quả TẤT ĐỊNH (gọi hai lần trên cùng
    tập file phải ra byte y hệt; đây là điều kiện để golden/determinism khoá được).
    Khuôn 'unknown' KHÔNG bị bỏ qua im lặng: dồn vào `bo_qua` để bên gọi rc≠0 — chính chỗ này là
    nơi lỗi cũ trốn được (`van_ban += <chuỗi>` trải CHUỖI thành từng KÝ TỰ rồi mới chết ở nơi khác).
    Dedup văn bản theo `so_hieu` (giữ bản đầu); phát hiện KHÔNG dedup ở đây — rasoat_phuluc.dedup()
    mới là chỗ dedup xuyên luật, để nguyên tắc "đếm một lần" chỉ có MỘT chỗ cài."""
    van_ban, noi_dung, nguon, thieu_o, bo_qua = [], [], [], [], []
    seen_vb = set()
    for ten, d in (docs or []):
        shape = _rasoat_unit_shape(d)
        if shape == "unit_v1":
            vbs, nds, thieu = _rasoat_unit_to_bang(d, nguon=ten)
            if thieu:
                thieu_o.append({"nguon": ten, "so_hieu": str((d or {}).get("van_ban") or ""), "o_trong": thieu})
        elif shape == "bang_v1":
            vbs = [x for x in ((d or {}).get("van_ban") or []) if isinstance(x, dict)]
            nds = [x for x in ((d or {}).get("noi_dung") or []) if isinstance(x, dict)]
        else:
            bo_qua.append({"nguon": ten, "ly_do": "KHUON_KHONG_NHAN_RA"})
            continue
        for r in vbs:
            k = _rasoat_sohieu_key(r.get("so_hieu")) if r.get("so_hieu") else ""
            if k and k in seen_vb:
                continue
            if k:
                seen_vb.add(k)
            van_ban.append(r)
        noi_dung += nds
        nguon.append({"nguon": ten, "khuon": shape, "so_van_ban": len(vbs), "so_phat_hien": len(nds)})
    co_quan = next((str(d.get("co_quan")) for _t, d in (docs or [])
                    if isinstance(d, dict) and d.get("co_quan")), "")
    return {"schema": _RASOAT_BANG_SCHEMA, "co_quan": co_quan,
            "van_ban": van_ban, "noi_dung": noi_dung,
            "_nguon": nguon, "_thieu_o_metadata": thieu_o, "_bo_qua": bo_qua}


def _rasoat_state_reconcile(state, master_unit_ids):
    """PURE (r213 — khe hở H8 ĐO ĐƯỢC 26-07): phiên kế nhiệm chết THẬT sau khi ghi
    `master/<unit>.json` nhưng TRƯỚC khi cập nhật state ⇒ state còn `doing` trong khi việc đã xong.
    Card `rasoat_hoso` chỉ có luật "đơn vị doing mồ côi trả về pending" — áp thẳng luật đó ở đây sẽ
    RÀ LẠI một đơn vị đã xong (tốn lượt, và đẻ phát hiện trùng số).

    Luật hoà giải (r213):
      doing + ĐÃ có master/<unit>.json  → done    (việc đã xong, chỉ mất bước ghi sổ)
      doing + KHÔNG có master           → pending (đúng luật mồ côi cũ)
      done                              → GIỮ NGUYÊN (bất biến done-không-reset, §0b)
    Trả (state_moi, thay_doi). Không sửa tại chỗ — state cũ giữ nguyên để so được 2 chiều."""
    import copy as _copy
    st = _copy.deepcopy(state) if isinstance(state, dict) else {}
    have = {str(x).strip() for x in (master_unit_ids or []) if str(x).strip()}
    thay_doi = []
    for u in (st.get("q_units") or []):
        if not isinstance(u, dict):
            continue
        uid, cur = str(u.get("unit_id") or ""), str(u.get("trang_thai") or "")
        if cur != "doing" or not uid:
            continue
        moi = "done" if uid in have else "pending"
        u["trang_thai"] = moi
        thay_doi.append({"unit_id": uid, "tu": cur, "sang": moi,
                         "can_cu": ("co master/" + uid + ".json") if moi == "done" else "khong co master"})
    return st, thay_doi


def _rasoat_meta_folder(a):
    """r213/a: giải folder `_meta/` cho đường ghi state. Thứ tự: --folder-id → env
    TL_META_FOLDER_ID (profile apply đã nạp từ `metaFolderId`). Trả (folder_id, loi).

    Lỗi KHÔNG cụt lủn: sự cố PROFILE_META_FOLDER_KHONG_CO_TRONG_CONFIG (26-07) làm mất thời gian
    đúng vì thông báo không chỉ đường; đường vòng ĐỌC-ONLY (profile-sync DRY, KHÔNG --apply) nay
    do máy đọc ra, không phải người tự nhớ."""
    fid = str(getattr(a, "folder_id", "") or "").strip()
    if fid:
        return fid, ""
    fid = os.environ.get("TL_META_FOLDER_ID", "").strip()
    if fid:
        return fid, ""
    return "", ("META_FOLDER_ID_TRONG — profile chưa có `metaFolderId`. Đọc marker KHÔNG cần --apply: "
                "`tl --profile <P> profile-sync --json` → rows[].diffs[].marker; rồi truyền "
                "`--folder-id <id>` hoặc đặt env TL_META_FOLDER_ID.")


def _rasoat_thieu_gia_tri(v) -> bool:
    """PURE — "trường này CÓ giá trị dùng được không", dùng CHUNG cho mọi phép đòi trường của
    `_rasoat_state_validate`. Sinh ra vì hai phép kiểm khác nhau đã tồn tại song song cho cùng một
    loại ràng buộc (`.strip()` cho trường nền, truthiness cho trường có điều kiện) và chỗ lệch ấy
    cho `"dong_luc": " "` đi lọt. Xử luôn list/dict RỖNG: `gioi_han_da_biet: []` là "chưa khai",
    không phải "đã khai rỗng" — mà `str([]).strip()` lại là `"[]"`, truthy, nên phép kiểm chuỗi
    trần cũng sai ở đúng chỗ ấy."""
    if v is None:
        return True
    if isinstance(v, (list, dict, tuple, set)):
        return len(v) == 0
    return not str(v).strip()


def _rasoat_state_validate(obj) -> tuple:
    """PURE — r295 (RAS-09, audit lõi 31-07): validate `rasoat_plan.v1` TRƯỚC khi ghi lên Drive.

    Trước bản vá, `state-put` chỉ `json.loads` rồi upload: root `[]`, JSON rỗng, `trang_thai` sai chính
    tả — tất cả đều lọt. State là NGUỒN SỰ THẬT của lớp điều phối; ghi rác vào đó làm phiên kế nhiệm
    đọc ra và quyết định sai, mà lỗi chỉ lộ ở lượt sau nên rất khó truy.

    Đặc tả: `references/RASOAT_PLAN_SCHEMA.md` §2-§3. Trả (ok, errors[]). Chỉ kiểm những gì đặc tả CHỐT
    (root object, schema, enum đóng, `unit_id` bắt buộc) — KHÔNG tự chế thêm ràng buộc ngoài đặc tả.

    ★ Từ vựng đóng để TRONG hàm có chủ đích: hằng mức module của `tl_core/*` KHÔNG tự có mặt trong
    namespace `tl` (chúng phải re-export tay như `_RASOAT_STATE_ALLOWED` ở `tl.py`), nên hằng rời là một
    nguồn `NameError` chỉ lộ trên đường sản xuất. Chỉ hàm này dùng ⇒ giữ tại chỗ, hết đường trôi.
    """
    _TT_UNIT = ("pending", "doing", "done", "blocked", "stale")
    # G4 (cross-review cục bộ P1): `RASOAT_PLAN_SCHEMA.md` §3 khai TÁM trạng thái; validator chỉ có
    # SÁU, nên state HỢP LỆ mang `da_quyet`/`da_quyet_va_thi_hanh` (mục người thẩm tra đã quyết) bị
    # bác. Trước đây vô hại vì chỉ `state-put` gọi; từ khi `rasoat-dot-check` biến nó thành CỔNG BẮT
    # BUỘC lúc đóng Đợt thì nó CHẶN OAN đúng lúc hồ sơ sắp xong — fail-closed sai chiều.
    _TT_INGEST = ("cho_tai", "cho_nguoi_tai", "dry_planned", "staged", "flipped", "out_of_scope",
                  "da_quyet", "da_quyet_va_thi_hanh")
    _TT_DOT = ("chua_mo", "dang_ra", "da_dong", "da_dong_co_gioi_han")
    # Hai trạng thái Q-INGEST được `rasoat-dot-check` quy thành claim «kho thiếu». Giữ TẠI CHỖ theo
    # đúng ghi chú ở đầu hàm: hằng mức module của `tl_core` không tự có trong namespace đã re-home.
    _TT_SINH_CLAIM = ("cho_tai", "cho_nguoi_tai")
    _TT_NLM = ("pending", "added", "failed")
    _LOAI_UNIT = ("ra_soat", "doi_chieu_bo_sung")
    errs = []
    if not isinstance(obj, dict):
        return False, ["ROOT_KHONG_PHAI_OBJECT:" + type(obj).__name__]
    if str(obj.get("schema") or "") != "rasoat_plan.v1":
        errs.append("SCHEMA_SAI:" + str(obj.get("schema")))
    _sc = obj.get("session_claim")
    if _sc is not None:
        if not isinstance(_sc, dict):
            errs.append("SESSION_CLAIM_KHONG_PHAI_OBJECT")
        elif not str(_sc.get("id") or "").strip():
            # LỚP C — CHẶN OAN cũng là hỏng, và nguy ngang fail-open vì nó chặn đúng lúc việc sắp
            # xong. §7 khai dạng ĐÃ NHẢ (`id: null` + `released_at`) và `_rasoat_vong_doi_findings`
            # ĐÃ mã hoá đúng dạng ấy ⇒ validator bác nó là hai chỗ trong cùng kho nói ngược nhau.
            # Chỉ tha khi CÓ `released_at`; `id` rỗng mà không nhả thì vẫn ĐỎ.
            # §7 khai dạng đã nhả là `id: null` — ĐÚNG NGHĨA null, không phải "mọi giá trị falsy".
            # `id: ""` hay `id: 0` mà có `released_at` thì `_rasoat_vong_doi_findings` vẫn coi là CHƯA
            # nhả (nó so `is None`), nên nới ở đây là để hai chốt trong cùng kho phán ngược nhau.
            # `.get("id")` trả None cho CẢ khoá vắng mặt — một claim ghi dở (chỉ có `released_at`)
            # khi ấy được coi là ĐÃ NHẢ. §7 đòi CẢ HAI dấu, nên phải hỏi khoá CÓ MẶT.
            if ("id" not in _sc or _sc.get("id") is not None
                    or not str(_sc.get("released_at") or "").strip()):
                errs.append("SESSION_CLAIM_THIEU_ID")
    # G4: mảng `dot` (§8) trước đây KHÔNG được kiểm gì ⇒ `dot: "broken"` lọt sạch. `dot_id`/`ten`
    # bắt buộc, `trang_thai` theo enum §3 — đúng những gì đặc tả CHỐT, không tự chế thêm.
    _dot = obj.get("dot")
    if _dot is not None:
        if not isinstance(_dot, list):
            errs.append("DOT_KHONG_PHAI_MANG")
        else:
            for _i, _x in enumerate(_dot):
                if not isinstance(_x, dict):
                    errs.append(f"DOT[{_i}]_KHONG_PHAI_OBJECT")
                    continue
                # H1 (P1): §8 khai BA trường bắt buộc; bản đầu chỉ đòi `dot_id` và tha `trang_thai`
                # RỖNG (`_tt and ...`) ⇒ `{"dot_id":"dot-01"}` lọt sạch.
                for _bb in ("dot_id", "ten", "trang_thai"):
                    if not str(_x.get(_bb) or "").strip():
                        errs.append(f"DOT[{_i}]_THIEU_" + _bb.upper())
                _tt = str(_x.get("trang_thai") or "").strip()
                if _tt and _tt not in _TT_DOT:
                    errs.append(f"DOT[{_i}]_TRANG_THAI_SAI:" + _tt)
                # LỚP B — §8 còn khai trường bắt buộc THEO TRẠNG THÁI. Bỏ chúng thì luật "cấm đóng
                # im lặng" mất hiệu lực đúng lúc cần nhất: khai `da_dong_co_gioi_han` mà không có
                # `gioi_han_da_biet` CHÍNH LÀ đóng im lặng, chỉ khác cái nhãn.
                # Trường có điều kiện phải dùng CÙNG phép kiểm với trường nền. Bản trước dùng
                # `not _x.get(...)` nên `"dong_luc": " "` (một dấu cách) là truthy ⇒ LỌT. Hai phép
                # kiểm khác nhau cho cùng một loại ràng buộc là chỗ lệch tự mọc ra; nay một hàm.
                for _tt_can, _truong in (("da_dong_co_gioi_han", "gioi_han_da_biet"),
                                         ("da_dong_co_gioi_han", "dong_luc"),
                                         ("da_dong", "dong_luc"), ("dang_ra", "mo_luc")):
                    if _tt == _tt_can and _rasoat_thieu_gia_tri(_x.get(_truong)):
                        errs.append(f"DOT[{_i}]_THIEU_{_truong.upper()}_KHI_{_tt.upper()}")
            # §8 bất biến 1: TỐI ĐA MỘT Đợt `dang_ra`. Kiểm từng-bản-ghi không bao giờ thấy điều
            # này — nó là ràng buộc của TẬP HỢP, nên phải kiểm sau vòng lặp. Hai Đợt chồng nhau thì
            # `dry_rounds_lien_tiep` và Q-INGEST không quy được về Đợt nào.
            _dang_ra = [str(x.get("dot_id") or "") for x in _dot
                        if isinstance(x, dict) and str(x.get("trang_thai") or "").strip() == "dang_ra"]
            if len(_dang_ra) > 1:
                errs.append("DOT_NHIEU_HON_MOT_DANG_RA:" + ",".join(sorted(_dang_ra)[:5]))
    # `dot` sai kiểu đã được ghi nhận `DOT_KHONG_PHAI_MANG` ở trên, nhưng comprehension này vẫn
    # LẶP trên nó ⇒ `{"dot": 1}` ném TypeError, và cả `state-put` lẫn `rasoat-dot-check` trả
    # traceback thay vì rc=2 có cấu trúc. Validator mà tự crash trên đầu vào hỏng thì nó không còn
    # là validator — chỉ dựng tập khi `_dot` THỰC SỰ là list.
    _dot_ids = ({str(x.get("dot_id") or "").strip() for x in _dot if isinstance(x, dict)} - {""}
                if isinstance(_dot, list) else set())
    for _khoa, _tt_hop_le in (("q_units", _TT_UNIT), ("q_ingest", _TT_INGEST), ("q_nlm", _TT_NLM)):
        _q = obj.get(_khoa)
        if _q is None:
            continue
        if not isinstance(_q, list):
            errs.append(_khoa.upper() + "_KHONG_PHAI_MANG")
            continue
        for _i, _x in enumerate(_q):
            if not isinstance(_x, dict):
                errs.append(f"{_khoa.upper()}[{_i}]_KHONG_PHAI_OBJECT")
                continue
            # LỚP B — `trang_thai` là trường MÁY ĐỌC nên KHÔNG được vắng. Bản trước chỉ kiểm enum
            # KHI có giá trị, nên mục thiếu hẳn `trang_thai` lọt sạch rồi bị lớp trên bỏ qua ⇒ cổng
            # trả rc=0 với 0 claim. "Kiểm-khi-có" là danh sách CẤM trá hình: nó tha đúng cái vắng mặt.
            if not str(_x.get("trang_thai") or "").strip():
                errs.append(f"{_khoa.upper()}[{_i}]_THIEU_TRANG_THAI")
            # Mục Q-INGEST không có `so_hieu` là mục KHÔNG CHỈ ĐÍCH ĐƯỢC văn bản nào. Cổng cuối Đợt
            # rút claim từ đây; mục rỗng bị lọc đi lặng lẽ ⇒ cổng KHÔNG đòi bằng chứng tra kho nào
            # rồi trả rc=0, trong khi luật đóng Đợt cấm còn mục chưa xử. Đòi ngay ở validator.
            # CHỈ ràng ở trạng thái SINH RA CLAIM. Đòi vô điều kiện là phá tương thích: mục đã
            # xử xong (`flipped`, `da_quyet`…) không cần `so_hieu`, và kho có sẵn fixture đóng-sạch
            # dùng `{"trang_thai":"flipped"}` — làm mọi `state-put` sau đó ĐỎ. Lý do của chốt này là
            # "mục còn treo bị lọc lặng lẽ thành 0 claim", nên phạm vi đúng là đúng hai trạng thái ấy.
            if (_khoa == "q_ingest" and str(_x.get("trang_thai") or "").strip() in _TT_SINH_CLAIM
                    and _rasoat_thieu_gia_tri(_x.get("so_hieu"))):
                errs.append(f"Q_INGEST[{_i}]_THIEU_SO_HIEU")
            # `dot_id` chỉ bắt buộc khi hồ sơ CÓ dùng Đợt — không ép hồ sơ chưa chia Đợt.
            if _dot and _khoa in ("q_units", "q_ingest"):
                _di = str(_x.get("dot_id") or "").strip()
                if not _di:
                    errs.append(f"{_khoa.upper()}[{_i}]_THIEU_DOT_ID")
                # KHÔNG đòi `dot_id` phải trỏ Đợt ĐÃ KHAI. Bản trước đòi, và nó BÁC chính ví dụ
                # chuẩn của đặc tả: `dot` mới có `dot-01` trong khi `q_units` đã tham chiếu `dot-02`
                # (`RASOAT_PLAN_SCHEMA.md` §2) — tức xếp việc cho Đợt SẮP MỞ là hình mẫu HỢP LỆ, và
                # chốt ấy làm mọi `state-put` theo đúng tài liệu bị chặn. Rủi ro "dot_id gõ nhầm" là
                # THẬT nhưng thuộc lúc ĐÓNG ĐỢT, không thuộc lúc ghi state: state không phân biệt
                # được "Đợt tương lai" với "gõ nhầm". Đã chuyển sang `rasoat-dot-check` (phát hiện,
                # rc=1) thay vì bác ở đây (rc=2) — đúng chỗ mới có đủ ngữ cảnh để phán.
            _tt = str(_x.get("trang_thai") or "")
            if _tt and _tt not in _tt_hop_le:
                errs.append(f"{_khoa.upper()}[{_i}].trang_thai_NGOAI_ENUM:{_tt}")
            if _khoa == "q_units":
                if not str(_x.get("unit_id") or "").strip():
                    errs.append(f"Q_UNITS[{_i}]_THIEU_unit_id")
                _loai = str(_x.get("loai") or "")
                if _loai and _loai not in _LOAI_UNIT:
                    errs.append(f"Q_UNITS[{_i}].loai_NGOAI_ENUM:{_loai}")
    return (not errs), errs


def _rasoat_state_newest(g, cands):
    """r295 (RAS-03, audit lõi 31-07): chọn bản MỚI NHẤT theo `modifiedTime` — DÙNG CHUNG cho
    `state-get` và `state-put`. Trả (pick, canh_bao[]).

    Trước bản vá `state-get` chọn newest còn `state-put` so CAS với `olds[0]` THÔ ⇒ hai lệnh có thể
    nhìn HAI tài liệu khác nhau, và ca trùng tên là có thật (chính code cũ đã phải in
    `CO_n_BAN_TRUNG_TEN`). Hệ quả: `--expect-claim` khớp với bản CŨ rồi ghi đè bản MỚI của phiên khác —
    đúng thứ ADR-0016 single-writer sinh ra để chặn.

    Khi MỌI lượt hỏng `modifiedTime` (rỗng hết): xếp theo `id` để tất định, và NÓI RA — không im lặng
    chọn theo thứ tự `list` trả về (thứ tự đó không cam kết, audit đã nêu ở phần rủi ro).
    """
    canh_bao = []
    if not cands:
        return None, canh_bao
    if len(cands) == 1:
        return cands[0], canh_bao
    stamped = []
    for c in cands:
        try:
            inf = (_gas_get_retry(g, "info", fileId=str(c.get("id"))) or {}).get("file") or {}
        except Exception:  # noqa: BLE001
            inf = {}
        stamped.append((str(inf.get("modifiedTime") or ""), str(c.get("id") or ""), c))
    if not any(t[0] for t in stamped):
        stamped.sort(key=lambda t: t[1])
        canh_bao.append("KHONG_DOC_DUOC_modifiedTime_CUA_BAN_NAO — chọn tất định theo id (%s); "
                        "chưa chứng minh được là bản mới nhất." % stamped[0][2].get("id"))
        return stamped[0][2], canh_bao
    stamped.sort(key=lambda t: (t[0], t[1]), reverse=True)
    pick = stamped[0][2]
    canh_bao.append("CO_%d_BAN_TRUNG_TEN — chọn bản mới nhất (%s); bản cũ chưa được dọn, "
                    "`state-put` lượt sau sẽ dọn." % (len(cands), pick.get("id")))
    return pick, canh_bao


def _rasoat_state_find(g, folder_id, name):
    """r213/a: tìm MỌI bản `name` trong folder `_meta/` (khớp tên CHÍNH XÁC — bài học
    `_index_old_candidates`: startswith từng suýt trash nhầm file backup của người dùng)."""
    items = (_gas_get_retry(g, "list", folderId=folder_id) or {}).get("items") or []
    return [x for x in items
            if str(x.get("name") or "") == name and str(x.get("type") or "") != "folder"]


def cmd_state_get(a) -> int:
    """r213/a — ĐỌC state rà hồ sơ từ Drive `_meta/` (WRITE_PATHS_v1). READ-ONLY.
    rc=0 đọc được · rc=3 CHƯA CÓ trên Drive (lượt đầu — KHÔNG phải lỗi) · rc=2 lỗi thật."""
    import base64
    # r295 (RAS-08, audit lõi 31-07): ÁP PROFILE TRƯỚC khi giải `_meta/`. Bản cũ gọi
    # `_rasoat_meta_folder(a)` rồi mới `load_creds(...)` — mà `metaFolderId` chỉ vào env KHI profile được
    # áp ⇒ `--profile <P>` bị bỏ qua sạch, lệnh báo META_FOLDER_ID_TRỐNG hoặc tệ hơn là dùng env còn sót
    # của profile TRƯỚC ĐÓ. Cùng khuôn với `cmd_rasoat_loop`/`cmd_rasoat_chongcheo` (đã áp từ đầu hàm).
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    name = str(getattr(a, "name", "") or "rasoat_state.json").strip()
    as_json = bool(getattr(a, "json", False))
    ok, why = _rasoat_state_scope(name)
    if not ok:
        _print_json_or_text({"schema": "rasoat_state_get.v1", "ok": False, "error": why}, True)
        return 2
    fid, err = _rasoat_meta_folder(a)
    if err:
        _print_json_or_text({"schema": "rasoat_state_get.v1", "ok": False, "error": err}, True)
        return 2
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        g = _gas()
        cands = _rasoat_state_find(g, fid, name)
    except SystemExit as e:
        _print_json_or_text({"schema": "rasoat_state_get.v1", "ok": False,
                             "error": "CAN_WEBAPP_LIVE: " + str(e)}, True)
        return 2
    except Exception as e:  # noqa: BLE001
        _print_json_or_text({"schema": "rasoat_state_get.v1", "ok": False,
                             "error": "LIST_FAILED: " + str(e)}, True)
        return 2
    if not cands:
        _print_json_or_text({"schema": "rasoat_state_get.v1", "ok": True, "found": False,
                             "name": name, "folderId": fid,
                             "note": "chưa có state trên Drive — lượt rà ĐẦU TIÊN của hồ sơ này"}, True)
        return 3
    # r295 (RAS-03): >1 bản cùng tên = lần dọn trước hụt. Chọn bản MỚI NHẤT qua helper DÙNG CHUNG với
    # `state-put` — trước đây hai lệnh cài hai phép chọn khác nhau nên có thể nhìn hai tài liệu khác nhau.
    pick, canh_bao = _rasoat_state_newest(g, cands)
    try:
        r = _gas_get_retry(g, "download", fileId=str(pick.get("id")))
        body = base64.b64decode(r["b64"]).decode("utf-8")
        state = json.loads(body)
    except Exception as e:  # noqa: BLE001
        _print_json_or_text({"schema": "rasoat_state_get.v1", "ok": False,
                             "error": "DOWNLOAD_OR_PARSE_FAILED: " + str(e),
                             "fileId": pick.get("id")}, True)
        return 2
    out_path = str(getattr(a, "out", "") or "").strip()
    if out_path:
        Path(out_path).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    payload = {"schema": "rasoat_state_get.v1", "ok": True, "found": True, "name": name,
               # r213 (bắt ở lượt kiểm LIVE 26-07): PHẢI đếm BYTE utf-8, không phải KÝ TỰ — `state-put`
               # đếm byte nên bản đầu báo 478/471 cho CÙNG một file (7 ký tự có dấu), nhìn như mất dữ liệu.
               "folderId": fid, "fileId": pick.get("id"), "bytes": len(body.encode("utf-8")),
               "out": out_path or None, "canh_bao": canh_bao}
    if as_json:
        payload["state"] = state
    _print_json_or_text(payload, True)
    return 0


def cmd_state_put(a) -> int:
    """r213/a — GHI state rà hồ sơ lên Drive `_meta/` (WRITE_PATHS_v1), KHÔNG cần người duyệt.

    Đây là điểm cả kiến trúc xoay quanh: `_meta/rasoat_state.json` là nguồn sự thật resume, phải
    ghi được sau MỖI đơn vị rà. Mượn cổng `profile-file-add --apply --confirm yes` là bắt người
    duyệt mỗi lần chốt state ⇒ phá nghiệm thu H7 (≤2 lần xen/hồ sơ). Vì vậy lệnh này KHÔNG có
    --confirm; đổi lại nó bị khoá bằng BA chốt máy:
      1. `_rasoat_state_scope` — chỉ đúng tên trong WRITE_PATHS_v1, fail-CLOSED;
      2. folder đích BẮT BUỘC là `_meta/` (--folder-id / TL_META_FOLDER_ID), không có mặc định root;
      3. `--expect-claim` — TỪ CHỐI ghi khi `session_claim.id` trên Drive khác kỳ vọng (single-writer).
    register/share="false" ⇒ KHÔNG vào registry, KHÔNG chia sẻ link (mặc định `upload` là
    ANYONE_WITH_LINK — state để mở link công khai là rò rỉ, phải tắt TƯỜNG MINH).
    THỨ TỰ AN TOÀN: tạo bản MỚI trước → mới dọn bản cũ. Chết giữa chừng = tồn 2 bản, `state-get`
    lấy bản mới nhất và lượt `state-put` sau dọn nốt; đảo thứ tự thì chết giữa chừng = MẤT state."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))   # r295 RAS-08 (xem state-get)
    name = str(getattr(a, "name", "") or "rasoat_state.json").strip()
    src = str(getattr(a, "in_file", "") or "").strip()
    dry = bool(getattr(a, "dry_run", False))
    ok, why = _rasoat_state_scope(name)
    if not ok:
        _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": False, "error": why}, True)
        return 2
    if not src or not Path(src).is_file():
        _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": False,
                             "error": "IN_FILE_KHONG_TON_TAI: " + (src or "(trống)")}, True)
        return 2
    try:
        body_obj = json.loads(Path(src).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": False,
                             "error": "IN_FILE_KHONG_PHAI_JSON_HOP_LE: " + str(e)}, True)
        return 2
    # r295 (RAS-09): JSON hợp lệ CHƯA phải state hợp lệ. Chốt thứ TƯ, cùng hạng ba chốt trong docstring.
    _v_ok, _v_errs = _rasoat_state_validate(body_obj)
    if not _v_ok:
        _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": False,
                             "error": "STATE_KHONG_HOP_LE", "loi": _v_errs,
                             "fix": "đặc tả `references/RASOAT_PLAN_SCHEMA.md` §2-§3 — root là object, "
                                    "`schema: rasoat_plan.v1`, `q_units[].unit_id` bắt buộc, "
                                    "`trang_thai`/`loai` phải trong từ vựng đóng."}, True)
        return 2
    fid, err = _rasoat_meta_folder(a)
    if err:
        _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": False, "error": err}, True)
        return 2
    body = json.dumps(body_obj, ensure_ascii=False, indent=2)
    if dry:
        _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": True, "dry_run": True,
                             "name": name, "folderId": fid, "bytes": len(body.encode("utf-8")),
                             "se_lam": ["upload bản mới (register/share=false)", "trash bản cũ trùng tên"]}, True)
        return 0
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        g = _gas()
        olds = _rasoat_state_find(g, fid, name)
    except SystemExit as e:
        _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": False,
                             "error": "CAN_WEBAPP_LIVE: " + str(e)}, True)
        return 2
    except Exception as e:  # noqa: BLE001
        _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": False,
                             "error": "LIST_FAILED: " + str(e)}, True)
        return 2
    expect = str(getattr(a, "expect_claim", "") or "").strip()
    # r295 (RAS-02, audit lõi 31-07): state ĐÃ TỒN TẠI thì `--expect-claim` là BẮT BUỘC. Bản cũ bọc trọn
    # khối CAS trong `if expect:` ⇒ không truyền cờ là bỏ qua sạch chốt single-writer, ghi đè thẳng
    # claim của phiên khác — trái ADR-0016, và đúng thứ chốt thứ 3 trong docstring hứa là có.
    # Chỉ create-first (chưa có bản nào) mới được miễn.
    if olds and not expect:
        _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": False,
                             "error": "THIEU_EXPECT_CLAIM", "so_ban_tren_drive": len(olds),
                             "note": "state đã tồn tại ⇒ PHẢI `--expect-claim <id claim đang cầm>` "
                                     "(single-writer, ADR-0016). Lấy id bằng `tl state-get --json` → "
                                     "`state.session_claim.id`. Chỉ lượt TẠO MỚI mới được bỏ cờ này."}, True)
        return 2
    if expect:
        import base64 as _b64
        cur_claim, doc_ok = "", False
        if olds:
            # r295 (RAS-03): so CAS với bản MỚI NHẤT — cùng helper `state-get` dùng để đọc. Bản cũ lấy
            # `olds[0]` THÔ nên khi có bản trùng tên, CAS soi bản CŨ rồi cho ghi đè bản MỚI.
            _pick_cas, _cb_cas = _rasoat_state_newest(g, olds)
            try:
                r = _gas_get_retry(g, "download", fileId=str((_pick_cas or {}).get("id")))
                cur = json.loads(_b64.b64decode(r["b64"]).decode("utf-8"))
                cur_claim = str(((cur or {}).get("session_claim") or {}).get("id") or "")
                doc_ok = True
            except Exception:  # noqa: BLE001
                doc_ok = False
        # FAIL-CLOSED: không đọc được bản trên Drive thì KHÔNG kết luận "chắc là khớp".
        if olds and not doc_ok:
            _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": False,
                                 "error": "EXPECT_CLAIM_KHONG_KIEM_DUOC — có bản trên Drive nhưng "
                                          "đọc/parse hỏng; từ chối ghi đè."}, True)
            return 2
        if olds and cur_claim != expect:
            _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": False,
                                 "error": "CLAIM_LECH", "claim_tren_drive": cur_claim,
                                 "claim_ky_vong": expect,
                                 "note": "phiên khác đang cầm claim — theo §9 stale-claim takeover: "
                                         "chỉ chiếm quyền khi claim quá hạn mà con trỏ tiến độ KHÔNG nhích."}, True)
            return 2
    rid = _apply_journal_start("state-put", {"name": name, "folderId": fid, "old": len(olds)})
    up = g.post("upload", b64=_b64_text(body), name=name, mime="application/json",
                folderId=fid, convert="false", register="false", share="false", force="true")
    new_id = up.get("fileId") or up.get("id")
    if not new_id:
        _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": False, "step": "upload",
                             "detail": up, "journal": rid}, True)
        return 2
    _journal_append(rid, {"t": "commit", "op": "state_upload", "key": new_id, "ok": True})
    cleanup = []
    for old in olds:
        oid = str(old.get("id") or "")
        if not oid or oid == new_id:
            continue
        _journal_append(rid, {"t": "intent", "op": "drive_trash", "key": oid, "set": {"restore": "action restore"}})
        try:
            tr = g.get("trash", fileId=oid, confirm="yes")
        except Exception as e:  # noqa: BLE001
            tr = {"ok": False, "error": str(e)}
        _journal_append(rid, {"t": "commit", "op": "drive_trash", "key": oid, "ok": bool(tr.get("ok"))})
        cleanup.append({"fileId": oid, "ok": bool(tr.get("ok"))})
    don_ok = all(x.get("ok") for x in cleanup)
    _print_json_or_text({"schema": "rasoat_state_put.v1", "ok": True, "name": name, "folderId": fid,
                         "fileId": new_id, "bytes": len(body.encode("utf-8")),
                         "don_ban_cu": cleanup, "don_sach": don_ok, "journal": rid,
                         "note": None if don_ok else "bản cũ chưa dọn hết — state-get vẫn đúng "
                                                     "(lấy bản mới nhất), lượt state-put sau dọn tiếp."}, True)
    return 0


def cmd_rasoat_merge(a) -> int:
    """r213/b — DỒN N phiếu `master/<unit>.json` (khuôn §6) thành MỘT bảng master mà
    `rasoat_phuluc.py` đọc thẳng được. Đây là mắt xích PHA 4 mà Đợt 1–3 tả bằng lời ("dồn phát hiện
    vào bảng master") nhưng không ai cài — nó sập ngay lần chạy thật đầu tiên (26-07).
    Không gọi mạng, không NLM. rc=0 sạch · rc=2 lỗi/có file khuôn lạ bị bỏ."""
    inp = str(getattr(a, "in_dir", "") or "").strip()
    p = Path(inp) if inp else None
    if not p or not p.exists():
        _print_json_or_text({"schema": "rasoat_merge.v1", "ok": False,
                             "error": "IN_KHONG_TON_TAI: " + (inp or "(trống)")}, True)
        return 2
    tat_ca = sorted(p.glob("*.json")) if p.is_dir() else [p]
    # r216 — bản sao lưu để lẫn trong master/ KHÔNG được gộp; bỏ qua nhưng phải KHAI BÁO.
    ban_sao = [f for f in tat_ca if p.is_dir() and _rasoat_la_ban_sao(f.name)]
    files = [f for f in tat_ca if f not in ban_sao]
    docs, hong = [], []
    for f in files:
        try:
            docs.append((f.name, json.loads(f.read_text(encoding="utf-8"))))
        except Exception as e:  # noqa: BLE001
            hong.append({"nguon": f.name, "ly_do": "JSON_HONG: " + str(e)})
    merged = _rasoat_merge_units(docs)
    bo_qua = (merged.get("_bo_qua") or []) + hong
    merged["_bo_qua"] = bo_qua
    out_path = str(getattr(a, "out", "") or "").strip() or str(
        (p.parent if p.is_dir() else p.parent) / "BANG_MASTER.json")
    bo_qua_ban_sao = [{"nguon": f.name, "ly_do": "BAN_SAO_LUU_BI_BO_QUA"} for f in ban_sao]
    # r321 (RAS-17): neo phải LỘ DIỆN ở MỌI chế độ — đếm ở ĐÂY, không phải trong nhánh ghi, để
    # `--check` và `--dry-run` cũng thấy. Trước bản này `anchor` không có đường nào chạm tới.
    anchor_hong = _rasoat_anchor_quet(docs)
    nen = {"schema": "rasoat_merge.v1", "in": str(p), "out": out_path,
           "so_file": len(files), "so_van_ban": len(merged.get("van_ban") or []),
           "so_phat_hien": len(merged.get("noi_dung") or []),
           "bo_qua_ban_sao": bo_qua_ban_sao,
           "so_anchor_hong": len(anchor_hong), "anchor_hong": anchor_hong}
    # r216 — CỔNG TRÙNG (fail-CLOSED): trùng `key`/`unit_id` ⇒ KHÔNG ghi. Ghi đè bằng bảng đã đếm
    # hai lần là mất luôn bản đúng để đối chiếu ở lượt sau.
    trung = _rasoat_trung_lap(docs)
    if trung.get("key") or trung.get("unit_id"):
        _print_json_or_text(dict(nen, ok=False, error="TRUNG_LAP_GIUA_CAC_NGUON", trung_lap=trung,
                                 da_ghi=False, bo_qua=bo_qua,
                                 fix="mỗi phát hiện chỉ được nằm ở MỘT phiếu và mỗi `unit_id` chỉ "
                                     "một file; bản sao lưu đặt NGOÀI thư mục master/"), True)
        return 2
    # r290 (RAS-11 — audit lõi 31-07): nguồn KHÔNG ĐỌC ĐƯỢC phải fail-CLOSED y như cổng trùng r216 ngay
    # trên. Bản cũ nhét `hong` vào `bo_qua` rồi VẪN `write_text` bảng master dựng từ phần input hợp lệ,
    # xong mới `return 2` — tức đã ghi đè bảng bằng bản THIẾU trong khi lệnh báo lỗi. Người vận hành thấy
    # rc=2 sẽ sửa file hỏng rồi chạy lại, nhưng bản đúng để đối chiếu đã mất từ lượt đó. Cùng một hậu quả
    # mà r216 sinh ra để chặn: "bảng master sai mà vẫn ghi đè thì lần chạy sau không còn bản đúng".
    if hong:
        _print_json_or_text(dict(nen, ok=False, error="NGUON_HONG_KHONG_DOC_DUOC", da_ghi=False,
                                 bo_qua=bo_qua, nguon_hong=hong,
                                 fix="sửa hoặc bỏ các file JSON hỏng rồi chạy lại; bảng master GIỮ "
                                     "NGUYÊN để còn đối chiếu"), True)
        return 2
    # r321 (RAS-17) — `--anchor-strict`: fail-CLOSED TRƯỚC mọi thao tác ghi, cùng khuôn r216/r290.
    # KHÔNG bật mặc định, và đó là lựa chọn CÓ CHỦ Ý: hồ sơ đang lưu giữ 82/82 ô neo sai khuôn, bật
    # mặc định là chặn đứng mọi hồ sơ CŨ vì một lỗi lượt rà không gây ra và chưa có đường sửa trọn
    # (đo 02-08: 47/82 ô di trú được từ cache, 35/82 thì KHÔNG). Vì vậy mặc định LỘ DIỆN, cưỡng chế
    # thì phải gọi tên — đúng khuôn r312 với ING-09: chặn cái MỚI, khai cái CŨ, không dọn lén.
    if bool(getattr(a, "anchor_strict", False)) and anchor_hong:
        _print_json_or_text(dict(nen, ok=False, error="ANCHOR_SAI_KHUON", da_ghi=False,
                                 bo_qua=bo_qua,
                                 fix="`anchor.doc_deps[].text_hash` phải khớp `sha256:<64hex>`; địa "
                                     "chỉ định vị chuyển sang trường `locator` cùng dep. Ô KHÔNG "
                                     "truy nguyên được thì ĐỂ TRỐNG và khai `anchor_con_hieu_luc:"
                                     "false` + `ly_do_anchor`, ĐỪNG tính lại bằng bản hiện hành — "
                                     "làm thế là khẳng định một độ tươi chưa hề kiểm."), True)
        return 2
    # r216 — `--check`: đối chiếu bảng master đang có với kết quả merge, KHÔNG ghi đè.
    if bool(getattr(a, "check", False)):
        cu_p = Path(out_path)
        if not cu_p.is_file():
            _print_json_or_text(dict(nen, ok=False, error="CHECK_KHONG_CO_BANG_MASTER_DE_DOI_CHIEU",
                                     da_ghi=False, bo_qua=bo_qua), True)
            return 2
        try:
            cu = json.loads(cu_p.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            _print_json_or_text(dict(nen, ok=False, error="CHECK_BANG_MASTER_HONG: " + str(e),
                                     da_ghi=False, bo_qua=bo_qua), True)
            return 2
        lech = _rasoat_check_lech(cu, merged)
        _print_json_or_text(dict(nen, ok=not lech and not bo_qua, che_do="check", da_ghi=False,
                                 so_lech=len(lech), lech=lech, bo_qua=bo_qua,
                                 fix=None if not lech else
                                 "bảng master ĐI TRƯỚC tầng unit: chép phát hiện về `master/<unit>.json` "
                                 "rồi merge lại, ĐỪNG merge đè — merge lấy unit làm nguồn."), True)
        return 0 if (not lech and not bo_qua) else 2
    # Hoà giải state (khe hở H8): CHỈ khi người gọi trỏ --state; sửa tại chỗ là quyết định của họ.
    # r290 (RAS-12 + RAS-07): TOÀN BỘ khối này chuyển lên TRƯỚC mọi thao tác ghi. Bản cũ bọc trọn nó
    # trong một `try/except` rồi nhét lỗi vào `hoa_giai["loi"]`, trong khi `ok = not bo_qua` ⇒ `--state`
    # hỏng mà lệnh vẫn `ok:true`, rc=0, và bảng master thì đã ghi xong từ dòng trên.
    hoa_giai, _st_moi = None, None
    st_path = str(getattr(a, "state", "") or "").strip()
    if st_path and Path(st_path).is_file():
        try:
            st = json.loads(Path(st_path).read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            _print_json_or_text(dict(nen, ok=False, error="STATE_HONG_KHONG_DOC_DUOC: " + str(e),
                                     da_ghi=False, bo_qua=bo_qua, state=st_path,
                                     fix="sửa file --state rồi chạy lại; CHƯA ghi gì cả"), True)
            return 2
        # RAS-07: `f.stem` KHÔNG phải định danh đơn vị. File `unit-a.json` mang `unit_id: unit-b` làm
        # state đánh DONE cho unit-a — đơn vị chưa hề được rà — và bỏ sót unit-b. Nguồn sự thật là
        # PAYLOAD; thiếu `unit_id` thì không chứng minh được đơn vị nào đã xong ⇒ fail-closed.
        _uid_theo_file = [(_n, str((_d or {}).get("unit_id") or "").strip()) for _n, _d in docs]
        _thieu_uid = [_n for _n, _u in _uid_theo_file if not _u]
        if _thieu_uid:
            _print_json_or_text(dict(nen, ok=False, error="STATE_HOA_GIAI_THIEU_UNIT_ID", da_ghi=False,
                                     bo_qua=bo_qua, thieu_unit_id=_thieu_uid,
                                     fix="mỗi phiếu `master/<unit>.json` phải mang `unit_id`; KHÔNG suy "
                                         "ra từ tên file vì tên có thể lệch nội dung"), True)
            return 2
        _ten_lech = [{"file": _n, "unit_id": _u} for _n, _u in _uid_theo_file if Path(_n).stem != _u]
        _st_moi, thay_doi = _rasoat_state_reconcile(st, [_u for _, _u in _uid_theo_file])
        hoa_giai = {"state": st_path, "thay_doi": thay_doi, "ten_file_lech_unit_id": _ten_lech,
                    "da_ghi": bool(thay_doi) and not bool(getattr(a, "dry_run", False))}
    # Mọi cổng đã qua ⇒ MỚI được ghi. Atomic (staging + os.replace): bản cũ `write_text` thẳng, bị kill
    # giữa chừng là để lại bảng master CỤT — đúng rủi ro "write_text chưa atomic" audit đã nêu.
    _write_text_atomic(Path(out_path), json.dumps(merged, ensure_ascii=False, indent=2) + "\n")
    if _st_moi is not None and hoa_giai.get("da_ghi"):
        _write_text_atomic(Path(st_path), json.dumps(_st_moi, ensure_ascii=False, indent=2) + "\n")
    out = dict(nen, ok=not bo_qua, da_ghi=True,
               nguon=merged.get("_nguon"), thieu_o_metadata=merged.get("_thieu_o_metadata"))
    out.update({"bo_qua": bo_qua, "hoa_giai_state": hoa_giai,
                "buoc_ke": "python scripts/rasoat_phuluc.py --in " + out_path
                           + " --out-dir <out-dir>/phuluc"})
    _print_json_or_text(out, True)
    return 0 if not bo_qua else 2


# ── r217 (v1.35.53): SỬA THEO ĐIỂM — `tl doc-patch` ─────────────────────────────────────────────
# Sinh ra từ kết luận lượt rà 6 (27-07): đối chiếu bản kho với bản Công báo cho ND 159 lệch 17 điểm,
# ND 158 lệch 111 điểm, và đo ra **không bản nào trùm bản nào** (bản Công báo mang lỗi riêng «ngưởi»
# = chính VD-34; bản kho mất HAI CÔNG THỨC tính vì công thức là ảnh/equation trong Google Doc).
# ⇒ THAY TRỌN GÓI LÀ ĐÁNH ĐỔI MÙ: sửa được vài điểm thì rước vào lỗi khác. Việc đúng là sửa ĐÚNG
# những điểm đã chứng minh, từng điểm một, có bằng chứng và có đường lùi.

def _docpatch_norm(s):
    """PURE (r217): NFC hoá chuỗi so khớp. Record cache do `normalize_document` ghi đã NFC; chuỗi
    người dùng gõ/copy từ PDF thường NFD ⇒ không chuẩn hoá thì đếm ra 0 và điểm bị từ chối oan."""
    import unicodedata as _ud
    return _ud.normalize("NFC", str(s or ""))


def _docpatch_vung_doc(record, vung):
    """PURE (r217): đọc nội dung MỘT vùng của record. Trả (ok, text, err).
    Vùng hợp lệ: `khoi_dau` · `dieu:<N>` · `phu_luc`. BẮT BUỘC khai vùng — không có chế độ "tìm khắp
    văn bản": một chuỗi chính tả sai thường xuất hiện ở nhiều Điều, sửa mù là sửa nhầm chỗ."""
    d = record if isinstance(record, dict) else {}
    v = str(vung or "").strip()
    if v == "khoi_dau":
        return True, str(d.get("khoi_dau") or ""), ""
    if v == "phu_luc":
        return True, str(d.get("phu_luc") or ""), ""
    m = re.fullmatch(r"dieu:(\d+[a-zđ]*)", v)
    if m:
        arts = d.get("articles") or {}
        k = m.group(1)
        if k not in arts:
            return False, "", "VUNG_KHONG_CO_TRONG_RECORD: dieu:" + k
        return True, str(arts[k] or ""), ""
    return False, "", "VUNG_KHONG_HOP_LE: " + (v or "(trống)") + " — dùng khoi_dau | dieu:<N> | phu_luc"


def _docpatch_vung_ghi(record, vung, text):
    """PURE (r217): ghi nội dung mới vào đúng vùng (trả record ĐÃ sửa tại chỗ)."""
    v = str(vung or "").strip()
    if v == "khoi_dau":
        record["khoi_dau"] = text
    elif v == "phu_luc":
        record["phu_luc"] = text
    else:
        record.setdefault("articles", {})[re.fullmatch(r"dieu:(\d+[a-zđ]*)", v).group(1)] = text
    return record


def _docpatch_ap(record, diem_list):
    """PURE (r217): áp danh sách điểm lên MỘT record cache. KHÔNG đọc/ghi file, KHÔNG in.
    Trả {"ok", "ket_qua": [...], "record": <bản mới>, "delta_chars", "loi": [...]}.

    FAIL-CLOSED TOÀN LÔ: chỉ cần MỘT điểm không thoả thì KHÔNG áp điểm nào. Sửa được nửa lô rồi
    dừng là để lại một bản kho không ai mô tả nổi — tệ hơn hẳn không sửa.

    Mỗi điểm phải khớp ĐÚNG MỘT lần trong vùng đã khai:
      · 0 lần  ⇒ `KHONG_KHOP` — chuỗi sai, hoặc bản kho khác bản người rà đang đọc;
      · >1 lần ⇒ `KHOP_NHIEU_LAN` — sửa cái nào? Máy không được chọn hộ. Thu hẹp bằng cách đưa thêm
        chữ hai bên vào `tim` cho tới khi duy nhất.
    `tim` == `thay` ⇒ từ chối (điểm rỗng nghĩa, chỉ làm nhiễu nhật ký)."""
    import copy as _copy
    rec = _copy.deepcopy(record if isinstance(record, dict) else {})
    ket_qua, loi = [], []
    for i, dm in enumerate(diem_list or []):
        d = dm if isinstance(dm, dict) else {}
        ma = str(d.get("ma") or f"#{i + 1}")
        vung = str(d.get("vung") or "")
        tim, thay = _docpatch_norm(d.get("tim")), _docpatch_norm(d.get("thay"))
        r = {"ma": ma, "vung": vung, "tim": tim, "thay": thay, "ly_do": str(d.get("ly_do") or "")}
        if not tim:
            r["trang_thai"] = "TIM_RONG"
        elif tim == thay:
            r["trang_thai"] = "TIM_BANG_THAY"
        else:
            ok, cur, err = _docpatch_vung_doc(rec, vung)
            if not ok:
                r["trang_thai"] = err
            else:
                n = _docpatch_norm(cur).count(tim)
                r["so_lan_khop"] = n
                r["trang_thai"] = "OK" if n == 1 else ("KHONG_KHOP" if n == 0 else "KHOP_NHIEU_LAN")
                if n == 1:
                    j = _docpatch_norm(cur).find(tim)
                    r["truoc"] = _docpatch_norm(cur)[max(0, j - 60):j]
                    r["sau"] = _docpatch_norm(cur)[j + len(tim):j + len(tim) + 60]
        if r["trang_thai"] != "OK":
            loi.append({"ma": ma, "vung": vung, "trang_thai": r["trang_thai"]})
        ket_qua.append(r)
    if not diem_list:
        loi.append({"ma": "(lô)", "trang_thai": "DANH_SACH_DIEM_RONG"})
    if loi:
        return {"ok": False, "ket_qua": ket_qua, "record": None, "delta_chars": 0, "loi": loi}
    delta = 0
    for r in ket_qua:
        _, cur, _e = _docpatch_vung_doc(rec, r["vung"])
        moi = _docpatch_norm(cur).replace(r["tim"], r["thay"], 1)
        delta += len(r["thay"]) - len(r["tim"])
        _docpatch_vung_ghi(rec, r["vung"], moi)
    st = rec.get("structure")
    if isinstance(st, dict):
        st["khoi_dau_chars"] = len(str(rec.get("khoi_dau") or ""))
        st["phu_luc_chars"] = len(str(rec.get("phu_luc") or ""))
    if isinstance(rec.get("chars"), int):
        rec["chars"] = rec["chars"] + delta
    return {"ok": True, "ket_qua": ket_qua, "record": rec, "delta_chars": delta, "loi": []}


def _docpatch_tim_file(so_hieu, cache_dir):
    """(r217) → danh sách Path record cache khớp số hiệu/alias. Dùng ĐÚNG luật chuẩn hoá của
    `scripts/cache.py::find` để không đẻ ra chiều tra thứ hai; nhiều hơn 1 ⇒ bên gọi fail-CLOSED."""
    key = re.sub(r"[^a-z0-9]+", "-", str(so_hieu or "").lower()).strip("-")
    ra = []
    for f in sorted(Path(cache_dir, "docs").glob("*.json")):
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        cands = [doc.get("so_hieu", ""), doc.get("number_symbol", "")] + list(doc.get("aliases", []) or [])
        if any(re.sub(r"[^a-z0-9]+", "-", str(c).lower()).strip("-") == key for c in cands if c):
            ra.append(f)
    return ra


def _docpatch_sha(p):
    import hashlib as _h
    return _h.sha256(Path(p).read_bytes()).hexdigest()


def _docpatch_cache_dir(a):
    return str(getattr(a, "cache_dir", "") or "").strip() or os.environ.get("TRA_LUAT_CACHE") \
        or os.environ.get("TL_CACHE_DIR") or str(Path(os.path.expanduser("~")) / ".tra_luat_cache")


def cmd_doc_patch(a) -> int:
    """r217 — SỬA CACHE VĂN BẢN THEO ĐIỂM, có nhật ký và đường lùi. DRY mặc định.

    Đây là lệnh GHI. Cổng duyệt = `--apply --confirm yes` (KHÔNG có chế độ ghi ngầm), và trước khi
    ghi luôn tự sao lưu nguyên bản record vào `docs/_doc_patch_bak/`. Hoàn tác: `tl doc-patch
    --undo <run_id> --apply --confirm yes`.

    Vì sao KHÔNG mượn `tl undo`: nhật ký undo hiện có phục vụ registry qua GAS (`reg_upsert`/
    `reg_bulk`) — hoàn tác của nó là ghi lại giá trị ô. Ở đây đối tượng là FILE record cache, hoàn
    tác là chép lại nguyên bản; trộn hai thứ vào một lệnh là mời một lớp lỗi mới.

    Đường lùi có CỔNG: undo chỉ chạy khi file hiện tại còn ĐÚNG sha256 mà lượt patch đã ghi. Khác
    ⇒ từ chối (đã có thay đổi khác chen vào; chép đè bản sao lưu sẽ nuốt luôn thay đổi đó)."""
    cache_dir = _docpatch_cache_dir(a)
    undo_run = str(getattr(a, "undo", "") or "").strip()
    apply_ = bool(getattr(a, "apply", False))
    nen = {"schema": "doc_patch.v1", "cache_dir": cache_dir}

    if undo_run:
        recs = _journal_read(undo_run) or []
        cm = [r for r in recs if r.get("t") == "commit" and r.get("op") == "doc_patch" and r.get("ok")]
        if not cm:
            _print_json_or_text(dict(nen, ok=False, error="UNDO_KHONG_CO_COMMIT_TRONG_JOURNAL",
                                     run_id=undo_run), True)
            return 2
        c = cm[-1]
        tgt, bak = Path(c.get("key") or ""), Path(c.get("bak") or "")
        if not tgt.is_file() or not bak.is_file():
            _print_json_or_text(dict(nen, ok=False, error="UNDO_THIEU_FILE", target=str(tgt),
                                     bak=str(bak), target_con=tgt.is_file(), bak_con=bak.is_file()), True)
            return 2
        sha_now = _docpatch_sha(tgt)
        if sha_now != c.get("sha_sau"):
            _print_json_or_text(dict(nen, ok=False, error="UNDO_FILE_DA_DOI_SAU_KHI_PATCH",
                                     sha_hien_tai=sha_now, sha_luc_patch=c.get("sha_sau"),
                                     fix="đã có thay đổi khác sau lượt patch — chép đè bản sao lưu sẽ "
                                         "nuốt luôn thay đổi đó. Đối chiếu tay với " + str(bak)), True)
            return 2
        if not apply_:
            _print_json_or_text(dict(nen, ok=True, che_do="DRY", run_id=undo_run, target=str(tgt),
                                     bak=str(bak), se_lam="chép bản sao lưu đè lên record",
                                     note="thêm `--apply --confirm yes` để hoàn tác"), True)
            return 0
        if str(getattr(a, "confirm", "") or "") != "yes":
            _print_json_or_text(dict(nen, ok=False, error="NEED_CONFIRM",
                                     note="undo GHI ĐÈ record cache — thêm `--confirm yes`"), True)
            return 2
        rid = _journal_new_run_id("doc-patch-undo")
        _journal_append(rid, {"t": "run_start", "cmd": "doc-patch --undo", "of_run": undo_run})
        _journal_append(rid, {"t": "intent", "op": "doc_patch_undo", "key": str(tgt),
                              "set": {"tu_bak": str(bak)}})
        tgt.write_bytes(bak.read_bytes())
        _journal_append(rid, {"t": "commit", "op": "doc_patch_undo", "key": str(tgt), "ok": True,
                              "sha_sau": _docpatch_sha(tgt)})
        _journal_append(rid, {"t": "run_end", "ok": True, "counts": {"restored": 1}})
        _print_json_or_text(dict(nen, ok=True, che_do="UNDO", run_id=undo_run, journal=rid,
                                 target=str(tgt), sha_sau_undo=_docpatch_sha(tgt),
                                 khop_sha_truoc_patch=_docpatch_sha(tgt) == c.get("sha_truoc")), True)
        return 0

    diem_file = str(getattr(a, "diem", "") or "").strip()
    so_hieu = str(getattr(a, "sohieu", "") or "").strip()
    if not so_hieu or not diem_file:
        _print_json_or_text(dict(nen, ok=False,
                                 error="CAN_SO_HIEU_VA_DIEM: `tl doc-patch <số hiệu> --diem <file.json>`"), True)
        return 2
    if not Path(diem_file).is_file():
        _print_json_or_text(dict(nen, ok=False, error="DIEM_FILE_KHONG_TON_TAI: " + diem_file), True)
        return 2
    try:
        dj = json.loads(Path(diem_file).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        _print_json_or_text(dict(nen, ok=False, error="DIEM_FILE_KHONG_PHAI_JSON: " + str(e)), True)
        return 2
    diem_list = dj.get("diem") if isinstance(dj, dict) else dj
    # Cổng nhầm-văn-bản: file điểm khai số hiệu thì phải khớp số hiệu đang sửa. Một tệp điểm soạn cho
    # ND 159 chạy nhầm lên ND 158 sẽ khớp được vài chuỗi chung — im lặng làm hỏng đúng thứ cần đúng.
    sh_khai = str((dj.get("so_hieu") if isinstance(dj, dict) else "") or "").strip()
    if sh_khai and _rasoat_sohieu_key(sh_khai) != _rasoat_sohieu_key(so_hieu):
        _print_json_or_text(dict(nen, ok=False, error="SO_HIEU_LECH_VOI_FILE_DIEM",
                                 so_hieu_lenh=so_hieu, so_hieu_file_diem=sh_khai), True)
        return 2
    hits = _docpatch_tim_file(so_hieu, cache_dir)
    if len(hits) != 1:
        _print_json_or_text(dict(nen, ok=False,
                                 error="CACHE_KHONG_TIM_THAY" if not hits else "CACHE_IDENTITY_CONFLICT",
                                 so_hieu=so_hieu, ung_vien=[p.name for p in hits]), True)
        return 2
    target = hits[0]
    record = json.loads(target.read_text(encoding="utf-8"))
    kq = _docpatch_ap(record, diem_list)
    nen.update({"so_hieu": so_hieu, "target": str(target), "so_diem": len(diem_list or []),
                "diem_file": diem_file})
    if not kq["ok"]:
        _print_json_or_text(dict(nen, ok=False, error="DIEM_KHONG_AP_DUOC", da_ghi=False,
                                 loi=kq["loi"], ket_qua=kq["ket_qua"],
                                 fix="FAIL-CLOSED toàn lô: không điểm nào được áp. `KHOP_NHIEU_LAN` "
                                     "⇒ thêm chữ hai bên vào `tim` cho tới khi duy nhất; `KHONG_KHOP` "
                                     "⇒ đối chiếu lại bản kho (`tl doc-text <id> --markup mark`)."), True)
        return 2
    if not apply_:
        _print_json_or_text(dict(nen, ok=True, che_do="DRY", da_ghi=False, delta_chars=kq["delta_chars"],
                                 ket_qua=kq["ket_qua"],
                                 note="thêm `--apply --confirm yes` để GHI (tự sao lưu + nhật ký undo)"), True)
        return 0
    if str(getattr(a, "confirm", "") or "") != "yes":
        _print_json_or_text(dict(nen, ok=False, error="NEED_CONFIRM", da_ghi=False,
                                 note="doc-patch GHI ĐÈ record cache — thêm `--confirm yes`"), True)
        return 2
    rid = _journal_new_run_id("doc-patch")
    sha_truoc = _docpatch_sha(target)
    bak_dir = Path(cache_dir, "docs", "_doc_patch_bak")
    bak_dir.mkdir(parents=True, exist_ok=True)
    bak = bak_dir / f"{target.stem}.{rid}.json"
    bak.write_bytes(target.read_bytes())
    _journal_append(rid, {"t": "run_start", "cmd": "doc-patch", "so_hieu": so_hieu,
                          "target": str(target), "bak": str(bak), "so_diem": len(diem_list)})
    _journal_append(rid, {"t": "intent", "op": "doc_patch", "key": str(target),
                          "set": {"diem": [{"ma": r["ma"], "vung": r["vung"]} for r in kq["ket_qua"]],
                                  "bak": str(bak), "sha_truoc": sha_truoc}})
    rec = kq["record"]
    lich_su = (rec.get("doc_patch") or {}).get("lich_su") or []
    lich_su.append({"run_id": rid, "diem_file": diem_file, "so_diem": len(kq["ket_qua"]),
                    "delta_chars": kq["delta_chars"], "sha_truoc": sha_truoc,
                    "diem": [{"ma": r["ma"], "vung": r["vung"], "tim": r["tim"], "thay": r["thay"],
                              "ly_do": r["ly_do"]} for r in kq["ket_qua"]]})
    rec["doc_patch"] = {"lich_su": lich_su}
    # r322 (RAS-18): TẠO `verify_flags` khi record chưa có, thay vì lặng lẽ bỏ cảnh báo. Bản r217
    # ghi có điều kiện `if isinstance(vf, list)` ⇒ record thiếu khoá thì lời khai «hash đã cũ» bốc
    # hơi đúng lúc cần nhất, mà lệnh vẫn rc=0. Cảnh báo biến mất theo hình dạng dữ liệu là fail-OPEN.
    vf = rec.get("verify_flags")
    if not isinstance(vf, list):
        vf = rec["verify_flags"] = []
    vf.append("DOC_PATCH: %d điểm sửa theo điểm (run %s) — `text_hash` vẫn là hash của BẢN NGUỒN "
              "trước khi sửa, KHÔNG tính lại (record không giữ bố cục dòng của bản gốc)."
              % (len(kq["ket_qua"]), rid))
    tmp = target.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(rec, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(target))
    sha_sau = _docpatch_sha(target)
    _journal_append(rid, {"t": "commit", "op": "doc_patch", "key": str(target), "ok": True,
                          "bak": str(bak), "sha_truoc": sha_truoc, "sha_sau": sha_sau})
    _journal_append(rid, {"t": "run_end", "ok": True, "counts": {"diem": len(kq["ket_qua"])}})
    _print_json_or_text(dict(nen, ok=True, che_do="APPLY", da_ghi=True, journal=rid, bak=str(bak),
                             delta_chars=kq["delta_chars"], sha_truoc=sha_truoc, sha_sau=sha_sau,
                             ket_qua=kq["ket_qua"],
                             undo="tl doc-patch --undo " + rid + " --apply --confirm yes"), True)
    return 0
