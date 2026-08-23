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
import os
import re
import select
import shutil
import subprocess
import sys
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
    try:
        with open(os.devnull) as rong:
            p = subprocess.run([lenh, "exec", "--skip-git-repo-check",
                                f"In ra dung mot tu: {DAU_HIEU_SONG}"],
                               stdin=rong, capture_output=True, text=True, env=moi,
                               timeout=HAN_KIEM_SONG_GIAY, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return (False, f"quá hạn {HAN_KIEM_SONG_GIAY}s")
    except (OSError, subprocess.SubprocessError) as e:
        return (False, f"không chạy được: {type(e).__name__}")
    ra = (p.stdout or "") + (p.stderr or "")
    for dau in ("token_revoked", "refresh_token_invalidated", "401 unauthorized",
                "please log in again", "could not be refreshed"):
        if dau in ra.lower():
            return (False, f"credential BỊ TỪ CHỐI ({dau})")
    if DAU_HIEU_SONG not in ra:
        return (False, f"rc={p.returncode} nhưng KHÔNG thấy dấu hiệu sống trong đầu ra")
    return (True, f"rc={p.returncode}, có {DAU_HIEU_SONG}")


def _sao_luu(dich: Path) -> Path | None:
    """Sao lưu ra tên CHƯA TỒN TẠI — không bao giờ đè một bản sao lưu trước.

    Bản đầu đặt tên bằng `int(time.time())` và ca `t7` bắt ngay: hai lần sao lưu trong
    CÙNG một giây cho CÙNG một tên ⇒ bản thứ hai đè bản thứ nhất, tức là mất đúng thứ ta
    vừa hứa giữ. Cùng họ với va chạm `.pyc` theo (mtime GIÂY, kích thước) đã ghi ở đầu
    `codex_cred_test.py` — **giây là hạt quá thô để làm định danh**.
    Không chữa bằng đồng hồ mịn hơn (`time_ns` vẫn có thể trùng khi hệ thống lùi giờ);
    chữa bằng cách HỎI hệ tệp cho tới khi có tên trống.
    """
    if not dich.is_file():
        return None
    goc = f"{dich.name}.bak-{int(time.time())}"
    bak = dich.with_name(goc)
    i = 0
    while bak.exists():
        i += 1
        bak = dich.with_name(f"{goc}.{i}")
    shutil.copy2(dich, bak)
    os.chmod(bak, 0o600)
    return bak


def cmd_lay(a) -> int:
    if not _co_codex():
        _in("KHÔNG_ĐO_ĐƯỢC: không có `codex` trên PATH — cài rồi chạy lại.")
        return RC[KHONG_DO_DUOC]

    tam = Path(a.codex_home) if a.codex_home else Path(f"/tmp/codex-cred-{os.getpid()}")
    _in(f"CODEX_HOME tạm: {tam}   (bản đang dùng ở ~/.codex KHÔNG bị đụng)")
    ok, dau_ra = _chay_device_auth(tam, a.han_giay)
    if not ok:
        _in("KHÔNG_ĐO_ĐƯỢC: chưa hoàn tất device-auth.")
        _in(_sach(dau_ra)[-1200:])
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

    b64 = base64.b64encode(auth.read_bytes()).decode("ascii")
    ra = Path(a.ra) if a.ra else Path("/tmp/CODEX_AUTH_JSON.b64")
    ra.write_text(b64 + "\n", encoding="ascii")
    os.chmod(ra, 0o600)

    if a.cai_de:
        that = Path(os.path.expanduser("~/.codex/auth.json"))
        that.parent.mkdir(parents=True, exist_ok=True)
        bak = _sao_luu(that)
        shutil.copy2(auth, that)
        os.chmod(that, 0o600)
        _in(f"đã cài đè {that}" + (f" (sao lưu: {bak})" if bak else ""))

    _in("")
    _in("ĐẠT — credential mới, đã chứng minh bằng lời gọi thật.")
    _in(f"  base64 dài {len(b64)} ký tự, đã ghi (chmod 600): {ra}")
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
    home = Path(a.codex_home) if a.codex_home else Path(os.path.expanduser("~/.codex"))
    auth = home / "auth.json"
    if not auth.is_file():
        _in(f"KHÔNG_ĐO_ĐƯỢC: không có {auth}")
        return RC[KHONG_DO_DUOC]
    try:
        d = json.loads(auth.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        _in(f"ĐỎ: {auth} không đọc được ({type(e).__name__})")
        return RC[DO]
    # CHỈ đọc trường thời gian. Không in token, không trả token ra ngoài hàm.
    lr = d.get("last_refresh")
    _in(f"tệp        : {auth}")
    _in(f"last_refresh: {lr}")
    if not a.kiem_song:
        _in("CHƯA CHỨNG MINH khả dụng — thêm --kiem-song để gọi thật (tốn quota).")
        return RC[KHONG_DO_DUOC]
    song, vi_sao = _kiem_song(home)
    _in(f"kiểm sống  : {vi_sao}")
    return RC[DAT] if song else RC[DO]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Lấy/kiểm credential codex tất định (device-auth trong container).")
    sub = p.add_subparsers(dest="lenh", required=True)

    q = sub.add_parser("lay", help="chạy device-auth rồi xuất base64 cho CODEX_AUTH_JSON")
    q.add_argument("--codex-home", help="thư mục tạm (mặc định /tmp/codex-cred-<pid>)")
    q.add_argument("--ra", help="tệp ghi base64 (mặc định /tmp/CODEX_AUTH_JSON.b64)")
    q.add_argument("--han-giay", type=int, default=HAN_MAC_DINH_GIAY,
                   help=f"hạn chờ người dùng (mặc định {HAN_MAC_DINH_GIAY}s = hạn của mã)")
    q.add_argument("--in-gia-tri", action="store_true",
                   help="IN base64 ra màn hình — bí mật sẽ nằm lại trong nhật ký phiên")
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
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
