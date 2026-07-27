#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_deep.py — Kiểm tra sâu, leo thang 4 tầng, cho văn bản trước khi vào corpus/cache.
Triết lý: kiểm rẻ chạy LUÔN và đủ nhạy để quyết có gọi kiểm đắt không.
Happy path < 5s. Văn bản không bao giờ được im lặng về khuyết tật của nó.

  T0  soi nguồn PDF      : text layer từng trang (pdftotext), trang 0-chữ = trang scan  (~0.2s)
  T1  bất biến cấu trúc  : dãy Điều liên tục, Điều cuối khớp mô-típ kết, quốc hiệu/số hiệu,
                           Chương La Mã, mật độ ký tự rác OCR, mật độ từ chức năng có dấu  (<1s)
  T2  đối chiếu chéo     : so độ dài TỪNG Điều giữa 2 biểu diễn (lệch >2% → cờ) + probe   (~0.3s)
  T3  diff từng từ       : CHỈ các Điều bị T2 cờ                                          (~ms/Điều)

Dùng:
  verify_deep.py --text A.txt [--so-hieu 89/VBHN-VPQH] [--declared-articles 79]
                 [--cross B.txt] [--pdf goc.pdf] [--json out.json] [--quick]
Exit code: 0 = PASS | 1 = PARTIAL (có cờ khoanh vùng, nạp với verified=partial+note)
           2 = FAIL (vỡ cấu trúc → QUARANTINE) | 3 = lỗi vận hành
