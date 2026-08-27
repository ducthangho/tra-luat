#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phản chứng CHẠY ĐƯỢC cho cổng `duyet-khac-danh-tinh` — packet #348.

HAI TẦNG, vì cổng này có hai mặt hỏng khác hẳn nhau:

 (A) VỊ TỪ — `phan_quyet()` là hàm THUẦN nhận dữ liệu làm đối số, nên đo được bằng ca
     BIẾT TRƯỚC ĐÁP ÁN. Đây là bài học `MOC_MO_HO_CO_SAN` của PR #343: một vị từ chỉ chạy
     trên dữ liệu THẬT thì nhánh "báo xấu" chưa từng chạy, và đột biến làm nó luôn-tha sẽ
     không giết được ca nào.

 (B) HÌNH DẠNG WORKFLOW — hai bẫy tự-vô-hiệu (B1 PR sửa được cổng của nó · B2
     `pull_request_target` chạy mã PR với token) KHÔNG kiểm được bằng cách chạy, vì chúng là
     ngữ nghĩa TRIGGER của GitHub. Kiểm được bằng cách đọc CHÍNH TỆP YAML và đòi nó mang
     những tính chất làm hai bẫy ấy bất khả.

     NÓI RÕ GIỚI HẠN, đừng để ai đọc mạnh hơn: tầng (B) đo HÌNH DẠNG TỆP, KHÔNG đo hành vi
     của GitHub. Nó không chứng minh `pull_request_target` thật sự lấy workflow từ nhánh cơ
     sở — nó chứng minh cổng đã được viết theo cách chỉ đúng NẾU điều đó đúng. Muốn đo hành
     vi thật thì phải mở một PR đối kháng, và đó là việc của lượt cross-review chứ không
     phải của bộ này. Nợ có tên: `ngu-nghia-trigger-chua-do-bang-PR-doi-khang`.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MA = HERE / "duyet_danh_tinh.py"
YML = ROOT / ".github" / "workflows" / "duyet-khac-danh-tinh.yml"

# DỰNG SAU KHI PHÂN TÍCH CÚ PHÁP, không cho chuỗi này đi nguyên văn trên đường truyền.
# Cùng lý do với mẹo `chr(92)` trong `CLAUDE.md`: nội dung NÓI VỀ một cú pháp thì phải
# tránh để chính cú pháp ấy bị một tầng nào đó diễn giải.
_MO_BIEU_THUC = "$" + "{" + "{"


def _nap():
    sp = importlib.util.spec_from_file_location("tl_duyet", str(MA))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _yaml():
    import yaml
    return yaml.safe_load(YML.read_text(encoding="utf-8"))


def _rv(ai, tt="APPROVED", luc="2026-01-01T00:00:00Z", commit="HEAD1"):
    return {"user": {"login": ai}, "state": tt, "submitted_at": luc, "commit_id": commit}


# ── TẦNG A — vị từ ─────────────────────────────────────────────────────────────────────
def ca_tu_duyet_bi_chan(m):
    dat, ly = m.phan_quyet("ducthangho", [_rv("ducthangho")])
    if dat:
        raise AssertionError("TỰ DUYỆT được cho qua: " + ly)


def ca_duyet_boi_danh_tinh_khac_thi_qua(m):
    dat, ly = m.phan_quyet("ducthangho", [_rv("code2nguyen")])
    if not dat:
        raise AssertionError("duyệt bởi danh tính khác bị chặn oan: " + ly)


def ca_nguoi_ngoai_danh_sach_khong_tinh(m):
    dat, _ = m.phan_quyet("ducthangho", [_rv("nguoi-la-hoan-toan")])
    if dat:
        raise AssertionError("login NGOÀI danh sách cho phép vẫn được tính là duyệt")


def ca_HOA_THUONG_khong_lam_lot_tu_duyet(m):
    """Login GitHub KHÔNG phân biệt hoa thường, nên so thô `!=` để lọt TỰ DUYỆT.

    HƯỚNG CỦA CA NÀY ĐÃ PHẢI ĐẢO, và lý do đáng ghi: bản đầu đặt tác giả `ducthangho` và
    người duyệt `DucThangHo`. Ca ấy XANH — nhưng xanh vì DANH SÁCH CHO PHÉP chặn
    (`DucThangHo` không có trong đó), KHÔNG phải vì luật "khác tác giả". Đột biến bỏ
    `casefold` không giết nổi nó, và chính điều đó phơi ra rằng ca đang đo nhầm thứ.
    Đảo lại: tác giả viết hoa-thường, người duyệt viết thường và NẰM TRONG danh sách — nay
    chỉ `casefold` mới cứu được."""
    dat, _ = m.phan_quyet("DucThangHo", [_rv("ducthangho")])
    if dat:
        raise AssertionError("`ducthangho` duyệt cho `DucThangHo` mà vẫn qua — tự duyệt lọt")


