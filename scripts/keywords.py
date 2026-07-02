#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
keywords.py — BÓC TỪ KHÓA CHỦ ĐỀ (cột `tukhoa`) một cách TẤT ĐỊNH, KHÔNG AI / KHÔNG RAG.

Vì sao tồn tại (xem SKILL.md v1.13.4):
  Registry là BẢN ĐỒ để Claude đọc → chọn đúng văn bản → mới `notebook_query` qua NLM MCP.
  Các cột cấu trúc (so_hieu/loai/linhvuc/goc/hieuluc/nlm_*) lo DANH TÍNH + CHỌN-ĐÚNG-PHIÊN-BẢN.
  `tukhoa` bổ sung đúng thứ chúng thiếu: MÓC CHỦ ĐỀ để khớp câu hỏi — ở dạng ĐẶC, nạp được cả
  corpus vào context (không bloat như prose describe → tránh "lost in the middle").

Nguồn từ khóa = CẤU TRÚC đã parse (có sẵn lúc ingest, miễn phí, idempotent vì chủ đề KHÔNG đổi
  khi văn bản bị sửa):
    • Tiêu đề CHƯƠNG  (Chương <La Mã>\n<TIÊU ĐỀ>)         — móc chủ đề mạnh nhất
    • Tiêu đề ĐIỀU    (dòng đầu mỗi "Điều N. <tiêu đề>")  — bản đồ nội dung
  KHÔNG nhét lại title/so_hieu/linhvuc (đã là cột riêng) → tránh trùng lặp.
  Boilerplate vô giá trị phân biệt (Phạm vi điều chỉnh, Đối tượng áp dụng, Hiệu lực thi hành…)
  bị STOPLIST loại bỏ.

API:  extract_keywords(record: dict) -> str        # record = legal_document.json
CLI:  python3 keywords.py --in legal_document.json  # in tukhoa
      python3 keywords.py --selftest                # tự kiểm
"""
import argparse, json, re, sys, unicodedata

MAX_PHRASES = 28
MAX_CHARS   = 700
SEP         = "; "

# Tiêu đề chương: "Chương I\n  QUẢN LÝ NHÀ NƯỚC…"  (lấy dòng tiêu đề ngay sau)
CHUONG_TITLE = re.compile(r"Chương\s+[IVXLC]+[ \t]*\n+[ \t]*([^\n]{2,120})")
# Bóc "Điều N." ở ĐẦU giá trị article (split_articles luôn prepend marker)
DIEU_HEAD    = re.compile(r"^\s*Điều\s+\d+[a-zđ]?\.?\s*")

# Boilerplate (chuẩn hóa: casefold, bỏ dấu câu cuối) — 0 giá trị phân biệt văn bản.
_STOP = {
    "pham vi dieu chinh", "doi tuong ap dung", "giai thich tu ngu",
    "ap dung phap luat", "ap dung luat", "hieu luc thi hanh", "hieu luc",
    "dieu khoan thi hanh", "dieu khoan chuyen tiep", "quy dinh chuyen tiep",
    "to chuc thuc hien", "trach nhiem thi hanh", "trach nhiem to chuc thuc hien",
    "quy dinh chung", "nhung quy dinh chung", "dieu khoan chung",
    "nguyen tac chung", "quy dinh chi tiet thi hanh",
    "to chuc thuc hien va dieu khoan thi hanh",
}


def _ascii(s: str) -> str:
    """casefold + bỏ dấu tiếng Việt + bỏ dấu câu rìa → khóa so khớp stoplist."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("đ", "d").replace("Đ", "d")
    s = re.sub(r"[^a-zA-Z0-9 ]", " ", s).strip().lower()
    return re.sub(r"\s+", " ", s)


def _is_stop(phrase: str) -> bool:
    k = _ascii(phrase)
    if not k or len(k) < 3:
        return True
    if k in _STOP:
        return True
    # "điều khoản …", "hiệu lực …" mở đầu boilerplate
    return k.startswith("dieu khoan ") or k == "ket luan"


