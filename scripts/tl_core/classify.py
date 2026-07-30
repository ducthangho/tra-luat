# -*- coding: utf-8 -*-
"""tl_core.classify — I9a (v1.34.13): hạ tầng PHÂN LOẠI/tên/tiêu-đề (loai/cat/title_vn/header-facts/strip-accents…) tách NGUYÊN VĂN từ tl.py. Đổi-luật-có-kiểm-soát đã grill (chiến lược I8→I9→I10): infra đa-module nay sống ở tl_core, tl giữ stub; bind REBASE __globals__."""
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
    """REBASE __globals__ từng hàm đã chuyển về namespace SỐNG của tl (khuôn I1-I8)."""
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



def _selected_profile_name(profile: str | None = None, cfg: dict | None = None) -> str:
    cfg = cfg or {}
    return (profile or os.environ.get("TL_PROFILE") or cfg.get("defaultProfile") or DEFAULT_PROFILE).strip() or DEFAULT_PROFILE


def _subject_tokens_for_entry(e: dict) -> set[str]:
    """Token chủ đề để nối luật gốc với luật sửa đổi khi registry thiếu goc/sua_doi."""
    txt = " ".join(str(x or "") for x in (
        _name_tail_key(_entry_name(e)), e.get("title_vn"), e.get("trich_yeu"),
        e.get("nlm_title"), e.get("official_title"), e.get("ten_van_ban"),
    ))
    toks = _token_set(txt)
    return {t for t in toks if t not in {"sua", "doi", "sung", "sdbs", "hop", "nhat"}}


def _verify_header_match(entry: dict, header_text: str) -> dict:
    """CỔNG CHÍNH XÁC: ĐỌC HEADER văn bản → đối chiếu SỐ HIỆU / TIÊU ĐỀ(chủ đề) / LOẠI / CAT khớp registry + tên + thư mục.
    KHÔNG tin metadata suông. Trả {ok, checks:{...bool}, mismatches:[...], header_sohieu:[...]}.
    `ok` = có ÍT NHẤT 1 check áp dụng VÀ mọi check áp dụng đều PASS (dùng làm cổng gán nhãn `tl confirm`)."""
    txt = unicodedata.normalize("NFC", header_text or "")
    head = txt[:6000]
    head_norm = _strip_accents(head).lower()
    full_norm = _strip_accents(txt).lower()
    checks: dict[str, bool] = {}
    mism: list[str] = []
    # 1) SỐ HIỆU trong header phải khớp registry
    reg_sh = _sohieu_key_entry(entry)
    head_shs = sorted({norm_sohieu(m.group(1)) for m in _SOHIEU_RE.finditer(head)})
    if reg_sh:
        ok = (reg_sh in head_shs) or (reg_sh.replace("/", "-").lower() in head_norm.replace("/", "-"))
        # A1 (v1.33.9 — log rà 90/531: header_mismatch_no_proposal=31 ~100% VBHN): số hiệu registry của VBHN
        # mang NĂM TIÊM THÊM theo bất biến NN-YYYY-VBHN-XXX (chống tái dùng số — đó là quy ước CỦA TA), còn văn
        # bản in dạng chính thức KHÔNG NĂM 'Số: NN/VBHN-XXX' → check cũ FAIL HỆ THỐNG với mọi VBHN đã year-fix.
        # Chấp nhận dạng KHÔNG-NĂM tương đương là KHỚP.
        if not ok:
            _m_vy = _VBHN_WITHYEAR_RE.fullmatch(reg_sh)
            if _m_vy:
                _yearless = f"{_m_vy.group(1)}-VBHN-{_m_vy.group(3)}"
                # S-2f (v1.33.15 — ca VBHN_21-2026 BLTTDS, log rà 40): layout VPQH in 'Số: NN/VBHN-VPQH' CHỈ ở
                # KHỐI KÝ CUỐI văn bản (đo thật: vị trí 492k/532k ký tự), đầu văn bản đi thẳng 'BỘ LUẬT TỐ TỤNG
                # DÂN SỰ' → head-6000 không bao giờ thấy. Số hiệu CỦA CHÍNH DOC xuất hiện Ở BẤT KỲ ĐÂU trong
                # văn bản (kể cả dạng không-năm) là corroborate đủ cho check này.
                _full_flat = full_norm.replace("/", "-")
                ok = (_yearless in head_shs) or (_yearless.lower() in head_norm.replace("/", "-")) \
                    or (_yearless.lower() in _full_flat) or (reg_sh.lower() in _full_flat)
        if not ok:
            # v1.33.17 (MERGE nhánh-5 — phần tốt của `tl_changes.patch` qua bundle patch-merged): header format
            # LỎNG 'Số: 47 / 2024 / NĐ - CP' — _SOHIEU_RE lẫn substring-check đều trượt vì separator lạ. So
            # COMPACT chỉ-chữ-số trên 2000 ký tự đầu (đủ chặt: chuỗi số+năm+cơ-quan phải LIỀN NHAU sau nén;
            # số hiệu SAI thật vẫn fail — verify bằng ca 99/2099 control).
            _head_comp = re.sub(r"[^a-z0-9]", "", _strip_accents(head[:2000]).lower())
            _reg_comp = re.sub(r"[^a-z0-9]", "", reg_sh.lower())
            _m_vy4 = _VBHN_WITHYEAR_RE.fullmatch(reg_sh)
            _yl_comp = (re.sub(r"[^a-z0-9]", "", f"{_m_vy4.group(1)}vbhn{_m_vy4.group(3)}".lower())
                        if _m_vy4 else "")
            ok = bool((_reg_comp and _reg_comp in _head_comp) or (_yl_comp and _yl_comp in _head_comp))
        checks["sohieu"] = ok
        if not ok:
            mism.append(f"SOHIEU: registry={reg_sh} không thấy trong header (header={head_shs[:4]})")
    # 2) TIÊU ĐỀ / chủ đề (token tên) xuất hiện đủ trong nội dung
    name = _entry_name(entry)
    # S-2a (v1.33.15 — log rà 40: 4/5 header_mismatch_no_proposal đều FAIL title vì token RÁC): _subject_tokens
    # trên TÊN ĐẦY ĐỦ nhét cả prefix/mảnh-số-hiệu vào chủ đề ('bluat', 'qh13', 'tt44', 'btc') — thứ không thuộc
    # thân văn bản. TAIL-FIRST: chỉ token phần CHỦ ĐỀ sau prefix+sohieu (_name_tail_key); fallback full-name
    # khi tail rỗng (tên trơ) — hành vi cũ.
    toks = _token_set(_name_tail_key(name)) or _subject_tokens(name)
    if toks:
        _ftoks = _token_set(full_norm)
        _full_comp = re.sub(r"[^a-z0-9]+", "", full_norm)
        hit = 0
        for _t in toks:
            if _t in _ftoks:
                hit += 1
                continue
            # S-2d (v1.33.15 — ca VBHN_62-2026 'NhapCanh_XuatCanh' khớp 0/2): token dạng NÉN CamelCase dính liền
            # không bao giờ trùng token có-space trong text — token ≥6 ký tự so SUBSTRING trên text đã nén.
            if len(_t) >= 6 and _t in _full_comp:
                hit += 1
                continue
            # D2 (v1.33.3 — log rà 66×3: 87/2015 'HD_giam_sat_QH_HDND' bị HEADER_MISMATCH 3/4 dù tên ĐÚNG):
            # token VIẾT TẮT trong tên (hdnd/blds/bhxh…) không xuất hiện nguyên dạng trong header viết đầy đủ
            # → tính khớp khi MỌI TỪ của bản mở rộng (_ABBREV_MAP) đều có trong nội dung.
            # S-2c (v1.33.15 — ca ND_47-2024 'CSDL'): bản mở rộng chứa TỪ ≤2 KÝ TỰ ('co','so','du') bị
            # _token_set lọc len≥3 → check cũ `w in _ftoks` KHÔNG BAO GIỜ đậu — so TỪ NGUYÊN VĂN trên text.
            _exp = _ABBREV_MAP.get(_t, "")
            if _exp and all(re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", full_norm)
                            for w in _exp.split()):
                hit += 1
        # D2b: ngưỡng cũ min(4,len) đòi TUYỆT ĐỐI với tên 3-4 token — 1 token lạ (viết tắt ngoài map/chính tả)
        # là FAIL cả check. Lối thoát TỶ LỆ ≥3/4 cho tên ≥4 token; tên ngắn 2-3 token giữ ngưỡng chặt cũ.
        # A1b (v1.33.9 — log rà 90/531): toks CÓ THỂ chỉ còn 1 token (VBHN 'Luat_Ke_toan' → 'luat' stop + 'ke'
        # ngắn bị bỏ, còn mỗi 'toan') mà SÀN max(2,…)=2 > số token → check KHÔNG BAO GIỜ pass = FAIL hệ thống.
        # Sàn phải bị chặn bởi CHÍNH số token đang có.
        _need = min(len(toks), max(2, min(4, len(toks))))
        ok = hit >= _need or (len(toks) >= 4 and hit / len(toks) >= 0.75)
        checks["title"] = ok
        if not ok:
            mism.append(f"TITLE: chủ đề tên không đủ trong nội dung (khớp {hit}/{len(toks)} token)")
    # 3) LOẠI (Luật/NĐ/TT…) — bậc tier suy từ registry phải có từ-loại tương ứng trong header
    rank = _vb_tier_rank(entry)
    loai_words = {5: ("luat", "bo luat", "nghi quyet", "hien phap", "hop nhat"), 4: ("phap lenh", "nghi quyet"),
                  3: ("nghi dinh",), 2: ("thong tu", "quyet dinh")}.get(rank, ())
    if loai_words:
        ok = any(w in head_norm for w in loai_words)
        checks["loai"] = ok
        if not ok:
            mism.append(f"LOAI: header thiếu từ loại bậc {rank} ({'/'.join(loai_words)})")
    # 4) CAT: mã suy từ TÊN phải chứa cat đang gán (tên ↔ thư mục nhất quán)
    # S-10 (v1.33.19) → v1.33.20 (MERGE bundle-20): suy luận qua HÀM CHUNG _header_verify_infer_cats —
    # 3 surface một nguồn, guard 00/23-not-applicable/boundary/omnibus nằm TRONG hàm; check này nay bắt CẢ
    # chiều omnibus/điều-ước NẰM NHẦM folder (infer trả 46/23 ≠ cc → FAIL kèm rule máy-đọc).
    cc = re.sub(r"\D", "", str(_entry_cat(entry)))[:2]
    _inf_list, _inf_rule = _header_verify_infer_cats(entry)
    inferred = {re.sub(r"\D", "", str(c))[:2] for c in (_inf_list or [])}
    inferred.discard("")
    if cc and inferred:
        ok = cc in inferred
        checks["cat"] = ok
        if not ok:
            _why = f"; rule={_inf_rule}" if _inf_rule else ""
            mism.append(f"CAT: cat={_entry_cat(entry)} không khớp suy luận theo tên ({sorted(inferred)}{_why})")
    return {"ok": bool(checks) and all(checks.values()), "checks": checks, "mismatches": mism, "header_sohieu": head_shs}


def _extract_header_facts(head: str) -> dict:
    """G2 (advisory, PURE): trích NGÀY BAN HÀNH ('ngày D tháng M năm Y'→YYYY-MM-DD) + CƠ QUAN từ header. KHÔNG ép vào
    _verify_header_match (giữ nguyên chữ ký + bộ check cũ) — chỉ phục vụ --fix-suggest. Thuần, test offline được."""
    txt = head or ""
    nrm = _strip_accents(txt).lower()
    m = _HEADER_DATE_RE.search(txt)
    issue_date = f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if m else ""
    agency = ""
    for pat, code in _HEADER_AGENCY_PATS:
        if pat in nrm:
            agency = code; break
    if not agency and ("bo truong" in nrm or re.search(r"\bbo\s+(y te|tai chinh|cong an|quoc phong|tu phap|noi vu|"
                                                         r"giao duc|y te|cong thuong|xay dung|giao thong)", nrm)):
        agency = "BO"
    return {"issue_date": issue_date, "agency": agency}


def _clean_subject_text(s: str) -> str:
    """A2: bỏ hậu tố KHÔNG-phải-chủ-đề khỏi tên file khi suy 'subject' cho QT-5 — `_HL<ngày hiệu lực>`, token `goc_…`,
    cụm 'sua doi/suadoi', ngày trơ — để query web KHÔNG thành 'thu do hl2026 07 01 hợp nhất'."""
    s = _strip_goc_token(str(s or ""))
    s = _HL_SUFFIX_RE.sub(" ", s)
    s = re.sub(r"\b(19|20)\d{2}[\s\-/.]\d{1,2}[\s\-/.]\d{1,2}\b", " ", s)   # ngày trơ yyyy-mm-dd
    s = re.sub(r"\bsua\s*doi\b|\bsuadoi\b", " ", s, flags=re.I)
    return re.sub(r"\s+", " ", s).strip()


def _has_diacritics(s: str) -> bool:
    """P0-1 (v1.31.0): chuỗi CÓ DẤU tiếng Việt? (so với bản strip-accents). Subject KHÔNG dấu → query
    site:vbpl/congbao recall kém → cờ QT5_SUBJECT_NO_DIACRITICS nhắc truyền --subject tay / backfill title_vn."""
    s = str(s or "")
    return bool(s) and s != _strip_accents(s)


def _looks_like_filename_title(s: str) -> bool:
    """P0-1 (v1.31.0, từ patch user đã thẩm định): nlm_title/title_vn NHIỀU KHI = chính TÊN FILE
    ('Luat_100-2015-QH13_Bo_Luat_Hinh_su') — KHÔNG phải trích yếu → KHÔNG dùng làm subject QT-5
    (query literal filename tìm ra 0; bằng chứng LIVE 2026-07-03 ca BLHS). Title THẬT có dấu không khớp các mẫu này."""
    s = str(s or "").strip()
    if not s:
        return False
    if re.match(r"^(Luat|Bo_?luat|BL[A-Za-z]{0,3}|VBHN|ND|NQ|TT|QD|PL|CT|KL|HP)[ _.\-]", s):
        return True
    if "_" in s and re.search(r"\d{1,5}-\d{4}-[A-Za-z0-9]+", s):        # cụm số hiệu kiểu file + underscore
        return True
    if s.count("_") >= 2 and re.search(r"QH\d|VBHN|ND-CP|UBTVQH|HDNN|LCT", s, flags=re.I):
        return True
    return False


def _name_tail_pretty(name: str) -> str:
    """P0-1 (v1.31.0, từ patch user): chủ đề human-readable GIỮ hoa/thường (KHÔNG strip dấu, KHÔNG lowercase) —
    query Google tốt hơn tail-key ASCII-lowercase. Bỏ ext, số dài, prefix loại, cụm số hiệu; '_' → space."""
    n = str(name or "")
    n = re.sub(r"\.(docx?|pdf|gdoc|txt|html?)$", "", n, flags=re.I)
    n = re.sub(r"[_ \-]?\d{5,}$", "", n)
    n = re.sub(r"^(Luat|Bo_?luat|BL[A-Za-z]{0,3}|VBHN|ND|NQ|TT|QD|PL|CT|KL|HP)[ _.\-]+", "", n, flags=re.I)
    n = re.sub(r"^\d{1,5}[-_/]\d{4}[-_/][A-Za-z0-9\-]+[ _.\-]*", "", n)
    n = re.sub(r"^\d{1,5}[-_/](?:\d{1,5}[-_/])?(?:VBHN[-_/])?[A-Za-z0-9\-]+[ _.\-]*", "", n, flags=re.I)
    # Review v1.31.0 (finding THẬT): tên VBHN chuẩn `VBHN_<sohieu>_<NĂM>_<chủ đề>` — sau khi bóc sohieu, NĂM đứng
    # đầu lọt vào subject ('2025 Luat Hon nhan…') → bóc thêm 1 lớp năm (chủ đề luật không bao giờ mở đầu bằng năm).
    n = re.sub(r"^(19|20)\d{2}[ _.\-]+", "", n)
    n = n.replace("_", " ")
    return re.sub(r"\s+", " ", n).strip()


