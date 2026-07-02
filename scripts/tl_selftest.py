#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tl_selftest.py — bộ selftest TÁCH khỏi tl.py để tl.py < ngưỡng mount (giảm bề mặt cắt cụt). Dùng TÊN TRẦN của
tl (norm_sohieu/extract_dieu/resolve_footnote_amendments/…) — nạp qua bind(tl_module) gọi từ tl.selftest().
KHÔNG import tl ở top (tránh circular)."""
from __future__ import annotations
import re  # noqa: F401
import json  # noqa: F401

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
    ]
    _cfp = _corpus_fix_plan(_cfx)
    cases.append(("corpus_fix_plan_ordered_tiered",
                  [s["order"] for s in _cfp["steps"]] == sorted(s["order"] for s in _cfp["steps"])
                  and any(s["id"] == "shared_source_id" and s["tier"] == "human_confirm" for s in _cfp["steps"])
                  and any(s["id"] == "infra_in_corpus" and s["tier"] == "safe_auto" and s["reversible"] for s in _cfp["steps"])))
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
        _rt1 = _gas_get_retry(_gf, "manifest_export", _backoff=0)
        _gr = _GFlaky(9, "MANIFEST_NOT_FOUND")
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
        _dok = _pg.decide({"sohieu":"84-2015-QH13", "name":"Luat An toan ve sinh lao dong", "status":"CONSOLIDATED_INTO_VBHN",
                           "superseded_by":[{"sohieu":"14-2024-VBHN-VPQH", "name":"An toan ve sinh lao dong hop nhat", "on_nlm":True}]})
        cases.append(("status_vbhn_subject_mismatch_guard",
            _dmis["decision"] == "REVIEW" and _dmis.get("surface") == "VBHN_GOC_SUBJECT_MISMATCH"
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
    cases.append(("derive_subject_no_hl_garbage", "hl" not in _derive_subject_from_entries([{"name":"Luat_02-2026-QH16_Thu_do_HL2026-07-01"}]) and _derive_subject_from_entries([{"name":"Luat_115-2023-QH15_Kham_chua_benh"}]) == "kham chua benh"))
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
    cases.append(("source_map_unlinked_amendment_detected", bool(sm_tdk.get("unlinked_amendment_candidates")) and any("PAUSE_AND_ASK_USER" in w for w in sm_tdk.get("warnings", []))))
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
    cases.append(("emit_raw_no_gdoc_rc2", _emit_raw_no_gdoc("x.docx", True) == 2))
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
    ok = sum(1 for _, p in cases if p)
    for n, p in cases:
        print(f"  [{'OK' if p else 'FAIL'}] {n}")
    print(f"== tl selftest {ok}/{len(cases)} ==")
    return 0 if ok == len(cases) else 1
