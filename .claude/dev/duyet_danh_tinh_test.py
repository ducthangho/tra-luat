#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phản chứng CHẠY ĐƯỢC cho cổng `duyet-khac-danh-tinh` — packet #348.

BA TẦNG, vì cổng này có ba mặt hỏng khác hẳn nhau:

 (A) VỊ TỪ — `phan_quyet()` và `doc_het_review()` nhận dữ liệu/nguồn đọc làm ĐỐI SỐ, nên đo
     được bằng ca BIẾT TRƯỚC ĐÁP ÁN. Đây là bài học `MOC_MO_HO_CO_SAN` của PR #343: một vị
     từ chỉ chạy trên dữ liệu THẬT thì nhánh "báo xấu" chưa từng chạy, và đột biến làm nó
     luôn-tha sẽ không giết được ca nào.

 (B) HÌNH DẠNG WORKFLOW — hai bẫy tự-vô-hiệu (B1 PR sửa được cổng của nó · B2
     `pull_request_target` chạy mã PR với token) KHÔNG kiểm được bằng cách chạy, vì chúng là
     ngữ nghĩa TRIGGER của GitHub. Kiểm được bằng cách đọc CHÍNH TỆP YAML và đòi nó mang
     những tính chất làm hai bẫy ấy bất khả.

     TẦNG (B) ĐÃ PHẢI VIẾT LẠI SAU CROSS-REVIEW LƯỢT 1, và lý do là bài học chung của kho:
     bản đầu kiểm bằng DANH SÁCH CẤM (`if` phải chứa chuỗi `pull_request'` · `run` không
     được chứa `pip install`/`npm `) và reviewer đo được ba đường lách vẫn cho `18/18,
     dead=NONE`: một vế `|| always()` nối thêm · `permissions: write` ghi đè ở MỨC JOB ·
     một bước kéo head PR chèn vào giữa. "Danh sách cấm không bao giờ đủ — phải đảo thành
     danh sách CHO PHÉP" (`lease-authority-spoof`, v1.36.68). Cross-review lượt 2 tiếp tục
     tìm được mức WORKFLOW còn hở (`env`, `defaults.run.shell`, giá trị `runs-on`). Vì vậy
     tầng (B) nay chỉ có MỘT allow-list: so BẰNG NHAU SÂU toàn bộ cây `safe_load` với một
     golden dict canonical. Thêm hoặc đổi ở bất kỳ mức nào đều làm lệch cả cây.

     NÓI RÕ GIỚI HẠN, đừng để ai đọc mạnh hơn: tầng (B) đo HÌNH DẠNG TỆP, KHÔNG đo hành vi
     của GitHub. Nó không chứng minh `pull_request_target` thật sự lấy workflow từ nhánh cơ
     sở — nó chứng minh cổng đã được viết theo cách chỉ đúng NẾU điều đó đúng. Muốn đo hành
     vi thật thì phải mở một PR đối kháng, và đó là việc của bước nghiệm thu trong
     `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md`. Nợ có tên:
     `ngu-nghia-trigger-chua-do-bang-PR-doi-khang`.

 (C) DINH NGHIA GITHUB — PyYAML chi cho biet YAML co nap duoc, khong biet workflow co
     duoc GitHub chap nhan. `actionlint` phai chay tren CA HAI tep cua packet; thieu cong
     cu la KHONG DO DUOC va lam suite DO, khong duoc bo qua.

MỖI ĐỘT BIẾN PHẢI GIẾT ĐÚNG VÀ CHỈ ĐÚNG TẬP CA ĐÃ KHAI. Runner chạy từng đột biến trên TOÀN
BỘ ca chứ không chỉ tập đích, rồi đòi hai tập BẰNG NHAU. Lượt cross-review 1 phải dựng một
runner ngoài để đo tính chất ấy; đưa nó vào đây thì bộ tự đo được, và một đột biến giết
tràn (ví dụ làm YAML không phân tích được) lộ ra ngay thay vì đi qua như "đã giết ca đích".
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MA = HERE / "duyet_danh_tinh.py"
YML = ROOT / ".github" / "workflows" / "duyet-khac-danh-tinh.yml"    # lane TIN CẬY
YML2 = ROOT / ".github" / "workflows" / "duyet-phan-chung.yml"       # lane PHẢN CHỨNG
YML_GOC = YML
YML2_GOC = YML2

# DỰNG SAU KHI PHÂN TÍCH CÚ PHÁP, không cho chuỗi này đi nguyên văn trên đường truyền.
# Cùng lý do với mẹo `chr(92)` trong `CLAUDE.md`: nội dung NÓI VỀ một cú pháp thì phải
# tránh để chính cú pháp ấy bị một tầng nào đó diễn giải.
_MO_BIEU_THUC = "$" + "{" + "{"


# ── GOLDEN TOÀN CÂY CỦA LANE TIN CẬY ──────────────────────────────────────────────────
_SU_KIEN_PHAN_CHUNG = {"pull_request"}

# PyYAML dung YAML 1.1 nen `on:` thanh khoa bool `True`; `"on":` lai la chuoi. `_doc_yaml`
# chuan hoa DUNG hai cach viet ay ve `True`, sau khi da chan ca khoa trung nguyen van lan
# collision ngu nghia `on:` + `"on":`. Golden van CO Y CHAT hon ngu nghia GitHub o cac
# diem sau: thu tu list `types`, kieu scalar (`false` khac `'false'`), chuoi `run` sau khi
# YAML construct, va topology deu phai khop. No KHONG do thu tu khoa mapping hay khoang
# trang YAML ma loader da bo. Day la pham vi co chu dich, khong phai byte-golden cua tep.
_GOLDEN_WORKFLOW_TIN_CAY = {
    "name": "duyet khac danh tinh",
    True: {
        "pull_request_target": {
            "types": ["opened", "reopened", "synchronize", "ready_for_review"],
        },
        "pull_request_review": {"types": ["submitted", "dismissed"]},
    },
    "permissions": {"contents": "read", "pull-requests": "read"},
    "jobs": {
        "cong": {
            "if": "github.event_name != 'pull_request'",
            "runs-on": "ubuntu-latest",
            "permissions": {"contents": "read", "pull-requests": "read"},
            "steps": [
                {
                    "name": "lay ma tu NHANH CO SO (khong bao gio head PR)",
                    "uses": "actions/checkout@v4",
                    "with": {
                        "ref": "${{ github.event.pull_request.base.ref }}",
                        "persist-credentials": False,
                    },
                },
                {
                    "name": "do nguoi duyet khac nguoi tao PR",
                    "env": {
                        "GH_TOKEN": "${{ secrets.GITHUB_TOKEN }}",
                        "TL_KHO": "${{ github.repository }}",
                        "TL_PR": "${{ github.event.pull_request.number }}",
                        "TL_TAC_GIA": "${{ github.event.pull_request.user.login }}",
                        "TL_HEAD": "${{ github.event.pull_request.head.sha }}",
                    },
                    "run": (
                        "set -eu\n"
                        'PY="$(command -v python3 || command -v python || command -v py)"\n'
                        '"$PY"  .claude/dev/duyet_danh_tinh.py --kho "$TL_KHO" '
                        '--pr "$TL_PR" \\\n'
                        '       --tac-gia "$TL_TAC_GIA" --head-sha "$TL_HEAD"\n'
                    ),
                },
            ],
        },
    },
}


