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
import datetime as _dt
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

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

    ghi_de = env.get("CONG_CU_BASH")
    # N57 (r17) — `PATH` VẮNG khác `PATH` RỖNG, và luật ấy là của HỆ ĐIỀU HÀNH chứ không
    # phải của ta. `os.get_exec_path()`/`execvp` dùng `os.defpath` khi biến VẮNG, còn một
    # `PATH=""` tường minh nghĩa là "đừng tìm ở đâu cả". Bản trước gộp hai ca vào `""`, nên
    # trên một máy KHÔNG đặt `PATH` thì `ung_vien()` trả `[]` và cổng báo KHONG_DO_DUOC —
    # đo được: `subprocess.run(["bash"])` trên CHÍNH máy ấy vẫn tìm thấy `/bin/bash`.
    # `None ≠ ""`, cùng một họ với `None ≠ False` mà packet này chống.
    if path is None:
        path = env["PATH"] if "PATH" in env else os.defpath
    # N70 (r19) — GHI ĐÈ BẰNG TÊN TRẦN PHẢI PHÂN GIẢI QUA PATH, rồi phép thử VÀ vân tay dùng
    # CÙNG một đường. Bản r18 đưa thẳng chuỗi `bash` vào: phép thử chạy nó qua PATH (tệp A),
    # còn `_van_tay_tep("bash")` `stat` một tệp `bash` ở THƯ MỤC HIỆN TẠI (tệp B). Đo được ở
    # vòng 13: có `./bash` giữ chỗ, PATH trỏ bash thật, `CONG_CU_BASH=bash`; thay bash trong
    # PATH bằng một bản `exit 7` ⇒ cache vẫn trả `bash`, đo lại trả `None`. Vân tay canh NHẦM
    # tệp. Giải cùng ngữ nghĩa N62 (thành phần rỗng là thư mục hiện tại). Đường có dấu phân
    # cách (`./bash`, `/usr/bin/bash`) giữ nguyên — người đặt đã chỉ đích danh tệp.
    if ghi_de:
        if os.sep in ghi_de or (os.altsep and os.altsep in ghi_de):
            them(ghi_de)
        else:
            for d in path.split(os.pathsep):
                # KHÔNG đặt tên `thay`: đó là tập khử trùng lặp mà `them` đóng quanh. Bản đầu của
                # N70 gán đè nó bằng một CHUỖI, và `k in thay` thành phép so chuỗi con — mọi ứng
                # viên bị bỏ, `ung_vien()` ra `[]`. Đo được ngay trước khi đẩy.
                tim_thay = shutil.which(ghi_de, path=d or os.curdir)
                if tim_thay:
                    them(os.path.join(d or os.curdir, os.path.basename(tim_thay)))
                    break
            else:
                # Không phân giải được ⇒ giữ tên trần: phép thử sẽ trượt đúng như `subprocess`
                # trượt, và một ứng viên MỚI xuất hiện sau đó làm N56 đếm lại.
                them(ghi_de)
    sr = env.get("SystemRoot", "") if system_root is None else system_root
    sr_norm = os.path.normcase(os.path.abspath(sr)).rstrip("\\/") if sr else None

    duoi_sr = []
    for d in path.split(os.pathsep):
        # N62 (r18) — THÀNH PHẦN RỖNG LÀ THƯ MỤC HIỆN TẠI, và `PATH=""` là MỘT thành phần rỗng.
        # Bản r17 viết ngược lại — *"một `PATH=""` tường minh nghĩa là đừng tìm ở đâu cả"* — và
        # gán nó cho HỆ ĐIỀU HÀNH mà KHÔNG ĐO. Vòng 12 đo, phiên đo lại, cả ba cùng một chiều:
        #   `os.get_exec_path({"PATH": ""})`           ⇒ `['']`
        #   `PATH= bash -c 'echo OK'` ở thư mục có bash   ⇒ rc=0 `OK`
        #   `subprocess.run(["bash"], env={"PATH": ""})` ⇒ rc=0 `OK`
        # Đó là LỜI KHAI RỘNG HƠN PHÉP ĐO — đúng họ N6 — và lần này do chính phiên viết ra.
        # CHUỖI ỨNG VIÊN phải là `./bash`, KHÔNG phải `bash`: `Path(".") / "bash"` chuẩn hoá
        # mất dấu `.` và cho ra một TÊN TRẦN, tức phép thử năng lực sẽ đi tìm theo PATH thay vì
        # thử đúng tệp ở thư mục hiện tại.
        # CHƯA ĐO trên Windows: `CreateProcess` có luật tìm thư mục hiện tại riêng.
        d = d or os.curdir
        for ten in ("bash.exe", "bash"):
            u = Path(os.path.join(d, ten))
            try:
                if not u.is_file():
                    continue
            except OSError:
                continue
            chuoi_u = os.path.join(d, ten)   # giữ `./` — xem N62 ở trên
            if _duoi_system_root(u, sr_norm):
                duoi_sr.append(chuoi_u)
            else:
                them(chuoi_u)
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


def _van_tay_tep(duong):
    """Dấu nhận dạng MỘT tệp ứng viên, hay None khi không `stat` được (N51, r16).

    Gồm cả `st_ino`/`st_dev` lẫn `st_mtime_ns`/`st_size`/`st_mode`: thay tệp bằng `rename`
    đổi inode, ghi đè tại chỗ đổi mtime+size, đổi quyền đổi mode. Không cái nào MỘT MÌNH đủ.
    Tệp biến mất ⇒ None, và None ≠ bất cứ vân tay nào ⇒ đo lại. Đúng `None ≠ False`.
    """
    try:
        st = os.stat(duong)
    except OSError:
        return None
    return (st.st_mtime_ns, st.st_size, st.st_ino, st.st_dev, st.st_mode)


def _van_tay_ung_vien(chan_doan):
    """Vân tay của MỌI ứng viên đã thử trong một lượt đo.

    GIÁ PHẢI TRẢ, khai thẳng: mỗi lần trúng cache nay tốn thêm một `os.stat` cho mỗi ứng
    viên — rẻ hơn nhiều bậc so với phép thử năng lực (mỗi phép là một tiến trình con), nên
    đổi được. CÒN LẠI MỘT KHE không đóng được: tệp vẫn có thể bị thay GIỮA lúc so vân tay
    và lúc thật sự chạy. Đó là đua ở mức hệ điều hành, không phải ở cache; ghi ra đây thay
    vì để người sau tưởng đã kín.
    """
    return tuple((c["duong"], _van_tay_tep(c["duong"])) for c in chan_doan)


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
    # (xem `_van_tay_ung_vien` cho N51 — van tay TEP, ben canh khoa DAU VAO)
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
    # N61 (r18) — KHOÁ THEO TOÀN BỘ MÔI TRƯỜNG, không theo một DANH SÁCH biến. Bản r4..r17
    # liệt kê năm biến mà `ung_vien()` đọc — nhưng thứ quyết phán quyết là PHÉP THỬ NĂNG LỰC,
    # và phép thử ấy chạy `bash`, mà `bash` đọc môi trường của chính nó. Đo được ở vòng 12:
    # cache `/bin/bash` xong, đặt `BASH_ENV` trỏ vào một tệp `exit 7` ⇒ cache vẫn trả
    # `/bin/bash`, còn đo lại trả `None` (`phép argv: rc=7`). `BASH_ENV`, `ENV`, `SHELLOPTS`,
    # `BASHOPTS`, `POSIXLY_CORRECT`… danh sách ấy KHÔNG BAO GIỜ ĐỦ — đúng bài học `CLAUDE.md`
    # về danh sách CẤM. Nên khoá băm TẤT CẢ: mọi thay đổi môi trường làm cache hết hiệu lực.
    # GIÁ: một biến chẳng liên quan đổi cũng làm đo lại. Trong một tiến trình, môi trường
    # hiếm khi đổi, nên giá ấy gần như bằng không. Chỉ lưu BĂM, không lưu giá trị — môi
    # trường có thể mang bí mật.
    van_tay_moi_truong = hashlib.sha256(
        json.dumps(sorted(os.environ.items())).encode("ascii")).hexdigest()
    khoa = json.dumps([sorted(ep.items()), bool(tat_ca), van_tay_moi_truong,
                       os.getcwd()], default=str)
    # N51 (r16) — KHOA DU MA TRA LOI VAN CU. Khoa gom moi DAU VAO, nhung ket qua khong
    # sinh ra tu dau vao — no sinh ra tu phep thu NANG LUC tren mot TEP. Thay chinh tep ay
    # tai cho (mot trinh cai ghi de thu `CONG_CU_BASH` tro toi) thi khoa khong doi mot bit,
    # va cache tra lai phan quyet cu. Do duoc tren `8180970`, CA HAI CHIEU:
    #   tot -> xau: `tim_bash()` tra `/tmp/f1cache/bash` trong khi `dung_cache=False` tra
    #                `None` (`chan_doan`: "phép argv: rc=7");
    #   xau -> tot: `tim_bash()` tra `None` trong khi khong cache tra dung duong ay.
    # Chieu THU HAI moi la chieu dau doc: cong bao "KHONG CO bash" tren mot may DA CO.
    # VAN TAY phai phu MOI ung vien da thu, khong chi ke thang — vi khi ket qua la `None`
    # thi khong co ke thang nao, ma `chan_doan` chinh la thu phai het hieu luc.
    # N56 (r17) — VÂN TAY PHẢI PHỦ CẢ TẬP ỨNG VIÊN, không chỉ những ứng viên ĐÃ THỬ.
    # N51 chụp vân tay của `chan_doan`, mà `chan_doan` chỉ chứa thứ đã có mặt lúc đo. Một
    # `bash` MỚI xuất hiện trong một thư mục `PATH` KHÔNG đổi thì không ứng viên cũ nào đổi,
    # nên vân tay khớp và cache trả lại câu trả lời cũ. Đo được ở vòng 11, chiều độc nhất:
    # thư mục rỗng ⇒ cache `(None, [])`; thêm một symlink `bash`; cache vẫn trả `None` trong
    # khi `dung_cache=False` tìm thấy và chấp nhận nó — cổng báo KHÔNG CÓ `bash` trên máy ĐÃ
    # CÓ. Chữa: ĐẾM LẠI ứng viên ở mỗi lần trúng cache. Phép đếm chỉ `stat`, không phóng tiến
    # trình nào, nên vẫn rẻ hơn phép thử năng lực nhiều bậc — cache vẫn là cache (`t51` chốt
    # chiều ấy).
    if dung_cache and khoa in _CACHE:
        kq_cu, ds_cu, van_tay_cu = _CACHE[khoa]
        ds_moi = ung_vien(**ep)
        if ds_moi == ds_cu and van_tay_cu == _van_tay_ung_vien(kq_cu[1]):
            return kq_cu
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
        _CACHE[khoa] = (kq, ung_vien(**ep), _van_tay_ung_vien(chan_doan))
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
# N45 (r16) — HAI HELPER CHAY QUA SHELL. `subprocess.getoutput("bash")` va
# `getstatusoutput("bash")` phong bash THAT qua `/bin/sh -c`; tren Windows chung di dung cai
# duong dan WSL ma packet nay sinh ra de chan. Do duoc tren `8180970` truoc va:
#   `_loi_goi_tran('import subprocess\nsubprocess.getoutput("bash")')`       => []
#   `_loi_goi_tran('import subprocess\nsubprocess.getstatusoutput("bash")')` => []
# va `subprocess.getstatusoutput("bash -c ...")` CHAY THAT, tra `(0, 'XIN_CHAO')`.
# CHU KY KHAC `Popen`: doi so DAU la `cmd` — mot CHUOI LENH SHELL — va KHONG co `executable`.
# Nen chung di rieng mot loai, khong muon luat vi tri thu ba cua `Popen`.
_TEN_SHELL_RA = ("getoutput", "getstatusoutput")
# N59 (r18) — CÁC API KHÁC PHÓNG `bash` THEO TÊN. Từ r8 docstring của `_loi_goi_tran` khai
# `os.system` / `os.execvp` / `asyncio.create_subprocess_exec` là NỢ CÓ TÊN; verdict r16 và
# r17 xin reviewer ĐO cái nào chạy thật để nâng lên luật. Vòng 12 đo ba cái; phiên đo thêm
# sáu. Cả CHÍN đều CHẠY BASH THẬT trên nền này (tiến trình con cô lập, in ra `OK`).
# MỖI MỤC MANG BA THUỘC TÍNH, và cả ba đều là PHÉP ĐO chứ không phải suy luận theo "loại":
#   · vị trí đối số mang tên chương trình, và tên từ khoá của nó (đọc `inspect.signature`);
#   · KIỂU được nhận. Gộp theo loại là SAI: `os.system(Path("bash"))` CHẠY, còn `os.popen`
#     và `create_subprocess_shell` ném `TypeError`/`ValueError` với path-like; `os.popen` còn
#     từ chối cả `bytes`. Bắt lời gọi mà runtime từ chối là BÁO ĐỘNG GIẢ — đúng lỗi F3 vòng 11.
# KHÔNG CÓ biến thể không-`p` (`execv`, `posix_spawn`, `spawnv`): chúng KHÔNG tìm theo PATH
# — đo được `execv("bash", …)` ném `FileNotFoundError` — nên `"bash"` ở đó là `./bash`, không
# phải khuyết tật packet này chặn.
_S, _B, _P = "str", "bytes", "path"
_API_THEO_TEN = {
    ("os", "execvp"): (0, "file", (_S, _B, _P)),
    ("os", "execvpe"): (0, "file", (_S, _B, _P)),
    ("os", "execlp"): (0, "file", (_S, _B, _P)),
    ("os", "execlpe"): (0, "file", (_S, _B, _P)),
    ("os", "posix_spawnp"): (0, "path", (_S, _B, _P)),
    ("os", "spawnlp"): (1, "file", (_S, _B, _P)),
    ("os", "spawnlpe"): (1, "file", (_S, _B, _P)),
    ("os", "spawnvp"): (1, "file", (_S, _B, _P)),
    ("os", "spawnvpe"): (1, "file", (_S, _B, _P)),
    ("os", "system"): (0, "command", (_S, _B, _P)),
    ("os", "popen"): (0, "cmd", (_S,)),
    ("asyncio", "create_subprocess_exec"): (0, "program", (_S, _B, _P)),
    ("asyncio", "create_subprocess_shell"): (0, "cmd", (_S, _B)),
}
# N66 (r19) — `pty.spawn(argv)` PHÓNG THEO TÊN, và đối số của nó là một ARGV chứ không phải
# một tên vô hướng: `pty.spawn(["bash", "-c", …])` in ra `PTY_OK`. Đo thêm chiều mà vòng 13
# dặn cẩn thận — `pty.spawn("bash")` với CHUỖI TRẦN — và nó CŨNG CHẠY (`rc 0`): `pty` đổi một
# chuỗi thành bộ một phần tử. Nên nó dùng đúng luật argv `_la_vec_bash`, không dùng bảng vô
# hướng `_API_THEO_TEN`.
_API_ARGV = {("pty", "spawn"): (0, "argv")}
# Vỏ bọc GIỮ HẰNG mà bộ tính hằng gấp được khi callee giải về đúng module (N58).
_BOC_OS = ("fspath", "fsencode", "fsdecode")
_KHOA_SHELL_RA = ("cmd",)
_LOAI_THEO_TEN = {**{t: "which" for t in _TEN_WHICH},
                  **{t: "spawn" for t in _TEN_SPAWN},
                  **{t: "shell_ra" for t in _TEN_SHELL_RA}}
