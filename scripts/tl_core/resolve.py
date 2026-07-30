# -*- coding: utf-8 -*-
"""tl_core.resolve — I9b (v1.34.14): ĐỘNG CƠ RESOLUTION canonical (_source_map_one + amendment-gate A1/A2/A3, dedup-status, classify-ref, footnote/VBHN helpers) tách NGUYÊN VĂN từ tl.py. Đổi-luật I6 CÓ KIỂM SOÁT đã grill: engine-stays-in-tl → engine-CANONICAL-ở-đây (r76 đổi theo, vẫn khoá 1-định-nghĩa-duy-nhất); tl giữ stub; bind REBASE __globals__."""
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


# MIRROR tl.py (default-param `sites=_DISCOVERY_SITES` của _discovery_links eval TRƯỚC bind — bẫy I2;
# r80_discovery_sites_mirror drift-lock khoá resolve._DISCOVERY_SITES == tl._DISCOVERY_SITES).
_DISCOVERY_SITES = ("vbpl.vn", "congbao.chinhphu.vn", "luatvietnam.vn", "thuvienphapluat.vn")


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



def _vbhn_agency_from_key(key: str) -> str:
    m = _VBHN_KEY_RE.fullmatch(norm_sohieu(key or ""))
    return m.group(1) if m else ""


def _sohieu_query_hits_entry(shq_key: str, entry_key: str, substring: bool = False) -> bool:
    """(v1.33.47): khớp SỐ HIỆU truy vấn ↔ khóa entry, NỚI ĐÚNG 1 CHIỀU cho VBHN bare — query THIẾU năm
    ('88-VBHN-VPQH') khớp entry year-qualified CÙNG số+cơ-quan MỌI năm (trúng nhiều năm → trả CẢ, người rà tự
    chốt, không im lặng chọn bừa). Query CÓ NĂM giữ so CHẶT như cũ ('50-2025-VBHN-VPQH' ≠ '50-2026-…' — giữ phân
    biệt collision). Chiều ngược (entry thiếu năm) KHÔNG nới — đó là nợ vbhn-year-fix, có detector riêng.
    substring=True cho site vốn lọc substring (reg-query); mặc định exact (source-map/locate/in_corpus)."""
    q, ek = (shq_key or ""), (entry_key or "")
    if not q:
        return True
    if (q in ek) if substring else (q == ek):
        return True
    bq = _vbhn_bare_key(q)
    if bq and bq == q and _vbhn_bare_key(ek) == bq:
        return True
    # v1.34.41 B.2 GĐ2 (grill D5): cùng phép nới 1 CHIỀU cho số Đảng/hành chính — query bare '04-CT-TW' khớp
    # entry year-qualified '04-2026-CT-TW' mọi năm; query CÓ năm vẫn so CHẶT (giữ phân biệt collision qua khóa).
    dq = _dang_bare_key(q)
    return bool(dq) and dq == q and _dang_bare_key(ek) == dq


def _sohieu_base_sort_year(s: str) -> int:
    """Sort-key cho goc-chain VBHN: LCT-HDNN là luật trước 1992 nhưng số hiệu không chứa năm."""
    y = _sohieu_year(s)
    if y is not None:
        return y
    return 1987 if re.search(r"(?:^|[-/_])LCT[-/_]HDNN\d+\b", s or "", re.I) else 9999


def _qt5_search_hints(q: str, hits: list[dict]) -> list[str]:
    """Gợi ý QT-5 2-LƯỢT (S9): 'hợp nhất' (lượt 1) + 'mới nhất <năm>'/Công báo (lượt 2 BẮT BUỘC — chống chốt VBHN lỗi thời)."""
    import datetime as _dt
    cur_year = _dt.date.today().year
    hints = []
    for e in hits[:3]:
        # MERGE bundle-45a (v1.33.47 — log phiên rà 34 Luật của nhánh kia): subject ưu tiên title_vn/trich_yeu
        # CÓ DẤU (registry đã backfill ~88%) — tail tên file ASCII ('cong chung'/'cntt') làm recall Google lượt-2
        # yếu. TINH CHỈNH so bundle: +guard _looks_like_filename_title (title_vn nhiều dòng = chính TÊN FILE —
        # bài học P0-1 v1.31.0, query literal filename tìm ra 0; bundle thiếu guard này).
        subj = str(e.get("title_vn") or e.get("trich_yeu") or "").strip()
        if subj and _looks_like_filename_title(subj):
            subj = ""
        tail = subj if (subj and len(_token_set(subj)) >= 2) else _name_tail_key(_entry_name(e))
        if tail and len(_token_set(tail)) >= 2:
            hints.append(f'"{tail}" "hợp nhất"')
            hints.append(f'"{tail}" "hợp nhất" mới nhất {cur_year}')          # S9 lượt-2
    if q:
        hints.append(f'"{q}" "văn bản hợp nhất"')
        hints.append(f'"{q}" "hợp nhất" mới nhất {cur_year}')                 # S9 lượt-2
        hints.append(f'site:congbao.chinhphu.vn "{q}" "hợp nhất"')           # S9 official-first
    out = []
    for h in hints:
        if h not in out:
            out.append(h)
    return out[:8]


def _goc_keys(e: dict) -> set[str]:
    raw = _entry_goc(e)
    parts: list[str] = []
    if isinstance(raw, (list, tuple, set)):
        parts = [str(x) for x in raw if x]
    elif isinstance(raw, dict):
        parts = [str(x) for x in raw.values() if x]
    else:
        parts = re.split(r"[;,|]+", str(raw or ""))
    keys = set()
    for part in parts:
        k = norm_sohieu(part.strip().replace("_", "-"))
        if k:
            keys.add(k)
    return keys


def _vbhn_base_key(e: dict) -> str:
    """Số hiệu BẢN GỐC (base) của VBHN hợp nhất = sohieu có NĂM NHỎ NHẤT trong chuỗi goc (luật gốc cũ nhất; các luật
    SỬA thì mới hơn). Phân biệt 'query LÀ gốc của VBHN' (VBHN-first redirect ĐÚNG, vd 45/2019→VBHN_18) với 'query chỉ là
    1 luật SỬA trong chuỗi' (vd 114/2025 Phòng bệnh nằm trong chuỗi VBHN Luật thuốc lá → KHÔNG phải canonical của 114/2025)."""
    keys = _goc_keys(e)
    if not keys:
        return ""
    # r275 (P15-F04): _goc_keys là SET — mọi khóa KHÔNG NĂM đều sort-year 9999 (trừ LCT-HDNN=1987) ⇒ hòa
    # điểm thì `min` ăn theo THỨ TỰ DUYỆT SET (hash seed từng process) ⇒ «query có LÀ base của VBHN không»
    # (_source_map_one) có thể LẬT giữa hai lần chạy trên chuỗi goc bẩn toàn-không-năm. Tie-break phụ theo
    # chính khóa (từ điển) cho TẤT ĐỊNH; chuỗi goc sạch (có năm) không đổi hành vi.
    return min(keys, key=lambda k: (_sohieu_base_sort_year(k), k))


