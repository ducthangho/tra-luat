#!/usr/bin/env python3
"""Phản chứng offline cho mcp_gh.py và trách nhiệm ca/đột biến."""
from __future__ import annotations

import http.server
import importlib
import importlib.util
import io
import json
import os
import pathlib
import socket
import sys
import tempfile
import threading
import urllib.error
import urllib.request

GOC = pathlib.Path(__file__).resolve().parent
NGUON = GOC / "mcp_gh.py"

def xoa_pyc(duong: pathlib.Path) -> None:
    pyc = pathlib.Path(importlib.util.cache_from_source(str(duong)))
    if pyc.exists():
        pyc.unlink()


def nap_dot_bien(duong: pathlib.Path, ten: str):
    """Ba lớp độc lập: xoá cache, cấm ghi bytecode, rồi vô hiệu cache import."""
    xoa_pyc(duong)
    cu = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    importlib.invalidate_caches()
    try:
        spec = importlib.util.spec_from_file_location(ten, duong)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.dont_write_bytecode = cu


def ten_ban_sao(i: int) -> str:
    return f"mcp_gh_db_{i}.py"

m = nap_dot_bien(NGUON, "mcp_gh_that")


class PhanHoiGia:
    def __init__(self, than: str, headers=None):
        self.than = than.encode()
        self.headers = headers or {}

    def read(self):
        return self.than

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def mo_gia(cac_than, ghi=None, headers_dau=None):
    hop = list(cac_than)

    def mo(req, timeout):
        if ghi is not None:
            ghi.append((json.loads(req.data.decode()), dict(req.headers)))
        headers = headers_dau if headers_dau and len(hop) == len(cac_than) else {}
        return PhanHoiGia(hop.pop(0) if hop else "{}", headers)

    return mo


def bi_chan(url: str) -> str:
    try:
        m.kiem_dich_den(url)
    except ValueError as e:
        return str(e)
    raise AssertionError(f"đích đáng lẽ phải bị chặn: {url}")

def thu_chuyen_huong(code: int) -> list[str | None]:
    """Hai HTTP server loopback: server hai chỉ ghi marker Authorization nhận được."""
    nhan = []

    class Dich(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            nhan.append(self.headers.get("Authorization"))
            self.send_response(204)
            self.end_headers()

        def log_message(self, *args):
            pass

    dich = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Dich)
    location = f"http://127.0.0.1:{dich.server_port}/dich"

    class Dau(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(code)
            self.send_header("Location", location)
            self.end_headers()

        def log_message(self, *args):
            pass

    dau = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Dau)
    threads = [threading.Thread(target=s.serve_forever, kwargs={"poll_interval": .01}, daemon=True)
               for s in (dich, dau)]
    for thread in threads:
        thread.start()
    req = urllib.request.Request(f"http://127.0.0.1:{dau.server_port}/dau",
                                 headers={"Authorization": "Bearer marker-offline"})
    try:
        try:
            with m._mo_mac_dinh(req, 2) as response:
                response.read()
        except urllib.error.HTTPError:
            pass
    finally:
        for server in (dau, dich):
            server.shutdown()
            server.server_close()
        for thread in threads:
            thread.join(1)
    return nhan


def lop_phien(mo=None, liet_ke=None, chay=None, ghi=None):
    class Gia:
        def __init__(self, path="/mcp/", token=None, **kwargs):
            self.path = path
            if ghi is not None:
                ghi.append(("init", path))

        def mo_phien(self):
            return {} if mo is None else mo

        def goi(self, method, params=None, bao_tin=False):
            if ghi is not None:
                ghi.append(("goi", method, self.path))
            return liet_ke if liet_ke is not None else {"result": {"tools": []}}

        def chay(self, ten, doi_so):
            if ghi is not None:
                ghi.append(("chay", ten, doi_so, self.path))
            return chay if chay is not None else {"result": {"content": [{"text": "ok"}]}}

    return Gia