def ca_KHONG_DOC_DUOC_review_la_DO(m):
    dat, ly = m.phan_quyet("ducthangho", None)
    if dat or "KHÔNG ĐO ĐƯỢC" not in ly:
        raise AssertionError("reviews=None phải là KHÔNG ĐO ĐƯỢC và ĐỎ: " + ly)


def ca_khong_co_review_nao_la_DO(m):
    dat, _ = m.phan_quyet("ducthangho", [])
    if dat:
        raise AssertionError("danh sách review RỖNG mà vẫn qua")


def ca_tac_gia_rong_la_DO(m):
    dat, ly = m.phan_quyet("", [_rv("code2nguyen")])
    if dat or "KHÔNG ĐO ĐƯỢC" not in ly:
        raise AssertionError("tác giả rỗng phải là KHÔNG ĐO ĐƯỢC và ĐỎ: " + ly)


def ca_danh_sach_cho_phep_RONG_la_DO(m):
    dat, ly = m.phan_quyet("ducthangho", [_rv("code2nguyen")], cho_phep=())
    if dat or "RỖNG" not in ly:
        raise AssertionError("danh sách cho phép RỖNG mà cổng vẫn xanh: " + ly)


def ca_yeu_cau_SUA_chua_go_thi_chan(m):
    dat, _ = m.phan_quyet("ducthangho",
                          [_rv("code2nguyen", "APPROVED", "2026-01-01T00:00:00Z"),
                           _rv("ducthangho", "CHANGES_REQUESTED", "2026-01-02T00:00:00Z")])
    if dat:
        raise AssertionError("có CHANGES_REQUESTED chưa gỡ mà vẫn qua")


def ca_CHI_tinh_review_MOI_NHAT(m):
    """Một người duyệt rồi đổi ý. Cộng dồn mọi bản ghi thì `APPROVED` đã bị thay vẫn tính."""
    doi_y = [_rv("code2nguyen", "APPROVED", "2026-01-01T00:00:00Z"),
             _rv("code2nguyen", "CHANGES_REQUESTED", "2026-01-02T00:00:00Z")]
    if m.phan_quyet("ducthangho", doi_y)[0]:
        raise AssertionError("APPROVED cũ đã bị thay bằng CHANGES_REQUESTED mà vẫn qua")
    # Chiều ngược: đổi ý theo hướng TỐT thì phải qua, kẻo bản vá thành chặn oan.
    doi_lai = [_rv("code2nguyen", "CHANGES_REQUESTED", "2026-01-01T00:00:00Z"),
               _rv("code2nguyen", "APPROVED", "2026-01-02T00:00:00Z")]
    if not m.phan_quyet("ducthangho", doi_lai)[0]:
        raise AssertionError("CHANGES_REQUESTED cũ đã được thay bằng APPROVED mà vẫn chặn")


def ca_ban_duyet_CU_khong_tinh(m):
    """Duyệt xong rồi ĐẨY THÊM COMMIT thì bản duyệt cũ thuộc về MÃ KHÁC.

    Không neo vào head thì cổng đo một thứ đã hết hạn: xin duyệt lúc diff vô hại, rồi đẩy
    tiếp. GitHub có ô "dismiss stale approvals", nhưng đó là CÀI ĐẶT KHO chứ không phải
    thuộc tính của cổng — dựa vào nó là dựa vào thứ nằm ngoài tầm cổng, đúng lối dựa mà
    packet này sinh ra để bỏ."""
    duyet = [_rv("code2nguyen", commit="HEAD1")]
    if not m.phan_quyet("ducthangho", duyet, head_sha="HEAD1")[0]:
        raise AssertionError("bản duyệt ĐÚNG head bị chặn oan")
    dat, ly = m.phan_quyet("ducthangho", duyet, head_sha="HEAD2")
    if dat:
        raise AssertionError("bản duyệt của commit CŨ vẫn được tính: " + ly)