def _source_map_one(q: str, entries: list[dict]) -> dict:
    """Resolve nguồn rà soát theo VBHN-first, chống nhầm do file gán tên sai."""
    q = q.strip()
    qkey = norm_sohieu(q.replace("_", "-")) if _looks_like_sohieu_query(q) else ""
    qn = _strip_accents(q).lower()
    qnk = _name_key(q)
    direct, by_name, related_vbhn, amends_vbhn, goc_mismatch_vbhn = [], [], [], [], []
    _vbhn_goc_hits = []
    for e in entries:
        sh = _sohieu_key_entry(e)
        nm_plain = _strip_accents(_entry_name(e)).lower()
        nk = _name_key(_entry_name(e))
        if qkey and _sohieu_query_hits_entry(qkey, sh):   # v1.33.47: +bare-VBHN 1 chiều (query không năm ↔ entry có năm)
            direct.append(e)
        if qn and (qn in nm_plain or (qnk and nk and (qnk in nk or nk in qnk))
                   or _entry_query_match(q, e, include_subject=False)):   # token/phrase: bắt 'Luật Dân số' ↔ '...Dan_so'
            by_name.append(e)
        if qkey and _is_vbhn_entry(e) and qkey in _goc_keys(e):
            _vbhn_goc_hits.append(e)
    # Phân loại VBHN-goc-hit SAU vòng lặp (cần direct/by_name để biết CHỦ ĐỀ truy vấn cho cổng chống goc-nhiễm).
    _q_subject = _derive_subject_from_entries(direct or by_name)
    for e in _vbhn_goc_hits:
        # VBHN-first redirect CHỈ khi query LÀ GỐC của VBHN (base = năm nhỏ nhất chuỗi goc). Nếu query chỉ là 1 luật
        # SỬA trong chuỗi (vd 114/2025 Phòng bệnh trong chuỗi VBHN thuốc lá) → amends_vbhn (liên quan, KHÔNG canonical).
        if _vbhn_base_key(e) != qkey:
            amends_vbhn.append(e)
        elif _vbhn_goc_corroborated(e, qkey, _q_subject):
            related_vbhn.append(e)
        else:
            # §1.1: registry.goc trỏ qkey NHƯNG tên/chủ đề VBHN thuộc văn bản KHÁC (goc nhiễm) → KHÔNG redirect.
            goc_mismatch_vbhn.append(e)
    amendment_candidates = _find_amendment_candidates(qkey, direct, by_name, entries)
    # §1.2 (log rà): nếu đã có VBHN-first (related_vbhn) thì luật-sửa NẰM TRONG CHUỖI goc của VBHN đó ĐÃ ĐƯỢC HỢP NHẤT
    # → KHÔNG còn là 'thiếu liên kết' và KHÔNG cần PAUSE (vd PPP 64/2020: 57/2024 & 90/2025 đã trong goc VBHN 123).
    _consolidated_keys = set()
    for v in related_vbhn:
        _consolidated_keys |= _goc_keys(v)
    consolidated_amendments = [e for e in amendment_candidates
                               if _consolidated_keys and _sohieu_key_entry(e) in _consolidated_keys]
    if _consolidated_keys:
        amendment_candidates = [e for e in amendment_candidates
                                if _sohieu_key_entry(e) not in _consolidated_keys]
    unlinked_amendments = [e for e in amendment_candidates if not e.get("_amendment_linked_to_query")]
    # P1-5 (log rà 71 luật): chỉ ESCALATE PAUSE_AND_ASK_USER khi có ÍT NHẤT 1 ứng viên MANG SỐ HIỆU VBQPPL hợp lệ
    # (QH/NĐ/TT/PL…). Ứng viên sohieu=∅ (raw chưa bóc số / thư góp ý) vẫn LIỆT KÊ nhưng KHÔNG tự dừng workflow.
    amendment_candidates_normative = [e for e in amendment_candidates if e.get("_amendment_has_sohieu")]
    # v1.29.6 (P0b): chỉ ứng viên MẠNH (linked/high — xem _find_amendment_candidates) mới đủ lực ESCALATE PAUSE.
    amendment_candidates_strong = [e for e in amendment_candidates_normative if e.get("_amendment_strong")]
    pool = related_vbhn or direct or by_name
    pool = list({(_entry_drive_id(e) or str(id(e))): e for e in pool}.values())
    pool.sort(key=_entry_score, reverse=True)
    canonical = pool[0] if pool else None
    # srcmap_name_resolution: truy van TEN neu LOAI 'Luat/Bo luat/Phap lenh' -> UU TIEN hit tier>=loai-neu (chong
    # chot ND/TT lam canonical chi vi diem cao). Chi nhan hit KHOP-CHAT (_name_strong_match) & KHONG cach ly -> vua
    # sua 'Luat Dau tu'->Luat (khong ND), vua KHONG over-fire LOW_CONFIDENCE khi co hit tier-Luat chac.
    _qdt = _query_doctype_tier(q)
    if (not qkey) and _qdt >= 4 and pool:
        _tier_strong = [e for e in pool if not _entry_quarantined(e)
                        and _vb_tier_rank(e) >= _qdt and _name_strong_match(q, _entry_name(e))]
        if _tier_strong:
            canonical = max(_tier_strong, key=_entry_score)
    warnings = []
    # name_rank_collision gate: truy vấn THEO TÊN (không số hiệu) có >1 hit nhưng hit điểm-cao chỉ khớp-MỜ
    # (không đủ chủ đề: 'Luật Dân số'→'Dân chủ ở cơ sở'/'Dân sự', 'Việc làm'→'đi làm việc ở nước ngoài',
    # 'Phí và lệ phí'→'Học phí'). KHÔNG chốt 1 canonical sai → trả None + LOW_CONFIDENCE thay vì in RÀ SOÁT TRÊN.
    name_only = (not qkey) and (not related_vbhn) and (not direct) and bool(by_name)
    # A1 (port Codex, verified): truy vấn THEO TÊN — ghim canonical CHỈ trong các hit KHỚP CHỦ ĐỀ thật
    # (_name_subject_match, abbrev-aware: 'BLLD'≡'Bộ luật Lao động', 'BHXH'≡'bảo hiểm xã hội'), KHÔNG cho token chung
    # chốt nhầm ('Bộ luật Lao động'→'Dân chủ cơ sở'). Query tier-Luat/Bộ luật → siết thêm tier+strong. Nếu KHÔNG có
    # hit chủ đề → canonical=None + SUBJECT_MISMATCH (thay vì ghim sai). Loại quarantine khỏi ứng viên (gốc rễ A1=B1).
    name_subject_hits = []
    if name_only:
        name_subject_hits = [e for e in pool if not _entry_quarantined(e) and _name_subject_match(q, e)]
        if _qdt >= 4:
            name_subject_hits = [e for e in name_subject_hits
                                 if _vb_tier_rank(e) >= _qdt and _name_strong_match(q, _entry_name(e))]
        if name_subject_hits:
            canonical = max(name_subject_hits, key=_entry_score)
        elif canonical is not None:
            canonical = None
            warnings.append("NAME_QUERY_SUBJECT_MISMATCH_NO_CANONICAL: truy vấn tên có chủ đề rõ nhưng các hit KHÔNG "
                            "khớp chủ đề — KHÔNG chốt canonical; chạy lại bằng SỐ HIỆU hoặc thêm chủ đề/năm.")
    if name_only and len(by_name) > 1 and canonical is not None and not _name_strong_match(q, _entry_name(canonical)):
        canonical = None
        warnings.append("LOW_CONFIDENCE_NAME_MATCH: nhiều hit theo tên nhưng hit điểm-cao chỉ KHỚP-MỜ (thiếu chủ đề "
                        "đầy đủ của truy vấn) — KHÔNG chốt canonical; xem name_hits, verify trích yếu/số hiệu trước khi rà.")
    if goc_mismatch_vbhn:
        warnings.append("GOC_SUBJECT_MISMATCH: registry.goc của 1 VBHN trỏ số hiệu này NHƯNG tên/chủ đề VBHN thuộc "
                        "văn bản KHÁC (goc bị nhiễm) — KHÔNG redirect sang VBHN đó; rà bản gốc đích. "
                        "Sửa registry.goc của VBHN (xem goc_mismatch_vbhn) qua `tl register` (reg_upsert).")
    if related_vbhn:
        warnings.append("VBHN_FIRST_APPLIED: có VBHN hợp nhất nhận số hiệu đích là BẢN GỐC (base) trong trường goc; nên rà trên VBHN.")
        # S9 (log 2026-07-01): VBHN TRONG CORPUS có thể LỖI THỜI (đã có bản hợp nhất mới hơn trên web chưa nạp — ca BLHS
        # 01/VBHN 2017 vs 135/VBHN 2025). BẮT BUỘC xác minh bản mới nhất (QT-5 lượt-2 'mới nhất <năm>' + Công báo).
        warnings.append("VBHN_CANDIDATE_UNVERIFIED_LATEST: VBHN trong corpus CHƯA chắc là BẢN MỚI NHẤT — chạy `tl vbhn-check "
                        "--goc <số> --subject <chủ đề>` rồi QT-5 lượt-2 ('mới nhất <năm>' + site:congbao.chinhphu.vn) tìm số "
                        "VBHN lớn hơn/ngày sau cùng VPQH trước khi trích dẫn (số VBHN tăng dần mỗi lần hợp nhất, KHÔNG semver).")
        if any(_is_high_amendment_subject(_entry_name(v)) or _is_high_amendment_subject(_derive_subject_from_entries([v])) for v in related_vbhn):
            warnings.append("VBHN_HIGH_AMENDMENT_VELOCITY: luật SỬA ĐỔI DỒN DẬP (2024-2026) — BẮT BUỘC kiểm Công báo năm hiện tại.")
    if len(related_vbhn) > 1:
        warnings.append("MULTIPLE_VBHN_BASE: số hiệu là GỐC của >1 VBHN (có thể số hiệu tái dùng theo năm) — KHÔNG chốt 1 canonical; xem related_vbhn và verify năm/loại trước khi rà.")
    if amends_vbhn and not related_vbhn:
        warnings.append("AMENDS_OTHER_VBHN: số hiệu đích là LUẬT SỬA nằm trong chuỗi hợp nhất của VBHN khác (KHÔNG phải bản gốc của VBHN đó); canonical là CHÍNH văn bản đích — KHÔNG redirect sang VBHN ấy. Xem amends_vbhn.")
    if consolidated_amendments:
        warnings.append(f"AMENDMENTS_ALREADY_CONSOLIDATED: {len(consolidated_amendments)} luật-sửa đã nằm trong chuỗi "
                        "hợp nhất của VBHN canonical (đã phản ánh) — KHÔNG cần nạp/link/PAUSE; xem consolidated_amendments.")
    # §1.2 cổng PHỤ (port Codex): với luật-sửa CÒN LẠI (chưa nằm trong chuỗi goc) — nếu VBHN canonical ban hành KHÔNG
    # sớm hơn TẤT CẢ (đều có ngày rõ) → coi như đã phản ánh, hạ PAUSE→INFO. Bổ trợ cổng goc-chain (dùng khi goc thiếu
    # nhưng ngày ban hành đủ). Trên manifest hiện thiếu ngày → cổng này im lặng; goc-chain đã lo phần lớn ca.
    _pause_vbhn = canonical if (canonical and _is_vbhn_entry(canonical)) else (related_vbhn[0] if related_vbhn else None)
    # ═══ v1.32.0 (log rà 77 Luật — 3 defect lớp amendment-gate A1/A2/A3) ═══
    _canon_confirmed = bool(canonical is not None and _entry_confirmed(canonical))
    _canon_is_vbhn = bool(canonical is not None and _is_vbhn_entry(canonical))
    _canon_is_omnibus = bool(canonical is not None and _is_omnibus_entry(canonical))
    # A2: canonical CHÍNH LÀ VBHN (query trực tiếp số VBHN — ca 115-2026-VBHN): luật nằm trong chuỗi goc CỦA NÓ là
    # thành-phần-đã-hợp-nhất, KHÔNG phải amendment mồ côi (khối consolidated ở trên chỉ gom goc của related_vbhn —
    # rỗng khi query thẳng VBHN). Chuyển các ứng viên đó sang consolidated_amendments.
    if _canon_is_vbhn:
        _ck2 = _goc_keys(canonical)
        _moved = [e for e in amendment_candidates if _ck2 and _sohieu_key_entry(e) in _ck2]
        if _moved:
            consolidated_amendments = consolidated_amendments + _moved
            _mkeys = {_sohieu_key_entry(e) for e in _moved}
            amendment_candidates = [e for e in amendment_candidates if _sohieu_key_entry(e) not in _mkeys]
            unlinked_amendments = [e for e in unlinked_amendments if _sohieu_key_entry(e) not in _mkeys]
            amendment_candidates_normative = [e for e in amendment_candidates_normative if _sohieu_key_entry(e) not in _mkeys]
            amendment_candidates_strong = [e for e in amendment_candidates_strong if _sohieu_key_entry(e) not in _mkeys]
            warnings.append(f"AMENDMENTS_ALREADY_CONSOLIDATED: {len(_moved)} luật-sửa nằm trong chuỗi goc của CHÍNH "
                            "canonical VBHN này (đã phản ánh) — KHÔNG nạp/link/PAUSE; xem consolidated_amendments.")
    vbhn_date_covered, vbhn_issue_date, covered_amendments = _amendments_covered_by_vbhn_date(
        _pause_vbhn, amendment_candidates_normative)
    # S-8 (v1.33.15 — log rà 67 Luật: 37/67 vào hàng web LƯỢT-2, ~15 ca CHỈ vì UNVERIFIED_LATEST dù VBHN
    # 2025-2026 vừa hợp nhất xong — 33-2024 Lưu trữ/45-2024 Di sản/50-2024 Công đoàn/87-2025): VBHN DUY NHẤT
    # + năm ban hành rõ ≥ năm-nay−1 + KHÔNG luật-sửa nào MỚI HƠN đã biết (covered theo ngày, hoặc không có ứng
    # viên normative) → hạ UNVERIFIED_LATEST thành cờ INFO — hàng đợi lượt-2 hết loãng, ưu tiên thật nổi lên.
    # KHÔNG đổi doctrine: HIGH_VELOCITY giữ nguyên (nhóm dồn dập vẫn bắt buộc Công báo), và trước khi TRÍCH DẪN
    # chính thức vẫn `tl vbhn-verify --official-required` như cũ — đây chỉ là hạ ƯU TIÊN hàng đợi.
    if related_vbhn and len(related_vbhn) == 1 and _pause_vbhn is not None:
        _vy8 = _entry_issue_year(_pause_vbhn) or _sohieu_year(_sohieu_key_entry(_pause_vbhn))
        # Nhóm HIGH_VELOCITY (BLHS/Đầu tư/Thuế…) KHÔNG hạ — doctrine S10: sửa dồn dập, Google rank trang cũ,
        # bản hợp nhất mới có thể ra TRONG NĂM → UNVERIFIED_LATEST của nhóm này luôn là việc thật.
        _hi_vel8 = any(w.startswith("VBHN_HIGH_AMENDMENT_VELOCITY") for w in warnings)
        if (_vy8 and _vy8 >= time.localtime().tm_year - 1 and not _hi_vel8
                and (vbhn_date_covered or not amendment_candidates_normative)):
            warnings = [w for w in warnings if not w.startswith("VBHN_CANDIDATE_UNVERIFIED_LATEST")]
            warnings.append(f"VBHN_LATEST_RECENT_COVERED: VBHN duy nhất ban hành {_vy8} (rất mới) và không có "
                            "luật-sửa nào MỚI HƠN đã biết trong corpus → hạ ưu tiên web LƯỢT-2; vẫn chạy "
                            "`tl vbhn-verify --official-required` trước khi trích dẫn chính thức.")
    # A1: canonical ĐÃ CONFIRM (registry.verified) → doctrine §confirm 'tin dùng luôn' phải phủ CẢ nhóm cờ
    # amendment-gate (ca 90-2025 confirmed=yes vẫn bị VBHN_RECHECK + UNLINKED). Suppression NHẤT QUÁN với
    # action_required bên dưới. Gỡ nhãn confirm nếu nghi có sửa đổi MỚI hơn ngày confirm.
    _gate_escalate = bool(amendment_candidates_strong) and not vbhn_date_covered and not _canon_confirmed
    if amendment_candidates:
        warnings.append("AMENDMENT_CANDIDATE_IN_CORPUS: phát hiện văn bản sửa đổi liên quan trong corpus/NLM; không được rà bản gốc đơn lẻ.")
        if _canon_confirmed:
            warnings.append("AMENDMENT_GATE_SUPPRESSED_CONFIRMED: canonical verified (đã rà kỹ) — bỏ UNLINKED/"
                            "VBHN_RECHECK/PAUSE theo doctrine §confirm; amendment_candidates chỉ liệt kê tham khảo. "
                            "Nghi có sửa đổi MỚI HƠN ngày confirm → gỡ nhãn verified rồi rà lại.")
        elif vbhn_date_covered:
            warnings.append(f"AMENDMENT_CANDIDATES_COVERED_BY_VBHN_DATE: VBHN ban hành ngày {vbhn_issue_date} không sớm "
                            "hơn toàn bộ luật-sửa có ngày rõ — hạ cảnh báo xuống INFO, KHÔNG PAUSE; vẫn nên verify footnote khi chốt.")
        else:
            # A3: canonical là OMNIBUS (sửa nhiều luật) — bản chất AMENDS_OTHER, không bao giờ có VBHN của chính nó;
            # ứng viên mồ-côi quanh nó phần lớn là nhiễu cùng-chủ-đề → cờ riêng, KHÔNG UNLINKED/LOW_CONF (hết REVIEW lặp).
            if unlinked_amendments and not _canon_is_omnibus:
                warnings.append("UNLINKED_AMENDMENT_CANDIDATE: văn bản sửa đổi có trong corpus nhưng thiếu goc/sua_doi; "
                                "phải hỏi người dùng để cập nhật registry trước khi rà tiếp "
                                "(DANH SÁCH ứng viên: key `unlinked_amendment_candidates`/`amendment_candidates` — v1.33.6).")
            if not related_vbhn:
                if _canon_is_vbhn:
                    # A2: KHÔNG 'tìm VBHN cho một VBHN' — chuyển sang xác minh chuỗi goc/sua_doi + bản mới nhất.
                    warnings.append("VBHN_GOC_VERIFY: canonical CHÍNH LÀ bản hợp nhất — không tìm VBHN cho VBHN; "
                                    "xác minh chuỗi goc/sua_doi phủ đủ (`tl footnote-map <id>` / `tl relation-check "
                                    "--base <goc>`) và bản MỚI NHẤT (QT-5 lượt-2, số VBHN tăng dần).")
                elif _canon_is_omnibus:
                    warnings.append(f"OMNIBUS_AMENDS_OTHER: canonical là luật SỬA NHIỀU LUẬT — không có VBHN của chính nó; "
                                    f"rà theo từng luật ĐÍCH trong goc/`tl relation-check --base <đích>`"
                                    + (f" ({len(unlinked_amendments)} ứng viên mồ-côi quanh nó = tham khảo, không REVIEW)."
                                       if unlinked_amendments else "."))
                else:
                    warnings.append("VBHN_RECHECK_REQUIRED: luật đã/ có thể đã được sửa đổi; chạy `tl vbhn-check` theo trích yếu + 'hợp nhất' và không kết luận chưa có VBHN.")
            # v1.29.6 (P0b — log 118 Luật: 15 PAUSE giả, 100% conf=low non-linked): PAUSE CHỈ khi có ứng viên MẠNH
            # (linked đúng số hiệu / confidence=high; omnibus non-linked = weak). Weak-only → REVIEW với cờ riêng.
            if _gate_escalate:
                warnings.append("PAUSE_AND_ASK_USER: DỪNG rà soát, trình danh sách amendment_candidates và xin xác nhận nạp/link/VBHN official-first.")
            elif amendment_candidates_normative and not _canon_is_omnibus:
                warnings.append("AMENDMENT_CANDIDATE_LOW_CONFIDENCE: ứng viên sửa-đổi đều KHỚP MỜ (confidence=low, "
                                "không dẫn chiếu số hiệu base / omnibus chưa xác định luật đích) — REVIEW khi rà, "
                                "KHÔNG dừng workflow; verify goc/sua_doi nếu nghi thật.")
    qyear = _sohieu_year(qkey)
    # r273: trần «luật đủ cũ để có thể đã có VBHN» phải ĐỘNG — hardcode `<= 2021` mục theo thời gian (đúng
    # lời tự phê của S-8b về «nhánh-4 hardcode 2024 sẽ mục»): năm 2026 luật 2022-2024 đã kịp bị sửa 2024-2026
    # mà gate im ⇒ false-clean. Chọn cur−2 ĐỒNG BỘ ngưỡng «rất mới» của S-8/S-8b (y ≥ cur−1/cur−2 = mới):
    # luật cur−1/cur chưa kịp có VBHN → im là đúng; luật ≤ cur−2 thiếu VBHN → phải nhắc QT-5 web.
    _vbhn_gate_cutoff = time.localtime().tm_year - 2
    # D (v1.33.18 — MERGE bundle-18, log rà 67: cặp gốc/sửa LỆCH PHA — 64-2006 HIV verdict OK 'đã hợp nhất'
    # nhưng luật sửa 71-2020 của CHÍNH chuỗi đó vẫn bị NO_VERIFIED_VBHN + QT5 đẩy vào web lượt-2): luật SỬA đã
    # nằm trong chuỗi goc của VBHN khác (amends_vbhn ≠ ∅, cờ AMENDS_OTHER_VBHN) thì nội dung của nó ĐÃ được
    # phản ánh trong VBHN của luật ĐÍCH — không đòi VBHN riêng cho nó nữa (đồng dạng nhánh omnibus AMENDS_OTHER).
    # r273b: canonical ĐÃ CONFIRM (registry.verified) không bị nhắc web mỗi lần quét — đồng bộ doctrine
    # §confirm (A1 v1.32.0 đã suppress nhóm amendment-gate; web-gate nag trên bản đã rà kỹ = re-review noise).
    if (not related_vbhn) and (not amends_vbhn) and qkey and direct and not _canon_confirmed \
            and not any(_is_vbhn_entry(e) for e in direct) and (qyear is None or qyear <= _vbhn_gate_cutoff):
        warnings.append("NO_VERIFIED_VBHN_IN_CORPUS: manifest chưa có VBHN đã xác minh; KHÔNG kết luận là không tồn tại.")
        warnings.append("QT5_WEB_REQUIRED: chạy tìm web theo trích yếu/chủ đề + 'hợp nhất' (không tìm một lần theo số hiệu bản gốc).")
    elif (not related_vbhn) and (not amends_vbhn) and (not qkey) and canonical is not None and not _canon_is_vbhn \
            and not any(_is_vbhn_entry(e) for e in pool):
        # A1 (v1.33.2 — log rà 111 Luật: source-map "Bộ luật Hình sự" trả OK/flags=[] chọn bản gốc 2015 dù §0.1
        # lấy chính BLHS làm ví dụ VBHN lỗi thời 135/VBHN-2025): gate trên đòi qkey+direct → truy vấn THEO TÊN
        # câm hoàn toàn = false-clean. Cùng điều kiện với gate sohieu, năm lấy từ CANONICAL thay vì query.
        _cyr = _sohieu_year(_sohieu_key_entry(canonical)) or _entry_issue_year(canonical)
        if not _canon_confirmed and (_cyr is None or _cyr <= _vbhn_gate_cutoff):
            warnings.append("NO_VERIFIED_VBHN_IN_CORPUS: manifest chưa có VBHN đã xác minh; KHÔNG kết luận là không tồn tại.")
            warnings.append("QT5_WEB_REQUIRED: chạy tìm web theo trích yếu/chủ đề + 'hợp nhất' (không tìm một lần theo số hiệu bản gốc).")
    # A1b (v1.33.2): nhóm SỬA DỒN DẬP (S10) phải cảnh báo CẢ khi corpus chưa có VBHN nào — trước chỉ gắn trong
    # nhánh `related_vbhn` nên đúng ca cần nhất (thiếu VBHN) lại im.
    if (not related_vbhn) and canonical is not None and not _canon_is_vbhn and (
            _is_high_amendment_subject(q) or _is_high_amendment_subject(_entry_name(canonical))):
        warnings.append("VBHN_HIGH_AMENDMENT_VELOCITY: luật SỬA ĐỔI DỒN DẬP (2024-2026) mà corpus CHƯA có VBHN "
                        "tương ứng — BẮT BUỘC kiểm Công báo năm hiện tại trước khi rà bản gốc.")
    if qkey:
        direct_vbhn = [e for e in direct if _is_vbhn_entry(e)]
        if direct_vbhn:
            # v1.17.17: chỉ bật reuse-risk khi metadata chưa đủ hoặc có nhiều ứng viên cùng số.
            # Một VBHN đã có năm/chủ đề rõ không cần cảnh báo nhiễu ở mọi truy vấn.
            # v1.33.0 (log rà 15 — B4: 25-2025-VBHN-VPQH năm ĐỦ ở cả sohieu-key lẫn tên VẪN bị REVIEW): 'nhiều
            # ứng viên cùng số' và cờ thiếu-năm chỉ xét trên VĂN BẢN PHÂN BIỆT — bỏ sidecar file-thô + quarantine
            # (cặp GDoc+.docx cùng số là MỘT văn bản, không phải tái dùng số). Tên trơ thiếu năm (133/61/72) vẫn
            # cờ đúng qua VBHN_NAME_MISSING_YEAR trên chính bản phân biệt.
            _distinct_vbhn = [e for e in direct_vbhn
                              if not _entry_quarantined(e) and not _is_source_sidecar(e, direct, canonical)]
            risky_vbhn = (len(_distinct_vbhn) > 1) or any(
                (not _vbhn_year_complete(e)) and
                set(_title_flags(e)) & {"VBHN_BARE_NUMBER", "VBHN_MISSING_YEAR_OR_DATE", "VBHN_NAME_MISSING_YEAR"}
                for e in (_distinct_vbhn or direct_vbhn)
            )
            if risky_vbhn:
                warnings.append("VBHN_NUMBER_REUSE_RISK: số VBHN có thể tái sử dụng theo năm; phải verify ngày ban hành + tiêu đề + dòng hợp nhất trước khi tin.")
            # P1-4 (log rà 71 luật): TÁI DÙNG SỐ THẬT — >1 VBHN CÙNG số hiệu nhưng KHÁC CHỦ ĐỀ (vd 89-VBHN-VPQH =
            # NSNN 2026 + NSNN gốc + MTTQ). KHÔNG tự chốt 1 canonical theo điểm (dễ trả nhầm MTTQ khi người hỏi NSNN);
            # trả canonical=None + đòi phân định. CHỈ khi ĐA CHỦ ĐỀ (nhiều version cùng chủ đề → vẫn chốt bản điểm cao).
            _nonraw_vbhn = [e for e in direct_vbhn
                            if not _is_raw_no_gdoc_name(_entry_name(e)) and not _entry_quarantined(e)]
            # CHỈ đếm CHỦ ĐỀ RÕ (tail không rỗng): bản tên-trơ '89-VBHN-VPQH' (tail='') KHÔNG tính là chủ đề khác
            # → tránh false-ambiguity (trước fallback full-name làm bản trơ ≠ bản có chủ đề → clear canonical oan).
            _subj_keys = {tk for e in _nonraw_vbhn if (tk := _name_tail_key(_entry_name(e)))}
            if len(_nonraw_vbhn) > 1 and len(_subj_keys) > 1:
                canonical = None
                warnings.append("VBHN_REUSE_AMBIGUOUS_NO_CANONICAL: >1 VBHN dùng CÙNG số hiệu nhưng KHÁC chủ đề — "
                                "KHÔNG tự chốt canonical theo điểm. Phân định bằng `tl source-map \"<số hiệu> <chủ đề/năm>\"` "
                                "(hoặc `tl vbhn-check --goc <số> --subject <chủ đề>`); xem direct_hits chọn đúng bản trước khi rà.")
    if len(by_name) > 1 and not qkey:
        warnings.append("NAME_QUERY_MULTIPLE_HITS: truy vấn theo tên có nhiều hit; phải dựa canonical/vb_status, không lấy hit đầu theo tên.")
    # entry ĐÃ CONFIRM (registry.verified) = đã rà kỹ → TIN dùng luôn, KHÔNG nhồi vào DIRTY/WARN (giảm nhiễu, tăng tốc).
    dirty = [e for e in pool if not _entry_confirmed(e) and ((not _entry_sohieu(e)) or _bad_cat(_entry_cat(e)) or ("root" in _entry_cat(e).lower()))]
    if dirty:
        warnings.append("DIRTY_CANDIDATES: có dòng root/orphan/metadata rỗng trong nhóm; chạy `tl hygiene plan` trước khi thao tác ghi.")
    risky = []
    for e in pool:
        if _entry_quarantined(e) or _entry_confirmed(e):   # cách ly HOẶC đã-confirm → không WARN (giảm nhiễu)
            continue
        # A1 (log rà 122 Luật): ghost/rỗng-tên trong candidate set không được kích TITLE_OR_REGISTRY_WARN hàng loạt.
        if not _name_key(_entry_name(e)):
            continue
        flags = _source_map_flags(e)
        # B3 (v1.32.0 — log rà 77: 21 ca RAW_NAME_NOT_NLM là sidecar .docx/.pdf cạnh GDoc, đúng thiết kế nhưng loãng
        # tín hiệu mỗi lần rà): bỏ cờ này khỏi risky khi entry là SIDECAR của bản chuẩn trong cùng nhóm.
        if "RAW_NAME_NOT_NLM" in flags and _is_source_sidecar(e, pool, canonical):
            # review v1.32.0 (CONFIRMED): PHẢI truyền canonical — thiếu nó, guard 'other is not canonical' trong
            # _is_source_sidecar không kích hoạt → có thể suppress nhầm khi sidecar chỉ khớp entry thường.
            flags = [f for f in flags if f != "RAW_NAME_NOT_NLM"]
        # A3 (tối ưu MERGE): CHỈ kích WARN trên cờ SIÊU-DỮ-LIỆU per-law thật; cờ TRÔI toàn cục (NLM/raw-sibling) không
        # WARN (đã ở doctor/sweep + nlm_gaps). Vẫn giữ `flags` đầy đủ trong risky entry để không mất thông tin.
        substantive = [f for f in flags if f not in _TITLE_WARN_GLOBAL_FLAGS]
        if substantive:
            risky.append({"entry": _summ_entry_source_map(e), "flags": flags, "reason": _flags_reason(flags)})
    if risky:
        warnings.append("TITLE_OR_REGISTRY_WARN: có ứng viên bị WARN; xem `risky_candidates` và chạy `tl hygiene plan --json`.")
    if canonical is not None and _entry_confirmed(canonical):
        warnings.append(f"CONFIRMED: canonical đã rà kỹ & gán nhãn verified={_entry_confirmed(canonical)} — tin dùng luôn, không cần re-review.")
    # A3 (log rà): canonical là VBHN nhưng số hiệu CHỈ MỤC (registry/qkey) là số hiệu BẢN GỐC khác hẳn số hiệu VBHN
    # thật (vd row 52-2014-QH13 nhưng canonical = VBHN_121-VBHN-VPQH Hôn nhân) → cảnh báo để KHÔNG trích dẫn nhầm số.
    if canonical is not None:
        _can_name_sh = norm_sohieu(_parse_sohieu_from_name(_entry_name(canonical)).replace("_", "-"))
        _can_reg_sh = _sohieu_key_entry(canonical)
        if _can_name_sh and _can_reg_sh and _can_name_sh != _can_reg_sh \
                and "VBHN" in _can_name_sh and "VBHN" not in _can_reg_sh:
            warnings.append(f"CANONICAL_VBHN_NUMBER_DIFFERS: số hiệu chỉ mục ({_can_reg_sh}) khác số hiệu VBHN thật của "
                            f"bản canonical ({_can_name_sh}) — trích dẫn theo số hiệu VBHN, không theo số bản gốc.")
    # #5 log (đề xuất): NỔI số đếm PENDING ngay ở source-map — rủi ro hiệu-lực-tương-lai lặp xuyên BHXH/BLLĐ/BHYT.
    # Rẻ: chỉ soi NGÀY HIỆU LỰC (registry) của nhóm > hôm nay (KHÔNG chạy footnote-map nặng); rỗng thì im lặng.
    import datetime as _dt
    _today = _dt.date.today().isoformat()
    _pp = {(_entry_drive_id(e) or str(id(e))): e
           for e in (([canonical] if canonical else []) + direct + related_vbhn + amends_vbhn + by_name)}
    pending_future = [(e, hl) for e in _pp.values() if (hl := _entry_hieuluc_date(e)) and hl > _today]
    if pending_future:
        warnings.append(f"PENDING_FUTURE_EFFECT: {len(pending_future)} văn bản trong nhóm có NGÀY HIỆU LỰC tương lai (> {_today}) "
                        "— rủi ro 'chưa/đang có hiệu lực'; chạy `tl footnote-map` để rà pending cấp Điều trước khi kết luận.")
    _pp_vals = list(_pp.values())
    draft_hits = [e for e in _pp_vals if _entry_is_draft(e)]
    if draft_hits:
        warnings.append(f"DRAFT_NOT_EFFECTIVE: {len(draft_hits)} nguồn là DỰ THẢO — chưa hiệu lực; không dùng như luật/văn bản đang có hiệu lực.")
    _cov_pp = _chunk_covered_sohieu(_pp_vals)     # r253: phủ-bằng-chunk KHÔNG tính là nợ NLM
    nlm_gaps = [e for e in _pp_vals if "CORPUS_TRUE_NOT_ON_NLM" in _title_flags(e, _cov_pp)
                and not _dup_of_live_sibling(e, _pp_vals)]
    if nlm_gaps:
        warnings.append(f"CORPUS_TRUE_NOT_ON_NLM: {len(nlm_gaps)} văn bản corpus=true nhưng chưa có nguồn NLM live "
                        "— chạy `tl ingest-local`/`tl nlm-push` hoặc xác nhận để ngoài NLM có chủ ý.")
    out = {
        "query": q,
        "query_key": qkey or None,
        "canonical": _summ_entry_source_map(canonical),
        "mode": "vbhn_related" if related_vbhn else ("direct_sohieu" if direct else "name" if by_name else "not_found"),
        "direct_hits": [_summ_entry_source_map(e) for e in sorted(direct, key=_entry_score, reverse=True)[:10]],
        "name_hits": [_summ_entry_source_map(e) for e in sorted(by_name, key=_entry_score, reverse=True)[:10]],
        "related_vbhn": [_summ_entry_source_map(e) for e in sorted(related_vbhn, key=_entry_score, reverse=True)[:10]],
        "amends_vbhn": [(_summ_entry_source_map(e) or {}) | {"vbhn_base": _vbhn_base_key(e)} for e in sorted(amends_vbhn, key=_entry_score, reverse=True)[:10]],
        "goc_mismatch_vbhn": [(_summ_entry_source_map(e) or {}) | {"registry_goc": _entry_goc(e), "name_goc_base": _name_goc_base_key(_entry_name(e))} for e in sorted(goc_mismatch_vbhn, key=_entry_score, reverse=True)[:10]],
        "consolidated_amendments": [_summ_entry_source_map(e) for e in sorted(consolidated_amendments, key=_entry_score, reverse=True)[:10]],
        "amendment_candidates": [(_summ_entry_source_map(e) or {}) | {"linked_to_query": bool(e.get("_amendment_linked_to_query")), "subject_overlap": e.get("_amendment_subject_overlap", 0), "confidence": e.get("_amendment_confidence", "low"), "strong": bool(e.get("_amendment_strong")), "omnibus": bool(e.get("_amendment_omnibus"))} for e in amendment_candidates[:10]],
        "unlinked_amendment_candidates": [(_summ_entry_source_map(e) or {}) | {"subject_overlap": e.get("_amendment_subject_overlap", 0), "confidence": "low"} for e in unlinked_amendments[:10]],
        "pending_future_count": len(pending_future),
        "pending_future": [(_summ_entry_source_map(e) or {}) | {"hieu_luc": hl} for e, hl in sorted(pending_future, key=lambda x: x[1], reverse=True)[:10]],
        "draft_count": len(draft_hits),
        "draft_hits": [_summ_entry_source_map(e) for e in draft_hits[:10]],
        "nlm_gap_count": len(nlm_gaps),
        "nlm_gaps": [_summ_entry_source_map(e) for e in nlm_gaps[:10]],
        "risky_candidates": risky[:10],
        "qt5_search_hints": list(dict.fromkeys((_qt5_search_hints(q, direct or by_name) + _qt5_queries(_derive_subject_from_entries(direct or by_name), qkey or q, ""))))[:8],
        "action_required": "PAUSE_AND_ASK_USER" if _gate_escalate else None,   # v1.29.6 P0b chỉ MẠNH; v1.32.0 A1: confirmed KHÔNG escalate (nhất quán warning)
        "covered_by_vbhn_date": bool(vbhn_date_covered),
        "vbhn_issue_date": vbhn_issue_date,
        "covered_amendment_candidates": [(_summ_entry_source_map(x["entry"]) or {}) | {"issue_date": x["issue_date"]} for x in covered_amendments[:10]],
        "warnings": warnings,
    }
    # 4D (v1.33.30 — MERGE bundle-29, STRUCTURED thay compact-string v1.33.29 ta): item tự mang chi tiết
    # ứng viên sửa đổi (số hiệu/tên/confidence/linked/strong/omnibus) — driver hết phải gọi thêm review-queue.
    _cand_seen: set = set()
    _cand_rows: list = []
    for _kind, _lst in (("amendment", amendment_candidates), ("unlinked_amendment", unlinked_amendments)):
        for _ce in (_lst or [])[:10]:
            _ck = _entry_drive_id(_ce) or _sohieu_key_entry(_ce) or str(id(_ce))
            if _ck in _cand_seen:
                continue
            _cand_seen.add(_ck)
            _row = (_summ_entry_source_map(_ce) or {})
            _row.update({"candidate_type": _kind,
                         "sohieu_key": _sohieu_key_entry(_ce),
                         "linked_to_query": bool(_ce.get("_amendment_linked_to_query")),
                         "subject_overlap": _ce.get("_amendment_subject_overlap", 0),
                         "confidence": _ce.get("_amendment_confidence", "low"),
                         "strong": bool(_ce.get("_amendment_strong")),
                         "omnibus": bool(_ce.get("_amendment_omnibus"))})
            _cand_rows.append(_row)
    out["candidates"] = _cand_rows
    out["candidate_count"] = len(_cand_rows)
    out["flags"] = _warning_codes(warnings)
    # v1.33.25 — schema parity với review-queue: source-map đơn lẻ cũng có flags_all/review_reason.
    out["flags_all"] = list(out["flags"])
    out["review_reason"] = list(out["flags"])
    # v1.33.25 — QT-5 fallback: nếu có cờ web nhưng hint rỗng, sinh query tối thiểu từ canonical/direct/related.
    if not out.get("qt5_search_hints") and (set(out["flags"]) & _RQ_WEB_FLAGS or "QT5_WEB_REQUIRED" in out["flags"]):
        _hint_pool = ([canonical] if canonical else []) + direct + related_vbhn + amends_vbhn + by_name
        _hint_subject = _derive_subject_from_entries(_hint_pool)
        _hint_key = qkey or (_sohieu_key_entry(canonical) if canonical else q)
        _hint_year = str(_sohieu_year(_hint_key) or "")
        out["qt5_search_hints"] = _qt5_queries(_hint_subject, _hint_key, _hint_year)[:8]
    out["verdict"] = _source_map_verdict(out)
    out["qt5_queries"] = out["qt5_search_hints"]   # P1-5 (v1.31.0): vocab thống nhất họ QT-5 {verdict,flags,qt5_queries} — giữ key cũ compat
    return out


