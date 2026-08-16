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
import re
import sys
import tempfile
from pathlib import Path

MOC_MO = "# >>> tra-luat: shell_environment_policy (quan ly tu dong) >>>"
MOC_DONG = "# <<< tra-luat <<<"

# Cờ CHẶN codex, đặt CẠNH config chứ không PHẢI TRONG config — ta đang từ chối vì
# không dám sửa tệp của người dùng, nên chặn cũng không được sửa vào đó.
TEN_CO_CHAN = "tra-luat-CHAN-CODEX"

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


# KHỐI CANONICAL — nguyên văn thân khối mà hook TỪNG ghi (lấy từ `c7bbd81`). Đây là
# bản DUY NHẤT từng được ghi ra; nếu sau này có thêm biến thể thì THÊM vào tuple này,
# đừng nới luật so sánh.
#
# ## Vì sao so nguyên khối, không kiểm từng dòng (cross-review lượt 9, MEDIUM)
#
# Bản trước kiểm MEMBERSHIP TỪNG DÒNG: mỗi dòng giữa hai marker chỉ cần khớp một mẫu
# trong danh sách là được. Reviewer đưa ba phản chứng chạy được, cả ba đều bị XOÁ với
# lý do "da go khoi cua ta":
#     [shell_environment_policy] + inherit = "core"   <- GIÁ TRỊ KHÁC HẲN
#     một dòng "# ghi chu cua nguoi dung" đơn độc      <- KHÔNG PHẢI khối ta
#     inherit = "all" rồi mới [shell_environment_policy]  <- THỨ TỰ ĐẢO NGƯỢC
# Trái đúng câu tôi viết ngay trên đầu: "toàn bộ hình dạng khối cũ, không hơn" và
# "người dùng sửa giữa khối ⇒ từ chối". Kiểm từng dòng không thấy CẤU TRÚC.
#
# So nguyên khối thì không còn khe đó: hoặc đúng thứ ta viết, hoặc từ chối. Chuẩn hoá
# tối thiểu — bỏ khoảng trắng cuối dòng và dòng trắng đầu/cuối — vì trình soạn thảo hay
# cắt khoảng trắng cuối, và đó KHÔNG phải "người dùng sửa nội dung".
_THAN_KHOI_CU = (
    '[shell_environment_policy]\n'
    'inherit = "all"\n'
    'exclude = [\n'
    '  "GITHUB_PAT",                                 # credential THAT, khong khop mau mac dinh\n'
    '  "CLAUDE_CODE_SESSION_ID",                     # danh tinh phien, codex khong can\n'
    '  "CLAUDE_CODE_REMOTE_SESSION_ID",\n'
    '  "CLAUDE_CODE_WEBSOCKET_AUTH_FILE_DESCRIPTOR",\n'
    ']',
)


def _chuan_hoa(than: str) -> str:
    return "\n".join(d.rstrip() for d in than.strip("\n").splitlines())


