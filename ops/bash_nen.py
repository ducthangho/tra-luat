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
import ast
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


def _do_nang_luc(argv_ung_vien, thu_muc_tam=None, han=None):
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
    # `han` tham số hoá CHỈ để ca test chạy nhanh; mặc định là `_HAN_GIAY` của sản phẩm.
    # Mặt TREO là dạng hỏng THỨ BA của bộ phóng WSL, đo được ở `570-do-3`: nó làm
    # `./cai_cong_cu.sh` treo tới 60s thay vì trả `rc=127`. Hạn ở đây là thứ DUY NHẤT chặn
    # nó, nên nó phải có ca canh — trước r2 nó đúng do MAY, không do thiết kế.
    han = _HAN_GIAY if han is None else han

    # (1) TRUNG THỰC ARGV.
    rc, ra = _chay(argv_ung_vien + ["-c", _SCRIPT_ARGV, _NHAN_ARGV, *_DOI_SO], han=han)
    if rc != 0:
        # `rc == -998` là QUÁ HẠN, tức ứng viên TREO. Nó phải rơi vào nhánh TỪ CHỐI này,
        # không được coi là "không kết luận được rồi cho qua".
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
        rc, ra = _chay(argv_ung_vien + [str(tep)], han=han)
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


def tim_bash(dung_cache=True, tat_ca=False, **ep):
    """Đường dẫn `bash` ĐÃ CHỨNG MINH làm được việc, hoặc None. Trả (đường, chẩn_đoán).

    None KHÔNG phải "không có bash" — nó là KHÔNG ĐO ĐƯỢC, và người gọi phải ĐỎ chứ
    không được bỏ qua ca. Chẩn đoán kèm theo để thông điệp lỗi nói được VÌ SAO.

    `tat_ca=True` thử MỌI ứng viên thay vì dừng ở cái đầu tiên đạt. Đường sản xuất KHÔNG
    dùng nó (thử thừa là trả tiền vô ích), nhưng CHẨN ĐOÁN thì cần: r1 của spec đòi log
    Windows cho thấy `C:\\Windows\\system32\\bash.EXE` đã được THỬ rồi bị TỪ CHỐI, mà
    với đường dừng-sớm thì Git Bash đạt trước nên System32 chưa từng được chạm — tức tiêu
    chí ấy đòi một thứ CLI không sinh ra được. Đây là chỗ sinh ra nó.
    """
    # KHOA CACHE PHAI GOM MOI TRUONG (#570 r4, N19). `ung_vien()` doc `CONG_CU_BASH`,
    # `PATH`, `SystemRoot`, `ProgramFiles` tu `os.environ` khi tham so la None — nen mot
    # khoa chi gom `ep` se tra ket qua KHONG khop moi truong hien tai, IM LANG.
    # ĐO ĐƯỢC (cross-review 05ec2eb5, executor do lai): goi `tim_bash()`; dat `CONG_CU_BASH`
    # sang mot bash THAT o duong khac; goi lai => van tra duong CU. Khoa cu: `[[], false]`.
    # Nut ghi de ma module TU KHAI la co, bi chinh cache nuot.
    # r7: khoa CON THIEU HAI dau vao NGAM, va ca hai da duoc DO (cross-review codex tren
    # 55f9bce). (1) THU MUC LAM VIEC — mot muc TUONG DOI trong `CONG_CU_BASH`/`PATH` giai
    # theo cwd, nen doi cwd la doi ung vien; do duoc tren Linux: dat `CONG_CU_BASH=bash`,
    # `PATH=.`, goi o `a/` roi goi o `b/` => tra CUNG mot ket qua, tuc cache nuot.
    # (2) `PATHEXT` — `ung_vien()` goi `shutil.which("git", path=path)`, ma tren Windows
    # `which` doc `PATHEXT` de biet duoi nao la thuc thi duoc.
    # KHAI THANG: ve (2) chua do duoc tren nen nay (Linux bo qua `PATHEXT`); no vao khoa vi
    # LY LE doc duoc tu ma, khong phai vi mot phep do. `None != False`.
    _ENV_ANH_HUONG = ("CONG_CU_BASH", "PATH", "PATHEXT", "SystemRoot", "ProgramFiles")
    moi_truong = {k: os.environ.get(k) for k in _ENV_ANH_HUONG}
    khoa = json.dumps([sorted(ep.items()), bool(tat_ca), sorted(moi_truong.items()),
                       os.getcwd()], default=str)
    if dung_cache and khoa in _CACHE:
        return _CACHE[khoa]
    chan_doan = []
    ket = None
    for u in ung_vien(**ep):
        dat, ly_do = _do_nang_luc([u])
        chan_doan.append({"duong": u, "dat": dat, "ly_do": ly_do})
        if dat and ket is None:
            ket = u
            if not tat_ca:
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
# CACH VIET Windows cua dung khuyet tat Windows. Bo sot no la bo sot dung cho can chan —
# va `ung_vien()` ngay trong tep nay cung dung `("bash.exe", "bash")`.
_HANG_BASH = ("bash", "bash.exe")
# Doi so co the den bang TEN thay vi VI TRI. `shutil.which(cmd="bash")` va
# `subprocess.run(args=["bash", ...])` deu hop le va deu lot qua ban chi doc `args[0]`.
_KHOA_WHICH = ("cmd",)
_KHOA_SPAWN = ("args",)


# BIEN MOI TRUONG CHON KHO / CHON INDEX / TIEM CAU HINH. Danh sach nay KHONG BAO GIO DU —
# do la ly do no di KEM `_doc_noi_dung` doc tu BLOB: gap nhau o cho ca hai deu phai sai thi
# phan quyet moi sai. Khai thang: mot bien git moi ma phien nay chua biet se KHONG bi go.
_BIEN_GIT_CHON_KHO = (
    "GIT_DIR", "GIT_INDEX_FILE", "GIT_WORK_TREE", "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_CEILING_DIRECTORIES", "GIT_DISCOVERY_ACROSS_FILESYSTEM",
    "GIT_NAMESPACE", "GIT_INDEX_VERSION",
    "GIT_CONFIG", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_CONFIG_NOSYSTEM",
    "GIT_CONFIG_COUNT",
)


def _moi_truong_git_sach():
    """(môi trường cho tiến trình git con, tên các biến đã GỠ).

    SINH TỪ r11 (N28), cross-review codex vòng 5. `git -C <goc>` KHÔNG ghim được kho: nếu
    `GIT_INDEX_FILE` có mặt thì `-C` vẫn đúng thư mục mà INDEX lại là tệp khác. Đo được trên
    `6131cbd`: cùng một kho, index THẬT trả `['bad.py']`, đặt `GIT_INDEX_FILE` trỏ index khác
    trả `[]` — và **cả hai lần đều khai `nguon_tep=git`**. Một cổng nói "tôi đọc INDEX" trong
    khi đọc index của người khác là cổng tệ hơn không có cổng.
    `GIT_CONFIG_COUNT`/`KEY_n`/`VALUE_n` cũng bị gỡ: chúng tiêm cấu hình tuỳ ý vào lượt chạy.
    ĐO ĐƯỢC, không phải lý lẽ: môi trường của chính phiên soạn bản vá này ĐANG mang
    `GIT_CONFIG_COUNT=3` cùng ba cặp KEY/VALUE.
    """
    moi = dict(os.environ)
    da_go = sorted(k for k in moi
                   if k in _BIEN_GIT_CHON_KHO
                   or k.startswith("GIT_CONFIG_KEY_") or k.startswith("GIT_CONFIG_VALUE_"))
    for k in da_go:
        moi.pop(k, None)
    return moi, da_go