def _vb_tier_rank(e: dict) -> int:
    """Thứ bậc hiệu lực VBQPPL để chặn 'cấp dưới sửa cấp trên' (sai thứ bậc): một VB chỉ bị SỬA bởi VB NGANG/CAO hơn.
    5=Hiến pháp/Bộ luật/Luật/NQ-QH/VBHN-VPQH · 4=Pháp lệnh/NQ-UBTVQH · 3=Nghị định/NQ-CP · 2=Thông tư/TTLT/QĐ-TTg · 0=không rõ.
    Khóa theo HẬU TỐ số hiệu (tin cậy nhất), fallback trường `loai`."""
    shraw = (_sohieu_key_entry(e) or str(_entry_sohieu(e) or "")).upper().replace("Đ", "D")
    name = _strip_accents(_entry_name(e)).upper().replace("Đ", "D")
    nameblob = shraw + " " + name              # gồm cả TÊN: dòng rác sohieu=∅ vẫn mang 'ND-CP'/'TT-' trong tên
    loai = _strip_accents(str(e.get("loai") or "")).lower()
    # NĐ/TT/PL: nhận từ TÊN nữa (rac thường mang loại ở tên). LUẬT (QH\d) CHỈ nhận từ số hiệu THẬT (shraw) —
    # tránh nhầm 1 NĐ "quy định chi tiết Luật 57/2024/QH15" thành cấp luật do tên nhúng số hiệu luật khác.
    if "VPQH" in shraw or "hien phap" in loai:
        return 5                                   # Hiến pháp / VBHN của luật (VBHN-VPQH)
    if "UBTVQH" in nameblob or "-PL-" in nameblob or "phap lenh" in loai:
        return 4                                   # Pháp lệnh / NQ-UBTVQH  (xét TRƯỚC QH vì 'UBTVQH' chứa 'QH')
    if re.search(r"QH\d", shraw) or "bo luat" in loai or re.fullmatch(r"luat", loai or "") \
       or loai.startswith("luat ") or "nghi quyet cua quoc hoi" in loai:
        return 5                                   # Bộ luật / Luật / NQ-QH
    if "ND-CP" in nameblob or "nghi dinh" in loai:
        return 3                                   # Nghị định / NQ-CP
    if "TT-" in nameblob or "TTLT" in nameblob or "QD-TTG" in nameblob or "thong tu" in loai or "quyet dinh" in loai:
        return 2                                   # Thông tư / TTLT / QĐ-TTg
    if "nghi quyet" in loai:
        return 4
    return 0