def main_gia(argv, lop, token="token-gia"):
    cu_lop, cu_token = m.Phien, os.environ.get("GITHUB_PAT")
    m.Phien = lop
    if token is None:
        os.environ.pop("GITHUB_PAT", None)
    else:
        os.environ["GITHUB_PAT"] = token
    out, err, cu_out, cu_err = io.StringIO(), io.StringIO(), sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, err
    try:
        rc = m.main(list(argv))
    finally:
        sys.stdout, sys.stderr, m.Phien = cu_out, cu_err, cu_lop
        if cu_token is None:
            os.environ.pop("GITHUB_PAT", None)
        else:
            os.environ["GITHUB_PAT"] = cu_token
    return rc, out.getvalue(), err.getvalue()


# A — đích credential và chuyển hướng
def a1_cong_444_bi_chan():
    bi_chan("https://api.githubcopilot.com:444/mcp/")


def a2_origin_va_cu_phap_url():
    for url in ("https://api.githubcopilot.com:8080/mcp/",
                "https://api.githubcopilot.com/mcp/?x=1",
                "https://api.githubcopilot.com/mcp/#frag"):
        bi_chan(url)
    m.kiem_dich_den("https://API.GitHubCopilot.COM/mcp/")


def a3_khong_lo_bi_mat_trong_loi():
    secret = "marker-bi-mat"
    loi = bi_chan(f"https://user:{secret}@api.githubcopilot.com/mcp/")
    assert secret not in loi, loi


def a4_kiem_lai_luc_gui():
    da_mo = []
    p = m.Phien("/mcp/", "tok", mo=lambda *args: da_mo.append(True))
    p.url = "https://evil.example/x"
    try:
        p.goi("tools/list", {})
    except ValueError:
        pass
    else:
        raise AssertionError("URL gán lại không bị chặn")
    assert not da_mo, "đã mở kết nối trước khi kiểm lại đích"


def a5_khong_theo_301():
    assert thu_chuyen_huong(301) == [], "301 làm credential tới server thứ hai"


def a6_khong_theo_302():
    assert thu_chuyen_huong(302) == [], "302 làm credential tới server thứ hai"


def a6_khong_theo_303():
    assert thu_chuyen_huong(303) == [], "303 làm credential tới server thứ hai"


def a7_khong_theo_307_308():
    assert thu_chuyen_huong(307) == [] and thu_chuyen_huong(308) == []


def a8_hai_duong_thuan():
    m.Phien("/mcp/", "tok", mo=mo_gia([]))
    m.Phien("/mcp/x/actions", "tok", mo=mo_gia([]))


def a9_host_hau_to_bi_chan():
    bi_chan("https://api.githubcopilot.com.example/mcp/")


def a10_http_bi_chan():
    bi_chan("http://api.githubcopilot.com/mcp/")


def a11_duong_ngoai_tap_bi_chan():
    bi_chan("https://api.githubcopilot.com/x")


# B — chín bất biến đã trả giá
def b1_sse_lay_data_cuoi():
    raw = 'data: {"result":{"sai":1}}\n\ndata: {"result":{"dung":1}}\n'
    assert json.loads(m.tach_than(raw))["result"] == {"dung": 1}


def b2_khong_cat_hai_tang():
    text = json.dumps({"x": ["y" * 40] * 500})
    kq = {"result": {"content": [{"text": text}]}}
    than = m._bo_tien_to_data("data: " + json.dumps(kq))
    assert len(than) > 20000
    json.loads(than)
    van_ban = m.rut_van_ban(kq)
    assert len(van_ban) > 20000
    json.loads(van_ban)


def b3_thieu_token_fail_close():
    cu_ket_noi, so_ket_noi = socket.create_connection, []
    def chan_ket_noi(*args, **kwargs):
        so_ket_noi.append(1)
        raise AssertionError("đã ra mạng")
    socket.create_connection = chan_ket_noi
    try:
        rc, _, err = main_gia(["--liet-ke"], m.Phien, token=None)
    finally:
        socket.create_connection = cu_ket_noi
    assert rc == 3 and "KHÔNG ĐO ĐƯỢC" in err and not so_ket_noi


