#!/usr/bin/env python3
"""Phản chứng cho `codex_cred.py` — CHẠY ĐƯỢC, không cần mạng, mỗi ca một đột biến.

Mọi ca đều đo trên MỘT module nạp động, nên đột biến chạy trên **bản sao tạm có tên
RIÊNG** chứ không ghi vào tệp thật. Hai lý do, cả hai đã trả giá trong kho này:

* ghi vào tệp thật rồi khôi phục trong `finally` là **bom hẹn giờ** — lượt chạy bị giết
  giữa chừng thì `finally` không chạy và tệp ở lại trạng thái méo; một bản vá NGƯỢC đã đi
  thẳng vào commit theo đúng đường đó;
* CPython coi `.pyc` còn hợp lệ theo **(mtime tính bằng GIÂY, kích thước)** — hai đột biến
  cùng kích thước ghi trong cùng một giây thì bản sau **chạy mã của bản trước** và mutant
  báo "đã giết" mà chưa từng chạy. Ba lượt review từng chết vì chuyện này.

Vì vậy: `sys.dont_write_bytecode = True` + tên tệp riêng từng đột biến + `invalidate_caches`.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # lớp 1 chống va chạm .pyc

GOC = Path(__file__).with_name("codex_cred.py")
_dem = 0


def nap(nguon: str, nhan: str):
    """Nạp `nguon` thành module với tên tệp RIÊNG cho từng lần gọi."""
    global _dem
    _dem += 1
    d = Path(tempfile.mkdtemp(prefix="cc-test-"))
    # tên riêng từng đột biến: lớp 2 chống va chạm .pyc
    t = d / f"cc_{nhan}_{_dem}.py"
    t.write_text(nguon, encoding="utf-8")
    importlib.invalidate_caches()  # lớp 3
    spec = importlib.util.spec_from_file_location(t.stem, t)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    assert not list(d.glob("__pycache__/*")), "đã ghi .pyc — chốt chống va chạm hỏng"
    return m


# ── đầu ra THẬT của `codex login --device-auth`, chép nguyên (kèm ANSI) từ lần đo
#    2026-08-23. Giữ nguyên byte: nếu codex đổi định dạng, ca này phải ĐỎ chứ không
#    được im lặng thích nghi.
DAU_RA_THAT = (
    "\x1b[?25l\r\n"
    "Welcome to Codex [v\x1b[90m0.149.0\x1b[0m]\r\n"
    "\x1b[90mOpenAI's command-line coding agent\x1b[0m\r\n\r\n"
    "Follow these steps to sign in with ChatGPT using device code authorization:\r\n\r\n"
    "1. Open this link in your browser and sign in to your account\r\n"
    "   \x1b[94mhttps://auth.openai.com/codex/device\x1b[0m\r\n\r\n"
    "2. Enter this one-time code \x1b[90m(expires in 15 minutes)\x1b[0m\r\n"
    "   \x1b[94m8FY2-J8PNS\x1b[0m\r\n\r\n"
)


class GiaChay:
    """`subprocess.run` giả GIỮ TRẠNG THÁI, không diễn kịch bản.

    Kho này đã có 40/40 xanh trong khi một đột biến xoá hẳn lệnh phá vẫn qua, vì đồ giả
    diễn kịch bản. Nên đồ giả ở đây ghi NHẬT KÝ lời gọi để ca test đọc được.
    """

    def __init__(self, rc=0, ra="", loi=""):
        self.rc, self.ra, self.loi, self.nhat_ky = rc, ra, loi, []

    def __call__(self, argv, **kw):
        self.nhat_ky.append(list(argv))
        return subprocess.CompletedProcess(argv, self.rc, self.ra, self.loi)


# ─────────────────────────── các ca ───────────────────────────
# Mỗi ca nhận module M để chạy được trên cả bản gốc lẫn bản đột biến.

def t1_doc_duoc_url_va_ma_tu_dau_ra_that(M):
    url, ma = M.doc_moc_device(DAU_RA_THAT)
    assert url == "https://auth.openai.com/codex/device", f"url sai: {url!r}"
    assert ma == "8FY2-J8PNS", f"mã sai: {ma!r}"


def t2_chua_thay_thi_tra_None_khong_doan(M):
    # Log nội bộ có mặt nhưng CHƯA có url/mã — đây đúng trạng thái ba lượt thử đầu mắc kẹt.
    url, ma = M.doc_moc_device("INFO codex_cli::login: starting device code login flow\n")
    assert url is None and ma is None, f"bịa ra ({url!r}, {ma!r}) từ đầu vào không có gì"


def t3_kiem_song_doi_DAU_HIEU_khong_tin_rc0(M):
    # rc=0 + đầu ra RỖNG là ca ĐÃ XẢY RA THẬT (r244). Cổng tin rc là cổng bị lừa.
    M.subprocess.run = GiaChay(rc=0, ra="", loi="")
    ok, vi_sao = M._kiem_song(Path("/khong-quan-trong"))
    assert not ok, "rc=0 + đầu ra rỗng mà vẫn báo SỐNG"
    assert "dấu hiệu sống" in vi_sao, vi_sao


def t4_kiem_song_bat_credential_bi_tu_choi(M):
    M.subprocess.run = GiaChay(rc=0, ra=f"{M.DAU_HIEU_SONG}", loi="error: refresh_token_invalidated")
    ok, vi_sao = M._kiem_song(Path("/khong-quan-trong"))
    assert not ok, "có dấu hiệu bị từ chối mà vẫn báo SỐNG"
    assert "TỪ CHỐI" in vi_sao, vi_sao


def t5_kiem_song_dat_khi_co_dau_hieu(M):
    # Chiều BẮT OAN: đủ điều kiện thì phải ĐẠT, không cảnh báo thừa.
    M.subprocess.run = GiaChay(rc=0, ra=f"nói: {M.DAU_HIEU_SONG}\n")
    ok, _ = M._kiem_song(Path("/khong-quan-trong"))
    assert ok, "đầu ra có dấu hiệu sống mà vẫn báo CHẾT"


def t6_khong_in_gia_tri_khi_khong_co_co(M, capsys=None):
    """Mặc định KHÔNG được in base64 ra màn hình."""
    bi_mat = b'{"tokens":{"refresh_token":"BIMAT-KHONG-DUOC-IN"}}'
    d = Path(tempfile.mkdtemp())
    (d / "auth.json").write_bytes(bi_mat)
    M._co_codex = lambda: "/gia/codex"
    M._chay_device_auth = lambda home, han: (True, "ok")
    M._kiem_song = lambda home: (True, "rc=0, có dấu hiệu")
    ra_tep = d / "b64.txt"

    class A:
        codex_home, ra, han_giay = str(d), str(ra_tep), 5
        in_gia_tri, cai_de = False, False

    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = M.cmd_lay(A())
    out = buf.getvalue()
    assert rc == 0, f"đáng lẽ ĐẠT, được rc={rc}"
    b64 = __import__("base64").b64encode(bi_mat).decode()
    assert b64 not in out, "ĐÃ IN base64 ra màn hình dù KHÔNG có --in-gia-tri"
    assert "BIMAT-KHONG-DUOC-IN" not in out, "lộ token thô"
    assert ra_tep.is_file() and ra_tep.read_text().strip() == b64, "không ghi đúng tệp ra"
    assert (ra_tep.stat().st_mode & 0o777) == 0o600, "tệp bí mật không phải 0600"


def t7_sao_luu_khong_de_ban_cu(M):
    d = Path(tempfile.mkdtemp())
    f = d / "auth.json"
    f.write_text("CU")
    b1 = M._sao_luu(f)
    assert b1 and b1.read_text() == "CU"
    assert (b1.stat().st_mode & 0o777) == 0o600, "bản sao lưu không phải 0600"
    f.write_text("MOI")
    b2 = M._sao_luu(f)
    assert b2 != b1, "bản sao lưu thứ hai ĐÈ lên bản thứ nhất"
    assert b1.read_text() == "CU", "sao lưu cũ bị hỏng"


def t8_thieu_codex_la_KHONG_DO_DUOC_khong_phai_DAT(M):
    M._co_codex = lambda: None

    class A:
        codex_home = ra = None
        han_giay, in_gia_tri, cai_de = 5, False, False

    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = M.cmd_lay(A())
    assert rc == M.RC[M.KHONG_DO_DUOC], f"thiếu codex phải là KHÔNG_ĐO_ĐƯỢC, được rc={rc}"
    assert rc != 0, "thiếu công cụ mà trả 0 — đúng lỗi 'cổng tự tắt'"


CA = [t1_doc_duoc_url_va_ma_tu_dau_ra_that, t2_chua_thay_thi_tra_None_khong_doan,
      t3_kiem_song_doi_DAU_HIEU_khong_tin_rc0, t4_kiem_song_bat_credential_bi_tu_choi,
      t5_kiem_song_dat_khi_co_dau_hieu, t6_khong_in_gia_tri_khi_khong_co_co,
      t7_sao_luu_khong_de_ban_cu, t8_thieu_codex_la_KHONG_DO_DUOC_khong_phai_DAT]

# ─────────────────────────── đột biến ───────────────────────────
# (nhãn, chuỗi CŨ, chuỗi MỚI, ca ĐÍCH phải chết)
DOT_BIEN = [
    # Đột biến của t1 phải chạm ĐÚNG tính chất t1 canh (rút đúng url+mã từ đầu ra CÓ ANSI).
    # Bản đầu nới lỏng regex url thành r"device" — nó giết cả t2, vì chuỗi "device code
    # login flow" khớp. Đó là đột biến ĐO HAI THỨ, không phải chốt trói nhầm: sửa đột
    # biến, đừng sửa chốt. Bỏ bước lột ANSI chỉ hỏng đúng đường có mã màu ⇒ t2 (đầu vào
    # không màu) vẫn xanh.
    ("t1_khong_lot_ansi", 'return _ANSI.sub("", s)', "return s",
     "t1_doc_duoc_url_va_ma_tu_dau_ra_that"),
    ("t2_doan_bua_khi_thieu", "return (u.group(0) if u else None, m.group(1) if m else None)",
     'return (u.group(0) if u else "https://auth.openai.com/codex/device",\n'
     '            m.group(1) if m else "AAAA-BBBBB")',
     "t2_chua_thay_thi_tra_None_khong_doan"),
    ("t3_tin_rc0", 'if DAU_HIEU_SONG not in ra:', 'if False:',
     "t3_kiem_song_doi_DAU_HIEU_khong_tin_rc0"),
    ("t4_bo_dau_hieu_tu_choi", '"please log in again", "could not be refreshed"):',
     '"please log in again",):' + "\n" + " " * 8 + 'dau = "\\x00khong-bao-gio-khop"',
     "t4_kiem_song_bat_credential_bi_tu_choi"),
    ("t5_bao_chet_bua", "return (True, f\"rc={p.returncode}, có {DAU_HIEU_SONG}\")",
     'return (False, "bịa")', "t5_kiem_song_dat_khi_co_dau_hieu"),
    ("t6_in_bi_mat_luon", "if a.in_gia_tri:", "if True:",
     "t6_khong_in_gia_tri_khi_khong_co_co"),
    # Gỡ đúng vòng tìm tên trống ⇒ quay lại bệnh "hai lần trong cùng một giây thì đè nhau".
    ("t7_bo_vong_tim_ten_trong", "while bak.exists():", "while False:",
     "t7_sao_luu_khong_de_ban_cu"),
    ("t8_thieu_cong_cu_van_xanh", "return RC[KHONG_DO_DUOC]\n\n    tam =",
     "return RC[DAT]\n\n    tam =", "t8_thieu_codex_la_KHONG_DO_DUOC_khong_phai_DAT"),
]


def chay_suite(M) -> set[str]:
    """Chạy TOÀN BỘ ca trên module M, trả tập tên ca ĐỎ."""
    do = set()
    for ca in CA:
        # module nạp lại mỗi ca: các ca vá `subprocess.run`/`_co_codex` lên module,
        # không cô lập thì ca sau ăn bản vá của ca trước và bán kính đo ra sai.
        Mi = nap(M.__nguon__, M.__nhan__)
        Mi.__nguon__, Mi.__nhan__ = M.__nguon__, M.__nhan__
        try:
            ca(Mi)
        except Exception as e:
            do.add(ca.__name__)
            if os.environ.get("CC_CHI_TIET"):
                print(f"    ĐỎ {ca.__name__}: {type(e).__name__}: {e}")
    return do


def main() -> int:
    goc = GOC.read_text(encoding="utf-8")
    M = nap(goc, "goc")
    M.__nguon__, M.__nhan__ = goc, "goc"

    do = chay_suite(M)
    n = len(CA)
    print(f"nền: {n - len(do)}/{n} đạt")
    for t in sorted(do):
        print(f"  ĐỎ  {t}")
    if do:
        print("TỔNG: ĐỎ (nền chưa xanh — không đo đột biến khi nền đã đỏ)")
        return 1

    print()
    print("ĐỘT BIẾN — mỗi ca một cái, bán kính đo trên TOÀN suite:")
    xau = []
    for nhan, cu, moi, dich in DOT_BIEN:
        if cu not in goc:
            print(f"  ĐỎ  {nhan}: không tìm thấy mỏ neo {cu!r}")
            xau.append(nhan)
            continue
        Mm = nap(goc.replace(cu, moi, 1), nhan)
        Mm.__nguon__, Mm.__nhan__ = goc.replace(cu, moi, 1), nhan
        chet = chay_suite(Mm)
        ok = dich in chet
        ngoai = sorted(chet - {dich})
        trang = "ok " if ok and not ngoai else "ĐỎ "
        print(f"  {trang} {nhan:26} giết {len(chet)}/{n}"
              f"  đích={'CHẾT' if ok else 'SỐNG'}"
              + (f"  NGOÀI HỌ={ngoai}" if ngoai else "  ngoài họ=0"))
        if not ok:
            xau.append(f"{nhan}: đích SỐNG — đột biến không giết được ca nó canh")
        if ngoai:
            xau.append(f"{nhan}: giết thêm {ngoai} — chốt trói nhầm thứ")

    print()
    print(f"SỐ LIỆU:  ca {n}  ·  đột biến {len(DOT_BIEN)}")
    if xau:
        print("TỔNG: ĐỎ")
        for x in xau:
            print(f"  - {x}")
        return 1
    print("TỔNG: ĐẠT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
