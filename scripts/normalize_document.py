#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize_document.py — Chuẩn hóa văn bản → doc record schema tra-luat-bundle/1.9 + cập nhật cache.
Bản tự đủ v1.9.14, tương thích CHÍNH XÁC interface mà ingest_to_cache.py::run_normalize gọi:
  --input --out --structure-level article --document-variant V --origin O --source-type S
  --cache --cache-dir D [--number-symbol] [--title] [--source-url] [--issuing-agency]
  [--effective-status] [--officialness-level]
Hỗ trợ input: .txt/.md (utf-8), .html (strip thẻ), .docx (python-docx nếu có, fallback unzip xml),
.pdf (pdftotext — KHÔNG convert OCR; trang scan sẽ thiếu và bị verify bắt), .doc (antiword nếu có).
Parse Điều chịu dính dòng (cùng regex verify_deep). Tự chạy T1 verify; coverage ghi trung thực.
"""
import argparse, hashlib, json, re, subprocess, sys, datetime, html as _html
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_deep import split_articles, t1_structure, ROMAN_PAT, extract_appendix, appendix_start  # noqa: E402
from keywords import extract_keywords  # noqa: E402  (v1.13.4: bắt tukhoa tất định lúc ingest)


def _clean_md_artifacts(t: str) -> str:
    """v1.15.2: làm sạch artifact của Google Docs read_file_content/markdown export
    (chỉ kích hoạt khi PHÁT HIỆN artifact ⇒ giữ nguyên hành vi với input đã sạch):
      - thực thể xuống dòng &#10; / &#xA; -> \\n  (để có whitespace TRƯỚC 'Điều N.')
      - bỏ backslash thoát markdown:  \\* \\. \\- \\[ \\] ...
      - bỏ chú thích/link footnote kiểu [\\[1\\]](url) và [1] sót lại
      - bỏ dấu nhấn ** / * (để ký tự trước 'Điều' là whitespace, không phải '*')
      - bỏ viền bảng markdown | và dòng phân tách |---|---|
    Nếu không vá, regex tách Điều (ART_SPLIT) trượt vì 'Điều' đứng sau '*' và không có newline."""
    has_artifacts = ("&#10;" in t) or ("\\*" in t) or ("](http" in t) \
        or ("**" in t) or bool(re.search(r"(?m)^\s*\|", t))
    if not has_artifacts:
        return t
    t = t.replace("&#10;", "\n").replace("&#xA;", "\n").replace("&#xa;", "\n")
    t = re.sub(r"\\([*_~`\[\]()#+.\-])", r"\1", t)            # unescape md punctuation
    t = re.sub(r"\[\s*\[?\d+\]?\s*\]\([^)]*\)", "", t)         # footnote link refs
    t = re.sub(r"(?<![\w])\[\d+\]", "", t)                     # [1] residues
    t = re.sub(r"\*{1,3}", "", t)                              # strip bold/italic asterisks
    t = re.sub(r"(?m)^\s*\|", "", t)                           # left table border
    t = re.sub(r"(?m)\|\s*$", "", t)                           # right table border
    t = re.sub(r"(?m)^\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)*$", "", t)  # table separator rows
    t = t.replace(" | ", "  ")
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t


def _docx_to_text(path: str) -> str:
    """Bóc text từ .docx GIỮ THỨ TỰ tài liệu, bao gồm CẢ bảng (w:tbl).

    Vá lỗi v1.15.6: trước đây dùng `docx.Document(path).paragraphs` — chỉ lấy
    đoạn văn, BỎ QUA bảng ⇒ phụ lục dạng bảng bị rớt khỏi text (vd Phụ lục IV
    'Danh mục ngành, nghề ĐTKD có điều kiện' của Luật Đầu tư). Hệ quả:
    `appendix_start`/`phu_luc` mất nguyên Phụ lục IV, đối chiếu sai (tưởng vắng
    ngành nghề). Nay duyệt body theo THỨ TỰ tài liệu, lấy cả w:p và w:tbl, để
    phụ lục bảng nằm đúng vị trí (sau thân) và `appendix_start` bắt được.
    """
    try:
        import docx  # type: ignore
        from docx.oxml.ns import qn
        from docx.table import Table
        from docx.text.paragraph import Paragraph
        doc = docx.Document(path)
        out: list[str] = []
        for child in doc.element.body.iterchildren():
            tag = child.tag
            if tag == qn("w:p"):
                out.append(Paragraph(child, doc).text)
            elif tag == qn("w:tbl"):
                for row in Table(child, doc).rows:
                    prev = None
                    cells = []
                    for c in row.cells:           # ô gộp (merge) trả lặp -> khử trùng liền kề
                        txt = c.text.strip()
                        if txt != prev:
                            cells.append(txt)
                        prev = txt
                    out.append("\t".join(cells))
        return "\n".join(out)
    except ImportError:
        import zipfile
        xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8", "replace")
        # GIỮ bảng: xuống dòng theo đoạn & hàng bảng, tab giữa ô
        xml = (xml.replace("</w:p>", "\n")
                  .replace("</w:tr>", "\n")
                  .replace("</w:tc>", "\t"))
        return _html.unescape(re.sub(r"<[^>]+>", "", xml))


def read_input(p: str) -> str:
    path = Path(p); ext = path.suffix.lower()
    if ext in (".txt", ".md"):
        return _clean_md_artifacts(path.read_text(encoding="utf-8", errors="replace"))
    if ext in (".html", ".htm"):
        h = path.read_text(encoding="utf-8", errors="replace")
        h = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)
        h = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</tr>", "\n", h)
        return _html.unescape(re.sub(r"(?s)<[^>]+>", " ", h))
    if ext == ".docx":
        return _docx_to_text(str(path))
    if ext == ".pdf":
        r = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            raise RuntimeError("pdftotext lỗi: " + r.stderr[:300])
        return r.stdout
    if ext == ".doc":
        for cmd in (["antiword", str(path)], ["catdoc", str(path)]):
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if r.returncode == 0 and len(r.stdout) > 200:
                    return r.stdout
            except FileNotFoundError:
                continue
        raise RuntimeError(".doc cần antiword/catdoc, hoặc convert .doc→.docx trước")
    raise RuntimeError(f"Định dạng chưa hỗ trợ: {ext}")


def doc_key_of(so_hieu: str, variant: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", so_hieu.lower()).strip("-") + "--" + variant


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--structure-level", default="article")
    ap.add_argument("--document-variant", default="original")
    ap.add_argument("--origin", default="drive")
    ap.add_argument("--source-type", default="google_drive")
    ap.add_argument("--cache", action="store_true")
    ap.add_argument("--cache-dir", default=str(Path.home() / ".tra_luat_cache"))
    ap.add_argument("--number-symbol", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--source-url", default="")
    ap.add_argument("--issuing-agency", default="")
    ap.add_argument("--effective-status", default="")
    ap.add_argument("--officialness-level", default="official")
    ap.add_argument("--goc", default="", help="VBHN: số hiệu gốc + sđbs, phân tách ';'")
    ap.add_argument("--aliases", default="", help="Số hiệu tra cứu bổ sung, phân tách ';'")
    ap.add_argument("--as-appendix", action="store_true",
                    help="Văn bản CHỈ là phụ lục/mẫu: lưu nguyên khối phu_luc, không ép thành Điều, không FATAL.")
    a = ap.parse_args()

    raw = read_input(a.input).replace("\r\n", "\n")
    if a.as_appendix:
        # v1.12.9: nạp văn bản PHỤ LỤC/MẪU độc lập — lưu nguyên khối, không yêu cầu Điều.
        body = ""           # không phân tích thân
        phu_luc = raw.strip()
        arts = split_articles(raw)   # giữ Điều nội bộ của mẫu (nếu có), KHÔNG bắt buộc
        rep = {"flags": ["APPENDIX: nạp dạng phụ lục/mẫu — không kiểm cấu trúc Điều nghị định"]}
        rep["t1"] = {"tier": "T1", "ok": True, "fatal": False, "articles_found": len(arts)}
        coverage = "appendix_only"
        a.document_variant = "appendix"
    else:
        # v1.12.8: TÁCH phụ lục TRƯỚC — phân tích cấu trúc chỉ trên phần THÂN (body),
        # tránh mẫu/biểu trong phụ lục bơm "Điều"/"Chương" giả gây T1 FATAL sai.
        _ap = appendix_start(raw)
        body = raw[:_ap] if _ap >= 0 else raw
        phu_luc = raw[_ap:].strip() if _ap >= 0 else ""
        arts = split_articles(body)
        if not arts:
            print(json.dumps({"error": "Không tách được Điều nào — kiểm tra nguồn "
                              "(nếu là phụ lục/mẫu độc lập, dùng --as-appendix)"}, ensure_ascii=False))
            sys.exit(2)
        # T1 nội bộ → coverage trung thực (chạy trên body, không gồm phụ lục)
        rep = {"flags": []}
        t1_structure(body, 0, a.number_symbol, rep)
        t1 = rep["t1"]
        if t1.get("fatal"):
            print(json.dumps({"error": "T1 FATAL: " + "; ".join(rep["flags"]),
                              "hint": "QUARANTINE — không nạp"}, ensure_ascii=False))
            sys.exit(2)
        coverage = "complete_vs_independent" if not rep["flags"] else (
            "partial: " + " | ".join(rep["flags"])[:400])

    nums = sorted(arts)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    norm = re.sub(r"[ \t]+", " ", raw).strip()
    so_hieu = a.number_symbol or "UNKNOWN"
    key = doc_key_of(so_hieu, a.document_variant)
    record = {
        "schema": "tra-luat-bundle/1.9",
        "doc_key": key, "so_hieu": so_hieu, "number_symbol": so_hieu,
        "title": a.title, "variant": a.document_variant,
        "goc": a.goc, "aliases": [s for s in a.aliases.split(";") if s],
        "issuing_agency": a.issuing_agency, "document_status": a.effective_status,
        "provenance": a.officialness_level, "officialness": a.officialness_level,
        "source": {"origin": a.origin, "source_type": a.source_type, "url": a.source_url,
                   "input_file": str(Path(a.input).name)},
        "text_hash": hashlib.sha256(norm.encode()).hexdigest(), "chars": len(raw),
        "structure": {"chapters": len(ROMAN_PAT.findall(body)),
                      "articles": len(nums), "terminal_article": (nums[-1] if nums else 0),
                      "has_phu_luc": bool(phu_luc), "phu_luc_chars": len(phu_luc),
                      "is_appendix": bool(getattr(a, "as_appendix", False))},
        "coverage": coverage, "verify_flags": rep["flags"],
        "verified_at": now, "ingested_at": now,
        "articles": {str(n): arts[n] for n in nums},
        "has_phu_luc": bool(phu_luc),
        "phu_luc": phu_luc,
    }
    # v1.13.4: MÓC CHỦ ĐỀ tất định (Chương/Điều) — KHÔNG AI, idempotent. Để Claude lọc-thô
    # chọn nguồn trước khi notebook_query. Danh tính (so_hieu/loai/linhvuc) đã là cột riêng.
    record["tukhoa"] = extract_keywords(record)
    Path(a.out).write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")

    if a.cache:
        cd = Path(a.cache_dir); (cd / "docs").mkdir(parents=True, exist_ok=True)
        (cd / "docs" / f"{key}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
        bi_p = cd / "bundle_index.json"
        bi = json.loads(bi_p.read_text(encoding="utf-8")) if bi_p.exists() else \
            {"schema": "tra-luat-bundle/1.9", "docs": []}
        bi["docs"] = [d for d in bi["docs"] if d.get("doc_key") != key]
        bi["docs"].append({k: record[k] for k in
                           ("doc_key", "so_hieu", "title", "variant", "text_hash",
                            "coverage", "verified_at")} | {"aliases": record["aliases"]})
        bi["generatedAt"] = now
        bi_p.write_text(json.dumps(bi, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"ok": True, "doc_key": key, "articles": len(nums),
                      "coverage": coverage}, ensure_ascii=False))


if __name__ == "__main__":
    main()
