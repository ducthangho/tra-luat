# -*- coding: utf-8 -*-
"""LỚP 3 — bốn chốt theo LỚP, không theo CA (cross-review lượt 3 trên PR #450: 4×P1 + 1×P2).

VÌ SAO CA NÀY KHÁC `wp93`/`wp94`: ba lượt review liên tiếp ra CÙNG hai hình dạng lỗi, vì mỗi lượt
chỉ vá đúng ca reviewer vừa nêu. `CLAUDE.md` chốt sẵn ngưỡng: *"Đếm hình dạng lỗi, đừng chỉ đếm
lỗi — cùng một hình dạng lặp ba lần trở lên thì câu hỏi đúng là 'có nên làm việc này không', không
phải 'vá thế nào'"*. Nên ca này khẳng định LỚP:

  A  MỌI lỗi tính toàn vẹn của tập đếm đều phải làm số liệu KHÔNG KHẢ DỤNG — kiểm cả BA nguồn
     (NFC lệch · thiếu phiếu/đếm đúp · master hỏng) qua MỘT vị từ. Trước đây mỗi nguồn là một ca
     riêng và nguồn thứ ba vẫn lọt.
  B  validator phải ĐÒI trường, không "kiểm enum khi có giá trị" — `trang_thai` ở mọi hàng đợi, và
     trường bắt buộc THEO TRẠNG THÁI của `dot` (§8). "Kiểm-khi-có" tha đúng cái vắng mặt.
  C  CHẶN OAN cũng là hỏng: dạng `session_claim` ĐÃ NHẢ (`id: null` + `released_at`) có khai ở §7
     và đã được `_rasoat_vong_doi_findings` mã hoá ⇒ phải NHẬN. Nhưng không được nới thành "mọi
     claim rỗng đều qua".
  D  một chốt chỉ sống ở MỘT NHÁNH là chốt vắng mặt ở nhánh kia: coverage đơn vị `done` phải chạy
     cả khi KHÔNG truyền `--dot`.

LƯỢT 4 — cùng bốn LỚP ấy, nhưng đo TÍNH TOÀN. Lượt 3 tôi tuyên bố "vá theo LỚP" mà thực tế chỉ gom
các nguồn ĐANG BIẾT, nên lượt review kế tiếp lại ra đúng ba hình dạng cũ: `dot_loi`/`state_loi` không
nằm trong vị từ A · `.strip()` không áp cho nhánh có điều kiện của B · sổ tra kho bị đòi cả khi không
có kết luận nào (C). Các khẳng định dưới đây kiểm MỌI nguồn của từng lớp, chứ không kiểm nguồn mới nhất.
"""

import contextlib
import io
import json
import tempfile
import unicodedata
from pathlib import Path

TEST_ID = "wp95_rasoat_dot_check_bon_lop"

_MUC = "217/2025/ND-CP"


