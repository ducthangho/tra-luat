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
  13  công cụ CÓ MẶT nhưng CHƯA DÙNG ĐƯỢC — thiếu xác thực (xem `doctor`, `chuan-bi`)
  14  workspace là git worktree — phải dùng clone độc lập
  15  probe năng lực ĐỎ hoặc KHÔNG ĐO ĐƯỢC
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

VÀ `trang_thai` CŨNG KHÔNG ĐỦ — nói thẳng kẻo câu trên bị đọc rộng hơn thực tế.
`xong` chỉ nghĩa là CON ĐÃ THOÁT VỚI MÃ 0, không nghĩa là việc đã làm. Đo được
16-08-2026: một lượt gọi agent trả `trang_thai=xong`, `ma_thoat=0`, mà agent
dừng ngay ở bước đầu và từ chối làm vì môi trường thiếu quyền — nếu người vận
hành dừng ở hai trường ấy thì đã báo "chạy xong, không có gì" cho một lượt chưa
làm gì. Thứ tố cáo là THỜI LƯỢNG (43 giây cho việc lẽ ra hàng chục phút) và
KÍCH THƯỚC ĐẦU RA, nên hai thứ đó nay được ghi thẳng vào sổ: `thoi_luong_giay`,
`stdout_byte`, `stderr_byte`. Cùng họ với bài học "ca có MẶT khác ca có ĐO":
launcher đo VÒNG ĐỜI TIẾN TRÌNH, nó không biết và không thể biết nội dung công
việc. Ai gọi tự động phải tự đặt ngưỡng cho ba số ấy.
"""

from __future__ import annotations

import argparse
import base64
import contextlib
import hashlib
import hmac
import json
import os
import platform
import re
import runpy
import secrets
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.5.0"


def ky_ban_ghi_luot(ban_ghi: dict, khoa_hex: str) -> str:
    """Chuẩn hoá và HMAC-SHA256 một bản ghi, bỏ chính trường ``chu_ky``.

    Cơ chế này chống VÔ Ý và chống PHÁT LẠI. Nó KHÔNG chống giả mạo có chủ
    đích, và không thể, chừng nào executor còn cùng principal với launcher.
    Khoá nằm trong state chỉ mua integrity, không mua authenticity.
    """
    than = {k: v for k, v in ban_ghi.items() if k != "chu_ky"}
    raw = json.dumps(than, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                     allow_nan=False).encode("utf-8")
    return hmac.new(bytes.fromhex(khoa_hex), raw, hashlib.sha256).hexdigest()

# launcher-nang-luc: so-dinh-luong module-python hook-phien moi-truong chuan-bi tu-cu probe-qua-han-ba-trang-thai mcp-endpoint van-chuyen-prompt
#
# CÙNG CƠ CHẾ với `# hook-nang-luc:` trong `.claude/hooks/session-start.sh`, áp cho
# CHÍNH TỆP NÀY. Vì sao cần: sự cố 15-08 là hook của nhánh packet cũ hơn hook master;
# 16-08 lặp lại y hệt một tầng khác — một phiên chạy `launcher.py` từ cây đã checkout
# NHÁNH PACKET, nên bản chạy thật THIẾU đúng bản vá vừa land trên master. Sổ lượt chạy
# im lặng không có `thoi_luong_giay`/`stdout_byte`/`stderr_byte`, và người vận hành phải
# tự trừ hai mốc thời gian mới thấy — đúng thứ bản vá ấy sinh ra để khỏi phải làm.
#
# ĐO THEO NĂNG LỰC, KHÔNG THEO BĂM TOÀN TỆP: sửa một dấu phẩy trong chú thích mà chốt
# đỏ thì chốt sẽ bị bỏ qua. Và KHÔNG dùng quan hệ tổ tiên: nhánh packet cũ LÀ tổ tiên
# hợp lệ của master, nên tổ tiên không phân biệt được "cũ nhưng đủ" với "cũ và thiếu".
# Thêm năng lực so với master (nhánh mới hơn) KHÔNG phải lỗi.

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
MA_CHUA_XAC_THUC = 13
MA_WORKTREE = 14
MA_PROBE = 15


# Một provider chỉ có MỘT contract vận chuyển. Tên executable được chuẩn hoá bỏ
# hậu tố shim đa nền trước khi tra bảng; đường dẫn tuyệt đối không làm đổi identity.
_TRANSPORT_CONTRACTS = (
    ("anthropic_claude", ("claude",), "claude_code", "machine/local"),
    ("openai_codex", ("codex",), "codex_cli", "machine"),
    ("openai_api", ("llm",), "llm_cli", "machine"),
)

# Bề mặt KHÔNG đi qua một CLI của launcher nằm ngoài `_TRANSPORT_CONTRACTS`.
# Một provider có thể có cả hàng CLI và ngoài CLI với hai bề mặt khác nhau (Codex).
# Bộ kiểm biên nhận (`ops/bien_nhan_v2.py`) cần nguồn CÓ CẤU TRÚC cho các bề mặt này.
#
# VÌ SAO Ở ĐÂY, và vì sao là BẢNG chứ không phải văn xuôi: cross-review PR #455 đo được
# hai lần liên tiếp rằng một danh sách CHO PHÉP rút từ VĂN BẢN TỰ DO thì nới được bằng
# văn bản tự do — đầu tiên là một dòng chú thích bất kỳ trong tệp này, rồi (sau khi siết
# vào AST) là chính chuỗi `vi_sao` mô tả của một mục `CONG_CU`. Đổi NGUỒN mà giữ nguyên
# HÌNH DẠNG (đọc prose) thì cái lỗ chỉ đổi chỗ. Bảng này là hình dạng đúng: thêm một
# provider phải là một phép sửa CẤU TRÚC, không phải một câu chữ.
#
# (provider, execution_surface, transport) — cùng ba trường với `_TRANSPORT_CONTRACTS`,
# trừ tên lệnh vì không có lệnh nào.
_PROVIDER_NGOAI_CLI = (
    # `machine/local`, KHÔNG phải `machine` — chép đúng `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md`
    # §2 hàng "Google Antigravity". Cross-review PR #460 đo được hàng này LỆCH nguồn, và lệch
    # theo chiều CHẶN NHẦM: một biên nhận Antigravity khai TRUNG THỰC `machine/local` bị cổng
    # TỪ CHỐI, còn khai SAI `machine` thì ĐƯỢC NHẬN — validation đảo ngược. Cùng LỚP với
    # `R7-02` (chặn quá rộng theo một hằng chép tay lệch nguồn). `anthropic_claude` trong
    # `_TRANSPORT_CONTRACTS` vốn đã dùng `machine/local`, nên dạng giá trị này được hỗ trợ sẵn
    # và Antigravity là hàng DUY NHẤT còn lệch.
    ("google_antigravity", "antigravity", "machine/local"),
    ("openai_chatgpt", "chatgpt_web", "human_mediated"),
    # WP610: Desktop khai đúng bề mặt; không là CLI hoặc bằng chứng model/assurance.
    ("openai_codex", "codex_desktop", "machine"),
    # wp461 r3: Codex chạy như DỊCH VỤ — GitHub App `chatgpt-codex-connector[bot]` (review trên
    # PR) và Codex cloud nói chung. Không CLI, không Desktop; không chứng minh model/effort hay
    # tính độc lập của phiên. Tên máy chốt ở Mission #470 (Q1); định nghĩa ở spec r3 §2.
    ("openai_codex", "codex_service", "machine"),
    # Human Auditor — bộ ba chép từ bảng provider chuyển tiếp
    # (`ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` §2, hàng "Human Auditor"). Cross-review PR #455
    # lượt 7 (`R7-02`) đo được: `human` từng bị bộ kiểm biên nhận chép tay vào tập "KHÔNG hợp
    # đồng" nên bị cấm cả `human_audited` — mức `PROTOCOL §8` dành ĐÚNG cho người audit.
    # Vận chuyển là `human`, KHÔNG phải `human_mediated`: ở đây người LÀ reviewer, không phải
    # người chuyển tiếp đầu ra của một mô hình. Cột ấy là thứ bộ kiểm dùng để phân vùng mức
    # assurance người/mô hình, nên đừng đổi nó khi "dọn cho gọn".
    ("human", "manual_audit", "human"),
)

# BÍ DANH LỊCH SỬ → tên chính tắc. Hiện vật cũ của kho khai `anthropic` và
# `claude_code_cli`; giữ được đọc, nhưng phải CHUẨN HOÁ TRƯỚC mọi phép kiểm theo provider,
# kẻo bí danh thành đường lách quanh chính ràng buộc của tên chính tắc.
_PROVIDER_BI_DANH = (
    ("anthropic", "anthropic_claude"),
)
_BE_MAT_BI_DANH = (
    ("claude_code_cli", "claude_code"),
)


def _dinh_danh_van_chuyen(lenh: list[str]) -> dict:
    """Trả contract transport canonical và băm của chính contract ấy."""
    theo_provider = {}
    theo_lenh = {}
    for provider, ten_lenh, surface, transport in _TRANSPORT_CONTRACTS:
        contract = {"provider": provider, "execution_surface": surface,
                    "transport": transport}
        cu = theo_provider.setdefault(provider, contract)
        if cu != contract:
            raise RuntimeError(f"provider co nhieu transport: {provider}")
        for ten in ten_lenh:
            theo_lenh[ten] = contract
    ten = Path(str(lenh[0])).name.casefold() if lenh else ""
    for duoi in (".exe", ".cmd", ".bat"):
        if ten.endswith(duoi):
            ten = ten[:-len(duoi)]
            break
    contract = theo_lenh.get(ten, {
        "provider": "local_process", "execution_surface": "subprocess",
        "transport": "machine",
    })
    raw = json.dumps(contract, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {**contract, "transport_sha256": hashlib.sha256(raw).hexdigest()}

# Bộ đột biến dùng cùng mốc này để không thể trượt từ ~70% phép đo được xuống
# gần 0 mà vẫn xanh. Đặt ở mã được đột biến (không đặt trong chính runner test).
TY_LE_DOT_BIEN_TOI_THIEU_PHAN_MUOI = 7

# (Đã bỏ `KHONG_DOC_DUOC_KHOA`.) Ảnh chụp Windows không còn quét cả máy qua WMI
# rồi mang cờ "không đọc được khoá" đi kèm: nay `_chup_cay` dựng quan hệ cha-con
# bằng Toolhelp32, và CHỈ hỏi khoá danh tính cho các PID ĐÃ nằm trong cây. Phạm
# vi fail-closed vì thế đo thẳng được, không cần cờ mang theo — và một tiến trình
# hệ thống ngoài cây không còn làm hỏng ảnh của cây vô can.

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


def _chay_van_ban_an_toan(lenh: list[str], *, env: dict[str, str] | None = None,
                          stdin=subprocess.DEVNULL, timeout: float = 30.0,
                          cwd: Path | str | None = None) -> subprocess.CompletedProcess:
    """Chạy tiến trình lấy đầu ra văn bản an toàn đa nền tảng.

    Bắt buộc `encoding="utf-8", errors="replace"` để chống lỗi UnicodeDecodeError
    ('charmap' codec) trên Windows khi tiến trình con in ký tự ngoài code page cp1258/cp1252.
    """
    return subprocess.run(lenh, capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          env=env, stdin=stdin, timeout=timeout, cwd=cwd)


def _chay_json_chat_che(lenh: list[str], *, env: dict[str, str] | None = None,
                        stdin=subprocess.DEVNULL, timeout: float = 30.0,
                        cwd: Path | str | None = None) -> tuple[int, dict | list | None, str]:
    """Chạy tiến trình và phân tích JSON nghiêm ngặt từ đầu ra UTF-8.

    Không dùng errors="replace" làm biến dạng dữ liệu cấu trúc máy đọc.
    Trả về: (ma_thoat, parsed_json, thong_bao_loi).
    """
    try:
        p = subprocess.run(lenh, capture_output=True, text=True,
                           encoding="utf-8", errors="strict",
                           env=env, stdin=stdin, timeout=timeout, cwd=cwd)
    except UnicodeDecodeError as e:
        return (-1, None, f"loi giai ma UTF-8: {e}")
    except subprocess.TimeoutExpired:
        return (124, None, f"qua han {timeout}s")
    except (OSError, subprocess.SubprocessError) as e:
        return (-1, None, f"loi tien trinh: {e}")

    if p.returncode != 0:
        return (p.returncode, None, p.stderr.strip() or p.stdout.strip())
    try:
        data = json.loads(p.stdout)
        return (0, data, "")
    except json.JSONDecodeError as e:
        return (-1, None, f"loi phan tich JSON: {e}")


# --------------------------------------------------- danh tính tiến trình (kill an toàn)

def _khoa_danh_tinh(pid: int) -> str | None:
    """Khoá nhận dạng tiến trình để chống PID tái dùng. None = không xác định được.

    Không có khoá thì tuyệt đối không giết: PID quay vòng, và giết nhầm một tiến
    trình vô can là hỏng nặng hơn nhiều so với để một tiến trình sống thừa.
    """
    he = platform.system()
    try:
        if he == "Linux":
            # wp685 (Q-A.7; quyết định chủ kho, PR #688 comment 5905670017) — comm bị kernel cắt
            # 15 byte nên tên tiếng Việt thành UTF-8 hỏng; read_text() theo locale ném UnicodeDecodeError
            # và hàm trả None cho tiến trình CÒN SỐNG. latin-1 là song ánh byte↔ký tự: không bao giờ ném.
            noi_dung = Path(f"/proc/{pid}/stat").read_text(encoding="latin-1")
            # comm có thể chứa khoảng trắng và dấu ')' -> cắt từ ')' CUỐI CÙNG
            sau = noi_dung[noi_dung.rindex(")") + 2:].split()
            return f"linux:{sau[19]}"  # trường 22 tính từ 1 = starttime
        if he == "Darwin":
            p = subprocess.run(["ps", "-o", "lstart=", "-p", str(pid)],
                               capture_output=True, text=True, timeout=15)
            v = p.stdout.strip()
            return f"darwin:{v}" if v else None
        if he == "Windows":
            # KHÔNG qua PowerShell/WMI. Đã đo 15-08-2026: Get-CimInstance trả
            # Access denied trong sandbox dù chính tiến trình con do ta sinh ra,
            # làm mọi deadline tụt về rc=10. GetProcessTimes chỉ cần quyền query
            # trên đúng PID, không cần dịch vụ WMI hay external tool.
            import ctypes
            from ctypes import wintypes
            k32 = ctypes.windll.kernel32

            class _FILETIME(ctypes.Structure):
                _fields_ = [("dwLowDateTime", wintypes.DWORD),
                            ("dwHighDateTime", wintypes.DWORD)]

            k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            k32.OpenProcess.restype = wintypes.HANDLE
            k32.GetProcessTimes.argtypes = [wintypes.HANDLE,
                                            ctypes.POINTER(_FILETIME),
                                            ctypes.POINTER(_FILETIME),
                                            ctypes.POINTER(_FILETIME),
                                            ctypes.POINTER(_FILETIME)]
            k32.GetProcessTimes.restype = wintypes.BOOL
            k32.CloseHandle.argtypes = [wintypes.HANDLE]
            k32.CloseHandle.restype = wintypes.BOOL
            h = k32.OpenProcess(0x1000, False, int(pid))  # QUERY_LIMITED_INFORMATION
            if not h:
                return None
            try:
                tao, thoat, kernel, user = _FILETIME(), _FILETIME(), _FILETIME(), _FILETIME()
                if not k32.GetProcessTimes(h, ctypes.byref(tao), ctypes.byref(thoat),
                                           ctypes.byref(kernel), ctypes.byref(user)):
                    return None
                ticks = (int(tao.dwHighDateTime) << 32) | int(tao.dwLowDateTime)
                return f"win:{ticks}" if ticks else None
            finally:
                k32.CloseHandle(h)
    except (OSError, ValueError, IndexError):
        return None
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
                # wp685 (Q-A.7): giải mã latin-1, comm hỏng không được làm tiến trình sống "biến mất"
                nd = (p / "stat").read_text(encoding="latin-1")
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
                # wp685 (Q-A.7): giải mã latin-1, comm hỏng không được làm cháu vắng khỏi ảnh chụp
                nd = (p / "stat").read_text(encoding="latin-1")
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
        # Toolhelp lấy pid/ppid bằng Win32 API, không qua WMI (WMI bị sandbox từ
        # chối). Chỉ lấy khoá thời gian cho CÁC PID TRONG CÂY sau khi duyệt quan
        # hệ cha-con, nên một tiến trình hệ thống không query được không làm hỏng
        # phép đo của cây vô can.
        cha_theo_pid = _cac_pid_cha_windows()
        if cha_theo_pid is None:
            return None
        tt = {q: (cha, 0, "") for q, cha in cha_theo_pid.items()}
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
    # Fail-closed CÓ PHẠM VI, nay đo THẲNG thay vì mang cờ: chỉ các PID ĐÃ nằm
    # trong cây mới bị hỏi khoá danh tính. Hỏi được hết thì ảnh dùng được; một
    # PID trong cây không đọc nổi khoá thì ảnh là "không đo được" (None), chứ
    # KHÔNG phải "cây đã chết". Tiến trình hệ thống ngoài cây không còn ảnh
    # hưởng tới kết luận — đó là điều bản cũ (quét toàn máy) không tách được.
    if he == "Windows":
        for q in list(ra):
            khoa = _khoa_danh_tinh(q)
            if khoa is None:
                return None
            ra[q] = khoa
    return ra


def _cac_pid_cha_windows() -> dict[int, int] | None:
    """Ảnh pid->ppid bằng Toolhelp32; None = không đo được."""
    if platform.system() != "Windows":
        return None
    try:
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.windll.kernel32

        class _PROCESSENTRY32W(ctypes.Structure):
            _fields_ = [("dwSize", wintypes.DWORD),
                        ("cntUsage", wintypes.DWORD),
                        ("th32ProcessID", wintypes.DWORD),
                        ("th32DefaultHeapID", ctypes.c_size_t),
                        ("th32ModuleID", wintypes.DWORD),
                        ("cntThreads", wintypes.DWORD),
                        ("th32ParentProcessID", wintypes.DWORD),
                        ("pcPriClassBase", wintypes.LONG),
                        ("dwFlags", wintypes.DWORD),
                        ("szExeFile", wintypes.WCHAR * 260)]

        k32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        k32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        k32.Process32FirstW.argtypes = [wintypes.HANDLE,
                                        ctypes.POINTER(_PROCESSENTRY32W)]
        k32.Process32FirstW.restype = wintypes.BOOL
        k32.Process32NextW.argtypes = [wintypes.HANDLE,
                                       ctypes.POINTER(_PROCESSENTRY32W)]
        k32.Process32NextW.restype = wintypes.BOOL
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        k32.CloseHandle.restype = wintypes.BOOL
        snap = k32.CreateToolhelp32Snapshot(0x00000002, 0)  # TH32CS_SNAPPROCESS
        if snap == wintypes.HANDLE(-1).value:
            return None
        try:
            e = _PROCESSENTRY32W()
            e.dwSize = ctypes.sizeof(e)
            if not k32.Process32FirstW(snap, ctypes.byref(e)):
                return None
            ra = {}
            while True:
                ra[int(e.th32ProcessID)] = int(e.th32ParentProcessID)
                if not k32.Process32NextW(snap, ctypes.byref(e)):
                    break
            return ra
        finally:
            k32.CloseHandle(snap)
    except (OSError, AttributeError, ValueError):
        return None


def _con_song_dung_khoa(pid: int, khoa: str) -> bool:
    """Còn sống VÀ vẫn đúng tiến trình cũ. Khoá rỗng = không có khoá để so."""
    if not _con_song(pid):
        return False
    if not khoa:
        return True
    return _khoa_danh_tinh(pid) == khoa


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


def _con_song(pid: int, khoa: str | None = None) -> bool:
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
        return khoa is None or hien == khoa
    trang_thai = Path(f"/proc/{pid}/stat")
    # wp685 (ESRCH: PR #679, job 109303373142) — tiến trình biến mất giữa chừng làm phép thăm dò
    # NÉM ProcessLookupError thay vì trả False, và ngoại lệ ấy thoát khỏi _con_song. Phép hỏi
    # chạy ĐÚNG MỘT lần, không thử lại (cross-review lượt 2, lượt 6 trên PR #688).
    # Chỉ bắt họ OSError ở đây: nhóm phân tích, Exception, BaseException thoát nguyên
    # (cross-review lượt 3, lượt 5).
    # #743 (py314-path-exists-nuot-oserror; t156/t157 đỏ trên Python 3.14.6) — từ 3.14
    # `Path.exists()` là `os.path.exists`, NUỐT mọi OSError thành False và không đi qua
    # `Path.stat`, nên hai nhánh dưới chết câm. Thăm dò bằng `stat()` để GIỮ errno:
    # ENOENT/ENOTDIR ⇒ không có tệp; ESRCH ⇒ chết; OSError khác ⇒ chưa kết luận.
    try:
        trang_thai.stat()
        co_tep = True
    except (FileNotFoundError, NotADirectoryError):
        co_tep = False
    except ProcessLookupError:
        return False
    except OSError:
        co_tep = None   # KHÔNG kết luận: không stat được chưa có nghĩa là không đọc được
    if co_tep:
        # Nhánh tệp có giữ nguyên xi (Q-A.3), trừ cách giải mã (Q-A.7: latin-1, PR #688
        # comment 5905670017; cross-review lượt 7, lượt 8).
        try:
            noi_dung = trang_thai.read_text(encoding="latin-1")
            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"
        except (OSError, ValueError, IndexError):
            return False
    if co_tep is None:
        # wp685 (zombie: cross-review lượt 1 trên PR #688) — thử đọc nội dung ĐÚNG MỘT lần,
        # zombie vẫn phải tính là đã chết. Đọc lỗi hay nội dung hỏng ⇒ KHÔNG trả False mà rơi
        # về os.kill(pid, 0) bên dưới (cross-review lượt 2, lượt 4: bước kill phải THỰC SỰ được
        # gọi và quyết định). Khối bọc chỉ gồm phép đọc và biểu thức tách theo ')' CUỐI.
        try:
            noi_dung = trang_thai.read_text(encoding="latin-1")
            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"
        except (OSError, ValueError, IndexError):
            pass
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


def _job_windows(pid: int):
    """Nhốt tiến trình vào một Job Object. Trả handle, hoặc None nếu không được.

    VÌ SAO PHẢI CÓ: `taskkill /T` duyệt cây CHA-CON tại thời điểm chạy, nên một
    tiến trình mà cha đã thoát trước đó (MỒ CÔI) không nằm trong cây và sống sót
    nguyên vẹn. `_chup_cay` cũng đi đúng những liên kết ấy nên bỏ sót y hệt —
    nó chỉ nâng "tin rc=0" thành "kiểm từng pid", không phủ được ca mồ côi.
    Job Object là cơ chế DUY NHẤT trên Windows giữ được cả hậu duệ mồ côi: tiến
    trình con sinh ra đã ở trong job của cha, và ở lại đó kể cả khi cha chết.

    KHE HỞ, nói thẳng: `Popen` không cho gán job lúc tạo (không có CREATE_SUSPENDED),
    nên có một khoảng rất ngắn giữa lúc sinh con và lúc gán. Con nào sinh cháu
    trong khoảng đó thì cháu nằm ngoài job. Hẹp hơn hẳn khe cũ, nhưng không phải
    không có.
    """
    if platform.system() != "Windows":
        return None
    try:
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.windll.kernel32
        job = k32.CreateJobObjectW(None, None)
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


def _giet_windows(pid: int, khoa: str | None = None,
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
                           capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=30)
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


def _giet_cay(pid: int, khoa: str | None, job=None) -> KetGiet:
    """Giết tiến trình VÀ con cháu. Trả KetGiet, KHÔNG trả chuỗi.

    Phía gọi quyết định mã thoát bằng `.tron_ven`, nên không còn cách nào để một
    câu mô tả nghe-như-thành-công lọt qua.
    """
    if khoa is None:
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
            con = _chup_cay(pid)
            rong = con == {}
        else:
            con = _thanh_vien_nhom(pid)
            rong = con == []      # [] = đã chứng minh rỗng · None = không đo được
        if rong:
            return KetGiet(True, True, "tien trinh da khong con chay")
    elif hien != khoa:
        return KetGiet(False, False,
                       "tu choi giet: khoa danh tinh KHAC (PID da bi tai dung)",
                       tu_choi=True)
    if platform.system() == "Windows":
        # Chup TRUOC khi giet: sau khi me chet, hau due mo coi khong con duong nao
        # tim lai (cung ly le nhu POSIX, xem `_chup_cay`).
        return _giet_windows(pid, khoa, _chup_cay(pid), job)
    # POSIX: con được sinh với start_new_session nên pgid == pid, giết cả nhóm.
    # Ảnh chụp phải lấy TRƯỚC phát tín hiệu đầu tiên — sau đó kẻ đã setsid() là
    # không thể tìm lại (xem _chup_cay).
    # CHỐT TRƯỞNG NHÓM — `killpg` nhận PROCESS GROUP ID, còn ta đang cầm PID.
    #
    # Hai số đó chỉ bằng nhau khi tiến trình LÀ TRƯỞNG NHÓM — điều kiện mà
    # `start_new_session=True` lúc sinh con tạo ra. Chú thích ngay trên khai đúng giả
    # định ấy, nhưng KHÔNG AI KIỂM nó tại chỗ giết. Giả định không được kiểm là giả
    # định sẽ sai vào đúng ngày nó đắt nhất.
    #
    # ĐÃ ĐO: với một tiến trình sinh KHÔNG kèm `start_new_session` (pid=26072,
    # pgid=26071), `_giet_cay` gọi thẳng `killpg(26072)` — tức nhắm vào một nhóm
    # KHÔNG PHẢI nhóm của mục tiêu.
    #
    # Trên máy thường pid cỡ vài chục nghìn nên nhóm ấy hầu như không tồn tại và lỗi
    # tan thành `ProcessLookupError`. Trong PID NAMESPACE thì pid chạy từ 1 — và ở đó
    # `killpg(<số nhỏ>)` rất dễ trúng một nhóm CÓ THẬT, kể cả nhóm 1 là nhóm của chính
    # vỏ shell gọi ta. Đó khớp với triệu chứng cross-review đo được ba lượt liền: bộ
    # test chạy xong nhưng lệnh shell kế tiếp không bao giờ chạy.
    #
    # Đây đúng họ lỗi mà tệp này đã dựng chốt khoá-danh-tính để chặn ("PID bị tái dùng,
    # giết nhầm tiến trình vô can"). Chốt cũ hỏi "PID này còn là NGƯỜI CŨ không"; chốt
    # này hỏi "PID này có thật sự là CẢ NHÓM không". Thiếu vế sau thì vế trước không đủ.
    #
    # v1.35.86 (cross-review lượt 6, P1 `chot-truong-nhom-van-fail-open`) — bản vá
    # ĐẦU của chốt này ghi: "KHÔNG đo được `pgid` thì ĐI TIẾP — tiến trình có thể vừa
    # chết". Đó là FAIL-OPEN, và nó bỏ qua chốt ở ĐÚNG ca nguy hiểm nhất.
    #
    # `getpgid` không chỉ ném `ESRCH` (mục tiêu đã chết — vô hại). Nó còn ném `EPERM`
    # khi mục tiêu SỐNG nhưng ở SESSION KHÁC — tức đúng cái ca mà `killpg(pid)` bắn
    # vào nhóm của người vô can. Bản trước không phân biệt được hai ca đó, và vẫn bắn.
    #
    # Doctrine tệp này đã viết rồi: `None` (không đo được) KHÁC `False`. Tôi viết nó
    # vào chỗ khác rồi vi phạm ngay tại dòng vá.
    #
    # Chốt mới: `killpg` CHỈ chạy khi ĐO ĐƯỢC và `pgid == pid`. Không đo được thì
    # KHÔNG mua an toàn bằng cách thôi giết — vẫn giết, nhưng bằng `_giet_rieng` trên
    # ẢNH CHỤP, tức từng pid một CÓ KHOÁ DANH TÍNH. `_chup_cay` phủ chính `pid`, mọi
    # hậu duệ VÀ mọi thành viên nhóm, nên đường này không yếu hơn về tầm với.
    # Khe duy nhất mất đi, nói thẳng: tiến trình GIA NHẬP nhóm SAU lúc chụp — `killpg`
    # với tới, `_giet_rieng` thì không. Đổi một khe hẹp lấy việc thôi bắn vào nhóm 1.
    nhom_that = None
    try:
        nhom_that = os.getpgid(pid)
    except OSError:
        nhom_that = None
    if nhom_that is not None and nhom_that != pid:
        return KetGiet(False, False,
                       f"tu choi giet: pid {pid} KHONG phai truong nhom "
                       f"(pgid={nhom_that}) - killpg({pid}) se nham vao nhom KHAC",
                       tu_choi=True)
    dung_killpg = nhom_that == pid          # CHỈ True khi ĐO ĐƯỢC và bằng nhau

    anh = _chup_cay(pid)
    if not dung_killpg and not anh:
        # Không được `killpg`, mà ảnh chụp cũng rỗng/không đo được ⇒ KHÔNG còn đường
        # giết nào an toàn. Nói thật là không giết được, đừng im lặng không làm gì.
        return KetGiet(False, False,
                       "tu choi giet: pgid KHONG do duoc (khong duoc killpg) va anh "
                       "chup rong/khong do duoc - khong con duong giet an toan",
                       tu_choi=True)

    def _con_lai():
        """Ai còn sống: ảnh chụp (bắt cả kẻ đã rời nhóm) HỢP thành viên nhóm hiện
        tại (bắt cả kẻ sinh sau lúc chụp). None = không đo được ⇒ KHÔNG khẳng định.

        Khi KHÔNG dùng `killpg`, nhóm của `pid` KHÔNG phải đơn vị kế toán của ta —
        ta chưa từng bắn vào nó, và `pid` còn chẳng phải trưởng nhóm — nên phần nhóm
        đóng góp RỖNG. Đây không phải khẳng định "nhóm đã rỗng"; là "nhóm không nằm
        trong phạm vi ta nhận trách nhiệm". Ảnh chụp vẫn phủ cả thành viên nhóm tại
        thời điểm chụp, nên phần bị bỏ đúng bằng khe đã khai ở trên."""
        nhom = _thanh_vien_nhom(pid) if dung_killpg else []
        if nhom is None or anh is None:
            return None
        return {q for q, k in anh.items() if _con_song_dung_khoa(q, k)} | set(nhom)

    if dung_killpg:
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
    if dung_killpg:
        try:
            os.killpg(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass                   # nhóm đã sạch giữa chừng
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

    def __init__(self, ma: int, thong_diep: str, probe: dict | None = None):
        super().__init__(thong_diep)
        self.ma = ma
        self.thong_diep = thong_diep
        self.probe = probe


def chot_workspace(ws: str) -> str:
    d = Path(ws).expanduser()
    if not d.is_dir():
        raise Chan(MA_THAM_SO, f"workspace khong phai thu muc: {ws}")
    rc, top, err = _git_mot_dong(d, "rev-parse", "--show-toplevel")
    if rc != 0 or not top:
        raise Chan(MA_GIT, f"khong doc duoc repo tai {d}: {err or 'git that bai'}")
    return str(Path(top).resolve())


def _probe_workspace(ws: str) -> dict:
    git_meta = Path(ws) / ".git"
    try:
        if git_meta.is_file():
            return {"trang_thai": "DO", "chi_tiet": "git worktree", "ma": "git_worktree"}
        if git_meta.is_dir():
            return {"trang_thai": "DAT", "chi_tiet": ".git la thu muc"}
    except OSError as e:
        return {"trang_thai": "KHONG_DO_DUOC", "chi_tiet": type(e).__name__}
    return {"trang_thai": "KHONG_DO_DUOC", "chi_tiet": ".git khong phai tep/thu muc"}


def _probe_ghi(ws: str) -> dict:
    tep = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".launcher-probe-", dir=ws, delete=False) as f:
            tep = Path(f.name)
            f.write(b"LAUNCHER_WRITE_PROBE\n")
            f.flush()
        if tep.read_bytes() != b"LAUNCHER_WRITE_PROBE\n":
            return {"trang_thai": "DO", "chi_tiet": "ghi/readback lech"}
        tep.unlink()
        tep = None
        return {"trang_thai": "DAT", "chi_tiet": "ghi-readback-xoa thanh cong"}
    except OSError as e:
        return {"trang_thai": "DO", "chi_tiet": f"ghi workspace: {type(e).__name__}"}
    finally:
        if tep is not None:
            try:
                tep.unlink()
            except OSError:
                pass


def _probe_spawn(chuong_trinh: str, ws: str) -> dict:
    try:
        p = _chay_van_ban_an_toan([chuong_trinh, "--version"], cwd=ws, timeout=30)
    except (OSError, subprocess.SubprocessError) as e:
        return {"trang_thai": "DO", "chi_tiet": f"spawn --version: {type(e).__name__}"}
    ra = (p.stdout or "") + (p.stderr or "")
    if p.returncode == 0 and bool(ra.strip()):
        return {"trang_thai": "DAT", "chi_tiet": f"rc=0; output={len(ra.encode('utf-8'))}B"}
    return {"trang_thai": "DO", "chi_tiet": f"rc={p.returncode}; output={len(ra)} ky tu"}


def _probe_trust_claude(ws: str, home: Path | None = None) -> dict:
    try:
        data = json.loads(((home or Path.home()) / ".claude.json").read_text(encoding="utf-8"))
        # Claude writes Windows project keys with forward slashes. Only fold
        # separators; do not broaden trust through case, parents or symlinks.
        khoa = str(Path(ws).resolve())
        chuan = (lambda p: p.replace("\\", "/")) if platform.system() == "Windows" else (lambda p: p)
        cac_muc = [v for k, v in data.get("projects", {}).items() if chuan(k) == chuan(khoa)]
        muc = cac_muc[0] if cac_muc else None
    except (OSError, TypeError, AttributeError, json.JSONDecodeError):
        return {"trang_thai": "KHONG_DO_DUOC", "chi_tiet": "khong doc duoc trust Claude"}
    if not isinstance(muc, dict) or "hasTrustDialogAccepted" not in muc:
        return {"trang_thai": "KHONG_DO_DUOC", "chi_tiet": "thieu khoa trust Claude"}
    if any(not isinstance(v, dict) or "hasTrustDialogAccepted" not in v
           or v["hasTrustDialogAccepted"] is not muc["hasTrustDialogAccepted"] for v in cac_muc):
        return {"trang_thai": "KHONG_DO_DUOC", "chi_tiet": "trust Claude co alias mau thuan"}
    if muc["hasTrustDialogAccepted"] is True:
        return {"trang_thai": "DAT", "chi_tiet": "Claude trust=true"}
    if muc["hasTrustDialogAccepted"] is False:
        return {"trang_thai": "DO", "chi_tiet": "Claude trust=false"}
    return {"trang_thai": "KHONG_DO_DUOC", "chi_tiet": "trust Claude khong phai boolean"}


def _probe_cho_so(ds: dict) -> dict:
    return {ten: {"trang_thai": kq["trang_thai"], "chi_tiet": kq["chi_tiet"]}
            for ten, kq in ds.items()}


def chay_cac_probe(ws: str, lenh: list[str], bo_qua: str | None) -> tuple[dict, str | None]:
    ds = {"workspace": _probe_workspace(ws), "ghi": _probe_ghi(ws),
          "spawn": _probe_spawn(str(lenh[0]), ws)}
    if Path(str(lenh[0])).name.casefold() in ("claude", "claude.exe"):
        ds["claude_trust"] = _probe_trust_claude(ws)
    ly_do = bo_qua.strip() if bo_qua is not None else None
    if bo_qua is not None and not ly_do:
        raise Chan(MA_THAM_SO, "--bo-qua-probe bat buoc co ly do khac rong", ds)
    hong = {ten: kq for ten, kq in ds.items() if kq["trang_thai"] != "DAT"}
    if hong and ly_do is None:
        if ds["workspace"].get("ma") == "git_worktree":
            raise Chan(MA_WORKTREE, "workspace la git worktree; dung ban clone doc lap", ds)
        mo_ta = ", ".join(f"{ten}={kq['trang_thai']}" for ten, kq in hong.items())
        raise Chan(MA_PROBE, f"probe nang luc khong dat: {mo_ta}", ds)
    return ds, ly_do


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


def _ghi_so(thu_muc: Path, ban_ghi: dict, khoa_ky: str | None = None) -> None:
    """Ghi sổ NGUYÊN TỬ: ghi tệp tạm rồi đổi tên.

    Người đọc có thể là phiên khác / điện thoại đang poll; đọc trúng lúc ghi dở sẽ
    thấy JSON cụt. os.replace là nguyên tử trên cả POSIX lẫn Windows.
    """
    thu_muc.mkdir(parents=True, exist_ok=True)
    if khoa_ky:
        ban_ghi["chu_ky"] = ky_ban_ghi_luot(ban_ghi, khoa_ky)
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


def _kiem_checkpoint(a, kq) -> str | None:
    path = getattr(a, "resume_checkpoint", None)
    expected = getattr(a, "expected_checkpoint_sha256", None)
    if not path and not expected:
        return None
    try:
        if (not path or not expected or not re.fullmatch(r"[0-9a-f]{64}", expected)
                or not a.expected_head or not a.expected_prompt_sha256):
            raise ValueError("missing resume anchors")
        with Path(path).open("rb") as f:
            data = f.read(4097)
        if len(data) > 4096 or hashlib.sha256(data).hexdigest() != expected:
            raise ValueError("checkpoint changed")
        cp = json.loads(data)
        if (not isinstance(cp, dict) or type(cp.get("schema_version")) is not int
                or cp["schema_version"] != 1
                or set(cp) != {"schema_version", "checkpoint_id", "head", "prompt_sha256"}
                or not isinstance(cp["checkpoint_id"], str)
                or not re.fullmatch(r"[0-9a-f]{32}", cp["checkpoint_id"])
                or cp["head"] != kq["head"]
                or cp["prompt_sha256"] != kq["prompt_sha256"]):
            raise ValueError("resume identity mismatch")
        return cp["checkpoint_id"]
    except (OSError, ValueError, TypeError, KeyError, UnicodeError):
        raise Chan(MA_THAM_SO, "Checkpoint/HEAD/prompt không khớp; chưa materialize hoặc resume") from None


# wp748 r25 (#748 issuecomment-6378484722; đo 24-10-2026, codex-cli 0.163.0) — MODEL DO MÁY CHỦ TRẢ cho từng
# response của lượt codex. `--json`, rollout `~/.codex/sessions` và `logs_2.sqlite` đều KHÔNG có nó (rollout chỉ có
# model CẤU HÌNH); chỉ khung `response.created`/`response.completed` mà máy chủ gửi về mới mang `response.model`, và
# khung ấy chỉ lộ ra ở log trace của target `tungstenite::protocol`. Log trace thô chứa thông tin xác thực (đo được:
# 13 dòng nhắc `authorization`), nên: dòng TRACE/DEBUG và mọi dòng nối tiếp của nó KHÔNG BAO GIỜ chạm đĩa — chỉ
# {response_id, model} được giữ trong bộ nhớ. Bật trace hẹp là để giảm lượng đi qua ống; LỌC mới là chốt.
_RUST_LOG_DO_MODEL = "tungstenite::protocol=trace"
# v r25 vòng 3 (cross-review l909d R25-SEC-01/CONTRACT-07; chủ kho chọn 24-10-2026, spec r25 v2): stderr của lượt
# codex là DANH SÁCH CHO PHÉP NGUYÊN VĂN — chỉ dòng trọn vẹn bằng đúng một mục dưới đây được ghi; mọi byte khác
# bị bỏ và chỉ được ĐẾM. Vòng 1 (chặn dòng nhận ra là trace) và vòng 2 (ghi mọi thứ trước dấu hiệu log đầu tiên)
# đều phải ĐOÁN dòng nào nguy hiểm; ở đây không đoán gì: thứ chạm đĩa là hằng số trong mã.
# Đo 24-10-2026 (codex-cli 0.163.0, --json): phần không phải trace của stderr đúng bằng dòng này, 39 byte.
_STDERR_CHO_PHEP = (b"Reading additional input from stdin...",)
# v r26 (cross-review r26a R26-ALLOW-08): so NGUYÊN VĂN cả kết thúc dòng — đúng `\n` hoặc đúng một `\r\n`;
# `rstrip(b"\r\n")` cũ cắt mọi CR/LF nên `…\r\r\n` lọt qua.
_STDERR_CHO_PHEP_DONG = frozenset(x + duoi for x in _STDERR_CHO_PHEP for duoi in (b"\n", b"\r\n"))
_RE_ANSI_B = re.compile(rb"\x1b\[[0-9;?]*[ -/]*[@-~]")
_DAU_NHAN = rb"^\d{4}-\d\d-\d\dT\S+\s+TRACE\s+tungstenite::protocol: Received message "
_RE_KHUNG = re.compile(_DAU_NHAN + rb"(\{.*\})\s*$")
# v r26 vòng 2 (cross-review r26b R25-EVID-05/R26-CLASSIFY-11): MỘT DÒNG VẬT LÝ được phân loại MỘT lần, khi đã đọc
# hết mọi đoạn của nó — vá theo từng đường reviewer chỉ (token ở đầu dòng, rồi token vắt chỗ cắt, rồi sự kiện khác)
# là đúng cái bẫy "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba". Bốn đường của một dòng:
#   (1) đọc TRỌN trong một đoạn: phân loại theo `type` ĐÃ PARSE (khoá viết bằng escape cũng bắt được), dòng không
#       phải khung thì chỉ tính MẤT khi có token ứng viên;
#   (2) nhiều đoạn hoặc cụt ở EOF: token ứng viên ở BẤT KỲ đâu, kể cả vắt qua chỗ cắt, tính MẤT;
#   (3) không có token mà dòng mở đầu bằng header NHẬN và tiền tố xác nhận một sự kiện KHÁC: không tính;
#   (4) header NHẬN mà không xác nhận được loại: KHÔNG RÕ — không khai là "mất khung", nhưng vẫn chặn DO_DUOC.
# Tìm token qua chỗ cắt: bỏ ANSI rồi bỏ MỌI khoảng trắng (token ứng viên khi ấy dài cố định, không còn `\s*` không
# chặn), giữ đuôi `_DUOI_UNG_VIEN` byte của dạng đã gọn sang đoạn sau. Gọn hoá chỉ mở rộng tập khớp — bảo thủ.
_RE_UNG_VIEN_GON = re.compile(rb'"type":"response\.(?:created|completed)"')
_RE_KHOANG_TRANG_B = re.compile(rb"\s+")
_DUOI_UNG_VIEN = 64
_RE_LOAI_DAU = re.compile(_DAU_NHAN + rb'\{\s*"type"\s*:\s*"([^"\\]*)"')
_RE_DAU_NHAN = re.compile(_DAU_NHAN)
_TRAN_DAU_DONG = 4096         # trần phần đầu dòng giữ lại để xác nhận loại sự kiện của dòng nhiều đoạn
_TRAN_DONG = 4 << 20          # trần một lần đọc (R25-ROBUST-04)
_SU_KIEN_KHUNG = ("response.created", "response.completed")


def _la_codex(lenh) -> bool:
    return Path(lenh[0]).name.lower() in ("codex", "codex.exe", "codex.cmd")


def _loc_stderr_codex(ong, f_err, ket: list, loi: list, dem: dict | None = None) -> None:
    """Đọc stderr của con codex tới EOF, mỗi lần tối đa `_TRAN_DONG` byte. Chỉ dòng TRỌN VẸN (một đoạn, có xuống
    dòng) bằng nguyên văn một mục `_STDERR_CHO_PHEP_DONG` được ghi vào `f_err`; còn lại bỏ và đếm vào `dem`. Khung
    máy chủ chỉ nhận từ dòng trọn vẹn khớp `_RE_KHUNG` (UTF-8 chặt, id và model khác rỗng): {response_id, model,
    su_kien} vào `ket`, khử trùng theo response_id + model. Dòng bị bỏ mà là khung created/completed đọc không được
    thì đếm dem["mat"], dòng NHẬN không xác định được loại thì dem["khong_ro"] (xem bốn đường ở trên) — cả hai
    đều cấm DO_DUOC. Bộ lọc hỏng thì ghi tên lỗi vào `loi` rồi XẢ ống có giới hạn, không ghi gì."""
    dem = {} if dem is None else dem
    try:
        _loc_tung_dong(ong, f_err, ket, dem)
    except Exception as e:
        loi.append(type(e).__name__)
        with contextlib.suppress(Exception):
            for doan in iter(lambda: ong.read(_TRAN_DONG), b""):
                _dem_bo(dem, doan)   # R26-COUNT-09: byte xả đi vẫn là byte bị bỏ


def _phan_loai_khung(sach: bytes):
    """(khung | None, loại) của MỘT dòng đọc trọn: "nhan" · "ung_vien_hong" (đúng sự kiện mà id/model hỏng) ·
    "khac" (khung parse được, sự kiện khác) · None (không phải khung)."""
    k = _RE_KHUNG.match(sach)
    if not k:
        return None, None
    try:
        ev = json.loads(k.group(1).decode("utf-8"))
    except ValueError:
        return None, None
    if not isinstance(ev, dict):
        return None, None
    if ev.get("type") not in _SU_KIEN_KHUNG:
        return None, "khac"
    r = ev.get("response")
    rid, mdl = (r.get("id"), r.get("model")) if isinstance(r, dict) else (None, None)
    if not (isinstance(rid, str) and rid.strip() and isinstance(mdl, str) and mdl.strip()):
        return None, "ung_vien_hong"
    return {"response_id": rid, "model": mdl, "su_kien": ev["type"]}, "nhan"


def _dem_bo(dem: dict, doan: bytes) -> None:
    """Một ĐOẠN ĐỌC bị bỏ (không phải một dòng vật lý: dòng dài hơn `_TRAN_DONG` là nhiều đoạn)."""
    dem["dong_bo"] = dem.get("dong_bo", 0) + 1
    dem["byte_bo"] = dem.get("byte_bo", 0) + len(doan)


def _ghi_het(f_err, doan: bytes, dem: dict) -> None:
    """Ghi `doan` tới hết; phần CHƯA ghi được thì đếm là bỏ (R26-COUNT-09 vòng 2). Hợp đồng: `f_err` là tệp KHÔNG
    ĐỆM (`lenh_run` mở `buffering=0`), nên mỗi `write` là một lời gọi hệ thống — hoặc trả số byte đã ghi, hoặc
    ném mà không ghi byte nào của lời gọi ấy; số byte bỏ vì thế là số ĐO, không phải số đoán."""
    da = 0
    try:
        while da < len(doan):
            n = f_err.write(doan[da:])
            if not n:
                raise OSError("write tra 0 byte")
            da += n
    except ValueError:
        _dem_bo(dem, doan[da:])  # tệp đã đóng vì hậu duệ giữ ống quá hạn chờ: bỏ, không ghi lệch chỗ
    except Exception:
        _dem_bo(dem, doan[da:])
        raise


def _ket_dong(dau: bytes, so_doan: int, tron: bool, ung_vien: bool, ket: list, dem: dict) -> None:
    """Phân loại MỘT dòng vật lý đã bị bỏ, khi đã đọc hết các đoạn của nó (bốn đường ở trên)."""
    if so_doan == 1 and tron:
        m, loai = _phan_loai_khung(_RE_ANSI_B.sub(b"", dau))
        if m is not None:
            if not any(x["response_id"] == m["response_id"] and x["model"] == m["model"] for x in ket):
                ket.append(m)
        elif loai == "ung_vien_hong" or ung_vien:
            dem["mat"] = dem.get("mat", 0) + 1
        return
    if ung_vien:
        dem["mat"] = dem.get("mat", 0) + 1
        return
    sach = _RE_ANSI_B.sub(b"", dau)
    k = _RE_LOAI_DAU.match(sach)
    if k:
        try:
            loai = k.group(1).decode("utf-8")
        except UnicodeDecodeError:
            loai = None          # loại không đọc được chặt: KHÔNG xác nhận là sự kiện khác
        if loai is not None and loai not in _SU_KIEN_KHUNG:
            return
    if _RE_DAU_NHAN.match(sach):
        dem["khong_ro"] = dem.get("khong_ro", 0) + 1


def _loc_tung_dong(ong, f_err, ket: list, dem: dict) -> None:
    het_dong = True              # đoạn trước kết thúc bằng xuống dòng: đoạn tới mở một dòng mới
    dau, duoi, ung_vien, so_doan = b"", b"", False, 0
    for doan in iter(lambda: ong.readline(_TRAN_DONG), b""):
        if het_dong:
            dau, duoi, ung_vien, so_doan = b"", b"", False, 0
        het_dong = doan.endswith(b"\n")
        so_doan += 1
        if so_doan == 1 and het_dong and doan in _STDERR_CHO_PHEP_DONG:
            _ghi_het(f_err, doan, dem)
            continue
        _dem_bo(dem, doan)
        if so_doan == 1:
            dau = doan               # dòng một đoạn cần TRỌN đoạn để parse
        elif len(dau) < _TRAN_DAU_DONG:
            dau = (dau + doan)[:max(len(dau), _TRAN_DAU_DONG)]
        gon = _RE_KHOANG_TRANG_B.sub(b"", _RE_ANSI_B.sub(b"", duoi + doan))
        ung_vien = ung_vien or bool(_RE_UNG_VIEN_GON.search(gon))
        duoi = gon[-_DUOI_UNG_VIEN:]
        if het_dong:
            _ket_dong(dau, so_doan, True, ung_vien, ket, dem)
    if not het_dong:
        _ket_dong(dau, so_doan, False, ung_vien, ket, dem)


def _ket_luan_model(ket: list, loi: list, con_doc: bool, mat: int = 0, khong_ro: int = 0) -> tuple:
    """(trạng thái, lý do). DO_DUOC chỉ khi CÓ khung, bộ lọc KHÔNG hỏng, đã đọc tới EOF, không mất khung nào và
    không có dòng NHẬN nào không rõ loại."""
    if loi:
        return "KHONG_DO_DUOC", f"bo loc stderr hong ({loi[0]}); phan con lai cua stderr da bi bo"
    if con_doc:
        return "KHONG_DO_DUOC", "ong stderr con mo sau 10s (hau due giu ong); danh sach co the thieu"
    if mat:
        return "KHONG_DO_DUOC", f"{mat} dong giong khung response.created/completed khong doc duoc; danh sach thieu"
    if khong_ro:
        return "KHONG_DO_DUOC", (f"{khong_ro} dong Received message vuot tran doc, khong xac dinh duoc loai su kien; "
                                 "danh sach co the thieu")
    if not ket:
        return "KHONG_DO_DUOC", ("khong thay khung response.created/response.completed nao mang model "
                                 "trong stderr cua con; KHONG suy tu -m hay cau hinh")
    return "DO_DUOC", None


class _BoLocStderr:
    """Toàn bộ trạng thái đo của một lượt codex trong MỘT đối tượng (R25-TEST-03): `lenh_run` chỉ trao đối tượng, nên
    không còn đối số rời nào để một lời gọi lỡ tay thay bằng giá trị rỗng. `ket_thuc` làm ĐÚNG THỨ TỰ chờ có hạn →
    CHỐT trạng thái luồng → đóng tệp (R26-EOF-10): phần đọc xong trong lúc đóng tệp không còn chỗ ghi đúng, nên
    không được tính là đọc tới EOF đúng hạn."""

    def __init__(self, ong, f_err):
        self.ong, self.f_err = ong, f_err
        self.ket: list = []
        self.loi: list = []
        self.dem: dict = {}
        self.con_doc = None      # None = chưa chốt, coi như còn đọc; True/False = chốt lúc join trả về
        self.luong = threading.Thread(target=_loc_stderr_codex, args=(ong, f_err, self.ket, self.loi, self.dem),
                                      daemon=True)

    def bat_dau(self) -> None:
        try:
            self.luong.start()
        except Exception as e:
            # Không sinh được luồng đọc thì không ai đọc ống: con sẽ treo khi ống đầy. Ghi lỗi (cấm DO_DUOC) và ĐÓNG
            # đầu đọc để lần ghi stderr kế tiếp của con nhận EPIPE thay vì chặn.
            self.loi.append(type(e).__name__)
            with contextlib.suppress(Exception):
                self.ong.close()

    def ket_thuc(self, han: float) -> None:
        if self.luong.ident is not None:     # luồng chưa từng chạy (bat_dau hỏng) thì không có gì để chờ
            self.luong.join(timeout=han)
            self.con_doc = self.luong.is_alive()
        self.f_err.close()

    def ghi_so(self, ban_ghi: dict) -> None:
        """Chốt kết quả vào sổ từ MỘT ảnh chụp (R25-RACE-06): trạng thái luồng đã chốt ở `ket_thuc`, rồi mới chụp
        danh sách/lỗi/bộ đếm; trạng thái và các trường ghi sổ suy từ cùng ảnh chụp ấy."""
        con_doc = True if self.con_doc is None else self.con_doc
        ket_s, loi_s, dem_s = list(self.ket), list(self.loi), dict(self.dem)
        tt, ld = _ket_luan_model(ket_s, loi_s, con_doc, dem_s.get("mat", 0), dem_s.get("khong_ro", 0))
        ban_ghi["model_phuc_vu"] = ket_s
        ban_ghi["model_phuc_vu_trang_thai"] = tt
        if ld:
            ban_ghi["model_phuc_vu_ly_do"] = ld
        ban_ghi["stderr_bo_dong"] = dem_s.get("dong_bo", 0)   # số ĐOẠN ĐỌC bị bỏ, xem _dem_bo
        ban_ghi["stderr_bo_byte"] = dem_s.get("byte_bo", 0)


def lenh_run(a) -> int:
    # Git/probes must never inherit the snapshot, including rejected resumes.
    snapshot = os.environ.pop("CODEX_AUTH_JSON", "")
    if not a.lenh:
        raise Chan(MA_THAM_SO, "thieu lenh de chay (dat sau dau --)")
    kq = chay_cac_chot(a)
    resume_id = _kiem_checkpoint(a, kq)
    if snapshot:
        ket = chuan_bi_xac_thuc(that_su=True, snapshot=snapshot)
        snapshot = ""
        if not ket or not all(x.get("ok") for x in ket):
            raise Chan(MA_CHUA_XAC_THUC, "Không chuẩn bị được Codex credential; chưa chạy child")
    if _la_codex(a.lenh):
        if _cho_snapshot_hoac_chan():
            raise Chan(MA_CHUA_XAC_THUC, "CHỜ snapshot Codex mới; không lặp credential đã thất bại")
    try:
        probe, ly_do_bo_qua = chay_cac_probe(kq["workspace"], a.lenh, a.bo_qua_probe)
    except Chan as e:
        if e.probe is None:
            raise
        run_root = Path(a.run_root).expanduser().resolve()
        rid, sid = _cap_id(run_root)
        luc = _bay_gio().isoformat()
        _ghi_so(run_root / sid, {
            "version": VERSION, "run_id": rid, "short_id": sid, "ten": a.name,
            "lenh": _tom_tat_lenh(a.lenh), "trang_thai": "hong", "giai_doan": "probe",
            "bat_dau_utc": luc, "ket_thuc_utc": luc, "ma_thoat": e.ma,
            "ly_do_dung": e.thong_diep, "pid": None, "khoa_danh_tinh": None,
            **kq, **_dinh_danh_van_chuyen(a.lenh),
            "probe": _probe_cho_so(e.probe), "bo_qua_probe_ly_do": None,
        })
        raise
    kq.update(probe=_probe_cho_so(probe), bo_qua_probe_ly_do=ly_do_bo_qua)
    if bool(a.attempt_state) != bool(a.void_reason):
        raise Chan(MA_THAM_SO, "--attempt-state và --void-reason phải đi cùng nhau")
    khoa_ky = None
    neo = None
    if a.attempt_state:
        try:
            st = json.loads(Path(a.attempt_state).read_text(encoding="utf-8"))
            neo = st["attempt_anchor"]
            if (not st.get("attempt_open") or neo.get("consumed")
                    or not re.fullmatch(r"[0-9a-f]{32}", neo["nonce"])
                    or not re.fullmatch(r"[0-9a-f]{64}", st["hmac_key"])):
                raise ValueError("neo không thuộc lượt đang mở")
            khoa_ky = st["hmac_key"]
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as e:
            raise Chan(MA_THAM_SO, f"không đọc được neo lượt từ --attempt-state: {e}") from None
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
        **kq, **_dinh_danh_van_chuyen(a.lenh),
    }
    if neo:
        ban_ghi.update(nonce=neo["nonce"], attempt=neo["attempt"], void_reason=a.void_reason)
    if resume_id:
        ban_ghi["resumed_from_checkpoint"] = resume_id
    if kq.get("prompt_sha256"):
        checkpoint = {"schema_version": 1, "checkpoint_id": rid,
                      "head": kq["head"], "prompt_sha256": kq["prompt_sha256"]}
        data = (json.dumps(checkpoint, sort_keys=True) + "\n").encode("utf-8")
        with (thu_muc / "checkpoint.json").open("xb") as f:
            f.write(data)
        ban_ghi["checkpoint_sha256"] = hashlib.sha256(data).hexdigest()
    _ghi_so(thu_muc, ban_ghi, khoa_ky)

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
        _ghi_so(thu_muc, ban_ghi, khoa_ky)
    elif any("{PROMPT_FILE}" in x for x in lenh_con):
        # Có chỗ thay mà không có gì để thay: con nhận CHUỖI NGUYÊN VĂN
        # "{PROMPT_FILE}" làm đường dẫn, rc=0, sổ ghi "xong" — người vận hành tin
        # prompt đã được neo còn agent nhận một đường dẫn vô nghĩa. Im lặng ở đây
        # là fail-open, nên chặn hẳn.
        raise Chan(MA_THAM_SO,
                   "lenh co {PROMPT_FILE} nhung khong truyen --prompt-file: "
                   "con se nhan chuoi nguyen van")

    f_out = (thu_muc / "stdout.log").open("w", encoding="utf-8")
    do_model = _la_codex(a.lenh)
    # Lượt codex: stderr đi qua ỐNG và bộ lọc danh sách cho phép, tệp mở nhị phân để ghi đúng byte.
    # Không đệm (R26-COUNT-09 vòng 2): mỗi write là một lời gọi hệ thống, nên `_ghi_het` đếm được đúng phần chưa ghi.
    f_err = (thu_muc / "stderr.log").open("wb" if do_model else "w",
                                          **({"buffering": 0} if do_model else {"encoding": "utf-8"}))
    them = {}
    bo_loc = None
    if do_model:
        env = dict(os.environ)
        # GHI ĐÈ, không nối: RUST_LOG thừa kế có thể bật target khác mang credential (R25-SEC-01).
        rust_log_cu = env.get("RUST_LOG")
        env["RUST_LOG"] = _RUST_LOG_DO_MODEL
        if rust_log_cu:
            ban_ghi["model_phuc_vu_rust_log_ke_thua_bi_ghi_de"] = True
        them["env"] = env
    if platform.system() == "Windows":
        them["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        # nhóm tiến trình riêng: điều kiện CẦN để giết được cả con cháu sau này
        them["start_new_session"] = True
    try:
        p = subprocess.Popen(lenh_con, cwd=kq["workspace"],
                             stdout=f_out, stderr=subprocess.PIPE if do_model else f_err,
                             stdin=subprocess.DEVNULL, **them)
        if do_model:
            bo_loc = _BoLocStderr(p.stderr, f_err)
            bo_loc.bat_dau()
    except (OSError, ValueError) as e:
        if isinstance(e, ValueError):
            ban_ghi.pop("void_reason", None)
        ban_ghi.update(trang_thai="hong", ly_do_dung=f"khong chay duoc lenh: {e}",
                       ket_thuc_utc=_bay_gio().isoformat())
        _ghi_so(thu_muc, ban_ghi, khoa_ky)
        f_out.close(); f_err.close()
        raise Chan(MA_THAM_SO, f"khong chay duoc lenh: {e}")

    # Once a child has started, a timeout/nonzero exit does not prove its cause.
    # Keep the requested label for audit, not as a machine-void certificate.
    # The existing consumer rejects a signed record without void_reason.
    requested_void = ban_ghi.pop("void_reason", None)
    if requested_void:
        ban_ghi["void_reason_requested"] = requested_void
    ban_ghi["failure_class"] = "unknown"

    # Nhot con vao Job Object NGAY sau khi sinh: chi co no giu duoc hau due mo coi
    # tren Windows (xem `_job_windows`). Tren POSIX tra None, khong anh huong gi.
    job = _job_windows(p.pid)
    khoa = _khoa_danh_tinh(p.pid)
    ban_ghi.update(pid=p.pid, khoa_danh_tinh=khoa)
    if platform.system() == "Windows":
        ban_ghi["job_windows"] = job is not None
    if khoa is None:
        # Nói RÕ vì sao thiếu, đừng để phía đọc phải đoán. Con thoát quá nhanh là
        # ca lành; không lấy được khoá cho một tiến trình CÒN SỐNG mới là ca đáng lo.
        ban_ghi["khoa_thieu_ly_do"] = ("con da thoat truoc khi lay duoc khoa"
                                       if p.poll() is not None
                                       else "khong doc duoc danh tinh du tien trinh con song")
    _ghi_so(thu_muc, ban_ghi, khoa_ky)
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
                ket_giet = _giet_cay(p.pid, khoa, job)
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
        ban_ghi["ly_do_dung"] = "bi ngat: " + _giet_cay(p.pid, khoa, job).mo_ta
        bi_ngat = True
        ma = 130
    finally:
        f_out.close()
        if bo_loc is not None:
            # Hậu duệ còn giữ ống thì EOF không tới: chờ có hạn, CHỐT trạng thái, rồi mới đóng tệp — trong một lời gọi.
            bo_loc.ket_thuc(10)
        else:
            f_err.close()
    if bo_loc is not None:
        bo_loc.ghi_so(ban_ghi)

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
    ket_thuc = _bay_gio()
    ban_ghi.update(ket_thuc_utc=ket_thuc.isoformat(), ma_thoat=ma_that)
    # wp484 g7 (connector P2 17-10, đo: run `47cf857e` ghi `xong`/0/`unknown`) — nhãn
    # "unknown" gán lúc con vừa sinh là đúng cho lượt chết GIỮA chừng; lượt đã CHẠY HẾT
    # và thoát 0 thì không có failure nào để phân lớp, giữ nhãn là khai sai trong sổ.
    if ban_ghi["trang_thai"] == "xong" and ma_that == 0:
        ban_ghi.pop("failure_class", None)
    # BẰNG CHỨNG ĐỊNH LƯỢNG cho câu "xong" — xem CẢNH BÁO ở đầu tệp. `trang_thai`
    # và `ma_thoat` chỉ nói về vòng đời tiến trình; ba số dưới đây là thứ duy nhất
    # trong sổ phân biệt được "đã làm" với "thoát 0 mà chưa làm gì". Tính ở đây
    # chứ không bắt người đọc tự trừ hai mốc thời gian: một phép tính phải làm tay
    # là một phép tính sẽ bị bỏ qua đúng lúc cần nhất.
    try:
        bat_dau = datetime.fromisoformat(ban_ghi["bat_dau_utc"])
        ban_ghi["thoi_luong_giay"] = round((ket_thuc - bat_dau).total_seconds(), 3)
    except (ValueError, KeyError, TypeError):
        ban_ghi["thoi_luong_giay"] = None    # không đo được thì nói KHÔNG ĐO ĐƯỢC
    for ten, ten_bam, tep in (("stdout_byte", "stdout_sha256", "stdout.log"),
                              ("stderr_byte", "stderr_sha256", "stderr.log")):
        try:
            duong = thu_muc / tep
            ban_ghi[ten] = duong.stat().st_size
            bam = hashlib.sha256()
            with duong.open("rb") as f:
                for khoi in iter(lambda: f.read(1024 * 1024), b""):
                    bam.update(khoi)
            ban_ghi[ten_bam] = bam.hexdigest()
        except OSError:
            ban_ghi[ten] = None
            ban_ghi[ten_bam] = None
    _ghi_so(thu_muc, ban_ghi, khoa_ky)
    if a.json:
        print(json.dumps(ban_ghi, ensure_ascii=False))
    else:
        print(f"trang thai: {ban_ghi['trang_thai']}  ma_thoat={ma}")
        # In CẠNH nhau, không để người đọc phải mở sổ mới thấy: "xong ma_thoat=0"
        # đứng một mình là câu dễ tin nhất và cũng dễ sai nhất.
        print(f"thoi luong: {ban_ghi.get('thoi_luong_giay')}s  "
              f"stdout={ban_ghi.get('stdout_byte')}B  "
              f"stderr={ban_ghi.get('stderr_byte')}B")
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
                           ("short_id", "ten", "trang_thai", "ma_thoat", "bat_dau_utc",
                            "thoi_luong_giay", "stdout_byte", "stderr_byte")})
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
    if not pid:
        raise Chan(MA_THAM_SO, "so khong co pid")
    if khoa is None:
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
    ket = _giet_cay(int(pid), khoa)
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
    # `ci: False` — KHÔNG phải nới tay, mà vì một fail-close đặt sai chỗ ở đây TẮT
    # LUÔN PHÉP ĐO. Đã trả giá đúng một lượt: `launcher-windows.yml` chỉ cài `rg` rồi
    # chạy `doctor`; đặt `claude`/`codex` bắt buộc làm `doctor` trả 12 trên CẢ hai nền,
    # và mọi bước sau — 110 ca, 66 đột biến, bốn probe Windows — bị SKIP sạch. Runner CI
    # ĐO chính launcher, nó không chạy phiên agent, nên đòi chuỗi công cụ agent ở đó là
    # đòi sai thứ. Cùng câu kho đã ghi: cổng tự tắt khi thiếu công cụ là cổng không tồn
    # tại đúng lúc nó cần nhất.
    {"ten": "claude", "bat_buoc": {"mac_dinh": True, "remote": True, "ci": False},
     "ung_vien": ["claude"],
     "vi_sao": "CLI chinh thuc de goi phien Claude (khong tu viet script spawn)",
     "cai": {"*": "npm install -g @anthropic-ai/claude-code"},
     # `claude auth status` in JSON co cau truc (`loggedIn`, `authMethod`), tuc
     # co the DOC va doi chieu — khac han `codex login status` ngay duoi.
     "xac_thuc": ["auth", "status"]},
    {"ten": "codex", "bat_buoc": {"mac_dinh": True, "remote": True, "ci": False},
     "ung_vien": ["codex"],
     "vi_sao": "CLI chinh thuc de goi phien Codex (khong tu viet script spawn)",
     "cai": {"*": "npm install -g @openai/codex"}},
    # CO Y KHONG khai `xac_thuc` cho codex, du nhanh nguon co khai `["login","status"]`.
    # CLAUDE.md ghi thang: **`codex login status` NOI DOI** — rc=0 "Logged in" trong khi
    # moi loi goi tra 401, va kho DA TRA GIA HAI lan vi tin no. `_xac_thuc` ket luan
    # "dat" khi rc=0 va co dau ra, dung hai dieu ma ban noi doi thoa man => no bien
    # tin hieu SAI THANH XANH thanh mot cong. Do 17-08-2026 tai container nay:
    # `codex login status` rc=0 "Logged in using ChatGPT" VA `codex exec` that su chay
    # (rc=0) — hai ben DONG Y hom nay. Mot mau dong y KHONG chung minh probe dang tin;
    # kho da do no BAT DONG truoc day. Cong chi duoc dung tin hieu KIEM CHUNG DUOC.
    # Muon do auth cua codex thi phai do bang mot loi goi THAT (vd `codex exec` mot
    # cau lenh re) chu khong hoi `login status` — viec do thuoc buoc 3.
    # rg (ripgrep): codex và Claude Code đều gọi nó để tìm trong mã. Nhanh hơn grep
    # nhiều lần, tôn trọng .gitignore, và đọc UTF-8 đúng — quan trọng với kho tiếng
    # Việt, nơi `findstr` của Windows đọc sai dấu.
    #
    # BẮT BUỘC từ 15-08-2026 (trước đó là tuỳ chọn, lý do cũ: "mọi chốt trong tệp này
    # chạy được khi thiếu nó"). Lý do cũ đúng về LAUNCHER và sai về VIỆC: thiếu `rg`
    # thì lệnh tìm của agent gãy giữa chừng chứ KHÔNG tự lùi về `grep`, nên phiên mất
    # khả năng tra cứu mà không báo lỗi ở chỗ đọc được. Một công cụ mà thiếu nó phiên
    # vẫn "chạy" nhưng làm việc sai thì nguy hơn công cụ thiếu là chết ngay.
    # wp802 (Q5/Q6): PHẢI khớp `rg.cai` của ops/cong_cu.yaml và hook — `r802_bang_cai_rg_khop_cong_cu_yaml`.
    {"ten": "rg", "bat_buoc": True, "ung_vien": ["rg"],
     "vi_sao": "tim trong ma - codex/Claude Code goi rg; findstr doc sai dau tieng Viet",
     "cai": {"Windows": "winget install --id BurntSushi.ripgrep.MSVC -e"
                        " --accept-source-agreements --accept-package-agreements"
                        " --disable-interactivity"
                        " || choco install ripgrep --yes --no-progress",
             "Darwin": "brew install ripgrep",
             "Linux": "sudo apt-get install -y ripgrep"}},
    # bash: `.claude/settings.json` gọi hook qua bash và session-start.sh là bash
    # script. Máy Windows KHÔNG có Git Bash thì hook hỏng, mà doctor cũ vẫn in
    # "DU CONG CU BAT BUOC" — đo thiếu đúng chỗ môi trường phụ thuộc (audit vòng 3).
    {"ten": "bash", "bat_buoc": True, "ung_vien": ["bash"],
     "vi_sao": "hook SessionStart la bash script; Windows can Git Bash",
     "cai": {"Windows": "winget install --id Git.Git -e  (kem Git Bash)",
             "Darwin": "co san", "Linux": "sudo apt-get install -y bash"}},
    # gh — BAT BUOC THEO NEN, khong phai mot bool chung cho moi noi.
    #
    # Day la ket luan cua BUOC 3, va no khac ca hai phia truoc do. Nhanh nguon khai
    # `bat_buoc: True` (ADR-0017: PR/Issue la nguon su that dieu phoi, nen mat `gh`
    # la mat duong du phong). Buoc 2 cua toi ha xuong `False` voi ly do "proxy chan
    # api.github.com" — LY DO AY SAI VE CHI TIET, do lai 17-08-2026 moi ro:
    #
    #   /rate_limit          -> 200, CO header X-GitHub-*   (toi GitHub)
    #   /user                -> 200, CO header X-GitHub-*   (toi GitHub)
    #   /repos/<kho>         -> 403, KHONG header GitHub    (proxy tu sinh)
    #   /repos/<kho>/pulls/N -> 403, KHONG header GitHub    (proxy tu sinh)
    #   co token va khong token: KET QUA Y HET => chinh sach theo DUONG DAN,
    #   khong theo danh tinh (dung nhu CLAUDE.md ghi).
    #
    # Nen su that KHONG phai "gh khong ket noi duoc" ma la mot thu NGUY HIEM HON:
    # `gh auth status` hoi `/user` — duong DUOC PHEP — nen no bao "da xac thuc"
    # ngon lanh, roi MOI lenh viec that (`gh pr view`, `gh api repos/...`) an 403.
    # Mot cong cu qua duoc phep tu kiem ma khong lam noi viec thi TE HON cong cu
    # vang mat: no bien mot loi ha tang thanh mot loi "chac tai quyen token", va
    # nguoi doc di sai huong. Dung ho `codex login status` NOI DOI.
    #
    # Vi vay: BAT BUOC o may nguoi dung (noi gh chay that va la duong du phong
    # thuc su), KHONG bat buoc o phien remote (noi no chi biet noi doi). Mot bool
    # chung se phai sai o mot trong hai noi. `doctor` van LUON do va in ca hai
    # duong REST, de khong ai ket luan tu duong hong.
    {"ten": "gh", "bat_buoc": {"mac_dinh": True, "remote": False, "ci": False},
     "ung_vien": ["gh"],
     "vi_sao": "duong du phong/chan doan GitHub; o remote kho di bang MCP github + git",
     "cai": {"Windows": "winget install --id GitHub.cli -e  (hoac: choco install gh -y)",
             "Darwin": "brew install gh", "Linux": "sudo apt-get install -y gh"}},
    # npm: session-start.sh rẽ nhánh trên `co npm`, không phải trên `node`.
    {"ten": "npm", "bat_buoc": False, "ung_vien": ["npm"],
     "vi_sao": "hook cai hai CLI agent bang npm; co node chua chac co npm",
     "cai": {"Windows": "winget install --id OpenJS.NodeJS.LTS -e",
             "Darwin": "brew install node", "Linux": "sudo apt-get install -y npm"}},
    {"ten": "node", "bat_buoc": False, "ung_vien": ["node"],
     "vi_sao": "can de cai hai CLI tren",
     "cai": {"Windows": "winget install --id OpenJS.NodeJS.LTS -e",
             "Darwin": "brew install node", "Linux": "sudo apt-get install -y nodejs npm"}},
    {"ten": "llm", "bat_buoc": False, "ung_vien": ["llm"],
     "vi_sao": "CLI client goi OpenAI API (provider: openai_api, surface: llm_cli)",
     "cai": {"*": "pip install llm  (hoac: uv tool install llm / brew install llm)"}},
    {"ten": "agy", "bat_buoc": False, "ung_vien": ["agy"],
     "vi_sao": "CLI client cho Google Antigravity (provider: google_antigravity, surface: antigravity)",
     "cai": {"Windows": "irm https://antigravity.google/cli/install.ps1 | iex",
             "Darwin": "curl -fsSL https://antigravity.google/cli/install.sh | bash",
             "Linux": "curl -fsSL https://antigravity.google/cli/install.sh | bash"},
     "xac_thuc": ["models"]},
    {"ten": "actionlint", "bat_buoc": False, "ung_vien": ["actionlint"],
     "vi_sao": "kiem tra cu phap va schema cua GitHub Actions workflow (M1)",
     "cai": {"*": "winget/brew install actionlint, hoac bash ops/cai_actionlint.sh"}},
    {"ten": "shellcheck", "bat_buoc": False, "ung_vien": ["shellcheck"],
     "vi_sao": "tinh huong va bat loi shell script trong kho (M1)",
     "cai": {"*": "winget/brew/apt-get install shellcheck"}},
]

# MODULE PYTHON — bảng RIÊNG, cố ý không nhét vào `CONG_CU`.
#
# `CONG_CU` đo bằng `shutil.which`, tức đo LỆNH TRÊN PATH. PyYAML không có binary
# nào cả: `which pyyaml` không bao giờ thấy gì. Thêm nó vào bảng trên thì `doctor`
# sẽ báo "thiếu" trên MỌI máy, kể cả máy đã cài — một chốt luôn đỏ là chốt sẽ bị bỏ
# qua, và bỏ qua được một chốt thì bỏ qua được cả bảng.
#
# `bat_buoc: False` là ĐO ĐƯỢC chứ không phải nhân nhượng: `launcher.py` KHÔNG import
# yaml (đo 16-08-2026: 0 lần nhắc trong cả tệp). Người cần nó là `ops/lease_publish.py`
# và `ops/lease_publish_test.py`. Đặt bắt buộc sẽ làm `doctor` thoát 12 trên máy chỉ
# gọi agent mà không đụng đường ops — chặn oan, và chặn oan cũng là một dạng nói dối.
#
# VÌ SAO ĐÁNG CÓ MỤC NÀY: thiếu PyYAML thì cổng đăng lease chết bằng `ImportError`
# giữa chừng chứ không nói "thiếu phụ thuộc". `ops/lease_publish.py` đã cố dịch câu
# ấy sang "thiếu PyYAML — `pip install pyyaml`", nhưng chỉ ở nhánh nó chạy được tới;
# hỏi TRƯỚC vẫn rẻ hơn hỏng GIỮA CHỪNG. Từ 16-08-2026 cả `ci.yml` lẫn
# `ops-publish-lease.yml` ghim `PyYAML==6.0.3`, nên máy dev lệch bản với CI là chuyện
# đọc được ngay ở đây thay vì đọc trong log CI.
MODULE_PY = [
    {"ten": "yaml", "goi_la": "PyYAML", "bat_buoc": False,
     "vi_sao": "ops/lease_publish.py + bo phan chung cua no doc/ghi lease bang YAML",
     "cai": {"*": "python -m pip install PyYAML==6.0.3   (dung so voi ci.yml)"}},
]


# HẠN PROBE PHỤ THUỘC NỀN — đo trên `windows-latest` 17-08-2026, KHÔNG phải đoán.
#
# Mốc 8s đặt theo cảm giác trên Linux đã dán nhãn SAI cho hai công cụ có thật và chạy
# được: `gh.EXE` và `npm.CMD` đều báo `KHONG chay duoc: timeout sau 8.0s`. Khởi động
# NGUỘI một `.EXE`/`.CMD` trên runner Windows (Defender quét lần đầu, `.CMD` còn phải
# qua `cmd.exe`) vượt xa 8s. Trên máy người dùng `gh` là BẮT BUỘC, nên mốc ấy làm
# `doctor` đỏ oan đúng chỗ nó phải đáng tin nhất.
#
# Đây là cùng lớp "chạy được ở đây" với hằng số: một con số hợp lý ở nền này là một
# chốt nói dối ở nền kia. Trần TỔNG cũng phải giãn theo, kẻo nới hạn từng probe rồi
# lại đụng trần chung và ra đúng nhãn sai ấy bằng đường khác.
# Bản môi trường ĐÃ CHUẨN HOÁ của lượt `doctor` đang chạy — đặt trong `lenh_doctor`.
# Bảng KHA_NANG gọi `_do_github` qua lambda nên không nhận được tham số; để `None`
# thì probe lại rơi về `os.environ` tức đúng bản giữ chỗ mà ta vừa loại.
_MOI_TRUONG_DA_DOC: dict[str, str] | None = None

# KẾT QUẢ PROBE XÁC THỰC CỦA LƯỢT `doctor` ĐANG CHẠY — khoá (đường dẫn, đối số), giá
# trị là bộ bốn của `_xac_thuc_kem_dau_ra` (ok, mô tả, quá hạn, đầu ra gộp).
# Vì sao có: cross-review PR "#426" (codex, P2 trên `4639462`) — `lenh_doctor` đã chạy
# `agy models` cho bảng `CONG_CU` (`xac_thuc`), rồi `_do_antigravity` ở khối `KHA_NANG`
# chạy lại CÙNG lệnh ấy chỉ để kết luận lại một chuyện đã có bằng chứng. `models` đi
# mạng: lần hai có thể quá hạn/ném trong khi lần một đã dương, và cổng tự lật kết
# luận. Nên mỗi lượt `doctor` chạy probe ĐÚNG MỘT LẦN và mọi phép đo sau đọc lại.
# Chỉ `lenh_doctor` ghi; `lenh_doctor` xoá sạch khi bắt đầu để lượt sau không đọc
# ảnh chụp của lượt trước. Gọi `_do_antigravity` NGOÀI `doctor` thì bảng rỗng và nó
# tự chạy probe như cũ — hợp đồng độc lập của hàm không đổi.
_XAC_THUC_DA_DO: dict[tuple[str, tuple[str, ...]], tuple[bool, str, bool, str]] = {}

_LA_WINDOWS = platform.system() == "Windows"
PROBE_TIMEOUT_GIAY = 25.0 if _LA_WINDOWS else 8.0


def _tran_doctor() -> float:
    """Trần TỔNG suy từ SỐ PHÉP ĐO, không phải một con số chọn tay.

    Lỗi của bản trước (P2 cross-review PR "#143"): 120s là số tôi chọn cho "có vẻ
    rộng", trong khi bảng có thể chạy 9+ probe `--version` cộng probe auth, mỗi cái
    được phép tới 25s. Một chuỗi khởi động nguội HỢP LỆ ~13–20s là đủ vét sạch 120s
    TRƯỚC KHI đo tới các công cụ cuối bảng — rồi chúng bị báo là thiếu dù KHÔNG cái
    nào vượt hạn riêng. Tức trần tổng biến "hết ngân sách" thành "công cụ hỏng":
    đúng cái nhãn sai mà đợt này vừa đi sửa, chỉ khác đường tới.

    Nên trần phải LỚN LÊN THEO BẢNG. Cộng cả mục `xac_thuc` vì chúng cũng tiêu hạn,
    và cộng biên cho phần đo khả dụng chạy SAU vòng lặp.
    """
    # ĐẾM ĐÚNG SỐ PROBE SẼ CHẠY, không đếm số DÒNG trong bảng (P2 review "#143").
    # `_cac_duong_dan` trả MỌI executable khớp trong PATH — `python` có ba ứng viên
    # (`python3`/`python`/`py`), và một máy có nhiều bản `rg` thì mỗi bản là một
    # probe. Lấy `len(CONG_CU)` là giả định mỗi công cụ đúng một phép đo, tức lại
    # đặt trần theo thứ ta MONG chứ không theo thứ sẽ CHẠY.
    moi_truong = dict(os.environ)
    so_probe = 0
    for c in CONG_CU:
        try:
            n = len(_cac_duong_dan(c, moi_truong))
        except OSError:
            n = len(c.get("ung_vien") or [1])
        so_probe += max(1, n) + (1 if c.get("xac_thuc") else 0)
    return max(30.0, PROBE_TIMEOUT_GIAY * so_probe + 30.0)


def _bat_buoc(c: dict, moi_truong: dict[str, str]) -> bool:
    """Giải `bat_buoc` — bool, hoặc bảng theo NỀN.

    Vì sao cần: "công cụ này có bắt buộc không" KHÔNG có một câu trả lời đúng cho
    mọi nơi. `gh` là đường dự phòng thật trên máy người dùng, và là thứ chỉ biết
    nói dối trong container remote (xem chú thích tại mục `gh`). Ép một bool
    chung thì chắc chắn sai ở một trong hai nền — và cái sai đó là fail-close,
    tức nó CHẶN phiên chứ không chỉ báo nhầm.

    Khoá `remote` đọc `CLAUDE_CODE_REMOTE`, đúng biến mà `session-start.sh` đã
    dùng để quyết có cài gì không — một nguồn, không phải hai.
    """
    bb = c["bat_buoc"]
    if isinstance(bb, bool):
        return bb
    # CI ĐỨNG TRƯỚC `remote`: một runner có thể mang cả hai dấu, mà việc của nó
    # hẹp hơn hẳn — nó ĐO chính launcher, không phải chạy phiên agent.
    if moi_truong.get("GITHUB_ACTIONS") == "true" or moi_truong.get("CI") == "true":
        return bool(bb.get("ci", bb["mac_dinh"]))
    if moi_truong.get("CLAUDE_CODE_REMOTE", "") == "true":
        return bool(bb["remote"])
    return bool(bb["mac_dinh"])


def _doc_moi_truong() -> tuple[dict[str, str], dict]:
    """Chụp môi trường MỘT LẦN, trước khi resolve/chạy bất kỳ công cụ nào.

    Bản công khai chỉ ghi CÓ/KHÔNG và nguồn credential, tuyệt đối không ghi giá
    trị. Bản đầy đủ chỉ truyền cho tiến trình con. `GITHUB_PAT` là tên biến cũ
    của kho; gh chính thức đọc `GH_TOKEN`, nên ánh xạ trong môi trường CON thay
    vì ghi credential xuống đĩa hoặc sửa môi trường cha.

    Thứ tự "đọc env TRƯỚC khi hỏi công cụ" là chốt của bài học 15-08-2026: gặp
    `Not logged in` mà chưa biết công cụ xác thực bằng ĐƯỜNG NÀO thì kết luận
    "không dùng được" là đoán, không phải đo.
    """
    con = dict(os.environ)                 # thao tác đầu tiên: đọc toàn bộ env
    path = con.get("PATH", "")

    # BIẾN GIỮ CHỖ TỆ HƠN BIẾN CHƯA ĐẶT — và ở đây nó đổi hẳn kết luận.
    #
    # Thứ tự "GH_TOKEN trước, GITHUB_PAT sau" là thứ tự ĐÚNG THEO TÀI LIỆU của gh,
    # nhưng SAI trong container này, và đã ĐO 17-08-2026: `GH_TOKEN` `GITHUB_TOKEN`
    # (cùng `AWS_*`, `CLOUDSDK_*`) đều mang CÙNG một chuỗi giữ chỗ 14 ký tự, còn
    # credential GitHub thật nằm ở `GITHUB_PAT` (93 ký tự). Lấy theo thứ tự tài liệu
    # là chọn đúng cái giữ chỗ, rồi báo `nguon_xac_thuc_github: GH_TOKEN` — một dòng
    # đọc như "đã có credential" trong khi công cụ sẽ nhận "sai thông tin đăng nhập".
    # CLAUDE.md ghi sẵn cái bẫy này; nó chỉ lộ ra vì lượt đo đầu tiên in ra dòng ấy.
    #
    # DẤU HIỆU máy đọc được, không cần đoán danh sách tên: một "token GitHub" mà
    # TRÙNG BYTE với một biến chẳng liên quan gì tới GitHub (khoá AWS, token gcloud)
    # thì không phải credential — đó là chuỗi giữ chỗ dùng chung. So bằng `_van_tay`
    # (HMAC khoá phiên) nên KHÔNG bao giờ có giá trị nào rời khỏi tiến trình.
    khong_lien_quan = ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY",
                       "CLOUDSDK_AUTH_ACCESS_TOKEN")
    van_tay_ngoai = {_van_tay(con[t]) for t in khong_lien_quan if con.get(t)}
    giu_cho = []
    nguon_gh = "none"
    for ten in ("GH_TOKEN", "GITHUB_TOKEN", "GITHUB_PAT"):
        v = con.get(ten)
        if not v:
            continue
        if _van_tay(v) in van_tay_ngoai:
            giu_cho.append(ten)          # CHỈ tên, không bao giờ giá trị
            continue
        nguon_gh = ten if ten == "GH_TOKEN" else f"{ten}->GH_TOKEN"
        con["GH_TOKEN"] = v              # ghi đè cả khi GH_TOKEN cũ là giữ chỗ
        break
    if nguon_gh == "none":
        con.pop("GH_TOKEN", None)        # thà KHÔNG có còn hơn có bản giữ chỗ:
        con.pop("GITHUB_TOKEN", None)    # "chưa đăng nhập" đọc đúng, "sai thông
        # tin đăng nhập" đẩy người đọc đi sai hướng.
    con["TL_LAUNCHER_ENV_DA_DOC"] = "1"
    ten_bien = (
        "CODEX_HOME", "CODEX_AUTH_JSON", "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY", "GH_TOKEN", "GITHUB_TOKEN", "GITHUB_PAT",
        "CLAUDE_CODE_REMOTE", "CLAUDE_PROJECT_DIR", "TL_WORKSPACE",
    )
    cong_khai = {
        "da_doc_truoc_cong_cu": True,
        "path_co": bool(path),
        "so_muc_path": len([x for x in path.split(os.pathsep) if x]),
        # CHỈ bool — không bao giờ giá trị. Biến giữ chỗ và biến thật nhìn giống
        # nhau ở đây, đó là chủ ý: `moi-truong` mới là chỗ gom theo vân tay.
        "bien_co": {ten: bool(os.environ.get(ten)) for ten in ten_bien},
        "nguon_xac_thuc_github": nguon_gh,
        # Tên các biến bị loại vì trùng byte với credential không liên quan. Rỗng
        # là "không phát hiện", KHÔNG phải "đã kiểm và sạch" — phép đo này chỉ
        # thấy được chuỗi giữ chỗ nào DÙNG CHUNG với biến khác.
        "bien_giu_cho": giu_cho,
    }
    return con, cong_khai


def _cac_duong_dan(c: dict, moi_truong: dict[str, str]) -> list[tuple[str, str]]:
    """Mọi executable khớp trong PATH chụp sẵn, rồi các vị trí nền chuẩn.

    Trả CẶP `(ten_ung_vien, duong_dan)`, không trả riêng đường dẫn: `doctor` báo
    `goi_bang` = TÊN gọi được (`python` khi máy không có `python3`) và `duong_dan`
    = binary cụ thể. Hai trường trả lời hai câu khác nhau và `t55` ghim trường
    đầu, nên gộp chúng lại là lặng lẽ đổi hợp đồng của một lệnh đã có người gọi.

    `shutil.which('rg')` chỉ trả mục ĐẦU TIÊN. Trên Windows 15-08-2026 mục đó là
    rg của Codex Desktop trong WindowsApps và CreateProcess trả Access denied;
    dừng ở đó che mất bản tốt phía sau. Hàm này giữ thứ tự nhưng không dừng sớm.
    """
    ra: list[tuple[str, str]] = []

    def them(ten: str, duong) -> None:
        if not duong:
            return
        s = str(duong)
        khoa = os.path.normcase(os.path.abspath(s))
        if khoa not in {os.path.normcase(os.path.abspath(x)) for _, x in ra}:
            ra.append((ten, s))

    path = moi_truong.get("PATH", "")
    for ten in c["ung_vien"]:
        for muc in path.split(os.pathsep):
            if not muc:
                continue
            try:   # wp802: không `which` — trên Windows nó chèn cwd vào MỌI `muc` (Codex lượt 3 F6)
                them(ten, _ten_tran_giai_ra(ten, dict(moi_truong, PATH=muc), kieu_bash=False))
            except OSError:
                continue

    if platform.system() == "Windows":
        pf = moi_truong.get("ProgramFiles", r"C:\Program Files")
        local = moi_truong.get("LOCALAPPDATA", "")
        ten0 = c["ung_vien"][0]
        if c["ten"] == "bash":
            them(ten0, Path(pf) / "Git" / "bin" / "bash.exe")
            them(ten0, Path(pf) / "Git" / "usr" / "bin" / "bash.exe")
        elif c["ten"] == "rg" and local:
            them(ten0, Path(local) / "Microsoft" / "WinGet" / "Links" / "rg.exe")
        elif c["ten"] == "gh":
            them(ten0, Path(pf) / "GitHub CLI" / "gh.exe")
        elif c["ten"] == "agy" and local:
            them(ten0, Path(local) / "agy" / "bin" / "agy.exe")
    return [(t, x) for t, x in ra if Path(x).is_file()]


def _ten_tran_giai_ra(ten: str, moi_truong: dict[str, str], kieu_bash: bool = True) -> str | None:
    """Bản bash gọi khi gõ TÊN TRẦN: PATH theo thứ tự, mục RỖNG = cwd (wp802, Codex lượt 1 F1).
    `kieu_bash=False`: thứ tự PATHEXT của `which` (`x.CMD` hơn shim `x`), cho tiến trình native (F6)."""
    duoi = [""]
    if platform.system() == "Windows":   # PATHEXT rỗng ⇒ mặc định, như `which` CPython 3.13 (F6 lượt 4)
        ext = [e.rstrip(".") for e in (moi_truong.get("PATHEXT") or ".COM;.EXE;.BAT;.CMD;.VBS;.JS;.WS;.MSC")
               .split(";") if e]
        duoi = (duoi + ext if kieu_bash else   # native: tên trần CHỈ khi đã mang đuôi PATHEXT, rồi vẫn nối đuôi
                ([""] if any(ten.upper().endswith(e.upper()) for e in ext) else []) + ext)
    for muc in moi_truong.get("PATH", "").split(os.pathsep):
        for d in duoi:
            p = os.path.join(muc or ".", ten + d)
            if os.path.isfile(p) and os.access(p, os.X_OK):
                return os.path.abspath(p)
    return None


def _phien_ban(duong_dan: str, *, env=None,
               timeout=PROBE_TIMEOUT_GIAY) -> tuple[bool, str, bool]:
    """Chạy thử `--version`. Trả (chay_duoc, dong_dau, qua_han).

    `shutil.which()` KHÔNG phải bằng chứng công cụ dùng được — audit codex dựng hai
    tệp RỖNG tên git.exe/python.exe rồi doctor báo xanh; và ngay trên máy đó `rg.exe`
    có trong PATH nhưng chạy ra "Access is denied". Có mặt ≠ chạy được.

    `stdin=DEVNULL`: một công cụ chờ stdin sẽ TREO tới hết deadline thay vì trả
    lời. Cùng họ với bẫy `$Args` (r244) — tiến trình đọc stdin, EOF, rc=0, đầu ra
    rỗng: cổng xanh mà chẳng đo gì.

    `qua_han` là TÍN HIỆU KIỂU riêng, không phải chuỗi để phía gọi dò: TimeoutExpired
    nghĩa là "KHÔNG ĐO ĐƯỢC trong hạn" — khác hẳn "đo được là hỏng" (rc != 0, OSError,
    không in gì). Đây là NGUỒN CHỚP của `t53` (ops/NO_KY_THUAT.md, "doctor chớp"):
    một lượt `--version` hết hạn dưới churn tiến trình từng bị đếm là THIẾU công cụ
    rồi hai phút sau lại đủ — cùng lệnh, cùng máy. Phân loại bằng cách dò chữ
    "timeout" trong mô tả là ĐOÁN, không phải ĐO (bài học phân loại HTTP bằng văn
    bản tự do); nên cờ này phải là phần tử trả về riêng.
    """
    try:
        p = subprocess.run([duong_dan, "--version"], capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, env=env, timeout=max(0.1, timeout),
                           encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return (False, f"timeout sau {timeout:.1f}s", True)
    except (OSError, subprocess.SubprocessError) as e:
        return (False, str(e)[:120], False)
    ra = (p.stdout or "") + (p.stderr or "")   # nhiều CLI in phiên bản ra stderr
    dong = [d.strip() for d in ra.splitlines() if d.strip()]
    if p.returncode != 0 or not dong:
        return (False, dong[0][:80] if dong else f"rc={p.returncode}, khong in gi", False)
    return (True, dong[0][:80], False)


def _xac_thuc(duong_dan: str, doi_so: list[str], *, env=None,
              timeout=PROBE_TIMEOUT_GIAY) -> tuple[bool, str, bool]:
    """Bọc `_xac_thuc_kem_dau_ra`, bỏ phần tử đầu ra — hợp đồng ba phần tử cho caller
    ngoài. `doctor` KHÔNG gọi hàm này nữa mà gọi thẳng hàm dưới (nó cần đầu ra để
    ghi vào `_XAC_THUC_DA_DO`), nên test muốn giả probe auth của `doctor` phải giả
    `_xac_thuc_kem_dau_ra` (bộ bốn). Ai cần ĐẦU RA của chính probe ấy (đếm dòng,
    chẩn đoán) thì gọi hàm dưới, ĐỪNG chạy lại lệnh."""
    ok, mo_ta, qua_han, _ = _xac_thuc_kem_dau_ra(duong_dan, doi_so, env=env, timeout=timeout)
    return (ok, mo_ta, qua_han)


def _xac_thuc_kem_dau_ra(duong_dan: str, doi_so: list[str], *, env=None,
                         timeout=PROBE_TIMEOUT_GIAY) -> tuple[bool, str, bool, str]:
    """Probe auth không tương tác; không bao giờ trả stdout/stderr có credential.

    Phần tử thứ tư là stdout+stderr GỘP của chính lần chạy này — để caller dùng
    lại thay vì gọi lệnh lần hai. Cross-review PR "#426" (codex, P2 trên
    `15f2dbf`): `_do_antigravity` từng gọi `agy models` thêm một lần chỉ để đếm
    dòng; lần hai ấy đi mạng, quá hạn/OSError sẽ ném thẳng lên `lenh_doctor` và
    lật kết luận thành KHONG_DO_DUOC dù đã có bằng chứng dương trong tay.

    `rc=0` MỘT MÌNH không phải bằng chứng — đúng doctrine "đòi BẰNG CHỨNG DƯƠNG,
    đừng tin rc". Một CLI thiếu subcommand có thể thoát 0 và không in gì; đọc thế
    là "đã xác thực" thì cổng tự bịa ra một kết luận.

    GIỚI HẠN CÓ THẬT, khai thẳng: hàm này chỉ phân biệt được "chạy và có nói gì
    đó" với "không". Nó KHÔNG biết nội dung ấy đúng hay sai, nên một lệnh trả
    rc=0 kèm câu khẳng định SAI (vd `codex login status` — xem chú thích ở
    `CONG_CU`) vẫn qua. Vì thế chỉ gắn `xac_thuc` cho công cụ có đầu ra KIỂM
    CHỨNG ĐƯỢC, đừng gắn đại trà.

    Phần tử thứ ba `qua_han` cùng hợp đồng với `_phien_ban`: quá hạn là "KHÔNG ĐO
    ĐƯỢC trong hạn", không phải "đo được là sai" — probe auth cũng gọi CLI chậm
    (node) nên cũng là một đường chớp của `t53` y như probe `--version`.
    Thông điệp quá hạn cố ý KHÁC chữ với `_phien_ban` để mỗi mỏ neo đột biến
    khớp đúng một chỗ (chốt `moi mau dot bien phai khop DUNG MOT cho`).
    """
    try:
        p = subprocess.run([duong_dan, *doi_so], capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, env=env, timeout=max(0.1, timeout),
                           encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return (False, f"probe xac thuc timeout sau {timeout:.1f}s", True, "")
    except (OSError, subprocess.SubprocessError) as e:
        return (False, type(e).__name__, False, "")
    dau_ra = (p.stdout or "") + (p.stderr or "")
    co_loi_ra = bool(dau_ra.strip())
    if p.returncode != 0:
        return (False, f"rc={p.returncode}", False, dau_ra)
    if not co_loi_ra:
        return (False, "rc=0 nhung khong co bang chung xac thuc", False, dau_ra)
    return (True, "ok", False, dau_ra)


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


# ------------------------------------------------- BIẾN MÔI TRƯỜNG & KHẢ DỤNG
#
# VÌ SAO CÓ CẢ MẢNG NÀY — sự cố 15-08-2026, mất gần trọn một ngày làm việc.
#
# Phiên điều phối chạy `codex login status`, nhận `Not logged in`, rồi KẾT LUẬN
# "container không gọi được codex" và báo với chủ kho rằng cross-review phải chờ
# một máy khác. Sai. `codex` xác thực qua biến môi trường `CODEX_AUTH_JSON`
# (base64 của chính `auth.json`); giải mã ra `~/.codex/auth.json` là chạy được
# NGAY, và lượt cross-review thứ 11 đã chạy trọn trong chính container đó.
#
# BA lỗi chồng lên nhau, mỗi lỗi một bài học, và cả ba đều đã có tiền lệ trong kho:
#
#   1. Dừng ở MỘT lệnh. `codex login status` nói đúng sự thật của nó — không có
#      `auth.json` trên đĩa — nhưng câu hỏi đúng là "nó xác thực bằng ĐƯỜNG NÀO",
#      không phải "nó đã đăng nhập chưa". `.claude/skills/work-packet/SKILL.md`
#      viết sẵn: "Vắng mặt là một QUAN SÁT; 'môi trường không có' là một KẾT LUẬN."
#
#   2. Tìm biến bằng DANH SÁCH TÊN ĐOÁN TRƯỚC (`OPENAI_API_KEY`, `CODEX_API_KEY`…)
#      nên trượt đúng cái tên thật. Y hệt lỗi bộ quét secrets lọc theo PHẦN MỞ RỘNG
#      rồi mù với `.env` (CLAUDE.md đã ghi). Lọc theo danh sách đoán trước thì mù
#      đúng chỗ thứ cần tìm đang nằm. Ở đây: quét TOÀN BỘ `os.environ` theo MẪU.
#
#   3. Đưa base64 THÔ vào `auth.json`, nhận `expected value at line 1 column 1`,
#      rồi đọc thành "biến này không dùng được" thay vì "mình đưa sai định dạng".
#      `chuan_bi_xac_thuc()` thử CẢ HAI định dạng và khi hỏng thì nói rõ hỏng ở đâu.
#
# LUẬT ĐỌC BIẾN TRƯỚC KHI DÙNG CÔNG CỤ: mọi kết luận "công cụ X không dùng được"
# phải đi sau một lượt quét biến môi trường. `doctor` cưỡng chế bằng cách LUÔN in
# phần biến, kể cả khi mọi công cụ đều xanh.
#
# TUYỆT ĐỐI KHÔNG IN GIÁ TRỊ. Chỉ tên · độ dài · vân tay 8 ký tự. Vân tay có mục
# đích riêng, xem `_nhom_van_tay`.

_RE_BIEN_NHAY_CAM = re.compile(
    r"TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|COOKIE|AUTH|APIKEY|API_KEY"
    r"|ACCESS_KEY|_KEY$|^KEY_|PAT$|_PAT|SESSION",
    re.IGNORECASE,
)

# Biến LIÊN QUAN tới ba khả năng dưới, kể cả khi tên không khớp mẫu bí mật.
_RE_BIEN_LIEN_QUAN = re.compile(
    r"CODEX|CLAUDE|ANTHROPIC|OPENAI|^GH_|GITHUB|GIT_CONFIG", re.IGNORECASE)


# Dưới ngưỡng này, hai biến trùng giá trị không nói lên điều gì — `"1"`, `"true"`,
# `"0"` trùng nhau khắp nơi. Không có credential thật nào ngắn tới mức này.
NGUONG_DO_DAI_BI_MAT = 8


# Khoá NGẪU NHIÊN mỗi tiến trình, KHÔNG BAO GIỜ xuất ra. Xem `_van_tay`.
_KHOA_PHIEN = secrets.token_bytes(32)


def _van_tay(v: str) -> str:
    """Nhãn so sánh NỘI BỘ. TUYỆT ĐỐI KHÔNG ĐƯỢC XUẤT RA NGOÀI.

    Bản trước trả 8 hex đầu của **sha256 trần** VÀ xuất nó ra `moi-truong` /
    `doctor --json` cho mọi biến khớp mẫu, kèm ĐỘ DÀI CHÍNH XÁC. Cross-review
    `deterministic-secret-fingerprint-is-dictionary-oracle` (mức HIGH) chỉ ra đó là
    **oracle từ điển**: với biến có tập ứng viên nhỏ — cờ, token cấu hình, mật khẩu
    yếu — người đọc transcript chỉ cần băm ngoại tuyến từng ứng viên rồi so 32 bit là
    ra giá trị. Digest ổn định còn cho phép NỐI một biến qua nhiều transcript.

    Đau nhất là chỗ này: ngưỡng `NGUONG_DO_DAI_BI_MAT` tôi thêm CHỈ nằm trong
    `_nhom_van_tay`, tức phép GOM — trong khi `van_tay` được XUẤT ở
    `quet_bien_moi_truong`, một chỗ khác hẳn. Đặt chốt đúng chỗ mình đang nghĩ tới,
    rồi xuất dữ liệu ở chỗ mình quên. Và mỉa mai đúng chỗ đáng nhớ: bản vá này sinh
    ra để chống kết luận sai VỀ biến môi trường, rồi tự mở một đường suy ngược GIÁ TRỊ
    biến môi trường.

    Nay dùng HMAC với khoá ngẫu nhiên sống trong đúng một tiến trình. Hệ quả: so sánh
    trong CÙNG một lượt vẫn đúng (thứ duy nhất phép gom cần), còn băm ngoại tuyến và
    nối chéo transcript đều chết vì kẻ đọc không có khoá. Đầu ra người dùng thấy là
    nhãn thứ tự (`nhom-1`), không phải digest.
    """
    return hmac.new(_KHOA_PHIEN, v.encode("utf-8", "replace"),
                    hashlib.sha256).hexdigest()[:8]


def _nhom_van_tay(ten_bien: list[str]) -> dict:
    """Nhóm các biến theo vân tay giá trị. Trả {van_tay: [tên, …]}.

    ĐÂY LÀ PHÉP KIỂM ĐÁNG GIÁ NHẤT TRONG TỆP NÀY, và nó ra đời từ một phép đo.

    Container 15-08-2026 có `GH_TOKEN`, `GITHUB_TOKEN`, `AWS_ACCESS_KEY_ID`,
    `AWS_SECRET_ACCESS_KEY`, `CLOUDSDK_AUTH_ACCESS_TOKEN` — NĂM biến, CÙNG một
    giá trị 14 ký tự, cùng vân tay `f07d7417`. Một chuỗi giữ chỗ. Còn credential
    THẬT của GitHub nằm ở `GITHUB_PAT` (93 ký tự, tiền tố `github_pat_`).

    Hệ quả nếu không có phép kiểm này: `gh auth status` đọc `GH_TOKEN` giữ chỗ rồi
    hỏng, và người đọc kết luận "GitHub không dùng được" — trong khi đường thật vẫn
    mở. ĐÃ ĐẶT ≠ DÙNG ĐƯỢC, và một biến giữ chỗ còn tệ hơn biến chưa đặt: biến chưa
    đặt thì công cụ nói "chưa đăng nhập", biến giữ chỗ thì công cụ nói "sai thông tin
    đăng nhập" — thông điệp đẩy người đọc đi sai hướng.

    Ba biến trở lên trùng vân tay thì gần như chắc chắn là giữ chỗ: hai dịch vụ khác
    nhau không tình cờ cấp cùng một chuỗi.

    HAI ĐIỀU KIỆN LỌC, và chúng có được là nhờ ĐO chứ không nhờ nghĩ ra. Bản đầu chỉ
    nhóm theo vân tay và lập tức báo oan hai nhóm lớn: tám biến cùng vân tay
    `6b86b273` (là sha256 của `"1"`) và chín biến `b5bea41b` (sha256 của `"true"`).
    Đó là CỜ BẬT/TẮT, không phải credential. Giá trị ngắn thì đụng nhau là chuyện
    thường, nên:

      · giá trị phải dài `>= NGUONG_DO_DAI_BI_MAT` — dưới ngưỡng đó, trùng nhau
        không nói lên điều gì;
      · tên phải khớp mẫu bí mật — phép kiểm này chỉ trả lời đúng MỘT câu hỏi
        ("biến credential này có phải chuỗi giữ chỗ không"), nên đừng để nó phán
        về những biến không phải credential.
    """
    nhom: dict = {}
    for t in ten_bien:
        v = os.environ.get(t)
        if v and len(v) >= NGUONG_DO_DAI_BI_MAT and _RE_BIEN_NHAY_CAM.search(t):
            nhom.setdefault(_van_tay(v), []).append(t)
    return nhom


def quet_bien_moi_truong() -> dict:
    """Quét TOÀN BỘ `os.environ` theo MẪU. Không bao giờ trả về giá trị."""
    ten = sorted(k for k in os.environ
                 if _RE_BIEN_NHAY_CAM.search(k) or _RE_BIEN_LIEN_QUAN.search(k))
    nhom = _nhom_van_tay(ten)
    giu_cho = {t for ds in nhom.values() if len(ds) >= 3 for t in ds}
    # Nhãn nhóm THỨ TỰ, không phải digest. Chỉ những nhóm >= 3 mới được đặt tên, vì
    # đó là thứ duy nhất phép kiểm này cần nói ra ("mấy biến này CÙNG một giá trị").
    trung = sorted((k for k, v in nhom.items() if len(v) >= 3), key=lambda k: sorted(nhom[k]))
    nhan = {k: f"nhom-{i}" for i, k in enumerate(trung, 1)}
    thuoc_nhom = {t: nhan[k] for k, ds in nhom.items() if k in nhan for t in ds}

    def _do_dai(v: str) -> str:
        # Độ dài CHÍNH XÁC của một giá trị NGẮN thu hẹp không gian tìm kiếm thêm một
        # bậc nữa, cộng với nhãn nhóm là đủ để đoán. Giá trị dài thì độ dài chính xác
        # vô hại và có ích khi chẩn đoán, nên chỉ gộp ở đầu ngắn.
        n = len(v)
        return str(n) if n >= NGUONG_DO_DAI_BI_MAT else f"<{NGUONG_DO_DAI_BI_MAT}"

    return {
        "so_bien": len(ten),
        "bien": [{"ten": t, "do_dai": _do_dai(os.environ.get(t, "")),
                  "nhom": thuoc_nhom.get(t, ""),
                  "nghi_giu_cho": t in giu_cho}
                 for t in ten],
        # Khoá là NHÃN, không phải băm — không có gì băm ngoại tuyến được nữa.
        "nhom_trung_gia_tri": {nhan[k]: sorted(v) for k, v in nhom.items() if k in nhan},
    }


def _chuan_bi_va_bo_snapshot() -> None:
    """Materialize in this process, then remove the snapshot before any child."""
    if not os.environ.get("CODEX_AUTH_JSON"):
        os.environ.pop("CODEX_AUTH_JSON", None)
        return
    try:
        ket = chuan_bi_xac_thuc(that_su=True)
        if not ket or not all(x.get("ok") for x in ket):
            raise Chan(MA_CHUA_XAC_THUC, "Không chuẩn bị được Codex credential; chưa chạy child")
    finally:
        os.environ.pop("CODEX_AUTH_JSON", None)


def _codex_home_hieu_luc() -> Path:
    """Resolve only; standalone doctor must not depend on another dev module."""
    raw = os.environ.get("CODEX_HOME", "")
    home = Path(raw).expanduser() if raw else Path.home() / ".codex"
    if not home.is_absolute() or ".." in home.parts:
        raise OSError("CODEX_HOME must be an absolute path without parent traversal")
    return home


def _cho_snapshot_hoac_chan() -> bool:
    """wp484 g7 (P2 #509 thread XML) — `CODEX_HOME` sai từng rơi ra traceback rc=1 ở
    `credential-status` và `run … codex`, nên người gọi không phân biệt được "cấu hình
    credential hỏng" với "launcher sập". Nay là một `Chan` có mã: KHÔNG ĐO ĐƯỢC ≠ sập."""
    try:
        home = _codex_home_hieu_luc()
    except OSError as e:
        raise Chan(MA_CHUA_XAC_THUC, f"CODEX_HOME không hợp lệ: {e}") from None
    return _dang_cho_snapshot(home)


class _KhoCodex:
    """Pinned directory storage. No symlink traversal, broad ACL, or repo writes.

    POSIX uses directory-relative descriptors. Windows pins every ancestor without
    FILE_SHARE_DELETE, opens reparse points themselves, and checks DACLs on handles.
    Native calls are local only; no shell, chmod-as-ACL, or credential subprocess.
    """
    MAX_BYTES = 8 * 1024 * 1024

    def __init__(self, home: Path, create=False, artifact=False):
        self.home = home
        self.stack = contextlib.ExitStack()
        self.fd = None
        self.windows = os.name == "nt"
        try:
            if not home.is_absolute() or ".." in home.parts or home == Path(home.anchor):
                raise OSError("invalid Codex home")
            if self.windows:
                if home.anchor.startswith("\\\\") or any(
                        p.rstrip(" .") != p or ":" in p for p in home.parts[1:]):
                    raise OSError("unsupported Windows Codex home")
                self._win_init()
                current = Path(home.anchor)
                for part in (None, *home.parts[1:]):
                    if part is not None:
                        current /= part
                        if create and not current.exists():
                            with self._win_security(directory=True) as sa:
                                if not self.k.CreateDirectoryW(str(current), self.c.byref(sa)):
                                    raise OSError("cannot create private Codex directory")
                    h = self._win_open(current, directory=True, security=current == home)
                    self.stack.callback(self.k.CloseHandle, h)
                    if (current / ".git").exists() or (current / ".git").is_symlink():
                        raise OSError("Codex home is inside a repository")
                self._win_private(h)
            else:
                if not hasattr(os, "O_NOFOLLOW") or os.open not in os.supports_dir_fd:
                    raise OSError("secure directory-relative storage unavailable")
                current = os.open(home.anchor, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
                self.stack.callback(os.close, current)
                for part in (None, *home.parts[1:]):
                    if part is not None:
                        if create:
                            try:
                                os.mkdir(part, mode=0o700, dir_fd=current)
                            except FileExistsError:
                                pass
                        current = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                          dir_fd=current)
                        self.stack.callback(os.close, current)
                    try:
                        os.stat(".git", dir_fd=current, follow_symlinks=False)
                    except FileNotFoundError:
                        pass
                    else:
                        raise OSError("Codex home is inside a repository")
                info = os.fstat(current)
                private = info.st_uid == os.getuid() and not info.st_mode & 0o022
                sticky_export = (artifact and info.st_uid in (0, os.getuid())
                                 and bool(info.st_mode & stat.S_ISVTX))
                if not private and not sticky_export:
                    raise OSError("Codex directory has unsafe ownership or permissions")
                self.fd = current
        except BaseException:
            self.stack.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.stack.close()

    def _name(self, name):
        if not name or Path(name).name != name or name in (".", "..") or ":" in name:
            raise OSError("invalid credential filename")

    def read(self, name="auth.json"):
        self._name(name)
        try:
            if self.windows:
                import msvcrt
                h = self._win_open(self.home / name)
                try:
                    self._win_private(h)
                    fd = msvcrt.open_osfhandle(h, os.O_RDONLY | os.O_BINARY)
                except BaseException:
                    self.k.CloseHandle(h)
                    raise
            else:
                fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=self.fd)
                info = os.fstat(fd)
                if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
                        or info.st_uid != os.getuid() or info.st_mode & 0o077):
                    os.close(fd)
                    raise OSError("credential file has unsafe ownership or permissions")
        except FileNotFoundError:
            return None
        with os.fdopen(fd, "rb") as f:
            data = f.read(self.MAX_BYTES + 1)
        if len(data) > self.MAX_BYTES:
            raise OSError("credential file exceeds size limit")
        return data

    def write(self, name, data, expected):
        self._name(name)
        if len(data) > self.MAX_BYTES:
            raise OSError("credential exceeds size limit")
        if self.read(name) != expected:
            raise OSError("credential changed during preparation")
        temp = "." + name + ".tmp-" + secrets.token_hex(16)
        try:
            if self.windows:
                import msvcrt
                with self._win_security() as sa:
                    h = self._win_open(self.home / temp, create=True, sa=sa)
                try:
                    self._win_private(h)
                    fd = msvcrt.open_osfhandle(h, os.O_WRONLY | os.O_BINARY)
                except BaseException:
                    self.k.CloseHandle(h)
                    raise
            else:
                fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             0o600, dir_fd=self.fd)
            with os.fdopen(fd, "wb") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            if self.read(name) != expected:
                raise OSError("credential changed before promotion")
            if self.windows:
                os.replace(self.home / temp, self.home / name)
            else:
                os.replace(temp, name, src_dir_fd=self.fd, dst_dir_fd=self.fd)
                os.fsync(self.fd)
        finally:
            try:
                if self.windows:
                    (self.home / temp).unlink()
                else:
                    os.unlink(temp, dir_fd=self.fd)
            except FileNotFoundError:
                pass

    def _win_init(self):
        import ctypes as c
        from ctypes import wintypes as w
        self.c, self.w = c, w
        self.k = c.WinDLL("kernel32", use_last_error=True)
        self.a = c.WinDLL("advapi32", use_last_error=True)
        V, D, H, B, S = c.c_void_p, w.DWORD, w.HANDLE, w.BOOL, w.LPCWSTR
        for dll, name, args, result in (
            (self.k, "CreateFileW", [S,D,D,V,D,D,H], H),
            (self.k, "CreateDirectoryW", [S,V], B),
            (self.k, "CloseHandle", [H], B),
            (self.k, "GetCurrentProcess", [], H),
            (self.k, "GetFileInformationByHandle", [H,V], B),
            (self.k, "GetFileType", [H], D),
            (self.k, "LocalFree", [V], V),
            (self.a, "OpenProcessToken", [H,D,c.POINTER(H)], B),
            (self.a, "GetTokenInformation", [H,c.c_int,V,D,c.POINTER(D)], B),
            (self.a, "ConvertSidToStringSidW", [V,c.POINTER(w.LPWSTR)], B),
            (self.a, "ConvertStringSidToSidW", [S,c.POINTER(V)], B),
            (self.a, "GetSecurityInfo", [H,c.c_int,D,V,V,V,V,c.POINTER(V)], D),
            (self.a, "ConvertSecurityDescriptorToStringSecurityDescriptorW",
             [V,D,D,c.POINTER(w.LPWSTR),V], B),
            (self.a, "ConvertStringSecurityDescriptorToSecurityDescriptorW",
             [S,D,c.POINTER(V),V], B),
        ):
            fn = getattr(dll, name)
            fn.argtypes, fn.restype = args, result
        token = H()
        if not self.a.OpenProcessToken(self.k.GetCurrentProcess(), 8, c.byref(token)):
            raise OSError("cannot determine credential owner")
        try:
            length = D()
            self.a.GetTokenInformation(token, 1, None, 0, c.byref(length))
            buf = c.create_string_buffer(length.value)
            if not self.a.GetTokenInformation(token, 1, buf, length, c.byref(length)):
                raise OSError("cannot determine credential owner")
            sid = c.cast(buf, c.POINTER(V))[0]
            text = w.LPWSTR()
            if not self.a.ConvertSidToStringSidW(sid, c.byref(text)):
                raise OSError("cannot determine credential owner")
            try:
                self.sid = text.value
            finally:
                self.k.LocalFree(c.cast(text, V))
        finally:
            self.k.CloseHandle(token)

    def _win_open(self, path, directory=False, create=False, sa=None, security=True):
        c, w = self.c, self.w
        # FILE_LIST_DIRECTORY (bit 1) participates in share-access accounting;
        # an attributes-only handle does NOT prevent rename despite share=3.
        access = (0x81 | (0x20000 if security else 0)) if directory else (0x40020000 if create else 0x80020000)
        h = self.k.CreateFileW(str(path), access, 3 if directory else 1,
                               c.byref(sa) if sa is not None else None,
                               1 if create else 3, 0x02000000 | 0x00200000, None)
        if h == c.c_void_p(-1).value:
            error = c.get_last_error()
            if error in (2, 3) and not create:
                raise FileNotFoundError("credential path does not exist")
            raise OSError(error, "cannot open credential path securely")
        class Info(c.Structure):
            _fields_ = [("attrs", w.DWORD), ("times", w.FILETIME * 3),
                        ("volume", w.DWORD), ("size_hi", w.DWORD),
                        ("size_lo", w.DWORD), ("links", w.DWORD),
                        ("index_hi", w.DWORD), ("index_lo", w.DWORD)]
        info = Info()
        if (not self.k.GetFileInformationByHandle(h, c.byref(info))
                or info.attrs & 0x400 or bool(info.attrs & 0x10) != directory
                or self.k.GetFileType(h) != 1 or (not directory and info.links != 1)):
            self.k.CloseHandle(h)
            raise OSError("credential path is a reparse point or non-regular object")
        return h

    def _win_sid(self, value):
        # SDDL may abbreviate a token SID (e.g. local RID 500 -> LA).
        # Compare identity, never accept an alias for every caller.
        c, w = self.c, self.w
        sid, text = c.c_void_p(), w.LPWSTR()
        if not self.a.ConvertStringSidToSidW(value, c.byref(sid)):
            raise OSError("cannot resolve credential ACL principal")
        try:
            if not self.a.ConvertSidToStringSidW(sid, c.byref(text)):
                raise OSError("cannot normalize credential ACL principal")
            return text.value
        finally:
            if text:
                self.k.LocalFree(c.cast(text, c.c_void_p))
            self.k.LocalFree(sid)

    def _win_private(self, handle):
        c, w = self.c, self.w
        sd, text = c.c_void_p(), w.LPWSTR()
        if self.a.GetSecurityInfo(handle, 1, 5, None, None, None, None, c.byref(sd)):
            raise OSError("cannot verify credential ACL")
        try:
            if not self.a.ConvertSecurityDescriptorToStringSecurityDescriptorW(
                    sd, 1, 5, c.byref(text), None):
                raise OSError("cannot inspect credential ACL")
            value = text.value
        finally:
            if text:
                self.k.LocalFree(c.cast(text, c.c_void_p))
            self.k.LocalFree(sd)
        owner = re.search(r"O:(.*?)(?=[GDS]:|$)", value)
        acl = re.search(r"D:(.*?)(?=S:|$)", value)
        allowed = {self.sid, "S-1-5-18", "S-1-5-32-544"}
        if (not owner or not acl or "NO_ACCESS_CONTROL" in acl[1]
                or self._win_sid(owner[1]) not in allowed):
            raise OSError("credential owner or DACL is unsafe")
        for ace in re.findall(r"\(([^()]*)\)", acl[1]):
            fields = ace.split(";")
            if len(fields) != 6:
                raise OSError("unsupported credential ACL")
            if "IO" in fields[1] or fields[0] == "D":
                continue
            # Python's private Windows directories use OWNER RIGHTS (OW).
            # It is safe here only because the actual owner was checked above.
            if fields[0] != "A" or self._win_sid(fields[5]) not in allowed | {"S-1-3-4"}:
                raise OSError("credential ACL grants access to another principal")

    @contextlib.contextmanager
    def _win_security(self, directory=False):
        c, w = self.c, self.w
        class SA(c.Structure):
            _fields_ = [("length", w.DWORD), ("descriptor", c.c_void_p),
                        ("inherit", w.BOOL)]
        flags = "OICI" if directory else ""
        sddl = "D:P" + "".join(f"(A;{flags};FA;;;{sid})" for sid in (self.sid, "SY", "BA"))
        sd = c.c_void_p()
        if not self.a.ConvertStringSecurityDescriptorToSecurityDescriptorW(sddl, 1, c.byref(sd), None):
            raise OSError("cannot create private credential ACL")
        try:
            yield SA(c.sizeof(SA), sd, False)
        finally:
            self.k.LocalFree(sd)


