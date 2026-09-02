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


def cai_provider_gia(M):
    """Use an inert typed-capability adapter; individual cases control `_co_codex`."""
    class Bound:
        def __init__(self, executable):
            self.executable = Path(executable)
            self.sanitized_path = str(self.executable.parent)

    def bind(_source=None):
        executable = M._co_codex()
        if not executable:
            raise M._ProviderExecutableError("provider_executable_missing")
        return Bound(executable)

    M._bind_codex = bind
    M._provider_argv = lambda bound, arguments: [
        str(bound.executable), *map(str, arguments)]
    M._bound_provider_source = lambda source, bound: {
        **dict(source), "PATH": bound.sanitized_path}


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
            # These cases measure Codex response classification, not the
            # platform's directory-relative secret primitives.
            M._shared_checked_secret_destination = (
                lambda path, *, create_parent=True: Path(path))
            M._shared_read_secret_bytes = lambda _path: b'{"tokens":{"refresh_token":"FIXTURE"}}'
            with M._shared_private_provider_home() as provider_home:
                return M._kiem_song(provider_home)
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
    result = kiem_song_bang_codex_gia(M)
    assert result.status is M.LiveStatus.NOT_MEASURED, "rc=0 + đầu ra rỗng mà vẫn báo SỐNG"
    assert "dấu hiệu sống" in result.reason, result.reason
    assert kiem_song_bang_codex_gia(
        M, loi=f"echo prompt {M.DAU_HIEU_SONG}").status is M.LiveStatus.NOT_MEASURED, \
        "tin dấu hiệu bị echo ở stderr"


def t4_kiem_song_bat_credential_bi_tu_choi(M):
    result = kiem_song_bang_codex_gia(
        M, ra=M.DAU_HIEU_SONG, loi="error: refresh_token_invalidated")
    assert result.status is M.LiveStatus.REJECTED, "có dấu hiệu bị từ chối mà vẫn báo SỐNG"
    assert "TỪ CHỐI" in result.reason, result.reason


def t5_kiem_song_dat_khi_co_dau_hieu(M):
    # Chiều BẮT OAN: đủ điều kiện thì phải ĐẠT, không cảnh báo thừa.
    assert kiem_song_bang_codex_gia(
        M, rc=7, ra=f"{M.DAU_HIEU_SONG}\n").status is M.LiveStatus.NOT_MEASURED, \
        "rc!=0 mà vẫn báo SỐNG"
    result = kiem_song_bang_codex_gia(M, ra=f"{M.DAU_HIEU_SONG}\n")
    assert result.status is M.LiveStatus.PASSED, "đầu ra có dấu hiệu sống mà vẫn báo CHẾT"


def gia_kiem_song_dat(M, reason="rc=0, có dấu hiệu"):
    result = M.LiveResult(M.LiveStatus.PASSED, reason)
    M._kiem_song = lambda *_a, **_k: result
    M._kiem_song_checked = lambda *_a, **_k: result


def t6_khong_in_gia_tri_khi_khong_co_co(M, capsys=None):
    """Mặc định KHÔNG được in base64 ra màn hình."""
    bi_mat = b'{"tokens":{"refresh_token":"BIMAT-KHONG-DUOC-IN"}}'
    d = Path(tempfile.mkdtemp())
    M._co_codex = lambda: "/gia/codex"
    def device_auth(home, _han, _bound):
        (home / "auth.json").write_bytes(bi_mat)
        return (True, "ok")
    M._chay_device_auth = device_auth
    gia_kiem_song_dat(M)
    ra_tep = d / "b64.txt"
    vat_giu = d / "khong-duoc-doi.txt"
    vat_giu.write_text("GIU-NGUYEN")
    os.link(vat_giu, ra_tep)  # ghi tại chỗ sẽ sửa cả hardlink; replace nguyên tử thì không

    class A:
        codex_home, ra, han_giay = str(d / "CALLER-MUST-NOT-CONTROL"), str(ra_tep), 5
        in_gia_tri, cai_de = False, False
        tep_dan = None          # argparse thật LUÔN có trường này; đồ giả phải giống thật.

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
    assert vat_giu.read_text() == "GIU-NGUYEN", "ghi đè tại chỗ làm đổi inode dùng chung"
    doi_tep_kin(ra_tep, "tệp bí mật không phải 0600")

    homes = []
    def dang_nhap_tam(home, _han, _bound):
        homes.append(home); (home / "auth.json").write_bytes(bi_mat)
        return (True, "ok")
    M._chay_device_auth = dang_nhap_tam
    class B(A):
        codex_home, ra, tep_dan = None, str(d / "b64-2.txt"), str(d / "setup-2.md")
    with redirect_stdout(io.StringIO()):
        assert M.cmd_lay(B()) == 0
    assert homes and not homes[0].exists(), "CODEX_HOME tạm còn giữ raw credential sau khi xong"
    assert all(home != Path(A.codex_home) for home in homes), "caller redirected device-auth storage"
    assert not Path(A.codex_home).exists(), "caller-owned CODEX_HOME was touched"


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
    def device_auth(home, _han, _bound):
        (home / "auth.json").write_bytes(bi_mat)
        return (True, "ok")
    M._chay_device_auth = device_auth
    gia_kiem_song_dat(M, "rc=0")
    tep_dan = d / "huong_dan.md"

    class A:
        codex_home, ra, han_giay = str(d), str(d / "b64.txt"), 5
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
    M._shared_checked_secret_destination = (
        lambda path, *, create_parent=True: Path(path))
    M._shared_read_secret_bytes = lambda path: Path(path).read_bytes()
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
    d = Path(tempfile.mkdtemp())
    nguon, dich = d / "bi-mat.json", d / "auth.json"
    nguon.write_text("BI-MAT")
    try:
        dich.symlink_to(nguon)
    except (OSError, NotImplementedError):
        print("  BỎ QUA symlink thật; nền không cho tạo — đo guard bằng symlink giả")
        class SymlinkGia:
            def is_symlink(self): return True
            def is_file(self): return False
            def __str__(self): return str(dich)
        dich = SymlinkGia()
    try:
        M._sao_luu(dich)
    except OSError:
        pass
    else:
        raise AssertionError("_sao_luu không từ chối đích là symlink")
    assert nguon.read_text() == "BI-MAT", "đã sửa nguồn mà symlink trỏ tới"


