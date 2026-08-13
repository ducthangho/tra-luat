#!/usr/bin/env python3
"""launcher.py — gọi agent (Claude/Codex/bất kỳ) một cách TẤT ĐỊNH, đa nền.

VÌ SAO CÓ TỆP NÀY
Bản gốc của các chốt này là hai script PowerShell chạy được đúng một nền: Windows.
Điện thoại và phiên remote không có shell cục bộ, macOS/Linux không có PowerShell
mặc định — nghĩa là các bảo đảm quan trọng nhất (neo HEAD, neo prompt, hạn chót,
giết cả cây tiến trình) chỉ tồn tại ở một chỗ. Tệp này đưa chúng về Python 3, nền
duy nhất đã có mặt ở mọi đường vào của kho này.

BỐN BẪY ĐA NỀN ĐÃ TRẢ GIÁ, và cách tệp này né:

1. `git -C <đường dẫn có dấu>` — Windows PowerShell 5.1 mã hoá đối số lệnh native
   theo codepage ANSI, nên `D:\\Quốc hội\\tra-luat` tới git đã méo và git báo
   "not a git repository" dù thư mục có `.git`. ĐÃ ĐO TRÊN MÁY NGƯỜI DÙNG.
   Ở đây: subprocess nhận list đối số và Windows dùng CreateProcessW (Unicode),
   nên lỗi đó BIẾN MẤT — không phải né, mà là không còn tồn tại.

2. `(& git ...).Trim()` — đầu ra rỗng thành None rồi ném ngay tại đó, khiến dòng
   kiểm mã lỗi bên dưới thành CODE CHẾT. Ở đây mọi lệnh git đi qua `_git()` trả về
   bộ ba (rc, out, err) và rc được kiểm TRƯỚC khi đụng vào chuỗi.

3. rc=0 mà stdout RỖNG (wrapper hỏng, git giả, vỏ bọc doanh nghiệp) — chỉ kiểm rc
   là lọt. Mọi chốt ở đây kiểm CẢ HAI: rc và nội dung.

4. Giết theo PID trần — PID bị tái dùng, giết nhầm tiến trình vô can. Ở đây kèm
   "khoá danh tính" (thời điểm khởi động). KHÔNG lấy được khoá thì TỪ CHỐI giết
   (thoát 10) chứ không giết liều.

MÃ THOÁT — mỗi chốt một mã, để phía gọi xử lý được mà không phải đọc chữ:
  0   qua hết
  2   tham số sai
  3   workspace không phải repo git / git không chạy được
  4   HEAD lệch
  5   ref lệch
  6   worktree bẩn
  7   prompt: thiếu tệp / rỗng / sha lệch
  8   hạn chót đã qua trước khi chạy
  9   va chạm run_id/short_id
  10  không xác định được danh tính tiến trình → từ chối giết
  11  kho không đúng (remote/commit gốc lệch)
  12  thiếu công cụ bắt buộc (xem `doctor`)
  124 quá hạn trong lúc chạy (giống `timeout(1)`) — VÀ đã giết được
  125 quá hạn NHƯNG KHÔNG giết được: tiến trình còn sống, cần người can thiệp
  130 bị ngắt (Ctrl-C) — đã giết con
  141 đầu ra bị cắt ống ở chỗ không giữ được kết luận (128+SIGPIPE)
  1   mã thoát của con nằm ngoài 0..255; số THẬT ở `ma_thoat_that` trong sổ

CẢNH BÁO VỀ CHÍNH BẢNG TRÊN: với `run`, mã thoát của TIẾN TRÌNH CON được trả
nguyên vẹn, nên nó ĐÈ LÊN mọi mã ở đây — `rc=124` không phân biệt được "launcher
cưỡng chế hạn chót" với "con tự thoát 124" (con chạy `timeout(1)`, hoặc con là
một launcher khác). Phía gọi TỰ ĐỘNG phải đọc `trang_thai` trong `run.json`
(`xong` · `qua_han` · `bi_ngat` · `da_dung` · `hong`) chứ đừng suy từ mã trần.
`check`/`status`/`stop`/`doctor` không có con nên bảng trên là dứt khoát.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"

MA_OK = 0
MA_THAM_SO = 2
MA_GIT = 3
MA_HEAD = 4
MA_REF = 5
MA_BAN = 6
MA_PROMPT = 7
MA_HAN = 8
MA_VA_CHAM = 9
MA_DANH_TINH = 10
MA_KHO = 11
MA_QUA_HAN = 124
MA_GIET_HUT = 125
MA_THIEU_CONG_CU = 12

# Bộ đột biến dùng cùng mốc này để không thể trượt từ ~70% phép đo được xuống
# gần 0 mà vẫn xanh. Đặt ở mã được đột biến (không đặt trong chính runner test).
TY_LE_DOT_BIEN_TOI_THIEU_PHAN_MUOI = 7

# Ảnh chụp Windows: tiến trình CÓ MẶT nhưng không đọc được `CreationDate`, tức
# không lấy được khoá danh tính cho nó. Đánh dấu thay vì bỏ qua im lặng — bỏ qua
# thì một hậu duệ biến mất khỏi ảnh rồi ảnh rỗng thành "cả cây đã chết".
KHONG_DOC_DUOC_KHOA = "\x00khong-doc-duoc-khoa"

# Số tick 100ns từ 0001-01-01 tới 1601-01-01. FILETIME đếm từ 1601, .NET
# DateTime.Ticks đếm từ năm 1 — đây là toàn bộ phần lệch EPOCH giữa hai nguồn.
LECH_EPOCH_FILETIME = 504_911_232_000_000_000

# Tạo cờ CREATE_SUSPENDED: `subprocess` không đặt tên hằng này, mà `creationflags`
# chỉ là số nguyên nên truyền thẳng được.
CREATE_SUSPENDED = 0x0000_0004

# Trạng thái CUỐI của một lượt chạy — `stop` không được ghi đè lên chúng.
TRANG_THAI_KET_THUC = {"xong", "qua_han", "bi_ngat", "hong", "da_dung"}

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
# git@host:owner/repo.git  —  dạng kiểu scp, KHÔNG phải URL nên urlparse đọc sai
REMOTE_SCP_RE = re.compile(r"^[\w.+-]+@([^:/]+):(.+)$")
# scheme://[thông-tin-đăng-nhập@]host[:cổng]/owner/repo[.git]
REMOTE_URL_RE = re.compile(r"^[a-zA-Z][\w+.-]*://(?:[^@/]*@)?([^/:]+)(?::\d+)?/(.+)$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


# ---------------------------------------------------------------- tiện ích nền

def _bay_gio() -> datetime:
    return datetime.now(timezone.utc)


def _doc_iso(s: str) -> datetime | None:
    """Đọc mốc thời gian ISO 8601. 'Z' hợp lệ; thiếu múi giờ thì COI LÀ UTC.

    Không đoán múi giờ địa phương: hạn chót là thứ hai phía phải hiểu giống nhau,
    mà máy người dùng và máy chạy phiên remote thường khác múi.
    """
    if not s:
        return None
    t = s.strip().replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(t)
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)


def _git(workspace: str | os.PathLike, *doi_so: str) -> tuple[int, str, str]:
    """Chạy git, trả (rc, stdout, stderr). KHÔNG dùng shell, KHÔNG nối chuỗi.

    Đối số đi dạng list nên đường dẫn có dấu/khoảng trắng an toàn trên mọi nền —
    đây chính là chỗ bản PowerShell gãy.
    """
    if not shutil.which("git"):
        return (127, "", "khong tim thay git trong PATH")
    try:
        # timeout BẮT BUỘC: một `git` treo (ổ mạng, credential helper hỏi mật khẩu,
        # vỏ bọc doanh nghiệp) sẽ treo LUÔN cả đường cưỡng chế hạn chót — đúng thứ
        # mà --deadline-utc tồn tại để bảo đảm. Audit vòng 3: chỉ _phien_ban có timeout.
        p = subprocess.run(["git", "-C", str(workspace), *doi_so],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=120)
    except subprocess.TimeoutExpired:
        return (127, "", "git treo qua 120s")
    except OSError as e:  # git bị xoá giữa chừng, quyền, ...
        return (127, "", str(e))
    return (p.returncode, p.stdout, p.stderr)


def _git_mot_dong(workspace, *doi_so) -> tuple[int, str, str]:
    """Như _git nhưng đòi ĐÚNG một dòng có nội dung.

    rc=0 mà rỗng là ca thật (git giả, wrapper nuốt stdout) và phải bị coi là hỏng —
    nếu chỉ kiểm rc thì chốt thủng đúng ở đây.
    """
    rc, out, err = _git(workspace, *doi_so)
    if rc != 0:
        return (rc, "", err.strip() or out.strip())
    dong = [d for d in out.splitlines() if d.strip()]
    if not dong:
        return (rc, "", "git thoat 0 nhung KHONG in gi")
    return (0, dong[0].strip(), "")


# --------------------------------------------------- danh tính tiến trình (kill an toàn)

def _khoa_win(tick_nam_1_utc) -> str | None:
    """Khoá Windows CHUẨN HOÁ: MICRO-GIÂY kể từ năm 1, giờ UTC.

    Windows có HAI nguồn đọc được thời điểm khởi động, và chúng KHÔNG cùng đơn vị:

      · CIM `Win32_Process.CreationDate` — `DateTime` kiểu Local, `.Ticks` đếm
        100ns từ năm 1. Chuỗi CIM_DATETIME gốc chỉ có tới MICRO-giây, nên ba chữ
        số tick cuối luôn là 0.
      · `GetProcessTimes` trên handle — FILETIME, 100ns từ 1601, luôn UTC, ĐỦ
        độ phân giải 100ns.

    Nếu để nguyên hai dạng rồi so bằng `==` thì khoá KHÔNG BAO GIỜ khớp, và hậu
    quả đi theo chiều nguy hiểm nhất: chốt danh tính hoá ra LUÔN TỪ CHỐI giết —
    hỏng âm thầm, tệ hơn hẳn không có chốt (cảnh báo mở đầu của khe hở #3).
    Nên chuẩn hoá về mẫu số chung THÔ HƠN cả hai:
      · epoch: cả hai đưa về năm 1 (cộng `LECH_EPOCH_FILETIME` cho FILETIME);
      · múi giờ: cả hai đưa về UTC (PowerShell gọi `ToUniversalTime()`, tránh
        hẳn việc phải tự suy độ lệch múi giờ TẠI THỜI ĐIỂM ĐÓ — nghĩ được là DST
        đã sai rồi);
      · độ phân giải: chia 10, tức bỏ phần 100ns mà CIM vốn đã không có.

    Cắt xuống micro-giây KHÔNG làm loãng chốt: nó tồn tại để phân biệt hai tiến
    trình dùng lại cùng một PID, mà hai lần khởi động cách nhau xa hơn 1µs rất
    nhiều lần.
    """
    try:
        return f"win:{int(tick_nam_1_utc) // 10}"
    except (TypeError, ValueError):
        return None


def _khop_khoa(hien: str | None, mong_doi) -> bool:
    """`hien` có khớp khoá mong đợi không. `mong_doi` là MỘT khoá hoặc BỘ khoá.

    VÌ SAO LÀ BỘ: trên Windows một lượt chạy có thể ghi được khoá từ hai nguồn
    độc lập (CIM và handle `Popen`, xem `_khoa_tu_handle`). Chúng phải ra cùng
    một chuỗi — nhưng "phải" là suy luận cho tới khi đo được trên Windows thật.
    Ghi cả hai rồi chấp nhận khớp BẤT KỲ nghĩa là: một sai sót trong phép quy đổi
    epoch không thể biến chốt thành "luôn từ chối". Không nới lỏng gì cả — PID bị
    tái dùng vẫn không khớp khoá nào, vì cả hai đều nói về THỜI ĐIỂM KHỞI ĐỘNG.
    """
    if hien is None or mong_doi is None:
        return False
    if isinstance(mong_doi, str):
        return hien == mong_doi
    return hien in set(mong_doi)


def _ds_khoa(khoa) -> list[str]:
    """Đưa khoá (một chuỗi / bộ khoá / None) về danh sách chuỗi không rỗng."""
    if khoa is None:
        return []
    if isinstance(khoa, str):
        return [khoa] if khoa else []
    return [k for k in khoa if isinstance(k, str) and k]


def _khoa_danh_tinh(pid: int) -> str | None:
    """Khoá nhận dạng tiến trình để chống PID tái dùng. None = không xác định được.

    Không có khoá thì tuyệt đối không giết: PID quay vòng, và giết nhầm một tiến
    trình vô can là hỏng nặng hơn nhiều so với để một tiến trình sống thừa.
    """
    he = platform.system()
    try:
        if he == "Linux":
            noi_dung = Path(f"/proc/{pid}/stat").read_text()
            # comm có thể chứa khoảng trắng và dấu ')' -> cắt từ ')' CUỐI CÙNG
            sau = noi_dung[noi_dung.rindex(")") + 2:].split()
            return f"linux:{sau[19]}"  # trường 22 tính từ 1 = starttime
        if he == "Darwin":
            p = subprocess.run(["ps", "-o", "lstart=", "-p", str(pid)],
                               capture_output=True, text=True, timeout=15)
            v = p.stdout.strip()
            return f"darwin:{v}" if v else None
        if he == "Windows":
            # Win32_Process.CreationDate chu KHONG Get-Process.StartTime: `_chup_cay`
            # phai lay ca cay trong MOT lan goi, ma nguon duy nhat cho ca pid lan
            # ParentProcessId lan thoi diem tao la CIM. Hai nguon khac nhau thi
            # `.Ticks` lech dinh dang/epoch, khoa khong bao gio khop, va chot hoa ra
            # LUON tu choi giet - hong am tham theo chieu nguoc lai.
            # `.ToUniversalTime()` la BAT BUOC: CIM tra DateTime kieu Local, con
            # nguon thu hai (`_khoa_tu_handle`) la FILETIME von luon UTC. Doi ve UTC
            # NGAY TAI NGUON thi khong ai phai tu suy do lech mui gio - va khong ai
            # phai nho rang do lech ay con doi theo DST.
            p = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command",
                 f'(Get-CimInstance Win32_Process -Filter "ProcessId={pid}")'
                 '.CreationDate.ToUniversalTime().Ticks'],
                capture_output=True, text=True, timeout=30)
            v = p.stdout.strip()
            return _khoa_win(v) if v.isdigit() else None
    except (OSError, ValueError, IndexError):
        return None
    return None


def _khoa_tu_handle(p) -> str | None:
    """Khoá danh tính đọc từ HANDLE mà `Popen` đang giữ. None = không lấy được.

    VÌ SAO CẦN, dù đã có `_khoa_danh_tinh` (khe hở #3 của đợt trước): trên Windows
    một tiến trình VỪA THOÁT là biến mất hẳn khỏi CIM/`Get-Process`, nên con chạy
    nhanh hơn lần gọi powershell đầu tiên sẽ không bao giờ có khoá. POSIX không
    dính vì `/proc/<pid>` còn ở dạng zombie cho tới khi cha `wait`. Hậu quả ĐO
    ĐƯỢC trên windows-latest: sổ ghi `khoa_danh_tinh=null` ⇒ `stop` lượt đó TỪ
    CHỐI vĩnh viễn bằng mã 10, kể cả khi lượt chạy hoàn toàn bình thường.

    Handle thì khác: `Popen` giữ nó cho tới lúc đóng, và Windows không tái dùng
    PID chừng nào còn một handle mở. Nên `GetProcessTimes` trên chính handle ấy
    đọc được thời điểm khởi động SAU KHI tiến trình đã thoát — đúng chỗ CIM mù.

    Trả về cùng khuôn `_khoa_win` với nguồn CIM; xem hàm đó về lệch epoch/múi giờ.
    """
    if platform.system() != "Windows":
        return None
    try:
        import ctypes
        from ctypes import wintypes
        h = getattr(p, "_handle", None)
        if not h:
            return None
        tao, thoat, nhan, nguoi = (wintypes.FILETIME() for _ in range(4))
        if not ctypes.windll.kernel32.GetProcessTimes(
                ctypes.c_void_p(int(h)), ctypes.byref(tao), ctypes.byref(thoat),
                ctypes.byref(nhan), ctypes.byref(nguoi)):
            return None
        ft = (int(tao.dwHighDateTime) << 32) | int(tao.dwLowDateTime)
        if ft <= 0:
            return None
        return _khoa_win(ft + LECH_EPOCH_FILETIME)
    except (OSError, AttributeError, ValueError):
        return None


def _thanh_vien_nhom(pgid: int) -> list[int] | None:
    """PID còn SỐNG trong nhóm tiến trình `pgid`. Zombie KHÔNG tính là sống.

    Trả `[]` = đã CHỨNG MINH nhóm rỗng · danh sách = còn người · `None` = KHÔNG
    đo được (và khi đó tuyệt đối không được khẳng định "cả cây đã chết").

    VÌ SAO CẦN (audit vòng 3, đo trên Linux): `_con_song(pid)` chỉ nói về tiến
    trình MẸ. Bản trước thoát vòng chờ ngay khi mẹ chết rồi trả
    KetGiet(True, True, "SIGTERM: da tat ca cay") — nên `killpg(SIGKILL)` bên
    dưới KHÔNG BAO GIỜ được gửi, và một tiến trình CHÁU chỉ cần `SIG_IGN` cho
    SIGTERM là sống sót nguyên vẹn trong khi hạn chót trả 124 ("đã giết được").
    Dựng lại được bằng hai cách, cả hai đều ra 124 với cháu còn sống:
      · cháu gọi setsid() rồi rời nhóm
      · cháu ở NGUYÊN trong nhóm, chỉ phớt lờ SIGTERM  <- ca này nhóm vẫn thấy
    Đúng lớp lỗi mà vòng 2 đã vá cho Windows: "đã gọi lệnh giết" ≠ "đã chết".

    GIỚI HẠN: đây chỉ là bằng chứng theo NHÓM — cháu tự `setsid()` đã rời nhóm
    nên hàm này KHÔNG thấy nó. Phần đó do `_chup_cay` lo (chụp trước khi giết).
    """
    he = platform.system()
    if he == "Linux":
        try:
            ds = [p for p in Path("/proc").iterdir() if p.name.isdigit()]
        except OSError:
            return None
        ra = []
        for p in ds:
            try:
                nd = (p / "stat").read_text()
                sau = nd[nd.rindex(")") + 2:].split()
                if sau[0] == "Z":          # zombie = đã chết, chờ thu hồi
                    continue
                if int(sau[2]) == pgid:    # trường 5 tính từ 1 = pgrp
                    ra.append(int(p.name))
            except (OSError, ValueError, IndexError):
                continue   # tiến trình biến mất giữa lúc quét: coi như đã chết
        return ra
    if he == "Darwin":  # không có /proc — hỏi ps, và CÓ timeout
        try:
            p = subprocess.run(["ps", "-A", "-o", "pid=,pgid=,state="],
                               capture_output=True, text=True, timeout=15)
        except (OSError, subprocess.SubprocessError):
            return None
        if p.returncode != 0:
            return None
        ra = []
        for dong in p.stdout.splitlines():
            phan = dong.split()
            if len(phan) < 3:
                continue
            try:
                if int(phan[1]) == pgid and not phan[2].startswith("Z"):
                    ra.append(int(phan[0]))
            except ValueError:
                continue
        return ra
    return None


def _chup_cay(pid: int) -> dict[int, str] | None:
    """Ảnh chụp {pid: khoá danh tính} của `pid`, MỌI hậu duệ, và mọi thành viên nhóm.

    PHẢI chụp TRƯỚC khi giết. Cháu đã `setsid()` thì đã rời NHÓM; đến khi mẹ chết
    nó được init nhận nuôi nên mất nốt liên kết CHA — sau thời điểm đó không còn
    đường nào tìm ra nó nữa. Chụp trước là cách duy nhất giữ được danh sách phải
    kiểm, và cũng là cách duy nhất GIẾT được nó (`killpg` không với tới).

    Kèm khoá danh tính từng pid để lúc kiểm/giết lại không đụng nhầm một PID đã
    bị tái dùng — cùng doctrine với `_khoa_danh_tinh`.

    Còn lại đúng một khe không phủ được, nói thẳng: tiến trình sinh ra SAU lúc
    chụp rồi lập tức `setsid()`. Nó không ở trong ảnh, cũng không ở trong nhóm.
    """
    he = platform.system()
    if he == "Linux":
        try:
            ds = [p for p in Path("/proc").iterdir() if p.name.isdigit()]
        except OSError:
            return None
        tt = {}
        for p in ds:
            try:
                nd = (p / "stat").read_text()
                sau = nd[nd.rindex(")") + 2:].split()
                if sau[0] == "Z":                     # zombie = đã chết
                    continue
                tt[int(p.name)] = (int(sau[1]), int(sau[2]), f"linux:{sau[19]}")
            except (OSError, ValueError, IndexError):
                continue
    elif he == "Darwin":
        try:
            p = subprocess.run(["ps", "-A", "-o", "pid=,ppid=,pgid=,state="],
                               capture_output=True, text=True, timeout=15)
        except (OSError, subprocess.SubprocessError):
            return None
        if p.returncode != 0:
            return None
        tt = {}
        for dong in p.stdout.splitlines():
            phan = dong.split()
            if len(phan) < 4 or phan[3].startswith("Z"):
                continue
            try:                                       # ps không cho starttime gọn
                tt[int(phan[0])] = (int(phan[1]), int(phan[2]), "")
            except ValueError:
                continue
    elif he == "Windows":
        # Windows KHONG co process group, nen chi con duong lien ket CHA-CON.
        # Mot lan goi lay het pid|ppid|ticks; loc hau due o duoi dung chung khuon
        # voi POSIX. Day la thu thay cho `_thanh_vien_nhom` (von tra None o day).
        try:
            pr = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command",
                 "Get-CimInstance Win32_Process | ForEach-Object { if ($_.CreationDate) "
                 "{ \"OK|$($_.ProcessId)|$($_.ParentProcessId)|"
                 "$($_.CreationDate.ToUniversalTime().Ticks)\" } "
                 "else { \"ERR|$($_.ProcessId)|$($_.ParentProcessId)|NO_CREATION_DATE\" } }"],
                capture_output=True, text=True, timeout=60)
        except (OSError, subprocess.SubprocessError):
            return None
        if pr.returncode != 0:
            return None
        tt = {}
        for dong in pr.stdout.splitlines():
            phan = dong.strip().split("|")
            # Thiếu CreationDate là "không đo được", KHÔNG phải "tiến trình
            # không tồn tại". Bỏ qua im lặng có thể làm mất đúng một hậu duệ rồi
            # ảnh rỗng được đọc thành bằng chứng cả cây đã chết.
            #
            # NHƯNG fail-closed phải CÓ PHẠM VI. Bản đầu (vòng 7) trả None ngay khi
            # BẤT KỲ tiến trình nào trên máy thiếu `CreationDate` — kể cả tiến trình
            # hệ thống chẳng liên quan gì tới cây ta sắp giết. Như thế ảnh chụp có
            # dùng được hay không lại phụ thuộc trạng thái máy ở chỗ khác, mà từ khi
            # `_giet_cay` lấy ảnh rỗng làm bằng chứng "đã tắt" trên Windows thì đó là
            # đường quyết định 0-hay-125. Nên: giữ nguyên tiến trình mù TRONG cây (có
            # ppid nên nối được cây), đánh dấu bằng `KHONG_DOC_DUOC_KHOA`, rồi CHỈ trả
            # None nếu dấu đó thật sự rơi vào cây — kiểm ở cuối hàm.
            if len(phan) != 4 or phan[0] not in ("OK", "ERR"):
                return None
            try:
                khoa_q = _khoa_win(phan[3]) if phan[0] == "OK" else None
                tt[int(phan[1])] = (int(phan[2]), 0, khoa_q or KHONG_DOC_DUOC_KHOA)
            except ValueError:
                return None
    else:
        return None
    con = {}
    for q, (cha, _, _) in tt.items():
        con.setdefault(cha, []).append(q)
    ra, hang = {}, [pid]
    while hang:                                        # duyệt cây theo liên kết cha
        q = hang.pop()
        if q in ra or q not in tt:
            continue
        ra[q] = tt[q][2]
        hang.extend(con.get(q, []))
    if he != "Windows":       # process group la khai niem POSIX
        for q, (_, nhom, khoa) in tt.items():          # + thành viên nhóm không phải hậu duệ
            if nhom == pid:
                ra.setdefault(q, khoa)
    ra.pop(os.getpid(), None)                          # tuyệt đối không tự giết mình
    # Fail-closed CÓ PHẠM VI (xem nhánh Windows ở trên): chỉ khi một tiến trình
    # KHÔNG đọc được danh tính nằm TRONG cây thì ảnh mới là "không đo được". Kiểm
    # SAU khi đã bỏ chính mình ra, để tiến trình của ta không tự làm hỏng ảnh.
    if KHONG_DOC_DUOC_KHOA in ra.values():
        return None
    return ra


def _con_song_dung_khoa(pid: int, khoa) -> bool:
    """Còn sống VÀ vẫn đúng tiến trình cũ. Khoá rỗng = không có khoá để so."""
    if not _con_song(pid):
        return False
    ds = _ds_khoa(khoa)
    if not ds:
        return True
    return _khop_khoa(_khoa_danh_tinh(pid), ds)


def _giet_rieng(anh: dict[int, str], tin_hieu: int) -> None:
    """Gửi tín hiệu tới TỪNG pid trong ảnh chụp, có kiểm khoá danh tính trước.

    Cần vì `killpg` không với tới tiến trình đã tự `setsid()` rời nhóm. Kiểm khoá
    nên không bao giờ giết nhầm một PID đã bị tái dùng — đúng chốt số 4 ở đầu tệp.
    """
    for q, khoa in anh.items():
        if q == os.getpid() or not _con_song_dung_khoa(q, khoa):
            continue
        try:
            os.kill(q, tin_hieu)
        except OSError:
            pass


def _con_song(pid: int, khoa=None) -> bool:
    """Tiến trình còn sống không. Dùng để KIỂM SAU khi giết, không đoán.

    `khoa` là khoá danh tính mong đợi. Có nó thì "còn sống" nghĩa là ĐÚNG tiến
    trình cũ còn sống. Thiếu nó, trên Windows hàm này chỉ hỏi được "có tiến trình
    nào mang PID này không" — mà giữa taskkill và lúc kiểm có tới ~2 lần gọi
    powershell (~vài giây, audit vòng 3 đếm được), thừa chỗ để PID bị tái dùng ⇒
    đọc thành "chưa giết được" và trả 125 GIẢ. Fail-closed nên an toàn, nhưng là
    báo động nhầm mà chỉ cần so khoá là hết.

    ZOMBIE PHẢI TÍNH LÀ ĐÃ CHẾT. Con của chính ta, sau khi bị giết, nằm ở trạng
    thái Z cho tới khi được `wait` thu hồi — mà `os.kill(pid, 0)` với zombie vẫn
    THÀNH CÔNG. Bản đầu của hàm này quên điều đó nên báo "khong giet duoc" cho một
    tiến trình đã chết hẳn, và hạn chót trả 125 thay vì 124 (bắt được nhờ t27/t28
    đỏ ngay lượt chạy đầu — đúng việc của phản chứng).
    """
    if platform.system() == "Windows":
        hien = _khoa_danh_tinh(pid)
        if hien is None:
            return False
        return khoa is None or _khop_khoa(hien, khoa)
    trang_thai = Path(f"/proc/{pid}/stat")
    if trang_thai.exists():
        try:
            noi_dung = trang_thai.read_text()
            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"
        except (OSError, ValueError, IndexError):
            return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # tồn tại nhưng khác chủ
    except OSError:
        return False
    if platform.system() == "Darwin":  # không có /proc: hỏi ps
        try:
            p = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)],
                               capture_output=True, text=True, timeout=15)
        except (OSError, subprocess.SubprocessError):
            return True          # không đo được ⇒ KHÔNG dám nói là đã chết
        return not p.stdout.strip().startswith("Z")
    return True


class KetGiet:
    """Kết quả giết, dạng CẤU TRÚC.

    ĐÃ TRẢ GIÁ (audit codex vòng 2): bản trước trả về một CHUỖI rồi hai chỗ gọi đi
    tìm substring "da tat". Nhánh dự phòng ghi "da tat (CON CHAU CO THE CON SONG)"
    — chứa đúng chuỗi đó — nên hạn chót trả 124 trong khi tiến trình CHÁU vẫn sống.
    Giao thức bằng chuỗi tự do là mời lỗi; nay ba sự thật tách bạch:
      me_da_chet  — đã xác nhận tiến trình mẹ biến mất
      ca_cay      — có BẰNG CHỨNG không còn ai sống ngoài mẹ: taskkill /T rc=0
                    (Windows) hoặc nhóm tiến trình đã rỗng (POSIX). Vòng 3 sửa:
                    trước đây POSIX đặt True chỉ vì killpg KHÔNG NÉM LỖI, tức là
                    suy đoán chứ không đo — xem _thanh_vien_nhom.
      mo_ta       — chỉ để người đọc, KHÔNG ai được quyết định dựa vào nó
    """

    def __init__(self, me_da_chet: bool, ca_cay: bool, mo_ta: str, tu_choi: bool = False):
        self.me_da_chet = me_da_chet
        self.ca_cay = ca_cay
        self.mo_ta = mo_ta
        # tu_choi = KHÔNG hề gửi tín hiệu nào (thiếu khoá / khoá lệch). Khác hẳn
        # "đã giết mà chưa trọn vẹn", nên phía gọi trả mã khác nhau: 10 vs 125.
        self.tu_choi = tu_choi

    @property
    def tron_ven(self) -> bool:
        return self.me_da_chet and self.ca_cay

    def __str__(self) -> str:
        return self.mo_ta


def _ten_job(run_id: str) -> str:
    """Tên Job Object cho một lượt chạy. `Local\\` = không gian tên của phiên đăng nhập.

    Có TÊN thì `stop` — chạy ở TIẾN TRÌNH KHÁC — mới mở lại được job. Không tên
    thì handle chỉ sống trong tiến trình `run`, và đó chính là khe hở #2: đường
    `stop` phải rơi về `taskkill` + ảnh chụp cha-con, tức mù với hậu duệ mồ côi.
    """
    return f"Local\\tl-launcher-{run_id}"


def _mo_job_windows(ten: str):
    """Mở lại Job Object THEO TÊN. None = không mở được (job đã mất, hoặc không phải Windows).

    Job Object biến mất khi handle CUỐI CÙNG đóng — mà cờ KILL_ON_JOB_CLOSE khiến
    lúc đó mọi thành viên bị giết luôn. Nên "mở không được" ở đây có hai nghĩa và
    cả hai đều lành: hoặc tiến trình `run` đã thoát (job đóng ⇒ cây đã bị giết),
    hoặc lượt chạy này không dựng được job. KHÔNG được đọc thành "cây đã sạch" —
    hàm gọi vẫn phải đi tiếp xuống các phép đo khác.
    """
    if platform.system() != "Windows" or not ten:
        return None
    try:
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.windll.kernel32
        k32.OpenJobObjectW.restype = wintypes.HANDLE
        job = k32.OpenJobObjectW(0x1F001F, False, ctypes.c_wchar_p(ten))  # ALL_ACCESS
        return job or None
    except (OSError, AttributeError, ValueError):
        return None


def _job_windows(pid: int, ten: str | None = None):
    """Nhốt tiến trình vào một Job Object. Trả handle, hoặc None nếu không được.

    VÌ SAO PHẢI CÓ: `taskkill /T` duyệt cây CHA-CON tại thời điểm chạy, nên một
    tiến trình mà cha đã thoát trước đó (MỒ CÔI) không nằm trong cây và sống sót
    nguyên vẹn. `_chup_cay` cũng đi đúng những liên kết ấy nên bỏ sót y hệt —
    nó chỉ nâng "tin rc=0" thành "kiểm từng pid", không phủ được ca mồ côi.
    Job Object là cơ chế DUY NHẤT trên Windows giữ được cả hậu duệ mồ côi: tiến
    trình con sinh ra đã ở trong job của cha, và ở lại đó kể cả khi cha chết.

    KHE CŨ ĐÃ KHÉP: bản trước sinh con rồi mới gán job, nên tồn tại một khoảng
    rất ngắn mà cháu sinh trong đó nằm NGOÀI job. Nay `lenh_run` sinh con ở trạng
    thái TREO (CREATE_SUSPENDED), gán job xong mới thả — con chưa chạy được một
    lệnh nào trước khi đã ở trong job, nên không còn khoảng nào để lọt. Xem
    `_thao_treo` về việc thả, và vì sao thả HỎNG thì phải giết con chứ không
    được để nó treo.
    """
    if platform.system() != "Windows":
        return None
    try:
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.windll.kernel32
        job = k32.CreateJobObjectW(None, ctypes.c_wchar_p(ten) if ten else None)
        if not job:
            return None

        class _GIOI_HAN(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64),
                        ("PerJobUserTimeLimit", ctypes.c_int64),
                        ("LimitFlags", wintypes.DWORD),
                        ("MinimumWorkingSetSize", ctypes.c_size_t),
                        ("MaximumWorkingSetSize", ctypes.c_size_t),
                        ("ActiveProcessLimit", wintypes.DWORD),
                        ("Affinity", ctypes.POINTER(ctypes.c_ulong)),
                        ("PriorityClass", wintypes.DWORD),
                        ("SchedulingClass", wintypes.DWORD)]

        class _IO(ctypes.Structure):
            _fields_ = [("ReadOperationCount", ctypes.c_uint64),
                        ("WriteOperationCount", ctypes.c_uint64),
                        ("OtherOperationCount", ctypes.c_uint64),
                        ("ReadTransferCount", ctypes.c_uint64),
                        ("WriteTransferCount", ctypes.c_uint64),
                        ("OtherTransferCount", ctypes.c_uint64)]

        class _MO_RONG(ctypes.Structure):
            _fields_ = [("BasicLimitInformation", _GIOI_HAN),
                        ("IoInfo", _IO),
                        ("ProcessMemoryLimit", ctypes.c_size_t),
                        ("JobMemoryLimit", ctypes.c_size_t),
                        ("PeakProcessMemoryUsed", ctypes.c_size_t),
                        ("PeakJobMemoryUsed", ctypes.c_size_t)]

        tt = _MO_RONG()
        tt.BasicLimitInformation.LimitFlags = 0x2000   # KILL_ON_JOB_CLOSE
        if not k32.SetInformationJobObject(job, 9, ctypes.byref(tt), ctypes.sizeof(tt)):
            k32.CloseHandle(job)
            return None
        h = k32.OpenProcess(0x1F0FFF, False, int(pid))  # PROCESS_ALL_ACCESS
        if not h:
            k32.CloseHandle(job)
            return None
        ok = k32.AssignProcessToJobObject(job, h)
        k32.CloseHandle(h)
        if not ok:
            k32.CloseHandle(job)
            return None
        return job
    except (OSError, AttributeError, ValueError):
        return None


def _thao_treo(p) -> str | None:
    """Thả tiến trình sinh ra ở trạng thái TREO. None = đã thả; chuỗi = lý do HỎNG.

    VÌ SAO PHẢI TREO RỒI THẢ (khe hở #1): gán job SAU khi con đã chạy để hở đúng
    một khoảng — ngắn, nhưng con chỉ cần sinh một cháu trong khoảng đó là cháu
    nằm ngoài job vĩnh viễn, và job là cơ chế DUY NHẤT trên Windows giữ được hậu
    duệ mồ côi. Sinh con treo thì con chưa thực thi được lệnh nào trước lúc đã ở
    trong job, nên khoảng đó không còn tồn tại.

    VÌ SAO KHÔNG DÙNG ResumeThread THẲNG: `Popen` ĐÓNG handle luồng chính ngay
    trong `_execute_child`, nên phía Python không còn thứ để thả. `NtResumeProcess`
    chỉ cần handle TIẾN TRÌNH — thứ `Popen` vẫn giữ. Nó là API không tài liệu
    nhưng ổn định lâu đời; dù vậy vẫn có đường dự phòng bằng Toolhelp bên dưới,
    vì một con TREO MÃI là hỏng nặng hơn hẳn mọi khe hở mà bản vá này khép.

    Phía gọi BẮT BUỘC phải giết con khi hàm này trả về chuỗi. Để một tiến trình
    treo sống tiếp là biến bản vá thành treo cả lượt chạy tới tận hạn chót.
    """
    if platform.system() != "Windows":
        return None
    h = getattr(p, "_handle", None)
    if not h:
        return "khong co handle tien trinh de tha treo"
    loi = ""
    try:
        import ctypes
        rc = ctypes.windll.ntdll.NtResumeProcess(ctypes.c_void_p(int(h)))
        if rc == 0:
            return None
        loi = f"NtResumeProcess NTSTATUS=0x{rc & 0xFFFFFFFF:08x}"
    except (OSError, AttributeError, ValueError) as e:
        loi = f"NtResumeProcess loi: {e}"
    try:                       # dự phòng: duyệt luồng bằng Toolhelp rồi thả từng cái
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.windll.kernel32

        class _LUONG(ctypes.Structure):
            _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
                        ("th32ThreadID", wintypes.DWORD),
                        ("th32OwnerProcessID", wintypes.DWORD),
                        ("tpBasePri", ctypes.c_long), ("tpDeltaPri", ctypes.c_long),
                        ("dwFlags", wintypes.DWORD)]

        k32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        anh = k32.CreateToolhelp32Snapshot(0x00000004, 0)   # SNAPTHREAD
        if not anh:
            return loi + "; khong chup duoc danh sach luong"
        te = _LUONG()
        te.dwSize = ctypes.sizeof(_LUONG)
        da_tha = 0
        try:
            tiep = k32.Thread32First(anh, ctypes.byref(te))
            while tiep:
                if int(te.th32OwnerProcessID) == int(p.pid):
                    ht = k32.OpenThread(0x0002, False, te.th32ThreadID)  # SUSPEND_RESUME
                    if ht:
                        if k32.ResumeThread(ht) != -1:
                            da_tha += 1
                        k32.CloseHandle(ht)
                tiep = k32.Thread32Next(anh, ctypes.byref(te))
        finally:
            k32.CloseHandle(anh)
        if da_tha:
            return None
        return loi + "; Toolhelp khong tha duoc luong nao"
    except (OSError, AttributeError, ValueError) as e:
        return f"{loi}; Toolhelp loi: {e}"


def _pid_trong_job(job) -> list[int] | None:
    """PID còn trong job. [] = đã chứng minh rỗng · None = không đọc được."""
    try:
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.windll.kernel32

        # JOBOBJECT_BASIC_PROCESS_ID_LIST là mảng độ dài biến đổi. Không đóng
        # đinh 512 PID: job lớn hơn sẽ trả ERROR_MORE_DATA; đó là tín hiệu tăng
        # buffer, không phải "job rỗng".
        suc_chua = 64
        for _ in range(8):
            class _DS(ctypes.Structure):
                _fields_ = [("NumberOfAssignedProcesses", wintypes.DWORD),
                            ("NumberOfProcessIdsInList", wintypes.DWORD),
                            ("ProcessIdList", ctypes.c_size_t * suc_chua)]

            ds = _DS()
            if k32.QueryInformationJobObject(job, 3, ctypes.byref(ds),
                                             ctypes.sizeof(ds), None):
                n = int(ds.NumberOfProcessIdsInList)
                if n > suc_chua:
                    return None
                return [int(ds.ProcessIdList[i]) for i in range(n)]
            can = int(ds.NumberOfAssignedProcesses)
            if can <= suc_chua:
                return None
            suc_chua = max(suc_chua * 2, can)
        return None
    except (OSError, AttributeError, ValueError):
        return None


def _giet_windows(pid: int, khoa=None,
                  anh: dict[int, str] | None = None, job=None) -> KetGiet:
    """Giết trên Windows: taskkill trước, rồi TerminateProcess nếu vẫn sống.

    ĐÃ ĐO (codex, 12-08-2026): `taskkill /PID x /T /F` trả rc=1 "Access denied"
    ngay cả trên tiến trình do CHÍNH mình sinh ra, trong khi `Stop-Process -Force`
    lại giết được — nghĩa là không được coi taskkill là đường duy nhất. Tệ hơn:
    bản trước trả "taskkill rc=1" mà phía gọi vẫn báo quá-hạn-đã-xử-lý, nên
    tiến trình mẹ LẪN cháu sống tiếp sau hạn chót. Đó là chốt nói dối.

    TerminateProcess qua ctypes không cần tiến trình ngoài nên không dính lớp
    quyền của taskkill.exe; đổi lại nó KHÔNG diệt con cháu, nên khi phải rơi
    xuống nhánh này ta nói thẳng là con cháu có thể còn sống.
    """
    buoc = []
    if job is not None:
        # Job Object phu duoc ca hau due MO COI, thu ma taskkill /T va anh chup
        # theo lien ket cha-con deu bo sot. Dung no TRUOC, va DOI bang chung:
        # danh sach pid trong job phai RONG.
        try:
            import ctypes
            ctypes.windll.kernel32.TerminateJobObject(job, 1)
        except (OSError, AttributeError, ValueError) as e:
            buoc.append(f"TerminateJobObject loi: {e}")
        else:
            time.sleep(0.3)
            con_job = _pid_trong_job(job)
            if con_job == []:
                return KetGiet(True, True, "job: da tat ca cay")
            if con_job:
                buoc.append(f"job con {len(con_job)} tien trinh")
            else:
                buoc.append("job: khong doc duoc danh sach pid")
    try:
        p = subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                           capture_output=True, text=True, timeout=30)
        ma_tk = p.returncode
    except (OSError, subprocess.SubprocessError):
        ma_tk = None             # treo/không chạy được: coi như /T KHÔNG chạy
    buoc.append(f"taskkill rc={ma_tk}")
    # CHỈ taskkill rc=0 mới là bằng chứng CẢ CÂY. rc khác 0 nghĩa là /T không chạy,
    # nên dù mẹ có chết (do nhánh dưới) thì con cháu vẫn CHƯA được xác nhận.
    # `taskkill /T rc=0` KHONG phai bang chung ca cay chet. Nó duyet cay CHA-CON
    # tai thoi diem chay, nen mot tien trinh mà cha đã thoat truoc do (mo coi) KHONG
    # nam trong cay do va song sot nguyen ven. Vòng 2 đã bắt đúng lớp lỗi này ở chỗ
    # khác; ở đây nó nấp sau rc=0. Nay doi bang chung tung pid tu ANH CHUP.
    if ma_tk == 0 and not _con_song(pid, khoa):
        if anh is None:
            return KetGiet(True, False, "; ".join(buoc)
                           + "; me da tat, KHONG chup duoc cay - KHONG khang dinh ca cay")
        _giet_rieng(anh, signal.SIGTERM)       # tren Windows = TerminateProcess
        time.sleep(0.3)
        con_lai = [q for q, k in anh.items() if _con_song_dung_khoa(q, k)]
        if not con_lai:
            return KetGiet(True, True, "; ".join(buoc) + "; ca cay da tat")
        return KetGiet(True, False, "; ".join(buoc)
                       + f"; con {len(con_lai)} tien trinh song {sorted(con_lai)[:5]}")
    try:
        import ctypes
        k32 = ctypes.windll.kernel32
        PROCESS_TERMINATE = 0x0001
        h = k32.OpenProcess(PROCESS_TERMINATE, False, int(pid))
        if h:
            ok = k32.TerminateProcess(h, 1)
            k32.CloseHandle(h)
            buoc.append(f"TerminateProcess ok={bool(ok)}")
        else:
            buoc.append(f"OpenProcess that bai (err={k32.GetLastError()})")
    except (OSError, AttributeError, ValueError) as e:
        buoc.append(f"ctypes loi: {e}")
    time.sleep(0.3)
    if _con_song(pid, khoa):
        return KetGiet(False, False, "; ".join(buoc) + "; KHONG GIET DUOC")
    buoc.append("me da tat NHUNG CON CHAU CHUA XAC NHAN (taskkill /T that bai)")
    return KetGiet(True, False, "; ".join(buoc))


def _giet_cay(pid: int, khoa, job=None) -> KetGiet:
    """Giết tiến trình VÀ con cháu. Trả KetGiet, KHÔNG trả chuỗi.

    Phía gọi quyết định mã thoát bằng `.tron_ven`, nên không còn cách nào để một
    câu mô tả nghe-như-thành-công lọt qua.

    `khoa` nhận MỘT khoá hoặc BỘ khoá — xem `_khop_khoa` về lý do có bộ.
    """
    ds_khoa = _ds_khoa(khoa)
    if not ds_khoa:
        return KetGiet(False, False, "tu choi giet: khong co khoa danh tinh", tu_choi=True)
    hien = _khoa_danh_tinh(pid)
    if hien is None:
        # TIẾN TRÌNH ĐÃ BIẾN MẤT — KHÔNG phải "PID bị tái dùng". Bản trước gộp hai
        # chuyện NGƯỢC NHAU vào một câu và một mã: `stop` một lượt vừa chạy xong
        # bình thường báo "PID da bi tai dung" + rc=10, tức là hô hoán đúng cái
        # mối nguy mà khoá danh tính sinh ra để bắt, trong ca vô hại và PHỔ BIẾN
        # nhất (audit vòng 3: 7/12 lần đua). Chỉ còn con cháu là đáng hỏi.
        # Mỗi nền một PHÉP ĐO cho câu hỏi "còn hậu duệ không", và cả hai chỉ kết
        # luận khi ĐO ĐƯỢC-VÀ-RỖNG (`None` = không đo được, tuyệt đối không đọc
        # thành rỗng — đó là lỗ vòng 7 vừa vá).
        # `_thanh_vien_nhom` là phép đo POSIX (nhóm tiến trình) nên trên Windows nó
        # LUÔN trả None. Hỏi mỗi nó thì Windows không bao giờ chạm được nhánh này:
        # ĐO ĐƯỢC trên windows-latest 13-08, `stop` một lượt ĐÃ KẾT THÚC rơi xuống
        # taskkill trên một PID không còn tồn tại, rc≠0, thành 125 "không giết được"
        # (t69 đỏ). Windows CÓ phép đo tương đương: ảnh chụp. `{}` nghĩa là không
        # tiến trình sống nào nhận `pid` làm tổ tiên, và `hien is None` ở trên đã
        # chứng minh chính `pid` đã tắt.
        if platform.system() == "Windows":
            # Job Object la bang chung MANH NHAT o day: no giu ca hau due MO COI,
            # dung thu ma anh chup theo lien ket cha-con bo sot (cha da thoat thi
            # chau khong con nam trong cay tinh tu `pid`). Chi lui ve anh chup khi
            # KHONG co job - luot chay cu, hoac job da dong. `None` van la khong do
            # duoc, khong bao gio doc thanh rong.
            trong_job = _pid_trong_job(job) if job is not None else None
            if trong_job is not None:
                con, rong = trong_job, (trong_job == [])
            else:
                con = _chup_cay(pid)
                rong = con == {}
        else:
            con = _thanh_vien_nhom(pid)
            rong = con == []      # [] = đã chứng minh rỗng · None = không đo được
        if rong:
            return KetGiet(True, True, "tien trinh da khong con chay")
    elif not _khop_khoa(hien, ds_khoa):
        return KetGiet(False, False,
                       "tu choi giet: khoa danh tinh KHAC (PID da bi tai dung)",
                       tu_choi=True)
    if platform.system() == "Windows":
        # Chup TRUOC khi giet: sau khi me chet, hau due mo coi khong con duong nao
        # tim lai (cung ly le nhu POSIX, xem `_chup_cay`).
        return _giet_windows(pid, ds_khoa, _chup_cay(pid), job)
    # POSIX: con được sinh với start_new_session nên pgid == pid, giết cả nhóm.
    # Ảnh chụp phải lấy TRƯỚC phát tín hiệu đầu tiên — sau đó kẻ đã setsid() là
    # không thể tìm lại (xem _chup_cay).
    anh = _chup_cay(pid)

    def _con_lai():
        """Ai còn sống: ảnh chụp (bắt cả kẻ đã rời nhóm) HỢP thành viên nhóm hiện
        tại (bắt cả kẻ sinh sau lúc chụp). None = không đo được ⇒ KHÔNG khẳng định."""
        nhom = _thanh_vien_nhom(pid)
        if nhom is None or anh is None:
            return None
        return {q for q, k in anh.items() if _con_song_dung_khoa(q, k)} | set(nhom)

    try:
        os.killpg(pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError, OSError) as e:
        return KetGiet(False, False, f"killpg SIGTERM loi: {e}")
    if anh:
        _giet_rieng(anh, signal.SIGTERM)   # killpg không với tới kẻ đã setsid()
    for _ in range(20):  # 2 giây chờ tự chết tử tế
        time.sleep(0.1)
        # KHÔNG hỏi mỗi _con_song(pid): mẹ chết KHÔNG chứng minh cháu chết. Cũng
        # không killpg(0): nhóm còn tồn tại chừng nào zombie chưa được thu hồi.
        con = _con_lai()
        if con is None:
            # Không đo được: chỉ dám khẳng định về MẸ, ca_cay=False để phía gọi
            # trả 125 chứ không nói dối bằng 124.
            if not _con_song(pid):
                return KetGiet(True, False, "SIGTERM: me da chet, KHONG do duoc cay")
            continue
        if not con:
            return KetGiet(True, True, "SIGTERM: cay da sach")
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass                       # nhóm đã sạch giữa chừng
    except OSError as e:
        return KetGiet(False, False, f"killpg SIGKILL loi: {e}")
    if anh:
        _giet_rieng(anh, signal.SIGKILL)
    time.sleep(0.3)
    # KIỂM LẠI kể cả sau SIGKILL: tiến trình ở trạng thái D (chờ I/O) không chết
    # ngay, và báo "đã tắt" lúc nó còn sống là đúng thứ lỗi vừa bắt được ở Windows.
    con = _con_lai()
    if con is None:
        return KetGiet(not _con_song(pid), False,
                       "SIGKILL: KHONG do duoc cay - KHONG khang dinh ca cay")
    if not con:
        return KetGiet(True, True, "SIGKILL: cay da sach")
    return KetGiet(pid not in con, False,
                   f"SIGKILL: con {len(con)} tien trinh song {sorted(con)[:5]}")


# -------------------------------------------------------------------- các chốt

class Chan(Exception):
    """Một chốt chặn. Mang theo mã thoát để phía gọi phân biệt được."""

    def __init__(self, ma: int, thong_diep: str):
        super().__init__(thong_diep)
        self.ma = ma
        self.thong_diep = thong_diep


def chot_workspace(ws: str) -> str:
    d = Path(ws).expanduser()
    if not d.is_dir():
        raise Chan(MA_THAM_SO, f"workspace khong phai thu muc: {ws}")
    rc, top, err = _git_mot_dong(d, "rev-parse", "--show-toplevel")
    if rc != 0 or not top:
        raise Chan(MA_GIT, f"khong doc duoc repo tai {d}: {err or 'git that bai'}")
    return str(Path(top).resolve())


# ------------------------------------------------- nhận diện kho, KHÔNG theo đường dẫn

def _danh_tinh_remote(url: str) -> str | None:
    """URL remote -> 'host/owner/repo'. Trả None nếu không đọc được.

    VÌ SAO KHÔNG SO CHUỖI THÔ: cùng một kho có ít nhất bốn cách viết —
      https://github.com/o/r.git · git@github.com:o/r · ssh://git@github.com/o/r
      · https://x-access-token:<token>@github.com/o/r
    So thô thì cùng một kho ra bốn danh tính khác nhau, và chốt thành vô dụng
    ngay khi ai đó đổi https sang ssh.

    CŨNG LÀ CHỖ RÒ BÍ MẬT: dạng thứ tư có TOKEN nằm ngay trong URL (CI, phiên
    remote hay dùng). Hàm này cắt phần `...@` TRƯỚC khi trả về, nên token không
    bao giờ đi vào stdout/JSON/sổ lượt chạy.
    """
    u = (url or "").strip()
    if not u:
        return None
    m = REMOTE_SCP_RE.match(u) or REMOTE_URL_RE.match(u)
    if not m:
        return None
    host, duong = m.group(1), m.group(2).strip("/")
    if duong.endswith(".git"):
        duong = duong[:-4]
    if not duong:
        return None
    return f"{host.lower()}/{duong}"


def _cac_remote(ws) -> list[str]:
    rc, out, _ = _git(ws, "remote", "-v")
    if rc != 0:
        return []
    ra = []
    for dong in out.splitlines():
        phan = dong.split()
        if len(phan) >= 2:
            d = _danh_tinh_remote(phan[1])
            if d and d not in ra:
                ra.append(d)
    return ra


def _commit_goc(ws) -> list[str]:
    """Commit gốc (không cha). Đây là vân tay BỀN NHẤT của một kho.

    Nó không đổi khi kho bị đổi tên, chuyển chủ, fork, thêm/bớt remote, hay khi
    clone về một đường dẫn khác — và đọc được KHÔNG CẦN MẠNG. Đường dẫn thì đổi
    theo từng máy; remote thì đổi theo cách clone; commit gốc thì không.
    """
    rc, out, _ = _git(ws, "rev-list", "--max-parents=0", "HEAD")
    if rc != 0:
        return []
    return [d.strip() for d in out.splitlines() if d.strip()]


def _kho_khop(thuc_te: str, mong_doi: str) -> bool:
    """So danh tính kho. `thuc_te` luôn dạng 'host/owner/repo'.

    LỖ AN NINH ĐÃ CÓ THẬT (codex đo, 12-08-2026): bản trước dùng
    `r.endswith("/" + can)`, nên `--expected-repo github.com/o/r` KHỚP với remote
    `https://evil.example/github.com/o/r.git`. Một kho do người khác dựng, đặt
    đúng cái tên đường dẫn đó, sẽ qua chốt — chốt nhận diện kho thành vô dụng
    đúng lúc cần nhất.

    Luật nay theo Ý ĐỊNH của người viết:
    · nêu HOST ('github.com/o/r' — đoạn đầu có dấu chấm) ⇒ đòi BẰNG NHAU tuyệt đối.
    · không nêu host ('o/r') ⇒ so N đoạn CUỐI, đúng bằng số đoạn người ta viết.
      Đây là lựa chọn của người dùng: không nói host thì không chặn theo host.
      Muốn chặt thì nêu host, hoặc dùng --expected-root-commit.

    So KHÔNG phân biệt hoa/thường: GitHub coi 'Owner/Repo' và 'owner/repo' là một
    kho, và bản trước chặn oan chính bản clone hợp lệ (codex đo: rc=11).
    """
    t = thuc_te.strip().lower().strip("/")
    m = mong_doi.strip().lower().strip("/")
    if not t or not m:
        return False
    doan_m = m.split("/")
    # Đếm ĐOẠN, không dò dấu chấm. Audit codex bắt được hai lối lách của bản trước:
    # · host không có dấu chấm ('localhost/o/r') bị coi là 'owner/repo' rồi khớp
    #   hậu tố với remote 'evil.example/localhost/o/r' — giả mạo lọt.
    # · một đoạn duy nhất ('r') cũng được nhận, nên bất kỳ chủ nào có kho tên 'r'
    #   đều khớp, dù help ghi rõ phải là owner/repo.
    if len(doan_m) >= 3:
        # ≥3 đoạn = người ta ĐÃ nêu host ⇒ đòi bằng nhau tuyệt đối.
        # KHÔNG bó ở đúng 3 (audit vòng 3): GitLab subgroup và GHE lồng nhau có
        # 4+ đoạn và LÀ danh tính hợp lệ. Bó ở 3 thì `--expected-repo
        # gitlab.com/nhom/nhom-con/kho` bị TỪ CHỐI dù đúng từng ký tự, kèm thông
        # điệp tự mâu thuẫn "mong doi X, thuc te [X]" — người đọc đi tìm lỗi ở
        # remote chứ không ở chốt. Và người dùng GitLab/GHE mất hẳn lựa chọn
        # neo-theo-host. Bằng-nhau-tuyệt-đối nên tính an ninh không đổi.
        return t == m
    if len(doan_m) != 2:
        return False                       # 1 đoạn = viết sai, KHÔNG đoán
    doan_t = t.split("/")
    return len(doan_t) > 2 and doan_t[-2:] == doan_m


def tim_workspace(chi_dinh: str | None) -> str:
    """Tìm gốc repo mà KHÔNG cần ai truyền đường dẫn tuyệt đối.

    Thứ tự: --workspace  ->  $TL_WORKSPACE  ->  thư mục hiện tại.
    Rồi luôn hỏi git `rev-parse --show-toplevel`, nên đứng ở thư mục con cũng ra
    đúng gốc. Đây là thứ chạy giống nhau ở máy bạn, máy đồng nghiệp, và container
    của phiên remote - nơi kho được clone vào một đường dẫn không ai biết trước.
    """
    goc = chi_dinh or os.environ.get("TL_WORKSPACE") or os.getcwd()
    return chot_workspace(goc)


def chot_kho(ws: str, kho_mong_doi: str | None, goc_mong_doi: str | None) -> dict:
    """Neo DANH TÍNH kho, thay cho việc neo đường dẫn."""
    remotes = _cac_remote(ws)
    goc = _commit_goc(ws)
    if kho_mong_doi:
        can = kho_mong_doi.strip().lower().rstrip("/")
        if can.endswith(".git"):
            can = can[:-4]
        khop = any(_kho_khop(r, can) for r in remotes)
        if not khop:
            raise Chan(MA_KHO, f"kho lech: mong doi {can}, thuc te {remotes or '(khong co remote)'}")
    if goc_mong_doi:
        can = goc_mong_doi.strip().lower()
        if not SHA_RE.match(can):
            raise Chan(MA_THAM_SO, f"--expected-root-commit khong phai sha40: {goc_mong_doi}")
        if can not in goc:
            raise Chan(MA_KHO, f"commit goc lech: mong doi {can}, thuc te {goc or '(khong doc duoc)'}")
    return {"remotes": remotes, "commit_goc": goc}


def chot_head(ws: str, mong_doi: str) -> str:
    rc, sha, err = _git_mot_dong(ws, "rev-parse", "HEAD")
    if rc != 0 or not SHA_RE.match(sha):
        raise Chan(MA_GIT, f"khong doc duoc HEAD (rc={rc}): {err or sha!r}")
    if mong_doi and sha != mong_doi.strip().lower():
        raise Chan(MA_HEAD, f"HEAD lech: mong doi {mong_doi}, thuc te {sha}")
    return sha


def chot_ref(ws: str, mong_doi: str | None) -> str:
    rc, ref, err = _git_mot_dong(ws, "rev-parse", "--abbrev-ref", "HEAD")
    if rc != 0 or not ref:
        raise Chan(MA_GIT, f"khong doc duoc ref (rc={rc}): {err}")
    if mong_doi and ref != mong_doi.strip():
        raise Chan(MA_REF, f"ref lech: mong doi {mong_doi}, thuc te {ref}")
    return ref


def chot_sach(ws: str, bat_buoc: bool) -> str:
    rc, out, err = _git(ws, "status", "--porcelain=v1", "--untracked-files=all")
    if rc != 0:
        raise Chan(MA_GIT, f"khong doc duoc trang thai worktree (rc={rc}): {err.strip()}")
    ban = out.strip()
    if bat_buoc and ban:
        so = len(ban.splitlines())
        raise Chan(MA_BAN, f"worktree KHONG sach ({so} muc) - tu choi chay mo ho")
    return ban


def chot_prompt(duong: str | None, sha_mong_doi: str | None) -> str | None:
    """Neo prompt: tệp phải có, không rỗng, và sha256 phải khớp.

    Rỗng bị chặn riêng: một tệp prompt rỗng vẫn có sha256 hợp lệ, nên chỉ so sha
    thì "gửi prompt rỗng" là một lượt chạy hợp lệ về hình thức mà vô nghĩa thật.
    """
    if duong is None and sha_mong_doi is None:
        return None
    if duong is None or sha_mong_doi is None:
        raise Chan(MA_THAM_SO, "phai co CA --prompt-file lan --expected-prompt-sha256")
    p = Path(duong).expanduser()
    if not p.is_file():
        raise Chan(MA_PROMPT, f"khong thay tep prompt: {p}")
    b = p.read_bytes()
    if not b.strip():
        raise Chan(MA_PROMPT, f"tep prompt RONG: {p}")
    sha = hashlib.sha256(b).hexdigest()
    md = sha_mong_doi.strip().lower()
    if not SHA256_RE.match(md):
        raise Chan(MA_THAM_SO, f"--expected-prompt-sha256 khong phai sha256: {sha_mong_doi}")
    if sha != md:
        raise Chan(MA_PROMPT, f"prompt lech: mong doi {md}, thuc te {sha}")
    return sha


def chot_han(han: str | None) -> datetime | None:
    if not han:
        return None
    d = _doc_iso(han)
    if d is None:
        raise Chan(MA_THAM_SO, f"--deadline-utc khong doc duoc: {han}")
    if d <= _bay_gio():
        raise Chan(MA_HAN, f"han chot da qua: {d.isoformat()}")
    return d


def chay_cac_chot(a) -> dict:
    ws = tim_workspace(a.workspace)
    kho = chot_kho(ws, a.expected_repo, a.expected_root_commit)
    head = chot_head(ws, a.expected_head)
    ref = chot_ref(ws, a.expected_ref)
    ban = chot_sach(ws, bool(a.require_clean))
    sha_prompt = chot_prompt(a.prompt_file, a.expected_prompt_sha256)
    han = chot_han(a.deadline_utc)
    return {
        "workspace": ws, "head": head, "ref": ref, **kho,
        "worktree_sach": (ban == ""),
        "so_muc_ban": (0 if not ban else len(ban.splitlines())),
        "prompt_sha256": sha_prompt,
        "deadline_utc": (han.isoformat() if han else None),
    }


# ----------------------------------------------------------------- sổ lượt chạy

def _cap_id(run_root: Path) -> tuple[str, str]:
    """run_id đầy đủ + short_id 8 ký tự, ĐẢM BẢO chưa từng dùng trong run_root.

    Không tin "8 hex thì khó trùng": kho lượt chạy sống lâu, và một short_id trùng
    làm mọi lệnh status/stop trỏ nhầm lượt. Thà thử lại vài lần rồi bỏ cuộc.
    """
    try:
        run_root.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        # --run-root không ghi được: nói ra bằng mã thoát, đừng để traceback thô
        # rơi ra ngoài (audit codex: PermissionError WinError 5 lộ nguyên stack).
        raise Chan(MA_THAM_SO, f"khong dung duoc --run-root {run_root}: {e}") from None
    # Dọn tệp tạm mồ côi TOÀN run_root. Tên tạm riêng theo writer nên không bao
    # giờ bị ghi đè (khác tên cố định cũ vốn tự lành), và writer bị SIGKILL giữa
    # `write_text` và `os.replace` để lại rác vĩnh viễn. Phải quét từ run_root:
    # rác nằm trong thư mục của lượt ĐÃ CHẾT, mà lượt đó không ai ghi lại nữa.
    # Ban chup prompt cung quet o day: xem chu thich `cay_da_chet` trong lenh_run.
    # Khong the giu mot tep chua NOI DUNG PROMPT tren dia vo thoi han chi vi nen
    # do khong do duoc nhom tien trinh.
    try:
        for mau in ("*/run.json.*.tmp", "*/prompt.snapshot"):
            for cu in run_root.glob(mau):
                try:
                    if time.time() - cu.stat().st_mtime > 86400:
                        cu.unlink()
                except OSError:
                    pass
    except OSError:
        pass

    for _ in range(64):
        rid = uuid.uuid4().hex
        sid = rid[:8]
        da_co = {p.name.split("-", 1)[0] for p in run_root.iterdir() if p.is_dir()}
        if sid in da_co:
            continue
        # Thư mục lượt chạy tên ĐÚNG BẰNG short_id, nên `mkdir` không exist_ok
        # CHÍNH LÀ hành vi giành short_id, nguyên tử ở tầng hệ tệp.
        #
        # ĐÃ TRẢ GIÁ HAI LẦN. Bản đầu "quét rồi mkdir" có khe hở giữa hai bước.
        # Bản vá vòng 2 đổi sang mkdir độc quyền và ghi rằng khe hở đã đóng —
        # NHƯNG KHÔNG: lúc đó thư mục tên "{sid}-{rid}", nên mkdir chỉ chặn
        # trùng run_id ĐẦY ĐỦ (uuid4, 2^128 — chưa ai lo). Trùng short_id, thứ
        # làm status/stop trỏ NHẦM lượt, vẫn lọt vì hai bên ra hai tên KHÁC
        # nhau và cả hai mkdir đều thành công (audit vòng 3 ép được bằng cách
        # cho hai luồng quét xong rồi mới mkdir). Bỏ rid khỏi TÊN là sửa ở
        # tầng: không còn cách nào để hai lượt cùng sid cùng tồn tại.
        # run_id đầy đủ vẫn nằm trong run.json và `_tim_luot` vẫn tra được.
        thu_muc = run_root / sid
        try:
            thu_muc.mkdir(parents=False)
        except FileExistsError:
            continue
        except OSError as e:
            raise Chan(MA_THAM_SO, f"khong tao duoc thu muc luot chay: {e}") from None
        return rid, sid
    raise Chan(MA_VA_CHAM, "khong cap duoc short_id khong trung sau 64 lan thu")


def _tom_tat_lenh(lenh: list) -> dict:
    """Tóm tắt lệnh con để ghi sổ — KHÔNG lưu đối số nguyên văn.

    Audit codex: `list(a.lenh)` vào run.json nghĩa là token, API key hay cả prompt
    truyền qua dòng lệnh sẽ nằm lại lâu dài trong sổ, ở một tệp không ai coi là
    chỗ chứa bí mật. Giữ đủ để truy vết (chương trình gì, bao nhiêu đối số) và một
    vân tay để đối chiếu hai lượt chạy có cùng lệnh không — nhưng không phơi nội dung.
    """
    lenh = [str(x) for x in (lenh or [])]
    if not lenh:
        return {"chuong_trinh": None, "so_doi_so": 0, "van_tay": None}
    return {
        "chuong_trinh": Path(lenh[0]).name,
        "so_doi_so": len(lenh) - 1,
        "van_tay": hashlib.sha256("\x00".join(lenh).encode("utf-8")).hexdigest()[:16],
    }


def _ghi_so(thu_muc: Path, ban_ghi: dict) -> None:
    """Ghi sổ NGUYÊN TỬ: ghi tệp tạm rồi đổi tên.

    Người đọc có thể là phiên khác / điện thoại đang poll; đọc trúng lúc ghi dở sẽ
    thấy JSON cụt. os.replace là nguyên tử trên cả POSIX lẫn Windows.
    """
    thu_muc.mkdir(parents=True, exist_ok=True)
    # Tên tệp tạm phải RIÊNG cho từng người ghi. Dùng chung "run.json.tmp" thì hai
    # tiến trình cùng ghi sẽ đụng nhau — trên Windows là PermissionError WinError 32
    # ngay vòng đầu (audit codex đo được khi stress hai writer).
    tam = thu_muc / f"run.json.{os.getpid()}.{uuid.uuid4().hex[:8]}.tmp"
    try:
        tam.write_text(json.dumps(ban_ghi, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tam, thu_muc / "run.json")
    finally:
        try:
            tam.unlink()
        except OSError:
            pass


def _doc_so(thu_muc: Path) -> dict | None:
    f = thu_muc / "run.json"
    if not f.is_file():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _tim_luot(run_root: Path, dinh_danh: str) -> Path | None:
    """Tìm theo run_id đầy đủ HOẶC short_id.

    Tên thư mục CHỈ là short_id (xem `_cap_id`), nên run_id đầy đủ phải tra
    trong sổ. Thử khớp tên trước để không phải đọc mọi run.json cho ca thường.
    """
    if not run_root.is_dir():
        return None
    ds = [p for p in sorted(run_root.iterdir()) if p.is_dir()]
    for p in ds:
        if p.name == dinh_danh:
            return p
    for p in ds:
        so = _doc_so(p)
        if so and dinh_danh == so.get("run_id"):
            return p
    return None


# -------------------------------------------------------------------- lệnh chạy

def lenh_check(a) -> int:
    kq = chay_cac_chot(a)
    if a.json:
        print(json.dumps({"ok": True, "version": VERSION, **kq}, ensure_ascii=False))
    else:
        print(f"workspace : {kq['workspace']}")
        print(f"kho       : {', '.join(kq['remotes']) or '(khong co remote)'}")
        print(f"commit goc: {', '.join(c[:7] for c in kq['commit_goc']) or '(khong doc duoc)'}")
        print(f"HEAD      : {kq['head']}")
        print(f"ref       : {kq['ref']}")
        print(f"worktree  : {'sach' if kq['worktree_sach'] else str(kq['so_muc_ban']) + ' muc ban'}")
        if kq["prompt_sha256"]:
            print(f"prompt    : {kq['prompt_sha256']}")
        if kq["deadline_utc"]:
            print(f"han chot  : {kq['deadline_utc']}")
        print("KET LUAN  : QUA HET CHOT")
    return MA_OK


def lenh_run(a) -> int:
    if not a.lenh:
        raise Chan(MA_THAM_SO, "thieu lenh de chay (dat sau dau --)")
    kq = chay_cac_chot(a)
    # resolve() BẮT BUỘC, không phải cho đẹp: con được sinh với cwd=gốc repo, còn
    # launcher có thể đang đứng ở THƯ MỤC CON (tim_workspace quảng cáo đúng điều
    # đó). Với --run-root TƯƠNG ĐỐI, đường dẫn bản chụp thay vào {PROMPT_FILE} là
    # tương đối theo cwd của LAUNCHER nhưng con lại đọc theo cwd của NÓ ⇒ con
    # không thấy tệp. Audit vòng 3 đo được: sổ ghi prompt_kin_hoan_toan=True,
    # con in "No such file or directory", mà lượt chạy vẫn trả rc=0 và "xong" —
    # neo prompt fail-OPEN kèm một lời khẳng định SAI trong sổ.
    run_root = Path(a.run_root).expanduser().resolve()
    rid, sid = _cap_id(run_root)   # _cap_id đã TẠO thư mục (giành chỗ nguyên tử)
    thu_muc = run_root / sid       # tên = short_id: xem `_cap_id`

    ban_ghi = {
        "version": VERSION, "run_id": rid, "short_id": sid,
        "ten": a.name, "lenh": _tom_tat_lenh(a.lenh), "trang_thai": "dang_chay",
        "bat_dau_utc": _bay_gio().isoformat(), "ket_thuc_utc": None,
        "ma_thoat": None, "ly_do_dung": None, "pid": None, "khoa_danh_tinh": None,
        **kq,
    }
    _ghi_so(thu_muc, ban_ghi)

    # --- TOCTOU của prompt. Audit codex đo được: hash xong rồi con vẫn MỞ LẠI
    # đường dẫn gốc, nên đổi nội dung tệp giữa hai thời điểm là qua mặt được neo.
    # Hai lớp: (1) hash LẠI ngay trước khi sinh con — khép cửa sổ giữa kiểm và chạy;
    # (2) nếu lệnh có {PROMPT_FILE} thì con đọc BẢN CHỤP bất biến trong thư mục lượt
    # chạy, khép hẳn cửa sổ SAU khi sinh con. Không dùng {PROMPT_FILE} thì lớp (2)
    # không có — và điều đó được nói thẳng trong sổ, không giả vờ là đã kín.
    lenh_con = [str(x) for x in a.lenh]
    if kq.get("prompt_sha256"):
        b = Path(a.prompt_file).expanduser().read_bytes()
        if hashlib.sha256(b).hexdigest() != kq["prompt_sha256"]:
            raise Chan(MA_PROMPT, "prompt DOI giua luc kiem va luc chay")
        ban_chup = thu_muc / "prompt.snapshot"
        # 0600 NGAY TỪ LÚC TẠO. `write_bytes` để lại 0644 theo umask, tức là MỌI
        # user đọc được — mà prompt là thứ có thể chứa bí mật, chính vì thế
        # `_tom_tat_lenh` đã bỏ argv ra khỏi sổ. Bỏ argv (phù du) rồi ghi toàn văn
        # prompt ra đĩa world-readable VĨNH VIỄN là mở rộng bề mặt lộ, không phải
        # thu hẹp (audit vòng 3). Thư mục cũng siết 0700.
        _fd = os.open(ban_chup, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(_fd, "wb") as _f:
            _f.write(b)
        try:
            os.chmod(thu_muc, 0o700)
        except OSError:
            pass                 # Windows/ổ lạ không chỉnh được: không phải lý do dừng
        ban_ghi["prompt_ban_chup"] = str(ban_chup)
        if any("{PROMPT_FILE}" in x for x in lenh_con):
            lenh_con = [x.replace("{PROMPT_FILE}", str(ban_chup)) for x in lenh_con]
            ban_ghi["prompt_kin_hoan_toan"] = True
        else:
            ban_ghi["prompt_kin_hoan_toan"] = False
        _ghi_so(thu_muc, ban_ghi)
    elif any("{PROMPT_FILE}" in x for x in lenh_con):
        # Có chỗ thay mà không có gì để thay: con nhận CHUỖI NGUYÊN VĂN
        # "{PROMPT_FILE}" làm đường dẫn, rc=0, sổ ghi "xong" — người vận hành tin
        # prompt đã được neo còn agent nhận một đường dẫn vô nghĩa. Im lặng ở đây
        # là fail-open, nên chặn hẳn.
        raise Chan(MA_THAM_SO,
                   "lenh co {PROMPT_FILE} nhung khong truyen --prompt-file: "
                   "con se nhan chuoi nguyen van")

    f_out = (thu_muc / "stdout.log").open("w", encoding="utf-8")
    f_err = (thu_muc / "stderr.log").open("w", encoding="utf-8")
    them = {}
    if platform.system() == "Windows":
        # CREATE_SUSPENDED: con dung yen cho toi khi da nam trong Job Object. Day
        # la ca noi dung ban va khe ho #1 - xem `_job_windows` va `_thao_treo`.
        them["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | CREATE_SUSPENDED
    else:
        # nhóm tiến trình riêng: điều kiện CẦN để giết được cả con cháu sau này
        them["start_new_session"] = True
    try:
        p = subprocess.Popen(lenh_con, cwd=kq["workspace"],
                             stdout=f_out, stderr=f_err, stdin=subprocess.DEVNULL, **them)
    except (OSError, ValueError) as e:
        ban_ghi.update(trang_thai="hong", ly_do_dung=f"khong chay duoc lenh: {e}",
                       ket_thuc_utc=_bay_gio().isoformat())
        _ghi_so(thu_muc, ban_ghi)
        f_out.close(); f_err.close()
        raise Chan(MA_THAM_SO, f"khong chay duoc lenh: {e}")

    # Nhot con vao Job Object TRUOC KHI no chay duoc lenh nao (con dang TREO): chi
    # co job giu duoc hau due mo coi tren Windows (xem `_job_windows`). Job co TEN
    # de `stop` - chay o tien trinh khac - mo lai duoc (khe ho #2).
    # Tren POSIX ca hai ham deu tra None/khong lam gi.
    ten_job = _ten_job(rid)
    job = _job_windows(p.pid, ten_job)
    # Khoa danh tinh doc NGAY, TRUOC khi tha treo: con dang treo thi chac chan
    # chua thoat, nen day la thoi diem duy nhat ca hai nguon deu chac chan doc duoc.
    khoa_cim = _khoa_danh_tinh(p.pid)
    khoa_handle = _khoa_tu_handle(p)
    loi_tha = _thao_treo(p)
    if loi_tha:
        # Con dang TREO ma khong tha duoc: khong duoc de no song: no se treo cho
        # toi han chot roi bao "qua han", tuc bao sai nguyen nhan. Giet ngay va noi
        # thang la KHONG CHAY DUOC LENH - cung ho voi nhanh Popen hong o tren.
        try:
            p.kill()
        except OSError:
            pass
        ban_ghi.update(trang_thai="hong", pid=p.pid,
                       ly_do_dung=f"khong tha duoc tien trinh treo: {loi_tha}",
                       ket_thuc_utc=_bay_gio().isoformat())
        _ghi_so(thu_muc, ban_ghi)
        f_out.close(); f_err.close()
        raise Chan(MA_THAM_SO, f"khong chay duoc lenh: khong tha duoc tien trinh treo: {loi_tha}")

    # GHI CA HAI khoa. `_khop_khoa` chap nhan khop bat ky - nen mot sai sot trong
    # phep quy doi epoch cua `_khoa_tu_handle` khong the bien chot thanh "luon tu
    # choi giet", ma chi lam thua mot khoa khong ai khop. Xem `_khop_khoa`.
    ds_khoa = [k for k in (khoa_cim, khoa_handle) if k]
    khoa = ds_khoa[0] if ds_khoa else None
    ban_ghi.update(pid=p.pid, khoa_danh_tinh=khoa)
    if platform.system() == "Windows":
        ban_ghi["job_windows"] = job is not None
        ban_ghi["job_ten"] = ten_job if job is not None else None
        ban_ghi["khoa_danh_tinh_ds"] = ds_khoa
        ban_ghi["khoa_nguon"] = ("ca hai" if khoa_cim and khoa_handle
                                 else "cim" if khoa_cim
                                 else "handle" if khoa_handle else None)
        # PHEP DO, khong phai loi: hai nguon doc lap cung noi ve MOT thoi diem khoi
        # dong thi phai ra cung mot chuoi. Ghi ket qua so sanh de lan sau khong ai
        # phai doan - `t85` tren Windows that doc dung truong nay.
        ban_ghi["khoa_hai_nguon"] = ("khop" if khoa_cim and khoa_cim == khoa_handle
                                     else "lech" if khoa_cim and khoa_handle
                                     else "khong du hai nguon")
    if khoa is None:
        # Nói RÕ vì sao thiếu, đừng để phía đọc phải đoán. Con thoát quá nhanh là
        # ca lành; không lấy được khoá cho một tiến trình CÒN SỐNG mới là ca đáng lo.
        ban_ghi["khoa_thieu_ly_do"] = ("con da thoat truoc khi lay duoc khoa"
                                       if p.poll() is not None
                                       else "khong doc duoc danh tinh du tien trinh con song")
    _ghi_so(thu_muc, ban_ghi)
    if not a.json:
        print(f"short_id  : {sid}")
        print(f"run_id    : {rid}")
        print(f"so        : {thu_muc}")

    han = _doc_iso(kq["deadline_utc"]) if kq["deadline_utc"] else None
    qua_han = False
    bi_ngat = False
    try:
        if han is None:
            ma = p.wait()
        else:
            con_lai = (han - _bay_gio()).total_seconds()
            try:
                ma = p.wait(timeout=max(0.0, con_lai))
            except subprocess.TimeoutExpired:
                qua_han = True
                ket_giet = _giet_cay(p.pid, ds_khoa, job)
                ban_ghi["ly_do_dung"] = "qua han: " + ket_giet.mo_ta
                ban_ghi["giet_tron_ven"] = ket_giet.tron_ven
                # 124 CHỈ khi cả cây đã chết. Mẹ chết mà cháu chưa xác nhận vẫn là
                # 125: có tiến trình mồ côi đang ghi tiếp vào workspace.
                ma = MA_QUA_HAN if ket_giet.tron_ven else MA_GIET_HUT
                try:
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
    except KeyboardInterrupt:
        ban_ghi["ly_do_dung"] = "bi ngat: " + _giet_cay(p.pid, ds_khoa, job).mo_ta
        bi_ngat = True
        ma = 130
    finally:
        f_out.close()
        f_err.close()

    if khoa is None and qua_han:
        # không giết được vì không có khoá: nói thẳng, đừng báo "đã dừng"
        ma = MA_DANH_TINH

    # Mã thoát của tiến trình con có thể nằm ngoài 0..255 (Windows trả -1 =
    # 4294967295). Trả thẳng ra thì bị cắt còn 255 hoặc 0 - phía gọi đọc nhầm
    # "hỏng" thành "xong". Giữ số THẬT trong sổ, trả ra một mã hợp lệ.
    ma_that = ma
    if not isinstance(ma, int) or not (0 <= ma <= 255):
        ban_ghi["ma_thoat_that"] = ma
        ma = 1

    # Có thể `stop` đã ghi "da_dung" trong lúc ta còn chờ. Đừng đè lên quyết định
    # đó: ĐÃ ĐO (codex) - stop ghi da_dung xong runner ghi đè thành "xong", nên
    # sổ nói lượt chạy kết thúc bình thường trong khi thực tế nó bị dừng.
    so_moi = _doc_so(thu_muc) or {}
    if so_moi.get("trang_thai") == "da_dung":
        ban_ghi["trang_thai"] = "da_dung"
        ban_ghi["ly_do_dung"] = so_moi.get("ly_do_dung") or ban_ghi.get("ly_do_dung")
    else:
        # "xong" nghĩa là CHẠY HẾT. Bản trước để Ctrl-C rơi vào nhánh này: lượt
        # chạy bị ngắt giữa chừng và con bị giết, mà `trang_thai` — đúng trường
        # `status` liệt kê — nói là kết thúc bình thường. Cùng lớp lỗi với t50.
        ban_ghi["trang_thai"] = ("bi_ngat" if bi_ngat
                                 else "qua_han" if qua_han else "xong")
    # Wrapper thoát KHÔNG có nghĩa bản chụp đã hết việc: nó có thể vừa
    # sinh cháu, và cháu mới là người mở {PROMPT_FILE}. Xoá ngay khi p.wait()
    # trả về tạo một TOCTOU do chính launcher gây ra: sổ báo xong/rc=0
    # nhưng agent đọc trễ nhận ENOENT. Chỉ xoá khi đã CHỨNG MINH nhóm
    # tiến trình rỗng. Không đo được hoặc còn hậu duệ thì giữ bản 0600;
    # làm hỏng lần đọc tệ hơn việc tạm giữ một tệp kín cho tiến trình còn sống.
    # `== []` chu khong `not ...`: [] la DA CHUNG MINH rong, None la KHONG DO
    # DUOC. Tren Windows (va moi nen khong phai Linux/Darwin) _thanh_vien_nhom
    # luon tra None, nen o do dieu kien nay LUON sai va ban chup KHONG BAO GIO
    # bi xoa ngay. Do la lua chon co y (hong lan doc te hon giu mot tep kin),
    # nhung "khong xoa ngay" KHONG duoc thanh "nam lai vinh vien": `_cap_id`
    # quet don ban chup qua han o moi luot chay moi.
    cay_da_chet = (_thanh_vien_nhom(p.pid) == [])
    if (ban_ghi.get("prompt_ban_chup") and not a.giu_ban_chup
            and cay_da_chet):
        try:
            Path(ban_ghi["prompt_ban_chup"]).unlink()
            ban_ghi["prompt_ban_chup_da_xoa"] = True
        except OSError:
            pass
    ban_ghi.update(ket_thuc_utc=_bay_gio().isoformat(), ma_thoat=ma_that)
    _ghi_so(thu_muc, ban_ghi)
    if a.json:
        print(json.dumps(ban_ghi, ensure_ascii=False))
    else:
        print(f"trang thai: {ban_ghi['trang_thai']}  ma_thoat={ma}")
        if ban_ghi["ly_do_dung"]:
            print(f"ly do     : {ban_ghi['ly_do_dung']}")
    return ma


def lenh_status(a) -> int:
    run_root = Path(a.run_root).expanduser().resolve()   # xem lenh_run
    if a.id:
        thu_muc = _tim_luot(run_root, a.id)
        if thu_muc is None:
            raise Chan(MA_THAM_SO, f"khong thay luot chay: {a.id}")
        so = _doc_so(thu_muc)
        if so is None:
            raise Chan(MA_THAM_SO, f"so luot chay hong: {thu_muc}")
        _in_an_toan(json.dumps(so, ensure_ascii=False, indent=2))
        return MA_OK
    ds = []
    hong = False
    if run_root.is_dir():
        for p in sorted(run_root.iterdir()):
            if not p.is_dir():
                continue
            so = _doc_so(p)
            if so:
                ds.append({k: so.get(k) for k in
                           ("short_id", "ten", "trang_thai", "ma_thoat", "bat_dau_utc")})
            elif (p / "run.json").exists():
                # Sổ hỏng mà im lặng bỏ qua là fail-open: danh sách rỗng trông
                # hệt như "không có lượt nào". Nói ra, và trả mã khác 0.
                ds.append({"thu_muc": p.name, "loi": "run.json khong doc duoc"})
                hong = True
    _in_an_toan(json.dumps(ds, ensure_ascii=False, indent=2))
    return MA_THAM_SO if hong else MA_OK


def lenh_stop(a) -> int:
    run_root = Path(a.run_root).expanduser().resolve()   # xem lenh_run
    thu_muc = _tim_luot(run_root, a.id)
    if thu_muc is None:
        raise Chan(MA_THAM_SO, f"khong thay luot chay: {a.id}")
    so = _doc_so(thu_muc)
    if so is None:
        raise Chan(MA_THAM_SO, f"so luot chay hong: {thu_muc}")
    pid, khoa = so.get("pid"), so.get("khoa_danh_tinh")
    # Bộ khoá đầy đủ nếu sổ có (Windows ghi cả hai nguồn); nếu không thì khoá đơn.
    # Đọc bằng `or` để sổ CŨ — chỉ có `khoa_danh_tinh` — vẫn chạy y như trước.
    ds_khoa = _ds_khoa(so.get("khoa_danh_tinh_ds") or khoa)
    if not pid:
        raise Chan(MA_THAM_SO, "so khong co pid")
    if not ds_khoa:
        # KHÔNG nới thành "đã xong thì trả OK": thiếu khoá nghĩa là KHÔNG ĐO ĐƯỢC
        # gì cả, kể cả việc con cháu đã chết hay chưa. Trên Linux `stop` trả 0 cho
        # lượt đã xong là vì `_giet_cay` ĐO được tiến trình đã biến mất, không phải
        # vì suy ra từ nhãn trong sổ. Vòng 5 đã thử nới chỗ này và nó đụng thẳng
        # t32 — đúng ra thì t32 mới là bên giữ doctrine.
        print("KET LUAN  : TU CHOI - khong co khoa danh tinh, khong giet theo PID tran")
        return MA_DANH_TINH
    # VẪN chạy _giet_cay kể cả khi sổ nói đã kết thúc: nhãn có thể cũ, và chốt
    # danh tính phải được hỏi (t31). Chỉ KHÔNG đổi nhãn của một lượt đã kết thúc —
    # bản trước ghi đè trang_thai="da_dung" lên lượt vừa "xong" bình thường, tức
    # sổ nói nó bị dừng trong khi nó chạy hết. Đúng lớp lỗi mà t50 khoá ở chiều
    # ngược lại (runner đè lên quyết định của stop); chiều này bị bỏ sót.
    # Mở lại Job Object THEO TÊN. Đây là khe hở #2 của đợt trước: handle job chỉ
    # sống trong tiến trình `run`, nên `stop` — tiến trình KHÁC — không với tới,
    # phải rơi về `taskkill` + ảnh chụp cha-con và mù với hậu duệ MỒ CÔI. Tên nằm
    # trong sổ nên mở lại được; mở không được thì `job=None` và đường cũ vẫn chạy.
    job = _mo_job_windows(so.get("job_ten") or "")
    ket = _giet_cay(int(pid), ds_khoa, job)
    if so.get("trang_thai") in TRANG_THAI_KET_THUC:
        print(f"KET LUAN  : luot chay da ket thuc tu truoc "
              f"(trang_thai={so['trang_thai']}); {ket.mo_ta}")
    else:
        so.update(trang_thai="da_dung", ly_do_dung=ket.mo_ta,
                  giet_tron_ven=ket.tron_ven, ket_thuc_utc=_bay_gio().isoformat())
        _ghi_so(thu_muc, so)
        print(f"KET LUAN  : {ket.mo_ta}")
    if ket.tron_ven:
        return MA_OK
    # TỪ CHỐI giết (10) KHÁC đã-giết-mà-chưa-trọn-vẹn (125). Bản trước trả 10 cho
    # cả hai, nên một cảnh báo "còn tiến trình mồ côi" đọc y hệt "không có khoá".
    return MA_DANH_TINH if ket.tu_choi else MA_GIET_HUT


# ------------------------------------------------------------ kiểm công cụ môi trường

# Vì sao có `doctor`: cùng một lệnh phải chạy được ở máy Windows của người dùng,
# ở máy macOS/Linux, và trong container của phiên remote — mà ba nơi đó KHÔNG có
# cùng bộ công cụ. Container Claude Code trên web ĐÃ ĐO ngày 12-08-2026: có
# python/git/node/claude, KHÔNG có codex, gh, pwsh. Thiếu công cụ mà chỉ lộ ra
# giữa chừng thì lượt chạy hỏng ở chỗ khó đọc; hỏi trước thì hỏng ở chỗ dễ đọc.
#
# Bảng này KHÔNG cài gì cả — nó chỉ đo và chỉ ra lệnh cài chính thức. Việc cài do
# hook phiên (.claude/hooks/session-start.sh) hoặc do người dùng làm.
CONG_CU = [
    {"ten": "git", "bat_buoc": True, "ung_vien": ["git"],
     "vi_sao": "moi chot neo HEAD/ref/worktree deu qua git",
     "cai": {"Windows": "winget install --id Git.Git -e",
             "Darwin": "xcode-select --install  (hoac: brew install git)",
             "Linux": "sudo apt-get install -y git"}},
    {"ten": "python", "bat_buoc": True, "ung_vien": ["python3", "python", "py"],
     "vi_sao": "chinh launcher nay chay bang python",
     # Windows KHONG co lenh `python3` (chi `python` va `py`) - dung doi tai lieu
     # bat nguoi ta cai them mot bi danh; nhan CA BA ten la du.
     "cai": {"Windows": "winget install --id Python.Python.3.12 -e",
             "Darwin": "brew install python@3.12",
             "Linux": "sudo apt-get install -y python3"}},
    {"ten": "claude", "bat_buoc": False, "ung_vien": ["claude"],
     "vi_sao": "CLI chinh thuc de goi phien Claude (khong tu viet script spawn)",
     "cai": {"*": "npm install -g @anthropic-ai/claude-code"}},
    {"ten": "codex", "bat_buoc": False, "ung_vien": ["codex"],
     "vi_sao": "CLI chinh thuc de goi phien Codex (khong tu viet script spawn)",
     "cai": {"*": "npm install -g @openai/codex"}},
    # rg (ripgrep): codex và Claude Code đều gọi nó để tìm trong mã. Nhanh hơn
    # grep nhiều lần, tôn trọng .gitignore, và đọc UTF-8 đúng — quan trọng với kho
    # tiếng Việt, nơi `findstr` của Windows đọc sai dấu. Không bắt buộc vì mọi chốt
    # trong tệp này chạy được khi thiếu nó; chỉ là công cụ tra cứu bị chậm và mù hơn.
    {"ten": "rg", "bat_buoc": False, "ung_vien": ["rg"],
     "vi_sao": "tim trong ma - codex/Claude Code goi rg; findstr doc sai dau tieng Viet",
     "cai": {"Windows": "winget install --id BurntSushi.ripgrep.MSVC -e",
             "Darwin": "brew install ripgrep",
             "Linux": "sudo apt-get install -y ripgrep"}},
    # bash: `.claude/settings.json` gọi hook qua bash và session-start.sh là bash
    # script. Máy Windows KHÔNG có Git Bash thì hook hỏng, mà doctor cũ vẫn in
    # "DU CONG CU BAT BUOC" — đo thiếu đúng chỗ môi trường phụ thuộc (audit vòng 3).
    {"ten": "bash", "bat_buoc": False, "ung_vien": ["bash"],
     "vi_sao": "hook SessionStart la bash script; Windows can Git Bash",
     "cai": {"Windows": "winget install --id Git.Git -e  (kem Git Bash)",
             "Darwin": "co san", "Linux": "sudo apt-get install -y bash"}},
    # npm: session-start.sh rẽ nhánh trên `co npm`, không phải trên `node`.
    {"ten": "npm", "bat_buoc": False, "ung_vien": ["npm"],
     "vi_sao": "hook cai hai CLI agent bang npm; co node chua chac co npm",
     "cai": {"Windows": "winget install --id OpenJS.NodeJS.LTS -e",
             "Darwin": "brew install node", "Linux": "sudo apt-get install -y npm"}},
    {"ten": "node", "bat_buoc": False, "ung_vien": ["node"],
     "vi_sao": "can de cai hai CLI tren",
     "cai": {"Windows": "winget install --id OpenJS.NodeJS.LTS -e",
             "Darwin": "brew install node", "Linux": "sudo apt-get install -y nodejs npm"}},
]


def _phien_ban(duong_dan: str) -> tuple[bool, str]:
    """Chạy thử `--version`. Trả (chay_duoc, dong_dau).

    `shutil.which()` KHÔNG phải bằng chứng công cụ dùng được — audit codex dựng hai
    tệp RỖNG tên git.exe/python.exe rồi doctor báo xanh; và ngay trên máy đó `rg.exe`
    có trong PATH nhưng chạy ra "Access is denied". Có mặt ≠ chạy được.
    """
    try:
        p = subprocess.run([duong_dan, "--version"], capture_output=True, text=True,
                           timeout=15, encoding="utf-8", errors="replace")
    except (OSError, subprocess.SubprocessError):
        return (False, "")
    ra = (p.stdout or "") + (p.stderr or "")   # nhiều CLI in phiên bản ra stderr
    dong = [d.strip() for d in ra.splitlines() if d.strip()]
    if p.returncode != 0 or not dong:
        return (False, dong[0][:80] if dong else f"rc={p.returncode}, khong in gi")
    return (True, dong[0][:80])


def _in_an_toan(chuoi: str) -> bool:
    """In một dòng; ống bị đóng thì thôi, KHÔNG đổi kết luận đã tính xong.

    Audit vòng 3: `main` bắt BrokenPipeError rồi trả 141, nên `doctor | head`
    trên môi trường LÀNH cũng ra 141 (20/20 lượt) — phía gọi kiểm `rc != 0` vẫn
    báo "THIEU CONG CU" oan, đúng triệu chứng mà bản vá trước định dẹp; còn lúc
    THIẾU công cụ thì 141 lại nuốt mất mã 12. Mã thoát phải là kết luận, không
    phải chuyện người đọc có chịu đọc hết hay không.
    """
    try:
        print(chuoi)
        return True
    except BrokenPipeError:
        return False


def lenh_doctor(a) -> int:
    he = platform.system()
    ket = []
    thieu_bat_buoc = []
    for c in CONG_CU:
        thay = None
        co_mat_nhung_hong = None
        for ten in c["ung_vien"]:
            d = shutil.which(ten)
            if not d:
                continue
            chay_duoc, pb = _phien_ban(d)
            if chay_duoc:
                thay = {"goi_bang": ten, "duong_dan": d, "phien_ban": pb}
                break
            co_mat_nhung_hong = {"goi_bang": ten, "duong_dan": d, "loi": pb}
        cai = c["cai"].get(he) or c["cai"].get("*") or ""
        muc = {"ten": c["ten"], "bat_buoc": c["bat_buoc"], "co": thay is not None,
               "vi_sao": c["vi_sao"], "lenh_cai": cai, **(thay or {})}
        if thay is None and co_mat_nhung_hong:
            muc["co_mat_nhung_khong_chay_duoc"] = co_mat_nhung_hong
        ket.append(muc)
        if thay is None and c["bat_buoc"]:
            thieu_bat_buoc.append(c["ten"])

    if a.json:
        _in_an_toan(json.dumps({"ok": not thieu_bat_buoc, "he_dieu_hanh": he,
                                "python_dang_chay": sys.version.split()[0],
                                "cong_cu": ket, "thieu_bat_buoc": thieu_bat_buoc},
                               ensure_ascii=False, indent=2))
    else:
        con_ong = _in_an_toan(
            f"he dieu hanh : {he}  |  python dang chay: {sys.version.split()[0]}")
        for c in ket:
            if not con_ong:
                break
            hong = c.get("co_mat_nhung_khong_chay_duoc")
            dau = "co  " if c["co"] else ("HONG" if hong else
                                          ("THIEU" if c["bat_buoc"] else "khong"))
            mo_ta = c.get("phien_ban", "") if c["co"] else c["vi_sao"]
            con_ong = _in_an_toan(f"  {dau:<5} {c['ten']:<8} {mo_ta}")
            if hong and con_ong:
                con_ong = _in_an_toan(
                    f"        co o {hong['duong_dan']} nhung KHONG chay duoc: {hong['loi']}")
            if not c["co"] and con_ong:
                con_ong = _in_an_toan(f"        cai bang: {c['lenh_cai']}")
        _in_an_toan("KET LUAN  : " + ("DU CONG CU BAT BUOC" if not thieu_bat_buoc
                                      else "THIEU " + ", ".join(thieu_bat_buoc)))
    return MA_THIEU_CONG_CU if thieu_bat_buoc else MA_OK


# ----------------------------------------------------------------------- CLI

def _them_chot(p):
    # KHONG required: mac dinh lay $TL_WORKSPACE roi den thu muc hien tai, vi
    # duong dan tuyet doi la thu duy nhat khong mang duoc sang may khac.
    p.add_argument("--workspace", default=None)
    p.add_argument("--expected-repo", default=None,
                   help="owner/repo hoac host/owner/repo - neo DANH TINH kho, khong phai duong dan")
    p.add_argument("--expected-root-commit", default=None,
                   help="sha40 commit goc - van tay ben nhat, doc duoc khong can mang")
    p.add_argument("--expected-head", default="")
    p.add_argument("--expected-ref", default="")
    p.add_argument("--require-clean", action="store_true")
    p.add_argument("--prompt-file", default=None)
    p.add_argument("--expected-prompt-sha256", default=None)
    p.add_argument("--deadline-utc", default=None)
    p.add_argument("--json", action="store_true")


def build_parser():
    ap = argparse.ArgumentParser(prog="launcher.py", description=__doc__.split("\n")[0])
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="lenh_con", required=True)

    c = sub.add_parser("check", help="chi chay cac chot, khong goi gi")
    _them_chot(c)
    c.set_defaults(fn=lenh_check)

    r = sub.add_parser("run", help="chay cac chot roi goi lenh dat sau --")
    _them_chot(r)
    r.add_argument("--run-root", required=True)
    r.add_argument("--name", default="")
    r.add_argument("--giu-ban-chup", action="store_true",
                   help="giu prompt.snapshot sau khi con thoat (mac dinh XOA: no chua noi dung prompt)")
    r.add_argument("lenh", nargs=argparse.REMAINDER)
    r.set_defaults(fn=lenh_run)

    s = sub.add_parser("status", help="xem so luot chay")
    s.add_argument("--run-root", required=True)
    s.add_argument("--id", default=None, help="run_id day du hoac short_id")
    s.set_defaults(fn=lenh_status)

    d = sub.add_parser("doctor", help="kiem cong cu moi truong (KHONG cai gi)")
    d.add_argument("--json", action="store_true")
    d.set_defaults(fn=lenh_doctor)

    k = sub.add_parser("stop", help="dung mot luot chay (giet ca cay tien trinh)")
    k.add_argument("--run-root", required=True)
    k.add_argument("--id", required=True)
    k.set_defaults(fn=lenh_stop)
    return ap


def _cung_hoa_dau_ra() -> None:
    """Ép stdout/stderr sang UTF-8 TRƯỚC khi in bất cứ thứ gì.

    ĐÃ ĐO TRÊN WINDOWS (codex, 12-08-2026): console mặc định là cp1258 ở máy tiếng
    Việt, nên `print(duong_dan_co_dau)` ném UnicodeEncodeError và launcher chết rc=1
    — CHÍNH ca mà tệp này khoe là đã sửa. Bẫy nằm ở ĐẦU RA, không phải ở đối số:
    subprocess truyền đường dẫn đúng, git trả về đúng, rồi câu `print` giết cả lượt.
    Cùng lệnh đó với PYTHONUTF8=1 thì rc=0 — bằng chứng nó là lỗi encode console.
    """
    for luong in (sys.stdout, sys.stderr):
        try:
            luong.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass  # luồng bị thay bằng thứ không reconfigure được: thà chạy tiếp


def main(argv=None) -> int:
    _cung_hoa_dau_ra()
    a = build_parser().parse_args(argv)
    if getattr(a, "lenh", None) and a.lenh and a.lenh[0] == "--":
        a.lenh = a.lenh[1:]
    try:
        ma = a.fn(a)
    except Chan as e:
        # In lỗi cũng có thể vỡ ống (stderr gộp vào ống rồi bị cắt). `except
        # BrokenPipeError` bên dưới là ANH EM của `except Chan`, KHÔNG bọc thân
        # nó — nên câu print này mà ném thì traceback thô rơi ra ngoài.
        try:
            print(f"CHAN [{e.ma}]: {e.thong_diep}", file=sys.stderr)
        except (BrokenPipeError, OSError):
            pass
        ma = e.ma
    except BrokenPipeError:
        # Tới đây nghĩa là ống vỡ ở chỗ KHÔNG qua `_in_an_toan`, nên chưa có kết
        # luận nào để giữ. 141 = 128+SIGPIPE, khác 0 nên không báo thành công oan.
        ma = 141
    # Ống đã đóng thì lúc dọn dẹp Python cũng không flush được, và ngoại lệ ở đó
    # KHÔNG ai bắt: nó in "Exception ignored" rồi ĐỔI mã thoát thành 120. Trỏ fd 1
    # sang devnull để mã ta vừa quyết định là mã thật sự đi ra ngoài.
    try:
        sys.stdout.flush()
    except (BrokenPipeError, OSError):
        try:
            os.dup2(os.open(os.devnull, os.O_WRONLY), 1)
        except OSError:
            pass
    return ma


if __name__ == "__main__":
    sys.exit(main())
