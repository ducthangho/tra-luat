# -*- coding: utf-8 -*-
"""F2-A (ADR-0018) — nghiem thu cho `.githooks/eol_policy.py`.

Phu dung bang nghiem thu F2-A trong docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md:116 —
"test file moi, Unicode, space, LF/CRLF; hook khong chi so voi HEAD" — cong phan chung cho
rename/copy va cho binary khong chua NUL.

Suite NAY chay truc tiep (CI goi thang, ca ubuntu lan windows). Regression trong canonical
selftest nam o `scripts/test_fragments/wp49_eol_policy_index_blobs.py`; hai duong CO Y trung
mot phan de mot duong hong thi duong kia van bat.

Moi ca dung MOT kho git tam. Blob duoc bom bang `hash-object --no-filters` + `update-index`
thay vi `git add`: duoi policy dich `git add` TU chuan hoa ve LF, nen khong the dung no de dung
hien truong "CRLF nam trong index" — dung hien truong ma ca F2-B phai don.
"""
from __future__ import annotations

import builtins
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

# Đặt TRƯỚC mọi import cây. Các ca cuối tệp dùng LẠI hợp đồng fragment canonical, mà `__pycache__`
# rơi vào `scripts/test_fragments/` sẽ làm CHÍNH hợp đồng đó ném `INVALID_FRAGMENT_PATH`:
# `_candidate_path` từ chối mọi child không phải `wp*.py`, kể cả thư mục. Một bộ test không được
# để lại thứ làm hỏng cây mà nó vừa đo.
sys.dont_write_bytecode = True

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eol_policy  # noqa: E402

_SOURCE_ROOT = Path(__file__).resolve().parent.parent
_CANONICAL_SCRIPTS = _SOURCE_ROOT / "scripts"
_CONG_BUNDLE_FRAGMENT = _SOURCE_ROOT / ".github" / "checks" / "bundle_fragment_check.py"

_ATTRS = (
    b"* text=auto eol=lf\n"
    b"*.cmd text eol=crlf\n"
    b"*.bat text eol=crlf\n"
    b"references/golden/** -text\n"
    # Giữ ĐỒNG BỘ với khối binary của `.gitattributes` thật. Danh sách ở đây là FIXTURE của kho
    # tạm, không phải nguồn sự thật: phép suy ra từ bảng ingest/loader nằm ở
    # `scripts/test_fragments/wp49_eol_policy_index_blobs.py`, chạy trong canonical selftest.
    b"*.pdf -text\n"
    b"*.doc -text\n"
    b"*.docx -text\n"
    b"*.rtf -text\n"
    b"*.odt -text\n"
    b"*.xls -text\n"
    b"*.xlsx -text\n"
    b"*.png -text\n"
    b"*.jpg -text\n"
    b"*.jpeg -text\n"
    b"*.tif -text\n"
    b"*.tiff -text\n"
    b"*.zip -text\n"
)

# Mẫu binary KHÔNG chứa NUL, mỗi họ một chữ ký thật. Chọn không-NUL có chủ đích: đó là đúng chỗ
# heuristic `text=auto` hụt, nên nếu policy tuột mất một họ thì ca test sẽ thấy ngay.
_MAU_BINARY = {
    "tep.pdf": b"%PDF-1.4\r\n1 0 obj\r\nendobj\r\n%%EOF\r\n",
    "tep.docx": b"PK\x03\x04word/document.xml\r\ncontent\r\n",
    "tep.xls": b"\xd0\xcf\x11\xe0BIFF\r\nrecord\r\n",
    "tep.odt": b"PK\x03\x04mimetypeapplication/vnd.oasis\r\n",
    "tep.rtf": b"{\\rtf1\\ansi\r\n\\par test\r\n}\r\n",
    "tep.tif": b"II*\x2a\r\nIFD\r\n",
    "tep.tiff": b"MM\x2a\x2b\r\nIFD\r\n",
    "tep.png": b"\x89PNG\r\n\x1a\r\nIHDR\r\n",
    "tep.jpg": b"\xff\xd8\xff\xe0JFIF\r\n",
}


# ── wp1221 (đặc tả r3): ca đỏ phải nói VÌ SAO — và chỉ nói bằng DANH SÁCH CHO PHÉP ──────────────────
#
# Mỗi ca chỉ trả `bool`, nên trước bản vá một ca đỏ chỉ để lại `FAIL <ca>` (CI Windows run 41975947155:
# 28/30, không biết fragment nào hỏng). Kênh dưới đây cho ca GHI lại thứ nó đã thấy; `main()` chỉ in khi
# ca FAIL. Bất biến M4: phần ghi KHÔNG BAO GIỜ đổi kết quả ca — lỗi của nó chỉ thành `CHAN_DOAN_LOI`.
#
# M3: KHÔNG có bộ che. Bộ che hỏi "chuỗi này có GIỐNG bí mật không" và đã thua năm lần trong mười lượt
# review (mỗi phép biến đổi trên đường in đẻ ra một biểu diễn mới). Ở đây bộ lọc hỏi "giá trị này có
# NGUỒN GỐC an toàn không": số/bool, mã trong tập đóng, định danh do chính kho khai. Chuỗi tự do (stderr,
# thông điệp lỗi, `detail`…) chỉ in LOẠI + ĐỘ DÀI. Nội dung thô chỉ có ở `--chan-doan-tho` (M8), ngoài CI.
_CD_TRAN_CHUOI = 2000       # mỗi giá trị đã lọc
_CD_TRAN_PAYLOAD = 4000     # mọi dòng của MỘT payload cộng lại
_CD_TRAN_CA = 12000         # cả khối chẩn đoán của một ca (đã TÍNH chỗ cho dấu cắt)
_CD_CHO_DAU_CAT = 80        # ngân sách dành sẵn cho dòng `…[cat khoi …]`
_CD_TRAN_MUC = 200          # danh sách: giữ ĐẦU, tối đa ngần này phần tử
_CD_NGAN_XEP = [[]]         # ngăn xếp kênh; `_chay_mot_ca` đẩy một kênh mới cho mỗi ca
_CD_DUONG = [set()]         # chuỗi CHÍNH ca truyền cho `_git`/`_inject` — nguồn gốc của đường dẫn (P12)
_CD_THO = [False]           # M8: chỉ `main` bật, chỉ bằng `--chan-doan-tho`, chỉ ngoài CI
_TEN_LOP = type.__dict__["__name__"].__get__   # đọc tên lớp KHÔNG qua metaclass

_MA_PROBLEMS = frozenset((  # P6 — sáu mã `problems` của `bundle_fragment_check.py` (dòng 185–195)
    "BUNDLED_FRAGMENT_LOAD_FAILED", "DEV_FRAGMENT_DISCOVERY_FAILED", "NO_BUNDLED_CASES", "TEST_ID_SET_MISMATCH",
    "BUNDLED_FRAGMENT_FAILED", "UNEXPECTED_TOPOLOGY"))
_MA_CONG = _MA_PROBLEMS | {"RELEASE_BUNDLE_FAILED", "EXTRACTED_ROOT_NOT_FOUND", "DRIVER_NON_JSON"}   # P5 (127/136/155)
_MA_LOI_FRAGMENT = frozenset((   # P8b — mã literal của họ `FragmentError` (`scripts/tl_core/test_fragments.py`)
    "FRAGMENT_CONTRACT", "PATH_ID_MISMATCH", "DUPLICATE_FRAGMENT_PATH", "DUPLICATE_TEST_ID", "FRAGMENT_EXECUTION",
    "FRAGMENT_IMPORT", "INVALID_FRAGMENT_PATH", "INVALID_FRAGMENT_ROOT", "PATH_TRAVERSAL", "BUNDLED_MODULE_MISSING",
    "BUNDLED_MODULE_READ", "FRAGMENT_READ", "TEST_ID_INDEX_READ", "BUNDLED_MODULE_SYNTAX", "FRAGMENT_SYNTAX",
    "TEST_ID_INDEX_SYNTAX", "BUNDLED_FRAGMENT_SOURCES", "BUNDLED_MODULE_CONTRACT"))
_MA_VI_PHAM = frozenset(("CRLF_IN_INDEX", "MIXED_EOL_IN_INDEX", "LONE_CR_IN_INDEX"))          # P11
_TAP_EOL_ATTR = frozenset(("crlf", "lf", "unspecified", "unset", "set"))                         # P13
_TAP_EXPECTED = frozenset(("LF trong index", "LF trong index (checkout tu vat chat hoa CRLF)"))
_TAP_SCHEMA = frozenset(("bundle_fragment_check.v1", "eol_policy.v1"))                         # P4
_KHOA_TOPOLOGY = ("has_bundled_module", "dev_fragments_absent", "editorconfig_absent", "gitattributes_present")
_RE_TRANG_THAI = re.compile(r"[ACDMRTU][0-9]{0,3}")                                           # P14
_RE_DUONG = re.compile(r"[^\x00-\x1f]{1,200}")


def _trong(tap):
    """Luật cho phép: chuỗi thuộc một TẬP ĐÓNG biết trước."""
    return lambda s: s if s in tap else None


def _id_kho(s):
    """P9: CHỈ định danh kho đã khai — fragment ở cây dev và ba probe của tệp này (tập, không phải hình)."""
    ten = {p.stem for p in _fragment_canonical()} | {_PROBE_FILE_ID, _PROBE_LOAD_ID, _PROBE_FAIL_ID}
    return s if s in ten or (s[-3:] == ".py" and s[:-3] in ten) else None


def _duong_ca(s):
    """P12: đường dẫn chỉ in khi CHÍNH ca đã đặt nó qua `_inject`/`git mv` (nguồn: literal của tệp này)."""
    return s if s in _CD_DUONG[-1] and _RE_DUONG.fullmatch(s) else None


def _ho_fragment(lop):
    tf = _hop_dong_fragment()
    t = getattr(tf, lop, None)
    return t if isinstance(t, type) and issubclass(t, tf.FragmentError) else None


def _lop_kho(lop):
    """P8a/X1/X3: tên lớp chỉ in khi là ngoại lệ builtin hoặc thuộc họ `FragmentError` của hợp đồng canonical."""
    t = getattr(builtins, lop, None) if type(lop) is str else None
    return lop if (isinstance(t, type) and issubclass(t, BaseException)) or _ho_fragment(lop) else None