def b4_initialize_jsonrpc_error():
    raw = '{"error":{"code":-32000,"message":"khong duoc phep"}}'
    kq = m.Phien("/mcp/", "tok", mo=mo_gia([raw])).mo_phien()
    assert kq.get("_loi", "").startswith("JSON-RPC error -32000"), kq


def b5_loi_van_chuyen_co_khoi_rieng():
    def mo(req, timeout):
        raise urllib.error.URLError("offline")
    kq = m.Phien("/mcp/", "tok", mo=mo).goi("tools/list", {})
    assert "_mang" in kq and m.loi_cua(kq)


def b6_init_thuc_su_goi_chot():
    cu, ds = m.kiem_dich_den, []
    m.kiem_dich_den = lambda url: ds.append(url)
    try:
        m.Phien("/mcp/", "tok", mo=mo_gia([]))
    finally:
        m.kiem_dich_den = cu
    assert ds == ["https://api.githubcopilot.com/mcp/"]


def _nap_co_pyc(path, name):
    cu = sys.dont_write_bytecode
    sys.dont_write_bytecode = False
    importlib.invalidate_caches()
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.dont_write_bytecode = cu


def b7_xoa_pyc_cu():
    with tempfile.TemporaryDirectory() as d:
        path = pathlib.Path(d) / "mau.py"
        path.write_text("GIA_TRI = 'cu'\n", encoding="utf-8")
        moc = 1_700_000_000
        os.utime(path, (moc, moc))
        assert _nap_co_pyc(path, "mau_cu").GIA_TRI == "cu"
        path.write_text("GIA_TRI = 'moi'\n", encoding="utf-8")
        os.utime(path, (moc, moc))
        assert nap_dot_bien(path, "mau_moi").GIA_TRI == "moi"
        assert not pathlib.Path(importlib.util.cache_from_source(str(path))).exists()


def b7_tat_ghi_bytecode():
    with tempfile.TemporaryDirectory() as d:
        path = pathlib.Path(d) / "khong_pyc.py"
        path.write_text("X = 1\n", encoding="utf-8")
        nap_dot_bien(path, "khong_pyc")
        assert not list(pathlib.Path(d).glob("__pycache__/*")), "loader để lại .pyc"


def b7_invalidate_cache():
    cu, goi = importlib.invalidate_caches, []
    importlib.invalidate_caches = lambda: goi.append(True)
    try:
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "cache.py"
            path.write_text("X = 1\n", encoding="utf-8")
            nap_dot_bien(path, "cache")
    finally:
        importlib.invalidate_caches = cu
    assert goi == [True]


def b7_ten_tung_dot_bien_rieng():
    assert len({ten_ban_sao(i) for i in range(4)}) == 4


def b8_notification_dung_thoi_diem_khong_id():
    ghi = []
    hong = m.Phien("/mcp/", "tok", mo=mo_gia(['{"error":{"code":-1}}'], ghi)).mo_phien()
    assert hong.get("_loi") and len(ghi) == 1, "đã báo initialized sau initialize hỏng"
    ghi = []
    ok = m.Phien("/mcp/", "tok", mo=mo_gia(['{"result":{"ok":1}}', ""], ghi)).mo_phien()
    assert ok == {} and len(ghi) == 2
    assert ghi[1][0]["method"] == "notifications/initialized" and "id" not in ghi[1][0]


def b9_giu_session_id():
    ghi = []
    p = m.Phien("/mcp/", "tok", mo=mo_gia(['{"result":{}}', '{"result":{}}'], ghi,
                                           {"Mcp-Session-Id": "S-42"}))
    p.goi("initialize", {})
    p.goi("tools/list", {})
    headers = {k.lower(): v for k, v in ghi[1][1].items()}
    assert p.sid == "S-42" and headers.get("mcp-session-id") == "S-42"


# C/D — bất biến cổng và hợp đồng CLI
def _du_ca(registry, ran):
    return len(registry) > 0 and tuple(ran) == tuple(registry)


def _co_dot_bien(mutants):
    return bool(mutants)


