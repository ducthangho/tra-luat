# -*- coding: utf-8 -*-
"""Sinh tệp ma trận N4 (SECRETS-SET-BUNDLE-KIEU r5 §4 quy tắc 4) TRƯỚC khi chạy rig.
Tập đích mỗi đột biến dựng từ CƠ CHẾ (đọc `_secrets_set_body` của ứng viên), KHÔNG đọc bản đồ đo được.
Cách dùng: python sinh_ma_tran.py > ma-tran-n4.json"""
import json, sys
T5 = ("list", "str", "int", "null", "true")
C5 = ("gas_token", "webapp", "gws", "nlm", "khong_co")
TOK = tuple("%s.%s" % (k, c) for k in ("list", "dict", "int") for c in ("gws", "nlm"))
HQ = ("gas_token", "webapp", "gws", "nlm", "khong_co", "env_token.gws")
HQ5 = tuple(h for h in HQ if h != "khong_co")               # 5 lượt đi tới upload/cuối hàm
QK = ("rc3", "dong", "fetch1", "upload0", "stage_enc0", "gws_export0", "nlm_refresh0", "canary0", "gas0", "encrypt0")
QT = ("rc0", "upload1", "stage_enc0", "khoa_public_rong", "canh_bao_co", "khong_dong_loi")
QH = ("rc", "fetch", "gas", "upload", "stage_enc", "gws_export", "nlm_refresh", "canary", "encrypt", "khoa_public")
DANH_MUC = sorted(["kieu.%s.%s.%s" % (t, c, q) for t in T5 for c in C5 for q in QK] + ["token_kieu.%s.%s" % (l, q) for l in TOK for q in QT]
                  + ["hoi_quy.%s.%s" % (l, q) for l in HQ for q in QH])
assert len(DANH_MUC) == 346
def k(*xs): return ["kieu.%s.%s.%s" % x for x in xs]
def kieu_all(q): return k(*((t, c, q) for t in T5 for c in C5))
def tok(*qs): return ["token_kieu.%s.%s" % (l, q) for l in TOK for q in qs]
def hq(luot, *qs): return ["hoi_quy.%s.%s" % (l, q) for l in luot for q in qs]
def bo_kiem(ts):
    # M1 vắng ⇒ bundle không phải dict đi tiếp: gas_token/webapp: TypeError ở câu gán đầu ⇒ rc 5, dòng `dừng vì lỗi`;
    # gws: export (đếm 1) rồi TypeError; nlm: refresh + canary (đếm 1) rồi TypeError; khong_co: `không có trường nào` rc 1.
    out = []
    for t in ts:
        out += k((t, "gas_token", "rc3"), (t, "gas_token", "dong"), (t, "webapp", "rc3"), (t, "webapp", "dong"),
                 (t, "khong_co", "rc3"), (t, "khong_co", "dong"), (t, "gws", "rc3"), (t, "gws", "dong"), (t, "gws", "gws_export0"),
                 (t, "nlm", "rc3"), (t, "nlm", "dong"), (t, "nlm", "nlm_refresh0"), (t, "nlm", "canary0"))
    return out
M1_NEU = "    if not isinstance(bundle, dict):   # WP433 SS: không phải object ⇒ từ chối như giải mã lỗi, TRƯỚC mọi cờ/export/canary\n"
M1_IN = '        print("[secrets-set] ✗ dữ liệu không hợp lệ: bundle", file=sys.stderr)\n'
M1 = M1_NEU + M1_IN + "        return 3\n"
M2 = '_tok = os.environ.get("TL_TOKEN") or (_bt if isinstance(_bt, str) else "")'
FETCH = "    blob, _src = _secrets_fetch(a, fid)\n"
CHANGED = "    changed = []\n    nlm_confirmed = None\n    if getattr(a, \"gas_token\", None):\n"
KHONG_CO = '        print("[secrets-set] ⚠ không có trường nào để đổi (--gas-token/--webapp/--gws/--nlm).", file=sys.stderr)\n        return 1\n'
UPLOAD = '    _secrets_upload(new, getattr(a, "folder", None) or HOPNAP_FOLDER_ID, fid)\n'
CUOI = "public cũng tươi.\")\n    return 0\n"
CANH_BAO = 'print("[secrets-set] ⚠ thiếu webapp token'
VAO = '    _entry_nb = os.environ.get("TL_NOTEBOOK_ID")      # WP714: ghim TRƯỚC load_creds của lệnh\n    return _nlm_contained("secrets-set"'
GHI = '            self.ban_do["%s.%s" % (luot, k)] = v is True\n'
STAGE_GIA = '_stage_enc_upload("x", store.encrypt(b"", "k-wp433"), None, None, False)'
def m1_chen(stmt): return [[M1, M1_NEU + M1_IN + "        " + stmt + "\n        return 3\n"]]
def sau_changed(stmt): return [[CHANGED, "    changed = []\n    " + stmt + "\n" + CHANGED[len("    changed = []\n"):]]]
DB = []
def them(ten, nhom, cap, dich, mong="GIET", co_che=None, cap_fragment=(), nguon="ung_vien", ly_do=""):
    DB.append(dict(ten=ten, nhom=nhom, nguon=nguon, cap=cap, cap_fragment=list(cap_fragment), dich=sorted(set(dich)), co_che_luot=co_che,
                   mong=mong, ly_do=ly_do))
