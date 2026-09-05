# -*- coding: utf-8 -*-
"""LỚP 3 — năm chốt FAIL-CLOSED của `rasoat-dot-check` (cross-review PR #450: 3×P1 + 2×P2).

Cả năm đều là ca «cổng báo SẠCH trong khi nó chưa đo được gì» — lớp lỗi nguy nhất, vì rc=0 với
`ok:true` là thứ người đọc tin ngay. Mỗi ca dựng lại ĐÚNG bản tái hiện của reviewer, và mỗi ca kèm
ĐỐI CHỨNG dương (đầu vào lành phải vẫn rc=0) để phép đo phân biệt được «chặn đúng» với «chặn tuốt».

  F2 P1  `ket_qua:"error"` được nhận là bằng chứng `not_found`      → enum ĐÓNG
  F3 P1  state sai schema / hàng đợi sai kiểu vẫn cho rc=0          → `_rasoat_state_validate`
  F4 P1  `master/u1.json = {}` cho báo cáo trắng 0 phát hiện        → `_rasoat_unit_shape`
  F5 P2  `--dot` chỉ lọc `q_ingest`, master vẫn nạp cả Đợt khác     → lọc theo `q_units[].dot_id`
  F6 P2  NFC lệch mà vẫn xuất số liệu (trái điều chốt ① tự hứa)     → không đếm, khai KHÔNG KHẢ DỤNG
"""

import contextlib
import io
import json
import tempfile
import unicodedata
from pathlib import Path

TEST_ID = "wp93_rasoat_dot_check_fail_closed"

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


def _dong(ket_qua="not_found", muc=_MUC):
    return {"thoi_diem": "2026-09-05T09:00", "muc_tieu": muc, "khoa_so_hieu": muc,
            "khoa_ten": "ten day du " + muc, "khoa_dinh_danh": "217-2025-ND-CP",
            "ket_qua": ket_qua, "lenh": "tl reg-query + tl locate + tl dedup-check"}


def _state(**kw):
    return dict({"schema": "rasoat_plan.v1", "cap_nhat": "2026-09-05T09:00:00",
                 "q_ingest": [{"so_hieu": _MUC, "trang_thai": "cho_tai", "dot_id": "dot-01"}]}, **kw)


