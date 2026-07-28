#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docx_markup.py — v1.35.12 (r182): XỬ LÝ MARKUP SỬA ĐỔI (tracked changes) trong .docx.

BẤT BIẾN NGHIỆP VỤ (lỗi ĐÚNG-SAI về nội dung pháp luật):
  · w:del / w:delText / w:moveFrom  → chữ ĐÃ BỎ  ⇒ KHÔNG được đọc như quy phạm còn hiệu lực.
  · w:strike / w:dstrike            → chữ ĐÃ BỎ (gạch ngang thủ công, KHÔNG dùng track-changes).
  · w:ins / w:moveTo                → chữ MỚI THÊM ⇒ PHẢI đọc.
  · w:rPrChange / w:pPrChange       → BẢN GHI ĐỊNH DẠNG CŨ, không phải nội dung ⇒ bỏ (và phải bỏ TRƯỚC
    khi dò strike, vì rPrChange lưu w:strike CŨ ⇒ dễ tưởng run hiện tại bị gạch).

Trước r182 cả 3 reader sản xuất đều đọc SAI: nhánh python-docx của normalize_document GIỮ chữ gạch
ngang và MẤT chữ w:ins (python-docx bỏ run không phải con TRỰC TIẾP của w:p); hai nhánh strip-tag
(`_docx_unzip_text` của `tl doc-text`/`tl extract`, `_profile_read_probe_text` của cổng nạp) giữ CẢ
w:delText — tức đọc dự thảo sai CẢ HAI CHIỀU.

THIẾT KẾ: chỉ CẮT/BÓC TAG cấu trúc markup trên chuỗi `word/document.xml`, KHÔNG đụng gì khác ⇒ tài
liệu KHÔNG có markup thì xml ra = xml vào (bytes) ⇒ mọi corpus đã nạp GIỮ NGUYÊN text_hash. Đây là
bất biến được ca `r182_no_markup_xml_unchanged` khoá.

