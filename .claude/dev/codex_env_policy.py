#!/usr/bin/env python3
"""THU HỒI khối `shell_environment_policy` mà hook phiên từng ghi vào config codex.

## Vì sao thu hồi (cross-review lượt 7, HIGH)

Khối cũ đặt `inherit = "all"`, tức truyền TOÀN BỘ môi trường vào mọi lệnh con của
codex, chỉ loại bốn tên quan sát được trên MỘT máy tại MỘT thời điểm. Lập luận bảo
vệ nó là "phiên codex cần thấy `CODEX_AUTH_JSON` để tự tái dựng credential".

Lập luận đó SAI ngay trong chính luồng hook: `CODEX_AUTH_JSON` đã được khôi phục ra
`~/.codex/auth.json` **TRƯỚC KHI** khối policy được ghi. Từ đó codex và mọi lệnh con
đọc credential từ tệp chuẩn, không cần biến. Và nếu hook không chạy thì policy cũng
không được cài — nên nó chưa bao giờ là đường cứu hộ độc lập. Ta đã đổi MỘT credential
lấy CẢ MÔI TRƯỜNG mà không mua được gì.

Danh sách `exclude` cũng không cứu được: quét theo TÊN không chứng minh được gì cho
`PGPASSWORD`, `DATABASE_URL`, `REDIS_URL`, `SSH_AUTH_SOCK`, hay biến vendor mới. Nó
lỗi thời đúng vào lúc môi trường đổi — và bên quên cập nhật chính là bên đẩy lọt.

## Vì sao KHÔNG viết đè, chỉ GỠ

Bản trước gỡ khối CÓ MARKER rồi LUÔN prepend một `[shell_environment_policy]`. Người
dùng đã có sẵn bảng cùng tên nhưng KHÔNG marker (cấu hình codex hoàn toàn hợp lệ) thì
tệp thành HAI bảng trùng tên và codex từ chối parse — ta làm hỏng config của họ.

Nay chỉ có đúng hai kết cục: gỡ ĐÚNG khối của mình, hoặc TỪ CHỐI kèm chẩn đoán. Không
đoán, không viết đè, không prepend. Marker hỏng một đầu là ca phải từ chối chứ không
phải ca để suy diễn — suy sai ở đây là xoá mất cấu hình người khác.

Mã thoát:  0 = xong (đã gỡ, hoặc không có gì để gỡ) · 2 = sai tham số
           3 = TỪ CHỐI kèm chẩn đoán, KHÔNG đụng tệp
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

MOC_MO = "# >>> tra-luat: shell_environment_policy (quan ly tu dong) >>>"
MOC_DONG = "# <<< tra-luat <<<"

MA_OK, MA_THAM_SO, MA_TU_CHOI = 0, 2, 3


def _in(s: str, loi: bool = False) -> None:
    # stdout/stderr ép UTF-8 TRƯỚC khi in: console máy Việt là cp1258, in đường dẫn
    # có dấu sẽ ném UnicodeEncodeError và giết cả lượt chạy trước khi logic kịp sai.
    for luong in (sys.stdout, sys.stderr):
        try:
            luong.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass
    print(s, file=sys.stderr if loi else sys.stdout)


def go_khoi(noi_dung: str) -> tuple[str | None, str]:
    """Trả `(noi_dung_moi, ly_do)`. `None` = TỪ CHỐI, `ly_do` giải thích.

    `noi_dung_moi == noi_dung` nghĩa là không có gì để gỡ.
    """
    so_mo, so_dong = noi_dung.count(MOC_MO), noi_dung.count(MOC_DONG)
    if so_mo == 0 and so_dong == 0:
        return noi_dung, "khong co khoi nao do ta quan ly"
    if so_mo != 1 or so_dong != 1:
        # Nhiều hơn một cặp = tệp đã bị chồng khối (đúng triệu chứng của bản prepend
        # cũ khi marker hỏng). Gỡ "cặp đầu tiên" là ĐOÁN; đoán sai thì xoá nhầm.
        return None, (f"marker khong thanh MOT cap (mo={so_mo}, dong={so_dong}) — "
                      f"KHONG doan, sua tay roi chay lai")
    dau = noi_dung.index(MOC_MO)
    cuoi = noi_dung.index(MOC_DONG)
    if cuoi < dau:
        return None, "marker DONG nam TRUOC marker MO — tep da bi sua tay, KHONG doan"
    moi = noi_dung[:dau] + noi_dung[cuoi + len(MOC_DONG):]
    # Dọn đúng phần trắng thừa do việc gỡ tạo ra, không đụng phần còn lại của tệp.
    moi = moi.strip("\n")
    return (moi + "\n" if moi else ""), "da go khoi cua ta"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tep", default="~/.codex/config.toml",
                   help="config codex; mac dinh ~/.codex/config.toml")
    p.add_argument("--thu-khan", action="store_true",
                   help="chi bao se lam gi, KHONG ghi")
    a = p.parse_args(argv)

    tep = Path(os.path.expanduser(a.tep))
    if not tep.exists():
        _in("codex env policy: khong co config.toml — khong co gi de go")
        return MA_OK
    try:
        cu = tep.read_text(encoding="utf-8")
    except OSError as e:
        _in(f"codex env policy: KHONG doc duoc {tep}: {e}", loi=True)
        return MA_TU_CHOI

    moi, ly_do = go_khoi(cu)
    if moi is None:
        _in(f"codex env policy: TU CHOI — {ly_do} ({tep})", loi=True)
        return MA_TU_CHOI
    if moi == cu:
        _in(f"codex env policy: {ly_do}")
        return MA_OK
    if a.thu_khan:
        _in(f"codex env policy: SE go khoi ({len(cu) - len(moi)} ky tu) — thu khan, khong ghi")
        return MA_OK
    try:
        tep.write_text(moi, encoding="utf-8")
        os.chmod(tep, 0o600)
    except OSError as e:
        _in(f"codex env policy: KHONG ghi duoc {tep}: {e}", loi=True)
        return MA_TU_CHOI
    _in("codex env policy: DA GO khoi inherit=all (xem chu thich dau tep nay)")
    return MA_OK


if __name__ == "__main__":
    sys.exit(main())