def _dung(root, state, units, rows):
    (root / "master").mkdir(parents=True)
    (root / "rasoat_state.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    for ten, u in units.items():
        (root / "master" / ten).write_text(json.dumps(u, ensure_ascii=False), encoding="utf-8")
    (root / "rasoat_tra_kho.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return root


def _unit(van_ban="Nghị định 217"):
    return {"unit_id": "u1", "phat_hien": [{"key": "P1", "tieu_chi": "T2", "van_ban": van_ban}]}


def run(tl_module):
    with tempfile.TemporaryDirectory(prefix="wp93_") as tmp:
        t = Path(tmp)

        # ĐỐI CHỨNG DƯƠNG — mọi thứ lành: rc=0, và số liệu PHẢI khả dụng.
        rc_lanh, p_lanh = _goi(tl_module, ["rasoat-dot-check", "--in",
                                           str(_dung(t / "lanh", _state(), {"u1.json": _unit()},
                                                     [_dong()])), "--json"])

        # F2 — `error` không phải `not_found`; đối chứng: `found` vẫn bị chặn như cũ.
        rc_err, p_err = _goi(tl_module, ["rasoat-dot-check", "--in",
                                         str(_dung(t / "f2", _state(), {"u1.json": _unit()},
                                                   [_dong("error")])), "--json"])
        rc_found, p_found = _goi(tl_module, ["rasoat-dot-check", "--in",
                                             str(_dung(t / "f2b", _state(), {"u1.json": _unit()},
                                                       [_dong("found")])), "--json"])

        # F3 — state đọc được nhưng SAI khuôn ⇒ lỗi ĐẦU VÀO rc=2, không phải verdict rc=1.
        rc_st, p_st = _goi(tl_module, ["rasoat-dot-check", "--in",
                                       str(_dung(t / "f3", {"schema": "wrong", "cap_nhat": "2026-09-05",
                                                            "q_units": "broken"},
                                                 {"u1.json": _unit()}, [_dong()])), "--json"])

        # F4 — `{}` giải mã sạch nhưng không phải unit_v1/bang_v1 ⇒ không được đếm là 0 phát hiện.
        rc_m, p_m = _goi(tl_module, ["rasoat-dot-check", "--in",
                                     str(_dung(t / "f4", _state(), {"u1.json": {}}, [_dong()])), "--json"])

        # F5 — hai Đợt, hỏi dot-01: chỉ được đếm unit của dot-01.
        # `trang_thai` bắt buộc ở MỌI hàng đợi (§3) — fixture cũ thiếu, validator siết nên ĐỎ.
        # §8: MỖI Đợt phải có bản ghi metadata trong `dot`; thiếu ⇒ `--dot` KHÔNG ĐO ĐƯỢC (rc=2).
        hai_dot = _state(dot=[{"dot_id": "dot-01", "ten": "Đợt 1", "trang_thai": "dang_ra", "mo_luc": "2026-09-01"},
                              {"dot_id": "dot-02", "ten": "Đợt 2", "trang_thai": "chua_mo"}],
                         q_units=[{"unit_id": "u1", "dot_id": "dot-01", "trang_thai": "pending"},
                                  {"unit_id": "u2", "dot_id": "dot-02", "trang_thai": "pending"}])
        d5 = _dung(t / "f5", hai_dot,
                   {"u1.json": _unit(), "u2.json": {"unit_id": "u2", "phat_hien": [
                       {"key": "P9", "tieu_chi": "T9", "van_ban": "thuộc Đợt khác"}]}}, [_dong()])
        rc5, p5 = _goi(tl_module, ["rasoat-dot-check", "--in", str(d5), "--dot", "dot-01", "--json"])
        rc5b, p5b = _goi(tl_module, ["rasoat-dot-check", "--in", str(d5), "--json"])
        # `--dot` không ánh xạ được sang unit nào ⇒ KHÔNG ĐO ĐƯỢC, phải rc=2 chứ không trả một phần.
        rc5c, p5c = _goi(tl_module, ["rasoat-dot-check", "--in", str(d5), "--dot", "dot-99", "--json"])

        # F6 — NFC lệch ⇒ dừng đếm; số liệu phải KHÔNG khả dụng, không phải "0".
        rc6, p6 = _goi(tl_module, ["rasoat-dot-check", "--in",
                                   str(_dung(t / "f6", _state(),
                                             {"u1.json": _unit(unicodedata.normalize("NFD", "Nghị định 217"))},
                                             [_dong()])), "--json"])

    def _dem(p):
        return next((r["gia_tri"] for r in (p.get("chot_3_so_lieu", {}).get("so_lieu") or [])
                     if r["ten"] == "so_phat_hien"), None)

    def _ma(p):
        return {f.get("ma") for f in (p.get("chot_2_tra_kho", {}).get("phat_hien") or [])}

    lanh = (rc_lanh == 0 and p_lanh.get("ok") is True
            and p_lanh["chot_3_so_lieu"].get("kha_dung") is True and _dem(p_lanh) == 1)
    # `error` phải bị bắt ở TẦNG ĐỌC SỔ (dòng hỏng), chứ không lặng lẽ thành bằng chứng not_found
    f2 = (rc_err == 1 and p_err.get("ok") is False
          and any(h.get("ma") == "KET_QUA_NGOAI_ENUM"
                  for h in (p_err.get("chot_2_tra_kho", {}).get("hong") or []))
          and rc_found == 1 and "CO_HIT_MA_VAN_KET_LUAN_THIEU" in _ma(p_found))
    f3 = (rc_st == 2 and p_st.get("ok") is False
          and str(p_st.get("state", {}).get("loi") or "").startswith("STATE_KHONG_HOP_LE"))
    f4 = (rc_m == 1 and p_m.get("ok") is False
          and any(h.get("ma") == "KHUON_KHONG_NHAN_RA" for h in (p_m.get("master_hong") or [])))
    f5 = (rc5 == 0 and _dem(p5) == 1          # chỉ Đợt 01
          and rc5b == 0 and _dem(p5b) == 2    # không truyền --dot thì đếm cả hai — chứng minh fixture có 2
          # `dot-99` không có CẢ bản ghi metadata LẪN unit. Nay lý do nêu ra là cái THIẾU TRƯỚC
          # (`DOT_KHONG_CO_BAN_GHI`) — chính xác hơn bản cũ; chỉ đòi đúng lớp "Đợt không giải được".
          and rc5c == 2 and str(p5c.get("dot_loi") or "").startswith("DOT_KHONG_"))
    f6 = (rc6 == 1 and p6["chot_3_so_lieu"].get("kha_dung") is False
          and not (p6["chot_3_so_lieu"].get("so_lieu") or [])
          and p6["chot_1_nfc"]["ok"] is False)
    return bool(lanh and f2 and f3 and f4 and f5 and f6)