def t12_sao_luu_O_NOFOLLOW_tai_diem_doc(M):
    d = Path(tempfile.mkdtemp())
    dich = d / "auth.json"
    dich.write_text("AN-TOAN")
    seen = []
    def capability_read(path):
        seen.append(Path(path))
        raise OSError("actual parent capability changed")
    M._shared_read_secret_bytes = capability_read
    try:
        M._sao_luu(dich)
    except OSError:
        pass
    else:
        raise AssertionError("đổi nguồn thành symlink giữa check/use mà vẫn sao lưu")
    assert seen == [dich.resolve()], "backup bypassed the shared capability reader"
    assert not list(d.glob("*.bak-*")), "đã tạo backup sau khi source read bị từ chối"


def t13_sao_luu_fail_closed_khi_thieu_O_NOFOLLOW(M):
    d = Path(tempfile.mkdtemp())
    dich = d / "auth.json"
    dich.write_text("AN-TOAN")
    real_reader = M._shared_read_secret_bytes
    M._shared_read_secret_bytes = lambda _path: (_ for _ in ()).throw(
        OSError("handle-relative read unavailable"))
    try:
        M._sao_luu(dich)
        raise AssertionError("missing capability reader did not fail closed")
    except OSError:
        pass
    assert not list(d.glob("*.bak-*")), "đã tạo .bak trước khi fail-closed"
    M._shared_read_secret_bytes = real_reader
    bak = M._sao_luu(dich)
    assert bak and bak.read_text() == "AN-TOAN", "chặn oan nền có O_NOFOLLOW"


def t14_cmd_lay_tu_choi_dich_trong_repository_truoc_device_auth(M):
    repo = GOC.resolve().parents[2]
    with tempfile.TemporaryDirectory() as sd, \
         tempfile.TemporaryDirectory(prefix="codex-cred-repo-", dir=repo) as rd:
        source = Path(sd)
        repo_slot = Path(rd)
        (source / "auth.json").write_text(
            '{"tokens":{"access_token":"a.b.c","refresh_token":"FIXTURE"}}',
            encoding="utf-8")
        spawned = []
        M._co_codex = lambda: "/gia/codex"
        def device_auth(home, _timeout, _bound):
            spawned.append(True)
            (home / "auth.json").write_text(
                '{"tokens":{"access_token":"a.b.c","refresh_token":"FIXTURE"}}',
                encoding="utf-8")
            return (True, "ok")
        M._chay_device_auth = device_auth
        gia_kiem_song_dat(M, "rc=0")
        import io
        from contextlib import redirect_stdout
        linked_parent = source / "linked-repository-parent"
        try:
            linked_parent.symlink_to(repo_slot, target_is_directory=True)
        except OSError:
            linked_parent = None

        cases = [
            ("--ra direct", str(source), str(repo_slot / "b64.txt"), None, False, None),
            ("--tep-dan direct", str(source), str(source / "b64.txt"),
             str(repo_slot / "setup.md"), False, None),
            ("--cai-de direct", str(source), str(source / "b64.txt"),
             str(source / "setup.md"), True, repo_slot / "installed-home"),
        ]
        if linked_parent is not None:
            cases.append(("parent symlink", str(source), str(linked_parent / "linked.b64"),
                          str(source / "setup.md"), False, None))

        original_effective_home = M.effective_codex_home
        try:
            for name, codex_home, ra, tep_dan, cai_de, install_home in cases:
                spawned.clear()
                M.effective_codex_home = (lambda p=install_home: p) \
                    if install_home is not None else original_effective_home

                class A:
                    han_giay, in_gia_tri = 5, False

                args = A()
                args.codex_home, args.ra, args.tep_dan = codex_home, ra, tep_dan
                args.cai_de = cai_de
                with redirect_stdout(io.StringIO()):
                    rc = M.cmd_lay(args)
                assert rc == M.RC[M.DO], f"{name}: đích trong repository phải ĐỎ, rc={rc}"
                assert not spawned, f"{name}: đã chạy device-auth trước destination guard"
        finally:
            M.effective_codex_home = original_effective_home
        assert not list(repo_slot.rglob("*.b64")), "đã ghi credential vào repository"
        assert not (repo_slot / "setup.md").exists(), "đã ghi tệp dán vào repository"
        assert not (repo_slot / "installed-home" / "auth.json").exists(), \
            "đã cài credential vào repository"