"""
import argparse, json, re, subprocess, sys, unicodedata
from difflib import SequenceMatcher
from pathlib import Path

VN_FUNC_WORDS = ["của", "được", "người", "định", "việc", "phải", "đối", "Điều"]
TERMINAL_PAT = re.compile(
    r"(hiệu\s*lực\s*thi\s*hành|quy\s*định\s*chi\s*tiết|điều\s*khoản\s*(thi\s*hành|chuyển\s*tiếp))",
    re.I)
HEAD_PAT = re.compile(r"CỘNG\s*HÒA\s*XÃ\s*HỘI\s*CHỦ\s*NGHĨA\s*VIỆT\s*NAM", re.I)
# Tách Điều chịu dính dòng: "Điều N." + tiêu đề bắt đầu bằng chữ hoa
ART_SPLIT = re.compile(r"(?:(?<=^)|(?<=[\s.;:]))(Điều\s+(\d+)\.)\s+(?=[A-ZĐÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ])",
                       re.M)
ROMAN_PAT = re.compile(r"(?m)^Chương\s+([IVXLC]+)\b")
# v1.12.8: heading PHỤ LỤC đứng riêng — sau "PHỤ LỤC" phải là SỐ (La Mã/Ả Rập, có thể kèm "SỐ")
# HOẶC hết dòng. Tránh bắt cụm trong câu kiểu "...PHỤ LỤC VÀ BẢN SAO VĂN BẢN".
PHU_LUC_PAT = re.compile(r"(?m)^[ \t]*PHỤ\s+LỤC(?:[ \t]*$|[ \t]+(?:SỐ[ \t]+)?[IVXLC0-9]+\b)")
ROMAN_VAL = {"I":1,"V":5,"X":10,"L":50,"C":100}


def roman_to_int(s):
    v, prev = 0, 0
    for ch in reversed(s):
        cur = ROMAN_VAL.get(ch, 0)
        v = v - cur if cur < prev else v + cur
        prev = max(prev, cur)
    return v


def split_articles(raw):
    """→ dict {n:int → text}; giữ lần xuất hiện ĐẦU (thân luật), bỏ trích dẫn lặp ở footnote.
    v1.12.8: cắt khối PHỤ LỤC khỏi Điều CUỐI (phụ lục luôn nằm sau Điều cuối)."""
    parts = ART_SPLIT.split(raw)
    arts = {}
    i = 1
    while i + 2 < len(parts) + 1 and i + 1 < len(parts):
        marker, num = parts[i], int(parts[i + 1])
        body = parts[i + 2] if i + 2 < len(parts) else ""
        # v1.12.8: bỏ "Điều N." THÂN RỖNG — đây là trích dẫn nội văn (vd "...khoản 2 Điều 210."
        # đứng ngay trước "Điều 2.") bị tách nhầm thành Điều, gây Điều giả/đứt dãy.
        if num not in arts and body.strip():
            arts[num] = (marker + " " + body).strip()
        i += 3
    if arts:
        last = max(arts)
        cut = PHU_LUC_PAT.search(arts[last])
        if cut:
            arts[last] = arts[last][:cut.start()].strip()
    return arts


def preamble_of(raw):
    """→ KHỐI ĐẦU VĂN BẢN: phần đứng TRƯỚC "Điều 1" (Quốc hiệu, cơ quan ban hành, Số hiệu, địa danh-
    ngày tháng, tên loại + trích yếu, toàn bộ khối "Căn cứ…", tiêu đề Chương I). '' nếu không tách được Điều.

    r215 (sổ lỗi CACHE_BUILD_DANH_ROI_KHOI_DAU_VAN_BAN, đo 27-07-2026): `split_articles` bỏ `parts[0]`
    nên record cache consolidated KHÔNG hề lưu khối này ⇒ bản dựng lại từ `articles` bắt đầu thẳng từ
    "Điều 1", văn bản KHÔNG TỰ CHỨNG MINH ĐƯỢC DANH TÍNH và `_classify_doc_header` đoán sai (đã trả giá
    ở VBHN Luật NSNN 89-2026). Dùng CHUNG `ART_SPLIT` với `split_articles` để hai bên không bao giờ lệch
    định nghĩa "chỗ Điều đầu tiên bắt đầu"."""
    parts = ART_SPLIT.split(raw or "")
    return parts[0].strip() if len(parts) > 1 else ""


CB_DONG_CHAY = re.compile(
    r"^\s*(?:\d{1,4}\s+)?CÔNG\s+BÁO\s*/\s*Số\s+[^/\n]*/\s*Ngày\s+\d{1,2}\s*-\s*\d{1,2}\s*-\s*\d{4}\s*(?:\d{1,4}\s*)?$")
CB_SO_TRANG = re.compile(r"^\s*\d{1,4}\s*$")
CB_CHU_KY_SO = (re.compile(r"^\s*Người\s+ký\s*:"), re.compile(r"^\s*Email\s*:"),
                re.compile(r"^\s*Cơ\s+quan\s*:"), re.compile(r"^\s*Thời\s+gian\s+ký\s*:"))
CB_DAU_MUC = re.compile(r"^\s*(?:VĂN\s+BẢN\s+QUY\s+PHẠM\s+PHÁP\s+LUẬT|PHẦN\s+VĂN\s+BẢN\s+QUY\s+PHẠM\s+PHÁP\s+LUẬT)\s*$")


def loc_rac_congbao(raw):
    """PURE (r217 — sổ lỗi `BAN_CONG_BAO_BOC_RA_CON_RAC_KHONG_CO_BUOC_LAM_SACH_CHUAN`, lượt rà 6):
    bóc PDF Công báo ra thì thân văn bản bị chèn RÁC TRÌNH BÀY. Trả dict — KHÔNG ghi file, KHÔNG in.

    Bỏ ĐÚNG BA loại có khuôn CHẮC, mỗi loại đều phải khớp TOÀN DÒNG (dính chữ khác ⇒ KHÔNG bỏ):
      · `dong_chay`  — dòng chạy đầu trang `[số] CÔNG BÁO/Số …/Ngày d-m-yyyy [số]`;
      · `so_trang`   — dòng CHỈ có số VÀ đứng KỀ một dòng chạy (bỏ qua dòng trắng xen giữa). Điều kiện
                       kề là bắt buộc: trong phụ lục/biểu mẫu có vô số dòng chỉ-một-số là DỮ LIỆU THẬT;
      · `chu_ky_so`  — khối chữ ký số ĐỦ 4 dòng liên tiếp đúng thứ tự Người ký/Email/Cơ quan/Thời gian ký.
                       ★Đo 27-07: khối này KHÔNG chỉ nằm ở đầu bản — ND 159 có HAI khối nằm GIỮA thân
                       (sau khoản 6 Điều 1), Luật 41/2024 có một khối; bản làm sạch bằng tay ở lượt 6 chỉ
                       bắt khối ở đầu nên còn sót. Vì vậy quét TOÀN VĂN, không neo vị trí.

    ★KHÔNG tự bỏ NHÃN MỤC Công báo ở đầu bản (`VĂN BẢN QUY PHẠM PHÁP LUẬT`, tên cơ quan in một mình) —
    chỉ KHAI BÁO ở `canh_bao`. Đo trên 3 bản thật cho thấy mọi quy tắc tự động đều cắt vào khối đầu:
    Công báo in tên cơ quan HAI lần (nhãn mục + cơ quan ban hành), và neo «CỘNG HÒA XÃ HỘI CHỦ NGHĨA
    VIỆT NAM» nằm SAU dòng số hiệu ở cả Luật 41/2024 (`Luật số: 41/2024/QH15` trên neo 1 dòng) lẫn
    ND 159 (`Số: 159/2025/NĐ-CP`) ⇒ cắt tại neo là ăn mất chính danh tính văn bản. Người quyết, không máy.

    Phản chứng NỘI TẠI (chạy mỗi lần, không phải chỉ trong test): số dòng giữ + số dòng bỏ phải bằng số
    dòng vào, và bản ra phải ĐÚNG BẰNG `"\\n".join(dòng giữ)` — lệch ⇒ bước làm sạch đã đụng thứ khác."""
    lines = (raw or "").split("\n")
    n = len(lines)
    bo = {}

    def _ke_dong_chay(i):
        for buoc in (-1, 1):
            j = i + buoc
            while 0 <= j < n and not lines[j].strip():
                j += buoc
            if 0 <= j < n and CB_DONG_CHAY.match(lines[j]):
                return True
        return False

    for i, ln in enumerate(lines):
        if CB_DONG_CHAY.match(ln):
            bo[i] = "dong_chay"
    for i, ln in enumerate(lines):
        if i not in bo and CB_SO_TRANG.match(ln) and _ke_dong_chay(i):
            bo[i] = "so_trang"
    for i in range(n - 3):
        if all(CB_CHU_KY_SO[k].match(lines[i + k]) for k in range(4)):
            for k in range(4):
                bo.setdefault(i + k, "chu_ky_so")

    giu = [ln for i, ln in enumerate(lines) if i not in bo]
    out = "\n".join(giu)
    if len(giu) + len(bo) != n or out != "\n".join(giu):
        raise AssertionError("LOC_CONGBAO_PHAN_CHUNG_HONG: %d giữ + %d bỏ ≠ %d dòng vào" % (len(giu), len(bo), n))

    canh_bao = []
    con_dau_muc = [i + 1 for i, ln in enumerate(lines) if i not in bo and CB_DAU_MUC.match(ln)]
    if con_dau_muc:
        canh_bao.append("DAU_MUC_CONG_BAO_CON_LAI: dòng %s — nhãn mục của Công báo, KHÔNG tự bỏ được "
                        "(Công báo in tên cơ quan hai lần; cắt máy sẽ ăn vào khối đầu). Cắt tay tới dòng "
                        "mang số hiệu (`Số: …` / `Luật số: …`) rồi nạp lại."
                        % ", ".join(str(x) for x in con_dau_muc))
    sot = [i + 1 for i, ln in enumerate(lines) if i not in bo and "CÔNG BÁO/" in ln.replace("  ", " ")]
    if sot:
        canh_bao.append("DONG_CHAY_DINH_CHU_THAN_VAN_BAN: dòng %s có 'CÔNG BÁO/' nhưng KHÔNG khớp toàn "
                        "dòng ⇒ cố ý KHÔNG bỏ (có thể là chữ của thân văn bản). Kiểm bằng mắt."
                        % ", ".join(str(x) for x in sot[:10]))
    return {"text": out,
            "counts": {"dong_chay": sum(1 for v in bo.values() if v == "dong_chay"),
                       "so_trang": sum(1 for v in bo.values() if v == "so_trang"),
                       "chu_ky_so": sum(1 for v in bo.values() if v == "chu_ky_so")},
            "bo": [{"dong": i + 1, "loai": bo[i], "noi_dung": lines[i]} for i in sorted(bo)],
            "canh_bao": canh_bao,
            "dong_vao": n, "dong_ra": len(giu),
            "chars_vao": len(raw or ""), "chars_ra": len(out)}


def co_rac_congbao(raw):
    """PURE (r217): CHỈ ĐO, không sửa — dùng ở đường nạp khi người dùng KHÔNG bật `--loc-congbao`.
    Trả list mô tả; rỗng = sạch. Cùng họ với cờ `khoi_dau_missing` của r215: khai báo, KHÔNG chặn —
    bản Công báo còn rác vẫn là bản chính thức, chặn nạp là phá đúng ca dùng chính đáng."""
    r = loc_rac_congbao(raw)
    c = r["counts"]
    ra = []
    if any(c.values()):
        ra.append("NGUON_CONG_BAO_CON_RAC: dòng chạy=%d · số trang=%d · chữ ký số=%d (bỏ được bằng "
                  "`--loc-congbao`)" % (c["dong_chay"], c["so_trang"], c["chu_ky_so"]))
    ra.extend(r["canh_bao"])
    return ra


def appendix_start(raw):
    """→ chỉ số ký tự nơi khối PHỤ LỤC bắt đầu (heading đầu tiên TỪ Điều cuối trở đi), hoặc -1."""
    last_art = None
    for mm in ART_SPLIT.finditer(raw):
        last_art = mm
    start = last_art.start() if last_art else 0
    m = PHU_LUC_PAT.search(raw, start)
    return m.start() if m else -1


def extract_appendix(raw):
    """→ khối phụ lục (từ heading 'PHỤ LỤC <số>' đầu tiên sau Điều cuối tới hết). '' nếu không có."""
    i = appendix_start(raw)
    return raw[i:].strip() if i >= 0 else ""


def garbage_ratio(text):
    """Tỷ lệ ký tự rác kiểu OCR hỏng (~, \\x, ký tự lạ) trên ký tự chữ."""
    letters = sum(1 for c in text if c.isalpha())
    if not letters:
        return 1.0
    bad = text.count("~") + text.count("\ufffd") + len(re.findall(r"[A-Za-z][0-9][A-Za-z]", text))
    return bad / letters


def diacritic_density(text):
    """%% ký tự CÓ DẤU tiếng Việt trên tổng chữ cái. Văn bản Việt thật ~20-35%%;
    OCR mất dấu tụt về ~0%%. Đo theo ký tự bền hơn theo từ (Điều liệt kê danh từ
    vẫn nhiều dấu — tránh false positive kiểu Điều 30 Luật AI)."""
    letters = [c for c in text if c.isalpha()]
    if len(letters) < 100:
        return None
    diac = sum(1 for c in letters if ord(c) > 127)
    return 100.0 * diac / len(letters)


# ---------------- T0 ----------------
def t0_pdf(pdf_path, report):
    out = {"tier": "T0", "pages": [], "scan_pages": [], "ok": True}
    try:
        info = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True, timeout=20)
        m = re.search(r"Pages:\s+(\d+)", info.stdout)
        npages = int(m.group(1)) if m else 0
        for p in range(1, npages + 1):
            r = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), pdf_path, "-"],
                               capture_output=True, text=True, timeout=30)
            n = len(r.stdout.strip())
            out["pages"].append(n)
            if n < 120:                       # cùng ngưỡng assert_pdf_not_scanned
                out["scan_pages"].append(p)
        if out["scan_pages"]:
            out["ok"] = False
            report["flags"].append(f"T0: trang scan/0-text: {out['scan_pages']} "
                                   f"(nội dung các trang này SẼ MẤT nếu chỉ lấy text layer)")
    except FileNotFoundError:
        out["note"] = "pdftotext/pdfinfo không có — bỏ T0"
    except Exception as e:
        out["note"] = f"T0 lỗi: {e}"
    report["t0"] = out


# ---------------- T1 ----------------
def t1_structure(raw, declared_n, so_hieu, report):
    out = {"tier": "T1", "ok": True, "fatal": False}
    arts = split_articles(raw)
    nums = sorted(arts)
    out["articles_found"] = len(nums)
    out["terminal_article"] = nums[-1] if nums else 0
    # 1) dãy liên tục
    expect_n = declared_n or (nums[-1] if nums else 0)
    missing = [i for i in range(1, expect_n + 1) if i not in arts]
    out["missing"] = missing
    if missing:
        out["ok"] = False
        # thiếu Điều GIỮA văn bản = vỡ cấu trúc; chỉ thiếu cụm cuối = khả năng cụt/trang scan
        mid_missing = [m for m in missing if m < expect_n - len(missing) + 1] if missing != list(
            range(expect_n - len(missing) + 1, expect_n + 1)) else []
        # VBHN (văn bản hợp nhất) thường KHUYẾT Điều ở giữa do Điều bị BÃI BỎ khi hợp nhất
        # ⇒ đây là hợp lệ, KHÔNG coi là FATAL (vẫn ghi cờ để rà soát thủ công).
        is_vbhn = "VBHN" in (so_hieu or "").upper()
        if mid_missing and not is_vbhn:
            out["fatal"] = True
            report["flags"].append(f"T1-FATAL: thiếu Điều GIỮA văn bản: {mid_missing}")
        elif mid_missing and is_vbhn:
            report["flags"].append(
                f"T1-VBHN: khuyết Điều giữa {mid_missing} — coi là Điều đã bãi bỏ khi hợp nhất (không FATAL)")
        else:
            report["flags"].append(f"T1: thiếu cụm Điều CUỐI {missing} — nghi cụt/trang scan")
    # 1b) v1.12.8: Điều cuối lớn bất thường ⇒ nghi phụ lục/mẫu chưa tách (export phi chuẩn,
    #     không có heading 'PHỤ LỤC <số>'). Cờ MỀM để surface, không FATAL.
    if len(nums) >= 3:
        others = [len(arts[n]) for n in nums[:-1]]
        avg = sum(others) / max(1, len(others))
        last_len = len(arts[nums[-1]])
        if last_len > 8000 and last_len > 8 * avg:
            out["ok"] = False
            report["flags"].append(
                f"T1: Điều cuối ({nums[-1]}) dài {last_len} ký tự ≫ TB {int(avg)} — "
                "nghi phụ lục/mẫu chưa tách (heading phụ lục phi chuẩn)")
    # 2) Điều cuối khớp mô-típ kết
    if nums and not TERMINAL_PAT.search(arts[nums[-1]]):
        out["ok"] = False
        report["flags"].append(f"T1: Điều cuối ({nums[-1]}) không khớp mô-típ kết "
                               "(hiệu lực/quy định chi tiết/chuyển tiếp) — nghi cụt")
    # 3) đầu văn bản
    head = raw[:2000]
    if not HEAD_PAT.search(head):
        out["ok"] = False
        report["flags"].append("T1: không thấy quốc hiệu ở đầu — nghi thiếu trang đầu/lẫn chrome web")
    if so_hieu:
        key = re.escape(so_hieu.split("/")[0])
        if not re.search(key, head):
            report["flags"].append(f"T1-nhẹ: số '{so_hieu}' không thấy trong 2000 ký tự đầu")
    # 4) Chương La Mã liên tục
    romans = [roman_to_int(r) for r in ROMAN_PAT.findall(raw)]
    out["chapters"] = len(romans)
    if romans and romans != list(range(1, len(romans) + 1)):
        out["ok"] = False
        report["flags"].append(f"T1: dãy Chương không liên tục: {romans}")
    # 5) rác OCR theo cửa sổ 3000 ký tự
    bad_zones = []
    for i in range(0, len(raw), 3000):
        z = raw[i:i + 3000]
        if garbage_ratio(z) > 0.01:
            bad_zones.append(i)
    if bad_zones:
        out["ok"] = False
        report["flags"].append(f"T1: vùng ký tự rác OCR tại offset {bad_zones[:5]}"
                               f"{'…' if len(bad_zones) > 5 else ''}")
    # 6) mất dấu theo Điều
    flat = []
    for n in nums:
        d = diacritic_density(arts[n])
        if d is not None and d < 10.0:
            flat.append(n)
    if flat:
        out["ok"] = False
        report["flags"].append(f"T1: nghi OCR MẤT DẤU tại Điều {flat}")
    report["t1"] = out
    return arts


# ---------------- T2 + T3 ----------------
def norm_words(s):
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.split(" ")


def t2_t3_cross(arts_a, arts_b, report):
    """So HASH nội dung chuẩn hóa TỪNG Điều giữa 2 biểu diễn: khác hash → suspect,
    bất kể lệch 1 từ hay 1 đoạn (vụ 'gồm/bao gồm' lệch 0.05%% độ dài vẫn phải bắt).
    Vẫn O(n) rẻ; T3 word-diff chỉ chạy trên Điều suspect."""
    import hashlib as _h
    t2 = {"tier": "T2", "ok": True, "suspect": []}
    common = sorted(set(arts_a) & set(arts_b))
    only_a = sorted(set(arts_a) - set(arts_b))
    only_b = sorted(set(arts_b) - set(arts_a))
    if only_a or only_b:
        t2["ok"] = False
        report["flags"].append(f"T2: lệch tập Điều — chỉ A có {only_a}, chỉ B có {only_b}")
    def h(s):
        return _h.sha1(" ".join(norm_words(s)).encode()).hexdigest()
    for n in common:
        if h(arts_a[n]) != h(arts_b[n]):
            t2["suspect"].append(n)
    if t2["suspect"]:
        t2["ok"] = False
    report["t2"] = t2
    # T3: chỉ diff Điều nghi
    t3 = {"tier": "T3", "diffs": []}
    for n in t2["suspect"]:
        wa, wb = norm_words(arts_a[n]), norm_words(arts_b[n])
        sm = SequenceMatcher(None, wa, wb)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != "equal":
                t3["diffs"].append({"article": n,
                                    "a": " ".join(wa[i1:i2])[:160],
                                    "b": " ".join(wb[j1:j2])[:160],
                                    "ctx": " ".join(wa[max(0, i1 - 5):i1])[:80]})
    if t3["diffs"]:
        report["flags"].append(f"T3: {len(t3['diffs'])} khác biệt câu chữ tại Điều {t2['suspect']}"
                               " — xem report['t3']['diffs']")
    report["t3"] = t3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True, help="Văn bản chính (txt, utf-8)")
    ap.add_argument("--cross", help="Biểu diễn độc lập thứ 2 để đối chiếu (txt)")
    ap.add_argument("--pdf", help="PDF nguồn (chạy T0 per-page)")
    ap.add_argument("--so-hieu", default="")
    ap.add_argument("--declared-articles", type=int, default=0,
                    help="Số Điều khai báo/kỳ vọng (vd từ mục lục/ATCL); 0 = lấy max tìm được")
    ap.add_argument("--quick", action="store_true", help="Chỉ T1")
    ap.add_argument("--json", help="Ghi report JSON")
    a = ap.parse_args()

    report = {"flags": [], "verdict": None}
    raw = Path(a.text).read_text(encoding="utf-8").replace("\r\n", "\n")
    if a.pdf and not a.quick:
        t0_pdf(a.pdf, report)
    arts = t1_structure(raw, a.declared_articles, a.so_hieu, report)
    if a.cross and not a.quick:
        raw_b = Path(a.cross).read_text(encoding="utf-8").replace("\r\n", "\n")
        t2_t3_cross(arts, split_articles(raw_b), report)

    if report.get("t1", {}).get("fatal"):
        report["verdict"] = "FAIL_QUARANTINE"; code = 2
    elif report["flags"]:
        report["verdict"] = "PARTIAL"; code = 1
    else:
        report["verdict"] = "PASS"; code = 0
    out = json.dumps(report, ensure_ascii=False, indent=1)
    if a.json:
        Path(a.json).write_text(out, encoding="utf-8")
    print(out)
    sys.exit(code)


if __name__ == "__main__":
    main()