def ca_thieu_commit_id_khong_duoc_doc_thanh_DAT(m):
    """Neo thì phải neo CHẶT: thiếu `commit_id` mà đang có head để so là KHÔNG ĐO ĐƯỢC."""
    thieu = [{"user": {"login": "code2nguyen"}, "state": "APPROVED",
              "submitted_at": "2026-01-01T00:00:00Z"}]
    if m.phan_quyet("ducthangho", thieu, head_sha="HEAD1")[0]:
        raise AssertionError("bản ghi THIẾU `commit_id` vẫn được tính là duyệt đúng head")


# ── TẦNG B — hình dạng workflow ────────────────────────────────────────────────────────
def ca_cong_KHONG_chay_tren_pull_request(m):
    """B1. `pull_request` lấy workflow TỪ NHÁNH PR ⇒ PR tự nới cổng cho mình."""
    d = _yaml()
    dk = str(d["jobs"]["cong"].get("if") or "")
    if "pull_request'" not in dk or "!=" not in dk:
        raise AssertionError("job `cong` không loại trừ `pull_request`: if=%r" % dk)


def ca_cong_KHONG_checkout_head_PR(m):
    """B2. `pull_request_target` cầm token của kho; checkout head PR là mở cửa chạy mã lạ."""
    xau = []
    for b in _yaml()["jobs"]["cong"]["steps"]:
        ref = str((b.get("with") or {}).get("ref") or "")
        if "head" in ref.lower():
            xau.append("bước %r neo vào HEAD: %s" % (b.get("name") or b.get("uses"), ref))
        if str(b.get("uses") or "").startswith("actions/checkout") and "base" not in ref:
            xau.append("checkout KHÔNG neo vào nhánh cơ sở: ref=%r" % ref)
    if xau:
        raise AssertionError("; ".join(xau))


def ca_khong_co_cu_phap_bieu_thuc_trong_run(m):
    """Đã trả giá 16-08-2026: một cặp ngoặc biểu thức RỖNG trong CHÚ THÍCH của `run` làm cả
    tệp bị GitHub TỪ CHỐI (run mang tên đường dẫn tệp, 0 job)."""
    xau = [b.get("name") or b.get("uses")
           for j in _yaml()["jobs"].values() for b in j["steps"]
           if _MO_BIEU_THUC in str(b.get("run") or "")]
    if xau:
        raise AssertionError("có cú pháp biểu thức trong thân `run`: %s" % xau)


def ca_workflow_TRUYEN_head_sha(m):
    """Vị từ neo được vào head KHÔNG có nghĩa gì nếu workflow quên truyền head vào.
    Ca `ban_duyet_CU_khong_tinh` gọi vị từ TRỰC TIẾP, nên nó vẫn xanh trong khi cổng thật
    mù — đúng khoảng cách giữa "hàm đúng" và "cổng đúng"."""
    r = "".join(str(b.get("run") or "") for b in _yaml()["jobs"]["cong"]["steps"])
    if "--head-sha" not in r:
        raise AssertionError("job `cong` KHÔNG truyền `--head-sha` — vị từ neo mà cổng không neo")


def ca_quyen_CHI_DOC(m):
    q = _yaml().get("permissions") or {}
    xau = [f"{k}={v}" for k, v in q.items() if str(v) != "read"]
    if not q:
        raise AssertionError("workflow KHÔNG khai `permissions` — nhận mặc định của kho")
    if xau:
        raise AssertionError("quyền KHÔNG chỉ-đọc: %s" % ", ".join(xau))


def ca_cong_KHONG_chay_ma_den_tu_PR(m):
    """Job `cong` chỉ được chạy đúng script của kho, lấy từ nhánh cơ sở."""
    for b in _yaml()["jobs"]["cong"]["steps"]:
        r = str(b.get("run") or "")
        if not r:
            continue
        if "pip install" in r or "npm " in r:
            raise AssertionError("job `cong` cài phụ thuộc — bề mặt chạy mã lạ: %r" % r[:60])


