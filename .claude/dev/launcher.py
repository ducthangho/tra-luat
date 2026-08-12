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
  124 quá hạn trong lúc chạy (giống `timeout(1)`)
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


def _giet_cay(pid: int, khoa: str | None) -> str:
    """Giết tiến trình VÀ con cháu. Trả về chuỗi mô tả việc đã làm."""
    if khoa is None:
        return "tu choi giet: khong co khoa danh tinh"
    if False:
        return "tu choi giet: khoa danh tinh KHAC (PID da bi tai dung)"
    he = platform.system()
    if he == "Windows":
        p = subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                           capture_output=True, text=True)
        return f"taskkill rc={p.returncode}"
    # POSIX: con được sinh với start_new_session nên pgid == pid, giết cả nhóm
    try:
        os.killpg(pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError, OSError) as e:
        return f"killpg SIGTERM loi: {e}"
    for _ in range(20):  # 2 giây chờ tự chết tử tế
        time.sleep(0.1)
        try:
            os.killpg(pid, 0)
        except (ProcessLookupError, OSError):
            return "SIGTERM: da tat"
    try:
        os.killpg(pid, signal.SIGKILL)
    except OSError as e:
        return f"killpg SIGKILL loi: {e}"
    return "SIGKILL: da tat"


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
        # cho phép viết 'owner/repo' hoặc đầy đủ 'host/owner/repo'
        khop = any(r == can or r.endswith("/" + can) for r in remotes)
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
    run_root.mkdir(parents=True, exist_ok=True)
    da_co = {p.name for p in run_root.iterdir() if p.is_dir()}
    ngan_da_co = {t.split("-", 1)[0] for t in da_co}
    for _ in range(64):
        rid = uuid.uuid4().hex
        sid = rid[:8]
        if sid not in ngan_da_co and f"{sid}-{rid}" not in da_co:
            return rid, sid
    raise Chan(MA_VA_CHAM, "khong cap duoc short_id khong trung sau 64 lan thu")


def _ghi_so(thu_muc: Path, ban_ghi: dict) -> None:
    """Ghi sổ NGUYÊN TỬ: ghi tệp tạm rồi đổi tên.

    Người đọc có thể là phiên khác / điện thoại đang poll; đọc trúng lúc ghi dở sẽ
    thấy JSON cụt. os.replace là nguyên tử trên cả POSIX lẫn Windows.
    """
    thu_muc.mkdir(parents=True, exist_ok=True)
    tam = thu_muc / "run.json.tmp"
    tam.write_text(json.dumps(ban_ghi, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tam, thu_muc / "run.json")


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
    rid, sid = _cap_id(run_root)
    thu_muc = run_root / f"{sid}-{rid}"
    thu_muc.mkdir(parents=True)

    ban_ghi = {
        "version": VERSION, "run_id": rid, "short_id": sid,
        "ten": a.name, "lenh": list(a.lenh), "trang_thai": "dang_chay",
        "bat_dau_utc": _bay_gio().isoformat(), "ket_thuc_utc": None,
        "ma_thoat": None, "ly_do_dung": None, "pid": None, "khoa_danh_tinh": None,
        **kq,
    }
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
        p = subprocess.Popen(list(a.lenh), cwd=kq["workspace"],
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
                ban_ghi["ly_do_dung"] = "qua han: " + _giet_cay(p.pid, khoa)
                ma = MA_QUA_HAN
                try:
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
    except KeyboardInterrupt:
        ban_ghi["ly_do_dung"] = "bi ngat: " + _giet_cay(p.pid, khoa)
        ma = 130
    finally:
        f_out.close()
        f_err.close()

    if khoa is None and qua_han:
        # không giết được vì không có khoá: nói thẳng, đừng báo "đã dừng"
        ma = MA_DANH_TINH

    ban_ghi.update(trang_thai=("qua_han" if qua_han else "xong"),
                   ket_thuc_utc=_bay_gio().isoformat(), ma_thoat=ma)
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
    if run_root.is_dir():
        for p in sorted(run_root.iterdir()):
            so = _doc_so(p) if p.is_dir() else None
            if so:
                ds.append({k: so.get(k) for k in
                           ("short_id", "ten", "trang_thai", "ma_thoat", "bat_dau_utc")})
    print(json.dumps(ds, ensure_ascii=False, indent=2))
    return MA_OK


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
    so.update(trang_thai="da_dung", ly_do_dung=ket, ket_thuc_utc=_bay_gio().isoformat())
    _ghi_so(thu_muc, so)
    print(f"KET LUAN  : {ket}")
    return MA_OK if "da tat" in ket or "rc=0" in ket else MA_DANH_TINH


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

    k = sub.add_parser("stop", help="dung mot luot chay (giet ca cay tien trinh)")
    k.add_argument("--run-root", required=True)
    k.add_argument("--id", required=True)
    k.set_defaults(fn=lenh_stop)
    return ap


def main(argv=None) -> int:
    a = build_parser().parse_args(argv)
    if getattr(a, "lenh", None) and a.lenh and a.lenh[0] == "--":
        a.lenh = a.lenh[1:]
    try:
        return a.fn(a)
    except Chan as e:
        print(f"CHAN [{e.ma}]: {e.thong_diep}", file=sys.stderr)
        return e.ma


if __name__ == "__main__":
    sys.exit(main())