def _mo_ta_loi(s):
    """P8: `"Lớp: thông điệp"` của cổng/driver. In tên lớp đã kiểm; với họ `FragmentError` (`code:fragment:detail`)
    in thêm `code` thuộc tập đóng và `fragment` đã khai. Phần còn lại là văn bản tự do ⇒ CHỈ độ dài."""
    lop, co, msg = s.partition(": ")
    if not co or not _lop_kho(lop):
        return None
    ra, manh = [lop], msg.split(":")
    if _ho_fragment(lop) and manh[0] in _MA_LOI_FRAGMENT:
        ra.append("code=" + manh.pop(0))
        if manh and _id_kho(manh[0]):
            ra.append("fragment=" + manh.pop(0))
    return " ".join(ra + ["con_lai_len=%d" % len(":".join(manh))])


def _loai(x):
    """Mô tả KHÔNG đọc nội dung: `<loai:<kiểu builtin> len:<n|->>`; kiểu không builtin ⇒ `<doi_tuong>`."""
    t = type(x)
    if getattr(builtins, _TEN_LOP(t), None) is not t:
        return "<doi_tuong>"
    co_len = any(t is k for k in (str, bytes, bytearray, list, tuple, dict, set, frozenset))
    return "<loai:%s len:%s>" % (_TEN_LOP(t), len(x) if co_len else "-")


def _loc(x, cho=None, sau=0):
    """M3 — MỘT bộ lọc, luật THEO TRƯỜNG. `cho` là `bool`/`int` (đúng KIỂU ấy, so bằng `is`), một luật chuỗi
    (trả chuỗi được phép hoặc None), hoặc tuple luật theo VỊ TRÍ cho một danh sách. Danh sách không có luật vị trí
    lọc từng phần tử bằng `cho`. Mọi thứ khác (sai kiểu, chuỗi bị từ chối, trường không luật) ⇒ `_loai`."""
    t = type(x)
    if x is None:
        return "None"
    if (cho is bool or cho is int) and t is cho:
        return str(x)
    if type(cho) is tuple:
        if t is list and len(x) == len(cho) and sau < 3:
            return "[" + ", ".join(_loc(v, c, sau + 1) for v, c in zip(x, cho)) + "]"
        return _loai(x)
    if t is str and cho is not None and cho is not bool and cho is not int:
        kq = cho(x)
        if type(kq) is str:
            return kq
    if any(t is k for k in (list, tuple, set, frozenset)) and sau < 3:
        cap = list(x)
        if t is set or t is frozenset:
            cap = sorted(cap) if all(type(v) is str for v in cap) else cap
        phan, dai = [], 2
        for v in cap:               # M5: dừng TRƯỚC trần, dấu cắt luôn còn tổng số mục
            m = _loc(v, cho, sau + 1)
            if len(phan) >= _CD_TRAN_MUC or dai + len(m) + 2 > _CD_TRAN_CHUOI - 40:
                break
            phan.append(m)
            dai += len(m) + 2
        du = len(cap) - len(phan)
        return "[" + ", ".join(phan + (["…[cat %d/%d muc]" % (du, len(cap))] if du else [])) + "]"
    return _loai(x)


def _tho(x):
    """M8 — CHỈ ở chế độ `--chan-doan-tho`: nội dung thô, không che (người đứng ở máy mình tự chịu)."""
    if any(type(x) is k for k in (bytes, bytearray)):
        return bytes(x).decode("utf-8", "replace")
    return x if type(x) is str else repr(x)


def _lop_loi(exc):
    """X3: tên lớp (chỉ builtin / họ `FragmentError`, và đúng CHÍNH lớp ấy) + độ dài thông điệp; không in thông điệp."""
    t, lop = type(exc), _TEN_LOP(type(exc))
    that = getattr(builtins, lop, None) is t or _ho_fragment(lop) is t
    try:
        n = len(str(exc))
    except Exception:                                    # noqa: BLE001 — `__str__` lạ
        n = "-"
    return "%s len:%s" % (lop if that else "<lop khong in>", n)


def _ghi_an_toan(ham):
    """Chạy một bước GHI chẩn đoán; mọi lỗi của nó (trừ Ctrl-C) thành `CHAN_DOAN_LOI` (M4)."""
    try:
        ham()
    except KeyboardInterrupt:
        raise
    except BaseException as exc:                         # noqa: BLE001 — M4: không đổi kết quả ca
        _CD_NGAN_XEP[-1].append(("CHAN_DOAN_LOI", _lop_loi(exc)))


def _cat(text, tran):
    """M5: giữ ĐẦU (giá trị dài trên đường mặc định là danh sách id); chế độ thô giữ ĐUÔI (lỗi nằm cuối)."""
    if len(text) <= tran:
        return text
    dau = "…[cat %d ky tu]" % len(text)
    giu = tran - len(dau)                       # dấu cắt nằm TRONG ngân sách
    dau = "…[cat %d ky tu]" % (len(text) - giu)
    return dau + text[-giu:] if _CD_THO[0] else text[:giu] + dau


def _cd(nhan, gia_tri, cho=None):
    """Ghi `nhãn → giá trị đã lọc` vào kênh của ca đang chạy; trả lại `gia_tri` nguyên vẹn.

    `nhan` PHẢI là literal (P17): giá trị chạy đi qua `gia_tri` và luật `cho`, không ghép vào nhãn.
    """
    def ghi():
        chuoi = _tho(gia_tri) if _CD_THO[0] else _loc(gia_tri, cho)
        _CD_NGAN_XEP[-1].append((nhan, _cat(chuoi, _CD_TRAN_CHUOI)))
    _ghi_an_toan(ghi)
    return gia_tri


def _ve(nhan, gia_tri):
    """Ghi giá trị một vế của biểu thức quyết định, trả lại nó — dùng TRONG chuỗi `and` (giữ short-circuit)."""
    _cd("ve:" + nhan, gia_tri, bool)
    return gia_tri


def _chay_tien_trinh(nhan, cmd, **kw):
    """`subprocess.run` + ghi `rc` dưới NHÃN LỆNH HẰNG (bảng N). stdout/stderr chỉ ghi ở chế độ thô (M8)."""
    kw.setdefault("stdout", subprocess.PIPE)
    kw.setdefault("stderr", subprocess.PIPE)
    proc = subprocess.run(cmd, **kw)
    _cd(nhan + " :: rc", proc.returncode, int)
    if _CD_THO[0]:
        _cd(nhan + " :: stdout", proc.stdout)
        _cd(nhan + " :: stderr", proc.stderr)
    return proc


def _chay_policy(root, mode):
    """`eol_policy.run` + ghi các trường P3/P4/P10–P13 của kết quả (nhóm B), mỗi trường một luật."""
    out = eol_policy.run(root, mode)

    def ghi():
        _cd("eol_policy.run :: mode", mode, _trong(("staged", "all")))
        _cd("eol_policy.run :: schema", out.get("schema"), _trong(_TAP_SCHEMA))
        _cd("eol_policy.run :: ok", out.get("ok"), bool)
        _cd("eol_policy.run :: [scanned, checked, skipped]", [out.get(k) for k in ("scanned", "checked", "skipped")],
            (int, int, int))
        vp = out.get("violations")
        _cd("eol_policy.run :: so vi_pham", len(vp) if type(vp) is list else vp, int)
        for v in (vp if type(vp) is list else [])[:50]:
            _cd("eol_policy.run :: vi_pham [path, error, cr, lf, crlf, eol_attr, expected]",
                [v.get(k) for k in ("path", "error", "cr", "lf", "crlf", "eol_attr", "expected")] if type(v) is dict else v,
                (_duong_ca, _trong(_MA_VI_PHAM), int, int, int, _trong(_TAP_EOL_ATTR), _trong(_TAP_EXPECTED)))
    _ghi_an_toan(ghi)
    return out


def _dong_cua(nhan, chuoi):
    """ĐÚNG các dòng sẽ in cho một mục kênh — dùng CHUNG cho in và cho ngân sách M5 (kể cả dòng tiếp nối)."""
    if nhan == "CHAN_DOAN_LOI":
        return ["CHAN_DOAN_LOI: %s" % chuoi]
    phan = chuoi.splitlines() or [""]
    return ["CHAN_DOAN: %s = %s" % (nhan, phan[0])] + ["CHAN_DOAN:   | %s" % p for p in phan[1:]]


def _dai_dong(n, v):
    return sum(len(d) + 1 for d in _dong_cua(n, v))


def _ghi_payload_cong(nhan, p):
    """Ghi payload JSON của cổng/driver theo bảng P (P2–P9), mỗi trường một luật. `detail`/khoá lạ: KHÔNG nội dung."""
    def ghi():
        if type(p) is not dict:
            return _cd(nhan + " :: payload", p)
        kenh, dau = _CD_NGAN_XEP[-1], len(_CD_NGAN_XEP[-1])
        for k, cho in (("schema", _trong(_TAP_SCHEMA)), ("ok", bool), ("error", _trong(_MA_CONG)),
                       ("problems", _trong(_MA_PROBLEMS)), ("case_count", int), ("detail", None),
                       ("load_error", _mo_ta_loi), ("dev_discovery_error", _mo_ta_loi)):
            if k in p:
                _cd(nhan + " :: " + k, p[k], cho)
        tp = p.get("topology")
        if type(tp) is dict:
            _cd(nhan + " :: topology", [tp.get(k) for k in _KHOA_TOPOLOGY], (bool,) * 4)
        dev, goi = p.get("dev_test_ids"), p.get("bundle_test_ids")
        if type(dev) is list and type(goi) is list:
            _cd(nhan + " :: so_id [dev, goi]", [len(dev), len(goi)], (int, int))
            _cd(nhan + " :: id chi o dev", [i for i in dev if i not in goi], _id_kho)
            _cd(nhan + " :: id chi o goi", [i for i in goi if i not in dev], _id_kho)
        cases = p.get("cases")
        if type(cases) is list:
            for c in [c for c in cases if not (type(c) is dict and c.get("ok") is True)][:50]:
                _cd(nhan + " :: ca khong ok [name, test_id, ok, error]",
                    [c.get(k) for k in ("name", "test_id", "ok", "error")] if type(c) is dict else c,
                    (_id_kho, _id_kho, bool, _mo_ta_loi))
        bo = 0                                                # M5: trần payload tính trên dòng sẽ in
        while len(kenh) > dau and sum(_dai_dong(n, v) for n, v in kenh[dau:]) > _CD_TRAN_PAYLOAD - 100:
            kenh.pop()
            bo += 1
        if bo:
            kenh.append((nhan + " :: payload", "…[cat %d muc]" % bo))
    _ghi_an_toan(ghi)


def _doc_json_cong(nhan, proc):
    """stdout của cổng/driver → payload; không phải JSON ⇒ ghi nhãn kèm LOẠI + ĐỘ DÀI, không nội dung (M2)."""
    try:
        return json.loads(proc.stdout.decode("utf-8", "replace"))
    except ValueError:
        _cd(nhan + " :: stdout_khong_phai_json", proc.stdout)
        return None