CA = [
    ("tu_duyet_bi_chan", ca_tu_duyet_bi_chan),
    ("duyet_boi_danh_tinh_khac_thi_qua", ca_duyet_boi_danh_tinh_khac_thi_qua),
    ("nguoi_ngoai_danh_sach_khong_tinh", ca_nguoi_ngoai_danh_sach_khong_tinh),
    ("HOA_THUONG_khong_lam_lot_tu_duyet", ca_HOA_THUONG_khong_lam_lot_tu_duyet),
    ("KHONG_DOC_DUOC_review_la_DO", ca_KHONG_DOC_DUOC_review_la_DO),
    ("khong_co_review_nao_la_DO", ca_khong_co_review_nao_la_DO),
    ("tac_gia_rong_la_DO", ca_tac_gia_rong_la_DO),
    ("danh_sach_cho_phep_RONG_la_DO", ca_danh_sach_cho_phep_RONG_la_DO),
    ("yeu_cau_SUA_chua_go_thi_chan", ca_yeu_cau_SUA_chua_go_thi_chan),
    ("CHI_tinh_review_MOI_NHAT", ca_CHI_tinh_review_MOI_NHAT),
    ("ban_duyet_CU_khong_tinh", ca_ban_duyet_CU_khong_tinh),
    ("thieu_commit_id_khong_duoc_doc_thanh_DAT", ca_thieu_commit_id_khong_duoc_doc_thanh_DAT),
    ("cong_KHONG_chay_tren_pull_request", ca_cong_KHONG_chay_tren_pull_request),
    ("cong_KHONG_checkout_head_PR", ca_cong_KHONG_checkout_head_PR),
    ("khong_co_cu_phap_bieu_thuc_trong_run", ca_khong_co_cu_phap_bieu_thuc_trong_run),
    ("workflow_TRUYEN_head_sha", ca_workflow_TRUYEN_head_sha),
    ("quyen_CHI_DOC", ca_quyen_CHI_DOC),
    ("cong_KHONG_chay_ma_den_tu_PR", ca_cong_KHONG_chay_ma_den_tu_PR),
]

DOT_BIEN_MA = {
    "bo_kiem_KHAC_tac_gia": (
        "                 if st in _TAN and a in cho and a != ta and _dung_commit(c))",
        "                 if st in _TAN and a in cho and _dung_commit(c))",
        ["tu_duyet_bi_chan", "HOA_THUONG_khong_lam_lot_tu_duyet"]),
    "so_tho_khong_casefold": (
        '    return str(x or "").strip().casefold()',
        '    return str(x or "").strip()',
        ["HOA_THUONG_khong_lam_lot_tu_duyet"]),
    "reviews_None_doc_thanh_rong": (
        "    if reviews is None:\n",
        "    if False:\n",
        ["KHONG_DOC_DUOC_review_la_DO"]),
    # `if True:` KHONG dung duoc lam dot bien o day: no cho ban ghi CUOI thang, ma voi
    # fixture `doi_y` ban cuoi dung la CHANGES_REQUESTED — tinh co ra CUNG ket qua. Mot dot
    # bien khong-tac-dung trong y het mot ca yeu. Giu ban DAU moi lat duoc phan quyet.
    "cong_don_moi_review": (
        "        if ai not in moi_nhat or khoa > moi_nhat[ai][0]:",
        "        if ai not in moi_nhat:",
        ["CHI_tinh_review_MOI_NHAT"]),
    "bo_kiem_YEU_CAU_SUA": (
        "    if chan:\n",
        "    if False:\n",
        ["yeu_cau_SUA_chua_go_thi_chan"]),
    "cho_phep_RONG_van_tha": (
        "    if not cho:\n",
        "    if False:\n",
        ["danh_sach_cho_phep_RONG_la_DO"]),
    "bo_neo_vao_HEAD": (
        "        return True if not head_sha else (c == str(head_sha))",
        "        return True",
        ["ban_duyet_CU_khong_tinh", "thieu_commit_id_khong_duoc_doc_thanh_DAT"]),
    "tac_gia_rong_van_tha": (
        "    if not ta:\n",
        "    if False:\n",
        ["tac_gia_rong_la_DO"]),
}

DOT_BIEN_YML = {
    # B1: nới `if` để cổng chạy ở `pull_request` — tức lấy workflow TỪ NHÁNH PR.
    "dung_pull_request_thay_vi_target": (
        "    if: github.event_name != 'pull_request'\n",
        "    if: always()\n",
        ["cong_KHONG_chay_tren_pull_request"]),
    # B2: checkout head PR trong job cầm token.
    "checkout_head_PR": (
        "          ref: ${{ github.event.pull_request.base.ref }}\n",
        "          ref: ${{ github.event.pull_request.head.sha }}\n",
        ["cong_KHONG_checkout_head_PR"]),
    "workflow_quen_truyen_head_sha": (
        ' \\\n                 --tac-gia "$TL_TAC_GIA" --head-sha "$TL_HEAD"\n',
        ' --tac-gia "$TL_TAC_GIA"\n',
        ["workflow_TRUYEN_head_sha"]),
    "quyen_ghi": (
        "permissions:\n  contents: read\n  pull-requests: read\n",
        "permissions:\n  contents: write\n  pull-requests: read\n",
        ["quyen_CHI_DOC"]),
    "bo_khai_quyen": (
        "permissions:\n  contents: read\n  pull-requests: read\n",
        "",
        ["quyen_CHI_DOC"]),
}