# N45 (r16) — TEN CHUONG TRINH VIET QUA `pathlib`. `subprocess.run([Path("bash")])`,
# `run(["nhan"], executable=Path("bash"))` va `shutil.which(Path("bash"))` deu CHAY bash that
# (do duoc: `run([Path("bash")], ...)` in ra `OK`), nhung bo loc hang chi nhan `str`/`bytes`
# nen ca ba deu ra `[]`. Day KHONG phai mot API moi — no la CUNG mot cach viet ten chuong
# trinh, chi khac vo boc. Lop "so khop theo MOT cach viet" nay da lap lai lan thu TU trong
# packet (casefold r7, bytes r11, duoi `.pyw` r12, nay `Path`).
_TEN_DUONG_PATHLIB = ("Path", "PurePath", "PosixPath", "WindowsPath",
                      "PurePosixPath", "PureWindowsPath")


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


_DUOI_PY = (".py", ".pyw")


def _la_nguon_py(rel: str) -> bool:
    """N35 (r12) — HẬU TỐ so KHÔNG phân biệt hoa/thường, và `.pyw` cũng là nguồn Python.

    Đo được trên `1d63f80`: `git ls-files --cached -s -- '*.py'` trả RỖNG cho `VI_PHAM.PY` và
    `w.pyw`, nên cả hai vô hình với cổng dù cả hai đều `shutil.which("bash")`. Pathspec `*.py`
    là một phép so THEO MỘT CÁCH VIẾT — cùng lớp với mặt hoa/thường ở r7 và mặt byte ở r11.
    Đây là thực thể THỨ BA của lớp ấy, nên nó được đưa ra MỘT HÀM thay vì vá tại chỗ.
    """
    return rel.casefold().endswith(_DUOI_PY)


def _giai_ma_nguon(raw: bytes) -> str:
    """N34 (r12) — giải mã theo ĐÚNG khai báo của chính tệp, không giả định UTF-8.

    Python hợp lệ KHÔNG nhất thiết là UTF-8: PEP 263 cho phép `# coding: latin-1`, và một BOM
    UTF-8 ở đầu tệp cũng hợp lệ. Bản r11 giải mã cứng `utf-8`, và đo được trên `1d63f80`:
        `# coding: latin-1` + một ký tự Latin-1  ⇒ rc=3 KHONG_DO_DUOC (UnicodeDecodeError)
        tệp có BOM                               ⇒ rc=3 (U+FEFF lọt vào `ast.parse`)
    Tức một tệp Python HỢP LỆ làm cổng CHẶN VĨNH VIỄN cả kho. Fail-close đúng chỗ là khi
    KHÔNG ĐO ĐƯỢC; ở đây nó đo được, chỉ là đọc sai cách.
    """
    import io, tokenize
    ma, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
    van = raw.decode(ma)
    return van[1:] if van.startswith("\ufeff") else van


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
    # N32 (r12) — REF THAY THẾ. `git replace <xấu> <sạch>` là một ref CỦA MÁY, và `cat-file`
    # trả bytes thay thế một cách trong suốt. Đo được trên `1d63f80`: sau `git replace`,
    # `ngoai_danh_sach` RỖNG; đặt `GIT_NO_REPLACE_OBJECTS=1` thì ra `['vi_pham.py']`.
    # Đây là MẶT THỨ TÁM của lớp *phán quyết phụ thuộc trạng thái LOCAL của máy* — và nó là
    # đúng món NỢ mà spec r11 đã KHAI TRƯỚC: *"danh sách biến git bị gỡ KHÔNG BAO GIỜ ĐỦ"*.
    # Nợ ấy nay đến hạn; cơ chế không đổi, chỉ thêm một biến và một cờ.
    da_go = sorted(k for k in moi
                   if k in _BIEN_GIT_CHON_KHO
                   or k.startswith("GIT_CONFIG_KEY_") or k.startswith("GIT_CONFIG_VALUE_"))
    for k in da_go:
        moi.pop(k, None)
    return moi, da_go


def _chay_git(goc: Path, *doi_so, **kw):
    """MỘT chỗ duy nhất dựng mọi tiến trình `git` con của cổng.

    HAI hàng rào cho ref thay thế nằm CÙNG MỘT CHỖ có lý do đo được: nếu tách ra hai nơi thì
    KHÔNG đột biến nào đo được cái nào — bỏ một hàng rào thì hàng rào kia vẫn che, và một luật
    không thể ĐỎ thì không phải luật. Gom lại đây thì một đột biến gỡ cả hai, và `t47` chốt (1)
    ĐỎ được.
      · `--no-replace-objects` (cờ) và `GIT_NO_REPLACE_OBJECTS=1` (biến) — ref thay thế là ref
        CỦA MÁY; `cat-file` trả bytes thay thế một cách trong suốt (N32);
      · môi trường đã gỡ mọi biến chọn kho / chọn index / tiêm cấu hình (N28).
    """
    env, _ = _moi_truong_git_sach()
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return subprocess.run(["git", "--no-replace-objects", "-C", str(goc), *doi_so],
                          env=env, **kw)


