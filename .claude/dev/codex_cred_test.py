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
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # lớp 1 chống va chạm .pyc

GOC = Path(__file__).with_name("codex_cred.py")
_dem = 0


class TinHieuChotCa(AssertionError):
    """#1079 F01: tín hiệu chốt của suite; mã triển khai không tự ném lớp này."""


def la_chot_cua_suite(e: BaseException) -> bool:
    """#1079 F01 — đỏ-do-assertion CHỈ khi `TinHieuChotCa`, hoặc `assert` trần mà khung
    trong cùng là một câu `assert` của CHÍNH tệp này. `except … raise AssertionError` hay
    AssertionError từ codex_cred.py không qua được: khung trong cùng không phải `assert` ở đây."""
    if isinstance(e, TinHieuChotCa):
        return True
    if type(e) is not AssertionError or e.__traceback__ is None:
        return False
    tb = e.__traceback__
    while tb.tb_next is not None:
        tb = tb.tb_next
    import linecache
    tep = tb.tb_frame.f_code.co_filename
    return (os.path.realpath(tep) == os.path.realpath(__file__)
            and linecache.getline(tep, tb.tb_lineno).lstrip().startswith("assert"))


def nap(nguon: str, nhan: str):
    """Nạp `nguon` thành module với tên tệp RIÊNG cho từng lần gọi."""
    global _dem
    _dem += 1
    d = Path(tempfile.mkdtemp(prefix="cc-test-"))
    # tên riêng từng đột biến: lớp 2 chống va chạm .pyc
    t = d / f"cc_{nhan}_{_dem}.py"
    t.write_text(nguon, encoding="utf-8")
    # The public credential command uses the repository's shared storage backend.
    companion = Path(__file__).with_name("launcher.py")
    (d / "launcher.py").write_text(companion.read_text(encoding="utf-8"),
                                    encoding="utf-8", newline="\n")
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


def kiem_song_bang_codex_gia(M, rc=0, ra="", loi=""):
    """Dựng script `codex` giả portable: `sys.executable exec ...` trên mọi nền."""
    with tempfile.TemporaryDirectory(prefix="codex-gia-") as td:
        d = Path(td)
        (d / "exec").write_text(
            "import sys\n"
            f"sys.stdout.write({ra!r})\n"
            f"sys.stderr.write({loi!r})\n"
            f"raise SystemExit({rc})\n",
            encoding="utf-8")
        cwd = os.getcwd()
        try:
            os.chdir(d)
            M._co_codex = lambda: sys.executable
            return M._kiem_song(d)
        finally:
            os.chdir(cwd)


def doi_tep_kin(f: Path, thong_bao: str):
    # Windows không biểu diễn ACL bằng bit POSIX; chính ca vẫn chạy, chỉ phép đo bit là POSIX-only.
    if os.name != "nt":
        assert (f.stat().st_mode & 0o777) == 0o600, thong_bao
    else:
        assert f.is_file(), thong_bao


def gan_O_NOFOLLOW_gia_cho_ca_khong_do_kernel(M):
    """Giữ ca phi-kernel chạy được trên Windows; t12 mới đo ngữ nghĩa cờ thật."""
    if not hasattr(M.os, "O_NOFOLLOW"):
        class OsCoNoFollow:
            O_NOFOLLOW = 0
            def __getattr__(self, ten): return getattr(os, ten)
        M.os = OsCoNoFollow()


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
    ok, vi_sao = kiem_song_bang_codex_gia(M)
    assert not ok, "rc=0 + đầu ra rỗng mà vẫn báo SỐNG"
    assert "dấu hiệu sống" in vi_sao, vi_sao
    assert not kiem_song_bang_codex_gia(
        M, loi=f"echo prompt {M.DAU_HIEU_SONG}")[0], "tin dấu hiệu bị echo ở stderr"


