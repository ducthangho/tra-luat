#!/usr/bin/env python3
"""gh_readback_test.py — phản chứng cho gh_readback.py.

Cùng doctrine với `launcher_test.py`/`packet_loop_test.py`: một chốt chỉ TỒN TẠI nếu
có trường hợp làm nó ĐỎ. Toàn bộ ca ở đây chạy OFFLINE — không gọi GitHub, không cần
credential — vì thứ đáng đo là LOGIC SO SÁNH, không phải mạng.

Chạy:  python .claude/dev/gh_readback_test.py
"""
from __future__ import annotations

import importlib.util
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

MODUN = Path(__file__).resolve().parent / "gh_readback.py"
CA: list = []


def ca(fn):
    CA.append(fn)
    return fn


def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise AssertionError(thong_diep)


def _nap():
    """Nạp module SẠCH, không để `.pyc` cũ chấm điểm một bản khác bản trên đĩa."""
    truoc = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("gh_readback_duoi_test", MODUN)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m
    finally:
        sys.dont_write_bytecode = truoc


G = _nap()


@ca
def t01_chuan_hoa_chi_dung_hai_thu_CRLF_va_newline_cuoi():
    """Chuẩn hoá THÊM là tự bịt mắt: nó giấu đúng loại mất mát công cụ này để bắt.

    Mỗi khẳng định dưới đây là MỘT cặp chuỗi mà đúng phép chuẩn hoá tương ứng sẽ
    làm chúng BẰNG NHAU. Ai thêm phép ấy vào `_chuan` thì dòng ấy đỏ ngay.

    Bản đầu chỉ khoá được nhánh khoảng-trắng/strip, và có một khẳng định gần như
    vô dụng (`"Å"` với `"Å".upper() + " "` — `.upper()` là no-op ở đây nên nó chỉ
    đo mỗi dấu cách cuối). Review W0-T1 (PR #158) đo được: thêm `NFC` hoặc
    `casefold` vào `_chuan` thì suite VẪN 7/7 xanh, tức docstring của `_chuan` và
    PR body khai rộng hơn thứ ca này khoá. Hai dòng NFC/casefold dưới đây vá đúng
    chỗ đó — và NFC không phải lo xa: nó là đúng họ `cödex` của PR #92.

    Cặp NFC dựng bằng `chr()` chứ không viết chuỗi thoát: nội dung NÓI VỀ chuẩn
    hoá ký tự thì không nên phụ thuộc vào việc tệp này được lưu/vận chuyển ra sao.
    """
    bang(G._chuan("a\r\nb\r\n") == "a\nb", "CRLF/newline cuoi chua duoc chuan hoa")
    # Các cặp dưới đây KHÁC nhau và PHẢI tiếp tục khác sau chuẩn hoá.
    bang(G._chuan("a  b") != G._chuan("a b"), "da gop khoang trang — se giau mat mat")
    bang(G._chuan("a\nb") != G._chuan("a\n\nb"), "da nuot dong trong — se giau mat mat")
    bang(G._chuan("  a") != G._chuan("a"), "da strip dau dong — se giau mat mat")
    # A + dau vong tren (to hop)  vs  A-vong-tren dung san: NFC lam hai cai bang nhau.
    bang(G._chuan("A" + chr(0x030A)) != G._chuan(chr(0x00C5)),
         "da NFC/NFKC — to hop dau bi che, dung ho co-dot-dot-dex cua PR #92")
    bang(G._chuan("KHOP") != G._chuan("khop"),
         "da casefold/lower — khac biet hoa-thuong bi che")


@ca
def t02_the_HTML_phai_bi_canh_bao_TRUOC_khi_dang():
    """Đây là ca sinh ra từ mất mát THẬT: `<path>` bị xoá sạch khỏi body PR #155."""
    c = G._canh_bao_ky_tu("chay `git cat-file -e HEAD:<path>` roi doc lai")
    bang(any("<path>" in x for x in c), f"KHONG canh bao the HTML: {c}")
    # Không được bắt oan. Bản đầu viết vế này dưới dạng `X == [] or all(...)`, mà
    # `all(...)` trên generator RỖNG luôn True ⇒ cả biểu thức luôn True, bất kể mã.
    # Review W0-T1 chứng minh bằng đột biến: nới regex để bắt cả `<đây>` thì ca này
    # VẪN xanh. Một assert không thể đỏ thì không phải chốt. Nay khẳng định thẳng.
    bang(G._canh_bao_ky_tu("a > b va 3 > 2, xem <đây> nhé") == [],
         "bat oan dau lon hon hoac the phi-ASCII")
    bang(G._canh_bao_ky_tu("khong co gi") == [], "bat oan van ban sach")


@ca
def t03_chuoi_thoat_kieu_u_phai_bi_canh_bao():
    """Bài học PR #92: `\\u0308` là escape HỢP LỆ của JSON nên bị giải mã trên đường."""
    c = G._canh_bao_ky_tu("hai ten: codex va co\\u0308dex")
    bang(any("\\u" in x for x in c), f"KHONG canh bao chuoi thoat: {c}")


@ca
def t04_chay_tra_ma_thoat_THAT_khong_phai_cua_lenh_cuoi_pipe():
    """Chốt trung tâm: `lenh | tail; echo $?` cho mã của `tail`. Ở đây không có pipe."""
    rc, out, _ = G._chay(sys.executable, "-c", "import sys; print('xong'); sys.exit(7)")
    bang(rc == 7, f"ma thoat bi nuot: {rc} (mong doi 7)")
    bang("xong" in out, f"mat stdout: {out!r}")
    rc0, _, _ = G._chay(sys.executable, "-c", "pass")
    bang(rc0 == 0, f"lenh thanh cong ma bao {rc0}")