def _nap():
    sp = importlib.util.spec_from_file_location("tl_duyet", str(MA))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


class _SafeLoaderKhongKhoaTrung(yaml.SafeLoader):
    """SafeLoader nhung tu choi mapping co khoa lap lai thay vi lay ban ghi sau."""


def _lap_mapping_khong_trung(loader, node, deep=False):
    """Dung mapping mot lan; khoa lap lai la loi co ten, khong bi `dict` nuot."""
    loader.flatten_mapping(node)
    ket = {}
    for khoa_node, gia_tri_node in node.value:
        khoa = loader.construct_object(khoa_node, deep=deep)
        try:
            da_co = khoa in ket
        except TypeError:
            raise yaml.constructor.ConstructorError(
                "dang dung mapping", node.start_mark,
                "khoa khong hash duoc: %r" % (khoa,), khoa_node.start_mark) from None
        if da_co:
            raise yaml.constructor.ConstructorError(
                "dang dung mapping", node.start_mark,
                "khoa trung: %r" % (khoa,), khoa_node.start_mark)
        ket[khoa] = loader.construct_object(gia_tri_node, deep=deep)
    return ket


_SafeLoaderKhongKhoaTrung.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _lap_mapping_khong_trung)


def _chuan_khoa_on(d):
    """Chap nhan `on:` hoac `"on":`, nhung khong nuot khi ca hai cung co mat."""
    if not isinstance(d, dict) or "on" not in d:
        return d
    if True in d:
        raise ValueError("khoa trung ngu nghia: 'on' (dong thoi co on: va \"on\":)")
    return {True if k == "on" else k: v for k, v in d.items()}


def _doc_yaml(p):
    d = yaml.load(p.read_text(encoding="utf-8"), Loader=_SafeLoaderKhongKhoaTrung)
    return _chuan_khoa_on(d)


def _doc_yaml_safe_load_roi_chuan_on(p):
    """Dot bien: giu chuan hoa `on`, nhung mo lai loi safe_load nuot khoa trung."""
    return _chuan_khoa_on(yaml.safe_load(p.read_text(encoding="utf-8")))


def _doc_yaml_khong_chuan_on(p):
    """Dot bien: van chan khoa trung, nhung tu choi cach viet `"on":` hop le."""
    return yaml.load(p.read_text(encoding="utf-8"), Loader=_SafeLoaderKhongKhoaTrung)


def _doc_yaml_on_de_len(p):
    """Dot bien thu tam: gap ca hai cach viet thi de `"on"` len ban `on` con lai."""
    d = _doc_yaml_khong_chuan_on(p)
    if isinstance(d, dict) and "on" in d:
        d = dict(d)
        d[True] = d.pop("on")
    return d


def _yaml():
    return _doc_yaml(YML)


def _yaml2():
    return _doc_yaml(YML2)


def _su_kien(d):
    """Tập sự kiện của một workflow. `yaml.safe_load` biến khoá `on` thành `True` (YAML 1.1
    coi `on` là bool) — đọc nhầm chỗ này thì mọi kiểm tra sự kiện im lặng trở thành rỗng."""
    kh = d.get("on", d.get(True))
    if isinstance(kh, str):
        return {kh}
    return set(kh or ())


def _lech_sau(mong, thuc, duong="$"):
    """Định vị chỗ lệch đầu tiên để phép so toàn cây không trả thông báo mơ hồ."""
    if type(mong) is not type(thuc):
        return "%s: kiểu đòi %s, đang là %s" % (duong, type(mong).__name__, type(thuc).__name__)
    if isinstance(mong, dict):
        thieu = sorted(set(mong) - set(thuc), key=repr)
        thua = sorted(set(thuc) - set(mong), key=repr)
        if thieu or thua:
            return "%s: khoá thiếu=%r, thừa=%r" % (duong, thieu, thua)
        for k in mong:
            if mong[k] != thuc[k]:
                return _lech_sau(mong[k], thuc[k], "%s[%r]" % (duong, k))
    elif isinstance(mong, list):
        if len(mong) != len(thuc):
            return "%s: độ dài đòi %d, đang là %d" % (duong, len(mong), len(thuc))
        for i, (a, b) in enumerate(zip(mong, thuc)):
            if a != b:
                return _lech_sau(a, b, "%s[%d]" % (duong, i))
    elif mong != thuc:
        return "%s: đòi %r, đang là %r" % (duong, mong, thuc)
    return "%s: lệch nhưng không định vị được" % duong


def _rv(ai, tt="APPROVED", luc="2026-01-01T00:00:00Z", commit="HEAD1", ma=None, kieu="User"):
    r = {"user": {"login": ai, "type": kieu}, "state": tt, "submitted_at": luc,
         "commit_id": commit}
    if ma is not None:
        r["id"] = ma
    return r


def _nguon(trang_lo):
    """Nguồn đọc GIẢ + nhật ký URL. `doc_het_review` nhận nguồn làm đối số chính để có ca
    biết trước đáp án — một hàm chỉ chạy trên mạng thật thì không ai đo được nó cắt ở đâu."""
    da = []

    def doc(url, _token):
        da.append(url)
        i = len(da) - 1
        return trang_lo[i] if i < len(trang_lo) else []
    return doc, da


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


def ca_COMMENTED_khong_xoa_ban_duyet(m):
    """P1 `commented-pending-xoa-quyet-dinh-cu`, chiều CHẶN OAN.

    Bản cũ lấy bản ghi mới nhất TRƯỚC rồi mới xét state, nên một lời bình gửi sau khi duyệt
    làm mất luôn bản duyệt. Reviewer đo: `APPROVED` → `COMMENTED` ⇒ ĐỎ; `APPROVED` →
    `PENDING` ⇒ ĐỎ. Lời bình không phải quyết định, nó không được xoá quyết định nào."""
    for sau in ("COMMENTED", "PENDING"):
        bg = [_rv("code2nguyen", "APPROVED", "2026-01-01T00:00:00Z"),
              _rv("code2nguyen", sau, "2026-01-02T00:00:00Z")]
        if not m.phan_quyet("ducthangho", bg)[0]:
            raise AssertionError("`%s` mới hơn đã xoá mất bản duyệt còn hiệu lực" % sau)


def ca_COMMENTED_khong_GO_YEU_CAU_SUA(m):
    """P1 `commented-pending-xoa-quyet-dinh-cu`, chiều NGUY HIỂM — và đây mới là chiều làm
    cổng fail-OPEN: `CHANGES_REQUESTED` → `COMMENTED` gỡ mất yêu cầu sửa, rồi một approval
    của người khác đủ làm cổng XANH. Reviewer đo được đúng chuỗi ấy trả ĐẠT."""
    bg = [_rv("ducthangho", "CHANGES_REQUESTED", "2026-01-01T00:00:00Z"),
          _rv("ducthangho", "COMMENTED", "2026-01-02T00:00:00Z"),
          _rv("code2nguyen", "APPROVED", "2026-01-03T00:00:00Z")]
    dat, ly = m.phan_quyet("ducthangho", bg)
    if dat:
        raise AssertionError("một LỜI BÌNH đã gỡ được yêu cầu SỬA: " + ly)