def _duong_bao_cao(rel: str) -> str:
    r"""Đường dẫn AN TOÀN cho báo cáo. Giữ nguyên đường Unicode thường; đường mang byte không
    giải mã được thì đổi surrogate thành `\\xNN` đọc được.

    N43 (r15) — N36 giữ byte thô bằng `surrogateescape`, và đó là ĐÚNG cho việc đối chiếu với
    INDEX. Nhưng chuỗi ấy đi thẳng ra `json.dumps(..., ensure_ascii=False)` thì stdout phát lại
    byte thô và **một bộ đọc JSON UTF-8 nghiêm từ chối**. Đo được trên `f6189e3`: đường
    `ops/xau_\xff.py` ⇒ rc=2 kèm đầu ra `UnicodeDecodeError`.
    Chính verdict r13 đã KHAI món nợ này — *"báo cáo một đường như vậy ra JSON trên nền khác
    thì CHƯA ĐO"*. Nay đo được, nên trả.
    Đường dẫn NỘI BỘ vẫn nguyên vẹn; chỉ biên giới BÁO CÁO mới đổi.

    N54 (r17) — PHÉP NÀY PHẢI ĐƠN ÁNH, và bản r15/r16 thì KHÔNG. Đặc tả r15 tự khai chỗ chưa
    đo: *"hai đường khác nhau về byte CÓ THỂ in ra giống nhau — chưa đo trường hợp ấy"*. Vòng
    11 đo được: một đường mang byte `0xff` cho `ops/bad_\xff.py`, còn một đường KHÁC chứa
    đúng bốn ký tự ASCII `\`,`x`,`f`,`f` cũng cho `ops/bad_\xff.py` — **hai đường khác nhau,
    một chuỗi**. Chuỗi ấy là KHOÁ của `co_loi_goi_tran`, nên một tệp ghi đè vị trí của tệp kia
    và hạn ngạch đếm sai. Chữa bằng cách **nhân đôi dấu chéo ngược TRƯỚC** khi thoát surrogate:
    sau đó mọi `\x` ĐƠN trong kết quả chỉ có thể đến từ một surrogate, nên phép đổi có nghịch
    đảo. GIÁ: một đường chứa dấu chéo ngược THẬT nay in ra dấu đôi — đổi lấy việc hai đường
    không bao giờ đè nhau nữa.
    KHOÁ BÁO CÁO thì KHÔNG dùng phép này nữa: `co_loi_goi_tran` giữ đường NGUYÊN VẸN, và
    `_ra_json` lo phần an toàn ở biên giới. Hai lớp, mỗi lớp một việc.
    """
    rel = rel.replace("\\", "\\\\")
    try:
        rel.encode("utf-8")
        return rel
    except UnicodeEncodeError:
        return rel.encode("utf-8", "surrogateescape").decode("utf-8", "backslashreplace")


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
            ra[rel] = _giai_ma_nguon((goc / rel).read_bytes())
        return ra, []
    lien_ket = sorted(rel for rel, che_do, _ in muc if che_do == "120000")
    if lien_ket:
        return None, lien_ket
    if not muc:
        return {}, []
    yeu_cau = "".join(sha + "\n" for _, _, sha in muc).encode("ascii")
    pc = _chay_git(goc, "cat-file", "--batch", input=yeu_cau,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
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
        ra[rel] = _giai_ma_nguon(than)
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
        try:
            # N36 (r13) — KHÔNG `text=True`. Dịch dòng phổ quát chạy TRƯỚC khi tách khung
            # `\0`/`\t`, nên `ops/va\r.py` và `ops/va\n.py` — HAI đường khác nhau trong INDEX —
            # gộp thành MỘT `rel`, và `_doc_noi_dung` ghi đè im lặng. Đo được trên `cf6e6cb`:
            # tệp `\r` mang lời gọi trần, tệp `\n` sạch với OID cao hơn ⇒ `rc=0 DAT`,
            # `co_loi_goi_tran` RỖNG. Tách khung trên BYTES rồi mới giải mã, và giải mã bằng
            # `surrogateescape` để không mất byte nào.
            pc = _chay_git(goc, "ls-files", "--cached", "-s", "-z",
                           capture_output=True, timeout=60)
            if pc.returncode == 0:
                muc, chua_hoa_giai = [], set()
                for tho in pc.stdout.split(b"\0"):
                    if not tho:
                        continue
                    dau_b, tab, rel_b = tho.partition(b"\t")
                    if not tab:
                        return [], f"git-hong: ls-files -s trả dòng lạ {tho[:120]!r}"
                    truong = dau_b.decode("ascii", "replace").split()
                    rel = rel_b.decode("utf-8", "surrogateescape")
                    if len(truong) < 3 or not rel:
                        return [], f"git-hong: ls-files -s trả dòng lạ {tho[:120]!r}"
                    # N35 — LỌC HẬU TỐ Ở ĐÂY, không bằng pathspec `*.py`: pathspec so theo MỘT
                    # cách viết nên `VI_PHAM.PY` và `w.pyw` vô hình (đo được: ls-files trả rỗng).
                    if not _la_nguon_py(rel):
                        continue
                    # N33 — STAGE LÀ MỘT PHẦN CỦA BẢN GHI. `ls-files -s` phát stage 1/2/3 cho
                    # đường chưa hoà giải; bản r11 vứt trường ấy đi, nên ba bản ghi cùng `rel`
                    # rơi vào cùng một khoá của `noi_dung` và blob có SHA LỚN NHẤT thắng. Đo
                    # được: xung đột có stage 1/2 mang lời gọi trần, stage 3 sạch ⇒ cổng cho qua.
                    if truong[2] != "0":
                        chua_hoa_giai.add(rel)
                        continue
                    muc.append((rel, truong[0], truong[1]))
                if chua_hoa_giai:
                    # FAIL-CLOSE. Một INDEX chưa hoà giải KHÔNG có blob nào để duyệt: chọn bừa
                    # một stage là tự bịa ra một cây chưa từng tồn tại.
                    return [], ("git-hong: INDEX chưa hoà giải ở "
                                + ", ".join(sorted(chua_hoa_giai))
                                + " — không có blob stage-0 nào để duyệt")
                return sorted(set(muc)), "git"
            return [], ("git-hong: ls-files rc=%d %r"
                        % (pc.returncode, pc.stderr.decode("utf-8", "replace").strip()[:200]))
        except (OSError, subprocess.SubprocessError) as e:
            return [], f"git-hong: {type(e).__name__}: {e}"
    return sorted((x.relative_to(goc).as_posix(), None, None)
                  for x in goc.rglob("*")
                  if x.is_file() and _la_nguon_py(x.name)), "rglob"


def _so_cho_phep(muc):
    """(so_lan_duoc_phep, ly_do) cua mot mục miễn trừ.

    `(số, lý_do)` là hình dạng DUY NHẤT hợp lệ. Một CHUỖI trần trả `(None, chuỗi)` để báo cáo
    in được, nhưng `quet()` coi mục ấy là KHÔNG ĐO ĐƯỢC chứ không tha — r7 từng cho chuỗi
    giữ "luật cũ, chỉ bắt lúc về 0", và đó là một VÉ VÔ HẠN đúng nghĩa: đo được ở r8, mục
    chuỗi với 9 lời gọi ⇒ `rc=0 DAT`. Cùng lớp với F1 (hạn ngạch 0 bị bỏ qua): miễn trừ khai
    theo TƯ CÁCH THÀNH VIÊN thay vì theo HẠN NGẠCH. `t40` đọc bảng THẬT để chặn ngay lúc khai.
    """
    if isinstance(muc, (tuple, list)) and len(muc) in (2, 3):
        # N63 (r18) — KHÔNG ÉP KIỂU, HỎI KIỂU. Bản trước gọi `int(muc[0])` vô điều kiện, nên
        # một hạn ngạch gõ nhầm ném `ValueError` TRƯỚC khi `quet()` kịp vào nhánh fail-close
        # đã khai — đo được: `("not-a-number", "lý do")` ⇒ CLI thoát 1 kèm traceback thay vì
        # báo cáo ba trạng thái. `bool` bị loại tường minh vì `True` LÀ một `int` (bằng 1)
        # trong Python; số âm bị loại vì một hạn ngạch âm không có nghĩa. Trả `None` ⇒ mục ấy
        # rơi đúng vào `khong_khai_so` ⇒ KHONG_DO_DUOC. `None ≠ False`.
        so = muc[0]
        if not isinstance(so, int) or isinstance(so, bool) or so < 0:
            return None, str(muc[-1])
        return so, str(muc[-1])            # (số, lý do) hay (số, OID, lý do) — N38
    return None, str(muc)


def _oid_dong_cung(muc):
    """OID blob mà mục miễn trừ GHIM, hay None khi mục không ghim gì HỢP LỆ (N38, N71).

    N71 (r19) — CHỈ bộ ba với một OID 40 ký tự hex thường. Bản r18 trả `str(muc[1])` cho mọi
    bộ ba và `None` cho mọi thứ khác, rồi vòng lặp OID `continue` khi gặp `None` — tức một mục
    `ANH_CHUP_DONG_CUNG` lỡ bị sửa thành `(số, lý do)` thì phép ghim blob TẮT IM LẶNG. Đo được
    ở vòng 13: thay một mục thật như thế ⇒ `quet()` ra `rc=0 DAT`, `lech_oid_dong_cung` RỖNG,
    và tệp "đông cứng" đổi được nội dung miễn là giữ số lời gọi. Lời khai "không được sửa một
    byte" lại rộng hơn phép đo — N6, lần nữa.
    """
    if isinstance(muc, (tuple, list)) and len(muc) == 3 \
            and isinstance(muc[1], str) and re.fullmatch(r"[0-9a-f]{40}", muc[1]):
        return muc[1]
    return None


# `_la_hang_bash` ĐÃ GỠ Ở r17 — nó thành MÃ CHẾT sau N52. Bộ tính hằng làm đúng việc ấy
# rộng hơn, nên hàm cũ không còn người gọi. Đo được lý do phải gỡ chứ không phải để đó:
# hai đột biến `bn_ten_phan_biet_hoa_thuong` và `bn_bo_hang_byte` neo vào nó và SỐNG SÓT —
# một đột biến trên mã chết không đo được gì, và nó làm bảng thống kê nói dối. Hai đột biến
# ấy nay neo vào `_ten_tu_gia_tri`/`_la_ten_bash`, nơi luật THẬT sống.

_KHONG_BIET = object()          # "không rút gọn được" — KHÁC với "rút gọn ra None"

_TEN_DUNG_DUONG = {"Path", "PurePath", "PosixPath", "WindowsPath",
                   "PurePosixPath", "PureWindowsPath"}


def _gia_tri_hang(nut, tra_ten=None, sau=0):
    """GIÁ TRỊ mà một biểu thức hằng đặt ra, hay `_KHONG_BIET` (N52, r17).

    VÌ SAO ĐỔI KIẾN TRÚC Ở ĐÂY. Bốn revision liền trước vá lớp này bằng cách THÊM MỘT HÌNH
    DẠNG vào bảng liệt kê: `casefold` (r7) → hằng byte (r11) → đuôi `.pyw` (r12) → `pathlib`
    và hai helper shell (r16). Vòng 10 rồi vòng 11 vẫn ra hình dạng mới — `Path("", "bash")`,
    `Path(".", "bash")`, `{"bash"}` — và mỗi cái đều CHẠY BASH THẬT (đo được: `Path("","bash")`
    in ra `OK`; `run({"bash"})` thoát `rc=0`). Đó đúng là thứ `CLAUDE.md` gọi tên: **danh sách
    CẤM không bao giờ đủ**. Nên ta thôi hỏi *"biểu thức này viết theo hình dạng nào"* và hỏi
    *"biểu thức này RÚT GỌN RA GIÁ TRỊ GÌ"* — rồi mới hỏi giá trị ấy có phải tên `bash`.

    ĐO ĐƯỢC trên 20 hình dạng, trước khi chọn: luật liệt kê r16 sai **5/20**, bộ tính hằng sai
    **1/20**. Chủ kho chọn phương án này sau khi đọc phép đo.

    PHỦ: hằng `str`/`bytes`/số, list/tuple/set/dict lồng nhau, nối chuỗi liền kề, phép `+`
    trên hằng chuỗi hoặc byte, và **hàm dựng `pathlib`** khi callee giải được về `pathlib`
    thật. `sau` chặn đệ quy sâu vô hạn trên biểu thức lồng.

    KHÔNG PHỦ, và đây là **nợ có tên** chứ không phải chỗ đã kín: mọi thứ đi qua BIẾN, qua
    `os.fspath`, qua `getattr`, hay qua một hàm do người dùng viết. Rút gọn hằng không phải
    phân tích luồng dữ liệu.
    """
    if sau > 8:
        return _KHONG_BIET
    try:
        return ast.literal_eval(nut)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        pass
    if isinstance(nut, ast.BinOp) and isinstance(nut.op, ast.Add):
        t = _gia_tri_hang(nut.left, tra_ten, sau + 1)
        ph = _gia_tri_hang(nut.right, tra_ten, sau + 1)
        if isinstance(t, str) and isinstance(ph, str):
            return t + ph
        if isinstance(t, bytes) and isinstance(ph, bytes):
            return t + ph
        return _KHONG_BIET
    # N65 (r19) — BỐN TOÁN TỬ GIỮ HẰNG NỮA. Vòng 13 đo được `f"bash"`, `"%s" % "bash"`,
    # `"".join(["ba", "sh"])`, `"hsab"[::-1]` — cả bốn CHẠY BASH THẬT (in ra `OK`) mà r18 trả
    # `[]`. Cả bốn là phép trên HẰNG của kiểu dựng sẵn, nên KHÔNG che được và không cần giải
    # tên. Phép THẬT được gọi trên giá trị đã gấp; không mô phỏng.
    # NÓI THẲNG, lần thứ hai: đây vẫn là một TẬP TOÁN TỬ liệt kê, và nó KHÔNG đóng.
    if isinstance(nut, ast.JoinedStr):
        # CHỈ f-string không có biểu thức nào: `f"bash"`. Có `{x}` thì giá trị phụ thuộc
        # luồng dữ liệu — nợ có tên, không đoán.
        if all(isinstance(x, ast.Constant) and isinstance(x.value, str) for x in nut.values):
            return "".join(x.value for x in nut.values)
        return _KHONG_BIET
    if isinstance(nut, ast.BinOp) and isinstance(nut.op, ast.Mod):
        t = _gia_tri_hang(nut.left, tra_ten, sau + 1)
        ph = _gia_tri_hang(nut.right, tra_ten, sau + 1)
        if isinstance(t, (str, bytes)) and ph is not _KHONG_BIET \
                and isinstance(ph, (str, bytes, int, float, tuple)):
            try:
                return t % ph
            except (TypeError, ValueError, KeyError):
                return _KHONG_BIET
        return _KHONG_BIET
    if isinstance(nut, ast.Subscript):
        goc = _gia_tri_hang(nut.value, tra_ten, sau + 1)
        chi = nut.slice
        if isinstance(goc, (str, bytes)):
            try:
                if isinstance(chi, ast.Slice):
                    phan = [None if x is None else _gia_tri_hang(x, tra_ten, sau + 1)
                            for x in (chi.lower, chi.upper, chi.step)]
                    if all(x is None or type(x) is int for x in phan):
                        return goc[slice(*phan)]
                    return _KHONG_BIET
                k = _gia_tri_hang(chi, tra_ten, sau + 1)
                if type(k) is int:
                    return goc[k]
            except (IndexError, ValueError):
                return _KHONG_BIET
        return _KHONG_BIET
    # KHÔNG có nhánh cho bao chứa: `ast.literal_eval` đã phủ bao chứa HẰNG, còn bao chứa
    # mà phần tử phải GẤP thì `_la_vec_bash` đã mở theo CÚ PHÁP trước khi tới đây. Bản đầu
    # của r17 có nhánh ấy và đột biến `bn_khong_rut_gon_bao_chua` SỐNG SÓT — dấu hiệu đo
    # được của mã không đường nào đi tới. Gỡ, thay vì giữ một nhánh không ai kiểm được.
    if isinstance(nut, ast.Call):
        boc = _gap_vo_boc(nut, tra_ten, sau)
        if boc is not _KHONG_BIET:
            return boc
    if isinstance(nut, ast.Call) and tra_ten is not None:
        if not _la_dung_duong(nut.func, tra_ten) or nut.keywords:
            return _KHONG_BIET
        phan = [_gia_tri_hang(a, tra_ten, sau + 1) for a in nut.args]
        if not phan or not all(isinstance(x, str) for x in phan):
            return _KHONG_BIET
        try:
            # DÙNG `PurePosixPath` CHO MỌI HÀM DỰNG, có chủ đích: ta chỉ CHẤP NHẬN kết quả
            # khi nó đúng bằng `bash`/`bash.exe`, mà cả hai đều không chứa dấu phân cách —
            # nên khác biệt POSIX/Windows không đổi được phán quyết, còn dùng một lớp cố
            # định thì phép đo không phụ thuộc nền đang chạy.
            return str(PurePosixPath(*phan))
        except (ValueError, TypeError):
            return _KHONG_BIET
    return _KHONG_BIET


def _gap_vo_boc(nut, tra_ten, sau):
    """Gấp một VỎ BỌC GIỮ HẰNG quanh một giá trị hằng, hay `_KHONG_BIET` (N58, r18).

    Vòng 12 đo được bốn cách viết CHẠY BASH THẬT mà N52 trả `[]`: `"bash".encode()`,
    `str(Path("bash"))`, `os.fspath(Path("bash"))`, `bytes("bash", "ascii")`. Cùng một tên,
    thêm một lớp gọi hàm THUẦN quanh nó.
    TẬP ĐƯỢC GẤP, và vì sao dừng ở đó:
      · `.encode()` / `.decode()` trên một hằng — KHÔNG che được (không ai gán lại được
        phương thức của `str`/`bytes`), nên không cần giải tên;
      · `str(…)` / `bytes(…)` — là TÊN DỰNG SẴN, nên CHE ĐƯỢC. Chỉ gấp khi tên ấy KHÔNG có
        ràng buộc nào trong chuỗi phạm vi; có thì coi như hàm người dùng, không gấp;
      · `os.fspath` / `os.fsencode` / `os.fsdecode` — chỉ khi callee GIẢI được về `os` thật.
    Hàm THẬT được gọi trên giá trị ĐÃ GẤP, không mô phỏng: `str(b"bash")` ra `"b'bash'"` như
    Python làm, và vì thế KHÔNG bị nhận nhầm là tên `bash`.
    NÓI THẲNG: đây vẫn là một TẬP TOÁN TỬ liệt kê — nhỏ hơn tập hình dạng r16 nhiều, nhưng
    KHÔNG đóng. Thứ đóng được cửa là phân tích luồng dữ liệu, và nó vẫn là nợ có tên.
    """
    f = nut.func
    try:
        if (isinstance(f, ast.Attribute) and f.attr == "join" and not nut.keywords
                and len(nut.args) == 1):
            # N65 (r19) — `"".join([...])` trên một HẰNG phân cách. Không che được.
            sep = _gia_tri_hang(f.value, tra_ten, sau + 1)
            if isinstance(nut.args[0], (ast.List, ast.Tuple)):
                phan = [_gia_tri_hang(a, tra_ten, sau + 1) for a in nut.args[0].elts]
            else:
                phan = _gia_tri_hang(nut.args[0], tra_ten, sau + 1)
            if isinstance(sep, (str, bytes)) and isinstance(phan, (list, tuple)) \
                    and all(type(x) is type(sep) for x in phan):
                return sep.join(phan)
            return _KHONG_BIET
        if (isinstance(f, ast.Attribute) and f.attr in ("encode", "decode")
                and not nut.keywords and len(nut.args) <= 2):
            goc = _gia_tri_hang(f.value, tra_ten, sau + 1)
            doi = [_gia_tri_hang(a, tra_ten, sau + 1) for a in nut.args]
            if (isinstance(goc, str if f.attr == "encode" else bytes)
                    and all(isinstance(x, str) for x in doi)):
                return getattr(goc, f.attr)(*doi)
            return _KHONG_BIET
        if (isinstance(f, ast.Name) and f.id in ("str", "bytes") and not nut.keywords
                and 1 <= len(nut.args) <= 3 and tra_ten is not None
                and not tra_ten(f.id, hoi_rang_buoc=True)):
            doi = [_gia_tri_hang(a, tra_ten, sau + 1) for a in nut.args]
            if all(isinstance(x, (str, bytes)) for x in doi):
                return (str if f.id == "str" else bytes)(*doi)
            return _KHONG_BIET
        if tra_ten is not None and len(nut.args) == 1 and not nut.keywords:
            ten = None
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                muc = tra_ten(f.value.id)
                if muc and muc[0] == "os" and muc[1] is None and f.attr in _BOC_OS:
                    ten = f.attr
            elif isinstance(f, ast.Name):
                muc = tra_ten(f.id)
                if muc and muc[0] == "os" and muc[1] in _BOC_OS:
                    ten = muc[1]
            if ten is not None:
                v = _gia_tri_hang(nut.args[0], tra_ten, sau + 1)
                if isinstance(v, (str, bytes)):
                    return getattr(os, ten)(v)
                return _KHONG_BIET
    except (TypeError, ValueError, UnicodeError, LookupError):
        return _KHONG_BIET
    return _KHONG_BIET


def _la_dung_duong(f, tra_ten):
    """Callee này có phải một hàm dựng đường của `pathlib` THẬT không."""
    if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
        muc = tra_ten(f.value.id)
        return bool(muc) and muc[1] is None and muc[0] == "pathlib" \
            and f.attr in _TEN_DUNG_DUONG
    if isinstance(f, ast.Name):
        muc = tra_ten(f.id)
        return bool(muc) and muc[0] == "pathlib" and muc[1] in _TEN_DUNG_DUONG
    return False


def _ten_tu_gia_tri(v):
    """TÊN chương trình mà một giá trị đặt ra, hay None. KHÔNG mở bao chứa."""
    if isinstance(v, bytes):
        # CHỈ ASCII: không giải mã bừa byte ngoài ASCII — một tên chương trình thật thì ASCII.
        try:
            v = v.decode("ascii")
        except UnicodeDecodeError:
            return None
    return v if isinstance(v, str) else None


def _ten_trong_vec(v):
    """TÊN chương trình mà một `argv` đặt ra: phần tử đầu của bao chứa, hay chính chuỗi trần.

    TẬP HỢP MỘT PHẦN TỬ được tính — `subprocess.run({"bash"})` CHẠY bash thật (đo được:
    `rc=0`). Tập NHIỀU phần tử thì KHÔNG: thứ tự duyệt của `set` không xác định nên không
    biết phần tử nào là chương trình, và đoán bừa là bắt oan.
    """
    if isinstance(v, (list, tuple)):
        v = v[0] if v else None
    elif isinstance(v, dict):
        # N58 (r18) — Python duyệt `dict` theo KHOÁ, và thứ tự khoá là XÁC ĐỊNH (thứ tự
        # chèn). Đo được: `subprocess.run({"bash": None, "-c": None, "echo OK": None})` in ra
        # `OK`. Khác `set`: ở đó thứ tự KHÔNG xác định nên chỉ tập MỘT phần tử mới tính.
        v = next(iter(v)) if v else None
    elif isinstance(v, (set, frozenset)):
        v = next(iter(v)) if len(v) == 1 else None
    return _ten_tu_gia_tri(v)


def _la_ten_bash(nut, tra_ten, cho_duong=True, nhan=None):
    """Nút này có đặt ra TÊN chương trình `bash` không.

    `cho_duong=False` cho hai helper chạy qua shell: `Popen(..., shell=True)` **TỪ CHỐI** đối
    số path-like (đo được: `subprocess.getoutput(Path("bash"))` ném
    `TypeError: path-like args is not allowed when shell is true`). Bản r16 báo `[(3, 0)]` cho
    lời gọi ấy — một BÁO ĐỘNG GIẢ do chính bản vá r16 đẻ ra, và *"một cổng bắt oan là cổng sẽ
    bị tắt"*. Nên ở nhánh ấy chỉ hằng `str`/`bytes` mới tính.
    """
    if nut is None:
        return False
    # `nhan` (N59, r18): KIỂU mà API này thật sự nhận, đo riêng từng API. `cho_duong=False`
    # là cách viết cũ của "không nhận path-like", giữ cho hai helper shell của r16/r17.
    if nhan is None:
        nhan = (_S, _B, _P) if cho_duong else (_S, _B)
    if _P not in nhan and isinstance(nut, ast.Call) and tra_ten is not None \
            and _la_dung_duong(nut.func, tra_ten):
        return False
    # GIẢI TÊN ở mọi nhánh, kể cả nhánh không nhận path-like: `os.popen(os.fspath(Path(
    # "bash")))` đưa vào một `str` và CHẠY bash. Thứ bị loại là một ĐỐI TƯỢNG path ở ngọn,
    # không phải mọi phép gấp có `pathlib` bên trong — chốt ngay trên làm đúng việc ấy.
    v = _gia_tri_hang(nut, tra_ten)
    if v is _KHONG_BIET:
        return False
    if isinstance(v, bytes) and _B not in nhan:
        return False
    ten = _ten_tu_gia_tri(v)
    return ten is not None and ten.casefold() in _HANG_BASH


def _la_vec_bash(nut, tra_ten):
    """`argv` này có đặt ra TÊN chương trình `bash` ở vị trí đầu không.

    MỞ BAO CHỨA THEO CÚ PHÁP TRƯỚC, rút gọn sau — và đây là một phép đo, không phải một
    lựa chọn phong cách. Bản đầu của N52 rút gọn CẢ vector, nên
    `subprocess.run(["bash", "-c", kich])` — phần tử sau là một BIẾN — không rút gọn được và
    **LỌT**. Chính cổng trên cây thật bắt: `.claude/dev/launcher_test.py` khai 7 mà đo được 6,
    dòng mất là `(3101, 16)`. Chỉ phần tử ĐẦU mới quyết chương trình nào chạy; các phần tử
    sau là đối số và chúng KHÔNG cần là hằng.
    """
    if nut is None:
        return False
    if isinstance(nut, (ast.List, ast.Tuple)):
        return bool(nut.elts) and _la_ten_bash(nut.elts[0], tra_ten)
    if isinstance(nut, ast.Set):
        # Tập NHIỀU phần tử: thứ tự duyệt không xác định ⇒ không biết cái nào là chương trình.
        return len(nut.elts) == 1 and _la_ten_bash(nut.elts[0], tra_ten)
    if isinstance(nut, ast.Dict):
        # Khoá đầu TIÊN. Khoá `None` là một `**x` trải ra — không biết nó mang gì, không đoán.
        return bool(nut.keys) and nut.keys[0] is not None \
            and _la_ten_bash(nut.keys[0], tra_ten)
    v = _gia_tri_hang(nut, tra_ten)          # `run("bash")` — chuỗi trần cũng phóng theo TÊN
    if v is _KHONG_BIET:
        return False
    ten = _ten_trong_vec(v)
    return ten is not None and ten.casefold() in _HANG_BASH


def _doi_so_thu(nut, vt, khoa):
    """Đối số ở VỊ TRÍ `vt`, hay đối số từ khoá `khoa`. Có `*` trải trước vị trí ấy thì
    không đoán — trả None (không bắt), đúng kỷ luật `_doi_so_executable`."""
    if len(nut.args) > vt and not any(isinstance(a, ast.Starred) for a in nut.args[:vt + 1]):
        return nut.args[vt]
    for k in nut.keywords:
        if k.arg == khoa:
            return k.value
    return None


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


def _co_the_thanh_bash(nut, sau=0):
    """Cây con này CÓ THỂ rút gọn ra tên `bash` không — phép thử RẺ, cố ý RỘNG (N52, r17).

    KHÔNG rút gọn ở đây (rút gọn là phần đắt, dành cho `_loi_goi_tran`), chỉ hỏi hai câu:
    có một hằng mang tên `bash` ở đâu đó không, hay có một phép NỐI hằng chuỗi — thứ có thể
    ghép `"ba" + "sh"` thành tên ấy. Bộ lọc hẹp hơn luật thật là một lỗi LỌT IM LẶNG: luật
    thật sẽ không bao giờ được hỏi.
    """
    if sau > 8 or nut is None:
        return False
    if isinstance(nut, ast.Constant):
        v = nut.value
        if isinstance(v, bytes):
            try:
                v = v.decode("ascii")
            except UnicodeDecodeError:
                return False
        return isinstance(v, str) and v.casefold() in _HANG_BASH
    if isinstance(nut, ast.BinOp) and isinstance(nut.op, ast.Add):
        return True                    # phép nối hằng: để luật thật quyết
    if isinstance(nut, ast.BinOp) and isinstance(nut.op, ast.Mod):
        return True                    # N65: `"%s" % "bash"`
    if isinstance(nut, (ast.JoinedStr, ast.Subscript)):
        return True                    # N65: `f"bash"`, `"hsab"[::-1]` — để luật thật quyết
    if isinstance(nut, ast.Call) and isinstance(nut.func, ast.Attribute) \
            and nut.func.attr == "join":
        # N65: `"".join(["ba", "sh"])` — không mảnh nào là hằng `bash`, nên nếu chỉ hỏi "có
        # hằng `bash` không" thì bộ lọc loại nó TRƯỚC khi luật thật được hỏi. Đo được ở bản
        # đầu của r19: đúng hình dạng này lọt trong khi ba toán tử kia bị bắt.
        return True
    if isinstance(nut, (ast.List, ast.Tuple, ast.Set, ast.Dict, ast.Call, ast.Attribute)):
        # `Dict` cho argv kiểu từ điển, `Attribute` cho `"bash".encode()` (N58, r18).
        return any(_co_the_thanh_bash(x, sau + 1) for x in ast.iter_child_nodes(nut))
    return False


def _mang_hang_bash(nut):
    """Lời gọi có thể mang tên `bash` ở ĐỐI SỐ NÀO ĐÓ không — bộ lọc RẺ, cố ý RỘNG hơn luật
    thật (mọi vị trí, mọi từ khoá); quyết định đúng nằm ở `_loi_goi_tran`. Sai chiều rộng thì
    chỉ tốn công giải callee thừa; sai chiều hẹp mới là lọt."""
    return any(_co_the_thanh_bash(a)
               for a in (*nut.args, *(kw.value for kw in nut.keywords)))


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
      · `subprocess.getoutput` / `getstatusoutput` mà `cmd` là hằng `bash` — chúng chạy
        lệnh QUA SHELL và phóng bash thật (N45, r16). Chữ ký khác `Popen`: một đối số, đến
        bằng VỊ TRÍ hay `cmd=`, và KHÔNG có `executable`;
      · đối số được **RÚT GỌN VỀ GIÁ TRỊ** rồi mới hỏi (N52, r17), nên mọi cách VIẾT ra
        cùng một tên đều bị bắt: hằng `str`/`bytes`, `Path("bash")`,
        `Path("", "bash")`, `Path(".", "bash")`, `PurePath("bash.exe")`, tập hợp MỘT
        phần tử `{"bash"}`, và phép nối hằng `"ba" + "sh"`. Cả ba chỗ — `which`,
        `argv[0]`, `executable=` — dùng chung phép rút gọn ấy;
      · CHÍN API phóng theo TÊN ngoài `subprocess`/`shutil` (N59, r18): `os.execvp`/
        `execvpe`/`execlp`/`execlpe`, `os.posix_spawnp`, `os.spawnlp`/`spawnlpe`/`spawnvp`/
        `spawnvpe` (tên ở vị trí THỨ HAI, sau chế độ), `os.system`, `os.popen`,
        `asyncio.create_subprocess_exec`/`_shell`. Từ r8 chúng là NỢ CÓ TÊN; cả chín đo được
        là CHẠY BASH THẬT. KIỂU được nhận đo RIÊNG từng API (bảng `_API_THEO_TEN`);
      · `dict` làm argv — KHOÁ ĐẦU TIÊN, vì thứ tự khoá xác định — và VỎ BỌC GIỮ HẰNG:
        `"bash".encode()`, `str(…)`/`bytes(…)` khi tên dựng sẵn không bị che, `os.fspath`/
        `fsencode`/`fsdecode` khi callee giải về `os` thật (N58, r18);
      · bộ tính hằng gấp thêm f-string KHÔNG biểu thức, `%` trên hằng, `"sep".join([...])`, cắt
        lát và chỉ số trên hằng (N65, r19); và `pty.spawn(argv)` — kể cả chuỗi trần — là lời
        phóng kiểu argv (N66, r19);
      · CHÚ THÍCH không được tính thì KHÔNG bị quét (N68, r19): có `from __future__ import
        annotations`, hoặc chú thích biến CỤC BỘ trong hàm (không bao giờ tính, PEP 526). Giá
        trị mặc định, decorator, cơ sở lớp thì vẫn quét — chúng chạy lúc định nghĩa;
      · nhưng HAI HELPER SHELL thì KHÔNG nhận path-like: `Popen(..., shell=True)` **từ
        chối** đối số đường dẫn (đo được: `TypeError`), nên `getoutput(Path("bash"))`
        là một BÁO ĐỘNG GIẢ và không được bắt;
      · MODULE và THÂN LỚP tra tên theo THỨ TỰ THỰC THI (N46 r16, N53 r17): ràng buộc
        **HOÀN TẤT MUỘN NHẤT** trước lời gọi là ràng buộc đang có hiệu lực, và một ràng
        buộc chỉ hoàn tất SAU khi vế phải / giá trị mặc định / decorator / cơ sở lớp của nó
        tính xong. Nên `subprocess = object()` · `import subprocess` · `run(["bash"])` bị
        bắt, và `subprocess = subprocess.run(["bash"])` cũng vậy. Phạm vi HÀM trực tiếp
        chứa lời gọi CŨNG theo thứ tự thực thi (N67, r19 — đổi ngược doctrine r8), chỉ khác
        một điều: chưa có lần ghi cục bộ nào hoàn tất thì đó là `UnboundLocalError`, KHÔNG
        đọc sang phạm vi ngoài;
      · `type X[T] = …` (PEP 695) có phạm vi chú thích RIÊNG (N47, r16): `T` của nó không rò
        ra phạm vi chứa;
      · callee giải theo PHẠM VI TỪ VỰNG (r8, F3 codex vòng 3): `import subprocess` ở module
        rồi gọi trong hàm ⇒ bắt; `import` nằm trong hàm A thì hàm B KHÔNG thấy; tên bị THAM
        SỐ hay PHÉP GÁN che ở phạm vi gần nhất ⇒ không còn là stdlib ⇒ không bắt. Bản trước
        `ast.walk` mọi `import` của tệp vào MỘT bảng, đo được: `def a(): import subprocess`
        + `def b(subprocess): subprocess.run(["bash"])` ⇒ `[(5, 4)]`, phải là `[]`.

    **KHÔNG PHỦ**, và khai thẳng ra đây thay vì để người đọc tưởng đã kín:
      · mọi thứ đi qua BIẾN, qua `os.fspath`, qua `getattr`, hay qua một hàm người dùng
        viết — rút gọn HẰNG không phải phân tích luồng dữ liệu;
      · tập hợp NHIỀU phần tử — thứ tự duyệt không xác định nên không biết phần tử nào là
        chương trình;
      · chuỗi lệnh NHIỀU TỪ (`run("bash -c ...", shell=True)`, `getoutput("bash -c x")`) —
        chỉ chuỗi trần đúng một tên `bash` được phủ; tách một dòng lệnh shell là bài toán
        KHÁC (trích dẫn, thoát ký tự), và ở đây không đo được cái nào nên không viết bừa;
      · biến thể KHÔNG `p` — `os.execv`, `os.posix_spawn`, `os.spawnv*` — vì chúng KHÔNG tìm
        theo PATH (đo được: `execv("bash", …)` ném `FileNotFoundError`), nên `"bash"` ở đó là
        `./bash`, không phải khuyết tật packet này chặn;
      · tên `bash` đi qua BIẾN TRUNG GIAN, nối chuỗi, danh sách dựng nơi khác, hay một
        `executable=` KHÔNG phải hằng;
      · `from shutil import *`, tên đến qua `globals()`/`getattr`.
    Các nhóm ấy cần phân tích luồng dữ liệu, không phải khớp cây cú pháp. Chúng là **nợ có
    tên**, không phải chỗ đã kín. Ai mở rộng thì thêm hình dạng vào `t33` TRƯỚC.
    Mọi phạm vi đều giải theo THỨ TỰ THỰC THI (N46/N53/N67) — xem `_giai_ten`. Ở HÀM, tên
    cục bộ chưa có lần ghi nào hoàn tất là `UnboundLocalError`, không rơi ra ngoài. Hai chỗ
    vẫn lệch đã khai ở đó: nhánh `if` không chạy (rơi về phía thận trọng), và `global` ghi từ
    một hàm định nghĩa sau nhưng gọi trước. Hàm BAO NGOÀI một hàm lồng không lọc theo vị trí.
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
        if tra_ten is None:
            continue                       # N68: nằm trong một chú thích KHÔNG được tính
        loai = _loai_loi_goi(nut, tra_ten)
        if loai is None:
            continue
        if loai == "which":
            dau = _doi_so_dau(nut, _KHOA_WHICH)
            dinh = _la_ten_bash(dau, tra_ten)
        elif loai.startswith("argv:"):
            mod, _, ham = loai[5:].partition(".")
            vt, kw = _API_ARGV[(mod, ham)]
            dinh = _la_vec_bash(_doi_so_thu(nut, vt, kw), tra_ten)
        elif loai.startswith("api:"):
            mod, _, ham = loai[4:].partition(".")
            vt, kw, nhan = _API_THEO_TEN[(mod, ham)]
            dinh = _la_ten_bash(_doi_so_thu(nut, vt, kw), tra_ten, nhan=nhan)
        elif loai == "shell_ra":
            # `getoutput(cmd)` / `getstatusoutput(cmd)`: MOT doi so, chay qua shell, KHONG
            # co `executable`. Ap luat vi tri thu ba cua `Popen` vao day la doc sai chu ky.
            dau = _doi_so_dau(nut, _KHOA_SHELL_RA)
            dinh = _la_ten_bash(dau, tra_ten, cho_duong=False)
        else:
            exe = _doi_so_executable(nut)
            if exe is None:
                dinh = _la_vec_bash(_doi_so_dau(nut, _KHOA_SPAWN), tra_ten)
            else:
                # `executable=` GHI ĐÈ, không cộng thêm: `args[0]` khi ấy chỉ còn là
                # `argv[0]` trang trí. Một lời gọi là MỘT bản ghi dù cả hai cùng tên `bash`.
                dinh = _la_ten_bash(exe, tra_ten)
        if dinh:
            ban_ghi.append((nut.lineno, nut.col_offset))
    # MỘT BẢN GHI CHO MỖI `ast.Call`, không phải cho mỗi DÒNG. Tập dòng cũ gộp hai lời gọi
    # trên cùng một dòng thành một — đo được: `(which("bash"), which("bash"))` ra `[2]`.
    return sorted(set(ban_ghi))


# Nhận diện theo TÊN mà không giải được CALLEE thì sai CẢ HAI HƯỚNG — đo được cả hai:
#   lọt:     `subprocess.run(["x"], executable="bash")`  ⇒ `[]`
#   bắt oan: `runner.run(["bash"])`, `matcher.which("bash")` ⇒ `[2]`
# Nên phải biết cái tên ấy có THẬT SỰ trỏ vào `subprocess`/`shutil` hay không.
_MODULE_CHU = {"subprocess": _TEN_SPAWN + _TEN_SHELL_RA, "shutil": _TEN_WHICH,
               # `pathlib` CO MAT de GIAI TEN `Path`, khong phai de phan loai loi goi:
               # `_LOAI_THEO_TEN.get()` tra None cho chung nen `Path(...)` khong bao gio
               # bi tinh la mot lan phong tien trinh.
               "pathlib": _TEN_DUONG_PATHLIB,
               # N58/N59 (r18) — `os`/`asyncio` CÓ MẶT vì hai lý do khác nhau: các API ở
               # `_API_THEO_TEN` là lời PHÓNG; `_BOC_OS` chỉ là VỎ BỌC để bộ tính hằng gấp.
               "os": tuple(t for (m, t) in _API_THEO_TEN if m == "os") + _BOC_OS,
               "asyncio": tuple(t for (m, t) in _API_THEO_TEN if m == "asyncio"),
               "pty": tuple(t for (m, t) in _API_ARGV if m == "pty")}


# Các nút MỞ PHẠM VI TỪ VỰNG mới (luật Python 3): hàm, lambda, lớp, và bốn loại comprehension.
# N47 (r16) — `type X[T] = ...` (PEP 695) MO MOT PHAM VI CHU THICH RIENG. Ban r15 chi
# ghi TEN alias vao pham vi chua roi duyet tiep XUONG, nen `T` cua alias RO RI ra ngoai.
# Do duoc tren Python 3.12.3 THAT, truoc va:
#   `import subprocess` + `type X[subprocess] = int` + `subprocess.run(["bash"])` => []
# — mot lan phong bash THAT bi mot tham so kieu o dong tren nuot mat. `getattr` vi 3.11
# khong co `ast.TypeAlias`; o do `type X = ...` con la SyntaxError nen khong the co nut nay.
_NUT_PHAM_VI = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef,
                ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp) + tuple(
    x for x in (getattr(ast, "TypeAlias", None),) if x is not None)