def t15_cmd_lay_phai_dung_duong_canonical_guard_tra_ve(M):
    """Preflight is not advisory: every later operation uses its returned path."""
    root = Path(tempfile.mkdtemp(prefix="codex-canonical-"))
    caller_home = root / "caller-home"
    alias_b64, real_b64 = root / "alias.b64", root / "real.b64"
    alias_setup, real_setup = root / "alias.md", root / "real.md"
    mapping = {
        alias_b64: real_b64,
        alias_setup: real_setup,
    }
    checked = M._shared_checked_secret_destination
    guard_calls = []
    underlying_calls = []

    def canonical_guard(path, *, create_parent=True):
        path = Path(path)
        guard_calls.append((path, create_parent))
        if path in mapping:
            # Mapping models a canonical capability returned by the guard.  Do
            # not evaluate the real guard as an eager ``dict.get`` fallback:
            # touching the unchecked alias would defeat this fixture's seam.
            return mapping[path]
        underlying_calls.append((path, create_parent))
        return checked(path, create_parent=create_parent)

    M._shared_checked_secret_destination = canonical_guard
    homes = []
    M._co_codex = lambda: "/gia/codex"
    def device_auth(home, _timeout, _bound):
        homes.append(Path(home))
        (home / "auth.json").write_text(
            '{"tokens":{"access_token":"a.b.c","refresh_token":"FIXTURE"}}',
            encoding="utf-8")
        return (True, "ok")
    M._chay_device_auth = device_auth
    gia_kiem_song_dat(M, "rc=0")

    class A:
        codex_home, ra, tep_dan = str(caller_home), str(alias_b64), str(alias_setup)
        han_giay, in_gia_tri, cai_de = 5, False, False

    import io
    from contextlib import redirect_stdout
    with redirect_stdout(io.StringIO()):
        rc = M.cmd_lay(A())
    assert rc == M.RC[M.DAT], f"canonical destinations not honored, rc={rc}"
    assert len(homes) == 1 and homes[0] != caller_home and not homes[0].exists(), \
        f"device auth storage was not process-private: {homes}"
    assert not caller_home.exists(), "caller-owned CODEX_HOME was touched"
    assert real_b64.is_file() and real_setup.is_file(), "outputs missed canonical targets"
    assert not alias_b64.exists() and not alias_setup.exists(), "writer reused unchecked aliases"
    private_auth = homes[0] / "auth.json"
    assert (private_auth, False) in guard_calls, \
        f"post-login auth recheck was allowed to create parents: {guard_calls}"
    assert (alias_b64, True) in guard_calls and (alias_setup, True) in guard_calls, \
        f"output aliases did not pass through the canonical guard: {guard_calls}"
    assert all(path not in mapping for path, _create_parent in underlying_calls), \
        f"canonical mapping evaluated the unchecked alias eagerly: {underlying_calls}"


def t16_cmd_lay_phan_loai_tu_choi_tai_diem_ghi(M):
    root = Path(tempfile.mkdtemp(prefix="codex-use-time-"))
    (root / "auth.json").write_text(
        '{"tokens":{"access_token":"a.b.c","refresh_token":"FIXTURE"}}',
        encoding="utf-8")
    M._co_codex = lambda: "/gia/codex"
    def device_auth(home, _timeout, _bound):
        (home / "auth.json").write_text(
            '{"tokens":{"access_token":"a.b.c","refresh_token":"FIXTURE"}}',
            encoding="utf-8")
        return (True, "ok")
    M._chay_device_auth = device_auth
    gia_kiem_song_dat(M, "rc=0")

    class A:
        codex_home, ra, tep_dan = str(root), str(root / "out.b64"), str(root / "setup.md")
        han_giay, in_gia_tri, cai_de = 5, False, False

    import io
    from contextlib import redirect_stdout
    for error, expected in ((M._UnsafeSecretDestination("parent changed"), M.RC[M.DO]),
                            (OSError("disk lookup failed"), M.RC[M.KHONG_DO_DUOC])):
        M._ghi_bi_mat = lambda *_a, _error=error: (_ for _ in ()).throw(_error)
        with redirect_stdout(io.StringIO()):
            rc = M.cmd_lay(A())
        assert rc == expected, f"use-time {type(error).__name__} mapped to rc={rc}"