def _query_doctype_tier(q: str) -> int:
    """Bac LOAI van ban NEU TRONG TRUY VAN ten (Luat/Bo luat/Phap lenh) de source-map uu tien hit dung cap, KHONG
    chot ND/TT (tier thap) lam canonical khi nguoi dung hoi 'Luat'. 0 neu query khong neu loai."""
    qn = _strip_accents(str(q or "")).lower().strip()
    if re.match(r"^bo\s+luat\b", qn):
        return 5
    if re.match(r"^phap\s+lenh\b", qn):
        return 4
    if re.match(r"^luat\b", qn):
        return 5
    return 0


def _relation_audit(entries: list[dict], base: str = "", subject: str = "", amendments: list[str] | None = None, footnote_amend_keys: set | None = None) -> dict:
    base_key = norm_sohieu(base.replace("_", "-")) if base else ""
    amendment_keys = {norm_sohieu(x.replace("_", "-")) for x in (amendments or []) if x}
    base_entries = []
    if base_key:
        base_entries = [e for e in entries if _sohieu_key_entry(e) == base_key]
    if not subject:
        subject = _derive_subject_from_entries(base_entries)
    candidates: list[dict] = []
    cand_reason: dict[str, str] = {}   # drive_id → 'direct'|'ref'|'subject' (vì sao khớp — quyết định backfill)
    vbhn: list[dict] = []
    base_year = _sohieu_year(base_key) or 0
    for e in entries:
        sh = _sohieu_key_entry(e)
        refs = _relation_refs(e)
        sscore = _subject_score(e, subject)
        is_direct_amend = bool(amendment_keys and sh in amendment_keys)
        is_related_amend = bool(base_key and base_key in refs and _is_amendment_like(e))
        is_subject_amend = bool(subject and sscore >= 35 and _is_amendment_like(e) and sh != base_key)
        if base_year and _sohieu_year(sh) and _sohieu_year(sh) < base_year:
            is_subject_amend = False
        if is_direct_amend or is_related_amend or is_subject_amend:
            candidates.append(e)
            did = _entry_drive_id(e) or str(id(e))
            cand_reason[did] = "direct" if is_direct_amend else ("ref" if is_related_amend else "subject")
        if _is_vbhn_entry(e) and ((base_key and base_key in refs) or (subject and sscore >= 35)):
            # P1-4 (v1.31.0): VBHN cấp Bộ + base Luật QH → CHỈ giữ khi goc-chain THẬT dẫn chiếu base (refs);
            # subject-match sscore≥35 một mình KHÔNG đủ (log: VBHN-BGDDT nổi cho Luật Giáo dục 123/2025).
            if _vbhn_agency_mismatch(base_key, e) and not (base_key and base_key in refs):
                continue
            vbhn.append(e)
    candidates = list({(_entry_drive_id(e) or str(id(e))): e for e in candidates}.values())
    candidates.sort(key=_entry_score, reverse=True)
    vbhn = list({(_entry_drive_id(e) or str(id(e))): e for e in vbhn}.values())
    vbhn.sort(key=_entry_score, reverse=True)
    # ── #1 FIX: footnote-map của VBHN là nguồn XÁC THỰC, ưu tiên hơn heuristic trùng chủ đề ──
    # Reason MẠNH NHẤT theo số hiệu (1 số hiệu có thể nhiều entry): direct > ref > subject.
    _reason_rank = {"direct": 3, "ref": 2, "subject": 1}
    key_reason: dict[str, str] = {}
    for e in candidates:
        k = _sohieu_key_entry(e)
        if not k:
            continue
        did = _entry_drive_id(e) or str(id(e))
        r = cand_reason.get(did, "subject")
        if _reason_rank.get(r, 0) > _reason_rank.get(key_reason.get(k, ""), 0):
            key_reason[k] = r
    fn_keys = {norm_sohieu(str(k).replace("_", "-")) for k in (footnote_amend_keys or []) if k}
    def _eligible_sua_doi(k: str) -> bool:
        # direct (user xác nhận qua --amendment) / ref (registry trỏ base) = luôn đủ điều kiện.
        # subject-only (CHỈ trùng chủ đề) = CHỈ khi footnote-map của VBHN xác nhận; không có footnote-map → KHÔNG backfill.
        if key_reason.get(k, "subject") in ("direct", "ref"):
            return True
        return bool(fn_keys) and k in fn_keys
    eligible_keys = sorted(k for k in key_reason if _eligible_sua_doi(k))
    blocked_subject_keys = sorted(k for k in key_reason if not _eligible_sua_doi(k))
    footnote_only_amendments = sorted(fn_keys - set(key_reason)) if fn_keys else []
    missing_links = []
    for e in base_entries:
        sua = {norm_sohieu(x) for x in re.split(r"[;,|]+", str(_entry_sua_doi(e) or "")) if x.strip()}
        # CHỈ backfill sua_doi cho số hiệu ĐỦ ĐIỀU KIỆN (direct/ref/footnote-confirmed) — KHÔNG dùng candidate thô.
        missing = [k for k in eligible_keys if k and k not in sua]
        if missing:
            missing_links.append({"action": "BACKFILL_SUA_DOI_ON_BASE", "drive_id": _entry_drive_id(e),
                                  "sohieu": _entry_sohieu(e), "add": missing,
                                  "evidence": "footnote-map" if fn_keys else "direct/registry-linked"})
    subject_only_review = []
    for e in candidates:
        k = _sohieu_key_entry(e)
        did = _entry_drive_id(e) or str(id(e))
        reason = cand_reason.get(did, "subject")
        refs = _relation_refs(e)
        # #6: BỎ QUA dòng đã CÁCH LY / corpus=false (bản TRÙNG đã quarantine) — KHÔNG đề xuất backfill goc/review (action vô nghĩa → nhiễu).
        if _entry_quarantined(e) or str(e.get("corpus") or "").strip().lower() == "false":
            continue
        if reason == "direct" and base_key and base_key not in refs:
            # CHỈ amendment XÁC THỰC (base liệt kê nó ở amendment_keys) mới đề xuất set_goc.
            missing_links.append({"action": "BACKFILL_GOC_ON_AMENDMENT", "drive_id": _entry_drive_id(e),
                                  "sohieu": _entry_sohieu(e), "set_goc": base})
        elif reason == "subject" and k not in eligible_keys:
            # Trùng CHỦ ĐỀ nhưng KHÔNG tham chiếu base & KHÔNG trong footnote-map → KHÔNG auto-backfill (dương tính giả #1/#3).
            subject_only_review.append({"sohieu": _entry_sohieu(e), "name": _entry_name(e)[:90],
                                        "in_footnote_map": False,
                                        "note": ("Trùng chủ đề nhưng KHÔNG có trong footnote-map của VBHN — KHÔNG ghi sua_doi/goc; xác minh nguyên văn thủ công."
                                                 if fn_keys else
                                                 "Trùng chủ đề, CHƯA tham chiếu base — xác minh nội dung thủ công, KHÔNG set_goc/sua_doi tự động.")})
    warnings = []
    if candidates:
        warnings.append("AMENDMENT_FOUND_IN_CORPUS: có văn bản sửa đổi trong corpus/NLM; không được kết luận corpus thiếu văn bản.")
    if subject_only_review:
        warnings.append("SUBJECT_ONLY_CANDIDATES: có ứng viên CHỈ trùng chủ đề (không tham chiếu base) — "
                        "KHÔNG đề xuất backfill goc/sua_doi cho chúng; phải đọc nguyên văn xác minh quan hệ trước khi kết luận.")
    if fn_keys and blocked_subject_keys:
        warnings.append("SUBJECT_ONLY_BLOCKED_BY_FOOTNOTE: ứng viên trùng chủ đề KHÔNG xuất hiện trong footnote-map của VBHN đã bị loại khỏi backfill sua_doi (footnote-map ưu tiên hơn heuristic).")
    if footnote_only_amendments:
        warnings.append("FOOTNOTE_AMENDMENT_NOT_IN_CORPUS: footnote-map của VBHN có văn bản sửa đổi CHƯA thấy trong corpus — nạp QT-5 trước khi kết luận (xem footnote_only_amendments).")
    if missing_links:
        warnings.append("RELATION_BACKFILL_REQUIRED: registry thiếu goc/sua_doi; hỏi người dùng rồi ghi registry trước khi rà soát tiếp.")
    if not vbhn:
        warnings.append("NO_VERIFIED_VBHN_IN_CORPUS: chưa thấy VBHN trong manifest; KHÔNG kết luận không có, phải chạy tìm web QT-5.")
        warnings.append("QT5_WEB_REQUIRED: chạy các truy vấn `vbhn_queries`, gồm cả nguồn secondary như Thư viện Pháp luật để phát hiện nhanh.")
    # Lọc NHIỄU khỏi amendment_candidates: ứng viên CHỈ-trùng-chủ-đề (reason=subject, KHÔNG trong eligible/footnote) đã nằm
    # trong subject_only_review rồi — đừng lặp lại như "ứng viên sửa đổi" (dương-tính-giả: vd 108/2026 với BLLĐ, Luật
    # Thanh niên/Công đoàn theo cụm chủ đề quá rộng). Backfill-gate KHÔNG đổi (chỉ lọc DANH SÁCH HIỂN THỊ).
    def _is_subject_noise(e):
        did = _entry_drive_id(e) or str(id(e))
        return cand_reason.get(did, "subject") == "subject" and _sohieu_key_entry(e) not in eligible_keys
    real_amend = [e for e in candidates if not _is_subject_noise(e)]
    subject_noise_n = len(candidates) - len(real_amend)
    if subject_noise_n:
        warnings.append(f"SUBJECT_ONLY_FILTERED: lọc {subject_noise_n} ứng viên CHỈ-trùng-chủ-đề (không tham chiếu base, không trong "
                        "footnote-map) KHỎI amendment_candidates → chỉ còn ở subject_only_review (giảm dương-tính-giả kiểu 108/2026).")
    out = {
        "ok": True,
        "base": base or None,
        "base_key": base_key or None,
        "subject": subject or None,
        "amendment_keys": sorted(amendment_keys),
        "base_entries": [_summ_entry(e) for e in sorted(base_entries, key=_entry_score, reverse=True)],
        "amendment_candidates": [{"entry": _summ_entry(e), "flags": _relation_candidate_flags(e, base_key, subject)} for e in real_amend[:20]],
        "amendment_candidates_subject_filtered_count": subject_noise_n,
        "vbhn_candidates": [{"entry": _summ_entry(e), "flags": _vbhn_quality_flags(e, subject, {base_key} if base_key else set(), "")} for e in vbhn[:20]],
        "missing_links": missing_links,
        "subject_only_review": subject_only_review,
        "footnote_gate": bool(fn_keys),
        "footnote_amend_keys": sorted(fn_keys),
        "footnote_only_amendments": footnote_only_amendments,
        "blocked_subject_only": blocked_subject_keys,
        "warnings": warnings,
        "vbhn_queries": _qt5_queries(subject, base, ""),
        "google_discovery": _discovery_links(subject or base or "")["links_markdown"],
    }
    # P1-5 (v1.31.0): vocab thống nhất họ QT-5 {verdict, flags, qt5_queries, google_discovery} — driver batch hết
    # đặc-cách từng lệnh. Giữ vbhn_queries (compat). Verdict cùng vocab vbhn-check: REVIEW khi cần người xử
    # (missing_links/footnote-thiếu-corpus/subject-only) · QT5_WEB_REQUIRED khi chưa thấy VBHN · OK còn lại.
    out["qt5_queries"] = out["vbhn_queries"]
    out["flags"] = _warning_codes(warnings)
    out["verdict"] = ("REVIEW" if (missing_links or footnote_only_amendments or subject_only_review)
                      else ("QT5_WEB_REQUIRED" if not vbhn else "OK"))
    return out


def _vbhn_goc_corroborated(vbhn_entry: dict, qkey: str, query_subject: str = "") -> bool:
    """§1.1 (log rà 108 lần): chống registry.goc bị NHIỄM khiến source-map/status redirect VBHN-first SANG SAI văn bản.
    Ca thật: VBHN 'Bảo vệ sức khỏe nhân dân' (tên goc_21-LCT-HDNN8) bị registry.goc=113-2025 (Luật Dân số) → query
    Dân số redirect nhầm sang VBHN Bảo vệ sức khỏe. True chỉ khi quan hệ goc=qkey được CORROBORATE:
      • tên VBHN mã hoá base (goc_<base>) phải KHỚP qkey (nếu tên có mã hoá), VÀ
      • chủ đề truy vấn KHÔNG xung khắc lĩnh vực với chủ đề VBHN (BHXH↔BHYT…).
    Tên không mã hoá base + không xung khắc chủ đề → vẫn tin registry.goc (giữ tương thích VBHN chưa đặt tên goc_)."""
    name_base = _name_goc_base_key(_entry_name(vbhn_entry))
    if name_base and qkey and name_base != qkey:
        return False
    if query_subject and _disc_conflict(query_subject, _entry_subject_text(vbhn_entry)):
        return False
    return True


def _is_vbhn_entry(e: dict) -> bool:
    txt = " ".join(str(x or "") for x in (_entry_sohieu(e), e.get("loai"), _entry_name(e))).upper()
    return "VBHN" in txt or "VAN BAN HOP NHAT" in _strip_accents(txt).upper()


