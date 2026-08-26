#!/usr/bin/env python3
"""Client MCP GitHub cứu hộ, dùng được như module lẫn CLI."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from urllib.parse import urlsplit

DIEM_CUOI = "https://api.githubcopilot.com"
HOST_CHO_PHEP = "api.githubcopilot.com"
CONG_CHO_PHEP = 443
DUONG_CHO_PHEP = ("/mcp/", "/mcp/x/actions")
PHIEN_BAN_GIAO_THUC = "2025-06-18"


def kiem_dich_den(url: str) -> None:
    """Chỉ nhận đúng origin HTTPS và hai đường MCP; không phản chiếu URL vào lỗi."""
    u = urlsplit(url)
    if u.username is not None or u.password is not None:
        raise ValueError("URL không được mang thông tin đăng nhập")
    try:
        port = u.port
    except ValueError:
        raise ValueError("cổng URL không hợp lệ") from None
    port = CONG_CHO_PHEP if port is None else port
    if u.scheme != "https":
        raise ValueError("chỉ được gửi credential qua HTTPS")
    if u.hostname != HOST_CHO_PHEP:
        raise ValueError("host nhận credential không được phép")
    if port != CONG_CHO_PHEP:
        raise ValueError("cổng nhận credential không được phép")
    if u.query or u.fragment:
        raise ValueError("URL MCP không được mang query hoặc fragment")
    if u.path not in DUONG_CHO_PHEP:
        raise ValueError("đường dẫn MCP không được phép")


class _KhongChuyenHuong(urllib.request.HTTPRedirectHandler):
    """Fail-close cho từng nhóm mã để không chuyển tiếp Authorization."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if code == 301:
            return None
        if code == 302:
            return None
        if code == 303:
            return None
        if code in (307, 308):
            return None
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_KhongChuyenHuong())


def _mo_mac_dinh(req, timeout):
    return _OPENER.open(req, timeout=timeout)


def tach_than(raw: str) -> str:
    """Lấy dòng data cuối của SSE, hoặc giữ nguyên JSON thuần; không cắt tải trọng."""
    for dong in reversed(raw.splitlines()):
        if dong.startswith("data:"):
            return dong[5:].strip()
    return raw


def loi_cua(d, can_result: bool = True):
    """Chuẩn hoá lỗi giao vận/JSON-RPC mà không bắt lỗi lập trình trần."""
    if not isinstance(d, dict):
        return f"phản hồi JSON phải là object, nhận {type(d).__name__}"
    if "_http" in d:
        return f"HTTP {d['_http']} — {str(d.get('_than', ''))[:200]}"
    if "_mang" in d:
        return f"lỗi mạng — {d['_mang']}"
    if "_tho" in d:
        return f"phản hồi không phải JSON — {str(d['_tho'])[:200]}"
    if isinstance(d.get("error"), dict):
        e = d["error"]
        return f"JSON-RPC error {e.get('code')} — {str(e.get('message', ''))[:200]}"
    if can_result and "result" not in d:
        return f"phản hồi thiếu `result` — {json.dumps(d, ensure_ascii=False)[:200]}"
    return None


def loi_cong_cu(d):
    loi = loi_cua(d)
    if loi:
        return loi
    result = d["result"]
    if isinstance(result, dict) and result.get("isError") is True:
        return "công cụ trả result.isError=true"
    return None


def rut_van_ban(kq):
    """Giữ nguyên content.text để người gọi còn json.loads được tải trọng dài."""
    if isinstance(kq, dict):
        nd = kq.get("result", {}).get("content") if isinstance(kq.get("result"), dict) else None
        if isinstance(nd, list) and nd and isinstance(nd[0], dict) and "text" in nd[0]:
            return nd[0]["text"]
    return json.dumps(kq, ensure_ascii=False, indent=2)