def t4_kiem_song_bat_credential_bi_tu_choi(M):
    ok, vi_sao = kiem_song_bang_codex_gia(
        M, ra=M.DAU_HIEU_SONG, loi="error: refresh_token_invalidated")
    assert not ok, "có dấu hiệu bị từ chối mà vẫn báo SỐNG"
    assert "TỪ CHỐI" in vi_sao, vi_sao


def t5_kiem_song_dat_khi_co_dau_hieu(M):
    # Chiều BẮT OAN: đủ điều kiện thì phải ĐẠT, không cảnh báo thừa.
    assert not kiem_song_bang_codex_gia(
        M, rc=7, ra=f"{M.DAU_HIEU_SONG}\n")[0], "rc!=0 mà vẫn báo SỐNG"
    ok, _ = kiem_song_bang_codex_gia(M, ra=f"{M.DAU_HIEU_SONG}\n")
    assert ok, "đầu ra có dấu hiệu sống mà vẫn báo CHẾT"


def t6_khong_in_gia_tri_khi_khong_co_co(M, capsys=None):
    """Mặc định KHÔNG được in base64 ra màn hình."""
    bi_mat = b'{"tokens":{"refresh_token":"BIMAT-KHONG-DUOC-IN"}}'
    d = Path(tempfile.mkdtemp())
    M._co_codex = lambda: "/gia/codex"
    def login(home, han):
        (home / "auth.json").write_bytes(bi_mat)
        (home / "auth.json").chmod(0o600)
        return True, "ok"
    M._chay_device_auth = login
    M._kiem_song = lambda home: (True, "rc=0, có dấu hiệu")
    ra_tep = d / "b64.txt"
    vat_giu = d / "khong-duoc-doi.txt"
    vat_giu.write_text("GIU-NGUYEN")
    os.link(vat_giu, ra_tep)  # ghi tại chỗ sẽ sửa cả hardlink; replace nguyên tử thì không

    class A:
        codex_home, ra, han_giay = None, str(ra_tep), 5
        in_gia_tri, cai_de = False, False
        tep_dan = None          # argparse thật LUÔN có trường này; đồ giả phải giống thật.

    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    # The shared store now rejects hardlinked output rather than replacing it.
    # Both links must remain intact on that fail-closed path.
    with redirect_stdout(io.StringIO()):
        try:
            M.cmd_lay(A())
        except OSError:
            pass
        else:
            raise TinHieuChotCa("hardlinked credential artifact was accepted")
    assert ra_tep.read_text() == vat_giu.read_text() == "GIU-NGUYEN"
    ra_tep.unlink()
    with redirect_stdout(buf):
        rc = M.cmd_lay(A())
    out = buf.getvalue()
    assert rc == 0, f"đáng lẽ ĐẠT, được rc={rc}"
    b64 = __import__("base64").b64encode(bi_mat).decode()
    assert b64 not in out, "ĐÃ IN base64 ra màn hình dù KHÔNG có --in-gia-tri"
    assert "BIMAT-KHONG-DUOC-IN" not in out, "lộ token thô"
    assert ra_tep.is_file() and ra_tep.read_text().strip() == b64, "không ghi đúng tệp ra"
    assert vat_giu.read_text() == "GIU-NGUYEN", "ghi đè tại chỗ làm đổi inode dùng chung"
    doi_tep_kin(ra_tep, "tệp bí mật không phải 0600")

    homes = []
    def dang_nhap_tam(home, _han):
        homes.append(home); (home / "auth.json").write_bytes(bi_mat)
        (home / "auth.json").chmod(0o600)
        return (True, "ok")
    M._chay_device_auth = dang_nhap_tam
    class B(A):
        codex_home, ra, tep_dan = None, str(d / "b64-2.txt"), str(d / "setup-2.md")
    with redirect_stdout(io.StringIO()):
        assert M.cmd_lay(B()) == 0
    assert homes and not homes[0].exists(), "CODEX_HOME tạm còn giữ raw credential sau khi xong"


