# -*- coding: utf-8 -*-
"""tl_core/rasoat_dot_check.py — LỚP 3: cổng kiểm CUỐI ĐỢT của vòng rà hồ sơ (READ-ONLY, offline).

VÌ SAO ĐỨNG RIÊNG MỘT TỆP (bóc khỏi `lookup_ops.py`, không đổi một dòng thân nào):
ratchet `py_size` (WARN >280KiB, khoá bởi ca `r125_py_size_guard_wired_in_audit` đòi `warn == []`)
đã CẮN HAI LẦN trong một phiên khi khối này còn nằm trong `lookup_ops.py`: 287.366 B rồi
287.272 B, hai lần phải nén chú thích để luồn xuống dưới, lần cuối chỉ còn dư 451 B. Nén
chú thích để luồn qua một ratchet là trả bằng thứ kho này coi trọng nhất — phần "vì sao" — để
mua một lượt xanh; ratchet sinh ra chính là để ÉP BÓC chứ không để ép cắt chữ.

Khối này KHÔNG import gì từ `tl_core` khác: sau khi `bind()` chạy, mọi tên dùng chung (`norm_sohieu`,
`_rasoat_la_ban_sao`, `_rasoat_unit_shape`, `_rasoat_state_validate`, `_rasoat_trung_lap`,
`_print_json_or_text`, `_json_dumps`, `json`, `re`, `unicodedata`, `Path`) được giải qua
`__globals__` đã re-home về `tl` — cùng cơ chế mọi module `tl_core` khác đang dùng.
"""

_TL = None


def bind(tl_module) -> None:
    """REBASE `__globals__` từng hàm về namespace SỐNG của `tl` (khổ I1-I5, chép từ `lookup_ops`).

    ĐIỂM NỐI DÂY THỨ 5, và là cái TÔI ĐÃ ĐOÁN SAI: khi bóc khối này ra, tôi viết trong chính
    docstring ở đầu tệp rằng "mọi tên dùng chung giải qua `__globals__` đã re-home" — một lời khai
    KHÔNG ĐO. Re-home KHÔNG tự xảy ra: nó là việc của `bind()`, và `tl.py` chỉ gọi `bind` cho
    những module nằm trong danh sách ở cuối tệp. Thiếu cả hai ⇒ `NameError: Path` ngay lời gọi đầu.
    """
    global _TL
    _TL = tl_module
    import types
    g = globals()
    tg = tl_module.__dict__
    for _n, _fn in list(g.items()):
        if isinstance(_fn, types.FunctionType) and _fn.__module__ == __name__ and _n != "bind":
            _re = types.FunctionType(_fn.__code__, tg, _n, _fn.__defaults__, _fn.__closure__)
            _re.__kwdefaults__ = _fn.__kwdefaults__
            _re.__doc__ = _fn.__doc__
            _re.__module__ = __name__
            g[_n] = _re


# ══════════ LỚP 3 — `rasoat-dot-check`: cổng kiểm CUỐI ĐỢT (READ-ONLY, offline) ══════════
# Ba chốt máy cho ba lỗi NGƯỜI lặp lại, đo trên hồ sơ ATVSLĐ (7 Đợt / 11 lượt):
#   L3-1 NFC     — số kho thừa kế qua nhiều lượt không đo lại; đếm trên bản đã chuẩn hoá ra số KHÁC
#                  ⇒ mọi phép ĐẾM chạy trên NFC, lệch thì DỪNG chứ không tự sửa rồi đếm tiếp.
#   L3-2 3 KHOÁ  — 3 lần kết luận "kho thiếu" SAI vì tra MỘT khoá: `ILO 81` (kho lưu `ILO-081`) ·
#                  NĐ 217/2025 (dừng khi thấy NĐ 216/2025) · NQ 66.17/2026 (lọc máy móc theo loại).
#   L3-3 TÁI LẬP — số lệch giữa Phiếu/Báo cáo/Phụ lục vì không ghi "đếm trên gì, tiêu chí nào".
# KHÔNG phải engine thứ hai: không sinh đơn vị, không ghi state, không mạng/NLM/Drive — chỉ ĐỌC và
# trả verdict. Chi tiết từng bản vá: xem ca `wp91`–`wp94`.

_DOT_CHECK_SCHEMA = "rasoat_dot_check.v1"
_TRA_KHO_TRUONG = ("thoi_diem", "muc_tieu", "ket_qua", "lenh")   # sổ sách — thiếu = chưa ghi sổ
_TRA_KHO_KHOA = ("khoa_so_hieu", "khoa_ten", "khoa_dinh_danh")    # mỗi dòng ghi ÍT NHẤT MỘT khoá đã tra
_DOT_CHECK_THIEU_TT = ("cho_tai", "cho_nguoi_tai")
_DOT_CHECK_SO_TRA_KHO = "rasoat_tra_kho.jsonl"
# F2 (P1, tái hiện được): bản đầu chỉ từ chối ĐÚNG chuỗi `found`, nên `ket_qua="error"` (tra HỎNG)
# vẫn thành bằng chứng `not_found`, rc=0 `ok:true`. Danh sách CẤM thua danh sách CHO PHÉP: enum ĐÓNG.
_TRA_KHO_KET_QUA = ("not_found", "found")


