#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tl_selftest.py — bộ selftest TÁCH khỏi tl.py để tl.py < ngưỡng mount (giảm bề mặt cắt cụt). Dùng TÊN TRẦN của
tl (norm_sohieu/extract_dieu/resolve_footnote_amendments/…) — nạp qua bind(tl_module) gọi từ tl.selftest().
KHÔNG import tl ở top (tránh circular)."""
from __future__ import annotations
import re  # noqa: F401
import json  # noqa: F401

import io as _hio
import os as _hos
import sys as _hsys


class _hush:
    """v1.31.2 (log deploy user 2026-07-03 'Vẫn lỗi'): NUỐT stdout/stderr của các test CỐ TÌNH đi nhánh lỗi —
    argparse chặn '--row-kind xyz' (in usage+error là PASS-by-design), retry-transient mock, CẮT BATCH loud,
    fallback gws-direct-media — output đó xả ra console deploy khiến người đọc tưởng selftest hỏng.
    Debug: TL_SELFTEST_VERBOSE=1 để xem lại toàn bộ."""

    def __enter__(self):
        self._v = str(_hos.environ.get("TL_SELFTEST_VERBOSE", "")).lower() in ("1", "true", "yes")
        if not self._v:
            self._so, self._se = _hsys.stdout, _hsys.stderr
            _hsys.stdout = _hsys.stderr = _hio.StringIO()
        return self

    def __exit__(self, *exc):
        if not self._v:
            _hsys.stdout, _hsys.stderr = self._so, self._se
        return False


_BOUND = False
def bind(tl_module):
    global _BOUND
    if _BOUND:
        return
    g = globals()
    for k, v in vars(tl_module).items():
        if not k.startswith("__") and k not in g:
            g[k] = v
    g["_TL_MODULE"] = tl_module      # giữ ref module để monkeypatch nội-bộ (vd H1: thay _manifest_entries)
    _BOUND = True


def run() -> int:
    cases = []
    cases.append(("norm_sohieu", norm_sohieu("113/2025/QH15") == "113-2025-QH15"
                  and norm_sohieu("95/2026/NĐ-CP") == "95-2026-ND-CP"))
    cases.append(("norm_vbhn_vpqh_short", norm_sohieu("19/VPQH") == "19-VBHN-VPQH"
                  and norm_sohieu("40-VPQH") == "40-VBHN-VPQH"))
    cases.append(("parse_ministry_vbhn_sohieu", norm_sohieu("05/VBHN-BGDĐT") == "05-VBHN-BGDDT"
                  and _parse_sohieu_from_name("2279_VBHN_BLĐTBXH_2024_Thong_tu_HopNhat.docx") == "2279_VBHN_BLĐTBXH"))
    sample = ("Điều 63. Điều kiện hưởng\nNội dung 63.\n"
              "Điều 64. Mức hưởng\nKhoản 1. abc\nKhoản 2. def\n"
              "Điều 66. Trợ cấp\nNội dung 66.")
    b64 = extract_dieu(sample, 64)
    cases.append(("extract_dieu_block", b64 is not None and "Mức hưởng" in b64 and "Trợ cấp" not in b64))
    cases.append(("extract_dieu_skip", extract_dieu(sample, 65) is None))   # số nhảy cóc
    cases.append(("extract_dieu_last", "Trợ cấp" in (extract_dieu(sample, 66) or "")))
    cases.append(("parse_raw_sohieu", _sohieu_key_entry({"name":"143_2025_QH15_681550.docx"}) == "143-2025-QH15"))
    cases.append(("skip_template_parse", _parse_sohieu_from_name("Mau_04_2025_QH15.docx") == "" and _parse_sohieu_from_name("PL_05_2025_QH15.docx") == ""))
    cases.append(("skip_template_reconcile", _reconcile_clusters([{"id":"m4","name":"Mau_04_2025_QH15.docx","cat":"UBVHXH"}, {"id":"p4","name":"PL_04_2025_QH15.docx","cat":"UBVHXH"}]) == []))
    cases.append(("title_flag_omnibus_narrow", "OMNIBUS_NARROW_TITLE_CHECK" in _title_flags({
        "name": "Luat_57-2024-QH15_Bao_hiem_y_te.docx", "sohieu": "57/2024/QH15",
        "cat": "Văn bản luật", "nlm_source_id": "src",
        "goc": "15/2017/QH14; 39/2019/QH14; 64/2020/QH14; 22/2023/QH15",
    })))
    cases.append(("find_nfc", len(_find_nfc("Phụ lục IV — cho thuê lại lao động", "Phụ lục IV")) == 1))
    cases.append(("strip_accents_dd", _strip_accents("thi đua").lower() == "thi dua"))
    _draft_text = "DỰ THẢO\nNGHỊ QUYẾT\nSố: 42/2026/NQ-CP\nĐiều 1. Phạm vi\nĐiều 2. Tổ chức thực hiện"
    _dinfo = _classify_doc_header(_draft_text, "du_thao_nq42.pdf")
    cases.append(("profile_ingest_classifies_draft_nq",
                  _dinfo["draft"] and _dinfo["kind"] == "draft" and _dinfo["loai"] == "Nghị quyết"
                  and _dinfo["sohieu_key"] == "42-2026-NQ-CP"))
    cases.append(("profile_doc_name_duthao_prefix",
                  _safe_profile_doc_name(_dinfo, "du_thao_nq42").startswith("DUTHAO_")))
    try:
        import tempfile as _tmp_ap, os as _os_ap
        _apf = _os_ap.path.join(_tmp_ap.gettempdir(), "tl_selftest_bhxh.txt")
        open(_apf, "w", encoding="utf-8").write(
            "QUỐC HỘI\nLUẬT BẢO HIỂM XÃ HỘI\nSố: 41/2024/QH15\n"
            "Điều 1. Phạm vi điều chỉnh về bảo hiểm xã hội, bảo hiểm y tế.\n"
            "Điều 2. Đối tượng áp dụng."
        )
        _ap = _vb_ingest_auto_plan(_apf)
        _ap_no_text = _vb_ingest_auto_plan("Luat_41-2024-QH15_Bao_hiem_xa_hoi.docx")
        cases.append(("vb_ingest_auto_plan_content_cat",
                      _ap["sohieu"] == "41/2024/QH15" and _ap["loai"] == "Luật"
                      and _ap["cat"] == "02" and _ap["name"] == "Luat_41-2024-QH15_Bao_hiem_xa_hoi"  # (MERGE) CHỦ ĐỀ thật, không lặp số hiệu
                      and "NO_PROBE_TEXT_FOR_AUTO_CAT" in _ap_no_text["warnings"]))
    except Exception:
        cases.append(("vb_ingest_auto_plan_content_cat", False))
    finally:
        try: _os_ap.remove(_apf)
        except Exception: pass
    # (MERGE Claude) chủ đề đặt tên lấy dòng tiêu đề THẬT (bỏ dòng số hiệu, strip loại) — chống bug Codex lặp số hiệu
    cases.append(("merge_doc_subject_and_name",
                  _doc_subject_for_name("Luật số: 113/2025/QH15\nLUẬT DÂN SỐ\nĐiều 1.", {}) == "DÂN SỐ"
                  and _vb_standard_doc_name({"loai": "Luật", "sohieu": "113/2025/QH15", "title": "Dân số"}, "x") == "Luat_113-2025-QH15_Dan_so"))
    # (MERGE) ca 1 DÒNG gộp số hiệu NHÚNG (dash & slash) → chủ đề sạch, không lọt số hiệu vào tên
    cases.append(("merge_subject_strips_inline_sohieu",
                  _doc_subject_for_name("Luật số 113-2025-QH15 Về Dân số\nĐiều 1.", {}) == "Dân số"
                  and _doc_subject_for_name("Luật số 113/2025/QH15 về Dân số\nĐiều 1.", {}) == "Dân số"
                  and _doc_subject_for_name("113/2025/QH15\nLUẬT ĐẤT ĐAI\nĐiều 1.", {}) == "ĐẤT ĐAI"))
    # v1.26 (yêu cầu user): corpus-fix orchestrator + shared-source-fix + source-rename
    _cfx = [
        {"drive_id": "d1", "nlm_source_id": "S", "nlm_status": "pushed", "name": "Luat_a", "so_hieu": "1/2025/QH15", "corpus": "true"},
        {"drive_id": "d2", "nlm_source_id": "S", "nlm_status": "pushed", "name": "Luat_b", "so_hieu": "2/2025/QH15", "corpus": "true"},
        {"drive_id": "inf", "name": "tl_secrets.enc", "corpus": "true", "mimeType": "application/octet-stream"},
        # MERGE Codex v1.33.11: nguồn thô .html đang trên NLM → plan phải có bước raw_on_nlm (human_confirm).
        {"drive_id": "rawhtml", "name": "luat-dau-thau-so-22-2023-qh15-259737-d1.html", "mime": "text/html",
         "corpus": "true", "nlm_source_id": "rawsrc", "nlm_status": "pushed"},
    ]
    _cfp = _corpus_fix_plan(_cfx)
    cases.append(("corpus_fix_plan_ordered_tiered",
                  [s["order"] for s in _cfp["steps"]] == sorted(s["order"] for s in _cfp["steps"])
                  and any(s["id"] == "shared_source_id" and s["tier"] == "human_confirm" for s in _cfp["steps"])
                  and any(s["id"] == "infra_in_corpus" and s["tier"] == "safe_auto" and s["reversible"] for s in _cfp["steps"])
                  and any(s["id"] == "raw_on_nlm" and s["tier"] == "human_confirm" for s in _cfp["steps"])))
    _ssf = _shared_source_fix_plan([
        {"drive_id": "hi", "nlm_source_id": "S", "name": "Luat_x", "so_hieu": "1/2025/QH15", "nlm_status": "pushed"},
        {"drive_id": "lo", "nlm_source_id": "S", "name": "lo", "nlm_status": "pushed"},
    ])
    cases.append(("shared_source_fix_keep_clear",
                  len(_ssf) == 1 and _ssf[0]["source_id"] == "S" and len(_ssf[0]["clear"]) == 1
                  and ({_ssf[0]["keep"]["drive_id"]} | {c["drive_id"] for c in _ssf[0]["clear"]}) == {"hi", "lo"}))
    _srf = [{"drive_id": "D", "name": "Luat_113-2025-QH15_Dan_so", "so_hieu": "113/2025/QH15", "cat": "08"}]
    _sr = _source_rename_plan(_srf, "113/2025/QH15")
    _sr2 = _source_rename_plan(_srf, "113/2025/QH15", new_name="Luat_113-2025-QH15_Dan_so_v2")
    cases.append(("source_rename_plan",
                  _sr["ok"] and _sr["drive_id"] == "D" and _sr["new_name"] == "Luat_113-2025-QH15_Dan_so"
                  and _sr["already_standard"] and _sr2["new_name"] == "Luat_113-2025-QH15_Dan_so_v2"
                  and _source_rename_plan(_srf, "999/2099/QH99").get("error") == "NOT_FOUND"))
    # v1.26.1 (MERGE port Codex source CRUD): source-delete + source-update-corpus, GUARD shared_source_id
    _shdel = [{"drive_id": "d", "nlm_source_id": "S", "name": "x", "so_hieu": "1/2025/QH15"},
              {"drive_id": "d2", "nlm_source_id": "S", "name": "y", "so_hieu": "2/2025/QH15"}]
    _sd = _source_delete_plan(_shdel, "1/2025/QH15")
    _sd2 = _source_delete_plan([{"drive_id": "u", "nlm_source_id": "U", "name": "z", "so_hieu": "3/2025/QH15"}], "3/2025/QH15")
    cases.append(("source_delete_ABORTS_on_shared",
                  _sd["blocked_shared"] is True and _sd["error"] == "SHARED_SOURCE_MUST_FIX_FIRST" and _sd["reversible"] is False
                  and _sd2.get("blocked_shared") is not True and "nlm source delete U" in _sd2["actions"][0]
                  and _source_delete_plan(_shdel, "999/2099/QH99").get("error") == "NOT_FOUND"))
    _suc_f = _source_update_corpus_plan([{"drive_id": "u", "nlm_source_id": "U", "name": "z", "so_hieu": "3/2025/QH15"}], "3/2025/QH15", False)
    _suc_sh = _source_update_corpus_plan(_shdel, "1/2025/QH15", False)
    _suc_t = _source_update_corpus_plan([{"drive_id": "u", "name": "z", "so_hieu": "3/2025/QH15"}], "3/2025/QH15", True)
    cases.append(("source_update_corpus_guard_and_ingest",
                  _suc_f["set_corpus"] is False and _suc_f["will_remove_nlm"] is True and _suc_f.get("blocked_shared") is not True
                  and _suc_sh.get("blocked_shared") is True and _suc_sh["will_remove_nlm"] is False
                  and _suc_t["set_corpus"] is True and _suc_t["needs_ingest"] is True))
    # S9/S10/S11 (log 2026-07-01 — chống chốt VBHN LỖI THỜI, ca BLHS 01/VBHN 2017 vs 135/VBHN 2025)
    import datetime as _dt9
    _yr9 = _dt9.date.today().year
    _qh = _qt5_queries("Bộ luật Hình sự", "100/2015/QH13", "")
    cases.append(("qt5_two_pass_latest",
                  any("mới nhất" in q for q in _qh) and any("congbao" in q for q in _qh)
                  and any(f"VBHN VPQH {_yr9}" in q for q in _qh)
                  and ("mới nhất" in _qh[0] or "congbao" in _qh[0] or str(_yr9) in _qh[0])))   # high-velocity → lượt-2 lên đầu
    cases.append(("high_amendment_velocity_detect",
                  _is_high_amendment_subject("Bộ luật Hình sự") and _is_high_amendment_subject("Bo_luat_hinh_su")
                  and _is_high_amendment_subject("Phí và lệ phí") and not _is_high_amendment_subject("Thi đua khen thưởng")))
    _smlv = _source_map_one("100/2015/QH13", [
        {"id": "blhs", "name": "Luat_100-2015-QH13_Bo_luat_hinh_su", "so_hieu": "100-2015-QH13", "cat": "16", "corpus": "true"},
        {"id": "vbhnlv", "name": "VBHN_11-VBHN-VPQH_2025_Bo_luat_hinh_su_goc_100-2015-QH13", "so_hieu": "11-VBHN-VPQH", "loai": "VBHN", "goc": "100-2015-QH13;59-2024-QH15", "cat": "16", "corpus": "true", "nlm_source_id": "n"}])
    cases.append(("source_map_vbhn_unverified_latest_flag",
                  any("VBHN_CANDIDATE_UNVERIFIED_LATEST" in w for w in _smlv["warnings"])
                  and any("VBHN_HIGH_AMENDMENT_VELOCITY" in w for w in _smlv["warnings"])
                  and any("mới nhất" in q for q in _qt5_search_hints("Bộ luật Hình sự", []))))
    # Pha sau: consolidation-cleanup — 'cả VBHN + gốc/sửa đổi rời' → GIỮ VBHN, thành phần corpus=false (reversible)
    _cc = _consolidation_cleanup_plan([
        {"drive_id": "vbhn", "name": "VBHN_11-VBHN-VPQH_2025_Bo_luat_hinh_su_goc_100-2015-QH13",
         "so_hieu": "11-VBHN-VPQH", "loai": "VBHN", "goc": "100-2015-QH13;59-2024-QH15", "corpus": "true", "nlm_source_id": "nb"},
        {"drive_id": "goc", "name": "Luat_100-2015-QH13_Bo_luat_hinh_su", "so_hieu": "100-2015-QH13", "corpus": "true"},        # thành phần rời, KHÔNG trên NLM → ready
        {"drive_id": "sua", "name": "Luat_59-2024-QH15_sua_BLHS", "so_hieu": "59-2024-QH15", "corpus": "true", "nlm_source_id": "ns"},  # thành phần còn NLM → review
        {"drive_id": "khac", "name": "Luat_999-2099-QH99_Khac", "so_hieu": "999-2099-QH99", "corpus": "true"},                 # không bị phủ → bỏ qua
    ])
    _cc_ready_ids = {r["drive_id"] for r in _cc["ready"]}
    _cc_review_ids = {r["drive_id"] for r in _cc["review_on_nlm"]}
    cases.append(("consolidation_cleanup_keeps_vbhn_flags_components",
                  _cc_ready_ids == {"goc"} and _cc_review_ids == {"sua"} and _cc["total_ready"] == 1
                  and "vbhn" not in _cc_ready_ids and "vbhn" not in _cc_review_ids and "khac" not in (_cc_ready_ids | _cc_review_ids)))
    # VBHN chưa on NLM (chưa verify) → KHÔNG đề xuất set component corpus=false
    _cc2 = _consolidation_cleanup_plan([
        {"drive_id": "vbhn2", "name": "VBHN_x_goc_100-2015-QH13", "so_hieu": "12-VBHN-VPQH", "loai": "VBHN",
         "goc": "100-2015-QH13", "corpus": "true"},   # KHÔNG nlm_source_id → chưa verify
        {"drive_id": "goc2", "name": "Luat_100-2015-QH13_x", "so_hieu": "100-2015-QH13", "corpus": "true"}])
    cases.append(("consolidation_cleanup_requires_verified_vbhn", _cc2["total_ready"] == 0 and not _cc2["review_on_nlm"]))
    # corpus-audit (A+B): engine ĐỀ XUẤT dùng chung — đọc header → đề xuất sửa số hiệu/tên-trích-yếu/năm (propose-only)
    _ca_sohieu = _corpus_audit_row(
        {"drive_id": "D", "name": "Luat_113-2025-QH15_Dan_so", "so_hieu": "113/2025/QH15", "cat": "08", "corpus": "true"},
        "QUỐC HỘI\nLuật số: 112/2025/QH15\nLUẬT DÂN SỐ\nCăn cứ Hiến pháp;\nĐiều 1. Phạm vi\n")
    _ca_s = [p for p in _ca_sohieu["proposals"] if p["type"] == "SOHIEU_MISMATCH"]
    cases.append(("corpus_audit_sohieu_mismatch",
                  len(_ca_s) == 1 and _ca_s[0]["suggested"] == "112-2025-QH15"
                  and "source-rename" in _ca_s[0]["fix_command"] and "--sohieu" in _ca_s[0]["fix_command"]))
    _ca_name = _corpus_audit_row(
        {"drive_id": "D2", "name": "44_2024_QH15_Duoc_583839", "so_hieu": "44/2024/QH15", "cat": "29", "corpus": "true"},
        "QUỐC HỘI\nLuật số: 44/2024/QH15\nLUẬT SỬA ĐỔI, BỔ SUNG MỘT SỐ ĐIỀU CỦA LUẬT DƯỢC\nCăn cứ;\nĐiều 1.\n")
    _ca_n = [p for p in _ca_name["proposals"] if p["type"] == "NAME_TRICH_YEU"]
    cases.append(("corpus_audit_name_trich_yeu",
                  len(_ca_n) == 1 and _ca_n[0]["suggested"].startswith("Luat")
                  and "--name" in _ca_n[0]["fix_command"] and not any(p["type"] == "SOHIEU_MISMATCH" for p in _ca_name["proposals"])))
    _ca_yr = _corpus_audit_row(
        {"drive_id": "D3", "name": "VBHN_25-VBHN-VPQH_Ke_toan", "so_hieu": "25/VBHN-VPQH", "loai": "VBHN", "cat": "44", "corpus": "true"},
        "VĂN BẢN HỢP NHẤT\nLuật Kế toán\nĐiều 1.\n")
    _ca_y = [p for p in _ca_yr["proposals"] if p["type"] == "MISSING_YEAR"]
    cases.append(("corpus_audit_missing_year_vbhn",
                  len(_ca_y) == 1 and "vbhn-year-fix" in _ca_y[0]["fix_command"]))
    _ca_clean = _corpus_audit_row(
        {"drive_id": "D4", "name": "Luat_100-2015-QH13_Bo_luat_hinh_su", "so_hieu": "100/2015/QH13", "cat": "16", "corpus": "true"},
        "QUỐC HỘI\nBộ luật số: 100/2015/QH13\nBỘ LUẬT HÌNH SỰ\nCăn cứ Hiến pháp;\nĐiều 1.\n")
    _hi = {"SOHIEU_MISMATCH", "NAME_TRICH_YEU", "MISSING_YEAR", "LOAI_MISMATCH"}
    cases.append(("corpus_audit_clean_no_high_severity",
                  not any(p["type"] in _hi for p in _ca_clean["proposals"])
                  and _ca_clean["proposals"] == sorted(_ca_clean["proposals"], key=lambda p: p["severity"])))
    cases.append(("corpus_audit_name_nonstandard_detect",
                  _name_looks_nonstandard("44_2024_QH15_Duoc_583839") and _name_looks_nonstandard("luat-dau-thau.html")
                  and not _name_looks_nonstandard("Luat_100-2015-QH13_Bo_luat_hinh_su")))
    # REGRESSION AN TOÀN (ca thật lộ khi chạy manifest): VBHN tên ĐÃ CHUẨN + header nêu 'VĂN PHÒNG QUỐC HỘI' đầu trang
    # → TUYỆT ĐỐI KHÔNG đề xuất đổi tên (tránh rớt năm + nhặt boilerplate 'Van_phong_quoc_hoi' thay 'Ke_toan').
    _ca_danger = _corpus_audit_row(
        {"drive_id": "V", "name": "VBHN_25-2025-VBHN-VPQH_Luat_Ke_toan", "so_hieu": "25-2025-VBHN-VPQH", "loai": "VBHN", "cat": "44", "corpus": "true"},
        "VĂN PHÒNG QUỐC HỘI\nVĂN BẢN HỢP NHẤT\nLUẬT KẾ TOÁN\nĐiều 1.\n")
    cases.append(("corpus_audit_no_rename_standard_name",
                  not any(p["type"] == "NAME_TRICH_YEU" for p in _ca_danger["proposals"])))
    cases.append(("corpus_audit_subject_boilerplate_guard",
                  _subject_is_boilerplate("VĂN PHÒNG QUỐC HỘI") and _subject_is_boilerplate("")
                  and not _subject_is_boilerplate("Kế toán")))
    # REGRESSION (review an toàn #2): VBHN số hiệu THIẾU NĂM + tên hỏng cấu trúc → CHỈ MISSING_YEAR, KHÔNG NAME_TRICH_YEU
    # (dựng tên từ sohieu year-less sẽ RỚT NĂM — vi phạm bất biến; vbhn-year-fix --with-name xử trước, đổi cả tên).
    _ca_noyr = _corpus_audit_row(
        {"drive_id": "Y", "name": "VBHN_25_raw_Ke_toan.docx", "so_hieu": "25/VBHN-VPQH", "loai": "VBHN", "cat": "44", "corpus": "true"},
        "VĂN BẢN HỢP NHẤT\nLUẬT KẾ TOÁN\nĐiều 1.\n")
    _ca_types = {p["type"] for p in _ca_noyr["proposals"]}
    cases.append(("corpus_audit_vbhn_noyear_defers_name",
                  "MISSING_YEAR" in _ca_types and "NAME_TRICH_YEU" not in _ca_types))
    # S12/S13 (log PHA 5 ingest-missing): skip sohieu='' + dedup nguồn LIVE (chống trùng) + checkpoint backward-compat
    _im_targets = [{"drive_id": "1aRKrGw6PEkRZvi1MIbb7CfB", "so_hieu": "80/2020/ND-CP", "name": "x"},
                   {"drive_id": "2bSLmHx7QFlSAwj2NJcc8DgC", "so_hieu": "", "name": "80-nd-cp.signed.pdf"},   # sohieu rỗng = rác
                   {"drive_id": "3cTMnIy8RGmTBxk3OKdd9EhD", "so_hieu": "106/2025/QH15", "name": "y"}]
    _im_valid, _im_ns = _ingest_missing_partition(_im_targets)
    cases.append(("ingest_missing_partition_skips_no_sohieu",
                  len(_im_valid) == 2 and len(_im_ns) == 1 and _im_ns[0]["drive_id"] == "2bSLmHx7QFlSAwj2NJcc8DgC"))
    # nguồn LIVE trỏ drive_id thứ 1 (qua URL /d/<id>) → phải LINK, KHÔNG source_add lại
    _im_live = [{"id": "srcLIVE", "url": "https://docs.google.com/document/d/1aRKrGw6PEkRZvi1MIbb7CfB/edit"}]
    _im_add, _im_link, _im_unres = _ingest_missing_dedup_live(_im_targets, _im_live)
    cases.append(("ingest_missing_dedup_live_links_existing",
                  len(_im_link) == 1 and _im_link[0][0]["drive_id"] == "1aRKrGw6PEkRZvi1MIbb7CfB" and _im_link[0][1] == "srcLIVE"
                  and len(_im_add) == 2 and all(t["drive_id"] != "1aRKrGw6PEkRZvi1MIbb7CfB" for t in _im_add)))
    # (review#1) FALLBACK số hiệu khi URL nguồn LIVE KHÔNG parse được fileId (vd /folders/) → vẫn LINK theo sohieu DUY NHẤT
    _im_live_sohieu = [{"id": "srcSH", "url": "https://drive.google.com/drive/folders/xxx", "sohieu": "106/2025/QH15"}]
    _a2, _l2, _u2 = _ingest_missing_dedup_live(_im_targets, _im_live_sohieu)
    cases.append(("ingest_missing_dedup_sohieu_fallback",
                  any(sid == "srcSH" and ent["drive_id"] == "3cTMnIy8RGmTBxk3OKdd9EhD" for ent, sid in _l2)
                  and all(t["drive_id"] != "3cTMnIy8RGmTBxk3OKdd9EhD" for t in _a2)))

    class _FakeCkpt:
        def __init__(self, c): self._c = c
        def exists(self): return self._c is not None
        def read_text(self, encoding="utf-8"): return self._c
    import json as _jm
    # (review#1) format list cũ / None → BỎ HẲN (entry không source_id vô giá trị + tránh skip-mù không bao giờ nạp lại)
    _ck_old = _ingest_ckpt_load(_FakeCkpt(_jm.dumps({"done": ["d1", "d2"]})))
    _ck_mix = _ingest_ckpt_load(_FakeCkpt(_jm.dumps({"done": {"d1": "s1", "d2": None, "d3": ""}})))
    cases.append(("ingest_ckpt_load_drops_null_sourceid",
                  _ck_old == {} and _ck_mix == {"d1": "s1"} and _ingest_ckpt_load(_FakeCkpt(None)) == {}))
    # v1.29.1 (log LIVE 2026-07-02) — ckpt FULL 4 khóa: backward-compat file cũ chỉ có done; format mới round-trip.
    _cf_old = _ingest_ckpt_load_full(_FakeCkpt(_jm.dumps({"done": {"d1": "s1", "d2": None}})))
    _cf_new = _ingest_ckpt_load_full(_FakeCkpt(_jm.dumps({"done": {"d1": "s1"}, "pending": {"d9": "Tit"},
                                                          "linked": {"d1": "s1"}, "fails": {"dF": 3}})))
    cases.append(("r2_ckpt_full_compat",
                  _cf_old["done"] == {"d1": "s1"} and _cf_old["pending"] == {} and _cf_old["linked"] == {} and _cf_old["fails"] == {}
                  and _cf_new["pending"] == {"d9": "Tit"} and _cf_new["linked"] == {"d1": "s1"} and _cf_new["fails"] == {"dF": 3}
                  and _ingest_ckpt_load_full(_FakeCkpt(None))["done"] == {}))
    # v1.29.1 — dedup-live TẦNG 3 exact-title: sohieu bất-đối-xứng năm (registry '67-2025-VBHN-VPQH' vs title parse
    # '67-VBHN-VPQH') làm tầng 2 MISS → title (do tool đặt = _entry_name[:120]) khớp DUY NHẤT → LINK không add lại.
    _t3_e = {"drive_id": "dX", "name": "VBHN_67-VBHN-VPQH_2025_Luat_Doanh_nghiep_HopNhat", "so_hieu": "67-2025-VBHN-VPQH"}
    _t3_live = [{"id": "s9", "title": "VBHN_67-VBHN-VPQH_2025_Luat_Doanh_nghiep_HopNhat"}]
    _t3_ta, _t3_al, _t3_u = _ingest_missing_dedup_live([_t3_e], _t3_live)
    _t3_dup_ta, _t3_dup_al, _ = _ingest_missing_dedup_live(
        [_t3_e], [{"id": "s9", "title": "Cung mot title"}, {"id": "s8", "title": "Cung mot title"}])
    cases.append(("r2_dedup_live_title_tier",
                  _t3_al == [(_t3_e, "s9")] and _t3_ta == []                    # title duy nhất → LINK
                  and _t3_dup_al == [] and _t3_dup_ta == [_t3_e]))              # title KHÔNG khớp/không duy nhất → add
    # v1.29.1 — LOAI_MISMATCH guard (2.5a): header cụt làm checks['loai']=False nhưng loai chuẩn hoá BẰNG NHAU → KHÔNG fire.
    cases.append(("r2_loai_same_norm_no_selfmismatch",
                  _normalize_loai("Nghị định") == _normalize_loai("nghi dinh") != ""))

    # ═══ v1.29.3 (AUDIT #7) — ĐỢT TEST CHECKPOINT-RECOVERY: mock GAS + nhánh LỖI của verified-write/journal/resume/
    # undo/gate + primitive mới (#3 dedup-gate, #4 overlay, #5 raw-dup detector). Journal ghi file THẬT ~/.tl_journal
    # (tiền lệ smoke v1.28.3) → cleanup sau; cache-bust test cô lập qua TL_PROFILE tạm. ═══
    import types as _ty3, os as _os3

    class _FakeG:
        def __init__(self, post_r=None, get_r=None, post_exc=None, get_exc=None):
            self.posts, self.gets = [], []
            self._pr, self._gr, self._pe, self._ge = post_r, get_r, post_exc, get_exc
        def post(self, action, **kw):
            self.posts.append((action, kw))
            if self._pe:
                raise self._pe
            return dict(self._pr or {"ok": True, "patched": len(kw.get("items") or []), "missed": 0, "miss": []})
        def get(self, action, **kw):
            self.gets.append((action, kw))
            if self._ge:
                raise self._ge
            return dict(self._gr or {"ok": True, "updated": True})

    _r3_env = {k: _os3.environ.get(k) for k in ("TL_PROFILE", "TL_REGISTRY_DOC_ID")}
    _r3_runs = []
    try:
        _os3.environ["TL_PROFILE"] = "selftest-r3"          # cô lập cache-dir + precheck theo profile GIẢ
        _os3.environ.pop("TL_REGISTRY_DOC_ID", None)
        # (1) verified-write: OK / idempotent / miss THẬT / cột sai (chặn TRƯỚC post) / post raise
        _g = _FakeG(post_r={"ok": True, "patched": 2, "missed": 0, "miss": []})
        cases.append(("r3_verified_write_ok", _verified_reg_write(_g, [{"drive_id": "d1", "corpus": "false"},
                                                                       {"drive_id": "d2", "corpus": "false"}], "corpus").get("verified") is True))
        _g = _FakeG(post_r={"ok": True, "patched": 0, "missed": 0, "miss": []})
        cases.append(("r3_verified_write_idempotent",
                      _verified_reg_write(_g, [{"drive_id": "d1", "corpus": "false"}], "corpus").get("verified") is True))
        _g = _FakeG(post_r={"ok": True, "patched": 1, "missed": 1, "miss": ["dX"]})
        _vm = _verified_reg_write(_g, [{"drive_id": "d1", "corpus": "false"}, {"drive_id": "dX", "corpus": "false"}], "corpus")
        cases.append(("r3_verified_write_miss", _vm.get("verified") is False and "dX" in (_vm.get("missed_ids") or [])))
        _g = _FakeG()
        _vb = _verified_reg_write(_g, [{"drive_id": "d1", "so_hieu": "x"}], "so_hieu")
        cases.append(("r3_verified_write_badcols_blocks_before_post",
                      _vb.get("verified") is False and _vb.get("error") == "REG_COLS_NOT_IN_SCHEMA" and _g.posts == []))
        _g = _FakeG(post_exc=RuntimeError("boom"))
        cases.append(("r3_verified_write_raise",
                      _verified_reg_write(_g, [{"drive_id": "d1", "corpus": "false"}], "corpus").get("verified") is False))
        _g = _FakeG(post_r={"ok": True, "patched": 0, "missed": ["dY"], "miss": ["dY"]})   # webapp variant: missed=LIST
        _vl = _verified_reg_write(_g, [{"drive_id": "dY", "corpus": "false"}], "corpus")
        cases.append(("r3_verified_write_missed_list_guard", _vl.get("verified") is False))
        # (2) journaled write: intent{set,before}+commit per-row + partial-fail → inflight + BUST cache marker (#1 v1.29.2)
        _cdir = _profile_cache_dir(); _cdir.mkdir(parents=True, exist_ok=True)
        _marker = _cache_file("manifest.json"); _marker.write_text("{}", encoding="utf-8")
        _rid1 = _apply_journal_start("selftest-r3-write", {})
        _r3_runs.append(_rid1)
        _g = _FakeG(post_r={"ok": True, "patched": 1, "missed": 1, "miss": ["d2"]})
        _journaled_reg_write(_rid1, _g, [{"drive_id": "d1", "corpus": "false"}, {"drive_id": "d2", "corpus": "false"}],
                             "corpus", before_by_key={"d1": {"corpus": "true"}, "d2": {"corpus": "true"}})
        _recs1 = _journal_read(_rid1)
        _ints = [r for r in _recs1 if r.get("t") == "intent"]
        _cmts = {r.get("key"): r.get("ok") for r in _recs1 if r.get("t") == "commit"}
        _st1 = _journal_resume_state(_recs1)
        cases.append(("r3_journaled_write_records",
                      len(_ints) == 2 and _ints[0].get("set") == {"corpus": "false"} and _ints[0].get("before") == {"corpus": "true"}
                      and _cmts.get("d1") is True and _cmts.get("d2") is False))
        cases.append(("r3_journaled_write_partial_inflight", "d2" in [iv.get("key") for iv in _st1.get("inflight") or []]))
        cases.append(("r3_bust_cache_after_write", not _marker.exists()))
        # (3) journaled upsert: idempotent updated=False = verified; bust cache
        _marker.write_text("{}", encoding="utf-8")
        _rid2 = _apply_journal_start("selftest-r3-upsert", {})
        _r3_runs.append(_rid2)
        _g = _FakeG(get_r={"ok": True, "updated": False})
        _vu = _journaled_reg_upsert(_rid2, _g, {"drive_id": "d9", "sohieu": "1-2025-ND-CP"}, before={"sohieu": "1-ND-CP"})
        cases.append(("r3_journaled_upsert_idempotent_ok", _vu.get("verified") is True and _vu.get("changed") is False
                      and not _marker.exists()))
        # (4) resume BỎ QUA op non-reg (composite ingest-local 2.4) + undo CHỈ op có before
        _recs_mix = [{"t": "run_start", "run_id": "rX", "cmd": "ingest-local"},
                     {"t": "intent", "op": "nlm_source_add", "key": "g1", "key_field": "drive_id", "set": {"notebook": "nb"}},
                     {"t": "intent", "op": "reg_bulk", "key": "g2", "key_field": "drive_id", "cols": "corpus",
                      "set": {"corpus": "false"}, "before": {"corpus": "true"}},
                     {"t": "commit", "op": "reg_bulk", "key": "g2", "ok": True}]
        _rops = _journal_resume_ops(_recs_mix)
        cases.append(("r3_resume_ignores_nonreg_ops", all(op.get("op") in ("reg_bulk", "reg_upsert") for op in _rops)
                      and not any(op.get("key") == "g1" for op in _rops)))
        _uops = _journal_undo_ops(_recs_mix)
        cases.append(("r3_undo_only_with_before", any(op.get("key") == "g2" for op in _uops)
                      and not any(op.get("key") == "g1" for op in _uops)))
        # (5) _apply_gate: profile GIẢ + registryDocId RỖNG = BLOCKER (chống clobber) → chặn; --force-unsafe vượt
        _a_blk = _ty3.SimpleNamespace(force_unsafe=False)
        _a_frc = _ty3.SimpleNamespace(force_unsafe=True)
        _gate_blocked, _ = _apply_gate(_a_blk, write_cols="corpus", stream=False)
        _gate_forced, _ = _apply_gate(_a_frc, write_cols="corpus", stream=False)
        cases.append(("r3_gate_blocks_empty_profile_registry", _gate_blocked is False and _gate_forced is True))
        # (6) #3 dedup-gate: dup theo drive_id / clear / skipped / list_failed (ok:False + raise)
        class _FakeNC:
            def __init__(self, r=None, exc=None): self._r, self._exc = r, exc
            def source_list(self, nb, skip_freshness=True, drive=True):
                if self._exc:
                    raise self._exc
                return self._r
        _DG = "1FakeDriveId0123456789abcd"           # ≥20 ký tự — _nlm_source_drive_id đòi id Drive thật độ dài này
        _nc_dup = _FakeNC({"ok": True, "sources": [{"id": "s1", "title": "T", "drive_id": _DG}]})
        _v1, _d1 = _nlm_dedup_gate(_nc_dup, "nb", [{"drive_id": _DG, "name": "X"}])
        _v2, _ = _nlm_dedup_gate(_nc_dup, "nb", [{"drive_id": "1OtherDriveId9876543210zyxw", "name": "Khac hoan toan"}])
        _v3, _ = _nlm_dedup_gate(_nc_dup, "nb", [{"drive_id": _DG, "name": "X"}], skip=True)
        _v4, _ = _nlm_dedup_gate(_FakeNC({"ok": False}), "nb", [{"drive_id": _DG, "name": "X"}])
        _v5, _ = _nlm_dedup_gate(_FakeNC(exc=RuntimeError("net")), "nb", [{"drive_id": _DG, "name": "X"}])
        cases.append(("r3_nlm_dedup_gate", _v1 == "dup" and _d1 and _d1[0][1] == "s1" and _v2 == "clear"
                      and _v3 == "skipped" and _v4 == "list_failed" and _v5 == "list_failed"))
        # (7) #4 overlay gws-live: CHỈ thay trường mutable, GIỮ enrichment; entry không khớp giữ nguyên
        _ov = _entries_with_live_fields(
            [{"id": "dA", "so_hieu": "1-2025-ND-CP", "issue_year": 2025, "corpus": "true", "nlm_status": ""},
             {"id": "dB", "so_hieu": "2-2025-ND-CP", "corpus": "true"}],
            [{"drive_id": "dA", "corpus": "false", "nlm_status": "pushed", "sohieu": "RAW-KHAC"}])
        cases.append(("r3_live_overlay_mutable_only",
                      _ov[0]["corpus"] == "false" and _ov[0]["nlm_status"] == "pushed"
                      and _ov[0]["so_hieu"] == "1-2025-ND-CP" and _ov[0]["issue_year"] == 2025
                      and _ov[1]["corpus"] == "true"))
        # (8) #5 detector raw_dup_of_standard: ca THẬT ND274_2025 + negative (2 chuẩn cùng số-năm / raw parse được / chuẩn tắt corpus)
        _std = {"drive_id": "dS", "so_hieu": "274-2025-ND-CP", "name": "ND_274-2025-ND-CP_Cham_dong_BHXH", "corpus": "true"}
        _raw = {"drive_id": "dR", "name": "ND274_2025_cham dong-tron dong BH.pdf", "corpus": "true"}
        _rr1 = _raw_dup_of_standard_rows([_std, _raw])
        _rr2 = _raw_dup_of_standard_rows([_std, dict(_std, drive_id="dS2", name="ND_274-2025-ND-CP_ban2"), _raw])
        _rr3 = _raw_dup_of_standard_rows([dict(_std, corpus="false"), _raw])
        cases.append(("r3_raw_dup_detector",
                      len(_rr1) == 1 and _rr1[0]["drive_id"] == "dR" and _rr1[0]["standard"]["drive_id"] == "dS"
                      and _rr2 == [] and _rr3 == []))
        # zero-padded num (ca PL_06 log LIVE): std key '06-2003-PL-…' phải khớp raw 'PL 6 2003…' (num chuẩn hoá int)
        _rr4 = _raw_dup_of_standard_rows([
            {"drive_id": "dS4", "so_hieu": "06-2003-PL-UBTVQH11", "name": "PL_06-2003-PL-UBTVQH11_Dan_so", "corpus": "true"},
            {"drive_id": "dR4", "name": "PL 6_2003 phap lenh dan so ban scan.pdf", "corpus": "true"}])
        cases.append(("r3_raw_dup_zero_padded", len(_rr4) == 1 and _rr4[0]["drive_id"] == "dR4"))
        # regression smoke-LIVE: tên CHUẨN loại hiếm (CD=Công điện, family ngoài list loose-RE, KHÔNG space/đuôi-file)
        # KHÔNG được ghép nhầm bản chuẩn khác cùng số-năm (ca thật CD_32-2026 vs TT_32-2026).
        _rr5 = _raw_dup_of_standard_rows([
            {"drive_id": "dS5", "so_hieu": "32-2026-TT-BGDDT", "name": "TT_32-2026-TT-BGDDT_Chuc_danh", "corpus": "true"},
            {"drive_id": "dR5", "name": "CD_32-2026-CD-TTg_To_chuc_tong_ra_soat_VBQPPL", "corpus": "true"}])
        cases.append(("r3_raw_dup_standard_name_not_candidate", _rr5 == []))
    finally:
        for _k, _vv in _r3_env.items():
            if _vv is None:
                _os3.environ.pop(_k, None)
            else:
                _os3.environ[_k] = _vv
        for _r in _r3_runs:
            try:
                (_journal_dir() / f"{_r}.jsonl").unlink()
            except Exception:
                pass
        try:
            import shutil as _sh3
            _sh3.rmtree(Path(_os3.path.expanduser("~")) / ".tra_luat_cache" / "selftest-r3", ignore_errors=True)
        except Exception:
            pass
    # (9) #6 — _persist_profile_config CÓ JOURNAL: intent{before block cũ} + commit{readback_match} (op config_write, non-reg)
    import tempfile as _tf3
    _cfg_tmp = Path(_tf3.gettempdir()) / "tl_selftest_r3_config.json"
    _jd_before = set(p.name for p in _journal_dir().glob("*.jsonl")) if _journal_dir().exists() else set()
    try:
        _cfg_tmp.write_text(_jm.dumps({"profiles": {"pX": {"rootFolderId": "OLD"}}}), encoding="utf-8")
        _written = _persist_profile_config(str(_cfg_tmp), "pX", {"rootFolderId": "NEW", "notebookId": "nb1"})
        _new_runs = [p for p in _journal_dir().glob("*.jsonl") if p.name not in _jd_before]
        _cw = []
        for p in _new_runs:
            _cw.extend([r for r in _journal_read(p.stem) if r.get("op") == "config_write"])
        _cw_int = next((r for r in _cw if r.get("t") == "intent"), {})
        _cw_cmt = next((r for r in _cw if r.get("t") == "commit"), {})
        _disk = _jm.loads(_cfg_tmp.read_text(encoding="utf-8"))
        cases.append(("r3_config_write_journaled",
                      bool(_written) and _disk["profiles"]["pX"]["rootFolderId"] == "NEW"
                      and _cw_int.get("before") == {"rootFolderId": "OLD"} and _cw_int.get("set", {}).get("notebookId") == "nb1"
                      and _cw_cmt.get("ok") is True))
    except Exception:
        cases.append(("r3_config_write_journaled", False))
    finally:
        try:
            _cfg_tmp.unlink()
        except Exception:
            pass
        for p in (_journal_dir().glob("*.jsonl") if _journal_dir().exists() else []):
            if p.name not in _jd_before:
                try:
                    p.unlink()
                except Exception:
                    pass

    # ═══ v1.29.4 (xử 5 vấn đề LIVE i1-i5 + roadmap #8/#9/#10) — r4_* ═══
    _r4_env = {k: _os3.environ.get(k) for k in ("TL_PROFILE", "TL_REGISTRY_DOC_ID")}
    _r4_runs = []
    try:
        _os3.environ["TL_PROFILE"] = "selftest-r4"
        _os3.environ.pop("TL_REGISTRY_DOC_ID", None)
        # (i3/i4) _journaled_reg_clear: cleared≥1 = verified; cleared=0 = HỤT; cột không clearable = CHẶN TRƯỚC call
        _rid4 = _apply_journal_start("selftest-r4-clear", {}); _r4_runs.append(_rid4)
        _gc1 = _FakeG(get_r={"ok": True, "cleared": 1, "drive_ids": ["dC"]})
        _vc1 = _journaled_reg_clear(_rid4, _gc1, "dC", "nlm_source_id", before={"nlm_source_id": "sOLD"})
        _gc0 = _FakeG(get_r={"ok": True, "cleared": 0})
        _vc0 = _journaled_reg_clear(_rid4, _gc0, "dC", "nlm_source_id")
        _gcb = _FakeG()
        _vcb = _journaled_reg_clear(_rid4, _gcb, "dC", "sohieu")
        _rc4 = _journal_read(_rid4)
        _rc4_int = next((r for r in _rc4 if r.get("t") == "intent" and r.get("op") == "reg_clear"), {})
        cases.append(("r4_journaled_reg_clear",
                      _vc1.get("verified") is True and _vc1.get("cleared") == 1
                      and _gc1.gets and _gc1.gets[0][0] == "reg_clear" and _gc1.gets[0][1].get("confirm") == "yes"
                      and _vc0.get("verified") is False
                      and _vcb.get("verified") is False and "COLS_NOT_CLEARABLE" in str(_vcb.get("error")) and _gcb.gets == []
                      and _rc4_int.get("before") == {"nlm_source_id": "sOLD"}))
        # (i2) tên chuẩn prefix hiếm KHÔNG còn bị coi 'hỏng cấu trúc'; boilerplate bắt tên bộ-ngành
        cases.append(("r4_name_standard_prefixes",
                      (not _name_looks_nonstandard("KL_18-KL-TW_Tiep_tuc_sap_xep")) and
                      (not _name_looks_nonstandard("CD_32-2026-CD-TTg_To_chuc_ra_soat")) and
                      (not _name_looks_nonstandard("TTLT_01-2020-TTLT_Phoi_hop")) and
                      _name_looks_nonstandard("van ban moi.pdf")))
        cases.append(("r4_boilerplate_agency", _subject_is_boilerplate("Bộ Tài chính") and _subject_is_boilerplate("Ngân hàng Nhà nước")
                      and not _subject_is_boilerplate("Bổ sung một số điều của Luật Kế toán")))
        # (i1) --offset phân trang trong resolver batch
        _ents4 = [{"drive_id": f"d{i}", "name": f"Doc {i}", "cat": "45", "corpus": "true"} for i in range(5)]
        with _hush():   # cảnh báo CẮT BATCH = chính thứ đang test (phân trang loud) — không xả ra console deploy
            _tg_a = _resolve_headerverify_targets(_ty3.SimpleNamespace(drive_id=None, sohieu=None, cat="45", all=False, limit=2, offset=0), _ents4)
            _tg_b = _resolve_headerverify_targets(_ty3.SimpleNamespace(drive_id=None, sohieu=None, cat="45", all=False, limit=2, offset=2), _ents4)
            _tg_c = _resolve_headerverify_targets(_ty3.SimpleNamespace(drive_id=None, sohieu=None, cat="45", all=False, limit=2, offset=4), _ents4)
        cases.append(("r4_headerverify_offset",
                      [e["drive_id"] for e in _tg_a] == ["d0", "d1"] and [e["drive_id"] for e in _tg_b] == ["d2", "d3"]
                      and [e["drive_id"] for e in _tg_c] == ["d4"]))
        # (i5) _gas_get_retry: lỗi transient → retry rồi OK; lỗi webapp THẬT (ok:false JSON) → KHÔNG retry
        class _GFlaky:
            def __init__(self, fails, err):
                self.n, self.fails, self.err = 0, fails, err
            def get(self, action, **kw):
                self.n += 1
                if self.n <= self.fails:
                    return {"ok": False, "error": self.err}
                return {"ok": True, "entries": []}
        _gf = _GFlaky(2, "webapp GET manifest_export: TimeoutError: timed out")
        _gr = _GFlaky(9, "MANIFEST_NOT_FOUND")
        with _hush():   # dòng '[gas-retry] … thử lại' là MOCK chủ đích — không xả ra console deploy
            _rt1 = _gas_get_retry(_gf, "manifest_export", _backoff=0)
            _rt2 = _gas_get_retry(_gr, "manifest_export", _backoff=0)
        cases.append(("r4_gas_retry_transient_only", _rt1.get("ok") is True and _gf.n == 3
                      and _rt2.get("ok") is False and _gr.n == 1))
        # (#10) PURE _ingest_local_cat_gate
        _pd4 = {"45": {"ten": "Van ban khac", "folder": "45_Van_ban_khac"}}
        _g1 = _ingest_local_cat_gate("45", {"45"}, _pd4)
        _g2 = _ingest_local_cat_gate("45", set(), _pd4)
        _g3 = _ingest_local_cat_gate("99", {"45"}, _pd4)
        _g4 = _ingest_local_cat_gate("", {"45"}, _pd4)
        cases.append(("r4_ingest_local_cat_gate",
                      _g1["cat_valid"] and not _g1["need_mkdir"] and not _g1["review_cat"]
                      and _g2["cat_valid"] and _g2["need_mkdir"] and "chưa có folder" in (_g2["cat_note"] or "")
                      and not _g3["cat_valid"] and _g3["review_cat"]
                      and _g4["review_cat"] and "CHƯA gán cat" in (_g4["cat_note"] or "")))
    finally:
        for _k, _vv in _r4_env.items():
            if _vv is None:
                _os3.environ.pop(_k, None)
            else:
                _os3.environ[_k] = _vv
        for _r in _r4_runs:
            try:
                (_journal_dir() / f"{_r}.jsonl").unlink()
            except Exception:
                pass
        try:
            import shutil as _sh4
            _sh4.rmtree(Path(_os3.path.expanduser("~")) / ".tra_luat_cache" / "selftest-r4", ignore_errors=True)
        except Exception:
            pass
    # v1.29.2 (AUDIT roadmap #1) — bust-cache-after-write THỐNG NHẤT trong _journaled_reg_write: có items → bust 1 lần;
    # items rỗng → KHÔNG bust. Monkeypatch qua _TL_MODULE (pattern H1) — không chạm mạng/cache thật.
    _cnt = {"bust": 0}
    _ivb, _vwb = _TL_MODULE._invalidate_manifest_cache, _TL_MODULE._verified_reg_write
    try:
        _TL_MODULE._invalidate_manifest_cache = lambda: _cnt.__setitem__("bust", _cnt["bust"] + 1)
        _TL_MODULE._verified_reg_write = lambda g, items, cols: {
            "verified": True, "reg_ok": True, "patched": 0, "expected": len(items),
            "missed": 0, "missed_ids": [], "reg_bulk": {"ok": True, "patched": 0}}
        _rid3 = _apply_journal_start("selftest-bust", {})
        _vv = _TL_MODULE._journaled_reg_write(_rid3, None, [{"drive_id": "dT", "nlm_title": "x"}], "nlm_title")
        _TL_MODULE._journaled_reg_write(_rid3, None, [], "nlm_title")   # items rỗng → không bust thêm
    finally:
        _TL_MODULE._invalidate_manifest_cache, _TL_MODULE._verified_reg_write = _ivb, _vwb
    cases.append(("r3_bust_cache_after_write", _cnt["bust"] == 1 and bool(_vv.get("verified"))))
    # v1.29.2 (AUDIT roadmap #2) — _reg_before_from_manifest: map key qua _entry_drive_id (manifest đổi drive_id→id),
    # sohieu qua _entry_sohieu (so_hieu); key vắng trong manifest → bỏ qua (best-effort cho undo).
    _mfb = _TL_MODULE._manifest_entries
    try:
        _TL_MODULE._manifest_entries = lambda refresh=False: [
            {"id": "dA", "so_hieu": "80/2025/QH15", "nlm_notebook_id": "nbOLD", "nlm_title": "T1"}]
        _bf = _TL_MODULE._reg_before_from_manifest(
            [{"drive_id": "dA", "nlm_notebook_id": "nbNEW"}, {"drive_id": "dZZ", "nlm_notebook_id": "x"}],
            ["nlm_notebook_id", "sohieu"])
        _bf_src = _TL_MODULE._reg_before_from_manifest([{"nlm_source_id": "sX"}], ["nlm_title"], "nlm_source_id")
    finally:
        _TL_MODULE._manifest_entries = _mfb
    cases.append(("r3_before_from_manifest",
                  _bf.get("dA") == {"nlm_notebook_id": "nbOLD", "sohieu": "80/2025/QH15"} and "dZZ" not in _bf
                  and _bf_src == {}))
    # v1.29.2 — parser: 3 lệnh mới wrap có --force-unsafe (gate escape) + push-overflow giữ required args.
    _ap3 = build_parser()
    _pa3 = _ap3.parse_args(["push-overflow", "--drive-id", "d1", "--source-id", "s1", "--force-unsafe"])
    _pa4 = _ap3.parse_args(["register", "--drive-id", "d1", "--name", "N", "--force-unsafe"])
    _pa5 = _ap3.parse_args(["backfill-notebook", "--notebook", "nb", "--drive-ids", "d1", "--force-unsafe"])
    cases.append(("r3_force_unsafe_flags", _pa3.force_unsafe and _pa4.force_unsafe and _pa5.force_unsafe))
    # ─── PHA 0: nền tảng checkpoint/an toàn (WAL journal + verified-write + preflight) — pure cores ───
    _jr = _journal_resume_state([
        {"t": "run_start", "run_id": "r1", "cmd": "recat"},
        {"t": "plan", "steps": [1, 2, 3], "total": 3},
        {"t": "intent", "key": "d1", "op": "reg", "before": {"cat": "00"}},
        {"t": "commit", "key": "d1", "ok": True},
        {"t": "intent", "key": "d2", "op": "reg", "before": {"cat": "01"}}])   # d2: intent chưa commit → inflight
    cases.append(("journal_resume_done_vs_inflight",
                  _jr["counts"] == {"intents": 2, "done": 1, "inflight": 1}
                  and _jr["done_keys"] == ["d1"] and [iv["key"] for iv in _jr["inflight"]] == ["d2"]))
    _ju = _journal_undo_ops([
        {"t": "intent", "key": "d1", "op": "reg", "cols": "cat", "before": {"cat": "00"}}, {"t": "commit", "key": "d1", "ok": True},
        {"t": "intent", "key": "d2", "op": "reg", "cols": "cat", "before": {"cat": "01"}}, {"t": "commit", "key": "d2", "ok": True},
        {"t": "intent", "key": "d3", "op": "reg", "before": {}}, {"t": "commit", "key": "d3", "ok": True}])   # d3: no before → không undo
    cases.append(("journal_undo_reverse_restore",
                  [o["key"] for o in _ju] == ["d2", "d1"] and _ju[0]["before"] == {"cat": "01"} and all(o["op"] == "restore" for o in _ju)))
    cases.append(("reg_cols_valid_catches_so_hieu",
                  _reg_cols_valid("sohieu,corpus")[0] and (not _reg_cols_valid("so_hieu")[0]) and _reg_cols_valid("so_hieu")[1] == ["so_hieu"]
                  and _reg_cols_valid(["cat", "nlm_source_id"])[0]))
    # review#6: cột RỖNG/None → CHẶN (webapp chỉ vá nlm_title mặc định = ghi mù ngoài ý muốn)
    cases.append(("reg_cols_valid_blocks_empty",
                  (not _reg_cols_valid("")[0]) and (not _reg_cols_valid(None)[0]) and (not _reg_cols_valid([])[0])))
    # review#3: retry ghi intent 2 lần cùng key → resume GIỮ intent đầu; undo 1 restore dùng 'before' GỐC (không mất)
    _jr_retry = _journal_resume_state([
        {"t": "intent", "key": "d1", "op": "reg", "before": {"cat": "OLD"}},
        {"t": "intent", "key": "d1", "op": "reg", "before": {}},
        {"t": "commit", "key": "d1", "ok": True}])
    _ju_retry = _journal_undo_ops([
        {"t": "intent", "key": "d1", "op": "reg", "cols": "cat", "before": {"cat": "OLD"}},
        {"t": "intent", "key": "d1", "op": "reg", "cols": "cat", "before": {}},
        {"t": "commit", "key": "d1", "ok": True}])
    cases.append(("journal_retry_keeps_first_before",
                  _jr_retry["counts"]["inflight"] == 0 and _jr_retry["done_keys"] == ["d1"]
                  and len(_ju_retry) == 1 and _ju_retry[0]["before"] == {"cat": "OLD"}))
    # Pha 1: `_journaled_reg_write` ghi intent{before}+commit{verify} + verified-write (integration, dọn file sau)
    import os as _os2

    class _FGjrw:
        def post(self, action, **kw): return {"ok": True, "patched": len(kw.get("items", []))}
    _test_run = "selftest_jrw_" + str(_os2.getpid())
    _jrw_pass = False
    try:
        _vj = _journaled_reg_write(_test_run, _FGjrw(), [{"drive_id": "dX", "cat": "16"}], "cat", before_by_key={"dX": {"cat": "00"}})
        _recs = _journal_read(_test_run)
        _st2 = _journal_resume_state(_recs)
        _undo2 = _journal_undo_ops(_recs)
        _jrw_pass = (bool(_vj.get("verified")) and _st2["counts"]["done"] == 1 and _st2["done_keys"] == ["dX"]
                     and len(_undo2) == 1 and _undo2[0]["before"] == {"cat": "00"})
    finally:
        try:
            _journal_path(_test_run).unlink()
        except Exception:
            pass
    cases.append(("journaled_reg_write_records_intent_commit", _jrw_pass))
    # commit PER-ROW dùng `miss[]` (API reg_bulk = drive_id KHÔNG khớp): dòng miss=inflight, dòng khớp (kể cả idempotent)=done
    class _FGmiss:
        def post(self, action, **kw):
            its = kw.get("items", [])
            return {"ok": True, "patched": max(0, len(its) - 1), "miss": [its[-1]["drive_id"]] if its else []}
    _run_m = "selftest_miss_" + str(_os2.getpid())
    _miss_pass = False
    try:
        _journaled_reg_write(_run_m, _FGmiss(), [{"drive_id": "dA", "cat": "1"}, {"drive_id": "dB", "cat": "2"}], "cat")
        _stm = _journal_resume_state(_journal_read(_run_m))
        _miss_pass = (_stm["done_keys"] == ["dA"] and [iv["key"] for iv in _stm["inflight"]] == ["dB"])
    finally:
        try:
            _journal_path(_run_m).unlink()
        except Exception:
            pass
    cases.append(("journaled_reg_write_per_row_missed", _miss_pass))
    # (log 2026-07-02) idempotent: reg_bulk patched=0 + KHÔNG miss = ghi lại giá trị đã đúng → THÀNH CÔNG (không báo động giả)
    class _FGidem:
        def post(self, action, **kw): return {"ok": True, "patched": 0, "miss": []}   # 0 đổi, 0 miss
    _run_id2 = "selftest_idem_" + str(_os2.getpid())
    _idem_pass = False
    try:
        _vi = _journaled_reg_write(_run_id2, _FGidem(), [{"drive_id": "dZ", "cat": "1"}], "cat")
        _sti = _journal_resume_state(_journal_read(_run_id2))
        _idem_pass = (_vi["verified"] and _vi.get("no_change") and _sti["done_keys"] == ["dZ"] and not _sti["inflight"])
    finally:
        try:
            _journal_path(_run_id2).unlink()
        except Exception:
            pass
    cases.append(("reg_bulk_idempotent_patched0_ok", _idem_pass))
    # reg_upsert: updated=False (giá trị đã đúng) = idempotent SUCCESS (verified True, changed False); cột lạ vẫn CHẶN
    class _FGups:
        def __init__(self, changed=True): self.changed = changed
        def get(self, action, **kw): return {"ok": True, "updated": self.changed}
    _vu_ok = _verified_reg_upsert(_FGups(True), {"drive_id": "d", "sohieu": "1-2025-VBHN-VPQH"})
    _vu_no = _verified_reg_upsert(_FGups(False), {"drive_id": "d", "sohieu": "x"})     # updated=False → idempotent = OK
    _vu_bad = _verified_reg_upsert(_FGups(True), {"drive_id": "d", "so_hieu": "x"})    # cột lạ → CHẶN trước khi gọi
    cases.append(("verified_reg_upsert_gate",
                  _vu_ok["verified"] and _vu_ok["changed"]
                  and _vu_no["verified"] and (not _vu_no["changed"])      # idempotent: verified True, changed False
                  and (not _vu_bad["verified"]) and _vu_bad.get("error") == "REG_COLS_NOT_IN_SCHEMA"))
    _run_u = "selftest_ups_" + str(_os2.getpid())
    _ups_pass = False
    try:
        _journaled_reg_upsert(_run_u, _FGups(True), {"drive_id": "dU", "sohieu": "1-2025-VBHN-VPQH"}, before={"sohieu": ""})
        _recu = _journal_read(_run_u)
        _stu = _journal_resume_state(_recu)
        _undou = _journal_undo_ops(_recu)
        _ups_pass = (_stu["done_keys"] == ["dU"] and len(_undou) == 1 and _undou[0]["before"] == {"sohieu": ""})
    finally:
        try:
            _journal_path(_run_u).unlink()
        except Exception:
            pass
    cases.append(("journaled_reg_upsert_records", _ups_pass))
    # Pha 2: undo (before, đã commit) vs resume (set, inflight) — phân loại + giữ orig_op/key_field
    _j2 = [
        {"t": "run_start", "run_id": "r2", "cmd": "recat"},
        {"t": "intent", "op": "reg_bulk", "key": "dA", "key_field": "drive_id", "cols": "cat", "set": {"cat": "16"}, "before": {"cat": "00"}},
        {"t": "commit", "op": "reg_bulk", "key": "dA", "ok": True},
        {"t": "intent", "op": "reg_upsert", "key": "dB", "key_field": "drive_id", "cols": "sohieu", "set": {"sohieu": "1-2025-VBHN-VPQH"}, "before": {"sohieu": ""}}]   # dB chưa commit → inflight
    _undo2 = _journal_undo_ops(_j2)
    _res2 = _journal_resume_ops(_j2)
    cases.append(("journal_undo_and_resume_ops",
                  len(_undo2) == 1 and _undo2[0]["key"] == "dA" and _undo2[0]["before"] == {"cat": "00"} and _undo2[0]["orig_op"] == "reg_bulk"
                  and _undo2[0]["key_field"] == "drive_id"
                  and len(_res2) == 1 and _res2[0]["key"] == "dB" and _res2[0]["set"] == {"sohieu": "1-2025-VBHN-VPQH"} and _res2[0]["op"] == "reg_upsert"))
    # (review#2) undo/resume chạm cột IMMUTABLE (sohieu) mà op gốc là reg_bulk → PHẢI đi reg_upsert (reg_bulk bỏ im lặng khi đổi)
    class _FGdisp:
        def __init__(self): self.calls = []
        def get(self, action, **kw): self.calls.append(("get", action)); return {"ok": True, "updated": True}
        def post(self, action, **kw): self.calls.append(("post", action)); return {"ok": True, "patched": len(kw.get("items", []))}
    _run_d = "selftest_disp_" + str(_os2.getpid())
    _disp_pass = False
    try:
        _fd1 = _FGdisp()
        _journal_reapply_one(_run_d, _fd1, {"key": "d", "key_field": "drive_id", "orig_op": "reg_bulk", "cols": "sohieu"}, {"sohieu": ""})
        _fd2 = _FGdisp()
        _journal_reapply_one(_run_d, _fd2, {"key": "d", "key_field": "drive_id", "orig_op": "reg_bulk", "cols": "cat"}, {"cat": "00"})
        _disp_pass = (("get", "reg_upsert") in _fd1.calls and ("post", "reg_bulk") not in _fd1.calls       # sohieu → upsert
                      and ("post", "reg_bulk") in _fd2.calls)                                              # cat → bulk
    finally:
        try:
            _journal_path(_run_d).unlink()
        except Exception:
            pass
    cases.append(("reapply_immutable_col_uses_upsert", _disp_pass))
    # Pha 3: loop controller (hội tụ/no-progress/max-iter) + step-decision (chỉ DONE khi verify)
    cases.append(("pipeline_step_decision",
                  _pipeline_step_decision(False, True, True) == "SKIP"
                  and _pipeline_step_decision(True, False, True) == "PAUSE"
                  and _pipeline_step_decision(True, True, False) == "PAUSE"
                  and _pipeline_step_decision(True, True, True) == "DONE"))
    cases.append(("loop_controller_converged",
                  _loop_controller([{"fixed": 5, "remaining": 5}, {"fixed": 0, "remaining": 0}, {"fixed": 0, "remaining": 0}], k_dry=2, max_iter=8)["status"] == "converged"))
    cases.append(("loop_controller_no_progress",
                  _loop_controller([{"fixed": 5, "remaining": 5}, {"fixed": 5, "remaining": 5}], k_dry=2, max_iter=8)["status"] == "paused"))
    cases.append(("loop_controller_continue",
                  _loop_controller([{"fixed": 5, "remaining": 5}, {"fixed": 3, "remaining": 3}], k_dry=2, max_iter=8)["status"] == "continue"))
    cases.append(("loop_controller_max_iter",
                  _loop_controller([{"fixed": 1, "remaining": 1}] * 8, k_dry=2, max_iter=8)["status"] == "paused"))
    cases.append(("verify_reg_result_by_missed_not_patched",
                  _verify_reg_result({"ok": True, "patched": 3, "miss": []}, 3)["verified"]                    # đủ, không miss → OK
                  and _verify_reg_result({"ok": True, "patched": 0, "miss": []}, 3)["verified"]               # idempotent (patched<expected, không miss) → OK
                  and _verify_reg_result({"ok": True, "patched": 0, "miss": []}, 3)["no_change"]              # cờ no_change
                  and (not _verify_reg_result({"ok": True, "patched": 2, "miss": ["dX"]}, 3)["verified"])     # có miss → HỤT thật
                  and (not _verify_reg_result({"ok": False, "patched": 3}, 3)["verified"])))                  # ok=False → hụt

    class _FakeGas:
        def __init__(self): self.calls = []
        def post(self, action, **kw): self.calls.append((action, kw)); return {"ok": True, "patched": len(kw.get("items", []))}
    _fg = _FakeGas()
    _vw_bad = _verified_reg_write(_fg, [{"drive_id": "d", "so_hieu": "1/2025"}], "so_hieu")   # cột lạ → KHÔNG post
    _vw_ok = _verified_reg_write(_fg, [{"drive_id": "d", "sohieu": "1/2025"}], "sohieu")       # hợp lệ → post 1 lần
    cases.append(("verified_reg_write_blocks_bad_cols",
                  (not _vw_bad["verified"]) and _vw_bad.get("error") == "REG_COLS_NOT_IN_SCHEMA"
                  and _vw_ok["verified"] and len(_fg.calls) == 1))
    _LEG = "1mATGFhaW0e_CYienAD80DsTS1K4zfJNlTAx-DsHaCD8"
    _pf_leg = _preflight_verdict(_preflight_invariants({"registryDocId": _LEG, "is_base_profile": True}))
    _pf_emp = _preflight_verdict(_preflight_invariants({"registryDocId": "SHEET1", "is_base_profile": False, "profile_registry_id": ""}))
    _pf_bad = _preflight_verdict(_preflight_invariants({"registryDocId": "SHEET1", "is_base_profile": True, "write_cols": "so_hieu"}))
    _pf_ok = _preflight_verdict(_preflight_invariants({"registryDocId": "SHEET1", "is_base_profile": True, "write_cols": "sohieu", "snapshot_age_seconds": 10}))
    _pf_stale = _preflight_verdict(_preflight_invariants({"registryDocId": "SHEET1", "is_base_profile": True, "snapshot_age_seconds": 5000}))
    cases.append(("preflight_invariants_gate",
                  (not _pf_leg["ok"]) and "REGISTRY_NOT_LEGACY_DOC" in _pf_leg["blockers"]
                  and (not _pf_emp["ok"]) and "PROFILE_REGISTRY_ID_NOT_EMPTY" in _pf_emp["blockers"]
                  and (not _pf_bad["ok"]) and "WRITE_COLS_IN_SCHEMA" in _pf_bad["blockers"]
                  and _pf_ok["ok"] and not _pf_ok["warnings"]
                  and _pf_stale["ok"] and "MANIFEST_FRESH" in _pf_stale["warnings"]))
    # goc-pollution (ca thật 21-LCT-HDNN8 vs Dân số 113-2025): VBHN tên mã hoá base 21-LCT-HDNN8 nhưng goc NHIỄM 113-2025
    # → component Dân số KHỚP goc nhưng KHÔNG corroborate → review GOC_POLLUTION_SUSPECT, KHÔNG auto corpus=false
    _cc3 = _consolidation_cleanup_plan([
        {"drive_id": "vbhnp", "name": "VBHN_22-VBHN-VPQH_Bao_ve_suc_khoe_nhan_dan_goc_21-LCT-HDNN8", "so_hieu": "22-VBHN-VPQH",
         "loai": "VBHN", "goc": "21-LCT-HDNN8;113-2025-QH15", "corpus": "true", "nlm_source_id": "np"},
        {"drive_id": "danso", "name": "Luat_113-2025-QH15_Dan_so", "so_hieu": "113-2025-QH15", "corpus": "true"}])
    cases.append(("consolidation_cleanup_routes_goc_pollution_to_review",
                  _cc3["total_ready"] == 0
                  and any(r["drive_id"] == "danso" and r.get("reason") == "GOC_POLLUTION_SUSPECT" and r.get("corroborated") is False
                          for r in _cc3["review_on_nlm"])))
    # (MERGE Claude) GUARD shared_source_id khi purge NLM của profile/file (không xóa nguồn gãy link kia)
    _pds_entries = [{"drive_id": "d1", "nlm_source_id": "SH", "nlm_status": "pushed"},
                    {"drive_id": "d2", "nlm_source_id": "SH", "nlm_status": "pushed"},
                    {"drive_id": "d3", "nlm_source_id": "U", "nlm_status": "pushed"}]
    _pds_ok, _pds_blk = _profile_deletable_sources(_pds_entries, ["SH", "U"])
    cases.append(("profile_deletable_guards_shared", _pds_ok == ["U"] and _pds_blk == ["SH"]))
    _gate_unverified = _ingest_verify_gate(_draft_text, _dinfo, "ocr", False)
    _gate_verified = _ingest_verify_gate(_draft_text + "\nPhụ lục\nNội dung", _dinfo, "ocr", True)
    cases.append(("profile_ingest_ocr_gate",
                  (not _gate_unverified["corpus_allowed"]) and _gate_verified["corpus_allowed"]))
    _long_dieu_text = (
        "Mở đầu\n"
        "Điều 1. A\n" + ("x\n" * 6000) +
        "Điều 2. B\n" + ("x\n" * 6000) +
        "Điều 3. C\nx\n"
    )
    _chunks = _split_by_dieu_chunks(_long_dieu_text, max_chars=10000)
    cases.append(("profile_ingest_split_by_dieu",
                  len(_chunks) >= 2 and all("Điều" in c["text"] for c in _chunks)
                  and _chunks[0]["start_dieu"] == 1))
    cases.append(("draft_title_flag_and_source_map_warning",
                  "DRAFT_NOT_EFFECTIVE" in _title_flags({"name": "DUTHAO_NQ_42", "hieuluc": "du_thao"})
                  and any("DRAFT_NOT_EFFECTIVE" in w for w in _source_map_one("42/2026/NQ-CP", [
                      {"id": "d", "name": "DUTHAO_NQ_42", "so_hieu": "42/2026/NQ-CP", "hieuluc": "du_thao", "corpus": "true"}
                  ])["warnings"])))
    cases.append(("registry_schema_27_cols", len(REGISTRY_SCHEMA_COLS) == 27 and REGISTRY_SCHEMA_COLS[-1] == "row_kind"))
    # Instruction profile: cross_notebook_query gồm profile + VBQPPL + VBQPPL-2 (+shard), ưu tiên profile, id thật → dùng được luôn.
    try:
        import gen_instructions as _gi
        _instr = _gi.generate("project", "1.24.0", "kx_profile", "NBPROFILEX", "kx_profile", "ROOTX")
        cases.append(("instruction_cross_notebook_all_shards",
                      "NBPROFILEX" in _instr and "743ed200" in _instr and "45739ff7" in _instr
                      and "ƯU TIÊN TÌM TRONG 1 NOTEBOOK" in _instr and "canonical PROFILE THẮNG" in _instr
                      and "cross_notebook_query" in _instr and _gi.audit(_instr).get("ok") is True))
    except Exception:
        cases.append(("instruction_cross_notebook_all_shards", False))
    _old_prof, _old_cat, _old_reg = os.environ.get("TL_PROFILE"), os.environ.get("TL_CATEGORIES_MODE"), os.environ.get("TL_REGISTRY_DOC_ID")
    try:
        os.environ["TL_PROFILE"] = "nq36"; os.environ["TL_CATEGORIES_MODE"] = "inherit"; os.environ["TL_REGISTRY_DOC_ID"] = "SHEET1"
        _pe = _profile_policy_error(require_registry=True, forbid_inherit=True)
        cases.append(("profile_policy_forbids_inherit", (_pe or {}).get("error") == "PROFILE_CATEGORIES_INHERIT_FORBIDDEN"))
    finally:
        for _k, _v in (("TL_PROFILE", _old_prof), ("TL_CATEGORIES_MODE", _old_cat), ("TL_REGISTRY_DOC_ID", _old_reg)):
            if _v is None:
                os.environ.pop(_k, None)
            else:
                os.environ[_k] = _v
    fx = [
        {"id":"goc41", "name":"Luat_41-2024-QH15_BHXH", "so_hieu":"41-2024-QH15", "cat":"20", "corpus":"true"},
        {"id":"vbhn19", "name":"VBHN_19-VPQH_Bao_hiem_xa_hoi", "so_hieu":"19-VPQH", "loai":"VBHN", "goc":"41-2024-QH15", "cat":"20", "nlm_source_id":"n", "corpus":"true"},
        {"id":"wrong57", "name":"Luat_57-2024-QH15_Bao_hiem_y_te", "so_hieu":"57-2024-QH15", "cat":"34", "title_vn":"Luật sửa đổi, bổ sung một số điều của Luật Quy hoạch, Luật Đầu tư, Luật Đầu tư theo phương thức đối tác công tư và Luật Đấu thầu", "goc":"15/2017/QH14;39/2019/QH14;64/2020/QH14", "corpus":"true"},
        {"id":"vbhn40", "name":"VBHN_40-VPQH_Bao_hiem_y_te", "so_hieu":"40-VPQH", "loai":"VBHN", "goc":"25-2008-QH12;46-2014-QH13;51-2024-QH15", "cat":"20", "nlm_source_id":"n", "corpus":"true"},
        {"id":"atvsld", "name":"Luat_84-2015-QH13_An_toan_ve_sinh_lao_dong", "so_hieu":"84-2015-QH13", "cat":"20", "nlm_source_id":"n", "corpus":"true"},
    ]
    cases.append(("source_map_vbhn_first", (_source_map_one("41/2024/QH15", fx)["canonical"] or {}).get("drive_id") == "vbhn19"))
    cases.append(("source_map_name_pollution", (_source_map_one("bảo hiểm y tế", fx)["canonical"] or {}).get("drive_id") == "vbhn40"))
    cases.append(("source_map_no_verified_vbhn_warning", any("NO_VERIFIED_VBHN" in w for w in _source_map_one("84/2015/QH13", fx)["warnings"])))
    cases.append(("source_map_new_law_quiet", not any("NO_VBHN" in w for w in _source_map_one("74/2025/QH15", fx + [{"id":"law74", "name":"Luat_74-2025-QH15_Viec_lam", "so_hieu":"74-2025-QH15", "cat":"20", "nlm_source_id":"n", "hieuluc":"Còn hiệu lực"}])["warnings"])))
    cases.append(("vbhn_bare_number_flag", set(_title_flags({"id":"v14", "name":"VBHN_14-VBHN-VPQH", "so_hieu":"14/VBHN-VPQH", "loai":"VBHN", "cat":"20"})) >= {"VBHN_BARE_NUMBER", "VBHN_MISSING_YEAR_OR_DATE"}))
    cases.append(("source_map_vbhn_number_reuse_risk", any("VBHN_NUMBER_REUSE_RISK" in w for w in _source_map_one("14/VBHN-VPQH", [{"id":"v14", "name":"VBHN_14-VBHN-VPQH", "so_hieu":"14/VBHN-VPQH", "loai":"VBHN", "cat":"20"}])["warnings"])))
    # v1.22.61 (log Chat/Cowork): VBHN-first redirect CHỈ cho BẢN GỐC (base), KHÔNG cho luật-sửa-trong-chuỗi; NĐ/TT không thể
    # sửa Luật (sai thứ bậc); PENDING hiệu-lực-tương-lai nổi ngay ở source-map.
    _v61fx = fx + [
        {"id":"thuocla", "name":"VBHN_11-VBHN-VPQH_Luat_PCTH_thuoc_la", "so_hieu":"11-VBHN-VPQH", "loai":"VBHN",
         "goc":"09-2012-QH13;28-2018-QH14;114-2025-QH15", "cat":"02", "nlm_source_id":"n", "corpus":"true"},
        {"id":"phongbenh", "name":"Luat_114-2025-QH15_Phong_benh", "so_hieu":"114-2025-QH15", "cat":"02", "corpus":"true"},
    ]
    _sm114 = _source_map_one("114/2025/QH15", _v61fx)
    cases.append(("vbhn_base_redirect_skips_amendment", (_sm114["canonical"] or {}).get("drive_id") == "phongbenh"))
    cases.append(("vbhn_amends_other_not_redirect", any("AMENDS_OTHER_VBHN" in w for w in _sm114["warnings"]) and not _sm114["related_vbhn"]))
    cases.append(("vbhn_base_redirect_for_real_base", (_source_map_one("09/2012/QH13", _v61fx)["canonical"] or {}).get("drive_id") == "thuocla"))
    # v1.24.1 (log rà 108 lần — §1.1/§1.2/A3/B3): chống registry.goc NHIỄM khiến redirect VBHN-first sang SAI văn bản.
    cases.append(("name_goc_base_extract",
        _name_goc_base_key("VBHN_22-VBHN-VPQH_Luat_Bao_ve_suc_khoe_nhan_dan_goc_21-LCT-HDNN8") == norm_sohieu("21-LCT-HDNN8")
        and _name_goc_base_key("VBHN_123-VBHN-VPQH_Luat_PPP_goc_64-2020-QH14") == "64-2020-QH14"
        and _name_goc_base_key("VBHN_89-VBHN-VPQH_Luat_NSNN_goc_89-2025-QH15_sdbs_145-2025-QH15") == "89-2025-QH15"
        and _name_goc_base_key("Luat_113-2025-QH15_Dan_so") == ""))
    _pollfx = [
        {"id":"danso", "name":"Luat_113-2025-QH15_Dan_so", "so_hieu":"113-2025-QH15", "cat":"08", "corpus":"true", "nlm_source_id":"n"},
        {"id":"bvskvbhn", "name":"VBHN_22-VBHN-VPQH_Luat_Bao_ve_suc_khoe_nhan_dan_goc_21-LCT-HDNN8", "so_hieu":"22-VBHN-VPQH", "loai":"VBHN", "goc":"113-2025-QH15", "cat":"02", "corpus":"true", "nlm_source_id":"n2"},
    ]
    _smpoll = _source_map_one("113/2025/QH15", _pollfx)
    cases.append(("source_map_goc_pollution_no_wrong_redirect",
        (_smpoll["canonical"] or {}).get("drive_id") == "danso"
        and any("GOC_SUBJECT_MISMATCH" in w for w in _smpoll["warnings"])
        and bool(_smpoll.get("goc_mismatch_vbhn")) and not _smpoll.get("related_vbhn")))
    cases.append(("goc_pollution_detector",
        len(_goc_pollution_groups(_pollfx)) == 1
        and _goc_pollution_groups(_pollfx)[0]["name_goc_base"] == norm_sohieu("21-LCT-HDNN8")))
    _legitvbhn = [
        {"id":"pppluat", "name":"Luat_64-2020-QH14_Dau_tu_PPP", "so_hieu":"64-2020-QH14", "cat":"34", "corpus":"true"},
        {"id":"pppvbhn", "name":"VBHN_123-VBHN-VPQH_Luat_PPP_goc_64-2020-QH14", "so_hieu":"123-VBHN-VPQH", "loai":"VBHN", "goc":"64-2020-QH14;57-2024-QH15;90-2025-QH15", "cat":"34", "corpus":"true", "nlm_source_id":"n"},
        {"id":"sd57", "name":"Luat_57-2024-QH15_SuaDoi_PPP", "so_hieu":"57-2024-QH15", "cat":"34", "corpus":"true", "nlm_source_id":"n3", "goc":"64-2020-QH14", "title_vn":"Luật sửa đổi, bổ sung một số điều của Luật Đầu tư theo phương thức đối tác công tư"},
        {"id":"sd57docx", "name":"Luat_57-2024-QH15_SuaDoi_PPP.docx", "so_hieu":"57-2024-QH15", "cat":"34", "corpus":"true", "title_vn":"Luật sửa đổi PPP"},
    ]
    _smppp = _source_map_one("64/2020/QH14", _legitvbhn)
    cases.append(("vbhn_first_redirect_corroborated_preserved", (_smppp["canonical"] or {}).get("drive_id") == "pppvbhn"))
    cases.append(("goc_pollution_no_false_positive_on_legit", _goc_pollution_groups(_legitvbhn) == []))
    cases.append(("consolidated_amendment_suppresses_pause",
        _smppp.get("action_required") != "PAUSE_AND_ASK_USER"
        and any("AMENDMENTS_ALREADY_CONSOLIDATED" in w for w in _smppp["warnings"])
        and bool(_smppp.get("consolidated_amendments"))))
    _dupfx = [
        {"id":"base", "name":"Luat_06-2022-QH15_Thi_dua", "so_hieu":"06-2022-QH15", "cat":"29", "corpus":"true", "nlm_source_id":"n"},
        {"id":"am1", "name":"Luat_06-2026-QH16_SuaDoi_Thi_dua", "so_hieu":"06-2026-QH16", "cat":"29", "corpus":"true", "nlm_source_id":"n2"},
        {"id":"am1docx", "name":"Luat_06-2026-QH16_SuaDoi_Thi_dua.docx", "so_hieu":"06-2026-QH16", "cat":"29", "corpus":"true"},
    ]
    _amc = _find_amendment_candidates("06-2022-QH15", [_dupfx[0]], [], _dupfx)
    cases.append(("amendment_candidate_dedup_raw_docx", sum(1 for e in _amc if _sohieu_key_entry(e) == "06-2026-QH16") == 1))
    _hnfx = [{"id":"hn", "name":"VBHN_121-VBHN-VPQH_2025_Luat_Hon_nhan_va_gia_dinh", "so_hieu":"52-2014-QH13", "cat":"08", "corpus":"true", "nlm_source_id":"n"}]
    cases.append(("canonical_vbhn_number_differs_warn",
        any("CANONICAL_VBHN_NUMBER_DIFFERS" in w for w in _source_map_one("52/2014/QH13", _hnfx)["warnings"])))
    _riskyfx = [{"id":"r", "name":"Luat_99-2025-QH15_Test", "so_hieu":"99-2025-QH15", "cat":"", "corpus":"true"}]
    _smr = _source_map_one("99/2025/QH15", _riskyfx)
    cases.append(("risky_candidate_has_reason", bool(_smr["risky_candidates"]) and all(rc.get("reason") for rc in _smr["risky_candidates"])))
    cases.append(("flags_reason_maps", "thiếu folder chủ đề hợp lệ" in _flags_reason(["ORPHAN_CAT"]) and _flags_reason([]) == ""))
    _lctfx = [{"id":"lct", "name":"Luat_21-LCT-HDNN8_Bao_ve_suc_khoe_nhan_dan", "so_hieu":"21-LCT-HDNN8", "cat":"45", "corpus":"true", "nlm_source_id":"n"}]
    _smlct = _source_map_one("21-LCT-HDNN8", _lctfx)
    cases.append(("source_map_lct_hdnn_direct",
                  _looks_like_sohieu_query("21-LCT-HDNN8") and _parse_sohieu_from_name("Luat_21-LCT-HDNN8.docx") == "21-LCT-HDNN8"
                  and (_smlct["canonical"] or {}).get("drive_id") == "lct" and _smlct["mode"] == "direct_sohieu"
                  and _vbhn_base_key({"loai":"VBHN", "goc":"21-LCT-HDNN8;113-2025-QH15"}) == "21-LCT-HDNN8"))
    _ghost_pool = [
        {"id":"ghost", "name":"", "so_hieu":"60/2024/QH15", "cat":"root", "corpus":"true"},
        {"id":"real60", "name":"Luat_60-2024-QH15_Du_lieu", "so_hieu":"60/2024/QH15", "cat":"32", "corpus":"true", "nlm_source_id":"n", "nlm_notebook_id":"nb"},
    ]
    _smghost = _source_map_one("60/2024/QH15", _ghost_pool)
    cases.append(("source_map_empty_name_not_risky_warn",
                  not any((rc.get("entry") or {}).get("drive_id") == "ghost" for rc in _smghost.get("risky_candidates") or [])
                  and not any("TITLE_OR_REGISTRY_WARN" in w for w in _smghost.get("warnings") or [])))
    _smstatus = _source_map_one("60/2024/QH15", [{"id":"stat", "name":"Luat_60-2024-QH15_Du_lieu", "so_hieu":"60/2024/QH15", "cat":"32", "corpus":"true", "nlm_source_id":"n", "nlm_status":"added", "nlm_notebook_id":"nb"}])
    cases.append(("source_map_suppresses_global_nlm_status",
                  "NLM_STATUS_MISMATCH" in _title_flags({"name":"x", "so_hieu":"60/2024/QH15", "cat":"32", "nlm_source_id":"n", "nlm_status":"added"})
                  and "NLM_STATUS_MISMATCH" not in ((_smstatus["canonical"] or {}).get("flags") or [])
                  and not _smstatus.get("risky_candidates")))
    cases.append(("json_verdict_helpers",
                  _source_map_verdict(_smstatus) in {"OK", "REVIEW"}
                  and _vbhn_check_verdict(["QT5_WEB_REQUIRED"], False) == "QT5_WEB_REQUIRED"))
    # A3 (tối ưu MERGE): bản THÔ song song chỉ dính cờ TRÔI (CORPUS_TRUE_NOT_ON_NLM/RAW_NAME_NOT_NLM) → KHÔNG kích WARN
    _rawsib = [
        {"id":"gdoc60", "name":"Luat_60-2024-QH15_Du_lieu", "so_hieu":"60/2024/QH15", "cat":"32_Thong_tin_truyen_thong", "corpus":"true", "nlm_source_id":"n", "nlm_status":"pushed", "nlm_notebook_id":"nb"},
        {"id":"raw60", "name":"Luat_60_2024_QH15_Du_lieu.doc", "so_hieu":"60/2024/QH15", "cat":"32_Thong_tin_truyen_thong", "corpus":"true"},
    ]
    cases.append(("title_warn_skips_raw_sibling_drift", not any("TITLE_OR_REGISTRY_WARN" in w for w in _source_map_one("60/2024/QH15", _rawsib)["warnings"])))
    # ...nhưng cờ SIÊU-DỮ-LIỆU per-law thật (ORPHAN_CAT) VẪN kích WARN
    _orphfx2 = [{"id":"orph2", "name":"Luat_88-2025-QH15_Test", "so_hieu":"88-2025-QH15", "cat":"root", "corpus":"true", "nlm_source_id":"n", "nlm_status":"pushed", "nlm_notebook_id":"nb"}]
    cases.append(("title_warn_fires_on_substantive_flag", any("TITLE_OR_REGISTRY_WARN" in w for w in _source_map_one("88/2025/QH15", _orphfx2)["warnings"])))
    # §1.3: VBHN không dẫn-chiếu goc đã cho → cờ GOC_NOT_EVIDENT_IN_METADATA (driver tách uncertain_candidates trong cmd_vbhn_check)
    cases.append(("vbhn_quality_flag_goc_not_evident",
        "GOC_NOT_EVIDENT_IN_METADATA" in _vbhn_quality_flags(
            {"name":"VBHN_92-VPQH_2025_Luat_Thanh_nien", "so_hieu":"92-VBHN-VPQH", "loai":"VBHN", "cat":"29"},
            "Việc làm", {norm_sohieu("74-2025-QH15")}, "")
        and "GOC_NOT_EVIDENT_IN_METADATA" not in _vbhn_quality_flags(
            {"name":"VBHN_14_ATVSLD", "so_hieu":"14-VBHN-VPQH", "loai":"VBHN", "goc":"84-2015-QH13", "cat":"20"},
            "an toàn vệ sinh lao động", {norm_sohieu("84-2015-QH13")}, "")))
    # §1.8 (preingest_gate): luật mới hieuluc trống → REVIEW nhưng nêu GAP + gợi ý (không tự kết luận)
    try:
        _pg = _imp("preingest_gate")
        import datetime as _dt2
        _cur = _dt2.date.today().year
        _dnew = _pg.decide({"status":"IN_REGISTRY_HIEULUC_UNKNOWN", "sohieu":f"134-{_cur}-QH15"})
        _dold = _pg.decide({"status":"IN_REGISTRY_HIEULUC_UNKNOWN", "sohieu":"45-1990-QH8"})
        cases.append(("status_hieuluc_unknown_recent_hint",
            _dnew["decision"] == "REVIEW" and _dnew.get("hieuluc_unknown") is True
            and _dnew.get("recent_issue_year") == _cur and "nhiều khả năng" in _dnew["reason"]
            and _dold.get("recent_issue_year") == 1990 and "nhiều khả năng" not in _dold["reason"]))
    except Exception:
        cases.append(("status_hieuluc_unknown_recent_hint", False))
    # v1.24.1 MERGE (port Codex hotfix): date-coverage hạ PAUSE + status subject-guard
    cases.append(("entry_issue_date_iso_parse",
        _entry_issue_date_iso({"ngay_ban_hanh":"15/06/2025"}) == "2025-06-15"
        and _entry_issue_date_iso({"issue_date":"2025-06-15"}) == "2025-06-15"
        and _entry_issue_date_iso({"ngay_ban_hanh":"ngày 16 tháng 9 năm 2024"}) == "2024-09-16"
        and _entry_issue_date_iso({"name":"x"}) is None))
    _cov_vb = {"loai":"VBHN", "sohieu":"20-VBHN-VPQH", "name":"VBHN_20", "ngay_ban_hanh":"15/06/2025"}
    _cov1 = _amendments_covered_by_vbhn_date(_cov_vb, [{"sohieu":"62-2022-QH15", "ngay_ban_hanh":"20/11/2022"}])[0]
    _cov2 = _amendments_covered_by_vbhn_date(_cov_vb, [{"sohieu":"99-2026-QH15", "ngay_ban_hanh":"01/01/2026"}])[0]
    _cov3 = _amendments_covered_by_vbhn_date(_cov_vb, [{"sohieu":"62-2022-QH15"}])[0]
    cases.append(("amendments_covered_by_vbhn_date", _cov1 is True and _cov2 is False and _cov3 is False))
    _datefx = [
        {"id":"basex", "name":"Luat_50-2020-QH14_Xay_dung", "so_hieu":"50-2020-QH14", "cat":"25", "corpus":"true", "nlm_source_id":"n"},
        {"id":"vbhnx", "name":"VBHN_20-VBHN-VPQH_2025_Luat_Xay_dung_goc_50-2020-QH14", "so_hieu":"20-VBHN-VPQH", "loai":"VBHN", "goc":"50-2020-QH14", "cat":"25", "corpus":"true", "nlm_source_id":"n2", "ngay_ban_hanh":"15/06/2025"},
        {"id":"amx", "name":"Luat_62-2022-QH15_SuaDoi_Xay_dung", "so_hieu":"62-2022-QH15", "cat":"25", "corpus":"true", "nlm_source_id":"n3", "goc":"50-2020-QH14", "ngay_ban_hanh":"20/11/2022", "title_vn":"Luật sửa đổi, bổ sung một số điều của Luật Xây dựng"},
    ]
    _smdate = _source_map_one("50/2020/QH14", _datefx)
    cases.append(("source_map_amendment_covered_by_vbhn_date",
        _smdate.get("covered_by_vbhn_date") is True and _smdate.get("action_required") != "PAUSE_AND_ASK_USER"
        and any("COVERED_BY_VBHN_DATE" in w for w in _smdate["warnings"])))
    try:
        _pg = _imp("preingest_gate")
        _dmis = _pg.decide({"sohieu":"113-2025-QH15", "name":"Luat Dan so", "status":"CONSOLIDATED_INTO_VBHN",
                            "superseded_by":[{"sohieu":"18-2026-VBHN-VPQH", "name":"Bo luat Lao dong", "on_nlm":True}]})
        # MERGE Codex v1.33.11 (ca 143-2025→61-2026 log): VBHN gợi ý KHÔNG có tên/chủ đề để corroborate →
        # REVIEW VBHN_GOC_SUBJECT_UNVERIFIED (trước đây unknown = no-op → tự tin USE_VBHN không bằng chứng).
        _dunk = _pg.decide({"sohieu":"143-2025-QH15", "name":"Luat Dau tu", "status":"CONSOLIDATED_INTO_VBHN",
                            "superseded_by":[{"sohieu":"61-2026-VBHN-VPQH", "on_nlm":True}]})
        _dok = _pg.decide({"sohieu":"84-2015-QH13", "name":"Luat An toan ve sinh lao dong", "status":"CONSOLIDATED_INTO_VBHN",
                           "superseded_by":[{"sohieu":"14-2024-VBHN-VPQH", "name":"An toan ve sinh lao dong hop nhat", "on_nlm":True}]})
        cases.append(("status_vbhn_subject_mismatch_guard",
            _dmis["decision"] == "REVIEW" and _dmis.get("surface") == "VBHN_GOC_SUBJECT_MISMATCH"
            and _dunk["decision"] == "REVIEW" and _dunk.get("surface") == "VBHN_GOC_SUBJECT_UNVERIFIED"
            and _dok["decision"] == "SKIP" and _dok.get("use_vbhn") == "14-2024-VBHN-VPQH"))
    except Exception:
        cases.append(("status_vbhn_subject_mismatch_guard", False))
    cases.append(("vb_tier_rank_levels",
        _vb_tier_rank({"so_hieu":"41-2024-QH15"}) == 5 and _vb_tier_rank({"so_hieu":"18-VBHN-VPQH", "loai":"VBHN"}) == 5
        and _vb_tier_rank({"so_hieu":"23-2024-PL-UBTVQH15"}) == 4 and _vb_tier_rank({"so_hieu":"118-2016-ND-CP"}) == 3
        and _vb_tier_rank({"so_hieu":"31-2024-TT-BYT"}) == 2))
    cases.append(("vb_tier_rank_from_name_when_sohieu_empty", _vb_tier_rank({"name":"118_2016_ND-CP_sửa đổi Nghị định"}) == 3))
    _amfx = [
        {"id":"law25", "name":"Luat_25-2008-QH12_Bao_hiem_y_te", "so_hieu":"25-2008-QH12", "cat":"02", "corpus":"true", "nlm_source_id":"n"},
        {"id":"nd118", "name":"Nghi_dinh_118-2016-ND-CP_sửa đổi bổ sung một số điều", "so_hieu":"118-2016-ND-CP", "goc":"25-2008-QH12", "cat":"02", "corpus":"true"},
    ]
    _smam = _source_map_one("25/2008/QH12", _amfx)
    cases.append(("amendment_gate_excludes_lower_tier", not any(c.get("drive_id") == "nd118" for c in _smam["amendment_candidates"])))
    _smp = _source_map_one("99/2027/QH16", [{"id":"futurelaw", "name":"Luat_99-2027-QH16_Test", "so_hieu":"99-2027-QH16", "cat":"02", "corpus":"true", "hieuluc":"01/01/2099"}])
    cases.append(("source_map_pending_future_effect", _smp.get("pending_future_count", 0) >= 1 and any("PENDING_FUTURE_EFFECT" in w for w in _smp["warnings"])))
    # v1.22.63 (merge): đọc HEADER xác minh + nhãn confirm + upload-flow MIME
    _ce = {"so_hieu":"25-2008-QH12", "name":"Luat_25-2008-QH12_Bao_hiem_y_te", "cat":""}
    _vh = _verify_header_match(_ce, "LUẬT BẢO HIỂM Y TẾ\nLuật số 25/2008/QH12 ngày 14 tháng 11 năm 2008\nĐiều 1. Phạm vi điều chỉnh\nLuật này quy định về bảo hiểm y tế.")
    cases.append(("verify_header_match_pass", _vh["ok"] and _vh["checks"].get("sohieu") and _vh["checks"].get("title") and _vh["checks"].get("loai")))
    _vh2 = _verify_header_match(_ce, "LUẬT BẢO HIỂM Y TẾ\nLuật số 99/2099/QH15\nquy định về bảo hiểm y tế")
    cases.append(("verify_header_match_sohieu_mismatch", (_vh2["checks"].get("sohieu") is False) and not _vh2["ok"]))
    _vh3 = _verify_header_match(_ce, "BỘ LUẬT HÌNH SỰ\nLuật số 25/2008/QH12\nĐiều 1. tội phạm và hình phạt")
    cases.append(("verify_header_match_title_mismatch", (_vh3["checks"].get("title") is False) and not _vh3["ok"]))
    cases.append(("entry_confirmed_label", _entry_confirmed({"verified":"2026-06-28"}) == "2026-06-28" and _entry_confirmed({"verified":""}) == "" and _entry_confirmed({"verified":"no"}) == ""))
    _smc = _source_map_one("bảo hiểm y tế", [{"id":"cc", "name":"Luat_25-2008-QH12_Bao_hiem_y_te", "so_hieu":"", "cat":"root", "corpus":"true", "verified":"2026-06-28"}])
    cases.append(("source_map_confirmed_trusts", any("CONFIRMED" in w for w in _smc["warnings"]) and not any(("DIRTY_CANDIDATES" in w or "TITLE_OR_REGISTRY_WARN" in w) for w in _smc["warnings"])))
    cases.append(("upload_mime_ext", _upload_mime_ext("x.pdf") == ("application/pdf", ".pdf")
                  and _upload_mime_ext("x.doc") == ("application/msword", ".doc")
                  and _upload_mime_ext("VBHN.DOCX") == (_DOCX_MIME, ".docx")
                  and _upload_mime_ext("weird.xyz") == (_DOCX_MIME, ".docx")))
    _ds = _source_map_one("Luật Dân số", [{"id":"ds113", "name":"Luat_113-2025-QH15_Dan_so", "so_hieu":"113/2025/QH15", "cat":"08", "corpus":"true", "nlm_source_id":"n"}])
    cases.append(("source_map_luat_prefix_alias_dan_so", (_ds["canonical"] or {}).get("drive_id") == "ds113"))
    # v1.22.64 (runlog fixes — workflow điều tra+verify đối kháng): name-rank/reg-query/cluster/vbhn-verify/footnote/fontrun/...
    # name_rank: 'Luật Dân số' giữa bản SAI (Dân chủ ở cơ sở, điểm-cao VBHN+nlm) và bản ĐÚNG (Dân số) → chốt ĐÚNG, KHÔNG fuzzy.
    _nrc = _source_map_one("Luật Dân số", [{"id":"danchu", "name":"VBHN_87-VPQH_2025_Luat_Dan_chu_co_so_HopNhat", "so_hieu":"87-VBHN-VPQH", "loai":"VBHN", "cat":"36", "nlm_source_id":"n", "corpus":"true"}, {"id":"danso", "name":"Luat_113-2025-QH15_Dan_so", "so_hieu":"113-2025-QH15", "cat":"08", "nlm_source_id":"n", "corpus":"true"}])
    cases.append(("name_rank_no_fuzzy_collision", (_nrc["canonical"] or {}).get("drive_id") == "danso" and _name_strong_match("Luật Dân số", "Luat_113-2025-QH15_Dan_so") and not _name_strong_match("Luật Dân số", "VBHN_87-VPQH_2025_Luat_Dan_chu_co_so_HopNhat")))
    # name_rank gate: khi MỌI hit chỉ khớp-MỜ (không bản nào strong, vd 'Việc làm'↔'đi làm việc ở nước ngoài') → canonical None + LOW_CONFIDENCE.
    _lc = _source_map_one("Việc làm", [{"id":"a", "name":"VBHN_8-VBHN-BNV_NLD_di_lam_viec_o_nuoc_ngoai", "so_hieu":"8-VBHN-BNV", "loai":"VBHN", "cat":"20", "nlm_source_id":"n", "corpus":"true"}, {"id":"b", "name":"Luat_giai_quyet_viec_va_lam_them", "so_hieu":"99-2020-QH14", "cat":"20", "nlm_source_id":"n", "corpus":"true"}])
    cases.append(("name_rank_low_confidence_gate", _lc["canonical"] is None and any("LOW_CONFIDENCE_NAME_MATCH" in w for w in _lc["warnings"])))
    cases.append(("name_phrase_no_single_token_matchall", (not _name_phrase_match("Dân số", "VBHN_87-VPQH_2025_Luat_Dan_chu_co_so_HopNhat")) and _name_phrase_match("Dân số", "Luat_113-2025-QH15_Dan_so")))
    _clk = _cluster_lookup("pháp luật về bảo hiểm y tế")["matches"]
    cases.append(("cluster_bhyt_anchors_y_te_not_lao_dong", len(_clk) >= 1 and all(m["cluster"] == "y_te_kham_chua_benh" for m in _clk) and not any(m["cluster"] == "lao_dong_xa_hoi" for m in _clk)))
    cases.append(("vbhn_verify_official_header_not_assembled", "HEADER_NOT_CLEAR_VBHN" not in _vbhn_verify_flags("VĂN PHÒNG QUỐC HỘI\nSố: 14/VBHN-VPQH\nHà Nội, ngày 16 tháng 9 năm 2024\nLUẬT AN TOÀN, VỆ SINH LAO ĐỘNG\nbệnh nghề nghiệp không đúng quy định của pháp luật") and "ASSEMBLED_VBHN_NOT_ALLOWED_AS_CANONICAL" not in _vbhn_official_flags("bệnh nghề nghiệp không đúng quy định của pháp luật") and "ASSEMBLED_VBHN_NOT_ALLOWED_AS_CANONICAL" in _vbhn_official_flags("nội dung", "VBHN_14_zzz_assembled_taluat")))
    cases.append(("corpus_not_nlm_suppress_removed", ("CORPUS_TRUE_NOT_ON_NLM" not in _title_flags({"name":"Luat_84-2015-QH13_ATVSLD", "so_hieu":"84/2015/QH13", "cat":"05", "corpus":"true", "nlm_status":"removed_superseded_by_vbhn"})) and ("CORPUS_TRUE_NOT_ON_NLM" in _title_flags({"name":"Luat_84-2015-QH13_ATVSLD", "so_hieu":"84/2015/QH13", "cat":"05", "corpus":"true"}))))
    cases.append(("footnote_multi_diem_target", _parse_footnote_def("3", "Điểm c và điểm d khoản 2 Điều 30 được sửa đổi, bổ sung theo khoản 5 Điều 1 của Luật số 41/2024/QH15")["diem"] == "c và d" and _parse_footnote_def("4", "Điểm a khoản 1 Điều 5 được bổ sung theo khoản 1 Điều 1 của Luật số 41/2024/QH15")["diem"] == "a"))
    cases.append(("strip_font_runs", _strip_font_runs("Arial\nĐiều 1. Phạm vi\nTimes New Roman\nNội dung") == "Điều 1. Phạm vi\nNội dung" and _strip_font_runs("Theo Times báo\nArial Group") == "Theo Times báo\nArial Group"))
    cases.append(("scan_inline_amendments", _scan_inline_amendments("Điều 53. Sửa đổi, bổ sung một số điều của Luật Phí và lệ phí số 97/2015/QH13") == ["97-2015-QH13"] and _scan_inline_amendments("Luật số 97/2015/QH13 đã được sửa đổi, bổ sung một số điều theo Luật số 09/2017/QH14") == []))
    cases.append(("vbhn_disc_excludes_atvsld_from_bhyt", _subject_score({"name":"VBHN_14-VBHN-VPQH_2024_Luat_ATVSLD_HopNhat", "cat":"20_Lao_dong", "tukhoa":"an toàn vệ sinh lao động; bệnh nghề nghiệp"}, "bảo hiểm y tế") == 0))
    cases.append(("relcheck_skip_quarantined_backfill", not any(m.get("action") == "BACKFILL_GOC_ON_AMENDMENT" and m.get("drive_id") == "DUP1" for m in _relation_audit([{"name":"100_2025_QH15.docx", "sohieu":"100/2025/QH15", "cat":"01", "corpus":"true", "drive_id":"BASE1"}, {"name":"150_2026_QH15_TRUNG.docx", "sohieu":"150/2026/QH15", "cat":"_ZZZ_QUARANTINE_taluat", "corpus":"false", "drive_id":"DUP1"}], base="100/2025/QH15", amendments=["150/2026/QH15"])["missing_links"])))
    _gap = _source_map_one("114/2025/QH15", [{"id":"pb114", "name":"Luat_114-2025-QH15_Phong_benh", "so_hieu":"114/2025/QH15", "cat":"45", "corpus":"true"}])
    cases.append(("source_map_flags_corpus_true_not_on_nlm", _gap.get("nlm_gap_count") == 1 and "CORPUS_TRUE_NOT_ON_NLM" in ((_gap["canonical"] or {}).get("flags") or [])))
    # v1.22.65 (batch-2 run-log fixes — workflow điều tra+verify đối kháng trên copy cô lập)
    cases.append(("srcmap_doctype_tier_prefers_luat", _query_doctype_tier("Luật Đầu tư") == 5 and _query_doctype_tier("Việc làm") == 0 and (_source_map_one("Luật Đầu tư", [{"id":"nd", "name":"VBHN_73-82-ND-CP_Quan_ly_dau_tu", "so_hieu":"73-82-ND-CP", "loai":"VBHN", "cat":"34", "nlm_source_id":"n", "corpus":"true"}, {"id":"luat", "name":"VBHN_03-VBHN-VPQH_Luat_Dau_tu_cong", "so_hieu":"03-VBHN-VPQH", "loai":"VBHN", "cat":"34", "nlm_source_id":"n", "corpus":"true"}])["canonical"] or {}).get("drive_id") == "luat"))
    cases.append(("issue_year_not_from_goc_token", _entry_issue_year({"name":"VBHN_123-VBHN-VPQH_Luat_PPP_goc_64-2020-QH14", "so_hieu":"123-VBHN-VPQH", "loai":"Văn bản hợp nhất", "goc":"64-2020-QH14;90-2025-QH15", "issue_year":"2020"}) != 2020 and _strip_goc_token("VBHN_123_Luat_PPP_goc_64-2020-QH14") == "VBHN_123_Luat_PPP"))
    cases.append(("dedup_vbhn_first_base_goc", (lambda vb, gc: _is_vbhn_entry(vb) and _vbhn_base_key(vb) == _sohieu_key_entry(gc) and bool({_sohieu_key_entry(gc)} & _goc_keys(vb)) and not _is_vbhn_entry(gc))({"name":"VBHN_123-VBHN-VPQH_Luat_PPP_goc_64-2020-QH14", "sohieu":"123-VBHN-VPQH", "goc":"64-2020-QH14"}, {"name":"Luat_64-2020-QH14_Dau_tu_PPP", "sohieu":"64-2020-QH14"})))
    _ftn = resolve_footnote_amendments("Điều 1. Test\n1. Khoản này [1] giữ nguyên.\n2. Khoản này dẫn chiếu Luật số 23/2008/QH12 [2].\n\n[1] Khoản 1 Điều 1 được sửa đổi, bổ sung theo khoản 1 Điều 5 của Luật số 90/2025/QH15.\n[2] Cụm từ này được hiểu theo quy định tại Luật số 23/2008/QH12.")
    cases.append(("relcheck_footnote_only_no_citation_fp", ("90-2025-QH15" in _ftn["mapped_sohieu"]) and ("23-2008-QH12" not in _ftn["mapped_sohieu"]) and ("23-2008-QH12" in _ftn["footnote_sohieu"])))
    cases.append(("corpus_nlm_sidecar_fp", _dup_of_live_sibling({"name":"12_2022_ND-CP_m_479312", "corpus":"true"}, [{"name":"ND_12-2022-ND-CP_xu_phat", "so_hieu":"12-2022-ND-CP", "nlm_source_id":"x", "nlm_status":"pushed"}, {"name":"12_2022_ND-CP_m_479312", "corpus":"true"}]) is True and _dup_of_live_sibling({"name":"Luat_60-2024-QH15_Phong_benh.doc", "corpus":"true"}, [{"name":"Luat_60-2024-QH15_Du_lieu", "so_hieu":"60-2024-QH15", "nlm_source_id":"y", "nlm_status":"pushed"}, {"name":"Luat_60-2024-QH15_Phong_benh.doc", "corpus":"true"}]) is False))
    _rj = _relation_audit([{"name":"100_2025_QH15.docx", "sohieu":"100/2025/QH15", "cat":"01", "corpus":"true", "drive_id":"B1"}], base="100/2025/QH15", amendments=[])
    cases.append(("relcheck_subject_filtered_is_count", isinstance(_rj.get("amendment_candidates_subject_filtered_count"), int) and "amendment_candidates_subject_filtered" not in _rj and isinstance(_rj["amendment_candidates"], list)))
    cases.append(("vbhn_verdict_fields", _vbhn_verdict([]) == ("OFFICIAL_OK", True, False) and _vbhn_verdict(["OFFICIAL_SOURCE_NOT_CONFIRMED"]) == ("FAIL", False, False) and _vbhn_verdict(["ASSEMBLED_VBHN_NOT_ALLOWED_AS_CANONICAL"]) == ("FAIL", False, True) and _vbhn_verdict([], True) == ("PROVISIONAL", False, True)))
    cases.append(("xref_sohieu_typo_agency", _classify_ref({"raw":"k", "name_phrase":"Bảo hiểm xã hội", "sohieu":"41-2024-QH14", "loai":"Luật"}, [{"so_hieu":"41/2024/QH15", "name":"Luat Bao hiem xa hoi", "tukhoa":"bhxh", "cat":"02"}])["flag"] == "DOC_TEXT_SOHIEU_TYPO"))
    cases.append(("cluster_ppp_dau_tu", any(m["cluster"] == "dau_tu_PPP" for m in _cluster_lookup("đối tác công tư")["matches"])))
    # v1.22.67 (rà 59 luật — A2 subject sạch / A6 keyring noise / không xung đột _HL_DATE_RE thân-văn-bản)
    cases.append(("clean_subject_strips_hl_suadoi", ("hl2026" not in _clean_subject_text("thu do hl2026 07 01")) and _clean_subject_text("suadoi quang cao") == "quang cao" and _clean_subject_text("kham chua benh") == "kham chua benh"))
    # v1.31.0 P0-1: derive_subject nay GIỮ hoa/thường (pretty-tail — query web tốt hơn) → so case-insensitive.
    cases.append(("derive_subject_no_hl_garbage", "hl" not in _derive_subject_from_entries([{"name":"Luat_02-2026-QH16_Thu_do_HL2026-07-01"}]).lower() and _derive_subject_from_entries([{"name":"Luat_115-2023-QH15_Kham_chua_benh"}]).lower() == "kham chua benh"))
    cases.append(("hl_date_body_regex_intact", "hiệu lực" in _HL_DATE_RE.pattern and _HL_SUFFIX_RE.pattern.startswith(r"\bhl")))
    cases.append(("strip_keyring_noise", _imp("tl_gws")._strip_keyring_noise("Using keyring backend: keyring\n{\"ok\":true}") == "{\"ok\":true}" and _imp("tl_gws")._strip_keyring_noise("data\nok") == "data\nok"))
    # R1 (nhóm-D READ gws-primary): parse Sheets values → rows PARITY GAS rowsToObjs_ (header-zip, ép str, bù ô đuôi
    # rỗng, đủ mọi cột schema, BỎ dòng drive_id rỗng). Đọc GHI vẫn GAS. Test PURE (không chạm gws/mạng).
    _r1rows = _imp("tl_gws")._parse_sheet_values_to_rows(
        [["drive_id", "sohieu", "corpus"], ["d1", "80/2025/QH15", "true"], ["", "99/2025/QH15", "true"], ["d3"]],
        ["drive_id", "sohieu", "corpus", "note"])
    cases.append(("r1_sheet_parse_parity",
                  len(_r1rows) == 2                                   # dòng drive_id rỗng (d="") bị BỎ
                  and _r1rows[0]["drive_id"] == "d1" and _r1rows[0]["sohieu"] == "80/2025/QH15"
                  and _r1rows[0]["corpus"] == "true"                  # giữ RAW (không norm ở parser)
                  and _r1rows[1]["drive_id"] == "d3" and _r1rows[1]["sohieu"] == "" and _r1rows[1]["corpus"] == ""  # ô đuôi thiếu → ''
                  and _r1rows[0]["note"] == "" and "note" in _r1rows[1]))   # cột schema thiếu trong sheet → bù ''
    cases.append(("r1_sheet_parse_empty", _imp("tl_gws")._parse_sheet_values_to_rows([], ["drive_id"]) == []
                  and _imp("tl_gws")._parse_sheet_values_to_rows([["drive_id"]], ["drive_id"]) == []))
    # PARITY GAS rowsToObjs_: khóa THEO VỊ TRÍ theo `cols` (KHÔNG theo tên header) → header lệch tên vẫn map đúng
    # schema (giống GAS map positional REG_COLS_). Chống mất-parity khi header Sheet bị sửa cỡ chữ/thứ tự.
    _r1pos = _imp("tl_gws")._parse_sheet_values_to_rows([["HEADER_X", "header_y"], ["d9", "80/2025/QH15"]],
                                                        ["drive_id", "sohieu"])
    cases.append(("r1_sheet_parse_positional_by_cols",
                  len(_r1pos) == 1 and _r1pos[0]["drive_id"] == "d9" and _r1pos[0]["sohieu"] == "80/2025/QH15"
                  and "HEADER_X" not in _r1pos[0]))   # KHÔNG dùng tên header thực làm khóa
    # v1.22.68 (rà 133+81 luật — raw-entry precondition + footnote dedup)
    cases.append(("raw_no_gdoc_detect", _is_raw_no_gdoc_name("Luat Viec lam.docx") and _is_raw_no_gdoc_name("x.pdf") and _is_raw_no_gdoc_name("y.HTML") and (not _is_raw_no_gdoc_name("19/VBHN-VPQH")) and (not _is_raw_no_gdoc_name("VBHN_19_Bao_hiem")) and _raw_no_gdoc("", {"ok": False, "error": "Export only supports Docs Editors files."}) and _raw_no_gdoc("a.pdf")))
    _fdd = resolve_footnote_amendments("Điều 73. Test\n1. Khoản này[1][2][3] quy định.\n\n[1] Khoản 1 Điều 73 được sửa đổi theo khoản 1 Điều 5 của Luật số 113/2025/QH15.\n[2] Khoản 1 Điều 73 được sửa đổi theo khoản 1 Điều 5 của Luật số 113/2025/QH15.\n[3] Khoản 1 Điều 73 được sửa đổi theo khoản 1 Điều 5 của Luật số 113/2025/QH15.", today="2025-01-01")
    cases.append(("footnote_dieu_level_dedup", len(_fdd["dieu_level_amendment_map"]) == 1 and _fdd.get("footnote_raw_count") == 3 and len(_fdd["footnote_defs"]) == 3))
    _body_eff = resolve_footnote_amendments("Điều 30. Hiệu lực thi hành\n1. Luật này có hiệu lực thi hành từ ngày 01 tháng 7 năm 2026.\n2. Điểm c và điểm d khoản 1 Điều 14 của Luật này có hiệu lực từ ngày 01 tháng 01 năm 2027.", today="2026-06-28")
    cases.append(("body_effective_dates_pending", _body_eff["body_pending_effect_count"] == 2 and _body_eff["pending_effect_count"] == 2))
    cases.append(("vbhn_year_from_name", _entry_issue_year({"name":"VBHN_14-VBHN-VPQH_2024_Luat_ATVSLD_HopNhat", "so_hieu":"14/VBHN-VPQH", "loai":"VBHN"}) == 2024))
    cases.append(("vbhn_short_sohieu_flag", "VBHN_SOHIEU_NORMALIZED_FROM_SHORT_VPQH" in _title_flags({"name":"VBHN_19-VPQH_2026_Luat_BHXH_HopNhat", "so_hieu":"19-VPQH", "loai":"VBHN", "cat":"20"})))
    cases.append(("ministerial_vbhn_requires_year", {"VBHN_MINISTRY_SCOPE", "VBHN_MINISTRY_MISSING_YEAR"} <= set(_title_flags({"name":"VBHN_09-VBHN-BYT_Thong_tu_HopNhat", "so_hieu":"09/VBHN-BYT", "loai":"VBHN", "cat":"20"}))))
    cases.append(("ministerial_vbhn_name_needs_year", "VBHN_MINISTRY_NAME_MISSING_YEAR" in _title_flags({"name":"VBHN_05-VBHN-BGDDT_Nghi_dinh_Hoc_phi_HopNhat", "so_hieu":"05/VBHN-BGDĐT", "loai":"VBHN", "cat":"20", "issue_year":"2024"})))
    min_recs = _vbhn_normalize_recommendations([{"id":"m05", "name":"VBHN_05-VBHN-BGDDT_Nghi_dinh_Hoc_phi_HopNhat", "so_hieu":"05/VBHN-BGDĐT", "loai":"VBHN", "cat":"20", "issue_year":"2024"}])
    cases.append(("ministerial_vbhn_normalize_pattern", bool(min_recs and any((a.get("suggested_pattern") or "").startswith("VBHN_<so>-VBHN-<co_quan>") for a in min_recs[0]["actions"]))))
    reuse_fx = [
        {"id":"a1", "name":"VBHN_14-VBHN-VPQH_2024_Luat_ATVSLD_HopNhat", "so_hieu":"14/VBHN-VPQH", "loai":"VBHN", "goc":"84/2015/QH13;41/2024/QH15", "cat":"20", "nlm_source_id":"n1"},
        {"id":"a2", "name":"VBHN_14-VBHN-VPQH_2024_Luat_ATVSLD_HopNhat", "so_hieu":"14/VBHN-VPQH", "loai":"VBHN", "goc":"84/2015/QH13;41/2024/QH15", "cat":"20", "nlm_source_id":"n2"},
        {"id":"b1", "name":"VBHN_14-VBHN-VPQH_2023_NLD_di_lam_viec_nuoc_ngoai_HopNhat", "so_hieu":"14/VBHN-VPQH", "loai":"VBHN", "goc":"69/2020/QH14", "cat":"20", "nlm_source_id":"n3"},
    ]
    reuse_clusters = _reconcile_clusters(reuse_fx)
    reuse_q = [(_summ_entry(e) or {}).get("drive_id") for c in reuse_clusters for e in c.get("quarantine") or []]
    cases.append(("hygiene_vbhn_reuse_not_quarantine_other_subject", "b1" not in reuse_q and "a2" in reuse_q))
    ghost = {"id":"ghost", "name":"", "so_hieu":"", "cat":"", "nlm_source_id":"src"}
    real = {"id":"real74", "name":"Luat_74-2025-QH15_Viec_lam", "so_hieu":"74/2025/QH15", "cat":"20"}
    cases.append(("nlm_ghost_score_sink", _entry_score(ghost) < _entry_score(real) and "NLM_GHOST_SOURCE" in _title_flags(ghost)))
    cases.append(("nlm_status_mismatch_flag", "NLM_STATUS_MISMATCH" in _title_flags({"id":"nlm_added", "name":"Luat_143-2025-QH15_Dau_tu", "so_hieu":"143/2025/QH15", "cat":"34", "nlm_source_id":"src", "nlm_status":"added"})))
    ok_vbhn = {"id":"v40", "name":"VBHN_40-VBHN-VPQH_2026_Luat_BHYT_HopNhat", "so_hieu":"40-VBHN-VPQH", "loai":"VBHN", "cat":"20"}
    cases.append(("vbhn_reuse_warning_suppressed_when_metadata_ok", not any("VBHN_NUMBER_REUSE_RISK" in w for w in _source_map_one("40/VBHN-VPQH", [ok_vbhn])["warnings"])))
    cases.append(("empty_name_not_match_any_query", not _cluster_matches({"entries": [ghost]}, "14/VBHN-VPQH") and (_source_map_one("bảo hiểm y tế", [ghost] + fx)["canonical"] or {}).get("drive_id") != "ghost"))
    norm_fx = [{"id":"v40", "name":"VBHN_40-VPQH_Luat_BHYT_HopNhat", "so_hieu":"40-VPQH", "loai":"VBHN", "cat":"20", "nlm_source_id":"n"}]
    norm_recs = _vbhn_normalize_recommendations(norm_fx)
    cases.append(("vbhn_normalize_recommends_backfill", norm_recs and any(a.get("action") == "BACKFILL_SOHIEU_CANONICAL_VBHN" for a in norm_recs[0].get("actions", []))))
    sidecar_fx = [
        {"id":"gdoc", "name":"VBHN_40-VBHN-VPQH_2026_Luat_BHYT_HopNhat", "so_hieu":"40/VBHN-VPQH", "loai":"VBHN", "cat":"20", "nlm_source_id":"n"},
        {"id":"docx", "name":"VBHN_40-VBHN-VPQH_2026_Luat_BHYT_HopNhat.docx", "so_hieu":"40/VBHN-VPQH", "loai":"VBHN", "cat":"20"},
    ]
    side_groups = _hygiene_groups(sidecar_fx)
    cases.append(("sidecar_source_file_not_orphan", len(side_groups["orphans"]) == 0 and len(side_groups["sidecar_source_files"]) == 1))
    cases.append(("duplicate_identity_groups_reported", len(side_groups["duplicate_identity_groups"]) >= 1))
    omni_wrong = {"id":"wrong57", "name":"Luat_57-2024-QH15_Bao_hiem_y_te", "so_hieu":"57/2024/QH15", "cat":"34", "title_vn":"Luật sửa đổi, bổ sung một số điều của Luật Quy hoạch, Luật Đầu tư, Luật Đầu tư theo phương thức đối tác công tư và Luật Đấu thầu", "goc":"15/2017/QH14;39/2019/QH14;64/2020/QH14"}
    cases.append(("hygiene_query_filters_omnibus_wrong_title", not _cluster_matches({"entries":[omni_wrong], "canonical":omni_wrong}, "bảo hiểm y tế") and _cluster_matches({"entries":[omni_wrong], "canonical":omni_wrong}, "57/2024/QH15")))
    null_clusters = _reconcile_clusters([{"id":"orphan30", "name":"30_2020_TT_BYT_12345", "cat":"", "drive_id":"orphan30"}])
    sel, skipped = _select_hygiene_clusters(null_clusters, "30/2020/TT-BYT")
    cases.append(("hygiene_plan_skips_null_canonical", not sel and skipped and skipped[0].get("skip_reason") == "MISSING_CANONICAL_REVIEW_ONLY"))
    cases.append(("nlm_notebook_missing_flag", "NLM_NOTEBOOK_ID_MISSING" in _title_flags({"id":"v40", "name":"VBHN_40-VBHN-VPQH_2026_Luat_BHYT_HopNhat", "so_hieu":"40/VBHN-VPQH", "loai":"VBHN", "cat":"20", "nlm_source_id":"src", "nlm_status":"pushed"})))
    cases.append(("reg_query_row_live_nlm_fields", (lambda r: r["on_nlm"] is False and r["nlm_source_id"] == "src" and r["nlm_notebook_id"] == "")(_reg_query_row({"id":"v40", "name":"VBHN_40", "so_hieu":"40/VBHN-VPQH", "cat":"20", "nlm_source_id":"src", "nlm_status":"removed_from_drive"}))))
    cases.append(("vbhn_check_queries", any("hợp nhất" in q for q in _qt5_queries("an toàn vệ sinh lao động", "84/2015/QH13", "2024"))))
    cases.append(("vbhn_check_queries_tvpl", any("thuvienphapluat.vn" in q.lower() or "Thư viện Pháp luật" in q for q in _qt5_queries("thi đua khen thưởng", "06/2022/QH15", ""))))
    cases.append(("vbhn_check_queries_simple_recall", any(_strip_accents(q).lower() == "luat thi dua khen thuong hop nhat" for q in _qt5_queries("thi đua khen thưởng", "06/2022/QH15", ""))))
    cases.append(("amendment_like_english_marker", _is_amendment_like({"name":"Law_06-2026-QH16_Amendment_Thi_dua_Khen_thuong", "loai":"Luật"})))
    rel_fx = [
        {"id":"tdkt2022", "name":"Luat_06-2022-QH15_Thi_dua_Khen_thuong", "so_hieu":"06/2022/QH15", "cat":"29", "nlm_source_id":"n1"},
        {"id":"tdkt2026", "name":"Luat_06-2026-QH16_SuaDoi_Thi_dua_Khen_thuong", "so_hieu":"06/2026/QH16", "cat":"29", "nlm_source_id":"n2"},
    ]
    rel = _relation_audit(rel_fx, base="06/2022/QH15", subject="thi đua khen thưởng", amendments=["06/2026/QH16"])
    cases.append(("relation_check_finds_unlinked_amendment", (rel["amendment_candidates"] or [{}])[0].get("entry", {}).get("drive_id") == "tdkt2026" and len(rel["missing_links"]) >= 2))
    sm_tdk = _source_map_one("06/2022/QH15", rel_fx)
    # v1.29.6 (P0b — log 118 Luật): candidate NON-LINKED conf=low nay là WEAK → REVIEW (cờ LOW_CONFIDENCE),
    # KHÔNG còn PAUSE (trước 15/118 Luật dừng giả vì chính pattern này). Vẫn phải LIỆT KÊ đủ trong unlinked list.
    cases.append(("source_map_unlinked_amendment_detected",
                  bool(sm_tdk.get("unlinked_amendment_candidates"))
                  and any("AMENDMENT_CANDIDATE_LOW_CONFIDENCE" in w for w in sm_tdk.get("warnings", []))
                  and not any("PAUSE_AND_ASK_USER" in w for w in sm_tdk.get("warnings", []))
                  and sm_tdk.get("verdict") == "REVIEW"))
    # v1.29.6 P0b: candidate LINKED (registry goc trỏ đúng base) = STRONG → vẫn PAUSE như cũ (không mất an toàn).
    rel_fx_linked = [rel_fx[0], dict(rel_fx[1], goc="06-2022-QH15")]
    sm_tdk_l = _source_map_one("06/2022/QH15", rel_fx_linked)
    cases.append(("source_map_linked_amendment_still_pauses",
                  sm_tdk_l.get("action_required") == "PAUSE_AND_ASK_USER"
                  and any(c.get("strong") for c in sm_tdk_l.get("amendment_candidates") or [])))
    # v1.29.6 P0a: corpus=false / cat Van_ban_thuong / tên phi-quy-phạm (lịch trình/thẩm tra/YK_) KHÔNG là candidate.
    _p0a_ents = [rel_fx[0],
                 dict(rel_fx[1], corpus="false"),
                 {"id": "hr1", "drive_id": "hr1", "name": "YK_tham_gia_du_thao_SDBS_QCLV_mau", "cat": "Van_ban_thuong",
                  "so_hieu": "", "corpus": "true"},
                 {"id": "lt1", "drive_id": "lt1", "name": "Lịch trình thẩm tra dự án Luật sửa đổi Luật Thi đua",
                  "so_hieu": "", "cat": "29", "corpus": "true"}]
    _p0a_c = _find_amendment_candidates("06-2022-QH15", [_p0a_ents[0]], [], _p0a_ents)
    cases.append(("amendment_filter_corpus_false_thuong_nonnormative", _p0a_c == []))
    # v1.29.6 P0d: omnibus 'sua_doi_N_luat' non-linked = weak (omnibus=True, strong=False); linked qua goc → strong.
    # Fixture đặt subject-tokens TRONG TÊN để candidate THẬT SỰ vào list (probe: tukhoa không đủ vào overlap-gate)
    # — assert đòi len>=1, KHÔNG cho vacuous-pass.
    _omn = {"id": "om1", "drive_id": "om1", "name": "Luat_90-2025-QH15_sua_doi_8_luat_Thi_dua_Khen_thuong_va_khac",
            "so_hieu": "90/2025/QH15", "cat": "29", "corpus": "true"}
    _omn_c = _find_amendment_candidates("06-2022-QH15", [rel_fx[0]], [], [rel_fx[0], _omn])
    cases.append(("amendment_omnibus_nonlinked_weak",
                  len(_omn_c) >= 1 and all((c.get("_amendment_omnibus") and not c.get("_amendment_strong")) for c in _omn_c)))
    # ═══ v1.32.0 (log rà 77 Luật — 3 defect lớp amendment-gate) — r11_* ═══
    # (A1) canonical CONFIRMED → suppress TOÀN BỘ escalation (kể cả strong-linked), ar=None, verdict OK.
    _sm11a = _source_map_one("06/2022/QH15", [dict(rel_fx[0], verified="yes"), rel_fx[1]])
    _sm11b = _source_map_one("06/2022/QH15", [dict(rel_fx[0], verified="yes"), dict(rel_fx[1], goc="06-2022-QH15")])
    cases.append(("r11_confirmed_suppresses_amendment_gate",
                  any(w.startswith("AMENDMENT_GATE_SUPPRESSED_CONFIRMED") for w in _sm11a["warnings"])
                  and not any(w.startswith(("UNLINKED_AMENDMENT_CANDIDATE", "VBHN_RECHECK_REQUIRED",
                                            "AMENDMENT_CANDIDATE_LOW_CONFIDENCE")) for w in _sm11a["warnings"])
                  and _sm11a.get("action_required") is None and _sm11a["verdict"] == "OK"
                  and _sm11b.get("action_required") is None and _sm11b["verdict"] == "OK"
                  and not any(w.startswith("PAUSE_AND_ASK_USER") for w in _sm11b["warnings"])))
    # (A2a) canonical CHÍNH LÀ VBHN + candidate nằm trong chuỗi goc CỦA NÓ → consolidated, sạch cờ mồ-côi (ca 115-2026).
    _vb115 = {"id": "v115", "drive_id": "v115", "name": "VBHN_115-2026-VBHN-VPQH_2026_Luat_Thi_dua_Khen_thuong_HopNhat",
              "so_hieu": "115-2026-VBHN-VPQH", "loai": "VBHN", "cat": "29", "goc": "06-2026-QH16;06-2022-QH15",
              "nlm_source_id": "nv"}
    _sm11c = _source_map_one("115-2026-VBHN-VPQH", [_vb115, rel_fx[1], rel_fx[0]])
    cases.append(("r11_vbhn_canonical_consolidates_own_goc",
                  [c.get("drive_id") for c in _sm11c["consolidated_amendments"]] == ["tdkt2026"]
                  and not any(w.startswith(("UNLINKED_AMENDMENT_CANDIDATE", "VBHN_RECHECK_REQUIRED"))
                              for w in _sm11c["warnings"])
                  and _sm11c["verdict"] == "OK"))
    # (A2b) canonical VBHN + candidate NGOÀI goc → VBHN_GOC_VERIFY (không 'tìm VBHN cho VBHN'); REVIEW giữ (đúng —
    # VBHN có amendment chưa hợp nhất là rủi ro lỗi thời thật).
    _sm11d = _source_map_one("115-2026-VBHN-VPQH", [dict(_vb115, goc="01-2020-QH14"), rel_fx[1], rel_fx[0]])
    cases.append(("r11_vbhn_canonical_goc_verify_not_recheck",
                  any(w.startswith("VBHN_GOC_VERIFY") for w in _sm11d["warnings"])
                  and not any(w.startswith("VBHN_RECHECK_REQUIRED") for w in _sm11d["warnings"])))
    # (A3) canonical OMNIBUS → OMNIBUS_AMENDS_OTHER, KHÔNG UNLINKED/LOW_CONF/RECHECK → hết REVIEW lặp.
    _omn11 = {"id": "om1", "drive_id": "om1", "name": "Luat_90-2025-QH15_sua_doi_8_luat_Thi_dua_Khen_thuong_va_khac",
              "so_hieu": "90/2025/QH15", "cat": "29", "corpus": "true", "nlm_source_id": "no1"}
    _cand11 = {"id": "c2", "drive_id": "c2", "name": "Luat_99-2026-QH16_SuaDoi_Thi_dua_Khen_thuong",
               "so_hieu": "99/2026/QH16", "cat": "29"}
    _sm11e = _source_map_one("90/2025/QH15", [_omn11, _cand11])
    cases.append(("r11_omnibus_canonical_amends_other",
                  _is_omnibus_entry(_omn11)
                  and any(w.startswith("OMNIBUS_AMENDS_OTHER") for w in _sm11e["warnings"])
                  and not any(w.startswith(("UNLINKED_AMENDMENT_CANDIDATE", "VBHN_RECHECK_REQUIRED",
                                            "AMENDMENT_CANDIDATE_LOW_CONFIDENCE")) for w in _sm11e["warnings"])
                  and _sm11e["verdict"] == "OK"))
    cases.append(("r11_omnibus_detector",
                  _is_omnibus_entry({"name": "Luat_57-2024-QH15_SuaDoi_QuyHoach_DauTu", "cat": "46"})
                  and not _is_omnibus_entry(rel_fx[0])
                  and not _is_omnibus_entry(_vb115)))
    # (A4) enum Điều ước quốc tế/Công ước — hết nonmappable/loai_noncanonical GIẢ cho công ước ILO.
    _t11 = {"drive_id": "cu1", "name": "CU_ILO-105_Xoa_bo_lao_dong_cuong_buc", "loai": "Điều ước quốc tế"}
    _s11, _u11, _n11 = _backfill_loai_candidates([_t11], normalize=True)
    cases.append(("r11_treaty_loai_enum",
                  _normalize_loai("dieu uoc quoc te") == "Điều ước quốc tế"
                  and "Điều ước quốc tế" in _LOAI_CANON_VALUES and "Công ước" in _LOAI_CANON_VALUES
                  and _s11 == [] and _n11 == []))
    # (B3) RAW_NAME_NOT_NLM là SIDECAR cạnh GDoc → không vào risky (cờ gốc _title_flags vẫn có — chỉ suppress hiển thị).
    _gd11 = {"id": "g1", "drive_id": "g1", "name": "Luat_60_2024_QH15_Du_lieu", "so_hieu": "60/2024/QH15",
             "cat": "03", "nlm_source_id": "s1", "corpus": "true"}
    _raw11 = {"id": "r1", "drive_id": "r1", "name": "Luat_60_2024_QH15_Du_lieu.docx", "so_hieu": "", "cat": "03",
              "mime": "application/vnd.openxmlformats"}
    _sm11f = _source_map_one("60/2024/QH15", [_gd11, _raw11])
    cases.append(("r11_rawname_sidecar_not_risky",
                  "RAW_NAME_NOT_NLM" in _title_flags(_raw11)
                  and not any("RAW_NAME_NOT_NLM" in (r.get("flags") or []) for r in _sm11f["risky_candidates"])))
    # ═══ v1.32.1 (log rà 119 — read-path chết + false-green) — r12_* ═══
    # _read_doc_text_via_nlm: gate offline (không nlm_source_id / nguồn removed → '' KHÔNG network).
    cases.append(("r12_nlm_read_fallback_gates",
                  _read_doc_text_via_nlm({}) == ""
                  and _read_doc_text_via_nlm({"nlm_source_id": "s1", "nlm_status": "removed_from_drive"}) == ""
                  and _read_doc_text_via_nlm({"name": "x", "nlm_source_id": ""}) == ""))
    # v1.32.2 (log rà 69): omnibus theo ĐỀ-TÀI-TRONG-TÊN dạng nén (57-2024 registry chưa backfill goc → nhánh
    # ≥2-ref câm; tên SuaDoi_QuyHoach_DauTu strip xong DÍNH LIỀN nên phải so compact); sửa-1-luật KHÔNG omnibus.
    cases.append(("r12_omnibus_name_topics_compact",
                  _is_omnibus_entry({"name": "Luat_57-2024-QH15_SuaDoi_QuyHoach_DauTu_PPP_DauThau", "cat": "34"})
                  and not _is_omnibus_entry({"name": "Luat_75-2025-QH15_SuaDoi_Quang_cao", "cat": "35"})
                  and not _is_omnibus_entry({"name": "Luat_68-2025-QH15_Quan_ly_dau_tu_von_nha_nuoc_tai_DN", "cat": "26"})))
    # v1.32.2 (ca 115-2026-VBHN loai='Luật'): conflict-mode CHỈ khi tên VBHN_ + sohieu -VBHN- đồng thuận.
    _cfl = {"drive_id": "v115", "name": "VBHN_115-VBHN-VPQH_2026_Thi_dua", "so_hieu": "115-2026-VBHN-VPQH", "loai": "Luật"}
    _s12a, _, _n12a = _backfill_loai_candidates([_cfl], normalize=True)
    _s12b, _, _ = _backfill_loai_candidates([dict(_cfl, loai="Văn bản hợp nhất")], normalize=True)
    _s12c, _, _ = _backfill_loai_candidates([dict(_cfl, name="Luat_115_Thi_dua", so_hieu="115/2026/QH16")], normalize=True)
    cases.append(("r12_loai_conflict_vbhn_corroborated",
                  len(_s12a) == 1 and _s12a[0]["mode"] == "conflict" and _s12a[0]["loai"] == "Văn bản hợp nhất"
                  and _s12a[0]["loai_raw"] == "Luật" and _s12b == [] and _s12c == [] and _n12a == []))
    # v1.29.6 P0c: VBHN year-fallback — VBHN key 2026 > luật-sửa key 2025 → covered (year-only); CÙNG năm → KHÔNG.
    _vbhn26 = {"id": "v26", "drive_id": "v26", "name": "VBHN_25-2026-VBHN-VPQH_2026_Luat_Gia", "so_hieu": "25-2026-VBHN-VPQH", "loai": "VBHN"}
    _am25 = {"id": "a25", "drive_id": "a25", "name": "Luat_90-2025-QH15_sua_doi_8_luat", "so_hieu": "90/2025/QH15"}
    _cv1, _lbl1, _ = _amendments_covered_by_vbhn_date(_vbhn26, [_am25])
    _am26 = {"id": "a26", "drive_id": "a26", "name": "Luat_99-2026-QH16_SuaDoi", "so_hieu": "99/2026/QH16"}
    _cv2, _, _ = _amendments_covered_by_vbhn_date(_vbhn26, [_am26])
    cases.append(("vbhn_date_year_fallback", _cv1 is True and "year-only" in str(_lbl1) and _cv2 is False))
    # v1.29.6 P2.2: VBHN sohieu-key ĐÃ CÓ NĂM (133-2025-VBHN-VPQH) → KHÔNG cờ MISSING_YEAR (hết reuse-risk oan).
    _vf_y = _vbhn_metadata_flags({"id": "x", "name": "VBHN_133-2025-VBHN-VPQH_Luat_Dat_dai", "so_hieu": "133-2025-VBHN-VPQH", "loai": "VBHN"}, "luat dat dai")
    _vf_n = _vbhn_metadata_flags({"id": "y", "name": "VBHN_14-VBHN-VPQH_Luat_X", "so_hieu": "14/VBHN-VPQH", "loai": "VBHN"}, "luat x")
    cases.append(("vbhn_flags_key_year_no_false_missing",
                  "VBHN_MISSING_YEAR_OR_DATE" not in _vf_y and "VBHN_NAME_MISSING_YEAR" not in _vf_y
                  and "VBHN_MISSING_YEAR_OR_DATE" in _vf_n))
    # v1.29.6 P2.3: cờ boolean nhận giá trị tường minh.
    cases.append(("optional_bool_flag", _optional_bool_flag("true") is True and _optional_bool_flag("False") is False))

    # ═══ v1.33.0 (log rà 69+15 Luật — CAT over-fire ~78% / BLDS name / reuse-risk / dup-real / breaker) — r13_* ═══
    # (F1a) CAT_LIKELY_WRONG chỉ suy từ TIÊU ĐỀ — thân văn bản nhắc 'điều ước'/'sửa đổi các luật' KHÔNG còn là
    # bằng chứng: BLHS (cur=16) không →23; VBHN Kế toán (cur=17) không →46.
    _hx13_blhs = ("QUỐC HỘI\n\nBỘ LUẬT\nHÌNH SỰ\n\nCăn cứ Hiến pháp\nĐiều 1. Nhiệm vụ\n"
                  "việc thực hiện điều ước quốc tế mà Việt Nam là thành viên; "
                  "sửa đổi, bổ sung một số điều của luật A, luật B và các luật khác.")
    _e13_blhs = {"drive_id": "d100", "name": "Luat_100-2015-QH13_Bo_Luat_Hinh_su", "so_hieu": "100/2015/QH13",
                 "loai": "Bộ luật", "cat": "16", "corpus": "true"}
    _hx13_vbhn = ("VĂN BẢN HỢP NHẤT\n\nLUẬT\nKẾ TOÁN\n\nhợp nhất các văn bản: "
                  "sửa đổi, bổ sung một số điều của các luật: luật X, luật Y, luật Z.")
    _e13_vbhn = {"drive_id": "d25", "name": "VBHN_25-2025-VBHN-VPQH_2025_Luat_Ke_toan",
                 "so_hieu": "25-2025-VBHN-VPQH", "loai": "VBHN", "cat": "17", "corpus": "true"}
    cases.append(("r13_cat_body_not_evidence",
                  _cat_likely_wrong_suggest(_e13_blhs, _hx13_blhs) is None
                  and _cat_likely_wrong_suggest(_e13_vbhn, _hx13_vbhn) is None))
    # (F1b) pin Quyết định 26/6: AI/CĐS đang cat 19 → KHÔNG đề xuất dời dù nội dung/alias nói gì.
    cases.append(("r13_cat_pin19_qd266",
                  _cat_likely_wrong_suggest({"drive_id": "d134", "name": "Luat_134-2025-QH15_Tri_tue_nhan_tao",
                                             "so_hieu": "134/2025/QH15", "loai": "Luật", "cat": "19",
                                             "corpus": "true"}, "LUẬT\nTRÍ TUỆ NHÂN TẠO\n\nĐiều 1. Phạm vi") is None
                  and _cat_likely_wrong_suggest({"drive_id": "d148", "name": "Luat_148-2025-QH15_Chuyen_doi_so",
                                                 "so_hieu": "148/2025/QH15", "loai": "Luật", "cat": "19",
                                                 "corpus": "true"}, "LUẬT\nCHUYỂN ĐỔI SỐ\n\nĐiều 1.") is None))
    # (F1c) tín hiệu THẬT giữ nguyên: 143-2025 'Đầu tư' ở cat 45 → đề xuất 34 (alias pháp điển đồng thuận).
    _p13_143 = _cat_likely_wrong_suggest({"drive_id": "d143", "name": "Luat_143-2025-QH15_Dau_tu",
                                          "so_hieu": "143/2025/QH15", "loai": "Luật", "cat": "45",
                                          "corpus": "true"}, "LUẬT\nĐẦU TƯ\n\nĐiều 1. Phạm vi điều chỉnh")
    cases.append(("r13_cat_true_positive_alias_agree",
                  _p13_143 is not None and _p13_143["suggested"] == "34"
                  and "alias" in str(_p13_143.get("evidence"))))
    # (F1d) omnibus tên NÉN (57-2024, title-block miss) → vẫn đề xuất 46; cùng entry dạng VBHN → im.
    _p13_57 = _cat_likely_wrong_suggest({"drive_id": "d57", "name": "Luat_57-2024-QH15_SuaDoi_QuyHoach_DauTu_PPP_DauThau",
                                         "so_hieu": "57/2024/QH15", "loai": "Luật", "cat": "34", "corpus": "true"}, "")
    _p13_57v = _cat_likely_wrong_suggest({"drive_id": "d57v", "name": "VBHN_131-2025-VBHN-VPQH_2025_Luat_Quy_hoach_HopNhat",
                                          "so_hieu": "131-2025-VBHN-VPQH", "loai": "VBHN", "cat": "43",
                                          "corpus": "true"},
                                         "VĂN BẢN HỢP NHẤT\n\nLUẬT\nQUY HOẠCH\n\nsửa đổi, bổ sung một số điều của "
                                         "các luật: luật A, luật B, luật C.")
    cases.append(("r13_cat_omnibus_46_vbhn_never_46",
                  _p13_57 is not None and _p13_57["suggested"] == "46" and _p13_57v is None))
    # (F2) tên BLDS_/BLHS_ = quy ước hợp lệ (viết tắt Bộ luật) — hết NAME_NONSTANDARD oan; tên hỏng thật vẫn bắt.
    cases.append(("r13_name_boluat_abbrev_ok",
                  _name_structural_issues("BLDS_91-2015-QH13_Bo_luat_Dan_su") == []
                  and not _name_looks_nonstandard("BLDS_91-2015-QH13_Bo_luat_Dan_su")
                  and "FILE_EXTENSION" in _name_structural_issues("luat-dau-thau-22-2023.html")
                  and _name_prefix_family(_NAME_TYPE_PREFIX_RE.match("BLDS_x")) == "Bo_luat"))
    # (F4) reuse-risk: GDoc năm-đủ + sidecar .docx cùng số = MỘT văn bản → KHÔNG VBHN_NUMBER_REUSE_RISK;
    # control: VBHN tên trơ thiếu năm (133-VPQH) VẪN cờ (tín hiệu thật giữ).
    _v13 = {"id": "v25", "drive_id": "v25", "name": "VBHN_25-2025-VBHN-VPQH_2025_Luat_Ke_toan",
            "so_hieu": "25-2025-VBHN-VPQH", "loai": "VBHN", "cat": "17", "corpus": "true", "nlm_source_id": "s25"}
    _v13raw = {"id": "v25r", "drive_id": "v25r", "name": "VBHN_25-2025-VBHN-VPQH_2025_Luat_Ke_toan.docx",
               "so_hieu": "25-2025-VBHN-VPQH", "cat": "17"}
    _sm13a = _source_map_one("25-2025-VBHN-VPQH", [_v13, _v13raw])
    _v13b = {"id": "v133", "drive_id": "v133", "name": "VBHN_133-VPQH_Luat_Dat_dai_HopNhat",
             "so_hieu": "133-2025-VBHN-VPQH", "loai": "VBHN", "cat": "18", "corpus": "true", "nlm_source_id": "s133"}
    _sm13b = _source_map_one("133-2025-VBHN-VPQH", [_v13b])
    cases.append(("r13_vbhn_reuse_sidecar_suppressed",
                  not any(w.startswith(("VBHN_NUMBER_REUSE_RISK", "TITLE_OR_REGISTRY_WARN"))
                          for w in _sm13a["warnings"])
                  and any(w.startswith("VBHN_NUMBER_REUSE_RISK") for w in _sm13b["warnings"])
                  and _vbhn_year_complete(_v13) and not _vbhn_year_complete(_v13b)))
    # (F5) dup by_sohieu: gốc+VBHN cùng số chỉ-mục = LÀNH; 2 bản corpus=true cùng phía = trùng THẬT; phụ lục tách = LÀNH.
    _d13_goc = {"id": "a", "drive_id": "a", "name": "Luat_52-2014-QH13_Hon_nhan_gia_dinh",
                "so_hieu": "52/2014/QH13", "corpus": "true", "cat": "20"}
    _d13_vbhn = {"id": "b", "drive_id": "b", "name": "VBHN_121-2025-VBHN-VPQH_2025_Hon_nhan_HopNhat",
                 "so_hieu": "52/2014/QH13", "loai": "VBHN", "corpus": "true", "cat": "20"}
    _d13_l1 = {"id": "c", "drive_id": "c", "name": "ND_30-2020-ND-CP_Cong_tac_van_thu",
               "so_hieu": "30/2020/NĐ-CP", "corpus": "true", "cat": "05"}
    _d13_l2 = {"id": "d", "drive_id": "d", "name": "ND_30-2020-ND-CP_Van_thu_ban_hai",
               "so_hieu": "30/2020/NĐ-CP", "corpus": "true", "cat": "05"}
    _d13_pl = {"id": "e", "drive_id": "e", "name": "ND_142-2026-ND-CP_Luat_TTNT_PhuLuc",
               "so_hieu": "142/2026/NĐ-CP", "corpus": "true", "cat": "19"}
    _d13_main = {"id": "f", "drive_id": "f", "name": "ND_142-2026-ND-CP_TTNT_Final",
                 "so_hieu": "142/2026/NĐ-CP", "corpus": "true", "cat": "19"}
    cases.append(("r13_dup_sohieu_real",
                  not _sohieu_dup_group_real([_d13_goc, _d13_vbhn])
                  and _sohieu_dup_group_real([_d13_l1, _d13_l2])
                  and not _sohieu_dup_group_real([_d13_pl, _d13_main])
                  and not _sohieu_dup_group_real([_d13_l1, dict(_d13_l2, corpus="false")])))
    # (F3) circuit-breaker: gws lỗi AUTH 1 lần → op sau đi THẲNG GAS (gws chỉ bị gọi 1 lần); cờ bật.
    import transport as _tp13
    _calls13 = {"gws": 0, "gas": 0}
    class _FkGas13:
        def get(self, action, **kw):
            _calls13["gas"] += 1
            return {"ok": True, "text": "x"}
    def _fk13_avail():
        return True
    def _fk13_call(op, **kw):
        _calls13["gws"] += 1
        raise _tp13.gws_bridge.GwsError("gws rc=2: Authentication failed")
    _o13_avail, _o13_call = _tp13.gws_bridge.is_available, _tp13.gws_bridge.call
    _o13_dead, _o13_warn = _tp13._GWS_AUTH_DEAD, set(_tp13._GWS_FALLBACK_WARNED)
    try:
        _tp13.gws_bridge.is_available = _fk13_avail
        _tp13.gws_bridge.call = _fk13_call
        _tp13._GWS_AUTH_DEAD = False
        with _hush():   # [FALLBACK→GAS] chủ đích của test breaker — nuốt khỏi console deploy
            _tp13.drive_op("read", gas=_FkGas13(), file_id="f1")
            _tp13.drive_op("read", gas=_FkGas13(), file_id="f2")
        _ok13 = _calls13["gws"] == 1 and _calls13["gas"] == 2 and _tp13._GWS_AUTH_DEAD is True
    finally:
        _tp13.gws_bridge.is_available = _o13_avail
        _tp13.gws_bridge.call = _o13_call
        _tp13._GWS_AUTH_DEAD = _o13_dead
        _tp13._GWS_FALLBACK_WARNED.clear(); _tp13._GWS_FALLBACK_WARNED.update(_o13_warn)
    cases.append(("r13_gws_auth_circuit_breaker",
                  _ok13 and _tp13._is_gws_auth_error("GWS_CRED_EXPIRED: invalid_grant")
                  and not _tp13._is_gws_auth_error("timeout sau 30s")))
    # (F6) parser nhận --sohieu-file/--resume.
    _ns13 = build_parser().parse_args(["corpus-audit", "--sohieu-file", "ds.txt", "--resume"])
    cases.append(("r13_corpus_audit_sohieu_file_flags",
                  _ns13.sohieu_file == "ds.txt" and _ns13.resume is True))

    # ═══ v1.33.1 (log Cowork A1 — vòng đời cred: 2 đường bundle + public đều phải tự tươi) — r14_* ═══
    # _stage_enc_upload: mặc định GHI ĐÈ TẠI CHỖ (update_content, fileId giữ nguyên — hết bake lại sau mỗi lần
    # token rụng); --new/thiếu fid → upload MỚI (hành vi cũ). Fake bridge đếm đường đi + soi đúng byte blob.
    import tl_gws as _tg14
    class _FkBridge14:
        def __init__(self):
            self.upd = 0; self.up = 0; self.last = None
        def update_content(self, fid, path, mime=None, **k):
            with open(path, "rb") as f:
                self.last = (fid, f.read())
            self.upd += 1
            return {"ok": True, "file": {"id": fid}}
        def upload(self, name, path, parents=None, mime=None, **k):
            self.up += 1
            return {"ok": True, "file": {"id": "NEWID14"}}
    _b14 = _FkBridge14()
    _f14a, _ip14a = _tg14._stage_enc_upload("x.enc", b"BLOB14", "fold", "FID14", False, g=_b14)
    _f14b, _ip14b = _tg14._stage_enc_upload("x.enc", b"BLOB14", "fold", "FID14", True, g=_b14)   # --new
    _f14c, _ip14c = _tg14._stage_enc_upload("x.enc", b"BLOB14", "fold", None, False, g=_b14)     # thiếu fid
    cases.append(("r14_stage_enc_inplace",
                  _f14a == "FID14" and _ip14a is True and _b14.upd == 1 and _b14.last == ("FID14", b"BLOB14")
                  and _f14b == "NEWID14" and _ip14b is False
                  and _f14c == "NEWID14" and _ip14c is False and _b14.up == 2))
    # Parser: gws-auth-stage/nlm-auth-stage nhận --cred-file-id/--new; secrets-set nhận --no-public
    # (mặc định no_public=False = CÓ đồng bộ public — đúng chốt 'cả 2 đường đều chạy').
    _ap14 = build_parser()
    _g14 = _ap14.parse_args(["gws-auth-stage", "--cred-file-id", "F1", "--new"])
    _n14 = _ap14.parse_args(["nlm-auth-stage", "--cred-file-id", "F2"])
    _s14 = _ap14.parse_args(["secrets-set", "--gws", "--no-public"])
    _s14b = _ap14.parse_args(["secrets-set", "--gws"])
    cases.append(("r14_auth_stage_parser_flags",
                  _g14.cred_file_id == "F1" and _g14.new is True
                  and _n14.cred_file_id == "F2" and _n14.new is False
                  and _s14.no_public is True and _s14b.no_public is False))

    # ═══ v1.33.2 (log rà 111 Luật — 6 defect A1..A6) — r15_* ═══
    # (A1) source-map query THEO TÊN không còn false-clean: BLHS name-query phải REVIEW + đủ 3 cờ (gate cũ đòi
    # qkey+direct nên câm); control: pool có VBHN canonical → gate im.
    _blhs15 = {"id": "b15", "drive_id": "b15", "name": "Luat_100-2015-QH13_Bo_Luat_Hinh_su",
               "so_hieu": "100/2015/QH13", "loai": "Bộ luật", "cat": "16", "corpus": "true", "nlm_source_id": "sb15"}
    _smA15 = _source_map_one("Bộ luật Hình sự", [_blhs15])
    _smB15 = _source_map_one("Luật Kế toán", [_v13])
    cases.append(("r15_srcmap_name_query_vbhn_gate",
                  any(w.startswith("NO_VERIFIED_VBHN_IN_CORPUS") for w in _smA15["warnings"])
                  and any(w.startswith("QT5_WEB_REQUIRED") for w in _smA15["warnings"])
                  and any(w.startswith("VBHN_HIGH_AMENDMENT_VELOCITY") for w in _smA15["warnings"])
                  and _smA15["verdict"] == "REVIEW"
                  and not any(w.startswith("NO_VERIFIED_VBHN_IN_CORPUS") for w in _smB15["warnings"])))
    # (A2) pin §0.13: XNC đang 01 → IM (hết đề xuất 01→39); XNC ở cat SAI → đề xuất CHÍNH pin 01;
    # AI/CĐS (QĐ 26/6) im lặng CẢ 2 chiều kể cả khi nằm cat lạ.
    _xnc15 = {"drive_id": "d62", "name": "VBHN_62-2025-VBHN-VPQH_2025_Nhap_canh_xuat_canh_qua_canh_cu_tru_NNN",
              "so_hieu": "62-2025-VBHN-VPQH", "loai": "VBHN", "cat": "01", "corpus": "true"}
    _hx15 = "VĂN BẢN HỢP NHẤT\n\nLUẬT\nNHẬP CẢNH, XUẤT CẢNH, QUÁ CẢNH, CƯ TRÚ CỦA NGƯỜI NƯỚC NGOÀI TẠI VIỆT NAM"
    _p15a = _cat_likely_wrong_suggest(_xnc15, _hx15)
    _p15b = _cat_likely_wrong_suggest(dict(_xnc15, cat="39"), _hx15)
    _p15c = _cat_likely_wrong_suggest({"drive_id": "d134b", "name": "Luat_134-2025-QH15_Tri_tue_nhan_tao",
                                       "so_hieu": "134/2025/QH15", "loai": "Luật", "cat": "45", "corpus": "true"}, "")
    cases.append(("r15_cat_pin_rules_s013",
                  _p15a is None and _p15b is not None and _p15b["suggested"] == "01"
                  and "§0.13" in str(_p15b.get("evidence")) and _p15c is None))
    # (A3) evidence không còn khẳng định 'đồng thuận cat-audit' (cat-audit có guard riêng, có thể vẫn im).
    _p15d = _cat_likely_wrong_suggest({"drive_id": "d143b", "name": "Luat_143-2025-QH15_Dau_tu",
                                       "so_hieu": "143/2025/QH15", "loai": "Luật", "cat": "45",
                                       "corpus": "true"}, "LUẬT\nĐẦU TƯ\n\nĐiều 1.")
    cases.append(("r15_cat_evidence_no_overclaim",
                  _p15d is not None and "đồng thuận cat-audit" not in str(_p15d.get("evidence"))
                  and "alias" in str(_p15d.get("evidence"))))
    # (A4) NO_SUBJECT_TOKENS hết oan: 'Thong_ke' ('thong' đụng stop-token thông-tư) = CÓ chủ đề; tên trơ thật vẫn cờ.
    cases.append(("r15_no_subject_tokens_fallback",
                  _name_structural_issues("Luat_89-2015-QH13_Luat_Thong_ke") == []
                  and "NO_SUBJECT_TOKENS" in _name_structural_issues("Luat_123-2025-QH15_GD")
                  and "NO_SUBJECT_TOKENS" in _name_structural_issues("Luat_71-2020-QH14")))
    # (A5+A6) parser: nlm-reconcile nhận --json; corpus-audit --limit default None (phân biệt explicit).
    _ns15 = build_parser().parse_args(["nlm-reconcile", "nb1", "--json"])
    _ca15 = build_parser().parse_args(["corpus-audit", "--all"])
    cases.append(("r15_reconcile_json_and_limit_default", _ns15.json is True and _ca15.limit is None))
    # (A6) --sohieu-file: mặc định CẢ LÔ (dedup, bỏ comment); --limit cắt LOUD + pool_total giữ tổng thật.
    import tempfile as _tf15, os as _os15
    _tlm15 = _TL_MODULE
    _fx15 = {"111-2025-QH15": {"id": "t1", "drive_id": "t1", "name": "Luat_111-2025-QH15_A", "so_hieu": "111/2025/QH15"},
             "112-2025-QH15": {"id": "t2", "drive_id": "t2", "name": "Luat_112-2025-QH15_B", "so_hieu": "112/2025/QH15"},
             "113-2025-QH15": {"id": "t3", "drive_id": "t3", "name": "Luat_113-2025-QH15_C", "so_hieu": "113/2025/QH15"}}
    _orig15 = _tlm15._canonical_for_query
    def _fk15(qq, refresh=False):
        e = _fx15.get(norm_sohieu(qq))
        return (e, [e] if e else [])
    _tlm15._canonical_for_query = _fk15
    try:
        _fd15, _fp15 = _tf15.mkstemp(suffix=".txt"); _os15.close(_fd15)
        with open(_fp15, "w", encoding="utf-8") as _f15:
            _f15.write("111/2025/QH15\n# comment\n112/2025/QH15\n113/2025/QH15\n111/2025/QH15\n")
        _nsA15 = build_parser().parse_args(["corpus-audit", "--sohieu-file", _fp15])
        _nsB15 = build_parser().parse_args(["corpus-audit", "--sohieu-file", _fp15, "--limit", "2"])
        with _hush():   # CẮT BATCH loud là chủ đích — nuốt khỏi console deploy
            _tA15 = _resolve_headerverify_targets(_nsA15, [])
            _tB15 = _resolve_headerverify_targets(_nsB15, [])
        _ok15 = (len(_tA15) == 3 and len(_tB15) == 2
                 and getattr(_nsB15, "_targets_pool_total", 0) == 3
                 and [_e["drive_id"] for _e in _tB15] == ["t1", "t2"])
    finally:
        _tlm15._canonical_for_query = _orig15
        try:
            _os15.remove(_fp15)
        except OSError:
            pass
    cases.append(("r15_sohieu_file_respects_limit", _ok15))

    # ═══ v1.33.3 (log rà 66×3 — D1/D2 dương-tính-giả heuristic + B nghẽn gom-tay lượt-2) — r16_* ═══
    # (D2) header-verify title: token VIẾT TẮT (hdnd) khớp theo dạng mở rộng; tên sai chủ đề THẬT vẫn FAIL.
    _hv16 = {"id": "h87", "drive_id": "h87", "name": "Luat_87-2015-QH13_HD_giam_sat_QH_HDND",
             "so_hieu": "87/2015/QH13", "loai": "Luật", "cat": "35", "corpus": "true"}
    _hx16 = ("QUỐC HỘI\n\nLUẬT\nHOẠT ĐỘNG GIÁM SÁT CỦA QUỐC HỘI VÀ HỘI ĐỒNG NHÂN DÂN\n\n"
             "Luật số: 87/2015/QH13\nCăn cứ Hiến pháp;\n"
             "Quốc hội ban hành Luật hoạt động giám sát của Quốc hội và Hội đồng nhân dân.\nĐiều 1. Phạm vi")
    _vr16 = _verify_header_match(_hv16, _hx16)
    _vr16b = _verify_header_match(dict(_hv16, name="Luat_87-2015-QH13_Kinh_doanh_bat_dong_san"), _hx16)
    cases.append(("r16_header_title_abbrev_ratio",
                  _vr16["checks"].get("title") is True and _vr16b["checks"].get("title") is False))
    # (D1) CAT_LIKELY_WRONG: 87/2015 (cur=35) KHÔNG còn bị gợi 44 chỉ vì alias 'giam sat' 2/10 từ (coverage-gate);
    # misfile THẬT giữ nguyên: 46/2024 Công chứng ở 09 → 04 (alias phủ TRỌN chủ đề).
    _p16a = _cat_likely_wrong_suggest({"drive_id": "d87", "name": "Luat_87-2015-QH13_HD_giam_sat_QH_HDND",
                                       "so_hieu": "87/2015/QH13", "loai": "Luật", "cat": "35", "corpus": "true"},
                                      "LUẬT\nHOẠT ĐỘNG GIÁM SÁT CỦA QUỐC HỘI VÀ HỘI ĐỒNG NHÂN DÂN\n\nĐiều 1.")
    _p16b = _cat_likely_wrong_suggest({"drive_id": "d46", "name": "Luat_46-2024-QH15_Cong_chung",
                                       "so_hieu": "46/2024/QH15", "loai": "Luật", "cat": "09", "corpus": "true"},
                                      "LUẬT\nCÔNG CHỨNG\n\nĐiều 1.")
    cases.append(("r16_cat_content_alias_coverage",
                  _p16a is None and _p16b is not None and _p16b["suggested"] == "04"))
    # (B) review-queue: gom đúng nhóm — BLHS → web LƯỢT-2 (★ high-velocity); luật 2025 sạch → clean;
    # dòng Luật thiếu sohieu → đếm LOUD; VBHN không thành mục hàng đợi riêng.
    _rq_new16 = {"id": "n1", "drive_id": "n1", "name": "Luat_91-2025-QH15_Bao_ve_du_lieu_ca_nhan",
                 "so_hieu": "91/2025/QH15", "loai": "Luật", "cat": "03", "corpus": "true", "nlm_source_id": "sn1"}
    _rq_nosh16 = {"id": "n2", "drive_id": "n2", "name": "Luat_khong_ro_so_hieu", "loai": "Luật", "corpus": "true"}
    _rq16 = _review_queue_report([_blhs15, _rq_new16, _rq_nosh16, _v13], limit=None)
    cases.append(("r16_review_queue_groups",
                  _rq16["laws_scanned"] == 2 and _rq16["skipped_no_sohieu"] == 1
                  and _rq16["web_round2_count"] == 1 and _rq16["web_round2"][0]["sohieu"] == "100-2015-QH13"
                  and _rq16["web_round2"][0]["priority_high_velocity"] is True
                  and bool(_rq16["web_round2"][0]["qt5_queries"])
                  and _rq16["clean_count"] == 1 and _rq16["relation_backfill"] == []))
    _rqns16 = build_parser().parse_args(["review-queue", "--json", "--limit", "5"])
    cases.append(("r16_review_queue_parser", _rqns16.json is True and _rqns16.limit == 5))

    # ═══ v1.33.4 (log chạy LIVE review-queue lần đầu — A1 backfill khống 2/5, A2 đếm không khớp; B1 status
    # thiếu verdict; C1/C2 điểm mù sweep) — r17_* ═══
    # (A1) canonical CONFIRMED (verdict OK + suppressor) KHÔNG còn thành relation_backfill khống → về clean.
    _rq17_base_ok = dict(rel_fx[0], drive_id="tdkt2022", corpus="true", loai="Luật", verified="yes")
    _rq17_amend = dict(rel_fx[1], drive_id="tdkt2026x")
    _rq17a = _review_queue_report([_rq17_base_ok, _rq17_amend], limit=None)
    cases.append(("r17_review_queue_no_fake_rel",
                  _rq17a["relation_backfill"] == [] and _rq17a["clean_count"] == 1
                  and _rq17a["laws_scanned"] == 1
                  and sum(_rq17a["counts"].values()) == _rq17a["laws_scanned"]))
    # (A1b, CẬP NHẬT P2-2 v1.33.12) base KHÔNG verified + amendment mồ côi LOW-CONF → REVIEW + UNLINKED nhưng
    # ứng viên toàn low-conf → bucket INFO `relation_low_confidence` (log: relation-check phủ định 3/3 ca
    # low-conf — bucket HÀNH ĐỘNG chỉ nhận strong/linked); vẫn kèm fix_command + flags_all (P2-1);
    # counts loại trừ nhau cộng đúng về tổng (A2).
    _rq17_base_rev = dict(rel_fx[0], drive_id="tdkt2022b", corpus="true", loai="Luật")
    _rq17b = _review_queue_report([_rq17_base_rev, _rq17_amend], limit=None)
    cases.append(("r17_review_queue_rel_low_conf_info",
                  _rq17b["relation_backfill"] == []
                  and len(_rq17b["relation_low_confidence"]) == 1
                  and "relation-check" in _rq17b["relation_low_confidence"][0]["fix_command"]
                  and "relation_low_confidence" in _rq17b["relation_low_confidence"][0]["buckets"]
                  and bool(_rq17b["relation_low_confidence"][0].get("flags_all"))
                  and sum(_rq17b["counts"].values()) == _rq17b["laws_scanned"] == 1
                  and sum(_rq16["counts"].values()) == _rq16["laws_scanned"]))
    # (B1) status/preingest_gate: alias {verdict, flags} top-level — driver batch hết nhận None câm;
    # decision/surface GIỮ NGUYÊN (compat).
    _pg17 = _need_base("preingest_gate")
    _st17a = _pg17._alias_vocab(_pg17.decide({"status": "IN_REGISTRY_HIEULUC_UNKNOWN", "sohieu": "74/2025/QH15"},
                                             [], False, False))
    _st17b = _pg17._alias_vocab(_pg17.decide({"status": "NOT_FOUND"}, [], False, False))
    cases.append(("r17_status_verdict_flags_alias",
                  _st17a.get("verdict") == "REVIEW" and _st17a.get("decision") == "REVIEW"
                  and "IN_REGISTRY_HIEULUC_UNKNOWN" in (_st17a.get("flags") or [])
                  and _st17b.get("verdict") == "ADD" and "NOT_FOUND" in (_st17b.get("flags") or [])))
    # (C2) detector raw_on_nlm: file THÔ (html/docx) đang là nguồn NLM LIVE = vi phạm 'chỉ push GDoc';
    # GDoc-native trên NLM và raw KHÔNG trên NLM đều không dính.
    _c17_html = {"id": "h1", "drive_id": "h1", "name": "luat-dau-thau-so-22-2023-qh15-259737-d1.html",
                 "mime": "text/html", "corpus": "true", "nlm_source_id": "eb6d0f", "nlm_status": "pushed"}
    _c17_gdoc = {"id": "g1", "drive_id": "g1", "name": "Luat_22-2023-QH15_Dau_thau", "corpus": "true",
                 "mime": "application/vnd.google-apps.document", "nlm_source_id": "s22", "nlm_status": "pushed"}
    _c17_raw = {"id": "r1", "drive_id": "r1", "name": "Luat_X.docx", "mime": "application/msword"}
    _c17 = _raw_on_nlm_rows([_c17_html, _c17_gdoc, _c17_raw])
    cases.append(("r17_raw_on_nlm_detector",
                  [e["drive_id"] for e in _c17] == ["h1"]))

    # ═══ v1.33.5 (log rà 69 v1.33.3-mount — khoá nốt regression + kế toán minh bạch) — r18_* ═══
    # (r18a) ĐÚNG HÌNH DẠNG ca 19-2012: amendment LINKED (goc) + VBHN năm-nay phủ theo năm → verdict OK +
    # AMENDMENT_CANDIDATES_COVERED_BY_VBHN_DATE → KHÔNG vào relation_backfill (v1.33.3 cũ xếp backfill khống).
    # CẬP NHẬT S-8 v1.33.15: VBHN duy nhất RẤT MỚI + covered + không thuộc nhóm HIGH_VELOCITY → UNVERIFIED_LATEST
    # hạ thành VBHN_LATEST_RECENT_COVERED (INFO) → RỜI hàng web_round2 luôn (về clean; năm fixture đặt ĐỘNG
    # để bất biến theo thời gian — VBHN năm-nay luôn 'rất mới').
    import time as _t18
    _yr18 = _t18.localtime().tm_year
    _r18_base = {"id": "b19", "drive_id": "b19", "name": "Luat_19-2012-QH13_Xuat_ban", "so_hieu": "19/2012/QH13",
                 "loai": "Luật", "cat": "32", "corpus": "true", "nlm_source_id": "sb19"}
    _r18_vbhn = {"id": "v26x", "drive_id": "v26x", "name": f"VBHN_25-{_yr18}-VBHN-VPQH_{_yr18}_Luat_Xuat_ban_HopNhat",
                 "so_hieu": f"25-{_yr18}-VBHN-VPQH", "loai": "VBHN", "goc": "19-2012-QH13", "cat": "32",
                 "corpus": "true", "nlm_source_id": "sv26"}
    _r18_amend = {"id": "a25x", "drive_id": "a25x", "name": "Luat_35-2025-QH15_SuaDoi_Xuat_ban",
                  "so_hieu": "35/2025/QH15", "cat": "32", "goc": "19-2012-QH13"}
    _sm18 = _source_map_one("19/2012/QH13", [_r18_base, _r18_vbhn, _r18_amend])
    _rq18 = _review_queue_report([_r18_base, _r18_vbhn, _r18_amend], limit=None)
    cases.append(("r18_covered_shape_no_fake_rel",
                  any(w.startswith("AMENDMENT_CANDIDATES_COVERED_BY_VBHN_DATE") for w in _sm18["warnings"])
                  and any(w.startswith("VBHN_LATEST_RECENT_COVERED") for w in _sm18["warnings"])
                  and not any(w.startswith("VBHN_CANDIDATE_UNVERIFIED_LATEST") for w in _sm18["warnings"])
                  and _sm18["verdict"] == "OK"
                  and _rq18["relation_backfill"] == [] and _rq18["laws_scanned"] == 1
                  and _rq18["counts"]["web_round2"] == 0 and _rq18["clean_count"] == 1
                  and sum(_rq18["counts"].values()) == 1))
    # (r18b) VBHN đội lốt loai='Luật' (ca 115-VBHN — data bẩn lọt bộ lọc Luật của người vận hành) →
    # đếm TƯỜNG MINH skipped_vbhn_as_base, không thành mục hàng đợi, kế toán 69-vs-68 khớp máy.
    _rq18b = _review_queue_report([dict(_v13, loai="Luật")], limit=None)
    cases.append(("r18_vbhn_as_base_accounting",
                  _rq18b["laws_scanned"] == 0 and _rq18b["skipped_vbhn_as_base"] == 1
                  and sum(_rq18b["counts"].values()) == 0))

    # ═══ v1.33.6 (log rà 66/68 chạy CANONICAL v1.33.5 — C flag≠payload, B7 reg-query --loai, F --version,
    # D cat trơ-vs-đủ) — r19_* ═══
    # (C) row rel (nay ở bucket relation_low_confidence — P2-2 v1.33.12) phải KÈM ứng viên cụ thể để soi ngay
    # (log: 'cổng báo có ứng viên mà không trả ứng viên nào') — _rq17b là ca UNLINKED 06/2026 quanh 06/2022.
    _r19_cands = (_rq17b["relation_low_confidence"][0].get("candidates") or [])
    cases.append(("r19_rel_row_carries_candidates",
                  bool(_r19_cands) and any("06/2026" in c or "06-2026" in c for c in _r19_cands)))
    # (B7) reg-query: trường loai + loai_canon trong row; parser nhận --loai.
    _r19_row = _reg_query_row({"drive_id": "x", "name": "Luat_X", "loai": "Luat"})
    _r19_ns = build_parser().parse_args(["reg-query", "--loai", "Luật", "--corpus"])
    cases.append(("r19_reg_query_loai",
                  _r19_row["loai"] == "Luat" and _r19_row["loai_canon"] == "Luật"
                  and _r19_ns.loai == "Luật"))
    # (F) `tl --version` là flag hợp lệ (argparse action=version → SystemExit 0, KHÔNG usage-error).
    with _hush():
        try:
            build_parser().parse_args(["--version"])
            _r19_ver = False
        except SystemExit as _se19:
            _r19_ver = (_se19.code in (0, None))
    cases.append(("r19_version_flag", _r19_ver))
    # (D) detector cat trơ-vs-đủ-tên: prefix có CẢ '05' lẫn '05_...' = biến thể; '31_X' đơn độc không dính.
    _r19_cv = _cat_bare_full_variants([{"cat": "05"}, {"cat": "05_Can_bo_cong_chuc_vien_chuc"},
                                       {"cat": "32"}, {"cat": "32_Thong_tin_bao_chi_xuat_ban"},
                                       {"cat": "31_Xay_dung"}, {"cat": "45"}])
    cases.append(("r19_cat_bare_full_variants",
                  set(_r19_cv) == {"05", "32"} and "31" not in _r19_cv and "45" not in _r19_cv))

    # ═══ v1.33.7 (log rà v1.33.6 — corpus-audit A1..A5 + schema marker) — r20_* ═══
    # (A1+A3+A4) `--all --resume`: cày TRỌN pool theo trang, rc=3=PARTIAL rồi LẶP CÙNG LỆNH tới rc=0 + tự dọn
    # checkpoint; nhánh RAW vẫn chạy check TÊN offline (slug .html 22-2023 — ca nonstandard nặng nhất trước đây
    # bị skip câm); JSON có partial/remaining/scanned_ids/clean_ids.
    import io as _io20, contextlib as _ctx20
    _tlm20 = _TL_MODULE
    _fix20 = [
        {"id": "w1", "drive_id": "w1", "name": "luat-dau-thau-so-22-2023-qh15-259737-d1.html",
         "so_hieu": "22/2023/QH15", "cat": "34", "corpus": "true", "mime": "text/html"},
        {"id": "w2", "drive_id": "w2", "name": "37_2025_TT-BYT_668487.docx", "so_hieu": "37/2025/TT-BYT",
         "cat": "45", "corpus": "true", "mime": "application/msword"},
        {"id": "w3", "drive_id": "w3", "name": "ND_39-2016-ND-CP_Quy_dinh_chi_tiet.docx", "so_hieu": "39/2016/NĐ-CP",
         "cat": "20", "corpus": "true", "mime": "application/msword"},
    ]
    _orig_me20 = _tlm20._manifest_entries
    _tlm20._manifest_entries = lambda refresh=False: _fix20
    _ck20 = _cache_file("corpus_audit_ckpt_all.json")
    try:
        if _ck20.exists():
            _ck20.unlink()
        _ns20a = build_parser().parse_args(["corpus-audit", "--all", "--resume", "--limit", "2", "--json"])
        _buf20a = _io20.StringIO()
        with _ctx20.redirect_stdout(_buf20a), _ctx20.redirect_stderr(_io20.StringIO()):
            _rc20a = cmd_corpus_audit(_ns20a)
        _o20a = json.loads(_buf20a.getvalue())
        _ns20b = build_parser().parse_args(["corpus-audit", "--all", "--resume", "--limit", "2", "--json"])
        _buf20b = _io20.StringIO()
        with _ctx20.redirect_stdout(_buf20b), _ctx20.redirect_stderr(_io20.StringIO()):
            _rc20b = cmd_corpus_audit(_ns20b)
        _o20b = json.loads(_buf20b.getvalue())
        _ck20_gone = not _ck20.exists()
    finally:
        _tlm20._manifest_entries = _orig_me20
        try:
            if _ck20.exists():
                _ck20.unlink()
        except OSError:
            pass
    cases.append(("r20_corpus_audit_all_resume_pages",
                  _rc20a == 3 and _o20a["partial"] is True and _o20a["remaining"] == 1
                  and _rc20b == 0 and _o20b["partial"] is False and _o20b["coverage_complete"] is True
                  and _ck20_gone))
    cases.append(("r20_raw_name_nonstandard_flagged",
                  any(r["drive_id"] == "w1" and any(p["type"] == "NAME_NONSTANDARD" for p in r["proposals"])
                      for r in _o20a["rows"])
                  and "scanned_ids" in _o20a and "header_mismatch_no_proposal" in _o20a))
    # (A2) Bộ luật ↔ Luật: header 'BỘ LUẬT' + registry loai='Luat' → LOAI_MISMATCH suggested 'Bộ luật';
    # registry đã đúng 'Bộ luật' → im.
    _hx20 = "QUỐC HỘI\n\nBỘ LUẬT\nHÌNH SỰ\n\nLuật số: 100/2015/QH13\nCăn cứ Hiến pháp\nĐiều 1. Nhiệm vụ"
    _e20 = {"drive_id": "d100b", "name": "Luat_100-2015-QH13_Bo_Luat_Hinh_su", "so_hieu": "100/2015/QH13",
            "loai": "Luat", "cat": "16", "corpus": "true"}
    _ar20a = _corpus_audit_row(_e20, _hx20)
    _ar20b = _corpus_audit_row(dict(_e20, loai="Bộ luật"), _hx20)
    cases.append(("r20_loai_bo_luat_mismatch",
                  any(p["type"] == "LOAI_MISMATCH" and p["suggested"] == "Bộ luật" for p in _ar20a["proposals"])
                  and not any(p["type"] == "LOAI_MISMATCH" for p in _ar20b["proposals"])))
    # (schema marker) driver kiểm trước khi tin payload review-queue.
    cases.append(("r20_review_queue_schema_marker", _rq18b.get("schema") == "review_queue.v1"))

    # ═══ v1.33.8 (log rà v1.33.6 gửi lại — mục còn thiếu duy nhất: 'cần chế độ đọc header song song') — r21_* ═══
    # --workers N: PREFETCH text song song theo chùm rồi xử TUẦN TỰ — mỗi doc chỉ đọc ĐÚNG 1 lần (không re-read
    # ở vòng tuần tự), kết quả/scanned_ids như tuần tự; mặc định 1 = hành vi cũ.
    _calls21 = {"n": 0}
    def _fk21_read(did, cfg=None):
        _calls21["n"] += 1
        if did == "g1":
            return "QUỐC HỘI\n\nLUẬT\nTHƯ VIỆN\n\nLuật số: 46/2019/QH14\nĐiều 1. Phạm vi"
        return "QUỐC HỘI\n\nLUẬT\nBÁO CHÍ\n\nLuật số: 126/2025/QH15\nĐiều 1. Phạm vi"
    _fix21 = [
        {"id": "g1", "drive_id": "g1", "name": "Luat_46-2019-QH14_Thu_vien", "so_hieu": "46/2019/QH14",
         "loai": "Luật", "cat": "32_Thong_tin_bao_chi_xuat_ban", "corpus": "true",
         "mime": "application/vnd.google-apps.document"},
        {"id": "g2", "drive_id": "g2", "name": "Luat_126-2025-QH15_Bao_chi", "so_hieu": "126/2025/QH15",
         "loai": "Luật", "cat": "32_Thong_tin_bao_chi_xuat_ban", "corpus": "true",
         "mime": "application/vnd.google-apps.document"},
    ]
    _orig_me21, _orig_rd21 = _tlm20._manifest_entries, _tlm20._read_doc_text
    _tlm20._manifest_entries = lambda refresh=False: _fix21
    _tlm20._read_doc_text = _fk21_read
    try:
        _ns21 = build_parser().parse_args(["corpus-audit", "--all", "--json", "--workers", "2"])
        _buf21 = _io20.StringIO()
        with _ctx20.redirect_stdout(_buf21), _ctx20.redirect_stderr(_io20.StringIO()):
            _rc21 = cmd_corpus_audit(_ns21)
        _o21 = json.loads(_buf21.getvalue())
    finally:
        _tlm20._manifest_entries = _orig_me21
        _tlm20._read_doc_text = _orig_rd21
    cases.append(("r21_corpus_audit_parallel_prefetch",
                  _rc21 == 0 and sorted(_o21["scanned_ids"]) == ["g1", "g2"]
                  and _calls21["n"] == 2 and _o21["scanned_clean"] == 2))

    # ═══ v1.33.9 (log rà 90/531 chạy v1.33.8 — A1 header_mismatch_no_proposal 31 ca ~100% VBHN, A6 dedup schema,
    # B '6 con số corpus') — r22_* ═══
    # (A1) GỐC RỄ: registry VBHN mang NĂM TIÊM THÊM (bất biến NN-YYYY-VBHN-XXX) còn văn bản in 'Số: NN/VBHN-XXX'
    # KHÔNG năm → check sohieu FAIL hệ thống; kèm A1b: toks title chỉ còn 1 token ('Luat_Ke_toan' → 'toan') mà
    # sàn max(2,…)=2 → title KHÔNG BAO GIỜ pass. Sau vá: header_ok=True, 0 proposals, RA KHỎI bucket.
    _e22v = {"drive_id": "v25t", "name": "VBHN_25-2025-VBHN-VPQH_2025_Luat_Ke_toan", "so_hieu": "25-2025-VBHN-VPQH",
             "loai": "VBHN", "cat": "17", "corpus": "true"}
    _hx22 = "VĂN PHÒNG QUỐC HỘI\n\nSố: 25/VBHN-VPQH\n\nLUẬT\nKẾ TOÁN\n\nCăn cứ\nĐiều 1. Phạm vi điều chỉnh kế toán"
    _vr22 = _verify_header_match(_e22v, _hx22)
    _ar22 = _corpus_audit_row(_e22v, _hx22)
    cases.append(("r22_vbhn_yearless_header_ok",
                  _vr22["checks"].get("sohieu") is True and _vr22["checks"].get("title") is True
                  and _vr22["ok"] is True and _ar22["proposals"] == []))
    # (A6) dedup-check: verdict=COLLISION nhưng payload chỉ ở exact_sohieu_collision → driver đọc `groups` thấy 0.
    # Nay alias groups/duplicates = cùng payload.
    _fix22 = [{"id": "da", "drive_id": "da", "name": "Luat_44-2024-QH15_SuaDoi_Duoc", "so_hieu": "44/2024/QH15",
               "corpus": "true", "cat": "45", "mime": "application/vnd.google-apps.document"},
              {"id": "db", "drive_id": "db", "name": "44_2024_QH15_583839.docx", "so_hieu": "44_2024_QH15",
               "cat": "45", "mime": "application/msword"}]
    _orig_me22 = _tlm20._manifest_entries
    _tlm20._manifest_entries = lambda refresh=False: _fix22
    try:
        _ns22 = build_parser().parse_args(["dedup-check", "44/2024/QH15", "--json"])
        _buf22 = _io20.StringIO()
        with _ctx20.redirect_stdout(_buf22), _ctx20.redirect_stderr(_io20.StringIO()):
            cmd_dedup_check(_ns22)
        _o22 = json.loads(_buf22.getvalue())
        # (B) tl counts: MỘT BẢNG mẫu số + định nghĩa trên cùng snapshot fixture.
        _ns22c = build_parser().parse_args(["counts", "--json"])
        _buf22c = _io20.StringIO()
        with _ctx20.redirect_stdout(_buf22c), _ctx20.redirect_stderr(_io20.StringIO()):
            _rc22c = cmd_counts(_ns22c)
        _o22c = json.loads(_buf22c.getvalue())
    finally:
        _tlm20._manifest_entries = _orig_me22
    cases.append(("r22_dedup_check_groups_alias",
                  _o22["verdict"] == "COLLISION" and _o22["groups"] == _o22["exact_sohieu_collision"]
                  and len(_o22["groups"]) >= 2 and _o22["duplicates"] == _o22["groups"]))
    cases.append(("r22_counts_one_table",
                  _rc22c == 0 and _o22c["counts"]["registry_rows"] == 2
                  and _o22c["counts"]["corpus_client"] == 1 and _o22c["counts"]["luat_loai_all"] == 0
                  and set(_o22c["basis"]) == set(_o22c["counts"])))

    # ═══ v1.33.10 (log rà: xref chết exporttext-scope dù gws sống; status vs vbhn-check 'mâu thuẫn' 143;
    # nlm-get không nhận tên profile; nghi --json bẩn stdout) — r23_* ═══
    # (B1) status USE_VBHN tự khai corroboration: goc VBHN RỖNG → +VBHN_GOC_UNCORROBORATED (vbhn-check --goc
    # 0 candidate là TẤT YẾU, không phải 2 sự thật) + LUÔN +USE_VBHN_UNVERIFIED_LATEST (S9 chưa lượt-2);
    # goc CÓ dẫn chiếu bản gốc → hết UNCORROBORATED.
    # (v1.33.11: fixture PHẢI có tên 2 bên khớp chủ đề — unknown-guard MERGE Codex nay chặn USE_VBHN khi
    # thiếu bằng chứng; nhánh SKIP + cờ corroboration bên dưới là ca ĐÃ pass subject.)
    _cur23 = {"status": "CONSOLIDATED_INTO_VBHN", "sohieu": "143/2025/QH15", "name": "Luat Dau tu"}
    _vb23a = {"sohieu": "61-2026-VBHN-VPQH", "on_nlm": True, "goc": "", "name": "Luat Dau tu hop nhat"}
    _vb23b = {"sohieu": "61-2026-VBHN-VPQH", "on_nlm": True, "goc": "143-2025-QH15; 90-2025-QH15",
              "name": "Luat Dau tu hop nhat"}
    _st23a = _pg17._alias_vocab(_pg17.decide(dict(_cur23, superseded_by=[_vb23a]), [], False, False))
    _st23b = _pg17._alias_vocab(_pg17.decide(dict(_cur23, superseded_by=[_vb23b]), [], False, False))
    cases.append(("r23_status_use_vbhn_corroboration",
                  _st23a.get("decision") == "SKIP" and "USE_VBHN_UNVERIFIED_LATEST" in _st23a["flags"]
                  and "VBHN_GOC_UNCORROBORATED" in _st23a["flags"]
                  and _st23b.get("use_vbhn_goc_corroborated") is True
                  and "VBHN_GOC_UNCORROBORATED" not in _st23b["flags"]
                  and "USE_VBHN_UNVERIFIED_LATEST" in _st23b["flags"]))
    # (B1-log1) --json SẠCH stdout máy-đọc: sweep + review-queue cmd-level trên fixture → stdout parse thẳng
    # json.loads, không banner/preamble (heartbeat đều đi stderr — corpus-audit/dedup/counts đã khoá ở r20-r22).
    _orig_me23 = _tlm20._manifest_entries
    _tlm20._manifest_entries = lambda refresh=False: _fix21
    try:
        _ns23s = build_parser().parse_args(["sweep", "--json"])
        _buf23s = _io20.StringIO()
        with _ctx20.redirect_stdout(_buf23s), _ctx20.redirect_stderr(_io20.StringIO()):
            cmd_sweep(_ns23s)
        _o23s = json.loads(_buf23s.getvalue())
        _ns23r = build_parser().parse_args(["review-queue", "--json"])
        _buf23r = _io20.StringIO()
        with _ctx20.redirect_stdout(_buf23r), _ctx20.redirect_stderr(_io20.StringIO()):
            cmd_review_queue(_ns23r)
        _o23r = json.loads(_buf23r.getvalue())
    finally:
        _tlm20._manifest_entries = _orig_me23
    cases.append(("r23_json_stdout_pure",
                  _buf23s.getvalue().lstrip().startswith("{") and isinstance(_o23s.get("total"), int)
                  and _buf23r.getvalue().lstrip().startswith("{") and _o23r.get("schema") == "review_queue.v1"))
    # (E1) nlm-get nhận TÊN PROFILE quen: 'vbqppl'/'base' → notebook nền (hết NLM API NOT_FOUND).
    _nb23, _er23 = _resolve_nlm_notebook("vbqppl")
    _nb23b, _ = _resolve_nlm_notebook("743ed200-aaaa-bbbb-cccc-000000000000")
    cases.append(("r23_nlm_notebook_profile_alias",
                  _nb23 == NLM_BASE_NOTEBOOK and _er23 is None
                  and _nb23b == "743ed200-aaaa-bbbb-cccc-000000000000"))

    # ═══ v1.33.12 (backlog 9 lỗi phiên khắc phục 04/07 — P0 register-rác · P1 recat/folder/BLuat · P2) — r24_* ═══
    # (P0-1) register: drive_id lạ (không manifest, không Drive) → validator False = REFUSE, KHÔNG insert dòng
    # rác; id trong manifest / file mới trên Drive (live_prober True) → cho ghi; parser có --force-insert.
    _orig_me24 = _tlm20._manifest_entries
    _tlm20._manifest_entries = lambda refresh=False: [{"id": "okid", "drive_id": "okid", "name": "Luat_X"}]
    try:
        _ok24a = _register_target_exists("okid", live_prober=lambda f: False)
        _ok24b = _register_target_exists("1CutOffId", live_prober=lambda f: False)
        _ok24c = _register_target_exists("1NewUploadId", live_prober=lambda f: True)
    finally:
        _tlm20._manifest_entries = _orig_me24
    _ns24 = build_parser().parse_args(["register", "--drive-id", "d1", "--force-insert", "--loai", "Luật"])
    cases.append(("r24_register_target_guard",
                  _ok24a is True and _ok24b is False and _ok24c is True and _ns24.force_insert is True))
    # (P1-1) recat ghi NHÃN ĐỦ canonical `NN_Ten` (khớp cat-list/folder) — nhãn trơ cùng mã vẫn được relabel.
    cases.append(("r24_recat_full_label",
                  _cat_reg_label("05") == "05_Can_bo_cong_chuc_vien_chuc"
                  and _cat_reg_label("34").startswith("34_")
                  and _cat_reg_label("QUARANTINE") == "QUARANTINE"))
    # (P1-3) `BLuat_` (chuẩn SINH TỰ ĐỘNG của standardize_name) là prefix hợp lệ, cùng họ Bo_luat với BLDS_/BLHS_.
    cases.append(("r24_bluat_prefix",
                  _name_structural_issues("BLuat_100-2015-QH13_Hinh_su") == []
                  and _name_prefix_family(_NAME_TYPE_PREFIX_RE.match("BLuat_x")) == "Bo_luat"))
    # (P2-3) backfill-loai --normalize: nhãn KÉP 'Quyết định/Quy định' → vế đầu; VBHN_* + loai='thuong'
    # (LỖI THẬT từng lọt) → conflict 'Văn bản hợp nhất'; không dòng nào rơi nonmappable.
    _bl24 = [{"drive_id": "q1", "name": "QD_5-2025-QD-TTg_X", "so_hieu": "5/2025/QĐ-TTg",
              "loai": "Quyết định/Quy định"},
             {"drive_id": "v67", "name": "VBHN_67-2025_Luat_Doanh_nghiep", "so_hieu": "67/2025",
              "loai": "thuong"}]
    _s24, _, _n24 = _backfill_loai_candidates(_bl24, normalize=True)
    _by24 = {s["drive_id"]: s for s in _s24}
    cases.append(("r24_backfill_loai_dual_and_vbhn_thuong",
                  _by24.get("q1", {}).get("loai") == "Quyết định"
                  and _by24.get("v67", {}).get("loai") == "Văn bản hợp nhất"
                  and _by24.get("v67", {}).get("mode") == "conflict" and _n24 == []))
    # (P2-2) ngưỡng strong của bucket rel + (P0-2) parser sweep --live-nlm.
    _ns24s = build_parser().parse_args(["sweep", "--live-nlm", "--json"])
    cases.append(("r24_rel_strong_and_sweep_live_flag",
                  _rq_rel_strong([{"confidence": "high"}]) and _rq_rel_strong([{"linked_to_query": True}])
                  and _rq_rel_strong([{"strong": True}]) and not _rq_rel_strong([{"confidence": "low"}])
                  and not _rq_rel_strong([]) and _ns24s.live_nlm is True))

    # ═══ v1.33.13 (MERGE patch AUDIT 07/2026 — 2 nhánh cùng vá backlog 9 lỗi trên v1.33.11) — r25_* ═══
    # (P0-1 LỚP 1) format-guard drive_id: ID thật 33/44 ký tự PASS, prefix nlm: PASS, id cắt cụt/rỗng FAIL.
    cases.append(("r25_looks_like_drive_id",
                  _looks_like_drive_id("198ZW9NykVi9NGaWReLH8zicdxdOkWz7CunOdlVixhu4") is True
                  and _looks_like_drive_id("nlm:398d50d7-a639-4528-8820-56644b12fb3e") is True
                  and _looks_like_drive_id("198ZW9NykVi9") is False
                  and _looks_like_drive_id("") is False))
    # (P2-3 mở rộng) VBHN đội lốt với sohieu -VBHN- corroborate nhãn KHÔNG-map-được BẤT KỲ → conflict;
    # BC working-doc loai='thuong' KHÔNG tên VBHN_ → tuyệt đối KHÔNG bị đề xuất 'Văn bản hợp nhất'
    # (assertion gốc của patch nới cho phép normalize enum hợp lệ nếu _normalize_loai map được 'thuong').
    _bl25 = [{"drive_id": "1AAAAAAAAAAAAAAAAAAAAAAAA", "name": "VBHN_67-2025-VBHN-VPQH_2025_Luat_Doanh_nghiep",
              "so_hieu": "67-2025-VBHN-VPQH", "loai": "nhãn-lạ-không-map"},
             {"drive_id": "1CCCCCCCCCCCCCCCCCCCCCCCC", "name": "BC_bao_cao_lam_viec", "so_hieu": "",
              "loai": "thuong"}]
    _s25, _, _n25 = _backfill_loai_candidates(_bl25, normalize=True)
    _by25 = {s["drive_id"]: s for s in _s25}
    cases.append(("r25_vbhn_masquerade_sohieu_corroborated",
                  _by25.get("1AAAAAAAAAAAAAAAAAAAAAAAA", {}).get("loai") == "Văn bản hợp nhất"
                  and _by25.get("1AAAAAAAAAAAAAAAAAAAAAAAA", {}).get("mode") == "conflict"
                  and _by25.get("1CCCCCCCCCCCCCCCCCCCCCCCC", {}).get("loai") != "Văn bản hợp nhất"))
    # (P0-1 bulk + recat alias + review_reason) parser/plan vocab: register --bulk chặn qua cùng cờ
    # --force-insert (wired — patch kia dùng --force-unsafe KHÔNG có trong parser register).
    cases.append(("r25_recat_plan_cat_label_alias", _cat_reg_label("32") == "32_Thong_tin_bao_chi_xuat_ban"))

    # ═══ v1.33.14 (MERGE nhánh-3 `D:\admin\tra-luat\tra-luat.zip` — bản độc lập thứ 3 trên v1.33.11) — r26_* ═══
    # (1) _normalize_loai tách nhãn KÉP tại NGUỒN (mọi caller hưởng): '/', ' và '.
    cases.append(("r26_normalize_loai_dual_at_source",
                  _normalize_loai("Quyết định/Quy định") == "Quyết định"
                  and _normalize_loai("Luat") == "Luật"))
    # (2) _infer_loai nhận prefix BLuat_ (chuẩn sinh standardize_name).
    cases.append(("r26_infer_loai_bluat",
                  _infer_loai("BLuat_100-2015-QH13_Hinh_su", "") == "Bộ luật"))
    # (3) register --bulk LỚP 2: id đúng-dạng nhưng không tồn tại → really_missing; id trong manifest/probe-OK
    # không dính; quá cap → coi missing luôn (không probe).
    _items26 = [{"drive_id": "1KnownIdAAAAAAAAAAAAAAAA"}, {"drive_id": "1GoodOnDriveBBBBBBBBBBBB"},
                {"drive_id": "1GhostIdCCCCCCCCCCCCCCCC"}]
    _rm26 = _register_bulk_missing(_items26, {"1KnownIdAAAAAAAAAAAAAAAA"},
                                   lambda f: f == "1GoodOnDriveBBBBBBBBBBBB")
    _rm26b = _register_bulk_missing([{"drive_id": f"1Cap{i:020d}"} for i in range(3)], set(),
                                    lambda f: True, cap=2)
    cases.append(("r26_register_bulk_missing",
                  _rm26 == ["1GhostIdCCCCCCCCCCCCCCCC"] and len(_rm26b) == 1))
    # (4) _resolve_cat_folder_impl (FakeG): exact-canonical dùng luôn KHÔNG rename; bare-đơn-nhất → RENAME về
    # canonical (gộp thật, giữ fileId); miss hết → mkdir đúng tên + parentId root.
    class _FkG26:
        def __init__(self, items):
            self.items = items; self.renames = []; self.mkdirs = []
        def get(self, action, **kw):
            if action == "list":
                return {"ok": True, "items": self.items}
            if action == "rename":
                self.renames.append((kw.get("fileId"), kw.get("name"))); return {"ok": True}
            if action == "info":
                return {"ok": True, "file": {"id": kw.get("fileId"), "name": "cũ-có-dấu"}}
            if action == "mkdir":
                self.mkdirs.append(kw); return {"ok": True, "folderId": "NEWF26", "created": True}
            raise AssertionError(action)
    _gA = _FkG26([{"id": "fE", "name": "05_Can_bo_cong_chuc_vien_chuc", "type": "folder"},
                  {"id": "fB", "name": "05", "type": "folder"}])
    _fidA, _ = _resolve_cat_folder_impl(_gA, "05", {}, "ROOT", "05_Can_bo_cong_chuc_vien_chuc")
    _gB = _FkG26([{"id": "fB", "name": "05", "type": "folder"}])
    with _hush():   # print 'gộp folder' chủ đích
        _fidB, _ = _resolve_cat_folder_impl(_gB, "05", {}, "ROOT", "05_Can_bo_cong_chuc_vien_chuc")
        _gC = _FkG26([])
        _fidC, _createdC = _resolve_cat_folder_impl(_gC, "05", {}, "ROOT", "05_Can_bo_cong_chuc_vien_chuc")
    cases.append(("r26_resolve_cat_folder_impl",
                  _fidA == "fE" and _gA.renames == []
                  and _fidB == "fB" and _gB.renames == [("fB", "05_Can_bo_cong_chuc_vien_chuc")]
                  and _fidC == "NEWF26" and _createdC is True
                  and _gC.mkdirs and _gC.mkdirs[0].get("parentId") == "ROOT"))
    # (5) backfill-loai trigger name-only v1.33.14: VBHN_ + loai='Luật' (sohieu KHÔNG -VBHN-) vẫn conflict
    # (ca 115 tổng quát — trước cần 2 bằng chứng nên sohieu thiếu -VBHN- là lọt).
    _s26, _, _ = _backfill_loai_candidates([{"drive_id": "v115b", "name": "VBHN_115_Thi_dua_HopNhat",
                                             "so_hieu": "115/2026/QH16", "loai": "Luật"}], normalize=True)
    cases.append(("r26_vbhn_name_only_conflict",
                  len(_s26) == 1 and _s26[0]["mode"] == "conflict" and _s26[0]["loai"] == "Văn bản hợp nhất"))

    # ═══ v1.33.15 (log rà 40/531 + review-queue 67 Luật CHẠY LIVE v1.33.14 — S-1 row-serialize · S-2 header
    # no-proposal 5 ca · S-3 cat-audit đề nghị rời rổ 46 · S-8 over-flag UNVERIFIED_LATEST 37/67 web) — r27_* ═══
    # (S-2b) _name_tail_key strip prefix họ Bộ-luật (BLuat chuẩn sinh + BLDS/BLHS… legacy) + sohieu → tail SẠCH
    # (trước: tail = NGUYÊN tên → token chủ đề dính rác 'bluat'/'qh13').
    cases.append(("r27_name_tail_key_bluat",
                  _name_tail_key("BLuat_100-2015-QH13_Bo_luat_hinh_su") == "bo luat hinh su"
                  and _name_tail_key("BLDS_91-2015-QH13_Bo_luat_Dan_su") == "bo luat dan su"))
    # (S-2a/c/d/e) title-check header-verify: token TAIL-first (hết rác prefix/sohieu), token NÉN CamelCase
    # ('NhapCanh') khớp text đã nén, viết tắt CSDL/NCC mở rộng so TỪ NGUYÊN VĂN trên text (từ 2-ký-tự 'co'/'so'/
    # 'du' bị _token_set lọc không còn làm trượt). 3 ca thật log rà 40 tái dựng — TRƯỚC fail title, NAY pass.
    _e27a = {"drive_id": "b27", "name": "BLuat_100-2015-QH13_Bo_luat_hinh_su", "so_hieu": "100/2015/QH13",
             "loai": "Bộ luật", "cat": "16_Hinh_su", "corpus": "true"}
    _vr27a = _verify_header_match(_e27a, "BỘ LUẬT\nHÌNH SỰ\nLuật số: 100/2015/QH13\nBộ luật này quy định về tội phạm và hình phạt.")
    _e27b = {"drive_id": "v62", "name": "VBHN_62-2026-VBHN-VPQH_2026_Luat_NhapCanh_XuatCanh_NN",
             "so_hieu": "62-2026-VBHN-VPQH", "loai": "Văn bản hợp nhất", "cat": "01", "corpus": "true"}
    _vr27b = _verify_header_match(_e27b, "VĂN BẢN HỢP NHẤT\nLUẬT\nNhập cảnh, xuất cảnh, quá cảnh, cư trú của người "
                                         "nước ngoài tại Việt Nam\nSố: 62/VBHN-VPQH\nLuật này quy định nhập cảnh, xuất cảnh.")
    _e27c = {"drive_id": "n47", "name": "ND_47-2024-ND-CP_CSDL_Quoc_gia", "so_hieu": "47/2024/NĐ-CP",
             "loai": "Nghị định", "cat": "03", "corpus": "true"}
    _vr27c = _verify_header_match(_e27c, "NGHỊ ĐỊNH\nSố: 47/2024/NĐ-CP\nChính phủ ban hành Nghị định về danh mục "
                                         "cơ sở dữ liệu quốc gia.")
    cases.append(("r27_header_title_no_junk_tokens",
                  _vr27a["checks"].get("title") is True and _vr27b["checks"].get("title") is True
                  and _vr27c["checks"].get("title") is True))
    # (S-2f) layout VPQH: 'Số: NN/VBHN-VPQH' CHỈ ở khối ký CUỐI văn bản (ca VBHN_21-2026 BLTTDS — đo thật vị trí
    # 492k/532k, ngoài head-6000) → check sohieu tìm trên TOÀN văn bản vẫn PASS.
    _e27f = {"drive_id": "v21", "name": "VBHN_21-2026-VBHN-VPQH_2026_Bo_luat_To_tung_dan_su",
             "so_hieu": "21-2026-VBHN-VPQH", "loai": "Văn bản hợp nhất", "cat": "37", "corpus": "true"}
    _txt27f = ("BỘ LUẬT\nTỐ TỤNG DÂN SỰ\nBộ luật Tố tụng dân sự số 92/2015/QH13 được sửa đổi, bổ sung bởi:\n"
               + ("Điều X. Nội dung tố tụng dân sự.\n" * 300)
               + "VĂN PHÒNG QUỐC HỘI\nSố: 21/VBHN-VPQH")
    _vr27f = _verify_header_match(_e27f, _txt27f)
    cases.append(("r27_vbhn_sohieu_in_signature_tail",
                  len(_txt27f) > 6000 and _vr27f["checks"].get("sohieu") is True))
    # (S-1) row corpus-audit TỰ MÔ TẢ: mirror proposal CHÍNH lên top-level (type/severity/suggested_name/
    # fix_command/proposal/flags) — driver phẳng hết đọc null; idempotent (checkpoint đời cũ nạp lại vẫn ra).
    _ar27 = _corpus_audit_row({"drive_id": "d141", "name": "ND_141-2024-ND-CP", "so_hieu": "141/2024/NĐ-CP",
                               "loai": "Nghị định", "cat": "45", "corpus": "true"},
                              "NGHỊ ĐỊNH\nSố: 141/2024/NĐ-CP\nquy định chi tiết một số điều")
    cases.append(("r27_audit_row_selfdescribing",
                  _ar27.get("type") == "NAME_NONSTANDARD"
                  and _ar27.get("suggested_name") == _ar27["proposals"][0]["suggested"]
                  and _ar27.get("fix_command") == _ar27["proposals"][0]["fix_command"]
                  and _ar27.get("flags") == ["NAME_NONSTANDARD"]
                  and _audit_row_flatten(dict(_ar27)).get("type") == "NAME_NONSTANDARD"))
    # (S-2g) header_ok=False + 0 đề xuất KHÔNG còn câm: row mang header_mismatches/header_checks nêu LÝ DO.
    _ar27g = _corpus_audit_row({"drive_id": "d27g", "name": "Luat_99-2020-QH14_Chu_de_khong_khop",
                                "so_hieu": "99/2020/QH14", "loai": "Luật", "cat": "20", "corpus": "true"},
                               "LUẬT\nSố: 99/2020/QH14\nquy định về vấn đề riêng.")
    cases.append(("r27_hdr_bad_carries_reason",
                  _ar27g.get("header_ok") is False and _ar27g["proposals"] == []
                  and any("TITLE" in m for m in _ar27g.get("header_mismatches") or [])))
    # (S-3) rổ 46: bằng chứng omnibus theo TÊN/REF — KHÔNG lấy cat 46 làm bằng chứng cho chính nó (lập luận
    # vòng); đang ở 46 + có bằng chứng → cat-audit/CAT_LIKELY_WRONG không đề xuất rời (ca 57-2024 46→34 log rà
    # 40); sửa-1-đích (TT_37) và luật thường không dính; chiều đề xuất VÀO 46 giữ nguyên (r13).
    cases.append(("r27_omnibus_name_evidence",
                  _omnibus_name_evidence({"name": "Luat_57-2024-QH15_SuaDoi_QuyHoach_DauTu_PPP_DauThau"})
                  and not _omnibus_name_evidence({"name": "TT_37-2025-TT-BYT_SuaDoi_TT05-2024_Dau_thau_thuoc"})
                  and not _omnibus_name_evidence({"name": "Luat_143-2025-QH15_Dau_tu"})))
    _e27o = {"drive_id": "o57", "name": "Luat_57-2024-QH15_SuaDoi_QuyHoach_DauTu_PPP_DauThau",
             "so_hieu": "57/2024/QH15", "loai": "Luật", "cat": "46_Sua_doi_nhieu_luat", "corpus": "true"}
    cases.append(("r27_cat_keeps_omnibus_in_46",
                  _cat_likely_wrong_suggest(_e27o, "") is None
                  and _cat_likely_wrong_suggest(dict(_e27o, cat="34"), "") is not None))
    import io as _io27, contextlib as _ctx27
    _orig_me27 = _TL_MODULE._manifest_entries
    _TL_MODULE._manifest_entries = lambda refresh=False: [_e27o]
    _buf27 = _io27.StringIO()
    try:
        with _ctx27.redirect_stdout(_buf27):
            _rc27 = _TL_MODULE.cmd_cat_audit(build_parser().parse_args(["cat-audit", "--json"]))
    finally:
        _TL_MODULE._manifest_entries = _orig_me27
    _ca27 = json.loads(_buf27.getvalue())
    cases.append(("r27_cat_audit_cmd_keeps_46", _rc27 == 0 and _ca27["count"] == 0))
    # (S-8) hạ UNVERIFIED_LATEST khi VBHN DUY NHẤT + RẤT MỚI (năm ≥ nay−1) + không luật-sửa nào MỚI HƠN đã biết
    # → cờ INFO VBHN_LATEST_RECENT_COVERED, rời hàng web LƯỢT-2 (log: 37/67 vào lượt-2, ~15 chỉ vì cờ này);
    # VBHN CŨ giữ nguyên hành vi (verify bản-mới-nhất là việc THẬT).
    import time as _t27
    _yr27 = _t27.localtime().tm_year
    _r27_base = {"id": "b50", "drive_id": "b50", "name": "Luat_50-2024-QH15_Cong_doan", "so_hieu": "50/2024/QH15",
                 "loai": "Luật", "cat": "20", "corpus": "true", "nlm_source_id": "s50"}
    _r27_vnew = {"id": "v90", "drive_id": "v90", "name": f"VBHN_90-{_yr27}-VBHN-VPQH_{_yr27}_Luat_Cong_doan_HopNhat",
                 "so_hieu": f"90-{_yr27}-VBHN-VPQH", "loai": "Văn bản hợp nhất", "goc": "50-2024-QH15",
                 "cat": "20", "corpus": "true", "nlm_source_id": "sv90"}
    _sm27n = _source_map_one("50/2024/QH15", [_r27_base, _r27_vnew])
    _r27_vold = {"id": "v01", "drive_id": "v01", "name": "VBHN_01-2017-VBHN-VPQH_2017_Luat_Cong_doan_HopNhat",
                 "so_hieu": "01-2017-VBHN-VPQH", "loai": "Văn bản hợp nhất", "goc": "50-2024-QH15",
                 "cat": "20", "corpus": "true", "nlm_source_id": "sv01"}
    _sm27o = _source_map_one("50/2024/QH15", [_r27_base, _r27_vold])
    cases.append(("r27_recent_vbhn_downgrades_unverified",
                  not any(w.startswith("VBHN_CANDIDATE_UNVERIFIED_LATEST") for w in _sm27n["warnings"])
                  and any(w.startswith("VBHN_LATEST_RECENT_COVERED") for w in _sm27n["warnings"])
                  and any(w.startswith("VBHN_CANDIDATE_UNVERIFIED_LATEST") for w in _sm27o["warnings"])
                  and not any(w.startswith("VBHN_LATEST_RECENT_COVERED") for w in _sm27o["warnings"])))
    _rq27 = _review_queue_report([_r27_base, _r27_vnew], limit=None)
    cases.append(("r27_review_queue_web_denoised",
                  _rq27["web_round2_count"] == 0 and _rq27["clean_count"] == 1
                  and sum(_rq27["counts"].values()) == _rq27["laws_scanned"] == 1))

    # ═══ v1.33.16 (MERGE nhánh-4 `tra-luat-skill-v1.33.15-gws3env-patched.zip` — bản độc lập CÙNG backlog
    # S-1..S-9 trên v1.33.14; port chọn lọc + REJECT có kiểm chứng) — r28_* ═══
    # (S-3b) _omnibus_name_text: pattern chữ 'sửa đổi (bổ sung) (một số) (điều của) các/nhiều luật' (nới hơn
    # nhánh-4 — bắt cả phrasing thật) + dạng nén giữ nguyên; KHÔNG double-count 'dautucong' (bug nhánh-4:
    # 'dautu' ⊂ 'dautucong' → 1 đề tài đếm thành 2 → false-omnibus, đã reject).
    cases.append(("r28_omnibus_text_patterns",
                  _omnibus_name_text("Luat_SuaDoi_bo_sung_mot_so_dieu_cua_cac_luat_ve_dau_tu")
                  and _omnibus_name_text("Luật sửa đổi nhiều luật")
                  and _omnibus_name_text("Luat_57-2024-QH15_SuaDoi_QuyHoach_DauTu_PPP_DauThau")
                  and not _omnibus_name_text("Luat_SuaDoi_Dau_tu_cong")
                  and not _omnibus_name_text("Luat_75-2025-QH15_SuaDoi_Quang_cao")))
    # (S-3b) boundary rule ép 46 cho omnibus dạng NÉN nằm nhầm folder — GUARD: VBHN không bao giờ ép 46
    # (lỗ nhánh-4: VBHN của luật-sửa tên có SuaDoi+nhiều đề tài sẽ bị kéo vào 46 — trái doctrine).
    cases.append(("r28_boundary_46_compact_not_vbhn",
                  _cat_boundary_rule("Luat_57-2024-QH15_SuaDoi_QuyHoach_DauTu_PPP_DauThau")[0] == "46"
                  and _cat_boundary_rule("VBHN_09-2026-VBHN-VPQH_2026_SuaDoi_QuyHoach_DauTu_HopNhat")[0] != "46"))
    # (S-2h) _declared_loai_from_header — detector VIẾT LẠI: dòng IN HOA đứng riêng, khớp đầu-dòng, dòng ĐẦU
    # TIÊN thắng. 2 ca REJECT nhánh-4 (repro thật): NĐ 'Căn cứ Bộ luật…' phải ra Nghị định (bản 12k-scan của
    # nhánh-4 ra 'Bộ luật' → LOAI_MISMATCH oan 🔴); TT 'Căn cứ Văn bản hợp nhất số…' phải ra Thông tư.
    _nd28 = ("NGHỊ ĐỊNH\nSố: 145/2020/NĐ-CP\nQuy định chi tiết Bộ luật Lao động\n"
             "Căn cứ Bộ luật Lao động ngày 20 tháng 11 năm 2019;")
    cases.append(("r28_declared_loai_anchored",
                  _declared_loai_from_header("BỘ LUẬT\nSố: 100/2015/QH13\nHÌNH SỰ\nĐiều 1. Phạm vi") == "Bộ luật"
                  and _declared_loai_from_header("VĂN BẢN HỢP NHẤT\nLUẬT\nCÔNG ĐOÀN\nLuật Công đoàn số 50/2024/QH15") == "Văn bản hợp nhất"
                  and _declared_loai_from_header(_nd28) == "Nghị định"
                  and _declared_loai_from_header("THÔNG TƯ\nSố: 95/2025/TT-BTC\nCăn cứ Văn bản hợp nhất số 19/VBHN-VPQH;") == "Thông tư"))
    # (S-2h) 4c corpus-audit: registry 'Luật' + tiêu đề 'BỘ LUẬT' xen kẽ (ca 4/4b câm — repro trên chính bản ta
    # TRƯỚC port: 0 đề xuất) → nay LOAI_MISMATCH 'Bộ luật'; NEGATIVE: NĐ trích 'Căn cứ Bộ luật' KHÔNG dính,
    # entry VBHN (tiêu đề in luật gốc 'BỘ LUẬT' — ca 21-2026 BLTTDS) KHÔNG dính.
    _bl28 = _corpus_audit_row({"drive_id": "Dbl28", "name": "Luat_100-2015-QH13_Hinh_su", "loai": "Luật",
                               "so_hieu": "100/2015/QH13", "cat": "16", "corpus": "true"},
                              "BỘ LUẬT\nSố: 100/2015/QH13\nHÌNH SỰ\nĐiều 1. Phạm vi tội phạm hình sự")
    _nd28r = _corpus_audit_row({"drive_id": "Dnd28", "name": "ND_145-2020-ND-CP_Dieu_kien_lao_dong",
                                "loai": "Nghị định", "so_hieu": "145/2020/NĐ-CP", "cat": "20", "corpus": "true"},
                               _nd28 + "\nquy định điều kiện lao động")
    _vb28r = _corpus_audit_row({"drive_id": "Dvb28", "name": "VBHN_21-2026-VBHN-VPQH_2026_Bo_luat_To_tung_dan_su",
                                "loai": "Văn bản hợp nhất", "so_hieu": "21-2026-VBHN-VPQH", "cat": "37",
                                "corpus": "true"},
                               "BỘ LUẬT\nTỐ TỤNG DÂN SỰ\nSố: 21/VBHN-VPQH\nvề tố tụng dân sự")
    cases.append(("r28_loai_declared_proposal_guarded",
                  any(p["type"] == "LOAI_MISMATCH" and p["suggested"] == "Bộ luật" for p in _bl28["proposals"])
                  and not any(p["type"] == "LOAI_MISMATCH" for p in _nd28r["proposals"])
                  and not any(p["type"] == "LOAI_MISMATCH" for p in _vb28r["proposals"])))
    # (S-8b) vbhn-check dampener: luật RẤT MỚI (năm động ≥ nay−2) không candidate + không high-velocity → hạ;
    # high-velocity (Đấu thầu) / có candidate / luật cũ → KHÔNG hạ.
    _yr28 = _t27.localtime().tm_year
    cases.append(("r28_vbhn_latest_low_priority",
                  _vbhn_latest_low_priority_recent_law("Lưu trữ", f"33/{_yr28}/QH15", "", False)
                  and not _vbhn_latest_low_priority_recent_law("Đấu thầu", f"57/{_yr28}/QH15", "", False)
                  and not _vbhn_latest_low_priority_recent_law("Lưu trữ", f"33/{_yr28}/QH15", "", True)
                  and not _vbhn_latest_low_priority_recent_law("Thư viện", "46/2019/QH14", "", False)))
    # (S-1b) flatten alias driver phẳng: command/proposal_count/current (phần port được của
    # _corpus_audit_json_row nhánh-4; proposal_rows[] KHÔNG port — trùng proposals[] vốn đã phẳng từng món).
    _fl28 = _audit_row_flatten({"drive_id": "x", "proposals": [
        {"type": "NAME_NONSTANDARD", "current": "cu", "suggested": "moi", "severity": 2, "icon": "🟠",
         "fix_command": "tl header-verify --drive-id x --fix-suggest"}]})
    cases.append(("r28_flatten_command_alias",
                  _fl28["command"] == _fl28["fix_command"] and _fl28["proposal_count"] == 1
                  and _fl28["current"] == "cu"))

    # ═══ v1.33.17 (MERGE nhánh-5 `tra-luat-skill-v1.33.17-gws3env-patch-merged.zip` — nền là CHÍNH v1.33.15
    # canonical + merge song song nhánh-4 + `tl_changes.patch`; port 1 món mới + khoá 2 reject) — r29_* ═══
    # (S-2i) số hiệu format LỎNG 'Số: 47 / 2024 / NĐ - CP' (separator lạ — _SOHIEU_RE trượt) → compact-match
    # alnum trên 2000 ký tự đầu vẫn khớp; số hiệu SAI THẬT (99/2099) vẫn fail (test gốc của nhánh-5, giữ nguyên).
    _vr29_loose = _verify_header_match(_e27c, "NGHỊ ĐỊNH\nSố: 47 / 2024 / NĐ - CP\nquy định về cơ sở dữ liệu quốc gia")
    _vr29_wrong = _verify_header_match(_e27c, "NGHỊ ĐỊNH\nSố: 99 / 2099 / NĐ - CP\nquy định về cơ sở dữ liệu quốc gia")
    cases.append(("r29_header_sohieu_loose_spacing",
                  _vr29_loose["checks"].get("sohieu") is True
                  and _vr29_wrong["checks"].get("sohieu") is False))
    # (S-3, chiều VÀO-46 — test nhánh-5 PASS bằng CƠ CHẾ ta: boundary text-pattern, KHÔNG phải evidence
    # refs-based của họ): omnibus 57-2024 nằm nhầm 34 → cat-audit đề xuất 46.
    _e29o = dict(_e27o, cat="34_Dau_tu")
    _TL_MODULE._manifest_entries = lambda refresh=False: [_e29o]
    _buf29 = _io27.StringIO()
    try:
        with _ctx27.redirect_stdout(_buf29):
            _rc29 = _TL_MODULE.cmd_cat_audit(build_parser().parse_args(["cat-audit", "--json"]))
    finally:
        _TL_MODULE._manifest_entries = _orig_me27
    _ca29 = json.loads(_buf29.getvalue())
    cases.append(("r29_cat_audit_moves_omnibus_into_46",
                  _rc29 == 0 and _ca29["count"] == 1 and _ca29["flags"][0].get("suggest") == ["46"]))
    # (REJECT nhánh-5, PHẢN CHỨNG khoá vĩnh viễn): luật sửa MỘT đích + registry có goc+related (2 ref tokens)
    # KHÔNG được coi là omnibus để kéo vào 46 — bundle nhánh-5 dùng _omnibus_name_evidence (gồm nhánh ≥2-refs)
    # làm cờ VÀO-46 → 71-2020 SuaDoi_HIV (cat 45 Y tế) bị đề xuất 45→46 confidence HIGH (repro trên bundle).
    # Evidence refs-based CHỈ được dùng chiều SUPPRESS (giữ-trong-46), chiều PROPOSE phải qua text-pattern chặt.
    _e29hiv = {"id": "a71", "drive_id": "a71", "name": "Luat_71-2020-QH14_SuaDoi_Phong_chong_HIV_AIDS",
               "so_hieu": "71/2020/QH14", "loai": "Luật", "cat": "45_Y_te", "corpus": "true",
               "goc": "64-2006-QH11", "related": "01-2021-VBHN-VPQH"}
    _TL_MODULE._manifest_entries = lambda refresh=False: [_e29hiv]
    _buf29b = _io27.StringIO()
    try:
        with _ctx27.redirect_stdout(_buf29b):
            _rc29b = _TL_MODULE.cmd_cat_audit(build_parser().parse_args(["cat-audit", "--json"]))
    finally:
        _TL_MODULE._manifest_entries = _orig_me27
    _ca29b = json.loads(_buf29b.getvalue())
    cases.append(("r29_single_target_amender_not_forced_46",
                  _rc29b == 0 and not any(f.get("suggest") == ["46"] for f in _ca29b["flags"])))

    # ═══ v1.33.18 (log rà 67 Luật CHẠY LIVE v1.33.17 — A1 nlm-get --json · A2 pagination mâu thuẫn ·
    # A3 thiếu full-audit · D cặp gốc/sửa lệch pha; MERGE bundle-18 [4 fix đúng trọng tâm] + tl_changes.patch
    # [chỉ lấy ngữ nghĩa --full-giữ-checkpoint; reject bypass-sohieu/into-46-refs/fix_command --apply]) — r30_* ═══
    # (A1+A3 parser) nlm-get nhận --json no-op; corpus-audit nhận --full.
    _ns30 = build_parser().parse_args(["nlm-get", "nb743", "--json"])
    _ns30b = build_parser().parse_args(["corpus-audit", "--all", "--full", "--json"])
    cases.append(("r30_parser_nlm_get_json_and_full",
                  _ns30.json is True and _ns30b.full is True and _ns30b.all is True))
    # (D) luật SỬA đã nằm trong chuỗi goc của VBHN khác (AMENDS_OTHER_VBHN) → KHÔNG còn NO_VERIFIED_VBHN/QT5
    # (nội dung đã phản ánh trong VBHN của luật ĐÍCH — hết lệch pha 64-2006 OK vs 71-2020 bị đẩy web lượt-2);
    # control: thiếu VBHN trong corpus thì gate cũ VẪN nổ (không nới quá tay).
    _r30_base = {"id": "h64", "drive_id": "h64", "name": "Luat_64-2006-QH11_Phong_chong_HIV_AIDS",
                 "so_hieu": "64/2006/QH11", "loai": "Luật", "cat": "45", "corpus": "true", "nlm_source_id": "s64"}
    _r30_amend = {"id": "h71", "drive_id": "h71", "name": "Luat_71-2020-QH14_SuaDoi_Phong_chong_HIV",
                  "so_hieu": "71/2020/QH14", "loai": "Luật", "cat": "45", "corpus": "true", "nlm_source_id": "s71"}
    _r30_vbhn = {"id": "hv30", "drive_id": "hv30", "name": "VBHN_01-2021-VBHN-VPQH_2021_Luat_Phong_chong_HIV_HopNhat",
                 "so_hieu": "01-2021-VBHN-VPQH", "loai": "Văn bản hợp nhất", "goc": "64-2006-QH11;71-2020-QH14",
                 "cat": "45", "corpus": "true", "nlm_source_id": "sv30"}
    _sm30 = _source_map_one("71/2020/QH14", [_r30_base, _r30_amend, _r30_vbhn])
    _sm30b = _source_map_one("71/2020/QH14", [_r30_base, _r30_amend])
    cases.append(("r30_amends_vbhn_suppresses_no_verified",
                  any(w.startswith("AMENDS_OTHER_VBHN") for w in _sm30["warnings"])
                  and not any(w.startswith("NO_VERIFIED_VBHN_IN_CORPUS") for w in _sm30["warnings"])
                  and not any(w.startswith("QT5_WEB_REQUIRED") for w in _sm30["warnings"])
                  and any(w.startswith("NO_VERIFIED_VBHN_IN_CORPUS") for w in _sm30b["warnings"])
                  and any(w.startswith("QT5_WEB_REQUIRED") for w in _sm30b["warnings"])))
    # (A2+A3 END-TO-END offline, fixture RAW nên không đọc mạng): vòng 1 `--all --resume --limit 1` →
    # rc=3 PARTIAL + resume_required + next_offset=PROGRESS(1) + pagination_mode=checkpoint_resume;
    # vòng 2 `--all --full` NỐI CHECKPOINT (ngữ nghĩa tl_changes.patch — bundle-18 chạy trần mất tiến độ
    # nếu chết giữa chừng) → quét nốt 2 target còn lại, rc=0, coverage_complete, checkpoint tự dọn.
    _fx30 = [
        {"id": "z1", "drive_id": "z1", "name": "37_2025_TT-BYT_668487.docx", "so_hieu": "37/2025/TT-BYT",
         "cat": "45", "corpus": "true", "mime": "application/msword"},
        {"id": "z2", "drive_id": "z2", "name": "141_2024_ND-CP_999.docx", "so_hieu": "141/2024/NĐ-CP",
         "cat": "20", "corpus": "true", "mime": "application/msword"},
        {"id": "z3", "drive_id": "z3", "name": "95_2025_TT-BTC_888.docx", "so_hieu": "95/2025/TT-BTC",
         "cat": "06", "corpus": "true", "mime": "application/msword"},
    ]
    _ck30 = _cache_file("corpus_audit_ckpt_all.json")
    _orig_me30 = _TL_MODULE._manifest_entries
    _TL_MODULE._manifest_entries = lambda refresh=False: _fx30
    try:
        if _ck30.exists():
            _ck30.unlink()
        _b30a, _e30a = _io27.StringIO(), _io27.StringIO()
        with _ctx27.redirect_stdout(_b30a), _ctx27.redirect_stderr(_e30a):
            _rc30a = _TL_MODULE.cmd_corpus_audit(
                build_parser().parse_args(["corpus-audit", "--all", "--resume", "--limit", "1", "--json"]))
        _j30a = json.loads(_b30a.getvalue())
        _b30b, _e30b = _io27.StringIO(), _io27.StringIO()
        with _ctx27.redirect_stdout(_b30b), _ctx27.redirect_stderr(_e30b):
            _rc30b = _TL_MODULE.cmd_corpus_audit(
                build_parser().parse_args(["corpus-audit", "--all", "--full", "--json"]))
        _j30b = json.loads(_b30b.getvalue())
        _ck30_gone = not _ck30.exists()
    finally:
        _TL_MODULE._manifest_entries = _orig_me30
        try:
            if _ck30.exists():
                _ck30.unlink()
        except OSError:
            pass
    cases.append(("r30_pagination_partial_markers",
                  _rc30a == 3 and _j30a["partial"] is True and _j30a["resume_required"] is True
                  and _j30a["next_offset"] == 1 and _j30a["pagination_mode"] == "checkpoint_resume"
                  and bool(_j30a["resume_command"]) and _j30a["remaining"] == 2))
    cases.append(("r30_full_resumes_checkpoint_to_done",
                  _rc30b == 0 and _j30b["partial"] is False and _j30b["resume_required"] is False
                  and _j30b["pagination_mode"] == "full_checkpoint" and _j30b["scanned"] == 2
                  and _j30b["next_offset"] is None and _j30b["coverage_complete"] is True and _ck30_gone))

    # ═══ v1.33.19 (log rà v1.33.18 LIVE — S-10 guard cat mới vá 2/3 surface + nhóm B schema/heuristic) — r31_* ═══
    # (S-10) header-verify checks.cat ĐỒNG BỘ guard với cat-audit/corpus-audit: omnibus-46 PASS; điều ước
    # cat 23 → check KHÔNG ÁP DỤNG (mirror cat-audit skip 00/23); misfile THẬT trong 46 (không bằng chứng
    # omnibus) VẪN FAIL — không nới quá tay.
    _e31o = {"drive_id": "o57h", "name": "Luat_57-2024-QH15_SuaDoi_QuyHoach_DauTu_PPP_DauThau",
             "so_hieu": "57/2024/QH15", "loai": "Luật", "cat": "46_Sua_doi_nhieu_luat", "corpus": "true"}
    _hdr31 = ("LUẬT\nSửa đổi, bổ sung một số điều của Luật Quy hoạch, Luật Đầu tư, Luật PPP, Luật Đấu thầu\n"
              "Luật số: 57/2024/QH15\nCăn cứ Hiến pháp...")
    _vr31o = _verify_header_match(_e31o, _hdr31)
    _e31t = {"drive_id": "ilo88", "name": "DUQT_ILO-088_Dich_vu_viec_lam", "so_hieu": "",
             "loai": "Điều ước quốc tế", "cat": "23_Ngoai_giao_dieu_uoc", "corpus": "true"}
    _vr31t = _verify_header_match(_e31t, "CÔNG ƯỚC SỐ 88\nVề tổ chức dịch vụ việc làm\nlao động việc làm dịch vụ")
    _e31bad = {"drive_id": "m38", "name": "Luat_38-2019-QH14_Quan_ly_thue", "so_hieu": "38/2019/QH14",
               "loai": "Luật", "cat": "46_Sua_doi_nhieu_luat", "corpus": "true"}   # misfile thật trong 46 (infer 33)
    _vr31bad = _verify_header_match(_e31bad, "LUẬT\nQUẢN LÝ THUẾ\nLuật số: 38/2019/QH14\nquản lý thuế")
    cases.append(("r31_header_cat_guard_3_surfaces",
                  _vr31o["checks"].get("cat") is True
                  and "cat" not in _vr31t["checks"]
                  and _vr31bad["checks"].get("cat") is False))
    # (B.1) review-queue: row REVIEW có cờ NGOÀI nhóm-việc → flags mirror flags_all (hết flags=[] câm);
    # tạo REVIEW bằng DIRTY_CANDIDATES (∈ review-set nhưng ∉ nhóm-việc): bản sao cùng số hiệu cat root.
    _e31d = {"id": "dr31", "drive_id": "dr31", "name": "Luat_88-2030-QH17_Thu_nghiem",
             "so_hieu": "88/2030/QH17", "loai": "Luật", "cat": "20", "corpus": "true", "nlm_source_id": "sd31"}
    _e31dirty = {"id": "dr31b", "drive_id": "dr31b", "name": "Luat_88-2030-QH17_Thu_nghiem_copy",
                 "so_hieu": "88/2030/QH17", "loai": "Luật", "cat": "root_ZZ", "corpus": "true"}
    _rq31 = _review_queue_report([_e31d, _e31dirty], limit=None)
    _row31 = (_rq31["review_other"] or [{}])[0]
    cases.append(("r31_review_other_flags_not_empty",
                  len(_rq31["review_other"]) >= 1
                  and bool(_row31.get("flags")) and "DIRTY_CANDIDATES" in (_row31.get("flags") or [])))
    # (B.2+B.3) viết tắt GDDH/VBQPPL nở được + đuôi _HL<date> bị strip khỏi tail:
    _e31g = {"drive_id": "g125", "name": "Luat_125-2025-QH15_GDDH", "so_hieu": "125/2025/QH15",
             "loai": "Luật", "cat": "13", "corpus": "true"}
    _vr31g = _verify_header_match(_e31g, "LUẬT\nGIÁO DỤC ĐẠI HỌC\nLuật số: 125/2025/QH15\ngiáo dục đại học")
    _e31v = {"drive_id": "v64", "name": "Luat_64-2025-QH15_BH_VBQPPL", "so_hieu": "64/2025/QH15",
             "loai": "Luật", "cat": "42", "corpus": "true"}
    _vr31v = _verify_header_match(_e31v, "LUẬT\nBAN HÀNH VĂN BẢN QUY PHẠM PHÁP LUẬT\nLuật số: 64/2025/QH15\n"
                                         "văn bản quy phạm pháp luật")
    cases.append(("r31_abbrev_gddh_vbqppl_title_pass",
                  _vr31g["checks"].get("title") is True and _vr31v["checks"].get("title") is True))
    cases.append(("r31_hl_suffix_stripped",
                  _name_tail_key("Luat_02-2026-QH16_Thu_do_HL2026-07-01") == "thu do"))
    # (B.5) TITLE_METADATA_MISMATCH hết oan khi metadata title là TÊN-FILE-CỤT ('Luat_123-2025-QH15_GD' →
    # tail rỗng = không bằng chứng); misname THẬT (meta trích yếu chủ đề KHÁC hẳn) vẫn bắt.
    _tf31a = _title_flags({"name": "Luat_123-2025-QH15_SuaDoi_Giao_duc", "so_hieu": "123/2025/QH15",
                           "loai": "Luật", "cat": "13", "nlm_title": "Luat_123-2025-QH15_GD"})
    _tf31b = _title_flags({"name": "Luat_123-2025-QH15_SuaDoi_Giao_duc", "so_hieu": "123/2025/QH15",
                           "loai": "Luật", "cat": "13", "title_vn": "Quản lý thuế xuất khẩu, thuế nhập khẩu"})
    cases.append(("r31_title_meta_filename_not_mismatch",
                  "TITLE_METADATA_MISMATCH" not in _tf31a and "TITLE_METADATA_MISMATCH" in _tf31b))
    # (B.7) orphan detector: FTA-chương/văn kiện Đảng KHÔNG còn là orphan (lớp riêng); tên thô THẬT vẫn orphan.
    _g31 = _hygiene_groups([
        {"id": "c19", "drive_id": "c19", "name": "CPTPP_Chuong_19_Lao_dong", "cat": "23_Ngoai_giao_dieu_uoc"},
        {"id": "vk4", "drive_id": "vk4", "name": "VK_DH_XIV_Bao_cao_chinh_tri", "cat": "00_Van_ban_cua_Dang"},
        {"id": "raw3", "drive_id": "raw3", "name": "219_2025_ND-CP_m_668418", "cat": "20"},
    ])
    cases.append(("r31_orphans_exclude_treaty_party",
                  [_x.get("drive_id") for _x in _g31["orphans"]] == ["raw3"]
                  and len(_g31["treaties"]) == 1 and len(_g31["party_docs"]) == 1))

    # ═══ v1.33.20 (MERGE bundle-20 — nhánh song song CÙNG backlog S-10/nhóm-B trên v1.33.18; lấy KIẾN TRÚC
    # hàm chung _header_verify_infer_cats + infer_cat_rule, SỬA 2 guard-bug của họ) — r32_* ═══
    # (S-10 chiều MỚI, port bundle-20): omnibus thật NẰM NHẦM 34 → header-verify nay bắt được (infer ['46']
    # + rule máy-đọc trong mismatch) — v1.33.19 ta chỉ chắn chiều giữ-đúng-chỗ, surface này im với misfile.
    _e32mis = {"drive_id": "o57m", "name": "Luat_57-2024-QH15_SuaDoi_QuyHoach_DauTu_PPP_DauThau",
               "so_hieu": "57/2024/QH15", "loai": "Luật", "cat": "34_Dau_tu", "corpus": "true"}
    _vr32mis = _verify_header_match(_e32mis, _hdr31)
    cases.append(("r32_header_catches_misfiled_omnibus",
                  _header_verify_infer_cats(_e32mis) == (["46"], "omnibus-46")
                  and _vr32mis["checks"].get("cat") is False
                  and any("rule=omnibus-46" in m for m in _vr32mis["mismatches"])))
    # (REJECT bundle-20, khoá lần 3 lớp r29 trên surface THỨ 3): luật sửa MỘT đích + goc+related (2 refs)
    # nằm ĐÚNG 45 — bundle infer ['46'] rule omnibus-46 → cat:False oan (repro trên bundle). Ta: chiều
    # PROPOSE chỉ text-pattern → infer KHÔNG phải ['46'].
    _e32hiv = {"drive_id": "a71h", "name": "Luat_71-2020-QH14_SuaDoi_Phong_chong_HIV_AIDS",
               "so_hieu": "71/2020/QH14", "loai": "Luật", "cat": "45_Y_te", "corpus": "true",
               "goc": "64-2006-QH11", "related": "01-2021-VBHN-VPQH"}
    cases.append(("r32_single_target_refs_not_forced_46_3rd_surface",
                  _header_verify_infer_cats(_e32hiv)[0] != ["46"]))
    # (SUPPRESS arm giữ evidence RỘNG): omnibus tên mờ ('SuaDoi_Mot_so_van_ban' — text-pattern im) nhưng
    # registry có ≥2 refs, ĐANG Ở 46 → giữ (infer ['46'] = pass).
    _e32sup = {"drive_id": "s99", "name": "Luat_99-2029-QH17_SuaDoi_Mot_so_van_ban",
               "so_hieu": "99/2029/QH17", "loai": "Luật", "cat": "46_Sua_doi_nhieu_luat", "corpus": "true",
               "goc": "11-2020-QH14;22-2021-QH15"}
    cases.append(("r32_suppress_arm_refs_kept_in_46",
                  _header_verify_infer_cats(_e32sup) == (["46"], "omnibus-46")))
    # (treaty 2 chiều): trong 23 → not-applicable (rỗng); tên treaty nằm NHẦM 20 → đề xuất về 23.
    _e32t20 = {"drive_id": "cu105", "name": "CU_ILO-105_Lao_dong_cuong_buc", "so_hieu": "",
               "loai": "Công ước", "cat": "20_Lao_dong", "corpus": "true"}
    cases.append(("r32_treaty_two_directions",
                  _header_verify_infer_cats(_e31t) == ([], "cat-23-not-applicable")
                  and _header_verify_infer_cats(_e32t20) == (["23"], "treaty-23")))
    # (abbrev bổ sung bundle-20): bh/qppl/gdpt nở được (append-only).
    _exp32 = _expand_abbrev("bh qppl gdpt")
    cases.append(("r32_abbrev_bh_qppl_gdpt",
                  "ban hanh" in _exp32 and "quy pham phap luat" in _exp32 and "giao duc pho thong" in _exp32))

    # ═══ v1.33.21 (log verify v1.33.20 — B.5-residual: 15/17 title_mismatch là VBHN tên-thiếu-năm, sohieu ĐÃ
    # year-fix → KHÔNG fixer nào phủ, backlog treo vĩnh viễn) — r33_* ═══
    # (a) _name_inject_vbhn_year nhận CẢ dạng NGẮN NN-VPQH (ca thật VBHN_34-VPQH trả nguyên tên trước fix);
    # idempotent với tên đã có năm.
    cases.append(("r33_name_inject_short_form",
                  _name_inject_vbhn_year("VBHN_34-VPQH_Luat_Luu_tru_hop_nhat", "34", 2026, "VPQH")
                  == "VBHN_34-2026-VBHN-VPQH_Luat_Luu_tru_hop_nhat"
                  and _name_inject_vbhn_year("VBHN_61-VBHN-VPQH_An_toan_thuc_pham", "61", 2025, "VPQH")
                  == "VBHN_61-2025-VBHN-VPQH_An_toan_thuc_pham"
                  and _name_inject_vbhn_year("VBHN_61-2025-VBHN-VPQH_ATTP", "61", 2025, "VPQH")
                  == "VBHN_61-2025-VBHN-VPQH_ATTP"))
    # (b) lane NAME-ONLY trong _vbhn_year_fix_items: sohieu có năm + tên thiếu năm → mode=name_only, sohieu
    # GIỮ NGUYÊN; tên đã đủ năm → KHÔNG đề xuất; corpus=false → bỏ qua; ca sohieu-thiếu-năm cũ vẫn ra như trước.
    _fx33 = [
        {"id": "y1", "drive_id": "y1", "name": "VBHN_34-VPQH_Luat_Luu_tru_hop_nhat",
         "so_hieu": "34-2026-VBHN-VPQH", "loai": "Văn bản hợp nhất", "corpus": "true"},
        {"id": "y2", "drive_id": "y2", "name": "VBHN_61-2025-VBHN-VPQH_An_toan_thuc_pham",
         "so_hieu": "61-2025-VBHN-VPQH", "loai": "Văn bản hợp nhất", "corpus": "true"},
        {"id": "y3", "drive_id": "y3", "name": "VBHN_99-VPQH_Bo_qua_quarantine",
         "so_hieu": "99-2026-VBHN-VPQH", "loai": "Văn bản hợp nhất", "corpus": "false"},
        {"id": "y4", "drive_id": "y4", "name": "VBHN_14-VBHN-VPQH_ATVSLD", "so_hieu": "14-VBHN-VPQH",
         "loai": "Văn bản hợp nhất", "corpus": "true", "issue_year": "2024"},
    ]
    _f33, _n33, _c33 = _vbhn_year_fix_items(_fx33)
    _f33_no = [s for s in _f33 if s.get("mode") == "name_only"]
    _f33_sh = [s for s in _f33 if s.get("mode") != "name_only"]
    cases.append(("r33_year_fix_name_only_lane",
                  len(_f33_no) == 1 and _f33_no[0]["drive_id"] == "y1"
                  and _f33_no[0]["new_sohieu"] == _f33_no[0]["old_sohieu"] == "34-2026-VBHN-VPQH"
                  and "2026" in _f33_no[0]["new_name"]
                  and len(_f33_sh) == 1 and _f33_sh[0]["drive_id"] == "y4"
                  and _f33_sh[0]["new_sohieu"] == "14-2024-VBHN-VPQH"
                  and not any(s["drive_id"] in ("y2", "y3") for s in _f33)))

    # ═══ v1.33.22 (MERGE bundle-21 — nhánh hội tụ trên v1.33.20, BỔ TRỢ v1.33.21 ta: advisory-split +
    # quarantine stale-ref fixer; SỬA PRIMITIVE bundle vi phạm bất biến reg_clear) — r34_* ═══
    # (B3/B9 bucket) quarantine: ref NLM + status removed → clear_stale_nlm_ref; status pushed (live) →
    # ghost_nlm (KHÔNG clear — xoá nguồn tay); không ref → không bucket nào.
    _q34 = _quarantine_fix_items([
        {"id": "q1", "drive_id": "q1", "name": "VBHN_09-VBHN-VPQH_Dau_tu", "cat": QUARANTINE_CAT,
         "corpus": "false", "nlm_source_id": "s-old", "nlm_status": "removed"},
        {"id": "q2", "drive_id": "q2", "name": "Luat_X_ghost", "cat": QUARANTINE_CAT,
         "corpus": "false", "nlm_source_id": "s-live", "nlm_status": "pushed"},
        {"id": "q3", "drive_id": "q3", "name": "Luat_Y_sach", "cat": QUARANTINE_CAT, "corpus": "false"},
    ])
    cases.append(("r34_quarantine_stale_vs_ghost",
                  [r["drive_id"] for r in _q34["clear_stale_nlm_ref"]] == ["q1"]
                  and [r["drive_id"] for r in _q34["ghost_nlm"]] == ["q2"]))
    # (B3/B9 primitive — khoá BẤT BIẾN): _quarantine_clear_stale phải đi action `reg_clear` keyed+confirm,
    # KHÔNG reg_bulk giá trị rỗng (bundle-21 dùng _journaled_reg_write → webapp BỎ QUA ghi-rỗng = false-success).
    class _FkG34:
        def __init__(self):
            self.calls = []
        def get(self, action, **kw):
            self.calls.append((action, kw))
            if action == "reg_clear":
                return {"ok": True, "cleared": 1}
            raise AssertionError(f"lệnh cấm: {action}")
    _g34 = _FkG34()
    _ok34, _fail34 = _quarantine_clear_stale("selftest-r34", _g34,
                                             [{"drive_id": "q1", "nlm_source_id": "s-old", "nlm_notebook_id": "nb1"}])
    cases.append(("r34_clear_stale_uses_reg_clear",
                  _ok34 == 1 and _fail34 == []
                  and len(_g34.calls) == 1 and _g34.calls[0][0] == "reg_clear"
                  and _g34.calls[0][1].get("confirm") == "yes"
                  and "nlm_source_id" in str(_g34.calls[0][1].get("cols"))))
    # (B.5-residual split) headline title_mismatch CHỈ còn lệch hành-động-được; VBHN metadata → advisory riêng.
    _g34h = _hygiene_groups([
        {"id": "t1", "drive_id": "t1", "name": "VBHN_14-VBHN-VPQH_Luat_84-2015_ATVSLD_HopNhat",
         "so_hieu": "14/VBHN-VPQH", "loai": "VBHN", "issue_year": "2024", "cat": "20", "corpus": "true"},
        {"id": "t2", "drive_id": "t2", "name": "Luat_123-2025-QH15_SuaDoi_Giao_duc", "so_hieu": "123/2025/QH15",
         "loai": "Luật", "cat": "13", "corpus": "true", "title_vn": "Quản lý thuế xuất khẩu, thuế nhập khẩu"},
    ])
    cases.append(("r34_title_mismatch_vs_vbhn_advisory_split",
                  [_x.get("drive_id") for _x in _g34h["title_mismatch"]] == ["t2"]
                  and [_x.get("drive_id") for _x in _g34h["vbhn_metadata_advisory"]] == ["t1"]))

    # ═══ v1.33.23 (log rà Cowork LIVE v1.33.20 — C-1.4: installer ghi PATH vào ~/.profile/.bashrc nhưng bash
    # NON-INTERACTIVE không source → `nlm` trần chết, chỉ chạy được absolute-path/`tl nlm-*`) — r35_* ═══
    # _symlink_nlm_system_path: 3 nhánh test được offline (nhánh symlink thật chỉ chạy POSIX/Cowork):
    # non-POSIX → no-op; src chưa cài → no-op; dst đã tồn tại trỏ chỗ khác → CẢNH BÁO, KHÔNG đè.
    _tg35 = _need_base("tl_gws")
    import tempfile as _tmp35
    with _tmp35.TemporaryDirectory() as _d35:
        _src35 = os.path.join(_d35, "nlm"); _dst35 = os.path.join(_d35, "usrbin_nlm")
        open(_src35, "w").write("#!/bin/sh\n")
        open(_dst35, "w").write("other\n")
        _r35a = _tg35._symlink_nlm_system_path(src=_src35, dst=_dst35, posix=False)      # non-POSIX
        _r35b = _tg35._symlink_nlm_system_path(src=os.path.join(_d35, "khong_co"),
                                               dst=_dst35, posix=True)                    # src thiếu
        _r35c = _tg35._symlink_nlm_system_path(src=_src35, dst=_dst35, posix=True)        # dst đã có → cảnh báo
    cases.append(("r35_nlm_symlink_guards",
                  _r35a == "" and _r35b == "" and "đã tồn tại" in _r35c))

    # ═══ v1.33.24 (MERGE bundle-23 — nhánh hội tụ trên v1.33.22, xử CÙNG log Cowork bằng các món BỔ TRỢ ta:
    # cowork-plan / package-integrity / up --nlm 1-bước / counts --live-nlm; bundle sạch nhất từ trước tới nay
    # — verify trên cây thật + canary PASS, 0 reject) — r36_* ═══
    # (2 test gốc bundle giữ nguyên) package integrity canary: cây lành PASS; NUL/cắt cụt bị bắt.
    import tempfile as _tmp36
    import pathlib as _pl36
    with _tmp36.TemporaryDirectory() as _td36:
        _base36 = _pl36.Path(_td36)
        for _fn36 in ["tl.py", "tl_gws.py", "nlm_cli.py", "transport.py", "gas.py", "boot.py", "contract_check.py",
                      # v1.33.56 (tl_core/F3): canary phủ thêm tl_core — cây mock phải có đủ
                      "tl_core/__init__.py", "tl_core/deterministic.py", "tl_core/jsonio.py",
                      "tl_core/workflow.py", "tl_core/release.py", "tl_core/live.py",
                      "tl_core/zip_ingest.py", "tl_core/ocr.py", "tl_core/chunking.py",
                      "tl_core/command_registry.py"]:
            _fp36 = _base36 / _fn36
            _fp36.parent.mkdir(parents=True, exist_ok=True)
            _fp36.write_text("# ok\n" + "x=1\n" * 100, encoding="utf-8")
        cases.append(("r36_skill_package_integrity_ok", _skill_package_integrity(_base36)["ok"] is True))
        (_base36 / "tl_gws.py").write_bytes(b"x=1\x00")
        cases.append(("r36_skill_package_integrity_catches_nul", _skill_package_integrity(_base36)["ok"] is False))
    # (+của ta) integrity phải PASS trên CHÍNH cây skill đang chạy (boot.py nằm ở _fallback — lookup phải với tới;
    # nếu check này đỏ trên cây lành thì doctor sẽ false-alarm vĩnh viễn) + parser nhận cowork-plan/counts --live-nlm.
    cases.append(("r36_integrity_passes_on_real_tree", _skill_package_integrity(None)["ok"] is True))
    _ns36 = build_parser().parse_args(["counts", "--live-nlm", "--notebook-id", "nb1"])
    _ns36b = build_parser().parse_args(["cowork-plan", "--json"])
    cases.append(("r36_parser_cowork_plan_counts_live",
                  _ns36.live_nlm is True and _ns36.notebook_id == "nb1" and _ns36b.json is True))

    # ═══ v1.33.25 (log rà 67 LIVE v1.33.24 — A5: schema lệch giữa 2 surface: source-map --json trả
    # flags_all=None + qt5_queries rỗng trong khi review-queue đầy đủ → driver batch đọc đồng nhất gãy) — r37_* ═══
    _sm37 = _source_map_one("71/2020/QH14", [_r30_base, _r30_amend, _r30_vbhn])
    cases.append(("r37_source_map_item_flags_all_alias",
                  set(_sm37.get("flags_all") or []) == set(_sm37.get("flags") or [])
                  and _sm37.get("flags_all") is not None
                  and isinstance(_sm37.get("qt5_queries"), list)))

    # ═══ v1.33.26 (MERGE bundle-25 — nhánh hội tụ trên v1.33.24, A5 của họ là SUPERSET bản ta v1.33.25
    # [+review_reason, dedup BASE_SCOPE_HIT, QT5-fallback] + 2 món mới: --out atomic [A3 timeout] +
    # config-pin-registry [S-9]; port trọn, 0 reject — lần 2 liên tiếp) — r38_* ═══
    # (test gốc bundle, giữ ngữ nghĩa) schema parity: REVIEW có cờ web → flags_all/review_reason/qt5 đủ.
    _sm38 = _source_map_one("100-2015-QH13", [
        {"id": "law100", "name": "BLuat_100-2015-QH13_Bo_luat_hinh_su", "so_hieu": "100/2015/QH13",
         "loai": "Bộ luật", "cat": "22", "corpus": "true", "mime": "application/vnd.google-apps.document"}])
    cases.append(("r38_source_map_schema_parity_qt5",
                  isinstance(_sm38.get("flags_all"), list)
                  and set(_sm38.get("flags_all") or []) == set(_sm38.get("flags") or [])
                  and isinstance(_sm38.get("review_reason"), list) and bool(_sm38.get("qt5_queries"))))
    # (test gốc bundle) config-pin-registry: pin an toàn vào config local, TỪ CHỐI Doc legacy 1mATG,
    # giữ nguyên key khác trong config (read-modify-write, không clobber).
    import tempfile as _tmp38
    import os as _os38
    _cfg38 = _os38.path.join(_tmp38.gettempdir(), "tl_selftest_pin_cfg38.json")
    try:
        open(_cfg38, "w", encoding="utf-8").write(json.dumps(
            {"profiles": {"vbqppl": {"rootFolderId": "R0"}}, "defaultProfile": "vbqppl", "webappUrl": "https://x"}))
        _pin_ok38 = _pin_registry_doc_id_config(_cfg38, "SHEET_REAL_123", profile="vbqppl")
        _pin_bad38 = _pin_registry_doc_id_config(_cfg38, _LEGACY_REGISTRY_DOC_ID, profile="vbqppl")
        _pd38 = json.loads(open(_cfg38, encoding="utf-8").read())
        cases.append(("r38_config_pin_registry_safe",
                      bool(_pin_ok38.get("ok")) and _pin_bad38.get("error") == "REFUSE_LEGACY_DOC_ID"
                      and _pd38["profiles"]["vbqppl"]["registryDocId"] == "SHEET_REAL_123"
                      and _pd38["profiles"]["vbqppl"]["rootFolderId"] == "R0"
                      and _pd38.get("webappUrl") == "https://x"))
    finally:
        try:
            _os38.remove(_cfg38)
        except OSError:
            pass
    # (+của ta) --out atomic: _emit_json_payload ghi file + in path; nội dung parse lại đúng.
    _out38 = _os38.path.join(_tmp38.gettempdir(), "tl_selftest_out38", "payload.json")
    try:
        _b38 = _io27.StringIO()
        with _ctx27.redirect_stdout(_b38):
            _emit_json_payload({"ok": True, "n": 3}, _out38)
        _rt38 = json.loads(open(_out38, encoding="utf-8").read())
        cases.append(("r38_emit_json_out_atomic",
                      _rt38 == {"ok": True, "n": 3} and _out38 in _b38.getvalue()
                      and not _os38.path.exists(_out38 + ".tmp")))
    finally:
        try:
            _os38.remove(_out38)
        except OSError:
            pass

    # ═══ v1.33.27 (log Cowork lặp A/B/C/D/E): ops-plan + --out phủ lệnh JSON nặng — r39_* ═══
    _cfg39 = _os38.path.join(_tmp38.gettempdir(), "tl_selftest_ops_cfg39.json")
    try:
        open(_cfg39, "w", encoding="utf-8").write(json.dumps(
            {"profiles": {"vbqppl": {"notebookId": "NB39"}}, "defaultProfile": "vbqppl"}))
        # v1.33.28 (sửa test bundle-27 env-leak): các case trước gọi apply_profile_offline(config THẬT) →
        # TL_REGISTRY_DOC_ID (máy đã pin) + TL_NOTEBOOK_ID nằm sẵn trong env và ĐÈ fixture → action pin biến
        # mất + notebook ≠ NB39 → fail OAN trên máy-đã-pin. Test phải HERMETIC: pop cả bộ env, khôi phục sau.
        _env39 = {k: _os38.environ.pop(k, None) for k in ("TL_REGISTRY_DOC_ID", "TL_NOTEBOOK_ID", "TL_PROFILE")}
        try:
            _op39 = _ops_plan_report([], config_path=_cfg39, profile="vbqppl")
        finally:
            for _k39, _v39 in _env39.items():
                if _v39 is not None:
                    _os38.environ[_k39] = _v39
        _ids39 = {x.get("id") for x in _op39.get("actions") or []}
        cases.append(("r39_ops_plan_has_pin_slot_cowork",
                      _op39.get("schema") == "ops_plan.v1"
                      and "pin_registry_doc_id" in _ids39
                      and "slot_preflight" in _ids39
                      and "cowork_bootstrap_guard" in _ids39
                      and _op39.get("notebook") == "NB39"))
        _ap39 = build_parser()
        _n39a = _ap39.parse_args(["ops-plan", "--json", "--out", "/tmp/ops.json"])
        _n39b = _ap39.parse_args(["sweep", "--json", "--out", "/tmp/sweep.json"])
        _n39c = _ap39.parse_args(["counts", "--json", "--out", "/tmp/counts.json"])
        _n39d = _ap39.parse_args(["nlm-get", "NB39", "--json", "--out", "/tmp/nlm.json"])
        _n39e = _ap39.parse_args(["doctor", "--json", "--out", "/tmp/doctor.json"])
        cases.append(("r39_parser_out_heavy_json_commands",
                      _n39a.out.endswith("ops.json") and _n39b.out.endswith("sweep.json")
                      and _n39c.out.endswith("counts.json") and _n39d.out.endswith("nlm.json")
                      and _n39e.out.endswith("doctor.json")))
    except Exception:
        cases.append(("r39_ops_plan_has_pin_slot_cowork", False))
        cases.append(("r39_parser_out_heavy_json_commands", False))
    finally:
        try:
            _os38.remove(_cfg39)
        except OSError:
            pass

    # ═══ v1.29.7 (log NĐ131 — 9 vấn đề ingest phụ lục) — r5_* ═══
    # (#2) resolver: query SỐ HIỆU với 2 ứng viên (chính văn + PHỤ LỤC cùng key) phải chọn CHÍNH VĂN —
    # cả khi chính văn có sohieu-registry khớp, lẫn khi CẢ HAI sohieu rỗng (PL_ penalty tự quyết).
    _r5_main = {"id": "m131", "drive_id": "m131", "name": "ND_131-2021-ND-CP_Nghi_dinh_chi_tiet_BLLD",
                "so_hieu": "131/2021/NĐ-CP", "loai": "Nghị định", "corpus": "true",
                "mime": "application/vnd.google-apps.document"}
    _r5_pl = {"id": "p131", "drive_id": "p131", "name": "PL_131-2021-ND-CP_Phu_luc_I_Bieu_mau",
              "so_hieu": "", "corpus": "true", "mime": "application/vnd.google-apps.document"}
    _r5_best, _r5_gid, _n, _h = _resolve_deep_target("131/2021/NĐ-CP", [_r5_pl, _r5_main])
    cases.append(("r5_resolver_main_over_appendix", _r5_gid == "m131"))
    _r5_main2 = dict(_r5_main, so_hieu="")   # cả hai sohieu rỗng → PL_ penalty vẫn đẩy chính văn lên
    _r5_best2, _r5_gid2, _n2, _h2 = _resolve_deep_target("131/2021/NĐ-CP", [_r5_pl, _r5_main2])
    cases.append(("r5_resolver_pl_penalty_alone", _r5_gid2 == "m131"))
    # (#4) dedup gate KHÔNG còn tier sohieu: phụ lục (drive_id khác, title khác) CÙNG SỐ HIỆU với nguồn live
    # → 'clear' (trước: false-positive TITLE_ALREADY_ON_NOTEBOOK trỏ nhầm source chính văn). Trùng THẬT vẫn 'dup'.
    class _FakeNC5:
        def __init__(self, srcs): self._s = srcs
        def source_list(self, nb, skip_freshness=True, drive=True):
            return {"ok": True, "sources": self._s}
    _DGM = "1MainDriveId0123456789abcd"
    _live5 = [{"id": "s-main", "title": "ND_131-2021-ND-CP_Nghi_dinh_chi_tiet_BLLD", "drive_id": _DGM}]
    _v5a, _d5a = _nlm_dedup_gate(_FakeNC5(_live5), "nb", [{"drive_id": "1PhuLucDriveId9876543210zz",
                                                           "name": "PL_131-2021-ND-CP_Phu_luc_I_Bieu_mau"}])
    _v5b, _d5b = _nlm_dedup_gate(_FakeNC5(_live5), "nb", [{"drive_id": _DGM, "name": "khac"}])
    _v5c, _d5c = _nlm_dedup_gate(_FakeNC5(_live5), "nb", [{"drive_id": "1XyzDriveId000000000000aa",
                                                           "name": "ND_131-2021-ND-CP_Nghi_dinh_chi_tiet_BLLD"}])
    cases.append(("r5_dedup_gate_sohieu_variant_clear", _v5a == "clear" and _d5a == []
                  and _v5b == "dup" and _d5b[0][1] == "s-main" and _v5c == "dup"))
    # (#7) register --row-kind: parser nhận own/overflow/ref, CHẶN giá trị lạ (SystemExit).
    _ap5 = build_parser()
    _ns5 = _ap5.parse_args(["register", "--drive-id", "d1", "--row-kind", "own"])
    with _hush():   # argparse in `usage… error: invalid choice: 'xyz'` = PASS-by-design (parser CHẶN đúng) — nuốt
        try:
            _ap5.parse_args(["register", "--drive-id", "d1", "--row-kind", "xyz"])
            _r5_bad = False
        except SystemExit:
            _r5_bad = True
    cases.append(("r5_register_row_kind_flag", _ns5.row_kind == "own" and _r5_bad))
    # (#9) ingest-local có cờ --skip-nlm-preflight (mặc định False = pre-check bật).
    _ns9 = _ap5.parse_args(["ingest-local", "x.docx"])
    cases.append(("r5_ingest_local_nlm_preflight_flag", getattr(_ns9, "skip_nlm_preflight", None) is False))
    cases.append(("source_map_qt5_hint_from_number_subject", any("thi dua khen thuong" in _strip_accents(q).lower() and "hop nhat" in _strip_accents(q).lower() for q in sm_tdk.get("qt5_search_hints", []))))
    cases.append(("vbhn_check_derives_subject_from_goc", any("thi dua khen thuong" in _strip_accents(q).lower() for q in _qt5_queries(_derive_subject_from_entries([rel_fx[0]]), "06/2022/QH15", ""))))
    cases.append(("vbhn_check_candidate", (_vbhn_candidates([
        {"id":"v14", "name":"VBHN_14-VBHN-VPQH_2024_An_toan_ve_sinh_lao_dong", "so_hieu":"14/VBHN-VPQH", "loai":"VBHN", "goc":"84/2015/QH13;41/2024/QH15", "cat":"20"}
    ], "an toàn vệ sinh lao động", "84/2015/QH13", "2024") or [{}])[0].get("id") == "v14"))
    good_vbhn = "VĂN BẢN HỢP NHẤT\nLuật An toàn, vệ sinh lao động\nSố 14/VBHN-VPQH năm 2024\nLuật số 84/2015/QH13 được sửa đổi, bổ sung bởi Luật số 41/2024/QH15."
    bad_vbhn = "VĂN BẢN HỢP NHẤT\nLuật Người lao động Việt Nam đi làm việc ở nước ngoài\nSố 14/VBHN-VPQH năm 2023\nLuật số 69/2020/QH14."
    cases.append(("vbhn_verify_good", _vbhn_verify_flags(good_vbhn, "an toàn vệ sinh lao động", ["84/2015/QH13", "41/2024/QH15"], "2024") == []))
    cases.append(("vbhn_verify_bad", {"EXPECT_TITLE_NOT_FOUND", "EXPECT_GOC_NOT_FOUND:84/2015/QH13", "EXPECT_YEAR_NOT_FOUND"} <= set(_vbhn_verify_flags(bad_vbhn, "an toàn vệ sinh lao động", ["84/2015/QH13"], "2024"))))
    cases.append(("vbhn_official_required_flags", {"OFFICIAL_SOURCE_NOT_CONFIRMED", "VBHN_FOOTNOTES_NOT_EVIDENT"} <= set(_vbhn_official_flags(good_vbhn, "", True))))
    official_53 = "VĂN BẢN HỢP NHẤT [1]\nĐiều 53. Trợ cấp\nCăn cứ khoản 1 Điều 90 của Luật này."
    assembled_53 = "VĂN BẢN HỢP NHẤT\nĐiều 53. Trợ cấp\nCăn cứ khoản 1 Điều 111 của Luật này. Căn cứ khoản 1 Điều 90 của Luật này."
    cmp53 = _vbhn_compare(official_53, assembled_53, ["Điều 53"])
    cases.append(("vbhn_compare_stale_ref", {"CANDIDATE_MISSING_FOOTNOTES", "FOCUS_REF_DIFF:Điều 53"} <= set(cmp53["flags"])))
    cases.append(("issue_year_not_from_goc_in_keywords", _entry_issue_year({"name":"VBHN_14-VBHN-VPQH_Luat_ATVSLD_HopNhat", "so_hieu":"14/VBHN-VPQH", "loai":"VBHN", "tukhoa":"Luật 84/2015/QH13 an toàn vệ sinh lao động"}) is None))
    cases.append(("issue_year_from_vbhn_name_separator", _entry_issue_year({"name":"VBHN_14-VBHN-VPQH_2024_Luat_ATVSLD_HopNhat", "so_hieu":"14/VBHN-VPQH", "loai":"VBHN", "tukhoa":"Luật 84/2015/QH13"}) == 2024))
    cases.append(("issue_year_from_issue_date", _entry_issue_year({"name":"VBHN_14-VBHN-VPQH_Luat_ATVSLD_HopNhat", "so_hieu":"14/VBHN/Vpqh", "loai":"VBHN", "ngay_ban_hanh":"Hà Nội, ngày 16/9/2024"}) == 2024))
    cases.append(("vbhn_name_year_must_match_issue_year", "VBHN_NAME_MISSING_YEAR" in _title_flags({"name":"VBHN_14-VBHN-VPQH_Luat_84-2015_ATVSLD_HopNhat", "so_hieu":"14/VBHN-VPQH", "loai":"VBHN", "issue_year":"2024"})))
    good_instruction = "\n".join([
        "SKILL_OF_RECORD tra-luat",
        "ingest_handoff research_import source_add(url) QT-3 notebook đang dùng docx official-first",
        "confirm_gate_web",
        "download_link_priority corpus_profile manifest_fallback cross_notebook_query nlm_notebook_id",
        "verify nguyên văn VBHN-first DỰ THẢO source id Điều",
    ])
    cases.append(("instruction_audit_good", _instruction_audit_text(good_instruction)["ok"]))
    cases.append(("instruction_audit_bad", not _instruction_audit_text("research_start có thể import nguồn vào notebook mới.")["ok"]))
    plan_bad = _external_ingest_plan("https://example.com/nd129.pdf", fmt="pdf", source_kind="secondary", action="research_import", notebook="new", confirm="")
    cases.append(("external_ingest_blocks_direct_nlm", {"DIRECT_NLM_IMPORT_FORBIDDEN", "RESEARCH_IMPORT_DISCOVERY_ONLY", "QT3_REQUIRED_BEFORE_NLM"} <= set(plan_bad["errors"])))
    cases.append(("external_ingest_blocks_new_notebook", "NEW_NOTEBOOK_OR_FOLDER_FORBIDDEN_BY_DEFAULT" in plan_bad["errors"]))
    plan_ok = _external_ingest_plan("https://congbao.chinhphu.vn/file.docx", fmt="docx", source_kind="official", action="qt3_plan", cat="02", folder="current", notebook="current", name="ND_129-2025-ND-CP", sohieu="129/2025/ND-CP", trichyeu="phan dinh tham quyen", confirm="yes")
    cases.append(("external_ingest_qt3_plan_ok", plan_ok["ok"] and plan_ok["format_class"] == "docx_convertible"))
    cases.append(("external_ingest_mentions_download_link_priority", any("TVPL" in s and "canonical" in s for s in plan_ok["required_steps"])))
    lp = _download_link_plan(["https://vbpl.vn/x", "https://thuvienphapluat.vn/y", "https://congbao.chinhphu.vn/z", "https://luatvietnam.vn/a"])
    cases.append(("download_link_priority_order", [x["source"] for x in lp[:3]] == ["thuvienphapluat.vn", "luatvietnam.vn", "congbao.chinhphu.vn"]))
    cfg2 = {"schema": 2, "webappUrl": "u", "token": "t", "defaultProfile": "vbqppl", "profiles": {
        "vbqppl": {"manifestId": "m1", "notebookId": "n1", "rootFolderId": "r1", "registryDocId": "g1"},
        "vbthuong": {"manifestId": "m2", "notebookId": "n2", "rootFolderId": "r2", "registryDocId": "g2"},
    }}
    prof = _apply_profile_env(cfg2, "vbthuong")
    cases.append(("profile_config_v2_overlay", prof["profile"] == "vbthuong" and os.environ.get("TL_MANIFEST_ID") == "m2" and os.environ.get("TL_NOTEBOOK_ID") == "n2"))
    cases.append(("profile_cache_separated", str(_cache_file("manifest.json")).replace("\\", "/").endswith(".tra_luat_cache/vbthuong/manifest.json") or "/vbthuong/manifest.json" in str(_cache_file("manifest.json")).replace("\\", "/")))
    # v1.19 (Cách B): profile KHÁC mặc định → forward registryDocId/manifestId vào mọi call webapp
    _sp = _scope_params()
    cases.append(("scope_params_forwarded_nonbase", _sp.get("registryDocId") == "g2" and _sp.get("manifestId") == "m2" and _sp.get("rootFolderId") == "r2" and _sp.get("profileName") == "vbthuong"))
    _sg = _ScopedGas(None)
    _m = _sg._merge({"q": "x"})
    cases.append(("scoped_gas_merge_adds_scope", _m.get("registryDocId") == "g2" and _m.get("manifestId") == "m2"))
    _m2 = _sg._merge({"registryDocId": "EXPLICIT"})
    cases.append(("scoped_gas_merge_keeps_explicit", _m2["registryDocId"] == "EXPLICIT"))
    _apply_profile_env(cfg2, "vbqppl")  # reset về mặc định: KHÔNG forward (dùng nền VBQPPL)
    cases.append(("scope_params_empty_for_default", _scope_params() == {}))

    # ═══ v1.30.0 (profile ops: A base-also / B discover / C adopt / D doctor / E index) — r6_* ═══
    from types import SimpleNamespace as _NS6
    cfg6 = {"schema": 2, "defaultProfile": "vbqppl", "profiles": {
        "vbqppl": {"manifestId": "m1", "notebookId": "n1", "rootFolderId": "r1", "registryDocId": "g1",
                   "overflowNotebookId": "n1b", "shards": ["n1", "n1b", "n1c"]},
        "p6": {"manifestId": "m6", "notebookId": "n6", "rootFolderId": "r6", "registryDocId": "g6", "categories": "own"},
        "p6off": {"manifestId": "m7", "notebookId": "n7", "rootFolderId": "r7", "registryDocId": "g7",
                  "categories": "own", "baseAlso": False},
    }}
    # (A) TL_BASE_ALSO: profile DỰ ÁN mặc định BẬT; opt-out config baseAlso=false; vbqppl KHÔNG set; CLI override thắng.
    _apply_profile_env(cfg6, "p6")
    cases.append(("r6_base_also_default_on_project", os.environ.get("TL_BASE_ALSO") == "1" and _base_also_enabled()))
    _apply_profile_env(cfg6, "p6off")
    cases.append(("r6_base_also_optout_config", os.environ.get("TL_BASE_ALSO") == "0" and not _base_also_enabled()))
    cases.append(("r6_base_also_cli_override", _base_also_enabled(_NS6(base_also=True))
                  and not _base_also_enabled(_NS6(base_also=False))))
    _apply_profile_env(cfg6, "vbqppl")
    cases.append(("r6_base_also_unset_on_default", "TL_BASE_ALSO" not in os.environ and not _base_also_enabled()))
    cases.append(("r6_vbqppl_notebooks_dedup", _vbqppl_notebooks(cfg6) == ["n1", "n1b", "n1c"]))
    _m6 = _merge_base_entries([{"id": "A", "drive_id": "A"}, {"id": "B", "drive_id": "B"}],
                              [{"id": "B", "drive_id": "B"}, {"id": "C", "drive_id": "C"}])
    cases.append(("r6_merge_base_entries_dedup_order",
                  [_entry_drive_id(e) for e in _m6] == ["A", "B", "C"] and _m6[2].get("_scope") == "vbqppl"
                  and "_scope" not in _m6[0]))
    # (A) _base_manifest_entries KHÔI PHỤC env overlay profile (kể cả TL_BASE_ALSO) dù đọc nền lỗi/thành công.
    _apply_profile_env(cfg6, "p6")
    with _hush():   # có thể chạm LIVE (cache miss → gas-retry/gws-fallback GWS_CRED_EXPIRED) — test chỉ cần env-restore
        _ents6, _err6 = _base_manifest_entries(None)
    cases.append(("r6_base_entries_restores_env", isinstance(_ents6, list) and (_err6 is None or isinstance(_err6, str))
                  and os.environ.get("TL_PROFILE") == "p6" and os.environ.get("TL_REGISTRY_DOC_ID") == "g6"
                  and os.environ.get("TL_BASE_ALSO") == "1"))
    _apply_profile_env(cfg6, "vbqppl")
    # (B) phân loại item Drive — khoan dung biến thể tên thật (Registry_NQ36 / _manifest_DinhMucChi.json / bare).
    cases.append(("r6_discover_item_kinds",
                  _discover_item_kind({"name": "Registry_NQ36", "mime": REGISTRY_SHEET_MIME, "type": "file"}) == "registry"
                  and _discover_item_kind({"name": "tra_luat_registry", "mime": "application/vnd.google-apps.document", "type": "file"}) == "registry_nonsheet"
                  and _discover_item_kind({"name": "tra_luat_registry.X.csv", "mime": "text/csv", "type": "file"}) == "registry_csv"
                  and _discover_item_kind({"name": "_manifest_DinhMucChi.json", "mime": "application/json", "type": "file"}) == "manifest"
                  and _discover_item_kind({"name": "_PROFILES_INDEX", "mime": REGISTRY_SHEET_MIME, "type": "file"}) == "index"
                  and _discover_item_kind({"name": "BC_khao_sat.docx", "mime": "application/x", "type": "file"}) == "other"
                  and _discover_item_kind({"name": "sub", "mime": "application/vnd.google-apps.folder", "type": "folder"}) == "folder"))
    _fx6_folders = [
        {"id": "F1", "name": "Luat_BHXH", "items": [
            {"id": "R1", "name": "tra_luat_registry.LuatBHXH", "mime": REGISTRY_SHEET_MIME, "type": "file"},
            {"id": "M1", "name": "tra_luat_manifest.LuatBHXH.json", "mime": "application/json", "type": "file"}]},
        {"id": "F2", "name": "Định mức chi", "items": [
            {"id": "R2", "name": "tra_luat_registry.DinhMucChi", "mime": REGISTRY_SHEET_MIME, "type": "file"},
            {"id": "M2", "name": "_manifest_DinhMucChi.json", "mime": "application/json", "type": "file"}]},
        {"id": "F3", "name": "Khảo sát Luật XB", "items": []},
        {"id": "F4", "name": "Khảo sát Luật Xuất bản", "items": [
            {"id": "D1", "name": "BC_khao_sat.docx", "mime": "application/x-docx", "type": "file"}]},
    ]
    _fx6_root = [
        {"id": "RG36", "name": "Registry_NQ36", "mime": REGISTRY_SHEET_MIME, "type": "file"},
        {"id": "MN36", "name": "tra_luat_manifest.NQ36.json", "mime": "application/json", "type": "file"},
        {"id": "IDX", "name": "_PROFILES_INDEX", "mime": REGISTRY_SHEET_MIME, "type": "file"},
        {"id": "RVBT", "name": "tra_luat_registry", "mime": REGISTRY_SHEET_MIME, "type": "file"},
    ]
    _fx6_profiles = {"vbqppl": {"rootFolderId": "r1"},
                     "LuatBHXH": {"rootFolderId": "F1", "registryDocId": "R1", "manifestId": "M1"},
                     "vbthuong": {"rootFolderId": "VBT", "registryDocId": "RVBT", "manifestId": "MVBT"},
                     "ghost": {"rootFolderId": "FX"}}
    _dc6 = _discover_classify(_fx6_folders, _fx6_root, _fx6_profiles, vbt_id="VBT")
    _st6 = {r["folder_id"]: r["status"] for r in _dc6["folders"]}
    cases.append(("r6_discover_classify_buckets",
                  _st6 == {"F1": "in_config", "F2": "unregistered_profile", "F3": "empty_folder", "F4": "plain_folder"}))
    cases.append(("r6_discover_suggest_adopt",
                  len(_dc6["unregistered"]) == 1
                  and "profile-adopt --name Dinh_muc_chi --folder F2 --registry R2 --manifest M2" in _dc6["unregistered"][0]["suggest"]))
    cases.append(("r6_discover_misplaced_root_assets",
                  {m["id"] for m in _dc6["misplaced_root_assets"]} == {"RG36", "MN36"}))
    cases.append(("r6_discover_config_only_skips_vbt_root",
                  [c["profile"] for c in _dc6["config_only"]] == ["ghost"]))
    # (C) adopt: chọn asset đơn trị; nhiều registry → AMBIGUOUS; tên-registry-không-Sheet → chặn; override thắng.
    _pk6 = _adopt_pick_assets(_fx6_folders[0]["items"])
    cases.append(("r6_adopt_pick_single", (_pk6["registry"] or {}).get("id") == "R1"
                  and (_pk6["manifest"] or {}).get("id") == "M1" and not _pk6["errors"]))
    _pk6b = _adopt_pick_assets(_fx6_folders[0]["items"]
                               + [{"id": "R9", "name": "tra_luat_registry.copy", "mime": REGISTRY_SHEET_MIME, "type": "file"}])
    cases.append(("r6_adopt_pick_ambiguous", any(x.startswith("REGISTRY_AMBIGUOUS") for x in _pk6b["errors"])))
    _pk6c = _adopt_pick_assets([{"id": "RD", "name": "tra_luat_registry", "mime": "application/vnd.google-apps.document", "type": "file"}])
    cases.append(("r6_adopt_blocks_nonsheet_registry", _pk6c["registry"] is None
                  and any(x.startswith("REGISTRY_NOT_SHEET") for x in _pk6c["errors"])))
    _pk6d = _adopt_pick_assets([], reg_override="RX", man_override="MX")
    cases.append(("r6_adopt_override_wins", (_pk6d["registry"] or {}).get("id") == "RX"
                  and (_pk6d["manifest"] or {}).get("id") == "MX" and not _pk6d["errors"]))
    _pk6e = _adopt_pick_assets([{"id": "R1", "name": "tra_luat_registry.X", "mime": REGISTRY_SHEET_MIME, "type": "file"},
                                {"id": "MA", "name": "tra_luat_manifest.X.json", "mime": "application/json", "type": "file"},
                                {"id": "MB", "name": "_manifest_X.json", "mime": "application/json", "type": "file"}])
    cases.append(("r6_adopt_manifest_prefers_standard", (_pk6e["manifest"] or {}).get("id") == "MA" and not _pk6e["errors"]))
    # (D) doctor: bất biến layout (registry/manifest trong root|_meta) + legacy-Doc critical + thiếu id.
    _prof6 = {"rootFolderId": "F1", "metaFolderId": "MT1", "notebookId": "n6", "registryDocId": "R1", "manifestId": "M1"}
    _inf6_ok = {"R1": {"mimeType": REGISTRY_SHEET_MIME, "parents": ["MT1"], "trashed": False},
                "M1": {"mimeType": "application/json", "parents": ["F1"], "trashed": False}}
    cases.append(("r6_doctor_clean", _doctor_check_profile("p", _prof6, _inf6_ok) == []))
    _inf6_mis = {"R1": {"mimeType": REGISTRY_SHEET_MIME, "parents": ["VBT"], "trashed": False},
                 "M1": {"mimeType": "application/json", "parents": ["F1"], "trashed": False}}
    _fd6 = _doctor_check_profile("p", _prof6, _inf6_mis)
    cases.append(("r6_doctor_misplaced_fix_to_meta",
                  any(x.get("check") == "MISPLACED_ASSET" and (x.get("fix") or {}).get("to") == "MT1" for x in _fd6)))
    _fd6b = _doctor_check_profile("p", dict(_prof6, registryDocId=_LEGACY_REGISTRY_DOC_ID), _inf6_ok)
    cases.append(("r6_doctor_legacy_doc_critical",
                  any(x.get("check") == "REGISTRY_LEGACY_DOC" and x.get("severity") == "critical" for x in _fd6b)))
    _fd6c = _doctor_check_profile("p", {"rootFolderId": "F1"}, {})
    cases.append(("r6_doctor_missing_ids",
                  any(x.get("check") == "NO_REGISTRY_ID" and x.get("severity") == "critical" for x in _fd6c)
                  and any(x.get("check") == "NO_NOTEBOOK_ID" for x in _fd6c)))
    # (E) index: BẢN CHIẾU từ config — default marker, folder_name map, cột baseAlso, CSV header đúng thứ tự cột.
    _rows6 = _profile_index_rows(cfg6, folder_names={"r6": "P6_folder"})
    _rmap6 = {r["profile"]: r for r in _rows6}
    cases.append(("r6_index_rows_from_config",
                  _rmap6["vbqppl"]["default"] == "yes" and _rmap6["p6"]["folder_name"] == "P6_folder"
                  and _rmap6["p6"]["baseAlso"] == "on" and _rmap6["p6off"]["baseAlso"] == "off"
                  and _rmap6["vbqppl"]["baseAlso"] == ""))
    _csv6 = _profile_index_csv(_rows6)
    cases.append(("r6_index_csv_header", _csv6.splitlines()[0] == ",".join(_PROFILES_INDEX_COLS)
                  and len([x for x in _csv6.splitlines() if x.strip()]) == 1 + len(_rows6)))
    # (wiring) parser: cờ base-also trên lệnh đọc + 3 lệnh profile mới nhận đúng flags.
    _ap6 = build_parser()
    _ns6a = _ap6.parse_args(["locate", "q"])
    _ns6b = _ap6.parse_args(["reg-query", "--no-base-also"])
    _ns6c = _ap6.parse_args(["profile-adopt", "--name", "x", "--folder", "f", "--bootstrap-manifest"])
    _ns6d = _ap6.parse_args(["profile-doctor", "--fix"])
    _ns6e = _ap6.parse_args(["profile-index", "--rebuild"])
    _ns6f = _ap6.parse_args(["profile-list", "--discover", "--folder-cap", "99"])
    cases.append(("r6_parser_wiring",
                  getattr(_ns6a, "base_also", "MISSING") is None and _ns6b.base_also is False
                  and _ns6c.bootstrap_manifest is True and _ns6d.fix is True and _ns6e.rebuild is True
                  and _ns6f.discover is True and _ns6f.folder_cap == 99))
    # ═══ v1.30.0 review đối kháng — 8 finding CONFIRMED → vá + test ═══
    # (fix1) profile KHÔNG tồn tại trong config rơi về data NỀN → KHÔNG set TL_BASE_ALSO (hết nền tự quét mình 2 lần).
    _apply_profile_env(cfg6, "khong_ton_tai_trong_config")
    cases.append(("r6_base_also_not_set_unknown_profile",
                  "TL_BASE_ALSO" not in os.environ and not _base_also_enabled()))
    _apply_profile_env(cfg6, "vbqppl")
    # (fix5/6) asset dùng chung ≥2 profile: owners map + doctor BỎ fix-move, nâng SHARED_ASSET_MULTI_PROFILE critical.
    _shared_profs = {"P1": {"registryDocId": "R1", "manifestId": "M1"},
                     "P2": {"registryDocId": "R1", "manifestId": "M2"},
                     "P3": {"registryDocId": "R3"}}
    cases.append(("r6_profile_asset_owners", _profile_asset_owners(_shared_profs, "R1") == ["P1", "P2"]
                  and _profile_asset_owners(_shared_profs, "R3") == ["P3"]
                  and _profile_asset_owners(_shared_profs, "") == []))
    _sf = _strip_shared_fixes([{"check": "MISPLACED_ASSET", "severity": "warn", "profile": "P1", "fileId": "R1",
                                "fix": {"action": "move", "fileId": "R1", "to": "MT"}},
                               {"check": "MISPLACED_ASSET", "severity": "warn", "profile": "P3", "fileId": "R3",
                                "fix": {"action": "move", "fileId": "R3", "to": "MT3"}}], _shared_profs)
    cases.append(("r6_doctor_strips_shared_fix",
                  _sf[0].get("check") == "SHARED_ASSET_MULTI_PROFILE" and _sf[0].get("severity") == "critical"
                  and "fix" not in _sf[0] and _sf[0].get("owners") == ["P1", "P2"]
                  and _sf[1].get("check") == "MISPLACED_ASSET" and _sf[1].get("fix")))
    # (fix4) manifest lạ (profile ≠ tên adopt) KHÔNG được cấp notebookId; manifest đúng/không ghi profile → lấy bình thường.
    _nb1, _w1 = _notebook_from_manifest_json({"profile": "P_khac", "notebookId": "nb_x"}, "P_dang_adopt")
    _nb2, _w2 = _notebook_from_manifest_json({"profile": "Định mức chi", "notebookId": "nb_ok"}, "Dinh_muc_chi")
    _nb3, _w3 = _notebook_from_manifest_json({"notebookId": "nb_bare"}, "P1")
    cases.append(("r6_manifest_notebook_profile_mismatch",
                  _nb1 == "" and (_w1 or "").startswith("MANIFEST_PROFILE_MISMATCH")
                  and _nb2 == "nb_ok" and _w2 is None and _nb3 == "nb_bare" and _w3 is None))
    # (fix7) index chỉ dọn TÊN CHÍNH XÁC — file người dùng `_PROFILES_INDEX_backup…` KHÔNG bị trash.
    _oc = _index_old_candidates([{"id": "1", "name": "_PROFILES_INDEX"}, {"id": "2", "name": "_PROFILES_INDEX.csv"},
                                 {"id": "3", "name": "_PROFILES_INDEX_backup_2026.csv"}, {"id": "4", "name": "khac.csv"}])
    cases.append(("r6_index_old_exact_names", [x["id"] for x in _oc] == ["1", "2"]))
    # (fix3) _ProfileEnvGuard: lệnh profile-ops ép scope nền bên trong nhưng KHÔI PHỤC env caller (kể cả khi lỗi).
    _apply_profile_env(cfg6, "p6")
    try:
        with _ProfileEnvGuard():
            _apply_profile_env(cfg6, "vbqppl")
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    cases.append(("r6_profile_env_guard_restores",
                  os.environ.get("TL_PROFILE") == "p6" and os.environ.get("TL_REGISTRY_DOC_ID") == "g6"
                  and os.environ.get("TL_BASE_ALSO") == "1"))
    _apply_profile_env(cfg6, "vbqppl")

    # ═══ v1.30.1 (xử log LIVE 2026-07-03: #1 nlm-install 45s / #7 corpus lệch / #4 loai phi-chuẩn) — r7_* ═══
    # (#1) máy trạng thái cài nlm: bước kế dò từ ĐĨA (fetch→extract→install→done), idempotent.
    import tempfile as _tf7
    from pathlib import Path as _P7
    _tlg7 = _imp("tl_gws")
    with _tf7.TemporaryDirectory() as _d7:
        _st7 = _tlg7._nlm_install_probe(home=_d7, nlm_path="")
        _ok7a = _st7["next_step"] == "fetch" and not _st7["have_tgz"] and not _st7["have_pybin"]
        _P7(_st7["tgz"]).parent.mkdir(parents=True, exist_ok=True)
        _P7(_st7["tgz"]).write_bytes(b"x")
        _ok7b = _tlg7._nlm_install_probe(home=_d7, nlm_path="")["next_step"] == "extract"
        _P7(_st7["pybin"]).parent.mkdir(parents=True, exist_ok=True)
        _P7(_st7["pybin"]).write_bytes(b"x")
        _ok7c = _tlg7._nlm_install_probe(home=_d7, nlm_path="")["next_step"] == "install"
        _ok7d = _tlg7._nlm_install_probe(home=_d7, nlm_path="/x/nlm")["next_step"] == "done"
    cases.append(("r7_nlm_install_probe_steps", _ok7a and _ok7b and _ok7c and _ok7d))
    cases.append(("r7_nlm_install_step_rc_map", _tlg7._NLM_STEP_RC == {"fetch": 2, "extract": 4, "install": 5}))
    # (#7) 2 thước đo corpus: client corpus=='true' vs luật server GAS (vbqppl/overflow đếm; ref/thuong loại).
    _ents7 = [
        {"corpus": "true", "row_kind": "own", "loai": "Luật"},     # cả 2 thước đếm
        {"corpus": "vbqppl", "row_kind": "own", "loai": ""},       # CHỈ server
        {"corpus": "false", "row_kind": "overflow", "loai": ""},   # CHỈ server (overflow)
        {"corpus": "true", "row_kind": "ref", "loai": ""},         # CHỈ client (server loại ref)
        {"corpus": "true", "row_kind": "own", "loai": "thuong"},   # CHỈ client (server loại thuong — EXACT match)
        {"corpus": "false", "row_kind": "own", "loai": ""},        # không ai đếm
        {"corpus": "true", "row_kind": "own", "loai": "Thuong"},   # CẢ 2 (review: GAS exact 'thuong' — 'Thuong' hoa VẪN đếm)
    ]
    cases.append(("r7_corpus_count_server_rule", _corpus_count_server_rule(_ents7) == 4
                  and _corpus_count_server_rule([_ents7[0], _ents7[3], _ents7[4]]) == 1))
    _rep7 = _sweep_report([{"id": "a1", "drive_id": "a1", "name": "Luat_12-2025-QH15_X",
                            "so_hieu": "12/2025/QH15", "corpus": "true", "row_kind": "own", "loai": "Luật"}])
    cases.append(("r7_sweep_two_measures_fields", _rep7.get("corpus") == 1
                  and _rep7.get("corpus_server_rule_equiv") == 1 and isinstance(_rep7.get("corpus_basis"), dict)
                  and "regIsCorpusCounted_" in _rep7["corpus_basis"]["corpus_server_rule_equiv"]))
    # (#4) backfill-loai: mặc định CHỈ điền dòng RỖNG; --normalize sửa dòng SAI enum map tất định; giá trị lạ → báo.
    _sug7, _uns7, _non7 = _backfill_loai_candidates([
        {"id": "e1", "drive_id": "e1", "name": "Luat_12-2025-QH15_X", "so_hieu": "12/2025/QH15", "loai": ""},
        {"id": "e2", "drive_id": "e2", "name": "abc", "loai": "Luat"},
        {"id": "e3", "drive_id": "e3", "name": "def", "loai": "loai-la-khong-map-duoc"},
        {"id": "e4", "drive_id": "e4", "name": "ghi", "loai": "Luật"},
    ], normalize=True)
    cases.append(("r7_backfill_loai_normalize",
                  any(s["drive_id"] == "e2" and s["loai"] == "Luật" and s.get("mode") == "normalize" for s in _sug7)
                  and any(s["drive_id"] == "e1" and s.get("mode") == "fill" for s in _sug7)
                  and [x["drive_id"] for x in _non7] == ["e3"]
                  and all(s["drive_id"] != "e4" for s in _sug7) and _uns7 == 0))
    _sug7b, _uns7b, _non7b = _backfill_loai_candidates([{"id": "e2", "drive_id": "e2", "name": "abc", "loai": "Luat"}],
                                                       normalize=False)
    cases.append(("r7_backfill_loai_default_skips_nonempty", _sug7b == [] and _non7b == [] and _uns7b == 0))
    cases.append(("r7_normalize_loai_map", _normalize_loai("Luat") == "Luật" and _normalize_loai("vbhn") == "Văn bản hợp nhất"
                  and _normalize_loai("Cong dien") == "Công điện" and _normalize_loai("Công điện") == "Công điện"
                  and _normalize_loai("CD") == "Công điện"))     # review: CD ∈ họ canonical → phải map, không nonmappable
    # wiring parser
    _ap7 = build_parser()
    _n7a = _ap7.parse_args(["nlm-install", "--resume", "--version", "0.5.0"])
    _n7b = _ap7.parse_args(["backfill-loai", "--normalize"])
    cases.append(("r7_parser_wiring", _n7a.resume is True and _n7a.version == "0.5.0" and _n7b.normalize is True))

    # ═══ v1.31.0 (backlog P0/P1 log rà 68 Luật 2026-07-03) — r8_* ═══
    # (P0-1) guard tên-file + pretty-tail + đảo ưu tiên title-first + cờ không-dấu.
    cases.append(("r8_looks_like_filename_title",
                  _looks_like_filename_title("Luat_100-2015-QH13_Bo_Luat_Hinh_su")
                  and _looks_like_filename_title("VBHN_121-VBHN-VPQH_2025_Luat_HNGD")
                  and not _looks_like_filename_title("Luật Hôn nhân và gia đình")
                  and not _looks_like_filename_title("Bộ luật Hình sự")
                  and not _looks_like_filename_title("")))
    cases.append(("r8_name_tail_pretty_keeps_case",
                  _name_tail_pretty("Luat_100-2015-QH13_Bo_Luat_Hinh_su") == "Bo Luat Hinh su"
                  # review v1.31.0: SO CHÍNH XÁC (endswith từng che year-leak '2025 Luat …') + năm sau sohieu phải bị bóc
                  and _name_tail_pretty("VBHN_121-VBHN-VPQH_2025_Luat_Hon_nhan_va_gia_dinh") == "Luat Hon nhan va gia dinh"
                  and _name_tail_pretty("ND_131-2021-ND-CP_Nghi_dinh_chi_tiet_BLLD") == "Nghi dinh chi tiet BLLD"))
    cases.append(("r8_derive_subject_prefers_diacritic_title",
                  _derive_subject_from_entries([{"name": "Luat_100-2015-QH13_Bo_Luat_Hinh_su",
                                                 "title_vn": "Bộ luật Hình sự"}]) == "Bộ luật Hình sự"
                  and _derive_subject_from_entries([{"name": "Luat_100-2015-QH13_Bo_Luat_Hinh_su",
                                                     "nlm_title": "Luat_100-2015-QH13_Bo_Luat_Hinh_su"}]) == "Bo Luat Hinh su"))
    cases.append(("r8_has_diacritics", _has_diacritics("Bộ luật Hình sự") and not _has_diacritics("Bo luat Hinh su")
                  and not _has_diacritics("")))
    # (P0-1) _title_vn_from_header: header IN HOA có dấu → 'Loại + Chủ đề'; mất dấu/boilerplate → skip loud.
    _h8 = "LUẬT\nPHÒNG, CHỐNG BỆNH TRUYỀN NHIỄM\nCăn cứ Hiến pháp...\nĐiều 1. Phạm vi điều chỉnh"
    _tv8, _w8 = _title_vn_from_header(_h8, {"name": "Luat_Phong_chong_benh_truyen_nhiem", "loai": "Luật"})
    cases.append(("r8_title_vn_from_header_diacritic",
                  _tv8.startswith("Luật ") and _has_diacritics(_tv8) and _w8 == ""))
    _tv8b, _w8b = _title_vn_from_header("LUAT\nDAU THAU\nDieu 1.", {"name": "luat-dau-thau.html", "loai": ""})
    cases.append(("r8_title_vn_skips_no_diacritics", _tv8b == "" and _w8b in ("NO_DIACRITICS", "NO_SUBJECT", "BOILERPLATE")))
    _c8 = _backfill_titlevn_candidates([
        {"drive_id": "a", "name": "Luat_A", "corpus": "true", "row_kind": "own", "title_vn": ""},
        {"drive_id": "b", "name": "Luat_B", "corpus": "true", "row_kind": "own", "title_vn": "Luật B thật"},
        {"drive_id": "c", "name": "Luat_C", "corpus": "false", "row_kind": "own", "title_vn": ""},
        {"drive_id": "d", "name": "Luat_D", "corpus": "true", "row_kind": "ref", "title_vn": ""},
    ])
    cases.append(("r8_backfill_titlevn_candidates", [x["drive_id"] for x in _c8] == ["a"]))
    _c8f = _backfill_titlevn_candidates([
        {"drive_id": "e", "name": "Luat_E", "corpus": "true", "row_kind": "own", "title_vn": "Luat_100-2015-QH13_X"},
        {"drive_id": "f", "name": "Luat_F", "corpus": "true", "row_kind": "own", "title_vn": "Luật F chuẩn"},
    ], force=True)
    cases.append(("r8_backfill_titlevn_force_skips_real_title", [x["drive_id"] for x in _c8f] == ["e"]))
    # (P0-3) cấu trúc tên độc lập header — 3 ca log fire, tên chuẩn KHÔNG fire.
    cases.append(("r8_name_structural_issues",
                  "FILE_EXTENSION" in _name_structural_issues("luat-dau-thau-2023-so-22-2023-qh15-moi-nhat.html")
                  and "NO_SOHIEU_IN_NAME" in _name_structural_issues("Luat_Phong_chong_benh_truyen_nhiem")
                  and "NO_SUBJECT_TOKENS" in _name_structural_issues("Luat_64-2006-QH11")
                  and _name_structural_issues("Luat_113-2025-QH15_Dan_so") == []
                  and _name_structural_issues("VBHN_14-VBHN-VPQH_2024_Luat_An_toan_ve_sinh_lao_dong") == []))
    # (P0-2) CAT_LIKELY_WRONG: cat có giá trị + suy-nội-dung high ra cat khác → REVIEW proposal (không auto).
    _e8 = {"id": "x8", "drive_id": "x8", "name": "Luat_143-2025-QH15_Dau_tu", "so_hieu": "143/2025/QH15",
           "sohieu": "143/2025/QH15", "loai": "Luật", "cat": "45_Y_te_duoc", "corpus": "true", "row_kind": "own"}
    _hdr8 = ("LUẬT\nĐẦU TƯ\nSố: 143/2025/QH15\nngày 15 tháng 6 năm 2025\n"
             "Điều 1. Phạm vi điều chỉnh\nLuật này quy định về hoạt động đầu tư kinh doanh tại Việt Nam, "
             "ngành nghề đầu tư kinh doanh có điều kiện, ưu đãi đầu tư, dự án đầu tư.")
    _ar8 = _corpus_audit_row(_e8, _hdr8)
    _clw8 = [p for p in _ar8["proposals"] if p["type"] == "CAT_LIKELY_WRONG"]
    cases.append(("r8_cat_likely_wrong_fires", len(_clw8) == 1 and "REVIEW" in _clw8[0]["fix_command"]))
    _e8ok = dict(_e8, cat="34_Xay_dung_nha_o_do_thi")   # alias chính thức 'đầu tư'→34 (khớp gợi ý backlog cho Luật 57-2024)
    _ar8b = _corpus_audit_row(_e8ok, _hdr8)
    cases.append(("r8_cat_likely_wrong_silent_when_cat_matches",
                  not any(p["type"] == "CAT_LIKELY_WRONG" for p in _ar8b["proposals"])))
    cases.append(("r8_name_nonstandard_proposal",
                  any(p["type"] == "NAME_NONSTANDARD" for p in _corpus_audit_row(
                      {"id": "y8", "drive_id": "y8", "name": "Luat_64-2006-QH11", "so_hieu": "64/2006/QH11",
                       "loai": "Luật", "cat": "19", "corpus": "true", "row_kind": "own"},
                      "LUẬT\nCÔNG NGHỆ THÔNG TIN\nSố: 64/2006/QH11")["proposals"])))
    # (P1-8) điều ước quốc tế: nhận diện + KHÔNG NAME_NONSTANDARD + tách khỏi orphans trong hygiene.
    _tr8 = {"id": "t8", "drive_id": "t8", "name": "CU_ILO-105_Xoa_bo_lao_dong_cuong_buc", "so_hieu": "",
            "sohieu": "", "loai": "", "cat": "23_Ngoai_giao_dieu_uoc_quoc_te", "corpus": "true", "row_kind": "own"}
    cases.append(("r8_treaty_detect", _is_treaty_entry(_tr8)
                  and _is_treaty_entry({"name": "Cong_uoc_Vien_1980", "loai": ""})
                  and not _is_treaty_entry({"name": "Luat_113-2025-QH15_Dan_so", "loai": "Luật"})))
    _hg8 = _hygiene_groups([_tr8, {"id": "o8", "drive_id": "o8", "name": "van_ban_la_khong_so", "so_hieu": "",
                                   "sohieu": "", "loai": "", "cat": "19", "corpus": "true", "row_kind": "own"}])
    cases.append(("r8_treaty_not_orphan",
                  all(_entry_drive_id(x) != "t8" for x in _hg8["orphans"])
                  and any(_entry_drive_id(x) == "t8" for x in _hg8["treaties"])
                  and any(_entry_drive_id(x) == "o8" for x in _hg8["orphans"])))
    # (P1-6) quarantine still_on_nlm = LIVE (loại removed*), nlm_source_id sót → stale_nlm_ref.
    _q8 = [{"id": "q1", "drive_id": "q1", "name": "A", "cat": QUARANTINE_CAT, "corpus": "false",
            "nlm_source_id": "s1", "nlm_status": "pushed", "row_kind": "own"},
           {"id": "q2", "drive_id": "q2", "name": "B", "cat": QUARANTINE_CAT, "corpus": "false",
            "nlm_source_id": "s2", "nlm_status": "removed_below_nd", "row_kind": "own"}]
    _sw8 = _sweep_report(_q8)
    cases.append(("r8_sweep_still_on_nlm_live",
                  _sw8["quarantine"]["still_on_nlm"] == 1 and _sw8["quarantine"]["stale_nlm_ref"] == 1
                  and isinstance(_sw8.get("treaties"), int)))
    # (P1-4) VBHN cấp Bộ không được làm candidate của Luật QH khi thiếu goc-chain; VPQH/goc-match giữ nguyên.
    cases.append(("r8_vbhn_agency_mismatch_helper",
                  _vbhn_agency_mismatch("90-2025-QH15", {"name": "VBHN_4231-2025-VBHN-BTP_ND_xu_ly", "so_hieu": "4231/2025/VBHN-BTP"})
                  and not _vbhn_agency_mismatch("90-2025-QH15", {"name": "VBHN_121-VBHN-VPQH_2025_HNGD", "so_hieu": "121/VBHN-VPQH"})
                  and not _vbhn_agency_mismatch("187-2025-ND-CP", {"name": "VBHN_4231-2025-VBHN-BTP_ND", "so_hieu": "4231/2025/VBHN-BTP"})))
    _vc8 = _vbhn_candidates([
        {"id": "m8", "drive_id": "m8", "name": "VBHN_4231-2025-VBHN-BTP_Nghi_dinh_dau_tu", "so_hieu": "4231/2025/VBHN-BTP",
         "loai": "Văn bản hợp nhất", "cat": "26", "corpus": "true", "row_kind": "own", "goc": "",
         "tukhoa": "đầu tư kinh doanh"},
    ], subject="đầu tư", goc="90/2025/QH15", year="2025")
    cases.append(("r8_vbhn_candidates_agency_gate", _vc8 == []))
    _vc8b = _vbhn_candidates([
        {"id": "v8", "drive_id": "v8", "name": "VBHN_12-VBHN-VPQH_2025_Luat_Dau_tu", "so_hieu": "12/VBHN-VPQH",
         "loai": "Văn bản hợp nhất", "cat": "26", "corpus": "true", "row_kind": "own", "goc": "90/2025/QH15",
         "tukhoa": "đầu tư kinh doanh"},
    ], subject="đầu tư", goc="90/2025/QH15", year="2025")
    cases.append(("r8_vbhn_candidates_vpqh_kept", len(_vc8b) == 1))
    # (P1-5) vocab thống nhất: relation-audit có verdict/flags/qt5_queries; source-map item có alias qt5_queries.
    _ra8 = _relation_audit([], base="90/2025/QH15", subject="đầu tư", amendments=[], footnote_amend_keys=[])
    cases.append(("r8_relation_audit_vocab",
                  _ra8.get("verdict") in ("OK", "REVIEW", "QT5_WEB_REQUIRED") and isinstance(_ra8.get("flags"), list)
                  and _ra8.get("qt5_queries") == _ra8.get("vbhn_queries")))
    _sm8 = _source_map_one("Luật Đầu tư", [])
    cases.append(("r8_source_map_qt5_alias", _sm8.get("qt5_queries") == _sm8.get("qt5_search_hints")))
    # (P1-7) sweep --verbose parser + backfill-title-vn parser wiring.
    _ap8 = build_parser()
    _n8a = _ap8.parse_args(["sweep", "--verbose"])
    _n8b = _ap8.parse_args(["backfill-title-vn", "--limit", "5", "--offset", "40", "--force-refresh"])
    cases.append(("r8_parser_wiring", _n8a.verbose is True and _n8b.limit == 5 and _n8b.offset == 40
                  and _n8b.force_refresh is True))

    # ═══ v1.31.1 (log phiên rà 68 Luật — vòng 2: N1 at-ingest / N2 tukhoa tier / N3 alias-strict / N4 sweep) — r9_* ═══
    cases.append(("r9_tukhoa_title_extract",
                  _title_vn_from_tukhoa("Phạm vi điều chỉnh của Bộ luật hình sự Điều 2 Giải thích",
                                        "Luat_100-2015-QH13_Bo_Luat_Hinh_su") == "Bộ luật Hình sự"
                  and _title_vn_from_tukhoa("Luật Đầu tư và các luật có liên quan", "Luat_143-2025-QH15_Dau_tu") == "Luật Đầu tư"
                  and _title_vn_from_tukhoa("Luật Bảo hiểm xã hội năm", "Luat_41-2024-QH15_Bao_hiem_xa_hoi") == "Luật Bảo hiểm xã hội"))
    cases.append(("r9_tukhoa_abbrev_crosscheck",   # bài học #2 log: CNTT phải khớp nhờ _ABBREV_MAP mở rộng (hết false-reject)
                  _title_vn_from_tukhoa("Luật công nghệ thông tin quy định", "Luat_67-2006-QH11_CNTT") == "Luật Công nghệ thông tin"))
    cases.append(("r9_tukhoa_rejects",
                  _title_vn_from_tukhoa("Luật Mặt trận tổ quốc", "Luat_113-2025-QH15_Dan_so") == ""      # méo/khác luật
                  and _title_vn_from_tukhoa("Luat Dau tu khong dau", "Luat_143-2025-QH15_Dau_tu") == ""   # không dấu
                  and _title_vn_from_tukhoa("", "Luat_x") == ""))
    cases.append(("r9_tukhoa_heading_split_not_lowercase_dj",   # 'đ' thường ∈ dải À-Ỹ từng bị coi là HOA → cắt giữa 'quy định'
                  _title_vn_from_tukhoa("Luật Thủ đô quy định", "Luat_39-2024-QH15_Thu_do") == "Luật Thủ đô"))
    # review v1.31.1 (CONFIRMED): split theo TỪ-KHÓA heading — tukhoa Title-Case không còn cụt còn 1 từ;
    # tên có danh-từ-riêng viết Hoa giữa chừng (Tổ quốc Việt Nam) không bị cắt.
    cases.append(("r9_tukhoa_titlecase_not_truncated",
                  _title_vn_from_tukhoa("Luật Bảo Hiểm Xã Hội Điều 2 Giải thích",
                                        "Luat_41-2024-QH15_Bao_hiem_xa_hoi") == "Luật Bảo Hiểm Xã Hội"
                  and _title_vn_from_tukhoa("Luật Mặt trận Tổ quốc Việt Nam Điều 1",
                                            "Luat_75-2015-QH13_Mat_tran_To_quoc") == "Luật Mặt trận Tổ quốc Việt Nam"))
    cases.append(("r9_expected_cat_alias",   # ca thật log: 143-2025 Đầu tư→34, 46-2024 Công chứng→04; boundary vốn-NN nhường
                  _expected_cat_from_alias("Dau tu")[0] == "34" and _expected_cat_from_alias("Cong chung")[0] == "04"
                  and _expected_cat_from_alias("dau tu von nha nuoc tai doanh nghiep") == ("", "")
                  and _expected_cat_from_alias("") == ("", "")))
    # v1.31.2 (FP thật phiên rà): Luật CNTT phải ra 03 POSITIVE (không phải 19 qua alias 'cong nghe' trần, không im lặng);
    # 'cong nghe' trần = blacklist; alias 19 đặc thù (khoa hoc cong nghe) vẫn sống.
    cases.append(("r9_expected_cat_cntt_boundary",
                  _expected_cat_from_alias("Cong nghe thong tin") == ("03", "cong nghe thong tin")
                  and _expected_cat_from_alias("Luat Cong nghe thong tin quy dinh")[0] == "03"
                  and _expected_cat_from_alias("cong nghe") == ("", "")
                  and _expected_cat_from_alias("khoa hoc cong nghe")[0] == "19"))
    cases.append(("r9_title_vn_from_plan",
                  _title_vn_from_plan({"classification": {"title": "Dân số", "loai": "Luật"}}) == "Luật Dân số"
                  and _title_vn_from_plan({"classification": {"title": "Dan so", "loai": "Luat"}}) == ""
                  and _title_vn_from_plan({}) == ""))
    _sw9 = _sweep_report([
        {"drive_id": "a1", "name": "luat-dau-thau-2023.html", "corpus": "true", "row_kind": "own"},
        {"drive_id": "a2", "name": "Luat_113-2025-QH15_Dan_so", "corpus": "true", "row_kind": "own"},
        {"drive_id": "a3", "name": "PL_06-2025-QH15_Phu_luc", "corpus": "true", "row_kind": "own"},
        {"drive_id": "a4", "name": "CU_ILO-105_Xoa_bo_lao_dong_cuong_buc", "corpus": "true", "row_kind": "own"},
    ])
    cases.append(("r9_sweep_name_nonstandard_offline",
                  _sw9.get("name_nonstandard") == 1
                  and _sw9["name_nonstandard_rows"][0]["drive_id"] == "a1"
                  and any("tên phi-chuẩn" in x for x in _sw9["next_actions"])))
    _ap9 = build_parser()
    cases.append(("r9_parser_from_tukhoa", _ap9.parse_args(["backfill-title-vn", "--from-tukhoa"]).from_tukhoa is True))

    # ═══ v1.31.2 (log LIVE vòng 3 — UTF-8 capture vỡ + nguồn trích yếu = KHỐI TIÊU ĐỀ) — r10_* ═══
    # (U2) parser khối tiêu đề — ghim đúng các ca script tham khảo làm HỎNG (sidecar họ gửi lộ lỗi):
    cases.append(("r10_title_block_multiline_no_cap",   # họ cắt 4 dòng → 'Luật Ban hành văn bản quy phạm pháp' CỤT
                  _title_block_from_text("LUẬT\nBAN HÀNH VĂN BẢN\nQUY PHẠM PHÁP LUẬT\n\nCăn cứ...")
                  == ("Luật", "Ban hành văn bản quy phạm pháp luật")))
    cases.append(("r10_title_block_bo_luat_kind",       # họ match 'LUẬT' trước → 91/2015 thành 'Luật Dân sự' SAI LOẠI
                  _title_block_from_text("BỘ LUẬT\nDÂN SỰ\nCăn cứ...") == ("Bộ luật", "Dân sự")))
    cases.append(("r10_title_block_keeps_special_tokens",   # họ .lower() trần → hỏng '(HIV/AIDS)'; họ cụt '…miễn'
                  _title_block_from_text("LUẬT\nPHÒNG, CHỐNG NHIỄM VI RÚT GÂY RA HỘI CHỨNG SUY GIẢM MIỄN DỊCH "
                                         "MẮC PHẢI Ở NGƯỜI (HIV/AIDS)\nCăn cứ...")[1].endswith("(HIV/AIDS)")))
    cases.append(("r10_title_block_stops_at_lowercase",   # dòng thường (không in hoa) = hết khối, không nuốt bừa
                  _title_block_from_text("NGHỊ ĐỊNH\nQuy định chi tiết một số điều...\nCăn cứ...") == ("", "")))
    cases.append(("r10_title_vn_header_tier1_block",     # _title_vn_from_header ưu tiên tier khối-tiêu-đề
                  _title_vn_from_header("BỘ LUẬT\nDÂN SỰ\nCăn cứ...", {"name": "BLDS_91-2015-QH13"})[0] == "Bộ luật Dân sự"))
    cases.append(("r10_title_sentence_case_tokens",
                  _title_sentence_case("QUẢN LÝ, SỬ DỤNG VŨ KHÍ (CT06) VÀ VẬT LIỆU NỔ")
                  == "Quản lý, sử dụng vũ khí (CT06) và vật liệu nổ"))
    # (U1) sanitize export text: diệt lone-surrogate + control-byte, GIỮ \n\t + tiếng Việt.
    _dirty = "Điều 1.\tPhạm vi\x00\x0b" + "\udcE1" + "\nĐiều 2."
    _clean = _sanitize_export_text(_dirty)
    cases.append(("r10_sanitize_export_text",
                  "\x00" not in _clean and "\x0b" not in _clean and "\udcE1" not in _clean
                  and "Điều 1.\tPhạm vi" in _clean and "\nĐiều 2." in _clean
                  and _clean.encode("utf-8") is not None))
    _rk, _rd, _rr = _profile_rebuild_partition([
        {"id": "own-no-nb", "row_kind": "own"},
        {"id": "notebook-row", "nlm_notebook_id": "n2", "row_kind": "own"},
        {"id": "shared-ref", "row_kind": "ref"},
        {"id": "polluted", "row_kind": "own"},
    ], {"own-no-nb"}, "n2")
    cases.append(("profile_rebuild_keeps_root_notebook_ref",
                  {x["drive_id"] for x in _rk} == {"own-no-nb", "notebook-row", "shared-ref"} and
                  [x["drive_id"] for x in _rd] == ["polluted"] and _rr == {
                      "root_tree": 1, "notebook": 1, "ref": 1}))
    _slot_rows = [
        {"nlm_source_id": "s1", "nlm_status": "pushed", "nlm_notebook_id": "n2"},
        {"nlm_source_id": "s2", "nlm_status": "pushed", "nlm_notebook_id": "n1"},
        {"nlm_source_id": "s3", "nlm_status": "pushed"},
    ]
    slot = _nlm_slot_count(_slot_rows, "n2")
    # notebook dự án n2 (KHÔNG phải base): dòng rỗng KHÔNG cộng → slots_effective == matching == 1 (hết full giả)
    cases.append(("nlm_slot_count_by_notebook_id", slot["slots_for_notebook"] == 1 and slot["rows_with_nlm_status_any_notebook"] == 3 and slot["rows_missing_nlm_notebook_id"] == 1 and slot["slots_effective"] == 1 and not slot["is_base_notebook"]))
    # notebook NỀN (VBQPPL): dòng rỗng QUY VỀ base → slots_effective gồm cả dòng rỗng (giữ đếm đúng VBQPPL, không cần backfill)
    slot_base = _nlm_slot_count(_slot_rows, NLM_BASE_NOTEBOOK)
    cases.append(("nlm_slot_count_base_fallback", slot_base["is_base_notebook"] and slot_base["slots_for_notebook"] == 0 and slot_base["slots_effective"] == 1))
    # v1.19.7 WS1/WS2: bộ danh tính + alias + bóc/đối chiếu dẫn chiếu
    cases.append(("alias_expand_bhxh", "bao hiem xa hoi" in _alias_terms("BHXH") and "bhxh" in _alias_terms("Bảo hiểm xã hội")))
    _refs = extract_refs("Bộ luật Lao động số 45/2019/QH15 và Luật Bảo hiểm xã hội số 41/2024/QH15.")
    cases.append(("extract_refs_2", len(_refs) == 2 and _refs[0]["sohieu"] == "45-2019-QH15"))
    _ents = [{"so_hieu": "45/2019/QH15", "name": "Bo luat Lao dong", "tukhoa": "lao dong blld", "cat": "21"}]
    _cl = _classify_ref({"raw": "x", "name_phrase": "Bộ luật Lao động", "sohieu": "49-2019-QH14"}, _ents)
    cases.append(("xref_sohieu_mismatch", _cl["flag"] == "SOHIEU_MISMATCH" and _cl["canonical"]["sohieu"] == "45/2019/QH15"))
    _ents2 = [{"so_hieu": "41/2024/QH15", "name": "Luat Bao hiem xa hoi", "tukhoa": "bhxh"}]
    cases.append(("resolve_alias_tukhoa", bool(resolve_identity("BHXH", _ents2)) and _entry_sohieu(resolve_identity("BHXH", _ents2)[0][0]) == "41/2024/QH15"))
    _clok = _classify_ref({"raw": "y", "name_phrase": "Bộ luật Lao động", "sohieu": "45-2019-QH15"}, _ents)
    cases.append(("xref_ok_when_match", _clok["flag"] in ("OK", "OUTDATED")))
    _clmiss = _classify_ref({"raw": "z", "name_phrase": "Luật Không Tồn Tại", "sohieu": "999-2099-QH99"}, _ents)
    cases.append(("xref_missing", _clmiss["flag"] == "MISSING"))
    # A1: bản trong _ZZZ_QUARANTINE KHÔNG thắng VBHN-có-goc khi truy vấn theo TÊN
    _a1 = [{"id": "q", "name": "Luat_41-2024-QH15_Bao_hiem_xa_hoi", "so_hieu": "41/2024/QH15", "cat": "_ZZZ_QUARANTINE_taluat", "nlm_source_id": "x"},
           {"id": "v", "name": "VBHN_19-VBHN-VPQH_Bao_hiem_xa_hoi", "so_hieu": "19/VBHN-VPQH", "loai": "VBHN", "cat": "20", "goc": "41/2024/QH15", "hieuluc": "Còn hiệu lực", "nlm_source_id": "y"}]
    _a1h = resolve_identity("bảo hiểm xã hội", _a1, max_hits=2)
    cases.append(("a1_vbhn_beats_quarantine_by_name",
                  bool(_a1h) and _is_vbhn_entry(_a1h[0][0]) and _entry_score(_a1[0]) < _entry_score(_a1[1])))
    # B1: KHÔNG OUTDATED khi bản còn hiệu lực, và khi nằm trong chuỗi hợp nhất của VBHN đang xét
    _b1ents = [{"id": "g", "name": "BLLĐ", "so_hieu": "45/2019/QH15", "hieuluc": "Còn hiệu lực"},
               {"id": "vb", "name": "VBHN BLLĐ", "so_hieu": "18/VBHN-VPQH", "loai": "VBHN", "goc": "45/2019/QH15"}]
    cases.append(("b1_no_outdated_when_effective",
                  _classify_ref({"raw": "", "name_phrase": "", "sohieu": "45-2019-QH15"}, _b1ents)["flag"] != "OUTDATED"))
    cases.append(("b1_no_outdated_in_base_chain",
                  _classify_ref({"raw": "", "name_phrase": "", "sohieu": "124-2025-QH15"},
                                [{"id": "x", "name": "GDNN", "so_hieu": "124/2025/QH15"},
                                 {"id": "v", "name": "VBHN", "so_hieu": "18/VBHN-VPQH", "loai": "VBHN", "goc": "124/2025/QH15"}],
                                base_goc_keys={"124-2025-QH15"})["flag"] != "OUTDATED"))
    # B3+B4: footnote-resolver bản đồ cấp Điều + PENDING_EFFECT
    _b3 = resolve_footnote_amendments(
        "Điều 139. Nghỉ thai sản\n1.[4] Lao động nữ nghỉ 06 tháng.\n"
        "[4] Khoản này được sửa đổi theo quy định tại khoản 1 Điều 29 của Luật Dân số số 113/2025/QH15, có hiệu lực kể từ ngày 01/7/2026.",
        today="2026-06-25")
    _r = _b3["dieu_level_amendment_map"]
    cases.append(("b3_footnote_resolver",
                  len(_r) == 1 and _r[0]["dieu"] == "139" and _r[0]["khoan"] == "1"
                  and _r[0]["amending_sohieu"] == "113-2025-QH15" and _r[0]["hieu_luc"] == "2026-07-01"
                  and _r[0]["pending_effect"] is True))
    # E2: subject-cluster 'pháp luật về X' → số hiệu canonical
    cases.append(("e2_subject_cluster",
                  any(m["sohieu"] == "19/VBHN-VPQH" for m in _cluster_lookup("pháp luật về bảo hiểm xã hội")["matches"])
                  and any(m["sohieu"] == "113/2025/QH15" for m in _cluster_lookup("dân số")["matches"])))
    # WS1 fast-lane: phân loại reconcile theo ground-truth (live_ids)
    _rents = [{"nlm_source_id": "A", "nlm_notebook_id": "", "nlm_status": "pushed"},   # on NLM, thiếu notebook → backfill
              {"nlm_source_id": "B", "nlm_notebook_id": "NB", "nlm_status": "synced"}, # on NLM, đã đúng → bỏ qua
              {"nlm_source_id": "C", "nlm_status": "pushed"},                          # ∉ NLM + pushed → desync_real
              {"nlm_source_id": "E", "nlm_status": "removed_below_nd"},                # ∉ NLM + removed* → already_removed
              {"nlm_source_id": "F", "nlm_status": "removed_from_drive"},              # ∉ NLM + removed* → already_removed
              {"nlm_source_id": "G", "nlm_notebook_id": "OTHER", "nlm_status": "pushed"},  # ∉ NLM này nhưng ở shard khác → other_notebook
              {"nlm_source_id": "", "name": "x"}]                                      # không nlm → bỏ qua
    _pl = _nlm_reconcile_plan({"A", "B", "D"}, _rents, "NB")
    cases.append(("nlm_reconcile_plan",
                  len(_pl["backfill"]) == 1 and _entry_nlm(_pl["backfill"][0]) == "A"
                  and len(_pl["stale"]) == 1 and _entry_nlm(_pl["stale"][0]) == "C"
                  and _pl["unregistered"] == ["D"]))
    # v1.19.9: tách already_removed (removed*) khỏi desync_real (pushed/synced nhưng vắng)
    cases.append(("nlm_reconcile_split_removed",
                  len(_pl["desync_real"]) == 1 and _entry_nlm(_pl["desync_real"][0]) == "C"
                  and len(_pl["already_removed"]) == 2
                  and {_entry_nlm(x) for x in _pl["already_removed"]} == {"E", "F"}))
    # v1.19.11: dòng ở shard/notebook khác (overflow) KHÔNG bị tính desync của notebook này
    cases.append(("nlm_reconcile_other_notebook",
                  len(_pl.get("other_notebook") or []) == 1
                  and _entry_nlm(_pl["other_notebook"][0]) == "G"
                  and all(_entry_nlm(x) != "G" for x in _pl["desync_real"])))
    # fetcher: ưu tiên FORMAT docx>doc>pdf → TVPL/LVN trước, vbpl, rồi Công báo
    _fp = _fetch_plan("134/2025/QH15")["sources"]
    cases.append(("fetch_plan_format_priority",
                  [r["source"] for r in _fp][:4] == ["thuvienphapluat.vn", "luatvietnam.vn", "vbpl.vn", "congbao.chinhphu.vn"]
                  and [r["expected_format"] for r in _fp][:4] == ["docx", "docx", "doc", "pdf"]
                  and _fp[0]["rank"] == 1))
    # Google site: discovery (search nội bộ kém → dùng Google)
    _g = _google_site_url("Luật PPP hợp nhất", "thuvienphapluat.vn")
    cases.append(("google_site_url", _g.startswith("https://www.google.com/search?q=") and "site%3Athuvienphapluat.vn" in _g
                  and "google_global" in _fetch_plan("Luật PPP") and _fetch_plan("Luật PPP")["sources"][0].get("discover") == "google_site"))
    # C2(b)/C4: link TẢI LÊN _HOP_NAP bấm-được đúng folder + C3: env không chắc → 'chat' (an toàn)
    _up = _hopnap_upload_md()
    cases.append(("fetch_links_hopnap_upload",
                  _up.startswith("- [") and HOPNAP_FOLDER_ID in _up
                  and f"drive.google.com/drive/folders/{HOPNAP_FOLDER_ID}" in _up))
    cases.append(("runtime_env_explicit", _runtime_env("chat") == "chat" and _runtime_env("code") == "code" and _runtime_env("cowork") == "cowork"))
    # (1) NLM write qua CLI: _add_args dựng đúng argv cho `nlm source add --drive ... --wait`
    try:
        import nlm_cli as _nc
        _aa = _nc._add_args("NB1", drive_id="GDOC1", doc_type="doc", wait=True, timeout=600)
        cases.append(("nlm_cli_add_args_drive",
                      _aa[:3] == ["source", "add", "NB1"] and "-j" not in _aa and "--drive" in _aa
                      and "GDOC1" in _aa and "--type" in _aa and "--wait" in _aa))
        # cross/get/rename wrapper tồn tại + guard
        cases.append(("nlm_cli_cross_get_rename",
                      all(hasattr(_nc, fn) for fn in ("cross_query", "notebook_get", "source_rename"))
                      and _nc.cross_query("q").get("ok") is False))   # thiếu notebooks → từ chối
    except Exception:
        cases.append(("nlm_cli_add_args_drive", False))
        cases.append(("nlm_cli_cross_get_rename", False))
    # (4) cat normalize + (4)/(5) ingest-local helpers
    cases.append(("ingest_norm_cat", _norm_cat("9") == "09" and _norm_cat("23") == "23" and _norm_cat("QUARANTINE") == "QUARANTINE"))
    # (4) bảng 45 chủ đề pháp điển: đủ 45 + 01/37 đúng tên, slug có tiền tố mã
    _pd = _load_phapdien()
    cases.append(("phapdien_45_official",
                  len([k for k in _pd if k.isdigit() and 1 <= int(k) <= 45]) == 45
                  and _pd.get("01", {}).get("ten") == "An ninh quốc gia"
                  and _pd.get("37", {}).get("folder", "").startswith("37_To_tung")
                  and "Dân tộc" == _pd.get("10", {}).get("ten")))
    # reg-query/cat-audit helpers: suy chủ đề từ tên + hint đã sửa (16/12/14)
    cases.append(("infer_cats_strong",
                  _infer_cats("Luat_100-2015-QH13_Bo_Luat_Hinh_su") == ["16"]
                  and _infer_cats("Luat_67-2006-QH11_CNTT") == ["03"]
                  and "33" in _infer_cats("VBHN_112-VPQH_Luat_Thue_TNCN")
                  and _CAT_REVIEW_HINTS["hình sự"] == "16" and _CAT_REVIEW_HINTS["doanh nghiệp"] == "12"))
    # _subject_sig: phân biệt khác-cơ-quan (BNV≠BYT) + phụ-lục≠chính; trùng biến thể ND/NĐ
    cases.append(("subject_sig_discriminate",
                  _subject_sig("17_2025_TT-BNV_x") != _subject_sig("17_2025_TT-BYT_x")
                  and _subject_sig("ND_128-2026-ND-CP_Phu_luc") != _subject_sig("ND_128-2026-ND-CP_SuaDoi_luat_gia")
                  and _subject_sig("ND_160-2025-ND-CP_Du_lieu") == _subject_sig("NĐ_160-2025-NĐ-CP_Du_lieu")))
    # B1/B2/B3 footnote def-driven (đặc tả 26/6): 5 marker đúng luật/Điều/khoản + hiệu_lực + pending
    _fntxt = ("Điều 59.\nĐiều 61.\nĐiều 139.\nĐiều 154.\nĐiều 217.\n"
              "[1] Bộ luật này được hợp nhất từ các văn bản.\n"
              "[2] Điều 59 được sửa đổi, bổ sung theo điểm a khoản 1 Điều 43 của Luật Giáo dục nghề nghiệp số 124/2025/QH15.\n"
              "[3] Khoản 3 Điều 61 được sửa đổi, bổ sung theo điểm b khoản 1 Điều 43 của Luật Giáo dục nghề nghiệp số 124/2025/QH15.\n"
              "[4] Khoản 1 Điều 139 được sửa đổi theo quy định tại khoản 1 Điều 29 của Luật Dân số số 113/2025/QH15, có hiệu lực kể từ ngày 01/7/2026.\n"
              "[5] Khoản 8a Điều 154 được bổ sung theo khoản 4 Điều 49 của Luật Công nghiệp công nghệ số số 71/2025/QH15.\n"
              "[6] Điều 217 được bổ sung theo Điều 50 của Luật Công nghiệp công nghệ số số 71/2025/QH15.\n")
    _fn = resolve_footnote_amendments(_fntxt, today="2026-06-26",
                                      entries=[{"so_hieu": "124/2025/QH15", "hieuluc": "có hiệu lực từ ngày 01/01/2026"}])
    _d = _fn["footnote_defs"]
    cases.append(("footnote_gdnn_markers",
                  _fn["footnote_count"] == 5
                  and _d.get("2", {}).get("dieu") == "59" and _d["2"]["amending_sohieu"] == "124-2025-QH15" and "điểm a" in (_d["2"].get("amending_vitri") or "")
                  and _d.get("3", {}).get("dieu") == "61" and _d["3"].get("khoan") == "3" and _d["3"]["amending_sohieu"] == "124-2025-QH15"
                  and _d.get("5", {}).get("khoan") == "8a" and _d.get("6", {}).get("dieu") == "217"))
    cases.append(("footnote_hieuluc_fill",
                  _d.get("4", {}).get("hieu_luc") == "2026-07-01" and _d.get("2", {}).get("hieu_luc") == "2026-01-01"))
    cases.append(("pending_from_footnote",
                  _d.get("4", {}).get("pending_effect") is True and _d.get("2", {}).get("pending_effect") is False
                  and sum(1 for r in _fn["dieu_level_amendment_map"] if r.get("pending_effect")) == 1))
    # L1/L2: footnote-resolver bắt dấu-kép "[n]n"/"x[n]" + khoản chữ + pending future-effect
    _ft = resolve_footnote_amendments(
        "Điều 139.\n1. abc...[4]\nĐiều 154.\n8a. xyz...[5]\n\n"
        "[4]4 Khoản 1 Điều 139 sửa đổi theo khoản 1 Điều 29 của Luật Dân số số 113/2025/QH15, có hiệu lực kể từ ngày 01/7/2026.\n"
        "[5]5 Khoản 8a Điều 154 bổ sung theo Luật số 71/2025/QH15.", today="2026-06-26")
    _m = {r["marker"]: r for r in _ft["dieu_level_amendment_map"]}
    cases.append(("footnote_dau_kep_L1L2",
                  _ft["footnote_count"] == 2 and _m.get("4", {}).get("dieu") == "139" and _m["4"]["khoan"] == "1"
                  and _m["4"]["amending_sohieu"] == "113-2025-QH15" and _m["4"]["pending_effect"] is True
                  and _m.get("5", {}).get("khoan") == "8a"))
    # BỎ chú thích TRÍCH DẪN (căn cứ ban hành / 'quy định như sau') — KHÔNG phải amendment (lỗi #1/#6 từ rà soát thật)
    _ftc = resolve_footnote_amendments(
        "[1] Luật số 71/2025/QH15 có căn cứ ban hành như sau: “Căn cứ Hiến pháp...”.\n"
        "[2] Khoản 1 Điều 139 được sửa đổi theo khoản 1 Điều 29 của Luật số 113/2025/QH15.\n"
        "[3] Điều 50 của Luật số 71/2025/QH15 quy định như sau: “Điều 50. Hiệu lực thi hành. Luật này được sửa đổi, bổ sung...”.\n")
    _mc = {r["marker"]: r for r in _ftc["dieu_level_amendment_map"]}
    cases.append(("footnote_skip_citation", _ftc["footnote_count"] == 1 and "2" in _mc and "1" not in _mc and "3" not in _mc))
    # Marker DEF kiểu SỐ TRẦN đầu dòng (vd VBHN-18 viết "\n2 Điểm này được sửa đổi…" thay vì "[2]") — phải bắt được
    _ftb = resolve_footnote_amendments(
        "Điều 59. Đào tạo nghề\n2. Quyền của người sử dụng lao động:\na) [2]Thành lập cơ sở giáo dục nghề nghiệp.\n\n"
        "[1] Luật số 124/2025/QH15 có căn cứ ban hành như sau: “Căn cứ Hiến pháp.”.\n"
        "2 Điểm này được sửa đổi, bổ sung theo quy định tại điểm a khoản 1 Điều 43 của Luật số 124/2025/QH15, "
        "có hiệu lực kể từ ngày 01 tháng 01 năm 2026.\n", today="2026-06-26")
    _mb = {r["marker"]: r for r in _ftb["dieu_level_amendment_map"]}
    cases.append(("footnote_bare_number_marker",
                  _ftb["footnote_count"] == 1 and _mb.get("2", {}).get("dieu") == "59"
                  and _mb["2"]["amending_sohieu"] == "124-2025-QH15" and _mb["2"]["hieu_luc"] == "2026-01-01"
                  and not _mb["2"].get("def_missing")))
    # Footnote TRÍCH DẪN (is_amend=False — vd "[6] Điều 50 của Luật 71/2025 quy định như sau: 'Điều 50. Hiệu lực thi
    # hành…'") đặt trên TIÊU ĐỀ CHƯƠNG "ĐIỀU KHOẢN THI HÀNH" (sau Điều 217) — KHÔNG được gắn nhầm thành "Điều 217 ←
    # 71/2025" (false-positive Type-B cũ). Marker thật ([5] sửa Điều 154) vẫn nhận.
    _ftc6 = resolve_footnote_amendments(
        "Điều 154. Giấy phép lao động\n8. abc\n8a) [5]Người nước ngoài.\n"
        "Điều 217. Xử lý vi phạm\n3. Nội dung 217 K3.\n"
        "CHƯƠNG XVII\nĐIỀU KHOẢN THI HÀNH [6]\nĐiều 218. Hiệu lực.\n\n"
        "[5] Khoản 8a Điều 154 được bổ sung theo khoản 4 Điều 49 của Luật số 71/2025/QH15.\n"
        "[6] Điều 50 của Luật Công nghiệp công nghệ số số 71/2025/QH15 quy định như sau: “Điều 50. Hiệu lực thi "
        "hành. Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026.”.\n", today="2026-06-27")
    _mc6 = {r["marker"]: r for r in _ftc6["dieu_level_amendment_map"]}
    cases.append(("footnote_citation_not_amendment",
                  "5" in _mc6 and _mc6["5"].get("dieu") == "154"
                  and "6" not in _mc6 and not any(r.get("dieu") == "217" for r in _ftc6["dieu_level_amendment_map"])
                  and _ftc6["footnote_count"] == 1))
    # B3 (84/2025): sửa đổi kiểu "Cụm từ '…' được BỎ / THAY THẾ BẰNG '…' theo…" PHẢI được bắt (trước đây bỏ sót
    # toàn bộ tác động của Luật Thanh tra 84/2025 vì parser chỉ nhận 'sửa đổi/bổ sung'). [2]=bỏ@Điều16, [3]=thay thế@Điều17.
    _ftd = resolve_footnote_amendments(
        "Điều 16. Nhiệm vụ\n1. Nội dung [2].\n"
        "Điều 17. Quyền hạn\n2. Nội dung [3].\n\n"
        "[2] Cụm từ “thanh tra viên” tại khoản 1 Điều 16 được bỏ theo quy định tại điểm a khoản 1 Điều 60 của Luật Thanh tra số 84/2025/QH15.\n"
        "[3] Cụm từ “cơ quan” được thay thế bằng “đơn vị” theo quy định tại khoản 2 Điều 60 của Luật Thanh tra số 84/2025/QH15.\n",
        today="2026-06-27")
    _md = {r["marker"]: r for r in _ftd["dieu_level_amendment_map"]}
    cases.append(("footnote_remove_phrase_amendment",
                  "2" in _md and _md["2"].get("dieu") == "16" and _md["2"].get("amending_sohieu") == "84-2025-QH15"
                  and "3" in _md and _md["3"].get("dieu") == "17"
                  and _ftd["footnote_count"] == 2))
    # BUG#4: footnote-map HẠ ƯU TIÊN omnibus cắt-ngang + bãi-bỏ-cục-bộ (đừng ngang hàng luật sửa chuyên đề)
    _ftrk = resolve_footnote_amendments(
        "Điều 2. Người nộp thuế.\n3. Nội dung [7].\n"
        "Điều 16. Quy hoạch.\n4. Nội dung [8].\n"
        "Điều 29. Trợ cấp.\n1. Nội dung [9].\n\n"
        "[7] Khoản 3 Điều 2 được bãi bỏ theo quy định tại khoản 4 Điều 1 của Luật số 32/2013/QH13 sửa đổi, bổ sung một số điều của Luật Thuế thu nhập doanh nghiệp.\n"
        "[8] Khoản 4 Điều 16 được sửa đổi, bổ sung theo quy định tại Điều 1 của Luật số 35/2018/QH14 sửa đổi, bổ sung một số điều của 37 luật có liên quan đến quy hoạch.\n"
        "[9] Khoản 1 Điều 29 được sửa đổi theo khoản 1 Điều 5 của Luật Dân số số 113/2025/QH15.\n",
        today="2026-06-28")
    _mrk = {r["marker"]: r for r in _ftrk["dieu_level_amendment_map"]}
    cases.append(("footnote_rel_kind_crosscut_partial",
                  _mrk.get("7", {}).get("rel_kind") == "PARTIAL_REPEAL"
                  and _mrk.get("8", {}).get("rel_kind") == "CROSS_CUTTING"
                  and _mrk.get("9", {}).get("rel_kind") == ""))
    # BUG#3 preflight: discover overflow notebook từ registry (row_kind=overflow phổ biến nhất ≠ notebook chính)
    cases.append(("discover_overflow_from_registry", _discover_overflow_from_registry([
        {"row_kind": "overflow", "nlm_notebook_id": "OVF-1"},
        {"row_kind": "overflow", "nlm_notebook_id": "OVF-1"},
        {"row_kind": "overflow", "nlm_notebook_id": "OVF-2"},
        {"row_kind": "own", "nlm_notebook_id": "MAIN-NB"},
        {"row_kind": "overflow", "nlm_notebook_id": "MAIN-NB"},
    ], "MAIN-NB") == "OVF-1"))
    cases.append(("discover_overflow_empty", _discover_overflow_from_registry([
        {"row_kind": "own", "nlm_notebook_id": "MAIN-NB"},
    ], "MAIN-NB") == ""))
    # BUG#5 extract: --sohieu khớp entry có sohieu RỖNG nhưng TÊN mang số hiệu (114_2025_QH15_…); tên Mẫu_ KHÔNG khớp giả
    _cfq_e = {"name": "114_2025_QH15_658530", "so_hieu": "", "drive_id": "TARGET"}
    _cfq_key = norm_sohieu("114-2025-QH15")
    cases.append(("canonical_sohieu_from_name",
                  _sohieu_key_entry(_cfq_e) == _cfq_key
                  and norm_sohieu(_entry_sohieu(_cfq_e)) != _cfq_key
                  and ("114-2025-qh15" not in _strip_accents(_entry_name(_cfq_e)).lower())
                  and _sohieu_key_entry({"name": "Mau_114_2025_QH15.docx", "so_hieu": ""}) == ""))
    # BUG#1 gws_rename: rename PHẢI assert tên sau update — gws trả 200 mà echo tên CŨ ⇒ raise, KHÔNG ok giả.
    try:
        _gb = _imp("gws_bridge")
        _orig_run = _gb._run
        try:
            _gb._run = lambda _a, **_k: json.dumps({"id": "F", "name": "OLD.docx"})
            _raised = False
            try:
                _gb.rename("F", "NEW_CHUAN.docx")
            except _gb.GwsError:
                _raised = True
            _gb._run = lambda _a, **_k: json.dumps({"id": "F", "name": "NEW_CHUAN.docx", "parents": ["p"], "trashed": False})
            _ok_real = _gb.rename("F", "NEW_CHUAN.docx").get("ok") is True
        finally:
            _gb._run = _orig_run
        cases.append(("gws_rename_assert", _raised and _ok_real))
    except Exception:
        cases.append(("gws_rename_assert", False))
    # source-map/relation: BHXH↔BHYT KHÔNG match chéo dù chung "bảo hiểm" (51/2024 sửa BHYT ≠ chủ đề BHXH → hết
    # AMENDMENT_CANDIDATE/PAUSE_AND_ASK giả). BHXH thật vẫn match cao.
    cases.append(("subject_bhxh_not_bhyt",
                  _subject_score({"name": "Luat 51/2024/QH15 sửa đổi Luật Bảo hiểm y tế", "cat": "02"}, "bảo hiểm xã hội") == 0
                  and _subject_score({"name": "VBHN 19 Luật Bảo hiểm xã hội hợp nhất", "cat": "02"}, "bảo hiểm xã hội") >= 30))
    # Tra-theo-tên: 'Luật Bảo hiểm xã hội' PHẢI khớp 'VBHN_19-VPQH_Bao_hiem_xa_hoi' (token-subset, vì 'luat/vbhn/19/vpqh'
    # chèn giữa làm substring liền THẤT BẠI → trước đây source-map/reg-query trả not_found/0 dù VBHN ở corpus). KHÔNG khớp BHYT.
    cases.append(("name_subset_match_vbhn",
                  _name_subset_match("Luật Bảo hiểm xã hội", "VBHN_19-VPQH_Bao_hiem_xa_hoi") is True
                  and _name_subset_match("Bảo hiểm xã hội", "Luat_51-2024-QH15_SuaDoi_Bao_hiem_y_te") is False))
    # source-map: canonical = VBHN (corpus) chứ KHÔNG phải bản gốc đã QUARANTINE (ranking phạt quarantine -400).
    # Tên VBHN dùng VIẾT TẮT 'BHXH' (đúng tên file thật) — phải khớp 'Luật Bảo hiểm xã hội' qua _expand_abbrev,
    # nếu không sẽ nhặt nhầm bản gốc 41/2024 (viết-đầy-đủ) đã quarantine.
    _sm = _source_map_one("Luật Bảo hiểm xã hội", [
        {"name": "VBHN_19-VBHN-VPQH_2026_Luat_BHXH_HopNhat", "sohieu": "19/VBHN-VPQH", "cat": "02_Bao_hiem", "corpus": "true", "nlm_source_id": "s1", "loai": "VBHN"},
        {"name": "Luat_41-2024-QH15_Bao_hiem_xa_hoi", "sohieu": "41/2024/QH15", "cat": "_ZZZ_QUARANTINE_taluat", "corpus": "false"},
    ])
    cases.append(("source_map_name_finds_vbhn_not_quarantine",
                  _sm["mode"] != "not_found" and bool(_sm.get("canonical"))
                  and "19" in (_sm["canonical"].get("sohieu") or "")))
    # Viết tắt pháp lý: 'BHXH' ≡ 'bảo hiểm xã hội'; 'BHYT' ≠ (loại trừ chéo vẫn giữ).
    cases.append(("abbrev_bhxh_expand_match",
                  _name_subset_match("Luật Bảo hiểm xã hội", "VBHN_19-VBHN-VPQH_2026_Luat_BHXH_HopNhat") is True
                  and _subject_score({"name": "VBHN_19_Luat_BHXH_HopNhat", "cat": "02"}, "bảo hiểm xã hội") >= 30
                  and _name_subset_match("Luật Bảo hiểm xã hội", "Luat_57_Luat_BHYT_SuaDoi") is False))
    # A3 (log relation-check): vbhn_candidates KHÔNG nhận VBHN khác lĩnh vực chỉ vì TRÙNG NĂM (VBHN_43 Xuất bản 2024
    # lọt vào chủ đề 'bảo hiểm xã hội'). VBHN đúng nhận qua goc-match. year-một-mình KHÔNG đủ khi đã có subject.
    _vc = _vbhn_candidates([
        {"name": "VBHN_43-VBHN-VPQH_2024_Xuat_ban", "sohieu": "43/VBHN-VPQH", "loai": "VBHN", "cat": "32", "nlm_source_id": "x"},
        {"name": "VBHN_19-VBHN-VPQH_2026_Bao_hiem_xa_hoi", "sohieu": "19/VBHN-VPQH", "loai": "VBHN", "cat": "02", "nlm_source_id": "y", "goc": "41/2024/QH15"},
    ], subject="bảo hiểm xã hội", goc="41/2024/QH15", year="2024")
    _vn = [_entry_name(e) for e in _vc]
    cases.append(("vbhn_candidates_year_alone_excluded",
                  any("19" in n for n in _vn) and not any("Xuat_ban" in n for n in _vn)))
    # #11 OMNIBUS: luật sửa có tên khác lĩnh vực base (84/2025=Thanh tra sửa BHXH) → có note; cùng lĩnh vực → None.
    _oents = [
        {"name": "Luat_84-2025-QH15_Thanh_tra", "sohieu": "84/2025/QH15", "cat": "44"},
        {"name": "Luat_142-2025-QH15_Bao_hiem_xa_hoi_sua_doi", "sohieu": "142/2025/QH15", "cat": "02"},
    ]
    cases.append(("omnibus_cross_domain_flag",
                  bool(_omnibus_cross_domain_note("84/2025/QH15", "bảo hiểm xã hội", _oents))
                  and _omnibus_cross_domain_note("142/2025/QH15", "bảo hiểm xã hội", _oents) is None
                  and _omnibus_cross_domain_note("99/2099/QH99", "bảo hiểm xã hội", _oents) is None))
    # B3 false-positive: luật sửa TÊN SỐ TRƠ (metadata trống) KHÔNG bị gắn omnibus (chỉ thiếu metadata ≠ cross-domain);
    # luật sửa CÓ chủ đề rõ + khác lĩnh vực thì VẪN gắn.
    _oents3 = [{"name": "51_2024_QH15_505750", "sohieu": "51/2024/QH15", "cat": "02"},
               {"name": "Luat_84-2025-QH15_Thanh_tra", "sohieu": "84/2025/QH15", "cat": "44"}]
    cases.append(("omnibus_no_flag_bare_number",
                  _omnibus_cross_domain_note("51/2024/QH15", "bảo hiểm y tế", _oents3) is None
                  and bool(_omnibus_cross_domain_note("84/2025/QH15", "bảo hiểm xã hội", _oents3))))
    # B5: _summ_entry.nlm = LIVE (False nếu removed) → khớp reg-query (không còn nlm=True cho bản đã gỡ).
    cases.append(("summ_entry_nlm_live",
                  _summ_entry({"nlm_source_id": "s", "nlm_status": "removed"})["nlm"] is False
                  and _summ_entry({"nlm_source_id": "s", "nlm_status": "pushed"})["nlm"] is True
                  and _summ_entry({"nlm_source_id": ""})["nlm"] is False))
    # locate: cụm danh từ KHÔNG bị coi là số hiệu (hết LOW_CONFIDENCE giả); số hiệu thật thì có.
    cases.append(("locate_not_treat_phrase_as_sohieu",
                  _looks_like_sohieu_query("bảo hiểm xã hội") is False
                  and _looks_like_sohieu_query("142/2025/QH15") is True
                  and _looks_like_sohieu_query("19-VBHN-VPQH") is True))
    # worksheet auto-cache: tách giá trị cờ --so-hieu/--variant (cả dạng = ) để dò cache + resolve gdoc.
    cases.append(("flag_value_parse",
                  _flag_value(["--so-hieu", "19/VBHN-VPQH", "--variant", "consolidated"], "--so-hieu") == "19/VBHN-VPQH"
                  and _flag_value(["--variant=deep"], "--variant") == "deep"
                  and _flag_value(["--x", "y"], "--so-hieu") is None))
    # subject filter CHỐNG nhiễu từ-phổ-biến: 'Luật Xuất bản' (từ khoá có 'Bảo đảm'/'bảo hộ'/'hội') KHÔNG khớp
    # 'bảo hiểm xã hội' (thiếu cụm-đầu 'bảo hiểm'); VBHN BHXH thật vẫn ≥30. (root fix khi chạy mục B live.)
    cases.append(("subject_score_common_word_noise",
                  _subject_score({"name": "VBHN_43-VBHN-VPQH_Luat_Xuat_ban", "cat": "32_Thong_tin_bao_chi_xuat_ban",
                                  "tukhoa": "Bảo đảm quyền phổ biến tác phẩm; bảo hộ quyền tác giả; hội"}, "bảo hiểm xã hội") == 0
                  and _subject_score({"name": "VBHN_19_Luat_BHXH_HopNhat", "cat": "02_Bao_hiem"}, "bảo hiểm xã hội") >= 30))
    # cat = nhãn FOLDER, KHÔNG phải chủ đề: NHNN misfile trong '02_Bao_hiem' KHÔNG được khớp 'bảo hiểm xã hội'.
    cases.append(("subject_score_ignores_cat_folder",
                  _subject_score({"name": "VBHN_25-VBHN-VPQH_2022_Luat_NHNN", "cat": "02_Bao_hiem"}, "bảo hiểm xã hội") == 0
                  and _subject_score({"name": "VBHN_31_Luat_KDBH_HopNhat", "cat": "02_Bao_hiem"}, "bảo hiểm xã hội") >= 30))
    # L4: số hiệu lỏng-năm — '72/NQ-TW' ≡ '72/2025/NQ-TW'
    cases.append(("sohieu_loose_L4", _sohieu_loose("72/NQ-TW") == _sohieu_loose("72/2025/NQ-TW")
                  and _sohieu_loose("45/2019/QH14") != _sohieu_loose("47/2019/QH14")))
    # L5: slot-count loại removed_* dù còn nlm_source_id sót
    _sc = _nlm_slot_count([
        {"nlm_source_id": "s1", "nlm_status": "pushed", "nlm_notebook_id": NLM_BASE_NOTEBOOK},
        {"nlm_source_id": "s2", "nlm_status": "removed_below_nd", "nlm_notebook_id": NLM_BASE_NOTEBOOK},
        {"nlm_source_id": "s3", "nlm_status": "removed_superseded_by_vbhn", "nlm_notebook_id": NLM_BASE_NOTEBOOK},
    ], NLM_BASE_NOTEBOOK)
    cases.append(("slot_excludes_removed_L5", _sc["slots_effective"] == 1))
    # discovery dùng chung: Google site: VBHN-first cho mọi tính năng tìm-văn-bản-web
    _dl = _discovery_links("Luật PPP")
    cases.append(("discovery_links_shared",
                  _dl["query_variants"][0] == "Luật PPP hợp nhất"
                  and any("site:thuvienphapluat.vn" in m for m in _dl["links_markdown"])
                  and any("site:vbpl.vn" in m for m in _dl["links_markdown"])
                  and "google.com/search" in _dl["links_markdown"][0]))
    # VBHN-first query expansion: tên → 'hợp nhất' trước; số hiệu → tìm thẳng
    cases.append(("query_variants_vbhn_first",
                  _query_variants("Luật PPP") == ["Luật PPP hợp nhất", "Luật PPP mới nhất", "Luật PPP"]
                  and _query_variants("64/2020/QH14") == ["64/2020/QH14"]
                  and _query_variants("Luật Đầu tư hợp nhất")[0] == "Luật Đầu tư hợp nhất"))
    try:
        import gen_instructions as _gi  # type: ignore
        _txt = _gi.generate("both", "1.18.0") if hasattr(_gi, "generate") else _gi.build_instruction("both", "1.18.0")
        _audit = _gi.audit(_txt) if hasattr(_gi, "audit") else {"ok": _gi.validate_instruction(_txt)[0]}
        cases.append(("gen_instructions_skill_binding", bool(_audit.get("ok"))))
    except Exception:
        cases.append(("gen_instructions_skill_binding", False))
    cases.append(("expect_version", EXPECT_VERSION == "2.21.2i"))
    cases.append(("gws_pin_set", bool(re.match(r"^\d+\.\d+\.\d+$", GWS_PINNED_VERSION)) and "latest" not in GWS_PINNED_VERSION))
    try:
        _tr = _imp("transport")
        cases.append(("transport_pin_sync", _tr.gws_bridge.PINNED_VERSION == GWS_PINNED_VERSION))
        cases.append(("transport_selftest", _tr.selftest() == 0))
    except Exception:
        cases.append(("transport_pin_sync", False))
        cases.append(("transport_selftest", False))
    try:
        cases.append(("gws_cred_store", _imp("gws_cred_store").selftest()))
    except Exception:
        cases.append(("gws_cred_store", False))
    # #1/#3: relation-check chỉ backfill (goc & sua_doi) cho amendment XÁC THỰC; subject-only → review, KHÔNG vào sua_doi
    try:
        _ents = [
            {"so_hieu": "45/2019/QH14", "name": "Bộ luật Lao động", "loai": "Luật", "linhvuc": "lao động", "drive_id": "b"},
            {"so_hieu": "55/2024/QH15", "name": "Luật sửa đổi Bộ luật Lao động lao động", "loai": "Luật", "linhvuc": "lao động", "drive_id": "d"},
            {"so_hieu": "108/2026/NĐ-CP", "name": "Nghị định sửa đổi trường giáo dưỡng lao động", "loai": "Nghị định", "linhvuc": "lao động", "drive_id": "s"},
        ]
        _o = _relation_audit(_ents, base="45/2019/QH14", subject="lao động", amendments=["55/2024/QH15"])
        _goc = [m for m in _o["missing_links"] if m["action"] == "BACKFILL_GOC_ON_AMENDMENT"]
        _sua = [m for m in _o["missing_links"] if m["action"] == "BACKFILL_SUA_DOI_ON_BASE"]
        _add = " ".join(str(m.get("add")) for m in _sua)   # add = số hiệu CHUẨN HOÁ (dấu gạch): 55-2024-QH15
        _ok = (any("55/2024" in (m["sohieu"] or "") for m in _goc)
               and not any("108/2026" in (m["sohieu"] or "") for m in _goc)
               and any("108/2026" in (r["sohieu"] or "") for r in _o.get("subject_only_review", []))
               and "55-2024" in _add               # direct VẪN backfill sua_doi
               and "108-2026" not in _add)          # #1: subject-only KHÔNG vào sua_doi backfill
        cases.append(("relation_subject_only_no_backfill", _ok))
    except Exception:
        cases.append(("relation_subject_only_no_backfill", False))
    # #1: footnote-map = nguồn ưu tiên — subject-only ĐƯỢC footnote xác nhận thì backfill, KHÔNG có thì chặn
    try:
        _entsf = [
            {"so_hieu": "45/2019/QH14", "name": "Bộ luật Lao động", "loai": "Luật", "linhvuc": "lao động", "drive_id": "b"},
            {"so_hieu": "113/2025/QH15", "name": "Luật Dân số sửa đổi lao động", "loai": "Luật", "linhvuc": "lao động", "drive_id": "ds"},
            {"so_hieu": "108/2026/NĐ-CP", "name": "Nghị định sửa đổi trường giáo dưỡng lao động", "loai": "Nghị định", "linhvuc": "lao động", "drive_id": "s"},
        ]
        _of = _relation_audit(_entsf, base="45/2019/QH14", subject="lao động", footnote_amend_keys={"113/2025/QH15"})
        _addf = " ".join(str(m.get("add")) for m in _of["missing_links"] if m["action"] == "BACKFILL_SUA_DOI_ON_BASE")
        _okf = ("113-2025" in _addf                  # footnote xác nhận → rescue subject-only (số hiệu chuẩn hoá)
                and "108-2026" not in _addf           # không trong footnote → chặn
                and any("108/2026" in (r["sohieu"] or "") for r in _of.get("subject_only_review", []))
                and _of.get("footnote_gate") is True)
        cases.append(("relation_footnote_gate_rescue_block", _okf))
    except Exception:
        cases.append(("relation_footnote_gate_rescue_block", False))
    # #6: số hiệu TRÙNG (14/VBHN-VPQH) → disambiguate theo chủ đề, GIỮ VBHN-first (không tụt về Luật gốc)
    try:
        _e2 = [
            {"so_hieu": "14/VBHN-VPQH", "name": "VBHN 14 2024 An toan Ve sinh lao dong hop nhat", "hieuluc": "Còn hiệu lực", "issue_year": "2024", "loai": "VBHN"},
            {"so_hieu": "14/VBHN-VPQH", "name": "VBHN 14 2023 NLD di lam viec nuoc ngoai hop nhat", "hieuluc": "Còn hiệu lực", "issue_year": "2023", "loai": "VBHN"},
        ]
        _r = _resolve_cluster_member("14/VBHN-VPQH", "an toàn vệ sinh lao động", _e2)
        cases.append(("cluster_dup_sohieu_disambig", "An toan Ve sinh" in (_r.get("name") or "") and _r.get("ambiguous") is True))
    except Exception:
        cases.append(("cluster_dup_sohieu_disambig", False))
    # #4: cùng số hiệu KHÔNG xung đột năm/goc = nhân-đôi 1 văn bản (1 doc); năm KHÁC = reuse-khác-doc (2 doc)
    _same = _split_distinct_vbhn_docs([
        {"so_hieu": "18/VBHN-VPQH", "issue_year": "2026", "goc": "45/2019/QH14", "nlm_source_id": "x"},
        {"so_hieu": "18/VBHN-VPQH"}])
    _reuse = _split_distinct_vbhn_docs([
        {"so_hieu": "14/VBHN-VPQH", "issue_year": "2024", "goc": "84/2015/QH13"},
        {"so_hieu": "14/VBHN-VPQH", "issue_year": "2023", "goc": "69/2020/QH14"}])
    cases.append(("vbhn_same_doc_vs_reuse", len(_same) == 1 and len(_reuse) == 2))
    # #4: tl rasoat worksheet <số hiệu> map positional → --so-hieu (giữ nguyên khi đã có cờ / -h / sub khác)
    cases.append(("rasoat_worksheet_positional_maps_so_hieu",
                  _rasoat_map_positional("worksheet", ["18/VBHN-VPQH"]) == ["--so-hieu", "18/VBHN-VPQH"]
                  and _rasoat_map_positional("worksheet", ["--so-hieu", "x"]) == ["--so-hieu", "x"]
                  and _rasoat_map_positional("phuluc", ["m.json", "--out-dir", "."]) == ["--in", "m.json", "--out-dir", "."]
                  and _rasoat_map_positional("keywords", ["foo"]) == ["foo"]
                  and _rasoat_map_positional("worksheet", ["--help"]) == ["--help"]))
    # #6: dòng đã cách ly (quarantine cat / corpus=false & không NLM) KHÔNG nổi lên risky_candidates của source-map
    cases.append(("entry_quarantined_detect",
                  _entry_quarantined({"cat": "_ZZZ_QUARANTINE_taluat"}) is True
                  and _entry_quarantined({"corpus": "false"}) is True
                  and _entry_quarantined({"corpus": "false", "nlm_source_id": "n"}) is False
                  and _entry_quarantined({"corpus": "true", "cat": "20"}) is False))
    _qfx = [
        {"id": "good", "name": "VBHN_18-VBHN-VPQH_2026_BLLD_HopNhat", "so_hieu": "18/VBHN-VPQH", "loai": "VBHN", "cat": "20", "issue_year": "2026", "goc": "45/2019/QH14", "nlm_source_id": "n", "corpus": "true"},
        {"id": "bare", "name": "VBHN_18-VPQH_BLLD", "so_hieu": "18-VPQH", "loai": "VBHN", "cat": "20", "corpus": "false"},
    ]
    _smq = _source_map_one("18/VBHN-VPQH", _qfx)
    cases.append(("source_map_quarantine_not_risky",
                  not any((rc.get("entry") or {}).get("drive_id") == "bare" for rc in _smq.get("risky_candidates", []))))
    # truncation-resilience: subprocess script lành → _healed_script_path trả thẳng bản gốc (không tạo temp thừa)
    cases.append(("healed_script_path_intact_returns_original",
                  _healed_script_path("rasoat_worksheet") == str(HERE / "rasoat_worksheet.py")
                  and _healed_script_path("tl_boot") == str(HERE / "tl_boot.py")
                  and _healed_script_path("khong_ton_tai_xyz") is None))
    # #3 (chat): reg-query JSON dùng khóa NLM rõ-nghĩa (on_nlm/nlm_source_id/nlm_status), bỏ `nlm`/`src_id` mơ hồ
    _rq = _reg_query_row({"drive_id": "d", "name": "x", "nlm_source_id": "src9", "nlm_status": "pushed", "corpus": "true"})
    cases.append(("reg_query_row_unambiguous_nlm",
                  _rq["on_nlm"] is True and _rq["nlm_source_id"] == "src9" and _rq["nlm_status"] == "pushed"
                  and "nlm" not in _rq and "src_id" not in _rq
                  and _reg_query_row({"drive_id": "e", "name": "y"})["on_nlm"] is False))
    # verify-integrity DETECT (hậu bỏ _parts): MỌI file compile được → NOPARTS (không còn _parts để đối chiếu),
    # KHÔNG file nào TRUNCATED/NUL/MISSING. tl + tl_boot phải có mặt & lành.
    _iscan = _integrity_scan()
    cases.append(("integrity_scan_all_healthy",
                  all(r["status"] in ("OK", "NOPARTS") for r in _iscan)
                  and any(r["name"] == "tl" and r["status"] in ("OK", "NOPARTS") for r in _iscan)
                  and any(r["name"] == "tl_boot" and r["status"] in ("OK", "NOPARTS") for r in _iscan)))
    # KH1 Pha 1.1 — H1 (báo cáo mục H): reg-query --json LUÔN rc=0 + envelope hợp lệ khi CHẠY OK (kể cả dump toàn bộ,
    # KHÔNG filter). rc=1 trong log là confound redirect/&&/bản deployed cũ → KHÓA để không tái phát. Monkeypatch
    # _manifest_entries (offline, không cần boot/manifest live).
    import io as _io, contextlib as _ctx
    _h1 = False
    try:
        _saved_me = _TL_MODULE._manifest_entries
        _TL_MODULE._manifest_entries = lambda refresh=False: [
            {"drive_id": "d1", "name": "Luat_X_2020", "so_hieu": "1/2020/QH14",
             "corpus": "true", "nlm_source_id": "s1", "nlm_status": "pushed"}]
        try:
            _ns = argparse.Namespace(json=True, name=None, sohieu=None, cat=None, row_kind=None, mime=None,
                                     nlm=False, no_nlm=False, corpus=False, no_corpus=False, limit=None,
                                     refresh=False, config=None, profile=None)
            _buf = _io.StringIO()
            with _ctx.redirect_stdout(_buf):
                _rc = _TL_MODULE.cmd_reg_query(_ns)
            _env = json.loads(_buf.getvalue())
            _h1 = (_rc == 0 and _env.get("ok") is True and _env.get("schema") == "reg-query.v2"
                   and _env.get("count") == 1 and len(_env.get("rows", [])) == 1)
        finally:
            _TL_MODULE._manifest_entries = _saved_me
    except Exception:
        _h1 = False
    cases.append(("reg_query_json_rc0_envelope", _h1))
    # KH1 Pha 1.1 — H2: registry-doctor text & JSON DÙNG CHUNG schema. Dòng text sinh từ _DOCTOR_SUMMARY_KEYS;
    # MỌI token-key của text PHẢI là khóa top-level JSON (trước lệch: duplicate_sohieu↔_groups, title_mismatch↔_candidates).
    _h2 = False
    try:
        _rh = _imp("registry_hygiene")
        _rep = _rh.analyze(_rh.entries({"entries": [
            {"so_hieu": "1/2020/QH14", "name": "Luat A", "drive_id": "d1", "corpus": "true"},
            {"so_hieu": "1/2020/QH14", "name": "Luat A khac", "drive_id": "d2", "corpus": "true"},
        ]}))
        _summary = _rh.build_doctor_summary(_rep)
        _txt = _rh.format_doctor_text(_summary)
        _toks = [t.split("=", 1)[0] for t in _txt.split()]
        _h2 = (set(_toks) == set(_rh._DOCTOR_SUMMARY_KEYS)
               and all(k in _summary for k in _toks) and "samples" not in _toks
               and _summary["count"] == 2 and _summary["duplicate_sohieu_groups"] == 1)
    except Exception:
        _h2 = False
    cases.append(("registry_doctor_text_json_parity", _h2))
    # KH1 Pha 1.4 — III.1: tl.py set PYTHONUTF8=1 → script con (gen_instructions…) in tiếng Việt không ném
    # UnicodeEncodeError trên console Windows cp125x.
    cases.append(("utf8_child_env_set", os.environ.get("PYTHONUTF8") == "1"))
    # ───── KH1 Pha 1.2 — Cổng G3 (category theo nội dung + quy tắc ranh giới), test PURE helper (offline) ─────
    cases.append(("g3_load_linhvuc_has_rules",
                  len(_load_linhvuc().get("quy_tac_ranh_gioi", [])) >= 5
                  and "02" in (_load_linhvuc().get("chude") or {})))
    cases.append(("g3_cat_taxonomy_45plus2",
                  all(c in _cat_taxonomy() for c in ("02", "20", "26", "46", "00", "QUARANTINE"))
                  and "99" not in _cat_taxonomy()))
    # quy_tac_ranh_gioi: BHXH/BHYT → 02 (KHÔNG 20 dù gắn lao động)
    cases.append(("g3_boundary_bhxh_to_02",
                  _cat_boundary_rule("Luật này quy định về bảo hiểm xã hội bắt buộc")[0] == "02"
                  and _cat_boundary_rule("chế độ bảo hiểm y tế cho người lao động")[0] == "02"))
    # đầu tư CÔNG → 26 (không 34); đầu tư KINH DOANH → KHÔNG bị ép (để _infer_cats_text ra 34)
    cases.append(("g3_boundary_dau_tu_cong_26_kd_free",
                  _cat_boundary_rule("quản lý đầu tư công vốn nhà nước")[0] == "26"
                  and _cat_boundary_rule("hoạt động đầu tư kinh doanh")[0] is None
                  and (_infer_cats_text("hoạt động đầu tư kinh doanh, đấu thầu")[0][0] == "34")))
    cases.append(("g3_boundary_hai_quan_26_not_33",
                  _cat_boundary_rule("Luật Hải quan về quản lý hải quan")[0] == "26"))
    # sửa ≥2 luật → 46; sửa 1 luật → KHÔNG ép 46
    cases.append(("g3_boundary_sua_nhieu_luat_46",
                  _cat_boundary_rule("Luật sửa đổi, bổ sung một số điều của Luật A, Luật B và Luật C")[0] == "46"
                  and _cat_boundary_rule("Luật sửa đổi, bổ sung một số điều của Luật Đầu tư")[0] != "46"))
    cases.append(("g3_boundary_dieu_uoc_23_dang_00",
                  _cat_boundary_rule("Luật Điều ước quốc tế")[0] == "23"
                  and _cat_boundary_rule("Nghị quyết của Ban Chấp hành Trung ương Đảng")[0] == "00"))
    # KHÔNG ép sai khi không thuộc ranh giới (giáo dục → None, để infer xử)
    cases.append(("g3_boundary_none_when_no_rule",
                  _cat_boundary_rule("Luật Giáo dục đại học")[0] is None
                  and _infer_cats_text("Luật Giáo dục đại học và đào tạo")[0][0] == "13"))
    # _infer_cats_text suy theo NỘI DUNG (cụm nhiều từ thắng nhiễu đơn từ)
    cases.append(("g3_infer_cats_text_content",
                  _infer_cats_text("khám bệnh, chữa bệnh và an toàn thực phẩm")[0][0] == "45"
                  and _infer_cats_text("")[:1] == []))
    # ───── KH1 Pha 1.2 — Cổng G2 (tên↔header), test PURE helper (offline) ─────
    cases.append(("g2_extract_header_facts_date",
                  _extract_header_facts("Luật số 45 ban hành ngày 20 tháng 11 năm 2019")["issue_date"] == "2019-11-20"
                  and _extract_header_facts("không có ngày")["issue_date"] == ""))
    cases.append(("g2_extract_header_facts_agency",
                  _extract_header_facts("QUỐC HỘI nước Cộng hòa")["agency"] == "QH"
                  and _extract_header_facts("CHÍNH PHỦ ban hành")["agency"] == "CP"
                  and _extract_header_facts("ỦY BAN THƯỜNG VỤ QUỐC HỘI")["agency"] == "UBTVQH"))
    # G2 lõi: _verify_header_match — header khớp → ok; số hiệu sai trong header → sohieu check False + ok False.
    _e_hv = {"name": "Luat_45-2019-QH14_Bo_luat_lao_dong", "so_hieu": "45/2019/QH14", "cat": "20_Lao_dong"}
    _hv_good = _verify_header_match(_e_hv, "QUỐC HỘI\nLuật số 45/2019/QH14\nBỘ LUẬT LAO ĐỘNG\nquy định về lao động, việc làm, tiền lương, hợp đồng lao động")
    _hv_bad = _verify_header_match(_e_hv, "QUỐC HỘI\nLuật số 99/2099/QH99\nVĂN BẢN KHÁC\nnội dung hoàn toàn khác biệt")
    cases.append(("g2_verify_header_match_smoke",
                  _hv_good["checks"].get("sohieu") is True and _hv_good["ok"] is True
                  and _hv_bad["checks"].get("sohieu") is False and _hv_bad["ok"] is False))
    # ───── KH1 Pha 1.2 — Cổng G1 (nguồn official-first + toàn vẹn), test PURE helper (offline) ─────
    cases.append(("g1_content_md5_deterministic",
                  len(_content_md5("abc")) == 32 and _content_md5("abc") == _content_md5("abc")
                  and _content_md5("") == ""
                  and _content_md5("Việt") == _content_md5(unicodedata.normalize("NFD", "Việt"))))
    cases.append(("g1_official_rank_first",
                  _official_rank("https://vbpl.vn/x") == 1 and _official_rank("congbao.chinhphu.vn/y") == 1
                  and _official_rank("abc.gov.vn") == 2 and _official_rank("luatvietnam.vn") == 3
                  and _official_rank("thuvienphapluat.vn") == 4 and _official_rank("https://example.com") == 5
                  and _DISCOVERY_SITES[0] == "vbpl.vn"
                  and _official_rank(_DISCOVERY_SITES[0]) <= _official_rank(_DISCOVERY_SITES[-1])))
    # ───── KH1 Pha 1.2 — frontier-expand: pure _frontier_candidates (dedup số hiệu + ưu tiên + in_corpus), offline ─────
    _classed_fx = [
        {"sohieu": "45/2019/QH14", "flag": "OK", "canonical": {"sohieu": "45/2019/QH14"}, "name_phrase": "BLLĐ"},
        {"sohieu": "45/2019/QH14", "flag": "OK", "canonical": {"sohieu": "45/2019/QH14"}, "name_phrase": "trùng"},
        {"sohieu": "99/2099/QH99", "flag": "MISSING", "canonical": None, "name_phrase": "thiếu"},
        {"sohieu": "18/VBHN-VPQH", "flag": "OUTDATED", "canonical": {"sohieu": "18/VBHN-VPQH"}, "name_phrase": "vbhn"},
    ]
    _fx = _frontier_candidates(_classed_fx, {norm_sohieu("100/2099/QH99")})
    cases.append(("frontier_candidates_dedup_priority_incorpus",
                  len(_fx) == 3                                                   # dedup 4→3
                  and [f["sohieu"] for f in _fx if not f["in_corpus"]] == ["99/2099/QH99"]
                  and any(f["sohieu_norm"] == norm_sohieu("18/VBHN-VPQH") and f["priority"] == 2 for f in _fx)
                  and all(f["in_corpus"] for f in _fx if f["flag"] in ("OK", "OUTDATED"))))
    _fx2 = _frontier_candidates([{"sohieu": "84/2015/QH13", "flag": "OK", "canonical": {"sohieu": "84/2015/QH13"}}],
                                {norm_sohieu("84/2015/QH13")})
    cases.append(("frontier_candidates_amending_priority1", bool(_fx2) and _fx2[0]["priority"] == 1))
    # ───── KH1 Pha 1.2 — ingest-missing: pure select (idempotent) + route (KHÔNG tạo notebook), offline ─────
    _ents_im = [
        {"corpus": "true", "drive_id": "d1", "so_hieu": "1/2020/QH14", "name": "A"},                              # cần nạp
        {"corpus": "true", "drive_id": "d2", "so_hieu": "2/2020/QH14", "name": "B", "nlm_source_id": "s2", "nlm_status": "pushed"},  # đã NLM → bỏ
        {"corpus": "false", "drive_id": "d3", "so_hieu": "3/2020/QH14", "name": "C"},                             # không corpus → bỏ
        {"corpus": "true", "drive_id": "", "so_hieu": "4/2020/QH14", "name": "D"},                                # không drive_id → bỏ
    ]
    cases.append(("ingest_missing_select_idempotent",
                  [_entry_drive_id(e) for e in _ingest_missing_select(_ents_im)] == ["d1"]))
    cases.append(("ingest_missing_route_never_creates",
                  _overflow_route(5, "OV-1", 10)[0] == "base"
                  and _overflow_route(0, "OV-1", 10)[0] == "overflow"
                  and _overflow_route(0, "OV-1", 0)[0] == "blocked"
                  and _overflow_route(0, "", 0)[0] == "blocked"
                  and all(_overflow_route(b, o, r)[0] in ("base", "overflow", "blocked")
                          for b in (0, 5) for o in ("", "OV-1") for r in (0, 10))))
    # ───── KH1 Pha 1.2 — rasoat-loop: pure _rasoat_dedup_push (dedup seen chống lặp + ưu tiên + tín hiệu dry), offline ─────
    _rl_fr, _rl_seen = [], set()
    _rl_a = _rasoat_dedup_push(_rl_fr, _rl_seen,
                               [{"sohieu": "1/2020/QH14", "sohieu_norm": norm_sohieu("1/2020/QH14"), "priority": 3},
                                {"sohieu": "18/VBHN-VPQH", "sohieu_norm": norm_sohieu("18/VBHN-VPQH"), "priority": 1}])
    _rl_b = _rasoat_dedup_push(_rl_fr, _rl_seen,
                               [{"sohieu": "1/2020/QH14", "sohieu_norm": norm_sohieu("1/2020/QH14"), "priority": 3}])
    cases.append(("rasoat_loop_dedup_priority_no_infinite",
                  _rl_a == 2 and _rl_b == 0 and len(_rl_seen) == 2
                  and _rl_fr[0]["sohieu_norm"] == norm_sohieu("18/VBHN-VPQH")))   # priority 1 lên đầu; trùng → 0 (dry++)
    # ───── KH1 Pha 1.5 — backfill-loai: pure _infer_loai (tên+số hiệu → loai chuẩn), offline ─────
    cases.append(("infer_loai_name_and_sohieu",
                  _infer_loai("BLDS_91-2015-QH13_Bo_luat_Dan_su", "91/2015/QH13") == "Bộ luật"
                  and _infer_loai("Luat_109-2025-QH15_Thue_TNCN", "109/2025/QH15") == "Luật"
                  and _infer_loai("VBHN_18-VBHN-VPQH_BLLD", "18/VBHN-VPQH") == "Văn bản hợp nhất"
                  and _infer_loai("002 Nghi dinh 145", "145/2020/NĐ-CP") == "Nghị định"
                  and _infer_loai("x", "10/2020/TT-BYT") == "Thông tư"
                  and _infer_loai("khong ro", "") == ""
                  and all((_infer_loai(n, s) in _LOAI_CANON_VALUES or _infer_loai(n, s) == "")
                          for n, s in [("a", "b"), ("Luat_x", "1/2020/QH14"), ("NQ_x", "5/2020/NQ-CP")])))
    # ───── KH1 Pha 1.5 — registry-doctor tách SOHIEU_CONFLICT_DIFFERENT_DOC vs SAME_DOC (sidecar), offline ─────
    _rh2 = _imp("registry_hygiene")
    _rep_c = _rh2.analyze(_rh2.entries({"entries": [
        {"so_hieu": "67/2006/QH11", "name": "Luat_67-2006-QH11_CNTT", "drive_id": "c1"},
        {"so_hieu": "67/2006/QH11", "name": "Luat_67-2006-QH11_NLD_di_lam_viec_nuoc_ngoai.doc", "drive_id": "c2"},
        {"so_hieu": "91/2015/QH13", "name": "BLDS_91-2015-QH13_Bo_luat_Dan_su", "drive_id": "s1"},
        {"so_hieu": "91/2015/QH13", "name": "BLDS_91-2015-QH13_Bo_luat_Dan_su.docx", "drive_id": "s2"},
    ]}))
    _k67, _k91 = norm_sohieu("67/2006/QH11"), norm_sohieu("91/2015/QH13")
    cases.append(("registry_doctor_sohieu_conflict_split",
                  _k67 in _rep_c["sohieu_conflict_different_doc"]
                  and _k91 in _rep_c["sohieu_dup_same_doc"]
                  and _k91 not in _rep_c["sohieu_conflict_different_doc"]))
    # ───── KH1 Pha 1.5 — missing-sohieu: parse số hiệu từ TÊN (bỏ Mẫu/Phụ lục), offline ─────
    cases.append(("missing_sohieu_parse_from_name",
                  _parse_sohieu_from_name("143_2025_QH15_681550.docx") == "143_2025_QH15"
                  and _parse_sohieu_from_name("Mau_04_2025_QH15.docx") == ""
                  and _parse_sohieu_from_name("Luat Cong doan khong so") == ""))
    # ───── REGRESSION 1.23.5 — missing-sohieu --apply PHẢI ghi cột `sohieu` (KHÔNG `so_hieu`, webapp bỏ im lặng) ─────
    try:
        import inspect as _insp
        _ms_src = _insp.getsource(cmd_missing_sohieu)
        cases.append(("missing_sohieu_reg_bulk_col_sohieu",
                      'cols="sohieu"' in _ms_src and 'cols="so_hieu"' not in _ms_src
                      and '"sohieu": s["sohieu_suggested"]' in _ms_src))
    except Exception:
        cases.append(("missing_sohieu_reg_bulk_col_sohieu", False))
    # ───── REGRESSION 1.23.6 (cập nhật 2026-07-02) — recat PHẢI LOUD + rc=1 khi ghi HỤT THẬT (miss), KHÔNG cảnh báo giả
    # khi patched=0 do cat đã đúng (idempotent). Cờ hụt = `not v.get("verified")` (verified nay dựa `missed`, KHÔNG patched).
    try:
        import inspect as _insp2
        _rc_src = _insp2.getsource(cmd_recat)
        cases.append(("recat_warns_on_real_miss_not_idempotent",
                      'not v.get("verified")' in _rc_src and "return 1" in _rc_src
                      and "KHÔNG khớp drive_id" in _rc_src and "patched < len(ids)" not in _rc_src))
    except Exception:
        cases.append(("recat_warns_on_real_miss_not_idempotent", False))
    # ───── 1.23.7 — BẤT BIẾN số hiệu VBHN PHẢI có NĂM: inject năm + quét fixable/needs ─────
    cases.append(("vbhn_sohieu_inject_year",
                  _vbhn_sohieu_inject_year("61-VBHN-VPQH", 2025) == "61-2025-VBHN-VPQH"
                  and _vbhn_sohieu_inject_year("61/VBHN-VPQH", 2026) == "61-2026-VBHN-VPQH"
                  and _vbhn_sohieu_inject_year("18-VBHN-BTC", 2026) == "18-2026-VBHN-BTC"
                  and _vbhn_sohieu_inject_year("61-2025-VBHN-VPQH", 2025) is None   # đã có năm → bỏ
                  and _vbhn_sohieu_inject_year("41-2024-QH15", 2024) is None        # không phải VBHN → bỏ
                  and _vbhn_sohieu_inject_year("61-VBHN-VPQH", None) is None))
    cases.append(("vbhn_name_inject_year",
                  _name_inject_vbhn_year("VBHN_61-VBHN-VPQH_An_toan_thuc_pham", "61", 2025, "VPQH")
                  == "VBHN_61-2025-VBHN-VPQH_An_toan_thuc_pham"))
    cases.append(("vbhn_year_fix_items_split",
                  (lambda fx, nd, cf: len(fx) == 1 and fx[0]["new_sohieu"] == "14-2024-VBHN-VPQH" and len(nd) == 1 and len(cf) == 0)
                  (*_vbhn_year_fix_items([
                      {"drive_id": "d1", "sohieu": "14-VBHN-VPQH", "name": "VBHN ATVSLD", "issue_year": "2024", "corpus": "true"},
                      {"drive_id": "d2", "sohieu": "14-VBHN-VPQH", "name": "VBHN NLD nuoc ngoai", "corpus": "true"},  # không suy được năm
                      {"drive_id": "d3", "sohieu": "41-2024-QH15", "name": "Luat BHXH", "corpus": "true"},            # không phải VBHN
                      {"drive_id": "d4", "sohieu": "14-VBHN-VPQH", "name": "VBHN ATVSLD sidecar", "issue_year": "2024", "corpus": "false"},  # corpus=false → BỎ
                  ]))))
    # safeguard: 2 dòng suy ra CÙNG new_sohieu → conflicts (KHÔNG fixable, tránh tạo collision mới)
    cases.append(("vbhn_year_fix_conflict_detect",
                  (lambda fx, nd, cf: len(fx) == 0 and len(cf) == 2 and cf[0]["new_sohieu"] == "62-2026-VBHN-VPQH")
                  (*_vbhn_year_fix_items([
                      {"drive_id": "c1", "sohieu": "62-VBHN-VPQH", "name": "VBHN A 2026", "issue_year": "2026", "corpus": "true"},
                      {"drive_id": "c2", "sohieu": "62-VBHN-VPQH", "name": "VBHN B 2026", "issue_year": "2026", "corpus": "true"},
                  ]))))
    # ───── A1 (1.23.11) — source-map gate: cross-DOMAIN không strong-match → KHÔNG ghim canonical ─────
    # 'Bộ luật Lao động' KHÔNG được ghim 'Luật Dân chủ cơ sở' (khác chủ đề, _name_strong_match=False → null + LOW_CONFIDENCE).
    _bll = {"drive_id": "bll", "name": "VBHN_18_Bo_luat_Lao_dong", "sohieu": "", "corpus": "true"}
    _danchu = {"drive_id": "dc", "name": "VBHN_87_Luat_Dan_chu_co_so", "sohieu": "", "corpus": "true"}
    # ép cả 2 vào by_name bằng query khớp-mờ cả hai ('luật ... cơ sở' không có) — dùng đường _name_strong_match trực tiếp:
    cases.append(("source_map_cross_domain_not_strong",
                  _name_strong_match("Bộ luật Lao động", _bll["name"]) is True
                  and _name_strong_match("Bộ luật Lao động", _danchu["name"]) is False))
    # A1 (port Codex, subject-gate): 'Bộ luật Lao động hợp nhất' ghim BLLĐ (BLLD abbrev) KHÔNG ghim Dân chủ 87;
    # hit generic không chủ đề → canonical=None + SUBJECT_MISMATCH.
    _sm_blld = _source_map_one("Bộ luật Lao động hợp nhất", [
        {"id": "bad", "name": "VBHN_87-VPQH_2025_Luat_Dan_chu_co_so", "so_hieu": "87/VBHN-VPQH", "cat": "08", "corpus": "true", "nlm_source_id": "bad", "loai": "VBHN"},
        {"id": "good", "name": "VBHN_18-VBHN-VPQH_2025_Luat_BLLD_HopNhat", "so_hieu": "18/VBHN-VPQH", "cat": "20", "corpus": "true", "nlm_source_id": "good", "loai": "VBHN"},
    ])
    cases.append(("source_map_name_subject_gate_blld",
                  (_sm_blld.get("canonical") or {}).get("drive_id") == "good"))
    _sm_blld_none = _source_map_one("Bộ luật Lao động hợp nhất", [
        {"id": "generic", "name": "Luat", "so_hieu": "87/VBHN-VPQH", "cat": "08", "corpus": "true", "nlm_source_id": "bad", "loai": "VBHN"},
    ])
    cases.append(("source_map_name_subject_no_false_canonical",
                  _sm_blld_none.get("canonical") is None
                  and any("SUBJECT_MISMATCH" in w for w in _sm_blld_none.get("warnings", []))))
    cases.append(("resolve_identity_name_tokens_thu_vien",
                  bool(resolve_identity("Luật Thư viện", [
                      {"name": "Luat_46-2019-QH14_Thu_vien", "so_hieu": "46/2019/QH14", "cat": "32"}]))))
    # ───── COMPOSITE `tl sweep` — pure _sweep_report tổng hợp + next_actions điền sẵn (offline) ─────
    _swr = _sweep_report([
        {"drive_id": "a", "name": "VBHN_19_BHXH", "sohieu": "19-VBHN-VPQH", "corpus": "true", "issue_year": "2026"},
        {"drive_id": "b", "name": "Luat_X", "sohieu": "41-2024-QH15", "corpus": "true"},
    ])
    cases.append(("sweep_report_shape",
                  _swr["total"] == 2 and _swr["vbhn_year"]["fixable"] == 1
                  and "next_actions" in _swr and any("vbhn-year-fix" in x for x in _swr["next_actions"])))
    # ───── NLM status FAMILY — biến thể removed_* KHÔNG false-fire NLM_STATUS_MISMATCH + tính ĐÚNG removed/live ─────
    cases.append(("nlm_status_family_recognition",
                  _nlm_status_known("removed_superseded_by_VBHN") and _nlm_status_known("removed_dedup")
                  and _nlm_status_known("pushed") and _nlm_status_known("") and not _nlm_status_known("weird_label")
                  and _nlm_status_removed("removed_superseded_by_VBHN") and _nlm_status_removed("trashed")
                  and not _nlm_status_removed("pushed")
                  and _entry_on_nlm_live({"nlm_source_id": "s", "nlm_status": "pushed"}) is True
                  and _entry_on_nlm_live({"nlm_source_id": "s", "nlm_status": "removed_superseded_by_VBHN"}) is False))
    # NLM_STATUS_MISMATCH KHÔNG còn fire trên removed_superseded_by_VBHN (false-fire cũ)
    cases.append(("nlm_status_mismatch_no_false_fire",
                  "NLM_STATUS_MISMATCH" not in _title_flags({"nlm_source_id": "s", "nlm_status": "removed_superseded_by_VBHN", "name": "x"})
                  and "NLM_STATUS_MISMATCH" in _title_flags({"nlm_source_id": "s", "nlm_status": "weird_label", "name": "x"})))
    # ───── FALSE-LINK NLM — ≥2 drive_id cùng 1 nlm_source_id (ca NQ42 user gặp; detector cho sweep) ─────
    _ssg = _shared_source_id_groups([
        {"drive_id": "d1", "name": "NQ42 canonical", "sohieu": "42-2023-NQ-TW", "nlm_source_id": "S1"},
        {"drive_id": "d2", "name": "NQ42 ghost", "sohieu": "42-2023-NQ-TW", "nlm_source_id": "S1"},
        {"drive_id": "d3", "name": "khac", "sohieu": "x", "nlm_source_id": "S2"},
    ])
    cases.append(("shared_source_id_detect",
                  len(_ssg) == 1 and _ssg[0]["source_id"] == "S1" and len(_ssg[0]["rows"]) == 2))
    # ───── 5.2 (report rà 106 Luật) — vbhn-check goc_hit cross-subject KHÔNG lọt khi đã biết subject ─────
    _vc52 = _vbhn_candidates([
        {"name": "VBHN_14-2024-VBHN-VPQH_ATVSLD", "sohieu": "14-2024-VBHN-VPQH", "loai": "VBHN", "cat": "20", "nlm_source_id": "x", "goc": "09-2017-QH14"},
    ], subject="du lịch", goc="09-2017-QH14")
    cases.append(("vbhn_candidates_goc_cross_subject_drop", len(_vc52) == 0))
    _vc52b = _vbhn_candidates([
        {"name": "VBHN_09-VPQH_Du_lich", "sohieu": "09-VBHN-VPQH", "loai": "VBHN", "cat": "22", "nlm_source_id": "y", "goc": "09-2017-QH14"},
    ], subject="du lịch", goc="09-2017-QH14")
    cases.append(("vbhn_candidates_goc_same_subject_keep", len(_vc52b) >= 1))
    # ───── GUARD registryDocId Doc-legacy 1mATG (sự cố 2026-06-30: config trỏ Doc → webapp đọc rỗng count=0 ẢO) ─────
    try:
        import inspect as _insp4
        cases.append(("legacy_registry_doc_guard",
                      _LEGACY_REGISTRY_DOC_ID.startswith("1mATG")
                      and "_LEGACY_REGISTRY_DOC_ID" in _insp4.getsource(cmd_doctor)
                      and "AUTO-HEAL" in _insp4.getsource(cmd_init_config)))
    except Exception:
        cases.append(("legacy_registry_doc_guard", False))
    # ───── GUARD chống clobber registry NỀN (sự cố 2026-06-30: profile registryDocId rỗng → xóa base) ─────
    try:
        import inspect as _insp3
        _src_pr = _insp3.getsource(cmd_profile_rebuild_registry)
        _src_mf = _insp3.getsource(cmd_manifest)
        cases.append(("profile_registry_clobber_guard",
                      "PROFILE_REGISTRY_ID_EMPTY_WOULD_CLOBBER_BASE" in _src_pr
                      and "PROFILE_REGISTRY_ID_EMPTY_WOULD_CLOBBER_BASE" in _src_mf
                      and "TL_REGISTRY_DOC_ID" in _src_pr))
    except Exception:
        cases.append(("profile_registry_clobber_guard", False))
    # ───── infra-in-corpus detector — .enc/.json/secrets/delta lẫn corpus=true = RÁC (bảo vệ văn bản thật) ─────
    cases.append(("infra_in_corpus_detect",
                  _is_infra_entry({"name": "tl_secrets.enc"})
                  and _is_infra_entry({"name": "nlm_sources_delta_2026-06-11.json"})
                  and not _is_infra_entry({"name": "Luat_106-2025-QH15_THADS", "mime": "application/vnd.google-apps.document"})
                  and not _is_infra_entry({"name": "80-nd-cp.signed.pdf", "mime": "application/pdf"})))
    # ───── COMPOSITE `tl dedup-plan` — giữ canonical, quarantine dup; KHÔNG đụng canonical cụm khác ─────
    _dp = _dedup_plan([
        {"drive_id": "g", "name": "VBHN_19_BHXH_HopNhat", "sohieu": "19-2026-VBHN-VPQH", "cat": "02", "corpus": "true", "nlm_source_id": "s1", "nlm_status": "pushed", "mime": "application/vnd.google-apps.document", "md5": "M"},
        {"drive_id": "d", "name": "VBHN_19_BHXH_HopNhat.docx", "sohieu": "19-2026-VBHN-VPQH", "cat": "02", "corpus": "true", "md5": "M"},
    ])
    _ready_ids = [d["drive_id"] for it in _dp["ready"] for d in it["quarantine"]]
    cases.append(("dedup_plan_keeps_canonical",
                  _dp["total_quarantine"] == 1 and "d" in _ready_ids and "g" not in _ready_ids))
    # ───── COMPOSITE `tl quarantine-fix` — phân loại dọn quarantine mâu thuẫn (pure) ─────
    _qf = _quarantine_fix_items([
        {"drive_id": "r", "name": "Luat so 41_2024_BHXH.pdf", "sohieu": "", "cat": "_ZZZ_QUARANTINE_taluat", "corpus": "true"},
        {"drive_id": "g", "name": "VBHN_18_BLLD", "sohieu": "18-VBHN-VPQH", "cat": "QUARANTINE", "corpus": "true", "mime": "application/vnd.google-apps.document"},
        {"drive_id": "h", "name": "NQ_42", "sohieu": "42-2023-NQ-TW", "cat": "_ZZZ_QUARANTINE_taluat", "corpus": "false", "nlm_source_id": "s1", "nlm_status": "pushed"},
    ])
    cases.append(("quarantine_fix_classify",
                  len(_qf["set_corpus_false"]) == 1 and len(_qf["review_restore"]) == 1
                  and len(_qf["normalize_label"]) >= 1 and len(_qf["ghost_nlm"]) == 1))
    # ───── A2 (1.23.11) — nhãn quarantine biến thể (code 'QUARANTINE' ≠ chuẩn QUARANTINE_CAT) ─────
    cases.append(("quarantine_label_variant",
                  _is_quarantine_label_variant("QUARANTINE")
                  and not _is_quarantine_label_variant(QUARANTINE_CAT)
                  and not _is_quarantine_label_variant("30_Thi_hanh_an")
                  and _is_quarantine_cat(QUARANTINE_CAT) and _is_quarantine_cat("QUARANTINE")))
    # ───── 1.23.10 — GUARD cat hợp lệ (chặn folder rác gõ tay, vd '30_To_chuc_bo_may_nha_nuoc') ─────
    cases.append(("valid_cat_value_guard",
                  _is_valid_cat_value("30") and _is_valid_cat_value("30_Thi_hanh_an")
                  and _is_valid_cat_value("QUARANTINE") and _is_valid_cat_value("")
                  and not _is_valid_cat_value("30_To_chuc_bo_may_nha_nuoc")   # số 30 + tên cat 35 = RÁC
                  and not _is_valid_cat_value("99_Khong_co_that")))
    # ───── KH1 Pha 1.3 (II.5) — slot-audit per-shard: pure _slot_count_all_shards, offline ─────
    cases.append(("slot_count_all_shards",
                  _slot_count_all_shards([
                      {"nlm_notebook_id": "NB-A", "nlm_status": "pushed", "nlm_source_id": "s1"},
                      {"nlm_notebook_id": "NB-A", "nlm_source_id": "s2"},
                      {"nlm_notebook_id": "NB-B", "nlm_status": "pushed", "nlm_source_id": "s3"},
                      {"nlm_notebook_id": "NB-A", "nlm_status": "removed_dedup", "nlm_source_id": "s4"},
                      {"nlm_notebook_id": "", "nlm_status": "pushed", "nlm_source_id": "s5"},
                  ]) == {"NB-A": 2, "NB-B": 1}))
    # ───── KH1 III.2 — edit-skill: cổng assert-đếm (DRY, an toàn), offline ─────
    import tempfile as _tfx
    _esf = Path(_tfx.gettempdir()) / "_selftest_editskill.py"
    _editskill = False
    try:
        _esf.write_text("x = 1\ny = 2\n", encoding="utf-8")
        _ns_ok = argparse.Namespace(file=str(_esf), patch=json.dumps([{"old": "x = 1", "new": "x = 10", "count": 1}]),
                                    patch_file=None, apply=False, config=None, profile=None)
        _ns_bad = argparse.Namespace(file=str(_esf), patch=json.dumps([{"old": "khong-co", "new": "z", "count": 1}]),
                                     patch_file=None, apply=False, config=None, profile=None)
        _buf = _io.StringIO()
        with _ctx.redirect_stdout(_buf), _ctx.redirect_stderr(_buf):
            _rc_ok = _TL_MODULE.cmd_edit_skill(_ns_ok)
            _rc_bad = _TL_MODULE.cmd_edit_skill(_ns_bad)
        _editskill = (_rc_ok == 0 and _rc_bad == 2 and _esf.read_text(encoding="utf-8") == "x = 1\ny = 2\n")  # DRY KHÔNG ghi
    except Exception:
        _editskill = False
    finally:
        try: _esf.unlink()
        except Exception: pass
    cases.append(("edit_skill_assert_count_gate_dry", _editskill))
    # ───── KH1 1.23.2 — nlm-orphans: pure _classify_nlm_sources (active / mismatch-live / unregistered), offline ─────
    _orph = _classify_nlm_sources(
        [{"id": "s1", "title": "Active"}, {"id": "s2", "title": "Mislabel live"}, {"id": "s3", "title": "Unregistered"}],
        [{"nlm_source_id": "s1", "nlm_status": "pushed", "drive_id": "d1", "name": "A", "so_hieu": "1/2020/QH14", "corpus": "true"},
         {"nlm_source_id": "s2", "nlm_status": "removed_from_drive", "drive_id": "d2", "name": "B", "so_hieu": "66", "corpus": "false"}])
    cases.append(("nlm_orphans_classify_3way",
                  _orph["registered_active"] == 1
                  and _orph["mismatch_count"] == 1 and _orph["status_mismatch_live"][0]["source_id"] == "s2"
                  and _orph["status_mismatch_live"][0]["drive_id"] == "d2"
                  and _orph["unregistered_count"] == 1 and _orph["unregistered"][0]["source_id"] == "s3"))
    # ───── 1.23.3 — GUARD: header SKILL.md PHẢI khớp VERSION (chống lỗi 'deploy thấy version cũ' do quên sed SKILL.md) ─────
    try:
        _skmd = (Path(__file__).resolve().parent.parent / "SKILL.md").read_text(encoding="utf-8")[:1500]
        cases.append(("skill_md_version_matches_VERSION", ("v" + VERSION) in _skmd))
    except Exception:
        cases.append(("skill_md_version_matches_VERSION", False))
    # ───── v1.33.37 (MERGE bundle-14) — ENFORCEMENT #15: SKILL.md PHẢI khai §15 SCRIPT-REUSE GATE + token
    # SCRIPT_REUSE_GATE. Selftest ĐỎ nếu doctrine #15 bị xoá khỏi SKILL.md (chống trôi nguyên tắc kiểm-kho). ─────
    try:
        _skmd_full = (Path(__file__).resolve().parent.parent / "SKILL.md").read_text(encoding="utf-8")
        cases.append(("skill_md_has_script_reuse_gate",
                      ("SCRIPT-REUSE GATE" in _skmd_full) and ("SCRIPT_REUSE_GATE" in _skmd_full)))
    except Exception:
        cases.append(("skill_md_has_script_reuse_gate", False))
    # ───── KH1 Pha 1.5 — relation-backfill: pure _relation_backfill_items (set goc + MERGE sua_doi, không đè), offline ─────
    _ml_rb = [
        {"action": "BACKFILL_GOC_ON_AMENDMENT", "drive_id": "a1", "sohieu": "90/2025/QH15", "set_goc": "19/2012/QH13"},
        {"action": "BACKFILL_SUA_DOI_ON_BASE", "drive_id": "b1", "sohieu": "19/2012/QH13", "add": ["90/2025/QH15"]},
    ]
    _rbi = _relation_backfill_items(_ml_rb, [{"drive_id": "b1", "sua_doi": "50/2024/QH15"}])   # base đã có 1 sua_doi → merge
    _g = [i for i in _rbi if "goc" in i]
    _s = [i for i in _rbi if "sua_doi" in i]
    cases.append(("relation_backfill_items_merge",
                  len(_rbi) == 2
                  and bool(_g) and _g[0]["drive_id"] == "a1" and _g[0]["goc"] == "19/2012/QH13" and _g[0]["_cols"] == "goc"
                  and bool(_s) and _s[0]["drive_id"] == "b1"
                  and "90/2025/QH15" in _s[0]["sua_doi"] and "50/2024/QH15" in _s[0]["sua_doi"]))
    # ───── KH1 1.23.1 — overflow-resolve PHYSICAL-aware: MAX(registry,physical) + REGISTRY_BEHIND_LIVE gap (offline) ─────
    _ost = _overflow_status(279, 315, "OV-1", 39, 39)        # base reg 279 / vật lý 315 (vượt cap) → hiệu lực 315
    cases.append(("overflow_status_physical_truth",
                  _ost["base_used"] == 315                                    # MAX(279,315) — KHÔNG under-count
                  and _ost["flag"] == "OVERFLOW_SHARD_EXISTS_DO_NOT_CREATE"   # base đầy thật → dùng overflow
                  and any(g["shard"] == "base" and g["gap"] == 36 for g in _ost["registry_live_gap"])
                  and _overflow_status(100, None, "OV-1", 0, None)["flag"] == "BASE_HAS_ROOM"
                  and _overflow_status(300, 300, "", 0, None)["flag"] == "ALL_SHARDS_FULL_ASK_USER_BEFORE_CREATE"
                  and _overflow_status(279, None, "OV-1", 39, None)["registry_live_gap"] == []))  # không physical → không gap giả
    # Bug A (log rà 71 luật): `tl status` verdict REVIEW là PHÁT HIỆN dữ liệu (A3 EXIT CODE), KHÔNG phải lệnh lỗi.
    # preingest_gate.verdict_exit: rc=0 mặc định cho ADD/SKIP/REVIEW; rc=1 chỉ khi --strict + REVIEW (mirror xref).
    try:
        _pg = _imp("preingest_gate")
        _rev = _pg.decide({"status": "IN_REGISTRY_HIEULUC_UNKNOWN"})
        _add = _pg.decide({"status": ""})
        cases.append(("status_verdict_review_then_add",
                      _rev["decision"] == "REVIEW" and _add["decision"] == "ADD"))
        cases.append(("status_review_rc0_unless_strict",
                      _pg.verdict_exit("REVIEW", False) == 0
                      and _pg.verdict_exit("REVIEW", True) == 1
                      and _pg.verdict_exit("ADD", True) == 0
                      and _pg.verdict_exit("SKIP", True) == 0))
    except Exception as _e:  # noqa: BLE001
        cases.append(("status_review_rc0_unless_strict", False))
    # Bug E (log rà 71 luật): standardize_name bỏ đuôi .doc/.docx/.pdf khỏi TÊN CHUẨN (GoogleDoc) nhưng
    # GIỮ đuôi thật cho tên FILE gốc (build_file_name). 5 luật rò '.docx'/'.doc' vào tên chuẩn.
    try:
        _sn = _imp("standardize_name")
        cases.append(("standardize_name_strips_ext",
                      _sn.build_doc_name("Luat", "57/2024/QH15", "Bao_hiem_y_te.docx") == "Luat_57-2024-QH15_Bao_hiem_y_te"
                      and _sn.build_doc_name("Luat", "60/2024/QH15", "Phong benh.doc") == "Luat_60-2024-QH15_Phong_benh"
                      and _sn.build_file_name("Luat", "57/2024/QH15", "Bao_hiem_y_te.docx", "docx") == "Luat_57-2024-QH15_Bao_hiem_y_te.docx"
                      and _sn.build_doc_name("Luat", "01/2025/QH15", "Dan so") == "Luat_01-2025-QH15_Dan_so"))
    except Exception as _e:  # noqa: BLE001
        cases.append(("standardize_name_strips_ext", False))
    # Bug P2-6 (log rà 71 luật): vbhn-check chỉ ép CONTENT_VERIFY khi collision CỦA CHÍNH số hiệu ứng viên
    # (KHÔNG phải collision toàn corpus — gốc rễ nhiễu 86 lần). Ứng viên verified+năm+duy nhất+không tự-collision → tin.
    try:
        _p26 = [
            {"id": "a1", "name": "VBHN_99-VBHN-VPQH_Luat_X", "so_hieu": "99/VBHN-VPQH", "loai": "VBHN", "cat": "20"},
            {"id": "a2", "name": "VBHN_99-VBHN-VPQH_Luat_Y", "so_hieu": "99/VBHN-VPQH", "loai": "VBHN", "cat": "21"},
            {"id": "b1", "name": "VBHN_88-VBHN-VPQH_Luat_Sach", "so_hieu": "88/VBHN-VPQH",
             "loai": "VBHN", "cat": "20", "verified": "yes", "nam": "2024", "hieuluc": "Còn"},
        ]
        _scan26 = _vbhn_scan(_p26)
        _bkey = norm_sohieu("88/VBHN-VPQH")
        _self_col_88 = any(c["key"] == _bkey for c in _scan26["collisions"])
        cases.append(("vbhn_check_self_collision_not_corpus_wide",
                      bool(_scan26["collisions"]) and not _self_col_88
                      and bool(_entry_confirmed(_p26[2])) and bool(_entry_years(_p26[2]))
                      and not _entry_confirmed(_p26[0])))
    except Exception as _e:  # noqa: BLE001
        cases.append(("vbhn_check_self_collision_not_corpus_wide", False))
    # Bug B + P1-3 (log rà): xref dedup theo SỐ HIỆU → mệnh đề chuyển tiếp ("…này có hiệu lực thi hành…") quanh
    # CÙNG 1 số hiệu KHÔNG sinh phantom; tên prose bị cắt; tên luật thật ("Thi hành án dân sự") KHÔNG bị cắt nhầm.
    _phantom = ("Nghị quyết số 258/2025/QH15 quy định. Nghị quyết này có hiệu lực thi hành thì thực hiện "
                "theo Nghị quyết số 258/2025/QH15. Áp dụng Nghị quyết số 258/2025/QH15.")
    _pr = extract_refs(_phantom)
    cases.append(("xref_dedup_phantom_one_per_sohieu",
                  sum(1 for r in _pr if r["sohieu"] == "258-2025-QH15") == 1))
    _legit = extract_refs("Luật Thi hành án dân sự số 26/2008/QH12.")
    cases.append(("xref_name_phrase_keeps_real_title",
                  any(r["sohieu"] == "26-2008-QH12" and "Thi hành án dân sự" in r["name_phrase"] for r in _legit)))
    # Bug P0-2: DOC_TEXT_SOHIEU_TYPO KHÔNG bắc cầu QUA HỌ loại VB (QH ↔ NQ-TW/NĐ-CP); CÙNG họ (QH14↔QH15) vẫn flag.
    _p02ents = [{"so_hieu": "29/2013/NQ-TW", "name": "NQ TW", "cat": "99"},
                {"so_hieu": "39/2019/ND-CP", "name": "ND", "cat": "99"}]
    cases.append(("xref_typo_no_cross_doctype",
                  _sohieu_typo_near("29-2013-QH13", _p02ents, "Luật KHCN") is None
                  and _sohieu_typo_near("39-2019-QH14", _p02ents, "Luật Đầu tư công") is None
                  and _doctype_family("QH13") == "QH" and _doctype_family("NQ-TW") == "TW"
                  and _doctype_family("QH14") == _doctype_family("QH15")))
    # Bug P1-5 (log rà): văn bản PHI quy phạm (sohieu=∅ + "góp ý/kiến nghị/ý kiến") KHÔNG vào amendment_candidates
    # và KHÔNG escalate PAUSE; có ứng viên MANG SỐ HIỆU mới escalate.
    _p15base = [{"id": "base", "name": "VBHN_19-VBHN-VPQH_Bao_hiem_xa_hoi", "so_hieu": "19/VBHN-VPQH", "loai": "VBHN", "cat": "06", "corpus": "true"},
                {"id": "gy", "name": "006. Agribank- gop y kien nghi sua doi luat BHXH.pdf", "so_hieu": "", "loai": "", "cat": "06", "corpus": "true"}]
    _sm15 = _source_map_one("19/VBHN-VPQH", _p15base)
    cases.append(("amendment_rejects_nonnormative_opinion",
                  len(_sm15["amendment_candidates"]) == 0 and _sm15["action_required"] is None))
    _sm15b = _source_map_one("19/VBHN-VPQH", _p15base + [
        {"id": "sd", "name": "Luat_97-2025-QH15_SuaDoi_BHXH", "so_hieu": "97/2025/QH15", "loai": "Luat", "cat": "06", "corpus": "true", "goc": "19/VBHN-VPQH"}])
    cases.append(("amendment_pause_when_normative_present", _sm15b["action_required"] == "PAUSE_AND_ASK_USER"))
    # Bug P1-4 (log rà): >1 VBHN CÙNG số hiệu KHÁC chủ đề → canonical=None + cảnh báo; CÙNG chủ đề → vẫn chốt.
    _sm14 = _source_map_one("89/VBHN-VPQH", [
        {"id": "nsnn", "name": "VBHN_89-VBHN-VPQH_Ngan_sach_nha_nuoc", "so_hieu": "89/VBHN-VPQH", "loai": "VBHN", "cat": "26", "corpus": "true"},
        {"id": "mttq", "name": "VBHN_89-VBHN-VPQH_Mat_tran_to_quoc", "so_hieu": "89/VBHN-VPQH", "loai": "VBHN", "cat": "36", "corpus": "true"}])
    cases.append(("source_map_vbhn_reuse_diff_subject_no_canonical",
                  _sm14["canonical"] is None and any("VBHN_REUSE_AMBIGUOUS_NO_CANONICAL" in w for w in _sm14["warnings"])))
    _sm14b = _source_map_one("40/VBHN-VPQH", [
        {"id": "v1", "name": "VBHN_40-VBHN-VPQH_Bao_hiem_y_te", "so_hieu": "40/VBHN-VPQH", "loai": "VBHN", "cat": "45", "corpus": "true"},
        {"id": "v2", "name": "VBHN_40-VBHN-VPQH_Bao_hiem_y_te", "so_hieu": "40/VBHN-VPQH", "loai": "VBHN", "cat": "45", "corpus": "true"}])
    cases.append(("source_map_vbhn_reuse_same_subject_keeps_canonical", _sm14b["canonical"] is not None))
    # Bug G (log rà): file thô .docx cạnh GDoc canonical mà corpus=true → vào sidecar_corpus_fix (đề xuất corpus=false).
    _gfx = [{"id": "gdoc", "name": "Luat_57-2024-QH15_Bao_hiem_y_te", "so_hieu": "57/2024/QH15", "loai": "Luật", "cat": "45", "corpus": "true", "nlm_source_id": "src1", "nlm_status": "pushed"},
            {"id": "side", "name": "Luat_57-2024-QH15_Bao_hiem_y_te.docx", "so_hieu": "57/2024/QH15", "loai": "Luật", "cat": "45", "corpus": "true"}]
    _gg = _hygiene_groups(_gfx)
    cases.append(("hygiene_sidecar_corpus_fix_detected",
                  len(_gg["sidecar_corpus_fix"]) == 1
                  and _gg["sidecar_corpus_fix"][0]["name"].endswith(".docx")))
    # Bug P2-7 (log rà): chuẩn hoá enum loai/hieuluc + bucket hygiene loai_noncanonical (KHÔNG nhồi _title_flags).
    cases.append(("normalize_loai_enum",
                  _normalize_loai("Luat") == "Luật" and _normalize_loai("VBHN") == "Văn bản hợp nhất"
                  and _normalize_loai("nd") == "Nghị định" and _normalize_loai("ttlt") == "Thông tư liên tịch"
                  and _normalize_loai("XYZ") == "XYZ"))
    cases.append(("normalize_hieuluc_enum",
                  _normalize_hieuluc("Con") == "Còn" and _normalize_hieuluc("thay the") == "Hết"
                  and _normalize_hieuluc("01/07/2026") == "01/07/2026"))
    _p27 = _hygiene_groups([
        {"id": "a", "name": "x", "so_hieu": "1/2020/QH14", "loai": "VBHN", "cat": "35", "corpus": "true"},
        {"id": "b", "name": "y", "so_hieu": "2/2020/QH14", "loai": "Luật", "cat": "35", "corpus": "true"}])
    cases.append(("hygiene_loai_noncanonical_bucket",
                  len(_p27["loai_noncanonical"]) == 1 and _p27["loai_noncanonical"][0].get("loai") == "VBHN"
                  and "LOAI_NONCANONICAL" not in _title_flags(_p27["loai_noncanonical"][0])))
    # HỢP NHẤT Codex v1.22.69 — deep-resolver: GDoc native thắng sidecar raw cùng số hiệu; tên DÀI toàn chữ-gạch
    # dưới resolve theo TÊN (không bị nhận nhầm DriveId = bug C trọn vẹn); ENTRY_RAW_NO_GDOC rc=2.
    _mres = [
        {"id": "g", "name": "VBHN_18-VBHN-VPQH_Bo_luat_Lao_dong", "so_hieu": "18/VBHN-VPQH", "cat": "20", "corpus": "true", "nlm_source_id": "s1", "mime": "application/vnd.google-apps.document"},
        {"id": "s", "name": "18_VBHN-VPQH_699429.docx", "so_hieu": "18/VBHN-VPQH", "cat": "20", "corpus": "true", "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
        {"id": "c", "name": "Luat_Phong_chong_benh_truyen_nhiem", "so_hieu": "", "cat": "45", "corpus": "true", "drive_id": "DRV_pcbtn"},
    ]
    _b, _gid, _nm, _h = _resolve_deep_target("18/VBHN-VPQH", _mres)
    cases.append(("deep_resolver_prefers_gdoc", _b is not None and _entry_google_doc(_b) and not _entry_raw_no_gdoc(_b)))
    _b2, _gid2, _nm2, _h2 = _resolve_deep_target("Luat_Phong_chong_benh_truyen_nhiem", _mres)
    cases.append(("deep_resolver_long_name_not_driveid", _gid2 == "DRV_pcbtn"))
    with _hush():   # in JSON ENTRY_RAW_NO_GDOC là hành vi đang test — nuốt khỏi console deploy
        _er_rc10 = _emit_raw_no_gdoc("x.docx", True)
    cases.append(("emit_raw_no_gdoc_rc2", _er_rc10 == 2))
    # HỢP NHẤT Codex — _classify_ref kiểm VBHN-coverage TRƯỚC TYPO/MISSING (số hiệu gốc đã có VBHN → OUTDATED).
    _vcov = [{"id": "v", "name": "VBHN_11-VBHN-VPQH_PCTH_thuoc_la", "so_hieu": "11/VBHN-VPQH", "cat": "45", "corpus": "true", "goc": "09/2012/QH13;28/2018/QH14"}]
    _clv = _classify_ref({"raw": "x", "name_phrase": "PCTH thuoc la", "sohieu": "09-2012-QH13", "loai": "Luật"}, _vcov)
    cases.append(("xref_vbhn_coverage_before_typo", _clv["flag"] == "OUTDATED"))
    # Group B (log rà mới): _ingest_target dùng NOTEBOOK CỦA PROFILE (TL_NOTEBOOK_ID), không hard-code VBQPPL base.
    import os as _os
    _prev = _os.environ.get("TL_NOTEBOOK_ID"); _prevov = _os.environ.get("TL_OVERFLOW_NOTEBOOK_ID")
    try:
        _os.environ["TL_NOTEBOOK_ID"] = "NB_PROFILE_X"; _os.environ.pop("TL_OVERFLOW_NOTEBOOK_ID", None)
        _tgt, _ = _ingest_target(None, "1/2020/QH14", "x")
        cases.append(("ingest_target_uses_profile_notebook", _tgt == "NB_PROFILE_X"))
    except Exception:
        cases.append(("ingest_target_uses_profile_notebook", False))
    finally:
        _os.environ.pop("TL_NOTEBOOK_ID", None) if _prev is None else _os.environ.__setitem__("TL_NOTEBOOK_ID", _prev)
        if _prevov is not None:
            _os.environ["TL_OVERFLOW_NOTEBOOK_ID"] = _prevov
    # Group C1 (log rà mới): nlm-reconcile bắc cầu gdoc↔source_id — NLM source khớp drive_id của registry row thiếu
    # source_id → link_candidate (KHÔNG còn 'unregistered'); back-compat nhận set(ids) cũ.
    _c1ents = [{"id": "e1", "name": "VBHN_19_BHXH", "so_hieu": "19/VBHN-VPQH", "drive_id": "DRVabcdefghijklmnopqrst"}]
    _c1src = [{"id": "src-1", "title": "BHXH", "url": "https://docs.google.com/document/d/DRVabcdefghijklmnopqrst/edit"}]
    _c1pl = _nlm_reconcile_plan(_c1src, _c1ents, "NB1")
    cases.append(("nlm_reconcile_link_gdoc_to_source",
                  len(_c1pl["link_candidates"]) == 1 and _c1pl["link_candidates"][0]["by"] == "drive_id" and not _c1pl["unregistered"]))
    cases.append(("nlm_reconcile_set_backcompat", _nlm_reconcile_plan({"src-x"}, _c1ents, "NB1")["unregistered"] == ["src-x"]))
    cases.append(("nlm_source_drive_id_from_url", _nlm_source_drive_id({"url": "https://docs.google.com/document/d/ABCdef1234567890XYZmnop/edit"}) == "ABCdef1234567890XYZmnop"))
    # Group A1 (log rà mới): profile-create GHI BỀN config.profiles.<name> (merge, giữ profile khác).
    import tempfile as _tmp, json as _json2
    _cfgf = _os.path.join(_tmp.gettempdir(), "tl_selftest_cfg.json")
    try:
        open(_cfgf, "w", encoding="utf-8").write(_json2.dumps({"profiles": {"vbqppl": {"rootFolderId": "R0"}}}))
        _pp = _persist_profile_config(_cfgf, "nq36", {"rootFolderId": "RX", "notebookId": "NBX",
                                                       "registryDocId": "SHEET1", "manifestId": "MAN1",
                                                       "manifestScope": "own", "categories": "own"})
        _pd = _json2.loads(open(_cfgf, encoding="utf-8").read())
        cases.append(("persist_profile_config_merge",
                      _pp == _cfgf and _pd["profiles"]["nq36"]["notebookId"] == "NBX"
                      and _pd["profiles"]["nq36"]["categories"] == "own"
                      and _pd["profiles"]["vbqppl"]["rootFolderId"] == "R0"))
        _use = _set_default_profile_config(_cfgf, "nq36")
        _ren = _rename_profile_config(_cfgf, "nq36", "nq36_new")
        _del_refuse = _remove_profile_config(_cfgf, "vbqppl")
        _del = _remove_profile_config(_cfgf, "nq36_new")
        _pd2 = _json2.loads(open(_cfgf, encoding="utf-8").read())
        cases.append(("profile_config_lifecycle",
                      _use.get("ok") and _ren.get("ok") and _del.get("ok")
                      and _del_refuse.get("error") == "REFUSE_DELETE_DEFAULT_PROFILE"
                      and "nq36_new" not in _pd2["profiles"]
                      and _pd2.get("defaultProfile") == "vbqppl"))
    except Exception:
        cases.append(("persist_profile_config_merge", False))
        cases.append(("profile_config_lifecycle", False))
    finally:
        try: _os.remove(_cfgf)
        except Exception: pass
    # Group E1 (log rà mới): nlm_cli strip keyring noise (JSON sạch để parse) + KHÔNG nuốt thân JSON có cụm keyring.
    try:
        _nc = _imp("nlm_cli")
        cases.append(("nlm_cli_strips_keyring",
                      _nc._strip_keyring('Using keyring backend: keyring\n{"ok":1}') == '{"ok":1}'
                      and _nc._strip_keyring('{"e":"Using keyring backend failed"}') == '{"e":"Using keyring backend failed"}'))
    except Exception:
        cases.append(("nlm_cli_strips_keyring", False))
    # Review v70: Group B notebook resolver theo profile — profile DỰ ÁN thiếu notebookId → ERROR (KHÔNG fallback base).
    _pNB = _os.environ.get("TL_NOTEBOOK_ID"); _pPR = _os.environ.get("TL_PROFILE")
    try:
        _os.environ["TL_PROFILE"] = "nq36"; _os.environ.pop("TL_NOTEBOOK_ID", None)
        _nbx, _errx = _resolve_nlm_notebook(None)
        _os.environ["TL_NOTEBOOK_ID"] = "NBnq36"; _nby, _erry = _resolve_nlm_notebook(None)
        _os.environ.pop("TL_PROFILE", None); _os.environ.pop("TL_NOTEBOOK_ID", None)
        _nbz, _errz = _resolve_nlm_notebook(None)
        cases.append(("resolve_nlm_notebook_profile_aware",
                      (_nbx == "" and bool(_errx)) and (_nby == "NBnq36" and not _erry)
                      and (_nbz == NLM_BASE_NOTEBOOK and not _errz)))
    except Exception:
        cases.append(("resolve_nlm_notebook_profile_aware", False))
    finally:
        _os.environ.pop("TL_NOTEBOOK_ID", None) if _pNB is None else _os.environ.__setitem__("TL_NOTEBOOK_ID", _pNB)
        _os.environ.pop("TL_PROFILE", None) if _pPR is None else _os.environ.__setitem__("TL_PROFILE", _pPR)
    # Review v70: C1 KHÔNG false-link khi số hiệu VBHN TÁI DÙNG (>1 dòng cùng số hiệu, source chỉ khớp số hiệu) → bỏ qua.
    _coll_ents = [{"id": "a", "name": "NSNN", "so_hieu": "89/VBHN-VPQH", "drive_id": "D1"},
                  {"id": "b", "name": "MTTQ", "so_hieu": "89/VBHN-VPQH", "drive_id": "D2"}]
    _coll = _nlm_reconcile_plan([{"id": "s1", "title": "x", "sohieu": "89/VBHN-VPQH"}], _coll_ents, "NB1")
    cases.append(("nlm_reconcile_no_falselink_on_sohieu_reuse", len(_coll["link_candidates"]) == 0 and _coll["unregistered"] == ["s1"]))
    # ═══ v1.33.29 (log verify v1.33.28 — doctor pin-check stale · footgun tl_fetch ROOT · NO_SOHIEU số kép ·
    # candidates parity · BrokenPipe rc=1 ma) — r40_* ═══
    # (F1) _resolve_registry_doc_id: env thắng; env rỗng → profile → root; nguồn ghi rõ.
    _cfg40 = _os38.path.join(_tmp38.gettempdir(), "tl_selftest_reg40.json")
    _env40 = {k: _os38.environ.pop(k, None) for k in ("TL_REGISTRY_DOC_ID", "TL_PROFILE")}
    try:
        open(_cfg40, "w", encoding="utf-8").write(json.dumps(
            {"profiles": {"vbqppl": {"registryDocId": "SHEET_PROF"}}, "defaultProfile": "vbqppl",
             "registryDocId": "SHEET_ROOT"}))
        _r40a = _resolve_registry_doc_id(_cfg40, "vbqppl")
        open(_cfg40, "w", encoding="utf-8").write(json.dumps(
            {"profiles": {"vbqppl": {}}, "defaultProfile": "vbqppl", "registryDocId": "SHEET_ROOT"}))
        _r40b = _resolve_registry_doc_id(_cfg40, "vbqppl")
        _os38.environ["TL_REGISTRY_DOC_ID"] = "SHEET_ENV"
        _r40c = _resolve_registry_doc_id(_cfg40, "vbqppl")
    finally:
        for _k40, _v40 in _env40.items():
            if _v40 is not None:
                _os38.environ[_k40] = _v40
            else:
                _os38.environ.pop(_k40, None)
        try:
            _os38.remove(_cfg40)
        except OSError:
            pass
    cases.append(("r40_resolve_registry_doc_id_layers",
                  _r40a[0] == "SHEET_PROF" and _r40a[1].startswith("config:")
                  and _r40b[0] == "SHEET_ROOT" and _r40c == ("SHEET_ENV", "env")))
    # (F4) số hiệu VBHN GỘP 'NN-MM-CQ-CQ' KHÔNG còn cờ NO_SOHIEU oan; tên thật-sự-thiếu-số vẫn cờ.
    cases.append(("r40_compound_sohieu_not_flagged",
                  "NO_SOHIEU_IN_NAME" not in _name_structural_issues("VBHN_73-82-ND-CP_Quan_ly_dau_tu_CNTT_NSNN")
                  and "NO_SOHIEU_IN_NAME" in _name_structural_issues("Luat_Phong_chong_benh_truyen_nhiem")))
    # (F5 → v1.33.30 MERGE bundle-29: STRUCTURED thay compact) source-map item + candidates[] dict đầy đủ
    # sohieu_key/confidence/candidate_type/linked/strong — driver hết gọi thêm review-queue.
    _sm40 = _source_map_one("44/2019/QH14", [
        {"id": "b44", "drive_id": "b44", "name": "Luat_44-2019-QH14_PCTH_ruou_bia", "so_hieu": "44/2019/QH14",
         "loai": "Luật", "cat": "45", "corpus": "true", "nlm_source_id": "s44"},
        {"id": "a44", "drive_id": "a44", "name": "Luat_99-2029-QH17_SuaDoi_PCTH_ruou_bia",
         "so_hieu": "99/2029/QH17", "loai": "Luật", "cat": "45", "corpus": "true"}])
    cases.append(("r40_source_map_candidates_structured",
                  isinstance(_sm40.get("candidates"), list) and bool(_sm40["candidates"])
                  and _sm40["candidates"][0].get("sohieu_key") == "99-2029-QH17"
                  and {"candidate_type", "confidence", "linked_to_query", "strong"}.issubset(set(_sm40["candidates"][0].keys()))
                  and _sm40.get("candidate_count") == len(_sm40["candidates"])))

    # ═══ v1.33.30 (MERGE bundle-29 — nhánh song song CÙNG log v1.33.28: giữ ta [doctor helper, BrokenPipe,
    # tl_fetch version-compare, .gitattributes], port họ [candidates STRUCTURED, compound-sohieu tầng PARSER
    # có guard VBHN-marker, --refresh flag], +test rc-doctrine của họ) — r41_* ═══
    # (parser tầng sâu) số kép trả VỀ GIÁ TRỊ với tên VBHN; KHÔNG nhận với tên thường (guard marker).
    cases.append(("r41_parse_compound_sohieu_guarded",
                  _parse_sohieu_from_name("VBHN_73-82-ND-CP_Quan_ly_dau_tu_CNTT_NSNN") == "73-82-ND-CP"
                  and _parse_sohieu_from_name("Bao_cao_73-82-ND-CP_tong_ket") == ""   # số kép KHÔNG marker VBHN → guard chặn
                  and _parse_sohieu_from_name("Luat_100-2015-QH13_Hinh_su") == "100-2015-QH13"))
    # (rc-doctrine, test gốc bundle-29 adapt fixture ta): sweep/review-queue --json rc=0 dù có findings.
    _orig_me41 = _TL_MODULE._manifest_entries
    _TL_MODULE._manifest_entries = lambda refresh=False: _fx30
    try:
        _b41s, _b41r = _io27.StringIO(), _io27.StringIO()
        with _ctx27.redirect_stdout(_b41s), _ctx27.redirect_stderr(_io27.StringIO()):
            _rc41s = _TL_MODULE.cmd_sweep(build_parser().parse_args(["sweep", "--json"]))
        with _ctx27.redirect_stdout(_b41r), _ctx27.redirect_stderr(_io27.StringIO()):
            _rc41r = _TL_MODULE.cmd_review_queue(build_parser().parse_args(["review-queue", "--json"]))
    finally:
        _TL_MODULE._manifest_entries = _orig_me41
    cases.append(("r41_sweep_review_queue_rc0_findings", _rc41s == 0 and _rc41r == 0
                  and json.loads(_b41s.getvalue()).get("total") == 3))

    # ═══ v1.33.31 (log rà LIVE v1.33.28 — S-1 hai engine bất đồng 124/125-2025 · S-2 advisory kép
    # OMNIBUS_NARROW 45-2019 · A cookie 19 ngày nạp im lặng) — r42_* ═══
    # (S-1a — CẬP NHẬT v1.33.32 MERGE bundle-12) relation-check phủ định → row RỜI bucket hành động sang bucket
    # RIÊNG `relation_probe_suppressed` (bundle), mang cờ RELATION_CHECK_NEGATED (ta) + payload `relation_probe`
    # (bundle), fix_command nêu PHỦ ĐỊNH, negated_count đếm; counts (có bucket mới) vẫn cộng về tổng.
    # Audit fake qua monkeypatch — hình dạng bất đồng THẬT đã field-verify LIVE (124/125-2025).
    _orig_ra42 = _TL_MODULE._relation_audit
    _TL_MODULE._relation_audit = (lambda entries, base="", subject="", amendments=None,
                                  footnote_amend_keys=None: {"verdict": "OK", "missing_links": []})
    try:
        _rq42 = _TL_MODULE._review_queue_report([_rq17_base_rev, _rq17_amend], limit=None)
    finally:
        _TL_MODULE._relation_audit = _orig_ra42
    _rq42_row = (_rq42["relation_probe_suppressed"] or [{}])[0]
    cases.append(("r42_rel_negated_demoted_and_flagged",
                  _rq42["relation_backfill"] == [] and _rq42["relation_low_confidence"] == []
                  and _rq42["relation_negated_count"] == 1
                  and _rq42["counts"]["relation_probe_suppressed"] == 1
                  and "RELATION_CHECK_NEGATED" in (_rq42_row.get("flags_all") or [])
                  and "RELATION_CHECK_NEGATED" in (_rq42_row.get("flags") or [])
                  and (_rq42_row.get("relation_probe") or {}).get("suppressed") is True
                  and "PHỦ ĐỊNH" in _rq42_row.get("fix_command", "")
                  and sum(_rq42["counts"].values()) == _rq42["laws_scanned"] == 1))
    # (S-1b control) audit THẬT trả subject_only (fixture 06/2022) → KHÔNG negate — _rq17b giữ nguyên bucket
    # rel_low, negated_count=0, payload probe đi kèm với suppressed=False (driver thấy vì sao GIỮ).
    cases.append(("r42_rel_not_negated_when_audit_review",
                  _rq17b["relation_negated_count"] == 0
                  and _rq17b["relation_probe_suppressed"] == []
                  and "RELATION_CHECK_NEGATED" not in (_rq17b["relation_low_confidence"][0].get("flags_all") or [])
                  and (_rq17b["relation_low_confidence"][0].get("relation_probe") or {}).get("suppressed") is False))
    # (S-1c — CẬP NHẬT v1.33.32) ops-plan 3 tầng: P0 CHỈ strong; low-conf còn tín hiệu → P2 read-only probe
    # (bundle); ca phủ định → P3 info audit-trail (ta). Không còn low-conf/negated nào lọt P0.
    _orig_rq42 = _TL_MODULE._review_queue_report
    _TL_MODULE._review_queue_report = lambda entries, limit=None: {
        "counts": {}, "web_round2": [], "relation_backfill": [],
        "relation_low_confidence": [{"sohieu": "68-2025-QH15", "name": "Luat_DT_von_NN",
                                     "flags_all": ["AMENDMENT_CANDIDATE_LOW_CONFIDENCE"]}],
        "relation_probe_suppressed": [{"sohieu": "124-2025-QH15", "name": "Luat_GDNN",
                                       "flags_all": ["RELATION_CHECK_NEGATED", "UNLINKED_AMENDMENT_CANDIDATE"]}],
        "relation_negated_count": 1}
    try:
        _op42 = _TL_MODULE._ops_plan_report([], include_sweep=False)
    finally:
        _TL_MODULE._review_queue_report = _orig_rq42
    _op42_ids = {x["id"]: x for x in _op42["actions"]}
    cases.append(("r42_ops_plan_negated_not_p0",
                  "relation_check_before_backfill" not in _op42_ids
                  and _op42_ids.get("relation_low_confidence_probe", {}).get("priority") == "P2"
                  and _op42_ids["relation_low_confidence_probe"]["count"] == 1
                  and _op42_ids["relation_low_confidence_probe"]["confirm_required"] is False
                  and _op42_ids.get("relation_candidates_negated", {}).get("priority") == "P3"
                  and _op42_ids["relation_candidates_negated"]["count"] == 1
                  and _op42_ids["relation_candidates_negated"]["confirm_required"] is False))
    # (S-2) advisory-split OMNIBUS_NARROW: 45-2019 BLLĐ (sua_doi ≥2 ref, tên hẹp) → omnibus_title_advisory,
    # KHÔNG còn ở headline title_mismatch (hết đếm kép với cờ trên bảng danh sách); TITLE_METADATA giữ headline.
    _g42 = _hygiene_groups([
        {"id": "o1", "drive_id": "o1", "name": "BLuat_45-2019-QH14_Lao_dong", "so_hieu": "45/2019/QH14",
         "loai": "Bộ luật", "cat": "20", "corpus": "true", "sua_doi": "51-2024-QH15;74-2025-QH15"},
        {"id": "o2", "drive_id": "o2", "name": "Luat_123-2025-QH15_SuaDoi_Giao_duc", "so_hieu": "123/2025/QH15",
         "loai": "Luật", "cat": "13", "corpus": "true", "title_vn": "Quản lý thuế xuất khẩu, thuế nhập khẩu"},
    ])
    cases.append(("r42_omnibus_narrow_advisory_split",
                  [_x.get("drive_id") for _x in _g42["omnibus_title_advisory"]] == ["o1"]
                  and [_x.get("drive_id") for _x in _g42["title_mismatch"]] == ["o2"]
                  and "OMNIBUS_NARROW_TITLE_CHECK" in _title_flags(dict(_g42["omnibus_title_advisory"][0]))))
    # (A cookie) ngưỡng cảnh báo tuổi cookie: ≥14 ngày → chuỗi ⚠ chủ động; trẻ/không rõ → rỗng.
    _tg42 = _need_base("tl_gws")
    cases.append(("r42_nlm_cookie_age_note_threshold",
                  bool(_tg42._nlm_cookie_age_note(19.0)) and "19" in _tg42._nlm_cookie_age_note(19.0)
                  and _tg42._nlm_cookie_age_note(3.0) == "" and _tg42._nlm_cookie_age_note(None) == ""
                  and _tg42._NLM_COOKIE_WARN_DAYS == 14))

    # ═══ v1.33.32 (MERGE bundle-12 `tra-luat-skill-v1.33.31-gws3env-fixed.zip` — nhánh song song CÙNG 3 vấn đề
    # trên v1.33.30: PORT tiêu chí actionable + bucket suppressed + payload probe + ops-plan 3 tầng + mirror
    # registry_hygiene; GIỮ ta: phạm vi probe strong+low, cờ NEGATED, P3 audit-trail, cookie superset) — r43_* ═══
    # (a) TIÊU CHÍ PORT: phủ định theo TÍN-HIỆU-HÀNH-ĐỘNG, KHÔNG đòi verdict=OK — corpus chỉ có base (không
    # candidate, KHÔNG VBHN → verdict=QT5_WEB_REQUIRED) vẫn suppressed; có subject_only → GIỮ (không phủ định).
    _p43a = _rq_relation_probe([_rq17_base_rev], _rq17_base_rev)
    _p43b = _rq_relation_probe([_rq17_base_rev, _rq17_amend], _rq17_base_rev)
    cases.append(("r43_probe_criterion_actionable_not_verdict",
                  _p43a["ok"] and _p43a["suppressed"] is True and _p43a["verdict"] == "QT5_WEB_REQUIRED"
                  and _p43b["ok"] and _p43b["suppressed"] is False and _p43b["subject_only_review"] >= 1))
    # (b) mirror registry_hygiene (PORT bundle-12): entry CHỈ có OMNIBUS_NARROW không vào title_mismatch_rows
    # của registry-doctor (cờ vẫn giữ ở title_flags); TITLE_METADATA vẫn vào.
    _rh43 = _need_base("registry_hygiene")
    _rh43_omn = {"so_hieu": "45/2019/QH14", "name": "BLuat_45-2019-QH14_Lao_dong", "drive_id": "rh1",
                 "corpus": "true", "sua_doi": "51-2024-QH15;74-2025-QH15", "loai": "Bộ luật", "cat": "20"}
    _rh43_rep = _rh43.analyze([_rh43_omn])
    cases.append(("r43_registry_hygiene_omnibus_not_title_mismatch",
                  "OMNIBUS_NARROW_TITLE_CHECK" in _rh43.title_flags(_rh43_omn)
                  and _rh43_rep["title_mismatch_rows"] == []))

    # (r43b — phát hiện live 2026-07-05 khi refresh nlm token thật): `nlm login --force` re-auth THÀNH CÔNG
    # (account xác nhận, session mới) nhưng root auth.json.extracted_at KHÔNG được nlm CLI bản mới ghi lại
    # → _nlm_auth_age_days cũ báo ~19 ngày dù VỪA refresh xong. Fix: ưu tiên metadata.json.last_validated (ISO,
    # cập nhật đúng lúc login/--check OK) — fixture "vừa xong" (last_validated=now) phải cho age≈0 dù
    # auth.json.extracted_at cũ 19 ngày; thiếu metadata.json → fallback extracted_at (bundle cũ, tương thích ngược).
    import datetime as _dt43
    import time as _t43
    _now_iso43 = _dt43.datetime.now().isoformat()
    _old_epoch43 = _t43.time() - 19 * 86400
    _fresh_meta = {"auth.json": json.dumps({"extracted_at": _old_epoch43}),
                   "profiles/default/metadata.json": json.dumps({"last_validated": _now_iso43})}
    _legacy_only = {"auth.json": json.dumps({"extracted_at": _old_epoch43})}
    _age_fresh43 = _tg42._nlm_auth_age_days(_fresh_meta)
    _age_legacy43 = _tg42._nlm_auth_age_days(_legacy_only)
    cases.append(("r43_nlm_auth_age_prefers_metadata_last_validated",
                  _age_fresh43 is not None and _age_fresh43 < 0.01
                  and _age_legacy43 is not None and 18.9 < _age_legacy43 < 19.1))

    # ═══ v1.33.34 (MERGE bundle-13 `tra-luat-v1.33.33.zip` — nhánh song song thêm cờ --out cho reg-query +
    # corpus-audit [S-4]; DISJOINT với cookie-fix v1.33.33 ta → PORT trọn, 0 reject) — r44_* ═══
    # (S-4) reg-query + corpus-audit CHẤP NHẬN --out (trước TỪ CHỐI → unrecognized arguments, rc=2 dù mọi lệnh
    # JSON nặng khác đã có). Behavior-lock: parser nhận --out; và --out tự bật JSON (cmd_* gate _is_json |= a.out).
    _bp44 = build_parser()
    def _parse_out(_argv):
        try:
            _ns = _bp44.parse_args(_argv)
        except SystemExit:
            return None
        return getattr(_ns, "out", "__MISSING__")
    _rq44 = _parse_out(["reg-query", "--out", "/tmp/_rq_selftest.json"])
    _ca44 = _parse_out(["corpus-audit", "--all", "--out", "/tmp/_ca_selftest.json"])
    cases.append(("r44_reg_query_accepts_out", _rq44 == "/tmp/_rq_selftest.json"))
    cases.append(("r44_corpus_audit_accepts_out", _ca44 == "/tmp/_ca_selftest.json"))

    # ═══ v1.33.35 (log rà 45 Luật LIVE — M1 NLM auth false-green · M2 slot-audit −288 giả · Q1 QT5 lai dấu) — r45_* ═══
    build_parser()   # đảm bảo tl_gws đã bind (_imp khả dụng) trước khi gọi _nlm_auth_alive
    # (M1) canary LIVE phân loại đúng: ok:True→alive True · auth_hint→False (RED) · lỗi-non-auth→None (không đỏ
    # oan) · thiếu binary→None. Monkeypatch nlm_cli.notebook_get/nlm_available (KHÔNG chạm mạng thật).
    _tg45 = _need_base("tl_gws"); _nc45 = _need_base("nlm_cli")
    _o_ng45, _o_av45 = _nc45.notebook_get, _nc45.nlm_available
    try:
        _nc45.nlm_available = lambda: True
        _nc45.notebook_get = lambda nb, timeout=120: {"ok": True, "source_count": 298}
        _m1_ok = _tg45._nlm_auth_alive("NB45")
        _nc45.notebook_get = lambda nb, timeout=120: {"ok": False, "error": "Authentication expired", "auth_hint": "nlm login"}
        _m1_exp = _tg45._nlm_auth_alive("NB45")
        _nc45.notebook_get = lambda nb, timeout=120: {"ok": False, "error": "notebook not found", "auth_hint": None}
        _m1_inc = _tg45._nlm_auth_alive("NB45")
        _nc45.nlm_available = lambda: False
        _m1_nob = _tg45._nlm_auth_alive("NB45")
    finally:
        _nc45.notebook_get, _nc45.nlm_available = _o_ng45, _o_av45
    cases.append(("r45_nlm_auth_alive_classifies",
                  _m1_ok[0] is True and _m1_exp[0] is False and _m1_inc[0] is None and _m1_nob[0] is None
                  and "EXPIRED" in _m1_exp[1]))
    # (M2) slot-audit: notebook_get ok:False (auth chết, KHÔNG raise) → phys KHÔNG bị coi là 0 → KHÔNG suy gap
    # (trước: int(None or 0)=0 → gap −288 giả); live_read_failed=True, không có physical_source_count.
    _o_ng46 = _nc45.notebook_get; _o_me46 = _TL_MODULE._manifest_entries
    _nc45.notebook_get = lambda nb, timeout=120: {"ok": False, "error": "Authentication expired", "auth_hint": "nlm login"}
    _TL_MODULE._manifest_entries = lambda refresh=False: [
        {"drive_id": "d1", "nlm_source_id": "s1", "nlm_notebook_id": "NB46", "corpus": "true"}]
    try:
        _b46 = _io27.StringIO()
        with _ctx27.redirect_stdout(_b46), _ctx27.redirect_stderr(_io27.StringIO()):
            _TL_MODULE.cmd_slot_audit(build_parser().parse_args(
                ["slot-audit", "--notebook-id", "NB46", "--json"]))
        _out46 = json.loads(_b46.getvalue())
    finally:
        _nc45.notebook_get = _o_ng46; _TL_MODULE._manifest_entries = _o_me46
    cases.append(("r46_slot_audit_authfail_no_fake_gap",
                  "gap" not in _out46 and "physical_source_count" not in _out46
                  and _out46.get("live_read_failed") is True))
    # (Q1) QT5: subject KHÔNG dấu → KHÔNG trộn keyword có dấu (query nhất quán không-dấu); subject CÓ dấu → giữ
    # có dấu. Thuần offline.
    _q_nd = _qt5_queries("Bo luat hinh su")
    _q_d = _qt5_queries("Bộ luật hình sự")
    cases.append(("r47_qt5_consistent_diacritics",
                  not any("hợp nhất" in q or "mới nhất" in q for q in _q_nd)
                  and any("hop nhat" in q for q in _q_nd)
                  and any("hợp nhất" in q for q in _q_d)))
    # ═══ v1.33.37 (MERGE bundle-14 — BOM/zero-width lọt title_vn ca QD_671) — r48_* ═══
    # sentence-case strip BOM ở đầu (hết 'Quyết định ﻿bộ…'); title_vn header có BOM → BOILERPLATE/rỗng (không
    # ghi rác); header sạch vẫn bóc đúng (BỘ LUẬT trước LUẬT). BOM = "﻿".
    _bom = "﻿"
    _tv48_bom = _TL_MODULE._title_vn_from_header("QUYẾT ĐỊNH\n" + _bom + "BỘ THÔNG TIN VÀ\n\nĐiều 1.", {})
    _tv48_ok = _TL_MODULE._title_vn_from_header("BỘ LUẬT\nHÌNH SỰ\n\nĐiều 1.", {})
    cases.append(("r48_title_vn_strips_bom_zero_width",
                  not _TL_MODULE._title_sentence_case(_bom + "BỘ THÔNG TIN VÀ").startswith(_bom)
                  and _tv48_bom[0] == "" and _tv48_ok[0] == "Bộ luật Hình sự"))

    # ═══ v1.33.38 (log Cowork: STAGE cookie TƯƠI mà vẫn 'Authentication expired' — auth.json root STALE vì nlm
    # CLI mới chỉ ghi profiles/default; Cowork đọc auth.json stale) — r49_* ═══
    # _nlm_sync_authjson_from_profile: profile TƯƠI hơn → dựng lại auth.json từ profile (cookies+csrf+session_id,
    # extracted_at=now); auth.json mới hơn → None (KHÔNG hạ cấp); thiếu profile → None.
    import tempfile as _tmp49
    _tg49 = _need_base("tl_gws")
    with _tmp49.TemporaryDirectory() as _d49:
        _prof = _os38.path.join(_d49, "profiles", "default"); _os38.makedirs(_prof)
        _aj49 = _os38.path.join(_d49, "auth.json")
        _ck49 = _os38.path.join(_prof, "cookies.json"); _md49 = _os38.path.join(_prof, "metadata.json")
        open(_aj49, "w", encoding="utf-8").write(json.dumps(
            {"cookies": [{"name": "OTZ", "expires": 100}], "csrf_token": "old", "session_id": "olds", "extracted_at": 1}))
        open(_ck49, "w", encoding="utf-8").write(json.dumps(
            [{"name": "__Secure-1PSID", "expires": 9999999999, "value": "v", "domain": ".google.com"}]))
        open(_md49, "w", encoding="utf-8").write(json.dumps(
            {"csrf_token": "newcsrf", "session_id": "newsess", "build_label": "b"}))
        _os38.utime(_aj49, (1000, 1000)); _os38.utime(_ck49, (2000, 2000)); _os38.utime(_md49, (2000, 2000))
        _sj49 = json.loads(_tg49._nlm_sync_authjson_from_profile(_d49) or "{}")
        _fresh_ok = (len(_sj49.get("cookies", [])) == 1 and _sj49["cookies"][0]["name"] == "__Secure-1PSID"
                     and _sj49.get("csrf_token") == "newcsrf" and _sj49.get("session_id") == "newsess"
                     and _sj49.get("extracted_at", 0) > 1)
        _os38.utime(_aj49, (3000, 3000))                       # auth.json mới hơn profile → None
        _none_older = (_tg49._nlm_sync_authjson_from_profile(_d49) is None)
        _os38.remove(_ck49)                                     # thiếu profile → None
        _none_noprof = (_tg49._nlm_sync_authjson_from_profile(_d49) is None)
    cases.append(("r49_nlm_authjson_synced_from_fresh_profile",
                  _fresh_ok and _none_older and _none_noprof))

    # ═══ v1.33.39 (log Cowork: stage cookie 'mới' [extracted_at tiến] mà NLM từ chối MỌI endpoint — cookie hết
    # hạn NHANH, chết cả local; stage cookie chết = Cowork kẹt vòng lặp) — r50_* ═══
    # cmd_nlm_auth_stage VERIFY LIVE (canary notebook_get, KHÔNG tin nlm login --check) TRƯỚC stage:
    # dead+không-force → rc=4 TỪ CHỐI (KHÔNG upload); dead+--force → bỏ qua cổng, upload chạy; alive → stage.
    _tg50 = _need_base("tl_gws")
    _o_files50, _o_alive50, _o_up50 = _tg50._nlm_auth_files, _tg50._nlm_auth_alive, _tg50._stage_enc_upload
    _o_tok50 = _os38.environ.get("TL_TOKEN")
    _uploaded50 = []
    _os38.environ["TL_TOKEN"] = _o_tok50 or "selftest-token"
    try:
        _tg50._nlm_auth_files = lambda: {"auth.json": "{}"}
        _tg50._stage_enc_upload = lambda name, blob, folder, fid, force, g=None: (_uploaded50.append(fid) or (fid, True))
        _mkns50 = lambda force: argparse.Namespace(config=None, profile=None, refresh=False, folder=None,
                                                   cred_file_id="F50", new=False, force=force)
        _tg50._nlm_auth_alive = lambda nb, timeout=30: (False, "AUTH_EXPIRED (test)")
        with _hush():
            _rc50_dead = _tg50.cmd_nlm_auth_stage(_mkns50(False))
        _refused = (_rc50_dead == 4 and _uploaded50 == [])
        with _hush():
            _rc50_force = _tg50.cmd_nlm_auth_stage(_mkns50(True))
        _forced = (_rc50_force == 0 and _uploaded50 == ["F50"])
        _uploaded50.clear()
        _tg50._nlm_auth_alive = lambda nb, timeout=30: (True, "LIVE OK (test)")
        with _hush():
            _rc50_alive = _tg50.cmd_nlm_auth_stage(_mkns50(False))
        _allowed = (_rc50_alive == 0 and _uploaded50 == ["F50"])
    finally:
        _tg50._nlm_auth_files, _tg50._nlm_auth_alive, _tg50._stage_enc_upload = _o_files50, _o_alive50, _o_up50
        if _o_tok50 is None:
            _os38.environ.pop("TL_TOKEN", None)
        else:
            _os38.environ["TL_TOKEN"] = _o_tok50
    cases.append(("r50_nlm_stage_refuses_dead_cookie", _refused and _forced and _allowed))

    # ═══ v1.33.40 (MERGE bundle-15 'complete': source-delete (a) KHÔNG trash Drive dù docstring nói, (b) reg_delete
    # SAI shape g.get(fileId,force) — GAS đòi POST+drive_ids[]+confirm=yes) — r51_* ═══
    _sd_calls = []
    class _FakeGSD:
        def get(self, action, **kw): _sd_calls.append(("get", action, kw)); return {"ok": True, "trashed": True, "name": "T"}
        def post(self, action, **kw): _sd_calls.append(("post", action, kw)); return {"ok": True, "removed": 1}
    _sd_keys = ("apply_profile_offline", "_manifest_entries", "_apply_gate", "load_creds", "_gas",
                "_apply_journal_start", "_journal_append", "_resolve_nlm_notebook", "_invalidate_manifest_cache")
    _sd_saved = {k: getattr(_TL_MODULE, k) for k in _sd_keys}
    try:
        _sd_ent = {"drive_id": "d51", "name": "Test_Doc", "so_hieu": "", "cat": "20", "corpus": "true"}
        _TL_MODULE.apply_profile_offline = lambda *a, **k: None
        _TL_MODULE._manifest_entries = lambda refresh=False: [_sd_ent]
        _TL_MODULE._apply_gate = lambda a: (True, None)
        _TL_MODULE.load_creds = lambda *a, **k: None
        _TL_MODULE._gas = lambda: _FakeGSD()
        _TL_MODULE._apply_journal_start = lambda *a, **k: "run51"
        _TL_MODULE._journal_append = lambda *a, **k: None
        _TL_MODULE._resolve_nlm_notebook = lambda x: (None, "skip")
        _TL_MODULE._invalidate_manifest_cache = lambda: None
        with _hush():
            _sd_rc = _TL_MODULE.cmd_source_delete(argparse.Namespace(
                config=None, profile=None, refresh=False, target="d51", apply=True, confirm="yes"))
    finally:
        for _k, _v in _sd_saved.items():
            setattr(_TL_MODULE, _k, _v)
    _sd_trash = any(c[0] == "get" and c[1] == "trash" and c[2].get("fileId") == "d51"
                    and c[2].get("confirm") == "yes" for c in _sd_calls)
    _sd_reg = any(c[0] == "post" and c[1] == "reg_delete" and json.loads(c[2].get("drive_ids", "[]")) == ["d51"]
                  and c[2].get("confirm") == "yes" and c[2].get("require_removed") == "no" for c in _sd_calls)
    _sd_no_legacy = not any(c[0] == "get" and c[1] == "reg_delete" for c in _sd_calls)   # hết g.get(reg_delete,force)
    cases.append(("r51_source_delete_trashes_drive_and_posts_reg_delete",
                  _sd_rc == 0 and _sd_trash and _sd_reg and _sd_no_legacy))

    # ═══ v1.33.41 (log rà VBHN-first 4 văn bản: N1 double-add sau timeout · N2 ingest-analyze sai cho VBHN ·
    # N3 register bỏ field im lặng · N4 corpus=false không clear ref · N5 nlm-list cắt câm) — r52_* ═══
    # (N2a/b) VBHN: match sohieu đầu tiên là số GỐC (layout VPQH in số VBHN ở khối ký cuối) → sohieu rỗng thay vì
    # số gốc; có số VBHN trong probe → bắt đúng; loai=VBHN dù header in 'BỘ LUẬT'; draft=False (marker 'lấy ý
    # kiến' trong THÂN không còn bắn); luật thường + dự thảo thật không đổi.
    _hdr52 = ("VĂN PHÒNG QUỐC HỘI\nBỘ LUẬT\nHÌNH SỰ\n\nBộ luật Hình sự số 100/2015/QH13 của Quốc hội, "
              "được hợp nhất bởi văn bản hợp nhất...\n" + "Điều X. Việc lấy ý kiến nhân dân..." * 40)
    _c52a = _classify_doc_header(_hdr52, "vbhn-blhs.docx")
    _c52b = _classify_doc_header(_hdr52 + "\n\nXÁC THỰC VĂN BẢN HỢP NHẤT\nSố: 135/VBHN-VPQH", "vbhn-blhs.docx")
    _c52c = _classify_doc_header("QUỐC HỘI\nLUẬT\nDÂN SỐ\nLuật số: 113/2025/QH15", "luat113.docx")
    _c52d = _classify_doc_header("DỰ THẢO\nLUẬT ABC\n...", "duthao.docx")
    cases.append(("r52_vbhn_header_classify",
                  _c52a["sohieu"] == "" and _c52a["loai"] == "Văn bản hợp nhất" and _c52a["draft"] is False
                  and "135" in _c52b["sohieu"] and "VBHN" in _c52b["sohieu"].upper()
                  and _c52c["sohieu"] == "113/2025/QH15" and _c52c["draft"] is False
                  and _c52d["draft"] is True))
    # (N2c) chủ đề đặt tên KHÔNG dính dòng cơ quan 'VĂN PHÒNG QUỐC HỘI'.
    _s52 = _doc_subject_for_name("VĂN PHÒNG QUỐC HỘI\nBỘ LUẬT\nHÌNH SỰ\n", {"title": ""})
    cases.append(("r52_subject_skips_van_phong", "phong" not in _strip_accents(_s52).lower()))
    # (N3) _verified_reg_upsert READ-BACK field-level: webapp ok nhưng cột bị bỏ im lặng (read-back lệch) →
    # verified=False + fields_dropped; read-back khớp → verified=True (ca 62/2025 goc/title_vn=null).
    class _FkG52:
        def __init__(self, row):
            self.row = row
        def get(self, action, **kw):
            if action == "reg_upsert":
                return {"ok": True, "updated": True}
            if action == "reg_get":
                return {"ok": True, "rows": [self.row]}
            raise AssertionError(action)
    _v52a = _verified_reg_upsert(_FkG52({"goc": "", "title_vn": ""}),
                                 {"drive_id": "d62", "goc": "62-2025-QH15", "title_vn": "Luật X"})
    _v52b = _verified_reg_upsert(_FkG52({"goc": "62-2025-QH15", "title_vn": "Luật X"}),
                                 {"drive_id": "d62", "goc": "62-2025-QH15", "title_vn": "Luật X"})
    cases.append(("r52_reg_upsert_readback_catches_dropped_fields",
                  _v52a["verified"] is False and _v52a.get("error") == "FIELDS_DROPPED_ON_WRITE"
                  and {d["col"] for d in _v52a["fields_dropped"]} == {"goc", "title_vn"}
                  and _v52b["verified"] is True))
    # (N1) _nlm_post_add_dup_check: 2 nguồn cùng drive_id → payload 🔴 kèm fix; 1 nguồn → None; list fail → None.
    class _FkNC52:
        def __init__(self, srcs, ok=True):
            self.srcs, self.okv = srcs, ok
        def source_list(self, nb, skip_freshness=True, drive=True):
            return {"ok": self.okv, "sources": self.srcs}
    _dX52 = "D52" + "x" * 25   # drive_id thật ≥20 ký tự (_nlm_source_drive_id lọc id ngắn)
    _dup52 = _nlm_post_add_dup_check(_FkNC52([{"id": "s1", "drive_id": _dX52}, {"id": "s2", "drive_id": _dX52}]),
                                     "NB", _dX52, "s2")
    _one52 = _nlm_post_add_dup_check(_FkNC52([{"id": "s1", "drive_id": _dX52}]), "NB", _dX52, "s1")
    _fail52 = _nlm_post_add_dup_check(_FkNC52([], ok=False), "NB", _dX52, "s1")
    cases.append(("r52_post_add_dup_check",
                  _dup52 is not None and _dup52["dup_after_add"] and "s1" in _dup52["fix"]
                  and _one52 is None and _fail52 is None))
    # (N4) source-update-corpus false: NLM delete OK → reg_clear nlm_source_id,nlm_notebook_id; register --apply
    # (N3) + nlm-list --max/--out (N5) parser nhận.
    _n4_calls = []
    class _FkG54:
        def get(self, action, **kw):
            _n4_calls.append((action, kw))
            if action == "reg_upsert":
                return {"ok": True, "updated": True}
            if action == "reg_get":
                return {"ok": True, "rows": [{"corpus": "false", "nlm_status": "removed_by_user"}]}
            if action == "reg_clear":
                return {"ok": True, "cleared": 1}
            raise AssertionError(action)
    _n4_ent = {"drive_id": "d54", "name": "Luat_54", "so_hieu": "54/2020/QH14", "cat": "20",
               "corpus": "true", "nlm_source_id": "sid54", "nlm_notebook_id": "NB54", "nlm_status": "pushed"}
    _n4_keys = ("apply_profile_offline", "_manifest_entries", "_apply_gate", "load_creds", "_gas",
                "_apply_journal_start", "_journal_append", "_resolve_nlm_notebook", "_invalidate_manifest_cache")
    _n4_saved = {k: getattr(_TL_MODULE, k) for k in _n4_keys}
    _nc54 = _need_base("nlm_cli")
    _o_sd54, _o_av54 = _nc54.source_delete, _nc54.nlm_available
    try:
        _TL_MODULE.apply_profile_offline = lambda *a, **k: None
        _TL_MODULE._manifest_entries = lambda refresh=False: [_n4_ent]
        _TL_MODULE._apply_gate = lambda a, write_cols=None: (True, None)
        _TL_MODULE.load_creds = lambda *a, **k: None
        _TL_MODULE._gas = lambda: _FkG54()
        _TL_MODULE._apply_journal_start = lambda *a, **k: "run54"
        _TL_MODULE._journal_append = lambda *a, **k: None
        _TL_MODULE._resolve_nlm_notebook = lambda x: ("NB54", None)
        _TL_MODULE._invalidate_manifest_cache = lambda: None
        _nc54.nlm_available = lambda: True
        _nc54.source_delete = lambda sid, timeout=120: {"ok": True}
        with _hush():
            _n4_rc = _TL_MODULE.cmd_source_update_corpus(argparse.Namespace(
                config=None, profile=None, refresh=False, target="d54", status="false",
                apply=True, confirm="yes"))
    finally:
        for _k, _v in _n4_saved.items():
            setattr(_TL_MODULE, _k, _v)
        _nc54.source_delete, _nc54.nlm_available = _o_sd54, _o_av54
    _n4_clear = [c for c in _n4_calls if c[0] == "reg_clear"]
    cases.append(("r52_corpus_false_clears_nlm_refs",
                  _n4_rc == 0 and len(_n4_clear) == 1
                  and "nlm_source_id" in str(_n4_clear[0][1].get("cols"))
                  and "nlm_notebook_id" in str(_n4_clear[0][1].get("cols"))))
    _bp52 = build_parser()
    try:
        _ns52a = _bp52.parse_args(["register", "--drive-id", "X" * 30, "--goc", "1-2020-QH14", "--apply"])
        _ns52b = _bp52.parse_args(["nlm-list", "--max", "0", "--out", "/tmp/_nl.json"])
        _p52_ok = (_ns52a.apply is True and _ns52b.max == 0 and _ns52b.out == "/tmp/_nl.json")
    except SystemExit:
        _p52_ok = False
    cases.append(("r52_register_apply_nlm_list_flags", _p52_ok))

    # ═══ v1.33.42 (MERGE bundle-16 + N6 determinism) — r53_* ═══
    # (bundle-16 ROOT CAUSE) reg-query projection THIẾU title_vn/goc → field ghi ĐÚNG mà đọc lại =None → chẩn
    # đoán sai 'register không persist'. Nay phơi title_vn/goc + sua_doi/hieuluc (cùng lớp gap).
    _r53row = _reg_query_row({"drive_id": "x53", "name": "Luat_X", "title_vn": "Luật X", "goc": "1-2020-QH14",
                              "sua_doi": "2-2021-QH15", "hieuluc": "Còn hiệu lực"})
    cases.append(("r53_reg_query_row_exposes_relation_fields",
                  _r53row.get("title_vn") == "Luật X" and _r53row.get("goc") == "1-2020-QH14"
                  and _r53row.get("sua_doi") == "2-2021-QH15" and _r53row.get("hieuluc") == "Còn hiệu lực"))
    # (N6) _ingest_local_prev_state đọc journal run trước: match theo meta.file; nhặt fileId/gdoc/source_id từ
    # commit ok; run MỚI NHẤT thắng; file khác → {}. + parser ingest-local nhận --resume.
    import tempfile as _tmp53
    with _tmp53.TemporaryDirectory() as _d53:
        _o_env53 = _os38.environ.get("TL_JOURNAL_DIR")
        _os38.environ["TL_JOURNAL_DIR"] = _d53
        try:
            _j53 = _os38.path.join(_d53, "ingest-local_100_1.jsonl")
            with open(_j53, "w", encoding="utf-8") as _fh53:
                _fh53.write(json.dumps({"t": "run_start", "cmd": "ingest-local", "run_id": "ingest-local_100_1",
                                        "file": "C:/in/f53.docx", "name": "Luat_53"}) + "\n")
                _fh53.write(json.dumps({"t": "commit", "op": "upload", "key": "Luat_53.docx", "ok": True,
                                        "verify": {"fileId": "FID53"}}) + "\n")
                _fh53.write(json.dumps({"t": "commit", "op": "organize", "key": "FID53", "ok": True,
                                        "verify": {"gdoc": "GD53", "srcId": "SRC53"}}) + "\n")
                _fh53.write(json.dumps({"t": "commit", "op": "nlm_source_add", "key": "GD53", "ok": False,
                                        "verify": {"source_id": None}}) + "\n")   # add FAIL → không nhặt
            _st53 = _TL_MODULE._ingest_local_prev_state("C:/in/f53.docx", "Luat_53")
            _st53_miss = _TL_MODULE._ingest_local_prev_state("C:/in/khac.docx", "Luat_khac")
        finally:
            if _o_env53 is None:
                _os38.environ.pop("TL_JOURNAL_DIR", None)
            else:
                _os38.environ["TL_JOURNAL_DIR"] = _o_env53
    try:
        _ns53 = build_parser().parse_args(["ingest-local", "f.docx", "--apply", "--resume"])
        _p53_ok = (_ns53.resume is True and _ns53.apply is True)
    except SystemExit:
        _p53_ok = False
    cases.append(("r53_ingest_local_prev_state_and_resume_flag",
                  _st53.get("upload_fid") == "FID53" and _st53.get("gdoc") == "GD53"
                  and _st53.get("src_docx") == "SRC53" and "nlm_source_id" not in _st53
                  and _st53.get("journal_prev") == "ingest-local_100_1"
                  and _st53_miss == {} and _p53_ok))

    # ═══ v1.33.43 (MERGE bundle-17 — A2 backfill-title-vn KẸT pagination: ép offset=0 ở --apply + next_offset=
    # None ⇒ lô đầu TOÀN skip lặp vĩnh viễn, pool 79 mà 0/79 quét được) — r54_* ═══
    # --apply nay HONOR --offset; trang toàn-skip → next_offset TIẾN QUA skip; trang cuối → None+coverage_complete.
    _r54_keys = ("apply_profile_offline", "_manifest_entries", "_backfill_titlevn_candidates", "_apply_gate",
                 "load_creds", "_gas", "_apply_journal_start", "_journal_append", "_invalidate_manifest_cache")
    _r54_saved = {k: getattr(_TL_MODULE, k) for k in _r54_keys}
    class _FkG54b:
        def get(self, action, **kw): return {"ok": True}
        def post(self, action, **kw): return {"ok": True, "patched": 0}
    def _r54_run(off, lim):
        _ns = argparse.Namespace(config=None, profile=None, refresh=False, force_refresh=False,
                                 offset=off, limit=lim, from_tukhoa=True, apply=True, out=None)
        _b = _io27.StringIO()
        with _ctx27.redirect_stdout(_b), _ctx27.redirect_stderr(_io27.StringIO()):
            _rc = _TL_MODULE.cmd_backfill_titlevn(_ns)
        return _rc, json.loads(_b.getvalue())
    try:
        _TL_MODULE.apply_profile_offline = lambda *a, **k: None
        _TL_MODULE._manifest_entries = lambda refresh=False: []
        _TL_MODULE._backfill_titlevn_candidates = lambda entries, force=False: [
            {"entry": {"tukhoa": ""}, "drive_id": f"d54{i}", "name": f"ND_{i}-2020-ND-CP_X"} for i in range(5)]
        _TL_MODULE._apply_gate = lambda a, write_cols=None: (True, None)
        _TL_MODULE.load_creds = lambda *a, **k: None
        _TL_MODULE._gas = lambda: _FkG54b()
        _TL_MODULE._apply_journal_start = lambda *a, **k: "run54b"
        _TL_MODULE._journal_append = lambda *a, **k: None
        _TL_MODULE._invalidate_manifest_cache = lambda: None
        _rc54a, _s54a = _r54_run(0, 2)     # trang đầu: 2 skip / pool 5 → next=2
        _rc54b, _s54b = _r54_run(2, 10)    # trang cuối: 3 skip, hết pool → next=None
    finally:
        for _k, _v in _r54_saved.items():
            setattr(_TL_MODULE, _k, _v)
    cases.append(("r54_backfill_titlevn_offset_advances_past_skips",
                  _rc54a == 0 and _s54a.get("next_offset") == 2 and _s54a.get("coverage_complete") is False
                  and _rc54b == 0 and _s54b.get("next_offset") is None and _s54b.get("coverage_complete") is True))

    # ═══ v1.33.44 (log Cowork 7A — vá lô vấn đề vận hành skill S4-S14) — r55_* ═══
    # S4/S5/S6 — ingest-local ghi registry SẠCH ngay tại ingest: shape-lock nguồn (normalize loai + nhãn cat đủ +
    # corpus=true ở bước link cuối) + helper thật chạy offline đúng ('VBHN'→enum, '03'→nhãn đủ).
    import inspect as _ins55
    _src55 = _ins55.getsource(_TL_MODULE.cmd_ingest_local)
    cases.append(("r55_ingest_local_canonical_loai_cat_corpus",
                  "loai = _normalize_loai(loai)" in _src55
                  and "_cat_reg_label(cat)" in _src55
                  and '"corpus": "true"' in _src55
                  and _normalize_loai("VBHN") == "Văn bản hợp nhất"
                  and _cat_reg_label("03") == "03_Buu_chinh_vien_thong"))
    # S7 — journal --close: PURE plan chỉ heal op có set ĐÃ KHỚP registry (so mềm strip+lower); mismatch/không-set → blocked.
    _cp55 = _journal_close_plan(
        [{"t": "run_start", "run_id": "r55", "cmd": "ingest-local"},
         {"t": "intent", "op": "reg_bulk", "key": "g1",
          "set": {"nlm_source_id": "s1", "nlm_status": "pushed", "corpus": "true"}},
         {"t": "intent", "op": "reg_bulk", "key": "g2", "set": {"nlm_source_id": "s2"}},
         {"t": "intent", "op": "upload", "key": "f3"}],
        {"g1": {"nlm_source_id": "s1", "nlm_status": " PUSHED", "corpus": "true"},
         "g2": {"nlm_source_id": ""}})
    cases.append(("r55_journal_close_plan_heals_matched_only",
                  _cp55["counts"] == {"inflight": 3, "healable": 1, "blocked": 2}
                  and _cp55["healable"][0]["key"] == "g1"
                  and {b["key"]: b["reason"] for b in _cp55["blocked"]}
                  == {"g2": "VALUES_NOT_MATCHED", "f3": "NO_SET_TO_VERIFY"}))
    # S8 — nlm-add nhận alias --drive (=--drive-id) + --wait no-op (drift doc↔CLI hết gãy usage-error).
    _n55 = build_parser().parse_args(["nlm-add", "--drive", "D55", "--wait"])
    cases.append(("r55_nlm_add_flag_aliases", _n55.drive_id == "D55" and _n55.wait is True and _n55.no_wait is False))
    # S11/S12 — sweep: headline name_nonstandard = VBQPPL thật (trừ loai='thuong' + quarantine → _other);
    # next_action gợi corpus-audit trang NHỎ Cowork-safe (--limit 15).
    _sw55 = _sweep_report([
        {"drive_id": "b1", "name": "luat-dau-thau-2023.html", "corpus": "true", "row_kind": "own"},
        {"drive_id": "b2", "name": "bao-cao-giao-ban-q3.html", "corpus": "true", "row_kind": "own", "loai": "thuong"},
        {"drive_id": "b3", "name": "van-ban-cach-ly-cu.html", "corpus": "true", "row_kind": "own",
         "cat": "_ZZZ_QUARANTINE_taluat"},
    ])
    cases.append(("r55_sweep_name_nonstandard_corpus_scope",
                  _sw55.get("name_nonstandard") == 1
                  and _sw55["name_nonstandard_rows"][0]["drive_id"] == "b1"
                  and _sw55.get("name_nonstandard_other") == 2
                  and any("--limit 15" in x for x in _sw55["next_actions"])))
    # S14 — source-rename gợi ý: chủ đề từ title_vn (bỏ từ-loại đầu) + số hiệu GẠCH-NỐI đủ (hết 'TT_28_2023_TT-BYT' cụt);
    # thiếu sohieu → cảnh báo SOHIEU_MISSING_IN_SUGGESTION.
    _pl55 = _source_rename_plan(
        [{"drive_id": "x55", "name": "thong-tu-28-2023-tt-byt-benh-nghe-nghiep.html", "sohieu": "28/2023/TT-BYT",
          "title_vn": "Thông tư Hướng dẫn chẩn đoán bệnh nghề nghiệp do yếu tố vi sinh", "corpus": "true"}], "x55")
    _pl55b = _source_rename_plan(
        [{"drive_id": "y55", "name": "van-ban-khong-so-hieu.html", "corpus": "true"}], "y55")
    cases.append(("r55_source_rename_suggest_titlevn_and_hyphen_sohieu",
                  _pl55.get("ok") is True
                  and _pl55["new_name"].startswith("TT_28-2023-TT-BYT_")
                  and "Huong_dan" in _pl55["new_name"]
                  and "28_2023" not in _pl55["new_name"]
                  and any(w.startswith("SOHIEU_MISSING_IN_SUGGESTION") for w in _pl55b.get("warnings") or [])))

    # ═══ v1.33.47 (MERGE bundle-45 + đối chiếu fix v1.33.46 nhánh song song) — r56_* ═══
    # (a) bare-VBHN matcher 1 CHIỀU — ca thật 'VBHN 88 Quảng cáo ĐÃ CÓ mà lần nào chạy cũng báo thiếu':
    # web/footnote ghi '88/VBHN-VPQH' (không năm), corpus lưu '88-2025-VBHN-VPQH' → exact/substring miss.
    cases.append(("r56_vbhn_bare_key",
                  _vbhn_bare_key("88-2025-VBHN-VPQH") == "88-VBHN-VPQH"
                  and _vbhn_bare_key("88/VBHN-VPQH") == "88-VBHN-VPQH"
                  and _vbhn_bare_key("113-2025-QH15") == ""))
    cases.append(("r56_sohieu_query_hits_entry_one_way",
                  _sohieu_query_hits_entry("88-VBHN-VPQH", "88-2025-VBHN-VPQH") is True      # bare → year-qualified: NỚI
                  and _sohieu_query_hits_entry("50-2025-VBHN-VPQH", "50-2026-VBHN-VPQH") is False  # có năm: giữ CHẶT (collision)
                  and _sohieu_query_hits_entry("88-2025-VBHN-VPQH", "88-VBHN-VPQH") is False       # chiều ngược: KHÔNG nới
                  and _sohieu_query_hits_entry("113-2025", "113-2025-QH15", substring=True) is True
                  and _sohieu_query_hits_entry("", "gi-cung-duoc") is True))
    # site-level: source-map direct + locate-match dùng matcher mới (query bare hit entry year-qualified)
    _e56 = {"drive_id": "v56", "name": "VBHN_88-2025-VBHN-VPQH_Quang_cao", "sohieu": "88/2025/VBHN-VPQH", "corpus": "true"}
    _sm56 = _source_map_one("88/VBHN-VPQH", [_e56])
    cases.append(("r56_source_map_direct_bare_vbhn",
                  any(x.get("drive_id") == "v56" for x in (_sm56.get("direct_hits") or []))))
    # (b) QT-5 hints ưu tiên title_vn CÓ DẤU + guard tên-file (bundle thiếu guard — P0-1 v1.31.0)
    _h56 = _qt5_search_hints("", [{"name": "Luat_46-2024-QH15_Cong_chung", "title_vn": "Luật Công chứng"}])
    _h56b = _qt5_search_hints("", [{"name": "Luat_46-2024-QH15_Cong_chung",
                                    "title_vn": "Luat_46-2024-QH15_Cong_chung"}])   # title_vn = tên file → guard, fallback tail
    cases.append(("r56_qt5_hints_titlevn_first_with_filename_guard",
                  any("Luật Công chứng" in h for h in _h56)
                  and not any("Luat_46-2024-QH15" in h for h in _h56b)
                  and any("cong chung" in h for h in _h56b)))
    # (c) _nlm_auth_alive retry ×3: transient lần đầu → True khi lần 2 OK; auth_hint BỀN → False (GIỮ M1 —
    # bundle xếp clientauthentication vào transient-final → cookie chết thật thành INCONCLUSIVE = false-green);
    # transient bền → None (không đỏ oan). Patch time.sleep (module chia sẻ) để khỏi chờ backoff thật.
    _tg56 = _imp("tl_gws")
    import time as _tm56
    _sleep56, _imp56 = _tm56.sleep, _tg56.__dict__.get("_imp")
    class _FkNC56:
        def __init__(self, seq): self.seq, self.i = seq, 0
        def nlm_available(self): return True
        def notebook_get(self, nb, timeout=30):
            r = self.seq[min(self.i, len(self.seq) - 1)]; self.i += 1; return r
    try:
        _tm56.sleep = lambda s: None
        def _mk56(seq):
            _fk = _FkNC56(seq)
            _tg56._imp = lambda name: _fk if name == "nlm_cli" else _imp56(name)
            return _tg56._nlm_auth_alive("nb56")
        _a56 = _mk56([{"ok": False, "error": "network_error: could not reach host"}, {"ok": True, "source_count": 5}])
        _b56 = _mk56([{"ok": False, "error": "ClientAuthenticationError: expired", "auth_hint": True}] * 3)
        _c56 = _mk56([{"ok": False, "error": "network_error: connection reset"}] * 3)
    finally:
        _tm56.sleep = _sleep56
        if _imp56 is not None:
            _tg56._imp = _imp56
    cases.append(("r56_nlm_auth_alive_retry_transient_vs_expired",
                  _a56[0] is True and _b56[0] is False and "AUTH_EXPIRED" in _b56[1]
                  and _c56[0] is None and "INCONCLUSIVE" in _c56[1]))

    # ═══ v1.33.48 (rà Instruction Project 'Luật BHXH' — profile tên CÓ DẤU + KHOẢNG TRẮNG) — r57_* ═══
    # (a) _profile_lookup chịu-lỗi-gõ: exact > khớp không-dấu/hoa-thường/space-_- DUY NHẤT; ≥2 ứng viên mờ → không đoán.
    _p57 = {"vbqppl": {"a": 1}, "Luật BHXH": {"notebookId": "NB-BHXH"}, "Luật BHYT": {"notebookId": "NB-BHYT"}}
    cases.append(("r57_profile_lookup_tolerant",
                  _profile_lookup(_p57, "Luật BHXH")[0] == "Luật BHXH"
                  and _profile_lookup(_p57, "luat_bhxh")[0] == "Luật BHXH"
                  and _profile_lookup(_p57, "LUAT-BHXH")[1] is not None
                  and _profile_lookup(_p57, "Luat XYZ")[1] is None
                  and _profile_lookup({"Luat BHXH": {}, "Luật BHXH": {}}, "luat bhxh")[1] is None))  # 2 ứng viên mờ → không đoán
    # (b) _apply_profile_env: tên KHÔNG có trong config → scope RỖNG + profile_found=False (KHÔNG rơi âm thầm
    # về nền vbqppl — trước đây TL_REGISTRY_DOC_ID/TL_NOTEBOOK_ID bị điền từ base → ghi/push nhầm corpus nền).
    _cfg57 = {"schema": 2, "defaultProfile": "vbqppl",
              "profiles": {"vbqppl": {"notebookId": "NB-BASE", "registryDocId": "REG-BASE"},
                           "Luật BHXH": {"notebookId": "NB-BHXH", "registryDocId": "REG-BHXH",
                                         "categories": "own", "manifestScope": "own"}}}
    _envk57 = ("TL_PROFILE", "TL_NOTEBOOK_ID", "TL_REGISTRY_DOC_ID", "TL_MANIFEST_ID", "TL_ROOT_FOLDER_ID",
               "TL_META_FOLDER_ID", "TL_OVERFLOW_NOTEBOOK_ID", "TL_CATEGORIES_MODE", "TL_MANIFEST_SCOPE", "TL_BASE_ALSO")
    _sav57 = {k: _hos.environ.get(k) for k in _envk57}
    try:
        with _hush():   # PROFILE_NOT_FOUND in stderr là PASS-by-design
            _r57a = _apply_profile_env(_cfg57, "Luật BHXH")
            _ok57a = (_hos.environ.get("TL_NOTEBOOK_ID") == "NB-BHXH"
                      and _hos.environ.get("TL_CATEGORIES_MODE") == "own" and _r57a["profile_found"])
            _r57b = _apply_profile_env(_cfg57, "luat bhxh")     # gõ không dấu → vẫn đúng scope + TL_PROFILE canonical
            _ok57b = (_hos.environ.get("TL_PROFILE") == "Luật BHXH"
                      and _hos.environ.get("TL_NOTEBOOK_ID") == "NB-BHXH" and _r57b["profile_found"])
            _r57c = _apply_profile_env(_cfg57, "Luat XYZ")      # sai hẳn → scope RỖNG, không lấy nền
            _ok57c = (_hos.environ.get("TL_NOTEBOOK_ID") is None
                      and _hos.environ.get("TL_REGISTRY_DOC_ID") is None and not _r57c["profile_found"])
    finally:
        for _k, _v in _sav57.items():
            if _v is None:
                _hos.environ.pop(_k, None)
            else:
                _hos.environ[_k] = _v
    cases.append(("r57_profile_env_no_silent_base_fallback", _ok57a and _ok57b and _ok57c))
    # (c) --profile/--config nhận Ở CẢ SAU subcommand (Instruction dặn 'mọi lệnh truyền --profile' — trước gãy
    # rc=2); SUPPRESS giữ giá trị đặt TRƯỚC subcommand không bị default đè (bẫy namespace-con copy-đè Python mới).
    _ap57 = build_parser()
    cases.append(("r57_profile_flag_after_subcommand",
                  _ap57.parse_args(["reg-query", "--profile", "Luật BHXH", "--json"]).profile == "Luật BHXH"
                  and _ap57.parse_args(["--profile", "Luật BHXH", "reg-query", "--json"]).profile == "Luật BHXH"
                  and _ap57.parse_args(["reg-query", "--json"]).profile is None
                  and _ap57.parse_args(["--profile", "A", "reg-query", "--profile", "B"]).profile == "B"
                  and _ap57.parse_args(["counts", "--config", "/tmp/c57.json"]).config == "/tmp/c57.json"))
    # (d) slot per-notebook (Instruction manifest_fallback: 'chỉ đếm rows có nlm_notebook_id == notebook đích').
    _es57 = [{"nlm_source_id": "s1", "nlm_notebook_id": "NB-A", "nlm_status": "pushed"},
             {"nlm_source_id": "s2", "nlm_notebook_id": "NB-A", "nlm_status": "removed_from_drive"},
             {"nlm_source_id": "s3", "nlm_notebook_id": "NB-B", "nlm_status": "pushed"},
             {"nlm_source_id": "s4", "nlm_status": "pushed"},
             {"name": "khong-nlm"}]
    cases.append(("r57_registry_claim_per_notebook",
                  _registry_claim_by_notebook(_es57) == {"NB-A": 2, "(trống)": 1, "NB-B": 1}
                  and _registry_claim_target(_es57, "NB-A") == 1      # removed KHÔNG đếm ('không đếm mọi nlm_status')
                  and _registry_claim_target(_es57, "NB-B") == 1
                  and _registry_claim_target(_es57, "") is None))
    # ═══ v1.33.49 (log rà 34 Luật corpus — status amendment false-negative + hieuluc gap) — r58_* ═══
    _m58_saved = _TL_MODULE._manifest_entries
    try:
        _TL_MODULE._manifest_entries = lambda refresh=False: [
            {"drive_id": "d57", "name": "Luat_57-2024-QH15_SuaDoi_QuyHoach_DauTu_PPP_DauThau",
             "so_hieu": "57/2024/QH15", "corpus": "true", "nlm_source_id": "s57", "nlm_status": "pushed"}]
        _g58 = _status_amendment_registry_guard(argparse.Namespace(
            amendment=True, sohieu="57-2024-QH15", refresh=False, strict=False, json=True))
    finally:
        _TL_MODULE._manifest_entries = _m58_saved
    cases.append(("r58_status_amendment_registry_guard",
                  _g58 is not None and _g58[0]["decision"] == "SKIP"
                  and _g58[0]["surface"] == "AMENDMENT_ALREADY_IN_CORPUS_ON_NLM"))
    _hl58, _why58 = _hieuluc_from_header_text(
        "Tình trạng hiệu lực: Còn hiệu lực\nĐiều 99. Hiệu lực thi hành. Luật này có hiệu lực từ ngày 01 tháng 7 năm 2026.",
        today="2026-07-07")
    _hl58b, _ = _hieuluc_from_header_text(
        "Điều 1. Luật này có hiệu lực từ ngày 01 tháng 01 năm 2027.", today="2026-07-07", infer_from_date=True)
    cases.append(("r58_hieuluc_header_parser",
                  _hl58 == "Còn hiệu lực; hiệu lực từ 01/07/2026" and _why58 == ""
                  and _hl58b == "Chưa có hiệu lực; hiệu lực từ 01/01/2027"))
    _bf58 = _backfill_hieuluc_candidates([
        {"drive_id": "a", "name": "Luat_A", "corpus": "true", "row_kind": "own", "hieuluc": ""},
        {"drive_id": "b", "name": "Luat_B", "corpus": "true", "row_kind": "own", "hieuluc": "Còn hiệu lực"},
        {"drive_id": "c", "name": "Luat_C", "corpus": "false", "row_kind": "own", "hieuluc": ""},
    ])
    _ap58 = build_parser()
    cases.append(("r58_backfill_hieuluc_candidates_and_parser",
                  [x["drive_id"] for x in _bf58] == ["a"]
                  and _ap58.parse_args(["backfill-hieuluc", "--limit", "5", "--offset", "3",
                                        "--infer-from-date"]).infer_from_date is True))
    # (v1.33.49) LỚP 2 fix #2 — preingest_gate.decide đối chiếu registry_hit khi webapp NOT_FOUND (phủ CẢ
    # đường không --amendment / gọi trực tiếp): hit corpus=true → SKIP IN_REGISTRY_LOCAL; hit thô → REVIEW.
    _pg58 = _need_base("preingest_gate")
    _pg58a = _pg58.decide({"status": "NOT_FOUND",
                           "registry_hit": {"name": "Luat_57", "corpus": True, "on_nlm": True, "drive_id": "d"}})
    _pg58b = _pg58.decide({"status": "", "registry_hit": {"name": "raw", "corpus": False, "on_nlm": False, "drive_id": "e"}})
    _pg58c = _pg58.decide({"status": "NOT_FOUND"})
    _pg58h = _pg58.registry_hit_summary(
        "57-2024-QH15",
        [{"sohieu": "57/2024/QH15", "name": "raw_57", "corpus": "false", "drive_id": "a"},
         {"sohieu": "57-2024-QH15", "name": "Luat_57_canon", "corpus": "true", "nlm_source_id": "s", "drive_id": "b"}],
        lambda q, e: _sohieu_query_hits_entry(norm_sohieu(q), _sohieu_key_entry(e)))
    cases.append(("r58_preingest_registry_hit_layer",
                  _pg58a["decision"] == "SKIP" and _pg58a["surface"] == "IN_REGISTRY_LOCAL"
                  and _pg58b["decision"] == "REVIEW" and _pg58b["surface"] == "IN_REGISTRY_LOCAL_RAW"
                  and _pg58c["decision"] == "ADD"
                  and _pg58h is not None and _pg58h["corpus"] and _pg58h["name"] == "Luat_57_canon"
                  and "IN_REGISTRY_LOCAL" in _pg58._alias_vocab(_pg58a)["flags"]))
    # (v1.33.49) drive-push route auto|gws|gcloud (PURE) — auto ưu tiên gws, chết → gcloud LOUD; ép thì chặt.
    _dr58 = _imp("tl_gws")._drive_push_route
    cases.append(("r58_drive_push_route",
                  _dr58("auto", True, False)[0] == "gws"
                  and _dr58("auto", False, True)[0] == "gcloud" and "FALLBACK" in _dr58("auto", False, True)[1]
                  and _dr58("auto", False, False)[0] == ""
                  and _dr58("gws", False, True)[0] == "" and _dr58("gcloud", True, False)[0] == ""
                  and _dr58("gcloud", False, True)[0] == "gcloud"
                  and _ap58.parse_args(["drive-push", "x.zip", "--via", "gcloud"]).via == "gcloud"))

    # ═══ v1.33.54 (MERGE bundle determinism-hardening 50-53) — r59_*: khoá PURE helpers determinism trong
    # gate --selftest (bundle thêm ~3300 dòng nhưng 0 test ở đây; determinism-audit/workflow-audit là lệnh
    # RIÊNG không chạy tự động lúc đóng gói — upload script chỉ chạy --selftest) ═══
    # (a) zip member normalize: zip-slip (..) → rỗng=unsafe; ./ + backslash chuẩn hoá; dir-entry rỗng.
    cases.append(("r59_zip_normalized_member_path",
                  _zip_normalized_member_path("a/../b.txt") == ""
                  and _zip_normalized_member_path("./x/./y.txt") == "x/y.txt"
                  and _zip_normalized_member_path("a\\b\\c.txt") == "a/b/c.txt"
                  and _zip_normalized_member_path("d/") == ""
                  and _zip_normalized_member_path("") == ""))
    # (b) zip member order tất định (độc lập thứ tự entry gốc) — dựng zip in-memory đảo thứ tự.
    import io as _io59, zipfile as _zf59
    _buf59 = _io59.BytesIO()
    with _zf59.ZipFile(_buf59, "w") as _z59:
        for _n in ("b.txt", "B/a.txt", "a.txt"):
            _z59.writestr(_n, "x")
    with _zf59.ZipFile(_buf59) as _z59:
        _order59 = [i.filename for i in _zip_sorted_infos(_z59)]
    cases.append(("r59_zip_sorted_infos_stable", _order59 == ["a.txt", "b.txt", "B/a.txt"]))   # '.'(2E)<'/'(2F)
    # (c) _json_dumps deterministic: sort_keys + scrub volatile ("<volatile>"), default (det=False) GIỮ NGUYÊN.
    _o59 = {"zeta": 1, "alpha": 2, "generatedAt": "2026-07-08T00:00:00Z", "seconds": 1.23}
    _det59 = _json_dumps(_o59, deterministic=True)
    _raw59 = _json_dumps(_o59, deterministic=False)
    cases.append(("r59_json_dumps_det_scrub",
                  _det59.index('"alpha"') < _det59.index('"zeta"')
                  and '"<volatile>"' in _det59 and "2026-07-08" not in _det59
                  and "2026-07-08T00:00:00Z" in _raw59))
    # (d) route-task nhận CẢ positional lẫn --task (fix merge v1.33.54 — drift doc↔CLI lớp S8/A1).
    _ap59 = build_parser()
    _ns59a = _ap59.parse_args(["route-task", "ingest_local", "--json"])
    _ns59b = _ap59.parse_args(["route-task", "--task", "ingest_local", "--json"])
    cases.append(("r59_route_task_positional_and_flag",
                  getattr(_ns59a, "task_pos", None) == "ingest_local"
                  and getattr(_ns59b, "task", None) == "ingest_local"))
    # (e) release-manifest exclude: config THẬT/.enc/CLAUDE.md/.claude KHÔNG vào manifest (rò metadata +
    # file_count lệch zip-set → release-verify trong gói fail); example + file gói THẬT thì vào.
    import tempfile as _tf59
    with _tf59.TemporaryDirectory() as _d59:
        _r59 = Path(_d59)
        (_r59 / "scripts").mkdir(); (_r59 / ".claude").mkdir()
        for _rel, _keep in (("SKILL.md", True), ("scripts/tl.py", True), ("tra_luat_config.example.json", True),
                            ("tra_luat_config.v2.json", False), ("CLAUDE.md", False),
                            ("scripts/tl_secrets.enc", False), (".claude/settings.json", False)):
            _fp = _r59 / _rel
            _fp.write_text("x", encoding="utf-8")
            if _release_should_include(_fp, _r59) is not _keep:
                cases.append((f"r59_release_exclude[{_rel}]", False))
                break
        else:
            cases.append(("r59_release_exclude_dev_local_files", True))
    # ═══ v1.33.55 (MERGE Pha B core-json-determinism) — r60_*: PARITY wrapper tl.py ↔ tl_core (refactor
    # không được đổi hành vi) + GIỮ fix #4 trong tl_core.jsonio (bundle fork từ 1.33.53 mang bug cũ trở lại) ═══
    import tl_core.deterministic as _td60
    import tl_core.jsonio as _tj60
    _o60 = {"zeta": 1, "alpha": {"generatedAt": "x", "path": "C:\tmp\abc" if _hos.name == "nt" else "/tmp/abc"},
            "seconds": 9, "note": "giữ nguyên"}
    cases.append(("r60_wrapper_parity_tl_core",
                  _json_dumps(_o60, deterministic=True) == _td60.json_dumps(_o60, deterministic=True, project_root=HERE.parent)
                  and _json_dumps(_o60, deterministic=False) == _td60.json_dumps(_o60, deterministic=False, project_root=HERE.parent)
                  and _scrub_volatile(_o60) == _td60.scrub_volatile(_o60, project_root=HERE.parent)
                  and _VOLATILE_JSON_KEYS is _td60.VOLATILE_JSON_KEYS))
    # fix #4 sống trong tl_core.jsonio: schema lạ (không groups/route_task) → in JSON, KHÔNG render route-task.
    import io as _io60, contextlib as _cl60
    _buf60 = _io60.StringIO()
    with _cl60.redirect_stdout(_buf60):
        _tj60.print_json_or_text({"ok": True, "schema": "release_manifest.v1", "file_count": 3}, False)
    _txt60 = _buf60.getvalue()
    cases.append(("r60_jsonio_unknown_schema_json_fallback",
                  '"file_count": 3' in _txt60 and "route-task ok=" not in _txt60))
    # deterministic_enabled 3 tầng: flag > default_on > env (env đọc ĐỘNG).
    _sav60 = _hos.environ.pop("TL_DETERMINISTIC", None)
    try:
        _ok60 = (not _td60.deterministic_enabled(None, default_on=False)
                 and _td60.deterministic_enabled(None, default_on=True)
                 and _td60.deterministic_enabled(argparse.Namespace(deterministic=True), default_on=False))
        _hos.environ["TL_DETERMINISTIC"] = "1"
        _ok60 = _ok60 and _td60.deterministic_enabled(None, default_on=False)
    finally:
        if _sav60 is None:
            _hos.environ.pop("TL_DETERMINISTIC", None)
        else:
            _hos.environ["TL_DETERMINISTIC"] = _sav60
    cases.append(("r60_deterministic_enabled_precedence", _ok60))
    # ═══ v1.33.56 (Pha C) — r61_*: khoá facade tl ↔ tl_core.{workflow,release,live} ═══
    # (a) bind copy-globals: hàm dùng chung trong module LÀ hàm tl (identity — không snapshot lệch);
    #     tham chiếu CHÉO đi qua STUB tl (release._golden_test là stub tl, không phải def của workflow).
    import tl_core.workflow as _w61, tl_core.release as _r61, tl_core.live as _l61
    cases.append(("r61_bind_identity_and_cross_stub",
                  _w61._json_dumps is _json_dumps
                  and _l61._build_release_manifest is _build_release_manifest      # stub tl trong live
                  and _r61._golden_test is _golden_test                            # stub tl trong release
                  and _w61._golden_test is not _golden_test                        # def THẬT ở workflow
                  and _TASK_TO_WORKFLOW is _w61._TASK_TO_WORKFLOW                  # const alias
                  and _IDEMPOTENCY_CONTRACTS is _w61._IDEMPOTENCY_CONTRACTS))
    # (b) facade dispatch: lệnh moved chạy qua stub tl (in-process, offline, _hush nuốt stdout).
    with _hush():
        _rc61a = cmd_tool_inventory(argparse.Namespace(json=True, deterministic=True))
        _rc61b = cmd_route_task(argparse.Namespace(task="ingest_local", task_pos=None, json=True, deterministic=True))
    cases.append(("r61_facade_dispatch_smoke", _rc61a == 0 and _rc61b == 0))
    # (c) module KHÔNG đọc bare mutable-global của tl (chống snapshot-stale khi main() gán lại).
    import io as _io61
    _mut61 = []
    import tl_core.zip_ingest as _z61, tl_core.ocr as _o61x, tl_core.chunking as _c61
    for _mod61 in (_w61, _r61, _l61, _z61, _o61x, _c61):
        _src61 = _io61.open(_mod61.__file__, encoding="utf-8").read()
        if "_DETERMINISTIC_ON" in _src61 or "_CRED_AUTH_DEAD" in _src61:
            _mut61.append(_mod61.__name__)
    cases.append(("r61_no_bare_mutable_globals_in_tl_core", not _mut61))
    # ═══ v1.33.56 — r62: ROOT-CAUSE flake determinism-audit (age_days nhảy bucket 0.001-ngày giữa 2
    # snapshot con → live-state-diff báo unexpected ~5%/lần). Khoá: diff bỏ key volatile ở LEAF. ═══
    import tempfile as _tf62, json as _json62
    with _tf62.TemporaryDirectory() as _d62:
        _b62 = Path(_d62) / "b.json"; _a62 = Path(_d62) / "a.json"
        _snap = lambda age, extra=None: {"auth": {"gws_credentials": {"present": True, "age_days": age}},
                                         "volatile": {"generatedAt": "x"}, **({} if extra is None else extra)}
        _b62.write_text(_json62.dumps(_snap(4.793)), encoding="utf-8")
        _a62.write_text(_json62.dumps(_snap(4.794)), encoding="utf-8")
        _dd62 = _tl_live._live_state_diff(str(_b62), str(_a62))
        _a62.write_text(_json62.dumps(_snap(4.794, {"registry": {"rows": 746}})), encoding="utf-8")
        _b62.write_text(_json62.dumps(_snap(4.793, {"registry": {"rows": 745}})), encoding="utf-8")
        _dd62b = _tl_live._live_state_diff(str(_b62), str(_a62))
    _strip62 = _tl_live._strip_snapshot_volatile({"volatile": {"x": 1}, "auth": {"age_days": 1.2, "present": True}, "seconds": 9})
    cases.append(("r62_live_diff_ignores_volatile_leaf",
                  _dd62["ok"] and _dd62["summary"]["changed"] == 0
                  and (not _dd62b["ok"]) and _dd62b["unexpected_changes"][0]["path"] == "registry.rows"
                  and _strip62 == {"auth": {"present": True}}))
    # ═══ v1.33.56 — r63_*: khoá lô vá review 5-phân-hệ (PH2/P4/F-series) ═══
    import tempfile as _tf63, zipfile as _zf63, json as _json63
    # (a) PH2-03: tên member cấm trên Windows → unsafe ngay tại plan.
    cases.append(("r63_zip_member_windows_forbidden",
                  not _zip_is_safe_member("bao cao?.txt") and not _zip_is_safe_member("a<b>.docx")
                  and not _zip_is_safe_member("xy.txt") and _zip_is_safe_member("thu-muc/van_ban.docx")))
    # (b) PH2-02: extract tôn trọng max_size_mb như plan.
    with _tf63.TemporaryDirectory() as _d63:
        _zp63 = Path(_d63) / "t.zip"
        with _zf63.ZipFile(_zp63, "w") as _z:
            _z.writestr("big.txt", "x" * (2 * 1024 * 1024))
            _z.writestr("small.txt", "ok")
        _got63 = _safe_extract_zip_for_ingest(str(_zp63), str(Path(_d63) / "out"), max_size_mb=1)
        cases.append(("r63_zip_extract_respects_size_cap",
                      [x["normalized_path"] for x in _got63] == ["small.txt"]))
    # (c) PH2-08: 'Điều N.' đầu dòng nhưng là THAM CHIẾU wrap dòng (dòng trước chưa kết câu) → KHÔNG phải heading.
    _tx63 = "\n".join(["Điều 1. Phạm vi", "Nội dung theo quy định tại",
                       "Điều 5. của Luật Xây dựng thì áp dụng.", "",
                       "Điều 2. Đối tượng", "nội dung 2", ""])
    _strat63, _recs63 = _chunk_records_from_text(_tx63, name="t", max_chars=10_000)
    cases.append(("r63_dieu_heading_not_wrapped_reference",
                  _strat63 == "by_article" and len(_recs63) == 1
                  and _recs63[0]["start_dieu"] == 1 and _recs63[0]["end_dieu"] == 2))
    # (d) PH2-06: OCR manifest là JSON hợp lệ nhưng KHÔNG phải object → lỗi sạch, không AttributeError.
    with _tf63.TemporaryDirectory() as _d63b:
        _tf = Path(_d63b) / "a.ocr.txt"; _tf.write_text("x", encoding="utf-8")
        _mp63 = _ocr_manifest_path_for_text(_tf); _mp63.write_text('"tampered"', encoding="utf-8")
        _man63, _warn63 = _load_ocr_manifest_for_text(_tf)
        cases.append(("r63_ocr_manifest_nondict_clean_error",
                      _man63 is None and any("NOT_A_JSON_OBJECT" in w for w in _warn63)))
    # (e) PH2-07 end-to-end: đường dẫn nguồn chứa '---' → chunk-apply + chunk-verify vẫn khớp hash.
    with _tf63.TemporaryDirectory() as _d63c:
        _srcdir = Path(_d63c) / "ho-so---2026"; _srcdir.mkdir()
        _sf63 = _srcdir / "vb.txt"
        _sf63.write_text("\n".join(["Điều 1. Một", "nội dung một", "", "Điều 2. Hai", "nội dung hai", ""]),
                         encoding="utf-8")
        with _hush():
            _rc63a = cmd_chunk_apply(argparse.Namespace(file=str(_sf63), mode="profile", name="vb",
                                                        max_chars=40, out_dir=None, expected_hash=None,
                                                        json=True, deterministic=False))
            _rc63b = cmd_chunk_verify(argparse.Namespace(manifest=str(_srcdir / "vb_chunks" / "chunk_manifest.json"),
                                                         json=True, deterministic=False))
        cases.append(("r63_chunk_roundtrip_path_with_dashes", _rc63a == 0 and _rc63b == 0))
    # (f) P4-03: --config/--profile root-position sống với subparser TỰ khai (doctor) — SUPPRESS hết đè None.
    _ap63 = build_parser()
    _ns63 = _ap63.parse_args(["--config", "/tmp/c63.json", "--profile", "P63", "doctor"])
    cases.append(("r63_selfdeclared_flags_keep_root_position",
                  getattr(_ns63, "config", None) == "/tmp/c63.json" and getattr(_ns63, "profile", None) == "P63"))
    # (g) P4-05: parser cha gọi trần (hygiene) → namespace không fn (guard main trả help+rc2, hết traceback).
    _ns63b = _ap63.parse_args(["hygiene"])
    cases.append(("r63_bare_parent_no_fn_attr", getattr(_ns63b, "fn", None) is None))
    # ═══ v1.33.58 (Pha E) — r64_*: command registry ↔ parser ↔ cards ↔ contracts ═══
    import tl_core.command_registry as _reg64
    _ap64 = build_parser()
    _rv64 = _reg64.validate_registry(_ap64, _TL_MODULE, load_card=_load_workflow_card,
                                     contracts=_IDEMPOTENCY_CONTRACTS)
    cases.append(("r64_registry_validate_clean", bool(_rv64.get("ok")) and _rv64.get("issues") == []))
    # parser SINH từ spec parse y hệt hành vi cũ (positional + flags + required)
    _ok64 = (_ap64.parse_args(["route-task", "ingest_local", "--json"]).task_pos == "ingest_local"
             and _ap64.parse_args(["tool-inventory", "--group", "inventory_decision", "--json"]).group == "inventory_decision"
             and _ap64.parse_args(["release-verify", "M.json", "--strict"]).manifest == "M.json"
             and _ap64.parse_args(["golden-test", "--write"]).write is True
             and _ap64.parse_args(["determinism-audit", "--strict", "--full"]).full is True)
    try:
        with _hush():
            _ap64.parse_args(["release-bundle"])   # thiếu --out (required) → SystemExit(2)
        _ok64 = False
    except SystemExit as _e64:
        _ok64 = _ok64 and _e64.code == 2
    cases.append(("r64_generated_parsers_behavior", _ok64))
    # meta invariants: mọi spec sinh đều có meta generated=True; counts nhất quán; summary schema chuẩn.
    _sum64 = _reg64.registry_summary()
    cases.append(("r64_registry_meta_invariants",
                  all(_reg64.COMMAND_META.get(sp["name"], {}).get("generated") for sp in _reg64.GENERATED_SPECS)
                  and _sum64["counts"]["generated_parsers"] == len(_reg64.GENERATED_SPECS)
                  and _sum64["schema"] == "command_registry.v1"
                  and _sum64["counts"]["total"] == len(_reg64.COMMAND_META)
                  and all(m["risk"] in ("low", "medium", "high") for m in _reg64.COMMAND_META.values())))
    # ═══ v1.33.59 (Pha G) — r65_*: siết-6 contract + bundle-export/guard + golden {FIXTURES}/raw-stability ═══
    import tl_core.command_registry as _reg65
    import tl_core.workflow as _w65
    _six65 = _reg65._CONTRACT_REQUIRED
    # v1.34.1: HẾT grandfather — _CONTRACT_REQUIRED = TRỌN 12 lệnh ghi high-risk (Pha G 6 + siết-6).
    cases.append(("r65_contract_required_six_wired",
                  _six65 == {"nlm-add", "recat", "source-rename", "source-delete", "reg-delete", "dedup-plan",
                             "register", "drive-push", "nlm-reconcile", "push-overflow",
                             "shared-source-fix", "source-update-corpus"}
                  and all(_reg65.COMMAND_META[n]["idempotency_contract"] in _w65._IDEMPOTENCY_CONTRACTS for n in _six65)))
    # drift-lock: KHÔNG còn lệnh ghi high-risk nào thiếu contract (lệnh MỚI quên contract → set ≠ rỗng → fail)
    _adv65 = {n for n, m in _reg65.COMMAND_META.items()
              if m["risk"] == "high" and not m["read_only"] and not m["idempotency_contract"] and n not in _six65}
    cases.append(("r65_grandfather_advisory_exact_set", _adv65 == set()))
    # siết-6 (v1.34.1): 6 contract mới đúng key meta ↔ _IDEMPOTENCY_CONTRACTS và ĐỦ 8 field chuẩn v1
    _new68 = {"register": "register", "push-overflow": "push_overflow", "nlm-reconcile": "nlm_reconcile",
              "drive-push": "drive_push", "shared-source-fix": "shared_source_fix",
              "source-update-corpus": "source_update_corpus"}
    _fields68 = {"schema", "idempotency_key", "journal_key", "resume_behavior", "duplicate_guard",
                 "readback_command", "resume_command", "rollback_hint"}
    cases.append(("r68_contract_siet6_wired_and_complete",
                  all(_reg65.COMMAND_META[c]["idempotency_contract"] == k
                      and set(_w65._IDEMPOTENCY_CONTRACTS.get(k, {})) == _fields68
                      and _w65._IDEMPOTENCY_CONTRACTS[k]["schema"] == "idempotency_contract.v1"
                      for c, k in _new68.items())))
    # v1.34.1: shared-source-fix / source-update-corpus meta requires_confirm khớp code (--apply --confirm yes)
    cases.append(("r68_confirm_meta_matches_code",
                  _reg65.COMMAND_META["shared-source-fix"]["requires_confirm"] is True
                  and _reg65.COMMAND_META["source-update-corpus"]["requires_confirm"] is True))
    # ═══ v1.34.2 — r69_*: vá 4 phát hiện Pha H live-smoke ═══
    # (a) reg-query --drive-id tồn tại trong parser (contract readback hết drift doc↔CLI)
    _ns69 = build_parser().parse_args(["reg-query", "--drive-id", "x123"])
    cases.append(("r69_reg_query_drive_id_flag", getattr(_ns69, "drive_id", None) == "x123"))
    # (b) nlm-add có nhánh reg_link sau add (drift-lock: gỡ nhánh này là fail — đúng ca S14 nguồn 'unregistered')
    import inspect as _ins69
    _src69 = _ins69.getsource(cmd_nlm_add)
    cases.append(("r69_nlm_add_reg_link_wired",
                  "_journaled_reg_write" in _src69 and "nlm-add-link" in _src69 and "row xương" in _src69))
    # (c) live-smoke-plan bước snapshot_diff mang ĐỦ allow-prefix path THẬT (thiếu → diff báo unexpected oan);
    #     quét source tl_core.live (bước khai inline trong hàm plan) — gỡ prefix là fail.
    import tl_core.live as _lv69
    _src_lv69 = _ins69.getsource(_lv69)
    cases.append(("r69_smoke_diff_allow_prefixes",
                  "live_contract_report.nlm.notebook_get.source_count" in _src_lv69
                  and "live_contract_report.contract_checks" in _src_lv69))
    # (d) contract text khớp parser thật: source_delete resume có --apply; reg_delete resume dùng --drive-ids
    import tl_core.workflow as _w69
    cases.append(("r69_contract_resume_matches_parser",
                  "--apply --confirm yes" in _w69._IDEMPOTENCY_CONTRACTS["source_delete"]["resume_command"]
                  and "--drive-ids" in _w69._IDEMPOTENCY_CONTRACTS["reg_delete"]["resume_command"]))
    # bundle-export + guard (ADR-0001)
    import tempfile as _tf65, zipfile as _zf65
    with _tf65.TemporaryDirectory() as _d65:
        _out65 = Path(_d65) / "b.zip"
        with _hush():
            _rc65 = cmd_bundle_export(argparse.Namespace(root=None, out=str(_out65), note="r65", json=True))
        with _zf65.ZipFile(_out65) as _z65:
            _names65 = _z65.namelist()
            _meta65 = json.loads(_z65.read([n for n in _names65 if n.endswith("BUNDLE_META.json")][0]).decode("utf-8"))
        (Path(_d65) / "BUNDLE_META.json").write_text("{}", encoding="utf-8")
        _blocks65 = _imp("tl_gws")._bundle_meta_blocks_push(Path(_d65))
        _noblock65 = _imp("tl_gws")._bundle_meta_blocks_push(HERE.parent)
    cases.append(("r65_bundle_export_meta_and_guard",
                  _rc65 == 0 and _meta65.get("version_forked") == VERSION
                  and _meta65.get("schema") == "bundle_meta.v1"
                  and _blocks65 is True and _noblock65 is False
                  and build_parser().parse_args(["drive-push", "x.zip", "--force"]).force is True))
    # golden plumbing: {FIXTURES} substitution + fixtures tồn tại
    _w65._golden_ensure_fixtures()
    _case65 = {"args": ["chunk-plan", "{FIXTURES}/sample_profile.txt", "--json"]}
    _sub65 = _w65._golden_args(_case65)
    cases.append(("r65_golden_fixtures_substitution",
                  "{FIXTURES}" not in _sub65[1] and Path(_sub65[1]).exists()
                  and (_w65._golden_fixdir() / "slip.zip").exists() and (_w65._golden_fixdir() / "dup.zip").exists()))
    # ═══ v1.33.61 — r66_*: CI run #1/#2 bắt 2 lớp bug máy-phụ-thuộc → khoá vĩnh viễn ═══
    # (a) idempotency_key ĐỘC LẬP container: cùng nội dung, STORED vs DEFLATED → CÙNG key.
    import tempfile as _tf66, zipfile as _zf66
    import tl_core.zip_ingest as _zi66
    with _tf66.TemporaryDirectory() as _d66:
        _za, _zb = Path(_d66) / "a.zip", Path(_d66) / "b.zip"
        for _pz, _comp in ((_za, _zf66.ZIP_STORED), (_zb, _zf66.ZIP_DEFLATED)):
            with _zf66.ZipFile(_pz, "w", compression=_comp) as _z:
                _z.writestr("van_ban.docx", "noi dung giong het nhau")
        _ka = _zi66._zip_plan(str(_za), mode="vbqppl", cat="01")["idempotency_key"]
        _kb = _zi66._zip_plan(str(_zb), mode="vbqppl", cat="01")["idempotency_key"]
    cases.append(("r66_idempotency_key_container_independent", bool(_ka) and _ka == _kb))
    # (b) writer atomic ghi LF trên MỌI OS (trước: Windows CRLF → manifest/golden hash lệch CI).
    with _tf66.TemporaryDirectory() as _d66b:
        _fp66 = Path(_d66b) / "t.txt"
        _write_text_atomic(_fp66, "dong1" + chr(10) + "dong2" + chr(10))
        _raw66 = _fp66.read_bytes()
    cases.append(("r66_atomic_writer_lf_all_os",
                  chr(13).encode() not in _raw66 and _raw66.count(chr(10).encode()) == 2))
    # ═══ v1.34.0 (Pha F) — r67: kernel chống-phình (size ≤ 48KB + links references tồn tại) ═══
    with _hush():
        _rc67 = cmd_workflow_audit(argparse.Namespace(strict=False, json=True, deterministic=False))
    # gọi lại lấy payload trực tiếp (audit in stdout; kiểm qua _workflow_cards_audit + block kernel tự tính)
    _sk67 = (HERE.parent / "SKILL.md").read_bytes()
    import re as _re67
    _links67 = sorted({m.rstrip(".,;:)]}") for m in _re67.findall(r"references/[A-Za-z0-9_./\-]+", _sk67.decode("utf-8", "replace"))})
    _miss67 = [l for l in _links67 if "*" not in l and not (HERE.parent / l).exists()]
    cases.append(("r67_kernel_size_and_links",
                  _rc67 == 0 and len(_sk67) <= 48 * 1024 and not _miss67 and len(_links67) >= 6))
    ok = sum(1 for _, p in cases if p)
    for n, p in cases:
        print(f"  [{'OK' if p else 'FAIL'}] {n}")
    print(f"== tl selftest {ok}/{len(cases)} ==")
    return 0 if ok == len(cases) else 1