def t7_sao_luu_khong_de_ban_cu(M):
    gan_O_NOFOLLOW_gia_cho_ca_khong_do_kernel(M)
    d = Path(tempfile.mkdtemp())
    f = d / "auth.json"
    f.write_text("CU")
    M.time.time = lambda: 1234567890
    da_giu = d / "auth.json.bak-1234567890"
    da_giu.write_text("KHONG-DUOC-DE")
    b1 = M._sao_luu(f)
    assert b1 and b1.read_text() == "CU"
    assert da_giu.read_text() == "KHONG-DUOC-DE" and b1 != da_giu, "đè tên đã bị giữ"
    doi_tep_kin(b1, "bản sao lưu không phải 0600")
    f.write_text("MOI")
    b2 = M._sao_luu(f)
    assert b2 != b1, "bản sao lưu thứ hai ĐÈ lên bản thứ nhất"
    assert b1.read_text() == "CU", "sao lưu cũ bị hỏng"


def t8_thieu_codex_la_KHONG_DO_DUOC_khong_phai_DAT(M):
    M._co_codex = lambda: None

    class A:
        codex_home = ra = tep_dan = None
        han_giay, in_gia_tri, cai_de = 5, False, False

    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = M.cmd_lay(A())
    assert rc == M.RC[M.KHONG_DO_DUOC], f"thiếu codex phải là KHÔNG_ĐO_ĐƯỢC, được rc={rc}"
    assert rc != 0, "thiếu công cụ mà trả 0 — đúng lỗi 'cổng tự tắt'"


def t9_cmd_lay_GHI_tep_huong_dan_dan(M):
    """Tệp hướng dẫn dán phải do CHÍNH lệnh sinh ra, không phải việc làm tay sau đó.

    Lần đầu tôi soạn tệp ấy bằng tay sau khi lệnh chạy xong. Làm tay thì lần sau người
    khác quên — nên nó phải là một bước của mã, và ca này canh đúng chuyện đó.
    """
    bi_mat = b'{"tokens":{"access_token":"a.b.c","refresh_token":"R"}}'
    d = Path(tempfile.mkdtemp())
    M._co_codex = lambda: "/gia/codex"
    def login(home, han):
        (home / "auth.json").write_bytes(bi_mat)
        (home / "auth.json").chmod(0o600)
        return True, "ok"
    M._chay_device_auth = login
    M._kiem_song = lambda home: (True, "rc=0")
    tep_dan = d / "huong_dan.md"

    class A:
        codex_home, ra, han_giay = None, str(d / "b64.txt"), 5
        in_gia_tri, cai_de = False, False
    A.tep_dan = str(tep_dan)

    import io
    from contextlib import redirect_stdout
    with redirect_stdout(io.StringIO()):
        rc = M.cmd_lay(A())
    assert rc == 0, f"rc={rc}"
    assert tep_dan.is_file(), "KHÔNG sinh tệp hướng dẫn dán"
    noi = tep_dan.read_text(encoding="utf-8")
    b64 = __import__("base64").b64encode(bi_mat).decode()
    assert b64 in noi, "tệp hướng dẫn thiếu chính chuỗi cần dán"
    assert "CODEX_AUTH_JSON" in noi, "tệp không nói tên biến"
    doi_tep_kin(tep_dan, "tệp chứa bí mật không phải 0600")