def _doc_auth_bytes(data: bytes) -> dict:
    if len(data) > _KhoCodex.MAX_BYTES:
        raise ValueError("snapshot too large")
    parsed = json.loads(data.decode("utf-8"))
    if not isinstance(parsed, dict) or not isinstance(parsed.get("tokens"), dict):
        raise ValueError("tokens must be an object")
    if any(v is not None and not isinstance(v, str) for v in parsed["tokens"].values()):
        raise ValueError("token fields must be strings")
    return parsed


def _credential_id(data: bytes) -> str:
    # Formatting, last_refresh and extra metadata cannot revive a rejected token.
    tokens = _doc_auth_bytes(data)["tokens"]
    # A changed access/id token or account metadata cannot rehabilitate the same
    # rejected refresh token. That is the credential used to renew this snapshot.
    key = "refresh_token" if tokens.get("refresh_token") else "access_token"
    payload = {key: tokens.get(key)}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _doc_rejected(store):
    raw = store.read("credential-recovery.json")
    if raw is None:
        return [], None
    state = json.loads(raw.decode("utf-8"))
    rejected = state.get("rejected") if (isinstance(state, dict)
                and type(state.get("version")) is int and state["version"] == 1) else None
    if (not isinstance(rejected, list) or len(rejected) > 4096
            or any(not isinstance(x, str) or not re.fullmatch(r"[0-9a-f]{64}", x) for x in rejected)):
        raise ValueError("invalid credential recovery state")
    return rejected, raw


