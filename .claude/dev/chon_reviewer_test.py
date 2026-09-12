#!/usr/bin/env python3
"""Phan chung #351: chay toan bang; nen do thi tu choi cong bo diem dot bien."""
from __future__ import annotations
import contextlib, importlib, importlib.util, io, itertools, json, sys, tempfile
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
MA = HERE / "chon_reviewer.py"
BAC = (("claude-opus-5", "high"), ("claude-opus-5", "xhigh"),
       ("claude-fable-5", "xhigh"), ("claude-fable-5", "max"))
def _nap(path=MA, nhan="nen"):
    importlib.invalidate_caches()
    sp = importlib.util.spec_from_file_location("tl351_" + nhan, str(path)); m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m
def _doi_loi(m, ham, *args):
    try: ham(*args)
    except m.KhongDoDuoc as exc: return str(exc)
    raise AssertionError("đầu vào không đo được nhưng không bị từ chối: %r" % (args,))
def _bac(m, review_class, paths, so_dong=0, luot=1, bac_truoc=None):
    return m.chon(review_class, paths, so_dong, luot, bac_truoc)[:2]
def _cli(m, *args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = m.main(list(args))
    return rc, out.getvalue(), err.getvalue()
def r01_bon_bac_biet_truoc(m):
    for path in ("scripts/tl.py", ".claude/dev/x.py", "ops/x.py",
                 "references/x.txt", "README.md"):
        if _bac(m, "routine", [path]) != BAC[0]: raise AssertionError("điểm 0 sai cho vùng đã biết: %s" % path)
    mot_diem = [
        _bac(m, "routine", ["docs/adr/0001-x.md"]),
        _bac(m, "routine", ["scripts/x.py"], so_dong=400),
        _bac(m, "routine", ["scripts/x.py"], luot=3),
        _bac(m, "routine", ["scripts/%d.py" % i for i in range(5)]),
    ]
    if any(x != BAC[1] for x in mot_diem): raise AssertionError("một khoản +1 không cho bậc điểm 1–2: %r" % mot_diem)
    if _bac(m, "routine", [".github/workflows/ci.yml"]) != BAC[1]: raise AssertionError("vùng cong +2 không cho đúng bậc")
    if _bac(m, "sensitive", [".claude/skills/x/SKILL.md"]) != BAC[2]: raise AssertionError("điểm 3 không cho fable/xhigh")
    nam_tep = [".github/workflows/ci.yml"] + ["scripts/%d.py" % i for i in range(4)]
    kq = m.chon("sensitive", nam_tep, 0, 1)
    if kq[:2] != BAC[3] or "bậc cuối=claude-fable-5/max" not in kq[2]: raise AssertionError("điểm 5 hoặc giải thích bậc cuối sai: %r" % (kq,))
def r02_khong_biet_day_len_cao_nhat(m):
    kq = m.chon("sensitive", ["vi-du/la.txt"], 0, 1)
    if kq[:2] != BAC[3] or "+3 chạm vùng khong-biet" not in kq[2]: raise AssertionError("đường lạ không fail-close lên bậc cao nhất: %r" % (kq,))
def r03_banh_coc_hai_chieu(m):
    giu = _bac(m, "routine", ["scripts/x.py"], bac_truoc=BAC[3])
    if giu != BAC[3]: raise AssertionError("bậc trước cao hơn đã bị tụt: %r" % (giu,))
    nam_tep = [".github/workflows/ci.yml"] + ["scripts/%d.py" % i for i in range(4)]
    khong_keo = _bac(m, "sensitive", nam_tep, bac_truoc=BAC[0])
    if khong_keo != BAC[3]: raise AssertionError("bậc trước thấp kéo kết quả mới xuống: %r" % (khong_keo,))
def r04_dinh_danh_allow_list(m):
    for alias in ("opus", "fable", "sonnet"):
        _doi_loi(m, m.kiem_dinh_danh, alias, "high")
    m.kiem_dinh_danh("claude-opus-5", "high")
    _doi_loi(m, m.kiem_dinh_danh, "claude-opus-5", "khong-ton-tai")
# Giu du 9 nhan cua hai rig de mot rig khong bi rut khoi phep do.
PHU = "claude-haiku-4-5-20251001"
def _ket_qua(loi, *models):
    return {"subtype": "success", "is_error": loi,
            "modelUsage": {x: {"canonicalModel": x.rsplit("-", 1)[0] if x == PHU else x} for x in models}}
FIXTURE = (
    ("trống/opus", "claude-opus-5", _ket_qua(False, "claude-opus-5"), True),
    ("trống/fable", "claude-fable-5", _ket_qua(False, "claude-fable-5"), True),
    ("trống/model-rác", "claude-khong-ton-tai-9", _ket_qua(True), False),
    ("kho/opus/không-tool", "claude-opus-5", _ket_qua(False, PHU, "claude-opus-5"), True),
    ("kho/opus/có-tool", "claude-opus-5", _ket_qua(False, PHU, "claude-opus-5"), True),
    ("kho/fable/không-tool", "claude-fable-5", _ket_qua(False, "claude-fable-5", PHU), True),
    ("kho/fable/có-tool", "claude-fable-5", _ket_qua(False, "claude-fable-5", PHU), True),
    ("kho/sonnet/không-tool", "claude-sonnet-5", _ket_qua(False, PHU, "claude-sonnet-5"), True),
    ("kho/model-rác", "claude-khong-ton-tai-9", _ket_qua(True, PHU), False),
)
def r05_chin_fixture_hai_rig(m):
    if len(FIXTURE) != 9: raise AssertionError("bảng fixture không còn đủ 9 bản ghi: %d" % len(FIXTURE))
    for nhan, model, du_lieu, phai_dat in FIXTURE:
        loi = ""
        try:
            thong_bao = m.kiem_ket_qua(model, du_lieu)
            dat = True
        except m.KhongDoDuoc as exc:
            dat = False
            loi = str(exc)
        if dat != phai_dat: raise AssertionError("fixture %s: nhận %s, mong %s" % (nhan, dat, phai_dat))
        if dat and len(du_lieu["modelUsage"]) > 1 and PHU not in thong_bao: raise AssertionError("fixture %s không kể khoá phụ trong thông báo" % nhan)
        if nhan == "kho/model-rác" and "model yêu cầu" not in loi: raise AssertionError("fixture model rác bị chặn sai nhánh: %r" % loi)
def r06_json_mo_ho_phai_do(m):
    thieu_is_error = {"modelUsage": {"claude-opus-5": {"canonicalModel": "claude-opus-5"}}}
    for x in (None, [], {}, {"is_error": False, "modelUsage": {}},
              thieu_is_error,
              {"is_error": False, "modelUsage": {"claude-fable-5": {"canonicalModel": "claude-fable-5"}}}):
        _doi_loi(m, m.kiem_ket_qua, "claude-opus-5", x)
    m.kiem_ket_qua("claude-opus-5", {"is_error": False, "modelUsage": {"claude-opus-5-20260827": {"canonicalModel": "claude-opus-5"}}})
    _doi_loi(m, m.kiem_ket_qua, "claude-opus-5", {"is_error": False, "modelUsage": {"id-theo-ngay": {"canonicalModel": "claude-fable-5"}}})
def r13_tut_giua_chung_bi_chan(m):
    du_lieu = _ket_qua(False, "claude-fable-5", "claude-opus-4-8")
    try:
        m.kiem_ket_qua("claude-fable-5", du_lieu)
    except m.KhongDoDuoc as exc:
        if "mô hình LẠ" not in str(exc): raise AssertionError("tụt giữa chừng bị chặn sai nhánh: %s" % exc)
        return
    raise AssertionError("tụt giữa chừng mang hai model chính vẫn ĐẠT")
def r14_khong_co_model_phu_van_dat(m):
    thong_bao = m.kiem_ket_qua("claude-fable-5", _ket_qua(False, "claude-fable-5"))
    if "mô hình phụ bỏ qua=[]" not in thong_bao: raise AssertionError("lượt không có model phụ không được báo đúng: %r" % thong_bao)
def r07_don_dieu_moi_to_hop(m):
    vung = (".github/workflows/ci.yml", "docs/adr/x.md", "scripts/x.py", ".claude/dev/x.py", "references/x.txt", "vi-du/la.txt")
    def ds(path, nhieu):
        return [path] + (["scripts/phu-%d.py" % i for i in range(4)] if nhieu else [])
    for review_class, path, nhieu, dai, muon in itertools.product(
            ("routine", "systemic", "sensitive"), vung, (False, True), (False, True), (False, True)):
        args = (ds(path, nhieu), 400 if dai else 399, 3 if muon else 2)
        hien_tai = BAC.index(_bac(m, review_class, *args))
        cac_ban_them = [_bac(m, "sensitive", *args), _bac(m, review_class, ds(path, True), args[1], args[2]),
                        _bac(m, review_class, args[0], 400, args[2]), _bac(m, review_class, args[0], args[1], 3)]
        if any(BAC.index(x) < hien_tai for x in cac_ban_them): raise AssertionError("thêm khoản điểm làm tụt bậc: %r" % ((review_class,) + args,))
        co_so = BAC.index(_bac(m, review_class, ds("scripts/co-so.py", nhieu), args[1], args[2]))
        if hien_tai < co_so: raise AssertionError("đổi từ vùng 0 điểm sang %s làm tụt bậc" % path)
def r08_review_class_allow_list(m):
    for x in ("sensitve", "SENSITIVE", None):
        _doi_loi(m, m.chon, x, ["scripts/x.py"], 0, 1)
    for x in ("routine", "systemic", "sensitive"):
        m.chon(x, ["scripts/x.py"], 0, 1)
    if _bac(m, " sensitive ", ["scripts/x.py"]) != BAC[1]: raise AssertionError("review_class hợp lệ sau strip bị từ chối")
def r09_write_set_rong_khong_do_duoc(m):
    for x in ([], "", (), [" ", ""]):
        _doi_loi(m, m.chon, "routine", x, 0, 1)
def r10_so_am_khong_phai_pham_vi_nho(m):
    for so_dong, luot in ((-999, 1), (0, -5), (0, 0), (1.5, 1), (0, True)):
        _doi_loi(m, m.chon, "routine", ["scripts/x.py"], so_dong, luot)
    m.chon("routine", ["scripts/x.py"], 0, 1)
def r11_systemic_cong_mot_diem(m):
    kq = m.chon("systemic", ["scripts/x.py"], 0, 1)
    if kq[:2] != BAC[1] or "+1 review_class=systemic" not in kq[2]: raise AssertionError("systemic không cộng đúng +1: %r" % (kq,))
def r12_effective_khong_duoc_ha_lop(m):
    lease = {"review_class": "sensitive", "effective_review_class": "routine"}
    if _bac(m, lease, ["scripts/x.py"]) != BAC[1]: raise AssertionError("effective thấp hơn đã hạ lớp khai báo")
def r15_backslash_bi_tu_choi(m):
    path = "la\\la.md"
    if "backslash" not in _doi_loi(m, m.chon, "routine", [path], 0, 1): raise AssertionError("đường chứa backslash không bị từ chối đích danh")
def r16_bang_vung_r6_va_nhan_planned(m):
    bang = {".github/checks/x.py": "cong", ".claude/settings.json": "cong",
            "RELEASE_MANIFEST.json": "cong", ".claude/agents/x.md": "giao-thuc",
            "docs/PROTOCOL_DA_PHIEN.md": "giao-thuc", "docs/adr/x.md": "giao-thuc",
            ".gitignore": "dev", "docs/x.md": "tai-lieu"}
    sai = {x: m._vung(x) for x, v in bang.items() if m._vung(x) != v}
    if sai: raise AssertionError("bảng vùng r6 sai: %r" % sai)
    if m._cac_duong_dan(["planned:ops/x.sh", "ops/x.sh"]) != ("ops/x.sh",): raise AssertionError("nhãn planned: chưa được bóc trước phân loại/dedup")
    if "khong-biet" in m.chon("routine", ["planned:ops/x.sh"], 0, 1)[2]: raise AssertionError("planned:ops/x.sh bị tính như đường lạ")
def r17_cli_khong_hoan_vi_so_dong_luot(m):
    rc, out, _ = _cli(m, "--review-class", "routine", "--duong-dan", "scripts/x.py", "--so-dong", "398", "--luot", "1", "--json")
    if rc or (json.loads(out)["model"], json.loads(out)["effort"]) != BAC[0]: raise AssertionError("CLI hoán vị so_dong/luot hoặc không trả JSON đúng")
def r18_cli_bac_truoc_fail_close(m):
    co_so = ("--review-class", "routine", "--duong-dan", "scripts/x.py", "--so-dong", "1", "--luot", "1", "--json")
    rc, out, _ = _cli(m, *co_so, "--bac-truoc", "claude-fable-5,max")
    if rc or (json.loads(out)["model"], json.loads(out)["effort"]) != BAC[3]: raise AssertionError("CLI bỏ qua bánh cóc")
    for x in ("claude-fable-5", "la,max", "claude-fable-5,la"):
        rc, _, err = _cli(m, *co_so, "--bac-truoc", x)
        if rc != 2 or "KHÔNG ĐO ĐƯỢC" not in err: raise AssertionError("--bac-truoc sai không fail-close: %r" % x)
def r19_dinh_danh_phai_khop_bang_nhau(m):
    for usage in ({"claude-opus-5x": {}}, {"id": {"canonicalModel": "claude-opus-5x"}}):
        _doi_loi(m, m.kiem_ket_qua, "claude-opus-5", {"is_error": False, "modelUsage": usage})
def r20_dict_chi_review_class_van_chay(m):
    if _bac(m, {"review_class": "sensitive"}, ["scripts/x.py"]) != BAC[1]: raise AssertionError("dict chỉ có review_class mất nhánh fallback")
def r21_ghim_bien_duoi_tuyet_doi(m):
    ca = [_bac(m, "routine", ["scripts/x.py"], 399, 1),
          _bac(m, "routine", ["scripts/%d.py" % i for i in range(4)], 0, 1),
          _bac(m, "routine", ["scripts/x.py"], 0, 2),
          _bac(m, "sensitive", [".github/workflows/ci.yml"], 0, 1)]
    if ca != [BAC[0], BAC[0], BAC[0], BAC[2]]: raise AssertionError("biên dưới ngưỡng không được ghim tuyệt đối: %r" % ca)
def r22_duong_khong_chuan_va_planned_lap(m):
    for path, chuan in (("ops//lease_publish.py", "ops/lease_publish.py"), ("a/./b", "a/b"), ("a/../b", "b")):
        loi = _doi_loi(m, m.chon, "routine", [path], 0, 1)
        if "bản chuẩn" not in loi or chuan not in loi: raise AssertionError("đường không chuẩn thiếu bản chuẩn: %r -> %r" % (path, loi))
    for path in ("/tuyet-doi", "planned:planned:ops/x.sh"):
        _doi_loi(m, m.chon, "routine", [path], 0, 1)
def r23_nhan_thu_muc_chi_boc_mot_slash(m):
    if m._cac_duong_dan(["ops/reviews/"]) != ("ops/reviews",): raise AssertionError("nhãn thư mục một slash cuối bị từ chối")
    _doi_loi(m, m.chon, "routine", ["ops/reviews//"], 0, 1)
def r24_cli_effective_leo_lop(m):
    rc, out, _ = _cli(m, "--review-class", "routine", "--effective-review-class", "sensitive", "--duong-dan", "scripts/x.py", "--so-dong", "0", "--luot", "1", "--json")
    if rc or (json.loads(out)["model"], json.loads(out)["effort"]) != BAC[1]: raise AssertionError("CLI không lấy lớp cao hơn giữa review_class và effective")
def r25_hop_dong_loi_api(m):
    _doi_loi(m, m.kiem_ket_qua, "claude-opus-5", {"is_error": False, "modelUsage": {None: {}}})
    _doi_loi(m, m.chon, "routine", ["scripts/x.py"], 0, 1, ("claude-opus-5",))
def r26_duong_dan_bi_chan_nham(m):
    for path in ("..foo.py", "..a/b.py", "...x", "..ops/x.py"):
        if m._chuan_hoa_duong(path) != path: raise AssertionError("bị stripped: %s" % path)
        if _bac(m, "routine", [path]) != BAC[2]: raise AssertionError("không thành khong-biet: %s" % path)
    if m._chuan_hoa_duong("ops/..bar.md") != "ops/..bar.md": raise AssertionError("bị stripped: ops/..bar.md")
    if _bac(m, "routine", ["ops/..bar.md"]) != BAC[0]: raise AssertionError("ops/..bar.md sai điểm")
def r27_duong_dan_thoat_repo(m):
    for path in ("..", "../x", "../../etc/passwd", "ops/../../x"):
        _doi_loi(m, m.chon, "routine", [path], 0, 1)
def r28_so_bang_nhau_exact_match(m):
    kq1 = m.chon("routine", [".claude/settings.json"], 0, 1)
    if "chạm vùng cong" not in kq1[2]: raise AssertionError("sai vùng .claude/settings.json")
    if m._vung(".claude/settings.json") != "cong": raise AssertionError(".claude/settings.json không là cong")
    kq2 = m.chon("routine", ["RELEASE_MANIFEST.json"], 0, 1)
    if "chạm vùng cong" not in kq2[2]: raise AssertionError("sai vùng RELEASE_MANIFEST.json")
    if m._vung("RELEASE_MANIFEST.json") != "cong": raise AssertionError("RELEASE_MANIFEST.json không là cong")
    kq3 = m.chon("routine", ["docs/PROTOCOL_DA_PHIEN.md"], 0, 1)
    if "chạm vùng giao-thuc" not in kq3[2]: raise AssertionError("sai vùng docs/PROTOCOL_DA_PHIEN.md")
    if m._vung("docs/PROTOCOL_DA_PHIEN.md") != "giao-thuc": raise AssertionError("docs/PROTOCOL_DA_PHIEN.md không là giao-thuc")
    kq4 = m.chon("routine", [".gitignore"], 0, 1)
    if "khong-biet" in kq4[2] or "cong" in kq4[2] or "giao-thuc" in kq4[2]: raise AssertionError("sai vùng .gitignore")
    if m._vung(".gitignore") != "dev": raise AssertionError(".gitignore không là dev")
    if m._vung("tmp/.claude/settings.json.bak") != "khong-biet": raise AssertionError("tmp/.claude/settings.json.bak không là khong-biet")
    if m._vung("x/RELEASE_MANIFEST.json") != "khong-biet": raise AssertionError("x/RELEASE_MANIFEST.json không là khong-biet")
    if m._vung("docs/PROTOCOL_DA_PHIEN.md.orig") != "tai-lieu": raise AssertionError("docs/PROTOCOL_DA_PHIEN.md.orig không là tai-lieu")
    if m._vung("vendor/.gitignore") != "khong-biet": raise AssertionError("vendor/.gitignore không là khong-biet")
    if m._vung("a/b/.claude/settings.json") != "khong-biet": raise AssertionError("a/b/.claude/settings.json không là khong-biet")
    if m._vung("ops/RELEASE_MANIFEST.json.tmp") != "dev": raise AssertionError("ops/RELEASE_MANIFEST.json.tmp không là dev")

CA = [(h.__name__, h) for h in (r01_bon_bac_biet_truoc, r02_khong_biet_day_len_cao_nhat, r03_banh_coc_hai_chieu,
    r04_dinh_danh_allow_list, r05_chin_fixture_hai_rig, r06_json_mo_ho_phai_do, r07_don_dieu_moi_to_hop,
    r08_review_class_allow_list, r09_write_set_rong_khong_do_duoc, r10_so_am_khong_phai_pham_vi_nho,
    r11_systemic_cong_mot_diem, r12_effective_khong_duoc_ha_lop, r13_tut_giua_chung_bi_chan,
    r14_khong_co_model_phu_van_dat, r15_backslash_bi_tu_choi, r16_bang_vung_r6_va_nhan_planned,
    r17_cli_khong_hoan_vi_so_dong_luot, r18_cli_bac_truoc_fail_close, r19_dinh_danh_phai_khop_bang_nhau,
    r20_dict_chi_review_class_van_chay, r21_ghim_bien_duoi_tuyet_doi, r22_duong_khong_chuan_va_planned_lap,
    r23_nhan_thu_muc_chi_boc_mot_slash, r24_cli_effective_leo_lop, r25_hop_dong_loi_api,
    r26_duong_dan_bi_chan_nham, r27_duong_dan_thoat_repo, r28_so_bang_nhau_exact_match)]
def _db(tim, thay, *dich): return tim, thay, list(dich)
DOT_BIEN = {
    "bo_nhanh_khong_biet": _db('    if "khong-biet" in cac_vung: cong(3, "chạm vùng khong-biet")', '    if "khong-biet" in cac_vung: pass', "r02_khong_biet_day_len_cao_nhat", "r26_duong_dan_bi_chan_nham"),
    "bo_banh_coc": _db("        if truoc > chi_so:", "        if False and truoc > chi_so:", "r03_banh_coc_hai_chieu", "r18_cli_bac_truoc_fail_close"),
    "nhan_bi_danh": _db('MO_HINH_CHO_PHEP = ("claude-opus-5", "claude-fable-5")', 'MO_HINH_CHO_PHEP = ("claude-opus-5", "claude-fable-5", "opus", "fable", "sonnet")', "r04_dinh_danh_allow_list"),
    "tin_subtype_success": _db('    model_usage = ket_qua_json.get("modelUsage")', '    if ket_qua_json.get("subtype") == "success":\n        return "modelUsage: ĐẠT (đột biến tin subtype)"\n    model_usage = ket_qua_json.get("modelUsage")', "r05_chin_fixture_hai_rig", "r13_tut_giua_chung_bi_chan", "r14_khong_co_model_phu_van_dat"),
    "doi_modelUsage_thanh_dung_mot_khoa": _db('    def danh_tinh(ten, thong_tin):', '    if len(model_usage) != 1:\n        raise KhongDoDuoc("đột biến đòi đúng một khoá")\n    def danh_tinh(ten, thong_tin):', "r05_chin_fixture_hai_rig", "r13_tut_giua_chung_bi_chan"),
    "chi_kiem_modelUsage_khong_rong": _db('    if chinh != {yeu_cau_model}:', '    if False and chinh != {yeu_cau_model}:', "r05_chin_fixture_hai_rig", "r06_json_mo_ho_phai_do", "r13_tut_giua_chung_bi_chan", "r19_dinh_danh_phai_khop_bang_nhau"),
    "tap_bang_nhau_noi_thanh_membership": _db('    if chinh != {yeu_cau_model}:', '    if yeu_cau_model not in chinh:', "r13_tut_giua_chung_bi_chan"),
    "tap_bang_nhau_noi_thanh_issubset": _db('    if chinh != {yeu_cau_model}:', '    if not {yeu_cau_model}.issubset(chinh):', "r13_tut_giua_chung_bi_chan"),
    "doi_model_phu_phai_co": _db('    chinh = {dinh_danh for ten, dinh_danh in muc if ten not in phu}', '    chinh = {dinh_danh for ten, dinh_danh in muc if ten not in phu}\n    if not phu:\n        raise KhongDoDuoc("đột biến đòi model phụ")', "r05_chin_fixture_hai_rig", "r06_json_mo_ho_phai_do", "r13_tut_giua_chung_bi_chan", "r14_khong_co_model_phu_van_dat"),
    "bo_canonicalModel_chi_so_ten_khoa": _db('        if isinstance(thong_tin, dict) and "canonicalModel" in thong_tin:', '        if False and isinstance(thong_tin, dict) and "canonicalModel" in thong_tin:', "r06_json_mo_ho_phai_do"),
    "kiem_is_error_truoc_so_tap": _db('    def danh_tinh(ten, thong_tin):', '    if ket_qua_json.get("is_error") is not False:\n        raise KhongDoDuoc("đột biến kiểm is_error trước")\n    def danh_tinh(ten, thong_tin):', "r05_chin_fixture_hai_rig"),
    "thieu_is_error_doc_false": _db('    if ket_qua_json.get("is_error") is not False:', '    if ket_qua_json.get("is_error", False) is not False:', "r06_json_mo_ho_phai_do"),
    "review_class_la_doc_nhu_routine": _db('    if gia_tri not in _HANG_REVIEW:', '    if False and gia_tri not in _HANG_REVIEW:', "r08_review_class_allow_list"),
    "write_set_rong_van_chon": _db("    if not ket_qua:", "    if False and not ket_qua:", "r09_write_set_rong_khong_do_duoc"),
    "so_am_doc_nhu_pham_vi_nho": _db("    if type(so_dong) is not int or so_dong < 0 or type(luot) is not int or luot < 1:", "    if type(so_dong) is not int or type(luot) is not int:", "r10_so_am_khong_phai_pham_vi_nho"),
    "systemic_khong_cong_diem": _db('    if review_class == "systemic":', '    if False and review_class == "systemic":', "r11_systemic_cong_mot_diem"),
    "ha_lop_theo_effective": _db('            review_class = max((khai, hieu_luc), key=_HANG_REVIEW.get)', '            review_class = hieu_luc', "r12_effective_khong_duoc_ha_lop"),
    "backslash_la_ky_tu_thuong": _db('    if "\\\\" in duong:', '    if False and "\\\\" in duong:', "r15_backslash_bi_tu_choi"),
    "bo_bang_vung_mo_rong": _db('".github/workflows/", ".github/checks/", ".claude/hooks/",', '".github/workflows/", ".claude/hooks/",', "r16_bang_vung_r6_va_nhan_planned"),
    "bo_boc_nhan_planned": _db('        if duong.startswith("planned:"): duong = duong[len("planned:"):].strip()', '        if False and duong.startswith("planned:"): duong = duong[len("planned:"):].strip()', "r16_bang_vung_r6_va_nhan_planned"),
    "cli_hoan_vi_so_dong_luot": _db('chon(lop, a.duong_dan, a.so_dong, a.luot, bac_truoc)', 'chon(lop, a.duong_dan, a.luot, a.so_dong, bac_truoc)', "r17_cli_khong_hoan_vi_so_dong_luot", "r24_cli_effective_leo_lop"),
    "cli_bo_qua_bac_truoc": _db('chon(lop, a.duong_dan, a.so_dong, a.luot, bac_truoc)', 'chon(lop, a.duong_dan, a.so_dong, a.luot, None)', "r18_cli_bac_truoc_fail_close"),
    "khoa_noi_long_substring": _db('        return ten', '        return yeu_cau_model if yeu_cau_model in ten else ten', "r19_dinh_danh_phai_khop_bang_nhau"),
    "canonical_noi_long_startswith": _db('            return can', '            return yeu_cau_model if can.startswith(yeu_cau_model) else can', "r19_dinh_danh_phai_khop_bang_nhau"),
    "dict_bo_fallback_review_class": _db('        else: review_class = khai', '        else: review_class = review_class.get("effective_review_class")', "r20_dict_chi_review_class_van_chay"),
    "luot_ha_bien_duoi": _db('    if luot >= 3: cong(1, "lượt=%d >= 3" % luot)', '    if luot >= 2: cong(1, "lượt=%d >= 3" % luot)', "r21_ghim_bien_duoi_tuyet_doi"),
    "so_tep_ha_bien_duoi": _db('    if len(ds) >= 5: cong(1, "số tệp=%d >= 5" % len(ds))', '    if len(ds) >= 4: cong(1, "số tệp=%d >= 5" % len(ds))', "r21_ghim_bien_duoi_tuyet_doi"),
    "so_dong_ha_bien_duoi": _db('    if so_dong >= 400: cong(1, "số dòng=%d >= 400" % so_dong)', '    if so_dong >= 399: cong(1, "số dòng=%d >= 400" % so_dong)', "r21_ghim_bien_duoi_tuyet_doi"),
    "diem_ha_bien_duoi": _db('    return 0 if diem <= 0 else 1 if diem <= 2 else 2 if diem <= 4 else 3', '    return 0 if diem <= 0 else 1 if diem <= 2 else 2 if diem < 4 else 3', "r21_ghim_bien_duoi_tuyet_doi"),
    "bo_chuan_hoa_duong": _db('        duong = _chuan_hoa_duong(duong)', '        duong = duong', "r15_backslash_bi_tu_choi", "r22_duong_khong_chuan_va_planned_lap", "r23_nhan_thu_muc_chi_boc_mot_slash", "r27_duong_dan_thoat_repo"),
    "boc_planned_lap": _db('        if duong.startswith("planned:"): raise KhongDoDuoc("nhãn planned: lặp: %r" % duong)', '        while duong.startswith("planned:"): duong = duong[len("planned:"):].strip()', "r22_duong_khong_chuan_va_planned_lap"),
    "boc_slash_cuoi_nhieu_lan": _db('    de_so = duong[:-1] if duong.endswith("/") else duong', '    de_so = duong.rstrip("/") if duong.endswith("/") else duong', "r23_nhan_thu_muc_chi_boc_mot_slash"),
    "duong_khong_chuan_thanh_khong_biet": _db('    if de_so != chuan: raise KhongDoDuoc("đường dẫn không chuẩn %r; bản chuẩn: %r" % (duong, chuan))', '    if de_so != chuan: return duong', "r22_duong_khong_chuan_va_planned_lap", "r23_nhan_thu_muc_chi_boc_mot_slash", "r27_duong_dan_thoat_repo"),
    "bo_uu_tien_effective_review_class": _db('            review_class = max((khai, hieu_luc), key=_HANG_REVIEW.get)', '            review_class = khai', "r24_cli_effective_leo_lop"),
    "revert_startswith_dotdot": _db('if chuan == ".." or chuan.startswith("../"):', 'if chuan.startswith(".."):', 'r26_duong_dan_bi_chan_nham'),
    "bo_escape_bang_cham_cham": _db('if chuan == ".." or chuan.startswith("../"):', 'if chuan.startswith("../"):', 'r27_duong_dan_thoat_repo'),
    "bo_escape_startswith_cham_cham_slash": _db('if chuan == ".." or chuan.startswith("../"):', 'if chuan == "..":', 'r27_duong_dan_thoat_repo'),
    "rong_settings_json": _db('path == ".claude/settings.json"', '".claude/settings.json" in path', 'r28_so_bang_nhau_exact_match'),
    "rong_release_manifest": _db('path == "RELEASE_MANIFEST.json"', '"RELEASE_MANIFEST.json" in path', 'r28_so_bang_nhau_exact_match'),
    "rong_protocol": _db('path == "docs/PROTOCOL_DA_PHIEN.md"', '"docs/PROTOCOL_DA_PHIEN.md" in path', 'r28_so_bang_nhau_exact_match'),
    "rong_gitignore": _db('path == ".gitignore"', '".gitignore" in path', 'r28_so_bang_nhau_exact_match'),
    "rong_bon_exact_match": _db(
        '    if path == ".claude/settings.json" or path == "RELEASE_MANIFEST.json" or path.startswith(\n            (".github/workflows/", ".github/checks/", ".claude/hooks/",\n                        ".claude/dev/packet_loop", "ops/lease_publish")): return "cong"\n    if path == "docs/PROTOCOL_DA_PHIEN.md" or path.startswith(\n            ("docs/adr/", ".claude/skills/", ".claude/agents/")): return "giao-thuc"\n    if path.startswith("scripts/"): return "runtime"\n    if path == ".gitignore"',
        '    if ".claude/settings.json" in path or "RELEASE_MANIFEST.json" in path or path.startswith(\n            (".github/workflows/", ".github/checks/", ".claude/hooks/",\n                        ".claude/dev/packet_loop", "ops/lease_publish")): return "cong"\n    if "docs/PROTOCOL_DA_PHIEN.md" in path or path.startswith(\n            ("docs/adr/", ".claude/skills/", ".claude/agents/")): return "giao-thuc"\n    if path.startswith("scripts/"): return "runtime"\n    if ".gitignore" in path',
        'r28_so_bang_nhau_exact_match'
    ),
    "dot_names_become_known": _db('    return "khong-biet"', '    if path.startswith(".."): return "dev"\n    return "khong-biet"', 'r26_duong_dan_bi_chan_nham'),
    "normalizer_strips_leading_dots": _db('    return chuan', '    return chuan.lstrip(".")', 'r01_bon_bac_biet_truoc', 'r21_ghim_bien_duoi_tuyet_doi', 'r26_duong_dan_bi_chan_nham', 'r28_so_bang_nhau_exact_match'),
    "same_score_wrong_zone": _db('    if path == ".gitignore" or path.startswith((".claude/dev/", "ops/")): return "dev"', '    if path == ".gitignore" or path.startswith((".claude/dev/", "ops/")) or path.endswith(".orig"): return "dev"', 'r28_so_bang_nhau_exact_match'),
}
def _chay(m):
    dat, ly = {}, {}
    for ten, ham in CA:
        try:
            ham(m)
            dat[ten] = True
        except Exception as exc:  # ca đỏ là DỮ LIỆU, runner phải chạy hết bảng
            dat[ten] = False
            ly[ten] = "%s: %s" % (type(exc).__name__, exc)
    return dat, ly
def _ap(van, tim, thay):
    if van.count(tim) != 1:
        raise AssertionError("mốc đột biến khớp %d chỗ: %r" % (van.count(tim), tim))
    return van.replace(tim, thay, 1)
def main():
    nen, ly = _chay(_nap())
    do_san = sorted(k for k, v in nen.items() if not v)
    print("nền: %d/%d đạt" % (sum(nen.values()), len(nen)))
    for ten in do_san:
        print("  ĐỎ %s: %s" % (ten, ly[ten]))
    if do_san:
        print("TỪ CHỐI công bố điểm đột biến: nền có %d ca ĐỎ" % len(do_san))
        return 1
    hong = []
    goc = MA.read_text(encoding="utf-8")
    sys.dont_write_bytecode = True  # mutant cùng kích thước/mtime từng làm CPython nạp nhầm .pyc.
    with tempfile.TemporaryDirectory(prefix="tl351-mut-") as d:
        for i, (ten, (tim, thay, dich)) in enumerate(sorted(DOT_BIEN.items())):
            path = Path(d) / ("mut-%02d-%s.py" % (i, ten))
            path.write_text(_ap(goc, tim, thay), encoding="utf-8")
            dat, _ = _chay(_nap(path, "mut_%02d" % i))
            chet = sorted(k for k, v in dat.items() if not v)
            dung = chet == sorted(dich)
            print("  %s %s -> %s" % ("ok" if dung else "LỖI", ten, chet or "KHÔNG CA NÀO"))
            if not dung:
                hong.append("%s: khai=%s, thực=%s" % (ten, sorted(dich), chet))
    print("SỐ LIỆU: ca=%d; đột biến=%d" % (len(CA), len(DOT_BIEN)))
    if hong:
        print("TỔNG: %d lỗi" % len(hong))
        for x in hong:
            print("  " + x)
        return 1
    print("TỔNG: ĐẠT")
    return 0
if __name__ == "__main__":
    sys.exit(main())
