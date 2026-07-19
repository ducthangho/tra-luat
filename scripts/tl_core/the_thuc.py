# -*- coding: utf-8 -*-
"""tl_core.the_thuc — R2 v1.34.75 (kế hoạch `ke-hoach-the-thuc-2026-07-19.md`, user duyệt 6/6 grill):
`tl the-thuc-check <docx>` — kiểm THỂ THỨC file .docx PURE OFFLINE, stdlib-only (zipfile + xml.etree;
KHÔNG python-docx — bất biến zero-dependency; docx = zip, đọc word/document.xml + word/styles.xml).

4+1 hệ tiêu chí (nguồn số: `references/THE_THUC_TRINH_BAY.md` — NEO-DRIFT-LOCK, r136 khóa 2 chiều
`the_thuc_neo_lines()` == block trong reference; đổi 1 phía là selftest đỏ):
  hanh_chinh — NĐ 30/2020 PL I · vbqppl — NĐ 78/2025 Đ60-71 + PL I NĐ 187/2025 (PL NĐ78 bị thay toàn bộ)
  vbqppl_qh — NQ 351/2017/UBTVQH14 (VẪN HIỆU LỰC cho QH/UBTVQH/CTN, user xác nhận 2026-07-19; thân 14
  CỐ ĐỊNH; lề 20-25/20-25/30-35/15-20 mm từ sơ đồ Mẫu PDF Công báo — v1.34.76 áp FAIL) · vbhn —
  NĐ 250/2026 (font/lề kế thừa vbqppl) · dang — QĐ 399-QĐ/TW + HD 05-HD/VPTW (lề đơn trị 20/20/30/15).

Resolve font/cỡ BẮT BUỘC fallback 3 tầng run → style Normal → docDefaults (mổ XML 19-07: file convert
GDoc để trống run — ND187 0 thẻ rFonts); ET parser thật nên miễn nhiễm bẫy whitespace `<w:sz ... />`.
Đa section: kiểm lề từng sectPr; section landscape → WARN TT-TRINH-BAY-NGANG, bỏ kiểm lề section đó
(NĐ30/NĐ187 Mục I.2 cho phép chiều rộng khi có bảng biểu). twips→mm = ×25,4/1440, dung sai ±1mm; cỡ
chữ pt = w:sz/2 (tiếng Việt = Latin script → w:sz, KHÔNG w:szCs).

Hàm rebase lên namespace tl (khuôn I1/I2) — import stdlib đặt TRONG THÂN HÀM (sau rebase __globals__
là tl, không phải module này); hằng tiêu chí sống trong `_the_thuc_criteria()` (hàm, né bẫy I11
re-export hằng)."""
from __future__ import annotations

_TL = None


def bind(tl_module) -> None:
    """REBASE __globals__ từng hàm đã chuyển về namespace SỐNG của tl (khuôn I1/I2)."""
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


def _the_thuc_criteria():
    """Bảng tiêu chí 4+1 hệ + normalize — NGUỒN SỰ THẬT phía code, render lại NGUYÊN VĂN 6 dòng
    NEO-DRIFT-LOCK của references/THE_THUC_TRINH_BAY.md (r136 so ==; thứ tự key = thứ tự trong dòng).
    Giá trị dạng chuỗi "lo-hi" | "n" (đơn trị) | "na" (không kiểm FAIL — NQ351 lề theo phụ lục sơ đồ)."""
    return {
        "hanh_chinh": {
            "le_tren_mm": "20-25", "le_duoi_mm": "20-25", "le_trai_mm": "30-35", "le_phai_mm": "15-20",
            "font": "Times New Roman", "co_noi_dung": "13-14", "so_trang": "13-14", "quoc_hieu": "12-13",
            "tieu_ngu": "13-14", "so_ky_hieu": "13", "noi_nhan_tu": "12", "noi_nhan_ds": "11",
            "thut_dau_dong_cm": "1-1.27", "doan_pt_min": "6", "dong_max_lines": "1.5"},
        "vbqppl": {
            "le_tren_mm": "15-20", "le_duoi_mm": "15-20", "le_trai_mm": "30-35", "le_phai_mm": "15-20",
            "font": "Times New Roman", "co_noi_dung": "13-14", "so_trang": "13", "quoc_hieu": "12-13",
            "ten_luat": "14", "can_cu": "14", "chuc_vu_ky": "13", "noi_nhan_ds": "11",
            "thut_dau_dong_cm": "1-1.27", "doan_pt_min": "6", "dong_max_lines": "1.5"},
        "vbqppl_qh": {
            "le_tren_mm": "20-25", "le_duoi_mm": "20-25", "le_trai_mm": "30-35", "le_phai_mm": "15-20",
            "font": "Times New Roman", "co_noi_dung": "14-14", "so_trang": "13", "quoc_hieu": "12-12",
            "tieu_ngu": "14-14", "so_ky_hieu": "13", "can_cu": "14", "chuc_vu_ky": "13",
            "noi_nhan_tu": "12", "noi_nhan_ds": "11", "thut_dau_dong_cm": "1-1.27", "doan_pt_min": "6",
            "dong_min": "don_hoac_15pt"},
        "vbhn": {
            "ke_thua": "vbqppl", "so_trang": "13-14", "ky_hieu": "STT/NAM/VBHN-loai-cq",
            "can_co": "liet_ke_vb,chu_thich_chan_trang,khoi_xac_thuc"},
        "dang": {
            "le_tren_mm": "20", "le_duoi_mm": "20", "le_trai_mm": "30", "le_phai_mm": "15",
            "font": "Times New Roman", "co_noi_dung": "14-15", "tieu_de": "15", "the_loai": "15-16",
            "so_ky_hieu": "14", "noi_nhan_tu": "14", "noi_nhan_ds": "12", "lien_he": "10",
            "ky_hieu_soan": "11", "so_trang": "14", "line_pt": "18-22", "thut_dau_dong_mm": "10",
            "doan_pt_min": "6"},
        "normalize": {
            "le": "20/20/30/15", "font": "Times New Roman", "sz_nha_nuoc": "13", "sz_dang": "14"},
    }


