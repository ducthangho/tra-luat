#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phản chứng CHẠY ĐƯỢC cho cổng `duyet-khac-danh-tinh` — packet #348.

HAI TẦNG, vì cổng này có hai mặt hỏng khác hẳn nhau:

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
     danh sách CHO PHÉP" (`lease-authority-spoof`, v1.36.68). Nay tầng (B) là ba allow-list:
     TẬP SỰ KIỆN · BIỂU THỨC `if` sau chuẩn hoá · TOPOLOGY các bước của job `cong` (đúng 2
     bước, thân `run` và bảng `env` khớp nguyên văn).

     NÓI RÕ GIỚI HẠN, đừng để ai đọc mạnh hơn: tầng (B) đo HÌNH DẠNG TỆP, KHÔNG đo hành vi
     của GitHub. Nó không chứng minh `pull_request_target` thật sự lấy workflow từ nhánh cơ
     sở — nó chứng minh cổng đã được viết theo cách chỉ đúng NẾU điều đó đúng. Muốn đo hành
     vi thật thì phải mở một PR đối kháng, và đó là việc của bước nghiệm thu trong
     `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md`. Nợ có tên:
     `ngu-nghia-trigger-chua-do-bang-PR-doi-khang`.

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

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MA = HERE / "duyet_danh_tinh.py"
YML = ROOT / ".github" / "workflows" / "duyet-khac-danh-tinh.yml"    # lane TIN CẬY
YML2 = ROOT / ".github" / "workflows" / "duyet-phan-chung.yml"       # lane PHẢN CHỨNG

# DỰNG SAU KHI PHÂN TÍCH CÚ PHÁP, không cho chuỗi này đi nguyên văn trên đường truyền.
# Cùng lý do với mẹo `chr(92)` trong `CLAUDE.md`: nội dung NÓI VỀ một cú pháp thì phải
# tránh để chính cú pháp ấy bị một tầng nào đó diễn giải.
_MO_BIEU_THUC = "$" + "{" + "{"


def _bt(x):
    return "%s %s }}" % (_MO_BIEU_THUC, x)


# ── BA ALLOW-LIST CỦA TẦNG (B) ─────────────────────────────────────────────────────────
_SU_KIEN_CHO_PHEP = {"pull_request_target", "pull_request_review"}
_SU_KIEN_PHAN_CHUNG = {"pull_request"}
_DIEU_KIEN_CHO_PHEP = ("github.event_name != 'pull_request'",)
_QUYEN_CHO_PHEP = {"read", "none"}
_CHECKOUT = "actions/checkout@v4"

_RUN_CONG = ('set -eu '
             'PY="$(command -v python3 || command -v python || command -v py)" '
             '"$PY" .claude/dev/duyet_danh_tinh.py --kho "$TL_KHO" --pr "$TL_PR" '
             '--tac-gia "$TL_TAC_GIA" --head-sha "$TL_HEAD"')

# `env` PHẢI KHỚP NGUYÊN VĂN, không chỉ khớp TÊN BIẾN. Thân `run` cố định rồi thì đường
# tấn công còn lại là ĐỔI GIÁ TRỊ: `TL_KHO: <biểu thức trỏ head.repo.full_name>` làm cổng
# đi hỏi kho FORK của người mở PR — cổng vẫn chạy đúng script, vẫn xanh, và đo nhầm kho.
_ENV_CONG = {
    "GH_TOKEN": _bt("secrets.GITHUB_TOKEN"),
    "TL_KHO": _bt("github.repository"),
    "TL_PR": _bt("github.event.pull_request.number"),
    "TL_TAC_GIA": _bt("github.event.pull_request.user.login"),
    "TL_HEAD": _bt("github.event.pull_request.head.sha"),
}

_TOPOLOGY_CONG = (
    {"khoa": ("name", "uses", "with"), "uses": _CHECKOUT,
     "with_khoa": ("ref", "persist-credentials"),
     "with_gia_tri": {"persist-credentials": False}},
    {"khoa": ("name", "env", "run"), "run": _RUN_CONG, "env": _ENV_CONG},
)


