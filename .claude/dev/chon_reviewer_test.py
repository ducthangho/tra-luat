#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phản chứng offline cho bộ chọn reviewer — packet #351.
Mỗi đột biến chạy trên TOÀN BỘ bảng ca và phải giết ĐÚNG, CHỈ ĐÚNG tập đã khai.
Nền đỏ thì từ chối công bố điểm: ca đỏ sẵn không phải một mutant bị giết.
"""

from __future__ import annotations

import importlib
import importlib.util
import itertools
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
MA = HERE / "chon_reviewer.py"
BAC = (("claude-opus-5", "high"), ("claude-opus-5", "xhigh"),
       ("claude-fable-5", "xhigh"), ("claude-fable-5", "max"))

def _nap(path=MA, nhan="nen"):
    importlib.invalidate_caches()
    sp = importlib.util.spec_from_file_location("tl351_" + nhan, str(path))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m
def _doi_loi(m, ham, *args):
    try:
        ham(*args)
    except m.KhongDoDuoc:
        return
    raise AssertionError("đầu vào không đo được nhưng không bị từ chối: %r" % (args,))
def _bac(m, review_class, paths, so_dong=0, luot=1, bac_truoc=None):
    return m.chon(review_class, paths, so_dong, luot, bac_truoc)[:2]
def r01_bon_bac_biet_truoc(m):
    # Năm vùng đã biết không tự sinh điểm; nếu một tiền tố trượt allow-list, ca 0 sẽ lộ.
    for path in ("scripts/tl.py", ".claude/dev/x.py", "ops/x.py",
                 "references/x.txt", "README.md"):
        if _bac(m, "routine", [path]) != BAC[0]:
            raise AssertionError("điểm 0 sai cho vùng đã biết: %s" % path)

    mot_diem = [
        _bac(m, "routine", ["docs/adr/0001-x.md"]),
        _bac(m, "routine", ["scripts/x.py"], so_dong=400),
        _bac(m, "routine", ["scripts/x.py"], luot=3),
        _bac(m, "routine", ["scripts/%d.py" % i for i in range(5)]),
    ]
    if any(x != BAC[1] for x in mot_diem):
        raise AssertionError("một khoản +1 không cho bậc điểm 1–2: %r" % mot_diem)
    if _bac(m, "routine", [".github/workflows/ci.yml"]) != BAC[1]:
        raise AssertionError("vùng cong +2 không cho đúng bậc")
    if _bac(m, "sensitive", [".claude/skills/x/SKILL.md"]) != BAC[2]:
        raise AssertionError("điểm 3 không cho fable/xhigh")
    nam_tep = [".github/workflows/ci.yml"] + ["scripts/%d.py" % i for i in range(4)]
    kq = m.chon("sensitive", nam_tep, 0, 1)
    if kq[:2] != BAC[3] or "bậc cuối=claude-fable-5/max" not in kq[2]:
        raise AssertionError("điểm 5 hoặc giải thích bậc cuối sai: %r" % (kq,))
def r02_khong_biet_day_len_cao_nhat(m):
    kq = m.chon("sensitive", ["vi-du/la.txt"], 0, 1)
    if kq[:2] != BAC[3] or "+3 chạm vùng khong-biet" not in kq[2]:
        raise AssertionError("đường lạ không fail-close lên bậc cao nhất: %r" % (kq,))
def r03_banh_coc_hai_chieu(m):
    giu = _bac(m, "routine", ["scripts/x.py"], bac_truoc=BAC[3])
    if giu != BAC[3]:
        raise AssertionError("bậc trước cao hơn đã bị tụt: %r" % (giu,))
    nam_tep = [".github/workflows/ci.yml"] + ["scripts/%d.py" % i for i in range(4)]
    khong_keo = _bac(m, "sensitive", nam_tep, bac_truoc=BAC[0])
    if khong_keo != BAC[3]:
        raise AssertionError("bậc trước thấp kéo kết quả mới xuống: %r" % (khong_keo,))
def r04_dinh_danh_allow_list(m):
    for alias in ("opus", "fable", "sonnet"):
        _doi_loi(m, m.kiem_dinh_danh, alias, "high")
    m.kiem_dinh_danh("claude-opus-5", "high")
    _doi_loi(m, m.kiem_dinh_danh, "claude-opus-5", "khong-ton-tai")
# Đúng 9 bản ghi ở cả hai rig của đặc tả §0(c)/(c′). Bốn cặp opus/fable trong
# sandbox có kho khác nhau ở việc dùng công cụ, dù các trường liên quan của JSON giống
# nhau. Giữ cả 9 nhãn để một rig không âm thầm bị rút khỏi phép đo lần nữa.
PHU = "claude-haiku-4-5-20251001"

def _ket_qua(loi, *models):
    return {"subtype": "success", "is_error": loi,
            "modelUsage": {x: {"canonicalModel": x.rsplit("-", 1)[0]
                                if x == PHU else x} for x in models}}
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
    if len(FIXTURE) != 9:
        raise AssertionError("bảng fixture không còn đủ 9 bản ghi: %d" % len(FIXTURE))
    for nhan, model, du_lieu, phai_dat in FIXTURE:
        loi = ""
        try:
            thong_bao = m.kiem_ket_qua(model, du_lieu)
            dat = True
        except m.KhongDoDuoc as exc:
            dat = False
            loi = str(exc)
        if dat != phai_dat:
            raise AssertionError("fixture %s: nhận %s, mong %s" % (nhan, dat, phai_dat))
        if dat and len(du_lieu["modelUsage"]) > 1 and PHU not in thong_bao:
            raise AssertionError("fixture %s không kể khoá phụ trong thông báo" % nhan)
        if nhan == "kho/model-rác" and "model yêu cầu" not in loi:
            raise AssertionError("fixture model rác bị chặn sai nhánh: %r" % loi)
def r06_json_mo_ho_phai_do(m):
    thieu_is_error = {"modelUsage": {
        "claude-opus-5": {"canonicalModel": "claude-opus-5"}}}
    for x in (None, [], {}, {"is_error": False, "modelUsage": {}},
              thieu_is_error,
              {"is_error": False, "modelUsage": {"claude-fable-5": {
                  "canonicalModel": "claude-fable-5"}}}):
        _doi_loi(m, m.kiem_ket_qua, "claude-opus-5", x)
    # Khoá không khớp nhưng canonical khớp thì vẫn là bằng chứng dương hợp lệ.
    m.kiem_ket_qua("claude-opus-5", {"is_error": False, "modelUsage": {
        "claude-opus-5-20260827": {"canonicalModel": "claude-opus-5"}}})
    _doi_loi(m, m.kiem_ket_qua, "claude-opus-5", {"is_error": False, "modelUsage": {
        "id-theo-ngay": {"canonicalModel": "claude-fable-5"}}})
def r07_don_dieu_moi_to_hop(m):
    """144 tổ hợp gốc; với mỗi tổ hợp, thêm từng khoản điểm và so chỉ số bậc."""
    vung = (".github/workflows/ci.yml", "docs/adr/x.md", "scripts/x.py",
            ".claude/dev/x.py", "references/x.txt", "vi-du/la.txt")

    def ds(path, nhieu):
        return [path] + (["scripts/phu-%d.py" % i for i in range(4)] if nhieu else [])

    for review_class, path, nhieu, dai, muon in itertools.product(
            ("routine", "systemic", "sensitive"), vung,
            (False, True), (False, True), (False, True)):
        args = (ds(path, nhieu), 400 if dai else 399, 3 if muon else 2)
        hien_tai = BAC.index(_bac(m, review_class, *args))
        cac_ban_them = [
            _bac(m, "sensitive", *args),
            _bac(m, review_class, ds(path, True), args[1], args[2]),
            _bac(m, review_class, args[0], 400, args[2]),
            _bac(m, review_class, args[0], args[1], 3),
        ]
        if any(BAC.index(x) < hien_tai for x in cac_ban_them):
            raise AssertionError("thêm khoản điểm làm tụt bậc: %r" % ((review_class,) + args,))
        co_so = BAC.index(_bac(m, review_class, ds("scripts/co-so.py", nhieu),
                              args[1], args[2]))
        if hien_tai < co_so:
            raise AssertionError("đổi từ vùng 0 điểm sang %s làm tụt bậc" % path)
def r08_review_class_allow_list(m):
    # Đo lượt 2: `sensitve`/`SENSITIVE`/None từng âm thầm bớt 2 điểm; strip thì hợp lệ.
    for x in ("sensitve", "SENSITIVE", None):
        _doi_loi(m, m.chon, x, ["scripts/x.py"], 0, 1)
    for x in ("routine", "systemic", "sensitive"):
        m.chon(x, ["scripts/x.py"], 0, 1)
    if _bac(m, " sensitive ", ["scripts/x.py"]) != BAC[1]:
        raise AssertionError("review_class hợp lệ sau strip bị từ chối")
def r09_write_set_rong_khong_do_duoc(m):
    for x in ([], "", (), [" ", ""]):
        _doi_loi(m, m.chon, "routine", x, 0, 1)
def r10_so_am_khong_phai_pham_vi_nho(m):
    for so_dong, luot in ((-999, 1), (0, -5), (0, 0), (1.5, 1), (0, True)):
        _doi_loi(m, m.chon, "routine", ["scripts/x.py"], so_dong, luot)
    m.chon("routine", ["scripts/x.py"], 0, 1)
def r11_systemic_cong_mot_diem(m):
    kq = m.chon("systemic", ["scripts/x.py"], 0, 1)
    if kq[:2] != BAC[1] or "+1 review_class=systemic" not in kq[2]:
        raise AssertionError("systemic không cộng đúng +1: %r" % (kq,))
def r12_uu_tien_effective_review_class(m):
    lease = {"review_class": "sensitive", "effective_review_class": "routine"}
    if _bac(m, lease, ["scripts/x.py"]) != BAC[0]:
        raise AssertionError("không ưu tiên lớp sau escalation")
CA = [(ham.__name__, ham) for ham in (
    r01_bon_bac_biet_truoc, r02_khong_biet_day_len_cao_nhat, r03_banh_coc_hai_chieu,
    r04_dinh_danh_allow_list, r05_chin_fixture_hai_rig, r06_json_mo_ho_phai_do,
    r07_don_dieu_moi_to_hop, r08_review_class_allow_list, r09_write_set_rong_khong_do_duoc,
    r10_so_am_khong_phai_pham_vi_nho, r11_systemic_cong_mot_diem,
    r12_uu_tien_effective_review_class)]

DOT_BIEN = {
    "bo_nhanh_khong_biet": (
        '        cong(3, "chạm vùng khong-biet")',
        '        pass  # đột biến: bỏ điểm vùng ngoài allow-list',
        ["r02_khong_biet_day_len_cao_nhat"]),
    "bo_banh_coc": (
        "        if truoc > chi_so:", "        if False and truoc > chi_so:",
        ["r03_banh_coc_hai_chieu"]),
    "nhan_bi_danh": (
        'MO_HINH_CHO_PHEP = ("claude-opus-5", "claude-fable-5")',
        'MO_HINH_CHO_PHEP = ("claude-opus-5", "claude-fable-5", "opus", "fable", "sonnet")',
        ["r04_dinh_danh_allow_list"]),
    "tin_subtype_success": (
        '    model_usage = ket_qua_json.get("modelUsage")',
        '    if ket_qua_json.get("subtype") == "success":\n'
        '        return "modelUsage: ĐẠT (đột biến tin subtype)"\n'
        '    model_usage = ket_qua_json.get("modelUsage")',
        ["r05_chin_fixture_hai_rig"]),
    "doi_modelUsage_thanh_dung_mot_khoa": (
        '    khoa_khop = yeu_cau_model if yeu_cau_model in model_usage else None',
        '    if len(model_usage) != 1:\n'
        '        raise KhongDoDuoc("đột biến đòi đúng một khoá")\n'
        '    khoa_khop = yeu_cau_model if yeu_cau_model in model_usage else None',
        ["r05_chin_fixture_hai_rig"]),
    "chi_kiem_modelUsage_khong_rong": (
        '    khoa_khop = yeu_cau_model if yeu_cau_model in model_usage else None',
        '    khoa_khop = next(iter(model_usage))  # đột biến không tìm model yêu cầu',
        ["r05_chin_fixture_hai_rig", "r06_json_mo_ho_phai_do"]),
    "thieu_is_error_doc_false": (
        '    if ket_qua_json.get("is_error") is not False:',
        '    if ket_qua_json.get("is_error", False) is not False:',
        ["r06_json_mo_ho_phai_do"]),
    "review_class_la_doc_nhu_routine": (
        '    if review_class not in ("routine", "systemic", "sensitive"):',
        '    if False and review_class not in ("routine", "systemic", "sensitive"):',
        ["r08_review_class_allow_list"]),
    "write_set_rong_van_chon": (
        "    if not ket_qua:", "    if False and not ket_qua:",
        ["r09_write_set_rong_khong_do_duoc"]),
    "so_am_doc_nhu_pham_vi_nho": (
        "    if type(so_dong) is not int or so_dong < 0 or type(luot) is not int or luot < 1:",
        "    if type(so_dong) is not int or type(luot) is not int:",
        ["r10_so_am_khong_phai_pham_vi_nho"]),
    "systemic_khong_cong_diem": (
        '    if review_class == "systemic":',
        '    if False and review_class == "systemic":',
        ["r11_systemic_cong_mot_diem"]),
    "bo_uu_tien_effective_review_class": (
        '        review_class = review_class.get("effective_review_class", review_class.get("review_class"))',
        '        review_class = review_class.get("review_class")',
        ["r12_uu_tien_effective_review_class"]),
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