def t17_lay_khong_con_codex_home_va_windows_fail_closed(M):
    try:
        M.build_parser().parse_args(["lay", "--codex-home", "CALLER-DIRECTED"])
        raise AssertionError("lay still accepts caller-directed --codex-home")
    except SystemExit as exc:
        assert exc.code == 2
    root = Path(tempfile.mkdtemp(prefix="codex-private-home-"))
    ambient = root / "caller-temp"; ambient.mkdir()
    spawned = []
    private_homes = []
    real_private_home = M._shared_private_provider_home
    from contextlib import contextmanager
    @contextmanager
    def process_private_home():
        with real_private_home() as home:
            private_homes.append(Path(home))
            yield home
    M._shared_private_provider_home = process_private_home
    M._co_codex = lambda: "/gia/codex"
    def device_auth(home, _timeout, _bound):
        spawned.append(Path(home))
        (home / "auth.json").write_text(
            '{"tokens":{"access_token":"a.b.c","refresh_token":"FIXTURE"}}')
        return (True, "ok")
    M._chay_device_auth = device_auth
    gia_kiem_song_dat(M, "rc=0")
    class A:
        codex_home = str(root / "CALLER-DIRECTED")
        ra, tep_dan = str(root / "out.b64"), str(root / "setup.md")
        han_giay, in_gia_tri, cai_de = 5, False, False
    import io
    from contextlib import redirect_stdout
    old_temp = {key: os.environ.get(key) for key in ("TMPDIR", "TMP", "TEMP")}
    try:
        os.environ.update({key: str(ambient) for key in old_temp})
        with redirect_stdout(io.StringIO()):
            rc = M.cmd_lay(A())
    finally:
        for key, value in old_temp.items():
            if value is None: os.environ.pop(key, None)
            else: os.environ[key] = value
    assert len(private_homes) == 1
    assert ambient.resolve() not in (private_homes[0].resolve(strict=False),
                                     *private_homes[0].resolve(strict=False).parents), \
        f"device-auth storage followed ambient temp selection: {private_homes}"
    if os.name == "nt":
        assert rc == M.RC[M.KHONG_DO_DUOC]
        assert not spawned, "Windows fail-close happened after device-auth spawn"
    else:
        assert rc == M.RC[M.DAT]
        assert len(spawned) == 1 and spawned[0] != Path(A.codex_home)
        assert not spawned[0].exists(), "process-private raw auth was not destroyed"
    assert not Path(A.codex_home).exists(), "caller-owned CODEX_HOME was touched"


def t18_kiem_song_CODEX_HOME_thuong_dung_provider_home_rieng(M):
    """Live check keeps credentials in CODEX_HOME and all other state elsewhere."""
    from contextlib import contextmanager

    root = Path(tempfile.mkdtemp(prefix="codex-live-split-"))
    codex_home = root / "credentials"
    codex_home.mkdir(mode=0o700)
    (codex_home / "auth.json").write_text(
        '{"tokens":{"access_token":"a.b.c","refresh_token":"FIXTURE"}}',
        encoding="utf-8")
    fake = root / "fake"
    fake.mkdir()
    (fake / "exec").write_text(
        "import sys\n"
        f"sys.stdout.write({(M.DAU_HIEU_SONG + chr(10))!r})\n",
        encoding="utf-8")

    real_private_home = M._shared_private_provider_home
    real_child_env = M._shared_provider_child_env
    private_roots = []
    child_envs = []

    @contextmanager
    def observed_private_home():
        with real_private_home() as home:
            private_roots.append(Path(home).parent)
            yield home

    def observed_child_env(source, home, **required):
        env = real_child_env(source, home, **required)
        child_envs.append(dict(env))
        return env

    M._shared_private_provider_home = observed_private_home
    M._shared_provider_child_env = observed_child_env
    M._co_codex = lambda: sys.executable
    if os.name == "nt":
        # This case measures the split between credential storage and provider
        # storage. Windows capability fail-close is covered by t19; inject the
        # already-validated auth capability so the positive control can run.
        M._shared_checked_secret_destination = (
            lambda path, *, create_parent=True: Path(path))
        M._shared_read_secret_bytes = lambda path: Path(path).read_bytes()
    old_cwd = os.getcwd()
    isolated_keys = ("CODEX_AUTH_JSON", "CLAUDE_CODE_OAUTH_TOKEN", "GITHUB_PAT",
                     "TL_MASTER_KEY", "TMPDIR", "TMP", "TEMP")
    old_env = {key: os.environ.get(key) for key in isolated_keys}
    ambient = root / "ambient-temp"
    ambient.mkdir()
    try:
        os.chdir(fake)
        os.environ.update({
            "CODEX_AUTH_JSON": "AMBIENT-CODEX",
            "CLAUDE_CODE_OAUTH_TOKEN": "AMBIENT-CLAUDE",
            "GITHUB_PAT": "AMBIENT-GITHUB",
            "TL_MASTER_KEY": "AMBIENT-TL",
            "TMPDIR": str(ambient), "TMP": str(ambient), "TEMP": str(ambient),
        })
        result = M._kiem_song(codex_home)
    finally:
        os.chdir(old_cwd)
        for key, value in old_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    assert result.status is M.LiveStatus.PASSED, \
        f"ordinary CODEX_HOME required provider scaffold: {result.reason}"
    assert len(private_roots) == 1 and len(child_envs) == 1, \
        f"live check did not allocate exactly one private provider context: {private_roots}"
    private_root, child = private_roots[0], child_envs[0]
    assert Path(child["CODEX_HOME"]) == codex_home, child
    for key in ("HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_DATA_HOME",
                "XDG_STATE_HOME", "TMPDIR", "TMP", "TEMP"):
        path = Path(child[key])
        assert path == private_root or private_root in path.parents, \
            f"{key} escaped private provider context: {path} vs {private_root}"
    assert Path(child["HOME"]) != codex_home, "credential directory reused as provider HOME"
    assert ambient != private_root and ambient not in private_root.parents, \
        f"private provider context followed ambient temp: {private_root}"
    for key in ("CODEX_AUTH_JSON", "CLAUDE_CODE_OAUTH_TOKEN", "GITHUB_PAT", "TL_MASTER_KEY"):
        assert key not in child, f"ambient credential leaked into Codex live check: {key}"
    assert not private_root.exists(), "private provider context survived live-check cleanup"
    assert sorted(path.name for path in codex_home.iterdir()) == ["auth.json"], \
        "live check scaffolded HOME/XDG/TMP inside ordinary CODEX_HOME"

    # Allocation/validation refusal is still before subprocess start.
    child_started = []

    @contextmanager
    def unavailable_private_home():
        raise OSError("fixture private provider storage unavailable")
        yield  # pragma: no cover - makes this a contextmanager

    M._shared_private_provider_home = unavailable_private_home
    real_subprocess_run = M.subprocess.run
    M.subprocess.run = lambda *_a, **_k: child_started.append(True)
    try:
        result = M._kiem_song(codex_home)
    finally:
        M.subprocess.run = real_subprocess_run
    assert result.status is M.LiveStatus.NOT_MEASURED \
        and "provider storage" in result.reason, result
    assert child_started == [], "live check spawned before private provider allocation passed"