def the_thuc_neo_lines():
    """Render 6 dòng NEO-DRIFT-LOCK từ hằng — r136 so == block trong THE_THUC_TRINH_BAY.md."""
    c = _the_thuc_criteria()
    return [k + ": " + " ".join(f"{a}={b}" for a, b in c[k].items())
            for k in ("hanh_chinh", "vbqppl", "vbqppl_qh", "vbhn", "dang", "normalize")]


def _tt_range(spec):
    """'20-25' → (20.0, 25.0); '13' → (13.0, 13.0); 'na'/None → None. Dấu '-' chỉ tách khi cả 2 vế là số."""
    if not spec or spec == "na":
        return None
    s = str(spec)
    if "-" in s:
        lo, _, hi = s.partition("-")
        try:
            return (float(lo), float(hi))
        except ValueError:
            return None
    try:
        v = float(s)
        return (v, v)
    except ValueError:
        return None


def _tt_mm(twips):
    """twips → mm (1 mm = 1440/25,4 twips). None-safe."""
    if twips is None:
        return None
    return twips * 25.4 / 1440.0


def _the_thuc_parse_docx(path):
    """Đọc docx (zip): sections (pgSz/pgMar/orient), docDefaults + style Normal (font, sz half-points),
    runs [(font|None, sz|None, len_text)], text (mỗi paragraph 1 dòng). ET namespace đầy đủ — miễn
    nhiễm khác biệt whitespace giữa công cụ sinh XML."""
    import zipfile
    import xml.etree.ElementTree as ET
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(path) as z:
        doc = z.read("word/document.xml").decode("utf-8", "replace")
        try:
            sty = z.read("word/styles.xml").decode("utf-8", "replace")
        except KeyError:
            sty = ""
        try:
            fnx = z.read("word/footnotes.xml").decode("utf-8", "replace")   # chú thích chân trang (VBHN!)
        except KeyError:
            fnx = ""
    droot = ET.fromstring(doc)
    footnotes = ""
    if fnx:
        try:
            froot = ET.fromstring(fnx)
            footnotes = "\n".join(
                "".join((t.text or "") for t in fn.iter(W + "t")) for fn in froot.iter(W + "footnote"))
        except ET.ParseError:
            footnotes = ""

    def _gi(el, attr):
        if el is None:
            return None
        v = el.get(W + attr)
        try:
            return int(v)
        except (TypeError, ValueError):
            return None

    sections = []
    for sp in droot.iter(W + "sectPr"):
        pg = sp.find(W + "pgSz")
        mar = sp.find(W + "pgMar")
        sections.append({
            "w": _gi(pg, "w"), "h": _gi(pg, "h"),
            "orient": (pg.get(W + "orient") if pg is not None else None),
            "top": _gi(mar, "top"), "bottom": _gi(mar, "bottom"),
            "left": _gi(mar, "left"), "right": _gi(mar, "right")})

    def _rpr_font_sz(rpr):
        f = s = None
        if rpr is not None:
            rf = rpr.find(W + "rFonts")
            if rf is not None:
                f = rf.get(W + "ascii") or rf.get(W + "hAnsi")
            sz = rpr.find(W + "sz")
            if sz is not None:
                try:
                    s = int(sz.get(W + "val"))
                except (TypeError, ValueError):
                    s = None
        return f, s

    defaults = {"font": None, "sz": None}
    normal = {"font": None, "sz": None}
    if sty:
        sroot = ET.fromstring(sty)
        dd = sroot.find(f"{W}docDefaults/{W}rPrDefault/{W}rPr")
        defaults["font"], defaults["sz"] = _rpr_font_sz(dd)
        for st in sroot.iter(W + "style"):
            if st.get(W + "styleId") == "Normal":
                normal["font"], normal["sz"] = _rpr_font_sz(st.find(W + "rPr"))
                break

    runs = []
    paras = []
    for p in droot.iter(W + "p"):
        ppr = p.find(W + "pPr")
        ind_fl = sp_line = None
        sp_rule = None
        if ppr is not None:
            iel = ppr.find(W + "ind")
            if iel is not None:
                try:
                    ind_fl = int(iel.get(W + "firstLine"))
                except (TypeError, ValueError):
                    ind_fl = None
            sel = ppr.find(W + "spacing")
            if sel is not None:
                sp_rule = sel.get(W + "lineRule")
                try:
                    sp_line = int(sel.get(W + "line"))
                except (TypeError, ValueError):
                    sp_line = None
        ptxt = []
        pszs = {}                      # sz RESOLVED (run→Normal→docDefaults) → số chữ, per-paragraph (T3 bậc)
        for r in p.iter(W + "r"):
            rt = "".join((t.text or "") for t in r.iter(W + "t"))
            f, s = _rpr_font_sz(r.find(W + "rPr"))
            if rt:
                runs.append((f, s, len(rt)))
                ptxt.append(rt)
                se = s if s is not None else (normal["sz"] if normal["sz"] is not None else defaults["sz"])
                if se is not None:
                    pszs[se] = pszs.get(se, 0) + len(rt)
        if ptxt:
            paras.append({"text": "".join(ptxt), "ind": ind_fl, "line": sp_line, "rule": sp_rule, "szs": pszs})
    return {"sections": sections, "defaults": defaults, "normal": normal,
            "runs": runs, "text": "\n".join(p["text"] for p in paras), "paras": paras,
            "footnotes": footnotes}