def go_khoi(noi_dung: str) -> tuple[str | None, str]:
    """Trả `(noi_dung_moi, ly_do)`. `None` = TỪ CHỐI, `ly_do` giải thích.

    `noi_dung_moi == noi_dung` nghĩa là không có gì để gỡ.

    ## v2 — bản v1 khớp marker bằng SUBSTRING và LÀM MẤT DỮ LIỆU

    Cross-review lượt 8 (MEDIUM) đưa phản chứng chạy được, không phải suy luận:

        x=1 # <MOC_MO>
        y=2
        z=3 # <MOC_DONG>      ->  "x=1 #\nz=3\n"     (MẤT y=2)

    Marker nằm CÙNG DÒNG với nội dung thật vẫn được `str.index` nhận là marker, và
    phần bị cắt mang theo dòng của người dùng. Tệ nhất: kết quả VẪN parse được như
    TOML hợp lệ, nên phép "parse lại sau khi gỡ" mà tôi dùng làm bằng chứng ở lượt
    trước MÙ HOÀN TOÀN với ca này. Một phép kiểm không thể đỏ thì không phải bằng chứng.

    Hai chốt, PHỦ LÊN NHAU (đo được: gỡ riêng chốt 1 thì chốt 2 vẫn bắt — khai thẳng,
    không nhận là mỗi chốt đã chứng minh độc lập):
      1. marker phải là DÒNG RIÊNG (cho phép khoảng trắng hai bên, không gì khác);
      2. phần GIỮA hai marker phải khớp NGUYÊN KHỐI một bản canonical trong
         `_THAN_KHOI_CU` — xem chú thích ở đó về việc kiểm từng dòng đã hỏng thế nào.
    Chốt 2 chặn cả ca marker nằm trong chuỗi TOML nhiều dòng: nội dung kẹp giữa khi
    ấy là văn bản bất kỳ, không khớp khối canonical nào.
    """
    dong = noi_dung.splitlines(keepends=True)
    vt_mo = [i for i, d in enumerate(dong) if d.strip() == MOC_MO]
    vt_dong = [i for i, d in enumerate(dong) if d.strip() == MOC_DONG]
    # Marker LỌT vào giữa dòng khác: không nhận là marker, nhưng cũng KHÔNG lờ đi —
    # nó là dấu hiệu tệp đã bị sửa tay hoặc bị bản v1 cắt hỏng.
    le_loi = (noi_dung.count(MOC_MO) != len(vt_mo)
              or noi_dung.count(MOC_DONG) != len(vt_dong))
    if not vt_mo and not vt_dong:
        if le_loi:
            return None, "marker xuat hien GIUA dong khac — tep da bi sua tay, KHONG doan"
        return noi_dung, "khong co khoi nao do ta quan ly"
    if le_loi:
        return None, "co marker nam GIUA dong khac ben canh marker dong rieng — KHONG doan"
    if len(vt_mo) != 1 or len(vt_dong) != 1:
        # Nhiều hơn một cặp = tệp đã bị chồng khối (đúng triệu chứng của bản prepend
        # cũ khi marker hỏng). Gỡ "cặp đầu tiên" là ĐOÁN; đoán sai thì xoá nhầm.
        return None, (f"marker khong thanh MOT cap (mo={len(vt_mo)}, dong={len(vt_dong)}) — "
                      f"KHONG doan, sua tay roi chay lai")
    i_mo, i_dong = vt_mo[0], vt_dong[0]
    if i_dong < i_mo:
        return None, "marker DONG nam TRUOC marker MO — tep da bi sua tay, KHONG doan"
    than = _chuan_hoa("".join(dong[i_mo + 1:i_dong]))
    if than not in tuple(_chuan_hoa(k) for k in _THAN_KHOI_CU):
        return None, ("phan giua hai marker KHONG khop khoi canonical nao cua ta "
                      f"({than.splitlines()[0][:40]!r}...) — da bi sua tay, KHONG doan")
    # Xoá đúng các dòng của khối, CỘNG NHIỀU NHẤT MỘT dòng trắng ngay sau — đúng dấu
    # phân cách mà chính bản ghi cũ chèn (`KHOI + "\n\n" + phan_con_lai`).
    #
    # Bản trước dùng `strip("\n")` trên cả tệp: nó xoá luôn dòng trắng đầu/cuối CỦA
    # NGƯỜI DÙNG, tức sửa thứ ta không được phép sửa. Reviewer bắt đúng: "TOML vẫn
    # hợp lệ" KHÔNG đồng nghĩa "đã bảo toàn tệp của họ".
    het = i_dong + 1
    if het < len(dong) and dong[het].strip() == "":
        het += 1
    moi = "".join(dong[:i_mo] + dong[het:])
    return moi, "da go khoi cua ta"