def _ghi_rejected(store, identity):
    rejected, raw = _doc_rejected(store)
    if identity in rejected:
        return
    if len(rejected) >= 4096:
        raise OSError("credential recovery history is full")
    rejected.append(identity)
    data = json.dumps({"version": 1, "rejected": rejected}, sort_keys=True).encode("utf-8")
    store.write("credential-recovery.json", data, raw)


def _danh_dau_auth_hong(home: Path, da_probe: bytes | None = None) -> bool:
    """Ghi danh tính credential ĐÃ BỊ TỪ CHỐI vào state.

    wp484 g7 (cross-review Codex lượt 1 F03) — bản trước ĐỌC LẠI `auth.json` sau probe rồi ghi
    danh tính của bản ĐANG có. Tiến trình khác refresh giữa chừng (A bị từ chối, B vừa ghi)
    thì B — chưa từng bị thử — bị chặn, còn A không vào lịch sử. Người gọi có bytes đã probe
    thì truyền vào `da_probe`; `_dang_cho_snapshot` so với bản đang có nên B vẫn đi tiếp."""
    try:
        with _KhoCodex(home) as store:
            data = da_probe if da_probe is not None else store.read()
            if data is None:
                return False
            _ghi_rejected(store, _credential_id(data))
        return True
    except (OSError, ValueError, UnicodeError):
        return False


