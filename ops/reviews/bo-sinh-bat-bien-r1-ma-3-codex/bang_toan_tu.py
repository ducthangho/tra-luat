#!/usr/bin/env python3
"""Bảng MỆNH ĐỀ × TOÁN TỬ cho các chốt mà packet bo-sinh-bat-bien thêm vào hai tệp test. Công cụ ĐO dev-side, không vào kho.

Với TỪNG mệnh đề chốt, áp một tập toán tử CỐ ĐỊNH lên BẢN SAO (clone rời do công cụ tự dựng dưới --ra; không ghi vào <goc>), rồi chạy
các ca phản chứng. Một đột biến là GIET khi có ca phản chứng thoát rc 3 và in `DO:<ca phản chứng>:`; SONG khi mọi ca phản chứng rc 0;
HONG khi có ca thoát mã khác 0/3 mà không ca nào giết (lỗi vô can KHÔNG được tính là giết).

  python3 -B bang_toan_tu.py --goc <clone tại SHA ứng viên> --ra <thư mục ra> [--song-song 4] [--loc <chuỗi con của id>]

Toán tử (cột): bo (bỏ nguyên mệnh đề) · ge (== → >=, hoặc > → >=) · le (== → <=) · ne (== → !=, != → ==) · gt/lt (!= → > / <) ·
dao (đảo `not`, hoặc đảo phép so) · cong1 / tru1 (hằng +1 / −1) · or (and → or) · yeu (all ↔ any, quan hệ chứa → dạng yếu hơn).
Ô không có trong bảng M của một mệnh đề = `khong_ap_dung`, lý do ghi ở KAD. Đột biến khai TUONG_DUONG phải kèm lập luận ở TD và phải SONG
thật (nếu bị giết thì ghi `GIET (khai tuong duong)` — không lỗi). rc 0 chỉ khi: baseline xanh, 0 HONG, mọi SONG đều có lập luận tương đương,
mọi neo xuất hiện đúng một lần.
"""
import argparse
import concurrent.futures as cf
import json
import subprocess
import sys
from pathlib import Path

B, A = "ops/land_evidence_nguon_test.py", "ops/gate_output_doi_chieu_test.py"
C38, C39, C40, A136 = ("c38_c36_do_khi_bang_cua_dot_a_mat_ca", "c39_c37_do_khi_bo_sinh_lech_mien",
                       "c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o", "a136_a135_do_khi_bo_sinh_lech_mien")
CA_PC = {B: (C39, C40, C38), A: (A136,)}   # thứ tự chạy; mọi ca đều chạy tới khi có ca giết
OPS = ("bo", "ge", "le", "ne", "gt", "lt", "dao", "cong1", "tru1", "or", "yeu")

C36_SO = "bang(rc == 0 and dem[0] - truoc == mong,"
C36_KN = "bang(len(van_tay) == mong - lap,"
C36_BMP = "bang(any(ord(c) > 0xFFFF for c in thay),"
C37 = "bang(len(vu_tru) == 158 and len(set(vu_tru)) == 158 and not lech,"
C37_LECH = 'lech = [loai for loai in LOAI if bmp.count(loai) != (loai != "Cs")]'
C37_BMP = "bmp = [unicodedata.category(c) for c in ngoai if ord(c) <= 0xFFFF]"
C37_O = "bang(len(o) == 648,"
A_SO, A_VANG, A_LAP = '("so_phan_tu", len(ra) == so)', '("category_vang", sorted(set(LOAI_UNICODE) - set(bmp)) == sorted(vang))', '("lap_category", len(bmp) == len(set(bmp)))'
A_CAM, A_80 = '("thuoc_cam", not any(c in cam for c in ra))', '("tu_0080", all(ord(c) >= 0x80 for c in ra))'
A_CUOI = '("cuoi_ngoai_bmp", bool(ra) and ord(ra[-1]) > 0xFFFF and len(ra) - len(bmp) == 1)'
A_BMP = "bmp = [category(c) for c in ra if ord(c) <= 0xFFFF]"

