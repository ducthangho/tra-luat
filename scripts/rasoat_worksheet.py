#!/usr/bin/env python3
"""rasoat_worksheet.py — Sinh PHIẾU CÔNG TÁC RÀ SOÁT từ cache (Tầng 1 tự động, 0 NLM).

Đọc cache doc JSON (đã ingest_to_cache), quét TẤT ĐỊNH từng Điều theo các dấu hiệu
"Điều rủi ro cao" (giao quy định chi tiết · điều kiện ĐTKD/thủ tục · từ định tính · liên luật
· vấn đề mới), gắn cờ T2/T4/T5/T6/LL và tầng (HIGH/LOW), rồi xuất:
  1) Bảng phân tầng rủi ro (mỗi Điều một dòng, cờ tick được)        -> phục vụ Tầng 1
  2) Khung theo dõi tiến độ (đơn vị rà × trạng thái × call NLM)      -> phiếu công tác
  3) Khung NHẬT KÝ TRUY VẤN NLM (CSV)                               -> truy vết Tầng 2/3

KHÔNG gọi NLM, KHÔNG gọi mạng. Chỉ đọc cache. Heuristic là GỢI Ý phân tầng, người rà soát
quyết định cuối cùng. Mục tiêu: tập trung công sức vào nhóm HIGH, bỏ qua boilerplate.

Cách dùng:
  rasoat_worksheet.py --so-hieu 18/VBHN-VPQH \
      [--variant consolidated] [--cache-dir ~/.tra_luat_cache] \
      [--out-dir .] [--title "Bộ luật Lao động (VBHN 18/VPQH)"]
"""
import argparse, json, os, re, csv, datetime
from pathlib import Path

DEFAULT_CACHE = os.path.expanduser("~/.tra_luat_cache")

# --- Dấu hiệu TẤT ĐỊNH cho từng tiêu chí (mỗi cờ = danh sách pattern, IGNORECASE) ---
SIGNALS = {
    "T2_giao_chi_tiet": [
        r"quy định chi tiết Điều này", r"Chính phủ quy định chi tiết",
        r"Chính phủ quy định", r"Bộ trưởng[^.]{0,40}quy định",
        r"theo quy định của Chính phủ", r"do Chính phủ quy định",
        r"quy định chi tiết(?: và)? hướng dẫn thi hành", r"hướng dẫn thi hành",
    ],
    "T4_dieu_kien_tthc": [
        r"kinh doanh có điều kiện", r"ngành, nghề[^.]{0,30}có điều kiện",
        r"[Gg]iấy phép", r"cấp(?:, cấp lại| lại)?[^.]{0,30}[Gg]iấy phép",
        r"thu hồi[^.]{0,20}[Gg]iấy phép", r"ký quỹ", r"đăng ký",
        r"điều kiện(?: để| được)?[^.]{0,20}(?:hoạt động|hành nghề|cấp)",
        r"khai trình", r"báo cáo định kỳ",
    ],
    "T5_dinh_tinh": [
        r"lý do chính đáng", r"trường hợp khác(?:\s+do)?", r"trường hợp cần thiết",
        r"tính chất đặc thù", r"đặc biệt nghiêm trọng", r"thiệt hại nghiêm trọng",
        r"công việc có tính chất đặc biệt", r"tình tiết phức tạp",
        r"thường xuyên không hoàn thành", r"khi cần thiết", r"biện pháp khác",
    ],
    "T6_van_de_moi": [
        r"điện tử", r"thông điệp dữ liệu", r"nền tảng", r"công nghệ số",
        r"giao dịch điện tử", r"chuyển đổi số", r"làm việc từ xa", r"làm tại nhà",
    ],
    "LL_lien_luat": [
        r"pháp luật về bảo hiểm xã hội", r"pháp luật về (?:công đoàn|việc làm)",
        r"pháp luật về an toàn, vệ sinh lao động", r"pháp luật về đầu tư",
        r"pháp luật về (?:giáo dục nghề nghiệp|bảo hiểm y tế)",
        r"theo quy định của (?:Luật|Bộ luật)[^.]{0,40}",
        r"Luật[^.]{0,5}\d+/\d{4}", r"điều ước quốc tế",
        r"tổ chức đại diện người lao động", r"\bcông đoàn\b",
        r"thương lượng tập thể", r"thỏa ước lao động tập thể", r"đình công",
        r"bảo hiểm (?:xã hội|thất nghiệp|y tế|tai nạn)",
    ],
}
FLAG_ORDER = ["T2_giao_chi_tiet", "T4_dieu_kien_tthc", "T5_dinh_tinh", "T6_van_de_moi", "LL_lien_luat"]
FLAG_SHORT = {"T2_giao_chi_tiet": "T2-giao", "T4_dieu_kien_tthc": "T4-ĐK/TTHC",
              "T5_dinh_tinh": "T5-định tính", "T6_van_de_moi": "T6-mới", "LL_lien_luat": "LL-liên luật"}