def t10_gio_con_lai_doc_exp_va_bu_padding(M):
    """`exp` đọc từ JWT; payload base64url THIẾU padding là ca thật, không phải giả định."""
    import base64 as _b, json as _j, time as _t
    than = _j.dumps({"exp": int(_t.time()) + 7200}).encode()
    # bỏ padding đúng như JWT thật làm
    p64 = _b.urlsafe_b64encode(than).decode().rstrip("=")
    assert len(p64) % 4 != 0, "fixture chưa chạm ca thiếu padding — sửa fixture"
    d = Path(tempfile.mkdtemp())
    (d / "a.json").write_text(_j.dumps({"tokens": {"access_token": f"h.{p64}.s"}}))
    gio = M._gio_con_lai(d / "a.json")
    assert gio is not None, "không đọc được exp (nhiều khả năng vỡ ở padding)"
    assert 1.9 < gio < 2.1, f"exp sai: {gio}"
    # hỏng thì phải trả None, KHÔNG được ném
    (d / "b.json").write_text('{"tokens":{"access_token":"khong-phai-jwt"}}')
    assert M._gio_con_lai(d / "b.json") is None, "token không phải JWT mà vẫn trả số"
    for i, obj in enumerate(([], {"tokens": "khong-phai-object"})):
        f = d / f"auth-hong-{i}.json"; f.write_text(_j.dumps(obj))
        assert M._gio_con_lai(f) is None, f"auth dị dạng {i} làm văng/ra số"
    (d / "auth.json").write_text("[]")
    class A:
        codex_home, kiem_song = str(d), False
    import io as _io
    from contextlib import redirect_stdout as _redirect
    with _redirect(_io.StringIO()):
        assert M.cmd_kiem(A()) == M.RC[M.DO], "cmd_kiem văng/xanh với JSON không phải object"
    for i, payload in enumerate(([], {}, {"exp": True}, {"exp": "12"},
                                 {"exp": float("nan")}, {"exp": 10 ** 400})):
        raw = _b.urlsafe_b64encode(_j.dumps(payload).encode()).decode().rstrip("=")
        f = d / f"jwt-hong-{i}.json"
        f.write_text(_j.dumps({"tokens": {"access_token": f"h.{raw}.s"}}))
        assert M._gio_con_lai(f) is None, f"payload dị dạng {i} làm văng/ra số"


def t11_sao_luu_tu_choi_symlink(M):
    gan_O_NOFOLLOW_gia_cho_ca_khong_do_kernel(M)
    d = Path(tempfile.mkdtemp())
    nguon, dich = d / "bi-mat.json", d / "auth.json"
    nguon.write_text("BI-MAT")
    try:
        dich.symlink_to(nguon)
    except (OSError, NotImplementedError):
        print("  BỎ QUA symlink thật; nền không cho tạo — đo guard bằng symlink giả")
        original_path = dich
        class SymlinkGia:
            def is_symlink(self): return True
            def is_file(self): return False
            def __str__(self): return str(original_path)
        dich = SymlinkGia()
    try:
        M._sao_luu(dich)
    except OSError as e:
        assert "từ chối sao lưu qua symlink" in str(e), f"từ chối sai tầng: {e}"
    else:
        raise TinHieuChotCa("_sao_luu không từ chối đích là symlink")
    assert nguon.read_text() == "BI-MAT", "đã sửa nguồn mà symlink trỏ tới"


def t12_sao_luu_O_NOFOLLOW_tai_diem_doc(M):
    d = Path(tempfile.mkdtemp())
    dich, bi_mat = d / "auth.json", d / "ngoai-pham-vi"
    dich.write_text("AN-TOAN")
    bi_mat.write_text("BI-MAT-KHAC")
    mo_that = os.open
    nofollow = getattr(os, "O_NOFOLLOW", 0)

    if nofollow:
        class OsDoiNguon:
            da_doi = False
            def __getattr__(self, ten): return getattr(os, ten)
            def open(self, path, flags, mode=0o777):
                if Path(path) == dich:
                    self.da_doi = True
                    dich.unlink(); dich.symlink_to(bi_mat)
                return mo_that(path, flags, mode)
    else:
        print("  BỎ QUA phản chứng kernel O_NOFOLLOW; đo wiring bằng os giả có cờ")
        dich = d / "auth-race.json"; dich.write_text("AN-TOAN")
        class OsDoiNguon:
            O_NOFOLLOW = 1 << 29
            da_doi = False
            def __getattr__(self, ten): return getattr(os, ten)
            def open(self, path, flags, mode=0o777):
                if Path(path) == dich:
                    self.da_doi = True
                    if flags & self.O_NOFOLLOW:
                        raise OSError("os giả từ chối symlink tại điểm dùng")
                    return mo_that(bi_mat, flags, mode)
                return mo_that(path, flags, mode)

    os_doi = OsDoiNguon()
    M.os = os_doi
    try:
        M._sao_luu(dich)
    except OSError:
        pass
    else:
        raise TinHieuChotCa("đổi nguồn thành symlink giữa check/use mà vẫn sao lưu")
    assert os_doi.da_doi, "ca chưa chạm lần os.open nguồn"
    assert bi_mat.read_text() == "BI-MAT-KHAC", "đã sửa nguồn ngoài phạm vi"