def _truong_luc_dinh_nghia(con):
    """Các nút được TÍNH ở phạm vi CHỨA khi định nghĩa `con` — decorator, giá trị mặc định,
    chú thích, cơ sở lớp, và **tham số kiểu PEP 695** (N41). Không gồm THÂN."""
    import ast
    ra = list(getattr(con, "type_params", ()) or ())
    ra += list(getattr(con, "decorator_list", ()) or ())
    a = getattr(con, "args", None)
    if a is not None:
        ra += [*a.defaults, *[x for x in a.kw_defaults if x is not None]]
        ra += [x.annotation for x in (*a.posonlyargs, *a.args, *a.kwonlyargs, a.vararg, a.kwarg)
               if x is not None and x.annotation is not None]
    if getattr(con, "returns", None) is not None:
        ra.append(con.returns)
    ra += list(getattr(con, "bases", ()) or ())
    ra += [k.value for k in (getattr(con, "keywords", ()) or ())]
    return ra


def _dich_walrus_trong(nut):
    """Tên bị `:=` ràng buộc bên trong `nut`, không xuống hàm/lambda/lớp lồng."""
    import ast
    ra, chong = [], [nut]
    while chong:
        n = chong.pop()
        if n is not nut and isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef,
                                           ast.Lambda, ast.ClassDef)):
            continue
        if isinstance(n, ast.NamedExpr) and isinstance(n.target, ast.Name):
            ra.append(n.target.id)
        chong.extend(ast.iter_child_nodes(n))
    return ra


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