def _derive_subject_from_entries(entries: list[dict]) -> str:
    """P0-1 (v1.31.0 — log LIVE 2026-07-03): ĐẢO thứ tự ưu tiên — (1) trích yếu THẬT có dấu từ title_vn/trich_yeu/
    nlm_title (_META_TITLE_KEYS; guard KHÔNG phải tên-file) → (2) tail GIỮ hoa/thường (đọc được hơn tail-key) →
    (3) fallback tail-key ASCII cũ. Trước đây tên file thắng title → query QT-5 literal filename tìm ra 0."""
    for e in sorted(entries, key=_entry_score, reverse=True):
        title = _field_text(e, _META_TITLE_KEYS)
        if title and not _looks_like_filename_title(title) and _subject_tokens(title):
            return title.strip()
        pretty = _clean_subject_text(_name_tail_pretty(_entry_name(e)))
        if pretty and _subject_tokens(pretty) and not re.fullmatch(r"[\d\s]+", pretty):
            return pretty
        tail = _clean_subject_text(_name_tail_key(_entry_name(e)))   # A2: bỏ _HL<ngày>/goc/SuaDoi khỏi subject
        if tail and _subject_tokens(tail):
            return tail
    return ""


def _strip_accents(s: str) -> str:
    s = (s or "").replace("Đ", "D").replace("đ", "d")
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def _entry_name(e: dict) -> str:
    return e.get("name") or e.get("title") or ""


def _nlm_status_known(status: str) -> bool:
    """status NLM HỢP LỆ = họ active (pushed*/synced/active) HOẶC removed (_nlm_status_removed). Rỗng = OK.
    Nhận BIẾN THỂ tiền tố → KHÔNG false-fire NLM_STATUS_MISMATCH trên removed_superseded_by_VBHN v.v."""
    s = (status or "").strip().lower()
    if not s:
        return True
    return s.startswith("pushed") or s.startswith("synced") or s == "active" or _nlm_status_removed(s)


def _nlm_status_write_ok(status: str) -> bool:
    """r179 T1 (ADR-0010 — nlm_status là TỪ VỰNG ĐÓNG ở CỬA GHI): hợp lệ = họ pushed*/synced*/active/
    removed_<lý do> (hậu tố lý do BẮT BUỘC — 'removed' trần không nói vì sao gỡ) + rỗng (route clear).
    KHÁC `_nlm_status_known` (phía ĐỌC/audit khoan dung dữ liệu cũ: nhận thêm trash*/deleted/removed-trần
    — GIỮ NGUYÊN by-design). added/live/ready là từ cũ ngoài từ vựng: backfill-nlm-status nắn added→pushed,
    live→active MỘT LẦN; cửa ghi TỪ CHỐI để sổ không tái nhiễm."""
    s = (status or "").strip().lower()
    if not s:
        return True
    return bool(s.startswith("pushed") or s.startswith("synced") or s == "active"
                or re.match(r"removed_.+", s))


def _name_goc_base_key(name: str) -> str:
    """Số hiệu BẢN GỐC (base) MÃ HOÁ TRONG TÊN VBHN qua token 'goc_<base>' (vd 'Luat_PPP_goc_64-2020-QH14'
    → '64-2020-QH14'; 'NSNN_goc_89-2025-QH15_sdbs_145-2025-QH15' → '89-2025-QH15'). Tên do quy trình đặt tên
    chuẩn hoá ghi ra → nguồn CORROBORATE đáng tin để đối chiếu registry.goc (chống goc bị nhiễm). '' nếu tên không mã hoá."""
    m = _GOC_BASE_RE.search(str(name or ""))
    if not m:
        return ""
    tok = re.split(r"[_\s.\-]sdbs[_\s.\-]", m.group(1), flags=re.I)[0]
    return norm_sohieu(tok.replace("_", "-"))