def _doc_noi_dung(goc: Path, muc, nguon_tep):
    """({đường: thân}, [mục là SYMLINK]). NỘI DUNG LẤY TỪ ĐÂU là một phần của phán quyết.

    N28 — SINH TỪ r11, cross-review codex vòng 5. r9/r10 lấy DANH SÁCH từ INDEX rồi đọc NỘI
    DUNG bằng `read_text()` trên cây làm việc. Hai nguồn khác nhau, và khe giữa chúng đo được:
    một mục `*.py` trong INDEX là SYMLINK thì `read_text()` đi theo ra NGOÀI kho. Đo trên
    `6131cbd`: sửa tệp đích **bên ngoài kho** làm phán quyết đổi `['ops/lien_ket.py']` → `[]`
    trong khi INDEX **không đổi một byte** — và `nguon_tep` vẫn khai `git`.
    Đó là mặt thứ SÁU của lớp *phán quyết phụ thuộc trạng thái LOCAL của máy*. r9 giết được
    "tệp NÀO", nhưng lớp còn phủ "BYTE nào" và "INDEX nào" (xem `_moi_truong_git_sach`).
    Chủ kho quyết ở r11: **nội dung cũng lấy từ INDEX** — `git cat-file --batch` trên chính
    các blob đã stage.

    GIÁ, khai thẳng: tệp đã `git add` rồi sửa tiếp trên đĩa sẽ được quét ở DẠNG ĐÃ STAGE. Cổng
    thôi phản ánh đĩa. Trong CI không khác gì (checkout sạch). Tại chỗ, nó có nghĩa "cổng xử
    thứ anh đã stage" — đúng mạch với N23 ("danh sách là INDEX").
    SYMLINK ⇒ **fail-close có tên**, không im lặng bỏ qua: blob của một mục mode `120000` là
    CHUỖI ĐƯỜNG DẪN chứ không phải mã, nên đọc nó như Python là vô nghĩa. Đo trên kho hôm nay:
    `git ls-files -s -- '*.py'` có **0** mục mode `120000` trên **264** mục, nên luật này KHÔNG
    tốn gì ở hiện tại — nó là hàng rào cho ngày mai.
    TỐC ĐỘ, đo chứ không đoán: `cat-file --batch` đọc trọn 264 blob trong **0,098 s**.
    """
    if nguon_tep != "git":
        ra = {}
        for rel, _, _ in muc:
            ra[rel] = (goc / rel).read_text(encoding="utf-8")
        return ra, []
    lien_ket = sorted(rel for rel, che_do, _ in muc if che_do == "120000")
    if lien_ket:
        return None, lien_ket
    if not muc:
        return {}, []
    env, _ = _moi_truong_git_sach()
    yeu_cau = "".join(sha + "\n" for _, _, sha in muc).encode("ascii")
    pc = subprocess.run(["git", "-C", str(goc), "cat-file", "--batch"],
                        input=yeu_cau, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        timeout=180, env=env)
    if pc.returncode != 0:
        raise OSError(f"cat-file --batch rc={pc.returncode}: {pc.stderr[:200]!r}")
    ra, dem, i = {}, 0, 0
    kq = pc.stdout
    for rel, _, sha in muc:
        nl = kq.index(b"\n", i)
        dau = kq[i:nl].split()
        if len(dau) != 3 or dau[0].decode() != sha:
            raise OSError(f"cat-file trả không khớp ở {rel}: {kq[i:nl][:120]!r}")
        co = int(dau[2])
        than = kq[nl + 1:nl + 1 + co]
        i = nl + 1 + co + 1          # bỏ qua `\n` kết thúc mỗi bản ghi
        ra[rel] = than.decode("utf-8")
        dem += 1
    return ra, []


def _liet_ke_py(goc: Path):
    """(danh sách `*.py` cần quét, nguồn đã dùng). BA nguồn, và nó KHAI ra dùng nguồn nào.

    VÌ SAO KHÔNG CÒN `rglob` TRẦN — một phép đo, không phải khẩu vị. Từ r4 cổng quét TOÀN
    CÂY, nên `rglob("*.py")` chạm cả thứ `.gitignore` đã loại: `node_modules/`, `dist/`,
    `reports/`, `references/golden/fixtures/`, các cache. Cross-review codex trên `55f9bce`
    khai, và executor ĐO LẠI thấy đúng, trên cây giả:
        thêm `node_modules/x.py`    ⇒ rc=2 DO           (báo động giả)
        thêm `node_modules/hong.py` ⇒ rc=3 KHONG_DO_DUOC (fail-close CẢ KHO vì một tệp rác)
    Tức phán quyết của cổng phụ thuộc MÁY AI CHẠY chứ không phụ thuộc cây ứng viên. Một cổng
    đọc khác nhau trên hai máy là cổng sẽ bị tắt.

    DANH SÁCH = INDEX (`git ls-files --cached`), KHÔNG HƠN — quyết định KIẾN TRÚC của chủ kho
    ở r8, sau khi cùng một LỚP khuyết tật (*phán quyết phụ thuộc trạng thái LOCAL của máy*) lộ
    ra BỐN mặt qua ba bản vá nối tiếp, mỗi bản đúng và có răng ở chỗ nó phủ:
        vòng 1  `--others --exclude-standard`          nghe `core.excludesFile` của người chạy;
        vòng 2  `--exclude-per-directory=.gitignore`   "trong cây" = BẢN LÀM VIỆC — một dòng
                                                       `.gitignore` chưa commit giấu được một
                                                       bản sao thứ tư (đo: True → False);
        r8 nháp luật ignore từ BLOB ĐÃ THEO DÕI qua kho tạm cách ly — đóng ba mặt, rồi mặt
                thứ tư đo được: cây có `.git` giả lồng trong kho khác thì kho CHA trả lời.
    Gốc của cả lớp là việc cổng tự trả lời "tệp CHƯA theo dõi nào bị ignore" — câu ấy luôn có
    một tầng máy nữa. Chỉ đọc INDEX thì không còn luật ignore nào để nghe: lớp chết theo kiến
    trúc, không theo bản vá. GIÁ, khai thẳng: tệp chưa `git add` KHÔNG được quét. Trong CI cây
    luôn đã commit nên độ phủ không giảm; tại chỗ, ai quên `add` sẽ thấy ở PR. `t37` trói đúng
    đánh đổi ấy (đã add ⇒ quét, chưa add ⇒ không); `t43` trói "không luật ignore nào — của kho
    hay của máy — đổi được danh sách".

    BA TRẠNG THÁI, khai thẳng trong báo cáo ở khoá `nguon_tep`:
      `git`      — danh sách từ INDEX của kho;
      `rglob`    — cây KHÔNG phải kho git (bộ ca dựng cây giả), quét thẳng;
      `git-hong: …` — có `.git` mà lệnh git hỏng (rc khác 0, hết giờ, không sinh được tiến
                    trình). KHÔNG lùi, KHÔNG trả danh sách: `quet()` biến trạng thái này
                    thành `KHONG_DO_DUOC`.

    VÌ SAO KHÔNG LÙI VỀ `rglob` KHI GIT HỎNG (N26, #570 r10). Bản r9 lùi và ĐẶT TÊN cho việc
    lùi (`rglob-git-hong`), với lý lẽ "người đọc phải thấy". Cross-review codex vòng 4 khai,
    và executor ĐO LẠI thấy đúng, trên cây có `.git` GIẢ:
        `_liet_ke_py` trả `rac_bi_ignore.py` kèm `rglob-git-hong`; `quet` ra `rc=2 DO`.
    Tức ĐÚNG cái lớp mà r9 giết bằng kiến trúc — *phán quyết phụ thuộc trạng thái LOCAL của
    máy* — sống lại qua CỬA SAU: git của người chạy hỏng thì tệp chưa theo dõi lại quyết
    phán quyết. Một TRƯỜNG cho người đọc không phải một CỔNG; đó đúng là thứ `CLAUDE.md` gọi
    là "lời dặn bằng miệng không phải hàng rào", lần này nằm trong chính mã của packet.
    Không lấy được INDEX thì KHÔNG CÓ danh sách, nên KHÔNG CÓ phán quyết — fail-close, cùng
    luật với tệp không phân tích được ở `quet()`. `None ≠ False`.
    Một tệp có trong INDEX mà không đọc được trên đĩa (đã xoá, sparse checkout) làm cổng
    KHÔNG_ĐO_ĐƯỢC ở `quet` — cây không khớp index thì không có gì để đo.
    """
    if (goc / ".git").exists():
        env, _ = _moi_truong_git_sach()
        try:
            pc = subprocess.run(
                ["git", "-C", str(goc), "ls-files", "--cached", "-s", "-z", "--", "*.py"],
                capture_output=True, text=True, timeout=60, env=env)
            if pc.returncode == 0:
                muc = []
                for dong in pc.stdout.split("\0"):
                    if not dong:
                        continue
                    dau, _, rel = dong.partition("\t")
                    truong = dau.split()
                    if len(truong) < 2 or not rel:
                        return [], f"git-hong: ls-files -s trả dòng lạ {dong[:120]!r}"
                    muc.append((rel, truong[0], truong[1]))
                return sorted(set(muc)), "git"
            return [], f"git-hong: ls-files rc={pc.returncode} {pc.stderr.strip()[:200]!r}"
        except (OSError, subprocess.SubprocessError) as e:
            return [], f"git-hong: {type(e).__name__}: {e}"
    return [(x.relative_to(goc).as_posix(), None, None)
            for x in sorted(goc.rglob("*.py"))], "rglob"


