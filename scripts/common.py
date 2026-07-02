#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, unquote

SOURCE_RULES = {
    "vbpl": ("official", 1),
    "congbao": ("official", 1),
    "official_portal": ("official", 1),
    "google_drive": ("needs_manual_check", 3),
    "thuvienphapluat": ("secondary", 2),
    "luatvietnam": ("secondary", 2),
    "uploaded_file": ("needs_manual_check", 3),
    "aitracuuluat": ("secondary", 2),
    "dangcongsan": ("official", 1),
    "other": ("needs_manual_check", 4),
}

DOC_TYPES = ["Hiến pháp", "Bộ luật", "Luật", "Pháp lệnh", "Nghị quyết", "Nghị định",
             "Thông tư", "Quyết định", "Chỉ thị", "Kết luận", "Văn kiện",
             "Báo cáo chính trị"]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def guess_source_type(url: str | None) -> str:
    if not url:
        return "uploaded_file"
    host = urlparse(url).netloc.lower()
    if "vbpl.vn" in host:
        return "vbpl"
    if "congbao" in host or host.endswith("congbao.chinhphu.vn"):
        return "congbao"
    if "thuvienphapluat" in host:
        return "thuvienphapluat"
    if "luatvietnam" in host:
        return "luatvietnam"
    if "dangcongsan" in host:
        return "dangcongsan"
    if host.endswith(".gov.vn") or host.endswith(".chinhphu.vn"):
        return "official_portal"
    if "drive.google.com" in host or "docs.google.com" in host:
        return "google_drive"
    return "other"


def source_meta(source_type: str) -> tuple[str, int]:
    return SOURCE_RULES.get(source_type, SOURCE_RULES["other"])


def guess_file_format(path: str | Path, content_type: str = "") -> str:
    ext = Path(path).suffix.lower().lstrip(".")
    if ext in {"docx", "doc"}:
        return "docx"
    if ext == "pdf":
        return "pdf"
    if ext in {"htm", "html"}:
        return "html"
    if ext in {"txt", "md", "json"}:
        return "text"
    ct = (content_type or "").lower()
    if "pdf" in ct:
        return "pdf"
    if "word" in ct or "officedocument" in ct or "msword" in ct:
        return "docx"
    if "html" in ct:
        return "html"
    return "text"


def safe_filename(name: str, default: str = "source") -> str:
    name = unquote(name or default)
    name = re.sub(r"[^\w\-.()\[\] àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]+", "_", name, flags=re.I)
    return name.strip("._ ")[:180] or default


def strip_markdown_artifacts(s: str) -> str:
    """Gỡ rác markdown khi nguồn là Google Doc -> markdown (vd qua read_file_content):
    bảng `| :-: |`, escape `\\*`, `\\.`, entity `&#10;`, bullet/heading. Trả text thuần
    để split_structure bóc Điều/Khoản chuẩn. An toàn với text không phải markdown.
    
    v1.9.9.10 (FIX): LUÔN loại bỏ **...** markers ở bất cứ đâu
    - Cách cũ giữ **Điều 1...** làm parser không nhận diện (lỗi!)
    - Bây giờ: **Điều 1...** → Điều 1... (loại bỏ ** nhưng GIỮ text bên trong)
    - Áp dụng cho tất cả dòng, không phân loại structure vs non-structure
    """
    if not s:
        return ""
    s = s.replace("&#10;", "\n").replace("&amp;", "&").replace("&nbsp;", " ")
    # Hàng phân cách bảng markdown: | :-: | :-: |
    s = re.sub(r"^\s*\|[\s:\-\|]+\|\s*$", "", s, flags=re.M)
    # Ô bảng: bỏ ký tự pipe ở đầu/cuối dòng và gộp cell bằng khoảng trắng
    s = re.sub(r"^\s*\|(.*)\|\s*$", lambda m: m.group(1).replace("|", " "), s, flags=re.M)
    # Heading markdown (#, ##...) -> bỏ dấu #
    s = re.sub(r"^\s*#{1,6}\s*", "", s, flags=re.M)
    # Escape của markdown: \* \_ \. \- \( \) \[ \]  -> ký tự gốc
    s = re.sub(r"\\([\*\_\.\-\(\)\[\]\#\+`~])", r"\1", s)
    
    # **BOLD** COMPLETE STRIP (v1.9.9.10 FIX):
    # Luôn loại bỏ **...** từ BẤT CỨ đâu (đầu dòng, giữa dòng, ...)
    # VD: **Điều 1. Phạm vi** → Điều 1. Phạm vi
    s = re.sub(r'\*\*([^*]*)\*\*', r'\1', s)  # Strip **...**
    s = re.sub(r'__([^_]*)__', r'\1', s)      # Strip __...__
    # Các dạng markdown khác
    s = re.sub(r'_([^_]+)_', r'\1', s)        # Strip _italic_
    s = re.sub(r'\*([^*]+)\*', r'\1', s)      # Strip *italic* (nếu còn)
    
    # Dọn khoảng trắng thừa
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s