def _chay(chi=None, m=None, doi_yml=None):
    """Trả (đạt, lý do đỏ). `doi_yml` = (tìm, thay) áp lên bản sao YAML trong bộ nhớ."""
    global YML
    cu_yml = YML
    tam = None
    try:
        if doi_yml:
            goc = cu_yml.read_text(encoding="utf-8")
            tim, thay = doi_yml
            if goc.count(tim) != 1:
                raise AssertionError("MỐC YAML khớp %d chỗ" % goc.count(tim))
            tam = Path(tempfile.mkdtemp(prefix="tl348-")) / "w.yml"
            tam.write_text(goc.replace(tim, thay, 1), encoding="utf-8")
            YML = tam
        mod = m or _nap()
        dat, ly = {}, {}
        for ten, f in CA:
            if chi and ten not in chi:
                continue
            try:
                f(mod)
                dat[ten] = True
            except Exception as e:                       # noqa: BLE001 — ca đỏ là DỮ LIỆU
                dat[ten] = False
                ly[ten] = f"{type(e).__name__}: {e}"
        return dat, ly
    finally:
        YML = cu_yml


def _ap(van, tim, thay):
    if van.count(tim) != 1:
        raise AssertionError("MỐC khớp %d chỗ: %r" % (van.count(tim), tim[:56]))
    return van.replace(tim, thay, 1)


def main() -> int:
    dat, ly = _chay()
    do_san = sorted(k for k, v in dat.items() if v is False)
    print(f"nền: {sum(1 for v in dat.values() if v)}/{len(dat)} đạt")
    for k in do_san:
        print(f"  ĐỎ    {k}: {ly[k]}")
    if do_san:
        # Nền đỏ thì mọi đột biến "giết" tầm thường bằng chính ca đỏ sẵn — tỷ lệ ấy KHÔNG
        # CÓ NGHĨA. Bài học P1 của PR #342, và nay là nếp chung của kho.
        print(f"\nTỪ CHỐI công bố điểm đột biến: nền có {len(do_san)} ca ĐỎ")
        return 1

    print("\ntự chứng minh KHÔNG RỖNG (ca đích phải ĐỎ):")
    hong = []
    goc_ma = MA.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="tl348-mut-") as d:
        for ten, (tim, thay, dich) in sorted(DOT_BIEN_MA.items()):
            f = Path(d) / f"{ten}.py"
            f.write_text(_ap(goc_ma, tim, thay), encoding="utf-8")
            sp = importlib.util.spec_from_file_location("mut_" + ten, str(f))
            mo = importlib.util.module_from_spec(sp)
            sp.loader.exec_module(mo)
            d2, _ = _chay(chi=set(dich), m=mo)
            chet = sorted(k for k, v in d2.items() if v is False)
            thieu = [x for x in dich if x not in chet]
            print(f"  {'ok ' if not thieu else 'LỖI'} {ten} → giết {chet or 'KHÔNG CA NÀO'}")
            if thieu:
                hong.append(f"{ten}: ca đích còn sống: {thieu}")

    for ten, (tim, thay, dich) in sorted(DOT_BIEN_YML.items()):
        d2, _ = _chay(chi=set(dich), doi_yml=(tim, thay))
        chet = sorted(k for k, v in d2.items() if v is False)
        thieu = [x for x in dich if x not in chet]
        print(f"  {'ok ' if not thieu else 'LỖI'} {ten} → giết {chet or 'KHÔNG CA NÀO'}")
        if thieu:
            hong.append(f"{ten}: ca đích còn sống: {thieu}")

    print(f"\nSỐ LIỆU (đếm bằng máy):\n  ca        : {len(dat)}\n"
          f"  đột biến  : {len(DOT_BIEN_MA) + len(DOT_BIEN_YML)}")
    print("NỢ  : `ngu-nghia-trigger-chua-do-bang-PR-doi-khang` — tầng (B) đo HÌNH DẠNG tệp,")
    print("      KHÔNG đo hành vi trigger của GitHub. Muốn đo thật phải mở PR đối kháng.")
    if hong:
        print("TỔNG: %d lỗi" % len(hong))
        for x in hong:
            print("   " + x)
        return 1
    print("TỔNG: ĐẠT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