def _khoi_chan_doan(ghi, tran=None):
    """Dựng các dòng chẩn đoán từ kênh `ghi`. Mọi dòng bắt đầu bằng tiền tố `CHAN_DOAN`."""
    tran = _CD_TRAN_CA if tran is None else tran
    if not ghi:
        return ["CHAN_DOAN: (rong — ca khong ghi chan doan)"]
    dong, tong = [], 0
    for i, (nhan, chuoi) in enumerate(ghi):
        moi = _dong_cua(nhan, chuoi)
        do_dai = sum(len(d) + 1 for d in moi)
        if tong + do_dai > tran - _CD_CHO_DAU_CAT:
            dong.append("CHAN_DOAN: …[cat khoi: bo %d muc, ~%d ky tu]"
                        % (len(ghi) - i, sum(len(n) + len(c) for n, c in ghi[i:])))
            break
        dong += moi
        tong += do_dai
    return dong


def _don_thu_muc_tam(td):
    td.cleanup()


def _vi_tri_loi(exc):
    """X1: `tệp:dòng` của frame SÂU NHẤT thuộc tập NHỎ tệp đã biết (tệp này, policy, hợp đồng fragment, cổng), không có
    ⇒ `?`. Không tin `co_filename`/`__file__` của module bất kỳ: loader cấp được tên tùy ý (F1b, lượt 2–3)."""
    biet = {os.path.realpath(str(x)) for x in (__file__, _SOURCE_ROOT / ".githooks" / "eol_policy.py",
                                                _CANONICAL_SCRIPTS / "tl_core" / "test_fragments.py", _CONG_BUNDLE_FRAGMENT)}
    tb, ra = exc.__traceback__, "?"
    while tb is not None:
        duong = os.path.realpath(tb.tb_frame.f_code.co_filename)
        if duong in biet:
            ra = "%s:%d" % (os.path.basename(duong), tb.tb_lineno)
        tb = tb.tb_next
    return ra


def _dong_don_dep(exc, td):
    """X2: tên lớp, errno, winerror, có nằm trong thư mục tạm của ca không. Không thông điệp, không đường dẫn."""
    if _CD_THO[0]:
        return "CHAN_DOAN_DON_DEP: %s (%s)" % (_cat(_tho(exc), _CD_TRAN_CHUOI), td.name)
    so = [getattr(exc, k, None) for k in ("errno", "winerror")]
    fn = getattr(exc, "filename", None)
    trong = type(fn) is str and (fn == td.name or fn.startswith(td.name + os.sep))
    return "CHAN_DOAN_DON_DEP: %s errno:%s winerror:%s la_thu_muc_tam:%s" % (
        _lop_loi(exc).split(" len:")[0], *[v if type(v) is int else None for v in so], trong)


def _chay_mot_ca(case, don_dep=None):
    """Chạy MỘT ca trong thư mục tạm riêng; trả `(ok, dòng_cần_in)`.

    Lỗi dọn thư mục tạm (Windows khoá tệp) KHÔNG làm sập suite và KHÔNG đổi kết quả ca: nó chỉ
    thành một dòng `CHAN_DOAN_DON_DEP` (M7). Lỗi của `_init` vẫn ném như trước.
    """
    don_dep = _don_thu_muc_tam if don_dep is None else don_dep
    ghi, truoc, sau, loi_don = [], [], [], None
    td = tempfile.TemporaryDirectory(prefix="eol_policy_")
    _CD_NGAN_XEP.append(ghi)
    _CD_DUONG.append(set())
    try:
        root = Path(td.name) / "kho"
        root.mkdir()
        _init(root)
        try:
            ok = bool(case(root))
        except Exception as exc:                     # noqa: BLE001 — bao loi, khong nuot
            ok = False
            try:
                truoc.append("  ! %s: %s" % (case.__name__, _cat(repr(exc), _CD_TRAN_CHUOI) if _CD_THO[0] else
                                             "%s tai %s" % (_lop_loi(exc), _vi_tri_loi(exc))))
            except Exception:                        # noqa: BLE001 — M4
                truoc.append("  ! %s: <loi khong mo ta duoc>" % case.__name__)
    finally:
        _CD_NGAN_XEP.pop()
        _CD_DUONG.pop()
        try:
            don_dep(td)
        except OSError as exc:
            loi_don = exc
    if loi_don is not None:
        try:
            sau.append(_dong_don_dep(loi_don, td))
        except KeyboardInterrupt:
            raise
        except BaseException:                        # noqa: BLE001 — M7: không làm sập suite
            sau.append("CHAN_DOAN_DON_DEP: <loi don thu muc tam; khong mo ta duoc>")
    if not ok:
        try:     # dòng dọn dẹp tính vào trần toàn khối
            sau += _khoi_chan_doan(ghi, _CD_TRAN_CA - sum(len(d) + 1 for d in truoc + sau))   # X1/X2 trong trần
        except KeyboardInterrupt:
            raise
        except BaseException as exc:                 # noqa: BLE001 — M4: không đổi kết quả
            sau.append("CHAN_DOAN_LOI: %s" % _lop_loi(exc))
    return ok, truoc + ["%s %s" % ("PASS" if ok else "FAIL", case.__name__)] + sau


def _git(root, *args, stdin=None):
    if args[:1] == ("mv",):                   # P12: đường dẫn CHỈ từ `git mv` của ca (không phải mọi đối số git)
        _CD_DUONG[-1].update(a for a in args[1:] if type(a) is str)
    proc = subprocess.run(
        ["git", "-C", str(root)] + list(args),
        input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError("git %s: %s" % (args[0], proc.stderr.decode("utf-8", "replace")))
    return proc.stdout


def _init(root):
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "user.name", "eol policy test")
    _git(root, "config", "core.autocrlf", "false")
    (root / ".gitattributes").write_bytes(_ATTRS)
    _git(root, "add", ".gitattributes")
    _git(root, "commit", "-q", "-m", "attrs")


def _inject(root, relpath, blob):
    """Dat `blob` NGUYEN BYTE vao index tai `relpath`, bo qua moi filter cua git."""
    _CD_DUONG[-1].add(relpath)
    oid = _git(root, "hash-object", "-w", "--no-filters", "--stdin", stdin=blob)
    oid = oid.decode("ascii").strip()
    _git(root, "update-index", "--add", "--cacheinfo", "100644,%s,%s" % (oid, relpath))
    return oid


def _commit_blob(root, relpath, blob, msg="seed"):
    """Commit `blob` nguyen byte VA dat no len dia.

    Ban tren dia la bat buoc cho cac ca rename: `git mv` doi tep that ton tai trong working tree
    ("bad source" neu chi co trong index). `git mv` giu nguyen blob OID — no doi ten chu khong
    re-add — nen byte CRLF trong index van con nguyen de phan chung co hieu luc.
    """
    path = root / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(blob)
    _inject(root, relpath, blob)
    _git(root, "commit", "-q", "-m", msg)


def _paths(payload):
    return {v["path"] for v in payload["violations"]}


def _install_real_pre_commit(root):
    """Cài đúng hook/validator đang được test để `git commit` tự gọi qua shebang thật."""
    hooks = root / ".githooks"
    hooks.mkdir(parents=True, exist_ok=True)
    for name in ("pre-commit", "eol_policy.py"):
        dest = hooks / name
        shutil.copyfile(_SOURCE_ROOT / ".githooks" / name, dest)
        dest.chmod(0o755)
    _git(root, "config", "core.hooksPath", ".githooks")


def _ghi_ve_hook(statuses, proc, output, ten):
    """Hai ca `real_hook`: giá trị TỪNG vế (P2/P14/P17). Output của `git commit` KHÔNG in, chỉ in vế bool."""
    _cd("statuses", statuses, lambda s: s if _RE_TRANG_THAI.fullmatch(s) else None)
    _cd("ve:rc!=0", proc.returncode != 0, bool)
    _cd("ve:CRLF_IN_INDEX in output", "CRLF_IN_INDEX" in output, bool)
    _cd("ve:[ten tep in output]", [t in output for t in ten], bool)


