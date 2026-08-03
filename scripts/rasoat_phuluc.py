#!/usr/bin/env python3
"""rasoat_phuluc.py — Sinh Phụ lục 03–07-BN từ BẢNG TỔNG HỢP PHÁT HIỆN (master).

Triết lý (xem references/QUY_TRINH_RA_SOAT_3_TANG.md, mục Pha 4): rà từng luật, dồn
phát hiện vào MỘT bảng tổng hợp, rồi sinh phụ lục MỘT LẦN ở cuối — dedup xuyên luật,
đánh số liên tục theo lĩnh vực. Đây là bước KẾT XUẤT, không phân tích lại.

Đầu vào: 1 file JSON master, HOẶC 1 thư mục chứa nhiều file .json (gộp tất cả).
Cấu trúc master: xem templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json
  {
    "co_quan": "...",
    "van_ban":  [ {linh_vuc, loai, so_hieu, ngay, ten, hieu_luc_tu, tinh_trang,
                   sua_doi_bo_sung, ghi_chu} ... ],   # -> Phụ lục I (03-BN)
    "noi_dung": [ {key, linh_vuc, van_ban, can_cu, phan_tich, hinh_thuc,
                   lo_trinh, tieu_chi, ghi_chu,
                   muc_chac_chan, anchor{cite,…}} ... ] # -> Phụ lục II..V (04..07-BN)
  }
  (v1.35.45 r209/H1b: `muc_chac_chan` + `anchor.cite` được nối vào cột Ghi chú khi kết xuất —
   field lạ khác vẫn bỏ qua như cũ.)

Định tuyến theo trường "hinh_thuc" (không phân biệt hoa thường, có dấu):
  - "ban hành mới"                              -> 05-BN (Phụ lục III)
  - "bãi bỏ toàn bộ"                            -> 06-BN (Phụ lục IV)
  - "tạm ngưng/ngừng toàn bộ"                   -> 07-BN (Phụ lục V)
  - "nghiên cứu" / "mục f" / "chờ"             -> KHÔNG vào phụ lục (đưa danh sách Mục F)
  - sửa đổi/bổ sung/thay thế/bãi bỏ một phần/tạm ngưng hiệu lực/giải thích/hướng dẫn
                                               -> 04-BN (Phụ lục II)
  - RỖNG hoặc ngoài từ vựng                    -> FAIL-CLOSED (không dựng phụ lục)

Dedup: theo "key" nếu có; nếu trống thì theo (van_ban + can_cu + hinh_thuc) chuẩn hóa.
Giữ bản đầu, gộp các văn bản trùng vào ghi chú, ĐẾM MỘT LẦN (đúng nguyên tắc Mục D).

KHÔNG gọi mạng, KHÔNG gọi NLM. Xuất Markdown (bảng) + tóm tắt số liệu Mục D.
Văn phong: tuân references/VAN_PHONG_HANH_CHINH.md (người nhập chịu trách nhiệm nội dung ô).

Cách dùng:
  rasoat_phuluc.py --in master.json --out-dir .
  rasoat_phuluc.py --in thu_muc_cac_luat/ --out-dir .   # gộp nhiều file
"""
import argparse, json, re, hashlib, datetime, sys, unicodedata
from pathlib import Path


def _norm(s):
    s = (s or "").strip().lower()
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s)


class HinhThucKhongHopLe(ValueError):
    """v1.36.45 (r311/DOC-01) — `hinh_thuc` RỖNG hoặc ngoài từ vựng. Trước đây hai ca này rơi
    ÂM THẦM về "04"; nay nổ ra để `main()` gom lại và FAIL-CLOSED."""