def ca_DISMISSED_go_quyet_dinh(m):
    """`DISMISSED` thì NGƯỢC LẠI — nó LÀ quyết định (quyết định huỷ), nên nó gỡ được.

    Ca này giữ cho bản vá trên không thành "mọi thứ đều không gỡ được": REST đổi chính bản
    ghi cũ sang `DISMISSED` khi bản duyệt bị gỡ, nên state ấy phải cập nhật trạng thái."""
    go_chan = [_rv("ducthangho", "CHANGES_REQUESTED", "2026-01-01T00:00:00Z"),
               _rv("ducthangho", "DISMISSED", "2026-01-02T00:00:00Z"),
               _rv("code2nguyen", "APPROVED", "2026-01-03T00:00:00Z")]
    if not m.phan_quyet("ducthangho", go_chan)[0]:
        raise AssertionError("`DISMISSED` KHÔNG gỡ được yêu cầu sửa đã bị gỡ thật")
    go_duyet = [_rv("code2nguyen", "APPROVED", "2026-01-01T00:00:00Z"),
                _rv("code2nguyen", "DISMISSED", "2026-01-02T00:00:00Z")]
    if m.phan_quyet("ducthangho", go_duyet)[0]:
        raise AssertionError("bản duyệt ĐÃ BỊ GỠ (`DISMISSED`) vẫn được tính")


def ca_trung_moc_thoi_gian_TAT_DINH(m):
    """P2 `timestamp-trung-phu-thuoc-thu-tu-mang`. Bản cũ tie-break bằng VỊ TRÍ TRONG MẢNG:
    reviewer hoán vị hai review mâu thuẫn cùng mốc và nhận hai phán quyết trái nhau.

    Hai chiều, và cả hai đều phải TẤT ĐỊNH:
      · có `id` phân biệt ⇒ `id` lớn hơn thắng, và hai hoán vị cho CÙNG kết quả;
      · thiếu `id` mà hai bản mâu thuẫn ⇒ KHÔNG ĐO ĐƯỢC ⇒ ĐỎ ở CẢ HAI hoán vị."""
    luc = "2026-02-02T02:02:02Z"
    co_ma = [_rv("code2nguyen", "CHANGES_REQUESTED", luc, ma=11),
             _rv("code2nguyen", "APPROVED", luc, ma=22)]
    kq = {m.phan_quyet("ducthangho", co_ma)[0],
          m.phan_quyet("ducthangho", list(reversed(co_ma)))[0]}
    if len(kq) != 1:
        raise AssertionError("cùng dữ liệu, hai hoán vị cho hai phán quyết khác nhau")
    if kq != {True}:
        raise AssertionError("`id` lớn hơn (APPROVED) phải thắng mà cổng vẫn chặn")
    khong_ma = [_rv("code2nguyen", "CHANGES_REQUESTED", luc),
                _rv("code2nguyen", "APPROVED", luc)]
    for bo in (khong_ma, list(reversed(khong_ma))):
        dat, ly = m.phan_quyet("ducthangho", bo)
        if dat or "KHÔNG ĐO ĐƯỢC" not in ly:
            raise AssertionError("mâu thuẫn KHÔNG tách được mà không ĐỎ: " + ly)


def ca_MOC_THOI_GIAN_so_theo_THOI_DIEM_khong_theo_CHUOI(m):
    """F3 của cross-review lượt 2: bản đầu so `submitted_at` bằng CHUỖI.

    Hai chiều. Chiều một là chính ca reviewer dựng: `APPROVED` lúc `12:00:00+07:00` (=05:00Z)
    so với `CHANGES_REQUESTED` lúc `06:00:00Z` — bản CHẶN muộn hơn THẬT, nhưng theo thứ tự
    chuỗi thì `"12:00…+07" > "06:00…Z"` nên bản duyệt thắng và cổng trả XANH.
    Chiều hai chặn bản vá thành fail-close mù: mốc HỎNG phải là KHÔNG ĐO ĐƯỢC, và mốc HỢP LỆ
    ở nhiều dạng viết (có phần giây lẻ, offset không có dấu hai chấm) vẫn phải đọc được."""
    lech_mui = [_rv("code2nguyen", "APPROVED", "2026-05-05T12:00:00+07:00", ma=1),
                _rv("code2nguyen", "CHANGES_REQUESTED", "2026-05-05T06:00:00Z", ma=2)]
    dat, ly = m.phan_quyet("ducthangho", lech_mui)
    if dat:
        raise AssertionError("bản CHẶN muộn hơn THẬT bị thua vì so chuỗi: " + ly)
    hong = [_rv("code2nguyen", "APPROVED", "hom qua")]
    dat, ly = m.phan_quyet("ducthangho", hong)
    if dat or "KHÔNG ĐO ĐƯỢC" not in ly:
        raise AssertionError("mốc thời gian HỎNG phải là KHÔNG ĐO ĐƯỢC và ĐỎ: " + ly)
    for dang in ("2026-05-05T06:00:00.123Z", "2026-05-05T06:00:00+0000",
                 "2026-05-05T06:00:00+00:00"):
        if not m.phan_quyet("ducthangho", [_rv("code2nguyen", "APPROVED", dang)])[0]:
            raise AssertionError("mốc HỢP LỆ dạng %r bị từ chối oan" % dang)


def ca_login_BOT_trung_ten_khong_tinh(m):
    """Bản ghi mang `user.type` khác `User` không được tính là bản duyệt của người ấy.

    Nói thẳng phạm vi: login bot GitHub luôn có hậu tố `[bot]` nên ca này CHƯA CHỨNG MINH
    ĐƯỢC là xảy ra thật — nó chốt một giả định rẻ, không phải một lỗ đã đo."""
    if m.phan_quyet("ducthangho", [_rv("code2nguyen", kieu="Bot")])[0]:
        raise AssertionError("bản ghi `type=Bot` trùng login vẫn được tính là duyệt")


# ── TẦNG A2 — phân trang ───────────────────────────────────────────────────────────────
def ca_doc_HET_moi_trang(m):
    """P1 `reviews-qua-100-bi-cat-va-fail-open`, đo trên chính đường đọc."""
    lo1 = [_rv("nguoi-%d" % i, "COMMENTED", ma=i) for i in range(100)]
    lo2 = [_rv("code2nguyen", "CHANGES_REQUESTED", "2026-03-03T00:00:00Z", ma=999)]
    nguon, da = _nguon([lo1, lo2])
    het = m.doc_het_review("G", "t", doc=nguon)
    if len(het) != 101:
        raise AssertionError("đọc được %d/101 bản ghi — cắt mất trang sau" % len(het))
    if len(da) != 2 or "page=1" not in da[0] or "page=2" not in da[1]:
        raise AssertionError("chuỗi URL đã gọi KHÔNG đúng hai trang: %s" % da)