Zero-dependency (chỉ stdlib) — dùng được cả từ normalize_document.py (script tự đủ) lẫn tl_core qua
`_imp("docx_markup")`.
"""
import html as _html
import re

__all__ = ["MODES", "MARK_OPEN", "MARK_CLOSE", "has_markup", "scan", "scan_file", "strip_markup",
           "warn_line", "resolve_mode", "xml_chunk_text", "chunk_payload"]

MARK_OPEN = "⟦BỎ:"
MARK_CLOSE = "⟧"
MODES = ("auto", "strip", "mark", "raw")

# Dấu hiệu nhanh: không có chuỗi nào trong đây ⇒ tài liệu sạch markup ⇒ đường tắt, khỏi regex.
_HINTS = ("<w:del", "<w:ins", "<w:strike", "<w:dstrike", "<w:moveFrom", "<w:moveTo",
          "<w:delText", "<w:rPrChange", "<w:pPrChange")

# Bản ghi ĐỊNH DẠNG CŨ — phải quét sạch TRƯỚC khi dò strike (xem docstring).
_RE_PRCHANGE = re.compile(r"<w:(rPrChange|pPrChange)\b[^>]*(?:/>|>.*?</w:\1>)", re.S)
# Khối chữ ĐÃ BỎ (không lồng nhau trong OOXML) + dạng tự đóng (đánh dấu xoá dấu-đoạn/ô).
_RE_DROP = re.compile(r"<w:(del|moveFrom)\b[^>]*(?:/>|>.*?</w:\1>)", re.S)
# Chữ MỚI THÊM: chỉ BÓC vỏ, giữ nguyên ruột.
_RE_UNWRAP = re.compile(r"</?w:(?:ins|moveTo)\b[^>]*/?>")
# delText lạc ngoài w:del (docx sinh bởi công cụ lạ) — lưới phụ.
_RE_DELTEXT = re.compile(r"<w:delText\b[^>]*>.*?</w:delText>", re.S)
_RE_RUN = re.compile(r"<w:r\b[^>]*>.*?</w:r>", re.S)
# Ruột text THẬT của mẩu xml (w:t/w:delText). `\b` chặn khớp nhầm <w:tab/>.
_RE_TEXTEL = re.compile(r"<w:(t|delText)\b[^>]*>(.*?)</w:\1>", re.S)
_RE_RPR = re.compile(r"<w:rPr\b[^>]*>.*?</w:rPr>", re.S)
_RE_STRIKE = re.compile(r"<w:(?:d)?strike\b[^>]*/?>")
_RE_VAL = re.compile(r'w:val\s*=\s*"([^"]*)"')
_RE_TAG = re.compile(r"<[^>]+>")
_RE_SOFTBREAK = re.compile(r"<w:(?:tab|br|cr)\b[^>]*/?>")
_OFF = {"0", "false", "off", "none"}


def _strike_on(run_xml: str) -> bool:
    """Run có bị gạch ngang KHÔNG? Chỉ xét w:rPr CỦA CHÍNH run; `w:val="false"` = ĐÈ TẮT (không gạch)."""
    m = _RE_RPR.search(run_xml)
    if not m:
        return False
    for s in _RE_STRIKE.finditer(m.group(0)):
        v = _RE_VAL.search(s.group(0))
        if v is None or v.group(1).strip().lower() not in _OFF:
            return True
    return False


def xml_chunk_text(chunk: str) -> str:
    """Chữ THUẦN của một mẩu xml (để dựng nhãn ⟦BỎ:…⟧)."""
    t = _RE_SOFTBREAK.sub(" ", chunk)
    t = _html.unescape(_RE_TAG.sub("", t))
    return re.sub(r"\s+", " ", t).strip()


def chunk_payload(chunk: str) -> str:
    """v1.35.58 (r222) — chữ THÔ của mẩu xml: CHỈ ruột w:t/w:delText (tab/br/cr = một dấu cách),
    GIỮ NGUYÊN khoảng trắng. Khác `xml_chunk_text` đúng ở chỗ r222 cần: `xml_chunk_text` nén rồi
    `.strip()` nên trả "" cho CẢ mẩu RỖNG HẲN lẫn mẩu CHỈ-KHOẢNG-TRẮNG — mà hai thứ đó phải xử lý
    NGƯỢC nhau (xem `strip_markup._keep_space`). Chỉ đọc trong w:t/w:delText, không phải mọi text
    lọt giữa tag, để docx bị in đẹp (xuống dòng giữa các tag) không bị hiểu nhầm là có khoảng trắng."""
    x = _RE_SOFTBREAK.sub("<w:t> </w:t>", chunk or "")
    return "".join(_html.unescape(m.group(2)) for m in _RE_TEXTEL.finditer(x))


def has_markup(xml: str) -> bool:
    """Có dấu hiệu markup sửa đổi không (rẻ, dùng làm đường tắt giữ nguyên hành vi cũ)."""
    return any(h in (xml or "") for h in _HINTS)


def scan(xml: str) -> dict:
    """Đếm markup theo THỂ. Thuần đọc, không sửa chuỗi."""
    x = xml or ""
    st = {"del": 0, "ins": 0, "strike": 0, "move_from": 0, "move_to": 0, "pr_change": 0}
    if not has_markup(x):
        return st
    st["pr_change"] = len(_RE_PRCHANGE.findall(x))
    clean = _RE_PRCHANGE.sub("", x)
    for m in _RE_DROP.finditer(clean):
        st["del" if m.group(1) == "del" else "move_from"] += 1
    st["ins"] = len(re.findall(r"<w:ins\b[^>]*>", clean))
    st["move_to"] = len(re.findall(r"<w:moveTo\b[^>]*>", clean))
    st["strike"] = sum(1 for r in _RE_RUN.finditer(_RE_DROP.sub("", clean)) if _strike_on(r.group(0)))
    return st


def scan_file(path) -> dict:
    """Đếm markup của MỘT file .docx (thuần đọc). Không mở được/không phải docx → mọi thể = 0."""
    import zipfile
    try:
        from tl_core.ingest_engine import read_member_bounded   # r188 SEC-01: chống zip-bomb
        with zipfile.ZipFile(path) as z:
            return scan(read_member_bounded(z, "word/document.xml").decode("utf-8", "replace"))
    except Exception:  # noqa: BLE001 — docx hỏng/mã hoá/không phải zip/vượt trần → coi như sạch markup
        return scan("")


def resolve_mode(mode: str, *, is_draft: bool) -> str:
    """`auto` = ĐÁNH DẤU cho DỰ THẢO (người rà cần thấy chữ nào bị đề nghị bỏ), LOẠI HẲN cho VBQPPL đã
    ban hành (văn bản ban hành không được lẫn chữ đã bỏ)."""
    m = (mode or "auto").strip().lower()
    if m not in MODES:
        raise ValueError(f"markup mode không hợp lệ: {mode!r} (chọn {'/'.join(MODES)})")
    if m != "auto":
        return m
    return "mark" if is_draft else "strip"


def strip_markup(xml: str, mode: str = "strip") -> tuple:
    """Trả (xml_đã_xử_lý, stats). mode: strip=loại hẳn · mark=thay bằng ⟦BỎ:…⟧ · raw=giữ nguyên (hành vi
    TRƯỚC r182, chỉ để đối chứng). Tài liệu sạch markup ⇒ trả CHÍNH chuỗi vào (bất biến no-op).

    v1.35.58 (r222): mẩu bị bỏ mà ruột CHỈ có khoảng trắng thì GIỮ khoảng trắng ở MỌI chế độ (kể cả
    `mark`: nhãn ⟦BỎ: ⟧ vừa là rác vừa không phải nội dung bị bỏ) — xem `_keep_space`."""
    x = xml or ""
    st = scan(x)
    if mode == "raw" or not has_markup(x):
        return x, st

    def _label(m):
        """Nhãn ⟦BỎ:…⟧ phải là phần tử w:t THẬT: python-docx CHỈ nối w:t, chèn text trần thì nhánh
        lib đánh rơi nhãn (đo được r182) — trong khi nhánh strip-tag lại giữ. Escape XML để chuỗi có
        &/</> không phá cây (nhánh strip-tag unescape ở bước cuối nên round-trip khớp)."""
        t = xml_chunk_text(m.group(0))
        if not t:
            return ""
        t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<w:t xml:space="preserve">{MARK_OPEN}{t}{MARK_CLOSE}</w:t>'

    def _keep_space(m):
        """v1.35.58 (r222) — mẩu bị bỏ mà ruột CHỈ có khoảng trắng thì trả CHÍNH khoảng trắng đó,
        ngược lại trả None (= bỏ như cũ). Đo 28-07 trên `19-2026-VBHN-VPQH` @121.553: nguồn viết
        `[run 'hủy bỏ quyết định tuyên bố mất tích'] + [run STRIKE ' '] + [run 'quyết định…']`, bỏ
        cả run giữa ⇒ raw 187.401 vs strip 187.399 ⇒ **«hủy bỏquyết định»** — công cụ ĐẺ RA một chữ
        không có trong văn bản. DẤU CÁCH bị gạch là TÀN DƯ ĐỊNH DẠNG, không phải «chữ đã bỏ» theo
        nghĩa nghiệp vụ: bỏ chữ thì mất nội dung, bỏ dấu cách thì SINH nội dung — hại hơn.
        ★Vế `pay and` KHÔNG thừa, nhưng lý do KHÔNG phải «đẻ dấu cách ma» — đo bằng đột biến M2 của
        r222: bỏ vế đó thì mẩu rỗng trả `""`, mà `"" is not None` nên sinh ra `<w:t></w:t>` RỖNG, tức
        VĂN BẢN không đổi (mọi ca đo theo text đều xanh — chốt trông như mã chết). Khác biệt thật ở
        mức XML: `<w:del …/>` tự đóng (đánh dấu xoá DẤU-ĐOẠN) có ở mọi docx track-changes, nên bỏ vế
        này là chèn một run rỗng vào MỌI ranh giới đoạn — phá bất biến thiết kế của module («chỉ
        CẮT/BÓC tag markup, KHÔNG đụng gì khác», cùng họ với `r182_no_markup_is_noop`). Ca khoá phải
        so ở mức XML mới giết được M2."""
        pay = chunk_payload(m.group(0))
        return pay if (pay and not pay.strip()) else None

    def _cut_block(m):
        """Chỗ thay là cấp INLINE trong w:p (w:del / w:moveFrom / w:r) → bọc trong w:r cho hợp lệ."""
        sp = _keep_space(m)
        if sp is not None:
            return f'<w:r><w:t xml:space="preserve">{sp}</w:t></w:r>'
        if mode != "mark":
            return ""
        lb = _label(m)
        return f"<w:r>{lb}</w:r>" if lb else ""

    def _cut_inline(m):
        """delText lạc nằm SẴN trong w:r → chỉ thay bằng w:t (bọc w:r nữa sẽ lồng run, sai lược đồ)."""
        sp = _keep_space(m)
        if sp is not None:
            return f'<w:t xml:space="preserve">{sp}</w:t>'
        return _label(m) if mode == "mark" else ""

    x = _RE_PRCHANGE.sub("", x)          # (1) bản ghi định dạng cũ — TRƯỚC khi dò strike
    x = _RE_DROP.sub(_cut_block, x)      # (2) w:del / w:moveFrom → chữ ĐÃ BỎ
    x = _RE_RUN.sub(lambda m: _cut_block(m) if _strike_on(m.group(0)) else m.group(0), x)   # (3) gạch ngang
    x = _RE_UNWRAP.sub("", x)            # (4) w:ins / w:moveTo → BÓC VỎ, GIỮ CHỮ
    x = _RE_DELTEXT.sub(_cut_inline, x)  # (5) lưới phụ: delText lạc
    return x, st


def warn_line(stats: dict, where: str = "") -> str:
    """Câu cảnh báo 1 dòng (rỗng nếu tài liệu sạch). Caller in ra stderr."""
    st = stats or {}
    if not any(st.get(k) for k in ("del", "ins", "strike", "move_from", "move_to")):
        return ""
    bits = [f"{k}={st[k]}" for k in ("del", "strike", "move_from", "ins", "move_to") if st.get(k)]
    return (f"[docx-markup] ⚠ {where or 'tài liệu'} CÓ MARKUP SỬA ĐỔI ({', '.join(bits)}) — "
            "đây là DỰ THẢO đang sửa: chữ w:del/gạch-ngang ĐÃ BỎ, w:ins là chữ MỚI THÊM. "
            "KHÔNG trích dẫn như quy phạm hiện hành khi chưa đối chiếu bản ban hành.")