def t13_sao_luu_fail_closed_khi_thieu_O_NOFOLLOW(M):
    d = Path(tempfile.mkdtemp())
    dich = d / "auth.json"
    dich.write_text("AN-TOAN")
    mo_that = os.open
    co_nofollow = hasattr(os, "O_NOFOLLOW")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    def cam_mo(*_a, **_kw):
        raise TinHieuChotCa("đã gọi os.open trên nền thiếu O_NOFOLLOW")
    try:
        if co_nofollow:
            delattr(os, "O_NOFOLLOW")
        os.open = cam_mo
        try:
            M._sao_luu(dich)
        except OSError as e:
            assert "O_NOFOLLOW" in str(e), f"lỗi không nêu giới hạn nền: {e}"
        else:
            raise TinHieuChotCa("nền thiếu O_NOFOLLOW mà _sao_luu vẫn chạy")
        assert not list(d.glob("*.bak-*")), "đã tạo .bak trước khi fail-closed"
    finally:
        os.open = mo_that
        if co_nofollow:
            os.O_NOFOLLOW = nofollow
    gan_O_NOFOLLOW_gia_cho_ca_khong_do_kernel(M)
    bak = M._sao_luu(dich)
    assert bak and bak.read_text() == "AN-TOAN", "chặn oan nền có O_NOFOLLOW"


def t14_probe_khong_ke_thua_snapshot(M):
    """A real inert child checks its environment before returning the marker."""
    from unittest.mock import patch
    with tempfile.TemporaryDirectory(prefix="codex-env-boundary-") as td:
        d = Path(td)
        (d / "exec").write_text(
            "import os\nassert 'CODEX_AUTH_JSON' not in os.environ\n"
            "print('TRALUAT-CRED-OK')\n", encoding="utf-8")
        cwd = os.getcwd()
        try:
            os.chdir(d)
            M._co_codex = lambda: sys.executable
            with patch.dict(os.environ, {"CODEX_AUTH_JSON": "INERT-RAW-SNAPSHOT"}):
                ok, message = M._kiem_song(d)
                assert ok and "TRALUAT-CRED-OK" in message
                assert os.environ["CODEX_AUTH_JSON"] == "INERT-RAW-SNAPSHOT"
        finally:
            os.chdir(cwd)


def t15_home_chua_tao_la_KHONG_DO_DUOC(M):
    """wp484 g7 (P2 #509 thread XL-): home hợp lệ nhưng chưa tạo = chưa có credential (rc 3),
    cùng mã với thư mục có mà thiếu auth.json — không phải ĐỎ rc 2."""
    import argparse
    with tempfile.TemporaryDirectory(prefix="codex-home-vang-") as td:
        for home in (Path(td) / "chua-tao", Path(td)):
            rc = M.cmd_kiem(argparse.Namespace(codex_home=str(home), kiem_song=False))
            assert rc == M.RC[M.KHONG_DO_DUOC], f"{home}: rc {rc} != {M.RC[M.KHONG_DO_DUOC]}"


