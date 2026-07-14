#!/usr/bin/env python3
"""Tra cứu CHÍNH XÁC TỪNG CÂU CHỮ một đơn vị (Điều/Khoản/Điểm/Mục) từ một
legal_document.json đã chuẩn hóa.

NGUYÊN TẮC CỐT LÕI: đây là tra cứu XÁC ĐỊNH (deterministic lookup), KHÔNG sinh
văn bản, KHÔNG paraphrase. Trả về nguyên văn `text` của đơn vị trong structure[]
— vốn được tách trực tiếp từ nguồn đã xác minh. Vì vậy nội dung trung thực 100%
với nguồn đã nạp (rủi ro còn lại chỉ ở khâu thu thập/parse, được kiểm bằng
verify substring).

Khác hẳn hỏi đáp RAG/NotebookLM (có sinh + cắt chunk, ~92-96%). NotebookLM chỉ
nên dùng để ĐỊNH VỊ văn bản; nội dung trả về phải qua tra cứu nguyên văn này.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import read_json  # noqa: E402
import provenance  # noqa: E402


def _norm(s: str) -> str:
    return unicodedata.normalize("NFC", (s or "")).strip().lower()


def _norm_label(s: str) -> str:
    """Chuẩn hóa nhãn truy vấn: 'điều 7, khoản 2, điểm a' -> 'điều 7 khoản 2 điểm a'."""
    s = _norm(s)
    s = re.sub(r"[.,;]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _expand_abbrev(s: str) -> str:
    """Mở viết tắt phổ biến (đã lowercase), xử lý THEO TỪNG TOKEN để không nuốt
    nhầm các từ đầy đủ (điều/khoản/điểm/mục). Quy tắc theo ký tự sau:
      đ/d + SỐ -> điều ; đ/d + 1 CHỮ -> điểm ; k/kh + SỐ -> khoản ;
      m + SỐ/La Mã -> mục. Chấp nhận không dấu (d) và dính liền (đ7k2đa)."""
    # 0) gộp viết tắt bị tách bởi dấu chấm/cách: 'đ . 7' / 'đ. 7' / 'đ 7' / 'k 2' -> 'đ7' 'k2'.
    #    chỉ gộp khi chữ đơn lẻ (đ/d/k/kh/m) đứng riêng rồi tới số/La Mã/1-chữ-cái.
    s = re.sub(r"\b(đ|d|kh|k|m)\s*\.?\s+(?=(?:\d+|[ivxlcdm]+\b|[a-zđ]\b))", r"\1", s)
    # 1) tách cụm dính liền: chèn space trước mỗi ký tự mở cụm mới (đ/d/k/kh/m + định danh)
    #    chỉ tách khi đứng sau chữ-số (không phá token đang ở đầu).
    s = re.sub(r"(?<=[\w])(?=(?:đ|d|kh|k|m)(?:\d|[ivxlcdm]\b|[a-zđ]\b))", " ", s)
    tokens = s.split()
    out = []
    full = {"điều", "khoản", "điểm", "mục", "điểm."}
    for tk in tokens:
        if tk in full or tk.isdigit() or (len(tk) == 1 and tk.isalpha()):
            out.append(tk); continue
        m = re.fullmatch(r"([đdkm]|kh)\.?([0-9]+|[ivxlcdm]+|[a-zđ])", tk)
        if not m:
            out.append(tk); continue
        head, val = m.group(1), m.group(2)
        if head in ("đ", "d"):
            out.append(f"điều {val}" if val.isdigit() else f"điểm {val}")
        elif head in ("k", "kh"):
            out.append(f"khoản {val}" if val.isdigit() else tk)
        elif head == "m":
            out.append(f"mục {val}")
        else:
            out.append(tk)
    s = " ".join(out)
    s = re.sub(r"\bđiểm\s+([a-zđ])\b", r"điểm \1", s)
    return re.sub(r"\s+", " ", s).strip()


def canonicalize_query(q: str) -> str:
    """Đưa truy vấn TỰ NHIÊN về thứ tự chuẩn của nhãn trong structure[].

    Người Việt hay hỏi 'khoản 2 Điều 7', 'Đ7 K2', 'điểm a khoản 2 Điều 7'
    (đảo thứ tự / viết tắt). Chuẩn hóa về: '<điều N|mục R> [khoản M] [điểm X]'.
    Nếu không nhận ra mẫu điều/mục, trả lại nhãn đã chuẩn hóa nguyên trạng.
    """
    s = _expand_abbrev(_norm_label(q))
    # anchor: 'điều N' hoặc 'mục <số/La Mã>'
    m_dieu = re.search(r"điều\s+(\d+)", s)
    m_muc = re.search(r"mục\s+([ivxlcdm]+|\d+)", s)
    m_khoan = re.search(r"khoản\s+(\d+)", s)
    m_diem = re.search(r"điểm\s+([a-zđ])", s)
    parts = []
    if m_dieu:
        parts.append(f"điều {m_dieu.group(1)}")
    elif m_muc:
        anchor = m_muc.group(1)
        parts.append(f"mục {anchor.upper() if not anchor.isdigit() else anchor}".lower())
    else:
        return s  # không có anchor điều/mục → giữ nguyên
    if m_khoan:
        parts.append(f"khoản {m_khoan.group(1)}")
    if m_diem:
        parts.append(f"điểm {m_diem.group(1)}")
    return " ".join(parts)


def _parse_form_query(q: str) -> tuple[str, str]:
    s = _norm_label(q)
    m = re.search(r"mẫu\s+([a-z]{1,3}\d{2}[a-z]?)", s, flags=re.I)
    if not m:
        return "", ""
    form = f"mẫu {m.group(1).lower()}"
    md = re.search(r"điều\s+(\d+)", s, flags=re.I)
    return form, (f"điều {md.group(1)}" if md else "")


def find_units(doc: dict, query_label: str, exact: bool = False) -> list[dict]:
    """Tìm đơn vị theo nhãn, có chống nhầm Điều thật và Điều nội bộ của Mẫu.

    - 'Điều 7' chỉ tìm level=article/clause/point, KHÔNG trả form_article.
    - 'Mẫu AI09a' trả level=form.
    - 'Mẫu AI09a Điều 7' trả level=form_article neo trong Mẫu đó.
    """
    structure = doc.get("structure", [])
    form, form_dieu = _parse_form_query(query_label)
    hits = []
    if form:
        for u in structure:
            lab = _norm_label(u.get("label", ""))
            lvl = u.get("level", "")
            if form_dieu:
                if lvl == "form_article" and lab == f"{form} {form_dieu}":
                    hits.append(u)
            else:
                if lvl == "form" and lab == form:
                    hits.append(u)
        return hits

    q = canonicalize_query(query_label)
    query_is_article = q.startswith("điều ")
    for u in structure:
        lvl = u.get("level", "")
        if query_is_article and lvl in ("form", "form_article", "appendix", "table"):
            continue
        lab = _norm_label(u.get("label", ""))
        if exact:
            if lab == q:
                hits.append(u)
        else:
            if lab == q or lab.startswith(q + " "):
                hits.append(u)
    return hits


def verify_in_source(text: str, source_full_text: str) -> bool:
    """Kiểm tra text trả về có thật sự là chuỗi con của toàn văn nguồn không."""
    a = re.sub(r"\s+", " ", _norm(text))
    b = re.sub(r"\s+", " ", _norm(source_full_text))
    return a in b if a else False


def format_answer(doc: dict, hits: list[dict], query: str) -> str:
    if not hits:
        return (f"Không tìm thấy '{query}' trong văn bản "
                f"{doc.get('number_symbol') or doc.get('title','')}.\n"
                f"Gợi ý: kiểm tra lại số Điều/Mục, hoặc văn bản chưa nạp đơn vị này.")
    out = []
    head = doc.get("title") or doc.get("number_symbol", "")
    out.append(f"# {head}")
    meta = []
    if doc.get("number_symbol"):
        meta.append(f"Số hiệu: {doc['number_symbol']}")
    if doc.get("issued_date"):
        meta.append(f"Ngày: {doc['issued_date']}")
    if doc.get("effective_status"):
        meta.append(f"Hiệu lực: {doc['effective_status']}")
    if meta:
        out.append("> " + " | ".join(meta))
    out.append("")
    for u in hits:
        title = f" — {u['title']}" if u.get("title") else ""
        out.append(f"## {u['label']}{title}")
        if u.get("text"):
            out.append(u["text"])
        out.append("")
    # nguồn
    src = doc.get("source", {}) or {}
    prov = []
    if src.get("type"):
        prov.append(f"nguồn: {src['type']}")
    if src.get("url"):
        prov.append(src["url"])
    if doc.get("officialness_level"):
        prov.append(f"độ chính thống: {doc['officialness_level']}")
    if prov:
        out.append("---")
        out.append("_" + " · ".join(prov) + "_")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc", nargs="?", help="legal_document.json (bỏ trống nếu dùng --cache-id)")
    ap.add_argument("--cache-id", default="", help="Tra thẳng từ cache theo số ký hiệu/tên")
    ap.add_argument("--cache-dir", default="")
    ap.add_argument("--cite", required=True,
                    help="Nhãn cần tra: 'Điều 7' | 'Đ7 K2' | 'khoản 2 Điều 7' | "
                         "'Điều 7 khoản 2 điểm a' | 'Mục II' | 'Mục II khoản 1'")
    ap.add_argument("--exact", action="store_true", help="Chỉ trả đúng đơn vị, không trả con")
    ap.add_argument("--verify-source", default="",
                    help="File text toàn văn nguồn để kiểm chứng substring (tùy chọn)")
    ap.add_argument("--expected-content-hash", default="",
                    help="Hash từ NotebookLM/bundle mong đợi. Nếu lệch thì dừng, không trả verbatim.")
    ap.add_argument("--allow-stale", action="store_true",
                    help="Cho phép trả kết quả dù expected-content-hash lệch (không khuyến nghị)")
    ap.add_argument("--stale-days", type=int, default=provenance.DEFAULT_STALE_DAYS,
                    help="Ngưỡng ngày coi bản đã ban hành là 'có thể cũ' khi chưa đối chiếu lại")
    ap.add_argument("--no-warnings", action="store_true", help="Tắt khối cảnh báo nguồn/hiệu lực")
    ap.add_argument("--json", action="store_true", help="Xuất JSON thay vì markdown")
    args = ap.parse_args()

    cache_meta = {}
    if args.cache_id:
        from cache import get_doc, get_record
        try:
            doc = get_doc(args.cache_id, args.cache_dir)
        except RuntimeError as e:
            # v1.34.45 (audit merge): find() raises CACHE_IDENTITY_CONFLICT when >1 cached doc shares
            # the query so_hieu (e.g. gốc + VBHN both cached). Fail closed with a clean message/exit
            # code — never a raw traceback, and never guess which verbatim text to return.
            if str(e).startswith("CACHE_IDENTITY_CONFLICT"):
                print(f"CACHE_IDENTITY_CONFLICT cho '{args.cache_id}': cache có nhiều bản trùng số hiệu "
                      f"— không trả nguyên văn khi mơ hồ. Dọn bản trùng hoặc truyền --cache-id chính xác hơn. "
                      f"({e})", file=sys.stderr)
                sys.exit(2)
            raise
        if doc is None:
            print(f"MISS cache cho '{args.cache_id}' — cần tải & chuẩn hóa nguồn trước.",
                  file=sys.stderr)
            sys.exit(2)
        rec = get_record(args.cache_id, args.cache_dir)
        if rec:
            # trục freshness/doc_status sống trên index record, không phải trên doc
            for k in ("verified_at", "verified_against", "doc_status",
                      "consolidation_checked", "fetched_at", "officialness",
                      "source_type", "document_variant"):
                if rec.get(k) not in (None, ""):
                    cache_meta[k] = rec[k]
    elif args.doc:
        doc = read_json(args.doc)
    else:
        sys.exit("Cần truyền doc.json hoặc --cache-id.")

    current_hash = doc.get("text_hash") or doc.get("content_hash") or ""
    if args.expected_content_hash and current_hash and args.expected_content_hash != current_hash and not args.allow_stale:
        payload = {
            "error": "hash_mismatch",
            "message": "Nguồn định vị (NotebookLM/bundle) không khớp cache hiện hành. Cần re-export/re-sync trước khi dùng làm nguyên văn.",
            "expected_content_hash": args.expected_content_hash,
            "current_content_hash": current_hash,
            "number_symbol": doc.get("number_symbol", ""),
            "title": doc.get("title", ""),
        }
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"HASH_MISMATCH: {payload['message']}", file=sys.stderr)
            print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(3)

    hits = find_units(doc, args.cite, exact=args.exact)

    verified = None
    if args.verify_source and hits:
        full = Path(args.verify_source).read_text(encoding="utf-8")
        verified = all(verify_in_source(u["text"], full) for u in hits if u.get("text"))

    # v1.9.8: cảnh báo provenance + freshness (trộn doc + cache record).
    warn_meta = dict(doc)
    warn_meta.update(cache_meta)
    warnings = [] if args.no_warnings else provenance.build_warnings(warn_meta, stale_days=args.stale_days)

    if args.json:
        print(json.dumps({"query": args.cite, "count": len(hits),
                          "verified_in_source": verified,
                          "content_hash": current_hash,
                          "verbatim_status": doc.get("verbatim_status", ""),
                          "warnings": warnings,
                          "units": hits}, ensure_ascii=False, indent=2))
    else:
        print(format_answer(doc, hits, args.cite))
        if verified is not None:
            print(f"\n[kiểm chứng nguồn: {'✅ khớp nguyên văn' if verified else '⚠️ KHÔNG khớp — kiểm tra lại'}]")
        if warnings:
            print(provenance.render_warnings(warnings))


if __name__ == "__main__":
    main()