# v1.36.45 (r311/DOC-01) — nhóm 04 nay là NHẬN DIỆN DƯƠNG, không còn là cái sọt "còn lại".
# Cố ý khớp CHỨA (không khớp bằng) vì người nhập hay viết kèm phạm vi ("sửa đổi, bổ sung Điều 54"):
# giữ nguyên hành vi cho mọi giá trị HỢP LỆ đang chạy, chỉ chặn cái ngoài từ vựng.
_HINH_THUC_04 = ("sửa đổi", "bổ sung", "thay thế", "bãi bỏ một phần",
                 "tạm ngưng hiệu lực", "tạm ngừng hiệu lực", "giải thích", "hướng dẫn")


def route(hinh_thuc):
    """v1.36.45 (r311/DOC-01 — đo LIVE 02-08): FAIL-CLOSED thay cho fallback "04".

    Bằng chứng bản cũ: `route("ban hanh moi") == "04"` (đáng lẽ 05), `route("bai bo toan bo") == "04"`
    (đáng lẽ 06), `route("") == route("xyz la gi") == "04"`. Nghĩa là MỘT lỗi gõ dấu trong bảng master
    đủ để một đề xuất "ban hành mới" bị đếm sang Mẫu 04-BN — sai cả phụ lục lẫn số liệu Mục D, và
    KHÔNG có tín hiệu nào. Chính `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` (`_canh_bao_hinh_thuc`)
    và `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md:272` đã chốt "không để route() fallback im lặng".

    Chọn FAIL-CLOSED chứ KHÔNG bỏ dấu để đoán ý: `RASOAT_HOSO_LOOP.md:177` đã bắt buộc "CHỈ dùng giá
    trị trong `_vocab_hinh_thuc`" ⇒ đoán ý ở tầng định tuyến phụ lục là thêm nguồn chân lý thứ hai.
    Thứ tự nhánh là RÀNG BUỘC: "chờ bổ sung căn cứ" chứa "bổ sung" nên nhánh F PHẢI đứng trước 04."""
    h = _norm(hinh_thuc)
    if not h:
        raise HinhThucKhongHopLe("`hinh_thuc` RỖNG")
    if "ban hành mới" in h:
        return "05"
    if "bãi bỏ toàn bộ" in h:
        return "06"
    if ("tạm ngưng toàn bộ" in h) or ("tạm ngừng toàn bộ" in h):
        return "07"
    if ("nghiên cứu" in h) or ("mục f" in h) or h.startswith("chờ"):
        return "F"
    if any(k in h for k in _HINH_THUC_04):
        return "04"
    raise HinhThucKhongHopLe(f"{str(hinh_thuc)!r} ngoài từ vựng")


