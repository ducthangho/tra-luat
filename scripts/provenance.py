#!/usr/bin/env python3
"""Sinh CẢNH BÁO provenance + freshness cho câu trả lời nguyên văn.

Hai trục ĐỘC LẬP (phản biện v1.9.8):
  - provenance (nguồn ở đâu): official vs secondary vs draft/upload.
  - freshness  (còn hiện hành không): bản đã verified lần cuối khi nào, đối chiếu
    với cái gì. Một bản 'official' nhưng lấy 6 tháng trước VẪN có thể lỗi thời nếu
    đã có VBHN/sửa đổi mới — đây là lỗ hổng mà phân tầng provenance KHÔNG bắt được.

Hàm thuần, deterministic -> test hermetic. KHÔNG gọi mạng: chỉ đọc metadata sẵn có.
"""
from __future__ import annotations

from datetime import datetime, timezone

# Ngưỡng coi cache là "có thể đã cũ" cho văn bản đã ban hành (ngày).
DEFAULT_STALE_DAYS = 120


def _parse_iso(s: str):
    if not s:
        return None
    try:
        s2 = s.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s2)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None


def _age_days(iso_ts: str, now: datetime | None = None) -> int | None:
    dt = _parse_iso(iso_ts)
    if not dt:
        return None
    now = now or datetime.now(timezone.utc)
    return (now - dt).days


def build_warnings(meta: dict, now: datetime | None = None,
                   stale_days: int = DEFAULT_STALE_DAYS) -> list[dict]:
    """meta: trộn legal_document + cache record. Trường dùng (đều optional):
        officialness_level / officialness, verbatim_status, source.type,
        doc_status, document_variant, consolidation_checked,
        verified_at, verified_against, fetched_at.

    Trả list cảnh báo [{level, code, message}]. level: info|warn|block.
    """
    off = (meta.get("officialness_level") or meta.get("officialness") or "").lower()
    vstat = (meta.get("verbatim_status") or "").lower()
    src_type = ((meta.get("source") or {}).get("type") or meta.get("source_type") or "").lower()
    doc_status = (meta.get("doc_status") or "unknown").lower()
    variant = (meta.get("document_variant") or "").lower()
    consolidation_checked = bool(meta.get("consolidation_checked", False))
    verified_at = meta.get("verified_at") or ""
    verified_against = meta.get("verified_against") or ""
    fetched_at = meta.get("fetched_at") or ""

    w: list[dict] = []

    # --- PROVENANCE ---
    if doc_status == "draft" or variant == "draft" or src_type in {"uploaded_file", "google_drive"} and doc_status != "promulgated":
        if doc_status == "draft" or variant == "draft":
            w.append({"level": "warn", "code": "draft",
                      "message": "Đây là bản DỰ THẢO / bản làm việc, KHÔNG phải văn bản đã ban hành. "
                                 "Không dùng làm trích dẫn chính thức."})
    if off == "secondary" or vstat == "secondary_html" or src_type in {"aitracuuluat", "thuvienphapluat", "luatvietnam"}:
        w.append({"level": "warn", "code": "secondary_source",
                  "message": "Nguồn SECONDARY (vd AI Tra Cứu Luật/Thư viện Pháp luật). Dùng để tra nhanh; "
                             "ĐỐI CHIẾU bản official (vbpl/Công báo) trước khi dùng trong văn bản chính thức."})
    if vstat == "ocr_unverified":
        w.append({"level": "warn", "code": "ocr_unverified",
                  "message": "Nội dung có thể qua OCR/trích text — kiểm lại file gốc."})
    if src_type in {"uploaded_file", "google_drive"} and off in {"", "needs_manual_check"} and doc_status != "draft":
        w.append({"level": "info", "code": "user_provided",
                  "message": "Bản do người dùng/Drive cung cấp, chưa xác minh nguồn gốc official."})

    # --- VERSION (original vs VBHN) ---
    if variant in {"original", ""} and not consolidation_checked and doc_status != "draft":
        w.append({"level": "warn", "code": "consolidation_unchecked",
                  "message": "Là bản GỐC và CHƯA kiểm liệu đã có văn bản hợp nhất (VBHN)/sửa đổi mới hơn chưa. "
                             "Nếu văn bản từng được sửa đổi, ưu tiên VBHN."})

    # --- FRESHNESS (trục riêng) ---
    if doc_status == "promulgated" or off == "official":
        if not verified_at:
            ref = fetched_at
            age = _age_days(ref)
            if age is None:
                w.append({"level": "info", "code": "freshness_unknown",
                          "message": "Chưa ghi nhận thời điểm đối chiếu official — không rõ còn hiện hành không."})
            elif age >= stale_days:
                w.append({"level": "warn", "code": "stale_unverified",
                          "message": f"Lấy ~{age} ngày trước và CHƯA đối chiếu official kể từ đó — "
                                     f"có thể đã có sửa đổi/VBHN mới. Nên kiểm lại VBPL."})
        else:
            age = _age_days(verified_at)
            note = f" (đối chiếu: {verified_against})" if verified_against else ""
            if age is not None and age >= stale_days:
                w.append({"level": "warn", "code": "verified_but_old",
                          "message": f"Đối chiếu official lần cuối ~{age} ngày trước{note} — cân nhắc kiểm lại nếu cần bản mới nhất."})
    return w


def render_warnings(warnings: list[dict]) -> str:
    if not warnings:
        return ""
    icon = {"info": "ℹ️", "warn": "⚠️", "block": "⛔"}
    lines = ["", "---", "**Cảnh báo nguồn / hiệu lực:**"]
    for x in warnings:
        lines.append(f"- {icon.get(x['level'], '•')} {x['message']}")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    import json
    ap = argparse.ArgumentParser()
    ap.add_argument("meta_json", help="File JSON metadata (legal_document hoặc cache record)")
    ap.add_argument("--stale-days", type=int, default=DEFAULT_STALE_DAYS)
    a = ap.parse_args()
    meta = json.load(open(a.meta_json, encoding="utf-8"))
    ws = build_warnings(meta, stale_days=a.stale_days)
    print(json.dumps(ws, ensure_ascii=False, indent=2))
    print(render_warnings(ws))