def ca_quyet_dinh_o_TRANG_SAU_van_chan(m):
    """Hai chiều trên CÙNG một tập dữ liệu, và chiều thứ hai mới là bằng chứng:
    tập ĐỦ 101 bản ghi ⇒ ĐỎ; nhìn ĐÚNG 100 bản đầu ⇒ XANH. Chênh lệch ấy chính là thứ bản
    cũ đẩy ra khỏi tầm nhìn của cổng, và reviewer đo được `main()` in `XANH` với `rc=0`."""
    lo1 = ([_rv("code2nguyen", "APPROVED", "2026-01-01T00:00:00Z", ma=1)]
           + [_rv("nguoi-%d" % i, "COMMENTED", ma=100 + i) for i in range(99)])
    lo2 = [_rv("code2nguyen", "CHANGES_REQUESTED", "2026-03-03T00:00:00Z", ma=999)]
    nguon, _ = _nguon([lo1, lo2])
    du = m.doc_het_review("G", "t", doc=nguon)
    if m.phan_quyet("ducthangho", du)[0]:
        raise AssertionError("quyết định CHẶN ở trang 2 không được tính")
    if not m.phan_quyet("ducthangho", lo1)[0]:
        raise AssertionError("ca RỖNG: nhìn 100 bản đầu lẽ ra XANH, mà nó đã ĐỎ sẵn")


def ca_cham_TRAN_TRANG_la_KHONG_DO_DUOC(m):
    """Máy chủ trả mãi trang đầy thì cổng KHÔNG ĐƯỢC coi là đã đọc hết. Trần cũng là chốt
    chống lặp vô hạn — một cổng treo là một cổng vắng mặt."""
    day = [_rv("nguoi-%d" % i, "COMMENTED", ma=i) for i in range(5)]
    nguon, da = _nguon([day] * 50)
    try:
        m.doc_het_review("G", "t", doc=nguon, tran=3, moi_trang=5)
    except m.KhongDoDuoc:
        if len(da) != 3:
            raise AssertionError("chạm trần sau %d lượt đọc, đòi đúng 3" % len(da))
        return
    raise AssertionError("chạm TRẦN mà vẫn trả về danh sách như thể đã đọc hết")


def ca_TRAN_TRANG_MAC_DINH_co_rang(m):
    """Goi KHONG truyen `tran` de ghim chinh hang `_TRAN_TRANG=20` cua duong that.

    Ca cu truyen `tran=3`, nen doi hang thanh `10**9` van xanh. Nguon nay co 21 trang
    day roi moi het: ban dung phai dung sau 20 lan; mutant vo tran se doc tiep va lo ra.
    """
    day = [_rv("nguoi", "COMMENTED", ma=1)]
    nguon, da = _nguon([day] * 21 + [[]])
    try:
        m.doc_het_review("G", "t", doc=nguon, moi_trang=1)
    except m.KhongDoDuoc:
        if len(da) != 20:
            raise AssertionError("tran mac dinh dung sau %d lan, doi dung 20" % len(da))
        return
    raise AssertionError("hang _TRAN_TRANG khong con chan duong goi mac dinh")


def ca_phan_hoi_KHONG_phai_danh_sach_la_KHONG_DO_DUOC(m):
    nguon, _ = _nguon([{"message": "Not Found"}])
    try:
        m.doc_het_review("G", "t", doc=nguon)
    except m.KhongDoDuoc:
        return
    raise AssertionError("phản hồi không phải danh sách mà vẫn đi tiếp")


# ── TẦNG B — hình dạng workflow ────────────────────────────────────────────────────────
def ca_workflow_tin_cay_KHOP_GOLDEN(m):
    """So NGUYÊN CÂY, không ghép các allow-list rời rồi bỏ hở một mức khác.

    `loi_quyen` cũ bị gỡ cùng các phép so từng mảnh. Nó đòi khai quyền ở cả workflow lẫn
    job rồi gọi cấu hình chỉ-job là "không chỉ-đọc", dù GitHub cho cấu hình ấy có thể chỉ
    đọc thật. Golden ở đây cố ý chặt hơn vì nó đóng băng TOÀN workflow; thông báo chỉ nói
    cây lệch canonical, không gán sai ngữ nghĩa quyền cho một cấu hình khác."""
    thuc = _yaml()
    if thuc != _GOLDEN_WORKFLOW_TIN_CAY:
        raise AssertionError("workflow tin cậy KHÁC golden — "
                             + _lech_sau(_GOLDEN_WORKFLOW_TIN_CAY, thuc))


def ca_khong_co_cu_phap_bieu_thuc_trong_run(m):
    """Đã trả giá 16-08-2026: một cặp ngoặc biểu thức RỖNG trong CHÚ THÍCH của `run` làm cả
    tệp bị GitHub TỪ CHỐI (run mang tên đường dẫn tệp, 0 job). Quét CẢ HAI lane."""
    xau = [(p.name, b.get("name") or b.get("uses"))
           for p in (YML, YML2)
           for j in (_doc_yaml(p)["jobs"] or {}).values() for b in j["steps"]
           if _MO_BIEU_THUC in str(b.get("run") or "")]
    if xau:
        raise AssertionError("có cú pháp biểu thức trong thân `run`: %s" % xau)


def ca_hai_lane_KHAC_context(m):
    """P1 `runbook-chua-tach-rieng-bang-chung-cua-check-cong`.

    Context của một required check là `<tên workflow> / <tên job>`. Khi hai lane ở CHUNG một
    tệp, job `cong` xuất hiện ở cả lane `pull_request` (với kết luận `skipped`) lẫn lane tin
    cậy, mang CÙNG một context — người cấu hình branch protection không phân biệt được. Tách
    tệp là chưa đủ nếu hai tệp trùng `name:`; ca này đo đúng thứ quyết định context."""
    d1, d2 = _yaml(), _yaml2()
    if str(d1.get("name") or "") == str(d2.get("name") or ""):
        raise AssertionError("hai lane TRÙNG `name:` ⇒ context check trùng: %r"
                             % d1.get("name"))
    sk2 = _su_kien(d2)
    if sk2 != _SU_KIEN_PHAN_CHUNG:
        raise AssertionError("lane phản chứng có sự kiện %s, đòi đúng %s"
                             % (sorted(sk2), sorted(_SU_KIEN_PHAN_CHUNG)))
    trung = sorted(set(d1["jobs"]) & set(d2["jobs"]))
    if trung:
        raise AssertionError("hai lane trùng tên job: %s" % trung)


_BIEN_THE_KHOA_TRUNG = {
    "permissions-workflow": (
        "name: duyet khac danh tinh\n\non:\n",
        "name: duyet khac danh tinh\n\npermissions:\n  contents: write\n\non:\n",
        "permissions"),
    "permissions-job": (
        "  cong:\n    # Giu lai",
        "  cong:\n    permissions:\n      contents: write\n    # Giu lai",
        "permissions"),
    "runs-on": (
        "    runs-on: ubuntu-latest\n",
        "    runs-on: [self-hosted, linux]\n    runs-on: ubuntu-latest\n",
        "runs-on"),
    "if-always": (
        "    if: github.event_name != 'pull_request'\n",
        "    if: always()\n    if: github.event_name != 'pull_request'\n",
        "if"),
}


