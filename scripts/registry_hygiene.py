#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""registry_hygiene.py — detect duplicate/orphan/mislabeled manifest rows without mutating Drive.

Inputs:
  - --manifest FILE: local manifest JSON produced by tl boot, or
  - no --manifest: call webapp manifest_export + download via gas.py.

The script reports suspicious groups only. It never moves, trashes, or rewrites registry rows.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent


def strip_vn(s: str) -> str:
    table = str.maketrans({"đ": "d", "Đ": "D"})
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s.translate(table))
                   if unicodedata.category(c) != "Mn")


def norm_sohieu(s: str) -> str:
    if not s:
        return ""
    s = s.strip().upper().replace("Đ", "D")
    s = re.sub(r"[\/\s]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    m = re.fullmatch(r"(\d{1,4})-VPQH", s)
    if m:
        return f"{m.group(1)}-VBHN-VPQH"
    return s


VBHN_KEY_RE = re.compile(r"^\d{1,5}(?:-\d{1,5})?-VBHN-([A-Z0-9D]+)$")


def vbhn_agency_from_key(key: str) -> str:
    m = VBHN_KEY_RE.fullmatch(norm_sohieu(key or ""))
    return m.group(1) if m else ""


def name_key(name: str) -> str:
    n = re.sub(r"\.(docx?|pdf|txt|html?)$", "", name or "", flags=re.I)
    n = re.sub(r"_\d{5,}$", "", n)
    n = strip_vn(n).lower()
    n = re.sub(r"[^a-z0-9]+", "_", n).strip("_")
    return n


def row_id(e: dict) -> str:
    return e.get("id") or e.get("drive_id") or e.get("gdoc_id") or ""


def row_sohieu(e: dict) -> str:
    raw = norm_sohieu(e.get("so_hieu") or e.get("sohieu") or "")
    return raw


def row_kind(e: dict) -> str:
    return str(e.get("row_kind") or "own").strip().lower() or "own"


def is_own_thuong(e: dict) -> bool:
    corpus = str(e.get("corpus") or "").strip().lower()
    loai = str(e.get("loai") or "").strip().lower()
    return row_kind(e) == "own" and (loai == "thuong" or corpus in {"false", "thuong"})


def is_raw_name(name: str) -> bool:
    return bool(re.match(r"^\d+_\d{4}_[A-Z]+_\d{5,}", name or ""))


def is_vbhn_entry(e: dict) -> bool:
    txt = " ".join(str(x or "") for x in (e.get("so_hieu") or e.get("sohieu"), e.get("loai"), e.get("name"))).upper()
    return "VBHN" in txt or "VAN BAN HOP NHAT" in strip_vn(txt).upper()


def entry_date_text(e: dict) -> str:
    for k in ("ngay_ban_hanh", "ngayBanHanh", "ngaybanhanh", "issued_date", "issue_date", "date", "ngay", "ban_hanh"):
        v = e.get(k)
        if v:
            return str(v)
    return ""


def year_from_text_safe(text: str) -> int | None:
    txt = strip_vn(str(text or "")).lower()
    pats = [
        r"(?:ngay)\s+\d{1,2}\s*(?:/|-|\s+thang\s+)\s*\d{1,2}\s*(?:/|-|\s+nam\s+)(19\d{2}|20\d{2})",
        r"(?:nam|issue[_\s-]*year|issued[_\s-]*year|nam[_\s-]*ban[_\s-]*hanh)\D{0,8}(19\d{2}|20\d{2})",
        r"(?:^|[_\s.-])(19\d{2}|20\d{2})(?=$|[_\s.-])",
    ]
    for pat in pats:
        m = re.search(pat, txt, re.I)
        if m:
            return int(m.group(1))
    return None


def entry_issue_year(e: dict) -> int | None:
    explicit = e.get("issue_year") or e.get("issued_year") or e.get("year") or e.get("nam") or e.get("nam_ban_hanh")
    if explicit:
        y = year_from_text_safe(str(explicit))
        if y:
            return y
        m0 = re.fullmatch(r"\s*(19\d{2}|20\d{2})\s*", str(explicit))
        if m0:
            return int(m0.group(1))
    y = year_from_text_safe(entry_date_text(e))
    if y:
        return y
    # Do not read tukhoa/keywords/trich_yeu here: those often contain the year
    # of source documents consolidated into a VBHN, not the VBHN issue year.
    for text in (e.get("name"), e.get("title_vn"), e.get("nlm_title")):
        y = year_from_text_safe(str(text or ""))
        if y:
            return y
    return None


STOP_TOKENS = {
    "luat", "bo", "nghi", "dinh", "thong", "tu", "quyet", "van", "ban",
    "hop", "nhat", "vbhn", "qh", "vpqh", "cp", "docx", "pdf", "goc",
    "raw", "final", "copy", "ve", "cua", "va", "cac", "mot", "so",
}
OMNIBUS_TITLE_HINTS = (
    "sua doi", "bo sung", "mot so dieu", "mot so luat", "nhieu luat",
    "quy hoach", "dau tu", "dau thau", "ppp", "doi tac cong tu", "luat khac",
)
META_TITLE_KEYS = (
    "title_vn", "nlm_title", "trich_yeu", "mo_ta", "description",
    "official_title", "ten", "ten_van_ban",
)
REF_KEYS = (
    "goc", "sua_doi", "sua_doi_bo_sung", "sdbs", "supersedes",
    "targets", "target_sohieu", "related", "relations",
)


def field_text(e: dict, keys: tuple[str, ...]) -> str:
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


def token_set(s: str) -> set[str]:
    toks = re.findall(r"[a-z0-9]{3,}", strip_vn(str(s or "")).lower())
    return {t for t in toks if t not in STOP_TOKENS and not t.isdigit()}


def ref_tokens(s) -> set[str]:
    text = strip_vn(json.dumps(s, ensure_ascii=False) if isinstance(s, (dict, list, tuple)) else str(s or "")).upper()
    pats = re.findall(r"\b\d{1,5}[-/]\d{4}[-/][A-Z0-9-]+\b|\b\d{1,5}[-/](?:\d{1,5}[-/])?VBHN[-/][A-Z0-9D]{2,20}\b|\b\d{1,5}[-/](?:VBHN-)?[A-Z0-9]{2,12}\b", text)
    return {norm_sohieu(x) for x in pats}


def name_tail_key(name: str) -> str:
    n = strip_vn(str(name or "")).lower()
    n = re.sub(r"\.(docx?|pdf|gdoc|txt|html?)$", "", n, flags=re.I)
    n = re.sub(r"[_ -]?\d{5,}$", "", n)
    n = re.sub(r"^(luat|bo_luat|bl|vbhn|nd|nq|tt|qd|pl|ct|kl|hp)[ _.-]+", "", n)
    n = re.sub(r"^\d{1,5}[-_/]\d{4}[-_/][a-z0-9-]+[ _.-]*", "", n)
    n = re.sub(r"^\d{1,5}[-_/](?:\d{1,5}[-_/])?(?:vbhn[-_/])?[a-z0-9-]+[ _.-]*", "", n)
    n = re.sub(r"[^a-z0-9]+", " ", n)
    return re.sub(r"\s+", " ", n).strip()


def _nlm_status_known_local(status: str) -> bool:
    """r253 — CỬA ĐỌC nlm_status theo ADR-0010, dạng TIỀN TỐ. Trước đây chỗ này giữ BẢN SAO exact-set
    {pushed,synced,removed,removed_from_drive,deleted,trash,trashed} — đã TRÔI LỆCH khỏi bản chuẩn
    `tl_core.classify._nlm_status_known`: thiếu `active` (ADR-0010 nắn live→active MỘT LẦN) và thiếu MỌI
    biến thể `removed_<lý do>` (chính docstring bản chuẩn hứa `removed_superseded_by_VBHN` chạy được).
    Script này CỐ Ý đứng độc lập (chỉ import `gas` lazy) nên KHÔNG import tl_core — giữ bản sao NHƯNG
    theo cùng LUẬT tiền tố, không phải danh sách cứng, để không trôi lệch lần nữa.
    Đo 30-07-2026: chưa false-fire THẬT vì `analyze()` skip row_kind=ref + own_thuong TRƯỚC khi gắn cờ
    (6 dòng `active` đều ref; 10 dòng `removed_*` đều own_thuong) — vá vì cờ sẽ nổ ngay khi có dòng
    own/khác-thuong mang các giá trị ĐÚNG CHUẨN đó."""
    s = (status or "").strip().lower()
    if not s:
        return True
    return (s.startswith("pushed") or s.startswith("synced") or s == "active"
            or s.startswith("removed") or s.startswith("trash") or s == "deleted")


def title_flags(e: dict) -> list[str]:
    flags = []
    name = e.get("name", "")
    cat = str(e.get("cat") or "").strip().lower()
    if e.get("nlm_source_id") and not name and not row_sohieu(e) and ((not cat) or cat in ("root", "(root)", "none", "null")):
        flags.append("NLM_GHOST_SOURCE")
    nlm_status = str(e.get("nlm_status") or "").strip().lower()
    if e.get("nlm_source_id") and nlm_status and not _nlm_status_known_local(nlm_status):
        flags.append("NLM_STATUS_MISMATCH")
    if (not cat) or cat in ("root", "(root)", "none", "null"):
        flags.append("ORPHAN_CAT")
    if not row_sohieu(e):
        flags.append("MISSING_SOHIEU")
    if is_raw_name(name) and not e.get("nlm_source_id"):
        flags.append("RAW_NAME_NOT_NLM")

    tail = name_tail_key(name)
    if is_vbhn_entry(e):
        issue_year = entry_issue_year(e)
        if len(token_set(tail)) < 2:
            flags.append("VBHN_BARE_NUMBER")
        if issue_year is None:
            flags.append("VBHN_MISSING_YEAR_OR_DATE")
        raw = norm_sohieu(e.get("so_hieu") or e.get("sohieu") or "")
        if re.fullmatch(r"\d{1,4}-VBHN-VPQH", row_sohieu(e)) and "VBHN" not in str(e.get("so_hieu") or e.get("sohieu") or "").upper():
            flags.append("VBHN_SOHIEU_NORMALIZED_FROM_SHORT_VPQH")
        if issue_year is not None and not re.search(rf"(?<!\d){issue_year}(?!\d)", name or ""):
            flags.append("VBHN_NAME_MISSING_YEAR")
        agency = vbhn_agency_from_key(row_sohieu(e))
        if agency and agency != "VPQH":
            flags.append("VBHN_MINISTRY_SCOPE")
            if issue_year is None:
                flags.append("VBHN_MINISTRY_MISSING_YEAR")
            elif not re.search(rf"(?<!\d){issue_year}(?!\d)", name or ""):
                flags.append("VBHN_MINISTRY_NAME_MISSING_YEAR")
    refs = ref_tokens(field_text(e, REF_KEYS))
    if (not is_vbhn_entry(e)) and len(refs) >= 2 and tail and not any(h in tail for h in OMNIBUS_TITLE_HINTS):
        flags.append("OMNIBUS_NARROW_TITLE_CHECK")

    meta_text = field_text(e, META_TITLE_KEYS)
    if tail and meta_text:
        tail_tokens = token_set(tail)
        meta_tokens = token_set(meta_text)
        if len(tail_tokens) >= 2 and meta_tokens and not (tail_tokens & meta_tokens):
            flags.append("TITLE_METADATA_MISMATCH")
    return flags


DEFAULT_PROFILE = "vbqppl"


def _scope_params() -> dict:
    if (os.environ.get("TL_PROFILE") or DEFAULT_PROFILE) == DEFAULT_PROFILE:
        return {}
    out = {}
    if os.environ.get("TL_REGISTRY_DOC_ID"):
        out["registryDocId"] = os.environ["TL_REGISTRY_DOC_ID"]
    if os.environ.get("TL_MANIFEST_ID"):
        out["manifestId"] = os.environ["TL_MANIFEST_ID"]
    return out


def load_manifest_from_webapp() -> dict:
    sys.path.insert(0, str(HERE))
    sys.path.insert(0, str(HERE / "_fallback"))
    import gas  # type: ignore
    scope = _scope_params()
    head = gas.get("manifest_export", **scope)
    if head.get("ok") is False:
        raise RuntimeError(json.dumps(head, ensure_ascii=False))
    mid = head.get("manifestId") or head.get("manifestFileId") or head.get("driveFileId")
    if not mid:
        raise RuntimeError("manifest_export did not return manifestId")
    down = gas.get("download", fileId=mid, **scope)
    if down.get("ok") is False or not down.get("b64"):
        raise RuntimeError(json.dumps(down, ensure_ascii=False))
    return json.loads(base64.b64decode(down["b64"]).decode("utf-8"))


def entries(man: dict) -> list[dict]:
    rows = man.get("entries") or man.get("files") or []
    if isinstance(rows, dict):
        return list(rows.values())
    if isinstance(rows, list):
        return rows
    return []


def _subject_sig(name: str) -> str:
    """KH1 Pha 1.5: chữ ký CHỦ ĐỀ của tên (bỏ đuôi file + doctype + số hiệu/năm + cơ quan TW) để phân biệt dup CÙNG
    văn bản (sidecar/khác format) vs văn bản KHÁC NHAU cùng số hiệu. Mirror tl._subject_sig."""
    s = strip_vn(re.sub(r"\.(docx?|pdf)$", "", name or "")).lower()
    s = re.sub(r"\b(vbhn|vpqh|ubtvqh\d*|qh\d*|nd|cp|tt|nq|qd|ct|pl|tw|ttg|lctn|blds?|luat|bo|nghidinh|thongtu|quyetdinh|chithi|nghiquyet|hopnhat|goc)\b", " ", s)
    s = re.sub(r"\d", " ", s)
    return re.sub(r"[^a-z]", "", s)


def analyze(rows: list[dict]) -> dict:
    by_so, by_name = defaultdict(list), defaultdict(list)
    root_rows, raw_rows, no_sohieu, title_mismatch, ghost_rows = [], [], [], [], []
    # v1.35.65: ĐẾM phần bị loại. Trước đây `count` = TỔNG dòng còn mọi bucket chỉ tính trên phần ĐÃ LỌC
    # ⇒ đọc "count=90, missing_sohieu=19" ra "19/90" là SAI (thật ra 19 trên ~34 dòng được quét; hồ sơ
    # Luật BHXH có 56 dòng sohieu rỗng). Phơi `scanned` + `basis` như `sweep.corpus_basis` để hết đọc nhầm.
    skipped_ref = skipped_thuong = 0
    for e in rows:
        if row_kind(e) == "ref":
            skipped_ref += 1
            continue
        if is_own_thuong(e):
            skipped_thuong += 1
            continue
        sh = row_sohieu(e)
        nk = name_key(e.get("name", ""))
        flags = title_flags(e)
        # S-2 (v1.33.32 — PORT bundle-12): OMNIBUS_NARROW_TITLE_CHECK là advisory trên entry (source-map/status;
        # sweep tl.py có bucket omnibus_title_advisory riêng) — mirror này không đếm kép vào title_mismatch.
        if any(f in flags for f in ("TITLE_METADATA_MISMATCH", "VBHN_BARE_NUMBER", "VBHN_MISSING_YEAR_OR_DATE", "VBHN_NAME_MISSING_YEAR", "VBHN_SOHIEU_NORMALIZED_FROM_SHORT_VPQH", "VBHN_MINISTRY_MISSING_YEAR", "VBHN_MINISTRY_NAME_MISSING_YEAR", "NLM_GHOST_SOURCE", "NLM_STATUS_MISMATCH")):
            title_mismatch.append(e)
        if "NLM_GHOST_SOURCE" in flags:
            ghost_rows.append(e)
        if sh:
            by_so[sh].append(e)
        else:
            no_sohieu.append(e)
        if nk:
            by_name[nk].append(e)
        if str(e.get("cat") or "") == "(root)":
            root_rows.append(e)
        if is_raw_name(e.get("name", "")):
            raw_rows.append(e)
    dup_so = {k: v for k, v in by_so.items() if len(v) > 1}
    # KH1 Pha 1.5: TÁCH dup số hiệu — CONFLICT (≥2 chữ-ký-chủ-đề KHÁC nhau cùng số hiệu = văn bản KHÁC, NGUY HIỂM tra sai)
    # vs SAME_DOC (1 chữ ký = sidecar/khác-format CÙNG văn bản, lành). Bản nào ĐÚNG do header-verify (G2) quyết.
    conflict, same_doc = {}, {}
    for k, v in dup_so.items():
        sigs = {_subject_sig(e.get("name", "")) for e in v}
        sigs.discard("")
        (conflict if len(sigs) > 1 else same_doc)[k] = v
    return {
        "count": len(rows),
        "scanned": len(rows) - skipped_ref - skipped_thuong,
        "skipped_ref": skipped_ref,
        "skipped_own_thuong": skipped_thuong,
        "basis": ("count = TỔNG dòng registry; MỌI bucket dưới đây chỉ tính trên `scanned` "
                  "(= count − skipped_ref − skipped_own_thuong): dòng row_kind='ref' (mượn từ scope NỀN) "
                  "và bản gốc loai='thuong' KHÔNG được quét vì chúng vốn không mang số hiệu/tên chuẩn."),
        "duplicate_sohieu": dup_so,
        "sohieu_conflict_different_doc": conflict,
        "sohieu_dup_same_doc": same_doc,
        "duplicate_name": {k: v for k, v in by_name.items() if len(v) > 1},
        "root_rows": root_rows,
        "raw_name_rows": raw_rows,
        "missing_sohieu": no_sohieu,
        "title_mismatch_rows": title_mismatch,
        "ghost_nlm_rows": ghost_rows,
    }


def compact(e: dict) -> dict:
    return {
        "id": row_id(e),
        "name": e.get("name", ""),
        "so_hieu": e.get("so_hieu") or e.get("sohieu") or "",
        "cat": e.get("cat", ""),
        "row_kind": e.get("row_kind") or "own",
        "corpus": e.get("corpus", ""),
        "nlm": bool(e.get("nlm_source_id")),
        "status": e.get("nlm_status", ""),
        "issue_year": entry_issue_year(e),
        "flags": title_flags(e),
    }


# H2: KHÓA tóm tắt top-level của registry-doctor. Dòng text SINH TỪ danh sách này → text & JSON DÙNG CHUNG
# schema, KHÔNG THỂ lệch nhãn lần nữa (trước đây text in 'duplicate_sohieu/title_mismatch/rows' lệch JSON).
_DOCTOR_SUMMARY_KEYS = ("count", "scanned", "duplicate_sohieu_groups", "sohieu_conflict_groups",
                        "duplicate_name_groups",
                        "root_rows", "raw_name_rows", "missing_sohieu", "title_mismatch_candidates", "ghost_nlm_rows")


def build_doctor_summary(rep: dict) -> dict:
    """Đếm theo bucket → dict scalar top-level (cùng KHÓA cho text lẫn JSON).
    v1.35.65: `scanned` đi kèm `count` — mọi bucket là trên `scanned`, KHÔNG phải trên `count`."""
    return {
        "count": rep["count"],
        "scanned": rep.get("scanned", rep["count"]),
        "skipped_ref": rep.get("skipped_ref", 0),
        "skipped_own_thuong": rep.get("skipped_own_thuong", 0),
        "basis": rep.get("basis", ""),
        "duplicate_sohieu_groups": len(rep["duplicate_sohieu"]),
        "sohieu_conflict_groups": len(rep.get("sohieu_conflict_different_doc", {})),
        "duplicate_name_groups": len(rep["duplicate_name"]),
        "root_rows": len(rep["root_rows"]),
        "raw_name_rows": len(rep["raw_name_rows"]),
        "missing_sohieu": len(rep["missing_sohieu"]),
        "title_mismatch_candidates": len(rep["title_mismatch_rows"]),
        "ghost_nlm_rows": len(rep.get("ghost_nlm_rows", [])),
    }


def format_doctor_text(summary: dict) -> str:
    """Dòng text 1-1 với khóa JSON (sinh từ _DOCTOR_SUMMARY_KEYS) → parser text/json đọc cùng tên khóa."""
    return " ".join(f"{k}={summary[k]}" for k in _DOCTOR_SUMMARY_KEYS)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", help="local manifest JSON file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--limit", type=int, default=20)
    a = ap.parse_args(argv)
    if a.manifest:
        man = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    else:
        try:
            man = load_manifest_from_webapp()
        except Exception as e:
            print(f"[registry-doctor] {e}\n  → dùng --manifest <file> offline, hoặc tl init-config / export TL_WEBAPP+TL_TOKEN.")
            return 2
    rep = analyze(entries(man))
    summary = build_doctor_summary(rep)        # H2: 8 khóa scalar dùng CHUNG cho text + JSON
    out = {
        **summary,
        "samples": {
            "duplicate_sohieu": {k: [compact(x) for x in v[:a.limit]]
                                  for k, v in list(rep["duplicate_sohieu"].items())[:a.limit]},
            "sohieu_conflict": {k: [compact(x) for x in v[:a.limit]]
                                 for k, v in list(rep.get("sohieu_conflict_different_doc", {}).items())[:a.limit]},
            "duplicate_name": {k: [compact(x) for x in v[:a.limit]]
                                for k, v in list(rep["duplicate_name"].items())[:a.limit]},
            "root_rows": [compact(x) for x in rep["root_rows"][:a.limit]],
            "raw_name_rows": [compact(x) for x in rep["raw_name_rows"][:a.limit]],
            "title_mismatch": [compact(x) for x in rep["title_mismatch_rows"][:a.limit]],
            "ghost_nlm": [compact(x) for x in rep.get("ghost_nlm_rows", [])[:a.limit]],
        }
    }
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(format_doctor_text(summary))     # H2: nhãn text = khóa JSON (sinh từ _DOCTOR_SUMMARY_KEYS)
        print(json.dumps(out["samples"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
