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
    droot = ET.fromstring(doc)

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
        ptxt = []
        for r in p.iter(W + "r"):
            rt = "".join((t.text or "") for t in r.iter(W + "t"))
            f, s = _rpr_font_sz(r.find(W + "rPr"))
            if rt:
                runs.append((f, s, len(rt)))
                ptxt.append(rt)
        if ptxt:
            paras.append("".join(ptxt))
    return {"sections": sections, "defaults": defaults, "normal": normal,
            "runs": runs, "text": "\n".join(paras)}


def _the_thuc_detect_he(text):
    """Phân luồng hệ theo §1 THE_THUC_TRINH_BAY.md: dang → vbhn → vbqppl (nhánh _qh nếu ký hiệu
    QH/UBTVQH/CTN hoặc tên loại LUẬT/BỘ LUẬT/PHÁP LỆNH) → hanh_chinh."""
    import re
    head = (text or "")[:4000]
    if "ĐẢNG CỘNG SẢN VIỆT NAM" in head and "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" not in head:
        return "dang"
    if re.search(r"\d+/\d{4}/VBHN-", head):
        return "vbhn"
    if re.search(r"\d+/\d{4}/[A-ZĐ]", head):
        if (re.search(r"/(QH|UBTVQH)\d+\b|/CTN\b", head)
                or re.search(r"(?m)^\s*(BỘ\s+)?LUẬT\s*$|^\s*PHÁP\s+LỆNH\s*$", head)):
            return "vbqppl_qh"
        return "vbqppl"
    return "hanh_chinh"


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

    findings.sort(key=lambda f: (f["id"], f["level"], f["location"]))
    n_fail = sum(1 for f in findings if f["level"] == "FAIL")
    n_warn = sum(1 for f in findings if f["level"] == "WARN")
    n_info = sum(1 for f in findings if f["level"] == "INFO")
    ok = (n_fail == 0) and (not strict or n_warn == 0)
    return {"ok": ok, "schema": "the_thuc_check.v1", "file": os.path.basename(str(path)),
            "he": he_eff, "he_source": he_source, "strict": bool(strict), "findings": findings,
            "summary": {"fail": n_fail, "warn": n_warn, "info": n_info},
            "can_cu_nguon": "references/THE_THUC_TRINH_BAY.md"}


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