def load_master(p):
    """v1.35.49 (r213/b — sự cố PHA 4 SẬP đo LIVE 26-07): nhận CẢ khuôn bảng master lẫn khuôn §6
    `master/<unit>.json`, qua ĐÚNG hàm quy đổi của `tl rasoat-merge` (một nguồn chân lý).

    Bản cũ `van_ban += d.get("van_ban", [])` gặp khuôn §6 (`van_ban` là CHUỖI số hiệu) thì `+=` trải
    CHUỖI thành TỪNG KÝ TỰ rồi mới chết ở nơi khác ("'str' object has no attribute 'get'") — hỏng
    IM LẶNG trước, báo lỗi sai chỗ sau. Nay: khuôn lạ FAIL-CLOSED, nói rõ file nào."""
    path = Path(p)
    try:
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).resolve().parent))
        from tl_core.lookup_ops import _rasoat_la_ban_sao, _rasoat_merge_units, _rasoat_trung_lap
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"[rasoat_phuluc] không nạp được tl_core.lookup_ops ({e}) — chạy từ trong "
                         f"cây skill, hoặc dựng bảng master trước bằng `tl rasoat-merge`.")
    # r290 (RAS-15 — audit lõi 31-07): lọc BẢN SAO LƯU y như `tl rasoat-merge`. Bản cũ `glob("*.json")`
    # nuốt cả `*.bak*.json`, nên chạy TRỰC TIẾP script này trên cùng thư mục mà wrapper đã lọc sạch lại
    # đếm phát hiện HAI LẦN — chính sự cố r216 đo được 27-07 (40 → 53 phát hiện, 13 mã VD trùng), chỉ
    # khác đường vào. Cùng một hàm `_rasoat_la_ban_sao` để hai đường không thể trôi khỏi nhau.
    _tat_ca = sorted(path.glob("*.json")) if path.is_dir() else [path]
    _ban_sao = [f for f in _tat_ca if path.is_dir() and _rasoat_la_ban_sao(f.name)]
    files = [f for f in _tat_ca if f not in _ban_sao]
    if _ban_sao:
        print(f"[rasoat_phuluc] BỎ QUA {len(_ban_sao)} bản sao lưu: "
              f"{', '.join(f.name for f in _ban_sao)}", file=sys.stderr)
    docs = []
    for f in files:
        try:
            docs.append((f.name, json.loads(f.read_text(encoding="utf-8"))))
        except Exception as e:  # noqa: BLE001
            raise SystemExit(f"[rasoat_phuluc] {f.name}: JSON hỏng — {e}")
    merged = _rasoat_merge_units(docs)
    if merged.get("_bo_qua"):
        ten = ", ".join(str(x.get("nguon")) for x in merged["_bo_qua"])
        raise SystemExit(f"[rasoat_phuluc] KHUÔN KHÔNG NHẬN RA: {ten}. Chờ 1 trong 2: khuôn bảng "
                         f"master (van_ban=DANH SÁCH + noi_dung) hoặc khuôn §6 master/<unit>.json "
                         f"(phat_hien). File có CẢ hai khoá cũng bị từ chối — không đoán.")
    # r290 (RAS-06 — audit lõi 31-07): cổng TRÙNG r216 trước đây CHỈ có ở `tl rasoat-merge`. Chạy thẳng
    # script này với hai phiếu trùng `key`, `dedup()` lặng lẽ GIỮ BẢN ĐẦU và VỨT bản sau — mất phát hiện
    # mà không ai biết. Dùng chung `_rasoat_trung_lap` để phụ lục không bao giờ sinh ra từ nguồn đã trùng.
    _trung = _rasoat_trung_lap(docs)
    if _trung.get("key") or _trung.get("unit_id"):
        raise SystemExit(f"[rasoat_phuluc] TRÙNG LẶP GIỮA CÁC NGUỒN — không dựng phụ lục. "
                         f"key={[x.get('gia_tri') for x in _trung.get('key') or []]} "
                         f"unit_id={[x.get('gia_tri') for x in _trung.get('unit_id') or []]}. "
                         f"Mỗi phát hiện chỉ nằm ở MỘT phiếu, mỗi `unit_id` chỉ một file.")
    return merged.get("co_quan", ""), merged.get("van_ban", []), merged.get("noi_dung", [])


def dedup(items):
    seen, out = {}, []
    for it in items:
        k = (it.get("key") or "").strip()
        if not k:
            k = hashlib.md5(("|".join(_norm(it.get(x, "")) for x in
                            ("van_ban", "can_cu", "hinh_thuc"))).encode()).hexdigest()
        if k in seen:
            # nội dung trùng (vd cùng mâu thuẫn lộ ra từ 2 luật) — đếm 1 lần, gộp văn bản
            base = out[seen[k]]
            vb = it.get("van_ban", "")
            if vb and vb not in base.get("van_ban", ""):
                base["ghi_chu"] = (base.get("ghi_chu", "") +
                                   ("; " if base.get("ghi_chu") else "") +
                                   "Cũng phát sinh khi rà: " + vb)
            continue
        seen[k] = len(out)
        out.append(dict(it))
    return out


def group_by_linhvuc(items):
    g = {}
    for it in items:
        # r290 (RAS-16 — audit lõi 31-07): `dict.get(khoá, mặc_định)` CHỈ thay khi khoá VẮNG MẶT;
        # `linh_vuc: ""` (rất thường gặp — template để trống) lọt qua nguyên vẹn và sinh heading RỖNG
        # trong phụ lục trình. Phải chuẩn hoá theo GIÁ TRỊ, không theo sự tồn tại của khoá.
        g.setdefault((it.get("linh_vuc") or "").strip() or "(Chưa phân loại)", []).append(it)
    return g


