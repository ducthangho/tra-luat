#!/usr/bin/env python3
"""ingest_to_cache.py — Cổng nạp toàn văn VBQPPL vào cache theo THỨ TỰ ƯU TIÊN.

Mục tiêu: một đường vào duy nhất, chọn phương án hiệu quả + verbatim nhất hiện có,
parse đúng (docx/text/markdown/pdf/html), KHÓA số hiệu canonical, gắn method +
evidence_status=verified + nlm_source_id, rồi cache.

THỨ TỰ ƯU TIÊN NẠP (ingest priority) — VERIFIED 2026-06-09 (134/2025/QH15: 35 Điều):

  0. CACHE đã có (phiên này)                         -> dùng luôn, 0 chi phí.
  1. DRIVE (Google Doc native), theo độ sạch verbatim & tính sẵn sàng:
       a. Apps Script  exportdocx  -> .docx -> python-docx   (✅ PASS rank 95 — ƯU TIÊN NHẤT)
       b. MCP download_file_content (export DOCX) -> .docx   (✅ PASS rank 94 — FALLBACK 1a fail)
       c. Apps Script  exporttext  -> text/plain             (✅ PASS rank 80 — FALLBACK)
       d. MCP read_file_content     -> markdown              (✅ PASS rank 60 — FALLBACK cuối, fix v1.9.9.10)
  2. URL công khai (whitelist) — định dạng hiệu quả nhất TRƯỚC:
       a. .docx  -> python-docx          (cấu trúc rõ nhất)
       b. .doc   -> convert -> python-docx
       c. .pdf   -> pdfplumber/pypdf
       d. .html  -> bóc nội dung chính    (kém tin cậy nhất, chỉ khi không có file)
  3. NLM (notebook_query) — CHỈ để ĐỊNH VỊ Điều/Khoản, KHÔNG phải trích dẫn chính thức.

Phương án chạy được hoàn toàn trong bash (Claude tự động hoá): 1a, 1c, 2*.
Phương án MCP (1b, 1d) do Claude gọi tool rồi truyền file qua --input (--method tương ứng).

Cách dùng tiêu biểu:
  # 1a — Drive exportdocx (ưu tiên cao nhất khi Apps Script sẵn sàng)
  ingest_to_cache.py --so-hieu 18/VBHN-VPQH --gdoc-id <ID> --nlm-source-id <UUID> \
      --method exportdocx --webapp "$WEBAPP" --token "$TOKEN"
  # 1b/1d/file — đã có file (vd MCP tải về) thì truyền thẳng
  ingest_to_cache.py --so-hieu 18/VBHN-VPQH --input /tmp/x.docx --method download_file_content
  # 2 — URL công khai
  ingest_to_cache.py --so-hieu 79/2025/NĐ-CP --url "https://vbpl.vn/.../vanban.docx" --method url
"""
import argparse, json, os, subprocess, sys, tempfile, urllib.request, urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_CACHE = os.path.expanduser("~/.tra_luat_cache")

# Thứ hạng độ tin cậy verbatim của từng method (cao = sạch hơn) — chỉ để ghi vào metadata.
# v1.9.9.10: Verified bằng test 134/2025/QH15 (35 Điều + 8 Chương):
#  - exportdocx (1a): ✅ PASS (rank 95) — ưu tiên cao nhất, sạch nhất
#  - download_file_content (1b): ✅ PASS (rank 94) — fallback nếu 1a fail, không cần Apps Script
#  - exporttext (1c): ✅ PASS (rank 80) — fallback, nhanh hơn 1a
#  - read_file_content (1d): ✅ PASS after fix (rank 60) — fallback cuối, cần strip markdown
# v1.9.9.11: PDF (CÓ lớp text máy đọc) xếp TRÊN .doc theo cấu hình người dùng.
#   Lý do: .pdf official thường là bản gốc đáng tin, giữ phụ lục/bảng nguyên khối;
#   chỉ XẾP SAU .docx (cấu trúc đoạn rõ nhất). PDF SCAN (không text layer) bị CHẶN
#   ở fetch_url (raise ScannedPDFError) -> KHÔNG bao giờ nạp, chuyển nguồn web khác.
METHOD_RANK = {
    "exportdocx": 95, "download_file_content": 94,
    "exporttext": 80, "read_file_content": 60,
    "url_docx": 90, "url_pdf": 80, "url_doc": 75, "url_html": 40,
    "file": 50, "url": 50,
}


