# -*- coding: utf-8 -*-
"""tl_core.hygiene — I1 (v1.34.3): tách NGUYÊN VĂN cụm hygiene/report/backfill từ scripts/tl.py.

KHÔNG gọi trực tiếp từ ngoài — public CLI vẫn là scripts/tl.py (stub ủy quyền). Module nhận các helper
dùng chung của tl qua `bind(tl_module)`: copy MỌI tên public/private của tl vào globals() TRỪ tên đã có
(def riêng của module thắng; tên thuộc module anh em resolve qua STUB đã định nghĩa trong tl trước bind).
Hành vi được KHÓA byte-level bởi 6 golden hygiene_* (commit characterization TRƯỚC cut) — golden phải
khớp nguyên trạng, không regen.
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
import zipfile    # noqa: F401
from pathlib import Path  # noqa: F401

_TL = None


def bind(tl_module) -> None:
    """I1 (khác bind sibling-module): REBASE __globals__ của TỪNG HÀM đã chuyển về namespace SỐNG của tl —
    hàm chạy đúng trên globals tl lúc gọi (monkeypatch của selftest trên tl ăn NGAY, helper không stale,
    không copy-snapshot). Hàm hygiene gọi lẫn nhau resolve qua STUB trong tl → vòng về module này."""
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



def _vbhn_year_complete(e: dict) -> bool:
    """B4 (v1.33.0): năm đã XÁC ĐỊNH ĐẦY ĐỦ — sohieu-key dạng NN-YYYY-VBHN-XXX VÀ năm đó có mặt trong TÊN.
    Số VBHN tái dùng THEO NĂM ⇒ năm đủ ở cả hai nơi = hết rủi ro tái-dùng-số cho entry đó (chủ đề trơ nếu có
    là vấn đề NAME hygiene riêng, không phải reuse)."""
    m = _VBHN_WITHYEAR_RE.fullmatch(_sohieu_key_entry(e) or "")
    return bool(m and re.search(rf"(?<!\d){m.group(2)}(?!\d)", _entry_name(e) or ""))


def _vbhn_year_fix_items(entries: list) -> tuple[list, list, list]:
    """Quét entry VBHN có SỐ HIỆU THIẾU NĂM. Trả (fixable, needs_year, conflicts):
    - fixable: suy được năm + sohieu mới DUY NHẤT → an toàn ghi.
    - needs_year: KHÔNG suy được năm offline → xác minh tay (đọc header/NLM).
    - conflicts: ≥2 dòng suy ra CÙNG sohieu mới (`NN-YYYY-VBHN-XXX`) → ghi sẽ TẠO collision MỚI (dòng dup cùng
      văn bản = phải dedup; hoặc 2 văn bản khác cùng số+năm = năm không đủ phân biệt) → KHÔNG auto-apply."""
    cand, needs = [], []
    seen = set()
    for e in entries:
        if not _is_vbhn_entry(e):
            continue
        # CHỈ sửa số hiệu của văn bản CORPUS (canonical). Sidecar/quarantine (corpus=false) KHÔNG year-fix —
        # vừa không cần, vừa tránh CONFLICT GIẢ (sidecar corpus=false va sohieu với GDoc canonical cùng số).
        if str(e.get("corpus")).lower() != "true":
            continue
        key = norm_sohieu(_entry_sohieu(e) or "")
        m = _VBHN_NOYEAR_RE.fullmatch(key)
        if not m:
            # B.5-residual (v1.33.21 — log rà v1.33.20: 15/17 title_mismatch là VBHN, 11 ca
            # VBHN_NAME_MISSING_YEAR có sohieu ĐÃ year-fix nhưng TÊN FILE còn thiếu năm
            # ['VBHN_34-VPQH_Luat_Luu_tru', '61-VBHN-VPQH_ATTP'] — KHÔNG fixer nào phủ lớp name-only →
            # backlog treo vĩnh viễn, phải rename tay ×11): lane NAME-ONLY — sohieu chuẩn NN-YYYY-VBHN-XXX
            # + tên thiếu năm-ban-hành → đề xuất đổi TÊN (mode='name_only', CHỈ ghi khi --with-name;
            # sohieu giữ nguyên nên không thể tạo collision số hiệu).
            m2 = _VBHN_WITHYEAR_RE.fullmatch(key)
            if m2:
                did2 = _entry_drive_id(e)
                nm2 = _entry_name(e)
                if did2 and did2 not in seen and str(m2.group(2)) not in (nm2 or ""):
                    _new_nm = _name_inject_vbhn_year(nm2, m2.group(1), int(m2.group(2)), m2.group(3))
                    if _new_nm and _new_nm != nm2:
                        seen.add(did2)
                        cand.append({"drive_id": did2, "old_sohieu": key, "new_sohieu": key,
                                     "year": int(m2.group(2)), "name": nm2, "new_name": _new_nm,
                                     "mode": "name_only"})
            continue                                  # sohieu đã có năm / không phải dạng VBHN chuẩn → bỏ
        did = _entry_drive_id(e)
        if not did or did in seen:
            continue
        seen.add(did)
        number, agency = m.group(1), m.group(2)
        yr = _entry_issue_year(e)
        nm = _entry_name(e)
        if yr:
            cand.append({"drive_id": did, "old_sohieu": key, "new_sohieu": _vbhn_sohieu_inject_year(key, yr),
                         "year": yr, "name": nm, "new_name": _name_inject_vbhn_year(nm, number, yr, agency)})
        else:
            needs.append({"drive_id": did, "sohieu": key, "name": nm})
    # safeguard: new_sohieu trùng nhau giữa ≥2 dòng → conflicts (ghi sẽ tạo collision mới)
    by_new: dict = {}
    for c in cand:
        by_new.setdefault(c["new_sohieu"], []).append(c)
    fixable, conflicts = [], []
    for new_sh, group in by_new.items():
        if len(group) == 1:
            fixable.append(group[0])
        else:
            conflicts.extend(group)
    return fixable, needs, conflicts


def _quarantine_fix_items(entries: list) -> dict:
    """PURE (test offline): phân loại dòng quarantine MÂU THUẪN để dọn TẤT ĐỊNH (nhóm B report rà corpus):
    - set_corpus_false: corpus=true NHƯNG file THÔ (.pdf/.docx/.doc — _entry_raw_no_gdoc) = dup định dạng gán nhầm
      corpus → set corpus=false AN TOÀN (canonical GDoc nằm chỗ khác).
    - review_restore: corpus=true NHƯNG là GDoc native → CÓ THỂ là canonical sống bị kẹt quarantine (như A1/BLLĐ) →
      KHÔNG auto, người dùng quyết khôi phục (recat ra chủ đề) hay set false.
    - normalize_label: nhãn quarantine biến thể (cat != QUARANTINE_CAT) → chuẩn hoá cat=QUARANTINE_CAT.
    - clear_stale_nlm_ref (B3/B9 v1.33.22 — MERGE bundle-21): quarantine còn nlm_source_id nhưng KHÔNG live
      (status removed*/deleted — _entry_on_nlm_live=False) → chỉ là REF TREO trong registry, clear an toàn
      (log rà 67: 4 ca stale_nlm_ref đều đã removed khỏi NLM, trước phải reg_clear tay từng dòng).
    - ghost_nlm: quarantine nhưng còn nguồn NLM LIVE → cần `nlm source delete` (verify nội dung trước, KHÔNG auto)."""
    out = {"set_corpus_false": [], "review_restore": [], "normalize_label": [], "clear_stale_nlm_ref": [], "ghost_nlm": []}
    for e in entries:
        if not _is_quarantine_cat(_entry_cat(e)):
            continue
        did = _entry_drive_id(e)
        if not did:
            continue
        row = {"drive_id": did, "sohieu": _entry_sohieu(e) or "", "name": _entry_name(e)[:60],
               "nlm_source_id": e.get("nlm_source_id") or "",
               "nlm_notebook_id": str(e.get("nlm_notebook_id") or "")}
        if str(e.get("corpus")).lower() == "true":
            (out["review_restore"] if _entry_google_doc(e) else out["set_corpus_false"]).append(row)
        if _is_quarantine_label_variant(_entry_cat(e)):
            out["normalize_label"].append(row)
        if _entry_on_nlm_live(e):
            out["ghost_nlm"].append(row)
        elif _entry_nlm(e):
            out["clear_stale_nlm_ref"].append(row)
    return out


def _quarantine_clear_stale(run_id: str, g, rows: list[dict]) -> tuple[int, list[dict]]:
    """B3/B9 (v1.33.22 — MERGE bundle-21 SỬA PRIMITIVE): clear ref NLM treo trên dòng quarantine. Bundle-21
    dùng `_journaled_reg_write` (reg_bulk) ghi giá trị RỖNG — VI PHẠM BẤT BIẾN 'ghi rỗng qua reg_bulk/upsert
    bị webapp BỎ QUA im lặng' → báo cleared nhưng KHÔNG clear gì (false-success). Đường đúng duy nhất:
    `_journaled_reg_clear` (action reg_clear keyed drive_id + confirm=yes server-side), từng dòng, kèm before
    để `tl undo` khôi phục được."""
    ok_n, fail = 0, []
    for r in rows or []:
        v = _journaled_reg_clear(run_id, g, r["drive_id"], "nlm_source_id,nlm_notebook_id",
                                 before={"nlm_source_id": r.get("nlm_source_id") or "",
                                         "nlm_notebook_id": r.get("nlm_notebook_id") or ""})
        if v.get("verified"):
            ok_n += 1
        else:
            fail.append({"drive_id": r["drive_id"], "error": v.get("error") or v.get("resp")})
    return ok_n, fail


def _hygiene_groups(entries: list[dict]) -> dict:
    own_entries = [e for e in entries if _entry_row_kind(e) != "ref"]
    hygiene_entries = [e for e in own_entries if not _entry_is_own_thuong(e)]
    by_so, by_name, by_md5 = {}, {}, {}
    for e in own_entries:
        so = _sohieu_key_entry(e)
        nk = _name_key(_entry_name(e))
        md5 = e.get("md5") or e.get("md5Checksum") or ""
        if so: by_so.setdefault(so, []).append(e)
        if nk: by_name.setdefault(nk, []).append(e)
        if md5: by_md5.setdefault(md5, []).append(e)
    dup_so = {k:v for k,v in by_so.items() if len(v) > 1}
    dup_name = {k:v for k,v in by_name.items() if len(v) > 1}
    dup_md5 = {k:v for k,v in by_md5.items() if len(v) > 1}
    # C4 (v1.33.0): trùng số hiệu THẬT (≥2 corpus=true cùng phía, loại gốc+VBHN/phụ-lục/sidecar/quarantine) —
    # headline dùng số này; dup_so giữ nguyên làm số RAW tham khảo (dedup-plan/rà tay vẫn thấy đủ cụm).
    dup_so_real = {k: v for k, v in dup_so.items() if _sohieu_dup_group_real(v)}
    # P2-4 (v1.33.12 — log: sau dedup set corpus=false, counter raw KHÔNG đổi → tưởng 'dedup không chạy'):
    # biến thể ACTIVE = cụm còn ≥2 dòng corpus=true — GIẢM theo tiến độ dedup; raw đếm mọi dòng (theo thiết kế).
    def _grp_active(v):
        return sum(1 for e in v if str(e.get("corpus")).lower() == "true") >= 2
    dup_name_active = {k: v for k, v in dup_name.items() if _grp_active(v)}
    dup_so_raw_active = {k: v for k, v in dup_so.items() if _grp_active(v)}
    title_mismatch = []
    orphans = []
    treaties = []
    party_docs = []                # B.7 v1.33.19: văn kiện Đảng (cat 00/VK_) — không số hiệu là HỢP LỆ
    vbhn_metadata_advisory = []    # B.5-residual v1.33.22 (MERGE bundle-21): VBHN metadata — advisory, KHÔNG phải lệch tên
    omnibus_title_advisory = []    # S-2 v1.33.31: OMNIBUS_NARROW một mình = advisory trên entry, KHÔNG phải lệch tên
    sidecars = []
    ghost_nlm = []
    vbhn_reuse: dict[str, list[dict]] = {}
    for e in hygiene_entries:
        flags = _title_flags(e)
        # B.5-residual (v1.33.22 — MERGE bundle-21, log verify v1.33.20: headline 17 title_mismatch mà 15 là
        # VBHN hợp lệ theo quy ước [thiếu năm ở TÊN — việc của vbhn-year-fix --with-name, KHÔNG phải
        # source-rename/recat]): headline `title_mismatch` CHỈ còn lệch tên/tiêu đề HÀNH ĐỘNG ĐƯỢC
        # (OMNIBUS_NARROW/TITLE_METADATA); cờ VBHN metadata → bucket advisory riêng; drift NLM
        # (NLM_STATUS_MISMATCH/NOTEBOOK_ID_MISSING/CORPUS_TRUE_NOT_ON_NLM) đã có nhóm `nlm_drift` — hết đếm kép.
        # S-2 (v1.33.31 — log rà v1.33.28: 45-2019 BLLĐ đếm KÉP — cờ OMNIBUS_NARROW đã hiện ở bảng flags
        # từng entry [source-map/review-queue/corpus-audit] RỒI lại vào title_mismatch của sweep → người rà
        # tưởng 2 vấn đề; 'không sai dữ liệu' — tên hẹp vs BỊ luật sửa-nhiều-luật đụng tới, không có action
        # rename): headline title_mismatch CHỈ giữ TITLE_METADATA_MISMATCH (lệch hành-động-được);
        # OMNIBUS_NARROW một mình → bucket advisory riêng (mirror advisory-split v1.33.22 cho VBHN_*).
        if "TITLE_METADATA_MISMATCH" in flags:
            title_mismatch.append(e)
        elif "OMNIBUS_NARROW_TITLE_CHECK" in flags:
            omnibus_title_advisory.append(e)
        elif _is_vbhn_entry(e) and any(f.startswith("VBHN_") for f in flags):
            vbhn_metadata_advisory.append(e)
        if "NLM_GHOST_SOURCE" in flags:
            ghost_nlm.append(e)
        cat = _entry_cat(e).lower()
        nm = _entry_name(e)
        is_template = _name_is_template_or_appendix(nm)
        raw_name = (not is_template) and bool(re.search(r"(^|[/_ -])\d{2,4}[_-]\d{4}[_-]", nm))
        if _is_source_sidecar(e, entries):   # sidecar (file gốc của GDoc) → bucket riêng, KHÔNG tính là document
            sidecars.append(e)               # độc lập trong phân tích va chạm số hiệu (tránh false reuse/same-doc).
            continue
        if _is_vbhn_entry(e):
            vk = _sohieu_key_entry(e)
            if vk:
                vbhn_reuse.setdefault(vk, []).append(e)
        if (not is_template) and ((not _entry_sohieu(e)) or (not cat) or ("root" in cat) or (raw_name and not _entry_nlm(e))):
            # P1-8 (v1.31.0 — log LIVE: orphans=46 gộp cả Công ước ILO): điều ước quốc tế sohieu RỖNG là HỢP LỆ
            # → LỚP RIÊNG `treaties` (không đòi sohieu/tên Luat_*), KHÔNG tính orphan.
            # B.7 (v1.33.19 — log rà v1.33.18: orphans=16 gộp cả VK_DH_XIV_* văn kiện Đảng): văn kiện Đảng
            # (cat 00 / tên VK_/Van_kien) cũng KHÔNG có số hiệu VBQPPL → lớp riêng `party_docs`, không orphan.
            _nm_low = _strip_accents(nm).lower()
            if _is_treaty_entry(e):
                treaties.append(e)
            elif cat.startswith("00") or re.match(r"^(vk[_\-]|van[_ ]?kien)", _nm_low):
                party_docs.append(e)
            else:
                orphans.append(e)
    reuse_collisions = []
    same_document_dups = []        # #4: CÙNG số hiệu, KHÔNG xung đột năm/goc = nhân đôi 1 văn bản → quarantine dup
    for k, arr in vbhn_reuse.items():
        if len(arr) <= 1:
            continue
        docs = _split_distinct_vbhn_docs(arr)         # tách theo XUNG ĐỘT năm/goc (reuse-thật vs nhân-đôi)
        if len(docs) > 1:          # ≥2 văn bản KHÁC nhau dùng chung số → reuse-khác-doc (GIỮ, không quarantine)
            reuse_collisions.append({"key": k, "subjects": sorted(_doc_subject_key(g[0]) for g in docs), "entries": arr})
        for grp in docs:
            if len(grp) > 1:        # ≥2 entry CÙNG văn bản → trùng THẬT: chọn canonical (NLM/điểm cao), còn lại = dup
                canon = max(grp, key=_entry_score)
                same_document_dups.append({"key": k, "subject": _doc_subject_key(canon), "canonical": canon,
                                           "dups": [e for e in grp if e is not canon], "entries": grp})
    # G (log rà 71 luật): FILE THÔ (.doc/.docx) cạnh GDoc canonical mà LẪN corpus=true → phải set corpus=false
    # (sidecar = bản gốc bên cạnh GDoc, KHÔNG add NLM, KHÔNG tính là corpus). Bắt cặp .docx BHYT/.doc Phòng bệnh…
    # (57/60/67-2024, 91-2015/2025) đang corpus=true lẫn vào corpus. KHÁC quarantine: chỉ cần FLIP cờ corpus.
    sidecar_corpus_fix = [e for e in sidecars if _entry_corpus_true(e)]
    # P2-7: `loai` có giá trị nhưng KHÁC enum chuẩn (Luat/VBHN/nd…) → đề xuất chuẩn hoá (bucket riêng, không nhồi
    # _title_flags để tránh nhiễu source-map). Đếm để rà tay/regen2; register mới đã tự chuẩn hoá.
    loai_noncanonical = [e for e in hygiene_entries if _loai_is_noncanonical(e)]
    reconcile_clusters = _reconcile_clusters(hygiene_entries)
    duplicate_identity_groups = [c for c in reconcile_clusters if len(c.get("entries") or []) > 1]
    return {"duplicates_by_sohieu": dup_so, "duplicates_by_sohieu_real": dup_so_real,
            "duplicates_by_sohieu_raw_active": dup_so_raw_active,
            "duplicates_by_name_active": dup_name_active,
            "duplicates_by_name": dup_name,
            "duplicates_by_md5": dup_md5, "orphans": orphans, "treaties": treaties,
            "party_docs": party_docs,
            "vbhn_metadata_advisory": vbhn_metadata_advisory,
            "omnibus_title_advisory": omnibus_title_advisory,
            "sidecar_source_files": sidecars, "sidecar_corpus_fix": sidecar_corpus_fix,
            "loai_noncanonical": loai_noncanonical,
            "ghost_nlm_sources": ghost_nlm,
            "vbhn_reuse_collisions": reuse_collisions,
            "vbhn_same_document_dups": same_document_dups,
            "duplicate_identity_groups": duplicate_identity_groups,
            "title_mismatch": title_mismatch,
            "reconcile_clusters": reconcile_clusters}


def cmd_hygiene(a) -> int:
    """Registry hygiene: phát hiện duplicate/orphan kể cả dòng `sohieu` rỗng; lập kế hoạch QUARANTINE an toàn."""
    # v1.19.4: always apply profile before choosing cache. Otherwise
    # `--profile vbthuong hygiene scan` can still read the base VBQPPL cache.
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    # DRY-RUN/invalid-confirm phải đọc được cache offline; chỉ cần creds khi refresh, cache thiếu,
    # hoặc apply đã xác nhận thật.
    need_apply_creds = bool(getattr(a, "apply", False) and getattr(a, "confirm", None) == "yes")
    if a.refresh or need_apply_creds or not (_cache_file("manifest.json")).exists():
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=a.refresh)
    except Exception as e:
        print(f"[tl] hygiene: không đọc được manifest: {e}", file=sys.stderr)
        return 1
    groups = _hygiene_groups(entries)
    clusters = groups["reconcile_clusters"]
    if a.hsub == "scan":
        out = {"ok": True, "entries": len(entries),
               # C4 v1.33.0: headline = trùng THẬT (cùng phía, corpus=true); raw = mọi cụm ≥2 (gồm gốc+VBHN/
               # phụ-lục/quarantine lành) — trước đây 2 khóa cùng in raw → '93 trùng' báo động giả.
               "duplicates_by_sohieu": len(groups["duplicates_by_sohieu_real"]),
               "duplicate_sohieu_groups_raw": len(groups["duplicates_by_sohieu"]),
               "duplicate_identity_groups": len(groups["duplicate_identity_groups"]),
               "duplicates_by_name": len(groups["duplicates_by_name"]),
               "duplicates_by_md5": len(groups["duplicates_by_md5"]),
               "orphans": len(groups["orphans"]),
               "sidecar_source_files": len(groups["sidecar_source_files"]),
               "sidecar_corpus_fix": len(groups["sidecar_corpus_fix"]),
               "loai_noncanonical": len(groups["loai_noncanonical"]),
               "ghost_nlm_sources": len(groups["ghost_nlm_sources"]),
               "vbhn_reuse_collisions": len(groups["vbhn_reuse_collisions"]),
               "vbhn_same_document_dups": len(groups["vbhn_same_document_dups"]),
               "title_mismatch_candidates": len(groups["title_mismatch"]),
               "vbhn_metadata_advisory": len(groups.get("vbhn_metadata_advisory") or []),
               "omnibus_title_advisory": len(groups.get("omnibus_title_advisory") or []),
               "reconcile_clusters": len(clusters),
               "quarantine_candidates": sum(len(c["quarantine"]) for c in clusters),
               "quarantine_label_variants": sum(1 for e in entries if _is_quarantine_label_variant(_entry_cat(e))),
               # TRẠNG THÁI MÂU THUẪN: dòng trong cat quarantine NHƯNG corpus=true (lẽ ra false) hoặc còn nlm live (ghost).
               "quarantine_corpus_true": sum(1 for e in entries if _is_quarantine_cat(_entry_cat(e)) and str(e.get("corpus")).lower() == "true"),
               "quarantine_still_on_nlm": sum(1 for e in entries if _is_quarantine_cat(_entry_cat(e)) and _entry_nlm(e)),
               "samples": {"clusters": [{"key": c["key"], "canonical": _summ_entry(c.get("canonical")),
                                            "quarantine": [_summ_entry(x) for x in c["quarantine"][:5]]}
                                           for c in clusters[:10]],
                           "duplicates_by_md5": {k:[_summ_entry(x) for x in v[:5]] for k,v in list(groups["duplicates_by_md5"].items())[:10]},
                           "duplicate_identity_groups": [{"key": c.get("key"), "canonical": _summ_entry(c.get("canonical")),
                                                          "entries": [_summ_entry(x) for x in (c.get("entries") or [])[:5]]}
                                                         for c in groups["duplicate_identity_groups"][:10]],
                           "title_mismatch": [_summ_entry(x) for x in groups["title_mismatch"][:20]],
                           "vbhn_metadata_advisory": [_summ_entry(x) for x in (groups.get("vbhn_metadata_advisory") or [])[:20]],
                           "ghost_nlm_sources": [_summ_entry(x) for x in groups["ghost_nlm_sources"][:20]],
                           "vbhn_reuse_collisions": [{"key": c["key"], "subjects": c["subjects"], "entries": [_summ_entry(x) for x in c["entries"][:8]]} for c in groups["vbhn_reuse_collisions"][:20]],
                           "vbhn_same_document_dups": [{"key": c["key"], "subject": c["subject"], "canonical": _summ_entry(c["canonical"]), "dups": [_summ_entry(x) for x in c["dups"][:5]]} for c in groups["vbhn_same_document_dups"][:20]],
                           "sidecar_source_files": [_summ_entry(x) for x in groups["sidecar_source_files"][:20]],
                           "sidecar_corpus_fix": [_summ_entry(x) for x in groups["sidecar_corpus_fix"][:20]],
                           "loai_noncanonical": [(_summ_entry(x) or {}) | {"loai_raw": str(x.get("loai") or ""), "loai_suggested": _normalize_loai(x.get("loai"))} for x in groups["loai_noncanonical"][:20]],
                           "orphans": [_summ_entry(x) for x in groups["orphans"][:20]]}}
        if a.json:
            print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
        else:
            print(f"entries={out['entries']} dup_sohieu_raw={out['duplicate_sohieu_groups_raw']} dup_identity={out['duplicate_identity_groups']} dup_name={out['duplicates_by_name']} "
                  f"dup_md5={out['duplicates_by_md5']} orphans={out['orphans']} reconcile_clusters={out['reconcile_clusters']} "
                  f"title_mismatch={out['title_mismatch_candidates']} vbhn_advisory={out['vbhn_metadata_advisory']} "
                  f"omnibus_advisory={out['omnibus_title_advisory']} "
                  f"same_doc_dups={out['vbhn_same_document_dups']} quarantine_candidates={out['quarantine_candidates']}")
            for d in groups["vbhn_same_document_dups"][:10]:   # #4: trùng CÙNG văn bản (cùng số hiệu) → cần dọn
                print(f"  ⚠TRÙNG-CÙNG-VĂN-BẢN [{d['key']}] giữ «{_entry_name(d['canonical'])[:48]}» · dọn {len(d['dups'])}: "
                      + "; ".join(_entry_name(x)[:36] for x in d["dups"][:4]))
            _print_reconcile(clusters[:20])
        return 0
    # plan/query/reconcile
    q = getattr(a, "query", "") or ""
    selected, skipped = _select_hygiene_clusters(clusters, q)
    # #4: bổ sung cụm TRÙNG-CÙNG-VĂN-BẢN (cùng số hiệu + cùng chủ đề) làm ứng viên quarantine — reconcile bỏ sót
    for d in groups.get("vbhn_same_document_dups", []):
        sdc = {"key": d["key"], "canonical": d["canonical"], "quarantine": d["dups"], "entries": d["entries"]}
        if _cluster_matches(sdc, q) and not any(c.get("key") == d["key"] for c in selected):
            selected.append(sdc)
    quarantine = [e for c in selected for e in c.get("quarantine") or []]
    # G: file thô .doc/.docx cạnh GDoc đang corpus=true → đề xuất SET_CORPUS_FALSE (KHÁC quarantine: chỉ flip cờ,
    # KHÔNG move cat). Lọc theo query để khớp scope plan. DRY: chỉ trình hành động, KHÔNG tự ghi registry.
    _sidecar_fix = [e for e in groups.get("sidecar_corpus_fix", [])
                    if (not q) or _entry_query_match_safe_for_hygiene(q, e)]
    out = {"ok": True, "query": q or None,
           "clusters": [{"key": c["key"], "canonical": _summ_entry(c.get("canonical")),
                         "quarantine_candidates": [_summ_entry(e) for e in c.get("quarantine") or []]}
                        for c in selected],
           "sidecar_corpus_fix": [(_summ_entry(e) or {}) | {"action": "SET_CORPUS_FALSE"} for e in _sidecar_fix],
           "skipped_clusters": [{"key": c.get("key"), "skip_reason": c.get("skip_reason"),
                                 "entries": [_summ_entry(e) for e in (c.get("entries") or [])[:5]]}
                                for c in skipped],
           "quarantine_candidates": [_summ_entry(e) for e in quarantine],
           "note": "DRY-RUN. Dùng --apply --confirm yes để move cat=QUARANTINE; không trash. skipped_clusters=thiếu canonical, chỉ rà tay."}
    if a.apply:
        if a.confirm != "yes":
            out["ok"] = False; out["error"] = "cần --confirm yes để apply"
            print(_json_dumps(out, deterministic=_deterministic_enabled(a))); return 2
        out["applied"] = _apply_quarantine(quarantine, getattr(a, "to_cat", None) or "QUARANTINE")
    if a.json or a.hsub in ("plan", "reconcile"):
        print(_json_dumps(out, deterministic=_deterministic_enabled(a)))
    else:
        _print_reconcile(selected)
    return 0 if out.get("ok") else 1


def cmd_registry_doctor(a) -> int:
    """Chạy registry_hygiene.py nếu có: báo duplicate/orphan/root/raw rows, không mutate Drive."""
    script = HERE / "registry_hygiene.py"
    if not script.exists():
        print("[tl] thiếu scripts/registry_hygiene.py", file=sys.stderr)
        return 2
    # Nếu đã truyền --manifest local thì không cần credential/webapp.
    if not getattr(a, "manifest", None):
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    cmd = [sys.executable, str(script)]
    if getattr(a, "manifest", None):
        cmd += ["--manifest", a.manifest]
    if getattr(a, "json", False):
        cmd += ["--json"]
    if getattr(a, "limit", None):
        cmd += ["--limit", str(a.limit)]
    return subprocess.call(cmd)


def cmd_cat_audit(a) -> int:
    """AUDIT CẤP 2: rà mỗi doc corpus xem folder chủ đề có khớp suy luận từ TÊN (từ khóa → 45 chủ đề) không.
    Gắn cờ khi tên gợi MẠNH một chủ đề khác folder hiện tại. Read-only (xuất lệnh recat đề xuất)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] cat-audit: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    pd = _load_phapdien()
    tax = _cat_taxonomy()
    flags, tax_bad = [], []
    for e in entries:
        if str(e.get("corpus")).lower() != "true":
            continue
        ec = str(_entry_cat(e) or "")
        fc = ec.split("_")[0] if re.match(r"\d", ec) else ""
        nm = _entry_name(e); did = _entry_drive_id(e)
        if fc and fc not in tax:                  # cat hiện tại NGOÀI 45+2 (G3: validate taxonomy)
            tax_bad.append({"folder": fc, "drive_id": did, "name": nm})
        if fc in ("", "00", "23"):                # bỏ root + Đảng + điều ước (nội dung khác lĩnh vực là bình thường)
            continue
        if fc == "46" and not _is_vbhn_entry(e) and _omnibus_name_evidence(e):
            # S-3 (v1.33.15 — log rà 40: cat-audit gợi dời 57-2024 omnibus 46→34): rổ 46 = luật sửa nhiều luật
            # (doctrine §13, PHI-pháp-điển) — heuristic đề-tài level-2 (_infer_cats/alias) là NHIỄU với omnibus.
            # Bằng chứng omnibus lấy từ TÊN/REF (không lấy cat 46 làm bằng chứng cho chính nó — lập luận vòng).
            continue
        forced, rule = _cat_boundary_rule(nm)     # quy tắc ranh giới theo TÊN (tín hiệu MẠNH, ưu tiên)
        inf = _infer_cats(nm)
        if forced and forced != fc:
            flags.append({"folder": fc, "suggest": [forced], "rule": rule, "confidence": "high", "drive_id": did, "name": nm})
        elif inf and fc not in inf:
            flags.append({"folder": fc, "suggest": inf, "rule": None,
                          "confidence": "medium" if len(inf) == 1 else "low", "drive_id": did, "name": nm})
        elif not forced and not inf and re.match(r"^(Luat|Bo_?luat|BL[A-Z]{2,})[_\-]", nm, re.I):
            # N3 (v1.31.1 — cat_audit_strict phiên rà): tầng ALIAS pháp điển (giàu hơn _CAT_KEYWORDS) bắt cat
            # SAI-có-giá-trị offline khi boundary + keyword-tên đều im — ca thật 143-2025 'Đầu tư' nằm 45 Y tế,
            # 46-2024 'Công chứng' nằm 09. Precision-first: chỉ Luật/Bộ luật, alias ≥5 ký tự longest-match,
            # subject = tail-pretty + title_vn (giàu thêm sau backfill-title-vn). REVIEW-tay, không auto.
            _exp, _al = _expected_cat_from_alias(f"{_name_tail_pretty(nm)} {e.get('title_vn') or ''}")
            if _exp and _exp != fc:
                flags.append({"folder": fc, "suggest": [_exp], "rule": f"alias:{_al}", "confidence": "medium",
                              "check": "CAT_LIKELY_WRONG", "drive_id": did, "name": nm})
    flags.sort(key=lambda x: (x["confidence"] != "high", x["folder"]))
    # v1.30.1 (#8 log): cat-audit CỐ Ý ít cờ (heuristic TÊN, precision-first) — tự khai độ phủ để không bị dùng
    # nhầm làm audit duy nhất (log: 1 cờ/515 doc trong khi sweep thấy 77 loai + 29 title_mismatch — KHÁC CHIỀU đo).
    _cov = ("cat-audit = heuristic TÊN level-2, precision-first (ít cờ là THIẾT KẾ, không phải corpus sạch). "
            "Audit sâu đọc HEADER thật: `tl corpus-audit [--offset N]` (level-3, có SOHIEU/LOAI/NAME/CAT mismatch); "
            "sức khoẻ tổng: `tl sweep`; nội dung từng file: `tl cat-verify <id>`.")
    if getattr(a, "json", False):
        # v1.33.7: +scanned — 0 finding với scanned lớn = precision-first thật; scanned nhỏ/0 = chưa quét gì
        # (log rà v1.33.6 báo 'cat-audit 0 mismatch' trong khi canonical + cache flag đủ 2 ca — minh bạch để đối chiếu).
        print(json.dumps({"ok": True, "gate": "G3", "scanned": sum(1 for e in entries if str(e.get("corpus")).lower() == "true"),
                          "count": len(flags), "flags": flags,
                          "taxonomy_violations": tax_bad, "coverage_note": _cov}, ensure_ascii=False, indent=2))
    else:
        print(f"== cat-audit: {len(flags)} doc NGHI sai chủ đề (quy tắc ranh giới + từ khóa tên) ==")
        print(f"  ℹ {_cov}")
        for fl in flags:
            ten = "/".join((pd.get(c) or {}).get("ten", c) for c in fl["suggest"])
            tag = "RULE" if fl["rule"] else fl["confidence"]
            print(f"  [{tag:6s}] folder {fl['folder']} → {','.join(fl['suggest']):8s} | {fl['name'][:44]:44s} [{fl['drive_id'][:14]}] ({ten[:34]})")
        if tax_bad:
            print(f"  ⚠ {len(tax_bad)} doc cat NGOÀI 45+2: " + ", ".join(f"{t['folder']}({t['name'][:18]})" for t in tax_bad[:8]))
        print("  (Khắc phục: tl cat-verify <drive_id> (đọc nội dung) → tl recat <drive_id> --cat <NN> [--force-cat] --apply. RULE=ranh giới cứng.)")
    return 1 if (getattr(a, "strict", False) and (flags or tax_bad)) else 0