def _the_thuc_detect_he(text):
    """Phân luồng hệ theo §1 THE_THUC_TRINH_BAY.md: dang → vbhn → vbqppl (nhánh _qh nếu ký hiệu
    QH/UBTVQH/CTN hoặc tên loại LUẬT/BỘ LUẬT/PHÁP LỆNH) → hanh_chinh."""
    import re
    head = (text or "")[:4000]
    if "ĐẢNG CỘNG SẢN VIỆT NAM" in head and "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" not in head:
        return "dang"
    # r140 (v1.34.80): chỉ nhận SỐ KÝ HIỆU CỦA CHÍNH VB — anchored đầu dòng "(<loại> )Số:"; công văn
    # VIỆN DẪN "…Nghị định số 30/2020/NĐ-CP ngày…" giữa câu KHÔNG được làm lệch hệ (demo 1.5 bắt được).
    _SO = r"(?m)^\s*(?:(?:Bộ\s+luật|Luật|Pháp\s+lệnh|Lệnh|Nghị\s+quyết|Nghị\s+định|Quyết\s+định|Thông\s+tư)\s+)?[Ss]ố\s*:\s*"
    if re.search(_SO + r"\d+/(?:\d{4}/)?VBHN-", head):   # nhận cả dạng CŨ n/VBHN-CQ (vd 4231/VBHN-BTP)
        return "vbhn"
    if re.search(_SO + r"\d+/\d{4}/[A-ZĐ]", head):
        if (re.search(r"/(QH|UBTVQH)\d+\b|/CTN\b", head)
                or re.search(r"(?m)^\s*(BỘ\s+)?LUẬT\s*$|^\s*PHÁP\s+LỆNH\s*$", head)):
            return "vbqppl_qh"
        return "vbqppl"
    return "hanh_chinh"


