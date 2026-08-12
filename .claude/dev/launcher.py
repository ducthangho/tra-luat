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
        p = subprocess.run(["git", "-C", str(workspace), *doi_so],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
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
                               capture_output=True, text=True)
            v = p.stdout.strip()
            return f"darwin:{v}" if v else None
        if he == "Windows":
            p = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command",
                 f"(Get-Process -Id {pid} -ErrorAction Stop).StartTime.Ticks"],
                capture_output=True, text=True)
            v = p.stdout.strip()
            return f"win:{v}" if v.isdigit() else None
    except (OSError, ValueError, IndexError):
        return None
    return None


def _con_song(pid: int) -> bool:
    """Tiến trình còn sống không. Dùng để KIỂM SAU khi giết, không đoán.

    ZOMBIE PHẢI TÍNH LÀ ĐÃ CHẾT. Con của chính ta, sau khi bị giết, nằm ở trạng
    thái Z cho tới khi được `wait` thu hồi — mà `os.kill(pid, 0)` với zombie vẫn
    THÀNH CÔNG. Bản đầu của hàm này quên điều đó nên báo "khong giet duoc" cho một
    tiến trình đã chết hẳn, và hạn chót trả 125 thay vì 124 (bắt được nhờ t27/t28
    đỏ ngay lượt chạy đầu — đúng việc của phản chứng).
    """
    if platform.system() == "Windows":
        return _khoa_danh_tinh(pid) is not None
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
        p = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)],
                           capture_output=True, text=True)
        return not p.stdout.strip().startswith("Z")
    return True


class KetGiet:
    """Kết quả giết, dạng CẤU TRÚC.

    ĐÃ TRẢ GIÁ (audit codex vòng 2): bản trước trả về một CHUỖI rồi hai chỗ gọi đi
    tìm substring "da tat". Nhánh dự phòng ghi "da tat (CON CHAU CO THE CON SONG)"
    — chứa đúng chuỗi đó — nên hạn chót trả 124 trong khi tiến trình CHÁU vẫn sống.
    Giao thức bằng chuỗi tự do là mời lỗi; nay ba sự thật tách bạch:
      me_da_chet  — đã xác nhận tiến trình mẹ biến mất
      ca_cay      — có bằng chứng CẢ CÂY đã chết (taskkill /T rc=0, hoặc killpg)
      mo_ta       — chỉ để người đọc, KHÔNG ai được quyết định dựa vào nó
    """

    def __init__(self, me_da_chet: bool, ca_cay: bool, mo_ta: str):
        self.me_da_chet = me_da_chet
        self.ca_cay = ca_cay
        self.mo_ta = mo_ta

    @property
    def tron_ven(self) -> bool:
        return self.me_da_chet and self.ca_cay

    def __str__(self) -> str:
        return self.mo_ta


def _giet_windows(pid: int) -> KetGiet:
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
    p = subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                       capture_output=True, text=True)
    buoc.append(f"taskkill rc={p.returncode}")
    # CHỈ taskkill rc=0 mới là bằng chứng CẢ CÂY. rc khác 0 nghĩa là /T không chạy,
    # nên dù mẹ có chết (do nhánh dưới) thì con cháu vẫn CHƯA được xác nhận.
    if p.returncode == 0 and not _con_song(pid):
        return KetGiet(True, True, "; ".join(buoc) + "; da tat ca cay")
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
    if _con_song(pid):
        return KetGiet(False, False, "; ".join(buoc) + "; KHONG GIET DUOC")
    buoc.append("me da tat NHUNG CON CHAU CHUA XAC NHAN (taskkill /T that bai)")
    return KetGiet(True, False, "; ".join(buoc))