def _nap():
    sp = importlib.util.spec_from_file_location("tl_duyet", str(MA))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _doc_yaml(p):
    import yaml
    return yaml.safe_load(p.read_text(encoding="utf-8"))


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


def chuan_hoa_bieu_thuc(s):
    """Chuẩn hoá TỐI THIỂU trước khi so với allow-list: bỏ cặp ngoặc biểu thức bao ngoài,
    thống nhất kiểu nháy, gộp khoảng trắng.

    KHÔNG cố hiểu biểu thức. Hiểu nửa vời chính là lỗ vừa bị đo: bản cũ "hiểu" điều kiện
    bằng cách tìm hai mẩu chuỗi trong đó, và một vế `|| always()` nối thêm vẫn mang đủ hai
    mẩu ấy. So BẰNG NHAU với một tập hữu hạn thì không có chỗ cho vế nối thêm."""
    t = str(s or "").strip()
    if t.startswith(_MO_BIEU_THUC) and t.endswith("}}"):
        t = t[len(_MO_BIEU_THUC):-2].strip()
    return " ".join(t.replace('"', "'").split())


def chuan_hoa_lenh(s):
    """Gộp nối dòng `\\` và mọi khoảng trắng thành một dấu cách, đủ để so BẰNG NHAU mà
    không đỏ giả chỉ vì xuống dòng khác đi."""
    return " ".join(str(s or "").replace("\\\n", " ").split())


def loi_quyen(d, ten_job):
    """Danh sách lỗi quyền HIỆU LỰC (mức workflow HỢP mức job).

    Bản cũ chỉ đọc `permissions` mức workflow. GitHub cho job GHI ĐÈ trọn vẹn khai báo ấy,
    nên đọc một mình mức workflow là đo nửa sự thật — reviewer thêm `permissions: write` vào
    ĐÚNG job cầm token và cả 18 ca cũ vẫn đạt. Đòi CẢ HAI mức: mức workflow vì nó là mặc
    định cho mọi job thêm sau, mức job vì nó là thứ thật sự hiệu lực cho job này."""
    xau = []
    for nhan, o, bat_buoc in (("workflow", d, True),
                              ("job `%s`" % ten_job, (d.get("jobs") or {}).get(ten_job) or {},
                               True)):
        if "permissions" not in o:
            if bat_buoc:
                xau.append("%s KHÔNG khai `permissions` — nhận mặc định của kho" % nhan)
            continue
        q = o["permissions"]
        if isinstance(q, str):
            if q != "read-all":
                xau.append("%s khai `permissions: %s`" % (nhan, q))
            continue
        if not isinstance(q, dict) or not q:
            xau.append("%s khai `permissions` RỖNG/không đọc được: %r" % (nhan, q))
            continue
        xau += ["%s: %s=%s" % (nhan, k, v) for k, v in sorted(q.items())
                if str(v) not in _QUYEN_CHO_PHEP]
    return xau