def _the_thuc_check_t2(text, he_eff, add, footnotes=""):
    """T2 (R3 v1.34.77) — hiện diện CẤU TRÚC bằng regex trên text bóc: thành phần bắt buộc theo hệ
    (Đ8 k2 NĐ30 / Đ71 k2 NĐ78 / Đ15 QĐ399), số ký hiệu đúng cú-pháp-hệ (bẫy chéo Đảng↔nhà nước),
    checklist VBHN (NĐ250), dấu sao + 5 gạch VB Đảng (HD05). Thiếu bắt buộc = FAIL; thành phần
    heuristic/điều-kiện = WARN."""
    import re
    t = text or ""
    head = t[:4000]
    CAN9 = {"hanh_chinh": "NĐ 30/2020 Đ8 k2 — 9 thành phần chính",
            "vbqppl": "NĐ 78/2025 Đ71 k2 — thành phần chính (địa danh/nơi nhận: nếu có)",
            "vbqppl_qh": "NĐ 78/2025 Đ71 k2 + NQ 351/2017 Chương II",
            "vbhn": "NĐ 250/2026 Phụ lục — thể thức văn bản hợp nhất",
            "dang": "QĐ 399-QĐ/TW Đ15 — 9 thành phần bắt buộc"}
    can9 = CAN9[he_eff]
    nha_nuoc = he_eff in ("hanh_chinh", "vbqppl", "vbqppl_qh", "vbhn")
    if nha_nuoc:
        if "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" not in head:
            add("TT-QUOC-HIEU", "FAIL", "không thấy Quốc hiệu",
                "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM (trên cùng bên phải trang đầu)", can9)
        if not re.search(r"Độc lập\s*-\s*Tự do\s*-\s*Hạnh phúc", head):
            add("TT-TIEU-NGU", "FAIL", "không thấy Tiêu ngữ",
                "Độc lập - Tự do - Hạnh phúc (dưới Quốc hiệu, có đường kẻ ngang)", can9)
    elif "ĐẢNG CỘNG SẢN VIỆT NAM" not in head:
        add("TT-TIEU-DE-DANG", "FAIL", "không thấy tiêu đề",
            "ĐẢNG CỘNG SẢN VIỆT NAM (góc phải dòng đầu, in hoa 15 đậm)", can9)
    SK = {
        "hanh_chinh": (r"Số:\s*\d+\s*/\s*[A-ZĐ][\wĐ]*(?:-[\wĐ]+)*",
                       "Số: <n>/<viết tắt loại>-<viết tắt CQ> — PL I NĐ30 Mục II.3"),
        "vbqppl": (r"[Ss]ố:\s*\d+/\d{4}/[A-ZĐ]", "<n>/<năm>/<ký hiệu> — PL I NĐ187 Phần II.3"),
        "vbqppl_qh": (r"[Ss]ố:\s*\d+/\d{4}/[A-ZĐ]", "<n>/<năm>/<ký hiệu> — NQ 351/2017 Đ32"),
        "vbhn": (r"Số:\s*\d+/(?:\d{4}/)?VBHN-", "…/VBHN-… — NĐ250 PL II.1 (dạng cũ không năm hợp lệ trước 01/7/2026)"),
        "dang": (r"Số\s+\d+\s*-\s*[A-ZĐ]+/[A-ZĐ]+", "Số <n>-<loại>/<CQ>, KHÔNG dấu hai chấm — HD05 mục 3.2"),
    }
    pat, exp = SK[he_eff]
    if not re.search(pat, head):
        meas = "không khớp cú pháp hệ " + he_eff
        if he_eff == "dang" and re.search(r"Số:\s*\d+/", head):
            meas = "dùng cú pháp nhà nước 'Số: n/LOẠI-CQ' trong văn bản Đảng"
        elif nha_nuoc and re.search(r"Số\s+\d+\s*-[A-ZĐ]+/", head):
            meas = "dùng cú pháp Đảng 'Số n-LOẠI/CQ' trong văn bản nhà nước"
        add("TT-SO-KY-HIEU", "FAIL", meas, exp, can9)
    if not re.search(r",\s*ngày\s+\d{1,2}\s+tháng\s+\d{1,2}\s+năm\s+\d{4}", head):
        lvl = "WARN" if he_eff in ("vbqppl", "vbqppl_qh") else "FAIL"   # Đ71: địa danh (nếu có); luật ghi thời điểm thông qua cuối VB
        add("TT-DIA-DANH-NGAY", lvl, "không thấy '<địa danh>, ngày … tháng … năm …'",
            "vd: Hà Nội, ngày 05 tháng 01 năm 2026", can9)
    if he_eff in ("hanh_chinh", "dang") and not re.search(r"Nơi nhận\s*:", t):
        add("TT-NOI-NHAN", "FAIL", "không thấy 'Nơi nhận:'", "khối Nơi nhận cuối văn bản", can9)
    elif he_eff == "vbqppl" and not re.search(r"Nơi nhận\s*:", t):
        add("TT-NOI-NHAN", "WARN", "không thấy 'Nơi nhận:' (Đ71 k2: nếu có)", "khối Nơi nhận", can9)
    LOAI_NN = (r"(NGHỊ QUYẾT|QUYẾT ĐỊNH|CHỈ THỊ|QUY CHẾ|QUY ĐỊNH|THÔNG CÁO|THÔNG BÁO|HƯỚNG DẪN|CHƯƠNG TRÌNH"
               r"|KẾ HOẠCH|PHƯƠNG ÁN|ĐỀ ÁN|DỰ ÁN|BÁO CÁO|BIÊN BẢN|TỜ TRÌNH|HỢP ĐỒNG|CÔNG ĐIỆN|GIẤY MỜI"
               r"|GIẤY GIỚI THIỆU|GIẤY NGHỈ PHÉP|PHIẾU GỬI|PHIẾU CHUYỂN|PHIẾU BÁO|NGHỊ ĐỊNH|THÔNG TƯ"
               r"|BỘ LUẬT|LUẬT|PHÁP LỆNH|LỆNH|CÔNG VĂN)")
    LOAI_DANG = (r"(CƯƠNG LĨNH|ĐIỀU LỆ|CHIẾN LƯỢC|NGHỊ QUYẾT|QUYẾT ĐỊNH|CHỈ THỊ|KẾT LUẬN|QUY CHẾ|QUY ĐỊNH"
                 r"|THÔNG TRI|HƯỚNG DẪN|THÔNG BÁO|THÔNG CÁO|TUYÊN BỐ|LỜI KÊU GỌI|BÁO CÁO|KẾ HOẠCH|QUY HOẠCH"
                 r"|CHƯƠNG TRÌNH|ĐỀ ÁN|PHƯƠNG ÁN|DỰ ÁN|TỜ TRÌNH|CÔNG VĂN|BIÊN BẢN)")
    if he_eff == "hanh_chinh" and not (re.search(LOAI_NN, head) or "V/v" in head):
        add("TT-TEN-LOAI", "WARN", "không nhận diện tên loại (hoặc trích yếu công văn 'V/v')",
            "tên loại in hoa đậm 13-14 / công văn: 'V/v …'", can9)
    if he_eff == "dang" and not re.search(LOAI_DANG, head):
        add("TT-TEN-LOAI", "WARN", "không nhận diện thể loại trong 25 thể loại", "thể loại in hoa 15-16 đậm — Đ5 QĐ399", can9)
    if not re.search(r"(TM\.|KT\.|TL\.|TUQ\.|Q\.|T/M\b|CHỦ TỊCH|PHÓ CHỦ TỊCH|BỘ TRƯỞNG|THỨ TRƯỞNG|THỦ TƯỚNG"
                     r"|PHÓ THỦ TƯỚNG|CHÁNH VĂN PHÒNG|PHÓ CHÁNH VĂN PHÒNG|CHÁNH ÁN|VIỆN TRƯỞNG|TỔNG THƯ KÝ"
                     r"|TỔNG BÍ THƯ|BÍ THƯ|PHÓ BÍ THƯ|GIÁM ĐỐC|TRƯỞNG BAN)", t):
        add("TT-CHUC-VU-KY", "WARN", "không nhận diện quyền hạn/chức vụ người ký",
            "TM./KT./TL./TUQ. hoặc chức danh in hoa (VB Đảng: T/M)", can9)
    if he_eff in ("vbqppl", "vbqppl_qh", "vbhn") and "Căn cứ" not in t:
        add("TT-CAN-CU", "WARN", "không thấy 'Căn cứ …'", "căn cứ ban hành, in thường 14 nghiêng", can9)
    if he_eff == "dang":
        if "*" not in head[:2500]:
            add("TT-DANG-SAO", "FAIL", "không thấy dấu sao (*) dưới tên cơ quan",
                "dấu * ngăn tên cơ quan với số ký hiệu — HD05 mục 2", can9)
        if not re.search(r"-{5,}", t):
            add("TT-DANG-5GACH", "FAIL", "không thấy 5 dấu gạch nối '-----'",
                "5 gạch ngăn trích yếu với nội dung — HD05 mục 5", can9)
    if he_eff == "vbhn":
        n_vb = len(re.findall(r"[Ss]ố\s+\d+/\d{4}/", head))
        if n_vb < 2:
            add("TT-VBHN-LIET-KE", "FAIL", f"chỉ thấy {n_vb} tham chiếu 'số n/năm/…' phần đầu",
                "liệt kê ≥2 văn bản được hợp nhất ngay sau tên — NĐ250 mục II.2", can9)
        t_fn = t + "\n" + (footnotes or "")               # chú thích chân trang docx nằm word/footnotes.xml
        if re.search(r"sửa đổi, bổ sung", t) and not re.search(
                r"được\s+(sửa đổi, bổ sung|sửa đổi|bổ sung|thay thế|bãi bỏ|đính chính)[^.\n]{0,80}theo quy định tại", t_fn):
            add("TT-VBHN-CHU-THICH", "FAIL", "có nội dung sửa đổi/bổ sung nhưng thiếu chú thích chân trang đúng mẫu câu",
                "'… được sửa đổi, bổ sung theo quy định tại …, có hiệu lực kể từ ngày …' — NĐ250 mục V-XI", can9)
        if "XÁC THỰC VĂN BẢN HỢP NHẤT" not in t:
            add("TT-VBHN-XAC-THUC", "FAIL", "không thấy khối 'XÁC THỰC VĂN BẢN HỢP NHẤT'",
                "khối ký xác thực cuối văn bản, trên đường kẻ ngang — NĐ250 mục XIII", can9)