def _dang_cho_snapshot(home: Path) -> bool:
    try:
        with _KhoCodex(home) as store:
            rejected, _ = _doc_rejected(store)
            data = store.read()
            return data is not None and _credential_id(data) in rejected
    except FileNotFoundError:
        return False
    except (OSError, ValueError, UnicodeError):
        return True  # unreadable recovery state is not permission to retry


def _probe_snapshot(data: bytes):
    """Use the existing credential probe; promote its refreshed bytes, not the input."""
    import runpy
    helper = Path(__file__).with_name("codex_cred.py")
    if not helper.is_file():
        return None, False
    with tempfile.TemporaryDirectory(prefix="tral-cred-candidate-") as temp:
        home = Path(temp) / "codex"
        with _KhoCodex(home, create=True) as candidate:
            candidate.write("auth.json", data, None)
            ok, reason = runpy.run_path(str(helper))["_kiem_song"](home)
            if not ok:
                return None, reason.startswith("credential BỊ TỪ CHỐI (")
            refreshed = candidate.read()
            if refreshed is None:
                return None, False
            _doc_auth_bytes(refreshed)
            return refreshed, False


def chuan_bi_xac_thuc(that_su: bool = True, snapshot=None) -> list[dict]:
    """Prepare disk credentials, without claiming health from readability/freshness.

    Existing credentials are replaced only after an isolated live probe. Initial
    materialization is structural preparation, not a live-auth success claim.
    All path/storage errors are controlled; errors never contain snapshot bytes.
    """
    raw = os.environ.get("CODEX_AUTH_JSON", "") if snapshot is None else snapshot
    raw = raw.strip()
    if not raw:
        return []
    result = {"ten": "codex", "ok": False, "doi": False}
    try:
        home = _codex_home_hieu_luc()
        result["duong_dan"] = str(home / "auth.json")
        data, parsed = None, None
        if len(raw) <= 2 * _KhoCodex.MAX_BYTES:
            for method in ("base64", "JSON thô"):
                try:
                    value = base64.b64decode(raw, validate=True) if method == "base64" else raw.encode("utf-8")
                    parsed = _doc_auth_bytes(value)
                    data = value
                    break
                except (ValueError, UnicodeError):
                    pass
        if data is None:
            result["cach"] = "HỎNG: đã thử base64 và JSON thô; cần JSON object có tokens object"
            return [result]
        with contextlib.ExitStack() as stack:
            try:
                store = stack.enter_context(_KhoCodex(home))
            except FileNotFoundError:
                if not that_su:
                    result.update(ok=True, doi=True, cach="JSON hợp lệ; thử khan, chưa kiểm quyền đích chưa tồn tại")
                    return [result]
                store = stack.enter_context(_KhoCodex(home, create=True))
            rejected, _ = _doc_rejected(store)
            identity = _credential_id(data)
            if identity in rejected or len(rejected) >= 4096:
                result["cach"] = "CHỜ snapshot mới: credential này đã thất bại hoặc history đã đầy"
                return [result]
            old = store.read()
            old_parsed = _doc_auth_bytes(old) if old is not None else None
            if old == data:
                result.update(ok=True, cach="đã khớp, không đụng; chưa phải bằng chứng sống")
                return [result]
            before = _moc_refresh(old_parsed.get("last_refresh")) if old_parsed else None
            after = _moc_refresh(parsed.get("last_refresh"))
            if before is not None and after is not None and before >= after:
                if _credential_id(old) in rejected:
                    result["cach"] = "CHỜ snapshot mới hơn; không lặp credential đã thất bại"
                    return [result]
                result.update(ok=True, cach="trên đĩa mới hơn hoặc bằng; giữ nguyên, không hạ cấp")
                return [result]
            if not that_su:
                result.update(ok=True, doi=True, cach="thử khan; chưa probe, chưa ghi")
                return [result]
            if old is not None:
                candidate, rejected_auth = _probe_snapshot(data)
                if candidate is None:
                    if rejected_auth:
                        # wp484 g7 (Codex lượt 1 F01, lối thứ ba) — lỗi ghi state từng rơi xuống câu
                        # "HỎNG" chung. Không nhớ hộ được qua tiến trình (nợ chủ kho chấp nhận:
                        # `codex-rejected-state-khong-ghi-duoc`), nhưng phải nói ĐÚNG lý do.
                        try:
                            _ghi_rejected(store, identity)
                        except (OSError, ValueError) as e:
                            result["cach"] = ("CHỜ snapshot mới: auth bị từ chối nhưng KHÔNG ghi được "
                                              f"trạng thái chờ ({type(e).__name__}) — CHẶN; giữ credential cũ")
                            return [result]
                    result["cach"] = ("CHỜ snapshot mới: auth bị từ chối; giữ nguyên credential cũ" if rejected_auth
                                       else "CHƯA ĐO ĐƯỢC probe; giữ nguyên credential cũ, chưa kết luận auth hỏng")
                    return [result]
                refreshed = _doc_auth_bytes(candidate)
                refreshed_time = _moc_refresh(refreshed.get("last_refresh"))
                if before is not None and (refreshed_time is None or refreshed_time < before):
                    result["cach"] = "từ chối snapshot sau probe vì không chứng minh được không hạ cấp"
                    return [result]
                data = candidate
            store.write("auth.json", data, old)
            result.update(ok=True, doi=True, cach="đã chuẩn bị credential an toàn" if old is None else "probe đạt; đã promote")
            return [result]
    except (OSError, ValueError, UnicodeError):
        result["cach"] = "HỎNG: không đọc/ghi an toàn được credential hoặc state; không chạy child"
        return [result]


