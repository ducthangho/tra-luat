# -*- coding: utf-8 -*-
"""LỚP 3 — BÀI KIỂM TỰ CHỨNG MINH: dựng lại ĐÚNG ba ca tra sót đã xảy ra và chứng minh cổng chặn cả ba.

Ba ca (hồ sơ ATVSLĐ, 7 Đợt kế hoạch / 11 lượt thực tế) — mỗi ca kết luận "kho thiếu" sau khi tra MỘT khoá:
  · ILO 81            — kho lưu `ILO-081`, tra chuỗi "ILO 81" trượt;
  · NĐ 217/2025       — dừng ngay sau khi thấy NĐ 216/2025;
  · NQ 66.17/2026     — lọc máy móc theo loại văn bản, số hiệu có phần thập phân bị bỏ.

Đo BA vế, thiếu vế nào cũng ĐỎ:
  (a) CHẶN — cả ba ca đều bị nêu đích danh, mỗi ca kèm khoá còn thiếu;
  (b) KHÔNG BÁO GIẢ — cùng ba ca nhưng đã tra đủ 3 khoá và đều `not_found` ⇒ cổng SẠCH;
  (c) ĐỊNH DANH — log ghi `ILO-081` thoả kết luận viết `ILO 81` (nếu không thì cổng chỉ so chuỗi thô,
      tức chưa hề sửa được nguyên nhân gốc), và một khoá `found` ⇒ chặn kết luận "thiếu".
"""

import contextlib
import io
import json
import tempfile
from pathlib import Path

TEST_ID = "wp92_rasoat_dot_check_chan_3_ca_tra_sot"

_BA_CA = ("ILO 81", "217/2025/NĐ-CP", "66.17/2026/NQ-CP")
_DINH_DANH_MONG_DOI = {"ILO 81": "ILO-081", "217/2025/NĐ-CP": "217-2025-ND-CP",
                       "66.17/2026/NQ-CP": "66.17-2026-NQ-CP"}


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


def _dung(root: Path, dong_log):
    (root / "master").mkdir(parents=True)
    (root / "rasoat_state.json").write_text(json.dumps(
        {"schema": "rasoat_plan.v1", "cap_nhat": "2026-09-03T17:00:00",
         "q_ingest": [{"so_hieu": sh, "trang_thai": "cho_tai", "dot_id": "dot-05"} for sh in _BA_CA]},
        ensure_ascii=False), encoding="utf-8")
    (root / "master" / "u1.json").write_text(json.dumps(
        {"unit_id": "u1", "phat_hien": []}, ensure_ascii=False), encoding="utf-8")
    (root / "rasoat_tra_kho.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in dong_log), encoding="utf-8")


def _mot_khoa(muc_tieu):
    return {"thoi_diem": "2026-09-03T09:00", "muc_tieu": muc_tieu, "khoa_so_hieu": muc_tieu,
            "ket_qua": "not_found", "lenh": "tl reg-query --sohieu " + muc_tieu}


def _du_khoa(muc_tieu, dinh_danh, ket_qua="not_found"):
    return {"thoi_diem": "2026-09-03T09:00", "muc_tieu": muc_tieu, "khoa_so_hieu": muc_tieu,
            "khoa_ten": "ten day du cua " + muc_tieu, "khoa_dinh_danh": dinh_danh,
            "ket_qua": ket_qua, "lenh": "tl locate + tl reg-query + tl dedup-check"}


def run(tl_module):
    with tempfile.TemporaryDirectory(prefix="wp92_tra_sot_") as tmp:
        # (a) đúng cách lượt rà đã làm: một khoá
        a = Path(tmp) / "mot_khoa"
        _dung(a, [_mot_khoa(sh) for sh in _BA_CA])
        rc_a, p_a = _goi(tl_module, ["rasoat-dot-check", "--in", str(a), "--json"])

        # (b) đã tra đủ ba khoá, đều not_found → kết luận "thiếu" HỢP LỆ
        b = Path(tmp) / "du_khoa"
        _dung(b, [_du_khoa(sh, _DINH_DANH_MONG_DOI[sh]) for sh in _BA_CA])
        rc_b, p_b = _goi(tl_module, ["rasoat-dot-check", "--in", str(b), "--json"])

        # (c1) log ghi theo ĐỊNH DANH kho (`ILO-081`) trong khi kết luận viết `ILO 81`
        c = Path(tmp) / "dinh_danh"
        _dung(c, [_du_khoa("ILO-081", "ILO-081")]
              + [_du_khoa(sh, _DINH_DANH_MONG_DOI[sh]) for sh in _BA_CA[1:]])
        rc_c, p_c = _goi(tl_module, ["rasoat-dot-check", "--in", str(c), "--json"])

        # (c2) một khoá trả `found` mà vẫn kết luận thiếu → phải chặn
        d = Path(tmp) / "co_hit"
        _dung(d, [_du_khoa("ILO 81", "ILO-081", ket_qua="found")]
              + [_du_khoa(sh, _DINH_DANH_MONG_DOI[sh]) for sh in _BA_CA[1:]])
        rc_d, p_d = _goi(tl_module, ["rasoat-dot-check", "--in", str(d), "--json"])

    ph_a = {f["muc_tieu"]: f for f in (p_a.get("chot_2_tra_kho", {}).get("phat_hien") or [])}
    chan_du_ba = (set(ph_a) == set(_BA_CA)
                  and all(ph_a[sh]["ma"] == "THIEU_KHOA" for sh in _BA_CA)
                  and all(ph_a[sh]["khoa_thieu"] == ["khoa_ten", "khoa_dinh_danh"] for sh in _BA_CA)
                  and all(ph_a[sh]["dinh_danh"] == _DINH_DANH_MONG_DOI[sh] for sh in _BA_CA)
                  and rc_a == 1)
    khong_bao_gia = rc_b == 0 and p_b.get("ok") is True and not (
        p_b.get("chot_2_tra_kho", {}).get("phat_hien") or [])
    dinh_danh_khop = rc_c == 0 and p_c.get("ok") is True
    chan_co_hit = (rc_d == 1
                   and any(f["ma"] == "CO_HIT_MA_VAN_KET_LUAN_THIEU"
                           for f in (p_d.get("chot_2_tra_kho", {}).get("phat_hien") or [])))
    return bool(chan_du_ba and khong_bao_gia and dinh_danh_khop and chan_co_hit)