def md_escape(s):
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def table_03(van_ban):
    L = ["| STT | Số, ký hiệu; ngày ban hành | Tên gọi/Trích yếu | Thời điểm có hiệu lực "
         "| VB sửa đổi, bổ sung, bãi bỏ một phần | Ghi chú |",
         "|---|---|---|---|---|---|"]
    n = 0
    for lv, rows in group_by_linhvuc(van_ban).items():
        L.append(f"| | **LĨNH VỰC {lv.upper()}** | | | | |")
        loai_g = {}
        for r in rows:
            # r290 (RAS-16): cùng lớp lỗi với `linh_vuc` ngay trên — `loai: ""` sinh dòng phân nhóm rỗng.
            loai_g.setdefault((r.get("loai") or "").strip() or "Bộ luật, luật của Quốc hội", []).append(r)
        for loai, rs in loai_g.items():
            L.append(f"| | *{loai}* | | | | |")
            for r in rs:
                n += 1
                sh = md_escape(r.get("so_hieu", ""))
                ngay = md_escape(r.get("ngay", ""))
                L.append("| {} | {} | {} | {} | {} | {} |".format(
                    n, (sh + (", ngày " + ngay if ngay else "")),
                    md_escape(r.get("ten", "")), md_escape(r.get("hieu_luc_tu", "")),
                    md_escape(r.get("sua_doi_bo_sung", "")),
                    md_escape(r.get("tinh_trang", "") + ("; " + r.get("ghi_chu") if r.get("ghi_chu") else ""))))
    return "\n".join(L), n


def table_xuly(items, kind):
    """04/05/06/07 — cùng khung 8 cột (đủ cho 04); 05 có cột khác nhưng dùng chung cho gọn."""
    L = ["| STT | Tên VB được rà soát | Căn cứ rà soát | Phân tích nội dung cần xử lý "
         "| Hình thức xử lý | Lộ trình | Tiêu chí | Ghi chú |",
         "|---|---|---|---|---|---|---|---|"]
    n = 0
    for lv, rows in group_by_linhvuc(items).items():
        L.append(f"| | **LĨNH VỰC {lv.upper()}** | | | | | | |")
        for r in rows:
            n += 1
            # v1.35.45 (r209/H1b) — phụ lục không được rơi mất mức chắc chắn + cite nguyên văn (bảng C):
            # nối vào cột Ghi chú; master vẫn là nguồn sự thật đầy đủ.
            gc = r.get("ghi_chu", "") or ""
            mcc = (r.get("muc_chac_chan") or "").strip()
            cite = ((r.get("anchor") or {}).get("cite") or "").strip()
            if mcc:
                gc = gc + ("; " if gc else "") + "mức: " + mcc
            if cite:
                gc = gc + ("; " if gc else "") + "cite: " + cite
            L.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                n, md_escape(r.get("van_ban", "")), md_escape(r.get("can_cu", "")),
                md_escape(r.get("phan_tich", "")), md_escape(r.get("hinh_thuc", "")),
                md_escape(r.get("lo_trinh", "")), md_escape(r.get("tieu_chi", "")),
                md_escape(gc)))
    return "\n".join(L), n


