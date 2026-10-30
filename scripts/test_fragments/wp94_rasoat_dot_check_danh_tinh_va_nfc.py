# -*- coding: utf-8 -*-
"""LỚP 3 — bốn chốt của lượt cross-review CỤC BỘ (4×P1), chạy TRƯỚC khi đẩy nên không tốn lượt CI nào.

Cả bốn đều là ca «cổng báo SẠCH khi chưa đo được gì», nhưng ở tầng sâu hơn `wp93`: ba cái đầu là lỗ
trong CHÍNH cái chốt vừa dựng, cái thứ tư là chặn OAN — nguy ngang nhau vì nó chặn việc đúng.

  G1 P1  `khoa_dinh_danh` chỉ cần KHÁC RỖNG là được tính là đã tra bằng định danh chuẩn hoá, nên một
         giá trị TRỏ ĐI ĐÂU KHÁC vẫn làm cổng báo sạch. *Reviewer nêu ví dụ `ILO-81`, và ví dụ ấy SAI:
         `_dinh_danh_chuan_hoa("ILO-81")` cũng ra `ILO-081` nên nhận nó là ĐÚNG.* Đã ĐO rồi mới viết ca:
         phản chứng thật là giá trị chuẩn hoá ra KHÁC (`ILO-82` → `ILO-082`).
  G2 P1  `json.dumps` MẶC ĐỊNH `ensure_ascii=True` ⇒ chuỗi NFD nằm trên đĩa dưới dạng escape ASCII;
         dòng thô là ASCII thuần nên NFC-sạch, bộ quét cũ IM, rồi `json.loads` dựng lại NFD và hàm
         đếm chuẩn hoá trong bộ nhớ. Cổng khai "đã chuẩn hoá" trong khi đếm trên biểu diễn KHÁC.
  G3 P1  lọc Đợt theo TÊN TỆP: `master/<unit>.json` là quy ước §6 chứ không phải bất biến ⇒ phiếu
         đúng đặt tên khác bị BỎ (báo 0 phát hiện "sạch"). Danh tính phải đọc từ payload `unit_id`,
         và đơn vị `done` mà thiếu phiếu là KHÔNG ĐO ĐƯỢC chứ không phải Đợt sạch (A6).
  H1 P1  `dot` chỉ bị đòi `dot_id`, còn `ten` không kiểm và `trang_thai` RỖNG lách qua enum ⇒
         `{"dot_id":"dot-01"}` lọt sạch dù §8 khai CẢ BA là bắt buộc. (Ca này ĐỎ đúng một fixture
         cũ của `wp91` — fixture sai, không phải bản vá sai.)
  H2 P2  đơn vị `done` thiếu phiếu / trùng `unit_id` mà vẫn xuất tổng kèm `kha_dung:true` — đúng lỗ
         G2/F6 ở dạng khác: số "tái lập được" tính trên tập KHÔNG phải tập đáng lẽ đếm.
  H3 P2  hai tệp cùng `unit_id` (bản chép đổi tên) bị đếm HAI LẦN; bất biến một-phiếu-một-đơn-vị
         đã có sẵn ở `_rasoat_trung_lap` (r216).
  G4 P1  `_rasoat_state_validate` thiếu `da_quyet`/`da_quyet_va_thi_hanh` mà đặc tả §3 CÓ khai ⇒ khi
         lệnh này biến nó thành cổng BẮT BUỘC lúc đóng Đợt thì state hợp lệ bị bác: fail-closed SAI
         CHIỀU. Kèm: mảng `dot` (§8) trước đây không được kiểm gì.
"""

import contextlib
import io
import json
import tempfile
import unicodedata
from pathlib import Path

TEST_ID = "wp94_rasoat_dot_check_danh_tinh_va_nfc"


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


def _dong(muc, dinh_danh, ket_qua="not_found"):
    return {"thoi_diem": "2026-09-05T09:00", "muc_tieu": muc, "khoa_so_hieu": muc,
            "khoa_ten": "ten day du " + muc, "khoa_dinh_danh": dinh_danh,
            "ket_qua": ket_qua, "lenh": "tl reg-query + tl locate + tl dedup-check"}