def loi_topology(cac_buoc):
    """Danh sách lỗi topology của job `cong` — ALLOW-LIST, không phải danh sách cấm.

    Bản cũ cấm đúng hai chuỗi (`pip install`, `npm `). Reviewer chèn một bước kéo head PR
    bằng `git` và không chạm hai chuỗi ấy: `18/18 dead=NONE`. Danh sách cấm phải đoán trước
    mọi cách chạy mã lạ (`curl|sh`, `gh pr checkout`, `actions/download-artifact`, một
    action bất kỳ ở phiên bản bất kỳ) nên thua từ trong thiết kế. Tập bước HỢP LỆ thì hữu
    hạn và biết trước: đúng hai bước, và cả hai khớp nguyên văn.

    GIÁ PHẢI TRẢ, nói thẳng: đổi workflow một cách CHÍNH ĐÁNG cũng làm ca này đỏ, và người
    đổi phải cập nhật bảng trên. Đó là chi phí đúng với một job cầm token của kho."""
    xau = []
    if len(cac_buoc) != len(_TOPOLOGY_CONG):
        return ["job `cong` có %d bước, allow-list đòi ĐÚNG %d"
                % (len(cac_buoc), len(_TOPOLOGY_CONG))]
    for i, (b, mau) in enumerate(zip(cac_buoc, _TOPOLOGY_CONG), 1):
        thua = sorted(set(b) - set(mau["khoa"]))
        if thua:
            xau.append("bước %d có khoá NGOÀI allow-list: %s" % (i, thua))
        if "uses" in mau and str(b.get("uses") or "") != mau["uses"]:
            xau.append("bước %d: `uses`=%r, allow-list đòi %r"
                       % (i, b.get("uses"), mau["uses"]))
        if "run" in mau and chuan_hoa_lenh(b.get("run")) != mau["run"]:
            xau.append("bước %d: thân `run` KHÁC bản trong allow-list" % i)
        if "env" in mau and dict(b.get("env") or {}) != mau["env"]:
            xau.append("bước %d: bảng `env` KHÁC bản trong allow-list" % i)
        w = b.get("with") or {}
        thieu = sorted(set(mau.get("with_khoa") or ()) - set(w))
        if thieu:
            xau.append("bước %d: `with` thiếu %s" % (i, thieu))
        for k, v in sorted((mau.get("with_gia_tri") or {}).items()):
            if w.get(k) != v:
                xau.append("bước %d: `with.%s`=%r, allow-list đòi %r" % (i, k, w.get(k), v))
    return xau


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


def ca_phan_hoi_KHONG_phai_danh_sach_la_KHONG_DO_DUOC(m):
    nguon, _ = _nguon([{"message": "Not Found"}])
    try:
        m.doc_het_review("G", "t", doc=nguon)
    except m.KhongDoDuoc:
        return
    raise AssertionError("phản hồi không phải danh sách mà vẫn đi tiếp")


# ── TẦNG B — hình dạng workflow ────────────────────────────────────────────────────────
def ca_su_kien_DUNG_allow_list(m):
    """B1, lớp THỨ NHẤT và là lớp mạnh nhất: nếu `on:` không chứa `pull_request` thì không
    có cách nào chạy workflow này từ nhánh PR. ALLOW-LIST, so BẰNG NHAU — thêm bất cứ sự
    kiện nào (kể cả `workflow_run`, `issue_comment`) cũng phải làm ca này đỏ."""
    co = _su_kien(_yaml())
    if co != _SU_KIEN_CHO_PHEP:
        raise AssertionError("tập sự kiện %s KHÁC allow-list %s"
                             % (sorted(co), sorted(_SU_KIEN_CHO_PHEP)))


def ca_cong_KHONG_chay_tren_pull_request(m):
    """B1, lớp THỨ HAI. Bản cũ chỉ đòi chuỗi điều kiện CHỨA `pull_request'` và `!=`, nên một
    vế `|| always()` nối thêm vẫn qua trong khi job chạy ở `pull_request` (P1
    `b1-if-kiem-bang-chuoi-co-the-luon-dung`). Nay so BẰNG NHAU với allow-list."""
    dk = chuan_hoa_bieu_thuc((_yaml()["jobs"]["cong"] or {}).get("if"))
    if dk not in _DIEU_KIEN_CHO_PHEP:
        raise AssertionError("điều kiện của job `cong` NGOÀI allow-list: %r" % dk)


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


def ca_topology_job_cong(m):
    """B2, lớp đóng cả một HỌ đường tấn công thay vì từng đường. Xem `loi_topology`."""
    xau = loi_topology(_yaml()["jobs"]["cong"]["steps"])
    if xau:
        raise AssertionError("; ".join(xau))


def ca_quyen_HIEU_LUC_CHI_DOC(m):
    """P1 `b2-job-permissions-va-buoc-keo-head-deu-mu`: job ghi đè được `permissions`."""
    xau = loi_quyen(_yaml(), "cong")
    if xau:
        raise AssertionError("quyền KHÔNG chỉ-đọc: %s" % ", ".join(xau))