def _ket_nut(nut):
    """(dòng, cột) NGAY SAU một nút — nơi giá trị của nó đã tính xong."""
    return (getattr(nut, "end_lineno", None) or getattr(nut, "lineno", 0),
            getattr(nut, "end_col_offset", None) or getattr(nut, "col_offset", 0))


def _vi_tri_hoan_tat(n, mac_dinh):
    """Vị trí mà một ràng buộc sinh trong câu lệnh `n` THỰC SỰ có hiệu lực (N53, r17).

    Python ràng buộc tên SAU khi vế phải đã tính xong, không phải ở chỗ cái tên được viết.
    Bản r16 neo vào vị trí của chính nút tên, nên hai ca sau đều LỌT — đo được cả hai, và cả
    hai CHẠY BASH THẬT:
        `import subprocess`  ·  `subprocess = subprocess.run(["bash"])`          ⇒ []
        `import subprocess`  ·  `def subprocess(x=subprocess.run(["bash"])): …`  ⇒ []
    Ở cả hai, lời gọi nằm trong chính biểu thức SINH RA ràng buộc, nên lúc nó chạy thì tên vẫn
    còn trỏ vào module. Neo theo điểm HOÀN TẤT làm cả lớp ấy chết theo cơ chế.
    """
    import ast
    if isinstance(n, (ast.Assign, ast.AugAssign)):
        return _ket_nut(n.value)
    if isinstance(n, ast.AnnAssign):
        return _ket_nut(n.value) if n.value is not None else _ket_nut(n)
    if isinstance(n, (ast.Import, ast.ImportFrom, ast.Delete)):
        return _ket_nut(n)
    if isinstance(n, (ast.For, ast.AsyncFor)):
        return _ket_nut(n.iter)
    if isinstance(n, (ast.With, ast.AsyncWith)):
        return _ket_nut(n.items[-1].context_expr) if n.items else _ket_nut(n)
    if isinstance(n, ast.ExceptHandler):
        return _ket_nut(n.type) if n.type is not None else _ket_nut(n)
    if isinstance(n, ast.NamedExpr):
        return _ket_nut(n.value)
    if isinstance(n, ast.stmt):
        # MẶC ĐỊNH CỦA MỘT CÂU LỆNH LÀ "CÂU LỆNH ĐÃ XONG", không phải giá trị thừa kế.
        # Đo được: thiếu nhánh này thì `type subprocess = int` và `:=` trong comprehension
        # ràng buộc ở vị trí `(0, 0)` — tức TRƯỚC cả `import` — nên phép che hợp lệ của chúng
        # bị bỏ qua và cổng BẮT OAN: `type subprocess = int` rồi `subprocess.run(["bash"])`
        # ra `[(3, 0)]` trên Python 3.12.3, mong `[]`.
        return _ket_nut(n)
    return mac_dinh


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
    # N46 (r16) — MOI rang buoc mang VI TRI `(dong, cot)` cua nut sinh ra no. Phep giai o
    # pham vi HAM khong dung toi no (luat ten cuc bo cua Python la LUC BIEN DICH, khong theo
    # dong chay), nhung MODULE va THAN LOP thi CO: xem `_giai_ten`.
    vi_tri = [(0, 0)]

    def them(ten, rb):   # noqa: D401
        if ten:
            bang.setdefault(ten, set()).add((rb, vi_tri[0]))

    if isinstance(pham_vi, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        a = pham_vi.args
        for x in (*a.posonlyargs, *a.args, *a.kwonlyargs, a.vararg, a.kwarg):
            if x is not None:
                them(x.arg, ("khac",))
    if type(pham_vi).__name__ == "TypeAlias":
        # Chi `type_params` va `value` thuoc pham vi alias; `name` rang buoc o pham vi CHUA.
        chong = [*getattr(pham_vi, "type_params", ()), pham_vi.value]
    else:
        chong = list(ast.iter_child_nodes(pham_vi))
    chong = [(x, (0, 0)) for x in chong]
    while chong:
        n, ht = chong.pop()
        ht = _vi_tri_hoan_tat(n, ht)
        vi_tri[0] = ht
        if isinstance(n, _NUT_PHAM_VI):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda,
                              ast.ClassDef)):
                if not isinstance(n, ast.Lambda):
                    # N53 (r17) — tên hàm/lớp chỉ CÓ HIỆU LỰC sau khi decorator, giá trị mặc
                    # định, chú thích và cơ sở lớp đã tính xong. Neo vào đầu THÂN chính là
                    # neo vào thời điểm ấy. Đo được: `def subprocess(x=subprocess.run(
                    # ["bash"]))` — bản r16 coi tên đã ràng buộc từ dòng `def` nên LỌT.
                    than_dau = n.body[0] if getattr(n, "body", None) else n
                    if isinstance(n, ast.ClassDef):
                        # N60 (r18) — THÂN LỚP CHẠY NGAY LÚC ĐỊNH NGHĨA, thân hàm thì không.
                        # Nên tên LỚP chỉ có hiệu lực sau khi CẢ thân đã chạy xong và
                        # decorator đã áp. Bản r17 neo cả hai vào dòng đầu thân — đúng cho
                        # hàm, SAI cho lớp. Đo được: `import subprocess` ·
                        # `class subprocess: x = 1; subprocess.run(["bash"])` — lời gọi trong
                        # thân lớp CHẠY BASH THẬT (in ra `OK`) mà r17 trả `[]`.
                        vi_tri[0] = _ket_nut(n)
                    else:
                        vi_tri[0] = (than_dau.lineno, than_dau.col_offset)
                    them(n.name, ("khac",))
                    vi_tri[0] = ht
                # N40 (r15) — `:=` trong TRƯỜNG LÚC ĐỊNH NGHĨA (mặc định, decorator, chú
                # thích, cơ sở lớp) ràng buộc ở phạm vi CHỨA, vì chính các trường ấy được
                # TÍNH ở phạm vi chứa (N37). Bản r13 bỏ qua cả nút nên mất ràng buộc ấy.
                # Đo được: `import subprocess`, `def f(x=(subprocess := runner)): pass`,
                # rồi `subprocess.run(["bash"])` ⇒ `[(4, 0)]` — BẮT OAN một phép che hợp lệ.
                # CHỈ trường lúc định nghĩa, KHÔNG xuống thân: `:=` trong thân là của thân.
                for x in _truong_luc_dinh_nghia(n):
                    for y in _dich_walrus_trong(x):
                        them(y, ("khac",))
            elif isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                # N29 (r11) — PEP 572: `:=` bên trong một comprehension ràng buộc ở phạm vi
                # CHỨA comprehension, không ở trong nó. Bản r10 `continue` thẳng nên ràng buộc
                # ấy biến mất; đo được: `import subprocess` rồi
                # `[(subprocess := runner) for _ in [0]]` thì lời gọi SAU đó vẫn bị báo `[(3,0)]`
                # — cổng CHẶN một phép che hợp lệ.
                for x in _dich_walrus(n):
                    them(x, ("khac",))
            elif type(n).__name__ == "TypeAlias":
                # N47 — CHI cai TEN tro ra ngoai; `type_params` o lai trong pham vi alias.
                them(getattr(getattr(n, "name", None), "id", None), ("khac",))
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
        elif type(n).__name__ in ("TypeVar", "ParamSpec", "TypeVarTuple"):
            # N41 — tên tham số kiểu CHE tên ngoài trong thân: `def f[subprocess]()` thì
            # `subprocess` trong thân là TypeVar, không phải module.
            them(getattr(n, "name", None), ("khac",))
        elif isinstance(n, ast.Global):
            toan_cuc.update(n.names)
        elif isinstance(n, ast.Nonlocal):
            phi_cuc_bo.update(n.names)
        elif type(n).__name__ in ("MatchAs", "MatchStar"):
            them(getattr(n, "name", None), ("khac",))
        elif type(n).__name__ == "MatchMapping":
            them(getattr(n, "rest", None), ("khac",))
        chong.extend((c, ht) for c in ast.iter_child_nodes(n))
    return bang, toan_cuc, phi_cuc_bo