def cong(registry, ran, mutants, killed, errors):
    return (_du_ca(registry, ran) and _co_dot_bien(mutants)
            and tuple(killed) == tuple(mutants) and not errors)


def phan_dinh(lines):
    return not any("ĐỎ" in line or "KHÔNG_ĐO_ĐƯỢC" in line for line in lines)


def ma_thoat(xanh):
    return 0 if xanh else 1


def c1_so_ca_rong_do():
    assert not cong((), (), ("m",), ("m",), ())


def c2_so_dot_bien_rong_do():
    assert not cong(("c",), ("c",), (), (), ())


def c3_ca_hai_so_rong_do():
    assert not cong((), (), (), (), ())


def c4_co_ten_nhung_khong_chay_do():
    assert not cong(("c",), (), ("m",), ("m",), ())


def d1_tool_top_level_error_rc3():
    lop = lop_phien(chay={"error": {"code": -1, "message": "hong"}})
    rc, _, _ = main_gia(["tool", "{}"], lop)
    assert rc == 3


def d2_tool_iserror_rc3():
    lop = lop_phien(chay={"result": {"isError": True, "content": []}})
    rc, _, _ = main_gia(["tool", "{}"], lop)
    assert rc == 3  # phản hồi bơm; chưa đo được từ công cụ thật


def d3_initialize_result_rong_do():
    kq = m.Phien("/mcp/", "tok", mo=mo_gia(['{"result":{}}'])).mo_phien()
    assert kq.get("_loi"), kq


def d4_phan_hoi_list_co_loi_cau_truc():
    kq = m.Phien("/mcp/", "tok", mo=mo_gia(["[]"])).mo_phien()
    assert "phải là object" in kq.get("_loi", ""), kq


def d5_notification_loi_van_chuyen():
    hop = iter(({"result": {"ok": 1}}, {"_mang": "notification hong"}))
    p = m.Phien("/mcp/", "tok", mo=mo_gia([]))
    p.goi = lambda *args, **kwargs: next(hop)
    kq = p.mo_phien()
    assert kq.get("_loi", "").startswith("lỗi mạng"), kq


def d6_hop_dong_cli_0_2_3():
    ghi = []
    lop = lop_phien(liet_ke={"result": {"tools": [{"name": "mot"}]}}, ghi=ghi)
    assert main_gia(["--liet-ke"], lop)[0] == 0
    assert main_gia(["tool", '{"x":1}'], lop)[0] == 0
    assert main_gia(["--liet-ke", "--path", "/mcp/x/actions"], lop)[0] == 0
    assert main_gia(["tool", "{"], lop)[0] == 2
    assert main_gia(["--path", "/sai"], m.Phien)[0] == 3
    assert sum(x[0] == "goi" and x[1] == "tools/list" for x in ghi) == 2
    assert any(x[0] == "chay" and x[1] == "tool" for x in ghi)
    assert any(x[0] == "init" and x[1] == "/mcp/x/actions" for x in ghi)


def d7_cong_xanh_chi_khi_hai_so_duong_bang_nhau():
    assert cong(("c",), ("c",), ("m",), ("m",), ())


def dong_dot_bien(kill_sets, mutants, failed, errors=()):
    if failed:
        return "ĐỘT BIẾN   : KHÔNG_ĐO_ĐƯỢC (nền đỏ)"
    ok = _co_dot_bien(mutants) and len(kill_sets) == len(mutants) and not errors
    return f"ĐỘT BIẾN   : đã đo {len(kill_sets)}/{len(mutants)} tập giết · " + ("ĐẠT" if ok else "ĐỎ")


def d7b_nen_do_khong_dem_dot_bien():
    assert "KHÔNG_ĐO_ĐƯỢC" in dong_dot_bien((), ("m",), (("c", "đỏ"),))


def loi_d8(cases, mutants, kill_sets):
    targets = {name: target for name, *_, target in mutants}
    return (
        [name for name, target in targets.items()
         if target not in kill_sets.get(name, ())],
        [name for name in targets if not kill_sets.get(name, ())],
        [case for case in cases if case not in targets.values()],
    )