# (id mệnh đề, tệp, ca phản chứng chạy trước, neo, {toán tử: văn bản thay neo})
M = [
    ("c36.so_phan_tu  `dem[0] - truoc == mong`", B, C40, C36_SO, {
        "bo": "bang(rc == 0,", "ge": C36_SO.replace("== mong", ">= mong"), "le": C36_SO.replace("== mong", "<= mong"),
        "ne": C36_SO.replace("== mong", "!= mong"), "cong1": C36_SO.replace("== mong", "== mong + 1"), "tru1": C36_SO.replace("== mong", "== mong - 1"),
        "or": C36_SO.replace("rc == 0 and", "rc == 0 or")}),
    ("c36.khac_nhau  `len(van_tay) == mong - lap`", B, C40, C36_KN, {
        "bo": "bang(True,", "ge": C36_KN.replace("==", ">="), "le": C36_KN.replace("==", "<="), "ne": C36_KN.replace("==", "!="),
        "cong1": C36_KN.replace("- lap", "- lap + 1"), "tru1": C36_KN.replace("- lap", "- lap - 1")}),
    ("c36.category  `not thieu`", B, C40, "bang(not thieu,", {
        "bo": "bang(True,", "dao": "bang(thieu,", "yeu": "bang(len(thieu) < len(set(LOAI) - set(tru)),"}),
    ("c36.ngoai_bmp  `any(ord(c) > 0xFFFF ...)`", B, C40, C36_BMP, {
        "bo": "bang(True,", "ge": C36_BMP.replace("> 0xFFFF", ">= 0xFFFF"), "dao": C36_BMP.replace("> 0xFFFF", "<= 0xFFFF"),
        "cong1": C36_BMP.replace("0xFFFF", "0x10000"), "tru1": C36_BMP.replace("0xFFFF", "0xFFFE"), "yeu": C36_BMP.replace("any(", "all(")}),
    ("c36.cong_thuc  `... - len(tru or ()) + 1`", B, C40, "(len(LOAI) - len(tru or ()) + 1)", {
        "cong1": "(len(LOAI) - len(tru or ()) + 2)", "tru1": "(len(LOAI) - len(tru or ()) + 0)"}),
    ("c37.tong  `len(vu_tru) == 158`", B, C39, C37, {
        "bo": C37.replace("len(vu_tru) == 158 and ", ""), "ge": C37.replace("len(vu_tru) == 158", "len(vu_tru) >= 158"),
        "le": C37.replace("len(vu_tru) == 158", "len(vu_tru) <= 158"), "ne": C37.replace("len(vu_tru) == 158", "len(vu_tru) != 158"),
        "cong1": C37.replace("len(vu_tru) == 158", "len(vu_tru) == 159"), "tru1": C37.replace("len(vu_tru) == 158", "len(vu_tru) == 157"),
        "or": C37.replace("len(vu_tru) == 158 and", "len(vu_tru) == 158 or")}),
    ("c37.khac_nhau  `len(set(vu_tru)) == 158`", B, C39, C37, {
        "bo": C37.replace("len(set(vu_tru)) == 158 and ", ""), "ge": C37.replace("len(set(vu_tru)) == 158", "len(set(vu_tru)) >= 158"),
        "le": C37.replace("len(set(vu_tru)) == 158", "len(set(vu_tru)) <= 158"), "ne": C37.replace("len(set(vu_tru)) == 158", "len(set(vu_tru)) != 158"),
        "cong1": C37.replace("len(set(vu_tru)) == 158", "len(set(vu_tru)) == 159"), "tru1": C37.replace("len(set(vu_tru)) == 158", "len(set(vu_tru)) == 157"),
        "or": C37.replace("== 158 and not lech", "== 158 or not lech")}),
    ("c37.category  `not lech`", B, C39, C37, {"bo": C37.replace(" and not lech", ""), "dao": C37.replace("and not lech", "and lech")}),
    ("c37.lech  `bmp.count(loai) != (loai != \"Cs\")`", B, C39, C37_LECH, {
        "ne": C37_LECH.replace("bmp.count(loai) !=", "bmp.count(loai) =="), "gt": C37_LECH.replace("bmp.count(loai) !=", "bmp.count(loai) >"),
        "lt": C37_LECH.replace("bmp.count(loai) !=", "bmp.count(loai) <"), "dao": C37_LECH.replace('(loai != "Cs")', '(loai == "Cs")'),
        "bo": "lech = []"}),
    ("c37.bien_bmp  `ord(c) <= 0xFFFF`", B, C39, C37_BMP, {
        "cong1": C37_BMP.replace("0xFFFF", "0x10000"), "tru1": C37_BMP.replace("0xFFFF", "0xFFFE"), "dao": C37_BMP.replace("<= 0xFFFF", "> 0xFFFF"),
        "bo": C37_BMP.replace(" if ord(c) <= 0xFFFF", "")}),
    ("c37.phan_bo_sinh  `vu_tru[128:]`", B, C39, "ngoai = vu_tru[128:]", {"cong1": "ngoai = vu_tru[129:]", "tru1": "ngoai = vu_tru[127:]"}),
    ("c37.so_o  `len(o) == 648`", B, C39, C37_O, {
        "bo": "bang(True,", "ge": C37_O.replace("==", ">="), "le": C37_O.replace("==", "<="), "ne": C37_O.replace("==", "!="),
        "cong1": C37_O.replace("648", "649"), "tru1": C37_O.replace("648", "647")}),
    ("nap_sua.neo  `nguon.count(cu) == 1`", B, C39, "bang(nguon.count(cu) == 1,", {
        "bo": "bang(True,", "ge": "bang(nguon.count(cu) >= 1,", "le": "bang(nguon.count(cu) <= 1,", "ne": "bang(nguon.count(cu) != 1,",
        "cong1": "bang(nguon.count(cu) == 2,", "tru1": "bang(nguon.count(cu) == 0,"}),
    ("a135.so_phan_tu  `len(ra) == so`", A, A136, A_SO, {
        "bo": '("so_phan_tu", True)', "ge": A_SO.replace("==", ">="), "le": A_SO.replace("==", "<="), "ne": A_SO.replace("==", "!="),
        "cong1": A_SO.replace("== so", "== so + 1"), "tru1": A_SO.replace("== so", "== so - 1")}),
    ("a135.category_vang  `sorted(...) == sorted(vang)`", A, A136, A_VANG, {
        "bo": '("category_vang", True)', "ge": A_VANG.replace("==", ">="), "le": A_VANG.replace("==", "<="), "ne": A_VANG.replace("==", "!="),
        "yeu": '("category_vang", set(vang) <= set(LOAI_UNICODE) - set(bmp))'}),
    ("a135.lap_category  `len(bmp) == len(set(bmp))`", A, A136, A_LAP, {
        "bo": '("lap_category", True)', "ge": A_LAP.replace("==", ">="), "le": A_LAP.replace("==", "<="), "ne": A_LAP.replace("==", "!=")}),
    ("a135.thuoc_cam  `not any(c in cam ...)`", A, A136, A_CAM, {
        "bo": '("thuoc_cam", True)', "dao": A_CAM.replace("not any(", "any("), "yeu": A_CAM.replace("not any(", "not all(")}),
    ("a135.tu_0080  `all(ord(c) >= 0x80 ...)`", A, A136, A_80, {
        "bo": '("tu_0080", True)', "ge": A_80.replace(">= 0x80", "> 0x80"), "cong1": A_80.replace("0x80", "0x81"), "tru1": A_80.replace("0x80", "0x7F"),
        "yeu": A_80.replace("all(", "any("), "dao": A_80.replace(">= 0x80", "< 0x80")}),
    ("a135.cuoi.khong_rong  `bool(ra)`", A, A136, A_CUOI, {"bo": A_CUOI.replace("bool(ra) and ", ""), "dao": A_CUOI.replace("bool(ra)", "not ra"),
                                                           "or": A_CUOI.replace("bool(ra) and", "bool(ra) or")}),
    ("a135.cuoi.vi_tri  `ord(ra[-1]) > 0xFFFF`", A, A136, A_CUOI, {
        "bo": A_CUOI.replace("ord(ra[-1]) > 0xFFFF and ", ""), "ge": A_CUOI.replace("> 0xFFFF", ">= 0xFFFF"), "dao": A_CUOI.replace("> 0xFFFF", "<= 0xFFFF"),
        "cong1": A_CUOI.replace("0xFFFF", "0x10000"), "tru1": A_CUOI.replace("0xFFFF", "0xFFFE"), "or": A_CUOI.replace("> 0xFFFF and", "> 0xFFFF or")}),
    ("a135.cuoi.duy_nhat  `len(ra) - len(bmp) == 1`", A, A136, A_CUOI, {
        "bo": A_CUOI.replace(" and len(ra) - len(bmp) == 1", ""), "ge": A_CUOI.replace("== 1)", ">= 1)"), "le": A_CUOI.replace("== 1)", "<= 1)"),
        "ne": A_CUOI.replace("== 1)", "!= 1)"), "cong1": A_CUOI.replace("== 1)", "== 2)"), "tru1": A_CUOI.replace("== 1)", "== 0)")}),
    ("a135.bien_bmp  `ord(c) <= 0xFFFF`", A, A136, A_BMP, {
        "cong1": A_BMP.replace("0xFFFF", "0x10000"), "tru1": A_BMP.replace("0xFFFF", "0xFFFE"), "dao": A_BMP.replace("<= 0xFFFF", "> 0xFFFF"),
        "bo": A_BMP.replace(" if ord(c) <= 0xFFFF", "")}),
    ("a135.gom  `if not dat` / `bang(not lech`", A, A136, "len(ra) - len(bmp) == 1)) if not dat]", {"dao": "len(ra) - len(bmp) == 1)) if dat]", "bo": "len(ra) - len(bmp) == 1)) if False]"}),
]