def _name_key(name: str) -> str:
    s = _strip_accents(name).lower()
    s = re.sub(r"\.(docx?|pdf|gdoc|txt)$", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\b(raw|copy|final|vbqppl|goc|root)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _omnibus_name_text(text: str) -> bool:
    """S-3b (v1.33.16 — MERGE nhánh-4 `_is_omnibus_cat46_name`, giữ lõi ta): pattern omnibus trên TEXT TRẦN
    (tên file / title-scope), không cần entry: 'sua doi N luat' / 'sửa đổi (bổ sung) (một số) (điều của)
    các|nhiều luật' [nới hơn nhánh-4 — bắt cả phrasing thật 'một số điều của các luật'] / cụm sửa-đổi + ≥2
    đề-tài dạng NÉN. KHÔNG thêm topic 'dautucong' của nhánh-4: 'dautu' là SUBSTRING của 'dautucong' → tên
    1-đề-tài 'SuaDoi_Dau_tu_cong' bị đếm 2 = false-omnibus (bug nhánh-4, reject)."""
    n = _strip_accents(str(text or "")).lower().replace("_", " ")
    if not n:
        return False
    if re.search(r"sua[\s]*doi[\s]*\d+[\s]*luat", n):
        return True
    _spaced = re.sub(r"[^a-z0-9]+", " ", n).strip()
    if re.search(r"\bsua\s*doi(?:\s+bo\s+sung)?(?:\s+mot\s+so)?(?:\s+dieu)?(?:\s+cua)?\s+(?:cac|nhieu)\s+luat\b",
                 _spaced):
        return True
    if re.search(r"sua[\s]*doi|suadoi", n):
        # v1.32.2 (log rà 69 — ca 57-2024 vẫn REVIEW lặp dù là omnibus): registry goc/sua_doi CHƯA backfill →
        # nhánh ≥2-ref câm. Đếm ĐỀ TÀI trong TÊN sau cụm sửa-đổi; so DẠNG NÉN (tên kiểu SuaDoi_QuyHoach_DauTu
        # strip xong dính liền 'quyhoach dautu' — 'dau tu' có-space không khớp).
        _ncomp = re.sub(r"[^a-z0-9]+", "", n)
        _topics = ("quy hoach", "dau tu", "dau thau", "ppp", "doi tac cong tu", "thue", "hai quan",
                   "tai san cong", "quang cao", "giao duc", "luat khac")
        return sum(1 for t in _topics if t.replace(" ", "") in _ncomp) >= 2
    return False


def _omnibus_name_evidence(e: dict) -> bool:
    """S-3 (v1.33.15, PURE): bằng chứng omnibus ĐỘC LẬP VỚI CAT — pattern text (_omnibus_name_text) HOẶC cụm
    sửa-đổi + ≥2 ref goc-sua_doi registry. Dùng khi CHÍNH cat 46 đang bị auditor nghi vấn: lấy 'đang ở 46' làm
    bằng chứng 'thuộc rổ 46' là lập luận vòng — cat-audit/CAT_LIKELY_WRONG phải gọi hàm này, KHÔNG _is_omnibus_entry."""
    n = _strip_accents(str(_entry_name(e) or "")).lower().replace("_", " ")
    if _omnibus_name_text(n):
        return True
    if re.search(r"sua[\s]*doi|suadoi", n):
        refs = _goc_keys(e) | _ref_tokens(_field_text(e, _REF_KEYS))
        return len(refs) >= 2
    return False


def _is_omnibus_entry(e: dict) -> bool:
    """A3 (v1.32.0, PURE — log rà 77 Luật): entry là luật SỬA NHIỀU LUẬT (omnibus)? Bản chất omnibus = AMENDS_OTHER
    — KHÔNG BAO GIỜ có VBHN của chính nó ⇒ amendment-gate phải đi nhánh riêng (không REVIEW vì 'thiếu VBHN'/mồ côi).
    Nhận diện: cat 46 (rổ sửa-nhiều-luật) HOẶC bằng chứng theo tên/ref (_omnibus_name_evidence — S-3 v1.33.15)."""
    if str(_entry_cat(e) or "").startswith("46"):
        return True
    return _omnibus_name_evidence(e)


def _name_subset_match(q: str, hay: str) -> bool:
    """Khớp tên theo TẬP TOKEN PHÂN BIỆT (bỏ doctype/số hiệu/dấu qua _token_set): query tokens ⊆ entry tokens.
    Bắt ca 'Luật Bảo hiểm xã hội [hợp nhất]' ↔ 'VBHN_19-VPQH_Bao_hiem_xa_hoi' mà substring LIỀN không bắt (vì
    'luat'/'vbhn'/'19'/'vpqh' chèn giữa). Yêu cầu ≥2 token phân biệt để tránh khớp quá rộng 1 token.
    LOẠI TRỪ CHÉO BHXH↔BHYT↔BHTN: token phân biệt ('y tế'/'xã hội') ngắn <3 nên _token_set bỏ → 'bảo hiểm y tế'
    rút còn {bao,hiem} ⊆ entry BHXH → phải chặn bằng _disc_conflict (nếu không sẽ kéo nhầm như BHYT↔BHXH)."""
    qt = _token_set(q)
    if len(qt) < 2 or not (qt <= _token_set(hay)):
        return False
    return not _disc_conflict(q, hay)


def _compact_phrase(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", _strip_accents(str(s or "")).lower())


def _name_phrase_match(q: str, hay: str) -> bool:
    """Khớp cụm tên sau khi bỏ loại văn bản/số hiệu.

    Vá âm-tính-giả kiểu query "Luật Dân số" trong khi canonical là
    `Luat_113-2025-QH15_Dan_so`: token-subset bỏ mất token ngắn "số",
    còn substring liền bị số hiệu chen giữa.
    """
    qtail = _name_tail_key(q)
    htail = _name_tail_key(hay)
    if not qtail or not htail or _disc_conflict(qtail, htail):
        return False
    qc, hc = _compact_phrase(qtail), _compact_phrase(htail)
    if len(qc) >= 4 and (qc == hc or qc in hc or hc in qc):
        return True
    qt, ht = _token_set(qtail), _token_set(htail)
    # reg_query_name_matchall: query 1-token sau khi bỏ stopword (vd "Dân SỐ"→{dan}, "Phí"→{phi}) là TẬP-CON của MỌI
    # tên chứa token đó → match-all giả (reg-query --name "Dân số" trả 87). Yêu cầu ≥2 token cho nhánh subset;
    # query 1-token đã được nhánh cụm-nén ở trên xử lý (qc in hc, vd "danso" ⊆ "…danso") nên vẫn bắt đúng bản Dân số.
    return bool(qt and len(qt) >= 2 and qt <= ht)


def _name_content_tokens(s: str) -> set[str]:
    """Token CHỦ ĐỀ thực (bỏ token mã-số-hiệu, viết tắt đã expand, cụm 'hopnhat' dính) để so khớp tên CHẶT."""
    out = set()
    for t in _token_set(s):
        if _NAME_CODE_TOK.match(t) or t in _ABBREV_MAP:
            continue
        t = t.replace("hopnhat", "")
        if t:
            out.add(t)
    return out


def _name_strong_match(q: str, name: str) -> bool:
    """Khớp tên CHẶT (đủ chủ đề), KHÔNG phải khớp-mờ tập-con: dùng để gate canonical khi tên va chạm token.

    Chống ca 'Luật Dân số' kéo nhầm 'Luật Dân chủ ở cơ sở' / 'Bộ luật Dân sự', 'Luật Việc làm' kéo
    'NLĐ đi làm việc ở nước ngoài', 'Luật Phí và lệ phí' kéo 'Học phí'. Hai cửa:
      (1) cụm chủ đề (đã bỏ loại VB/số hiệu) khớp LIỀN theo dạng nén ('danso' ⊆ 'danso', phân biệt 'dansu');
      (2) token chủ đề thực BẰNG NHAU (≥2 token) — KHÔNG nhận tập-con để tránh entry có token phân biệt thừa
          ('chu'/'co' của Dân chủ cơ sở) lọt; token ngắn <3 ('số'/'sự'/'y') đã rơi nên (1) là chốt chính."""
    qtail, htail = _name_tail_key(q), _name_tail_key(name)
    if not qtail or not htail or _disc_conflict(qtail, htail):
        return False
    qc, hc = _compact_phrase(qtail), _compact_phrase(htail)
    if len(qc) >= 4 and qc in hc:
        return True
    qt, ht = _name_content_tokens(qtail), _name_content_tokens(htail)
    return bool(qt and len(qt) >= 2 and qt == ht)


def _name_subject_text(s: str) -> str:
    """Chuẩn hóa phần CHỦ ĐỀ thật của truy vấn/tên, bỏ từ điều hướng kiểu 'hợp nhất/mới nhất/vbhn'."""
    tail = _clean_subject_text(_name_tail_key(s))
    tail = re.sub(r"\b(van\s+ban\s+hop\s+nhat|hop\s+nhat|moi\s+nhat|vbhn)\b", " ", tail, flags=re.I)
    return re.sub(r"\s+", " ", tail).strip()


def _name_subject_match(q: str, e: dict) -> bool:
    """A1: True khi query THEO TÊN có chủ đề KHỚP entry (abbrev-aware qua _disc_conflict/_name_content_tokens) —
    dùng để KHÔNG chốt canonical theo token CHUNG ('Bộ luật Lao động'→'Dân chủ cơ sở'). qsub rỗng (query không có
    chủ đề rõ) → True (không chặn)."""
    qsub = _name_subject_text(q)
    if not qsub:
        return True
    hay = " ".join([_name_subject_text(_entry_name(e)), _field_text(e, _META_TITLE_KEYS)])
    if not hay or _disc_conflict(qsub, hay):
        return False
    qc = _compact_phrase(qsub)
    ec = _compact_phrase(hay)
    if len(qc) >= 4 and qc in ec:
        return True
    qt = _name_content_tokens(qsub)
    et = _name_content_tokens(hay)
    return bool(qt and len(qt) >= 2 and qt <= et)


def _normalize_loai(s: str) -> str:
    """Map biến thể `loai` → enum chuẩn (đầy đủ tiếng Việt). Giữ nguyên (để gắn cờ) nếu không nhận diện.
    MERGE nhánh-3 v1.33.14: nhãn KÉP 'Quyết định/Quy định'/'A và B' → lấy VẾ ĐẦU ngay TẠI NGUỒN (mọi caller
    hưởng: register-normalize, backfill-loai, reg-query --loai, corpus-audit) thay vì vá lẻ từng chỗ."""
    raw = str(s or "").strip()
    if not raw:
        return raw
    for _sep in ("/", "\\", "|", " và ", " va "):
        if _sep in raw:
            raw = raw.split(_sep)[0].strip()
            break
    if raw in _LOAI_CANON_VALUES:
        return raw
    key = re.sub(r"[^a-z0-9]+", " ", _strip_accents(raw).lower()).strip()   # gộp mọi ký tự lạ (._-()/…) → space
    return _LOAI_CANON.get(key) or _LOAI_CANON.get(key.replace(" ", "")) or raw


def _infer_loai(name: str, sohieu: str = "") -> str:
    """KH1 Pha 1.5 (PURE, test offline): suy `loai` CHUẨN (∈ _LOAI_CANON_VALUES) cho dòng registry thiếu loai, từ
    TIỀN TỐ TÊN chuẩn hoá (Luat_/BLDS_/ND_/TT_/NQ_…) + mã cơ quan trong SỐ HIỆU. '' nếu không chắc. VBHN → 'Văn bản
    hợp nhất' (bất kể QH gốc). Tên-trước (corpus chuẩn hoá tên) rồi số-hiệu fallback (raw)."""
    nm = _strip_accents(str(name or "")).upper()
    sh = _strip_accents(str(sohieu or "")).upper()
    if "VBHN" in nm or "VBHN" in sh:
        return "Văn bản hợp nhất"
    # 1) tiền tố/khóa TÊN (corpus dùng Luat_/BLDS_/ND_/TT_/NQ_…)
    if any(t in nm for t in ("BO_LUAT", "BO LUAT", "BOLUAT", "BLUAT", "BLDS", "BLHS", "BLLD", "BLTTHS", "BLTTDS")):
        return "Bộ luật"   # MERGE nhánh-3 v1.33.14: +BLUAT (prefix chuẩn sinh của standardize_name — P1-3 v1.33.12)
    if "TTLT" in nm:
        return "Thông tư liên tịch"
    if nm.startswith("ND_") or "NGHI_DINH" in nm or "NGHI DINH" in nm:
        return "Nghị định"
    if nm.startswith("TT_") or "THONG_TU" in nm or "THONG TU" in nm:
        return "Thông tư"
    if nm.startswith("NQ_") or "NGHI_QUYET" in nm or "NGHI QUYET" in nm:
        return "Nghị quyết"
    if nm.startswith("QD_") or "QUYET_DINH" in nm or "QUYET DINH" in nm:
        return "Quyết định"
    if nm.startswith("PL_") or "PHAP_LENH" in nm or "PHAP LENH" in nm:
        return "Pháp lệnh"
    if nm.startswith("HP_") or "HIEN_PHAP" in nm or "HIEN PHAP" in nm:
        return "Hiến pháp"
    if nm.startswith("LUAT_") or nm.startswith("LUAT "):
        return "Luật"
    # v1.34.31 (rà corpus 2026-07-11): điều ước quốc tế + văn kiện Đảng KHÔNG có số hiệu VN chuẩn → suy từ TIỀN TỐ
    # tên chuẩn (CU_/CPTPP_/EVFTA_ và KL_/CT_/HD_). backfill-loai cũ bỏ trống 38 dòng corpus vì thiếu các prefix này.
    if nm.startswith("CU_") or "CONG_UOC" in nm or "CONG UOC" in nm:
        return "Công ước"
    if nm.startswith("CPTPP") or nm.startswith("EVFTA") or "DIEU_UOC" in nm or "DIEU UOC" in nm:
        return "Điều ước quốc tế"
    if nm.startswith("KL_") or "KET_LUAN" in nm:
        return "Kết luận"
    if nm.startswith("CT_") or "CHI_THI" in nm:
        return "Chỉ thị"
    if nm.startswith("HD_") or "HUONG_DAN" in nm:
        return "Hướng dẫn"
    # v1.34.40 B.2: prefix loại VĂN BẢN THƯỜNG (profile) — thiếu thì blank-over-guess không nhận được bằng
    # chứng name_prefix. CHỈ PREFIX ĐẦU TÊN (không substring giữa tên — 'VK_DH_XIV_Bao_cao' dị thể phải để
    # manual, doctrine r93). PL_ giữ nguyên = Pháp lệnh (quy ước corpus).
    if nm.startswith(("KH_", "KE_HOACH")):
        return "Kế hoạch"
    if nm.startswith(("TB_", "THONG_BAO")):
        return "Thông báo"
    if nm.startswith(("CV_", "CONG_VAN")):
        return "Công văn"
    if nm.startswith(("TTR_", "TO_TRINH")):
        return "Tờ trình"
    if nm.startswith(("DA_", "DE_AN")):
        return "Đề án"
    if nm.startswith(("BC_", "BAO_CAO")):
        return "Báo cáo"
    if nm.startswith(("PHU_LUC", "PHULUC")):
        return "Phụ lục"
    # v1.34.41 B.2 GĐ2 (grill D7): CTr_ đã sống trên corpus (CTr_02-2026-CTr-BCDTW) — 'CTR_' không đụng 'CT_'
    # (ký tự thứ 3 khác). Các mã mới khác (QDi/QC/TTri/DL) CHƯA gặp tên thật → gặp thật mới thêm (nếp D6).
    if nm.startswith(("CTR_", "CHUONG_TRINH")):
        return "Chương trình"
    # 2) fallback: mã cơ quan trong SỐ HIỆU
    if "ND-CP" in sh:
        return "Nghị định"
    if "TTLT" in sh:
        return "Thông tư liên tịch"
    if "/TT-" in sh or "TT-B" in sh:
        return "Thông tư"
    if "NQ-" in sh:
        return "Nghị quyết"
    if "QD-" in sh:
        return "Quyết định"
    if "-KL-" in sh:      # v1.34.31: văn kiện Đảng theo số hiệu (NN-KL-TW / NN-CT-TW / NN-HD-VPTW)
        return "Kết luận"
    if "-CT-" in sh:
        return "Chỉ thị"
    if "-HD-" in sh:
        return "Hướng dẫn"
    if "PL-" in sh or "/UBTVQH" in sh:
        return "Pháp lệnh"
    if re.search(r"QH\d", sh) or "/QH" in sh or "LCT-HDNN" in sh:
        return "Luật"
    return ""


def _loai_is_noncanonical(e: dict) -> bool:
    """True nếu `loai` có giá trị NHƯNG khác enum chuẩn (cần chuẩn hoá). Rỗng → bỏ qua (không tính)."""
    loai = str(e.get("loai") or "").strip()
    return bool(loai) and loai not in _LOAI_CANON_VALUES


def _name_tail_key(name: str) -> str:
    n = _strip_accents(str(name or "")).lower()
    n = re.sub(r"\.(docx?|pdf|gdoc|txt|html?)$", "", n, flags=re.I)
    n = re.sub(r"[_ -]?\d{5,}$", "", n)
    # S-2b (v1.33.15 — log rà 40: 'BLuat_100-2015-QH13_Bo_luat_hinh_su' KHÔNG bị strip prefix+sohieu → tail =
    # NGUYÊN tên, token chủ đề dính rác 'bluat'/'qh13'): nhận họ prefix Bộ-luật (BLuat chuẩn sinh P1-3 v1.33.12
    # + BLDS/BLHS/BLLD/BLTTDS… legacy) qua bl[a-z]{2,6}; giữ 'bl' trần cho 'BL_'.
    n = re.sub(r"^(luat|bo[_ .-]?luat|bl[a-z]{2,6}|bl|vbhn|nd|nq|tt|qd|pl|ct|kl|hp)[ _.-]+", "", n)
    n = re.sub(r"^\d{1,5}[-_/]\d{4}[-_/][a-z0-9-]+[ _.-]*", "", n)
    n = re.sub(r"^\d{1,5}[-_/](?:\d{1,5}[-_/])?(?:vbhn[-_/])?[a-z0-9-]+[ _.-]*", "", n)
    n = re.sub(r"[^a-z0-9]+", " ", n)
    # B.3 (v1.33.19 — log rà v1.33.18: 'Thu_do_HL2026-07-01' → token rác 'hl2026' làm title-check 1/2 fail):
    # hậu tố NGÀY-HIỆU-LỰC _HL<date> không phải chủ đề — strip SAU khi đổi separator thành space
    # (trước đó '_hl…' dính underscore, \b của _HL_SUFFIX_RE không bắt được).
    n = _HL_SUFFIX_RE.sub(" ", n)
    return re.sub(r"\s+", " ", n).strip()


def _title_flags(e: dict, covered_sohieu: set | None = None) -> list[str]:
    """Cờ rủi ro từ log chạy thật: tên file có thể hẹp/sai so với metadata quan hệ VBQPPL.
    r253 `covered_sohieu` (tùy chọn, từ `_chunk_covered_sohieu(entries)`): số hiệu đã PHỦ bằng chunk con
    `__partNN` trên NLM → KHÔNG bắn CORPUS_TRUE_NOT_ON_NLM cho dòng canonical. Mặc định None = giữ NGUYÊN
    hành vi cũ (20+ caller không có row-set vẫn gọi 1 tham số như trước)."""
    flags = []
    name = _entry_name(e)
    cat = _entry_cat(e)
    if _entry_nlm(e) and (not name) and (not _entry_sohieu(e)) and _bad_cat(cat):
        flags.append("NLM_GHOST_SOURCE")
    nlm_status = str(e.get("nlm_status") or "").strip().lower()
    if _entry_nlm(e) and nlm_status and not _nlm_status_known(nlm_status):   # nhận họ removed_*/pushed*/synced (hết false-fire)
        flags.append("NLM_STATUS_MISMATCH")
    if _entry_on_nlm_live(e) and not _entry_nlm_notebook_id(e):
        flags.append("NLM_NOTEBOOK_ID_MISSING")
    if _entry_corpus_true(e) and (not _entry_on_nlm_live(e)) and not _is_quarantine_cat(cat) \
            and not nlm_status.startswith("removed") \
            and not (covered_sohieu and norm_sohieu(_entry_sohieu(e)) in covered_sohieu
                     and not _is_chunk_part_name(name)):
        # nlm_status 'removed*' (vd removed_superseded_by_VBHN/removed_below_nd) = đã gỡ khỏi NLM CÓ CHỦ ĐÍCH
        # (VBHN thay / dưới ngưỡng) → KHÔNG báo thiếu NLM. Chỉ flag khi THẬT SỰ thiếu (status rỗng/khác).
        # r253: cũng KHÔNG báo khi số hiệu đã PHỦ bằng chunk con `__partNN` trên NLM (dòng canonical cố ý
        # không mang source_id) — mời nạp lại bản đầy đủ = NHÂN ĐÔI luật. `and not _is_chunk_part_name(name)`:
        # chính dòng part mà rớt khỏi NLM thì VẪN phải kêu, không được tự phủ cho mình.
        flags.append("CORPUS_TRUE_NOT_ON_NLM")
    if _entry_is_draft(e):
        flags.append("DRAFT_NOT_EFFECTIVE")
    if _bad_cat(cat):
        flags.append("ORPHAN_CAT")
    if not (_entry_sohieu(e) or _parse_sohieu_from_name(name)):
        flags.append("MISSING_SOHIEU")
    raw_name = (not _name_is_template_or_appendix(name)) and bool(re.search(r"(^|[/_ -])\d{2,4}[_-]\d{4}[_-]", name))
    if raw_name and not _entry_nlm(e):
        flags.append("RAW_NAME_NOT_NLM")
    if _name_is_template_or_appendix(name):
        return flags

    tail = _name_tail_key(name)
    flags.extend(_vbhn_metadata_flags(e, tail))
    rel_text = _field_text(e, _REF_KEYS)
    refs = _ref_tokens(rel_text)
    if (not _is_vbhn_entry(e)) and len(refs) >= 2 and tail and not any(h in tail for h in _OMNIBUS_TITLE_HINTS):
        flags.append("OMNIBUS_NARROW_TITLE_CHECK")

    # B.5 (v1.33.19 — log rà v1.33.18: TITLE_METADATA_MISMATCH oan cho 123-2025/71-2020 vì nlm_title là TÊN
    # FILE CỤT 'Luat_123-2025-QH15_GD'/'Luat_71-2020-QH14' — token hoá chỉ còn 'qh15'/'qh14', không bao giờ
    # giao với tail chủ đề): metadata DẠNG-TÊN-FILE (_looks_like_filename_title — P0-1 v1.31.0 sinh ra đúng
    # cho việc này) KHÔNG phải trích yếu → so TAIL-vs-TAIL thay vì so thô; tail meta rỗng = không có bằng
    # chứng, KHÔNG buộc tội. Misname THẬT (meta là tên/trích yếu văn bản KHÁC chủ đề) vẫn bắt như cũ.
    if tail:
        _meta_plain, _meta_fname = [], []
        for _k in _META_TITLE_KEYS:
            _v = str(e.get(_k) or "").strip()
            if not _v:
                continue
            (_meta_fname if _looks_like_filename_title(_v) else _meta_plain).append(_v)
        meta_tokens = _token_set(" ".join(_meta_plain)) | _token_set(" ".join(_name_tail_key(v) for v in _meta_fname))
        tail_tokens = _token_set(tail)
        if len(tail_tokens) >= 2 and meta_tokens and not (tail_tokens & meta_tokens):
            flags.append("TITLE_METADATA_MISMATCH")
    return flags


def _is_treaty_entry(e: dict) -> bool:
    """P1-8 (v1.31.0, PURE): Công ước/Điều ước quốc tế (CU_ILO-105, Cong_uoc_…) — sohieu RỖNG là HỢP LỆ
    (điều ước KHÔNG có số hiệu VBQPPL) → tách LỚP RIÊNG: không tính orphan, không đòi sohieu/tên chuẩn Luat_*.
    B.7 (v1.33.19 — log rà v1.33.18: orphans=16 vẫn gộp CPTPP_Chuong_19/EVFTA_Chuong_13): nhận thêm prefix
    FTA/chương điều ước (CPTPP/EVFTA/RCEP/UKVFTA/DUQT_/ILO-) — cũng là điều ước, không có số hiệu VBQPPL."""
    n = _strip_accents(str(_entry_name(e) or "")).lower()
    lo = _strip_accents(str(e.get("loai") or "")).lower().strip()
    return bool(re.match(r"^(cu[_\-]|cong[_ ]?uoc|dieu[_ ]?uoc|hiep[_ ]?dinh|cong[_ ]?ham|duqt[_\-]"
                         r"|cptpp|evfta|rcep|ukvfta|ilo[_\-]|unesco[_\-])", n)
                or lo in ("cong uoc", "dieu uoc", "dieu uoc quoc te", "hiep dinh"))


def _name_is_template_or_appendix(name: str) -> bool:
    """Không parse số đầu tên Mẫu_/PL_ thành số hiệu văn bản.

    Bug chạy thật: các tài liệu làm việc kiểu `Mẫu_04...`, `PL_05...` bị cụm hóa
    thành số hiệu giả `04/2025/...`, khiến hygiene đề xuất QUARANTINE nhầm.
    Chỉ bỏ lớp parse từ TÊN; nếu registry có `sohieu` thật thì vẫn dùng.
    """
    n = unicodedata.normalize("NFC", name or "").strip()
    return bool(_TEMPLATE_PREFIX_RE.search(n))


def _parse_sohieu_from_name(name: str) -> str:
    if _name_is_template_or_appendix(name):
        return ""
    raw = name or ""
    m = _RAW_SOHIEU_RE.search(raw)
    if m:
        return m.group(0)
    # 4D (v1.33.30 — MERGE bundle-29, SÂU hơn suppress-flag v1.33.29 ta): VBHN SỐ KÉP/nhiều gốc trong TÊN
    # ('VBHN_73-82-ND-CP_…') là số hiệu HỢP LỆ của bản hợp nhất nhóm văn bản — regex chuẩn không bắt → mọi
    # consumer (MISSING_SOHIEU/sweep/corpus-audit) đều oan. GUARD: chỉ mở rộng khi tên có dấu hiệu VBHN,
    # không nhận nhầm chuỗi số thường ('Bao_cao_2024-2025').
    if re.search(r"(?i)(^|[_\s-])VBHN([_\s-]|$)", raw) or "van ban hop nhat" in _ascii_lower(raw):
        m2 = re.search(r"(?i)(?<![0-9A-Za-zĐđ])(\d{1,4})[-_/](\d{1,4})[-_/]"
                       r"((?:NĐ|ND|TT|QD|QĐ|NQ|PL|VBHN|VPQH|UBTVQH|LCT|HDNN)"
                       r"(?:[-_/](?:CP|QH\d*|UBTVQH\d*|TTG|TW|VPQH|BTC|BCA|BQP|BNV|BYT|NHNN|BTTTT|HDNN\d*)){0,2})"
                       r"(?=$|[_\s.-])", raw)
        if m2:
            return m2.group(0)
    return ""


def _doc_subject_key(e: dict) -> str:
    """Khoá CHỦ ĐỀ văn bản theo NAME-TAIL (bỏ năm + bỏ refs) — để gom bản NHÂN ĐÔI CÙNG văn bản dù metadata
    refs khác nhau (vd canonical có goc 45/2019 còn bản quarantine bare thì không). Khác `_vbhn_subject_key`
    (vốn trộn refs nên tách nhầm same-doc). Dùng cho #3/#4: phân biệt trùng-cùng-document vs reuse-khác-document."""
    tail = _name_tail_key(_entry_name(e))
    tail = re.sub(r"\b(?:20\d{2}|19\d{2})\b", " ", tail)
    toks = _subject_tokens(tail)
    return " ".join(sorted(toks)) if toks else (re.sub(r"\s+", " ", tail).strip() or "UNKNOWN")


def _cat_bare_full_variants(entries: list[dict]) -> dict:
    """D (v1.33.6 — log rà: tồn tại ĐỒNG THỜI folder '05' & '05_Can_bo_cong_chuc_vien_chuc', '32' &
    '32_Thong_tin_bao_chi_xuat_ban' → nhóm/đếm theo cat phân mảnh, recat/cat-audit dễ bỏ sót; bare '32' còn
    chứa văn bản làm việc lọt corpus): prefix 2-số nào có CẢ nhãn TRƠ ('NN') lẫn nhãn ĐỦ TÊN ('NN_...') =
    biến thể cần gộp về folder đủ tên (`tl recat`). Trả {prefix: [các nhãn]}."""
    by_pfx: dict[str, set] = {}
    for e in entries:
        c = str(_entry_cat(e) or "").strip()
        m = re.match(r"^(\d{2})(?:_|$)", c)
        if m:
            by_pfx.setdefault(m.group(1), set()).add(c)
    return {p: sorted(v) for p, v in by_pfx.items() if len(v) > 1 and p in v}


def _subject_tokens(s: str) -> set[str]:
    return {t for t in _token_set(_strip_accents(s or "").lower()) if len(t) >= 3 and t not in _STOP_TOKENS}


def _entry_subject_text(e: dict) -> str:
    # KHÔNG gồm `cat` (tên FOLDER pháp điển, vd "02_Bao_hiem") — nó là NHÃN LƯU TRỮ, không phải chủ đề văn bản; gộp
    # vào sẽ khiến MỌI entry trong folder "02_Bao_hiem" khớp "bảo hiểm" (NHNN/Bảo vệ sức khoẻ misfile → sscore 60 giả).
    return " ".join([
        _entry_name(e), str(e.get("title_vn") or ""), str(e.get("trichyeu") or e.get("trich_yeu") or ""),
        str(e.get("tukhoa") or e.get("keywords") or ""), str(e.get("nlm_title") or ""),
    ])


def _disc_conflict(q_text: str, e_text: str) -> bool:
    """True nếu query & entry CÙNG nhóm tiền-tố-chung nhưng token PHÂN BIỆT khác hẳn (loại trừ chéo BHXH↔BHYT…).
    CHUẨN HOÁ dấu phân cách (_-./ → space) vì tên file dùng underscore: 'bao_hiem_xa_hoi' ≠ 'bao hiem' nếu không chuẩn hoá."""
    def _norm(s: str) -> str:
        return re.sub(r"[\s_\-./]+", " ", _strip_accents(_expand_abbrev(s)).lower())
    qa, ea = _norm(q_text), _norm(e_text)
    for shared, discs in _SUBJECT_DISC_GROUPS:
        if shared in qa and shared in ea:
            qd = {i for i, alts in enumerate(discs) if any(a in qa for a in alts)}
            ed = {i for i, alts in enumerate(discs) if any(a in ea for a in alts)}
            if qd and ed and not (qd & ed):    # mỗi bên có discriminator riêng, KHÔNG giao → khác bản chất
                return True
    return False


def _subject_score(e: dict, subject: str) -> int:
    if not subject:
        return 0
    if _disc_conflict(subject, _entry_subject_text(e)):    # BHXH vs BHYT… → KHÔNG cùng chủ đề dù chung "bảo hiểm"
        return 0
    qk = _name_key(subject)
    ek = _name_key(_entry_subject_text(e))
    score = 0
    if qk and (qk in ek or ek in qk):
        score += 80
    qs, es = _subject_tokens(subject), _subject_tokens(_entry_subject_text(e))
    if qs:
        ov = len(qs & es)
        # CHỐNG NHIỄU TỪ-PHỔ-BIẾN: token overlap KHÔNG đủ tin nếu chỉ trùng từ thường (bảo/hội/nhà/nước…). Chỉ cho
        # điểm đầy đủ khi entry chứa CỤM-ĐẦU PHÂN BIỆT của chủ đề ('bảo hiểm'='baohiem') — nếu không, 'Bảo đảm/bảo hộ' +
        # 'hội' ở từ-khoá Luật Xuất bản khớp 'bảo…hội' giả (sscore 40 → lọt vbhn_candidates relation-check). Mở viết tắt.
        head = re.sub(r"[^a-z0-9]", "", _strip_accents(subject).lower())[:7]
        ek_compact = re.sub(r"[^a-z0-9]", "", _strip_accents(_expand_abbrev(_entry_subject_text(e))).lower())
        if len(head) < 5 or head in ek_compact:                  # có cụm đầu phân biệt / chủ đề quá ngắn → tính đủ
            score += min(60, int(60 * ov / max(1, len(qs))))
        elif ov >= len(qs):                                      # không cụm đầu nhưng khớp TRỌN token → điểm vừa
            score += min(45, int(45 * ov / max(1, len(qs))))
        # else: chỉ trùng từ-phổ-biến lẻ → 0 điểm (loại Xuất bản/Người cao tuổi/Thanh niên/Công đoàn khỏi chủ đề BHXH)
    return score


def _discover_classify(folders: list[dict], root_files: list[dict], profiles: dict, vbt_id: str = "") -> dict:
    """B (PURE, test offline) + P1 MARKER-FIRST (v1.34.22, ADR-0003): đối chiếu thư-mục-thật-trên-Drive vs
    config.profiles + marker `tra_luat_profile.json` → buckets:
    configured (trong config; kèm marker_status ok/missing/broken/drift) / adoptable (marker HỢP LỆ nhưng chưa
    vào config → gợi ý `profile-sync --apply`, hết heuristic) / broken_marker (marker có nhưng đọc/validate lỗi)
    / unregistered_profile (có registry|manifest riêng, KHÔNG marker → gợi ý profile-adopt) / empty_folder /
    plain_folder + misplaced_root_assets (registry/manifest Ở GỐC Van_ban_thuong — ca NQ36) + orphaned
    (config có, Drive không thấy — tên cũ config_only).
    folders: [{id,name,items:[...], marker?, marker_error?}] — items đã gộp con trực tiếp + con của _meta."""
    profiles = profiles or {}
    by_root = {str((p or {}).get("rootFolderId") or "").strip(): n
               for n, p in profiles.items() if str((p or {}).get("rootFolderId") or "").strip()}
    known_asset_ids = {str((p or {}).get(k) or "").strip()
                       for p in profiles.values() for k in ("registryDocId", "manifestId")
                       if str((p or {}).get(k) or "").strip()}
    rows, unregistered, empty, misplaced, adoptable, broken = [], [], [], [], [], []
    folder_ids = {str(f.get("id") or "") for f in (folders or [])}
    for f in folders or []:
        items = f.get("items") or []
        kinds = {}
        for it in items:
            kinds.setdefault(_discover_item_kind(it), []).append(it)
        reg = kinds.get("registry") or []
        man = kinds.get("manifest") or []
        marker = f.get("marker") if isinstance(f.get("marker"), dict) else None
        marker_err = f.get("marker_error")
        m_ok, m_errs = (_marker_validate(marker) if marker else (False, []))
        in_cfg = by_root.get(str(f.get("id") or ""))
        marker_status = None
        if in_cfg:
            status = "configured"
            if marker and m_ok:
                _mdiffs = _marker_diff(marker, profiles.get(in_cfg) or {})
                marker_status = "drift" if _mdiffs else "ok"
            elif marker or marker_err:
                marker_status = "broken"
            else:
                marker_status = "missing"
        elif marker and m_ok:
            status = "adoptable"
        elif marker or marker_err:
            status = "broken_marker"
        elif reg or man:
            status = "unregistered_profile"
        elif not items:
            status = "empty_folder"
        else:
            status = "plain_folder"
        row = {"folder_id": f.get("id"), "folder_name": f.get("name"), "status": status,
               "profile": in_cfg, "n_items": len(items),
               "registry": [{"id": x.get("id"), "name": x.get("name")} for x in reg],
               "manifest": [{"id": x.get("id"), "name": x.get("name")} for x in man],
               "registry_nonsheet": [{"id": x.get("id"), "name": x.get("name")}
                                     for x in (kinds.get("registry_nonsheet") or [])]}
        if marker_status:
            row["marker_status"] = marker_status
            if marker_status == "missing":
                row["suggest"] = "tl profile-backfill-markers --apply  (sinh marker từ config — ADR-0003)"
        if status == "adoptable":
            row["marker_profile"] = str(marker.get("profile") or "")
            row["suggest"] = (f"tl profile-sync --apply  (marker '{row['marker_profile']}' → config, "
                              "một chiều — hết heuristic)")
            adoptable.append(row)
        elif status == "broken_marker":
            row["marker_error"] = str(marker_err or ";".join(m_errs))
            row["suggest"] = ("marker hỏng/thiếu field — nếu profile này có trong config: "
                              "`tl profile-backfill-markers --profile-name <p> --force`; nếu không: sửa tay qua adopt.")
            broken.append(row)
        elif status == "unregistered_profile":
            slug = _profile_file_slug(str(f.get("name") or ""))
            row["suggest"] = (f"tl profile-adopt --name {slug} --folder {f.get('id')}"
                              + (f" --registry {reg[0]['id']}" if reg else "")
                              + (f" --manifest {man[0]['id']}" if man else ""))
            unregistered.append(row)
        elif status == "empty_folder":
            row["suggest"] = f"trash folder {f.get('id')} (vỏ rỗng — phục hồi được từ Trash; xác nhận với người dùng trước)"
            empty.append(row)
        rows.append(row)
    for it in root_files or []:
        kind = _discover_item_kind(it)
        if kind in ("registry", "manifest", "registry_nonsheet") and str(it.get("id") or "") not in known_asset_ids:
            misplaced.append({"id": it.get("id"), "name": it.get("name"), "kind": kind,
                              "note": "registry/manifest nằm Ở GỐC Van_ban_thuong (lạc chỗ — vi phạm bất biến layout). "
                                      "Adopt bằng --registry/--manifest rồi `profile-doctor --fix` move vào thư mục profile."})
    orphaned = []
    for n in sorted(profiles):
        if n == DEFAULT_PROFILE:
            continue
        rid = str((profiles.get(n) or {}).get("rootFolderId") or "").strip()
        if rid and rid != str(vbt_id or "") and rid not in folder_ids:
            orphaned.append({"profile": n, "rootFolderId": rid,
                             "note": "profile trong config nhưng KHÔNG thấy thư mục tương ứng dưới Van_ban_thuong "
                                     "(root ngoài VBT, đã trash, hoặc quét bị cap?)."})
    return {"folders": rows, "unregistered": unregistered, "empty_folders": empty, "adoptable": adoptable,
            "broken_markers": broken, "misplaced_root_assets": misplaced, "orphaned": orphaned}


def _clean_ref_name_phrase(name: str) -> str:
    """Cắt phần PROSE chuyển-tiếp lẫn vào name_phrase, chỉ giữ phần đầu là tên/loại văn bản thật ('' nếu toàn prose)."""
    n = (name or "").strip(" -–—\t")
    m = _REF_PROSE_RE.search(n)
    if m:
        n = n[:m.start()].strip(" -–—\t")
    return n


def _is_raw_no_gdoc_name(name: str) -> bool:
    """Entry là FILE THÔ (chưa convert GDoc native) nếu tên có đuôi .docx/.doc/.pdf/.html… (GDoc native KHÔNG có đuôi)."""
    return bool(_RAW_EXT_RE.search(str(name or "")))


def _load_subject_clusters() -> dict:
    global _SUBJECT_CLUSTERS_CACHE
    if _SUBJECT_CLUSTERS_CACHE is None:
        p = Path(__file__).resolve().parent.parent / "references" / "subject_clusters.json"
        try:
            _SUBJECT_CLUSTERS_CACHE = json.loads(p.read_text(encoding="utf-8"))
        except FileNotFoundError:
            _SUBJECT_CLUSTERS_CACHE = {"clusters": {}}
        except Exception as e:   # B6: file CÓ nhưng KHÔNG parse (cắt cụt/NUL do mount) → CẢNH BÁO, không im lặng
            sys.stderr.write(f"[tl] ⚠ subject_clusters.json KHÔNG parse được ({type(e).__name__}: {e}) — cụm sẽ "
                             f"RỖNG; ĐỪNG kết luận 'không có cụm'. Re-sync/sửa references/subject_clusters.json.\n")
            _SUBJECT_CLUSTERS_CACHE = {"clusters": {}, "_parse_error": str(e)}
    return _SUBJECT_CLUSTERS_CACHE


def _norm_cat(cat: str) -> str:
    """Chuẩn hóa mã cat: số 1 chữ số → zero-pad ('9'→'09'); QUARANTINE giữ nguyên."""
    c = (cat or "").strip()
    return ("0" + c) if c.isdigit() and len(c) == 1 else c


def _is_valid_cat_value(v: str) -> bool:
    """`cat` HỢP LỆ cho registry = mã số trong taxonomy 45+2, HOẶC tên folder chuẩn (vd '30_Thi_hanh_an'),
    HOẶC QUARANTINE/rỗng. CHẶN folder RÁC gõ tay (vd '30_To_chuc_bo_may_nha_nuoc' = số 30 ghép tên của cat 35).
    Thiếu taxonomy → trả True (không false-block)."""
    v = (v or "").strip()
    if v in ("", "QUARANTINE"):
        return True
    pd = _load_phapdien()
    if not pd:
        return True
    folders = {(info or {}).get("folder") for info in pd.values()}
    return v in folders or v in set(pd.keys()) or _norm_cat(v) in set(pd.keys())


def _ascii_lower(s: str) -> str:
    """Hạ chữ + bỏ dấu tiếng Việt (Đ→D), để so khớp tên không phụ thuộc dấu/biến thể."""
    s = (s or "").replace("Đ", "D").replace("đ", "d")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def _infer_cats(name: str) -> list:
    """Suy các mã chủ đề từ TÊN văn bản theo _CAT_KEYWORDS (tín hiệu mạnh). Trả list mã khớp."""
    s = _ascii_lower(name)
    return sorted({c for c, kws in _CAT_KEYWORDS.items() if any(k in s for k in kws)})


def _cat_taxonomy() -> set:
    """Tập mã cat HỢP LỆ (45 chủ đề + 00 Đảng + 46 sửa-nhiều-luật + QUARANTINE). Dùng kiểm 'cat ∈ 45+2'."""
    codes = set(_load_phapdien().keys())
    codes |= set((_load_linhvuc().get("chude") or {}).keys())
    codes |= {"QUARANTINE"}
    return {c for c in codes if c}


def _alias_cat_pairs() -> list:
    """N3 (v1.31.1): cặp (alias_ascii, cat2) từ linhvuc_phapdien.chude[].alias + slug — LONGEST-FIRST (đặc thù
    thắng chung: 'dau tu cong' > 'dau tu'), bỏ alias <5 ký tự + alias quá chung (_ALIAS_TOO_GENERIC). Cache module."""
    global _ALIAS_CAT_PAIRS
    if _ALIAS_CAT_PAIRS is None:
        pairs = []
        for code, ent in ((_load_linhvuc().get("chude") or {})).items():
            ent = ent if isinstance(ent, dict) else {}
            c2 = re.sub(r"\D", "", str(code))[:2].zfill(2)
            if not c2.strip("0") and c2 != "00":
                continue
            for al in list(ent.get("alias") or []) + [str(ent.get("slug") or "").replace("_", " ")]:
                al = _strip_accents(str(al or "")).lower().strip()
                if len(al) >= 5 and al not in _ALIAS_TOO_GENERIC:
                    pairs.append((al, c2))
        pairs.sort(key=lambda x: len(x[0]), reverse=True)
        _ALIAS_CAT_PAIRS = pairs
    return _ALIAS_CAT_PAIRS


def _expected_cat_from_alias(subject_text: str) -> tuple[str, str]:
    """N3 (v1.31.1 — cat_audit_strict.py phiên rà 68 Luật, thẩm định): CAT KỲ VỌNG từ alias pháp điển khớp CHỦ ĐỀ
    (tail-pretty + title_vn), longest-match whole-word. BOUNDARY-GUARD trước: 'vốn nhà nước/đầu tư công/ngân sách'
    → ('','') — nhường _cat_boundary_rule (chống over-fire ca 68-2025 'đầu tư vốn NN'→34 mà đúng là 26).
    Trả (cat2, alias_bằng_chứng) hoặc ('','')."""
    s = _strip_accents(str(subject_text or "")).lower()
    if not s.strip():
        return "", ""
    if re.search(r"\bvon nha nuoc\b|\bdau tu cong\b|\bngan sach\b", s):
        return "", ""
    # v1.31.2 (FP thật phiên rà 2026-07-03 — Luật CNTT ở cat 03 bị alias 'cong nghe'(19) kéo nhầm): CNTT = chủ đề 03
    # ĐÃ XÁC MINH pháp điển (doctrine SKILL §0.13: CNTT/dữ liệu/CSDL về 03; AI/công nghiệp công nghệ số mới TẠM 19).
    # Trả POSITIVE 03 (mạnh hơn defer-im-lặng của script tham khảo: bắt được cả ca Luật CNTT nằm SAI cat khác).
    if re.search(r"\bcong nghe thong tin\b", s):
        return "03", "cong nghe thong tin"
    for al, c2 in _alias_cat_pairs():
        if re.search(r"\b" + re.escape(al) + r"\b", s):
            return c2, al
    return "", ""


def _infer_cats_text(text: str, top: int = 5) -> list:
    """G3: suy chủ đề từ NỘI DUNG (phạm vi điều chỉnh/Điều 1) theo alias CHÍNH THỨC (linhvuc_phapdien.chude[].alias),
    KHÔNG chỉ theo tên. Trả [(code, score, [alias_khớp])] giảm dần; score = tổng SỐ-TỪ alias khớp (cụm dài thắng nhiễu
    đơn-từ). Khớp WHOLE-WORD (\\b) → 'nuoc'/'hoi' không lọt giữa từ khác. 00/46/QUARANTINE xử ở _cat_boundary_rule."""
    s = _ascii_lower(text or "")
    if not s:
        return []
    scored = []
    for code, meta in (_load_linhvuc().get("chude") or {}).items():
        if code in ("00", "46", "QUARANTINE"):
            continue
        hits, score = [], 0
        for al in (meta.get("alias") or []):
            a = _ascii_lower(al).strip()
            if len(a) < 3:
                continue
            if re.search(r"\b" + re.escape(a) + r"\b", s):
                hits.append(al); score += len(a.split())
        if hits:
            scored.append((code, score, hits))
    scored.sort(key=lambda x: (x[1], len(x[2])), reverse=True)
    return scored[:top]


def _distinct_target_luat_subjects(s: str) -> int:
    """v1.34.39 (audit 2026-07-13 FP: Luat_26-2018 SuaDoi TDTT + Luat_75-2025 SuaDoi Quảng cáo bị đề xuất →46):
    scope suy-cat GHÉP nhiều biến thể tiêu đề của CÙNG một luật (tail + title_vn + khối tiêu đề) → đếm token
    `luat` ≥3 luôn thoả dù chỉ sửa MỘT luật đích. Đếm đúng = số CHỦ ĐỀ PHÂN BIỆT đứng sau token 'luat'
    (bỏ stopword sửa-đổi/bổ-sung, lấy 2 từ đầu để các biến thể dài-ngắn của cùng chủ đề gộp một). PURE."""
    subs = set()
    for m in re.finditer(r"\bluat\s+((?:[a-z]+\s+){0,3}[a-z]+)", s or ""):
        w = re.sub(r"\b(sua|doi|bo|sung|mot|so|dieu|cua|nay|va|hien|hanh|khac|lien|quan)\b", " ", m.group(1))
        w = " ".join(re.sub(r"\s+", " ", w).strip().split()[:2])
        if w:                       # stopword đã strip — còn gì là chủ đề (kể cả tên ngắn 'Luật A/B' fixture)
            subs.add(w)
    return len(subs)


def _cat_boundary_rule(text: str) -> tuple:
    """G3: ÉP quy_tac_ranh_gioi (linhvuc_phapdien.quy_tac_ranh_gioi) cho các trường hợp BẮT BUỘC dễ gán nhầm.
    Trả (code, rule_text) hoặc (None, None). Chạy trên TÊN+NỘI DUNG đã gộp (ascii). Thứ tự ưu tiên: Đảng →
    sửa-≥2-luật → BHXH/BHYT → đầu-tư-công/hải-quan → điều-ước. (đầu tư KINH DOANH → 34 để _infer_cats_text lo.)"""
    s = _ascii_lower(text or "")
    if not s:
        return (None, None)
    if any(k in s for k in ("ban chap hanh trung uong", "bo chinh tri", "ban bi thu",
                            "nghi quyet trung uong", "van kien dai hoi", "dang cong san", "bch trung uong")):
        return ("00", "Văn bản Đảng → 00 (ngoài pháp điển 01-46)")
    # S-3b (v1.33.16 — MERGE nhánh-4): nhận CẢ dạng NÉN 'SuaDoi_QuyHoach_DauTu_PPP_DauThau' (_omnibus_name_text)
    # → cat-audit đề xuất ĐƯA VÀO 46 khi omnibus nằm nhầm folder khác. GUARD hơn nhánh-4: VBHN KHÔNG BAO GIỜ
    # ép 46 (VBHN cat theo LUẬT ĐÍCH — kể cả VBHN của luật-sửa, tên có SuaDoi + nhiều đề tài).
    # v1.34.39: `len(findall 'luat')>=3` cũ đếm token LẶP trên scope ghép nhiều biến thể tiêu đề của CÙNG 1 luật
    # → sửa-MỘT-luật cũng bị ép 46 (FP audit 2026-07-13: 26-2018 TDTT, 75-2025 Quảng cáo). Nay: tín hiệu dương
    # tường minh ('cac/nhieu luat', 'sua doi N luat') HOẶC ≥2 CHỦ ĐỀ LUẬT PHÂN BIỆT sau token 'luat'.
    # v1.35.67 (r231): rổ 46 = "LUẬT sửa đổi ≥2 luật" ⇒ theo định nghĩa chỉ LUẬT/BỘ LUẬT mới vào được.
    # Guard cũ chỉ chặn VBHN, nên hồ sơ Luật BHXH bị đề xuất đẩy `ND_233-2025-ND-CP`, `ND_212-2025-ND-CP`
    # và cả một CÔNG VĂN (`CV_10593-NHNo-ALCO`) vào 46 — chỉ vì phần căn cứ của Nghị định trích ≥8 số hiệu
    # LUẬT, đủ kích `_distinct_target_luat_subjects >= 2`. Nhánh omnibus lại chạy TRƯỚC nhánh BHXH→02 nên
    # nuốt luôn. Nay: tên mang tiền tố doctype KHÁC luật (ND_/TT_/QD_/NQ_/CT_/CV_/BC_/TTr_/PL_/VBT_/DUTHAO_)
    # thì KHÔNG BAO GIỜ ép 46.
    _non_luat_prefix = re.match(r"^\s*(nd|tt|qd|nq|ct|cv|bc|ttr|pl|vbt|duthao|cu|scan)[_\s-]", s)
    if (not s.lstrip().startswith("vbhn")) and ("van ban hop nhat" not in s) and (not _non_luat_prefix) \
            and (_omnibus_name_text(s) or ("sua doi" in s and (
                "cac luat" in s or "nhieu luat" in s
                or re.search(r"sua doi\D{0,25}\b\d+\s+luat\b", s)
                or _distinct_target_luat_subjects(s) >= 2))):
        return ("46", "Luật sửa ≥2 luật → 46 (xác minh số luật ở Điều 1; linhvuc theo luật đích)")
    if any(k in s for k in ("bao hiem xa hoi", "bao hiem y te", "bao hiem that nghiep")):
        return ("02", "BHXH/BHYT → 02 (Bảo hiểm), KHÔNG vào 20 dù gắn lao động")
    if "dau tu cong" in s or "von dau tu cong" in s:
        return ("26", "Đầu tư công (vốn NSNN) → 26, KHÔNG 34 (đầu tư kinh doanh)")
    if "hai quan" in s:
        return ("26", "Hải quan → 26 (tài chính nhà nước), KHÔNG 33 (thuế/phí)")
    if any(k in s for k in ("dieu uoc quoc te", "cong uoc quoc te", "thoa thuan quoc te")):
        return ("23", "Điều ước/Công ước quốc tế → 23")
    return (None, None)


def _subject_sig(name: str) -> str:
    """Chữ ký 'chủ đề' của tên: bỏ đuôi + doctype + số hiệu/năm + cơ quan TRUNG ƯƠNG (qh/cp/tw/nd/tt/nq…),
    GIỮ cơ quan bộ (bnv/byt/btc…) + từ chủ đề (phu_luc/sua_doi/treem…). Dùng để phân biệt dup thật vs phụ-lục/khác-cơ-quan."""
    s = _ascii_lower(re.sub(r"\.(docx?|pdf)$", "", name or ""))
    s = re.sub(r"\b(vbhn|vpqh|ubtvqh\d*|qh\d*|nd|cp|tt|nq|qd|ct|pl|tw|ttg|lctn|blds?|luat|bo|nghidinh|thongtu|quyetdinh|chithi|nghiquyet|hopnhat|goc)\b", " ", s)
    s = re.sub(r"\d", " ", s)
    return re.sub(r"[^a-z]", "", s)


def _cat_reg_label(code: str) -> str:
    """P1-1 (v1.33.12): nhãn ĐỦ canonical `NN_Ten` để ghi registry (phap_dien_45.folder — khớp cat-list).
    QUARANTINE/không có folder → giữ nguyên mã."""
    code = _norm_cat(code)
    return str((_load_phapdien().get(code) or {}).get("folder") or code)


def _resolve_cat_folder_impl(g, code: str, cats: dict, root_id: str | None, folder_name: str | None):
    """LÕI resolve folder cat (PURE-ish, testable với FakeG — MERGE nhánh-3 v1.33.14, contract-verified:
    list/info/rename/mkdir+parentId đều có trong API_CONTRACT). Thứ tự:
      (1) root_id có → LIST con: khớp TÊN CANONICAL chính xác → dùng luôn; nếu chỉ có ĐÚNG 1 folder mã-trơ
          cùng prefix 2-số (ca '05' vs '05_Can_bo…') → RENAME về canonical rồi dùng (gộp thật sự — mkdir-by-name
          của v1.33.12 tạo folder mới song song, folder trơ vẫn ôm file); ≥2 ứng viên mờ → dùng cái đầu,
          KHÔNG rename (mơ hồ — người vận hành gộp tay).
      (2) config.categories[code] → best-effort rename về canonical (info + rename) rồi dùng.
      (3) mkdir(name=canonical, parentId=root nếu có) find-or-create."""
    cat_key = code.split("_")[0] if "_" in code else code
    if root_id and folder_name:
        try:
            _items = [it for it in (g.get("list", folderId=root_id).get("items") or [])
                      if it.get("type") == "folder"]
            _exact = [it for it in _items if (it.get("name") or "") == folder_name]
            if _exact:
                return _exact[0].get("id"), False
            _bare = [it for it in _items
                     if (m := re.match(r"^(\d{2})(?:\D|$)", it.get("name") or "")) and m.group(1) == cat_key]
            if len(_bare) == 1:
                _fid = _bare[0].get("id")
                try:
                    g.get("rename", fileId=_fid, name=folder_name)
                    print(f"[tl] gộp folder: '{_bare[0].get('name')}' → '{folder_name}' (canonical, giữ fileId)",
                          file=sys.stderr)
                except Exception as _re:  # noqa: BLE001
                    print(f"[tl] ⚠ không rename được folder {_fid}: {_re}", file=sys.stderr)
                return _fid, False
            if len(_bare) > 1:
                print(f"[tl] ⚠ {len(_bare)} folder cùng prefix {cat_key} — dùng '{_bare[0].get('name')}', "
                      f"KHÔNG tự rename (mơ hồ, gộp tay).", file=sys.stderr)
                return _bare[0].get("id"), False
        except Exception as _le:  # noqa: BLE001
            print(f"[tl] resolve_cat_folder list lỗi ({_le}) — rơi xuống config/mkdir.", file=sys.stderr)
    if isinstance(cats, dict) and cat_key in cats:
        _fid = cats[cat_key]
        if folder_name:
            try:
                _actual = ((g.get("info", fileId=_fid) or {}).get("file") or {}).get("name")
                if _actual and _actual != folder_name:
                    g.get("rename", fileId=_fid, name=folder_name)
                    print(f"[tl] gộp folder (config-map): '{_actual}' → '{folder_name}'", file=sys.stderr)
            except Exception:  # noqa: BLE001
                pass
        return _fid, False
    if not folder_name:
        return None, False
    try:
        mk = g.get("mkdir", name=folder_name, **({"parentId": root_id} if root_id else {}))
        return mk.get("folderId"), bool(mk.get("created"))
    except Exception:  # noqa: BLE001
        return None, False


def _resolve_cat_folder(g, code: str):
    """Trả (folderId, created) cho mã cat — P1-2 v1.33.12 (canonical-name-first) + MERGE nhánh-3 v1.33.14
    (inherit-aware, root-aware, RENAME folder trơ về canonical thay vì tạo song song). Lõi ở
    `_resolve_cat_folder_impl` (testable)."""
    code = _norm_cat(code)
    cfg = None
    for p in _config_candidates(os.environ.get("TL_CONFIG_PATH")):
        if p and Path(p).exists():
            cfg = _read_json_file(p)
            if cfg:
                break
    prof = (_profiles_from_config(cfg).get(_active_profile()) or {}) if cfg else {}
    cats = prof.get("categories", {}) if cfg else {}
    if isinstance(cats, str) and cats == "inherit":
        # MERGE nhánh-3: categories='inherit' → cây của profile mặc định (doctrine §12).
        prof = _profiles_from_config(cfg).get((cfg or {}).get("defaultProfile", DEFAULT_PROFILE)) or {}
        cats = prof.get("categories", {}) or {}
    pd = _load_phapdien()
    folder_name = (pd.get(code) or {}).get("folder")
    if not folder_name and code == "QUARANTINE":
        folder_name = "QUARANTINE"
        if isinstance(cats, dict) and cats.get("QUARANTINE"):
            return cats["QUARANTINE"], False
    return _resolve_cat_folder_impl(g, code, cats if isinstance(cats, dict) else {},
                                    prof.get("rootFolderId"), folder_name)


def _title_sentence_case(s: str) -> str:
    """U2 (v1.31.2, PURE): IN HOA → câu thường tiếng Việt NHƯNG GIỮ token có số/'/'/ngoặc ('(HIV/AIDS)', 'CT06')
    — script tham khảo dùng `s[1:].lower()` trần làm hỏng cả các token này lẫn tên riêng viết tắt."""
    words = _ZERO_WIDTH_RE.sub("", str(s or "")).split()   # v1.33.37: strip BOM/zero-width (ca QD_671)
    out = []
    for i, w in enumerate(words):
        keep = bool(re.search(r"[\d/()\[\]]", w))
        w2 = w if keep else w.lower()
        if i == 0 and w2 and not keep:
            w2 = w2[0].upper() + w2[1:]
        out.append(w2)
    return " ".join(out)


def _title_block_from_text(text: str) -> tuple[str, str]:
    """U2 (v1.31.2 — từ log LIVE 22/22 + script tham khảo, LÀM LẠI parser vì bản gốc lỗi: cap 4 dòng → cụt
    'HIV/AIDS'/'…quy phạm pháp', match 'LUẬT' trước 'BỘ LUẬT' → 91/2015 thành 'Luật Dân sự' SAI LOẠI, casing
    `.lower()` trần phá token): bóc TRÍCH YẾU từ KHỐI TIÊU ĐỀ toàn văn — dòng LOẠI IN HOA đứng riêng
    ('BỘ LUẬT'/'LUẬT'/…) → gom CÁC dòng chủ đề IN HOA kế tiếp (không cap cứng; dừng ở Căn cứ/CHƯƠNG/Điều/kẻ ngang)
    → sentence-case bảo toàn token đặc biệt. Trả (kind_chuẩn, subject) hoặc ('','')."""
    lines = [ln.strip() for ln in str(text or "").splitlines()[:80]]
    for i, ln in enumerate(lines):
        m = _TITLE_BLOCK_KIND_RE.match(ln)
        if not m:
            continue
        kind = _normalize_loai(m.group(1))
        subj_lines = []
        for nxt in lines[i + 1:i + 9]:
            if not nxt:
                if subj_lines:
                    break               # đã có chủ đề, gặp dòng trống = hết khối
                continue
            if _TITLE_BLOCK_STOP_RE.match(nxt):
                break
            # dòng chủ đề = chủ yếu IN HOA (cho phép số/ngoặc/phẩy); dòng thường (Quốc hội khóa…, ngày…) → dừng
            _letters = [c for c in nxt if c.isalpha()]
            if _letters and sum(1 for c in _letters if c.isupper()) / len(_letters) >= 0.8:
                subj_lines.append(nxt)
            else:
                break
        subj = re.sub(r"\s+", " ", " ".join(subj_lines)).strip(" ,;")
        if kind in _LOAI_CANON_VALUES and subj and len(subj) >= 3:
            return kind, _title_sentence_case(subj)
    return "", ""


def _title_vn_from_header(header_text: str, entry: dict) -> tuple[str, str]:
    """P0-1 (v1.31.0, PURE): TRÍCH YẾU CÓ DẤU từ header → giá trị cột title_vn ('<Loại> <Chủ đề>', vd
    'Luật Phòng, chống bệnh truyền nhiễm'). Trả (title, skip_reason) — title RỖNG khi KHÔNG tự tin:
    NO_DIACRITICS (header OCR mất dấu/subject từ tên file — ghi vào chỉ nhân bản rác ASCII) / BOILERPLATE /
    NO_SUBJECT. KHÔNG đoán — dòng skip sửa tay qua `tl register --title-vn`.
    ★ U2 (v1.31.2): TIER-1 = khối tiêu đề IN HOA (_title_block_from_text — log LIVE chứng minh nguồn đúng,
    `--dieu 1` trả nhầm khoản phạm-vi); miss mới rơi về _doc_subject_for_name (tier-2 cũ)."""
    header_text = _ZERO_WIDTH_RE.sub("", header_text or "")   # v1.33.37: strip BOM/zero-width TRƯỚC khi bóc (phủ cả 2 tier)
    kind, subj_tb = _title_block_from_text(header_text)
    if kind and subj_tb and _has_diacritics(subj_tb) and not _subject_is_boilerplate(subj_tb):
        return f"{kind} {subj_tb}", ""
    info = _classify_doc_header(header_text or "", _entry_name(entry))
    subj = _doc_subject_for_name(header_text or "", info)
    if not subj:
        return "", "NO_SUBJECT"
    if _subject_is_boilerplate(subj):
        return "", "BOILERPLATE"
    subj = subj.strip()
    if subj.isupper():
        subj = _title_sentence_case(subj)  # U2: giữ token số/(…) — trước dùng .capitalize() trần
    if not _has_diacritics(subj):
        return "", "NO_DIACRITICS"
    loai = _normalize_loai(str(info.get("loai") or entry.get("loai") or "")).strip()
    if loai and loai in _LOAI_CANON_VALUES and not _strip_accents(subj).lower().startswith(_strip_accents(loai).lower()):
        return f"{loai} {subj}", ""
    return subj, ""


def _title_vn_from_tukhoa(tukhoa: str, name: str) -> str:
    """N2 (v1.31.1 — backfill_trichyeu.py phiên rà, thẩm định + vá 2 lỗi họ TỰ BÁO): bóc '(Bộ luật|Luật) <chủ đề
    CÓ DẤU>' từ field tukhoa sẵn có (tiêu đề Điều đầu — NHIỄU: 'Luật Thi' cụt, đuôi '…và các luật có liên quan').
    Guard: cắt heading-giữa-câu + đuôi liên từ + CROSS-CHECK token với TÊN FILE qua _token_set (ĐÃ expand viết tắt
    — hết false-reject CNTT↔'công nghệ thông tin' họ gặp) + boilerplate + PHẢI có dấu. Tier-2 offline RẺ (0 call);
    header (`backfill-title-vn` mặc định) vẫn là tier-1 chất lượng."""
    m = _TUKHOA_TITLE_RE.search(str(tukhoa or ""))
    if not m:
        return ""
    kind = "Bộ luật" if _strip_accents(m.group(1)).lower().startswith("bo") else "Luật"
    subj = m.group(2).strip().rstrip(",")
    subj = _TUKHOA_HEADING_SPLIT_RE.split(subj)[0].strip()             # cắt ở heading-mới giữa câu ('… Điều 2 Giải thích')
    words = subj.split()
    while words and words[-1].lower().strip(",") in _TUKHOA_TAIL_JUNK:  # cắt đuôi liên từ
        words.pop()
    subj = " ".join(words).strip(" ,")
    if len(subj) < 3 or _subject_is_boilerplate(subj) or not _has_diacritics(subj):
        return ""       # subj phải TỰ có dấu (kind 'Luật' luôn có dấu — check trên subj mới có nghĩa)
    if not (_token_set(subj) & _token_set(_name_tail_key(name))):
        return ""       # không trùng token tên file (kể cả sau expand viết tắt) → nghi méo/nhầm luật khác — bỏ
    return f"{kind} {subj[0].upper()}{subj[1:]}"


def _title_vn_from_plan(plan: dict) -> str:
    """N1 (v1.31.1 — 'fix gốc' log phiên rà: bắt trích yếu CÓ DẤU tại thời điểm INGEST, không vá post-hoc):
    title_vn từ auto-plan ingest (analyzer ĐÃ đọc header/probe-text sẵn — 0 call thêm). Cùng chuẩn giá trị với
    _title_vn_from_header; '' khi không tự tin (không dấu/boilerplate) — KHÔNG đoán."""
    cls = (plan or {}).get("classification") or {}
    subj = str(cls.get("title") or "").strip()
    if not subj or _subject_is_boilerplate(subj) or not _has_diacritics(subj):
        return ""
    loai = _normalize_loai(str(cls.get("loai") or "")).strip()
    if loai and loai in _LOAI_CANON_VALUES and not _strip_accents(subj).lower().startswith(_strip_accents(loai).lower()):
        return f"{loai} {subj}"
    return subj


def _backfill_titlevn_candidates(entries: list, force: bool = False) -> list[dict]:
    """P0-1 (v1.31.0, PURE): dòng cần backfill title_vn — corpus=true, row_kind own/overflow (bỏ ref),
    title_vn RỖNG hoặc (force) title_vn hiện tại là TÊN-FILE (_looks_like_filename_title) / không dấu."""
    out = []
    for e in entries or []:
        if not _entry_corpus_true(e) or _entry_row_kind(e) == "ref":
            continue
        cur = str(e.get("title_vn") or "").strip()
        if cur and not force:
            continue
        if cur and force and _has_diacritics(cur) and not _looks_like_filename_title(cur):
            continue                       # title_vn đã là trích yếu thật → không đè kể cả --force-refresh
        out.append({"drive_id": _entry_drive_id(e), "name": _entry_name(e), "title_vn_cur": cur, "entry": e})
    return out


def _profile_title_from_header(text: str, fallback: str = "") -> str:
    # r179 T4 (đo file thật): BỎ BOM đầu file (.txt/.html đọc utf-8 giữ ﻿ → regex noise `^\s*` KHÔNG
    # khớp, quốc hiệu thành title rác).
    # r201 FIX-B (grill 24-07 đêm C3, ca sống 342-QĐ/BTCTW — 3 defect): (a) strip zero-width PER-LINE
    # (_ZERO_WIDTH_RE — BOM/artifact docx GIỮA text thoát lstrip đầu-text, dòng letterhead mang BOM né
    # agency-skip vì regex anchored fail → thành title rác trong title_vn); (b) dòng «Căn cứ …» KHÔNG BAO
    # GIỜ là title — DỪNG quét khi gặp (trước: căn cứ nhắc 'Quyết định số 216-QĐ/TW' bị vòng từ-khóa bắt
    # nhầm); (c) loại Đảng/hành-chính ĐỨNG RIÊNG (line-anchored FULLMATCH, KHÔNG substring — 'quy định'
    # giữa câu không ăn) → title = loại + dòng «Về …» kế tiếp.
    lines = [re.sub(r"\s+", " ", _ZERO_WIDTH_RE.sub("", x)).strip() for x in (text or "").splitlines()[:80]]
    lines = [x for x in lines if x]
    _cancu_re = re.compile(r"^[-–—]?\s*can cu\b")
    _dang_kind_re = re.compile(r"^(?:quy dinh|quy che|chi thi|ket luan|huong dan|thong bao|ke hoach)$")
    for _i, line in enumerate(lines):
        n = _strip_accents(line).lower()
        if _cancu_re.match(n):
            break
        if any(k in n for k in ("luat ", "bo luat", "nghi quyet", "nghi dinh", "thong tu", "quyet dinh")):
            return line[:160]
        if _dang_kind_re.fullmatch(n):
            for _nxt in lines[_i + 1:_i + 3]:
                if re.fullmatch(r"[-_=*.\s]+", _nxt):
                    continue   # separator giữa loại và trích yếu
                _nn = _strip_accents(_nxt).lower()
                if _nn.startswith("ve ") or _nn.startswith("v/v"):
                    return f"{line} {_nxt}"[:160]
                break
            return line[:160]
    # r179 T4: dòng LETTERHEAD TÊN CƠ QUAN (IN HOA, ngắn) không phải title — '598805267335BỘ NỘI VỤ'
    # (artifact toạ độ docx + agency, đo file thật 8_Ban_tong_hop) / 'BAN CHẤP HÀNH TRUNG ƯƠNG' từng thành
    # title rác. Pattern agency BOUNDED (bo\s+(?!luat) né 'BỘ LUẬT'; không nhận 'so|vu|ban' trần — 'SO SÁNH'/
    # 'BAN HÀNH' là title thật).
    _AGENCY_RE = (r"^(?:bo\s+(?!luat)|uy\s+ban\b|quoc\s+hoi\b|chinh\s+phu\b|van\s+phong\b|"
                  r"ban\s+(?:chap\s+hanh|bi\s+thu|chi\s+dao|to\s+chuc|tuyen\s+giao|dan\s+van|noi\s+chinh|"
                  r"kinh\s+te|can\s+su|cong\s+tac)|bo\s+chinh\s+tri\b|dang\s+cong\s+san\b|dang\s+bo\b|"
                  r"(?:tinh|thanh|huyen|quan|xa|dang)\s+uy\b|hoi\s+dong\s+nhan\s+dan\b|hdnd\b|ubnd\b|"
                  r"tong\s+cuc\b|cuc\s+[a-z]|so\s+(?:noi\s+vu|y\s+te|tu\s+phap|tai\s+chinh|giao\s+duc|"
                  r"lao\s+dong|xay\s+dung|cong\s+thuong)|vu\s+(?:phap\s+che|to\s+chuc))")
    for line in lines:
        _l = re.sub(r"^(?:left|right|center)?-?\d{4,}", "", line).strip()
        n = _strip_accents(_l).lower()
        if _cancu_re.match(n):
            break   # r201 FIX-B (b): fallback cũng không bao giờ lấy dòng Căn cứ làm title
        if len(_l) < 12 or re.search(r"^\s*(cong hoa|doc lap|so:|số:|ha noi)", n):
            continue
        if len(_l) <= 60 and _l == _l.upper() and re.match(_AGENCY_RE, n):
            continue
        return _l[:160]
    return Path(fallback).stem[:160]


def _doc_subject_for_name(text: str, info: dict) -> str:
    """(MERGE Claude) Trích CHỦ ĐỀ để đặt tên: dòng TIÊU ĐỀ/trích yếu thật ('LUẬT DÂN SỐ'→'Dân số'; ND 'Quy định chi
    tiết Luật BHYT'). BỎ dòng số hiệu ('Số: 113…'/'113/2025/QH15'), quốc hiệu/căn cứ/'DỰ THẢO'; strip tiền tố loại; nếu
    dòng CHỈ là loại thì lấy dòng sau. Dừng khi tới 'Điều N'/'Chương'. Fallback title đã classify. (Chống bug Codex tên
    lặp số hiệu 'Luat_113-2025-QH15_113_2025_QH15'.)"""
    for raw in (text or "").splitlines()[:60]:
        s = raw.strip()
        if len(s) < 4:
            continue
        sl = _strip_accents(s).lower()
        if re.match(r"^(dieu\s+\d|chuong\s+|phan\s+thu|muc\s+[ivx0-9])", sl):
            break
        if re.search(r"\bso\s*:\s*\d", sl):     # dòng 'Số: 113…' DÀNH RIÊNG số hiệu → bỏ (số hiệu nhúng-trong-tiêu-đề xử ở dưới)
            continue
        if _SUBJ_NOISE_RE.match(sl):
            continue
        subj = _SUBJ_LOAI_RE.sub("", s).strip(" :.-")
        # (MERGE Claude) ca 1 DÒNG gộp 'Luật số 113-2025-QH15 Về Dân số': strip số hiệu NHÚNG (dash/slash) + tiền tố
        # 'số'/'về' còn sót → 'Dân số' (không để lọt số hiệu vào tên như bản Codex).
        subj = re.sub(r"\d{1,4}[-/]\d{2,4}[-/][A-Za-zĐđ0-9\-]+|\d{1,4}[-/](?:VBHN|VPQH|LCT[-/]?HDNN)[A-Za-zĐđ0-9\-]*",
                      " ", subj, flags=re.I)
        subj = re.sub(r"^\s*(?:(?:số|so|về|ve)\b[:.\-]?\s*)+", "", subj, flags=re.I)
        subj = re.sub(r"\s+", " ", subj).strip(" :.-")
        if len(subj) >= 3 and not re.search(r"\d{1,4}\s*[-/]\s*\d{2,4}", subj):
            return subj[:120]
    return info.get("title") or ""


def _vb_title_short_for_name(info: dict, fallback_name: str = "") -> str:
    title = str((info or {}).get("title") or fallback_name or "").strip()
    title = re.sub(r"\.[A-Za-z0-9]{1,8}$", "", title)
    title = re.sub(r"(?i)^\s*(dự\s*thảo|du\s*thao)\s+", "", title)
    title = re.sub(r"(?i)^\s*(luật|luat|bộ\s+luật|bo\s+luat|nghị\s+quyết|nghi\s+quyet|nghị\s+định|nghi\s+dinh|"
                   r"thông\s+tư|thong\s+tu|quyết\s+định|quyet\s+dinh|pháp\s+lệnh|phap\s+lenh|"
                   r"văn\s+bản\s+hợp\s+nhất|van\s+ban\s+hop\s+nhat)\s+", "", title).strip(" _-:")
    title = re.sub(r"(?i)^\s*số\s*[:\-.]?\s*", "", title).strip()
    return title or Path(fallback_name or "van_ban").stem


def _vb_standard_doc_name(info: dict, fallback_name: str = "") -> str:
    """Tên chuẩn VBQPPL theo standardize_name.py, fallback về profile name builder nếu module thiếu."""
    loai = str((info or {}).get("loai") or "").strip() or "VB"
    sohieu = str((info or {}).get("sohieu") or "").strip()
    title = _vb_title_short_for_name(info, fallback_name)
    try:
        sn = _imp("standardize_name")
        name = sn.build_doc_name(loai, sohieu, title)
        if name:
            return name[:160]
    except Exception:
        pass
    return _safe_profile_doc_name(info, fallback_name)


def _vb_auto_cat_from_text(text: str, name: str, explicit_cat: str = "") -> dict:
    explicit_cat = _norm_cat(explicit_cat or "")
    if explicit_cat:
        return {"cat": explicit_cat, "source": "explicit", "confidence": "explicit",
                "rule": None, "candidates": []}
    blob = ((name or "") + "\n" + (text or "")[:24000]).strip()
    rule_code, rule_text = _cat_boundary_rule(blob)
    if rule_code:
        return {"cat": rule_code, "source": "boundary_rule", "confidence": "high",
                "rule": rule_text, "candidates": []}
    scored = _infer_cats_text(text or name, top=3)
    if scored:
        top = scored[0]
        next_score = scored[1][1] if len(scored) > 1 else 0
        confident = top[1] >= 2 and top[1] > next_score
        return {"cat": top[0] if confident else "", "source": "content_alias",
                "confidence": "high" if confident else "low",
                "rule": None,
                "candidates": [{"cat": c, "score": s, "hits": h[:6]} for c, s, h in scored]}
    name_hits = _infer_cats(name or "")
    if len(name_hits) == 1:
        return {"cat": name_hits[0], "source": "filename_keyword", "confidence": "medium",
                "rule": None, "candidates": [{"cat": name_hits[0], "score": 1, "hits": ["filename"]}]}
    return {"cat": "", "source": "none", "confidence": "missing",
            "rule": None, "candidates": [{"cat": c, "score": 1, "hits": ["filename"]} for c in name_hits[:5]]}


def _name_prefix_family(m) -> str:
    return _NAME_PREFIX_FAMILY.get(m.group(1), m.group(1)) if m else ""


def _name_structural_issues(name: str) -> list[str]:
    """P0-3 (v1.31.0, PURE): so tên với MẪU CHUẨN `<Loai>_<sohieu>_<Chu_de>` ĐỘC LẬP header — bắt cả ca header
    parse ĐƯỢC nhưng tên registry hỏng (4 ca log 2026-07-03 đều 0 proposals): đuôi file ('luat-dau-thau-….html'),
    thiếu cụm SỐ HIỆU trong tên ('Luat_Phong_chong_benh_truyen_nhiem'), thiếu token CHỦ ĐỀ ('Luat_64-2006-QH11')."""
    n = str(name or "")
    if not n:
        return ["NAME_EMPTY"]
    issues = []
    if re.search(r"\.(docx?|pdf|html?|txt)$", n, re.I):
        issues.append("FILE_EXTENSION")
    if re.search(r"_\d{5,}\b", n):
        issues.append("UUID_TAIL")
    if not _NAME_TYPE_PREFIX_RE.match(n):   # A2 v1.33.0: nhận cả viết tắt Bộ luật (BLDS_/BLHS_/…)
        issues.append("NO_TYPE_PREFIX")
    if not _parse_sohieu_from_name(n):
        # 4D (v1.33.29 — log rà v1.33.28: 'VBHN_73-82-ND-CP_Quan_ly_dau_tu_CNTT_NSNN' cờ NO_SOHIEU oan):
        # VBHN GỘP nhiều văn bản mang SỐ KÉP 'NN-MM-<CQ>[-<CQ>]' — parser số hiệu chuẩn không nhận nhưng
        # tên KHÔNG thiếu số hiệu → đừng đẩy vào worklist rename.
        if not re.search(r"(?<![0-9A-Za-z])\d{1,5}-\d{1,5}(?:-[A-Za-z]{1,10}){1,3}(?![0-9A-Za-z])", n):
            issues.append("NO_SOHIEU_IN_NAME")
    if not _subject_tokens(_name_tail_key(n)):
        # A4 (v1.33.2 — log rà 111: NO_SUBJECT_TOKENS oan hệ thống cho tên CÓ chủ đề 'Thong_ke'/'Gia'/'Lao_dong'/
        # 'Thu_vien', dính cả 3 lệnh dùng chung checker): _subject_tokens bỏ stop-token TRÙNG TỪ-LOẠI văn bản
        # ('thong'∈thông-tư, 'quyet'/'dinh'…) + từ <3 ký tự → chủ đề thật đếm rỗng. Fallback: tail còn TỪ-CHỮ
        # ≥3 ký tự ngoài từ-loại/hậu-tố → CÓ chủ đề, không cờ. Tên trơ thật ('GD', rỗng) vẫn cờ đúng.
        _tw = [w for w in re.findall(r"[a-z]{3,}", _ascii_lower(_name_tail_key(n)))
               if w not in ("luat", "vbhn", "goc", "raw", "final", "copy", "docx", "pdf", "html", "hop", "nhat")]
        if not _tw:
            issues.append("NO_SUBJECT_TOKENS")
    return issues


def _name_looks_nonstandard(name: str) -> bool:
    """Tên KHÔNG theo chuẩn <Loai>_<sohieu>_<Chu_de>: còn đuôi file, có chuỗi số UUID rời (_583839), hoặc không mở đầu mã loại."""
    n = str(name or "")
    if re.search(r"\.(docx?|pdf|html?)$", n, re.I):
        return True
    if re.search(r"_\d{5,}\b", n):
        return True
    # v1.29.4 (log LIVE i2a): bổ sung KL/CT/CD/TTLT/TB — thiếu chúng làm tên ĐÃ CHUẨN (KL_..., CD_...) bị coi 'hỏng
    # cấu trúc' → NAME_TRICH_YEU đề xuất tên tự-trích KÉM HƠN tên chuẩn sẵn (khớp standardize_name.TYPE_PREFIX).
    # A2 v1.33.0: dùng _NAME_TYPE_PREFIX_RE (nhận cả BLDS_/BLHS_/… — '_' là word-char nên KHÔNG dùng \b).
    return not _NAME_TYPE_PREFIX_RE.match(n)


def _subject_is_boilerplate(subj: str) -> bool:
    s = _strip_accents(subj or "").lower().strip()
    return (not s) or len(_token_set(s)) < 1 or any(s == b or s.startswith(b) for b in _SUBJECT_BOILERPLATE)


def _cat_alias_evidence_for(cat2: str, scope_ascii: str) -> str:
    """D1a (v1.33.3 — log rà 66×3: 87/2015 cat 35 bị gợi 44 CHỈ vì alias 'giam sat'): alias pháp điển của CHÍNH
    cat đang gán có xuất hiện trong title-scope không. Có → title cũng ỦNG HỘ cat hiện tại → đề xuất dời tầng
    content_alias không đủ bằng chứng (precision-first). Trả alias khớp hoặc ''."""
    meta = (_load_linhvuc().get("chude") or {}).get(str(cat2 or "")) or {}
    for al in (meta.get("alias") or []):
        a = _ascii_lower(str(al)).strip()
        if len(a) >= 4 and re.search(r"\b" + re.escape(a) + r"\b", scope_ascii or ""):
            return str(al)
    return ""


def _cat_likely_wrong_suggest(entry: dict, header_text: str) -> dict | None:
    """v1.33.0 (log rà 69 Luật: CAT_LIKELY_WRONG false-positive ~78% — 59 đề xuất/54 Luật; log rà 15: BLHS 100→23
    'điều ước', VBHN Kế toán/Quy hoạch →46 hàng loạt): khối 5b cũ đưa CẢ 24KB header vào _vb_auto_cat_from_text
    → điều khoản chuyển tiếp 'sửa đổi, bổ sung' + dẫn chiếu 'điều ước quốc tế' + token lạc chủ đề (hải quan/BHXH)
    có trong THÂN của gần như mọi luật ⇒ boundary-rule bắn nhầm luật độc lập (134 AI, 113 Dân số), Bộ luật và mọi
    VBHN. Nay CHỈ suy từ PHẠM VI TIÊU ĐỀ + cổng phủ định:
      (1) title-scope = tên + khối tiêu đề IN HOA (_title_block_from_text) + title_vn — KHÔNG lấy thân văn bản;
      (2) →46 KHÔNG bao giờ cho VBHN (hợp nhất nhiều lần sửa ≠ omnibus — cat theo LUẬT ĐÍCH); ngược lại omnibus
          THẬT (_is_omnibus_entry: 'sua doi N luat'/đề-tài-nén/≥2 ref) vẫn đề xuất 46 dù title-block không parse;
      (3) →23 (điều ước) KHÔNG cho entry đã định danh Luật/Bộ luật (BLHS nhắc 'công ước' ≠ điều ước);
      (4) pin Quyết định 26/6: AI/CĐS/CNCNS đang cat 19 → KHÔNG đề xuất dời (chưa có đề mục pháp điển);
      (5) cross-check alias pháp điển (CÙNG engine cat-audit → hết 2 auditor mâu thuẫn): alias khẳng định cat
          HIỆN TẠI → bỏ; alias ra cat THỨ BA ≠ đề xuất → bỏ (bằng chứng xung đột — precision-first). Riêng 46
          miễn cross-check (rổ pháp điển 46 thắng linhvuc-theo-luật-đích, doctrine _cat_boundary_rule).
    Trả proposal-dict (type CAT_LIKELY_WRONG) hoặc None."""
    cur_cat = re.sub(r"\D", "", str(_entry_cat(entry)))[:2]
    name = _entry_name(entry)
    did = _entry_drive_id(entry)
    # v1.34.39 (audit 2026-07-13 FP: CPTPP_Chuong_19_Lao_dong bị đề xuất 23→20 vì alias 'lao dong'): quy ước
    # corpus GOM MỌI điều ước/công ước ở 23 (CU_ILO-168 chống thất nghiệp cũng 23) — chương/công ước CHUYÊN ĐỀ
    # không tách theo chủ đề nội dung; đang ở 23 + là điều ước → im.
    if cur_cat == "23" and (_is_treaty_entry(entry) or re.match(r"^(CU|CPTPP|EVFTA|DUQT)_", name or "")):
        return None
    _kind_tb, _subj_tb = _title_block_from_text(header_text or "")
    subject = " · ".join(x for x in (_name_tail_pretty(name), _subj_tb, str(entry.get("title_vn") or "")) if x)
    _scope = _ascii_lower((name or "") + " " + subject)
    _is_vbhn = _is_vbhn_entry(entry)
    # v1.33.16 (MERGE nhánh-4): omnibus nhận CẢ qua TITLE-SCOPE (tên nén + title_vn + khối tiêu đề) — tên file
    # opaque nhưng trích yếu nói 'sửa đổi các luật' vẫn bắt được.
    _omnibus = (not _is_vbhn) and (_is_omnibus_entry(entry) or _omnibus_name_text(_scope))
    # S-3 (v1.33.15 — log rà 40: đề xuất dời Luat_57-2024_SuaDoi_QuyHoach_DauTu_PPP_DauThau 46→34): rổ 46 là
    # ĐÚNG cho luật sửa nhiều luật (doctrine §13, PHI-pháp-điển — linhvuc theo đề-tài là NHIỄU). Đang ở 46 +
    # bằng chứng omnibus theo TÊN/REF/TITLE-SCOPE (không lấy cat làm bằng chứng cho chính nó) → KHÔNG đề xuất rời.
    # VBHN nằm nhầm 46 vẫn được đề xuất dời (VBHN cat theo luật đích, không thuộc 46).
    if cur_cat == "46" and not _is_vbhn and (_omnibus_name_evidence(entry) or _omnibus_name_text(_scope)):
        return None
    if _CAT19_PIN_RE.search(_scope):
        return None                    # (4) QĐ 26/6: AI/CĐS/CNCNS im lặng CẢ 2 chiều — không dời, không flag misfile
    for _rx, _pin, _why in _CAT_PIN_RULES:                              # (4b) A2 v1.33.2: pin §0.13
        if _rx.search(_scope):
            if cur_cat == _pin:
                return None            # cat hiện tại ĐÚNG doctrine — mọi suy diễn khác (39/23/…) là nhiễu
            if _omnibus:
                break                  # omnibus nhắc chủ đề pin trong tên (SuaDoi_..._To_tung) → rổ 46 xử bên dưới
            return {"type": "CAT_LIKELY_WRONG", "current": str(_entry_cat(entry)), "suggested": _pin,
                    "evidence": f"title-scope §0.13 PIN: {_why}", "subject_scope": subject[:100],
                    "fix_command": f"tl recat {did} --cat {_pin}   # REVIEW TAY (DRY) rồi mới --apply — không auto-move"}
    catp = _vb_auto_cat_from_text(subject, name, "")                    # (1) blob = tên + title-scope, KHÔNG thân
    sug_cat = re.sub(r"\D", "", str(catp.get("cat") or ""))[:2]
    evidence = catp.get("rule") or catp.get("source") or ""
    if _omnibus and cur_cat != "46" and sug_cat != "46":
        # (2) omnibus thật nhưng title-block miss (tên nén 'SuaDoi_QuyHoach_DauTu') → vẫn nghi 46.
        sug_cat, evidence = "46", "omnibus (tên/registry ≥2 luật đích) → 46; linhvuc theo luật đích"
        catp = dict(catp, confidence="high")
    if not sug_cat or sug_cat in ("00", cur_cat):
        return None
    if sug_cat == "46" and _is_vbhn:
        return None                                                    # (2) VBHN ≠ omnibus
    if sug_cat == "46":
        # v1.34.39 (audit 2026-07-13 FP: ND_187-2025 sửa 2 NGHỊ ĐỊNH bị đề xuất 44→46): rổ 46 pháp điển =
        # 'LUẬT sửa đổi, bổ sung nhiều LUẬT' — NĐ/TT/QĐ sửa nhiều văn bản cùng cấp vẫn cat theo lĩnh vực đích.
        _loai46 = _normalize_loai(str(entry.get("loai") or ""))
        if _loai46 in ("Nghị định", "Thông tư", "Thông tư liên tịch", "Quyết định", "Công điện") \
                or re.match(r"^(ND|TT|TTLT|QD|CD)_", name or ""):
            return None
    if sug_cat != "46" and catp.get("confidence") != "high":
        return None
    if sug_cat == "23" and not _is_treaty_entry(entry):
        _loai = _normalize_loai(str(entry.get("loai") or ""))
        if _loai in ("Luật", "Bộ luật") or re.match(r"^(Luat|Bo_luat|BL[A-Z])", name or ""):
            return None                                                # (3)
    alias_cat, alias_ev = _expected_cat_from_alias(subject)
    if sug_cat != "46":
        if alias_cat and alias_cat == cur_cat:
            return None                                                # (5) chủ đề khẳng định cat hiện tại
        if alias_cat and alias_cat != sug_cat:
            return None                                                # (5) 2 engine mâu thuẫn → không đủ mạnh
        # D1a (v1.33.3): title cũng ủng hộ cat HIỆN TẠI (alias của chính cur_cat trong scope) → không dời.
        if _cat_alias_evidence_for(cur_cat, _scope):
            return None
        # D1b (v1.33.3 — ca 87/2015 35→44 'nghi giả', log rà 66×3): đề xuất tầng content_alias phải là CHỦ ĐỀ
        # BAO TRÙM — alias khớp phủ ≥1/2 số từ chủ đề ('dau tu'/'cong chung' phủ TRỌN subject → GIỮ 143→34,
        # 46/2024→04; 'giam sat' 2/10 từ của 'Hoạt động giám sát của QH và HĐND' → nhiễu, BỎ).
        # Boundary-rule/pin/omnibus-46 KHÔNG qua cổng này (bằng chứng tầng doctrine).
        if catp.get("source") == "content_alias":
            _subj_core = _ascii_lower(_subj_tb or _name_tail_pretty(name))
            _sw = [w for w in re.findall(r"[a-z]{2,}", _subj_core) if w not in ("luat", "bo", "cua", "va")]
            _aw = re.findall(r"[a-z]{2,}", _ascii_lower(alias_ev or ""))
            if _sw and (not _aw or len(_aw) / len(_sw) < 0.5):
                return None
    if alias_cat and alias_cat == sug_cat:
        # A3 (v1.33.2): KHÔNG ghi "(đồng thuận cat-audit)" — cat-audit có guard/blacklist riêng nên có thể VẪN im
        # với cùng alias (log rà 111: XNC/Thống kê ghi 'đồng thuận' mà cat-audit không gắn cờ) → chỉ nêu sự thật.
        evidence = f"{evidence} · alias:{alias_ev}→{alias_cat} (alias pháp điển cùng hướng; cat-audit có guard riêng, có thể vẫn im)"
    return {"type": "CAT_LIKELY_WRONG", "current": str(_entry_cat(entry)), "suggested": sug_cat,
            "evidence": f"title-scope: {evidence}", "subject_scope": subject[:100],
            "fix_command": f"tl recat {did} --cat {sug_cat}   # REVIEW TAY (DRY) rồi mới --apply — không auto-move"}


def _declared_loai_from_header(text: str) -> str:
    """S-2h (v1.33.16 — MERGE nhánh-4 NHƯNG viết lại detector): LOẠI khai báo ở khối tiêu đề. Bản nhánh-4 scan
    12k ký tự TỰ DO → NĐ 'Căn cứ Bộ luật Lao động' bị đọc thành 'Bộ luật', TT 'Căn cứ Văn bản hợp nhất số 19/…'
    thành 'VBHN' (repro thật → 🔴 LOAI_MISMATCH oan hàng loạt, REJECT). Bản này: CHỈ dòng IN HOA ĐỨNG RIÊNG khớp
    ĐẦU-DÒNG từ-loại, lấy dòng khớp ĐẦU TIÊN (dòng căn cứ mixed-case bị loại; 'BỘ LUẬT\\nSố:…\\nHÌNH SỰ' xen kẽ
    mà _title_block_from_text miss vẫn bắt được; banner 'VĂN BẢN HỢP NHẤT [1]' đứng trước 'LUẬT' → ưu tiên đúng)."""
    txt = unicodedata.normalize("NFC", str(text or ""))[:6000]
    for ln in txt.splitlines()[:60]:
        ln = ln.strip()
        if not ln or ln != ln.upper() or not any(c.isalpha() for c in ln):
            continue
        low = re.sub(r"[^a-z0-9]+", " ", _strip_accents(ln).lower()).strip()
        for pat, canon in _DECLARED_LOAI_MAP:
            if low == pat or low.startswith(pat + " "):
                return canon
    return ""


def _file_name(info: dict) -> str:
    f = info.get("file") or {}
    return str(f.get("name") or f.get("title") or "").strip()

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


def _nlm_status_removed(status: str) -> bool:
    """HỌ status 'đã gỡ': mọi biến thể tiền tố `removed*` (removed_superseded_by_VBHN, removed_dedup…) + deleted/trash*.
    Trước đây check exact-set → biến thể removed_* bị coi NHẦM là 'còn sống' (lệch still_on_nlm/ghost)."""
    s = (status or "").strip().lower()
    return s.startswith("removed") or s.startswith("trash") or s == "deleted"

def _expand_abbrev(text: str) -> str:
    """Nối thêm dạng ĐẦY ĐỦ của viết tắt pháp lý vào text (KHÔNG thay thế → không phá token khác). 'Luat BHXH' →
    'Luat BHXH bao hiem xa hoi'. Dùng trong _token_set + _disc_conflict để khớp chủ đề bất kể viết tắt/đầy đủ."""
    low = _strip_accents(str(text or "")).lower()
    extra = [_ABBREV_MAP[m] for m in dict.fromkeys(_ABBREV_RE.findall(low))]
    return (str(text or "") + " " + " ".join(extra)) if extra else str(text or "")

def _discover_item_kind(item: dict) -> str:
    """B (PURE): phân loại 1 item Drive (shape action `list`: {id,name,mime,type}) cho discovery/adopt.
    Nhận diện KHOAN DUNG các biến thể tên thật trên Drive: 'tra_luat_registry.LuatBHXH', 'Registry_NQ36',
    'tra_luat_registry' trơ, '_manifest_DinhMucChi.json', 'tra_luat_manifest.NQ36.json'."""
    name = str(item.get("name") or "")
    mime = str(item.get("mime") or item.get("mimeType") or "")
    if str(item.get("type") or "") == "folder" or mime.endswith("apps.folder"):
        return "folder"
    if name.startswith(_PROFILES_INDEX_NAME):
        return "index"    # sổ cái (E) = hạ tầng, KHÔNG phải asset profile lạc chỗ
    if re.match(r"^(tra_luat_registry|registry)([._\-]|$)", name, re.IGNORECASE):
        if mime == REGISTRY_SHEET_MIME:
            return "registry"
        return "registry_csv" if name.lower().endswith(".csv") else "registry_nonsheet"
    if re.search(r"manifest[\w.\-]*\.json$", name, re.IGNORECASE):
        return "manifest"
    return "other"

# ── I11: bảng hằng chuyển từ tl.py (tl re-export giữ globals) ──
_ABBREV_MAP = {
    "bhxh": "bao hiem xa hoi", "bhyt": "bao hiem y te", "bhtn": "bao hiem that nghiep",
    "bluat": "bo luat",   # P1-3 v1.33.12: prefix chuẩn sinh-tự-động của standardize_name
    "blhs": "bo luat hinh su", "blld": "bo luat lao dong", "blds": "bo luat dan su",
    "bltths": "bo luat to tung hinh su", "blttds": "bo luat to tung dan su",
    "atvsld": "an toan ve sinh lao dong", "kdbh": "kinh doanh bao hiem",
    "tnld": "tai nan lao dong", "bnn": "benh nghe nghiep", "nsnn": "ngan sach nha nuoc",
    "ppp": "doi tac cong tu", "doi tac cong tu": "ppp",
    # N2 (v1.31.1 — bài học #2 log phiên rà 68 Luật): viết tắt trong TÊN FILE làm cross-check token FALSE-REJECT
    # bản đúng ('CNTT' ∌ token 'cong nghe thong tin') → bổ sung các viết tắt phổ biến còn thiếu.
    "cntt": "cong nghe thong tin", "pcth": "phong chong tac hai", "pccc": "phong chay chua chay",
    "hnvgd": "hon nhan va gia dinh", "gtvt": "giao thong van tai", "khcn": "khoa hoc cong nghe",
    # D2 (v1.33.3 — log rà 66×3: 87/2015 'HD_giam_sat_QH_HDND' FAIL title-check vì 'hdnd' không bao giờ xuất
    # hiện nguyên dạng trong header viết đầy đủ): viết tắt CƠ QUAN DÂN CỬ/đoàn thể còn thiếu.
    "hdnd": "hoi dong nhan dan", "ubnd": "uy ban nhan dan", "mttq": "mat tran to quoc",
    # S-2e (v1.33.15 — log rà 40: ND_47-2024 'CSDL_Quoc_gia' + TT_95-2025 'uu_dai_NCC' FAIL title-check vì
    # viết tắt không có trong map): bổ sung viết tắt còn thiếu gặp trong corpus thật.
    "csdl": "co so du lieu", "ncc": "nguoi co cong",
    # B.2 (v1.33.19 — log rà v1.33.18: GDDH khớp 0/1, BH_VBQPPL khớp 0/1 — title-check fail oan dù
    # sohieu/loai/cat đều PASS): viết tắt giáo dục + VBQPPL trong tên chuẩn.
    "gddh": "giao duc dai hoc", "gdnn": "giao duc nghe nghiep",
    "vbqppl": "van ban quy pham phap luat",
    # v1.33.20 (MERGE bundle-20): thêm họ hàng cùng lớp — 'bh' đứng-một-mình theo quy ước tên corpus = Ban hành
    # (bảo hiểm luôn viết BHXH/BHYT/KDBH dài hơn); expansion chỉ APPEND token nên rủi ro = 0 thay thế.
    "gdpt": "giao duc pho thong", "bh": "ban hanh", "qppl": "quy pham phap luat",
}

# ── I11: bảng hằng chuyển từ tl.py (tl re-export giữ globals) ──
_LOAI_CANON = {
    "luat": "Luật", "bo luat": "Bộ luật", "bluat": "Bộ luật", "bo_luat": "Bộ luật",
    "van ban hop nhat": "Văn bản hợp nhất", "vbhn": "Văn bản hợp nhất", "vanbanhopnhat": "Văn bản hợp nhất",
    "nghi dinh": "Nghị định", "nd": "Nghị định", "nghidinh": "Nghị định",
    "thong tu": "Thông tư", "tt": "Thông tư", "thongtu": "Thông tư",
    "thong tu lien tich": "Thông tư liên tịch", "ttlt": "Thông tư liên tịch",
    "nghi quyet": "Nghị quyết", "nq": "Nghị quyết", "nghiquyet": "Nghị quyết",
    "quyet dinh": "Quyết định", "qd": "Quyết định", "quyetdinh": "Quyết định",
    "phap lenh": "Pháp lệnh", "pl": "Pháp lệnh", "phaplenh": "Pháp lệnh",
    "ket luan": "Kết luận", "kl": "Kết luận", "chi thi": "Chỉ thị", "ct": "Chỉ thị",
    "huong dan": "Hướng dẫn", "huongdan": "Hướng dẫn",   # v1.34.31 (rà corpus): Hướng dẫn (VB Đảng HD_) — thiếu enum
    "hien phap": "Hiến pháp", "hp": "Hiến pháp", "lenh": "Lệnh",
    # v1.30.1 (#4): Công điện = họ tên-chuẩn từ v1.29.4 (CD_32-2026-CD-TTg) nhưng THIẾU trong enum → dòng
    # loai='Công điện' bị đếm phi-chuẩn vĩnh viễn + --normalize không map được. Review CONFIRMED: 'cd' trần
    # CŨNG phải map (CD ∈ họ canonical dòng _canon_fams; nhất quán nd/tt/nq/qd/kl/ct đã có; 'CĐ'→'cd' sau norm).
    "cong dien": "Công điện", "congdien": "Công điện", "cd": "Công điện",
    # A4 (v1.32.0 — log rà 77 Luật): công ước ILO/điều ước mang loai='Điều ước quốc tế' HỢP LỆ nhưng thiếu trong
    # enum → 56 dòng đếm nonmappable/loai_noncanonical GIẢ mỗi lần sweep/backfill. Thêm cả 2 giá trị canonical.
    "dieu uoc quoc te": "Điều ước quốc tế", "dieu uoc": "Điều ước quốc tế", "dieuuoc": "Điều ước quốc tế",
    "cong uoc": "Công ước", "conguoc": "Công ước",
    # v1.34.38 (#3 log phiên Chỉ thị: loai_noncanonical=26/53 — GẦN NỬA registry profile đếm phi-chuẩn GIẢ):
    # 7 loại văn bản THƯỜNG hợp lệ dùng suốt các profile nhưng thiếu enum (khuôn bổ sung như Hướng dẫn/Công điện).
    # Alias ngắn CHỈ thêm khi không đụng khóa đã có ('pl'=Pháp lệnh, 'tt'=Thông tư → Phụ lục/Tờ trình không alias 2 chữ).
    "ke hoach": "Kế hoạch", "kehoach": "Kế hoạch", "kh": "Kế hoạch",
    "de an": "Đề án", "dean": "Đề án",
    "thong bao": "Thông báo", "thongbao": "Thông báo", "tb": "Thông báo",
    "phu luc": "Phụ lục", "phuluc": "Phụ lục",
    "cong van": "Công văn", "congvan": "Công văn", "cv": "Công văn",
    "phat bieu": "Phát biểu", "phatbieu": "Phát biểu",
    "to trinh": "Tờ trình", "totrinh": "Tờ trình", "ttr": "Tờ trình",
    "bieu mau": "Biểu mẫu", "bieumau": "Biểu mẫu",   # dùng ở profile 'Biểu mẫu DMVB' 2026-07-13
    "bao cao": "Báo cáo", "baocao": "Báo cáo", "bc": "Báo cáo",   # profile 'Thẩm tra Luật Xuất bản'
    "tai lieu": "Tài liệu", "tailieu": "Tài liệu",
    # v1.34.41 B.2 GĐ2 (grill D8): +5 loại hệ văn bản ĐẢNG — ca thật QĐ 383-QĐ/TW letterhead 'QUY ĐỊNH'
    # (≠ Quyết định dù cùng mã QĐ) + CTr_02 'Chương trình' đếm noncanonical giả ở profile Chỉ thị.
    # 'qd' GIỮ = Quyết định (Quy định KHÔNG alias 2 chữ — mơ hồ thì blank-over-guess, D8).
    "quy dinh": "Quy định", "quydinh": "Quy định",
    "chuong trinh": "Chương trình", "chuongtrinh": "Chương trình", "ctr": "Chương trình",
    "quy che": "Quy chế", "quyche": "Quy chế",
    # v1.35.67 (r231 — hồ sơ Luật BHXH): TÀI LIỆU LÀM VIỆC của hồ sơ trình dự án luật. Chúng là loại hợp lệ,
    # dùng suốt các profile thẩm tra, nhưng thiếu enum ⇒ `loai_noncanonical` kêu VĨNH VIỄN và `--normalize`
    # không map được (suggested == raw, đúng bệnh Hướng dẫn/Công điện/Điều ước đã chữa 3 lần trước). Ca thật:
    # điền loai cho 12 dòng đang RỖNG (bản so sánh ×3, ý kiến góp ý ×8, mục lục) làm số này nhảy 4→16 dù
    # DỮ LIỆU TỐT LÊN — chứng tỏ thước đo thiếu rổ chứ không phải dữ liệu sai.
    "ban so sanh": "Bản so sánh", "bansosanh": "Bản so sánh",
    "y kien gop y": "Ý kiến góp ý", "ykiengopy": "Ý kiến góp ý", "gop y": "Ý kiến góp ý",
    "ban thuyet minh": "Bản thuyết minh", "banthuyetminh": "Bản thuyết minh", "thuyet minh": "Bản thuyết minh",
    "ban danh gia": "Bản đánh giá", "bandanhgia": "Bản đánh giá",
    "ban tong hop": "Bản tổng hợp", "bantonghop": "Bản tổng hợp",
    "tai lieu lam viec": "Tài liệu làm việc", "tailieulamviec": "Tài liệu làm việc",
    "dieu le": "Điều lệ", "dieule": "Điều lệ",
    "thong tri": "Thông tri", "thongtri": "Thông tri",
}

# ── I11: bảng hằng chuyển từ tl.py (tl re-export giữ globals) ──
_CAT_KEYWORDS = {
    "01": ["an_ninh_quoc_gia", "xuat_canh", "nhap_canh", "qua_canh", "bi_mat_nha_nuoc", "an_ninh_mang", "co_yeu"],
    "02": ["bao_hiem_xa_hoi", "bhxh", "bao_hiem_y_te", "bhyt", "kinh_doanh_bao_hiem", "bao_hiem_that_nghiep", "bao_hiem_tien_gui"],
    "03": ["buu_chinh", "vien_thong", "cong_nghe_thong_tin", "cntt", "giao_dich_dien_tu", "du_lieu", "an_toan_thong_tin", "tan_so", "bao_ve_du_lieu_ca_nhan", "csdl"],
    "05": ["can_bo", "cong_chuc", "vien_chuc", "cong_vu"],
    "06": ["nguoi_cao_tuoi", "nguoi_khuyet_tat", "bao_tro_xa_hoi", "giam_ngheo", "nguoi_co_cong"],
    "08": ["dan_so", "binh_dang_gioi", "bao_luc_gia_dinh", "tre_em", "nuoi_con_nuoi", "hon_nhan"],
    "09": ["dan_su", "bo_luat_dan_su"],
    "10": ["dan_toc"],
    "11": ["dat_dai", "dia_chinh"],
    "12": ["doanh_nghiep", "hop_tac_xa", "ho_kinh_doanh"],
    "13": ["giao_duc", "dao_tao", "nha_giao", "giao_vien", "day_nghe", "nghe_nghiep", "dai_hoc"],
    "14": ["giao_thong", "van_tai", "duong_bo", "duong_sat", "hang_khong", "hang_hai", "duong_thuy"],
    "15": ["ho_tich", "quoc_tich", "ly_lich_tu_phap", "boi_thuong_nha_nuoc"],
    "16": ["hinh_su", "thi_hanh_an_hinh_su", "dac_xa"],
    "17": ["ke_toan", "kiem_toan"],
    "18": ["khieu_nai", "to_cao", "tiep_cong_dan", "phong_chong_tham_nhung", "thanh_tra"],
    # v1.34.39 (audit 2026-07-13: 10+ TT 'Tiêu_chuẩn_sức_khỏe/chức_danh' BYT-BQP-BCA ở cat 45 bị suy 19 GIẢ):
    # 'tieu_chuan' TRẦN va chạm mọi 'tiêu chuẩn <ngành>' — đề mục 19 pháp điển là 'Tiêu chuẩn, ĐO LƯỜNG, CHẤT
    # LƯỢNG' → chỉ giữ cụm dài đặc thù; 'do_luong'/'chat_luong_san_pham' sẵn có phủ phần còn lại.
    "19": ["khoa_hoc", "so_huu_tri_tue", "tieu_chuan_do_luong", "quy_chuan_ky_thuat", "do_luong", "chat_luong_san_pham", "nang_luong_nguyen_tu", "chuyen_giao_cong_nghe"],
    "20": ["lao_dong", "viec_lam", "an_toan_ve_sinh_lao_dong", "tien_luong"],
    "21": ["moi_truong", "da_dang_sinh_hoc"],
    "22": ["ngan_hang", "tien_te", "cac_tctd", "tin_dung", "ngoai_hoi"],
    "23": ["ngoai_giao", "dieu_uoc_quoc_te", "lanh_su"],
    "24": ["nong_nghiep", "nong_thon", "thuy_san", "lam_nghiep", "chan_nuoi", "thu_y", "bao_ve_thuc_vat", "thuy_loi", "de_dieu"],
    "25": ["quoc_phong", "bien_phong", "dan_quan", "nghia_vu_quan_su", "sy_quan"],
    "26": ["ngan_sach", "dau_tu_cong"],
    "27": ["tai_nguyen", "khoang_san", "dia_chat", "bien_va_hai_dao"],
    "28": ["tai_san_cong", "du_tru_nha_nuoc"],
    "29": ["thi_dua", "khen_thuong", "danh_hieu_vinh_du"],
    "30": ["thi_hanh_an_dan_su"],
    "31": ["thong_ke"],
    "32": ["bao_chi", "xuat_ban", "thu_vien"],
    "33": ["thue", "le_phi", "hai_quan", "hoa_don"],
    "34": ["thuong_mai", "chung_khoan", "canh_tranh", "nguoi_tieu_dung", "ppp", "dau_thau"],
    "35": ["to_chuc_chinh_phu", "to_chuc_quoc_hoi", "chinh_quyen_dia_phuong", "to_chuc_toa_an", "to_chuc_vien_kiem_sat"],
    "36": ["mat_tran_to_quoc", "thanh_nien", "cong_doan", "cuu_chien_binh"],
    "37": ["to_tung", "trong_tai_thuong_mai", "hoa_giai"],
    "38": ["ton_giao", "tin_nguong"],
    "39": ["ma_tuy", "mai_dam", "phong_chay", "chua_chay", "vu_khi", "vat_lieu_no", "can_cuoc", "phong_chong_thien_tai"],
    "40": ["tuong_tro_tu_phap"],
    "41": ["van_hoa", "the_thao", "du_lich", "di_san", "dien_anh", "quang_cao", "the_duc"],
    "42": ["van_thu", "luu_tru"],
    "43": ["xay_dung", "nha_o", "do_thi", "quy_hoach", "kien_truc"],
    "44": ["ban_hanh_van_ban", "vbqppl", "thi_hanh_phap_luat", "pho_bien_giao_duc_phap_luat", "phap_dien"],
    "45": ["y_te", "kham_benh", "chua_benh", "an_toan_thuc_pham", "duoc_pham", "phong_chong_benh", "hien_mau", "hien_tang"],
}

# ── I11: hằng DẪN XUẤT theo map (compile lúc import — phải sống cùng file với map gốc, bài học _ABBREV_RE) ──
_ABBREV_RE = re.compile(r"(?<![a-z])(" + "|".join(_ABBREV_MAP) + r")(?![a-z])")
_LOAI_CANON_VALUES = set(_LOAI_CANON.values())
