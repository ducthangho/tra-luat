#!/usr/bin/env python3
"""Lấy credential codex TẤT ĐỊNH — device-auth trong container, ra base64 cho CODEX_AUTH_JSON.

VÌ SAO CÓ TỆP NÀY
-----------------
Quy trình cũ bắt người giữ kho phải: cài `codex` trên máy CÁ NHÂN → `codex login` →
`base64 -w0 ~/.codex/auth.json` → dán vào biến môi trường. Ba bước đó nằm ngoài container
nên không đo được, và bước base64 phải làm NGAY sau `login` vì refresh token XOAY VÒNG —
chạy `codex` thêm một lần ở máy cá nhân là chuỗi vừa chép đã chết.

Đo 2026-08-23: **device-auth CHẠY ĐƯỢC ngay trong container này**. Nên toàn bộ phần máy
làm được đã tự động hoá ở đây; phần duy nhất cần người là mở một URL và gõ một mã 10 ký tự.

BỐN SỰ THẬT ĐÃ ĐO — mỗi cái từng làm hỏng một lượt thử
-------------------------------------------------------
1. **`--device-auth` KHÔNG có trong `codex login --help`** (v0.149.0) nhưng VẪN được nhận.
   Đọc help rồi kết luận "phiên bản này không hỗ trợ" là kết luận SAI — đã suýt mắc.
2. **Không có TTY thì codex KHÔNG in gì cả.** Ba lượt thử đầu trông y hệt "treo": chạy 25s,
   45s, 150s, stdout RỖNG. Thật ra flow đã khởi động (log nội bộ ghi "starting device code
   login flow") nhưng đầu ra bị đệm KHỐI. Vì vậy tệp này spawn qua **pty**, không qua ống.
3. **`CODEX_HOME` phải TỒN TẠI trước.** Trỏ vào thư mục chưa có ⇒ codex thoát ngay với
   "Error loading configuration", rc=1 — và nếu bạn đang chờ một URL thì nó trông hệt như
   lượt (2). Hai bệnh khác nhau, cùng một triệu chứng.
4. **`curl https://auth.openai.com/` trả 403 nhưng đường KHÔNG bị chặn.** `CONNECT` trả
   `200 Connection Established`, còn 403 kèm `cf-mitigated: challenge` là Cloudflare chặn
   BOT — client thật của codex đi qua bình thường. Cùng bài học `api.githubcopilot.com`
   trong CLAUDE.md: **một công cụ thất bại chưa phải một đường bị chặn.**

CHỐT AN TOÀN
------------
* Mặc định chạy trong `CODEX_HOME` **TẠM**, không đụng `~/.codex` đang dùng được.
* Muốn cài đè bản đang có phải `--cai-de`, và nó **sao lưu trước**, không hỏi lại sau.
* base64 ghi ra tệp `0600`; **KHÔNG in giá trị** trừ khi có `--in-gia-tri`. Bí mật in ra
  màn hình là bí mật nằm lại trong nhật ký phiên, mà nhật ký sống lâu hơn phiên.
* Thành công CHỈ được công bố sau một **lời gọi codex THẬT** (`_kiem_song`). `codex login
  status` NÓI DỐI — nó chỉ kiểm tệp đọc được, rc=0 trong khi mọi lời gọi trả 401.
* **Giới hạn Windows:** stdlib thiếu `os.O_NOFOLLOW`, nên `_sao_luu` fail-closed: không
  đọc nguồn, không tạo `.bak`; không dựa vào check-then-use `is_symlink()`.

MÃ THOÁT (cùng quy ước `ops/cong_cu.py`)
    0  ĐẠT            việc xong VÀ đã chứng minh bằng lời gọi thật
    2  ĐỎ             chạy được nhưng kết quả sai/không xác thực được
    3  KHÔNG_ĐO_ĐƯỢC  thiếu công cụ, hết giờ, người dùng chưa hoàn tất — KHÔNG phải ĐẠT
    4  lỗi đối số
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import os
import re
import runpy
import select
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

DAT, DO, KHONG_DO_DUOC = "DAT", "DO", "KHONG_DO_DUOC"
RC = {DAT: 0, DO: 2, KHONG_DO_DUOC: 3}
RC_ARG = 4

# Mã thiết bị hết hạn sau 15 phút (codex tự in ra như vậy). Chờ lâu hơn là chờ một mã đã chết.
HAN_MAC_DINH_GIAY = 15 * 60
# Lời gọi kiểm sống phải rẻ và có đáp án BIẾT TRƯỚC — xem `_kiem_song`.
HAN_KIEM_SONG_GIAY = 120
DAU_HIEU_SONG = "TRALUAT-CRED-OK"

_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
# URL device: chốt theo TIỀN TỐ https, không khớp lỏng, để không nhặt nhầm chữ trong câu.
_URL = re.compile(r"https://\S*device\S*")
# Mã một lần: codex in dạng `8FY2-J8PNS`. Cho phép độ dài khác nhau vì đây là định dạng của
# BÊN KIA, ta không kiểm soát — nhưng vẫn đòi có gạch nối và toàn hoa/số để khỏi nhặt nhầm.
_MA = re.compile(r"\b([A-Z0-9]{3,6}-[A-Z0-9]{3,6})\b")


def _in(*a):
    print(*a, flush=True)


def _codex_home_hieu_luc() -> Path:
    raw = os.environ.get("CODEX_HOME", "")
    home = Path(raw).expanduser() if raw else Path.home() / ".codex"
    if not home.is_absolute() or ".." in home.parts:
        raise OSError("CODEX_HOME must be an absolute path without parent traversal")
    return home


def _repo_helpers():
    helper = Path(__file__).with_name("launcher.py")
    if not helper.is_file():
        raise OSError("missing repository credential storage helper")
    return runpy.run_path(str(helper))


def _sach(s: str) -> str:
    return _ANSI.sub("", s)


def doc_moc_device(text: str) -> tuple[str | None, str | None]:
    """Rút (url, mã) từ đầu ra codex. Trả None cho phần chưa thấy.

    Tách riêng khỏi phần I/O để test được mà KHÔNG cần mạng — phần lớn cách hỏng của
    lệnh này nằm ở đây chứ không ở chỗ gọi mạng.
    """
    t = _sach(text)
    u = _URL.search(t)
    m = _MA.search(t)
    return (u.group(0) if u else None, m.group(1) if m else None)


def _co_codex() -> str | None:
    return shutil.which("codex")


def _chay_device_auth(codex_home: Path, han_giay: int) -> tuple[bool, str]:
    """Chạy `codex login --device-auth` qua PTY, in URL+mã NGAY khi thấy.

    Trả (thành_công, toàn_bộ_đầu_ra). Không phán xét kết quả ở đây — việc phán xét
    dành cho `_kiem_song`, vì rc=0 của login KHÔNG chứng minh token dùng được.
    """
    import pty

    codex_home.mkdir(parents=True, exist_ok=True)  # sự thật (3): phải TỒN TẠI trước
    moi = dict(os.environ, CODEX_HOME=str(codex_home))
    moi.pop("CODEX_AUTH_JSON", None)
    chu, con = pty.openpty()  # sự thật (2): không có TTY thì codex im lặng hoàn toàn
    try:
        p = subprocess.Popen([_co_codex() or "codex", "login", "--device-auth"],
                             stdin=con, stdout=con, stderr=con, env=moi, close_fds=True)
    except OSError as e:
        os.close(chu); os.close(con)
        return (False, f"không chạy được codex: {type(e).__name__}: {e}")
    os.close(con)

    het = time.monotonic() + han_giay
    gom, da_in = "", False
    try:
        while True:
            if p.poll() is not None and not select.select([chu], [], [], 0)[0]:
                break
            if time.monotonic() > het:
                p.kill(); p.wait(timeout=10)
                return (False, gom + "\n[QUÁ HẠN chờ người dùng hoàn tất]")
            r, _, _ = select.select([chu], [], [], 1.0)
            if not r:
                continue
            try:
                mau = os.read(chu, 4096)
            except OSError:
                break
            if not mau:
                break
            gom += mau.decode("utf-8", "replace")
            if not da_in:
                url, ma = doc_moc_device(gom)
                if url and ma:
                    da_in = True
                    _in("")
                    _in("  ┌─ CẦN BẠN LÀM, MỘT LẦN, ~30 GIÂY ────────────────────────")
                    _in(f"  │  1. Mở:  {url}")
                    _in(f"  │  2. Nhập mã:  {ma}")
                    _in("  │     (mã hết hạn sau 15 phút — lấy lại bằng cách chạy lại)")
                    _in("  └──────────────────────────────────────────────────────────")
                    _in("")
                    _in("  đang chờ bạn hoàn tất trên trình duyệt…")
    finally:
        try: os.close(chu)
        except OSError: pass
        if p.poll() is None:
            p.kill(); p.wait(timeout=10)
    if not da_in:
        # Không thấy URL/mã ⇒ KHÔNG kết luận "codex hỏng". Đây đúng chỗ sự thật (2) và (3)
        # trông giống hệt nhau, nên trả nguyên đầu ra cho người đọc tự phân biệt.
        return (False, gom or "[codex không in gì — xem sự thật (2) và (3) ở đầu tệp]")
    return (p.returncode == 0, gom)


def _kiem_song(codex_home: Path) -> tuple[bool, str]:
    """BẰNG CHỨNG DƯƠNG: gọi codex thật và đòi đúng một chuỗi biết trước.

    KHÔNG dùng `codex login status` — nó chỉ kiểm tệp đọc được. Kho này đã trả giá HAI lần
    vì tin nó: một lần dán nhãn DÙNG_ĐƯỢC sai, một lần để một chốt bảo vệ đúng bản đã chết.
    Và không đòi mỗi `rc=0`: rc=0 kèm đầu ra RỖNG là ca đã có thật (r244).
    """
    lenh = _co_codex()
    if not lenh:
        return (False, "không có codex trên PATH")
    moi = dict(os.environ, CODEX_HOME=str(codex_home))
    moi.pop("CODEX_AUTH_JSON", None)
    try:
        with open(os.devnull) as rong:
            p = subprocess.run([lenh, "exec", "--skip-git-repo-check",
                                f"In ra dung mot tu: {DAU_HIEU_SONG}"],
                               stdin=rong, capture_output=True, text=True, env=moi, cwd=codex_home,
                               timeout=HAN_KIEM_SONG_GIAY, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return (False, f"quá hạn {HAN_KIEM_SONG_GIAY}s")
    except (OSError, subprocess.SubprocessError) as e:
        return (False, f"không chạy được: {type(e).__name__}")
    stdout, stderr = p.stdout or "", p.stderr or ""
    ra = stdout + stderr
    for dau in ("token_revoked", "refresh_token_invalidated", "401 unauthorized",
                "please log in again", "could not be refreshed"):
        if dau in ra.lower():
            return (False, f"credential BỊ TỪ CHỐI ({dau})")
    if p.returncode != 0:
        return (False, f"codex exec thoát rc={p.returncode}")
    # Chỉ stdout là câu trả lời. Stderr có thể echo chính prompt, vốn đã chứa dấu hiệu.
    if DAU_HIEU_SONG not in stdout:
        return (False, "rc=0 nhưng KHÔNG thấy dấu hiệu sống trong stdout")
    return (True, f"rc={p.returncode}, có {DAU_HIEU_SONG}")


def _gio_con_lai(auth: Path, document=None) -> float | None:
    """Số giờ còn lại của access_token, đọc `exp` trong JWT. None khi không đọc được.

    CHỈ rút trường thời gian; token KHÔNG bao giờ được trả ra hay in ra. `exp` lấy từ
    payload mà KHÔNG kiểm chữ ký — đủ để CẢNH BÁO SỚM (hạ nhãn), không đủ để khẳng
    định còn dùng được: khẳng định đó chỉ đến từ `_kiem_song`.
    """
    try:
        d = json.loads(auth.read_text(encoding="utf-8")) if document is None else document
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    if not isinstance(d, dict):
        return None
    tokens = d.get("tokens") or {}
    if not isinstance(tokens, dict):
        return None
    tok = tokens.get("access_token") or d.get("access_token")
    if not isinstance(tok, str) or tok.count(".") != 2:
        return None
    than = tok.split(".")[1]
    than += "=" * (-len(than) % 4)  # JWT bỏ padding base64url; thiếu nó là ném binascii.Error
    try:
        payload = json.loads(base64.urlsafe_b64decode(than))
    except (ValueError, TypeError):
        return None
    if not isinstance(payload, dict):
        return None
    exp = payload.get("exp")
    if isinstance(exp, bool) or not isinstance(exp, (int, float)):
        return None
    try:
        exp = float(exp)
    except (OverflowError, ValueError):
        return None
    if not math.isfinite(exp):
        return None
    return (exp - time.time()) / 3600.0


def _ghi_bi_mat(dich: Path, noi_dung: bytes) -> None:
    """Use repository storage for private atomic artifacts, including native ACLs."""
    dich = dich.absolute()
    with _repo_helpers()["_KhoCodex"](dich.parent, artifact=True) as store:
        store.write(dich.name, noi_dung, store.read(dich.name))


def _sao_luu(dich: Path) -> Path | None:
    """Sao lưu ra tên CHƯA TỒN TẠI — không bao giờ đè một bản sao lưu trước.

    Bản đầu đặt tên bằng `int(time.time())` và ca `t7` bắt ngay: hai lần sao lưu trong
    CÙNG một giây cho CÙNG một tên ⇒ bản thứ hai đè bản thứ nhất, tức là mất đúng thứ ta
    vừa hứa giữ. Cùng họ với va chạm `.pyc` theo (mtime GIÂY, kích thước) đã ghi ở đầu
    `codex_cred_test.py` — **giây là hạt quá thô để làm định danh**.
    Không chữa bằng đồng hồ mịn hơn (`time_ns` vẫn có thể trùng khi hệ thống lùi giờ);
    chữa bằng cách HỎI hệ tệp cho tới khi có tên trống.
    """
    if not hasattr(os, "O_NOFOLLOW"):
        raise OSError("từ chối sao lưu: nền thiếu os.O_NOFOLLOW")
    if dich.is_symlink():
        raise OSError(f"từ chối sao lưu qua symlink: {dich}")
    if not dich.is_file():
        return None
    goc = f"{dich.name}.bak-{int(time.time())}"
    i = 0
    while True:
        bak = dich.with_name(goc if i == 0 else f"{goc}.{i}")
        try:
            fd = os.open(bak, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_TRUNC, 0o600)
            break
        except FileExistsError:
            i += 1
    try:
        with os.fdopen(fd, "wb") as ra:
            # Chính lần MỞ nguồn mới là chốt use-time; guard đầu hàm bảo đảm cờ có thật,
            # nên getattr không bao giờ được phép suy biến thành mở trần.
            nguon_fd = os.open(dich, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            try:
                nguon = os.fdopen(nguon_fd, "rb")
            except Exception:
                os.close(nguon_fd)
                raise
            with nguon:
                shutil.copyfileobj(nguon, ra)
            ra.flush()
            os.fsync(ra.fileno())
        os.chmod(bak, 0o600)
        return bak
    except Exception:
        bak.unlink(missing_ok=True)
        raise


def soan_tep_dan(b64: str, luc_utc: str, gio_con: float | None) -> str:
    """Soạn tệp hướng dẫn dán — bản chiếu DUY NHẤT của chuỗi, để giao cho chủ kho.

    Tách khỏi I/O để test được. Lần đầu việc này làm BẰNG TAY sau khi lệnh chạy xong;
    làm tay thì lần sau người khác quên, nên nó thành một bước của chính lệnh.
    """
    han = f"{gio_con:.0f} giờ" if gio_con is not None else "không đọc được"
    return f"""# CODEX_AUTH_JSON — credential codex