def _backfill_loai_candidates(entries: list, normalize: bool = False) -> tuple[list[dict], int, list[dict]]:
    """v1.30.1 (#4 log — PURE): ứng viên ghi cột `loai`. Mặc định: CHỈ dòng loai RỖNG (suy từ tên/sohieu — hành vi
    cũ, idempotent). normalize=True: THÊM dòng loai PHI-CHUẨN map được TẤT ĐỊNH qua _normalize_loai (vd 'Luat'→
    'Luật', 'nd'→'Nghị định') — trước đây sweep gợi `backfill-loai --apply` cho loai_noncanonical nhưng lệnh BỎ QUA
    mọi dòng đã-có-loai ⇒ 77 dòng phi-chuẩn KHÔNG BAO GIỜ được sửa (gap log 2026-07-03 #4). Giá trị lạ không map
    được → nonmappable (báo, KHÔNG đoán). Trả (sug, unsure_rỗng, nonmappable)."""
    sug, unsure, nonmap = [], 0, []
    for e in entries or []:
        raw = str(e.get("loai") or "").strip()
        if not raw:
            loai = _infer_loai(_entry_name(e), _entry_sohieu(e))
            if loai:
                sug.append({"drive_id": _entry_drive_id(e), "sohieu": _entry_sohieu(e),
                            "name": _entry_name(e)[:54], "loai": loai, "mode": "fill"})
            else:
                unsure += 1
            continue
        if normalize and raw not in _LOAI_CANON_VALUES:
            fixed = _normalize_loai(raw)   # v1.33.14: nhãn KÉP 'A/B' đã tách VẾ ĐẦU ngay trong _normalize_loai
            # P2-3b → MERGE nhánh-3 v1.33.14: tên prefix VBHN_ là bằng chứng ĐỦ MẠNH MỘT MÌNH (tên chuẩn hoá
            # của CHÍNH TA đặt) — mọi nhãn khác 'Văn bản hợp nhất' trên dòng VBHN_ đều vô lý → conflict.
            # Lịch sử nới dần có kiểm chứng: S3 v1.32.2 đòi 2 bằng chứng (tên+sohieu) → 2 ca THẬT lọt lưới
            # (115 loai='Luật', 67-2025 loai='thuong' sohieu thiếu -VBHN-) → name-only; propose-only/DRY nên
            # rủi ro nới = 0 ghi tự động.
            if re.match(r"^VBHN[_\-]", str(_entry_name(e) or "")):
                sug.append({"drive_id": _entry_drive_id(e), "sohieu": _entry_sohieu(e),
                            "name": _entry_name(e)[:54], "loai": "Văn bản hợp nhất", "loai_raw": raw,
                            "mode": "conflict"})
                continue
            if fixed in _LOAI_CANON_VALUES and fixed != raw:
                sug.append({"drive_id": _entry_drive_id(e), "sohieu": _entry_sohieu(e),
                            "name": _entry_name(e)[:54], "loai": fixed, "loai_raw": raw, "mode": "normalize"})
            else:
                nonmap.append({"drive_id": _entry_drive_id(e), "loai_raw": raw, "name": _entry_name(e)[:40]})
            continue
        if normalize and raw in _LOAI_CANON_VALUES and raw != "Văn bản hợp nhất":
            # Nhánh enum-hợp-lệ nhưng VÔ LÝ trên dòng VBHN_ (ca 115 loai='Luật', 'Văn bản thường'…) — cùng
            # trigger name-only v1.33.14 (thay điều kiện 2-bằng-chứng S3).
            _nm = str(_entry_name(e) or "")
            if re.match(r"^VBHN[_\-]", _nm):
                sug.append({"drive_id": _entry_drive_id(e), "sohieu": _entry_sohieu(e),
                            "name": _nm[:54], "loai": "Văn bản hợp nhất", "loai_raw": raw, "mode": "conflict"})
    return sug, unsure, nonmap


def cmd_backfill_loai(a) -> int:
    """KH1 Pha 1.5: suy `loai` CHUẨN cho dòng registry ĐỂ TRỐNG (loai rỗng) từ tiền tố tên + mã số hiệu
    (`_infer_loai`). ★ v1.30.1 `--normalize`: sửa CẢ dòng loai PHI-CHUẨN map tất định ('Luat'→'Luật') — đường sửa
    77 dòng loai_noncanonical của sweep. DRY mặc định; --apply ghi reg_bulk cột loai. IDEMPOTENT; chỉ ghi khi CHẮC."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] backfill-loai: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    sug, unsure, nonmap = _backfill_loai_candidates(entries, normalize=getattr(a, "normalize", False))
    lim = getattr(a, "limit", None) or len(sug)
    sel = [s for s in sug[:lim] if s["drive_id"]]
    if getattr(a, "apply", False):
        _ok_gate, _ = _apply_gate(a, write_cols="loai")
        if not _ok_gate:
            return 2
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        except (Exception, SystemExit):
            pass
        g = _gas()
        run_id = _apply_journal_start("backfill-loai", {"n": len(sel)})
        # Review v1.30.1 (CONFIRMED): kèm before{loai cũ} → `tl undo` khôi phục được (fill: rỗng; normalize: loai_raw).
        _before = {s["drive_id"]: {"loai": s.get("loai_raw") or ""} for s in sel}
        v = _journaled_reg_write(run_id, g, [{"drive_id": s["drive_id"], "loai": s["loai"]} for s in sel], "loai",
                                 before_by_key=_before) if sel else {"patched": 0}
        _invalidate_manifest_cache()
        _journal_append(run_id, {"t": "run_end", "ok": True, "counts": {"applied": v.get("patched")}})
        print(json.dumps({"ok": True, "applied": v.get("patched"), "suggested": len(sug), "unsure": unsure,
                          "nonmappable": len(nonmap), "journal": run_id}, ensure_ascii=False))
        print(f"[tl] backfill-loai: ghi {v.get('patched')}/{len(sel)}. journal={run_id}. MANIFEST_STALE: `tl boot --refresh`.", file=sys.stderr)
        return 0
    from collections import Counter
    cnt = Counter(s["loai"] for s in sug)
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "mode": "DRY", "normalize": bool(getattr(a, "normalize", False)),
                          "suggested_count": len(sug), "unsure": unsure,
                          "nonmappable_count": len(nonmap), "nonmappable": nonmap[:20],
                          "distribution": dict(cnt), "suggested": sel}, ensure_ascii=False, indent=2))
    else:
        print(f"== backfill-loai DRY{' +normalize' if getattr(a, 'normalize', False) else ''} · suy được {len(sug)} "
              f"· không chắc {unsure} · phi-chuẩn-không-map-được {len(nonmap)} (--apply để ghi) ==")
        print("  phân bố: " + ", ".join(f"{k}={v}" for k, v in cnt.most_common()))
        for s in sel[:20]:
            _m = "≪norm≫" if s.get("mode") == "normalize" else "      "
            print(f"  {_m} {s['loai']:18s} {(s['sohieu'] or '(?)'):16s} {s['name']}"
                  + (f"  (loai cũ: {s['loai_raw']})" if s.get("loai_raw") else ""))
        for x in nonmap[:8]:
            print(f"  ⚠ KHÔNG map được: loai='{x['loai_raw']}' — {x['name']} [{x['drive_id'][:12]}] (sửa tay qua register)")
        if not getattr(a, "normalize", False):
            print("  ℹ dòng loai PHI-CHUẨN (đã có giá trị nhưng sai enum) chỉ được sửa khi thêm `--normalize`.")
    return 0


def cmd_backfill_titlevn(a) -> int:
    """P0-1 (v1.31.0 — log LIVE 2026-07-03): BACKFILL cột `title_vn` (TRÍCH YẾU CÓ DẤU — cột registry SẴN CÓ
    v2.13.0, không cần đổi schema/GAS) từ HEADER thật. Sau backfill, QT-5 (_derive_subject_from_entries ưu tiên
    _META_TITLE_KEYS) sinh query có dấu → site:vbpl/congbao recall đúng, hết literal-filename. Đọc header per-file
    (heartbeat, --limit/--offset phân trang như corpus-audit); DRY mặc định; --apply journaled reg_bulk cột
    title_vn (before→undo). Dòng KHÔNG tự tin (mất dấu/boilerplate) → skip LOUD, sửa tay `tl register --title-vn`."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] backfill-title-vn: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    cands = _backfill_titlevn_candidates(entries, force=getattr(a, "force_refresh", False))
    _pool = len(cands)
    _off = max(0, int(getattr(a, "offset", None) or 0))
    # A2 (v1.33.43 — MERGE bundle-17, KẸT PAGINATION LIVE: ép _off=0 ở --apply + next_offset=None → khi lô đầu
    # TOÀN skip [boilerplate] pool KHÔNG co ⇒ mọi lần chạy lặp đúng lô đầu, KHÔNG BAO GIỜ tới dòng sau — pool 79
    # mà 0/79 quét được): thiết kế cũ 'pool tự co' chỉ đúng khi CÓ dòng ghi được. Nay HONOR --offset ở --apply;
    # next_offset TIẾN QUA số dòng SKIP (dòng ghi được rời pool nên offset không nhảy cóc — xem nhánh apply dưới).
    # N2 (v1.31.1): --from-tukhoa = tier-2 OFFLINE (bóc từ field tukhoa, 0 call/dòng — quét cả pool 1 phát);
    # mặc định = tier-1 đọc HEADER thật (chậm, lô 40). Chạy tukhoa TRƯỚC cho phủ nhanh, header vét phần còn lại.
    _src_tukhoa = bool(getattr(a, "from_tukhoa", False))
    lim = getattr(a, "limit", None) or (len(cands) if _src_tukhoa else 40)
    page = cands[_off:_off + lim]
    _next = (_off + len(page)) if (_off + len(page)) < _pool else None
    done, skipped, need_read, err = [], [], [], []
    _read_fail_streak = 0
    for _ci, c in enumerate(page, 1):
        e = c["entry"]
        if _src_tukhoa:
            tv, why = _title_vn_from_tukhoa(e.get("tukhoa"), c["name"]), "TUKHOA_NO_CLEAN_TITLE"
        else:
            print(f"[backfill-title-vn] {_ci}/{len(page)} {c['name'][:48]}", file=sys.stderr, flush=True)
            if _entry_raw_no_gdoc(e):
                need_read.append({"drive_id": c["drive_id"], "name": c["name"][:55]}); continue
            try:
                txt = _read_doc_text(c["drive_id"], getattr(a, "config", None))
            except Exception:  # noqa: BLE001
                txt = ""
            if not (txt or "").strip():
                txt = _read_doc_text_via_nlm(e)     # P1 v1.32.1: Drive chết → thử NLM
            if not (txt or "").strip():
                err.append({"drive_id": c["drive_id"], "name": c["name"][:55], "error": "header rỗng (Drive+NLM)"})
                _read_fail_streak += 1
                if _read_fail_streak >= 3:          # P1 v1.32.1: fast-fail như corpus-audit — không cày pool all-error
                    print("[tl] backfill-title-vn: 3 lỗi đọc LIÊN TIẾP (Drive+NLM) → READ_BACKEND_DOWN, dừng. "
                          "Chẩn đoán `tl gws-ping`; khắc phục `gws auth login` → `tl secrets-set --gws`; "
                          "tạm dùng --from-tukhoa (offline, không cần đọc Drive).", file=sys.stderr)
                    return 2
                continue
            _read_fail_streak = 0
            tv, why = _title_vn_from_header(txt, e)
        if tv:
            done.append({"drive_id": c["drive_id"], "name": c["name"][:54], "title_vn": tv,
                         "title_vn_cur": c["title_vn_cur"]})
        else:
            skipped.append({"drive_id": c["drive_id"], "name": c["name"][:50], "reason": why})
    summary = {"ok": True, "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
               "source": "tukhoa (tier-2 offline)" if _src_tukhoa else "header (tier-1)",
               "pool_total": _pool, "offset": _off, "scanned": len(page), "next_offset": _next,
               "coverage_complete": _next is None, "writable": len(done), "skipped": skipped,
               "need_manual_read": need_read, "errors": err,
               "note": "skip NO_DIACRITICS/BOILERPLATE = KHÔNG tự tin — sửa tay `tl register --drive-id <id> "
                       "--title-vn \"<trích yếu có dấu>\"`; raw .docx/.pdf → Claude đọc header rồi register tay."}
    if not getattr(a, "apply", False):
        summary["rows"] = done
        # MERGE bundle-45b (v1.33.47): --out ghi JSON summary atomic qua _emit_json_payload (đồng bộ doctor/
        # sweep/counts/corpus-audit) — trước thiếu, Cowork phải `>` redirect vỡ trần output.
        if getattr(a, "out", None) or getattr(a, "json", False):
            _emit_json_payload(summary, getattr(a, "out", None))
        if not (getattr(a, "json", False) or getattr(a, "out", None)):
            print(f"== backfill-title-vn DRY · pool={_pool} · trang này ghi được {len(done)} · skip {len(skipped)} "
                  f"· cần đọc tay {len(need_read)} · lỗi {len(err)} ==")
            for d in done[:20]:
                print(f"  {d['title_vn'][:70]:70s} ← {d['name'][:40]}")
            for s in skipped[:10]:
                print(f"  ⚠ SKIP {s['reason']:14s} {s['name']}")
            if _next is not None:
                print(f"  ⚠ CHƯA PHỦ HẾT — trang kế: --offset {_next} (mặc định lô 40 vì đọc header chậm)")
            print("  --apply để ghi (journaled, undo được).")
        return 0
    _ok_gate, _ = _apply_gate(a, write_cols="title_vn")
    if not _ok_gate:
        return 2
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (Exception, SystemExit):
        pass
    g = _gas()
    run_id = _apply_journal_start("backfill-title-vn", {"n": len(done)})
    _before = {d["drive_id"]: {"title_vn": d.get("title_vn_cur") or ""} for d in done}
    v = _journaled_reg_write(run_id, g, [{"drive_id": d["drive_id"], "title_vn": d["title_vn"]} for d in done],
                             "title_vn", before_by_key=_before) if done else {"patched": 0}
    _invalidate_manifest_cache()
    _journal_append(run_id, {"t": "run_end", "ok": True, "counts": {"applied": v.get("patched")}})
    summary["applied"] = v.get("patched")
    summary["journal"] = run_id
    # A2 (v1.33.43 — MERGE bundle-17): dòng GHI ĐƯỢC rời pool (lần sau pool đã co); dòng SKIP/need_read/err CÒN
    # trong pool → offset lần sau phải TIẾN QUA chúng, nếu không lô-đầu-toàn-skip kẹt vĩnh viễn (ca live 79 dòng).
    _stay = len(skipped) + len(need_read) + len(err)
    _adv = _off + _stay
    summary["next_offset"] = _adv if (_stay > 0 and _adv < (_pool - len(done))) else None
    summary["coverage_complete"] = summary["next_offset"] is None
    summary["note_apply"] = ("dòng GHI ĐƯỢC rời pool; SKIP còn lại trong pool → trang kế chạy `--offset "
                             "<next_offset>` để QUA chúng (next_offset=None = đã phủ hết); skip = sửa tay "
                             "`tl register --title-vn`.")
    _emit_json_payload(summary, getattr(a, "out", None))   # MERGE bundle-45b: --out atomic (không out → in stdout như cũ)
    if summary["next_offset"] is not None:
        print(f"[tl] backfill-title-vn: CHƯA PHỦ HẾT — trang kế: LẶP CÙNG LỆNH + --offset {summary['next_offset']}.",
              file=sys.stderr)
    elif v.get("patched"):
        print("[tl] backfill-title-vn: đã phủ hết pool (coverage_complete).", file=sys.stderr)
    print(f"[tl] backfill-title-vn: ghi {v.get('patched')}/{len(done)}. journal={run_id}. MANIFEST_STALE: `tl boot --refresh`.",
          file=sys.stderr)
    return 0


def _backfill_hieuluc_candidates(entries: list, force: bool = False) -> list[dict]:
    """Dòng cần backfill hieuluc: corpus=true, own/overflow, hieuluc rỗng; force cho phép refresh giá trị mơ hồ."""
    vague = {"", "can_kiem_tra", "cần kiểm tra", "unknown", "không rõ", "chưa rõ"}
    out = []
    for e in entries or []:
        if not _entry_corpus_true(e) or _entry_row_kind(e) == "ref":
            continue
        cur = str(e.get("hieuluc") or e.get("hieu_luc") or "").strip()
        if cur and not force:
            continue
        if cur and force and _strip_accents(cur).lower() not in {_strip_accents(x).lower() for x in vague}:
            continue
        out.append({"drive_id": _entry_drive_id(e), "name": _entry_name(e), "hieuluc_cur": cur, "entry": e})
    return out


def cmd_backfill_hieuluc(a) -> int:
    """BACKFILL cột `hieuluc` từ header/export text. DRY mặc định; --apply ghi journaled reg_bulk cột hieuluc."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] backfill-hieuluc: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    cands = _backfill_hieuluc_candidates(entries, force=getattr(a, "force_refresh", False))
    pool = len(cands)
    off = max(0, int(getattr(a, "offset", None) or 0))
    lim = getattr(a, "limit", None) or 40
    page = cands[off:off + lim]
    next_off = (off + len(page)) if (off + len(page)) < pool else None
    done, skipped, need_read, err = [], [], [], []
    fail_streak = 0
    for i, c in enumerate(page, 1):
        e = c["entry"]
        print(f"[backfill-hieuluc] {i}/{len(page)} {c['name'][:48]}", file=sys.stderr, flush=True)
        if _entry_raw_no_gdoc(e):
            need_read.append({"drive_id": c["drive_id"], "name": c["name"][:55]}); continue
        try:
            txt = _read_doc_text(c["drive_id"], getattr(a, "config", None))
        except Exception:  # noqa: BLE001
            txt = ""
        if not (txt or "").strip():
            txt = _read_doc_text_via_nlm(e)
        if not (txt or "").strip():
            err.append({"drive_id": c["drive_id"], "name": c["name"][:55], "error": "header rỗng (Drive+NLM)"})
            fail_streak += 1
            if fail_streak >= 3:
                print("[tl] backfill-hieuluc: 3 lỗi đọc LIÊN TIẾP (Drive+NLM) → READ_BACKEND_DOWN; "
                      "chẩn đoán `tl gws-ping` / `tl nlm-auth-load` rồi chạy lại.", file=sys.stderr)
                return 2
            continue
        fail_streak = 0
        hl, why = _hieuluc_from_header_text(txt, infer_from_date=getattr(a, "infer_from_date", False))
        if hl:
            done.append({"drive_id": c["drive_id"], "name": c["name"][:54], "hieuluc": hl,
                         "hieuluc_cur": c["hieuluc_cur"]})
        else:
            skipped.append({"drive_id": c["drive_id"], "name": c["name"][:50], "reason": why})
    summary = {"ok": True, "mode": "APPLY" if getattr(a, "apply", False) else "DRY",
               "pool_total": pool, "offset": off, "scanned": len(page), "next_offset": next_off,
               "coverage_complete": next_off is None, "writable": len(done), "rows": done,
               "skipped": skipped, "need_manual_read": need_read, "errors": err,
               "infer_from_date": bool(getattr(a, "infer_from_date", False)),
               "note": "Mặc định chỉ ghi khi header có nhãn Còn/Hết/Chưa hiệu lực rõ; date-only cần --infer-from-date."}
    if not getattr(a, "apply", False):
        if getattr(a, "out", None) or getattr(a, "json", False):
            _emit_json_payload(summary, getattr(a, "out", None))
        if not (getattr(a, "json", False) or getattr(a, "out", None)):
            print(f"== backfill-hieuluc DRY · pool={pool} · trang này ghi được {len(done)} · "
                  f"skip {len(skipped)} · cần đọc tay {len(need_read)} · lỗi {len(err)} ==")
            for d in done[:20]:
                print(f"  {d['hieuluc'][:70]:70s} ← {d['name'][:40]}")
            for s in skipped[:10]:
                print(f"  ⚠ SKIP {s['reason']:18s} {s['name']}")
            if next_off is not None:
                print(f"  ⚠ CHƯA PHỦ HẾT — trang kế: --offset {next_off}")
            print("  --apply để ghi (journaled, undo được).")
        return 0
    _ok_gate, _ = _apply_gate(a, write_cols="hieuluc")
    if not _ok_gate:
        return 2
    try:
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
    except (Exception, SystemExit):
        pass
    g = _gas()
    run_id = _apply_journal_start("backfill-hieuluc", {"n": len(done)})
    before = {d["drive_id"]: {"hieuluc": d.get("hieuluc_cur") or ""} for d in done}
    v = _journaled_reg_write(run_id, g, [{"drive_id": d["drive_id"], "hieuluc": d["hieuluc"]} for d in done],
                             "hieuluc", before_by_key=before) if done else {"patched": 0}
    _invalidate_manifest_cache()
    _journal_append(run_id, {"t": "run_end", "ok": True, "counts": {"applied": v.get("patched")}})
    summary["applied"] = v.get("patched")
    summary["journal"] = run_id
    stay = len(skipped) + len(need_read) + len(err)
    adv = off + stay
    summary["next_offset"] = adv if (stay > 0 and adv < (pool - len(done))) else None
    summary["coverage_complete"] = summary["next_offset"] is None
    _emit_json_payload(summary, getattr(a, "out", None))
    if summary["next_offset"] is not None:
        print(f"[tl] backfill-hieuluc: CHƯA PHỦ HẾT — trang kế: LẶP CÙNG LỆNH + --offset {summary['next_offset']}.",
              file=sys.stderr)
    print(f"[tl] backfill-hieuluc: ghi {v.get('patched')}/{len(done)}. journal={run_id}. MANIFEST_STALE: `tl boot --refresh`.",
          file=sys.stderr)
    return 0


def cmd_missing_sohieu(a) -> int:
    """KH1 Pha 1.5: đề xuất SỐ HIỆU cho dòng registry THIẾU sohieu (field rỗng, 257 dòng) — parse từ TÊN
    (`_parse_sohieu_from_name`, bỏ Mẫu/Phụ lục). DRY mặc định; --apply ghi reg_bulk cột `sohieu` (KHÔNG `so_hieu` — webapp bỏ im lặng). ⚠ ĐỀ XUẤT theo TÊN —
    XÁC MINH bằng `tl header-verify` (G2, đọc header thật) trước khi tin tuyệt đối. Idempotent (bỏ dòng đã có sohieu)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] missing-sohieu: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    sug, no_parse = [], 0
    for e in entries:
        if str(_entry_sohieu(e) or "").strip():        # đã có sohieu field → bỏ (idempotent)
            continue
        sh = _parse_sohieu_from_name(_entry_name(e))
        if sh:
            sug.append({"drive_id": _entry_drive_id(e), "name": _entry_name(e)[:54], "sohieu_suggested": sh})
        else:
            no_parse += 1
    lim = getattr(a, "limit", None) or len(sug)
    sel = [s for s in sug[:lim] if s["drive_id"]]
    note = "ĐỀ XUẤT theo TÊN — chạy `tl header-verify` (G2) xác minh khớp HEADER trước khi tin tuyệt đối."
    if getattr(a, "apply", False):
        _ok_gate, _pfv = _apply_gate(a, write_cols="sohieu")   # (Pha 1) chống clobber/ghi-mù (cột 'sohieu' ĐÚNG, không 'so_hieu')
        if not _ok_gate:
            return 2
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        except (Exception, SystemExit):
            pass
        g = _gas()
        run_id = _apply_journal_start("missing-sohieu", {"n": len(sel)})
        _before = {s["drive_id"]: {"sohieu": ""} for s in sel}   # trước: sohieu RỖNG → undo = clear lại
        v = _journaled_reg_write(run_id, g, [{"drive_id": s["drive_id"], "sohieu": s["sohieu_suggested"]} for s in sel],
                                 "sohieu", before_by_key=_before) if sel else {"patched": 0, "verified": True}
        patched = v.get("patched") or 0
        _ok_reg = v.get("verified", True)
        _journal_append(run_id, {"t": "run_end", "ok": bool(_ok_reg), "counts": {"applied": patched, "missed": v.get("missed") or 0}})
        print(json.dumps({"ok": bool(_ok_reg), "applied": patched, "suggested": len(sug), "no_parse": no_parse, "journal": run_id, "note": note}, ensure_ascii=False))
        if sel and not _ok_reg:
            print(f"[tl] ⚠ missing-sohieu: {v.get('missed') or 0} dòng KHÔNG khớp drive_id ({v.get('missed_ids')}) — thường row mới, webapp index chưa thấy → `tl boot --refresh` rồi lặp lại.", file=sys.stderr)
        print(f"[tl] missing-sohieu: ghi {patched}/{len(sel)} (patched=0 mà không miss = đã có sohieu đúng). XÁC MINH G2 `header-verify`. journal={run_id}.", file=sys.stderr)
        return 0 if (not sel or _ok_reg) else 1
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "mode": "DRY", "suggested_count": len(sug), "no_parse": no_parse, "suggested": sel, "note": note}, ensure_ascii=False, indent=2))
    else:
        print(f"== missing-sohieu DRY · suy được {len(sug)} · không parse được {no_parse} (--apply để ghi) ==")
        for s in sel[:20]:
            print(f"  {s['sohieu_suggested']:18s} {s['name']}  [{s['drive_id'][:14]}]")
        print(f"  ⚠ {note}")
    return 0