def _so_cho_phep(muc):
    """(so_lan_duoc_phep, ly_do) cua mot mục miễn trừ.

    `(số, lý_do)` là hình dạng DUY NHẤT hợp lệ. Một CHUỖI trần trả `(None, chuỗi)` để báo cáo
    in được, nhưng `quet()` coi mục ấy là KHÔNG ĐO ĐƯỢC chứ không tha — r7 từng cho chuỗi
    giữ "luật cũ, chỉ bắt lúc về 0", và đó là một VÉ VÔ HẠN đúng nghĩa: đo được ở r8, mục
    chuỗi với 9 lời gọi ⇒ `rc=0 DAT`. Cùng lớp với F1 (hạn ngạch 0 bị bỏ qua): miễn trừ khai
    theo TƯ CÁCH THÀNH VIÊN thay vì theo HẠN NGẠCH. `t40` đọc bảng THẬT để chặn ngay lúc khai.
    """
    if isinstance(muc, (tuple, list)) and len(muc) == 2:
        return int(muc[0]), str(muc[1])
    return None, str(muc)


def _la_hang_bash(nut):
    """Hang so nay co phai mot TEN `bash` khong — so KHONG phan biet hoa/thuong.

    `casefold()` chu khong phai `lower()`, va khong phai so thang: tren Windows ten tep thuc
    thi KHONG phan biet hoa/thuong, nen `shutil.which("BASH.EXE")` va
    `subprocess.run(["Bash.exe"])` phong ra DUNG mot tep nhu `bash.exe`.
    DO DUOC (cross-review codex tren 55f9bce, executor do lai): ban truoc tra `[]` cho ca hai
    cach viet ay trong khi tra `[2]` cho `bash` va `bash.exe`. Tuc cong vua mo ra toan cay bi
    di vong bang MOT PHIM SHIFT — tren dung cai nen ma packet nay sinh ra de phuc vu.
    `_HANG_BASH` da toan chu thuong nen chi can casefold ve MOT phia.
    """
    import ast as _ast
    if not isinstance(nut, _ast.Constant):
        return False
    v = nut.value
    if isinstance(v, str):
        return v.casefold() in _HANG_BASH
    if isinstance(v, bytes):
        # N30 (r11) — `shutil.which(b"bash")` và `subprocess.run([b"bash"])` CHẠY bash thật;
        # bản r10 loại chúng chỉ vì không phải `str`, tức một đường vòng không cần phân tích
        # luồng dữ liệu nào. Đo được trước vá: cả năm hình dạng byte đều ra `[]`.
        # CHỈ ASCII: không giải mã bừa byte ngoài ASCII — một tên chương trình thật thì ASCII.
        try:
            return v.decode("ascii").casefold() in _HANG_BASH
        except UnicodeDecodeError:
            return False
    return False


def _doi_so_dau(nut, khoa):
    """Doi so DAU TIEN cua mot lenh goi, du no den bang VI TRI hay bang TEN."""
    if nut.args:
        return nut.args[0]
    for kw in nut.keywords:
        if kw.arg in khoa:
            return kw.value
    return None


def _doi_so_executable(nut):
    """Nút `executable` của một lời gọi spawn, hay None khi vắng (kể cả `executable=None`
    tường minh). Đến bằng TÊN (`executable=`) hoặc bằng VỊ TRÍ — `Popen(args, bufsize,
    executable, …)` xếp nó ở chỗ thứ ba, và `run`/`call`/`check_*` chuyển `*popenargs`
    nguyên xi. Có `*` trải trước chỗ ấy thì không đoán."""
    import ast
    exe = None
    for kw in nut.keywords:
        if kw.arg == "executable":
            exe = kw.value
    if exe is None and len(nut.args) > 2 \
            and not any(isinstance(a, ast.Starred) for a in nut.args[:3]):
        exe = nut.args[2]
    if isinstance(exe, ast.Constant) and exe.value is None:
        return None
    return exe


def _ten_chuong_trinh(dau):
    """Nút mang TÊN CHƯƠNG TRÌNH trong `args` của một lời gọi spawn: phần tử đầu của
    list/tuple, hoặc CHÍNH CHUỖI khi `args` là một chuỗi trần — `run("bash")` phóng `bash`
    theo TÊN y như `run(["bash"])` (POSIX `execvp`, Windows `CreateProcess` tìm PATH), có hay
    không có `shell=True`. Đo được ở r8: bản trước trả `[]` cho `run("bash")` — lọt, cùng lớp
    F3/F4 "độ phủ theo hình dạng sai cả hai hướng"."""
    import ast
    if isinstance(dau, (ast.List, ast.Tuple)):
        return dau.elts[0] if dau.elts else None
    return dau


def _mang_hang_bash(nut):
    """Lời gọi có hằng `bash` ở ĐỐI SỐ NÀO ĐÓ không — bộ lọc RẺ, cố ý RỘNG hơn luật thật (mọi vị
    trí, mọi từ khoá); quyết định đúng nằm ở `_loi_goi_tran`. Sai chiều rộng thì chỉ tốn công
    giải callee thừa; sai chiều hẹp mới là lọt — nên nó không được hẹp hơn tập luật thật xét."""
    for a in (*nut.args, *(kw.value for kw in nut.keywords)):
        if _la_hang_bash(a) or (isinstance(a, (ast.List, ast.Tuple)) and a.elts
                                and _la_hang_bash(a.elts[0])):
            return True
    return False