class Phien:
    def __init__(self, path: str = "/mcp/", token: str | None = None, mo=None, timeout: int = 90):
        self.url = DIEM_CUOI + path
        kiem_dich_den(self.url)  # chốt lúc dựng là một bất biến độc lập
        self.token = token
        self.sid: str | None = None
        self.n = 0
        self._mo = mo or _mo_mac_dinh
        self.timeout = timeout

    def goi(self, method: str, params=None, bao_tin: bool = False):
        kiem_dich_den(self.url)  # kiểm lại ngay trước mỗi lần gắn credential
        msg = {"jsonrpc": "2.0", "method": method}
        if not bao_tin:
            self.n += 1
            msg["id"] = self.n
        if params is not None:
            msg["params"] = params
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": PHIEN_BAN_GIAO_THUC,
        }
        if self.sid:
            headers["Mcp-Session-Id"] = self.sid
        req = urllib.request.Request(self.url, data=json.dumps(msg).encode(), headers=headers)
        try:
            with self._mo(req, self.timeout) as response:
                sid = response.headers.get("Mcp-Session-Id")
                if sid:
                    self.sid = sid
                raw = response.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return {"_http": e.code, "_than": e.read().decode("utf-8", "replace")}
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            return {"_mang": f"{type(e).__name__}: {e}"}
        if bao_tin or not raw.strip():
            return {}
        try:
            return json.loads(tach_than(raw))
        except ValueError:
            return {"_tho": tach_than(raw)}

    def mo_phien(self):
        kq = self.goi("initialize", {
            "protocolVersion": PHIEN_BAN_GIAO_THUC,
            "capabilities": {},
            "clientInfo": {"name": "tra-luat-cuu-ho", "version": "1"},
        })
        loi = loi_cua(kq)
        if loi:
            return {"_loi": loi}
        if not isinstance(kq.get("result"), dict) or not kq["result"]:
            return {"_loi": "initialize trả result rỗng hoặc sai dạng"}
        thong_bao = self.goi("notifications/initialized", {}, bao_tin=True)
        loi = loi_cua(thong_bao, can_result=False)
        if loi:
            return {"_loi": loi}
        return {}

    def cong_cu(self) -> list:
        d = self.goi("tools/list", {})
        return [t["name"] for t in d.get("result", {}).get("tools", [])]

    def chay(self, ten: str, doi_so: dict):
        return self.goi("tools/call", {"name": ten, "arguments": doi_so})


def main(argv: list[str]) -> int:
    argv = list(argv)
    path = "/mcp/"
    if "--path" in argv:
        i = argv.index("--path")
        if i + 1 >= len(argv):
            print("SAI ĐỐI SỐ: --path cần một giá trị", file=sys.stderr)
            return 2
        path = argv[i + 1]
        del argv[i:i + 2]
    tok = os.environ.get("GITHUB_PAT") or ""
    if not tok:
        print("KHÔNG ĐO ĐƯỢC: thiếu GITHUB_PAT", file=sys.stderr)
        return 3
    try:
        p = Phien(path, tok)
    except ValueError as e:
        print(f"KHÔNG ĐO ĐƯỢC: đích không hợp lệ — {e}", file=sys.stderr)
        return 3
    mo = p.mo_phien()
    if mo.get("_loi"):
        print(f"KHÔNG ĐO ĐƯỢC: initialize — {mo['_loi']}", file=sys.stderr)
        return 3
    if not argv or argv[0] == "--liet-ke":
        d = p.goi("tools/list", {})
        loi = loi_cua(d)
        if loi:
            print(f"KHÔNG ĐO ĐƯỢC: tools/list — {loi}", file=sys.stderr)
            return 3
        tools = d["result"].get("tools", []) if isinstance(d["result"], dict) else []
        print(f"{path}  ·  {len(tools)} công cụ")
        for tool in tools:
            print("  " + tool["name"])
        return 0
    try:
        doi_so = json.loads(argv[1]) if len(argv) > 1 else {}
    except ValueError as e:
        print(f"SAI ĐỐI SỐ: đối số phải là JSON — {e}", file=sys.stderr)
        return 2
    kq = p.chay(argv[0], doi_so)
    loi = loi_cong_cu(kq)
    if loi:
        print(f"KHÔNG ĐO ĐƯỢC: tools/call — {loi}", file=sys.stderr)
        return 3
    print(rut_van_ban(kq))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
