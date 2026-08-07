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
    return subprocess.run(
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
    out = eol_policy.run(root, "staged")
    return out["ok"] is False and _paths(out) == {"moi.py"}


def case_new_file_lf_duoc_qua(root):
    _inject(root, "moi.py", b"a = 1\nb = 2\n")
    out = eol_policy.run(root, "staged")
    return out["ok"] is True and out["checked"] == 1


def case_ten_co_khoang_trang(root):
    """`for f in $staged` cua hook cu tach theo khoang trang -> mot ten thanh hai path ma."""
    _inject(root, "thu muc/ghi chu.md", b"x\r\ny\r\n")
    out = eol_policy.run(root, "staged")
    return out["ok"] is False and _paths(out) == {"thu muc/ghi chu.md"}


def case_ten_tieng_viet(root):
    """Kho nay checkout o `D:/Quốc hội/tra-luat`; ten co dau khong phai gia dinh."""
    ten = "tài liệu/Quốc hội.md"
    _inject(root, ten, b"x\r\ny\r\n")
    out = eol_policy.run(root, "staged")
    return out["ok"] is False and _paths(out) == {ten}


def case_cmd_lf_trong_index_duoc_qua(root):
    """`*.cmd text eol=crlf`: index van phai LF, CRLF chi sinh ra luc checkout."""
    _inject(root, "setup.cmd", b"@echo off\nexit /b 0\n")
    out = eol_policy.run(root, "staged")
    return out["ok"] is True and out["checked"] == 1


def case_cmd_crlf_trong_index_bi_chan(root):
    _inject(root, "setup.cmd", b"@echo off\r\nexit /b 0\r\n")
    out = eol_policy.run(root, "staged")
    if out["ok"] is not False or _paths(out) != {"setup.cmd"}:
        return False
    # Thong diep phai noi ro index-LF/checkout-CRLF, neu khong nguoi sua mo tep tren dia thay
    # CRLF dung nhu mong doi va ket luan validator sai.
    return "checkout" in out["violations"][0]["expected"]


def case_golden_duoc_bo_qua(root):
    """`references/golden/** -text`: golden so BYTE, validator khong duoc dung vao."""
    _inject(root, "references/golden/fix.json", b"{\r\n  \"a\": 1\r\n}\r\n")
    out = eol_policy.run(root, "staged")
    return out["ok"] is True and out["checked"] == 0 and out["skipped"] == 1


def case_mixed_eol_bi_chan(root):
    _inject(root, "tron.txt", b"a\r\nb\nc\r\n")
    out = eol_policy.run(root, "staged")
    return (out["ok"] is False and _paths(out) == {"tron.txt"}
            and out["violations"][0]["error"] == "MIXED_EOL_IN_INDEX")


def case_lone_cr_bi_chan(root):
    _inject(root, "co.txt", b"a\rb\r")
    out = eol_policy.run(root, "staged")
    return (out["ok"] is False and _paths(out) == {"co.txt"}
            and out["violations"][0]["error"] == "LONE_CR_IN_INDEX")


def case_khong_chi_so_voi_head(root):
    """CRLF DA NAM trong HEAD va khong doi: hook cu thay "khong flip" nen cho qua.

    Validator hoi "co dung policy khong", khong hoi "co DOI khong" — nen `--all` van bat duoc.
    `--staged` sach la dung: khong co gi dang stage. Do la ly do CI phai chay `--all`.
    """
    _commit_blob(root, "cu.py", b"a = 1\r\n", "legacy crlf")
    staged = eol_policy.run(root, "staged")
    allrun = eol_policy.run(root, "all")
    return (staged["ok"] is True and staged["scanned"] == 0
            and allrun["ok"] is False and _paths(allrun) == {"cu.py"})


def case_attr_doc_tu_gitattributes(root):
    """Policy khong duoc chep cung: doi `.gitattributes` trong index thi verdict phai doi theo."""
    _inject(root, "x.txt", b"a\r\nb\r\n")
    truoc = eol_policy.run(root, "staged")
    _inject(root, ".gitattributes", _ATTRS + b"x.txt -text\n")
    sau = eol_policy.run(root, "staged")
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
    out = eol_policy.run(root, "staged")
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
    out = eol_policy.run(root, "staged")
    return out["ok"] is False and "ban_sao.txt" in _paths(out)


def case_rename_hop_le_van_qua(root):
    """Phan chung P1(c). Rename giua hai path text tren blob LF phai KHONG bi chan."""
    _commit_blob(root, "cu.py", b"a = 1\n", "lf source")
    _git(root, "mv", "cu.py", "moi.py")
    out = eol_policy.run(root, "staged")
    return out["ok"] is True and out["scanned"] == 1 and out["checked"] == 1


def case_rename_dich_unicode_va_khoang_trang(root):
    """Phan chung P1(d). Path DICH co dau va dau cach phai duoc bao nguyen ven."""
    ten = "tài liệu/Quốc hội mới.md"
    _commit_blob(root, "references/golden/fix.json", b"a\r\nb\r\n", "golden")
    (root / "tài liệu").mkdir(parents=True, exist_ok=True)   # `git mv` doi thu muc dich co san
    _git(root, "mv", "references/golden/fix.json", ten)
    out = eol_policy.run(root, "staged")
    return out["ok"] is False and _paths(out) == {ten}


def case_parse_raw_z_hai_path(root):
    """Parser phai nhay 3 o cho `R`/`C` va LUON lay path DICH.

    Nhay 2 o thi con tro lech va MOI ban ghi sau do bi doc sai — nen ca nay ghep mot ban ghi
    rename, mot ban ghi copy va mot ban ghi modify lien tiep de bat dung loi lech do.
    """
    z = (b":100644 100644 " + b"a" * 40 + b" " + b"b" * 40 + b" R100\x00src.txt\x00dst.txt\x00"
         b":100644 100644 " + b"c" * 40 + b" " + b"d" * 40 + b" C75\x00from.txt\x00to.txt\x00"
         b":100644 100644 " + b"e" * 40 + b" " + b"f" * 40 + b" M\x00plain.txt\x00")
    got = eol_policy.parse_raw_z(z)
    return got == [("dst.txt", "b" * 40), ("to.txt", "d" * 40), ("plain.txt", "f" * 40)]


def case_real_hook_rename_only_bi_chan(root):
    """Integration: chính pre-commit hook phải chặn stage chỉ có một bản ghi R100."""
    _commit_blob(root, "references/golden/fix.json", b"a\r\nb\r\n", "golden")
    _git(root, "mv", "references/golden/fix.json", "moved.txt")
    statuses = _staged_statuses(root)
    proc = _commit_through_real_hook(root)
    output = (proc.stdout + proc.stderr).decode("utf-8", "replace")
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
    proc = subprocess.run(
        [sys.executable, str(_SOURCE_ROOT / "scripts" / "tl.py"),
         "release-bundle", "--root", str(_SOURCE_ROOT),
         "--out", str(out_zip), "--top", "tra-luat", "--json"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if proc.returncode != 0 or not out_zip.is_file():
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
raise SystemExit(0 if ok else 1)
'''
    checked = subprocess.run(
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
    proc = subprocess.run(
        [sys.executable, str(_CONG_BUNDLE_FRAGMENT), "--json"],
        cwd=str(copy), env=_env_con(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        payload = json.loads(proc.stdout.decode("utf-8", "replace"))
    except ValueError:
        payload = {}
    return proc.returncode, payload


def _truoc(problems, truoc, sau):
    return truoc in problems and sau in problems and problems.index(truoc) < problems.index(sau)


def case_probe_hop_dong_canonical_o_cay_dev(root):
    """Probe HỢP LỆ phải qua được cả discovery lẫn runtime dev của hợp đồng canonical."""
    if ("TEST_ID: str = 'wp999_file_probe'" not in _PROBE_FILE_SRC
            or "__file__" not in _PROBE_FILE_SRC):
        return False
    tf = _hop_dong_fragment()
    scripts = root.parent / "dev" / "scripts"
    frag = scripts / "test_fragments"
    frag.mkdir(parents=True)
    (frag / (_PROBE_FILE_ID + ".py")).write_text(_PROBE_FILE_SRC, encoding="utf-8", newline="\n")

    ids = {entry.test_id for entry in tf.discover_fragment_test_ids(frag)}
    cases = tf.load_runtime_fragment_cases(scripts)
    return (ids == {_PROBE_FILE_ID}
            and len(cases) == 1 and cases[0].test_id == _PROBE_FILE_ID
            and cases[0].run(object()) is True)


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
    return (len(cases) == 1 and cases[0].test_id == _PROBE_FILE_ID
            and cases[0].run(object()) is True)


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
    proc = subprocess.run(
        [sys.executable, str(_CANONICAL_SCRIPTS / "tl.py"), "release-bundle",
         "--root", str(_SOURCE_ROOT), "--out", str(out_zip), "--top", "tra-luat", "--json"],
        env=_env_con(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0 or not out_zip.is_file():
        return False
    goi = root.parent / "giai-nen" / "tra-luat"
    with zipfile.ZipFile(out_zip) as archive:
        archive.extractall(goi.parent)
    if (goi / "scripts" / "test_fragments").exists() or (goi / ".editorconfig").exists():
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
    chay = subprocess.run(
        [sys.executable, str(driver), str(goi)], cwd=str(goi), env=_env_con(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        payload = json.loads(chay.stdout.decode("utf-8", "replace"))
    except ValueError:
        return False
    cases = payload.get("cases") or []
    return (payload.get("load_error") is None
            and len(cases) == len(goc) + 1
            and all(c.get("ok") for c in cases)
            and any(c.get("test_id") == _PROBE_FILE_ID for c in cases))


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
    return (rc == 1 and p.get("ok") is False
            and p.get("error") == "BUNDLED_FRAGMENT_LOAD_FAILED"
            and problems[:1] == ["BUNDLED_FRAGMENT_LOAD_FAILED"]
            and _PROBE_LOAD_ID in (p.get("load_error") or "")
            and p.get("case_count") == 0
            and p.get("dev_discovery_error") is None
            and _truoc(problems, "BUNDLED_FRAGMENT_LOAD_FAILED", "NO_BUNDLED_CASES")
            and _truoc(problems, "BUNDLED_FRAGMENT_LOAD_FAILED", "TEST_ID_SET_MISMATCH"))


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
    return (rc == 1 and p.get("ok") is False
            and p.get("error") == "DEV_FRAGMENT_DISCOVERY_FAILED"
            and problems[:1] == ["DEV_FRAGMENT_DISCOVERY_FAILED"]
            and "INVALID_FRAGMENT_PATH" in (p.get("dev_discovery_error") or "")
            and p.get("load_error") is None
            and p.get("case_count") == len(_fragment_canonical())
            and not p.get("failed")
            and _truoc(problems, "DEV_FRAGMENT_DISCOVERY_FAILED", "TEST_ID_SET_MISMATCH"))


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
    return (rc == 1 and p.get("ok") is False
            and (p.get("problems") or []) == ["BUNDLED_FRAGMENT_FAILED"]
            and p.get("error") == "BUNDLED_FRAGMENT_FAILED"
            and hong == {_PROBE_FAIL_ID}
            and p.get("load_error") is None
            and p.get("dev_discovery_error") is None
            and p.get("dev_test_ids") == p.get("bundle_test_ids")
            and p.get("case_count") == len(_fragment_canonical()) + 1)


# ── P2: binary khai -text, khong dua vao NUL ──────────────────────────────────────────────────

def case_binary_nul_duoc_bo_qua(root):
    """`text=auto` coi blob co NUL la binary — luoi CUOI, khong phai co che chinh."""
    _inject(root, "data.unknownext", b"\x89PNG\r\n\x1a\n\x00\x00\x00\x0d")
    out = eol_policy.run(root, "staged")
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
    out = eol_policy.run(root, "staged")
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
    out = eol_policy.run(root, "staged")
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
    out = eol_policy.run(root, "staged")
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
    out = eol_policy.run(root, "all")
    return sau_pdf == pdf and sau_zip == zipish and out["ok"] is True


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
]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    dat = 0
    hong = []
    for case in CASES:
        with tempfile.TemporaryDirectory(prefix="eol_policy_") as tmp:
            root = Path(tmp) / "kho"
            root.mkdir()
            _init(root)
            try:
                ok = bool(case(root))
            except Exception as exc:                     # noqa: BLE001 — bao loi, khong nuot
                ok = False
                print("  ! %s: %r" % (case.__name__, exc))
        print("%s %s" % ("PASS" if ok else "FAIL", case.__name__))
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