def _loi_goi_tran(than: str):
    """Số dòng các lời gọi phân giải `bash` theo TÊN mà hàm này PHỦ. Ném `SyntaxError`
    nếu không phân tích được — người gọi biến nó thành KHÔNG ĐO ĐƯỢC, KHÔNG bỏ qua tệp.

    PHẠM VI, KHAI CHO ĐÚNG — bản trước viết *"mọi lời gọi"* và đó là một **lời khai rộng
    hơn phép đo**, đúng lớp lỗi kho đã đặt tên. Cross-review trên `05ec2eb5` cho ăn 12 hình
    dạng và đo được **BẮT 3 / LỌT 9**; phiên executor đo lại và ra **y hệt**.

    PHỦ (mỗi hình dạng có một khẳng định riêng trong `t33`):
      · `which("bash")` · `which("bash.exe")` · `which(cmd="bash")`, không phân biệt hoa/thường;
      · `run`/`Popen`/`call`/`check_output`/`check_call` mà TÊN CHƯƠNG TRÌNH là hằng `bash`:
        phần tử đầu của list/tuple (đến bằng VỊ TRÍ hay `args=`), hoặc `args` là CHUỖI TRẦN
        `"bash"` (r8);
      · `executable=` (hoặc đối số vị trí thứ ba) là hằng `bash`. Nó GHI ĐÈ chương trình
        thật sự chạy, nên khi có mặt thì CHỈ NÓ quyết: `run(["bash"], executable="/bin/echo")`
        chạy `echo` và KHÔNG bị bắt; `run(["bash"], executable="bash")` là ĐÚNG MỘT bản ghi.
        (r8, F4 codex vòng 3 — bản trước CỘNG THÊM thay vì ghi đè, đo được `[(2, 0)]` cho
        trường hợp `echo`.)
      · callee giải theo PHẠM VI TỪ VỰNG (r8, F3 codex vòng 3): `import subprocess` ở module
        rồi gọi trong hàm ⇒ bắt; `import` nằm trong hàm A thì hàm B KHÔNG thấy; tên bị THAM
        SỐ hay PHÉP GÁN che ở phạm vi gần nhất ⇒ không còn là stdlib ⇒ không bắt. Bản trước
        `ast.walk` mọi `import` của tệp vào MỘT bảng, đo được: `def a(): import subprocess`
        + `def b(subprocess): subprocess.run(["bash"])` ⇒ `[(5, 4)]`, phải là `[]`.

    **KHÔNG PHỦ**, và khai thẳng ra đây thay vì để người đọc tưởng đã kín:
      · chuỗi lệnh NHIỀU TỪ (`run("bash -c ...", shell=True)`) — chỉ chuỗi trần đúng một
        tên `bash` được phủ;
      · `os.system` / `os.execvp` / `os.spawn*` / `asyncio.create_subprocess_exec`;
      · tên `bash` đi qua BIẾN TRUNG GIAN, nối chuỗi, danh sách dựng nơi khác, hay một
        `executable=` KHÔNG phải hằng;
      · `from shutil import *`, tên đến qua `globals()`/`getattr`.
    Các nhóm ấy cần phân tích luồng dữ liệu, không phải khớp cây cú pháp. Chúng là **nợ có
    tên**, không phải chỗ đã kín. Ai mở rộng thì thêm hình dạng vào `t33` TRƯỚC.
    Phạm vi giải THEO TÊN, không theo DÒNG CHẢY (đúng luật tên cục bộ của Python): `import
    shutil` rồi `shutil = x` trong CÙNG một phạm vi làm tên ấy mơ hồ và KHÔNG bị bắt, dù thứ
    tự hai câu ra sao.
    """
    cay = ast.parse(than)
    # LỌC TRƯỚC THEO HẰNG, GIẢI CALLEE SAU. Bộ giải phạm vi dựng bảng ràng buộc cho MỌI phạm
    # vi của tệp, và đo được trên kho thật nó chiếm 8,5/10,4s của `quet` (12.912 phạm vi) trong
    # khi chỉ 6 tệp có hằng `bash`. Một lời gọi không mang hằng `bash` ở đối số nào thì không
    # cần biết callee là ai — nên chỉ tệp CÓ ứng viên mới trả tiền cho bộ giải.
    ung_vien = [n for n in ast.walk(cay) if isinstance(n, ast.Call) and _mang_hang_bash(n)]
    if not ung_vien:
        return []
    tra_theo_nut = {id(n): tra for n, tra in _giai_callee_theo_pham_vi(cay)}
    ban_ghi = []
    for nut in ung_vien:
        tra_ten = tra_theo_nut[id(nut)]
        loai = _loai_loi_goi(nut, tra_ten)
        if loai is None:
            continue
        if loai == "which":
            dau = _doi_so_dau(nut, _KHOA_WHICH)
            dinh = dau is not None and _la_hang_bash(dau)
        else:
            exe = _doi_so_executable(nut)
            if exe is None:
                dinh = _la_hang_bash(_ten_chuong_trinh(_doi_so_dau(nut, _KHOA_SPAWN)))
            else:
                # `executable=` GHI ĐÈ, không cộng thêm: `args[0]` khi ấy chỉ còn là
                # `argv[0]` trang trí. Một lời gọi là MỘT bản ghi dù cả hai cùng tên `bash`.
                dinh = _la_hang_bash(exe)
        if dinh:
            ban_ghi.append((nut.lineno, nut.col_offset))
    # MỘT BẢN GHI CHO MỖI `ast.Call`, không phải cho mỗi DÒNG. Tập dòng cũ gộp hai lời gọi
    # trên cùng một dòng thành một — đo được: `(which("bash"), which("bash"))` ra `[2]`.
    return sorted(set(ban_ghi))


# Nhận diện theo TÊN mà không giải được CALLEE thì sai CẢ HAI HƯỚNG — đo được cả hai:
#   lọt:     `subprocess.run(["x"], executable="bash")`  ⇒ `[]`
#   bắt oan: `runner.run(["bash"])`, `matcher.which("bash")` ⇒ `[2]`
# Nên phải biết cái tên ấy có THẬT SỰ trỏ vào `subprocess`/`shutil` hay không.
_MODULE_CHU = {"subprocess": _TEN_SPAWN, "shutil": _TEN_WHICH}


# Các nút MỞ PHẠM VI TỪ VỰNG mới (luật Python 3): hàm, lambda, lớp, và bốn loại comprehension.
_NUT_PHAM_VI = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef,
                ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


def _dich_walrus(nut):
    """Tên bị `:=` ràng buộc bên trong `nut` (một comprehension) — PEP 572 nói chúng thuộc
    phạm vi CHỨA comprehension. KHÔNG xuống hàm/lambda/lớp lồng bên trong: `:=` ở đó ràng buộc
    trong chính phạm vi ấy, không trồi ra."""
    import ast
    ra = []
    chong = list(ast.iter_child_nodes(nut))
    while chong:
        n = chong.pop()
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
            continue
        if isinstance(n, ast.NamedExpr) and isinstance(n.target, ast.Name):
            ra.append(n.target.id)
        chong.extend(ast.iter_child_nodes(n))
    return ra