# Điều "boilerplate" hạ tầng — luôn LOW dù trùng từ khóa định tính lặt vặt
BOILERPLATE_TITLE = re.compile(r"(Phạm vi điều chỉnh|Đối tượng áp dụng|Giải thích từ ngữ|"
                               r"Hiệu lực thi hành|Quy định chuyển tiếp|Điều khoản thi hành|"
                               r"Trách nhiệm thi hành|Tổ chức thực hiện)", re.I)


def load_doc(so_hieu, variant, cache_dir):
    key = re.sub(r"[^a-z0-9]+", "-", so_hieu.lower()).strip("-") + "--" + variant
    p = Path(cache_dir) / "docs" / (key + ".json")
    if not p.exists():
        raise SystemExit(f"Không thấy cache: {p}\n"
                         f"  -> dựng cache trước: `tl cache-build {so_hieu} --gdoc-id <id>` "
                         f"(hoặc `--input <file>`); rồi chạy lại worksheet.")
    return json.loads(p.read_text(encoding="utf-8")), key


def article_items(doc):
    arts = doc.get("articles") or {}
    if isinstance(arts, dict):
        def keyf(k):
            m = re.match(r"\d+", str(k)); return int(m.group()) if m else 9999
        return [(str(k), arts[k]) for k in sorted(arts, key=keyf)]
    out = []
    for a in arts:
        if isinstance(a, str):
            m = re.match(r"Điều\s+(\d+)\.", a); out.append((m.group(1) if m else "?", a))
        elif isinstance(a, dict):
            out.append((str(a.get("number") or a.get("no") or "?"),
                        a.get("text") or a.get("body") or ""))
    return out


def short_title(text, limit=120):
    # #9: lấy TRỌN tiêu đề trên dòng rồi rút gọn ở RANH GIỚI TỪ (không cắt giữa chữ) + dấu … báo đã rút.
    # r296 (P16-F15, cùng họ): `\d+\.` đòi dấu chấm NGAY sau số ⇒ "Điều 7a. …" không khớp và phiếu rà soát
    # ra tiêu đề RỖNG cho mọi điều được chèn thêm.
    m = re.match(r"\s*Điều\s+\d+[a-zđ]*\.\s*([^\n]+)", text, re.I)
    if not m:
        return ""
    s = m.group(1).strip().rstrip(". ")
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(" ", 1)[0].rstrip(",;:· ")
    return (cut or s[:limit]) + "…"


def scan(text):
    flags = []
    for f in FLAG_ORDER:
        if any(re.search(p, text, re.I) for p in SIGNALS[f]):
            flags.append(f)
    return flags