def _gia_tri_trang_thai_song(result):
    """Read old/new shapes so a RED reports behavior, not a missing test helper."""
    status = result.status if hasattr(result, "status") else result[0]
    return getattr(status, "value", status)


def t19_kiem_song_guard_dich_truoc_doc_cap_phat_va_child(M):
    """Repository aliases stop before read/provider/child; canonical auth is reused."""
    from contextlib import contextmanager
    import subprocess as _sp
    from types import SimpleNamespace

    repository = GOC.resolve().parents[2]
    events = []

    @contextmanager
    def forbidden_provider():
        events.append("provider")
        raise AssertionError("provider allocated before Codex destination guard")
        yield  # pragma: no cover - contextmanager shape only

    M._co_codex = lambda: sys.executable
    M._shared_private_provider_home = forbidden_provider
    with tempfile.TemporaryDirectory(prefix="codex-direct-repo-", dir=repository) as raw_repo:
        direct_home = Path(raw_repo)
        (direct_home / "auth.json").write_text(
            '{"tokens":{"refresh_token":"FIXTURE_ONLY"}}', encoding="utf-8")
        result = M._kiem_song(direct_home)
        assert _gia_tri_trang_thai_song(result) == "rejected", result
        assert events == [], f"repository destination consumed resources first: {events}"

    # Parent link/junction resolving into the repository has the same ordering.
    with tempfile.TemporaryDirectory(prefix="codex-guard-link-") as raw:
        root = Path(raw)
        linked = root / "linked-repository"
        if os.name == "nt":
            made = _sp.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(linked), str(repository)],
                stdin=_sp.DEVNULL, capture_output=True).returncode == 0
        else:
            linked.symlink_to(repository, target_is_directory=True)
            made = True
        assert made, "could not construct required parent link/junction fixture"
        result = M._kiem_song(linked / "CODEX-HOME")
        assert _gia_tri_trang_thai_song(result) == "rejected", result
        assert events == [], f"linked repository destination consumed resources first: {events}"

    # A benign alias must be replaced by the one canonical identity returned by
    # the shared guard before the credential read, provider allocation, or child.
    with tempfile.TemporaryDirectory(prefix="codex-guard-order-") as raw:
        root = Path(raw)
        alias_home = root / "alias-home"
        canonical_home = root / "canonical-home"
        canonical_auth = canonical_home / "auth.json"
        provider_home = root / "provider-root" / "home"
        provider_home.mkdir(parents=True)

        def checked(path, *, create_parent=True):
            events.append(("guard", Path(path), create_parent))
            return canonical_auth

        def read_secret(path):
            events.append(("read", Path(path)))
            return b'{"tokens":{"refresh_token":"FIXTURE_ONLY"}}'

        class Bound:
            executable = Path(sys.executable)
            sanitized_path = str(Path(sys.executable).parent)

        def bind_codex(_source=None):
            events.append("bind")
            return Bound()

        @contextmanager
        def observed_provider():
            events.append("provider")
            yield provider_home

        def child_env(_source, _provider_home, **required):
            events.append(("env", dict(required)))
            return {"CODEX_HOME": required["CODEX_HOME"]}

        def child_run(*_args, **kwargs):
            events.append(("child", kwargs["env"]["CODEX_HOME"]))
            return SimpleNamespace(returncode=0, stdout=M.DAU_HIEU_SONG + "\n", stderr="")

        events.clear()
        M._shared_checked_secret_destination = checked
        M._bind_codex = bind_codex
        M._shared_read_secret_bytes = read_secret
        M._shared_private_provider_home = observed_provider
        M._shared_provider_child_env = child_env
        M.subprocess.run = child_run
        result = M._kiem_song(alias_home)
        assert _gia_tri_trang_thai_song(result) == "passed", result
        assert events == [
            ("guard", alias_home / "auth.json", False),
            "bind",
            ("read", canonical_auth),
            "provider",
            ("env", {"CODEX_HOME": str(canonical_home)}),
            ("child", str(canonical_home)),
        ], f"guard/read/provider/child order or canonical identity drifted: {events}"


