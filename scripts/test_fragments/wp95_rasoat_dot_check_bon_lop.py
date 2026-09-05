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

        # ── LỚP D: coverage chạy cả khi KHÔNG có `--dot` (ca a_thieu ở trên đã bỏ `--dot`) ──
        d_co_dot = go("d1", _st(q_units=[{"unit_id": "u1", "dot_id": "dot-01", "trang_thai": "done"},
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
    return bool(lanh and lop_a and lop_b and lop_c and lop_d)