def t16_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra(M):
    """wp484 g7 — đường thứ hai của P2 thread XMG: `kiem --kiem-song` từng nuốt kết quả ghi."""
    import argparse
    import json as _json
    with tempfile.TemporaryDirectory(prefix="codex-ghi-hong-") as td:
        home = Path(td) / "codex"
        that = M._repo_helpers()
        with that["_KhoCodex"](home, create=True) as store:
            store.write("auth.json", _json.dumps({"tokens": {"refresh_token": "INERT"}}).encode(), None)
        gia = dict(that, _danh_dau_auth_hong=lambda h, da_probe=None: False, _dang_cho_snapshot=lambda h: False)
        M._repo_helpers = lambda: gia
        M._kiem_song = lambda h: (False, "credential BỊ TỪ CHỐI (INERT)")
        ra = []
        M._in = lambda *a: ra.append(" ".join(str(x) for x in a))
        rc = M.cmd_kiem(argparse.Namespace(codex_home=str(home), kiem_song=True))
        assert rc == M.RC[M.DO], f"rc {rc}"
        assert any("KHÔNG ghi được trạng thái chờ snapshot" in x for x in ra), f"lỗi ghi bị nuốt: {ra}"


def t17_token_invalidated_la_tu_choi_va_thang_rc0(M):
    """wp484 g7 (Codex lượt 1 F02) — hồi quy so master: `token_invalidated` phải là TỪ CHỐI, kể cả
    khi rc=0 và stdout có dấu hiệu sống."""
    ok, vi_sao = kiem_song_bang_codex_gia(M, rc=1, loi="error: token_invalidated")
    assert not ok and "TỪ CHỐI (token_invalidated)" in vi_sao, vi_sao
    ok, vi_sao = kiem_song_bang_codex_gia(M, rc=0, ra=f"{M.DAU_HIEU_SONG}\n", loi="token_invalidated")
    assert not ok and "TỪ CHỐI" in vi_sao, f"rc0 + marker che mất từ chối: {vi_sao}"


def t18_kiem_ghi_dung_ban_da_probe(M):
    """wp484 g7 (Codex lượt 1 F03) qua `cmd_kiem` thật: probe từ chối A trong lúc B được ghi ⇒
    A vào lịch sử, B không bị chặn."""
    import argparse
    import json as _json
    with tempfile.TemporaryDirectory(prefix="codex-f03-") as td:
        home = Path(td) / "codex"
        h = M._repo_helpers()
        a = _json.dumps({"tokens": {"refresh_token": "INERT-A"}}).encode()
        b = _json.dumps({"tokens": {"refresh_token": "INERT-B"}}).encode()
        with h["_KhoCodex"](home, create=True) as store:
            store.write("auth.json", a, None)
        def kiem_song(hm):
            with h["_KhoCodex"](hm) as st:
                st.write("auth.json", b, a)
            return False, "credential BỊ TỪ CHỐI (INERT)"
        M._kiem_song = kiem_song
        M._repo_helpers = lambda: h
        M._in = lambda *x: None
        M.cmd_kiem(argparse.Namespace(codex_home=str(home), kiem_song=True))
        with h["_KhoCodex"](home) as store:
            rejected, _ = h["_doc_rejected"](store)
        assert h["_credential_id"](a) in rejected, "A không vào lịch sử"
        assert h["_credential_id"](b) not in rejected, "B bị ghi nhầm"
        assert not h["_dang_cho_snapshot"](home), "B bị chặn oan"


CA = [t1_doc_duoc_url_va_ma_tu_dau_ra_that, t2_chua_thay_thi_tra_None_khong_doan,
      t3_kiem_song_doi_DAU_HIEU_khong_tin_rc0, t4_kiem_song_bat_credential_bi_tu_choi,
      t5_kiem_song_dat_khi_co_dau_hieu, t6_khong_in_gia_tri_khi_khong_co_co,
      t7_sao_luu_khong_de_ban_cu, t8_thieu_codex_la_KHONG_DO_DUOC_khong_phai_DAT,
      t9_cmd_lay_GHI_tep_huong_dan_dan, t10_gio_con_lai_doc_exp_va_bu_padding,
      t11_sao_luu_tu_choi_symlink, t12_sao_luu_O_NOFOLLOW_tai_diem_doc,
      t13_sao_luu_fail_closed_khi_thieu_O_NOFOLLOW, t14_probe_khong_ke_thua_snapshot,
      t15_home_chua_tao_la_KHONG_DO_DUOC, t16_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra,
      t17_token_invalidated_la_tu_choi_va_thang_rc0, t18_kiem_ghi_dung_ban_da_probe]