def _tep_bien_the_khoa_trung(ten, thu_muc):
    """Dua gia tri DOC o lan khai dau, giu gia tri hop le o lan sau."""
    tim, thay, khoa = _BIEN_THE_KHOA_TRUNG[ten]
    van = YML_GOC.read_text(encoding="utf-8")
    if van.count(tim) != 1:
        raise AssertionError("moc bien the %s khop %d cho" % (ten, van.count(tim)))
    tep = Path(thu_muc) / (ten + ".yml")
    tep.write_text(van.replace(tim, thay, 1), encoding="utf-8")
    return tep, khoa


def _do_cu_xanh_moi_do_khoa_trung(ten):
    """Tra loi do hai ve: safe_load cu trung golden, loader moi chan dung khoa."""
    with tempfile.TemporaryDirectory(prefix="tl348-dup-") as d:
        tep, khoa = _tep_bien_the_khoa_trung(ten, d)
        cu = yaml.safe_load(tep.read_text(encoding="utf-8"))
        cu_xanh = cu == _GOLDEN_WORKFLOW_TIN_CAY
        loi_moi = ""
        try:
            _doc_yaml(tep)
        except Exception as e:  # noqa: BLE001 - thong diep chan la bang chung cua ca
            loi_moi = str(e)
        moi_do = ("khoa trung: %r" % khoa) in loi_moi
        return cu_xanh, moi_do, loi_moi


def _doi_khoa_trung(ten):
    cu_xanh, moi_do, loi = _do_cu_xanh_moi_do_khoa_trung(ten)
    if not cu_xanh:
        raise AssertionError("fixture %s khong tai hien ban CU xanh" % ten)
    if not moi_do:
        raise AssertionError("loader MOI khong chan dung khoa %s: %s" % (ten, loi))


def ca_khoa_trung_permissions_MUC_WORKFLOW_bi_chan(m):
    _doi_khoa_trung("permissions-workflow")


def ca_khoa_trung_permissions_MUC_JOB_bi_chan(m):
    _doi_khoa_trung("permissions-job")


def ca_khoa_trung_runs_on_bi_chan(m):
    _doi_khoa_trung("runs-on")


def ca_khoa_trung_if_always_bi_chan(m):
    _doi_khoa_trung("if-always")


def ca_khoa_trung_o_lane_PHAN_CHUNG_bi_chan(m):
    """Loader chung phai chan ca tep thu hai, khong chi lane tin cay co golden."""
    tim = "name: phan chung duyet khac danh tinh\n\non:\n"
    thay = ("name: phan chung duyet khac danh tinh\n\npermissions:\n"
            "  contents: write\n\non:\n")
    van = YML2_GOC.read_text(encoding="utf-8")
    if van.count(tim) != 1:
        raise AssertionError("moc lane phan chung khop %d cho" % van.count(tim))
    with tempfile.TemporaryDirectory(prefix="tl348-dup-yml2-") as d:
        tep = Path(d) / "w.yml"
        tep.write_text(van.replace(tim, thay, 1), encoding="utf-8")
        if yaml.safe_load(tep.read_text(encoding="utf-8")) != _doc_yaml(YML2_GOC):
            raise AssertionError("fixture lane phan chung khong tai hien safe_load nuot khoa")
        try:
            _doc_yaml(tep)
        except Exception as e:  # noqa: BLE001 - can doi chieu thong diep khoa trung
            if "khoa trung: 'permissions'" in str(e):
                return
            raise AssertionError("chan sai ly do: %s" % e) from None
    raise AssertionError("lane phan chung van nuot khoa trung")


def ca_khoa_on_CO_THE_TRICH_DAN(m):
    """`on:` va `"on":` la hai cach viet hop le cua cung mot khoa GitHub."""
    van = YML_GOC.read_text(encoding="utf-8")
    tim, thay = "\non:\n", "\n\"on\":\n"
    if van.count(tim) != 1:
        raise AssertionError("moc `on` khop %d cho" % van.count(tim))
    with tempfile.TemporaryDirectory(prefix="tl348-on-") as d:
        tep = Path(d) / "w.yml"
        tep.write_text(van.replace(tim, thay, 1), encoding="utf-8")
        thuc = _doc_yaml(tep)
        if thuc != _GOLDEN_WORKFLOW_TIN_CAY:
            raise AssertionError("`\"on\":` hop le nhung bi golden tu choi: "
                                 + _lech_sau(_GOLDEN_WORKFLOW_TIN_CAY, thuc))


def ca_hai_cach_viet_on_CUNG_LUC_bi_chan(m):
    """Bay thu tam: chuan hoa bang ghi de se nuot mot trong `on:` va `"on":`."""
    tim = "name: duyet khac danh tinh\n\non:\n"
    thay = ("name: duyet khac danh tinh\n\n\"on\":\n"
            "  pull_request: {}\n\non:\n")
    van = YML_GOC.read_text(encoding="utf-8")
    if van.count(tim) != 1:
        raise AssertionError("moc collision `on` khop %d cho" % van.count(tim))
    with tempfile.TemporaryDirectory(prefix="tl348-on-collision-") as d:
        tep = Path(d) / "w.yml"
        tep.write_text(van.replace(tim, thay, 1), encoding="utf-8")
        try:
            _doc_yaml(tep)
        except ValueError as e:
            if "khoa trung ngu nghia: 'on'" in str(e):
                return
            raise AssertionError("chan sai ly do: %s" % e) from None
    raise AssertionError("co ca `on:` va `\"on\":` ma phep chuan hoa van ghi de")


def _kiem_actionlint(tim=None, chay=None):
    """Lint dung hai workflow packet; thieu binary la KHONG DO DUOC va phai do."""
    import shutil
    import subprocess
    tim = tim or shutil.which
    chay = chay or subprocess.run
    duong = tim("actionlint")
    if not duong:
        raise AssertionError(
            "KHONG DO DUOC: thieu `actionlint`. PyYAML khong biet luat workflow GitHub. "
            "Cai 1.7.7: `bash ops/cai_actionlint.sh` (hoac tai binary tu releases).")
    p = chay([duong, str(YML_GOC), str(YML2_GOC)], capture_output=True, text=True)
    if p.returncode != 0:
        raise AssertionError("actionlint DO (rc=%d) tren hai workflow packet:\n%s%s"
                             % (p.returncode, p.stdout, p.stderr))


def ca_hai_workflow_QUA_ACTIONLINT(m):
    _kiem_actionlint()