def looks_like_markdown(s: str) -> bool:
    """Phát hiện text có rác markdown (bảng/escape/entity) cần strip_markdown_artifacts."""
    if not s:
        return False
    sample = s[:5000]
    signals = 0
    if re.search(r"\|\s*:-:", sample):       signals += 1   # bảng căn giữa
    if "&#10;" in sample:                     signals += 1   # entity xuống dòng
    if re.search(r"\\\*|\\\.", sample):       signals += 1   # escape \* \.
    if re.search(r"^\s*\|.*\|\s*$", sample, flags=re.M): signals += 1
    return signals >= 2


def clean_text(s: str) -> str:
    s = re.sub(r"\r\n?", "\n", s or "")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def read_json(path: str | Path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_json(obj, path: str | Path):
    # Ghi ATOMIC: viết ra file tạm + fsync rồi os.replace (rename nguyên tử trên cùng
    # filesystem). Tránh index.json/cache bị cụt nếu tiến trình bị ngắt giữa chừng.
    import os as _os
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.parent / (p.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
        fh.flush()
        try:
            _os.fsync(fh.fileno())
        except Exception:
            pass
    _os.replace(str(tmp), str(p))


def infer_type(title: str) -> str:
    t = (title or "").strip().lower()
    for label in DOC_TYPES:
        if t.startswith(label.lower()):
            return label
    for label in DOC_TYPES:
        if re.search(r"\b" + re.escape(label.lower()) + r"\b", t):
            return label
    return ""


def infer_body_type(doc_type: str, issuing_agency: str = "", title: str = "") -> str:
    combined = f"{doc_type} {issuing_agency} {title}".lower()
    if "hội đồng nhân dân" in combined or "hđnd" in combined:
        return "HDND"
    if "ủy ban nhân dân" in combined or "uỷ ban nhân dân" in combined or "ubnd" in combined:
        return "UBND"
    return "OTHER"


def convert_doc_to_docx_if_needed(path: str | Path) -> Path:
    """Convert legacy .doc to .docx with LibreOffice if available. Returns original if not needed or failed."""
    path = Path(path)
    if path.suffix.lower() != ".doc":
        return path
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return path
    with tempfile.TemporaryDirectory() as td:
        try:
            subprocess.run([soffice, "--headless", "--convert-to", "docx", "--outdir", td, str(path)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            converted = Path(td) / (path.stem + ".docx")
            if converted.exists():
                out = path.with_suffix(".converted.docx")
                shutil.copy2(converted, out)
                return out
        except Exception:
            return path
    return path


def infer_verbatim_status(source_type: str, officialness_level: str = "", file_format: str = "") -> str:
    """Mức tin cậy của nguyên văn đã trích.

    official_verified: nguồn chính thức hoặc cổng Đảng/chính phủ/quốc hội, đủ dùng
      để trả nguyên văn sau khi parser/substring verify.
    secondary_html: nguồn phụ trợ/thương mại/MCP đủ để định vị, cần đối chiếu khi
      dùng làm trích dẫn pháp lý chính thức.
    uploaded_unverified: file người dùng/Drive chưa xác minh nguồn gốc.
    ocr_unverified: PDF/upload có thể qua OCR/trích text, cần kiểm lại file gốc.
    """
    st = (source_type or "").lower()
    off = (officialness_level or "").lower()
    fmt = (file_format or "").lower()
    if st in {"vbpl", "congbao", "official_portal", "dangcongsan"} or off == "official":
        return "official_verified"
    if st in {"luatvietnam", "thuvienphapluat", "aitracuuluat"} or off == "secondary":
        return "secondary_html"
    if fmt == "pdf" and st in {"uploaded_file", "google_drive", "other", ""}:
        return "ocr_unverified"
    return "uploaded_unverified"