def _the_thuc_check_t3(parsed, he_eff, add):
    """T3 (R3 v1.34.77) — khuyến nghị WARN/INFO: nhất-quán-bậc cỡ chữ (footnote Mục V NĐ30 — đo sz
    Quốc hiệu↔Tiêu ngữ phải lệch đúng 1pt; Đảng: tiêu đề phải 15pt), ngày<10/tháng<3 thêm 0, thụt đầu
    dòng 1-1,27cm (Đảng ~10mm) qua w:ind, viết tắt tên loại đối chiếu bảng, giãn dòng Đảng 18-22pt Exactly."""
    import re
    from collections import Counter
    text = parsed["text"] or ""
    paras = parsed.get("paras") or []
    head = text[:4000]

    def _psz(sub):
        for p in paras:
            if sub in p["text"]:
                return max(p["szs"].items(), key=lambda kv: kv[1])[0] if p["szs"] else None
        return None

    if he_eff == "dang":
        s = _psz("ĐẢNG CỘNG SẢN VIỆT NAM")
        if s is not None and s != 30:
            add("TT-BAC-CO-CHU", "WARN", f"tiêu đề ĐCSVN {s/2:g}pt", "15pt cố định",
                "HD 05-HD/VPTW Phụ lục 2 (TT 1)")
    else:
        sq = _psz("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM")
        st = _psz("Độc lập")
        if sq is not None and st is not None and (st - sq) != 2:
            add("TT-BAC-CO-CHU", "WARN",
                f"Quốc hiệu {sq/2:g}pt / Tiêu ngữ {st/2:g}pt",
                "Tiêu ngữ = Quốc hiệu + 1pt (cặp 12-13 hoặc 13-14 — tăng, giảm phải thống nhất)",
                "PL I NĐ 30/2020 Mục V, chú thích 1")
    n_bad = len(re.findall(r"ngày\s+\d\s+tháng", text)) + len(re.findall(r"tháng\s+[12]\s+năm", text))
    if n_bad:
        add("TT-SO-NHO-10", "WARN", f"{n_bad} vị trí ngày<10/tháng<3 chưa đệm số 0",
            "vd: ngày 05 tháng 01 năm 2026", "PL I NĐ 30/2020 Mục II.4.b")
    inds = [p["ind"] for p in paras if p.get("ind")]
    if len(inds) >= 3:
        mi = Counter(inds).most_common(1)[0][0] * 25.4 / 1440.0
        lo, hi = (9.0, 11.0) if he_eff == "dang" else (9.9, 12.8)
        if not (lo <= mi <= hi):
            add("TT-THUT-DAU-DONG", "INFO", f"thụt đầu dòng phổ biến {mi:.1f} mm",
                "1-1,27 cm (nhà nước) / ~10 mm (Đảng)", "PL I NĐ30 Mục II.6 / PL I NĐ187 / HD05 6.2.2")
    ABBR_NN = {"NQ", "QĐ", "CT", "QC", "QyĐ", "TC", "TB", "HD", "CTr", "KH", "PA", "ĐA", "DA", "BC", "BB",
               "TTr", "HĐ", "CĐ", "BGN", "BTT", "GUQ", "GM", "GGT", "GNP", "PG", "PC", "PB", "SY", "TrS", "SL"}
    ABBR_QPPL = {"NĐ", "QĐ", "TT", "NQ", "NQLT", "TTLT", "PL", "L", "LQ"}
    ABBR_VBHN = {"LQ", "PL", "NQ", "NQTV", "NL", "LC", "QĐC", "NĐ", "QĐ", "TT", "TL", "QĐCT"}
    ABBR_DANG = {"NQ", "QĐ", "CT", "KL", "QC", "TT", "TTr", "CTr", "HD", "TB", "TC", "BC", "KH", "QH",
                 "ĐA", "PA", "DA", "CV", "BB", "CL", "ĐL", "ĐH"}
    m = None
    aset = None
    if he_eff == "hanh_chinh":
        m = re.search(r"Số:\s*\d+\s*/\s*([A-ZĐ][\wĐ]*)", head)
        aset = ABBR_NN
    elif he_eff in ("vbqppl", "vbqppl_qh"):
        m = re.search(r"[Ss]ố:\s*\d+/\d{4}/([A-ZĐ][\wĐ]*)", head)
        if m and re.match(r"(?:QH|UBTVQH)\d+$|CTN$", m.group(1)):
            m = None                                   # luật/pháp lệnh: token sau năm là CƠ QUAN, không phải loại
        aset = ABBR_QPPL
    elif he_eff == "vbhn":
        m = re.search(r"\d+/\d{4}/VBHN-([A-ZĐ][\wĐ]*)-", head)   # dạng cũ n/VBHN-CQ: token là cơ quan → bỏ
        aset = ABBR_VBHN
    elif he_eff == "dang":
        m = re.search(r"Số\s+\d+\s*-\s*([A-ZĐ][\wĐ]*)/", head)
        aset = ABBR_DANG
    if m and aset is not None and m.group(1) not in aset:
        add("TT-VIET-TAT", "INFO", f"viết tắt loại '{m.group(1)}' không thuộc bảng hệ {he_eff}",
            "bảng viết tắt tên loại — THE_THUC_TRINH_BAY §7", "PL III NĐ30 / NĐ250 II.1 / HD05 3.2")
    if he_eff == "dang":
        lines = [p["line"] for p in paras if p.get("rule") == "exact" and p.get("line")]
        if lines:
            ml = Counter(lines).most_common(1)[0][0]
            if not (360 <= ml <= 440):
                add("TT-DONG", "WARN", f"giãn dòng Exactly {ml/20:g}pt", "18-22pt (Exactly)",
                    "HD 05-HD/VPTW Phần II mục 6.2.2")