class ScannedPDFError(RuntimeError):
    """PDF không có lớp text máy đọc (bản scan/ảnh). KHÔNG nạp — phải đổi nguồn web khác."""


def pdf_text_layer_chars(path: str, max_pages: int = 5) -> int:
    """Đếm ký tự text trích được từ <= max_pages trang đầu. 0 ~ PDF scan/ảnh."""
    total = 0
    try:
        import pdfplumber  # type: ignore
        with pdfplumber.open(path) as pdf:
            for pg in pdf.pages[:max_pages]:
                total += len((pg.extract_text() or "").strip())
        return total
    except Exception:
        pass
    try:
        from pypdf import PdfReader  # type: ignore
        r = PdfReader(path)
        for pg in r.pages[:max_pages]:
            total += len((pg.extract_text() or "").strip())
    except Exception:
        return total
    return total


def assert_pdf_not_scanned(path: str, min_chars: int = 120) -> None:
    """Chặn PDF scan: < min_chars text trên các trang đầu => coi là scan -> raise.
    Quy tắc cứng (người dùng): PDF scan TUYỆT ĐỐI KHÔNG tải/nạp, đi tìm nguồn khác."""
    n = pdf_text_layer_chars(path)
    if n < min_chars:
        raise ScannedPDFError(
            f"PDF có vẻ là bản SCAN (chỉ {n} ký tự text ở trang đầu). "
            f"KHÔNG nạp theo quy tắc cứng — hãy chuyển sang nguồn web TEXT khác "
            f"(thuvienphapluat .docx > .pdf-text khác > luatvietnam > vbpl/Công báo...).")


def _curl_get(url: str, out_path: str, timeout: int = 180) -> tuple[bool, str, str]:
    """GET có follow-redirect (-L). Trả (ok, content_type, err)."""
    try:
        # -sS: im nhưng vẫn báo lỗi; -L: follow redirect; -w: in content-type ra stderr cuối
        p = subprocess.run(
            ["curl", "-sSL", "--max-time", str(timeout), "-o", out_path,
             "-w", "%{content_type}", url],
            capture_output=True, text=True, timeout=timeout + 10)
        ct = (p.stdout or "").strip()
        if p.returncode != 0:
            return False, ct, (p.stderr or f"curl rc={p.returncode}")
        return True, ct, ""
    except Exception as e:
        return False, "", str(e)


def _appsscript(webapp: str, token: str, action: str, **params) -> dict:
    q = {"token": token, "action": action, **params}
    url = webapp + "?" + urllib.parse.urlencode(q)
    with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as fh:
        tmp = fh.name
    ok, _ct, err = _curl_get(url, tmp)
    if not ok:
        raise RuntimeError(f"Apps Script {action} lỗi: {err}")
    data = json.load(open(tmp))
    os.unlink(tmp)
    if not data.get("ok", False):
        raise RuntimeError(f"Apps Script {action} trả lỗi: {data.get('error')}")
    return data


def fetch_drive_exportdocx(gdoc_id: str, webapp: str, token: str) -> str:
    """1a. Apps Script exportdocx -> .docx (base64) -> file tạm. Trả path .docx."""
    import base64
    data = _appsscript(webapp, token, "exportdocx", fileId=gdoc_id)
    b64 = data.get("b64") or data.get("base64") or ""
    raw = base64.b64decode(b64)
    out = tempfile.mktemp(suffix=".docx")
    open(out, "wb").write(raw)
    return out


def fetch_drive_exporttext(gdoc_id: str, webapp: str, token: str) -> str:
    """1c. Apps Script exporttext -> text -> file .txt. Trả path."""
    data = _appsscript(webapp, token, "exporttext", fileId=gdoc_id)
    txt = data.get("text", "")
    out = tempfile.mktemp(suffix=".txt")
    open(out, "w").write(txt)
    return out


def fetch_drive_convert_docx(file_id: str, webapp: str, token: str) -> str:
    """v1.12.9: file .docx/.doc/.pdf NHỊ PHÂN trên Drive (KHÔNG Google-native) →
    copy_convert sang Google Doc tạm rồi exportdocx. Trả path .docx."""
    data = _appsscript(webapp, token, "copy_convert", fileId=file_id, toType="doc", register="false")
    new_id = (data.get("newId") or data.get("fileId") or data.get("id")
              or (data.get("copied") or {}).get("id"))
    if not new_id:
        raise RuntimeError("copy_convert không trả id GDoc mới")
    return fetch_drive_exportdocx(new_id, webapp, token)