def _commit_through_real_hook(root):
    _install_real_pre_commit(root)
    return _chay_tien_trinh(
        "git commit (pre-commit hook)",
        ["git", "-C", str(root), "commit", "-m", "hook must block"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )


def _staged_statuses(root):
    raw = _git(root, "diff", "--cached", "--raw", "-z", "--abbrev=40")
    fields = raw.split(b"\x00")
    return [
        field.decode("ascii", "replace").split()[-1]
        for field in fields
        if field.startswith(b":")
    ]


# ── ca co ban ─────────────────────────────────────────────────────────────────────────────────

def case_new_file_crlf_bi_chan(root):
    """Tep MOI (chua co trong HEAD) mang CRLF phai BI CHAN.

    Day dung la lo hong cua hook shell cu: `git cat-file -e "HEAD:$f" || continue` bo qua tron
    tep moi, tuc la duong de dua CRLF moi vao kho khong he bi soi.
    """
    _inject(root, "moi.py", b"a = 1\r\nb = 2\r\n")
    out = _chay_policy(root, "staged")
    return out["ok"] is False and _paths(out) == {"moi.py"}


def case_new_file_lf_duoc_qua(root):
    _inject(root, "moi.py", b"a = 1\nb = 2\n")
    out = _chay_policy(root, "staged")
    return out["ok"] is True and out["checked"] == 1


def case_ten_co_khoang_trang(root):
    """`for f in $staged` cua hook cu tach theo khoang trang -> mot ten thanh hai path ma."""
    _inject(root, "thu muc/ghi chu.md", b"x\r\ny\r\n")
    out = _chay_policy(root, "staged")
    return out["ok"] is False and _paths(out) == {"thu muc/ghi chu.md"}


def case_ten_tieng_viet(root):
    """Kho nay checkout o `D:/Quốc hội/tra-luat`; ten co dau khong phai gia dinh."""
    ten = "tài liệu/Quốc hội.md"
    _inject(root, ten, b"x\r\ny\r\n")
    out = _chay_policy(root, "staged")
    return out["ok"] is False and _paths(out) == {ten}


def case_cmd_lf_trong_index_duoc_qua(root):
    """`*.cmd text eol=crlf`: index van phai LF, CRLF chi sinh ra luc checkout."""
    _inject(root, "setup.cmd", b"@echo off\nexit /b 0\n")
    out = _chay_policy(root, "staged")
    return out["ok"] is True and out["checked"] == 1


def case_cmd_crlf_trong_index_bi_chan(root):
    _inject(root, "setup.cmd", b"@echo off\r\nexit /b 0\r\n")
    out = _chay_policy(root, "staged")
    if out["ok"] is not False or _paths(out) != {"setup.cmd"}:
        return False
    # Thong diep phai noi ro index-LF/checkout-CRLF, neu khong nguoi sua mo tep tren dia thay
    # CRLF dung nhu mong doi va ket luan validator sai.
    return "checkout" in out["violations"][0]["expected"]


def case_golden_duoc_bo_qua(root):
    """`references/golden/** -text`: golden so BYTE, validator khong duoc dung vao."""
    _inject(root, "references/golden/fix.json", b"{\r\n  \"a\": 1\r\n}\r\n")
    out = _chay_policy(root, "staged")
    return out["ok"] is True and out["checked"] == 0 and out["skipped"] == 1


def case_mixed_eol_bi_chan(root):
    _inject(root, "tron.txt", b"a\r\nb\nc\r\n")
    out = _chay_policy(root, "staged")
    return (out["ok"] is False and _paths(out) == {"tron.txt"}
            and out["violations"][0]["error"] == "MIXED_EOL_IN_INDEX")


def case_lone_cr_bi_chan(root):
    _inject(root, "co.txt", b"a\rb\r")
    out = _chay_policy(root, "staged")
    return (out["ok"] is False and _paths(out) == {"co.txt"}
            and out["violations"][0]["error"] == "LONE_CR_IN_INDEX")


def case_khong_chi_so_voi_head(root):
    """CRLF DA NAM trong HEAD va khong doi: hook cu thay "khong flip" nen cho qua.

    Validator hoi "co dung policy khong", khong hoi "co DOI khong" — nen `--all` van bat duoc.
    `--staged` sach la dung: khong co gi dang stage. Do la ly do CI phai chay `--all`.
    """
    _commit_blob(root, "cu.py", b"a = 1\r\n", "legacy crlf")
    staged = _chay_policy(root, "staged")
    allrun = _chay_policy(root, "all")
    return (staged["ok"] is True and staged["scanned"] == 0
            and allrun["ok"] is False and _paths(allrun) == {"cu.py"})


def case_attr_doc_tu_gitattributes(root):
    """Policy khong duoc chep cung: doi `.gitattributes` trong index thi verdict phai doi theo."""
    _inject(root, "x.txt", b"a\r\nb\r\n")
    truoc = _chay_policy(root, "staged")
    _inject(root, ".gitattributes", _ATTRS + b"x.txt -text\n")
    sau = _chay_policy(root, "staged")
    return (truoc["ok"] is False
            and sau["ok"] is True and sau["skipped"] == 1 and sau["checked"] == 1)


# ── P1: rename / copy phai duoc kiem theo path DICH ───────────────────────────────────────────

def case_rename_golden_sang_text_bi_chan(root):
    """Phan chung P1(a). `git mv references/golden/x -> moved.txt` tren blob CRLF.

    CRLF hop le duoi `-text` cua golden; sang path text thi KHONG. Ban cu dung
    `--diff-filter=ACM` nen ban ghi `R100` bi loc mat va bao `scanned: 0, ok: true` —
    duong ngan nhat dua CRLF hop le sang cho khong hop le, di lot khong dau vet.
    """
    _commit_blob(root, "references/golden/fix.json", b"a\r\nb\r\n", "golden")
    _git(root, "mv", "references/golden/fix.json", "moved.txt")
    out = _chay_policy(root, "staged")
    return (out["ok"] is False and _paths(out) == {"moved.txt"}
            and out["violations"][0]["error"] == "CRLF_IN_INDEX")


def case_copy_golden_sang_text_bi_chan(root):
    """Phan chung P1(b). Ban sao cua blob CRLF dat o path text phai bi chan.

    Khang dinh o KET QUA chu khong o dang ban ghi: tuy `diff.renames` ma git bieu dien no la
    `C` (hai path) hay `A` (mot path) — ca hai deu phai dan toi CHAN. Hinh dang `C` co ban ghi
    rieng duoc kiem trong case_parse_raw_z_hai_path.
    """
    _commit_blob(root, "references/golden/fix.json", b"a\r\nb\r\n", "golden")
    _git(root, "config", "diff.renames", "copies")
    blob = _git(root, "cat-file", "blob", ":references/golden/fix.json")
    _inject(root, "ban_sao.txt", blob)
    out = _chay_policy(root, "staged")
    return out["ok"] is False and "ban_sao.txt" in _paths(out)


def case_rename_hop_le_van_qua(root):
    """Phan chung P1(c). Rename giua hai path text tren blob LF phai KHONG bi chan."""
    _commit_blob(root, "cu.py", b"a = 1\n", "lf source")
    _git(root, "mv", "cu.py", "moi.py")
    out = _chay_policy(root, "staged")
    return out["ok"] is True and out["scanned"] == 1 and out["checked"] == 1


def case_rename_dich_unicode_va_khoang_trang(root):
    """Phan chung P1(d). Path DICH co dau va dau cach phai duoc bao nguyen ven."""
    ten = "tài liệu/Quốc hội mới.md"
    _commit_blob(root, "references/golden/fix.json", b"a\r\nb\r\n", "golden")
    (root / "tài liệu").mkdir(parents=True, exist_ok=True)   # `git mv` doi thu muc dich co san
    _git(root, "mv", "references/golden/fix.json", ten)
    out = _chay_policy(root, "staged")
    return out["ok"] is False and _paths(out) == {ten}


def case_parse_raw_z_hai_path(root):
    """Parser phai nhay 3 o cho `R`/`C` va LUON lay path DICH.

    Nhay 2 o thi con tro lech va MOI ban ghi sau do bi doc sai — nen ca nay ghep mot ban ghi
    rename, mot ban ghi copy va mot ban ghi modify lien tiep de bat dung loi lech do.
    """
    z = (b":100644 100644 " + b"a" * 40 + b" " + b"b" * 40 + b" R100\x00src.txt\x00dst.txt\x00"
         b":100644 100644 " + b"c" * 40 + b" " + b"d" * 40 + b" C75\x00from.txt\x00to.txt\x00"
         b":100644 100644 " + b"e" * 40 + b" " + b"f" * 40 + b" M\x00plain.txt\x00")
    got = _cd("parse_raw_z", eol_policy.parse_raw_z(z), _trong(("dst.txt", "to.txt", "plain.txt")))
    return got == [("dst.txt", "b" * 40), ("to.txt", "d" * 40), ("plain.txt", "f" * 40)]


def case_real_hook_rename_only_bi_chan(root):
    """Integration: chính pre-commit hook phải chặn stage chỉ có một bản ghi R100."""
    _commit_blob(root, "references/golden/fix.json", b"a\r\nb\r\n", "golden")
    _git(root, "mv", "references/golden/fix.json", "moved.txt")
    statuses = _staged_statuses(root)
    proc = _commit_through_real_hook(root)
    output = (proc.stdout + proc.stderr).decode("utf-8", "replace")
    _ghi_an_toan(lambda: _ghi_ve_hook(statuses, proc, output, ("moved.txt",)))   # đủ vế, từ dữ liệu đã có
    return (
        statuses == ["R100"]
        and proc.returncode != 0
        and "CRLF_IN_INDEX" in output
        and "moved.txt" in output
    )


def case_real_hook_rename_copy_only_bi_chan(root):
    """Integration: pre-commit phải chạy khi stage chỉ gồm R/C, không có A/C/M fallback giả."""
    blob = b"a\r\nb\r\n"
    _commit_blob(root, "references/golden/fix.json", blob, "golden")
    _git(root, "config", "diff.renames", "copies")
    _git(root, "rm", "-q", "references/golden/fix.json")
    _inject(root, "copied.txt", blob)
    _inject(root, "moved.txt", blob)
    statuses = _staged_statuses(root)
    proc = _commit_through_real_hook(root)
    output = (proc.stdout + proc.stderr).decode("utf-8", "replace")
    _ghi_an_toan(lambda: _ghi_ve_hook(statuses, proc, output, ("copied.txt", "moved.txt")))
    return (
        sorted(statuses) == ["C100", "R100"]
        and proc.returncode != 0
        and "CRLF_IN_INDEX" in output
        and "copied.txt" in output
        and "moved.txt" in output
    )


def case_release_bundle_chay_real_wp49_fragment(root):
    """Integration: case wp49 thật phải xanh sau release-bundle + extract, không có editorconfig."""
    out_zip = root.parent / "wp49-release.zip"
    proc = _chay_tien_trinh(
        "tl.py release-bundle",
        [sys.executable, str(_SOURCE_ROOT / "scripts" / "tl.py"),
         "release-bundle", "--root", str(_SOURCE_ROOT),
         "--out", str(out_zip), "--top", "tra-luat", "--json"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if proc.returncode != 0 or not out_zip.is_file():
        _cd("tra_false_som: tl.py release-bundle hong [rc, co_zip]", [proc.returncode, out_zip.is_file()], (int, bool))
        return False
    extract_root = root.parent / "extracted"
    with zipfile.ZipFile(out_zip) as archive:
        archive.extractall(extract_root)
    package_root = extract_root / "tra-luat"
    if (
        (package_root / ".editorconfig").exists()
        or (package_root / "scripts" / "test_fragments").exists()
        or not (package_root / ".gitattributes").is_file()
        or not (package_root / "scripts" / "tl_test_fragments_bundled.py").is_file()
    ):
        _cd("tra_false_som: bo cuc goi sai [.editorconfig, test_fragments, .gitattributes, bundled.py]", [
            (package_root / ".editorconfig").exists(), (package_root / "scripts" / "test_fragments").exists(),
            (package_root / ".gitattributes").is_file(),
            (package_root / "scripts" / "tl_test_fragments_bundled.py").is_file()], (bool,) * 4)
        return False
    probe = r'''import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
import tl
from tl_core.test_fragments import load_runtime_fragment_cases, _runtime_fragment_topology

topology, _ = _runtime_fragment_topology(root / "scripts")
cases = load_runtime_fragment_cases(root / "scripts")
targets = [case for case in cases if case.test_id == "wp49_eol_policy_index_blobs"]
ok = topology == "bundle" and len(targets) == 1 and bool(targets[0].run(tl))
try:   # wp1221 M2: một dòng JSON có cấu trúc; không bao giờ đổi mã thoát
    import json
    sys.stdout.write(json.dumps({"topology": topology if type(topology) is str else None,
                                 "so_target": len(targets), "ok": ok}))
except Exception:
    pass
raise SystemExit(0 if ok else 1)
'''
    checked = _chay_tien_trinh(
        "python -c <probe wp49 trong goi>",
        [sys.executable, "-c", probe, str(package_root)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    kq = _doc_json_cong("python -c <probe wp49 trong goi>", checked)
    if type(kq) is dict:
        _cd("probe :: topology", kq.get("topology"), _trong(("bundle", "dev", "none")))
        _cd("probe :: [so_target, ok]", [kq.get("so_target"), kq.get("ok")], (int, bool))
    return checked.returncode == 0


# ── F2-A: hành vi của `.github/checks/bundle_fragment_check.py` ───────────────────────────────
#
# Cổng đó từng tự dựng hợp đồng fragment thứ hai (`exec(compile(...), {})` + regex TEST_ID) và bản
# sao ấy nói dối theo CẢ HAI hướng. Nay nó chỉ còn là NGƯỜI GỌI của `scripts/tl_core/test_fragments.py`
# — nhưng bằng chứng của lần sửa đó chạy một lần rồi bốc hơi, nên không gì giữ cho lần sau. Sáu ca
# dưới đây khoá lại, và bản thân chúng KHÔNG dựng loader/parser/hợp đồng thứ hai: mọi phép dò và nạp
# đều đi qua `discover_fragment_test_ids` / `load_runtime_fragment_cases` /
# `generate_bundled_module_bytes` canonical, còn đường trong gói đi qua ĐÚNG `_DRIVER` của cổng.
#
# Negative control dựng bằng BẢN SAO cây trong Temp, không bao giờ chạm cây canonical.

# `TEST_ID` khai ANNOTATED + NHÁY ĐƠN, `run` dùng `__file__`: đúng hai chỗ mà bản sao hợp đồng cũ mù
# (regex `^TEST_ID = "…"` bỏ sót dòng khai; `exec(code, {})` không seed `__file__` nên một fragment
# HỢP LỆ chết `NameError`). Làm probe "hiền" đi là gỡ mất chính thứ đang phân biệt.
_PROBE_FILE_ID = "wp999_file_probe"
_PROBE_FILE_SRC = (
    "# -*- coding: utf-8 -*-\n"
    "from pathlib import Path\n"
    "\n"
    "TEST_ID: str = 'wp999_file_probe'\n"
    "\n"
    "\n"
    "def run(tl_module):\n"
    "    return Path(__file__).name == 'wp999_file_probe.py'\n"
)

# Hỏng lúc NẠP. Cú pháp và AST vẫn hợp lệ nên generator lẫn discovery đi qua trót lọt; chỉ `exec`
# mới nổ ⇒ tách SẠCH load-failure khỏi discovery-failure, không lẫn hai bệnh vào nhau.
_PROBE_LOAD_ID = "wp999_load_probe"
_PROBE_LOAD_SRC = (
    "# -*- coding: utf-8 -*-\n"
    'TEST_ID = "wp999_load_probe"\n'
    "\n"
    "raise RuntimeError('probe: hong ngay o muc module')\n"
    "\n"
    "\n"
    "def run(tl_module):\n"
    "    return True\n"
)

# Hỏng lúc CHẠY: nạp trót lọt, `run` trả False.
_PROBE_FAIL_ID = "wp999_fail_probe"
_PROBE_FAIL_SRC = (
    "# -*- coding: utf-8 -*-\n"
    'TEST_ID = "wp999_fail_probe"\n'
    "\n"
    "\n"
    "def run(tl_module):\n"
    "    return False\n"
)


# A14 (lượt 6 r3) so CẤU TRÚC thân `_env_con` (bỏ docstring) với hằng này — danh sách CHO PHÉP, không đoán idiom.
# SỬA `_env_con` THÌ PHẢI SỬA HẰNG NÀY, có chủ đích và qua review; lệch một nút AST là A14 đỏ.
_HINH_ENV_CON = ('env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1", PYTHONIOENCODING="utf-8")\n'
                 'for ten in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY"):\n    env.pop(ten, None)\nreturn env\n')


def _env_con():
    """Env cho tiến trình con: không đẻ bytecode, UTF-8, và KHÔNG rò biến git của tiến trình cha.

    `bundle_fragment_check._repo_root()` chạy `git rev-parse --show-toplevel` THEO CWD; một `GIT_DIR`
    rò rỉ sẽ kéo nó về kho khác, và cả ca đo sai thứ mà vẫn báo xanh.
    """
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    for ten in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY"):
        env.pop(ten, None)
    return env


def _hop_dong_fragment():
    """Hợp đồng fragment CANONICAL. Append chứ không insert: `scripts/` không được che stdlib."""
    duong = str(_CANONICAL_SCRIPTS)
    if duong not in sys.path:
        sys.path.append(duong)
    from tl_core import test_fragments
    return test_fragments


def _fragment_canonical():
    """Fragment đang có ở cây dev — ĐẾM chứ không ghim số, để packet sau thêm ca không đỏ oan."""
    goc = _CANONICAL_SCRIPTS / "test_fragments"
    return sorted(p for p in goc.glob("wp*.py") if p.is_file())


def _ban_sao_cay(dest):
    """Bản sao CÂY LÀM VIỆC theo `git ls-files` — bỏ `.git`, bỏ mọi rác bị ignore (`__pycache__`).

    `git init` ở bản sao là có chủ đích: cổng lấy gốc kho qua `git rev-parse --show-toplevel`, nên
    bản sao phải là kho THẬT thì ca mới đo đúng đường mà CI đi, chứ không phải nhánh dự phòng.
    """
    for rel in _git(_SOURCE_ROOT, "ls-files", "-z").split(b"\x00"):
        if not rel:
            continue
        ten = rel.decode("utf-8")
        src = _SOURCE_ROOT / ten
        if not src.is_file():
            continue
        dich = dest / ten
        dich.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dich)
    _git(dest, "init", "-q")
    return dest


def _tai_sinh_bundled(copy):
    """Tái sinh adapter bundled bằng CHÍNH generator canonical — không viết tay module sinh ra."""
    tf = _hop_dong_fragment()
    data = tf.generate_bundled_module_bytes(copy / "scripts" / "test_fragments")
    (copy / "scripts" / "tl_test_fragments_bundled.py").write_bytes(data)


def _chay_cong(copy):
    """Chạy CHÍNH cổng production trên bản sao tạm; trả `(rc, payload)`."""
    proc = _chay_tien_trinh(
        "bundle_fragment_check.py --json",
        [sys.executable, str(_CONG_BUNDLE_FRAGMENT), "--json"],
        cwd=str(copy), env=_env_con(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    payload = _doc_json_cong("bundle_fragment_check.py --json", proc)
    _ghi_payload_cong("bundle_fragment_check.py --json", payload if payload is not None else {})
    return proc.returncode, (payload if payload is not None else {})


def _truoc(problems, truoc, sau):
    return truoc in problems and sau in problems and problems.index(truoc) < problems.index(sau)


def case_probe_hop_dong_canonical_o_cay_dev(root):
    """Probe HỢP LỆ phải qua được cả discovery lẫn runtime dev của hợp đồng canonical."""
    if ("TEST_ID: str = 'wp999_file_probe'" not in _PROBE_FILE_SRC
            or "__file__" not in _PROBE_FILE_SRC):
        _cd("tra_false_som: _PROBE_FILE_SRC thieu dong TEST_ID annotated hoac __file__", True, bool)
        return False
    tf = _hop_dong_fragment()
    scripts = root.parent / "dev" / "scripts"
    frag = scripts / "test_fragments"
    frag.mkdir(parents=True)
    (frag / (_PROBE_FILE_ID + ".py")).write_text(_PROBE_FILE_SRC, encoding="utf-8", newline="\n")

    ids = _cd("ids_do_duoc", {entry.test_id for entry in tf.discover_fragment_test_ids(frag)}, _id_kho)
    cases = tf.load_runtime_fragment_cases(scripts)
    _ghi_an_toan(lambda: _cd("cases_nap_duoc", [c.test_id for c in cases], _id_kho))
    return (_ve("ids == {_PROBE_FILE_ID}", ids == {_PROBE_FILE_ID})
            and _ve("len(cases) == 1 and cases[0].test_id == _PROBE_FILE_ID", len(cases) == 1 and cases[0].test_id == _PROBE_FILE_ID)
            and _ve("cases[0].run(object()) is True", cases[0].run(object()) is True))


def case_probe_qua_bundled_topology_canonical(root):
    """Cùng probe đó, qua adapter SINH RA: generator + runtime bundle phải nạp và chạy được."""
    tf = _hop_dong_fragment()
    frag = root.parent / "nguon" / "test_fragments"
    frag.mkdir(parents=True)
    (frag / (_PROBE_FILE_ID + ".py")).write_text(_PROBE_FILE_SRC, encoding="utf-8", newline="\n")

    scripts = root.parent / "goi" / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "tl_test_fragments_bundled.py").write_bytes(tf.generate_bundled_module_bytes(frag))

    cases = tf.load_runtime_fragment_cases(scripts)     # không có test_fragments/ ⇒ topology bundle
    _ghi_an_toan(lambda: _cd("cases_nap_duoc", [c.test_id for c in cases], _id_kho))
    return (_ve("len(cases) == 1 and cases[0].test_id == _PROBE_FILE_ID", len(cases) == 1 and cases[0].test_id == _PROBE_FILE_ID)
            and _ve("cases[0].run(object()) is True", cases[0].run(object()) is True))


def case_driver_that_chay_probe_tren_bundle_giai_nen(root):
    """`_DRIVER` THẬT của cổng phải chạy được probe TRONG gói đã giải nén, không phải ở cây dev.

    Đây đúng là chỗ bản sao hợp đồng cũ chết: `exec(compile(...), {})` không seed `__file__`. Ca này
    lấy `_DRIVER` từ CHÍNH tệp cổng, nên hạ cổng về bản cũ là ca này đỏ ngay.
    """
    spec = importlib.util.spec_from_file_location(
        "_wp49_bundle_fragment_check", _CONG_BUNDLE_FRAGMENT)
    cong = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cong)

    out_zip = root.parent / "driver-release.zip"
    proc = _chay_tien_trinh(
        "tl.py release-bundle",
        [sys.executable, str(_CANONICAL_SCRIPTS / "tl.py"), "release-bundle",
         "--root", str(_SOURCE_ROOT), "--out", str(out_zip), "--top", "tra-luat", "--json"],
        env=_env_con(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0 or not out_zip.is_file():
        _cd("tra_false_som: tl.py release-bundle hong [rc, co_zip]", [proc.returncode, out_zip.is_file()], (int, bool))
        return False
    goi = root.parent / "giai-nen" / "tra-luat"
    with zipfile.ZipFile(out_zip) as archive:
        archive.extractall(goi.parent)
    if (goi / "scripts" / "test_fragments").exists() or (goi / ".editorconfig").exists():
        _cd("tra_false_som: bo cuc goi sai [test_fragments, .editorconfig]", [
            (goi / "scripts" / "test_fragments").exists(), (goi / ".editorconfig").exists()], (bool, bool))
        return False

    # Bơm probe vào adapter BÊN TRONG gói tạm, qua generator canonical. Cây canonical không bị chạm.
    tf = _hop_dong_fragment()
    nguon = root.parent / "nguon-driver"
    nguon.mkdir(parents=True)
    goc = _fragment_canonical()
    for p in goc:
        shutil.copyfile(p, nguon / p.name)
    (nguon / (_PROBE_FILE_ID + ".py")).write_text(_PROBE_FILE_SRC, encoding="utf-8", newline="\n")
    (goi / "scripts" / "tl_test_fragments_bundled.py").write_bytes(
        tf.generate_bundled_module_bytes(nguon))

    driver = root.parent / "driver.py"
    driver.write_text(cong._DRIVER, encoding="utf-8", newline="\n")
    chay = _chay_tien_trinh(
        "bundle_fragment_check._DRIVER (driver.py)",
        [sys.executable, str(driver), str(goi)], cwd=str(goi), env=_env_con(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    payload = _doc_json_cong("bundle_fragment_check._DRIVER (driver.py)", chay)
    if payload is None:
        return False
    _cd("so_fragment_canonical", len(goc), int)
    _ghi_payload_cong("bundle_fragment_check._DRIVER (driver.py)", payload)
    cases = payload.get("cases") or []
    return (_ve("payload.get('load_error') is None", payload.get("load_error") is None)
            and _ve("len(cases) == len(goc) + 1", len(cases) == len(goc) + 1)
            and _ve("all(c.get('ok') for c in cases)", all(c.get("ok") for c in cases))
            and _ve("any(c.get('test_id') == _PROBE_FILE_ID for c in cases)",
                    any(c.get("test_id") == _PROBE_FILE_ID for c in cases)))


def case_cong_bao_load_failed_truoc_trieu_chung(root):
    """Hỏng lúc NẠP phải báo `BUNDLED_FRAGMENT_LOAD_FAILED`, và báo TRƯỚC triệu chứng.

    Loader ném ⇒ `cases` rỗng ⇒ `NO_BUNDLED_CASES` và `TEST_ID_SET_MISMATCH` cũng đỏ theo. Nêu
    triệu chứng thay cho nguyên nhân sẽ đẩy người đọc đi sai hướng, nên THỨ TỰ ở đây là hợp đồng.
    """
    copy = _ban_sao_cay(root.parent / "sao-load")
    (copy / "scripts" / "test_fragments" / (_PROBE_LOAD_ID + ".py")).write_text(
        _PROBE_LOAD_SRC, encoding="utf-8", newline="\n")
    _tai_sinh_bundled(copy)

    rc, p = _chay_cong(copy)
    problems = p.get("problems") or []
    return (_ve("rc == 1 and p.get('ok') is False", rc == 1 and p.get("ok") is False)
            and _ve("p.get('error') == 'BUNDLED_FRAGMENT_LOAD_FAILED'", p.get("error") == "BUNDLED_FRAGMENT_LOAD_FAILED")
            and _ve("problems[:1] == ['BUNDLED_FRAGMENT_LOAD_FAILED']", problems[:1] == ["BUNDLED_FRAGMENT_LOAD_FAILED"])
            and _ve("_PROBE_LOAD_ID in (p.get('load_error') or '')", _PROBE_LOAD_ID in (p.get("load_error") or ""))
            and _ve("p.get('case_count') == 0", p.get("case_count") == 0)
            and _ve("p.get('dev_discovery_error') is None", p.get("dev_discovery_error") is None)
            and _ve("_truoc(problems, 'BUNDLED_FRAGMENT_LOAD_FAILED', 'NO_BUNDLED_CASES')", _truoc(problems, "BUNDLED_FRAGMENT_LOAD_FAILED", "NO_BUNDLED_CASES"))
            and _ve("_truoc(problems, 'BUNDLED_FRAGMENT_LOAD_FAILED', 'TEST_ID_SET_MISMATCH')", _truoc(problems, "BUNDLED_FRAGMENT_LOAD_FAILED", "TEST_ID_SET_MISMATCH")))


def case_cong_bao_dev_discovery_failed_truoc_mismatch(root):
    """Dò ở cây dev hỏng phải báo `DEV_FRAGMENT_DISCOVERY_FAILED`, không im lặng co tập ID lại.

    Regex cũ lặng lẽ BỎ QUA tệp không khớp: một fragment hỏng làm tập ID co lại, rồi phép so với
    bundle vẫn "đúng" một cách vô nghĩa. Ở ca này đường bundle VẪN LÀNH — đỏ không do hỏng chung.
    """
    copy = _ban_sao_cay(root.parent / "sao-dev")
    (copy / "scripts" / "test_fragments" / "khong_hop_le.txt").write_text(
        "khong phai fragment\n", encoding="utf-8", newline="\n")

    rc, p = _chay_cong(copy)
    problems = p.get("problems") or []
    return (_ve("rc == 1 and p.get('ok') is False", rc == 1 and p.get("ok") is False)
            and _ve("p.get('error') == 'DEV_FRAGMENT_DISCOVERY_FAILED'", p.get("error") == "DEV_FRAGMENT_DISCOVERY_FAILED")
            and _ve("problems[:1] == ['DEV_FRAGMENT_DISCOVERY_FAILED']", problems[:1] == ["DEV_FRAGMENT_DISCOVERY_FAILED"])
            and _ve("'INVALID_FRAGMENT_PATH' in (p.get('dev_discovery_error') or '')", "INVALID_FRAGMENT_PATH" in (p.get("dev_discovery_error") or ""))
            and _ve("p.get('load_error') is None", p.get("load_error") is None)
            and _ve("p.get('case_count') == len(_fragment_canonical())", p.get("case_count") == len(_fragment_canonical()))
            and _ve("not p.get('failed')", not p.get("failed"))
            and _ve("_truoc(problems, 'DEV_FRAGMENT_DISCOVERY_FAILED', 'TEST_ID_SET_MISMATCH')", _truoc(problems, "DEV_FRAGMENT_DISCOVERY_FAILED", "TEST_ID_SET_MISMATCH")))


def case_cong_bao_fragment_failed_khi_run_tra_false(root):
    """`run` trả False vẫn phải là `BUNDLED_FRAGMENT_FAILED` — không hoá trang thành load/discovery.

    Kiêm luôn POSITIVE CONTROL: mọi fragment canonical xanh trong bản sao tạm và tập ID dev == bundle.
    Thiếu nó, ba ca âm ở trên có thể xanh chỉ vì bản sao tạm hỏng toàn diện.
    """
    copy = _ban_sao_cay(root.parent / "sao-fail")
    (copy / "scripts" / "test_fragments" / (_PROBE_FAIL_ID + ".py")).write_text(
        _PROBE_FAIL_SRC, encoding="utf-8", newline="\n")
    _tai_sinh_bundled(copy)

    rc, p = _chay_cong(copy)
    hong = {c.get("test_id") for c in (p.get("failed") or [])}
    return (_ve("rc == 1 and p.get('ok') is False", rc == 1 and p.get("ok") is False)
            and _ve("(p.get('problems') or []) == ['BUNDLED_FRAGMENT_FAILED']", (p.get("problems") or []) == ["BUNDLED_FRAGMENT_FAILED"])
            and _ve("p.get('error') == 'BUNDLED_FRAGMENT_FAILED'", p.get("error") == "BUNDLED_FRAGMENT_FAILED")
            and _ve("hong == {_PROBE_FAIL_ID}", hong == {_PROBE_FAIL_ID})
            and _ve("p.get('load_error') is None", p.get("load_error") is None)
            and _ve("p.get('dev_discovery_error') is None", p.get("dev_discovery_error") is None)
            and _ve("p.get('dev_test_ids') == p.get('bundle_test_ids')", p.get("dev_test_ids") == p.get("bundle_test_ids"))
            and _ve("p.get('case_count') == len(_fragment_canonical()) + 1", p.get("case_count") == len(_fragment_canonical()) + 1))


# ── P2: binary khai -text, khong dua vao NUL ──────────────────────────────────────────────────

def case_binary_nul_duoc_bo_qua(root):
    """`text=auto` coi blob co NUL la binary — luoi CUOI, khong phai co che chinh."""
    _inject(root, "data.unknownext", b"\x89PNG\r\n\x1a\n\x00\x00\x00\x0d")
    out = _chay_policy(root, "staged")
    return out["ok"] is True and out["checked"] == 0 and out["skipped"] == 1


def case_binary_khong_co_NUL_van_duoc_tha_nho_khai_text(root):
    """Phan chung cho finding 3: policy KHONG duoc phu thuoc duy nhat vao NUL.

    PDF that bat dau bang `%PDF-` va co the KHONG co NUL nao trong ca tep (stream FlateDecode
    van co the toan byte in duoc). No CO CR — day la CR DU LIEU, khong phai xuong dong. Neu
    validator chi dua vao NUL de nhan binary thi tep nay bi hoi la text va bi chan OAN, roi
    ai do se "sua" no bang cach doi CR -> LF va lam HONG file.
    """
    pdf = b"%PDF-1.4\r\n1 0 obj\r\n<< /Type /Catalog >>\r\nendobj\r\n%%EOF\r\n"
    assert b"\x00" not in pdf
    _inject(root, "tep.pdf", pdf)
    out = _chay_policy(root, "staged")
    return out["ok"] is True and out["checked"] == 0 and out["skipped"] == 1


def case_moi_ho_binary_deu_duoc_tha(root):
    """MỌI họ binary khai `-text` phải được tha — không họ nào rơi lại vào đường text.

    Vòng trước chỉ kiểm `.pdf` nên `.xls/.odt/.tif/.tiff` thiếu khai mà test vẫn xanh: test và
    policy cùng thiếu một chỗ thì chúng xác nhận lẫn nhau. Ở đây duyệt TỪNG họ, và mọi mẫu đều
    KHÔNG có NUL nên `text=auto` không thể cứu — chỉ khai báo `-text` mới cứu được.
    """
    for ten, blob in _MAU_BINARY.items():
        assert b"\x00" not in blob, ten
        _inject(root, ten, blob)
    out = _chay_policy(root, "staged")
    return (out["ok"] is True and out["checked"] == 0
            and out["skipped"] == len(_MAU_BINARY))


def case_ho_binary_thieu_khai_thi_bi_bat(root):
    """Phản chứng của ca trên: BỎ một họ khỏi `.gitattributes` thì nó phải BỊ CHẶN ngay.

    Không có ca này thì `case_moi_ho_binary_deu_duoc_tha` có thể xanh vì lý do sai (ví dụ mọi thứ
    đều bị bỏ qua), và ta lại có một test tự xác nhận chính mình.
    """
    thieu = _ATTRS.replace(b"*.tif -text\n", b"")
    _inject(root, ".gitattributes", thieu)
    _inject(root, "tep.tif", _MAU_BINARY["tep.tif"])
    out = _chay_policy(root, "staged")
    return out["ok"] is False and "tep.tif" in _paths(out)


def case_binary_giu_nguyen_byte_qua_renormalize(root):
    """`-text` phai giu NGUYEN BYTE qua `git add --renormalize .`, khong chi qua validator."""
    pdf = b"%PDF-1.4\r\n1 0 obj\r\nendobj\r\n%%EOF\r\n"
    zipish = b"PK\x03\x04binary-ish\r\npayload\r\n"
    _commit_blob(root, "tep.pdf", pdf, "pdf")
    _commit_blob(root, "goi.zip", zipish, "zip")
    (root / "tep.pdf").write_bytes(pdf)
    (root / "goi.zip").write_bytes(zipish)
    _git(root, "add", "--renormalize", ".")
    sau_pdf = _git(root, "cat-file", "blob", ":tep.pdf")
    sau_zip = _git(root, "cat-file", "blob", ":goi.zip")
    _cd("[sau_pdf == pdf, sau_zip == zipish]", [sau_pdf == pdf, sau_zip == zipish], (bool, bool))
    out = _chay_policy(root, "all")
    return sau_pdf == pdf and sau_zip == zipish and out["ok"] is True


# ── wp1221 r3: tự kiểm kênh chẩn đoán (M6) ────────────────────────────────────────────────────────

def _vi_pham_kien_truc():
    """A14: AST của NGUỒN ĐANG CHẠY (qua `linecache` — bộ đột biến nạp bản đột biến vào đó). Trả `(env, che)`: dòng đọc
    env ngoài `main` (chốt M8)/`_env_con` (khớp `_HINH_ENV_CON`)/hai ca tự kiểm, và dòng mang bộ che (import/hằng chuỗi nhắc bộ quét bí mật, `.sub`)."""
    import ast
    import linecache
    cay = ast.parse("".join(linecache.getlines(str(Path(__file__).resolve()))))
    ham = {f.name: f for f in cay.body if isinstance(f, ast.FunctionDef)}
    bo = {id(n) for k in ("case_chan_doan_mac_dinh_khong_lo_bi_mat", "case_chan_doan_co_tho_chi_cuc_bo")
          for n in ast.walk(ham[k])}            # miễn HẸP: main chỉ `"X" in os.environ`, _env_con chỉ `dict(os.environ…)`
    bo |= {id(c.comparators[0]) for c in ast.walk(ham["main"]) if isinstance(c, ast.Compare) and isinstance(c.ops[0], ast.In)}
    khop = [ast.dump(x) for x in ham["_env_con"].body[1:]] == [ast.dump(x) for x in ast.parse(_HINH_ENV_CON).body]
    bo |= {id(n) for n in ast.walk(ham["_env_con"])} if khop else set()   # khớp hình mẫu ⇒ thân đã được duyệt
    env = [ham["_env_con"].lineno] * (not khop) + [n.lineno for n in ast.walk(ham["main"]) if isinstance(n, (ast.Global, ast.Nonlocal))]
    goi = {id(k.value.func) for c in ast.walk(cay) if isinstance(c, ast.Call) and ast.unparse(c.func) in ("subprocess.run",
           "_chay_tien_trinh") for k in c.keywords if k.arg == "env" and isinstance(k.value, ast.Call)}   # CHỈ env= tiến trình con
    env += [n.lineno for n in ast.walk(cay) if getattr(n, "id", 0) == "_env_con" and id(n) not in goi | bo]
    che, moc = [], "".join(["pkg_secret", "_scan"])
    for n in ast.walk(cay):
        ten = getattr(n, "attr", None) or getattr(n, "id", None) or getattr(n, "name", None)   # `name`: alias của import
        if id(n) not in bo and ten in ("environ", "getenv", "putenv", "environb", "getenvb"):
            env.append(getattr(n, "lineno", 0))
        if (isinstance(n, (ast.Attribute, ast.alias)) and ten in ("sub", "subn")) or (isinstance(n, (ast.Import, ast.ImportFrom))
                and moc in ast.dump(n)) or (isinstance(n, ast.Constant) and type(n.value) is str and moc in n.value):
            che.append(getattr(n, "lineno", 0))
    return env, che


def case_chan_doan_mac_dinh_khong_lo_bi_mat(root):
    """A6/A7/A14: phản chứng của 10 lượt review r2 và lượt 1 r3 đi qua ĐƯỜNG MẶC ĐỊNH ⇒ 0 cửa sổ 8 ký tự của bí mật.

    Bí mật là dữ liệu GIẢ dựng lúc chạy (viết nguyên văn thì bộ quét bí mật của gói bắt nhầm). Mỗi vector đi đúng
    đường thật: tiến trình con (V1 PEM LF/CRLF/cắt dở, V2 PEM ở argv[1]/argv[3], V3 env bằng nguyên payload / tiền
    tố token / bọc PEM, V4 hai khoá chồng nhau), payload cổng (V5: mã, `code`, fragment, lớp ngoài tập; sai kiểu
    trường), ngoại lệ ca (V6, cả lớp động), lỗi dọn dẹp (V7), stdout cổng không phải JSON (V8).
    """
    import base64
    b64 = base64.b64encode(os.urandom(240)).decode()                   # có `/` `+` như thân PEM thật
    hx, k1, k2, h3, h4, h5, h6 = (os.urandom(n).hex() for n in (16, 10, 18, 9, 9, 9, 9))
    pem = "\n".join(["-----BEG" + "IN RSA PRIVATE KEY-----"] + [b64[i:i + 64] for i in range(0, 320, 64)]
                    + ["-----END RSA PRIVATE KEY-----"])
    api = "AI" + "za" + k1 + "AI" + "za" + k2[:35]                      # V4: hai khoá chồng nhau (họ F)
    tok = "GOC" + "SPX-" + hx
    payload = {"schema": tok, "ok": 5, "error": tok, "problems": ["NO_BUNDLED_CASES", "DRIVER_NON_JSON", hx],
               "detail": pem + api, "case_count": True, "load_error": "FragmentPathError: INVALID_FRAGMENT_PATH:"
               + _PROBE_LOAD_ID + ".py:" + tok, "dev_discovery_error": "FragmentExecutionError: S" + h3.upper()
               + ":wp1_" + h4 + ":x", "topology": {"has_bundled_module": tok}, "dev_test_ids": [_PROBE_FILE_ID, hx],
               "bundle_test_ids": [], "cases": [{"name": hx + ".py", "test_id": _PROBE_FAIL_ID, "ok": False,
                                                 "error": "W" + h5 + "Error: " + pem}]}
    env = {"EOL_TEST_FAKE_TOKEN": "TIEN_" + pem + "_HAU", "EOL_TEST_FAKE_SECRET": json.dumps(payload, sort_keys=True),
           "EOL_TEST_FAKE_KEY": tok[:14]}                               # V3: họ D / E / C
    bi_mat = [b64[:320], hx, k1, k2[:35], h3.upper(), h4, h5, h6]
    cu, tho = {k: os.environ.get(k) for k in env}, _CD_THO[0]
    _CD_THO[0] = False                          # ca này đo ĐƯỜNG MẶC ĐỊNH, kể cả khi suite chạy với `--chan-doan-tho`
    os.environ.update(env)
    ma = ("import os,sys; x=sys.argv[1]; e=''.join(os.environ[k] for k in sorted(os.environ) if 'FAKE' in k);"
          " sys.stdout.write(x.replace(chr(10), chr(13)+chr(10)) + e); sys.stderr.write(x + x[:100] + e + sys.argv[2]);"
          " sys.exit(3)")

    def ca_gia(r):
        _chay_tien_trinh("python -c <ca tu kiem>", [sys.executable, "-c", ma, pem, api], env=_env_con())
        _chay_tien_trinh("python <pem o argv1>", [sys.executable, pem], env=_env_con())
        _ghi_payload_cong("bundle_fragment_check.py --json", payload)
        _doc_json_cong("bundle_fragment_check.py --json", subprocess.run(
            [sys.executable, "-c", "import sys; sys.stdout.write(sys.argv[1])", api + pem], stdout=subprocess.PIPE))
        _cd("luat hong", tok, lambda s: 1 // 0)                        # M4: lỗi khi ghi ⇒ CHAN_DOAN_LOI, ca vẫn chạy
        _git(r, "config", "wp1221.tu-kiem", hx)
        _cd("duong tu git config", hx, _duong_ca)                      # P12: đối số `git config` KHÔNG phải đường dẫn
        return False

    def ca_nem(r):
        raise OSError(5, "loi " + tok, os.path.join(str(r), hx))

    def ca_nem_lop_dong(r):
        raise type("E" + h5, (ValueError,), {})("x")

    def don_khoa(td):
        td.cleanup()
        raise PermissionError(13, "D14_KHOA_GIA " + tok, os.path.join(td.name, hx))

    def ca_dai(r):                                                      # A7: danh sách dài + payload + khối vượt trần
        _ghi_payload_cong("payload dai", {"dev_test_ids": [_PROBE_FILE_ID] * 5000, "bundle_test_ids": [],
                                          "cases": [{"name": hx, "ok": False}] * 60})
        [_cd("rc", 1, int) for _ in range(1000)]                       # mục nhỏ: khối đầy SÁT trần
        raise ValueError("z" * 50)                                      # X1 cũng nằm trong trần khối (F3)
    def bia(g):                                 # F1b: module ĐĂNG KÝ trong sys.modules, `__file__` bịa trong kho/stdlib
        def ca(r):
            sys.modules["wp1221_bia"] = m = type(sys)("wp1221_bia")
            m.__file__ = os.path.join(g, h6 + ".py")
            exec(compile("raise ValueError('x')", m.__file__, "exec"), m.__dict__)
        return ca
    try:
        ra = []
        for ca, dd in ((ca_gia, None), (ca_nem, None), (ca_nem_lop_dong, None), (lambda r: True, don_khoa),
                       (bia(str(_SOURCE_ROOT)), None), (bia(os.path.dirname(os.__file__)), None)):
            ra += _chay_mot_ca(ca, don_dep=dd)[1]
        _, dai = _chay_mot_ca(ca_dai)
        _CD_THO[0] = True                       # F3: payload THÔ nhiều dòng — trần tính cả dòng tiếp nối
        dai_tho = _chay_mot_ca(lambda r: _ghi_payload_cong("payload tho", {"detail": "x\n" * 400}) or False)[1]
        _CD_THO[0] = False
    finally:
        _CD_THO[0] = tho
        sys.modules.pop("wp1221_bia", None)
        for k, v in cu.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
    out = "\n".join(ra + dai)
    lo = [s[i:i + 8] for s in bi_mat for i in range(len(s) - 7) if s[i:i + 8] in out]
    _cd("so cua so 8 ky tu da so / so lo", [sum(len(s) - 7 for s in bi_mat), len(lo)], (int, int))
    dong_pl = [d for d in dai if d.startswith("CHAN_DOAN: payload dai")]
    env_sai, che = _vi_pham_kien_truc()
    return (_ve("A6 khong cua so 8 ky tu nao cua bi mat", not lo)
            and _ve("A6 rc + nhan lenh hang", "python -c <ca tu kiem> :: rc = 3" in out
                    and "python <pem o argv1> :: rc = 2" in out)
            and _ve("A6 stdout khong phai JSON: chi loai + do dai",
                    "bundle_fragment_check.py --json :: stdout_khong_phai_json = <loai:bytes len:" in out)
            and _ve("A6 P8 in code + fragment DA KHAI; code/fragment/lop ngoai tap => khong in",
                    "FragmentPathError code=INVALID_FRAGMENT_PATH fragment=wp999_load_probe.py con_lai_len=" in out
                    and "dev_discovery_error = FragmentExecutionError con_lai_len=" in out
                    and "[<loai:str len:35>, wp999_fail_probe, False, <loai:str len:" in out)
            and _ve("A6 P2/P3/P5/P6 luat theo truong", "ok = <loai:int len:->" in out
                    and "case_count = <loai:bool len:->" in out and "error = <loai:str" in out
                    and "problems = [NO_BUNDLED_CASES, <loai:str len:15>, <loai:str" in out)
            and _ve("A6 X1 ngoai le: lop + vi tri; lop dong => khong in", "  ! ca_nem: OSError len:" in out
                    and " tai eol_policy_test.py:" in out and "  ! ca_nem_lop_dong: <lop khong in> len:1" in out
                    and out.count("  ! ca: ValueError len:1 tai eol_policy_test.py:") == 2)
            and _ve("A6 M4 loi ghi => CHAN_DOAN_LOI", "CHAN_DOAN_LOI: ZeroDivisionError len:" in out)
            and _ve("A6 X2 don dep", "PASS <lambda>" in out and "CHAN_DOAN_DON_DEP: PermissionError errno:13" in out
                    and "la_thu_muc_tam:True" in out and "D14_KHOA_GIA" not in out)
            and _ve("A7 tran gia tri / payload / khoi, dau cat con tong so muc",
                    all(_CD_TRAN_CHUOI - 2 <= len(_cat("x" * n, _CD_TRAN_CHUOI)) <= min(n, _CD_TRAN_CHUOI)
                        for n in (1999, 2000, 2001, 50000))
                    and sum(len(d) + 1 for d in dong_pl) <= _CD_TRAN_PAYLOAD and "/5000 muc]" in "".join(dong_pl)
                    and sum(len(d) + 1 for d in dai if d != "FAIL ca_dai") <= _CD_TRAN_CA and "…[cat khoi" in dai[-1]
                    and sum(len(d) + 1 for d in dai_tho if d.startswith("CHAN_DOAN")) <= _CD_TRAN_PAYLOAD)
            and _ve("A14 khong ham nao (tru main/_env_con) doc env", not env_sai)
            and _ve("A14 khong co bo che bi mat", not che))


def case_chan_doan_co_tho_chi_cuc_bo(root):
    """A13 (M8): `--chan-doan-tho` in được stderr thô ngoài CI (repr ngoại lệ vẫn bị cắt M5); có khoá `CI`/`GITHUB_ACTIONS`
    (kể cả rỗng) ⇒ rc 2, không chạy ca nào; không cờ ⇒ đường mặc định dù env đặt sẵn biến mang tên giống cờ;
    lỗi khi in một dòng chẩn đoán ⇒ `CHAN_DOAN_LOI`, suite vẫn chạy hết (M4, lượt 1 r3 F7)."""
    con = ("import os, runpy, sys\n"
           "ns = runpy.run_path(sys.argv[1], run_name='eol_tu_kiem')\n"
           "def ca_gia(r):\n"
           "    ns['_chay_tien_trinh']('python -c <ma tho>', [sys.executable, '-c',"
           " \"import sys; sys.stderr.write('WP1221_' + 'MA_THO'); sys.exit(4)\"])\n"
           "    return False\n"
           "def ca_nem(r):\n"
           "    raise ValueError('y' * 50000)\n"
           "ns['CASES'][:] = [ca_gia, ca_nem]\n"
           "class S:\n"
           "    lan = []\n"
           "    def write(self, d):\n"
           "        if d.startswith('CHAN_DOAN:') and not self.lan:\n"
           "            self.lan.append(1)\n"
           "            raise OSError(5, 'loi in')\n"
           "        return sys.__stdout__.write(d)\n"
           "    def flush(self):\n"
           "        sys.__stdout__.flush()\n"
           "if os.environ.get('WP1221_LOI_IN'):\n"
           "    sys.stdout = S()\n"
           "sys.exit(ns['main'](sys.argv[2:]))\n")
    nen = {k: v for k, v in _env_con().items() if k not in ("CI", "GITHUB_ACTIONS")}
    kq = {}
    for ten, co, them in (("a", ["--chan-doan-tho"], {}), ("b", ["--chan-doan-tho"], {"CI": ""}),
                          ("c", ["--chan-doan-tho"], {"GITHUB_ACTIONS": "true"}),
                          ("d", [], {"CHAN_DOAN_THO": "1", "EOL_TEST_CHAN_DOAN_THO": "1"}),
                          ("e", [], {"WP1221_LOI_IN": "1"})):
        p = subprocess.run([sys.executable, "-c", con, str(Path(__file__).resolve())] + co, env=dict(nen, **them),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        kq[ten] = (p.returncode, p.stdout.decode("utf-8", "replace"))
    _cd("A13 :: rc [a, b, c, d, e]", [kq[t][0] for t in "abcde"], (int,) * 5)
    tu_choi = "CHAN_DOAN_THO: tu choi"
    return (_ve("A13a co, ngoai CI: in tho, repr van bi cat", kq["a"][0] == 1 and "WP1221_MA_THO" in kq["a"][1]
                and "CHAN_DOAN_THO: BAT" in kq["a"][1]
                and max(len(d) for d in kq["a"][1].splitlines()) <= _CD_TRAN_CHUOI + 40)
            and _ve("A13b CI rong: tu choi", kq["b"][0] == 2 and tu_choi in kq["b"][1] and "FAIL" not in kq["b"][1])
            and _ve("A13c GITHUB_ACTIONS: tu choi", kq["c"][0] == 2 and tu_choi in kq["c"][1])
            and _ve("A13d khong co: mac dinh", kq["d"][0] == 1 and "WP1221_MA_THO" not in kq["d"][1]
                    and "CHAN_DOAN_THO" not in kq["d"][1] and "python -c <ma tho> :: rc = 4" in kq["d"][1])
            and _ve("A13e loi in dong chan doan khong thoat main", kq["e"][0] == 1 and "0/2 dat" in kq["e"][1]
                    and "CHAN_DOAN_LOI: OSError len:" in kq["e"][1]))


CASES = [
    case_new_file_crlf_bi_chan,
    case_new_file_lf_duoc_qua,
    case_ten_co_khoang_trang,
    case_ten_tieng_viet,
    case_cmd_lf_trong_index_duoc_qua,
    case_cmd_crlf_trong_index_bi_chan,
    case_golden_duoc_bo_qua,
    case_mixed_eol_bi_chan,
    case_lone_cr_bi_chan,
    case_khong_chi_so_voi_head,
    case_attr_doc_tu_gitattributes,
    case_rename_golden_sang_text_bi_chan,
    case_copy_golden_sang_text_bi_chan,
    case_rename_hop_le_van_qua,
    case_rename_dich_unicode_va_khoang_trang,
    case_parse_raw_z_hai_path,
    case_real_hook_rename_only_bi_chan,
    case_real_hook_rename_copy_only_bi_chan,
    case_release_bundle_chay_real_wp49_fragment,
    case_probe_hop_dong_canonical_o_cay_dev,
    case_probe_qua_bundled_topology_canonical,
    case_driver_that_chay_probe_tren_bundle_giai_nen,
    case_cong_bao_load_failed_truoc_trieu_chung,
    case_cong_bao_dev_discovery_failed_truoc_mismatch,
    case_cong_bao_fragment_failed_khi_run_tra_false,
    case_binary_nul_duoc_bo_qua,
    case_binary_khong_co_NUL_van_duoc_tha_nho_khai_text,
    case_moi_ho_binary_deu_duoc_tha,
    case_ho_binary_thieu_khai_thi_bi_bat,
    case_binary_giu_nguyen_byte_qua_renormalize,
    case_chan_doan_mac_dinh_khong_lo_bi_mat,
    case_chan_doan_co_tho_chi_cuc_bo,
]


def _in_dong(d):
    """M4: lỗi khi in MỘT dòng chẩn đoán không được thoát khỏi `main` (lượt 1 r3, F7)."""
    try:
        print(d)
    except Exception as exc:                             # noqa: BLE001
        try:
            print("CHAN_DOAN_LOI: %s" % _lop_loi(exc))
        except Exception:                                # noqa: BLE001 — luồng ra hỏng hẳn: không làm gì thêm
            pass


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    tho = "--chan-doan-tho" in argv
    if tho and ("CI" in os.environ or "GITHUB_ACTIONS" in os.environ):   # M8: CÓ MẶT là đủ, kể cả rỗng
        print("CHAN_DOAN_THO: tu choi — CI/GITHUB_ACTIONS duoc dat")
        return 2
    _CD_THO[0] = tho
    if tho:
        print("CHAN_DOAN_THO: BAT — output co the chua bi mat; khong dan vao CI/issue")
    dat = 0
    hong = []
    try:
        for case in CASES:
            ok, dong = _chay_mot_ca(case)
            trang_thai = "%s %s" % ("PASS" if ok else "FAIL", case.__name__)
            for d in dong:
                print(d) if d == trang_thai else _in_dong(d)
            if ok:
                dat += 1
            else:
                hong.append(case.__name__)
    finally:
        _CD_THO[0] = False
    print("\n%d/%d dat" % (dat, len(CASES)))
    if hong:
        print("HONG: %s" % ", ".join(hong))
    return 0 if not hong else 1


if __name__ == "__main__":
    sys.exit(main())