def ghi_nguyen_tu(tep: Path, noi_dung: str) -> None:
    """Ghi kiểu THAY THẾ: tệp đích hoặc là bản CŨ, hoặc là bản MỚI, không có ở giữa.

    Cross-review lượt 8 (MEDIUM): bản trước gọi thẳng `write_text`. Nó TRUNCATE trước
    rồi mới ghi — lỗi giữa chừng (đầy đĩa, tín hiệu) để lại tệp CỤT, trong khi nhánh
    bắt lỗi vẫn trả `MA_TU_CHOI`. Tức ta trả về "đã từ chối, không đụng tệp" cho một
    tệp ĐÃ HỎNG. Hợp đồng của chính tệp này bị phá bởi cách ghi.

    Ghi ra tệp tạm CÙNG THƯ MỤC (khác thư mục thì `os.replace` không còn nguyên tử vì
    có thể qua ranh giới filesystem), `fsync` nội dung, rồi `os.replace`. Hỏng ở bất
    kỳ bước nào trước `replace` thì bản gốc còn nguyên; tệp tạm được dọn.
    """
    # v2 — bản v1 TỰ MỞ MỘT LỖ trong lúc đang vá một lỗ (cross-review lượt 9, MEDIUM).
    #
    # Tên tạm cũ ĐOÁN ĐƯỢC (`config.toml.tra-luat-tam-<pid>`) và mở bằng `open(...,"w")`
    # — không `O_EXCL`, không chống symlink. Phản chứng chạy được: trỏ đúng tên đó thành
    # symlink tới một tệp `victim` ⇒ VICTIM BỊ GHI ĐÈ. Hỏng TRƯỚC `os.replace`, tức phá
    # đúng hợp đồng viết ở dòng ngay trên. Vá một lỗ mà mở lỗ khác trong cùng hàm.
    #
    # `mkstemp` cho tên NGẪU NHIÊN + `O_CREAT|O_EXCL|O_NOFOLLOW`: đã tồn tại (kể cả là
    # symlink) thì tạo THẤT BẠI thay vì ghi xuyên qua.
    ten_that = os.path.realpath(tep)
    if os.path.islink(tep):
        # `os.replace` thay CHÍNH symlink chứ không cập nhật đích — với người dùng quản
        # lý dotfiles bằng symlink, đó là phá cách bố trí của họ. Không đoán ý: từ chối,
        # và chỉ họ chạy thẳng trên đường thật.
        raise OSError(f"{tep} la SYMLINK toi {ten_that} — chay lai voi --tep {ten_that}")
    # GIỮ NGUYÊN quyền tệp gốc. Bản trước ép 0600 cho MỌI tệp: đó là đổi metadata sau
    # lưng người dùng ("thắt chặt lén" — reviewer gọi đúng). Ta đang GỠ một khối, không
    # phải đặt lại chính sách quyền của họ.
    try:
        che_do = os.stat(tep).st_mode & 0o7777
    except OSError:
        che_do = 0o600
    fd, ten_tam = tempfile.mkstemp(dir=str(tep.parent), prefix=tep.name + ".tra-luat-",
                                   suffix=".tam")
    tam = Path(ten_tam)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(noi_dung)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tam, che_do)
        os.replace(tam, tep)        # nguyên tử trong cùng filesystem
        # `fsync` NỘI DUNG thôi chưa đủ để bền qua mất điện: mục lục thư mục cũng phải
        # xuống đĩa, nếu không `replace` có thể bay. Rẻ, và đây là tệp cấu hình chứ
        # không phải vòng lặp nóng.
        try:
            dfd = os.open(str(tep.parent), os.O_RDONLY)
            try:
                os.fsync(dfd)
            finally:
                os.close(dfd)
        except OSError:
            pass                    # không fsync được thư mục thì thôi, KHÔNG hỏng việc
    except BaseException:
        # Kể cả KeyboardInterrupt: rác tạm phải dọn, rồi NÉM TIẾP để phía gọi biết.
        try:
            tam.unlink()
        except OSError:
            pass
        raise


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tep", default="~/.codex/config.toml",
                   help="config codex; mac dinh ~/.codex/config.toml")
    p.add_argument("--thu-khan", action="store_true",
                   help="chi bao se lam gi, KHONG ghi")
    p.add_argument("--co-chan", default=None,
                   help="duong dan tep CO CHAN codex; mac dinh canh config")
    a = p.parse_args(argv)

    tep = Path(os.path.expanduser(a.tep))
    co_chan = Path(os.path.expanduser(a.co_chan)) if a.co_chan else tep.with_name(TEN_CO_CHAN)

    def tu_choi(ly_do: str) -> int:
        # FAIL-CLOSE (cross-review luot 8, HIGH). Ban truoc chi in canh bao roi di tiep:
        # dung luc phat hien config NGUY HIEM ma khong go duoc thi khoi `inherit="all"`
        # cu VAN CON HIEU LUC. Bien mot loi xac-dinh-an-toan thanh phoi moi truong CO
        # CHU DICH — chinh chu reviewer dung, va do la loi cua ban va truoc cua toi.
        #
        # Ta KHONG duoc sua config cua ho (do la ly do dang tu choi), nen chan o phia
        # TA: dung mot la co RIENG. `_do_codex` doc la co nay va ha codex xuong
        # CHUA_XAC_THUC, nen `doctor --doi-kha-dung` chan, va nguoi doc thay ly do.
        _in(f"codex env policy: TU CHOI — {ly_do} ({tep})", loi=True)
        try:
            co_chan.write_text(
                "codex bi CHAN: khong go duoc khoi shell_environment_policy cu.\n"
                f"ly do: {ly_do}\n"
                f"tep: {tep}\n"
                "Khoi `inherit = \"all\"` co the VAN CON HIEU LUC — no truyen TOAN BO\n"
                "moi truong cho moi lenh con cua codex. Sua tay roi chay lai:\n"
                "  python3 .claude/dev/codex_env_policy.py\n",
                encoding="utf-8")
        except OSError as e:
            _in(f"codex env policy: KHONG dat duoc co chan ({e}) — CHAN CODEX BANG TAY",
                loi=True)
        return MA_TU_CHOI

    def go_co_chan() -> None:
        """Gỡ cờ khi đã sạch. Cờ không tự hết là một chốt đỏ thường trực."""
        try:
            co_chan.unlink()
            _in("codex env policy: da go co chan codex")
        except OSError:
            pass

    if not tep.exists():
        _in("codex env policy: khong co config.toml — khong co gi de go")
        go_co_chan()
        return MA_OK
    try:
        cu = tep.read_text(encoding="utf-8")
    except OSError as e:
        return tu_choi(f"KHONG doc duoc: {e}")

    moi, ly_do = go_khoi(cu)
    if moi is None:
        return tu_choi(ly_do)
    if moi == cu:
        _in(f"codex env policy: {ly_do}")
        go_co_chan()
        return MA_OK
    if a.thu_khan:
        _in(f"codex env policy: SE go khoi ({len(cu) - len(moi)} ky tu) — thu khan, khong ghi")
        return MA_OK
    try:
        ghi_nguyen_tu(tep, moi)
    except OSError as e:
        return tu_choi(f"KHONG ghi duoc: {e}")
    _in("codex env policy: DA GO khoi inherit=all (xem chu thich dau tep nay)")
    go_co_chan()
    return MA_OK


if __name__ == "__main__":
    sys.exit(main())