def dong_d8(errors, failed):
    labels = ("D8(a) đích nằm trong tập giết", "D8(b) không tập giết rỗng",
              "D8(c) mọi ca có đột biến canh")
    if failed:
        return [f"{label}: KHÔNG_ĐO_ĐƯỢC (nền đỏ)" for label in labels]
    return [f"{label}: " + (f"ĐỎ {bad!r}" if bad else "ĐẠT")
            for label, bad in zip(labels, errors)]


def bang_giao_pham_vi(mutants, kill_sets, failed):
    lines = ["GIAO PHẠM VI:", "| đột biến | đích | ca ngoài đích bị giết |",
             "|---|---|---|"]
    if failed:
        return lines + ["| KHÔNG_ĐO_ĐƯỢC | — | nền đỏ |"]
    rows = []
    for name, *_, target in mutants:
        extra = [case for case in kill_sets.get(name, ()) if case != target]
        if extra:
            rows.append(f"| {name} | {target} | {', '.join(extra)} |")
    return lines + (rows or ["| (không có) | — | — |"])


def d8_quy_trach_nhiem_ba_dieu_kien():
    mutants = (("m", "test", "old", "new", "c"),)
    assert loi_d8(("c",), mutants, {"m": ("c", "d")}) == ([], [], [])
    assert loi_d8(("c",), mutants, {"m": ("d",)})[0] == ["m"]
    assert loi_d8(("c",), mutants, {"m": ()})[1] == ["m"]
    assert loi_d8(("c", "d"), mutants, {"m": ("c",)})[2] == ["d"]


def d9_ngan_sach_900_dong_ma():
    tong = sum(sum(1 for _ in path.open(encoding="utf-8")) for path in (NGUON, pathlib.Path(__file__)))
    assert tong <= 900, f"hai tệp mã dùng {tong}/900 dòng"


def d10_main_khong_chay_ca_phai_do():
    assert ma_thoat(False) == 1


def d11_chay_cli_khong_duoc_xanh_khi_d8_do():
    da_chay = []
    class Canh:
        CASES = (("c", lambda: da_chay.append(True)),)
    mutants = (("m", "test", "", "", "c"),)
    cu_out = sys.stdout
    try:
        for lan, (kill_sets, do) in enumerate((({"m": ("c",)}, False), ({"m": ()}, True)), 1):
            out = sys.stdout = io.StringIO()
            rc = chay_cli(Canh, mutants, lambda: (kill_sets, []))
            report = out.getvalue()
            assert len(da_chay) == lan and ("ĐỎ" in report) == do == (rc != 0)
            assert f"TỔNG: {'ĐỎ' if do else 'ĐẠT'}" in report
            assert all(x in report for x in ("CA ", "ĐỘT BIẾN", "D8(a)", "D8(b)", "D8(c)", "GIAO PHẠM VI"))
    finally:
        sys.stdout = cu_out


