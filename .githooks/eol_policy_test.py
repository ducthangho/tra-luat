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

import importlib.util
import json
import os
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


# ── wp1221: ca đỏ phải nói VÌ SAO ────────────────────────────────────────────────────────────────
#
# Mỗi ca chỉ trả `bool`, nên trước bản vá một ca đỏ chỉ để lại dòng `FAIL <ca>`: CI Windows run
# 41975947155 ra 28/30 mà không biết fragment nào hỏng. Kênh dưới đây cho ca GHI lại thứ nó đã thấy
# (rc, stderr, payload, vế nào trượt); `main()` chỉ in khi ca FAIL. Bất biến (đặc tả wp1221 r2, M4):
# phần ghi KHÔNG BAO GIỜ đổi kết quả ca — mọi lỗi của nó bị bắt và chỉ in thành `CHAN_DOAN_LOI`.
_CD_TRAN_CHUOI = 2000       # mỗi giá trị chuỗi: giữ ĐUÔI (lỗi Python/git nằm ở cuối)
_CD_TRAN_PAYLOAD = 4000     # payload JSON tuần tự hoá
_CD_TRAN_CA = 12000         # cả khối chẩn đoán của một ca (đã TÍNH chỗ cho dấu cắt)
_CD_CHO_DAU_CAT = 80        # ngân sách dành sẵn cho dòng `…[cat khoi …]`
_CD_TU_ENV = ("TOKEN", "SECRET", "KEY", "PAT", "PASSWORD", "AUTH", "COOKIE")
_CD_NGAN_XEP = [[]]          # ngăn xếp kênh; `_chay_mot_ca` đẩy một kênh mới cho mỗi ca
_CD_BO_CHE = []              # (tên, regex) nạp từ `_CD_NGUON_MAU` — KHÔNG chép bảng vào tệp này
_CD_NGUON_MAU = _CANONICAL_SCRIPTS / "pkg_secret_scan.py"


def _nap_bo_che():
    """Bảng mẫu bí mật của kho, nạp từ ĐÚNG một chỗ (CLAUDE.md: hai bản sẽ trôi lệch).

    Nạp NGUYÊN TỬ: dựng bảng tạm, kiểm từng mục, chỉ công bố vào cache khi đủ cả. Hỏng ⇒ `None`,
    và `_che` từ chối in mọi giá trị (fail-closed). Cache dở không bao giờ được dùng lại.
    """
    if _CD_BO_CHE:
        return _CD_BO_CHE
    try:
        spec = importlib.util.spec_from_file_location("_wp1221_pkg_secret_scan", _CD_NGUON_MAU)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        bang = [(ten, mau) for ten, mau in mod.PATTERNS]
        if not bang or not all(type(t) is str and callable(getattr(m, "sub", None)) for t, m in bang):
            return None
    except Exception:                                    # noqa: BLE001 — fail-closed ở `_che`
        return None
    _CD_BO_CHE[:] = bang
    return _CD_BO_CHE


def _che(text):
    """Che bí mật trong MỘT chuỗi: giá trị env có tên nhạy cảm (cả dạng đã thoát JSON/repr) rồi
    mẫu của `pkg_secret_scan` (đặc tả M3). Gọi trên chuỗi LÁ, trước mọi bước tuần tự hoá."""
    bang = _nap_bo_che()
    if bang is None:
        return "<CHE:khong_nap_duoc_bang_mau — khong in gia tri>"
    dang = []
    for ten, gt in os.environ.items():
        if len(gt) >= 8 and any(tu in ten.upper() for tu in _CD_TU_ENV):
            for d in {gt, json.dumps(gt)[1:-1], json.dumps(gt, ensure_ascii=False)[1:-1], repr(gt)[1:-1]}:
                dang.append((d, ten))
    for gt, ten in sorted(dang, key=lambda x: -len(x[0])):  # dài trước: chuỗi con không che dở
        text = text.replace(gt, "<CHE:env:%s>" % ten)
    for ten, mau in bang:
        text = mau.sub("<CHE:%s>" % ten, text)
    return text


_TEN_LOP = type.__dict__["__name__"].__get__   # đọc tên lớp KHÔNG qua metaclass (lượt review 2, F3)


def _la(t, *kieu):
    """`t` là đúng một trong các kiểu — so bằng `is`, không `in`/`==` (metaclass có thể hook `__eq__`)."""
    return any(t is k for k in kieu)