def t20_kiem_song_ba_trang_thai_dong_va_caller_khong_truthiness(M):
    """Only evidenced refusal is rejected; both callers preserve all 3 statuses."""
    from contextlib import contextmanager, redirect_stdout
    from types import SimpleNamespace
    import io

    root = Path(tempfile.mkdtemp(prefix="codex-live-status-"))
    auth = root / "auth.json"
    auth_bytes = b'{"last_refresh":"fixture","tokens":{"refresh_token":"FIXTURE_ONLY"}}'
    auth.write_bytes(auth_bytes)
    provider_home = root / "provider" / "home"
    provider_home.mkdir(parents=True)

    M._shared_checked_secret_destination = (
        lambda path, *, create_parent=True: auth)
    M._shared_read_secret_bytes = lambda path: auth_bytes

    @contextmanager
    def provider():
        yield provider_home

    @contextmanager
    def unavailable_provider():
        raise OSError("fixture provider unavailable")
        yield

    @contextmanager
    def cleanup_failure_provider():
        yield provider_home
        raise OSError("fixture checked cleanup failure")

    M._shared_private_provider_home = provider
    M._shared_provider_child_env = lambda *_a, **required: dict(required)

    def measure(*, cli=sys.executable, outcome=None, provider_factory=provider):
        M._co_codex = lambda: cli
        M._shared_private_provider_home = provider_factory
        if isinstance(outcome, BaseException):
            M.subprocess.run = lambda *_a, **_k: (_ for _ in ()).throw(outcome)
        else:
            M.subprocess.run = lambda *_a, **_k: outcome
        return _gia_tri_trang_thai_song(M._kiem_song(root))

    cases = {
        "missing_cli": measure(cli=None),
        "timeout": measure(outcome=M.subprocess.TimeoutExpired("codex", 1)),
        "spawn": measure(outcome=OSError("fixture spawn failure")),
        "provider": measure(outcome=None, provider_factory=unavailable_provider),
        "cleanup": measure(outcome=SimpleNamespace(
            returncode=0, stdout=M.DAU_HIEU_SONG + "\n", stderr=""),
            provider_factory=cleanup_failure_provider),
        "plain_nonzero": measure(outcome=SimpleNamespace(
            returncode=7, stdout="", stderr="upstream unavailable")),
        "marker_missing": measure(outcome=SimpleNamespace(
            returncode=0, stdout="", stderr="")),
        "refused": measure(outcome=SimpleNamespace(
            returncode=7, stdout="", stderr="401 unauthorized")),
        "passed": measure(outcome=SimpleNamespace(
            returncode=0, stdout=M.DAU_HIEU_SONG + "\n", stderr="")),
    }
    assert cases == {
        "missing_cli": "not_measured",
        "timeout": "not_measured",
        "spawn": "not_measured",
        "provider": "not_measured",
        "cleanup": "not_measured",
        "plain_nonzero": "not_measured",
        "marker_missing": "not_measured",
        "refused": "rejected",
        "passed": "passed",
    }, cases

    def live_result(value, reason="fixture"):
        if hasattr(M, "LiveResult"):
            return M.LiveResult(M.LiveStatus(value), reason)
        # Old shape makes the focused RED expose the two-state collapse.
        return (value == "passed", reason)

    # cmd_kiem must keep its missing-auth contract and must not coerce a status.
    missing = root / "missing" / "auth.json"
    M._shared_checked_secret_destination = (
        lambda path, *, create_parent=True: missing if Path(path).parent.name == "missing" else auth)
    real_read = M._shared_read_secret_bytes
    M._shared_read_secret_bytes = lambda path: (
        (_ for _ in ()).throw(FileNotFoundError(str(path)))
        if Path(path) == missing else auth_bytes)
    class MissingArgs:
        codex_home, kiem_song = str(missing.parent), True
    missing_out = io.StringIO()
    with redirect_stdout(missing_out):
        missing_rc = M.cmd_kiem(MissingArgs())
    assert missing_rc == M.RC[M.KHONG_DO_DUOC]
    assert "KHÔNG_ĐO_ĐƯỢC: không có" in missing_out.getvalue()
    M._shared_read_secret_bytes = real_read

    class CheckArgs:
        codex_home, kiem_song = str(root), True
    for value, expected in (("passed", M.RC[M.DAT]),
                            ("rejected", M.RC[M.DO]),
                            ("not_measured", M.RC[M.KHONG_DO_DUOC])):
        result = live_result(value)
        M._kiem_song = lambda *_a, _result=result, **_k: _result
        M._kiem_song_checked = lambda *_a, _result=result, **_k: _result
        with redirect_stdout(io.StringIO()):
            rc = M.cmd_kiem(CheckArgs())
        assert rc == expected, f"cmd_kiem collapsed {value} to rc={rc}"

    # Acquisition caller has the same mapping after device auth succeeds.
    M._shared_checked_secret_destination = lambda path, **_k: Path(path)
    M._shared_read_secret_bytes = lambda _path: auth_bytes
    M._chay_device_auth = lambda home, _timeout, _bound: (
        (home / "auth.json").write_bytes(auth_bytes) is not None, "ok")
    M._ghi_bi_mat = lambda *_a, **_k: None
    M._gio_con_lai = lambda _path: None
    class AcquireArgs:
        ra, tep_dan = str(root / "out.b64"), str(root / "setup.md")
        cai_de, in_gia_tri, han_giay = False, False, 5
    for value, expected in (("passed", M.RC[M.DAT]),
                            ("rejected", M.RC[M.DO]),
                            ("not_measured", M.RC[M.KHONG_DO_DUOC])):
        result = live_result(value)
        M._kiem_song = lambda *_a, _result=result, **_k: _result
        M._kiem_song_checked = lambda *_a, _result=result, **_k: _result
        with redirect_stdout(io.StringIO()):
            rc = M._cmd_lay_private(AcquireArgs(), root, M._bind_codex())
        assert rc == expected, f"_cmd_lay_private collapsed {value} to rc={rc}"

    # Checked context exit happens after the inner return expression. It must
    # still override a would-be DAT acquisition result.
    @contextmanager
    def cleanup_fails_after_inner_return():
        yield root
        raise OSError("fixture cleanup failed after return")
    M._co_codex = lambda: sys.executable
    M._shared_private_provider_home = cleanup_fails_after_inner_return
    M._shared_checked_secret_destination = lambda path, **_k: Path(path)
    M._cmd_lay_private = lambda *_a, **_k: M.RC[M.DAT]
    with redirect_stdout(io.StringIO()):
        rc = M.cmd_lay(AcquireArgs())
    assert rc == M.RC[M.KHONG_DO_DUOC], \
        f"cleanup failure after inner DAT return survived as rc={rc}"