def _vbhn_metadata_flags(e: dict, tail: str) -> list[str]:
    if not _is_vbhn_entry(e):
        return []
    flags = []
    issue_year = _entry_issue_year(e)
    raw = norm_sohieu(_entry_sohieu(e) or "")
    name = _entry_name(e)
    sh_key = _sohieu_key_entry(e)
    # v1.29.6 (log 118 Luật — P2.2: VBHN_NUMBER_REUSE_RISK nổ trên MỌI VBHN kể cả bản ĐÃ CÓ NĂM trong sohieu-key
    # như VBHN_133-2025 → kéo TITLE_OR_REGISTRY_WARN nhiễu 24×): sohieu-key dạng chuẩn NN-YYYY-VBHN-XXX = năm ĐÃ
    # XÁC ĐỊNH (bất biến đặt tên) → coi như biết năm, KHÔNG cờ thiếu-năm dù _entry_issue_year không suy được.
    _key_m = _VBHN_WITHYEAR_RE.fullmatch(sh_key or "")
    _key_year = int(_key_m.group(2)) if _key_m else None
    _known_years = {y for y in (issue_year, _key_year) if y}
    # B4 (v1.33.0 — log rà 15: ca 25-2025 'Luat_Ke_toan' bị coi TÊN TRƠ → kéo REUSE_RISK + TITLE_WARN oan):
    # _token_set bỏ 'luat' (stop-word) + 'ke' (ngắn) nên tail CÓ chủ đề vẫn đếm <2. Fallback: đếm TỪ-CHỮ ≥2 ký tự
    # trong tail — 'luat ke toan' = 3 từ = có chủ đề; tail rỗng/'hopnhat' đơn độc vẫn là trơ đúng.
    if len(_token_set(tail)) < 2 and len(re.findall(r"[a-z]{2,}", _ascii_lower(tail))) < 2:
        flags.append("VBHN_BARE_NUMBER")
    if not _known_years:
        flags.append("VBHN_MISSING_YEAR_OR_DATE")
    agency = _vbhn_agency_from_key(sh_key)
    if re.fullmatch(r"\d{1,4}-VBHN-VPQH", raw) and "VBHN" not in str(_entry_sohieu(e) or "").upper():
        flags.append("VBHN_SOHIEU_NORMALIZED_FROM_SHORT_VPQH")
    _year_in_name = any(re.search(rf"(?<!\d){y}(?!\d)", name or "") for y in _known_years)
    if _known_years and not _year_in_name:
        flags.append("VBHN_NAME_MISSING_YEAR")
    if agency and agency != "VPQH":
        flags.append("VBHN_MINISTRY_SCOPE")
        if not _known_years:
            flags.append("VBHN_MINISTRY_MISSING_YEAR")
        elif not _year_in_name:
            flags.append("VBHN_MINISTRY_NAME_MISSING_YEAR")
    return flags


def _vbhn_sohieu_inject_year(sohieu_key: str, year) -> str | None:
    """`61-VBHN-VPQH` + 2025 → `61-2025-VBHN-VPQH`. None nếu sohieu KHÔNG phải VBHN-thiếu-năm hoặc year rỗng/sai."""
    m = _VBHN_NOYEAR_RE.fullmatch(norm_sohieu(sohieu_key or ""))
    try:
        y = int(year)
    except (TypeError, ValueError):
        return None
    if not m or not (1900 <= y <= 2100):
        return None
    return f"{m.group(1)}-{y}-VBHN-{m.group(2)}"


def _name_inject_vbhn_year(name: str, number: str, year, agency: str) -> str:
    """Chèn năm vào token số-VBHN trong TÊN (chịu / - _ phân tách); idempotent (đã có năm → giữ nguyên).
    v1.33.21: nhận CẢ dạng NGẮN `NN-VPQH` (thiếu segment VBHN — ca thật 'VBHN_34-VPQH_Luat_Luu_tru': trước trả
    nguyên tên → lane name-only câm với đúng lớp cần sửa nhất)."""
    if not name or not year:
        return name
    pat = re.compile(rf"(?<!\d){re.escape(str(number))}([/_-])VBHN([/_-]){re.escape(str(agency))}(?![A-Za-z0-9])")
    out = pat.sub(rf"{number}\g<1>{year}\g<1>VBHN\g<2>{agency}", name)
    if out != name:
        return out
    # dạng NGẮN 'NN-VPQH' (không có 'VBHN' giữa) → chuẩn hoá thẳng về NN-YYYY-VBHN-XXX
    pat2 = re.compile(rf"(?<!\d){re.escape(str(number))}([/_-]){re.escape(str(agency))}(?![A-Za-z0-9])")
    return pat2.sub(rf"{number}\g<1>{year}\g<1>VBHN\g<1>{agency}", name)


def _field_text(e: dict, keys: tuple[str, ...]) -> str:
    vals = []
    for k in keys:
        v = e.get(k)
        if isinstance(v, (list, tuple, set)):
            vals.extend(str(x) for x in v if x)
        elif isinstance(v, dict):
            vals.extend(str(x) for x in v.values() if x)
        elif v:
            vals.append(str(v))
    return " ".join(vals)


def _flags_reason(flags: list) -> str:
    """Diễn giải NGẮN GỌN cho mỗi cờ rủi ro (vá log: risky_candidates trước đây trống trường lý do)."""
    parts = [_FLAG_REASONS.get(f, f) for f in (flags or [])]
    return "; ".join(dict.fromkeys(parts))


def _resolve_deep_target(target: str, entries: list[dict]) -> tuple[dict | None, str, str, list[dict]]:
    """Resolve target (gdocId|số hiệu|tên) cho lệnh đọc sâu → (entry tốt nhất, gid, name, danh sách ranked).
    Ưu tiên GDoc/corpus/live thay vì sidecar raw/quarantine. Trả (None,target,target,[]) nếu không có hit."""
    target = str(target or "").strip()
    if not target:
        return None, "", "", []
    cands: list[dict] = []
    cands.extend([e for e in entries if _entry_drive_id(e) == target])          # khớp drive_id chính xác
    qkey = norm_sohieu(target.replace("_", "-")) if _looks_like_sohieu_query(target) else ""
    if qkey:
        cands.extend([e for e in entries if _sohieu_key_entry(e) == qkey])      # khớp số hiệu
    cands.extend([e for e, _s, _r in resolve_identity(target, entries, max_hits=8)])  # LUÔN thử theo tên/alias
    seen, uniq = set(), []
    for e in cands:
        k = _entry_drive_id(e) or id(e)
        if k in seen:
            continue
        seen.add(k); uniq.append(e)

    # v1.29.7 (log NĐ131 #2): query SỐ HIỆU có ≥2 ứng viên (chính văn + PHỤ LỤC cùng khớp '131-2021') từng chọn
    # NHẦM phụ lục (dù sohieu rỗng, tên PL_). Tie-break: (a) registry-sohieu KHỚP THẬT qkey (+150 — thắng bản chỉ
    # parse-từ-tên); (b) tên dạng PHỤ LỤC (PL_/Phu_luc đầu tên) −120 (bản PHỤ không làm canonical cho query số hiệu).
    def _rk(e):
        r = _deep_entry_rank(e)
        if qkey:
            if norm_sohieu(str(_entry_sohieu(e) or "")) == qkey:
                r += 150
            if re.match(r"^(pl|phu[\s_]?luc)[\s_\-]", _strip_accents(_entry_name(e)).lower()):
                r -= 120
        return r

    uniq.sort(key=_rk, reverse=True)
    if not uniq:
        return None, target, target, []
    best = uniq[0]
    return best, (_entry_drive_id(best) or ""), _entry_name(best), uniq


def _split_distinct_vbhn_docs(arr: list[dict]) -> list[list[dict]]:
    """Chia nhóm CÙNG SỐ HIỆU thành các VĂN BẢN KHÁC NHAU theo XUNG ĐỘT metadata: 2 entry là khác-document nếu
    NĂM ban hành rời nhau (cùng có) HOẶC goc rời nhau (cùng có). Entry thiếu cả năm lẫn goc → KHÔNG xung đột với
    ai → gộp vào doc có sẵn. Phân biệt reuse-thật (vd 14/VBHN: ATVSLĐ-2024 vs NLĐ-2023, năm khác) với nhân-đôi
    cùng-document (vd 18/VBHN BLLĐ: GDoc 2026 + .docx thiếu năm). Xếp entry CÓ metadata trước để neo nhóm."""
    groups: list[dict] = []

    def conflict(g, ys, gos):
        if ys and g["years"] and not (ys & g["years"]):
            return True
        if gos and g["gocs"] and not (gos & g["gocs"]):
            return True
        return False

    for e in sorted(arr, key=lambda x: (bool(_entry_years(x)) or bool(_goc_keys(x))), reverse=True):
        ys, gos = set(_entry_years(e)), set(_goc_keys(e))
        g = next((g for g in groups if not conflict(g, ys, gos)), None)
        if g is None:
            g = {"years": set(), "gocs": set(), "entries": []}
            groups.append(g)
        g["years"] |= ys
        g["gocs"] |= gos
        g["entries"].append(e)
    return [g["entries"] for g in groups]


def _vbhn_subject_key(e: dict) -> str:
    """Tách các VBHN tái sử dụng cùng số theo năm/chủ đề/gốc."""
    y = str(_entry_issue_year(e) or "")
    refs = sorted(_goc_keys(e) | _ref_tokens(_field_text(e, _REF_KEYS + _META_TITLE_KEYS)))
    tail = _name_tail_key(_entry_name(e))
    # Bỏ năm trong tail để bản GDoc và file gốc cùng năm vẫn nhập cụm.
    tail = re.sub(r"\b(?:20\d{2}|19\d{2})\b", " ", tail)
    tail = re.sub(r"\s+", " ", tail).strip()
    if refs:
        return "G" + ",".join(refs[:6])
    if y or tail:
        return "Y" + y + ":T" + tail
    return "UNKNOWN"


def _dup_of_live_sibling(e: dict, group: list[dict]) -> bool:
    """True nếu `e` (corpus, KHÔNG trên NLM live) chỉ là BẢN SAO/SIDECAR của một anh-em CÙNG
    văn bản trong nhóm ĐÃ trên NLM live → KHÔNG báo nhầm CORPUS_TRUE_NOT_ON_NLM cho dòng phụ
    (GDoc trùng `..._m_<id>`, file gốc .doc/.docx/.pdf cạnh GDoc). An toàn va-chạm-số-hiệu: yêu cầu
    CÙNG dedupe-key (VBHN khóa theo chủ đề/gốc) VÀ (md5 trùng HOẶC chủ-đề-tail không mâu thuẫn —
    1 bên rỗng/coded HOẶC chứa nhau). Bản thô CÙNG số nhưng KHÁC chủ đề (vd 60/2024 Phòng_bệnh vs
    Dữ_liệu, 67/2006 NLĐ vs CNTT) VẪN bị flag — đó là gap thật, không suppress."""
    if _entry_on_nlm_live(e):
        return False
    dk = _dedupe_key_entry(e)
    if not dk:
        return False
    def _topic(x: dict) -> str:
        sig = _subject_sig(_entry_name(x))
        return re.sub(r"^(?:luat|bo|nghidinh|thongtu|quyetdinh|chithi|nghiquyet|hopnhat|goc|nd|ndcp|cp|tt|qd|nq|ct|pl|vbhn|vpqh|m|qh|ubtvqh)+", "", sig)
    et = _topic(e)
    emd5 = _entry_md5(e)
    for s in group:
        if s is e or not _entry_on_nlm_live(s):
            continue
        if emd5 and emd5 == _entry_md5(s):
            return True
        if _dedupe_key_entry(s) != dk:
            continue
        st = _topic(s)
        if (not et) or (not st) or et == st or et in st or st in et:
            return True
    return False


def _warning_codes(warnings: list[str]) -> list[str]:
    """Mã cờ = tiền tố MÃ dẫn đầu warning (mọi warning format `CODE_NAME: mô tả` hoặc mã trần). CHỈ lấy mã dẫn đầu →
    `flags` SẠCH cho driver máy-đọc, KHÔNG nhặt token IN-HOA phụ trong phần mô tả (vd 'VBHN'/'NLM' trong câu chữ)."""
    out = []
    for w in warnings or []:
        head = str(w or "").split(":", 1)[0].strip()
        if re.fullmatch(r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*", head) and head not in out:
            out.append(head)
    return out


def _aggregate_verdict(items: list[dict]) -> str:
    verdicts = [it.get("verdict") for it in items or []]
    if any(v == "PAUSE_AND_ASK_USER" for v in verdicts):
        return "PAUSE_AND_ASK_USER"
    if any(v == "REVIEW" for v in verdicts):
        return "REVIEW"
    if verdicts and all(v == "UNKNOWN_NOT_ABSENT" for v in verdicts):
        return "UNKNOWN_NOT_ABSENT"
    return "OK"


def _vbhn_quality_flags(e: dict, subject: str = "", goc_keys: set[str] | None = None, year: str = "") -> list[str]:
    flags = list(_title_flags(e))
    if _is_vbhn_entry(e):
        yrs = _entry_years(e)
        if year and year not in yrs and year not in _entry_name(e):
            flags.append("VBHN_YEAR_NOT_IN_METADATA")
        if "VBHN_BARE_NUMBER" in flags:
            flags.append("VBHN_NAME_MISSING_SUBJECT")
    if subject and _subject_score(e, subject) < 30:
        flags.append("SUBJECT_NOT_EVIDENT_IN_METADATA")
    if goc_keys:
        refs = _goc_keys(e) | _ref_tokens(_field_text(e, _REF_KEYS + _META_TITLE_KEYS))
        if not (refs & goc_keys):
            flags.append("GOC_NOT_EVIDENT_IN_METADATA")
    out = []
    for f in flags:
        if f not in out:
            out.append(f)
    return out


def _vbhn_scan(entries: list[dict]) -> dict:
    vbhn = [e for e in entries if _is_vbhn_entry(e)]
    by_num: dict[str, list[dict]] = {}
    missing_subject = []
    for e in vbhn:
        k = norm_sohieu(_entry_sohieu(e) or _parse_sohieu_from_name(_entry_name(e)))
        if k:
            by_num.setdefault(k, []).append(e)
        flags = _vbhn_quality_flags(e)
        if "VBHN_BARE_NUMBER" in flags or "VBHN_MISSING_YEAR_OR_DATE" in flags or "VBHN_NAME_MISSING_SUBJECT" in flags:
            missing_subject.append(e)
    collisions = []
    for k, arr in by_num.items():
        if len(arr) > 1:
            years = sorted(set().union(*[_entry_years(x) for x in arr]))
            collisions.append({"key": k, "years": years, "entries": sorted(arr, key=_entry_score, reverse=True)})
    return {"vbhn_count": len(vbhn), "collisions": collisions, "missing_subject": missing_subject}


def _vbhn_latest_low_priority_recent_law(subject: str, goc: str, year: str, has_candidates: bool) -> bool:
    """S-8b (v1.33.16 — MERGE nhánh-4, PURE): vbhn-check trên LUẬT RẤT MỚI chưa có ứng viên VBHN nào trong
    corpus không nên gắn VBHN_CANDIDATE_UNVERIFIED_LATEST nặng như luật ĐÃ có VBHN chưa xác minh mới nhất —
    QT5_WEB_REQUIRED giữ nguyên, chỉ hạ riêng cờ latest. Điều kiện: không candidate + năm luật (từ --year hoặc
    sohieu goc) ≥ năm-nay−2 [ĐỘNG — nhánh-4 hardcode 2024 sẽ mục theo thời gian] + không thuộc nhóm dồn dập."""
    if has_candidates:
        return False
    y = 0
    try:
        y = int(str(year or "").strip()[:4]) if str(year or "").strip() else 0
    except (TypeError, ValueError):
        y = 0
    if not y and goc:
        y = _sohieu_year(norm_sohieu(goc)) or 0
    if not y or y < time.localtime().tm_year - 2:
        return False
    return not (_is_high_amendment_subject(subject) or _is_high_amendment_subject(goc))


def _vbhn_agency_mismatch(base_key: str, e: dict) -> bool:
    """P1-4 (v1.31.0, PURE): True khi ứng viên là VBHN CẤP BỘ/ngành (VBHN-BTP/BGDDT/BTC/NHNN…) mà base là văn bản
    QUỐC HỘI (…-QHxx/UBTVQH/LCT-HDNN/Pháp lệnh). VBHN cấp Bộ hợp nhất NĐ/TT — KHÔNG BAO GIỜ là VBHN của Luật QH
    (VBHN của Luật do VPQH ban hành). Log LIVE 2026-07-03: 4231-2025-VBHN-BTP (NĐ) score 158 nổi làm candidate
    Luật 90/2025; loạt VBHN-BGDDT nổi cho Luật Giáo dục 123/2025. Agency rỗng/VPQH → KHÔNG chặn."""
    bk = str(base_key or "")
    # base QH-family: Luật/Bộ luật/NQ-QH (…-QHxx) · Pháp lệnh/NQ-UBTVQH (…-UBTVQHxx) · luật trước-1992 (LCT-HDNN).
    if not bk or not re.search(r"-QH\d+$|-UBTVQH\d+$|LCT-HDNN", bk):
        return False
    ag = _vbhn_agency_from_key(_sohieu_key_entry(e))
    return bool(ag) and ag != "VPQH"


def _vbhn_candidates(entries: list[dict], subject: str = "", goc: str = "", year: str = "") -> list[dict]:
    gkeys = {norm_sohieu(goc)} if goc else set()
    # #7: số hiệu ĐÃ có bản NLM → bản .docx/.pdf thô cùng số hiệu là THỪA. (GIỮ .docx VBHN mới CHƯA-NLM để người
    # dùng vẫn thấy lúc vừa tải về — tránh regression mà workflow xác minh chỉ ra.)
    _nlm_keys = {_sohieu_key_entry(e) for e in entries if _entry_nlm(e) and _sohieu_key_entry(e)}
    out = []
    for e in entries:
        if not _is_vbhn_entry(e):
            continue
        # Bỏ file gốc thô (.doc/.docx/.pdf, KHÔNG nằm NLM) khi: là sidecar, HOẶC số hiệu rỗng, HOẶC đã có bản NLM
        # TRÙNG số hiệu (bản thô thừa — vd "000.01…18_VBHN-VPQH.docx" hay "108-VBHN-VPQH.docx" cạnh GDoc NLM).
        _raw_doc = (not _entry_nlm(e)) and bool(re.search(r"\.(docx?|pdf)$", _entry_name(e), re.IGNORECASE))
        if _is_source_sidecar(e, entries) or (
                _raw_doc and ((not _entry_sohieu(e)) or (_sohieu_key_entry(e) in _nlm_keys))):
            continue
        refs = _goc_keys(e) | _ref_tokens(_field_text(e, _REF_KEYS + _META_TITLE_KEYS))
        # A3: loại trừ chéo lĩnh vực ngay (BHXH↔BHYT… dù trùng năm/tiền tố) — đừng để lọt ứng viên khác bản chất.
        if subject and _disc_conflict(subject, _entry_subject_text(e)):
            continue
        sscore = _subject_score(e, subject)
        yscore = 20 if (year and year in _entry_years(e)) else 0
        gscore = 80 if (gkeys and refs & gkeys) else 0
        goc_hit = bool(gkeys and refs & gkeys)
        # #2/A3: goc-ref = tín hiệu mạnh. subject≥60 = trùng tên/đủ token. **year CHỈ tính KHI subject cũng liên quan
        # (≥30)** — year-MỘT-MÌNH kéo nhầm VBHN khác lĩnh vực cùng năm. Không có subject → year là tín hiệu duy nhất.
        # 5.2 (report rà 106 Luật): goc_hit cross-subject LỌT khi `_disc_conflict` KHÔNG biết cặp (vd 'du lịch' vs 'lao
        # động' → 14-2024 ATVSLĐ lọt vào --goc 09-2017 Du lịch). FIX: khi ĐÃ biết subject (truyền/suy từ goc), goc_hit
        # phải TƯƠNG THÍCH chủ đề (sscore≥30) — chặn bare-number/goc-ref nhiễu khác lĩnh vực. subject rỗng → goc_hit
        # vẫn nhận (không có chủ đề để đối chiếu).
        goc_keep = goc_hit and ((not subject) or sscore >= 30)
        # P1-4 (v1.31.0): base --goc là văn bản QH + ứng viên VBHN CẤP BỘ (hợp nhất NĐ/TT) → LOẠI khi KHÔNG có
        # goc-chain dẫn chiếu base (subject/year-match KHÔNG đủ bằng chứng — chặn 4231-VBHN-BTP nổi cho Luật 90/2025).
        if gkeys and not goc_hit and _vbhn_agency_mismatch(next(iter(gkeys)), e):
            continue
        keep = (goc_keep
                or (subject and sscore >= 60)
                or (subject and sscore >= 30 and yscore)
                or (not subject and yscore))
        if keep:
            out.append((gscore + sscore + yscore + _entry_score(e), e))
    out.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in out]


