#!/usr/bin/env python3
"""Phản chứng offline cho phân loại probe và cho chính cổng đột biến."""
from __future__ import annotations
import contextlib
import errno
import importlib.util
import io
import os
import socket
import sys
import tempfile
import urllib.error
from pathlib import Path
from unittest import mock
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="backslashreplace")
sys.dont_write_bytecode = True
GOC = Path(__file__).with_name("probe_mang.py")
SO_DOT_BIEN_MONG_DOI = 5
def nap(nguon: str, nhan: str):
    with tempfile.TemporaryDirectory(prefix="pm-test-") as d:
        p = Path(d) / f"pm_{nhan}.py"
        p.write_text(nguon, encoding="utf-8")
        importlib.invalidate_caches()
        spec = importlib.util.spec_from_file_location(p.stem, p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        assert not list(Path(d).glob("__pycache__/*")), "đã ghi .pyc"
        return m
def url_loi(M, exc):
    with mock.patch.object(M.urllib.request, "urlopen", side_effect=exc):
        return M.kenh_urlopen()
def git_loi(M, stderr):
    p = mock.MagicMock(returncode=128, stderr=stderr, stdout=b"")
    with mock.patch.object(M.subprocess, "run", return_value=p):
        return M.kenh_git_ls_remote()
def t1_url_sai_cu_phap(M):
    assert M.kenh_urlopen("khong-phai-url")["lop"] == M.ENDPOINT_ERROR
def t2_dns_loi(M):
    e = urllib.error.URLError(socket.gaierror(-2, "name or service not known"))
    assert url_loi(M, e)["lop"] == M.DNS_ERROR
def t3_timeout(M):
    assert url_loi(M, TimeoutError("timeout"))["lop"] == M.TIMEOUT
def t4_path_rong(M):
    # PATH rong khong dong nghia executable vang mat tren Windows: CreateProcess van co
    # the tim git qua App Paths. Mo phong dung bien san pham that su bat.
    with mock.patch.object(M.subprocess, "run",
                           side_effect=FileNotFoundError("git")):  # probe-missing-tool
        x = M.kenh_git_ls_remote()
    assert (x["lop"], x["stage"]) == (M.TOOL_ERROR, "spawn")
def t5_kho_khong_ton_tai(M):
    x = git_loi(M, b"fatal: repository not found"); assert (x["lop"], x["rc"]) == (M.REPOSITORY_ERROR, 128)
def t6_auth_loi(M):
    x = git_loi(M, b"fatal: Authentication failed for 'https://user:secret@example.invalid/repo'")
    assert x["lop"] == M.AUTH_ERROR and "secret" not in x["raw"]
def t7_policy_denied(M):
    e = PermissionError(errno.EPERM, "Operation not permitted")
    with mock.patch.object(M.socket, "socket", side_effect=e):
        x = M.kenh_socket_loopback()
    assert (x["lop"], x["stage"]) == (M.POLICY_DENIED, "create")
def t8_giai_doan_socket(M):
    for stage in ("bind", "listen"):
        s = mock.MagicMock()
        getattr(s, stage).side_effect = PermissionError(errno.EPERM, "denied")
        with mock.patch.object(M.socket, "socket", return_value=s):
            assert M.kenh_socket_loopback()["stage"] == stage
def t9_lot_unknown(M):
    cm = mock.MagicMock()
    cm.__enter__.return_value = cm
    with mock.patch.object(M.urllib.request, "urlopen", return_value=cm):
        assert M.kenh_urlopen()["lop"] == M.LOT
    x = url_loi(M, TypeError("bug")); assert x["lop"] == M.UNKNOWN and x["raw"]
def t10_main_schema_va_fail_close(M):
    a, b, c = M.kq(M.LOT, "done"), M.kq(M.POLICY_DENIED, "create"), M.kq(M.DNS_ERROR, "urlopen")
    with mock.patch.object(M, "kenh_socket_loopback", return_value=a), \
         mock.patch.object(M, "kenh_urlopen", return_value=b), \
         mock.patch.object(M, "kenh_git_ls_remote", return_value=c):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            assert M.main() == 0
    dong = out.getvalue().splitlines()
    assert len(dong) == 3 and all(" class=" in d and " stage=" in d for d in dong)
    # Ca thu hai van phai offline: khong de socket/git that lot ra sau khi ba patch tren
    # het hieu luc.
    with mock.patch.object(M, "kenh_socket_loopback", return_value=a), \
         mock.patch.object(M, "kenh_urlopen", return_value=M.kq(M.UNKNOWN, "urlopen")), \
         mock.patch.object(M, "kenh_git_ls_remote", return_value=c):
        with contextlib.redirect_stdout(io.StringIO()):
            assert M.main() == 1
def t11_ma_phan_loai_doc_nhat(M):
    lop = [M.LOT, M.POLICY_DENIED, M.ENDPOINT_ERROR, M.TIMEOUT, M.TOOL_ERROR,
           M.UNKNOWN, M.DNS_ERROR, M.REPOSITORY_ERROR, M.AUTH_ERROR]
    assert len(lop) == len(set(lop)) == 9
CA_SAN_PHAM = [t1_url_sai_cu_phap, t2_dns_loi, t3_timeout, t4_path_rong,
               t5_kho_khong_ton_tai, t6_auth_loi, t7_policy_denied, t8_giai_doan_socket,
               t9_lot_unknown, t10_main_schema_va_fail_close, t11_ma_phan_loai_doc_nhat]
# (ID, mỏ neo duy nhất, thay thế, các ca tối thiểu phải giết)
DOT_BIEN = [
    ("m1_sai_stage_bind", 'stage = "bind"', 'stage = "create"', {"t8_giai_doan_socket"}),
    ("m2_gom_dns_endpoint", "return kq(DNS_ERROR, stage, raw)", "return kq(ENDPOINT_ERROR, stage, raw)", {"t2_dns_loi"}),
    ("m3_gom_auth_repo", "(AUTH_ERROR, (", "(REPOSITORY_ERROR, (", {"t6_auth_loi"}),
    ("m4_main_bo_kenh_git", '                "git_ls_remote": kenh_git_ls_remote()}', '}', {"t10_main_schema_va_fail_close"}),
    ("m5_gom_hai_ma", 'AUTH_ERROR = "AUTH_ERROR"', "AUTH_ERROR = REPOSITORY_ERROR", {"t11_ma_phan_loai_doc_nhat"}),
]
def chay_suite(nguon: str, cases=CA_SAN_PHAM) -> set[str]:
    do = set()
    for ca in cases:
        try:
            ca(nap(nguon, ca.__name__))
        except Exception as e:
            do.add(ca.__name__)
            if os.environ.get("PM_CHI_TIET"):
                print(f"    ĐỎ {ca.__name__}: {type(e).__name__}: {e}")
    return do
def bao(s: str) -> int:
    print(s)
    return 1
def gate(goc: str, cases=CA_SAN_PHAM, mutants=DOT_BIEN,
         expected=SO_DOT_BIEN_MONG_DOI) -> int:
    if len(mutants) != expected: return bao(f"ĐỎ số đột biến {len(mutants)} != {expected}")  # canh-so-luong
    do = chay_suite(goc, cases)
    print(f"nền: {len(cases) - len(do)}/{len(cases)} đạt")
    if do: return bao(f"TỔNG: ĐỎ (nền đỏ: {sorted(do)})")  # canh-nen-do
    xau = []
    for nhan, cu, moi, phai_chet in mutants:
        if goc.count(cu) != 1: xau.append(f"{nhan}: mỏ neo không duy nhất"); continue  # canh-duy-nhat
        chet = chay_suite(goc.replace(cu, moi, 1), CA_SAN_PHAM)
        ok = phai_chet <= chet
        print(f"  {'ok ' if ok else 'ĐỎ '} {nhan}: kill-set={sorted(chet)}")
        if not ok: xau.append(f"{nhan}: thiếu {sorted(phai_chet - chet)}")  # canh-ghi-song
    print(f"SỐ LIỆU: ca {len(cases)} · đột biến {len(mutants)} · sống {len(xau)}")
    if xau: return bao(f"TỔNG: ĐỎ ({xau})")  # canh-ket-luan
    print("TỔNG: ĐẠT")
    return 0
def bo_dong(nguon: str, dau: str) -> str:
    dong = nguon.splitlines(keepends=True)
    assert sum(dau in d for d in dong) <= 1
    return "".join(d for d in dong if dau not in d)
def go(f, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return f(*args, **kwargs)
def t12_cong_dot_bien_tu_canh(_M):
    ts, goc = Path(__file__).read_text(encoding="utf-8"), GOC.read_text(encoding="utf-8")
    for i in range(1, 6):
        m = nap(bo_dong(ts, f'("m{i}_'), f"self_m{i}")
        assert (go(gate, goc), go(m.gate, goc)) == (0, 1)
    goc_trung = goc + "\n# " + DOT_BIEN[-1][1] + "\n"
    m = nap(bo_dong(ts, "# canh-" + "duy-nhat"), "self_duy_nhat")
    assert (go(gate, goc_trung), go(m.gate, goc_trung)) == (1, 0)
    def ca_do(_): raise AssertionError("fixture nền đỏ")
    kw = {"cases": [ca_do], "mutants": [], "expected": 0}
    m = nap(bo_dong(ts, "# canh-" + "nen-do"), "self_nen_do")
    assert (go(gate, goc, **kw), go(m.gate, goc, **kw)) == (1, 0)
    song = [("song", 'LOT = "LOT"', 'LOT = "LOT"', {"t11_ma_phan_loai_doc_nhat"})]
    kw = {"mutants": song, "expected": 1}
    for key in ("ghi-song", "ket-luan"):
        m = nap(bo_dong(ts, "# canh-" + key), "self_" + key)
        assert (go(gate, goc, **kw), go(m.gate, goc, **kw)) == (1, 0)
    print("tự đột biến cổng: 9/9 chết (m1..m5 + 4 dòng cơ chế)")
    cu = 'side_effect=FileNotFoundError("git")):  ' + "# probe-missing-tool"
    moi = ('return_value=mock.MagicMock(returncode=0)):  '
           '# probe_missing_tool_executes_git')
    assert ts.count(cu) == 1
    m = nap(ts.replace(cu, moi, 1), "probe_missing_tool_executes_git")
    san_pham = nap(goc, "probe_missing_tool_product")
    t4_path_rong(san_pham)
    try:
        m.t4_path_rong(san_pham)
    except AssertionError:
        pass
    else:
        raise AssertionError("named mutant da song")
    print("named mutant probe_missing_tool_executes_git: 1/1 chết")
def main() -> int:
    try:
        t12_cong_dot_bien_tu_canh(None)
    except Exception as e:
        return bao(f"TỔNG: ĐỎ (t12_cong_dot_bien_tu_canh: {type(e).__name__}: {e})")
    return gate(GOC.read_text(encoding="utf-8"))
if __name__ == "__main__":
    sys.exit(main())