def the_thuc_check(path, he=None, strict=False):
    """Engine kiểm T1 (R2): khổ giấy / lề / font / cỡ chữ nội dung / trình bày ngang — PURE, trả
    envelope dict `the_thuc_check.v1` deterministic (findings sort theo id). rc do cmd quyết:
    0 = không FAIL (strict: và không WARN), 2 = có FAIL."""
    import os
    d = _the_thuc_parse_docx(path)
    he_source = "flag" if he else "auto"
    he_eff = he or _the_thuc_detect_he(d["text"])
    crit_all = _the_thuc_criteria()
    base = "vbqppl" if he_eff == "vbhn" else he_eff
    c = crit_all.get(base) or crit_all["hanh_chinh"]

    CAN_A4 = {
        "hanh_chinh": "PL I NĐ 30/2020, Mục I.1: khổ A4 (210 mm x 297 mm)",
        "vbqppl": "PL I NĐ 187/2025, Mục 1 Phần I: khổ A4 (210 mm x 297 mm)",
        "vbqppl_qh": "NQ 351/2017, Đ39.1: trang giấy khổ A4 (210 mm x 297 mm)",
        "vbhn": "NĐ 250/2026, PL mục I.1 (kế thừa kỹ thuật VBQPPL): khổ A4",
        "dang": "HD 05-HD/VPTW, Phần II mục IV: khổ giấy A4 (210 mm x 297 mm)"}
    CAN_NGANG = {
        "hanh_chinh": "PL I NĐ 30/2020, Mục I.2: bảng biểu không làm phụ lục riêng có thể trình bày theo chiều rộng",
        "vbqppl": "PL I NĐ 187/2025, Mục 1 Phần I: phụ lục có bảng biểu có thể trình bày theo chiều rộng",
        "vbqppl_qh": "NQ 351/2017 (kiểu trình bày theo chiều dài khổ A4)",
        "vbhn": "NĐ 250/2026 (kế thừa kỹ thuật VBQPPL)",
        "dang": "HD 05-HD/VPTW (trình bày theo chiều dài khổ A4)"}
    CAN_LE = {
        "hanh_chinh": "PL I NĐ 30/2020, Mục I.3: lề trên/dưới 20-25 mm, trái 30-35 mm, phải 15-20 mm",
        "vbqppl": "PL I NĐ 187/2025, Mục 1 Phần I.3: mép trên/dưới/phải 15-20 mm, mép trái 30-35 mm",
        "vbqppl_qh": "NQ 351/2017, Đ39.1 + chú thích lề sơ đồ Mẫu 1-16 (Phụ lục I): trên/dưới 20-25, trái 30-35, phải 15-20 mm",
        "vbhn": "NĐ 250/2026, PL mục I.1 → PL I NĐ 187/2025 Phần I.3: trên/dưới/phải 15-20, trái 30-35 mm",
        "dang": "HD 05-HD/VPTW, Phần II mục IV.4.1: lề trên 20 / dưới 20 / trái 30 / phải 15 mm"}
    CAN_FONT = {
        "hanh_chinh": "PL I NĐ 30/2020, Mục I.4: Times New Roman, Unicode TCVN 6909:2001, màu đen",
        "vbqppl": "PL I NĐ 187/2025, Mục 1 Phần I: Times New Roman, Unicode TCVN 6909:2001, màu đen",
        "vbqppl_qh": "NQ 351/2017, Đ39.2: Times New Roman, Unicode TCVN 6909:2001",
        "vbhn": "NĐ 250/2026 (kế thừa kỹ thuật VBQPPL): Times New Roman",
        "dang": "HD 05-HD/VPTW, Phần II mục IV.1: Times New Roman, Unicode TCVN 6909:2001, màu đen"}
    CAN_SZ = {
        "hanh_chinh": "PL I NĐ 30/2020, Mục II.6: nội dung cỡ 13-14",
        "vbqppl": "PL I NĐ 187/2025: nội dung cỡ 13-14",
        "vbqppl_qh": "NQ 351/2017, Đ35.1: nội dung cỡ chữ 14",
        "vbhn": "NĐ 250/2026 → PL I NĐ 187/2025: nội dung cỡ 13-14",
        "dang": "HD 05-HD/VPTW, Phụ lục 2: nội dung cỡ 14-15"}

    findings = []

    def add(fid, level, measured, expected, can_cu, location=""):
        findings.append({"id": fid, "level": level, "measured": measured, "expected": expected,
                         "can_cu": can_cu, "location": location})

    # ── T1: khổ giấy + lề theo từng section ──
    SIDE_KEY = {"TREN": ("top", "le_tren_mm", (15, 25)), "DUOI": ("bottom", "le_duoi_mm", (15, 25)),
                "TRAI": ("left", "le_trai_mm", (30, 35)), "PHAI": ("right", "le_phai_mm", (15, 20))}
    for i, s in enumerate(d["sections"], 1):
        loc = f"section {i}"
        land = (s.get("orient") == "landscape") or bool(s.get("w") and s.get("h") and s["w"] > s["h"])
        wmm, hmm = _tt_mm(s.get("w")), _tt_mm(s.get("h"))
        if wmm is not None and hmm is not None:
            a4_doc = abs(wmm - 210) <= 1 and abs(hmm - 297) <= 1
            a4_ngang = abs(wmm - 297) <= 1 and abs(hmm - 210) <= 1
            if not (a4_doc or (land and a4_ngang)):
                add("TT-KHO-GIAY", "FAIL", f"{wmm:.1f}x{hmm:.1f} mm", "A4 210x297 mm (±1 mm)",
                    CAN_A4[he_eff], loc)
        if land:
            add("TT-TRINH-BAY-NGANG", "WARN", f"trang ngang ({loc})",
                "chiều dài A4; chiều rộng chỉ hợp lệ khi chứa bảng biểu", CAN_NGANG[he_eff], loc)
            continue  # lề quy định cho trang dọc — không áp section ngang
        for side, (mk, ck, hop) in SIDE_KEY.items():
            mm = _tt_mm(s.get(mk))
            if mm is None:
                continue
            rng = _tt_range(c.get(ck))
            if rng is None:  # vbqppl_qh: chỉ WARN theo dải-hợp nhà nước
                lo, hi = hop
                if not (lo - 1 <= mm <= hi + 1):
                    add(f"TT-LE-{side}", "WARN", f"{mm:.1f} mm",
                        f"dải-hợp {lo}-{hi} mm (chưa có ngưỡng máy-đọc NQ351)", CAN_LE[he_eff], loc)
            else:
                lo, hi = rng
                if not (lo - 1 <= mm <= hi + 1):
                    add(f"TT-LE-{side}", "FAIL", f"{mm:.1f} mm", f"{c[ck]} mm", CAN_LE[he_eff], loc)

    # ── T1: font + cỡ chữ nội dung (resolve 3 tầng run → Normal → docDefaults) ──
    eff = [((f or d["normal"]["font"] or d["defaults"]["font"]),
            (sz or d["normal"]["sz"] or d["defaults"]["sz"]), n) for f, sz, n in d["runs"]]
    total = sum(n for _, _, n in eff)
    if total:
        bad = {}
        unknown_font = 0
        for f, _, n in eff:
            if f is None:
                unknown_font += n
            elif f != c.get("font", "Times New Roman"):
                bad[f] = bad.get(f, 0) + n
        if bad:
            top = sorted(bad.items(), key=lambda kv: (-kv[1], kv[0]))
            pct = round(100 * sum(bad.values()) / total)
            add("TT-FONT", "FAIL", f"{', '.join(k for k, _ in top[:3])} ({pct}% chữ)",
                c.get("font", "Times New Roman"), CAN_FONT[he_eff])
        elif unknown_font == total:
            add("TT-FONT", "WARN", "font không khai báo ở run/Normal/docDefaults",
                c.get("font", "Times New Roman"), CAN_FONT[he_eff])
        szs = {}
        for _, sz, n in eff:
            if sz is not None:
                szs[sz] = szs.get(sz, 0) + n
        rng = _tt_range((crit_all["vbqppl"] if he_eff == "vbhn" else c).get("co_noi_dung", "13-14"))
        if szs:
            mode_sz = max(szs.items(), key=lambda kv: (kv[1], -kv[0]))[0]
            pt = mode_sz / 2.0
            if rng and not (rng[0] <= pt <= rng[1]):
                add("TT-CO-CHU-NOI-DUNG", "FAIL", f"{pt:g} pt (phổ biến nhất theo lượng chữ)",
                    f"{(crit_all['vbqppl'] if he_eff == 'vbhn' else c).get('co_noi_dung')} pt", CAN_SZ[he_eff])
        else:
            add("TT-CO-CHU-NOI-DUNG", "WARN", "cỡ chữ không khai báo (Word render theo fallback ứng dụng)",
                f"{(crit_all['vbqppl'] if he_eff == 'vbhn' else c).get('co_noi_dung')} pt", CAN_SZ[he_eff])

    # ── T2 cấu trúc + T3 khuyến nghị (R3 v1.34.77) ──
    _the_thuc_check_t2(d["text"], he_eff, add, footnotes=d.get("footnotes", ""))
    _the_thuc_check_t3(d, he_eff, add)

    findings.sort(key=lambda f: (f["id"], f["level"], f["location"]))
    n_fail = sum(1 for f in findings if f["level"] == "FAIL")
    n_warn = sum(1 for f in findings if f["level"] == "WARN")
    n_info = sum(1 for f in findings if f["level"] == "INFO")
    ok = (n_fail == 0) and (not strict or n_warn == 0)
    return {"ok": ok, "schema": "the_thuc_check.v1", "file": os.path.basename(str(path)),
            "he": he_eff, "he_source": he_source, "strict": bool(strict), "findings": findings,
            "summary": {"fail": n_fail, "warn": n_warn, "info": n_info},
            "can_cu_nguon": "references/THE_THUC_TRINH_BAY.md"}