# Đăng ký xong mới đóng băng; runner không sửa tuple này.
CASES = (
    ("A1", a1_cong_444_bi_chan), ("A2", a2_origin_va_cu_phap_url),
    ("A3", a3_khong_lo_bi_mat_trong_loi), ("A4", a4_kiem_lai_luc_gui),
    ("A5", a5_khong_theo_301), ("A6-302", a6_khong_theo_302),
    ("A6-303", a6_khong_theo_303), ("A7", a7_khong_theo_307_308), ("A8", a8_hai_duong_thuan),
    ("A9-host", a9_host_hau_to_bi_chan), ("A10-scheme", a10_http_bi_chan),
    ("A11-path", a11_duong_ngoai_tap_bi_chan),
    ("B1", b1_sse_lay_data_cuoi), ("B2", b2_khong_cat_hai_tang),
    ("B3", b3_thieu_token_fail_close), ("B4", b4_initialize_jsonrpc_error),
    ("B5", b5_loi_van_chuyen_co_khoi_rieng), ("B6", b6_init_thuc_su_goi_chot),
    ("B7-xoa", b7_xoa_pyc_cu), ("B7-khong-ghi", b7_tat_ghi_bytecode),
    ("B7-cache", b7_invalidate_cache), ("B7-ten", b7_ten_tung_dot_bien_rieng),
    ("B8", b8_notification_dung_thoi_diem_khong_id), ("B9", b9_giu_session_id),
    ("C1", c1_so_ca_rong_do), ("C2", c2_so_dot_bien_rong_do),
    ("C3", c3_ca_hai_so_rong_do), ("C4", c4_co_ten_nhung_khong_chay_do),
    ("D1", d1_tool_top_level_error_rc3), ("D2", d2_tool_iserror_rc3),
    ("D3", d3_initialize_result_rong_do), ("D4", d4_phan_hoi_list_co_loi_cau_truc),
    ("D5", d5_notification_loi_van_chuyen), ("D6", d6_hop_dong_cli_0_2_3),
    ("D7", d7_cong_xanh_chi_khi_hai_so_duong_bang_nhau),
    ("D7b", d7b_nen_do_khong_dem_dot_bien),
    ("D8", d8_quy_trach_nhiem_ba_dieu_kien), ("D9", d9_ngan_sach_900_dong_ma),
    ("D10-main", d10_main_khong_chay_ca_phai_do), ("D11-gate", d11_chay_cli_khong_duoc_xanh_khi_d8_do),
)