def _loc_truoc(cac_rang_buoc, truoc):
    """Ràng buộc HOÀN TẤT MUỘN NHẤT mà vẫn trước `truoc`; `truoc is None` ⇒ lấy tất.

    N53 (r17) — "muộn nhất thắng", KHÔNG phải "đúng một cái". Bản r16 lọc theo vị trí rồi vẫn
    đòi tập còn lại có ĐÚNG MỘT phần tử, nên `subprocess = object()` · `import subprocess` ·
    `subprocess.run(["bash"])` cho hai ràng buộc cùng nằm trước lời gọi ⇒ mơ hồ ⇒ **LỌT**, dù
    lúc gọi thì `import` đã ghi đè phép gán. Ở module và thân lớp, không gian tên là thứ bị
    SỬA TUẦN TỰ: cái ghi sau cùng là cái đang có hiệu lực.
    Vẫn mơ hồ khi HAI ràng buộc hoàn tất ở CÙNG một vị trí (ví dụ `a = b = …`) — khi ấy tập
    trả về có nhiều hơn một phần tử và `_tra_import` từ chối, đúng phía thận trọng.
    """
    if truoc is None:
        return set(cac_rang_buoc)
    truoc_do = [x for x in cac_rang_buoc if x[1] < truoc]
    if not truoc_do:
        return set()
    dinh = max(x[1] for x in truoc_do)
    return {x for x in truoc_do if x[1] == dinh}


def _tra_import(cac_rang_buoc, truoc=None):
    """(module, hàm|None) khi tên bị ràng buộc ĐÚNG MỘT LẦN và là `import` theo dõi; None khi
    bị che, mơ hồ, hay trỏ vào thứ khác.

    `truoc` — vị trí `(dòng, cột)` của lời gọi. Chỉ phạm vi chạy theo THỨ TỰ CÂU LỆNH mới
    truyền nó vào (N46); `None` giữ nguyên ngữ nghĩa cũ "ràng buộc là thuộc tính của CẢ
    phạm vi", đúng luật tên cục bộ lúc biên dịch của hàm."""
    cac = _loc_truoc(cac_rang_buoc, truoc)
    if len(cac) == 1:
        ((rb, _vt),) = cac
        if rb[0] == "import":
            return rb[1], rb[2]
    return None


def _co_rang_buoc(ten, chuoi):
    """Tên này có ràng buộc NÀO trong chuỗi phạm vi nhìn thấy được không (N58, r18).

    KHÔNG xét vị trí, có chủ đích: câu hỏi là "có an toàn để coi đây là tên dựng sẵn không",
    và một ràng buộc ở BẤT KỲ đâu trong chuỗi là đủ để trả lời "không". Sai chiều ấy chỉ làm
    ta bỏ gấp một vỏ bọc — tức LỌT về phía đã khai là nợ, không bao giờ BẮT OAN.
    """
    n = len(chuoi)
    for i in range(n - 1, -1, -1):
        la_lop, bang, toan_cuc, phi_cuc_bo = chuoi[i]
        if la_lop and i != n - 1:
            continue
        if ten in bang or ten in toan_cuc or ten in phi_cuc_bo:
            return True
    return False


