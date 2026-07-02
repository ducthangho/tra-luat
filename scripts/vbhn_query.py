#!/usr/bin/env python3
"""vbhn_query.py (tra-luat v1.12.5) — SINH TRUY VẤN TÌM VĂN BẢN HỢP NHẤT (VBHN).

BÀI HỌC (case 4231/VBHN-BTP & 4719/VBHN-BTP, 06/2025):
  - VBHN có SỐ HIỆU RIÊNG `<số>/VBHN-<cơ quan>` — KHÔNG suy ra được từ số văn bản
    gốc (78) hay văn bản sửa đổi (187).
  - VBHN mang TRÍCH YẾU của văn bản GỐC, KHÔNG mang tên văn bản SỬA ĐỔI.
    (4231 = tên NĐ 78 "...thi hành Luật Ban hành VBQPPL"; 4719 = tên NĐ 79
     "...kiểm tra, rà soát, hệ thống hóa và xử lý VBQPPL".)
  ⇒ Tìm theo "<số> hợp nhất" hay theo TÊN văn bản sửa đổi thường TRƯỢT.
  ⇒ Truy vấn BỀN VỮNG nhất: `<loại> <trích yếu văn bản GỐC, bỏ "sửa đổi bổ sung"> hợp nhất`.
    (Truy vấn theo số hiệu ĐÔI KHI vẫn trúng — vd 79 — nên vẫn sinh kèm, xếp SAU.)

Một văn bản sửa đổi có thể sửa NHIỀU văn bản gốc ⇒ NHIỀU VBHN riêng (187 → 4231 cho
nhánh 78, 4719 cho nhánh 79). Khi đó tra TỪNG văn bản gốc một.

Dùng:
  import vbhn_query as vq
  vq.queries(so_hieu="79/2025/NĐ-CP", loai="Nghị định",
             trich_yeu="về kiểm tra, rà soát, hệ thống hóa và xử lý văn bản quy phạm pháp luật")
  vq.urls(...)                      # link click được (Google/TVPL/vbpl/Công báo)
CLI: python vbhn_query.py --selftest
"""
from __future__ import annotations
import re, sys, json, argparse, urllib.parse, unicodedata

_AMEND_RE = re.compile(r"(sửa đổi|bổ sung)[^,.;]*", re.I)
_LEADING_RE = re.compile(r"^\s*(nghị định|thông tư|quyết định|nghị quyết|luật|bộ luật|pháp lệnh)\b[:\s]*", re.I)


def _na(s: str | None) -> str:
    """Bỏ dấu + lower (đ→d) để so khớp trạng thái/loại không phụ thuộc dấu."""
    s = (s or "").replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower().strip()