# (tên, tệp đích, mẫu cũ, mẫu mới, ca đích phải nằm trong tập giết)
MUTATIONS = (
    ("a1_cong_444", "app", "if port != CONG_CHO_PHEP:", "if port not in (CONG_CHO_PHEP, 444):", "A1"),
    ("a2_bo_query", "app", "if u.query or u.fragment:", "if False:", "A2"),
    ("a3_lo_secret", "app", 'raise ValueError("URL không được mang thông tin đăng nhập")', 'raise ValueError(f"URL không hợp lệ: {url}")', "A3"),
    ("a4_bo_chot_gui", "app", "        kiem_dich_den(self.url)  # kiểm lại ngay trước mỗi lần gắn credential", "        pass  # đột biến bỏ chốt lúc gửi", "A4"),
    ("a5_theo_301", "app", "if code == 301:", "if code == -301:", "A5"),
    ("a6_theo_302", "app", "if code == 302:", "if code == -302:", "A6-302"),
    ("a6_theo_303", "app", "if code == 303:", "if code == -303:", "A6-303"),
    ("a7_theo_307_308", "app", "if code in (307, 308):", "if False:", "A7"),
    ("a8_bo_actions", "app", 'DUONG_CHO_PHEP = ("/mcp/", "/mcp/x/actions")', 'DUONG_CHO_PHEP = ("/mcp/",)', "A8"),
    ("a9_bo_host", "app", 'if u.hostname != HOST_CHO_PHEP:', "if False:", "A9-host"),
    ("a10_bo_scheme", "app", 'if u.scheme != "https":', "if False:", "A10-scheme"),
    ("a11_bo_path", "app", "if u.path not in DUONG_CHO_PHEP:", "if False:", "A11-path"),
    ("b1_bo_data", "app", 'if dong.startswith("data:"):', "if False:", "B1"),
    ("b2_cat_than", "app", "return dong[5:].strip()", "return dong[5:].strip()[:6000]", "B2"),
    ("b2_cat_text", "app", 'return nd[0]["text"]', 'return nd[0]["text"][:6000]', "B2"),
    ("b3_bo_token", "app", "if not tok:", "if False:", "B3"),
    ("b4_bo_jsonrpc", "app", 'if isinstance(d.get("error"), dict):', "if False:", "B4"),
    ("b5_bo_urlerror", "app", "except (urllib.error.URLError, TimeoutError, OSError) as e:", "except (ValueError,) as e:", "B5"),
    ("b6_bo_chot_init", "app", "        kiem_dich_den(self.url)  # chốt lúc dựng là một bất biến độc lập", "        pass  # đột biến bỏ chốt init", "B6"),
    ("b7_bo_xoa_pyc", "test", "    xoa_pyc(duong)\n    cu = sys.dont_write_bytecode", "    cu = sys.dont_write_bytecode", "B7-xoa"),
    ("b7_bo_cam_ghi", "test", "    sys.dont_write_bytecode = True\n    importlib.invalidate_caches()", "    importlib.invalidate_caches()", "B7-khong-ghi"),
    ("b7_bo_invalidate", "test", "    importlib.invalidate_caches()\n    try:\n        spec =", "    try:\n        spec =", "B7-cache"),
    ("b7_trung_ten", "test", 'return f"mcp_gh_db_{i}.py"', 'return "mcp_gh_db.py"', "B7-ten"),
    ("b8_notification_co_id", "app", "if not bao_tin:", "if True:", "B8"),
    ("b9_bo_sid", "app", "                if sid:\n                    self.sid = sid", "                if False:\n                    self.sid = sid", "B9"),
    ("c1_cho_so_ca_rong", "test", "return len(registry) > 0 and tuple(ran) == tuple(registry)", "return tuple(ran) == tuple(registry)", "C1"),
    ("c2_cho_so_db_rong", "test", "return bool(mutants)", "return True", "C2"),
    ("c3_cho_ca_hai_rong", "test", "    return (_du_ca(registry, ran) and _co_dot_bien(mutants)", "    return ((not registry and not mutants) or _du_ca(registry, ran) and _co_dot_bien(mutants)", "C3"),
    ("c4_khong_goi_ca", "test", "return len(registry) > 0 and tuple(ran) == tuple(registry)", "return bool(registry)", "C4"),
    ("d1_bo_top_error", "app", "    if loi:\n        return loi\n    result = d[\"result\"]", "    if loi:\n        return None\n    result = d[\"result\"]", "D1"),
    ("d2_bo_iserror", "app", 'if isinstance(result, dict) and result.get("isError") is True:', "if False:", "D2"),
    ("d3_nhan_result_rong", "app", 'if not isinstance(kq.get("result"), dict) or not kq["result"]:', 'if not isinstance(kq.get("result"), dict) or False:', "D3"),
    ("d4_bo_shape", "app", "if not isinstance(d, dict):", "if False:", "D4"),
    ("d5_nuot_loi_notification", "app", "        if loi:\n            return {\"_loi\": loi}\n        return {}", "        if False:\n            return {\"_loi\": loi}\n        return {}", "D5"),
    ("d6_doi_co_cli", "app", 'argv[0] == "--liet-ke"', 'argv[0] == "--liet-ke-doi"', "D6"),
    ("d7_cong_khong_xanh", "test", "return len(registry) > 0 and tuple(ran) == tuple(registry)", "return False", "D7"),
    ("d7b_dem_khi_nen_do", "test", "    if failed:\n        return \"ĐỘT BIẾN   : KHÔNG_ĐO_ĐƯỢC (nền đỏ)\"", "    if False:\n        return \"ĐỘT BIẾN   : KHÔNG_ĐO_ĐƯỢC (nền đỏ)\"", "D7b"),
    ("d8_bo_dieu_kien_a", "test", "if target not in kill_sets.get(name, ())", "if False", "D8"),
    ("d8_bo_dieu_kien_b", "test", "if not kill_sets.get(name, ())", "if False", "D8"),
    ("d8_bo_dieu_kien_c", "test", "if case not in targets.values()", "if False", "D8"),
    ("d9_vuot_ngan_sach", "test", "assert tong <= 900", "assert tong < 0", "D9"),
    ("d10_main_luon_xanh", "test", "return 0 if xanh else 1", "return 0", "D10-main"),
    ("d11_ep_rc_xanh", "test", "return 0 if xanh else 1", "return 0", "D11-gate"),
    ("d11_phan_dinh_xanh", "test", "return not any(\"ĐỎ\" in line or \"KHÔNG_ĐO_ĐƯỢC\" in line for line in lines)", "return True", "D11-gate"),
    ("d11_xoa_d8", "test", "    lines += dong_d8(d8_errors, failed)\n    lines += bang_giao_pham_vi", "    lines += bang_giao_pham_vi", "D11-gate"),
    ("d11_xoa_tong", "test", "    lines.append(\"TỔNG: \" + (\"ĐẠT\" if xanh else \"ĐỎ\"))", "    pass", "D11-gate"),
    ("d11_xoa_ban_in", "test", "    print(\"\\n\".join(lines))", "    pass", "D11-gate"),
    ("d11_bo_than_ca", "test", "    for name, fn in module.CASES:\n        ran.append(name)\n        try:\n            fn()\n        except Exception as e:  # runner phải biến mọi lỗi ca thành ĐỎ, nhưng không che nội dung\n            failed.append((name, f\"{type(e).__name__}: {e}\"))", "    for name, fn in module.CASES:\n        pass", "D11-gate"),
)