def cmd_vbhn_year_fix(a) -> int:
    """BẤT BIẾN ĐẶT TÊN: số hiệu VBHN PHẢI có NĂM (số VBHN tái dùng theo năm → collision, vd 61/VBHN-VPQH = ATTP 2025
    + Thuế TNDN 2026). Quét registry các VBHN có sohieu THIẾU năm (`NN-VBHN-XXX`) → suy năm (ngày ban hành/tên) →
    đề xuất sohieu `NN-YYYY-VBHN-XXX` (+ tên có năm với --with-name). DRY mặc định; --apply GHI qua reg_upsert (KHÔNG
    reg_bulk — sohieu là khóa immutable, reg_bulk bỏ im lặng). Ca không suy được năm → needs_year (xác minh tay)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] vbhn-year-fix: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    fixable, needs, conflicts = _vbhn_year_fix_items(entries)
    lim = getattr(a, "limit", None) or len(fixable)
    sel = fixable[:lim]
    with_name = getattr(a, "with_name", False)
    # v1.33.21: lane name_only chỉ có nghĩa khi --with-name (sohieu giữ nguyên, chỉ đổi TÊN) — chạy không
    # --with-name thì loại khỏi sel để khỏi upsert sohieu no-op, và nhắc LOUD.
    _name_only_n = sum(1 for s in fixable if s.get("mode") == "name_only")
    if not with_name and _name_only_n:
        sel = [s for s in sel if s.get("mode") != "name_only"]
        print(f"[tl] vbhn-year-fix: {_name_only_n} ca NAME-ONLY (sohieu đã có năm, TÊN thiếu năm) bị BỎ QUA "
              f"vì thiếu --with-name — chạy lại kèm --with-name để sửa tên.", file=sys.stderr)
    if getattr(a, "apply", False):
        _ok_gate, _pfv = _apply_gate(a, write_cols=("sohieu,name" if with_name else "sohieu"))
        if not _ok_gate:
            return 2
        try:
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        except (Exception, SystemExit):
            pass
        g = _gas()
        run_id = _apply_journal_start("vbhn-year-fix", {"n": len(sel), "with_name": with_name})
        ok_n, fail = 0, []
        for s in sel:
            payload = {"drive_id": s["drive_id"], "sohieu": s["new_sohieu"]}
            before = {"sohieu": s.get("old_sohieu") or ""}
            if with_name and s.get("new_name") and s["new_name"] != s["name"]:
                payload["name"] = s["new_name"]; before["name"] = s.get("name") or ""
            v = _journaled_reg_upsert(run_id, g, payload, before=before)   # journal intent{before sohieu/name}+verify updated
            if v.get("verified"):
                ok_n += 1
            else:
                fail.append({"drive_id": s["drive_id"], "new_sohieu": s["new_sohieu"], "resp": v.get("reg_upsert") or {"error": v.get("error")}})
        _journal_append(run_id, {"t": "run_end", "ok": not fail, "counts": {"applied": ok_n, "failed": len(fail)}})
        print(json.dumps({"ok": True, "applied": ok_n, "fixable": len(fixable), "needs_year": len(needs),
                          "conflicts": len(conflicts), "failed": fail, "with_name": with_name, "journal": run_id}, ensure_ascii=False, indent=2))
        msg = f"[tl] vbhn-year-fix: ghi {ok_n}/{len(sel)} sohieu (kèm năm)"
        if fail:
            msg += f" · {len(fail)} THẤT BẠI (xem failed; drive_id cắt? reg_upsert updated=False?)"
        if needs:
            msg += f" · {len(needs)} cần xác minh năm tay"
        if conflicts:
            msg += f" · {len(conflicts)} CONFLICT (new_sohieu trùng → KHÔNG ghi; dedup/phân biệt tay)"
        print(msg + ". MANIFEST_STALE: chạy `tl boot --refresh` để cache thấy thay đổi.", file=sys.stderr)
        return 1 if (fail or conflicts) else 0
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "mode": "DRY", "fixable_count": len(fixable), "needs_year_count": len(needs),
                          "conflict_count": len(conflicts), "fixable": sel, "needs_year": needs, "conflicts": conflicts},
                         ensure_ascii=False, indent=2))
    else:
        print(f"== vbhn-year-fix DRY · ghi-được {len(fixable)} · xác-minh-tay {len(needs)} · CONFLICT {len(conflicts)} (--apply ghi fixable; --with-name sửa cả tên) ==")
        for s in sel[:30]:
            tail = f"  TÊN→ {s['new_name']}" if (s.get('new_name') != s['name']) else ""
            _mk = "📛NAME-ONLY " if s.get("mode") == "name_only" else ""
            print(f"  {_mk}{s['old_sohieu']:20s} → {s['new_sohieu']:25s} (năm {s['year']}) [{s['drive_id'][:14]}]{tail}")
        for c in conflicts[:20]:
            print(f"  🔴 CONFLICT   {c['old_sohieu']:20s} → {c['new_sohieu']} (năm {c['year']}) [{c['drive_id'][:14]}] {c['name'][:40]}")
        for n in needs[:20]:
            print(f"  ⚠ NEEDS_YEAR  {n['sohieu']:20s} {n['name'][:50]} [{n['drive_id'][:14]}]")
        print("  → fixable ghi qua reg_upsert (KHÔNG reg_bulk). CONFLICT = ≥2 dòng ra CÙNG sohieu mới → dedup (nếu trùng văn bản) HOẶC phân biệt tay (nếu khác văn bản cùng số+năm). NEEDS_YEAR: đọc header/NLM lấy ngày ban hành rồi `tl register --drive-id <id> --sohieu NN-YYYY-VBHN-XXX`.")
    return 0


def cmd_dedup_plan(a) -> int:
    """COMPOSITE: kế hoạch DEDUP toàn corpus 1 lệnh (thay chạy `hygiene plan <q>` từng cụm). GIỮ canonical, set
    corpus=false cho bản dup CÙNG văn bản (reversible). DRY mặc định; --apply ghi reg_bulk corpus=false. review (thiếu
    canonical) + dups_on_nlm (còn nguồn NLM → cân nhắc xoá nguồn tay) chỉ BÁO."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] dedup-plan: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    p = _dedup_plan(entries)
    if getattr(a, "apply", False):
        _ok_gate, _ = _apply_gate(a, write_cols="corpus")
        if not _ok_gate:
            return 2
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        g = _gas()
        run_id = _apply_journal_start("dedup-plan", {"clusters": len(p["ready"])})
        items = [{"drive_id": d["drive_id"], "corpus": "false"} for it in p["ready"] for d in it["quarantine"]]
        _before = {it2["drive_id"]: {"corpus": "true"} for it2 in items}
        v = _journaled_reg_write(run_id, g, items, "corpus", before_by_key=_before) if items else {"patched": 0, "verified": True}
        _invalidate_manifest_cache()
        _journal_append(run_id, {"t": "run_end", "ok": bool(v.get("verified", True)), "counts": {"corpus_false": v.get("patched")}})
        print(json.dumps({"ok": True, "corpus_false_patched": v.get("patched"), "clusters": len(p["ready"]), "journal": run_id,
                          "quarantined": len(items), "review": len(p["review"]), "dups_on_nlm": len(p["dups_on_nlm"]),
                          "dups_on_nlm_rows": p["dups_on_nlm"]}, ensure_ascii=False, indent=2))
        print(f"[tl] dedup-plan: corpus=false {v.get('patched')}/{len(items)} bản dup ({len(p['ready'])} cụm, GIỮ canonical) · "
              f"review {len(p['review'])} cụm thiếu canonical · {len(p['dups_on_nlm'])} dup CÒN trên NLM (cân nhắc xoá nguồn tay). "
              f"MANIFEST_STALE: `tl boot --refresh`.", file=sys.stderr)
        return 0
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "mode": "DRY", **p}, ensure_ascii=False, indent=2))
    else:
        print(f"== dedup-plan DRY · {len(p['ready'])} cụm sẽ dedup ({p['total_quarantine']} bản dup→corpus=false) · "
              f"review {len(p['review'])} cụm thiếu canonical · {len(p['dups_on_nlm'])} dup còn NLM (--apply để ghi) ==")
        for it in p["ready"][:25]:
            print(f"  GIỮ {it['canonical']['sohieu'] or '∅':20s} {it['canonical']['name'][:42]}")
            for d in it["quarantine"]:
                print(f"    ✗ dup{' [NLM]' if d['on_nlm'] else ''}: {d['name'][:50]} [{d['drive_id'][:14]}]")
        for r in p["review"][:15]:
            print(f"  🟡 REVIEW (thiếu canonical) [{r['key']}] {len(r['dups'])} bản — quyết tay")
        print("  → --apply: GIỮ canonical, set corpus=false bản dup (reversible). dup [NLM] → cân nhắc `nlm source delete` tay.")
    return 0


# ── B1 (v1.34.63 — kế hoạch `ke-hoach-dedup-corpus-B1-2026-07-18.md` ADR-1..7): `tl dedup-corpus` —
# dedup TRỤC NỘI DUNG (md5 + content-hash + BoW), COEXIST `dedup-plan` (trục chủ đề). Helper identity
# (`_content_hash`/`_bow_jaccard`/`_bow_tokens`/`_doc_type_kind`) sống ở tl_core/doc_identity.py —
# gọi qua stub tl, KHÔNG copy (drift-lock r124_b1_reuses_identity_module). ──
_DEDUP_JUNK_NAME_RE = re.compile(r"SMOKE_TEST|KhongPhaiVanBan|JUNK_TEST", re.I)


def _dedup_sohieu_reps(members: list) -> list:
    """PURE: đại diện so-content của 1 sohieu-group — gom CỤM theo md5 (cùng md5 = cùng BYTES, đã chứng
    minh trùng ở tầng md5, khỏi đọc text), mỗi cụm 1 đại diện (drive_id nhỏ nhất, tất định); dòng không
    md5 (GDoc) = cụm đơn. md5-first ADR-7: chỉ đại diện mới cần content-hash."""
    clusters = {}
    for e in members:
        key = _entry_md5(e) or ("~" + _entry_drive_id(e))
        clusters.setdefault(key, []).append(e)
    return [sorted(v, key=_entry_drive_id)[0] for _k, v in sorted(clusters.items())]


def _dedup_md5_cluster(members: list, rep) -> list:
    """PURE: từ đại diện → TOÀN CỤM cùng-md5 của nó trong group (mở rộng nhóm content đủ mọi bản bytes-hệt)."""
    m = _entry_md5(rep)
    if not m:
        return [rep]
    return [e for e in members if _entry_md5(e) == m]


def _dedup_corpus_candidates(entries: list) -> dict:
    """PURE (B1 §2.2 bước 1 — candidate-gen FREE): md5-group + sohieu-group (≥2) từ manifest, scope own-row.
    `need_content` (md5-first ADR-7): (a) đại diện cụm của sohieu-group có ≥2 đại diện (content-hash/BoW);
    (b) 1 đại diện/md5-group KHÁC sohieu (header content-verify mislabel — cùng bytes nên 1 bản đủ).
    Dòng md5-unique không thuộc group nào KHÔNG BAO GIỜ bị đọc text."""
    own = [e for e in entries if _entry_drive_id(e) and _entry_row_kind(e) == "own"]
    by_md5, by_so = {}, {}
    for e in own:
        m = _entry_md5(e)
        if m:
            by_md5.setdefault(m, []).append(e)
        k = _sohieu_key_entry(e)
        if k:
            by_so.setdefault(k, []).append(e)
    md5_groups = {k: sorted(v, key=_entry_drive_id) for k, v in by_md5.items() if len(v) > 1}
    so_groups = {k: sorted(v, key=_entry_drive_id) for k, v in by_so.items() if len(v) > 1}
    need, _seen = [], set()

    def _need(e):
        d = _entry_drive_id(e)
        if d not in _seen:
            _seen.add(d)
            need.append(e)
    for _k, v in sorted(so_groups.items()):
        reps = _dedup_sohieu_reps(v)
        if len(reps) >= 2:
            for e in reps:
                _need(e)
    for _m5, v in sorted(md5_groups.items()):
        if len({_sohieu_key_entry(e) for e in v if _sohieu_key_entry(e)}) >= 2:
            _need(v[0])
    return {"scoped": len(own), "md5_groups": md5_groups, "sohieu_groups": so_groups, "need_content": need}


def _dedup_corpus_content(cands: dict, *, refresh: bool = False, state_dir=None) -> dict:
    """I/O (B1 §2.2 bước 2): đọc text ứng viên qua `_doc_text_any` (A1 — tự cache extract_<id>.txt) →
    content-hash (doc_identity) + BoW + header; memo `.tl_state/content_hash_<did>.json` — TIN CHỈ khi
    md5 khớp (md5 đổi = file đổi; GDoc không md5 → luôn đọc lại từ extract-cache, không tin mù TTL).
    Mỗi did đọc TỐI ĐA 1 lần/lượt chạy (memo in-run)."""
    _dir = Path(state_dir) if state_dir else Path(os.environ.get("TL_DEDUP_STATE_DIR") or (HERE / ".tl_state"))
    out, _texts = {}, {}

    def _read(e):
        did = _entry_drive_id(e)
        if did not in _texts:
            t, _src = _doc_text_any(did, entry=e, refresh=refresh)
            _texts[did] = t or ""
        return _texts[did]

    def _fill(e, *, want_text: bool):
        did = _entry_drive_id(e)
        if did not in out:
            rec = None
            m = _entry_md5(e)
            typ = _doc_type_kind(str(e.get("mime") or ""), _entry_name(e))
            cp = _dir / f"content_hash_{did}.json"
            if not refresh and m and cp.exists():
                try:
                    c = json.loads(cp.read_text(encoding="utf-8"))
                    if str(c.get("md5") or "") == m and c.get("content_hash"):
                        rec = {"content_hash": str(c["content_hash"]), "type": str(c.get("type") or typ),
                               "chars": int(c.get("chars") or 0), "dieu_count": int(c.get("dieu_count") or 0),
                               "header_text": "", "bow": None, "text_empty": False, "from_cache": True}
                except Exception:  # noqa: BLE001 — cache hỏng = coi như không có cache
                    rec = None
            if rec is None:
                t = _read(e)
                rec = {"content_hash": _content_hash(t), "type": typ, "chars": len(t),
                       "dieu_count": len(re.findall(r"(?m)^\s*Điều\s+\d+", t)),
                       "header_text": t[:16000], "bow": (_bow_tokens(t) if t else set()),
                       "text_empty": not bool(t.strip()), "from_cache": False}
                try:
                    _dir.mkdir(parents=True, exist_ok=True)
                    cp.write_text(json.dumps({"schema": "dedup_content_hash.v1", "drive_id": did, "md5": m,
                                              "content_hash": rec["content_hash"], "type": rec["type"],
                                              "chars": rec["chars"], "dieu_count": rec["dieu_count"]},
                                             ensure_ascii=False), encoding="utf-8")
                except Exception:  # noqa: BLE001 — memo best-effort, không chặn kết quả
                    pass
            out[did] = rec
        if want_text and out[did].get("bow") is None and not out[did].get("text_empty"):
            t = _read(e)   # cache-hit chỉ có hash → nhóm cần so-mềm phải đọc text thật (extract-cache rẻ)
            out[did].update({"header_text": t[:16000], "bow": (_bow_tokens(t) if t else set()),
                             "chars": len(t) or out[did]["chars"], "text_empty": not bool(t.strip())})
        return out[did]

    for e in cands.get("need_content") or []:
        _fill(e, want_text=False)
    for _sk, mem in sorted((cands.get("sohieu_groups") or {}).items()):
        reps = _dedup_sohieu_reps(mem)
        if len(reps) < 2:
            continue
        hs = {}
        for r in reps:
            rec = out.get(_entry_drive_id(r))
            if rec and rec.get("content_hash") and not rec.get("text_empty"):
                hs.setdefault(rec["content_hash"], []).append(r)
        for _h, rl in sorted(hs.items()):
            if len(rl) == 1:
                _fill(rl[0], want_text=True)   # hash không khớp ai trong group → ứng viên NEAR → cần BoW
    for _m5, mem in sorted((cands.get("md5_groups") or {}).items()):
        if len({_sohieu_key_entry(e) for e in mem if _sohieu_key_entry(e)}) >= 2:
            _fill(mem[0], want_text=True)      # mislabel: header content-verify (ADR-3) — 1 bản đủ (cùng bytes)
    return out


def _dedup_corpus_pick_canonical(members: list) -> tuple:
    """PURE (ADR-4 — picker RIÊNG, KHÔNG kế thừa bug picker-chọn-ngược của dedup-plan): thứ tự GIỮ
    (1) on-NLM-live + corpus=true → (2) corpus=true → (3) tên CHUẨN (phạt hậu tố _v2/_vN + tên phi chuẩn
    thô) → (4) tie-break tất định drive_id sort. Trả (keep, act_list)."""
    def _badname(e):
        n = str(_entry_name(e) or "")
        try:
            issues = len(_name_structural_issues(n) or [])
        except Exception:  # noqa: BLE001 — checker tên lỗi thì không phạt (tie-break lo phần còn lại)
            issues = 0
        return issues + (2 if re.search(r"[_\-]v\d+(?:[_.\-]|$)", n, re.I) else 0)

    def _key(e):
        return (0 if (_entry_on_nlm_live(e) and _entry_corpus_true(e)) else 1,
                0 if _entry_corpus_true(e) else 1,
                _badname(e), _entry_drive_id(e))
    ms = sorted(members, key=_key)
    return ms[0], ms[1:]


def _dedup_corpus_classify(entries: list, content_by_did: dict, *, T: float = 0.95,
                           all_profiles: bool = False) -> dict:
    """PURE (B1 §2.2 bước 3 — test offline): phân loại nhóm ứng viên → 7 classification. Ưu tiên quyết định:
    CROSS_PROFILE_DUAL_REG (ADR-6, flag-only) > PHYSICAL_DUP (ADR-4 lằn ranh — ≥2 on-NLM-live, đẩy layer
    NLM bất biến #16) > JUNK > MISLABEL_RESOLVED/_UNRESOLVED (ADR-3 content-verify header, fail-closed) >
    DUP_EXACT (ADR-2: CÙNG TYPE + exact). docx-gốc+GDoc-convert cùng hash → legit_convert_pairs (KHÔNG
    dup). Cặp không-exact Jaccard ≥ T → NEAR_DUP_REVIEW (bất biến #6 — KHÔNG BAO GIỜ auto, act rỗng)."""
    cands = _dedup_corpus_candidates(entries)
    content_by_did = dict(content_by_did or {})
    groups, legit, counts, emitted = [], [], {}, set()

    def _summ_c(e):
        s = dict(_summ_entry(e) or {})
        s["corpus"] = str(e.get("corpus") or "")
        return s

    def _emit(cls, key, kind, typ, members, keep=None, act=None, evidence=None, suggested=None, profiles=None):
        counts[cls] = counts.get(cls, 0) + 1
        g = {"classification": cls, "key": str(key), "group_kind": kind, "type": typ or "",
             "members": [_summ_c(e) for e in members],
             "keep": (_summ_c(keep) if keep is not None else None),
             "act": [_summ_c(e) for e in (act or [])],
             "evidence": evidence or {}, "suggested_commands": suggested or []}
        if profiles is not None:
            g["profiles"] = profiles
        groups.append(g)

    def _cls_group(members, key, kind, typ):
        members = sorted(members, key=_entry_drive_id)
        profs = sorted({str(e.get("_tl_profile") or "") for e in members})
        if all_profiles and len(profs) > 1:
            _emit("CROSS_PROFILE_DUAL_REG", key, kind, typ, members, evidence={"profiles": profs},
                  suggested=["# dual-reg CHỦ ĐÍCH (ADR-6 — bài học 54 hồ sơ khảo sát): KHÔNG auto-dedup "
                             "xuyên profile; muốn gộp thì quyết TAY trong từng profile"],
                  profiles=[p for p in profs if p] or profs)
            return
        live = [e for e in members if _entry_on_nlm_live(e)]
        if len(live) >= 2:
            _emit("PHYSICAL_DUP", key, kind, typ, members,
                  evidence={"on_nlm_live": [_entry_nlm(e) for e in live]},
                  suggested=["tl nlm-audit-physical --json   # đối soát vật lý trước (bất biến #16)",
                             "tl nlm-source-remove <source_id> --apply --confirm yes   # gỡ nguồn NLM dư sau audit"])
            return
        if members and all(_DEDUP_JUNK_NAME_RE.search(str(_entry_name(e) or "")) for e in members):
            _emit("JUNK", key, kind, typ, members, keep=None, act=list(members),
                  evidence={"junk_names": [_entry_name(e) for e in members]},
                  suggested=["# JUNK: đề xuất `--mode delete` (mặc định corpus-false KHÔNG tự xóa — ADR-5)"])
            return
        so_keys = {_sohieu_key_entry(e) for e in members if _sohieu_key_entry(e)}
        if len(so_keys) >= 2:
            rec = next((content_by_did.get(_entry_drive_id(e)) for e in members
                        if (content_by_did.get(_entry_drive_id(e)) or {}).get("header_text")), None)
            hd_sohieu = ""
            if rec:
                try:   # filename ĐỂ TRỐNG có chủ đích: tên file là thứ đang bị nghi — CHỈ ruột văn bản phân xử
                    hd_sohieu = str((_classify_doc_header(str(rec.get("header_text") or ""), "") or {}).get("sohieu") or "")
                except Exception:  # noqa: BLE001 — header lỗi = không đọc được → fail-closed
                    hd_sohieu = ""
            khd = norm_sohieu(hd_sohieu.replace("_", "-")) if hd_sohieu else ""
            matches = [e for e in members if khd and _sohieu_key_entry(e) == khd]
            if len(matches) == 1:
                keep = matches[0]
                act = [e for e in members if _entry_drive_id(e) != _entry_drive_id(keep)]
                _emit("MISLABEL_RESOLVED", key, kind, typ, members, keep=keep, act=act,
                      evidence={"sohieu_header": hd_sohieu, "sohieu_registered": sorted(so_keys)},
                      suggested=[f"# header khai '{hd_sohieu}' → GIỮ {_entry_name(keep)}; act = bản gán nhãn "
                                 f"SAI (ca data-op 57-2024/67-2006/64-2020/60-2024)"])
            else:
                _emit("MISLABEL_UNRESOLVED", key, kind, typ, members,
                      evidence={"sohieu_header": hd_sohieu, "sohieu_registered": sorted(so_keys),
                                "matches": len(matches)},
                      suggested=["# fail-closed (ADR-3): header khớp 0/>1 hoặc không đọc được — phân xử TAY: "
                                 "tl doc-text <id> soi header rồi register sửa sohieu"])
            return
        keep, act = _dedup_corpus_pick_canonical(members)
        _emit("DUP_EXACT", key, kind, typ, members, keep=keep, act=act,
              evidence=({"md5": str(key)} if kind == "md5" else {"content_hash": str(key)}))

    for m5, mem in sorted(cands["md5_groups"].items()):
        typ = _doc_type_kind(str(mem[0].get("mime") or ""), _entry_name(mem[0]))
        _cls_group(mem, m5, "md5", typ)
        emitted.add(frozenset(_entry_drive_id(e) for e in mem))
    for _sk, mem in sorted(cands["sohieu_groups"].items()):
        reps = _dedup_sohieu_reps(mem)
        recs = []
        for r in reps:
            rec = content_by_did.get(_entry_drive_id(r)) or {}
            h = str(rec.get("content_hash") or "")
            if not h or rec.get("text_empty"):
                continue   # không đọc được text → KHÔNG bằng chứng → không nhóm (fail-closed)
            t = str(rec.get("type") or "") or _doc_type_kind(str(r.get("mime") or ""), _entry_name(r))
            recs.append((r, h, t, rec))
        by_ht = {}
        for r, h, t, _rec in recs:
            by_ht.setdefault((h, t), []).append(r)
        for (h, t), rlist in sorted(by_ht.items()):
            if len(rlist) < 2:
                continue
            full = []
            for r in rlist:
                full.extend(_dedup_md5_cluster(mem, r))
            fkey = frozenset(_entry_drive_id(e) for e in full)
            if fkey in emitted:
                continue
            emitted.add(fkey)
            _cls_group(full, h, "content", t)
        hs = {}
        for r, h, t, _rec in recs:
            hs.setdefault(h, []).append((r, t))
        for h, lst in sorted(hs.items()):
            if len(lst) >= 2 and len({t for _r, t in lst}) >= 2:
                legit.append({"content_hash": h, "sohieu_key": _sk,
                              "members": [{"drive_id": _entry_drive_id(r), "name": _entry_name(r), "type": t}
                                          for r, t in sorted(lst, key=lambda x: _entry_drive_id(x[0]))],
                              "note": "docx/pdf GỐC + GDoc CONVERT cùng nội dung = KHÔNG trùng "
                                      "(định nghĩa user 2026-07-16 — lưu trữ gốc + bản đưa NLM, cả 2 hợp lệ)"})
        for i in range(len(recs)):
            for j in range(i + 1, len(recs)):
                ra, ha, ta, reca = recs[i]
                rb, hb, tb, recb = recs[j]
                if ha == hb:
                    continue
                ba, bb = reca.get("bow"), recb.get("bow")
                if not ba or not bb:
                    continue
                jac = _bow_jaccard(ba, bb)
                if jac < T:
                    continue
                pair = sorted([ra, rb], key=_entry_drive_id)
                pkey = frozenset(_entry_drive_id(e) for e in pair)
                if pkey in emitted:
                    continue
                emitted.add(pkey)
                _emit("NEAR_DUP_REVIEW", "~".join(_entry_drive_id(e) for e in pair), "near",
                      (ta if ta == tb else f"{ta}|{tb}"), pair, keep=None, act=[],
                      evidence={"jaccard": round(jac, 4),
                                "delta_dieu": abs(int(reca.get("dieu_count") or 0) - int(recb.get("dieu_count") or 0)),
                                "delta_chars": abs(int(reca.get("chars") or 0) - int(recb.get("chars") or 0))},
                      suggested=["# bất biến #6 gốc-vs-sửa-đổi: GIỮ CẢ HAI — chỉ dedup sau khi RÀ TAY xác "
                                 "nhận trùng thật (ca 155-2018 _v2 0.983 / 25-2021 _MyPham 0.992)"])
    groups.sort(key=lambda g: (g["classification"], str(g.get("key") or "")))
    return {"groups": groups, "counts": counts, "legit_convert_pairs": legit,
            "scoped": cands["scoped"], "md5_group_count": len(cands["md5_groups"]),
            "sohieu_group_count": len(cands["sohieu_groups"])}


