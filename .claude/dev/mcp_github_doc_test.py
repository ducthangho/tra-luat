#!/usr/bin/env python3
"""Phản chứng offline cho mcp_github_doc.py; đồ giả mô phỏng trạng thái máy chủ.

Chạy thường:  python3 .claude/dev/mcp_github_doc_test.py
Đo răng:      python3 .claude/dev/mcp_github_doc_test.py --dot-bien
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from contextlib import redirect_stderr
from contextlib import contextmanager
from io import StringIO
from pathlib import Path

MODUN = Path(__file__).with_name("mcp_github_doc.py")
CA = []


def ca(fn):
    CA.append(fn)
    return fn


def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise AssertionError(thong_diep)


def _nap(path=MODUN):
    truoc = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("mcp_github_doc_duoi_test", path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m
    finally:
        sys.dont_write_bytecode = truoc


M = _nap()


@contextmanager
def _cau_hinh(noi_dung, env=None):
    cu = os.environ.copy()
    try:
        with tempfile.TemporaryDirectory() as d:
            Path(d, ".mcp.json").write_text(json.dumps(noi_dung), encoding="utf-8")
            for k in ("TOKEN_TEST_MCP", "TL_MCP_TOOLSET"):
                os.environ.pop(k, None)
            os.environ.update(env or {})
            yield Path(d)
    finally:
        os.environ.clear()
        os.environ.update(cu)


def _cfg(url="https://api.example/mcp", headers=None, ten="github"):
    return {"mcpServers": {ten: {"url": url, "headers": headers or {}}}}


def _hong(fn, m=M):
    try:
        fn()
    except m.Hong as e:
        return str(e)
    raise AssertionError("mong doi Hong nhung ham da cho qua")


class _TraLoi:
    def __init__(self, status=200, body="", headers=None):
        self.status, self._body, self.headers = status, body, headers or {}

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return self._body.encode()


class _MayChuGia:
    """State machine nhỏ: phản hồi theo method JSON-RPC, không theo số thứ tự gọi."""
    def __init__(self, responses):
        self.responses, self.requests = responses, []

    def __call__(self, req, timeout):
        than = json.loads(req.data)
        method = than["method"]
        self.requests.append((method, req, timeout))
        value = self.responses[method]
        if isinstance(value, Exception):
            raise value
        return value


@contextmanager
def _urlopen_gia(m, server):
    goc = m.urllib.request.urlopen
    m.urllib.request.urlopen = server
    try:
        yield
    finally:
        m.urllib.request.urlopen = goc


@ca
def t01_doc_dung_server_chinh_xac_va_giai_header(m=M):
    with tempfile.TemporaryDirectory() as d:
        _hong(lambda: m._doc_cau_hinh(Path(d)), m)
    with _cau_hinh(_cfg(headers={"Authorization": "Bearer ${TOKEN_TEST_MCP}"}),
                   {"TOKEN_TEST_MCP": "secret-value"}) as d:
        url, headers = m._doc_cau_hinh(d)
        bang(url == "https://api.example/mcp", f"url sai: {url}")
        bang(headers["Authorization"] == "Bearer secret-value", "khong giai env header")
    with _cau_hinh(_cfg(ten="github-actions")) as d:
        _hong(lambda: m._doc_cau_hinh(d), m)
    with _cau_hinh(_cfg(headers={"A": "${TOKEN_TEST_MCP}"})) as d:
        try:
            _hong(lambda: m._doc_cau_hinh(d), m)
        except Exception as e:
            raise AssertionError(f"env thiếu gây lỗi ngoài hợp đồng: {type(e).__name__}") from None
    with _cau_hinh({"mcpServers": {"github": "khong-phai-object"}}) as d:
        _hong(lambda: m._doc_cau_hinh(d), m)
    with _cau_hinh({"sai-khoa": {"github": {"url": "https://x"}}}) as d:
        _hong(lambda: m._doc_cau_hinh(d), m)
    with _cau_hinh([]) as d:
        _hong(lambda: m._doc_cau_hinh(d), m)
    with _cau_hinh({"mcpServers": {"github": {}}}) as d:
        mo_ta = _hong(lambda: m._doc_cau_hinh(d), m)
        bang("khong khai `url`" in mo_ta, f"url rong bi phan loai sai: {mo_ta}")
    with _cau_hinh(_cfg(headers=["khong", "phai", "object"])) as d:
        try:
            _hong(lambda: m._doc_cau_hinh(d), m)
        except Exception as e:  # lỗi triển khai vô can không được giết mutant
            raise AssertionError(f"headers méo gây lỗi ngoài hợp đồng: {type(e).__name__}") from None


@ca
def t12_headers_falsy_co_mat_phai_bi_tu_choi(m=M):
    for headers in ([], "", 0, False, None):
        cfg = {"mcpServers": {"github": {"url": "https://api.example/mcp",
                                           "headers": headers}}}
        with _cau_hinh(cfg) as d:
            mo_ta = _hong(lambda: m._doc_cau_hinh(d), m)
            bang("headers" in mo_ta and "object" in mo_ta,
                 f"headers={headers!r} bi phan loai sai: {mo_ta}")
    with _cau_hinh({"mcpServers": {"github": {"url": "https://api.example/mcp"}}}) as d:
        _, headers = m._doc_cau_hinh(d)
        bang(headers == {}, "headers vang mat khong mac dinh thanh object rong")


@ca
def t13_goc_mac_dinh_neo_theo_tep_va_tl_goc_ghi_de(m=M):
    cu = os.environ.pop("TL_GOC", None)
    cwd = Path.cwd()
    try:
        os.chdir(MODUN.parent)
        bang(m._goc_du_an() == MODUN.resolve().parents[2],
             f"goc mac dinh troi theo CWD: {m._goc_du_an()}")
        with tempfile.TemporaryDirectory() as d:
            os.environ["TL_GOC"] = d
            bang(m._goc_du_an() == Path(d).resolve(), "TL_GOC khong ghi de goc")
    finally:
        os.chdir(cwd)
        if cu is None:
            os.environ.pop("TL_GOC", None)
        else:
            os.environ["TL_GOC"] = cu


@ca
def t10_khoa_co_mat_hong_khong_roi_sang_du_phong(m=M):
    du_phong = {"github": {"url": "https://du-phong.example/mcp"}}
    for gia_tri, ten_kieu in ((None, "NoneType"), (["github"], "list")):
        with _cau_hinh({"mcpServers": gia_tri, "servers": du_phong}) as d:
            mo_ta = _hong(lambda: m._doc_cau_hinh(d), m)
            bang("`mcpServers`" in mo_ta and ten_kieu in mo_ta,
                 f"khong neu dung khoa/kieu hong: {mo_ta}")
            bang("du-phong" not in mo_ta, f"da roi sang khoa du phong: {mo_ta}")


@ca
def t11_ten_server_casefold_phai_duy_nhat(m=M):
    with _cau_hinh(_cfg(ten="GitHub")) as d:
        try:
            url, _ = m._doc_cau_hinh(d)
        except m.Hong:
            url = None
        bang(url == "https://api.example/mcp", f"khong nhan ten casefold duy nhat: {url}")
    with _cau_hinh({"mcpServers": {
            "github": {"url": "https://mot.example/mcp"},
            "GitHub": {"url": "https://hai.example/mcp"},
    }}) as d:
        mo_ta = _hong(lambda: m._doc_cau_hinh(d), m)
        bang("2 server" in mo_ta and "chuan hoa" in mo_ta, f"khong chan ten mo ho: {mo_ta}")


@ca
def t02_moi_url_tu_choi_khong_probe_khong_ro_bi_mat(m=M):
    bi_mat = "GOCSPX-abc"
    cac_url = [
        f"https://host:{bi_mat}/mcp", f"https://u:{bi_mat}@host/mcp",
        f"{bi_mat}:x", f"{bi_mat}://host/mcp", f"http:///{bi_mat}",
    ]
    goc = m.urllib.request.urlopen
    da_probe = []
    m.urllib.request.urlopen = lambda *a, **k: da_probe.append((a, k))
    try:
        for url in cac_url:
            with _cau_hinh(_cfg(url=url)) as d:
                mo_ta = _hong(lambda: m.Phien(d), m)
                bang(bi_mat not in mo_ta, f"nhanh tu choi lam lo url: {mo_ta!r}")
        bang(not da_probe, "URL bi tu choi ma van probe")
    finally:
        m.urllib.request.urlopen = goc


@ca
def t03_toolset_chi_la_hau_to_path_an_toan(m=M):
    with _cau_hinh(_cfg("https://api.example/mcp?keep=1#frag"),
                   {"TL_MCP_TOOLSET": "x/actions"}) as d:
        url, _ = m._doc_cau_hinh(d)
        bang(url == "https://api.example/mcp/x/actions?keep=1#frag", f"ghep sai URL: {url}")
    for xau in ("../actions", "/x", "x/", "x//actions", "X/actions", "x?token=leak"):
        with _cau_hinh(_cfg(), {"TL_MCP_TOOLSET": xau}) as d:
            _hong(lambda: m._doc_cau_hinh(d), m)


@ca
def t04_post_giu_header_timeout_va_khong_in_secret(m=M):
    with _cau_hinh(_cfg(headers={"Authorization": "Bearer ${TOKEN_TEST_MCP}"}),
                   {"TOKEN_TEST_MCP": "secret-value"}) as d:
        p = m.Phien(d)
        server = _MayChuGia({"tools/list": _TraLoi(200, '{"result":{}}')})
        with _urlopen_gia(m, server):
            p._post({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        _, req, timeout = server.requests[0]
        bang(req.get_header("Authorization") == "Bearer secret-value", "mat auth header")
        bang(req.get_header("Mcp-protocol-version") == m._GIAO_THUC, "mat protocol header")
        bang(timeout == m._QUA_HAN_GIAY, f"timeout troi: {timeout}")
        server = _MayChuGia({"tools/list": RuntimeError("server echoed secret-value")})
        with _urlopen_gia(m, server):
            mo_ta = _hong(lambda: p._post({"method": "tools/list"}), m)
        bang("secret-value" not in mo_ta, f"lo secret qua exception: {mo_ta}")


@ca
def t05_bat_tay_giu_session_va_gui_notification(m=M):
    init = json.dumps({"jsonrpc": "2.0", "id": 1, "result": {"serverInfo": {"name": "gh"}}})
    server = _MayChuGia({
        "initialize": _TraLoi(200, init, {"X-GitHub-Request-Id": "r", "Mcp-Session-Id": "sid"}),
        "notifications/initialized": _TraLoi(202, "", {"X-GitHub-Request-Id": "r"}),
    })
    with _cau_hinh(_cfg()) as d:
        p = m.Phien(d)
        with _urlopen_gia(m, server):
            kq = p.bat_tay()
    bang(kq["serverInfo"]["name"] == "gh", f"mat result initialize: {kq}")
    bang([x[0] for x in server.requests] == ["initialize", "notifications/initialized"],
         f"sai state transition: {server.requests}")
    bang(server.requests[1][1].get_header("Mcp-session-id") == "sid", "khong giu session id")


@ca
def t06_thieu_header_github_phai_chan(m=M):
    init = json.dumps({"jsonrpc": "2.0", "id": 1, "result": {}})
    server = _MayChuGia({"initialize": _TraLoi(200, init, {})})
    with _cau_hinh(_cfg()) as d:
        with _urlopen_gia(m, server):
            mo_ta = _hong(lambda: m.Phien(d).bat_tay(), m)
    bang("proxy" in mo_ta, f"khong phan loai proxy: {mo_ta}")
    bang(len(server.requests) == 1, "da gui initialized sau response khong co header GitHub")


@ca
def t07_sse_nhieu_event_phai_lay_response_khong_lay_event_cuoi(m=M):
    raw = "\n".join([
        'event: message', 'data: {"jsonrpc":"2.0","method":"progress"}', '',
        'data: {"jsonrpc":"2.0","id":2,"result":{"ok":true}}', '',
        'data: {"jsonrpc":"2.0","method":"late-notification"}', '',
    ])
    bang(m.Phien._boc(raw).get("result") == {"ok": True}, "da lay event SSE cuoi")
    _hong(lambda: m.Phien._boc("data: not-json\n\n"), m)


@ca
def t14_sse_nhieu_data_chi_noi_trong_mot_event(m=M):
    raw = "\n".join([
        'data: {"jsonrpc":"2.0",', 'data: "id":2,"result":{"ok":true}}', '',
        'data: {"jsonrpc":"2.0","method":"khong-noi-vao-response"}', '',
    ])
    bang(m.Phien._boc(raw).get("result") == {"ok": True},
         "khong ghep cac data field trong cung SSE event")


@ca
def t15_stdio_la_khac_pham_vi_khong_phai_lech_parser(m=M):
    cfg = {"mcpServers": {"github": {"command": "github-mcp-server"}}}
    with _cau_hinh(cfg) as d:
        co_khai, _, ten, url = m._launcher._doc_mcp_json(str(d))
        bang(co_khai and ten == "github" and url is None,
             "launcher khong con cong nhan khai bao stdio")
        mo_ta = _hong(lambda: m._doc_cau_hinh(d), m)
        bang("client HTTP" in mo_ta, f"client khong khai ro pham vi HTTP: {mo_ta}")


@ca
def t16_cau_hinh_doi_giua_hai_pha_khong_tron_url_credential(m=M):
    a = _cfg("https://endpoint-a.example/mcp", {"Authorization": "token-a"})
    b = _cfg("https://endpoint-b.example/mcp", {"Authorization": "token-b"})
    with _cau_hinh(a) as d:
        tep = d / ".mcp.json"
        doc_goc = m._launcher._doc_mcp_json
        da_probe = []

        def doc_roi_doi(goc):
            ket_qua = doc_goc(goc)
            tep.write_text(json.dumps(b), encoding="utf-8")
            return ket_qua

        m._launcher._doc_mcp_json = doc_roi_doi
        goc_urlopen = m.urllib.request.urlopen
        m.urllib.request.urlopen = lambda *args, **kwargs: da_probe.append((args, kwargs))
        try:
            mo_ta = _hong(lambda: m.Phien(d), m)
        finally:
            m._launcher._doc_mcp_json = doc_goc
            m.urllib.request.urlopen = goc_urlopen
        bang("thay doi trong luc doc" in mo_ta, f"khong fail-close khi doi anh: {mo_ta}")
        bang("endpoint-a" not in mo_ta and "token-b" not in mo_ta,
             f"nhanh tu choi cho du lieu hai anh ra mo ta: {mo_ta}")
        bang(not da_probe, "cau hinh doi anh ma van tao luu luong mang")


@ca
def t08_loi_initialized_khong_duoc_nuot(m=M):
    init = json.dumps({"jsonrpc": "2.0", "id": 1, "result": {}})
    loi = json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -1}})
    server = _MayChuGia({
        "initialize": _TraLoi(200, init, {"X-GitHub-Request-Id": "r"}),
        "notifications/initialized": _TraLoi(200, loi, {"X-GitHub-Request-Id": "r"}),
    })
    with _cau_hinh(_cfg()) as d:
        with _urlopen_gia(m, server):
            mo_ta = _hong(lambda: m.Phien(d).bat_tay(), m)
    bang("notifications/initialized" in mo_ta, f"nuot loi notification: {mo_ta}")
    server.responses["initialize"] = _TraLoi(
        200, json.dumps({"id": 1, "error": {"code": -2}}), {"X-GitHub-Request-Id": "r"})
    with _cau_hinh(_cfg()) as d:
        with _urlopen_gia(m, server):
            mo_ta = _hong(lambda: m.Phien(d).bat_tay(), m)
    bang("initialize loi" in mo_ta, f"nuot loi initialize: {mo_ta}")


@ca
def t09_rpc_loi_va_ket_qua_tool_duoc_xu_ly(m=M):
    with _cau_hinh(_cfg()) as d:
        p = m.Phien(d)
        p._post = lambda than: (200, json.dumps({"id": 2, "error": {"code": 9}}), {})
        _hong(lambda: p.rpc("tools/list", {}), m)
        p._post = lambda than: (200, json.dumps({"id": 2, "result": {"tools": [
            {"name": "z"}, {"name": "a"}]}}), {})
        bang(p.liet_ke() == ["a", "z"], "tools khong duoc sap xep")
        p._post = lambda than: (200, json.dumps({"id": 2, "result": {"content": [
            {"type": "text", "text": "a"}, {"type": "image", "data": "x"},
            {"type": "text", "text": "b"}]}}), {})
        bang(p.goi("x", {}) == "a\nb", "khong loc/noi content text")
        p._post = lambda than: (200, json.dumps({"id": 2, "result": {
            "isError": "true", "content": [{"type": "text", "text": "mo rong"}]}}), {})
        bang(p.goi("x", {}) == "mo rong", "da so truthiness thay vi dung True")
        bi_mat_url = "URL-SECRET-KHONG-DUOC-LO"
        p.url = "https://" + bi_mat_url + "/mcp"
        p._post = lambda than: (200, json.dumps({"id": 2, "result": {
            "isError": True, "content": [{"type": "text", "text": "repo 404"}]}}), {})
        mo_ta = _hong(lambda: p.goi("x", {}), m)
        bang("may chu MCP bao loi" in mo_ta and "repo 404" in mo_ta,
             f"mo ta loi may chu thieu text: {mo_ta}")
        bang(bi_mat_url not in mo_ta, f"lo du lieu url trong loi: {mo_ta}")
        _hong(lambda: p.liet_ke(), m)
        p.bat_tay = lambda: {}
        phien_goc = m.Phien
        m.Phien = lambda goc: p
        try:
            with redirect_stderr(StringIO()):
                rc = m._main(["mcp_github_doc.py", "goi", "x", "{}"])
        finally:
            m.Phien = phien_goc
        bang(rc != 0, f"_main bao thanh cong cho isError=true: rc={rc}")


# Mỗi mẫu chỉ thay đúng một chốt; ca đích phải đỏ trên bản mutant tương ứng.
DOT_BIEN = [
    ("chon_khoa_theo_kieu_dict",
     '    co_khai, mo_ta, ten_chuan, url = _launcher._doc_mcp_json(str(goc))\n'
     '    anh_sau = tep.read_bytes()',
     '    co_khai, mo_ta, ten_chuan, url = _launcher._doc_mcp_json(str(goc))\n'
     '    d_mutant = json.loads(anh_truoc.decode("utf-8"))\n'
     '    if not co_khai and not isinstance(d_mutant.get("mcpServers"), dict):\n'
     '        co_khai, ten_chuan, url = True, "github", "https://du-phong.example/mcp"\n'
     '        d_mutant.pop("mcpServers", None)\n'
     '        anh_truoc = json.dumps(d_mutant).encode("utf-8")\n'
     '    anh_sau = anh_truoc',
     "t10_khoa_co_mat_hong_khong_roi_sang_du_phong"),
    ("ten_server_chi_khop_literal",
     '    co_khai, mo_ta, ten_chuan, url = _launcher._doc_mcp_json(str(goc))',
     '    co_khai, mo_ta, ten_chuan, url = _launcher._doc_mcp_json(str(goc))\n    if ten_chuan is not None and ten_chuan != "github":\n        co_khai = False',
     "t11_ten_server_casefold_phai_duy_nhat"),
    ("ten_server_mo_ho_chon_dai",
     '    co_khai, mo_ta, ten_chuan, url = _launcher._doc_mcp_json(str(goc))',
     '    co_khai, mo_ta, ten_chuan, url = _launcher._doc_mcp_json(str(goc))\n    if not co_khai and "server cung khop" in mo_ta:\n        co_khai, ten_chuan, url = True, "github", "https://mot.example/mcp"',
     "t11_ten_server_casefold_phai_duy_nhat"),
    ("bo_kiem_headers_object", '    if not isinstance(headers, dict):', '    if False:', "t01_doc_dung_server_chinh_xac_va_giai_header"),
    ("bo_chot_hai_anh_cau_hinh",
     '    if hashlib.sha256(anh_truoc).digest() != hashlib.sha256(anh_sau).digest():',
     '    if False:', "t16_cau_hinh_doi_giua_hai_pha_khong_tron_url_credential"),
    ("headers_falsy_thanh_rong", '    headers = muc["headers"] if "headers" in muc else {}',
     '    headers = muc.get("headers") or {}', "t12_headers_falsy_co_mat_phai_bi_tu_choi"),
    ("goc_mac_dinh_theo_cwd", '    return Path(ghi_de).resolve() if ghi_de else Path(__file__).resolve().parents[2]',
     '    return Path(ghi_de or ".").resolve()', "t13_goc_mac_dinh_neo_theo_tep_va_tl_goc_ghi_de"),
    ("bo_doc_port", "        _ = p.port\n", "", "t02_moi_url_tu_choi_khong_probe_khong_ro_bi_mat"),
    ("bo_userinfo", '    if (p.username, p.password) != (None, None):', '    if False:', "t02_moi_url_tu_choi_khong_probe_khong_ro_bi_mat"),
    ("bo_scheme", '    if p.scheme.lower() not in ("http", "https"):', '    if False:', "t02_moi_url_tu_choi_khong_probe_khong_ro_bi_mat"),
    ("bo_hostname", '    if not p.hostname:', '    if False:', "t02_moi_url_tu_choi_khong_probe_khong_ro_bi_mat"),
    ("lo_url_o_nhanh_port", 'raise Hong(f"`url` khong phan tich duoc ({type(e).__name__})")', 'raise Hong(f"`url` khong phan tich duoc: {url}")', "t02_moi_url_tu_choi_khong_probe_khong_ro_bi_mat"),
    ("env_thieu_thanh_rong", '            if not v:', '            if False:', "t01_doc_dung_server_chinh_xac_va_giai_header"),
    ("bo_loc_toolset", '        if len(hau_to) > 64 or not _RE_HAU_TO.fullmatch(hau_to):', '        if False:', "t03_toolset_chi_la_hau_to_path_an_toan"),
    ("ghep_toolset_bang_chuoi", '        p = p._replace(path=p.path.rstrip("/") + "/" + hau_to)', '        p = urllib.parse.urlsplit(str(url).rstrip("/") + "/" + hau_to)', "t03_toolset_chi_la_hau_to_path_an_toan"),
    ("bo_header_github", '        if not any(k.lower().startswith("x-github") for k in dau):', '        if False:', "t06_thieu_header_github_phai_chan"),
    ("bo_giu_session", '                self.phien_id = v', '                self.phien_id = None', "t05_bat_tay_giu_session_va_gui_notification"),
    ("sse_parse_tung_data", '        mau = su_kien or [raw]',
     '        mau = [d[5:].lstrip() for d in raw.splitlines() if d.startswith("data:")] or [raw]',
     "t14_sse_nhieu_data_chi_noi_trong_mot_event"),
    ("sse_lay_event_cuoi", '        for d in da_doc:\n            if "id" in d and ("result" in d or "error" in d):\n                return d', '        return da_doc[-1]', "t07_sse_nhieu_event_phai_lay_response_khong_lay_event_cuoi"),
    ("nuot_loi_initialize", '        if "error" in d:\n            raise Hong("initialize loi: " + json.dumps(d["error"], ensure_ascii=False)[:300])', '        if False:\n            raise Hong("initialize loi")', "t08_loi_initialized_khong_duoc_nuot"),
    ("nuot_loi_initialized", '            if "error" in bao:\n                raise Hong("notifications/initialized loi")', '            if "error" in bao:\n                pass', "t08_loi_initialized_khong_duoc_nuot"),
    ("nuot_loi_rpc", '        if "error" in d:\n            raise Hong(f"{method} loi: " + json.dumps(d["error"], ensure_ascii=False)[:300])', '        if False:\n            raise Hong("rpc loi")', "t09_rpc_loi_va_ket_qua_tool_duoc_xu_ly"),
    ("bo_chot_iserror", '        if isinstance(kq, dict) and kq.get("isError") is True:', '        if False:', "t09_rpc_loi_va_ket_qua_tool_duoc_xu_ly"),
]


def _phan_hang_dot_bien(q, ca_dich):
    if q.returncode == 0:
        return "song_sot"
    dau_assert = f"HONG {ca_dich}: AssertionError:"
    if any(dong.strip().startswith(dau_assert) for dong in q.stdout.splitlines()):
        return "giet_that"
    return "tin_dung_gia"


def _tu_kiem_phan_hang_dot_bien():
    class Q:
        def __init__(self, rc, stdout):
            self.returncode, self.stdout = rc, stdout

    bang(_phan_hang_dot_bien(Q(1, "HONG ca_dich: AssertionError: do chot"), "ca_dich")
         == "giet_that", "runner khong nhan AssertionError cua ca dich")
    bang(_phan_hang_dot_bien(Q(1, "HONG ca_dich: TypeError: loi vo can"), "ca_dich")
         == "tin_dung_gia", "runner cap tin dung cho TypeError")
    bang(_phan_hang_dot_bien(Q(1, "HONG ca_khac: AssertionError: sai ca"), "ca_dich")
         == "tin_dung_gia", "runner cap tin dung cho AssertionError cua ca khac")
    bang(_phan_hang_dot_bien(Q(0, ""), "ca_dich") == "song_sot",
         "runner khong nhan mutant song sot")


def _chay_dot_bien():
    _tu_kiem_phan_hang_dot_bien()
    nguon = MODUN.read_text(encoding="utf-8")
    giet_that, tin_dung_gia, song_sot = [], [], []
    with tempfile.TemporaryDirectory() as d:
        for ten, cu, moi, ca_dich in DOT_BIEN:
            n = nguon.count(cu)
            if n != 1:
                print(f"  HONG {ten}: mau khop {n}, can dung 1")
                continue
            p = Path(d, ten + ".py")
            p.write_text(nguon.replace(cu, moi, 1), encoding="utf-8")
            env = os.environ.copy()
            env["MCP_DOC_MUTANT"] = str(p)
            q = subprocess.run([sys.executable, __file__, "--ca", ca_dich],
                               capture_output=True, text=True, env=env)
            hang = _phan_hang_dot_bien(q, ca_dich)
            if hang == "giet_that":
                giet_that.append(ten)
                print(f"  GIET THAT {ten} -> {ca_dich}")
            elif hang == "tin_dung_gia":
                tin_dung_gia.append(ten)
                ly_do = next((x.strip() for x in q.stdout.splitlines()
                               if x.strip().startswith(f"HONG {ca_dich}:")),
                              f"rc={q.returncode}")
                print(f"  TIN DUNG GIA {ten} -> {ca_dich}: {ly_do}")
            else:
                song_sot.append(ten)
                print(f"  SONG SOT {ten} -> {ca_dich}")
    print(f"\nGIET THAT ({len(giet_that)}): {', '.join(giet_that) or '-'}")
    print(f"TIN DUNG GIA ({len(tin_dung_gia)}): {', '.join(tin_dung_gia) or '-'}")
    print(f"SONG SOT ({len(song_sot)}): {', '.join(song_sot) or '-'}")
    return 0 if len(giet_that) == len(DOT_BIEN) else 1


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv == ["--dot-bien"]:
        return _chay_dot_bien()
    module = _nap(Path(os.environ["MCP_DOC_MUTANT"])) if "MCP_DOC_MUTANT" in os.environ else M
    chon = argv[1] if len(argv) == 2 and argv[0] == "--ca" else None
    ds = [fn for fn in CA if chon is None or fn.__name__ == chon]
    if chon and not ds:
        print(f"khong co ca {chon}")
        return 2
    qua, hong = 0, []
    for fn in ds:
        try:
            fn(module)
            qua += 1
        except Exception as e:  # noqa: BLE001
            hong.append((fn.__name__, f"{type(e).__name__}: {e}"))
    for ten, ly_do in hong:
        print(f"  HONG {ten}: {ly_do}")
    print(f"\nmcp_github_doc tests: {qua}/{len(ds)} ca QUA (hong {len(hong)}, bo qua 0)")
    return 1 if hong else 0


if __name__ == "__main__":
    raise SystemExit(main())