def _khoa_hop_le(v) -> str:
    """Giá trị khoá tra kho chỉ hợp lệ khi nó là CHUỖI khác rỗng — trả bản đã strip, hoặc "".

    Bản trước dùng `str(v).strip()` khắp nơi, mà `str([""])` là `"['']"` — KHÁC RỖNG. Một dòng
    khai `khoa_ten: [""]` vì thế được tính là "đã tra bằng tên", và cổng trả `ok:true` cho một
    kết luận «kho thiếu» chưa có bằng chứng nào về tên. `str()` nhận MỌI thứ, nên nó không phải
    phép kiểm — nó là phép ép kiểu đội lốt phép kiểm."""
    return v.strip() if isinstance(v, str) else ""


def _dinh_danh_chuan_hoa(s) -> str:
    """Khoá THỨ BA khi tra kho (`references/RASOAT_HOSO_LOOP.md` §10). BỌC `norm_sohieu` SẴN CÓ — SKILL.md
    §0 #15 cấm viết lại cái đã có — và chỉ thêm đúng hai biệt lệ ĐÃ ĐO ĐƯỢC:
      · `_` → `-` trước khi chuẩn hoá (tên file Drive dùng `_`, registry dùng `/`);
      · công ước ILO đệm 0 tới 3 chữ số: `ILO 81` ≡ `ILO81` ≡ `ILO-81` ≡ `ILO-081` (ca tra sót thật).
    GIỮ dấu chấm phần số (`66.17/2026/NQ-CP` → `66.17-2026-NQ-CP`): đó là số hiệu thật, không phải nhiễu."""
    raw = unicodedata.normalize("NFC", str(s or "")).strip()
    if not raw:
        return ""
    key = norm_sohieu(raw.replace("_", "-"))
    m = re.fullmatch(r"ILO-?(\d{1,3})", key)
    return "ILO-%03d" % int(m.group(1)) if m else key


def _nfc_lech(text) -> list:
    """Số dòng (1-based) chưa ở dạng NFC. Fail-CLOSED: nêu ĐÍCH DANH dòng lệch, KHÔNG âm thầm chuẩn hoá
    rồi đếm tiếp — đếm trên bản vừa tự sửa là mất luôn bằng chứng vì sao số cũ khác số mới."""
    out = []
    for i, line in enumerate(str(text or "").split("\n"), 1):
        if unicodedata.normalize("NFC", line) != line:
            out.append(i)
            if len(out) >= 50:
                break
    return out


def _nfc_lech_json(obj, duong="$") -> list:
    """G2 (P1) — quét NFC trên GIÁ TRỊ ĐÃ GIẢI MÃ, đệ quy.

    Quét dòng thô KHÔNG đủ: `json.dumps` mặc định `ensure_ascii=True` nên chuỗi NFD nằm trên đĩa
    dưới dạng escape ASCII ⇒ dòng thô là ASCII thuần, NFC-SẠCH, bộ quét cũ im; rồi `json.loads`
    dựng lại NFD và hàm đếm chuẩn hoá trong bộ nhớ — cổng khai "đã chuẩn hoá" mà đếm trên biểu
    diễn KHÁC. Khoá dict cũng phải soi."""
    out = []
    if isinstance(obj, str):
        if unicodedata.normalize("NFC", obj) != obj:
            out.append(duong)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            ks = str(k)
            if unicodedata.normalize("NFC", ks) != ks:
                out.append(duong + ".<khoá>" + ks)
            out += _nfc_lech_json(v, duong + "." + ks)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += _nfc_lech_json(v, duong + "[%d]" % i)
    return out[:50]