def ca_thieu_ACTIONLINT_la_DO(m):
    try:
        _kiem_actionlint(tim=lambda _ten: None)
    except AssertionError as e:
        if "KHONG DO DUOC: thieu `actionlint`" in str(e):
            return
        raise AssertionError("thieu cong cu nhung do sai ly do: %s" % e) from None
    raise AssertionError("thieu actionlint ma tang dinh nghia van xanh")


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
    ("COMMENTED_khong_xoa_ban_duyet", ca_COMMENTED_khong_xoa_ban_duyet),
    ("COMMENTED_khong_GO_YEU_CAU_SUA", ca_COMMENTED_khong_GO_YEU_CAU_SUA),
    ("DISMISSED_go_quyet_dinh", ca_DISMISSED_go_quyet_dinh),
    ("trung_moc_thoi_gian_TAT_DINH", ca_trung_moc_thoi_gian_TAT_DINH),
    ("MOC_THOI_GIAN_so_theo_THOI_DIEM_khong_theo_CHUOI",
     ca_MOC_THOI_GIAN_so_theo_THOI_DIEM_khong_theo_CHUOI),
    ("login_BOT_trung_ten_khong_tinh", ca_login_BOT_trung_ten_khong_tinh),
    ("doc_HET_moi_trang", ca_doc_HET_moi_trang),
    ("quyet_dinh_o_TRANG_SAU_van_chan", ca_quyet_dinh_o_TRANG_SAU_van_chan),
    ("cham_TRAN_TRANG_la_KHONG_DO_DUOC", ca_cham_TRAN_TRANG_la_KHONG_DO_DUOC),
    ("TRAN_TRANG_MAC_DINH_co_rang", ca_TRAN_TRANG_MAC_DINH_co_rang),
    ("phan_hoi_KHONG_phai_danh_sach_la_KHONG_DO_DUOC",
     ca_phan_hoi_KHONG_phai_danh_sach_la_KHONG_DO_DUOC),
    ("workflow_tin_cay_KHOP_GOLDEN", ca_workflow_tin_cay_KHOP_GOLDEN),
    ("khong_co_cu_phap_bieu_thuc_trong_run", ca_khong_co_cu_phap_bieu_thuc_trong_run),
    ("hai_lane_KHAC_context", ca_hai_lane_KHAC_context),
    ("khoa_trung_permissions_MUC_WORKFLOW_bi_chan",
     ca_khoa_trung_permissions_MUC_WORKFLOW_bi_chan),
    ("khoa_trung_permissions_MUC_JOB_bi_chan",
     ca_khoa_trung_permissions_MUC_JOB_bi_chan),
    ("khoa_trung_runs_on_bi_chan", ca_khoa_trung_runs_on_bi_chan),
    ("khoa_trung_if_always_bi_chan", ca_khoa_trung_if_always_bi_chan),
    ("khoa_trung_o_lane_PHAN_CHUNG_bi_chan", ca_khoa_trung_o_lane_PHAN_CHUNG_bi_chan),
    ("khoa_on_CO_THE_TRICH_DAN", ca_khoa_on_CO_THE_TRICH_DAN),
    ("hai_cach_viet_on_CUNG_LUC_bi_chan", ca_hai_cach_viet_on_CUNG_LUC_bi_chan),
    ("hai_workflow_QUA_ACTIONLINT", ca_hai_workflow_QUA_ACTIONLINT),
    ("thieu_ACTIONLINT_la_DO", ca_thieu_ACTIONLINT_la_DO),
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
    "lay_quyet_dinh_CU_NHAT": (
        "    luc_max = max(x[0] for x in ban_ghi)",
        "    luc_max = min(x[0] for x in ban_ghi)",
        ["CHI_tinh_review_MOI_NHAT", "DISMISSED_go_quyet_dinh",
         "MOC_THOI_GIAN_so_theo_THOI_DIEM_khong_theo_CHUOI",
         "quyet_dinh_o_TRANG_SAU_van_chan"]),
    "bo_kiem_YEU_CAU_SUA": (
        "    if chan:\n",
        "    if False:\n",
        ["yeu_cau_SUA_chua_go_thi_chan", "COMMENTED_khong_GO_YEU_CAU_SUA"]),
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
    # ── ba đột biến cho P1 `commented-pending-xoa-quyet-dinh-cu` và P2 tie-break ─────────
    "COMMENTED_cung_la_quyet_dinh": (
        '_QUYET_DINH = ("APPROVED", "CHANGES_REQUESTED", "DISMISSED")',
        '_QUYET_DINH = ("APPROVED", "CHANGES_REQUESTED", "DISMISSED", "COMMENTED", "PENDING")',
        ["COMMENTED_khong_xoa_ban_duyet", "COMMENTED_khong_GO_YEU_CAU_SUA"]),
    "DISMISSED_khong_phai_quyet_dinh": (
        '_QUYET_DINH = ("APPROVED", "CHANGES_REQUESTED", "DISMISSED")',
        '_QUYET_DINH = ("APPROVED", "CHANGES_REQUESTED")',
        ["DISMISSED_go_quyet_dinh"]),
    "tie_break_bo_id": (
        "        return int(ma)",
        "        return None",
        ["trung_moc_thoi_gian_TAT_DINH"]),
    "mo_ho_van_tha_ban_dau": (
        '    raise KhongDoDuoc(\n        "%d b',
        '    return dong[0][2], dong[0][3]\n    raise KhongDoDuoc(\n        "%d b',
        ["trung_moc_thoi_gian_TAT_DINH"]),
    "so_MOC_bang_CHUOI_nhu_ban_dau": (
        "            luc = _moc((r or {}).get(\"submitted_at\"))",
        "            luc = str((r or {}).get(\"submitted_at\") or \"\")",
        ["MOC_THOI_GIAN_so_theo_THOI_DIEM_khong_theo_CHUOI"]),
    "moc_HONG_thi_bo_qua_ban_ghi": (
        '        except KhongDoDuoc as e:\n'
        '            # Mốc hỏng là KHÔNG ĐO ĐƯỢC cho CẢ phán quyết, không phải "bỏ qua bản ghi này":\n'
        '            # bỏ qua nghĩa là một bản CHANGES_REQUESTED có mốc lạ biến mất khỏi phép tính.\n'
        '            return False, "KHÔNG ĐO ĐƯỢC: %s — %s" % (ai, e)',
        "        except KhongDoDuoc:\n            continue",
        ["MOC_THOI_GIAN_so_theo_THOI_DIEM_khong_theo_CHUOI"]),
    "bo_kiem_type_bot": (
        '        if str(u.get("type") or "User") != "User":\n            continue\n',
        "",
        ["login_BOT_trung_ten_khong_tinh"]),
    # ── ba đột biến cho P1 `reviews-qua-100-bi-cat-va-fail-open` ────────────────────────
    "chi_doc_TRANG_DAU": (
        "        if len(lo) < moi_trang:\n            return het\n",
        "        return het\n",
        ["doc_HET_moi_trang", "quyet_dinh_o_TRANG_SAU_van_chan",
         "cham_TRAN_TRANG_la_KHONG_DO_DUOC", "TRAN_TRANG_MAC_DINH_co_rang"]),
    "cham_TRAN_van_tra_ve": (
        '            raise KhongDoDuoc(\n                "review vượt trần',
        '            return het\n            raise KhongDoDuoc(\n                "review vượt trần',
        ["cham_TRAN_TRANG_la_KHONG_DO_DUOC", "TRAN_TRANG_MAC_DINH_co_rang"]),
    "bo_kiem_kieu_danh_sach": (
        "        if not isinstance(lo, list):\n",
        "        if False:\n",
        ["phan_hoi_KHONG_phai_danh_sach_la_KHONG_DO_DUOC"]),
    "noi_TRAN_TRANG_MAC_DINH": (
        "_TRAN_TRANG = 20",
        "_TRAN_TRANG = 10**9",
        ["TRAN_TRANG_MAC_DINH_co_rang"]),
}