def _safe_output_dir(raw):
    out = Path(raw).expanduser().resolve()
    skill_root = Path(__file__).resolve().parent.parent
    if out == skill_root or skill_root in out.parents:
        raise ValueError(f"OUT_DIR_TRONG_CAY_SKILL:{out}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="file master.json hoặc thư mục .json")
    ap.add_argument("--out-dir", required=True,
                    help="thư mục output bắt buộc, phải nằm ngoài cây skill")
    ap.add_argument("--title", default="")
    a = ap.parse_args()

    try:
        out = _safe_output_dir(a.out_dir)
    except ValueError as e:
        raise SystemExit(f"[rasoat_phuluc] {e}") from e

    co_quan, van_ban, noi_dung = load_master(a.inp)
    noi_dung = dedup(noi_dung)

    # v1.36.45 (r311/DOC-01): kiểm TRỌN BỘ trước khi dựng, báo MỘT LẦN đủ mọi dòng sai — cùng lối
    # "nói rõ file nào" của load_master. Nổ giữa vòng lặp thì người nhập phải sửa từng dòng một lượt.
    _sai = []
    for _i, it in enumerate(noi_dung, 1):
        try:
            route(it.get("hinh_thuc"))
        except HinhThucKhongHopLe as e:
            _sai.append(f"  #{_i} key={it.get('key') or '(trống)'} · van_ban={it.get('van_ban') or '(trống)'} → {e}")
    if _sai:
        raise SystemExit(f"[rasoat_phuluc] HÌNH THỨC XỬ LÝ KHÔNG HỢP LỆ ({len(_sai)} dòng) — KHÔNG dựng "
                         "phụ lục. CHỈ dùng giá trị trong `_vocab_hinh_thuc` của "
                         "templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json:\n" + "\n".join(_sai))

    buckets = {"04": [], "05": [], "06": [], "07": [], "F": []}
    for it in noi_dung:
        buckets[route(it.get("hinh_thuc"))].append(it)

    today = datetime.date.today().isoformat()
    out.mkdir(parents=True, exist_ok=True)
    f = out / "PHU_LUC_03_07_BN_TONG_HOP.md"

    NAMES = {"04": ("Phụ lục II", "Mẫu 04-BN", "đề xuất sửa đổi, bổ sung; thay thế; tạm ngưng hiệu lực, bãi bỏ một phần"),
             "05": ("Phụ lục III", "Mẫu 05-BN", "đề xuất ban hành mới"),
             "06": ("Phụ lục IV", "Mẫu 06-BN", "đề xuất bãi bỏ toàn bộ"),
             "07": ("Phụ lục V", "Mẫu 07-BN", "đề xuất tạm ngưng hiệu lực toàn bộ")}

    P = [f"# PHỤ LỤC TỔNG HỢP KẾT QUẢ RÀ SOÁT (03–07-BN)",
         f"*Cơ quan rà soát: {co_quan or '……'} · lập ngày {today} · "
         f"{len(van_ban)} văn bản · {len(noi_dung)} nội dung (đã dedup)*",
         "\n> Văn phong tuân `references/VAN_PHONG_HANH_CHINH.md`. Đếm theo văn bản gốc, mỗi nội dung một lần.\n",
         "## Phụ lục I — Mẫu 03-BN — Danh mục VBQPPL thuộc đối tượng, phạm vi rà soát"]
    t03, n03 = table_03(van_ban); P.append(t03)

    counts = {"03": n03}
    for k in ("04", "05", "06", "07"):
        pl, mau, mota = NAMES[k]
        P.append(f"\n## {pl} — {mau} — Danh mục VBQPPL {mota}")
        if buckets[k]:
            tb, nb = table_xuly(buckets[k], k); P.append(tb); counts[k] = nb
        else:
            P.append("*Không có nội dung.*"); counts[k] = 0

    # r217 (lượt rà 8, 27-07): Mục F NAY LÀ MỘT PHỤ LỤC CÓ SỐ. Trước đây nó in ra dưới nhãn "Mục F
    # — KHÔNG vào phụ lục" trong khi Báo cáo rà soát lại hứa một "Phụ lục" cho đúng danh mục đó ⇒ bộ
    # hồ sơ trình không khớp tên với chính nó. ★Số VI/VII chứ KHÔNG phải III/IV: III/IV/V đã thuộc về
    # Mẫu 05/06/07-BN — chiếm lại số của chúng là đổi nghĩa một bộ biểu mẫu chuẩn chỉ vì trong hồ sơ
    # này chúng tình cờ rỗng.
    # Tên phải nói ĐÚNG cái nhóm này chứa: `route()` dồn vào đây CẢ "nghiên cứu, rút kinh nghiệm"
    # LẪN "chờ bổ sung căn cứ" — gọi tắt là "chưa đủ căn cứ kết luận" sẽ mô tả sai phần lớn số dòng.
    P.append("\n## Phụ lục VI — Danh mục nội dung đề nghị nghiên cứu, rút kinh nghiệm "
             "và nội dung chưa đủ căn cứ kết luận")
    if buckets["F"]:
        P.append("| STT | Mã | Văn bản | Nội dung | Căn cứ cần bổ sung |")
        P.append("|---|---|---|---|---|")
        for i, r in enumerate(buckets["F"], 1):
            P.append(f"| {i} | {md_escape(r.get('key',''))} | {md_escape(r.get('van_ban',''))} "
                     f"| {md_escape(r.get('phan_tich',''))} | {md_escape(r.get('can_cu',''))} |")
    else:
        P.append("*Không có.*")

    # r217 — Phụ lục VII: BẢNG TỔNG HỢP toàn bộ nội dung rà soát theo mã. Đây là bản TRÌNH BÀY của
    # bảng master; trước r217 chỉ tồn tại dưới dạng dữ liệu JSON, nên Báo cáo hứa một phụ lục mà
    # không có gì để đính kèm. Cột "Thuộc phụ lục" cho phép tra chéo ngược từ mã về nơi nó được đề
    # xuất xử lý — đối chiếu hai chiều với các phụ lục trên.
    _PL_CUA = {"04": "II", "05": "III", "06": "IV", "07": "V", "F": "VI"}
    P.append("\n## Phụ lục VII — Bảng tổng hợp nội dung rà soát (theo mã)")
    if noi_dung:
        P.append("| STT | Mã | Văn bản được rà soát | Căn cứ đối chiếu | Nội dung | Hình thức xử lý "
                 "| Mức | Thuộc phụ lục |")
        P.append("|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(noi_dung, 1):
            P.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                i, md_escape(r.get("key", "")), md_escape(r.get("van_ban", "")),
                md_escape(r.get("can_cu", "")), md_escape(r.get("phan_tich", "")),
                md_escape(r.get("hinh_thuc", "")), md_escape(r.get("muc_chac_chan", "")),
                _PL_CUA.get(route(r.get("hinh_thuc")), "")))
    else:
        P.append("*Không có.*")

    # Tóm tắt Mục D
    P.append("\n## Tóm tắt số liệu (đối chiếu Mục D Báo cáo)")
    P.append(f"- Tổng văn bản rà soát (Mẫu 03-BN): **{counts['03']}**")
    P.append(f"- Đề xuất sửa đổi, bổ sung… (Mẫu 04-BN): **{counts['04']}**")
    P.append(f"- Đề xuất ban hành mới (Mẫu 05-BN): **{counts['05']}**")
    P.append(f"- Đề xuất bãi bỏ toàn bộ (Mẫu 06-BN): **{counts['06']}**")
    P.append(f"- Đề xuất tạm ngưng toàn bộ (Mẫu 07-BN): **{counts['07']}**")
    P.append(f"- Nội dung nghiên cứu, rút kinh nghiệm + chưa đủ căn cứ kết luận (Phụ lục VI): **{len(buckets['F'])}**")
    P.append(f"- Tổng nội dung rà soát (Phụ lục VII): **{len(noi_dung)}**")

    f.write_text("\n".join(P), encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(f), "counts": counts,
                      "muc_f": len(buckets["F"]), "phu_luc_vi": len(buckets["F"]),
                      "phu_luc_vii": len(noi_dung), "n_van_ban": len(van_ban),
                      "n_noi_dung_dedup": len(noi_dung)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
