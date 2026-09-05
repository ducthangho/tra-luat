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
        b_dot = go("b2", _st(dot=[{"dot_id": "d1", "ten": "D1",
                                   "trang_thai": "da_dong_co_gioi_han"}]), {"u1.json": _unit()})
        b_dot_ok = go("b3", _st(dot=[{"dot_id": "d1", "ten": "D1", "trang_thai": "da_dong_co_gioi_han",
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
        f_trang = go("f3", _st(dot=[{"dot_id": "a", "ten": "A", "trang_thai": "da_dong",
                                     "dong_luc": " "}]), {"u1.json": _unit()})
        f_list_rong = go("f4", _st(dot=[{"dot_id": "a", "ten": "A", "dong_luc": "x",
                                         "trang_thai": "da_dong_co_gioi_han",
                                         "gioi_han_da_biet": []}]), {"u1.json": _unit()})

        # ── #6 — không kết luận «kho thiếu» nào thì KHÔNG được đòi sổ (chặn oan) ──
        g = t / "g1"
        (g / "master").mkdir(parents=True)
        (g / "rasoat_state.json").write_text(json.dumps(
            {"schema": "rasoat_plan.v1", "cap_nhat": "2026-09-05"}, ensure_ascii=False), encoding="utf-8")
        (g / "master" / "u1.json").write_text(json.dumps(_unit(), ensure_ascii=False), encoding="utf-8")
        g_no_claim = _goi(tl_module, ["rasoat-dot-check", "--in", str(g), "--json"])

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
    khoa_toan = (e_sai[0] == 1 and any(
        f.get("ma") == "THIEU_KHOA" and "khoa_so_hieu" in (f.get("khoa_thieu") or [])
        and any(x.get("khoa") == "khoa_so_hieu" for x in (f.get("khoa_dinh_danh_lech") or []))
        for f in (e_sai[1].get("chot_2_tra_kho", {}).get("phat_hien") or [])))
    val_toan = (f_khong_bg[0] == 2 and "DOT_KHONG_CO_BAN_GHI" in str(f_khong_bg[1].get("dot_loi") or "")
                and f_hai_dangra[0] == 2
                and "DOT_NHIEU_HON_MOT_DANG_RA" in str(f_hai_dangra[1].get("state", {}).get("loi") or "")
                # trắng-sau-strip VÀ list rỗng phải cùng bị bắt — hai dạng "có mà không dùng được"
                and f_trang[0] == 2 and f_list_rong[0] == 2)
    khong_chan_oan = g_no_claim[0] == 0 and g_no_claim[1].get("ok") is True
    out_toan = h_out[0] == 0 and h_out_ok
    return bool(lanh and lop_a and lop_b and lop_c and lop_d
                and lop_a_toan and khoa_toan and val_toan and khong_chan_oan and out_toan)