def _giai_ten(ten, chuoi, vi_tri=None):
    """Giải `ten` theo chuỗi phạm vi `chuoi` (ngoài → trong), luật Python: phạm vi gần nhất
    có ràng buộc thắng; thân LỚP không nhìn thấy được từ hàm lồng trong nó; `global` nhảy về
    module; `nonlocal` bỏ qua phạm vi hiện tại.

    N46 (r16) — MODULE và THÂN LỚP tra tên theo THỨ TỰ CÂU LỆNH, hàm thì không. Đây không
    phải một tinh chỉnh, nó là hai luật KHÁC NHAU của chính Python: trong một hàm, mọi phép
    gán trong thân làm cái tên thành cục bộ ngay từ lúc BIÊN DỊCH (nên `import` rồi gán lại ở
    dòng dưới là mơ hồ THẬT); ở module và thân lớp thì không có bước ấy, mỗi câu lệnh sửa
    không gian tên khi nó CHẠY. Đo được trên `8180970`:
        `import subprocess` · `subprocess.run(["bash"])` · `subprocess = runner`  ⇒  []
    — lời gọi ở dòng 2 CHẠY THẬT trên module đã `import`, phép gán dòng 3 chưa xảy ra. Thân
    lớp cùng bệnh. Chiều ngược (`gán TRƯỚC, gọi SAU`) vẫn phải ra `[]`, và vẫn ra.

    LỌC RỖNG KHÔNG PHẢI "KHÔNG TÌM THẤY": trong thân lớp, mọi ràng buộc nằm SAU lời gọi ⇒
    lúc ấy tên còn thuộc phạm vi BAO, nên phải đi tiếp ra ngoài chứ không trả None.

    KHAI THẲNG chỗ vẫn lệch: một phép gán nằm trước lời gọi nhưng nằm trong nhánh `if` KHÔNG
    chạy, hay một lời gọi trong vòng lặp mà vòng sau đã bị che — vị trí không nói được. Cả
    hai đều rơi về phía THẬN TRỌNG (coi là mơ hồ ⇒ không báo), trừ một chỗ: `global` ghi từ
    một hàm định nghĩa SAU lời gọi mà lại được gọi TRƯỚC. Đó là lối vào duy nhất còn báo oan
    được, và nó cần phân tích luồng gọi — **nợ có tên**, không phải chỗ đã kín.
    """
    n = len(chuoi)
    for i in range(n - 1, -1, -1):
        la_lop, bang, toan_cuc, phi_cuc_bo = chuoi[i]
        if la_lop and i != n - 1:
            continue
        # Module là `chuoi[0]`; thân lớp mang cờ `la_lop`. Cả hai chạy theo thứ tự câu lệnh.
        # N67 (r19) — VÀ PHẠM VI HÀM TRỰC TIẾP CHỨA LỜI GỌI CŨNG VẬY. ĐỔI NGƯỢC doctrine r8/N46,
        # và phải nói thẳng: r8 viết *"trong hàm, phép gán làm tên thành cục bộ ngay từ lúc biên
        # dịch, nên `import` rồi gán lại ở dòng dưới là mơ hồ THẬT"*. SAI. "Là cục bộ" chỉ quyết
        # một điều: đọc TRƯỚC lần ghi đầu tiên thì `UnboundLocalError`. Nó KHÔNG quyết giá trị
        # nào đang có lúc gọi — và giá trị ấy đi theo thứ tự thực thi, y như ở module. Đo được
        # trên Python 3.12.3 THẬT (CI ghim 3.12): `def f(): import subprocess;
        # subprocess.run(["bash", …]); subprocess = object()` IN RA `OK`, mà r18 trả `[]`.
        # CHỈ phạm vi TRỰC TIẾP chứa lời gọi (`i == n - 1`): một hàm BAO NGOÀI chạy lúc nào so
        # với hàm lồng thì vị trí cú pháp không nói được, nên ở đó vẫn không lọc.
        la_ham = i == n - 1 and i != 0 and not la_lop
        truoc = vi_tri if (vi_tri is not None and (la_lop or i == 0 or la_ham)) else None
        if ten in toan_cuc:
            # N39 (r15) — phạm vi KHAI `global x` mà TỰ NÓ ràng buộc `x` thì dùng ràng buộc
            # ẤY: bên trong hàm vừa `import subprocess`, cái tên là module, không mơ hồ.
            # Không có ràng buộc riêng (khai ĐỌC KHÔNG) thì mới về bảng module.
            # Đối xứng cả hai chiều: `global x; x = gia()` cho `("khac",)` ⇒ None ⇒ KHÔNG báo,
            # đúng, vì tên ấy đã bị che.
            if ten in bang and _loc_truoc(bang[ten], truoc):
                return _tra_import(bang[ten], truoc)
            # Bảng module KHÔNG lọc theo vị trí: lời gọi nằm trong một hàm, và hàm ấy chạy
            # lúc nào thì vị trí cú pháp không nói được. Không lọc = phía thận trọng.
            return _tra_import(chuoi[0][1].get(ten, ()))
        if ten in phi_cuc_bo:
            if ten in bang and _loc_truoc(bang[ten], truoc):
                return _tra_import(bang[ten], truoc)
            continue
        if ten in bang:
            if _loc_truoc(bang[ten], truoc):
                return _tra_import(bang[ten], truoc)
            if la_ham:
                # Tên là CỤC BỘ mà chưa có lần ghi nào hoàn tất trước lời gọi ⇒ Python ném
                # `UnboundLocalError`, KHÔNG đọc sang phạm vi ngoài. Khác hẳn module/thân lớp.
                return None
            continue                       # mọi ràng buộc còn ở PHÍA SAU ⇒ đi ra phạm vi bao
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
        # N39 (r15) — CHÉP, KHÔNG DỜI. Bản r13 `pop` ràng buộc khỏi phạm vi khai `global`,
        # nên bên TRONG chính hàm vừa `import`, cái tên ấy mất ràng buộc và bộ giải trả None.
        # Cross-review codex vòng 8 nêu lại đúng ca này, và họ ĐÚNG — phiên trước tôi lập luận
        # ngược lại rằng "tên bị ràng buộc hai lần nên mơ hồ là đúng", và lập luận ấy SAI:
        # sự mơ hồ nằm ở phạm vi MODULE, không nằm trong thân hàm đã tự `import`.
        # Đo được trên `f6189e3`: `subprocess = object()` ở module, rồi
        # `def f(): global subprocess; import subprocess; subprocess.run(["bash"])` ⇒ `[]`.
        # Chép thì: bảng của `f` giữ `("import", …)` ⇒ trong `f` BẮT; bảng module có cả
        # `("khac",)` lẫn `("import", …)` ⇒ ngoài module vẫn mơ hồ ⇒ KHÔNG bắt oan. Cả hai
        # chiều mà r11 đã vá vẫn giữ nguyên.
        for ten in toan_cuc:
            rb = rieng.get(ten)
            if rb:
                bang[goc][0].setdefault(ten, set()).update(rb)
        for ten in phi_cuc_bo:
            rb = rieng.get(ten)
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

    N37 (r13) — MÓN NỢ ẤY ĐÃ ĐẾN HẠN. Bản r12 khai thẳng chỗ bỏ qua: *"decorator / giá trị mặc
    định của một `def` lồng và `iter` đầu tiên của comprehension thật ra thuộc phạm vi NGOÀI…
    chưa có phép đo nào cần nó."* Cross-review codex vòng 7 đưa ra đúng phép đo ấy:
        `def f(shutil=shutil.which("bash"))` ⇒ `[]` — LỌT, dù định nghĩa `f` CÓ gọi bash.
    Python tính decorator, giá trị mặc định, chú thích, cơ sở lớp và `iter` ĐẦU TIÊN của
    comprehension ở phạm vi CHỨA, chỉ THÂN mới ở phạm vi mới. Nay duyệt đúng thế.
    Bốn hình dạng kia (`x=…`, `@…`, `x: …`, `class C(…)`) vốn ĐÃ bắt được vì tên không bị che;
    lệch chỉ lộ khi chính tham số che tên module — đúng ca codex dựng.
    """
    import ast
    ket = []
    bang_cua = _bang_pham_vi_ca_cay(cay)

    def pham_vi(nut):
        bang, toan_cuc, phi_cuc_bo = bang_cua[id(nut)]
        return (isinstance(nut, ast.ClassDef), bang, toan_cuc, phi_cuc_bo)

    # N68 (r19) — CHÚ THÍCH KHÔNG PHẢI LÚC NÀO CŨNG CHẠY. Đo trên Python 3.12.3 THẬT:
    #   · có `from __future__ import annotations` ⇒ chú thích tham số / trả về / biến được
    #     LƯU dạng chuỗi, không tính — `def f(x: subprocess.run(["bash"…]))` KHÔNG in gì;
    #   · chú thích biến CỤC BỘ trong hàm (`x: … = 1` trong thân) KHÔNG BAO GIỜ được tính, kể
    #     cả không có `__future__` (PEP 526; đo được: không in gì) — rộng hơn đề xuất vòng 13
    #     một bậc, và phép đo là lý do;
    #   · chú thích biến ở MODULE / THÂN LỚP mà không có `__future__` thì CÓ chạy (in ra).
    # Bản r18 quét mọi chú thích như lời gọi thật ⇒ BÁO OAN. Decorator, giá trị mặc định, cơ
    # sở lớp vẫn quét: chúng chạy lúc định nghĩa bất kể `__future__`.
    # CHƯA ĐO: Python 3.14 hoãn chú thích MẶC ĐỊNH (PEP 649); CI ghim 3.12 nên ở đây không đo.
    hoan_chu_thich = any(
        isinstance(n, ast.ImportFrom) and n.module == "__future__"
        and any(al.name == "annotations" for al in n.names) for n in cay.body)

    def _ngoai_va_trong(con):
        """(nút tính ở phạm vi NGOÀI, nút tính ở phạm vi TRONG) của một nút phạm vi."""
        if isinstance(con, (ast.FunctionDef, ast.AsyncFunctionDef)):
            a = con.args
            # N41 (r15) — PEP 695. Bản r13 KHÔNG duyệt `type_params`, nên một lời gọi ở
            # `bound` được `ast.walk` tìm thấy mà `tham` không thăm ⇒ `tra_theo_nut[id]`
            # ném **KeyError** và CLI thoát 1. Đo trên Python 3.12.3 THẬT (CI ghim 3.12):
            #   `def f[T: shutil.which("bash")](): pass`      ⇒ KeyError
            #   `class C[T: subprocess.run(["bash"])]: pass`  ⇒ KeyError
            #   `def f[subprocess](): subprocess.run(["bash"])` ⇒ [(3,4)] — BẮT OAN
            # `getattr` để mã vẫn chạy trên 3.11 (máy soạn bản vá) — ở đó nó là no-op.
            ngoai = [*getattr(con, "type_params", ()), *con.decorator_list, *a.defaults,
                     *[x for x in a.kw_defaults if x is not None],
                     *[x.annotation for x in (*a.posonlyargs, *a.args, *a.kwonlyargs,
                                              a.vararg, a.kwarg)
                       if x is not None and x.annotation is not None
                       and not hoan_chu_thich]]
            if con.returns is not None and not hoan_chu_thich:
                ngoai.append(con.returns)
            return ngoai, list(con.body)
        if isinstance(con, ast.Lambda):
            a = con.args
            return ([*a.defaults, *[x for x in a.kw_defaults if x is not None]], [con.body])
        if isinstance(con, ast.ClassDef):
            return ([*getattr(con, "type_params", ()), *con.decorator_list, *con.bases,
                     *[k.value for k in con.keywords]], list(con.body))
        if type(con).__name__ == "TypeAlias":
            # N47 — KHONG co gi tinh o pham vi ngoai: `name` chi la dich cua phep gan, con
            # `type_params` va `value` deu nam TRONG pham vi chu thich cua alias.
            return [], [*getattr(con, "type_params", ()), con.value]
        if isinstance(con, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            gen = con.generators
            if not gen:
                return [], list(ast.iter_child_nodes(con))
            trong = [x for x in ast.iter_child_nodes(con) if x is not gen[0]]
            return [gen[0].iter], trong + [gen[0].target, *gen[0].ifs]
        return [], list(ast.iter_child_nodes(con))

    def khong_chay(nut):
        """Ghi MỌI lời gọi trong `nut` là KHÔNG CHẠY (tra = None) — tường minh, không bỏ sót.

        Bỏ qua một cây con mà không ghi gì thì `_loi_goi_tran` lại gặp đúng `KeyError` của N41
        (lời gọi `ast.walk` thấy mà bộ duyệt không thăm). Ghi `None` giữ nguyên chốt ấy cho
        mọi nút KHÁC: nút thật sự bị bỏ sót vẫn ném, chỉ nút đã khai "không chạy" mới được tha.
        """
        for n in ast.walk(nut):
            if isinstance(n, ast.Call):
                ket.append((n, None))

    def tham(con, chuoi):
        """Thăm MỘT nút. Nút phạm vi được xử lý TẠI ĐÂY chứ không phải ở vòng lặp của nút cha.

        Bản đầu của N37 truyền nút phạm vi vào hàm duyệt như GỐC, nên chính nó không còn được
        nhận ra là phạm vi và một hàm lồng trong hàm mất đúng một tầng. Đo được ngay trên kho:
        `scripts/tl_selftest.py` khai 1 lời gọi trần mà đo được 0 — cổng ra ĐỎ và chỉ thẳng tệp.
        Ca tối giản: `def run(): def f(): import shutil as sh; sh.which("bash")` ⇒ `[]`.
        """
        if hoan_chu_thich and isinstance(con, (ast.FunctionDef, ast.AsyncFunctionDef)):
            a = con.args
            for x in (*a.posonlyargs, *a.args, *a.kwonlyargs, a.vararg, a.kwarg):
                if x is not None and x.annotation is not None:
                    khong_chay(x.annotation)
            if con.returns is not None:
                khong_chay(con.returns)
        if isinstance(con, ast.AnnAssign) and (hoan_chu_thich
                                               or (len(chuoi) > 1 and not chuoi[-1][0])):
            # Chú thích biến: bị hoãn (có `__future__`), hoặc nằm trong HÀM (không bao giờ tính).
            khong_chay(con.annotation)
            for x in (con.target, con.value):
                if x is not None:
                    tham(x, chuoi)
            return
        if isinstance(con, _NUT_PHAM_VI):
            ngoai, trong = _ngoai_va_trong(con)
            chuoi_trong = chuoi + [pham_vi(con)]
            for x in ngoai:
                tham(x, chuoi)
            for x in trong:
                tham(x, chuoi_trong)
            return
        if isinstance(con, ast.Call):
            # `hoi_rang_buoc=True` (N58, r18): hỏi "tên này có ràng buộc nào trong chuỗi phạm
            # vi không" — để biết `str`/`bytes` còn là tên DỰNG SẴN hay đã bị che. `_giai_ten`
            # trả None cho CẢ "không ràng buộc" lẫn "bị che", nên không trả lời được câu ấy.
            ket.append((con, lambda ten, hoi_rang_buoc=False, c=chuoi,
                        v=(con.lineno, con.col_offset):
                        _co_rang_buoc(ten, c) if hoi_rang_buoc else _giai_ten(ten, c, v)))
        for x in ast.iter_child_nodes(con):
            tham(x, chuoi)

    for _con in ast.iter_child_nodes(cay):
        tham(_con, [pham_vi(cay)])
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
    if ten in _TEN_SHELL_RA:
        return "shell_ra"
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
            return _loai_theo_cap(mod, nut.func.attr)
        return None
    if isinstance(nut.func, ast.Name):
        muc = tra_ten(nut.func.id)
        if muc and muc[1] is not None and muc[1] in _MODULE_CHU[muc[0]]:
            return _loai_theo_cap(muc[0], muc[1])
    return None


def _loai_theo_cap(mod, ham):
    """Loại lời gọi cho CẶP (module, hàm). Tra theo CẶP chứ không theo tên trần: `run` của
    `subprocess` và một `run` giả định của module khác không được lẫn nhau."""
    if (mod, ham) in _API_THEO_TEN:
        return f"api:{mod}.{ham}"
    if (mod, ham) in _API_ARGV:
        return f"argv:{mod}.{ham}"
    if mod in ("subprocess", "shutil"):
        return _LOAI_THEO_TEN.get(ham)
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
# N38 (r13) — ĐÔNG CỨNG PHẢI GHIM BLOB, KHÔNG CHỈ ĐẾM SỐ. Bảng này KHAI "không được sửa một
# byte" mà chỉ ĐO số lời gọi. Lời khai RỘNG HƠN PHÉP ĐO — đúng hình dạng kho đã đặt tên ở
# packet N6-LOI-KHAI-RONG-HON-PHEP-DO. Đo được trên `cf6e6cb`: đổi HẾT bảy `shutil.which("bash")`
# thành `subprocess.run(["bash"])`, giữ nguyên số 7, cổng vẫn `rc=0 DAT`, `lech_so` RỖNG.
# Nay mỗi mục mang `(số_lần, OID_blob, lý_do)`: OID lệch ⇒ ĐỎ, dù số có khớp. Làm mới ảnh chụp
# hợp lệ thì phải cập nhật OID tường minh — đó là cái giá, và là cái giá ĐÚNG.
ANH_CHUP_DONG_CUNG = {
    "ops/reviews/goi-va-lease-hoi-toan-kho-1/lease_publish_test.py":
        (7, "1d7f5f41e27558473fded1876aa920c6433da2de",
         "ảnh chụp verdict đông cứng — `t26` băm lại mỗi lượt, KHÔNG được sửa một byte"),
    "ops/reviews/goi-va-lease-hoi-toan-kho-2/lease_publish_test.py":
        (7, "d74def6953f72325bcf03f108fd8ee695785ab29",
         "ảnh chụp verdict đông cứng — như trên"),
}

# RATCHET. Mỗi mục là một tệp CHƯA chuyển sang `tim_bash`, kèm lý do đo được. Cổng ĐỎ theo
# CẢ HAI chiều:
#   · tệp NGOÀI `CHO_PHEP ∪ CHUA_CHUYEN` mà có lời gọi trần  ⇒ ĐỎ (bản sao thứ tư);
#   · tệp TRONG `CHUA_CHUYEN` mà KHÔNG còn lời gọi trần nào ⇒ ĐỎ (danh sách đã mục).
# Chiều thứ hai là thứ bắt danh sách phải NGẮN đi. Thiếu nó thì ratchet thành nghĩa trang:
# ai vá xong cũng quên xoá tên mình, và cổng dần hết ý nghĩa mà vẫn xanh.
# NGAY GO la BAT BUOC cho moi muc (#570 r4, N17). Mot danh sach khong co ngay go la mot
# nghia trang — dung thu N5 sinh ra de chan, chi cham hon.
# N44 (r15) — NGÀY GỠ PHẢI ĐƯỢC ĐỌC. Trước r15 hằng này chỉ được nội suy vào chuỗi LÝ DO và
# KHÔNG mã nào so sánh nó: đo được trên `f6189e3` — `_NGAY_GO` chỉ xuất hiện ở `Assign` và
# `FormattedValue`, không một `Compare` nào, không `import datetime`. Tức sau 2026-12-31 mọi
# mục ratchet vẫn pass VÔ HẠN. Lại đúng họ **N6-LOI-KHAI-RONG-HON-PHEP-DO** — lần thứ BA trong
# packet, sau `ANH_CHUP_DONG_CUNG` (r13) và chính bảng này.
# Ngày so theo **UTC** để phán quyết không đổi theo múi giờ người chạy; `quet(hom_nay=...)`
# cho ca đo tiêm ngày, nên luật này ĐỎ được mà không phải chờ tới cuối năm.
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


def quet(goc: Path, hom_nay=None):
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
    # N42 (r15) — `tokenize.detect_encoding` ném `SyntaxError` khi cookie mã hoá lạ, và
    # `LookupError` khi tên mã hoá không tồn tại. Bản r13 không bắt hai loại ấy, nên CLI
    # THOÁT 1 KÈM TRACEBACK thay vì trả `rc=3 KHONG_DO_DUOC` như tài liệu khai. Đo được trên
    # `f6189e3`: tệp `# coding: khong-ton-tai` ⇒ rc=1, stdout KHÔNG phải JSON, stderr có
    # traceback. BẮT HẸP — chỉ quanh `_doc_noi_dung` — để một lỗi hiện thực khác không bị
    # biến thành "phép đo thất bại".
    except (OSError, UnicodeDecodeError, SyntaxError, LookupError, ValueError) as e:
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
                                  "lien_ket_tuong_trung": [_duong_bao_cao(x) for x in lien_ket],
                                  "bien_git_da_go": bien_git_da_go,
                                  "ly_do": "mục `*.py` trong INDEX là SYMLINK: "
                                           + ", ".join(_duong_bao_cao(x) for x in lien_ket)
                                           + ". Nội dung thật nằm NGOÀI thứ INDEX ghim, nên cổng "
                                             "không đo được — `None ≠ False`."}
    co_loi_goi = {}
    for rel, than in sorted(noi_dung.items()):
        try:
            dong = _loi_goi_tran(than)
        except (SyntaxError, ValueError) as e:
            # FAIL-CLOSE. Một tệp không phân tích được là một tệp KHÔNG ĐO ĐƯỢC, không
            # phải một tệp sạch — `None ≠ False`.
            # N48 (r16) — `_duong_bao_cao` PHAI phu CA loi ra LOI. Ban r15 chi lam sach
            # duong o `co_loi_goi`, con nhanh nay nhet `rel` THO vao `ly_do`; do duoc: mot
            # muc `ops/bad_\xff.py` cu phap hong lam `quet --json` nha byte 0xff, va mot
            # trinh doc UTF-8 NGHIEM NGAT tu choi ca ban bao cao. Duong xau chi can mot loi
            # ra chua sach la du hong; nen luat di theo TRUONG, khong theo nhanh.
            return RC_KHONG_DO_DUOC, {"trang_thai": "KHONG_DO_DUOC", "nguon_tep": nguon_tep,
                                      "bien_git_da_go": bien_git_da_go,
                                      "ly_do": "không đọc/phân tích được "
                                               f"{_duong_bao_cao(rel)}: {e}"}
        if dong:
            # N54 (r17) — KHOÁ GIỮ NGUYÊN VẸN. `_duong_bao_cao` là phép HIỂN THỊ; dùng nó
            # làm khoá thì hai đường khác nhau có thể đè nhau (đo được ở vòng 11).
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
    # N38 — OID lệch là ĐỎ, dù số có khớp. Một mục khai "đông cứng từng byte" mà chỉ đo SỐ là
    # lời khai rộng hơn phép đo.
    lech_oid = {}
    # N71 (r19) — KIỂM HÌNH DẠNG BẢNG ĐÔNG CỨNG ở MỌI chế độ, không chỉ khi cây là kho git.
    # Bản đầu của N71 đặt phép kiểm này BÊN TRONG nhánh `git`, và chốt mới của `t40` ĐỎ: cây
    # của `t40` không phải kho git nên mục hỏng lọt qua. Một bảng đông cứng thiếu OID là lỗi
    # CẤU HÌNH, bất kể cây đang quét là gì — nên nó đi vào `khong_khai_so` trước tiên.
    for t, m in ANH_CHUP_DONG_CUNG.items():
        if _oid_dong_cung(m) is None and t not in khong_khai_so:
            khong_khai_so.append(t)
    if nguon_tep == "git":
        oid_that = {rel: sha for rel, _, sha in cac_tep}
        for t, m in ANH_CHUP_DONG_CUNG.items():
            ghim = _oid_dong_cung(m)
            if ghim is None:
                continue                   # đã vào `khong_khai_so` ở trên
            thay_oid = oid_that.get(t)
            if thay_oid != ghim:
                lech_oid[t] = {"ghim": ghim, "do_duoc": thay_oid}
    if hom_nay is None:
        hom_nay = _dt.datetime.now(_dt.timezone.utc).date()
    qua_han = sorted(CHUA_CHUYEN) if (CHUA_CHUYEN and hom_nay > _dt.date.fromisoformat(_NGAY_GO)) else []
    da_sach = [t for t in CHUA_CHUYEN if t not in co_loi_goi]
    bao = {"da_quet": str(thu_muc), "pham_vi": "toan-cay", "nguon_tep": nguon_tep,
           "nguon_noi_dung": "blob-index" if nguon_tep == "git" else "cay-lam-viec",
           "bien_git_da_go": bien_git_da_go, "co_loi_goi_tran": co_loi_goi,
           "ngoai_danh_sach": moi, "muc_ratchet_da_sach": sorted(da_sach), "lech_so_loi_goi": lech_so,
           "cho_phep": sorted(CHO_PHEP), "anh_chup": sorted(ANH_CHUP_DONG_CUNG), "chua_chuyen": sorted(CHUA_CHUYEN),
           "lech_oid_dong_cung": lech_oid, "ngay_go": _NGAY_GO,
           # N71 (r19) — TRƯỜNG CƠ CHẾ: mục miễn trừ không đo được (hạn ngạch hỏng, mục đông
           # cứng không ghim OID hợp lệ). Có nó thì ca đo được N63/N71 mà không phải chốt
           # `trang_thai` — N22.
           "mien_tru_hong": sorted(_duong_bao_cao(t) for t in khong_khai_so),
           "ratchet_qua_han": qua_han,
           "so_cho_phep": {t: _so_cho_phep(m)[0] for t, m in sorted(_MIEN_TRU.items())}}
    if khong_khai_so:
        # FAIL-CLOSE. Một mục miễn trừ không khai hạn ngạch số là một mục KHÔNG ĐO ĐƯỢC,
        # không phải một mục được tha — r7 tha nó, và đó là vé vô hạn (xem `_so_cho_phep`).
        bao["trang_thai"] = "KHONG_DO_DUOC"
        bao["ly_do"] = ("mục miễn trừ KHÔNG khai hạn ngạch số: "
                        + ", ".join(_duong_bao_cao(t) for t in sorted(khong_khai_so))
                        + ". Mỗi mục phải là `(số_lần, lý_do)`; một chuỗi trần là miễn trừ "
                          "theo TƯ CÁCH THÀNH VIÊN — đo được: mục chuỗi, 9 lời gọi ⇒ DAT.")
        return RC_KHONG_DO_DUOC, bao
    if moi:
        bao["trang_thai"] = "DO"
        bao["ly_do"] = (
            "có lời gọi `bash` TRẦN ở tệp ngoài danh sách cho phép: "
            + "; ".join(f"{_duong_bao_cao(t)}:{d}" for t, d in sorted(moi.items()))
            + ". Dùng `ops/bash_nen.py::tim_bash()` — nó QUYẾT BẰNG NĂNG LỰC, và "
              "`shutil.which(\"bash\")` trên Windows trả bộ phóng WSL (Issue #570).")
        return RC_DO, bao
    if qua_han:
        bao["trang_thai"] = "DO"
        bao["ly_do"] = (
            f"mục ratchet QUÁ NGÀY GỠ {_NGAY_GO} (hôm nay {hom_nay}): " + ", ".join(qua_han)
            + ". Ngày gỡ là một HẠN, không phải một chữ trong lý do — hoặc chuyển các tệp ấy "
              "sang `tim_bash()`, hoặc gia hạn tường minh kèm phép đo nói vì sao.")
        return RC_DO, bao
    if lech_oid:
        bao["trang_thai"] = "DO"
        bao["ly_do"] = (
            "ảnh chụp ĐÔNG CỨNG đã đổi BLOB: "
            + "; ".join(f"{_duong_bao_cao(t)} ghim {v['ghim'][:12]} mà đo được "
                        f"{str(v['do_duoc'])[:12]}"
                        for t, v in sorted(lech_oid.items()))
            + ". Mục khai 'không được sửa một byte' thì phải ĐO bằng blob, không bằng số lần — "
              "đổi hết 7 lời gọi sang một hình dạng khác mà giữ số 7 thì phép đếm không thấy gì. "
              "Làm mới ảnh chụp hợp lệ ⇒ cập nhật OID tường minh.")
        return RC_DO, bao
    if lech_so:
        bao["trang_thai"] = "DO"
        bao["ly_do"] = (
            "số lời gọi trần LỆCH với hạn ngạch khai (CHO_PHEP ∪ CHUA_CHUYEN ∪ ANH_CHUP_DONG_CUNG): "
            + "; ".join(f"{_duong_bao_cao(t)} khai {v['khai']} mà đo được {v['do_duoc']} "
                        f"(dòng {v['dong']})"
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


def _ra_json(bao) -> str:
    r"""JSON cua CLI, ASCII thuan — HANG RAO THU HAI cua N48 (r16).

    `_duong_bao_cao` lam sach TUNG TRUONG; ham nay lam sach CA BAN BAO CAO. Hai lop gap nhau
    o cho ca hai deu phai sai thi dau ra moi hong — dung ky luat `_doc_noi_dung` + go bien
    `GIT_*` da dung. `ensure_ascii=True` bien mot surrogate lac thanh `\udcff` sau ky tu
    ASCII, nen stdout LUON giai ma duoc bang UTF-8 nghiem ngat, con `json.loads` van tra lai
    dung chuoi cu. CAI GIA, khai thang: chu Viet trong `ly_do` ra duoi dang `\uXXXX` — doc
    bang may thi y het, doc bang mat thi xau hon. Doi lay mot loi ra KHONG BAO GIO hong.
    """
    return json.dumps(bao, ensure_ascii=True, indent=2)


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
        print(_ra_json(out) if a.json else (duong or "KHONG_DO_DUOC"))
        return RC_OK if duong else RC_KHONG_DO_DUOC

    rc, bao = quet(Path(a.root))
    if a.json:
        print(_ra_json(bao))
    else:
        print(f"{bao['trang_thai']}: {bao.get('ly_do', 'không có lời gọi trần mới')}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