def _vbhn_official_flags(text: str, source_name: str = "", official_required: bool = False,
                         allow_provisional: bool = False) -> list[str]:
    """Guard quy trình: bản tự ghép chỉ được là bản tạm, không được chốt làm canonical."""
    blob = unicodedata.normalize("NFC", (source_name or "") + "\n" + (text or "")[:30000])
    norm = _strip_accents(blob).lower().replace("_", " ")
    flags = []
    # vbhn_verify_header_unread: marker 'tự ghép'/'không dùng'/'zzz_assembled' là tín hiệu ĐẶT-TÊN-FILE/quarantine —
    # CHỈ soi SOURCE_NAME, KHÔNG soi thân văn bản (vd 'không đúng'='khong dung' trong thân luật bình thường → ASSEMBLED giả).
    name_norm = _strip_accents(source_name or "").lower().replace("_", " ")
    assembled = any(h in name_norm for h in _ASSEMBLED_HINTS)
    if assembled and not allow_provisional:
        flags.append("ASSEMBLED_VBHN_NOT_ALLOWED_AS_CANONICAL")
    if official_required:
        official_hit = any(h in norm for h in _OFFICIAL_HINTS)
        if not official_hit:
            flags.append("OFFICIAL_SOURCE_NOT_CONFIRMED")
        if not re.search(r"\[\d+\]", blob):
            flags.append("VBHN_FOOTNOTES_NOT_EVIDENT")
    return flags


def _vbhn_verdict(flags: list[str], allow_provisional: bool = False) -> tuple[str, bool, bool]:
    """Suy verdict tường minh từ flags: OFFICIAL_OK / PROVISIONAL / FAIL.
    official = qua gate sạch (không flags) và không phải bản tạm/tự ghép;
    provisional = chạy ở chế độ bản tạm (--allow-provisional) hoặc bị bắt là bản tự ghép."""
    flags = list(flags or [])
    provisional = bool(allow_provisional) or ("ASSEMBLED_VBHN_NOT_ALLOWED_AS_CANONICAL" in flags)
    official = (not flags) and not provisional
    verdict = "FAIL" if flags else ("OFFICIAL_OK" if official else "PROVISIONAL")
    return verdict, official, provisional