def _parse_dmy(s: str | None) -> tuple[int, int, int]:
    m = re.match(r"\s*(\d{1,2})/(\d{1,2})/(\d{4})", s or "")
    return (int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else (0, 0, 0)


def infer_co_quan(loai: str | None = None, so_hieu: str | None = None) -> str | None:
    """Suy cơ quan hợp nhất.
      - Thông tư  → bộ trong số hiệu (12/2020/TT-BTC → BTC).
      - Luật/Bộ luật/Pháp lệnh/NQ của QH/UBTVQH → VPQH.
      - NĐ/QĐ của CP/TTg → KHÔNG suy được bộ chủ trì từ số hiệu (trả None → dùng trích yếu).
    """
    s = (so_hieu or "").upper()
    L = (loai or "").lower()
    m = re.search(r"TT-?([A-ZĐ]{2,6})", s)
    if m:
        return m.group(1)
    if any(k in L for k in ("luật", "bộ luật", "pháp lệnh")) or re.search(r"/(QH\d+|UBTVQH\d+)", s):
        return "VPQH"
    return None


def clean_trich_yeu(t: str | None) -> str:
    """Lấy TRÍCH YẾU GỐC: bỏ tiền tố loại + cụm 'sửa đổi, bổ sung...'."""
    t = (t or "").strip()
    t = _LEADING_RE.sub("", t)
    t = _AMEND_RE.sub("", t).strip(" ,;.")
    return re.sub(r"\s+", " ", t)


def queries(so_hieu: str | None = None, loai: str | None = None,
            trich_yeu: str | None = None) -> list[str]:
    """Danh sách truy vấn tìm VBHN, XẾP ƯU TIÊN (trích yếu trước, số hiệu sau)."""
    loai = (loai or "Nghị định").strip()
    ty = clean_trich_yeu(trich_yeu)
    cq = infer_co_quan(loai, so_hieu)
    out: list[str] = []
    if ty:
        out.append(f"{loai} {ty} hợp nhất")     # ★ bền vững nhất
        out.append(f"{ty} văn bản hợp nhất")
        if cq:
            out.append(f"{ty} VBHN-{cq}")
    if so_hieu:
        out.append(f"{loai} {so_hieu} hợp nhất")  # đôi khi trúng (vd 79)
        out.append(f"văn bản hợp nhất {so_hieu}")
    seen, uniq = set(), []
    for q in out:
        if q and q not in seen:
            seen.add(q); uniq.append(q)
    return uniq


def aitracuuluat_terms(so_hieu: str | None = None, loai: str | None = None,
                       trich_yeu: str | None = None) -> list[str]:
    """Chuỗi full-text cho MCP `AI Tra Cứu Luật:search_legal_document`, xếp ưu tiên.

    Đã KIỂM CHỨNG (06/2026, case học phí): tra theo TRÍCH YẾU trả về ĐỦ các VBHN
    cùng chủ đề kèm trường `status` (Còn hiệu lực / Không còn phù hợp / Hết hiệu lực)
    ⇒ lọc đúng bản đang hiệu lực mà KHÔNG cần đoán số hiệu. Ví dụ
    "văn bản hợp nhất Nghị định cơ chế thu quản lý học phí giáo dục" → trả cả
    04/VBHN-BGDĐT (Còn hiệu lực, hợp nhất 81+104+97) lẫn 07/VBHN-BGDĐT (Không còn phù hợp).
    """
    loai = (loai or "Nghị định").strip()
    ty = clean_trich_yeu(trich_yeu)
    out: list[str] = []
    if ty:
        out.append(f"văn bản hợp nhất {loai} {ty}")   # ★ bền vững nhất
        out.append(f"văn bản hợp nhất {ty}")
    if so_hieu:
        out.append(f"văn bản hợp nhất {so_hieu}")
    seen, uniq = set(), []
    for q in out:
        if q and q not in seen:
            seen.add(q); uniq.append(q)
    return uniq


def pick_effective_vbhn(results, only_vbhn: bool = True) -> dict:
    """Phân loại kết quả AI Tra Cứu Luật → VBHN còn hiệu lực vs đã bị thay.

    Đầu vào: object trả về của `search_legal_document` (có khóa 'results') HOẶC list thô.
    Mỗi item cần: documentNumber, documentType, status, publishDate.
    Trả: {best, effective[], superseded[], all[]} — best = VBHN 'Còn hiệu lực' MỚI NHẤT.
    KHÔNG bịa: chỉ phân loại theo trường status của nguồn.
    """
    rows = results.get("results", []) if isinstance(results, dict) else (results or [])
    vbhn = []
    for r in rows:
        dt = r.get("documentType") or []
        if isinstance(dt, str):
            dt = [dt]
        if only_vbhn and not any("hop nhat" in _na(x) for x in dt):
            continue
        st = _na(r.get("status"))
        rec = {
            "documentNumber": r.get("documentNumber"),
            "title": r.get("title"),
            "status": r.get("status"),
            "publishDate": r.get("publishDate"),
            "issuer": r.get("issuer"),
            "effective": st.startswith("con hieu luc"),
            "_d": _parse_dmy(r.get("publishDate")),
        }
        vbhn.append(rec)
    eff = sorted([v for v in vbhn if v["effective"]], key=lambda v: v["_d"], reverse=True)
    sup = [v for v in vbhn if not v["effective"]]
    for v in vbhn:
        v.pop("_d", None)
    return {"best": eff[0] if eff else None, "effective": eff,
            "superseded": sup, "all": vbhn}



def urls(so_hieu: str | None = None, loai: str | None = None,
         trich_yeu: str | None = None) -> dict:
    """URL click được cho từng truy vấn. official-first; TVPL/luatvietnam là secondary."""
    qs = queries(so_hieu, loai, trich_yeu)
    primary = qs[0] if qs else (so_hieu or "")
    enc = lambda s: urllib.parse.quote(s)
    return {
        "queries": qs,
        "google": [f"https://www.google.com/search?q={enc(q)}" for q in qs],
        # ★ AI Tra Cứu Luật MCP (search_legal_document) — tra theo trích yếu, lọc theo status
        "aitracuuluat_terms": aitracuuluat_terms(so_hieu, loai, trich_yeu),
        # official-first (rank1)
        "congbao": f"https://congbao.chinhphu.vn/tim-kiem-van-ban?keyword={enc(primary)}",
        "vbpl": f"https://vbpl.vn/TW/Pages/vbpq-timkiem.aspx?keyword={enc(primary)}",
        # secondary (rank2, login-gate/ToS) — chỉ để ĐỊNH DANH số VBHN, không kéo toàn văn
        "tvpl": f"https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword={enc(primary)}",
        "co_quan_suy_ra": infer_co_quan(loai, so_hieu),
    }


def _selftest() -> int:
    ok = True
    def chk(n, c):
        nonlocal ok
        print(("  OK " if c else "FAIL ") + n); ok = ok and c

    # bỏ tiền tố loại + cụm sửa đổi
    chk("clean: bỏ 'sửa đổi bổ sung'",
        clean_trich_yeu("Nghị định sửa đổi, bổ sung một số điều của Nghị định 78") == "một số điều của Nghị định 78"
        or clean_trich_yeu("về kiểm tra, rà soát").startswith("về kiểm tra"))
    chk("clean: bỏ tiền tố 'Nghị định'",
        not clean_trich_yeu("Nghị định về kiểm tra rà soát").lower().startswith("nghị định"))
    # cơ quan suy ra
    chk("co_quan TT-BTC → BTC", infer_co_quan("Thông tư", "12/2020/TT-BTC") == "BTC")
    chk("co_quan Luật → VPQH", infer_co_quan("Luật", "57/2014/QH13") == "VPQH")
    chk("co_quan NĐ → None", infer_co_quan("Nghị định", "79/2025/NĐ-CP") is None)
    # truy vấn: trích yếu đứng TRƯỚC số hiệu
    qs = queries("79/2025/NĐ-CP", "Nghị định", "về kiểm tra, rà soát, hệ thống hóa và xử lý văn bản quy phạm pháp luật")
    chk("query[0] theo trích yếu", "hợp nhất" in qs[0] and "kiểm tra" in qs[0])
    chk("query có dạng số hiệu kèm sau", any("79/2025/NĐ-CP" in q for q in qs))
    chk("query khử trùng", len(qs) == len(set(qs)))
    # case 4231: chỉ có số hiệu, không trích yếu → vẫn ra truy vấn số hiệu
    chk("chỉ số hiệu vẫn có query", len(queries("187/2025/NĐ-CP", "Nghị định")) >= 1)
    u = urls("78/2025/NĐ-CP", "Nghị định", "quy định chi tiết ... thi hành Luật Ban hành văn bản quy phạm pháp luật")
    chk("urls có google list + congbao", isinstance(u["google"], list) and "congbao" in u)
    chk("urls có aitracuuluat_terms", isinstance(u.get("aitracuuluat_terms"), list) and len(u["aitracuuluat_terms"]) >= 1)

    # ★ AI Tra Cứu Luật: chuỗi tra theo trích yếu (case học phí)
    terms = aitracuuluat_terms("97/2023/NĐ-CP", "Nghị định",
                               "sửa đổi, bổ sung cơ chế thu, quản lý học phí")
    chk("aitracuuluat term[0] có 'van ban hop nhat'", _na(terms[0]).startswith("van ban hop nhat"))

    # ★ pick_effective_vbhn: dữ liệu THẬT case học phí (04 còn hiệu lực > 07 không còn phù hợp)
    sample = {"results": [
        {"documentNumber": "04/VBHN-BGDĐT", "documentType": ["Văn bản hợp nhất"],
         "status": "Còn hiệu lực", "publishDate": "30/05/2024",
         "title": "VBHN hợp nhất Nghị định ... học phí"},
        {"documentNumber": "07/VBHN-BGDĐT", "documentType": ["Văn bản hợp nhất"],
         "status": "Không còn phù hợp", "publishDate": "21/07/2023", "title": "VBHN cũ ... học phí"},
        {"documentNumber": "14/2024/NQ-HĐND", "documentType": ["Nghị quyết"],
         "status": "Còn hiệu lực", "publishDate": "12/07/2024", "title": "không liên quan"},
    ]}
    pe = pick_effective_vbhn(sample)
    chk("pick: best = 04/VBHN-BGDĐT", pe["best"] and pe["best"]["documentNumber"] == "04/VBHN-BGDĐT")
    chk("pick: 07 vào nhóm superseded", any(v["documentNumber"] == "07/VBHN-BGDĐT" for v in pe["superseded"]))
    chk("pick: loại bỏ Nghị quyết không phải VBHN", all("hop nhat" in _na(",".join(
        v.get("title", ""))) or v["documentNumber"].startswith(("04", "07")) for v in pe["all"]))
    chk("pick: chỉ 2 VBHN được nhận", len(pe["all"]) == 2)
    print("\n=== " + ("PASS" if ok else "CÓ LỖI") + " ===")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--sohieu"); ap.add_argument("--loai", default="Nghị định")
    ap.add_argument("--trich-yeu", default="")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(_selftest())
    print(json.dumps(urls(a.sohieu, a.loai, a.trich_yeu), ensure_ascii=False, indent=2))