# Cảnh báo TRƯỚC khi hỏng, không phải sau. Sự cố 15-08-2026: credential bị thu hồi giữa
# chừng, một lượt cross-review đã cấp lease bị mất trắng, và `doctor` chỉ phát hiện SAU
# khi mọi thứ đã 401. Bản vá hôm đó thêm phép kiểm hạn offline — nhưng nó chỉ đỏ khi ĐÃ
# hết hạn, tức vẫn báo muộn.
#
# 24 giờ là con số CHỌN, không phải đo: đủ để người dùng thấy cảnh báo ở phiên kế tiếp và
# kịp chạy `codex login` trước khi nó chặn việc. Ai thấy quá dài/ngắn thì đổi ở ĐÂY, một
# chỗ, và nói rõ vì sao.
NGUONG_CANH_BAO_GIO = 24.0

# `last_refresh` là dấu ẤN THỜI ĐIỂM CHỤP của chuỗi trong biến môi trường. Refresh token
# XOAY VÒNG: mỗi lần codex làm mới, bản trên đĩa đổi và bản cũ bị vô hiệu. Nên một ảnh
# chụp CŨ là dấu hiệu sắp hỏng KỂ CẢ khi `exp` còn xa — đo được 15-08: `access_token` còn
# 199 giờ mà credential đã bị thu hồi, trong khi `last_refresh` đã quá 40 giờ. Đây là tín
# hiệu DUY NHẤT nhìn thấy trước, nên đừng bỏ.
NGUONG_ANH_CHUP_CU_GIO = 24.0