def the_thuc_normalize(in_path, out_path, he=None):
    """R4 v1.34.78 — chuẩn hoá KHUNG mẫu docx trước khi seed kho chung (kế hoạch §5 R4):
    sectPr PORTRAIT → A4 (11906×16838) + lề 20/20/30/15 mm (1134/1134/1701/850 twips — bộ giá trị nằm
    trong dải CẢ 3 hệ, trùng lề cố định VB Đảng); docDefaults → Times New Roman + sz theo hệ (nhà nước
    26 half-pt = 13pt / Đảng 28 = 14pt); style Normal BỎ rFonts/sz/szCs đè (ca ND250: Normal=Arial đè
    docDefaults=TNR); KHÔNG đụng run-level rPr (giữ format cục bộ); section LANDSCAPE giữ nguyên trọn
    (bảng khổ rộng hợp lệ — NĐ30/NĐ187 Mục I.2). Sửa bằng REGEX TARGETED trên string XML (không
    parse-serialize toàn bộ — tránh vỡ namespace); zip repack date cố định 1980 → deterministic +
    idempotent bytes. Self-gate: the_thuc_check(out) phải HẾT FAIL nhóm T1; còn → ok=False rc=2."""
    import os
    import re
    import zipfile
    if os.path.abspath(str(in_path)) == os.path.abspath(str(out_path)):
        return {"ok": False, "schema": "the_thuc_normalize.v1", "error": "IN_OUT_SAME",
                "in": os.path.basename(str(in_path)), "out": os.path.basename(str(out_path))}
    with zipfile.ZipFile(in_path) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    doc = data.get("word/document.xml", b"").decode("utf-8", "replace")
    sty = data.get("word/styles.xml", b"").decode("utf-8", "replace") if "word/styles.xml" in data else ""
    if he in (None, "auto"):
        # r141 (v1.34.81): auto dùng detect THẬT (5 hệ) — mẫu Luật auto ra vbqppl_qh → 14pt đúng NQ351.
        # PHẢI chèn \n tại </w:p> TRƯỚC khi strip tag — detect anchored "^Số:" cần ranh giới dòng (r140).
        plain = re.sub(r"<[^>]+>", "", re.sub(r"</w:p>", "\n", doc[:200000]))[:6000]
        he_eff = _the_thuc_detect_he(plain)
    else:
        he_eff = str(he).replace("-", "_")   # nha_nuoc = alias cũ (.78): cỡ nhà nước 13pt, self-check auto
    sz = "28" if he_eff in ("dang", "vbqppl_qh") else "26"
    n_fixed = [0]

    def _fix_sect(m):
        blk = m.group(0)
        land = 'w:orient="landscape"' in blk
        if not land:
            m2 = re.search(r'<w:pgSz\b[^>]*w:w="(\d+)"[^>]*w:h="(\d+)"', blk)
            if m2 and int(m2.group(1)) > int(m2.group(2)):
                land = True                            # w>h không khai orient — vẫn là trang ngang
        if land:
            return blk
        new = blk
        m3 = re.search(r"<w:pgMar\b([^>]*)/>", new)
        if m3:
            attrs = m3.group(1)

            def _keep(name, dflt):
                mm = re.search(rf'w:{name}="(-?\d+)"', attrs)
                return mm.group(1) if mm else dflt
            gut = re.search(r'w:gutter="(-?\d+)"', attrs)
            new_mar = ('<w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701"'
                       f' w:header="{_keep("header", "720")}" w:footer="{_keep("footer", "720")}"'
                       + (f' w:gutter="{gut.group(1)}"' if gut else "") + "/>")
            new = new.replace(m3.group(0), new_mar, 1)
        m4 = re.search(r"<w:pgSz\b[^>]*/>", new)
        if m4 and m4.group(0) != '<w:pgSz w:w="11906" w:h="16838"/>':
            new = new.replace(m4.group(0), '<w:pgSz w:w="11906" w:h="16838"/>', 1)
        if new != blk:
            n_fixed[0] += 1
        return new

    doc2 = re.sub(r"<w:sectPr\b.*?</w:sectPr>", _fix_sect, doc, flags=re.S)
    DD = ("<w:docDefaults><w:rPrDefault><w:rPr>"
          '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
          f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
          "</w:rPr></w:rPrDefault><w:pPrDefault/></w:docDefaults>")
    if "<w:docDefaults>" in sty:
        sty2 = re.sub(r"<w:docDefaults>.*?</w:docDefaults>", DD, sty, count=1, flags=re.S)
    elif sty:
        sty2 = re.sub(r"(<w:styles\b[^>]*>)", lambda mm: mm.group(1) + DD, sty, count=1)
    else:
        sty2 = ('<?xml version="1.0"?><w:styles xmlns:w='
                '"http://schemas.openxmlformats.org/wordprocessingml/2006/main">' + DD + "</w:styles>")
    dd_replaced = (sty2 != sty)

    def _clean_normal(m):
        blk = m.group(0)
        blk = re.sub(r"<w:rFonts\b[^>]*/>", "", blk)
        blk = re.sub(r"<w:szCs\b[^>]*/>", "", blk)
        blk = re.sub(r"<w:sz\b[^>]*/>", "", blk)
        return blk

    sty3, _n_norm = re.subn(r'<w:style\b[^>]*w:styleId="Normal".*?</w:style>', _clean_normal,
                            sty2, count=1, flags=re.S)
    normal_cleaned = (sty3 != sty2)
    data["word/document.xml"] = doc2.encode("utf-8")
    data["word/styles.xml"] = sty3.encode("utf-8")
    if "word/styles.xml" not in names:
        names.append("word/styles.xml")
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zo:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zo.writestr(zi, data[n])
    chk_he = he_eff if he_eff in ("hanh_chinh", "vbqppl", "vbqppl_qh", "vbhn", "dang") else None
    env_chk = the_thuc_check(out_path, he=chk_he)
    T1IDS = ("TT-KHO-GIAY", "TT-LE-TREN", "TT-LE-DUOI", "TT-LE-TRAI", "TT-LE-PHAI",
             "TT-FONT", "TT-CO-CHU-NOI-DUNG")
    t1f = sorted({f["id"] for f in env_chk["findings"] if f["level"] == "FAIL" and f["id"] in T1IDS})
    return {"ok": not t1f, "schema": "the_thuc_normalize.v1",
            "in": os.path.basename(str(in_path)), "out": os.path.basename(str(out_path)),
            "he": he_eff, "sz_default_halfpt": int(sz),
            "changes": {"sections_fixed": n_fixed[0], "docdefaults_replaced": dd_replaced,
                        "normal_cleaned": normal_cleaned},
            "self_check": {"he_check": env_chk.get("he"), "t1_fail": len(t1f), "t1_fail_ids": t1f,
                           "fail": env_chk["summary"]["fail"], "warn": env_chk["summary"]["warn"]}}