def _vat_hoa(x, sau=0):
    """Dựng bản BUILTIN đã che của `x`: không gọi `repr`/hook nào của đối tượng lạ (đặc tả M4)."""
    t = type(x)
    if t is str:
        return _che(x)
    if _la(t, bytes, bytearray):
        return _che(bytes(x).decode("utf-8", "replace"))
    if x is None or _la(t, bool, int, float):
        return x
    if sau >= 6:
        return "<sau qua 6 tang>"
    if t is dict:
        cap = list(x.items())
        r = {(_che(k) if type(k) is str else "<khoa:%s>" % _TEN_LOP(type(k))): _vat_hoa(v, sau + 1)
             for k, v in cap[:200]}
        if len(cap) > 200:
            r["<cat>"] = "bo %d muc" % (len(cap) - 200)
        return r
    if _la(t, list, tuple, set, frozenset):
        cap = list(x)
        return [_vat_hoa(v, sau + 1) for v in cap[:200]] + (["<cat %d muc>" % (len(cap) - 200)] if len(cap) > 200 else [])
    return "<%s>" % _TEN_LOP(t)


def _ghi_an_toan(ham):
    """Chạy một bước GHI chẩn đoán; mọi lỗi của nó (kể cả BaseException trừ Ctrl-C) thành `CHAN_DOAN_LOI`."""
    try:
        ham()
    except KeyboardInterrupt:
        raise
    except BaseException as exc:                         # noqa: BLE001 — M4: không đổi kết quả ca
        _CD_NGAN_XEP[-1].append(("CHAN_DOAN_LOI", _loi_an_toan(exc)))


def _loi_an_toan(exc):
    """Mô tả lỗi đã che, dựng từ `args` qua `_vat_hoa` (không `repr` đối tượng); hỏng ⇒ chỉ tên lớp."""
    try:
        than = [_vat_hoa(a) for a in exc.args] + [_vat_hoa(getattr(exc, "filename", None))]
        return _cat_duoi(_che("%s%s" % (_TEN_LOP(type(exc)), json.dumps(than, ensure_ascii=False))),
                         _CD_TRAN_CHUOI)
    except KeyboardInterrupt:
        raise
    except BaseException:                                # noqa: BLE001
        return "<loi khong mo ta duoc>"


def _cat_duoi(text, tran):
    if len(text) <= tran:
        return text
    return "…[cat %d ky tu dau]" % (len(text) - tran) + text[-tran:]


def _cd(nhan, gia_tri):
    """Ghi một cặp `nhãn → giá trị` vào kênh của ca đang chạy; trả lại `gia_tri` nguyên vẹn.

    Không bao giờ đổi kết quả ca (đặc tả M4): chỉ đọc kiểu builtin, mọi lỗi thành `CHAN_DOAN_LOI`.
    """
    def ghi():
        if _la(type(gia_tri), str, bytes, bytearray):
            chuoi, tran = _vat_hoa(gia_tri), _CD_TRAN_CHUOI
        else:   # che LÁ (dạng thoát) rồi che CẢ chuỗi cuối: số/tên lớp sinh ra khi tuần tự hoá (F8)
            chuoi = _che(json.dumps(_vat_hoa(gia_tri), ensure_ascii=False, sort_keys=True))
            tran = _CD_TRAN_PAYLOAD
        _CD_NGAN_XEP[-1].append((_che(str(nhan)), _cat_duoi(chuoi, tran)))
    _ghi_an_toan(ghi)
    return gia_tri


def _ve(nhan, gia_tri):
    """Ghi giá trị một vế của biểu thức quyết định, trả lại nó — dùng TRONG chuỗi `and`.

    Giữ nguyên short-circuit: vế cuối cùng được ghi chính là vế đã trượt. Không gọi `bool()` thêm.
    """
    _cd("ve:" + nhan, gia_tri)
    return gia_tri


def _ten_ngan(arg):
    s = str(arg)
    return os.path.basename(s) if (os.sep in s or "/" in s) else s


def _chay_tien_trinh(nhan, cmd, **kw):
    """`subprocess.run` + ghi lệnh rút gọn, rc, stdout, stderr. Không bao giờ ghi `env`."""
    kw.setdefault("stdout", subprocess.PIPE)
    kw.setdefault("stderr", subprocess.PIPE)
    proc = subprocess.run(cmd, **kw)

    def ghi():
        _cd(nhan + ".lenh", " ".join(_ten_ngan(a) for a in cmd[:4]))
        _cd(nhan + ".rc", proc.returncode)
        for kenh in ("stdout", "stderr"):
            if getattr(proc, kenh):
                _cd(nhan + "." + kenh, getattr(proc, kenh))
    _ghi_an_toan(ghi)
    return proc