def cmd_dedup_corpus(a) -> int:
    """B1 (v1.34.63): `tl dedup-corpus` — dedup TRỤC NỘI DUNG toàn corpus (md5-first → content-hash →
    BoW-Jaccard), 7 classification, canonical-picker on-NLM-first RIÊNG. DRY mặc định; `--apply --confirm
    yes` mặc định `--mode corpus-false` (reversible — ủy quyền `source-update-corpus` TỪNG id: guard
    shared-source + gỡ NLM + journal-undo có sẵn); `--mode delete` OPT-IN (ủy quyền `source-delete` —
    trash Drive + reg row) cho file Drive dư/JUNK; guards fail-closed đè MỌI mode (ADR-5); `--only-md5`/
    `--limit` duyệt từng bước (ADR-7); `--all-profiles` FLAG-ONLY (ADR-6)."""
    try:
        apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    except (SystemExit, Exception):  # noqa: BLE001
        pass
    try:   # lazy-creds best-effort NGAY ĐẦU (khuôn doc-text A1): máy có config nhưng chưa boot-cache vẫn
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))   # tự nạp manifest; thiếu → fail sạch dưới
    except (SystemExit, Exception):  # noqa: BLE001
        pass
    _mode = str(getattr(a, "mode", "corpus-false") or "corpus-false")
    _apply = bool(getattr(a, "apply", False))
    _allp = bool(getattr(a, "all_profiles", False))
    try:
        T = float(getattr(a, "near_threshold", 0.95) or 0.95)
    except (TypeError, ValueError):
        T = 0.95
    if _apply and _allp:
        print(json.dumps({"ok": False, "error": "APPLY_ALL_PROFILES_UNSUPPORTED",
                          "note": "--all-profiles là chế độ FLAG-ONLY (ADR-6: cross-profile = dual-reg chủ "
                                  "đích, KHÔNG auto-dedup) — bỏ --all-profiles rồi apply trong TỪNG profile."},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    profiles_loaded, profile_errors = [], []
    if _allp:
        cfg = None
        for p in _config_candidates(getattr(a, "config", None) or os.environ.get("TL_CONFIG_PATH")):
            if p and Path(p).exists():
                cfg = _read_json_file(p)
                if cfg:
                    break
        if not cfg:
            print("[tl] dedup-corpus --all-profiles: không đọc được config (danh sách profiles).", file=sys.stderr)
            return 2
        try:
            _orig = _active_profile()
        except Exception:  # noqa: BLE001
            _orig = None
        entries = []
        try:
            for pname in sorted(_profiles_from_config(cfg)):
                try:
                    apply_profile_offline(getattr(a, "config", None), pname)
                    for e in _manifest_entries(refresh=getattr(a, "refresh", False)):
                        entries.append({**e, "_tl_profile": pname})
                    profiles_loaded.append(pname)
                except Exception as pe:  # noqa: BLE001 — profile chưa boot: báo, không chặn profile khác
                    profile_errors.append({"profile": pname, "error": str(pe)[:160]})
        finally:
            try:
                apply_profile_offline(getattr(a, "config", None), _orig)
            except Exception:  # noqa: BLE001
                pass
        if not entries:
            print(json.dumps({"ok": False, "error": "NO_PROFILE_MANIFEST", "profile_errors": profile_errors,
                              "note": "không nạp được manifest profile nào — `tl boot` từng profile trước."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
    else:
        try:
            entries = _manifest_entries(refresh=getattr(a, "refresh", False))
        except Exception as e:  # noqa: BLE001
            print(f"[tl] dedup-corpus: cần `tl boot` trước ({e}).", file=sys.stderr)
            return 2
    cands = _dedup_corpus_candidates(entries)
    if cands.get("need_content"):
        try:   # lazy-creds best-effort (khuôn doc-text A1): ứng viên chưa có extract-cache cần export/download
            load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        except (SystemExit, Exception):  # noqa: BLE001
            pass
    content = _dedup_corpus_content(cands, refresh=getattr(a, "refresh", False))
    rep = _dedup_corpus_classify(entries, content, T=T, all_profiles=_allp)
    _AUTO = {"DUP_EXACT", "MISLABEL_RESOLVED"} | ({"JUNK"} if _mode == "delete" else set())
    _GUARD = {"MISLABEL_UNRESOLVED", "PHYSICAL_DUP", "NEAR_DUP_REVIEW", "CROSS_PROFILE_DUAL_REG"}
    sel = [g for g in rep["groups"] if g["classification"] in _AUTO and g["act"]]
    _only = str(getattr(a, "only_md5", "") or "")
    if _only:
        sel = [g for g in sel if str(g.get("key") or "") == _only
               or str((g.get("evidence") or {}).get("md5") or "") == _only]
    _lim = getattr(a, "limit", None)
    if _lim:
        sel = sel[:max(0, int(_lim))]
    env = {"ok": True, "schema": "dedup_corpus.v1", "mode": "DRY", "apply_mode": _mode, "threshold": T,
           "scoped": rep["scoped"], "counts": rep["counts"], "groups": rep["groups"],
           "legit_convert_pairs": rep["legit_convert_pairs"],
           "auto_eligible": sorted(_AUTO), "guards_fail_closed": sorted(_GUARD),
           "eligible_groups": len(sel)}
    if _allp:
        env["profiles_loaded"] = profiles_loaded
        env["profile_errors"] = profile_errors

    def _emit_env(rc_note=""):
        body = _json_dumps(env, deterministic=_deterministic_enabled(a))
        if getattr(a, "out", None):
            Path(a.out).write_text(body + "\n", encoding="utf-8")
            print(f"[tl] dedup-corpus → {a.out} ({env['mode']}, {len(rep['groups'])} nhóm)", file=sys.stderr)
        if getattr(a, "json", False):
            print(body)
            return
        _c = rep["counts"]
        print(f"== dedup-corpus {env['mode']}({_mode}) · scoped {rep['scoped']} · "
              + (" · ".join(f"{k}={_c[k]}" for k in sorted(_c)) or "0 nhóm") + f" · eligible {len(sel)} ==")
        for g in rep["groups"][:25]:
            _kp = (g.get("keep") or {}).get("name") or "∅"
            print(f"  [{g['classification']}] {str(g.get('key'))[:16]} type={g.get('type') or '?'} "
                  f"GIỮ {_kp[:40]} act={len(g.get('act') or [])}")
        if rep["legit_convert_pairs"]:
            print(f"  ℹ {len(rep['legit_convert_pairs'])} cặp gốc+convert HỢP LỆ (không trùng — ADR-2)")
        if rc_note:
            print(rc_note)

    if not _apply or str(getattr(a, "confirm", "") or "").strip().lower() != "yes":
        if _apply:
            env["confirm_required"] = "--apply --confirm yes"
        _emit_env("" if not _apply else "  → thiếu --confirm yes: mới chỉ in kế hoạch (DRY).")
        return 0
    _ok_gate, _ = _apply_gate(a, write_cols=("corpus" if _mode == "corpus-false" else None))
    if not _ok_gate:
        return 2
    run_id = _apply_journal_start("dedup-corpus", {"mode": _mode, "groups": len(sel),
                                                   "acts": sum(len(g["act"]) for g in sel)})
    results, all_ok, skipped_false = [], True, 0
    for g in sel:
        for m in g["act"]:
            did = str(m.get("drive_id") or "")
            if not did:
                continue
            if _mode == "corpus-false" and str(m.get("corpus") or "").strip().lower() != "true":
                skipped_false += 1   # đã ngoài corpus → không ghi lại (idempotent, đỡ call)
                continue
            if _mode == "corpus-false":
                _ns = argparse.Namespace(target=did, status="false", apply=True, confirm="yes", refresh=False,
                                         config=getattr(a, "config", None), profile=getattr(a, "profile", None),
                                         force_unsafe=bool(getattr(a, "force_unsafe", False)), json=False)
                rc_i = cmd_source_update_corpus(_ns)
            else:
                _ns = argparse.Namespace(target=did, apply=True, confirm="yes", refresh=False,
                                         config=getattr(a, "config", None), profile=getattr(a, "profile", None),
                                         force_unsafe=bool(getattr(a, "force_unsafe", False)), json=False)
                rc_i = cmd_source_delete(_ns)
            results.append({"drive_id": did, "classification": g["classification"], "rc": rc_i})
            all_ok = all_ok and rc_i == 0
    _journal_append(run_id, {"t": "run_end", "ok": all_ok,
                             "counts": {"applied": len(results), "skipped_already_false": skipped_false,
                                        "mode": _mode}})
    env.update({"ok": all_ok, "mode": "APPLY", "applied": results,
                "skipped_already_false": skipped_false, "journal": run_id})
    _emit_env()
    print(f"[tl] dedup-corpus APPLY({_mode}): {len(results)} act (ok={all_ok}), bỏ qua {skipped_false} dòng "
          f"đã corpus=false. Undo: theo journal TỪNG id (source-update-corpus/source-delete) — "
          f"`tl undo <journal-con>`. MANIFEST_STALE: `tl boot --refresh`.", file=sys.stderr)
    return 0 if all_ok else 2


def _sweep_report(entries: list) -> dict:
    """PURE (test offline): tổng hợp sức khoẻ corpus từ entries → dict đếm + next_actions điền sẵn. KHÔNG I/O/mạng."""
    g = _hygiene_groups(entries)
    shared_sid = _shared_source_id_groups(entries)
    goc_pollution = _goc_pollution_groups(entries)
    infra = [e for e in entries if str(e.get("corpus")).lower() == "true" and _is_infra_entry(e)]
    _rawdup = _raw_dup_of_standard_rows(entries)   # v1.29.3 (#5): bản thô trùng bản chuẩn (propose-only)
    # N4 (v1.31.1): tên phi-chuẩn offline (cùng guard corpus-audit: bỏ phụ lục/mẫu/điều ước, chỉ corpus=true)
    _name_ns_all = [e for e in entries
                    if _entry_corpus_true(e) and not _is_treaty_entry(e)
                    and not re.match(r"^(PL|Mau|Phu_luc)[_\-]", str(_entry_name(e) or ""), re.I)
                    and _name_structural_issues(_entry_name(e))]
    # S12 (v1.33.44 — log 7A: sweep báo name_nonstandard=65 gây hiểu nhầm 'corpus bẩn' — thực VBQPPL corpus=true
    # chỉ 8, còn lại là văn bản LÀM VIỆC loai='thuong' + dòng kẹt quarantine): HEADLINE = VBQPPL thật (trừ thuong/
    # quarantine — nhóm nguồn rename); phần loại trừ đếm riêng name_nonstandard_other (không nuốt, không phồng ảo).
    _name_ns = [e for e in _name_ns_all
                if str(e.get("loai") or "").strip().lower() != "thuong" and not _is_quarantine_cat(_entry_cat(e))]
    _name_ns_other = len(_name_ns_all) - len(_name_ns)
    fixable, needs, conflicts = _vbhn_year_fix_items(entries)
    _dk = ("NLM_STATUS_MISMATCH", "CORPUS_TRUE_NOT_ON_NLM", "NLM_NOTEBOOK_ID_MISSING")
    drift = {k: 0 for k in _dk}
    _cov_dk = _chunk_covered_sohieu(entries)      # r253: phủ-bằng-chunk KHÔNG tính là nợ NLM
    for e in entries:
        _ef = set(_title_flags(e, _cov_dk))
        for k in _dk:
            if k in _ef:
                drift[k] += 1
    _qcat = [e for e in entries if _is_quarantine_cat(_entry_cat(e))]
    rep = {
        "ok": True, "total": len(entries),
        "corpus": sum(1 for e in entries if str(e.get("corpus")).lower() == "true"),
        # v1.30.1 (#7): 2 THƯỚC ĐO in cạnh nhau trên CÙNG snapshot — 'corpus' (client, corpus=='true' thuần) vs
        # 'corpus_server_rule_equiv' (đúng luật GAS corpus_count mà `tl boot` in). Lệch còn lại giữa lệnh = snapshot
        # khác thời điểm (GAS đọc-cache ~600s), KHÔNG phải mất dữ liệu.
        "corpus_server_rule_equiv": _corpus_count_server_rule(entries),
        "corpus_basis": {
            "corpus": "client: corpus=='true' (mọi row_kind, kể cả loai='thuong')",
            "corpus_server_rule_equiv": "luật server GAS manifest_export.corpus_count: corpus∈{true,vbqppl} ∪ "
                                        "row_kind=overflow, trừ ref & loai='thuong' (Code.gs regIsCorpusCounted_)",
            "note": "so với `tl boot` dùng corpus_server_rule_equiv; lệch còn lại = snapshot (GAS cache ~600s) → "
                    "`tl boot --refresh` rồi `tl sweep --refresh` cùng phiên.",
        },
        "quarantine": {
            "total": len(_qcat),
            "label_variants": sum(1 for e in _qcat if _is_quarantine_label_variant(_entry_cat(e))),
            "corpus_true": sum(1 for e in _qcat if str(e.get("corpus")).lower() == "true"),
            # P1-6 (v1.31.0 — log LIVE: hygiene=4 vs reg-query=0 bất đồng): still_on_nlm nay = LIVE-status
            # (_entry_on_nlm_live — loại removed*/deleted, KHỚP định nghĩa reg-query --nlm); nlm_source_id sót
            # trên dòng đã gỡ → tách `stale_nlm_ref` (rác metadata, dọn reg_clear — không phải nguồn sống).
            "still_on_nlm": sum(1 for e in _qcat if _entry_on_nlm_live(e)),
            "stale_nlm_ref": sum(1 for e in _qcat if _entry_nlm(e) and not _entry_on_nlm_live(e))},
        # C4 v1.33.0: by_sohieu = trùng THẬT (≥2 corpus=true cùng phía); by_sohieu_raw = mọi cụm ≥2 entry cùng
        # số (gồm cặp gốc+VBHN chỉ-mục-theo-số-gốc, phụ lục tách cố ý, sidecar, quarantine — LÀNH, không sửa).
        "duplicates": {"by_sohieu": len(g["duplicates_by_sohieu_real"]),
                       "by_sohieu_raw": len(g["duplicates_by_sohieu"]),
                       # P2-4 v1.33.12: *_active = còn ≥2 dòng corpus=true — GIẢM theo tiến độ dedup (raw thì không, by design)
                       "by_sohieu_raw_active": len(g["duplicates_by_sohieu_raw_active"]),
                       "by_name_active": len(g["duplicates_by_name_active"]),
                       "by_md5": len(g["duplicates_by_md5"]),
                       "by_name": len(g["duplicates_by_name"]), "identity": len(g["duplicate_identity_groups"]),
                       "same_document": len(g["vbhn_same_document_dups"])},
        "orphans": len(g["orphans"]), "treaties": len(g.get("treaties") or []),
        "party_docs": len(g.get("party_docs") or []),   # B.7 v1.33.19: văn kiện Đảng không-số-hiệu hợp lệ
        "title_mismatch": len(g["title_mismatch"]),
        # B.5-residual v1.33.22: VBHN metadata advisory (thiếu năm tên/bare-number…) — việc của vbhn-year-fix,
        # tách khỏi headline title_mismatch để hàng rename/recat hết phồng ảo.
        "vbhn_metadata_advisory": len(g.get("vbhn_metadata_advisory") or []),
        "vbhn_metadata_advisory_rows": [_summ_entry(e) for e in (g.get("vbhn_metadata_advisory") or [])[:50]],
        # S-2 v1.33.31: OMNIBUS_NARROW một mình — advisory (đã hiện ở flags từng entry), hết đếm kép với headline.
        "omnibus_title_advisory": len(g.get("omnibus_title_advisory") or []),
        "omnibus_title_advisory_rows": [_summ_entry(e) for e in (g.get("omnibus_title_advisory") or [])[:50]],
        "loai_noncanonical": len(g["loai_noncanonical"]),
        # N4 (v1.31.1 — name_audit.py phiên rà): tên phi-chuẩn OFFLINE toàn corpus (corpus-audit chỉ chấm dòng
        # ĐÃ đọc được header → thiếu độ phủ; đây là tầng đếm rẻ dùng _name_structural_issues sẵn có).
        "name_nonstandard": len(_name_ns),
        # S12 (v1.33.44): *_other = corpus=true NHƯNG loai='thuong'/quarantine (văn bản làm việc/kẹt cách ly) —
        # KHÔNG thuộc hàng rename VBQPPL; đếm riêng để headline hết phồng ảo (ca thật 65 báo vs 8 thật).
        "name_nonstandard_other": _name_ns_other,
        "name_nonstandard_basis": "headline = corpus=true, TRỪ loai='thuong' + quarantine (VBQPPL thật cần rename); "
                                  "_other = phần trừ ra (việc của tách profile vbthuong/quarantine-fix, không phải source-rename)",
        "name_nonstandard_rows": [{"drive_id": _entry_drive_id(e), "name": _entry_name(e)[:55],
                                   "issues": _name_structural_issues(_entry_name(e))} for e in _name_ns[:25]],
        "vbhn_year": {"fixable": len(fixable), "needs_year": len(needs), "conflicts": len(conflicts)},
        "shared_source_id": len(shared_sid), "shared_source_id_groups": shared_sid[:20],
        "goc_pollution": len(goc_pollution), "goc_pollution_rows": goc_pollution[:30],
        "infra_in_corpus": len(infra), "infra_in_corpus_rows": [_dedup_lite(e) for e in infra[:20]],
        "raw_dup_of_standard": len(_rawdup), "raw_dup_of_standard_rows": _rawdup[:20],
        "nlm_drift": drift, "nlm_drift_total": sum(drift.values()),
        # C1 (v1.33.4 — log: sweep nlm_drift=0 trong khi nlm-reconcile LIVE thấy 24 dòng desync/removed):
        # sweep là OFFLINE registry-only — 0 KHÔNG có nghĩa 'NLM sạch'; phải đối soát ground-truth CLI.
        "nlm_drift_basis": "OFFLINE registry-only — 0 KHÔNG kết luận 'NLM sạch' (ca thật: sweep=0 nhưng "
                           "nlm-reconcile live 24 dòng desync/removed); đối soát LIVE: tl nlm-reconcile <notebook>",
        "raw_on_nlm": len(_raw_on_nlm_rows(entries)),
        "raw_on_nlm_rows": [{"drive_id": _entry_drive_id(e), "name": _entry_name(e)[:55],
                             "nlm_source_id": _entry_nlm(e)} for e in _raw_on_nlm_rows(entries)[:15]],
        # D (v1.33.6): mã chủ đề có CẢ nhãn trơ lẫn đủ tên (05 vs 05_Can_bo…) — phân mảnh folder/đếm.
        "cat_label_variants": len(_cat_bare_full_variants(entries)),
        "cat_label_variants_rows": _cat_bare_full_variants(entries)}
    # NEXT ACTIONS — điền sẵn lệnh tất định theo cờ phát hiện.
    nb = os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
    acts = []
    if rep["shared_source_id"]:
        acts.append(f"⚠ {rep['shared_source_id']} nlm_source_id DÙNG CHUNG ≥2 drive_id (FALSE-LINK) — sửa TRƯỚC nlm-reconcile/xóa nguồn (xóa 1 gãy link kia): map_set/reg_clear tách + re-push")
    if rep["goc_pollution"]:
        acts.append(f"🔴 {rep['goc_pollution']} VBHN registry.goc NHIỄM (tên goc_<X> ≠ goc registry) → source-map/status redirect SAI văn bản; sửa goc về suggested_goc qua `tl register` (reg_upsert), xem goc_pollution_rows")
    if rep["infra_in_corpus"]:
        acts.append(f"{rep['infra_in_corpus']} file HẠ TẦNG (.json/.enc/secrets/delta) đang corpus=true = RÁC → set corpus=false (vd tl_secrets.enc, nlm_sources_delta*.json)")
    if rep["raw_dup_of_standard"]:
        acts.append(f"⚠ {rep['raw_dup_of_standard']} bản TẢI THÔ nghi TRÙNG bản chuẩn (tên kiểu 'ND274_2025_…', sohieu không trích được, "
                    f"đốt batch ingest-missing) → soát raw_dup_of_standard_rows rồi `tl source-update-corpus <id> false --apply` (undo được)")
    if rep["raw_on_nlm"]:
        acts.append(f"🔴 {rep['raw_on_nlm']} nguồn NLM là FILE THÔ (html/docx — trái 'chỉ push GDoc'; ca 22-2023 .html): "
                    f"convert GDoc (copy_convert) → re-push → gỡ nguồn raw + reg_clear mapping (xem raw_on_nlm_rows)")
    if rep["cat_label_variants"]:
        acts.append(f"⚠ {rep['cat_label_variants']} mã chủ đề có CẢ nhãn TRƠ lẫn ĐỦ TÊN (05 vs 05_Can_bo…) → gộp bare "
                    f"về folder đủ tên qua `tl recat <id> --cat NN` (xem cat_label_variants_rows; bare hay chứa văn bản làm việc lọt corpus)")
    acts.append(f"ℹ đối soát NLM/slot bằng LIVE: `tl sweep --live-nlm --json` hoặc `tl nlm-reconcile {nb} --json` "
                f"# sweep.nlm_drift là OFFLINE-only — 0 KHÔNG nghĩa NLM sạch; registry claim chỉ là ESTIMATE, "
                f"KHÔNG dùng để chốt FULL/overflow (S-4/S-5 log rà 67: claim 546 vs vật lý 298/300)")
    if rep["vbhn_year"]["fixable"]:
        acts.append(f"tl vbhn-year-fix --with-name --apply   # {rep['vbhn_year']['fixable']} VBHN thiếu năm")
    if rep["vbhn_year"]["conflicts"]:
        acts.append(f"soát {rep['vbhn_year']['conflicts']} vbhn-year CONFLICT (dedup/phân biệt tay)")
    if rep["quarantine"]["corpus_true"] or rep["quarantine"]["still_on_nlm"] or rep["quarantine"]["stale_nlm_ref"]:
        # B3/B9 (v1.33.22 — MERGE bundle-21): stale_nlm_ref nay có fixer tất định (quarantine-fix reg_clear);
        # still_on_nlm (nguồn LIVE) vẫn xoá tay sau verify.
        acts.append(f"soát quarantine mâu thuẫn: corpus_true={rep['quarantine']['corpus_true']} "
                    f"stale_nlm_ref={rep['quarantine']['stale_nlm_ref']} still_on_nlm={rep['quarantine']['still_on_nlm']} "
                    f"→ `tl quarantine-fix --apply` (corpus-flip + nhãn + reg_clear stale-ref); ghost LIVE xoá NLM tay sau verify")
    if rep["quarantine"]["label_variants"]:
        acts.append(f"chuẩn hoá {rep['quarantine']['label_variants']} nhãn quarantine biến thể")
    # nlm_drift TÁCH theo sub-type — mỗi cái lệnh KHÁC (reconcile chỉ chữa LINKAGE, không phải toàn bộ drift):
    if drift.get("NLM_NOTEBOOK_ID_MISSING"):
        acts.append(f"tl nlm-reconcile {nb} --apply   # {drift['NLM_NOTEBOOK_ID_MISSING']} thiếu notebook_id (LINKAGE; shard khác → reconcile từng shard)")
    if drift.get("NLM_STATUS_MISMATCH"):
        acts.append(f"{drift['NLM_STATUS_MISMATCH']} NLM_STATUS_MISMATCH = nhãn status LẠ ngoài họ pushed/synced/removed* (registry hygiene, KHÔNG phải live desync) → soát/chuẩn hoá nhãn; `tl nlm-orphans {nb} --fix-mismatch` CHỈ vá ca live-desync thật (MISMATCH_LIVE)")
    if drift.get("CORPUS_TRUE_NOT_ON_NLM"):
        acts.append(f"tl ingest-missing --apply   # {drift['CORPUS_TRUE_NOT_ON_NLM']} chưa push NLM (JOB LỚN, cần slot/overflow — phần lớn CẤU TRÚC do corpus>cap 300/notebook, sẽ KHÔNG về 0)")
    # S-7 (v1.33.16 — MERGE nhánh-4): cụm ACTIVE raw/name (P2-4 v1.33.12 đo được nhưng CHƯA nối vào trigger) —
    # log rà 67: 5 raw-active + 39 name-active cần dedup mà next-action im vì chỉ xét same_doc/md5/identity.
    if (rep["duplicates"]["same_document"] or rep["duplicates"]["by_md5"] or rep["duplicates"]["identity"]
            or rep["duplicates"]["by_sohieu_raw_active"] or rep["duplicates"]["by_name_active"]):
        acts.append("tl dedup-plan --apply   # dedup toàn corpus 1 lệnh (GIỮ canonical, set dup corpus=false; "
                    "gồm cả cụm ACTIVE by_sohieu_raw_active/by_name_active)")
    if rep["loai_noncanonical"]:
        acts.append(f"tl backfill-loai --normalize --apply   # {rep['loai_noncanonical']} loai phi-chuẩn (FIELD ngoài "
                    f"enum — cần --normalize v1.30.1 vì mặc định CHỈ điền dòng RỖNG; khác LOAI_MISMATCH của "
                    f"corpus-audit vốn đọc header; 2 thước đo khác nhau, đếm lệch là bình thường)")
    if rep["name_nonstandard"]:
        # S-6 (v1.33.16 — MERGE nhánh-4): 163 tên phi-chuẩn mà hướng dẫn cũ là lệnh TỪNG CA → chạy LÔ bằng
        # corpus-audit (rows đã tự mô tả từ S-1 v1.33.15: đọc rows[].fix_command/command).
        acts.append(f"soát {rep['name_nonstandard']} tên phi-chuẩn (name_nonstandard_rows: .html/thiếu-sohieu/"
                    f"thiếu-chủ-đề) → chạy LÔ `tl corpus-audit --all --resume --limit 15 --workers 4 --json` "
                    f"(S11: Cowork 45s cần trang NHỎ — lặp CÙNG LỆNH tới rc=0), đọc "
                    f"rows[].fix_command rồi source-rename TỪNG FILE/lệnh; header-verify --fix-suggest chỉ cho ca đơn lẻ")
    rep["next_actions"] = acts
    return rep


def cmd_sweep(a) -> int:
    """COMPOSITE read-only (TẤT ĐỊNH) — 1 lệnh thay cả CHUỖI audit thường chạy: hygiene scan + cat-audit + slot-audit
    + doctor-drift + vbhn-year-fix DRY + đếm quarantine/dup. KHÔNG mutate. In JSON (--json) hoặc text + NEXT ACTIONS
    điền sẵn lệnh. Mục tiêu: chấm sức khoẻ corpus 1 phát, hết chạy 6 lệnh rời rạc."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] sweep: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    rep = _sweep_report(entries)
    drift = rep["nlm_drift"]
    acts = rep["next_actions"]
    # P0-2 (v1.33.12 — log: sweep offline 0 ≠ NLM sạch, ca thật desync 76-2026 Dược chỉ lộ khi reconcile LIVE):
    # `--live-nlm` = sweep TỰ đối soát ground-truth CLI 1 lượt (read-only, chậm hơn) — khi rà TOÀN corpus nên bật.
    if getattr(a, "live_nlm", False):
        try:
            _nb_live = os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
            _nc = _imp("nlm_cli")
            _live = _nc.source_list(_nb_live, skip_freshness=True)
            if _live.get("ok"):
                _plan = _nlm_reconcile_plan(_live.get("sources") or [], entries, _nb_live)
                _live_count = len({s.get("id") for s in _live["sources"] if s.get("id")})
                # S-4/S-5 (v1.33.16 — MERGE nhánh-4, SỬA key: plan dùng `unregistered`, bản nhánh-4 đọc
                # `unregistered_on_nlm` không tồn tại → luôn 0): phơi ĐỦ các nhóm drift + gap máy-đọc — log rà
                # 67: registry claim 546 vs vật lý 298/300, driver từng dùng claim để chốt FULL/overflow SAI.
                rep["nlm_live"] = {"notebook": _nb_live,
                                   "live_on_nlm": _live_count,
                                   "desync_real": len(_plan["desync_real"]),
                                   "already_removed": len(_plan["already_removed"]),
                                   "other_notebook": len(_plan.get("other_notebook") or []),
                                   "link_candidates": len(_plan.get("link_candidates") or []),
                                   "unregistered_on_nlm": len(_plan.get("unregistered") or []),
                                   "registry_rows_claiming_nlm": _plan["registry_on_nlm_rows"],
                                   "registry_live_gap": _plan["registry_on_nlm_rows"] - _live_count,
                                   "basis": "LIVE source_list là ground-truth slot; registry_rows_claiming_nlm "
                                            "chỉ là estimate/offline claim (gồm shard khác + đã gỡ) — KHÔNG "
                                            "dùng để chốt FULL/overflow"}
                if _plan["desync_real"]:
                    acts.insert(0, f"🔴 LIVE desync_real={len(_plan['desync_real'])} (registry pushed nhưng VẮNG NLM) "
                                   f"→ tl nlm-reconcile {_nb_live} --apply --clear-stale (nếu gỡ chủ đích) hoặc re-push")
            else:
                rep["nlm_live"] = {"ok": False, "error": str(_live.get("error") or "")[:200]}
        except Exception as _le:  # noqa: BLE001
            rep["nlm_live"] = {"ok": False, "error": str(_le)[:200]}
    # v1.30.1 (#7): kèm tuổi snapshot để người đọc biết số liệu tươi tới đâu (impure — thêm ở tầng lệnh, giữ _sweep_report PURE)
    _age = _manifest_cache_age_seconds()
    rep["snapshot_age_s"] = None if _age is None else int(_age)
    if getattr(a, "json", False) or getattr(a, "out", None):
        _emit_json_payload(rep, getattr(a, "out", None))
    else:
        # P1-7 (v1.31.0 — log LIVE: 3 con số corpus dễ đọc nhầm 'mất dữ liệu'): 1 CON SỐ HEADLINE duy nhất =
        # server-rule (khớp `tl boot`); số client + giải thích định nghĩa lùi xuống 1 dòng phụ (đầy đủ khi --verbose).
        _delta = rep["corpus"] - rep["corpus_server_rule_equiv"]
        print(f"== tl sweep · {rep['total']} entry · CORPUS = {rep['corpus_server_rule_equiv']} (server-rule, khớp `tl boot`) "
              f"· snapshot {rep['snapshot_age_s'] if rep['snapshot_age_s'] is not None else '?'}s ==")
        if _delta:
            if getattr(a, "verbose", False):
                print(f"  ℹ client corpus=true = {rep['corpus']} (Δ{_delta:+d} là ĐỊNH NGHĨA, không phải mất dữ liệu: "
                      f"server đếm thêm corpus='vbqppl'/overflow, trừ ref & loai='thuong' — corpus_basis trong --json).")
            else:
                print(f"  ℹ client corpus=true = {rep['corpus']} (Δ{_delta:+d} = khác định nghĩa — --verbose/--json để xem).")
        print(f"  quarantine: {rep['quarantine']['total']} (corpus_true={rep['quarantine']['corpus_true']} "
              f"still_on_nlm={rep['quarantine']['still_on_nlm']}[live] stale_nlm_ref={rep['quarantine']['stale_nlm_ref']} "
              f"label_variants={rep['quarantine']['label_variants']})")
        print(f"  dup: sohieu={rep['duplicates']['by_sohieu']} (raw={rep['duplicates']['by_sohieu_raw']}, "
              f"raw-active={rep['duplicates']['by_sohieu_raw_active']} — active GIẢM theo dedup, raw thì không) "
              f"md5={rep['duplicates']['by_md5']} name={rep['duplicates']['by_name']}"
              f"(active={rep['duplicates']['by_name_active']}) identity={rep['duplicates']['identity']} "
              f"same_doc={rep['duplicates']['same_document']}")
        print(f"  orphans={rep['orphans']} (tách riêng hợp-lệ-không-số-hiệu: treaties={rep['treaties']} "
              f"party_docs={rep.get('party_docs', 0)}) "
              f"title_mismatch={rep['title_mismatch']} vbhn_advisory={rep.get('vbhn_metadata_advisory', 0)} "
              f"omnibus_advisory={rep.get('omnibus_title_advisory', 0)} "
              f"loai_noncanonical={rep['loai_noncanonical']} name_nonstandard={rep['name_nonstandard']}"
              + (f" (+{rep['name_nonstandard_other']} thuong/quarantine — ngoài hàng rename)"
                 if rep.get("name_nonstandard_other") else ""))
        print(f"  vbhn_year: fixable={rep['vbhn_year']['fixable']} needs_year={rep['vbhn_year']['needs_year']} conflicts={rep['vbhn_year']['conflicts']}")
        print(f"  nlm_drift: {rep['nlm_drift_total']} (" + " ".join(f"{k}={v}" for k, v in drift.items())
              + ") [OFFLINE registry-only — live: tl nlm-reconcile / sweep --live-nlm]")
        if isinstance(rep.get("nlm_live"), dict) and "desync_real" in rep.get("nlm_live", {}):
            _nl = rep["nlm_live"]
            print(f"  nlm LIVE: on_nlm={_nl['live_on_nlm']} desync_real={_nl['desync_real']} "
                  f"already_removed={_nl['already_removed']} other_nb={_nl.get('other_notebook', 0)} "
                  f"unregistered={_nl.get('unregistered_on_nlm', 0)} "
                  f"claiming={_nl['registry_rows_claiming_nlm']} gap={_nl.get('registry_live_gap', 0)} "
                  f"(claim=estimate, KHÔNG chốt FULL/overflow bằng số này)")
        if rep["raw_on_nlm"]:
            print(f"  🔴 raw_on_nlm: {rep['raw_on_nlm']} nguồn NLM là FILE THÔ (trái 'chỉ push GDoc') → convert GDoc + re-push (raw_on_nlm_rows)")
        if rep["cat_label_variants"]:
            print(f"  ⚠ cat_label_variants: {rep['cat_label_variants']} mã có cả nhãn TRƠ lẫn ĐỦ TÊN (05 vs 05_Can_bo…) → gộp qua recat (cat_label_variants_rows)")
        if rep["shared_source_id"]:
            print(f"  🔴 shared_source_id (FALSE-LINK): {rep['shared_source_id']} — xóa 1 nguồn gãy link kia! sửa TRƯỚC reconcile")
        if rep["goc_pollution"]:
            print(f"  🔴 goc_pollution: {rep['goc_pollution']} VBHN registry.goc NHIỄM (tên goc_<X> ≠ registry.goc) → redirect SAI; sửa goc qua reg_upsert")
        if rep["infra_in_corpus"]:
            print(f"  🔴 infra_in_corpus: {rep['infra_in_corpus']} file hạ tầng (.json/.enc/secrets) corpus=true = RÁC → set corpus=false")
        if rep["raw_dup_of_standard"]:
            print(f"  ⚠ raw_dup_of_standard: {rep['raw_dup_of_standard']} bản tải thô nghi trùng bản chuẩn (soát rows → source-update-corpus false)")
        if acts:
            print("  NEXT ACTIONS:")
            for x in acts:
                print(f"    • {x}")
    return 0


def cmd_corpus_fix(a) -> int:
    """ORCHESTRATOR dọn/chỉnh lý corpus 1 lệnh: kế hoạch THEO THỨ TỰ PHỤ THUỘC + 2 tầng an toàn. DRY/report mặc định.
    `--apply --tier safe`: CHỈ chạy thao tác REVERSIBLE (infra + dedup → corpus=false); còn lại LUÔN in lệnh, người duyệt."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] corpus-fix: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    plan = _corpus_fix_plan(entries)
    if getattr(a, "apply", False):
        if getattr(a, "tier", None) != "safe":
            print(json.dumps({"ok": False, "error": "APPLY_REQUIRES_TIER_SAFE",
                              "note": "corpus-fix --apply CHỈ chạy tier=safe (reversible: infra/dedup→corpus=false). "
                                      "Các bước metadata/human_confirm/structural chạy lệnh riêng in trong plan."},
                             ensure_ascii=False, indent=2), file=sys.stderr)
            return 2
        _ok_gate, _pfv = _apply_gate(a, write_cols="corpus")   # (Pha 1) chống clobber/ghi-mù TRƯỚC khi ghi
        if not _ok_gate:
            return 2
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        g = _gas()
        run_id = _apply_journal_start("corpus-fix", {"tier": "safe"})
        _sr = _corpus_safe_reversible(entries)
        items = [{"drive_id": x, "corpus": "false"} for x in _sr["ids"]]
        _before = {x: {"corpus": "true"} for x in _sr["ids"]}   # undo = trả corpus=true
        v = _journaled_reg_write(run_id, g, items, "corpus", before_by_key=_before) if items else {"patched": 0, "verified": True}
        _journal_append(run_id, {"t": "run_end", "ok": bool(v.get("verified", True)), "counts": {"corpus_false": v.get("patched")}})
        print(json.dumps({"ok": True, "tier": "safe", "corpus_false_patched": v.get("patched"), "journal": run_id,
                          "infra": _sr["infra"], "dedup": _sr["dedup"], "total_reversible": len(items),
                          "next_human_steps": [s["id"] for s in plan["needs_human"]]}, ensure_ascii=False, indent=2))
        print("[tl] corpus-fix (safe): reversible xong. Còn lại (metadata/human) chạy lệnh trong `corpus-fix` (DRY). "
              "MANIFEST_STALE: `tl boot --refresh`.", file=sys.stderr)
        return 0
    if getattr(a, "json", False):
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(f"== tl corpus-fix · {plan['total']} entry · corpus {plan['corpus']} · {plan['step_count']} bước "
              f"(THEO THỨ TỰ) ==")
        for s in plan["steps"]:
            tag = {"safe_auto": "✅AUTO", "metadata_deterministic": "🟡META", "human_confirm": "🔴NGƯỜI", "structural": "🏗CẤU-TRÚC"}.get(s["tier"], s["tier"])
            print(f"  {s['order']:2d}. [{tag}] {s['problem']} — {s['count']}")
            print(f"       → {s['command']}")
        print("  ✅AUTO=reversible (corpus=false) → `corpus-fix --apply --tier safe`. 🟡META/🔴NGƯỜI/🏗=chạy lệnh in sẵn, duyệt tay.")
    return 0


def _consolidation_cleanup_plan(entries: list) -> dict:
    """PURE (Pha sau): 'có đồng thời VBHN + gốc/sửa đổi RỜI' → GIỮ VBHN, set THÀNH PHẦN (gốc/luật-sửa) corpus=false
    (reversible) khi VBHN phủ chúng ĐÃ VERIFY (on NLM live). Khi tìm thành phần, source-map VBHN-first vẫn trả ra VBHN.
    An toàn nhiều lớp:
      • VBHN covering PHẢI on NLM live (đã verify), corpus=true; component KHÔNG phải VBHN + đang corpus=true.
      • CORROBORATE goc (chống goc-pollution — cùng guard với source-map VBHN-first `_vbhn_goc_corroborated`): chỉ vào
        'ready' (đủ điều kiện auto corpus=false) khi tồn tại VBHN phủ ĐƯỢC CORROBORATE cho component (tên VBHN mã hoá
        base khớp/không mã hoá + chủ đề không xung khắc). Khớp goc NHƯNG không corroborate = NGHI goc-pollution → review
        (cờ GOC_POLLUTION_SUSPECT), KHÔNG auto (đề phòng ẩn văn bản mà redirect VBHN-first lại không kích hoạt).
      • Component CÒN trên NLM → review (cân nhắc gỡ nguồn tay), không auto."""
    covered: dict = {}    # component_sohieu_key -> [vbhn phủ, đã on nlm]
    for e in entries:
        if _is_vbhn_entry(e) and _entry_corpus_true(e) and _entry_on_nlm_live(e):
            for k in _goc_keys(e):
                covered.setdefault(k, []).append(e)
    ready, review = [], []
    for e in entries:
        if _is_vbhn_entry(e) or not _entry_corpus_true(e):
            continue
        sk = _sohieu_key_entry(e)
        if not sk or sk not in covered:
            continue
        vbhns = covered[sk]
        subj = _entry_subject_text(e)
        corrob = [v for v in vbhns if _vbhn_goc_corroborated(v, sk, subj)]
        show = corrob if corrob else vbhns
        row = {"drive_id": _entry_drive_id(e), "name": _entry_name(e)[:60], "sohieu": _entry_sohieu(e) or "",
               "on_nlm": _entry_on_nlm_live(e), "nlm_source_id": _entry_nlm(e) or None,
               "corroborated": bool(corrob),
               "covered_by_vbhn": [{"sohieu": _entry_sohieu(v) or _sohieu_key_entry(v), "name": _entry_name(v)[:44]} for v in show[:3]]}
        if _entry_on_nlm_live(e):
            row["reason"] = "COMPONENT_STILL_ON_NLM"; review.append(row)
        elif not corrob:
            row["reason"] = "GOC_POLLUTION_SUSPECT"; review.append(row)   # khớp goc nhưng KHÔNG corroborate → nghi nhiễm
        else:
            ready.append(row)
    return {"ready": ready, "review_on_nlm": review, "total_ready": len(ready)}


def cmd_consolidation_cleanup(a) -> int:
    """Pha sau: gộp 'cả VBHN + gốc/sửa đổi rời' về VBHN — set THÀNH PHẦN corpus=false (reversible) khi VBHN phủ ĐÃ VERIFY
    (on NLM). Khi tìm thành phần vẫn trả VBHN (source-map VBHN-first). DRY mặc định; --apply ghi reg_bulk corpus=false.
    Component CÒN trên NLM → review (gỡ nguồn tay bằng `source-update-corpus`/`shared-source-fix` nếu muốn)."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] consolidation-cleanup: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    p = _consolidation_cleanup_plan(entries)
    if getattr(a, "apply", False):
        _ok_gate, _ = _apply_gate(a, write_cols="corpus")   # (Pha 1+) precheck + journal + verified-write
        if not _ok_gate:
            return 2
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        g = _gas()
        run_id = _apply_journal_start("consolidation-cleanup", {"components": len(p["ready"])})
        items = [{"drive_id": r["drive_id"], "corpus": "false"} for r in p["ready"]]
        _before = {r["drive_id"]: {"corpus": "true"} for r in p["ready"]}
        v = _journaled_reg_write(run_id, g, items, "corpus", before_by_key=_before) if items else {"patched": 0, "verified": True}
        _invalidate_manifest_cache()
        patched = v.get("patched") or 0
        under = bool(items) and not v.get("verified")   # HỤT THẬT = có dòng miss (drive_id không khớp); patched=0 do đã corpus=false sẵn = OK
        _journal_append(run_id, {"t": "run_end", "ok": not under, "counts": {"corpus_false": patched, "missed": v.get("missed") or 0}})
        print(json.dumps({"ok": not under, "corpus_false_patched": patched, "components": len(items), "journal": run_id,
                          "review_on_nlm": len(p["review_on_nlm"]),
                          "note": "Thành phần → corpus=false (reversible; undo: `tl undo <journal>`). Còn trên NLM (review) chưa đụng. `tl boot --refresh`."},
                         ensure_ascii=False, indent=2))
        if under:
            print(f"[tl] ⚠ consolidation-cleanup: {v.get('missed') or 0} dòng KHÔNG khớp ({v.get('missed_ids')}) — `tl boot --refresh` rồi lặp lại.", file=sys.stderr)
            return 1
        return 0
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "mode": "DRY", **p}, ensure_ascii=False, indent=2))
    else:
        _nlm = [r for r in p["review_on_nlm"] if r.get("reason") == "COMPONENT_STILL_ON_NLM"]
        _poll = [r for r in p["review_on_nlm"] if r.get("reason") == "GOC_POLLUTION_SUSPECT"]
        print(f"== consolidation-cleanup DRY · {p['total_ready']} thành phần → corpus=false · {len(_nlm)} còn NLM · {len(_poll)} nghi goc-nhiễm (review) ==")
        for r in p["ready"][:25]:
            print(f"  ✗ {r['sohieu'] or '∅':18s} {r['name'][:44]} → phủ bởi VBHN {r['covered_by_vbhn'][0]['sohieu'] if r['covered_by_vbhn'] else '?'}")
        for r in _nlm[:15]:
            print(f"  🟡 CÒN NLM: {r['sohieu'] or '∅':18s} {r['name'][:40]} — gỡ nguồn tay nếu muốn")
        for r in _poll[:15]:
            print(f"  ⚠ NGHI GOC-NHIỄM: {r['sohieu'] or '∅':18s} {r['name'][:38]} → không auto (verify goc VBHN; xem `tl sweep` goc_pollution)")
        print("  → --apply: set component corpus=false (GIỮ VBHN; reversible; CHỈ nhóm ✗ corroborated). Tìm thành phần vẫn ra VBHN (source-map VBHN-first).")
    return 0


def cmd_quarantine_fix(a) -> int:
    """COMPOSITE dọn quarantine MÂU THUẪN (nhóm B): set_corpus_false (raw dup gán nhầm corpus) + normalize_label
    (nhãn biến thể→QUARANTINE_CAT) TỰ ĐỘNG; review_restore (GDoc corpus=true nghi canonical kẹt) + ghost_nlm (còn
    nguồn NLM live) chỉ BÁO (cần quyết/verify tay). DRY mặc định; --apply ghi reg_bulk 2 nhóm an toàn."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:
        print(f"[tl] quarantine-fix: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    b = _quarantine_fix_items(entries)
    if getattr(a, "apply", False):
        _ok_gate, _ = _apply_gate(a, write_cols="corpus,cat")   # reg_clear validate cols riêng (_REG_CLEARABLE_COLS)
        if not _ok_gate:
            return 2
        load_creds(getattr(a, "config", None), getattr(a, "profile", None))
        g = _gas()
        run_id = _apply_journal_start("quarantine-fix", {"corpus_false": len(b["set_corpus_false"]),
                                                         "relabel": len(b["normalize_label"]),
                                                         "clear_stale_nlm_ref": len(b["clear_stale_nlm_ref"])})
        _cf_before = {r["drive_id"]: {"corpus": "true"} for r in b["set_corpus_false"]}
        rc = _journaled_reg_write(run_id, g, [{"drive_id": r["drive_id"], "corpus": "false"} for r in b["set_corpus_false"]],
                                  "corpus", before_by_key=_cf_before) if b["set_corpus_false"] else {"patched": 0}
        rn = _journaled_reg_write(run_id, g, [{"drive_id": r["drive_id"], "cat": QUARANTINE_CAT} for r in b["normalize_label"]],
                                  "cat") if b["normalize_label"] else {"patched": 0}
        # B3/B9 (v1.33.22): ref NLM treo → reg_clear TỪNG DÒNG (KHÔNG reg_bulk giá trị rỗng — webapp bỏ qua).
        _rs_ok, _rs_fail = _quarantine_clear_stale(run_id, g, b["clear_stale_nlm_ref"])
        _invalidate_manifest_cache()
        _journal_append(run_id, {"t": "run_end", "ok": not _rs_fail,
                                 "counts": {"corpus_false": rc.get("patched"), "relabel": rn.get("patched"),
                                            "clear_stale_nlm_ref": _rs_ok}})
        print(json.dumps({"ok": True, "corpus_false_patched": rc.get("patched"), "label_normalized": rn.get("patched"),
                          "stale_nlm_ref_cleared": _rs_ok, "stale_nlm_ref_failed": _rs_fail, "journal": run_id,
                          "review_restore": len(b["review_restore"]), "ghost_nlm": len(b["ghost_nlm"]),
                          "ghost_sources": b["ghost_nlm"]}, ensure_ascii=False, indent=2))
        print(f"[tl] quarantine-fix: corpus=false {rc.get('patched')}/{len(b['set_corpus_false'])} · "
              f"nhãn chuẩn {rn.get('patched')}/{len(b['normalize_label'])} · "
              f"stale_ref_clear {_rs_ok}/{len(b['clear_stale_nlm_ref'])} · review_restore {len(b['review_restore'])} · "
              f"ghost_nlm {len(b['ghost_nlm'])} (ghost LIVE: verify rồi `nlm source delete` tay). "
              f"MANIFEST_STALE: `tl boot --refresh`.", file=sys.stderr)
        return 1 if _rs_fail else 0
    print(f"== quarantine-fix DRY · set_corpus_false {len(b['set_corpus_false'])} · normalize_label "
          f"{len(b['normalize_label'])} · stale_nlm_ref {len(b['clear_stale_nlm_ref'])} · "
          f"review_restore {len(b['review_restore'])} · ghost_nlm {len(b['ghost_nlm'])} "
          f"(--apply ghi 3 nhóm an toàn đầu; ghost_nlm xoá nguồn tay) ==")
    for r in b["clear_stale_nlm_ref"][:20]:
        print(f"  ✅ STALE_NLM_REF (reg_clear an toàn) src={r['nlm_source_id'][:16]:16s} {r['sohieu'] or '∅':18s} {r['name']} [{r['drive_id'][:14]}]")
    for r in b["review_restore"][:20]:
        print(f"  🟡 REVIEW_RESTORE (GDoc corpus=true kẹt quarantine) {r['sohieu'] or '∅':20s} {r['name']} [{r['drive_id'][:14]}]")
    for r in b["ghost_nlm"][:20]:
        print(f"  🔴 GHOST_NLM (xoá nguồn tay) src={r['nlm_source_id'][:16]:16s} {r['sohieu'] or '∅':18s} {r['name']} [{r['drive_id'][:14]}]")
    if getattr(a, "json", False):
        print(json.dumps({"ok": True, "mode": "DRY", **{k: b[k] for k in b}}, ensure_ascii=False, indent=2))
    return 0


def _corpus_audit_row(entry: dict, header_text: str) -> dict:
    """PURE, dùng CHUNG cho `header-verify --fix-suggest` (B, per-file) và `corpus-audit` (A, toàn corpus): đọc header →
    SO registry → trả danh sách ĐỀ XUẤT {type, severity, current, suggested, fix_command}. PROPOSE-ONLY (không auto — nội
    dung là phán đoán). Tái dùng _verify_header_match + _classify_doc_header + _vb_standard_doc_name + _vb_auto_cat_from_text."""
    vr = _verify_header_match(entry, header_text)
    info = _classify_doc_header(header_text, _entry_name(entry))
    checks = vr.get("checks", {})
    did = _entry_drive_id(entry)
    name = _entry_name(entry)
    reg_sh = _sohieu_key_entry(entry)
    props: list[dict] = []

    # 1) SỐ HIỆU — header có ĐÚNG 1 số hiệu rõ ≠ registry → source-rename --sohieu.
    head_shs = [s for s in (vr.get("header_sohieu") or []) if s]
    if checks.get("sohieu") is False and len(head_shs) == 1 and head_shs[0] != reg_sh:
        # A1c (v1.33.9): KHÔNG BAO GIỜ đề xuất RỚT NĂM của VBHN đã year-fix (bất biến NN-YYYY-VBHN-XXX) chỉ vì
        # header in dạng chính-thức không-năm — check sohieu đã nhận dạng không-năm là khớp, guard này chống sót.
        _m_vy2 = _VBHN_WITHYEAR_RE.fullmatch(reg_sh or "")
        _yearless2 = f"{_m_vy2.group(1)}-VBHN-{_m_vy2.group(3)}" if _m_vy2 else None
        if head_shs[0] != _yearless2:
            props.append({"type": "SOHIEU_MISMATCH", "current": reg_sh or "∅", "suggested": head_shs[0],
                          "fix_command": f"tl source-rename {did} --sohieu {head_shs[0]} --apply"})

    # VBHN số hiệu THIẾU NĂM: xử ở MISSING_YEAR TRƯỚC (đúng thứ tự phụ thuộc) — KHÔNG để NAME_TRICH_YEU dựng tên từ sohieu
    # year-less (sẽ RỚT NĂM, vi phạm bất biến). vbhn-year-fix --with-name đã đổi CẢ tên khi thêm năm.
    _vbhn_noyear = bool(_is_vbhn_entry(entry) and reg_sh and _VBHN_NOYEAR_RE.fullmatch(reg_sh))

    # 2) TÊN / TRÍCH YẾU — CHỈ khi tên hiện tại HỎNG CẤU TRÚC (UUID/đuôi file/thiếu mã loại) — tên ĐÃ chuẩn KHÔNG đụng
    # (trích yếu-từ-header quá nhiễu để đổi tên chuẩn, dễ SAI: rớt năm/nhặt cơ quan). GUARD: subject không boilerplate +
    # phải CHIA SẺ ≥1 token với tên cũ (corroborate — chống Kế toán→Văn phòng quốc hội) + tên mới hợp lệ + KHÔNG VBHN-thiếu-năm.
    # v1.35.67 (r231): KHÔNG đề xuất đổi tên cho tệp BUNDLE nhiều phần (`..._phan_3_cua_8`, `..._part02...`).
    # Header của bundle là header của tài liệu ĐẦU TIÊN trong đó, nên `_doc_subject_for_name` trích ra chủ đề
    # của MỘT phần rồi đặt cho CẢ bundle: ca thật hồ sơ Luật BHXH — `VBT_Y_kien_gop_y_Luat_BHXH_16-7_phan_6_cua_8`
    # bị đề xuất thành `Luat_Cong_ngan_hang_nha_nuoc` (mất chỉ số phần + gắn tiền tố Luat_ cho thứ không phải luật).
    _is_bundle = bool(re.search(r"(?i)(phan|part)[_\s-]*\d+[_\s-]*(cua|of|/)[_\s-]*\d+"
                                r"|__part\d+__", name or ""))
    if _name_looks_nonstandard(name) and not _vbhn_noyear and not _is_bundle:
        merged = dict(info)
        if reg_sh and not merged.get("sohieu"):
            merged["sohieu"] = _entry_sohieu(entry); merged["sohieu_key"] = reg_sh
        subj = _doc_subject_for_name(header_text, merged)
        if subj and not _subject_is_boilerplate(subj):
            merged["title"] = subj.capitalize() if subj.isupper() else subj
            suggested_name = _vb_standard_doc_name(merged, name)
            share = _token_set(subj) & _token_set(_name_tail_key(name))
            # v1.29.4 (log LIVE i2c — ca đề xuất đổi KL_→NQ_ SAI loại): KHÔNG đề xuất tên ĐỔI MÃ LOẠI so với tên
            # hiện tại khi prefix hiện tại là mã canonical — phân loại-từ-header quá nhiễu để đổi LOẠI qua rename;
            # loại lệch THẬT đã có LOAI_MISMATCH riêng (trỏ header-verify tay).
            _cur_pfx = _NAME_TYPE_PREFIX_RE.match(name or "")
            _sug_pfx = _NAME_TYPE_PREFIX_RE.match(suggested_name or "")
            # A2 v1.33.0: so theo HỌ loại — BLDS_↔Bo_luat_ là cùng họ, không phải 'đổi mã loại'.
            _pfx_changed = bool(_cur_pfx and _sug_pfx and _name_prefix_family(_cur_pfx) != _name_prefix_family(_sug_pfx))
            if (suggested_name and _name_key(suggested_name) != _name_key(name)
                    and not _name_looks_nonstandard(suggested_name) and share and not _pfx_changed):
                props.append({"type": "NAME_TRICH_YEU", "current": name[:60], "suggested": suggested_name,
                              "fix_command": f"tl source-rename {did} --name {suggested_name} --apply"})

    # 2b) P0-3 (v1.31.0): CẤU TRÚC TÊN — kiểm ĐỘC LẬP header (trước đây NAME_TRICH_YEU cần header-subject
    # chia-sẻ-token → 4 ca tên hỏng lọt lưới 0 proposals). CHỈ cờ + trỏ lệnh; KHÔNG tự dựng tên (việc của
    # NAME_TRICH_YEU/vbhn-year-fix). Bỏ qua: phụ lục/mẫu (PL_/Mau_ có quy ước riêng), điều ước quốc tế, non-corpus.
    if (_entry_corpus_true(entry) and not _vbhn_noyear
            and not any(p["type"] == "NAME_TRICH_YEU" for p in props)
            and not _is_treaty_entry(entry)
            and not re.match(r"^(PL|Mau|Phu_luc)[_\-]", name, re.I)):
        _nsi = _name_structural_issues(name)
        if _nsi:
            props.append({"type": "NAME_NONSTANDARD", "current": name[:60],
                          "suggested": "<Loai>_<sohieu>_<Chu_de> (chuẩn hoá tay)", "issues": _nsi,
                          "fix_command": f"tl header-verify --drive-id {did} --fix-suggest   # rồi source-rename theo đề xuất"})

    # 3) THIẾU NĂM (VBHN corpus) — số hiệu dạng NN-VBHN-XXX không năm → vbhn-year-fix. ⚠ lệnh BATCH (sửa MỌI VBHN thiếu năm,
    # idempotent — KHÔNG chỉ dòng này); dùng --limit nếu muốn nhỏ giọt.
    if _vbhn_noyear and _entry_corpus_true(entry):
        props.append({"type": "MISSING_YEAR", "current": reg_sh, "suggested": f"{reg_sh} + NĂM (suy từ ngày ban hành)",
                      "fix_command": "tl vbhn-year-fix --with-name --apply   # BATCH: sửa MỌI VBHN thiếu năm"})

    # 4) LOẠI — CHỈ khi header NHẬN RA 1 loại KHÁC bậc registry (xung khắc thật), KHÔNG phải chỉ THIẾU từ loại (header
    # OCR/che khuyết → info.loai rỗng → BỎ, tránh nhiễu — review chỉ ra). Trỏ header-verify (review tay, không auto).
    # v1.29.1 (log LIVE 2.5a): checks['loai'] chỉ là "header CÓ TỪ-LOẠI đúng bậc tier" — header cụt/OCR làm nó False dù
    # loại THẬT khớp → từng đề xuất current==suggested GIỐNG HỆT. Guard: chỉ fire khi loai chuẩn hoá THỰC SỰ KHÁC.
    if (checks.get("loai") is False and info.get("loai")
            and _normalize_loai(str(info.get("loai"))) != _normalize_loai(str(entry.get("loai") or ""))):
        props.append({"type": "LOAI_MISMATCH", "current": str(entry.get("loai") or "?"), "suggested": info.get("loai"),
                      "fix_command": f"tl header-verify --drive-id {did}   # kiểm loại/tên thủ công"})
    # 4b) A2 (v1.33.7 — log rà v1.33.6: BLHS 100/2015 + BLLĐ 45/2019 đăng ký loai='Luat' mà proposals=0):
    # 'Bộ luật' và 'Luật' CÙNG tier-5 nên checks['loai'] pass khi header có 'luat' → nhánh trên câm.
    # Đối chiếu RIÊNG cặp Bộ-luật↔Luật theo HEADER (ground-truth của corpus-audit; title-block đã ưu tiên
    # 'BỘ LUẬT' trước 'LUẬT' từ v1.31.2).
    if not any(p["type"] == "LOAI_MISMATCH" for p in props):
        _hdr_lo = _normalize_loai(str(info.get("loai") or ""))
        _reg_lo = _normalize_loai(str(entry.get("loai") or ""))
        if {_hdr_lo, _reg_lo} == {"Bộ luật", "Luật"}:
            props.append({"type": "LOAI_MISMATCH", "current": str(entry.get("loai") or "?"), "suggested": _hdr_lo,
                          "fix_command": f"tl header-verify --drive-id {did}   # header={_hdr_lo}; sửa loai qua "
                                         "tl register/reg_upsert (KHÔNG reg_bulk) — backfill-loai không đoán ca này"})
    # 4c) S-2h (v1.33.16 — MERGE nhánh-4, detector viết lại): khối tiêu đề IN HOA khai 'BỘ LUẬT'/'VĂN BẢN HỢP
    # NHẤT' ≠ registry → LOAI_MISMATCH (4/4b câm khi cùng tier-5 và _classify miss layout xen kẽ). GUARD kép:
    # (a) entry VBHN (tên/loai/sohieu) KHÔNG qua đây — VBHN in tiêu đề luật GỐC 'BỘ LUẬT…' (đo thật ca 21-2026
    # BLTTDS) và backfill-loai name-only đã own lớp đó; (b) chỉ tin khai báo MẠNH (Bộ luật/VBHN), 'LUẬT' trần
    # không đủ đặc hiệu để đề xuất đổi loại.
    if not any(p["type"] == "LOAI_MISMATCH" for p in props) and not _is_vbhn_entry(entry):
        _decl_lo = _declared_loai_from_header(header_text)
        _reg_lo3 = _normalize_loai(str(entry.get("loai") or ""))
        if (_decl_lo in ("Bộ luật", "Văn bản hợp nhất") and _reg_lo3
                and _decl_lo != _reg_lo3 and _reg_lo3 != "Văn bản hợp nhất"):
            props.append({"type": "LOAI_MISMATCH", "current": str(entry.get("loai") or "?"), "suggested": _decl_lo,
                          "fix_command": f"tl header-verify --drive-id {did}   # khối tiêu đề khai {_decl_lo}; "
                                         "sửa loai qua tl register/reg_upsert (KHÔNG reg_bulk)"})

    # 5) CAT — CHỈ fill-missing (cat hiện RỖNG/00), suggested là cat HỢP LỆ (≠00) + confident. KHÔNG override cat thật —
    # auto-cat-từ-header quá nhiễu để đè cat đang đúng (vd đòi chuyển Hình sự 16→23); phát hiện cat SAI = dùng `cat-audit`.
    cur_cat = re.sub(r"\D", "", str(_entry_cat(entry)))[:2]
    if cur_cat in ("", "00"):
        catp = _vb_auto_cat_from_text(header_text, name, "")
        sug_cat = re.sub(r"\D", "", str(catp.get("cat") or ""))[:2]
        if sug_cat and sug_cat != "00" and sug_cat != cur_cat and catp.get("confidence") == "high":
            props.append({"type": "CAT_MISMATCH", "current": str(_entry_cat(entry)) or "∅", "suggested": str(catp.get("cat")),
                          "fix_command": f"tl recat {did} --cat {sug_cat} --apply"})
    else:
        # 5b) P0-2 (v1.31.0) + SIẾT v1.33.0 (log rà 69/15 Luật — over-fire ~78%, BLHS→23, VBHN→46 hàng loạt):
        # cat CÓ GIÁ TRỊ chỉ bị nghi SAI khi TIÊU ĐỀ (không phải 24KB thân văn bản) suy ra cat khác VÀ qua đủ
        # cổng phủ định (VBHN/điều-ước/pin-19/cross-check alias) — xem _cat_likely_wrong_suggest. Ca thật GIỮ:
        # 143-2025 'Đầu tư' ở cat 45 → 34 (alias đồng thuận); omnibus 57-2024 → 46.
        _clw = _cat_likely_wrong_suggest(entry, header_text)
        if _clw:
            props.append(_clw)

    for p in props:
        sev, icon = _AUDIT_SEVERITY.get(p["type"], (9, "•"))
        p["severity"] = sev; p["icon"] = icon
    props.sort(key=lambda p: p["severity"])
    # S-2g (v1.33.15 — log rà 40: 5 ca header_ok=False + 0 đề xuất chỉ trả {drive_id,name} CÂM — 'biết sai mà
    # không nói sai Ở ĐÂU'): row mang LUÔN lý do lệch từ _verify_header_match → hàng need_manual_read tự giải thích.
    return _audit_row_flatten({"drive_id": did, "name": name[:60], "sohieu": _entry_sohieu(entry) or "",
                               "cat": _entry_cat(entry), "header_ok": vr.get("ok"), "proposals": props,
                               "header_checks": checks, "header_mismatches": vr.get("mismatches") or []})


def cmd_corpus_audit(a) -> int:
    """(A) ĐỌC HEADER toàn corpus → worklist SỬA XẾP HẠNG (số hiệu/tên-trích-yếu/năm/loại/cat/ngày) + LỆNH điền sẵn.
    PROPOSE-ONLY (KHÔNG --apply — chỉ đề xuất; sửa chạy qua source-rename/vbhn-year-fix/recat). DRY. Dùng chung engine
    `_corpus_audit_row` với `header-verify --fix-suggest`. --all|--full|--sohieu|--drive-id|--cat NN|--limit. --strict → rc=1 nếu có 🔴."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] corpus-audit: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    # A1 (v1.33.7 — log rà v1.33.6: `--all` cắt âm thầm ở 40, còn `--limit 600` thì cày 531 header 1 lượt ~9'
    # vượt trần Cowork): `--all --resume` = CÀY TRỌN pool theo TRANG + checkpoint — idiom nlm-install:
    # LẶP CÙNG LỆNH tới rc=0; rc=3 = PARTIAL (còn trang, KHÔNG phải lỗi). --limit = cỡ trang (mặc định 40).
    # A3 (v1.33.18 — MERGE bundle-18 + tl_changes.patch, log rà 67: 530 doc ⇒ ~13 vòng --resume tay): `--all
    # --full` = quét HẾT pool trong 1 lệnh (bỏ cap trang). LẤY NGỮ NGHĨA CỦA PATCH chứ không phải bundle:
    # --full vẫn đi qua máy CHECKPOINT (_all_resume) — chết giữa chừng ở doc #500 không mất 499 header đã đọc,
    # chạy tiếp bằng CÙNG lệnh (hoặc --all --resume) là nối; bundle-18 cho --full chạy trần không checkpoint =
    # timeout là mất trắng. Cowork trần lệnh ngắn vẫn nên dùng --all --resume trang nhỏ.
    _all_full = bool(getattr(a, "full", False) and getattr(a, "all", False)
                     and not getattr(a, "sohieu_file", None))
    _all_resume = bool(getattr(a, "all", False) and (getattr(a, "resume", False) or _all_full)
                       and not getattr(a, "sohieu_file", None))
    _page_size = 40
    if _all_resume:
        _page_size = 10 ** 9 if _all_full else int(getattr(a, "limit", None) or 40)
        a.limit, a.offset = 10 ** 9, 0     # resolver trả TRỌN pool; trừ done + cắt trang bên dưới
    targets = _resolve_headerverify_targets(a, entries)
    if not targets:
        print("[tl] corpus-audit: không có target — dùng --all / --sohieu / --sohieu-file / --drive-id / --cat NN (+--limit).", file=sys.stderr); return 2
    rows, need_read, err = [], [], []
    # B3 (v1.33.0 — log rà 69): batch --sohieu-file có CHECKPOINT resumable — trước đây timeout giữa lô ×69 là
    # mất trắng tiến độ. State keyed theo md5 NỘI DUNG file (đổi danh sách = state mới); --resume nạp lại và bỏ
    # target đã xử; chạy trọn vẹn thì tự xoá state.
    _ckpt, _ck_done = None, set()
    if getattr(a, "sohieu_file", None):
        try:
            import hashlib as _hl
            _ckpt = _cache_file("corpus_audit_ckpt_" + _hl.md5(Path(a.sohieu_file).read_bytes()).hexdigest()[:12] + ".json")
        except OSError:
            _ckpt = None
    elif _all_resume:
        _ckpt = _cache_file("corpus_audit_ckpt_all.json")   # A1 v1.33.7: trang --all dùng chung máy checkpoint
    if _ckpt is not None and (getattr(a, "resume", False) or _all_full) and _ckpt.exists():
        try:
            _st = json.loads(_ckpt.read_text(encoding="utf-8"))
            _ck_done = set(_st.get("done") or [])
            rows = list(_st.get("rows") or []); need_read = list(_st.get("need_read") or [])
            err = list(_st.get("errors") or [])
            targets = [e for e in targets if _entry_drive_id(e) not in _ck_done]
            print(f"[corpus-audit] RESUME: {len(_ck_done)} target đã xử lượt trước → còn {len(targets)}.",
                  file=sys.stderr, flush=True)
        except Exception:  # noqa: BLE001
            _ck_done = set()
    # A1: cắt TRANG sau khi trừ done — mỗi lần gọi xử tối đa _page_size target rồi checkpoint.
    _remaining_after = 0
    if _all_resume:
        _remaining_after = max(0, len(targets) - _page_size)
        targets = targets[:_page_size]

    def _ckpt_save():
        if _ckpt is not None:
            try:
                _ckpt.parent.mkdir(parents=True, exist_ok=True)   # (r181) profile-cache-dir (profile≠default / phiên mới) có thể CHƯA tồn tại → tạo trước, khỏi ghi HỤT im lặng (mất tiến độ)
                _ckpt.write_text(json.dumps({"done": sorted(_ck_done), "rows": rows, "need_read": need_read,
                                             "errors": err}, ensure_ascii=False), encoding="utf-8")
            except OSError:
                pass
    _n_t = len(targets)
    _scanned_ids, _hdr_bad = [], []      # A4/A5 (v1.33.7): phân biệt 'sạch' vs 'chưa quét'; header FAIL không câm
    # A1b (v1.33.8 — log rà v1.33.6: '531 header × ~1s = ~9 phút, cần chế độ đọc song song'): PREFETCH text
    # theo CHÙM bằng thread-pool (I/O-bound: direct-media/GAS/NLM đều là network round-trip), rồi XỬ TUẦN TỰ
    # bên dưới — toàn bộ logic streak/fast-fail/checkpoint/heartbeat GIỮ NGUYÊN thứ tự. --workers 1 (mặc định)
    # = hành vi cũ 100%; circuit-breaker auth-dead (v1.33.0) dùng chung cờ process nên worker sau tự skip.
    _workers = max(1, int(getattr(a, "workers", None) or 1))
    _prefetched: dict = {}
    if _workers > 1:
        _to_read = [(e2, _entry_drive_id(e2)) for e2 in targets if not _entry_raw_no_gdoc(e2)]
        if _to_read:
            print(f"[corpus-audit] prefetch SONG SONG {_workers} luồng × {len(_to_read)} target…",
                  file=sys.stderr, flush=True)

            def _pf_read(_pair):
                _e2, _did2 = _pair
                try:
                    _t = _read_doc_text(_did2, getattr(a, "config", None))
                except Exception:  # noqa: BLE001
                    _t = ""
                if not (_t or "").strip():
                    _t = _read_doc_text_via_nlm(_e2)
                return _did2, _t

            import concurrent.futures as _cf
            with _cf.ThreadPoolExecutor(max_workers=_workers) as _px:
                for _did2, _t in _px.map(_pf_read, _to_read):
                    _prefetched[_did2] = _t
    # P1 (v1.32.1 — log rà 119): read-path Drive có thể CHẾT TOÀN BỘ (gws cred revoke + exporttext thiếu scope
    # script.external_request) — trước lặp 531 target × ~22s toàn 'header rỗng' (~3.2h all-error). FAST-FAIL:
    # ≥3 LỖI ĐỌC LIÊN TIẾP (đã thử cả đường NLM) → ABORT kèm remediation, không cày hết pool.
    _read_fail_streak = 0
    for _ci, e in enumerate(targets, 1):
        did = _entry_drive_id(e); nm = _entry_name(e)
        # v1.29.1 (log LIVE 2.5b): HEARTBEAT per-item — batch lớn từng "treo 0 output" (đọc header per-file có thể
        # chậm/nghẽn webapp) → stream tiến độ để thấy đang ở item nào, không tưởng treo.
        print(f"[corpus-audit] {_ci}/{_n_t} {nm[:48]}", file=sys.stderr, flush=True)
        if _entry_raw_no_gdoc(e):
            # A3 (v1.33.7 — log: 'luat-dau-thau-…-d1.html' KHÔNG bị corpus-audit flag trong khi tên chỉ-thiếu-sohieu
            # lại bị): nhánh raw trước đây skip LUÔN cả check TÊN — mà NAME structural là check OFFLINE, không cần
            # header. Ca nonstandard nặng nhất (slug .html) chính là raw → phải chạy tại đây.
            if (_entry_corpus_true(e) and not _is_treaty_entry(e)
                    and not re.match(r"^(PL|Mau|Phu_luc)[_\-]", nm, re.I)):
                _nsi_raw = _name_structural_issues(nm)
                if _nsi_raw:
                    rows.append(_audit_row_flatten(
                        {"drive_id": did, "name": nm[:60], "sohieu": _entry_sohieu(e) or "",
                         "cat": _entry_cat(e), "header_ok": None,
                         "proposals": [{"type": "NAME_NONSTANDARD", "current": nm[:60],
                                        "suggested": "<Loai>_<sohieu>_<Chu_de> (chuẩn hoá tay)",
                                        "issues": _nsi_raw, "severity": 2, "icon": "🟠",
                                        "fix_command": f"tl header-verify --drive-id {did} --fix-suggest   # rồi source-rename theo đề xuất"}]}))
            need_read.append({"drive_id": did, "name": nm[:55]})
            _ck_done.add(did); _ckpt_save()
            continue   # .docx/.pdf/scan → Claude đọc header (ingest-analyze --text-file)
        if did in _prefetched:                  # A1b v1.33.8: worker đã thử CẢ Drive lẫn NLM — không đọc lại
            txt = _prefetched[did]
        else:
            try:
                txt = _read_doc_text(did, getattr(a, "config", None))
            except Exception:  # noqa: BLE001
                txt = ""
            if not (txt or "").strip():
                txt = _read_doc_text_via_nlm(e)     # P1 v1.32.1: Drive chết → thử NLM (295 nguồn live vẫn đọc được)
        if not (txt or "").strip():
            err.append({"drive_id": did, "name": nm[:55], "error": "header rỗng (Drive + NLM đều không đọc được)"})
            _ck_done.add(did); _ckpt_save()
            _read_fail_streak += 1
            if _read_fail_streak >= 3:
                print(json.dumps({"ok": False, "error": "READ_BACKEND_DOWN", "scanned": _ci, "errors": err,
                                  "note": "3 lỗi đọc LIÊN TIẾP (cả Drive lẫn NLM) → read-path chết, ABORT thay vì cày "
                                          "hết pool all-error. Chẩn đoán: `tl gws-ping` (canary cred) / `tl doctor`. "
                                          "Khắc phục: `gws auth login` → `tl secrets-set --gws`; webapp exporttext cần "
                                          "scope script.external_request nếu muốn fallback GAS đọc được."
                                          + (" Tiến độ đã CHECKPOINT — chạy lại CÙNG lệnh + --resume để tiếp."
                                             if _ckpt is not None else "")},
                                 ensure_ascii=False, indent=2), file=sys.stderr)
                return 2
            continue
        _read_fail_streak = 0
        ar = _corpus_audit_row(e, txt)
        _scanned_ids.append(did)                      # A4: đã ĐỌC header thật (kể cả khi 0 đề xuất)
        if ar["proposals"]:
            rows.append(ar)
        elif ar.get("header_ok") is False:
            # A5 (v1.33.7 — log: 64-2006/71-2020 header_ok=False mà proposals=0 → biến mất câm): header verify
            # FAIL không đề xuất được gì máy-tin-được → hàng đợi RÀ TAY riêng, không nuốt.
            # S-2g (v1.33.15): kèm LÝ DO lệch (mismatches/checks) — người rà tay khỏi chạy lại header-verify.
            _hdr_bad.append({"drive_id": did, "name": nm[:55],
                             "mismatches": ar.get("header_mismatches") or [],
                             "checks": ar.get("header_checks") or {}})
        _ck_done.add(did); _ckpt_save()
    _partial = bool(_all_resume and _remaining_after > 0)
    if _ckpt is not None and _ckpt.exists() and not _partial:
        try:
            _ckpt.unlink()   # batch chạy TRỌN VẸN → dọn checkpoint (state chỉ sống qua lần chạy dở)
        except OSError:
            pass
    flat = [(r, p) for r in rows for p in r["proposals"]]
    flat.sort(key=lambda rp: rp[1]["severity"])
    by_type: dict = {}
    for _r, p in flat:
        by_type[p["type"]] = by_type.get(p["type"], 0) + 1
    has_red = any(p["type"] in ("SOHIEU_MISMATCH", "LOAI_MISMATCH") for _r, p in flat)
    # v1.29.6 (P1): minh bạch phạm vi quét + phân trang; đối chiếu sweep (2 detector đo THỨ KHÁC NHAU — không phải lỗi):
    # sweep.title_mismatch/loai_noncanonical = heuristic THEO TÊN/enum-FIELD (rẻ, rộng, nhiều nghi vấn);
    # corpus-audit = đọc HEADER thật + guard chặt (đề xuất ÍT nhưng bằng chứng mạnh). Đếm lệch là BÌNH THƯỜNG.
    _pool_total = getattr(a, "_targets_pool_total", None) or len(targets)
    _off0 = max(0, int(getattr(a, "offset", None) or 0))
    # A2 (v1.33.18 — MERGE bundle-18, log rà 67: `partial=true` nhưng `next_offset=None` MÂU THUẪN — driver
    # phân trang theo next_offset DỪNG sau lô 1 → audit 40/530 âm thầm): chế độ resume tiến độ đi bằng
    # CHECKPOINT chứ không offset, nên next_offset khi partial = PROGRESS MARKER (số drive_id đã checkpoint)
    # + marker tường minh pagination_mode/resume_required/resume_command — driver hết đường hiểu nhầm.
    _resume_next = len(_ck_done) if (_all_resume and _partial) else None
    _next_off = _resume_next if _resume_next is not None else (
        None if _all_resume else ((_off0 + len(targets)) if (_off0 + len(targets)) < _pool_total else None))
    _clean_ids = [d for d in _scanned_ids
                  if d not in {r["drive_id"] for r in rows} and d not in {h["drive_id"] for h in _hdr_bad}]
    if getattr(a, "json", False) or getattr(a, "out", None):   # S-4 (v1.33.34): --out tự bật JSON
        _audit_payload = ({"ok": True, "mode": "DRY_PROPOSE_ONLY", "scanned": len(targets),
                          "pool_total": _pool_total, "offset": _off0, "next_offset": _next_off,
                          "pagination_mode": ("full_checkpoint" if _all_full
                                              else ("checkpoint_resume" if _all_resume else "offset")),
                          # A1 (v1.33.7) + A2 (v1.33.18): PARTIAL máy-đọc — driver LẶP CÙNG LỆNH tới rc=0;
                          # next_offset ở chế độ checkpoint chỉ là PROGRESS, KHÔNG phải tham số --offset.
                          "partial": _partial, "remaining": _remaining_after,
                          "resume_required": bool(_partial),
                          # S11 (v1.33.44): resume_command GIỮ NGUYÊN cỡ trang người dùng đã chọn (--limit) —
                          # trước đây bỏ --limit → lần lặp sau rơi về trang 40 mặc định, Cowork 45s lại timeout.
                          "resume_command": (f"tl corpus-audit --all --resume --limit {_page_size} --json --workers 4"
                                             if _partial else None),
                          # A4 (v1.33.7): 'sạch' ≠ 'chưa quét' — ids đã ĐỌC header thật + ids sạch tường minh.
                          "scanned_ids": _scanned_ids, "scanned_clean": len(_clean_ids), "clean_ids": _clean_ids,
                          # A5 (v1.33.7): header verify FAIL nhưng 0 đề xuất → rà tay, không nuốt câm.
                          "header_mismatch_no_proposal": _hdr_bad,
                          "coverage_complete": (_next_off is None) and not _partial,
                          "note_vs_sweep": "corpus-audit đọc HEADER thật (guard chặt, ít đề xuất, bằng chứng mạnh); "
                                           "sweep.title_mismatch/loai_noncanonical = heuristic tên/enum-field (rộng, "
                                           "nghi vấn) — 2 thước đo KHÁC NHAU, đếm lệch là bình thường. "
                                           "CAT_LIKELY_WRONG (v1.33.0) CHỈ suy từ TIÊU ĐỀ (tên + khối tiêu đề + "
                                           "title_vn) + cross-check alias pháp điển (đồng bộ cat-audit) — thân văn "
                                           "bản KHÔNG còn là bằng chứng cat.",
                          "rows_with_proposals": len(rows), "proposal_count": len(flat),
                          "by_type": by_type, "need_manual_read": need_read, "errors": err,
                          # S-1 (v1.33.15): flatten Ở ĐÂY nữa (idempotent) — row nạp lại từ CHECKPOINT đời cũ
                          # (trước khi có mirror) cũng ra schema mới, không tuỳ lúc-có-lúc-không.
                          "rows": [_audit_row_flatten(r) for r in rows]})
        _emit_json_payload(_audit_payload, getattr(a, "out", None))   # S-4 (v1.33.34): atomic --out
    else:
        summ = " · ".join(f"{k}={v}" for k, v in sorted(by_type.items(), key=lambda kv: _AUDIT_SEVERITY.get(kv[0], (9,))[0]))
        print(f"== corpus-audit (DRY, propose-only): {len(targets)}/{_pool_total} quét · {len(rows)} dòng có đề xuất · {len(flat)} đề xuất ==")
        if _next_off is not None:
            print(f"   ⚠ CHƯA PHỦ HẾT ({_pool_total - _off0 - len(targets)} còn lại) — trang kế: --offset {_next_off}")
        print(f"   {summ or 'không có đề xuất'}   ({len(need_read)} cần đọc tay · {len(err)} không đọc được)")
        for r, p in flat[:40]:
            print(f"  {p['icon']} {p['type']:18s} {r['name'][:44]}")
            print(f"        {p['current']}  →  {p['suggested']}")
            print(f"        $ {p['fix_command']}")
        if len(flat) > 40:
            print(f"   … còn {len(flat) - 40} đề xuất (dùng --json để xem hết / --cat NN thu hẹp).")
        for r in need_read[:12]:
            print(f"  ⚠ CẦN ĐỌC TAY  {r['name'][:44]} — Claude đọc header → `tl ingest-analyze --text-file`")
        for h in _hdr_bad[:12]:
            _why = (h.get("mismatches") or ["?"])[0]
            print(f"  ⚠ HEADER LỆCH (0 đề xuất máy) {h['name'][:44]} — {_why[:70]} → `tl header-verify --drive-id {h['drive_id']} --fix-suggest`")
        if _partial:
            print(f"  ⏭ PARTIAL: còn {_remaining_after} target — LẶP CÙNG LỆNH (--all --resume) tới rc=0 "
                  f"(tiến độ: {_next_off}/{_pool_total} đã checkpoint).")
        print("  → PROPOSE-ONLY: chạy lệnh `$` để sửa (mỗi lệnh DRY riêng, thêm --apply). Nội dung/trích yếu = người duyệt.")
    if _partial:
        return 3   # A1: PARTIAL — còn trang (mirror nlm-install --resume), KHÔNG phải lỗi
    return 1 if (getattr(a, "strict", False) and has_red) else 0


def _review_queue_report(entries: list[dict], limit: int | None = None) -> dict:
    """B (v1.33.3 — 3 log rà liên tiếp cùng kết luận: '~26 Luật cần lượt web LƯỢT-2 mới finalize' nhưng phải GOM
    TAY từ 66-111 lần source-map rời): MỘT LỆNH offline gom HÀNG ĐỢI rà soát cho toàn bộ Luật/Bộ luật corpus —
    source-map từng số hiệu → nhóm theo việc-cần-làm (web LƯỢT-2 ưu tiên HIGH_VELOCITY / relation-backfill /
    PAUSE / sạch) + qt5_queries sẵn-dán cho phiên Chrome. KHÔNG thay thế bước verify official (QT-5 web +
    `vbhn-verify --official-required` vẫn chạy tay) — chỉ diệt công đoạn gom-và-phân-loại. PURE/offline."""
    laws, seen, no_sh, vbhn_base = [], set(), 0, 0
    for e in entries:
        if not _entry_corpus_true(e) or _entry_quarantined(e):
            continue
        _lo = _normalize_loai(str(e.get("loai") or ""))
        _lawish = _lo in ("Luật", "Bộ luật") or bool(re.match(r"^(Luat|Bo_luat|BL[A-Z])", _entry_name(e) or ""))
        if _is_vbhn_entry(e):
            # VBHN rà theo luật gốc của nó, không phải mục hàng đợi riêng. v1.33.5 (log: 'corpus có 69 Luật
            # nhưng laws_scanned=68' — phiên rà mất thời gian truy 1 dòng 'rớt'): VBHN ĐỘI LỐT Luật (loai='Luật'
            # bẩn — ca 115-VBHN) lọt bộ lọc reg-query của người vận hành → đếm TƯỜNG MINH cho kế toán khớp.
            if _lawish:
                vbhn_base += 1
            continue
        if not _lawish:
            continue
        k = _sohieu_key_entry(e)
        if not k:
            no_sh += 1                     # dòng Luật thiếu sohieu (E3 log) — đếm LOUD, không nuốt câm
            continue
        if k in seen:
            continue
        seen.add(k); laws.append(e)
    if limit:
        laws = laws[:int(limit)]
    web, rel, rel_low, rel_suppressed, pause, clean, other = [], [], [], [], [], [], []
    neg_n = 0                       # S-1: đếm mọi row bị relation-check phủ định (kể cả row rơi bucket web)
    for e in laws:
        r = _source_map_one(_entry_sohieu(e) or _sohieu_key_entry(e), entries)
        flags = set(r.get("flags") or _warning_codes(r.get("warnings") or []))
        # A1 (v1.33.4): rel = CÓ VIỆC THẬT — verdict phải khác OK VÀ không cờ hoá-giải (COVERED/CONFIRMED/
        # CONSOLIDATED/OMNIBUS); trước đây 19-2012 (OK+COVERED) và 90-2025 (OK+CONFIRMED) thành backfill khống.
        _rel_cands_raw = (r.get("unlinked_amendment_candidates") or r.get("amendment_candidates") or [])
        _in_rel_flags = (r.get("verdict") != "OK" and bool(flags & _RQ_REL_FLAGS)
                         and not (flags & _RQ_REL_SUPPRESS))
        # P2-2 (v1.33.12 — log: 3 Luật vào relation_backfill toàn ứng viên LOW-CONF mà `relation-check --base
        # --subject` trả OK/missing_links=[] cả 3): bucket HÀNH ĐỘNG chỉ nhận ứng viên MẠNH (linked/strong/
        # confidence≠low — cùng ngưỡng escalate v1.29.6); low-conf-only → nhóm INFO riêng, không phồng hàng đợi.
        _in_rel = _in_rel_flags and _rq_rel_strong(_rel_cands_raw)
        _in_rel_low = _in_rel_flags and not _in_rel
        # S-1 (v1.33.31 + MERGE bundle-12 v1.33.32 — log rà LIVE v1.33.28: review-queue gắn 124/125-2025 cờ
        # UNLINKED/LOW_CONFIDENCE → ops-plan đẩy P0, nhưng relation-check trả OK/candidates=[] — 2 engine BẤT
        # ĐỒNG): cross-validate NGAY TẠI ĐÂY bằng `_rq_relation_probe` (cùng engine, cùng entries) cho MỌI row
        # có cờ rel (strong LẪN low-conf — phạm vi ta, rộng hơn bundle chỉ-low-conf). Phủ định → cờ
        # RELATION_CHECK_NEGATED + rơi bucket riêng `relation_probe_suppressed` (bundle) — KHÔNG còn trong hàng
        # đợi hành động; audit còn tín hiệu (fixture 06/2022 subject-only) giữ nguyên.
        _rel_probe = _rq_relation_probe(entries, e) if (_in_rel or _in_rel_low) else None
        _rel_negated = bool(_rel_probe and _rel_probe.get("suppressed"))
        if _rel_negated:
            flags.add("RELATION_CHECK_NEGATED")
            _in_rel = _in_rel_low = False
            neg_n += 1
        _in_web = bool(flags & _RQ_WEB_FLAGS)
        _is_pause = r.get("verdict") == "PAUSE_AND_ASK_USER"
        _buckets = [b for b, c in (("pause", _is_pause), ("relation_backfill", _in_rel),
                                   ("web_round2", _in_web),
                                   ("relation_low_confidence", _in_rel_low),
                                   ("relation_probe_suppressed", _rel_negated)) if c] or \
                   (["clean"] if r.get("verdict") == "OK" else ["review_other"])
        # B.1 (v1.33.19 — log rà v1.33.18: 4/4 row review_other có flags=[] dù flags_all đầy — cờ REVIEW
        # của nhóm này [TITLE_OR_REGISTRY_WARN/AMENDS_OTHER_VBHN/…] không thuộc các nhóm-việc nên bị lọc
        # sạch → driver duyệt đồng nhất .flags thấy 'REVIEW không lý do'): lọc theo nhóm-việc TRƯỚC, nhưng
        # lọc RỖNG thì mirror toàn bộ flags_all — .flags không bao giờ câm khi có cờ thật.
        row = {"sohieu": _sohieu_key_entry(e), "name": _entry_name(e)[:55], "verdict": r.get("verdict"),
               "flags": (sorted(flags & (_RQ_WEB_FLAGS | _RQ_REL_FLAGS | _RQ_REL_SUPPRESS
                                         | {"PAUSE_AND_ASK_USER", "RELATION_CHECK_NEGATED"}))
                         or sorted(flags)),
               # P2-1 (v1.33.12 — log: review_other verdict=REVIEW mà flags=[] → REVIEW không nêu LÝ DO):
               # flags_all = TOÀN BỘ cờ source-map (không lọc nhóm) — mọi REVIEW đều tự giải thích được.
               "flags_all": sorted(flags),
               "priority_high_velocity": "VBHN_HIGH_AMENDMENT_VELOCITY" in flags,
               "buckets": _buckets,
               "qt5_queries": (r.get("qt5_queries") or [])[:4]}
        if _rel_probe:
            # bundle-12: payload probe đầy đủ (verdict/flags/counts/note) đi kèm row — driver thấy NGAY vì sao
            # phủ định/giữ, khỏi chạy lại relation-check tay; đi theo row cả khi row rơi bucket web.
            row["relation_probe"] = _rel_probe
        _cands = [f"{c.get('sohieu') or c.get('sohieu_key') or '?'}|{str(c.get('name') or '')[:38]}"
                  f"|{c.get('confidence', 'low')}" for c in _rel_cands_raw[:3]]
        # A2 (v1.33.4) + P2-2: bucket CHÍNH loại trừ lẫn nhau (pause > rel > web > rel_low > clean/other) →
        # counts CỘNG ĐÚNG; việc kép vẫn đủ qua `buckets`.
        if _is_pause:
            pause.append(row)
        elif _in_rel:
            # C (v1.33.6): kèm TOP-3 ứng viên (số hiệu|tên|confidence) từ chính payload source-map.
            rel.append(dict(row, candidates=_cands,
                            fix_command=f"tl relation-check --base {_sohieu_key_entry(e)} --json   "
                                        "# duyệt rồi backfill goc/sua_doi (hỏi user trước khi ghi)"))
        elif _in_web:
            web.append(row)
        elif _in_rel_low:
            rel_low.append(dict(row, candidates=_cands,
                                fix_command=f"tl relation-check --base {_sohieu_key_entry(e)} --json   "
                                            "# INFO: ứng viên đều low-conf — phủ định nhanh bằng relation-check trước khi tin"))
        elif _rel_negated:
            rel_suppressed.append(dict(row, candidates=_cands,
                                       fix_command=f"tl relation-check --base {_sohieu_key_entry(e)} --json   "
                                                   "# ĐÃ PHỦ ĐỊNH (S-1 probe): không missing_links/subject_only/"
                                                   "footnote-thiếu — KHÔNG cần backfill; chỉ chạy lại nếu có dữ liệu mới"))
        elif r.get("verdict") == "OK":
            clean.append(row)
        else:
            row["reason"] = ", ".join(sorted(flags)) or "verdict REVIEW không kèm cờ — soi source-map --json"
            # MERGE AUDIT 07/2026 (v1.33.13): review_reason dạng LIST máy-đọc (patch kia dùng key này).
            row["review_reason"] = sorted(flags) or [str(r.get("verdict") or "REVIEW")]
            other.append(row)   # REVIEW không rơi nhóm nào — flags_all/reason tự giải thích (P2-1)
    web.sort(key=lambda x: (not x["priority_high_velocity"], x["sohieu"]))
    return {"ok": True, "schema": "review_queue.v1",   # v1.33.7: driver kiểm marker trước khi tin payload (log: 1 lần nhận nhầm dump reg-query.v2 — không tái hiện)
            "laws_scanned": len(laws), "skipped_no_sohieu": no_sh,
            "skipped_vbhn_as_base": vbhn_base,   # v1.33.5: VBHN đội lốt loai='Luật' — rà theo luật gốc, kế toán khớp
            "web_round2": web, "web_round2_count": len(web),
            "web_priority_count": sum(1 for x in web if x["priority_high_velocity"]),
            "relation_backfill": rel, "relation_low_confidence": rel_low,
            "relation_probe_suppressed": rel_suppressed, "pause": pause,
            # S-1: số row bị relation-check phủ định (cờ RELATION_CHECK_NEGATED trên row) — ≥ len(bucket
            # relation_probe_suppressed) vì đếm cả row negated nhưng rơi bucket web. Driver/ops-plan loại các
            # ca này khỏi hàng đợi hành động thay vì chạy relation-check tay từng số.
            "relation_negated_count": neg_n,
            "clean_count": len(clean),
            "review_other": other,
            # A2: counts LOẠI TRỪ lẫn nhau — tổng LUÔN bằng laws_scanned (đối soát máy được).
            "counts": {"pause": len(pause), "relation_backfill": len(rel), "web_round2": len(web),
                       "relation_low_confidence": len(rel_low),
                       "relation_probe_suppressed": len(rel_suppressed),
                       "clean": len(clean), "review_other": len(other)},
            "note": "OFFLINE gom việc từ source-map. Bucket CHÍNH loại trừ nhau (counts cộng về laws_scanned); "
                    "việc kép xem trường `buckets` từng dòng. Chốt VBHN MỚI NHẤT vẫn PHẢI lượt-2 web (Chrome, "
                    "official-first, số VBHN tăng dần) + `tl vbhn-verify --official-required`; "
                    "relation-backfill phải hỏi user trước khi ghi registry."}


def _ops_plan_add(actions: list, priority: str, aid: str, title: str, command: str = "", count: int | None = None,
                  confirm_required: bool = False, mode: str = "dry", reason: str = "", note: str = "",
                  sample: list | None = None) -> None:
    """PURE helper for ops-plan. Keep rows compact and machine-readable."""
    row = {"priority": priority, "id": aid, "title": title, "mode": mode,
           "confirm_required": bool(confirm_required)}
    if count is not None:
        row["count"] = int(count)
    if command:
        row["command"] = command
    if reason:
        row["reason"] = reason
    if note:
        row["note"] = note
    if sample:
        row["sample"] = sample[:10]
    actions.append(row)


def _ops_plan_report(entries: list[dict], config_path: str | None = None, profile: str | None = None,
                     include_review: bool = True, include_sweep: bool = True) -> dict:
    """v1.33.27: one machine-readable action plan for the recurring run-log.

    It does NOT mutate. It turns the repeating A/B/C/D/E observations (pin registryDocId, nlm-reconcile, web QT-5,
    low-confidence relation-check, dedup, name audit, loai normalize, slot preflight) into one prioritized queue so the
    operator no longer has to parse a long prose log and manually derive commands.
    """
    cfg_path, cfg = _read_config_record(config_path)
    prof_name = profile or (cfg.get("defaultProfile") if isinstance(cfg, dict) else None) or os.environ.get("TL_PROFILE") or DEFAULT_PROFILE
    prof = (_profiles_from_config(cfg).get(prof_name) if isinstance(cfg, dict) else {}) or {}
    reg_id = os.environ.get("TL_REGISTRY_DOC_ID") or prof.get("registryDocId") or (cfg.get("registryDocId") if isinstance(cfg, dict) else "") or ""
    nb = os.environ.get("TL_NOTEBOOK_ID") or prof.get("notebookId") or NLM_BASE_NOTEBOOK
    actions: list[dict] = []
    if not reg_id:
        _ops_plan_add(actions, "P0", "pin_registry_doc_id", "Pin registryDocId Sheet thật vào config",
                      "tl config-pin-registry <SHEET_ID> --profile-name " + str(prof_name),
                      confirm_required=True, mode="config", reason="registryDocId rỗng → auto-discover mỗi call, rủi ro bắt nhầm Sheet trùng tên")
    elif reg_id == _LEGACY_REGISTRY_DOC_ID:
        _ops_plan_add(actions, "P0", "fix_legacy_registry_doc_id", "Sửa registryDocId đang trỏ Doc legacy 1mATG",
                      "tl config-pin-registry <SHEET_ID> --profile-name " + str(prof_name),
                      confirm_required=True, mode="config", reason="Doc legacy không phải Sheet registry; có thể gây count=0 ảo")
    review = _review_queue_report(entries) if include_review else {}
    sweep = _sweep_report(entries) if include_sweep else {}
    web_high = [x for x in (review.get("web_round2") or []) if x.get("priority_high_velocity")]
    web_all = review.get("web_round2") or []
    if web_high:
        _ops_plan_add(actions, "P0", "web_round2_high_velocity", "Web lượt-2 cho luật HIGH_VELOCITY trước",
                      "tl review-queue --json --out /tmp/review_queue.json  # lấy qt5_queries rồi Chrome official-first → tl vbhn-verify --official-required",
                      count=len(web_high), confirm_required=True, mode="manual_web",
                      reason="VBHN số hiệu tăng theo mỗi lần hợp nhất; không được chốt ở bản đầu tìm thấy",
                      sample=[f"{x.get('sohieu')}|{x.get('name')}" for x in web_high[:10]])
    web_normal = [x for x in web_all if not x.get("priority_high_velocity")]
    if web_normal:
        _ops_plan_add(actions, "P1", "web_round2_remaining", "Web lượt-2 cho các luật còn lại cần chốt VBHN",
                      "tl review-queue --json --out /tmp/review_queue.json",
                      count=len(web_normal), confirm_required=True, mode="manual_web",
                      reason="NO_VERIFIED_VBHN_IN_CORPUS/QT5_WEB_REQUIRED/VBHN_CANDIDATE_UNVERIFIED_LATEST")
    # S-1 (v1.33.31 + MERGE bundle-12 v1.33.32 — log rà v1.33.28: 124/125-2025 vào P0 dù relation-check trả OK):
    # ba tầng thay vì gộp hết vào P0 — P0 CHỈ ứng viên MẠNH chưa phủ định (bundle); low-conf còn tín hiệu →
    # P2 probe READ-ONLY (bundle — LOW_CONF là INFO, không phải việc P0); ca ĐÃ phủ định → P3 info audit-trail
    # (ta — bundle drop hẳn khỏi plan, mất dấu vết vì sao biến mất).
    rel = [x for x in (review.get("relation_backfill") or [])
           if "RELATION_CHECK_NEGATED" not in (x.get("flags_all") or [])]   # phòng-vệ kép; demote đã chuyển bucket
    if rel:
        _ops_plan_add(actions, "P0", "relation_check_before_backfill", "Xác minh ứng viên sửa đổi MẠNH trước khi backfill goc/sua_doi",
                      "tl relation-check --base <SOHIEU> --json  # chỉ --apply sau khi người dùng duyệt",
                      count=len(rel), confirm_required=True, mode="review_then_apply",
                      reason="UNLINKED_AMENDMENT_CANDIDATE mạnh (linked/strong) không được tự ghi registry",
                      sample=[f"{x.get('sohieu')}|{x.get('name')}" for x in rel[:10]])
    rel_low = review.get("relation_low_confidence") or []
    if rel_low:
        _ops_plan_add(actions, "P2", "relation_low_confidence_probe", "Soi lại ứng viên sửa đổi LOW_CONF còn tín hiệu sau probe",
                      "tl relation-check --base <SOHIEU> --json  # read-only; chỉ nâng cấp hàng đợi khi có missing_links",
                      count=len(rel_low), confirm_required=False, mode="read_only_probe",
                      reason="LOW_CONF là INFO — probe relation-check đã lọc, phần còn lại vẫn còn subject_only/footnote cần soi",
                      sample=[f"{x.get('sohieu')}|{x.get('name')}" for x in rel_low[:10]])
    rel_neg = review.get("relation_probe_suppressed") or []
    neg_total = int(review.get("relation_negated_count") or len(rel_neg))
    if neg_total:
        _ops_plan_add(actions, "P3", "relation_candidates_negated",
                      "Ứng viên sửa đổi ĐÃ bị relation-check phủ định — KHÔNG cần backfill",
                      count=neg_total, confirm_required=False, mode="info",
                      reason="review-queue probe qua _relation_audit: không missing_links/subject_only/footnote-thiếu — không đẩy P0 giả",
                      sample=[f"{x.get('sohieu')}|{x.get('name')}" for x in rel_neg[:10]])
    drift_total = int(sweep.get("nlm_drift_total") or 0) if isinstance(sweep, dict) else 0
    if drift_total:
        _ops_plan_add(actions, "P1", "nlm_reconcile_live", "Đối soát LIVE registry↔NLM trước khi kết luận slot/desync",
                      f"tl nlm-reconcile {nb} --json --out /tmp/nlm_reconcile.json",
                      count=drift_total, confirm_required=False, mode="read_live",
                      reason="sweep nlm_drift là offline; registry_claim_nlm chỉ là estimate",
                      note="Chỉ thêm --apply/--clear-stale sau khi đọc desync_real/link_candidates.")
    dups = (sweep.get("duplicates") or {}) if isinstance(sweep, dict) else {}
    dup_active = int(dups.get("by_sohieu_raw_active") or 0)
    if dup_active or int(dups.get("identity") or 0) or int(dups.get("by_md5") or 0):
        _ops_plan_add(actions, "P1", "dedup_active", "Dọn cụm trùng lặp active/raw/md5/identity",
                      "tl dedup-plan --apply  # xem dry-run trước nếu chưa chắc canonical",
                      count=dup_active or int(dups.get("identity") or 0), confirm_required=True,
                      mode="apply_reversible", reason="giữ canonical, set bản dup corpus=false")
    name_ns = int((sweep or {}).get("name_nonstandard") or 0) if isinstance(sweep, dict) else 0
    if name_ns:
        # S11 (v1.33.44 — log 7A: lệnh --all --full gợi ý ở đây KHÔNG chạy nổi trong Cowork 45s — 489 header,
        # mới tới 20/40 đã bị cắt): gợi ý dạng PHÂN TRANG NHỎ + checkpoint (lặp CÙNG LỆNH tới rc=0; rc=3=PARTIAL
        # là bình thường). --full chỉ dành cho shell không trần thời gian (local Code).
        _ops_plan_add(actions, "P1", "name_nonstandard_batch", "Chuẩn hóa tên phi chuẩn theo lô",
                      "tl corpus-audit --all --resume --limit 15 --workers 4 --json --out /tmp/corpus_audit_page.json"
                      "  # Cowork 45s: lặp CÙNG LỆNH tới rc=0 (rc=3=PARTIAL còn trang); local không trần → --all --full",
                      count=name_ns, confirm_required=True, mode="review_then_apply",
                      reason="thiếu số hiệu/chủ đề/.html; cần đọc header thật trước khi rename")
    loai_nc = int((sweep or {}).get("loai_noncanonical") or 0) if isinstance(sweep, dict) else 0
    if loai_nc:
        _ops_plan_add(actions, "P1", "loai_noncanonical", "Chuẩn hóa loai phi canonical",
                      "tl backfill-loai --normalize --apply", count=loai_nc,
                      confirm_required=True, mode="apply", reason="field loai ngoài enum")
    quar = (sweep.get("quarantine") or {}) if isinstance(sweep, dict) else {}
    q_stale = int(quar.get("stale_nlm_ref") or 0)
    q_live = int(quar.get("still_on_nlm") or 0)
    if q_stale:
        _ops_plan_add(actions, "P2", "quarantine_stale_ref", "Clear stale NLM refs trong quarantine",
                      "tl quarantine-fix --apply", count=q_stale, confirm_required=True,
                      mode="apply_reversible", reason="quarantine đã removed/stale nhưng còn nlm_source_id/nlm_notebook_id")
    if q_live:
        _ops_plan_add(actions, "P2", "quarantine_still_on_nlm", "Xác minh rồi gỡ nguồn quarantine còn LIVE trên NLM",
                      "tl quarantine-fix --json --out /tmp/quarantine_fix.json  # đọc ghost_nlm rồi xoá NLM thủ công nếu đúng",
                      count=q_live, confirm_required=True, mode="manual_live_delete",
                      reason="không tự source delete vì có thể xoá nhầm nguồn đang dùng")
    _ops_plan_add(actions, "P2", "slot_preflight", "Kế toán slot NLM bằng nguồn LIVE trước mọi lần push",
                  f"tl counts --live-nlm --notebook-id {nb} --json --out /tmp/counts_live.json",
                  confirm_required=False, mode="read_live", reason="notebook nền có thể gần 300; registry_claim_nlm không phải ground truth")
    _ops_plan_add(actions, "P3", "cowork_bootstrap_guard", "Dùng checklist Cowork thay vì đọc file mount trực tiếp",
                  "tl cowork-plan --json --out /tmp/cowork_plan.json",
                  confirm_required=False, mode="read_only", reason="mount có thể cắt cụt; gws cần MUSL; nlm-install phải --resume")
    rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    actions.sort(key=lambda x: (rank.get(x.get("priority"), 9), x.get("id", "")))
    return {"ok": True, "schema": "ops_plan.v1", "profile": prof_name, "config_path": cfg_path,
            "registryDocId_pinned": bool(reg_id and reg_id != _LEGACY_REGISTRY_DOC_ID),
            "notebook": nb, "review_counts": review.get("counts") or {},
            "sweep_summary": {"name_nonstandard": name_ns, "loai_noncanonical": loai_nc,
                              "nlm_drift_total": drift_total, "quarantine": quar, "duplicates": dups},
            "actions": actions,
            "note": "READ-ONLY plan. Các dòng confirm_required=true chỉ sinh lệnh/queue; không tự ghi registry/Drive/NLM."}


def cmd_ops_plan(a) -> int:
    """Read-only prioritized plan after sweep/review-queue; avoids re-parsing long run logs."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] ops-plan: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    rep = _ops_plan_report(entries, getattr(a, "config", None), getattr(a, "profile", None))
    if getattr(a, "json", False) or getattr(a, "out", None):
        _emit_json_payload(rep, getattr(a, "out", None)); return 0
    print(f"== tl ops-plan · profile={rep['profile']} · actions={len(rep['actions'])} ==")
    print(f"  registryDocId_pinned={rep['registryDocId_pinned']} · notebook={rep['notebook']}")
    for x in rep["actions"]:
        cnt = f" [{x.get('count')}]" if x.get("count") is not None else ""
        mark = "⚠ duyệt" if x.get("confirm_required") else "read"
        print(f"  {x['priority']} {x['id']}{cnt} — {x['title']} ({mark})")
        if x.get("command"):
            print(f"      $ {x['command']}")
    print("  → --json/--out để driver lấy full sample/reason; lệnh này không ghi gì.")
    return 0


def cmd_review_queue(a) -> int:
    """B (v1.33.3): `tl review-queue` — 1 lệnh thay vòng 66×source-map + gom tay: hàng đợi việc theo nhóm."""
    apply_profile_offline(getattr(a, "config", None), getattr(a, "profile", None))
    try:
        entries = _manifest_entries(refresh=getattr(a, "refresh", False))
    except Exception as e:  # noqa: BLE001
        print(f"[tl] review-queue: cần `tl boot` trước ({e}).", file=sys.stderr); return 2
    rep = _review_queue_report(entries, getattr(a, "limit", None))
    if getattr(a, "json", False) or getattr(a, "out", None):
        _emit_json_payload(rep, getattr(a, "out", None))
        return 0
    print(f"== review-queue · {rep['laws_scanned']} Luật · web LƯỢT-2: {rep['web_round2_count']} "
          f"(ưu tiên HIGH_VELOCITY: {rep['web_priority_count']}) · relation-backfill: {len(rep['relation_backfill'])} "
          f"· PAUSE: {len(rep['pause'])} · sạch: {rep['clean_count']}"
          + (f" · rel-LOW-CONF(info): {len(rep['relation_low_confidence'])}" if rep.get("relation_low_confidence") else "")
          + (f" · rel-ĐÃ-PHỦ-ĐỊNH: {rep['relation_negated_count']} (S-1 cross-check, bỏ khỏi hàng đợi)"
             if rep.get("relation_negated_count") else "")
          + (f" · REVIEW-khác: {len(rep['review_other'])}" if rep["review_other"] else "")
          + (f" · VBHN-rà-theo-gốc: {rep['skipped_vbhn_as_base']}" if rep.get("skipped_vbhn_as_base") else "")
          + (f" · ⚠ {rep['skipped_no_sohieu']} dòng Luật THIẾU sohieu (sửa registry)" if rep["skipped_no_sohieu"] else "")
          + " ==   (bucket loại trừ nhau — cộng đủ về tổng; việc kép xem `buckets`)")
    for x in rep["web_round2"][:40]:
        _pri = "★" if x["priority_high_velocity"] else " "
        print(f"  {_pri} {x['sohieu']:<18s} {x['name'][:44]}")
        if x["qt5_queries"]:
            print(f"      QT-5: {x['qt5_queries'][0]}")
    if len(rep["web_round2"]) > 40:
        print(f"   … còn {len(rep['web_round2']) - 40} (dùng --json xem hết).")
    for x in rep["relation_backfill"][:12]:
        _dual = " (+web lượt-2)" if "web_round2" in (x.get("buckets") or []) else ""
        print(f"  🔗 {x['sohieu']:<18s} {x['name'][:40]}{_dual}")
        for _c in (x.get("candidates") or [])[:3]:
            print(f"      ↳ ứng viên: {_c}")
        print(f"      $ {x['fix_command']}")
    if rep["pause"]:
        print(f"  ⏸ PAUSE: {', '.join(x['sohieu'] for x in rep['pause'][:10])}")
    print("  → web LƯỢT-2 (Chrome official-first) chốt VBHN mới nhất; ★ = HIGH_VELOCITY làm trước. --json để lấy đủ qt5_queries.")
    return 0

# ── I11 (v1.34.18): leftover-sweep từ tl.py (affinity-tốt-nhất) ──


def _is_quarantine_cat(cat: str) -> bool:
    """A1: nhận diện cat cách ly/loại bỏ (MỌI biến thể: code 'QUARANTINE', folder `_ZZZ_QUARANTINE_taluat`) →
    KHÔNG cho thắng canonical + audit hội tụ bất kể nhãn."""
    c = _strip_accents(str(cat or "")).lower()
    return ("quarantine" in c) or ("zzz" in c)

def _is_quarantine_label_variant(cat: str) -> bool:
    """A2: dòng ĐÃ quarantine nhưng nhãn KHÁC chuẩn QUARANTINE_CAT (vd code 'QUARANTINE' trơ) → nên chuẩn hoá."""
    c = str(cat or "").strip()
    return _is_quarantine_cat(c) and c != QUARANTINE_CAT

def _reconcile_clusters(entries: list[dict]) -> list[dict]:
    """Gộp cụm registry theo khóa an toàn HOẶC md5.

    VBHN không gom theo số hiệu trần vì VPQH có thể tái sử dụng cùng số ở năm/chủ đề khác nhau.
    Đây là lớp bù cho vb_status vốn dedup theo số hiệu và bỏ lọt orphan `sohieu=''`."""
    entries = [e for e in entries if _entry_row_kind(e) != "ref" and not _entry_is_own_thuong(e)]
    n = len(entries)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[ry] = rx
    for key_fn in (lambda e: _dedupe_key_entry(e), _entry_md5):
        buckets: dict[str, list[int]] = {}
        for i, e in enumerate(entries):
            k = key_fn(e)
            if k:
                buckets.setdefault(k, []).append(i)
        for idxs in buckets.values():
            for j in idxs[1:]:
                union(idxs[0], j)
    groups: dict[int, list[dict]] = {}
    for i, e in enumerate(entries):
        groups.setdefault(find(i), []).append(e)
    clusters = []
    for group in groups.values():
        # Cụm đáng quan tâm: có hơn 1 dòng, hoặc có orphan/root/số hiệu rỗng/tên thô.
        # Nhưng tuyệt đối KHÔNG suy luận số hiệu/quarantine từ tài liệu làm việc kiểu Mẫu_/PL_:
        # đây là số thứ tự biểu mẫu/phụ lục, không phải số hiệu VBQPPL.
        if all(_name_is_template_or_appendix(_entry_name(e)) for e in group):
            continue
        def rawish(e):
            return (not _name_is_template_or_appendix(_entry_name(e))) and bool(re.search(r"(^|[/_ -])\d{2,4}[_-]\d{4}[_-]", _entry_name(e)))
        def orphanish(e):
            return (not _name_is_template_or_appendix(_entry_name(e))) and ((not _entry_sohieu(e)) or _bad_cat(_entry_cat(e)) or (rawish(e) and not _entry_nlm(e) and not _is_source_sidecar(e, group)))
        # v1.34.38 (#4 log phiên Chỉ thị): CHUNK tách cố ý (<base>__partNN — profile-ingest-chunks) dùng chung
        # sohieu văn bản gốc BY DESIGN (liên kết qua goc) → 9 chunk Đề án CĐS từng bị gom thành
        # duplicate_identity_groups + gợi nhãn quarantine GIẢ (dedup-plan không mắc — chỉ hygiene scan). Chunk
        # KHÔNG tính vào ngưỡng flag; cụm chỉ-toàn-chunk (+tối đa 1 bản gốc lành) bỏ qua.
        non_chunk = [e for e in group if not _is_chunk_part_name(_entry_name(e))]
        flagged = len(non_chunk) > 1 or any(orphanish(e) for e in non_chunk)
        if not flagged:
            continue
        # Canonical = điểm cao nhất, nhưng ưu tiên có số hiệu + cat không root.
        ordered = sorted(group, key=_entry_score, reverse=True)
        canonical = ordered[0] if ordered else None

        # 2026-06: chỉ đề xuất QUARANTINE bản THỰC SỰ trùng văn bản với canonical (cùng chữ ký chủ đề,
        # hoặc một bên là tên thô/coded). Khác-cơ-quan (TT-BNV vs TT-BYT) hay phụ-lục-vs-chính (cùng số hiệu,
        # chủ đề khác) → GIỮ cả hai (cụm vẫn hiện để rà tay, nhưng không tự xếp quarantine).
        def _cluster_same_doc(e):
            if not _entry_drive_id(e) or _is_source_sidecar(e, group, canonical):
                return False
            cs = _subject_sig(_entry_name(canonical)) if canonical else ""
            es = _subject_sig(_entry_name(e))
            return (not es) or (not cs) or (es == cs) or (es in cs) or (cs in es)
        quarantine = [e for e in ordered[1:] if _cluster_same_doc(e)]
        # Nếu cụm chỉ có 1 orphan không canonical rõ, vẫn đưa vào candidates để rà tay/quarantine.
        if len(group) == 1 and orphanish(group[0]):
            canonical = None
            quarantine = [group[0]] if _entry_drive_id(group[0]) else []
        key = _dedupe_key_entry(canonical or group[0]) or _sohieu_key_entry(canonical or group[0]) or _name_key(_entry_name(canonical or group[0]))
        clusters.append({"key": key, "canonical": canonical, "entries": group, "quarantine": quarantine,
                         "sidecars": [e for e in group if _is_source_sidecar(e, group, canonical)]})
    clusters.sort(key=lambda c: (0 if c.get("canonical") else 1, c.get("key") or ""))
    return clusters

def _cluster_matches(c: dict, q: str) -> bool:
    if not q:
        return True
    for e in c.get("entries") or []:
        if _entry_query_match_safe_for_hygiene(q, e):
            return True
    return False

def _select_hygiene_clusters(clusters: list[dict], q: str) -> tuple[list[dict], list[dict]]:
    """Chọn cụm cho plan/apply.

    Cụm thiếu canonical chỉ được báo ở `skipped_clusters`, không đưa vào tập có thể apply.
    Như vậy consumer JSON không còn gặp object apply với `canonical: null`.
    """
    raw = [c for c in clusters if _cluster_matches(c, q)]
    selected = [c for c in raw if c.get("canonical")]
    skipped = []
    for c in raw:
        if c.get("canonical"):
            continue
        cc = dict(c)
        cc["skip_reason"] = "MISSING_CANONICAL_REVIEW_ONLY"
        skipped.append(cc)
    return selected, skipped

def _is_chunk_part_name(nm: str) -> bool:
    """v1.34.38 (#4): tên chunk tách cố ý theo quy ước profile-ingest-chunks (`<base>__partNN`) — các dòng này
    chung sohieu/goc văn bản mẹ BY DESIGN, không bao giờ là 'bản trùng'. PURE, test offline."""
    return bool(re.search(r"__part\d+", str(nm or ""), re.I))


def _sohieu_dup_group_real(group: list[dict]) -> bool:
    """C4 (v1.33.0 — log rà 15 Luật: sweep by_sohieu=93 'trùng' nhưng chỉ 4 cụm có ≥2 bản corpus=true và CẢ 4 là
    tách Phụ lục/Final CỐ Ý; 49 cụm còn lại là cặp gốc+VBHN/quarantine LÀNH — headline 93 = báo động giả, trái
    doctrine 'không gom VBHN theo số hiệu trần' v1.17.9/15): cụm trùng THẬT = ≥2 bản corpus=true CÙNG PHÍA
    (≥2 VBHN hoặc ≥2 non-VBHN) sau khi loại sidecar/quarantine/template/phụ-lục. Cặp gốc+VBHN cùng số (row VBHN
    chỉ mục theo số bản gốc) là quan hệ HỢP LỆ, không phải trùng."""
    core = []
    for e in group:
        if not _entry_corpus_true(e) or _entry_quarantined(e):
            continue
        nm = _entry_name(e)
        if _name_is_template_or_appendix(nm) or _is_source_sidecar(e, group):
            continue
        if "phuluc" in re.sub(r"[\s_-]", "", _ascii_lower(nm)):
            continue                       # phụ lục tách riêng cố ý (PhuLuc/Phu_luc/phu-luc — cả dạng nén)
        if _is_chunk_part_name(nm):
            continue                       # v1.34.38 #4: chunk __partNN chung sohieu gốc = thiết kế, không phải trùng
        core.append(e)
    if len(core) < 2:
        return False
    n_vbhn = sum(1 for e in core if _is_vbhn_entry(e))
    return n_vbhn >= 2 or (len(core) - n_vbhn) >= 2

def _print_reconcile(clusters: list[dict]) -> None:
    print(f"== tl reconcile — cụm vấn đề: {len(clusters)} | ứng viên QUARANTINE: {sum(len(c['quarantine']) for c in clusters)} ==\n")
    for c in clusters:
        canon = c.get("canonical")
        print(f"▸ cụm '{c.get('key') or '∅'}' ({len(c.get('entries') or [])} bản)")
        if canon:
            s = _summ_entry(canon)
            print(f"    GIỮ: {s['name'][:70]} | cat={s['cat']} | sohieu={s['sohieu'] or '∅'} | id={s['drive_id']}")
        else:
            print("    ⚠ KHÔNG có canonical rõ — rà tay trước khi move.")
        for e in c.get("quarantine") or []:
            s = _summ_entry(e)
            print(f"    → QUARANTINE? {s['name'][:70]} | cat={s['cat'] or '(root)'} | sohieu={s['sohieu'] or '∅'} | id={s['drive_id']}")
    print("\n[tl] DRY-RUN — KHÔNG trash. Dùng hygiene plan/reconcile --apply --confirm yes sau khi duyệt.")

def _apply_quarantine(entries: list[dict], to_cat: str = "QUARANTINE") -> list[dict]:
    g = _gas(); results = []
    dest = to_cat or "QUARANTINE"
    for e in entries:
        did = _entry_drive_id(e)
        if did:
            results.append({"drive_id": did, "name": _entry_name(e), "to_cat": dest, "move": g.get("move", fileId=did, cat=dest)})
    return results

def _resolve_headerverify_targets(a, entries: list[dict]) -> list[dict]:
    """G2: target cho header-verify. --drive-id(1) / --sohieu(canonical) / --cat NN(corpus) / --all(mọi corpus).
    KHÁC confirm: KHÔNG lọc 'chưa-confirm' (audit lại CẢ bản đã confirm để bắt DRIFT). Batch giới hạn --limit."""
    did = getattr(a, "drive_id", None)
    if did:
        return [e for e in entries if _entry_drive_id(e) == did]
    shf = getattr(a, "sohieu_file", None)
    if shf:
        # B3 (v1.33.0 — log rà 69: vòng `corpus-audit --sohieu X` ×69 PROCESS RỜI = 69 lần boot + retry gws
        # per-doc, dễ vượt timeout shell): cả lô trong 1 PROCESS. Mỗi dòng 1 số hiệu, '#' comment; resolve
        # canonical như --sohieu, dedup theo drive_id; dòng không resolve được báo LOUD (không nuốt câm).
        try:
            _lines = Path(shf).read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as _ex:
            print(f"[targets] --sohieu-file không đọc được: {_ex}", file=sys.stderr)
            return []
        out, seen = [], set()
        for _ln in _lines:
            q = _ln.split("#", 1)[0].strip()
            if not q:
                continue
            canon, _hits = _canonical_for_query(q, refresh=False)
            if canon is None:
                print(f"[targets] ⚠ --sohieu-file: không resolve được '{q}' — bỏ qua (kiểm chính tả/`tl locate`).",
                      file=sys.stderr)
                continue
            _cd = _entry_drive_id(canon)
            if _cd and _cd not in seen:
                seen.add(_cd); out.append(canon)
        try:
            a._targets_pool_total = len(out)
        except Exception:  # noqa: BLE001
            pass
        # A6 (v1.33.2 — log rà 111: --limit bị BỎ QUA IM LẶNG ở nhánh --sohieu-file): mặc định (không --limit)
        # = CẢ LÔ (đúng thiết kế 1-process + checkpoint --resume); truyền --limit/--offset → cắt LOUD như --all.
        _off = max(0, int(getattr(a, "offset", None) or 0))
        _lim = getattr(a, "limit", None)
        if _off or _lim:
            _end = min(_off + _lim, len(out)) if _lim else len(out)
            print(f"[targets] ⚠ CẮT BATCH --sohieu-file: {_off}..{_end}/{len(out)}"
                  + (f" — trang kế: --offset {_end}." if _end < len(out) else ".")
                  + " (Bỏ --limit/--offset để chạy CẢ LÔ + --resume.)", file=sys.stderr, flush=True)
            out = out[_off:_end]
        return out
    sh = getattr(a, "sohieu", None)
    if sh:
        canon, _hits = _canonical_for_query(sh, refresh=getattr(a, "refresh", False))
        return [canon] if canon else []
    cat = getattr(a, "cat", None)
    if cat or getattr(a, "all", False):
        cc = re.sub(r"\D", "", str(cat))[:2] if cat else ""
        pool = [e for e in entries if _entry_drive_id(e) and str(e.get("corpus") or "").lower() != "false"
                and not _entry_quarantined(e) and (not cc or re.sub(r"\D", "", str(_entry_cat(e)))[:2] == cc)]
        # v1.29.4 (log LIVE i1): --offset PHÂN TRANG — trước đây mỗi lần gọi quét lại TỪ ĐẦU nên limit lớn (cat 45,
        # limit 30-40) chạy quá dài → client-timeout giết = "treo im lặng". Nay: chạy lô nhỏ + --offset tiếp trang.
        _off = max(0, int(getattr(a, "offset", None) or 0))
        # A6 v1.33.2: corpus-audit --limit nay default=None (phân biệt explicit cho --sohieu-file) → fallback 40
        # ở đây giữ NGUYÊN hành vi --all/--cat cũ (header-verify vẫn truyền default 20 tường minh của nó).
        _lim = getattr(a, "limit", None) or 40
        # v1.29.6 (log 118 Luật — P1: `--all` bị cap ÂM THẦM ở limit mặc định → scanned=40/515, 0 proposal → tưởng
        # corpus SẠCH giả). KHÔNG bỏ cap (515 lần đọc-header = ~25' sẽ lại client-timeout như i1) — nhưng phải LOUD.
        if len(pool) > _off + _lim:
            print(f"[targets] ⚠ CẮT BATCH: quét {_off}..{min(_off + _lim, len(pool))}/{len(pool)} target "
                  f"(limit={_lim}). CHƯA PHỦ HẾT — trang kế: --offset {_off + _lim} --limit {_lim}. "
                  f"KHÔNG kết luận 'corpus sạch' khi chưa quét đủ.", file=sys.stderr, flush=True)
        try:
            a._targets_pool_total = len(pool)     # cho caller (corpus-audit) in pool_total/next_offset vào JSON
        except Exception:
            pass
        return pool[_off: _off + _lim]
    return []

def _emit_json_payload(obj, out_path: str | None = None) -> None:
    """Emit JSON consistently; --out writes atomically so Cowork scripts can parse a file instead of long stdout/heredoc."""
    txt = _json_dumps(obj)   # v1.33.56 (review regression/F4): tôn trọng TL_DETERMINISTIC/--deterministic (mặc định OFF → output y cũ)
    if out_path:
        target = Path(out_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        _fd, _tmp = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp", dir=str(target.parent))
        with os.fdopen(_fd, "w", encoding="utf-8", errors="replace", newline="\n") as _f:   # v1.33.56 (F7)
            _f.write(txt + "\n")
        os.replace(_tmp, str(target))
        print(str(target))
    else:
        print(txt)

def _hieuluc_from_header_text(text: str, today: str | None = None, infer_from_date: bool = False) -> tuple[str, str]:
    """Bóc trạng thái hiệu lực từ header/text đã export. Mặc định chỉ tin nhãn trạng thái rõ; date-only cần opt-in."""
    import datetime as _dt
    today = today or _dt.date.today().isoformat()
    head = unicodedata.normalize("NFC", text or "")
    head = "\n".join(head.splitlines()[:160])
    plain = _strip_accents(head).lower()
    status = ""
    if re.search(r"\b(khong\s+con\s+hieu\s+luc|het\s+hieu\s+luc|ngung\s+hieu\s+luc|da\s+het\s+hieu\s+luc)\b", plain):
        status = "Hết hiệu lực"
    elif re.search(r"\b(chua\s+co\s+hieu\s+luc|chua\s+hieu\s+luc|chua\s+den\s+hieu\s+luc)\b", plain):
        status = "Chưa có hiệu lực"
    elif re.search(r"\b(con\s+hieu\s+luc|dang\s+co\s+hieu\s+luc)\b", plain):
        status = "Còn hiệu lực"
    iso = _date_from_effect_match(_HL_DATE_RE.search(head)) or _date_from_effect_match(_HL_DATE_VN_RE.search(head))
    if not iso:
        body_dates = resolve_body_effective_dates(head, today=today)
        iso = (body_dates[0].get("hieu_luc") if body_dates else None)
    if status:
        ds = _hieuluc_date_display(iso)
        return (f"{status}; hiệu lực từ {ds}" if ds else status), ""
    if infer_from_date and iso:
        ds = _hieuluc_date_display(iso)
        status = "Chưa có hiệu lực" if iso > today else "Còn hiệu lực"
        return f"{status}; hiệu lực từ {ds}", ""
    return "", "NO_EFFECTIVE_STATUS"

def _read_doc_text_via_nlm(entry: dict) -> str:
    """P1 (v1.32.1 — log rà 119: gws cred revoke + webapp exporttext thiếu scope script.external_request →
    KHÔNG còn đường đọc Drive nào sống, corpus-audit 6/6 'header rỗng'): đường đọc DỰ PHÒNG qua NLM CLI
    (nlm-content vẫn CHẠY — 295 nguồn live). Text = bản đã nạp NLM (vẫn verbatim nguồn) — đủ cho header/audit;
    KHÔNG thay thế extract chính-văn khi cần byte-exact. Entry cần nlm_source_id live."""
    sid = str(entry.get("nlm_source_id") or "").strip()
    if not sid or not _entry_on_nlm_live(entry):
        return ""
    try:
        nc = _imp("nlm_cli")
        r = nc.source_content(sid)
        txt = str(r.get("text") or ((r.get("data") or {}) if isinstance(r.get("data"), dict) else {}).get("content") or "")
        return _sanitize_export_text(_strip_font_runs(txt))
    except Exception:
        return ""

def _goc_pollution_groups(entries: list) -> list:
    """PURE (§1.1 log rà 108 lần): VBHN có TÊN mã hoá base (token goc_<X>) NHƯNG registry.goc KHÔNG chứa X = goc NHIỄM.
    Ca thật: VBHN_22 'Bảo vệ sức khỏe nhân dân' tên goc_21-LCT-HDNN8 nhưng registry.goc=113-2025 (Dân số) → source-map
    redirect Dân số SANG VBHN Bảo vệ sức khỏe + webapp vb_status superseded_by sai. Trả [{drive_id,name,sohieu,
    registry_goc, name_goc_base, suggested_goc}] để SỬA registry.goc qua reg_upsert (KHÔNG reg_bulk — goc là quan hệ)."""
    out = []
    for e in entries:
        if not _is_vbhn_entry(e):
            continue
        nb = _name_goc_base_key(_entry_name(e))
        if nb and nb not in _goc_keys(e):
            out.append({"drive_id": _entry_drive_id(e), "name": _entry_name(e)[:60],
                        "sohieu": _entry_sohieu(e) or "", "registry_goc": _entry_goc(e),
                        "name_goc_base": nb, "suggested_goc": nb})
    return out

def _is_infra_entry(e: dict) -> bool:
    """File HẠ TẦNG (KHÔNG phải văn bản) lẫn vào corpus=true = RÁC: .json/.enc + tên nlm_sources/manifest/registry/
    secrets/_delta/reg_query. BẢO VỆ văn bản thật (GDoc/PDF/Word) → KHÔNG false-positive (vd tl_secrets.enc,
    nlm_sources_delta_2026-06-11.json bị đếm corpus)."""
    mime = str(e.get("mimeType") or e.get("mime") or "").lower()
    nm = _strip_accents(str(_entry_name(e) or "")).lower()
    if any(t in mime for t in ("vnd.google-apps.document", "pdf", "wordprocessing", "msword")):
        return False
    if "spreadsheet" in mime or mime.endswith("/json") or nm.endswith(".json") or nm.endswith(".enc"):
        return True
    return any(t in nm for t in ("nlm_sources", "manifest", "registry", "reg_query", "secrets", "_delta"))

def _dedup_lite(e: dict) -> dict:
    return {"drive_id": _entry_drive_id(e), "sohieu": _entry_sohieu(e) or "", "name": _entry_name(e)[:50],
            "corpus": str(e.get("corpus")).lower() == "true", "on_nlm": _entry_on_nlm_live(e),
            "nlm_source_id": _entry_nlm(e) or ""}

def _dedup_plan(entries: list) -> dict:
    """PURE: kế hoạch DEDUP tất định, tái dùng canonical-picker của `_hygiene_groups` (reconcile_clusters dùng
    `_cluster_same_doc` = CÙNG văn bản theo subject-sig, AN TOÀN). Mỗi cụm: GIỮ canonical, quarantine các bản dup.
    BẤT BIẾN AN TOÀN: (1) không quarantine chính canonical; (2) không quarantine drive_id LÀ canonical của cụm khác;
    (3) mỗi drive_id chỉ vào 1 lần. ready=cụm có canonical rõ; review=cụm thiếu canonical (quyết tay)."""
    g = _hygiene_groups(entries)
    canon_ids, seen = set(), set()
    ready, review = [], []
    for c in g["reconcile_clusters"]:
        # gộp quarantine (same-doc dup) + sidecars (.docx/.pdf cạnh GDoc canonical = dup định dạng) — cả 2 đều là bản dư.
        _qd, _q = {}, []
        for e in (c.get("quarantine") or []) + (c.get("sidecars") or []):
            did = _entry_drive_id(e)
            if did and did not in _qd:
                _qd[did] = e; _q.append(e)
        q = _q
        if not q:
            continue
        can = c.get("canonical")
        if not can:
            review.append({"key": c.get("key"), "dups": [_dedup_lite(e) for e in q]})
            continue
        cid = _entry_drive_id(can)
        canon_ids.add(cid)
        dups = [e for e in q if _entry_drive_id(e) != cid and _entry_drive_id(e) not in seen]
        for e in dups:
            seen.add(_entry_drive_id(e))
        if dups:
            ready.append({"key": c.get("key"), "canonical": _dedup_lite(can), "quarantine": [_dedup_lite(e) for e in dups]})
    # BẤT BIẾN (2): loại khỏi quarantine mọi drive_id là canonical của 1 cụm khác
    for it in ready:
        it["quarantine"] = [d for d in it["quarantine"] if d["drive_id"] not in canon_ids]
    ready = [it for it in ready if it["quarantine"]]
    dups_on_nlm = [d for it in ready for d in it["quarantine"] if d["on_nlm"]]
    return {"ready": ready, "review": review,
            "total_quarantine": sum(len(it["quarantine"]) for it in ready),
            "dups_on_nlm": dups_on_nlm}

def _raw_dup_of_standard_rows(entries: list) -> list:
    """PURE (v1.29.3 — AUDIT #5, log LIVE 2.3): bắt 'BẢN TẢI THÔ TRÙNG BẢN CHUẨN' — dòng corpus=true có tên thô KHÔNG
    trích được sohieu chuẩn (vd 'ND274_2025_cham dong-tron dong BH.pdf' — mã loại DÍNH TRƯỚC số nên _RAW_SOHIEU_RE miss)
    nhưng tên chứa <MÃ-LOẠI><số>_<năm> khớp LỎNG với ĐÚNG 1 bản CHUẨN corpus=true trong corpus → đề xuất corpus=false.
    PROPOSE-ONLY (match lỏng KHÔNG đủ tin auto; regex lỏng CHỈ để dedup-match, KHÔNG bao giờ dùng gán sohieu).
    An toàn: chỉ xét raw corpus=true + sohieu-key RỖNG; chỉ đề xuất khi match DUY NHẤT (num+năm[+family]); bản chuẩn
    phải corpus=true (chuẩn đã tắt → raw có thể là bản duy nhất, KHÔNG đề xuất)."""
    _fam_norm = {"NĐ": "ND", "QĐ": "QD"}
    # Họ mã-loại CANONICAL — key trích ra family NGOÀI họ này (vd '274-2025-CHAM' từ tên thô 'ND274_2025_cham dong…',
    # 'CHAM' = từ đầu trích yếu bị nhận nhầm) = trích SAI → vẫn là ứng viên raw (chính là ca 5 dòng LIVE lọt qua S12).
    _canon_fams = {"ND", "TT", "QD", "NQ", "PL", "CT", "TTLT", "QH", "UBTVQH", "VBHN", "L", "LCT", "HDNN", "BTC",
                   "NHNN", "BYT", "BCA", "BQP", "CP", "TW", "KL", "HD", "CD"}   # CD = Công điện (CĐ→CD sau norm)

    def _key_fam(k: str) -> tuple:
        m = re.match(r"^(\d{1,4})-((?:19|20)\d{2})-([A-ZĐ]+)", k or "")
        # num chuẩn hoá str(int(...)) — số ZERO-PADDED ('06-2003-PL-UBTVQH11', đúng ca PL_06 log LIVE) phải khớp
        # lookup lỏng int('06')→'6' phía raw; giữ raw '06' sẽ MISS.
        return (str(int(m.group(1))), m.group(2), _fam_norm.get(m.group(3), m.group(3))) if m else (None, None, None)

    std_by_numyear: dict[tuple, list] = {}
    std_keys = set()
    for e in entries or []:
        if not _entry_corpus_true(e):
            continue
        k = _sohieu_key_entry(e)
        num, yr, fam = _key_fam(k)
        if fam and fam in _canon_fams:
            std_by_numyear.setdefault((num, yr), []).append((fam, e))
            std_keys.add(k)
    rows = []
    for e in entries or []:
        if not _entry_corpus_true(e):
            continue
        _k = _sohieu_key_entry(e)
        if _k:
            _n, _y, _f = _key_fam(_k)
            if (_f and _f in _canon_fams) or _k in std_keys:
                continue                               # key chuẩn thật (hoặc trùng chuẩn → việc của dedup-plan)
        nm = _entry_name(e)
        # Ứng viên PHẢI trông như FILE THÔ: có đuôi file hoặc chứa SPACE — tên chuẩn hoá không bao giờ có cả hai
        # (chống false-positive smoke LIVE: 'CD_32-2026-CD-TTg_…' tên CHUẨN loại hiếm bị ghép nhầm TT_32-2026).
        if not (re.search(r"\.(docx?|pdf|html?)\b", nm or "", re.I) or " " in (nm or "")):
            continue
        lm = _RAW_LOOSE_SOHIEU_RE.search(nm or "")
        if not lm:
            continue
        fam_raw = _fam_norm.get((lm.group(1) or "").upper(), (lm.group(1) or "").upper())
        cands = std_by_numyear.get((str(int(lm.group(2))), lm.group(3))) or []
        if fam_raw:
            cands = [(f, s) for f, s in cands if f.startswith(fam_raw) or fam_raw.startswith(f)]
        if len(cands) != 1:
            continue                                   # 0 hoặc >1 → KHÔNG đủ tin, bỏ
        _f, std = cands[0]
        did = _entry_drive_id(e)
        rows.append({"drive_id": did, "name": nm[:60],
                     "loose_match": f"{fam_raw or '?'}{int(lm.group(2))}-{lm.group(3)}",
                     "standard": {"drive_id": _entry_drive_id(std), "sohieu": _entry_sohieu(std) or _sohieu_key_entry(std),
                                  "name": _entry_name(std)[:60]},
                     "fix_command": f"tl source-update-corpus {did} false --apply"})
    return rows

def _corpus_count_server_rule(entries: list) -> int:
    """v1.30.1 (#7 log — PURE): đếm corpus THEO ĐÚNG LUẬT SERVER GAS (manifestHashObjs_/regIsCorpusCounted_,
    Code.2.21.2i.gs:2173-2183) trên CÙNG snapshot entries: corpus∈{true,vbqppl} HOẶC row_kind=overflow; TRỪ ref;
    TRỪ loai='thuong'. Đây là con số `manifest_export.corpus_count` mà `tl boot` in ra — KHÁC `sweep.corpus`
    (corpus=='true' thuần). In CẢ HAI cạnh nhau ⇒ hết 'chênh 12 dòng' bí ẩn giữa 2 lệnh (527 boot vs 515 sweep:
    khác TIÊU CHÍ + khác snapshot GAS-cache ~600s, không phải mất dữ liệu). Profile có registryDocId riêng: server
    đếm MỌI dòng có drive_id (nhánh _REQ_REGISTRY_ID_) — số này chỉ áp cho scope VBQPPL nền."""
    return sum(1 for e in (entries or []) if _entry_is_corpus_effective(e))


def _entry_is_corpus_effective(e: dict) -> bool:
    """v1.34.42 (BUG3 — grill-with-docs): predicate PURE 'corpus theo ĐÚNG LUẬT SERVER GAS' cho 1 entry (tách từ
    _corpus_count_server_rule để reg-query --corpus-effective dùng chung): corpus∈{true,vbqppl} HOẶC row_kind=overflow;
    TRỪ ref; TRỪ loai='thuong' (exact — mirror GAS regIsCorpusCounted_, KHÔNG lower/strip). KHÁC `--corpus true`
    literal (chỉ cột corpus=='true', mọi row_kind). Test offline được."""
    rk = str(_entry_row_kind(e) or "own").lower()
    if rk == "ref":
        return False
    c = str(e.get("corpus") or "").lower()
    if not (c in ("true", "vbqppl") or rk == "overflow"):
        return False
    # Review v1.30.1 (CONFIRMED): GAS so `o.loai!=='thuong'` EXACT (không lower/strip — Code.gs:2183) →
    # mirror NGUYÊN XI; 'Thuong' hoa server VẪN đếm. Lower hoá ở đây = tự tạo lệch mới với boot.
    if str(e.get("loai") or "") == "thuong":
        return False
    return True

def _corpus_fix_plan(entries: list) -> dict:
    """PURE (test offline): ĐIỀU PHỐI dọn/chỉnh lý corpus — gộp mọi detector (sweep) → kế hoạch THEO THỨ TỰ PHỤ THUỘC +
    phân TẦNG an toàn. Thứ tự CỐ ĐỊNH: shared-link→goc-nhiễm→infra→dedup→year→loai→title/cat→nlm-relabel→ingest→
    consolidation→quarantine. KHÔNG mutate; chỉ trả plan (mỗi step: order,id,tier,problem,count,command,reversible,note)."""
    rep = _sweep_report(entries)
    nb = os.environ.get("TL_NOTEBOOK_ID") or NLM_BASE_NOTEBOOK
    d = rep["duplicates"]
    dr = rep["nlm_drift"]
    _vgoc = set()
    for e in entries:
        if _is_vbhn_entry(e):
            _vgoc |= _goc_keys(e)
    consol = sum(1 for e in entries if _entry_corpus_true(e) and not _is_vbhn_entry(e)
                 and _sohieu_key_entry(e) and _sohieu_key_entry(e) in _vgoc)
    steps = []

    def add(order, sid, tier, problem, count, command, reversible, note, sample=None):
        if count:
            st = {"order": order, "id": sid, "tier": tier, "problem": problem, "count": count,
                  "command": command, "reversible": reversible, "note": note}
            if sample:
                st["sample"] = sample[:5]
            steps.append(st)

    add(1, "shared_source_id", "human_confirm",
        "Link NLM SAI (≥2 drive_id chung 1 source_id) — SỬA TRƯỚC mọi thao tác NLM (xóa 1 nguồn gãy link kia)",
        rep["shared_source_id"], f"tl shared-source-fix {nb}", False,
        "Tách: giữ link ở bản đúng, reg_clear link sai bản kia rồi re-push.", rep.get("shared_source_id_groups"))
    add(2, "goc_pollution", "human_confirm",
        "registry.goc NHIỄM → source-map/status redirect SAI văn bản",
        rep["goc_pollution"], "tl register --drive-id <id> --goc <suggested_goc>", False,
        "Sửa goc về suggested_goc (reg_upsert, KHÔNG reg_bulk). Xem sweep.goc_pollution_rows.", rep.get("goc_pollution_rows"))
    add(3, "infra_in_corpus", "safe_auto",
        "File HẠ TẦNG (.json/.enc/secrets) đánh dấu corpus=true = RÁC",
        rep["infra_in_corpus"], "tl corpus-fix --apply --tier safe", True,
        "REVERSIBLE: chỉ set corpus=false.", rep.get("infra_in_corpus_rows"))
    add(4, "duplicates", "safe_auto",
        "Trùng lặp thật (same-document / md5 / identity)",
        d["same_document"] + d["by_md5"] + d["identity"], "tl dedup-plan --apply (hoặc corpus-fix --apply --tier safe)", True,
        "REVERSIBLE: GIỮ canonical, bản dup → corpus=false.")
    add(5, "vbhn_missing_year", "metadata_deterministic",
        "VBHN sohieu/tên THIẾU năm (số tái dùng theo năm → collision)",
        rep["vbhn_year"]["fixable"], "tl vbhn-year-fix --with-name --apply", False,
        f"{rep['vbhn_year']['needs_year']} cần xác minh năm tay; {rep['vbhn_year']['conflicts']} conflict phân biệt tay.")
    add(6, "loai_noncanonical", "metadata_deterministic",
        "Trường `loai` phi chuẩn", rep["loai_noncanonical"], "tl backfill-loai --normalize --apply", False,
        "Suy loai từ số hiệu/tên; --normalize sửa cả dòng loai SAI enum (map tất định 'Luat'→'Luật').")
    add(7, "title_cat_mismatch", "human_confirm",
        "Tên/cat/trích yếu LỆCH nội dung (cần ĐỌC header — cat-verify suy bừa khi GAS-fallback)",
        rep["title_mismatch"], "tl corpus-audit  → tl source-rename/recat theo header-verify", False,
        "KHÔNG auto: dùng `header-verify` ground-truth rồi sửa tay.")
    # MERGE Codex v1.33.11: bước raw_on_nlm vào orchestrator (detector v1.33.4 đã đếm — plan phải có đường sửa).
    add(8, "raw_on_nlm", "human_confirm",
        "FILE THÔ (.html/.docx/.pdf) đang là nguồn NLM live — trái doctrine 'chỉ push GDoc'",
        rep["raw_on_nlm"],
        "tl sweep --json  # xem raw_on_nlm_rows; từng dòng: copy_convert → nlm-add GDoc mới → source-update-corpus raw false --apply --confirm yes",
        False,
        "KHÔNG auto: phải bảo đảm GDoc mới đã push thành công trước khi gỡ source raw cũ; ưu tiên Luật trước.",
        rep.get("raw_on_nlm_rows"))
    add(9, "raw_dup_of_standard", "human_confirm",
        "Bản TẢI THÔ nghi TRÙNG bản chuẩn (tên thô không trích được sohieu, kẹt corpus=true, đốt batch ingest-missing)",
        rep["raw_dup_of_standard"], "tl source-update-corpus <drive_id> false --apply   # per-row, undo được", True,
        "PROPOSE-ONLY (match lỏng số+năm[+loại]): soát từng dòng raw_dup_of_standard_rows rồi tắt corpus bản thô.",
        rep.get("raw_dup_of_standard_rows"))
    add(10, "nlm_status_mismatch", "safe_auto",
        "Nhãn nlm_status LẠ (hygiene, KHÔNG phải desync sống)",
        dr.get("NLM_STATUS_MISMATCH", 0), f"tl nlm-orphans {nb} --fix-mismatch --apply", True,
        "Vá nhãn metadata (removed*→pushed nếu nguồn sống).")
    add(11, "corpus_not_on_nlm", "structural",
        "corpus=true CHƯA trên NLM (phần lớn do cap 300/notebook)",
        dr.get("CORPUS_TRUE_NOT_ON_NLM", 0), "tl ingest-missing --apply   (cần slot/overflow — JOB LỚN, KHÔNG về 0)", False,
        "CẤU TRÚC: corpus>cap → cần sharding/overflow.")
    add(12, "consolidation", "human_confirm",
        "Cùng lúc CÓ VBHN + gốc/sửa đổi RỜI còn corpus=true → nên gộp về VBHN (khi tìm thành phần trả ra VBHN)",
        consol, "tl consolidation-cleanup", True, "Set thành phần corpus=false khi VBHN verify phủ (reversible).")
    add(13, "quarantine_conflict", "safe_auto",
        "Quarantine MÂU THUẪN (corpus=true / stale NLM ref; nguồn LIVE xoá tay)",
        rep["quarantine"]["corpus_true"] + rep["quarantine"]["stale_nlm_ref"] + rep["quarantine"]["still_on_nlm"],
        "tl quarantine-fix --apply", True,
        "REVERSIBLE: chuẩn nhãn + corpus=false + reg_clear stale nlm_source_id (B3/B9 v1.33.22); "
        "still_on_nlm chỉ báo — xoá nguồn LIVE tay sau verify.")
    steps.sort(key=lambda s: s["order"])
    return {"ok": True, "total": rep["total"], "corpus": rep["corpus"], "step_count": len(steps), "steps": steps,
            "safe_auto": [s for s in steps if s["tier"] == "safe_auto"],
            "needs_human": [s for s in steps if s["tier"] != "safe_auto"],
            "note": "CHẠY THEO `order` (sai thứ tự=hỏng thêm). safe_auto=reversible (corpus=false) → `corpus-fix --apply "
                    "--tier safe`. metadata/human_confirm/structural: chạy lệnh in sẵn, người duyệt (đọc header/xác minh)."}

def _audit_row_flatten(r: dict) -> dict:
    """S-1 (v1.33.15 — log rà 40: driver đọc rows[].type/severity/suggested_name/proposal = null trong khi
    summary đếm proposal_count=2 — chi tiết chỉ nằm LỒNG trong proposals[], schema summary↔row lệch nhau):
    MIRROR đề xuất CHÍNH (proposals[0] — đã sort severity, nặng nhất) lên top-level row để driver phẳng đọc
    được; proposals[] giữ nguyên là nguồn sự thật đầy đủ. Idempotent (gọi lại trên row đã flatten vô hại)."""
    ps = r.get("proposals") or []
    p0 = ps[0] if ps else {}
    r["type"] = p0.get("type")
    r["severity"] = p0.get("severity")
    r["icon"] = p0.get("icon")
    r["current"] = p0.get("current")
    r["suggested"] = p0.get("suggested")
    r["suggested_name"] = p0.get("suggested")   # alias — driver log rà 40 đọc key này
    r["fix_command"] = p0.get("fix_command")
    r["command"] = p0.get("fix_command")        # v1.33.16 (MERGE nhánh-4): alias `command` cho driver phẳng
    r["proposal"] = p0 or None
    r["proposal_count"] = len(ps)               # v1.33.16 (MERGE nhánh-4): đối soát nhanh không cần đếm proposals[]
    r["flags"] = [p.get("type") for p in ps]
    return r

def _rq_rel_strong(cands: list[dict]) -> bool:
    """P2-2 (v1.33.12): ứng viên đủ MẠNH cho bucket HÀNH ĐỘNG relation_backfill — linked/strong/confidence≠low
    (cùng ngưỡng escalate v1.29.6). Toàn low-conf → relation_low_confidence (INFO), vì `relation-check --base
    --subject` (chuẩn) thường phủ định các ca này (log: 3/3 trả OK, missing_links=[])."""
    return any(bool(c.get("linked_to_query")) or bool(c.get("strong"))
               or (str(c.get("confidence") or "low") != "low") for c in (cands or []))