CA = [t1_doc_duoc_url_va_ma_tu_dau_ra_that, t2_chua_thay_thi_tra_None_khong_doan,
      t3_kiem_song_doi_DAU_HIEU_khong_tin_rc0, t4_kiem_song_bat_credential_bi_tu_choi,
      t5_kiem_song_dat_khi_co_dau_hieu, t8_thieu_codex_la_KHONG_DO_DUOC_khong_phai_DAT,
      t10_gio_con_lai_doc_exp_va_bu_padding,
      t17_lay_khong_con_codex_home_va_windows_fail_closed,
      t18_kiem_song_CODEX_HOME_thuong_dung_provider_home_rieng,
      t19_kiem_song_guard_dich_truoc_doc_cap_phat_va_child,
      t20_kiem_song_ba_trang_thai_dong_va_caller_khong_truthiness]
if os.name != "nt":
    CA += [t6_khong_in_gia_tri_khi_khong_co_co, t7_sao_luu_khong_de_ban_cu,
           t9_cmd_lay_GHI_tep_huong_dan_dan, t11_sao_luu_tu_choi_symlink,
           t12_sao_luu_O_NOFOLLOW_tai_diem_doc,
           t13_sao_luu_fail_closed_khi_thieu_O_NOFOLLOW,
           t14_cmd_lay_tu_choi_dich_trong_repository_truoc_device_auth,
           t15_cmd_lay_phai_dung_duong_canonical_guard_tra_ve,
           t16_cmd_lay_phan_loai_tu_choi_tai_diem_ghi]

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
    ("t3_tin_rc0", 'if DAU_HIEU_SONG not in stdout:', 'if False:',
     "t3_kiem_song_doi_DAU_HIEU_khong_tin_rc0"),
    ("t4_bo_dau_hieu_tu_choi", "        if dau in ra.lower():",
     "        if False:",
     "t4_kiem_song_bat_credential_bi_tu_choi"),
    ("t5_bo_dieu_kien_rc0", "if p.returncode != 0:", "if False:",
     "t5_kiem_song_dat_khi_co_dau_hieu"),
    ("t6_in_bi_mat_luon", "if a.in_gia_tri:", "if True:",
     "t6_khong_in_gia_tri_khi_khong_co_co"),
    # Gỡ exclusive ⇒ tên vừa bị giữ bị replace thay vì thử tên kế tiếp.
    ("t7_bo_mo_doc_quyen", "_shared_atomic_secret(bak, noi_dung, exclusive=True)",
     "_shared_atomic_secret(bak, noi_dung, exclusive=False)",
     "t7_sao_luu_khong_de_ban_cu"),
    # Gỡ hẳn bước sinh tệp: đúng bệnh "làm tay rồi lần sau quên".
    # Bỏ TRỌN khối sinh tệp (cả write_text lẫn chmod). Bản trước chỉ bỏ write_text nên
    # `os.chmod` phía sau ném FileNotFoundError và giết luôn t6 — đó là đột biến làm hỏng
    # HÀM cho mọi ca, không phải đột biến đo đúng tính chất t9 canh.
    ("t9_khong_sinh_tep_dan",
     '        _ghi_bi_mat(tep_dan, soan_tep_dan(\n'
     '            b64, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), gio_con).encode("utf-8"))',
     "        pass", "t9_cmd_lay_GHI_tep_huong_dan_dan"),
    # Bỏ bù padding base64url — ca t10 phải ĐỎ, và đây là lỗi thật rất dễ lọt.
    ("t10_khong_bu_padding", '\n    than += "=" * (-len(than) % 4)', "",
     "t10_gio_con_lai_doc_exp_va_bu_padding"),
    ("t8_thieu_cong_cu_van_xanh",
     '        return RC[KHONG_DO_DUOC]\n\n    # Acquisition storage',
     '        return RC[DAT]\n\n    # Acquisition storage',
     "t8_thieu_codex_la_KHONG_DO_DUOC_khong_phai_DAT"),
    ("t12_backup_pathname_read",
     "    noi_dung = _shared_read_secret_bytes(dich)",
     "    noi_dung = dich.read_bytes()",
     "t12_sao_luu_O_NOFOLLOW_tai_diem_doc"),
    ("t17_caller_redirects_private_home",
     '                tam = _shared_checked_secret_destination(\n'
     '                    private_home / "auth.json").parent',
     '                tam = _shared_checked_secret_destination(\n'
     '                    Path(getattr(a, "codex_home", None) or private_home) / "auth.json").parent',
     "t17_lay_khong_con_codex_home_va_windows_fail_closed"),
    ("kiem_song_requires_private_provider_scaffold",
     "                    source, provider_home, CODEX_HOME=str(auth.parent))",
     "                    source, auth.parent, CODEX_HOME=str(auth.parent))",
     "t18_kiem_song_CODEX_HOME_thuong_dung_provider_home_rieng"),
    ("codex_kiem_song_skips_destination_guard",
     '    target = _shared_checked_secret_destination(\n'
     '        Path(codex_home).expanduser() / "auth.json", create_parent=False)\n'
     '    bound = _bind_codex()\n'
     '    return target, _shared_read_secret_bytes(target), bound',
     '    target = Path(codex_home).expanduser() / "auth.json"\n'
     '    bound = _bind_codex()\n'
     '    return target, target.read_bytes(), bound',
     "t19_kiem_song_guard_dich_truoc_doc_cap_phat_va_child"),
    ("codex_auth_recheck_recreates_parent",
     'def _bound_codex_auth(codex_home: Path):\n'
     '    """Guard destination, bind executable, then and only then read credential."""\n'
     '    target = _shared_checked_secret_destination(\n'
     '        Path(codex_home).expanduser() / "auth.json", create_parent=False)',
     'def _bound_codex_auth(codex_home: Path):\n'
     '    """Guard destination, bind executable, then and only then read credential."""\n'
     '    target = _shared_checked_secret_destination(\n'
     '        Path(codex_home).expanduser() / "auth.json", create_parent=True)',
     "t19_kiem_song_guard_dich_truoc_doc_cap_phat_va_child"),
    ("kiem_song_unmeasured_collapses_to_rejected",
     '    if result.status is LiveStatus.NOT_MEASURED:\n'
     '        return RC[KHONG_DO_DUOC]',
     '    if result.status is LiveStatus.NOT_MEASURED:\n'
     '        return RC[DO]',
     "t20_kiem_song_ba_trang_thai_dong_va_caller_khong_truthiness"),
    # Ambient temp selection moved into the shared provider allocator.  Its
    # focused lock and named mutant now live in session_credentials_test.py;
    # retaining a duplicate source mutation here would target dead ownership.
]