def _moc_refresh(last_refresh):
    """`last_refresh` thành `datetime` CHÍNH XÁC — để MÁY so, không làm tròn.

    Tách khỏi `_tuoi_anh_chup_gio` (làm tròn 0,1h = 6 phút) vì làm tròn rồi so là cách
    hai mốc cách nhau vài phút thành "bằng nhau" (cross-review PR #128).
    """
    if not isinstance(last_refresh, str) or not last_refresh.strip():
        return None
    try:
        moc = datetime.fromisoformat(last_refresh.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return moc.replace(tzinfo=timezone.utc) if moc.tzinfo is None else moc


def _tuoi_anh_chup_gio(last_refresh) -> float | None:
    """Số giờ kể từ `last_refresh`. None = không đọc được, KHÁC với 0."""
    if not isinstance(last_refresh, str) or not last_refresh.strip():
        return None
    t = last_refresh.strip().replace("Z", "+00:00")
    try:
        moc = datetime.fromisoformat(t)
    except ValueError:
        return None
    if moc.tzinfo is None:
        moc = moc.replace(tzinfo=timezone.utc)
    return round((datetime.now(timezone.utc) - moc).total_seconds() / 3600, 1)


# Token NGẮN HẠN THEO THIẾT KẾ — hạn của chúng KHÔNG phải tín hiệu credential sắp chết.
# `id_token` đo được 1.0h ngay sau `codex login --device-auth`, trong khi `access_token`
# còn 240h. Lọc ở HAI nơi: lúc THU THẬP (`_han_token_codex`) và lúc QUYẾT ĐỊNH — vì test
# bơm thẳng vào `gio_con_lai` đã chứng minh lớp quyết định tự nó vẫn tin nếu lọt vào.
_TOKEN_KHONG_XET_HAN = frozenset({"id_token"})

# Tên cờ CHẶN codex — PHẢI khớp `TEN_CO_CHAN` trong `.claude/dev/codex_env_policy.py`.
# Hai tệp, một tên: đổi một bên mà quên bên kia thì chốt an ninh im lặng biến mất, nên
# `t102` khoá bằng cách ĐỌC hằng của tệp kia chứ không chép lại chuỗi.
CO_CHAN_CODEX = "tra-luat-CHAN-CODEX"


def _last_refresh_cua(noi_dung: str):
    """Đọc `last_refresh` từ nội dung auth.json. None nếu không đọc được."""
    try:
        return json.loads(noi_dung).get("last_refresh")
    except Exception:
        return None


def _han_token_codex() -> dict:
    """Đọc HẠN của token trong `~/.codex/auth.json`. KHÔNG in giá trị token.

    Chỉ trả về mốc thời gian và số giờ còn lại — `exp` là một con số, không phải bí mật.
    Không xác thực chữ ký: ta không kiểm token có THẬT, ta chỉ kiểm nó đã HẾT HẠN chưa.
    """
    ra = {"doc_duoc": False, "last_refresh": None, "tuoi_anh_chup_gio": None,
          "gio_con_lai": {}}
    try:
        with _KhoCodex(_codex_home_hieu_luc()) as store:
            data = store.read()
            if data is None:
                return ra
            d = _doc_auth_bytes(data)
    except Exception:
        return ra
    ra["doc_duoc"] = True
    ra["last_refresh"] = d.get("last_refresh") if _moc_refresh(d.get("last_refresh")) else None
    ra["tuoi_anh_chup_gio"] = _tuoi_anh_chup_gio(d.get("last_refresh"))
    for ten, v in (d.get("tokens") or {}).items():
        # BỎ QUA `id_token`: nó NGẮN HẠN THEO THIẾT KẾ (đo được: 1.0h ngay sau
        # `codex login --device-auth`) và được làm mới tự động. Lấy nó làm tín hiệu
        # thì credential VỪA ĐÚC XONG đã bị gắn "sắp hết hạn" — chốt đỏ thường trực,
        # đúng thứ sẽ bị bỏ qua, và tôi đã tự dựng nó vào chính bản vá cảnh báo sớm.
        #
        # Ca 15-08 (`id_token=-39.1h` trên credential đã chết) KHÔNG mất: thứ bắt được
        # nó là TUỔI ẢNH CHỤP 40h, chứ không phải `id_token`. Tín hiệu thật vẫn còn.
        if ten in _TOKEN_KHONG_XET_HAN:
            continue
        if not isinstance(v, str) or v.count(".") != 2:
            continue
        goi = v.split(".")[1]
        goi += "=" * (-len(goi) % 4)
        try:
            exp = json.loads(base64.urlsafe_b64decode(goi)).get("exp")
        except Exception:
            continue
        if isinstance(exp, (int, float)):
            ra["gio_con_lai"][ten] = round((exp - time.time()) / 3600, 1)
    return ra


def _co_chan_codex() -> str | None:
    """Lý do codex đang bị CHẶN, hoặc `None` nếu không bị chặn.

    CHỐT DÙNG CHUNG cho MỌI đường gọi codex do kho cung cấp (cross-review lượt 9,
    HIGH). Bản trước chỉ đọc cờ ở `_do_codex`, nên `_do_codex_song` — đường THẬT SỰ
    chạy `codex exec` — đi thẳng qua. Một chốt mà chỉ một trong hai cửa đọc thì không
    phải chốt; reviewer gọi đúng là "xanh giả với phạm vi nó tự nhận".

    PHẠM VI, khai thẳng: cờ này chặn được các cửa CỦA KHO. Người dùng gõ `codex` ở
    terminal thì KHÔNG có gì đọc cờ — muốn chặn tới đó phải là cơ chế khác (đổi PATH,
    gói bọc), và ta KHÔNG làm thế vì nó lại là thứ sửa môi trường sau lưng người dùng.
    """
    try:
        co = _codex_home_hieu_luc() / CO_CHAN_CODEX
    except (OSError, ValueError):
        return "BI CHAN: CODEX_HOME khong hop le"
    if not co.exists():
        return None
    return (f"BI CHAN: {co} ton tai — config codex con khoi "
            f"shell_environment_policy cu (hoac khong phan loai duoc), "
            f"`inherit=all` co the con hieu luc. Chua: "
            f"`python3 .claude/dev/codex_env_policy.py --go` roi TU thay tep")


def _do_codex_song(han_giay: int = 90, duong_dan: str | None = None) -> tuple[bool, str]:
    """Phép thử SỐNG: gọi `codex` thật và soi lỗi xác thực.

    ĐẮT (tốn quota + mạng) nên KHÔNG chạy mặc định — chỉ khi phía gọi đòi
    `--kiem-song`. Nhưng đây là thứ DUY NHẤT chứng minh được credential còn dùng được:
    refresh token bị THU HỒI phía máy chủ thì không phép kiểm offline nào thấy.

    `duong_dan`: spawn bằng ĐƯỜNG DẪN ĐÃ RESOLVE, không spawn tên trần — xem chú
    thích tại `_do_codex` (Windows: CreateProcess không tra PATHEXT nên tên trần
    "codex" chết FileNotFoundError trong khi `codex.cmd` vẫn nằm ngay trên PATH).
    """
    bi_chan = _co_chan_codex()
    if bi_chan:
        # Đây là cửa THẬT SỰ chạy `codex exec`. Bản trước bỏ sót đúng cửa này.
        return (False, bi_chan)
    home = _codex_home_hieu_luc()
    if _dang_cho_snapshot(home):
        return False, "CHỜ snapshot Codex mới"
    try:
        helper = Path(__file__).with_name("codex_cred.py")
        if not helper.is_file():
            return False, "Thiếu repository codex_cred.py"
        probe = runpy.run_path(str(helper))["_kiem_song"]
        probe.__globals__["HAN_KIEM_SONG_GIAY"] = han_giay
        if duong_dan:
            probe.__globals__["_co_codex"] = lambda: duong_dan
        try:   # F03: danh tính của ĐÚNG bản sắp được probe; đọc không được thì như cũ
            with _KhoCodex(home) as store:
                da_probe = store.read()
        except (OSError, ValueError):
            da_probe = None
        ok, reason = probe(home)
        if not ok and reason.startswith("credential BỊ TỪ CHỐI ("):
            # wp484 g7 (P2 #509 thread XMG) — kết quả ghi trạng thái từng bị NUỐT: không lưu được
            # thì lần gọi sau lại thử đúng credential đã biết là hỏng mà không ai hay. Không ghi
            # được thì không có cách nào nhớ hộ; tối thiểu phải nói ra, và lý do phải khác hẳn.
            if not _danh_dau_auth_hong(home, da_probe):
                return False, (f"KHÔNG ghi được trạng thái chờ snapshot sau khi {reason} — "
                               "CHẶN: sửa CODEX_HOME (quyền/dung lượng) trước khi thử lại")
        return ok, reason
    except (OSError, ValueError, UnicodeError):
        return False, "Không kiểm được credential Codex"



def _do_codex(kiem_song: bool = False) -> tuple[str, str]:
    """Đo `codex` bằng MÃ THOÁT, không bằng dòng đầu của đầu ra.

    ĐÃ ĐO: `codex login status` trả `rc=1` + `Not logged in` khi chưa xác thực,
    `rc=0` + `Logged in using ChatGPT` khi đã xác thực.

    Bản nháp của chính hàm này đọc `ra[0]` — DÒNG ĐẦU — rồi tìm chữ "not logged in"
    trong đó. Phản chứng bắt được ngay: với `HOME` sạch, `codex` in trước một dòng
    `WARNING: proceeding, even though we could not create PATH aliases: …`, nên dòng
    đầu KHÔNG phải câu trạng thái, phép kiểm trượt, và hàm báo `DUNG_DUOC` cho một
    `codex` CHƯA đăng nhập. Hỏng theo chiều FAIL-OPEN — chiều nguy hiểm, và đúng
    cùng một lỗi với sự cố sáng nay: tin dòng đầu tiên một công cụ nói ra.

    Nay: `rc != 0` là CHƯA XÁC THỰC, dứt khoát; chữ chỉ dùng để giải thích, và tìm
    trong TOÀN BỘ đầu ra chứ không riêng dòng nào.
    """
    duong_codex = shutil.which("codex")
    if not duong_codex:
        return ("THIEU", "chua cai — npm install -g @openai/codex")
    bi_chan = _co_chan_codex()
    if bi_chan:
        return ("CHUA_XAC_THUC", bi_chan)
    if _dang_cho_snapshot(_codex_home_hieu_luc()):
        return ("CHUA_XAC_THUC", "CHỜ snapshot Codex mới; không lặp credential đã thất bại")
    try:
        # Spawn bằng ĐƯỜNG DẪN `which` đã trả, KHÔNG spawn tên trần. ĐO 19-08-2026
        # trên Windows (packet PLAT-M3, #185): `shutil.which` thấy
        # `...\nodejs\codex.CMD` (tra PATHEXT), nhưng CreateProcessW với tên trần
        # "codex" chỉ tự thêm ".exe" ⇒ FileNotFoundError — trong khi bảng `CONG_CU`
        # ngay trên đo CÙNG công cụ bằng đường dẫn resolve và ra version ngon lành.
        # Một `doctor` mà hai probe của nó phân giải cùng một tên ra hai kết quả
        # ngược nhau là doctor tự mâu thuẫn; mọi spawn CLI agent (.cmd shim của
        # npm) phải đi qua đường dẫn resolve.
        p = subprocess.run([duong_codex, "login", "status"], capture_output=True,
                           text=True, timeout=30, encoding="utf-8", errors="replace")
        ra = ((p.stdout or "") + (p.stderr or ""))
        rc = p.returncode
    except (OSError, subprocess.SubprocessError) as e:
        return ("KHONG_DO_DUOC", f"khong chay duoc: {type(e).__name__}")
    # Câu trạng thái nằm ở đâu cũng được — lọc dòng nhiễu (WARNING/hint) rồi lấy
    # dòng cuối còn lại, vì `codex` in trạng thái SAU các cảnh báo.
    dong = [d.strip() for d in ra.splitlines() if d.strip()
            and not d.strip().upper().startswith(("WARNING", "NOTE", "HINT"))]
    mo_ta = dong[-1][:70] if dong else f"rc={rc}, khong in gi"
    if rc == 0 and "not logged in" not in ra.lower():
        # ĐẾN ĐÂY MỚI CHỈ BIẾT: có tệp credential, đọc được, `codex` không kêu.
        # KHÔNG biết nó còn DÙNG ĐƯỢC.
        #
        # ĐÃ ĐO 15-08-2026, và đây là lần THỨ HAI cùng một lớp lỗi trong đúng hàm này:
        # `codex login status` trả "Logged in using ChatGPT" rc=0 trong khi MỌI lời gọi
        # thật trả 401 `refresh_token_invalidated`. Lệnh ấy chỉ kiểm tệp đọc được, không
        # kiểm token còn sống. Bản trước gọi thẳng trạng thái này là `DUNG_DUOC` — tức
        # NÂNG NHÃN VƯỢT QUÁ BẰNG CHỨNG, đúng cái bệnh đã đốt cả ngày hôm nay.
        #
        # Nay tách làm hai nhãn. `CO_CREDENTIAL` nói đúng thứ đã chứng minh được, và
        # chỉ `--kiem-song` (gọi thật, tốn quota) mới được cấp `DUNG_DUOC`.
        han = _han_token_codex()
        het = [t for t, g in han["gio_con_lai"].items()
               if g <= 0 and t not in _TOKEN_KHONG_XET_HAN]
        chi_tiet = mo_ta
        if han["gio_con_lai"]:
            chi_tiet += " · con " + ", ".join(
                f"{t}={g}h" for t, g in sorted(han["gio_con_lai"].items())
                if t not in _TOKEN_KHONG_XET_HAN)
        if han["last_refresh"]:
            chi_tiet += f" · last_refresh={han['last_refresh']}"
        if het:
            # HẾT HẠN là thứ ĐO ĐƯỢC offline ⇒ dám kết luận.
            return ("CHUA_XAC_THUC", f"token HET HAN: {', '.join(het)} · {chi_tiet}")
        # SẮP hết hạn / ảnh chụp CŨ ⇒ vẫn dùng được NHƯNG phải báo NGAY. Đây là mục
        # 3.1 của phương án chống tái diễn sự cố thu hồi: cảnh báo TRƯỚC, không phải sau.
        sap = [f"{t}={g}h" for t, g in sorted(han["gio_con_lai"].items())
               if 0 < g <= NGUONG_CANH_BAO_GIO and t not in _TOKEN_KHONG_XET_HAN]
        tuoi = han.get("tuoi_anh_chup_gio")
        anh_cu = tuoi is not None and tuoi >= NGUONG_ANH_CHUP_CU_GIO
        if sap or anh_cu:
            vi_sao = []
            if sap:
                vi_sao.append("sap het han: " + ", ".join(sap))
            if anh_cu:
                vi_sao.append(f"anh chup CU {tuoi}h (refresh token xoay vong - ban trong "
                              f"CODEX_AUTH_JSON co the da bi vo hieu)")
            # `--kiem-song` phải chạy KỂ CẢ khi sắp hết hạn. Bản trước trả về ngay ở
            # đây, nên đòi kiểm sống mà KHÔNG BAO GIỜ kiểm — phép đo bị chính cảnh báo
            # nuốt mất. "Sắp hết hạn" và "còn dùng được không" là HAI câu hỏi khác nhau.
            if kiem_song:
                song, ly_do = _do_codex_song(duong_dan=duong_codex)
                if not song:
                    return ("CHUA_XAC_THUC", f"kiem song HONG: {ly_do} · {chi_tiet}")
                vi_sao.append(f"kiem song: {ly_do} (VAN dung duoc)")
            return ("SAP_HET_HAN", " · ".join(vi_sao) + f" · {chi_tiet}")
        if not kiem_song:
            return ("CO_CREDENTIAL",
                    f"{chi_tiet} · CHUA chung minh dung duoc (them --kiem-song de goi that)")
        song, vi_sao = _do_codex_song(duong_dan=duong_codex)
        if song:
            return ("DUNG_DUOC", f"{chi_tiet} · kiem song: {vi_sao}")
        return ("CHUA_XAC_THUC", f"kiem song HONG: {vi_sao} · {chi_tiet}")
    if os.environ.get("CODEX_AUTH_JSON"):
        return ("CAN_CHUAN_BI",
                f"chua co auth.json TREN DIA (rc={rc}) nhung CO $CODEX_AUTH_JSON "
                f"— chay `launcher.py chuan-bi`")
    return ("CHUA_XAC_THUC",
            f"rc={rc} · {mo_ta} · khong co $CODEX_AUTH_JSON de dung ra dia")


def _do_claude() -> tuple[str, str]:
    if not shutil.which("claude"):
        return ("THIEU", "chua cai — npm install -g @anthropic-ai/claude-code")
    tep = Path(os.path.expanduser("~/.claude/.credentials.json"))
    # ĐÒI GIÁ TRỊ, không chỉ đòi TÊN. `ANTHROPIC_API_KEY=""` là chỗ giữ chỗ rất phổ
    # biến trong `.env` mẫu; đếm nó là credential thì `DUNG_DUOC` — nhãn DUY NHẤT được
    # tính là đã-chứng-minh — được cấp cho một môi trường KHÔNG có credential nào.
    # Cùng lỗi "CÓ MẶT ≠ DÙNG ĐƯỢC" mà chính tệp này đi chữa.
    bien = [k for k, v in os.environ.items()
            if re.search(r"ANTHROPIC_API_KEY|CLAUDE_CODE_OAUTH_TOKEN", k, re.I)
            and v.strip()]
    if tep.exists():
        return ("DUNG_DUOC", f"credential tren dia ({tep})")
    if bien:
        return ("DUNG_DUOC", "qua bien: " + ", ".join(sorted(bien)))
    return ("CHUA_XAC_THUC", "khong co ~/.claude/.credentials.json va khong co bien")


def _do_openai_llm(moi_truong: dict[str, str] | None = None,
                   kiem_song: bool = False) -> tuple[str, str]:
    """Đo năng lực gọi OpenAI API qua `llm` CLI.

    Giao thức (§4, §5 `ops/OPENAI_LLM_PROVIDER.md`):
      Provider: openai_api
      Execution surface: llm_cli
      Logging: bắt buộc `--no-log`
    Không bao giờ gọi API trả phí trong doctor mặc định; chỉ gọi khi có `--kiem-song`.
    """
    mt = _env_da_chuan(moi_truong)

    if not shutil.which("llm"):
        return ("THIEU", "chua cai llm CLI — pip install llm")

    p_ver = _chay_van_ban_an_toan(["llm", "--version"], env=mt, timeout=PROBE_TIMEOUT_GIAY)
    ver = p_ver.stdout.strip() if p_ver.returncode == 0 else "llm"

    # Kiểm tra OPENAI_API_KEY trong môi trường hoặc keys.json của llm
    tok = mt.get("OPENAI_API_KEY", "").strip()
    co_key_file = False
    if not tok:
        try:
            p_k = _chay_van_ban_an_toan(["llm", "keys", "list"], env=mt, timeout=PROBE_TIMEOUT_GIAY)
            if p_k.returncode == 0 and "openai" in p_k.stdout.lower():
                co_key_file = True
        except (OSError, subprocess.SubprocessError):
            pass

    if not tok and not co_key_file:
        return ("CHUA_XAC_THUC", f"{ver} · khong co OPENAI_API_KEY va chua co `llm keys set openai`")

    if not kiem_song:
        return ("CO_CREDENTIAL", f"{ver} · co credential OpenAI (chua chung minh dung duoc, them --kiem-song)")

    # Kiểm sống: gọi probe qua prompt không lưu log (--no-log)
    try:
        p_song = _chay_van_ban_an_toan(
            ["llm", "prompt", "in ra: ok", "-m", "gpt-4o-mini", "--no-log"],
            env=mt, timeout=30)
    except (OSError, subprocess.SubprocessError) as e:
        return ("KHONG_DO_DUOC", f"kiem song khong chay duoc: {type(e).__name__}")

    if p_song.returncode == 0:
        return ("DUNG_DUOC", f"{ver} · kiem song: thanh cong (gpt-4o-mini)")
    err_msg = p_song.stderr.strip() or p_song.stdout.strip()
    return ("CHUA_XAC_THUC", f"{ver} · kiem song HONG (rc={p_song.returncode}): {err_msg[:60]}")


def _do_antigravity(moi_truong: dict[str, str] | None = None) -> tuple[str, str]:
    """Đo năng lực gọi Antigravity CLI (`agy`) — AG-T0-01B.

    Bốn trạng thái (Spec 6.2):
      DUNG_DUOC: `agy models` rc=0 và có đầu ra (stdout+stderr) — đã xác thực
      CO_MAT: `--version` rc=0 nhưng `models` rc≠0 — đã cài, chưa đăng nhập
      KHONG_DO_DUOC: timeout, OSError, models rc=0 không đầu ra, hoặc cả hai probe thất bại — không làm tròn thành THIEU
      THIEU: không thấy binary, kể cả sau đường lùi PATH trên Windows
    """
    mt = _env_da_chuan(moi_truong)
    candidates = _cac_duong_dan({"ten": "agy", "ung_vien": ["agy"]}, mt)
    if not candidates:
        return ("THIEU", "chua cai agy CLI — irm https://antigravity.google/cli/install.ps1 | iex (Windows) / curl -fsSL https://antigravity.google/cli/install.sh | bash")

    path_items = [p for p in mt.get("PATH", "").split(os.pathsep) if p]
    loi_cuoi = None
    co_mat_str = None
    for _, duong_agy in candidates:
        la_fallback = False
        if platform.system() == "Windows":
            la_fallback = not any(Path(p).resolve() == Path(duong_agy).parent.resolve() for p in path_items if Path(p).exists()) if path_items else True
        duoi_path = " · đã cài, PATH phiên này chưa thấy — mở terminal mới" if la_fallback else ""

        # Probe 1: Thử `_xac_thuc` với subcommand `models` (Spec 6.2 & 6.3).
        # Trong một lượt `doctor`, bảng `CONG_CU` (`xac_thuc: ["models"]`) ĐÃ chạy đúng
        # lệnh này trên đúng đường dẫn này — đọc lại bằng chứng ấy thay vì chạy lần
        # hai (P2 cross-review PR "#426" trên `4639462`). Ngoài `doctor` bảng rỗng.
        da_do = _XAC_THUC_DA_DO.get((duong_agy, ("models",)))
        if da_do is not None:
            ok_xt, mo_ta_xt, qua_han_xt, ra_xt = da_do
        else:
            ok_xt, mo_ta_xt, qua_han_xt, ra_xt = _xac_thuc_kem_dau_ra(duong_agy, ["models"], env=mt, timeout=PROBE_TIMEOUT_GIAY)
        if ok_xt:
            # Đếm dòng từ ĐẦU RA CỦA CHÍNH PROBE VỪA CHẠY — không gọi `agy models` lần hai.
            # `models` đi mạng: lần hai quá hạn/OSError sẽ ném lên `lenh_doctor` và lật
            # bằng chứng dương thành KHONG_DO_DUOC (P2 cross-review PR "#426").
            so_dong = len([d for d in ra_xt.splitlines() if d.strip()])
            return ("DUNG_DUOC", f"da xac thuc qua `agy models` ({so_dong} model){duoi_path}")

        if qua_han_xt:
            loi_cuoi = ("KHONG_DO_DUOC", f"probe models timeout sau {PROBE_TIMEOUT_GIAY:.1f}s{duoi_path}")
            continue

        if mo_ta_xt == "rc=0 nhung khong co bang chung xac thuc":
            # Finding 1: models rc=0 nhưng không có đầu ra -> KHONG_DO_DUOC (không làm tròn thành CO_MAT hay DUNG_DUOC)
            loi_cuoi = ("KHONG_DO_DUOC", f"probe models khong co dau ra (rc=0 nhung khong co bang chung xac thuc){duoi_path}")
            continue

        # Probe 2: Nếu models rc != 0 hoặc lỗi khác, probe `--version` (Spec 6.2)
        chay_ver, dong_ver, qua_han_ver = _phien_ban(duong_agy, env=mt, timeout=PROBE_TIMEOUT_GIAY)
        if qua_han_ver:
            loi_cuoi = ("KHONG_DO_DUOC", f"probe --version timeout sau {PROBE_TIMEOUT_GIAY:.1f}s{duoi_path}")
            continue

        if chay_ver:
            ver_str = dong_ver[:40] if dong_ver else "agy"
            co_mat_str = ("CO_MAT", f"{ver_str} · chua dang nhap — chay `agy` (mo TUI de login){duoi_path}")
        else:
            loi_cuoi = ("KHONG_DO_DUOC", f"probe agy that bai (models: {mo_ta_xt}, --version: {dong_ver}){duoi_path}")

    if co_mat_str:
        return co_mat_str
    if loi_cuoi:
        return loi_cuoi
    return ("KHONG_DO_DUOC", "probe agy khong xac dinh")


_RE_SLUG_GITHUB = re.compile(r"github\.com[:/]+([^/]+/[^/\s]+?)(?:\.git)?/*$")


def _do_rest_github(url: str, timeout: float = 6.0, *, token: str | None = None) -> tuple[str, str, bool]:
    """Đo MỘT đường REST. Trả (`mo`|`chan`|`khong_do_duoc`, mô tả, THAO TÁC THÀNH CÔNG).

    Ba giá trị vì có BA câu hỏi khác nhau, và gộp chúng là lỗi đã trả giá: đường
    có thông không · nó hỏng vì ai · và ta có LÀM ĐƯỢC VIỆC không. Một 404 kho
    riêng tư trả lời "thông" cho câu một và "không" cho câu ba.

    DẤU HIỆU PHÂN BIỆT là HEADER `X-GitHub-*`, KHÔNG phải mã trạng thái. Đo
    17-08-2026: `/repos/<kho>` trả 403 **không header GitHub nào**, còn
    `/rate_limit` và `/user` trả 200 **có** header — nghĩa là 403 kia do PROXY tự
    sinh, phản hồi chưa từng tới GitHub. Phân loại bằng mã trạng thái đơn thuần
    sẽ đọc nhầm nó thành "GitHub từ chối ta", rồi người đọc đi tìm quyền token —
    sai hướng hoàn toàn, vì token KHÔNG đổi gì (đo cả có lẫn không: y hệt).

    Một 4xx CÓ header GitHub vẫn là `mo`: đường tới nơi, chỉ là ta không có
    quyền — hai chuyện khác nhau và phải chữa bằng hai cách khác nhau.

    Trạng thái thứ ba `khong_do_duoc` (mạng hỏng, DNS, quá hạn) KHÔNG được gộp
    vào `chan` — đúng doctrine `None ≠ False`.
    """
    dau = {"Accept": "application/vnd.github+json"}
    # Credential ĐÃ CHUẨN HOÁ phải đi tới ĐÂY. `_doc_moi_truong` loại bản giữ chỗ và
    # ánh xạ `GITHUB_PAT` thật sang `GH_TOKEN`, nhưng sửa xong mà không nối vào chỗ
    # DÙNG thì bản sửa chỉ nằm trong biến trả về: probe vẫn đi bằng chuỗi giữ chỗ, và
    # một kho RIÊNG TƯ sẽ báo `chan` trong khi PAT thật đọc được (P2 PR "#143").
    if token:
        dau["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=dau)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            co_gh = any(k.lower().startswith("x-github") for k in r.headers)
            return ("mo" if co_gh else "chan",
                    f"HTTP {r.status}" + ("" if co_gh else " (KHONG header GitHub -> proxy tu sinh)"),
                    co_gh and 200 <= int(r.status) < 300)
    except urllib.error.HTTPError as e:
        co_gh = any(k.lower().startswith("x-github") for k in e.headers)
        # 4xx CÓ header GitHub = TỚI NƠI nhưng THAO TÁC HỎNG. `mo` đúng cho câu
        # "đường có thông không"; `thanh_cong=False` đúng cho câu "làm được việc
        # không". Gộp hai câu ấy chính là lỗi P1 mà cross-review bắt trên PR "#143".
        return ("mo" if co_gh else "chan",
                f"HTTP {e.code}" + (" (toi GitHub, thieu quyen)" if co_gh
                                    else " (KHONG header GitHub -> proxy tu sinh)"),
                False)
    except Exception as e:                       # mạng/DNS/quá hạn = KHÔNG ĐO ĐƯỢC
        return ("khong_do_duoc", f"{type(e).__name__}", False)


# --- ĐƯỜNG MCP -------------------------------------------------------------------
# VÌ SAO THÊM. `_do_github` đo `git`, `gh`, `rest` — nhưng đường mà kho THẬT SỰ dùng
# hằng ngày (công cụ `mcp__github__*`) thì KHÔNG nằm trong phép đo nào, và launcher
# chưa từng đọc `.mcp.json` (`grep -c mcp` = 0 trước bản này). Docstring của hàm ấy
# LIỆT KÊ "công cụ MCP github CHẠY" như một dữ kiện đã đo — nhưng đó là quan sát
# đóng băng trong chú thích, không phải phép đo chạy mỗi lượt. Đúng lớp bệnh mà chính
# `_do_github` vừa chữa cho `rest` ("có thể bị chặn" không phải phép đo).

_RE_ANSI = re.compile(r"\x1b\[[0-9;]*m")
_RE_STATUS = re.compile(r"^\s*Status:\s*(.+?)\s*$", re.MULTILINE)
# Ký hiệu trang trí ĐO ĐƯỢC: `√` `×` `⏸`. Cắt mọi thứ KHÔNG phải chữ/số ở đầu.
_RE_TRANG_TRI = re.compile(r"^[^0-9a-z]+")
_MCP_KHOE = ("connected",)                  # khớp ĐÚNG BẰNG, không phải tiền tố
_MCP_HONG = ("failed to connect", "pending approval", "not connected",
             "disconnected", "needs authentication")   # khớp TIỀN TỐ (có đuôi chi tiết)


def _env_da_chuan(mt: dict[str, str] | None) -> dict[str, str]:
    """Trả môi trường ĐÃ CHUẨN HOÁ, không bao giờ trả `None`.

    VÌ SAO LÀ HÀM RIÊNG chứ không chép hai dòng như `_do_github`: chép thì đoạn mã
    TRÙNG KHÍT nhau, mà `chay_dot_bien` thay chỗ khớp ĐẦU TIÊN — nên một đột biến nhắm
    `_do_github` sẽ lặng lẽ nhảy sang bản sao đứng trước nó, và ca đích không chết nữa.
    ĐÃ XẢY RA THẬT ở đúng bản vá này: `probe_github_bo_qua_moi_truong_chuan_hoa` (đột
    biến CÓ SẴN của master, canh `t113`) SỐNG SÓT ngay khi khối MCP được chèn vào phía
    trên. Không dòng logic nào sai — chốt chỉ mất răng vì trùng chữ. Tách hàm làm hai
    chỗ khác mặt nhau, nên mỗi đột biến lại nhắm đúng chỗ nó định nhắm.
    """
    if mt is not None:
        return mt
    if _MOI_TRUONG_DA_DOC is not None:
        return _MOI_TRUONG_DA_DOC
    return _doc_moi_truong()[0]


def _doc_mcp_json(ws: str | None, *, kem_headers: bool = False):
    """`.mcp.json` của DỰ ÁN có khai server `github` không, khai bằng TÊN NÀO, ở URL NÀO.

    Đây là phép đo CÓ MẶT, không phải DÙNG ĐƯỢC — và nói thẳng như vậy ở chỗ dùng.
    Nhưng nó phân biệt được "chưa khai server" (đo được, hỏng thật, chữa được) với
    "đã khai, chưa ai chứng minh nó chạy".

    Mặc định trả `(có_khai, mô_tả, tên_nguyên_văn, url)` để giữ hợp đồng của
    `doctor`. Khi ``kem_headers=True``, trả thêm phần tử thứ năm từ CHÍNH ảnh JSON
    đã dùng để chọn URL; caller HTTP nhờ đó không phải đọc lại tệp rồi ghép hai ảnh.

    `url` LÀ THỨ RIÊNG, và `có_khai` KHÔNG phụ thuộc nó. Hai câu hỏi khác nhau:
    `mcp-cli` chỉ cần TÊN (nó hỏi CLI), `mcp-endpoint` mới cần URL. Gộp lại thì một
    `.mcp.json` khai server kiểu `stdio` (không có `url`, hoàn toàn hợp lệ) sẽ bị
    tuyên là "chưa khai server" — sai, và sai ở phía làm người đọc đi chữa nhầm chỗ.
    URL hỏng/thiếu ⇒ `url is None`, và bên đo endpoint tự khai `khong_do_duoc`.
    """
    # NÓI RÕ ĐỌC Ở GỐC NÀO. `doctor` chạy ngoài repo thì `ws` là None và ta lùi về gốc
    # của chính launcher — hợp lý, nhưng im lặng thì người đọc tưởng đang xem kho họ
    # vừa trỏ tới. Đo một CÂY KHÁC cây người ta hỏi mà không khai là đúng lớp lỗi đã
    # đốt cả buổi ở `refs/pull/*/merge`.
    if ws:
        goc, nguon = Path(ws), "workspace"
    else:
        goc, nguon = Path(__file__).resolve().parents[2], "goc cua launcher (khong co workspace)"
    tep = goc / ".mcp.json"
    rong = (None,) if kem_headers else ()
    if not tep.is_file():
        return (False, f"khong thay .mcp.json o {goc} [{nguon}]", None, None) + rong
    try:
        d = json.loads(tep.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return (False, f".mcp.json [{nguon}] khong doc/parse duoc: {type(e).__name__}", None, None) + rong
    # KIỂM KIỂU BA TẦNG. JSON hợp lệ vẫn có thể sai lược đồ, và mỗi tầng là một
    # finding RIÊNG của cross-review: gốc là mảng ⇒ `d.get` ném AttributeError; bảng
    # server là mảng ⇒ vòng lặp duyệt PHẦN TỬ chứ không duyệt KHOÁ; giá trị của khoá
    # `github` là `null`/chuỗi ⇒ vẫn được tuyên là "đã khai". Cùng một hình dạng lỗi
    # tụt xuống sau mỗi tầng — nên kiểm hết một lượt thay vì vá dần theo báo cáo.
    if not isinstance(d, dict):
        return (False, f".mcp.json [{nguon}] khong phai object o goc (la {type(d).__name__})", None, None) + rong
    # PHÂN BIỆT "KHÔNG CÓ KHOÁ" VỚI "CÓ KHOÁ MÀ GIÁ TRỊ HỎNG": `or` nuốt mọi giá trị
    # FALSY nên `{"mcpServers": null, "servers": {...}}` lặng lẽ rơi sang trường dự
    # phòng rồi tuyên là đã khai — một trường CHÍNH sai kiểu bị trường DỰ PHÒNG che.
    for khoa in ("mcpServers", "servers"):
        if khoa in d:
            srv = d[khoa]
            break
    else:
        return (False, f".mcp.json [{nguon}] khong co khoa `mcpServers` lan `servers`", None, None) + rong
    if not isinstance(srv, dict):
        return (False, f".mcp.json [{nguon}] khoa `{khoa}` khong phai object (la {type(srv).__name__})", None, None) + rong
    # KHỚP CHÍNH XÁC sau chuẩn hoá hoa/thường, KHÔNG khớp chuỗi con: `not-github-backup`
    # từng được tính là "đã khai server github". Danh sách CHO PHÉP, không phải đoán
    # xem còn bao nhiêu cách viết.
    ten = [k for k in srv if k.casefold() == "github"]
    if not ten:
        return (False, (f".mcp.json [{nguon}] KHONG khai server ten dung bang `github` "
                        f"(co: {', '.join(srv) or 'khong co server nao'})"), None, None) + rong
    # NHIỀU TÊN CÙNG KHỚP ⇒ TỪ CHỐI, không chọn theo thứ tự khai báo. `claude mcp get`
    # coi `github` và `GitHub` là HAI server khác nhau (đo được: nó gợi ý "Did you
    # mean"), nên chọn `ten[0]` làm server được đo phụ thuộc THỨ TỰ KHOÁ trong JSON —
    # hai tệp cùng tập server mà đảo thứ tự sẽ cho hai nhãn khác nhau. Một phép đo bất
    # định thì không phải phép đo.
    if len(ten) > 1:
        return (False, (f".mcp.json [{nguon}] khai {len(ten)} server cung khop `github` sau "
                        f"chuan hoa hoa/thuong ({', '.join(sorted(ten))}) — MO HO, khong biet "
                        f"do cai nao; `claude mcp get` coi chung la hai server khac nhau"), None, None) + rong
    xau = [k for k in ten if not isinstance(srv[k], dict)]
    if xau:
        return (False, (f".mcp.json [{nguon}] khai `{', '.join(xau)}` nhung gia tri khong "
                        f"phai object (la {', '.join(type(srv[k]).__name__ for k in xau)})"), None, None) + rong
    # TRẢ TÊN NGUYÊN VĂN, không trả chuỗi dựng sẵn: `claude mcp get` PHÂN BIỆT HOA
    # THƯỜNG — khai `GitHub` rồi hỏi `mcp get github` thì CLI đáp `No MCP server named
    # "github". Did you mean "GitHub"?` và VẪN `rc=0`. Hai nơi phải dùng CÙNG một tên.
    # URL: lấy nếu có, KHÔNG bắt buộc. `str.strip()` trước khi trả để một giá trị
    # toàn khoảng trắng không đi tiếp thành "đã có URL".
    url = srv[ten[0]].get("url")
    url = url.strip() if isinstance(url, str) and url.strip() else None
    # KHONG noi suy `url` NGUYEN VAN vao mo ta. Finding R3 cua luot review 3: mot
    # `.mcp.json` khai `https://user:GOCSPX-abc@host/mcp` lam mo ta CHUA bi mat. Hien
    # caller duy nhat (`_do_github`) vut chuoi nay o nhanh duong nen chua lo ra ngoai —
    # nhung bat bien viet ngay trong `_do_mcp_endpoint` la "KHONG mot nhanh nao duoc mang
    # DU LIEU LAY TU url", va mot ham ben canh dung chuan khac la khau sung da nap dan:
    # them mot caller, hoac ai in truong nay vao JSON cua `doctor`, la lo ngay.
    # Chi in scheme + host — du de nguoi doc biet no tro DI DAU ma khong cho duoc bi mat.
    if url:
        try:
            _p = urllib.parse.urlsplit(url)
            _noi = f"{_p.scheme}://{_p.hostname}" if _p.hostname else "(url khong co ten may)"
        except ValueError:
            _noi = "(url khong phan tich duoc)"
        _duoi = f" @ {_noi}"
    else:
        _duoi = " (khong khai `url`)"
    kq = (True, f".mcp.json [{nguon}] khai server: {ten[0]}" + _duoi, ten[0], url)
    if not kem_headers:
        return kq
    muc = srv[ten[0]]
    headers = muc["headers"] if "headers" in muc else {}
    if not isinstance(headers, dict):
        return (False, f".mcp.json [{nguon}] headers cua `{ten[0]}` khong phai object",
                None, None, None)
    return kq + (headers,)


def _suc_khoe_mcp_github(ten: str = "github",
                         moi_truong: dict[str, str] | None = None) -> tuple[str, str]:
    """Hỏi `claude mcp get <tên>` xem server đang ở trạng thái nào.

    VÌ SAO DÙNG `get` CHỨ KHÔNG `list` — chữa ở TẦNG, không vá thêm biểu thức. Ba bản
    trước đều bổ dòng tóm tắt của `list` bằng dấu phân cách, và cả ba đều sai:
      · dò chuỗi con cả dòng   -> `Disconnected` thành "khoẻ"
      · `rpartition(" - ")`    -> `Connected - 3 tools` thành "hỏng"
      · tiền tố `connected`    -> `Connected (stale)` thành "khoẻ"
    Đo thật mới thấy dòng `list` KHÔNG THỂ bổ đúng, vì phần đứng TRƯỚC dấu phân cách
    là câu lệnh của server, mà câu lệnh chứa được bất cứ thứ gì:

        broken: /nonexistent/binary  - × Failed to connect — ENOENT: ...

    `claude mcp get` trả TRƯỜNG CÓ NHÃN (`Status:`) nên hết phải đoán ranh giới.

    BA TRẠNG THÁI ĐO ĐƯỢC (dựng server MCP thật trong HOME tạm, không đụng config
    người dùng): `√ Connected` · `× Failed to connect` · `⏸ Pending approval`.

    MẶC ĐỊNH LÀ `khong_do_duoc`, KHÔNG phải `hong`: ép mọi chuỗi vào nhị phân tốt/xấu
    chính là cỗ máy sinh ra cả ba lỗi trên. Chỉ chuỗi ĐÃ ĐO mới được phân loại.

    PHẠM VI — phải khai kẻo lại khai rộng hơn thứ đo được. `mcp get` đọc trạng thái
    DUYỆT SERVER `.mcp.json` CHO DỰ ÁN NÀY theo con mắt CLI — tức thứ mà một tiến
    trình `claude` MỚI SINH sẽ gặp — chứ KHÔNG phải công cụ của phiên đang chạy. Hai
    thứ lệch nhau được: đo được `Pending approval` trong khi phiên vẫn gọi
    `mcp__github__*` bình thường (cross-review đo độc lập, xác nhận). Với `launcher.py`
    thì đó ĐÚNG là câu hỏi cần — việc của nó là SINH agent bằng CLI.

    Trả (`khoe` | `hong` | `khong_do_duoc`, chi tiết).
    """
    if not shutil.which("claude"):
        return ("khong_do_duoc", "khong co `claude` de hoi `mcp get`")
    # CHUAN HOA NGAY TAI DAY, khong tin call-site. `subprocess.run(env=None)` KE THUA
    # `os.environ` THO — tuc dung bien GIU CHO ma `_doc_moi_truong` vua loai, dung lop
    # P2 mà #143 đã vá một lần. Bản trước để mặc định `None` đi thẳng xuống, và
    # cross-review lượt 7 hạ đúng nó: đường sản xuất hiện thời có chuẩn hoá trước khi
    # gọi, nên chưa tái phát — nhưng chốt phải bảo vệ HỢP ĐỒNG, không dựa vào việc mọi
    # call-site đều nhớ. Gọi thẳng `_suc_khoe_mcp_github()` theo mặc định là đủ để môi
    # trường thô lọt xuống.
    moi_truong = _env_da_chuan(moi_truong)
    try:
        r = subprocess.run(["claude", "mcp", "get", ten], capture_output=True, text=True,
                           encoding="utf-8", errors="replace",
                           env=moi_truong, stdin=subprocess.DEVNULL,
                           timeout=PROBE_TIMEOUT_GIAY)
    except (OSError, subprocess.SubprocessError) as e:
        return ("khong_do_duoc", f"`claude mcp get {ten}` khong chay duoc: {type(e).__name__}")
    # LẤY `Status:` ĐẦU TIÊN — lựa chọn CÓ TẢI TRỌNG, không phải tình cờ. Đo được:
    # nội dung do `.mcp.json` kiểm soát CHÈN ĐƯỢC một dòng `Status:` thứ hai (đặt args
    # của server thành chuỗi có xuống dòng ⇒ `grep -c "Status:"` = 2). Bản giả nằm SAU
    # bản thật vì CLI in `Status` trước mọi trường có giá trị do người dùng đặt, và
    # thứ in trước nó (tên server, `Scope:`) thì tên phải casefold ra `github` nên
    # không chứa được xuống dòng. Cross-review dựng lại độc lập và xác nhận.
    kq = _RE_STATUS.search(_RE_ANSI.sub("", r.stdout or ""))
    if not kq:
        return ("khong_do_duoc",
                f"`claude mcp get {ten}` khong in truong `Status:` (rc={r.returncode}) — "
                f"CHU Y rc=0 KHONG co nghia la tim thay: CLI tra rc=0 ca khi bao "
                f'"No MCP server named"')
    tho = kq.group(1)
    chuan = " ".join(_RE_TRANG_TRI.sub("", tho.casefold()).split())
    if chuan in _MCP_KHOE:
        return ("khoe", f"Status: {tho}")
    if chuan.startswith(_MCP_HONG):
        return ("hong", f"Status: {tho}")
    return ("khong_do_duoc", f"trang thai LA, chua tung do: Status: {tho}")


# --- ĐẦU KIA CỦA DÂY MCP ----------------------------------------------------------
# VÌ SAO THÊM (PLAT-M4, #194). Khối trên đo `.mcp.json` + `claude mcp get`, tức CẢ HAI
# đều hỏi phía CLI — DÂY NỐI. Không bước nào chạm tới đầu kia. Đo được: `claude mcp get
# github` trả `Pending approval` trong khi POST `initialize` thẳng tới chính URL ấy trả
# HTTP 200 kèm header GitHub đầy đủ. Một phiên web/điện thoại đọc `mcp=khong` rồi kết
# luận "GitHub bị chặn" và dừng — ĐÃ XẢY RA, mất trọn một lượt — trong khi đường vẫn
# thông. Hai câu hỏi khác nhau thì phải là HAI trường, đúng phép tách mà `_do_github` đã
# làm cho `rest` (`rest-chung` / `rest-kho`).

_MCP_GIAO_THUC = "2025-06-18"


def _do_mcp_endpoint(url: str | None, *, token: str | None = None,
                     timeout: float = PROBE_TIMEOUT_GIAY) -> tuple[str, str, bool]:
    """Một lượt `initialize` JSON-RPC tới endpoint MCP. Trả (`mo`|`chan`|`khong_do_duoc`,
    mô tả, THAO TÁC THÀNH CÔNG).

    PHẠM VI — khai trước kẻo lại tuyên rộng hơn thứ đo được. Nó chứng minh **endpoint
    TRẢ LỜI và token được nhận**; nó KHÔNG chứng minh phiên nào đó gọi được
    `mcp__github__*`, cũng không chứng minh đọc được kho này. Vì vậy `mcp-endpoint`
    CỐ Ý đứng ngoài `LAM_DUOC_VIEC` — cùng hạng `rest-chung`, không cùng hạng
    `rest-kho`. Kho đã ba lần đếm SỰ CÓ MẶT của một đường thay vì KHẢ NĂNG của nó
    (`shutil.which("gh")` · `rest-chung` · `gh auth status`); đây là chỗ thứ tư dễ tái
    phạm nhất.

    `initialize` là HANDSHAKE: không tạo, không sửa, không xoá gì phía máy chủ. Một
    lượt, **không auto-retry** — `doctor` là phép ĐO, không phải nỗ lực kết nối; retry
    làm số đo nhoè và làm một lượt `doctor` dài gấp đôi khi mạng hỏng.

    DẤU HIỆU PHÂN LOẠI LÀ HEADER `X-GitHub-*`, KHÔNG phải mã trạng thái — cùng tiêu chí
    `_do_rest_github` đã trả giá để có: 403 KHÔNG header là proxy tự sinh (phản hồi chưa
    từng tới GitHub), còn 4xx CÓ header là tới nơi nhưng thiếu quyền. Hai chuyện ấy chữa
    bằng hai cách khác hẳn nhau.
    """
    # KHÔNG CÓ URL / URL KHÔNG PHẢI HTTP ⇒ CHƯA ĐO ĐƯỢC, không phải HỎNG. Server kiểu
    # `stdio` không có `url` là khai hợp lệ; gọi nó là "hỏng" thì đẩy người đọc đi chữa
    # một thứ không gãy. Và `urlopen` nhận cả `file://` — một `.mcp.json` trỏ `file:///`
    # sẽ biến probe mạng thành lượt ĐỌC ĐĨA, nên chặn theo danh sách CHO PHÉP.
    if not url:
        return ("khong_do_duoc", "`.mcp.json` khong khai `url` cho server nay "
                                 "(server kieu stdio thi dieu do la BINH THUONG)", False)
    # KHOP TIEN TO CHUOI KHONG PHAI PHAN TICH URL — bai hoc PLAT-M4 luot 1 (P2).
    # `https://user:SECRET@host/mcp` qua duoc `startswith`, roi bi mat di NGUYEN VAN vao
    # `req.full_url` VA `req.host`. Nen phan tich CAU TRUC, va bat `userinfo` TRUOC scheme.
    #
    # VA MOT NUA THU HAI, do luot review 2/2 tim ra: doi thu tu THOI VAN CHUA DU.
    # Nhanh `userinfo` chi bat duoc URL PHAN TICH DUOC thanh userinfo. URL MEO —
    # `http:///user:S@h`, `javascript:user:S@h`, `http ://user:S@h`, `http://?u=user:S@h` —
    # khong co `username`/`password`, nen chung roi xuong nhanh scheme/hostname, va hai
    # nhanh ay tung noi suy `{url!r}`: KHONG probe nua nhung VAN lam lo bi mat qua MO TA.
    # Cung HINH DANG voi chinh finding goc, chi doi duong ra.
    # ⇒ LUAT O DAY: KHONG mot nhanh TU CHOI nao duoc mang DU LIEU LAY TU `url`. Ke ca
    # `scheme`: `urlsplit("GOCSPX-abc:x")` cho scheme `gocspx-abc`, tuc chinh bi mat.
    # Chan doan mat do CHINH XAC va duoc lai mot bao dam CAU TRUC — doi ay la co y.
    try:
        p_ep = urllib.parse.urlsplit(str(url))
        chu_ep, may_ep = p_ep.scheme.lower(), p_ep.hostname
        ai_ep = (p_ep.username, p_ep.password)
        # `.port` PHAI duoc doc TRONG `try` nay. Ly do la mot finding cua luot review 3
        # (R1): `urlsplit` chi gan `username`/`password` khi co dau `@`, nen mot bi mat
        # dat o VI TRI PORT — `https://host:GOCSPX-abc/mcp` — di qua het ba chot duoi
        # (khong userinfo, scheme https, co hostname) roi vao thang `Request`.
        # Runtime that KHONG lo: `http.client` nem `InvalidURL` truoc khi mo socket. Nhung
        # do la chot cua NGUOI KHAC, khong phai chot cua ta — cung ho voi bai hoc "cong
        # khong noi doi, no VANG MAT". `.port` la property ném `ValueError` voi port phi
        # so, nen doc no o day la du: ca dong roi vao nhanh `khong_do_duoc` ngay ben duoi,
        # va khong nhanh nao mang du lieu tu `url` ra.
        _ = p_ep.port
    except ValueError as e:
        # Ten LOP ngoai le la tap dong, khong lay tu `url`.
        return ("khong_do_duoc", f"`url` khong phan tich duoc ({type(e).__name__})", False)
    if ai_ep != (None, None):
        return ("khong_do_duoc", "`url` nhung credential trong userinfo — TU CHOI, KHONG "
                                 "probe (bi mat se di vao URL va header Host)", False)
    if chu_ep not in ("http", "https"):
        return ("khong_do_duoc", "`url` khong phai http(s) — scheme ngoai danh sach cho "
                                 "phep (KHONG in `url` ra day: no co the dang cho bi mat)",
                False)
    if not may_ep:
        return ("khong_do_duoc", "`url` khong co ten may (KHONG in `url` ra day: no co the "
                                 "dang cho bi mat)", False)
    dau = {"Content-Type": "application/json",
           "Accept": "application/json, text/event-stream"}
    if token:
        dau["Authorization"] = f"Bearer {token}"
    than = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": _MCP_GIAO_THUC, "capabilities": {},
                   "clientInfo": {"name": "tra-luat-launcher-doctor", "version": VERSION}},
    }).encode("utf-8")
    req = urllib.request.Request(url, data=than, headers=dau, method="POST")
    # MÔ TẢ KHÔNG BAO GIỜ CHỞ TOKEN. Không nội suy `dau`, không in `req.headers`, và
    # cũng không in thân phản hồi — máy chủ đầu kia quyết định thân ấy, và đã có tiền lệ
    # một chuỗi trong thân bị đọc thành trạng thái.
    # TÊN BIẾN `*_ep` LÀ CÓ CHỦ ĐÍCH (xem chú thích ở nhánh `except` cuối): trùng chữ với
    # `_do_rest_github` thì mọi mẫu đột biến viết cho ĐƯỜNG NÀY sẽ vá nhầm sang đường kia.
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            co_gh_ep = any(k.lower().startswith("x-github") for k in r.headers)
            ma_ep = int(r.status)
            ghi_chu_ep = "" if co_gh_ep else " (KHONG header GitHub -> proxy tu sinh)"
            return (("mo" if co_gh_ep else "chan"), f"HTTP {ma_ep}{ghi_chu_ep}",
                    co_gh_ep and 200 <= ma_ep < 300)
    except urllib.error.HTTPError as e:
        co_gh_ep = any(k.lower().startswith("x-github") for k in e.headers)
        vi_sao_ep = (" (toi GitHub, thieu quyen)" if co_gh_ep
                     else " (KHONG header GitHub -> proxy tu sinh)")
        # 4xx/5xx: tới nơi hay không thì THAO TÁC vẫn hỏng — hai câu hỏi, hai giá trị.
        return (("mo" if co_gh_ep else "chan"), f"HTTP {e.code}{vi_sao_ep}", False)
    except Exception as e:                       # mạng/DNS/quá hạn = KHÔNG ĐO ĐƯỢC
        # VIẾT KHÁC CHỮ với `_do_rest_github` LÀ CÓ CHỦ ĐÍCH, không phải ngẫu nhiên:
        # `t117` đòi mỗi mẫu đột biến khớp ĐÚNG MỘT chỗ, nên một dòng mới trùng chữ với
        # dòng mà một mutant đang nhắm sẽ tước răng của mutant đó (nó vá nhầm chỗ). Đã
        # ĐỎ thật ở lượt đầu của PLAT-M4 với đúng hai mẫu `rest_*`.
        return ("khong_do_duoc", f"{type(e).__name__} khi POST initialize", False)


def _nhan_duong(ok) -> str:
    """Kết xuất BA trạng thái của một đường: mở · hỏng · CHƯA ĐO ĐƯỢC.

    Bản trước ghi `'OK' if ok else 'khong'`, tức ép mọi thứ vào nhị phân — nên một
    đường KHÔNG ĐO ĐƯỢC hiện ra y hệt một đường ĐÃ ĐO VÀ HỎNG. Đó chính là chỗ
    `None != False` mà kho đã ghi sổ, và nó đắt đúng ở đây: người đọc thấy `mcp=khong`
    sẽ đi chữa server, trong khi sự thật có thể là "máy này không có `claude` để hỏi".

    CÒN MỘT CHỖ CÙNG BỆNH, khai ra để không ai tưởng đã quét hết: nhánh `rest-kho`
    khi không đọc được slug origin tự mô tả là `KHONG DO DUOC` nhưng vẫn đẩy cờ
    `False`. Sửa nó là thay đổi RIÊNG (nó đổi ngữ nghĩa một đường đang tính vào
    `LAM_DUOC_VIEC`), nên bản này KHÔNG đụng — chỉ ghi ra.
    """
    return "chua-do-duoc" if ok is None else ("OK" if ok else "khong")