def chay_cac_ca(module):
    ran, failed = [], []
    for name, fn in module.CASES:
        ran.append(name)
        try:
            fn()
        except Exception as e:  # runner phải biến mọi lỗi ca thành ĐỎ, nhưng không che nội dung
            failed.append((name, f"{type(e).__name__}: {e}"))
    return ran, failed


def chay_dot_bien():
    app_src = NGUON.read_text(encoding="utf-8")
    test_src = pathlib.Path(__file__).read_text(encoding="utf-8")
    kill_sets, errors = {}, []
    root = sys.modules[__name__]
    for i, (name, target_file, old, new, target_case) in enumerate(MUTATIONS):
        src = app_src if target_file == "app" else test_src
        if old not in src:
            errors.append(f"{name}: mẫu đột biến đã trôi")
            continue
        with tempfile.TemporaryDirectory() as d:
            folder = pathlib.Path(d)
            try:
                if target_file == "app":
                    path = folder / ten_ban_sao(i)
                    path.write_text(src.replace(old, new, 1), encoding="utf-8")
                    mutant = nap_dot_bien(path, f"mcp_gh_db_{i}")
                    old_module, globals()["m"] = globals()["m"], mutant
                    try:
                        _, failed = chay_cac_ca(root)
                    finally:
                        globals()["m"] = old_module
                else:
                    (folder / "mcp_gh.py").write_text(app_src, encoding="utf-8")
                    path = folder / f"mcp_gh_test_db_{i}.py"
                    path.write_text(src.replace(old, new, 1), encoding="utf-8")
                    mutant = nap_dot_bien(path, f"mcp_gh_test_db_{i}")
                    _, failed = chay_cac_ca(mutant)
                kill_sets[name] = tuple(case for case, _ in failed)
            except Exception as e:
                errors.append(f"{name}: runner lỗi {type(e).__name__}: {e}")
    return kill_sets, errors


def chay_cli(module=None, mutants=MUTATIONS, run_mutants=chay_dot_bien):
    module = sys.modules[__name__] if module is None else module
    cases = module.CASES
    ran, failed = chay_cac_ca(module)
    kill_sets, mutation_errors = ({}, []) if failed else run_mutants()
    d8_errors = ((), (), ()) if failed else loi_d8(
        tuple(name for name, _ in cases), mutants, kill_sets)
    lines = [f"CA         : {len(ran) - len(failed)}/{len(cases)} đạt · {len(failed)} đỏ · "
             + ("ĐẠT" if _du_ca(tuple(name for name, _ in cases), ran) and not failed else "ĐỎ")]
    lines += [f"  ĐỎ {name}: {error}" for name, error in failed]
    lines.append(dong_dot_bien(kill_sets, mutants, failed, mutation_errors))
    lines += dong_d8(d8_errors, failed)
    lines += bang_giao_pham_vi(mutants, kill_sets, failed)
    lines += [f"  LỖI RUNNER {error}" for error in mutation_errors]
    xanh = phan_dinh(lines)
    lines.append("TỔNG: " + ("ĐẠT" if xanh else "ĐỎ"))
    print("\n".join(lines))
    return ma_thoat(xanh)


if __name__ == "__main__":
    sys.exit(chay_cli())