def _giet_cay(pid: int, khoa: str | None) -> KetGiet:
    """Giết tiến trình VÀ con cháu. Trả KetGiet, KHÔNG trả chuỗi.

    Phía gọi quyết định mã thoát bằng `.tron_ven`, nên không còn cách nào để một
    câu mô tả nghe-như-thành-công lọt qua.
    """
    if khoa is None:
        return KetGiet(False, False, "tu choi giet: khong co khoa danh tinh")
    if _khoa_danh_tinh(pid) != khoa:
        return KetGiet(False, False, "tu choi giet: khoa danh tinh KHAC (PID da bi tai dung)")
    if platform.system() == "Windows":
        return _giet_windows(pid)
    # POSIX: con được sinh với start_new_session nên pgid == pid, giết cả nhóm
    try:
        os.killpg(pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError, OSError) as e:
        return KetGiet(False, False, f"killpg SIGTERM loi: {e}")
    for _ in range(20):  # 2 giây chờ tự chết tử tế
        time.sleep(0.1)
        # Hỏi _con_song chứ không killpg(0): nhóm tiến trình còn tồn tại chừng nào
        # zombie chưa được thu hồi, nên killpg(0) không phân biệt được sống/chết.
        if not _con_song(pid):
            # killpg giết theo NHÓM nên cả cây con cháu cùng nhóm đều nhận tín hiệu
            return KetGiet(True, True, "SIGTERM: da tat ca cay")
    try:
        os.killpg(pid, signal.SIGKILL)
    except OSError as e:
        return KetGiet(False, False, f"killpg SIGKILL loi: {e}")
    time.sleep(0.3)
    # KIỂM LẠI kể cả sau SIGKILL: tiến trình ở trạng thái D (chờ I/O) không chết
    # ngay, và báo "đã tắt" lúc nó còn sống là đúng thứ lỗi vừa bắt được ở Windows.
    if _con_song(pid):
        return KetGiet(False, False, "SIGKILL: KHONG GIET DUOC")
    return KetGiet(True, True, "SIGKILL: da tat ca cay")


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
    if len(doan_m) == 3:
        return t == m                      # host/owner/repo -> bằng nhau tuyệt đối
    if len(doan_m) != 2:
        return False                       # ngoài hai dạng đó = viết sai, KHÔNG đoán
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
    for _ in range(64):
        rid = uuid.uuid4().hex
        sid = rid[:8]
        da_co = {p.name.split("-", 1)[0] for p in run_root.iterdir() if p.is_dir()}
        if sid in da_co:
            continue
        thu_muc = run_root / f"{sid}-{rid}"
        try:
            # mkdir KHÔNG exist_ok = hành vi GIÀNH nguyên tử: hai tiến trình cùng
            # chọn trúng một id thì đúng một bên tạo được. "Quét rồi mkdir" của bản
            # trước có khe hở giữa hai bước (audit codex chỉ ra).
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
    """Tìm theo run_id đầy đủ HOẶC short_id."""
    if not run_root.is_dir():
        return None
    for p in sorted(run_root.iterdir()):
        if not p.is_dir():
            continue
        sid, _, rid = p.name.partition("-")
        if dinh_danh in (sid, rid, p.name):
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
    run_root = Path(a.run_root).expanduser()
    rid, sid = _cap_id(run_root)   # _cap_id đã TẠO thư mục (giành chỗ nguyên tử)
    thu_muc = run_root / f"{sid}-{rid}"

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
        ban_chup.write_bytes(b)
        ban_ghi["prompt_ban_chup"] = str(ban_chup)
        if any("{PROMPT_FILE}" in x for x in lenh_con):
            lenh_con = [x.replace("{PROMPT_FILE}", str(ban_chup)) for x in lenh_con]
            ban_ghi["prompt_kin_hoan_toan"] = True
        else:
            ban_ghi["prompt_kin_hoan_toan"] = False
        _ghi_so(thu_muc, ban_ghi)

    f_out = (thu_muc / "stdout.log").open("w", encoding="utf-8")
    f_err = (thu_muc / "stderr.log").open("w", encoding="utf-8")
    them = {}
    if platform.system() == "Windows":
        them["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
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

    khoa = _khoa_danh_tinh(p.pid)
    ban_ghi.update(pid=p.pid, khoa_danh_tinh=khoa)
    _ghi_so(thu_muc, ban_ghi)
    if not a.json:
        print(f"short_id  : {sid}")
        print(f"run_id    : {rid}")
        print(f"so        : {thu_muc}")

    han = _doc_iso(kq["deadline_utc"]) if kq["deadline_utc"] else None
    qua_han = False
    try:
        if han is None:
            ma = p.wait()
        else:
            con_lai = (han - _bay_gio()).total_seconds()
            try:
                ma = p.wait(timeout=max(0.0, con_lai))
            except subprocess.TimeoutExpired:
                qua_han = True
                ket_giet = _giet_cay(p.pid, khoa)
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
        ban_ghi["ly_do_dung"] = "bi ngat: " + _giet_cay(p.pid, khoa).mo_ta
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
        ban_ghi["trang_thai"] = "qua_han" if qua_han else "xong"
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
    run_root = Path(a.run_root).expanduser()
    if a.id:
        thu_muc = _tim_luot(run_root, a.id)
        if thu_muc is None:
            raise Chan(MA_THAM_SO, f"khong thay luot chay: {a.id}")
        so = _doc_so(thu_muc)
        if so is None:
            raise Chan(MA_THAM_SO, f"so luot chay hong: {thu_muc}")
        print(json.dumps(so, ensure_ascii=False, indent=2))
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
    print(json.dumps(ds, ensure_ascii=False, indent=2))
    return MA_THAM_SO if hong else MA_OK


def lenh_stop(a) -> int:
    run_root = Path(a.run_root).expanduser()
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
        print("KET LUAN  : TU CHOI - khong co khoa danh tinh, khong giet theo PID tran")
        return MA_DANH_TINH
    ket = _giet_cay(int(pid), khoa)
    so.update(trang_thai="da_dung", ly_do_dung=ket.mo_ta,
              giet_tron_ven=ket.tron_ven, ket_thuc_utc=_bay_gio().isoformat())
    _ghi_so(thu_muc, so)
    print(f"KET LUAN  : {ket.mo_ta}")
    return MA_OK if ket.tron_ven else MA_DANH_TINH


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
        print(json.dumps({"ok": not thieu_bat_buoc, "he_dieu_hanh": he,
                          "python_dang_chay": sys.version.split()[0],
                          "cong_cu": ket, "thieu_bat_buoc": thieu_bat_buoc},
                         ensure_ascii=False, indent=2))
    else:
        print(f"he dieu hanh : {he}  |  python dang chay: {sys.version.split()[0]}")
        for c in ket:
            hong = c.get("co_mat_nhung_khong_chay_duoc")
            dau = "co  " if c["co"] else ("HONG" if hong else
                                          ("THIEU" if c["bat_buoc"] else "khong"))
            mo_ta = c.get("phien_ban", "") if c["co"] else c["vi_sao"]
            print(f"  {dau:<5} {c['ten']:<8} {mo_ta}")
            if hong:
                print(f"        co o {hong['duong_dan']} nhung KHONG chay duoc: {hong['loi']}")
            if not c["co"]:
                print(f"        cai bang: {c['lenh_cai']}")
        print("KET LUAN  : " + ("DU CONG CU BAT BUOC" if not thieu_bat_buoc
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
        return a.fn(a)
    except Chan as e:
        print(f"CHAN [{e.ma}]: {e.thong_diep}", file=sys.stderr)
        return e.ma
    except BrokenPipeError:
        # Đầu ra bị cắt ống (`doctor | head`) không phải lỗi của ta. Bản trước đổ
        # nguyên traceback và thoát khác 0 — hook đọc mã đó rồi báo "THIEU CONG CU"
        # oan, làm hỏng cả lượt khởi động phiên. Đóng stdout tử tế rồi im lặng.
        try:
            sys.stdout.close()
        except OSError:
            pass
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno() if hasattr(sys.stdout, "fileno") else 1)
        return MA_OK


if __name__ == "__main__":
    sys.exit(main())