def resolve_identity(q: str, entries: list, max_hits: int = 8) -> list:
    """Giải danh tính chuẩn hóa: khớp qua SỐ HIỆU (chuẩn hóa) → tên/name_key → alias trên
    _entry_subject_text (gồm name+title_vn+trichyeu+TUKHOA+nlm_title+cat). Trả [(entry, score, reasons)]
    đã xếp hạng. Đây là bộ DÙNG CHUNG cho exists/source-map/dedup/xref/ingest-route (WS1)."""
    key = norm_sohieu(q)
    qn = _strip_accents(q).lower()
    qnk = _name_key(q)
    aterms = _alias_terms(q)
    out = []
    for e in entries:
        sh = norm_sohieu(_entry_sohieu(e))
        subj = _strip_accents(_entry_subject_text(e)).lower()
        nm = _strip_accents(_entry_name(e)).lower()
        nk = _name_key(_entry_name(e))
        score, reasons = 0, []
        if key and sh and sh == key:
            score += 100; reasons.append("sohieu")
        if qn and len(qn) >= 4 and qn in nm:
            score += 40; reasons.append("name_substr")
        if qnk and nk and (qnk in nk or nk in qnk):
            score += 30; reasons.append("name_key")
        hit_alias = [t for t in aterms if len(t) >= 3 and t in subj]
        if hit_alias:
            score += 20 + min(len(hit_alias), 3)
            reasons.append("alias/tukhoa:" + ",".join(sorted(hit_alias)[:3]))
        # B2 (port Codex): khớp tên theo TOKEN-subset (gồm subject) → bắt 'Luật Thư viện'↔'Luat_46-2019-QH14_Thu_vien'
        # khi substring/name_key hổng (số hiệu chèn giữa). Tăng độ tất định của dedup-check/identity resolver.
        if _entry_query_match(q, e, include_subject=True):
            score += 35; reasons.append("name_tokens")
        if score > 0:
            out.append((e, score + _entry_score(e) // 10, reasons))
    out.sort(key=lambda t: t[1], reverse=True)
    return out[:max_hits]


def _sohieu_typo_near(cited: str, entries: list, name_q: str = ""):
    """Số hiệu dẫn-chiếu KHÔNG khớp exact nhưng CÓ near-match trong corpus → gợi ý typo.
    (1) cùng SỐ+NĂM, KHÁC mã cơ quan/loại (vd QH14↔QH15) = typo mã. r278/F12: tích lũy DUY-NHẤT-THEO-SỐ-HIỆU
        (last-wins cũ trỏ bừa theo thứ tự manifest — nền có 26 nhóm (số,năm,họ) ≥2 mã đồng tồn tại hợp pháp:
        TT đa-bộ, luật↔VBHN-VPQH cùng số+năm); ≥2 số hiệu → corroborate tên; vẫn mơ hồ → (None, [sh...])
        để caller hạ conf + liệt kê, KHÔNG tự chọn.
    (2) cùng NĂM+mã, số thứ tự lệch 1 chữ số = typo số, CHỈ nhận khi tên (loai+name) đối chiếu DUY NHẤT
        1 SỐ HIỆU (r278: đếm theo số hiệu — identity-dup 2 bản/1 văn bản từng làm len(corro)=2 → từ chối oan).
    Trả: None | (entry, sohieu) | (None, [sohieu, ...]) khi vế (1) mơ hồ ≥2."""
    m = _SOHIEU_PARTS_RE.fullmatch(cited or "")
    if not m:
        return None
    cn, cy, ca = m.group(1), m.group(2), m.group(3)
    agency_cands, num_cands = {}, []   # sh → entry đại diện (max _entry_score, tie giữ bản gặp trước — khuôn r272)
    for e in entries:
        sh = norm_sohieu(_entry_sohieu(e))
        if sh == cited:
            return None   # số hiệu dẫn TỒN TẠI đúng → không phải typo
        em = _SOHIEU_PARTS_RE.fullmatch(sh)
        if not em:
            continue
        en, ey, ea = em.group(1), em.group(2), em.group(3)
        # P0-2: cùng SỐ+NĂM, KHÁC mã cơ quan = typo CHỈ KHI cùng HỌ loại văn bản (QH14↔QH15). Khác họ
        # (QH ↔ NQ-TW/NĐ-CP…) = tái dùng số+năm hợp pháp → KHÔNG phải typo (hết gợi ý ảo xuyên-không-gian).
        if en == cn and ey == cy and ea != ca and _doctype_family(ca) == _doctype_family(ea):
            if sh not in agency_cands or _entry_score(e) > _entry_score(agency_cands[sh]):
                agency_cands[sh] = e
        elif ey == cy and ea == ca and _sohieu_num_typo(cn, en):
            num_cands.append((e, sh))

    def _corro_sh():
        # tập SỐ HIỆU của các hit resolve theo tên — corroborate đếm theo số hiệu, miễn nhiễm identity-dup
        return {norm_sohieu(_entry_sohieu(he)) for he, _s, _r in resolve_identity(name_q, entries, max_hits=8)}

    if len(agency_cands) == 1:
        sh, e = next(iter(agency_cands.items()))
        return (e, sh)
    if len(agency_cands) >= 2:
        if name_q:
            corro = sorted(agency_cands.keys() & _corro_sh())
            if len(corro) == 1:
                return (agency_cands[corro[0]], corro[0])
        return (None, [sh for sh, _e in sorted(agency_cands.items(), key=lambda kv: (-_entry_score(kv[1]), kv[0]))])
    if name_q and num_cands:
        corro = sorted({sh for _e, sh in num_cands} & _corro_sh())
        if len(corro) == 1:
            e = max((e for e, sh in num_cands if sh == corro[0]), key=_entry_score)
            return (e, corro[0])
    return None


def _vbhn_for_goc(sohieu_key: str, entries: list) -> list:
    """Các entry VBHN/bản hợp nhất có 'goc' chứa số hiệu này → tín hiệu OUTDATED.
    r270: so THEO TẬP KHÓA `_goc_keys` (bóc từng phần ;,| rồi norm — cùng bộ với _vbhn_base_key), KHÔNG
    substring trên blob JSON như trước: norm_sohieu(gtxt) giữ nguyên chuỗi số nên '6-2012-QH13' khớp LỌT
    goc '16/2012/QH13' (không biên từ) ⇒ _classify_ref gắn OUTDATED giả «đã được VBHN bao phủ» cho dẫn
    chiếu THIẾU thật trong corpus — che MISSING/TYPO, đúng chiều nguy hiểm (đo 31-07: cited '1-2020-QH14'
    ↔ goc '41/2020/QH14' → OUTDATED). Đo 3 registry thật: goc chỉ chứa sohieu sạch/danh sách ;— exact-set
    không mất ca nào so substring, chỉ mất ca khớp-lọt."""
    key = norm_sohieu(str(sohieu_key or "").replace("_", "-"))
    if not key:
        return []
    out = []
    for e in entries:
        goc = e.get("goc")
        gtxt = json.dumps(goc, ensure_ascii=False) if isinstance(goc, (list, dict)) else str(goc or "")
        if gtxt and key in _goc_keys(e):
            if _is_vbhn_entry(e) or "VBHN" in gtxt.upper():
                out.append(e)
    return out


def _scan_inline_amendments(text: str) -> list:
    """E1 liên-domain: số hiệu luật KHÁC bị base sửa cấp Điều (outgoing) từ tiêu đề điều-khoản-thi-hành
    "Sửa đổi, bổ sung [một số điều của] Luật ... số <sh>". KHÔNG bắt repeal "Bãi bỏ ... của Luật ... số X"
    (động từ sửa phải liền trước "Luật") hay recital "Luật số X đã được sửa đổi". Trả list sohieu chuẩn hoá, dedup."""
    out, seen = [], set()
    for m in _INLINE_AMEND_RE.finditer(unicodedata.normalize("NFC", text or "")):
        sh = norm_sohieu(m.group("sh"))
        if sh and sh not in seen:
            seen.add(sh); out.append(sh)
    return out


def resolve_footnote_amendments(text: str, today: str | None = None, entries: list | None = None) -> dict:
    """B3 def-driven: MỖI chú thích '[n] …' = 1 bản ghi ĐỘC LẬP (không mượn số/đích/luật marker khác).
    B2: hiệu_lực từ chú thích ('có hiệu lực kể từ ngày…') hoặc registry (entries) theo số hiệu luật sửa; pending_effect = hl>today."""
    import datetime as _dt
    txt = unicodedata.normalize("NFC", text or "")
    # r277 (F10): extract .docx có thể còn cặn field-code Word « HYPERLINK \l "_ftn(ref)N" » và marker dính
    # đôi «[n][n]» ⇒ def trượt mốc `first` ^[n]␣ dưới → foot_region rỗng → footnote-map CÂM không phân biệt
    # được với "doc không có chú thích" (đo 31-07: 18 VBHN nền, ≈1059 marker). Chuẩn hóa TRƯỚC mọi phép tách.
    txt = re.sub(r'HYPERLINK\s*\\+l\s*["“”]_ftn(?:ref)?\d{1,3}["“”]', " ", txt)
    txt = re.sub(r"\[(\d{1,3})\](?:\[\1\])+", r"[\1]", txt)
    # L1: tách dấu dính số-khoản↔số-chú-thích
    txt = re.sub(r"(\d+)\.(\d+[a-zđ]?)\s*\[(\d{1,3})\]", r"\1.\2 [\3]", txt)
    txt = re.sub(r"(?<=[\dA-Za-zđ])\[(\d{1,3})\]", r" [\1]", txt)
    txt = re.sub(r"\[(\d{1,3})\](\d)", r"[\1] \2", txt)
    today = today or _dt.date.today().isoformat()
    # Khối CHÚ THÍCH = từ dòng bắt đầu '[n]' đầu tiên (def ở line-start; marker inline trong thân ở giữa dòng)
    first = re.search(r"(?m)^\s*\[\d{1,3}\]\s", txt)
    foot_region = txt[first.start():] if first else ""
    body_txt = txt[: first.start()] if first else txt
    # body-anchor fallback: marker inline trong thân → Điều/khoản đang theo dõi
    anchor, cur_dieu, cur_khoan = {}, None, None
    for line in body_txt.splitlines():
        dh = _DIEU_HEAD_RE.match(line)
        if dh: cur_dieu = dh.group(1); cur_khoan = None
        kh = _KHOAN_HEAD_RE.match(line)
        if kh: cur_khoan = kh.group(1)
        for mk in _MARK_RE.finditer(line):
            # r277 (F11): khóa marker CHUẨN int — "[01]" số-ô-biểu-mẫu ≠ "[1]" def khi so CHUỖI làm
            # processed-set trượt ⇒ sinh def_missing GIẢ is_amend=True (đo: 12/12 emit toàn corpus = rác NĐ 188).
            anchor.setdefault(str(int(mk.group(1))), (cur_dieu, cur_khoan))
    # Tách def THEO MARKER (không phụ thuộc xuống dòng): mỗi [n] → tới [next]
    rows, processed = [], set()
    marks = [(m.start(), m.end(), str(int(m.group(1)))) for m in _MARK_RE.finditer(foot_region)]   # r277 (F11): khóa chuẩn int
    bracketed = {n for _, _, n in marks}
    # Một số def đánh marker SỐ TRẦN đầu dòng (vd [2] bị viết "\n2 Điểm này được sửa đổi…") → _MARK_RE bỏ sót.
    # CHỈ cứu cho số CÓ anchor trong thân (là footnote thật) + theo sau là ngôn ngữ def (Điểm/Khoản/Điều/Cụm từ).
    for am in anchor:
        if am in bracketed:
            continue
        bm = re.search(r"(?:^|\n)[ \t]*0*" + re.escape(am) + r"[ \t]+(?=(?:Điểm|Khoản|Điều|Cụm từ)\b)", foot_region)   # r277: 0* dung sai zero-pad
        if bm:
            marks.append((bm.start(), bm.end(), am))
    marks.sort()
    max_foot = max((int(n) for _, _, n in marks if n.isdigit()), default=0)
    for i, (mstart, mend, n) in enumerate(marks):
        if n in processed:
            continue
        processed.add(n)                                   # đánh dấu ĐÃ XỬ LÝ (kể cả bỏ) để body-loop không lặp
        end = marks[i + 1][0] if i + 1 < len(marks) else len(foot_region)
        body = re.sub(r"\s+", " ", foot_region[mend:end]).strip()
        rec = _parse_footnote_def(n, body)
        if "căn cứ ban hành" in body.lower():              # Type C: chỉ căn cứ ban hành → KHÔNG sửa đổi ([1])
            continue
        if not rec.get("is_amend"):
            # is_amend=False = def TRÍCH DẪN (vd "Điều 50 của Luật 71/2025 quy định như sau: 'Điều 50. Hiệu lực
            # thi hành…'") — KHÔNG phải sửa đổi cấp Điều. BỎ. (Trước đây Type-B anchor-recovery gắn nhầm vào Điều
            # gần nhất — vd [6] marker nằm trên TIÊU ĐỀ CHƯƠNG "ĐIỀU KHOẢN THI HÀNH" sau Điều 217 → false-positive
            # "Điều 217 ← 71/2025"; đã bỏ. Amendment THẬT luôn có động-từ-sửa trong def → is_amend=True.)
            continue
        if not rec["dieu"] and n in anchor:                # Type A: anchor-fallback khi def thiếu Điều
            rec["dieu"], rec["khoan"] = anchor[n][0], rec["khoan"] or anchor[n][1]
        if not (rec["dieu"] or rec["amending_sohieu"]):
            continue
        rows.append(rec)
    # Marker trong THÂN nhưng KHÔNG có def ở foot_region (vd [2] ở Điều 59) → emit đích từ anchor, NGUỒN chưa rõ.
    for n, (ad, ak) in anchor.items():
        if n not in processed and ad and n.isdigit() and int(n) <= max_foot:
            rows.append({"marker": n, "dieu": ad, "khoan": ak, "diem": None, "is_amend": True,
                         "amending_sohieu": None, "amending_vitri": None, "hieu_luc": None,
                         "loai": "", "footnote": "", "def_missing": True})
            processed.add(n)
    # B2: điền hiệu_lực còn thiếu từ registry theo số hiệu luật sửa
    if entries:
        idx = {norm_sohieu(_entry_sohieu(e)): e for e in entries if _entry_sohieu(e)}
        for r in rows:
            if not r.get("hieu_luc") and r.get("amending_sohieu"):
                hl = _entry_hieuluc_date(idx.get(r["amending_sohieu"]))
                if hl: r["hieu_luc"] = hl
    for r in rows:
        r["pending_effect"] = bool(r.get("hieu_luc") and r["hieu_luc"] > today)
        r["rel_kind"] = _footnote_rel_kind(r)   # BUG#4: HẠ ƯU TIÊN omnibus cắt-ngang / bãi-bỏ-cục-bộ
    rows.sort(key=lambda r: int(r["marker"]) if r["marker"].isdigit() else 999)
    # A2 (log1): footnote phát mỗi marker[n] thành 1 dòng → cùng (Điều,Khoản,Điểm,luật-sửa) bị đếm 2-3 lần (vd Đ73K1 ×3 =47 dòng
    # trùng/316). GOM theo khoá (dieu,khoan,diem,amending_sohieu) cho MAP cấp-Điều + đếm pending. footnote_defs giữ ĐỦ marker.
    _seen_dl, dieu_rows = set(), []
    for r in rows:
        k = (r.get("dieu"), r.get("khoan"), r.get("diem"), r.get("amending_sohieu"))
        if k in _seen_dl:
            continue
        _seen_dl.add(k); dieu_rows.append(r)
    # L3: chuỗi hợp nhất CỦA CHÍNH VBHN (cho B1 không-OUTDATED + B2 rel_type)
    mapped_sohieu = {r["amending_sohieu"] for r in rows if r.get("amending_sohieu")}
    footnote_sohieu = {norm_sohieu(m.group(1)) for m in _SOHIEU_RE.finditer(foot_region)}
    hdr_end = re.search(r"(?m)^\s*(Chương\s+[IVX]+\b|Điều\s+1\b)", body_txt)
    header = body_txt[: hdr_end.start()] if hdr_end else body_txt[:2000]
    header_sohieu = {norm_sohieu(m.group(1)) for m in _SOHIEU_RE.finditer(header)}
    body_effective = resolve_body_effective_dates(body_txt, today=today)
    body_pending = sum(1 for r in body_effective if r.get("pending_effect"))
    footnote_pending = sum(1 for r in dieu_rows if r.get("pending_effect"))   # A2: đếm trên bản ĐÃ GOM (không trùng)
    return {"today": today, "footnote_count": len(dieu_rows), "footnote_raw_count": len(rows),
            "pending_effect_count": footnote_pending + body_pending,   # tổng pending (footnote + thân Điều hiệu lực)
            "footnote_pending_effect_count": footnote_pending,
            "body_pending_effect_count": body_pending,
            "body_effective_dates": body_effective,
            "footnote_defs": {r["marker"]: r for r in rows}, "dieu_level_amendment_map": dieu_rows,
            "mapped_sohieu": sorted(mapped_sohieu), "footnote_sohieu": sorted(footnote_sohieu),
            "header_sohieu": sorted(header_sohieu)}


def _classify_ref(ref: dict, entries: list, base_goc_keys: set | None = None) -> dict:
    """Gắn cờ 1 dẫn chiếu: OK | MISSING | SOHIEU_MISMATCH | OUTDATED (report-only).
    B1: KHÔNG gắn OUTDATED nếu canonical còn hiệu lực hoặc nằm trong chuỗi hợp nhất của VBHN đang xét."""
    cited = ref["sohieu"]
    # 1) khớp theo số hiệu trước — v1.33.47: +bare-VBHN 1 chiều (văn bản dẫn '88/VBHN-VPQH' không năm ↔ entry
    # year-qualified; trước đây miss → frontier/refs-audit gắn MISSING giả cho VBHN đã có).
    by_sohieu = [e for e in entries if _sohieu_query_hits_entry(cited, norm_sohieu(_entry_sohieu(e)))
                 or _sohieu_query_hits_entry(cited, _sohieu_key_entry(e))]
    # r272: (a) chọn canonical theo ĐIỂM (trước lấy by_sohieu[0] = THỨ TỰ REGISTRY — bản .docx cách ly đứng
    # trước GDoc live thì canonical hiển thị là bản cách ly); (b) nhóm chỉ toàn bản CÁCH LY/corpus=false
    # (raw-twin đã quarantine mà bản dùng được CHƯA có) KHÔNG được xác nhận OK — đó là gap thật: frontier/
    # refs-audit đọc OK sẽ rút nó khỏi hàng cần tải (đo 31-07: [quar-only] → flag OK, canonical=bản .docx).
    by_sohieu.sort(key=_entry_score, reverse=True)
    _bs_effective = [e for e in by_sohieu if not _entry_quarantined(e)]
    # 2) khớp theo TÊN (alias) — để bắt SOHIEU_MISMATCH khi số hiệu sai
    by_name = resolve_identity(ref["name_phrase"], entries, max_hits=3) if ref["name_phrase"] else []
    flag, canonical, conf, note = "OK", None, "", ""
    if by_sohieu and not _bs_effective:
        canonical = by_sohieu[0]
        flag, conf = "MISSING", "medium"
        note = (f"số hiệu '{cited}' CHỈ khớp bản đã cách ly/corpus=false ({_entry_name(canonical)[:60]}) — "
                "corpus CHƯA có bản dùng được; nạp bản chuẩn (QT-5/fetch-route) trước khi rà")
    elif by_sohieu:
        canonical = _bs_effective[0]
        # số hiệu khớp; kiểm OUTDATED nếu có VBHN hợp nhất số này — TRỪ các ca B1:
        hl = _strip_accents(str(canonical.get("hieuluc") or canonical.get("hieu_luc") or "")).lower()
        # r271: vị từ CÒN-hiệu-lực phải NEGATION-FIRST — check cũ `"con" not in hl` coi «Không còn hiệu lực»
        # là CÒN (substring 'con' nằm trong 'khong con') ⇒ im OUTDATED cho đúng bản đã hết hiệu lực. Cùng
        # ngữ nghĩa lookup_ops (`"het" not in hl and "khong" not in hl`) + _entry_score (phạt 'het'/'thay the');
        # thêm 'chua' («Chưa có hiệu lực» không phải còn) và \bcon\b (không ăn 'cong'/'condition').
        _hl_neg = any(t in hl for t in ("het", "khong", "bai bo", "thay the", "thay bang", "chua"))
        _hl_con = (not _hl_neg) and (bool(re.search(r"\bcon\b", hl)) or "hieu luc" in hl)
        in_base_chain = bool(base_goc_keys and cited.replace("/", "-") in base_goc_keys)
        _vbhn_hits = _vbhn_for_goc(cited, entries)
        if (_vbhn_hits and not _is_vbhn_entry(canonical)
                and not _hl_con                     # B1: bản CÒN hiệu lực (khai tường minh) → không OUTDATED
                and not in_base_chain):             # B1: nằm trong chuỗi hợp nhất của chính VBHN đang xét → không OUTDATED
            # B5: NÊU RÕ số hiệu VBHN thay thế (đừng lặp lại số gốc → tránh đọc nhầm "VBHN cùng số").
            _vbhn_sh = _entry_sohieu(_vbhn_hits[0]) or ""
            flag, conf = "OUTDATED", "medium"
            note = (f"đã có VBHN hợp nhất '{_vbhn_sh}' chứa số hiệu gốc {cited} → nên rà trên VBHN '{_vbhn_sh}'"
                    if _vbhn_sh else "có VBHN hợp nhất số hiệu này trong corpus (cân nhắc dùng VBHN)")
    else:
        # số hiệu dẫn KHÔNG khớp exact. (HỢP NHẤT Codex) VBHN-COVERAGE TRƯỚC TYPO/MISSING: nếu số hiệu gốc đã được
        # 1 VBHN trong corpus bao phủ (goc-chain) → OUTDATED (rà trên VBHN), KHÔNG vội gắn TYPO/MISSING (giảm dương
        # tính giả P0-2/P2-8). Chỉ khi KHÔNG có VBHN-coverage mới bắt TYPO (near-match) rồi resolve theo tên.
        _covered_by_vbhn = _vbhn_for_goc(cited, entries)
        _typo = None if _covered_by_vbhn else _sohieu_typo_near(cited, entries, ((ref.get("loai") or "") + " " + (ref.get("name_phrase") or "")).strip())
        if _covered_by_vbhn:
            canonical = _covered_by_vbhn[0]
            flag, conf = "OUTDATED", "medium"
            note = (f"số hiệu gốc '{cited}' không là canonical trực tiếp nhưng đã được VBHN "
                    f"'{_entry_sohieu(canonical)}' bao phủ trong corpus → rà trên VBHN trước khi kết luận MISSING/TYPO")
        elif _typo and _typo[0] is not None:
            canonical = _typo[0]
            flag, conf = "DOC_TEXT_SOHIEU_TYPO", "high"
            note = (f"số hiệu dẫn '{cited}' KHÔNG có trong corpus; gần khớp '{_typo[1]}' "
                    f"(cùng số/năm, sai mã cơ quan/số thứ tự) → nhiều khả năng GÕ SAI, nên dùng '{_typo[1]}'")
        elif _typo:
            # r278/F12: ≥2 số hiệu near-match đồng tồn tại hợp pháp (TT đa-bộ / luật↔VBHN-VPQH cùng số+năm) —
            # last-wins cũ trỏ bừa 1 bản theo thứ tự manifest (conf=high + canonical + «nên dùng X»), che
            # MISSING khi cited là văn bản thứ ba VẮNG corpus. Nay: KHÔNG chọn, KHÔNG trỏ canonical, hạ conf.
            _cands = _typo[1]
            flag, conf = "DOC_TEXT_SOHIEU_TYPO", "low"
            note = (f"số hiệu dẫn '{cited}' KHÔNG có trong corpus; {len(_cands)} ứng viên gần khớp cùng số+năm: "
                    + ", ".join(f"'{s}'" for s in _cands[:3]) + ("…" if len(_cands) > 3 else "")
                    + " — KHÔNG tự chọn; cited có thể là văn bản khác VẮNG corpus (MISSING) — kiểm tay trước khi dùng")
        elif by_name:
            cano = by_name[0][0]
            cano_sh = norm_sohieu(_entry_sohieu(cano))
            if cano_sh and cano_sh != cited:
                flag, canonical, conf = "SOHIEU_MISMATCH", cano, "high"
                # B5: phân biệt "trỏ sang VBHN mới" (HÀNH VI ĐÚNG) với "dẫn sai số hiệu" (lỗi) — đừng để cờ gây hiểu nhầm.
                if _is_vbhn_entry(cano):
                    note = (f"dẫn '{cited}' → canonical là VBHN hợp nhất '{_entry_sohieu(cano)}' "
                            "(ĐÚNG: trỏ sang bản hợp nhất mới, KHÔNG phải lỗi dẫn sai)")
                else:
                    note = f"văn bản dẫn '{cited}' nhưng canonical là '{_entry_sohieu(cano)}' — kiểm lại số hiệu"
            elif cano_sh:
                canonical = cano; flag = "OK"
            else:
                # khớp tên nhưng entry THIẾU số hiệu → KHÔNG xác nhận OK (vá lỗi false-OK).
                flag, conf = "MISSING", "medium"
                note = "khớp theo tên nhưng entry THIẾU số hiệu — không xác nhận được; kiểm QT-5/web"
        else:
            flag, conf = "MISSING", "medium"
            note = "không thấy canonical theo số hiệu lẫn tên (alias) — kiểm QT-5/web"
    res = {**ref, "flag": flag, "confidence": conf, "note": note}
    if canonical is not None:
        res["canonical"] = {"sohieu": _entry_sohieu(canonical), "name": _entry_name(canonical)[:70],
                            "cat": _entry_cat(canonical), "nlm": bool(_entry_nlm(canonical))}
    return res


def _discovery_links(q: str, sites=_DISCOVERY_SITES) -> dict:
    """Trả link Google `site:` (VBHN-first: '<q> hợp nhất' → 'mới nhất' → gốc) cho 'tìm văn bản' — markdown bấm-được."""
    q = (q or "").strip()
    if not q:
        return {"query_variants": [], "links_markdown": [], "google": {}}
    variants = _query_variants(q)
    md = []
    for site in sites:
        md.append(f"- [Google site:{site} — “{variants[0]}”]({_google_site_url(variants[0], site)})")
    md.append(f"- [Google (toàn cục) — “{variants[0]}”]({_google_site_url(variants[0])})")
    return {"query_variants": variants, "links_markdown": md,
            "note": "Tìm văn bản web = Google site: (tốt hơn search nội bộ) + VBHN-first ('hợp nhất' trước).",
            "google": {site: [_google_site_url(v, site) for v in variants] for site in sites}}


def _dedup_status(q: str):
    try:
        entries = _manifest_entries()
    except Exception:
        return {"checked": False, "hits": []}, []
    hits = resolve_identity(q, entries, max_hits=6)
    rows = []
    by_sohieu = False   # khớp SỐ HIỆU + đang active ⇒ chắc chắn đã có
    by_name = False     # chỉ khớp tên/alias + active ⇒ KHẢ NĂNG đã có (cần review)
    # r269: 'active' = ĐANG trên NLM thật — dùng vị từ chuẩn _entry_on_nlm_live (source_id + không removed*),
    # KHÔNG giữ bản-sao-từ-vựng nlm_status thứ ba (bài học r253/r257: set cũ thiếu 'active' của ADR-0010
    # live→active — đo registry nền 30-07: 9 dòng 'active' + 5 dòng status rỗng có source_id bị coi không-active
    # ⇒ fetch-batch xếp action=FETCH cho văn bản ĐÃ có = mời nạp trùng).
    qkey269 = norm_sohieu(q.replace("_", "-")) if _looks_like_sohieu_query(q) else ""
    for e, score, reasons in hits[:6]:
        st = str(e.get("nlm_status") or "").strip().lower()
        is_active = _entry_on_nlm_live(e)
        # r269: reasons chứa 'alias/tukhoa:<terms>' (không phải literal 'alias') và 'name_tokens' (B2 port) —
        # membership exact cũ CÂM cả hai ⇒ likely_in_corpus=false dù resolver TÌM THẤY hit active (đo 31-07).
        _rkinds = {str(r).split(":", 1)[0].split("/", 1)[0] for r in reasons}
        if is_active and "sohieu" in _rkinds:
            by_sohieu = True
        elif is_active and _rkinds & {"name_key", "name_substr", "alias", "name_tokens"}:
            by_name = True
        rows.append({"name": _entry_name(e), "so_hieu": _entry_sohieu(e), "status": st or "(rỗng)",
                     "active": is_active, "score": score, "match": reasons})
    # r269: parity v1.33.47 — query bare-VBHN ('88-VBHN-VPQH') phải khớp entry year-qualified CÙNG số+cơ-quan
    # (resolve_identity so exact nên miss ⇒ in_corpus_active=false, fetch-batch chỉ REVIEW thay vì SKIP_DEDUP).
    if qkey269 and not by_sohieu:
        for e in entries:
            if _entry_on_nlm_live(e) and _sohieu_query_hits_entry(qkey269, _sohieu_key_entry(e)):
                by_sohieu = True
                if not any(r.get("name") == _entry_name(e) for r in rows):
                    rows.insert(0, {"name": _entry_name(e), "so_hieu": _entry_sohieu(e),
                                    "status": str(e.get("nlm_status") or "").strip().lower() or "(rỗng)",
                                    "active": True, "score": "key", "match": ["sohieu_key"]})
                break
    # Dò TÊN bằng token-overlap (bù chỗ resolve_identity hụt khi số hiệu chèn giữa tên chuẩn hóa)
    _STOP = {"luat", "bo", "nghi", "dinh", "thong", "tu", "quyet", "so", "ve", "cua", "va", "cac", "mot", "dieu"}
    qtok = {t for t in re.findall(r"[a-z0-9]+", _strip_accents(q).lower()) if len(t) >= 3 and t not in _STOP}
    if qtok and not by_sohieu:
        for e in entries:
            st = str(e.get("nlm_status") or "").strip().lower()
            if not _entry_on_nlm_live(e):   # r269: cùng vị từ active với vòng trên (hết bản sao từ vựng)
                continue
            subj = set(re.findall(r"[a-z0-9]+", _strip_accents(_entry_subject_text(e)).lower()))
            if len(qtok & subj) / len(qtok) >= 0.8:
                by_name = True
                if not any(r["name"] == _entry_name(e) for r in rows):
                    rows.insert(0, {"name": _entry_name(e), "so_hieu": _entry_sohieu(e), "status": st,
                                    "active": True, "score": "tok", "match": ["name_tokens"]})
                break
    return {"checked": True, "in_corpus_active": by_sohieu, "likely_in_corpus": by_name,
            "hits": rows}, hits


def _rq_relation_probe(entries: list[dict], e: dict) -> dict:
    """S-1 (v1.33.32 — MERGE bundle-12 hội tụ trên cùng log): cross-check cờ ứng-viên-sửa-đổi của source-map
    bằng CHÍNH engine relation-check (`_relation_audit`, PURE). source-map chủ động RỘNG để không bỏ sót; bucket
    rel của nó đã nhiều lần tạo P0 giả (124/125-2025, 68-2025, 44-2019 — LIVE relation-check trả OK/candidates=[]).
    Tiêu chí phủ định (PORT bundle-12, tinh chỉnh): KHÔNG còn tín hiệu HÀNH ĐỘNG ĐƯỢC — missing_links /
    subject_only_review / footnote_only_amendments đều rỗng. KHÔNG đòi verdict=OK (thiếu VBHN → QT5 là việc của
    bucket WEB, không giữ oan tín hiệu rel); candidates ĐÃ-linked-đủ cũng không chặn (không có gì để backfill —
    tinh chỉnh so với bundle: họ tính cả amend_n → giữ oan ca đã hợp nhất xong)."""
    base = _sohieu_key_entry(e) or _entry_sohieu(e) or ""
    subject = (_derive_subject_from_entries([e]) or _clean_subject_text(_name_tail_pretty(_entry_name(e)))
               or _entry_name(e))
    try:
        audit = _relation_audit(entries, base=base, subject=subject)
    except Exception as ex:  # noqa: BLE001 — probe phụ trợ không được giết queue
        return {"ok": False, "suppressed": False, "error": f"{type(ex).__name__}: {str(ex)[:120]}"}
    missing_n = len(audit.get("missing_links") or [])
    subject_only_n = len(audit.get("subject_only_review") or [])
    footnote_only_n = len(audit.get("footnote_only_amendments") or [])
    actionable = bool(missing_n or subject_only_n or footnote_only_n)
    return {"ok": True, "suppressed": not actionable, "verdict": audit.get("verdict"),
            "flags": sorted(audit.get("flags") or []), "subject": audit.get("subject") or subject,
            "missing_links": missing_n,
            "amendment_candidates": len(audit.get("amendment_candidates") or []),
            "subject_only_review": subject_only_n, "footnote_only_amendments": footnote_only_n,
            "note": ("relation-check PHỦ ĐỊNH — không missing_links/subject_only/footnote-thiếu; "
                     "không đưa P0/backfill" if not actionable else
                     "relation-check còn tín hiệu cần soi — giữ INFO, không tự ghi")}

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


def _dedupe_key_entry(e: dict) -> str:
    sh = _sohieu_key_entry(e)
    if not sh:
        return ""
    if _is_vbhn_entry(e):
        return "VBHN:" + sh + ":" + _vbhn_subject_key(e)
    return sh

def _is_source_sidecar(e: dict, group: list[dict], canonical: dict | None = None) -> bool:
    """File .doc/.docx/.pdf gốc nằm cạnh GDoc là sidecar hợp lệ, không phải rác."""
    name = _entry_name(e)
    if _entry_nlm(e) or not re.search(r"\.(docx?|pdf)$", name or "", re.I):
        return False
    base = _name_key(re.sub(r"\.(docx?|pdf)$", "", name, flags=re.I))
    for other in group:
        if other is e:
            continue
        if canonical is not None and other is not canonical and not _entry_nlm(other):
            continue
        if _dedupe_key_entry(other) and _dedupe_key_entry(other) == _dedupe_key_entry(e):
            return True
        obase = _name_key(re.sub(r"\.(docx?|pdf)$", "", _entry_name(other), flags=re.I))
        if base and obase and (base == obase or base in obase or obase in base):
            return True
    return False

def _sohieu_num_typo(a: str, b: str) -> bool:
    """True nếu số thứ tự a↔b chênh đúng 1 ký tự (thay 1 chữ số) hoặc đảo 2 chữ số liền kề."""
    if len(a) != len(b) or a == b:
        return False
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    if len(diff) == 1:
        return True
    return (len(diff) == 2 and diff[1] == diff[0] + 1
            and a[diff[0]] == b[diff[1]] and a[diff[1]] == b[diff[0]])

def _doctype_family(agency: str) -> str:
    """P0-2 (log rà 71 luật): HỌ loại văn bản theo mã cơ quan trong số hiệu. Dùng để CHẶN gợi ý
    DOC_TEXT_SOHIEU_TYPO VƯỢT BIÊN họ — tái dùng SỐ+NĂM giữa Luật QH ↔ NQ-TW/KL-TW (Đảng) ↔ NĐ-CP (Chính phủ)
    là HỢP PHÁP, KHÔNG phải gõ nhầm (vd 29/2013/QH13 ≠ 29/2013/NQ-TW). Chỉ flag typo trong CÙNG họ (QH14↔QH15)."""
    a = _strip_accents(agency or "").upper().replace(" ", "")
    if "TW" in a:                                   # NQ-TW/KL-TW/QD-TW/CT-TW — văn bản của Đảng
        return "TW"
    if "VPQH" in a or re.search(r"QH\d", a) or a in ("QH", "LCT-HDNN8") or "UBTVQH" in a or "-PL-" in a or a.startswith("PL-"):
        return "QH"                                 # Quốc hội / UBTVQH / VBHN-VPQH / Pháp lệnh / Lệnh CTN
    if "CP" in a:                                   # ND-CP / NQ-CP — Chính phủ
        return "CP"
    if "TTG" in a:                                  # QD-TTg — Thủ tướng
        return "TTG"
    if a.startswith("TT") or "TTLT" in a or re.search(r"-B[A-Z]{2,}", a):  # Thông tư / TTLT / QĐ-Bộ
        return "TT"
    return a or "?"                                 # mã lạ → chính nó (khác mọi họ trên → KHÔNG bắc cầu)

def resolve_body_effective_dates(text: str, today: str | None = None) -> list[dict]:
    """Parse mệnh đề hiệu lực trong THÂN văn bản, không chỉ footnote VBHN.

    Dùng để bắt luật gốc mới có Điều hiệu lực tương lai (vd "Luật này có hiệu lực
    từ ngày..." và ngoại lệ "điểm c, d khoản 1 Điều 14 có hiệu lực...").
    """
    import datetime as _dt
    today = today or _dt.date.today().isoformat()
    txt = unicodedata.normalize("NFC", text or "")
    chunks = re.split(r"(?<=[.;])\s+|\n+", txt)
    out, seen = [], set()
    for raw in chunks:
        clause = re.sub(r"\s+", " ", raw).strip()
        if "hiệu lực" not in clause.lower():
            continue
        for dm in (_HL_DATE_RE.search(clause), _HL_DATE_VN_RE.search(clause)):
            hl = _date_from_effect_match(dm)
            if not hl:
                continue
            key = (hl, clause[:160])
            if key in seen:
                continue
            seen.add(key)
            positions = []
            for pm in _POS_RE.finditer(clause):
                positions.append(" ".join(p for p in [
                    ("điểm " + pm.group(1)) if pm.group(1) else None,
                    ("khoản " + pm.group(2)) if pm.group(2) else None,
                    ("Điều " + pm.group(3)) if pm.group(3) else None,
                ] if p))
            out.append({
                "scope": clause[:240],
                "positions": positions,
                "hieu_luc": hl,
                "pending_effect": hl > today,
                "source": "body_effective_clause",
            })
    return out

# ── I11: bảng hằng chuyển từ tl.py (tl re-export giữ globals) ──
_FLAG_REASONS = {
    "RAW_NAME_NOT_NLM": "bản thô (chưa GDoc/NLM) cạnh bản canonical",
    "CORPUS_TRUE_NOT_ON_NLM": "corpus=true nhưng chưa có nguồn NLM live",
    "NLM_STATUS_MISMATCH": "nlm_status lệch trạng thái thực (registry hygiene)",
    "NLM_NOTEBOOK_ID_MISSING": "trên NLM nhưng thiếu nlm_notebook_id",
    "NLM_GHOST_SOURCE": "nguồn NLM rỗng (không tên/số hiệu)",
    "ORPHAN_CAT": "thiếu folder chủ đề hợp lệ",
    "MISSING_SOHIEU": "chưa có số hiệu chuẩn",
    "DRAFT_NOT_EFFECTIVE": "là DỰ THẢO, chưa hiệu lực",
    "OMNIBUS_NARROW_TITLE_CHECK": "tên hẹp nhưng quan hệ sửa nhiều luật (omnibus)",
    "TITLE_METADATA_MISMATCH": "tên file lệch metadata quan hệ",
    "VBHN_BARE_NUMBER": "VBHN tên trơ, thiếu năm/cơ quan",
    "VBHN_MISSING_YEAR_OR_DATE": "VBHN thiếu năm trong số hiệu/tên",
    "VBHN_NAME_MISSING_YEAR": "tên VBHN thiếu năm ban hành",
    "VBHN_NAME_MISSING_SUBJECT": "tên VBHN thiếu chủ đề",
    "VBHN_MINISTRY_SCOPE": "VBHN cấp Bộ — cần năm + xử lý riêng",
    "VBHN_MINISTRY_MISSING_YEAR": "VBHN cấp Bộ thiếu năm trong số hiệu",
    "VBHN_MINISTRY_NAME_MISSING_YEAR": "VBHN cấp Bộ thiếu năm trong tên",
    "VBHN_SOHIEU_NORMALIZED_FROM_SHORT_VPQH": "số hiệu VBHN suy từ dạng rút gọn -VPQH",
    "VBHN_YEAR_NOT_IN_METADATA": "năm VBHN không thấy trong metadata",
    "SUBJECT_NOT_EVIDENT_IN_METADATA": "metadata không thể hiện rõ chủ đề",
    "GOC_NOT_EVIDENT_IN_METADATA": "metadata không dẫn-chiếu văn bản gốc đã cho",
}
