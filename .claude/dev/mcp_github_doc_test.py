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
from contextlib import contextmanager
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
        _hong(lambda: m._doc_cau_hinh(d), m)
    with _cau_hinh({"mcpServers": {"github": "khong-phai-object"}}) as d:
        _hong(lambda: m._doc_cau_hinh(d), m)
    with _cau_hinh({"sai-khoa": {"github": {"url": "https://x"}}}) as d:
        _hong(lambda: m._doc_cau_hinh(d), m)
    with _cau_hinh({"mcpServers": {"github": {}}}) as d:
        mo_ta = _hong(lambda: m._doc_cau_hinh(d), m)
        bang("khong khai `url`" in mo_ta, f"url rong bi phan loai sai: {mo_ta}")
    with _cau_hinh(_cfg(headers=["khong", "phai", "object"])) as d:
        _hong(lambda: m._doc_cau_hinh(d), m)


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


# Mỗi mẫu chỉ thay đúng một chốt; ca đích phải đỏ trên bản mutant tương ứng.
DOT_BIEN = [
    ("bo_kiem_tep_config", '    if not tep.is_file():', '    if False:', "t01_doc_dung_server_chinh_xac_va_giai_header"),
    ("bo_kiem_khoa_config", '    if srv is None:', '    if False:', "t01_doc_dung_server_chinh_xac_va_giai_header"),
    ("bo_kiem_muc_object", '    if not isinstance(muc, dict):', '    if False:', "t01_doc_dung_server_chinh_xac_va_giai_header"),
    ("bo_kiem_url_rong", '    if not url:', '    if False:', "t01_doc_dung_server_chinh_xac_va_giai_header"),
    ("bo_kiem_headers_object", '    if not isinstance(headers, dict):', '    if False:', "t01_doc_dung_server_chinh_xac_va_giai_header"),
    ("bo_doc_port", "        _ = p.port\n", "", "t02_moi_url_tu_choi_khong_probe_khong_ro_bi_mat"),
    ("bo_userinfo", '    if (p.username, p.password) != (None, None):', '    if False:', "t02_moi_url_tu_choi_khong_probe_khong_ro_bi_mat"),
    ("bo_scheme", '    if p.scheme.lower() not in ("http", "https"):', '    if False:', "t02_moi_url_tu_choi_khong_probe_khong_ro_bi_mat"),
    ("bo_hostname", '    if not p.hostname:', '    if False:', "t02_moi_url_tu_choi_khong_probe_khong_ro_bi_mat"),
    ("lo_url_o_nhanh_port", 'raise Hong(f"`url` khong phan tich duoc ({type(e).__name__})")', 'raise Hong(f"`url` khong phan tich duoc: {url}")', "t02_moi_url_tu_choi_khong_probe_khong_ro_bi_mat"),
    ("ten_server_khop_con", '    if "github" not in srv:', '    if not any("github" in k for k in srv):', "t01_doc_dung_server_chinh_xac_va_giai_header"),
    ("env_thieu_thanh_rong", '            if not v:', '            if False:', "t01_doc_dung_server_chinh_xac_va_giai_header"),
    ("bo_loc_toolset", '        if len(hau_to) > 64 or not _RE_HAU_TO.fullmatch(hau_to):', '        if False:', "t03_toolset_chi_la_hau_to_path_an_toan"),
    ("ghep_toolset_bang_chuoi", '        p = p._replace(path=p.path.rstrip("/") + "/" + hau_to)', '        p = urllib.parse.urlsplit(str(url).rstrip("/") + "/" + hau_to)', "t03_toolset_chi_la_hau_to_path_an_toan"),
    ("bo_header_github", '        if not any(k.lower().startswith("x-github") for k in dau):', '        if False:', "t06_thieu_header_github_phai_chan"),
    ("bo_giu_session", '                self.phien_id = v', '                self.phien_id = None', "t05_bat_tay_giu_session_va_gui_notification"),
    ("sse_lay_event_cuoi", '        for d in da_doc:\n            if "id" in d and ("result" in d or "error" in d):\n                return d', '        return da_doc[-1]', "t07_sse_nhieu_event_phai_lay_response_khong_lay_event_cuoi"),
    ("nuot_loi_initialize", '        if "error" in d:\n            raise Hong("initialize loi: " + json.dumps(d["error"], ensure_ascii=False)[:300])', '        if False:\n            raise Hong("initialize loi")', "t08_loi_initialized_khong_duoc_nuot"),
    ("nuot_loi_initialized", '            if "error" in bao:\n                raise Hong("notifications/initialized loi")', '            if "error" in bao:\n                pass', "t08_loi_initialized_khong_duoc_nuot"),
    ("nuot_loi_rpc", '        if "error" in d:\n            raise Hong(f"{method} loi: " + json.dumps(d["error"], ensure_ascii=False)[:300])', '        if False:\n            raise Hong("rpc loi")', "t09_rpc_loi_va_ket_qua_tool_duoc_xu_ly"),
]


def _chay_dot_bien():
    nguon = MODUN.read_text(encoding="utf-8")
    qua = 0
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
            if q.returncode != 0:
                qua += 1
                print(f"  DO {ten} -> {ca_dich}")
            else:
                print(f"  HONG {ten}: mutant SONG SOT")
    print(f"\nmcp_github_doc mutants: {qua}/{len(DOT_BIEN)} bi GIET")
    return 0 if qua == len(DOT_BIEN) else 1


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