def _clean(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip(" \t.;:–-—")
    return s


def _dieu_heading(text: str) -> str:
    """Tiêu đề của một Điều: phần sau 'Điều N.' tới hết DÒNG ĐẦU (cắt nếu lẫn thân)."""
    rest = DIEU_HEAD.sub("", text, count=1)
    line = rest.split("\n", 1)[0]
    line = _clean(line)
    if len(line) > 140:                      # heading dính thân → cắt ở câu đầu
        m = re.search(r"\.\s", line)
        line = _clean(line[: m.start()]) if m else line[:140]
    return line


def _collect(record: dict):
    arts = record.get("articles")
    phrases = []
    if isinstance(arts, dict) and arts:
        full = "\n".join(v for v in arts.values() if isinstance(v, str))
        for m in CHUONG_TITLE.finditer(full):          # chương trước (chủ đề mạnh)
            phrases.append(_clean(m.group(1)))
        def _key(x):
            try: return int(x)
            except Exception: return 10**9
        for n in sorted(arts, key=_key):               # rồi tới tiêu đề Điều
            if isinstance(arts[n], str):
                phrases.append(_dieu_heading(arts[n]))
    # Hồ sơ Mục (văn kiện Đảng) hoặc phụ lục: lấy dòng tiêu đề IN HOA
    if not phrases:
        for key in ("sections", "muc", "items"):
            sec = record.get(key)
            if isinstance(sec, dict):
                phrases += [_clean(str(v).split("\n", 1)[0]) for v in sec.values()]
            elif isinstance(sec, list):
                for it in sec:
                    t = it.get("title") or it.get("tieu_de") if isinstance(it, dict) else str(it)
                    if t: phrases.append(_clean(str(t)))
        if not phrases:
            body = record.get("phu_luc") or record.get("text") or ""
            for ln in body.split("\n"):
                s = _clean(ln)
                if 4 <= len(s) <= 90 and s == s.upper() and any(c.isalpha() for c in s):
                    phrases.append(s)
    return phrases


def extract_keywords(record: dict) -> str:
    """record (legal_document.json) → chuỗi tukhoa đặc, đã dedup + cap. '' nếu không có móc."""
    seen, out, total = set(), [], 0
    for p in _collect(record):
        if not p or _is_stop(p):
            continue
        k = _ascii(p)
        if k in seen:
            continue
        seen.add(k)
        add = len(p) + len(SEP)
        if total + add > MAX_CHARS or len(out) >= MAX_PHRASES:
            break
        out.append(p); total += add
    return SEP.join(out)


# ----------------------------------------------------------------------------- selftest
def _selftest() -> int:
    rec = {
        "so_hieu": "73/2025/QH15", "title": "Luật Nhà giáo",
        "articles": {
            "1": "Điều 1. Phạm vi điều chỉnh\nLuật này quy định về nhà giáo…",
            "2": "Điều 2. Giải thích từ ngữ\nTrong Luật này…",
            "3": "Điều 3. Quyền và nghĩa vụ của nhà giáo\n1. Nhà giáo có quyền…",
            "10": "Điều 10. Chính sách tiền lương, phụ cấp đối với nhà giáo\n…",
            "10a": "Điều 10a. Chế độ làm việc của nhà giáo\n…",
            "50": "Điều 50. Hiệu lực thi hành\nLuật này có hiệu lực…",
        },
    }
    # Thực tế: split_articles luôn để "Điều N." ở ĐẦU; tiêu đề CHƯƠNG nằm ở ĐUÔI Điều TRƯỚC.
    rec["articles"]["2"] = (rec["articles"]["2"]
                            + "\nChương II\nQUYỀN, NGHĨA VỤ CỦA NHÀ GIÁO")
    kw = extract_keywords(rec)
    ph = [p.strip() for p in kw.split(SEP) if p.strip()]
    ok = True
    def chk(cond, msg):
        nonlocal ok
        print(("  ok  " if cond else " FAIL ") + msg); ok = ok and cond
    chk("QUYỀN, NGHĨA VỤ CỦA NHÀ GIÁO" in ph, "bắt được tiêu đề CHƯƠNG")
    chk(any("Quyền và nghĩa vụ của nhà giáo" == p for p in ph), "bắt tiêu đề Điều thực chất")
    chk(any("tiền lương" in p for p in ph), "giữ Điều phân biệt (tiền lương, phụ cấp)")
    chk(all(_ascii(p) not in _STOP for p in ph), "loại boilerplate (phạm vi/giải thích/hiệu lực)")
    chk(not any("Phạm vi điều chỉnh" == p for p in ph), "KHÔNG có 'Phạm vi điều chỉnh'")
    chk(not any("Hiệu lực thi hành" == p for p in ph), "KHÔNG có 'Hiệu lực thi hành'")
    chk(len(ph) == len(set(_ascii(p) for p in ph)), "dedup (không trùng)")
    chk(len(kw) <= MAX_CHARS and len(ph) <= MAX_PHRASES, "tôn trọng cap")
    # Điều profile rỗng → fallback IN HOA
    rec2 = {"so_hieu": "X", "articles": {}, "phu_luc": "PHỤ LỤC I\nDANH MỤC HÀNG HÓA\nabc\nQUY CÁCH KỸ THUẬT"}
    kw2 = extract_keywords(rec2)
    chk("DANH MỤC HÀNG HÓA" in kw2, "fallback IN HOA khi không có Điều")
    # idempotent
    chk(extract_keywords(rec) == kw, "idempotent (chạy lại cùng kết quả)")
    print("tukhoa demo:", kw)
    print("\nSELFTEST:", "PASS ✅" if ok else "FAIL ❌")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Bóc tukhoa tất định từ legal_document.json")
    ap.add_argument("--in", dest="inp", help="đường dẫn legal_document.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(_selftest())
    if not a.inp:
        ap.error("cần --in <legal_document.json> hoặc --selftest")
    rec = json.load(open(a.inp, encoding="utf-8"))
    print(extract_keywords(rec))


if __name__ == "__main__":
    main()