def _safe_output_dir(raw):
    out = Path(raw).expanduser().resolve()
    skill_root = Path(__file__).resolve().parent.parent
    if out == skill_root or skill_root in out.parents:
        raise ValueError(f"OUT_DIR_TRONG_CAY_SKILL:{out}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so-hieu", required=True)
    ap.add_argument("--variant", default="consolidated")
    ap.add_argument("--cache-dir", default=DEFAULT_CACHE)
    ap.add_argument("--out-dir", required=True,
                    help="thư mục output bắt buộc, phải nằm ngoài cây skill")
    ap.add_argument("--title", default="")
    a = ap.parse_args()

    try:
        out = _safe_output_dir(a.out_dir)
    except ValueError as e:
        raise SystemExit(f"[rasoat_worksheet] {e}") from e

    doc, key = load_doc(a.so_hieu, a.variant, a.cache_dir)
    title = a.title or doc.get("title") or a.so_hieu
    items = article_items(doc)

    rows, n_deep, n_cross = [], 0, 0
    HARD = {"T2_giao_chi_tiet", "T4_dieu_kien_tthc", "T5_dinh_tinh", "T6_van_de_moi"}
    for no, text in items:
        st = short_title(text)
        fl = scan(text)
        if BOILERPLATE_TITLE.search(st or ""):
            fl = [f for f in fl if f in ("T2_giao_chi_tiet", "LL_lien_luat")]  # giữ cờ "cứng"
        has_hard = any(f in HARD for f in fl)
        has_soft = "LL_lien_luat" in fl
        if has_hard:
            tier = "SÂU"; n_deep += 1            # → Tầng 3: đào sâu theo Điều
        elif has_soft:
            tier = "ĐỐI CHIẾU"; n_cross += 1     # → Tầng 2: lô đối chiếu chéo với luật liên quan
        else:
            tier = "—"
        rows.append((no, st, fl, tier))
    n_low = len(items) - n_deep - n_cross

    today = datetime.date.today().isoformat()
    out.mkdir(parents=True, exist_ok=True)

    # ---- (1)+(2) PHIẾU CÔNG TÁC (markdown) ----
    ws = out / f"PHIEU_CONG_TAC_{re.sub(r'[^A-Za-z0-9]+','_',a.so_hieu)}.md"
    L = []
    L.append(f"# PHIẾU CÔNG TÁC RÀ SOÁT — {title}")
    L.append(f"*Số hiệu: {a.so_hieu} · cache_key: {key} · lập ngày {today} · tổng {len(items)} Điều · "
             f"SÂU (đào sâu Tầng 3): {n_deep} · ĐỐI CHIẾU (chéo Tầng 2): {n_cross} · thấp: {n_low}*")
    L.append("\n> Cờ là GỢI Ý phân tầng tất định (0 NLM), **để ƯU TIÊN công sức — KHÔNG loại trừ Điều khỏi rà soát**.")
    L.append("> • **SÂU** = có cờ cứng (giao chi tiết/điều kiện ĐTKD/định tính/mới) → đào sâu theo Điều (Tầng 3) rồi Claude so cache.")
    L.append("> • **ĐỐI CHIẾU** = chạm chủ đề luật liên quan → đưa vào lô đối chiếu chéo (Tầng 2) với căn cứ tương ứng.")
    L.append("> • Mức **'—'** vẫn được quét thô Tầng 2; xung đột liên văn bản (vd Điều 177 ↔ Luật Công đoàn) do Tầng 2 bắt, không phụ thuộc cờ Tầng 1.\n")
    L.append("## 1. BẢNG PHÂN TẦNG RỦI RO (Tầng 1)")
    L.append("| Điều | Tiêu đề | Cờ tiêu chí | Mức | Đã quét T2 | Đã đào T3 | Phát hiện? |")
    L.append("|---|---|---|---|:--:|:--:|:--:|")
    for no, st, fl, tier in rows:
        tags = ", ".join(FLAG_SHORT[f] for f in fl) if fl else "—"
        mark = {"SÂU": "**SÂU**", "ĐỐI CHIẾU": "ĐỐI CHIẾU", "—": "—"}[tier]
        L.append(f"| {no} | {st or '—'} | {tags} | {mark} | ☐ | ☐ | ☐ |")
    L.append("\n## 2. THEO DÕI TIẾN ĐỘ THEO ĐƠN VỊ RÀ (người rà soát điền)")
    L.append("| Đơn vị rà (nhóm Chương/chế định) | Điều thuộc nhóm | Số Điều SÂU | Trạng thái | Call NLM đã dùng | Ghi chú |")
    L.append("|---|---|:--:|---|:--:|---|")
    for _ in range(6):
        L.append("|  |  |  | ☐ chưa ▢ đang ▢ xong |  |  |")
    L.append(f"\n*Ngân sách NLM khuyến nghị: ≤6 sub-question/phiên; tổng ~11–14 (lưới thô Tầng 2) + Tầng 3 theo số Điều SÂU. "
             f"SÂU = {n_deep}, ĐỐI CHIẾU = {n_cross}.*")
    L.append("\n## 3. NHẬT KÝ TRUY VẤN NLM\nXem file CSV kèm theo: `" + ws.with_name('NHAT_KY_NLM_'+re.sub(r'[^A-Za-z0-9]+','_',a.so_hieu)+'.csv').name + "`")
    ws.write_text("\n".join(L), encoding="utf-8")

    # ---- (3) NHẬT KÝ NLM (CSV) ----
    log = out / f"NHAT_KY_NLM_{re.sub(r'[^A-Za-z0-9]+','_',a.so_hieu)}.csv"
    with log.open("w", newline="", encoding="utf-8-sig") as fcsv:
        w = csv.writer(fcsv)
        w.writerow(["STT", "Tầng (2/3)", "Phiên/conversation_id", "source_ids (scope)",
                    "Câu hỏi gửi NLM", "Điều NLM định vị", "Có trích «...»?",
                    "Verify (pass/normalized/failed)", "Nguồn verify (cache cite)",
                    "Tiêu chí", "Kết luận sơ bộ (Claude)", "Ngày"])
        w.writerow(["1", "", "", "", "", "", "", "", "", "", "", today])
    print(json.dumps({"ok": True, "so_hieu": a.so_hieu, "n_articles": len(items),
                      "n_deep": n_deep, "n_cross": n_cross, "n_low": n_low,
                      "worksheet": str(ws), "nlm_log": str(log)},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