def cmd_the_thuc_normalize(args):
    """CLI `tl the-thuc-normalize <in> <out> [--he auto|nha-nuoc|dang] [--json]` — ghi file OUT local
    (ghi đè nếu tồn tại; in==out bị chặn IN_OUT_SAME). rc: 0 = self-check hết FAIL T1; 2 = còn."""
    import os
    ip = getattr(args, "in_docx", None)
    op = getattr(args, "out_docx", None)
    if not ip or not os.path.isfile(ip):
        env = {"ok": False, "schema": "the_thuc_normalize.v1", "error": "FILE_NOT_FOUND", "in": str(ip or "")}
        print(_json_dumps(env))
        return 2
    env = the_thuc_normalize(ip, op, he=(getattr(args, "he", "auto") or "auto"))
    print(_json_dumps(env))
    return 0 if env.get("ok") else 2


def cmd_the_thuc_check(args):
    """CLI `tl the-thuc-check <docx> [--he ...] [--strict] [--json] [--out f]` — luôn in envelope JSON
    (READ-ONLY, offline; --json giữ tương thích bộ cờ chung). rc: 0 ok / 2 có FAIL (strict: WARN cũng 2)."""
    import os
    p = getattr(args, "docx_path", None)
    he_flag = (getattr(args, "he", "auto") or "auto").replace("-", "_")
    he = None if he_flag == "auto" else he_flag
    strict = bool(getattr(args, "strict", False))
    if not p or not os.path.isfile(p):
        env = {"ok": False, "schema": "the_thuc_check.v1", "error": "FILE_NOT_FOUND", "file": str(p or "")}
        rc = 2
    else:
        env = the_thuc_check(p, he=he, strict=strict)
        rc = 0 if env.get("ok") else 2
    out_s = _json_dumps(env)
    out_f = getattr(args, "out", None)
    if out_f:
        with open(out_f, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(out_s + "\n")
    print(out_s)
    return rc