# ─────────────────────────── đột biến ───────────────────────────
# (nhãn, chuỗi CŨ, chuỗi MỚI, ca ĐÍCH phải chết)
DOT_BIEN = [
    ("t14_probe_ke_thua_snapshot",
     '    moi.pop("CODEX_AUTH_JSON", None)\n    try:\n        with open(os.devnull)',
     '    try:\n        with open(os.devnull)',
     "t14_probe_khong_ke_thua_snapshot"),
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
    ("t3_tin_rc0", 'if DAU_HIEU_SONG not in stdout:', 'if False:',
     "t3_kiem_song_doi_DAU_HIEU_khong_tin_rc0"),
    ("t4_bo_dau_hieu_tu_choi", '"please log in again", "could not be refreshed"):',
     '"please log in again",):' + "\n" + " " * 8 + 'dau = "\\x00khong-bao-gio-khop"',
     "t4_kiem_song_bat_credential_bi_tu_choi"),
    ("t5_bo_dieu_kien_rc0", "if p.returncode != 0:", "if False:",
     "t5_kiem_song_dat_khi_co_dau_hieu"),
    ("t6_in_bi_mat_luon", "if a.in_gia_tri:", "if True:",
     "t6_khong_in_gia_tri_khi_khong_co_co"),
    # Gỡ O_EXCL ⇒ tên vừa bị giữ bị mở+truncate thay vì thử tên kế tiếp.
    ("t7_bo_mo_doc_quyen", "os.O_CREAT | os.O_EXCL | os.O_TRUNC",
     "os.O_CREAT | os.O_TRUNC",
     "t7_sao_luu_khong_de_ban_cu"),
    # Gỡ hẳn bước sinh tệp: đúng bệnh "làm tay rồi lần sau quên".
    # Bỏ TRỌN khối sinh tệp (cả write_text lẫn chmod). Bản trước chỉ bỏ write_text nên
    # `os.chmod` phía sau ném FileNotFoundError và giết luôn t6 — đó là đột biến làm hỏng
    # HÀM cho mọi ca, không phải đột biến đo đúng tính chất t9 canh.
    ("t9_khong_sinh_tep_dan",
     '    _ghi_bi_mat(tep_dan, soan_tep_dan(\n'
     '        b64, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), gio_con).encode("utf-8"))',
     "    pass", "t9_cmd_lay_GHI_tep_huong_dan_dan"),
    # Bỏ bù padding base64url — ca t10 phải ĐỎ, và đây là lỗi thật rất dễ lọt.
    ("t10_khong_bu_padding", '\n    than += "=" * (-len(than) % 4)', "",
     "t10_gio_con_lai_doc_exp_va_bu_padding"),
    ("t8_thieu_cong_cu_van_xanh", "return RC[KHONG_DO_DUOC]\n\n    tam_ctx =",
     "return RC[DAT]\n\n    tam_ctx =", "t8_thieu_codex_la_KHONG_DO_DUOC_khong_phai_DAT"),
    ("t11_bo_tu_choi_symlink",
     '    if dich.is_symlink():\n'
     '        raise OSError(f"từ chối sao lưu qua symlink: {dich}")\n', "",
     "t11_sao_luu_tu_choi_symlink"),
    ("t12_bo_O_NOFOLLOW", 'os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)', "os.O_RDONLY",
     "t12_sao_luu_O_NOFOLLOW_tai_diem_doc"),
    ("t13_bo_fail_closed",
     '    if not hasattr(os, "O_NOFOLLOW"):\n'
     '        raise OSError("từ chối sao lưu: nền thiếu os.O_NOFOLLOW")\n', "",
     "t13_sao_luu_fail_closed_khi_thieu_O_NOFOLLOW"),
    ("t15_bo_nhanh_home_vang", "    if not os.path.lexists(home):\n", "    if False:\n",
     "t15_home_chua_tao_la_KHONG_DO_DUOC"),
    ("t16_nuot_loi_ghi", '        if not helpers["_danh_dau_auth_hong"](home, raw):', "        if False:",
     "t16_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra"),
    ("t17_bo_token_invalidated", '"refresh_token_invalidated", "token_invalidated", "401 unauthorized",',
     '"refresh_token_invalidated", "401 unauthorized",', "t17_token_invalidated_la_tu_choi_va_thang_rc0"),
    ("t18_doc_lai_sau_probe", 'helpers["_danh_dau_auth_hong"](home, raw)', 'helpers["_danh_dau_auth_hong"](home)',
     "t18_kiem_ghi_dung_ban_da_probe"),
]