def _do_github(ws: str | None, moi_truong: dict[str, str] | None = None) -> tuple[str, str]:
    """Đo GitHub theo BA ĐƯỜNG ĐỘC LẬP, vì chúng hỏng độc lập với nhau.

    Đo được 15-08-2026 trong container remote:

      git đẩy/kéo HTTPS   CHẠY  (credential qua $GIT_CONFIG_KEY_*)
      công cụ MCP github  CHẠY  (đăng comment, đọc issue — dùng suốt ngày)
      REST api.github.com CHẶN  403 do PROXY, kèm nguyên văn "GitHub access is not
                                enabled for this session" — KHÔNG phải lỗi của
                                GitHub, KHÔNG phải thiếu token: `GITHUB_PAT` thật
                                cũng 403, mà `/user` lại 200. Chính sách theo
                                ĐƯỜNG DẪN, không theo danh tính.
      gh CLI              KHONG cai

    Vì vậy "gọi GitHub không được" là KẾT LUẬN SAI ở container này: hai trong bốn
    đường vẫn mở. Hàm này trả về ĐƯỜNG NÀO mở, để không ai kết luận theo đường hỏng.
    """
    # LÙI VỀ BẢN ĐÃ CHUẨN HOÁ, KHÔNG VỀ `os.environ` THÔ (P2 review "#143").
    # `_MOI_TRUONG_DA_DOC` chỉ được đặt trong `lenh_doctor`; mọi đường gọi khác
    # (bảng `KHA_NANG` từ lệnh khác, hoặc gọi trực tiếp) sẽ truyền `None`, và lùi
    # về `os.environ` là lùi về ĐÚNG bản giữ chỗ mà `_doc_moi_truong` vừa loại.
    # Sửa một chỗ rồi để đường lùi mang lại cái sai thì chưa sửa.
    if moi_truong is None:
        moi_truong = _MOI_TRUONG_DA_DOC
    if moi_truong is None:
        moi_truong, _ = _doc_moi_truong()
    mt = moi_truong
    tok = mt.get("GH_TOKEN") or None
    duong = []
    if ws:
        rc, out, _ = _git(ws, "ls-remote", "--heads", "origin", "HEAD")
        duong.append(("git", rc == 0, "day/keo HTTPS" if rc == 0 else f"rc={rc}"))
    # `gh` CÓ MẶT không chứng minh gì — `gh auth status` mới hỏi đúng câu "đã đăng nhập
    # chưa" (nó thoát 1 khi có vấn đề xác thực). Bản trước đếm `shutil.which("gh")` là
    # một ĐƯỜNG MỞ, nên ngoài repo thì chỉ cần CÀI `gh` là `any(...)` thành True và
    # GitHub được gắn `DUNG_DUOC` mà không có lấy một đường đã xác thực nào.
    if shutil.which("gh"):
        try:
            pg = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True,
                                encoding="utf-8", errors="replace",
                                env=mt, stdin=subprocess.DEVNULL, timeout=20)
            duong.append(("gh-cli", pg.returncode == 0,
                          "da xac thuc" if pg.returncode == 0 else f"CHUA xac thuc (rc={pg.returncode})"))
        except (OSError, subprocess.SubprocessError) as e:
            duong.append(("gh-cli", False, f"khong chay duoc: {type(e).__name__}"))
    else:
        duong.append(("gh-cli", False, "chua cai"))

    # --- REST: ĐO, KHÔNG ĐOÁN.
    # Bản trước NỐI THÊM câu "REST truc tiep co the bi proxy chan (403)" vào MỌI kết
    # quả, vô điều kiện. "Có thể" không phải phép đo, và câu ấy đúng/sai tuỳ nền —
    # nó chỉ là ghi chú của một lần quan sát bị đóng băng thành khẳng định. Tệ hơn:
    # docstring khai "đo theo các đường độc lập" trong khi hàm chỉ đo `git` và `gh`,
    # tức PHẠM VI TUYÊN BỐ lớn hơn phạm vi ĐO ĐƯỢC — đúng lỗi kho đã ghi sổ.
    #
    # Hai đường REST cố ý khác nhau, vì chính SỰ KHÁC NHAU giữa chúng mới là kết luận:
    #   · `/rate_limit` — đường proxy CHO PHÉP
    #   · `/repos/<kho>` — đường VIỆC THẬT (đọc PR, issue, nội dung kho)
    # Đo 17-08-2026: đường một `mo`, đường hai `chan`. Nên câu đúng KHÔNG phải
    # "REST bị chặn" mà là "REST bị chặn ĐÚNG CHỖ làm việc", và đó mới là điều đáng
    # nói với người đọc.
    tt_chung, mt_chung, _ = _do_rest_github("https://api.github.com/rate_limit", token=tok)
    # CHẨN ĐOÁN, KHÔNG TÍNH vào kết luận "dùng được" — xem `_tinh_kha_dung` dưới.
    duong.append(("rest-chung", tt_chung == "mo", mt_chung))
    slug = None
    if ws:
        rc_u, url_o, _ = _git(ws, "remote", "get-url", "origin")
        if rc_u == 0:
            k = _RE_SLUG_GITHUB.search((url_o or "").strip())
            slug = k.group(1) if k else None
    if slug:
        tt_kho, mt_kho, ok_kho = _do_rest_github(
            f"https://api.github.com/repos/{slug}", token=tok)
        # `ok` ở đây là THAO TÁC THÀNH CÔNG, không phải "đường thông". Một 404 kho
        # riêng tư vẫn là `mo` (tới GitHub) nhưng KHÔNG làm được việc.
        duong.append(("rest-kho", ok_kho, mt_kho if ok_kho else f"{mt_kho} [{tt_kho}]"))
    else:
        # `None` chứ KHÔNG `False`: không đọc được slug là CHƯA ĐO ĐƯỢC, và chi tiết
        # đã tự khai thế — để cờ `False` thì `_nhan_duong` in `rest-kho=khong`, tức
        # nhãn nói NGƯỢC với chi tiết ngay cạnh nó. Người vá bản hoà từng lấy cớ "đổi
        # nó là đổi ngữ nghĩa một đường đang tính vào LAM_DUOC_VIEC" để không sửa;
        # cross-review lượt 7 bác đúng: `any(...)` coi `None` và `False` NHƯ NHAU nên
        # kết luận khả dụng KHÔNG đổi — cái cớ ấy quá rộng, và món nợ là có thật.
        duong.append(("rest-kho", None, "khong doc duoc slug origin -> KHONG DO DUOC"))

    # `gh` mà "đã xác thực" TRONG KHI `rest-kho` bị chặn là bẫy, không phải tin vui:
    # `gh auth status` hỏi `/user` (đường được phép, 200) nên nó tự nhận đăng nhập,
    # rồi MỌI lệnh việc thật (`gh pr view`, `gh api repos/...`) ăn 403. Một công cụ
    # qua được phép tự kiểm mà không làm nổi việc thì tệ hơn công cụ vắng mặt —
    # cùng họ `codex login status`. Nói thẳng ra đây thay vì để người đọc tự vấp.
    # `gh` LÀM ĐƯỢC VIỆC hay không phải đo bằng MỘT THAO TÁC MỨC KHO, không bằng
    # `gh auth status`. Chính phiên này đo được `auth status` hỏi `/user` — đường
    # proxy CHO PHÉP — nên nó xanh trong khi mọi lệnh việc thật 403. Đếm nó là
    # "đường mở" là lần THỨ BA cùng một hình dạng trong kho: trước là
    # `shutil.which("gh")`, rồi `rest-chung`, giờ tới `gh auth status`. Ba lần thì
    # sai nằm ở ĐỊNH NGHĨA, không ở từng bản vá — nên "làm được việc" từ đây neo
    # vào một thao tác kho ĐÃ THÀNH CÔNG, không neo vào probe.
    if shutil.which("gh") and slug:
        try:
            pk = subprocess.run(["gh", "api", f"repos/{slug}", "--jq", ".full_name"],
                                capture_output=True, text=True,
                                encoding="utf-8", errors="replace", env=mt,
                                stdin=subprocess.DEVNULL, timeout=PROBE_TIMEOUT_GIAY)
            duong.append(("gh-kho", pk.returncode == 0 and bool((pk.stdout or "").strip()),
                          "doc duoc kho" if pk.returncode == 0 else f"rc={pk.returncode}"))
        except (OSError, subprocess.SubprocessError) as e:
            duong.append(("gh-kho", False, type(e).__name__))
    elif shutil.which("gh"):
        duong.append(("gh-kho", False, "khong doc duoc slug origin"))

    # --- MCP: ĐƯỜNG KHO THẬT SỰ DÙNG, và tới bản này mới ĐO thay vì khai trong chú thích.
    # Hai bước tách bạch, vì chúng hỏng khác nhau và chữa khác nhau:
    #   `.mcp.json` chưa khai server  -> phiên agent KHÔNG có công cụ nào, bất kể máy có gì
    #   đã khai nhưng CLI báo xấu     -> hỏng THẬT, chữa được (`claude` rồi duyệt)
    canh_ep = ""
    co_khai, mt_mcp, ten_mcp, url_mcp = _doc_mcp_json(ws)
    if not co_khai:
        duong.append(("mcp-cli", False, mt_mcp))
        # KHÔNG suy "endpoint hỏng" từ "chưa khai server": ta không biết URL nào để hỏi.
        # Đó là CHƯA ĐO ĐƯỢC, và nhãn phải nói đúng thế.
        duong.append(("mcp-endpoint", None, "khong biet URL — .mcp.json chua khai server"))
    else:
        tt_mcp, mt_khoe = _suc_khoe_mcp_github(ten_mcp or "github", mt)
        # BA TRẠNG THÁI, và `khong_do_duoc` PHẢI đọc ra khác `hong` ở phần mô tả — cờ
        # bool không chở nổi `None != False`, nên chữ phải chở.
        # `None` cho "chưa đo được" — KHÔNG phải `False`. Xem chỗ kết xuất bên dưới.
        duong.append(("mcp-cli", None if tt_mcp == "khong_do_duoc" else tt_mcp == "khoe", mt_khoe))
        # ĐẦU KIA CỦA DÂY. Tách hẳn khỏi `mcp-cli` vì hai đường này HỎNG ĐỘC LẬP: CLI
        # chưa duyệt server mà endpoint vẫn trả 200 là ca ĐÃ ĐO ĐƯỢC, không phải giả định.
        tt_ep, mt_ep, ok_ep = _do_mcp_endpoint(url_mcp, token=tok)
        co_ep = None if tt_ep == "khong_do_duoc" else (tt_ep == "mo" and ok_ep)
        duong.append(("mcp-endpoint", co_ep, mt_ep))
        # LÝ DO PHẢI ĐI RA TỚI NGƯỜI ĐỌC, không chỉ nằm trong hàm. ĐO ĐƯỢC ngay ở lượt
        # đầu của PLAT-M4: chuỗi tóm tắt chỉ nối `ten=nhan`, nên 401 CÓ header GitHub
        # (endpoint sống, token sai) và 403 KHÔNG header (proxy chặn) in ra Y HỆT nhau
        # — `mcp-endpoint=khong`. Phân loại đúng ở trong mà kết xuất gộp ở ngoài thì
        # người đọc vẫn đi chữa nhầm chỗ, tức packet này chỉ chữa được nửa đường. Nối
        # thêm mô tả khi cờ KHÔNG phải `True`, đúng khuôn `canh` mà `gh` đã dùng dưới
        # đây; đường xanh thì không thêm chữ, để dòng thường vẫn ngắn.
        if co_ep is not True:
            canh_ep = f" · mcp-endpoint: {mt_ep}"

    gh_ok = next((ok for t, ok, _ in duong if t == "gh-cli"), False)
    kho_chan = any(t == "rest-kho" and not ok for t, ok, _ in duong)
    canh = " · gh BAO da xac thuc nhung duong kho bi chan -> dung lam duong viec" \
        if (gh_ok and kho_chan) else ""
    # CHỈ ĐƯỜNG LÀM ĐƯỢC VIỆC mới được tính vào `DUNG_DUOC`.
    #
    # `rest-chung` (`/rate_limit`) MỞ trên container này, nhưng nó không đọc nổi một
    # PR nào — đưa nó vào `any(...)` là dán nhãn "GitHub dùng được" cho một phiên
    # không làm nổi việc gì với GitHub. `t103` bắt đúng lỗi này khi tôi vừa thêm
    # đường ấy, và nó là ĐÚNG MỘT lớp với lỗi cũ mà chính `t103` sinh ra để chặn:
    # bản trước đếm `shutil.which("gh")` là một đường mở. Hai lần, hai cái tên khác
    # nhau, cùng một sai lầm — đếm SỰ CÓ MẶT của một đường thay vì KHẢ NĂNG của nó.
    # `gh-cli` ĐÃ BỊ LOẠI khỏi tập này (P1 cross-review PR "#143"): nó chỉ chứng
    # minh ĐÃ XÁC THỰC, không chứng minh làm được việc. `gh-kho` mới là thao tác thật.
    # `mcp-cli` VÀ `mcp-endpoint` CỐ Ý KHÔNG có mặt ở đây, và đây là chỗ dễ thêm nhầm
    # nhất. `mcp-endpoint` mới cám dỗ hơn cả — nó CÓ chạm tới máy chủ thật — nhưng một
    # lượt `initialize` chỉ chứng minh endpoint TRẢ LỜI, y hệt `rate_limit` chứng minh
    # REST trả lời mà không đọc nổi một PR nào. Phép đo MCP hỏi
    # CLI xem server đã được duyệt chưa — nó chứng minh một tiến trình `claude` MỚI
    # SINH sẽ thấy gì, KHÔNG chứng minh phiên nào đó gọi được `mcp__github__*`. Đưa
    # nó vào tập này là lặp đúng lớp lỗi mà chính tập này sinh ra để chặn (đếm SỰ CÓ
    # MẶT của một đường thay vì KHẢ NĂNG của nó — đã ba lần: `which("gh")`,
    # `rest-chung`, `gh auth status`). Bằng chứng đường cuối cùng cho MCP là PHIÊN gọi
    # được `mcp__github__get_me`, và không tiến trình con nào cấp được bằng chứng ấy.
    LAM_DUOC_VIEC = {"git", "gh-kho", "rest-kho"}
    return (("DUNG_DUOC" if any(ok for t, ok, _ in duong if t in LAM_DUOC_VIEC)
             else "CHUA_XAC_THUC"),
            " · ".join(f"{t}={_nhan_duong(ok)}" for t, ok, _ in duong) + canh + canh_ep)


_RE_NANG_LUC_HOOK = re.compile(r"^#\s*hook-nang-luc:\s*(.+)$", re.MULTILINE)
_RE_NANG_LUC_LAUNCHER = re.compile(r"^#\s*launcher-nang-luc:\s*(.+)$", re.MULTILINE)


def _nang_luc_hook(noi_dung: str) -> set:
    """Đọc tập tên năng lực hook khai trong `# hook-nang-luc: …`.

    Hook CŨ không có dòng này ⇒ trả tập RỖNG ⇒ thiếu MỌI năng lực của master. Đó đúng
    là điều cần nói về một nhánh packet rẽ từ base cũ, và là lý do không cần đánh số
    phiên bản: vắng mặt tự nó đã mang đủ nghĩa.
    """
    ra = set()
    for m in _RE_NANG_LUC_HOOK.finditer(noi_dung):
        ra.update(t for t in m.group(1).split() if t)
    return ra


def _do_hook_cu(ws: str | None) -> tuple[str, str]:
    """Hook phiên đang checkout có CŨ HƠN bản trên nhánh chính không?

    ĐÂY LÀ NGUYÊN NHÂN GỐC CỦA SỰ CỐ 15-08-2026, và nó không phải chuyện xác thực.

    `.claude/hooks/session-start.sh` trên `master` ĐÃ khôi phục `CODEX_AUTH_JSON`
    từ 14-08-2026, có bốn chốt viết cẩn thận, và `docs/GOI_AGENT_DA_NEN.md` mô tả
    đúng như vậy. Nhưng phiên hôm đó đứng trên NHÁNH PACKET, rẽ từ `base_sha` CŨ
    HƠN commit ấy — nên hook thật sự chạy là bản cũ, KHÔNG có khối khôi phục. Kết
    quả: `codex login status` nói `Not logged in`, tài liệu nói "hook lo rồi", và
    hai câu đó cùng đúng.

    `.claude/skills/work-packet/SKILL.md` cảnh báo sẵn: "`base_sha` thường cũ hơn
    công cụ trên nhánh chính, nên cây làm việc của packet có thể thiếu cả bộ dựng
    công cụ lẫn hook phiên". Cảnh báo bằng CHỮ không chặn được ai — nên nay đo bằng
    MÁY: so băm hook đang có với hook trên `origin/master`.

    ĐO THEO NĂNG LỰC, KHÔNG THEO BĂM TOÀN TỆP. Bản trước so `sha256` cả tệp và
    cross-review bác đúng: sửa một dấu phẩy trong chú thích cũng làm chốt đỏ, mà chốt
    đỏ vì lý do vô hại là chốt sẽ bị bỏ qua. Câu hỏi đúng không phải "hai tệp có khác
    nhau không" mà là **"bản đang chạy có THIẾU thứ gì không"**.

    Cũng KHÔNG dùng quan hệ tổ tiên commit — reviewer nêu thẳng và đúng: chính nhánh
    packet CŨ mới là thứ cần cảnh báo, mà nó LÀ tổ tiên hợp lệ của master. Tổ tiên tính
    không phân biệt được "cũ nhưng đủ" với "cũ và thiếu".

    Hợp đồng là dòng `# hook-nang-luc: <tên> <tên> …` trong chính hook. So TẬP TÊN:
    thiếu tên nào so với master thì báo đúng tên đó. Hook có THÊM năng lực so với master
    (nhánh mới hơn) KHÔNG phải lỗi.

    KHÔNG gọi mạng. `git show` đọc ref đã fetch; chưa có ref thì nói KHONG_DO_DUOC
    chứ không đoán — một chốt không đo được phải nói là không đo được.
    """
    if not ws:
        return ("KHONG_DO_DUOC", "khong xac dinh duoc workspace")
    duong = Path(ws) / ".claude" / "hooks" / "session-start.sh"
    if not duong.exists():
        return ("CHUA_XAC_THUC", "cay nay KHONG co .claude/hooks/session-start.sh")
    rc, ra, _ = _git(ws, "show", "origin/master:.claude/hooks/session-start.sh")
    if rc != 0 or not ra:
        return ("KHONG_DO_DUOC",
                "chua co origin/master trong cay nay — `git fetch origin master` roi do lai")
    cua_master = _nang_luc_hook(ra)
    if not cua_master:
        # Master chưa khai năng lực nào ⇒ không có gì để so. Nói thẳng là không đo
        # được, đừng tụt về so băm: tụt về sẽ dựng lại đúng cái chốt vừa bị bác.
        return ("KHONG_DO_DUOC",
                "hook tren origin/master chua co dong `# hook-nang-luc:` de doi chieu")
    dang_co = _nang_luc_hook(duong.read_text(encoding="utf-8", errors="replace"))
    thieu = sorted(cua_master - dang_co)
    if not thieu:
        them = sorted(dang_co - cua_master)
        return ("DUNG_DUOC", "du nang luc so voi master"
                + (f" (+{','.join(them)} moi hon)" if them else ""))
    return ("CHUA_XAC_THUC",
            f"hook dang checkout THIEU nang luc: {', '.join(thieu)} — nhanh nay ra tu "
            f"base cu hon; lay hook tu master truoc khi ket luan ve moi truong")


def _nang_luc_launcher(noi_dung: str) -> set:
    """Đọc tập tên năng lực launcher khai trong `# launcher-nang-luc: …`."""
    ra = set()
    for m in _RE_NANG_LUC_LAUNCHER.finditer(noi_dung):
        ra.update(t for t in m.group(1).split() if t)
    return ra


def _do_launcher_cu(ws: str | None) -> tuple[str, str]:
    """Chính `launcher.py` ĐANG CHẠY có cũ hơn bản trên nhánh chính không?

    Cùng lớp với `hook-phien`, và đã trả giá RIÊNG một lần (16-08-2026): một phiên chạy
    `launcher.py` từ cây đang checkout NHÁNH PACKET để gọi reviewer. Bản vá thêm
    `thoi_luong_giay`/`stdout_byte`/`stderr_byte` vào sổ vừa land trên master nhưng KHÔNG
    có trên nhánh ấy, nên sổ lượt chạy thiếu cả ba trường mà không báo gì. Người vận hành
    phải tự trừ `bat_dau_utc` với `ket_thuc_utc` mới phát hiện — đúng việc mà bản vá sinh
    ra để khỏi phải làm.

    Đo TỆP ĐANG CHẠY (`__file__`), không đo tệp trong workspace: hai thứ đó có thể khác
    nhau, và thứ quyết định hành vi là cái đang chạy. Đây cũng là khác biệt so với
    `hook-phien` — hook thì cây quyết định, launcher thì lời gọi quyết định.

    KHÔNG gọi mạng: `git show` đọc ref đã fetch. Chưa có ref thì nói KHONG_DO_DUOC chứ
    không đoán.
    """
    if not ws:
        return ("KHONG_DO_DUOC", "khong xac dinh duoc workspace")
    rc, ra, _ = _git(ws, "show", "origin/master:.claude/dev/launcher.py")
    if rc != 0 or not ra:
        return ("KHONG_DO_DUOC",
                "chua co origin/master trong cay nay — `git fetch origin master` roi do lai")
    cua_master = _nang_luc_launcher(ra)
    if not cua_master:
        return ("KHONG_DO_DUOC",
                "launcher tren origin/master chua co dong `# launcher-nang-luc:` de doi chieu")
    try:
        dang_chay = Path(__file__).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return ("KHONG_DO_DUOC", f"khong doc duoc chinh tep dang chay: {e}")
    dang_co = _nang_luc_launcher(dang_chay)
    thieu = sorted(cua_master - dang_co)
    if not thieu:
        them = sorted(dang_co - cua_master)
        return ("DUNG_DUOC", "du nang luc so voi master"
                + (f" (+{','.join(them)} moi hon)" if them else ""))
    return ("CHUA_XAC_THUC",
            f"launcher DANG CHAY thieu nang luc: {', '.join(thieu)} — ban nay ra tu base "
            f"cu hon master; ket qua/so luot chay co the THIEU TRUONG ma khong bao gi")


# --- M3: DẤU VẾT HOOK ĐÃ CHẠY ----------------------------------------------------
_CAC_DUONG_VET_HOOK = (Path(".claude/.packet_state/session-start.ran"), Path(".tl_state/session-start.ran"))
_HAN_DAU_VET_HOOK_GIAY = 12 * 3600