def chay_suite(M, chi_chay: set[str] | None = None) -> set[str]:
    """Chạy toàn bộ hoặc đúng `chi_chay`, trả tập tên ca ĐỎ."""
    do = set()
    for ca in CA:
        if chi_chay is not None and ca.__name__ not in chi_chay:
            continue
        # module nạp lại mỗi ca: các ca vá I/O/`_co_codex` lên module,
        # không cô lập thì ca sau ăn bản vá của ca trước và bán kính đo ra sai.
        Mi = nap(M.__nguon__, M.__nhan__)
        Mi.__nguon__, Mi.__nhan__ = M.__nguon__, M.__nhan__
        cai_provider_gia(Mi)
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
    print("ĐỘT BIẾN — bán kính CHỈ đo trong phạm vi phai_chet:")
    xau = []
    ten_ca = {case.__name__ for case in CA}
    dot_bien = [mutant for mutant in DOT_BIEN if mutant[3] in ten_ca
                and not (os.name == "nt" and mutant[0] ==
                         "t17_caller_redirects_private_home")]
    for nhan, cu, moi, dich in dot_bien:
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
    print(f"SỐ LIỆU:  ca {n}  ·  đột biến {len(dot_bien)}")
    if xau:
        print("TỔNG: ĐỎ")
        for x in xau:
            print(f"  - {x}")
        return 1
    print("TỔNG: ĐẠT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