def ten_do(ten: str, e: BaseException, ca=None) -> str:
    """#1079 F01: tên ghi vào tập đỏ — lỗi vô can mang `(<Loại>)` nên không khớp `phai_chet`.
    F05 (Codex lượt 2): chốt sinh BÊN TRONG một ca đã đăng ký KHÁC mang `(chot cua ca khac)`."""
    if not la_chot_cua_suite(e):
        return f"{ten}({type(e).__name__})"
    # F08 (Codex lượt 3): ca cùng factory có chung `__code__` — mã của CHÍNH ca đích không phải "ca khác".
    khac = ({c.__code__ for c in CA if c is not ca} - {ca.__code__}) if ca is not None else set()
    tb = e.__traceback__
    while tb is not None:
        if tb.tb_frame.f_code in khac:
            return f"{ten}(chot cua ca khac)"
        tb = tb.tb_next
    return ten


def chay_suite(M, chi_chay: set[str] | None = None) -> set[str]:
    """Chạy toàn bộ hoặc đúng `chi_chay`, trả tập tên ca ĐỎ.

    #1079 F01: ca đỏ vì lỗi VÔ CAN (không qua `la_chot_cua_suite`) mang tên
    `<ca>(<Loại>)`, nên không bao giờ khớp `phai_chet` — tín dụng giả, không phải giết."""
    do = set()
    for ca in CA:
        if chi_chay is not None and ca.__name__ not in chi_chay:
            continue
        # module nạp lại mỗi ca: các ca vá I/O/`_co_codex` lên module,
        # không cô lập thì ca sau ăn bản vá của ca trước và bán kính đo ra sai.
        Mi = nap(M.__nguon__, M.__nhan__)
        Mi.__nguon__, Mi.__nhan__ = M.__nguon__, M.__nhan__
        try:
            ca(Mi)
        except Exception as e:
            do.add(ten_do(ca.__name__, e, ca))
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
    print("ĐỘT BIẾN — bán kính CHỈ đo trong phạm vi phai_chet:")
    xau = []
    for nhan, cu, moi, dich in DOT_BIEN:
        if goc.count(cu) != 1:
            print(f"  ĐỎ  {nhan}: mỏ neo xuất hiện {goc.count(cu)} lần, cần đúng 1")
            xau.append(nhan)
            continue
        nguon_m = goc.replace(cu, moi, 1)
        try:
            Mm = nap(nguon_m, nhan)
        except SyntaxError as e:
            # Một đột biến không biên dịch được thì KHÔNG chạy, nên nó không đo gì —
            # phải báo ĐỎ tại đây chứ không được làm sập cả lượt và che mọi đột biến sau.
            print(f"  ĐỎ  {nhan:26} KHÔNG BIÊN DỊCH ĐƯỢC: {e}")
            xau.append(f"{nhan}: đột biến không parse — không phải đột biến")
            continue
        Mm.__nguon__, Mm.__nhan__ = nguon_m, nhan
        phai_chet = {dich}
        chet = chay_suite(Mm, phai_chet)
        ok = chet == phai_chet
        print(f"  {'ok ' if ok else 'ĐỎ '} {nhan:26} giết {len(chet)}/{len(phai_chet)}"
              " trong phai_chet")
        if not ok:
            xau.append(f"{nhan}: chết {sorted(chet)}, phải chết {sorted(phai_chet)}")

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