def _do_hook_da_chay(ws: str | None, bay_gio: float | None = None) -> tuple[str, str]:
    """Hook phiên đã CHẠY chưa (M3) — đo bằng dấu vết, VÀ đo cả ĐỘ TƯƠI của dấu vết."""
    if not ws:
        return ("KHONG_DO_DUOC", "khong xac dinh duoc workspace")
    duong = Path(ws) / ".claude" / "hooks" / "session-start.sh"
    if not duong.exists():
        return ("KHONG_DO_DUOC", "cay nay KHONG co .claude/hooks/session-start.sh")
    goc = Path(ws)
    bay_gio = time.time() if bay_gio is None else bay_gio
    for rel in _CAC_DUONG_VET_HOOK:
        tep = goc / rel
        if not tep.is_file():
            continue
        try:
            noi_dung = tep.read_text(encoding="utf-8", errors="replace").strip()
            tuoi = bay_gio - tep.stat().st_mtime
        except OSError as e:
            return ("KHONG_DO_DUOC", f"co dau vet {rel.as_posix()} nhung khong doc duoc: {e}")
        if tuoi > _HAN_DAU_VET_HOOK_GIAY:
            gio = int(tuoi // 3600)
            return ("KHONG_DO_DUOC", f"KHÔNG ĐO ĐƯỢC — dau vet {rel.as_posix()} CU {gio}h (> {_HAN_DAU_VET_HOOK_GIAY // 3600}h, ghi luc {noi_dung or '?'}): no chung minh hook TUNG chay, khong chung minh hook chay cho phien nay")
        truong = noi_dung.split()
        nhanh = " [bo qua theo thiet ke tren may cuc bo]" if len(truong) > 1 and truong[1] == "cuc_bo" else ""
        return ("DA_CHAY", f"ĐÃ CHẠY (dấu vết: {rel.as_posix()}" + (f" lúc {noi_dung}{nhanh})" if noi_dung else ")"))
    return ("CHUA_CHAY", "CHƯA CHẠY — hook chua chay lan nao trong cay nay (chua co dau vet)")


# --- M2: ĐO HAI BIẾN UTF-8 -------------------------------------------------------
def _do_bien_utf8(moi_truong: dict[str, str] | None = None) -> dict:
    """Đo hai biến môi trường UTF-8 (M2). Cảnh báo khi thiếu PYTHONUTF8 hoặc PYTHONIOENCODING."""
    mt = _env_da_chuan(moi_truong)
    u8, enc = mt.get("PYTHONUTF8"), mt.get("PYTHONIOENCODING")
    import locale
    try:
        ma_nen = locale.getpreferredencoding(False).lower()
    except Exception:
        ma_nen = "unknown"
    thieu = [f"PYTHONUTF8={u8 or '<chua dat>'}" for _ in [1] if u8 != "1"]
    if not enc or enc.lower() != "utf-8":
        thieu.append(f"PYTHONIOENCODING={enc or '<chua dat>'}")
    canh_bao = ((f"chua dat du hai bien UTF-8 ({', '.join(thieu)}) — nen dat PYTHONUTF8=1 va PYTHONIOENCODING=utf-8 de tranh loi doc ma charmap/cp1258 tren Windows") if thieu else None)
    return {"PYTHONUTF8": u8, "PYTHONIOENCODING": enc, "ma_nen": ma_nen,
            "nen_la_utf8": ma_nen in ("utf-8", "utf_8"), "canh_bao": canh_bao}


# --- M5: ĐO ĐƯỜNG DẪN KHO -------------------------------------------------------
def _kiem_tra_duong_dan_kho(ws: str | None) -> tuple[bool, str]:
    """Đo đường dẫn kho (M5): có dấu cách hoặc ký tự ngoài ASCII thì nêu ra."""
    if not ws:
        return False, ""
    duong = str(Path(ws).resolve())
    co_dau_cach = " " in duong
    co_ngoai_ascii = any(ord(c) > 127 for c in duong)
    if co_dau_cach or co_ngoai_ascii:
        loai = "dau cach va ky tu ngoai ASCII" if co_dau_cach and co_ngoai_ascii else "dau cach" if co_dau_cach else "ky tu ngoai ASCII"
        return True, f"duong dan kho chua {loai} ('{duong}'): 6 ca da biet se do (lop B: t35-t40 trong lease_publish_test)"
    return False, ""


KHA_NANG = [
    {"ten": "codex", "do": lambda ws, ks=False: _do_codex(ks),
     "vi_sao": "reviewer cross-provider (§8) — executor claude thi reviewer PHAI la codex",
     "khac_phuc": "launcher.py chuan-bi   (hoac: codex login --device-auth)"},
    {"ten": "claude", "do": lambda ws, ks=False: _do_claude(),
     "vi_sao": "executor va phien dieu phoi",
     "khac_phuc": "dat ANTHROPIC_API_KEY / dang nhap lai claude"},
    {"ten": "github", "do": lambda ws, ks=False: _do_github(ws, _MOI_TRUONG_DA_DOC),
     "vi_sao": "dang handoff/verdict, doc issue, day nhanh",
     "khac_phuc": "khai server `github` trong .mcp.json; neu `claude mcp get github` bao "
                  "Pending approval thi chay `claude` roi duyet; git + MCP la duong cua kho"},
    {"ten": "launcher-phien", "do": lambda ws, ks=False: _do_launcher_cu(ws),
     "vi_sao": "launcher dang chay cu hon master = so luot chay THIEU truong ma khong bao",
     "khac_phuc": "chay launcher tu cay da merge master, hoac merge master vao nhanh nay"},
    {"ten": "hook-phien", "do": lambda ws, ks=False: _do_hook_cu(ws),
     "vi_sao": "hook cu hon master = thieu chot ma master da co (nguyen nhan goc 15-08)",
     "khac_phuc": "git show origin/master:.claude/hooks/session-start.sh > <tep>  "
                  "roi chay no; hoac merge master vao nhanh nay"},
    {"ten": "hook-da-chay", "do": lambda ws, ks=False: _do_hook_da_chay(ws),
     "vi_sao": "hook phien da thuc su CHAY chua (M3) — do bang dau vet de lai, tach khoi hook-phien",
     "khac_phuc": "chay .claude/hooks/session-start.sh de thiet lap moi truong"},
    {"ten": "openai-llm", "do": lambda ws, ks=False: _do_openai_llm(_MOI_TRUONG_DA_DOC, ks),
     "vi_sao": "provider openai_api qua execution_surface llm_cli (§4, §5 ops/OPENAI_LLM_PROVIDER.md)",
     "khac_phuc": "pip install llm && export OPENAI_API_KEY=... (hoac llm keys set openai)"},
    {"ten": "antigravity", "do": lambda ws, ks=False: _do_antigravity(_MOI_TRUONG_DA_DOC),
     "vi_sao": "provider google_antigravity qua execution_surface antigravity (AG-T0-01B)",
     "khac_phuc": "cai agy CLI va chay `agy` (mo TUI de dang nhap)"},
]


def lenh_moi_truong(a) -> int:
    q = quet_bien_moi_truong()
    if a.json:
        print(json.dumps(q, ensure_ascii=False, indent=2))
        return MA_OK
    print(f"BIEN MOI TRUONG khop mau: {q['so_bien']}  "
          f"(chi in TEN · DO DAI · VAN TAY — KHONG bao gio in gia tri)")
    for b in q["bien"]:
        canh = "  <-- NGHI GIU CHO (trung gia tri voi bien khac)" if b["nghi_giu_cho"] else ""
        print(f"  {b['ten']:<40} {b['do_dai']:>6} ky tu  {b['nhom']:<8}{canh}")
    if q["nhom_trung_gia_tri"]:
        print("\nNHOM TRUNG GIA TRI — gan nhu chac chan la chuoi giu cho:")
        for ten_nhom, ds in q["nhom_trung_gia_tri"].items():
            print(f"  {ten_nhom}  {len(ds)} bien: {', '.join(ds)}")
        print("  DA DAT != DUNG DUOC. Dung ket luan tu mot bien co mat.")
    return MA_OK


def lenh_chuan_bi(a) -> int:
    ket = chuan_bi_xac_thuc(that_su=not a.thu_khan)
    if not ket:
        print("chuan-bi: khong co bien nao can dung ra dia (hien chi codex can)")
        return MA_OK
    xau = 0
    for k in ket:
        if k["ok"]:
            print(f"  ok    {k['ten']:<8} {k['cach']} -> {k['duong_dan']}")
        else:
            xau += 1
            print(f"  HONG  {k['ten']:<8} {k['cach']}", file=sys.stderr)
    return MA_CHUA_XAC_THUC if xau else MA_OK


# Nhãn DUY NHẤT được tính là ĐÃ CHỨNG MINH khả dụng. Danh sách TRẮNG, cố ý:
# thêm nhãn mới mà quên cập nhật ở đây thì nó rơi vào "chưa chứng minh" — sai về
# phía AN TOÀN. Danh sách ĐEN thì ngược lại, nhãn mới lọt thẳng thành "khả dụng",
# và đó đúng là cách `CO_CREDENTIAL` lọt qua ở lượt trước.
#
# `SAP_HET_HAN` KHÔNG có trong đây: nếu không chạy `--kiem-song` thì nó cũng chỉ là
# `CO_CREDENTIAL` kèm cảnh báo, và hạn lấy từ JWT KHÔNG xác thực chữ ký — lời khai đó
# đủ để HẠ nhãn (fail-closed), không đủ để NÂNG.
DA_CHUNG_MINH_KHA_DUNG = frozenset({"DUNG_DUOC"})


def _ma_doctor(thieu_bat_buoc, chua_xac_thuc, doi_kha_dung: bool,
               chua_chung_minh=()) -> int:
    """Mã thoát của `doctor`. Thiếu công cụ BẮT BUỘC luôn là 12.

    CHƯA XÁC THỰC chỉ thành mã 13 khi phía gọi ĐÒI (`--doi-kha-dung`). Mặc định
    vẫn 0, và đây là quyết định có lý do chứ không phải nhân nhượng:

    `doctor` là chốt "môi trường có đủ đồ nghề không", và nhiều phiên hợp lệ KHÔNG
    cần gọi agent nào — bắt chúng đỏ vì `codex` chưa đăng nhập là chặn nhầm. Nguy
    hơn: mục `hook-phien` đỏ trên gần như MỌI nhánh packet (nhánh rẽ từ base_sha cũ),
    nên để nó vào mã thoát mặc định thì hook phiên sẽ đỏ thường trực, và một chốt
    đỏ thường trực là chốt bị bỏ qua.

    Bản trước của tôi trả 13 vô điều kiện và làm đỏ `t53_doctor_bao_du_khi_du` —
    ca đó ghim đúng hợp đồng cũ. Nới hợp đồng của một lệnh đã có người gọi thì phải
    nới bằng CỜ, không nới ngầm.

    Thông tin vẫn LUÔN được in ra, kể cả khi mã thoát là 0 — biết là một chuyện,
    chặn là chuyện khác.
    """
    if thieu_bat_buoc:
        return MA_THIEU_CONG_CU
    # `--doi-kha-dung` FAIL-CLOSED: phía gọi đòi "khả dụng" thì "chưa chứng minh được"
    # phải chặn y như "đo được là hỏng". Chỉ mặc định (không có cờ) mới rộng lượng.
    if (chua_xac_thuc or chua_chung_minh) and doi_kha_dung:
        return MA_CHUA_XAC_THUC
    return MA_OK


# wp802 (Q2/Q3) — "BỊ CHE": bản TÊN TRẦN hỏng mà bản khác chạy được. Đo 17-10-2026: `doctor`
# rc=0 trỏ bản TỐT trong khi `rg --version` gõ trong shell rc=1. Chỉ công cụ agent gõ trần:
# KHÔNG `bash` (đầu PATH Windows là WSL), KHÔNG `python` (đã dò ba tên).
_AP_DUNG_BI_CHE = frozenset({"rg", "git"})


def lenh_doctor(a) -> int:
    _chuan_bi_va_bo_snapshot()
    # ĐỌC MÔI TRƯỜNG TRƯỚC MỌI PHÉP HỎI CÔNG CỤ — thứ tự này là nội dung, không
    # phải nếp code: kết luận "công cụ không dùng được" chỉ có nghĩa khi đã biết
    # nó xác thực bằng đường nào (bài học 15-08-2026).
    moi_truong, moi_truong_cong_khai = _doc_moi_truong()
    global _MOI_TRUONG_DA_DOC
    _MOI_TRUONG_DA_DOC = moi_truong
    _XAC_THUC_DA_DO.clear()        # lượt mới, bằng chứng mới — không đọc ảnh chụp cũ
    he = platform.system()
    ket = []
    thieu_bat_buoc = []
    chua_do_bat_buoc = []          # bắt buộc nhưng HẾT NGÂN SÁCH trước khi đo tới
    # Trần tổng cho cả vòng đo: `doctor` là thứ người ta chạy KHI đã nghi ngờ môi
    # trường, nên nó không được phép treo — mỗi probe có hạn riêng, và cả lượt có
    # hạn chung.
    het_han = time.monotonic() + _tran_doctor()
    for c in CONG_CU:
        thay = None
        co_mat_nhung_hong = None
        het_ngan_sach = None
        qua_han_probe = None
        xac_thuc_ok = None
        loi_xac_thuc = None
        xac_thuc_chua_do = None
        hong_dau = None            # bản TÊN TRẦN (shell gọi) đo được là hỏng
        ung_vien = _cac_duong_dan(c, moi_truong)
        # Bản tên trần giải ĐỘC LẬP rồi đặt LÊN ĐẦU — đo nó trước mọi bản dự phòng.
        tran = (_ten_tran_giai_ra(c["ung_vien"][0], moi_truong)
                if c["ten"] in _AP_DUNG_BI_CHE else None)
        if tran:
            ung_vien = [(c["ung_vien"][0], tran)] + [
                x for x in ung_vien
                if os.path.normcase(os.path.abspath(x[1])) != os.path.normcase(os.path.abspath(tran))]
        for ten_uv, d in ung_vien:
            con_lai = het_han - time.monotonic()
            if con_lai <= 0:
                # HẾT NGÂN SÁCH KHÔNG PHẢI "CÔNG CỤ HỎNG" — trạng thái thứ ba.
                # Bản trước ghi nó vào `co_mat_nhung_khong_chay_duoc`, tức dán đúng
                # cái nhãn sai mà đợt này đi sửa: người đọc sẽ đi cài lại một công cụ
                # chưa hề được đo. `None ≠ False`, và "chưa đo" ≠ "đo được là hỏng".
                het_ngan_sach = {"goi_bang": ten_uv, "duong_dan": d,
                                 "ly_do": "doctor het ngan sach truoc khi do toi day"}
                break
            chay_duoc, pb, qua_han = _phien_ban(d, env=moi_truong,
                                                timeout=min(PROBE_TIMEOUT_GIAY, con_lai))
            if not chay_duoc and qua_han:
                # v1.3.0 (#185 + phép đo 12→0) — nguồn chớp của `t53`; vá tất định.
                # Đo được (ops/NO_KY_THUAT.md): `doctor` thoát 12 rồi 0, cùng lệnh,
                # cùng máy, cách nhau hai phút — vì MỘT lượt `--version` hết hạn
                # dưới churn tiến trình bị đếm là THIẾU. Quá hạn phụ thuộc đồng hồ
                # tường nên mọi cách đếm nó là THIẾU đều không tất định. Hai lớp vá:
                #   1. retry MỘT lượt với hạn GẤP ĐÔI (chớp đã đo là khởi động nguội
                #      dưới tải — lặp cùng hạn là tung lại đồng xu, không phải đo lại);
                #   2. vẫn quá hạn ⇒ "CHƯA ĐO ĐƯỢC" (`chua_do_duoc`/`chua_do_bat_buoc`),
                #      KHÔNG rơi vào `thieu_bat_buoc` — cùng doctrine với nhánh hết
                #      ngân sách ngay trên: `None ≠ False`.
                # Hỏng THẬT (rc != 0, OSError, không in gì) vẫn là THIẾU như cũ —
                # nhánh này chỉ tách QUA_HAN, không nới cho công cụ hỏng.
                con_lai = het_han - time.monotonic()
                if con_lai > 0:
                    chay_duoc, pb2, qua_han = _phien_ban(
                        d, env=moi_truong,
                        timeout=min(2 * PROBE_TIMEOUT_GIAY, con_lai))
                    # Retry ĐẠT thì phien_ban là của lượt 2 — giữ thông điệp lỗi
                    # lượt 1 làm "phiên bản" là chép nhầm bệnh án vào tên thuốc
                    # (t130 bắt được đúng lỗi này ở bản nháp đầu).
                    pb = pb2 if chay_duoc else f"luot 1: {pb} · luot 2: {pb2}"
            if chay_duoc:
                thay = {"goi_bang": ten_uv, "duong_dan": d, "phien_ban": pb}
                break
            if qua_han:
                qua_han_probe = {"goi_bang": ten_uv, "duong_dan": d,
                                 "ly_do": f"probe --version QUA HAN, chua do duoc: {pb}"}
                continue
            co_mat_nhung_hong = {"goi_bang": ten_uv,
                                 "duong_dan": d, "loi": pb}
            if tran and d == tran:
                hong_dau = co_mat_nhung_hong
        # Quá hạn ở bản tên trần KHÔNG tính: chưa đo được không phải hỏng (`None ≠ False`).
        bi_che = None
        if thay is not None and hong_dau is not None:     # `tran` chỉ có trong phạm vi
            hd = hong_dau or {}
            bi_che = {"trang_thai": "BI_CHE", "ban_hong": hd.get("duong_dan"),
                      "loi": hd.get("loi"), "ban_tot": thay["duong_dan"],
                      "cach_chua": (f"dua thu muc {os.path.dirname(thay['duong_dan'])} len "
                                    f"TRUOC trong PATH, hoac go ban hong "
                                    f"{hd.get('duong_dan')}")}
        if thay is not None and c.get("xac_thuc"):
            con_lai = het_han - time.monotonic()
            if con_lai <= 0:
                # Cũng vậy: chưa đo được auth thì để `None`, đừng khai là SAI.
                xac_thuc_ok, loi_xac_thuc = None, "doctor het ngan sach"
                xac_thuc_chua_do = loi_xac_thuc
            else:
                xac_thuc_ok, loi_xac_thuc, xt_qua_han, xt_dau_ra = _xac_thuc_kem_dau_ra(
                    thay["duong_dan"], c["xac_thuc"], env=moi_truong,
                    timeout=min(PROBE_TIMEOUT_GIAY, con_lai))
                xt_mo_ta_cuoi = loi_xac_thuc   # mô tả của LƯỢT CUỐI, không ghép chuỗi retry
                if not xac_thuc_ok and xt_qua_han:
                    # ĐƯỜNG CHỚP THỨ HAI của `t53`, cùng cơ chế với probe `--version`
                    # ngay trên: probe auth cũng gọi CLI chậm, quá hạn từng rơi thẳng
                    # vào `xac_thuc_ok is False` ⇒ `thieu_bat_buoc` ⇒ thoát 12.
                    # Cùng hai lớp vá: retry hạn gấp đôi, rồi mới nhận là CHƯA ĐO ĐƯỢC.
                    con_lai = het_han - time.monotonic()
                    if con_lai > 0:
                        xac_thuc_ok, loi_2, xt_qua_han, xt_dau_ra = _xac_thuc_kem_dau_ra(
                            thay["duong_dan"], c["xac_thuc"], env=moi_truong,
                            timeout=min(2 * PROBE_TIMEOUT_GIAY, con_lai))
                        xt_mo_ta_cuoi = loi_2
                        if not xac_thuc_ok:
                            loi_xac_thuc = f"luot 1: {loi_xac_thuc} · luot 2: {loi_2}"
                    if not xac_thuc_ok and xt_qua_han:
                        # `None ≠ False`: quá hạn cả hai lượt là CHƯA ĐO ĐƯỢC,
                        # không phải "xác thực sai".
                        xac_thuc_ok = None
                        xac_thuc_chua_do = f"probe xac thuc QUA HAN, chua do duoc: {loi_xac_thuc}"
                        loi_xac_thuc = xac_thuc_chua_do
                # GHI LẠI KẾT QUẢ CUỐI (sau retry) cho khối `KHA_NANG` đọc — probe auth
                # chạy MỘT lần mỗi lượt `doctor`, xem chú thích ở `_XAC_THUC_DA_DO`.
                # Quá hạn cả hai lượt cũng ghi (ok=False, qua_han=True): phép đo sau
                # phải thấy "CHƯA ĐO ĐƯỢC" chứ không được tự chạy thêm lần ba.
                _XAC_THUC_DA_DO[(thay["duong_dan"], tuple(c["xac_thuc"]))] = (
                    xac_thuc_ok is True, xt_mo_ta_cuoi, bool(xt_qua_han), xt_dau_ra)
        cai = c["cai"].get(he) or c["cai"].get("*") or ""
        bb = _bat_buoc(c, moi_truong)
        muc = {"ten": c["ten"], "bat_buoc": bb, "co": thay is not None,
               "vi_sao": c["vi_sao"], "lenh_cai": cai, **(thay or {})}
        if not isinstance(c["bat_buoc"], bool):
            # In CẢ bản khai lẫn bản đã giải: người đọc phải thấy con số này do
            # NỀN quyết, kẻo lại tưởng bảng tự mâu thuẫn giữa hai máy.
            muc["bat_buoc_khai"] = dict(c["bat_buoc"])
        if c.get("xac_thuc"):
            muc["xac_thuc_ok"] = xac_thuc_ok
            # Ghi lý do cho CẢ `False` (đo được là sai) LẪN `None` có lý do (chưa đo
            # được vì hết ngân sách/quá hạn) — JSON của lượt hỏng là thứ đã hụt HAI
            # lần khi săn flake này, đừng để nó câm thêm lần nữa.
            if xac_thuc_ok is not True and loi_xac_thuc:
                muc["loi_xac_thuc"] = loi_xac_thuc
        if thay is None and co_mat_nhung_hong:
            muc["co_mat_nhung_khong_chay_duoc"] = co_mat_nhung_hong
        if bi_che:            # `co` GIỮ True: công cụ CÓ cài, chỉ bản tên trần hỏng
            muc["trang_thai"] = "BI_CHE"
            muc["bi_che"] = bi_che
        if thay is None and het_ngan_sach:
            muc["chua_do_duoc"] = het_ngan_sach
        if thay is None and qua_han_probe:
            muc["chua_do_duoc"] = qua_han_probe
        ket.append(muc)
        # HẾT NGÂN SÁCH KHÔNG PHẢI THIẾU CÔNG CỤ (P2 review "#143"). Lượt trước tôi
        # tách được cái NHÃN (`chua_do_duoc`) nhưng chưa tách cái QUYẾT ĐỊNH: mục ấy
        # vẫn rơi vào `thieu_bat_buoc` nên `doctor` vẫn trả 12 và vẫn nói "THIEU".
        # Đổi tên chỗ hỏng mà giữ nguyên kết luận thì chưa sửa gì. Chưa đo được thì
        # phải nói CHƯA ĐO ĐƯỢC — `None ≠ False`.
        # Từ v1.3.0, `qua_han_probe` và `xac_thuc_chua_do` đi CÙNG nhánh với hết
        # ngân sách: cả ba đều là "chưa đo được", và đây chính là chỗ từng biến
        # một lượt probe quá hạn thành `doctor` thoát 12 (nguồn chớp của `t53`).
        # Chỉ khi CÓ phép đo hoàn tất (hỏng thật / xác thực sai) mới được nói THIẾU.
        if bb and thay is None and (het_ngan_sach is not None
                                    or qua_han_probe is not None):
            chua_do_bat_buoc.append(c["ten"])
        elif bb and thay is not None and xac_thuc_chua_do is not None:
            chua_do_bat_buoc.append(c["ten"])
        elif bb and (thay is None or xac_thuc_ok is False or bi_che):
            thieu_bat_buoc.append(c["ten"])

    # --- KHẢ DỤNG, không chỉ CÓ MẶT.
    # `--version` chạy được KHÔNG chứng minh công cụ dùng được: `codex --version` in
    # số phiên bản ngon lành trong khi `codex` chưa có credential nào. Cả ngày
    # 15-08-2026 mất đúng vì khoảng cách giữa hai điều đó. Bảng `CONG_CU` ở trên đo
    # CÓ MẶT + CHẠY ĐƯỢC; khối này đo DÙNG ĐƯỢC.
    try:
        ws = tim_workspace(getattr(a, "workspace", None))
    except Chan:
        ws = None                       # doctor phải chạy được cả ngoài repo
    kha_nang, chua_xac_thuc, chua_chung_minh = [], [], []
    for k in KHA_NANG:
        # KHỐI NÀY CŨNG PHẢI TIÊU NGÂN SÁCH CHUNG (P2 review "#143"). Trước đây nó
        # chạy NGOÀI mọi trần: `doctor` có thể vượt xa hạn tổng vì các phép đo khả
        # dụng, mà chúng gọi `gh`/`codex`/`claude` — đúng loại lệnh chậm nhất. Một
        # trần chỉ phủ nửa lượt chạy thì không phải trần.
        # Hết ngân sách ở đây là KHÔNG ĐO ĐƯỢC, không phải "chưa xác thực": trạng
        # thái thứ ba, `None ≠ False`.
        if time.monotonic() >= het_han:
            kha_nang.append({"ten": k["ten"], "trang_thai": "KHONG_DO_DUOC",
                             "chi_tiet": "doctor het ngan sach truoc khi do toi day",
                             "vi_sao": k["vi_sao"], "khac_phuc": k.get("khac_phuc", "")})
            chua_chung_minh.append(k["ten"])
            continue
        try:
            tt, mo_ta = k["do"](ws, getattr(a, "kiem_song", False))
        except Exception as e:           # doctor KHÔNG được chết vì một phép đo
            tt, mo_ta = "KHONG_DO_DUOC", f"{type(e).__name__}"
        kha_nang.append({"ten": k["ten"], "trang_thai": tt, "chi_tiet": mo_ta,
                         "vi_sao": k["vi_sao"], "khac_phuc": k.get("khac_phuc", "")})
        if k["ten"] == "hook-da-chay" and tt == "DA_CHAY":
            pass
        elif tt in ("CHUA_XAC_THUC", "CAN_CHUAN_BI"):
            chua_xac_thuc.append(k["ten"])
        elif tt not in DA_CHUNG_MINH_KHA_DUNG:
            chua_chung_minh.append(k["ten"])
    # --- MODULE PYTHON. Đo bằng `find_spec`, KHÔNG bằng `import`: một module hỏng
    # nửa chừng sẽ ném ngay giữa `doctor`, mà `doctor` không được chết vì một phép đo.
    #
    # NÓI RÕ ĐO BẰNG INTERPRETER NÀO, và đây không phải chi tiết thừa: `doctor` chạy
    # bằng `sys.executable`, còn `ops/lease_publish_test.py` trong CI chạy bằng python
    # của runner, và `run` sinh con bằng interpreter mà LỆNH tự nêu. Ba cái đó có thể
    # là ba môi trường khác nhau. Khẳng định đúng chỉ là "python ĐANG CHẠY doctor có
    # thấy module này" — khai rộng hơn là dựng lại đúng lớp lỗi "có mặt ≠ dùng được".
    import importlib.util as _ilu
    mo_dun = []
    thieu_mo_dun_bat_buoc = []
    for m in MODULE_PY:
        try:
            spec = _ilu.find_spec(m["ten"])
        except (ImportError, ValueError, AttributeError):
            spec = None
        pb = ""
        if spec is not None:
            # Phiên bản là THÔNG TIN, không phải chốt: hai workflow ghim `PyYAML==6.0.3`
            # nên lệch bản ở máy dev là chuyện đáng BIẾT, chưa phải chuyện đáng CHẶN.
            try:
                pb = getattr(__import__(m["ten"]), "__version__", "") or ""
            except Exception:            # noqa: BLE001 - doctor khong duoc chet
                pb = "(nap duoc spec nhung import loi)"
        mo_dun.append({"ten": m["ten"], "goi_la": m["goi_la"], "co": spec is not None,
                       "bat_buoc": m["bat_buoc"], "phien_ban": pb, "vi_sao": m["vi_sao"],
                       "lenh_cai": m["cai"].get(he) or m["cai"].get("*") or "",
                       "do_bang_interpreter": sys.executable})
        if spec is None and m["bat_buoc"]:
            thieu_mo_dun_bat_buoc.append(m["goi_la"])
    thieu_bat_buoc = thieu_bat_buoc + thieu_mo_dun_bat_buoc

    bien = quet_bien_moi_truong()

    # Mã thoát tính MỘT LẦN cho cả hai dạng in — hai bản sao của cùng một lời gọi
    # là hai bản sẽ trôi lệch. `chua_do_bat_buoc` đi vào vế fail-closed của
    # `--doi-kha-dung`: mặc định "chưa đo được" không chặn (đúng nhánh hết ngân
    # sách đã chọn từ trước), nhưng phía gọi đã ĐÒI khả dụng thì một công cụ bắt
    # buộc CHƯA ĐO ĐƯỢC không được lặng lẽ tính là đủ — không nối thì bản vá
    # "quá hạn ≠ thiếu" tự mở một fail-open mới cho đúng chế độ nghiêm nhất.
    ma_thoat = _ma_doctor(thieu_bat_buoc, chua_xac_thuc,
                          getattr(a, "doi_kha_dung", False),
                          chua_chung_minh + chua_do_bat_buoc)

    if a.json:
        # `ok` GIU NGHIA CU: đủ công cụ BẮT BUỘC hay không. Bản trước tôi đổi nó
        # thành "đủ công cụ VÀ đã xác thực", làm `t53` đỏ — và đúng ra là phải đỏ:
        # đổi nghĩa một trường mà phía gọi đã đọc thì cũng là nới hợp đồng ngầm,
        # y như đổi mã thoát. Thông tin mới đi vào TRƯỜNG MỚI (`ok_kha_dung`).
        #
        # v1.35.86 (cross-review lượt 6, P1 `co-credential-van-duoc-coi-la-kha-dung`):
        # `ok_kha_dung` trước chỉ trừ `chua_xac_thuc`, mà danh sách đó KHÔNG chứa
        # `CO_CREDENTIAL`. Hệ quả: tầng ĐO đã thôi nâng nhãn, nhưng tầng TIÊU THỤ
        # nâng lại nguyên vẹn — `ok_kha_dung=true` cho đúng credential mà lệnh gọi
        # thật trả 401. Sửa một đầu mà để đầu kia y nguyên thì chưa sửa gì.
        b_u8 = _do_bien_utf8(moi_truong)
        co_nd, mo_ta_nd = _kiem_tra_duong_dan_kho(ws)
        _in_an_toan(json.dumps({"ok": not thieu_bat_buoc,
                                # `chua_do_bat_buoc` cũng phủ định `ok_kha_dung`:
                                # "khả dụng" là nhãn ĐÃ CHỨNG MINH, mà công cụ bắt
                                # buộc chưa đo được thì chưa chứng minh được gì —
                                # cùng lý do nó vào vế fail-closed của mã thoát.
                                "ok_kha_dung": not thieu_bat_buoc and not chua_xac_thuc
                                               and not chua_chung_minh
                                               and not chua_do_bat_buoc,
                                "he_dieu_hanh": he,
                                "python_dang_chay": sys.version.split()[0],
                                "moi_truong": moi_truong_cong_khai,
                                # Tách hẳn khỏi `thieu_bat_buoc`: "chưa đo được"
                                # không phải "đo được là thiếu".
                                "chua_do_bat_buoc": chua_do_bat_buoc,
                                "cong_cu": ket, "mo_dun_python": mo_dun,
                                "thieu_bat_buoc": thieu_bat_buoc,
                                "kha_nang": kha_nang, "chua_xac_thuc": chua_xac_thuc,
                                "chua_chung_minh": chua_chung_minh,
                                "bien_moi_truong": bien,
                                "bien_utf8": b_u8,
                                "duong_dan_nguy_hiem": mo_ta_nd if co_nd else None},
                               ensure_ascii=False, indent=2))
        return ma_thoat
    else:
        con_ong = _in_an_toan(
            f"he dieu hanh : {he}  |  python dang chay: {sys.version.split()[0]}")
        for c in ket:
            if not con_ong:
                break
            hong = c.get("co_mat_nhung_khong_chay_duoc")
            chua_do = c.get("chua_do_duoc")
            xac_thuc_chua_do = (c.get("xac_thuc_ok") is None
                                 and c.get("loi_xac_thuc"))
            ly_do_chua_do = ((chua_do or {}).get("ly_do")
                              or xac_thuc_chua_do)
            che = c.get("bi_che")
            dau = ("BI_CHE" if che else "CHUA_DO" if ly_do_chua_do else
                   ("co  " if c["co"] else ("HONG" if hong else
                                             ("THIEU" if c["bat_buoc"] else "khong"))))
            mo_ta = (ly_do_chua_do or
                     (c.get("phien_ban", "") if c["co"] else c["vi_sao"]))
            con_ong = _in_an_toan(f"  {dau:<8} {c['ten']:<8} {mo_ta}")
            if che and con_ong:
                con_ong = _in_an_toan(f"        ten tran `{c['ten']}` goi {che['ban_hong']} - KHONG chay duoc: "
                                      f"{che['loi']}\n        ban chay duoc: {che['ban_tot']}\n        cach chua: {che['cach_chua']}")
            if hong and con_ong:
                con_ong = _in_an_toan(
                    f"        co o {hong['duong_dan']} nhung KHONG chay duoc: {hong['loi']}")
            if not c["co"] and not ly_do_chua_do and con_ong:
                con_ong = _in_an_toan(f"        cai bang: {c['lenh_cai']}")
            if c.get("xac_thuc_ok") is False and con_ong:
                con_ong = _in_an_toan(
                    f"        xac thuc KHONG dung: {c.get('loi_xac_thuc', 'khong ro')}")
            elif xac_thuc_chua_do and con_ong:
                con_ong = _in_an_toan(
                    f"        xac thuc CHUA DO: {xac_thuc_chua_do}")
        # In NGAY SAU bảng công cụ vì cùng trả lời câu "đủ đồ chưa", chỉ khác tầng:
        # bảng trên là LỆNH trên PATH, bảng này là MODULE của interpreter đang chạy.
        if mo_dun:
            _in_an_toan(f"MODULE PYTHON (do bang {sys.executable}):")
            for m in mo_dun:
                dau = "co  " if m["co"] else ("THIEU" if m["bat_buoc"] else "khong")
                mo_ta = (m["phien_ban"] or "co") if m["co"] else m["vi_sao"]
                _in_an_toan(f"  {dau:<5} {m['goi_la']:<8} {mo_ta}")
                if not m["co"]:
                    _in_an_toan(f"        cai bang: {m['lenh_cai']}")
        _in_an_toan("KHA DUNG (co mat != dung duoc):")
        for k in kha_nang:
            _in_an_toan(f"  {k['trang_thai']:<14} {k['ten']:<8} {k['chi_tiet']}")
        # LUẬT ĐỌC BIẾN TRƯỚC KHI KẾT LUẬN: phần này in KỂ CẢ khi mọi thứ xanh, để
        # không ai báo "cong cu X khong dung duoc" mà chưa từng nhìn vào biến.
        _in_an_toan(f"BIEN MOI TRUONG khop mau: {bien['so_bien']} "
                    f"(xem day du: `launcher.py moi-truong`)")
        for vt, ds in bien["nhom_trung_gia_tri"].items():
            _in_an_toan(f"  NGHI GIU CHO  {vt}  {len(ds)} bien cung gia tri: "
                        f"{', '.join(ds)}")
        # M2: LUẬT ĐỌC BIẾN UTF-8 TRƯỚC KHI KẾT LUẬN — in KỂ CẢ khi mọi thứ xanh.
        b_u8 = _do_bien_utf8(moi_truong)
        _in_an_toan("BIEN UTF-8 (chong loi charmap/cp1258 tren Windows):")
        _in_an_toan(f"  PYTHONUTF8      : {b_u8['PYTHONUTF8'] or '<chua dat>'}")
        _in_an_toan(f"  PYTHONIOENCODING: {b_u8['PYTHONIOENCODING'] or '<chua dat>'}")
        if b_u8["canh_bao"]:
            _in_an_toan(f"  CANH BAO        : {b_u8['canh_bao']}")
        # M5: Đo đường dẫn kho (có dấu cách hoặc ký tự ngoài ASCII)
        co_nd, mo_ta_nd = _kiem_tra_duong_dan_kho(ws)
        if co_nd:
            _in_an_toan(f"  CANH BAO DUONG DAN: {mo_ta_nd}")
        if chua_do_bat_buoc:
            _in_an_toan("CHUA DO DUOC: "
                        + ", ".join(chua_do_bat_buoc))
        if thieu_bat_buoc:
            ds_che = {c["ten"] for c in ket if c.get("bi_che")}
            ket_luan = "THIEU " + ", ".join(
                f"{t} (BI_CHE: co cai, ban ten tran hong)" if t in ds_che else t
                for t in thieu_bat_buoc)
        elif chua_do_bat_buoc:
            ket_luan = "CHUA DO DUOC " + ", ".join(chua_do_bat_buoc)
        else:
            ket_luan = "DU CONG CU BAT BUOC"
        _in_an_toan("KET LUAN  : " + ket_luan)
        # Mỗi khả năng một cách chữa RIÊNG. Bản trước gợi ý `chuan-bi` cho MỌI mục —
        # sai với `hook-phien` (hook cũ không chữa bằng chuan-bi) và với `github`.
        # Một gợi ý sai còn tệ hơn không gợi ý: nó làm người đọc chạy nhầm rồi tin là
        # đã thử.
        for k in kha_nang:
            if k["trang_thai"] in ("CHUA_XAC_THUC", "CAN_CHUAN_BI") and k["khac_phuc"]:
                _in_an_toan(f"  CHUA DUNG DUOC {k['ten']:<11} -> {k['khac_phuc']}")
        # SAP_HET_HAN vẫn DÙNG ĐƯỢC nên KHÔNG vào mục trên và KHÔNG đổi mã thoát — nhưng
        # để nó lẫn giữa danh sách thì cảnh báo sớm thành vô dụng. In riêng, kèm cách chữa.
        for k in kha_nang:
            if k["trang_thai"] == "SAP_HET_HAN":
                _in_an_toan(f"  CANH BAO SOM   {k['ten']:<11} -> {k['khac_phuc']}")
                _in_an_toan(f"                 {k['chi_tiet']}")
        # "Chưa chứng minh" KHÁC "đo được là hỏng" — in riêng, đừng để người đọc
        # suy ra im lặng là xanh. Đây chính là khoảng cách đã đốt cả ngày 15-08.
        if chua_chung_minh:
            _in_an_toan("  CHUA CHUNG MINH KHA DUNG (co mat, chua ai goi that): "
                        + ", ".join(chua_chung_minh))
            # Đừng khuyên bật một cờ ĐANG bật: `--kiem-song` đã chạy mà vẫn chưa có
            # bằng chứng thì lời khuyên "chạy lại với --kiem-song" là gợi ý sai —
            # một gợi ý sai còn tệ hơn không gợi ý (đo 19-08-2026: chân trang này
            # in y nguyên trong một lượt ĐÃ truyền cờ, đẩy người đọc chạy lại vô ích).
            if getattr(a, "kiem_song", False):
                _in_an_toan("                 --kiem-song DA chay ma van chua co bang "
                            "chung — xem chi tiet tung muc o tren")
            else:
                _in_an_toan("                 chay lai voi --kiem-song de doi bang chung that")
    return ma_thoat


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
    cs = sub.add_parser("credential-status", help="chốt offline: có đang chờ snapshot mới không")
    cs.set_defaults(fn=lambda a: MA_CHUA_XAC_THUC if _cho_snapshot_hoac_chan() else 0)

    c = sub.add_parser("check", help="chi chay cac chot, khong goi gi")
    _them_chot(c)
    c.set_defaults(fn=lenh_check)

    r = sub.add_parser("run", help="chay cac chot roi goi lenh dat sau --")
    _them_chot(r)
    r.add_argument("--run-root", required=True)
    r.add_argument("--name", default="")
    r.add_argument("--attempt-state", help="state packet chứa neo của lượt đang mở")
    r.add_argument("--resume-checkpoint", help="checkpoint.json của công việc cần tiếp tục")
    r.add_argument("--expected-checkpoint-sha256", help="SHA-256 checkpoint đã lưu trước khi thay credential")
    r.add_argument("--void-reason", choices=("infrastructure", "permission"),
                   help="lý do được buộc nguyên khối vào run.json của lượt")
    r.add_argument("--giu-ban-chup", action="store_true",
                   help="giu prompt.snapshot sau khi con thoat (mac dinh XOA: no chua noi dung prompt)")
    r.add_argument("--bo-qua-probe", metavar="LY_DO",
                   help="cho run tiep khi probe hong; bat buoc ghi ly do vao run.json")
    r.add_argument("lenh", nargs=argparse.REMAINDER)
    r.set_defaults(fn=lenh_run)

    s = sub.add_parser("status", help="xem so luot chay")
    s.add_argument("--run-root", required=True)
    s.add_argument("--id", default=None, help="run_id day du hoac short_id")
    s.set_defaults(fn=lenh_status)

    d = sub.add_parser("doctor", help="kiem cong cu + KHA DUNG + bien (KHONG cai gi)")
    d.add_argument("--json", action="store_true")
    d.add_argument("--workspace", default=None)
    d.add_argument("--kiem-song", action="store_true",
                   help="GOI THAT de chung minh credential con dung duoc (ton quota/mang)")
    d.add_argument("--doi-kha-dung", action="store_true",
                   help="thoat 13 neu co cong cu CHUA DUNG DUOC (mac dinh: chi bao, van thoat 0)")
    d.set_defaults(fn=lenh_doctor)

    m = sub.add_parser("moi-truong",
                       help="quet bien moi truong theo MAU — ten/do dai/van tay, KHONG in gia tri")
    m.add_argument("--json", action="store_true")
    m.set_defaults(fn=lenh_moi_truong)

    cb = sub.add_parser("chuan-bi",
                        help="dung credential tu bien ra dia cho CLI can doc tu dia (codex)")
    cb.add_argument("--thu-khan", action="store_true", help="chi bao se lam gi, khong ghi")
    cb.set_defaults(fn=lenh_chuan_bi)

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
        if a.lenh_con not in ("run", "doctor", "chuan-bi"):
            os.environ.pop("CODEX_AUTH_JSON", None)
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