Lấy lúc `{luc_utc}` bằng `python3 .claude/dev/codex_cred.py lay --cai-de`.
Đã chứng minh dùng được bằng một lời gọi `codex exec` THẬT (`rc=0`, có `{DAU_HIEU_SONG}`) —
KHÔNG phải bằng `codex login status` (lệnh đó nói dối), KHÔNG phải bằng `rc=0` suông.

`access_token` còn: **{han}** kể từ lúc lấy.

---

## Cách 1 — Environment settings (dùng được cho MỌI phiên sau)

* **Tên biến:** `CODEX_AUTH_JSON`
* **Giá trị:** đúng chuỗi dưới đây — MỘT dòng, không xuống dòng, không khoảng trắng thừa

```
{b64}
```

## Cách 2 — export trong shell (chỉ có tác dụng trong phiên shell đó)

```bash
export CODEX_AUTH_JSON={b64}
```

---

## Kiểm tra sau khi dán

```bash
python3 .claude/dev/launcher.py doctor --kiem-song    # phải thấy: DUNG_DUOC  codex
python3 .claude/dev/codex_cred.py kiem --kiem-song    # rc=0 và "có {DAU_HIEU_SONG}"
```

Đừng tin `codex login status`: nó chỉ kiểm tệp đọc được, trả `rc=0 "Logged in"` trong khi
mọi lời gọi thật trả 401. Kho này đã trả giá hai lần vì tin nó.

