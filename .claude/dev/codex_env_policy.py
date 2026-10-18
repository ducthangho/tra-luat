#!/usr/bin/env python3
"""PHÁT HIỆN khối `shell_environment_policy` mà hook phiên từng ghi vào config codex.

## Vì sao khối cũ phải biến mất (cross-review lượt 7, HIGH)

Khối đó đặt `inherit = "all"`, tức truyền TOÀN BỘ môi trường vào mọi lệnh con của codex,
chỉ loại bốn tên quan sát được trên MỘT máy tại MỘT thời điểm. Lý lẽ bảo vệ nó — "phiên
codex cần thấy `CODEX_AUTH_JSON` để tự tái dựng credential" — sai ngay trong luồng hook:
credential ĐÃ được ghi ra `~/.codex/auth.json` TRƯỚC khi khối policy chạy. Ta đổi MỘT
credential lấy CẢ MÔI TRƯỜNG mà không mua được gì. Đường đúng: `codex login --device-auth`.

## Vì sao tệp này KHÔNG CÒN TỰ GHI VÀO CONFIG (quyết định 16-08-2026)

Bốn lượt cross-review liên tiếp, BẢY phát hiện, TẤT CẢ cùng một đường — việc TỰ ĐỘNG ghi
lại config của người dùng:

    lượt 7   bảng TOML trùng tên ⇒ codex không parse được
    lượt 8   khớp marker bằng substring ⇒ MẤT DỮ LIỆU · `write_text` không nguyên tử
    lượt 9   kiểm từng dòng ⇒ VẪN mất dữ liệu · symlink tên tạm ⇒ ghi đè tệp khác
    lượt 10  CRLF ⇒ đổi kết thúc dòng toàn tệp · lost-update giữa lúc đọc và lúc thay

Mỗi lượt vá bảo toàn được thứ ta NGHĨ TỚI và làm hỏng thứ ta KHÔNG NGHĨ TỚI. Bảy lần theo
đúng một hình dạng thì vấn đề không nằm ở các bản vá — nó nằm ở QUYẾT ĐỊNH GỐC. Và phần
thưởng của cả đường ấy rất nhỏ: gỡ một khối mà chính ta đã thêm vào.

Nên: **tệp này không bao giờ ghi vào config của người dùng nữa.**

    mặc định   CHỈ ĐỌC. Phát hiện khối, đặt/gỡ CỜ CHẶN, in cách chữa. Không ghi config.
    `--go`     Dựng bản ĐÃ GỠ ra một tệp BÊN CẠNH để người dùng xem rồi tự thay.
               Vẫn KHÔNG đụng bản gốc.

Cả lớp rủi ro trên biến mất theo kiến trúc chứ không theo bản vá: không ghi đè thì không
có lost-update, không có tệp cụt, không có symlink bị xuyên, không có metadata bị đổi lén.
Phần còn lại — quyết định thay tệp — là việc người dùng làm có chủ đích, trên tệp của họ.

Đọc/ghi bằng BYTE, không qua universal-newline: `Path.read_text` đổi CRLF thành `\\n`
trước cả khi ta nhìn, nên chỉ cần ghi ra là toàn bộ phần của người dùng đổi kết thúc dòng
(lượt 10). Làm việc trên byte thì phần ngoài khối ra đúng từng byte như nó vào.

Mã thoát:  0 = sạch (không có khối, hoặc đã dựng xong bản đã gỡ)
           2 = sai tham số
           3 = CÒN KHỐI NGUY HIỂM hoặc KHÔNG PHÂN LOẠI ĐƯỢC ⇒ cờ chặn được đặt
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

MOC_MO = b"# >>> tra-luat: shell_environment_policy (quan ly tu dong) >>>"
MOC_DONG = b"# <<< tra-luat <<<"
BOM = b"\xef\xbb\xbf"

# Cờ CHẶN codex, đặt CẠNH config chứ không PHẢI TRONG config — ta không sửa tệp của
# người dùng, nên chặn cũng không được sửa vào đó.
TEN_CO_CHAN = "tra-luat-CHAN-CODEX"

# Đuôi của bản ĐÃ GỠ. Tệp MỚI, cạnh bản gốc; người dùng xem rồi tự `mv`.
DUOI_DA_GO = ".tra-luat-da-go"

MA_OK, MA_THAM_SO, MA_CON_KHOI = 0, 2, 3

# Nguyên văn THÂN khối mà hook từng ghi (lấy từ `c7bbd81`). Bản DUY NHẤT từng được ghi;
# thêm biến thể thì THÊM vào tuple, đừng nới luật so sánh.
#
# So NGUYÊN KHỐI, không kiểm từng dòng: lượt 9 đưa ba phản chứng cho thấy kiểm membership
# từng dòng không thấy CẤU TRÚC — `inherit = "core"`, một dòng chú thích đơn độc, và cả
# thứ tự đảo ngược đều bị nhận là "khối của ta".
_THAN_KHOI_CU = (
    b'[shell_environment_policy]\n'
    b'inherit = "all"\n'
    b'exclude = [\n'
    b'  "GITHUB_PAT",                                 # credential THAT, khong khop mau mac dinh\n'
    b'  "CLAUDE_CODE_SESSION_ID",                     # danh tinh phien, codex khong can\n'
    b'  "CLAUDE_CODE_REMOTE_SESSION_ID",\n'
    b'  "CLAUDE_CODE_WEBSOCKET_AUTH_FILE_DESCRIPTOR",\n'
    b']',
)

# Ba kết luận, ba mức bằng chứng khác nhau — đừng gộp.
SACH = "SACH"                      # đã chứng minh KHÔNG có khối của ta
CON_KHOI = "CON_KHOI"              # đã chứng minh CÒN khối canonical
KHONG_PHAN_LOAI = "KHONG_PHAN_LOAI"  # có dấu vết marker nhưng KHÔNG dám kết luận


def _in(s: str, loi: bool = False) -> None:
    # stdout/stderr ép UTF-8 TRƯỚC khi in: console máy Việt là cp1258, in đường dẫn có
    # dấu sẽ ném UnicodeEncodeError và giết cả lượt chạy trước khi logic kịp sai.
    for luong in (sys.stdout, sys.stderr):
        try:
            luong.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass
    print(s, file=sys.stderr if loi else sys.stdout)


def _goc_dong(d: bytes) -> bytes:
    """Dòng đã bỏ BOM, CR cuối và khoảng trắng hai bên — để SO SÁNH, không để ghi lại."""
    return d.lstrip(BOM).strip(b"\r\n").strip()


def _chuan_hoa(than: bytes) -> bytes:
    """Chuẩn hoá tối thiểu để so thân khối: bỏ CR, khoảng trắng cuối dòng, dòng trắng biên.

    Trình soạn thảo hay cắt khoảng trắng cuối và đổi kết thúc dòng; đó KHÔNG phải "người
    dùng sửa nội dung khối". Ngoài hai thứ đó thì không nới thêm gì.
    """
    return b"\n".join(d.rstrip() for d in than.replace(b"\r\n", b"\n").strip(b"\n").split(b"\n"))


def phan_loai(noi_dung: bytes) -> tuple[str, bytes | None, str]:
    """Trả `(ket_luan, noi_dung_da_go, ly_do)`. `noi_dung_da_go` chỉ có khi `CON_KHOI`.

    KHÔNG ghi gì — hàm này thuần tuý phân loại. Việc dựng bản đã gỡ nằm luôn ở đây vì nó
    chỉ là phép cắt trên byte, nhưng ai ghi nó ra đĩa là chuyện của `main`.
    """
    # BOM ĐẦU TỆP tách ra rồi gắn lại: khối cũ được ghi ở ĐẦU tệp, nên dòng marker mở
    # chính là dòng mang BOM — cắt dòng đó là mất BOM, tức lại sửa thứ ngoài phạm vi
    # (đúng họ lỗi CRLF ở lượt 10). Reviewer lượt 10 ghi BOM đang bị "từ chối oan";
    # nay nhận, và giữ nguyên.
    bom = BOM if noi_dung.startswith(BOM) else b""
    noi_dung = noi_dung[len(bom):]
    dong = noi_dung.splitlines(keepends=True)
    vt_mo = [i for i, d in enumerate(dong) if _goc_dong(d) == MOC_MO]
    vt_dong = [i for i, d in enumerate(dong) if _goc_dong(d) == MOC_DONG]
    # Marker LỌT giữa dòng khác: không nhận là marker, nhưng cũng KHÔNG lờ đi — đó là
    # dấu hiệu tệp đã bị sửa tay, hoặc bị bản cũ (khớp substring) cắt hỏng.
    le_loi = (noi_dung.count(MOC_MO) != len(vt_mo)
              or noi_dung.count(MOC_DONG) != len(vt_dong))
    if le_loi:
        return (KHONG_PHAN_LOAI, None,
                "marker xuat hien GIUA dong khac — tep da bi sua tay, KHONG doan")
    if not vt_mo and not vt_dong:
        return (SACH, None, "khong co khoi nao do ta quan ly")
    if len(vt_mo) != 1 or len(vt_dong) != 1:
        return (KHONG_PHAN_LOAI, None,
                f"marker khong thanh MOT cap (mo={len(vt_mo)}, dong={len(vt_dong)})")
    i_mo, i_dong = vt_mo[0], vt_dong[0]
    if i_dong < i_mo:
        return (KHONG_PHAN_LOAI, None, "marker DONG nam TRUOC marker MO")
    than = _chuan_hoa(b"".join(dong[i_mo + 1:i_dong]))
    if than not in tuple(_chuan_hoa(k) for k in _THAN_KHOI_CU):
        dau = than.split(b"\n")[0][:40].decode("utf-8", "replace") if than else ""
        return (KHONG_PHAN_LOAI, None,
                f"phan giua hai marker KHONG khop khoi canonical nao cua ta ({dau!r}...)")
    # Cắt đúng các dòng của khối, CỘNG NHIỀU NHẤT MỘT dòng trắng ngay sau — đúng dấu phân
    # cách mà bản ghi cũ chèn (`KHOI + "\n\n" + phan_con_lai`). Không `strip` cả tệp: dòng
    # trắng đầu/cuối là của người dùng.
    het = i_dong + 1
    if het < len(dong) and dong[het].strip() == b"":
        het += 1
    return (CON_KHOI, bom + b"".join(dong[:i_mo] + dong[het:]),
            "con khoi canonical cua ta")


def viet_ban_da_go(dich: Path, noi_dung: bytes) -> None:
    """Ghi bản đã gỡ ra một tệp MỚI. `O_EXCL`: đã tồn tại thì HỎNG, không ghi đè.

    Không `os.replace`, không đụng bản gốc — nên không có lost-update, không có tệp cụt,
    không có symlink bị xuyên, không có metadata bị đổi lén. Đó là cả bốn phát hiện của
    lượt 9-10, chết theo kiến trúc chứ không theo bản vá.
    """
    # `O_NOFOLLOW` KHONG co tren Windows — goi thang la `AttributeError`, ma `main`
    # chi bat `OSError`/`FileExistsError` nen no thoat ra ngoai va chan sach nguoi
    # dung Windows. `O_EXCL` mot minh da chan ghi de; `O_NOFOLLOW` la lop THEM.
    khong_theo_link = getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(str(dich), os.O_WRONLY | os.O_CREAT | os.O_EXCL | khong_theo_link, 0o600)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(noi_dung)
            f.flush()
            os.fsync(f.fileno())
    except BaseException:
        try:
            dich.unlink()
        except OSError:
            pass
        raise


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tep", default=None,
                   help="config codex; mac dinh <CODEX_HOME>/config.toml, fallback ~/.codex")
    p.add_argument("--go", action="store_true",
                   help="dung ban DA GO ra tep ben canh (VAN khong dung ban goc)")
    p.add_argument("--co-chan", default=None,
                   help="duong dan tep CO CHAN codex; mac dinh canh config")
    a = p.parse_args(argv)

    if a.tep is not None:
        tep = Path(os.path.expanduser(a.tep))
    else:
        raw = os.environ.get("CODEX_HOME", "")
        home = Path(raw).expanduser() if raw else Path.home() / ".codex"
        if not home.is_absolute() or ".." in home.parts:
            _in("codex env policy: CODEX_HOME khong hop le — CHAN", loi=True)
            return MA_CON_KHOI
        tep = home / "config.toml"
    co_chan = Path(os.path.expanduser(a.co_chan)) if a.co_chan else tep.with_name(TEN_CO_CHAN)

    def dat_co(ly_do: str) -> None:
        try:
            co_chan.write_text(
                "codex bi CHAN: config con khoi shell_environment_policy cu, hoac khong\n"
                "phan loai duoc.\n"
                f"ly do: {ly_do}\n"
                f"tep: {tep}\n"
                'Khoi `inherit = "all"` co the CON HIEU LUC — no truyen TOAN BO moi truong\n'
                "cho moi lenh con cua codex. Chua:\n"
                "  python3 .claude/dev/codex_env_policy.py --go   # dung ban da go ben canh\n"
                "roi xem va tu thay. Cong cu KHONG tu ghi vao config cua ban.\n",
                encoding="utf-8")
        except OSError as e:
            _in(f"codex env policy: KHONG dat duoc co chan ({e}) — CHAN CODEX BANG TAY",
                loi=True)

    def go_co() -> None:
        """Cờ phải TỰ HẾT khi sạch — cờ không tự hết là một chốt đỏ thường trực."""
        try:
            co_chan.unlink()
            _in("codex env policy: da go co chan codex")
        except OSError:
            pass

    if not tep.exists():
        _in("codex env policy: khong co config.toml — khong co gi de go")
        go_co()
        return MA_OK
    try:
        noi_dung = tep.read_bytes()
    except OSError as e:
        dat_co(f"KHONG doc duoc: {e}")
        _in(f"codex env policy: KHONG doc duoc {tep}: {e}", loi=True)
        return MA_CON_KHOI

    ket_luan, da_go, ly_do = phan_loai(noi_dung)

    if ket_luan == SACH:
        _in(f"codex env policy: {ly_do}")
        go_co()
        return MA_OK

    dat_co(ly_do)
    if ket_luan == KHONG_PHAN_LOAI:
        _in(f"codex env policy: KHONG PHAN LOAI DUOC — {ly_do} ({tep})", loi=True)
        _in("  => sua tay roi chay lai. Cong cu KHONG doan va KHONG ghi.", loi=True)
        return MA_CON_KHOI

    _in(f"codex env policy: CON KHOI `inherit=all` trong {tep}")
    if not a.go:
        _in(f"  => chay lai voi --go de dung ban da go ra {tep.name}{DUOI_DA_GO}")
        return MA_CON_KHOI
    dich = tep.with_name(tep.name + DUOI_DA_GO)
    try:
        viet_ban_da_go(dich, da_go)
    except FileExistsError:
        _in(f"codex env policy: {dich} DA TON TAI — xem/xoa no truoc, KHONG ghi de", loi=True)
        return MA_CON_KHOI
    except OSError as e:
        _in(f"codex env policy: KHONG ghi duoc {dich}: {e}", loi=True)
        return MA_CON_KHOI
    _in(f"  da dung ban da go: {dich}")
    _in(f"  xem thu:  diff {tep} {dich}")
    _in(f"  thay:     mv {dich} {tep}     # ban TU quyet dinh, cong cu khong lam ho")
    return MA_OK


if __name__ == "__main__":
    sys.exit(main())