TD = {   # lập luận TƯƠNG ĐƯƠNG, kiểm được bằng đọc: (id rút gọn, toán tử) -> lý do
    ("c37.tong", "le"): "len(set(x)) <= len(x) với mọi x. Vế kế bên đòi len(set(vu_tru)) == 158 nên len(vu_tru) >= 158; cộng `<= 158` ⇒ == 158. Cùng tập chấp nhận với bản gốc.",
    ("c37.khac_nhau", "ge"): "len(set(x)) <= len(x). Vế kế bên đòi len(vu_tru) == 158 nên len(set(vu_tru)) <= 158; cộng `>= 158` ⇒ == 158. Cùng tập chấp nhận với bản gốc.",
    ("a135.lap_category", "le"): "len(bmp) >= len(set(bmp)) luôn đúng, nên `len(bmp) <= len(set(bmp))` ⇔ `==`.",
    ("a135.cuoi.duy_nhat", "le"): "vế trước đòi ord(ra[-1]) > 0xFFFF, tức phần tử cuối KHÔNG thuộc bmp, nên len(ra) - len(bmp) >= 1; cộng `<= 1` ⇒ == 1.",
    ("c36.khac_nhau", "le"): None,
}
TD = {k: v for k, v in TD.items() if v}
KAD = {   # vì sao một toán tử không áp cho một nhóm mệnh đề
    "ge/le/ne": "chỉ áp cho mệnh đề có phép so == / != / > / >=; mệnh đề dạng `not X`, `any(...)`, `all(...)` thì dùng dao / yeu",
    "gt/lt": "chỉ áp cho phép so != (đổi thành một chiều)",
    "dao": "chỉ áp cho mệnh đề có `not` hoặc có phép so đảo được mà chưa nằm trong ge/le/ne",
    "cong1/tru1": "chỉ áp cho mệnh đề có hằng số",
    "or": "chỉ áp cho mệnh đề là một vế của phép `and`; vế cuối của chuỗi `and` dùng chung ô `or` với vế đứng trước nó",
    "yeu": "chỉ áp cho lượng từ all/any và quan hệ chứa",
}