def _goi(tl_module, args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        try:
            rc = tl_module.main(args)
        except SystemExit as exc:
            rc = int(exc.code or 0)
    try:
        payload = json.loads(out.getvalue())
    except (TypeError, ValueError):
        payload = {}
    return rc, payload


def _dong():
    return {"thoi_diem": "2026-09-05T09:00", "muc_tieu": _MUC, "khoa_so_hieu": _MUC,
            "khoa_ten": "ten day du " + _MUC, "khoa_dinh_danh": "217-2025-ND-CP",
            "ket_qua": "not_found", "lenh": "tl reg-query + tl locate + tl dedup-check"}


def _st(**kw):
    return dict({"schema": "rasoat_plan.v1", "cap_nhat": "2026-09-05T09:00:00",
                 "q_ingest": [{"so_hieu": _MUC, "trang_thai": "cho_tai", "dot_id": "dot-01"}]}, **kw)


def _unit(uid="u1", van_ban="Nghi dinh 217"):
    return {"unit_id": uid, "phat_hien": [{"key": "P1", "tieu_chi": "T2", "van_ban": van_ban}]}


def _dung(root, state, units, them=None):
    (root / "master").mkdir(parents=True)
    (root / "rasoat_state.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    for ten, u in units.items():
        (root / "master" / ten).write_text(json.dumps(u, ensure_ascii=False), encoding="utf-8")
    for ten, raw in (them or {}).items():
        (root / "master" / ten).write_text(raw, encoding="utf-8")
    (root / "rasoat_tra_kho.jsonl").write_text(
        json.dumps(_dong(), ensure_ascii=False) + "\n", encoding="utf-8")
    return root


def run(tl_module):
    with tempfile.TemporaryDirectory(prefix="wp95_") as tmp:
        t = Path(tmp)

        def go(ten, state, units, them=None, co=()):
            return _goi(tl_module, ["rasoat-dot-check", "--in",
                                    str(_dung(t / ten, state, units, them)), "--json"] + list(co))

        # ĐỐI CHỨNG DƯƠNG — thiếu nó thì mọi khẳng định dưới đây thoả được bằng cách CHẶN TUỐT.
        rc_ok, p_ok = go("lanh", _st(), {"u1.json": _unit()})

        # ── LỚP A: ba nguồn lỗi khác nhau, cùng MỘT hệ quả ──
        a_nfc = go("a1", _st(), {"u1.json": _unit(van_ban=unicodedata.normalize("NFD", "Nghị định"))})
        a_thieu = go("a2", _st(q_units=[{"unit_id": "u1", "dot_id": "dot-01", "trang_thai": "done"},
                                        {"unit_id": "u9", "dot_id": "dot-01", "trang_thai": "done"}]),
                     {"u1.json": _unit()})
        a_hong = go("a3", _st(), {"u1.json": _unit()}, them={"x.json": "{ khong phai json"})
        a_dup = go("a4", _st(), {"u1.json": _unit(), "u1.copy.json": _unit()})

        # ── LỚP B: đòi trường, không kiểm-khi-có ──
        b_queue = go("b1", _st(q_ingest=[{"so_hieu": _MUC}]), {"u1.json": _unit()})
        # `dot_id` là KHOÁ NGOẠI (chốt lượt 6) ⇒ bản ghi `dot` phải mang ĐÚNG id mà `q_ingest` trỏ tới.
        b_dot = go("b2", _st(dot=[{"dot_id": "dot-01", "ten": "D1",
                                   "trang_thai": "da_dong_co_gioi_han"}]), {"u1.json": _unit()})
        b_dot_ok = go("b3", _st(dot=[{"dot_id": "dot-01", "ten": "D1",
                                      "trang_thai": "da_dong_co_gioi_han",
                                      "dong_luc": "2026-09-05", "gioi_han_da_biet": [{"muc": "x"}]}]),
                      {"u1.json": _unit()})

        # ── LỚP C: nhận dạng đã khai, nhưng KHÔNG nới quá tay ──
        c_nha = go("c1", _st(session_claim={"id": None, "released_at": "2026-09-05T10:00"}),
                   {"u1.json": _unit()})
        c_rong = go("c2", _st(session_claim={"id": None}), {"u1.json": _unit()})

        # ── LỚP A phải TOÀN: `--dot` sai và state hỏng cũng là lỗi tính toàn vẹn ──
        DOT = [{"dot_id": "dot-01", "ten": "D1", "trang_thai": "dang_ra", "mo_luc": "2026-09-01"}]
        QU = [{"unit_id": "u1", "dot_id": "dot-01", "trang_thai": "pending"}]
        a_dot_sai = go("a5", _st(dot=DOT, q_units=QU), {"u1.json": _unit()}, co=("--dot", "dot-99"))
        a_state = go("a6", {"schema": "sai", "q_units": "hong"}, {"u1.json": _unit()})

        # ── #2 — MỌI khoá máy-so-được phải ràng với mục tiêu (ca thật: tìm 217 mà dừng ở 216) ──
        e_sai = _goi(tl_module, ["rasoat-dot-check", "--in", str(_dung(
            t / "e1", _st(dot=DOT, q_units=QU), {"u1.json": _unit()})), "--json"])
        (t / "e1" / "rasoat_tra_kho.jsonl").write_text(json.dumps(
            dict(_dong(), khoa_so_hieu="216/2025/ND-CP"), ensure_ascii=False) + "\n", encoding="utf-8")
        e_sai = _goi(tl_module, ["rasoat-dot-check", "--in", str(t / "e1"), "--json"])

        # ── #3/#4/#7 — validator: bản ghi `dot`, MỘT `dang_ra`, và trắng-sau-strip ──
        f_khong_bg = go("f1", _st(q_units=[{"unit_id": "u1", "dot_id": "dot-9", "trang_thai": "done"}]),
                        {"u1.json": _unit()}, co=("--dot", "dot-9"))
        f_hai_dangra = go("f2", _st(dot=DOT + [{"dot_id": "b", "ten": "B", "trang_thai": "dang_ra",
                                                "mo_luc": "x"}]), {"u1.json": _unit()})
        f_trang = go("f3", _st(dot=[{"dot_id": "dot-01", "ten": "A", "trang_thai": "da_dong",
                                     "dong_luc": " "}]), {"u1.json": _unit()})
        f_list_rong = go("f4", _st(dot=[{"dot_id": "dot-01", "ten": "A", "dong_luc": "x",
                                         "trang_thai": "da_dong_co_gioi_han",
                                         "gioi_han_da_biet": []}]), {"u1.json": _unit()})

        # ── #6 — không kết luận «kho thiếu» nào thì KHÔNG được đòi sổ (chặn oan) ──
        g = t / "g1"
        (g / "master").mkdir(parents=True)
        (g / "rasoat_state.json").write_text(json.dumps(
            {"schema": "rasoat_plan.v1", "cap_nhat": "2026-09-05"}, ensure_ascii=False), encoding="utf-8")
        (g / "master" / "u1.json").write_text(json.dumps(_unit(), ensure_ascii=False), encoding="utf-8")
        g_no_claim = _goi(tl_module, ["rasoat-dot-check", "--in", str(g), "--json"])

        # ── LƯỢT 5 — cùng bốn LỚP, các nguồn còn lại ──
        # B: mục Q-INGEST không `so_hieu` = không chỉ đích được văn bản nào ⇒ claim rỗng bị lọc lặng
        #    lẽ và cổng không đòi bằng chứng nào. C: dạng đã nhả đòi `id` NULL đúng nghĩa, vì
        #    `_rasoat_vong_doi_findings` so `is None` — nới thành falsy là để hai chốt phán ngược nhau.
        i_qi = go("i1", _st(q_ingest=[{"trang_thai": "cho_tai", "dot_id": "dot-01"}]),
                  {"u1.json": _unit()})
        i_claim_rong = go("i2", _st(session_claim={"id": "", "released_at": "x"}), {"u1.json": _unit()})
        i_claim_null = go("i3", _st(session_claim={"id": None, "released_at": "x"}), {"u1.json": _unit()})
        # A: khuôn LAI (`noi_dung` sai kiểu) từng ném TypeError trần — cổng phải hỏng ĐÚNG KHUÔN.
        # Gọi CÓ BẮT: chính cú traceback là thứ bản vá chặn, nên nó phải thành PHÉP ĐO chứ không
        # được thoát ra ngoài. Không bắt thì đột biến gỡ chốt "chết" bằng exception — ca đích không
        # assert gì cả mà vẫn được tính là giết: đúng định nghĩa TÍN DỤNG GIẢ (đã đo, không phải lo xa).
        i_lai_no = None
        try:
            i_lai = go("i4", _st(), {"u1.json": {"unit_id": "u1", "phat_hien": [], "noi_dung": "bad"}})
        except BaseException as _e:            # noqa: BLE001 — traceback CHÍNH LÀ ca hỏng cần đo
            i_lai, i_lai_no = (None, {}), type(_e).__name__
        # Sổ APPEND-ONLY: dòng CŨ tra nhầm văn bản mang `found` không được khoá vĩnh viễn kết luận;
        # nếu không, cách duy nhất đi tiếp là XOÁ lịch sử kiểm toán.
        _j = _dung(t / "i5", _st(), {"u1.json": _unit()})
        (_j / "rasoat_tra_kho.jsonl").write_text(
            json.dumps({"thoi_diem": "t", "muc_tieu": _MUC, "khoa_so_hieu": "216/2025/ND-CP",
                        "khoa_dinh_danh": "216-2025-ND-CP", "ket_qua": "found", "lenh": "x"},
                       ensure_ascii=False)
            + "\n" + json.dumps(_dong(), ensure_ascii=False) + "\n", encoding="utf-8")
        i_append = _goi(tl_module, ["rasoat-dot-check", "--in", str(_j), "--json"])

        # ── LƯỢT 6 — ba nguồn còn lại, trong đó MỘT là hồi quy do chính bản vá lượt 5 gây ra ──
        # Lượt 5 lọc dòng theo kiểu GIỮ-LẠI-KHI-KHỚP, nên dòng chỉ khai `khoa_ten` (không có khoá
        # máy-so-được nào) bị loại — kể cả khi mang `found` ⇒ cổng báo SẠCH cho văn bản ĐÃ TÌM THẤY.
        # Luật đúng là LOẠI-TRỪ: chỉ bỏ dòng NÓI RÕ nó trỏ văn bản khác.
        _k = _dung(t / "k1", _st(), {"u1.json": _unit()})
        (_k / "rasoat_tra_kho.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in (
            {"thoi_diem": "t", "muc_tieu": _MUC, "khoa_ten": "ten day du", "ket_qua": "found", "lenh": "tl locate"},
            {"thoi_diem": "t", "muc_tieu": _MUC, "khoa_so_hieu": _MUC, "ket_qua": "not_found", "lenh": "x"},
            {"thoi_diem": "t", "muc_tieu": _MUC, "khoa_dinh_danh": "217-2025-ND-CP",
             "ket_qua": "not_found", "lenh": "x"})), encoding="utf-8")
        k_ten_found = _goi(tl_module, ["rasoat-dot-check", "--in", str(_k), "--json"])
        # `dot_id` là KHOÁ NGOẠI: trỏ tới Đợt không khai thì mục bị lọc ra rồi Đợt đóng khi nó còn treo.
        k_mo_coi = go("k2", _st(dot=DOT, q_ingest=[{"so_hieu": _MUC, "trang_thai": "cho_tai",
                                                    "dot_id": "dot-typo"}]), {"u1.json": _unit()})
        # `.get("id")` trả None cho CẢ khoá vắng mặt ⇒ claim ghi dở bị coi là đã nhả.
        k_thieu_id = go("k3", _st(session_claim={"released_at": "x"}), {"u1.json": _unit()})

        # ── LƯỢT 7 — ba nguồn còn lại, hai trong số đó do chính bản vá lượt 6 gây ra ──
        # `da_tra` (theo TRƯỜNG) và `_khop` (theo DÒNG) từng là HAI luật xét khác nhau: dòng khai
        # đúng `khoa_ten` + `found` nhưng gõ nhầm `khoa_so_hieu` được tính KHOÁ mà không tính KẾT
        # QUẢ ⇒ báo sạch cho văn bản đã tìm thấy. Nay MỘT quyết định tư cách cho cả hai.
        _m = _dung(t / "m1", _st(), {"u1.json": _unit()})
        (_m / "rasoat_tra_kho.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in (
            {"thoi_diem": "t", "muc_tieu": _MUC, "khoa_ten": "ten day du",
             "khoa_so_hieu": "216/2025/ND-CP", "ket_qua": "found", "lenh": "x"},
            {"thoi_diem": "t", "muc_tieu": _MUC, "khoa_so_hieu": _MUC, "ket_qua": "not_found", "lenh": "x"},
            {"thoi_diem": "t", "muc_tieu": _MUC, "khoa_dinh_danh": "217-2025-ND-CP",
             "ket_qua": "not_found", "lenh": "x"})), encoding="utf-8")
        m_lai = _goi(tl_module, ["rasoat-dot-check", "--in", str(_m), "--json"])
        # Validator KHÔNG được tự crash trên đầu vào hỏng — nếu crash thì nó không còn là validator.
        m_dot_int_no = None
        try:
            m_dot_int = go("m2", {"schema": "rasoat_plan.v1", "cap_nhat": "x", "dot": 1},
                           {"u1.json": _unit()})
        except BaseException as _e:        # noqa: BLE001 — traceback CHÍNH LÀ ca hỏng cần ĐO
            m_dot_int, m_dot_int_no = (None, {}), type(_e).__name__
        # TƯƠNG THÍCH: chốt `so_hieu` chỉ áp cho trạng thái SINH RA CLAIM. Kho có sẵn fixture
        # đóng-sạch dùng `{"trang_thai":"flipped"}` không kèm `so_hieu` (tl_selftest.py) — đòi vô
        # điều kiện là làm mọi `state-put` sau đó ĐỎ, tức chặn oan trên dữ liệu hợp lệ có thật.
        m_flipped = go("m3", _st(q_ingest=[{"trang_thai": "flipped"}]), {"u1.json": _unit()})
        m_chotai = go("m4", _st(q_ingest=[{"trang_thai": "cho_tai"}]), {"u1.json": _unit()})

        # ── LƯỢT 8 — BA trạng thái cho một dòng sổ, không phải hai (lần thứ ba luật này bị sửa) ──
        # `khop` (không khoá máy nào lệch) · `khac` (MỌI khoá đều trỏ nơi khác ⇒ dòng lịch sử, bỏ qua)
        # · `mau_thuan` (vừa khớp vừa lệch ⇒ SỔ HỎNG, là PHÁT HIỆN). Bản trước gộp hai loại sau làm
        # một nên NUỐT bằng chứng `found` của dòng lai — nuốt bằng chứng tệ hơn đọc nhầm nó.
        def _so(ten, rows):
            _r = _dung(t / ten, _st(), {"u1.json": _unit()})
            (_r / "rasoat_tra_kho.jsonl").write_text(
                "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
            return _goi(tl_module, ["rasoat-dot-check", "--in", str(_r), "--json"])
        _sh = {"thoi_diem": "t", "muc_tieu": _MUC, "khoa_so_hieu": _MUC, "ket_qua": "not_found", "lenh": "x"}
        _dd = {"thoi_diem": "t", "muc_tieu": _MUC, "khoa_dinh_danh": "217-2025-ND-CP",
               "ket_qua": "not_found", "lenh": "x"}
        _ten = {"thoi_diem": "t", "muc_tieu": _MUC, "khoa_ten": "ten day du",
                "ket_qua": "not_found", "lenh": "x"}
        n_mau_thuan = _so("n1", [dict(_sh, khoa_dinh_danh="216-2025-ND-CP", ket_qua="found"),
                                 _sh, _dd, _ten])
        n_lich_su = _so("n2", [{"thoi_diem": "t", "muc_tieu": _MUC, "khoa_so_hieu": "216/2025/ND-CP",
                                "khoa_dinh_danh": "216-2025-ND-CP", "ket_qua": "found", "lenh": "x"},
                               _sh, _dd, _ten])
        n_sach = _so("n3", [_sh, _dd, _ten])
        n_found = _so("n4", [dict(_sh, ket_qua="found"), _dd, _ten])
        # LƯỢT 9 — `khac` chỉ đúng khi dòng CHẮC CHẮN nói về văn bản khác. Có `khoa_ten` (tra theo
        # TÊN, không quy về định danh được) thì KHÔNG chắc: phép tra ấy có thể đã trúng chính mục
        # tiêu ⇒ drop nó là nuốt một `found`. Không chắc ⇒ MÂU THUẪN (fail-closed).
        n_ten_lech = _so("n5", [{"thoi_diem": "t", "muc_tieu": _MUC, "khoa_ten": "ten",
                                 "khoa_so_hieu": "216/2025/ND-CP", "ket_qua": "found", "lenh": "x"},
                                _sh, _dd, _ten])
        # `dot_id` trỏ Đợt CHƯA KHAI: là PHÁT HIỆN lúc đóng (rc=1), KHÔNG phải lỗi state (rc=2) —
        # đặc tả §2 có ví dụ CHUẨN xếp việc cho Đợt sắp mở, nên bác ở validator là chặn oan.
        n_orphan = go("n6", _st(dot=DOT, q_ingest=[{"so_hieu": _MUC, "trang_thai": "cho_tai",
                                                    "dot_id": "dot-typo"}]), {"u1.json": _unit()})
        n_tuong_lai = go("n7", _st(dot=DOT,
                                   q_units=[{"unit_id": "u1", "dot_id": "dot-01", "trang_thai": "pending"},
                                            {"unit_id": "u9", "dot_id": "dot-02", "trang_thai": "pending"}]),
                         {"u1.json": _unit()})

        # ── LƯỢT 10 — năm nguồn của lượt review thứ 9 ──
        _FULL = {"thoi_diem": "t", "muc_tieu": _MUC, "khoa_so_hieu": _MUC, "khoa_ten": "ten day du",
                 "khoa_dinh_danh": "217-2025-ND-CP", "ket_qua": "not_found", "lenh": "x"}
        def _sok(ten, rows, st=None, co=()):
            _r = _dung(t / ten, st or _st(), {"u1.json": _unit()})
            (_r / "rasoat_tra_kho.jsonl").write_text(
                "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
            return _goi(tl_module, ["rasoat-dot-check", "--in", str(_r), "--json"] + list(co)), _r
        # `str([""])` là `"['']"` — KHÁC RỖNG. `str()` nhận MỌI thứ nên nó là phép ÉP KIỂU đội lốt
        # phép KIỂM: khoá `[""]`  từng được tính là "đã tra bằng tên".
        o_ten_list, _ = _sok("o1", [dict(_FULL, khoa_ten=[""])])
        o_ten_str, _ = _sok("o2", [_FULL])
        # `--strict` gộp rc=1 vào rc=2 ⇒ quyết theo rc thì đường đóng HẠN CHẾ biến mất. Phải quyết
        # theo `loai_verdict`: đã đo được thì vẫn đóng hạn chế được, dù rc=2 vì `--strict`.
        o_strict, _ = _sok("o3", [dict(_FULL, khoa_ten=None, khoa_dinh_danh=None)], co=("--strict",))
        o_hong, _ = _sok("o4", [_FULL], st=_st(dot="broken"), co=("--strict",))
        # Hỏi MỘT Đợt thì mục của Đợt KHÁC không được làm nhiễu; soi cả hồ sơ thì vẫn phải nêu.
        _QI = [{"so_hieu": _MUC, "trang_thai": "cho_tai", "dot_id": "dot-01"},
               {"so_hieu": "9/2026/ND-CP", "trang_thai": "cho_tai", "dot_id": "dot-02"}]
        _STD = _st(dot=DOT, q_units=[{"unit_id": "u1", "dot_id": "dot-01", "trang_thai": "pending"}],
                   q_ingest=_QI)
        o_dot, _ = _sok("o5", [_FULL], st=_STD, co=("--dot", "dot-01"))
        o_ca_ho_so, _ = _sok("o6", [_FULL], st=_STD)
        # Sổ tái lập phải nhận diện TẬP NGUỒN, không chỉ thư mục.
        o_dem, _r6 = _sok("o7", [_FULL])
        # `--out` trỏ vào `--in` phá chính lời khai READ-ONLY của lệnh.
        o_out = _goi(tl_module, ["rasoat-dot-check", "--in", str(_r6), "--json",
                                 "--out", str(_r6 / "rasoat_state.json")])

        # ── #8 — `--out` dưới thư mục cha CHƯA TỒN TẠI phải ghi được (writer nguyên tử) ──
        _out = t / "chua" / "co" / "kq.json"
        h_out = _goi(tl_module, ["rasoat-dot-check", "--in", str(t / "lanh"), "--json", "--out", str(_out)])
        h_out_ok = _out.exists()

        # ── LỚP D: coverage chạy cả khi KHÔNG có `--dot` (ca a_thieu ở trên đã bỏ `--dot`) ──
        d_co_dot = go("d1", _st(dot=DOT,
                                q_units=[{"unit_id": "u1", "dot_id": "dot-01", "trang_thai": "done"},
                                         {"unit_id": "u9", "dot_id": "dot-01", "trang_thai": "done"}]),
                      {"u1.json": _unit()}, co=("--dot", "dot-01"))

    def _kd(p):
        return p.get("chot_3_so_lieu", {}).get("kha_dung")

    def _rong(p):
        return not (p.get("chot_3_so_lieu", {}).get("so_lieu") or [])

    lanh = rc_ok == 0 and p_ok.get("ok") is True and _kd(p_ok) is True and not _rong(p_ok)
    # A — cả BỐN đường vào đều phải cho cùng hệ quả; đây là điều "vá từng ca" KHÔNG bảo đảm được
    lop_a = all(rc == 1 and _kd(p) is False and _rong(p)
                and str(p["chot_3_so_lieu"].get("ly_do") or "").startswith("KHONG_DO_DUOC")
                for rc, p in (a_nfc, a_thieu, a_hong, a_dup))
    lop_b = (b_queue[0] == 2 and "Q_INGEST[0]_THIEU_TRANG_THAI" in str(b_queue[1].get("state", {}).get("loi") or "")
             and b_dot[0] == 2 and "GIOI_HAN_DA_BIET" in str(b_dot[1].get("state", {}).get("loi") or "")
             and b_dot_ok[0] == 0 and b_dot_ok[1].get("ok") is True)   # đối chứng dương của LỚP B
    lop_c = (c_nha[0] == 0 and c_nha[1].get("ok") is True                      # dạng đã nhả ⇒ NHẬN
             and c_rong[0] == 2                                                # rỗng mà không nhả ⇒ ĐỎ
             and "SESSION_CLAIM_THIEU_ID" in str(c_rong[1].get("state", {}).get("loi") or ""))
    # D — cùng một hồ sơ, có `--dot` và không `--dot` phải cho CÙNG phán quyết coverage
    lop_d = (d_co_dot[0] == 1 and a_thieu[0] == 1
             and any(x.get("ma") == "DON_VI_DONE_THIEU_PHIEU_MASTER" and x.get("unit_id") == "u9"
                     for x in (d_co_dot[1].get("thieu_payload") or []))
             and any(x.get("ma") == "DON_VI_DONE_THIEU_PHIEU_MASTER" and x.get("unit_id") == "u9"
                     for x in (a_thieu[1].get("thieu_payload") or [])))
    # LỚP A TOÀN — SÁU nguồn lỗi khác nhau, MỘT hệ quả. Đây là điều "vá từng ca" không bảo đảm.
    lop_a_toan = all(_kd(p) is False and _rong(p) for _, p in (a_dot_sai, a_state))
    # #2 — khoá số hiệu lệch ⇒ không được tính là đã tra, và phải NÊU giá trị sai
    # `khoa_so_hieu` lệch trong khi `khoa_dinh_danh` khớp ⇒ dòng TỰ MÂU THUẪN (phân loại lượt 8),
    # và phải NÊU ĐÍCH DANH khoá sai — không được gộp chung thành "thiếu khoá".
    khoa_toan = (e_sai[0] == 1 and any(
        f.get("ma") == "DONG_TU_MAU_THUAN"
        and any(x.get("khoa") == "khoa_so_hieu" for d in (f.get("dong") or [])
                for x in (d.get("khoa_lech") or []))
        for f in (e_sai[1].get("chot_2_tra_kho", {}).get("phat_hien") or [])))
    val_toan = (f_khong_bg[0] == 2 and "DOT_KHONG_CO_BAN_GHI" in str(f_khong_bg[1].get("dot_loi") or "")
                and f_hai_dangra[0] == 2
                and "DOT_NHIEU_HON_MOT_DANG_RA" in str(f_hai_dangra[1].get("state", {}).get("loi") or "")
                # trắng-sau-strip VÀ list rỗng phải cùng bị bắt — hai dạng "có mà không dùng được"
                and f_trang[0] == 2 and f_list_rong[0] == 2)
    khong_chan_oan = g_no_claim[0] == 0 and g_no_claim[1].get("ok") is True
    out_toan = h_out[0] == 0 and h_out_ok
    luot5 = (i_qi[0] == 2 and "Q_INGEST[0]_THIEU_SO_HIEU" in str(i_qi[1].get("state", {}).get("loi") or "")
             and i_claim_rong[0] == 2 and i_claim_null[0] == 0      # đối chứng: `id: None` phải QUA
             and i_lai_no is None                                   # KHÔNG được ném ra ngoài
             and i_lai[0] == 1 and i_lai[1].get("ok") is False      # hỏng ĐÚNG KHUÔN, không traceback
             and any(x.get("ma") == "TRUONG_SAI_KIEU" for x in (i_lai[1].get("master_hong") or []))
             and i_append[0] == 0 and i_append[1].get("ok") is True)
    luot6 = (k_ten_found[0] == 1 and k_ten_found[1].get("ok") is False
             and any(f.get("ma") == "CO_HIT_MA_VAN_KET_LUAN_THIEU"
                     for f in (k_ten_found[1].get("chot_2_tra_kho", {}).get("phat_hien") or []))
             # Chốt `dot_id` đã CHUYỂN CHỖ: đặc tả §2 cho phép trỏ Đợt sắp mở, nên bác ở validator là
             # chặn oan; nay là PHÁT HIỆN lúc đóng (rc=1) — đúng chỗ mới đủ ngữ cảnh để phán.
             and k_mo_coi[0] == 1
             and any(x.get("ma") == "DOT_ID_CHUA_KHAI" for x in (k_mo_coi[1].get("thieu_payload") or []))
             and k_thieu_id[0] == 2
             and i_claim_null[0] == 0)      # đối chứng dương giữ nguyên: `id: None` TƯỜNG MINH vẫn qua
    luot7 = (m_lai[0] == 1 and m_lai[1].get("ok") is False          # dòng LAI không được cho qua
             and m_dot_int_no is None                                # KHÔNG được ném ra ngoài
             and m_dot_int[0] == 2                                   # hỏng ĐÚNG KHUÔN, không traceback
             and "DOT_KHONG_PHAI_MANG" in str(m_dot_int[1].get("state", {}).get("loi") or "")
             and m_flipped[0] == 0 and m_flipped[1].get("ok") is True    # tương thích: PHẢI qua
             and m_chotai[0] == 2)                                       # còn defect thật: vẫn chặn
    def _ma(r):
        return {f.get("ma") for f in (r[1].get("chot_2_tra_kho", {}).get("phat_hien") or [])}
    luot8 = (n_mau_thuan[0] == 1 and "DONG_TU_MAU_THUAN" in _ma(n_mau_thuan)   # KHÔNG được nuốt
             and n_lich_su[0] == 0 and n_lich_su[1].get("ok") is True          # append-only vẫn sửa được
             and n_sach[0] == 0 and n_sach[1].get("ok") is True                # đối chứng dương
             and n_found[0] == 1 and "CO_HIT_MA_VAN_KET_LUAN_THIEU" in _ma(n_found)   # chốt gốc còn
             and n_ten_lech[0] == 1 and "DONG_TU_MAU_THUAN" in _ma(n_ten_lech)
             and n_orphan[0] == 1                       # phát hiện, KHÔNG phải lỗi đầu vào
             and any(x.get("ma") == "DOT_ID_CHUA_KHAI" for x in (n_orphan[1].get("thieu_payload") or []))
             and n_tuong_lai[0] == 0 and n_tuong_lai[1].get("ok") is True)  # ví dụ CHUẨN của §2 phải QUA
    _so1 = (o_dem[1].get("chot_3_so_lieu", {}).get("so_lieu") or [{}])[0].get("dem_tren") or ""
    luot10 = (o_ten_list[0] == 1 and o_ten_str[0] == 0          # khoá phải là CHUỖI; đối chứng dương
              and o_strict[1].get("loai_verdict") == "do_duoc"
              and o_strict[1].get("co_the_dong_han_che") is True   # rc=2 vì --strict, VẪN đóng hạn chế được
              and o_hong[1].get("loai_verdict") == "khong_do_duoc"
              and o_hong[1].get("co_the_dong_han_che") is False    # state hỏng ⇒ chặn CỨNG
              and o_dot[0] == 0 and o_dot[1].get("ok") is True     # Đợt khác không làm nhiễu
              and any(x.get("ma") == "DOT_ID_CHUA_KHAI"            # …nhưng soi cả hồ sơ thì vẫn nêu
                      for x in (o_ca_ho_so[1].get("thieu_payload") or []))
              and "sha256=" in _so1 and "phiếu" in _so1            # sổ nhận diện được TẬP NGUỒN
              and o_out[0] == 2 and "OUT_TRONG_IN" in str(o_out[1].get("out_loi") or ""))
    return bool(lanh and lop_a and lop_b and lop_c and lop_d
                and lop_a_toan and khoa_toan and val_toan and khong_chan_oan and out_toan and luot5 and luot6 and luot7 and luot8 and luot10)