## Chuỗi này chết theo hai cách

1. **Refresh token XOAY VÒNG.** Chạy `codex login` ở máy khác bằng cùng tài khoản là chuỗi
   này vô hiệu ngay, kể cả khi nó vẫn nằm nguyên trong biến môi trường.
2. **Nó là ẢNH CHỤP**, không tự cập nhật.

Cần bản mới: `python3 .claude/dev/codex_cred.py lay --cai-de` — ~30 giây, chỉ cần mở một URL
và gõ một mã 10 ký tự.

## Bảo mật

Chuỗi này **tương đương mật khẩu tài khoản** cho mục đích codex. Đừng commit vào git, đừng
dán vào issue/PR/chat. **Dán xong thì xoá tệp này.**
"""


def cmd_lay(a) -> int:
    if not _co_codex():
        _in("KHÔNG_ĐO_ĐƯỢC: không có `codex` trên PATH — cài rồi chạy lại.")
        return RC[KHONG_DO_DUOC]

    tam_ctx = None if a.codex_home else tempfile.TemporaryDirectory(prefix="codex-cred-")
    tam = Path(a.codex_home).expanduser().absolute() if a.codex_home else Path(tam_ctx.name)
    try:
        # Reject export aliases before starting login, and revalidate at each write.
        ra = Path(a.ra).expanduser().absolute() if a.ra else Path(tempfile.gettempdir()) / "CODEX_AUTH_JSON.b64"
        dan = Path(a.tep_dan).expanduser().absolute() if a.tep_dan else ra.with_name("CODEX_AUTH_JSON_setup.md")
        protected = [tam.resolve(), _codex_home_hieu_luc().resolve()]
        outputs = [ra.resolve(), dan.resolve()]
        if outputs[0] == outputs[1] or any(p == h or h in p.parents for p in outputs for h in protected):
            raise OSError("Từ chối artifact trùng credential home hoặc trùng nhau")
        for output in (ra, dan):
            with _repo_helpers()["_KhoCodex"](output.parent, artifact=True) as out_store:
                out_store.read(output.name)
        a.ra, a.tep_dan = str(ra), str(dan)
        with _repo_helpers()["_KhoCodex"](tam, create=True) as store:
            if store.read() is not None:
                _in("ĐỎ: home device-auth phải trống; dùng một home tạm mới")
                return RC[DO]
            return _lay_trong_home(a, tam, store)
    finally:
        if tam_ctx is not None:
            tam_ctx.cleanup()


def _lay_trong_home(a, tam, store) -> int:
    _in(f"CODEX_HOME tạm: {tam}   (bản đang dùng ở ~/.codex KHÔNG bị đụng)")
    ok, dau_ra = _chay_device_auth(tam, a.han_giay)
    if not ok:
        _in("KHÔNG_ĐO_ĐƯỢC: chưa hoàn tất device-auth.")
        # Only the parsed URL/device code may be printed by the login runner.
        # Unclassified child output can contain credentials and is not a log.
        return RC[KHONG_DO_DUOC]

    auth = tam / "auth.json"
    if not auth.is_file():
        _in(f"ĐỎ: login báo xong nhưng không có {auth}")
        return RC[DO]

    _in("đã nhận credential — đang KIỂM SỐNG bằng một lời gọi codex thật…")
    song, vi_sao = _kiem_song(tam)
    if not song:
        _in(f"ĐỎ: credential mới KHÔNG dùng được — {vi_sao}")
        return RC[DO]
    _in(f"kiểm sống: {vi_sao}")

    auth_bytes = store.read()
    if auth_bytes is None:
        return RC[DO]
    document = _repo_helpers()["_doc_auth_bytes"](auth_bytes)
    b64 = base64.b64encode(auth_bytes).decode("ascii")
    ra = Path(a.ra) if a.ra else Path(tempfile.gettempdir()) / "CODEX_AUTH_JSON.b64"
    _ghi_bi_mat(ra, (b64 + "\n").encode("ascii"))

    if a.cai_de:
        that = _codex_home_hieu_luc() / "auth.json"
        helpers = _repo_helpers()
        helpers["_doc_auth_bytes"](auth_bytes)
        with helpers["_KhoCodex"](that.parent, create=True) as store:
            old = store.read()
            before = helpers["_moc_refresh"](helpers["_doc_auth_bytes"](old).get("last_refresh")) if old else None
            after = helpers["_moc_refresh"](document.get("last_refresh"))
            if before is not None and (after is None or after < before):
                _in("ĐỎ: từ chối hạ cấp credential đang có")
                return RC[DO]
            bak = None
            if old is not None:
                name = "auth.json.bak-" + str(time.time_ns())
                store.write(name, old, None)
                bak = that.parent / name
            store.write("auth.json", auth_bytes, old)
        _in(f"đã cài đè {that}" + (f" (sao lưu: {bak})" if bak else ""))

    # Tệp hướng dẫn dán: bước CUỐI của lệnh, không phải việc làm tay sau đó. Phiên nào
    # cũng phải giao được cùng một thứ cho chủ kho, nên nó thuộc về mã.
    gio_con = _gio_con_lai(auth, document=document)
    tep_dan = Path(a.tep_dan) if a.tep_dan else ra.with_name("CODEX_AUTH_JSON_setup.md")
    _ghi_bi_mat(tep_dan, soan_tep_dan(
        b64, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), gio_con).encode("utf-8"))

    _in("")
    _in("ĐẠT — credential mới, đã chứng minh bằng lời gọi thật.")
    _in(f"  base64 dài {len(b64)} ký tự, đã ghi với quyền riêng tư: {ra}")
    _in(f"  tệp hướng dẫn dán với quyền riêng tư: {tep_dan}")
    if gio_con is not None:
        _in(f"  access_token còn ~{gio_con:.0f} giờ")
    _in("  → GỬI TỆP TRÊN cho chủ kho (SendUserFile), đừng in chuỗi ra màn hình.")
    _in("")
    if a.in_gia_tri:
        _in("  ↓ GIÁ TRỊ để dán vào biến CODEX_AUTH_JSON ↓")
        _in(b64)
        _in("  ↑ GIÁ TRỊ ↑")
        _in("")
        _in("  LƯU Ý: chuỗi này tương đương mật khẩu tài khoản cho mục đích codex, và nó vừa")
        _in("  nằm lại trong nhật ký phiên. Đổi credential nếu nhật ký này đi ra ngoài.")
    else:
        _in("  KHÔNG in giá trị (mặc định). Muốn in ra để chép, chạy lại kèm --in-gia-tri,")
        _in(f"  hoặc tự đọc:   cat {ra}")
    _in("")
    _in("  Dán vào: Environment settings → biến CODEX_AUTH_JSON (cạnh GITHUB_PAT).")
    _in("  Chép NGAY: refresh token XOAY VÒNG — chạy codex ở nơi khác là chuỗi này chết.")
    return RC[DAT]


def cmd_kiem(a) -> int:
    """Đo credential ĐANG dùng: còn sống thật không, còn bao lâu."""
    try:
        home = Path(a.codex_home).expanduser() if a.codex_home else _codex_home_hieu_luc()
        auth = home / "auth.json"
        # wp484 g7 (P2 #509 thread XL-) — home hợp lệ nhưng CHƯA tạo cũng là "chưa có
        # credential", giống thư mục có mà thiếu auth.json; bản trước để `_KhoCodex` ném
        # FileNotFoundError rơi vào nhánh ĐỎ rc=2. `lexists`: symlink treo vẫn đi tiếp để
        # `_KhoCodex` từ chối như cũ — không nới đường an toàn.
        if not os.path.lexists(home):
            _in("KHÔNG_ĐO_ĐƯỢC: thư mục Codex home chưa tồn tại — chưa có credential")
            return RC[KHONG_DO_DUOC]
        helpers = _repo_helpers()
        with helpers["_KhoCodex"](home) as store:
            raw = store.read()
            if raw is None:
                _in("KHÔNG_ĐO_ĐƯỢC: không có auth.json")
                return RC[KHONG_DO_DUOC]
            d = helpers["_doc_auth_bytes"](raw)
    except (OSError, ValueError, UnicodeError):
        _in("ĐỎ: không đọc credential an toàn được")
        return RC[DO]
    if not isinstance(d, dict):
        _in(f"ĐỎ: {auth} không chứa JSON object")
        return RC[DO]
    # CHỈ đọc trường thời gian. Không in token, không trả token ra ngoài hàm.
    lr = helpers["_moc_refresh"](d.get("last_refresh"))
    _in(f"tệp        : {auth}")
    _in(f"last_refresh: {lr}")
    gio = _gio_con_lai(auth, document=d)
    if gio is not None:
        _in(f"access_token: còn ~{gio:.1f} giờ"
            + ("   ⚠ SẮP HẾT — chạy `lay --cai-de` để lấy bản mới" if gio < 48 else ""))
    if not a.kiem_song:
        _in("CHƯA CHỨNG MINH khả dụng — thêm --kiem-song để gọi thật (tốn quota).")
        return RC[KHONG_DO_DUOC]
    if helpers["_dang_cho_snapshot"](home):
        _in("CHỜ snapshot mới; không lặp credential đã thất bại")
        return RC[DO]
    song, vi_sao = _kiem_song(home)
    if not song and vi_sao.startswith("credential BỊ TỪ CHỐI ("):
        # wp484 g7 — cùng lỗi với `_do_codex_song` (P2 thread XMG), đường THỨ HAI reviewer không chỉ.
        if not helpers["_danh_dau_auth_hong"](home):
            vi_sao = (f"KHÔNG ghi được trạng thái chờ snapshot sau khi {vi_sao} — "
                      "CHẶN: sửa CODEX_HOME trước khi thử lại")
    _in(f"kiểm sống  : {vi_sao}")
    return RC[DAT] if song else RC[DO]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Lấy/kiểm credential codex tất định (device-auth trong container).")
    sub = p.add_subparsers(dest="lenh", required=True)

    q = sub.add_parser("lay", help="chạy device-auth rồi xuất base64 cho CODEX_AUTH_JSON")
    q.add_argument("--codex-home", help="thư mục tạm (mặc định tên ngẫu nhiên an toàn trong temp)")
    q.add_argument("--ra", help="tệp ghi base64 (mặc định /tmp/CODEX_AUTH_JSON.b64)")
    q.add_argument("--han-giay", type=int, default=HAN_MAC_DINH_GIAY,
                   help=f"hạn chờ người dùng (mặc định {HAN_MAC_DINH_GIAY}s = hạn của mã)")
    q.add_argument("--in-gia-tri", action="store_true",
                   help="IN base64 ra màn hình — bí mật sẽ nằm lại trong nhật ký phiên")
    q.add_argument("--tep-dan",
                   help="tệp .md hướng dẫn dán (mặc định cạnh --ra); GỬI tệp này cho chủ kho")
    q.add_argument("--cai-de", action="store_true",
                   help="cài đè ~/.codex/auth.json (có sao lưu) để dùng ngay trong phiên này")
    q.set_defaults(fn=cmd_lay)

    q = sub.add_parser("kiem", help="đo credential đang dùng")
    q.add_argument("--codex-home")
    q.add_argument("--kiem-song", action="store_true", help="gọi codex thật (tốn quota)")
    q.set_defaults(fn=cmd_kiem)
    return p


def main(argv=None) -> int:
    a = build_parser().parse_args(argv)
    try:
        return a.fn(a)
    except (OSError, ValueError, UnicodeError):
        _in("ĐỎ: không thao tác credential an toàn được; không xuất nội dung lỗi")
        return RC[DO]


if __name__ == "__main__":
    sys.exit(main())