def _rang_buoc_cua(pham_vi):
    """Bảng tên → tập ràng buộc TRỰC TIẾP trong MỘT phạm vi, KHÔNG xuống phạm vi con.

    Mỗi ràng buộc là `("import", module, hàm|None)` khi là `import`/`from … import` của một
    module trong `_MODULE_CHU`, hoặc `("khac",)` cho MỌI ràng buộc còn lại: tham số, phép gán
    (kể cả đích của `for`/`with … as`/`except … as`/`:=`/`match … as`), `def`/`class` lồng,
    `del`, và cả `import` của module KHÔNG theo dõi (`from toi import run` trỏ vào thứ khác,
    không phải `subprocess.run`). Trả thêm hai tập: tên khai `global`, tên khai `nonlocal`.

    VÌ SAO KHÔNG XUỐNG PHẠM VI CON — đó chính là F3: bản trước `ast.walk` cả cây, nên một
    `import` trong hàm A "có hiệu lực" ở hàm B, và một tham số tên `subprocess` ở B không che
    được gì. Python giải tên theo PHẠM VI TỪ VỰNG; bộ giải cũng phải thế, không hơn.

    MỘT RÀNG BUỘC ĐƯỢC PHÂN LOẠI THEO CÁC TRƯỜNG CỦA NÚT, KHÔNG THEO MỖI CÁI TÊN (N27, r10).
    Cross-review codex vòng 4 chỉ MỘT mặt; quét theo LỚP ra BA, hai chiều ngược nhau:
      · `ImportFrom.level >= 1` — `from .subprocess import run` là module CÙNG GÓI. Bỏ qua
        `level` ⇒ BÁO OAN một API nội bộ. Đo được: `[(2, 0)]`. (codex chỉ)
      · `Import` tên CÓ CHẤM, không `as` — `import subprocess.x` ràng buộc tên `subprocess`
        vào CHÍNH module stdlib ấy. Coi là `("khac",)` ⇒ BỎ SÓT. Đo được: `[]`. (codex KHÔNG
        chỉ — tìm ra bằng phép quét theo lớp.)
      · `from subprocess import *` — vẫn KHÔNG PHỦ, và đó là **nợ có tên**, không phải một
        mặt mới: `*` đòi biết module xuất ra những gì, tức phải NẠP nó, chứ không phải đọc
        cây cú pháp. Cùng hàng với `shell=True` và biến trung gian.
    `import subprocess.x as y` KHÔNG ràng buộc `subprocess` (chỉ `y` ← module con) nên vẫn là
    `("khac",)` — kiểm cả ở `t33`, để chiều "bắt oan" có răng.
    """
    import ast
    bang, toan_cuc, phi_cuc_bo = {}, set(), set()

    def them(ten, rb):
        if ten:
            bang.setdefault(ten, set()).add(rb)

    if isinstance(pham_vi, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        a = pham_vi.args
        for x in (*a.posonlyargs, *a.args, *a.kwonlyargs, a.vararg, a.kwarg):
            if x is not None:
                them(x.arg, ("khac",))
    chong = list(ast.iter_child_nodes(pham_vi))
    while chong:
        n = chong.pop()
        if isinstance(n, _NUT_PHAM_VI):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                them(n.name, ("khac",))
            elif isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                # N29 (r11) — PEP 572: `:=` bên trong một comprehension ràng buộc ở phạm vi
                # CHỨA comprehension, không ở trong nó. Bản r10 `continue` thẳng nên ràng buộc
                # ấy biến mất; đo được: `import subprocess` rồi
                # `[(subprocess := runner) for _ in [0]]` thì lời gọi SAU đó vẫn bị báo `[(3,0)]`
                # — cổng CHẶN một phép che hợp lệ.
                for x in _dich_walrus(n):
                    them(x, ("khac",))
            continue                                   # KHÔNG xuống phạm vi con
        if isinstance(n, ast.Import):
            for al in n.names:
                dau = al.name.split(".")[0]
                if al.name in _MODULE_CHU:
                    them(al.asname or al.name, ("import", al.name, None))
                elif al.asname is None and dau in _MODULE_CHU:
                    # `import subprocess.x` RÀNG BUỘC tên `subprocess` vào CHÍNH module ấy —
                    # luật Python, không phải suy diễn. Bản r9 gán `("khac",)` nên
                    # `import subprocess.x` + `subprocess.run(["bash"])` LỌT (đo được: `[]`).
                    them(dau, ("import", dau, None))
                else:
                    them(al.asname or dau, ("khac",))
        elif isinstance(n, ast.ImportFrom):
            for al in n.names:
                if al.name == "*":
                    continue                           # KHÔNG PHỦ — khai trong docstring
                # `level` LÀ MỘT PHẦN CỦA Ý NGHĨA, không phải siêu dữ liệu (N27, r10).
                # `from .subprocess import run` trỏ vào module CÙNG GÓI, không phải stdlib;
                # bản r9 bỏ qua `level` nên nó BÁO OAN một API nội bộ (đo được: `[(2, 0)]`).
                # `from . import subprocess` đã đúng sẵn: `n.module is None`.
                if n.level == 0 and n.module in _MODULE_CHU:
                    them(al.asname or al.name, ("import", n.module, al.name))
                else:
                    them(al.asname or al.name, ("khac",))
        elif isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            them(n.id, ("khac",))
        elif isinstance(n, ast.ExceptHandler):
            them(n.name, ("khac",))
        elif isinstance(n, ast.Global):
            toan_cuc.update(n.names)
        elif isinstance(n, ast.Nonlocal):
            phi_cuc_bo.update(n.names)
        elif type(n).__name__ in ("MatchAs", "MatchStar"):
            them(getattr(n, "name", None), ("khac",))
        elif type(n).__name__ == "MatchMapping":
            them(getattr(n, "rest", None), ("khac",))
        chong.extend(ast.iter_child_nodes(n))
    return bang, toan_cuc, phi_cuc_bo


def _tra_import(cac_rang_buoc):
    """(module, hàm|None) khi tên bị ràng buộc ĐÚNG MỘT LẦN và là `import` theo dõi; None khi
    bị che, mơ hồ, hay trỏ vào thứ khác."""
    if len(cac_rang_buoc) == 1:
        (rb,) = cac_rang_buoc
        if rb[0] == "import":
            return rb[1], rb[2]
    return None


def _giai_ten(ten, chuoi):
    """Giải `ten` theo chuỗi phạm vi `chuoi` (ngoài → trong), luật Python: phạm vi gần nhất
    có ràng buộc thắng; thân LỚP không nhìn thấy được từ hàm lồng trong nó; `global` nhảy về
    module; `nonlocal` bỏ qua phạm vi hiện tại."""
    n = len(chuoi)
    for i in range(n - 1, -1, -1):
        la_lop, bang, toan_cuc, phi_cuc_bo = chuoi[i]
        if la_lop and i != n - 1:
            continue
        if ten in toan_cuc:
            return _tra_import(chuoi[0][1].get(ten, ()))
        if ten in phi_cuc_bo:
            continue
        if ten in bang:
            return _tra_import(bang[ten])
    return None


def _bang_pham_vi_ca_cay(cay):
    """{id(nút phạm vi): (bảng, toàn_cục, phi_cục_bộ)} cho CẢ cây, SAU khi các ràng buộc khai
    `global`/`nonlocal` đã được CHUYỂN về phạm vi SỞ HỮU chúng.

    N29 — SINH TỪ r11, cross-review codex vòng 5. `_rang_buoc_cua` gom ràng buộc theo phạm vi
    CÚ PHÁP, nhưng `global x` / `nonlocal x` nói rằng phép gán/`import` trong thân này thuộc về
    một phạm vi KHÁC. Bản r10 bỏ qua điều ấy, và nó sai CẢ HAI HƯỚNG — đo được trên `6131cbd`:
      LỌT   `subprocess = object()` ở module, rồi `def f(): global subprocess; import subprocess;
             subprocess.run(["bash"])` ⇒ `[]` — một lời gọi bash THẬT không bị thấy;
      OAN   `def f(): global subprocess; subprocess = gia()` rồi `subprocess.run(["bash"])` ở
             module ⇒ `[(5, 0)]` — báo trên một cái tên đã bị che hợp lệ.
      `nonlocal` cùng bệnh: `[(6, 4)]`.

    Khai báo ĐỌC KHÔNG (`global x` mà không gán gì trong thân) KHÔNG chuyển gì — nếu chuyển thì
    hoá ra vô hiệu hoá tên ấy vì cớ không đâu.
    """
    import ast
    nut_cua, cha_cua, thu_tu = {}, {}, []

    def ghi(nut, cha):
        nut_cua[id(nut)] = nut
        cha_cua[id(nut)] = cha
        thu_tu.append(id(nut))
        xuong(nut, id(nut))

    def xuong(nut, chu):
        for con in ast.iter_child_nodes(nut):
            if isinstance(con, _NUT_PHAM_VI):
                ghi(con, chu)
            else:
                xuong(con, chu)

    ghi(cay, None)
    bang = {i: list(_rang_buoc_cua(nut_cua[i])) for i in thu_tu}
    goc = thu_tu[0]
    _HAM = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
    for i in thu_tu[1:]:
        rieng, toan_cuc, phi_cuc_bo = bang[i]
        for ten in toan_cuc:
            rb = rieng.pop(ten, None)
            if rb:
                bang[goc][0].setdefault(ten, set()).update(rb)
        for ten in phi_cuc_bo:
            rb = rieng.pop(ten, None)
            if not rb:
                continue
            j = cha_cua[i]
            while j is not None and not (isinstance(nut_cua[j], _HAM) and ten in bang[j][0]):
                j = cha_cua[j]
            # Không tìm được chủ sở hữu thì ràng buộc ấy BIẾN MẤT — đúng: `nonlocal` không có
            # phạm vi bao nào ràng buộc tên ấy là một lỗi cú pháp của chính mã được quét.
            if j is not None:
                bang[j][0].setdefault(ten, set()).update(rb)
    return {i: tuple(bang[i]) for i in thu_tu}


def _giai_callee_theo_pham_vi(cay):
    """[(nút `Call`, hàm tra tên)] cho MỌI lời gọi trong cây; hàm tra tên trả
    `(module, hàm|None)` hay None, theo đúng phạm vi từ vựng CHỨA lời gọi ấy.

    Bỏ qua có chủ đích, khai thẳng: decorator/giá trị mặc định của một `def` lồng và `iter`
    đầu tiên của comprehension thật ra thuộc phạm vi NGOÀI; ở đây chúng được giải trong phạm
    vi TRONG. Lệch chỉ lộ khi tham số của chính hàm ấy trùng tên `subprocess`/`shutil` và
    decorator lại gọi `bash` — chưa có phép đo nào cần nó.
    """
    import ast
    ket = []
    bang_cua = _bang_pham_vi_ca_cay(cay)

    def pham_vi(nut):
        bang, toan_cuc, phi_cuc_bo = bang_cua[id(nut)]
        return (isinstance(nut, ast.ClassDef), bang, toan_cuc, phi_cuc_bo)

    def duyet(nut, chuoi):
        for con in ast.iter_child_nodes(nut):
            if isinstance(con, _NUT_PHAM_VI):
                duyet(con, chuoi + [pham_vi(con)])
                continue
            if isinstance(con, ast.Call):
                ket.append((con, lambda ten, c=chuoi: _giai_ten(ten, c)))
            duyet(con, chuoi)

    duyet(cay, [pham_vi(cay)])
    return ket


def _loai_theo_TEN_khong_giai_callee(nut):
    """Bản CŨ — nhận diện CHỈ theo TÊN. Giữ lại làm ĐÍCH CHO ĐỘT BIẾN, không dùng ở đường thật.

    Nó sai CẢ HAI HƯỚNG và cả hai đều đo được: lọt `run(["x"], executable="bash")`, và bắt
    OAN `runner.run(["bash"])` / `matcher.which("bash")` — những API chẳng liên quan stdlib.
    """
    import ast
    ten = (nut.func.attr if isinstance(nut.func, ast.Attribute)
           else nut.func.id if isinstance(nut.func, ast.Name) else None)
    if ten in _TEN_WHICH:
        return "which"
    if ten in _TEN_SPAWN:
        return "spawn"
    return None


def _loai_loi_goi(nut, tra_ten):
    """"which" | "spawn" | None — callee có trỏ vào `shutil`/`subprocess` thật không, hỏi qua
    `tra_ten` (đã gắn với phạm vi CHỨA lời gọi)."""
    import ast
    if isinstance(nut.func, ast.Attribute) and isinstance(nut.func.value, ast.Name):
        muc = tra_ten(nut.func.value.id)
        if not muc or muc[1] is not None:
            return None
        mod, _ = muc
        if nut.func.attr in _MODULE_CHU[mod]:
            return "which" if mod == "shutil" else "spawn"
        return None
    if isinstance(nut.func, ast.Name):
        muc = tra_ten(nut.func.id)
        if muc and muc[1] is not None and muc[1] in _MODULE_CHU[muc[0]]:
            return "which" if muc[0] == "shutil" else "spawn"
    return None

# CHỈ tệp này được phép chứa lời gọi trần — nó LÀ bộ giải. NHƯNG CÓ HẠN NGẠCH, không phải
# một tấm vé vô hạn: cross-review codex trên `1253e3a` chỉ ra, và executor đo lại thấy đúng —
# thêm `BAN_SAO_THU_NAM = shutil.which("bash")` vào CHÍNH tệp này thì cổng vẫn `rc=0 DAT`.
# Packet này tồn tại để chặn BẢN SAO THỨ TƯ, mà chỗ miễn trừ vô hạn lại đúng là nơi BẢN SAO
# THỨ NĂM sẽ mọc — trong tệp không ai nghi ngờ nhất.
# HẠN NGẠCH = 0, và đó là một PHÉP ĐO: bộ giải phân giải `bash` bằng ỨNG VIÊN + phép thử
# NĂNG LỰC, nó không `which("bash")` lần nào. `which("git", …)` không tính vì không phải `bash`.
CHO_PHEP = {
    "ops/bash_nen.py": (0, "bộ giải — quyết bằng NĂNG LỰC nên KHÔNG có lời gọi `bash` trần nào"),
}

# ẢNH CHỤP ĐÔNG CỨNG. `ops/reviews/**` từng được bỏ qua bằng TIỀN TỐ, tức miễn trừ vô hạn:
# ba tệp bẩn thêm vào đó cho `rc=0 DAT` và `co_loi_goi_tran` RỖNG (đo được). Nay là KIỂM KÊ
# TƯỜNG MINH — đúng hai tệp, đúng số lời gọi; một tệp review MỚI mang lời gọi trần sẽ ĐỎ.
ANH_CHUP_DONG_CUNG = {
    "ops/reviews/goi-va-lease-hoi-toan-kho-1/lease_publish_test.py":
        (7, "ảnh chụp verdict đông cứng — `t26` băm lại mỗi lượt, KHÔNG được sửa một byte"),
    "ops/reviews/goi-va-lease-hoi-toan-kho-2/lease_publish_test.py":
        (7, "ảnh chụp verdict đông cứng — như trên"),
}

# RATCHET. Mỗi mục là một tệp CHƯA chuyển sang `tim_bash`, kèm lý do đo được. Cổng ĐỎ theo
# CẢ HAI chiều:
#   · tệp NGOÀI `CHO_PHEP ∪ CHUA_CHUYEN` mà có lời gọi trần  ⇒ ĐỎ (bản sao thứ tư);
#   · tệp TRONG `CHUA_CHUYEN` mà KHÔNG còn lời gọi trần nào ⇒ ĐỎ (danh sách đã mục).
# Chiều thứ hai là thứ bắt danh sách phải NGẮN đi. Thiếu nó thì ratchet thành nghĩa trang:
# ai vá xong cũng quên xoá tên mình, và cổng dần hết ý nghĩa mà vẫn xanh.
# NGAY GO la BAT BUOC cho moi muc (#570 r4, N17). Mot danh sach khong co ngay go la mot
# nghia trang — dung thu N5 sinh ra de chan, chi cham hon.
_NGAY_GO = "2026-12-31"
CHUA_CHUYEN = {
    ".claude/dev/launcher_test.py": (7,
        f"Dòng 6004-6005 là BẢN SAO THỨ TƯ THẬT: `shutil.which(\"bash\")` cộng "
        f"một đường Git Bash GHI CỨNG (`C:/Program Files/Git/bin/bash.exe`) — tức một bộ "
        f"giải RIÊNG quyết bằng ĐƯỜNG DẪN, đúng hình dạng vừa bị gỡ khỏi `_bash_posix` (r2) "
        f"và `_bash_windows` (r3). Ngoài write set của #570. NGÀY GỠ {_NGAY_GO}."),
    ".claude/hooks/session_start.py": (1,
        f"Dòng 58. CHẠY Ở MỌI PHIÊN, nên đây là mục đáng gỡ sớm nhất. Ngoài "
        f"write set của #570. NGÀY GỠ {_NGAY_GO}."),
    ".claude/hooks/subagent_ghi_detect_test.py": (2,
        f"Ngoài write set của #570. NGÀY GỠ {_NGAY_GO}."),
    "scripts/tl_selftest.py": (1,
        f"Dòng 22376. `scripts/**` là runtime phát hành, đụng vào cần packet "
        f"riêng. Ngoài write set của #570. NGÀY GỠ {_NGAY_GO}."),
}
# MỖI MỤC MANG SỐ LẦN ĐƯỢC PHÉP, không phải một tấm vé miễn trừ cho cả tệp — sửa ở r7 sau một
# phép đo. Cross-review codex trên `55f9bce` khai, và executor ĐO LẠI thấy đúng: thêm lời gọi
# trần THỨ HAI vào `.claude/hooks/session_start.py` (mục khai đúng 1 lời gọi) thì cổng vẫn
# `rc=0 DAT`, vì `moi` loại CẢ ĐƯỜNG DẪN còn `da_sach` chỉ bắt lúc về 0.
# Tức đúng những tệp mang nợ cũ — nơi rủi ro cao nhất — là nơi bản sao mới mọc thêm mà không
# ai thấy. Nay so SỐ DÒNG đo được với SỐ KHAI: lệch chiều nào cũng ĐỎ.
# RỖNG TỪ r3 (#570, 20-09-2026). Đây là trạng thái ĐÍCH của ratchet, không phải một danh sách
# chưa ai điền: `CHO_PHEP` nay là chỗ DUY NHẤT trong `ops/**` còn lời gọi trần, và nó là chính
# bộ giải. Thêm một tên vào đây là đi LÙI — chỉ làm khi có phép đo nói rõ vì sao không chuyển
# được, và kèm ngày gỡ.
#
# ĐÃ RỜI DANH SÁCH — ghi lại để người sau thấy ratchet đã NGẮN đi thật, chứ không phải bị xoá:
#   `ops/lease_publish_test.py` (r2) — 7 lời gọi (6 ở `t35`-`t40` + 1 trong `_bash_posix`);
#                                      `_bash_posix` nay uỷ quyền cho `tim_bash()`.
#   `ops/cong_cu_test.py`       (r2) — 3 lời gọi; nay đi qua `_bash_dung_duoc()`.
#   `ops/cong_cu.py`            (r3) — 2 lời gọi: `_bash_windows()` (bộ giải RIÊNG thứ hai,
#                                      quyết bằng ĐƯỜNG DẪN) và nhánh dự phòng của `_chay`
#                                      vốn rẽ sang `shutil.which("bash")` trần trên nền
#                                      KHÔNG phải Windows. Mục thứ hai đáng nhớ: bản cũ chỉ
#                                      gác nền SINH RA khuyết tật, nên nền kia vẫn phân giải
#                                      theo TÊN — đúng chỗ bộ giải thứ tư sẽ mọc lên.
# `t26` là thứ ĐỎ nếu ai để tên chúng nằm lại đây sau khi đã sạch.

# Khong quet: `.git/` (khong phai ma nguon) va `ops/reviews/` (anh chup DONG CUNG cua cac
# ban cu, giu de doi chieu review — khong phai ma dang song).
# CHỈ `.git/` — nó không phải mã nguồn, không ai review nó. `ops/reviews/` đã RỜI khỏi đây
# sang `ANH_CHUP_DONG_CUNG` để chịu hạn ngạch như mọi miễn trừ khác.
_BO_QUA_TOAN_CAY = (".git/",)


def quet(goc: Path):
    """Quét TOÀN CÂY kho. Trả (rc, báo_cáo). Ba trạng thái, không phải hai.

    PHẠM VI MỞ Ở r4 (#570, N17), và lý do là một phép đo chứ không phải một ý hay.
    Bản r3 chỉ quét `ops/**` — trong khi PR của chính packet này mở đầu bằng *"một bộ giải
    dùng chung + một CỔNG chặn bản sao thứ tư"*. Cross-review trên `05ec2eb5` chạy CHÍNH
    `_loi_goi_tran` của PR trên toàn cây và đo được **11 lời gọi / 4 tệp NGOÀI `ops/**`**,
    trong đó `.claude/dev/launcher_test.py:6004` là một bộ giải riêng quyết bằng ĐƯỜNG DẪN
    GHI CỨNG. Tức bản sao thứ tư **đã sống sẵn ngoài hàng rào** trước khi hàng rào dựng lên.

    Cái giá, khai thẳng: ratchet **DÀI RA** (0 → 4 mục), đi ngược tinh thần "ratchet phải
    NGẮN đi". Nhưng thứ phải ngắn đi là **số lời gọi trần CHƯA ĐƯỢC NHÌN THẤY**, không phải
    độ dài danh sách — và con số ấy nay về 0. Mỗi mục mang NGÀY GỠ; N5 (chiều ngược) vẫn bắt
    việc quên xoá khi một mục đã sạch.
    """
    goc = Path(goc)
    if not (goc / "ops").is_dir():
        return RC_KHONG_DO_DUOC, {"trang_thai": "KHONG_DO_DUOC",
                                  "ly_do": f"không thấy {goc / 'ops'} — cây không phải gốc kho"}
    thu_muc = goc
    cac_tep, nguon_tep = _liet_ke_py(goc)
    if nguon_tep.startswith("git-hong"):
        # FAIL-CLOSE (N26). Cây LÀ kho git mà không lấy được INDEX ⇒ không có danh sách để
        # quét. Lùi về `rglob` ở đây là mở lại đúng cái lớp r9 đã giết bằng kiến trúc.
        return RC_KHONG_DO_DUOC, {"trang_thai": "KHONG_DO_DUOC", "nguon_tep": nguon_tep,
                                  "da_quet": str(goc), "pham_vi": "toan-cay",
                                  "ly_do": f"cây có `.git` mà không lấy được INDEX ({nguon_tep})."
                                           " KHÔNG lùi về `rglob`: danh sách rộng hơn thì phán"
                                           " quyết lại phụ thuộc trạng thái LOCAL của máy —"
                                           " đúng lớp mà r9 giết bằng kiến trúc."}
    cac_tep = [m for m in cac_tep
               if not any(m[0].startswith(x) for x in _BO_QUA_TOAN_CAY)]
    _, bien_git_da_go = _moi_truong_git_sach()
    try:
        noi_dung, lien_ket = _doc_noi_dung(goc, cac_tep, nguon_tep)
    except (OSError, UnicodeDecodeError) as e:
        return RC_KHONG_DO_DUOC, {"trang_thai": "KHONG_DO_DUOC", "nguon_tep": nguon_tep,
                                  "da_quet": str(goc), "pham_vi": "toan-cay",
                                  "bien_git_da_go": bien_git_da_go,
                                  "ly_do": f"không đọc được nội dung từ INDEX: {e}"}
    if lien_ket:
        # FAIL-CLOSE CÓ TÊN (N28). Blob của một mục mode `120000` là CHUỖI ĐƯỜNG DẪN, không
        # phải mã. Đọc nó trên cây làm việc thì `read_text()` đi theo ra NGOÀI kho và phán
        # quyết lại phụ thuộc byte ngoài kho — đúng lớp r11 giết bằng kiến trúc.
        return RC_KHONG_DO_DUOC, {"trang_thai": "KHONG_DO_DUOC", "nguon_tep": nguon_tep,
                                  "da_quet": str(goc), "pham_vi": "toan-cay",
                                  "lien_ket_tuong_trung": lien_ket,
                                  "bien_git_da_go": bien_git_da_go,
                                  "ly_do": "mục `*.py` trong INDEX là SYMLINK: "
                                           + ", ".join(lien_ket)
                                           + ". Nội dung thật nằm NGOÀI thứ INDEX ghim, nên cổng "
                                             "không đo được — `None ≠ False`."}
    co_loi_goi = {}
    for rel, than in sorted(noi_dung.items()):
        try:
            dong = _loi_goi_tran(than)
        except (SyntaxError, ValueError) as e:
            # FAIL-CLOSE. Một tệp không phân tích được là một tệp KHÔNG ĐO ĐƯỢC, không
            # phải một tệp sạch — `None ≠ False`.
            return RC_KHONG_DO_DUOC, {"trang_thai": "KHONG_DO_DUOC", "nguon_tep": nguon_tep,
                                      "bien_git_da_go": bien_git_da_go,
                                      "ly_do": f"không đọc/phân tích được {rel}: {e}"}
        if dong:
            co_loi_goi[rel] = dong

    # MỘT LUẬT ĐẾM CHO MỌI BẢNG MIỄN TRỪ (r7 vòng 2). Ba bảng, ba ý nghĩa khác nhau —
    # `CHO_PHEP` vĩnh viễn, `CHUA_CHUYEN` có ngày gỡ, `ANH_CHUP_DONG_CUNG` bất biến — nhưng
    # CÙNG MỘT LUẬT: mỗi mục mang hạn ngạch, và lệch chiều nào cũng ĐỎ. Miễn trừ khai theo
    # TƯ CÁCH THÀNH VIÊN là lớp khuyết tật mà vòng này tìm ra BA thực thể.
    _MIEN_TRU = {}
    for _bang in (CHO_PHEP, CHUA_CHUYEN, ANH_CHUP_DONG_CUNG):
        _MIEN_TRU.update(_bang)
    moi = {t: d for t, d in co_loi_goi.items() if t not in _MIEN_TRU}
    # HẠN NGẠCH THEO SỐ LẦN, không theo tư cách thành viên (r7). Lệch CHIỀU NÀO cũng ĐỎ:
    # nhiều hơn = bản sao mới mọc trên đúng tệp mang nợ; ít hơn = đã vá mà quên hạ con số,
    # và một con số không còn đúng thì lần sau không ai dám tin nó.
    lech_so, khong_khai_so = {}, []
    for t, muc in _MIEN_TRU.items():
        cho_phep, _ = _so_cho_phep(muc)
        if cho_phep is None:
            khong_khai_so.append(t)
            continue
        thay = len(co_loi_goi.get(t, []))
        # HẠN NGẠCH LÀ HẠN NGẠCH Ở MỌI GIÁ TRỊ, KỂ CẢ 0 (r8, F1 codex vòng 3). r7 viết
        # `if thay and thay != cho_phep` — về 0 thì THÔI so, và `da_sach` chỉ phủ
        # `CHUA_CHUYEN`. Đo được: mục `ANH_CHUP_DONG_CUNG` khai 7, còn 7 ⇒ `lech_so={}`
        # (đúng); về 0 ⇒ cũng `lech_so={}` (sai — ảnh chụp "đông cứng" mất sạch lời gọi mà
        # cổng vẫn xanh). `CHO_PHEP["ops/bash_nen.py"]` khai 0 và ĐANG 0: `0 != 0` là sai nên
        # nó KHÔNG đỏ oan — vì so đủ hai vế, thay vì hỏi "có thấy gì không" rồi mới so.
        if thay != cho_phep:
            lech_so[t] = {"khai": cho_phep, "do_duoc": thay,
                          "dong": co_loi_goi.get(t, [])}
    # `da_sach` là chiều ngược RIÊNG của `CHUA_CHUYEN` — ratchet có NGÀY GỠ, phải ngắn đi, nên
    # thông điệp của nó là "xoá khỏi danh sách". Một mục số về 0 rơi vào CẢ `lech_so` lẫn đây;
    # báo cáo mang cả hai khoá, và đó là cố ý: hai luật, hai lý do, cùng một phán quyết.
    da_sach = [t for t in CHUA_CHUYEN if t not in co_loi_goi]
    bao = {"da_quet": str(thu_muc), "pham_vi": "toan-cay", "nguon_tep": nguon_tep,
           "nguon_noi_dung": "blob-index" if nguon_tep == "git" else "cay-lam-viec",
           "bien_git_da_go": bien_git_da_go, "co_loi_goi_tran": co_loi_goi,
           "ngoai_danh_sach": moi, "muc_ratchet_da_sach": sorted(da_sach), "lech_so_loi_goi": lech_so,
           "cho_phep": sorted(CHO_PHEP), "anh_chup": sorted(ANH_CHUP_DONG_CUNG), "chua_chuyen": sorted(CHUA_CHUYEN),
           "so_cho_phep": {t: _so_cho_phep(m)[0] for t, m in sorted(_MIEN_TRU.items())}}
    if khong_khai_so:
        # FAIL-CLOSE. Một mục miễn trừ không khai hạn ngạch số là một mục KHÔNG ĐO ĐƯỢC,
        # không phải một mục được tha — r7 tha nó, và đó là vé vô hạn (xem `_so_cho_phep`).
        bao["trang_thai"] = "KHONG_DO_DUOC"
        bao["ly_do"] = ("mục miễn trừ KHÔNG khai hạn ngạch số: " + ", ".join(sorted(khong_khai_so))
                        + ". Mỗi mục phải là `(số_lần, lý_do)`; một chuỗi trần là miễn trừ "
                          "theo TƯ CÁCH THÀNH VIÊN — đo được: mục chuỗi, 9 lời gọi ⇒ DAT.")
        return RC_KHONG_DO_DUOC, bao
    if moi:
        bao["trang_thai"] = "DO"
        bao["ly_do"] = (
            "có lời gọi `bash` TRẦN ở tệp ngoài danh sách cho phép: "
            + "; ".join(f"{t}:{d}" for t, d in sorted(moi.items()))
            + ". Dùng `ops/bash_nen.py::tim_bash()` — nó QUYẾT BẰNG NĂNG LỰC, và "
              "`shutil.which(\"bash\")` trên Windows trả bộ phóng WSL (Issue #570).")
        return RC_DO, bao
    if lech_so:
        bao["trang_thai"] = "DO"
        bao["ly_do"] = (
            "số lời gọi trần LỆCH với hạn ngạch khai (CHO_PHEP ∪ CHUA_CHUYEN ∪ ANH_CHUP_DONG_CUNG): "
            + "; ".join(f"{t} khai {v['khai']} mà đo được {v['do_duoc']} (dòng {v['dong']})"
                        for t, v in sorted(lech_so.items()))
            + ". Nhiều hơn ⇒ bản sao MỚI mọc trên tệp mang nợ; ít hơn ⇒ đã vá mà quên hạ "
              "con số; về 0 ⇒ mục đã chết, xoá nó. Cả ba đều phải sửa danh sách, không được "
              "để lệch.")
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
    q.add_argument("--tat-ca", dest="tat_ca", action="store_true",
                   help="CHẨN ĐOÁN: thử MỌI ứng viên thay vì dừng ở cái đầu tiên đạt")
    r = sub.add_parser("quet", help="cổng: chặn lời gọi `bash` trần mới trong ops/**")
    r.add_argument("--root", default=".")
    r.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    if a.lenh == "tim":
        duong, chan_doan = tim_bash(tat_ca=getattr(a, "tat_ca", False))
        out = {"duong": duong, "chan_doan": chan_doan,
               "da_thu_moi_ung_vien": bool(getattr(a, "tat_ca", False)),
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