def _chay_policy(root, mode):
    """`eol_policy.run` + ghi payload trả về (nhóm B của đặc tả wp1221)."""
    out = eol_policy.run(root, mode)
    _cd("eol_policy.run(%s)" % mode, out)
    return out


_KHOA_PAYLOAD_CONG = ("ok", "error", "problems", "failed", "load_error", "dev_discovery_error",
                      "case_count", "dev_test_ids", "bundle_test_ids")


def _ghi_payload_cong(nhan, payload):
    def ghi():
        if type(payload) is not dict:
            return _cd(nhan + ".payload_khong_phai_dict", type(payload).__name__)
        _cd(nhan + ".payload", {k: payload[k] for k in _KHOA_PAYLOAD_CONG if k in payload})
        cases = payload.get("cases")
        hong = [c for c in cases if not (type(c) is dict and c.get("ok") is True)] if type(cases) is list else cases
        if hong:
            _cd(nhan + ".cases_khong_ok", hong)
    _ghi_an_toan(ghi)


def _khoi_chan_doan(ghi, tran=None):
    """Dựng các dòng chẩn đoán từ kênh `ghi`. Mọi dòng bắt đầu bằng tiền tố `CHAN_DOAN`."""
    tran = _CD_TRAN_CA if tran is None else tran
    if not ghi:
        return ["CHAN_DOAN: (rong — ca khong ghi chan doan)"]
    dong, tong = [], 0
    for i, (nhan, chuoi) in enumerate(ghi):
        if nhan == "CHAN_DOAN_LOI":
            moi = ["CHAN_DOAN_LOI: %s" % chuoi]
        else:
            phan = chuoi.splitlines() or [""]
            moi = ["CHAN_DOAN: %s = %s" % (nhan, phan[0])]
            moi += ["CHAN_DOAN:   | %s" % p for p in phan[1:]]
        do_dai = sum(len(d) + 1 for d in moi)
        if tong + do_dai > tran - _CD_CHO_DAU_CAT:
            con = sum(len(n) + len(c) for n, c in ghi[i:])
            dong.append("CHAN_DOAN: …[cat khoi: bo %d muc, ~%d ky tu]" % (len(ghi) - i, con))
            break
        dong += moi
        tong += do_dai
    return dong


def _don_thu_muc_tam(td):
    td.cleanup()


def _chay_mot_ca(case, don_dep=None):
    """Chạy MỘT ca trong thư mục tạm riêng; trả `(ok, dòng_cần_in)`.

    Lỗi dọn thư mục tạm (Windows khoá tệp) KHÔNG làm sập suite và KHÔNG đổi kết quả ca: nó chỉ
    thành một dòng `CHAN_DOAN_DON_DEP` (đặc tả wp1221 r2, M7). Lỗi của `_init` vẫn ném như trước.
    """
    don_dep = _don_thu_muc_tam if don_dep is None else don_dep
    ghi, truoc, sau, loi_don = [], [], [], None
    td = tempfile.TemporaryDirectory(prefix="eol_policy_")
    _CD_NGAN_XEP.append(ghi)
    try:
        root = Path(td.name) / "kho"
        root.mkdir()
        _init(root)
        try:
            ok = bool(case(root))
        except Exception as exc:                     # noqa: BLE001 — bao loi, khong nuot
            ok = False
            truoc.append("  ! %s: %s" % (case.__name__, _loi_an_toan(exc)))
    finally:
        _CD_NGAN_XEP.pop()
        try:
            don_dep(td)
        except OSError as exc:
            loi_don = exc
    if loi_don is not None:
        try:
            sau.append(_cat_duoi("CHAN_DOAN_DON_DEP: %s (%s)" % (_loi_an_toan(loi_don), _vat_hoa(td.name)),
                                 _CD_TRAN_CHUOI))
        except KeyboardInterrupt:
            raise
        except BaseException:                        # noqa: BLE001 — M7: không làm sập suite (F9)
            sau.append("CHAN_DOAN_DON_DEP: <loi don thu muc tam; khong mo ta duoc an toan>")
    if not ok:
        try:     # dòng dọn dẹp tính vào trần toàn khối (F4)
            sau += _khoi_chan_doan(ghi, _CD_TRAN_CA - sum(len(d) + 1 for d in sau))
        except KeyboardInterrupt:
            raise
        except BaseException as exc:                 # noqa: BLE001 — M4: không đổi kết quả
            sau.append("CHAN_DOAN_LOI: %s" % _loi_an_toan(exc))
    return ok, truoc + ["%s %s" % ("PASS" if ok else "FAIL", case.__name__)] + sau