def _dot_check_nfc(files) -> dict:
    lech = []
    for p in files:
        fp = Path(p)
        try:
            t = fp.read_text(encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            lech.append({"file": fp.name, "ma": "KHONG_DOC_DUOC", "chi_tiet": str(e), "dong": []})
            continue
        d = _nfc_lech(t)
        if d:
            lech.append({"file": fp.name, "ma": "CHUA_CHUAN_HOA_NFC", "dong": d})
        # GIỮ phép quét thô ở trên (bắt cả tệp không phải JSON), THÊM phép quét giá trị đã giải mã.
        _suf = fp.suffix.lower()
        if _suf not in (".json", ".jsonl"):
            continue
        _khoi = []
        try:
            if _suf == ".jsonl":
                for _i, _ln in enumerate(t.splitlines(), 1):
                    if _ln.strip():
                        _khoi.append((_i, json.loads(_ln)))
            else:
                _khoi.append((0, json.loads(t)))
        except Exception:  # noqa: BLE001
            continue          # JSON hỏng đã có mã lỗi riêng ở đường gọi; đừng báo trùng
        _dd = []
        for _dong_so, _o in _khoi:
            for _duong in _nfc_lech_json(_o):
                _dd.append({"dong": _dong_so, "duong_dan": _duong} if _dong_so else {"duong_dan": _duong})
        if _dd:
            lech.append({"file": fp.name, "ma": "CHUA_CHUAN_HOA_NFC_SAU_GIAI_MA", "vi_tri": _dd[:50]})
    return {"so_file_da_quet": len(files), "lech": lech, "ok": not lech}


def _tra_kho_doc(path) -> tuple:
    """Đọc sổ `rasoat_tra_kho.jsonl` (khuôn `TRA_KHO_LOG_v1`). Mục thiếu trường = coi như CHƯA ghi sổ,
    cùng luật với `BUG_LEDGER_v1` 8 trường."""
    rows, hong = [], []
    p = Path(path)
    if not p.exists():
        return rows, [{"dong": 0, "ma": "SO_TRA_KHO_KHONG_TON_TAI", "file": p.name}]
    try:
        noi_dung = p.read_text(encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        return rows, [{"dong": 0, "ma": "SO_TRA_KHO_KHONG_DOC_DUOC", "chi_tiet": str(e)}]
    for i, line in enumerate(noi_dung.split("\n"), 1):
        s = line.strip()
        if not s:
            continue
        try:
            r = json.loads(s)
        except Exception:  # noqa: BLE001
            hong.append({"dong": i, "ma": "JSON_HONG"})
            continue
        if not isinstance(r, dict):
            hong.append({"dong": i, "ma": "JSON_HONG"})
            continue
        thieu = [k for k in _TRA_KHO_TRUONG if not str(r.get(k) or "").strip()]
        if thieu:
            hong.append({"dong": i, "ma": "THIEU_TRUONG", "truong": thieu})
            continue
        # Dòng KHÔNG khai khoá nào = không nói được đã tra bằng gì ⇒ vô nghĩa với chốt 3 khoá.
        if not any(_khoa_hop_le(r.get(k)) for k in _TRA_KHO_KHOA):
            hong.append({"dong": i, "ma": "KHONG_KHAI_KHOA", "truong": list(_TRA_KHO_KHOA)})
            continue
        # F2: `ket_qua` phải nằm trong enum ĐÓNG. `error`/lỗi chính tả/phản hồi lạ = KHÔNG BIẾT kết
        # quả, mà "không biết" ≠ "không có" — đúng doctrine ba trạng thái, `None` ≠ `False`.
        if str(r.get("ket_qua") or "").strip() not in _TRA_KHO_KET_QUA:
            hong.append({"dong": i, "ma": "KET_QUA_NGOAI_ENUM",
                         "gia_tri": str(r.get("ket_qua") or ""), "cho_phep": list(_TRA_KHO_KET_QUA)})
            continue
        rows.append(r)
    return rows, hong


def _dot_check_tra_kho(claims, rows) -> dict:
    """Kết luận «kho thiếu văn bản X» chỉ hợp lệ khi CẢ BA khoá đã được tra và đều `not_found`.
    So khớp mục tiêu bằng ĐỊNH DANH CHUẨN HOÁ, nên `ILO 81` và `ILO-081` là MỘT — chính chỗ ba ca
    tra sót đã lọt."""
    theo_dd = {}
    for r in rows:
        theo_dd.setdefault(_dinh_danh_chuan_hoa(r.get("muc_tieu")), []).append(r)
    phat_hien = []
    for c in claims:
        dd = _dinh_danh_chuan_hoa(c)
        lien_quan = theo_dd.get(dd) or []
        if not lien_quan:
            phat_hien.append({"muc_tieu": c, "dinh_danh": dd, "ma": "KHONG_CO_LOG_TRA_KHO"})
            continue
        # G1 (P1): bản trước chỉ hỏi trường có RỖNG không, nên một định danh TRỎ ĐI ĐÂU KHÁC vẫn
        # tính là đã tra. Phải KHỚP GIÁ TRỊ sau chuẩn hoá; ghi sai = CHƯA tra, và nói ra chỗ sai.
        # ★ MỘT quyết định TƯ CÁCH cho mỗi dòng, dùng cho CẢ khoá LẪN kết quả. Bản trước tách đôi:
        # `da_tra` tính khoá theo từng-trường còn `_khop` lọc theo từng-DÒNG ⇒ một dòng khai đúng
        # `khoa_ten` + `found` nhưng gõ nhầm `khoa_so_hieu` được TÍNH khoá mà KHÔNG tính kết quả
        # ⇒ cổng báo sạch cho văn bản đã tìm thấy. Hai luật xét khác nhau trên cùng một dòng là chỗ
        # lệch tự mọc; nay dòng nào NÓI RÕ trỏ văn bản khác thì bị loại HẲN — không góp khoá, không
        # góp kết quả. Đó cũng là câu trả lời đúng về ngữ nghĩa: dòng ấy không đáng tin cho mục tiêu này.
        def _phan_loai_dong(r):
            """BA trạng thái, không phải hai — và đây là lần thứ ba luật này bị sửa, nên viết rõ.

            Bản trước chỉ hỏi "có khoá nào trỏ nơi khác không"; dòng vừa có khoá KHỚP vừa có khoá
            LỆCH (vd `khoa_so_hieu=217…` + `khoa_dinh_danh=216…` + `found`) bị xếp là "của văn bản
            khác" rồi DROP — nuốt mất một bằng chứng `found` ⇒ các dòng `not_found` sau đó phủ đủ ba
            khoá là cổng trả `ok:true`. Nuốt bằng chứng còn tệ hơn đọc nhầm nó.
              · `khop`      — không khoá máy nào lệch (kể cả dòng chỉ có `khoa_ten`): TÍNH cả khoá
                              lẫn kết quả.
              · `khac`      — MỌI khoá máy đã khai đều trỏ nơi khác: dòng lịch sử của văn bản khác,
                              BỎ QUA (đây là điều cho sổ append-only sửa được mà không phải xoá).
              · `mau_thuan` — vừa khớp vừa lệch: SỔ HỎNG, không phải bằng chứng. Là PHÁT HIỆN.
            """
            khop, lech = [], []
            for k in ("khoa_dinh_danh", "khoa_so_hieu"):
                v = _khoa_hop_le(r.get(k))
                if not v:
                    continue
                (khop if _dinh_danh_chuan_hoa(v) == dd else lech).append(k)
            if khop and lech:
                return "mau_thuan"
            if lech:
                # `khac` = dòng CHẮC CHẮN nói về văn bản khác. Một dòng vừa có khoá máy LỆCH vừa khai
                # `khoa_ten` (tra theo TÊN — không quy về định danh được) thì KHÔNG chắc: phép tra
                # theo tên ấy có thể đã trúng CHÍNH mục tiêu. Xếp nó là "không liên quan" rồi drop là
                # nuốt một `found`. Không chắc ⇒ MÂU THUẪN, tức fail-closed.
                return "mau_thuan" if str(r.get("khoa_ten") or "").strip() else "khac"
            return "khop"

        da_tra, lech_dd, _khop = set(), [], []
        mau_thuan = []
        for r in lien_quan:
            _loai = _phan_loai_dong(r)
            if _loai != "khop":
                _ghi = [{"khoa": k, "da_ghi": _khoa_hop_le(r.get(k)),
                         "chuan_hoa_thanh": _dinh_danh_chuan_hoa(_khoa_hop_le(r.get(k)))}
                        for k in ("khoa_dinh_danh", "khoa_so_hieu")
                        if _khoa_hop_le(r.get(k))
                        and _dinh_danh_chuan_hoa(_khoa_hop_le(r.get(k))) != dd]
                lech_dd.extend(_ghi)
                if _loai == "mau_thuan":
                    mau_thuan.append({"thoi_diem": str(r.get("thoi_diem") or ""),
                                      "ket_qua": str(r.get("ket_qua") or ""), "khoa_lech": _ghi})
                continue
            _khop.append(r)
            for k in _TRA_KHO_KHOA:
                v = _khoa_hop_le(r.get(k))
                if not v:
                    continue
                # Khai thẳng giới hạn: `khoa_ten` là VĂN XUÔI, không quy về định danh được, nên chỉ
                # kiểm KHÁC RỖNG — đó là chỗ máy KHÔNG gác được, người phải đọc.
                da_tra.add(k)
        da_tra = sorted(da_tra)
        thieu = [k for k in _TRA_KHO_KHOA if k not in da_tra]
        if mau_thuan:
            # Sổ tự mâu thuẫn thì KHÔNG kết luận gì được từ nó — kể cả kết luận "đủ ba khoá".
            phat_hien.append({"muc_tieu": c, "dinh_danh": dd, "ma": "DONG_TU_MAU_THUAN",
                              "dong": mau_thuan[:5]})
            continue
        if thieu:
            _m = {"muc_tieu": c, "dinh_danh": dd, "ma": "THIEU_KHOA",
                  "khoa_da_tra": da_tra, "khoa_thieu": thieu}
            if lech_dd:
                _m["khoa_dinh_danh_lech"] = lech_dd[:5]
            phat_hien.append(_m)
            continue
        # F2: đòi MỌI dòng liên quan đều đúng `not_found`. Bản đầu chỉ hỏi "có dòng nào `found`
        # không" — mệnh đề ấy đúng nhưng KHÔNG đủ: nó im lặng với mọi giá trị thứ ba.
        # Sổ là APPEND-ONLY: một dòng CŨ tra nhầm văn bản (khoá trỏ 216 trong khi mục tiêu là 217)
        # mang `found` thì trước đây vẫn tính vào phán quyết, dù chính khoá ấy đã bị loại khỏi
        # `da_tra` vì không khớp. Hệ quả: các dòng SỬA SAU không bao giờ gỡ được cờ chặn, trừ khi
        # XOÁ lịch sử — tức cổng ép người ta phá sổ kiểm toán để đi tiếp. Chỉ lấy kết quả từ dòng
        # có khoá KHỚP mục tiêu; dòng không khớp đã được nêu ở `khoa_dinh_danh_lech`, không mất dấu.
        # HỒI QUY của chính bản vá trước, và nó mở một đường BÁO SẠCH: bản ấy GIỮ LẠI dòng khi có
        # khoá máy-so-được KHỚP, nên dòng chỉ khai `khoa_ten` (không có khoá máy-so-được nào) bị
        # LOẠI — kể cả khi nó mang `found`. Hai dòng kia `not_found` là cổng trả `ok:true` cho văn
        # bản THỰC RA ĐÃ TÌM THẤY. Luật đúng phải là LOẠI TRỪ, không phải GIỮ LẠI: chỉ bỏ dòng
        # NÓI RÕ nó trỏ văn bản KHÁC. Dòng không khai khoá máy-so-được nào thì không mâu thuẫn với
        # mục tiêu ⇒ kết quả của nó VẪN TÍNH (`khoa_ten` vốn đã được tính vào `da_tra` ở trên).
        if _khop and not all(str(r.get("ket_qua") or "").strip() == "not_found" for r in _khop):
            phat_hien.append({"muc_tieu": c, "dinh_danh": dd, "ma": "CO_HIT_MA_VAN_KET_LUAN_THIEU",
                              "ket_qua_da_ghi": sorted({str(r.get("ket_qua") or "") for r in _khop})})
    return {"so_ket_luan_thieu": len(claims), "phat_hien": phat_hien, "ok": not phat_hien}


def _dot_check_so_lieu(docs, ngay_chot, dem_tren) -> dict:
    """Hàm THUẦN — đếm lại từ `master/*.json` (chạy lại bao nhiêu lần cũng ra một số) và xuất SỔ TÁI LẬP:
    mỗi con số kèm ĐẾM TRÊN GÌ · TIÊU CHÍ NÀO · NGÀY CHỐT NÀO. Không có ngày chốt ⇒ số không tái lập được."""
    theo_tc, tong, van_ban = {}, 0, set()
    for _name, d in docs:
        muc = (d or {}).get("phat_hien") or (d or {}).get("noi_dung") or []
        for ph in muc if isinstance(muc, list) else []:
            if not isinstance(ph, dict):
                continue
            tong += 1
            tc = unicodedata.normalize("NFC", str(ph.get("tieu_chi") or "").strip()) or "(chưa ghi tiêu chí)"
            theo_tc[tc] = theo_tc.get(tc, 0) + 1
            vb = _dinh_danh_chuan_hoa(ph.get("van_ban"))
            if vb:
                van_ban.add(vb)
    so = [{"ten": "so_phat_hien", "gia_tri": tong, "tieu_chi": "(tất cả)"},
          {"ten": "so_van_ban_bi_cham", "gia_tri": len(van_ban), "tieu_chi": "(tất cả)"}]
    so += [{"ten": "so_phat_hien_theo_tieu_chi", "gia_tri": v, "tieu_chi": k}
           for k, v in sorted(theo_tc.items())]
    cach = "đếm phần tử `phat_hien`/`noi_dung` sau chuẩn hoá NFC; `van_ban` quy về định danh chuẩn hoá"
    for r in so:
        r["dem_tren"], r["ngay_chot"], r["cach_dem"] = dem_tren, ngay_chot, cach
    thieu_ngay = not str(ngay_chot or "").strip()
    return {"so_lieu": so, "thieu_ngay_chot": thieu_ngay, "ok": not thieu_ngay}


def cmd_rasoat_dot_check(a) -> int:
    """READ-ONLY cổng kiểm CUỐI ĐỢT — ba chốt L3-1 NFC · L3-2 tra kho 3 khoá · L3-3 số liệu tái lập.
    Offline hoàn toàn: chỉ đọc `<out-dir>` của lượt rà; không mạng, không NLM/Drive, không ghi state.
    rc=0 sạch · rc=1 CÓ PHÁT HIỆN (là VERDICT dữ liệu, không phải lệnh hỏng — khuôn EXIT CODE SKILL.md
    §2) · rc=2 lỗi đầu vào, hoặc `--strict` mà có phát hiện."""
    inp = str(getattr(a, "in_dir", "") or "").strip()
    p = Path(inp) if inp else None
    if not p or not p.is_dir():
        _print_json_or_text({"schema": _DOT_CHECK_SCHEMA, "ok": False,
                             "error": "IN_KHONG_PHAI_THU_MUC: " + (inp or "(trống)"),
                             "fix": "trỏ `--in` vào <out-dir> của lượt rà (ngoài cây skill)"}, True)
        return 2
    dot = str(getattr(a, "dot", "") or "").strip()
    state_path = Path(str(getattr(a, "state", "") or "").strip() or (p / "rasoat_state.json"))
    master_dir = p / "master"
    so_tra_kho = p / _DOT_CHECK_SO_TRA_KHO

    state = {}
    state_loi = ""
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            state_loi = "STATE_JSON_HONG: " + str(e)
        else:
            # F3 (P1, tái hiện được): «đọc được JSON» KHÁC «state hợp lệ» — `q_units:"broken"` bị đọc
            # thành RỖNG nên không claim nào được rút, cổng im lặng báo sạch. Tái dùng RAS-09 (#15).
            _ok_st, _errs = _rasoat_state_validate(state)
            if not _ok_st:
                state_loi = "STATE_KHONG_HOP_LE: " + "; ".join(_errs[:6])
                state = {}
    else:
        state_loi = "STATE_KHONG_TON_TAI"

    # ① claims = mọi kết luận "kho thiếu" của Đợt: q_ingest `cho_tai`/`cho_nguoi_tai` + `--claim` rời.
    claims = []
    for m in (state.get("q_ingest") or []) if isinstance(state, dict) else []:
        if not isinstance(m, dict):
            continue
        if dot and str(m.get("dot_id") or "") != dot:
            continue
        if str(m.get("trang_thai") or "") in _DOT_CHECK_THIEU_TT:
            claims.append(str(m.get("so_hieu") or "").strip())
    claims += [str(c).strip() for c in (getattr(a, "claim", None) or [])]
    claims = sorted({c for c in claims if c})

    master_files = sorted(master_dir.glob("*.json")) if master_dir.is_dir() else []
    # F5 (P2, tái hiện được): bản đầu chỉ lọc `q_ingest`, master nạp SẠCH ⇒ `--dot dot-01` vẫn đếm
    # unit của `dot-02`. Ánh xạ unit→Đợt ở `state.q_units[].dot_id`; thiếu ánh xạ ⇒ KHÔNG ĐO ĐƯỢC.
    # LỚP D: bản trước đặt CHỐT COVERAGE bên trong nhánh `--dot`, nên soi cả hồ sơ (bỏ `--dot`) thì
    # chốt biến mất — rc=0 `ok:true` cho một Đợt có đơn vị `done` thiếu phiếu. Một chốt chỉ sống ở
    # MỘT NHÁNH là chốt vắng mặt ở nhánh kia; nay tập kỳ vọng dựng cho CẢ HAI chế độ.
    dot_loi, unit_cua_dot, _hop_le = "", None, []
    _qu = (state.get("q_units") or []) if isinstance(state, dict) else []
    _md = [u for u in _qu if isinstance(u, dict)
           and (not dot or str(u.get("dot_id") or "") == dot)]
    _done_cua_dot = {str(u.get("unit_id") or "").strip()
                     for u in _md if str(u.get("trang_thai") or "") == "done"}
    _done_cua_dot.discard("")
    if dot:
        # Bản trước chỉ hỏi "có unit nào mang dot_id này". Một Đợt KHÔNG có bản ghi metadata trong
        # `state.dot` thì không có tên/trạng thái/mốc/giới hạn — không có gì để đóng, mà cổng vẫn
        # trả thành công. §8 đòi metadata cho MỖI Đợt ⇒ thiếu = KHÔNG ĐO ĐƯỢC.
        _bg = [x for x in ((state.get("dot") or []) if isinstance(state, dict) else [])
               if isinstance(x, dict) and str(x.get("dot_id") or "").strip() == dot]
        if len(_bg) != 1:
            dot_loi = ("DOT_KHONG_CO_BAN_GHI: state.dot có %d bản ghi mang dot_id=%r (phải đúng 1) "
                       "⇒ Đợt không có metadata để đóng" % (len(_bg), dot))
        unit_cua_dot = {str(u.get("unit_id") or "").strip() for u in _md}
        if not dot_loi and not unit_cua_dot:
            dot_loi = ("DOT_KHONG_ANH_XA_DUOC_UNIT: state.q_units không có mục nào mang dot_id=%r "
                       "⇒ không lọc được master theo Đợt" % dot)
    docs, master_hong = [], []
    for f in master_files:
        if _rasoat_la_ban_sao(f.name):
            continue
        try:
            _d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            master_hong.append({"file": f.name, "ma": "JSON_HONG", "chi_tiet": str(e)})
            continue
        # F4 (P1, tái hiện được): `{}` giải mã SẠCH rồi được đếm "0 phát hiện" ⇒ báo cáo trắng trông
        # y hệt Đợt thật sự sạch. `_rasoat_unit_shape` (r213/b) tự dặn FAIL-CLOSED trên `unknown`.
        _khuon = _rasoat_unit_shape(_d)
        if _khuon == "unknown":
            master_hong.append({"file": f.name, "ma": "KHUON_KHONG_NHAN_RA",
                                "chi_tiet": "không phải unit_v1 lẫn bang_v1"})
            continue
        # `_rasoat_unit_shape` chỉ hỏi trường KIA có phải LIST không, nên `{"phat_hien": [],
        # "noi_dung": "bad"}` được nhận là `unit_v1`; xuống `_rasoat_trung_lap` thì `[] + "bad"`
        # ném `TypeError` ⇒ traceback trần thay vì verdict có cấu trúc. Cổng phải hỏng ỒN ÀO ĐÚNG
        # KHUÔN, không hỏng bằng stack trace. Không sửa `_rasoat_unit_shape` vì `rasoat-merge` dùng
        # chung nó — chặn ngay tại chỗ gọi, đúng lời hàm ấy tự dặn (bên gọi FAIL-CLOSED).
        _lai = [_k for _k in ("phat_hien", "noi_dung")
                if _k in _d and not isinstance(_d.get(_k), list)]
        if _lai:
            master_hong.append({"file": f.name, "ma": "TRUONG_SAI_KIEU",
                                "truong": _lai, "chi_tiet": "phải là list hoặc vắng mặt"})
            continue
        docs.append((f.name, _d))
        _hop_le.append(f)

    # G3 (P1): lọc theo TÊN TỆP là danh tính không ai bảo đảm — `master/<unit>.json` là quy ước §6,
    # và `rasoat-merge` đã coi `unit_id` TRONG PAYLOAD là chân lý. Phân tích TRƯỚC, chọn theo payload.
    thieu_payload = []
    if unit_cua_dot is not None:
        _giu = {n for n, _d in docs
                if str((_d or {}).get("unit_id") or "").strip() in unit_cua_dot}
        docs = [(n, d) for n, d in docs if n in _giu]
        _hop_le = [f for f in _hop_le if f.name in _giu]
        # A6: `done` PHẢI có phiếu master ⇒ thiếu = KHÔNG ĐO ĐƯỢC, không phải "Đợt sạch". Chỉ đòi
        # ở `done`; `pending`/`blocked` chưa có phiếu là chuyện thường.

    # H3 (P2): hai tệp cùng `unit_id` ⇒ đếm HAI LẦN mà cổng vẫn `ok:true`. Tái dùng
    # `_rasoat_trung_lap` (r216, #15); áp SAU khi lọc Đợt để chỉ xét tập sắp đếm.
    # `dot_id` trỏ Đợt CHƯA KHAI: đặc tả cho phép ở state (xếp việc cho Đợt sắp mở), nhưng lúc ĐÓNG
    # thì một mục còn treo mà không thuộc Đợt nào đã khai là thứ phải NHÌN THẤY — nếu không, lọc theo
    # `--dot` sẽ im lặng bỏ qua nó. Nêu thành PHÁT HIỆN (rc=1), không phải lỗi đầu vào (rc=2): state
    # vẫn hợp lệ, chỉ là hồ sơ chưa sẵn sàng đóng.
    _dot_khai = {str(x.get("dot_id") or "").strip()
                 for x in ((state.get("dot") or []) if isinstance(state, dict) else [])
                 if isinstance(x, dict)} - {""}
    if _dot_khai:
        for _m in ((state.get("q_ingest") or []) if isinstance(state, dict) else []):
            if not isinstance(_m, dict) or str(_m.get("trang_thai") or "") not in _DOT_CHECK_THIEU_TT:
                continue
            _mid = str(_m.get("dot_id") or "").strip()
            # Khi hỏi MỘT Đợt thì chỉ xét mục CỦA Đợt ấy. Bản trước duyệt mọi mục còn treo, nên một
            # mục của `dot-02` sắp mở làm số liệu `dot-01` thành `kha_dung:false` — trái điều kiện
            # đóng (chỉ xét Q-INGEST **thuộc Đợt này**) và biến Đợt khác thành nguồn nhiễu.
            if dot and _mid != dot:
                continue
            if _mid and _mid not in _dot_khai:
                thieu_payload.append({"ma": "DOT_ID_CHUA_KHAI", "dot_id": _mid,
                                      "so_hieu": str(_m.get("so_hieu") or "")})

    # A6: MỌI đơn vị `done` phải có phiếu master — chạy ở cả hai chế độ (xem LỚP D ở trên).
    _co = {str((d or {}).get("unit_id") or "").strip() for _, d in docs}
    for _u in sorted(_done_cua_dot):
        if _u not in _co:
            thieu_payload.append({"unit_id": _u, "ma": "DON_VI_DONE_THIEU_PHIEU_MASTER"})
    for _loai, _muc in (_rasoat_trung_lap(docs) or {}).items():
        for _t in _muc or []:
            thieu_payload.append(dict({"ma": "TRUNG_" + str(_loai).upper()}, **(_t if isinstance(_t, dict) else {"gia_tri": _t})))

    # ② chốt 1 — NFC trước MỌI phép đếm (quét đúng những file mà số liệu được đếm trên đó)
    quet = list(_hop_le)
    for extra in (state_path, so_tra_kho, p / "BANG_MASTER.json", p / "rasoat_bugs.md"):
        if extra.exists():
            quet.append(extra)
    nfc = _dot_check_nfc(quet)

    # ③ chốt 2 — tra kho 3 khoá
    # Sổ tra kho tồn tại để CHỨNG MINH một kết luận «kho thiếu». Không kết luận nào thì không có gì
    # phải chứng minh — đòi sổ khi ấy là CHẶN OAN. Vẫn kiểm đủ khi sổ CÓ MẶT: có mà hỏng thì vẫn ĐỎ.
    if claims or so_tra_kho.exists():
        rows, tra_kho_hong = _tra_kho_doc(so_tra_kho)
    else:
        rows, tra_kho_hong = [], []
    tra_kho = _dot_check_tra_kho(claims, rows)
    tra_kho["so_hong"] = len(tra_kho_hong)
    tra_kho["hong"] = tra_kho_hong
    if tra_kho_hong:
        tra_kho["ok"] = False

    # ④ chốt 3 — số liệu tái lập
    ngay_chot = str(getattr(a, "ngay_chot", "") or "").strip() or str((state or {}).get("cap_nhat") or "").strip()
    # "Đếm trên gì" phải nhận diện được TẬP NGUỒN, không chỉ thư mục: master đổi trong cùng ngày thì
    # cùng đường dẫn + cùng ngày chốt vẫn cho số khác, tức sổ không tái lập được.
    _ten_dem = sorted(n for n, _ in docs)
    _map = dict(docs)
    _bam = hashlib.sha256()
    for _n in _ten_dem:
        _bam.update(_n.encode("utf-8"))
        _bam.update(json.dumps(_map[_n], ensure_ascii=False, sort_keys=True).encode("utf-8"))
    dem_tren = (("%s | %d phiếu: %s | sha256=%s"
                 % (master_dir, len(_ten_dem),
                    ",".join(_ten_dem[:12]) + ("…" if len(_ten_dem) > 12 else ""),
                    _bam.hexdigest()[:16])) if master_dir.is_dir()
                else "(không có thư mục master/)")
    # LỚP A — MỘT vị từ cho MỌI lỗi tính toàn vẹn, thay vì vá từng ca. Ba lượt cross-review liên
    # tiếp ra CÙNG một hình dạng: NFC lệch (F6) · thiếu phiếu/đếm đúp (H2) · master hỏng (#5) — mỗi
    # lần chỉ chặn đúng ca vừa nêu rồi ca kế tiếp lại lọt. Gom vào một danh sách thì nguồn lỗi thứ
    # tư chỉ tốn MỘT DÒNG và tự động chặn; đó là chữa LỚP chứ không chữa CA.
    # ★ BẢNG NÀY LÀ NƠI DUY NHẤT khai "thế nào là tập đếm KHÔNG đáng tin". Thêm tín hiệu toàn vẹn
    # nào sau này thì THÊM MỘT DÒNG VÀO ĐÂY, đừng viết nhánh `if` mới ở chỗ khác. Vì sao nhấn: bản
    # trước cũng TỰ NHẬN là "vá theo LỚP" mà chỉ gom BA tín hiệu tôi đang biết, bỏ quên `dot_loi`/
    # `state_loi` — nên `--dot` sai vẫn công bố `kha_dung:true` với số 0. Lời khai "đã chữa LỚP" khi
    # ấy RỘNG HƠN phép đo; bảng tường minh làm chỗ bỏ quên lộ ra ngay.
    _TIN_HIEU_TOAN_VEN = ((not nfc["ok"], "NFC_CHUA_DAT"),
                          (bool(thieu_payload), "PAYLOAD_KHONG_DAY_DU"),
                          (bool(master_hong), "MASTER_HONG"),
                          (bool(dot_loi), "DOT_KHONG_XAC_DINH"),
                          (bool(state_loi), "STATE_KHONG_HOP_LE"))
    ly_do_khong_dem = [_ma for _dk, _ma in _TIN_HIEU_TOAN_VEN if _dk]
    if not ly_do_khong_dem:
        so_lieu = _dot_check_so_lieu(docs, ngay_chot, dem_tren)
    else:
        # Không đếm khi tập đếm chưa đáng tin: một con số "tái lập được" tính trên tập KHÁC với tập
        # đáng lẽ phải đếm còn tệ hơn không có số. Giữ NGUYÊN hình dạng payload, chỉ khai lý do.
        so_lieu = {"so_lieu": [], "thieu_ngay_chot": not str(ngay_chot or "").strip(),
                   "kha_dung": False, "ly_do": "KHONG_DO_DUOC: " + " · ".join(ly_do_khong_dem),
                   "ok": False}
    so_lieu.setdefault("kha_dung", True)

    findings = (len(nfc["lech"]) + len(tra_kho["phat_hien"]) + len(tra_kho_hong)
                + len(master_hong) + len(thieu_payload) + (1 if so_lieu["thieu_ngay_chot"] else 0)
                + (0 if so_lieu.get("kha_dung", True) else 1))
    # ★ `--strict` gộp rc=1 và rc=2 làm một, mà workflow lại BẮT chạy `--strict` ⇒ đọc theo rc thì
    # đường đóng HẠN CHẾ biến mất (rc=2 bị luật đóng coi là "chưa đo được gì"). Sửa ở chỗ đúng:
    # khai TƯỜNG MINH loại verdict, để người đọc quyết theo NGUYÊN NHÂN chứ không theo mã thoát.
    #   `do_duoc`        — đã đo xong, có/không phát hiện: `co_the_dong_han_che` = True
    #   `khong_do_duoc`  — state hỏng hoặc `--dot` không giải được: CHẶN CỨNG, không miễn trừ
    _khong_do = bool(state_loi or dot_loi) or not so_lieu.get("kha_dung", True)
    payload = {"schema": _DOT_CHECK_SCHEMA, "in": str(p), "dot": dot or None,
               "dot_loi": dot_loi or None,
               "loai_verdict": "khong_do_duoc" if _khong_do else "do_duoc",
               "co_the_dong_han_che": not _khong_do,
               "ok": findings == 0 and not state_loi and not dot_loi,
               "state": {"file": str(state_path), "loi": state_loi or None},
               "chot_1_nfc": nfc, "chot_2_tra_kho": tra_kho, "chot_3_so_lieu": so_lieu,
               "master_hong": master_hong, "thieu_payload": thieu_payload,
               "so_phat_hien_cong": findings,
               "fix": "NFC lệch ⇒ chuẩn hoá nguồn rồi đếm lại; thiếu khoá ⇒ tra nốt khoá còn thiếu "
                      "TRƯỚC khi kết luận thiếu; thiếu ngày chốt ⇒ khai `--ngay-chot`"}
    out = str(getattr(a, "out", "") or "").strip()
    if out:
        # Seam canonical (`release.py::_write_text_atomic`): tạo thư mục cha, UTF-8+LF bất kể OS,
        # ghi tmp cùng thư mục rồi `os.replace`. `write_text` trần: thiếu cha ⇒ FileNotFoundError,
        # ngắt giữa chừng ⇒ tệp CỤT, Windows còn dính CRLF — ba đường hỏng cho một dòng.
        _o = Path(out).resolve()
        try:
            _trong_in = _o.is_relative_to(p.resolve())
        except Exception:  # noqa: BLE001 — Python cũ / đường dẫn lạ
            _trong_in = str(_o).startswith(str(p.resolve()))
        if _trong_in:
            # Lệnh tự khai READ-ONLY với hồ sơ rà. `--out` trỏ vào chính `<in>` phá lời khai ấy —
            # tệ nhất là trỏ thẳng `rasoat_state.json` rồi thay state bằng payload NGAY SAU khi
            # vừa đọc nó. Từ chối, đừng ghi rồi mới giải thích.
            payload["out_loi"] = ("OUT_TRONG_IN: --out không được nằm trong --in "
                                  "(lệnh READ-ONLY với hồ sơ rà)")
            _print_json_or_text(payload, True)
            return 2
        try:
            _write_text_atomic(_o, _json_dumps(payload) + "\n")
        except Exception as _e:  # noqa: BLE001 — hỏng đường ghi là LỖI LỆNH, không phải traceback
            payload["out_loi"] = "OUT_GHI_HONG: " + str(_e)
            _print_json_or_text(payload, True)
            return 2
        payload["out"] = out
    _print_json_or_text(payload, True)
    # đầu vào KHÔNG ĐO ĐƯỢC (state hỏng · `--dot` không ánh xạ được) = LỖI LỆNH rc=2, khác hẳn
    # rc=1 "có phát hiện" — trộn hai thứ là biến một phép đo bất khả thi thành một verdict dữ liệu.
    if state_loi or dot_loi or (findings and bool(getattr(a, "strict", False))):
        return 2
    return 1 if findings else 0
