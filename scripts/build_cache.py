#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_cache.py — bọc normalize_document logic, viết cache record CHUẨN (schema 1.9),
nhưng xử lý trung thực 2 lớp false-positive đã được verify_deep adjudicate trong phiên:
  1) NFC-normalize input (vô hại, đúng chuẩn verbatim) → sửa Điều heading dạng NFD.
  2) --declared-articles: bỏ qua số Điều > terminal thật (do trích dẫn sửa đổi luật khác).
  3) Điều bị 'missing' chỉ được tính là CÓ MẶT nếu xác nhận tombstone bãi bỏ
     'Điều N ... (được|bị) bãi bỏ' THỰC SỰ tồn tại trong nguồn → coverage=partial (trung thực),
     KHÔNG quarantine. Không hề sửa nội dung pháp lý.
Ghi cache vào <cache-dir>/docs/<key>.json + cập nhật bundle_index.json y như normalize_document.py.
"""
import argparse, hashlib, json, re, sys, datetime, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent / "scripts"
sys.path.insert(0, str(HERE))
from verify_deep import split_articles, t1_structure, ROMAN_PAT  # noqa: E402

FOOTNOTE = re.compile(r"\[\d+\]")
def tombstone_present(raw, n):
    # Xác nhận Điều n tồn tại dưới dạng tombstone bãi bỏ trong nguồn (NFC).
    pat = re.compile(r"Điều\s*%d\b[^\n]{0,40}?(được|bị)\s+bãi\s+bỏ" % n, re.IGNORECASE)
    return bool(pat.search(raw))

def doc_key_of(so_hieu, variant):
    return re.sub(r"[^a-z0-9]+", "-", so_hieu.lower()).strip("-") + "--" + variant

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--number-symbol", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--document-variant", default="original")
    ap.add_argument("--goc", default="")
    ap.add_argument("--aliases", default="")
    ap.add_argument("--declared-articles", type=int, default=0)
    ap.add_argument("--origin", default="drive")
    ap.add_argument("--source-type", default="google_drive")
    a = ap.parse_args()

    raw0 = Path(a.input).read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    raw = unicodedata.normalize("NFC", raw0)              # (1) lossless
    struct_text = FOOTNOTE.sub("", raw)                   # bỏ [n] CHỈ cho dò cấu trúc

    arts = split_articles(struct_text)
    if not arts:
        print(json.dumps({"error": "Không tách được Điều nào"}, ensure_ascii=False)); sys.exit(2)
    nums = sorted(arts)

    declared = a.declared_articles or nums[-1]
    raw_missing = [i for i in range(1, declared + 1) if i not in arts]
    # (3) lọc tombstone đã xác nhận tồn tại
    tomb = [n for n in raw_missing if tombstone_present(struct_text, n)]
    real_missing = [n for n in raw_missing if n not in tomb]

    flags = []
    if tomb:
        flags.append(f"T1: Điều {tomb} là tombstone '(được bãi bỏ)' — CÓ trong nguồn, đầy đủ dạng đã-bãi-bỏ")
    if real_missing:
        flags.append(f"T1-FATAL: thiếu thật Điều {real_missing}")
        print(json.dumps({"error": "; ".join(flags), "hint": "QUARANTINE — không nạp"},
                         ensure_ascii=False)); sys.exit(2)
    # cảnh báo cơ học số hiệu (không chặn)
    if a.number_symbol and a.number_symbol not in raw[:2000] \
       and a.number_symbol.replace("-", "/") not in raw[:2000]:
        flags.append(f"T1-nhẹ: số '{a.number_symbol}' không thấy trong 2000 ký tự đầu (cosmetic)")
    if declared < nums[-1]:
        flags.append(f"T1-nhẹ: có số Điều > {declared} (vd {nums[-1]}) — trích dẫn sửa đổi luật khác, đã bỏ qua theo declared")

    coverage = "complete_vs_independent" if not flags else "partial: " + " | ".join(flags)[:400]
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    norm = re.sub(r"[ \t]+", " ", raw).strip()
    key = doc_key_of(a.number_symbol, a.document_variant)
    record = {
        "schema": "tra-luat-bundle/1.9",
        "doc_key": key, "so_hieu": a.number_symbol, "number_symbol": a.number_symbol,
        "title": a.title, "variant": a.document_variant,
        "goc": a.goc, "aliases": [s for s in a.aliases.split(";") if s],
        "issuing_agency": "", "document_status": "", "provenance": "official", "officialness": "official",
        "source": {"origin": a.origin, "source_type": a.source_type, "url": "",
                   "input_file": Path(a.input).name},
        "text_hash": hashlib.sha256(norm.encode()).hexdigest(), "chars": len(raw),
        "structure": {"chapters": len(ROMAN_PAT.findall(raw)),
                      "articles": len(nums), "terminal_article": nums[-1],
                      "declared_articles": declared, "tombstone_repealed": tomb},
        "coverage": coverage, "verify_flags": flags,
        "verified_at": now, "ingested_at": now,
        "articles": {str(n): arts[n] for n in nums},
    }
    cd = Path(a.cache_dir); (cd / "docs").mkdir(parents=True, exist_ok=True)
    (cd / "docs" / f"{key}.json").write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    bi_p = cd / "bundle_index.json"
    bi = json.loads(bi_p.read_text(encoding="utf-8")) if bi_p.exists() else {"schema": "tra-luat-bundle/1.9", "docs": []}
    bi["docs"] = [d for d in bi["docs"] if d.get("doc_key") != key]
    bi["docs"].append({k: record[k] for k in ("doc_key", "so_hieu", "title", "variant",
                       "text_hash", "coverage", "verified_at")} | {"aliases": record["aliases"]})
    bi["generatedAt"] = now
    bi_p.write_text(json.dumps(bi, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"ok": True, "doc_key": key, "articles": len(nums),
                      "terminal": nums[-1], "declared": declared,
                      "tombstone_repealed": tomb, "coverage": coverage}, ensure_ascii=False))

if __name__ == "__main__":
    main()