def ca_khong_co_cu_phap_bieu_thuc_trong_run(m):
    """Đã trả giá 16-08-2026: một cặp ngoặc biểu thức RỖNG trong CHÚ THÍCH của `run` làm cả
    tệp bị GitHub TỪ CHỐI (run mang tên đường dẫn tệp, 0 job). Quét CẢ HAI lane."""
    xau = [(p.name, b.get("name") or b.get("uses"))
           for p in (YML, YML2)
           for j in (_doc_yaml(p)["jobs"] or {}).values() for b in j["steps"]
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
    ("login_BOT_trung_ten_khong_tinh", ca_login_BOT_trung_ten_khong_tinh),
    ("doc_HET_moi_trang", ca_doc_HET_moi_trang),
    ("quyet_dinh_o_TRANG_SAU_van_chan", ca_quyet_dinh_o_TRANG_SAU_van_chan),
    ("cham_TRAN_TRANG_la_KHONG_DO_DUOC", ca_cham_TRAN_TRANG_la_KHONG_DO_DUOC),
    ("phan_hoi_KHONG_phai_danh_sach_la_KHONG_DO_DUOC",
     ca_phan_hoi_KHONG_phai_danh_sach_la_KHONG_DO_DUOC),
    ("su_kien_DUNG_allow_list", ca_su_kien_DUNG_allow_list),
    ("cong_KHONG_chay_tren_pull_request", ca_cong_KHONG_chay_tren_pull_request),
    ("cong_KHONG_checkout_head_PR", ca_cong_KHONG_checkout_head_PR),
    ("topology_job_cong", ca_topology_job_cong),
    ("quyen_HIEU_LUC_CHI_DOC", ca_quyen_HIEU_LUC_CHI_DOC),
    ("khong_co_cu_phap_bieu_thuc_trong_run", ca_khong_co_cu_phap_bieu_thuc_trong_run),
    ("workflow_TRUYEN_head_sha", ca_workflow_TRUYEN_head_sha),
    ("hai_lane_KHAC_context", ca_hai_lane_KHAC_context),
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
    "bo_kiem_type_bot": (
        '        if str(u.get("type") or "User") != "User":\n            continue\n',
        "",
        ["login_BOT_trung_ten_khong_tinh"]),
    # ── ba đột biến cho P1 `reviews-qua-100-bi-cat-va-fail-open` ────────────────────────
    "chi_doc_TRANG_DAU": (
        "        if len(lo) < moi_trang:\n            return het\n",
        "        return het\n",
        ["doc_HET_moi_trang", "quyet_dinh_o_TRANG_SAU_van_chan",
         "cham_TRAN_TRANG_la_KHONG_DO_DUOC"]),
    "cham_TRAN_van_tra_ve": (
        '            raise KhongDoDuoc(\n                "review vượt trần',
        '            return het\n            raise KhongDoDuoc(\n                "review vượt trần',
        ["cham_TRAN_TRANG_la_KHONG_DO_DUOC"]),
    "bo_kiem_kieu_danh_sach": (
        "        if not isinstance(lo, list):\n",
        "        if False:\n",
        ["phan_hoi_KHONG_phai_danh_sach_la_KHONG_DO_DUOC"]),
}