_DICH_GOLDEN = ["workflow_tin_cay_KHOP_GOLDEN"]

DOT_BIEN_YML = {
    # P2 `cho-phep-muc-workflow-khong-day-du`: ba mức/giá trị này cùng đi vòng qua các
    # allow-list rời cũ. Cả ba phải chết ở đúng MỘT phép so toàn cây.
    "them_env_MUC_WORKFLOW": (
        "name: duyet khac danh tinh\n\non:\n",
        "name: duyet khac danh tinh\n\nenv:\n  PYTHONPATH: /tmp/ma-la\n\non:\n",
        _DICH_GOLDEN),
    "them_defaults_shell_MUC_WORKFLOW": (
        "name: duyet khac danh tinh\n\non:\n",
        "name: duyet khac danh tinh\n\ndefaults:\n  run:\n    shell: bash -x {0}\n\non:\n",
        _DICH_GOLDEN),
    "doi_runs_on_sang_SELF_HOSTED": (
        "    runs-on: ubuntu-latest\n",
        "    runs-on: [self-hosted, linux]\n",
        _DICH_GOLDEN),
    # F1 cross-review lượt 2 — hai đường lách reviewer đo được, cả hai từng cho `29/29 xanh`.
    "them_job_thu_hai_EVIL": (
        "jobs:\n  cong:\n",
        "jobs:\n  evil:\n    runs-on: ubuntu-latest\n    permissions:\n"
        "      contents: write\n    steps:\n      - uses: actions/checkout@v4\n"
        "        with:\n          ref: " + _MO_BIEU_THUC + " github.event.pull_request.head.sha }}\n"
        "      - run: bash ./tu-nhanh-PR.sh\n  cong:\n",
        _DICH_GOLDEN),
    "them_khoa_MUC_JOB_continue_on_error": (
        "    runs-on: ubuntu-latest\n    permissions:\n",
        "    runs-on: ubuntu-latest\n    continue-on-error: true\n    permissions:\n",
        _DICH_GOLDEN),
    # B1 — đúng đường lách reviewer đo được: điều kiện còn nguyên hai mẩu chuỗi cũ mà vẫn
    # luôn đúng. Bản cũ cho `18/18, dead=NONE`.
    "noi_them_ve_LUON_DUNG": (
        "    if: github.event_name != 'pull_request'\n",
        "    if: github.event_name != 'pull_request' || always()\n",
        _DICH_GOLDEN),
    "dung_pull_request_thay_vi_target": (
        "    if: github.event_name != 'pull_request'\n",
        "    if: always()\n",
        _DICH_GOLDEN),
    "them_su_kien_pull_request": (
        "  pull_request_review:\n",
        "  pull_request:\n    types: [opened]\n  pull_request_review:\n",
        _DICH_GOLDEN),
    # B2 — checkout head PR trong job cầm token.
    "checkout_head_PR": (
        "          ref: ${{ github.event.pull_request.base.ref }}\n",
        "          ref: ${{ github.event.pull_request.head.sha }}\n",
        _DICH_GOLDEN),
    "workflow_quen_truyen_head_sha": (
        ' \\\n                 --tac-gia "$TL_TAC_GIA" --head-sha "$TL_HEAD"\n',
        ' --tac-gia "$TL_TAC_GIA"\n',
        _DICH_GOLDEN),
    "quyen_ghi": (
        "permissions:\n  contents: read\n  pull-requests: read\n\njobs:\n",
        "permissions:\n  contents: write\n  pull-requests: read\n\njobs:\n",
        _DICH_GOLDEN),
    "bo_khai_quyen": (
        "permissions:\n  contents: read\n  pull-requests: read\n\njobs:\n",
        "jobs:\n",
        _DICH_GOLDEN),
    # B2 — hai đường lách reviewer đo được, cả hai từng cho `18/18 dead=NONE`.
    "job_GHI_DE_quyen_write": (
        "    permissions:\n      contents: read\n      pull-requests: read\n",
        "    permissions:\n      contents: write\n      pull-requests: read\n",
        _DICH_GOLDEN),
    "them_buoc_KEO_HEAD_PR": (
        "      - name: do nguoi duyet khac nguoi tao PR\n",
        "      - name: lay them ma cua PR\n        run: |\n"
        "          set -eu\n          git fetch origin \"$GITHUB_SHA\"\n"
        "          git checkout FETCH_HEAD\n"
        "      - name: do nguoi duyet khac nguoi tao PR\n",
        _DICH_GOLDEN),
    # ba đường lách reviewer lượt 2 đo được trên bản `with` chỉ-đòi-có-mặt.
    "them_with_repository_kho_LA": (
        "          persist-credentials: false\n",
        "          persist-credentials: false\n          repository: nguoi-la/kho-doc-hai\n",
        _DICH_GOLDEN),
    "them_with_token_bi_mat_KHAC": (
        "          persist-credentials: false\n",
        "          persist-credentials: false\n          token: " + _MO_BIEU_THUC + " secrets.PAT_GHI }}\n",
        _DICH_GOLDEN),
    "them_with_khoa_VO_HAI": (
        "          persist-credentials: false\n",
        "          persist-credentials: false\n          fetch-depth: 0\n",
        _DICH_GOLDEN),
    "doi_env_TL_KHO_sang_kho_FORK": (
        "          TL_KHO: ${{ github.repository }}\n",
        "          TL_KHO: ${{ github.event.pull_request.head.repo.full_name }}\n",
        _DICH_GOLDEN),
}

DOT_BIEN_YML2 = {
    "hai_lane_TRUNG_TEN": (
        "name: phan chung duyet khac danh tinh\n",
        "name: duyet khac danh tinh\n",
        ["hai_lane_KHAC_context"]),
    "lane_phan_chung_THANH_TIN_CAY": (
        "on:\n  pull_request:\n",
        "on:\n  pull_request_target:\n",
        ["hai_lane_KHAC_context"]),
}


def _chay(chi=None, m=None, doi_yml=None, doi_yml2=None,
          doc_yaml=None, kiem_actionlint=None):
    """Tra ket qua; cho dot bien thay DUNG mot tang noi bo trong pham vi mot luot."""
    global YML, YML2, _doc_yaml, _kiem_actionlint
    cu, cu2 = YML, YML2
    cu_doc, cu_actionlint = _doc_yaml, _kiem_actionlint
    tam_da_tao = []
    try:
        if doc_yaml is not None:
            _doc_yaml = doc_yaml
        if kiem_actionlint is not None:
            _kiem_actionlint = kiem_actionlint
        for nhan, doi in (("yml", doi_yml), ("yml2", doi_yml2)):
            if not doi:
                continue
            nguon = cu if nhan == "yml" else cu2
            goc = nguon.read_text(encoding="utf-8")
            tim, thay = doi
            if goc.count(tim) != 1:
                raise AssertionError("MỐC YAML (%s) khớp %d chỗ" % (nhan, goc.count(tim)))
            # Dung context co chu so huu de mutation khong de scratch lai sau suite.
            # TMPDIR duoc co lap theo packet; chi don dung thu muc do chinh luot nay tao.
            chu_tam = tempfile.TemporaryDirectory(prefix="tl348-")
            tam_da_tao.append(chu_tam)
            tam = Path(chu_tam.name) / "w.yml"
            tam.write_text(goc.replace(tim, thay, 1), encoding="utf-8")
            if nhan == "yml":
                YML = tam
            else:
                YML2 = tam
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
        YML, YML2 = cu, cu2
        _doc_yaml, _kiem_actionlint = cu_doc, cu_actionlint
        for chu_tam in reversed(tam_da_tao):
            chu_tam.cleanup()