# --- (ii) bốn đột biến r1
them("db_bo_kiem_kieu", "dot_bien", [[M1, ""]], bo_kiem(T5), co_che="kieu.list.gas_token", ly_do="bỏ M1")
them("db_kieu_chi_list", "dot_bien", [[M1_NEU, M1_NEU.replace("isinstance(bundle, dict)", "isinstance(bundle, (dict, str))")]], bo_kiem(["str"]),
     co_che="kieu.str.gas_token", ly_do="M1 để lọt str")
them("db_kieu_thong_diep", "dot_bien", [[M1_IN, M1_IN.replace("dữ liệu không hợp lệ: bundle", "giải mã lỗi: bundle")]], kieu_all("dong"),
     ly_do="sai thông điệp: chỉ dòng stderr")
them("db_token_repr", "dot_bien", [[M2, '_tok = os.environ.get("TL_TOKEN") or str(bundle.get("token") or "")']],
     tok("stage_enc0", "khoa_public_rong", "canh_bao_co"),
     ly_do="khoá public = repr ⇒ có đồng bộ public: stage 1, encrypt với khoá repr, không cảnh báo; rc/upload/không ✗ giữ")
# --- (iii) PC1, PC2 của r1
them("pc1_dong_stderr_thua", "dot_bien", [[M1_IN, M1_IN + '        print("[secrets-set] xem thêm", file=sys.stderr)\n']], kieu_all("dong"))
them("pc2_export_truoc_tu_choi", "dot_bien", [[M1_NEU, M1_NEU + '        if getattr(a, "gws", False):\n            _gws_export_cred()\n']],
     k(*((t, "gws", "gws_export0") for t in T5)))
# --- (i) phủ phần còn lại của danh mục: tác dụng phụ trong nhánh từ chối M1 (mọi lượt kieu)
for q, stmt in (("upload0", '_secrets_upload(b"", None, fid)'), ("stage_enc0", '_stage_enc_upload("x", b"", None, None, False)'),
                ("encrypt0", 'store.encrypt(b"", master)'), ("gws_export0", "_gws_export_cred()"), ("nlm_refresh0", "_refresh_nlm_auth()"),
                ("canary0", '_nlm_files_after_live_canary("secrets-set", entry_notebook)')):
    them("db_m1_" + q, "dot_bien", m1_chen(stmt), kieu_all(q))
# trước giải mã: chạy ở MỌI lượt (kieu + hoi_quy có khoá fetch/gas; token_kieu không có)
them("db_fetch_hai_lan", "dot_bien", [[FETCH, FETCH + "    _secrets_fetch(a, fid)\n"]], kieu_all("fetch1") + hq(HQ, "fetch"))
them("db_gas_goi_thu", "dot_bien", [[FETCH, FETCH + '    try:\n        _gas("wp433")\n    except Exception:\n        pass\n']],
     kieu_all("gas0") + hq(HQ, "gas"))