@ca
def t05_lenh_khong_ton_tai_KHONG_duoc_doc_thanh_thanh_cong():
    rc, _, err = G._chay("mot_lenh_chac_chan_khong_ton_tai_xyz123")
    bang(rc != 0, "lenh khong ton tai ma tra rc=0")
    bang(err.strip() != "", "khong co ly do nao duoc ghi")


@ca
def t06_tep_nguon_RONG_hoac_THIEU_phai_bi_tu_choi_truoc_khi_goi_mang():
    """Tệp rỗng vẫn có sha256 hợp lệ — đăng nó lên là xoá trắng body người khác."""
    import tempfile
    class A:
        pass
    with tempfile.TemporaryDirectory() as d:
        a = A()
        a.file = str(Path(d) / "khong-co.md")
        a.repo, a.number, a.loai, a.chi_kiem = "o/r", 1, "pr", True
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            bang(G.lenh_dang(a) == G.MA_NGUON, "tep THIEU van duoc cho di tiep")
        p = Path(d) / "rong.md"
        p.write_text("   \n\n", encoding="utf-8")
        a.file = str(p)
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            bang(G.lenh_dang(a) == G.MA_NGUON, "tep RONG van duoc cho di tiep")
        # Tệp không phải UTF-8: bảng mã thoát hứa `6`, bản đầu để `read_text` ném
        # `UnicodeDecodeError` ra ngoài và tiến trình chết rc=1 (review W0-T1 đo được).
        # Máy Windows đầy tệp cp1252/UTF-16 nên đây không phải ca hiếm.
        q = Path(d) / "khong-utf8.md"
        q.write_bytes(b"\x93xin chao\x94")
        a.file = str(q)
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            bang(G.lenh_dang(a) == G.MA_NGUON, "tep khong phai UTF-8 khong tra ma 6")


@ca
def t07_ma_thoat_lech_phai_KHAC_ma_thoat_loi_goi():
    """`5` (đã đăng nhưng LỆCH) là ca tệ nhất và không được lẫn với `3` (gọi hỏng)."""
    bang(G.MA_LECH != G.MA_GOI, "hai ca khac han lai dung chung ma thoat")
    bang(G.MA_LECH not in (0, 1), "ma LECH trung ma thong dung — phia goi khong phan biet duoc")
    bang(G.MA_OK == 0, "khop tung byte ma khong tra 0")


@ca
def t08_duong_SO_SANH_phai_tra_MA_LECH_va_IN_DIFF_khi_khac():
    """Chốt TRUNG TÂM của công cụ, và bản đầu KHÔNG có ca nào canh nó.

    Review W0-T1 (PR #158) chứng minh bằng đột biến: đổi `if n == d:` trong
    `lenh_dang` thành `if True:` thì suite vẫn 7/7 QUA, rc=0. Nghĩa là lời hứa lớn
    nhất của công cụ — "đọc ngược rồi diff toàn văn, lệch thì kêu to bằng mã 5" —
    chỉ tồn tại trong văn xuôi. Đúng bệnh mà chính công cụ này sinh ra để chữa:
    một chốt chỉ TỒN TẠI nếu có trường hợp làm nó ĐỎ.

    Chạy OFFLINE bằng cách thay `_chay` — không chạm mạng, không cần credential.
    `--chi-kiem` nên nhánh PATCH không bao giờ được đụng tới.
    """
    import tempfile

    class A:
        pass

    goc = G._chay
    try:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "nguon.md"
            p.write_text("dong mot\n", encoding="utf-8")
            a = A()
            a.file, a.repo, a.number, a.loai, a.chi_kiem = str(p), "o/r", 1, "pr", True

            # (a) ban da den KHAC ban da gui => MA_LECH, va PHAI in diff ra stderr
            G._chay = lambda *x, dau_vao=None: (0, "dong KHAC\n", "")
            loi = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(loi):
                bang(G.lenh_dang(a) == G.MA_LECH, "lech ma KHONG tra MA_LECH")
            bang("dong KHAC" in loi.getvalue(),
                 f"lech ma KHONG in diff — nguoi doc khong biet lech o dau: {loi.getvalue()!r}")

            # (b) giong het => MA_OK. Khong co ve nay thi mot ham luon tra MA_LECH
            #     cung qua duoc ve (a).
            G._chay = lambda *x, dau_vao=None: (0, "dong mot\n", "")
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                bang(G.lenh_dang(a) == G.MA_OK, "khop tung byte ma KHONG tra MA_OK")

            # (c) doc nguoc THAT BAI => MA_GOI, khong duoc doc thanh "khop"
            G._chay = lambda *x, dau_vao=None: (1, "", "gh: Not Found (HTTP 404)")
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                bang(G.lenh_dang(a) == G.MA_GOI, "doc nguoc hong ma khong tra MA_GOI")
    finally:
        G._chay = goc


def main() -> int:
    qua, hong = 0, []
    for fn in CA:
        try:
            fn()
            qua += 1
        except AssertionError as e:
            hong.append((fn.__name__, str(e)))
        except Exception as e:  # noqa: BLE001
            hong.append((fn.__name__, f"{type(e).__name__}: {e}"))
    for ten, ly_do in hong:
        print(f"  HONG {ten}: {ly_do}", flush=True)
    # Tử số CHỈ đếm ca thực sự qua — cùng chốt với `dong_ket_qua` của launcher_test (W0-M1).
    print(f"\ngh_readback tests: {qua}/{len(CA)} ca QUA (hong {len(hong)})", flush=True)
    return 1 if hong else 0


if __name__ == "__main__":
    sys.exit(main())