def _git(root, *args, stdin=None):
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


def _commit_through_real_hook(root):
    _install_real_pre_commit(root)
    return _chay_tien_trinh(
        "git_commit_qua_hook",
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
    got = _cd("parse_raw_z", eol_policy.parse_raw_z(z))
    return got == [("dst.txt", "b" * 40), ("to.txt", "d" * 40), ("plain.txt", "f" * 40)]


def case_real_hook_rename_only_bi_chan(root):
    """Integration: chính pre-commit hook phải chặn stage chỉ có một bản ghi R100."""
    _commit_blob(root, "references/golden/fix.json", b"a\r\nb\r\n", "golden")
    _git(root, "mv", "references/golden/fix.json", "moved.txt")
    statuses = _staged_statuses(root)
    proc = _commit_through_real_hook(root)
    output = (proc.stdout + proc.stderr).decode("utf-8", "replace")
    _ghi_an_toan(lambda: _cd("cac_ve", {          # ĐỦ mọi vế, từ dữ liệu đã có; không gọi lại commit
        "statuses": statuses, "statuses==R100": statuses == ["R100"], "rc!=0": proc.returncode != 0,
        "CRLF_IN_INDEX in output": "CRLF_IN_INDEX" in output, "moved.txt in output": "moved.txt" in output}))
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
    _ghi_an_toan(lambda: _cd("cac_ve", {
        "statuses": statuses, "statuses==C100,R100": sorted(statuses) == ["C100", "R100"],
        "rc!=0": proc.returncode != 0, "CRLF_IN_INDEX in output": "CRLF_IN_INDEX" in output,
        "copied.txt in output": "copied.txt" in output, "moved.txt in output": "moved.txt" in output}))
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
        "release-bundle",
        [sys.executable, str(_SOURCE_ROOT / "scripts" / "tl.py"),
         "release-bundle", "--root", str(_SOURCE_ROOT),
         "--out", str(out_zip), "--top", "tra-luat", "--json"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if proc.returncode != 0 or not out_zip.is_file():
        _cd("tra_false_som", "release-bundle hong: rc=%s, co_zip=%s" % (proc.returncode, out_zip.is_file()))
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
        _cd("tra_false_som", "bo cuc goi sai: %s" % {
            ".editorconfig": (package_root / ".editorconfig").exists(),
            "scripts/test_fragments": (package_root / "scripts" / "test_fragments").exists(),
            ".gitattributes": (package_root / ".gitattributes").is_file(),
            "tl_test_fragments_bundled.py":
                (package_root / "scripts" / "tl_test_fragments_bundled.py").is_file()})
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
if not ok:
    sys.stderr.write("probe: topology=%r targets=%d\n" % (topology, len(targets)))
raise SystemExit(0 if ok else 1)
'''
    checked = _chay_tien_trinh(
        "probe_wp49_trong_goi",
        [sys.executable, "-c", probe, str(package_root)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
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
        "cong_bundle_fragment",
        [sys.executable, str(_CONG_BUNDLE_FRAGMENT), "--json"],
        cwd=str(copy), env=_env_con(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        payload = json.loads(proc.stdout.decode("utf-8", "replace"))
    except ValueError:
        _cd("cong_bundle_fragment.stdout_khong_phai_json", proc.stdout)
        payload = {}
    if isinstance(payload, dict):
        _ghi_payload_cong("cong_bundle_fragment", payload)
    return proc.returncode, payload


def _truoc(problems, truoc, sau):
    return truoc in problems and sau in problems and problems.index(truoc) < problems.index(sau)


def case_probe_hop_dong_canonical_o_cay_dev(root):
    """Probe HỢP LỆ phải qua được cả discovery lẫn runtime dev của hợp đồng canonical."""
    if ("TEST_ID: str = 'wp999_file_probe'" not in _PROBE_FILE_SRC
            or "__file__" not in _PROBE_FILE_SRC):
        _cd("tra_false_som", "_PROBE_FILE_SRC thieu dong TEST_ID annotated hoac __file__")
        return False
    tf = _hop_dong_fragment()
    scripts = root.parent / "dev" / "scripts"
    frag = scripts / "test_fragments"
    frag.mkdir(parents=True)
    (frag / (_PROBE_FILE_ID + ".py")).write_text(_PROBE_FILE_SRC, encoding="utf-8", newline="\n")

    ids = _cd("ids_do_duoc", {entry.test_id for entry in tf.discover_fragment_test_ids(frag)})
    cases = tf.load_runtime_fragment_cases(scripts)
    _ghi_an_toan(lambda: _cd("cases_nap_duoc", [c.test_id for c in cases]))
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
    _ghi_an_toan(lambda: _cd("cases_nap_duoc", [c.test_id for c in cases]))
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
        "release-bundle",
        [sys.executable, str(_CANONICAL_SCRIPTS / "tl.py"), "release-bundle",
         "--root", str(_SOURCE_ROOT), "--out", str(out_zip), "--top", "tra-luat", "--json"],
        env=_env_con(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0 or not out_zip.is_file():
        _cd("tra_false_som", "release-bundle hong: rc=%s, co_zip=%s" % (proc.returncode, out_zip.is_file()))
        return False
    goi = root.parent / "giai-nen" / "tra-luat"
    with zipfile.ZipFile(out_zip) as archive:
        archive.extractall(goi.parent)
    if (goi / "scripts" / "test_fragments").exists() or (goi / ".editorconfig").exists():
        _cd("tra_false_som", "bo cuc goi sai: test_fragments=%s editorconfig=%s" % (
            (goi / "scripts" / "test_fragments").exists(), (goi / ".editorconfig").exists()))
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
        "driver_cong",
        [sys.executable, str(driver), str(goi)], cwd=str(goi), env=_env_con(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        payload = json.loads(chay.stdout.decode("utf-8", "replace"))
    except ValueError:
        _cd("tra_false_som", "stdout cua driver khong phai JSON")
        return False
    _cd("so_fragment_canonical", len(goc))
    if isinstance(payload, dict):
        _ghi_payload_cong("driver_cong", payload)
    cases = payload.get("cases") or []
    return (_ve("payload.get('load_error') is None", payload.get("load_error") is None)
            and _ve("len(cases) == len(goc) + 1", len(cases) == len(goc) + 1)
            and _ve("all(c.get('ok') for c in cases)", all(c.get("ok") for c in cases))
            and _ve("any(c.get('test_id') == _PROBE_FILE_ID for c in cases)", any(c.get("test_id") == _PROBE_FILE_ID for c in cases)))


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
    _cd("sau_pdf_giu_nguyen", sau_pdf == pdf)
    _cd("sau_zip_giu_nguyen", sau_zip == zipish)
    out = _chay_policy(root, "all")
    return sau_pdf == pdf and sau_zip == zipish and out["ok"] is True


# ── wp1221: tự kiểm kênh chẩn đoán ────────────────────────────────────────────────────────────

_MA_CD_NGAN = "WP1221_MA_NGAN"
_MA_CD_DUOI = "WP1221_MA_DUOI"
_MA_CD_DON = "WP1221_D14_KHOA_GIA"


def _ghi_vao_kenh_rieng(ham):
    """Chạy `ham()` với một kênh RIÊNG rồi trả `(kết_quả, ghi)`; kênh của ca gọi không bị chạm."""
    ghi = []
    _CD_NGAN_XEP.append(ghi)
    try:
        return ham(), ghi
    finally:
        _CD_NGAN_XEP.pop()


def case_chan_doan_kenh_in_che_cat(root):
    """Kênh chẩn đoán phải IN được rc + stderr, CHE được bí mật, CẮT giữ đuôi (đặc tả wp1221 M1/M3/M5/M6).

    Chuỗi bí mật dựng bằng ghép chuỗi LÚC CHẠY: viết nguyên văn vào tệp thì `pkg_secret_scan` của gói
    (hoặc của người đọc) sẽ bắt nhầm. Dùng CHÍNH `_chay_tien_trinh` / `_khoi_chan_doan` mà các ca thật
    dùng — chép lại một bản là đo bản chép.
    """
    bi_mat = "GOC" + "SPX-" + "Ab1x" * 6
    the = "wp1221" + "".join(chr(97 + (i * 7) % 26) for i in range(18))
    cu = os.environ.get("EOL_TEST_FAKE_TOKEN")
    os.environ["EOL_TEST_FAKE_TOKEN"] = the
    try:
        # Mã nhận biết dựng BÊN TRONG tiến trình con bằng ghép chuỗi: truyền qua argv thì nó hiện cả
        # ở dòng `.lenh`, và phép kiểm "có mã" luôn đúng dù stderr có được ghi hay không.
        ma_nguon = ("import os,sys; sys.stderr.write('WP1221_' + 'MA_NGAN ' + sys.argv[1] + ' '"
                    " + os.environ['EOL_TEST_FAKE_TOKEN'] + '\\n'); sys.exit(3)")
        _, ghi = _ghi_vao_kenh_rieng(lambda: _chay_tien_trinh(
            "gia", [sys.executable, "-c", ma_nguon, bi_mat]))
        ngan = "\n".join(_khoi_chan_doan(ghi))
    finally:
        if cu is None:
            os.environ.pop("EOL_TEST_FAKE_TOKEN", None)
        else:
            os.environ["EOL_TEST_FAKE_TOKEN"] = cu
    _cd("khoi_ngan", ngan)

    ma_dai = "import sys; sys.stderr.write('x' * 50000 + 'WP1221_' + 'MA_DUOI'); sys.exit(1)"
    _, ghi_dai = _ghi_vao_kenh_rieng(lambda: _chay_tien_trinh(
        "dai", [sys.executable, "-c", ma_dai]))
    dai = "\n".join(_khoi_chan_doan(ghi_dai))
    _cd("do_dai_khoi_dai", len(dai))

    def ca_gia_do(_root):
        return False

    def ca_gia_xanh(_root):
        _cd("khong_duoc_in_khi_PASS", "x")
        return True

    def don_hong(td):
        td.cleanup()
        raise PermissionError(_MA_CD_DON)

    class _StrNem:                                  # nhãn có __str__ ném: đường lỗi THẬT của `_cd`
        def __str__(self):
            raise RuntimeError("str hong " + bi_mat)

    _, ghi_loi = _ghi_vao_kenh_rieng(lambda: _cd(_StrNem(), 1))
    khoi_loi = "\n".join(_khoi_chan_doan(ghi_loi))
    _cd("khoi_loi", khoi_loi)

    ok_do, dong_do = _chay_mot_ca(ca_gia_do)
    ok_xanh, dong_xanh = _chay_mot_ca(ca_gia_xanh)
    ok_don, dong_don = _chay_mot_ca(ca_gia_xanh, don_dep=don_hong)
    _cd("dong_do", dong_do)
    _cd("dong_xanh", dong_xanh)
    _cd("dong_don", dong_don)

    nguon = Path(__file__).read_text(encoding="utf-8")
    dong_err = [d for d in ngan.split("\n") if d.startswith("CHAN_DOAN: gia.stderr = ")]
    dong_err_dai = "\n".join(d for d in dai.split("\n") if d.startswith("CHAN_DOAN: dai.stderr = "))
    return (_ve("ma ngan co trong dong stderr", any(_MA_CD_NGAN in d for d in dong_err))
            and _ve("rc = 3 co trong khoi", "gia.rc = 3" in ngan)
            and _ve("co dau <CHE:", "<CHE:google_oauth_client_secret>" in ngan)
            and _ve("bi mat tho KHONG co", bi_mat not in ngan)
            and _ve("env token bi che", "<CHE:env:EOL_TEST_FAKE_TOKEN>" in ngan and the not in ngan)
            and _ve("khoi dai <= tran", len(dai) <= _CD_TRAN_CA)
            and _ve("loi trong _cd thanh CHAN_DOAN_LOI da che",
                    khoi_loi.startswith("CHAN_DOAN_LOI: ") and bi_mat not in khoi_loi
                    and "<CHE:google_oauth_client_secret>" in khoi_loi)
            and _ve("khoi dai giu DUOI cua stderr", _MA_CD_DUOI in dong_err_dai and "…[cat " in dong_err_dai)
            and _ve("moi dong bat dau CHAN_DOAN", all(d.startswith("CHAN_DOAN") for d in dai.split("\n")))
            and _ve("ca do khong ghi => dong rong tuong minh",
                    ok_do is False and dong_do == ["FAIL ca_gia_do",
                                                    "CHAN_DOAN: (rong — ca khong ghi chan doan)"])
            and _ve("ca PASS khong in chan doan", ok_xanh is True and dong_xanh == ["PASS ca_gia_xanh"])
            and _ve("loi don dep khong doi ket qua", ok_don is True and dong_don[0] == "PASS ca_gia_xanh")
            and _ve("loi don dep in dung mot dong ngay duoi",
                    len(dong_don) == 2 and dong_don[1].startswith("CHAN_DOAN_DON_DEP: ")
                    and sum(d.count(_MA_CD_DON) for d in dong_don) == 1)
            and _ve("bang mau nap tu pkg_secret_scan, khong chep",
                    "pkg_secret_scan.py" in nguon and ("GOC" + "SPX") not in nguon
                    and bool(_nap_bo_che())))


def case_chan_doan_vat_hoa_va_nguon_mau(root):
    """Lượt review 1 của wp1221 (F1–F6): che TRƯỚC khi thoát ký tự, không gọi hook, nạp bảng nguyên tử.

    Mỗi vế là một phản chứng của reviewer, dựng lại bằng dữ liệu giả; mọi trạng thái toàn cục bị thay
    (env, `tempfile.tempdir`, nguồn bảng mẫu, cache) được khôi phục trong `finally`.
    """
    bi_mat = "GOC" + "SPX-" + "Ab1x" * 6
    the = 'wp1221"q\\b' + "".join(chr(97 + (i * 5) % 26) for i in range(14))   # có `"` và `\`
    goc = (os.environ.get("EOL_TEST_FAKE_TOKEN"), tempfile.tempdir, globals()["_CD_NGUON_MAU"],
           list(_CD_BO_CHE))
    tam = Path(root.parent) / "wp1221-nguon"
    tam.mkdir()
    try:
        os.environ["EOL_TEST_FAKE_TOKEN"] = the

        class _Moc:                                  # hook của đối tượng lạ KHÔNG được chạy (F3)
            goi = []

            def __repr__(self):
                _Moc.goi.append(1)
                raise SystemExit(23)
        out = {"ok": True, "x": _Moc()}
        _, g1 = _ghi_vao_kenh_rieng(lambda: (_cd("long", {"a": [the, {"b": bi_mat}]}), _cd("moc", out),
                                             _ghi_payload_cong("cong", {"ok": True, "cases": 1}),
                                             _chay_tien_trinh("con", [sys.executable, "-c",
                                                              "import json,os; print(json.dumps(os.environ['EOL_TEST_FAKE_TOKEN']))"])))
        k1 = "\n".join(_khoi_chan_doan(g1))
        _cd("khoi_vat_hoa", k1)
        dau_the = [the, json.dumps(the)[1:-1], repr(the)[1:-1]]

        tempfile.tempdir = str(tam / ("d-" + "Zq9" + "wp1221tmp" * 2))   # F2: đường dẫn mang giá trị env
        os.environ["EOL_TEST_FAKE_TOKEN"] = "Zq9" + "wp1221tmp" * 2

        def don_hong(td):
            td.cleanup()
            raise PermissionError("khoa")
        (tam / ("d-" + "Zq9" + "wp1221tmp" * 2)).mkdir()
        _, dong_don = _chay_mot_ca(lambda _r: True, don_dep=don_hong)
        tempfile.tempdir = goc[1]

        # F4: 6 mục x (17 + 1982 + 1) = ĐÚNG 12000 ký tự ⇒ không dành chỗ thì mục 7 đẩy dấu cắt vượt trần.
        _, g4 = _ghi_vao_kenh_rieng(lambda: [_cd("m%02d" % i, "y" * 1982) for i in range(7)])
        k4 = "\n".join(_khoi_chan_doan(g4))

        canary = "WP1221" + "CANARY" + "42"           # F5: bộ che phải đọc ĐÚNG nguồn đang trỏ tới
        (tam / "nguon_tot.py").write_text(
            "import re\nPATTERNS = [('canary', re.compile('WP1221' + 'CANARY[0-9]+'))]\n", encoding="utf-8")
        (tam / "nguon_do.py").write_text(               # F6: nạp dở rồi ném
            "import re\ndef _g():\n    yield ('a', re.compile('zzz'))\n    raise RuntimeError('do')\n"
            "PATTERNS = _g()\n", encoding="utf-8")
        _CD_BO_CHE[:] = []
        globals()["_CD_NGUON_MAU"] = tam / "nguon_tot.py"
        che_canary = _che(canary)
        _CD_BO_CHE[:] = []
        globals()["_CD_NGUON_MAU"] = tam / "nguon_do.py"
        che_do = [_che(bi_mat), _che(bi_mat)]
        do_dai_cache_do = len(_CD_BO_CHE)
        _CD_BO_CHE[:], globals()["_CD_NGUON_MAU"] = goc[3], goc[2]

        so = "7" + "3141592653" + "58979"                # lượt review 2: F8 số / tên lớp; F3 metaclass
        os.environ["EOL_TEST_FAKE_TOKEN"] = so
        goi = []

        class _Meta(type):
            def __eq__(cls, o):
                goi.append("eq")
                return False
            __hash__ = type.__hash__
            __name__ = property(lambda cls: goi.append("name"))
        _, g8 = _ghi_vao_kenh_rieng(lambda: (_cd("so", {"n": int(so), "o": type("T" + so, (), {})(),
                                                         "m": _Meta("M", (), {})()}),
                                             _ghi_payload_cong("cong", {"ok": True, "x": _Meta("N", (), {})()})))
        k8 = "\n".join(_khoi_chan_doan(g8)) + _loi_an_toan(type("E" + so, (Exception,), {})("x"))

        def ca_to(_r):        # F4: mục 1000 ký tự ⇒ khối dừng sát 11920; thiếu trừ dòng dọn dẹp là vượt
            [_cd("m%d" % i, "y" * 1000) for i in range(13)]
            return False
        def don_dai(td):                               # thông điệp dài: dòng dọn dẹp vượt chỗ dành sẵn
            td.cleanup()
            raise PermissionError("k" * 1500)
        _, dong_to = _chay_mot_ca(ca_to, don_dep=don_dai)

        class _SubHong:                                 # F9: bộ che ném lúc dựng dòng dọn dẹp
            def sub(self, *a):
                raise RuntimeError("WP1221_F9_" + "LOI_CHE")
        _CD_BO_CHE[:] = [("hong", _SubHong())]
        ok9, dong9 = _chay_mot_ca(lambda _r: True, don_dep=don_hong)
        _CD_BO_CHE[:] = goc[3]
    finally:
        tempfile.tempdir = goc[1]
        globals()["_CD_NGUON_MAU"] = goc[2]
        _CD_BO_CHE[:] = goc[3]
        if goc[0] is None:
            os.environ.pop("EOL_TEST_FAKE_TOKEN", None)
        else:
            os.environ["EOL_TEST_FAKE_TOKEN"] = goc[0]
    _cd("dong_don", dong_don)
    return (_ve("F1 env co \" va \\ bi che o moi dang", all(d not in k1 for d in dau_the)
                and k1.count("<CHE:env:EOL_TEST_FAKE_TOKEN>") >= 2)
            and _ve("F1 bi mat long trong dict bi che", bi_mat not in k1)
            and _ve("F3 khong goi hook cua doi tuong la", not _Moc.goi and '"x": "<_Moc>"' in k1)
            and _ve("F3 payload cong la khong lam hong", "CHAN_DOAN_LOI" not in k1)
            and _ve("F2 duong dan don dep da che", len(dong_don) == 2 and "wp1221tmpwp1221tmp" not in dong_don[1]
                    and "<CHE:env:EOL_TEST_FAKE_TOKEN>" in dong_don[1])
            and _ve("F4 khoi <= tran ke ca dau cat", len(k4) <= _CD_TRAN_CA and "…[cat khoi" in k4)
            and _ve("F5 doc dung nguon dang tro", che_canary == "<CHE:canary>")
            and _ve("F6 nap do => fail-closed ca hai lan, cache rong",
                    all(c.startswith("<CHE:khong_nap_duoc") for c in che_do) and do_dai_cache_do == 0)
            and _ve("F5 nguon mac dinh la bang chuan",
                    Path(goc[2]).resolve() == (_SOURCE_ROOT / "scripts" / "pkg_secret_scan.py").resolve())
            and _ve("F8 so/ten lop/ten loi da che", so not in k8 and k8.count("<CHE:env:EOL_TEST_FAKE_TOKEN>") >= 3)
            and _ve("F3 khong goi hook metaclass", goi == [])
            and _ve("F4 khoi + dong don dep <= tran",
                    sum(len(d) + 1 for d in dong_to if d.startswith("CHAN_DOAN")) <= _CD_TRAN_CA
                    and any(d.startswith("CHAN_DOAN_DON_DEP") for d in dong_to))
            and _ve("F9 che hong luc don dep khong sap suite",
                    ok9 is True and dong9[0] == "PASS <lambda>" and len(dong9) == 2 and dong9[1].startswith("CHAN_DOAN")
                    and "WP1221_F9_LOI_CHE" not in dong9[1]))


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
    case_chan_doan_kenh_in_che_cat,
    case_chan_doan_vat_hoa_va_nguon_mau,
]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    dat = 0
    hong = []
    for case in CASES:
        ok, dong = _chay_mot_ca(case)
        for d in dong:
            print(d)
        if ok:
            dat += 1
        else:
            hong.append(case.__name__)
    print("\n%d/%d dat" % (dat, len(CASES)))
    if hong:
        print("HONG: %s" % ", ".join(hong))
    return 0 if not hong else 1


if __name__ == "__main__":
    sys.exit(main())