# sau M1, ngay sau `changed = []`: mọi lượt hoi_quy (+token_kieu, không có khoá tương ứng)
them("db_sau_changed_gws_export", "dot_bien", sau_changed("_gws_export_cred()"), hq(HQ, "gws_export"))
them("db_sau_changed_nlm_refresh", "dot_bien", sau_changed("_refresh_nlm_auth()"), hq(HQ, "nlm_refresh"))
them("db_sau_changed_canary", "dot_bien", sau_changed('_nlm_files_after_live_canary("secrets-set", entry_notebook)'), hq(HQ, "canary"))
# khong_co (hoi_quy): bỏ `return 1` ⇒ guard qua, encrypt 1, upload 1, rc 0 (public: changed rỗng ⇒ không stage)
them("db_bo_tra_1", "dot_bien", [[KHONG_CO, KHONG_CO.replace("        return 1\n", "        pass\n")]], hq(["khong_co"], "rc", "upload", "encrypt"))
them("db_khong_co_stage", "dot_bien", [[KHONG_CO, KHONG_CO.replace("        return 1\n", "        " + STAGE_GIA + "\n        return 1\n")]],
     hq(["khong_co"], "stage_enc", "encrypt", "khoa_public"))
them("db_upload_hai_lan", "dot_bien", [[UPLOAD, UPLOAD + UPLOAD]], tok("upload1") + hq(HQ5, "upload"))
them("db_rc_cuoi", "dot_bien", [[CUOI, CUOI.replace("return 0", "return 7")]], tok("rc0") + hq(HQ5, "rc"))
them("db_stage_cuoi", "dot_bien", [[CUOI, CUOI.replace("    return 0\n", "    " + STAGE_GIA + "\n    return 0\n")]],
     tok("stage_enc0", "khoa_public_rong") + hq(HQ5, "stage_enc", "encrypt", "khoa_public"))
them("db_canh_bao_thanh_loi", "dot_bien", [[CANH_BAO, CANH_BAO.replace("⚠", "✗")]], tok("khong_dong_loi"),
     ly_do="dòng cảnh báo mang ✗: vẫn đúng một dòng `thiếu webapp token`")
# --- năm tự kiểm của bộ phân hạng (kết quả kỳ vọng riêng)
RC_DONG = kieu_all("rc3") + kieu_all("dong")
them("tk_a_attributeerror", "tu_kiem", [[M1, M1_NEU + '        raise AttributeError("wp433-tu-kiem")\n']], RC_DONG, mong="TIN_DUNG_GIA",
     co_che="kieu.list.gas_token", ly_do="rc 5 vì AttributeError: sai cơ chế")
them("tk_a2_typeerror_vo_can", "tu_kiem", [[M1, M1_NEU + "        len(7)\n"]], RC_DONG, mong="TIN_DUNG_GIA", co_che="kieu.list.gas_token",
     ly_do="TypeError nhưng sai vị trí frame")
them("tk_b_except_doi_kieu", "tu_kiem", [[VAO, "    try:\n        os.environ.wp433_khong_co\n    except AttributeError as e:\n"
                                           "        raise AssertionError(type(e).__name__)\n" + VAO]], DANH_MUC, mong="TIN_DUNG_GIA",
     ly_do="AssertionError văng khỏi lệnh ⇒ bản đồ thiếu khoá")
them("tk_c_chu_thich", "tu_kiem", [[M1_NEU, "    # vô hại\n" + M1_NEU]], bo_kiem(T5), mong="SONG_SOT")
them("tk_d_ep_xanh", "tu_kiem", [[M1, ""]], bo_kiem(T5), mong="LECH_TAP", co_che="kieu.list.gas_token",
     cap_fragment=[[GHI, GHI.replace("v is True", 'v is True or "%s.%s" % (luot, k) == "kieu.list.gws.gws_export0"')]],
     ly_do="dưới db_bo_kiem_kieu, fragment ép kieu.list.gws.gws_export0 thành True ⇒ so tập ĐỎ")
# --- đo nền (không tính phủ): ứng viên nguyên vẹn; nguồn tl_gws.py của base trong fragment ứng viên
them("do_ung_vien", "do_nen", [], [], mong="SONG_SOT")
them("do_nen_tl_gws_base", "do_nen", [], bo_kiem(T5) + tok("stage_enc0", "khoa_public_rong", "canh_bao_co"), nguon="base",
     ly_do="base = thiếu M1 và M2: đỏ N1 (65 khoá) + N2 (18 khoá), N3 xanh")
json.dump(dict(spec="SECRETS-SET-BUNDLE-KIEU-r5", danh_muc=DANH_MUC, dot_bien=DB), sys.stdout, ensure_ascii=False, indent=1, sort_keys=True)