def _ap(van, tim, thay):
    if van.count(tim) != 1:
        raise AssertionError("MỐC khớp %d chỗ: %r" % (van.count(tim), tim[:56]))
    return van.replace(tim, thay, 1)


def _khai(ten, chet, dich, hong):
    """Đòi tập ca chết BẰNG tập đã khai — không phải "chứa". Xem docstring đầu tệp."""
    ok = sorted(chet) == sorted(dich)
    print(f"  {'ok ' if ok else 'LỖI'} {ten} → giết {sorted(chet) or 'KHÔNG CA NÀO'}")
    if not ok:
        thieu = [x for x in dich if x not in chet]
        thua = [x for x in chet if x not in dich]
        hong.append(f"{ten}: khai {sorted(dich)}; thiếu={thieu} thừa={thua}")


def _chung_minh_khoa_trung(ten):
    if ten not in _BIEN_THE_KHOA_TRUNG:
        print("bien the khong hop le: %s; chon: %s"
              % (ten, ", ".join(sorted(_BIEN_THE_KHOA_TRUNG))))
        return 2
    cu_xanh, moi_do, loi = _do_cu_xanh_moi_do_khoa_trung(ten)
    print("%s: CU=%s (yaml.safe_load khop golden)" %
          (ten, "XANH" if cu_xanh else "DO"))
    print("%s: MOI=%s (%s)" %
          (ten, "DO" if moi_do else "XANH", loi.replace("\n", " | ")))
    return 0 if cu_xanh and moi_do else 1


def main() -> int:
    if len(sys.argv) > 1:
        if len(sys.argv) == 3 and sys.argv[1] == "--chung-minh-khoa-trung":
            return _chung_minh_khoa_trung(sys.argv[2])
        print("dung: duyet_danh_tinh_test.py "
              "[--chung-minh-khoa-trung permissions-workflow|permissions-job|runs-on|if-always]")
        return 2

    dat, ly = _chay()
    so_dot_bien_noi_bo = 4
    so_dot_bien = (len(DOT_BIEN_MA) + len(DOT_BIEN_YML) + len(DOT_BIEN_YML2)
                   + so_dot_bien_noi_bo)
    do_san = sorted(k for k, v in dat.items() if v is False)
    print(f"nền: {sum(1 for v in dat.values() if v)}/{len(dat)} đạt")
    for k in do_san:
        print(f"  ĐỎ    {k}: {ly[k]}")
    if do_san:
        # Nền đỏ thì mọi đột biến "giết" tầm thường bằng chính ca đỏ sẵn — tỷ lệ ấy KHÔNG
        # CÓ NGHĨA. Bài học P1 của PR #342, và nay là nếp chung của kho.
        print(f"\nTỪ CHỐI công bố điểm đột biến: nền có {len(do_san)} ca ĐỎ")
        print(f"SO LIEU: ca={len(dat)}; dot bien={so_dot_bien}")
        print("TONG: HONG")
        return 1

    print("\ntự chứng minh KHÔNG RỖNG (giết ĐÚNG và CHỈ ĐÚNG tập ca đã khai):")
    hong = []
    goc_ma = MA.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="tl348-mut-") as d:
        for ten, (tim, thay, dich) in sorted(DOT_BIEN_MA.items()):
            f = Path(d) / f"{ten}.py"
            f.write_text(_ap(goc_ma, tim, thay), encoding="utf-8")
            sp = importlib.util.spec_from_file_location("mut_" + ten, str(f))
            mo = importlib.util.module_from_spec(sp)
            sp.loader.exec_module(mo)
            d2, _ = _chay(m=mo)
            _khai(ten, [k for k, v in d2.items() if v is False], dich, hong)

    for bang, khoa in ((DOT_BIEN_YML, "doi_yml"), (DOT_BIEN_YML2, "doi_yml2")):
        for ten, (tim, thay, dich) in sorted(bang.items()):
            d2, _ = _chay(**{khoa: (tim, thay)})
            _khai(ten, [k for k, v in d2.items() if v is False], dich, hong)

    noi_bo = (
        ("safe_load_nuot_khoa_trung",
         {"doc_yaml": _doc_yaml_safe_load_roi_chuan_on},
         ["khoa_trung_permissions_MUC_WORKFLOW_bi_chan",
          "khoa_trung_permissions_MUC_JOB_bi_chan",
          "khoa_trung_runs_on_bi_chan", "khoa_trung_if_always_bi_chan",
          "khoa_trung_o_lane_PHAN_CHUNG_bi_chan"]),
        ("tu_choi_khoa_on_trich_dan",
         {"doc_yaml": _doc_yaml_khong_chuan_on},
         ["khoa_on_CO_THE_TRICH_DAN", "hai_cach_viet_on_CUNG_LUC_bi_chan"]),
        ("chuan_on_bang_GHI_DE",
         {"doc_yaml": _doc_yaml_on_de_len},
         ["hai_cach_viet_on_CUNG_LUC_bi_chan"]),
    )
    for ten, doi, dich in noi_bo:
        d2, _ = _chay(**doi)
        _khai(ten, [k for k, v in d2.items() if v is False], dich, hong)

    kiem_that = _kiem_actionlint

    def bo_qua_actionlint_vang(tim=None, chay=None):
        import shutil
        tim_that = tim or shutil.which
        if not tim_that("actionlint"):
            return None
        return kiem_that(tim=tim, chay=chay)

    d2, _ = _chay(kiem_actionlint=bo_qua_actionlint_vang)
    _khai("thieu_actionlint_van_xanh",
          [k for k, v in d2.items() if v is False], ["thieu_ACTIONLINT_la_DO"], hong)

    print("NỢ  : `ngu-nghia-trigger-chua-do-bang-PR-doi-khang` — tầng (B) đo HÌNH DẠNG tệp,")
    print("      KHÔNG đo hành vi trigger của GitHub. Muốn đo thật phải mở PR đối kháng;")
    print("      bước nghiệm thu của `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` là chỗ làm việc đó.")
    print(f"SO LIEU: ca={len(dat)}; dot bien={so_dot_bien}")
    if hong:
        print("CHI TIET HONG: %d lỗi" % len(hong))
        for x in hong:
            print("   " + x)
        print("TONG: HONG")
        return 1
    print("TONG: DAT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