def chay(lenh, cwd):
    r = subprocess.run(lenh, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout.strip()


def mot(worker, tep, truoc, neo, moi):
    p = worker / tep
    goc = p.read_text(encoding="utf-8")
    if goc.count(neo) != 1:
        return {"hang": "HONG", "ca": "", "rc": None, "dong": f"neo xuat hien {goc.count(neo)} lan"}
    kq, hong = None, None
    try:
        p.write_text(goc.replace(neo, moi), encoding="utf-8", newline="")
        for ca in (truoc, *(c for c in CA_PC[tep] if c != truoc)):
            rc, ra = chay([sys.executable, "-B", tep, "--mot-ca", ca], worker)
            if rc == 3 and ra.startswith(f"DO:{ca}:"):
                kq = {"hang": "GIET", "ca": ca, "rc": 3, "dong": ra[:400]}
                break
            if rc != 0:
                hong = hong or {"hang": "HONG", "ca": ca, "rc": rc, "dong": ra[:400]}
    finally:
        p.write_text(goc, encoding="utf-8", newline="")
    return kq or hong or {"hang": "SONG", "ca": "", "rc": 0, "dong": ""}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--goc", required=True)
    ap.add_argument("--ra", required=True)
    ap.add_argument("--song-song", type=int, default=4)
    ap.add_argument("--loc", default="")
    x = ap.parse_args()
    goc, ra = Path(x.goc).resolve(), Path(x.ra).resolve()
    ra.mkdir(parents=True, exist_ok=True)
    head = chay(["git", "rev-parse", "HEAD"], goc)[1]
    if chay(["git", "status", "--porcelain"], goc)[1]:
        print("KHONG_DO_DUOC: <goc> ban", file=sys.stderr)
        return 2
    workers = []
    for i in range(x.song_song):
        w = ra / f"w{i}"
        if not w.exists():
            subprocess.run(["git", "clone", "-q", str(goc), str(w)], check=True)
        subprocess.run(["git", "-C", str(w), "checkout", "-q", "--force", head], check=True)
        subprocess.run(["git", "-C", str(w), "config", "core.abbrev", "7"], check=True)
        if chay(["git", "status", "--porcelain"], w)[1] or chay(["git", "rev-parse", "HEAD"], w)[1] != head:
            print(f"KHONG_DO_DUOC: worker {w} khong sach / lech HEAD", file=sys.stderr)
            return 2
        workers.append(w)
    nen = {ca: chay([sys.executable, "-B", tep, "--mot-ca", ca], workers[0]) for tep in (B, A) for ca in CA_PC[tep]}
    nen_xanh = all(v == (0, "") for v in nen.values())
    viec = [(mid, tep, truoc, neo, op, moi) for mid, tep, truoc, neo, ops in M for op, moi in ops.items() if x.loc in mid]
    assert all(op in OPS for *_, op, _ in viec) and all(neo != moi for *_, neo, _, moi in viec)

    def lam(i_v):
        i, (mid, tep, truoc, neo, op, moi) = i_v
        return dict(mot(workers[i % len(workers)], tep, truoc, neo, moi), id=mid, op=op, tep=tep, cu=neo, moi=moi)
    # mỗi worker một luồng riêng: chia việc theo chỉ số để không hai đột biến nào cùng ghi một bản sao
    kq = [None] * len(viec)
    def luong(k):
        for i in range(k, len(viec), len(workers)):
            kq[i] = lam((i, viec[i]))
    with cf.ThreadPoolExecutor(len(workers)) as ex:
        list(ex.map(luong, range(len(workers))))
    sach = all(not chay(["git", "status", "--porcelain"], w)[1] for w in workers)
    for k in kq:
        td = TD.get((k["id"].split()[0], k["op"]))
        k["tuong_duong"] = td
        k["ket_luan"] = ("TUONG_DUONG" if td else "SONG") if k["hang"] == "SONG" else ("GIET (khai tuong duong)" if td and k["hang"] == "GIET" else k["hang"])
    dem = {h: sum(k["ket_luan"].startswith(h) for k in kq) for h in ("GIET", "TUONG_DUONG", "SONG", "HONG")}
    (ra / "bang.json").write_text(json.dumps({"head": head, "nen": {c: list(v) for c, v in nen.items()}, "dem": dem, "o": kq}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ids = list(dict.fromkeys(k["id"] for k in kq))
    o = {(k["id"], k["op"]): k for k in kq}
    ten_ngan = {C38: "c38", C39: "c39", C40: "c40", A136: "a136"}
    md = [f"# Bảng mệnh đề × toán tử — HEAD `{head}`", "",
          f"Baseline (bản nguyên vẹn, 4 ca phản chứng): {'XANH' if nen_xanh else 'KHÔNG XANH ' + json.dumps(nen, ensure_ascii=False)}. "
          f"Tổng {len(kq)} đột biến: GIET {dem['GIET']} · TUONG_DUONG {dem['TUONG_DUONG']} · SONG {dem['SONG']} · HONG {dem['HONG']}. Bản sao sạch sau khi đo: {sach}.", "",
          "Ô: ca phản chứng giết (rc 3, `DO:<ca>:`) · `TĐ` = tương đương có lập luận · `SỐNG` · `HỎNG` · `—` = không áp dụng (lý do cuối tệp).", "",
          "| Mệnh đề | " + " | ".join(OPS) + " |", "|---|" + "---|" * len(OPS)]
    for mid in ids:
        md.append(f"| {mid.replace('|', chr(92) + '|')} | " + " | ".join(
            "—" if (mid, op) not in o else {"GIET": ten_ngan.get(o[mid, op]["ca"], "?"), "TUONG_DUONG": "TĐ", "SONG": "**SỐNG**", "HONG": "**HỎNG**"}[o[mid, op]["ket_luan"].split()[0]]
            + (" (khai TĐ)" if o[mid, op]["ket_luan"].endswith("duong)") else "") for op in OPS) + " |")
    md += ["", "## Từng đột biến", "", "| Mệnh đề | Toán tử | Kết luận | Ca giết | rc | Văn bản thay | Dòng quan sát được |", "|---|---|---|---|---|---|---|"]
    for k in kq:
        md.append(f"| {k['id'].split()[0]} | {k['op']} | {k['ket_luan']} | {ten_ngan.get(k['ca'], k['ca'])} | {k['rc']} | `{k['moi'][:150]}` | `{k['dong'][:300]}` |")
    md += ["", "## Lập luận tương đương", ""] + [f"- **{a} / {b}**: {v}" for (a, b), v in TD.items()]
    md += ["", "## Không áp dụng", ""] + [f"- **{a}**: {v}" for a, v in KAD.items()]
    (ra / "bang.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    xau = [k for k in kq if k["ket_luan"] in ("SONG", "HONG")]
    for k in xau:
        print(f"{k['ket_luan']} | {k['id']} | {k['op']} | {k['ca']} rc={k['rc']} | {k['dong'][:300]}")
    print(f"BANG TOAN TU: {len(kq)} dot bien · GIET {dem['GIET']} · TUONG_DUONG {dem['TUONG_DUONG']} · SONG {dem['SONG']} · HONG {dem['HONG']} · baseline {'XANH' if nen_xanh else 'DO'} · ban sao sach {sach}")
    return 0 if nen_xanh and sach and not xau else 1


if __name__ == "__main__":
    raise SystemExit(main())