def fetch_url(url: str) -> tuple[str, str]:
    """2. Tải URL -> file tạm, chọn đuôi theo content-type. Trả (path, method_label)."""
    tmp = tempfile.mktemp()
    ok, ct, err = _curl_get(url, tmp)
    if not ok:
        raise RuntimeError(f"Tải URL lỗi: {err}")
    ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
    ctl = ct.lower()
    if ext == ".docx" or "wordprocessingml" in ctl:
        dst, m = tmp + ".docx", "url_docx"
    elif ext == ".doc" or "msword" in ctl:
        dst, m = tmp + ".doc", "url_doc"
    elif ext == ".pdf" or "pdf" in ctl:
        dst, m = tmp + ".pdf", "url_pdf"
    else:
        dst, m = tmp + ".html", "url_html"
    os.rename(tmp, dst)
    if m == "url_pdf":
        assert_pdf_not_scanned(dst)   # PDF scan -> raise ScannedPDFError, đổi nguồn
    return dst, m


def run_normalize(input_path: str, so_hieu: str, title: str, variant: str,
                  cache_dir: str, extra: dict) -> dict:
    """Gọi normalize_document.py (đã vá: VBHN, markdown, full_text) với số hiệu KHÓA."""
    out_json = tempfile.mktemp(suffix=".json")
    cmd = [sys.executable, str(HERE / "normalize_document.py"),
           "--input", input_path, "--out", out_json,
           "--structure-level", "article",          # article = giữ nguyên văn từng Điều
           "--document-variant", variant,
           "--origin", extra.get("origin", "drive"),
           "--source-type", extra.get("source_type", "google_drive"),
           "--cache", "--cache-dir", cache_dir]
    if so_hieu:
        cmd += ["--number-symbol", so_hieu]
    if title:
        cmd += ["--title", title]
    if extra.get("source_url"):
        cmd += ["--source-url", extra["source_url"]]
    if extra.get("issuing_agency"):
        cmd += ["--issuing-agency", extra["issuing_agency"]]
    if extra.get("effective_status"):
        cmd += ["--effective-status", extra["effective_status"]]
    if extra.get("officialness"):
        cmd += ["--officialness-level", extra["officialness"]]
    if extra.get("goc"):
        cmd += ["--goc", extra["goc"]]
    if extra.get("aliases"):
        cmd += ["--aliases", extra["aliases"]]
    if extra.get("as_appendix"):
        cmd += ["--as-appendix"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    sys.stderr.write(p.stderr)
    if p.returncode != 0:
        raise RuntimeError(f"normalize_document lỗi: {p.stdout}\n{p.stderr}")
    return json.load(open(out_json))


def patch_cache_metadata(cache_dir: str, so_hieu: str, method: str,
                         nlm_source_id: str, gdoc_id: str, source_url: str):
    """Gắn method + evidence_status=verified + nlm_source_id vào bản ghi cache vừa tạo."""
    from cache import cache_dir as _cd, find as _find  # type: ignore
    cd = _cd(cache_dir)
    # tìm file .tra-luat.json theo số hiệu
    key = so_hieu.replace("/", "-").lower()
    candidates = [p for p in Path(cd).glob("docs/*.json")] + \
                 [p for p in Path(cd).glob("*.tra-luat.json")]
    target = None
    for f in candidates:
        try:
            d = json.load(open(f))
        except Exception:
            continue
        if (d.get("number_symbol", "").replace("/", "-").lower() == key
                or d.get("so_hieu", "").replace("/", "-").lower() == key):
            target = f
            break
    if not target:
        # fallback: file mới nhất
        if candidates:
            target = max(candidates, key=lambda p: p.stat().st_mtime)
    if not target:
        return None
    d = json.load(open(target))
    src = d.get("source", {}) or {}
    src.update({"method": method, "method_rank": METHOD_RANK.get(method, 50)})
    if gdoc_id:
        src["gdoc_id"] = gdoc_id
    if source_url:
        src["url"] = source_url
    d["source"] = src
    d["evidence_status"] = "verified"
    if nlm_source_id:
        d["nlm_source_id"] = nlm_source_id
    if so_hieu:
        d["so_hieu"] = so_hieu
    json.dump(d, open(target, "w"), ensure_ascii=False, indent=2)
    return str(target)


def main():
    ap = argparse.ArgumentParser(description="Nạp toàn văn VBQPPL vào cache theo thứ tự ưu tiên.")
    ap.add_argument("--so-hieu", required=True, help="Số hiệu canonical, vd 18/VBHN-VPQH")
    ap.add_argument("--method", default="auto",
                    choices=["auto", "exportdocx", "exporttext", "download_file_content",
                             "read_file_content", "url", "file"],
                    help="Phương án nạp. auto: thử exportdocx->exporttext (cần --gdoc-id+webapp).")
    ap.add_argument("--input", default="", help="File đã tải sẵn (docx/doc/pdf/html/txt/md).")
    ap.add_argument("--gdoc-id", default="", help="Google Doc id (cho exportdocx/exporttext).")
    ap.add_argument("--url", default="", help="URL công khai (method=url).")
    ap.add_argument("--webapp", default="", help="Apps Script WebApp URL.")
    ap.add_argument("--token", default="", help="Apps Script token.")
    ap.add_argument("--nlm-source-id", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--variant", default="consolidated")
    ap.add_argument("--cache-dir", default=DEFAULT_CACHE)
    ap.add_argument("--issuing-agency", default="")
    ap.add_argument("--effective-status", default="in_force")
    ap.add_argument("--officialness", default="official")
    ap.add_argument("--goc", default="", help="VBHN: chuỗi số hiệu gốc+sđbs, phân tách ';' (vd 81-2021-ND-CP;104-2022-ND-CP;97-2023-ND-CP)")
    ap.add_argument("--aliases", default="", help="Số hiệu tra cứu bổ sung, ';'. Bỏ trống => tự lấy từ --goc.")
    ap.add_argument("--vbhn-first", action="store_true",
                    help="Nếu số hiệu đã bị VBHN còn hiệu lực hợp nhất (vb_status) => NẠP VBHN thay thế.")
    ap.add_argument("--as-appendix", action="store_true",
                    help="Văn bản CHỈ là phụ lục/mẫu (không có Điều nghị định): lưu nguyên khối phu_luc, không ép thành Điều.")
    args = ap.parse_args()
    sys.path.insert(0, str(HERE))
    # B3: tự nạp webapp/token như `tl` nếu chưa truyền — env TL_WEBAPP/TL_TOKEN, rồi config (key `webappUrl`/`token`,
    # KHÔNG phải `webapp`). Bỏ pain phải truyền tay --webapp/--token + nhầm tên key.
    if not args.webapp or not args.token:
        args.webapp = args.webapp or os.environ.get("TL_WEBAPP") or ""
        args.token = args.token or os.environ.get("TL_TOKEN") or ""
        if not args.webapp or not args.token:
            for _p in [os.environ.get("TL_CONFIG"), os.path.expanduser("~/.tra_luat_config.json"),
                       str(HERE.parent / "tra_luat_config.v2.json"), "/tmp/tra_luat_config.json"]:
                if _p and os.path.exists(_p):
                    try:
                        _c = json.load(open(_p, encoding="utf-8"))
                    except Exception:
                        continue
                    args.webapp = args.webapp or _c.get("webappUrl") or _c.get("TL_WEBAPP") or _c.get("webapp") or ""
                    args.token = args.token or _c.get("token") or _c.get("TL_TOKEN") or ""
                    if args.webapp and args.token:
                        break
    # Tự nhận diện file phụ lục theo số hiệu/tiêu đề
    _ap_hint = (args.so_hieu + " " + args.title).lower()
    if any(k in _ap_hint for k in ("phu_luc", "phu luc", "phuluc", "phụ lục", "-pl", "_pl")):
        args.as_appendix = True

    # ----- VBHN-FIRST: số hiệu bị thay thế => chuyển hướng nạp VBHN hợp nhất -----
    redirect_note = None
    if args.vbhn_first and args.webapp:
        try:
            vs = _appsscript(args.webapp, args.token, "vb_status", sohieu=args.so_hieu)
            live = [v for v in (vs.get("superseded_by") or [])
                    if str(v.get("hieuluc", "")).strip().lower().startswith("còn hiệu lực")
                    and v.get("drive_id")]
            if live:
                v = live[0]
                orig = args.so_hieu
                args.aliases = ";".join(x for x in [args.aliases, orig] if x)
                args.so_hieu = v.get("sohieu") or args.so_hieu
                args.gdoc_id = v.get("drive_id")
                args.nlm_source_id = v.get("nlm_source_id") or args.nlm_source_id
                args.effective_status = "Còn hiệu lực"
                if args.method in ("url", "file"):
                    args.method = "auto"
                args.input = ""
                redirect_note = f"VBHN-first: '{orig}' đã bị VBHN '{args.so_hieu}' (còn hiệu lực) hợp nhất ⇒ NẠP VBHN thay thế (gdoc={args.gdoc_id})."
                sys.stderr.write("[ingest] " + redirect_note + "\n")
        except Exception as e:
            sys.stderr.write(f"[ingest] vbhn-first bỏ qua (vb_status lỗi: {e})\n")

    method = args.method
    input_path = args.input
    src_url = args.url

    # ----- Lấy file theo thứ tự ưu tiên -----
    if input_path:
        if method in ("auto", "url"):
            method = "file"
        if input_path.lower().endswith(".pdf"):
            assert_pdf_not_scanned(input_path)   # PDF scan -> raise, đổi nguồn
    elif method in ("auto", "exportdocx") and args.gdoc_id and args.webapp:
        try:
            input_path = fetch_drive_exportdocx(args.gdoc_id, args.webapp, args.token)
            method = "exportdocx"
        except Exception as e:
            msg = str(e).lower()
            if "native" in msg or "403" in msg:
                sys.stderr.write(f"[ingest] exportdocx 403/không-native ({e}); copy_convert→GDoc rồi exportdocx...\n")
                input_path = fetch_drive_convert_docx(args.gdoc_id, args.webapp, args.token)
                method = "exportdocx"
            else:
                sys.stderr.write(f"[ingest] exportdocx lỗi ({e}); thử exporttext...\n")
                input_path = fetch_drive_exporttext(args.gdoc_id, args.webapp, args.token)
                method = "exporttext"
    elif method == "exporttext" and args.gdoc_id and args.webapp:
        input_path = fetch_drive_exporttext(args.gdoc_id, args.webapp, args.token)
    elif method == "url" and src_url:
        input_path, method = fetch_url(src_url)
    else:
        ap.error("Thiếu nguồn: cần --input, hoặc --gdoc-id+--webapp, hoặc --url.")

    # ----- Parse + cache (normalize đã vá VBHN/markdown/full_text) -----
    # Tự suy aliases từ goc nếu không truyền tường minh (để tra số gốc/sđbs trúng VBHN).
    goc = args.goc.strip()
    aliases = args.aliases.strip()
    if goc and not aliases:
        aliases = ";".join(s.strip() for s in goc.split(";") if s.strip())
    extra = {
        "origin": "fetch_url" if src_url else "drive",
        "source_type": "fetch_url" if src_url else "google_drive",
        "source_url": src_url,
        "issuing_agency": args.issuing_agency,
        "effective_status": args.effective_status,
        "officialness": args.officialness,
        "goc": goc,
        "aliases": aliases,
        "as_appendix": args.as_appendix,
    }
    run_normalize(input_path, args.so_hieu, args.title, args.variant, args.cache_dir, extra)
    target = patch_cache_metadata(args.cache_dir, args.so_hieu, method,
                                  args.nlm_source_id, args.gdoc_id, src_url)

    d = json.load(open(target)) if target else {}
    arts = d.get("articles", {})
    n_arts = len(arts) if isinstance(arts, dict) else len(arts or [])
    print(json.dumps({
        "ok": True, "so_hieu": d.get("so_hieu") or args.so_hieu,
        "method": method, "method_rank": METHOD_RANK.get(method, 50),
        "evidence_status": d.get("evidence_status"),
        "effective_status": d.get("document_status") or d.get("effective_status"),
        "aliases": d.get("aliases", []),
        "n_articles": n_arts,
        "redirected": redirect_note,
        "nlm_source_id": d.get("nlm_source_id", ""),
        "cache_file": target,
    }, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except ScannedPDFError as e:
        print(json.dumps({"ok": False, "reason": "scanned_pdf",
                          "action": "switch_source", "message": str(e)},
                         ensure_ascii=False))
        sys.exit(5)   # exit 5 = PDF scan, đổi nguồn web khác