DOT_BIEN_YML = {
    # B1 — đúng đường lách reviewer đo được: điều kiện còn nguyên hai mẩu chuỗi cũ mà vẫn
    # luôn đúng. Bản cũ cho `18/18, dead=NONE`.
    "noi_them_ve_LUON_DUNG": (
        "    if: github.event_name != 'pull_request'\n",
        "    if: github.event_name != 'pull_request' || always()\n",
        ["cong_KHONG_chay_tren_pull_request"]),
    "dung_pull_request_thay_vi_target": (
        "    if: github.event_name != 'pull_request'\n",
        "    if: always()\n",
        ["cong_KHONG_chay_tren_pull_request"]),
    "them_su_kien_pull_request": (
        "  pull_request_review:\n",
        "  pull_request:\n    types: [opened]\n  pull_request_review:\n",
        ["su_kien_DUNG_allow_list"]),
    # B2 — checkout head PR trong job cầm token.
    "checkout_head_PR": (
        "          ref: ${{ github.event.pull_request.base.ref }}\n",
        "          ref: ${{ github.event.pull_request.head.sha }}\n",
        ["cong_KHONG_checkout_head_PR"]),
    "workflow_quen_truyen_head_sha": (
        ' \\\n                 --tac-gia "$TL_TAC_GIA" --head-sha "$TL_HEAD"\n',
        ' --tac-gia "$TL_TAC_GIA"\n',
        ["workflow_TRUYEN_head_sha", "topology_job_cong"]),
    "quyen_ghi": (
        "permissions:\n  contents: read\n  pull-requests: read\n\njobs:\n",
        "permissions:\n  contents: write\n  pull-requests: read\n\njobs:\n",
        ["quyen_HIEU_LUC_CHI_DOC"]),
    "bo_khai_quyen": (
        "permissions:\n  contents: read\n  pull-requests: read\n\njobs:\n",
        "jobs:\n",
        ["quyen_HIEU_LUC_CHI_DOC"]),
    # B2 — hai đường lách reviewer đo được, cả hai từng cho `18/18 dead=NONE`.
    "job_GHI_DE_quyen_write": (
        "    permissions:\n      contents: read\n      pull-requests: read\n",
        "    permissions:\n      contents: write\n      pull-requests: read\n",
        ["quyen_HIEU_LUC_CHI_DOC"]),
    "them_buoc_KEO_HEAD_PR": (
        "      - name: do nguoi duyet khac nguoi tao PR\n",
        "      - name: lay them ma cua PR\n        run: |\n"
        "          set -eu\n          git fetch origin \"$GITHUB_SHA\"\n"
        "          git checkout FETCH_HEAD\n"
        "      - name: do nguoi duyet khac nguoi tao PR\n",
        ["topology_job_cong"]),
    "doi_env_TL_KHO_sang_kho_FORK": (
        "          TL_KHO: ${{ github.repository }}\n",
        "          TL_KHO: ${{ github.event.pull_request.head.repo.full_name }}\n",
        ["topology_job_cong"]),
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


def _chay(chi=None, m=None, doi_yml=None, doi_yml2=None):
    """Trả (đạt, lý do đỏ). `doi_yml`/`doi_yml2` = (tìm, thay) áp lên bản sao YAML tạm."""
    global YML, YML2
    cu, cu2 = YML, YML2
    try:
        for nhan, doi in (("yml", doi_yml), ("yml2", doi_yml2)):
            if not doi:
                continue
            nguon = cu if nhan == "yml" else cu2
            goc = nguon.read_text(encoding="utf-8")
            tim, thay = doi
            if goc.count(tim) != 1:
                raise AssertionError("MỐC YAML (%s) khớp %d chỗ" % (nhan, goc.count(tim)))
            tam = Path(tempfile.mkdtemp(prefix="tl348-")) / "w.yml"
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

    print(f"\nSỐ LIỆU (đếm bằng máy):\n  ca        : {len(dat)}\n"
          f"  đột biến  : {len(DOT_BIEN_MA) + len(DOT_BIEN_YML) + len(DOT_BIEN_YML2)}")
    print("NỢ  : `ngu-nghia-trigger-chua-do-bang-PR-doi-khang` — tầng (B) đo HÌNH DẠNG tệp,")
    print("      KHÔNG đo hành vi trigger của GitHub. Muốn đo thật phải mở PR đối kháng;")
    print("      bước nghiệm thu của `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` là chỗ làm việc đó.")
    if hong:
        print("TỔNG: %d lỗi" % len(hong))
        for x in hong:
            print("   " + x)
        return 1
    print("TỔNG: ĐẠT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
