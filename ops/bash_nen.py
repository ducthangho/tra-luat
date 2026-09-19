#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MỘT chỗ duy nhất trả lời "dùng `bash` nào", cộng CỔNG chặn bản sao thứ tư.

VÌ SAO CÓ TỆP NÀY — ba lần cùng một khuyết tật, ba bộ giải riêng
================================================================
`shutil.which("bash")` trên Windows trả `C:\\Windows\\System32\\bash.exe` — **bộ phóng
WSL**, không phải bash POSIX. Kho đã trả giá cho đúng nó BA lần, và mỗi lần chữa bằng
một bộ giải RIÊNG:

  1. `t32` (`master e03c6d28`, run `32351777642`) ⇒ sinh `_bash_posix()` trong
     `ops/lease_publish_test.py`;
  2. `gate (windows-latest)` run `33612364175`, 02-09-2026 ⇒ sinh `_bash_windows()`
     trong `ops/cong_cu.py`;
  3. `t35`–`t40` (Issue #570, đo 19-09-2026 trên Windows thật) ⇒ sáu ca gọi
     `shutil.which("bash")` TRẦN, cách `_bash_posix()` chưa tới 300 dòng trong CÙNG tệp.

`CLAUDE.md`: *"cùng một hình dạng lặp ba lần trở lên thì câu hỏi đúng là CÓ NÊN LÀM VIỆC
NÀY KHÔNG, không phải VÁ THẾ NÀO"*. Chủ kho quyết: một bộ giải dùng chung, cộng một cổng
làm ĐỎ mọi lời gọi trần MỚI. Bản vá thứ tư theo kiểu cũ đã bị từ chối có chủ đích.

QUYẾT BẰNG NĂNG LỰC, KHÔNG BẰNG TÊN
===================================
Hai bộ giải cũ lọc theo TÊN/đường dẫn: `_bash_posix` loại chuỗi `"system32"`,
`_bash_windows` loại mọi thứ dưới `%SystemRoot%`. Đó đúng hình dạng *"danh sách CẤM không
bao giờ đủ"* mà kho đã tuyên là thua từ trong thiết kế — một WSL bash cài chỗ khác, hay
một `bash.exe` khác cũng làm hỏng argv, đều lọt.

Và phép đo #570 lượt 2 cho thấy **không lọc theo tên nào diễn tả nổi khuyết tật thật**.
Đo được trên Windows thật, cùng một lời gọi `bash -c <thân> t40 A B C`:

    C:\\Windows\\system32\\bash.EXE        -> $0=/bin/bash  $#=0   (đối số BIẾN MẤT)
    C:\\Program Files\\Git\\bin\\bash.exe     -> $0=t40        $#=3
    C:\\Program Files\\Git\\usr\\bin\\bash.exe -> $0=t40        $#=3

và với một script 6 dòng, WSL bash báo lỗi ở **dòng 7** với nội dung `t40` — tức đối số bị
nối vào THÂN SCRIPT rồi chạy như một lệnh. Từ đó `$1`/`$2`/`$3` rỗng, nên `exec "$3"` nhận
lệnh RỖNG và chết `exec: : not found`.

Nên ở đây ứng viên phải TỰ CHỨNG MINH bằng hai phép chạy thật (`_do_nang_luc`):

  (1) TRUNG THỰC ARGV — `-c <script> <nhãn> A1 A2 A3` phải cho `$0 == nhãn`, `$# == 3`,
      `$1 == A1`. WSL bash trượt đúng ở đây.
  (2) MỞ ĐƯỢC ĐƯỜNG DẪN BẢN ĐỊA — chạy được một script truyền bằng `str(Path)` y như bộ
      test truyền. WSL bash trượt ở đây với `rc=127 No such file or directory`.

Thiếu một trong hai ⇒ TỪ CHỐI. Không ứng viên nào đạt ⇒ trả `None` để người gọi
**fail-close** (`KHÔNG ĐO ĐƯỢC`), KHÔNG đoán bừa — `None ≠ False`.

Loại theo `%SystemRoot%` vẫn còn, nhưng chỉ để XẾP THỨ TỰ thử cho nhanh; thứ RA QUYẾT
ĐỊNH là hai phép chạy trên. Gỡ phép loại ấy đi thì kết quả không đổi, chỉ chậm hơn.

KHÔNG ép `cygpath`: đo được `C:\\Program Files\\Git\\usr\\bin\\bash.exe` KHÔNG có `cygpath`
mà thân `t40` vẫn `rc=0`. Đòi `cygpath` là đòi một thứ không liên quan tới khuyết tật.

Mã thoát của CLI:
    0 tìm được / cổng SẠCH      2 cổng ĐỎ      3 KHÔNG ĐO ĐƯỢC (không ứng viên nào đạt)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RC_OK, RC_DO, RC_KHONG_DO_DUOC = 0, 2, 3

# Nhãn `$0` dùng cho phép thử trung thực argv. Cố ý KHÔNG phải một đường dẫn: bash chỉ
# in lại thứ được truyền, nên một giá trị lạ mắt làm phép so không thể đúng do tình cờ.
_NHAN_ARGV = "bn-argv-probe"
_DOI_SO = ("bn-A1", "bn-A2", "bn-A3")
_DAU_CHAY = "BN_DA_CHAY_TU_TEP"

_SCRIPT_ARGV = 'printf "BN0=%s\\nBNSO=%s\\nBN1=%s\\n" "$0" "$#" "${1-}"'

_HAN_GIAY = 30


def _chay(argv, han=_HAN_GIAY):
    """(rc, đầu_ra). `rc` lấy TRỰC TIẾP từ tiến trình, không qua pipe."""
    try:
        p = subprocess.run(argv, timeout=han, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True, errors="replace")
        return p.returncode, (p.stdout or "")
    except subprocess.TimeoutExpired:
        return -998, f"quá hạn {han}s"
    except OSError as e:
        return -999, f"không spawn được: {type(e).__name__}: {e}"


def _do_nang_luc(argv_ung_vien, thu_muc_tam=None):
    """Ứng viên có LÀM ĐƯỢC VIỆC không — hai phép chạy thật. Trả (đạt, lý_do).

    `argv_ung_vien` là một DANH SÁCH chứ không phải một đường dẫn: bộ test cần bơm được
    một ứng viên giả `[python, gia.py]` trên mọi nền (Windows không tạo được `.exe` giả).
    Đường sản xuất luôn truyền `[<đường dẫn bash>]`.

    Hai phép, và PHẢI CÓ CẢ HAI — chúng bắt hai khuyết tật KHÁC nhau của cùng một bộ
    phóng WSL, không phép nào suy ra được phép kia:
      · nuốt argv mà vẫn mở được tệp  -> chỉ (1) bắt;
      · truyền argv đúng mà không mở nổi đường dẫn bản địa -> chỉ (2) bắt.
    """
    argv_ung_vien = list(argv_ung_vien)

    # (1) TRUNG THỰC ARGV.
    rc, ra = _chay(argv_ung_vien + ["-c", _SCRIPT_ARGV, _NHAN_ARGV, *_DOI_SO])
    if rc != 0:
        return False, f"phép argv: rc={rc} — {ra.strip()[:200]}"
    doc = dict(re.findall(r"^(BN0|BNSO|BN1)=(.*)$", ra, re.M))
    if doc.get("BN0") != _NHAN_ARGV:
        return False, (f"phép argv: `$0` là {doc.get('BN0')!r}, mong {_NHAN_ARGV!r} — "
                       f"đối số vị trí KHÔNG tới nơi (chữ ký của bộ phóng WSL)")
    if doc.get("BNSO") != str(len(_DOI_SO)):
        return False, (f"phép argv: `$#` là {doc.get('BNSO')!r}, mong {len(_DOI_SO)!r} — "
                       f"đối số vị trí bị nuốt")
    if doc.get("BN1") != _DOI_SO[0]:
        return False, f"phép argv: `$1` là {doc.get('BN1')!r}, mong {_DOI_SO[0]!r}"

    # (2) MỞ ĐƯỢC ĐƯỜNG DẪN BẢN ĐỊA — truyền `str(Path)` y như bộ test vẫn truyền.
    tam = tempfile.mkdtemp(prefix="bash-nen-", dir=thu_muc_tam)
    try:
        tep = Path(tam) / "do_mo_duong_dan.sh"
        tep.write_text(f'#!/usr/bin/env bash\nprintf "%s\\n" "{_DAU_CHAY}"\n',
                       encoding="utf-8", newline="\n")
        try:
            os.chmod(tep, 0o755)
        except OSError:
            pass
        rc, ra = _chay(argv_ung_vien + [str(tep)])
        if rc != 0 or _DAU_CHAY not in ra:
            return False, (f"phép mở đường dẫn bản địa: rc={rc} — không chạy được "
                           f"{str(tep)!r}: {ra.strip()[:200]}")
    finally:
        shutil.rmtree(tam, ignore_errors=True)
    return True, "đạt cả hai phép"


def _duoi_system_root(u, sr_norm):
    if not sr_norm:
        return False
    q = os.path.normcase(os.path.abspath(str(u)))
    return q == sr_norm or q.startswith(sr_norm + os.sep) or q.startswith(sr_norm + "/")


def ung_vien(path=None, system_root=None, program_files=None, git=None):
    """Danh sách đường dẫn ĐỂ THỬ, đã xếp thứ tự. Đây KHÔNG phải quyết định — quyết định
    là `_do_nang_luc`. Xếp thứ tự chỉ để phép thử đắt nhất ít phải chạy nhất."""
    env = os.environ
    ds, thay = [], set()

    def them(u):
        if not u:
            return
        try:
            k = os.path.normcase(os.path.abspath(str(u)))
        except OSError:
            k = str(u)
        if k in thay:
            return
        thay.add(k)
        ds.append(str(u))

    them(env.get("CONG_CU_BASH"))
    path = env.get("PATH", "") if path is None else path
    sr = env.get("SystemRoot", "") if system_root is None else system_root
    sr_norm = os.path.normcase(os.path.abspath(sr)).rstrip("\\/") if sr else None

    duoi_sr = []
    for d in path.split(os.pathsep):
        if not d:
            continue
        for ten in ("bash.exe", "bash"):
            u = Path(d) / ten
            try:
                if not u.is_file():
                    continue
            except OSError:
                continue
            if _duoi_system_root(u, sr_norm):
                duoi_sr.append(str(u))
            else:
                them(u)
    if os.name == "nt":
        g = shutil.which("git", path=path) if git is None else git
        if g:
            goc = Path(g).resolve()
            for cha in (goc.parent.parent, goc.parent.parent.parent):
                them(cha / "bin" / "bash.exe")
                them(cha / "usr" / "bin" / "bash.exe")
        pf = env.get("ProgramFiles", r"C:\Program Files") if program_files is None \
            else program_files
        them(Path(pf) / "Git" / "bin" / "bash.exe")
        them(Path(pf) / "Git" / "usr" / "bin" / "bash.exe")
    # Ứng viên dưới `%SystemRoot%` xếp CUỐI, không bị LOẠI: nếu nó thật sự làm được việc
    # thì không có lý do gì cấm. Thứ loại nó là `_do_nang_luc`, không phải cái tên.
    for u in duoi_sr:
        them(u)
    return [u for u in ds if Path(u).is_file()]


_CACHE = {}


def tim_bash(dung_cache=True, **ep):
    """Đường dẫn `bash` ĐÃ CHỨNG MINH làm được việc, hoặc None. Trả (đường, chẩn_đoán).

    None KHÔNG phải "không có bash" — nó là KHÔNG ĐO ĐƯỢC, và người gọi phải ĐỎ chứ
    không được bỏ qua ca. Chẩn đoán kèm theo để thông điệp lỗi nói được VÌ SAO.
    """
    khoa = json.dumps(sorted(ep.items()), default=str)
    if dung_cache and khoa in _CACHE:
        return _CACHE[khoa]
    chan_doan = []
    ket = None
    for u in ung_vien(**ep):
        dat, ly_do = _do_nang_luc([u])
        chan_doan.append({"duong": u, "dat": dat, "ly_do": ly_do})
        if dat and ket is None:
            ket = u
            break
    kq = (ket, chan_doan)
    if dung_cache:
        _CACHE[khoa] = kq
    return kq


# ───────────────────────────── CỔNG chặn bản sao ─────────────────────────────
# Lời gọi TRẦN: phân giải `bash` theo TÊN rồi coi hit đầu tiên là dùng được.
#
# ĐO CẤU TRÚC, KHÔNG ĐO CHUỖI. Bản đầu của cổng này khớp regex trên văn bản thô, và nó
# đếm luôn hai lần nhắc `shutil.which("bash")` trong CHÍNH docstring ở đầu tệp này. Tức
# một tệp chỉ NÓI VỀ khuyết tật cũng bị tính là mắc nó — đúng bệnh `t43` đã ĐỎ oan vì
# một câu văn xuôi có nhắc cụm marker, và `CLAUDE.md` chép lại: *"một cổng báo động giả
# là cổng sẽ bị tắt, rồi cả ca chết theo"*. `ast` không thấy chú thích và docstring, nên
# cả lớp báo động giả ấy chết theo KIẾN TRÚC chứ không theo một bản vá regex.
_TEN_WHICH = ("which",)
_TEN_SPAWN = ("run", "Popen", "call", "check_output", "check_call")


def _la_hang_bash(nut):
    import ast as _ast
    return isinstance(nut, _ast.Constant) and nut.value == "bash"


def _loi_goi_tran(than: str):
    """Số dòng của mọi lời gọi phân giải `bash` theo TÊN. Ném `SyntaxError` nếu không
    phân tích được — người gọi biến nó thành KHÔNG ĐO ĐƯỢC, KHÔNG bỏ qua tệp."""
    import ast
    cay = ast.parse(than)
    dong = set()
    for nut in ast.walk(cay):
        if not isinstance(nut, ast.Call) or not nut.args:
            continue
        ten = (nut.func.attr if isinstance(nut.func, ast.Attribute)
               else nut.func.id if isinstance(nut.func, ast.Name) else None)
        if ten in _TEN_WHICH and _la_hang_bash(nut.args[0]):
            dong.add(nut.lineno)
        elif ten in _TEN_SPAWN and isinstance(nut.args[0], (ast.List, ast.Tuple)) \
                and nut.args[0].elts and _la_hang_bash(nut.args[0].elts[0]):
            dong.add(nut.lineno)
    return sorted(dong)

# CHỈ tệp này được phép chứa lời gọi trần — nó LÀ bộ giải.
CHO_PHEP = ("ops/bash_nen.py",)

# RATCHET. Mỗi mục là một tệp CHƯA chuyển sang `tim_bash`, kèm lý do đo được. Cổng ĐỎ theo
# CẢ HAI chiều:
#   · tệp NGOÀI `CHO_PHEP ∪ CHUA_CHUYEN` mà có lời gọi trần  ⇒ ĐỎ (bản sao thứ tư);
#   · tệp TRONG `CHUA_CHUYEN` mà KHÔNG còn lời gọi trần nào ⇒ ĐỎ (danh sách đã mục).
# Chiều thứ hai là thứ bắt danh sách phải NGẮN đi. Thiếu nó thì ratchet thành nghĩa trang:
# ai vá xong cũng quên xoá tên mình, và cổng dần hết ý nghĩa mà vẫn xanh.
CHUA_CHUYEN = {
    "ops/lease_publish_test.py":
        "7 lời gọi: 1 trong `_bash_posix()` + 6 ở `t35`-`t40` (#570). Đang bị lease "
        "`wp541-path-r2-g2-antigravity` (#541) giữ tới 2026-09-20T15:54:00Z — chạm vào "
        "lúc này là tự mở cửa sổ hai writer.",
    "ops/cong_cu.py":
        "1 lời gọi trong `_bash_windows()`. Hợp nhất vào tệp này được, nhưng lease g2 của "
        "#541 khai `ops/cong_cu.py` trong `khong_duoc_cham`.",
    "ops/cong_cu_test.py":
        "3 lời gọi trong giàn của chính bộ test công cụ.",
}

# Ảnh chụp ĐÔNG CỨNG của các bản cũ, giữ để đối chiếu review — không phải mã đang sống.
_BO_QUA_THU_MUC = ("ops/reviews/",)


def quet(goc: Path):
    """Quét `ops/**`. Trả (rc, báo_cáo). Ba trạng thái, không phải hai."""
    goc = Path(goc)
    thu_muc = goc / "ops"
    if not thu_muc.is_dir():
        return RC_KHONG_DO_DUOC, {"trang_thai": "KHONG_DO_DUOC",
                                  "ly_do": f"không thấy {thu_muc}"}
    co_loi_goi = {}
    for tep in sorted(thu_muc.rglob("*.py")):
        rel = tep.relative_to(goc).as_posix()
        if any(rel.startswith(x) for x in _BO_QUA_THU_MUC):
            continue
        try:
            than = tep.read_text(encoding="utf-8")
            dong = _loi_goi_tran(than)
        except (OSError, UnicodeDecodeError, SyntaxError, ValueError) as e:
            # FAIL-CLOSE. Một tệp không phân tích được là một tệp KHÔNG ĐO ĐƯỢC, không
            # phải một tệp sạch — `None ≠ False`.
            return RC_KHONG_DO_DUOC, {"trang_thai": "KHONG_DO_DUOC",
                                      "ly_do": f"không đọc/phân tích được {rel}: {e}"}
        if dong:
            co_loi_goi[rel] = dong

    moi = {t: d for t, d in co_loi_goi.items()
           if t not in CHO_PHEP and t not in CHUA_CHUYEN}
    da_sach = [t for t in CHUA_CHUYEN if t not in co_loi_goi]
    bao = {"da_quet": str(thu_muc), "co_loi_goi_tran": co_loi_goi,
           "ngoai_danh_sach": moi, "muc_ratchet_da_sach": sorted(da_sach),
           "cho_phep": list(CHO_PHEP), "chua_chuyen": sorted(CHUA_CHUYEN)}
    if moi:
        bao["trang_thai"] = "DO"
        bao["ly_do"] = (
            "có lời gọi `bash` TRẦN ở tệp ngoài danh sách cho phép: "
            + "; ".join(f"{t}:{d}" for t, d in sorted(moi.items()))
            + ". Dùng `ops/bash_nen.py::tim_bash()` — nó QUYẾT BẰNG NĂNG LỰC, và "
              "`shutil.which(\"bash\")` trên Windows trả bộ phóng WSL (Issue #570).")
        return RC_DO, bao
    if da_sach:
        bao["trang_thai"] = "DO"
        bao["ly_do"] = (
            "mục ratchet đã SẠCH mà còn nằm trong `CHUA_CHUYEN`: "
            + ", ".join(sorted(da_sach))
            + ". Xoá khỏi danh sách — ratchet phải NGẮN đi, không được phình.")
        return RC_DO, bao
    bao["trang_thai"] = "DAT"
    return RC_OK, bao


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="lenh", required=True)
    q = sub.add_parser("tim", help="tìm `bash` làm được việc")
    q.add_argument("--json", action="store_true")
    r = sub.add_parser("quet", help="cổng: chặn lời gọi `bash` trần mới trong ops/**")
    r.add_argument("--root", default=".")
    r.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    if a.lenh == "tim":
        duong, chan_doan = tim_bash()
        out = {"duong": duong, "chan_doan": chan_doan,
               "trang_thai": "CO" if duong else "KHONG_DO_DUOC"}
        print(json.dumps(out, ensure_ascii=False, indent=2) if a.json
              else (duong or "KHONG_DO_DUOC"))
        return RC_OK if duong else RC_KHONG_DO_DUOC

    rc, bao = quet(Path(a.root))
    if a.json:
        print(json.dumps(bao, ensure_ascii=False, indent=2))
    else:
        print(f"{bao['trang_thai']}: {bao.get('ly_do', 'không có lời gọi trần mới')}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