def _dung(root, state, units, rows, ensure_ascii=False):
    (root / "master").mkdir(parents=True)
    (root / "rasoat_state.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    for ten, u in units.items():
        (root / "master" / ten).write_text(json.dumps(u, ensure_ascii=ensure_ascii), encoding="utf-8")
    (root / "rasoat_tra_kho.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return root


def _unit(uid="u1", van_ban="Nghi dinh 217"):
    return {"unit_id": uid, "phat_hien": [{"key": "P1", "tieu_chi": "T2", "van_ban": van_ban}]}


def _st(q_ingest, **kw):
    return dict({"schema": "rasoat_plan.v1", "cap_nhat": "2026-09-05T09:00:00",
                 "q_ingest": q_ingest}, **kw)


def run(tl_module):
    ILO = "ILO 81"
    with tempfile.TemporaryDirectory(prefix="wp94_") as tmp:
        t = Path(tmp)
        qi = [{"so_hieu": ILO, "trang_thai": "cho_tai", "dot_id": "dot-01"}]

        # G1 — định danh TRỏ ĐI ĐÂU KHÁC phải KHÔNG được tính là đã tra; hai đối chứng dương ở dưới.
        # `ILO-82` chuẩn hoá thành `ILO-082` ≠ `ILO-081` ⇒ dòng KHÔNG chứng minh được đã tra định danh.
        rc_sai, p_sai = _goi(tl_module, ["rasoat-dot-check", "--in", str(
            _dung(t / "g1sai", _st(qi), {"u1.json": _unit()}, [_dong(ILO, "ILO-82")])), "--json"])
        # ĐỐI CHỨNG THỨ HAI (chống "chặn tuốt"): `ILO-81` viết thiếu đệm 0 vẫn quy về CÙNG định danh
        # ⇒ phải được NHẬN. Không có vế này thì ca không phân biệt được "khớp giá trị" với "khớp chuỗi".
        rc_tuong_duong, p_tuong_duong = _goi(tl_module, ["rasoat-dot-check", "--in", str(
            _dung(t / "g1td", _st(qi), {"u1.json": _unit()}, [_dong(ILO, "ILO-81")])), "--json"])
        rc_dung, p_dung = _goi(tl_module, ["rasoat-dot-check", "--in", str(
            _dung(t / "g1dung", _st(qi), {"u1.json": _unit()}, [_dong(ILO, "ILO-081")])), "--json"])

        # G2 — NFD ghi bằng `ensure_ascii=True`: dòng thô ASCII thuần, chỉ lộ khi soi GIÁ TRỊ đã giải mã.
        nfd = unicodedata.normalize("NFD", "Nghị định 217")
        d2 = _dung(t / "g2", _st(qi), {"u1.json": _unit(van_ban=nfd)},
                   [_dong(ILO, "ILO-081")], ensure_ascii=True)
        raw2 = (d2 / "master" / "u1.json").read_text(encoding="utf-8")
        rc2, p2 = _goi(tl_module, ["rasoat-dot-check", "--in", str(d2), "--json"])

        # G3 — phiếu ĐÚNG nhưng đặt tên khác: phải theo `unit_id` trong payload, không theo tên tệp.
        # §8: `--dot` đòi ĐÚNG MỘT bản ghi metadata trong `dot`.
        st3 = _st(qi, dot=[{"dot_id": "dot-01", "ten": "Đợt 1", "trang_thai": "dang_ra", "mo_luc": "2026-09-01"}],
                  q_units=[{"unit_id": "u1", "dot_id": "dot-01", "trang_thai": "done"}])
        rc3, p3 = _goi(tl_module, ["rasoat-dot-check", "--in", str(
            _dung(t / "g3", st3, {"other.json": _unit()}, [_dong(ILO, "ILO-081")])),
            "--dot", "dot-01", "--json"])
        # …và đơn vị `done` KHÔNG có phiếu nào = KHÔNG ĐO ĐƯỢC, không phải "Đợt sạch" (A6).
        st3b = _st(qi, dot=[{"dot_id": "dot-01", "ten": "Đợt 1", "trang_thai": "dang_ra", "mo_luc": "2026-09-01"}],
                   q_units=[{"unit_id": "u1", "dot_id": "dot-01", "trang_thai": "done"},
                            {"unit_id": "u9", "dot_id": "dot-01", "trang_thai": "done"}])
        rc3b, p3b = _goi(tl_module, ["rasoat-dot-check", "--in", str(
            _dung(t / "g3b", st3b, {"u1.json": _unit()}, [_dong(ILO, "ILO-081")])),
            "--dot", "dot-01", "--json"])

        # G4 — trạng thái ĐẶC TẢ CÓ KHAI phải được NHẬN (chặn oan cũng là hỏng); `dot` rác phải bị BÁC.
        rc4, p4 = _goi(tl_module, ["rasoat-dot-check", "--in", str(
            _dung(t / "g4", _st([{"so_hieu": ILO, "trang_thai": "da_quyet", "dot_id": "dot-01"}]),
                  {"u1.json": _unit()}, [_dong(ILO, "ILO-081")])), "--json"])
        rc4b, p4b = _goi(tl_module, ["rasoat-dot-check", "--in", str(
            _dung(t / "g4b", _st(qi, dot="broken"), {"u1.json": _unit()},
                  [_dong(ILO, "ILO-081")])), "--json"])

        # H1 — `dot` thiếu `ten`/`trang_thai` phải BỊ BÁC; đối chứng dương: đủ ba trường ⇒ qua.
        rch1, ph1 = _goi(tl_module, ["rasoat-dot-check", "--in", str(
            _dung(t / "h1", _st(qi, dot=[{"dot_id": "dot-01"}]), {"u1.json": _unit()},
                  [_dong(ILO, "ILO-081")])), "--json"])
        rch1b, ph1b = _goi(tl_module, ["rasoat-dot-check", "--in", str(
            _dung(t / "h1b", _st(qi, dot=[{"dot_id": "dot-01", "ten": "Đợt 1",
                                           "trang_thai": "dang_ra",
                                           "mo_luc": "2026-09-01T08:00:00"}]),
                  {"u1.json": _unit()}, [_dong(ILO, "ILO-081")])), "--json"])

        # H3 — hai tệp cùng `unit_id`; H2 — số liệu phải KHÔNG khả dụng khi tập đếm không toàn vẹn.
        rch3, ph3 = _goi(tl_module, ["rasoat-dot-check", "--in", str(
            _dung(t / "h3", _st(qi), {"u1.json": _unit(), "u1.copy.json": _unit()},
                  [_dong(ILO, "ILO-081")])), "--json"])
        # H2 — đơn vị `done` thiếu phiếu: đã có ở p3b, chỉ thêm khẳng định về số liệu.

    def _ph(p):
        return p.get("chot_2_tra_kho", {}).get("phat_hien") or []

    # Dòng này khai `khoa_so_hieu` KHỚP nhưng `khoa_dinh_danh` LỆCH ⇒ TỰ MÂU THUẪN. Phân loại ba
    # trạng thái (lượt 8) gọi đúng tên nó thay vì gộp vào `THIEU_KHOA` — sổ hỏng khác với sổ thiếu.
    g1 = (rc_sai == 1 and any(f["ma"] == "DONG_TU_MAU_THUAN" and f.get("dong") for f in _ph(p_sai))
          and rc_dung == 0 and p_dung.get("ok") is True
          and rc_tuong_duong == 0 and p_tuong_duong.get("ok") is True)
    # phản chứng của CHÍNH fixture: dòng thô PHẢI là ASCII thuần, nếu không thì ca này đo nhầm thứ
    g2 = (raw2.isascii() and unicodedata.normalize("NFC", raw2) == raw2
          and rc2 == 1 and p2["chot_1_nfc"]["ok"] is False
          and any(x["ma"] == "CHUA_CHUAN_HOA_NFC_SAU_GIAI_MA" and x.get("vi_tri")
                  for x in p2["chot_1_nfc"]["lech"]))
    g3 = (rc3 == 0 and p3.get("ok") is True
          and next((r["gia_tri"] for r in p3["chot_3_so_lieu"]["so_lieu"]
                    if r["ten"] == "so_phat_hien"), None) == 1
          and rc3b == 1 and any(x["ma"] == "DON_VI_DONE_THIEU_PHIEU_MASTER" and x["unit_id"] == "u9"
                                for x in (p3b.get("thieu_payload") or [])))
    g4 = (rc4 == 0 and p4.get("ok") is True            # `da_quyet` hợp lệ ⇒ KHÔNG được chặn
          and rc4b == 2 and "DOT_KHONG_PHAI_MANG" in str(p4b.get("state", {}).get("loi") or ""))
    h1 = (rch1 == 2 and "DOT[0]_THIEU_TEN" in str(ph1.get("state", {}).get("loi") or "")
          and "DOT[0]_THIEU_TRANG_THAI" in str(ph1.get("state", {}).get("loi") or "")
          and rch1b == 0 and ph1b.get("ok") is True)      # đối chứng dương: đủ ba trường ⇒ qua
    h3 = (rch3 == 1 and any(x.get("ma") == "TRUNG_UNIT_ID" and x.get("gia_tri") == "u1"
                            for x in (ph3.get("thieu_payload") or [])))
    # H2 — cả hai đường "tập đếm không toàn vẹn" đều phải khai KHÔNG KHẢ DỤNG, không xuất tổng
    h2 = (ph3["chot_3_so_lieu"].get("kha_dung") is False
          and not (ph3["chot_3_so_lieu"].get("so_lieu") or [])
          and p3b["chot_3_so_lieu"].get("kha_dung") is False
          and not (p3b["chot_3_so_lieu"].get("so_lieu") or []))
    return bool(g1 and g2 and g3 and g4 and h1 and h2 and h3)
