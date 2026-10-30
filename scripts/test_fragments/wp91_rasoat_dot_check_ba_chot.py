# -*- coding: utf-8 -*-
"""LỚP 3 — ba chốt của `rasoat-dot-check` chạy qua CLI công khai (không gọi hàm nội bộ).

Đo đúng ba mệnh đề, mỗi mệnh đề kèm PHẢN CHỨNG để phép đo phân biệt được:
  ① NFC — nguồn chưa chuẩn hoá ⇒ nêu ĐÍCH DANH dòng, KHÔNG âm thầm chuẩn hoá rồi đếm.
  ② rc — sạch rc=0 · có phát hiện rc=1 (VERDICT dữ liệu) · `--strict` cùng đầu vào rc=2.
  ③ số liệu tái lập — mỗi con số mang `dem_tren` + `tieu_chi` + `ngay_chot`; thiếu ngày chốt ⇒ phát hiện.
"""

import contextlib
import io
import json
import tempfile
import unicodedata
from pathlib import Path

TEST_ID = "wp91_rasoat_dot_check_ba_chot"


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


def _dung_ho_so(root: Path, *, nfc_lech=False, ngay_chot=True, du_khoa=True):
    (root / "master").mkdir(parents=True)
    # `dot` phải đủ BA trường bắt buộc (`RASOAT_PLAN_SCHEMA.md` §8). Fixture bản đầu chỉ khai
    # `dot_id`; ca `wp94`/H1 siết validator đúng theo đặc tả nên nó ĐỎ — fixture sai, không phải
    # bản vá sai. Giữ ghi chú để lần sau không ai "sửa cho xanh" bằng cách nới validator.
    state = {"schema": "rasoat_plan.v1", "ho_so_id": "hs",
             "dot": [{"dot_id": "dot-01", "ten": "Đợt 1", "trang_thai": "dang_ra",
                      "mo_luc": "2026-09-01T08:00:00"}],
             "q_ingest": [{"so_hieu": "217/2025/ND-CP", "trang_thai": "cho_tai", "dot_id": "dot-01"}]}
    if ngay_chot:
        state["cap_nhat"] = "2026-09-03T17:00:00"
    (root / "rasoat_state.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    ten = "Nghị định 217"
    if nfc_lech:                      # NFD: 'ị' tách thành i + dấu tổ hợp
        ten = unicodedata.normalize("NFD", ten)
    (root / "master" / "u1.json").write_text(json.dumps(
        {"unit_id": "u1", "phat_hien": [{"key": "P1", "tieu_chi": "T2", "van_ban": ten}]},
        ensure_ascii=False), encoding="utf-8")
    khoa = {"khoa_so_hieu": "217/2025/ND-CP"}
    if du_khoa:
        khoa.update({"khoa_ten": "Nghi dinh 217/2025", "khoa_dinh_danh": "217-2025-ND-CP"})
    dong = dict({"thoi_diem": "2026-09-03T09:00", "muc_tieu": "217/2025/ND-CP",
                 "ket_qua": "not_found", "lenh": "tl reg-query --sohieu 217/2025/ND-CP"}, **khoa)
    (root / "rasoat_tra_kho.jsonl").write_text(json.dumps(dong, ensure_ascii=False) + "\n", encoding="utf-8")


def run(tl_module):
    with tempfile.TemporaryDirectory(prefix="wp91_dot_") as tmp:
        sach = Path(tmp) / "sach"
        _dung_ho_so(sach)
        rc_sach, p_sach = _goi(tl_module, ["rasoat-dot-check", "--in", str(sach), "--json"])
        rc_strict, _ = _goi(tl_module, ["rasoat-dot-check", "--in", str(sach), "--strict", "--json"])

        lech = Path(tmp) / "lech"
        _dung_ho_so(lech, nfc_lech=True)
        rc_lech, p_lech = _goi(tl_module, ["rasoat-dot-check", "--in", str(lech), "--json"])
        rc_lech_strict, _ = _goi(tl_module, ["rasoat-dot-check", "--in", str(lech), "--strict", "--json"])

        thieu_ngay = Path(tmp) / "thieu_ngay"
        _dung_ho_so(thieu_ngay, ngay_chot=False)
        rc_ngay, p_ngay = _goi(tl_module, ["rasoat-dot-check", "--in", str(thieu_ngay), "--json"])

        rc_khong_co, p_khong_co = _goi(tl_module, ["rasoat-dot-check", "--in", str(Path(tmp) / "khong-ton-tai"),
                                                   "--json"])

    # ① sạch: rc=0 kể cả --strict (phản chứng: cùng đầu vào mà --strict đổi verdict thì cổng vô nghĩa)
    ok1 = (rc_sach == 0 and rc_strict == 0 and p_sach.get("ok") is True
           and p_sach["chot_1_nfc"]["ok"] is True and p_sach["chot_2_tra_kho"]["ok"] is True)
    # ② NFC lệch: rc=1 (verdict) → --strict rc=2; phải NÊU ĐÍCH DANH file + dòng
    _l = p_lech.get("chot_1_nfc", {}).get("lech") or []
    ok2 = (rc_lech == 1 and rc_lech_strict == 2 and _l
           and _l[0]["ma"] == "CHUA_CHUAN_HOA_NFC" and _l[0]["dong"]
           and _l[0]["file"].endswith(".json"))
    # ③ số liệu: mỗi dòng đủ ba trường truy nguyên; thiếu ngày chốt ⇒ phát hiện
    _so = p_sach.get("chot_3_so_lieu", {}).get("so_lieu") or []
    ok3 = (_so and all(r.get("dem_tren") and r.get("tieu_chi") and r.get("ngay_chot") for r in _so)
           and p_ngay.get("chot_3_so_lieu", {}).get("thieu_ngay_chot") is True and rc_ngay == 1)
    # ④ đầu vào sai = LỖI LỆNH (rc=2), khác hẳn "có phát hiện"
    ok4 = rc_khong_co == 2 and str(p_khong_co.get("error", "")).startswith("IN_KHONG_PHAI_THU_MUC")
    return bool(ok1 and ok2 and ok3 and ok4)
